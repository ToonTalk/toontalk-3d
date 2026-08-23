# Exploring Infinity

Ports of the **[Exploring Infinity](https://toontalk.github.io/tt-wasm/tt-wasm/build/infinity/index.html)**
activities — eight sessions on the cardinality of infinite sets, written for
ToonTalk and the WebLabs project. Load one with **Import file**.

The mathematics is Cantor's and the activity design is Ken Kahn's; what is new
here is the ToonTalk 3D construction, which differs from the original in one
structural way described under *Rooms* below.

## The worlds

| File | Activity | The question |
|---|---|---|
| `activity1-even-numbers` | 1 | A proper subset the same size as the whole |
| `activity2-all-integers` | 2 | Making all the integers, and counting them |
| `activity3-sequences-and-pairs` | 3 | Every sequence you can build is countable |
| `activity4-all-fractions` | 4 | The obvious enumerations fail; this one works |
| `activity5-above-one` | 5 | Reciprocals, and a one-to-one map falls out |
| `activity6-all-rationals` | 6 | Merging to get all of them — the capstone |
| `activity7-any-interval` | 7 | Scale and shift the unit interval; density |

Each is self-contained: set **Rounds**, pull the **lever** on the first room,
and the whole pipeline runs. Everything else is already dozing in its own room
waiting to be woken. The two text pads say what it does and what to ask.

## The robots

Every one of them is the same shape — a box of *somewhere to read from* and
*somewhere to write to* — and each is three to nine steps long.

| Robot | Box | What it does |
|---|---|---|
| Add 1 | `[n, bird]` | hands over `n`, then adds 1. The naturals, forever |
| Doubler | `[nest, bird]` | `n` → `2n` |
| Split | `[nest, A, B]` | alternates, by **swapping the two birds** each round |
| Negator | `[nest, bird]` | `n` → `−n` |
| Merge | `[nest, nest, bird]` | alternates, by **swapping the two nests** |
| Squares | `[nest, bird]` | `n` → `n²` |
| Match Maker | `[nest, count, bird]` | hands out `[count, term]`, then counts up |
| All Fractions | `[scale, bird]` | a team of two; see below |
| Box to Number | `[nest, bird]` | `[a, b]` → the single number `a/b` |
| Divides 1 | `[nest, bird]` | `n` → `1/n` |
| Add 10, Halve | `[nest, bird]` | one number dropped on each term |

Two of them are worth looking at twice.

**Split and Merge keep no counter.** Split gives the number to whichever bird
is in hole 1 and then swaps the two birds over; Merge gives away what is on the
first nest and then swaps the two nests. The swap *is* the alternation. There
is no state anywhere but the position of the things in the box.

**All Fractions branches on a scale.** Its box is
`[scale weighing numerator against denominator, bird]`, and a scale's two pans
are addressed exactly like box holes. While the scale tips towards the
denominator, *Next Numerator* matches and runs. When the numerator catches up
and the scale **balances**, that condition no longer matches, so the team falls
through to *Next Denominator*, which sets the numerator back to 1 and takes the
denominator up one. Nobody counts anything: the scale is the entire
conditional, and you can watch it tip.

## Rooms

In the original, robots run concurrently as a matter of course. Here, only one
robot can stand at the **open bench**, and a robot dozing on an empty nest keeps
that place until somebody picks it up — so a pipeline built in the open would
have to be run a stage at a time, by hand.

So **every robot lives in its own room**, the source included. A room is a
workshop of its own: the robot inside dozes at its own desk, wakes when a bird
delivers through the roof, and never competes for the bench outside. One pull
of a lever then drives a five-room pipeline, as in Activity 6. The source
room's lever is down when the world loads; pull it to start.

Building these was what turned up the fact that houses only worked while the
world outside was completely still — so a robot running on the bench froze
every house on the table until it stopped, and then they all caught up at once.
That is fixed: houses now run while you work, and while each other works, as
they always did in the original. Putting the source in a room as well is a
choice rather than a workaround — it makes every stage the same kind of thing,
and one lever starts all of them.

The rooms are glass, so you can watch. Click a roof to make it solid and it
runs at Instant speed instead; click the door to walk inside.

One idiom does the rest of the wiring: **a bird delivers to every nest that
answers to her name**, so two nests written with the same identity are one nest
in two places. That is how Activity 1 feeds Doubler and Split from a single
Add 1 without either taking terms from the other.

## What is not here

**Activity 8, Cantor's diagonal.** The Diagonal team needs the *n*th term of
the *n*th sequence, and a robot's addresses here are fixed paths — it can say
"hole 1 of what it was given" but not "the *n*th one". Building it would mean
a robot team that walks a growing box of nests, discarding terms as it counts.
Possible; not done.

**Resort Infinity.** Hilbert's hotel as a city of five problems. It depends on
ToonTalk's cities and on houses used as an addressing scheme, which this
workshop's rooms do not reproduce.

**No Copies**, which drops the duplicate fractions (`2/6` never gets past,
because `1/3` already did). Run Activity 4 and you will see the duplicates it
exists to remove — `2/4` after `1/2`, `3/6` after `1/2` again. Detecting them
needs a robot that remembers everything it has seen, which is a notebook and a
lookup, and is a good exercise rather than a finished world.

## Rebuilding

```bash
python make_activity1.py
```

Each generator writes its own `.world.json`. `_tt.py` holds the shared
vocabulary — things, conditions, steps, and the `room()` helper.
