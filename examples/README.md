# Examples

Saved worlds. Load one with the **Import file** button (or drag the file onto
the page).

## sentence-generator.world.json

A random-sentence factory — the first program to use the recursion-era pieces
(dice, robot teams branching on a roll, a room working while you do something
else).

A glass room called **Scriptorium** holds a team of twenty robots and their
state box; a nest sits outside on the table. Pull the big lever on the room's
right wall and sentences start arriving on the nest, one text pad each:

> the frog dreams of the witch.
> the cat chases the robot.

**How it works.** The state box holds a phase number, a die-roll slot, the
sentence under construction, two dictionary boxes (six nouns, six verbs), a
bird, and the pads "the" and ".". Each round exactly one team member's
thought matches the box:

- **Scribe** (phase 0) copies "the" into the sentence, throws a die onto the
  roll slot, and advances the phase.
- **noun1-1 … noun1-6** each match one roll and copy their noun onto the
  sentence's right edge, then roll again.
- **verb-1 … verb-6** append their verb (each ends with "the"), roll again.
- **noun2-1 … noun2-6** append the second noun.
- **post** appends ".", hands the finished sentence to the bird — who flies
  it out of the room to the nest — and resets the phase, so the whole team
  starts over.

Five rounds per sentence; the Rounds control decides how many the room makes
per pull of the lever. Open the door to walk in and watch, or click the roof
to make the walls opaque and let it work in private — the chimney smokes
while it's busy.

Regenerate the file with `python make_sentence_generator.py`.

## fibonacci.world.json

Doubly-recursive Fibonacci — the recursion stress test. fib(n) is computed
as the number of leaves of the call tree, so no reply channels are needed:
every leaf mails a **1** to one shared nest, and their sum is the answer.

The work box holds `[n, bird, spare-robot, empty, empty]`. Hand it to the
**Fib** robot:

- **leaf-1** and **leaf-2** (matching an exact 1 or 2) mail a 1 to the bird
  and empty the number hole, which stops the team.
- **branch** (matching any other number) drops a "−1" pad on n, carries the
  whole box to Mimi and takes the copy; does it again for n−2; then builds
  two rooms, installs a copy of the spare robot in each, drops one copied
  box into each, and stows both rooms in its own box's last two holes.

The box comes back to the table carrying two smoking rooms — the two
recursive calls — and each room's robot does exactly the same thing one
level down. For n = 8 that grows 40 rooms nested 6 deep, and 21 ones land
on the nest. When the smoke stops, hand the `[0, nest]` box to **Sum**: it
moves the pile onto the total one a round (dozing whenever the nest is
bare) and the total reads **21**.

Regenerate with `python make_fibonacci.py` (edit `N` for other inputs;
keep the room-nesting depth n−2 within the engine's cap of 12).

## bank-account.world.json

A message-passing bank account. The account is a box `[balance,
request-nest]` worked by the **Teller**. A request is a box `[amount,
reply-bird]`: drop one on the request bird (labelled *requests*) and she
files it on the teller's nest. The dozing Teller wakes, moves the amount
onto the balance — a negative amount is a withdrawal — sends a *copy* of
the new balance home with the request's own bird, vacuums the emptied
request away, and dozes again. The nest labelled *statements* piles up the
balance history.

Hand the account box to the Teller first (it dozes: the nest is empty),
then feed requests to the bird. Copy a request on Mimi for more — a copied
bird serves the same statements nest. Watch the Teller shrink to doze and
spring up whenever mail lands.

Regenerate with `python make_bank_account.py`.
