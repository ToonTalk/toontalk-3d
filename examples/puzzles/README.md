# Puzzles

A puzzle is a world file with a few more fields. Nothing here is a new kind of
thing.

```
name     the name a robot can open it by ("load" step)
intro    what Marty says when it opens
goal     what is wanted, for the card and for Marty
hints    in order; the last is the whole answer
rules    { stacks: [ids], tools: [ids], typing: {numbers, pads}, undo, maxSteps }
library  { name: world } -- other worlds bundled inside (optional: the app
         carries the whole set by name, and a server can fetch any file)
scenery  [ {thing, x, y, z, ry, sz} ] -- things standing in the room rather
         than on the table (Marty's ship, seven times hand size)
wipe     false means "add these things to the table" instead of replacing it
```

The pieces on the table:

- a **goal** with `fixed: true` -- shown, never taken, dropped into, vacuumed
  or erased
- a **bird** whose nest is inside the judge's house -- give her your answer
- a **reply nest** on the table -- wrong answers come back here, right ones
  get the judge's note
- the **judge**: a room with `judge: true`, opaque, running, whose robot team
  dozes on the post nest. The leader's thought is the goal; its program takes
  the answer off the nest, sends the note, and `load`s the next puzzle. The
  team behind it recognises any box, any number, any pad, and sends back a
  COPY of the judge's "not quite" pad (Mimi is the workshop's, so a robot in
  a house can copy) and then the answer itself. Every hole of the judge's
  thought but the first is `null` -- anything or nothing -- so the judge dozes
  on an empty nest once the note has gone.
- a `maxSteps` rule only where a lazy algorithm would otherwise solve the
  puzzle; it is announced when the lesson starts.

Stack ids: rooms, texts, nests, scales, dice, sounds, minis, numbers, boxes.
Tool ids: mimi, dusty, ruby, notebook, save, import, devices.

In a puzzle the judge's `load` step *offers* the next world: a Next button
appears on the card once the note has been read. Outside a puzzle `load`
opens the world at once.

**To make your own, read [MAKING-PUZZLES.md](MAKING-PUZZLES.md).**

`make_puzzles.py` writes p1 to p33 (after the original tutorial: a box with 1
and 2; a 4 from two 2s; a box with 8, 16 and 32, joined by dropping boxes on
each other's sides; a zero from a 3 and a −3; a box of two zeros made by a
robot you train, with Mimi; the total of the numbers on a nest, by a robot
whose thought Ruby loosens -- it dozes when the nest is empty; and exactly
1,024 from a single 1 and a robot that doubles, which never stops by itself:
Stop lets it finish the round it is in, so the player presses Stop -- or the
full-stop key -- when the number says 512; no box is needed, the robot
sets the copy down on its own desk; then a box inside a box inside a box, of
two-hole boxes; three zeros in the second hole of a box; six zeros from a box of two;
the door code 77 from powers of two; a half from a divide badge; a million
from a times-ten badge copied five times; A, B and C on pads, typed; the
seconds in a year from three times-badges; ToonTalk from two pads joined at
the edge; three quarters from a divide and a times; ¾ against ⅔ on a scale;
a box of exactly 24 zeros by copying and joining; then three robots: one
turns [3|2|1|_] round, one counts the letters on a nest and sends them on by
bird, one grows a box of zeros a hole a round and must be stopped at nine,
and one grows a box with a scale in its third hole and stops by itself when
the pans balance; then 1,024 by a doubler weighed against 1,000; the biggest
of three and a pair in order, with a scale by hand; a robot that swaps a
scale's stuck pans; letters poured into a word and a word into letters; the
third letter of a word picked out by a number; a halver weighed against
1; and a team of four robots that sorts three stuck fractions). Marty's ship lies on the floor behind every table as `scenery`; a small
goal carries `size` on its thing and stands larger.

There is no Rounds control: a robot runs until its thought stops fitting, so
a puzzle that iterates either stops by itself (an emptying nest) or is the
player's to stop in time (doubling). Each file is one puzzle; the page
carries the set. Open one with `?world=examples/puzzles/p1.world.json`, or
import the file.

The layout is one rule for every table (`table()` in `make_puzzles.py`): what
you work with across the front, the bird in the middle, the reply nest beside
her, the goal and the judge at the back.

## Shipping the set

`python make_puzzles.py` writes the files; then, from the project root,
`python embed_puzzles.py` puts every `*.world.json` here into `toontalk-3d.html`
as a JSON block, so the **Puzzle game** button on the door card works in a
published artifact where nothing can be fetched. Progress (the puzzle a
player is on, and the ones solved) is kept per person in the browser.
