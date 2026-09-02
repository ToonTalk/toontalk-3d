# Puzzles

A puzzle is a world file with a few more fields. Nothing here is a new kind of
thing.

```
name     the name a robot can open it by ("load" step)
intro    what Marty says when it opens
goal     what is wanted, for the card and for Marty
hints    in order; the last is the whole answer
rules    { stacks: [ids], tools: [ids], typing: {numbers, pads}, undo, maxSteps }
library  { name: world } -- other worlds bundled inside, so "load" works where
         nothing can be fetched (a published artifact)
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
  team behind it recognises any box, any number, any pad, and sends it back.

Stack ids: rooms, texts, nests, scales, dice, sounds, minis, numbers, boxes.
Tool ids: mimi, dusty, ruby, notebook, save, import, devices.

`make_puzzles.py` writes p1 and p2 (the first two of the original tutorial:
a box with 1 and 2 in it; a 4 from two 2s). Open one with
`?world=examples/puzzles/p1.world.json`, or import the file.
