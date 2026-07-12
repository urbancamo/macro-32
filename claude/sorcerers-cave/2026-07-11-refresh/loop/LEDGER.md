# SCAVE Refresh — Work Ledger

> The loop's memory. Read first, update last, every iteration
> (see [../loop-spec.md](../loop-spec.md) §5). Keep entries terse but evidenced.

**Status:** `ACTIVE`  (values: ACTIVE | DONE | NEEDS-HUMAN)
**Current gate:** G3
**Last iteration:** I004 (2026-07-12) — G2 exit test PASS: all 8 SETUP lines match the reference

## Gates

| Gate | State | Evidence (command + date) |
|---|---|---|
| G0 Harness | PASS | `make vms-scave-build` links SCAVE.EXE + SCCONF.EXE clean (0 warnings); `make vms-scave-conform VEC=solo-seed23-party4-6` runs end-to-end, emits well-formed `SETUP` line, diff pinpoints first divergence at the SETUP SEED (2026-07-12, I001) |
| G1 RNG + data | PASS | `make vms-scave-selfcheck` (I003): `NEXTSEED1 1103527590`, `DECK LARGE 60 SMALL 71`, `TYPES 14/15/5`, `PACK 37/27/7 = 71`, cells Hero 3/3 Priest 1/4 Man 2/4 Woman 2/4 Dwarf 0/4 Dragon 4/6 — all match A.1 (2026-07-12) |
| G2 Setup | PASS (exit) | All 8 vectors' SETUP lines match the reference (I004 per-vector diff, 2026-07-12): shuffle + consumption order (large60→small71→store) correct. **D2/S1 deferred** — see backlog note (not SETUP-visible; D2 verified at G4 draws, S1 not exercised by valid vectors) |
| G3 Movement | PENDING | — |
| G4 Chambers/encounters | PENDING | — |
| G5 Fights | PENDING | — |
| G6 Specials/artifacts/scoring | PENDING | — |
| G7 Part I audit | PENDING | — |
| G8 UI rewire | PENDING | — |
| G9 UI playability | PENDING | — |

## Vector status

Re-run `make vms-scave-conform-all` after any engine change; record the first divergent line
(or PASS). As of **I004 all 8 SETUP lines match the reference** (per-vector `grep SETUP` diff).
`ENG_APPLY` is still a stub, so every vector's FIRST divergence is now at **move 1** (no
move/turn/event applied). G3 (movement) starts closing these. `conform-all` still stops at the
first vector because every vector fails at move 1 until the reducer is built.

| Vector | Moves | Status | First divergence |
|---|---|---|---|
| solo-seed23-party4-6 | 7 | SETUP✓ | move 1 (ENG_APPLY stub) |
| solo-seed777-party5-6 | 7 | SETUP✓ | move 1 (ENG_APPLY stub) |
| solo-seed101-party1-7 | 8 | SETUP✓ | move 1 (ENG_APPLY stub) |
| solo-seed11-party5-6-7 | 15 | SETUP✓ | move 1 (ENG_APPLY stub) |
| solo-seed19-party2-7 | 18 | SETUP✓ | move 1 (ENG_APPLY stub) |
| solo-seed7-party1-7 | 19 | SETUP✓ | move 1 (ENG_APPLY stub) |
| solo-seed42-party3 | 31 | SETUP✓ | move 1 (ENG_APPLY stub) |
| solo-seed3-party0 | 61 | SETUP✓ | move 1 (ENG_APPLY stub) |

## Backlog

D-numbers refer to [../gap-analysis.md](../gap-analysis.md) §3. Work strictly by gate order.
States: TODO | IN-PROGRESS | DONE | BLOCKED(n strikes) | NA.

### G0 — Harness  (DONE, I001)
- [x] H1 Engine boundary skeleton: `ENGINE.MAR` with `ENG_NEWGAME` (real deck/map/party seat)
      + `ENG_APPLY` stub, event queue in `STATE.MAR` (`SCAVE_EVQ_N`/`SCAVE_EVQ`, cap 32),
      `SCAVE_STATE_PH` phase (SC-4-3). Action codes 1..17 redeclared file-local per module.
- [x] H2 `SCCONF.MAR`: RMS `CONFVEC.TXT` reader + action-grammar parser + `FAO`-formatted
      checkpoint writer (`CONFRES.TXT`), exact vector format. `ENG_APPLY` stub → post-SETUP
      lines repeat newGame state with `EV -` (the honest baseline the gates burn down).
- [x] H3 `MAKE.COM`/`sources.list`: second link target `SCCONF.EXE`
      (SCCONF,ENGINE,SETUP,UI,RNG,DATA,STATE). Added a headless `HELP_BROWSER` stub in
      `SCCONF.MAR` so the SETUP.OBJ→HELP_BROWSER ref resolves without dragging in SMG$
      (SCCONF never enters interactive setup). *Follow-up (later gate):* migrate the pure
      `INIT_DECKS`/`INIT_MAP` out of `SETUP.MAR` into the engine layer, then SCCONF can drop
      `SETUP.OBJ` and the stub.
- [x] H4 Makefile: `vms-scave-conform` / `vms-scave-conform-all` (push vector → run SCCONF →
      fetch `CONFRES.TXT` → diff → first divergent line). Both gained a `vmsdrive ping`
      emulator preflight + a hard 300s command cap so a wedged VAX can't stall the loop.

### G1 — RNG + static data
- [x] D1 71-card small pack (I003): template rewritten to 37/27/7 = 71; grew `SCAVE_DECK_SP`
      (`SCAVE$_SMALL_COUNT` 52→71); `INIT_DECKS` copy/shuffle + `CHAMBER` draw bound now read
      `SCAVE_DATA_SMALL_N`. Self-check: `PACK CREAT 37 TREAS 27 HAZ 7 TOTAL 71`.
- [x] D3 Area card index 41: 74 → 42 (I003, SC-3-3). Verified visually; vectors exercise it in G3.
- [x] D4 Reaction cells (I003): HOSTILE/INDIFF rewritten. Self-check: Hero 3/3, Priest 1/4,
      Man 2/4, Woman 2/4, Dwarf 0/4, Dragon 4/6 — all match A.1.
- [ ] D5 Seed injection: `ENG_NEWGAME` takes the seed (DONE in ENGINE.MAR); SCAVE reads
      `SCAVE_SEED` logical, falls back to `$GETTIM` — SC-5-13 (UI side, verify under scenarios).
- [x] H5 SCCONF self-check mode (`SELFCHECK` line → `make vms-scave-selfcheck`): prints
      `NEXTSEED1`, deck sizes, TYPES, PACK composition, A.1 CELLs. **RNG core verified correct:**
      `NEXTSEED1 1103527590` (SC-5-6). RNG.MAR needs no change (mask `BICL2 #^X80000000`, bits via
      `EXTZV #15,#16`, `min(5,·)+1` clamp all match A.5).
- [x] H6 `RAND_BELOW` n<=0 no-advance verified: `RB0 BEFORE 12345 AFTER 12345 VAL 0` (SC-5-8).

### G2 — Setup  (exit test PASS, I004)
- [x] D6 RNG consumption order: large pack → small pack → store cursor — SC-5-12. Verified: all 8
      SETUP lines match (INIT_DECKS shuffles LP then SP then stores; already correct).
- [ ] D2 Party drawn FROM the shuffled small pack (each pick's 100+id removed once) — SC-5-5.
      **Deferred to G4**: not SETUP-visible (removal is post-shuffle, consumes no RNG), and its
      effect (picked card can't appear as a stranger) is only exercised once the engine draws
      chambers (G4). Implement in `ENG_NEWGAME` (post-INIT_DECKS): scan `SCAVE_DECK_SP`, remove
      first `100+id` per pick, compact, track a live count `SCAVE_DECK_SN`; CHAMBER draw bound
      reads `SCAVE_DECK_SN`. Reference: setup.ts `smallPack.indexOf(100+id)`+splice.
- [ ] S1 newGame init: turn/level/score/phase/Gateway faceUp — SC-3-23/24 (DONE in ENG_NEWGAME);
      pick validation (empty, non-starter, budget≤6, stock) — SC-5-1..4. **Deferred**: all vectors
      use valid picks, so validation isn't vector-verified; add as a guard (validatePicks:
      len>0, id∈0..7 selectable, Σ SEL[id]≤6, count[id]≤START_COUNT[id]).

### G3 — Movement
- [ ] D7 Any printed level-1 stair-up is a cave exit; DIR_UP still blocked on L1 — SC-6.1-12
- [ ] D8 Secret doors: mirrored stairs (fresh draws AND already-placed areas), numbered — SC-6.1-13/14/15/17
- [ ] D9 Quake rubble impassable + withdraw-blocked-onto-destroyed — SC-6.1-5, SC-7.2-12
- [ ] D10 Large-pack exhaustion: `moved:false`, not a dead end — SC-6.1-6
- [ ] D11 Turn coupling: +1 only on success, clears fellThroughTrap; failed move no turn — SC-4-9
- [ ] M1 Movement event order: moved/deadEnd/blocked exactly as SC-6.1-18 emits them

### G4 — Chambers, hazards, encounters
- [ ] D13 Ghouls rewrite: heavy-drop first, Talisman ward, Ring immunity, carried-spill — SC-7.2-5/6/7
- [ ] D14 Medusa carried-spill (+ borne stays with body) — SC-7.2-3/13
- [ ] D15 Trap: any living Dwarf avoids (no one-trap memory); trap-fall chains — SC-7.2-9, SC-4-14
- [ ] D16 Mutiny splice order + all-ally loyal-first verify — SC-7.2-8
- [ ] D17 Lurking Medusa/Ghouls re-park; quake scar to display-only markers — SC-7.2-10
- [ ] D18 Natural-1 = effective roll 1 (NOT forced hostile) — SC-8.3-5
- [ ] D19 Withdraw blocked after trap fall / destroyed prev — SC-4-17
- [ ] D20 Surprise: fresh-entry only, test forfeits, hostile −1 paths — SC-4-16/21/22, SC-7.1-11
- [ ] D21 Retreated-from areas hostile-on-sight — SC-4-28
- [ ] D22 Pacified areas: free traversal + explicit Attack un-parks guards — SC-10.4-3/4
- [ ] D23 Unicorn: joins only with Woman/W-Hero; womanless Unicorn guards+pacifies — SC-4-19, SC-10.4-5
- [ ] D24 Passage-tile floor pickup on return — SC-7.3-12
- [ ] D25 Remove 20-slot treasure cap; identical array insert/remove order to engine
- [ ] D26 Remove 12-member party cap — SC-3-21
- [ ] P1 Pickup actions complete: take/leave/move/drop/retakeDropped semantics + Eye curse on
      drop/transfer — SC-4-29..33, SC-7.3-*

### G5 — Fights (battle-plan rewrite)
- [ ] D27 resolveRound(plan) + full validation set (rejection reasons; no state change on
      reject) — SC-9.1-1..9
- [ ] D28 Gang-up §395 + enemy-caster fold-in — SC-9.1-10/11
- [ ] D29 Casualty queue + chooseCasualty die (4-6 honours pick) — SC-9.5-4/5, SC-4-26
- [ ] D30 Heavy-treasure drop at round resolution + win-reclaim + retakeDropped — SC-9.5-1/2
- [ ] D31 Retreat: round>1 only, any exit, dead-end sets retreatBlocked — SC-9.5-6/7, SC-4-27
- [ ] D32 Caster hand-to-hand at TOTAL strength; vs Spectre MP-only / sword-bearer FS — SC-9.3-1, SC-9.4-2
- [ ] D33 Spectre nuances: no gang-attach, forced-empty plan, sole-caster leftover, Ring block — SC-9.4-3..6
- [ ] D34 Dragon-slayer credit single-handed only — SC-9.4-7
- [ ] D35 sweepFallen loot model (win→floor, wipe→tile, borne lost, retreat leaves all,
      viper loses all) — SC-9.5-8/11
- [ ] D36 Sorcerer: Eye −2 / Lotus −2 / floor 0; kill lifts curses — SC-9.4-8
- [ ] D37 Surprise ±1 round-1 die totals verify — SC-9.2-1

### G6 — Specials, artifacts, scoring
- [ ] D38 Viper Pit: fatal 1 OR 2; flute-eligible lull; loot into pit — SC-10.1-*
- [ ] D39 Deep Pool: single dropped list; crossing-on-exit (retrace safe); Giant-only
      weight-limited reclaim pickup — SC-10.2-*
- [ ] D40 Special entry-stops-at-edge timing — SC-10-3/4
- [ ] D41 `useArtifact` + `openChest` + `setBorne` actions — SC-4-34/35, SC-7.3-13/14 (D53)
- [ ] D42 Healing Balm — SC-11-14/15
- [ ] D43 Lotus Dust (+ sleeping 400+id parking) — SC-11-9..13
- [ ] D44 Magic Carpet (incl. deliberate SC-4-40 non-rule) — SC-11-4..7
- [ ] D45 Talisman — SC-11-16/17
- [ ] D46 Strength Potion activation — SC-11-18/19
- [ ] D47 Staff reanimation (active + passive on entry) — SC-11-21/22, SC-4-44
- [ ] D48 Ring L≥4 invincibility everywhere it applies — SC-11-25
- [ ] D49 Lost Ruby statue wrestle — SC-7.3-9, SC-11-26..28
- [ ] D50 Charmed Flute: dragon lull + secret-door reveal — SC-11-29..33
- [ ] D51 Eye of God (nullify/annihilate/still/curse paths) — SC-11-34..39
- [ ] D52 Treasure Chest open table + bonusScore — SC-11-40/41
- [ ] D54 Flat −30 curse penalty; Sorcerer kill lifts it — SC-12-9/10
- [ ] D55 bonusScore in the total — SC-12-8
- [ ] D56 Score breakdown itemisation — SC-12-15

### G7 — Part I audit
- [ ] A1 Build the per-SC-row checklist (solo rows only) and walk it with file:line evidence
- [ ] A2 Strip remaining legacy behaviour (Dwarf one-trap memory, pool doorway drops, party
      cap remnants, "always friendly humans" traces)

### G8 — UI rewire
- [ ] U1 MAIN/UI/VIEW consume events + legal-action data only; no rules in UI modules
- [ ] U2 New UI surfaces: battle-plan builder, casualty prompt, artifact menu (A), inventory +
      borne toggle (I), chest, retake-dropped, per-member score breakdown
- [ ] U3 Vectors re-pass after rewire; scripted seeded full game playable

### G9 — UI playability
- [ ] Scenario scripts S1–S9 written (key sequences + expects + seeds recorded here)
- [ ] All scenarios pass the §7 rubric; renders archived under `loop/screens/`
- [ ] Full-game agent playthrough clean

## Open defects

(id | gate | symptom | evidence | hypotheses tried | state)

— none yet —

## UI findings

(id | scenario/screen file | rubric # | description | state)

— none yet —

## Reference discrepancies

Suspected reference-engine bugs — log here, never diverge silently, never edit vectors.

— none yet —

## Requests for the reference side

e.g. extra targeted vectors (deep levels, Sorcerer kill, escape-with-loot). Non-blocking.

— none yet —

## Iteration log

(newest first: `I### | date | gate | item | change | evidence | result`)

- **I004 | 2026-07-12 | G2 | SETUP exit test** — Verified all 8 vectors' SETUP lines against the
  reference (per-vector run + `grep SETUP` on the diff). *Evidence:* solo-seed23/777/101/11/19/7/42/3
  all "SETUP OK". *Result:* G2 exit test PASS (shuffle + consumption order correct). D2/S1 deferred
  (not SETUP-visible / not vector-exercised) — see G2 backlog. Next: G3 movement (clears move 1).
- **I003 | 2026-07-12 | G1 | D1/D3/D4 static data** — Small pack 52→71 (DATA.MAR template +
  `SCAVE$_SMALL_COUNT`=71 + `INIT_DECKS`/`CHAMBER` counts via `SCAVE_DATA_SMALL_N`); area card 41
  74→42; reaction cells corrected. *Evidence:* self-check `SMALL 71`, `PACK 37/27/7`, cells
  Hero 3/3…Dragon 4/6; build clean; `conform VEC=solo-seed23` no longer crashes and its **SETUP
  line now MATCHES the reference** (SEED 446078340) — first divergence moved to move 1 (ENG_APPLY
  stub). *Result:* G1 PASS. Bonus: D6 consumption order was already correct (INIT_DECKS shuffles
  large→small→store); the pack size was the only thing keeping the SETUP seed off. Head-start on G2.
- **I002 | 2026-07-12 | G1 | H5/H6 self-check harness** — Added a `SELFCHECK` diagnostic mode to
  SCCONF (`DO_SELFCHECK`), a `SCAVE_DATA_SMALL_N` length symbol in DATA.MAR, and a
  `make vms-scave-selfcheck` target. *Evidence:* `NEXTSEED1 1103527590`, `RB0 ... AFTER 12345 VAL 0`,
  `DECK LARGE 60 SMALL 52`, `PACK CREAT 19 TREAS 27 HAZ 6 TOTAL 52`, cells Hero 0/0 … Dragon 6/6.
  *Result:* RNG core proven correct (no RNG.MAR change needed); D1/D4 baselines captured. H5/H6 done.

- **I001 | 2026-07-12 | G0 | H1–H4 harness green** — Found the G0 harness already built in the
  tree (ENGINE.MAR/SCCONF.MAR/STATE event queue/MAKE.COM/sources.list/Makefile conform targets)
  but unbuilt/unrecorded. Built it: SCAVE.EXE linked clean; SCCONF.EXE had one NUDFSYM
  (`HELP_BROWSER`, pulled in via SETUP.OBJ). Fixed with a headless stub in SCCONF.MAR.
  *Evidence:* `make vms-scave-build` → `LINK SCAVE`/`LINK SCCONF`/`DONE`, zero warnings;
  `make vms-scave-conform VEC=solo-seed23-party4-6` → well-formed `SETUP` line, first divergence
  at SETUP SEED (exp 446078340, got 1559363521). *Result:* G0 PASS; advance to G1.
  Also hardened the emulator harness against stalls (300s cap + `vmsdrive ping` preflight).
