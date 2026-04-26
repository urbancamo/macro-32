# macro-32

A working environment for writing **VAX MACRO-32 assembly** in 2026: sample
programs, a grep-able reference corpus distilled from the original DEC / Compaq
manuals, tooling for JetBrains IDEs, and a Claude Code skill that forces the
model to consult the manuals instead of hallucinating from thin base-model
knowledge.

The code targets the OpenVMS V7.3 family on VAX (or AMACRO on Alpha); the
sample programs have been verified to assemble and run under SIMH.

## Layout

```
src/macro32/            Sample MACRO-32 programs (one per directory)
  helloworld/             LIB$PUT_OUTPUT -- minimal MACRO-32 image
  primes/                 Sieve + text I/O
  mandelbrot/             ASCII Mandelbrot rendered to an RMS sequential file
  smg/                    Full-screen SMG window with centered text
reference/              Greppable markdown reference corpus
  INDEX.md                Meta-index of 995 callable routines across 26
                          facilities (LIB$, STR$, MTH$, OTS$, SMG$, SYS$/$*,
                          RMS, utilities) linked to their source manuals
  VAX-VMS-731/            OpenVMS V7.3 manual set: VAX MACRO ISA & directives,
                          MACRO-32 porting guide, RTL facilities, System
                          Services, RMS, utility routines, device support,
                          Programming Concepts
  macro-made-easy/        Hunter Goatley's 12-part MACRO-32 tutorial series
  samples/                Real-world MACRO-32 source (disassembler, VMS SMP
                          kernel code, a Smalltalk-80 VM, modem driver, ...)
  pdf/                    Original PDFs, kept for provenance
tools/
  jetbrains/              VAX_MACRO_32.xml -- file-type + syntax highlighting
                          for MACRO-32 in JetBrains IDEs
  vmsdrive/               persistent telnet/DCL/DEBUG session driver --
                          daemon + thin client; lets you script DCL and
                          OpenVMS Debugger commands and capture output
  vmsftp/                 thin wrapper around tnftp(1) for pushing
                          source / pulling listings + output files
Makefile                Top-level "round-trip" targets that wire vmsftp +
                        vmsdrive together: vms-build / vms-run /
                        vms-run-input / vms-debug
.claude/skills/
  vax-macro-32/           Claude Code skill: "grep the reference before
                          answering" -- forces verification against the
                          manuals on every MACRO-32 question
```

## Why the reference corpus

Base-model knowledge of VAX MACRO-32 is thin and frequently wrong on opcode
semantics, operand order, condition-code effects, and the OpenVMS calling
standard. The 15+ manuals under `reference/VAX-VMS-731/` were converted from
PDF to markdown specifically so they can be grepped and read directly by
humans and by the `vax-macro-32` Claude skill.

Start with `reference/INDEX.md` when looking up a callable routine; grep
the individual `.md` files for instructions, directives, or addressing
modes.

## Building the samples

Each `.mar` file begins with a block comment listing the references
consulted and the exact `MACRO` / `LINK` / `RUN` commands needed on
OpenVMS. Building requires either a real VAX / Alpha / Itanium system
running OpenVMS, or SIMH with an OpenVMS hobbyist installation.

## Round-tripping against a live VAX/VMS host

`tools/vmsdrive/` and `tools/vmsftp/` make it possible to assemble,
link, run, and source-debug the samples on a real (or SIMH-emulated)
VAX/VMS box without leaving this repo, and pull listings and output
back into the source tree for verification. The top-level `Makefile`
wraps both into one-liners.

### Why two tools rather than one?

A DCL session is *stateful* (`SET DEFAULT`, debugger breakpoints,
symbol assignments persist), but file transfer is naturally one-shot.
So:

- `tools/vmsdrive/` runs a **persistent telnet daemon** that holds one
  logged-in session, plus a thin client that sends a single command
  and prints the captured output up to the next prompt. The daemon
  knows about both `$ ` (DCL) and `DBG> ` (debugger) prompts and
  switches between them transparently as your commands cause
  transitions (e.g. `RUN/DEBUG image` enters DBG> in one call;
  `EXIT` leaves it).
- `tools/vmsftp/` opens a **fresh FTP connection** for each operation
  (`put`, `get`, `ls`, `delete`), auto-detecting ASCII vs binary
  from the local file extension. No daemon -- one process per call.

Both tools force IPv4 (`-4`) because macOS's DNS64 v4-mapped-v6
synthesis breaks bare `telnet`/`ftp` against a v4-only LAN host.

### Setup

Create `.env` in the repo root (gitignored) with your VAX
credentials:

```
VMS_HOST=orac           # hostname or IP (also resolvable via /etc/hosts)
VMS_USER=mwickens
VMS_PASSWORD=secret
VMS_WORKING_DIR=CLAUDE  # optional; SET DEFAULT [.CLAUDE] after login.
                        # If the value already starts with '[', it is
                        # passed through verbatim, e.g. [MSW.MACRO32].
```

You'll also need:

- **Python 3.10+** for `vmsdrive`. The daemon uses stdlib only.
- **`tnftp`** for `vmsftp`: `brew install tnftp` (Apple removed
  `/usr/bin/ftp` in macOS 10.13).

### Quick start

```sh
# Bring up the persistent session (idempotent; just re-runs if already up)
make vms-up

# Non-interactive program -- pushes source, MACRO/LIST/DEBUG, LINK/DEBUG,
# RUN/NODEBUG, captures stdout to <name>.log, and pulls <NAME>.LIS back
# into the source dir as <name>.lis:
make vms-run PROG=helloworld/hello

# Interactive program -- same, plus answer one program prompt and (optionally)
# fetch one output file back into the source dir:
make vms-run-input PROG=primes/primesio \
                   INPUT=100 \
                   PROMPT='generate: ' \
                   OUTFILE=PRIMES.TXT

# Source-level debug session -- builds, enters the debugger, leaves you at DBG>:
make vms-debug PROG=helloworld/hello
tools/vmsdrive/vmsdrive.py dbg 'STEP'
tools/vmsdrive/vmsdrive.py dbg 'EXAMINE R0..R5,SP,PC'
tools/vmsdrive/vmsdrive.py dbg 'EXIT'

# When you're done
make vms-down
```

### What lands where

For `PROG=primes/primesio` the round trip produces:

```
src/macro32/primes/
  primesio.mar           the source you wrote (committed)
  primesio.lis           assembly listing fetched from the VAX -- gitignored
  primesio.log           captured run output -- gitignored
  primes.txt             the program's output file (if you passed OUTFILE=) -- gitignored
```

The assembly listing is invaluable for verifying that what the
assembler actually emitted matches what you intended -- check the
hex offsets next to each MACRO instruction, the relocations, and the
symbol table at the end.

### Designing for verification

Treat every change to a `.mar` as something to immediately round-trip:

1. Edit the source.
2. `make vms-run PROG=...` (or `vms-run-input`) -- it'll re-upload, rebuild,
   and re-run in one step.
3. Inspect `<name>.log` to confirm output is what you expected, and
   `<name>.lis` to confirm the assembler emitted what you intended.
4. If you want to step through, `make vms-debug PROG=...` and drive the
   debugger.

`make help` prints the full target list with the current `PROG` value.

### Lower-level tool usage

Both tools are usable directly without the Makefile. See
`tools/vmsdrive/README.md` and the docstring at the top of
`tools/vmsftp/vmsftp.py` for the full subcommand reference. Highlights:

```sh
# vmsdrive
tools/vmsdrive/vmsdrive.py start
tools/vmsdrive/vmsdrive.py cmd 'SHOW TIME'
tools/vmsdrive/vmsdrive.py cmd 'RUN MYPROG' --expect 'enter value: '
tools/vmsdrive/vmsdrive.py cmd '42'
tools/vmsdrive/vmsdrive.py dbg 'SET BREAK %LINE 49'
tools/vmsdrive/vmsdrive.py log 200          # tail the session transcript
tools/vmsdrive/vmsdrive.py stop

# vmsftp
tools/vmsftp/vmsftp.py ls                    # list the working dir
tools/vmsftp/vmsftp.py put localpath REMOTE.MAR
tools/vmsftp/vmsftp.py get REMOTE.LIS localpath.lis
tools/vmsftp/vmsftp.py delete 'REMOTE.OBJ;*'
```

## JetBrains syntax highlighting

`tools/jetbrains/VAX_MACRO_32.xml` is a ready-to-import Custom File Type
for JetBrains IDEs (IntelliJ IDEA, WebStorm, CLion, PyCharm, ...) that
highlights `.mar` / `.mac` / `.macro` files: 383 mnemonics, 88 directives,
16 registers, and 234 commonly-used RTL / RMS / SMG / SYS symbols.

**Install** (IDE must be closed):

```
macOS     ~/Library/Application Support/JetBrains/<PRODUCT><VERSION>/filetypes/
Linux     ~/.config/JetBrains/<PRODUCT><VERSION>/filetypes/
Windows   %APPDATA%\JetBrains\<PRODUCT><VERSION>\filetypes\
```

Copy `VAX_MACRO_32.xml` into that directory (create `filetypes/` if it
doesn't exist), then restart the IDE and open any `.mar` file. Colours
are controlled by *Settings -> Editor -> Color Scheme -> Custom File
Types*.

See `tools/jetbrains/README.md` for the full rundown: a UI-based
fallback install, colour-category breakdown, the known `$`-tokenizer
caveat, and how the keyword lists were generated from the reference
corpus.

## License

GPL-3.0 -- see `LICENSE`.
