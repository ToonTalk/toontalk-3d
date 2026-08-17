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
- **A stack of miniature robots.** Set a mini on the table and drop something on
  it: it grows to full size, steps behind the bench, and takes what you gave it.
  Click a full-size robot to shrink it back into your hand — it keeps all its
  training. Drop one trained robot on another to form a **team**: given
  something, the first member whose condition matches takes the pass, so a team
  of "on a 5, double it" and "on a 10, add 3" turns a 5 into 13 and stops.
- **You move things; the robots don't.** In the workshop you pick things up
  and put them down anywhere on the bench — what you carry follows the pointer.
  A robot only ever acts inside its thought bubble, or when repeating what it
  learned.
- **A robot's actions name its own containers, never places in your world.**
  Every step is an address like *hole 1 of what it was given* or *hole 2 of
  spot 1* — the given thing, a scratch spot, or a copier surface, then hole
  indices. A trained robot therefore generalises to anything of the right shape
  for free, and can even pick up the whole thing it was given and hand back
  something built around it. Your bench is off limits to it.
- **A private work area.** Inside its thought bubble the robot has scratch spots
  and the copier to work with. That is safe where naming your bench would not
  be: the area belongs to the robot and starts empty on every run, so it cannot
  collide with your world or carry state between runs. Everything left there is
  vacuumed when the robot is done, and whatever it was given goes back on the
  table — changed, if the robot changed it.
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
- **A copier** with two surfaces: originals go on the upper platform and are
  scanned there, copies are delivered to the lower tray. Copies are independent
  deep copies — boxes come back with their contents duplicated, not shared.
  A robot copies too, but names a hole rather than the machine: arm the copier,
  then point it at what to copy.
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

- The robot no longer walks: its stand sits exactly where its claw reaches.
- The robot's scratch area is three fixed spots rather than free placement.
- When a robot uses the copier the object flies between claw and platform: the
  upper surface is above the claw's working height and there is no arm IK.
- `^` takes integer exponents only. Results are unbounded BigInts; the only
  limit is a guard that refuses a power whose size is estimated past 20000
  digits, so a runaway loop cannot lock the browser mid-calculation.
- The condition matches structure, values and operations, with wildcards — but
  you cannot yet express "any box" or constrain a number's range.
- One robot. No teams, no birds, no nests.
