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
tools/jetbrains/        VAX_MACRO_32.xml -- file-type + syntax highlighting
                        for MACRO-32 in JetBrains IDEs
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
