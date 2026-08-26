# Behaviours

Anima-gadgets, after the Playground project's answer to *how does a child
reuse behaviour without reading code* — a picture whose front carries
behaviours you can lift off and put on your own butterfly.

**A behaviour is one pad.** Its face says what it does, its panel carries the
robots that do it, and those robots speak about *my thing* through a live bird.
To use one:

1. drop it on your thing — its bird is re-pointed and **nothing else changes**
2. press **space** on it (**`.`** stops it)
3. wake **Ruby** and click it to let go again

Unattached, a behaviour's bird points at the behaviour itself. That is not a
demonstration mode: it is what *my thing* means when nobody has said otherwise,
which is why a gadget set down on the table does its own thing.

**Nothing here is built in.** There is no move, no bounce, no follow. There are
messages a thing already answers —

```
[set   | across   | 1/2]   [set  | away | 2]   [set  | position | [x|z]]
[move  | across   | 1/60]  [move | away | n]   [move | position | [dx|dz]]
[query | across   | bird]  [query| position | bird]
[listen| position | bird]  [listen | edge | bird]  [listen | touch | bird]
```

— and robots that send them. Bouncing is three robots that differ only in the
word they expect from the *edge* reading; flipping the step is a `×−1` dropped
on a number.

## library.world.json

The shelf: six gadgets and a star to try them on.

| gadget | how it works |
|---|---|
| moving right | two steps: copy the step, give it to my thing |
| moving left | the same gadget with a negative step — the step is data |
| bouncing | three robots on the `edge` reading: *left* → flip and move, *right* → flip and move, anything → move |
| wrapping at the edges | the same shape, but sends `[set \| across \| ∓3/2]` instead of flipping |
| following the pointer | the pointer device gives `[across \| away]`; a thing takes `[set \| position \| …]`; the robot puts one inside the other |
| moving with the arrow keys | five robots on the keyboard nest, one per arrow and one that swallows anything else so a stray key cannot stop the team |

Six, not the twelve the plan calls for. The remaining six in the starter set —
grow and shrink when touched, make a sound on hit, reverse on collision, a
speed limit, send a message to the score — all want either a **size message**
or arithmetic on what the `touch` channel hands over, and are the next thing to
build.

Regenerate with `python make_library.py`.

## The three worked examples

`library` folds the robots away on panels, which is what makes a gadget usable.
These three lay the same robots out **in the open**, one idea each, so you can
see what a behaviour is before meeting one folded up:

- **moving** — the two-step Mover, and what is *not* in it: the robot does not
  know what it moves, and the thing does not know it is being moved.
- **bouncing** — why the edge is a *reading* and not an event. An event leaves
  the nest empty most of the time, and a team member facing a bare nest dozes,
  which stops the very robot doing the moving.
- **following** — the test of whether two vocabularies were designed as data.
  The pointer device and the position message were written a week apart and fit
  without an adapter.

Regenerate with `python make_moving.py`, `make_bouncing.py`, `make_following.py`.

## Writing one

`_beh.py` has the helpers: `live(thing, lid)` gives a thing an identity,
`to(lid)` makes a bird addressed to it, `msg(...)` builds a message box, and a
gadget is

```python
{'kind': 'text', 'text': name, 'gadget': True,
 'lid': lid, 'evt': 'evt-' + lid, 'look': {...},
 'panel': {'kind': 'world', 'v': 3, 'bench': [],
           'stations': {'stand': work_box}, 'active': robot}}
```

The `gadget` mark is what makes dropping it *bind* rather than ride, and it is
also the rule from the 2000 write-up: a behaviour must be **one thing**, so
there is never a way to take home half a gadget.

None of these is in the regression gate. A gadget runs on the frame clock, in
its own panel, and the gate drives the main queue; they are verified by hand
instead — the bouncing gadget bound to the star and switched on ran to 1.24,
turned, ran to −1.17, and turned again.
