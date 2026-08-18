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
  ends, tapering to an ellipsis in the middle — and walking up close makes
  more digits appear. The other faces of the block show other forms of the
  same value: the top repeats it, the back gives English words or a mixed
  fraction, one side scientific notation, the other digit-grouped or exact
  decimal form. Only the visible digits are ever computed, and a repeating
  decimal that fits gets a bar over its repetend; one that doesn't ends in an
  ellipsis. Scientific notation gets the same treatment — a bar when the
  mantissa's cycle fits, an honest ellipsis when it is cut short, and no fake
  trailing zeros.
- **Text pads** come off their own stack blank. Type on a held pad to write;
  dropping one pad on another concatenates them, and the side of the drop
  decides the order — "Talk" on the right edge of "Toon" reads "ToonTalk",
  on the left "TalkToon". A whole number dropped on a written pad shifts its
  first or last letter along the alphabet; dropped on a blank pad it writes
  itself out as digits. In a robot's thought a pad matches its exact text
  until Dusty erases it to *any text*.
- **Boxes** have holes; a hole holds a number, a box, a scale, a bird or a
  nest, so structures nest. Type a digit on a held box to give it that many
  holes; shrinking splits it like an array, and the excess holes fall away as
  a box of their own — onto the bench when you do it, onto a free work spot
  when a robot does. Dropping a box on another **joins** them — on the left
  half its holes go in front, on the right half behind. Typing letters on a
  held box, bird or nest writes a name on a little plaque stuck to it.
- **Scales**, each with two pans that behave exactly like box holes; the beam
  tips toward the larger number. Unlike the original's, they stand alone
  rather than living in a three-hole box.
- **Nests with eggs.** Set a nest down and its egg hatches into a bird. Give
  the bird anything and she flies it home to her nest, where deliveries pile
  up; the pile travels with the nest. A new delivery goes *underneath* — the
  bird lifts the pile aside, tucks it in at the bottom, and stacks the pile
  back — so the top of a pile is always the oldest delivery, and it is the
  only one that can be taken. Nobody can move the pile as a whole; the nest
  and everything on it move together. Robots take from piles too: shown a
  pile top during training, a robot learns *take the top of the pile on that
  nest*, one delivery at a time. Naming a nest while its egg is still in it
  names the bird that hatches as well.
- **Nests are windows, not walls.** A robot trained on a covered nest gets a
  condition on the *top item*, so it matches either that thing there or a
  nest with that thing on top. And when the nest is empty at run time, the
  robot doesn't fail — it shrinks and dozes until a bird delivers something
  that fits, then springs back up and carries on. That is the receiving half
  of dataflow: a robot on an empty nest is a process blocked on a channel.
- **Copying birds and nests.** The copier now takes anything but robots. A
  copied bird serves the same nest as the original. A copied nest joins the
  original's delivery group: give any of their birds something and she copies
  herself on the spot, one clone per nest, every nest receiving its own copy
  at once — only the real bird flies home again; the clones deliver, rise,
  and fade away for good. Broadcast, in other words.
- **A copier** with two surfaces: originals are scanned on the upper platform,
  independent deep copies are delivered to the lower tray. Clicking a surface
  with an empty hand takes from that surface.
- **The notebook**, open on the table as a two-page spread. Drop anything on
  a blank half to file it; clicking a page's entry hands you a fresh copy
  while the page keeps its own. On a full page, a written text pad opens the
  first page whose contents mention its text and a whole number jumps to that
  page; corner tabs flip the spread. Dusty removes an entry, and a notebook
  itself only goes when open at two blank pages. The main notebook persists
  in this browser and starts with a blank notebook filed on page 1 — copy it
  out to make more.
- **The workbench reshapes.** "Reshape table" reveals glowing corner handles:
  click one to carry that corner, move the pointer to stretch or shrink the
  top (legs follow), click again to set it. Anything left overboard by a
  shrink slides back on, and the shape is remembered in this browser.
- **Dusty the vacuum and Ruby the eraser**, under the bench. Dusty *removes*:
  things from the world, entries from notebook pages, parts of a thought
  outright (leaving an empty hole that matches anything or nothing). Ruby
  *erases*: each click makes a part of a thought one step more general — 7,
  then *any number*, then *anything*. Waking one settles the other, and
  whoever is awake sways and fidgets so there is never any doubt.

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
  lesson, and what it was given stays on its stand, ready to Run. The robot
  also remembers the very thing it was first shown: click its thought bubble
  with an empty hand and a copy of the original falls out, whatever the
  condition has since been erased to.
- **The robot's furniture grows with the job.** Its stand is a small desk, and
  its scratch area starts as a single side-table; whenever the last free one
  is filled a new one rises beside it, and the extras sink away when its area
  is swept — unlimited temporary storage, no standing clutter.
- **The condition** — the exact thing it was trained on — floats in a thought
  bubble over its head, and refused runs pulse the mismatching parts red until
  something changes. Dusty erases progressively: a number becomes *any
  number*, a box *any box — any number of holes*, a scale *any scale*, and a
  second erase makes any of them *anything* (its own ?-cloud shape). What sits
  in a hole can be erased to *anything* on its own. A hole the robot was never
  shown anything in stays empty in the thought, and an empty hole matches
  anything *or* nothing — only the shape around it has to line up.
- **Running repeats while some condition still matches**, up to the Rounds
  limit — a loop is just a condition that stays true. **Teams**: drop one
  trained robot on another, and each pass is taken by the first member that
  recognises what is on the stand.
- **Robots fetch like you do.** A step that needs a fresh number or box sends
  the robot walking to the same stack you would use, and it drops things at
  the exact hole they belong in, not the middle of the box.
- **Saving and sharing.** Save names a robot in this browser — the name
  appears on its chest screen and in its tooltips. Export downloads it as a
  `.robot.json` file under its typed name; Import adds it to the library and
  wakes it in one step; Load wakes a robot automatically if none is at the
  bench, and never at the cost of the robot already there: loading brings in
  *another* robot. One that was working or has stopped shrinks onto the table
  with its training intact; one keeping a vigil over a nest stays on its feet,
  steps back and to the side with its own desk — and whatever it was given —
  and goes on waiting. Several robots can stand behind the bench that way;
  clicking one brings it into focus, clicking the focused one picks it up. A
  waiting robot takes the floor by itself the moment its bird delivers
  something that fits. **Save held thing** downloads *whatever you are
  holding* — a box, a number, a nest and its pile, a trained robot — as a
  `.thing.json` file; importing one (Import button or drag-drop onto the app)
  puts it straight into your hand, and a full hand sets what it held on the
  table first so the swap is visible. **Save world / Load world / Export
  world** do the same
  for the whole
  workshop — bench, stands, nests with their piles, birds with their pairings,
  and every robot's training — to this browser or to a `.world.json` file that
  Import recognises.

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

- Waiting robots resume only on deliveries; nothing else re-checks their
  condition, so filling the nest by hand does not wake one (give the thing
  to the bird instead).
- Nothing reads a scale's tilt — it shows a comparison but cannot yet be
  branched on.
- The condition cannot constrain a number's range, only match exactly or
  wildcard.
- `^` takes integer exponents only, and results are refused past an estimated
  20000 digits so a runaway loop cannot lock the browser.
- The robot's scratch area is a row of discrete spots rather than free
  placement, and there is no arm IK — transfers to the copier's raised
  platform animate the object, not the arm.
