# SCAVE Refresh — Loop-Based Agentic Specification

> Written 2026-07-11. Executes the findings of [gap-analysis.md](gap-analysis.md).
> Live state lives in [loop/LEDGER.md](loop/LEDGER.md) — **the ledger is the loop's memory**;
> every iteration starts by reading it and ends by updating it, so any fresh session (or a
> `/loop` firing) can pick up exactly where the last one stopped, without human intervention.

## 1. Mission & definition of done

Bring the VAX MACRO-32 Sorcerer's Cave (`src/macro32/sorcerer/`, `SCAVE.EXE`) to **solo feature
parity** with the reference engine at `/Users/msw/code/retro/sorcerers-cave/packages/engine`.

**Done means all four of:**

1. **Vector parity** — every line of all eight conformance vectors in
   `/Users/msw/code/retro/sorcerers-cave/docs/specs/conformance/solo-*.txt` matches, including
   the `FINAL`/`STATE`/`PARTY`/`AREA` blocks (PORTING-GUIDE §1 "definition of done").
2. **Part I audit** — every solo `SC-*` row of `engine-spec.md` Part I is marked *conformant*
   (or *n/a-multiplayer*, or a logged *reference-discrepancy*) in the ledger's audit checklist.
   Vectors are smoke tests; Part I is the contract (PORTING-GUIDE M7).
3. **UI rewire** — `SCAVE.EXE` drives the engine exclusively through the action/event boundary;
   no game fact is computed in UI code; the vectors still pass after the rewire.
4. **UI playability pass** — every scenario in §7 passes its rubric on captured emulator
   screens, with zero open UI findings, and one full seeded game has been played end-to-end
   through the real UI by the agent.

Out of scope: multiplayer (§MP), trading/unions/zombies, replay-by-code, save/load, sound.

## 2. Ground rules (apply to every iteration)

- **The reference engine wins.** If both readings of the rulebook are defensible, match the
  engine (PORTING-GUIDE §6). If the *reference* looks wrong, log it under
  `Reference discrepancies` in the ledger and move on — never diverge silently, **never
  hand-edit a vector**.
- **Invoke the `vax-macro-32` skill** before touching any `.MAR` — and grep the reference
  manuals rather than guessing opcodes, condition codes, or RTL/system-service signatures.
- **`.MAR` files are 7-bit ASCII only.** Including comments.
- **Keep `SC-*` ids in code comments** at the site that implements each rule — they make
  divergences discussable across the two codebases (PORTING-GUIDE §2).
- **Evidence before claims.** A gate is "passed" only on fresh command output captured in the
  ledger entry. Never report a diff as clean without running it.
- **Commit per green step**: `git commit` with message prefix `SCAVE:` after each iteration
  that ends with the build green and no previously-passing gate regressed. Do not push.
- **One writer.** The VAX daemon serialises everything; never run parallel agents that both
  drive `vmsdrive` or both edit `src/macro32/sorcerer/`.
- **Session hygiene**: `make vms-status || make vms-up` at start; `make vms-down` when the
  session ends. Credentials come from `.env` (never echo them).

## 3. Target architecture (the strangler-fig split)

New layering inside `src/macro32/sorcerer/` (names ≤ 9 chars, never DCL keywords, always
explicit `.MAR`/`.OBJ` extensions in DCL):

```
                +--------------------+       +---------------------+
   SCAVE.EXE =  |  UI layer          |       |  SCCONF.EXE =       |
                |  MAIN,SETUP(UI),   |       |  SCCONF.MAR         |
                |  VIEW,UI,HELP,     |       |  (vector replayer)  |
                +---------+----------+       +----------+----------+
                          | actions in / events out     |
                +---------v------------------------------v---------+
                |  ENGINE (pure, headless, deterministic)          |
                |  ENGINE.MAR (ENG_NEWGAME / ENG_APPLY / EVENTQ)   |
                |  + rules code migrated from MAP/CHAMBER/         |
                |    STRANGER/FIGHT/SPECIAL/SCORE                  |
                |  DATA.MAR  STATE.MAR  RNG.MAR                    |
                +---------------------------------------------------+
```

- **`ENG_NEWGAME(seed, picks)`** — validates picks (SC-5-1..4), builds decks in the normative
  RNG order (SC-5-12), draws the party from the small pack (SC-5-5), places the Gateway.
- **`ENG_APPLY(action, a1, a2, a3)`** — the single reducer (SC-4-1): dispatch on the 17-action
  catalog (SC-4-41), guard by phase, mutate in place, append integer event codes (+ args) to an
  **event queue** the caller drains (SC-4-42 order matters). A blocked/rejected action must
  change nothing (SC-4-6, SC-4-24). `resolveRound` takes a battle plan marshalled into a fixed
  STATE buffer by the caller (UI builder or SCCONF parser).
- **Shared state stays in `STATE.MAR`** (grow arrays per gap D25/D26: no 20-slot treasure cap,
  no 12-member cap — size for 60 members / open-ended treasure lists, and keep array
  insert/remove positions identical to the engine's, because vector indices refer to array
  order at action time).
- **`SCCONF.MAR`** — RMS-reads `CONFVEC.TXT`, parses SEED/PICKS/action grammar
  (`conformance/README.md`), calls the engine, `FAO`-formats one checkpoint line per action in
  the exact vector format, writes `CONFRES.TXT`. Exact-format output is what makes host-side
  `diff` pinpoint the first divergent line (PORTING-GUIDE §4).
- **Seed injection for the UI build**: `SCAVE.EXE` checks logical name `SCAVE_SEED` (via
  `$TRNLNM`; grep the skill references for the item-list form) before falling back to
  `$GETTIM` — this is what makes §7's scripted UI sessions reproducible.
- `MAKE.COM` + `sources.list` gain the new modules and the second link target; keep them in
  sync, and add a host-side make target:

```
make vms-scave-conform VEC=solo-seed23-party4-6
  = push vector as CONFVEC.TXT -> RUN SCCONF -> fetch CONFRES.TXT
    -> diff against the reference vector -> print PASS or the first divergent line
make vms-scave-conform-all       # all eight, shortest first, stop at first failure
```

## 4. Gates

Each gate has an entry state, an exit test, and the spec sections to read. **Never work past a
failing earlier gate** (vectors compound; PORTING-GUIDE §4).

| Gate | Work | Exit test |
|---|---|---|
| **G0 Harness** | Engine boundary skeleton + `SCCONF` + make targets (§3). Read Appendix D + `conformance/README.md` BEFORE any game logic | `make vms-scave-conform VEC=solo-seed23-party4-6` runs end-to-end and produces a well-formed `SETUP` line (content may still be wrong); `SCAVE.EXE` still builds |
| **G1 RNG + data** | Gaps D1–D6: 71-card pack, card 41→42, reaction cells, seed injection. Add a `SCCONF` self-check mode printing `nextSeed(1)`, deck sizes, and the A.1 cells | Self-check prints `1103527590`, 60/71, 14 creatures/15 treasures/5 hazards, corrected cells (SC-5-6, SC-3 counts) |
| **G2 Setup** | newGame: shuffle + consumption order, party-from-pack, Gateway init (SC-3-23/24, SC-5-*) | `SETUP` line of **all eight** vectors matches (proves shuffle + order alone) |
| **G3 Movement** | §6: D7–D12 (secret doors, rubble, exhaustion, turn coupling, L1 exits) | Every vector matches up to its first non-move action |
| **G4 Chambers/encounters** | §7–§8: D13–D26 (hazard rewrites, natural-1, withdraw/surprise/pacified/unicorn/hostile-areas, passage pickup, caps removed) | Vectors match through all non-fight actions; fights are the only remaining divergences |
| **G5 Fights** | §9: D27–D37 (battle plans + validation, casualty queue, heavy drop, retreat rules, sweepFallen, Sorcerer). The subtle part is `SC-9.1-*` validation | All fight actions (`FIGHT`, `CASUALTY`, `RETREAT`) replay correctly in every vector |
| **G6 Specials/artifacts/scoring** | §10–§12: D38–D56 (viper 1-2, pool model, all `USE`/`OPENCHEST`/`BORNE`, flat −30, bonusScore) | **All eight vectors match end-to-end including FINAL blocks** |
| **G7 Part I audit** | Walk every solo SC- row against the code; strip legacy rulebook behaviour the vectors didn't exercise (e.g. Dwarf one-trap memory, pool doorway drops). Also confirm engine purity edges: failed-action-no-mutation spot-checks | Audit checklist in the ledger 100% marked, each with file:line evidence |
| **G8 UI rewire** | SCAVE UI → actions/events only; new interactions get UI: battle-plan builder, casualty choice, artifact menu (`A`), inventory/borne (`I`), chest, retake-dropped, score breakdown | Vectors all still pass; a scripted seeded game is playable start→gameOver through the real UI |
| **G9 UI playability** | §7 loop until the rubric passes everywhere | All scenarios pass; zero open UI findings; full-game playthrough recorded |

## 5. The iteration protocol

One iteration = one bounded, verifiable step. Target ≤ ~90 minutes of work; smaller is better.

1. **Orient.** Read `loop/LEDGER.md`. Note current gate, per-vector first-divergence, open
   defects. `make vms-status || make vms-up`.
2. **Select.** The highest-priority item = earliest failing gate; within a gate, the shortest
   failing vector's **first divergent line** (fix causes, not symptoms; one divergence often
   clears many lines). Consult the triage table (§6) to map the field to a spec section.
3. **Study.** Read the exact `SC-*` rows (and Part II narrative section) for the item. For
   MACRO-32 constructs, grep the skill's reference manuals. Transcribe data, don't re-derive
   (PORTING-GUIDE §2).
4. **Implement** the smallest change that could clear the divergence. ASCII only; `SC-*` ids in
   comments; respect the no-mutation-on-reject discipline.
5. **Build.** `make vms-scave-build`. Fix assembler/linker errors immediately (§8 gotchas).
   A failed MACRO stops MAKE.COM before LINK — read the captured DCL output, and the fetched
   `.lis` listing when the error is positional.
6. **Verify.** Run the exit test of the current gate — at minimum
   `make vms-scave-conform VEC=<shortest failing>`; on a pass, `vms-scave-conform-all`. For
   G8/G9, run the relevant §7 scenario and render screens. Debug divergences with
   `make vms-scave-debug` (on `SCCONF`) + `vmsdrive dbg 'EXAMINE …'` over the STATE arrays —
   the `SEED` field names the exact action where roll count/order went wrong.
7. **Record.** Update the ledger: iteration log entry (id, item, change summary, command
   evidence, result), refreshed vector table, defect/UI-finding updates, gate flips.
8. **Commit** (`SCAVE: …`) if build green + no gate regressed. Then `make vms-scave-clean`
   every few iterations to stop VMS version-number creep.
9. **Continue or yield.** If inside a session with budget left, loop to step 2. Otherwise
   ensure the ledger is consistent, `make vms-down`, and (in `/loop` mode) schedule the next
   firing. **Stop the loop entirely** only when §1's four conditions are all met (mark ledger
   status `DONE`) or a `BLOCKED-ALL` state is reached (every remaining item blocked — see §8).

## 6. Divergence triage (from PORTING-GUIDE §4)

| First mismatching field | Look at |
|---|---|
| `SEED` on the `SETUP` line | LCG arithmetic, shuffle, or deck-build order (A.5, SC-5-9..12) |
| `SEED` on a move line | a roll happened that shouldn't / didn't / out of order inside that action — the spec row for that action pins the sequence |
| `ARA`/`LVL`/`TRN` | movement/placement (§6) |
| `PH`/`GS` | phase-machine transitions (§4) |
| `EV` list | event emission order (SC-4-42 + per-mechanic rows) |
| `FINAL`/`PARTY`/`AREA` block only | bookkeeping no checkpoint surfaces — usually treasure/contents handling (§7) |

Vector order (shortest first): `solo-seed23-party4-6` (7), `solo-seed777-party5-6` (7),
`solo-seed101-party1-7` (8), `solo-seed11-party5-6-7` (15), `solo-seed19-party2-7` (18),
`solo-seed7-party1-7` (19), `solo-seed42-party3` (31), `solo-seed3-party0` (61).
If targeted extra vectors would help (deeper levels, a Sorcerer kill, an escape with loot),
log the request in the ledger for the human — the reference side can mint them cheaply
(PORTING-GUIDE §6) — but never block on it.

## 7. The UI playability loop (G9, and the standing bar for G8)

The user's stated top weakness: *the player is not told clearly what happened or what state
they are in, and screens get cluttered/unreadable.* UI work is therefore verified the same way
engine work is — by captured evidence, judged against a rubric.

**Driver.** All scenarios run with a fixed seed (`DEFINE SCAVE_SEED <n>` before `RUN`), driven
keystroke-by-keystroke:

```
tools/vmsdrive/vmsdrive.py raw '<key>' --expect '<text unique to the next screen>'
python3 tools/vmsdrive/render_screen.py > claude/sorcerers-cave/2026-07-11-refresh/loop/screens/<scenario>/<step>-<name>.txt
```

`render_screen.py` reconstructs the 24×80 screen after the last `RUN … SCAVE` in the daemon
log. Choose `--expect` strings printed by the *new* screen, never echoes of the key. Save every
render; the `screens/` tree is the UI regression record (diff renders between iterations).

**Scenario suite** (each a scripted key sequence; seeds chosen once, recorded in the ledger):

| # | Scenario | Must show |
|---|---|---|
| S1 | Title → party pick → Gateway | budget/stock arithmetic live; picked party echoed before confirm |
| S2 | Moves incl. a dead end + a face-down placement | outcome of EVERY move stated (moved where / dead end WHY); turn counter visible |
| S3 | Chamber draw + treasure pickup + leave/drop | drawn contents itemised; carry capacity vs load visible per member; leave/drop consequences stated |
| S4 | Encounter: Withdraw / Attack / Test ×3 → pacified | reaction roll + modifiers SHOWN (die, charisma, curses, result); indifferent-streak progress; withdraw-blocked reasons |
| S5 | Multi-round fight: plan build → rejection → rounds → casualty choice → win | plan builder legible; rejection REASON in words; per-match dice/strength totals; casualty die outcome; loot sweep report |
| S6 | Hazards (Medusa, Ghouls, trap fall chain, quake) | each hazard: what fired, who was affected, what dropped/spilled, where the party now is |
| S7 | Artifact menu: potion in fight, balm, staff, chest, borne toggle | eligible bearers/targets only; consumption feedback; Eye curse warnings |
| S8 | Map browser + help browser round-trip | re-entry returns to an unchanged, uncorrupted turn screen |
| S9 | Endings: escape / wipe / quit | score breakdown itemised per member + bonuses/penalties, matching SC-12-15 |

**Rubric — every captured screen must satisfy:**

1. **State** — current phase, location/level, turn, and the legal actions are visible without
   memory of prior screens.
2. **Outcome** — the immediately-preceding action's result is explicitly reported (what
   happened AND why), not inferable-only.
3. **Legibility** — no overlapping/stale text, aligned columns, related info grouped, ≤80 cols
   honoured, no unexplained abbreviations.
4. **Dice transparency** — every roll that affects the player is shown with its modifiers.
5. **Consistency** — same key = same meaning everywhere; a persistent key legend.
6. **No dead ends** — every prompt lists a way out (cancel/back) where the rules allow one.

Each rubric failure becomes a ledger UI finding (screen file, rubric #, description). Fix →
re-run the scenario → attach the new render. The gate closes when all scenarios pass and a
full game (seeded, agent-driven, title to score screen) completes without a rubric violation.

## 8. Failure handling & anti-stall

- **3-strike rule**: an item still unresolved after 3 iterations of distinct hypotheses →
  mark `BLOCKED` in the ledger with the evidence trail (divergent line, debugger examines,
  hypotheses tried), pick the next item. Revisit blocked items when their gate is otherwise
  clean.
- **Suspected reference bug**: record under `Reference discrepancies` (vector, line, why the
  engine looks wrong) and continue with other items. The port does NOT change behaviour to
  disagree with the vectors, and vectors are never edited.
- **Daemon flakiness** (lost prompt, stale socket): `make vms-down && make vms-up`, retry once;
  still failing → ledger note + stop the session cleanly (the next firing retries).
- **Build regressions**: if a change breaks previously-passing vectors, revert it (`git
  checkout -- <file>` or revert commit) before iterating further — never leave the tree red
  between iterations.
- **BLOCKED-ALL**: every remaining work item blocked → set ledger status `NEEDS-HUMAN` with a
  one-paragraph summary per blocker, and stop the loop.

## 9. VMS / MACRO-32 gotchas (hard-won; violating these wastes iterations)

- System services: use the `$XXX_S` macros (`$QIOW_S`, `$TRNLNM_S`, …) — hand-rolled `CALLS`
  to `SYS$…` returns `SS$_INSFARG`.
- `LINK/DEBUG` images auto-launch the debugger under `RUN`; always `RUN/NODEBUG` for plain
  runs (the make targets already do).
- No `/NOOPTIMIZE` on MACRO — that's a compiler qualifier; `MACRO/DEBUG/LIST` is right.
- Always explicit `.MAR`/`.OBJ` extensions in DCL; avoid bare-keyword filenames (`DATA` alone
  fails silently).
- `=` constants are file-local; cross-module constants must live in an included header or be
  duplicated — a missing one links as **0 silently** (NUDFSYM). SCAVE shares symbols via
  `STATE.MAR` globals (`::`) — keep new shared constants there.
- Conditional branches are byte-range (±127): far targets need invert+`BRW` or inlining.
- RMS control blocks (`$FAB`/`$RAB`) must be `.ALIGN LONG`.
- `tools/gen_help.py` regenerates `SCAVEHLP.TXT` from `help/*.md` on every build — help-text
  edits go in `help/`, not the `.TXT`.

## 10. Launching the loop

The loop is designed for **self-paced `/loop` execution** in this repo:

```
/loop Execute one iteration of claude/sorcerers-cave/2026-07-11-refresh/loop-spec.md:
read loop/LEDGER.md, run the iteration protocol (spec section 5) once or more as budget
allows, update the ledger, commit green work. Stop the loop when the ledger status is
DONE or NEEDS-HUMAN.
```

Each firing is stateless-safe: the ledger + git history carry everything forward. A plain
interactive session can run the same protocol by hand ("do the next loop iteration"), and a
scheduled cloud agent is NOT suitable here — iterations need the LAN-attached VAX (`orac`,
reachable only from this machine).

Rough expected shape (not a commitment): G0–G2 a handful of iterations; G3–G4 the long
vector-grind; G5 the single biggest rewrite; G6 wide but shallow; G7 one careful sweep;
G8–G9 as many iterations as the rubric demands.
