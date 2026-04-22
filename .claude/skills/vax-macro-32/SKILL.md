---
name: vax-macro-32
description: Use when reading, writing, or debugging VAX MACRO-32 assembly (.MAR/.MAC/.MACRO files), including VMS calling standard, PSECTs, condition codes, macro directives, or porting MACRO-32 code to Alpha/Itanium. Base-model knowledge of this ISA is unreliable — always consult references.
---

# VAX MACRO-32

## Overview
Assembly language for the VAX architecture (32-bit, CISC, variable-length instructions). Training-data knowledge of MACRO-32 is thin and frequently wrong on opcodes, operand encoding, addressing modes, and VMS conventions. **Always grep the reference files before writing or explaining code.**

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

### Primary — `../../../reference/VAX_MACRO_INSTRUCTION_SET_REF.md`
The authoritative VSI/DEC manual. Use this first for anything about the language itself.

| Looking for… | Go to |
|---|---|
| Instruction semantics, operand specifiers, condition-code effects | Chapter 9 (`# **Chapter 9. VAX Instruction Set**`) |
| Addressing modes + their encodings | Chapter 5 |
| Assembler directives (`.PSECT`, `.ENTRY`, `.MACRO`, …) | Chapter 6 |
| Source statement format, symbols, numbers, expressions | Chapters 2–3 |
| Macro arguments, string operators, keyword args | Chapter 4 |
| Data types and basic architecture | Chapters 7–8 |
| Vector instructions | Chapter 10 |
| **Hex opcode → mnemonic lookup** | Appendix D (`Table D.1` alphabetic, `D.2` numeric) |
| ASCII / hex-decimal tables | Appendices A, B |
| Directives + language summary | Appendix C |
| Exceptions during execution | Appendix E |

### Secondary — `../../../reference/VSI_MACRO_COMPILER.md`
Porting guide and compiler reference. Use when the question is about *how code runs now* (Alpha/I64) rather than pure VAX.

| Looking for… | Go to |
|---|---|
| Porting VAX MACRO to Alpha or Itanium | Chapters 1, 3 |
| How the compiler differs across platforms | Chapter 2 |
| Performance tuning for ported code | Chapter 4 |
| 64-bit addressing | Chapter 5, Appendix E |
| Compiler qualifiers (`/qualifiers`) | Appendix A |
| Specialized directives (compiler-only) | Appendix B |
| **Compiler built-ins** (Alpha instr, PALcode, Itanium) | Appendix C |
| Porting macros VAX→Alpha/I64 | Appendix D |

### OpenVMS Run-Time Library — `../../../reference/VAX-VMS-731/rtl-*.md`
The RTL provides callable routines (`CALLS`/`CALLG`) for resource allocation, data conversion, I/O, math, screen handling, string manipulation, and language support. Per-routine entries include Format, Arguments (with OpenVMS usage / type / access / mechanism), Description, Condition Values Returned, and Examples.

| Facility | File | What's in it |
|---|---|---|
| **LIB$** | `rtl-lib.md` | Resource allocation (virtual memory, event flags), data type conversions, common-area I/O, condition handling, CRC, tree building, date/time, signal handling. Callable as `LIB$GET_INPUT`, `LIB$PUT_OUTPUT`, `LIB$SIGNAL`, `LIB$STOP`, `LIB$SPAWN`, etc. |
| **STR$** | `rtl-str.md` | String manipulation (`STR$COPY_R`, `STR$CONCAT`, `STR$COMPARE`, descriptor manipulation) |
| **MTH$** | `rtl-mth.md` | Math (integer + floating-point functions — D, F, G, H, S, T floats, trig, log, hyperbolic, complex) |
| **OTS$** | `rtl-ots.md` | General-purpose language support (division, conversion, copy, fill, move — the runtime helpers the compilers emit calls to) |
| **SMG$** | `rtl-smg.md` | Screen Management — terminal pasteboard/virtual display, menus, input fields, keypad definition |

For a **quick flat index** of all LIB$ routines with one-line descriptions (faster to grep than the full manual): `../../../reference/LIB_ROUTINES.md` (199 routines from the VSI wiki). Always cross-reference `rtl-lib.md` for argument specs.

### OpenVMS System Services — `../../../reference/VAX-VMS-731/system-services-*.md`
The `SYS$*` / `$*` services (`$QIO`, `$GETJPI`, `$CREPRC`, `$CRETVA`, `$DELTVA`, `$CMKRNL`, `$CMEXEC`, etc.) — kernel-level routines for process control, I/O, memory, synchronization, logical names, security. Per-service entries include Format, C Prototype, Arguments, Privileges, Required Quota, Related Services, Condition Values.

| File | Coverage |
|---|---|
| `system-services-a-g-2003.md` | `$ABORT_IO` … `$GETUAI` (2003 HP edition — **prefer this**) |
| `system-services-g-z-2003.md` | `$GETUTC` … `$WRITE` (2003 HP edition — **prefer this**) |
| `system-services-a-g-2002.md` | 2002 Compaq edition — older; check only if the 2003 version dropped something |
| `system-services-g-z-2002.md` | 2002 Compaq edition — older; same caveat |

### Record Management Services (RMS)
| File | Purpose |
|---|---|
| `../../../reference/VAX-VMS-731/rms-reference.md` | RMS reference — file control blocks (FAB, RAB, NAM, XAB), record operations (`$CREATE`, `$OPEN`, `$GET`, `$PUT`, `$UPDATE`), all file organizations |
| `../../../reference/VAX-VMS-731/file-applications-guide.md` | How to structure RMS programs — record formats, access modes, sharing, best practices |

### Utility Routines — `../../../reference/VAX-VMS-731/utility-routines.md`
Callable interfaces to OpenVMS utilities: SOR (SORT/MERGE), DCX (data compression), PSM (print symbiont modification), EDT, LBR (librarian), NCS (national character set), etc. Use when a program needs to invoke a utility's functionality rather than spawn the command.

### VAX Device Support — `../../../reference/VAX-VMS-731/vax-device-support-ref.md`
Reference companion to the Device Support Manual. Use only when writing or reading VAX device drivers — data structures (UCB, CRB, IRP), driver entry points, IOC routines.

### Older MACRO-32 editions (historical)
Superseded by the primary VSI refs at the top of this list, but occasionally contain material the VSI editions dropped:
- `../../../reference/VAX-VMS-731/vax-macro-ref-2001.md` — HP 2001 edition of the VAX MACRO Reference (older counterpart to `VAX_MACRO_INSTRUCTION_SET_REF.md`)
- `../../../reference/VAX-VMS-731/macro32-porting-2001.md` — HP 2001 edition of the MACRO-32 Porting Guide (older counterpart to `VSI_MACRO_COMPILER.md`)

### Tutorial — `../../../reference/macro-made-easy/part-*.md`
Hunter Goatley's 12-part series. Use for conceptual grounding and idiomatic examples, not as an authoritative reference.

| Part | Topic |
|---|---|
| part-01 | Introductions, source format, REVERSE.MAR walkthrough |
| part-02 | Branches |
| part-03 | Looping (CASE, SOBGTR, etc.) |
| part-04 | Calling All Code (CALLS/CALLG, calling standard) |
| part-05 | System services |
| part-06 | Character strings |
| part-07 | More macros |
| part-08 | Debug macros (rolling your own) |
| part-09 | RMS (Record Management Services) |
| part-10, 11 | Readin', Writin', and MACRO |
| part-12 | Full VAX + AXP example |

## Common Mistakes
- Confusing byte/word/long/quad suffixes (`MOVB` vs `MOVW` vs `MOVL` vs `MOVQ`)
- Forgetting which instructions set condition codes (N, Z, V, C) vs leave them unchanged — always check the "Condition Codes" block in Chapter 9
- Mixing up `CALLS` (args on stack, count in AP) vs `CALLG` (args in memory list)
- Assuming x86-style operand order — MACRO-32 is source-then-destination
- Omitting the register save mask word after `.ENTRY`
- Treating `MOVAL` as a load when it's an lea-style address computation
- Assuming VAX behavior holds on Alpha/I64 — check `VSI_MACRO_COMPILER.md` for platform differences and built-ins

## Red flags — stop and look it up
- You're about to state what a mnemonic does without having grepped the manual
- You're guessing an opcode hex value — grep Appendix D instead
- You're about to describe condition-code behavior from memory — it's in Chapter 9 under each instruction group
- You're porting code and haven't checked `VSI_MACRO_COMPILER.md` for platform-specific notes