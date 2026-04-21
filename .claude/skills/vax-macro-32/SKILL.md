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
1. Grep the reference files below for the mnemonic, directive, register, or concept.
2. Read the matching section before answering.
3. If the reference does not cover it, say so — do **not** guess operand forms, flag effects, or side effects.

## Reference files

All paths are relative to this skill directory.

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