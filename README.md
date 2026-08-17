# toontalk-3d

An experiment in rebuilding [ToonTalk](https://en.wikipedia.org/wiki/ToonTalk)'s ideas with real 3D
assets rather than the original's pre-rendered sprites — and in seeing how far
LLM-driven asset creation can carry a project like this.

Nothing here tries to copy the original's artwork. The characters are new
designs, generated from Blender Python scripts rather than modelled by hand.

## What works today

`nano-toontalk.html` — a programming-by-demonstration workshop:

### The things

- **Numbers** come off an infinite stack as 1s. They are exact BigInt fractions
  in lowest terms: type digits to set a value, `-` to negate — adding a
  negative *is* subtraction, so there is no separate subtract operation — and
  `* / ^` to set what a number *does* when dropped on another. Each operation
  colours the block and shows a badge. Division gives a real fraction, never a
  float. Numbers too long to fit render the ToonTalk way: full size at both
  ends, tapering to an ellipsis in the middle.
- **Boxes** have holes; a hole holds a number, a box, a scale, a bird or a
  nest, so structures nest. Type a digit on a held box to give it that many
  holes (up to 8). Dropping a box on another **joins** them — on the left half
  its holes go in front, on the right half behind.
- **Scales**, each with two pans that behave exactly like box holes; the beam
  tips toward the larger number. Unlike the original's, they stand alone
  rather than living in a three-hole box.
- **Nests with eggs.** Set a nest down and its egg hatches into a bird. Give
  the bird anything and she flies it home to her nest, where deliveries pile
  up; the pile travels with the nest. Clicking a pile item takes it, clicking
  the nest takes the nest.
- **A copier** with two surfaces: originals are scanned on the upper platform,
  independent deep copies are delivered to the lower tray. Clicking a surface
  with an empty hand takes from that surface.
- **Dusty the vacuum**, under the bench. Wake him and click things to remove
  them, or click parts of a robot's thought to erase them.

### The robots

- **A stack of miniature robots.** Set a mini on the table and drop something
  on it: it grows to full size, steps behind the bench, and takes what you
  gave it — training if untrained, ready to Run if trained. Click the
  full-size robot to shrink it back into your hand with its training intact.
  Hovering a trained mini shows its condition and whole program.
- **You move things; robots don't.** In the workshop everything you carry
  follows the pointer. A robot only acts inside its thought bubble, or when
  repeating what it learned — and it does things the same way you do,
  including using the copier and directing Dusty.
- **Steps name the robot's own containers, never places in your world.** Every
  action is an address like *hole 1 of what it was given* or *spot 2* — so a
  trained robot generalises to anything of the right shape for free. Its
  scratch spots and the copier are private and swept clean every run.
- **Training is a daydream.** Everything the robot does while learning is
  recorded, and leaving the bubble rewinds the world; the robot keeps only the
  lesson, and what it was given stays on its stand, ready to Run.
- **The condition** — the exact thing it was trained on — floats in a thought
  bubble over its head, and refused runs pulse the mismatching parts red until
  something changes. Dusty erases progressively: a number becomes *any
  number*, a box *any box with N holes*, a scale *any scale*, and a second
  erase makes any of them *anything* (its own ?-cloud shape).
- **Running repeats while some condition still matches**, up to the Rounds
  limit — a loop is just a condition that stays true. **Teams**: drop one
  trained robot on another, and each pass is taken by the first member that
  recognises what is on the stand.
- **Saving and sharing.** Save names a robot in this browser; Export downloads
  it as a `.robot.json` file; Import adds one to the library; Load wakes a
  robot automatically if none is at the bench.

Undo (Ctrl+Z or the button) unwinds moves, typing, joins, vacuums, erasures —
including recorded steps mid-lesson. Mode boundaries clear the history.

`robot-demo.html` — the earlier standalone pick-up-and-put-down demo.

## Running it

Needs any static server; the repo assumes port 8311.

```bash
node serve.js 8311
```

Then open <http://localhost:8311/nano-toontalk.html>.

`serve.js` also accepts `POST /capture`, which the pages use to write rendered
frames to `captures/` — that is how the 3D work gets reviewed without a human
having to eyeball every change.

## Assets

The `.py` files are the source of truth, **not** the `.blend` files: each one
regenerates its model, its turntable renders and its `.glb` from scratch.

```bash
blender --background --factory-startup --python robot_v4.py
blender --background --factory-startup --python dusty_v1.py
```

Edits made in Blender's GUI will be overwritten by a re-run, so fold anything
worth keeping back into the script.

## Known limits

- Birds and nests are objects, not yet communication: robots cannot be given
  them or wait on them, so there is no inter-robot dataflow yet.
- Nothing reads a scale's tilt — it shows a comparison but cannot yet be
  branched on.
- The condition cannot constrain a number's range, only match exactly or
  wildcard.
- `^` takes integer exponents only, and results are refused past an estimated
  20000 digits so a runaway loop cannot lock the browser.
- The robot's scratch area is three fixed spots rather than free placement,
  and there is no arm IK — transfers to the copier's raised platform animate
  the object, not the arm.
