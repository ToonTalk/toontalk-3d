# The back of things

**Status: designed, not built.** This is the spec settled in conversation
(Ken Kahn and Claude, 21–22 August 2026). DIVERGENCE.md stays the audit of
the original; this file is a design of our own — what replaces the
original's sensor family, and why it is smaller than what it replaces.

## The problem it solves

The original's sensors are live pads that both read and write (a picture's
x position). They are easy to use and easy to understand — and not
user-definable. A child can build a message interface *on top of* sensors,
but cannot give her own abstraction a sensor face: a Logo turtle can accept
`forward` and `turn`, but only the substrate decides what gets to look like
a sensor, and the substrate speaks Cartesian. Sensors also invite the one
race the language otherwise excludes: read x, compute, write x — two robots
doing that interleave, even though each individual update is atomic.

The resolution: **ordinary birds are all we need.** Sensors stop being
primitives and become an idiom — something assembled from parts the
language already has, by anyone, for anything.

## Backs are places

Every thing can be **flipped over**. The back is where its identity and
behaviour live: a little tabletop that travels glued to its thing, on which
the user can lay out, size and label things as they please. A back can hold
**several wall-less houses** — independent robot teams with their boxes and
work areas, each visible at a glance, each vacuumable, none hiding
anything. Houses with walls remain for when hiding is wanted; a back is
glass by default.

(The ancestor is the original ToonTalk's picture backs, which were always
where a picture's behaviour went. We generalise the gesture to every kind
that earns one.)

## Is "the back" the right metaphor?

Raised by Ken, 24 August, and the objection lands. Flipping suits a flat
world: in 2D every thing is a sprite with an unseen reverse side, so "the
back" names a real place that is really hidden. Here nothing has an unseen
side left. A number is a cube whose six faces are all spoken for — the
bottom face carries the continued fraction now — and the back of a house is
an outside wall with a name painted on it. "Flip it over" would collide
with the turning gesture that already exists (arrow keys, while holding),
which shows you MORE faces of the thing, not a different kind of place.

The replacement candidate: a **control panel**. Every thing has one; it
starts out holding only the bird and the event nest, and the user adds
working robots and wall-less houses to it. Some action while holding a
thing releases its panel.

What survives this rename is: everything. The back was never geometrically
a back — it was a place glued to its thing where behaviour lives. The
panel is the same place under an honest name; every semantic in this file
(one message at a time, suspension, echoes, gauges as an idiom) transfers
word for word. What actually changes is the access gesture and the
staging:

- **The gesture.** Three candidates. A button on the *holding card* — the
  card already carries the keyboard and the turning hints, so it is
  discoverable, and it is the only candidate that works identically on a
  tablet. A key, while holding. Or a **mechanic's bench**: one more
  station in the arc, and setting a thing on it slides the panel out —
  which gives the act a place, the way copying has Mimi, at the cost of
  arc space and a walk. The holding-card button is the current favourite;
  the bench could join later without conflict.
- **The staging.** Released, the panel is a tray — set it down anywhere and
  work at it like a small bench. It stays glued to its thing: copy the
  thing and the panel copies, vacuum the thing and the panel goes too.
  Closing it snaps it back inside.
- **The name.** Control panel, the workings, the service hatch — and the
  verb is "open it up", which is what children say about machines. This
  file keeps its name until the choice is built.

## Birds are the whole interface

Flipping a thing yields a **bird addressed to it** — the capability to send
it messages. Messages are ordinary boxes with a selector pad in front:

    [update, x, 100]      [query, y, reply-bird]      [rotate, 30]

Request/reply is the existing idiom (the bank account already does it: put
a reply bird in the box). The thing's back processes **one message at a
time**, so the no-concurrent-side-effects property holds by construction —
not by a special atomicity rule for sensors.

**Unary sugar: operation-numbers travel whole.** A `+10`-badged number
dropped on a live number delivers the *operation*, applied by the owner —
fetch-and-add in a single message. `set 50` is a plain write; `×2` an
atomic scaling. Read-modify-write races cannot exist because the
modification never travels in pieces. The badges were built for arithmetic;
they turn out to be the atomic-RMW message format. The sugar is limited to
one argument — selector boxes are the general form — but a badged number
displays its verb on its face, which is worth a lot at the table.

## Live numbers, and gauges as an idiom

A number's back adds an **event nest** announcing what happens to it:
`[dropped-on-top, bird-to-the-dropped-thing]`, and so on. A number with an
inhabited back is a **live number**: a place with identity, whose current
contents is a value. (The block on the table was always a place you could
retype; flipping makes the place's identity graspable. Matching stays pure
— liveness affects only suspension, never what matches what.)

A **gauge** is then no new kind at all: an ordinary number block, kept
current by a sync robot on its back that watches the picture, made writable
by a controller robot dozing on its event nest that forwards changes to the
picture's bird. The turtle's author exposes `forward`/`turn` — pure turtle
geometry — and *optionally* mints a heading gauge from the same parts.
Cartesian is no longer privileged; it is just the vocabulary the picture's
back happens to speak, wrapped at will. The observe and control halves are
separately handable: a number some robot keeps updated, with no controller
listening, is a read-only view — the capability split falls out of which
robots you deploy.

## Suspension: one rule

> If a mismatch — scale comparisons included — is attributable to a live
> thing, the robot dozes on that thing's events, and the match is retried
> per message.

This **subsumes the covered-nest rule**: a nest in a hole is just a live
thing whose mismatch suspends you until its stream delivers. One rule where
there were two.

The lineage is ask-suspension from concurrent constraint programming — the
bubble is an ask, live numbers are the variables the store knows about,
messages are tells — with one honest disanalogy: the classic store is
monotonic (an entailed ask stays entailed), ours is stateful (an update
replaces, so a condition can hold and later fail). So instead of confluence
we promise two things:

1. **Retry is serialized with the back's message handling.** One message,
   then the waiting matches are retried, then the next message. No robot
   ever matches against a value mid-update.
2. **Round atomicity.** A round begun under a true condition runs to
   completion even if the condition flickers false mid-round. (Both are how
   the engine already treats nests; the spec makes them promises.)

## Copying

Mimi copies the back. Copied robots carry copied birds, and copied birds
already serve the same nests — so **a copied gauge behaves identically and
watches the same subject** purely by existing semantics; no new rule. The
copy's own event nest is fresh: its drops are its own events, so twin
gauges don't fire each other's robots. Modify the copy's back and it
diverges — which is the point.

## Echoes

A two-way gauge is a feedback circuit: drop on the number → controller
updates the picture → picture's change event → sync robot updates the
number → event → controller again. The rule that breaks the loop:

> **An update that does not change the value is not an event.** The back
> swallows it.

Suppression compares the place's stored representation against its own last
value — not across representations — so a conversion wobble between the
picture's storage and the number's can never re-enter the loop.

## Devices

A **Devices notebook** holds event nests for the mouse and keyboard. Take a
copy of a nest and the existing broadcast-group semantics deliver every
event to every subscriber. These are read-only by construction: there is a
nest to copy but no bird to be had — nothing may move the user's mouse.
The observe/control split's first natural appearance.

## Behaviours as things: anima-gadgets

The Playground project (1999–2001) shipped ToonTalk's best answer to "how
does a child reuse behaviour without reading code": **anima-gadgets**.
(Sources, read 24 August 2026: the library's own `behave.tt` notebook, the
archived catalogue at the IOE, and the June 2000 write-up of how to use
them.) An anima-gadget was a picture whose front carried a family of
**behaviours** — purple rectangles — and which **demonstrated itself**: set
it on the floor, switch it on, and watch what each behaviour does to it.
"By observing the behaviour in action (or, with practice, simply by
reading the image)" you find the one you want — the catalogue was legible
by watching, not by reading. Each behaviour's back held the robots that
did the work, plus text labels that **spoke when pointed at**. To use one:
take the rectangle, flip your butterfly over, put the behaviour on its
back. The butterfly is ready.

The catalogue is worth keeping whole, as the target library. Start moving
(up, right, down, left); movement shapes (ellipse, square, random); move
with arrow keys, with shift-and-control, in diagonals; move with the
mouse (up-and-down, left-and-right, both); move with the joystick; bounce
off other things, bounce off edges, wrap at edges; jump and make a sound
when touched, jump on click; stop at edges, stop at barriers; shoot on
click, in four directions, on the trigger; I destroy anything that
touches me, I destroy myself when touched (each with or without an
animation); grow when touched, shrink when touched; change colour or
picture when touched; make a sound on hit, on click, on any key; add
numbers or letters together when they touch; scoring (send a message to
the score when hit, add to the score, reset the score); make something
appear on touch. And from `behave.tt` itself: bounce to stay on screen,
jump and make sound on collision, tend towards a static goal, tend
towards a moving goal, reverse on collision, a speed limit, broadcast
position.

Here a behaviour is an ordinary thing whose **panel carries robots** —
robots that speak about "my thing" the way a robot already speaks about
"hole 1 of what I was given". What makes reuse work is the binding rule
(Ken's, 24 August):

- **Panel on panel.** Place a control panel on a control panel, and the
  inner panel's robots now control the *outer panel's object*. The
  behaviour was written against its own thing; landing on the butterfly's
  panel re-points that one reference at the butterfly. Nothing inside the
  behaviour is edited — the binding is the only thing that moves.
- **Object on a control.** Drop a whole object onto a behaviour and the
  same wiring happens from the other side: the behaviour's panel becomes
  a sub-panel of the object's panel, and its controlled-object is
  re-assigned to the newcomer. Either direction of the gesture, same
  result.

Self-demonstration then costs nothing, because it is not a demo mode: an
unattached behaviour's "my thing" is *itself*, so a Bounce gadget set on
the table bounces, and a Grow-when-touched gadget grows when you touch
it. The anima-gadgets house — a floor of gadgets, each doing its thing —
is just a room of things whose bindings have not been given away yet.

The speaking labels come almost free: the hint voice already exists and
is already a per-user setting, so a control that says its name when
pointed at is the same machinery aimed at a smaller target.

## Inexact numbers

Trigonometry and non-integer powers arrive with pictures (rotation demands
them). The design is the Scheme lineage: **a rational plus an exactness
flag**, with contagion — exact op exact is exact, except operations inexact
by nature (trig, non-integer powers); anything touching inexact is inexact.

- Inexact results are computed to a **fixed, documented precision** and
  stored as the rational approximation. Slower than floats, but
  deterministic across machines — which matters for echo suppression, for
  replay, and for headless verification. Floats may become an internal
  optimisation later, behind the same flag.
- **Identity is untouched** — identity lives in the back, not the value —
  and equality remains decidable representation-equality, so echo
  suppression is unaffected.
- **Inexact numbers must look slightly different**, at a glance, on the
  block itself. The exact look is open; a candidate is a wavy fraction bar
  or an `≈` mark. The trailing ellipsis is already taken (digits that don't
  fit) and must not be overloaded.

## Imported things, and one way in

The workshop already takes things from outside: **Import file** and a drop on
the page both accept a saved thing or a saved world. That door should widen to
**any medium** rather than grow a second door beside it. Drop a `.png` and a
picture lands in your hand; a `.glb` and a model does; an `.mp3`, a sound; a
`.world.json`, the world it always did. One gesture, sorted by what arrived —
and the file picker's `accept` list is then the honest statement of what the
workshop can hold.

That matters more than it sounds. A child who has learnt that *everything* is
a thing you can hold, name, file in the notebook, put in a box, give to a bird
and hand to a robot should not meet a second, separate mechanism the first time
they want a photograph in their program.

### Pictures, and the flatness problem

A picture is two-dimensional and the workshop is not, and the awkwardness
is real. The trade has four standard answers. **Billboards** (sprites): the
image swivels to always face the camera — the particle-and-label trick,
legible from anywhere, but a thing that turns to face you refuses to be a
thing: it has no footprint, no edge, no side you can fail to see.
**Cards**: a textured plane standing in the world like a poster or a
painting — honest presence, but edge-on it vanishes to a line, and flat on
a table it is unhittable from most camera angles. **Floating panels** (the
VR answer, Quest and visionOS): a window hanging in space with a backing
plate, which is a billboard wearing a suit. **Decals**: images projected
onto surfaces — right for marks, wrong for things.

The workshop has already answered this once, for text. A pad is not a
plane; it is a **tablet** — flat but with thickness and an edge, lying on
the table the way paper actually lies, picked up, and rolled upright in
the hand by the turning gesture so it can be read. A picture is the same
object with an image where the writing goes: a **photograph**. It lies
flat, files in the notebook, sits in a box hole, weighs on a scale — it is
exactly as awkward as a pad, which is to say the awkwardness is already
solved and already familiar. Its verbs are the original's (position,
width, height); its panel carries the bird they go to.

**Video is a picture that plays.** The same tablet with `[play]`,
`[pause]`, `[seek, 30]`, and `[finished]` on its event nest — a living
photograph. The sound should come *from the pad*: positional audio, so a
video playing across the table is quieter than one in your hand. The
alternative staging — a little TV prop with the video on its screen — buys
charm at the cost of a new kind; a child who wants a TV can drop the video
pad onto a model of one.

### Pads, generalised

The moment a pad can carry an image, "text pad" is the wrong name: they
are **pads**, and writing was only ever one of the things you could put
on one. (Ken, 24 August — the rename should reach the manual, the
tooltips and Marty's briefing when this is built.)

How an image gets onto a pad — three doors, none of them new machinery:

- the pad's panel carries an **import button**, and
- the panel **receives drops** — the one file-door of this section, scoped
  to a single thing; and
- **paste, while holding**: hold a pad, paste an image, and the image
  covers the pad. Typing already routes to the held thing (that is how
  tablets write on pads); paste is the same route carrying a picture.

**Sub-pads.** A pad can hold pads, their coordinates **relative to the
containing pad**. That is scene-building: Pong's field is a pad, the
paddles and the ball are sub-pads, and each sub-pad's panel carries its
behaviours. Move the field and the game moves with it; file the field in
the notebook and the whole game is one entry. (The original's pictures
nested exactly this way — a picture on a picture lived in the parent's
frame.) The `position`, `width` and `height` messages then mean *within
my parent*, which is also what the original meant by them.

### Sounds: files, made, and remade

A sound file becomes a block like anything else — its top face a waveform,
since a sound has no look of its own. `[play]` by bird, or click it; its
event nest says `[finished]`.

Two more doors open at once, and neither needs a new mechanism:

**Made sounds.** The workshop's own effects are synthesized — an
oscillator and an envelope, not samples — so the machinery already exists.
The child-facing mint is a box, `[frequency, duration, shape]`, handed
over and answered with a sound block. A robot that builds such boxes and
sends them is an instrument; a robot that computes the frequencies is a
composer. (Where the mint lives — a machine in the arc, or a page of the
Devices notebook — is open below.)

**Remade sounds.** The badge gesture generalises to a new medium, which is
the whole workshop bet in miniature. A `×2` dropped on a sound plays it at
double speed; `×1/2` stretches it; `×(−1)` plays it backwards — negation
reading naturally as time's arrow. Addition has no obvious meaning on a
sound and is refused rather than invented. And the pads' own edge-drop
carries over: drop a sound on the *edge* of another and they concatenate,
first-then-second, exactly as "Toon" and "Talk" join — a melody is built
the way a word is. Transformations that need parameters (echo, muffle,
pitch without speed) are panel messages rather than badges.

### Models

A model is the case that pays for the whole design, because it is the first
thing whose back has genuinely interesting verbs. It arrives as a `.glb` —
the format the workshop's own characters already are — and becomes a thing:
holdable, copyable, fileable, droppable into a box or a room.

Its back carries a bird, and the messages are boxes with a selector pad:

    [turn, y, 30]            a rotation, in degrees, about one axis
    [move, x, 1.5]           the same shape as a picture's move
    [scale, 2]               bigger, uniformly
    [go to, x, 1, y, 0, z, 2]   somewhere, in one message
    [play, "walk"]           an animation clip the file already carries
    [stop]
    [query, y, reply-bird]   as everywhere else: put a bird in and wait
    [parts, reply-bird]      the named nodes, as a box of text pads

Three notes on the shape of that list.

**`play` is what a model has and a picture has not.** A `.glb` may carry
animation clips by name, and naming one is the whole interface — no timeline,
no keyframes. `[parts, reply-bird]` answers with the names inside the file, so
a child can find out what a model will answer to by asking it, rather than
being told.

**Rotation needs an axis, and that is a hole, not a new kind.** `[turn, y, 30]`
is the same selector-box idiom as everything else, and `y` is an ordinary text
pad. Nothing here needs a new sort of thing to exist.

**Gauges fall out unchanged.** A heading gauge for a model is the same idiom
as for a picture: a live number kept current by a sync robot watching the
model, made writable by a controller dozing on its event nest. The model's
author exposes `turn` and `play`; whether anybody mints a gauge from them is
somebody else's choice, later.

The event nest on a model's back announces what a model can notice —
`[dropped-on-top, bird]`, `[clicked, bird]`, `[finished, "walk"]` when a clip
ends. That last one is what makes a sequence of animations expressible without
a clock.

**Movability is declared in the file, four ways.** A `.glb` carries a tree
of **named nodes**, and every named part can be turned, moved and scaled on
its own — this is how the workshop's own robot walks: its elbows and knees
are just named nodes this code rotates. It may carry **skins**: skeletons
of named joints that deform a mesh. It may carry **morph targets**: named
sliders from 0 to 1 — a "smile", a "blink". And it may carry **animation
clips**: canned motions with names. All four are data in the file, which
means:

**The bird API is generated by reading the file.** At import the workshop
walks what actually arrived: clip names become the vocabulary of `[play,
…]`, node and joint names become `[turn, "LeftArm", y, 30]`, morph names
become `[set, "smile", 0.8]`, and `[parts, reply-bird]` answers with this
model's own words rather than any fixed list. Two honest caveats. Names
are whatever the author typed — a well-made model answers to "LeftArm", a
careless one to "Cube.003" — so the panel should display the vocabulary it
found, teaching the child what this model calls its own parts. And the
format declares no limits: nothing in the file says an elbow bends only
one way, so playing a clip is always safe but free posing can fold a model
through itself. At-your-own-risk — which in a workshop is a feature.

### What this costs

Import-by-medium and models are **+1–2 days** on top of the estimate below, and
they depend on backs and live numbers being there first — the bird and the
event nest are the whole interface, so there is nothing to build until those
exist. Sounds share almost all of it: a sound is a model with fewer
verbs, and made-and-remade sounds ride gestures that already exist — the
badge drop and the edge drop — for about another half day.

## Where the work happens

Ken's question, 24 August: should this be built under a new file name, so
the released `toontalk-3d.html` is untouched? The cost to weigh is the
fork: two 11,000-line files diverging across a week-long epic means every
unrelated bug fix ports twice, by hand. The alternative that buys the
same safety for nothing: **snapshot the release** — copy the current
file to `toontalk-3d-v1.html` and let `index.html` point at the snapshot
until the epic settles — and keep developing in the canonical file, held
honest by the byte-identical regression harness that already guards every
commit. The snapshot never changes, so it costs nothing to maintain, and
the canonical file keeps a single history. Decision deferred until
building starts.

## How much work

Estimated at the pace this project has actually run (the engine/view split
was a day; Marty was a day):

1. **Backs as places** — flip gesture, the back as a mounted world context
   (the room machinery reused without the room), layout/labels,
   save-format v3: **1–2 days**.
2. **Live numbers, events, suspension** — event nests, echo suppression,
   generalising mismatch-attribution to register waiters on live things
   (`mismatchPaths` already computes the failing paths): **~2 days**, the
   smallest code and the deepest semantics — test-heavy.
3. **Pictures** — import, a new thing kind, the verb vocabulary, back with
   bird: **1–2 days**. Sub-pads (relative coordinates, scene-building):
   **+half a day**. Sounds, made and remade: **+1–1.5 days**. Video:
   later.
4. **Behaviours / anima-gadgets** — the binding rule is small once panels
   exist (**~1 day**); the library is the real work and grows forever —
   the first dozen behaviours perhaps **1–2 days**, and they double as the
   test suite for everything above them.
5. **Devices notebook** — **half a day to a day**.
6. **Inexact numbers** — flag, contagion, fixed-precision trig/powers,
   the visual marker: **1–2 days**.

Total: **roughly 8–12 working days**, comparable to the rooms-and-engine
epic. Natural order: 1–2 first (the semantics), 3 second (the payoff),
4 third (the library that makes it sing), 5–6 after.

## Alternatives considered

- **Primitive sensors** (the original's): easiest to use, not
  user-definable, and they privilege the substrate's geometry. Superseded:
  the system's x/y sensors become gauges the system happened to mint — the
  same mechanism users get.
- **Glass nests + a gauge press** (earlier in this design conversation): a
  new kind of nest (replace-don't-stack, copy-don't-take) plus a machine to
  mint gauges. Everything it did reappears without the new kind:
  replace-don't-stack (a number *is* its latest value), wake-on-change (the
  suspension rule), multi-watcher (nest broadcast groups). Dropped.

## Open questions

- Dice backs. A die-drop is already `[add, random 1..6]` delivered whole,
  so nothing needs rescuing; whether dice grow backs (weighted dice, more
  faces of behaviour) — later.
- Boxes and robots as actors. A bird-to-a-box is a serialized shared array;
  a bird-to-a-robot is remote control. Doors deliberately not yet opened.
- Keyboard focus.
- The precision constant for inexact computation.
- Pictures' full verb vocabulary, and how far a model's differs from it.
- Whether an imported model's own node names are worth exposing as things
  in their own right (a robot could then hold an arm), or whether `parts`
  answering with pads is enough.
- What a dropped file that the workshop cannot read should do. Refusing it
  is easy; saying what it *would* have taken is the kind thing.
- What a live number shows before its first delivery.
- The exact look of inexact numbers (that they look different is settled).
- The panel-release gesture: holding-card button, a key, a mechanic's
  bench — or more than one of them.
- The name itself: back, control panel, the workings — and whether this
  file is renamed with it.
- Whether sound in the world is positional (a video across the table is
  quieter than one in your hand) or flat.
- Where made sounds are minted: a machine in the arc, or a page of the
  Devices notebook.
- Whether `×(−1)` playing a sound backwards is delight or confusion.
- Whether both directions of the gadget gesture ship (panel-on-panel and
  object-on-control), or one is enough to start.
- What an unattached behaviour's self-demonstration bumps into — does
  Bounce bounce off the workshop's own furniture, or only off the edges
  of the pad it sits on?
- Whether a behaviour's robots may also read the Devices notebook
  directly (move-with-mouse needs the mouse), or only their thing's own
  events.
