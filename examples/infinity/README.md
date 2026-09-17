# Exploring Infinity

Ports of the **[Exploring Infinity](https://toontalk.github.io/tt-wasm/tt-wasm/build/infinity/index.html)**
activities — eight sessions on the cardinality of infinite sets, written for
ToonTalk and the WebLabs project. All eight are here. Load one with **Import
file**.

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
| `activity8-counting-sequences` | 8 | Cantor's diagonal: the sequences are not countable |

Each is self-contained: pull the **lever** on the first room — and pull it
again when you have seen enough —
and the whole pipeline runs. Everything else is already dozing in its own room
waiting to be woken. The two text pads say what it does and what to ask.

Activity 8 is the exception: there you hand the sequences in yourself, one box
at a time, and its rooms start stopped. Give a box to the **All Sequences**
bird first and pull that room's lever after — the team takes a sequence in as
it arrives and counts from its first term, so a row that has already begun
would be counted from the wrong place.

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
| Diagonal | `[nest, nest, scale, bird]` | a team of three; see below |

Two of them are worth looking at twice.

**Split and Merge keep no counter.** Split gives the number to whichever bird
is in hole 1 and then swaps the two birds over; Merge gives away what is on the
first nest and then swaps the two nests. The swap *is* the alternation. There
is no state anywhere but the position of the things in the box.

**The Diagonal team counts to the term it wants.** A robot here says "hole 1
of what I was given", never "the *n*th one", so the *n*th term of the *n*th
sequence cannot be addressed — it has to be walked to. Its box is
`[Sequences, Current, scale(skipped | to skip), bird]`, and the scale's three
states are the three robots:

| tilt | robot | what it does |
|---|---|---|
| towards *to skip* | Skip a term | takes a term off Current and vacuums it; one more skipped |
| balanced | Hand one on | this is the term: to the bird. Then *to skip* up one, and *skipped* one higher still, which tips it over |
| towards *skipped* | Next sequence | drops the finished sequence, takes the next box off Sequences, puts its nest in Current, sets *skipped* to 0 |

No counter anywhere but the scale, and each robot dozes on exactly what it
needs — Skip and Hand one on look *through* Current for a number, Next
sequence looks through Sequences for a box — so the diagonal waits politely
between sequences. Measured on the three rows the world ships with (`1 2 3 4`,
`1 3 5 7`, `1 2 4 8`) the diagonal reads 1, 3, 4.

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

**Resort Infinity, problems 3 to 5.** Problems 1 and 2 are built (see
`🏨 resort-infinity` below). The last three are the same machinery with
different arithmetic: a second infinite group (move robot doubles, newcomers
take the odd addresses), three groups at once (times four), and infinitely
many groups (double, then walk the diagonal of the square of new guests —
which is Activity 6's merge, or Activity 8's diagonal, standing on grass).

**No Copies**, which drops the duplicate fractions: `2/6` never gets past,
because `1/3` already did. Run Activity 4 and you will see the duplicates it
exists to remove — `2/4` after `1/2`, `3/6` after `1/2` again. Detecting them
needs a robot that remembers everything it has seen, which is a notebook and a
lookup, and is a good exercise rather than a finished world.

## 🏨 resort-infinity.world.json

Hilbert's hotel, in the yard. You are the clerk; a cottage is a house standing
on the grass and an address is a place along the row, so *making room* is the
whole row shuffling up where you can see it.

**One nest each, which is the whole design.** A robot team stops at the first
member whose thought is waiting on an empty nest — that is what dozing *is* —
so nobody here may doze on two nests. Everything a guest hears arrives on one
nest of its own, under its own name *and the bell's* (a nest may answer to
more than one name: `aliases`), and everything the clerk hears arrives on one
nest on the desk. A guest is a little person of solid shapes with a name
plate, red-shirted for the first six and blue for the five who come later,
and its robots move it. What lands says who runs:

| the nest | what lands | who runs |
|---|---|---|
| a guest's | a number | *Stand at my address*: work out `x = n × 0.6 − 4.5` and tell my cottage to stand there |
| a guest's | a pad | *Move when told to*: the bell; write `[where I live \| bird]` to the moving office |
| the desk's | `[number \| bird]` | the clerk: a new guest asking where to live |
| the office's | `[number \| bird]` | the mover: a guest already housed, asking where to move |

Each cottage carries its own robots — the macro pad **the guests** holds one
behaviour per cottage, and one press of SPACE starts all six. That is the
resort's machinery, and the visitor never touches it. What is *theirs* is the
arithmetic, and the point of the activity is that they come up with it: a
three-step robot at the desk that gives a guest their address (problem 1),
and a robot that adds five (problem 2). The second works in the **moving
office**, a glass house by the desk with a post of its own, because the bench
holds one working robot and the clerk is standing there: drop a fresh robot
on the office, go in, and the lesson begins on the office post. **Ring the
bell** is a behaviour: SPACE on it gives every housed guest the pad "a move,
please" through the bird *to every guest*, then switches itself off by its
own perch bird, so it rings once a press. Both answers, *Next address* and
*Move up five*, lie by the fence for whoever would rather read one.

Problem 1: six guests house themselves at 1–6. Problem 2: ring the bell, and
the six ask the office where to go and shuffle to 6–11; then the five
newcomers take 1–5. Eleven cottages, no two at the same address. Set the
speed to 4× or 8×: eleven round trips at walking pace take a while.

`make_resort.py` writes it.

## Rebuilding

```bash
python make_activity1.py
```

Each generator writes its own `.world.json`. `_tt.py` holds the shared
vocabulary — things, conditions, steps, and the `room()` helper.

## 📮 zeno.world.json

Zeno's postman: the halver copies its fraction to the bird and drops a x1/2
badge on what is left; the totaller takes each delivery off the nest and
drops it on the running total (a number dropped on a number ADDS). Pull both
levers. The total is exact -- (2^k - 1)/2^k, readable off the block -- which
is the whole argument for exact rationals in one world.

`make_zeno.py` writes it (moved here from `behaviours/` on 13 Sep: Zeno's
postman is an infinity too, and reads best beside the others).
