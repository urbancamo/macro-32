# The Sorcerer's Cave — VAX MACRO-32 Implementation Plan

> Solitaire port of Terence Donnelly's 1978 board game, building on the
> Casio VX-4 BASIC implementation under
> `reference/sorcerors-cave/casio-vx4-implementation/`.
>
> This document is the implementation plan. It is not the spec — the
> spec is the rules in `reference/sorcerors-cave/sorcerers-cave-rules.md`
> together with the design docs in `casio-vx4-implementation/` (rules
> analysis, requirement-2..6 for architecture/data/UI/phases, and the
> ASCII map/encoding references).

---

## 1. Goal and Scope

Build a playable, single-file-per-module solitaire implementation of
Sorcerer's Cave, running on the live VAX/VMS host via the existing
`make vms-build`/`vms-run`/`vms-debug` workflow.

**In scope (v1)**
- Solitaire play only — one party, no player interaction rules
- Full exploration: all 60 area cards, dead ends, level transitions,
  multi-level map
- Chamber draws scaled by depth (1/2/3/4 + Tomb +1 + Great Hall +2)
- All five hazards (Mutiny, Trap, Earthquake, Medusa, Ghouls)
- Stranger encounters (withdraw / attack / test) with reaction tables
- Combat with surprise, retreat, dragon-slayer bonus, Spectre rule
- Special areas: Viper Pit, Deep Pool
- All twelve treasure/artifact cards with their effects (the Casio
  build only fully implemented a subset; see `2026-04-03-not-implemented.md`)
- Scoring + curses + game over

**Deferred**
- Multi-player, trading, unions, party fights — explicitly out by the
  solitaire scope decision in `requirement-1-rules-analysis.md`
- Zombies option, special scenarios (Sorcerer's Den, Quest, Ringbearer)
- Saved games / persistent high scores (just session high score in
  memory unless we add an RMS file later)
- Sound

**Stretch goals** (only after v1 ships)
- Full creature pairing UI for combat (Casio's biggest unimplemented item)
- RMS-backed high score table
- A small "minimap" showing the explored cave layout

---

## 2. Why MACRO-32, what's different from the Casio version

The Casio version is dominated by memory pressure — 32 KB total, with
aggressive bit-packing and array elimination throughout. On the VAX
those constraints don't apply. What does matter:

| Concern                                | Casio                          | VAX MACRO-32                                           |
|----------------------------------------|--------------------------------|--------------------------------------------------------|
| Memory                                 | 32 KB total — tight            | Effectively unbounded for a game this size             |
| Display                                | 4 lines × 32 cols              | 80 × 24 — six panels worth of room                     |
| Strings                                | First-class, but expensive     | Descriptors + STR$ — explicit but cheap                |
| Random numbers                         | `RAN#`                         | `MTH$RANDOM` (or LCG seeded from `$GETTIM`)            |
| Control flow                           | `GOSUB`/`RETURN`               | `CALLS`/`RET` with PSECT-isolated statics              |
| Source files                           | One                            | Split per subsystem; LINKER joins .OBJ + IMAGELIB      |
| File I/O                               | Cassette                       | RMS, but probably not needed for v1                    |
| Input                                  | `INKEY$`                       | `SMG$READ_KEYSTROKE` (blocking — turn-based)           |
| Sleep / animation                      | n/a                            | Not needed — no real-time UI                           |

**Design implication:** the bit-packed area-card encoding the Casio
uses is still the right encoding here — it's a clean schema, not a
memory hack. We re-use it. Same for the small-pack encoding
(`type×100 + index`) and creature/treasure indices.

---

## 3. High-level architecture

### 3.1 Module decomposition

One source file per concern. All modules link into a single
`SCAVE.EXE`:

| File           | Responsibility                                                                         |
|----------------|----------------------------------------------------------------------------------------|
| `MAIN.MAR`     | Entry point, top-level state machine, main turn dispatch, game-over branch             |
| `SETUP.MAR`    | Title screen, party selection UI, deck shuffle, map init (place GATEWAY)               |
| `MAP.MAR`      | Area-card decode, movement, dead-end detection, level transitions, map state queries   |
| `CHAMBER.MAR`  | Chamber entry, small-card draw (depth-scaled), hazard dispatch, treasure pickup        |
| `STRANGER.MAR` | Stranger encounter, leader determination, reaction test, withdraw/attack/test branch   |
| `FIGHT.MAR`    | Fight setup (matching), round resolution, retreat, dragon-slayer + Spectre handling    |
| `SPECIAL.MAR`  | Viper Pit (per-segment crossing), Deep Pool (drop-then-cross), special-area UI         |
| `ARTIFACT.MAR` | Artifact menu, per-artifact handlers (Carpet, Flute, Balm, Potion, Staff, Chest, Ruby) |
| `SCORE.MAR`    | End-game scoring (creatures + treasure + dragon × 2 + Sorcerer + curses), final screen |
| `UI.MAR`       | SMG$ pasteboard/display setup, panel painters, common prompts, area visualization      |
| `RNG.MAR`      | Die rolls, Fisher-Yates shuffle, seed from `$GETTIM`                                   |
| `DATA.MAR`     | Static data: 61 area cards, 14 creature defs, 15 treasure defs, 5 hazards, name tables |
| `STATE.MAR`    | All global state PSECTs and shared symbol definitions (`SCAVE$_*` offsets)             |

`STATE.MAR` deserves a note: every other module declares the symbols it
references with `.EXTRN`, but the *definitions* live in one place so we
get exactly one storage location per piece of state. Borrowing the
VMS convention, named offsets use a `SCAVE$_` prefix and bit masks use
`SCAVE$M_`.

### 3.2 Top-level state machine

```
            +---------------+
            |   TITLE       |
            +-------+-------+
                    | EXE
                    v
            +---------------+
            | PARTY_SELECT  |<-- BS = restart
            +-------+-------+
                    | EXE
                    v
            +---------------+
            | INIT_DECKS    |
            +-------+-------+
                    |
                    v
            +---------------+
+---------> | TURN_DISPATCH | <----------+
|           +-------+-------+            |
|                   |                    |
|   +-----+---------+--------+-----+     |
|   |     |                  |     |     |
|   v     v                  v     v     |
| MOVE  USE_ARTIFACT     SHOW_INV EXIT   |
|   |                                    |
|   +-> RESOLVE_NEW_AREA                 |
|       (chamber/special/dead end) ---+  |
|                                     |  |
|       +-----------------------------+  |
|       |                                |
|       v                                |
|   FIGHT_LOOP (when triggered) -------->+
|                                        |
+-- back to TURN_DISPATCH ---------------+

(GAME_OVER from any state when GS != 0)
```

This is direct dispatch — one CALLS per state transition. There is no
formal state-machine table; the calling pattern from `MAIN.MAR` is the
machine. State is held in `STATE.MAR` globals.

### 3.3 Calling conventions

- All inter-module routines are CALLS-callable with a `.ENTRY` and a
  proper register save mask. Use `^M<R2,R3,R4,...>` for whatever each
  routine clobbers; the assembler-emitted save/restore handles cleanup.
- Local helpers within a module are JSB/RSB if leaf and small,
  otherwise CALLS. Match LIFE.MAR's pattern.
- System services use the `$XXX_S` macros from STARLET.MLB
  (`$QIO_S`, `$ASSIGN_S`, `$GETTIM_S`, ...). Hand-rolled CALLS to
  system services with N<12 args returns SS$_INSFARG — this is
  recorded in the project memory `feedback_vms_syscall_macros_not_calls.md`.
- ASCII only in source files (`.MAR`).
- Branches: byte-range conditional branches need invert+`BRW` when
  the target is more than 127 bytes away, especially in the larger
  CHAMBER and FIGHT modules.

---

## 4. Build system

The existing Makefile assumes one source per build. We extend it:

```make
# Multi-file image build. List of object base names is in
# src/macro32/sorceror/sources.list (one BASENAME per line).
PROG_DIR := src/macro32/sorceror
SOURCES  := $(shell cat $(PROG_DIR)/sources.list)
SRCS     := $(addprefix $(PROG_DIR)/, $(addsuffix .MAR, $(SOURCES)))

vms-scave-build:
	@for s in $(SOURCES); do \
	  $(VMSFTP) put $(PROG_DIR)/$$s.MAR $$s.MAR; \
	  $(VMSDRIVE) cmd "MACRO/LIST $$s"; \
	done
	@$(VMSDRIVE) cmd 'LINK/EXEC=SCAVE.EXE $(shell echo $(SOURCES) | tr ' ' ',')'
```

`sources.list` is the link order:

```
MAIN
SETUP
MAP
CHAMBER
STRANGER
FIGHT
SPECIAL
ARTIFACT
SCORE
UI
RNG
DATA
STATE
```

LINK order matters less for object code (the linker does its own symbol
resolution), but matching this order makes the listing trail readable.
Use `LINK/MAP=SCAVE.MAP` in development to see the symbol table.

For interactive testing during development, `vms-scave-debug` mirrors
`vms-debug` — `LINK/DEBUG`, then `RUN/DEBUG SCAVE`.

---

## 5. Display design (80 × 24)

The Casio's 4×32 display forces sequential, screen-at-a-time UI. With
80×24 we can keep persistent context visible. The base layout has
five SMG$ virtual displays composited on a single pasteboard:

```
+==============================================================================+
| L1 GATEWAY               Turn 12   Score: 35   Curses: 0   Party: 3          |  status
+--------+----------------------+--------------------------+--------------------+
|        |                      |                          |                    |
| PARTY  |       MAP            |     CHAMBER CONTENTS     |    LEGEND          |
|        |   (current area      |                          |                    |
|        |    visualization)    |   Strangers:             |   N/E/S/W move     |
|        |                      |     WIZARD (str 7)       |   U/D stairs       |
|        |                      |                          |   I inventory      |
|        |                      |   Treasure:              |   A artifact       |
|        |                      |     GEMS                 |   ? help           |
|        |                      |     RING                 |   X exit cave      |
|        |                      |                          |                    |
+--------+----------------------+--------------------------+--------------------+
| > A wizard regards you suspiciously...                                       |  log
| > You hear distant footsteps echoing from the south.                         |
+------------------------------------------------------------------------------+
| [W]ithdraw   [A]ttack   [T]est   [I]nventory   [?]Help   [Q]uit             |  prompt
+==============================================================================+
```

### 5.1 Five virtual displays

| Name        | Rows  | Cols  | Origin (r,c) | Border | Notes                             |
|-------------|-------|-------|--------------|--------|-----------------------------------|
| `STATUS`    | 1     | 80    | (1, 1)       | yes    | Top status bar                    |
| `PARTY`     | 16    | 12    | (3, 1)       | yes    | Party + carried treasure          |
| `MAP`       | 16    | 22    | (3, 14)      | yes    | Current area visualization        |
| `CHAMBER`   | 16    | 26    | (3, 37)      | yes    | Strangers, treasure, hazards      |
| `LEGEND`    | 16    | 19    | (3, 64)      | yes    | Static legend / context help      |
| `LOG`       | 4     | 80    | (19, 1)      | yes    | Scrolling 4-line message log      |
| `PROMPT`    | 1     | 80    | (23, 1)      | yes    | Bottom action line                |

(Borders count toward the rows/cols. Minor adjustments at impl time
once we paste them and inspect on a real terminal.)

### 5.2 Area visualization

Reuse the Casio's chamber/tunnel ASCII vocabulary
(`area-ascii-mockups.md`), scaled up to ~22 cols × ~16 rows so we have
breathing room. Walls are `#`, exits are `^v<>` arrows, stairs are `↑`
(up) and `↓` (down) — except we keep ASCII (per the project
constraint, no Unicode in `.MAR` sources). So:

| Element     | Casio glyph | MACRO-32 glyph |
|-------------|-------------|----------------|
| Wall        | `█`/`▒`     | `#`            |
| North exit  | `↑`         | `^`            |
| South exit  | `↓`         | `v`            |
| East exit   | `→`         | `>`            |
| West exit   | `<`         | `<`            |
| Stair up    | `⇑`         | `<<` or `^^`   |
| Stair down  | `⇓`         | `vv`           |
| Creature    | `nC`        | `nC`           |
| Treasure    | `$`         | `$`            |
| Artifact    | `A`         | `A`            |
| Gateway     | `G`         | `G`            |
| Deep Pool   | `D`         | `D`            |
| Viper Pit   | `V`         | `V`            |
| Tomb        | `T`         | `T`            |
| Great Hall  | `H`         | `H`            |

Example (a chamber with N+E+S+W exits, stair up, with strangers and
treasure):

```
+----------------------+
| ###     ^      ###  |
| #                #  |
| <                >  |
| #     2C  $    ^^   |
| #                #  |
| ###     v      ###  |
+----------------------+
```

A simple tunnel (E-W straight) is much sparser:

```
+----------------------+
|                      |
| ##################   |
| <                 >  |
| ##################   |
|                      |
+----------------------+
```

### 5.3 Per-screen variants

Each major game state replaces one or more panels. The `STATUS` and
`PROMPT` panels are constant across all screens. The remaining panels
specialise:

| Screen          | PARTY | MAP | CHAMBER | LEGEND |
|-----------------|-------|-----|---------|--------|
| Title           | hidden, MAP fills the area showing the title art            ||||
| Party select    | grows  to show running selection           | hidden   | catalog of available creatures   ||
| Turn dispatch   | yes   | yes | yes     | yes (key reference)                |
| Hazard event    | yes   | yes | flash banner ("!! TRAP !!", ...)             ||
| Stranger encounter | yes  | yes | strangers + leader   | encounter options ||
| Fight round     | yes (with HP-style markers for surprise/dropped treasure)        ||||
| Score screen    | escape art, summary table fills the centre                       ||||

### 5.4 Log panel

A 4-line ring buffer rendered every redraw. Each line is one short
narrative sentence: "TROLL slain." / "PRIEST falls into the pit!" /
"You hear the wizard chanting." Low-priority game messages go here so
the prompt line can stay focused on input.

---

## 6. Input model

Single-keystroke input via `SMG$READ_KEYSTROKE` (blocking — this is
turn-based; no AST machinery needed, unlike LIFE).

Universal keys:

| Key   | Action                                          |
|-------|-------------------------------------------------|
| N E S W | Move in that direction                       |
| U D     | Stairs up/down                               |
| I       | Inventory / treasure redistribution          |
| A       | Artifact menu                                |
| ?       | Help screen                                  |
| X       | Exit cave (only on level-1 stair-up area)    |
| Q       | Quit (with confirm)                          |

Modal keys (depend on current state):

| Context   | Keys                                                  |
|-----------|-------------------------------------------------------|
| Encounter | W = withdraw, A = attack, T = test                    |
| Fight end | F = fight on, R = retreat                             |
| Party 2v1 loss | 1/2 to choose preferred sacrifice               |
| Yes/No    | Y / N                                                 |
| Lists     | space or arrow / enter to confirm, BS to back         |

Echo policy: SMG$ does not echo by default; we never echo invalid keys,
only valid ones (the game responds visibly).

---

## 7. Data structures

### 7.1 Static data (DATA.MAR)

All packed exactly per `requirement-3-4-data-structures.md`:

- `AK[61]` (longwords): area-card encoding, bits per the existing scheme
- `CD[14]` (longwords): creature data, packed
  `FS*100000 + MP*10000 + (CARRY/25)*1000 + SEL*100 + PT`
- Creature names: 14 ASCID descriptors, 7 chars each fits comfortably
- Treasure data, treasure names, hazard counts and names — same idea
- Pre-built small pack of 52 cards (`type*100 + index`) — see
  Casio's lines 8500-8590
- Reaction tables for the 8 cave-creature types (hostile-max,
  indifferent-max bytes)

We don't need to bit-pack creature flags into `CD`'s low bits — we
have plenty of room for a separate `CFLAGS[14]` table with one byte
each (`SCAVE$M_INHUMAN`, `SCAVE$M_CHARISMA`, `SCAVE$M_BEFRIENDS_UNICORN`,
`SCAVE$M_GUIDES_PAST_TRAP`, `SCAVE$M_HUMAN`).

### 7.2 Dynamic state (STATE.MAR)

Single `SCAVE_STATE` PSECT with named offsets. Concrete sizes:

```
; --- top-level state ---
SCAVE_STATE_GS:    .LONG 0       ; 0=playing, 1=escaped, 2=dead, 3=quit
SCAVE_STATE_TN:    .LONG 1       ; turn counter
SCAVE_STATE_SC:    .LONG 0       ; current/final score
SCAVE_STATE_NC:    .LONG 0       ; curse count
SCAVE_STATE_SK:    .LONG 0       ; sorcerer killed flag

; --- map ---
SCAVE_MAP_NM:      .LONG 0       ; areas placed
SCAVE_MAP_PA:      .LONG 1       ; current area index (1-60)
SCAVE_MAP_PL:      .LONG 1       ; current level
SCAVE_MAP_PP:      .LONG 0       ; previous area index (for earthquake)
SCAVE_MAP_MP:      .BLKL 61      ; area-card value at each placed slot
SCAVE_MAP_ML:      .BLKL 61      ; coords (level*10000 + y*100 + x)
SCAVE_MAP_MS:      .BLKL 61      ; stair links
SCAVE_MAP_MV:      .BLKB 64      ; visited-state byte per area; .ALIGN LONG

; --- per-area persistent contents ---
SCAVE_AREA_AC:     .BLKL 61*4    ; up to 4 leftover items per area
                                 ; encoded creature=100+i, treasure=200+i
SCAVE_AREA_AF:     .BLKL 61      ; per-area flags
                                 ; bit 0 trap-active, bit 1 medusa-active,
                                 ; bit 2 quake-destroyed, bit 3 hostile,
                                 ; bit 4 perm-indiff, bit 5 statue-aroused

; --- party (max 12 -- generous) ---
SCAVE_PARTY_NP:    .LONG 0       ; living count
SCAVE_PARTY_PC:    .BLKL 12      ; creature index
SCAVE_PARTY_PS:    .BLKL 12      ; status: 0=orig, 1=ally, 2=stone, 3=dead
SCAVE_PARTY_PK:    .BLKL 12      ; dragon kills
SCAVE_PARTY_PT:    .BLKL 12*4    ; treasure slots (4 items per creature)

; --- per-chamber working set ---
SCAVE_CHAMBER_NS:  .LONG 0       ; strangers count
SCAVE_CHAMBER_NT:  .LONG 0       ; treasure count
SCAVE_CHAMBER_NH:  .LONG 0       ; hazard count
SCAVE_CHAMBER_CS:  .BLKL 8       ; stranger creature indices
SCAVE_CHAMBER_CT:  .BLKL 8       ; treasure indices
SCAVE_CHAMBER_CH:  .BLKL 4       ; hazard indices

; --- decks ---
SCAVE_DECK_LP:     .BLKL 60      ; large pack (shuffled card indices)
SCAVE_DECK_LI:     .LONG 0       ; large pack draw position
SCAVE_DECK_SP:     .BLKL 52      ; small pack (shuffled card values)
SCAVE_DECK_SI:     .LONG 0

; --- fight state ---
SCAVE_FIGHT_FA:    .BLKL 8       ; party fighter slots (front)
SCAVE_FIGHT_FD:    .BLKL 8       ; defender (stranger) slots
SCAVE_FIGHT_FB:    .BLKL 8       ; background magic supporters
SCAVE_FIGHT_NF:    .LONG 0       ; matches
SCAVE_FIGHT_FS:    .LONG 0       ; surprise (+1=us, -1=them)
SCAVE_FIGHT_RD:    .LONG 1       ; round number
SCAVE_FIGHT_POTION:.LONG -1      ; party-slot using strength-potion this fight
```

Total: roughly 2 KB. Tiny by VAX standards.

Memory layout note: nothing needs `.ALIGN QUAD` (LIFE taught us that's
a Macro error if the PSECT alignment is `LONG`). Stay at `.ALIGN LONG`
throughout.

---

## 8. Subsystem designs

### 8.1 RNG (RNG.MAR)

VAX MACRO has no native PRNG. Two options:

1. `MTH$RANDOM` from the Math RTL — entry mask `^M<>`, takes a seed by
   reference, returns a random F-floating in `[0, 1)`. Reseed once
   from `$GETTIM_S` low longword. Then a die roll is
   `INT(MTH$RANDOM(seed) * 6) + 1`.
2. Hand-rolled LCG: `s = s*1103515245 + 12345 (mod 2^31)`. Cheaper, no
   floating point. Perfectly fine for this game.

**Decision:** Hand-rolled LCG. Simpler, deterministic for testing if
we ever want a fixed seed mode, no float entanglement. Reseed from
`$GETTIM_S`'s low longword on game start.

```
; ROLL_DIE -- returns 1..6 in R0
; State: SCAVE_RNG_SEED (longword)
ROLL_DIE:
        MOVL    SCAVE_RNG_SEED, R0
        MULL2   #1103515245, R0
        ADDL2   #12345, R0
        BICL2   #^X80000000, R0     ; force positive
        MOVL    R0, SCAVE_RNG_SEED
        EXTZV   #16, #16, R0, R1    ; take middle 16 bits
        DIVL2   #10923, R1          ; 65536 / 6 ~= 10923
        ADDL3   #1, R1, R0
        CMPL    R0, #6
        BLEQ    1$
        MOVL    #6, R0
1$:     RSB
```

(Refinements expected at impl time. The middle-bits trick avoids the
classic LCG low-bit periodicity.)

Fisher-Yates shuffle uses this primitive.

### 8.2 Map (MAP.MAR)

Public surface:

| Routine          | Returns                                       |
|------------------|-----------------------------------------------|
| `DECODE_AREA`    | Given an area-card value, fills decoded       |
|                  | exits/stairs/chamber/special into a struct    |
| `MOVE_PARTY`     | Implements the move-decision dispatch         |
| `DRAW_NEW_AREA`  | Pull next from large pack, place adjacent     |
| `MARK_QUAKE`     | Seal exits on `PP` (per the unimplemented-list fix) |
| `IS_DEAD_END`    | True if target card has no matching doorway   |

Movement algorithm — same shape as Casio lines 1080-1490:

1. Decode current area; verify chosen direction has an exit.
2. Compute target coordinates `(level, y, x)` with the unit-vector
   table for {N,E,S,W,U,D}.
3. If a placed area has those coords AND a matching reverse exit,
   move there. (Bidirectional-stair bug guard from
   `SORCERER.md`: stair links are only followed when the target
   level is in the right direction.)
4. Otherwise draw new area from `LP[LI++]`. Place it at the target
   coords. If matching exit → enter it; if not → mark dead-end (clear
   the exit on the *current* card so we don't pick this direction
   again, and leave the new card placed face-down).
5. Forced redraw rule: if every exit and stair leads to a dead end and
   no other progress is possible, return the dead-end card to the
   middle of the pack and draw again.

Level bookkeeping: a stair `U` from level 1 means the cave exit is
available; `MOVE_PARTY` returns a `SCAVE$_GAME_STATUS_EXIT_AVAILABLE`
flag so `MAIN.MAR` knows to offer `[X]`.

### 8.3 Chamber (CHAMBER.MAR)

Drawn-cards pipeline on first chamber entry:

```
ENTER_CHAMBER:
    if !first_visit -> use AC[area] persistent contents -> ENCOUNTER
    n = level
    if special == TOMB        -> n += 1
    if special == GREAT_HALL  -> n += 2
    if level >= 4             -> n  = 4  (cap, then add Tomb/Hall bonuses)
    draw n cards from SP, classify each into hazards/treasure/strangers
    resolve hazards in priority order: EARTHQUAKE -> MEDUSA -> GHOULS
                                      -> MUTINY -> TRAP
        TRAP recurses: party falls to next level, draw new area below,
        re-enter that chamber's hazard pipeline
    if strangers   -> stranger-encounter
    else if treasure -> auto-pickup loop
    else            -> turn ends
```

Per-hazard handlers are individual `.ENTRY` routines: `DO_QUAKE`,
`DO_MEDUSA`, `DO_GHOULS`, `DO_MUTINY`, `DO_TRAP`. The Casio's
"unimplemented list" notes earthquake's missing map effect (item #1) —
we implement the full version: zero exit bits on `PP` and the matching
exit on `PA`.

### 8.4 Stranger encounter (STRANGER.MAR)

Leader determination uses the priority table from the unimplemented
list (item #12) — implemented correctly from day one rather than
"first found":

```
SPECTRE > DRAGON > WIZARD > HERO/W-HERO > PRIEST > MAN/WOMAN > GIANT
       > OGRE > TROLL > DWARF
```

(Sorcerer effectively above Spectre, Unicorn outside the list and
handled separately.)

Reaction test:

```
roll = ROLL_DIE()
if any party-member-flags has SCAVE$M_CHARISMA      -> roll++
if any party-treasure has THE_RING                  -> roll++
roll -= NC          (curses)
clamp [1..6]
if rolled-1-on-die  -> roll = 1     (no charisma override)
look up leader's reaction table
   <= hostile-max     -> HOSTILE  -> FIGHT (strangers have surprise)
   <= indifferent-max -> INDIFF   -> indifference++ (3 = perm-indiff)
   else               -> FRIENDLY -> all strangers join party + treasure
```

### 8.5 Fight (FIGHT.MAR)

V1 implements auto-pairing only (the Casio simplification). The
unimplemented full-pairing UI (item #17) is a stretch goal.

Auto-pairing:

1. Both sides drop heavy treasure (the Casio's unimplemented item #16)
   into the area's `AC` slots.
2. Sort party fighters by total strength descending; sort strangers
   the same way.
3. Match strongest-vs-strongest. If outnumbered, send 1 vs 2 — second
   slot of the 1's match holds a "ghost" entry pointing at the 2's index.
4. Priests/Wizards in our party can be sent to the background (UI
   choice before the round starts) where their magical power adds to
   one front-line match.
5. Compute strengths with all bonuses:
   surprise (round-1 only), Ring (+1 to all rolls), curses (-1),
   Magic Sword (+2 hero, +1 man/woman), Magic Staff (+1 priest, +2
   wizard), Strength Potion (+2 to selected hero/man/woman for the
   whole fight).
6. Roll dice; resolve each match; remove casualties; check victory
   /defeat; offer F/R.

Spectre rule: if a Spectre is in the strangers and our party has no
magical power and no Magic Sword bearer, the strongest party
front-liner is auto-slain that round (rules p.490).

Dragon-slayer: 1-on-1 win against a Dragon increments
`PARTY_PK[slot]`; that slot's strength gets +PK[slot] thereafter.
This is the Casio's unimplemented item #11 — trivial to add at
strength-calc time.

### 8.6 Special areas (SPECIAL.MAR)

**Viper Pit** (per `requirement-5-6-phases-and-ui.md` §4.1):

- Arrival = land in the entry doorway, turn ends.
- Subsequent turn: choose target exit. Casio uses "segments" — same
  here. Adjacent exits = 1 segment, opposite = 2.
- Per segment, per creature: roll die. 1 = falls in, lost; treasure
  goes to pit-treasure list (recoverable only with Charmed Flute).
  2-6 = safe.
- If party has Charmed Flute: skip rolls; flute-bearer can also pull
  pit-treasure out at the end.

**Deep Pool** (§4.2):

- Arrival turn: stop at edge.
- Crossing turn: non-Giant creatures drop heavy treasure at the entry
  doorway (added to `AC[entry_area]`). Giants carry one load each.
  Multi-load Giants take additional turns.

### 8.7 Artifacts (ARTIFACT.MAR)

One handler per artifact. Several pieces are still unimplemented in
the Casio code; we close the gap from day one:

| Artifact         | Handler                                                          |
|------------------|------------------------------------------------------------------|
| Magic Sword      | passive: bonus picked up in FIGHT.MAR strength calc              |
| Magic Carpet     | active: pick direction, teleport (cannot exit cave); single use  |
| Lotus Dust       | active: pick stranger; sleep flag for 2 rounds; single use       |
| Healing Balm     | active: revive last-killed creature; needs Woman/Priest/Wizard   |
| Talisman         | passive: skip Ghouls hazard; on level 4+ also wards off Spectres |
| Strength Potion  | active: pick hero/man/woman; +2 strength for current fight       |
| Magic Staff      | passive: bonus in strength calc; active: re-animate stoned        |
| The Ring         | passive: +1 to all rolls; on level 4+ bearer is invincible       |
| The Lost Ruby    | passive: triggers statue fight when picked up                    |
| Charmed Flute    | passive: viper-pit safety, also opens secret doors when active   |
| Eye of God       | passive: destroys Spectres in same area; curse if dropped        |
| Treasure Chest   | active: open via die roll → curse/spectre/silver/gold/gems       |

Implementation order matches the Casio's "suggested order" list (easy
wins first). If an artifact is already in inventory when its passive
trigger fires, the artifact module exposes a query
`PARTY_HAS_ARTIFACT(treasure-index)` that other modules call.

### 8.8 SCORE.MAR

```
score = 0
for slot in party:
    if PS == 0 or PS == 1 (alive or ally):
        s = creature_points[PC[slot]]
        if PK[slot] > 0: s *= 2     ; dragon-slayer
        score += s
        for treasure-slot in PT[slot]:
            score += treasure_points[item]
discard single-use items (carpet/dust/potion/balm) from sum already
if SK == 1: score += 30
score -= 30 * NC
score = max(0, score)
```

Display: full-screen "ESCAPED THE CAVE" or "PERISHED" art with the
breakdown, then `[EXE] continue / play again`.

---

## 9. Implementation stages

Each stage produces a runnable image (`SCAVE.EXE`) that we can
demonstrate. Stages are deliberately incremental and overlap with the
Casio's six-stage plan.

### Stage 0 — Skeleton & build

- Create `STATE.MAR` (just `SCAVE_STATE_GS`) and `MAIN.MAR` (entry
  point that paints a blank pasteboard, waits for `q`).
- Wire up `make vms-scave-build` / `vms-scave-run`. Confirm
  multi-file LINK works.
- ~1 hour. Deliverable: an SMG$ image that boots and exits.

### Stage 1 — Setup

- `SETUP.MAR`: title splash, party-selection UI, deck shuffle, gateway
  placement.
- `RNG.MAR` complete (LCG + shuffle).
- `DATA.MAR` complete for area cards, creatures, treasures, hazards.
- `UI.MAR`: pasteboard + 5 virtual displays + log + prompt.
- `STATE.MAR`: full state map.
- Deliverable: choose a party, see the Gateway, exit cleanly.

### Stage 2 — Movement & exploration

- `MAP.MAR`: full move/draw/dead-end logic.
- `CHAMBER.MAR`: chamber detection (stub hazard/treasure for now).
- Stair handling, level transitions.
- Map panel rendering for tunnels and chambers.
- Deliverable: walk around the cave; chambers detected but no contents.

### Stage 3 — Chambers, hazards, strangers

- `CHAMBER.MAR`: full small-card draw + classification.
- Hazard handlers (all 5).
- `STRANGER.MAR`: leader priority, reaction test, withdraw branch.
- Treasure pickup (auto-distribute by carry capacity, with manual
  redistribute via `[I]`).
- Deliverable: explore + collect + dodge hazards + meet (and walk away
  from) strangers.

### Stage 4 — Combat

- `FIGHT.MAR`: auto-pairing rounds, retreat, surprise, dragon-slayer,
  Spectre rule.
- Combat panel rendering.
- Deliverable: a full game loop minus special areas and artifacts.

### Stage 5 — Special areas & artifacts

- `SPECIAL.MAR`: Viper Pit, Deep Pool.
- `ARTIFACT.MAR`: all 12 artifacts. Easy wins first — Dragon-slayer,
  Talisman, Mutineers-join-strangers, Earthquake-seal, Leader-priority
  fixes. Then medium: Strength Potion, Heavy treasure drop, Magic
  Staff, Ring, Dwarf-past-traps. Then complex: Healing Balm, Spectre-
  from-Chest, Lost Ruby. Finally hard: Lotus Dust, Magic Carpet,
  Secret doors.
- Deliverable: feature-complete v1.

### Stage 6 — Scoring & polish

- `SCORE.MAR`: full scoring breakdown screen.
- Help screen text.
- Final pass: log-panel narration, bug fixes, listing-clean.
- Deliverable: shippable v1.

Estimate: each stage is one focused session. Stage 4 (combat) is the
biggest by code volume; stage 5 the biggest by feature spread.

---

## 10. Build & test workflow

Reuse the existing toolchain unchanged:

| Command                                     | Effect                                         |
|---------------------------------------------|------------------------------------------------|
| `make vms-scave-build`                      | Push all `.MAR`, MACRO each, LINK to SCAVE.EXE |
| `make vms-scave-run`                        | Build then `RUN/NODEBUG SCAVE`                 |
| `make vms-scave-debug`                      | Build then `RUN/DEBUG SCAVE`                   |
| `tools/vmsdrive/vmsdrive.py dbg '...'`      | Send DBG commands during a debug session       |

Caveat from LIFE: `vmsdrive` is line-oriented and cannot capture raw
ANSI output. To exercise SMG$ screens, telnet from a real terminal:

```sh
telnet -4 orac
$ RUN SCAVE
```

For debugger-driven verification (state inspection without needing a
visible terminal), use `vms-scave-debug` and walk the state arrays
just like we did with LIFE's `GRID0`/`GRID1`.

---

## 11. Risks and open questions

1. **MTH$ vs hand-rolled RNG** — `MTH$RANDOM` requires F-floating
   handling in MACRO (the LIB$WAIT pattern from LIFE). The LCG is
   simpler. Going with LCG; revisit if the distribution feels off.

2. **PSECT alignment** — confirmed `.ALIGN LONG` is the safe maximum.
   Don't attempt `.ALIGN QUAD` unless we change the PSECT declaration
   (`%MACRO-E-ALIGNXCEED`).

3. **Branch ranges** — `CHAMBER.MAR` and `FIGHT.MAR` are the longest
   modules. We will hit `BRDESTRANG` errors and need invert+`BRW`
   the same way LIFE did. Not a design risk, but a watch-item.

4. **Interactive testing** — the `vmsdrive` line-buffered constraint
   means we cannot capture ANSI output for automated regression
   tests. Stage testing therefore relies on:
   - Debugger state inspection for non-visual logic (deck contents,
     party state, scoring math).
   - Manual telnet sessions for visual verification at each stage.

5. **Multi-file LINK on the VAX** — first time we do this in this
   repo. We need to confirm the LINK syntax: `LINK MAIN, SETUP, MAP,
   CHAMBER, ...` should work with each `.OBJ` resolving the
   `.EXTRN`s in others. If there are quirks (e.g., needing
   `/EXEC=SCAVE`, or option-file syntax for many files), capture them
   in a project memory.

6. **High score persistence** — RMS file or skip. Skipping for v1.

7. **Save game** — out of scope for v1. The Casio version doesn't
   have one either.

8. **Solitaire indifference rule** — three rolls of indifference and
   the strangers stay forever indifferent. This is per the rules; the
   Casio docs flag this as a solitaire-specific decision and we
   inherit it.

---

## 12. References used

- `reference/sorcerors-cave/sorcerers-cave-rules.md` — canonical rules
- `reference/sorcerors-cave/casio-vx4-implementation/SORCERER.BAS` — Casio source
- `reference/sorcerors-cave/casio-vx4-implementation/SORCERER.md` — Casio overview + line-number map
- `reference/sorcerors-cave/casio-vx4-implementation/requirement-1-rules-analysis.md` — gaps/ambiguities/scope
- `reference/sorcerors-cave/casio-vx4-implementation/requirement-2-high-level-architecture.md` — phases
- `reference/sorcerors-cave/casio-vx4-implementation/requirement-3-4-data-structures.md` — encodings
- `reference/sorcerors-cave/casio-vx4-implementation/requirement-5-6-phases-and-ui.md` — flowcharts + UI
- `reference/sorcerors-cave/casio-vx4-implementation/area-card-encoding.md` — exact 61-card numeric values
- `reference/sorcerors-cave/casio-vx4-implementation/area-ascii-mockups.md` — area visualization vocabulary
- `reference/sorcerors-cave/casio-vx4-implementation/2026-04-03-not-implemented.md` — gaps to close in this port
- `src/macro32/life/LIFE.mar` — calling-standard / SMG$ / system-service macro reference
- `src/macro32/smg/SMGHELLO.mar` — minimal SMG$ template
- This repo's `CLAUDE.md`, `reference/INDEX.md`, and `reference/VAX-VMS-731/` — the SMG$ + RTL + system-service docs we'll grep at impl time

---

## 13. Next step

Stage 0 — create the `MAIN.MAR` skeleton + Makefile target + minimal
state, prove multi-file build works, then proceed to Stage 1.
