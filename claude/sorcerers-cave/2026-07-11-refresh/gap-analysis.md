# Gap Analysis — VAX MACRO-32 SCAVE vs the reference engine

> Written 2026-07-11. Companion to [loop-spec.md](loop-spec.md), which turns this analysis
> into an autonomous work loop.
>
> **Reference ("the engine"):** `/Users/msw/code/retro/sorcerers-cave/packages/engine`, specified by
> `docs/specs/engine-spec.md` (v2, Part I = normative `SC-*` rules, Appendix A = data/RNG/state,
> Appendix B = deliberate deviations, Appendix D = conformance vectors) and
> `docs/specs/PORTING-GUIDE.md`. Scope: **solo play only** — §MP, the web UI, Convex, and
> replay-by-code are out of scope by instruction.
>
> **Target:** `src/macro32/sorcerer/` (15 modules → `SCAVE.EXE`), inventoried 2026-07-11 from
> source + `PLAN.md` + `claude/sorcerers-cave/2026-06-12-detailed-design/design-spec.html`.
>
> Historical note that shapes everything below: the June `design-spec.html` (written FROM this
> MACRO-32 code) is the **v1 spec the online engine started from**. The engine then evolved past
> it; engine-spec **Appendix B is therefore a curated list of exactly where today's MACRO-32 code
> is "correct to v1/the book" and must still change**. §15 of the June doc is the MACRO-32 side's
> own gap list and was verified against current source — both fed this analysis.

## 1. Verdict in one paragraph

The MACRO-32 version is a faithful v1 implementation with a **correct RNG core** and **mostly
correct static data**, but it diverges from the reference in four structural ways: (1) the
**52-card two-era small pack** instead of the engine's single 71-card deck that the party is
drawn from; (2) **focus-fire combat** instead of the engine's submitted-battle-plan model with
its validation rules; (3) roughly **half of §7–§11 mechanics missing** (most active artifacts,
loot-on-death model, casualty choice, heavy-treasure drop, secret doors, pacified re-attack…);
and (4) **no engine/UI boundary and no test harness**, so conformance cannot even be measured
yet. The UI works but is a single full-screen paint with known feedback/clutter weaknesses.
Parity is provable only through the eight conformance vectors; the port must build that harness
first (PORTING-GUIDE §4).

## 2. What already matches the reference (keep, verify under vectors)

| Area | Evidence |
|---|---|
| **LCG** `seed' = (seed*1103515245 + 12345) & 0x7FFFFFFF` | `RNG.MAR:79-84` (`BICL2 #^X80000000`) = A.5. First self-check `nextSeed(1)=1103527590` should already pass |
| **Die derivation** bits 15..30, `/10923`, clamp 5, +1 | `RNG.MAR:93-104` (`EXTZV #15,#16`, `DIVL2 #10923`) = SC-5-7 |
| **randBelow** `bits mod n` | `RNG.MAR:116-129` = SC-5-8 (verify the `n<=0` no-advance case) |
| **Fisher–Yates** `i = len-1 … 1`, `j = randBelow(i+1)`, swap | `RNG.MAR:145-166` = SC-5-9 |
| **Area-card bitfield** exits/chamber/stairs/special | `DATA.MAR:63-76` = SC-3-2 |
| **61 area cards, Gateway value 175 at index 21, pre-placed** | `DATA.MAR` + `SETUP.MAR` = SC-3-1 (except index 41, §3.1 below) |
| **Creature FS / MP / carry / cost / points / leaderPri** | `DATA.MAR` parallel arrays = A.1 verbatim (all 14 rows) |
| **Treasure points/weights** (Silver/Gold/Gems 25 kg, Chest 100 kg, 12 weightless artifacts) | `DATA.MAR` = A.2 verbatim |
| **Party budget 6, stock 1,1,3,3,3,6,3,3, costs 6,5,5,4,4,3,2,1** | `SETUP.MAR:276-365` = SC-3-7/9, SC-5-2 |
| **Chamber draw** `min(level,4)` +1 Tomb +2 Great Hall, cap 8; caps 8/8/4 | `CHAMBER.MAR:297-376` = SC-7.1-2/3/5 |
| **Card codes** 100+cid / 200+tid / 300+hid | = SC-3-17 (`400+cid` sleeping missing — no Lotus yet) |
| **Hazard firing order** Earthquake → Medusa → Ghouls → Mutiny → Trap | `CHAMBER.MAR:708` = SC-7.2-1 |
| **Reaction roll shape** d6 +1 charisma −curses, clamp 1..6 | `STRANGER.MAR:155` ≈ SC-8.3 (natural-1 nuance differs, §3.4) |
| **Leader priority order** | = SC-8.2-1 |
| **Coord packing** `level*10000 + y*100 + x`; dead-end prune + face-down placement | `MAP.MAR` = SC-3-19, SC-6.1-9/10 |
| **Scoring skeleton** living-only, dragon-slayer ×2 creature pts, +30 Sorcerer, clamp ≥0, DEAD→0 | `SCORE.MAR:140` ≈ §12 (curse penalty differs, §3.8) |
| **Tiles never rotated** | true by construction = SC-6.1-11 |

## 3. Divergences (the work list)

Ordered roughly as the porting guide's milestones. `SC-*` ids are the normative rows to
implement against; **every one of these is expressed in the seeded backlog in
[loop/LEDGER.md](loop/LEDGER.md)**.

### 3.1 Static data (milestone M1) — small, mechanical, but gates everything

| # | MACRO-32 today | Reference requires |
|---|---|---|
| D1 | Small pack = **52 cards** (19 creatures, 27 treasures, 6 hazards; "rulebook pack, no cave Priests" per `DATA.MAR:319-321`) | **71 cards**: 37 creatures (Hero1 W-Hero1 Ogre3 Troll3 **Priest3** Man6 Woman3 Dwarf3 Wizard3 Spectre3 Dragon3 Sorcerer1 Giant3 Unicorn1), 27 treasures (same), **7 hazards** (Mutiny1 Trap2 **Earthquake2** Medusa1 Ghouls1) — SC-3-13..16 |
| D2 | Party members conjured from stock; deck untouched | Party is **drawn from the shuffled small pack** — each pick's card (100+id) removed once, SC-5-5. Follows from D1 |
| D3 | Area card **index 41 = 74** (EWD) — `DATA.MAR:72` | **42** (EWU) — SC-3-3 (EWD has no tile; avoids illegal rotation) |
| D4 | Reaction cells: Hero 0/0, Priest 0/0, Man 0/0, Woman 0/0, Dwarf 0/0, **Dragon 6/6** | Hero **3/3**, Priest **1/4**, Man/Woman **2/4**, Dwarf **0/4**, Dragon **4/6** — A.1 / Appendix B ("humans always friendly" is the v1 reading; match the engine, not the book) |
| D5 | Seed from `$GETTIM`, forced odd | Seed is a **caller-supplied parameter** (SC-5-13). Keep clock seeding for casual play, but newGame must accept an injected seed (conformance + scripted UI runs) |
| D6 | RNG consumption order at setup unverified | Must be **large pack → small pack → store cursor** (SC-5-12); the SETUP line of every vector proves it |

### 3.2 Architecture (milestone M0 — the enabler)

The engine is `reduce(state, action) → {state, events}` (SC-4-1); MACRO-32 is a blocking
keystroke loop with SMG calls interleaved into rules code (`CHAMBER.MAR` 1943 lines does draw
+ hazards + pickup UI). **Without an action/event boundary the conformance vectors cannot be
replayed at all.** Required, per PORTING-GUIDE §4 ("build this first"):

- A headless entry pair — `ENG_NEWGAME(seed, picks)` and `ENG_APPLY(action…) → events` — with
  all game facts produced by the engine, never inferred by the UI (SC-4-1). In-place mutation is
  fine (PORTING-GUIDE §3), but a **rejected/blocked action must change nothing** (SC-4-6,
  SC-4-24) and a failed move must leave state untouched except documented pruning (SC-6.1-1/4/9).
- The 17-action catalog (SC-4-41) and 49-event catalog (SC-4-42) as integer codes.
- Phases `explore/encounter/fight/pickup/gameOver` as the interactive contract (SC-4-3..5).
- A second link target **`SCCONF.EXE`** (vector replayer: parse `solo-*.txt`, apply, print
  checkpoint lines in the exact vector format) sharing every engine object with `SCAVE.EXE`.

### 3.3 Movement & map (M3)

| # | Gap | Ref |
|---|---|---|
| D7 | Level-1 escape only via the Gateway's stair | ANY printed stair-up on level 1 is a cave exit; DIR_UP move still blocked on L1 | SC-6.1-12 |
| D8 | Secret doors absent | Vertical move onto a card lacking the return stair mirrors one (`mirroredStairs` 32/64, numbered `secretDoor`), including onto already-placed areas | SC-6.1-13/14/15/17 |
| D9 | Earthquake "destroyed" flag exists; traversal-block semantics unverified | AF_DESTROYED areas are impassable rubble (prune, deadEnd); withdraw onto destroyed `prev` blocked | SC-6.1-5, SC-7.2-12 |
| D10 | Pack-exhaustion behaviour unverified | Exhausted large pack → `{moved:false}` and NOT a dead end | SC-6.1-6 |
| D11 | Failed move / turn counter coupling unverified | Successful move: turn+1, clears `fellThroughTrap`; failed move does NOT advance the turn | SC-4-9 |
| D12 | Dead-end forced redraw: not implemented | Also deliberately absent in the engine — **keep absent** | SC-6.3-1 |

### 3.4 Chambers, hazards, encounters (M4)

| # | Gap | Ref |
|---|---|---|
| D13 | Ghouls: straight FS+d6 vs 2+d6 death rolls | FIRST all living members drop heavy treasure to the floor; Talisman wards entirely; Ring-invincibility (L≥4) prevents death; slain members' carried artifacts spill to the floor (`sweepFallen`) | SC-7.2-5/6/7 |
| D14 | Medusa: victim "drops treasure" | Victim's CARRIED items spill to floor; BORNE items petrify with the body; Staff-ward matches already | SC-7.2-3/13 |
| D15 | Trap: single Dwarf guides past ONE trap, "dwarf dies later → fall on leaving" memory | ANY living FLAG_GUIDES_PAST_TRAP member → `trapAvoided`, no one-trap-only limit, no deferred fall. Trap fall may CHAIN (re-enters resolution below, same turn) | SC-7.2-9, SC-4-14 |
| D16 | Mutiny ≈ matches | Verify splice order (deserters spliced out preserving order) + all-ally loyal-first rule | SC-7.2-8 |
| D17 | Medusa/Ghouls lurk re-park; Earthquake scar | Re-park 300+id into contents; quake scar to display-only `markers`, never re-fires | SC-7.2-10 |
| D18 | Natural-1 forces **hostile** | Natural 1 forces the effective roll to **1**, which is hostile only if the leader's hostileMax ≥ 1 (a Dwarf-led group: 1 = indifferent) | SC-8.3-5 |
| D19 | Withdraw always available | Blocked after a trap fall and when `prev` is quake-destroyed | SC-4-17, SC-8.1-3 |
| D20 | Surprise semantics coarse | `surpriseReady` only on fresh non-trap entry; testing forfeits it; Attack +1 only if ready; hostile test / hostile-area re-entry give strangers −1 | SC-4-16/21/22, SC-7.1-11 |
| D21 | Retreat-from-fight aftermath | Fled area becomes hostile-on-sight (`hostileAreas`) → immediate fight with strangers surprised on return | SC-4-28, SC-8.4-2 |
| D22 | Pacified areas: can never re-engage | Pacified (3× indifferent) area allows free traversal AND an explicit Attack that un-parks guards+treasure, surprise 0 | SC-10.4-3/4 |
| D23 | Unicorn always friendly | Friendly Unicorn joins only with a Woman/W-Hero; womanless Unicorn stays as guard and pacifies the area (`unicornGuards`) | SC-4-19, SC-10.4-5 |
| D24 | No passage-tile floor pickup | Treasure dropped/left on a passage tile is re-offered as pickup on return | SC-7.3-12 |
| D25 | 20 pack-slots per member | No such cap in the engine; remove or raise beyond reach (vectors index member `treasure[]` positionally — array order must evolve identically) | PORTING-GUIDE §3 |
| D26 | Party cap 12 | No party-size cap (friendly groups join in full; bound only by the finite pack). Arrays must grow (23 starters + 37 deck creatures is the theoretical ceiling) | SC-3-21, SC-8.4-7 |

### 3.5 Fights (M5) — the big rewrite

The entire §9 model changes from "pick a focus stranger, auto-pile" to **player-submitted
battle plans with validation**:

| # | Gap | Ref |
|---|---|---|
| D27 | Focus-fire pairing | `resolveRound(matches)`: fronts (1–2) + caster backers vs foes (1–2); rejection reasons (`twoVsTwo`, `mustEngageAll`, `backerNotCaster`, reuse, dead member…); illegal plan = `planRejected`, zero state change | SC-9.1-1..9 |
| D28 | — | Out-numbered gang-up only when no free fighter; enemy-caster MP fold-in to the focus match | SC-9.1-10/11 |
| D29 | Casualty = auto | Two-losers case queues `chooseCasualty`: player names the preferred casualty, d6 4–6 honours it | SC-9.5-4/5, SC-4-26 |
| D30 | No heavy-treasure drop | Every front fighter drops heavy treasure at round resolution (`fightDrops`); reclaimed on win; `retakeDropped` | SC-9.5-1/2, SC-7.3-10 |
| D31 | Retreat any time; no blocked-retreat state | Retreat only after round 1, never after trap fall, any exit incl. unexplored; dead-end retreat sets `retreatBlocked` (fight on) | SC-9.5-6/7, SC-4-27 |
| D32 | Casters support only | A caster fighting hand-to-hand fights at TOTAL strength (FS+MP); vs a Spectre a caster pits MP only, a sword-bearer full FS | SC-9.3-1, SC-9.4-2 |
| D33 | Spectre auto-slay ≈ present | Nuances: never gang-up-attached; forced-Spectre EMPTY plan; sole-caster may leave a second Spectre unengaged; Ring blocks the auto-slay | SC-9.4-3..6 |
| D34 | Dragon-slayer credit on any win | Only single-handed (1 front, no backers, 1 stranger); caster backer voids it | SC-9.4-7 |
| D35 | No death-loot model | `sweepFallen`: dead members' CARRIED items spill (win → pickup floor; wipe → tile contents); BORNE items lost with the body; retreat leaves the fallen's everything; viper deaths lose all into the pit | SC-9.5-8/11 |
| D36 | Sorcerer plain | Eye −2 MP (never 0), Lotus −2 more, floor 0; kill sets `sorcererKilled`, lifts curses | SC-9.4-8, SC-12-10 |
| D37 | Surprise ±1 both sides ≈ present | Round 1 only; verify exact die-total application | SC-9.2-1 |

### 3.6 Special areas (M6)

| # | Gap | Ref |
|---|---|---|
| D38 | Viper Pit fatal on **1** only | Fatal on **1 or 2**; per-member d6; flute lulls (eligible player only); fallen's treasure lost INTO the pit | SC-10.1-1..6 |
| D39 | Deep Pool per-doorway drop points, reclaim by return-through-doorway | Single `dropped` list on the tile; crossing = leaving by a different exit than entered (retrace safe); reclaim is a **Giant-only weight-limited pickup**; unclaimed sinks back | SC-10.2-1..6, SC-10-3/4 |
| D40 | Entry/crossing timing unverified | Entry stops at the edge (explore); crossing fires on the NEXT move out, not on entry, and only when not retracing | SC-10-3/4 |

### 3.7 Artifacts (M6) — mostly absent

Passive Sword/Staff/Ring(+1)/Potion(+2 path) exist in FIGHT; everything else:

| # | Artifact | Missing behaviour |
|---|---|---|
| D41 | `useArtifact` + `openChest` actions & UI | Whole active-use surface: per-artifact phase/target/bearer gates (SC-4-34/35) |
| D42 | Healing Balm | Woman/W-Hero/Priest/Wizard holder revives a dead member (explore/pickup), single-use — SC-11-14/15 |
| D43 | Lotus Dust | Sleep a stranger (400+id parked); no effect on Spectre; Sorcerer −2 MP instead; ends fight if last awake foe — SC-11-9..13 |
| D44 | Magic Carpet | Priest/Wizard bearer only; explore; one step ignoring doors; UP blocked on L1; consumed — SC-11-4..7 (carpet-landing withdraw rule deliberately NOT enforced, SC-4-40) |
| D45 | Talisman | Wards Ghouls at any level; drives off Spectres at L≥4 — SC-11-16/17 |
| D46 | Strength Potion activation | `useArtifact` in fight targeting Man/Woman/Hero/W-Hero; `potionActive` +2, Eye-immune, cleared at fight end — SC-11-18/19 |
| D47 | Magic Staff reanimation | Wizard frees stone members (active in explore/pickup; passive on re-entry); not consumed — SC-11-21/22, SC-4-44 |
| D48 | The Ring | L≥4 death-immunity on EVERY killing die (fights, Spectre auto-slay, Ghouls, Ruby statue); no reaction bonus (already correct) — SC-11-24/25 |
| D49 | Lost Ruby | Strength-8 statue wrestle on take; loser slain + carried spill; Ruby re-attemptable; Eye stills the statue — SC-7.3-9, SC-11-26..28 |
| D50 | Charmed Flute | Dragon lull (passive, eligible players), secret-door reveal (`USE 12 D5/D6`), viper lull already ≈ present — SC-11-29..33 |
| D51 | Eye of God | Nullifies party magic/Sword/Staff/Ring; annihilates Spectres on entry; Sorcerer −2 only; stills statue; curse on drop/transfer/bearer-death — SC-11-34..39 |
| D52 | Treasure Chest | `openChest` (explore, living carrier): d6 → Curse / Spectre fight / Sand / +20/+40/+80 `bonusScore`; consumed — SC-11-40/41 |
| D53 | Borne/carried (`setBorne`) | Sword/Staff/Ring bearable; governs the item's fate on death/petrification; stone/corpse gates on move/drop | SC-7.3-13/14 |

### 3.8 Scoring (M6)

| # | Gap | Ref |
|---|---|---|
| D54 | Curse penalty **−30 × NC** | Flat **−30** if any curse; **zeroed entirely once the Sorcerer is slain** | SC-12-9/10 |
| D55 | No `bonusScore` | Banked Chest loot added to the total | SC-12-8 |
| D56 | Breakdown display coarse | Per-member itemisation incl. non-counting members listed at 0 (feeds the score screen) | SC-12-6/15 |

### 3.9 Testing & UI

- **No automated tests.** The reference ships 8 machine-checkable vectors (7–61 moves;
  shortest `solo-seed23-party4-6.txt` exercises setup/movement/draw/pickup/Ruby statue) and a
  divergence-triage table (PORTING-GUIDE §4). `tools/vmsdrive/render_screen.py` already
  reconstructs the 24×80 SMG screen from the session log — so both engine-conformance and
  UI-screenshot testing are buildable today. (PLAN.md's "can't capture SMG output" note
  predates `render_screen.py`.)
- **UI**: single full-interior SMG display painted screen-at-a-time (the planned multi-panel
  layout in `STATE.MAR:241-247` was never built). The stated weaknesses — poor feedback about
  state/outcome, clutter, readability — plus the new mechanics above (battle-plan builder,
  casualty choice, artifact menu, borne toggle, chest, per-member score breakdown) make the UI a
  first-class work stream, handled by the playability loop in loop-spec.md §7. Note keys `I`
  (inventory) and `A` (artifact) were designed (June spec §13.4) but never wired.

## 4. Sequencing consequence

Data fixes (D1–D6) are cheap but **invalidate all current play balance**, and the combat rewrite
(D27–D37) invalidates most of FIGHT.MAR — so there is no value in patching mechanics before the
conformance harness exists. Hence the loop runs: harness → data/RNG → setup → movement →
chambers/encounters → fights → specials/artifacts/scoring → Part-I audit → UI rewire → UI
playability. That ordering, its gates, and the autonomous iteration protocol are specified in
[loop-spec.md](loop-spec.md); the live work ledger is [loop/LEDGER.md](loop/LEDGER.md).
