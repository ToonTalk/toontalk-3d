# games

Worlds that are games, built from the workshop's ordinary parts and made to
be read as well as played.

## 👾 space-invaders.world.json

Eight invaders, a ship, a dark field and a score. Point at the field and
press SPACE; the left and right arrows move the ship, the up arrow fires.

Every picture is a pad with its behaviours on its BACK as cards whose faces
are sentences -- "I explode when a bullet hits me: a bang, and I vanish." --
the way the original ToonTalk's Space Behaviours laid its anima-gadgets out.
Point at an invader and press the gear: its panel comes out with the cards
on it; Enter looks straight down at it. Point at a card there and press the
gear again: the card's own panel, its robot and the box it works on. The
knob folds each one home.

What it is made of: the touch reading's name hole (the invader's card is
trained on "bullet"), `[drop | bullet | [0 | -1/3]]` for firing a working
copy, `[vanish]`, the keyboard nest, a speed, and the field's own
`[listen | touches | bird]` for the referee that keeps the score.

Regenerate with `python make_space_invaders.py`; the Pongs with `make_pong.py`,
`make_pong_classic.py` and `make_pong_gadgets.py` (moved here from `behaviours/` on 13 Sep).

## 🏓 pong.world.json

The capstone, and nothing in it is new. The **table is the court**: three of
its walls are the table's own edges, the fourth is yours to guard. The ball,
the bat and the counter are three ordinary things standing on the table, and
two of them carry their own program on their own panel — so **two programs run
at once**, which is what makes it a game rather than a demonstration.

The ball's panel holds a team of six robots that differ only in what they
expect in two holes, the *edge* reading and the *touching* reading:

| what it expects | what it does |
|---|---|
| edge is `far` | flip the away step, then fly |
| edge is `near` | flip the away step, then fly |
| edge is `left` | flip the across step, then fly |
| edge is `right` | give the counter's bird a `+1`, flip, and start again in the middle |
| hit on my left or right | head the other way across, then fly |
| hit on my far or near side | head the other way away, then fly |
| anything else | fly |

The walls come first, because a wall **pins** you: a ball held against the near
wall and touching a pad on its left will turn round across for ever unless the
member that gets it off the wall is allowed a turn. And a collision **sets** a
direction rather than flipping one — flipping reverses whatever you were doing,
which half the time is back into the thing you have just hit. At a wall
flipping is safe, because the wall has clamped the ball exactly on the line.

None of them can doze, because both nests are **readings** and neither is ever
empty — which matters here more than anywhere, since the member that does the
moving is the last one tried.

The bat's panel holds one robot: take what the pointer just said, keep the
*away* of it, and give the bird on the perch `[set | away | that]`. Its across never
changes, which is why it stays a wall and does not wander off after your hand.

Every piece of it was built for something else — `[move | across | n]`, the
edge reading, the touch reading, the pointer device, a badged number given to a
bird, and `[set | width | n]`, which is the whole of why the bat is a bat and
the ball is a ball. Nothing anywhere knows the game is Pong.

**Clear the court first.** The ball bounces off *anything* on the table, so
vacuum the four instruction pads away with Dusty (he gives them back) and slide
your own notebook into a corner. That is not a workaround: it is the touch
reading being honest, and it is the shortest way to feel what it does.

Regenerate with `python make_pong.py`.

Measured, driving the frame clock by hand and the pointer with it: a player who
tracks the ball saves it twice and misses nothing; a player who walks away is
past at frame 675, the counter goes to 1 and the ball restarts at the middle of
the table. Median frame 13 ms with both panels running.

## 🏓 pong-classic.world.json

Ken sent the original — `My Programs/pong.tt`, saved out of ToonTalk 3 — and
asked for one like it. Opening the file up, the differences from `pong` are
three, and all three are the same idea: **a game is made of things, not of
robots doing things.**

**It is played on a FIELD.** The whole game is one green rectangle, and the
ball and the bat ride on it as pictures riding on a picture. The table is only
the floor the pitch stands on. So nothing on the table is in the ball's way —
not the instruction pads, not your notebook — and nothing needs clearing away
before you play.

**The ball has a SPEED.** `SpeedToRight=500`, `SpeedToTop=-600` are properties
of the picture in the original file, and they are properties of the pad here.
The ball moves on the world's own clock, smoothly, whether or not any robot is
doing anything — and its robots are left with the only interesting question,
which is what to do when it hits something.

**Collision says which SIDE.** The original's ball carries two robots, both
called *Bounce*, whose thoughts differ only in reading `Right Collide?` versus
`Up Collide?`. Ours differ only in the word they expect in the second hole of
the touching reading.

The ball's whole program is then: whatever you have run into, and whichever
side of you it is on, send yourself the message that turns you away from it —

```
[set | speed | [ 3/5 |     ]]   go right
[set | speed | [-3/5 |     ]]   go left
[set | speed | [     |  1/4]]   come near
[set | speed | [     | -1/4]]   go far
```

An **empty hole leaves that one alone**, which is the whole trick: *go left*
says nothing about up and down, so a ball that bounces off the bat keeps
climbing or falling exactly as it was. No arithmetic, nothing to flip, and
sending the same one twice does no harm — which matters, because a contact
lasts several rounds and the robot acts on every one of them.

Eight robots pick among those four, and a ninth does nothing, because most
rounds there is nothing to do. The bat's robot takes what the pointer just
said, keeps the *away* of it, subtracts the 9/5 that is the distance from the
front of the table to the middle of the field, and posts the difference. That
subtraction is not a workaround: a place is always measured from the middle of
whatever you are standing on, and it is the only sum that follows.

Regenerate with `python make_pong_classic.py`. Measured, driving the frame
clock by hand: a bat kept level with the ball saves it every time and the
counter stays at nought; a bat parked out of the way lets it past, the counter
goes to one, and the ball is served again from the middle. Median frame 1 ms
with both panels running.

**The ball is a real picture**, drawn with alpha so it is round on the green
rather than a green square with a circle in it — `draw_rgba` in
`examples/images/_img.py`, which is the same PNG writer the picture worlds use
with an alpha channel added.

## 🏓 pong-gadgets.world.json

The capstone clause, honoured late: Pong with NO bespoke robots. The ball is
a pad with three shelf gadgets bound to it (bouncing -- both axes since
28 Aug -- reverse on collision, send 1 to the score); the bat is a pad with
following-the-pointer; the score is a live number called "rally". Press SPACE
on the four gadget cards and play with the pointer.

The honest seams are on a card in the world: two bound movers ADD their
steps, and the counter scores hits where classic Pong scores misses. An ASK
MARTY card invites the question the world was built to answer well: "what
does the ball do?"
