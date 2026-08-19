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
