---
name: vax-macro-32
description: Use when reading, writing, or debugging VAX MACRO-32 assembly (.MAR/.MAC/.MACRO files), including VMS calling standard, PSECTs, condition codes, macro directives, or porting MACRO-32 code to Alpha/Itanium. Base-model knowledge of this ISA is unreliable — always consult references.
---

# VAX MACRO-32

## Overview
Assembly language for the VAX architecture (32-bit, CISC, variable-length instructions). Training-data knowledge of MACRO-32 is thin and frequently wrong on opcodes, operand encoding, addressing modes, and VMS conventions. **Always grep the reference files before writing or explaining code.**

## Source file constraint: ASCII only
MACRO-32 source files (`.MAR`, `.MAC`, `.MACRO`) **must contain only 7-bit ASCII characters** — no Unicode. The VAX MACRO assembler expects ASCII, and source that travels to a VAX/Alpha system (via SIMH, a real system, or any VMS toolchain) must be round-trippable through DEC Multinational Character Set / ISO-8859-1 without loss. This applies to *everything* in the file, including comments.

Common offenders and their ASCII replacements:

| Don't use                      | Use instead        |
|--------------------------------|--------------------|
| `—` (em-dash)                  | `--`               |
| `–` (en-dash)                  | `-`                |
| `…` (ellipsis)                 | `...`              |
| `≤` `≥`                        | `<=` `>=`          |
| `→`                            | `->`               |
| `²` `³`                        | `^2` `^3` or `**2` |
| `'` `'` `"` `"` (curly quotes) | `'` `"`            |
| `×` `÷`                        | `*` `/`            |

This constraint applies to source files only; markdown docs and skill files in this repo are free to use Unicode.

## When to Use
- File extensions: `.MAR`, `.MAC`, `.MACRO`
- Directives like `.PSECT`, `.ENTRY`, `.MACRO`, `.ENDM`, `.ADDRESS`, `.LONG`
- Mnemonics such as `MOVL`, `MOVAL`, `PUSHL`, `CALLS`, `CALLG`, `RET`, `BSBW`, `JSB`, `CHMK`
- Questions about the VMS calling standard, argument lists, register save masks, or condition handling
- Reading, porting, or modernizing code from VMS systems (VAX → Alpha / I64)

## Retrieval workflow
1. **For a callable routine** (`LIB$*`, `STR$*`, `MTH$*`, `OTS$*`, `SMG$*`, `$*`, `SYS$*`, RMS, utility facilities): start at `../../../reference/INDEX.md` — a 995-routine meta-index grouped by facility, with direct links into the per-manual sections. Finding a routine here is faster than grepping individual files.
2. **For instructions, directives, or addressing modes:** grep the MACRO-32 reference files listed below.
3. Read the matching section before answering.
4. If the reference does not cover it, say so — do **not** guess operand forms, flag effects, calling conventions, or side effects.

## Reference files

All paths are relative to this skill directory.

### Meta-index — `../../../reference/INDEX.md`
**Start here for callable routines.** 995 routines across 26 facilities (LIB$, STR$, MTH$, OTS$, SMG$, SYS$/$*, RMS, and every utility prefix), each linked to its section in the source manual. Grouped by facility, alphabetical within each group. Faster than grepping — use the meta-index first, then follow the link.

### Primary — `../../../reference/VAX-VMS-731/vax-macro-ref-2001.md`
The authoritative VAX MACRO and Instruction Set Reference Manual — the canonical language reference. Use this first for anything about the language itself.

| Looking for…                                                      | Go to                                                             |
|-------------------------------------------------------------------|-------------------------------------------------------------------|
| Instruction semantics, operand specifiers, condition-code effects | Chapter 9 — grep for `# **9**` then `### **VAX Instruction Set**` |
| Addressing modes + their encodings                                | Chapter 5                                                         |
| Assembler directives (`.PSECT`, `.ENTRY`, `.MACRO`, …)            | Chapter 6                                                         |
| Source statement format, symbols, numbers, expressions            | Chapters 2–3                                                      |
| Macro arguments, string operators, keyword args                   | Chapter 4                                                         |
| Data types and basic architecture                                 | Chapters 7–8                                                      |
| Vector instructions                                               | Chapter 10                                                        |
| **Hex opcode → mnemonic lookup**                                  | Appendix D (`Table D.1` alphabetic, `D.2` numeric)                |
| ASCII / hex-decimal tables                                        | Appendices A, B                                                   |
| Directives + language summary                                     | Appendix C                                                        |
| Exceptions during execution                                       | Appendix E                                                        |

### Secondary — `../../../reference/VAX-VMS-731/macro32-porting-2001.md`
The canonical OpenVMS MACRO-32 Porting and User's Guide. Use when the question is about *how code runs on Alpha* rather than pure VAX, compiler behaviour, or compiler built-ins.

| Looking for…                                         | Go to                 |
|------------------------------------------------------|-----------------------|
| Porting VAX MACRO to Alpha                           | Chapters 1, 3         |
| How to use the MACRO-32 compiler                     | Chapter 2             |
| Performance tuning for ported code                   | Chapter 4             |
| 64-bit addressing                                    | Chapter 5, Appendix E |
| Compiler qualifiers (`/qualifiers`)                  | Appendix A            |
| Specialized directives (compiler-only)               | Appendix B            |
| **Compiler built-ins** (Alpha instructions, PALcode) | Appendix C            |
| Porting macros VAX→Alpha                             | Appendix D            |

### OpenVMS Run-Time Library — `../../../reference/VAX-VMS-731/rtl-*.md`
The RTL provides callable routines (`CALLS`/`CALLG`) for resource allocation, data conversion, I/O, math, screen handling, string manipulation, and language support. Per-routine entries include Format, Arguments (with OpenVMS usage / type / access / mechanism), Description, Condition Values Returned, and Examples.

| Facility | File         | What's in it                                                                                                                                                                                                                                              |
|----------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **LIB$** | `rtl-lib.md` | Resource allocation (virtual memory, event flags), data type conversions, common-area I/O, condition handling, CRC, tree building, date/time, signal handling. Callable as `LIB$GET_INPUT`, `LIB$PUT_OUTPUT`, `LIB$SIGNAL`, `LIB$STOP`, `LIB$SPAWN`, etc. |
| **STR$** | `rtl-str.md` | String manipulation (`STR$COPY_R`, `STR$CONCAT`, `STR$COMPARE`, descriptor manipulation)                                                                                                                                                                  |
| **MTH$** | `rtl-mth.md` | Math (integer + floating-point functions — D, F, G, H, S, T floats, trig, log, hyperbolic, complex)                                                                                                                                                       |
| **OTS$** | `rtl-ots.md` | General-purpose language support (division, conversion, copy, fill, move — the runtime helpers the compilers emit calls to)                                                                                                                               |
| **SMG$** | `rtl-smg.md` | Screen Management — terminal pasteboard/virtual display, menus, input fields, keypad definition                                                                                                                                                           |

### OpenVMS System Services — `../../../reference/VAX-VMS-731/system-services-*.md`
The `SYS$*` / `$*` services (`$QIO`, `$GETJPI`, `$CREPRC`, `$CRETVA`, `$DELTVA`, `$CMKRNL`, `$CMEXEC`, etc.) — kernel-level routines for process control, I/O, memory, synchronization, logical names, security. Per-service entries include Format, C Prototype, Arguments, Privileges, Required Quota, Related Services, Condition Values.

| File                          | Coverage                                                                      |
|-------------------------------|-------------------------------------------------------------------------------|
| `system-services-a-g-2003.md` | `$ABORT_IO` … `$GETUAI` (2003 HP edition — **prefer this**)                   |
| `system-services-g-z-2003.md` | `$GETUTC` … `$WRITE` (2003 HP edition — **prefer this**)                      |
| `system-services-a-g-2002.md` | 2002 Compaq edition — older; check only if the 2003 version dropped something |
| `system-services-g-z-2002.md` | 2002 Compaq edition — older; same caveat                                      |

### Record Management Services (RMS)
| File                                                        | Purpose                                                                                                                                             |
|-------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| `../../../reference/VAX-VMS-731/rms-reference.md`           | RMS reference — file control blocks (FAB, RAB, NAM, XAB), record operations (`$CREATE`, `$OPEN`, `$GET`, `$PUT`, `$UPDATE`), all file organizations |
| `../../../reference/VAX-VMS-731/file-applications-guide.md` | How to structure RMS programs — record formats, access modes, sharing, best practices                                                               |

### Utility Routines — `../../../reference/VAX-VMS-731/utility-routines.md`
Callable interfaces to OpenVMS utilities: SOR (SORT/MERGE), DCX (data compression), PSM (print symbiont modification), EDT, LBR (librarian), NCS (national character set), etc. Use when a program needs to invoke a utility's functionality rather than spawn the command.

### VAX Device Support — `../../../reference/VAX-VMS-731/vax-device-support-ref.md`
Reference companion to the Device Support Manual. Use only when writing or reading VAX device drivers — data structures (UCB, CRB, IRP), driver entry points, IOC routines.

### OpenVMS System Manager's Manual — `../../../reference/VAX-VMS-731/system-manager-vol{1,2}.md`
Two-volume system administration reference for OpenVMS V7.3-1. Use when the question is *how to operate or configure the OpenVMS system itself* -- starting/stopping the system, managing devices and disks, setting up print and batch queues, system tuning, clusters, networking. Particularly important for this repo: chapters 13-14 of vol1 cover the print queue manager (`INITIALIZE/QUEUE`, `START/QUEUE`, `/PROCESSOR=`, characteristics, forms) which is what every custom symbiont (`src/macro32/symbiont/`) plugs into.

| Volume                                                         | Coverage                                                                                                                                                                                                                                                                                                                              |
|----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `system-manager-vol1.md` (Essentials)                          | Startup/shutdown (Ch.4), system time (Ch.6), storage media (Ch.9), files & directories (Ch.10), BACKUP (Ch.11), **queue manager** (Ch.13), **setting up + maintaining queues** (Ch.14)                                                                                                                                                |
| `system-manager-vol2.md` (Tuning, Monitoring, Complex Systems) | File system data caches (Ch.18), UETP system test (Ch.19), resource tracking (Ch.21), OpenVMS Cluster (Ch.22), networking (Ch.23), LAN software (Ch.24), InfoServer (Ch.25), DECdtm (Ch.27), special envs (Ch.28), **Files-11 on-disk structure** (App.A), TDF tables (App.B), Compaq MIB subagents (App.C), OpenVMS Registry (App.D) |

### OpenVMS User's Manual — `../../../reference/VAX-VMS-731/users-manual.md`
End-user reference for OpenVMS V7.3-1: how to log in, work at the DCL prompt, manage files, and write command procedures. Use when the question is *how to drive the system* rather than *how to write code that runs on it* -- e.g. "what does `$ SHOW SYMBOL` do", "how does logical-name resolution interact with `SYS$LOGIN`", "what's the syntax for a `COPY` over DECnet". Many MACRO-32 build / link / run / debug recipes ultimately go through DCL, so this is the reference for the surrounding command flow.

| Looking for…                                                                  | Go to      |
|-------------------------------------------------------------------------------|------------|
| **Logging in / out**, password rules, login classes, terminal characteristics | Chapter 1  |
| File specifications, wildcards, versions, network paths                       | Chapter 3  |
| Directory structure, default directories, search lists                        | Chapter 4  |
| EVE editor (text editing)                                                     | Chapter 8  |
| SORT and MERGE                                                                | Chapter 9  |
| **Symbols** (`$ x = …`), **defining DCL commands**, expressions               | Chapter 12 |
| **Command procedures** (`.COM` scripts) -- intro                              | Chapter 13 |
| **Advanced DCL programming**: control flow, parameters, error handling        | Chapter 14 |
| Processes, subprocesses, batch jobs, `SUBMIT` / `STOP`                        | Chapter 16 |
| ASCII / DEC Multinational / ISO-Latin-1 character sets                        | Appendix A |
| **Annotated example command procedures**                                      | Appendix B |

### OpenVMS Debugger — `../../../reference/VAX-VMS-731/debugger-manual.md`
Full reference for the OpenVMS Debugger (DBG / RUN/DEBUG). Covers both command-line and screen modes, with extensive content on debugging assembly-language programs (instruction-stream stepping, register/memory examination, breakpoints, watchpoints, traceback). Use when the question is *how to debug* a MACRO-32 program, not *what does this instruction do*.

| Looking for…                                                 | Go to           |
|--------------------------------------------------------------|-----------------|
| Getting started, command format, sessions                    | Chapters 1–2    |
| Breakpoints, watchpoints, stepping, execution control        | Chapter 3       |
| EXAMINE / DEPOSIT / EVALUATE / type-aware data inspection    | Chapter 4       |
| Symbols and symbol resolution (SET/CANCEL MODULE, SET SCOPE) | Chapter 5       |
| Screen mode (windowed source/register/output displays)       | Chapter 7       |
| Heap analyser, watchpoints on dynamic memory                 | Chapter 12      |
| Special cases: optimised code, traceback, exceptions         | Chapter 14      |
| Multiprocess and threaded programs                           | Chapters 15, 17 |
| **Full DBG command dictionary (alphabetical)**               | Part VI (large) |

### OpenVMS Programming Concepts — `../../../reference/VAX-VMS-731/programming-concepts-vol{1,2}.md`
Two-volume concept manual. These are prose references, not routine dictionaries — use for background when the per-routine manuals don't explain *how the pieces fit together*. Best grepped directly on the topic word.

| Volume                         | Coverage                                                                                                                                                                                                                             |
|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `programming-concepts-vol1.md` | Process creation and control, SMP synchronization, ASTs and condition handling, memory management, 64-bit addressing on Alpha, alignment                                                                                             |
| `programming-concepts-vol2.md` | **OpenVMS calling standard** (Ch. 17–18), calling RTL / system services (Ch. 19–20), RTL and system-service I/O, time operations, file ops, logical names, DECdtm, user-written system services, system security, ACM authentication |

### Example programs — `../../../reference/samples/`
Real-world MACRO-32 source code, kept as optional reading for idiomatic patterns. Use these to see how features are *actually used together*, not as authoritative references — if a sample disagrees with the manual, the manual wins.

| Location                                | What to look at it for                                                                                                                                                |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `samples/mbrt1.mar`                     | Arithmetic, output via LIB$PUT_OUTPUT — self-contained Mandelbrot generator                                                                                           |
| `samples/zap.mar`                       | RMS indexed-file patching — XAB usage, bucket I/O, interactive commands                                                                                               |
| `samples/dte_hayes.mar`                 | Modem driver — channel I/O, descriptors-by-reference, callable from `SET HOST/DTE/DIAL`                                                                               |
| `samples/mdml1{a,b,c}.mar`, `miml1.mar` | ML/I macro processor port — full application split into machine-dependent + independent parts, shows how to structure a multi-module program                          |
| `samples/rc2009sc/`                     | Short textbook examples (e.g. `example5_8.mar` — computation with labelled data)                                                                                      |
| `samples/various_macro/`                | VMS utilities — privilege fixups (`fixup_setprv.mar`), AST queueing (`queue_ast.mar`), process dumps (`proc_dump.mar`), network processes                             |
| `samples/smalltalk/`                    | A full VAX/Smalltalk-80 VM — 21 modules showing non-trivial MACRO-32 architecture: arithmetic primitives, memory, graphics, I/O, file system                          |
| `samples/vax_mp/src/VMS_VSMP/`          | Kernel-mode loadable code (SIMH VMS SMP support) — advanced: `startcpu.mar`, `smpcore.mar`, `dynpatch.mar`, `timesync.mar`. Only relevant for privileged/system work. |
| `samples/vmsdisasm/`                    | VMS image disassembler — shows how to decode VAX instruction streams in MACRO-32                                                                                      |

### Textbook — `../../../reference/vax-assembly-language/baase-1992.md`
Sara Baase, *VAX Assembly Language* (Prentice Hall, 2nd ed., 1992). 534-page university textbook treating MACRO-32 as a learning vehicle for assembly-language programming on the VAX. Use for *pedagogical* explanations of why things work the way they do (the manuals tell you *what*; this tells you *why*). OCR'd from a scan via `marker-pdf` -- prose is reliable, but code listings can have OCR errors (parentheses, `+` postfix on `(Rn)+`, subscripts) and should be checked against the source PDF before being trusted as exact.

| Looking for…                                              | Go to        |
|-----------------------------------------------------------|--------------|
| Memory model, registers, addressing modes, basic ISA      | Chapters 1–4 |
| Integer arithmetic, conversion (CVTSP/CVTPL/etc.)         | Chapters 5–6 |
| Procedure calls (CALLS / CALLG, calling standard)         | Chapter 9    |
| Program sections (PSECT), expressions, symbols            | Chapter 10   |
| Macros (`.MACRO`, conditional assembly, string functions) | Chapter 11   |
| Bit and bit-field operations, sets                        | Chapter 12   |
| Floating point and packed decimal                         | Chapter 13   |
| Character strings (MOVC, CMPC, MOVTC, EDIT)               | Chapter 14   |
| Interrupts and exceptions, condition handling             | Chapter 15   |
| RMS-based I/O for assembly-language programs              | Chapter 16   |
| Instruction summary appendix                              | Appendix A   |

### Tutorial — `../../../reference/macro-made-easy/part-*.md`
Hunter Goatley's 12-part series. Use for conceptual grounding and idiomatic examples, not as an authoritative reference.

| Part        | Topic                                                 |
|-------------|-------------------------------------------------------|
| part-01     | Introductions, source format, REVERSE.MAR walkthrough |
| part-02     | Branches                                              |
| part-03     | Looping (CASE, SOBGTR, etc.)                          |
| part-04     | Calling All Code (CALLS/CALLG, calling standard)      |
| part-05     | System services                                       |
| part-06     | Character strings                                     |
| part-07     | More macros                                           |
| part-08     | Debug macros (rolling your own)                       |
| part-09     | RMS (Record Management Services)                      |
| part-10, 11 | Readin', Writin', and MACRO                           |
| part-12     | Full VAX + AXP example                                |

## Common Mistakes
- Confusing byte/word/long/quad suffixes (`MOVB` vs `MOVW` vs `MOVL` vs `MOVQ`)
- Forgetting which instructions set condition codes (N, Z, V, C) vs leave them unchanged — always check the "Condition Codes" block in Chapter 9
- Mixing up `CALLS` (args on stack, count in AP) vs `CALLG` (args in memory list)
- Assuming x86-style operand order — MACRO-32 is source-then-destination
- Omitting the register save mask word after `.ENTRY`
- Treating `MOVAL` as a load when it's an lea-style address computation
- Assuming VAX behavior holds on Alpha — check `macro32-porting-2001.md` for platform differences and built-ins
- **RMS control blocks must be longword-aligned.** `$FAB`, `$RAB`, `$NAM`, `$XAB*` all need to start on a 4-byte boundary. Emit `.ALIGN LONG` immediately before each declaration in the data PSECT; otherwise the assembler produces `%MACRO-I-GENINFO, Generated INFO: RMS BLOCK NOT LONGWORD ALIGNED`.
- **Conditional branches are byte-range only (±127 bytes).** `BLBC`, `BLBS`, `BEQL`, `BNEQ`, `BGEQ`, `BLSS`, `BGTR`, `BLEQ`, `BCC`, `BCS`, `BVC`, `BVS`, `BBC`, `BBS` — all emit an 8-bit signed displacement. If the target is further away the assembler emits `%MACRO-E-BRDESTRANG, Branch destination out of range`. Only `BRB` is byte and `BRW` is word (±32 KB); there is no "BEQLW". Workarounds when the target is far:
  - **Invert + `BRW`:** replace `BLBC R0, far` with `BLBS R0, near / BRW far / near:`
  - **Inline the action:** replace `BLBC R0, 99$` with `BLBS R0, 1$ / RET / 1$:` — useful when the distant label was just `RET` or a short cleanup.

## Red flags — stop and look it up
- You're about to state what a mnemonic does without having grepped the manual
- You're guessing an opcode hex value — grep Appendix D instead
- You're about to describe condition-code behavior from memory — it's in Chapter 9 under each instruction group
- You're porting code and haven't checked `macro32-porting-2001.md` for Alpha-specific notes