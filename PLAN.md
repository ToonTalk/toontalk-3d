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

### Stage 3 — pads, generalized (2–3 days) — **done 25 Aug**

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

*Met.* All of it, and two example folders that stand as the acceptance test:
`examples/sounds/` (tones, transforms, melody) and `examples/images/`
(pictures, naming, album). `melody` and `naming` joined the gate, which is
now **13 worlds** — the first two that assert on media. `naming` is the
one worth reading: six robots dispatch on the PICTURE in their thought,
which needed no new machinery, only the fact that a picture is a pad.

Two conventions arrived with them. **Space turns a thing on and "." stops
it** — the thing in your hand, or the one under the pointer — which is
ToonTalk's own, and which replaced "picking a sound up plays it" (Ken:
startling). And a notebook's **spine** is a grip of its own: it picks up
the book rather than what is on its pages, and it is the one hold Dusty
accepts on a notebook that still has entries in it.

### Stage 4 — the Devices notebook (half a day to a day) — **done 25 Aug**

Event nests for mouse and keyboard, copied out of a Devices notebook;
read-only by construction (a nest to copy, no bird to be had). Placed
before behaviours because move-with-arrows and move-with-mouse read it.

*Acceptance:* a robot dozing on a keyboard nest wakes per keypress; a
mouse-position gauge; suite green.

*Met.* `examples/devices/keys` -- the Scribe joins each key onto a pad and
reads "Hello Ken!" after ten dispatched key events -- and
`examples/devices/pointer`, whose two numbers tracked three pointer positions
in table coordinates. Suite green at 13.

Two things fell out that were not in the plan. The nests are read-only
**by construction**: each arrives with no egg, and a bird is the only way
anything is ever put on a nest, so there is no rule to enforce. And a device
nest had to be exempted from the notebook's "a lone eggless nest comes out
fresh" rule, which was replacing it with a new nest and costing it the guid
that makes it a device at all.

### Stage 5 — behaviours: anima-gadgets (2–3 days) — **DONE 28 Aug: the shelf is twelve**

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

*Met, with the library short.* A star + the `bouncing` gadget dropped on it +
SPACE ran to 1.24, turned, ran to −1.17 and turned again, with no training
anywhere. Self-demonstration falls out of the binding rather than being built:
an unbound gadget's bird points at the gadget. Suite green at 13.

**All twelve** are on the shelf (28 Aug). The first six: moving right, moving
left, bouncing, wrapping at the edges, following the pointer, moving with the
arrow keys. The second six — grow when touched, shrink when touched, make a
sound on hit, reverse on collision, a speed limit, send 1 to the score when
hit — wanted two message-surface additions, both built the day the gadgets
were: a sayable SIZE ([set|move|query|listen | size | n], the number the held
card's +/− buttons step) and the #speed channel ([set | speed | ...] now
announces, with the numbers' echo rule). Two idioms carried the six:
**dozing on touch** (the touch nest starts empty, the team dozes until an
announcement, eats it, and acts once per change of contact — so grow grows
once per touch and an untouched gadget costs nothing) and **the scale is the
if** (the speed limit weighs the across-speed against the limit on an
ordinary scale and dispatches on the lean). The bell and the score ride in
their gadgets' work boxes — a live thing in a hole still gets its mail.
`reverse on collision` handles THINGS and leaves edges to `bouncing`;
binding both to one star is pong-ball physics with no training anywhere,
which is the composition the shelf exists to teach.

Two things came out differently from the plan. The binding is **one
direction** so far — a behaviour dropped on a thing — rather than the
two-way panel-on-panel gesture; the second direction is a placement question,
and the binding underneath it is the same call. And the EDGE had to be a
*reading* rather than an event, because a team member facing an empty nest
dozes and a dozing member stops the team — so an edge event would have
stopped the very robot doing the moving. Readings are never empty.

### Stage 6 — inexact numbers — **DONE 28 Aug**

Per BACKS.md: exactness flag, contagion, fixed-precision trig and powers,
the visual marker. Last because nothing above requires it — it unlocks the
*move in an ellipse* behaviour, which ships as its thirteenth-behaviour
proof.

*Acceptance:* `sin` of an exact number is inexact and marked; ellipse
movement runs; determinism holds across reloads; suite green.

*Met, and measured.* A number is a rational plus a flag; three operations are
inexact by nature — `sin`, `cos` and `root`, typed onto a held number the way
`mod` always was. Angles are DEGREES. Answers are kept to twelve decimal
places and the kernel works to thirty.

Nothing calls JS `Math`: `Math.sin` is implementation-approximated by the
spec, so two browsers may differ in the last bits and a saved world would
replay differently on another machine. Instead, argument reduction and a
Taylor series over rationals for sine, Newton's method over BigInts for
roots — deterministic BY CONSTRUCTION, which is what makes replay and
headless verification mean anything. Measured: sin 30 is exactly 1/2 and
marked; sin 45 is ~0.707106781187; the square root of 2 is ~1.414213562373;
**the square root of 4 is 2, exact** — a root that comes out whole is not an
approximation, and saying "approximately two" about it would be a lie.
Contagion holds, a world with approximations in it saves and reloads
byte-identical, and `examples/behaviours/ellipse.world.json` traces an
ellipse 2.2 across by 0.8 deep with every point on the curve.

Suite check twenty-one covers all of it; with contagion disabled it goes red.

### Capstone — Pong — **DONE 2026-08-26**, with one divergence

`examples/behaviours/pong.world.json`. The **table is the court**: three of its
walls are the table's own edges, the fourth is yours. The ball, the bat and the
counter are three ordinary things on the table; the ball and the bat each carry
their own program on their own panel, so two programs run at once — which is
what makes it a game rather than a demonstration.

*The divergence:* the plan said "built only from pads, sub-pads and **library**
behaviours — no bespoke robots". Pong's ball wants a team that dispatches on
two readings at once and counts a miss, and its bat wants to follow one axis
and not the other. Neither is on the shelf, and the four library gadgets that
would have covered them are among the six of twelve still unbuilt (`send a
message to the score` is literally one of them). So the ball and the bat carry
**bespoke robots on ordinary panels** instead.

What the clause was protecting is intact and is the thing worth claiming: no
engine work was done for Pong. Every part of it existed for another reason —
`[move | across | n]` and the `edge` reading from Stage 5, the `touch` reading,
the pointer device from Stage 4, a badged number given to a bird from Stage 2,
and `[set | width | n]` from Stage 3, which is the whole of why the bat is a
bat and the ball is a ball. Nothing anywhere knows the game is Pong. Building
the missing library gadgets and then rebuilding Pong out of them is a real
follow-up, and a good one. **Done 28 Aug:**
`examples/behaviours/pong-gadgets.world.json` — a ball that is a pad with
three shelf gadgets bound to it (bouncing, now both axes; reverse on
collision; send 1 to the score), a bat with one (following the pointer), and
not a single robot written for the occasion. Measured playing: the ball roams
3.2 × 1.1 bouncing on both axes, the rally climbs under a perfect
pointer-player and slows when the bat is parked. The honest seams are on a
card IN the world: two bound movers ADD their steps, and the counter scores
hits where classic Pong scores misses — a miss-counter would be an
edge-listening shelf gadget nobody has asked for yet.

Three things had to be fixed to make it run, all of them general and all of
them measured — see BACKS.md: the `touch` reading, auto-run inside a room, and
what the `edge` reading means when a thing is resting against a wall.

### Capstone II — Pong the original's way — **DONE 2026-08-26**

`examples/behaviours/pong-classic.world.json`, after Ken sent `pong.tt` out of
ToonTalk 3 and asked for one like it. Three capabilities came out of reading
that file, and none of them is about Pong (BACKS.md has the detail):

- **a pad can be a FIELD** — a thing riding on a pad has a place of its own,
  in that pad's own steps, and *the edge* means the edge of whatever it is
  standing on;
- **a thing can have a SPEED** — `[set | speed | [across | away]]`, moving on
  the world's clock, with an empty hole meaning "leave that one alone";
- **the touching reading says WHICH SIDE**, which is the original's pair of
  per-axis collide sensors under another name.

This one comes much closer to the plan's original clause than the first did:
its ball and bat are pads and sub-pads on a field, and the robots on their
panels send nothing but messages the workshop already had. What is still true
of both is that the library gadgets they would have been assembled from are
among the six of twelve unbuilt.

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
