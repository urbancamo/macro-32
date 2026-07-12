#!/usr/bin/env python3
"""vmsdrived -- persistent telnet/DCL session daemon for VAX/VMS automation.

Holds one logged-in telnet session to a VAX/VMS host, exposes a Unix-domain
socket so a thin client can send DCL and DEBUG commands and get back the
captured output up to the next prompt.

Configuration comes from .env at the repo root:
    VMS_HOST       hostname or IP of the VMS box
    VMS_USER       username
    VMS_PASSWORD   password (sent in the clear -- this is telnet)

The daemon writes its session log to /tmp/vmsdrive.log.
"""

from __future__ import annotations
import json
import logging
import os
import re
import select
import signal
import socket
import sys
import threading
import time
from pathlib import Path

SOCKET_PATH = "/tmp/vmsdrive.sock"
LOGFILE = "/tmp/vmsdrive.log"
ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

# Hard ceiling (seconds) on any single command's wait. The daemon is
# single-threaded in its accept loop, so one over-long command would block
# every later one; clamping here guarantees an unresponsive VAX can never wedge
# the daemon (or stall the automation loop) for longer than this. Mirrors
# MAX_TIMEOUT in the vmsdrive client.
MAX_TIMEOUT = 300.0

# Telnet IAC codes (RFC 854)
IAC = 0xFF
DONT, DO, WONT, WILL = 0xFE, 0xFD, 0xFC, 0xFB
SB, SE = 0xFA, 0xF0

# Prompt patterns. Anchored to the tail of the buffer so we only fire once
# the prompt has fully arrived. \Z is end-of-string in Python regex.
# DCL prompt may be customised (typical: "USER@NODE$ ") so we accept anything
# up to the dollar sign on the current line.
PROMPT_DCL = re.compile(rb"(?:^|\n)[^\n]*\$ \Z")
PROMPT_DBG = re.compile(rb"(?:^|\n)[^\n]*DBG> \Z")
PROMPT_USERNAME = re.compile(rb"(?:Username|User name):\s*\Z", re.IGNORECASE)
PROMPT_PASSWORD = re.compile(rb"Password:\s*\Z", re.IGNORECASE)
PROMPT_TAIL_RE = re.compile(r"^[^\n]*(?:\$|DBG>)\s*$")


def load_env(path: Path) -> dict:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        env[k.strip()] = v.strip()
    return env


class VMSSession:
    def __init__(self, host: str, port: int, user: str, password: str):
        self.host, self.port = host, port
        self.user, self.password = user, password
        self.sock: socket.socket | None = None
        self.buf = bytearray()
        self.lock = threading.Lock()
        self.alive = False
        self.reader: threading.Thread | None = None
        self.transcript = open(LOGFILE, "ab", buffering=0)

    def _log(self, tag: str, data: bytes) -> None:
        try:
            self.transcript.write(f"--- {tag} {time.strftime('%H:%M:%S')} ---\n".encode())
            self.transcript.write(data)
            if not data.endswith(b"\n"):
                self.transcript.write(b"\n")
        except Exception:
            pass

    def connect(self) -> None:
        logging.info("connecting to %s:%d", self.host, self.port)
        self.sock = socket.create_connection((self.host, self.port), timeout=15)
        self.sock.setblocking(False)
        self.alive = True
        self.reader = threading.Thread(target=self._read_loop, daemon=True)
        self.reader.start()

    # ---- IAC stripping ----
    # We refuse every option (WONT for any DO, DONT for any WILL). VMS handles
    # this gracefully and falls back to plain line-mode -- which is what we
    # want, since we drive the session character-by-character.
    def _process_iac(self, data: bytes) -> bytes:
        out = bytearray()
        responses = bytearray()
        i = 0
        while i < len(data):
            b = data[i]
            if b != IAC:
                out.append(b)
                i += 1
                continue
            if i + 1 >= len(data):
                break  # incomplete IAC -- drop tail; rare in practice
            cmd = data[i + 1]
            if cmd in (DO, DONT, WILL, WONT):
                if i + 2 >= len(data):
                    break
                opt = data[i + 2]
                if cmd == DO:
                    responses.extend(bytes([IAC, WONT, opt]))
                elif cmd == WILL:
                    responses.extend(bytes([IAC, DONT, opt]))
                # DONT / WONT need no response.
                i += 3
            elif cmd == SB:
                # Subnegotiation -- skip until IAC SE.
                j = i + 2
                while j + 1 < len(data) and not (data[j] == IAC and data[j + 1] == SE):
                    j += 1
                i = j + 2
            else:
                i += 2  # NOP, GA, etc.
        if responses and self.sock is not None:
            try:
                self.sock.sendall(bytes(responses))
            except OSError:
                pass
        return bytes(out)

    def _read_loop(self) -> None:
        assert self.sock is not None
        while self.alive:
            try:
                ready, _, _ = select.select([self.sock], [], [], 0.2)
                if not ready:
                    continue
                chunk = self.sock.recv(4096)
                if not chunk:
                    logging.warning("remote closed connection")
                    self.alive = False
                    return
                cleaned = self._process_iac(chunk)
                # Strip stray NUL bytes (VAX device-attribute exchange leaves
                # them in the stream).
                cleaned = cleaned.replace(b"\x00", b"")
                if cleaned:
                    self._log("RX", cleaned)
                    with self.lock:
                        self.buf.extend(cleaned)
            except OSError as e:
                logging.warning("read loop error: %s", e)
                self.alive = False
                return

    def send(self, data: bytes) -> None:
        assert self.sock is not None
        self._log("TX", data)
        self.sock.sendall(data)

    def send_line(self, text: str) -> None:
        # OpenVMS telnetd accepts CR; CRLF is also accepted. Keep CR-only so
        # echoed input matches the canonical form.
        self.send(text.encode("latin-1") + b"\r")

    def wait_for(self, patterns: list[re.Pattern], timeout: float) -> tuple[re.Pattern, str]:
        """Block until the buffer ends with one of the given patterns.

        Returns (matched-pattern, captured-text-including-the-prompt). Drains
        the matched portion from the buffer.
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not self.alive:
                raise ConnectionError("session is no longer alive")
            with self.lock:
                for p in patterns:
                    m = p.search(self.buf)
                    if m and m.end() == len(self.buf):
                        captured = bytes(self.buf[: m.end()])
                        del self.buf[: m.end()]
                        return p, captured.decode("latin-1", errors="replace")
            time.sleep(0.05)
        with self.lock:
            tail = bytes(self.buf[-200:])
        raise TimeoutError(
            f"timed out after {timeout}s waiting for prompt; buffer tail: {tail!r}"
        )

    def login(self, working_dir: str | None = None) -> None:
        logging.info("waiting for login prompt")
        self.wait_for([PROMPT_USERNAME], timeout=20)
        self.send_line(self.user)
        self.wait_for([PROMPT_PASSWORD], timeout=15)
        self.send_line(self.password)
        # First prompt after login may follow a banner / "Last interactive
        # login" message of arbitrary length.
        logging.info("waiting for first DCL prompt")
        self.wait_for([PROMPT_DCL], timeout=30)
        logging.info("logged in successfully")

        if working_dir:
            spec = working_dir if working_dir.startswith("[") else f"[.{working_dir}]"
            logging.info("setting default to %s", spec)
            with self.lock:
                self.buf.clear()
            self.send_line(f"SET DEFAULT {spec}")
            _, raw = self.wait_for([PROMPT_DCL], timeout=10)
            out = _clean_output(raw, f"SET DEFAULT {spec}")
            if "%" in out:
                # VMS error messages start with %FAC-S/I/W/E/F-...
                logging.warning("SET DEFAULT %s reported: %s", spec, out.strip())
            else:
                logging.info("default set; verifying with SHOW DEFAULT")
                self.send_line("SHOW DEFAULT")
                _, raw = self.wait_for([PROMPT_DCL], timeout=10)
                logging.info("default is now: %s",
                             _clean_output(raw, "SHOW DEFAULT").strip())

    def cmd(self, text: str, expected: list[re.Pattern], timeout: float) -> tuple[str, str]:
        """Send a line, wait for one of the expected prompts.

        Returns (matched-prompt-name, output-stripped-of-echo-and-prompt).
        """
        # Drain any unsolicited data still in the buffer (rare, but possible).
        with self.lock:
            self.buf.clear()
        self.send_line(text)
        matched, raw = self.wait_for(expected, timeout=timeout)
        return _prompt_name(matched), _clean_output(raw, text)

    def shutdown(self) -> None:
        try:
            self.send_line("LOGOUT")
        except Exception:
            pass
        self.alive = False
        try:
            assert self.sock is not None
            self.sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            assert self.sock is not None
            self.sock.close()
        except Exception:
            pass


def _prompt_name(p: re.Pattern) -> str:
    return {PROMPT_DCL: "dcl", PROMPT_DBG: "dbg",
            PROMPT_USERNAME: "username", PROMPT_PASSWORD: "password"}.get(p, "?")


def _clean_output(raw: str, sent: str) -> str:
    """Strip the leading echoed command line and the trailing prompt line."""
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    # Drop a leading echoed line that contains the sent command.
    if lines and sent.strip() and sent.strip() in lines[0]:
        lines = lines[1:]
    # Drop trailing lines that look like a DCL or DEBUG prompt.
    while lines and PROMPT_TAIL_RE.match(lines[-1]):
        lines.pop()
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


# ---- IPC server ----

def serve(session: VMSSession, sock_path: str) -> None:
    if os.path.exists(sock_path):
        os.unlink(sock_path)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(sock_path)
    os.chmod(sock_path, 0o600)
    server.listen(8)
    logging.info("listening on %s", sock_path)

    def cleanup(*_):
        logging.info("shutting down")
        try:
            session.shutdown()
        finally:
            try:
                os.unlink(sock_path)
            except OSError:
                pass
            os._exit(0)

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    while True:
        client, _ = server.accept()
        try:
            handle_client(client, session)
        except Exception as e:
            logging.exception("handler error")
            try:
                client.sendall((json.dumps({"ok": False, "error": str(e)}) + "\n").encode())
            except Exception:
                pass
        finally:
            client.close()


def handle_client(client: socket.socket, session: VMSSession) -> None:
    data = b""
    while not data.endswith(b"\n"):
        chunk = client.recv(4096)
        if not chunk:
            return
        data += chunk
    req = json.loads(data.decode("utf-8"))
    action = req.get("action")
    # Clamp to the hard ceiling so no client (present or future) can wedge the
    # single-threaded daemon past MAX_TIMEOUT.
    timeout = min(float(req.get("timeout", 30)), MAX_TIMEOUT)

    if action == "cmd":
        # Optional --expect overrides the default DCL/DBG prompt -- useful for
        # interactive programs that put up their own prompt mid-session.
        if "expect" in req:
            pat = re.compile(req["expect"].encode("latin-1"))
            patterns = [pat]
        else:
            patterns = [PROMPT_DCL, PROMPT_DBG]
        prompt, out = session.cmd(req["text"], patterns, timeout)
        resp = {"ok": True, "prompt": prompt, "output": out}
    elif action == "dbg":
        prompt, out = session.cmd(req["text"], [PROMPT_DBG, PROMPT_DCL], timeout)
        resp = {"ok": True, "prompt": prompt, "output": out}
    elif action == "raw":
        # Send arbitrary text, optionally wait for a regex.
        text = req["text"]
        session.send(text.encode("latin-1"))
        if "expect" in req:
            pat = re.compile(req["expect"].encode("latin-1"))
            _, out = session.wait_for([pat], timeout)
            resp = {"ok": True, "output": out}
        else:
            resp = {"ok": True, "output": ""}
    elif action == "status":
        with session.lock:
            tail = bytes(session.buf[-200:]).decode("latin-1", errors="replace")
        resp = {"ok": True, "alive": session.alive, "buffer_tail": tail}
    elif action == "shutdown":
        client.sendall((json.dumps({"ok": True}) + "\n").encode())
        client.close()
        session.shutdown()
        try:
            os.unlink(SOCKET_PATH)
        except OSError:
            pass
        os._exit(0)
    else:
        resp = {"ok": False, "error": f"unknown action: {action!r}"}
    client.sendall((json.dumps(resp) + "\n").encode())


def main() -> int:
    logging.basicConfig(
        filename=LOGFILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    env = load_env(ENV_PATH)
    host = env.get("VMS_HOST")
    user = env.get("VMS_USER")
    pw = env.get("VMS_PASSWORD")
    working_dir = env.get("VMS_WORKING_DIR") or None
    if not (host and user and pw):
        print("ERROR: VMS_HOST / VMS_USER / VMS_PASSWORD must be set in .env",
              file=sys.stderr)
        return 1
    session = VMSSession(host, 23, user, pw)
    try:
        session.connect()
        session.login(working_dir=working_dir)
    except Exception:
        logging.exception("login failed")
        session.shutdown()
        return 2
    serve(session, SOCKET_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
