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

Twelve gadgets since 28 Aug. The second six (make_library2.py): grow and
shrink when touched (dozing on the touch channel; a hit is [move | size |
1/4]), make a sound on hit (gives "play" to the bell riding in its work
box), reverse on collision (sets the step away from what it hit, like the
ball; edges are bouncing's job — bind both for pong-ball physics), speed
limit (weighs the speed against the limit on a scale — the scale is the if;
born too fast so SPACE alone demonstrates it), and send 1 to the score when
hit (a badged +1 to the score in its work box).

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

**Switching one on folds its panel away.** The robots keep working out of
sight, which is the state a panel already had for a house with work still in
it — six gadgets going at once would otherwise fill the table with trays.
Open a gadget's panel (hold it and press the ⚙ on the holding card) to watch
its robots at work.

**Speed.** A gadget runs a whole robot round per move, so at 1× a step is a
walk across the desk. **Instant** is the speed to watch these at; 8× is a
slideshow of the same thing.

**Enter looks straight at a pad**, filling the screen; **Escape** comes back.
That is how a game on a pad is played — not by holding it, which is for
reading and typing. The camera moves, so everything still works from there —
and while you are playing, the workshop's cards, tooltips, wiggle and pointer
all get out of the way.

**`[set | solid | no]`** makes a thing scenery: everything passes through it.
Solid is the default, because that is what makes a ball bounce off a bat — so
a score riding on the pitch is told otherwise once, and then the ball ignores
it. Holding a pad, **Ctrl with the arrows** sets its width (left/right) and its
height (up/down).

**A pad with behaviours on it is a scene.** SPACE on the pad switches on
everything riding it and `.` stops the lot — so a game is started by pointing
at the pitch, not at a four-millimetre ball.

**A behaviour runs until you switch it off.** There is no Rounds limit any
more, for anything: a finite job ends itself, a room has its lever, and the
bar’s **Pause** button holds the whole world still. And a gadget’s **speed**
waits for its switch too — SPACE starts robots and motion together, `.` stops
both.

**Riders belong to Dusty.** A thing riding on a pad is part of a scene, and a
scene should not come apart by being pointed at: wake **Dusty** and click to
take one off, click what he is holding to get it back, and drop it on the pad
to put it there again.

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

## pong.world.json

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
*away* of it, and send my thing `[set | away | that]`. Its across never
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

## pong-classic.world.json

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


## ellipse.world.json

The thirteenth behaviour, and Stage 6's proof. `moving in an ellipse` keeps an
angle and each round works out

    across = centre + radius x sin(angle)
    away   = centre + radius x cos(angle)
    angle  = angle + 6

Every line is badged numbers dropped on a running total on the scratch spot --
a copy of the angle, then the `sin` badge, then the radius (badged x), then
the centre (badged +). Nothing in it knows what an ellipse is.

It is deliberately NOT on the twelve-shelf, which is capped: it exists to show
that inexact numbers are good enough to draw with. The sines come back marked
`~` to twelve places, and the path measures 2.2 across by 0.8 deep with every
point on the curve.


## turtle.world.json

Logo's turtle, and neither `forward` nor `right` is built in. The turtle keeps
a NEST in its work box -- a letterbox -- and two robots read the top of it,
dispatching on the word in the order:

    [forward | 3/10]   ->  across += n x sin(heading)
                           away   += n x cos(heading)
    [right | 90]       ->  heading += a

Give an order to the bird and she posts it. Heading 0 points AWAY from you;
right turns toward across. A square is forward, right 90, four times -- and a
robot trained to do all four is a Logo program.

It needed Stage 6: facing anything but a right angle takes a sine. And an idle
turtle is genuinely asleep -- an empty nest dozes its whole team, and the
scheduler steps over a sleeping panel until the post arrives. An order posted
to a turtle nobody switched on WAKES it: the letterbox hydrates with its
panel, and the post starts the team.

Since 28 Aug it also draws: post the word "pendown" and every move leaves a
chalk stroke ([set | pen | down] under the hood -- a property of ANY thing,
not a turtle feature); "penup" lifts the chalk. pendown, then
forward/right-90 four times, draws a closed square in four strokes.


## pong-gadgets.world.json

The capstone clause, honoured late: Pong with NO bespoke robots. The ball is
a pad with three shelf gadgets bound to it (bouncing -- both axes since
28 Aug -- reverse on collision, send 1 to the score); the bat is a pad with
following-the-pointer; the score is a live number called "rally". Press SPACE
on the four gadget cards and play with the pointer.

The honest seams are on a card in the world: two bound movers ADD their
steps, and the counter scores hits where classic Pong scores misses. An ASK
MARTY card invites the question the world was built to answer well: "what
does the ball do?"


## The shelf is fifteen (28 Aug)

Three joined it when the gadget-built Pong was actually played:

* **following up and down** (G915) -- the pointer's AWAY only. A bat that
  tracks both axes sits under the cursor: it leaves its lane, and it can
  never be pointed at to be stopped.
* **bouncing at a speed** (G916) -- sets a speed, eats the edge reading, and
  dozes until a wall. The world's clock does the moving.
* **reverse a speed on collision** (G917) -- fills ONE hole of the speed box
  and leaves the other empty, so it shares a thing with G916 without the two
  arguing about the axis neither touched.

The step-based originals stay: same behaviour, two ways. Bind 'bouncing' and
then 'bouncing at a speed' to the same pad and watch which one stutters --
a robot cycle a frame costs about 10ms, a speed costs nothing.


## turtle3d.world.json

The turtle in the air: move, yaw, pitch, roll, home -- the vocabulary every
3D turtle has converged on, borrowed from aeroplanes, and all three turns
about the TURTLE's own axes.

The frame is one quaternion, multiplied and renormalised per turn, so the
turns compose in any order without drift: ninety one-degree yaws land on
exactly the frame of one ninety-degree yaw. That is deliberate -- sequential
Euler updates, which is how most systems do it, would not.

Unlike the flat turtle, the maths is BUILT IN, and a card in the world says
why: a heading is a number you can keep in a hole and see, an orientation is
not.


## ../models/ (29 Aug)

airplane.thing.json and dragonfly.thing.json: MODELS, things built of parts
(box / sphere / cylinder / cone with size, place, turn, colour). Import one
mid-project and it lands in your hand with fresh names; drop the 3D turtle
behaviour on it and it flies. Both face heading zero, so their noses agree
with the turtle frame from the first order.


## zeno.world.json (29 Aug)

Zeno's postman: the halver copies its fraction to the bird and drops a x1/2
badge on what is left; the totaller takes each delivery off the nest and
drops it on the running total (a number dropped on a number ADDS). Pull both
levers. The total is exact -- (2^k - 1)/2^k, readable off the block -- which
is the whole argument for exact rationals in one world.


## airplane-flight.world.json (30 Aug)

The toy airplane takes off, flies and loops. Two behaviours are bound to the
one plane -- the 3D turtle (giving it move/yaw/pitch/roll) and "the pilot"
(which speaks them) -- so one SPACE on the airplane starts both. The pilot has
no counter: its round is `move 10, move 10, pitch 30`, and a constant turn per
constant stride is a circle. Twelve rounds close it. The pen is down, so it
draws its own flight path; the plane starts mid-table because the loop needs a
radius of room behind it as well as in front.
