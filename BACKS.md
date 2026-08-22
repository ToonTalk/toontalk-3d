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
   bird: **1–2 days**. Sounds: **+1 day**. Video: later.
4. **Devices notebook** — **half a day to a day**.
5. **Inexact numbers** — flag, contagion, fixed-precision trig/powers,
   the visual marker: **1–2 days**.

Total: **roughly 6–9 working days**, comparable to the rooms-and-engine
epic. Natural order: 1–2 first (the semantics), 3 second (the payoff),
4–5 after.

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
- Pictures' full verb vocabulary.
- What a live number shows before its first delivery.
- The exact look of inexact numbers (that they look different is settled).
