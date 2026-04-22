# JetBrains Custom File Type for VAX MACRO-32

`VAX_MACRO_32.xml` is a ready-to-import JetBrains Custom File Type definition that adds syntax highlighting for `.mar` / `.mac` / `.macro` files in WebStorm, IntelliJ IDEA, CLion, PyCharm, and the other JetBrains IDEs.

## What it highlights

| Category | Colour scheme key | Count | Contents |
|---|---|---:|---|
| Keyword 1 | "Custom File Types · Keyword 1" | 383 | All VAX MACRO-32 mnemonics from the Permanent Symbol Table (Appendix D of the Reference Manual). |
| Keyword 2 | "Custom File Types · Keyword 2" | 88 | Assembler directives (`.PSECT`, `.ENTRY`, `.ASCID`, `.BLKB`, `.F_FLOATING`, …) including common abbreviations (`.EXTRN`, `.GLOBL`, `.SBTTL`, …). |
| Keyword 3 | "Custom File Types · Keyword 3" | 16 | Registers (R0–R11, AP, FP, SP, PC). |
| Keyword 4 | "Custom File Types · Keyword 4" | 234 | Commonly-used RTL calls, RMS services, symbol macros, and OpenVMS constants (LIB$\*, STR$\*, MTH$\*, OTS$\*, SMG$\*, SYS$\*, \$SSDEF, \$FABDEF, DSC$K_DTYPE_T, SS$_NORMAL, FAB/RAB field offsets, …). |

Comments start with `;`. Case-insensitive matching (VAX MACRO is case-insensitive).

## Install

1. Close JetBrains if it's open.
2. Copy `VAX_MACRO_32.xml` into the IDE's `filetypes/` directory:

   **macOS**
   ```
   ~/Library/Application Support/JetBrains/<PRODUCT><VERSION>/filetypes/
   ```
   e.g. `~/Library/Application Support/JetBrains/WebStorm2024.1/filetypes/`

   **Linux**
   ```
   ~/.config/JetBrains/<PRODUCT><VERSION>/filetypes/
   ```

   **Windows**
   ```
   %APPDATA%\JetBrains\<PRODUCT><VERSION>\filetypes\
   ```

   Create the `filetypes/` directory if it doesn't already exist.

3. Start the IDE. Open a `.mar` file — it should pick up the new file type automatically. Mnemonics, directives, registers, and RTL names will be highlighted according to your active colour scheme.

## Adjust the colours

The four keyword categories render through your active colour scheme. Tweak them here:

```
Settings -> Editor -> Color Scheme -> Custom File Types
  Keyword 1  (mnemonics)
  Keyword 2  (directives)
  Keyword 3  (registers)
  Keyword 4  (RTL/RMS/symbols)
```

## Fallback: import via the UI

If the XML file isn't picked up (JetBrains occasionally changes the schema), you can create the file type by hand:

1. `Settings -> Editor -> File Types -> "+"`
2. Name: `VAX MACRO-32`, Description: `VAX MACRO-32 assembly source (OpenVMS)`.
3. In *Syntax highlighting*:
   - **Line comment** = `;`
   - **Ignore case** checked
   - Paste the keyword lists into Keyword 1 / 2 / 3 / 4. You can copy them out of `VAX_MACRO_32.xml` directly -- each `<keyword name="..."/>` line gives you one word per line.
4. In *File name patterns*, add `*.mar`, `*.mac`, `*.macro`.

## A known wart

The JetBrains Custom File Type tokenizer treats `$` as a word boundary. That means a token like `LIB$GET_INPUT` is split into `LIB`, `$`, `GET_INPUT`, and the keyword-4 list *may* not match it as a single word. If you find the RTL names aren't colouring the way you expect, two options:

1. Live with it -- mnemonics/directives/registers cover 90% of what's visually distinctive in MACRO code.
2. Upgrade to a TextMate bundle (`*.tmLanguage.json`), which supports arbitrary token grammar. WebStorm imports via `Settings -> Editor -> TextMate Bundles`. No pre-built MACRO-32 bundle exists that I know of, so you'd author one.

## Regenerate

The XML was generated from the reference corpus in this repo: mnemonics from `reference/VAX-VMS-731/vax-macro-ref-2001.md` (Appendix D, Table D-1) and directives from Chapter 6 of the same manual. The registers and Keyword-4 list are hand-curated. If you update the reference manuals, the keyword lists can be regenerated from them.
