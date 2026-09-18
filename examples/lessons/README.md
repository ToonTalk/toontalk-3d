# Lessons: three small drawing programs

Three lessons written by ChatGPT (18 September 2026) as simpler versions of
three programs it had generated before, kept here as it wrote them -- the
robots, the boxes, the notes and this guide are its, lightly edited for the
move. Learn the planet first, then the flower, then the spark. The generator
is `make_lessons.py`; run it to rebuild the six files.

| world | what it teaches | robots | biggest robot | work box |
|---|---|---|---:|---:|
| 🪐 `step-and-turn-planet` | repeated motion: walk a little, turn a little, and a ring appears | step and turn; rest at zero | 8 actions | 4 holes |
| 🌸 `easy-flower` | a repeat inside a repeat: four sides make a square petal, six petals make a flower | go out to the petal; draw one side; back to the centre; draw the stalk and rest | 12 actions | 5 holes |
| ✨ `jumping-spark` | a movement amount that changes over time: the upward step shrinks each jump | fly one step; hide and rest | 10 actions | 5 holes |

No trigonometry, no long setup robot, no library of templates: ordinary
robots, boxes, numbers and birds.

## Open and explore

1. Open a **fresh** workshop (Free play) and **Import file** one of the
   `.world.json` files here. Into a busy workshop a world file lands as a
   notebook instead of opening.
2. Marty says what the world is. Choose **Instant** to see the result at
   once, or a slower speed to watch the robots work. Press **Start the
   robot**.
3. Press **Start this world over** before running again or experimenting:
   the last robot puts the work box away, so pressing Start again is not a
   fresh run. (To change the numbers first, take the work box off the desk
   before it is put away, or open a fresh copy of the world.)
4. Click the condition line above *Trained actions* to see the next robot in
   the team. Each robot carries a note saying what its job is.

## What the three programs share

A team shares one small work box. A number counts how much work is left. A
bird delivers letters to the thing on the table. A smaller box keeps the
letters together, each hole labelled with what the letter does.

Sending a letter takes two robot actions: **copy the letter**, then **give
the copy to the bird**. The original letter stays in its box for the next
turn.

The team tries its robots in order. The finishing robot goes first: it
recognises **zero**. Otherwise a working robot takes a turn. This is why
zero must be checked before "any number". The finisher uses Dusty to put
away the work box, and that ends the program.

The thing on the table is a small sphere. The robots make the drawing; there
is no hidden animation.

## 🪐 A step-and-turn planet

**The idea:** walking forward a little and turning a little, over and over,
makes a ring.

The work box has four holes:

| hole | what it holds | why it is there |
|---|---|---|
| 1 | 36 steps left | counts down to zero |
| 2 | planet bird | delivers letters to the blue sphere |
| 3 | letters | pen down, forward 0.06, turn 20°, pen up |
| 4 | −1 | counts one step |

**Step and turn:** put the pen down → walk forward → turn 20° → add −1 to
steps left. **Rest at zero:** lift the pen → put away the work box. The
workshop counts 37 rounds: 36 steps and the finisher's one.

Eighteen turns of 20° make a full turn, so thirty-six steps go twice round
the same ring. The sun stays still: this is a drawing recipe, not gravity.

**Try:** change steps left to 9. Predict how much of the ring will be drawn.
Then try 18. Changing the turn changes the ring's size and centre too; the
sun will not move to the new centre by itself.

## 🌸 An easy flower

**The idea:** four sides make a square petal; six petals on six spokes make
a flower.

The five holes hold **petals left (6)**, **petal steps left (5)**, **flower
bird**, **letters**, and **spare numbers**. A petal is five steps: the spoke
out, then four sides. The spare numbers are "five again" and "one less".
"Five again" carries the *set* badge, so it replaces the step count instead
of adding to it.

The petals stand a little way out from the centre, on **spokes drawn in
invisible ink**: `[set | pen | invisible]` keeps the pen drawing, unseen, so
the six petals and the stalk stay ONE drawing -- one thing for Dusty to
sweep up, one thing to save -- where a lifted pen would have ended the
trail. `[set | pen | hotpink]` brings the ink back.

The four robots have separate jobs:

1. **Draw the stalk and rest:** when petals left is zero, pink ink and pen
   down again, draw down 0.35 to the table, lift the pen, come back up, and
   put away the work box.
2. **Go out to the petal:** when petal steps left is five, walk out along a
   spoke in invisible ink, then pink again; that is the first step.
3. **Back to the centre:** when petal steps left is zero, turn about and walk
   the spoke back in invisible ink, turn to the next spoke, subtract one
   petal, and set petal steps left to five again.
4. **Draw one side:** put the pen down, walk 0.09, turn 90°, and subtract one
   step.

Watch the two counters: petal steps counts 5, 4, 3, 2, 1, 0 for each petal;
petals counts down once per petal. That is a repeat inside another repeat. The
flower head is flat, with a stalk going down into the third dimension.

**Try:** set petals left to 3 and change "next spoke" from 240° to 300°.
Keep the square corner at 90°. Why do those two turns have different jobs?
Then sweep the flower up with Dusty: it comes up as one thing.

## ✨ A jumping spark

**The idea:** keep moving forward, but make the upward step smaller each
time.

The world opens looking from the side, where the arch reads as an arch.
The five holes hold **jumps left (20)**, **spark bird**, **letters**,
**gravity (−1/100)**, and **one less (−1)**.

**Fly one step:** move up by the number in the upward-step letter → move
forward 0.02 → leave a small sphere → add gravity to the number inside the
upward-step letter → subtract one jump. **Hide and rest:** when jumps left is
zero, hide the moving spark and put away the work box. Its twenty dots
remain.

The upward steps begin 1/10, 9/100, 8/100… Eventually the number is zero,
then negative, and a negative upward step moves down: the dots draw an arch.
The number being changed is **inside the letter**, not in a separate speed
box.

**Try:** change gravity to zero. Predict the shape before running. Then try
−1/200. Keep twenty jumps while comparing, so only one thing changes.

## The helper cards

`🌸 flower-helper`, `🪐 orbit-helper` and `✨ spark-helper` are the same
teams as behaviour cards. Their birds address "my thing", so a card can be
attached to any sphere: import a card, drop it on a sphere of your own, and
switch it on. Pick the card up and press Ctrl+P to look inside; its little
door lets you inspect the team. A flower wants its sphere 0.35 above the
table, a spark 0.05. Start from a fresh copy of a card once its work box has
been put away. Colour and starting position belong to the thing; the robots'
recipe stays the same.
