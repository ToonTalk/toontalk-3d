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

`make_puzzles.py` writes p1 to p5 (after the original tutorial: a box with 1
and 2; a 4 from two 2s; a box with 8, 16 and 32, joined by dropping boxes on
each other's sides; a zero from a 3 wearing a minus badge; a box of two zeros
made by a robot you train, with Mimi). Every later puzzle rides in the earlier
ones' `library`, so p1 alone carries the set. Open one with
`?world=examples/puzzles/p1.world.json`, or import the file.

The layout is one rule for every table (`table()` in `make_puzzles.py`): what
you work with across the front, the bird in the middle, the reply nest beside
her, the goal and the judge at the back.

## Shipping the set

`python make_puzzles.py` writes the files; then, from the project root,
`python embed_puzzles.py` puts p1 (with its library) into `toontalk-3d.html`
as a JSON block, so the **Puzzle game** button on the door card works in a
published artifact where nothing can be fetched. Progress (the puzzle a
player is on, and the ones solved) is kept per person in the browser.
