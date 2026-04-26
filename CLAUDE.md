# macro-32

This repository contains **VAX MACRO-32 assembly** only. No other languages, frameworks, or tech stacks apply — the Rails / React / Tailwind defaults in the global user CLAUDE.md are not relevant here and should be ignored.

## Always use the vax-macro-32 skill

Before reading, writing, explaining, or reviewing any MACRO-32 code in this repo, invoke the `vax-macro-32` skill (at `.claude/skills/vax-macro-32/SKILL.md`). This is mandatory — do not answer MACRO-32 questions from memory.

The skill's core rule: **grep the reference files before answering**. Base-model knowledge of MACRO-32 is thin and unreliable.

## Reference corpus (greppable markdown)

- **`reference/INDEX.md`** — meta-index of 995 callable routines across all facilities (LIB$, STR$, MTH$, OTS$, SMG$, SYS$, RMS, utilities), each linked to its section. Start here when looking up a routine.
- `reference/VAX-VMS-731/` — full OpenVMS V7.3 manual set:
  - **MACRO-32 language:** `vax-macro-ref-2001.md` (ISA, directives, addressing modes, full opcode table in Appendix D), `macro32-porting-2001.md` (VAX→Alpha porting, compiler built-ins)
  - **RTL libraries:** `rtl-lib.md` (LIB$ full per-routine docs), `rtl-str.md` (STR$), `rtl-mth.md` (MTH$), `rtl-ots.md` (OTS$), `rtl-smg.md` (SMG$)
  - **System services:** `system-services-{a-g,g-z}-2003.md` (prefer), `…-2002.md` (older)
  - **RMS:** `rms-reference.md`, `file-applications-guide.md`
  - **Utilities:** `utility-routines.md`
  - **Device drivers:** `vax-device-support-ref.md`
  - **User's manual / DCL:** `users-manual.md` (logging in, file specs, **DCL symbols and command procedures** Ch. 12-14, processes/batch Ch. 16, annotated `.COM` examples in App. B)
  - **System manager's manual:** `system-manager-vol1.md` (essentials -- startup/shutdown, storage, BACKUP, **queue manager + queues** Ch. 13-14 = where symbionts plug in), `system-manager-vol2.md` (tuning/monitoring/complex -- caches, clusters, networking, **Files-11 on-disk structure** App. A)
  - **Debugger:** `debugger-manual.md` (DBG command reference, breakpoints, screen mode, full DBG command dictionary in Part VI)
  - **Programming concepts (prose):** `programming-concepts-vol1.md` (process/AST/condition handling/memory), `programming-concepts-vol2.md` (**calling standard**, calling RTL/system services, I/O, time, files, logical names, security/ACM)
- `reference/vax-assembly-language/baase-1992.md` — Sara Baase, *VAX Assembly Language* (Prentice Hall, 2nd ed., 1992). University textbook -- pedagogical companion to the manuals. OCR'd from a scan; prose is reliable, code listings should be verified against the source PDF before being trusted as exact.
- `reference/macro-made-easy/part-*.md` — Hunter Goatley's 12-part tutorial series
- `reference/samples/` — real-world MACRO-32 source (standalone tools, VMS utilities, a Smalltalk-80 VM, SMP kernel code, a disassembler) — for idiomatic patterns, not authoritative

Original PDFs are kept under `reference/pdf/` for provenance but should not be read directly — use the markdown versions above.
