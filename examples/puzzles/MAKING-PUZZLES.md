# Making puzzles for ToonTalk 3D

A puzzle is not a special kind of thing. It is a **world file** — the same
JSON the *Save world* button writes — with a few extra fields on it. That
means every puzzle can be built inside the workshop with the tools you already
know, saved, and finished with a text editor; or written outright in Python
with the small helpers in this folder. This document is the recipe, both ways.

What makes a world a puzzle:

1. **A constrained table.** Fewer stacks, perhaps no keyboard, maybe no Undo.
2. **A goal in plain sight** that cannot be picked up — the thing wanted.
3. **A bird** to give the answer to.
4. **A judge**: an opaque house whose robots decide, by their own thought
   bubbles, whether what arrived is the goal, and answer by bird with a note.
5. **Marty's words**: what he says on arrival, and hints in order.

Everything below is about those five.

## The shape of the file

```json
{
  "kind": "world", "v": 3,
  "name": "p2",
  "intro": "OK, now we’ll need a 4. Give it to the bird when you have one.",
  "goal": "a 4",
  "hints": ["Try putting the twos together.",
            "Drop a 2 on a 2 and wait until it turns into a 4.",
            "OK, here’s all you have to do: …"],
  "rules": { "stacks": [], "tools": [],
             "typing": { "numbers": false, "pads": false },
             "undo": true },
  "bench": [ … the things on the table, with x and z … ],
  "scenery": [ … things standing in the room … ],
  "stations": {}, "active": null
}
```

| field     | what it does |
|-----------|--------------|
| `name`    | how a robot's `load` step finds this world (`p2` finds `p2.world.json`), and the name progress is kept under |
| `intro`   | what Marty says when the world opens |
| `goal`    | what is wanted, in words — for the card and for Marty |
| `hints`   | in order; a visitor who asks Marty for a hint gets the next one, and the last again once they run out. By convention the last is the whole answer, for the desperate |
| `rules`   | which **stacks** still stand (`rooms`, `texts`, `nests`, `scales`, `dice`, `sounds`, `minis`, `numbers`, `boxes`); which **tools** are present (`mimi`, `dusty`, `ruby`, `notebook`, `save`, `import`, `devices`); whether the keyboard may write **numbers** and **pads**; whether **undo** is allowed; and optionally `maxSteps`, a cap on how many steps a robot may be taught |
| `bench`   | the things on the table: `{ "thing": …, "x": …, "z": … }` |
| `scenery` | things standing in the room rather than on the table: `{ "thing": …, "x", "y", "z", "ry" (turn in degrees), "sz" (size) }` — Marty's ship is one |
| `wipe`    | `false` means "add these things to the table" instead of replacing it |
| `library` | optional: other worlds bundled inside by name, for a file that must carry its own sequel |

A thing that must not be taken carries `"fixed": true`. A thing that is also
`"ghost": true` is scenery: it stays where it came down and nobody can lift
it.

Rules are **per puzzle**, and a step cap is worth having only where a lazy
algorithm would otherwise solve it (a robot taught to drop five things when
it should be taught one, and run five times).

## Route one: build it in the workshop

This is the way that needs no code at all.

1. **Start from free play** and set the table: the materials at the front
   where the visitor works, the bird in the middle, the reply nest beside
   her, the goal and the judge at the back. Make the goal by hand — it is an
   ordinary thing until you mark it fixed (step 5).

2. **Take away the stacks you do not want.** Wake Dusty and point him at a
   stack: he swallows the whole stack, and it leaves the world. Its rule is
   written down with the save, so it stays gone in the puzzle. Click Dusty to
   get it back if you change your mind. (Dusty cannot remove *himself*; the
   tools list is edited by hand in step 5.)

3. **Build the judge.** The judge is a room from the room stack with a robot
   team inside, dozing on a nest. Give the robot a box laid out like this:

   ```
   [ the post nest | the reply bird | note pad… | the "not quite" pad ]
   ```

   The bird on the *table* is the one whose nest is in the first hole, so
   whatever the visitor gives her lands under the judge's nose. The reply
   bird's nest goes on the table as *from the judge*. Train the **leader** on
   a box with the goal sitting on the nest: take the top thing off the nest,
   set it down, take the note pad, give it to the reply bird — and, if there
   is a next puzzle, a `load` step (see below). Then wake Ruby and loosen
   every hole of its thought but the first: an empty hole in a thought means
   *anything or nothing may sit here*, so the judge dozes quietly on an empty
   nest instead of nagging.

   Wrong answers must come back **with a note**, or the visitor waits
   forever. Add team-mates whose thoughts say *any box*, *any number*, *any
   pad* (Ruby loosens a thing all the way to "any") and teach each one: set a
   copy of the "not quite" pad on Mimi, give the copy to the reply bird, then
   take the answer off the nest and give that to the reply bird too. Mimi is
   the workshop's, not the table's, so a robot inside a house may copy.

   The team is tried **in order**, so the members behind the leader are the
   judge's *otherwise*: they run precisely when the answer was not the goal.
   That ordering is the only way to say "not" in a thought, and it is worth
   more than judging -- a member back there can count the tries, answer
   differently each time, or send back a hint.

   Click the roof until the walls are solid: an opaque house is what marks it
   as the judge, and the tooltip invites the visitor to look but not to
   cheat.

4. **Save the world** (the Save button, or *Save world* on the card).

5. **Finish it in a text editor.** Open the `.world.json` and add `name`,
   `intro`, `goal`, `hints`, and `rules` (the stacks Dusty swallowed are
   already there; add the `tools` you want to keep, the `typing` switches,
   `undo`). Put `"fixed": true` on the goal thing, and `"judge": true` on the
   room record so the card can find it. Add `"label": "we need this"` to the
   goal and labels to the bird and nest if you like — labels are tooltips.

6. **Try it**: open the app with `?world=examples/puzzles/yourname.world.json`
   (any path the server can reach), or import the file. Give the bird the
   goal by hand and make sure the note comes back; give her something wrong
   and make sure *that* comes back with a note too.

## Route two: write it in Python

`_pz.py` in this folder does steps 3 to 5 for you, and `make_puzzles.py` is
fourteen worked examples. The whole of puzzle 2 is:

```python
from _pz import *

puzzle(
    'p2',
    'Did you notice that things wiggle when they are ready to be picked up? '
    'OK, now we’ll need a 4. Give it to the bird when you have one.',
    'a 4',
    ['Try putting the twos together.',
     'Drop a 2 on a 2 and wait until it turns into a 4.',
     'OK, here’s all you have to do: drop one 2 on the other. When it '
     'turns into a 4, pick up the 4 and give it to the bird.'],
    rules(),                                   # no stacks, no tools, no typing
    table([num(2), num(2)],                    # materials, across the front
          fixed(num(4), 'we need this'),       # the goal
          bird(9911, 'p2-post', 'give me your answer'),
          nest(9912, 'p2-reply', 'from the judge'),
          judge('the judge', 9911, 'p2-post', 9912, 'p2-reply',
                right=num(4),
                on_right=next_note('') + [load('p3')],
                notes=['That’s it! The computer has its 4. Next: a box of three.'])),
    scenery=SCENERY)
```

- `num(n)`, `num(n, d)` (a fraction), `num(n, op='*')` (a badge: `+`, `-`,
  `*`, `/`), `box(a, b, …)` with `None` for an empty hole, `empty_box(n)`,
  `pad('A')` for a pad, `txt('A')` for a pad in a condition.
- `rules(stacks=[…], tools=[…], typing={…}, undo=True, max_steps=None)`.
- `fixed(thing, label)` marks the goal.
- `judge(name, post_id, post_guid, reply_id, reply_guid, right, on_right,
  notes, others, sorry)` builds the whole house: `right` is what a correct
  answer looks like on the nest, `on_right` the steps after it has been taken
  off and set down (`next_note('')` sends the first note pad; add
  `load('p3')` to offer the next puzzle), `notes` the pads in the box, and
  `sorry` the "not quite" text. Team-mates for any box, any number and any
  pad are added for you.
- `table(materials, goal, bird, nest, judge)` is the one layout every table
  uses; `SCENERY` is Marty's ship.
- Ids (`9911`, `'p2-post'`) just have to be unique across the set: a nest and
  its bird share a guid, and that is how the bird finds home.

Run `python make_puzzles.py` in this folder to write the files.

## What the judge can and cannot decide

The judge is a robot, so it decides what a robot's thought can say:

- **Exact identity.** A number matches a number of the same value *and the
  same badge*; a pad matches the same text; a box matches hole by hole, in
  order, with the same number of holes. `[2 | 1]` is not `[1 | 2]`. Say so
  in the intro when order matters.
- **Anything-or-nothing.** An empty hole in the thought accepts anything, or
  nothing, in that hole. There is no way yet to insist a hole be *empty*, so
  do not write a puzzle that turns on emptiness.
- **Ruby's loosening**: "any number", "any box", "any pad" — for catching
  wrong answers of the right kind, and for goals such as "any number bigger
  than…" only where a scale can be brought in.
- **"Not this" is a matter of order.** No thought can say *not*, but a team
  is tried in order and the first member whose thought fits is the one that
  runs -- so a member placed after the others runs exactly when none of them
  matched. That is how a wrong answer gets its note: the judge's leader
  recognizes the goal, and the members behind it (any box, any number, any
  pad) catch everything else and send the "not quite" pad back. Order the
  team from the most particular thought to the most general, and the last
  one is your *otherwise*.
- **Behavior, indirectly.** "A number that keeps getting bigger" is still
  not something a thought can name, and the originals used special cases for
  goals like it. Two things get close. A puzzle whose answer is a *process*
  can be written so the process leaves a thing -- the total in the box, the
  1,024 in the hole. And a robot behind the leader can be arranged to run
  when the match is *not* the goal, which is enough to answer, complain,
  count the tries, or hand back something different each time.
- **A robot needs no box.** It can be given a bare thing, and it can set
  something down on its own desk where that thing was -- the doubler in
  puzzle 7 works on a lone 1. Give it a box when the work needs more than
  one place.
- **No Rounds control.** A robot runs until its thought stops fitting. A
  puzzle that iterates must therefore either stop by itself (a nest that
  empties) or be the visitor's to stop in time (Stop, or the full-stop key,
  lets the robot finish the round it is in).

## Chaining puzzles and shipping a set

A `load` step in the judge's program names the next world. Inside a puzzle
it does not open the world at once: it arms the **Next puzzle** button on
the card, so the note stays readable. The app finds the world by name — in
memory if it was bundled, or by fetching `examples/puzzles/<name>.world.json`
from the server.

To put a set inside the page itself (the published artifact can fetch
nothing), drop the files in this folder and run, from the project root:

```bash
python embed_puzzles.py
```

Every `*.world.json` here goes into the page as one gzip block, and the
**Puzzle game** button on the door card starts from `p1`. Progress is kept
per visitor by name, so a returning visitor is offered *Carry on* or *Start
again*.

## Checklist before you call it done

- Give the bird the goal: does the note come back, and does Next light up?
- Give the bird something wrong of the right kind: does it come back with the
  "not quite" note?
- Ask Marty for hints until they run out: is the last one the whole answer?
- Is anything the visitor needs sitting in a stack you took away?
- Can the goal be picked up? It must not be.
- Does the intro say the one thing the judge is strict about (order, badge,
  exactly this number)?
