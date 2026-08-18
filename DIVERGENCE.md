# ToonTalk 3D — divergence audit

A living comparison of ToonTalk 3D against the original ToonTalk, drawn from
the manual (toontalk.com/English) and the original C++ source (tt-wasm).
Each item is marked:

- **KEEP** — deliberate divergence we consider an improvement
- **GAP** — original capability we lack and probably want
- **FIX** — misunderstanding worth correcting
- **UNDECIDED** — needs a decision
- **SAME** — noted only where the agreement is non-obvious

Update this file as decisions are made.

## Numbers

- Drop combines, target modified, dropped pad consumed — **SAME**.
- Ops: we have `+ - * / ^`. Original also has `=` (assignment), `%`
  (remainder), `& | ~` (bitwise), and **operation-only pads** (Backspace a
  number away and the bare operation remains; operations concatenate on one
  pad). — **GAP** (`=` and `%` are the useful ones; op-only pads are elegant).
- Exact rationals, huge integers, ellipsised digits — **SAME** (theirs
  inspired ours).
- Five faces showing English / scientific / decimal forms with repetend bars —
  **KEEP** (ours only).
- Erased number = "any number" wildcard — **SAME** (via Ruby).
- Cursor editing with arrow keys; we are append/Backspace only — **GAP**
  (minor).

## Text pads

- Sided concatenation, number shifts first/last letter, number on blank pad
  becomes digits, blank pad matches any text — **SAME**.
- Insertion-point editing — **GAP** (minor).

## Boxes

- Join by edge-drop; digit resizes; shrink drops the excess off the right —
  **SAME** in spirit (ours splits the excess off as a box *with its
  contents*; original drops "the extra part" — **KEEP** ours, it loses
  nothing).
- **Box dropped on a number N splits into [N holes | rest]** — **GAP**, and a
  lovely array primitive (the manual pairs it with blank-box matching to
  index arbitrary holes).
- Zero-hole boxes (vanish when joined) — **GAP** (needed as the empty-array
  base case for recursive box programs).
- Conversions onto a blank box: text → one character per hole; robot team →
  one robot per hole; notebook → one page per hole (and box → blank notebook
  the other way) — **GAP** (low priority, very ToonTalk).
- Hole labels exist and matching ignores them — **SAME**.
- Blank box matches any size — **SAME** (`anyBox`).

## Birds & nests

- Hatching pairs, delivery under the pile (top = oldest), copied bird → same
  nest, copied nest → multicast — **SAME** (ours implements the flock as a
  shared guid; the C++ confirms the original also keyed nests by GUID).
- Original birds accept only "rectangular" items (pads, boxes, pictures);
  ours carry anything, rooms included — **KEEP**.
- **Nest merging**: drop nest on nest, deliveries redirect to the survivor —
  **GAP** (cheap with guids: merging = adopting the other guid).
- Save a bird alone → she gets a new nest; save a nest alone → fresh egg —
  **SAME** in spirit (our notebook lone-copy rules).
- Robot facing a bare nest waits until covered — **SAME**; ours shows it by
  the robot shrinking and dozing — **KEEP**.

## Robots

- Positional hole addressing, re-run while matching, team pass-along, Escape/
  leave to end training — **SAME**.
- A robot in a thought bubble originally matches only a robot *with the same
  name* until erased; ours always reads "a robot" — **UNDECIDED** (named
  matching is more expressive; ours is simpler).
- "If a robot vacuums up the box he's working on the team stops for good" —
  **UNDECIDED** (we currently abort the step).
- Our extras: the bubble hands out a copy of the training object; robots
  fetch from stacks exactly as the user does; auto-run on being given a
  matching thing — **KEEP**.

## Trucks, houses, bombs  ← the recursion machinery

- Original: a truck loads **a robot (or team) + a box** (optionally a house-
  style picture, an address, and a notebook = module system); it drives to
  the nearest empty lot, builds a house, sets the robot inside with the box,
  and "He'll start working right away".
- Ours: rooms are *things* — nestable, mailable, fileable — which the
  original's houses are not. **KEEP** the rooms-as-things model.
- **GAP (critical for recursion): robots cannot obtain or populate rooms.**
  The room stack refuses robots, and there is no `newRoom` step. Everything
  else exists: dropping a robot into a room installs it; dropping a gift
  starts it. Plan: let robots take rooms and treat "robot + box into a room"
  as our truck.
- **GAP (critical): the copier refuses robots**, but the original's Magic
  Wand in 'S' mode copies a robot *and its team* — this self-copying is how
  doubly-recursive programs (Fibonacci) spawn their children. Plan: Mimi
  copies robots (botOut/botIn already round-trips them faithfully).
- Bombs: a robot can destroy the house it is in; contents are rescued only if
  Dusty is present. We have no teardown a robot can perform — finished
  recursive workers would accumulate forever. — **GAP**; our flavour needs
  deciding (a bomb thing? a self-vacuum step? parent-side cleanup of a room
  whose robot has stopped?). **UNDECIDED** on form, needed in substance.

## Magic Wand & Pumpy

- Wand copying → our copier Mimi — **KEEP** (a place, not a hand tool; robots
  use it the same way users do, which the wand couldn't offer).
- Wand 'O' mode (copy-and-restore-erased) — **GAP** (un-erase by copying).
- Pumpy (resizing things) — **GAP** (cosmetic; low priority).

## Dusty & Ruby

- Original: one Dusty with S/R/E modes. Ours: Dusty removes, Ruby erases —
  **KEEP** (the mode button needed a legend; two characters don't).
- 'R' spit-back — covered by Undo; Dusty's rescue role in explosions becomes
  relevant only with teardown — **UNDECIDED** with bombs.

## Notebook

- Filing, text/number navigation, Dusty-only removal, main-notebook
  persistence, blank first page holding a blank notebook — **SAME**.
- Robots may not touch the original's main notebook (it is shared); ours lets
  robots file — **UNDECIDED**.
- Retrieval gives a copy (manual is silent; we chose copy) — **KEEP**.

## Scales

- Original scales sit in a 3-hole box comparing their *neighbours*; ours are
  standalone with two pans — **KEEP** (documented divergence).
- Robots can match on a scale's tilt (>, <, =); ours cannot — **GAP** (this
  is the original's comparison/branching primitive; needed for real
  programs).
- Text comparison (alphabetical) — **GAP** alongside tilt matching.

## Sensors & randomness

- Original sensors are live pads in the notebook: mouse, keyboard, time,
  "my address" — **GAP** as a family (needed only when pictures/games
  arrive).
- **The random source** (needed for the sentence generator): sensor page 28,
  a live pad showing 0–999, "It tries its best to be random"; freeze a
  sample by dropping it on a zero. — **GAP**; our flavour could be a dice
  thing from a stack whose value re-rolls on each take. **Planned.**

## Architecture: how the original ran dozens of houses (from the C++)

The entire concurrency model reduces to `Sprite::default_duration`:

```cpp
if (showing_on_a_screen()) { ... return the_default_duration; }
return 0;                     // off-screen: every animation takes 0 ms
```

There is **one live world**. Houses are not separate documents — they are
places in a single city, all their robots stepped every frame from one
sprites list. Robots waiting on nests are *suspended* (`suspended_on`) and
woken by deliveries. What you are not watching still runs — its animations
simply take zero time. No serialisation, no world-swapping.

ToonTalk 3D instead *bottles* a room's world (serialise outer → load inner →
run → serialise → restore), because the engine is a singleton. That is fine
for a few rooms and collapses combinatorially for dozens (and deadlocks past
one level of nesting).

**The scaling plan** (in order):

1. *Semantics unlocks, current engine*: Mimi copies robots; robots take and
   populate rooms (`newRoom`); nested rooms' pending work runs recursively
   after each bottle; a dice thing for randomness; box-split-on-number and
   zero-hole boxes; scale-tilt matching. This makes the sentence generator
   and recursive Fibonacci *expressible*, if slow.
2. *The original's architecture*: separate the world model from the scene.
   Worlds stay data (the save format already is the data model); a headless
   interpreter steps robots against records; bird mail is guid-addressed
   queues between records; the 3D scene renders only the world you stand in,
   with everything else running at duration 0 — exactly the C++'s trick,
   reconstructed. This makes dozens of houses cheap.
