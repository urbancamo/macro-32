# vmsdrive

Persistent telnet/DCL session driver for VAX/VMS. Runs in two parts:

- **`vmsdrived.py`** — daemon. Holds one telnet session to the VAX, logs in
  using credentials from `.env`, and exposes a Unix-domain socket at
  `/tmp/vmsdrive.sock`. Refuses every telnet IAC option and falls back to
  raw line mode -- which is exactly what we want for scripted DCL.
- **`vmsdrive.py`** — client. Sends a single command (or arbitrary bytes)
  to the daemon, prints the captured output up to the next prompt, and
  exits. Designed to be called from shell scripts, Makefiles, or by Claude
  driving the VAX from this repo.

## Configuration

In the repo's `.env` (gitignored):

```
VMS_HOST=orac
VMS_USER=mwickens
VMS_PASSWORD=secret
VMS_WORKING_DIR=CLAUDE        # optional; SET DEFAULT [.CLAUDE] after login.
                              # If the value already starts with '[', it is
                              # passed through verbatim, e.g. [MSW.MACRO32].
```

## Usage

```sh
# bring the session up (idempotent)
tools/vmsdrive/vmsdrive.py start

# DCL commands -- output is everything between the echo line and the next prompt
tools/vmsdrive/vmsdrive.py cmd 'SHOW TIME'
tools/vmsdrive/vmsdrive.py cmd 'SET DEFAULT [.MACRO32.SMG]'
tools/vmsdrive/vmsdrive.py cmd 'MACRO/LIST SMGHELLO'
tools/vmsdrive/vmsdrive.py cmd 'LINK SMGHELLO'

# transitioning into the debugger -- `cmd` accepts either DCL or DBG prompt as the
# end of the response, so this works:
tools/vmsdrive/vmsdrive.py cmd 'RUN/DEBUG SMGHELLO'

# debugger commands -- prefer DBG> as the terminator
tools/vmsdrive/vmsdrive.py dbg 'SET BREAK %LINE 42'
tools/vmsdrive/vmsdrive.py dbg 'GO'
tools/vmsdrive/vmsdrive.py dbg 'EXAMINE R0..R5'
tools/vmsdrive/vmsdrive.py dbg 'EXIT'        # back to DCL

# escape hatch: send literal bytes, optionally wait for a regex
tools/vmsdrive/vmsdrive.py raw 'Y' --expect '\$ '

# inspect / stop
tools/vmsdrive/vmsdrive.py status
tools/vmsdrive/vmsdrive.py log 200             # tail the session log
tools/vmsdrive/vmsdrive.py stop
```

## Conventions

- All I/O is byte-level latin-1; nothing is decoded as UTF-8 because VMS
  doesn't speak it.
- Carriage returns sent are bare `\r` (matches what real terminals send).
- Stray NUL bytes from VAX terminal-attribute negotiation are stripped.
- The daemon refuses every telnet option (`WONT`/`DONT`) so VMS gives us
  a plain line-oriented stream without echo / suppress-GA quirks.
- Prompt regex matches anything ending in `$ ` (DCL) or `DBG> ` (DEBUG)
  at the tail of the buffer. Custom prompts like `MSW@ORAC$ ` work fine.

## Files

```
/tmp/vmsdrive.sock     control socket (UDS, mode 0600)
/tmp/vmsdrive.log      full session transcript + daemon log
```

## Limitations

- Single concurrent session. If you need to drive multiple VMS hosts at
  once you'd want a per-host socket path.
- `cmd` returns whatever showed up between the echo and the next prompt;
  it doesn't parse `$STATUS`. Grep the output for `%X-E-` patterns if
  you need failure detection.
- DCL `SPAWN` and other prompt-changing constructs aren't recognised.
- The daemon doesn't auto-reconnect on dropped connections -- run
  `vmsdrive stop && vmsdrive start` to recover.
