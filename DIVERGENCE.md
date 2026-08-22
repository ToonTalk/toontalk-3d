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
- Ops: `+ - * / ^`, and since 2026-08-20 **`mod` and `set`** — **DONE**, the
  original's `%` and `=` under names a child can read. An operation need not be
  one character: type the letters onto a held number and it takes the word as
  soon as it is complete. `& | ~` (bitwise) and **operation-only pads**
  (Backspace the digits away and the bare operation remains) — **GAP**; the
  `setOp` step is half of the latter already.
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
- Box dropped on a number N splits into [first N] and [the rest] — **DONE**
  (2026-08-19; our flavour spends the number and keeps both parts' contents).
- Zero-hole boxes — **DONE** (2026-08-19; type 0 on a held box; joining a
  0-hole box adds nothing and spends the husk).
- Conversions: **text → one character per hole**, **robot team → one robot per
  hole**, and a box of pads poured onto a blank pad → the word — **DONE**
  (2026-08-20). The mould is a box with **no holes at all**, which the project
  owner rightly pointed out is a different gesture from dropping a robot into a
  hole: a zero-hole box has no hole to drop into, so carrying a spare team in a
  hole (fibonacci-recursive, reverse) is untouched. Notebook ↔ box — **GAP**
  (low priority).
- Hole labels exist and matching ignores them — **SAME**.
- Blank box matches any size — **SAME** (`anyBox`).

## Birds & nests

- Hatching pairs, delivery under the pile (top = oldest), copied bird → same
  nest, copied nest → multicast — **SAME** (ours implements the flock as a
  shared guid; the C++ confirms the original also keyed nests by GUID).
- Original birds accept only "rectangular" items (pads, boxes, pictures);
  ours carry anything, rooms included — **KEEP**.
- **Nest merging**: drop nest on nest — **DONE** (2026-08-20). The pile of the
  one you are holding joins the pile below it and the survivor gains the
  other's guid as an *alias*, so the birds of both go on delivering without
  knowing anything changed. Aliases travel in save files.
- Save a bird alone → she gets a new nest; save a nest alone → fresh egg —
  **SAME** in spirit (our notebook lone-copy rules).
- Robot facing a bare nest waits until covered — **SAME**; ours shows it by
  the robot shrinking and dozing — **KEEP**.

## Robots

- Positional hole addressing, re-run while matching, team pass-along, Escape/
  leave to end training — **SAME**.
- A robot in a thought bubble matches only a robot with the **same name and
  the same lesson** — **DONE** (2026-08-20, the project owner's rule). Ruby
  erases it to "a robot — any one", and again to "anything". The lesson is
  compared as its recorded steps, so two robots taught the same moves are the
  same robot as far as a thought is concerned.
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
- Robots obtain and populate rooms — **DONE** (2026-08-19): the `newRoom`
  step takes one from the stack, and a robot loads it the way users do —
  robot + gift dropped in, our truck. Rooms stowed in the given box persist
  (scratch spots are still swept); dirty rooms now run wherever they sit,
  box holes included, and rooms inside rooms run recursively during the
  bottle (depth cap 6), fixing the old depth-2 deadlock.
- The copier duplicates robots, training, name and team included — **DONE**
  (2026-08-19), the original wand's 'S' mode; broadcast birds carry robots
  too. Recursive self-copying programs are now expressible.
- Bombs: a robot can destroy the house it is in; contents are rescued only if
  Dusty is present. **DONE** (2026-08-20) in our own flavour: **a robot
  vacuums the very box it was working on**. The original manual already says
  that ends the team for good, and it needs no new object — Dusty is the tool
  a child already knows. Three consequences, all deliberate:
  - the run ends with "swept its own box away: finished, for good" rather than
    advice about erasing its thought;
  - a house whose robot has done that is dead — nobody works there and nothing
    is left to work on — so it **folds away to nothing** (`markRoomDone` →
    `retireRoom`), which is what stops recursive workers accumulating;
  - anything still inside goes with it, which is the point: the robot swept up
    its own work first.
  Ken's five ports use it: `append`, `n-to-1` and `factorial` end this way, and
  `reverse`'s houses now clear themselves as each one finishes. A finisher
  whose box still holds live houses (reverse's own) sweeps a smaller thing
  instead — its bird.
- The original's truck can carry a **notebook**, and `reverse.tt` uses that as
  a module system. **DONE** (2026-08-20) in our own form: the workshop's
  notebook is *furniture*, like the stacks and the table — it survives loading
  a world — and robots can address it as a container. A robot fetches a blank
  pad, writes a name on it (the new `setText` step), drops it on the notebook
  to open it there, and takes a copy off the page: `take {c:'notebook',
  path:[1]}`. That is a module system, and it is how one program uses another.

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
- Dusty over an **empty hole** does nothing at all — **DONE** (2026-08-20).
  It used to stop the robot dead ("Dusty found nothing there"), which made it
  impossible to write one robot for a hole that sometimes holds a spent nest
  and sometimes holds nothing. That is exactly what Ken's `append` needs, and
  it is how the original behaves. A hole that does not EXIST is still an
  error worth stopping for.

## Notebook

- Filing, text/number navigation, Dusty-only removal, main-notebook
  persistence, blank first page holding a blank notebook — **SAME**.
- Robots may not touch the original's main notebook (it is shared); ours lets
  robots file AND look up — **KEEP** (2026-08-20). A shared library a robot can
  read is what makes one program able to use another by name.
- Retrieval gives a copy (manual is silent; we chose copy) — **KEEP**.

## Scales

- Original scales sit in a 3-hole box comparing their *neighbours*; ours are
  standalone with two pans — **KEEP** (documented divergence). Ken's
  `factorial.tt` and `swap.tt` both turn on this, and both port cleanly by
  moving the two compared numbers into the pans: `[so far, scale, bird]`
  where the scale holds `[count, N]`, instead of `[so far, count, scale, N,
  bird]`. The live comparison — the point of the idiom — survives intact.
- Robots match on a scale's tilt — **DONE** (2026-08-19): a scale showing a
  verdict trains a tilt condition ("a scale tipping left / right / a
  balanced scale"), contents ignored; Ruby erases it to "any scale". The
  bubble shows the scale frozen mid-tip.
- Text comparison (alphabetical) — **DONE** (2026-08-20): two pads on a scale
  weigh by alphabetical order, the later word being the heavier, and case is
  not weight, so "Apple" and "apple" balance.

## Sensors & randomness

- Original sensors are live pads in the notebook: mouse, keyboard, time,
  "my address" — **GAP** as a family (needed only when pictures/games
  arrive). **Designed 2026-08-22**: not as sensors at all — see
  [BACKS.md](BACKS.md), where the family dissolves into birds, backs and
  one suspension rule.
- **The random source** — **DONE** (2026-08-19), as dice rather than the
  original's live sensor pad (0–999 frozen by dropping on a zero): a dice
  stack on the arc; drop a die on a number and it re-rolls to 1..faces (the
  die is spent, like any dropped pad); drop a whole number on a die to set
  its faces. Robots take dice (`newDie`); an erased die matches any die.
  Dice also remove the main need for a remainder operation.

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

1. *Semantics unlocks, current engine* — **DONE 2026-08-19**: Mimi copies
   robots; robots take and populate rooms (`newRoom`); nested rooms run
   recursively inside the bottle; dice for randomness; box-split-on-number
   and zero-hole boxes; scale-tilt matching. **Proven the same day**: the
   sentence generator (examples/sentence-generator.world.json), doubly-
   recursive Fibonacci — a robot that copies itself through Mimi and builds
   its own call tree of 40 rooms, 6 deep, fib(8)=21 (examples/
   fibonacci.world.json) — and a message-passing bank account with a dozing
   teller (examples/bank-account.world.json). Room work is time-sliced
   (~1.2 s per idle tick) so deep recursion never freezes the page, and
   letters from deep rooms ride the bottles up one level at a time.
2. *The original's architecture* — **DONE 2026-08-19**, in an even more
   ToonTalk-native form than planned: rather than a headless interpreter
   over records, there is **one scene containing every world live** — a
   room's world is real nodes hanging inside the room at toy scale, and
   running it means pointing the single interpreter at that world's context
   for a moment, at Instant speed (the C++'s `default_duration → 0`,
   reconstructed as a context switch). No serialisation anywhere at
   runtime; records exist only in save files. Bird mail is direct, since
   every nest in every world is scene-connected. Glass rooms show the real
   miniature world, not stand-ins. Measured: recursive fib(10) = 55 across
   109 nested houses in under 3 seconds; the old engine stalled for
   minutes on fib(6).
