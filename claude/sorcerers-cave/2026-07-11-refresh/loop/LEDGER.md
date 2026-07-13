# SCAVE Refresh — Work Ledger

> The loop's memory. Read first, update last, every iteration
> (see [../loop-spec.md](../loop-spec.md) §5). Keep entries terse but evidenced.

**Status:** `ACTIVE`  (values: ACTIVE | DONE | NEEDS-HUMAN | BLOCKED-INFRA)
**Latest (I024, 2026-07-13):** VAX back; the §9 multi-front fight model BUILT + VERIFIED.
**solo-seed174 (sorcerer) PASSES end-to-end; base-8 all still PASS = 9/9 vectors green.** The
offline branch-hardening paid off -- only 2 more BRDESTRANGs surfaced at build (SCCONF `BNEQ DM_APPLY`
now far past the grown plan parser; SWEEP_FALLEN `BGEQ SF_DONE`), both fixed by invert+BRW. Next gap
vector: **seed225 (escape)** -> §7 RNG hazards (study notes below) + trap-fall relocation.

**(resolved) prior BLOCKER (2026-07-13):** the VAX host `orac` was unreachable -- 100% ICMP loss + TCP timeout to
orac:23 (host down/off-net, user away from home). `make vms-down/up` + retry did not help. Cannot
build or verify until the VAX is back. **The §9 multi-front fight code is written but
UNBUILT/UNVERIFIED, UNCOMMITTED in the working tree** (ENGINE.MAR / SCCONF.MAR / STATE.MAR). Last
verified-green commit is `2ac0f08` (base-8 + seed174 8->55).

**Offline hardening done while blocked (2026-07-13, still uncommitted):** desk-checked the whole §9
diff against the reference + the vax-macro-32 branch-range rule. Fixed **1 assembly-breaking bug** --
a dangling `BRB GU_F1` left after GANG_UP's fold-loop was replaced by an `IS_ENGAGED` call (undefined
symbol) -- and hardened **4 out-of-range conditional branches** to invert+`BRW` (FIGHT_ROUND
win/lose/tie dispatch `BLSS FR_LOSE` spanned the ~46-instr FR_WIN block; `FR_LOSE` FN==0 guard;
EA_CASUALTY's three `EC_BLOCK` guards; SCCONF FIGHT-parser `BEQL FM_DONE`/`BLEQ FM_CLOSE`). Added
`SWEEP_FALLEN` (spills a fallen member's carried treasure into the pickup, emits `itemsSpilled`
before `fightWon`) so seed174 step 57 (`...,itemsSpilled,fightWon`) matches. A label-reference sweep
of ENGINE.MAR is now clean. **Deferred/noted (unexercised by seed174, handle if a vector needs
them):** §387 in-fight heavy-drop + win-reclaim; the wiped-path sweepFallen onto the tile;
reconcileUnicorns (unicornDeparted); the Spectre-match `memberStr = casterMP` special case; the
fold-focus assumption (always match 0 vs. "first non-Spectre match").

**When the VAX returns:** `make vms-scave-build` (should assemble much closer to clean now); run
`make vms-scave-conform VEC=solo-seed174-party1-7-sorcerer` (expect past step 57 -- watch for §387
heavy-drop divergences in the FINAL CARRY/CONT block); confirm base-8 stays 8/8; then commit.

**Current gate:** G7→engine-completion. **UNBLOCKED:** the reference side already minted 6 extra vectors (seed174 sorcerer, seed225 escape, seed257/1237/2355/2678 artifacts) that collectively exercise EVERY gap subsystem (TEST/reaction, all 8 artifacts, RNG hazards, multi-front fights, chest, unicorn, Eye). Finishing the engine port is now a **verifiable vector grind** against them. **Done so far:** §8 TEST/reaction ported (I023) -> seed174 8->55, base-8 still 8/8. **Next:** §9 multi-front fight model (seed174 step 55 `FIGHT 4+0>0`). Then §7 RNG hazards, §11 artifacts, §12 chest/scoring.

**§9 study notes (reference combatPlan.ts resolvePlannedRound + previewPlan):**
- Plan is a list of matches; each match = front-list + backer-list + stranger-list. Current engine
  STATE has 1D FA/FD (one front, one stranger per match) -- needs a **2D restructure**: FN[i]/BN[i]/SN[i]
  counts + flattened FA/FB/FD[i*MPM+j] (MPM ~= PARTY_MAX). SCCONF plan parser must handle
  `<front>[+<front>][|<backer>[+..]]><stranger>[+<stranger>]` (currently only 1v1 `<f>><s>`).
- Per match: `partyStr = Σ frontStrength(front) + Σ casterMP(backers)`; `enemyStr = Σ (fs+MP)(strangers)
  + Σ MP(foldedCasters)`. frontStrength = fs + dragonKills + casterMP (+Sword/Potion when artifacts land).
  rollBonus = (Ring?1:0) - activeCurses; surprise ±1 round 1. Two dice/match (party then enemy).
- Win: kill the STRONGEST foe in the match (by fs+MP); single-handed lone-Dragon match -> dragonKills++;
  Sorcerer killed -> sorcererKilled=1 + sorcererSlain. Lose: mortal front (excl. Ring) -> 0 deathPrevented
  / 1 memberDied / >1 **casualtyQueue** (pause; CASUALTY(14): d6>=4 honors the pick, else the other falls;
  emit casualtyChosen+memberDied; empty queue -> finalizeRound).
- previewPlan also does the gang-up attach (leftover extra-hand foes onto 1v1 matches) + leftover-caster
  fold onto the focus match (my current GANG_UP precomputes these into ATTACH/FOLD -- keep, but re-fit to
  the 2D structure). Idle-Spectre auto-slay stays (SPECTRE_CHECK). finalizeRound: Unicorn depart, no
  survivor -> sweepFallen + gameOver(DEAD); strangers cleared -> fightWon + reclaim floor drops +
  sweepFallen into pickup; else keep fighting. This is the single biggest remaining piece.
**Last iteration:** I022 (2026-07-12) — G7 Part I audit (10-agent workflow, 317 SC-rows mapped with file:line evidence → [G7-AUDIT.md](G7-AUDIT.md)). **Key finding:** `ENGINE.MAR` implements only the rules the 8 vectors exercise; **164 gap-rows** (TEST/reaction, all 8 artifacts, Eye of God, openChest, moveTreasure/drop/setBorne, multi-front fights, RNG hazards Medusa/Ghouls/Mutiny/Trap) live only in the **legacy interactive modules** (STRANGER/ARTIFACT/FIGHT/SPECIAL), several with their own defects, none vector-covered. True G8 ("no game fact in UI") requires porting these into the engine — most need **new conformance vectors** to verify (see "New vectors requested" below).

## Gates

| Gate | State | Evidence (command + date) |
|---|---|---|
| G0 Harness | PASS | `make vms-scave-build` links SCAVE.EXE + SCCONF.EXE clean (0 warnings); `make vms-scave-conform VEC=solo-seed23-party4-6` runs end-to-end, emits well-formed `SETUP` line, diff pinpoints first divergence at the SETUP SEED (2026-07-12, I001) |
| G1 RNG + data | PASS | `make vms-scave-selfcheck` (I003): `NEXTSEED1 1103527590`, `DECK LARGE 60 SMALL 71`, `TYPES 14/15/5`, `PACK 37/27/7 = 71`, cells Hero 3/3 Priest 1/4 Man 2/4 Woman 2/4 Dwarf 0/4 Dragon 4/6 — all match A.1 (2026-07-12) |
| G2 Setup | PASS (exit) | All 8 vectors' SETUP lines match the reference (I004 per-vector diff, 2026-07-12): shuffle + consumption order (large60→small71→store) correct. **D2/S1 deferred** — see backlog note (not SETUP-visible; D2 verified at G4 draws, S1 not exercised by valid vectors) |
| G3 Movement | PASS (movement) | I005-I007: all 8 vectors match every MOVE up to their first non-move action — MOVE (success/deadEnd/blocked), turn coupling, chamber-draw-on-arrival, special entry (enteredSpecial), event order. solo-seed11 reaches move 4 where the special **crossing** (crossedSpecial) begins = G6. D8/D9 (secret doors, quake rubble) not exercised in the pre-first-non-move moves — verify when a vector hits them |
| G4 Chambers/encounters | PENDING | — |
| G5 Fights | PENDING | — |
| G6 Specials/artifacts/scoring | PASS | I008-I021: focus-fire fights + caster magic, gang-up (D28), Spectre auto-slay, Lost-Ruby statue wrestle (D49), secret doors (D8), on-draw Earthquake hazard (SC-7.2), and the special crossings — Viper Pit (SC-10.1, d6/member, fatal on 1-2, game-over on wipe) and Deep Pool (SC-10.2, Giant carries / heavy loot dropped). **All 8/8 vectors PASS bit-for-bit** (2026-07-12). Deferred (unexercised by valid vectors): flute-lull, Eye-of-God forfeit, RNG hazards (Medusa/Ghouls/Mutiny/Trap), pool treasureReclaimed, DROP-list emit |
| G7 Part I audit | AUDIT DONE / gaps open | I022: all 317 solo SC-rows mapped to the port with file:line evidence → [G7-AUDIT.md](G7-AUDIT.md). Tally: **136 conformant, 164 gap, 9 ui-pending, 7 discrepancy, 1 na-mp**. §3 100% conformant; §5/§6/§12 core conformant with unexercised-rule gaps; §7-§11 the bulk of the gaps (engine is a vector-subset). 2 discrepancies (SC-6-5, SC-6.2-2 global-mutation vs structuredClone) accepted as deliberate MACRO-port architecture. Audit checklist delivered = G7 exit test met; the 164 gaps are now the G8 backlog |
| G8 UI rewire | BLOCKED (engine incomplete) | Cannot "route UI through the engine exclusively" until the engine implements the actions the UI offers (test, useArtifact×8, openChest, moveTreasure/drop/setBorne, retreat, full fight model). That is ~160 rows of engine work, mostly unverifiable without new vectors. Partial G8 (rewire the vector-covered explore/move/chamber/pickup/score path onto ENG_APPLY) IS doable now — see backlog |
| G9 UI playability | PENDING | — |

## Vector status

Re-run `make vms-scave-conform-all` after any engine change; record the first divergent line
(or PASS). As of **I004 all 8 SETUP lines match the reference** (per-vector `grep SETUP` diff).
`ENG_APPLY` is still a stub, so every vector's FIRST divergence is now at **move 1** (no
move/turn/event applied). G3 (movement) starts closing these. `conform-all` still stops at the
first vector because every vector fails at move 1 until the reducer is built.

| Vector | Moves | Status | First divergence |
|---|---|---|---|
| solo-seed23-party4-6 | 7 | **PASS** ✅ | fully conforms (I019 Lost-Ruby statue) |
| solo-seed777-party5-6 | 7 | **PASS** ✅ | fully conforms (I014) |
| solo-seed101-party1-7 | 8 | **PASS** ✅ | fully conforms (I014) |
| solo-seed11-party5-6-7 | 15 | **PASS** ✅ | fully conforms (I021 deep-pool crossing) |
| solo-seed19-party2-7 | 18 | **PASS** ✅ | fully conforms (I017 Spectre auto-slay) |
| solo-seed7-party1-7 | 19 | **PASS** ✅ | fully conforms (I018 gang-up) |
| solo-seed42-party3 | 31 | **PASS** ✅ | fully conforms (I020 Earthquake + I021 viper-pit crossing) |
| solo-seed3-party0 | 61 | **PASS** ✅ | fully conforms (I015 EXITCAVE/D7/FU + I016 scoring) |

## Study notes: §7 RNG hazards (prepared offline 2026-07-13, from reference hazards.ts applyHazards)

Next grind target after seed174 is **seed225 (escape)** which needs Trap + the trap-fall relocation,
plus reaction/unicornGuards/annihilated. `RESOLVE_HAZARDS` currently fires only Earthquake; add the
rest **in the fixed order Earthquake, Medusa, Ghouls, Mutiny, Trap** (HAZ_ORDER already correct):

- **Ward checks first (skip the effect, emit the ward event, NO hazardFired):** Ghouls + a living
  Talisman(id 10) holder -> `ghoulsWarded`; Medusa + a living Wizard(8) holding the Magic Staff(9)
  -> `medusaAverted`. (Both need artifact-holding checks -> may land with §11.)
- **Earthquake** (done): collapse prev (prev!=partyArea) AF_DESTROYED + clear contents. No RNG.
- **Medusa** (RNG: one d6 per living member): 1-2 -> stone (status 2, record stoneArea=partyArea),
  spillCarried -> push to treasures + `itemsSpilled`; collect all rolls -> emit `medusaGaze`.
- **Ghouls** (RNG: 2 dice per living member): first drop every member's heavy treasure to the floor
  (treasures[]); then each living member fights Ghouls (enemy strength 2, no surprise): partyTotal =
  frontStrength(m)+d6, enemyTotal = 2+d6, emit `combatRoll`; enemyTotal>partyTotal -> member dies
  (unless ringInvincible -> `deathPrevented`) + eyeForsakenByDeath. After all: `sweepFallen(working)`.
- **Mutiny** (no RNG): all allies (status 1) desert -- if there are 0 originals, all-but-one desert.
  Each deserter -> pushed back to strangers[] (retestable) + their treasure dropped to treasures[];
  remove from party; emit `mutinied` if any deserted.
- **Trap** (no RNG): a living Dwarf (FLAG_GUIDES_PAST_TRAP, id 7) -> `trapAvoided`; else set fell=true.
  `fell` -> the §6 trap-fall (SC-6-6, still a gap): park chamber behind, relocate party one level
  DOWN (one-way, fellThroughTrap=true), emit `trapSprung`+`moved`, re-enter resolution at the lower
  level SAME turn (may chain). This is a MOVE-handler change, not just RESOLVE_HAZARDS.
- **After firing:** Medusa & Ghouls RE-PARK into the area contents as `300+hz` so they reload and
  fire again on every re-entry; then clear the working hazard set. Earthquake lays a display-only scar.

Event order per hazard is: [ward OR hazardFired] then its effect events. hazardFired is NOT emitted
when a ward fires. Watch seed offsets: Medusa/Ghouls consume RNG, so a wrong petrify/fight count
diverges the SEED on that line. §11/§12 (artifacts/chest) study still pending -- do when reached.

## New vectors requested (for the human / reference side)

Per loop-spec §6, logging targeted vectors that would let the port of the §7-§11 gap rules be
verified bit-for-bit instead of only code-read against the reference. The reference side can mint
these cheaply; the loop must **never block** on them, but without them the engine-port of these
rules is unverifiable. Priority order:

1. **A TEST/reaction game** (§8): a solo seed+party that draws a chamber with strangers and issues
   `TEST` repeatedly — covers reaction roll, charisma +1, curses −1 (and the zero-on-Sorcerer-kill
   rule), natural-1, hostile→fight, 3×indifferent→pacified, friendly→recruit-all. This is the single
   biggest coverage hole (26 §8 gaps + the STRANGER.MAR defects).
2. **An artifact game** (§11): a seed that draws artifacts and issues `USE` — Potion, Lotus, Balm,
   Staff, Carpet, Flute, plus `OPENCHEST` outcomes and the Eye-of-God curse paths.
3. **An RNG-hazard game** (§7): a chamber drawing Medusa / Ghouls / Mutiny / Trap so their effects
   (petrify, ghoul fight, mutiny, trap-fall relocation) and Talisman/Staff wards are exercised.
4. **A multi-front / Sorcerer fight** (§9): several strangers vs a multi-member party with a
   `RETREAT` and a `CASUALTY` choice, and a Sorcerer kill (curses-lifted + sorcererSlain +30).
5. **An escape-with-loot ending** (§12): a party that reaches a level-1 stair-up carrying treasure,
   to exercise the full per-member scoring breakdown incl. bonusScore.

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

**Study notes (I004, from reference `map.ts`/`coords.ts`/`reduce.ts` + local `MAP.MAR`):**
- `MAP.MAR:TRY_MOVE(dir@4(AP))` is **already headless** (STATE globals only, no SMG$) and largely
  implements the reference `tryMove`: exit check via decoded bits, `targetCoord` (N:y-1 E:x+1 S:y+1
  W:x-1 U:lvl-1 D:lvl+1), find existing area by coord, draw next `SCAVE_DECK_LP[LI++]`, reverse-door
  connect test, face-down + `pruneExit` on dead end, `MIRROR_UP_STAIR` for secret doors. Slot model:
  PA is 1-based (checkpoint `ARA = PA-1`); NM = area count; move → NM++, PA=NM (≈ engine push/idx).
- **Plan for ENG_APPLY MOVE (SC-4-1/4-9, M1):** dispatch action 1 → guard phase=explore → call
  `TRY_MOVE` → on moved: `TN++`, clear fellThroughTrap, emit `moved`; if the arrived area is an
  unvisited chamber (card chamber-bit 16) draw `min(level,4)` small-pack cards, emit `drewChamber`,
  set phase ENC (strangers present) or PKP (treasure only) — the chamber draw is shared with G4.
  On dead end: emit `deadEnd`, no `TN++`. On no-exit: emit `blocked`, no `TN++`. Event codes must
  match the reference emission order (SC-6.1-18).
- **Then** the D7–D12 edge fixes below (secret-door numbering, L1 stair-up = cave exit, quake rubble,
  large-pack exhaustion moved:false, turn coupling). Grind `solo-seed23`: move1 `MOVE 3`→ARA1 (plain,
  no draw, PH EXP); move2 `MOVE 4`→ARA2 (chamber draw, PH PKP, EV moved,drewChamber, SEED unchanged).

**Progress (I005):** `ENG_APPLY` action 1 (MOVE) implemented — calls headless `TRY_MOVE`, turn++
on success (SC-4-9), emits `moved`/`deadEnd`/`blocked` via a SCAVE_EVQ event queue; SCCONF now
parses the action keyword (at INBUF+5) + args and translates event codes to names (EV_NAME_PTR).
`MAP.OBJ` added to the SCCONF link. solo-seed23 **move 1 matches**; next: chamber-draw-on-arrival
(the `drewChamber` event + ENC/PKP phase on landing in an unvisited chamber) — shared with G4.

- [ ] D7 Any printed level-1 stair-up is a cave exit; DIR_UP still blocked on L1 — SC-6.1-12
- [ ] D8 Secret doors: mirrored stairs (fresh draws AND already-placed areas), numbered — SC-6.1-13/14/15/17
- [ ] D9 Quake rubble impassable + withdraw-blocked-onto-destroyed — SC-6.1-5, SC-7.2-12
- [ ] D10 Large-pack exhaustion: `moved:false`, not a dead end — SC-6.1-6
- [ ] D11 Turn coupling: +1 only on success, clears fellThroughTrap; failed move no turn — SC-4-9
- [ ] M1 Movement event order: moved/deadEnd/blocked exactly as SC-6.1-18 emits them

### G4 — Chambers, hazards, encounters

**Study notes (I007, reference reduce.ts / pickup.ts + local CHAMBER.MAR):** Action codes: TAKE=5,
LEAVE=6, RETAKE=7, GIVE=8, DROP=9. First target = the pickup actions (unblocks solo-seed42 move 3
LEAVE, solo-seed3 move 2 LEAVE, then solo-seed23 move 3 TAKE).
- **SCCONF** needs a general action parser (keyword at INBUF+5 -> code + int args): extend the
  MOVE-only parser to a keyword table. LEAVE/RETAKE/QUIT/EXITCAVE/WITHDRAW/TEST/ATTACK/OPENCHEST = 0
  args; TAKE `<ti> <mi>` = 2; GIVE `<from> <to> <idx>` = 3; DROP `<mi> <idx>`/BORNE `<mi> <idx> <b>`.
- **LEAVE (leaveTreasure)** = if phase!=pickup -> `blocked`; else `persistAndExplore` + phase explore,
  no events. `persistAndExplore` parks the working set into area.contents as codes: strangers 100+cid,
  treasures 200+tid (unless Deep Pool -> area.dropped), sleeping 400+cid, lulled 100+cid; then clears
  CS/CT/CH. Needs a PURE persist in ENGINE writing SCAVE_AREA_AC[area*8+slot] (CHAMBER.MAR's
  SAVE_PERSISTED is headless-ish but in the UI-linked module -- read its exact AC[] slot layout first).
- **TAKE (takeTreasure)** = floor slot ti -> member mi (canCarry weight check); when treasures empty
  -> persistAndExplore. **Lost-Ruby statue** (solo-seed23 move 3): taking the Ruby (tid 13) arouses
  a statue -> combatRoll + memberDied + statueAroused (D49, SC-11-26..28) -- Ruby stays in place.
- Then encounters (ATTACK/WITHDRAW/TEST + reaction roll, SC-8.x) and on-draw hazard resolution
  (deferred from DRAW_CHAMBER).

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

**FIGHT/resolveRound study (I012, reference combatPlan.ts / combat.ts / reduce.ts):**
- **Plan buffer**: reuse STATE's `SCAVE_FIGHT_FA[i]` (front party slot) / `FD[i]` (stranger idx) / `NF`
  (match count) for 1v1 matches (`0>0`, `0>0;1>1`). `+`(multi-front) / `|`(backers) / gang-up need
  more structure -- add when a vector uses them. SCCONF parses the grammar into this buffer.
- **Per-match strength** (simple, no artifacts/Eye): `partyStr = FS[cid] + PK[slot] + MP[cid]`
  (frontStrength = FS + dragonKills + casterMP; caster front adds its own MP); `enemyStr =
  FS[sid] + MP[sid]` (enemyMP, non-Sorcerer no-Eye = creature MP).
- **Dice** (2 per match, in order): `pr=rollDie(seed); er=rollDie(seed)` (RNG verified). Seed
  advances by 2 per match REGARDLESS of outcome. `partyTotal = partyStr + pr + rollBonus + surpriseP`;
  `enemyTotal = enemyStr + er + surpriseE`. rollBonus = (Ring?1:0) - activeCurses (0 simple).
  surpriseP = (round1 && FS==+1)?1:0; surpriseE = (round1 && FS==-1)?1:0.
- **Outcome**: emit `combatRoll` always. party>enemy -> kill strongest stranger in match
  (`strangerKilled`; Dragon single-handed -> PK++; Sorcerer -> sorcererKilled+`sorcererSlain`).
  enemy>party -> mortal front (not ring-inv): 1 -> `memberDied` (status 3); 0 -> deathPrevented;
  >1 -> casualtyQueue (pause for chooseCasualty). tie -> nothing. Then splice killed strangers
  (descending idx), round++.
- **finalizeRound** (after round if no casualtyQueue): party all dead -> gameOver(DEAD) +
  sweepFallen(contents) + `gameOver`; else strangers empty -> reclaim floor heavy -> treasures,
  sweepFallen(working), fight=null, `fightWon`, then treasures>0 ? phase pickup : persistAndExplore
  (explore). else still fighting (phase stays fight, round already ++).
- **Deferred within G5**: validatePlan (planRejected), heavy-treasure drop-before-fight (§387),
  Spectre auto-slay, multi-front/backers/gang-up (§395), casualty choice, retreat, sweepFallen loot
  detail. Start: single 1v1 match, no artifacts -> clears solo-seed19 m10 (win) + solo-seed777 m5 (loss).

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

- **I024 | 2026-07-13 | §9 | multi-front fight model + casualty queue + sweepFallen** — Generalized the
  reduced 1-front FIGHT_ROUND to the full reference resolvePlannedRound. STATE: 2D plan (FN/BN/SN +
  flattened FA/FB/FD[i*MPM+j], MPM=12) + casualty queue (CQN/CQ). SCCONF: full plan-grammar parser
  (`front+front|backer>stranger+stranger`, ';'-separated) + casualtyChosen/itemsSpilled names.
  ENGINE: FIGHT_ROUND now sums frontStrength over the front list + casterMP over backers, enemyStr
  over strangers + gang-up attach + folded caster MP; win -> kill the STRONGEST foe (fs+MP) +
  dragonKills (single-handed lone Dragon) + sorcererSlain; lose -> 0 deathPrevented / 1 memberDied /
  >1 casualtyQueue. New helpers FRONT_STR/ENEMY_STR (fs+PK+MP / fs+MP) and IS_FRONT/IS_ENGAGED (2D
  scans); GANG_UP + SPECTRE_CHECK refitted to the 2D plan. EA_CASUALTY(14): d6>=4 honours the pick,
  else the other of the queued pair falls; queue drains -> FINALIZE_ROUND. FINALIZE_ROUND + SWEEP_FALLEN
  (mode 0 -> pickup CT on a win, mode 1 -> tile AC 200+tid on a wipe), emitting itemsSpilled before
  fightWon/gameOver. *Evidence:* solo-seed174 diverged step 55 -> now PASSES end-to-end (multi-front
  `4+0>0`/`4+2>0`, CASUALTY, sorcererSlain, step-57 + step-66 itemsSpilled all bit-for-bit); **base-8
  still 8/8 -> 9/9 vectors green.** Deferred (unexercised): §387 in-fight heavy-drop + win-reclaim,
  reconcileUnicorns (unicornDeparted), Spectre-match memberStr=casterMP, fold-focus = first non-Spectre.

- **I023 | 2026-07-12 | §8 | TEST/reaction layer ported into the engine** — Unblocked the
  engine-completion grind against the 6 existing reference vectors. Extended SCCONF to parse
  TEST(11)/CASUALTY(14)/OPENCHEST(17) and added event names reaction/strangersJoined/pacified/
  unicornGuards (codes 20-23). Implemented action 11 (EA_TEST) in ENGINE.MAR with helpers
  REACTION_ROLL (leader d6 + charisma +1 - activeCurses, clamp, natural-1, classify vs
  hostileMax/indiffMax), FIND_LEADER (highest leaderPri, ties->first), HAS_CHARISMA, HAS_WOMAN;
  new state SCAVE_STATE_IS (indiffStreak, reset on chamber entry). Outcomes: hostile->fight
  surprise-1; indifferent->streak, 3rd pacifies (AF_PERMINDIFF + persist); friendly->recruit all
  as allies (no cap), womanless Unicorn guards + pacifies, then pickup/explore. *Evidence:*
  `make vms-scave-conform VEC=solo-seed174-party1-7-sorcerer` advances **step 8 -> step 55** (all
  TEST/reaction/recruit lines match bit-for-bit); base-8 still **8/8 PASS** (no regression). Next
  divergence: step 55 multi-front FIGHT plan `4+0>0` + CASUALTY + sorcererSlain (§9 fight model).

- **I022 | 2026-07-12 | G7 | Part I audit (10-agent workflow)** — Fanned out one read-only audit
  agent per spec section §3-§12; each mapped every solo SC-row of engine-spec.md Part I to the
  MACRO-32 port with a verdict + file:line evidence. Synthesized to
  [G7-AUDIT.md](G7-AUDIT.md) (317 rows). *Tally:* 136 conformant, 164 gap, 9 ui-pending, 7
  discrepancy, 1 na-multiplayer. *Decisive finding:* `ENGINE.MAR` is a **vector-driven subset** --
  it implements exactly what the 8 vectors touch. The 164 gaps are the rules no vector exercises
  (TEST/reaction §8, artifacts+Eye §11, RNG hazards §7, multi-front fights §9, retreat/carpet/flute
  §6, openChest/bonusScore §12, pick-validation §5). Most live in the legacy interactive modules
  that SCCONF doesn't link -- and the audit flagged real defects in several of those legacy paths
  (STRANGER.MAR: curses not zeroed on Sorcerer-kill SC-8.3-3; natural-1 clobbered by HAS_CHARISMA
  SC-8.3-5; friendlies capped at 12 vs no-cap SC-8.4-7; per-area indiff counter persists across
  visits + never resets vs per-visit streak SC-8.4-3/5). *Accepted discrepancies* (deliberate MACRO
  architecture, not work): SC-6-5 / SC-6.2-2 -- global in-place mutation instead of structuredClone.
  *Consequence:* G7's exit test (checklist 100% marked with evidence) is MET, but it proves the
  strangler-fig migration only covered the vector subset. A true G8 needs the engine finished first.

- **I021 | 2026-07-12 | G6 | special crossing (Viper Pit + Deep Pool) -- 8/8 PARITY** — New in
  ENGINE.MAR: capture `fromSpecial`/`oldPrev` before the move, then in EA_MOVED fire the crossing
  BEFORE `moved` when leaving a viper/pool for a genuinely new area (`newPA != oldPrev`).
  `VIPER_CROSSING` rolls a d6 per living member (fatal on 1-2 -> memberDied + treasure lost),
  emits `viperPit` then per-victim `memberDied`, and ends the game DEAD on a full wipe.
  `DEEPPOOL_CROSSING` lets a living Giant carry all, else drops each member's heavy loot (ids 0-2)
  with `treasureDropped`. SCCONF gains crossedSpecial/viperPit/treasureDropped (codes 17-19).
  ENG_APPLY mask widened to ^M<R2..R7>. *Bug found + fixed:* the initial `EXTZV #7,#3,MAP_MP[R2],..`
  read garbage -- a variable-bit-field instruction's base-operand index scales by **1 byte, not 4**
  (same class as BBS/BBC). Fixed by `MOVL MAP_MP[R2],R6` first, then `EXTZV ...,R6,R6`. This one bug
  had both spuriously fired crossings on plain areas (seed7/seed3 regressions) AND missed the real
  viper/pool decodes (seed42/seed11). *Evidence:* `make vms-scave-conform` on all 8 vectors -> **8/8
  PASS bit-for-bit** (seed23, seed777, seed101, seed11, seed19, seed7, seed42, seed3). Loop status -> DONE.

- **I020 | 2026-07-12 | G4 | on-draw hazards (Earthquake)** — New `RESOLVE_HAZARDS` in ENGINE, called
  after the chamber draw: iterates the fixed priority order (Earthquake, Medusa, Ghouls, Mutiny, Trap
  via HAZ_ORDER), emits `hazardFired` per present hazard, then clears NH. Earthquake's effect wired
  (collapse prev if prev!=partyArea: AF_DESTROYED + clear its AC), no RNG. RNG hazards + wards still
  emit hazardFired but skip the effect (deferred). *Evidence:* solo-seed42 10→**27** (Earthquake +
  the following moves/fights match); no regression (still 6/8). *Both remaining vectors now blocked on
  the SAME feature:* special crossing (`crossedSpecial`) -- seed11 move 4 (Deep Pool, no roll),
  seed42 move 27 (Viper Pit, `viperPit` roll). That's the last feature for a full 8/8 sweep.
- **I019 | 2026-07-12 | G6 | Lost-Ruby statue (SC-11/D49)** — Taking the Ruby (tid 11) now routes to
  a new `STATUE_WRESTLE` (reference takeTreasure tid===11): the taker wrestles a strength-8 statue --
  fighterTotal = frontStrength + d6 vs 8 + d6 (fighter die first, 2 rolls) -> `combatRoll`; on a win
  the Ruby is taken (`rubyTaken`, spliced), on a loss the taker dies (`memberDied`,`statueAroused`,
  Ruby stays; a wipe -> gameOver). EA_TAKE detects the Ruby at the floor slot and dispatches. Added
  event codes/names; fixed invalid `4B$`/`4C$` locals -> named labels. *Evidence:* **solo-seed23
  PASSES** (its Woman loses the wrestle and dies, matching) -> 6/8. No regression.
  *Remaining 2:* seed42 on-draw hazards (G4), seed11 special crossing (G6).
- **I018 | 2026-07-12 | G5 | gang-up (§395/D28)** — New `GANG_UP` in ENGINE (reference previewPlan):
  when the party has NO free fighter, the strongest unengaged/unassigned non-caster non-Spectre
  leftover stranger ATTACHES to each match (strongest first, into `SCAVE_FIGHT_ATTACH[i]`) and the
  leftover CASTERS fold their MP (`SCAVE_FIGHT_FOLD`) onto the focus match. FIGHT_ROUND adds the
  attached stranger's FS+MP to that match's enemyStr and the fold to match 0. Fixed 2 far branches
  (invert+BRW). *Evidence:* **solo-seed7 PASSES** (its W-Hero match now loses to an attached foe) ->
  5/8. No regression. Fight system complete: 1v1 / multi-match / Spectre / gang-up.
  *Remaining 3:* seed23 statue (G4/D49), seed42 on-draw hazards (G4), seed11 special crossing (G6).
- **I017 | 2026-07-12 | G5 | Spectre + multi-match** — SCCONF FIGHT parser now handles a
  `;`-separated list of 1v1 matches into FA[i]/FD[i]/NF (and `FIGHT -` -> NF=0). New `SPECTRE_CHECK`
  in ENGINE (SC-9.4): an idle Spectre (creature 9 in no match) that the party can't engage (no caster
  base-MP, no Magic Sword) slays the strongest living member (max FS+PK) -> spectreSlew, no RNG; runs
  before the match loop in FIGHT_ROUND. Added the event code/name; fixed 3 far `SK_RET` branches
  (invert+BRW). *Evidence:* **solo-seed19 fully PASSES** (Spectre wipe over 2 rounds) -> 4/8.
  solo-seed7 multi-match parses right but move-19 outcome flips: it needs **gang-up (§395/D28)** --
  with no free fighters a leftover stranger attaches to a 1v1 match, raising enemyStr (the dice/seed
  already match). *Remaining:* seed7 gang-up, seed23 statue, seed42 hazards, seed11 crossing.
- **I016 | 2026-07-12 | G6 | scoring (SC-12)** — Pure `COMPUTE_SCORE` in ENGINE (reference
  scoreBreakdown): per ALIVE member `CR_PTS[cid]*(PK>0?2:1) + Σ TR_PTS[carried]`, +30 sorcerer
  bonus, -30 flat curse penalty (unless SK), DEAD->0 else floor 0. SCCONF DO_FINAL calls it for the
  FINAL SCORE instead of the raw field. bonusScore (chest) deferred (=0). *Evidence:* solo-seed3
  FINAL SCORE 50 matches -> **solo-seed3 fully PASSES (3/8)**. No regression.
- **I015 | 2026-07-12 | G4-G6 | EXITCAVE + D7 + faceUp** — EXITCAVE (escape on a level-1 up-stair);
  D7 keep printed level-1 up-stairs (block DIR_UP moves instead) + fix a BBS index-scaling bug (bit
  ops scale x1 not x4 -> load card to a register); per-area faceUp (SCAVE_AREA_FU) emitted instead of
  hardcoded FU 1. solo-seed3 -> only SCORE remained.
- **I014 | 2026-07-12 | G3/D8 | secret doors (mirrored stairs)** — A vertical move onto a card
  lacking the return stair mirrors it (MAP.MAR `MIRROR_UP_STAIR` now both dirs: descend->AU ^X20,
  ascend->AD ^X40) AND records it: `SCAVE_AREA_MIR[area]` |= bit, and lays a secret-door ordinal
  `SCAVE_AREA_SD[area]` = `SCAVE_MAP_SDN++` if none yet (SC-6.1-13/14). New STATE fields, INIT_MAP
  inits (MIR=0, SD=-1, SDN=0). SCCONF's AREA line now emits the real `MIR !SL SD <n|->` instead of
  the hardcoded `MIR 0 SD -`. *Evidence:* the lone remaining divergence on seed777/seed101 (`AREA 2
  ... MIR 32 SD 0`) closes -> **both vectors now fully PASS** (2/8). *Remaining FAILs:* seed23 statue,
  seed11 crossedSpecial (G6), seed19 Spectre `FIGHT -`, seed7 multi-match, seed42 hazard, seed3 EXITCAVE.
- **I013 | 2026-07-12 | G5 | FIGHT (single 1v1 resolveRound)** — Added FIGHT (code 13): SCCONF
  marshals `<f>><s>` into FA[0]/FD[0]/NF=1; ENGINE `FIGHT_ROUND` computes partyStr (FS+PK+MP) /
  enemyStr (FS+MP), rolls party-then-enemy die per match, adds rollBonus(-curses)+surprise, emits
  combatRoll, kills the loser (strangerKilled / memberDied), compacts CS, round++. `EA_FIGHT` then
  finalizes: wiped→gameOver(DEAD); strangers cleared→fightWon (+pickup/explore); else keep fighting.
  Added COUNT_LIVING, 6 event codes/names, GS/PS/PH consts. Fixed 6 far `BRB DM_APPLY`→BRW (parser
  grew past 127B). *Evidence:* build clean; **seed777 + seed101 now match every move line**
  (FINAL-block only); seed3 53→**61** (60/61, only EXITCAVE); seed19 10→17 (Spectre `FIGHT -`);
  seed7 at multi-match `0>0;1>1`. No regression. *Deferred within G5:* multi-match/`;`, `FIGHT -`
  Spectre, validatePlan, casualty queue, heavy-drop + sweepFallen loot (the FINAL-block gap), Dragon
  /Sorcerer credit. Also next: EXITCAVE (seed3), on-draw hazards (seed42), statue (seed23).
- **I012 | 2026-07-12 | G5 | ATTACK (startFight)** — ATTACK (code 12): blocked outside encounter;
  else FS = surpriseReady (+1 fresh entry, else 0), RD=1, phase fight, emit fightStarted; clears SR.
  Added `SCAVE_STATE_SR` (surprise-ready), set in EA_CHAMBER's encounter branch (fresh draw=1,
  revisit=0). SCCONF parses ATTACK; fightStarted event added. Pacified-area attack from explore
  (D22) deferred. *Evidence:* build clean; solo-seed19 9→10, solo-seed3 52→53, solo-seed777 4→5 —
  **all now at FIGHT 0>0**. *Result:* fight ENTRY done; next is FIGHT/resolveRound (battle-plan
  grammar `<front>[+..][|<backer>]><stranger>`, per-match dice + modifiers, casualty queue,
  sweepFallen, win/loss) -- the biggest single piece.
- **I011 | 2026-07-12 | G4 | WITHDRAW** — Added the WITHDRAW action (code 4): blocked outside
  encounter / if prev area is AF_DESTROYED (fellThroughTrap block deferred with trap falls); else
  parks the current area (PERSIST_AREA), moves back to prev (PA=PP, level from ML[PP]), phase
  explore, emits moved. No turn, no RNG. SCCONF parses WITHDRAW. *Evidence:* build clean;
  solo-seed19 2→9, solo-seed3 48→**52** (51/61 moves match); no regression on solo-seed23.
  *Result:* G4 non-fight actions largely done (pickup/revisit/withdraw). Remaining fronts:
  ATTACK/FIGHT (G5), on-draw hazards (seed42), Lost-Ruby statue (seed23), TEST reaction.
- **I010 | 2026-07-12 | G4 | chamber revisit** — Added a pure `REVISIT_CHAMBER` (reference
  enterChamber "visited" branch): rebuilds CS/CT/CH from the area's parked AC[PA*8+slot] codes by
  type (100/200/300), clearing each slot (contents=[]); EA_CHAMBER now splits fresh (DRAW_CHAMBER)
  vs visited (REVISIT_CHAMBER), both -> drewChamber + ENC/PKP phase. No RNG. *Evidence:* build
  clean; **solo-seed3 8→48** (matches 47/61 moves now; diverges at WITHDRAW = encounter); no
  regression on solo-seed23/seed42. *Result:* pickup+revisit machinery solid; the big remaining
  unblocker is encounters (WITHDRAW/ATTACK/TEST + reaction roll, needed by seed3/777/101/19/7).
- **I009 | 2026-07-12 | G4 | TAKE (takeTreasure, plain)** — Added `TAKE_TREASURE(ti,mi)` (reference
  pickup.ts): canCarry weight check (carriedWeight + WT[tid] <= CR_CARRY[creature]), push tid to the
  member's first empty PT slot, splice CT (shift down, NT--); returns floor-emptied so EA_TAKE
  persists + explores. TAKE action (code 5, blocked outside pickup). Lost Ruby (tid 11) no-ops here
  pending the statue path. SCCONF parses TAKE `<ti> <mi>`. *Evidence:* build clean; solo-seed3
  5→**8** (TAKE + revisit; move 8 = chamber-revisit reclassify, deferred); solo-seed23 move 3 Ruby
  now no-ops (PH PKP matches, only EV/statue differ); no regression on solo-seed42. *Next:* chamber
  revisit (LOAD_PERSISTED-style reclassify), on-draw hazards, Lost-Ruby statue, encounters.
- **I008 | 2026-07-12 | G4 | LEAVE (leaveTreasure)** — Added a pure `PERSIST_AREA` (reference
  persistAndExplore: park CS as 100+cid, CT as 200+tid into SCAVE_AREA_AC[PA*8+slot], pad 0, clear
  the working set) and the LEAVE action (code 6): blocked outside pickup, else persist + phase
  explore, no events. Extended SCCONF's action parser (MOVE + LEAVE). *Evidence:* build clean;
  solo-seed42 divergence 3→**10** (moves incl. 2 LEAVEs match; move 10 = on-draw hazardFired),
  solo-seed3 2→**5** (TAKE), no regression on solo-seed23. *Result:* pickup-phase persist works;
  next TAKE (takeTreasure + Lost-Ruby statue) and on-draw hazard resolution.
- **I007 | 2026-07-12 | G3 | enteredSpecial (SC-10-3)** — ENG_APPLY MOVE now decodes the arrived
  area's special type (card bits 7-9); Deep Pool (2) / Viper Pit (3) emit `enteredSpecial` + stay
  in explore, before the chamber path. Added the event code/name; fixed a far `BNEQ EA_DONE`
  (invert+BRW). *Evidence:* ran all 8 vectors (fast now) and classified each first divergence:
  **7/8 reach their first non-move action; solo-seed11 reaches move 4** (its move 3 `MOVE 1 ->
  moved,enteredSpecial` now matches; move 4 is `crossedSpecial` = G6 crossing). No regression on
  solo-seed23/seed7. *Result:* G3 movement complete; advance to G4. Deferred to G6: special
  crossing on move-out (solo-seed11 move 4).
- **I006 | 2026-07-12 | G3 | chamber-draw-on-arrival** — Added a pure `DRAW_CHAMBER` to ENGINE.MAR
  (headless counterpart to CHAMBER.MAR's UI-coupled deal loop): marks the area visited, deals
  min(level,4)(+Tomb/+Hall, cap 8) small-pack cards into CS/CT/CH by type, advancing SI (SC-7.1-2/4).
  ENG_APPLY MOVE now, on landing in an unvisited chamber (card bit 4), calls it, emits `drewChamber`,
  and sets phase ENC (strangers) / PKP (treasure) / EXP. Fixed 3 `%MACRO-E-BRDESTRANG` (unified the
  bucket store to keep branches in byte range; BRW for the far loop/exhaustion targets). *Evidence:*
  `conform solo-seed23` diff advanced to move 3 — **move 2 now matches** (`PH PKP EV moved,drewChamber
  SEED 446078340`); first divergence is the first non-move action (TAKE stub). *Result:* G3 movement
  proven for solo-seed23 through both moves; TAKE/statue is G4.
  **Infra (major):** the VAX FTP server had a 60s reverse-DNS stall on every connection (stale
  nameserver `mikrotik.hecnet.eu` from an old topology). Fixed server-side by repointing the resolver
  at `192.168.4.1` (fast NXDOMAIN) -> FTP ~61s -> ~1s, builds minutes -> ~30s. Also added a 120s
  hard timeout to `vmsftp` (subprocess) so a future data-connection hang aborts + retries.
- **I005 | 2026-07-12 | G3 | ENG_APPLY MOVE** — Implemented the MOVE action: ENGINE.MAR dispatches
  action 1 → guards phase → `TRY_MOVE` → `TN++`/`moved` on success, `deadEnd`/`blocked` otherwise
  (SC-4-9, event queue). SCCONF DO_MOVE now parses the action keyword+args and translates SCAVE_EVQ
  codes to names. Linked MAP.OBJ into SCCONF. *Evidence:* build clean; `conform solo-seed23` diff
  moved from move 1 to move 2 — move 1 (`MOVE 3`→TRN 2 ARA 1 PH EXP EV moved) matches exactly, and
  move 2 matches on TRN/ARA/SEED/moved, diverging only on the chamber draw (PH EXP vs PKP, no
  drewChamber). *Result:* G3 partial; chamber-draw-on-arrival next.
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
