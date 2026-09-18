# The back of things

**Status: built, and still growing.** The first sections are the spec
settled in conversation (Ken Kahn and Claude, 21–24 August 2026); the dated
sections after them are the record of every round since — what Ken
reported, what was measured, what changed. The manual (`manual.html`)
describes the workshop as it is now; this file keeps the history and the
reasons. DIVERGENCE.md stays the audit of the original; the design here is
our own — what replaces the original's sensor family, and why it is
smaller than what it replaces.

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

The replacement: a **panel** — decided, 24 August. Every thing has one;
it starts out holding only the bird and the event nest, and the user adds
working robots and wall-less houses to it. The release gesture is also
decided: a button on the holding card, plus a key.

What survives this rename is: everything. The back was never geometrically
a back — it was a place glued to its thing where behaviour lives. The
panel is the same place under an honest name; every semantic in this file
(one message at a time, suspension, echoes, gauges as an idiom) transfers
word for word. What actually changes is the access gesture and the
staging:

- **The gesture — decided.** A button on the *holding card* (the card
  already carries the keyboard and the turning hints, so it is
  discoverable, and it works identically on a tablet), plus a key while
  holding. The third candidate, a **mechanic's bench** in the arc, is not
  ruled out — it could join later without conflict.
- **The staging.** Released, the panel is a tray — set it down anywhere and
  work at it like a small bench. It stays glued to its thing: copy the
  thing and the panel copies, vacuum the thing and the panel goes too.
  Closing it snaps it back inside.
- **The name — decided: "panel".** The verb is "open it up". This file
  keeps its historical name; the app's strings say panel.

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

## The info notebook: documentation you can copy

How does anyone learn what boxes a bird will accept? The answer should not
be a manual page about the workshop — it should be the workshop's own
gesture. **A panel's documentation is a notebook**, and notebooks already
have the right property: what you take from a page is a *copy*. So the
docs are pages of **live example boxes** — take one out, edit the numbers,
give it to the bird. Documentation that can be copied and run is hard to
leave rotten -- a stale example fails in your hands rather than in prose --
and cannot be misread, because the example IS the format.

The page layout is Miki's, from the anima-gadgets notebook of 1999: pairs
of pages, a text page on the left describing, the thing itself on the
facing page. Here the left page says what the box does and the right page
holds the example box; receive-pages (what the event nest will deliver)
are marked as arriving rather than sendable.

- **One button, not two.** The panel gets a single ℹ️ button opening the
  thing's info notebook, with a title page for each direction — "what you
  can send" (the bird) and "what it will tell you" (the nest). Two
  buttons on a small tray is clutter; the directions are pages, not
  places. (Open below if use proves otherwise.)
- **Built-in kinds** get authored notebooks, written once.
- **Imported models** get theirs *generated from the file*, exactly as the
  API is: each clip a page with a ready `[play, "walk"]` box, each named
  part a page with a `[turn, "LeftArm", y, 30]` box, the example names
  being the model's real ones.
- **User-built panels** get an empty info notebook that the author fills
  by the ordinary gesture — file an example box in it. Documentation is
  user-extensible with the same move as everything else, which also means
  a child can document her own gadget the way the library documents
  itself.

## Live numbers, and gauges as an idiom

**Revised in building (Ken, 25 August): event nests are obtained, not
furnished.** The panel carries only the thing's bird; `[listen |
reply-bird]` given to the bird answers with an event nest — you subscribe,
as with an event listener. The shape leaves room for specialized channels:
an image's bird will take `[listen | position | reply-bird]`, and a number,
having one channel, refuses any named one with a pointer to pictures. This
also keeps a panel's face quiet: a thing that nobody listens to carries no
nest filling with history.

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

## Native panels: extending the workshop from JavaScript

The Devices notebook is secretly the first instance of a general shape: a
thing whose panel is implemented *in JavaScript* rather than in robots —
events fed to a nest by code, messages to its bird handled by code. Ken's
ask (24 August): a user who wants some browser API — speech, MIDI, the
camera, geolocation, a gamepad — should be able to wrap it as something
loadable into the workshop: at minimum a bird-and-nest to the API,
ideally a full anima-gadget with an info notebook.

The natural contract is small: a loaded module declares a name, a handler
for boxes sent to its bird, and a way to post boxes to its nest — the
same two directions every panel has. Everything else (what it looks like,
its info notebook, behaviours built on top) is ordinary workshop material
that ships alongside in the same file.

Deliberately not designed yet: **the safety story**. Loading JavaScript
is running JavaScript, and a file traded between children must not be a
trap. Options run from honest scariness (a warning dialog naming what the
module asked for) to real sandboxing (an iframe or worker with a message
bridge, which the bird/nest shape happens to fit perfectly — a sandboxed
native panel is just a panel whose messages cross a postMessage boundary).
The bridge design makes this a candidate for AFTER the epic, not in it.

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

One warning in the 2000 write-up earns a design rule here. Copying a
behaviour with the magic wand came with the caution to get "the entire
purple rectangle shown" — because a behaviour was visually a *composite*
(a carrier picture with graphics riding on it), and a wand aimed at a
fragment copied artwork without the robots. The lesson: **a behaviour
must be one thing.** Here a behaviour is a single pad whose panel holds
its robots, so Mimi copies all of it or none of it; there must never be a
way to take home half a gadget. (Sub-pads reopen exactly this trap —
clicking a sub-pad naturally means the sub-pad — so a gadget's artwork
should be *faces of one pad*, not loose sub-pads riding on it.)

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
the canonical file keeps a single history. **Decided 24 August** — the
snapshot is taken, and the build order, checkpoints and ground rules live
in `PLAN.md`.

## How much work

Estimated at the pace this project has actually run (the engine/view split
was a day; Marty was a day):

1. **Backs as places** — flip gesture, the back as a mounted world context
   (the room machinery reused without the room), layout/labels,
   save-format v4 (v3 was taken by the pad-training fix): **1–2 days**.
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
- Whether one info button serves both directions, or use shows that
  send-docs and receive-docs want separate doors.
- Whether generated model docs show every named node (a rigged model can
  have hundreds) or a curated page per clip plus a parts index.
- The native-panel safety story: warning dialog, or a postMessage
  sandbox — and whether a native panel may be filed in a notebook and
  travel inside a world file.

## The look of a thing, as data

*Added 25 Aug, at Ken's insistence that captioning a picture by typing on it
"feels too special purpose".*

How a pad or a number is painted is not a property of the app, it is a
property of the thing, and it is ordinary data:

```
[set | background | grey]     the paper           pad, number
[set | colour     | white]    the writing         pad, number
[set | font       | sans]     serif sans mono round
[set | width      | 2]        in pad-widths       pad
[set | height     | 1/3]      likewise            pad
```

sent to the thing's own bird, in the same grammar as `[query | bird]` and
`[listen | bird]`. Each one is a real box on a page of the thing's info
notebook.

The consequence is the point. A LABEL — grey paper, white writing, wide and
short — stops being a feature and becomes four messages, which means a robot
can be trained to make one, which means a program can label every picture it
meets. That is the difference between a workshop that has captions and a
workshop in which captions can be *built*.

**Still to come.** Alignment and padding; a border colour and width of its
own; a `[query | look | bird]` so a robot can read a thing's appearance as
well as write it; the same treatment for boxes, scales and sounds (a sound's
waveform screen is already a canvas that could take a colour). And the harder
one: a picture pad's image as a settable property, so a robot can put a
picture on a pad it was handed rather than only on one it was shown.

## Three things Pong broke, and what they mean

*Added 26 Aug, building the capstone. None of them was about Pong; all three
were measured rather than reasoned about, and all three are the sort of bug
only a program that runs every frame can find.*

### The `touch` reading

`touch` began as an event: a bird arrives when you run into something. That is
unusable, and for the reason the `edge` reading already had written on it — an
event leaves the nest **empty** almost always, a team member facing an empty
nest **dozes**, and a dozing member stops the whole team, *including the member
that does the moving*. So a ball that bounces off a bat could not be written at
all.

It is a reading now, exactly like `edge` and `position`: the nest holds one
thing at all times — a live bird to whatever is against it, or a pad saying
`nothing`. And it is swept **every frame**, not sixteen times a second: a
behaviour takes a round a frame, so a reading refreshed more slowly is a
reading the robot sees several rounds running, and a ball told several times
over that it has just hit the bat turns round several times over, in front of
the bat.

A folded panel is a bench thing too, so switched-on behaviours had invisible
trays sitting on the table for the ball to bounce off. The sweep now asks for
things you can *see*, standing on the table.

### Auto-run belongs to the table

Mail landing on a nest inside the standing robot's own given sets
`autoRunArmed`, and `afterQueue` spends the flag by running the robot again.
On the table that is right: a robot dozing over a mismatch should get to work
when the post arrives.

Inside a room or a panel it is a catastrophe. A behaviour whose work box holds
a reading gets mail every round, so every round armed another — and the extra
round ran from inside the first round's own `drainQueue`, outside the room
scheduler, outside the `Rounds` limit and outside the frame budget. **Measured:
594 extra rounds in a single frame; sixteen seconds of one frame.** That is
exactly what "it freezes for about a second" looks like from the outside.

A robot in a room is driven by the room scheduler — one round a turn for a
panel — and is woken from a doze by `checkWaiting`, which is called two lines
above. It needs no second engine. Arming is now `!offstage()`.

*This moved one golden.* `examples/n-to-1` used to record **eleven** trailing
end-markers after eight rounds and now records **three**: the extra eight were
rounds the room was taking that nobody had asked it for. The answer itself —
1, 2, 3, 4, 5 and the end — is unchanged, and the other twelve worlds are
byte-identical.

### What `edge` means

`placeThing` clamped with a strict `>`, so only the move that was *refused*
reported `right`. A round sends two messages — the across step and the away
step — and the second one asks for a position the first already clamped to, so
it is not refused, so it reports `none`. The reading was back to `none` before
the round that would have acted on it began: **a robot whose thought asks for
the right-hand wall never once saw it.**

`>=` now. The edge says where a thing *is*, not what was refused — a thing
resting against a wall reads that wall for as long as it rests there.

### And one that is still there

A round makes canvases: message boxes get copied, readings get built, numbers
get painted. With both of Pong's panels running that is about **47 canvases a
frame**, and roughly once in eight hundred frames the browser stops for
~850 ms to sweep them up. Removing the thought-bubble rebuild for robots
nobody is watching (offstage, or Instant — the same condition
`showTriedAndFailed` already used) took seventeen of them off every round and
halved the spike. The rest is inherent to things being real objects; a canvas
pool for pads and numbers is the real fix, and it is a day's work on its own.


## A pad can be a field, and a thing can have a speed

*Added 26 Aug, after Ken sent the original Pong and asked for one like it.
Three capabilities came out of reading that file, and none of them is about
Pong.*

### Where a thing is, when it is standing on another thing

Only a thing on the TABLE had a place. But a thing riding on a pad already
carried `{u, v}` — where it sits, in fractions of the pad's face — so it had a
place all along; it just could not say so. Now it can, and it says so in the
**same steps the table uses**, so a behaviour trained on the table works
unchanged on a field, and *the edge* means the edge of whatever you are
standing on.

That one sentence is what makes a game rather than a demonstration possible.
The workshop's table is the floor; a **field** is a pitch you put down on it,
and what is on the floor is not in the way of what is on the pitch.

It also turned up an old bug on the way: `padFaceSize` read `sz` and the
picture's aspect and ignored the appearance API, so anything riding on a pad
that had been *told* its width and height was laid out against the wrong
rectangle.

### How fast it is going

```
[set   | speed | [across | away]]     an empty hole leaves that one alone
[move  | speed | [across | away]]     add to what it is doing
[query | speed | bird]
```

A thing with a speed moves on the world's own clock. This is the original's
model — `SpeedToRight` and `SpeedToTop` are properties of a picture in
`pong.tt` — and it changes what robots are FOR. They stop being responsible for
moving anything and are left with the only interesting question: what to do
when it hits something.

The empty-hole rule is the part worth keeping. Turning a ball round is then one
message with no arithmetic in it, and sending it twice does no harm — which
matters, because a contact lasts several rounds.

### Which side it hit

The touching reading was *what I ran into*. The only possible response to that
is to turn round in one fixed direction, so a ball that met the flat of a wide
pad slid along it turning round every round — which is exactly what Ken
reported. It is a box of two now:

```
[ a bird to what I ran into | which side of me it is on ]
[ nothing                   | none                      ]
```

The original had the same answer, and had it in 1999: not one collide sensor
but two, `Right Collide?` and `Up Collide?`, with a Bounce robot each.

### And the thing that was making everything slow

While measuring the above: **thought bubbles, built for robots nobody can
see.** A bubble is real geometry with a painted canvas for every part of the
thought, and a behaviour takes a round every frame. The winner's bubble, the
queue of losers' mini-bubbles, and the rebuild at the end of every run were
being made and thrown away sixty times a second inside a folded panel.

Measured on the classic Pong ball, with two panels running: **52 canvases and
36 ms a frame before, 0.2 canvases and 1 ms after.** The guard is the same one
`showTriedAndFailed` already used — *is anybody watching* — and the answer
inside a panel is always no.


## Rounds is for a robot you handed a box to, not for a ticker

*Added 26 Aug. Ken reported three things about the classic Pong -- the ball
hugged the near wall instead of bouncing, it stopped in the corner, and the
paddle never moved. All three were one thing, and the one thing was a number.*

**Rounds** defaults to 100 and the control's ceiling is 10000. A behaviour
takes a round every frame, so a switched-on gadget stopped after a hundred
frames: **under two seconds**. The ball then went on moving, because with a
speed it needs no robot for that, and with nobody left to turn it round it ran
into the near wall, slid along it and parked in the corner. The bat stopped in
the same second.

Rounds is the right idea for a robot you have *handed a box to*: it is the
brake on a loop whose condition never fails, and its own message says so --
"Stopped after N rounds, the Rounds limit, not its condition". It is the wrong
idea for a ticker. A behaviour is switched on with **SPACE** and off with
**"."**, and that is the whole of its life. Counting its heartbeats against the
same number as a factorial is a trap with a two-second fuse.

A panel's *turn* is still one round. The count of them is no longer held
against it.

Two smaller things came out of the same report:

- **Holding something stopped every behaviour on the table.** The frame loop
  ran rooms only when the outer world was completely still, and `!held` was one
  of the conditions. That is the same mistake as freezing the workshop while a
  robot runs, which Ken had already had corrected once; it makes a game
  unplayable the moment you reach for anything. Gone.

- **A stale `__running` flag stranded a panel for good.** A turn cannot outlive
  the frame it began in, so a panel still claiming to be running from an
  earlier frame has had its turn interrupted -- and the flag is now cleared
  rather than leaving the behaviour dead until a reload.

## Things riding on a pad belong to Dusty

*Same round. "I was able to pick up the ball and paddle (only Dusty should be
able to remove them) but then dropping them back on the green pad did not
restore them."*

Both halves were true, and the second one was the interesting one.

A rider was an ordinary click-to-lift thing, so a scene came apart by being
pointed at. In ToonTalk you take a picture off a picture with **Dusty**, and
that is how you take one off here now. Pointing still finds it -- the tooltip
and SPACE both need to.

And putting it back was refused by a rule that was put there on purpose: **a
behaviour dropped on a thing BINDS**, asked before any other rule, "because a
behaviour is a pad, and a pad landing on a pad would ride there instead, which
is the one thing a behaviour must never quietly do." Pong's ball is both at
once -- a behaviour, and something that rides.

The tie cannot be broken by looking at the two things, because both readings
are legitimate. It can be broken by looking at **where the thing came from**:
something that has just been taken off a pad is going back to riding on it.
`detach` now records that, which also means **put-it-back** (Ctrl+B) works for
riders, which it never did.


## Rounds is gone; one Pause button remains

*Added 26 Aug, at Ken's direction: "get rid of the maximum rounds and replace
it with a toggle for pause/resume everything."*

The Rounds box is out of the bar and the ceiling is out of the engine
(`maxIter` defaults to Infinity; tests still set a finite limit through
`__nano.rounds()`, which is what keeps their dumps finite). In its place:
**⏸ Pause** — one button that holds the whole world still, mid-stride, and
lets it all carry on exactly from there.

The replacements were there all along, and every RUN pad in `examples/` now
says the true thing about how its own run ends:

- a **finite job ends itself** — the condition stops matching, or the robot
  dozes on an empty nest (n-to-1, append, factorial, melody, naming, keys,
  pointer…);
- a **room** has its lever — the tap on an infinite stream (the infinity
  activities, the grammar rooms);
- a **behaviour** has SPACE and "." — and no number in a box ever stops it
  again;
- and **everything at once** has Pause.

## The ball was moving before anybody switched it on

Ken watched the classic Pong ball drift across the pitch, hug the near wall,
and park in the corner — with the paddle never moving. Two causes, and the
first was a design fault, not a bug: **the ball's speed came alive at load**,
before any robot was awake to turn it. Now a gadget's speed is part of its
behaviour — SPACE starts the whole thing, robots and motion together, and "."
stops the whole thing. A plain thing with a speed has no switch, so a speed a
robot gives it acts at once, as before.

The second cause was Rounds (above): even switched on, both panels died after
a hundred frames — under two seconds — which is also why the paddle "never"
moved.

### And a confession from the harness

Every headless verification of the last two days called
`__nano.speed('instant')` — which set the global speed to the **string**
`'instant'`, not Infinity. The old test-frame driver papered over it by
calling the engine parts directly, so "verified at Instant" was verifying a
path no user ever runs. Two fixes: the speed hook now accepts `'instant'`,
`'inf'` and `Infinity`; and `__nano.frame()` is now a copy of the animation
loop's own body, **gates included** — `worldReady`, `simPaused`, `busy`,
queue, mode — so a bug in the gates must fail in the tests too. Under the
faithful driver: the classic ball stands still until SPACE, bounces
continuously for 700+ frames with no Rounds set, misses count and re-serve,
"." freezes it, Pause holds everything and Run releases it.

## Dropped mid-pad it rides; on the edge it binds

Ken, on the put-back rule: "I'm not sure I understand the problem… A user
might develop them independently and then add them to a picture pad." He is
right, and the fix is to stop treating riding as a special case. A behaviour
dropped on another pad honestly means one of two things, and the pad's own
zones — the same zones that already decide join-versus-ride for plain pads —
say which:

- the **middle** takes it aboard as part of the scene (Ken's ball, added to
  the pitch he built);
- the **edges**, and anything that is not a pad, **bind** — the gadget's bird
  is re-pointed and nothing else changes.

A thing taken off a pad still goes back to riding wherever on that pad you
drop it, edge or middle — what it was doing a moment ago outranks the zones.

## The stripes on the paddle

Z-fighting: a flat rider lying flush on a big flat field, at a glancing
camera angle. Riders now sit three millimetres prouder and their faces pull
toward the camera in the depth buffer (`polygonOffset`), and a pad that
carries riders no longer paints “(blank)” under them.

## Set speed, and gauges — to return to

Ken: "Regarding set speed was this a primitive in ToonTalk?" It was —
`SpeedToRight` and `SpeedToTop` are properties of the picture in `pong.tt`,
read and written through sensors. Whether ToonTalk 3D needs it as a primitive
is deliberately left open: it buys motion that does not depend on how often a
robot gets a turn, at the price of a second way for a thing to move.

And the sharper follow-up, also his: **could speed gauges be user-built** — a
gauge object wired to a thing's speed the way the original's sensors were
wired to a picture's properties — and then used inside the ball, so that
"the ball's speed" is something a child can pick up, look at, and hand to a
robot? That is the direction that would make `set speed` not a primitive but
a convenience over sensors. To discuss before Stage 6 commits anything.


## The keyboard belonged to the last button you pressed

*Added 26 Aug. Ken: "When I load classic Pong and point to it and press space
the open file dialog appears... And if the last click was run/pause then a
space toggles that button."*

He loaded the world with **Import file**. A browser leaves a clicked button
focused, and space on a focused button activates it — so his next space went
to Import, not to the ball. The same was true of Pause, and has always been
true of Speed and Save. SPACE and "." are the workshop's own keys, and they
were being eaten by whatever the user last pressed.

There was half a guard for it already: clicking the **canvas** took the
keyboard back. But *pointing at a thing and pressing a key involves no click
at all* — which is precisely the gesture the whole space convention rests on,
so the guard never once fired where it mattered.

Two rules now:

- **A button hands the keyboard back as soon as its own click handler is
  done.** Captured (so a handler that stops propagation cannot escape it),
  deferred by a tick (so the handler runs first), and only if the button still
  holds focus afterwards — `#heldKeys` deliberately passes focus to the typing
  surface, and that must stand. Skipped when `e.detail` is 0, so tabbing to a
  button and pressing Enter still leaves the keyboard where it was.

- **While you are genuinely typing in a field, the workshop keeps its hands
  off.** The global keydown handler returns early for `INPUT`, `TEXTAREA`,
  `SELECT` and contenteditable — with the on-screen keyboard exempted, since
  it is a typing surface that exists to feed the workshop and handles its own
  keys.

Worth noting what this was hiding: every symptom Ken reported for two rounds
running — "the paddle never moved", "I still can't start it" — was consistent
with the behaviours being broken, and twice they were. This time they were
fine and the key never reached them.


## A scene starts and stops as one

*Added 26 Aug. Ken: "typing space to the game should start up all its parts.
And '.' should stop them."*

A pad with things riding on it is a **scene**, and the scene is what a child
points at — not the ball, which is four millimetres of rainbow. SPACE on a pad
now switches on every behaviour standing on it, all the way down, and "."
stops the lot. A lone behaviour is unchanged and still says its own piece.

The pitch also wears its name now, which turned up a second thing: a plaque on
a big pad stood in the middle of it, in front of the game being played there.
Nests had this solved already — flat, just past the near edge, like a museum
label — and a field is named the same way for the same reason.

## A number's name and the writing on its faces

*Same round: "When I missed the score became as in the screenshot — no longer
digits."*

`setThingLabel` hangs a plaque with a thing's **name** on it and stores that
name in `userData.label` — the same field for a nest, a bird, a box, a sound, a
notebook. A NUMBER also read `userData.label` for something else entirely: text
to paint on its faces **instead of** its digits, which exists for exactly one
caller — the "?" on an "any number" wildcard in a thought bubble.

So naming the counter "misses" armed a trap. The plaque appeared and the digits
stayed, because `setThingLabel` does not repaint a number. Then the first +1
arrived, `setValue` redrew the faces, and every one of them said *misses*.
Which is exactly why it looked right until the moment it mattered — and why
the same mistake was found once before, in round 9, when hole labels were
overwriting the numbers standing in them.

Two meanings, two fields. `label` is the name on the plaque, on every kind of
thing without exception; the face override is `faceText`. And naming a number
repaints it, so its plaque and its digits can never disagree again.


## Looking straight at a pad

*Added 26 Aug. Ken: "there needs to be a way to make any pad full screen
straight on. I tried holding it and clicking on the holding ... message and the
problem was that the game is too wide so I only saw green. And space was added
to its label."*

Both halves of that are one mistake of ours. **Holding a pad is for reading it
and typing on it** — which is exactly why his space went into the label — and
the reading pose is a fixed size that a pitch three times wider than a tablet
simply overflows. A game on a pad is not something you hold. It is something
you look at.

So: point at any pad and press **Enter**, and the camera goes and looks
straight down at it, framed so the whole face fits the window however it is
shaped. **Escape** comes back to exactly the view you left; Enter again on the
same pad does the same.

The important part is what it is *not*. It is not a screen, an overlay or a
second renderer: it is the workshop's own camera, moved. So everything that
worked on the table goes on working from up there — the pointer device still
reads where your hand is and the bat still follows it, SPACE and "." still
switch things on and off under the pointer, Dusty still takes a ball off the
board — and no robot ever knew anything happened.

Measured on a 1280×640 window: a 2.856 × 0.68 pitch fits inside 3.084 × 1.542,
straight above its middle; on a narrow 700×900 window the same pitch fits
3.08 × 3.97. An ordinary tablet pad fills the screen from 0.65 above, which
also makes this the comfortable way to read one.

## The syntax gate had never worked

Found while shipping the above, and much the more important half of the round.

Every patch this project makes is checked by extracting the app's script block
and running `node --check` on it. That gate has been reporting **ok** on a file
whose main block had an invalid unicode escape in a string — an error that
stops the app booting at all, and did: `__nano` was undefined and the workshop
was a blank screen.

The cause is the **extension**. The block is `<script type="module">`. Given a
`.js` file, node parses it as CommonJS, hits the `import` at the top, and falls
back to a module-*detection* pass that returns success without a strict parse.
Given the same bytes as `.mjs` it parses as a real ES module and fails
immediately, pointing at the character.

So the gate has been decorative for as long as it has existed. It now writes
`.mjs`, does the extract and the check in **one process** (the old two-command
form could check a stale extract), asserts that the block it parsed is the one
holding the app, and prints how many characters it actually looked at. Proved
by re-introducing the exact escape that got through: it fails, with the line.

The `artifact-sandbox` note that says "every script block should pass
`node --check`" needs this footnote: not as `.js` it doesn't.


## Playing is a mode, and whether a thing is in the way is data

*Added 26 Aug, from the first real go at the straight-on view.*

Ken, looking down at the pitch: *"The tooltips and the corner panel get in the
way. The entire game wiggles since the mouse is over it. The cursor shouldn't
be visible while over the game."* Three symptoms, one cause — the workshop's
furniture is built for a workshop. Looking straight at a pad is **playing**,
and `body.playing` now hides the cards and the tooltip, stops the wiggle
(a whole scene shaking under the pointer acknowledges nothing) and hides the
cursor. The bar stays, because Pause lives there.

*"Escape returned to normal twice and then stopped working."* That was a real
bug and a bad one. Coming back was driven by a **distance test** — lerp the
camera toward the pose you left, clear the mode when it gets close — so
anything that stopped it converging stranded the mode ON with the orbit
controls disabled: a workshop you cannot move. And pressing Enter again
mid-flight saved the half-way pose as "the workshop", so after a couple of
tries Escape had nowhere to go back to. It runs on a **clock** now, a number
from 0 to 1 and back, which always arrives; and the pose to come back to is
snapshotted only when there is not one already.

*"I was able to add the score to the game but the ball bounced off it. Not sure
what is a good way to deal with this in a general way."* The general way is the
way everything else here already works:

```
[set   | solid | no]     scenery: things pass through it
[set   | solid | yes]    an obstacle again
[query | solid | bird]
```

Solid is the default and has to be — it is what makes a ball bounce off a bat.
A score, a title, a line down the middle of the pitch is told otherwise once
and is then part of the scenery. Measured: the ball crosses the counter without
so much as a change of speed, and still turns at the bat.

*"We can change the size of objects but not their width or height
independently."* True: Ctrl with up and down scaled a pad whole. For a pad the
four arrows now shape it — left and right its **width**, up and down its
**height** — setting the same two properties `[set | width | n]` and
`[set | height | n]` do, reached with the arrows instead of a message box.

And the pitch itself is a proper board now: 6 by 3.2 tablets rather than 8.4
by 2, which is 2.04 by 1.088 — close to the original's proportions instead of
a letterbox. It stands left of centre so it never touches the notebook, which
leaves the right-hand strip of the table for the pads that explain it.


## A number riding on a board is a numeral, not a squashed block

*Added 26 Aug. Ken: "why is there that line through the score and 2 red dashes
at the bottom?"*

A number is a **cube** with six painted planes stuck to its sides — front, top,
back, left, right, bottom — because on the table it is a thing you turn over to
read six ways: the value, the words, the scientific form, the grouped digits,
the continued fraction. Riding on a pad it is squashed to seven per cent of its
height, and the five faces that are not the top squash with it. Each becomes a
sliver standing on edge. The FRONT one is the line across the score, and the
red marks under it are the top slice of the digit painted on it.

A bare number — one riding on a pad, a reading rather than a tool — now shows
its top face and nothing else. Which is exactly what a pad riding on a pad has
always done: `setSprite` leaves one face and turns the other five off. The
same treatment was needed for its **name**: a plaque is something you hang on a
thing standing on the table, and it was being squashed into a sliver of its
own. A thing riding in a scene is part of the scene, and pointing at it still
says what it is called.

Worth noting the shape of this bug, because it will recur: anything with real
thickness becomes wrong when it is flattened to ride. Pads and numbers are
handled; sounds, dice, scales and boxes are not, and the first one dropped on a
field will show the same slivers.


## The slowdown was arithmetic

*Added 26 Aug. Ken: "I tried your Pong on a desk and after a minute or two it
went slower and slower. A memory leak?"*

Yes, and it was found by bisection rather than by reading:

| what was running | textures after 250 frames | and after 500 |
|---|---|---|
| the ball alone | 77 | 77 |
| pointer readings arriving, nothing switched on | 171 | 171 |
| pointer readings **and the bat's robot** | 212 | 232 |

Scene objects flat at 1495 throughout — things were being removed from the
world and their canvases kept, which is the definition of this leak. Twenty
textures every 250 frames is about five a second in real play: six hundred in
the two minutes Ken gave it.

The culprit is one line, and it is in **combining numbers**. When a number is
dropped on a number the arriving one shrinks into the target and the animation
ends with `incoming.removeFromParent()` — and nothing else. A number carries
five or six painted faces, and removing a thing from the scene does not hand a
texture back to the card. On the table you combine numbers a few times a
minute and nobody ever noticed; the bat drops a −7/4 on the pointer's reading
**ten times a second**.

It is the same mistake as the sensor readings ("thirteen textures per pointer
reading, never falling") and the same fix: `disposeThing`. Measured after:
**flat at 84 across 2500 frames** of the full game with the pointer driving the
bat.

A second disposal went in on the way, though it was not what Ken was seeing: a
message that has been acted on is dropped by a dozen different lines in the
handlers and none of them disposed it either. It is done once now, at the one
door every message goes through — `handleLiveMsg` — in a `finally`, so it
happens however the handler returns, and *after* it, since a `[query | bird]`
pulls the reply bird out of the box and `disposeThing` only walks what is still
inside.

**The general lesson, for the next time:** anything the workshop makes sixty
times a second must be disposed, not merely detached. The three places that
mint things per round are readings (fixed weeks ago), messages, and arithmetic.

## Dusty's bag is a record of what YOU swept away

*Same round: "When the user or a robot being trained vacuums we should keep the
ability to grab the last thing vacuumed from the top of Dusty. But when robots
are running it should not put anything on Dusty."*

Exactly right, and it is an undo, not a cupboard: you vacuumed something and
you can have it back. A robot replaying its lesson made no gesture, so there is
nothing to give back — what it sweeps away is gone, and disposed. Training
still stows, because training *is* you doing it: the robot's arm is your hand
while it watches.

It was also crowding out the thing you wanted: the bat sweeps the husk of the
pointer's reading away ten times a second, so six husks filled the bag within a
second and pushed out whatever you had put there.

## A hole's name, big enough to read

The plate was as wide as one hole and a quarter as deep, and *across* and
*away* on the pointer's reading were squeezed into a slot. Half again as wide,
a third as deep rather than a quarter, and the type set from 58px — but not so
wide that two of them touch and read as one long plate, which is the mistake
round 10 caught with overlapping plaques.


## The second slowdown was a list nobody was shortening

*Added 26 Aug. Ken, after the disposal fix: "The 'ball' in pong world still
slows down after a minute or so."*

He was right, and I had measured the wrong game the round before. `pong` and
`pong-classic` are two different programs, and the one Ken plays is the first:
it copies and sends two message boxes every round, roughly four fresh numbers a
round per player, about two hundred and forty a second at Instant.

Every number the workshop makes is pushed onto `allNumbers`, which the frame
loop sweeps twice a second to decide which are close enough to draw with more
digits. The sweep dropped a number **with no parent**. But a number inside a
message box is parented to the box, and when the box is thrown away the number
goes with it *still attached* — so it was never dropped. Measured on
`pong.world` after 300 frames: **1230 numbers on the list, 19 of them
parentless, 1200 parented to something no longer in the world.** A minute is
fourteen thousand entries, each given a world position and a distance twice a
second, and climbing. That is the slowing down, and it is arithmetic rather
than a graphics problem: frame cost went 9.5 → 13.8 → 57.5 ms while the
scene's object count sat flat at 1402.

`disposeThing` already means *this is gone for good, let go of its canvases*.
Now it also marks what it touches, and the sweeps drop anything marked —
numbers and scales on `!parent || __gone`, **nests on `__gone` alone**, because
a nest in Dusty's bag has no parent and must still be able to receive mail.
After: the count oscillates 17–310 instead of growing, and 1800 frames of Pong
hold at 8.6–10.8 ms with no drift.

**The general shape, since this is the third time:** a thing removed from the
scene is not a thing removed from the program. Anything the workshop
*registers* must be deregistered by the same act that disposes it — which is
why the marking lives in `disposeThing` rather than in each of the sweeps.

### A leak is a test now

The sweep moved out of the frame loop into `advanceLOD(dt)`, which the loop and
the test harness both call, and `tests/regress.html` gained a fourteenth check:
switch on both of Pong's players, run 600 frames, and fail if `allNumbers` ever
passes 800. Proved by putting the bug back: **682, 1169, 1646, 2133, 2608** and
a red FAIL; with the fix, **310, 301, 290, 277, 252**.

The check also asserts the ball actually **moved**. Its first version selected
the players by bench index, which shifts between loads — it switched on a
number called *misses*, watched a dead world hold steady at 195 for five
batches, and reported PASS. A gate that passes because nothing happened is
precisely the bug it exists to catch, so it now finds the players by what they
are (`userData.gadget`) and refuses to pass a world that never started.

And `check.py`, the syntax gate that caught the shipped '\un' escape, has
moved out of a session scratchpad into `tests/check_syntax.py` where it can be
run tomorrow. It takes a list of files, so one command gates the source and
both builds.

**The honest caveat:** `pong.world` costs about 9 ms a frame where
`pong-classic` costs 1. That is not a leak, it is the price of the design — it
copies and sends two message boxes every round where the classic reads a sensor
and sets a direction. It no longer *grows*, which is what Ken was feeling.


## A thing off the table is out of play

*Added 26 Aug. Ken: "I put the square ball from pong.world on Mimi and it got
stuck."*

It did, and the console said so three hundred times a second:

    no place to move: the pad  parent chain text < worldRoot < Scene
    mode replay  busy true  speed Infinity

The ball is a gadget — a pad carrying a panel of robots and a speed. Switched
on, its panel takes a turn every frame. Pick it up, set it on Mimi's platform,
and the panel goes on taking turns — but the ball is at a station now, so
`thingPlace` gives it nothing, and every round its robot tried to move it,
failed, and said the failure out loud. It sat there being told to put itself on
the table, for as long as Ken left it there. Measured: six hundred ticks, six
hundred complaints, not one round that got anywhere.

The missing rule is one the table already implies. **A thing that is not on the
table is out of play.** In your hand, in a claw, in a hole, in a house, on
Mimi's platform — wherever it is, it is not in the game, so its behaviour
waits. It stays switched **on**; it simply has nothing to act on until it is
put back, and the moment it is back on the table it carries on from where it
was. That is the answer a robot already gives when it faces a bare nest: not
stopped, waiting.

It is one line, and it is *cheaper* than what it replaces — a panel that can do
nothing is skipped before its turn is taken rather than after it has failed:

```js
if (t.__owner && !thingPlace(t.__owner)) continue;
```

Measured after: six hundred ticks on the platform, **zero** complaints, the
panel still switched on, the copy comes out of the tray as it should, and put
back on the table the ball is moving again inside three seconds. Classic Pong,
whose ball rides on a field rather than the bare table, is untouched — one of
its three riders moves, which is the right one.

The sentence the ball was repeating also named the wrong machine: every station
was described as *"on the robot's own desk"*, which is true of the stand and the
scratch area and quite wrong for the copier. Mimi's platform and Mimi's tray say
so now.

**Not the bug, though it arrived with it:** `tiny-robot corrected entering run:
0.24 1` in the same console. That is a once-per-robot diagnostic with a captured
stack (`new Error().stack`, not a throw), and it self-corrects. Panel robots are
drawn at a twelfth scale and a dozen of them live in a Pong world, so it is
noise from the same scene rather than a second fault.

### And it is a test

`tests/regress.html` gained a fifteenth check: switch Pong on, put the ball on
Mimi, run six hundred ticks, and require all four of — **silent**, **still**,
**still switched on**, and **moving again** once it is back on the table. Proved
by putting the bug back: `silent=false`, red.

Its first draft had a flaw worth recording, because it is the same one as last
round in a new coat. The leak check asserted the ball had moved by comparing
where it finished against where it started — and **the ball bounces**, so on the
artifact run it finished where it began and the suite went red on a world that
was running perfectly well. Position is periodic; a single before-and-after
cannot see motion. It samples every eighth frame now and asks for the *spread*.
A test that can be wrong in both directions is worth more care than the code it
guards.


## A pause stops the world, not the workshop

*Added 27 Aug. Ken: "when I clicked pause to stop the bouncing ball and placed
it on Mimi the copying stopped."*

For the plainest reason: `tick()` is the only thing that drains the step queue,
and the pause gate sat in front of it. So while paused **nothing the user did
could finish** -- not a copy, not putting a thing down, not a machine answering.
Measured: paused, ball on Mimi's platform, nine hundred frames, the queue
climbing to five and never moving, no copy.

That is the wrong cut, and Ken's own use of it shows where the cut belongs. He
paused the ball *precisely so that* he could pick it up and copy it. A pause
that freezes Mimi as well is useless for the one thing it is wanted for.

So: a pause stops the **world running itself** -- robots taking fresh turns,
things moving under their own speed, touches being noticed, eggs hatching,
birds in flight. It does not stop the **workshop**. The queue keeps draining
whenever the floor is yours (`mode !== 'replay'`), and a robot caught mid-round
holds its breath exactly where it stands -- which is what the button already
promised.

The guard against fresh turns moved *inside* `processDirtyRooms` rather than
sitting at its call sites, because `afterQueue` calls it too: with the queue now
draining while paused, that back door would have let a panel start a new round
the moment a copy came out of the tray.

The button's own sentence says what it really does now: *"the world holds its
breath. Your hands still work: pick things up, copy them, put them back."*

## A copy's senses are its own

*Same round: "When I copied the ball that had never run and placed both on the
table and started them they ran ok for a while but then one disappeared."*

Copying already gave the copy a fresh identity and rewrote its panel to match,
by replacing the event guid as a whole JSON string:

    "evt-P901"   ->   "evt-L904-v5uzry"

But a thing does not have one event channel, it has several, and a channel wears
the thing's guid with the channel after a hash -- `evt-P901#edge`,
`evt-P901#touch`. Those are different strings, so the replacement never touched
them. **Measured on a copied Pong ball: the copy's panel mentioned the
original's id twenty times and its own fourteen.** The copy's edge and touch
nests were still registered as the original's, so both programs were reading one
ball's senses. They "ran ok for a while" because for a while the two agree.

The replacement now covers both forms and only those two -- the bare guid closed
by its own quote, the channel form closed by the hash. Neither can run past the
end of a guid into a longer one that merely starts the same way, which a loose
prefix match would do the first time an `L9` met an `L90`. After: **zero**
stale references, and the copy is a real independent ball (spread 3.21 across
the table where before it sat inert).

### Still open: a copied thing leaves the ORIGINAL still

Fixing the copy exposed the other half, and this one is **not fixed**. What is
established, by measurement:

* Baseline, no copying: the ball runs, spread **3.20**.
* After being copied: the copy runs (**3.23**), the original stands **still**.
* **The copy's existence is irrelevant** -- take the copy and vacuum it
  immediately, and the original is still dead. The act of copying does it.
* The original's identity survives: `liveReg.get('P901')` is still the original
  at every step of the copy (that is what the new `__nano.live(lid)` hook was
  added to settle).
* Its event nests survive: the nest count is flat at 10 across the whole copy.
* Its panel is still switched on, still has its live context, still takes turns
  -- and its move fails, repeatedly, with *"no place to move"*.

So the damage is done inside `copyThing`, in the one call that touches the
**original's live tray**: `ctxToRec(tray)`, which does `pushWorld(room)` →
`worldOut()` → `popWorld()` over the running panel. That round trip is the next
place to look.

**A caution for whoever picks this up, including me:** two of my measurements
this round selected the ball by its position on the bench, and the bench order
changes when a thing is picked up and put down -- so a probe that meant to watch
the ball watched the bat instead. Select by `lid`. The conclusions above all
come from a held object reference or from `live(lid)`, not from bench order.

### Two more tests

`tests/regress.html` now runs sixteen checks. The new one, **a pause stops the
world, not the workshop**, asserts four things at once: the ball stands still,
you can still pick it up, Mimi still finishes the copy, and no panel sneaks a
fresh turn. Proved by putting the old gate back: `copier-works=false`, red.


## One renaming, at every door that makes a copy

*Added 27 Aug. Ken: "I thought that copying produced an identical structure
with fresh nests and birds (and their guids). I also thought that serializing
and recreating would act like that. So I put the classic pong game in a
notebook and took a copy twice. One copy ran briefly and then the ball got
stuck in the corner."*

His model is the right one, and it was not implemented — it was hand-rolled in
one place (Mimi) and nowhere else. The notebook take path built copies straight
from the stored record, and `thingIn` registers anything wearing a lid under
that lid: `liveReg.set(o.lid, t)`. So every copy taken wore the record's
identity, and each new copy **evicted the previous owner of the name**. Things
are addressed by name; the last copy taken owned it, and every earlier one lost
its mail. A dispossessed ball still glides — motion is its own — but its
robot's bounce messages land on whoever owns the name, so it never bounces
again: into the corner and stuck. Exactly the screenshot.

And the hand-rolled rename in Mimi's `copyThing` had now been wrong twice in
two rounds: first it missed the `#channel` guids, then it renamed each rider
alone and could not see that riders on a copied field reference their
**siblings** — a copied game's ball would have rung the original's score.
Hand-rolling per-door is the bug. So there is one mechanism now:

**`rekeyRec`** walks a record once to find every identity it *defines* (a
thing carrying `lid`/`liveLid`), mints a fresh lid and event guid for each,
then walks again re-addressing the birds (`liveId`), the gadget bindings
(`boundTo`), and the event-nest guids — bare or with a `#channel`. What it
does **not** rename is the point: an ordinary nest's guid is shared on purpose
(a copied nest joins the original's delivery group — ToonTalk's own rule), and
a bird serving something *outside* the copy keeps serving it. Fresh names for
what is inside; untouched references to what is outside. It is applied at
every door where a record becomes a copy: the notebook page, Mimi, and a
robot's thought. A live pad or a scene copies as `thingOut → rekeyRec →
buildFromRec` — write it out, rename, read it back — which is precisely the
serialize-and-recreate Ken assumed.

### The rename that reached back through the mirror

The first version of `rekeyRec` renamed **in place**, and `thingOut` does not
clone a closed panel — `r.panel` *is* the live thing's own `panelWorld`. So
copying a ball whose panel was closed rewrote the ORIGINAL's program: the ball
kept its name, its panel spoke fresh names, and its robot went deaf after one
round. The interactive test missed it because that ball's tray happened to be
open (`ctxToRec` builds a fresh record); the suite's ball had it closed, and
went still. `rekeyRec` now works on its own deep copy, always. A rename that
can reach shared structure must not be trusted to be handed a clone.

This also settles the previous round's open mystery — "a copied thing leaves
the original still" — twice over: the half that was my broken harness (a full
hand silently no-oping, drops landing on stations), and now a real half, this
mutation, which the new suite check caught on its first honest run.

### And the minus button

*"I held the classic pong game and it ignored the − button to shrink it."*
`setPadSize` clamped at a floor of 1 — a pad could grow to 3× and never
shrink below full size, silently. A pitch told it is six tablets wide has
every reason to shrink: the floor is a quarter now, and − works held.

### The check, and what its drafts got wrong

`tests/regress.html` check seventeen, **copies are wholly their own**, has two
halves: *structural* — the classic game through Mimi once, then the copy's
record must share not one **defined** name with the original's (references may
be shared: both bats listen to the same pointer device, and that entanglement
is the design) — and *runtime* — the square ball, its copy, and a copy OF the
copy, all running, each required to sweep the table. Proved to bite: with the
renaming disabled, `0.0/0.0/3.2` — only the ball that owns the name moves,
which is Ken's report in numbers.

Its drafts failed three times, each a lesson already learned once: it read the
tripped thing's home position *while the thing sat on Mimi's platform* and put
it down off the table; it selected "the ball" as *the first gadget*, which is
the bat; and it placed three full-size pitches on a bench that cannot hold
them, where a ball pressed against a neighbouring solid pitch pins at the edge
— and blamed the app each time. A harness is code too, and it does not get to
skip the discipline.


## Round 28: six asks, and a confession the suite had to make

*Added 28 Aug. Ken's list: resizing Pong should resize its parts; Marty should
describe what a robot does at a high level; run/pause should apply to robots
only; gadgets dropped on a picture's panel should bind; importing resources
should not reset the world; Dusty should switch off what he vacuums — and:
"It seems you should have been able to catch some of the recent bugs without
my testing."*

**Riders scale with their field.** `subFootprint` capped a rider at 0.75 of
its natural size — an absolute number, so a shrunken pitch carried full-sized
players. The cap now scales with the field's chosen size (`0.75 * sz`): at
full size nothing changes, at half size the bat is half. A half-size game
still plays (five bounces in 600 frames).

**Pause is the robots holding still.** `advanceWorldClocks` gets a
`worldRuns` flag: paused, only `advanceMovers` (behaviour-driven motion)
holds; birds in flight, eggs, wobbles and chimneys go on. A delivery may land
while paused — that is the point — but `checkWaiting` refuses to give a woken
robot a turn until Run, and the unpause re-checks the vigil.

**Dusty switches off what he takes** — directly (`tray.dirty = false` down
the subs), not through `switchGadget`, which would conjure a tray for a thing
that never had one. And a thing with a speed re-joins the movers when it
comes back to the bench, because the sweep prunes whatever leaves the world.
Fallout fix: a tray stranded off the bench (its thing vacuumed and returned)
now comes back with its thing in `bringOutPanel` — before that, SPACE lit a
panel no list held, and nothing ever gave it a turn.

**A behaviour dropped on a thing's panel binds to the thing.** The drop rule
already existed for dropping a gadget ON a thing; dropped on the thing's
PANEL it matched the tray (a room) first and bound itself to the tray, which
is nothing. Drops on rooms come straight from the click handler — never
through combine — so the rule lives in `roomDrop`, with combine's copy kept
for the paths that do pass through it. Dropping the gadget's own open panel
means the same thing. Proved end to end: bind a ball to a plain pad and THE
PAD bounces (spread 1.89).

**Importing a world mid-project lands as a notebook** — one page per thing,
stations and the robot included, named after the file, wiping nothing. A
fresh workshop still opens the file whole, which is what opening a project
means. Taking a page off gives a fresh-named copy (rekeyRec at the notebook
door), so an imported game runs beside whatever is already on the table.

**Marty now gets the FACTS of every behaviour in reach** — condition, team
shape, steps in words (via `describe`), whether it is on, moving, or bound —
capped per fact and in total, plus a system rule: answer WHAT with the
purpose of the whole loop, recite steps only when asked HOW. The first
version of the cap dropped the ball's 2800-character team brief whole and the
facts block was always empty; each fact is now truncated to fit.

### The confession: the suite's own frame was lying

Ken: "you should have been able to catch some of the recent bugs without my
testing." He is right, and this round found something sharper than a promise:
`dustySuck` began `if (!dusty) return` — and demo frames do not build the
mascot. So in the SUITE's world, **every robot vacuum step has been a silent
no-op all along**, and the goldens faithfully recorded the wrong machine:
n-to-1's golden ended with the stand still occupied and a nest of empty boxes
— the program never worked in the frame that certified it. The mesh held the
semantics hostage.

The fallback stows without the mascot (queued, like the animated path, so a
vacuum keeps its place among the round's steps), and six goldens moved —
deliberately, for the better: n-to-1 now ends with the finished 5-4-3-2-1
chain, and the fractions worlds run FURTHER because vacuums clear the way.

The lesson written into the suite: **a missing model must never mean missing
semantics**, and a golden is only as honest as the frame that made it. The
round's four behaviours are check eighteen — riders-scale,
dusty-switches-off, panel-drop-binds, import-lands-as-notebook — each leg on
a fresh world, because the dusty leg's leftovers once failed the bind leg and
the report blamed the wrong feature.

**Still owed from Ken's list:** the remaining library gadgets (his "is it
time?" — yes; next round), and a place to see Marty's abstractions earn
their keep.


## The shelf is twelve

*Added 28 Aug. Ken: "Let's finish the library of anima-gadgets while I do
some testing."*

The blocked six wanted exactly what the plan said they wanted: a sayable SIZE
and something to do arithmetic against on the touch channel. Both went in as
message-surface additions, small and general: `size` joins across, away,
position, speed and solid (set / move / query / listen, in the units the held
card's + and − buttons step, with the echo rule and a `#size` announcement),
and `[set | speed | ...]` now announces on the `#speed` channel — skipping
echoes, like a number does.

Two idioms carried the gadgets, and they are the round's real yield:

**Dozing on touch.** The touch nest starts EMPTY; the team's conditions read
its top, so every member dozes until an announcement lands. The workshop
announces only when contact CHANGES; the robot eats what it acted on. So
"grow when touched" grows once per touch — not sixty times a second — and an
untouched gadget costs nothing at all. (The gadgets that must MOVE every
round — bouncing, reversing — keep a seeded reading instead: one dozing
member stops a whole team, mover included.)

**The scale is the if.** The speed limit queries nothing and branches
nowhere: a speed announcement arrives, the weigher puts its across-number on
one pan and the limit on the other, and the LEAN dispatches the next round —
capper on tilt-left, clearer otherwise. The gadget is born at 0.9 with a
limit of 1/2, so SPACE alone shows it braking itself: 0.9 → 0.5 inside
sixteen frames, measured.

Placement lessons, paid for twice: a live thing on a FOLDED tray's bench
hydrates unparented and cannot receive mail — so the bell and the score ride
in their gadgets' work boxes, where a live thing in a hole is still
reachable. And `reverse on collision` deliberately handles THINGS and leaves
edges to `bouncing`: alone it will eventually pin at a wall; bound together
with bouncing on one star it is pong-ball physics with no training anywhere,
and that composition is what the shelf exists to teach.

### The harness lied twice more, and the second time was structural

The shelf check failed in the suite while the same steps worked by hand —
twice, for two different reasons, both the harness's own:

1. At Instant speed, `fastForward` drains whole rounds per frame and the
   mover TELEPORTS across the grow pad between two touch sweeps. Contact is a
   thing that happens in sampled time; the check now runs at a walking pace.

2. Worse and older: every check stamped its frames with
   `performance.now() + i * 17` — a clock that runs seconds ahead of real
   time — and the touch sweep's dedup timestamp is GLOBAL. One check's
   synthetic future poisoned the next check's present: the sweep believed no
   time had passed and swept nothing, for real seconds. My manual repros
   "worked" only because real time passed between tool calls. The suite now
   runs every harness frame on one monotonic virtual clock (`fnow()`),
   started far above real time, shared across all checks.

`tests/regress.html` check nineteen, **the shelf is twelve**: all twelve lids
present, the speed limit caps itself, and grow grows when the shelf's own
mover drives through it. Proved to bite: with `size` removed from the message
surface, `grow-grows=false`, red.


## A rider's place is said in the field's own units

*Added 28 Aug. Ken: "When I shrank the classic pong game the paddle stopped
moving though once it moved and stopped."*

Because a rider's place was computed in DISPLAY units — `at.u * w`, where `w`
includes the field's chosen size — the bat's program, whose numbers were
authored against the full-size pitch, aimed outside the shrunken one and
pinned at the clamp after a single move. Which is precisely what "moved once
and stopped" looks like.

The rule that was missing: **a rider's place is said in the field's OWN
units** — the ones it has at natural size — however big the field is drawn.
Shrinking a game changes how it looks, never what its numbers mean. The
display size is divided out of `thingPlace`, out of the wall clamps, and out
of the write-back, so the same program plays the same game at every size; at
natural size the division is by one and the goldens do not move. The
half-size classic now plays measured: ball sweeping 0.79 of the pitch, bat
following the pointer at 0.53 — and it is a suite leg.

## The bind that only worked on the parts nobody clicks

*Same round: "I couldn't drop an anima-gadget nor its panel on the panel of
an image."*

The binding branch listened at `roomDrop` and in `combine` — the code paths a
synthetic `clickThing(tray)` takes. A REAL pointer drop lands on whatever
part of the tray it hits: the work box on the stand, a perch bird, the import
or info plaque, a wall — and every part has its own click meaning, handled in
`handleClick` before the general routes are ever reached. Dropping a gadget
on the perch GAVE the gadget to the picture as a message, which quietly
swallowed it.

One intercept now sits at the head of `handleClick`: a held behaviour (or its
own open panel) dropped on ANY part of another thing's panel binds to that
thing — `trayOfTarget` already knew how to walk from any pick to its tray.
Proved on an image's panel by its crowded part: dropped on the PERCH, bound,
and the picture itself marches (spread 1.00).

The testing lesson, again: my harness clicks name their targets and so take
the polite route; a mouse hits what it hits. When a click can land on six
different pick kinds, the feature must be tested through the hostile ones.

## Marty knows where things ride

*Same round: asked about a pad carrying a behaviour, Marty knew nothing.* The
facts block described the behaviour but never said WHERE it was, and the
hand line said "a blank pad", full stop. The hand line now names what rides
("a pad saying '*' carrying a behaviour riding on it: moving right") and
every behaviour's facts say where it stands — in the visitor's hand, riding
on the pad in the visitor's hand, or riding on some named thing — so an
answer about "what am I holding" has something to hold on to.


## The away-day probes: nine combinations, one real bug

*Added 28 Aug. Ken: "I'm away for a few hours — can you come up with new
tests and run them." The probes were aimed where his bugs have actually come
from: feature COMBINATIONS, save/load round-trips, and claims published but
never proved.*

What held, each by measurement:

1. **The composition claim** — bouncing + reversing bound to one star is
   pong-ball physics: the star wandered 3.06 across, 1.01 deep, and turned
   43 times in 900 frames, with no training anywhere. The manual's promise
   is true.
2. **Bindings survive a save/load** — both of the star's bindings reload and
   drive it again.
3. **A shrunken game survives a save/load** — sz, rider scales and all, and
   still plays.
4. **Vacuuming the TARGET of a working behaviour is graceful** — no errors
   while the target rides in the bag, and the drive resumes the moment it is
   put back.
5. **A Mimi copy of a bound gadget stays bound to the same star** — outside
   references entangle, as designed — and both drive it at double pace.
6. **Shrinking a game mid-play** does not interrupt it.
7. **The half-size game plays straight-on** and Escape restores.
9. **A filed binding survives the notebook page**: the copy comes off bound
   to the same star and drives it.

Probe 8 found the bug. Binding the speed limit to the classic BALL — a
legitimate wish: limit the ball! — fell through to the pad-join rule and
**merged their faces**, because the drop rule's guard read `!isGadget(target)`:
a behaviour could bind to anything except another behaviour, and the classic
ball IS a behaviour. Joining two gadget pads is never what anyone means — it
silently discards the dropped one's panel. The guard is now
`target !== incoming`: the middle of a gadget still takes a rider, the edge
binds, and "speed limit dropped on the ball limits the ball" works — proved
with the limiter attached to a running game.

Two harness notes with a general shape:

* The probes' `clickBench` parking kept feeding drops to the ride/join/bind
  resolution of whatever pad was nearby — three probes were eaten by it, one
  leaving a shelf gadget renamed "shrink when touched**" (the pad-join rule
  doing its documented job on a probe's sloppy drop). The harness now has
  `place(t, x, z)` — the tripod: exact placement, no gesture semantics.
  clickBench remains the way to test what a USER's drop would do; place is
  for probes that need a thing to stand where they said.
* Twenty checks now: **bindings travel** (gadget-binds-gadget with the face
  intact, bindings through a save/load, the composed star still wandering
  and bouncing, and Ruby releasing). Proved to bite: with the old guard back,
  red on exactly the found bug.

Probe 10 found the second bug, in a sentence the manual had promised for two
rounds: *"Wake Ruby and click it and it works on itself again."* The release
branch existed — and sat BELOW Ruby's erase-in-place branch, which catches
every thing-click first: dead code, and a Ruby click on a bound behaviour
quietly erased the gadget instead of freeing it. The release now comes first,
scoped to bound gadgets, and is measured working: boundTo cleared, face
intact, and the freed gadget moving itself again. A promise in the manual is
a claim the suite must hold — both of this session's real bugs were found by
reading published sentences back to the app.


## Stage 6 shipped: a rational plus a flag

*Added 28 Aug. Ken: "Yes let's introduce inexact numbers as discussed."*

Built as the design settled it. Three operations are inexact by nature —
`sin`, `cos`, `root` — typed onto a held number exactly as `mod` always was,
and they IGNORE the number they are written on: the badge is the whole
message, so a 1 wearing "sin" turns the 30 it lands on into sin 30. Angles
are **degrees**, because a child drawing a circle knows 360 and nothing in
the workshop wants radians for their own sake.

**Nothing calls JS `Math`.** `Math.sin` is implementation-approximated by the
spec: two browsers may legitimately differ in the last bits, and a saved
world would then replay differently on another machine — which would quietly
undo replay, echo suppression and headless verification all at once. So the
kernel is argument reduction plus a Taylor series over rationals for sine,
and Newton's method over BigInts for roots, every intermediate rounded to a
working thirty places so nothing grows without bound. Deterministic by
construction rather than by luck. Answers are kept to twelve places.

Two decisions worth recording:

* **A root that comes out whole stays EXACT.** The square root of four is
  two, and marking it "approximately two" would be a lie about a number the
  workshop got exactly right. `rootRat` tries the integer root first.
* **Exactness is part of the representation, so it is part of equality.** An
  exact half and an inexact half are different numbers; a thing told it is
  now approximately a half has genuinely changed and says so. That keeps echo
  suppression honest rather than breaking it.

The marker is a wavy equals and a DECIMAL: `≈0.707106781187`. Never a
fraction — 707106781187/1000000000000 tells a child nothing and claims an
exactness the number does not have.

`examples/behaviours/ellipse.world.json` is the thirteenth behaviour and
Stage 6's proof. It stays OFF the twelve-shelf, which is capped on purpose.
Nothing in it knows what an ellipse is: it is four badged numbers dropped on
a running total, twice, plus a step — `centre + radius × sin(angle)`. Measured
at 2.2 across by 0.8 deep with every sampled point on the curve.

## Speed: built in, and what that actually buys

*Same round, Ken: "I guess we'll go with speed being built-in... And as an
exercise it would be interesting to see if we can build it from the current
functionality in principle."*

It can be built — and it already is. `moving right` on the shelf IS speed
made of robots: one robot sending `[move | across | 1/60]` every round. So
the question is not whether the workshop CAN, but what the primitive buys.
Measured, and it is exactly one thing:

| | one second of wall clock |
|---|---|
| **robot-built** `moving right` | 60 rounds → **2.000** · 30 rounds → **1.000** |
| **built-in speed** (0.9 across per second) | 60 fps → **0.900** · 30 fps → **0.900** · 15 fps → **0.900** |

A robot's move is distance per TURN, so on a slower machine the thing goes
half as far in the same second. Built-in speed is distance per SECOND: the
same on any machine, because `advanceMovers` is handed the real elapsed time.
That is the whole of the case for the primitive, and it is worth having — a
game that runs at a different pace on a slow laptop is a game that plays
differently, and a child cannot debug that.

**On x-, y- and z-speed.** The workshop is a TABLE: every thing's place is
two numbers, across and away, and so are the edge reading (four walls), the
touch reading (four sides) and every field. A third axis is therefore not a
third number on speed — it is making the world three-dimensional, which
touches place, edges, touching and fields together. That is an epic, not a
tweak, and nothing on the table currently rests in the air.

The real question hiding inside it — whether speed should be per-axis NAMED
properties, as the original's `SpeedToRight` and `SpeedToTop` were two
separate sensors — is already answered by the empty-hole idiom:
`[set | speed | [1/2 | ]]` sets across and LEAVES AWAY ALONE. The speed limit
gadget on the shelf is built on exactly that. A named `speed across` /
`speed away` pair would be cheap and additive if the box of two ever reads as
a hurdle.

## Bottling is gone (and the note that said otherwise was stale)

*Same round, Ken: "I thought we got rid of world bottling. If not what is
holding us back?"*

He is right, and the memory note claiming otherwise is now corrected. A room
is **hydrated once** — `hydrateRoom` builds its live world from the record and
throws the record away — and from then on entering it is `pushWorld`, which
swaps a bank of globals and nothing more. There is no `worldOut`/`worldIn` in
the running path at all; the only two calls left are hydrate-once and
copy-on-demand.

Measured, by growing the OUTER world 29-fold under the same room:

| outer things | scan for dirty rooms | scan + run | **the run alone** |
|---|---|---|---|
| 7 | 0.0070 ms | 0.0110 | **0.0040** |
| 52 | 0.0160 | 0.0170 | **0.0010** |
| 202 | 0.0330 | 0.0350 | **0.0020** |

Entering and running a room is flat at two to four MICROseconds however big
the world outside is. What does grow is the per-frame scan of the bench for
dirty rooms — a linear walk over things, which any design would pay and
which costs a thirtieth of a millisecond at two hundred things.

**What is actually left of the engine/view split**, then, is two other
things, and neither is bottling:

1. **One execution context.** The globals are swapped, not duplicated, so
   only one world can be mid-turn at a time. That is what blocks
   multi-threaded houses — not serialisation cost.
2. **Every world is real 3D.** A room's contents are actual meshes mounted at
   toy scale inside it, so the renderer pays for worlds nobody is looking at.
   The headless-interpreter half of the split is the part still unbuilt.


## A turtle, built out of what was already there

*Added 28 Aug. Ken: "Can you implement a turtle that responds to forward and
right messages."*

Built as a BEHAVIOUR, not a primitive, because the shelf's own card says
"there is no move, no bounce, no follow — only messages a thing already
answers, and robots that send them". A turtle is the same claim under more
pressure, and it holds:

    forward n  ->  across = across + n x sin(heading)
                   away   = away   + n x cos(heading)
    right a    ->  heading = heading + a

Every line is badged numbers dropped on a running total on the scratch spot: a
copy of the heading, then the `sin` badge, then the distance taken out of the
order and TOLD TO MULTIPLY (`setOp`, the same step a child performs by typing
× on a number). Nothing in the workshop knows what a turtle is.

**How it hears.** The turtle keeps a NEST in its work box — a letterbox — and
its two robots read the top of it, dispatching on the word: `forward` or
`right`. That is the same shape as the arrow-key gadget dispatching on key
names and Pong's ball dispatching on edges. Give an order to the bird
addressed to that nest and she posts it; the member whose thought names the
word takes the floor and eats what it acted on.

**It needed Stage 6.** To face a direction that is not a right angle you need
a sine. Measured: after `[right 30]`, a `[forward 3/10]` moves across 0.1500
and away 0.2598 — a step of exactly 0.3000 along a 30-degree heading. Before
inexact numbers a turtle could only have turned in quarters.

## A sleeping panel now costs almost nothing

The turtle made an old promise measurable. Ken, rounds ago: *"In original
ToonTalk when a robot dozes it registers with what it is waiting on... There
is no runtime penalty for having a huge number of dozing robots. Is this how
you did it?"* It was not. One turtle asleep on an empty letterbox cost
**0.08 ms every frame** — eight per cent of a frame budget for a thing doing
nothing at all.

The reason was that **the poll WAS the wake**: a panel got a turn every frame,
and taking that turn is what ran `checkWaiting` and noticed the mail. Skipping
the turn would have meant never waking up.

So the wake got its own signal. `nestReceived` already walks up from a nest to
the room or panel containing it — that is how a delivery marks a panel dirty —
and it now leaves a mark there saying the post has arrived. The scheduler
steps over a panel whose team is asleep and whose mark is clear.

| | before | after |
|---|---|---|
| one sleeping turtle | 0.0795 ms/frame | **0.0240** |
| its turns in 700 frames | ~1400 | **47** |
| thirty sleeping turtles | ~2.4 ms/frame (projected) | **0.30** |

A delivery still wakes it **on frame 0** — measured, not assumed. A safety net
polls a sleeper about twice a second, because not every wake arrives by post:
a hand reaching into a sleeping panel's work box does not. Everything a
PROGRAM can do to wake one goes through a nest, and that is instant.

This is not yet the full registration index — the scheduler still WALKS the
list of panels each frame, so the cost is linear in how many there are, just
with a tiny constant instead of a whole world-swap. Registering waiters
against the guid of the nest they doze on would make it flat. What is bought
here is roughly a factor of ten.

### The same bug twice, in one afternoon

Skipping sleepers broke *a thing off the table is out of play*, and the reason
is worth keeping: **there are two schedulers**. The panel loop in
`processDirtyRooms` collects panels; if it collects none, the code falls
through to `findDirtyRoom`. The out-of-play rule lived only in the first one —
harmless while the first one always had work, fatal the moment sleepers
stopped filling it, because `findDirtyRoom` then picked up the very panels the
first loop excluded, and the endless "no place to move" came back.

Both tests are now named functions (`sleepingRoom`, `outOfPlay`) used by both
schedulers. **A rule that decides whether something runs must be asked by
every path that can run it** — and the suite caught this one within a minute
of the change, which is the entire argument for the suite.


## The pen, and the nest that was only asleep

*Added 28 Aug. Ken: '"Her nest is gone" when I tried the turtle world. Also
the arrangement wasn't so good... How can we add "pendown" and "penup" to the
turtle?'*

**Her nest was asleep, not gone.** The turtle's letterbox is authored inside
its panel, and a panel does not exist until it is hydrated — and a gadget
nobody has switched on yet is exactly the one a FIRST order arrives at. Ken
gave [forward] to the bird and was told the nest was gone. The delivery now
looks, before giving up, for a closed panel whose record holds a nest wearing
the guid, wakes that panel — folded, exactly as switching it on would — and
asks again. And since a delivery marks a panel dirty, **a posted order also
starts the turtle**: mail waking a sleeping machine is what mail is for, and
it is what houses have always done. Measured: order posted to a
never-switched-on turtle → the bird takes it, the panel hydrates, the turtle
steps 0.3.

**The pen is a thing property, not a turtle feature.** `[set | pen | down]`
makes ANY thing draw as it moves — each `placeThing` leaves a stroke from
where it stood to where it stands, on the table or scaled onto the field it
rides. `up` lifts it, `clear` rubs out, `[query | pen | bird]` answers. The
strokes are CHALK, not things: they cannot be picked up, they do not save,
and they are capped at six hundred per thing so an afternoon of turtling
cannot fill the machine. The turtle then learns `pendown` and `penup` as two
more team members dispatching on bare words posted to the letterbox — eight
lines of authoring, no engine knowledge.

Measured, the full Logo ritual: pendown, then forward/right-90 four times —
four corners each 0.3 apart, the path CLOSES to within 0.0000 of the start,
exactly four strokes on the table; penup, then forward — still four. The
suite's turtle check gained the pen legs (strokes 0/1/1).

The turtle world is also rearranged: the bird stands in front with nothing
behind her, the orders make one spaced row, and the TRY card teaches the pen.

**Ellipse-on-picture: could not reproduce.** Bound and traced measured-clean
through every route drivable headlessly — notebook copy onto the picture,
onto its panel, even picked up mid-run. One earlier "failure" turned out to
be this session's own contaminated page state (a wedged busy flag from an
interrupted probe). Ken is asked what the workshop SAID at the moment of
refusal — the say line is the fingerprint.


## Pong from the shelf, the wake index, and Marty's showcase

*Added 28 Aug. Three items off the todo list in one round.*

### The capstone clause, honoured late

`pong-gadgets.world.json`: the ball is a pad with THREE shelf gadgets bound
to it — bouncing, reverse on collision, send 1 to the score — the bat is a
pad with following-the-pointer, and no robot anywhere was written for Pong.
Measured playing: ball roams 3.2 × 1.1 bouncing on both axes (24/44 direction
changes), rally climbs under a perfect pointer-player, slows when the bat
parks. Suite check twenty-three.

What the rebuild taught, in order met:

* **Bouncing was one-axis.** A free ball pinned at the near and far walls, so
  the shelf gadget grew an away step and two members — five robots now,
  differing only in the edge word they expect. A thing called bouncing should
  bounce off every edge.
* **The prefix-collision bug, met in authoring.** A blind replace of `G912`
  ate the front of `G912S` — exactly the longer-id collision rekeyRec's
  comment warns about — and 470 scored contacts went to a tally wearing a
  mangled name. Then the "fix" renamed the WHOLE inner tally to the bench
  score's id, and two things claimed one name: the copies-clash bug,
  re-created by hand. The lesson both times: rename the suffixed id first,
  and re-aim BIRDS, not identities.
* **Step-movers compose by ADDITION.** Two bound movers sum their steps; after
  a wall bounce the two can briefly disagree. Playable, and a seam — the
  speed-based reactors that built classic Pong compose more cleanly, which is
  the measured argument for built-in speed all over again.
* **The rally scores HITS, not misses** — touch is what the shelf gadget
  hears. A miss-counter is an edge-listening shelf gadget nobody has asked
  for yet. The seams are on a card IN the world, where a player reads them.

### The registration index, at last

The other half of Ken's dozing-robot question. The sleeping-panel fix bought
the scheduler's half; this buys the WAKE's half. A robot going to sleep now
writes down the guids of the bare nests that blocked it (the scan that says
"nothing on the nest in hole 2 yet" was already walking them), and a delivery
asks only the robots registered on the nest it just fed — `checkWaiting(nest)`
from `nestReceived`, everyone when called bare. A doze over a LIVE mismatch
registers as a wildcard.

Proved with an army: thirty turtles with distinct letterboxes, all dozing;
one order posted to #17; **exactly [17] moved** and the other twenty-nine
never left their doze. The bank-account canary's golden did not move — its
robot still wakes to every statement request. Known edge, recorded: aliases
added by a nest-join AFTER a doze can miss the indexed wake; the broad
checkWaiting still runs from afterQueue, so it is a delayed wake at worst.

### Marty's showcase, and the judgment asked for

`pong-gadgets` is the showcase — a world where the purpose ("it keeps the
ball bouncing and rings the rally when it meets the bat") genuinely is not
written on any single panel, plus an ASK MARTY card inviting exactly that
question. Two facts-layer gaps found and fixed on the way: labelled pads and
numbers were described namelessly ("a blank pad" for the thing every fact
calls "the ball"), so Marty could not connect facts to things — labelled
things are called by name now.

The judgment itself is HALF-delivered, honestly: this environment has no
brain (the phrasebook fallback), so the abstraction cannot be graded here.
The facts layer is strong — bound-to stated, team shape, per-member
conditions and steps, locations, names — and the system rule is in place.
The other half is Ken's: open Marty on pong-gadgets and ask what the ball
does.


## The game starts at the ball (and the password prompt that never should have been)

*Added 28 Aug. Ken: "the gadget pong game doesn't run. space has no effect on
the ball. the anima-gadgets do nothing too... why did the save password
appear... The paddle is hard to find."*

**SPACE on the ball did nothing because the ball is not a gadget** — the
gadgets are BOUND to it, and SPACE only knew about gadgets and scenes. Now a
thing with behaviours bound to it is switched on and off as one by SPACE and
"." on the thing itself: `switchBound`, used by the key handler and exposed
to the suite, which now drives the pong check through it. The player's eye is
on the ball, not on the cards.

**The gadgets "did nothing" for the deeper reason the screenshot shows:** the
red notebook on his table means the world arrived MID-PROJECT, as a notebook,
and the pages were taken out one by one. Every page-take rekeys its copy —
copies are wholly their own — so the gadgets' `boundTo` still names the
V901 of the RECORD while the ball he took is a fresh L-something. Cross-page
bindings are cut by the notebook path BY DESIGN; the fix is honesty at the
moment of failure: switching on a behaviour whose bound thing is not here now
SAYS SO — "wake Ruby to make it work on itself, or drop it on a new thing"
(and dropping it on the new ball genuinely works). The aliveness test matches
the one deliveries use, because `liveReg` can hold a stale entry from an
earlier world whose thing has no parent — checking mere existence was
defeated by exactly that in testing.

**The password prompt** was the API-key field: a real `type="password"`
input, so Chrome's password manager offered to SAVE the OpenAI key on blur.
The key never left the machine — it lives in localStorage — but the field
should never have spoken to the password manager at all. It is a plain text
input masked with CSS now (`-webkit-text-security: disc`), no form around it:
nothing for Chrome to offer to save.

**And the bat** stands in the clear front-right now, away from the desk
notebook's home, with the rally in the clear front-left — the layout that
put it behind the score and the notebook is gone, and the RUN card teaches
the new SPACE.

Marty, meanwhile, DID WELL on both the Claude and the OpenAI keys — Ken's
words — which closes the judgment the last round could only half-deliver.


## An approximation dresses the part (five reports on the inexact rollout)

*Added 28 Aug. Ken: the square root of 2 worked but the English didn't make
sense; the tooltip is in the way of reading it; arrow keys intermittently
dead; inexact numbers should look different; the tooltip shouldn't show the
approximate fraction and should say it is inexact.*

**The English face spelled the fraction.** The words face fed the raw
rational to `englishText`, so √2 read "one trillion four hundred
fourteen billion … over one trillion" — the bookkeeping denominator,
in words. An approximation is READ ALOUD now, the way a person says a
decimal: "about one point four one four two…" — `englishApprox`, first
four places and a trailing ellipsis, "about" carrying the inexactness in
words. The suite asserts the spoken form for √2, a marked half, and a
negative.

**It looks different at a glance now.** An approximation wears a BROKEN
frame on every face (`setLineDash` on the face border) — a number that is
not exact is not dressed in an unbroken line, and the difference reads at
arm's length before the wavy sign does. The underside gave up its continued
fraction for owning up: "not exact — only the first twelve decimal places
are kept".

**The tooltip said too much and too little.** It offered the mixed-form
fraction ("2 414213562373/1000000000000") — false precision from the
improper-fraction courtesy, now guarded with `!v.x` — and never said
"inexact", now "an approximate number, not exact".

**The tooltip sat ON the face being read.** Beside the pointer, the tip
landed on the very thing it described — worst while CARRYING, when the
thing is at the pointer by definition. The tip now goes UNDER the thing's
projected screen box (the held thing's box while carrying), above it when
there is no room below, and docks near the bottom failing both.

**The intermittent arrow keys were the Speed select.** A change made with
the mouse leaves the SELECT focused and the arrows then belong to the
control — silently, until a click on the world took the keyboard back
(that click is why "later I could"). Same cure as the clicked-button rule
one entry up from it: a deferred blur on change, for every select.


## Why the suite did not catch it, and four things it now catches

*Added 28 Aug. Ken, after playing: "why didn't you catch this problem during
your testing? ... it slows down as it passes through text pads and its
bounces are sometimes not very natural. The anima-gadgets still don't behave
on their own. And you were wrong about loading pong-gadgets.world into a
non-fresh world so it loaded as a notebook. That wasn't the case. The paddle
follows the cursor everywhere ... I couldn't turn the paddle off."*

### The answer to the question

Every check drove behaviours with `switchGadget(g, true)` — the inside
function. Twenty-three checks proved the SIMULATION and not one of them ever
pressed a key, so "SPACE on the ball does nothing" was invisible: the door
was untested by construction. Even the round-34 check written to cover it
called `switchBound` directly, which is the same mistake one layer up.

There is now `D.press(thing, key)`: a real pointermove onto the thing (so
`resolve` and `lastMoveEv` do their own work) and a real keydown on the
window. The pong check goes through it, and asserts the four panels actually
started. A test that cannot fail the way a person fails is not a test of the
thing the person uses.

### Off is a decision, idle is a state

Ken could not stop the bat, even after pausing. Measured: "." DOES stop it —
and the next pointer delivery starts it again. `nestReceived` marks every
enclosing room dirty so that post wakes a sleeping team, and it could not
tell a team that is idle from one a person switched off. The pointer posts
sixty times a second, so the follower came back to life inside a frame,
every time, for ever.

A panel switched off now says so (`userData.stopped`), and post leaves it
alone until somebody switches it on again. The room lever and "." on a room
set the same flag, because the lever IS the switch.

### The ball scored against the documentation

"It slows down as it passes through text pads." The doc cards, the rally
counter and the gadget cards were all SOLID, so the ball collided with the
instructions — and every contact ran a scoring cycle. With the bat lifted
off the table the rally still climbed to 69 in 700 frames, 39 of those
scored while the ball sat on a doc card. Everything but the ball and the bat
is scenery now — `[set | solid | no]`, which the message surface has had
all along and this world never used. Measured after: 150 frames sitting on a
card, rally 0.

### The bounces: moving on the clock instead of on a turn

The rest of "not very natural" is the step-based movers. Each runs a mover
robot EVERY round, and a cycle builds a message box and flies a bird —
about 10ms. Three gadgets on one ball: 26ms a frame median, 57 at p90,
against 0.2ms idle. The ball therefore moved as unevenly as the frames
arrived (steps from 0.005 to 0.106), which the harness could never see
because it feeds fixed 17ms steps. THAT is the real answer to "why didn't
your tests catch it": the harness had no clock of its own to lose.

Two new shelf gadgets, and Pong rebuilt on them:

* **bouncing at a speed** (14) — sets a speed once, eats the edge reading,
  and dozes on the bare nest until a wall, where one robot flips one number
  and hands the speed over again.
* **reverse a speed on collision** (15) — the same four sides one box
  deeper, filling in ONE hole of the speed box and leaving the other EMPTY,
  which is the empty-hole rule the speed message already had. That is what
  lets it share a ball with 14 without the two arguing about the axis
  neither of them touched. No mover means its touch nest can be the dozing
  kind: between contacts it costs nothing at all.

Measured on the rebuilt world: 0.2ms a frame median (0.4 at p90), and a step
that is the same size every frame but the bounces — two distinct step
sizes where the step-based pair gave dozens. The step-based pair stays on the
shelf beside them: same behaviour, two ways, and a child can watch which one
stutters.

### And the bat is a wall again

**following up and down** (13) — classic Pong's own bat robot, promoted to
the shelf. "Following the pointer" sets POSITION, so the bat sat exactly
under the cursor: it wandered sideways out of its lane, and it could never
be pointed at to stop it, because it was always where the pointer was. This
one takes the AWAY out of the pointer reading and sends only that.

### The one thing not reproduced

"The anima-gadgets still don't behave on their own." From a clean load,
SPACE on a gadget card starts it and the ball moves (0.5157 in 120 frames,
panel open). What DID turn up while trying: a first-run name dialog holds
the keyboard, and `typingInAField()` then swallows every workshop key —
which is a real way for "nothing happens" to happen, and worth knowing. The
round-34 missing-target branch also used to warn AND start the robots
anyway; it refuses now, because a behaviour that says one thing and does
another is worse than one that plainly will not go.


## Two silent losses, a stop that did not stop, and a light that says paused

*Added 28 Aug, from Ken playing: "I couldn't turn off the ball... I
accidentally dropped it on a text pad and then undo returned a blank pad...
When all robots are paused it is easy to forget that... I dropped a PNG file
on the desk and all I see is '(a picture on the way)'... the anima-gadget
ends up on the desk instead of inside the panel... testing the library became
very slow."*

### The stop that did not stop (my regression, one round old)

Measured: "." DID quiet all three of the ball's panels — and the ball kept
gliding, 0.649 further in the next 120 frames. Rebuilding Pong on the world's
clock made the ball a plain pad carrying a SPEED, and `advanceMovers` only
ever gated GADGETS on their panel being dirty; a plain thing with a speed
"simply moves". So stopping the robots that drive a ball no longer stopped
the ball. Off has to mean off: stopping now parks the speed (kept, not
thrown away, because the gadget that set it is asleep on a bare nest and will
not set it again), and starting puts it back. Drift after "." is 0.0000 now,
and SPACE sends it off again.

### Undo was rebuilding the world from the wrong description

"Undo returned a blank pad" turned out to be the small visible corner of a
much larger loss: undo returned a world with **no colours, no names and
nothing bound to anything**. Snapshots are taken with `specOf`, which
describes a thing for MATCHING — what a robot's thought needs, where "a
pad" must not mean "a YELLOW pad called the ball". Rebuilding from that
description gives you one of the kind, not the thing.

`specOf` keeps its matching shape. A `full` spec now also carries look,
label, boundTo, ghost, gadget, speed and shape, and only the snapshot asks
for one. Measured before: after an undo, every lid on the bench had
`label:null, bg:null, boundTo:null`. After: names, colours and all four
bindings survive, and the held ball comes back yellow and called "the ball".

### A pad's name was never saved at all

Found while fixing the above, and worse in its way: `thingOut` wrote a label
for scales, rooms, boxes, nests — every kind except the commonest, the
pad. Save a world and open it and "the ball", "the bat" and "rally" were
gone. That also blinds Marty, whose facts call things by their names. One
line in the common block; the round trip now keeps all three.

### A named thing is not spare words

The ball did not "get dropped on a text pad" so much as get EATEN by it: pads
concatenate at the edges, and the ball's own words were empty, so it vanished
without changing the card by a letter and took three bindings with it. A pad
that has a name, or that behaviours are bound to, now refuses: *"the ball" is
not spare words — 3 behaviours work on it. Drop it in the MIDDLE of a pad to
ride there, or take its name off first.*

### A paused workshop looks paused

Ken's own suggestion, and the right one: nothing moves while the robots hold
still, so there is no motion to notice the absence of. The key light goes
cold and low (3.5 to 1.15, warm white to blue-white) and the ground goes from
#141821 to #0d1a2b. Unmistakable at a glance, and not a word written anywhere.

### The picture that could hang for ever

A 3.9MB photograph drops and lands here in under a second, so the stuck
"(a picture, on its way)" is the big-file case — and an `Image` that
neither loads nor errors leaves that pad saying it for ever. Two guards, both
of the same shape as the artifact-sandbox rule about racing every promise: a
picture bigger than 1400px on its long side is REDRAWN smaller before it is
stored (a 5MB data URL riding in every save and every copy of the world is
its own bug, and PNG gives way to JPEG past 900KB), and the load is raced
against a 12-second clock so silence is impossible by construction.

### The card that flew to the table

It cannot live inside the panel — a behaviour filed in another panel never
gets a turn, which is why it goes back out — but flying to an arbitrary free
spot and saying nothing is what makes a rule look like a bug. It lands
BESIDE the panel now (measured 0.65 away, was across the table) and the
workshop adds the reason to what binding already said.

### The library slowness: measured, and not a leak

No room leak (18 rooms = 3 + one panel each for fifteen gadgets, and the
trays are invisible), and numbers CHURN rather than accumulate (110 down to
49 over 600 frames). The cost is the step-based robot cycle itself: ONE
step-based gadget is 17-23ms a frame, so switching on a shelf full at once is
150ms+ a frame by arithmetic. The speed-based pair added last round is
0.1ms. This is the argument for built-in speed for the third measured time.
Still open, and needing Ken's steps: the field of desks in his screenshot —
switching gadgets on leaves no VISIBLE room here, though each switched-on
gadget does consume a bench spot (21 to 36).


## Why a robot's round cost eight milliseconds

*Added 28 Aug. Ken: "I don't understand why the library is slow. Why should
'one step-based gadget costs 17-23ms per frame' take that long?" A fair
challenge to a number I had reported without explaining.*

The frame grew a profiler (`__nano.profileFrames`), because that claim has to
be answerable per phase rather than shrugged at. With one step-based gadget
running: `tick` 8.0ms, `processDirtyRooms` 7.5ms, everything else 0.4ms —
and the rooms figure is partly a BUDGET, since panel work is deliberately
capped at 8ms a frame so behaviours cannot eat the whole thing.

Then the same question one level down. `moving right` — ONE robot, two
steps — runs 0.903 rounds a frame at 8.23ms a round. Building the pieces a
round needs, measured by making forty of each:

| piece | cost |
|---|---|
| an empty box | 0.09ms |
| a three-hole box | 0.32ms |
| a number | 0.35ms |
| **a text pad** | **1.04ms** |

A message box `[move | across | 1/60]` is a box, two pads and a number =
2.75ms predicted, 2.76ms measured. A pad costs a millisecond because its face
is a 512x384 canvas and the fit is a SEARCH: wrap the words, measure them,
shrink, wrap again, measure again, until they fit.

And every one of those faces was being painted inside a FOLDED panel, where
nobody could see it, for a copy that a bird carries off and the round
destroys.

So painting waits. A pad built while a panel works out of sight records its
words and paints nothing; a bounded list catches up the moment anything could
actually look at it (checked every frame, not every half second, so a pad set
down in front of somebody has a face immediately). Measured after: a round is
**3.95ms**, the frame 7.43 to 3.57, one `bouncing` 15.9 to 8.6, and the whole
shelf of fifteen at once 24.5 — from a state where the same measurement
timed out. Same rounds per frame (0.903 both times): the work is identical,
the waste is gone.

Proved correct as well as fast: open a running gadget's panel and the pads
inside show their words, ink on the canvas, nothing left due.

## TOUCHED was the wrong word

*Ken: "I meant what does it mean to be 'touched'? If it means to be clicked
on that picks it up. If it means another object collides with it then touched
isn't the right word."*

It has only ever meant the second, and he is right that the word is wrong —
the shelf was even inconsistent with itself, carrying "reverse on collision"
and "make a sound on hit" beside "grow when touched". The cards say **grow
when bumped** and **shrink when bumped** now, and the manual says what bumped
means and that clicking is not it.

The CHANNEL keeps its stored name (`evt-<lid>#touch`), because every saved
world in existence spells it that way and renaming it would break them all.
The message surface accepts `bump`, `bumped` and `hit` as the same word.

## The tooltip that promised what the code would not do

*Ken: "The tooltip correctly says I can drop the panel on the other panel but
when I do it isn't added to the panel but shows up next to it."*

The tip said "Drop to put that on the panel — it stays glued to X", which is
true of everything EXCEPT a behaviour: a behaviour binds to the panel's thing
and waits beside it, because one filed inside a panel never gets a turn. The
tip now says that, for behaviours only. A promise the code will not keep is
worse than no promise.


## What a round spends now, and how far nesting got

*Added 28 Aug. Ken: "what is taking so much time if the robots are not seen?"
and "Panels should be able to nest to convey different purposes (e.g.
movement vs sounds)... when not seen they can be implemented as a flat list
if that is better."*

### The remaining milliseconds

Not the faces any more, and worth saying exactly what instead. Per round of
the simplest gadget, measured by patching the browser's own APIs:

| what | per round |
|---|---|
| canvases allocated | 15.5, costing 0.074ms |
| `measureText` calls | 10.3, costing 0.148ms |
| `getElementById` (UI churn) | 7.3, costing 0.012ms |
| **everything else** | **~3.7ms** |

So painting and the interface are now 6% of it. The rest is the workshop
being literal: a round BUILDS a message box out of real meshes, materials
and textures — about twenty objects — hands it to a bird, delivers it,
and throws it away. A message here is a thing you could have picked up, and
that is not a metaphor in the implementation either.

Cross-checked against a second gadget: `bouncing`, with five robots and two
messages a round, costs 3.07ms a round against `moving right`'s 3.5 with one
robot and one message. The cost tracks MESSAGES BUILT, not robots matched —
which is the honest signature of "construction is the cost".

The next win, when it is wanted, is the same trick one level down: a pad
built out of sight still allocates a canvas and a texture it may never use.
Make the canvas itself lazy and a round should fall again.

### Nesting: half done, and the half that is missing is named

Ken asked for panels inside panels — a macro behaviour whose parts are
grouped by purpose — and said the implementation could keep them flat when
not seen. Both suggestions were right, and the first half works:

* **Switching nests.** SPACE on a macro sets every behaviour grouped inside
  its panel going, each in its own world, and "." rests them all. A panel
  whose work IS its parts (no robot of its own) is no longer refused with
  "nothing to run yet".
* **The scheduler reaches them**, by Ken's flat list: every tray is
  registered as it is made, because a nested tray sits on no bench the
  scheduler walks — the bench it belongs to is a snapshot that only exists
  while that world is the current one. That snapshot staleness is exactly
  what made the first, scoped attempt find nothing.

What does NOT work yet, stated plainly: a part inside a panel cannot move a
thing. `thingPlace` answers only for things standing on the CURRENT world's
bench, and while a nested part takes its turn its own world is not the
current one, so its thing has no place to move to. Nesting therefore groups
today; it does not yet drive. Making it drive means resolving a thing's place
against the world it LIVES in rather than the world that happens to be
loaded — a contained change, but its own piece of work.


## Nesting, finished — and the last of the paint

*Added 28 Aug. Ken: "You are right that a nested panel on a panel does not
drive its object but the object of the top-level panel is a part of. If it is
removed and its object is restored then it can run independently." And: "The
lazy allocation sounds good - do it."*

### The semantics were the missing piece, not the machinery

That one sentence dissolved the blocker I had reported. I had been looking
for a way to let a nested part move a thing inside its own panel; the answer
is that it should not be driving that thing at all. A part drives the object
of the panel it is PART OF: the macro's thing, reached by an ordinary bird,
exactly as a top-level behaviour reaches a thing on the table.

With that, one guard was left, and it was judging the wrong subject:

    const outOfPlay = (t) => !!(t.__owner && !thingPlace(t.__owner));

OUT OF PLAY exists so a behaviour whose thing is off the table — in a hand,
in a hole, on Mimi's platform — does not spin uselessly. But it asked about
the CARD, and a part nested in a macro's panel is on no table of its own, so
it was silently denied every single turn: dirty, registered, never run. It
asks about the thing the behaviour DRIVES now. Measured: the outer star moves
2.73 across the table, driven by a part living inside a macro's panel, and
"." on the macro rests it.

The scheduler half from the round before — Ken's own flat register of every
tray, because a nested tray sits on no bench the scheduler walks — was
right and stays. Check twenty-nine: "panels inside panels".

### The last of the paint

Deferring the PAINT left the allocation behind: a pad built out of sight
still made a 512x384 canvas and a GL texture it might never use. Now the
canvas is made the first time something is actually drawn on it, and every
unpainted pad shares one 1x1 texture until then. Canvases fell from 15.5 a
round to 11 (what is left is the numbers, which have their own faces), and a
round from about 3.5-4 to a warm median of **2.78ms** across eight samples.

The whole journey, for the record: **8.23ms a round** before any of this,
**~3.9** once faces stopped being painted out of sight, **2.78** once they
stopped being allocated out of sight. Same rounds per frame throughout —
0.903 — so the work is identical and only the waste is gone. Timing here is
noisy enough that single runs mislead: the first measurement after the change
read 4.7 and was cold-start noise.


## The picture was always there; the screen was showing an older upload

*Added 28 Aug. Ken: "The screenshot shows the result of dropping the same file
on the desk 5 times - it worked fine 3 times."*

The same file, three times right and twice wrong, is not a file problem and
not a decode problem. It was a texture problem, and my own state-checking is
what hid it: every probe I ran asked whether the picture had LOADED, and it
always had. The canvas held the picture perfectly. What the screen showed was
an upload made before it.

A pad takes the PICTURE'S PROPORTIONS the moment one loads — that is the
point of the aspect code — which resizes its face canvas. Measured on a real
drop: 512x392 becomes 512x398. And a resized canvas needs a fresh GL texture:
the number faces have said so in a comment for ages ("updating in place trips
glCopySubTextureCHROMIUM against the old allocation"). The pad never did it.
So the canvas was repainted with the picture and the GPU went on showing the
words "(a picture, on its way)", for ever, over a picture that was sitting
right there.

The pad renews its texture on resize now, exactly as the numbers do. Check
thirty — "a picture arrives" — asserts all three parts: the canvas really is
resized (392 to 398), the texture really is a NEW one, and the face really
carries the picture.

Two lessons worth keeping. First: when a thing is reported as INTERMITTENT
with identical input, stop looking at the input. Second, and sharper: I
tested `__imgEl` and `userData.img` and declared the path healthy three
rounds running. Those are the app's opinion of itself. The pixels are the
evidence, and the pixels were never in question either — what mattered was
the thing between the canvas and the eye, which nothing I had written could
see. A test that cannot see what the user sees is not testing what the user
reported.


## A panel you can drop into, a sound that listens, and a turtle in Logo units

*Added 28 Aug, from two sessions of Ken's notes.*

### The drop that finally does what the tooltip said

A behaviour dropped on a panel goes INSIDE it now. It was kept outside for a
reason that had stopped being true — "a panel filed inside another panel
never gets a turn" — and panels nest as of this morning. It binds to what
that panel's thing is bound to, which is Ken's own rule; and taking it out
again releases it, so it works on itself as a behaviour on the table should.

Putting parts INSIDE raised a question the round before had not: with the
card no longer on the table, what does a person press? The thing itself.
SPACE on any thing now starts the behaviours grouped inside its own panel as
well as the ones bound to it from outside. Measured end to end: drop
"moving right" on the star's panel, press SPACE on the STAR, and the star
crosses the table (0.9 to 1.53); "." rests it.

### A sound answers the box that makes one

Ken gave a sound's bird a [frequency | seconds | shape] box and nothing
happened — worse, the box was swallowed, because a sound answered only
[play] and [stop] by post. The parser is shared between the hand and the bird
now: 440, a half, sine, delivered by bird, and the sound sings.

### The turtle in Logo's units, and its box labelled

"fd 100 should move the distance that 1 does now." The scale went into the
BOX rather than into the robots: hole 9, **step size**, one hundredth,
multiplied into every step. `forward 30` now moves 0.3 — exactly what
`forward 3/10` moved before — so `forward 100` is a stride and a child who
wants a different gait changes one number in plain sight. All ten holes carry
their names on the box: my thing, heading, letterbox, sine, cosine, across
step, away step, pen down, pen up, step size.

The pen was never broken (the suite's own reading was `strokes=0/1/1`
throughout); at the old scale an `fd 100` flung the turtle into the wall,
which is what "pendown didn't seem to have an effect" looked like.

Two test lessons from the same change. Adding two robot steps to a turtle
order made the check's 220 frames too few, so I raised it — and it still
failed, because raising the budget was the wrong fix for the actual cause: I
had renamed `forward 3/10` to `forward 30/1` everywhere except the BACKWARD
order, so `orders['forward -3/10']` was undefined and the check was handing
the turtle nothing at all. A test that silently gives nothing looks exactly
like a thing that silently does nothing.

### Also

Notebooks have PAGE NUMBERS, on every page whether or not anything is filed
there. And a copy taken from a page now starts where its picture lies, so it
lifts off the page you took it from instead of appearing above the book and
flying in from somewhere else.

Marty was blind to what is attached to a thing: Ken held an imported picture
with two behaviours of its own and was told he was holding a blank pad. The
facts name a picture as a picture now, and list both the behaviours bound to
a thing from the table and the ones grouped inside its own panel.


## The pen was drawing on the floor

*Added 28 Aug. Ken, for the third time: "When you say that 'pendown' works
why don't I see a trail?"*

Because there was no trail to see. Every stroke was being laid at **y =
0.005** — five millimetres above the FLOOR — while the turtle drawing them
stood at y = 0.865 on the table. The chalk was under the furniture, hidden
by the table top from every angle a camera can take.

A thing on the bench carries the table's height in its own y; the stroke
code used a bare constant and never did. It takes the drawing thing's own
height now (its y less its resting thickness, plus a hair): measured, the
strokes land at 0.846 with the table top at 0.842 and the turtle at 0.865 —
chalk on the table, under the turtle, where a person can see it.

**And the suite said PASS the whole time.** Its pen test counted meshes of
the chalk colour. That is the third time in a week the same mistake has cost
Ken a report: the picture that had "loaded", the behaviours that were
"registered", the strokes that "existed". Existence is what the program
believes; POSITION is what a person sees. The check now measures each
stroke's height against the turtle's and counts only the ones near it, so a
trail on the floor fails.

## Also this round

**Hole labels at twice the pixels**, in darker ink, and set further out in
front of their holes — what stands IN a hole leans over the plate, and a
nest was sitting on the word "orders". Ken: "even closeup it is hard to read
the box labels".

**A pad can have no paper.** `[set | background | none]` clears the face and
makes the slab's sides invisible, so what is written is all that shows. The
turtle's shell uses it: a turtle rather than a turtle on a tile.


## Facing: the turn made visible

*Added 28 Aug. Ken: "right rotates the pad. I think we need the convention
that a heading of 0 points to far edge of the table or the far edge of the
containing pad."*

The convention he asked for was already half-present and never said out loud.
A step forward has always been across = **sin**(heading), away =
**cos**(heading) — which IS "zero points at the far edge, degrees clockwise".
All that was missing was for the thing to be turned as well as counted.

`facing` joins the message surface: `[set | facing | 90]`,
`[move | facing | 30]`, `[query | facing | bird]`, with `heading` and `turn`
accepted as the same word. It is stored on the thing, so it saves, reloads
and survives an undo like any other part of what a thing is.

The frame comes free for riders: a child's rotation is measured in its
parent's, so a thing on a pad turns relative to THAT pad's far edge without a
line of code for the case. Ken named both halves of the convention in one
sentence and the second half cost nothing.

The turtle's `right` now does two things where it did one: adds to the
heading number, then fills a `[set | facing | _]` from that same number and
hands it to the thing. Measured: `right 90` turns the pad a quarter turn and
the next `forward 30` moves 0.3 ACROSS and nothing away — it walks where it
points, which the check now asserts as a pair. A turtle that points one way
and walks another would be a lie told in pictures.


## A coloured pen, and the right angle that was the edge of the pad

*Added 28 Aug. Ken: the trail should be a first-class object that can be
vacuumed off even on a pad; pen colour and width; and "the screenshot is fd,
rt 30, fd but it looks like it did a right 90 instead".*

### The 90 degrees was the pad running out

Measured on the table: leg one bears 0, leg two bears 30, the turn is exactly
30. Measured with the turtle riding on a pad — Ken's screenshot — leg one
bears 0 and leg two bears **90**, with the legs different lengths (0.242 and
0.15).

Nothing is wrong with the turn. The pad in the picture is 0.68 deep and the
turtle's stride is 0.3: leg one spent the depth, and leg two's AWAY component
was clamped flat at the edge, leaving only its across part — which is a
right angle drawn by arithmetic that never happened. The turtle drew what it
was allowed to do rather than what it was told to do.

The remedy is already in the world and this is exactly why it was put there:
STEP SIZE is a number in the turtle's box. A turtle drawing on a pad wants a
smaller stride, and changing one number is the whole of it. What is still
owed is the honesty — a move flattened by an edge should say so, rather than
leaving a drawing that quietly lies about the angle it was given.

### The pen

`[set | pen | red]` and `[set | pen | 3]`: a colour is any colour the
workshop knows, a number is how many ordinary widths wide. Both are kept on
the thing that draws, so two turtles can hold different pens, and each stroke
keeps what it was drawn with — a line can change colour halfway. A new
colour also breaks the line, so the joint is not drawn in the wrong one.

Chalk comes off: a stroke answers Dusty, and the one he is pointed at is the
one that goes. Not yet a thing you can pick up and file — that wants a
record of its own and a place in the saved world, which is the rest of Ken's
"first-class object" — but a drawing you can correct rather than only clear.

Found while testing, by round-tripping a world: whether the pen was DOWN was
never saved. Colour and width went in with the rest, and the state that
matters most was missing. A world saved mid-drawing goes on drawing now.


## The imported world arrives whole

*Added 28 Aug. Ken: "the idea of importing a world as a notebook breaks
connections between objects - maybe the contents should be in one long box."*

He is right, and the diagnosis is the rule that makes copies safe. A page
hands out a COPY, and every copy is rekeyed so it cannot steal the mail of
the original — the copies-are-wholly-their-own rule, with its own check.
Taking the things one page at a time renames each of them SEPARATELY, so a
behaviour taken from one page goes on naming a ball that only another page
knows: the binding survives as a name pointing at nothing. That is the thing
that bit him back in round 34, when gadget-Pong came out of a notebook with
its bindings cut, and I diagnosed the symptom without seeing that the shape
of the import was the cause.

One box fixes it because rekeying happens ONCE for whatever is taken and is
consistent inside that one record. Page one of an imported world is now the
whole world in a box with every hole named — "the ball", "the bat",
"rally", "bouncing at a speed" — and the pieces keep their own pages after
it, for borrowing one thing.

The two properties pull against each other, so the check asserts both at
once: what comes out of the box still knows what came out with it, AND a
second take shares no name with the first. Measured: four bindings, all
resolving inside the box; second copy L915, L916, L917 against the first's
V901, V902, V905, no name in common, and its own four bindings resolving
inside itself.

The other half of why this works is worth writing down, because it is not
obvious: lifting a thing OUT of a box is a move, not a copy. Nothing is
renamed a second time, so a world can be unpacked hole by hole onto the table
and stay wired the whole way.


## A step is one move, and pendown remembers where it stands

*Added 28 Aug. Ken: "the movement is still wrong. I did forward 30, pendown,
forward -30, right 30, forward -30. That should have produced only 2 segments
with a 30 degree angle between them" — and the screenshot is a staircase.*

Two bugs, and the pen was telling the truth about both.

**A step was TWO messages.** `[move | across | ...]` and then
`[move | away | ...]`, each a move in its own right, so the pen drew an
across-only stroke and then an away-only one: a right angle per step, with
the net displacement perfectly correct all the same. A step is now one
message — `[move | position | [across | away]]` — with both legs filling in
the two numbers before anything is sent. One straight line per step, and half
as many messages.

**Pendown forgot where the turtle was.** It cleared the last place, so the
first move after a pendown had nothing to draw FROM and drew nothing at all.
Ken's five orders came out one segment short and the missing one was always
the first. Putting the pen down now records where the thing stands.

Measured on his exact sequence: two strokes, each 0.3 long, at 90 and 120
degrees — two segments with thirty degrees between them.

### Why none of my measurements caught either one

Because they all asked where the turtle ENDED, and the end was always right.
A staircase and a straight diagonal have the same endpoint; a drawing missing
its first segment ends in the same place as one that has it. The turtle check
asserted position, then position and rotation, then position and rotation and
a count of marks — and sailed past a drawing that looked nothing like the
one it was asked for.

It now asserts the SHAPE: how many strokes, how long each is, and the angle
between them. That is what a pen is for, and it is the fourth time this week
the fix has been "measure what the person can see" — the picture that had
loaded, the behaviours that were registered, the strokes that existed, and
now the strokes that existed in the right number and the wrong places.

**And it immediately earned its keep.** The new assertion failed on its first
run with THREE segments, which turned out to be nothing to do with the
turtle: pen strokes are plain meshes on the bench root rather than bench
things, so clearing the table for a new world left every line from the last
one lying on it. A world starts on clean paper now.


## The turtle in the air

*Added 28 Aug. Ken brought the convergent 3D-turtle vocabulary — move plus
yaw, pitch and roll, in the turtle's own frame, borrowed wholesale from
aeronautics — and, worth more than the vocabulary, a warning: most
implementations compose those three as sequential local-axis Euler updates,
which drifts and is sensitive to the order it is applied in.*

So the frame is ONE QUATERNION, multiplied on the right by each turn and
renormalised. Right-multiplication is what makes an axis local; associativity
is what makes a hundred small turns land where one big turn does. The three
names are not three angles kept side by side — they are three ways of
multiplying the same object, which is why there is no gimbal to lock and no
order-of-operations special case between them.

Measured, because the warning deserved an answer and not a promise: ninety
one-degree yaws give the quaternion [0, 0.7071, 0, 0.7071]; one ninety-degree
yaw gives [0, 0.7071, 0, 0.7071]. Identical to four places.

**The message surface grew a third dimension**: `up` (a place), `yaw`,
`pitch`, `roll` and `forward` (all relative, all in the thing's own frame),
and `home`. Turns refuse the verb `set` and say why: a turn is relative by
nature. Pitch is nose-UP for a positive turn, as "tilt up" means everywhere
this vocabulary comes from, so its axis is the thing's own left.

**And the pen climbs with it.** A stroke was a flat bar at one height because
everything that drew was flat on the table; it is a bar between two POINTS
now, turned along whatever direction the turtle actually travelled, and going
straight up draws too.

### The example, and the honest part of it

`examples/behaviours/turtle3d.world.json`: a gadget with seven robots —
move, yaw, pitch, roll, pendown, penup, home — each hearing a word off the
same kind of letterbox the flat turtle uses, filling a number into a message,
and handing it over. Measured playing: a spiral staircase of move / yaw 30 /
pitch 30 draws three strokes climbing 0.846, 0.921, 1.118 and ends 0.392
above the table.

A card in the world says the uncomfortable part out loud, because it is the
interesting part. The FLAT turtle works out its own trigonometry — a
heading, a sin badge, a cos badge, a sum you can lift the lid on. A turn in
SPACE is not an angle you can keep in a hole; it is an orientation, and two
of them compose by quaternion multiplication. Pretending that could be built
from number badges on a table would be a lie, so the frame is built in — as
speed is, as the table's edges are — and the robots do the part robots are
good at. Check thirty-two asserts the climb, the drawing in the air, and the
four yaws that close.


## Trails are things, models arrive, and the edge speaks

*Added 29 Aug. Ken: the swept trail "should be a new 3D object, and the 2d
trail should work this way too"; "maybe it is time to support the import of
models. Can you make a toy airplane and a dragonfly"; and "I had the turtle
move forward but nothing happened".*

### kind: trail

The note-pad in Dusty's bag is gone. Each stroke now remembers its own
endpoints, so sweeping a trail rebuilds it as a THING — segments kept
relative to its own base, each with the colour and width it was drawn with.
Out of the bag it is an ordinary object: put it down anywhere, save it, copy
it, sweep it up again. 2D and 3D are one code path, since a flat trail is
just one whose segments have no height.

### kind: model

A model is parts — box, sphere, cylinder, cone, each with a size, a place,
a turn in degrees and a colour. Deliberately that and nothing more: the toy
airplane is eight parts and a hand-readable file, rebuilt from primitives
with no loader and no download. A model with a lid is LIVE, so behaviours
bind to it and birds deliver to it; `examples/models/` has the airplane and
a dragonfly, both authored facing heading zero so the 3D turtle's frame
agrees with their noses.

Measured end to end: import the airplane, drop "a 3D turtle" on it (8
references re-pointed), pendown, pitch 30, move 30 — the airplane climbs
0.15, banks, and draws its climb in the air. And the swept trail of that
flight comes out of the bag as one thing, which survives a save and a load
along with the banked airplane.

**An imported thing gets fresh names now**, exactly as a notebook page gives
them: importing the same file twice used to put two things with one lid on
the table, where the inner one registered last would quietly take all the
mail — the copies-clash bug by another door. The check imports the airplane
twice and asserts the lids differ.

### The edge speaks

"I had the turtle move forward but nothing happened" was a turtle standing
against the table's edge, ordered into it: the clamp ate the whole move and
said nothing. Measured on the repro before fixing: the shell at z=2.2 with
the wall at 2.23 moved 0.03 and then nothing, silently. A message-driven
move now wholly absorbed by the edge says: "…is against the edge — that
move could not go anywhere. Turn it, or move it the other way." A move that
still travels PART of the way stays quiet, because something visibly
happened.

### Also

The turtle gadget cards in both turtle worlds stood at the far corner of the
desk, where they read as dropped rather than placed; they stand beside the
bird now, so behaviour, bird and shell read as one working group.


## Zeno's postman, and the turtle that dispenses solids

*Added 29 Aug. Ken: "make another example program where one robot gives the
bird 1/2, 1/4, 1/8 and so on and the other robot keeps a running total" and
"yes let's add the BeetleBlocks shape drops".*

### zeno.world

Two houses and a bird. The halver's whole program is two ordinary moves:
copy the fraction and give the copy to the bird; drop a x1/2 badge on what is
left. The totaller's program is ONE move: take the delivery off the nest and
drop it on the running total — a number dropped on a number adds itself, so
the total IS the arithmetic, with no adding machine anywhere. An empty nest
puts the totaller to sleep; it works only when the post comes.

The reason to do this here rather than in a spreadsheet is on a card in the
world: the numbers are EXACT. The check asserts the invariant, not a
tolerance: the total is (2^k - 1)/2^k at every moment — measured run,
255/256 — the denominator a power of two, the numerator exactly one
behind. THAT is why it creeps toward 1 forever and never arrives, and a
child can read the missing part off the block.

### [drop | sphere | 1/10]

BeetleBlocks' third idea, after move and the aeroplane turns: the turtle is a
dispenser. Sphere, cube, tube and cone land at the thing's position and
orientation (a tube lies along its forward), in the pen's colour, and they
JOIN THE PEN'S CURRENT TRAIL — so a sculpture of shapes and lines sweeps
up as one thing and survives a save, because trails already knew how to be
things. Measured: sphere, forward, cube, pitch 45, forward, tube — four
pieces, one sweep, all four still there after a save and a load.

One catch found the moment it was driven: the message surface's what-list
rejected 'sphere' before the drop verb was consulted, so the first sculpture
was one line and three silently swallowed messages.

### The leaked speed the new checks exposed

Adding two checks made pong "come apart" — same numbers every run, flips
exactly HALVED. Pong's pass had depended for weeks on a `D.speed(2)` leaked
from the shelf check two checks earlier; the new zeno check restored the
speed to 1 on its way out, and the inheritance broke. Pong now sets its own
speed and says why. A check that depends on a setting must set it — the
suite-hygiene twin of "a test that cannot see what the user sees".


## The scale weighs piles, the glass-house robot walks, the bird lands right

*Added 29 Aug. Four reports.*

### A third weighs the same as three ninths

Ken's design, implemented as stated: a plain (+ or -) number dropped by hand
on a number in a scale's pan STACKS instead of calculating, and the scale
weighs the pile — so the fact is discovered on the beam, not computed.
Measured: 1/3 against 1/9 tilts left; a second ninth, still left; the third
ninth and the beam is level, with the pan's own number still reading 1/9 and
the pile riding on top. Piles save, load, and come apart by picking a cube
back off.

The first cut broke three golden worlds inside the hour: factorial and two
infinity activities have ROBOTS that count by dropping badged numbers onto a
number in a pan — fetch-and-op, the oldest idiom in the workshop. So the
pile is the HAND'S gesture: a person's drop stacks, a robot's drop
calculates as it always did, and the goldens are byte-identical again. The
suite caught the collision before any person did, which is the golden
worlds doing exactly their job.

### The glass-house robot performs its round

The round itself still runs in an instant, offstage — that part is the
engine/view split, still on the wishlist — but each step names the hole it
touched, and the miniature now WALKS to each of those holes in turn, faces
it, bows, and comes back to the desk. Not the claw's full mime; the walk,
which is what reads at toy scale through glass. Measured in zeno.world: the
halver's robot leaves the desk, visits the bird's hole and the fraction's,
and returns.

### The bird lands where the mail is FOR

The turtle-panel-on-airplane-panel case: orders were delivered correctly,
but the visible bird flew to the middle of the desk, because she flies "to
the nest" and the letterbox lives inside a folded panel whose world position
is the tray's parked spot. A delivery's visible landing is now the thing a
person understands the mail to be for: the behaviour's bound thing (the
airplane), or failing that the behaviour card itself.

### The activity1 report, measured and NOT changed

"When I turned on the add 1 house all the houses became active. That
shouldn't happen." Reproduced step by step: Doubler and Split are AUTHORED
armed (dirty: true in the file), run once at load, and settle into a doze on
their empty nests. Turning on Add 1 posts naturals; the dozing servers wake
per delivery and doze again between — which is the flock/doze semantics the
bank canary depends on, and what this world's own cards describe. The rule
that must hold DOES: a house stopped by its lever stays stopped while the
post piles up on its nest (measured: Doubler stopped, pile growing, Split
serving on). Nothing was changed; if the intent is consumers that stay dark
until their own lever is pulled, the world should author them stopped, and
that is a one-line change to the activity file — Ken's call, not mine.


## The scale stacking, reverted — and the principle it broke

*Added 30 Aug. Ken: "Your solution is OK but breaks the idea that what robots
do and what the user does on the desk should not differ. I suggested it for
pedagogic reasons but now think it was a bad idea so let's revert the scales
to how they were before. Keep in mind the principle that training and
directly doing should not differ."*

Reverted whole: `panWeight`, `stackOnPan`, `unstackFromPan`, `scaleHolding`,
the combine branch, the save/load of piles, the manual paragraph and the
check. `scaleTilt` reads the two pans again and nothing else. Thirty-five
checks, goldens byte-identical, no trace of the feature left in the source.

**And the version I shipped was worse than his objection made it sound.**
When stacking broke three golden worlds, I kept them green by gating it on
`!busy && !roomWorkBusy && !clawHeld && mode === 'world'` — "the pile is
the hand's gesture". That reads as a tidy narrowing. It is not: TRAINING is
not mode 'world'. So the same gesture meant two different things depending on
who made it and when. Demonstrate a stack to a robot and the demonstration
itself would have CALCULATED; the robot would then faithfully repeat
something the person had never seen happen. The gate did not narrow the
feature, it split the gesture in two, which is the exact seam the principle
exists to forbid.

**The principle, written down where the next idea will meet it:**

> What the user does by hand and what a robot does must be the same act. A
> robot is trained by watching a person do it, so any gesture whose meaning
> depends on WHO is doing it, or on which mode the workshop is in, cannot be
> trained — and a workshop where some gestures cannot be trained is no longer
> one language.

Worth keeping too: the goldens caught the collision within the hour, and my
response to a failing test was to add a condition until it passed. The tests
went green and the language got worse. A gate added to make a test pass is a
design decision in disguise, and it deserves the same suspicion as the
feature it is propping up.

The pedagogy Ken wanted — seeing that 1/3 weighs the same as three 1/9ths —
is still worth having, and can be had without a special gesture: three ninths
ADDED make a third, and a scale with 1/3 against 1/3 balances. If a "pile of
weights" is ever wanted for real, it wants to be a THING (a bag of numbers
with a value of its own), not a special case in what dropping means.


## A house shows the props its robot needs, and wears its name on the roof

*Added 30 Aug. Ken: "robots in transparent houses should pick from stacks and
use tools. But only display those stacks and tools it needs." And: "the label
on the side of the house with the switch isn't needed. And when the roof is
displayed let's add the label to the roof."*

### Only what it needs

A house reads its robot's program (its team's too) and lays out exactly the
stacks and tools those steps name: `newNumber` wants a number stack,
`newText` a pad stack, `vacuum` wants Dusty, and so on. They are tokens
rather than the real stations — a small pedestal with a couple of cubes on
it, a green cone for Dusty — standing along the back wall, and the round's
performance walks to them for exactly the steps that name them.

activity1 is the perfect witness and became the check: **Add 1** and
**Doubler** both make fresh numbers, so each shows a number stack; **Split**
only swaps two birds, makes nothing, and shows nothing at all. An opaque
house builds none of it, because a toy nobody can see into should not pay for
furniture. Measured: the robot's walk closes to 0.05 of the stack against an
arrival threshold of 0.06 — it really goes there.

The half that is still honest to state: the FETCH is not simulated, only
performed. The round already happened offstage in an instant; the walk is the
account of it. Making the walk and the work the same event is the engine/view
split, still on the wishlist.

### The name, off the switch and onto the roof

The right-hand wall carries the lever, and the label was printed straight
across the arm with the knob sitting in the middle of the word. Three walls
now — front, back, left — and the ROOF, which is the face you actually look
at from above and the only one nothing else was using. The roof plate lies
along the front slope (the cone is r 0.36, h 0.17, turned 45 degrees so a
face looks forward), lifted a hair off it.

One trap worth recording: `paintRoomLabel` runs BEFORE `makeRoom` in the
file, so `WALL_TOP` is not in its scope. The first version used it, passed
the syntax gate, and would have thrown at the first labelled room. Numbers
with a comment explaining where they come from, not a borrowed constant.


## The airplane takes off and loops, and the loop has no counter

*Added 30 Aug. Ken: "Make an example of the airplane taking off and flying and
doing a loop."*

### Three orders, for ever

The temptation was a program with a takeoff phase, a climb phase and a loop
phase, counting strides in each. None of it is needed, and saying why is the
example: **a constant turn per constant stride IS a circle.** The pilot's
round is

    move 10, move 10, pitch 30

and nothing else. Two strides per turn widens the arc, so the plane runs, lifts
and comes over the top rather than pivoting on the spot; twelve rounds close
the circle exactly. No counter, no phase, no comparison — which also means
there is nothing to get wrong when a child edits it. Change 30 to 20 and the
loop is bigger; change it to 0 and it flies straight until the table runs out.

### Two behaviours, one airplane, one SPACE

Worth having as an example in its own right: the airplane carries the 3D
turtle (rebound to it, so it owns <em>move / yaw / pitch / roll</em>) AND the
pilot, and pressing SPACE on the airplane starts both, because everything
bound to a thing starts as one. The vocabulary and the speaker of the
vocabulary are separate objects you can open, read and change apart.

The plane's pen is down, so the loop draws itself — and since a trail is now a
first-class thing, the flight path can be picked up and kept.

### Two measurements that changed the design

The first attempt was `move 25 / pitch 12`, which is a radius of about 2.4 —
the plane hit the two-unit height ceiling and flew a flat arc along it. Sized
down to `move 10 / pitch 30`, radius 0.38.

Then the back quarter of the loop clipped the near wall: a loop is a circle
standing on its start, so it needs a radius of room BEHIND the plane as well
as in front. The plane starts mid-table at z 1.70 rather than at the near
edge. The check asserts what a person sees rather than what ran: the drawn
path must be as tall as it is deep (0.75 x 0.75), the plane must climb past
0.6 and come back under 0.05, and it must still be on the table at the end.


## The two houses that never moved, and the bird that was never seen

*Added 30 Aug. Ken: "When I run the first infinity example I don't see a bird
leaving the Add 1 house to the other houses. I do see birds leaving the other
houses to the nests on the desk. And the doubler and split robots don't move
despite the computation proceeding."*

Both reproduced by measurement before anything was touched:

    Add 1:   walk=5.087  perf-frames=199
    Doubler: walk=0.000  perf-frames=0
    Split:   walk=0.000  perf-frames=0

and the topology explains the bird: Add 1's bird answers to `inf1-nat`, whose
only two nests are **In** (inside Doubler) and **Input** (inside Split). Not
one of them is on the desk.

### A robot woken by mail did its round somewhere the performance could not see

The glass-house performance was built from `ran`, read straight after
`runProgram()`. A robot dozing on a nest does not run there: it runs from
`checkWaiting()`, which is BELOW, when its mail lands. So `ran` was 0 for
exactly the robots this activity is about, and the two that do the work were
the two that never moved. The performance is now built after the whole turn,
off `roundsEver` — a counter that only goes up, because `runCount` restarts
both at Run and every time a sleeper is woken, and so cannot answer "did a
round just happen".

That fixed the build but not the sight of it: Doubler walked 0.05. A house
driven by post is `dirty` for the one frame its round takes and quiet by the
next, and the walk only advanced while the house was working — so there was
never any time in which to walk. A performance is an account of a round that
already happened offstage in an instant; it is now allowed to outlast it
(`roomWorking(t) || t.__perf`). Measured after: 30.3 / 14.4 / 5.9, from
30.3 / 0.05 / 0.27.

### The courier only flew to the desk

A bird leaving a house hands her mail to a COURIER who flies it for real in
the world that will watch her — but only when the nest stood on the desk. A
nest inside another house fell through to the ordinary flight, which happens
inside the sending house's own tiny world at Instant: invisible by
construction, and the flight that says what the whole activity is doing.

The courier now flies to a nest inside another house as well, in the world
both houses stand on. Three things went wrong in the first cut, and each is
worth keeping:

- **It fed one nest.** Copies of a nest share a name and one bird feeds them
  all; the courier fed only the first found, so Split starved the moment
  house-to-house mail went by courier. The ordinary path had always done this
  with clone deliveries; the courier does now too.
- **It filled the air.** Letters to one name land in the order they set off,
  so a sender faster than a 0.9-second flight piles them up without limit:
  measured at 2384 birds over one desk. A cap of eight bounded it but was
  still a visible queue — Ken watched zeno's halver, whose whole job is to
  post as fast as it can, and saw eight birds stacked over the house. ONE
  letter to a NEST is in the air at a time now: a second one lands the first
  at once, which bounds the count AND keeps the pile in order, where simply
  skipping the flight would have reordered it. Measured on zeno: one bird,
  and the nest it feeds holds one thing rather than a backlog.

  Per nest, and the first cut counted per NAME — which the suite caught
  within the minute: copies of a nest share a name, activity1 has two of them,
  and each letter cancelled the other's flight in mid-air. Doubler stopped
  working altogether (walks 5.1/0.0/2.0, one number sorted in nine hundred
  frames). Each pile is its own queue and keeps its own bird: 5.1/5.0/2.0,
  seven crossings, five birds over the desk at the busiest moment.
- **A panel is a room too.** So every order posted to a behaviour's letterbox
  became a courier flight: the airplane's pilot posts three a round, and the
  suite caught it — the plane climbed and never came down. A folded panel is
  machinery, and its post arrives at once.

### The check that passed by luck

"the airplane loops" sampled the plane's height every 35 frames. The pilot's
round is three orders and the loop is twelve rounds — a 36-frame period. The
check was reading almost the same point of the loop each time, and whether it
ever saw the bottom was luck; a one-frame phase shift from an unrelated change
turned it red. It now records every frame. A sampling interval that lands near
the period of the thing sampled is not a measurement.

### And the check that would have caught all of it

The glass-house check asked whether the props were right and whether ONE robot
reached its stack. It never asked whether the other two moved, and never
looked at a bird — so an activity in which two of three robots stood still and
the mail teleported passed it clean. "a house posts to a house" measures the
walk of every house, the distance a bird actually flew across the desk, the
piles at the end, and the most birds ever in the air at once.


## A bird the size of the house she is delivering to

*Added 30 Aug. Ken, with two screenshots of zeno: "the bird is gigantic."*

She was, and it follows from the courier flying in the DESK's world: at desk
scale she is nine times the house she is aimed at, because a house's whole
interior stands at 0.11. Mail between houses is house-sized now — scaled to
0.3, lifted above the toy scale so she still reads as a bird crossing the
table rather than a speck. A nest ON the desk is unchanged at full size,
because that is the scale of the thing she lands on. Measured: 0.30 against a
house spanning 1.02.

## The suite writes its verdict to disk

*Added 30 Aug. Ken, watching a round take an hour and a half: "Is there a way
to address your need to wait so much of the browser channel?"*

Most of that hour was not work. Reading one line of text back out of the
browser — did the suite pass — was timing out more often than it answered, at
thirty to forty-five seconds a try, and a suite run takes four minutes. Eight
minutes of polling per run, five runs.

The sink that already takes the goldens takes the verdict now: the suite POSTs
`captures/verdict-<build>.json` when it finishes, so the answer is a `cat`
rather than a round trip through a wedged renderer. Named after the build, so
two runs at once do not overwrite each other. The other half was self-
inflicted: five tabs, each holding a live WebGL app, competing for the same
machine. Old tabs get closed now.


## She takes the rest with her

*Added 30 Aug. Ken: "I hear noises but I thought I didn't see birds even though
both houses are transparent. But they appear briefly above or between the
houses but their motion is so jerky it is hard to see any change."*

That is what capping the air at one letter per nest looks like from the desk.
The cap worked by LANDING the earlier letter to make room, so a sender faster
than a 0.9-second flight cut every flight short: a bird that blinks in and out
over the houses rather than one that crosses between them. Bounded, ordered,
and useless to watch.

A letter posted to a nest that already has a bird in the air JOINS HER now. One
bird flies at her own pace, carries whatever arrives while she is up, and sets
it all down in the order it was posted — the pile comes out right by
construction rather than by a rule, and the traffic is one bird per nest however
fast the sender runs. Measured on zeno: two birds over the desk, longest flight
1.88 across, **107 frames in the air** where before it was a blink.

She does not TOW it, though: the halver posting as fast as it can handed one
bird a tail of 241 pads. Four ride where you can see them; the rest ride along
unseen, and every one is still delivered.

## A pause cuts the power

*Ken: "When I paused the robots they turn back and forth — maybe this is good
or maybe we should think of pause as cutting the power to the robots so they
become still."*

Cutting the power. A robot holding still is what a pause looks like; one that
goes on swaying behind glass looks like a robot that ignored you. The room's
bustle — the sway, the walk, the chimney smoke — is gated on the same flag the
movers are. The lever still swings, because that is the switch you threw rather
than the work. Measured: the miniature stirs 0.0000 while paused and 110.6 over
the same number of frames running.

## Markdown on a pad

*Ken: "If a user imports an MD file then render the markdown on the text pad."*

A pad's paint centres every line in one size, which is right for a poem or a
word list and wrong for a document: headings, bullets and code all came out as
the same centred grey. A pad can be told it holds MARKDOWN, and then it is laid
out as a page — left-aligned from the top, headings in their sizes, bullets
hanging with their nesting, numbered lists, quotes ruled down the side, rules
ruled, fenced code in a mono face on a tint, and bold, italic and code read
inside a line. It picks the largest type at which the whole page still fits,
the same way the plain pad picks its size.

Only as much markdown as a pad can honestly show. Tables, links, images and
footnotes read as their own plain text rather than disappearing, which is the
better failure for a format nobody fully agrees on.

The mark lives on the PAD (`userData.md`), not on the file, and it is written
into the save record and restored BEFORE the words — so the first paint after a
load is already a page. That is the whole of what the first cut got wrong: the
import rendered beautifully and came back from a save as centred grey.

## Tests run silent

*Ken: "can you mute the app while you are running tests."*

Every one of a suite's thousands of rounds was chirping through the speakers of
whoever was in the room. `D.mute(true)`, called once the app has booted. NOT
through `setVolume`: that writes the preference to localStorage, and the suite
shares an origin with the workshop — muting a test would have muted Ken's own
desk, for good, from a page he never opened.


## A page needs pixels, and a backlog must not be performed

*Added 30 Aug. Ken: "The markdown rendering is working but it is blurry and too
low contrast." And: "the totaller produced a value with 38 digits and a stack
that kept growing (over 3000 numbers on it) This despite pausing the robots."*

### Blurry

A pad's face is 512 across whatever size the pad is, which is plenty for one
word at forty pixels and nowhere near enough for twenty lines of ten-pixel
type: a document pad is 2.5 tablets wide, so the same texture was stretched
over two and a half times the table. The canvas follows the pad's size now, and
a rendered page gets half again on top of that — 512 became **1920 x 1468**.
Anisotropy 4 to 8, because a pad on a table is always seen at a glancing angle.

Contrast was two things. The pad's navy (#1c2a52) is a colour chosen for one
word at forty pixels; under a page it reads grey, so a page is inked near-black
unless the pad has been told its own colour. And the paper's fibre flecks —
340 little strokes of grey and white — are noise behind small type, so a page
is drawn on clean paper.

### The three thousand

Not numbers: **queued animation steps**. Every delivery enqueued a four-step
tuck (slide the pile aside, drop the new one in, stack it back, refresh), and
zeno's halver posts as fast as it runs while the totaller takes one a round. The
queue reached **2983** — a workshop playing back a stack of tucks nobody was
watching, too busy to answer, and looking for all the world like it was still
producing after a pause. That is also why the pause seemed not to work: houses
DO stop when paused (processDirtyRooms has always returned early), but the queue
keeps draining while paused so the user's own actions can finish, and what was
draining was two thousand deliveries.

A delivery that arrives into a backlog is now TUCKED rather than performed: the
thing goes on the pile at once and the pile is restacked. The first letter of a
landing still flies and tucks properly, because that is the one you are
watching. Restacking is also what hides all but the ten a nest shows, so the
same fix cured the pile: before, every one of the pile's members was visible
(89 of 89, then 374 of 374), because the restack only ever ran at the end of a
tuck animation that was queued behind two thousand others.

Measured on zeno, before and after: queue **2983 to 0**, visible pile members
**89 to 10**, and paused growth **+93 to +0**. The nest still fills up — 162
letters waiting — because the halver really is faster than the totaller, and
that is zeno's own arithmetic honestly displayed rather than a bug.


## Pages, and a stop that sticks

*Added 30 Aug. Ken: "The readme.md in the behaviors folder renders like
screenshot 2 - not so good. Maybe when there is too much text to fit on a text
pad it can be viewed as having multiple pages." And: "when I typed '.' to the
halver house it kept running."*

### Shrink-to-fit is for a poem

The first cut chose the largest type at which the WHOLE document fitted, which
for an eighteen-thousand-character README is two hundred lines of grey thread.
A page is laid out at a size meant to be read — H/29, about fifteen lines —
and what does not fit starts the next one. The README makes twenty-three
pages, numbered in the corner. `]` and `[`, or PageDown and PageUp, turn the
page you are pointing at or holding; the arrows are left alone because they
already turn a pad. The page a pad is left on is part of the pad: it saves,
copies and travels with it.

One markdown rule I had skipped mattered more than the pagination:
**consecutive lines are one paragraph.** Most READMEs are hard-wrapped at
seventy characters, this project's included, so every source line became its
own line — broken mid-sentence, with any emphasis spanning the wrap left
unread as literal asterisks. Joined, the same file went from 44 pages to 23 and
started reading like prose.

### Off is a decision

A house's turn ends by working out whether there is more to do and assigning
that to `dirty`. A "." that arrived while the turn was running was therefore
undone a moment later, and the house carried straight on. The end of a turn now
respects a stop: `dirty = stopped ? false : cont`. Only the lever or SPACE
undoes it. Measured: three rounds at the stop, three rounds six seconds later.

### And the reason a round took so long today

Not the app: my own tool use. Every probe file written into the project opened
a browser tab that was never closed, and by the end eight of them were live at
once, each holding a renderer. Reads that had taken a second were taking
forty-five, and two suite runs never returned at all. Closed, the same probe
answered in seconds. The lesson for next time is the same one as the queue: a
thing that accumulates silently is measured only when somebody asks why
everything is slow.


## A running robot does not freeze the switches

*Added 31 Aug. Ken: "I entered the totaller house and restarted halver with a
space. But then the halver house refused to turn off either by '.' or toggling
the switch." And, when I could not reproduce it: "It doesn't matter whether I
enter the totaller house while halver is running or I stop halver before
entering and restart it after entering."*

That second message is what made it findable. My first attempt scripted the
sequence exactly and everything worked — because the totaller's robot was
mail-driven and happened to be dozing at every point I sampled. The condition
was never the ORDER of the steps; it was whether a robot was mid-round at the
moment the key was pressed.

Standing inside a house whose robot is working puts the CURRENT world into
'replay' — `enterRoom` starts that robot on purpose. Two separate guards then
fire, one for each way Ken tried:

- the keydown handler ran only when `mode !== 'replay'`, so SPACE and "." did
  nothing at all;
- `runRefusal` answered `roomLever` with *"One robot at a time — stop this one
  before setting another going"*, which is a rule about YOUR desk and was never
  meant to cover a house standing on the table.

Both are lifted for switches. A house and a behaviour are their own domains:
houses have always been allowed to work while you work and while another house
works, so switching one is not starting a second robot at your desk. What a
robot is working ON is still off limits while it works.

Measuring it needed the same care as finding it: a check that samples the mode
between rounds sees 'world' and proves nothing. The probe drives frames until
`mode === 'replay'` and presses the key in that very frame. Before: nothing.
After: `dirty=false stopped=true`, 0.0 rounds/sec.

### And the wrong fix I shipped and took back

Ken chose "rotate the entered world 180 degrees" for the robot that faces away,
and gave a good reason. I did it, measured it, and it was wrong: inside a house
the robot ALREADY faces you — you can read "the totaller" on its chest — and
the turn showed its back. What stands behind it is its DESK, so its work is
what is hidden, not its face. Reverted, with a note at the spot, because the
same plausible fix will look just as obvious next time.


## Stepping inside is the training view

*Added 31 Aug. Ken: "the point of entering the totaller house is for the user
to observe how it works. Seeing his back isn't helpful. And I don't see the
robot taking numbers off the nest stack and dropping them on the number.
Entering houses used to look very much like when training a robot or running a
just trained robot - why can't we restore that?"*

The tableau inside always WAS the training tableau — same middle desk, same
work spots, same robot body with the house's name on its screen. What differed
was the camera. The door's zoom animation lerps the camera 35% of the way
toward a house standing on the table, which ends LOW — about table height —
and close, and nothing ever restored it. From down there the robot's own body
hides its desk and the work spots laid out behind it (`reachLocal.z - i*0.62`),
which is the whole of "seeing his back" and of the invisible nest-to-number
round. Training looks right because the workshop camera is high (y 3.05) and
looks over the robot's shoulder.

So the door finishes the job: after the swap, the camera glides to the
workshop's own vantage, and the exit door does the same on the way out (it used
to strand you wherever you had orbited to inside). Measured: camera lands at
0.40/3.05/5.45 exactly, and standing inside the totaller for nine seconds shows
**eight rounds performed visibly** — the robot taking the top of the pile and
dropping it on the total, on camera.


## The robot reaches for the top of the pile

*Added 31 Aug. Ken: "When the robot takes the number from the top of the nest
stack it just magically appears in its hand. Let's animate something that
indicates taking an object off a nest stack. If the stack is too tall then
approximate it but otherwise have it reach for the top number and grab it."*

The take already walked to the nest and opened the claw — but the arm only
ever went to the one desk-height pose, and the top of the pile swooped down
into it. The grab pose is now aimed at where the top actually stands,
interpolated between the desk reach and the full copier stretch by the
pile-top's measured height. Both heights are measured off the template robot
at boot, the same way `reachLocal` always was, rather than guessed.

Two details worth keeping:

- **Aimed after the walk, filled in late.** `armTo` reads its pose at update
  time, so the pose object is completed in a step that runs after the walk —
  mail can land mid-walk and change where the top is.
- **"Approximate it" falls out of the clamp.** A pile taller than the arm
  clamps the pose at full stretch, and the thing crosses the remaining gap in
  the grasp settle, lengthened in proportion so a long grab reads as one
  rather than a snap.

The claw became measurable at the same time (`D.claw()` — pose and world
height), so the check is a number rather than an impression: over twelve
seconds of the totaller's rounds the claw peaks at y 1.17 against a resting
0.40, with the pile top at 1.06. A fixed desk reach peaks near its floor.


## The reach aims where the claw will be, and a dozing robot turns round

*Added 31 Aug. Ken, with a screenshot: "the robot is reaching to the wrong
place to take a number from the stack. Also my first and third test the robot
was faced away from the user. The second one was fine - not clear what the
difference is."*

### The aim

The height fix raised the ARM but never moved the AIM. The robot walks to
where the claw lands at the desk pose — standForPoint assumed reachLocal —
and the interpolated grab pose puts the claw at a different horizontal offset,
so the higher the pile, the further from it the claw arrived. The grip is now
measured in full at both poses (not just its height), standForPoint takes the
offset of the pose that will actually reach, and the whole decision — where
the top stands, the pose that meets it, where to stand so that pose lands on
it — is made in one place when the walk starts.

Measured over 27 grabs inside the totaller: worst claw-to-pile-top distance
0.284 (roughly one cube, part of it the intrinsic half-height of the grabbed
thing itself), claw peaking at 1.16. Before, the arm could be a full desk away.

### The facing

`enterWaiting` glides a dozing robot home in x and z — and kept whatever yaw
its last walk gave it. The scratch spots are BEHIND, so a round whose last
step touched one left the robot dozing with its back to you for however long
the next delivery took. Whether it did depended on the program's last step,
which is why it came and went between Ken's tests with nothing he did
differently. The glide home now turns the robot home too, by the shortest way
round. Measured: the dozing robot faces the eye by 0.89.


## Undo never mints a twin, and the robot reads its own notebook

*Added 31 Aug. Ken: "fix the bugs you listed and notebook copy on access by a
robot."*

### The twin

Round 53's mystery, finally reproduced by finding the right gesture: drop a
gadget into another gadget's OPEN TRAY, then undo. Tray interiors are
deliberately not rewound by undo (their worlds are live things a spec cannot
describe) — but the undo snapshot also remembered the drop as a bench spec,
and rebuilding that spec minted a SECOND pilot: one living on in the tray, one
fresh on the bench, both wearing the live name A903, the newcomer quietly
stealing the register. Ken's "extra copy", exactly.

The missing invariant: **a live name is never rebuilt while its owner
stands.** buildThing now looks the name up first and, if the registered thing
still exists, takes IT — detached from wherever it got to. For this undo that
is precisely the right motion: the pilot comes back out of the tray, the same
node, binding intact. One trap inside the fix: the reuse must NOT require the
node to be in the scene, because mid-restore the bench has been swept and the
tray holding the original is off the table at exactly the moment the check
runs — the first cut tested inScene and still made twins.

Measured: drop into tray, undo — one pilot, on the bench, boundTo kept.

### The notebook

Ken, earlier: "In original ToonTalk the notebook is shared by the user and
robots. I now suspect that is a mistake." Now: each ROUND, the first step that
reads the notebook snapshots its pages, and every read of that round comes
from the snapshot. The user can hold, flip or edit the real notebook mid-run;
the round is untouched and the next round sees the changes. The lock-out read
from the robot's side is gone too: a run used to DIE when the notebook was in
the user's hand ("there is no notebook here"), because mainNotebook() only
looked at the bench.

WRITES still go to the real notebook, on purpose: filing a result is how a
robot publishes, and publishing into a private copy that evaporates at the end
of the round would lose the work silently — the worse failure. Reads are the
robot's own; what it files, everyone sees.

Measured: a reader robot ran five rounds against a page holding 7 WHILE the
notebook sat in the user's hand — total 35, notebook still held.

### And two listed bugs that measurement closed without code

The "work behind the robot inside a house": the given box measures z +0.58
with the robot at 0 and the camera at +5.45 — the desk is between you and the
robot, and my listing was a leftover from the rotation detour. And the
multiple thought bubbles: zero reproduce since the scheduler was scoped to the
outer world; they were the inner world's condition bubble rebuilt at full size
by the same runaway that made a picked-up house run at Instant.


## The scheduler is contained, and the suite runs anywhere

*Added 31 Aug. The afternoon the suite would not finish, anywhere, for anyone.*

The trail ran: Ken's foreground tab hit "wait or kill" at the copies check; my
hidden pane crawled at two frames a second in the same place; a probe of the
same steps in a fresh world ran clean. The app's own profiler named it:
**1.2 seconds of room work per frame, 3615 registered numbers.** The
Instant-exemption for the sibling rule had resurrected the runaway in the one
place it still could — the inner g-loop ignores the once-per-turn frame gate
(its licence for a house's own nested pipeline), so at Instant the same
neighbouring TICKER ran fifty times per g-loop, per afterQueue, per frame.

The containment took three cuts to get right, each falsified by the goldens:

- **Once per turn** starved pipelines: three goldens settled with a lever
  still up, dumps otherwise byte-identical.
- **Dirt as the discriminator** (rerunnable only if it went quiet) left the
  same flag standing.
- **A cap of three visits** per neighbour per pass holds: every
  request-reply-acknowledge in the goldens fits, and a ticker is bounded.

Two real bugs surfaced under the same light. The `cont` tail asked "is there
still work" GLOBALLY, so two mail-partnered houses held each other dirty for
ever — A dirty because B was, B because A was; it now asks only within the
house's own world, which was its purpose. And a dozing room re-dirtied by a
final delivery clears only after its 30-frame sleep-cache expires — half a
second in the live app, an eternity to a dump taken sooner, so the harness
quiesces 40 frames before dumping.

The suite itself learned to run anywhere: yields via setTimeout when the tab
is VISIBLE (paint and input flow; a MessageChannel ping-pong starved both and
Chrome offered to kill the very tab the yields protect) and via MessageChannel
when HIDDEN (setTimeout is clamped to a second there; melody alone took 317s).
`?block=1` turns yielding off for headless drivers. And the check that watches
paced houses counts REAL seconds, not virtual frames — driven by frame count
its wall-clock was whatever the yields cost, so it passed while breathe() was
slow and failed the moment breathe() got fast.

End state: ok true, 41 checks, 13 goldens byte-identical.


## Panels get their door, and nest whole

*Added 31 Aug. Ken: "I think panels should have a door. Besides being
associated with an object via the bird it should be nestable. When I drop a
panel on a panel it doesn't get smaller and end up part of the panel
underneath." And, on the notebook: "robots can do what the user can do. It is
like a program writing a file so writes should apply" — ratifying the
write-through choice.*

### The door

A panel was always a room; now it has the room's entrance. The same little
door a house wears sits at the tray's front corner, and walking through it is
the same enterRoom: the panel's world at full size, robots running where you
can watch them, the workshop vantage, the tall door back out. Measured:
worlds-deep 1 inside, 0 after leaving, tray back on the bench.

### The nesting

Dropping tray A on tray B used to park A beside B and bind only A's owner
card — round 42's "the old panel is left behind", still standing. Now the
WHOLE panel moves in: card and tray both onto B's inner bench, shrinking with
B's world (measured at scale 0.11), visibly part of the group. The binding is
Ken's round-39 rule unchanged, and lifting it out restores independence.

Finding where to fix it was the work: the park-it-beside rule existed in
THREE copies — combine's panel branch, roomDrop, and a catch-all sitting
ahead of everything in handleClick ("a real drop lands on whatever part of
the tray the pointer hits"). The first fix went into roomDrop and measured a
clean zero, because the catch-all ate the gesture before roomDrop ever saw
it. All three now route to roomDrop; one source of truth.

### The reach, honestly

A pose-table aim (look the target up in the arm's measured geometry, after
the walk) was built, measured worse than the lerp it replaced, and taken back
out. The table and the stand disagreed about where the claw would end up
because each approximated the arm differently. The lerp — desk reach to
measured full stretch — is the "much better" baseline Ken judged, and it
stays until the kinematics are done once, properly, in one place. The one
durable find from the detour: actionTake shadows `window` with a boolean, and
an instrumented write to `window.__aim` crashed the room from inside — worth
remembering before instrumenting anything there again.


## The stop means stop, the post is paced, and a fold keeps its tenants

*Added 1 Sep. Ken: "if he's going to use that arm he should move over so his
hand is near the stack." "The totaller robot ignored the stop button." "I see
numbers being added to the nest stack but don't see any birds doing the
delivery... why should any bird deliveries be queued at all?" "The bird flew
to where the panel used to be - not where the airplane is. The plane was not
updated until I obtained its panel and removed the 3D turtle panel and set it
down."*

### The hand is at the stack

One decision, from which the stand and the arm both follow: the pile-top's
height (stand-invariant) picks the grab pose from the boot sweep's measured
table, and the robot walks to where THAT POSE's claw sits on the pile. The
earlier pose-table attempt failed because it aimed by the table but stood by
the lerp and the two disagreed; deriving the stand from the pose makes
disagreement impossible. Measured: horizontal claw-to-top distance 0.000 at
the grab and 0.000 at the release (the drop used to let go at desk height
beside the stack and float the number over). A pile past full stretch: the
robot stands directly under the top at maximum reach (claw 1.876 against a
top at 2.197) and the grasp settle carries the rest.

### The lever means stop

The totaller is a mail-driven house: dirty only for the instant between a
letter landing and its round answering, dozing the rest of the time. The
lever judged on/off by the dirty flag, so a press meant as STOP nearly always
found dirty=false and took the start branch — measured verbatim: "The lever
goes up — the robot inside gets to work." The stop was not ignored, it was
inverted.

Two wrong fixes first: "engaged = dirty or dozing" read a FRESHLY BUILT house
as on, because hydration runs the robot once offstage and leaves it on vigil
— the startup lever pull then STOPPED activity1's Doubler before its first
letter, and mail could never wake it (walks 40.4/0.0/0.0, measured twice).
"has it ever run" (stepRounds) failed the same way: loading gives every house
one settling turn. The truth is that a doze cannot say which way the switch
should throw, so the switch REMEMBERS being thrown: __switched marks a house
a person (or a drop, or watching it work from inside) set going, and only
that — or visible work — makes the next press a stop.

### The post is paced by its own delivery

Measured on zeno behind glass at speed 1: production outran delivery, and
after the halver was genuinely stopped, five more numbers landed over the
next six seconds — the backlog Ken watched, tucks queued behind the visible
round. In the original, giving a bird a letter and the bird delivering it is
one act. So now a room that has posted a courier is not offered another turn
until the letter is ON the nest: counted per parcel on the sending room
(joining letters included), released as the letter arrives — at landing, not
at the end of the tuck animation, which rides a queue that freezes when its
world steps off the stage — and released too when a flight is cancelled
mid-air, with a 20-second self-heal so a dropped queue can wedge nothing for
good. Instant is untouched: no couriers exist there, so nothing is ever
counted. Watched again from inside the totaller: one bird at a time, arrivals
cease when the halver stops, backlog zero.

### A fold keeps its tenants, and the mail comes down on the thing

The knob's fold judged a panel by ITS OWN work — no robot of its own, not
dirty — and took the serialize path, flattening the whole world into a
record with the switched-on turtle panel nested inside it: the letterbox left
the scene, the still-registered tray ticked on as a zombie, and hand-flown
orders had nowhere to land until re-opening the panel rebuilt the world. A
fold over live nested work now takes the stays-live path — the tray
invisible on the bench, where the scheduler already finds it. Verified: after
nest-and-fold the tray survives as a closed live tray and a [move | 10]
handed to the bench bird moves the plane 1.54 through both layers.

And the landing: flightLanding's plain-room branch caught TRAYS — a tray is
a room — so a bird flying to a letterbox inside a folded panel came down on
the invisible tray's parked spot, Ken's "the bird flew to where the panel
used to be." A room catches the mail only if the watcher can SEE it; hidden
rooms fall through to the owner branch and the bird comes down on the
behaviour's bound thing.

### What the probes taught

The airplane world carries its own example order boxes, and two of them are
PITCHES — turns, which change no position at all. A probe that gathered "the
boxes on the bench" and measured "did the plane move" spent three cycles
chasing a phantom bug: the message reached the plane every time (a new
`__msgN` odometer on deliverToThing said so), and the plane was obeying it —
by pitching. Know what the world you load already contains before measuring
what your own additions do. Houses pace by the wall clock, so a probe that
drives virtual ticks measures nothing about pacing — the suite's
postAcrossCheck learned this long ago; the probe had to relearn it. New D
hooks from the hunt, kept: `D.vigil()` (who dozes in the current world),
`D.ctxInfo(t)` (what a room's stashed world holds), and the `__msgN`
odometer.

And the round's best decoy: eight checks failed with "non-finite clientX",
which reads as a camera poisoned by a NaN position somewhere — a scene-wide
scan found nothing, because there was nothing. The instrumented press printed
the real story: `rect 0 160` — the embedding pane had collapsed mid-run, the
resize handler set `camera.aspect = 0/160`, and the projection matrix went
NaN in X for every later press. The app now ignores zero-size resizes (the
last good aspect holds until a real one arrives), so a folded-away tab can no
longer poison anything.

End state: suite ok, 44 checks, 13 goldens byte-identical.


## Marty makes things, and only things

*Added 1 Sep. Ken: "Could we make it so that Marty can be asked to produce new
resources that appear in the world? Could the API be used to request a new 3D
model (like the airplane and dragonfly) and then import it? Perhaps the Marty
dialog panel would need an additional button." And, for later: "I think we
should use turtle graphics for the procedural images. An interpreter isn't
difficult."*

It is not a text-to-3D problem, which is the whole reason it is cheap. The
airplane and the dragonfly are not imported meshes: a `model` thing IS its
parts list -- eight entries of `{shape, size, at, rot, color}` over four
solids, built by `makeModel` -- so asking for one is asking a language model
for a small piece of JSON, the thing it is best at. Only the robot and Dusty
are GLB. What arrives is first-class: pick it up, copy it, bind a behaviour,
save it. Nothing but text crosses the wire, so it works in every build, the
artifact included -- unlike generated PICTURES, which need an image endpoint
Anthropic does not have and a host the artifact frame refuses.

**The line he must not cross.** His standing orders forbid designing programs
for the visitor, because building it yourself is the point. A prop is the
opposite of that: a sailboat that does nothing is scenery ASKING to be
programmed. He makes nouns and never verbs, and the maker prompt says so as
plainly as the conversational one forbids the rest. The manual says it to the
child in the same breath as the button.

**Nothing an answer says is trusted.** Shapes must be one of the four; every
number is finite-checked and clamped; colours go to the browser's own parser
(so `chartreuse` works and `javascript:` does not); the part count is capped
at 40; and the whole is scaled to something a hand can pick up. That last one
goes BOTH ways, which the first screenshot taught: absolute scale is what a
model is least sure of, and a toy answered in centimetres is a speck too small
to point at, exactly as unusable as one the size of the table. A model that
survives the guards cannot be malformed, however odd it looks -- a strange toy
is funny, a NaN in a position is a poisoned scene.

**Testing something that lives behind an API.** The check hands the builder the
raw text a brain would have returned -- a good answer wrapped in the chatter
models like to add, a hostile one (200 parts, a shape called banana, NaN
positions, a colour that is a script, a boat the size of a house), a speck, and
an answer that is not JSON at all. The network is not part of the test because
the risk is not in the network; it is all on this side of the wire. Forty
seconds, and it caught the missing size floor.

`askBrain(sys, q, history, cap)` was lifted whole out of martyThink so the
maker can reach any of the five brains without inheriting the conversation --
threading the chat through it made models answer in prose ABOUT the thing
instead of building it.

**Then Ken used it, and found the hole.** "After it created something I
prompted 'good but it should have 6 legs' and it didn't take into account the
previous 'Make me:' prompts." That was my mistake and a deliberate one: I gave
the maker NO history on purpose, because threading the CHAT through it made
models answer in prose about a thing instead of building it -- and threw out
iteration along with the prose. Making is iterative by nature: you ask, you
look at what arrived, and you say what is wrong with it. So the maker now has
its OWN memory, one exchange deep, holding the PARTS rather than the chatter,
with a prompt line telling it to return the whole revised thing (and to ignore
what came before when a new thing is named).

A revision also REPLACES what it revises: a six-legged insect beside the
five-legged one is a graveyard, not an answer. Only while the thing is still
HIS, though -- standing free on the table, untouched. Once it has been picked
up, filed in a box or given to a bird it belongs to the visitor, and the new
one simply arrives beside it.

The testing lesson is sharper than the fix. The check covered the builder
because that was where I thought the risk was; the memory was the one thing
the seam did not reach, and it was the one thing that was wrong. `martyMake`
now splits at `applyMakerReply(wish, reply)` -- everything that happens to an
answer once one arrives -- so the check drives the whole of it, memory
included. A seam drawn where the risk is *imagined* to be tests what you
already believe.

Next in this direction, Ken's call: procedural images via a TURTLE GRAPHICS
interpreter. The virtue is that it reuses the vocabulary children already
learn from the turtle behaviour -- forward, pitch, yaw, roll, pen -- so the
drawing language is a second use of known words rather than a new notation.


## A full round, a square-on robot, and a nest that stays cheap

*Added 1 Sep. Ken: "Once again I saw a robot facing away when entering a
house." "The attached world responds very slowly despite no robots running."
Then, having reloaded it: "The world isn't slow when I refreshed and loaded
it. But it was very sluggish when I saved it. I think the scheduler should let
each robot do a full round every cycle regardless of how many steps it takes."*

### The robot really was facing away

The old note here insisted the world is not turned round, and it was right --
but it stopped one step short. The GLASS-HOUSE PERFORMANCE walks the mini
robot to each hole its round touched and turns it to face each one, and when
the round is done it walks home facing the direction of travel and stops
there. So a round that ended with a return from the left left it looking off
to the right for good. Measured on zeno's totaller: entering at ten different
moments, five showed its back, settled at -138 degrees and staying.

It squares up to the desk now when it arrives home, the way it stands when you
train it -- and if you walk in while it is still mid-performance, facing a
hole, it turns round to greet you.

The instructive part was the first attempt, which measured *zero* change. A
bot has both a `node` and a `root`, and `bindBody` sets the global `root` to
`bot.root`, the rig INSIDE the node -- but the performance turns the NODE.
The first fix animated `root`, whose yaw is 0 and stays 0, so it asked for a
turn of nothing and got it. Two objects with reasonable names, and the one the
eye sees was the other one.

### A nest that has taken a thousand letters

Ken's save holds 3,840 numbers on one nest, denominators up to 1,309 digits.
Two costs grew with it, and neither looks like anything but "sluggish":

`restackNest` hid EVERY member of the pile on every delivery, so a nest that
has taken n letters has cost n-squared visits by the time it holds them. Only
the ten that were standing up can need putting down, and that is what it does
now: measured on a 1,200 pile, a restack touches 10.

And the half-second detail sweep asked all 3,840 where they were in the WORLD,
which walks each one's parents and multiplies matrices -- 77ms in a single
frame, twice a second, with nothing running at all. A thing nobody can see has
no level of detail; the sweep still visits every number to prune the register
(that is what keeps it bounded) but only measures the ones on screen.

Both are tested as WORK rather than wall-clock: how many pile members a
restack touches, and how long a frame that is forced to run the sweep takes.
The first version of that check passed for the wrong reason -- it scrolled the
pile in the direction whose plate does not exist at the top of a pile, so
nothing was restacked and "touched <= 24" was true of nothing. It asserts
`touched > 0` now.

### A round is the quantum

Ken's rule: "the scheduler should let each robot do a full round every cycle
regardless of how many steps it takes." The budgets that stop BETWEEN rooms
were already right -- the panel loop's 8ms and ROOM_WORK_SLICE both decide how
many robots get a turn, never whether a round finishes. But `drainQueue`'s
count is a cap on WAVES of work (a step that enqueues more steps starts
another), so a long round could return half-run, with a thing in the claw and
a hole empty, until whenever its next turn came. The round's own two drains
pass Infinity now: only the wall-clock watchdog can end a round early, and
that is a runaway rather than a scheduling decision.


## A long answer is not a bad answer

*Added 1 Sep. Ken: "I see 'That came back as something I could not build...'
after asking for 'a 6-legged preying mantis'. I tried twice with Sonnet and
once with Opus. It worked with several GPT models. Gemini replied 'I could not
make it -- Gemini said 503.' Maybe API errors should be logged to the
console."*

The provider split was the whole clue, and it pointed at our code rather than
at any model. The OpenAI and Gemini branches of askBrain send no token cap at
all; Claude's sends max_tokens, and the maker asked for 1600. A mantis is a
body, a head, feelers and six legs -- twenty-odd parts, each a line of numbers
-- so Claude's answer was cut off mid-array and arrived as JSON that does not
parse. Nothing was wrong with the model or the wish. Worse, the message
blamed the child ("ask me again, or in fewer words") for a limit we had set.

Three fixes, and the third is Ken's:

**Room to answer**: 4000 tokens.

**A parser that reads what arrived.** It took the first brace to the LAST one,
so an answer with a sentence after the JSON, or two objects, was unreadable
for a second reason. It takes the first BALANCED object now -- and when the
braces never close, it salvages the parts that did arrive whole, builds the
toy from those, and says plainly that it came up short instead of pretending
it is finished. The salvage's own first version found nothing: it stopped at
the first unbalanced object, which in a cut-off answer is the OUTER one, so it
walked away from every whole part inside it -- the whole of what there was to
save.

**The console**, because "it didn't work" is not a bug report: every refusal
from a brain is logged with the provider, the model and the error, and every
answer that could not be built is logged with the raw text. A 503 is now also
told apart in what Marty says -- the mothership being busy is not the child's
fault and is worth trying again.

The check feeds the builder the two shapes Ken actually hit: a mantis cut off
mid-array (six whole parts and a seventh half-written) and an answer with
chatter after the JSON.


## Marty draws, with a turtle

*Added 1 Sep. Ken: "can you add a 'draw' button like the 'make' button that
generates images as you suggested earlier" -- and, from the round before, the
choice that made it worth doing: "I think we should use turtle graphics for
the procedural images. An interpreter isn't difficult."*

Turtle graphics rather than a drawing notation of my own, and Ken's reason is
the good one: children already learn forward, right, left and the pen from the
turtle behaviour, so the language a picture is written in is a SECOND USE of
words they know rather than a new thing to learn. It also leaves the picture
legible. A snowflake is six of something repeated and you can see that it is,
where an image from a picture-model is a wall you cannot get behind.

It is also the only kind of picture that works everywhere. Real image
generation needs an endpoint Anthropic does not have and a host the artifact
frame refuses; a turtle program is text, and text crosses every wire.

The interpreter records strokes rather than drawing as it goes, so the whole
picture can be measured and FITTED to the paper afterwards -- a turtle has no
idea how big the page is, and asking a language model to guess gets you a dot
in the corner or something ten times too big. The guards are the maker's: a
step count no honest drawing approaches (a `repeat 999999 [ repeat 999999
[...] ]` stops at 13,329 strokes), bounded nesting, colours put to the
browser's own parser, every number finite. Words the turtle does not know are
stepped over, so a flourish or a stray comment cannot stop the drawing --
measured: "draw a lovely house please fd 10 thank you rt 90 fd 10" draws the
two lines and ignores the rest.

And a turtle program degrades gracefully, which turns the truncation problem
from the last round into almost nothing: an answer cut off mid-order simply
draws less. The orders are pulled out of the half-written JSON by hand, run,
and Marty says the turtle ran out of breath rather than pretending it is
finished.

The check drives the interpreter and the whole path without a network: the
snowflake from the prompt (48 strokes), a pen lift that leaves a gap, prose
that draws nothing, a script for a colour, a runaway, a re-drawing that takes
the old one's place, the memory that makes "in red" a re-drawing at all, and a
truncated answer that still becomes a picture.


## Dusty, redrawn: an opening has to be cut

*Added 1 Sep. Ken: "I'm not very happy with how Dusty looks. It doesn't have
the charm of marty, ruby, and robots. Try a more appealing design." Then, of
the first attempts: "do it properly", and after one more pass on the mitts,
bag and glow: "I'm happy, go ahead."*

Eight versions, and the useful part is why the first four failed. Every one of
them faked its face by laying dark shapes ON the shell -- a visor slab, a
torus meant as a groove, an ellipsoid for a mouth -- and every one read as an
appliance with features glued to it. **A torus sits proud of a surface, so it
cannot be a groove; an ellipsoid laid over a sphere cannot be a hole.** The
eye knows the difference because a real opening has a rim, a wall and a
shadow, and none of those can be added by putting something on top.

  v2  a fire hydrant in a diving helmet: the "groove" became a helmet ring,
      the eyes stood off on stalks, and the snout crossed his cheek like a
      gas mask because it was placed at head height instead of below it.
  v3  the dark face panel read as a smudged bandit's mask; a stack of cones
      and cylinders read as a chess pawn.
  v4  one round body and a face with life in it at last -- and NO MOUTH: the
      intake ellipsoid was centred at y -0.132 with a y-radius of 0.079, and
      the body's front at that height is -0.195. It never reached the
      surface. He came out a red ball with lovely eyes.
  v5  a mouth placed by arithmetic instead of by eye, and it read as a boot.

Then the boolean, which is the whole fix: cut the mouth and the eye sockets
OUT of the body. v6 proved it and showed the next mistake immediately -- the
dark throat was placed where it poked back out of the hole it had just cut,
which is a tongue -- and the flattened pupils sat at the eyeball's own depth,
half buried, so he stared at the floor. v7 put the throat deep, gave him round
pupils standing proud (the gaze meets yours), and dropped the cream chin.

Ken's last pass named the three things left. Of those, one was a real
discovery: **the bag was invisible because it was coral on a coral body** --
the body's own colour on the body's own curve has no silhouette from three
quarters behind. Cream fixed it. The other two overshot on the first try
(v8): a 3.4-strength glow became a headlight filling the mouth, and mitts
swung round to the front fouled the mouth, which is the thing the whole face
is built around. v9 has the glow at 1.5 as a pool inside the lip and the
mitts back at his sides with a dark cuff, which is what turns a ball into a
mitten.

Swapping him in needed nothing else: the app never used his `intake` anchor,
it hangs the bag of vacuumed things at a fixed (0, 0.49, 0), and v9's top is
0.474 against v1's 0.474. Measured after the swap: his gaze lines up with the
bench to a dot product of 0.99, so the -1.5 rotation still means "facing the
desk".

One cost, and it was not cosmetic: the boolean triangulates what it cuts, so
the 40x20 spheres that were fine as primitives became a 693 KB glb once the
mouth and sockets were carved out of them -- and 903 KB of base64, over the
700 KB a single script block in the artifact build may hold. The build refused
outright, which is the right way to find out. Re-exported at 24x12 spheres and
22x10 tori -- tessellation, not shape -- he is 273 KB, SMALLER than the Dusty
he replaces, and the only visible difference is a touch of faceting on the
glow pool that half a metre of distance hides. Worth remembering before
cutting anything else: a boolean's cost lands in the export, not in the
viewport.

## What a room looks at

*Added 1 Sep. Ken: "There should be a way to return the info notebook -- maybe
the (i) changes to indicate return the notebook. Dusty is good but should be
facing the camera when nothing is held, otherwise the “hand”. Ruby and Marty
too. ... Can the JSON be formatted to make it easier to read and edit?" Then:
"Marty should look at its dialog panel when the user is typing or the cursor is
over it. ... gemini-3.7-flash is still reporting 503. ... I think Marty's eyes
can be better -- instead of white eye balls let's go with blue."

Six small things, and one of them took four measurements to get right.

**The plaque takes the notebook back.** A button that only ever gives is a
button you press once; the info plaque now shows a return arrow while its
notebook is out, and pressing it again takes the notebook off the bench,
whichever spot it wandered to. It is the same plaque, the same click, one
texture swapped -- which is the whole of the affordance: what a control will
do next is written on its face.

**They watch you, or your hand.** Dusty, Ruby and Marty stood at fixed yaws
chosen when they were placed. They now turn to the camera when your hand is
empty and to whatever you have picked up when it is not, eased at three
radians a second so it reads as attention rather than a snap. It costs one
`atan2` each per frame.

**Saved things are documents.** `prettyJSON` indents structure but keeps a
numeric array on one line and collapses any object under 130 characters, so a
part is one line -- `{ "shape": "box", "size": [0.16, 0.03, 0.34], ... }` --
and a model with twenty parts is twenty lines you can edit by eye. Ken's route
is save, edit in a text editor, import, and that route only works if the file
is legible when it is opened.

**Marty watches his own panel, and this is the one that was wrong twice.** The
first version unprojected the panel's middle at NDC z 0.5 and told him to look
there. Measured: he did not move at all. NDC depth is weighted hard toward the
near plane, so 0.5 lands about 13 cm in front of the camera -- from where
Marty stands that is your face to within a fraction of a degree. Pushing the
point 2.2 m out along the same ray was the second version and measured 1.3
degrees, in the wrong direction, at a full-size window.

The mistake underneath both was treating the panel as a thing in the room. **A
panel is a sheet of glass over your view, so every honest unprojection of it
lies on the line from the camera into the desk, and from anywhere else in the
room that line is one direction.** No arithmetic on it can produce a turn.
What you actually see when someone looks at a panel on the left of your screen
is that they look to YOUR left -- so the target is now a place beside the
camera, one and a bit metres out along the camera's own right-hand axis,
scaled by where the panel sits across the screen. Measured at 1400x782 with
the panel's middle at NDC x -0.75: nine and a half degrees toward it on hover,
the same on focus, and back to his idle 33.6 the moment you leave. The check
does not assert a number of degrees -- that would only be measuring the width
of the test frame -- it asks whether he is aiming at the place the code says,
and prints how far apart the two places were.

**Blue eyes**, 0x9fe4ff with the roughness dropped to 0.25 so they catch the
light. White eyeballs on a green face read as a cartoon of surprise.

**And Gemini 3.7's 503.** Ken has it on Google's own word that the new
thinking parameters are strict, and 3.6 works where 3.7 does not. We send no
thinking parameter at all, so there is nothing of ours to correct; what is
there now is one retry after 900 ms and a message that names the mothership
rather than the child. If it persists it is worth sending `thinkingLevel`
explicitly -- but not on a guess about a request shape nobody here can test.

## The number the robot was carrying

*Added 1 Sep. Ken: "Dusty's eyes are still white. The totaller robot's arm
motions after entering the house are better but the number it grabs and drops
isn't visible. But it is dropped and the addition happens. Enter should display
a number (or other objects besides pads) as the camera zoomed in on it. And the
arrow keys for rotation should still work. No need for wiggle feedback after
pressing enter for a closeup view of anything."*

**The invisible number was mine, from the round before.** Last round's speed fix
had the nest remember the ten members it last showed, so a restack costs ten
visits rather than one per letter ever delivered. But the top of the pile is
exactly what a robot takes, and `detach` splices the thing out of the pile and
restacks **while the thing is still hanging on the nest** -- so the memory hid
the number at the very moment the claw was closing on it, and nothing showed it
again until it landed somewhere else. A robot mimed an addition with nothing in
its hand for the whole walk across the desk.

Two false starts are worth recording, because both were the same error.

  1. The first fix guarded on parentage -- do not hide what has been reparented
     -- which sounds right and is useless here: at that instant the thing is
     still the nest's child. Kept anyway, with a truthful comment, because it
     catches the OTHER way a shown member leaves: two nests merging.
  2. The first *reproduction* was a false positive. A probe counted every
     invisible number that was not on a nest and found 1603 frames of them --
     but Ken had two houses, and the halver's whole world is legitimately
     hidden while you stand inside the totaller, claw and all. **A measurement
     that cannot tell your bug from the world working correctly is not a
     measurement.** The honest instrument was one line of debug -- what does
     the claw hold, and can it be seen -- and with it the bug reproduced in a
     world with no houses at all: 513 carried frames, 513 of them blind.

The cure is in `detach`: forget the thing where it stops being the nest's.
Measured after: 513 carried frames, 513 visible, and the sum still 33/1.

**A closeup of anything.** Enter answered for pads alone, and a pad is read from
straight above -- which for a number is a square with a lid on it, and no
vantage from which turning it means anything. Anything that is not a pad is now
flown to from the FRONT: the bearing you were already watching it from, lifted
17 degrees above its equator, as close as its own bounding sphere fits. Measured
on a number: 0.75 m away at 17 degrees, upright, and Escape lands back within a
hundredth of where you left. A pad is untouched -- still 90 degrees, still with
the flat up-vector.

The arrows turn what you are looking at, quarter by quarter, reusing the roll
that keeps a number's writing the right way up. That is the point of the whole
feature: a number says the same value six ways and five of them were unreadable
without picking it up.

**And no shaking in there.** The hover wiggle already refused to start in a
closeup -- but only `wiggleTargetOf` knew that, and it is consulted when the
pointer MOVES. After Enter the pointer does not have to move again, so whatever
was already shaking went on shaking, in the middle of the screen, at the thing
you had just asked to look at. Cleared on the way in, and refused every frame.

**Dusty's eyes** were cream balls with a cyan pupil at emit_str 2.0, and at that
strength the pupil blows out white too, so the whole eye read as a ping-pong
ball -- which is why "blue eyes" done to Marty last round left Dusty looking
exactly as before. v10: the ball is #9fe4ff and the pupil a navy that still
reads against it. 280 KB, four hundred bytes more than v9.

## The else that assumed a box

*Added 1 Sep. Ken: "The app froze when I placed a generated model on the
copier." Then: "I think the operator should not obscure the display of numbers
-- move it to the upper corner", and "Somehow [Dusty's] eyes are a bit creepy.
Maybe his eyes should be more like marty and ruby just a different color than
black."*

The copier knows how to copy each kind of thing, written out by hand: a robot,
a number, a die, a sound, a pad, a notebook, a room, a bird, a nest -- and then
an `else` that made a BOX. Not "if it is a box": an else. So every kind nobody
thought about arrived there and was copied by reading holes it does not have.
A model has parts and no holes, so the read threw.

**Where it threw is why it froze rather than complained.** The copy is made
inside the step that lowers it into the tray, and an exception in a queued
step leaves that step half-run: it never finishes, so the queue never advances,
and every click afterwards waits on a scan that will never end. The workshop
does not crash, it stops -- which is exactly what a person calls a freeze.

Three things came out of it, in order of how much they matter:

  1. The catch-all is now named (`box` or `scale`), and anything with no branch
     of its own is copied **from its own written record** -- whatever a thing
     can save, it can now be copied. That closed `trail` too, which had the
     same hole and which nobody had hit yet.
  2. The raw record, not the full one. `thingOut` carries the live name, and
     `buildThing` hands back the registered thing itself when it sees one -- so
     copying by the full record would have returned the ORIGINAL and called it
     a copy. Identity, panel and size are handled a level up.
  3. Mimi says so instead of throwing. Whatever else is ever wrong, the one
     thing she must not do is die inside her own scan.

And a fourth, found by the check rather than by Ken: `makeModel` did
`parts.slice()`, which copies the LIST and shares every part in it -- so a
model and its copy off the tray held the same parts, and editing one would have
edited the other. A copy is wholly its own or it is not a copy.

**The operator badge** was painted after the face, so wherever it sat it won,
and it sat at (54,54) with a radius of 30 -- reaching down to row 84 on a
256-square face. Every face centres its block on row 140 with up to 168 of
height, so a long number starts writing at row 56: the plus sign lay across the
first line of Ken's monster fraction. At radius 20 centred on 36 the badge ends
at 56. Measured on the six painted faces: writing starts at 85 at the earliest,
so it is clear by nearly thirty rows, and the check reads the painted canvases
rather than comparing the code with itself.

**Dusty's eyes.** Marty and Ruby share one eye -- a plain ball with a small
pupil standing just proud of it, the pupil a bit under half the ball's radius,
and no highlight at all. Dusty's had a pupil at 53% of the ball, lit, with a
hard white spark on top of that: the recipe for a googly eye. v11 takes Marty's
proportion, drops the spark, and makes the pupil indigo rather than the black
those two wear -- his one point of difference, which is what Ken asked for. He
is 251 KB, smaller again.

## The same else, three doors along

*Added 1 Sep. Ken: "I think even very large integers should be displayed in
English on one face of the cube. The app froze when I tried to train a robot
with a model. It couldn't pick it up and then it froze."*

The copier's `else` that assumed a box had two siblings, and the lesson is
about the shape of the mistake rather than any one of them. **A chain of
`else if (kind === ...)` ending in a bare `else` is a promise that no new kind
will ever be added** -- and models and drawings were added months after these
chains were written. Neither author did anything wrong; the `else` did.

  buildCondNode   the picture in the robot's thought bubble
  condText        the same thought, in words
  thingIn         the world reader (this one had a model branch already, and
                  its else is now guarded anyway: a record with no holes is
                  not a box with none)

The freeze came from the first two, and where they threw is why it read as a
freeze rather than an error: **the click that hands the robot its lesson builds
the bubble and the words in the same breath**, so the throw left the workshop
mid-gesture, with a lesson begun and no thought to show for it. Nothing
answered afterwards.

And underneath, quieter and worse: `matchState` had no rule for a model, and
its tail is `return 'no'` -- so a robot taught with Ken's boat **would not have
recognised that very boat**. The lesson would have been a waste even once it
stopped crashing. Same-kind-and-written-the-same-way is now the rule for the
kinds that have no parts to match on, and the check asks the question directly:
`recognises-it=yes`.

**Very large integers.** The scale names stopped at decillion, and past ten to
the thirty-sixth `englishText` gave up and handed back scientific notation --
which is exactly the thing a child cannot read aloud. The names now run to
vigintillion (ten to the sixty-third), and past even those a number is read as
"about five point seven times ten to the power of sixty-nine": still English,
still true, and short.

The subtler half was the FACE rather than the words. A sixty-digit number's
real name runs to eight hundred characters; on a face this size that becomes a
grey wall ending in an ellipsis, which is not the number displayed in English
but the number hidden in it. The face now takes a second, shorter wording and
uses it **only when the full name will not fit at any size** -- so Ken's
thirty-six digit number goes on saying itself in full, in small type, and a
sixty-digit one says itself briefly. Measured on the faces: 12, 36 and 40
digits in full, 70 and 200 in the short reading, and nothing cut off anywhere.

## What you did to it belongs to it

*Added 1 Sep. Ken: "why does this face have '...'? I think when the English
doesn't fit on a face let's have shrinking letters like shrinking digits so the
first and last parts are shown. I think if a number cube has been rotated by
the user that it should stay that way when released (or return for closeup
viewing) rather than restoring the default orientation. You can use the way
scale names are generated from Latin to handle much bigger numbers.
control-c while holding a number cube should put the top face text on the
clipboard."*

**The ellipsis.** A wrapped face that would not fit kept the first lines and
put an ellipsis on the end -- so a number nine hundred digits long showed its
beginning and threw its end away, and the end of a number is as much of it as
the beginning. It now works the way the digits face has always worked: head,
a gap, tail, with the lines either side of the gap set smaller so the break
reads as a break rather than as a sentence that stops making sense. Measured
on a 900-digit number: the gap is in the middle, the head is there, the tail
is there, and nothing trails off.

**The scale names are built now, not listed.** A table stops wherever whoever
wrote it got bored; ours stopped at decillion, and last round I extended it by
hand to vigintillion, which is the same mistake with a longer table. English
does not stop there -- past a nonillion the names are made from Latin numerals
to Conway and Wechsler's rule, and a rule can be written down once and answer
for every number. The subtlety is all in the joins: "tre" grows an *s*, "se"
an *s* or an *x*, "septe" and "nove" an *m* or an *n*, depending on what
follows, so that the word can be said aloud. Spot-checked against the
dictionaries: ten to the 63rd is one vigintillion, the 93rd one trigintillion,
the 303rd one centillion. It runs out at ten to the three thousandth, where the
short reading takes over.

**A turn is part of what a thing is.** Putting something down levelled it, so
a cube turned to the face you wanted went back to its digits the moment it
touched the table. There was already a field that means exactly "this is how
this thing points" -- `aim`, which putOnBench restores and the saved world
carries -- and turning now writes it. Measured: the quaternion after the drop
is the quaternion before it, and a fresh closeup finds the cube as it was left.

**And Ctrl+C.** A face is a canvas, and a canvas is not text: there was
nothing to copy. Each face now records its own wording as it is painted, and
Ctrl+C copies the face turned toward you -- the digits, the grouped form, the
English, the scientific -- rather than one fixed choice. Measured: untouched it
copies 1234567, and one turn later it copies 1,234,567.

## A herd of unicorns, and being told what shape to answer in

*Added 1 Sep. Ken: "Chrome's Gemini Nano isn't very capable but can it make any
models? Here's the console: [marty] could not build from this reply:
{"say":"Here you go! A little blue box to get you started.","demo":"boxes"} ...
The tooltip for dropping on a robot should be different for untrained and
trained robots ... I trained a robot to copy the unicorn model and it did fine
creating many extra platforms. But when I stopped the training all the objects
on the extra platforms ended up on the desk ... When holding a model the up and
down arrow should work as well."*

**Nano could always make models.** It was being told to answer in the wrong
shape. The brain built into Chrome is small, and the one thing that makes it
usable here is constrained decoding: it is *told* what shape its answer must
take. `nanoThink` passed the CHAT schema no matter what it was asked -- so
pressing Make produced a perfectly well-formed conversational reply, which the
maker then failed to build, and the console blamed the child for it. There are
three kinds of errand now and three schemas, and the errand chooses. Measured
with a stand-in for Chrome's model: told `name,parts` it makes a model, told
`name,orders` it draws.

**The unicorns were not a leak.** Four ways of making copies inside a lesson --
onto fresh work spots, onto the table, left on Mimi, left in the claw -- all
rewind to exactly the world you came in with; that is now a check. What Ken
watched was a RUN, whose work is real and is meant to stay: the run's results
go on the table when the robot stops, which is ToonTalk's own rule and one this
code has always followed deliberately.

The real fault was that **nothing said which of the two had just happened**. A
lesson ending and a run ending look identical at the moment the robot stops
moving. Both now say so in words: leaving a lesson says the table is as you
left it and the robot keeps only what it learned; a run that sweeps its work
spots says how many things it put on the table and that they are yours to keep.
A rule nobody can see is a rule nobody can rely on.

**And two small ones.** The tooltip for dropping something on a robot said
"training if it is untrained", making the reader do the case analysis every
time; it now says what will actually happen to the robot in front of them, with
the step count for one that already knows something. Tipping was refused for
everything but a number, on the grounds that only a number has six faces worth
reading -- but a made thing has a top and an underside, and being able to lay a
unicorn on its back is the difference between a toy and a picture of one.

## A puzzle is a world file

*Added 2 Sep. Ken, over three messages: puzzles should not be a new
capability but "creatable within ToonTalk 3D" -- a constrained world, a goal
the player can see, a way to submit, an action on success that "a puzzle
author should be able to train a robot to do", and a way to start over. Marty
gives hints. Each puzzle its own world file, "and a robot can load a named
world file", with a setting for whether loading wipes the table first.*

The original was read first: `puzzle.cpp` and the 74 `.pzl` files of the
tutorial (fix the ship's computer, then its clock). A `.pzl` is Marty's intro,
a saved room, a goal object with a one-line description, four permission
switches -- typing to numbers, typing to pads, flipping, function keys -- and
hints in escalating order, the last always the whole walkthrough, given one
per visit to Marty and repeated once exhausted. About a third of the goals are
BEHAVIOURS ("the sum of all the numbers", "a number that keeps getting
bigger"), judged by special cases with timed waits. That settled one thing at
once: a scale cannot be *the* mechanism, only the commonest program for the
judge to run.

Everything else composed out of what the workshop already had:

  the goal          a thing on the table with `fixed` on it -- shown, never
                    taken, dropped into, vacuumed or erased. The word is chosen
                    against `ghost`, which is scenery nothing runs into: this
                    is furniture nobody lifts.
  the submission    a bird on the table whose nest is inside the judge's
                    house. No new gadget: giving a bird your answer is the
                    thing every child here already knows how to do.
  the judge         a robot team in an opaque house, dozing on the post nest
                    the way Zeno's totaller dozes. The leader's thought IS the
                    goal; the team behind it recognises any box, any number,
                    any pad, and sends it back. A wrong answer therefore comes
                    home on the reply nest labelled "from the judge", which is
                    the whole of the feedback and needs no words.
  the rules         a `rules` field on the world: which stacks and tools exist,
                    whether the keyboard reaches numbers and pads, whether Undo
                    is there, how many steps a robot may be taught. Per puzzle,
                    as the original's switches were.
  the next puzzle   the one robot step that did not exist -- `load`, by name.
                    A `library` field bundles other worlds inside a file, since
                    a published artifact can fetch nothing, and every world
                    opened is remembered by name; the examples folder is asked
                    only when there is a server to ask.
  start over        a button on the card, present whenever the world came from
                    a named file; Marty answers "start over" the same way.
  hints             the author's, in order, from `hints`; Marty gives the next
                    one to anything that sounds like asking, brain or no brain,
                    and once they run out says so and gives the last again.

Two things went wrong, both instructive.

**A house's own world is hydrated through the same `worldIn`.** The first
build read the name, the rules and the hints from whatever record came
through that door -- and the judge's inner world, which has none, came through
it a moment after the puzzle's, and wiped them. Measured: rules null, every
stack back on the table, one line after they had been set. Only the outer
world names the place now; `offstage()` is the test, the same one `clearWorld`
already uses to keep a house from sweeping the user's bench.

**A robot asks for the next world from inside the world about to be
replaced.** So the request is noted and honoured at the top of a frame, where
nothing is standing anywhere -- and that is where the suite caught the second
mistake: it passed live and failed headless, because live the real frame loop
ran alongside the check and opened the pending world, while the check's own
frame driver did not. The driver now does what the loop does. A test driver
that is not faithful to the loop tests a different program.

Puzzle 1 runs end to end and is a check: a constrained table, a goal that
stays put, hints in order, a wrong answer sent back, the right one judged and
puzzle 2 arriving, Start over restoring the puzzle. Not yet built, and known:
the note the judge sends flies out a moment before the world changes, so the
player barely reads it -- the load should wait for the letter to land; the
per-puzzle `rules` do not yet cover flipping; behavioural goals need the
judge's program to copy and compare across rounds; and the whole authoring
side, which Ken has agreed to take after the first puzzle is right.

## The judge offers; the player presses

*Added 2 Sep. Ken: "I didn't see a message after solving puzzle 1 (I guess it
was reset too quickly) but puzzle 2 was fine. The layout could be better: the
bird could be central and the objects to be used closer to the camera side of
the desk. ... Instead you can add a button for going to the next puzzle and
one for starting over. After doing all this create several more puzzles."*

**The note was in the air when the table changed under it.** The judge's last
two steps were "give the bird the note" and "open p2", and a bird takes a
second to cross the desk. In a puzzle the `load` step now *offers* the next
world -- it arms a Next button on the card and says so -- and the player
presses it when they have read the note. Outside a puzzle the step still opens
the world at once. Measured: after the right answer the note is on the reply
nest, the table is still puzzle 1, the button is up; Next brings puzzle 2 and
the button goes down.

**The layout is one rule for every table:** what you work with across the
front, nearest you; the bird in the middle with the reply nest beside her; the
goal and the judge at the back, seen and out of the way. `make_puzzles.py`
lays every puzzle out with the same `table()`.

**Three more puzzles**, after the originals where the workshop's tools allow:

  p3  a box with 8, 16 and 32 -- boxes join by dropping one on the SIDE of
      another (left of centre joins on the left), and a 16 dropped on a boxed
      16 makes 32 where it sits
  p4  a zero -- the keyboard is off, so a 3 wearing a minus badge takes away
      when dropped on a plain 3; the original had Dusty find a zero in a
      messy room, which needs his reverse and erase modes we do not have
  p5  a box with two zeros, made by a ROBOT you train, with Mimi on and a cap
      of six steps: give it the box, set the box on Mimi, take the original
      back, set it on a work spot, take the copy, drop the copy on the box's
      side; leave the bubble, press Run, give the bird what it made

Each is its own file, and every later one rides in the earlier ones'
libraries, so the set travels as p1 alone. A check loads all five and asks each
judge, from outside its house, whether it would accept the very goal on its
table: `p1=yes p2=yes p3=yes p4=yes p5=yes`.

**Not built, on purpose:** the original's fourth puzzle, "a number bigger than
1,000", which is the first to need a judge that WEIGHS rather than matches -- a
scale inside the house, the answer set on one pan against a 1000, and a second
round reading the tilt. That is the enhanced-scales round Ken and I discussed,
and it deserves its own measurements rather than an afternoon's guess. Also
deferred, at Ken's word: a clock the robot can read (so the judge could pause
before the next puzzle), which he wants as a bird that carries messages to the
system's own senses, later; and puzzle files dropped on a published artifact
and cached in the browser -- the tt-wasm route -- a zip most likely.

## A hole in a box on a nest is still a hole

*Added 2 Sep. Ken, testing puzzle 1: a wrong answer should come back with a
message; Marty should say that the ORDER of a box's contents matters; an undo
"restored a copy of the original contents on the nest"; a 1 dropped on the box
on the nest "was added to the 3 far away"; a Read button for a held pad;
Marty's "front or behind" should be left or right; the box-over-box tooltip
should be about joining; a step cap only where a bad algorithm would solve the
puzzle, and said up front; and inside the judge's house the robot complained
of a mismatch every round instead of dozing.*

**Two of those were one bug, and it was old.** `holeOwnerOf` -- the walk that
finds which hole a thing sits in so `detach` can strike it off -- searched the
stations and the bench. A box delivered by a bird sits on a NEST, and nests
were not in the list. So a number lifted out of a box on the reply nest was
never removed from its hole: the box went on saying it held the number now in
your hand, a number dropped on another across the table changed the box's
reading too (Ken's "3 far away"), and undo rebuilt the pile from a record that
still listed both numbers, and the table filled with copies. The fix is one
line -- the piles are roots -- and the check now takes a number off a box on a
nest and asks whether the nest still thinks it has it.

**The judge complained every round because of a wildcard.** The conditions on
the judge's other holes were `wild`, and `wild` means SOMETHING must be there;
once the note pad had been sent, its hole was empty, so the leader's thought
answered "no" instead of "wait" -- and "no" beats "wait", so the robot nagged
instead of dozing. A `null` in a thought is a hole the robot never looked in:
anything or nothing. That is what those holes are now, and inside the house
after a solved puzzle the judge is `waiting: true` with no complaint said.
The run-start refusal is also said in full only once; the second time it is
"Still no match."

**A wrong answer comes back with a note, and the note is never used up.**
Mimi is the workshop's, not the table's -- `loadCtx` clears her platform but
she stands in every world -- so a robot in a house can `copy`. The
wrong-answer robots copy the judge's "not quite" pad, give the copy to the
bird, and then give the answer itself: two deliveries, the note first.

The rest is what it says: the box-over-box tooltip names the side and the
size of the joined box; the manual's "in front / behind" for joining is now
"left / right" (that sentence is what Marty was quoting); Marty's puzzle
context says a box is matched hole by hole, in order, and p1's goal says "in
that order"; a held pad's card has a **Read** button that puts the words on
the card in full and reads them aloud when Marty's voice is on; a step cap is
announced when the lesson starts, the first time with a pointer to the
Trained actions panel, and p5 no longer has one -- there is no lazy way to
make a box of two zeros.

## Two ways in the door

*Added 2 Sep. Ken: "We should replace the Start button with Free Play and
Puzzle Game (and maybe something about the infinity exercises too). If the
player has completed some of the puzzles then the Puzzle Game should provide
the choice of continuing or starting over."*

The card at the door asks who is working here; it now offers **Free play**
and **Puzzle game** instead of Start. Puzzle game opens the first puzzle -- or,
for somebody who has been here before, says "You were on puzzle 2, with 1
solved" and offers *Carry on at puzzle 2* or *Start again from the first*.
Where they got to is kept per person in this browser, beside their notebook:
the puzzle they are on is written when a puzzle opens, and a puzzle is marked
solved the moment the judge offers the next.

**The set has to be in the page.** A published artifact can fetch nothing, so
`embed_puzzles.py` puts p1 -- which carries every later puzzle in its
library -- into a JSON block beside the embedded manual, and the app reads it
at boot and remembers every world in it by name. Locally the files are still
fetched, so edits show up without re-embedding; run the script after
`make_puzzles.py` whenever a puzzle changes, the way `embed_manual.py` follows
the manual.

The infinity activities are not a third button: they are activity sheets that
open the workshop with `?activity=N` from outside, and a door inside the
workshop would need a sheet to hand back to. Left for a proper look.

**And a suite bug worth its own line.** The verdict's `ok` was an `&&` over
the flags that existed when the line was written. Every check added since --
nineteen of them -- reported PASS or FAIL in the log and was ignored by the
verdict, so a run could say `ok: true` over a FAIL line, and for most of a day
did. It now ANDs every flag, and the puzzle check that had been failing
quietly is green because its waits were wrong: the "not quite" note lands
AFTER the answer it accompanies, and the well-done note lands after the Next
button is armed; a check that reads the nest the instant the flag flips reads
it too early.

## The post, the ship, and a power of a prime

*Added 2 Sep. Ken: Marty and the card both say the goal; +3 dropped on −3 made
−6; could Mimi be a character, and why would she copy things; the "make it
more general" advice after a run confuses in a puzzle; more puzzles; and the
original's backstory needs the damaged ship to be visible, or another story.
Then, from a number cube: "Surely it isn't prime"; the words face should be
the whole name with the middle shrunk, not the short reading; a cube turned
in the closeup lay askew after Escape; Ctrl+C read out every digit.*

**One voice for the story.** Marty tells you what is wanted; the card said it
again, word for word. The card keeps to what a card is for -- where you are
and what the controls do -- and it is the card's *idle line* now, not a
one-off `say`, since the idle line is what `refreshUI` writes back the moment
your hand is empty and it had been overwriting the puzzle's line with "Take a
little robot from its stack".

**−6 was the badge model showing through.** p4's "minus three" was a 3
wearing a subtract badge, so dropping a plain 3 on it added 3 to its value
and showed 6 under a minus. The workshop's own rule is that *the minus key
negates* and adding a negative is subtraction; p4 now hands out a real −3,
and either drop makes 0. Measured both ways.

**Advice, not a verdict.** A robot that did its job once and stopped because
its desk no longer fits its thought has often just finished; telling the
player to loosen it read as a correction. It reads "Ran 1× and stopped: what
is on its desk no longer fits its thought. If you want it to work in more
situations, wake Ruby..." now.

**Puzzle 6 is the post.** There is no Rounds control any more -- a robot runs
until its thought stops fitting -- so the original's "double until 1,024"
cannot stop itself here, and neither can "four zeros by doubling". What
stops by itself is a nest: the original's *add up all the numbers on the
nest*. A box of [nest with 2, 3, 4 | 0], a robot, and Ruby: train one take
and one drop, loosen the number and the zero in its thought, give it the box,
and it adds a number a round and dozes when the nest is empty. That is the
first puzzle that needs Ruby, and the first whose end is the robot going to
sleep. Measured: thought "a box of any number and any number", total 9, pile
0, "the robot shrinks and waits", judge accepts.

**The ship.** Ken kept the original's story on condition that the damaged
ship be visible. It is a made model -- cylinder, scorched cone, two fins, a
stripe, a porthole, two puffs of smoke -- lying on its side at the back of
every puzzle table, fixed and ghost, and p1's intro points at it: "that's it
lying over there with its nose burnt". A fixed thing that is also ghost is
scenery, and its tooltip says it stays where it came down rather than calling
it the goal.

**A power of a prime is not prime.** The sixth face takes a whole number
apart, and 19 to the 199th came apart as a single part, "19¹⁹⁹", which the
one-part test read as prime. Prime is one part to the power of one; a lone
part with a power says "a power of the prime 19".

**The whole name, head and tail.** The short reading was offered whenever
the English name would not fit; Ken wanted the name itself, beginning and
end with the middle closing up, exactly as the digits face does. The short
reading remains only past the last Latin scale, where there is no name.

**Square on the table.** The hand's turn rolls a number about the line of
sight so its writing is upright for the camera; the closeup borrowed that
roll, and with the camera a little above the table it leaned the cube a few
degrees -- and after Escape it lay askew for good. Turns in the closeup are
quarter turns about the table's own axes now; measured axis-aligned after
Escape with two turns applied.

**Ctrl+C says it in a breath:** "Copied: 733333333… and 111 more digits", or
"… and 153 more words" on the words face.

**Mimi as a character** is a question, not a build yet. Her name says what
she is: a *mime*. A mime copies what she is shown -- and a mime *pulling a
solid copy out of the air* is a natural animation for a machine whose whole
job is that a copy appears. She would keep her platform and tray as a little
stage, and get a face like the others. The other candidate was a mimic
octopus, which also copies for a living; the mime is the better fit for the
name and for a cast of people rather than animals.

## A ship to travel in, a mime, and a robot you have to stop

*Added 2 Sep. Ken: stop bundling the later puzzles inside each earlier one
(files can be fetched, and an artifact can take them once into browser
storage -- postponable); yes, show the new Mimi; the ship should not be on the
desk but in the background, big enough for Marty to have travelled in; "hand
it to the robot instead" was heard while building the box of 8, 16 and 32;
picking up a turned number turned it again; a cube's face could end up not
parallel to the desk; and the 1,024 puzzle should ask for exactly 1,024, so
the player has to stop the robot in time.*

**One file, one puzzle.** Each `pN.world.json` is its own puzzle now with no
`library` inside it, and `embed_puzzles.py` bundles every file in
`examples/puzzles/` into the page as `{ worlds: { p1, p2, … } }` -- a robot's
`load` finds the next by name in memory, or by fetch when there is a server.
The reader still accepts the old one-world shape. Seven puzzles pack to five
kilobytes of gzip.

**The ship is scenery.** A world file has a `scenery` list: things that stand
in the *room* rather than on the table, each with a place, a turn and a size.
Marty's ship lies on the floor beyond the far side of the table at seven times
hand size, nose toward the room, and its label is scaled back down to twice
hand size so a sign the size of a door did not hang off it. Scenery is fixed
and ghost by nature, saved with the world and cleared with it. Measured after
loading p1: one model at (2.3, 0, −1.6), scale 7, labelled "Marty's ship".

**Puzzle 7 is the one you stop.** Exactly 1,024 from a single 1: a robot
trained to take the number out of its box, set it on Mimi, put the copy in
the box and drop the original on it -- six steps -- then loosened by Ruby,
doubles every round and never stops on its own. The Stop button (and now the
full-stop key, which the manual always said stops things but which did
nothing during a run) lets the robot *finish the round it is in*. So the
moment to stop is while the box says 512: that round ends at 1,024, and the
next number is 2,048 with no way back but Start over. Marty says exactly
this. Measured: training 6 steps, thought "a box of any number", a round of
about 17 s at 1× and 3.3 s at 8× (at ∞ the number is astronomical within
seconds -- that speed is the player's own choice), the wrong answer comes
back "Not quite — it has to be exactly 1,024", and the run stopped by "."
reports "Stopped after N rounds — it finished the one it was in".

**A turned number stays turned in the hand.** Pickup set the thing's turn to
identity, so a cube turned to the face you wanted read one thing on the
table and another in the hand. The turn it had is the hand's base now and the
arrows turn from there; measured: a 90° turn survives pickup.

**Square on the table, whatever the hand rolled.** The hand rolls a number
about the line of sight so its writing is upright for the camera, and that
roll rode along in `aim`: after a few turns a cube could lie on the desk a few
degrees off. A number or model set down snaps to the nearest of the 24 square
orientations. Measured: off-axis 0.46 in the hand, 0 after the drop.

**The desk of no robot is more table.** With no robot at the bench, a drop
on the desk went to "hand it to the robot instead"; it goes to the table now.

**Mimi, rendered.** `mimi_v1.py` builds the mime in Blender: white face,
black beret, black-and-white striped top, white gloves held up palms out --
the invisible wall, which is the copying pose -- Marty's own eye in her
colours, a small closed red mouth, one painted tear, and the family's amber
badge. `mimi_v1_hero.png` and `mimi_v1_sheet.png` are the look; the glb is
exported but she is not in the app until Ken says so.

## Seven more puzzles, a recipe for making them, and Dusty eats a stack

*Added 2 Sep. Ken: "please add more puzzles"; then "can you write a document
describing how a user could create new puzzles -- I noted that Dusty doesn't
seem to be able to remove stacks".*

**Puzzles 8 to 14** follow the originals' next steps with what the workshop
already has: a box inside a box inside a box; three zeros in the second hole
of a box, with Mimi to copy the one zero; six zeros from a box of two, copies
joined side by side; the door code 77 from a box of powers of two (a sum by
choosing, each number once); a half, from a 2 wearing a divide badge; a
million from a 10 and a times-ten badge copied five times; and A, B and C on
pads in a box -- the first puzzle that lets you type. Every judge accepts its
own goal in the suite, and the mechanics each one leans on were measured on
the page: divide (1 ÷ 2 = ½), times (10 × 10 = 100), a sum out of the box
(64 + 8 = 72), a box copied on Mimi and joined to its copy (two holes and
two holes make four), a capital A typed onto a blank pad under the typing
rule, and the goal [[[_]]] built from a hole list with `None` in it.

**A hole is a None.** `empty_box(n)` had written the sparse `{n, at}` form,
which the reader never understood: it counts `holes`, so every "empty box"
was a two-hole box, and p1's happened to be right. It writes a list of Nones
now.

**A real click has a point.** The test hook that clicks a thing carried no
point, so a number dropped on a number by script fell through to "set it
down beside" and stacked instead of adding -- which is not what a hand does.
The hook passes the thing's centre now, as a click would.

**How to make a puzzle** is written down in `examples/puzzles/MAKING-PUZZLES.md`:
the file's shape and every field; route one, building it inside the
workshop (set the table, take away stacks, build the judge house by training
its team, save, finish in a text editor); route two, the Python helpers with
a whole puzzle in twenty lines; what the judge can and cannot decide (exact
identity, anything-or-nothing holes, no emptiness, no behaviour, no Rounds);
chaining with `load`; embedding a set; and a checklist.

**Dusty swallows a stack.** Route one had a hole in it: a puzzle is a world
with fewer stacks, and the only way to have fewer was to edit the rules by
hand. Point Dusty at a stack now and the whole stack leaves the world -- in
free play that writes the whole workshop down as rules first and takes the
one stack out, so the save records exactly what is left. One of the stack's
cubes rides on his head, and clicking it gives the stack back. A robot cannot
be taught it. Measured in the suite: free play had no rules; the box stack
leaves the rules and is hidden; the save has no box stack; it rides with
him; it comes back.

## Mimi in the workshop, a ship that came down hard, and a quiet Next

*Added 2 Sep. Ken, with a picture of the ship: "If the user clicks on Next
puzzle then stop any ongoing narration. I think the broken spaceship can look
more broken. In free play I didn't see the new Mimi -- your design looks
good."*

**Mimi stands at her machine.** The mime from `mimi_v1.glb` is part of the
copier's node now: beside it on the bench side and a step behind, turned to
face her platform, hands up in the invisible-wall pose, at nearly twice the
size she was modelled at so her eyes are between the tray and the platform.
Clicking her is clicking the copier. Because she is a child of the copier's
node, a puzzle without Mimi hides her with the machine. The two artifact
builds carry her glb with the others.

**A new world silences the old one.** Next puzzle, Start over and a robot's
`load` all go through one `hushNarration()`: whatever the voice is reading
stops, and a demo in progress with it. Marty had been reading out the last
puzzle's note over the next puzzle's intro.

**The ship came down hard.** The nose is bent up and off the line of the
hull and scorched, with a scorched band behind it; a gash of three dark
slivers runs along the side; the hull is dented; one fin is still on, bent,
and the other snapped off and lies on the ground behind; the stripe is torn
in two; the porthole is cracked; bits of hull, nose and fin are scattered
where it slid; and three puffs of smoke still rise. Seen from two angles
by rendering the page's own canvas to a picture.

**Looking without a big pane.** The browser pane here is small and its
screenshots smaller, so the pictures in this round came from the page
itself: point the camera, render one frame, draw the canvas into an 800-wide
JPEG and hand the data URL out through the test hook. (A result over the
tool's size is saved to a file, which is where a picture wants to be.)

## No box for the doubler, a shorter Marty, advice only while it applies

*Added 2 Sep. Ken: "For the 1024 puzzle Marty starts off saying too much
about how to solve it. Also why do we need a box (original ToonTalk did but we
don't). After using Ruby to erase the advice to erase came too late -- no need
to say it if it has already been done. The box in a box in a box puzzle
shouldn't have 1-hole boxes because they aren't usefully nested. 2-hole boxes
are better."*

**The box was never needed.** A robot here can set a thing down on its own
desk where its given thing was: the stand is a container like a hole, and a
put on an empty stand is a put. So the doubler is trained on a bare 1: take
it, set it on Mimi, take the copy, put the copy on the desk, take the
original off the platform, drop it on the copy -- six steps, no box, and the
round ends with the doubled number where the given was, which is what the
next round needs. Measured in free play: trained to 2 on the desk; loosened
to "any number"; ran to 4 in two rounds and stopped cleanly by the full-stop
key. Puzzle 7 hands out a 1 and a robot and nothing else.

**Marty says less.** The intro is what the computer needs and the one fact
that matters -- a doubling robot never stops by itself, so you will have to
stop it in time -- and the recipe moved into the hints, where a visitor who
wants it asks.

**Advice only while there is something red.** "Wake Ruby and click a red
part" was appended to every stop and every refusal, including after Ruby had
already loosened everything. Both places now compute the red parts first and
say the Ruby line only when there are some.

**Two-hole boxes in a box in a box.** One-hole boxes nest without ever
looking nested; the puzzle asks for each box in the FIRST hole of the next,
so the goal is [[[_|_]|_]|_] and the judge reads it hole by hole.

## Mimi acts

*Added 2 Sep. Ken: "Can Mimi move and use her arms so it is clear she is
running the copier?"*

**A rig at load.** Her model is loose parts under one node -- the way the
Blender script built her -- so when it arrives the parts are regrouped: each
arm, forearm, glove and cuff under a shoulder pivot at the top of the arm,
and the head with everything on it under a neck. `attach` keeps their places;
only the pivots turn.

**The machine tells her what to do.** The copier's three steps -- the scan,
the copy growing out of the air, the copy lowered into the tray -- each set a
target pose as they run, with their own (0..1), so her acting keeps time with
the machine at any speed and pauses with it. She is small beside her
machine (the platform is above her head), so she conducts it: reaches up to
the thing on the platform and follows the scanning bar down with her hands,
gathers the copy between her gloves in front of her, lowers it to the tray,
and goes back to the wall. Between copies she feels along the wall, one hand
and then the other, and looks about. The joints ease toward their target
every frame, faster while acting, so nothing snaps. She now stands squarely
facing her platform.

**Measured** by stepping the world's frames by hand (the pane's tab was
hidden, so nothing animated on its own): the target pose changes with each
step -- scan start, scan mid, pull, lower -- the joints follow, the copy
lands in the tray, and after two seconds she is back to the wall.

**And she hands things over.** *Ken: "The animation is ok when Mimi is given
something but she should move her arms when taking something off the
copier."* A thing leaving her platform or her tray -- by a hand, a claw or
Dusty, since all of them go through `detach` -- starts a short act of her
own rather than a copier step: from the tray her hands go down to it and open
outward, from the platform they reach up and open the same way, with a look
down or up to match. Measured by stepping frames: the act starts on the take
from the tray (`copyOut`) and on the take from the platform (`copyIn`), and
the joints follow it.

## Spaced by width

*Added 3 Sep. Ken, with two pictures: "puzzle 9 has the boxes overlapping.
When I joined 2 [0 | 0] one of the numbers became the wrong size."*

**Materials are spaced by how wide they are.** The table laid its materials
0.45 apart whatever they were, and a three-hole box is 0.62 wide, so puzzle
9's boxes sat on each other. `width_of` in `make_puzzles.py` knows the app's
own rule -- a cube for a number, holes and walls for a box (holes shrink to a
floor as the count grows, then the box widens), a face for a pad -- and
`table` lays the row out from those widths with a gap between. Puzzle 9's
zero, three-hole box and two-hole box now stand at −0.69, −0.12 and 0.57.

**The wrong-sized zero I could not reproduce.** Joining two boxes of two
zeros was measured three ways -- the held copy on the right of the original,
the copy straight from the tray on the left, and every zero read back --
and all four zeros came out at the four-hole scale (0.47 in a 0.12 hole).
The join moves each thing with the same call that fits it to its hole. The
picture shows the big zero standing a little higher than the others, which
is how a number looks while it rests on another for a beat before merging;
so the likeliest story is a zero dropped on a zero in the box just before or
after the join. Ken has been asked for the exact steps.

## The zero under the pointer, and five more puzzles

*Added 3 Sep. Ken: "When I dropped [0 | 0] on a copy I was holding it over
one of the zeros (see tooltip) -- I suspect that is relevant. After fixing
this do some puzzles."*

**It was the wiggle.** The thing under the pointer wiggles to say it is
ready, and the wiggle writes the thing's scale every frame from the size it
started with. Ken dropped a box on the side of a box with the pointer over
one of its zeros: the join fitted every zero to the four-hole size, and the
wiggle wrote the two-hole size back over that one -- and restored it again
when the pointer left. Reproduced with real pointer events on the canvas
(the test hooks bypass the pointer, which is why the first three tries came
out right), and fixed where a thing is fitted to a hole: the wiggle is told
the new size. Measured the same way after: four zeros at 0.47. The suite
has `wiggleFitCheck`, which aims the wiggle at a zero and joins.

**Puzzles 15 to 19**, after the originals' next steps: the seconds in a
year from 365 and three times-badges (31,536,000); the word ToonTalk from
two pads joined at the right edge; three quarters from a 1, a divide-by-four
and a times-three; which is bigger, ¾ or ⅔, on a scale with the bigger in
the left pan (the judge reads a scale hole by hole like a box); and a box of
exactly 24 zeros from a box of three, copied and joined three times -- a
long box, which shows its ends and says how many holes lie between. Each
mechanic measured on the page: the times chain, the edge join, the fraction
chain, the pans and the tilt.

## Intros that keep the secret, edges that join, and three robot puzzles

*Added 3 Sep. Ken: "Puzzle 19 gives too big a hint before the player
starts. Make sure other puzzles also don't start with too big a hint.
Joining boxes doesn't accept a drop like in the screenshot -- any overlap
between the left or right edge of what is held with the opposite edge of the
thing underneath should be good for joining. True for pads too. Otherwise
all the puzzles are good -- keep going creating puzzles -- especially robot
training puzzles."*

**Intros say what, hints say how.** Puzzles 6, 10, 13, 14, 16 and 19 had
their method in Marty's first words; each now states the need and what is
on the table, and the method moved into the hints where it is asked for.

**An edge over an edge is a join.** A held box or pad set down on the bench
with its left edge over the right edge of a box or pad already there -- or
the other way about -- joins it on that side, exactly as a drop on that edge
would; before, only a drop that landed on the other thing joined, and Ken's
overlapping drop was "click to put that down". Measured: a copy set down
overlapping the right edge of [0|0] makes [0|0|0|0]; over the left edge, the
same; Talk over the right edge of Toon reads ToonTalk, over the left edge
TalkToon.

**Puzzles 20 to 22 are robots.** Twenty turns [3|2|1|_] into [1|2|3|_]: a
spare hole and a plan, three moves, one run. Twenty-one counts the letters
on a nest and sends each on by bird, adding a copy of a 1 to a count each
round, and dozes when the nest is empty -- the first that loosens two parts
of a thought (the letter and the count). Twenty-two grows a box by one hole
a round, copying a seed box of one zero from the box's second hole and
joining the copy on to the box in its first; it never stops, so the player
stops it at nine and, if it stopped at nine, runs one more round -- the same
lesson as 1,024. Each was trained and run by script: the reverse in three
moves; the counter's round of seven steps; the grower to nine holes, one
per round, stopped by the full-stop key.

**Two things the grower taught.** Ruby's ladder climbs from the innermost
detail -- clicking the box in the thought first loosens the zero inside it,
then the box's contents to anything, and only then the box itself to "any
box, any number of holes" -- so the hint says to click until it says so.
And in a lesson Dusty can only vacuum the robot's own things, which the
top of a pile is not; the counter sends its letters on by bird instead.

## Stuck fast, a robot handed on, and a tooltip that tells the truth

*Added 3 Sep. Ken: the edge-overlap drop works but the tooltip is wrong and
the box underneath should wiggle; a puzzle between 20 and 21 could hand the
player the robot from 20 with different numbers, so Ruby or Dusty is the
whole job; "I am a bit worried about how a player might just move the numbers
without the robot... Maybe the numbers are stuck into the box except the
robot is stronger"; puzzle 21 cannot use the bird in its fourth hole; and a
robot froze picking a copy off the copier.*

**The tooltip and the wiggle.** Hovering the bench with a box or pad held
now says "Drop to join the boxes -- its holes go after these" (or before),
and the thing that would be joined WIGGLES, so the drop is offered before it
is made. The full suite then caught what the edge-join had broken: a
behaviour is a pad, so setting a gadget down beside another pad joined them.
Gadgets, named pads and pads carrying scenes are excluded; joining those is
still a deliberate drop.

**Stuck fast.** A thing marked `stuck` cannot be lifted by you -- it wobbles
and says a robot's claw is stronger -- and a robot takes it without trouble.
Ruby leaves it alone too. It travels with the thing and is saved with the
world, so a puzzle can hand you numbers that only a trained robot can move.
That is Ken's own answer to the question of why one would train a robot when
dragging is quicker.

**A robot handed on.** Puzzle 20 trains a robot to move three stuck numbers
across into a second box, last first. Puzzle 21 gives you THAT robot, already
trained, and different numbers: it refuses, shows its thought with the
numbers it remembers in red, and Ruby is the whole puzzle -- three clicks and
it runs. The shape changed on measurement: a robot that swaps numbers inside
one box reverses them back for ever once loosened, so the round moves them
ACROSS, and a round that empties the box it reads cannot fit its own thought
again. It stops by itself.

**The bird could not stay.** The counting puzzle sent each read letter on by
bird from the box's fourth hole; a bird has to fly home, and the robot's
thought wants her in her hole. It uses Dusty now -- and Dusty in a lesson can
only take what is standing on the robot's own things, not what is in its
claw, so the round is: take the letter, set it on a work spot, vacuum it,
take a fresh 1 from the number stack, drop it on the count. Measured: five
steps, loosened twice, four rounds, dozing on the empty nest with 4 in the
box.

**The copier froze because the tray was empty.** Clicking the tray while
Mimi was still scanning fell back to the other surface and took the ORIGINAL
back off the platform -- one step into a program that no longer made sense.
Both the robot's own clicks and yours now say "the copy is still on its way"
instead.

**A fabricated click point cost three rounds.** The test hook that clicks a
thing had been filling in the thing's centre as the point of the click, so a
scripted drop always landed in the MIDDLE of a pad -- which means "ride here",
not "join". The turtle stopped walking, the bindings check threw, and the
failures looked like a regression in the edge-join written the same day. What
found it was bisecting the app itself: serve an old commit's file as
`app_probe.html` and point the harness at it with `?app=`. Two runs said the
break arrived with the hook, not with the join. The hook passes a point only
when the caller means one now.

## "Not" is a matter of order

*Added 3 Sep. Ken, on the making-puzzles document: "true there is no direct
'not behavior' but a robot behind can be arranged to run when the match is
not something." And: American spelling, please, even though he lives in the
UK.*

The document said a thought bubble cannot judge behavior and left it there.
It was half the truth. A team is tried **in order** and the first member
whose thought fits is the one that runs, so a member placed behind the
others runs precisely when none of them matched. That ordering is the only
way to say *not* in this language, and the judge has been leaning on it since
the first puzzle: the leader recognizes the goal, and the members behind it
catch everything else and send the "not quite" pad back. A robot back there
can do more than complain -- it can count the tries, answer differently each
time, or hand back a hint. Both places in the document that touched on it now
say so, and the note about behavior says what is still true: a thought cannot
name "keeps getting bigger", so a puzzle whose answer is a process is written
to leave a thing behind.

American spelling from here on, in the app and in these notes.

## Six from a play session

*Added 3 Sep. Ken: the card said Ruby had loosened enough when she had not,
and the parts that still did not fit stopped being red; a box dropped into a
hole joined instead, and Undo gave back the box joined TO and not the one he
was carrying; Mimi blocks the stacks in the opening view; a goal number's
tooltip offers typing a puzzle has taken away; a wide goal hides the bird and
her nest; and the ship should stand further back.*

**An erasure that was not enough now says so.** Rebuilding the thought threw
away the red marks with the nodes they were painted on, so a partial erasure
left a thought with nothing red in it and a card quoting the loosened
condition as if it fit. After each erasure the parts that still do not match
are marked again, and the line reads "...Still not what is on its desk — the
red parts are what to loosen next". It is said as an attention message,
because a plain one cannot displace the refusal already holding the card --
which is how Ken came to read a stale "the number 3" line after loosening
that very 3.

**Undo puts back what the claw was holding.** The undo snapshot captured your
hand and the whole table but not the robot's claw, and restoring emptied it.
Ken meant to drop a box into a hole, it joined instead, and Undo handed back
the box that had been joined to and nothing else. The claw is in the snapshot
now, by reference for a robot, nest or bird and by description for anything
else. Measured: a lesson step that joins, undone, leaves the box in the claw
and the step gone.

**A tooltip may only offer what is on offer.** A number in a puzzle where the
keyboard is gone no longer promises "type digits", the goal says it is the
goal, and a stuck thing says a robot's claw can move it.

**Room to see and room to reach.** Mimi and her machine stood square in front
of the box stack from the door; they are further out and back, and she stands
on the outer side of her machine. A ten-hole goal is a metre wide, so the
goal is centred at the back and the bird and her nest are placed clear of
whichever end of it is free -- both stay reachable however wide the goal
grows. The ship lies further back again.

## A robot that knows when to stop, and a voice one sentence behind

*Added 3 Sep. Ken: "Maybe puzzle 24 should introduce the idea of using a
scale so that the robot like puzzle 23 can make a box with any number of
zeros. And let's add more. When I use Ruby multiple times quickly the
narration falls behind and explains the old actions -- no need to explain
things that were more than one action ago -- but the transition should be
natural." And: puzzle 22's nest obscured the goal, and the goal was tinier
than need be.*

**Puzzle 24 is the grower with a scale.** The box's third hole holds a scale
with a count in the left pan and the 7 the computer wants in the right. The
robot's round is the same as before plus one step: a fresh 1 from the number
stack dropped on the count. Its thought records the scale *tipping right*,
and -- the one change the app needed -- Ruby now keeps which way a scale tips
when she loosens what is in a pan: "any number, but still the lighter one"
is the whole use of a scale in a thought. Measured: trained in eight steps;
the thought read "a scale tipping right, weighing the number 1 against the
number 7"; loosened to "any box" and "any number" with the tilt intact; ran
five rounds and stopped by itself with seven holes and the pans balanced.
Change the number in the pan and the same robot makes any number of zeros,
which is what the note at the end says.

**The voice stays one sentence behind at most.** The browser queues spoken
utterances without limit, so four quick erasures left it explaining the
first while the fourth had happened. Now one message waits, at most: a new
one replaces whatever was *waiting*, never what is being *said*, so the
current sentence ends naturally and the next thing spoken is the latest.
Nothing is cut off mid-word, and nothing older than one action is said.

**The goal, seen.** For a small goal -- one number, one pad -- the bench
record now carries a size and the thing stands half again as large; the
size is the bench's, not the thing's, so a copy made from it is ordinary.
The bird and her nest sit to the left of the goal in every layout, or at
the front right for the two goals too wide for that, so nothing stands in
front of the goal from the door.

## Eight more, and Dusty reaches the top of the pile

*Added 3 Sep. Ken: "While training a robot Dusty wouldn't vacuum the top of
a nest stack -- I had to move it to a spare work area and then vacuum it.
Did you address the obsolete narration issue? Many more puzzles please."*

**The top of a pile is the robot's too.** A delivery on a nest the robot was
given has no address of its own, so in a lesson Dusty refused it. It is
addressed now the way a take is -- the nest, and "the top of what is on
it" -- and the vacuum step carries that. Measured: one step recorded, the
pile one shorter. The counting puzzle's hint no longer sends the letter to
a work spot first.

**A saved robot keeps its tilt.** Saving and loading a thought dropped the
scale's tilt on both journeys; a robot trained to run while a scale tipped
right came back weighing anything against anything. Both directions keep
it.

**Puzzles 25 to 32.** Two more robots that stop by weighing: 1,024 again,
by a doubler in a scale's pan against 1,000, hands off this time; and down
to one, by a halver that copies its divide badge each round and weighs the
number against 1. Two scales by hand: the biggest of three, and a pair
sorted into a box smaller first. A robot that swaps a scale's stuck pans
through a spare hole, one run, because once swapped the thought no longer
fits. And three of letters: a box of letters poured onto a blank pad becomes
the word; a word dropped into a box with no holes comes apart a letter to a
hole; a pad dropped on a 3 picks out the third letter of Marty. Every
mechanic measured on the page -- the pour, the mould, the pick, the swap,
the doubler running to 1,024 and the halver to 1 -- and every judge accepts
its own goal.

The narration was answered in the round before: at most one sentence waits,
and a new one replaces what is waiting rather than what is being said.

## A drop on a scale means a pan

*Added 3 Sep. Ken: "While training the robot I accidentally picked up the 1
instead of the box with the 1 in the second hole. When I tried to drop back
in it ended up on the desk."*

An empty pan is a thin dish hanging under a wire and a beam, and from where
the camera stands a click on it meets the wire first. So the click meant
the scale, not the pan: the robot recorded "put it in hole 3", tried to
combine a number with a scale, was refused ("only numbers combine") and set
the 1 down on the bench. Measured before the fix: the step read `put [2]`
and the number stood on the bench; after it: the 1 is back in the left pan
and the step reads `put [2, 0]`.

Now a drop aimed at the scale itself means the pan on the pointer's side --
for your hand and for the claw alike, and an occupied pan takes the drop
onto what is in it, so a 1 aimed at the 7 in the right pan makes 8. The
tooltip says which pan. A step that names the scale (recorded before this)
lands in the pan on its recorded side when replayed.

## Sorting by team, a smart camera, and a robot that waits for Run

*Added 3 Sep. Ken, in one batch: the narrator said "Ran 5x" for a robot he
had watched run 1 + 6 times; puzzle 26 would be better with fractions or
very large numbers so nobody already knows which way the scale tips; puzzle
28 has no motivation for a robot rather than the scale; he expected a
sorting challenge after 28; a "smart camera" that zooms in on the action
while keeping some context, behind a toggle; and puzzle 32 was too easy to
cheat by grabbing the 1 from the scale -- with the worry that a robot
strong enough to move stuck things could pull the 1 out for the player.*

**Ran 5x, seen 1 + 6.** Measured on the page: after a lesson rewinds, the
thought still fits what is on the stand, so Ruby's first loosening set the
robot going while Ken was still loosening. It ran once, stopped when the
grown box no longer fit the still-particular thought, and ran five more
after the next erasure -- one, then five, and the training round makes
seven. The narrator counted the last run correctly; it was the early start
that was wrong. Now an erasure sets the robot going only when it turns a
mismatch into a match -- puzzle 21's whole point -- and a thought that
already fit waits for Run. The hints that said "give it the box, press Run"
say "press Run, it still has the box", since after the rewind it does.

**Puzzle 26 weighs 5/7, 8/11 and 13/18.** Nobody knows by eye; the scale
does.

**Puzzle 28 is the smallest piece of sorting.** Two stuck fractions, too
close to tell apart, the bigger one on the left: the scale says which is
which, and only a claw can swap them. The intro says so, and says a team of
these will sort three, which is now puzzle 33.

**Puzzle 33, the sorting challenge.** Three stuck fractions in a five-hole
box: a scale in hole 1 with two of them in its pans, the third in hole 2,
and holes 3, 4, 5 empty. Four robots: the swapper (a scale tipping LEFT:
left pan to hole 5, right pan to left, hole 5 to right, with Ruby on both
pans and Dusty on hole 2) and three movers, each keyed on a scale tipping
RIGHT and on which hole is full -- hole 2: left pan to hole 3 and hole 2 to
the left pan; hole 3: right pan to hole 4 and hole 3 to the right pan; hole
4: left pan to hole 2 and right pan to hole 3. Three compare-and-swaps, and
the team stops by itself when the scale is empty. The player trains on a
practice box of other fractions, running each robot once to reach the next
phase, then drops the four on one another and gives the team the stuck box.
The first design used hole 4 as the swapper's spare -- and hole 4 is where
the third mover parks the biggest number, so the swap ADDED two fractions:
71/45 in a pan, caught by running the team before writing a hint. Measured
after the change: both boxes sorted, five rounds each, and the player's
route trained by clicks gives exactly the thoughts the hints describe.

**Stuck stays inside.** Ken's idea, from an earlier round: things stuck in
a puzzle that only a robot is strong enough to move. His worry now: the
robot could pull the 1 out of the scale and hand it to the player. So a
claw can move a stuck thing only inside the thing the robot was given --
not out to its work area, the copier or a bird -- and puzzle 32's 64 and 1
are stuck, with the whole box, its scale balanced at 1 against 1, as the
answer. A step that tries to carry a stuck thing out is refused in a
lesson and aborts a run.

**And a rewind that forgot the flags.** Found while measuring the above:
after any lesson, the goal could be picked up and the stuck numbers moved
by hand. The rewind rebuilds the bench from specs, and three things dropped
the flags on the way: a full spec did not pass "full" down into a box's
holes, the robot's given was snapshotted without it, and a rebuilt box or
scale skipped the step that puts a thing's flags back. All three fixed;
measured on puzzle 28: fixed and stuck survive a lesson, on the bench and
on the stand. Undo had the same hole.

**The smart camera.** With Ruby or Dusty awake, pointing at the thought
bubble brings the camera in along its own line of sight -- the same view,
closer, so the workshop stays around the edges -- and pointing away brings
it back. A clock, like the closeup, so it always comes home. It is a toggle
in the More menu, remembered between visits, because a camera that moves by
itself is not always wanted.

**The balance question, answered.** Ken's question had been whether the
scale should *know* that multiplying by 2 is the same as dividing by 1/2
-- "there is some pedagogic value to this." It does now: a number's weight
is what it does. A plain 3 is "add 3"; a badge number is an operation, and
a divide badge folds into multiply by the reciprocal, a subtract badge into
add the negative, so x2 balances /(1/2) and +3 balances -(-3), and x2 is
lighter than x3. Across families -- a doubler against a plain 3, a power
against a multiplier -- the scale cannot decide and the beam bobs, which is
what it already did for a number against a word. Measured on four scales:
= = R ?.

## Signs, not answers; a camera on the action; two robots before four

*Added 3 Sep. Ken: puzzles like 26 should not show the answer -- a sign
saying "we need the biggest number" makes it more challenging, and 27
should be like that too, and harder; the smart camera should do more, for
instance when the numbers on the scale the robot works on are tiny, or when
the robot drops an operation on a tiny number; puzzle 30 should hint how to
make a no-hole box rather than provide one; the Ruby tips repeat too often;
the robots stand in front of the goal box; 33 is too complex for the first
puzzle involving teams.*

**A sign for a goal.** Puzzles 26 and 27 show a pad -- "the biggest of the
three", "the smaller one first" -- where the answer used to stand; 27's
numbers are 7/12 and 5/9. The judge checks the answer as before; the sign
is only what the player sees.

**The camera follows the work.** In a lesson or a run the smart camera
comes in on what the robot's claw carries, or what is in its hands, close
enough to read a small number in a pan and far enough to keep the robot and
the desk in the picture. Pointing at the side of the screen leans it back
out, so the stacks, the copier and the work area stay reachable; the
thought-bubble rule from before still holds in the workshop. Measured: the
camera 2.6 from the given box during a lesson, out again with the pointer
at the edge, and unmoved with the toggle off.

**Puzzle 30 makes its own mould.** The box stack is there instead of the
mould, and the hint says how a box gets no holes: hold it and type 0.

**The Ruby advice, twice.** The full sentence the first two times a
session needs it; after that a few words -- "Ruby or Dusty can loosen the
red parts."

**Robots at the back.** In the sorting puzzle the four robots stand on the
back row between the judge and the goal, where they hide nothing.

**Puzzle 33 is two robots, one run.** Two stuck fractions in a scale
tipping left and a spare hole: the swapper (tipping LEFT) swaps the pans
through the spare hole; the mover (tipping RIGHT) moves the right pan out.
Dropped one on the other they make a team, and one Run does both: swap,
tips right, move, one number left, nothing fits. Two identical boxes: one to
train on, one for the team. Measured: the team leaves 4/5 alone in the left
pan and 5/6 in the spare hole from a box tipping either way, and the
player's route trained by clicks gives the thoughts the hints describe. The
sorting challenge is puzzle 34.

## Clouds, and a camera that lets go

*Added 4 Sep. Ken: "Can we improve the way thought bubbles look? Both when
a robot is inside and afterwards? More cloudlike maybe? Less circular and
more textured? The smart camera does a good job when beginning to train a
robot but it shouldn't turn off user camera controls (e.g. zooming out if
desired)."*

**Clouds.** The thought's halo above a robot's head is a cloud of soft
puffs now: one round blob painted once, a radial fade with a little mottle,
shown as sprites that always face you, eight round a centre and two on
top, with a thin one underneath -- deterministic from a seed so a rebuilt
thought keeps its shape, and thin in the middle so what the thought holds
shows through. The first two tries were overlapping spheres: additive ones
summed to a white glare that hid the thought, normal-blended ones kept
their crisp circular edges and read as soap bubbles. The same cloud,
smaller, is the mini-robot's preview. The lesson's dome keeps its shape --
it is the whole workshop's ceiling -- and wears a tiled cloud texture,
wrapped three times round, as an alpha map; a puffy rim tried on it read as
grey discs where the spheres met the floor, and came off. Every puff of the
halo is still a click target for taking a copy of the memory.

**The camera lets go.** The smart camera no longer switches the orbit
controls off while it follows. Orbit or zoom and the follow lets go where it
is; the camera is yours until the next occasion -- the next lesson, run or
thought you point at. Measured: a wheel turn mid-follow ends the follow and
the camera stays where you put it.

## A still mouse, firmer puffs, and a reviewer's five findings

*Added 4 Sep. Ken: "better smart camera but let's not have it do anything
while a user is moving the mouse, wait a second or two after the mouse
stops moving." He also passed on a code review from ChatGPT: the clouds
read as luminous fog rather than discrete puffs and the thought inside is
faint and small; the camera change deserves a regression test across a
whole run, and the yield reset on any transient gap; program descriptions
went into the page as HTML; the dev server's path check was a prefix test;
one robot's disposal could dispose every cloud's texture; the cloud tile's
wrap offsets cancelled; a model that failed to load left "Loading..."
forever; and the one-megabyte file is a maintenance risk.*

**A still mouse.** The smart camera does nothing at all while the pointer
is moving -- neither in nor out -- and acts a second and a half after it
stops. A lesson begun with the mouse in motion leaves the camera where it
is until the hand rests.

**The yield lasts the occasion.** The player's orbit or zoom now holds
until the mode changes or there has been nothing to follow for three
seconds; before, the subject blinking out between two of a run's steps
handed the camera back. A suite check runs a team through a whole run:
still while moving, follows when still, lets go on an orbit, stays let go
to the end, follows the next occasion.

**Firmer puffs, a bigger thought.** The puff keeps a solid core and fades
only at its rim, the seven puffs sit further apart, and the thought inside
is a fifth larger, so the cloud is puffs rather than fog and the thought
reads.

**The reviewer's findings, taken.** Program descriptions are built from
elements and text, never markup -- an imported robot's name or pad text
could have carried HTML into the page; the saved-robot list likewise. The
dev server judges containment by relation to its directory, not by prefix,
so a neighbour named like it cannot be read. The two cloud textures are
marked shared, so discarding a mini-robot with a preview cloud no longer
disposes the puff every cloud uses. The cloud tile's wrapped copies are
drawn on the neighbouring tiles' side, so the dome's texture has no seam
(the old offsets cancelled and painted one spot four times). And a model
that fails to load says so on the loading veil, with the file's name,
instead of "Loading..." forever. Not taken, for now: splitting the file
into modules -- the single file is what makes the artifact and the chat
build trivial, and the suite is what keeps it honest -- and binding the
dev server to localhost, since Ken tests from a tablet on the same network.

## The camera shows the thought

*Added 4 Sep. Ken: "Remember that after leaving training to pull the
camera back enough to see the thought bubble. And when red parts appear in
the thought bubble."*

After a lesson the camera was close on what the robot held, and the
thought that lesson made sat above its head, out of the picture; and red
parts marked in a thought are the next thing to look at. Both now pull the
camera back to a view that holds the robot and its thought -- a glide that
stays where it arrives rather than easing back, since it is a resting view.
The still-mouse rule applies, and your own orbit cancels it. Measured on
puzzle 21: a refused box marks red parts and the camera settles 3.4 from
the thought with it on screen; a lesson ends with the camera at 2.6 from
the box and it pulls back to the same view.

Ken's screenshot, an hour later: a robot ran once, stopped with red parts,
and the camera stayed close on its box. The run's end switches the mode
back to the workshop in the same tick that asks for the thought view, and
the next frame read that switch as a later occasion and forgot the
request. The request now names itself the occasion (and starts a fresh
glide from wherever the camera is, rather than snapping a follow already at
its target). The suite check had passed by accident -- the test window's
default view happens to sit at the same distance from the thought -- so it
now starts the lesson from a far pose and includes Ken's case: a run that
stops with red parts, camera 3.6 from the box and 3.2 from the thought.

## The rounds in all, what the narration points at, and the work area

*Added 4 Sep. Ken: "Notice it says the robot stopped after 17 rounds when
it should be 18 (plus 1 before using Ruby). When the narration or Marty
refers to anything (Ruby, Mimi, the stack of pads, or whatever) then the
camera should pull back enough for that thing to be visible." Then, with a
screenshot of a run cut off at the bottom: "the camera should be pulled
back because you should always be able to see the work area of the robot
(unless the user explicitly moves the camera elsewhere)." And: "puzzle 33
can be accomplished by one robot -- no need for a team or 2 copies of the
box."*

**The rounds in all.** "Stopped after 17 rounds" counted since Run; Ken
counted since the robot was given the number, one round before Ruby
loosened it and seventeen after. Both are said when they differ: "Stopped
after 17 rounds (18 in all with this)", and "Ran 17x (18 in all with
this)". The count in all belongs to the thing on the stand and starts
again with a new one.

**What the narration points at.** A message on the card, or a line from
Marty, is read for the things it names -- Ruby, Dusty, Mimi and her
copier, Marty, any of the stacks, the notebook, the judge, the bird, the
nest, the robot's work area. Any of them off screen brings a view that
holds them and what the player was looking at, from further back along the
same line of sight; never closer. In a lesson or a run the camera then
rests until the next occasion, or the follow would come straight back in
and hide what was just shown. Measured: a lesson's camera close on the box,
"Wake Ruby and click a red part" pulls it back until Ruby is on screen.

**The work area stays in view.** Every smart pose -- following the claw,
the thought view, a mention -- is pulled back along its own line of sight
until what is on the robot's stand and its work spot are on screen. Ken's
screenshot showed the still-mouse rule freezing a glide half-way, the box
cut off at the bottom: a glide already under way now finishes, its target
frozen, and only new moves wait for the mouse to rest.

**Puzzle 33, two thoughts.** With one box, one robot did both steps and no
team was needed. Now the two boxes tip opposite ways, and a robot remembers
which way its scale tipped, so the one trained on the left-tipping box
refuses the other: two thoughts, two robots, and a team that takes either.
Both finished boxes go in a two-hole box for the bird. The team check and
the judge check cover it.

## A robot on the clipboard, supplies for the sort, and a leaning scale

*Added 4 Sep. Ken: one of the untrained robots in puzzle 34 blocks the
view of the scale the robot is working on; he picked up a team, typed
Ctrl+C, it said copied and nothing was on the clipboard; 34 is tricky and a
mistake means starting over -- there should be a stack of untrained robots,
a stack of boxes for training and a stack of test boxes; a scale with an
empty pan should lean toward the pan with something in it.*

**A robot on the clipboard.** Ctrl+C with a robot in hand copied its NAME,
and a nameless team copied nothing while the card said "Copied." Now
Ctrl+C with a robot, a team, a box, a scale, a nest or a room in hand puts
the thing on the clipboard as text -- the same record Save held thing
writes -- and Ctrl+V with an empty hand reads a record back into it, so a
team can travel between two workshops through the clipboard. The card
says "Copied" only once the browser has taken the text; before, the
promise was never waited for.

**Supplies for the sort.** Puzzle 34's four spare robots stood on the
back row, which is the robot's own work area, in front of the scale it was
working on. They are gone: robots come from the stack of little robots,
and Mimi is there to copy the practice box before a lesson, so a slip
costs a copy rather than a fresh start. Stacks of a particular box -- a
stack of practice boxes, a stack of test boxes -- would be a new kind of
stack; Mimi does that job for now, and a copy she makes keeps its stuck
numbers stuck (it did not, which would have let a copied test box be
sorted by hand).

**A leaning scale.** A scale with one full pan leans toward it; it used to
sit level, as though empty. A thought that wants two numbers still does
not fit a scale with one, so nothing that stops by balancing changes.

## Ruby's view, and a run watched from a distance

*Added 4 Sep. Ken: "when Ruby is activated pan and zoom into the thought
bubble. If the erasures mean that the robot matches and will run then the
camera should zoom out to watch the robot run."*

Waking Ruby (or Dusty) brings the camera in on the thought, the same close
view that pointing at the bubble gives, without the pointing. And when an
erasure turns a mismatch into a match, the run that follows is watched
from a distance -- what the robot holds, its work spot and, as Ken added,
Ruby herself, "so the player can turn her off" -- framed together, and the
camera rests there for the run instead of riding the claw. A run started
with the Run button is followed as before. The close-up is a deliberate
close look and is not pulled back for the work area or for her; the wider
views are. Measured: the thought view at five, Ruby wakes and the camera
comes to a length and a half from the thought; the erasure sends the robot
off and the camera out past three from the box, work area and Ruby on
screen, resting.

Two things found on the way. The bubble's tooltip still offered "click to
take a copy" while Ruby was awake -- Ken's "the entire contents of the
thought bubble ended up in my hands" is what that click does when she is
NOT awake, and the tip now says what a click does in each state. And an
erasure silently did nothing when the helper's model was not loaded yet,
since her flight had nothing to fly; it flies a stand-in now.

## Marty shows how to look around, and says your name

*Added 5 Sep. Ken: "I'm about to introduce ToonTalk 3D to my
grandchildren. I'm thinking to start by explaining how to move the camera
around. Then Marty can take over. But what about users who just visit the
site without someone to explain things? I wonder if Marty should be
extended to explain how to move the camera (depending upon whether they
are using a mouse or touch). Not sure if this should be offered to new
user names or just be a button somewhere or part of Marty's greeting. Also
I think Marty should occasionally use the user's name now and then when it
seems natural."*

**All three, because they cost little and reach different people.** A
name signed in here for the first time gets the offer at once, with a
welcome; Marty's greeting, the first time his panel opens, carries the
same offer in a sentence; and a "Look around" button sits beside Ask, Make
and Draw for anyone, any time. Asking him "how do I look around", "how do
I move the camera" or "zoom" is the lesson too.

**The lesson is a demonstration, not a paragraph.** Marty turns the whole
workshop, brings it closer and backs away, slides it sideways, and hands
the camera back where it was, saying at each beat what the visitor's own
hand does to get that -- in mouse words on a mouse (drag, the wheel, the
right button) and in finger words on a touch screen (one finger, a pinch,
two fingers). Which words is known for sure after the first touch or
click, and guessed from the device before that. The smart camera stands
aside for the demonstration, and the last line reminds that a drag of your
own always wins.

**The name.** Where a person would say it -- the greeting, the welcome,
"Now you, Ken", a solved puzzle -- and, for the brain, an instruction to
use it now and then and not in every reply. The solved line says it every
third time, so it never becomes a tic.

## A notebook that would not start

*Added 7 Sep. Ken, on his laptop, at the published site: "The app won't
load -- it shows 'Could not load robot_v4.glb -- Maximum call stack size
exceeded.' I think maybe the notebook has a very large object in it. But I
don't get to see how to enter the user name."*

The message was the new loading veil doing its job for the wrong culprit:
the model had loaded, and what overflowed was the start-up that follows,
which the loader reports as a load failure. The site loaded cleanly in an
empty browser, so the fault was stored state -- as Ken guessed, the
notebook. Its two open pages are drawn at start-up by building what is
filed on them in full, before any of the interface exists; a page holding
something enormous, or nested too deep, overflowed the stack, and with no
interface there was no signing in past it.

Three guards now. A page that cannot be built shows a note in its place --
"a page too big to show; Dusty can take it away" -- so the notebook and
everything else survive. If restoring the notebook fails anyway, it is
parked in the browser under a rescue name and a blank one takes its place,
with a card saying so. And `?fresh` on the address makes a visit that
ignores what the browser has stored without touching it, so a stuck visitor
can look, sign in, and rescue at leisure.

## A village of houses, a table that keeps the camera, and Marty in plain words

*Added 11 Sep. Ken, after his grandchildren played: "My grandson wanted to
make a town/village (like in original ToonTalk). We tried to have a robot
make lots of houses but that didn't work well. Lots of platforms appeared
but most were empty. And some of the platforms intersected with stacks of
elements. ... Marty and narration repeated some instructions. At some point
I couldn't navigate anymore but tooltips appeared I think I could pick up
and drop things. No navigation when desk is being enlarged. My
granddaughter ... tried to ask Marty to make something using voice it
replied: 'Yes, Sisi! Use **Make** and ask Marty for a person or people'.
Also notice the markdown."*

**The empty platforms, measured.** A robot trained to copy a house on Mimi
and set the copy down on an empty work spot repeats "set it down on spot 1".
Spot 1 is taken by the first copy on round two, and a drop onto a house is
"put it inside" -- so every copy from the second onward went inside the
first, each landing raised a fresh spot, and the spots stood empty in a
row. Twelve rounds: one house on the table, eleven inside it.

**A drop on an empty spot now remembers that the spot was empty.** The step
reads "set it down on spot 1 (or the next free spot)", and a run that finds
the spot taken uses the next free one. A drop onto what already stands on a
spot is recorded as before and still combines -- the doubler adds onto its
spot on purpose, and forty saved programs do the like -- so nothing already
trained changes its meaning. Twelve rounds now: twelve houses in a row on
the table, none inside another.

**The spots keep clear of the stacks.** Three to a row going back was fine
for a few; the fourth and fifth rows stood among the stacks. The first nine
spots are where they always were; the rest fill the right of the stand,
two behind, and the wings, each measured at least half a unit from where a
stack stands, and past those the front row runs on outward, never back.

**Reshaping the table no longer takes the camera.** Only a corner actually
in hand pins it, and letting go anywhere -- off the window included -- gives
it back. Handles left out for an afternoon were the likeliest reason the
workshop stopped turning while everything else still worked.

**Marty says it once, plainly, as himself.** A demonstration's line is read
aloud by Marty or by the card, not both. Whatever a brain sends comes off
its markdown before it is shown or spoken, and the brain is told it IS
Marty, in the first person, in spoken sentences. And "make me a lion",
typed or said into Ask, is the Make button; "draw a cat" is Draw.

**The scene itself is the real answer** to a village or a zoo, and it is a
design rather than a fix: a ground you can enter like a room, where things
stand where you put them and a robot on a thing's panel is how it behaves.
Brainstormed with Ken; not yet built.

## The yard, doors with names, a finger that drags, and a rocket that landed

*Added 11 Sep. Ken: "How about the idea that when you enter a house there
is an additional door that takes you to a room for making scenes. I'm not
sure what to call it... Model world, scene maker, microworld. I wonder if
there should be a way for users to edit the label on a door. The door to
return should have an appropriate label. By the way my grandson asked me
what the crashed rocket was. Maybe it should not be so broken." Then: "go
ahead with all of these. I think yard is best name since garden may cause
an expectation of finding flowers and other plants. Another issue is when
using a touch interface my grandson didn't realize he was still holding
something and when he moved his finger over to the thing he was indeed
holding he caused the camera to rotate which was confusing."*

**The yard.** Behind every place -- the workshop, and every house -- is
open ground. The back door stands beside the tall door out; through it
your table stays indoors and the ground takes its place, ten by five and a
half, at floor level, grass underfoot. Your hand, the stacks, the robot's
desk and Mimi all come along, exactly as they do into a house, so
whatever a robot sweeps off its work spots at the end of a run, and
whatever Marty makes, lands on the grass -- a village from a house-maker,
a zoo from a Make. What you carry through the door comes too, in either
direction; what you set down out there waits while you are inside, is
saved with the world, and folds into a house with the house. The sign on
the door says Outside, and from the yard, Inside, or Back to the workshop.

**Not a room.** A room is a copy of the workshop with a desk and stacks,
the wrong furniture for a zoo; and "your table came with you" is the
app's one rule about places, so the yard keeps it by swapping the table
for the ground rather than inventing a third kind of place. A yard
entered from inside a house is that house's own; leaving the house is
done from indoors, and the tall door says so.

**Doors with names.** The tall door wears a sign saying where it leads --
Back to the workshop, Back to “Add 1” -- and pointing at any door and
typing changes what it says: a house's door carries the house's name, the
tall door's words are kept with the house. A space joins a name being
typed and is the usual click otherwise.

**A finger drags the thing in hand.** On a touch screen the hand parks and
a tap says where the thing goes; a child who has forgotten he is holding
something reaches for it where it sits, and the finger turned the camera
instead. A touch that lands on the held thing now carries it, and the
thing goes where the finger lifts; a tap on it, and a tap anywhere else,
work as they did. Measured with synthetic touch events: the camera is off
while the finger is down and back the moment it lifts.

**The rocket.** It stood for a crash: on its side, nose bent, a fin
snapped off, smoking. It stands on its fins now, leaning seven degrees on
the one that took the landing, tail scorched, and Marty says he "landed
badly". Asked what the rocket is, he tells you.

## Filling a yard: robots on the ground, helpers put away, doors you can carry

*Added 11 Sep. Ken: "I'm thinking of ways a user might populate a yard. For
example, they might take a box full of items, place them, and leave holding
the empty box. Another would be to place a nest in the yard and then give
items to the bird and then go into the yard and arrange the items on the
nest and leave with the nest. A robot should be able to do these things as
well. Also can you make a sample file with a zoo in a yard. Catching 'make'
is good but I wonder if the following could have worked better: 'I want
another unicorn' [was answered with 'Press Make and tell me']. No need for
Ruby in the yard. There should be a way to hide Dusty and Mimi (and her
copier) when not needed (and to bring them back when needed). The user
should be able to move the door (and resize it). Perhaps by picking it by
the frame."*

**A robot sets things down on the ground.** Outside, a drop on the grass
while training is a step of its own, "set it down on the ground", and a
run finds a free patch each time: a box of animals carried out and
unpacked by a robot, one per round, in a spread rather than a heap. Taught
outside and run indoors, the robot says so and stops. The box and the nest
ways of filling a yard need nothing new: a box comes through the door in
your hand, its things come out one by one, and the empty box goes back in
with you; a nest set on the grass takes the bird's deliveries, and the
pile is arranged where it lies.

**"I want another unicorn" is Make.** A wish without the verb -- I want,
can I have, give me, another, one more -- goes to Make the way "make me"
does. A question about making still goes to the brain.

**Helpers put away.** Dusty, Mimi with her machine, and Ruby each have a
switch in the more-menu, remembered in this browser; a puzzle's rules
still decide who is there at all. Ruby stays indoors when you are in the
yard: there is no thought bubble on the grass.

**Doors you can carry.** Click a door by its frame and it comes with the
pointer along the floor; click where it should stand. The arrows turn it,
+ and - make it bigger or smaller, Escape puts it back. Where the doors
stand is remembered in this browser and saved with a world.

**A zoo in the yard**, `examples/yard-zoo.world.json`: seven animals built
from solid shapes the way Marty builds them, a welcome pad by the door,
and a bare table indoors. Generated by `examples/make_yard_zoo.py`.

## What is here, a name taken off, a pad that stands up, and a painted picture

*Added 11 Sep. Ken: "Not appropriate tooltip for Dusty. Go ahead with the
open yard issues. The yard was working and now I don't see the door to the
yard any more. Add Marty to the menu for adding/removing from a yard --
maybe there should be a general way to remove anything from the workspace
-- even stacks of objects. The menu 'Dusty: put away' is fine when Marty is
in the yard but should change when he's not there. I like the idea that
Dusty can remove labels but it didn't work on a 3D model -- the whole model
was vacuumed. I think + should permit larger sizes. I think when holding a
pad the up and down arrow should tilt it up or down so a few clicks and one
can put up a background image in the yard. When asking for a drawing if the
LLM supports text-to-image then use it instead."*

**The door that vanished.** The back door hid itself in any puzzle, and a
puzzle is where the workshop reopens if that is where you left it. Now it
is a tool like Mimi or Dusty: a puzzle whose rules list its tools without
the yard has none; everything else has the door, unless you put it away.

**What is here.** One place in the more-menu, a list of boxes to tick:
Marty (his panel stays), Dusty, Mimi and her machine, Ruby, the back door,
and each of the nine stacks. Unticked, a thing is gone until it is ticked
again, and the browser remembers. A puzzle's rules still decide what is
there at all, and a demonstration brings Marty back out. The wording was
the trouble with the three buttons -- "put away" read as a place -- so the
list says what is here and what is not.

**Dusty takes a name off.** A name plate is its thing's, except to Dusty,
who can take the name alone: the model, the box, the house stays. Dusty's
tooltip says what he does now -- vacuum a thing, take a name off, remove a
part of a thought -- rather than describing Ruby.

**A pad tilts in the hand.** Up and down tilt a pad by fifteen degrees a
press, and a standing pad rides high enough that its bottom edge rests on
the ground; set down, it stays so, and the world saves it so. Six presses
and a picture stands as a backdrop in the yard. Doors go up to six times
their size.

**A painted picture.** Where the brain can paint -- OpenAI and Gemini both
make pictures from words -- Draw paints; Claude and the little brain in
Chrome keep the turtle. The key goes to its own provider and nowhere else,
exactly as it does for words, and a painter that will not (a model name
that has moved on, a busy mothership) hands the wish to the turtle with a
word about why.

**The yard grows.** A thing set down within half a pace of an edge pushes
that edge out two paces, up to a limit, never toward the stacks; the size
is the yard's own and is kept with its things. Marty is told when you are
outside, so his answers say grass rather than table.

**Still open**, and said so: robots taking things off the ground (which
thing is not something a robot can be told without a new address), and
walking or wandering behaviours for animals -- though the behaviours that
exist (moving, bouncing, following) already bind to an animal in the yard,
since the ground is the table while you are out there.

## A place keeps its own, and a robot goes out through the back door

*Added 11 Sep. Ken: "When I clicked on What is Here the menu disappeared.
The door ended up far away when I started free play -- the door
repositioning should only apply to the context (yard or workshop). I meant
other objects should have a much larger maximum size -- e.g. 3d models and
pads. When Dusty removed a label he doesn't move to remove it. Typing to
3d model while held should edit its label. Saving worlds should have
different default file names depending upon yard or workshop. Why did I
hear 'setting it down and it says so' twice while standing up a pad?
Hiding/showing items should be specific to the context. I thought a robot
could move to a yard (holding whatever is in its hand) to place things
there -- when I clicked on the door while training a robot it said to wait
for work to finish first."*

**A place keeps its own.** Where the doors stand, and what is put away,
belong to the place you are in: moved in the yard, a door is moved in the
yard, and indoors it is where it was; a stack put away indoors is out on
the grass. The list in the menu says which place it is for, and both are
remembered and saved.

**A robot goes out.** The back door is a step: shown through it while
training, a robot goes out to the yard with whatever it holds -- and you
with it -- sets things down on the grass, and comes back in through the
same door. The run follows it there and back.

**Smaller things.** The menu stays open for What is here. Models and pads
grow to twelve times, in quarter steps to twice and halves after. Dusty
goes over to a name plate to take the name off and comes home. Typing
while holding a model names it. The saved file is yard.world.json when
saved from the yard. The tilt line is said in full once per hold and
briefly after; the reader keeps one line waiting, which is how the tail
of it was heard twice.

## The camera follows onto the grass, room for the whole thing, and the helpers behind the yard

*Added 11 Sep. Ken: "The camera doesn't follow a robot when placing things
on a yard. I moved the door to the yard in the workshop but when I loaded a
saved world the door went back to where it was. And yet when I entered the
yard the door was back to the default place. Screenshot shows how when the
robot places 3d objects in the yard they overlap -- they should only be
placed on spaces with enough room for the object. Instead of putting Marty,
Dusty and Mimi on the yard they should be behind the yard as they are in
the workshop."*

**The camera outside follows the subject.** Indoors the smart camera keeps
the desk and the work spots in the picture while it follows the claw; on
the grass that pulled it back until a robot setting a house down was a
speck. Outside, the work area is the ground, and it follows what the claw
carries. A robot's own walk out through the door no longer starts a camera
glide of its own that the follow would fight.

**Room for the whole thing.** A free spot was found by a thing's width
before the size it wears, so two houses shown at twice hand size were set
as if small and stood through each other. The footprint now includes the
scale, the search rings are sized to the thing, and there are enough of
them for a yard. The end-of-run sweep uses the same measure.

**The helpers stand behind the yard.** The ground begins past Marty,
Dusty and Mimi, who then stand between the stacks and the grass as they
stand beside the table. The near edge never grows. The zoo sample moved
with it.

**Doors in a saved world.** A world file carried where its doors stood
even when nobody had moved them, so loading one put a moved door back. A
world says where its doors stand only once somebody has moved one. (The
yard door standing in its own place outside is by design: each place
keeps its own.)

## A ground of its own, a reshaped yard, a saved list, and a robot that walks home

*Added 11 Sep. Ken: "I think a user should be able to make a pad as large
as the yard so they can have a different kind of ground. Is the show/hide
of elements setting saved when a world is saved? I think it should. The
reshape table button should change to reshape yard if the yard is visible.
After a robot placed something in the yard as the last step of its
training we should see it walk back to work and not jump back there."*

**A ground of its own.** The holding card, with a pad in hand, has "As
big as the ground": the pad is sized to whatever you stand on -- the yard,
or the table -- and laid squarely over it. What is dropped on it rides on
it, as on a pitch, so a pad with a picture is a beach, a floor, a map. A
pad's width and height in tablets go to forty-eight.

**What is here travels.** A world saved with anything put away carries
both lists, indoors and outside, and a world opened with them puts those
things away here too.

**Reshape yard.** The button says which it is, and the corner handles
stretch the yard as they stretch the table: as wide as the limit allows,
the far edge out to it, the near edge fixed where the helpers stand. The
size is kept with the yard.

**The robot walks home.** A lesson that ended out on the grass, or at the
copier, left the robot there and snapped it home. It walks, at every
speed but Instant.

## Wandering: a behaviour for animals

*Added 11 Sep. Ken: "go ahead with the wandering behaviors for animals".*

**Nothing here is about wandering.** The Wanderer is handed [a bird to my
thing, an across step, an away step, a die of three, a -2, a x1/25]. Each
round, on each step: a copy of the die lands on the step's number (1, 2 or
3), a copy of the -2 lands on it (-1, 0 or 1), a copy of the x1/25 lands
on it (a small step, or none), and a copy of the step goes to the bird.
The same four gestures a child makes by hand -- a die re-rolls a number,
a number is added, a number is multiplied, a bird carries a message -- and
an animal wanders. Hold the die and type 5 and it wanders further one way
than the other, which is a question worth asking a child.

**Where it lives.** `examples/behaviours/wandering.world.json` lays it out
in the open with a star to drift; the shelf (`library.world.json`) has it
as its sixteenth gadget; and the zoo has one on the grass, ready to drop
on an animal. Measured: bound to the flamingo and switched on, the
flamingo moves; in the open world the star drifts round by round and, at
the table's edge, says so and keeps rolling until a roll takes it away.

**Slow by the round, quick on a panel.** Sixteen steps a round means a
walk to Mimi and back six times, so in the open the star drifts at a
robot's pace even at Instant; folded into its panel, as a gadget is, the
rounds run offstage and it drifts at a frame's pace.

## Contagion through the root, drop hints, how far Marty goes, and a manual that agrees with itself

*Added 12 Sep. Ken, on Astra's review: "go ahead with contagion rule and
manual update. Happy to experiment with preview and then decide whether to
keep it. I like the idea of a setting to remove Marty's restriction on
creating programs for the user. And as you suggest the default should be
the current setting. Consistent wording is important."*

**The root keeps the approximation.** The root branch of `applyOp`
returned before the contagion rule could touch it, so a square root of an
approximate 4 came out an exact 2 while raising the same 4 to a half kept
the mark. It applies the rule itself now, and a check walks every
operation with an approximate input and expects the mark on every answer
-- and still no mark on the root of an exact 4.

**Drop hints.** While you carry something, the tooltip's first line says
what letting go here will do, in the drop's own readings: rides on this,
joins this on the right, goes inside the room, × 5 on the number, picks
letter 2, re-rolls it, is a lesson for the robot. A switch in the more-menu
(on, for the experiment). Astra's point was that a newcomer should be able
to predict a gesture; the wiggle said where, not what.

**How far Marty goes.** A setting in How Marty thinks, per person: hints
and demonstrations only (the default, as before), or he may plan and write
programs when asked -- as short numbered steps in the workshop's own
gestures, saying the idea first so the visitor can stop him and build it
themselves, and never claiming to have built anything. Astra argued the
boundary should be the learner's chosen level of help rather than "toys
yes, programs no"; Ken agreed with the current setting as the default.

**A manual that agrees with itself.** Two contradictions Astra found are
gone: the pads section said a number dropped on a pad shifts a letter (it
rides, measured), and the pen paragraph said strokes cannot be picked up
or saved while a later one explained that a trail is a thing (it is). The
history moved here. This file's opening no longer says "designed, not
built", and the claim that copyable documentation "cannot rot" now says
what is true: it is hard to leave rotten. And the manual gained a first
project -- a robot that counts, eight steps, meeting the lesson, the
thought and Ruby -- which the suite replays step for step.

## Computing words, commentary, a question that finds its thing, and a bird that is seen to fly

*Added 12 Sep. Ken: "I'm worried older learners and teachers won't know
how to get Marty to use computing words. Maybe a switch in Marty's
interface? When I entered the wandering panel when the robot dropped
something on the bird I didn't see it fly away and return. Redo the
wandering behavior to use the turtle commands instead. When the user is
watching a robot work let's add an option to Marty to provide a high-level
commentary. Ideally like good comments and not just a description of the
basic events. Also if a user asks about a robot, house, or panel (either
that they are holding or by label (or pad text)) Marty suggests running it
with commentary. The current response is inadequate."*

**Words.** A switch in How Marty thinks, per person: the workshop's words,
or computing words too. With it on, the first time a workshop word comes
up in an answer the programmer's word stands beside it in brackets -- a
thought (its condition, a pattern), a lesson (a program), a team (a case
analysis), a bird (a message), a nest (a mailbox), a house (a process),
Ruby (generalising), Mimi (cloning). One vocabulary for everyone, and a
second laid beside it for those who ask.

**Why the answer was inadequate.** Marty was told "copy what is in hole 4
of what it was given" without being told what hole 4 held, and so had to
guess. He is now told the work box hole by hole -- "[a bird to my thing |
[move | forward | 1/25] | [move | yaw | 0] | a die (1 to 3) | the number
-2 | the number badged × 30]" -- and every step names what it touches:
"copy what is in hole 3 (a die (1 to 3))". Purpose follows from that.

**A question finds its thing.** Asked about a robot, a behaviour or a
house -- the one in the hand, or one on the table named by its label, its
name or its words -- Marty answers, and a button appears under the answer:
run it with commentary.

**Commentary.** A box to tick in How Marty thinks: while a robot works,
Marty says what it is trying to achieve and the trick it uses -- as a good
comment would, purpose first, never a transcript -- at the start of a run,
when it stops (and why), and when a behaviour is switched on. It needs a
brain; the phrasebook stays quiet.

**The bird is seen to fly.** A panel's rounds run offstage, and the
miniature only mimes the walk to each hole afterwards. Two things stood in
the way. The mime's list was replaced by every round, and a ticker runs a
round every turn, so a ten-step round never got past its first few steps
(the older gadgets have two to four); a mime in progress now finishes before
the next round's list takes its turn. And a drop on the bird is now a flight
in that mime: a stand-in bird goes out to the thing she is addressed to and
comes back, in world space, while the bird in the hole hides -- the box is
redrawn each round, so the bird's own parent cannot be trusted for the
length of a flight.

**Wandering, in the turtle's words.** The Wanderer now sends [move | yaw |
a] and [move | forward | 1/25]: a die of three, a -2 and a ×30 land on the
turn in turn (−30, 0 or 30 degrees), a copy of the turn goes to the bird,
then a copy of the step -- so an animal faces where it goes.

## The examples after Astra: a gap to find, claims to investigate, experiments first, a ship that repairs

*Added 12 Sep. Ken: "go ahead and make all those changes. regarding
infinity exercises have you seen https://toontalk.com/Tools/Infinity/Doc/
index.htm and its links (including teacher guidance and the worksheets)?"*

**Ken's own worksheets first.** The guidance lives in Word comments in the
eight cardinality worksheets. Two of them settle two of Astra's points in
Ken's own words: the Activity 6 note says the fraction robot "only does so
if the denominator is less than the numerator, so it will never produce
1", and the reciprocal of 1 is 1; the Activity 3 note sets 1, 1, 1, ...
against 1, 2, 3, ... -- the same cardinality as sequences, {1} against
{1, 2, 3, ...} as sets -- and says that a program for a sequence without
duplicates is a one-to-one mapping. The edits below echo those.

**Zeno.** A fourth pad, The gap: build the distance still to go, put it on
one pan of a scale and the last delivery on the other, and say what is
true every round without fail -- an invariant, found rather than watched.
The Why pad keeps two claims apart: no delivery ever closes the gap, and
the whole endless series adds up to exactly 1.

**The activities.** Activity 3 asks for a robot that gives back 5 whatever
it is handed -- every position gets a partner, the set of values is {5},
a sequence and its set are two things -- on the pad, on the sheet, and in
Marty's brief. Activity 4 says the walk by denominator COVERS every
fraction, some more than once, and asks whether repeats make the count
wrong or only untidy (the original's No Copies robot, which tests for
lowest terms, is named). Activity 6's last nest is labelled "every positive
rational?", a claim to investigate; the pad says why 1 never arrives and
asks where it would go in. Activity 7 no longer calls three nests filling
at the same rate "the whole argument": the same rate shows the pairing,
and reversibility is the argument.

**Experiments before explanations.** Melody, the airplane and wandering
lay their pads out as run it, change it, then what it is. The airplane
gained Is it a circle?: twelve strides with a corner after every two, and
what halving both the stride and the turn does -- approximation by a
repeated process, on the table.

**The ship repairs.** Each puzzle stands the ship at a stage: leaning
seven degrees at first, straighter from puzzle 10, upright from 20, a
light in the porthole from 25, the nose beacon lit from 30, and Marty
says so on arriving at each. The constructions have a consequence you
can see behind the table.

**Built by demonstration.** Two of the examples Astra picked are now
trained in the suite through the lesson path, step by step, and run:
Zeno's halver and totaller (five deliveries, a total of 31/32) and
Melody's Singer (ten steps, eight notes off the nest). That is the
beginning of an answer to "how readily can a learner construct the same
programs through demonstration": these two can be.

## The house stack, a robot that takes out a panel, and a crocodile seen in its hole

*Added 12 Sep. Ken: "I wonder if the tick to show the 'room stack' should
refer to rooms as houses since that's what they look like. Tooltip too.
When training a robot to obtain the panel of an object it says to leave
the thought bubble first -- why can't the panel just float to a work area
of the robot? I want to train a robot that will give an object a behavior
by obtaining the panel (or a copy) and adding to another panel. Screenshot
1 shows that a 3d object just looks like its label when in a box;
screenshot 2 shows when zoomed and rotated nothing appears in hole 2."*

**The house stack.** The stack's label and tooltip say house now; the
manual's section keeps its name.

**A panel is a step.** In a lesson, ⚙ with something in the claw takes
out that thing's panel onto a free work spot, where the robot can take it
and drop it on another panel -- a panel dropped on a panel nests whole,
and the behaviour inside works on that thing. The step reads "take out
the panel of what it holds, onto a work spot". Measured: a robot given
[the wandering behaviour, a crocodile] takes out both panels and drops one
on the other, and the crocodile's panel holds the behaviour. (Dropping the
behaviour pad itself on the thing binds it too, in one step; the panel
route is for grouping behaviours inside a thing's own panel.) Mimi cannot
copy a panel; copy the behaviour pad instead.

**The crocodile in its hole.** Measured: the model was there, shrunk to a
third, and its name plate was scaled back up to stay readable -- so the
plate covered the model face-on, and turned edge-on left a model too small
to notice. In a hole a model now shows itself and not its plate; the
tooltip still names it, and the plate is back when it comes out.

## The crocodile on the rim, and a panel dropped in a hole

*Added 12 Sep. Ken: "crocodile in hole still not fixed. I still couldn't
train a robot to put a behavior on the crocodile. I was able to obtain
both panels but when I picked up one I couldn't put it back or onto
another platform. And when I dropped the panel in a box hole it
disappeared. And I couldn't drop a panel in a box hole even when not
training."*

**The crocodile.** Measured: the model was shrunk to a third and set on
the pocket FLOOR, 0.05 below the rim -- and the crocodile is 0.017 tall,
so from every angle but straight down the pocket wall hid it. A model in
a hole now rests on the rim, as boxes, sounds and nests already did.
Measured: its underside is at the rim; the screenshot shows it.

**Dropping the panel on the crocodile.** Reproduced with real pointer
events in the lesson: the wandering behaviour's panel, dropped on the
crocodile in its hole, DID bind the behaviour to the crocodile -- and
then the tray went to the user's bench, out of the robot's area and out
of the lesson's camera. That is what "disappeared" was. In a lesson or a
run the tray now lands on a free work spot; by hand it goes back beside
its thing. The lesson also records "put it in hole 2", so the trained
robot gives the crocodile the behaviour by that step alone -- no second
panel needed.

**Dropping a panel in an empty hole.** By hand it was refused with a
message about the bench; in a lesson it became a step that ABORTED,
which ended the lesson with the tray in your hand. Now: by hand, "A panel
does not go in a hole -- it goes back beside its thing. Put the thing
itself in, or drop the panel on a thing to give it the behaviour inside";
in a lesson the same words, and no step is recorded. By hand, the panel
dropped on a thing sitting in a hole binds now, the same as on the table
(it used to be refused there too).

**Putting the panel back.** With real clicks, at normal speed and with
the smart camera on, the tray taken off a work spot went back onto that
spot, onto another, and onto the other panel (nesting whole) every time;
this part is not reproduced. If it happens again, a screenshot of the
moment would help.

**Found on the way.** A pad dropped on its own open panel went INSIDE
its own panel -- a loop that every save, undo and copy walked until the
stack ran out. Refused now: "That is its own panel -- a thing does not go
inside itself."

## A lesson that survived a binding, the knob as a step, and a panel on the floor of a panel

*Added 12 Sep. Ken, with three screenshots and the robot he saved: "after
picking up the crocodile's panel I couldn't set it down on a work area.
When I picked up a fresh 2-hole box and typed 3 it worked fine but the
narration said it was a 2 hole box. Dropping the wandering panel on the
crocodile's panel worked but is displaced to the side away from the
panel. I'm training but the 'run what is learned' button is available
instead of the stop training button. I think it was because at the end I
clicked on the gold knob to return the panel to the crocodile. Attaching
the robot but it doesn't have the knob click or the rest."*

**One cause for three of them.** Measured, frame by frame: the moment a
panel dropped on another panel bound its behaviour, the mode went from
"training" to "world" -- badge "your workshop", Run button up, the thought
bubble still on screen (screenshot 3). Binding rebuilt the panel's live
world from its record, and to throw the old one away it called the
routine that stashes a world's mode, queue and hands -- one half of a
push, run on the OUTER world, which was the lesson. So the lesson ended
silently at that step: the knob click and everything after it were never
recorded (the saved robot stops at "put on spot 1"), and a panel picked up
afterwards was in Ken's own hand, which cannot go on a work spot
(screenshot 1). The old world root also stayed mounted, so a bound panel
showed its things twice -- the stray little robot beside the nested panel
in screenshot 2. The discard is a discard now; the lesson goes on.

**The knob is a step.** In a lesson, the knob on a panel standing on a
work spot records "put away the panel on spot N, back inside its thing",
and the robot does it in a run, wherever the thing is by then. A panel
with work still going inside is kept hidden on the bench, as the knob does
by hand. Measured: Ken's lesson, taught by hooks and then run on a fresh
box, ends with the wandering behaviour inside the crocodile's panel.

**On the floor of the panel.** Inside a pushed world "the bench" routed to
that world's work spots, whose points are the outer desk's -- a nested
panel sat 0.95 to the left of its host's centre, past the tray's edge. A
panel's contents are centred on its floor now.

**The box.** Typing a digit on a held box makes a new box; the words read
the old one's count. They say the count typed.

## A way back from a panel entered in the yard, and Ruby on the grass

*Added 12 Sep. Ken: "I can't go back inside after entering a panel while
in the yard." And: "I think I was wrong about Ruby since you can train a
robot while in the yard so it should say 'Ruby (inside only)'."*

**The door.** Measured: walking into a panel from the grass, the tall exit
door was hidden -- it was switched off whenever the yard was open, because
the yard itself has no exit door (its way back is the back door). Only the
yard is without one now; a house or panel entered from the grass shows the
door, its sign reads "Back to the yard", and it leads there.

**Ruby.** She stayed indoors when the yard was open ("no need for her in
the yard"). A robot can be trained on the grass, and a thought is where
she works, so she comes out too, and the list of what is here calls her plain "Ruby".

## Who ran into whom, a scene's own referee, and Space Invaders with its back readable

*Added 12 Sep. Ken: "Let's postpone the broker house. Please add the 3
enrichments. One thing I'd like to address is that the anima-gadgets of
original ToonTalk were much easier to see... How can we make a space
invader game that when the panel is obtained is readable as a collection
of gadgets and that gadgets are easy to inspect as in the attached
photos? Try to make a space invader game example and see how inspectable
you can make it."*

**The touch reading grew.** `[listen | touch | bird]` hands over four
holes now: the bird to what was run into, the side, the NAME of the thing
(its name, or what kind of thing it is), and which way it is, an
`[across | away]` box of length one from your middle to the other's. The
name is the original's "Touching Who?" matched by an erased picture, as a
word in a hole: a robot trained on "bullet" fires for bullets, and Ruby
loosens it. The normal is what a bounce that is not square-on needs. A
reading saved with two holes grows the other two on the way in, and a
robot's thought the two wildcards, so every bounce trained before still
matches (the pong ball's thoughts, measured).

**A scene's own listener.** `[listen | touches | bird]` sent to a pad with
things riding on it announces every pair of riders that starts touching,
once, as `[bird | name | bird | name | normal]`: what met what, with no
behaviour on either. That is the house every object was going to report
to, done by the workshop itself and costing nothing until asked; the
game's referee card keeps the score with it.

**Three the original's pictures had.** `[set | shown | no]` and `yes`;
`[vanish]`, gone for good the way a vacuumed thing goes (nothing keeps it
-- Dusty's bag is the undo for a gesture of yours); and `[drop | thing |
[across | away]]`, the thing in the message set down beside my thing, on
its field, arriving with its own behaviours switched on. That is how the
ship fires: a copy of the bullet kept in its work box, dropped in the
message.

**Space Invaders (examples/games).** Eight invaders, a ship, a dark field,
a score. Every picture is a pad with its behaviours on its BACK as cards
whose faces are sentences -- "I explode when a bullet hits me: a bang, and
I vanish." -- the way the original's Space Behaviours laid its gadgets
out. Point at an invader and press the gear: its panel comes out with the
two cards standing on it, magnified to read; Enter on the panel looks
straight down at it, framed like a page. Point at a card there and press
the gear again: the card's own panel comes out beside, with its robot at
the box it works on, and Enter there looks from the front. The knob folds
each one home. Measured end to end: SPACE starts ten parts, the arrows
steer, the up arrow fires, the bullet flies, meets an invader, both
vanish, and the score reads 1.

**What had to change to make it readable.** A panel dropped on a panel
used to nest as a miniature tray -- bird, knob and plaque and all; now the
tray folds into its card first and the card alone goes in. A panel's
contents are measured by what can be SEEN (a folded tray is invisible and
was still solid to the fit, which put the cards at the back of the floor)
and a page of cards is magnified to fill its floor; a card's own back,
with a robot on it, keeps toy scale so the robot never looms. The gear
works on what the pointer is over, not only on what is held, and in an
Enter view the flip goes on into the card's panel.

**A hang, found on the way.** Checking the waiters serialised any open
panel in a dozing robot's work box, which swapped worlds and rebuilt the
very Set being iterated -- for ever. The ship's fire card, dozing on the
keyboard with the switched-on bullet in its box, hung the whole workshop
at its first turn. The loop walks a snapshot now, and a gadget sitting in
a hole is a thing to work on, not a part to switch on.

## The examples in folders, with a picture on every name

*Added 13 Sep. Ken: "Let's organize the examples that are at the top-level
of the examples folder by moving them to existing or new subfolders. And
pong, airplane, and maybe others in behaviors should move. Add emojis when
appropriate to all the examples' filenames."*

**One folder per subject.** Nothing stands loose at the top of `examples/`
any more: the ports of Ken's own programs are in `numbers/` (🔀 swap, ❗
factorial, 🐇 Fibonacci twice, and 🌡️ the gauge) and `lists/` (🔢 n-to-1,
🔗 append, 🔁 reverse, with their converter); the sentence factory and the
grammar are `words/`; Sally's account, the bank and the live account are
`accounts/`; the zoo is `yard/`. Out of `behaviours/` went the three Pongs
(to `games/`, beside 👾 Space Invaders), the airplane's flight (to
`models/`, beside the airplane itself) and Zeno's postman (to `infinity/`).
What stays in `behaviours/` is the shelf and the single behaviours it is
made of, and the turtles.

**A picture on every name.** Every world and thing file is named with an
emoji and a space before its name -- 🏓 pong, 🦁 zoo, 📮 zeno, ✈️
airplane-flight, ⌨️ keys -- so a folder listing reads at a glance. The
puzzles keep their plain `p1`..`p34`: those are the names the app loads
them by. The server decodes the encoded paths, the activity sheets and the
suite fetch the new names, the goldens are keyed by them, and every
generator writes its world next to itself; all forty-six were run and every
world came out byte for byte the same.

**Found on the way.** Yesterday's fold-on-nest (a panel dropped on a panel
goes in as its card) broke "a fold keeps nested work alive": a WORKING
tray was hidden on the table instead of riding inside the group, so
folding the group serialised it and the turtle's letterbox left the scene.
A working tray goes in whole now, hidden, as before; only an idle one is
written into its card. A panel brought out to be read comes out onto the
table wherever its tray was riding, and a fold looks for a part's work
wherever its tray is.

## A team standing by, a mime by the right body, and closeups that nest

*Added 13 Sep. Ken, with a picture of the explode card's back in Space
Invaders: "the tiny robot is 'dancing' while the other looks too big. As
a waiting team the size difference should be much less between the larger
first robot and the rest. Maybe the bird is a bit too big. Notice that the
door enters into the frame. If one has clicked enter for a closeup of a
panel then when one extracts a subpanel it should be shown closeup too. I
think while inspecting it is awkward to enter and leave closeup mode.
Enter while holding should also switch to closeup mode."*

**Who was dancing.** On a card's back the member that recognised the work
takes the full-size body at the desk, and the leader parks in the queue.
The queue stood at toy size, a ninth of the performer's height -- and the
round's mime, the walk from hole to hole, moved the LEADER's node, not the
body that had done the round. So the big robot stood idle while a tiny one
walked its round for it. A team standing by is half-size now, and the mime
moves whoever performed.

**The tray.** The perch bird is a little smaller, and the door stands
inside the front rail instead of through it.

**Closeups nest.** In a closeup of a panel, the gear over a card takes the
closeup on into the card's panel, however that panel comes out -- new,
shown again, or brought out from riding inside the group. The knob, or
Escape, comes back to the panel it stands on, and only the last Escape
reaches the workshop. Enter works with something in the hand too: the
thing under the pointer, or failing that the thing held, fills the screen
where it is; Shift+Enter is the new line on a pad you are typing on.

## The thought stays in the picture, and Zeno's postman in seconds

*Added 13 Sep. From the suite: "the camera shows the thought" failed
headless (red-view on=false, d=4.59), and the same way against the app of
12 Sep, so not the last two days' changes -- find whether the app or the
check drifted. And Zeno's postman took more than twenty minutes on its own.*

**Whose view.** Two occasions arrive in the same instant when a robot
refuses a box: red parts appear in the thought, which asks the camera for
the thought; and the refusal names Ruby ("wake Ruby and click a red part"),
which since 4 Sep asks it to pull back until she is in view. The later ask
replaced the earlier, and the fit of the table and Ruby left the thought --
the very red parts the words point at -- above the top of the screen. The
check had passed only on 4 Sep, and only when another check (Ruby's view,
the narration) ran before it and left the camera where Ruby's home was
already on screen, so the mention never fired; on its own it has failed
since mentions came to say(). A mention now keeps a view already asked
for: if that view holds what was named it stands as it is; if not, the fit
holds the thought, the robot's work area and the named thing together.
(Pulling the thought view straight back until Ruby came in put the camera
eight units off, the thought too small to read.) Ruby's close look on the
thought is left alone. Headless the red view now lands 5.9 from the
thought with the thought on screen, and Ken's case -- the run that stops
on red parts -- the same.

**Zeno's postman in seconds.** The check pulled the halver's lever, waited,
then the totaller's, then ran 2,200 frames. At Instant a lever pull is a
whole 1.2-second slice of room work and every frame eighty halver rounds,
so the total became a fraction of tens of thousands of digits and the
frames took twenty minutes, each slower than the last as the numbers grew.
Not the pile: the totaller drains it within its first turn, and it stays
at nothing. Both levers first, the totaller's before the halver's, and the
invariant is read off the first eight deliveries -- it holds for every
single one, so eight are as good as a hundred thousand. The world itself
is not capped: a dropped letter would break the very exactness it teaches.

## A note on every robot, one thought at the desk, and no birds from nowhere

*Added 13 Sep. Ken: "In Pong gadgets world when I move the paddle I see a
tiny bird or two flying across the table where it isn't clear where it
starts or ends. Birds are ok if their paths make sense but I couldn't
figure it out. Let's add a way in the trained actions area to write a
comment associated with that robot that is persistent. All the examples
should have comments like this. The trained actions should display the
steps and comment of any robot held by the user." And, testing the
sentence generator: "2 thought bubbles and only one should be shown."*

**Birds from nowhere.** A behaviour switched on without its panel ever
being brought out works in a hidden tray, and the bat's follower stood
invisible in the middle of the table. Every round it performed -- a bird's
flight from the tray to the bat -- set off from there. Measured on the old
build: the follower's tray hidden at (0.62, 1.85), a ghost bird in flight
in 16 of 60 samples while the pointer moved, and a round to perform in all
60. A panel out of sight performs nothing now: no round is recorded for a
hidden tray, and a flight cut short by a fold ends at once. The new build:
no ghost in 60 samples, and the bat following as before.

**One thought at the desk.** A team's members standing by wore their own
small bubbles, and once the standby size went from a ninth to a half those
stood at four fifths of full size beside the performer's thought -- three
thoughts over one desk. And when a member took the floor, the leader
stepping back shrank to toy size -- a ninth -- and got its thought back
over its head: measured on Factorial at the desk, the leader at 0.24 with
a bubble while "multiply" worked. The thought on show is the performer's;
the members' are read on the card, a member at a time; whoever steps back
stands at the standby size, and a queue on the bench keeps its bubbles.

**A note on every robot.** The Trained actions card has a line under the
robot's thought for a note: click it and write what the robot is for, in
your own words. The note is the robot's -- it goes into a saved world, a
saved thing, the library and every copy -- and Marty reads it back when
asked what a robot does. The card now reads the robot in your hand: pick
one up off the table, out of a house or in from a file, and its steps and
its note are on the card, a member at a time if it leads a team; put it
down and the card returns to the desk. Every robot the examples ship
carries a note -- 396 of 408; the twelve without are the blank robots the
puzzles hand the player to train -- written into the generators, so a
rebuild keeps them, and all seventy-nine files came out byte for byte the
same but for the notes. The judges' members say which kind of wrong answer
each sends back. A key typed into the note is not a key press in the
workshop: no keyboard nest hears it.

## Out of a team, a little robot; a game that fits the yard

*Added 13 Sep. Ken: "'Run what it learned' is a good label after finishing
training a robot. But in other circumstances it should just say something
like 'start the robot'. I took a robot out from the grammar team and it
became huge. When I move the cursor over the robots in the team they shrink
to a smaller size before I click on them to pick one up. Picking up a
second team member ended up a normal size on the desk. Robot tooltips
should include the comment. After taking the space invader's game to the
yard and clicking to make it as big as the yard the game elements didn't
scale along with the game. And it is hard to drop it so it completely
covers the yard. And it wiggles when I move the mouse over it."*

**The button.** "Run what it learned" is right on the way out of a lesson.
A robot that arrived trained -- from a file, a house, a team -- has nothing
you just taught it, and its button says "Start the robot". A lesson that
recorded steps marks the robot, and the label follows.

**Sizes at the desk.** Three faults, one cause: a robot's `mini` flag, which
takeTheFloor sets on the leader while a member has the floor and nothing
unsets when the desk comes back. Entering the grammar house after a run,
the leader stood at 0.24 behind members at 0.5; the pointer's wiggle read
the flag and shrank a standby member to toy size before it was clicked; and
a member taken out of the team kept whatever size it had -- the performer
at 1.0 ("huge"), a standby at 0.5 ("a normal size") -- into the hand and
onto the table. Now a team at the desk stands whoever is performing, flags
or no flags; the wiggle keeps a standby at doll size; and the one taken out
is a little robot again, at toy size with its own thought over it, and the
leader takes the desk back if the leaver was performing. Measured in the
grammar house: leader 1.0, standby 0.5 before and after a hover, the two
taken out at 0.24 with bubbles.

**The tooltip** over a robot carries its note, under its condition.

**As big as the yard, riders and all.** Riders scale with a field's SIZE, not
with its stated width, and the fit button set the width -- so Space
Invaders fitted to the yard kept its ship and invaders table-sized. A field
with riders is now fitted by size (9.19 for the yard) and its depth by
shape, and the riders come with it (0.75 to 6.89). A pad the size of the
ground lands centred however it is dropped, and does not stir under the
pointer. The riders' speeds are still in table units, so the invaders march
slowly across a yard-sized field -- an open item.

## A narrated run waits for its narrator, and a ticker inside a thing keeps time

*Added 13 Sep. Ken, testing Marty's commentary with a robot that folds the
wandering behaviour into a crocodile and gives the crocodile to the bird:
"I think if the user wants narration the speed of the robot should be
ignored and it should match the narration instead. When I ran the crocodile
it did wander but the app became very slow. Clicking to change the speed
had the blank menu for many seconds."*

**The narrator.** With commentary on, Marty's opening line took seconds to
arrive and the robot was done before he had said a word. A run with
commentary now starts when his line is on the card and, with his voice on,
spoken; Stop during the wait still stops it. The closing line comes when
the run stops, as before.

**The ticker inside.** The card the robot folds into the crocodile is a
panel inside a panel, and the inner search that lets a house work through
its own houses -- revisiting one it has already run this turn, so a
pipeline does not stall mid-round -- treated the card the same way. A panel
is a ticker: it never goes quiet, so "revisit freely" was fifty rounds a
turn, a hundred a frame. Measured with the crocodile wandering: 690 ms a
frame, 306 turns of room work in three frames, the counts of things, trays,
robots and birds all flat. A panel inside gets one turn per parent turn,
like every ticker; the free revisits are for houses, which go quiet when
their mail is answered. Now 24 ms a frame, two rounds a frame, and the
crocodile wanders and turns as before. Ken's robot lives on in the suite as
`tests/give-behavior-robot.thing.json`.

## Commentary for every step, a notebook that moves, and Marty as a partner

*Added 13 Sep. Ken: "I think when Marty is asked to give commentary it
should be for every step of the robot's actions. And the robot should wait
until Marty is finished describing the step before moving on. The user
should be able to pick up his/her notebook and move it or resize it. They
can even vacuum it up temporarily or move it to the yard. I wonder if a
third Marty help mode could be to HELP plan and create programs. It tries
to engage the user in the plan by asking questions. It should try to
involve the user in the planning and training process but still ensure
there is progress if the user isn't able to move forward. (By the way,
'write programs' -- write isn't a good word here and elsewhere.) The arrow
keys didn't work for the space invaders game when it was full size on the
yard."*

**Every step, and the robot waits.** The sequencer can now HOLD a step: an
item whose hold() says when the world may go on, honoured at every speed,
Instant included. With commentary on, a round asks Marty once for one line
per step -- what it does and why it matters here -- and before each step
the line is said and the robot waits: until his voice has finished, or a
reading pace without it (under a second and a half for a short line, seven
at most). Whatever he does not cover, the step says itself, so a workshop
without a brain still narrates. Stop ends the wait. Measured on the
Factorial team at 1x with no brain: the first line on the card at once,
and the run four steps in after eight seconds where it used to be over.

**Your notebook comes with you.** It was furniture -- fixed to the desk,
refused by the hand, by Dusty and by resizing. Now it is picked up like
anything else, set down where you like (out on the grass too), resized in
the hand with + and −, and vacuumed by Dusty, who gives it back. Its place
and size are remembered with its pages, and the search for it looks
everywhere it can be: the table, your hand, Dusty's bag, the grass while
you are in, the table while you are out -- a notebook that could travel
was otherwise created afresh, a second one from the same pages, whenever
the table alone was looked at. Loading a world empties Dusty's bag, as it
always did; the notebook is rebuilt from its pages where it was last set
down. Measured: moved to (−1.2, 2.19) at 1.25, and back there after a
reload; one notebook throughout.

**A partner, not an author.** The Help setting has a third choice: *plans
and builds a program together with you*. In it Marty asks one question at
a time about what the program should do, says the plan in plain sentences
and checks it, hands over one next move at a time in the workshop's own
gestures and watches the table for it to be done, and when the visitor is
stuck -- says so, or two replies bring no progress -- does the next step
himself, a demonstration or a Make, and hands the move after it back. The
middle setting says "build", not "write", and so does everything else:
nobody writes programs here.

**The arrow keys in the yard.** The keyboard nest ignored every key while
any control had the focus -- the guard added with the robot's note -- and
the Speed menu keeps the focus after use, so the ship stood still. Only a
text field keeps a key now. The moves themselves were already in the
field's own units: five presses took the ship nearly half the yard.

## A robot that teaches a robot

*Added 13 Sep. Ken, after a brainstorm on meta-programming: ToonTalk
Reborn's first tour has a robot pick up a fresh robot, give it a number,
start its training, do two gestures, stop and name it "Add 1" -- "so it
should be possible for a robot to give an untrained robot a box and then
train it. Maybe the API won't need an extension?" And: "the meta robot
should be able to use text-to-speech like in ToonTalk Reborn. Of course
this could be a general capability of text pads."*

**Reborn's way.** Reborn's robot.js records, in a robot being trained, a
"start training" step when it starts another robot's training, a "train"
step carrying each step the other robot records while that lasts, and
"stop training" -- two levels only, by a comment's own admission. The
workshop does the same with its own gestures and nothing new to give a
robot. In a lesson the claw takes a box and is dropped on a little robot
among the robot's things: that is the step *teach*. The pupil steps up to
a desk of its own beside the teacher (a stand aside, as a dozing robot
takes), the box on its desk; the thought bubble, the card and the claw are
the pupil's, and everything done next is recorded into the pupil as its own
steps and into the teacher as *taught* steps carrying them -- Ruby's
loosening of the pupil's thought included, as *taught: loosen*. "Stop
teaching it" (the exit button, renamed while teaching) ends the pupil's
lesson with *endTeach*, and the teacher's own goes on. A robot may teach a
robot, not a robot that teaches a robot.

**The dream teaches nobody.** Leaving the teacher's bubble rewinds the
world, and the pupil rides the snapshot by reference, so it came back into
the box still trained; now every pupil taught in a dream is un-taught on
the way out, its desk and the box it was given taken away, and it lands in
its hole a little robot again. Measured: after the lesson the teacher has
nine steps (take, read aloud, put, take, teach, taught: take a new number,
taught: drop it on hole 1, taught: loosen, and that is its lesson), the
pupil is back in hole 2 with no steps and the box reads 1.

**Run, it teaches for real.** *teach* walks the claw to the pupil and drops
the box; the pupil steps up; each *taught* step is performed by the pupil
in front of you and added to its lesson; the loosening is Ruby's flight to
the pupil's thought; *endTeach* leaves the pupil trained at its desk with
its box, and the teacher takes the middle desk back. The teacher's thought
no longer fits its emptied box, so it runs once. Measured on the example:
the pupil aside with two steps, its thought loosened to any number, its box
reading 2; clicked and started, it counts to 5 in three rounds. Robots at
desks aside are saved with what is on their desks, waiting or taught.

**Pads speak.** A pad reads its own words aloud in the workshop's voice:
the Read button on the held card does it now whenever pressed; in a lesson
Read is the step *read aloud what it holds*, and the robot waits for its
own words; and [speak] (or [say]) given to a pad's bird has it speak. The
waits count on the sequencer's own clock and hold only while the engine is
really speaking, with a cap of a dozen seconds, so a silent engine -- a
headless browser queues what it will never say -- holds nothing.

**The example.** `examples/meta/🎓 teacher`: a robot whose box holds a pad,
a little robot, a box with a 1 and another pad. It reads the first pad
out, gives the box to the little robot, teaches it to add a fresh 1 to
what it was given, has Ruby loosen the pupil's thought, and reads the last
pad out.

## The pupil on its feet, said once, and a stop explained truthfully

*Added 13 Sep. Ken, running the teacher: "I heard 'I am teaching the robot
to count' twice. The pupil's arm is full size and the pupil is very small;
the student is lying down. The pupil grabs a 1 from the stack -- I thought
the idea was to use the number provided by the teacher. When I stopped the
pupil the narration said the pupil stopped because the teacher hadn't told
it how to work with 3, and yet when I started it again it worked fine. I
think the commentary should only apply at speed 1x."*

**On its feet.** A robot in a box hole lies flat at toy size, and taking it
out kept that pose: the pupil taught its whole lesson lying down, and at
the start of its growth its arm alone read as a robot. Measured: rotation
−1.57 about x for the whole run. It stands up as it steps out.

**Said once.** The pad's own voice said its words, and the card, reading
its messages aloud, said them again. The card shows them and keeps quiet.

**The teacher's own 1.** The pupil's box is [a count | a 1] now, and the
lesson is a copy of the 1 dropped on the count, with the count loosened to
any number: the number it counts with is the one the teacher gave it, not
one off the stack. Started, it counts 1, 2, 3.

**A stop explained truthfully.** The closing commentary asked what the run
achieved and why it stopped, and Marty guessed: "the teacher hadn't told it
how to work with 3" of a robot stopped by hand. The workshop's own account
of the stop -- Stop pressed, the Rounds limit, a thought that no longer
fits -- goes to him with the ask, read off the card a moment after whoever
stopped the run has said why, and he is told never to guess another.

**At 1x only.** Faster than 1x the robot is ahead of any sentence and at
Instant there is nothing to watch, so commentary -- the opening, the lines
per step, the closing -- keeps to 1x.

## The camera stays with the robot, and the pupil goes to its own desk

*Added 14 Sep. Ken, running the teacher: "The camera moves to show Dusty
when running the teacher robot. After the pupil's training is finished it
faces the wrong way in an impossible location (colliding with a platform).
Marty says 'I'm trying to make the count become 1'... Notice the correct
switch from the confusing 'I'm' to 'It'. If Marty is reading a comment
maybe it should preface it. Or was there another cause for 'I'm'?"*

**The camera.** Any line naming a helper moves the camera to frame it --
Ken asked for that, so a child told to wake Ruby can find her. A line of
Marty's commentary mid-run names Ruby too, and so the view left the robot
for the helpers' corner while it was working. While a run is on, the run's
own view owns the camera: mentions are ignored until it ends. Measured on
the teacher: the view asked for stays null for the whole run, following
the robot, where it used to fit the helpers. The refusal at the END of a
run still moves it, which is what the thought view depends on.

**The pupil's desk.** Two faults, both about where a robot aside stands.
The first slot aside is 0.35 from the fourth work spot, so the pupil's desk
stood inside that platform; a slot is now taken only if it clears every
work spot in play (and the next few the workshop would grow), every stack
and every other desk -- measured against the whole grid it rejected all
four slots and fell back to the bad one, so the lookahead is bounded. And
the pupil was left wherever its last step took it, facing whichever way it
had walked: measured at (-0.3, 0.36) turned -2.79 radians, in the middle of
the floor. It walks to its own desk and squares up when the teaching ends,
as a robot does at the end of a lesson. Measured now: home (1.25, -0.62),
yaw 0, 2.15 clear of the nearest work spot.

**Who is speaking.** No note was being read: told to comment on a robot,
the model slipped into the robot's own voice -- "I am trying to make the
count become 1" -- which reads as Marty claiming the work. Both asks pin
the pronouns now: Marty is watching, the robot is "it", and a robot's note
is its author's words, to be quoted as "its note says ..." and never spoken
as his own.

## The robot works while Marty talks, and watches itself from higher up

*Added 14 Sep. Ken, giving the teacher its box: Marty "correctly reads 'It is
trying to teach the little robot to count on from any number...' but that
causes a very long pause before the first action. I think they should
overlap." Also: "After the pupil has run a cycle it says 'It puts that 1 into
the first place, changing the 0 into 1 to begin the count' -- but the 0 is no
longer a zero." Also: "I wonder when a robot is working if the auto camera
should move higher. Not directly above the robot but a good deal higher so it
is easier to see what is in its boxes." Also: "When I changed the speed from
1x I still hear Marty's commentary while it runs... I guess it is fine to keep
commentary for 1/2x."*

**The pause.** A narrated run made two asks of the brain, one after the other
-- the opening comment, then a line for each step -- and waited for the whole
opening to be read out before the first step. Three waits, in series, and a
robot standing still through all of them. Now both asks go at once, the robot
sets off, and the opening is read while it works. A line he cannot say at that
moment -- his opening still going, his lines not yet come, a pad being read
aloud -- is not said at all rather than queued behind: the steps he could not
reach in time go unsaid, and the narration picks up from the step at hand.
Measured, with a brain held at the door: both asks out, nothing said, the
robot already holding a number and working. On the build before, the same
measurement found it idle with nothing in its hand.

**The 0 that is no longer a zero.** His lines are made once and said again on
every round, so a line that names a number goes wrong as soon as the number
changes -- "changing the 0 into 1" the moment the count is 1. And the 0 was
not even on the desk: a robot's steps are read to him against the box it was
shown in its lesson, so the facts carry the lesson's numbers as well as this
round's. The ask now rules out both: they are only where the counting starts,
and a hole is to be named by what it is -- the count, the number it was given
-- never by a value it happens to hold.

**Higher up.** The follow sat level with the bench -- twenty-four degrees
above the work, measured -- where the near wall of a box hides what is in its
holes. While a robot runs the same line of sight is tipped up to forty: into
the boxes, and nowhere near straight down, where a robot is a hat. A lesson is
the player's own work and keeps the view they chose.

**Only while someone is watching closely.** Commentary is for 1x and 1/2x.
Above that the robot is ahead of any sentence, so a run sped up mid-way stops
being narrated there and then -- the line in the air cut short with it, since
what is being spoken then is his.

## Watching, not reaching

*Added 14 Sep. Ken, on the teacher and the factorial robots: "The camera
didn't follow the use of Ruby after training the teacher robot." / "I
wouldn't say 'replace' when talking about adding 1 to 0." / "when there is a
team saying 'it' can be confusing -- maybe best to refer by name if it has
one." / "the camera angle could be greater and more zoomed in to watch how the
factorial robots work. The box the robot is working on should be easier to see
(while still maintaining the bigger context. But the left third of the view
isn't needed (pads, houses, marty, ...)" / "the nest is placed on top of the
notebook in the factorial example."*

**Ruby, in a run.** Waking Ruby by hand is an occasion the camera answers: it
goes in close on the thought where her work will show. A robot having her
loosen a pupil's thought was not an occasion at all, so the one moment of the
teacher's run worth watching happened somewhere off the picture. It asks for
the same close view now, and hands the camera back when she is done -- measured
on the teacher: the view asked for is the close thought at the moment Ruby
flies in, and the follow is back on the next step.

**The picture was four metres wide.** Three things had widened it. The camera
sat two and a half metres back whatever the screen, so a wide one showed four
metres of workshop across with the box in the middle of it a fifth of the
width; the fit that keeps the work area in view held the desk AND the claw in
the picture even when the robot had walked two metres off to a stack, which
pulled it back to five; and the pointer leaving the picture leans the camera
out, which is what reading Marty's card at the left of the screen does. Now:
the distance comes from the width wanted (about three metres of workshop
across, so a wide screen comes nearer rather than showing more), only what is
within arm's length of the subject is fitted in as well, and while a robot runs
the lean-out is off -- watching is not reaching. The angle is up from forty
degrees to forty-six. Measured on the factorial robots, same screen: the view
went from five metres back to one metre seven, and the box from 0.21 of the
screen's width to 0.31-0.43.

**What a drop does, and who is who.** Told only that a step puts a number in a
hole, models described adding 1 to 0 as "replacing" it. The workshop's rule is
now in what Marty is told: a number dropped on a number is arithmetic -- adds,
or whatever sign it carries -- and only an empty hole is filled. And with a
team at the desk, "it" is anybody: he is asked to say which robot by name
wherever the facts give one.

**The notebook steps aside.** It is furniture, dropped into whatever world you
open, and a world puts its own things where it likes to sit: the factorial
example's nest stood on top of it. Once a world's things are down, it moves to
the nearest clear spot; the place you left it is still the place you left it,
and it goes back there in a world that leaves it room. The dodge needed a fix
of its own first -- a thing already on the table blocked every spot around it
with its own footprint, so nothing 0.86 wide could ever find room to move.
Measured: the notebook now sits 0.62 from the nest, which is exactly the room
the two of them need.

## Every face of a turned cube reads

*Added 14 Sep. Ken, with a picture of a cube lying with its factors toward
him: "When a number cube has been rotated ensure that the text is rotated to
be as easy to read as possible... E.g. the scientific notation face in the
previous attachment."*

Turning a number lands the face you asked for upright -- the cube is rolled
about the line of sight until that face's writing stands up -- and left the
other five wherever the turn put them. Measured on a cube tipped one quarter:
of its six faces, two were upside down and two ran bottom-to-top up the side
of the block, the scientific notation among them.

A face is a real pane, so nothing needs deriving: each one is rolled about its
own normal by the quarter turn whose writing points most nearly the right way
-- up the screen for a pane seen side-on, and away from the front of the table
for one you look down on, which is how writing on a table reads and what the
lid already did before anything was turned. A cube standing as it was made
scores a perfect one on every face and nothing moves; tipped, turned, or set
back down turned, it scores one on every face again. The rolls are chosen
afresh from the pane as built, never added to what the last turn left, so a
hundred turns cannot drift.

Found on the way, and left alone: a turn made in the first third of a second
after picking a cube up is undone when the flight into the hand lands, because
that flight ends by writing the orientation it started with. Press again and
it takes.

## The eighth activity, and a resort in the yard

*Added 14 Sep. Ken: "Please add activity 8 from the Exploring Infinity page to
the infinity folder. Do you have ideas about how we might make a variant of
the Resort Infinity? Perhaps in the yard?"*

**Activity 8 is Cantor's diagonal**, and the reason it was the one left out is
in the README: a robot here says "hole 1 of what I was given", never "the nth
one", so the nth term of the nth sequence cannot be addressed. It can be
COUNTED to, and the counter is a scale. The Diagonal team's box is
`[Sequences, Current, scale(skipped | to skip), bird]` and the scale's three
states are its three robots: tipped towards *to skip*, **Skip a term** takes a
term off the current sequence and vacuums it; balanced, **Hand one on** gives
the term to the bird, takes *to skip* up one and sets *skipped* one higher
still, which tips the scale over; tipped towards *skipped*, **Next sequence**
drops the finished sequence, takes the next box off the Sequences nest, puts
the nest inside it in the Current hole and sets *skipped* back to nothing.
Nobody holds a growing box of nests; each sequence is used once and abandoned.

Each robot dozes on exactly what it needs -- Skip and Hand one on look through
Current for a number, Next sequence looks through Sequences for a box -- so
the diagonal waits between sequences instead of failing. Measured on the three
rows the world ships with (1 2 3 4 / 1 3 5 7 / 1 2 4 8): the diagonal reads
1, 3, 4, and the "Add 1 to it" room turns it into 2, 4, 5, which is none of
them. Measured also, and worth knowing: hand a box to the bird BEFORE pulling
its room's lever. A term delivered while the bird is still carrying the box
can be missed, and then the count is off by one -- the doubling row handed on
8 where 4 was wanted. The pad says so.

**Resort Infinity, in the yard.** The original is a ToonTalk city: you are the
clerk, guests arrive on a nest for ever, and you train an address robot that
says where each new guest's cottage is built -- and, from problem 2, a move
robot that tells the guests already housed where to move to. Five problems:
one infinite group; five more guests and no empty cottages (move up five); a
second infinite group (double, and the newcomers take the odd addresses); three
groups at once (times four); infinitely many groups (double, and walk the
diagonal of the square of new guests). The city was the addressing scheme, and
this workshop has no cities. It has the yard, which is a better fit than a city
was: a cottage is a house standing on the grass, an address is a place along
the row, and a move is something every guest walks. The sketch is in the
infinity README under *What is not here*; not built.

## Resort Infinity in the yard, and the view that goes with a world

*Added 14 Sep. Ken: "Yes build the 'infinity yard' and start with the first 2
problems. Let's add the camera state to saved worlds. The making-of should
provide the statistics split by when we first introduced images and other
media (around 23 August) and since."*

**Hilbert's hotel, outside.** The original is a ToonTalk city: you are the
clerk, guests arrive for ever, and you train a robot that says where each new
guest's cottage is built -- and, from problem 2, a second that tells the
guests already housed where to move to. The city was an addressing scheme, and
this workshop has none; it has the yard, which suits the story better. A
cottage is a house standing on the grass, an address is a place along the row
(x = n * 0.6 - 4.5), and making room is the whole row shuffling up where you
can watch it.

Three things had to be measured before any of it could be designed, and all
three came back yes: a gadget shipped in a world file, bound to a house by
`boundTo` and a live bird's `liveId`, comes up bound; a robot in its panel can
work out a place from a number and send `[set | position | [x|z]]` to its
thing; and that works on the grass as well as on the table. The probe cottage
jumped to exactly 3 * 0.6 - 4.5.

**One nest each, which is the whole design.** The first two builds failed the
same way, and the rule behind it is worth writing down: *a team stops at the
first member whose thought is waiting on an empty nest* -- that is what dozing
IS. So nobody may doze on two nests. A guest cannot listen for its address on
one nest and for the bell on another; a clerk cannot listen for arrivals on
one and for move requests on another. Each has ONE nest, and what lands says
who runs. A guest's nest answers to two names -- its own and the bell's, by
`aliases`, which a world file keeps -- so one ding reaches everybody and an
answer still comes back only to the guest who asked. The desk tells the two
kinds of letter apart by their shape: `[number | bird]` is a new guest,
`[pad | number | bird]` is a guest asking to move, and the pad in the longer
one is the ding itself, forwarded.

What the visitor trains is three steps long, which was the point: take the
letter off the post and give the bird the address. Problem 2's robot adds five
and joins the first as a team. Each cottage's own robots are the resort's
machinery, in a macro pad -- one press of SPACE starts all six.

Measured end to end: six guests house themselves at 1 to 6; the bell rings and
all six move to 6 to 11; the five newcomers then take 1 to 5. Eleven cottages,
no two at the same address. Problems 3 to 5 are the same machinery with
different arithmetic.

**The view goes with the world.** A world saved after you have put the camera
somewhere yourself opens at that view; one whose camera you never touched
carries none and opens at the workshop's own framing, which fits itself to the
window. The gate is the player's own gesture, not `userMoved` -- a demo sets
that too, and the goldens would have gained a camera each. Saved indoors only:
a file always opens indoors, so a view taken from the yard would look at the
wrong place. Checked: untouched saves none, a placed view comes back, and all
thirteen golden worlds stay byte-identical.

**The figures, split where the story splits.** The making-of's table now
divides at the day media arrived -- 25 August, the line "a picture is a pad" --
rather than at the day the page was written. Nine working days before, twelve
since; 154 commits and 87; 180 prompts and 189. The interesting one is the
ratio: thirty tool calls to the prompt before media, fifty-four since. The
second half is where measurement got cheaper than guessing.

## What Dusty took off a page, and where a pile stands

*Added 14 Sep. Ken: "When I vacuumed a page from a notebook it didn't end up
in Dusty's bag." / "activity 8 started to work but after it created 3 numbers
in the diagonal nothing more happened." / "The nests are not placed well since
they quickly obscure what is happening behind their stacks."*

**The page and the bag.** An open notebook draws four things -- a page
number, the entry on that page, the next page number, its entry -- and keeps
them in one list, in that order. Three places went looking for a page's entry
by counting into that list with the page's own number, which finds the NUMERAL
for a left-hand page and the neighbour's entry for a right-hand one. So Dusty
emptied the page you pointed at and carried off a little numeral; the entry
itself was simply gone. The entry is found by what it is now -- the node the
page's own clicks are set on -- and a check watches both pages: vacuum the 7
on the left and the pad on the right, click his head, and get back the 7 and
the pad.

**The diagonal stopping.** Not a fault: after the third sequence the team has
read every row it was given and is dozing on the Sequences nest, which is
exactly what it should do. It said nothing about it, though, which is the same
as being broken. The pad says it now, and says why it is the point: the list
is yours to go on adding to, and every row you add gives the diagonal one more
term.

**Where a pile stands.** A nest's pile grows upward, so a nest in the middle
of the table becomes a wall in front of whatever is behind it -- and these
worlds put their watch nests in the middle, where the rooms are. In Activity 8
the two you watch now stand at the front corners, clear of every room's line of
sight, and the pads, which lie flat and hide nothing, take the middle. The
other activity worlds have the same arrangement to fix; they are golden worlds,
so that is a change to make on purpose rather than in passing.

## Pictures are for the eye, and a model out of a file

*Added 14 Sep. Ken: "I like the emoji in 'press the microphone 🎤 and speak. I
read my answers aloud — the speaker 🔊 next to my name switches my voice off
and on' but it causes the narration to say 'microphone microphone' and 'speaker
speaker' — maybe emojis should be removed before sending to text-to-speech?"
and "We should be able to import 3d models? Implement it for formats that make
sense."*

**The pictures come out of the voice.** An emoji stands next to the word it
illustrates, so a voice reading it says the word twice. Everything spoken now
goes through one filter -- the card's reader, a pad's own voice, and Marty --
which takes out emoji along with their variation selectors, skin tones and
joiners, and the workshop's own icon glyphs (the ⋮ menu, the ⛶ full screen, ▶
and ⏸), then closes up the gaps so nothing is read with a stutter in it.
Arrows and arithmetic signs stay: "the ← and → arrows turn it" and "3 × 4 ÷ 2"
are words about arrows and sums, not decoration. A line that was nothing but a
picture is not spoken at all.

**A model out of a file.** glTF is the web's model format and every character
in this workshop is one, so the loader was already here: a .glb dropped on the
page arrives as a thing you can hold. It is named after its file and sized to
the table -- nothing in a model file says whether it was made in metres,
centimetres or millimetres, so the longest side is made a hand's width and the
model is stood on its feet rather than floating over the middle of itself. From
there it is a thing like any other: copied, filed, named, given a behaviour,
carried out to the yard.

It rides inside the saved world as a picture on a pad does, which sets the
limit: nine megabytes of file, and a plain sentence when something bigger
arrives. A .glb holds everything in one file and is what to export; a .gltf
works only when it is self-contained, and one that points at a .bin beside it
says so rather than failing silently. STL and OBJ would each want another
loader bundled into the three builds -- worth doing if they turn up, not
before.

Measured: the workshop's own Mimi (255 KB, 32 meshes) dropped in as a file
arrives 0.30 x 0.34 x 0.12 standing on the table, saves into a 0.33 MB world,
and comes back out of it with all 32 meshes and its name. Check: modelFile.

**And a refusal that says why.** Ken's first try was the Khronos Duck, and he
took the glTF-Draco folder: 3.8 KB of JSON that points at a Duck.bin and a
DuckCM.png which did not come with it, and asks for a squeezing we carry no
unpacker for. All the workshop said was that it could not be read -- and it
left the name plate standing over nothing, because the thing is made before
the loader has finished and nothing took it away when the loader failed.

Now the file is looked at before it is believed: the JSON is read out of
either form (a .glb's first chunk, or the .gltf itself) and four things are
told apart, because each has something different to do about it. Squeezed
(Draco, meshopt, Basis) -- no unpacker here, look for a plain .glb of the same
model. A table of contents -- it names the files it points at, Duck0.bin and
DuckCM.png, so you know what is missing rather than guessing. A web page --
the page ABOUT the file was saved instead of the file, which is what a GitHub
blob link gives you; go back and use its download button. And not a model at
all. Nothing is made in any of those cases, so nothing is left behind; a model
that fails later (out of a saved world) takes itself away.

The Duck's glTF-Binary folder holds Duck.glb, one file, 120 KB -- it comes in
and stands on the table at 0.34 x 0.32 x 0.24. The glTF-Embedded variant works
too. Draco itself would want three quarters of a megabyte of decoder bundled
into every build, so it is asked about rather than assumed.

## The yard is not a workbench, and a tooltip has two halves

*Added 14 Sep, from a batch of Ken's while playing Resort Infinity.*

**What you carry floated a metre over the grass.** The plane a held thing
slides along was measured once, from the robot's reach at the TABLE, and never
moved again -- so out in the yard, where the ground is a metre lower,
everything you picked up rode at table height. Seen from a camera looking down
that is not "slightly high": it is drawn a long way from the pointer, which is
how Ken's pad "appeared behind a house when I didn't move it there", and why
it did not seem to follow the mouse. The plane now comes from the surface
things actually rest on. Measured: indoors bench 0.84 and hand 1.11 (0.27
above); yard ground 0.02 and hand 1.11 (1.09 above) before, 0.29 (0.27 above)
after. Check: yardHand.

**And the words follow the ground.** "Your workbench", "put it down on the
bench", "set it on the table" -- all of them said indoors things while
standing on grass. Outside they say the grass, and the workbench's tooltip
says what the yard is FOR (room: a village, a zoo, a row of cottages) rather
than repeating the bench's own sentence. A robot may put things down out
there, which it may not do indoors, so that is what the robot line says too.

**A world may keep its whole point outside.** Resort Infinity opens on a table
with one pad on it; the eleven cottages, the desk, the bell and the clerks are
all on the grass. Opening a world now counts what is out there and says so --
"24 things are out in the YARD, through the green back door, which is where
this one is meant to be played".

**A tooltip has two halves.** What THIS thing is, then how anything of its
kind is worked, with a rule between them so the eye can skip the half it has
read a hundred times. A pad's first half is what is written on it -- not "A
pad", since the pad is what the pointer is on -- and the second begins "Click
to pick the pad up". The text is still put in as TEXT (a pad's own writing
goes in a tooltip) and the rule is a marker in the string that becomes an
<hr> element, never markup.

**A behaviour can carry a note.** A robot has had one since 13 Sep; Ken asked
for the same on a gadget, because "the guests" told him only what any
behaviour says when what it IS is the whole resort's machinery. The note is
written in the same field on the card -- hold the behaviour and it says *a
note about this behaviour* -- travels with it into a saved world, a saved
thing and every copy, and is the first thing its tooltip says.

**A bare operation says its own name.** sin and cos ignore the number they are
written on -- the badge is the whole message -- so a lone sine pad wearing a
"0" was a number that meant nothing. It says "sine" across its faces instead,
and drops the corner badge that would only say the same word again. "sin" is
what you type; "sine" is what it is. The making-of's open-gap list said
operation-only pads were still to come: for these two they have arrived, and
for plus and times they never will -- there is nothing for a bare plus to be
without its number.

**The camera looked away at the one moment something happened.** A copy is a
trip to Mimi: the claw sets the original on her platform, she scans it for
most of a second, and the claw takes it back. While she scans the claw is
EMPTY, and the follow fell through to the robot's own stand across the desk,
where nothing at all was going on -- away and back, for nothing (Ken). The
camera's subject is now the claw, else the copier while she has something of
its, else what the robot was given.

**And a space that went nowhere visible.** SPACE switches on the thing in your
hand if there is one, and otherwise whatever the pointer is over. So with the
desk box in your hand -- which is exactly where problem 1 has you -- pointing
at "the guests" and pressing SPACE typed a space into the BOX's name, and the
behaviour never started. Nothing said so. It says so now: "That space went
into the box's name -- whatever is in your hand takes the keys. Put it down
first, and SPACE switches on 'the guests'." Measured with an empty hand: six
letters on the post and 24 robots running.

**Your hand is yours while the houses run.** Ken, with zeno going: "picking
up and inspecting the text pads stopped working too". A house's own robots
call the same "what is in the hand now" bookkeeping for their CLAW -- which is
right, since that is what a lesson types on -- but they call it from inside a
pushed world, where the hand is the inner world's and yours is not visible at
all. So a second after the two levers went down, the card that reads a held
pad lost its Read button and the pad in your hand stopped being a pad as far
as the card was concerned. The card is about the hand, and it is left alone
from inside a pushed world. Pre-existing, not new: measured the same on the
previous build. Check: zenoCheck (your-hand-stays-yours).

**And the gap list was out of date about scales.** Ken: "don't they do that
already?" They do: a scale with a thousand in the other pan judges "a number
bigger than a thousand", puzzle 18 is judged exactly that way, and a robot
reads a scale's three states as its condition. What is actually missing is a
scale that gives a NUMBER -- how much heavier -- which is what the entry now
says.

**Resort Infinity's pads.** Problem 1 never said where a box to train on comes
from (it is the desk itself, lying on the grass), so it now says: take a
little robot, set it on the grass, click the desk to pick it up and drop it ON
the robot. It says what to watch for -- a letter landing on the post for each
guest -- and it says plainly that "Next address" beside it is the same answer
already trained, for a clerk who would rather read one than write one. Problem
2 says the same of "Move up five". The fence pad described one row of eleven
cottages when eleven were standing at the gate in two huddles; it now says
what the two huddles are and that the row forms as each one is housed.

## A name plate through a duck's head, and a model that said nothing

*Added 14 Sep. Ken imported the Khronos duck and sent a picture of its name
plate cutting straight through its head; and: "there are no tooltips for 3d
models".*

Every thing but a box, a bird, a nest and a field takes its plaque at a fixed
(0, 0.27, 0.06) -- which clears the workshop's own small models and sits
squarely inside a duck read off a file. A model is whatever shape it came as,
so the plate is now measured onto it: over its top, just in front of its face,
centred across. And a model out of a FILE is empty when it is named -- the
loader is still reading -- so the name goes on again when its meshes arrive.

The tooltip was simply missing: `model` fell off the end of the list to
`return null`, which mattered little while the only models were the
workshop's own and matters now that anybody can drop a duck on the page. It
says what it is, how it was made (out of a glTF file, or built of solid
shapes) and how big it stands, then the usual half: pick it up, + and - and
the arrows are its own and are saved with it, and from there it is a thing
like any other. Both halves measure the model and not the plate standing over
it. Check: modelFile (name-stands-clear), padTip.

## A behaviour that could never be moved

*Added 14 Sep. Ken copied the airplane, pressed SPACE on "the pilot", and only
one of them flew: "Shouldn't the copy have maintained the bird connection so
the gadget broadcast to both copies?" And then: "I typed '.' to the pilot and
after a while it stopped. Why the delay?"*

**The copy is its own airplane, and that is deliberate.** A copy of a live
thing gets a fresh identity, because two things answering to one name make the
mail ambiguous -- it is the same rule that stops a file imported twice from
putting two things with one name on the table. So "the pilot" goes on flying
the first plane.

**But the broadcast Ken expected is real, and it is how this world already
works.** The pilot does not address the plane directly: it posts orders to an
ordinary nest, `turtle3d-orders`, and "a 3D turtle" -- the behaviour BOUND to
the plane -- reads them and flies it. An ordinary nest's guid is never renamed
on copying, because sharing a guid is joining the flock, and a bird's delivery
goes to its own nest and a copy to every other nest answering that guid. So
one pilot CAN fly a squadron: what has to be copied is the TURTLE, bound to
each new plane, not the pilot.

**Which is where the real bug was.** Binding a behaviour to a different thing
always refused -- "Nothing on that panel speaks about my thing" -- because
`bindGadget` took the GADGET's own lid as what its panel speaks about. That is
true only while a behaviour works on itself; once bound, its panel names the
thing it is bound to. `releaseGadget` had it right all along and `bindGadget`
did not, so a behaviour could be let go of and could be given to a thing, but
never MOVED from one thing to another -- which is exactly what giving a copied
pilot to a copied airplane is. Measured: fails on the previous build, passes
now, panel and all. Check: rebind.

One thing the fix needed with it: binding a behaviour to the thing it is
ALREADY bound to must be a no-op, not a rebuild. While the code looked for the
wrong name it refused such a drop by accident; looking for the right one it
found every reference, re-pointed each to itself, and threw the live tray away
to rebuild it from the record -- which "a fold keeps nested work alive" caught
within a minute of the real fix going in. It says "already works on that" now.

**And the delay.** "." stops a behaviour's robots at once; it does not undo
what they have already sent. Orders posted to a nest are still in the pile and
whatever reads them goes on carrying them out -- the plane flies the rest of
its orders. The message says so now, and points at the thing itself as the
switch for that.

## The yard is a thing

*Added 15 Sep. Ken: "I wonder if a panel for the yard would be a good idea.
One particularly useful message would be to report all the objects on the
yard and to listen for changes. Perhaps a button under the What's here panel
since there is already the reshape yard button." Then: "Build it with birds in
the report. But I can imagine some situations where filtering by name would be
convenient."*

A place is not a thing, so nothing could address the yard: a zoo could not
count its animals, a village could not notice a house arriving. It has a node
now -- no shape, never on the bench, never picked -- with a name to write to
(`yardNode`, one per place, made the first time anything asks for it), a
panel of its own, and two things to say.

`[query | things | bird]` answers with a box, one hole per thing standing on
the grass, each holding a bird to it, its name and its place -- a BIRD, as
Ken chose, because that is how a thing is addressed here, so a robot can
answer the query and then tell any of them to move. A word in the third hole
filters by the name on its plaque or the words written on it. `[listen |
things | bird]` sends an event nest that hears `[arrived | name | bird]` and
`[left | name]`: a few times a second while you are outside, the things on
the grass are compared with the last look, and the first look is a baseline,
not a crowd arriving. The listener's own nest, carried onto the grass,
announces itself once -- it is a thing on the grass.

**Only the place you are in runs.** The table's things are detached while
you are out and the ground's while you are in, and a panel is a thing on a
bench, so a yard panel opened on the table would stand still the moment you
stepped out to watch it. The button opens it on the grass, and indoors says
so. The query still answers indoors -- the list is the ground's own -- and
the yard's name and panel are saved with the world.

A yard panel has no thing to press SPACE on, so SPACE on the open panel
switches it, the way a house's lever does. Check: yardPanel.

## An airplane with its pilot aboard

*Ken: "let's make another one where the behaviors are all local to the object
so that you can turn on airplane and turn it off."*

`✈️ airplane-with-pilot`: the same flight, the turtle and the pilot grouped
inside the airplane's own panel. SPACE on the airplane flies it and "." lands
it -- switchBound already started and stopped whatever is grouped inside a
thing -- and it can be picked up, copied, filed and carried with its pilot
aboard. The copy question answers itself here: a copy is a second airplane
with a second pilot, and one bird reaches both letterboxes, because a copied
nest keeps its name. Check: airplanePilot.

## Nothing in an example stands on anything else

*Ken's picture: the airplane's "home" pad under a corner of an order box.
"This can cause flicker and should be avoided in all the example programs."*

Every example world is now opened by the suite and every pair of top-level
things measured -- on the table, and on the grass where a world keeps things
outside -- solid parts only, precisely (a house's roof is a cone turned
forty-five degrees, and its loose box was a metre wide). Twelve worlds had
real overlaps, and most came from one fact nobody had written down: the table
clamps z to 2.19, so a row authored at z 2.20 and one at 2.40 or 2.90 were
the same row, and five houses across the table were four and a squeeze. The
generators are re-laid from the measured footprints; the rule is in
examples/README.md; the check is `overlap`, which names each pair with sizes
and centres so the next one is a two-minute fix.

## The keeper's round

*Added 15 Sep. Ken: "Please add a yard panel example to the yard folder.
Maybe add a button that queries the zoo yard and adds a wiggle behavior to
all the animals."*

Three things the vocabulary lacked, each found by trying to write the
keeper. A robot handles one thing a round and cannot walk the holes of a box
whose length it does not know, so the yard's report as ONE box was of no use
to it: `[query | each | bird]` delivers the same report one thing at a time,
oldest first off a nest, which is how every list in this workshop is walked.
The keeper must tell an animal from the welcome sign, so each entry now ends
with the thing's KIND, and the keeper's thought matches the word "model"; a
third member lets everything else go, or the first pad on the nest would
block the animals behind it. And a robot could not give a thing a behaviour
by mail: `[bind | pad]` to a thing's bird sets the behaviour down beside it,
binds it and switches it on, exactly as dropping the pad on it does -- and
`bindGadget` learned to keep quiet, since seven animals would have been seven
sentences.

**And two faults under the floor, found by the keeper.** A letter a robot
sends is opened INSIDE that robot's panel, where the bench, the stations and
the hands are the panel's: a behaviour bound from there was set down on the
robot's own work spot -- its tray on s0, a fresh work spot minted every round,
1,289 of them -- so a bind now waits for the thing's own world to be current,
which is never more than a turn away. And `switchNested`, which sets a
behaviour's parts going, decided "is this gadget in a hole?" by searching the
world that was current -- the walk runs before the panel's world is pushed, so
it could not see the panel's own holes at all -- and switched on the wiggle
the keeper keeps in its box as if it were a part: a stranded tray whose world
had captured the keeper's work spots, copied into every wiggle the keeper
handed out, each arriving with a spent [go] on its first spot. The test is
structural now: nothing inside a box, a nest or a scale is a part.

`🦓 zoo-keeper`: the zoo, a brown pad by the door. SPACE on it, and the
elephant, the giraffe, the lion, the zebra, the penguin, the crocodile and
the flamingo each get a wiggle of their own, lying beside them, bound and
running -- one a round. Check: zooKeeper (seven animals, seven wigglers, one
each, the sign spared).

## The keeper's second round

*Added 15 Sep. Ken: "some of the wiggle behaviors are blank"; "wiggle the
animals works but typing '.' doesn't stop the behavior"; "the elephant
doesn't wiggle"; "when I pick up any of the behaviors and type control-p the
panel appears at the far edge of the yard in the center. There should be
animation as it comes out (and when it returns via the knob). Same with the
info notebook."*

Four of seven wiggles came out white because the face-painting drain threw
away any pad with no parent as if it were gone -- and a behaviour taken out
of a `[bind | pad]` letter has no parent for the frame it waits for the
outer world. No parent is not gone now; only a disposed pad leaves the
queue.

"." did stop a wiggle, pointed at the wiggle or at its animal; what it did
not do was stop the zoo from the pad that started it. A behaviour handed out
by another behaviour's robots now remembers its giver (`givenBy`, saved and
copied with the pad), and is switched with it: "." on the keeper rests every
wiggle it gave, SPACE sets them going again, and "." on one animal says
where its behaviour came from.

The elephant wiggles as often as the rest -- about three turns a second,
measured at 100 ms -- which is also why a one-second sample could read it
as still for six seconds running: three turns a second sampled once a second
lands on the same side every time. A screenshot catches each animal at
0 or 25 degrees by chance. Nothing was changed for it; if it stood still
for Ken, the likeliest cause was "." over the elephant, which rested its
wiggle and now says so.

A panel on the grass went to the table's tray row -- the far edge of a
ten-metre yard, in the middle -- and a working panel brought back out with
Ctrl-P simply blinked on there; the knob blinked it off. `freeTraySpot` puts
a tray on the grass beside its thing (or beside the hand holding it), and
every way out now plays the same growth from the thing (`trayOutFrom`),
every fold the same shrink into it (`trayHomeInto`, ending hidden rather
than gone for a working panel). The info notebook rose from the world's
origin because it was nowhere yet: it comes out of its plaque now and goes
back into it.

Check: zooKeeper's second line (no blank faces; seven rested and none
turning; seven woken and all turning again; a tray that grows from the hand
to a spot beside it, and folds home to hide still working).

## Read once, spoken smoothly, and a behaviour in the hand

*Added 15 Sep. Ken: "When I picked up the pad 'the row goes on' in the
resort infinity example and clicked to read it I heard it read twice. And
there was unusual pauses in the narration"; "the 'the guests' and the 'five
more guests' buttons/pads don't do anything when I type space to them";
"the tooltip should include box label"; "the switches on houses are hard to
access sometimes"; "pointing to a transparent house should produce a
tooltip saying its name and how it can be turned on or off".*

Read showed the words as a hint and spoke them, and the hint reader spoke
them again: `hintLastSpoken` is set first now, as a robot's own reading
already did. The pauses were the pads' hand-wrapped lines -- a voice pauses
at every line break, and a problem pad has one every thirty characters.
`spokenWords` joins a single break into a space and reads a blank line as
the end of a sentence, supplying the full stop when the line above had
none.

"The guests" did nothing because clicking a pad picks it up, and SPACE on a
held pad is typing: the key went into its name ("the guests ") while the
card said to drop it on a robot. Measured: the same press with an empty
hand, pointing, sent six letters to the post. A behaviour in the hand is
now switched, not written on: SPACE sets it down where the hand is and
switches it on; "." sets it down and rests it. Problem 1's pad also said
"the box to train on is that desk" of a desk it had just called a box with
a nest in it; it says which box now, the moves to train the clerk are on a
pad of their own, and each problem fits one tooltip (P1 548, TRAIN 404,
P2 591 of the 600 characters a tooltip shows at once).

A box's tooltip begins with its name when it has one. A house pointed at
with an empty hand says its name, whether its walls are glass or solid,
whether it is running and which key or switch changes that, and what the
roof and the door do; the roof's own tip says which way the next click
takes the walls. The lever moved from the right wall, where the house next
door hid it as often as not, to the front beside the door.

## One turn a frame

*Found 15 Sep while chasing the keeper's "stuck" wiggler in the suite.*

`processDirtyRooms` is reached from the frame loop, from the top of
`tick()` and from `afterQueue`, and a ticker took a turn from each: in the
suite a wiggle received two letters a frame -- a turn and its undoing --
and stood still to the eye while its letters arrived as fast as the
elephant's (2633 to 2650). A panel is "one round a turn", and a turn is now
a rendered frame: `renderFrameNo` counts frames (tick, the harness's own
frame, and `D.rooms`), and a panel that has had its turn this frame is
passed by (`__rframe`). Houses are untouched; a woken panel takes its turn
a frame later at most. The check samples every frame now, since a flip a
frame aliases against any even sampling period.

## Activity 8 asks for its terms

*Added 15 Sep. Ken: "activity 8 is confusing - screenshot 2 is what I see
when I turn it on."*

What he saw was a tower: the three sequence rooms were tickers, each
making a term a round for ever, and their terms landed on the nests in the
boxes still standing on the table waiting to be handed over -- two metres
of numbered cubes over the desk, and the diagonal doing nothing because no
box had been given to it yet. The instructions said to hand the box over
first, which is the kind of order nobody keeps.

A sequence is made on demand now. A room dozes on an "asked" nest; a
number landing there is a request, and the robot spends it, gives its bird
a copy of its term and moves on to the next. A sequence arrives at the
diagonal as a box, [its nest | a bird to that room's nest], and every term
the team takes it asks for the next by dropping a copy of its "more" number
on that bird -- so a room is always one term ahead of the team, whatever
order the levers and the boxes go in. The RUN pad says so, and the
training and the argument have pads of their own (RUN 504, OWN 385,
THINK 356, MORE 385 characters). Check: diagonal (levers first, then the
boxes: nothing made before it is asked for, the diagonal reads 1, 3, 4,
and no sequence pile ever exceeds two).

## Resort Infinity: the guests walk

*Added 15 Sep. Ken: "Why are there 11 cottages and they disappear and
reappear when the robot runs? Problem 1 moves cottages 2 to 6 and then
cottage 1. Why? We need to convey the idea that guests at first move to a
cottage 5 down so the new guests can have rooms. Moving houses is just
confusing."*

The cottages were the guests: each was a house with a behaviour bound to
it, told where to stand by the clerk, and `[set | position]` put it there
in one frame -- a house vanishing at the gate and appearing along the row.
Now eleven cottages stand in a fixed row, numbered from the left, and a
guest is a pad at the gate that walks to the cottage it is given
(`make_resort.py`: `cottage(n)`, `guest(name, lid, bg)`; the guest
behaviours are bound to the pads and put them at z 5.2, in front of the
row at 4.5). A thing on the table or the grass told where to stand GLIDES
there now (`startGlide`/`advanceGlides`, half a second; a thing on a field
still jumps, since a game places its ball by the frame).

Guest 1 was housed last because of the post, not the clerk: the six letters
left together, the courier's own letter was tucked with an animation and
joined the pile when that ended, while the five that rode along were set
down at once -- so the first letter sent landed last. Her own letter is set
down with its companions now, in posting order (`advanceFlights`), and
the panels nested in a behaviour take their first turns in the order they
were made rather than from the end of the register.

What is NOT a fault: the clerk's round takes about nine seconds at 4x
because its copy walks to Mimi and its vacuum walks to Dusty, two metres
each way, which is the workshop's ordinary pace; the pads say to set the
Speed up.

Check: resort (eleven cottages, the letters land 1 to 6, guest 1 walks
first, the mover joins as a team, the bell moves everybody five along, the
five newcomers take 1 to 5, eleven distinct cottages, and a newcomer is seen
part-way across the grass).

## A bird to the computer

*Added 16 Sep. Ken: "We need a bird to the 'computer'... Various JavaScript
functionality can be accessed this way. Maybe the first example is to query a
timer or the time. Then using the number API we can construct something like
the timer sensor." And: "a 'computer' notebook in the devices folder. Page 1
should be a text pad saying 'Bird to computer' or the like, page 2 the bird,
and the rest alternating doc and sample messages."*

The computer is a live thing with a FIXED name (`COMPUTER`), made once at
start and kept through every world (`computerNode`, re-registered in
`clearWorld`), so a bird to it can be saved in any file and kept on a
notebook page. It has no body. `computerMsg` answers `[query | time |
bird]` with milliseconds since the workshop opened, `[query | date | bird]`
with `[year | month | day]` and `[query | clock | bird]` with
`[hours | minutes | seconds]`; anything else gets the list. No `listen`: the
timer is built, as Ken wanted. A number now takes `[set | value | n]`
(replace, where a badge adds; the echo rule applies). `devices/computer` is
the notebook Ken described, `devices/timer` the one-robot timer bound to a
number, measured at about two readings a second, resting on ".". The
in-app Devices notebook gained a page of words and the bird.

The year puzzle, p35, is played after the door code (p11 loads p35, p35
loads p12). Its judge cannot know the year, so it asks the computer, takes
the year out of the date box, gives it a minus badge and drops it on a copy
of the answer: exactly zero is right. The worked example in the last hint
is computed when the set is generated, so `make_puzzles.py` should be run
each new year. Numbering: p35 sits after p11 in play but not in name;
renumbering p12 to p34 would touch every file, the suite and players'
saved progress, and was left for a deliberate day.

## The second arc of puzzles

*Added 16 Sep. Ken: "Let's start on the second arc of 3D puzzles."*

Four puzzles, p36 to p39, chained from p34: the lion told where to stand,
turned until its facing reads 0, given the walk, and carried out to the
grass. What they needed was a judge that ASKS. A thing's place, facing or
whereabouts is not something the player can hand over, so the judge holds a
bird to the lion (or to the yard) and, when the player gives its own bird a
pad saying done, sends the question and reads the answer off its post.

Two things the first draft got wrong, both measured. The judge had a nest of
its own for the answer, and a team stops at the first member dozing on an
empty nest -- the leader dozed there and the member that asks never ran; so
everything now lands on the one post, and what lands says who runs: the
right answer, the done pad, or anything else (which goes back with the "not
quite" pad and the done pad, for next time). And the reply bird went into
the letter's third hole, which is right for `[query | position | _]` and
wrong for the yard's `[query | things | lion | _]`, where that hole holds
the word: the yard got a letter with no bird and said so to nobody.

Under the floor: a model's facing reading came from a field only
`[set | facing]` wrote, so a lion turned a quarter by `[move | yaw | 90]` or
by the arrows still answered 0; `facingOf` reads the thing's own turn now
(minding the hover wiggle, which borrows it), and `[set | facing]` on a thing
with an aim writes the aim, or the next set-down put the old turn back. A
model's "forward" is +z whatever way its head points, and the zoo's heads
point +x -- so the walk goes AWAY, towards the near edge, and the lion is
set facing you; a model built to look along +z is a job for another day.

## The timer, the way a player would build it

*Added 16 Sep. Ken: "When I dropped the timer panel on the number panel
instead of nesting the time pad began to float over the panel"; "the stop
button didn't work... it just started the next cycle"; "I typed '.' to it but
it didn't stop"; and the proposal that a behaviour is authored by training
robots INSIDE a thing's panel, with the panel's bird at hand and the
answers to what they send arriving while they are trained.*

Four faults, each measured. A card nested in a panel stood at table
height, and a panel has no table: three-quarters of a metre over the tray,
in either gesture. `fitRoomContents` now rests the lowest visible thing on
the floor (a robot's feet are already there, so a panel with a robot keeps
its desk). Inside a panel, Stop finished the round and a delivery landing
on the desk box armed the auto-run, so the robot set off again: a stop by
hand holds the auto-run until Start and puts the room you are standing in
to rest, so leaving does not set it going either. "." on a thing whose OWN
panel holds a working robot did nothing, because `switchBound` counted
only behaviours grouped inside; a robot of the panel's own counts now, and
SPACE starts it. And the computer answers `[query | seconds | bird]`.

The timer is rebuilt as Ken described: no separate pad, a box and a team of
two on the number's own panel. One robot asks and moves a "go" pad across
to the next hole; the other runs when a reading lands and the pad is there,
tells the number, and moves the pad back. That pad is the whole of the
composition: a team stops at the first member dozing on an empty nest, and
no thought can say "an empty nest", so two robots take turns by a token
crossing between two holes -- the wiggle's idiom, and now the timer's.

## The perch

*Added 16 Sep. Ken: "the idea of having access to 'my thing' bird while
training should work even when nested since as you say this bird goes to the
object of the outermost panel. Let's try it... just the my thing bird as
available during training and then will access that bird when run. I guess
a user should be able to test such a robot without entering a panel by
placing any bird on that pedestal."*

A pedestal beside the robot's desk, in every world: the perch. On a panel
it holds a bird to "my thing", the thing whose back the panel is. She
carries no name, and is resolved when a letter is given, from the world
that is current then: a robot's round runs in its panel's world, and so
does a hand inside an entered panel. A card standing on another thing's
panel, or a behaviour bound to a picture, resolves on up to the outermost
thing -- the original's rule that a sensor belongs to the owner of the
uppermost back -- so a robot trained on one panel does the same work
wherever it is moved. Take her off the perch and another is there at once;
the one in your hand goes in a box and travels with the robot. She is never
saved into a panel's world (a panel whose only content is its own fixture
is still an empty panel), and a training daydream's rewind leaves her be.
Nor is she in a panel's world while that world is stashed: in a tray's
miniature she stood where no perch is drawn and counted in the fit of the
panel's contents (a picture's page of cards came out smaller), and an
invisible node still counts to a bounding box -- so she is added to her
world only while it is the one on display.

On the bench the perch is empty and she has nothing to go to: a letter put
there says so and the round stops. Set a bird of your own on the perch and
a robot's letters go to her nest -- the way to try such a robot out without
entering a panel. A robot's put on the perch is a put on the bird standing
there, which a robot's put on any station already knew how to do; a put on
an empty perch, of anything but a bird, is refused in training and aborts
in a run.

The timer is rebuilt on it: the box on the number's own panel holds no bird
to the number now, and "Tell my number" gives its letter to the bird on the
perch. SPACE on a thing's panel starts the robots on it, as SPACE on the
thing does.

Ken: "once this is working we should add a few examples to meta where a
robot demonstrates how to create a behavior like this." Two: *telling*, a
teacher that trains one pupil to put a reading in a `[set | value | _]`
letter and give it to the bird on the perch, and *timer-teacher*, which
trains Ask and Tell one after the other, each on a box in the state that
robot works in. Both lessons run for real on the bench with a bird of your
own on the perch -- Ask really asks the computer, Tell's letter really lands
on "what it told" -- and the pads say how to move the pupils onto a number's
panel. Nothing was added to what a robot can do; `put('perch')` is a taught
step like any other.

## A lesson waiting, and the little robots it taught

*Added 16 Sep. Ken: "When I tried to train to have a panel robot to copy a
message, give it the thing bird, and then drop a 1 on the number in the box
the training started with the drop of the 1 -- and the copying, putting one
back, and giving the bird a copy were not recorded." And: "the meta timer
example doesn't involve panels - it should end up with a number that when
turned on is a stop watch."*

The first was measured as Ken described: a box dropped on a number's panel,
then a fresh robot, and the robot stood behind the panel's desk with the box
on it -- given offstage, where no lesson can begin -- so the hand's gestures
inside were a hand's, not a lesson's. An untrained robot with a thing on its
desk IS a lesson, so it begins as you enter the panel; the drop says "go in
to train it". Measured after: take, put on the copier, take the copy, put on
the perch (the number really reads 7 in the dream and 0 again after it),
a fresh 1, put in hole 2 -- six steps, and the run does them for real.

The second needed one thing a robot could not do: reach the little robot it
had taught. After "Stop teaching it" the pupil stood at a desk of its own,
addressable by nobody. Now the pupils a robot taught in this lesson (or this
run) are among its things -- "the first little robot it taught", "the box on
the desk of the second little robot it taught" -- and a click on the pupil
with an empty claw, or on the box on its desk, is a take. The pupil comes up
small in the claw, its desk goes when nothing and nobody is left at it, and
a put on a panel tray sets it behind the panel's desk (a second trained
robot joins as a team). The timer teacher ends that way: the number's panel
out onto a work spot, Ask's box back in its hole (a desk left aside holds
the panels still), Tell's box on the panel, Ask, Tell, fold -- and the
number, taken out of the box, climbs on SPACE. The dream rewinds it all.

## The behaviours on the perch

*Added 16 Sep. Ken: "Go ahead and update the examples to use the bird on
the perch but it should not come from 'the hole-0 bird' but from the panel's
bird."*

Every gadget's box loses its hole-0 bird to my thing; the holes shift down
one; the put that sent a message "to my thing" is a put on the perch, and
the bird standing there is the panel's own -- a bird to whatever the panel
is the back of, resolved when the letter is given. Birds to OTHER things
stay in the boxes: the bell, the score, the counter, the desk, the yard.
Twenty-odd builders: the shelf (both halves), moving, bouncing, following,
wandering, the ellipse, both turtles, Pong twice, Space Invaders' seven
cards, the zoo keeper's wiggle, the resort's guests, the puzzles' walk;
the airplane's pilot and the gauge were never about my thing and stand as
they were. The open-bench worlds set a bird to the star on the perch by the
world file.

Two things in the app had assumed the old way. Binding refused a gadget
whose panel held nothing that named it ("nothing to re-point"): the perch
speaks for my thing now, so binding sets what the panel is the back of and
re-points only the channel nests. And the yard's panel is the outer world
itself, so a thing on the grass is not "inside" it -- the resort's six
guests had been writing their positions to the yard.

## The switch, the stopwatch, and a copy of its own

*Added 17 Sep. Ken: "I made a copy of the stopwatch and it did nothing
(visible) when I started it... a stack of unprocessed responses"; "You can
turn off the stop watch and edit its value (e.g. to zero) but then starting
it again resumes its old value. I wonder if an event an object can listen
for is when it is started"; "the pupil should be ½ size"; "one of the work
spots has a white circle that comes and goes"; "the 'move up five' robot
fails to match the messages sent by the 5 more guests gadget"; and "the back
of a thing" should be its inside.*

Measured on the copy: its "readings" nest kept the original's name, so the
birds of both panels delivered to whichever nest was found first, and
readings piled up unprocessed on both. A nest on a panel with a bird to it
on the same panel is a private post, and a copy's private posts take fresh
names with their birds; a letterbox posted to from outside keeps its name,
since sharing a name is how one posting drives a squadron. And the original
had been running since the teacher built it: a robot dropped on a thing's
own panel set it going, as a robot dropped into a house does. A thing's
panel waits for SPACE now; a house is still set going by the drop.

A thing announces its switch: `[listen | switch | bird]` brings a nest that
gets "on" or "off" whenever SPACE, "." or a `[set | switch | on]` letter
throws it, and `[query | switch | bird]` asks. The stopwatch's Started robot
hears "on", forgets the start, marks the next reading fresh and asks the
number (by the perch) what it shows; Zero sets the start from that reading
and value, so the count goes on from wherever it stopped, and from 0 after a
0 is set. Two things the team rule taught: a thought about an empty nest
WAITS, and a waiting leader stops the whole team -- so Started sends a pad
to the switch nest by its own bird and the nest is never bare; and a box of
more than thirteen holes is drawn with its middle elided, and a nest in an
elided hole is not in the scene, so nothing reaches it -- the box is
thirteen holes exactly.

The timer teacher trains those four robots, the very ones of the devices
world, and needed one more taught step: Dusty on a pupil's thought (the hole
takes anything, or nothing), for the holes a robot must not look in -- the
token in either of two holes. Ruby's loosening had been a taught step; now
both are. A taught pupil stands half size at its desk once its lesson is
over, full size while it learns and works.

The white circle was the perch: its pale stone top, seen from above beside
the desk, read as a disc on a work spot. It has a post like the desks' legs,
a round wooden top, a rim and a plate saying "the perch". The resort's clerk
is a team from the start, and the bell is an announcement: "everybody move
up five", given to the bird "to every guest". And the two lone failures of
the suite were one fault: a step sent sixty times a second restarted the
glide from where the thing was seen, and a star sent across the table by
bouncing crept a ten-thousandth a frame. A step shorter than a finger applies
at once; a step that lands mid-glide extends the glide. The library's star
had also been riding on "bouncing at a speed"; it has a row of its own.

## The slider reaches the voices, who is at the desk, and an empty hole

Ken: "The volume control slider doesn't affect text-to-speech." The effects
are synthesised through one gain node and the slider drove that; speech goes
out through the browser's own engine, and none of the three speaking sites
(a robot's speak action, the hints, Marty) set the utterance's volume. One
`utterance(said)` makes every utterance now, at the slider's setting, and
the suite counts the constructor in the source: once.

"The tooltip could be better given that the robots have names. And if there
are no names either 'the robot' or 'the robots' is better than 'it'." The
drop-on-a-robot lines name whoever will wake -- "Drop that on 'Next address'
and 'Move up five': they wake, grow, and get to work on it -- they know 8
steps between them" -- and say "the robot" or "the robots" for the nameless,
through `botWho(bot)`. The little thought's line with something in your hand
had been the empty-hand line; it says to empty your hand first, since that
is all the click would have said.

"An empty hand pointing to an empty box hole should pick it up when
clicked." It said "That hole is empty". The hole is part of the box, so the
click takes the box; and the robot's empty claw on an empty hole in a lesson
takes the box too, where a take of the hole itself would have aborted the
lesson over nothing being there.

"Testing infinity resort led to the robot not doing anything when given the
nest after starting 'the guests' -- but I tried it 2 more times and it worked
fine except that the old guests didn't move 5 cottages over." Measured in
Ken's order (the guests first, then the desk to the clerk) at 1x: the drop of
the desk on the trained clerk sets it to work at once, letters and all, and
the run button reads Stop from that moment -- so "press Start", as the
problem 1 pad said, was a Stop. Pressed at once it left the clerk doing
nothing; pressed after a round it held the auto-run, and the bell's letters
then woke nobody, which is the guests staying put. The pad says the drop
sets it to work and not to press Start; the checks no longer press it
either. A page that went unresponsive once in Ken's play is not reproduced:
the resort at 1x in that order runs seven minutes clean under the suite.

## The guests are people

Ken: "let's make the guests be a simple model of a person - the two colors
(maybe clothing) are a good idea." A guest was a pad with a name; it is a
model now, built from solid shapes the way Marty builds them (`person(shirt)`
in `make_resort.py`: head, a cap of hair, shirt and sleeves, hands, legs,
shoes), under 0.3 wide since the cottages stand 0.6 apart, with the name on
a plate. The first six wear red, the five who come later blue. Everything
else is as it was: the model carries the guest's `lid` and `evt` like the pad
did, the behaviour is bound to it, and `[set | position | ...]` walks it. The
suite finds guests by label and kind now.

Ken also saw the first guests "replaced by the next 5 - they don't move
first" again. Measured at instant and at 4x, the guests first and the desk
after, the bell rung mid-run and the five more switched on straight after:
the six stand at 6 to 11 and the newcomers at 1 to 5, every time. In Ken's
picture guest 6 still stood at cottage 6, so the clerk had answered nobody's
move: the bell was not rung, or the clerk's auto-run was held by a Stop
(the old "press Start"). The problem 2 pad now says the clerk must be at
work, the button reading Stop, and the checks cover that order.

## The moving office: problem 2 is yours to solve

Ken: "I gave the bird the 'move up 5' message and nothing happened. But also
the point of this activity is the user should come up with the solution.
Something like resort_infinity.htm -- the user for problem 2 trains a robot
that receives [cottage-number | bird] and computes cottage-number+5 and gives
it to the bird. This robot is sent to the clerk who asks each guest for its
number and then runs the robot with the appropriate box."

So problem 2 is the player's again. The shipped "Move up five" is off the
clerk's team and lies by the fence with "Next address", answers for whoever
would rather read one. The player's mover cannot stand at the bench, since
the clerk is working there and the bench holds one working robot -- so it
works in THE MOVING OFFICE, a glass house by the desk whose stand holds a box
with a post of its own. Drop a fresh robot on the office and it steps inside
behind the desk; click the door and the lesson begins on that post (the
lesson-waiting rule), letters on it if the bell has been rung: take the
letter off the post onto a spot, drop a +5 on its number, give the number
to the bird, Dusty takes the empty letter, Ruby loosens the number. Leave,
and it works inside, where you can watch through the glass. The guest's
"Move when told to" now writes [where I live | my own bird] to the office
and throws the bell's pad away, the same letter shape as problem 1's, which
is what Ken asked for.

THE BELL IS A BEHAVIOUR, "ring the bell": one robot that gives every guest
the pad "a move, please" through the bird "to every guest" (every guest's
nest answers to the bell's name as an alias) and then sends [set | switch |
off] to the bird on the perch -- to itself -- so it rings once a press and
can be rung again. The loose bird and the two announcement pads are gone;
Ken did not see why they were there, and now nothing on the grass is a
mystery: two macros, the bell, the desk, the office, the pads, the answers.

Training pads say what nobody had said: a thought is exact at first, so Ruby
must erase the number in it, and letters must lie on the post before a
robot can be taught to take one -- the guests first, then the clerk; the
bell first, then the mover.

Found while scripting the office: a held house dropped on its own door made
a parent its own descendant, and every frame after overflowed the stack --
the shape of a hang. roomDrop refuses a house dropped into itself. By hand
the held thing hides from the pointer, so this is a guard, not Ken's hang;
that one is still not reproduced.

Checks: resortCheck (shipped answers: bell rings once, the mover dropped on
the office, a second ring moves everyone five more), resortLateCheck (Ken's
order, a fresh robot taught inside the office by hand; resortSlow by name at
4x), selfHouseCheck.

And the resort's "order flake" was never the app's: two lesson checks ended
with `D.rounds(0)`, a round limit of nought, so every run after them in the
same tab stopped before its first round -- the clerk answered nobody, the
guests stayed at the gate, and a check waiting six thousand frames for them
looked like a hang. They restore the suite's limit now.

## The resort teacher

Ken: "I still find infinity resort very confusing - can you make a meta
example that solves it." `examples/meta/make_resort_teacher.py`: the resort
in the yard, and at the yard's table a teacher given a thirteen-hole box
that does the whole of it -- the two lessons are the very robots of the
resort's answers, taught step by step. Four things it needed:

THREE ROBOTS, not one: a lesson takes a letter off a post, and letters take
a moment to fly. A robot cannot wait mid-round, but a thought about a post
waits for a letter -- so the teacher is a team: Seat the guests (hole 0
holds the pad; it reads it and has Dusty take it, so never again), Teach
the clerk (a little robot in hole 1 and a letter on the desk's post), Teach
the mover (a little robot in hole 3 and a letter on the office post). Each
takes a turn its predecessor makes possible, and makes it impossible for
itself. A hole a robot need not look in is `null` in its thought, which
matches anything or nothing; a `wild` thought needs something there, and the
team stopped on the vacuumed hole 0 until that was put right. And a member
teaches ITS first pupil: the taught robots are counted per robot, so the
mover's teacher says t1, not t2.

A PAD'S PANEL is where a pupil works, since the bench holds one working
robot and the teacher is standing there: the sign's panel out onto a work
spot, the pupil's box and the pupil on it, the panel folded away. But a pad
in a hole is out of play -- its panel gets no turn -- so the teacher sets
the sign on the grass (a put on `ground` with a spot) before throwing its
switch by mail.

A FOLDED TRAY TOOK A WORK SPOT: putOnBench gives a robot's put-downs a
scratch spot during a run, and a behaviour switched on by mail while the
teacher worked had its hidden tray land on spot 1, where the next lesson's
letter was "set down inside the room". A folded tray is placed as a person
would place it.

THE BELL BEFORE THE ADDRESS: the teacher rings the bell the moment the
clerk is at work, and at Instant the clerk's answers were still in the air,
so the bell's pad lay on TOP of the address on four guests' nests, and
nobody's thought fitted (Stand wants a number on top, Move a place already
set). Two more robots in every guest's machinery: Keep the bell for later
takes the pad off into hole 7, uncovering the address; Move on the bell I
kept moves once there is a place. Their order matters -- a thought looking
at the empty nest waits and stops the round there -- so the kept-pad robot
looks only at holes and comes first, and Move, which looks at the nest,
waits when it is bare, which is how a guest dozes.

And a glide bug the run exposed: thingPlace read the picture, and a
[set | position] that landed mid-glide was treated as a step added to the
old target, so the guests went past their cottages by the trip they had not
yet finished (and stood at z 3.8, the unfinished 1.4 of the walk from the
gate added twice). The place is the glide's target now, and a set is a set.

## The resort the original's way

Ken: "I have the feeling you've made it more complex than it needs to be.
Maybe you can load the original city and the solutions." Loaded and read
(the .cty and .tt files are zips of XML; `examples/infinity/dump_city.py`
prints every robot's thought and actions). In the city the player's Address
Robot receives [guest # | group # | bird] and is two actions -- pick up hole
1, give it to the bird; the Move Robot receives [address | bird], types a 5
onto the address and gives it to the bird; both go in a [Move | Build] box
to the Solution bird. The robots on the back of a pad do the rest: Broadcast
Announcement wand-copies the Announce nest (a copied nest is a broadcast)
and gives the Move robot to the "To old guests" bird; each guest's Find new
address wand-copies it, builds [copy | address, bird] and drops that on a
"local computation" pad, which runs it; Build new cottage does the same per
new guest and loads a truck. The player never touches a nest.

Mine had the player doing the machinery's job -- the desk with its post, the
letter off the post, a spot, Dusty, a house to enter. So: the player trains
a robot on a PRACTICE LETTER [number | bird to the practice nest] and gives
it to a bird, "to the front desk" or "to the moving office". Ken: "go ahead
- a robot could give a trained robot a box but better might be to put them
into a house and turn the house on (which is like trucks). but either should
work I think." The truck it is, and it needed no new step: a robot can take
a new house (newRoom), put a box on it (onto its stand) and put a robot on
it (a robot dropped on a house with a box on its stand sets the house
going). The machinery in each desk house: Run your robot on the letter takes
a fresh house onto a work spot, the letter into it, Mimi's copy of your robot
with a copy of Tidy dropped on it into it, and sets the house down; Take the
robot in moves your robot from its nest into a hole (and the office rings
the bell then). Tidy's thought fits the letter once your robot has taken its
number; it sweeps the letter away, and a house whose robot has swept its box
away folds itself up (retireRoom), so the grass is clear again.

What it took, each measured:
- YOUR ROBOT'S OWN NEST. A nest is a queue with the oldest on top, so a
  robot given after six letters was never seen; the bird "to the front
  desk" delivers to a nest of the robot's own.
- RUN FIRST. A team stops at the first member whose thought waits on an
  empty nest, and once your robot is in its hole, its nest is bare for good:
  with Take in first nothing behind it ever ran.
- A ROBOT IS A LETTER TOO: a held robot dropped on a bird was "Robots only
  team up with other robots"; it flies to her nest now.
- A ROBOT ON A ROBOT BY A CLAW IS A TEAM, as by your hand (combine refused
  it and left the second robot on the bench): that is how Tidy rides behind
  your robot's copy.
- A HOUSE HAS NO FLOOR OF ITS OWN: a robot inside it that sets a thing down
  on "the ground" sets it on the grass (or the table); the refusal "there is
  no ground in here" now applies only outside houses. The runner houses
  appear on the grass for a moment and fold away, like the trucks.
- A FOLDED TRAY TAKES NO ROOM: placed invisible, it neither shoves what
  stands there nor grows the yard (thirty hidden trays of the guests did
  both, and "The yard grows to make room" said so).
- THE LITTLE ROBOTS IT TAUGHT ARE THE WORLD'S: taughtNow is stashed with the
  world context. A desk house taking its turn started a run of its own and
  emptied the teacher's list -- "the second little robot it taught" was
  gone the moment a desk woke to the first (at 4x; at Instant the timing hid
  it).
- IN A LESSON, RUBY'S JUDGMENT IS AGAINST WHAT THE ROBOT WAS SHOWN, not the
  desk as it is mid-lesson (the number had been given away, so "still not
  what is on its desk" after loosening the very number).

The resort teacher is one robot again: it teaches on the two practice
letters in its box, puts each letter back (a desk left aside with a box on
it holds the houses still), and gives each pupil to its bird. The moving
office, the bell pad, the by-hand office lesson and the three-robot teacher
are gone. Kept: the guests' kept-bell robots (a bell before an address still
happens, since the office rings the moment your robot arrives).

## A named thing is introduced by its name

Ken, over the bird whose plate read "to the moving office": "the tooltip
should mention the label if the bird has one - there are probably other
tooltips that should be enhanced similarly." Boxes and models led with their
names; birds, nests, numbers, houses and the rest did not. `withLabel` wraps
every thing's tip now: a named thing's line begins with its name -- "to the
moving office" -- a bird -- drop something on her... -- unless the line
names it already. Covered in robotTipCheck.

## The mist

Ken: a cloud obscuring cottages 12 and up, so the resort is seen to go on
for ever rather than told so by a pad. The mist is a model of eighty
see-through puffs from just past cottage 11 to the fence, thin at its near
edge (opacity 0.14) and thicker with every step in (0.46 at the fence),
over the row and the guests' line in front of it; cottages 12, 13 and 14
stand inside, real houses half-seen, and a guest sent further walks in and
is lost to view. A model part may carry `opacity` now: it is drawn unlit
(lit, the puffs were a heap of shaded grey balls), without writing depth,
casting no shadow (vapour throws none) -- and the overlap check already
left parts under half opacity out of a thing's footprint. The mist is a
ghost, so the guests walk through it, and stuck, so a hand cannot carry the
weather away. The fence pad says what the mist shows.

## Codex's report, the first four

Ken had ChatGPT Codex test the workshop (17 September). Done from it:

- A ROBOT IS NOT SET GOING BY A LOOSENING (#4). Ken: "the robot should not
  start running as soon as Ruby has erased enough that it matches. The user
  may intend to erase multiple things and if so it is much easier if the
  robot waits for the start button." Ruby's and Dusty's erasures no longer
  arm an auto-run; the card says "It fits what is on its desk now: Start
  runs it", with attention, since the refusal that held the card would
  otherwise stay in front of it; and the run Start then begins is still
  watched from a distance with Ruby in view. The first project's step says
  so. (Deliveries still wake a dozing robot: that is post, not a loosening.)
- A FRESH NUMBER TAKES ITS FIRST DIGIT (#3). The stack's 1 typed 2 gave 12.
  A number just off the stack is `fresh`; the first digit replaces it, the
  next digits add on, Backspace takes one off, and any other change to its
  value ends the freshness. The manual says so.
- ENTER (#5): the manual said Enter for a new line; it is Shift+Enter, and
  Enter looks at the pad close up.
- THE LOADING OVERLAY (#6) is aria-hidden and display none once the scene
  is up, not merely faded.
- The manual's little workshops open with a line about the experiment in
  front of the reader, not "take a little robot".
Covered in codexCheck; rubyView and thoughtView press Start after Ruby now.

## Four of Ken's, after the Codex round

- DIGITS GO ON THE END, and stay so: Ken: "revert #3 and instead fix the
  manual so picking up a 1 and typing '2' results in 12." The fresh-number
  rule is gone; the manual says a 1 typed 2 is 12 and Backspace takes the
  last digit off.
- ENTER IN THE CLOSE-UP WRITES. Ken: "when in closeup mode a second Enter
  restores the camera... it should just make multi-line text. And
  control-enter restores the camera." A pad filling the screen is a page
  being written on: Enter there is a new line; Ctrl+Enter, like Escape,
  comes back; on anything but a pad in the hand a second Enter still comes
  back, since there is nothing to write. Shift+Enter is the new line
  anywhere.
- PAUSE IS THE ROBOTS'. Ken: "pause should stop all robots but I don't see
  why it should stop anything else." Movers, touches and the yard's sweeps
  no longer stop with it, and a PAUSED RUN keeps the world's clocks going
  while the robot's steps wait (before, a paused replay froze birds, glides
  and balls too). The button, the message and the manual say so. The suite
  drives the close-up's own clock by hand (holdLook), since it lives in the
  render loop.
- A LETTER NOBODY UNDERSTOOD IS SAID SO, EVEN FROM INSIDE. Ken: "If a
  message is given to a thing's bird that isn't properly formed or spelled
  there should be some kind of error feedback." There was, for a hand's
  letter -- and none for a robot's, because a robot works inside a house or
  a panel and say() is silent offstage. Every complaint about a letter
  (placeMsg, lookMsg, switchMsg and the kinds' own refusals) goes through
  mailSay/mailRefused now: "The target did not understand [set | positon |
  2] -- the letter is dropped. It answers ...", kept while a house has the
  stage and said the moment the stage is yours, once per wording every few
  seconds. The stale "Only numbers, pads and sounds answer messages" is
  gone: every thing answers the place messages.
- A TURNED TRAIL STANDS ON THE TABLE. Ken's spiral, a 3D turtle's trail with
  a quarter turn in its aim, set down after Dusty had it, ran into the
  table: its rest of four millimetres assumed it lay flat. putOnBench
  measures a turned trail or model after the turn and lifts whatever hangs
  below the top.
Covered in kenRoundCheck.

## Small screens, the first project in the workshop, the home view

From Codex's report, with Ken's go-ahead. SMALL SCREENS: every card keeps
inside the window and scrolls inside itself; Marty's panel stands above the
bar, not on it; below 600px wide the two top cards share the width in one
column (the actions card under the title, above the bar); in a short
landscape (under 460px tall) the title keeps to 250px, Marty's panel goes
between the cards, and the log shrinks. Measured at 390x844 and 844x390 by
DOM geometry: nothing overlaps, every close button is inside the window.
Not a phone app -- reading and simple play.

THE FIRST PROJECT, in the &#8942; menu: the manual's first project, step by
step. The workshop watches what you do rather than what you click -- a robot
on the table, a lesson begun, a put recorded, the bubble left, a run of one
round, a thought loosened, a run that counts -- and says each step as the
one before is seen to be done, with a ring of light on the stack or helper
to reach for. Nothing is done for you.

THE HOME VIEW: a button on the bar and the Home key put the camera back
where it starts for wherever you are -- the whole table, or the whole yard
-- out of any close-up first, and the smart camera's slate wiped so it
takes up from there. (Ken asked whether a reset-camera button was a good
idea: yes, and this is how it works.) And "As big as the ground" reads "As
big as the table" indoors (Ken).


## A saved arrangement loads exactly

ChatGPT, after building three worlds by script: "Automatic separation moved
pots away from stems and the fountain nozzle away from its launch point.
Saved arrangements should survive loading exactly." Measured: its garden's
three pens, saved in their pots, stood a row behind them after every load.
The shove (clearBenchSpot) was for a hand's near-miss and for what the stacks
hand out, and it ran on every put-down, loading included. Now a world file's
things -- and undo's -- go exactly where the file says, clamped to the table
and nothing more; a hand's drop still keeps clear. Our own examples: only
the library had two things on one spot (reverse a speed on collision stood
on reverse on collision), moved apart in make_library.py. Covered in
exactLoadCheck. (Its "against the edge" advisory during the garden's initial
positioning did not reproduce here in 667 rounds; it is the shape of the
mid-glide measurement fixed on 17 September -- [set | position] measured
from a glide's old target -- and its test ran on the public site that day.)

## A model's plaque is measured to the model

ChatGPT: "the planet labels were large compared with the planets and
obscured the animation." A model's name plate was 0.3 wide whatever the
model -- a box's is never wider than the box, and now a model's is the same:
no wider than the model and a little (1.3x), never narrower than 0.12, which
is as narrow as reads up close. Measured: a pea of a planet 0.1 across wears
a 0.13 plate; a shed keeps 0.3. Covered in modelPlaqueCheck. Hover already
begins with the name (the named-things round), so a plaque can be small.
