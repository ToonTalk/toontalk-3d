# Sounds

Three worlds, smallest first. Load one with **Import file** (or drag the file
onto the page). Each lays its instructions on the table as ordinary pads —
vacuum them away with Dusty once you know the drill.

A sound is a little speaker lying face-up: a walnut cabinet with a black
baffle, a woofer, a tweeter, and a screen showing the waveform it holds. What
it holds is a list of **segments** played one after another, and a segment is
either a made tone — a frequency, a duration, a waveshape — or a recording.

**Turning things on.** ToonTalk's own convention came over with these: press
**space** to turn on whatever is in your hand or under the pointer, and **`.`**
to stop it. For a sound that means play and stop; for a house or a panel it
means set the robot inside working, and stop it. Picking a sound up does *not*
play it.

## tones.world.json

Where a sound comes from. A sound arrives **silent** — a flat line on its
screen — and is made by dropping a `[frequency, seconds, shape]` box on it: the
number is hertz, the fraction is how long, the pad is one of `sine`, `square`,
`sawtooth`, `triangle` (anything else reads as sine).

The recipe box is an ordinary box, so the four shape words are laid out as pads
to swap into its third hole, and the frequency is a number you type on. Two
speakers hold the same note in two shapes, to hear the difference side by side.

Regenerate with `python make_tones.py`.

## transforms.world.json

Arithmetic you can hear. A sound answers `×` and `set`, and **refuses `+`** —
adding to a sound has no meaning, and the refusal says so.

- `×2` plays it twice as fast: an octave up, half as long.
- `×½` stretches it the other way.
- `×-1` plays it **backwards**.

That last one is the world's point. Nobody wrote a reverse operation: it is the
same minus sign that makes a number subtract, applied to a thing whose axis
happens to be time. Four copies of one rising phrase are laid out with the
three numbers to drop on them; they stack, so a phrase can be sped up *and*
reversed.

Regenerate with `python make_transforms.py`.

## melody.world.json

The first program here. **Singer** is handed
`[pitches, the tune, a blank sound, a recipe]` and each round it

1. copies the blank sound and the recipe onto two work spots,
2. takes the next pitch off the nest and drops it into the recipe's **empty
   frequency hole** — an empty hole takes what it is given, where a hole that
   already held a number would *add*,
3. drops the filled recipe on the copied sound, which makes it sing, and
4. joins the result onto the right edge of the tune, the same gesture that
   joins two pads into a word.

Its thought is `[any number, anything, anything, anything]`, so it knows no
notes. Give it the work box: a C major scale grows a note
at a time, playing as it goes, and then the robot shrinks and dozes on the bare
nest waiting for another pitch.

Then change it. Write `square` over `sine` in the recipe — same tune, new
instrument. Type other numbers onto the pitches — different tune, same robot.
Drop a `×-1` on the finished tune to hear the scale run backwards.

Regenerate with `python make_melody.py`.

## Recordings

Drag a `.wav`, `.mp3`, `.ogg`, `.m4a`, `.flac` or `.aac` onto the page and it
arrives on a speaker **where you dropped it**; drop it on a speaker that is
already there and it replaces what that one holds. A recording joins and
transforms exactly as a made tone does — `×-1` reverses it sample by sample —
but no `[frequency, duration, shape]` box will remake it, and its info notebook
does not offer one.

None of these three worlds carries a recording, because a world file carries
its sounds inline and a second of audio is larger than every example here put
together.

## Writing another one

`_snd.py` holds the shared vocabulary: `seg`, `sound`, `silent`, `tone_box`,
`NOTES` (equal temperament from A440, rounded to whole hertz) and `note`. It
imports `../infinity/_tt.py` for the rest — boxes, nests, robots, steps.

Two things to know when laying a bench out:

- The workshop's own notebook sits at about `x 0.95, z 1.33`, so keep a world's
  own things left of `x 0.45` or the bench will shove them aside.
- A nest serves its **oldest** arrival first, and a hand-written `pile` is read
  as newest-first — so write a queue last-item-first, as `melody` does with its
  scale.
