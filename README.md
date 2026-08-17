# toontalk-3d

An experiment in rebuilding [ToonTalk](https://en.wikipedia.org/wiki/ToonTalk)'s ideas with real 3D
assets rather than the original's pre-rendered sprites — and in seeing how far
LLM-driven asset creation can carry a project like this.

Nothing here tries to copy the original's artwork. The characters are new
designs, generated from Blender Python scripts rather than modelled by hand.

## What works today

`nano-toontalk.html` — a small but complete programming-by-demonstration loop:

- **Numbers and boxes.** Numbers come off an infinite stack. Boxes have holes;
  a hole holds a number *or another box*, so structures nest. Type a digit on a
  held box to give it that many holes (up to 8) — the holes shrink rather than
  the box growing off its pillar.
- **Exact arithmetic.** Numbers are BigInt fractions in lowest terms. Type
  digits to set a value and `+ - * / ^` to set what a number *does* when
  dropped on another; each operation colours the block and shows a badge.
  Division gives a real fraction, not a float. Numbers too long to fit render
  the ToonTalk way — full size at both ends, tapering to an ellipsis in the
  middle — so the most and least significant digits both stay readable at any
  length. Numerators and denominators are laid out independently.
- **A robot library.** Name a trained robot and save it; it persists in
  `localStorage` and reloads with its condition and actions intact.
- **A robot that walks the bench** and picks things up with a two-jaw claw.
- **You move things; the robot doesn't.** In the workshop you pick things up
  and put them down yourself — what you carry follows the pointer. The robot
  stands idle and only ever acts inside its thought bubble, or when repeating
  what it learned.
- **Training starts by giving.** Hand something to an untrained robot and it
  goes into its thought bubble to learn on it; from then on you direct the
  robot and everything it does is recorded. Leaving the bubble rewinds the
  world — the daydream was never real. Giving a *trained* robot something is
  just handing it work to run on.
- **A condition.** The robot records the exact thing it was trained on and will
  only run when given something that matches. It is shown as a thought floating
  above the pad.
  Refuse a run and the offending parts glow red in the bubble.
- **Dusty the vacuum** erases parts of that condition into wildcards (`?`),
  which is what turns a one-off into something general.
- **A copier.** Put anything on it and it produces an independent deep copy —
  boxes come back with their contents duplicated, not shared.
- **Running.** The robot repeats its trained actions on whatever it is given,
  and *keeps* repeating while its condition still holds — so a loop is just a
  condition that stays true.

`robot-demo.html` — the earlier standalone pick-up-and-put-down demo.

## Running it

Needs any static server; the repo assumes port 8311.

```bash
node serve.js 8311
```

Then open <http://localhost:8311/nano-toontalk.html>.

`serve.js` also accepts `POST /capture`, which the pages use to write rendered
frames to `captures/` — that is how the 3D work gets reviewed without a human
having to eyeball every change.

## Assets

The `.py` files are the source of truth, **not** the `.blend` files: each one
regenerates its model, its turntable renders and its `.glb` from scratch.

```bash
blender --background --factory-startup --python robot_v4.py
blender --background --factory-startup --python dusty_v1.py
```

Edits made in Blender's GUI will be overwritten by a re-run, so fold anything
worth keeping back into the script.

## Known limits

- The robot pivots and walks, but has no path-finding; stations are a fixed row.
- `^` takes integer exponents only. Results are unbounded BigInts; the only
  limit is a guard that refuses a power whose size is estimated past 20000
  digits, so a runaway loop cannot lock the browser mid-calculation.
- The condition matches structure, values and operations, with wildcards — but
  you cannot yet express "any box" or constrain a number's range.
- One robot. No teams, no birds, no nests.
