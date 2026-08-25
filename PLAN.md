# The panels epic — build plan

**Status: plan, approved approach; building not yet started.** BACKS.md is
the design — *what* and *why*. This file is *how* and *in what order*.
DIVERGENCE.md stays the audit of the original. (Ken Kahn and Claude,
24 August 2026.)

## How the work is protected

Approved 24 August: **snapshot the release, develop in the canonical file.**

- `toontalk-3d-v1.html` is a byte-for-byte copy of the released app, taken
  the day this plan landed. `index.html` points at the snapshot, so the
  GitHub Pages root serves the stable app for the whole epic. The snapshot
  is never edited.
- Anyone who wants the work in progress uses `toontalk-3d.html` directly —
  the canonical file, the only one that is ever developed.
- **Refresh policy:** until Stage 1 starts, any bug-fix commit re-copies
  the snapshot, so released users get fixes. Once Stage 1 starts the
  snapshot freezes; only a fix Ken judges critical is ported into it by
  hand.
- When the epic settles and Ken has tested, `index.html` returns to the
  canonical file and the snapshot is kept as `-v1` for the record.

## Ground rules, every commit

1. **The regression gate.** The nine-world suite (n-to-1, reverse, append,
   factorial, swap, infinity 1/2/4/6) must produce byte-identical dumps
   against the goldens before any commit lands. Stage 0 turns the
   session-bound harness into a repo file so the gate survives sessions.
   Each stage *adds* goldens; none are ever loosened. When behaviour must
   legitimately change, the commit message says which golden changed and
   why — the same discipline the nest-window fix already followed.
2. **Old worlds untouched.** Every capability in this epic is additive. A
   `v: 3` world must load and run identically until the epic's end.
   `FILE_V` goes to **4** at the first commit that saves panel data (the
   design doc's "v3" predates the pad-training bump), and `fileTooNew`
   already makes older builds refuse newer files politely.
3. **Syntax check** (`node --check` on the module) before every commit —
   already habitual; stated so it stays so.
4. **Artifact builds** (`build_artifact.py`, `build_chat_artifact.py`)
   rebuilt at stage ends, not every commit.
5. **The ledger and making-of** catch up at stage ends.
6. **Ken tests at checkpoints.** Every stage ends in something exercisable
   at the table, listed under *Acceptance* below. Nothing in a stage
   depends on a later stage.

## Stages

Order differs from BACKS.md in one place: the **Devices notebook comes
before behaviours**, because the most iconic behaviours (move with arrows,
move with the mouse) read device nests and cannot be built without them.

### Stage 0 — scaffolding (~half a day)

- Snapshot taken; `index.html` re-pointed; README names both URLs.
  *(Done with the commit that added this file. Stage 1 done 24 Aug.)*
- The regression harness becomes a repo file: `tests/` with a runner that
  loads each example world headless, runs it at Instant with fixed
  rounds, dumps, and diffs against `tests/golden/*.json` — plus a
  make-goldens mode. This is the session harness, formalized.
- **Decisions needed from Ken before Stage 1 — both made, 24 August:**
  the release gesture is the **holding-card button plus a key**, and the
  name is **panel**. Stage 1 is unblocked.

### Stage 1 — panels as places (1–2 days)

Every thing gains a panel: released by the chosen gesture while holding,
staged as a tray that can be set down and worked at, snapped back inside
on close. Glued semantics: copying the thing copies the panel, vacuuming
takes it too. Implementation reuses the room machinery (a panel is a
mounted world context without walls); persistence bumps `FILE_V` to 4.

*Acceptance:* open a number's panel; lay a robot and a box on it; the
robot runs there; close it; save and reload round-trips; a v3 world still
loads; suite green.

### Stage 2 — birds, live numbers, suspension (2–2.5 days) — **done 25 Aug**

*(Built with one design revision, recorded in BACKS.md: event nests are
obtained by `[listen | reply-bird]` rather than furnished on the tray.
Every acceptance item below ran; the gauge and the live account joined
the suite as goldens ten and eleven.)*

Opening a panel yields a **bird addressed to the thing**. Messages are
boxes with a selector pad; the panel handles one at a time. Event nests
announce changes; echo suppression per BACKS.md; and the suspension rule
generalizes — a robot whose match fails on a live thing dozes on that
thing's events, reusing `waiters` and `mismatchPaths`.

This is the smallest code and the deepest semantics in the epic —
test-heavy, and the **bank-account example rebuilt on panels is the
canary**: it already does request/reply with reply birds, so it must come
out cleaner, not different.

The **info notebook** ships here too (+ about half a day): every panel
gets an ℹ️ button opening a notebook of live example boxes — copy one
out, edit it, send it. Built-in kinds' notebooks are authored; user
panels get an empty one the author fills by the ordinary filing gesture.

*Acceptance:* a gauge built as an idiom (sync robot + controller); a
badged `+10` delivered as fetch-and-add; two robots hammering the same
live number cannot interleave a read-modify-write; an echo test showing a
sync robot's own write does not wake itself; an example box copied from a
number's info notebook, edited and delivered; suite green.

### Stage 3 — pads, generalized (2–3 days)

- **The rename**, first and as its own commit: "text pad" becomes **pad**
  in every string, the manual, tooltips and Marty's briefing — grep-audited.
- **Images**: the three doors (panel import button; panel receives drops;
  paste-while-holding covers the pad). Verbs: position, width, height.
- **Sub-pads**: pads hold pads, coordinates relative to the container.
- **Sounds**: files; made sounds (the `[frequency, duration, shape]`
  mint); remade sounds (badges — `×2` speed, `×(−1)` reverse — and
  edge-drop concatenation). Parameterized transforms as panel messages.
- Video only if it falls out of images trivially; otherwise deferred.

*Acceptance:* a photograph lies on the table, files in the notebook, sits
in a box; a butterfly sub-pad rides its field pad; a made sound plays and
two sounds concatenate by edge-drop; suite green plus new goldens.

### Stage 4 — the Devices notebook (half a day to a day)

Event nests for mouse and keyboard, copied out of a Devices notebook;
read-only by construction (a nest to copy, no bird to be had). Placed
before behaviours because move-with-arrows and move-with-mouse read it.

*Acceptance:* a robot dozing on a keyboard nest wakes per keypress; a
mouse-position gauge; suite green.

### Stage 5 — behaviours: anima-gadgets (2–3 days)

The binding rule (both directions unless Stage 1 experience says one is
enough): panel-on-panel re-points the inner robots at the outer panel's
object; object-on-a-control adopts the behaviour and re-assigns its
controlled object. Unattached behaviours control themselves — that is the
self-demonstration, free. Speaking labels ride the existing hint voice.

The **starter library — twelve, capped** (scope control; the catalogue in
BACKS.md is the long-term target): move with arrows · move with mouse ·
start moving right · bounce off edges · wrap at edges · reverse on
collision · speed limit · grow when touched · shrink when touched ·
make a sound on hit · I destroy what touches me · send a message to the
score when hit.

*Acceptance:* butterfly + move-with-mouse + bounce-off-edges is a playable
toy, assembled with no training; each library behaviour demonstrates
itself when set down alone; suite green.

### Stage 6 — inexact numbers (1–2 days)

Per BACKS.md: exactness flag, contagion, fixed-precision trig and powers,
the visual marker. Last because nothing above requires it — it unlocks the
*move in an ellipse* behaviour, which ships as its thirteenth-behaviour
proof.

*Acceptance:* `sin` of an exact number is inexact and marked; ellipse
movement runs; determinism holds across reloads; suite green.

### Capstone — Pong

`examples/pong.world.json`: built **only** from pads, sub-pads and library
behaviours — no bespoke robots. It is the epic's acceptance test, the
making-of's payoff, and the first candidate for the export-to-web wish.

## Decisions Ken owns, and when they bite

| Decision | Blocks | Recommendation on file |
|---|---|---|
| Release gesture | Stage 1 | **decided:** holding-card button + a key |
| The name | Stage 1 strings | **decided:** panel |
| Binding rule: both directions? | Stage 5 | start with both, drop one if confusing |
| Positional audio | Stage 3 | yes — from the thing |
| Where made sounds are minted | Stage 3 | — |
| `×(−1)` reverses a sound? | Stage 3 | try it, keep if it delights |
| What Bounce bounces off | Stage 5 | edges of its pad, not furniture |
| Keyboard focus | Stage 4 | — |
| Precision constant | Stage 6 | — |
| The look of inexact numbers | Stage 6 | — |

## Who builds it

Recorded 24 August, decided by task shape (and revisable per stage at any
`/model` switch — stage boundaries make the change free):

- **Stages 1, 2 and 6 — the strongest model, high effort.** Stage 1
  touches the world-context machinery that produced the tiny-robot and
  delivery-ordering bugs; Stage 2 is the deepest semantics in the epic;
  Stage 6 promises determinism. These are the stages where mistakes are
  architectural. (As of this writing that means Opus at high effort;
  Fable's positioning is not yet established — if Ken's experience says
  it is at that level, it can take these stages instead.)
- **Stages 3, 4 and 5 — a fast model, medium effort.** Additive,
  well-specified work with acceptance criteria already written; Stage 5's
  twelve behaviours are repetitive construction where iteration speed
  beats depth. Sonnet is the default; escalate any stage that fights
  back.
- The **regression gate is the model-insurance**: byte-identical dumps
  before every commit catch a weaker model's mistakes mechanically. The
  plan and BACKS.md are written so a fresh session of any model can pick
  up a stage cold — the acceptance criteria are the contract, not the
  conversation.

## Risks

- **Suspension touches the scheduler.** `waiters`/`checkWaiting` grew the
  small-robot bugs; every change there lands with a targeted test plus the
  suite. The bank account is the canary.
- **Panel contexts multiply.** Every thing owning a world context would
  be heavy; panels hydrate lazily, exactly as rooms already do
  (`hydrateRoom` precedent), and an unopened panel with no behaviour
  costs nothing.
- **Echo suppression correctness** depends on decidable equality — which
  exact arithmetic gives and Stage 6 must preserve (fixed precision,
  no floats in values).
- **The rename is wide.** One commit, grep-audited, nothing else in it.
- **The catalogue is a scope trap.** The library is capped at twelve for
  the epic; growth afterwards is welcome and unbounded.

## Estimate

Half + 1.5 + 2 + 2.5 + 0.75 + 2.5 + 1.5 days of stages ≈ **8–12 working
days** with the usual spread — the same shape as the rooms-and-engine
epic, which this project survived twice.
