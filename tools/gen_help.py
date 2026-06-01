#!/usr/bin/env python3
"""Generate SCAVEHLP.TXT -- the in-game help text resource for SCAVE.

Authoring is done in markdown under help/.  The live game reads a flat,
ASCII-only, pre-wrapped text file with a trivial line-tag grammar:

    *TOPIC|<title>|<key>
    <body line>
    <body line>
    ...
    *TOPIC|<next title>|<key>
    ...

HELP.MAR scans for the "*TOPIC|" prefix to build its topic index, and
pages the body lines that follow each header.  A body line beginning
"*H|" is a heading: the pager strips the marker and paints the rest in
bold.  All the markdown work happens here, at build time, so the runtime
needs no markdown parser -- just a line scan.  Everything is ASCII-
sanitized and wrapped to the display width so the MACRO-32 side can paint
lines verbatim.
"""
import os
import re
import sys
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Body wrap width.  The help pager paints inside the ~78-col main display
# with a small left margin, so 76 leaves comfortable room.
WIDTH = 76

# (title, single-key shortcut, markdown source) in display order.
TOPICS = [
    ("How to Play",       "H", "help/how-to-play.md"),
    ("Artifact Glossary", "A", "help/artifact-glossary.md"),
    ("Original Manual",   "M", "reference/sorcerors-cave/sorcerers-cave-rules.md"),
]

OUT = "src/macro32/sorcerer/SCAVEHLP.TXT"

# Unicode -> ASCII replacements (vax-macro-32 skill table + a few extras
# seen in the rules text).  MACRO-32 / VMS are 7-bit ASCII only.
UNI = {
    "—": "--", "–": "-", "‒": "-", "…": "...",
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"',
    "≤": "<=", "≥": ">=", "→": "->",
    "×": "x", "÷": "/", "•": "-", " ": " ",
    "½": "1/2", "¼": "1/4", "¾": "3/4",
    "°": " deg", "é": "e", "è": "e",
    "©": "(c)", "®": "(r)", "™": "(tm)",
    "←": "<-", "↑": "^", "↓": "v", "✝": "+",
    # box-drawing -> ASCII line art (rules tables/diagrams)
    "─": "-", "│": "|", "┌": "+", "┐": "+", "└": "+", "┘": "+",
    "├": "+", "┤": "+", "┬": "+", "┴": "+", "┼": "+",
    "═": "=", "║": "|", "╔": "+", "╗": "+", "╚": "+", "╝": "+",
}


def sanitize(s):
    for u, a in UNI.items():
        s = s.replace(u, a)
    # anything still non-ASCII becomes '?', so the file is strictly 7-bit.
    return s.encode("ascii", "replace").decode("ascii")


def strip_inline(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)        # [text](url) -> text
    s = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", s)   # **bold**/*em* -> text
    s = s.replace("`", "")
    s = s.replace("*", "")                                # stray markers (e.g. multi-line italics)
    return s


def convert(md):
    """Markdown -> list of ASCII, pre-wrapped plain-text lines."""
    lines = md.replace("\r\n", "\n").split("\n")
    out = []
    para = []

    def flush_para():
        if para:
            text = " ".join(x.strip() for x in para).strip()
            del para[:]
            if text:
                out.extend(textwrap.wrap(text, WIDTH) or [""])

    for raw in lines:
        line = sanitize(raw.rstrip())
        if not line.strip():
            flush_para()
            if out and out[-1] != "":
                out.append("")
            continue
        if re.match(r"^\s*([-*_])\1{2,}\s*$", line):     # horizontal rule -> break
            flush_para()
            if out and out[-1] != "":
                out.append("")
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", line)
        if h:
            flush_para()
            level = len(h.group(1))
            title = strip_inline(h.group(2)).strip().rstrip("#").strip()
            if out and out[-1] != "":
                out.append("")
            # Tag headings with a leading "*H|" marker so the pager can
            # render them in bold; HELP.MAR strips the marker before paint.
            out.append("*H|" + (title.upper() if level <= 2 else title))
            out.append("")
            continue
        b = re.match(r"^\s*[-*+]\s+(.*)$", line)
        if b:
            flush_para()
            item = strip_inline(b.group(1)).strip()
            wrapped = textwrap.wrap(item, WIDTH - 2) or [""]
            out.append("- " + wrapped[0])
            for cont in wrapped[1:]:
                out.append("  " + cont)
            continue
        if line.count("|") >= 2:          # markdown table row: keep verbatim
            flush_para()
            out.append(strip_inline(line)[:WIDTH])
            continue
        para.append(strip_inline(line))

    flush_para()
    while out and out[-1] == "":          # trim trailing blanks
        out.pop()
    return out


def main():
    chunks = []
    for title, key, src in TOPICS:
        path = os.path.join(ROOT, src)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        # Drop a leading level-1 heading -- the topic title already names it.
        text = re.sub(r"\A\s*#\s+[^\n]*\n", "", text, count=1)
        body = convert(text)
        chunks.append("*TOPIC|%s|%s" % (title, key))
        chunks.extend(body)

    outpath = os.path.join(ROOT, OUT)
    with open(outpath, "w", encoding="ascii", newline="\n") as f:
        f.write("\n".join(chunks) + "\n")

    print("wrote %s -- %d lines, %d topics" % (OUT, len(chunks), len(TOPICS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
