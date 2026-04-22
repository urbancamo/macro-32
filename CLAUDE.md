# macro-32

This repository contains **VAX MACRO-32 assembly** only. No other languages, frameworks, or tech stacks apply — the Rails / React / Tailwind defaults in the global user CLAUDE.md are not relevant here and should be ignored.

## Always use the vax-macro-32 skill

Before reading, writing, explaining, or reviewing any MACRO-32 code in this repo, invoke the `vax-macro-32` skill (at `.claude/skills/vax-macro-32/SKILL.md`). This is mandatory — do not answer MACRO-32 questions from memory.

The skill's core rule: **grep the reference files before answering**. Base-model knowledge of MACRO-32 is thin and unreliable.

## Reference corpus (greppable markdown)

- **`reference/INDEX.md`** — meta-index of 995 callable routines across all facilities (LIB$, STR$, MTH$, OTS$, SMG$, SYS$, RMS, utilities), each linked to its section. Start here when looking up a routine.
- `reference/VAX_MACRO_INSTRUCTION_SET_REF.md` — authoritative VSI/DEC MACRO-32 manual (ISA, directives, addressing modes, full opcode table in Appendix D)
- `reference/VSI_MACRO_COMPILER.md` — MACRO Compiler porting guide, built-ins, Alpha/I64 differences
- `reference/LIB_ROUTINES.md` — flat 199-routine LIB$ index (one-line descriptions)
- `reference/macro-made-easy/part-*.md` — Hunter Goatley's 12-part tutorial series
- `reference/VAX-VMS-731/` — full OpenVMS V7.3 manual set:
  - **RTL libraries:** `rtl-lib.md` (LIB$ full per-routine docs), `rtl-str.md` (STR$), `rtl-mth.md` (MTH$), `rtl-ots.md` (OTS$), `rtl-smg.md` (SMG$)
  - **System services:** `system-services-{a-g,g-z}-2003.md` (prefer), `…-2002.md` (older)
  - **RMS:** `rms-reference.md`, `file-applications-guide.md`
  - **Utilities:** `utility-routines.md`
  - **Device drivers:** `vax-device-support-ref.md`
  - **Older MACRO editions:** `vax-macro-ref-2001.md`, `macro32-porting-2001.md` (superseded)

Original PDFs are kept under `reference/pdf/` for provenance but should not be read directly — use the markdown versions above.
