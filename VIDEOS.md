# Short video demos of ToonTalk 3D

Suggestions for 20–60 second captioned clips. Each one shows a single idea,
opens on the thing that idea is about, and ends on the result — no menus,
no narration of what is about to happen, just the workshop doing it.

Site: https://toontalk.github.io/toontalk-3d/
A world opens straight from a link:
`toontalk-3d.html?world=examples/<folder>/<file>.world.json` (the gallery
cards carry these links; add `&fresh` to start from a clean workshop).

## Production notes

- Record a 16:9 window at 1280×720 or 1920×1080, mouse pointer visible —
  the pointer is part of the story in a hands-on language.
- Speed: the speed control is on the toolbar. Record training and giving at
  normal speed; long runs (gardens, planets, recursion) can jump to Instant
  for the payoff, or run at 2× — say so in a caption if it is sped up.
- Captions: one short line at a time, lower third, plain sentences. Say
  what the viewer is seeing, not what they should feel. American spelling.
- Sound is optional; the workshop has its own (birds, houses, Dusty) and it
  helps to keep it.
- Every claim in a caption must be visible on screen in the same clip. If
  the take does not show it, cut the caption, not the other way round.
- Start each clip with the world already open (trim the load).

## The shortlist (in this order for a first batch)

### 1. One robot, one job — 20 s
World: `examples/numbers/🔀 swap.world.json`
- Pick up the leaning scale, give it to the Swap robot. He swaps the two
  pans, the scale tips the other way, he stops.
- Give him the other scale, the one already the right way round. He looks
  and does nothing.
Captions: "A robot does what it was shown." / "It only starts when what it
sees matches what it was shown." / "This scale doesn't match — so he
waits."

### 2. Teach a robot by doing — 60 s
World: a fresh workshop (`?fresh`).
- Take a robot from the robot stack, a number from the number stack. Type
  `3` on the number.
- Drop the number into the robot's thought bubble. Take a `1` and drop it
  on the `3` — it becomes `4`. Come out of the thought bubble.
- Ruby (the eraser) rubs the `3` out of the bubble so the robot works on
  any number, not only 3.
- Press Run. The desk counts up: 4, 5, 6 …
Captions: "There is no code. You show the robot what to do." / "Drop 1 on
the number: it adds." / "Erase the 3 so it works for any number." / "Run.
He repeats what he was shown, forever."
(This is the core of ToonTalk. Worth the full minute.)

### 3. Birds and nests — 30 s
World: a fresh one with a bird and nest taken from the stacks.
- Take a bird from the stack; a nest comes with her. Set the nest on the
  other side of the table.
- Give the bird a number. She flies it to her nest and comes back.
- Give her three things in a row. Each lands on the nest, on top.
- Give a thing to the translucent stand-in while she is away: it waits for
  her, then goes.
Captions: "A bird carries anything to her nest." / "Things pile up on the
nest in the order they arrive." / "Give her something while she is out —
she takes it when she is back."

### 4. Through the door on its back — 40 s
World: `examples/behaviours/🏃 moving.world.json`
- Press SPACE on the star. It slides to the edge of the table and stops.
- Hold the star, press Ctrl+P. The camera goes through the panel door on
  the star's back: a robot is in there sending a letter each round.
- Pick up the step, type a minus, come back out, press SPACE: the star
  slides the other way.
Captions: "Every thing has a door on its back." / "Inside, a robot mails a
letter every round: move across, a sixtieth." / "Change the number in the
letter and the star changes direction."
(Rooms-as-things is new to ToonTalk 3D — this is the clip for it.)

### 5. A robot draws a garden — 30 s
World: `examples/lessons/🌷 flower-garden.world.json`
- Press Start the robot. Three pens rise from their pots, grow stems and
  leaves, and draw three flowers, at 2× or with the end at Instant.
- Pick up one flower with the pointer: it is one thing, and it lifts whole.
Captions: "A repeat inside a repeat inside a repeat." / "Twenty steps make
a petal, petals make a flower, three flowers a garden." / "Each flower is
one drawing — pick it up."

### 6. Planets on their tracks — 30 s
World: `examples/lessons/🔭 planetary-clockwork.world.json`
- Press Start the robot. Three planets go round the sun and a moon round
  the blue one; after 120 ticks everyone is home together.
- Pause on the boxes: an angle that grows by a step each tick, and sin and
  cos badges that turn it into a position.
Captions: "Each tick, every angle grows by its own step." / "Sine and
cosine turn the angle into a place on the track." / "Periods 30, 60, 120
and 15 — so they all come home together."

### 7. Recursion by houses — 40 s
World: `examples/numbers/🐇 fibonacci.world.json`
- Give the five-hole box to the Fib robot. Houses spring up on the table,
  each one sends its work into two more, smoke rises as they finish.
- Give the [0, nest] box to the Sum robot: the ones on the nest are added
  up and it stops at 21.
Captions: "fib(8): each call builds two houses and asks them." / "The
answers land on a nest as ones." / "Add them up: 21."

### 8. A puzzle, judged — 60 s
World: `examples/puzzles/p7.world.json` (stop the doubler at 1,024) or
`p1.world.json` for the gentlest one.
- The intro card says what is wanted. The given things are on the table.
- Solve it on camera.
- Give the answer to the judge's house. The house approves; the next
  puzzle loads.
Captions: "A puzzle is a world with a judge." / "Only what is on the table
may be used." / "The judge checks the answer — and opens the next one."

## Second batch

### 9. Pong, built from robots — 40 s
World: `examples/games/🏓 pong.world.json`
- Play two rallies. Then Ctrl+P into the paddle: the robots inside read
  the keyboard nest and mail move letters; into the ball: bounce is a team
  of robots that differ only in the word they expect from the edge.
Captions: "The paddle reads the keyboard." / "The ball is four robots, one
per edge."

### 10. Resort Infinity — 45 s
World: Resort Infinity 1 (in the yard; the gallery card links it) —
Hilbert's hotel.
- The hotel is full, forever. Five guests arrive. The bell rings, the
  moving office tells everyone to move up five cottages, and five are
  free.
Captions: "Every cottage is taken. Five more guests arrive." / "Everyone
moves up five." / "Five cottages are free — and the hotel is still full."

### 11. A robot that teaches a robot — 45 s
World: `examples/meta/🎓 teacher.world.json` (or `🎓 resort-teacher` for
the harder one).
- The teacher robot opens a pupil's thought bubble and trains it — drops
  the things, erases, closes — then the pupil is given work and does it.
Captions: "This robot is training another robot." / "The pupil now does the
job it was taught."

### 12. Marty — 40 s
Needs a provider key on the machine, or the published claude.ai artifact
(where Marty answers on the viewer's account).
- Ask Marty "what does a robot do?" He answers and offers Show me; press it
  and the demo trains and runs a robot on the table.
- Press Draw with a subject: a turtle draws it.
Captions: "Marty explains and, if asked, shows." / "The demo really trains
the robot — the desk counts up."

### 13. The lion in the yard — 30 s
World: `examples/puzzles/p36.world.json`
- Out through the back door, the table stays in, the ground takes its
  place; the lion and the puzzle are in the yard.
Captions: "Some puzzles are outside." / "The yard is a room too."

### 14. Live numbers — 25 s
World: `examples/numbers/🌡️ gauge.world.json`
- Pull both levers up. Drop a +3 on A: the change lands on the event nest
  and B answers. Drop a ×2 on B.
Captions: "Two numbers that listen to each other." / "Every change lands
on a nest, newest underneath."

### 15. Fireworks — 20 s
World: `examples/lessons/🎆 firework-fountain.world.json`
- Press Start; eight sparks rise in arcs of dots, hide, burst again turned
  15°, three times.
Captions: "Velocity, gravity, one dot per tick." / "Eight sparks, reused
three times."

### 16. Turtle in the air — 30 s
World: `examples/behaviours/🐢 turtle3d.world.json`
- Give the turtle pitch 45, forward, pitch −45, forward: the line leaves
  the table and climbs.
Captions: "A Logo turtle that isn't built in." / "Pitch, and it draws in
the air."

## Things not to do in a clip

- Do not narrate intentions the take does not show (the robot demo once
  said "off it goes" over a desk that stayed still; captions must match
  the pixels).
- Do not open the manual, the notebook, or the menus unless the clip is
  about them.
- Do not speed up the training clip (#2); its slowness is the point.
