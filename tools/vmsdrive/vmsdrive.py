#!/usr/bin/env python3
"""vmsdrive -- thin client that talks to vmsdrived over a Unix socket.

Subcommands:
    start                spawn the daemon and log in (idempotent)
    stop                 logout cleanly and kill the daemon
    status               daemon health + last 200 bytes of session buffer
    ping                 fast emulator liveness probe (SHOW TIME, bounded)
    cmd "<dcl>"          send a DCL command, print captured output, exit 0
    dbg "<debugger>"     send a DEBUG command, print captured output
    raw "<text>" [-e P]  send literal bytes; optionally wait for regex P
    log [N]              tail the session log (default 80 lines)

Examples:
    vmsdrive start
    vmsdrive cmd 'SHOW TIME'
    vmsdrive cmd 'SET DEFAULT [.MACRO32.SMG]'
    vmsdrive cmd 'MACRO/LIST SMGHELLO'
    vmsdrive cmd 'LINK SMGHELLO'
    vmsdrive cmd 'RUN/DEBUG SMGHELLO'
    vmsdrive dbg 'SET BREAK %LINE 42'
    vmsdrive dbg 'GO'
    vmsdrive dbg 'EXAMINE R0..R5'
    vmsdrive dbg 'EXIT'
    vmsdrive stop
"""

from __future__ import annotations
import argparse
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

SOCKET_PATH = "/tmp/vmsdrive.sock"
LOGFILE = "/tmp/vmsdrive.log"
DAEMON_SCRIPT = Path(__file__).resolve().parent / "vmsdrived.py"

# Hard ceiling (seconds) on any single emulator command. The daemon enforces
# the same cap; clamping here too keeps the socket wait bounded. Rationale: an
# unresponsive VAX must never stall the automation loop for longer than this
# (loop-spec section 8) -- "5 minutes, for example."
MAX_TIMEOUT = 300.0


def _clamp_timeout(t: float) -> float:
    return max(1.0, min(float(t), MAX_TIMEOUT))


def call(req: dict, timeout: float = 35) -> dict:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect(SOCKET_PATH)
    try:
        sock.sendall((json.dumps(req) + "\n").encode("utf-8"))
        data = b""
        while not data.endswith(b"\n"):
            chunk = sock.recv(8192)
            if not chunk:
                break
            data += chunk
    finally:
        sock.close()
    return json.loads(data.decode("utf-8")) if data else {"ok": False, "error": "no response"}


def call_safe(req: dict, timeout: float) -> dict:
    """call() but turn connection/timeout failures into a clean error dict
    instead of an uncaught traceback. A wedged emulator or daemon then becomes a
    fast non-zero exit the loop can recover from (loop-spec section 8: retry
    once, else stop the session cleanly)."""
    try:
        return call(req, timeout=timeout)
    except socket.timeout:
        return {"ok": False,
                "error": f"vmsdrive: no response within {timeout:.0f}s "
                         f"(emulator or daemon unresponsive)"}
    except (FileNotFoundError, ConnectionRefusedError):
        return {"ok": False,
                "error": "vmsdrive: daemon not running (try `make vms-up`)"}
    except OSError as e:
        return {"ok": False, "error": f"vmsdrive: socket error: {e}"}


def cmd_start() -> int:
    if os.path.exists(SOCKET_PATH):
        try:
            r = call({"action": "status"}, timeout=3)
            if r.get("ok") and r.get("alive"):
                print("daemon already running")
                return 0
        except Exception:
            pass
        os.unlink(SOCKET_PATH)
    log = open(LOGFILE, "ab")
    proc = subprocess.Popen(
        [sys.executable, str(DAEMON_SCRIPT)],
        stdout=log, stderr=log, start_new_session=True,
    )
    # Wait for the socket to appear and a status call to succeed.
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if os.path.exists(SOCKET_PATH):
            try:
                r = call({"action": "status"}, timeout=3)
                if r.get("ok") and r.get("alive"):
                    print(f"daemon up (pid {proc.pid})")
                    return 0
            except Exception:
                pass
        if proc.poll() is not None:
            print(f"daemon exited prematurely (rc={proc.returncode}); see {LOGFILE}",
                  file=sys.stderr)
            return 1
        time.sleep(0.25)
    print(f"daemon did not become ready; see {LOGFILE}", file=sys.stderr)
    return 1


def cmd_stop() -> int:
    if not os.path.exists(SOCKET_PATH):
        print("daemon not running")
        return 0
    try:
        call({"action": "shutdown"}, timeout=10)
    except Exception:
        pass
    # Daemon unlinks the socket on shutdown but be defensive.
    if os.path.exists(SOCKET_PATH):
        try:
            os.unlink(SOCKET_PATH)
        except OSError:
            pass
    print("daemon stopped")
    return 0


def cmd_status() -> int:
    if not os.path.exists(SOCKET_PATH):
        print(json.dumps({"ok": False, "error": "daemon not running"}))
        return 1
    try:
        r = call({"action": "status"}, timeout=3)
        print(json.dumps(r, indent=2))
        return 0 if r.get("ok") else 1
    except Exception as e:
        print(f"status call failed: {e}", file=sys.stderr)
        return 1


def _print_response(r: dict) -> int:
    if r.get("ok"):
        text = r.get("output", "")
        sys.stdout.write(text)
        if text and not text.endswith("\n"):
            sys.stdout.write("\n")
        return 0
    sys.stderr.write((r.get("error") or "unknown error") + "\n")
    return 1


def cmd_cmd(text: str, timeout: float, expect: str | None = None) -> int:
    timeout = _clamp_timeout(timeout)
    req = {"action": "cmd", "text": text, "timeout": timeout}
    if expect:
        req["expect"] = expect
    return _print_response(call_safe(req, timeout=timeout + 5))


def cmd_dbg(text: str, timeout: float) -> int:
    timeout = _clamp_timeout(timeout)
    return _print_response(
        call_safe({"action": "dbg", "text": text, "timeout": timeout}, timeout=timeout + 5)
    )


def cmd_raw(text: str, expect: str | None, timeout: float) -> int:
    timeout = _clamp_timeout(timeout)
    req = {"action": "raw", "text": text, "timeout": timeout}
    if expect:
        req["expect"] = expect
    return _print_response(call_safe(req, timeout=timeout + 5))


def cmd_ping(timeout: float) -> int:
    """Fast liveness probe: SHOW TIME, bounded. Exit 0 if the emulator answers,
    non-zero otherwise. Batch/test make targets call this as a preflight so a
    wedged VAX aborts the loop step in seconds instead of grinding through many
    long per-command timeouts."""
    timeout = _clamp_timeout(timeout)
    r = call_safe({"action": "cmd", "text": "SHOW TIME", "timeout": timeout},
                  timeout=timeout + 5)
    if r.get("ok"):
        out = (r.get("output") or "").strip().replace("\n", " ")
        print(f"emulator alive: {out}" if out else "emulator alive")
        return 0
    sys.stderr.write("emulator unresponsive: " + (r.get("error") or "no prompt") + "\n")
    return 1


def cmd_log(n: int) -> int:
    if not os.path.exists(LOGFILE):
        print(f"{LOGFILE} does not exist")
        return 1
    with open(LOGFILE, "rb") as f:
        data = f.read().decode("utf-8", errors="replace")
    lines = data.splitlines()
    sys.stdout.write("\n".join(lines[-n:]) + "\n")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="vmsdrive", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="action", required=True)

    sub.add_parser("start", help="spawn daemon and log in")
    sub.add_parser("stop", help="logout and stop daemon")
    sub.add_parser("status", help="daemon health and recent buffer")

    pp = sub.add_parser("ping", help="fast emulator liveness probe (SHOW TIME)")
    pp.add_argument("--timeout", type=float, default=10.0)

    pc = sub.add_parser("cmd", help="send a DCL command")
    pc.add_argument("text")
    pc.add_argument("--timeout", type=float, default=30.0)
    pc.add_argument("--expect", help="regex (bytes) to wait for instead of DCL/DBG prompt")

    pd = sub.add_parser("dbg", help="send a DEBUG command")
    pd.add_argument("text")
    pd.add_argument("--timeout", type=float, default=30.0)

    pr = sub.add_parser("raw", help="send literal bytes")
    pr.add_argument("text")
    pr.add_argument("-e", "--expect", help="regex (bytes) to wait for after sending")
    pr.add_argument("--timeout", type=float, default=10.0)

    pl = sub.add_parser("log", help="tail session log")
    pl.add_argument("n", type=int, nargs="?", default=80)

    args = p.parse_args()
    if args.action == "start":
        return cmd_start()
    if args.action == "stop":
        return cmd_stop()
    if args.action == "status":
        return cmd_status()
    if args.action == "ping":
        return cmd_ping(args.timeout)
    if args.action == "cmd":
        return cmd_cmd(args.text, args.timeout, args.expect)
    if args.action == "dbg":
        return cmd_dbg(args.text, args.timeout)
    if args.action == "raw":
        return cmd_raw(args.text, args.expect, args.timeout)
    if args.action == "log":
        return cmd_log(args.n)
    return 2


if __name__ == "__main__":
    sys.exit(main())
