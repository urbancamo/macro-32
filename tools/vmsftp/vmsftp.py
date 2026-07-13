#!/usr/bin/env python3
"""vmsftp -- thin wrapper around tnftp(1) for VAX/VMS file operations.

Each invocation opens a fresh FTP connection (no daemon), reads
credentials from .env, and runs one operation. ASCII vs binary mode is
auto-detected from the local file extension and can be overridden with
--mode.

Subcommands:
    ls [pattern]                list remote files in working dir
    put <local> [remote]        upload (mode auto-detected)
    get <remote> [local]        download (mode auto-detected)
    delete <remote>             delete one or more remote files
    raw <ftp-commands>          escape hatch: run a literal multi-line
                                FTP script (after the auto-cd into the
                                working dir)

Configuration -- same .env as vmsdrive:
    VMS_HOST           hostname of the VAX
    VMS_USER           username
    VMS_PASSWORD       password
    VMS_WORKING_DIR    optional; cd [.CLAUDE]-style on connect

Examples:
    tools/vmsftp/vmsftp.py ls
    tools/vmsftp/vmsftp.py put src/macro32/smg/SMGHELLO.mar
    tools/vmsftp/vmsftp.py get SMGHELLO.LIS
    tools/vmsftp/vmsftp.py delete 'SMGHELLO.OBJ;*'
"""

from __future__ import annotations
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

# Files that should travel as ASCII (record-mode) on a VMS server. Anything
# not listed here is treated as binary -- safer default than the other way
# around (binary-as-ASCII silently corrupts files; ASCII-as-binary is just
# a slightly less convenient line-ending situation).
ASCII_EXTS = {
    ".mar", ".mac", ".macro",        # VAX MACRO source
    ".com", ".dcl",                  # DCL command files
    ".txt", ".md", ".lis", ".log",   # text + listings
    ".for", ".pas", ".bas",          # other VMS source languages
    ".c", ".h", ".cc", ".cpp",
}


def load_env(p: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not p.exists():
        return env
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def detect_mode(path: str, override: str | None) -> str:
    if override:
        return override
    return "ascii" if Path(path).suffix.lower() in ASCII_EXTS else "binary"


def working_dir_spec(wd: str) -> str:
    return wd if wd.startswith("[") else f"[.{wd}]"


# Hard cap (seconds) on any single ftp invocation. A stalled FTP data
# connection would otherwise hang the whole build/loop indefinitely (the VAX
# shows no activity because the transfer never completes). On timeout we kill
# ftp and report failure so the caller (Makefile / loop) can retry instead of
# blocking forever -- the vmsftp analogue of vmsdrive's MAX_TIMEOUT.
FTP_TIMEOUT = 120


def run_ftp(env: dict[str, str], body: str) -> tuple[int, str]:
    host = env.get("VMS_HOST")
    user = env.get("VMS_USER")
    pw = env.get("VMS_PASSWORD")
    wd = env.get("VMS_WORKING_DIR") or ""
    if not (host and user and pw):
        sys.exit("ERROR: VMS_HOST / VMS_USER / VMS_PASSWORD must be set in .env")
    cd_line = f"cd {working_dir_spec(wd)}\n" if wd else ""
    script = f"user {user} {pw}\n{cd_line}{body}\nquit\n"
    try:
        proc = subprocess.run(
            ["ftp", "-nv", "-4", host],
            input=script, text=True, capture_output=True,
            timeout=FTP_TIMEOUT,
        )
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") + (e.stderr or "")
        return 1, out + (
            f"\nvmsftp: ftp timed out after {FTP_TIMEOUT}s "
            "(data connection stalled) -- killed; retry\n"
        )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def _scrub(out: str, env: dict[str, str]) -> str:
    """Remove credential-bearing lines from the captured transcript."""
    pw = env.get("VMS_PASSWORD", "")
    user = env.get("VMS_USER", "")
    cleaned = []
    for line in out.splitlines():
        if pw and pw in line:
            continue
        # tnftp echoes "USER msw" then "PASS xxxx" -- drop both.
        if line.startswith("USER ") or line.startswith("PASS "):
            continue
        if user and line.strip() == f"user {user} {pw}":
            continue
        cleaned.append(line)
    return "\n".join(cleaned) + ("\n" if out.endswith("\n") else "")


def _ftp_failed(out: str) -> bool:
    """True if any 5xx FTP response code appears in the transcript."""
    return bool(re.search(r"^\s*5\d\d\b", out, re.MULTILINE))


def _emit(env: dict[str, str], rc: int, out: str) -> int:
    sys.stdout.write(_scrub(out, env))
    if rc != 0 or _ftp_failed(out):
        return 1
    return 0


def cmd_ls(env, args):
    pattern = args.pattern or "*"
    rc, out = run_ftp(env, f"ls {pattern}")
    return _emit(env, rc, out)


def cmd_put(env, args):
    src = Path(args.local).expanduser()
    if not src.exists():
        sys.exit(f"local file not found: {src}")
    remote = args.remote or src.name
    mode = detect_mode(args.local, args.mode)
    rc, out = run_ftp(env, f"{mode}\nput {src} {remote}")
    return _emit(env, rc, out)


def cmd_get(env, args):
    remote = args.remote
    local = args.local or os.path.basename(remote.split(";", 1)[0])
    mode = detect_mode(local, args.mode)
    rc, out = run_ftp(env, f"{mode}\nget {remote} {local}")
    return _emit(env, rc, out)


def cmd_delete(env, args):
    # tnftp uses 'delete' (single) or 'mdelete' (glob/multi); use mdelete and
    # disable interactive confirmation with 'prompt' first.
    rc, out = run_ftp(env, f"prompt\nmdelete {args.remote}")
    return _emit(env, rc, out)


def cmd_raw(env, args):
    rc, out = run_ftp(env, args.script)
    return _emit(env, rc, out)


def main() -> int:
    p = argparse.ArgumentParser(
        prog="vmsftp", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="action", required=True)

    pl = sub.add_parser("ls", help="list remote files (default: working dir)")
    pl.add_argument("pattern", nargs="?")

    pp = sub.add_parser("put", help="upload local file")
    pp.add_argument("local")
    pp.add_argument("remote", nargs="?")
    pp.add_argument("--mode", choices=["ascii", "binary"])

    pg = sub.add_parser("get", help="download remote file")
    pg.add_argument("remote")
    pg.add_argument("local", nargs="?")
    pg.add_argument("--mode", choices=["ascii", "binary"])

    pd = sub.add_parser("delete", help="delete remote file(s) (glob ok)")
    pd.add_argument("remote")

    pr = sub.add_parser("raw", help="run a literal FTP script")
    pr.add_argument("script")

    args = p.parse_args()
    env = load_env(ENV_PATH)
    return {
        "ls": cmd_ls, "put": cmd_put, "get": cmd_get,
        "delete": cmd_delete, "raw": cmd_raw,
    }[args.action](env, args)


if __name__ == "__main__":
    sys.exit(main())
