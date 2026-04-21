# macro-32

This repository contains **VAX MACRO-32 assembly** only. No other languages, frameworks, or tech stacks apply — the Rails / React / Tailwind defaults in the global user CLAUDE.md are not relevant here and should be ignored.

## Always use the vax-macro-32 skill

Before reading, writing, explaining, or reviewing any MACRO-32 code in this repo, invoke the `vax-macro-32` skill (at `.claude/skills/vax-macro-32/SKILL.md`). This is mandatory — do not answer MACRO-32 questions from memory.

The skill's core rule: **grep the reference files before answering**. Base-model knowledge of MACRO-32 is thin and unreliable.

## Reference corpus (greppable markdown)

- `reference/VAX_MACRO_INSTRUCTION_SET_REF.md` — authoritative VSI/DEC manual (ISA, directives, addressing modes, full opcode table in Appendix D)
- `reference/VSI_MACRO_COMPILER.md` — MACRO Compiler porting guide, built-ins, Alpha/I64 differences
- `reference/macro-made-easy/part-*.md` — Hunter Goatley's 12-part tutorial series

Original PDFs are kept under `reference/` for provenance but should not be read directly — use the markdown versions.
