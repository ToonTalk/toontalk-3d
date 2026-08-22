# toontalk-3d

An experiment in rebuilding [ToonTalk](https://en.wikipedia.org/wiki/ToonTalk)'s ideas with real 3D
assets rather than the original's pre-rendered sprites — and in seeing how far
LLM-driven asset creation can carry a project like this.

Nothing here tries to copy the original's artwork. The characters are new
designs, generated from Blender Python scripts rather than modelled by hand.

For the story behind the project, see [the write-up](https://docs.google.com/document/d/1gwSygWYhvqXttB8eqZZdZbAmCEYeMUI2RLeaKsx9sVE/edit?usp=sharing).

## What works today

`toontalk-3d.html` — **ToonTalk 3D**, a programming-by-demonstration workshop
(`nano-toontalk.html` remains as a redirect):

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
  page; corner tabs flip the spread. Dusty removes an entry — and undo puts it
  back — but he will not touch your own notebook, and clicking it wobbles it
  rather than lifting it, so its corner tabs stay clickable. Any other notebook
  goes when open at two blank pages. The desk notebook persists
  in this browser **under your name** — the app asks who is working here at
  the start, with the last name already filled in, and each name gets a
  notebook of its own. It starts with a blank notebook filed on page 1 — copy
  it out to make more, and a copy shares nothing with the one it came from.
  A robot trained on the desk notebook looks it up by name when it runs; one
  trained on any *other* notebook — one it was given, or one on its own work
  area — reads that very notebook instead.
- **Saved files carry a format version.** Every world, thing, robot and the
  notebook records the format it was written in; a file from a *newer* build is
  refused with a message naming both versions rather than half-read into
  something quietly wrong, and a file with no version at all is read as the
  original v1. A box past 64 holes is written sparsely — a hole count and only
  the holes that hold something — which took one 500,000-hole box from 2.5 MB
  to 448 bytes.
- **The message under the title can read itself aloud** — a speaker button
  there turns it on and picks the voice, separately from Marty's. Both voices
  belong to whoever is signed in, not to the browser: like the notebook they
  are kept under the name, so one person choosing a voice does not change it
  for everybody else who uses the machine.
- **The workbench reshapes.** "Reshape table" reveals glowing corner handles:
  click one to carry that corner, move the pointer to stretch or shrink the
  top (legs follow), click again to set it. Anything left overboard by a
  shrink slides back on, and the shape is remembered in this browser.
- **Rooms** come off their own stack: little houses that each hold a whole
  workshop as data — worlds in a box, nestable without limit. Drop a robot
  through the roofline and it stands ready behind the desk inside; drop
  anything else and it lands on that desk, and the room's robot does the work
  the moment the outer world goes quiet (bottled up and run at Instant speed
  between frames, invisibly). Click the roof to toggle the walls between
  solid and glass — glass shows tiny stand-ins of what the room holds. Birds
  whose nests were filed into a room fly in, deliver, and come back out.
  Click the glowing door to step inside: the room swells to become the world,
  and the world you left shrinks onto the new room's table as a little room
  of its own — walk back out through its door. An opaque room's pending work
  is done by the time you arrive; a glass room runs before your eyes at your
  speed setting.
- **Dusty the vacuum and Ruby the eraser**, under the bench. Dusty *removes*:
  things from the world, entries from notebook pages, parts of a thought
  outright (leaving an empty hole that matches anything or nothing). Ruby
  *erases*: each click makes a part of a thought one step more general — 7,
  then *any number*, then *anything*. Waking one settles the other, and
  whoever is awake sways and fidgets so there is never any doubt.
- **Marty the Martian**, the green fellow beside them. Click him and ask
  anything about the workshop, or say *"show me birds"* and he walks over and
  demonstrates it on your table, one narrated step per click of **Next** — and
  when an answer of his suggests a demo, you get a *Show me* button, never a
  surprise performance. He never builds programs — that part is yours.
  Pick a brain in his panel. **Gemini Nano** wants no key and no account:
  desktop Chrome carries a small model inside it, nothing typed leaves the
  machine, and the panel offers the one-off (multi-gigabyte) download with a
  button of its own rather than starting it behind your back — which makes it
  the one brain a classroom can have without handing out a key. Being small it
  cannot hold the whole manual, so it is given the sections that score against
  the question rather than all of it. Claude, ChatGPT and the full Gemini each
  want that provider's key instead (kept in this browser only); a published
  artifact is sealed and cannot reach any of them, so there he only ever has
  the phrasebook. Without a brain, his replies are canned lines from a
  phrasebook that picks the right demonstration, and the panel says so. Left
  alone he speaks in a woman's voice where the browser has one — the high
  pitch and the drift between sentences are what make him Martian, not which
  voice it is.
  Whatever brain he has, **he answers from the manual**: `manual.html` is
  handed to him with every question (live when a server is serving it, from a
  copy embedded by `embed_manual.py` otherwise), so he describes the workshop
  that exists rather than one a model imagines.

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
- **Saving and sharing.** Three buttons: **Save held thing** writes whatever
  is in your hand to a `.thing.json` file — any thing, trained robots
  included; **Save world** writes the entire workshop to a `.world.json`
  file; **Import file** opens either (drag-drop onto the app works too) — a
  thing lands in your hand, a world replaces the workshop. Robots are named
  by typing while holding them (the name shows on their chest); rooms are
  named the same way, the name appearing on their three doorless walls.
  Loading a robot never costs the one already at the bench: it shrinks onto
  the table, or steps aside with its desk if it is waiting on a nest, and
  several robots can stand behind the bench — click one for focus, click the
  focused one to pick it up.
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

Every sound effect is synthesised on the spot from oscillators and filtered
noise — picks pop, drops thunk, combining rings, birds chirp, Dusty slurps,
Ruby squeaks, rooms whoosh — with a speaker button to mute and a slider for
volume. Textures are hand-painted canvases in code: wood-grain table and
desks, paper pads, straw nests, two-metal scales (brushed steel and brass),
leather notebook, stucco room walls. No image or audio files anywhere: the
whole app is still one HTML file.

## Running it

To use it unmodified, no setup needed: <https://toontalk.github.io/toontalk-3d/toontalk-3d.html>.

To run it locally, it needs any static server; the repo assumes port 8311.

```bash
node serve.js 8311
```

Then open <http://localhost:8311/toontalk-3d.html>. The **?** button in the
toolbar opens `manual.html` — a guided handbook whose illustrations are live
embedded workshops (the app itself in an iframe with a small canned scene), so
every example can actually be tried.

`serve.js` also accepts `POST /capture`, which the pages use to write rendered
frames to `captures/` — that is how the 3D work gets reviewed without a human
having to eyeball every change.

### One file, no server

```bash
python build_artifact.py
```

writes `toontalk-3d.artifact.html`: the same workshop with three.js, the
GLTFLoader and both `.glb` models packed inside it, so it needs nothing beside
it — hand it to somebody, put it on any static host, open it from disk. It is
built from `toontalk-3d.html`, which stays the only source; every one of the
eleven example worlds produces byte-identical results in the two.

It does **not** run as a published claude.ai artifact. The frame there tolerates
a full-screen three.js scene rendered once, but goes white — markup and all —
as soon as this workshop's animation loop runs, however long the boot is
delayed. Two smaller limits of that frame are worked around in the build:
inline scripts over about a megabyte are dropped silently (so the bundle is
split across several), and nothing may be fetched at all, not even a `data:`
URI the page made itself (so the models are parsed out of memory instead).
Marty, likewise, could only ever speak from his phrasebook inside one.

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

## License

MIT — see [LICENSE](LICENSE).
