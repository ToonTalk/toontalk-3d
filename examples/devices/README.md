# Devices

The workshop's own senses, as **nests**. Take one out of the Devices notebook
(the **Devices** button in the ⋮ menu) and it is already wired up: what happens
lands on it.

There is no new machinery here at all, and that is the point. A robot facing a
bare nest *dozes* — that rule has been in the workshop since the first list
example — so a robot given a keyboard nest wakes once per key press, waits when
nothing is happening, and needs no event loop, no callback and no subscription.
**A key press is mail.**

| nest | what lands on it | how many it keeps |
|---|---|---|
| `keyboard` | a pad naming the key — `a`, `B`, `7`, `Enter`, `ArrowLeft`, and a space for the space bar | the last 40 |
| `pointer` | `[across \| away]`, where the pointer is on the table, in the table's own steps | 1 — a position is a reading, not a history |
| `pointer press` | `down` or `up` | the last 8 |

**Read-only by construction.** Each arrives with no egg, so no bird can ever be
had from it — and a bird is the only way anything is ever put on a nest.
Nothing you build can write to the keyboard.

**Copies join the flock.** A device nest wears one of the workshop's guids, and
sharing a guid *is* joining a flock, so a second copy taken out of the notebook
receives the same mail. Two robots can watch one keyboard, and a saved world
carries its wiring with it.

## keys.world.json

A robot that types what you type. The **Scribe** is handed
`[keyboard, a pad]`; its thought is *some words on the nest, and anything
beside them*. Two steps: take the key off the nest, join it onto the right edge
of the pad.

Give it the work box and type. It shrinks and waits between
key presses, which is the whole of "waiting for input".

Regenerate with `python make_keys.py`.

## pointer.world.json

A gauge that follows your hand. The **Watcher** is handed
`[pointer, a reading]` and keeps the current reading where you can see it:
sweep the old one away, take what is on the nest, put it in the hole. Three
steps, and the two numbers change under your hand.

Zero across is the middle of the table and *away* grows towards you — the
table's own coordinates, not the screen's, so a robot reading them could put
something down where you are pointing.

Regenerate with `python make_pointer.py`.

## Writing another one

`_dev.py` holds the three guids and a `device()` helper. A device nest in a
world file is an ordinary nest record with `"dev": true` and the right `guid`;
it needs nothing else, because delivery is by guid.

Neither of these worlds is in the regression gate: both need a hand on the
keyboard or the pointer, and the gate only drives things it can drive without
one. They are verified by dispatching real key and pointer events at the app —
"Hello Ken!" on the pad, and the gauge tracking three pointer positions.
