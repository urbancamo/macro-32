#!/usr/bin/env python3
"""Render the last SCAVE screen from /tmp/vmsdrive.log into a 24x80 grid.

The vmsdrive transcript interleaves raw VMS output (RX) with "--- RX/TX
ts ---" annotation lines and the bytes we sent (TX).  We keep only the RX
byte runs after the last RUN of SCAVE, then run a minimal VT100 emulator
(cursor positioning, erase, SO/SI line-drawing charset) to reconstruct
the final screen.
"""
import re, sys

LOG = "/tmp/vmsdrive.log"
data = open(LOG, "rb").read()

# Start just after the last "RUN/NODEBUG SCAVE" we issued.
m = None
for m in re.finditer(rb"RUN/NODEBUG SCAVE", data):
    pass
if m:
    data = data[m.end():]

# Split on annotation markers; keep only RX segments' raw bytes.
parts = re.split(rb"--- (RX|TX) \d\d:\d\d:\d\d ---\n?", data)
# parts: [pre, 'RX'|'TX', seg, 'RX'|'TX', seg, ...]
rx = bytearray()
i = 1
while i < len(parts) - 1:
    tag = parts[i]
    seg = parts[i + 1]
    if tag == b"RX":
        rx += seg
    i += 2
if not rx:
    rx = bytearray(data)  # fallback

ROWS, COLS = 24, 80
grid = [[" "] * COLS for _ in range(ROWS)]
r = c = 0
gfx = False
# DEC special graphics -> ASCII approximations
G = {"q": "-", "x": "|", "l": "+", "k": "+", "m": "+", "j": "+",
     "n": "+", "t": "+", "u": "+", "v": "+", "w": "+", "a": ":", "~": "."}

b = rx
n = len(b)
i = 0
def put(ch):
    global c
    if 0 <= r < ROWS and 0 <= c < COLS:
        grid[r][c] = ch
    c += 1

while i < n:
    ch = b[i]
    if ch == 0x1B:  # ESC
        if i + 1 < n and b[i+1] == ord('['):
            j = i + 2
            while j < n and not (0x40 <= b[j] <= 0x7E):
                j += 1
            if j < n:
                params = b[i+2:j].decode("latin1")
                final = chr(b[j])
                if final in "Hf":
                    nums = [int(x) for x in params.split(";") if x != ""] or [1, 1]
                    if len(nums) == 1:
                        nums = [nums[0], 1]
                    r = max(0, nums[0] - 1); c = max(0, nums[1] - 1)
                elif final == "J":
                    if params in ("2", ""):
                        grid[:] = [[" "] * COLS for _ in range(ROWS)]; r = c = 0
                elif final == "K":
                    if params in ("", "0"):
                        for cc in range(c, COLS): grid[r][cc] = " "
                i = j + 1
                continue
        i += 1
        continue
    elif ch == 0x0E:  # SO -> graphics
        gfx = True; i += 1; continue
    elif ch == 0x0F:  # SI -> normal
        gfx = False; i += 1; continue
    elif ch == 0x0D:  # CR
        c = 0; i += 1; continue
    elif ch == 0x0A:  # LF
        r += 1; i += 1; continue
    elif ch == 0x08:  # BS
        c = max(0, c - 1); i += 1; continue
    elif ch == 0x09:  # TAB
        c = (c // 8 + 1) * 8; i += 1; continue
    elif 32 <= ch < 127:
        s = chr(ch)
        if gfx and s in G: s = G[s]
        put(s); i += 1; continue
    else:
        i += 1; continue

print("+" + "-" * COLS + "+")
for row in grid:
    print("|" + "".join(row) + "|")
print("+" + "-" * COLS + "+")
