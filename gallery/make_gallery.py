# -*- coding: utf-8 -*-
# THE EXAMPLES GALLERY: every example world in the order to learn them, each
# with what it teaches, what it needs first, how big it is (counted from the
# file), a picture, how to run it, and one thing to change and predict.
# ChatGPT's review of the examples asked for "an ordered route through it"
# (18 Sep 2026); Ken: "let's do 4 now".
#
#   python gallery/make_gallery.py            writes ../gallery.html
#
# The pictures come from tests/gallery_shots.html (open it with the dev
# server up; it posts them to captures/ as gallery-<n>.jpg), then
#   python gallery/make_gallery.py --shots     copies them in here as <n>.jpg
import io, json, os, sys, glob, shutil, html, re
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# (file under examples/, group, teaches, needs, how to run, change and predict, shot recipe)
ROUTE = [
  # ---------------------------------------------------------------- first steps
  ('numbers/🔀 swap', 'First steps',
   'A robot does one thing to what it is given, and stops when its thought no longer fits.',
   [], 'Give the leaning scale to the Swap robot: it swaps the two pans, the scale tips the other way, and the robot stops after one round.',
   'Give it the OTHER scale, the one already the right way round. Predict: does it run, and why not?', 'give'),
  ('behaviours/🏃 moving', 'First steps',
   'A behaviour is a letter to a bird: [move | across | 1/60] every round, and the star slides.',
   ['numbers/🔀 swap'], 'Press SPACE on the star: it slides right and stops at the table’s edge; "." stops it early. The Mover is on its back: hold the star and press Ctrl+P to go through its door and watch.',
   'In there, pick up the step and type a minus. Predict which way the star goes — then make the number bigger.', 'space'),
  ('lessons/🪐 step-and-turn-planet', 'First steps',
   'Repeated motion: walk a little, turn a little, thirty-six times, and a ring appears. Two robots share the work box.',
   ['behaviours/🏃 moving'], 'Press Start the robot: the planet walks and turns thirty-six times and a ring of dots appears round the sun. Instant shows the ring at once.',
   'Change steps left to 9 before you start. How much of the ring will be drawn? Then try 18.', 'run'),
  ('lessons/🌸 easy-flower', 'First steps',
   'A repeat inside a repeat: four sides make a square petal, six petals on spokes make a flower — each its own colour from a queue on a nest, and invisible ink keeps it one drawing.',
   ['lessons/🪐 step-and-turn-planet'], 'Press Start the robot: six square petals appear round a centre, each a different colour. The next member button above Trained actions shows each robot.',
   'Set petals left to 3 and next spoke from 240° to 300°. Predict the flower; then sweep it up with Dusty — one thing.', 'run'),
  ('lessons/✨ jumping-spark', 'First steps',
   'A movement amount that changes over time: gravity shrinks the upward step inside the letter each jump, and the dots draw an arch.',
   ['lessons/🪐 step-and-turn-planet'], 'Press Start the robot: the spark rises and falls in twenty steps and leaves an arch of dots behind. The world opens from the side, where the arch reads.',
   'Set gravity to 0. Predict the shape before running; then try −1/200.', 'run'),
  ('behaviours/🎨 random-colour', 'First steps',
   'A pad with a robot on its back: a die picks the Nth colour from a list by splitting the list there, and three letters paint the pad.',
   ['behaviours/🏃 moving'], 'Press SPACE on the pad: its colour changes again and again, one of the seven; "." stops it. Ctrl+P on it shows the robot at work.',
   'Open the panel and join another [name | ink] pair on the list, then give the die a face. Predict how often the new colour comes up.', 'space'),
  # ------------------------------------------------------- things that talk
  ('devices/⌨️ keys', 'Things that talk',
   'The keyboard is a nest: every key lands on it, and a robot dozing on the nest wakes per key.',
   ['behaviours/🏃 moving'], 'Give the work box to the Scribe, then type: each key you press appears on the pad.',
   'Type a space, then Backspace. Predict what the pad says — the Scribe joins whatever arrives.', 'give'),
  ('devices/🖱️ pointer', 'Things that talk',
   'The pointer is a nest too: a reading of [across | away] each move, and three steps keep a box up to date.',
   ['devices/⌨️ keys'], 'Give the work box to the Watcher and move the pointer over the table: the two numbers in its box follow the pointer.',
   'Stop moving. Predict whether the robot keeps running — an empty nest is a robot asleep.', 'give'),
  ('behaviours/🐾 following', 'Things that talk',
   'The pointer reading put inside a [set | position | …] letter: the star follows your hand.',
   ['devices/🖱️ pointer', 'behaviours/🏃 moving'], 'Press SPACE on the star and move the pointer over the table: the star comes to your hand and stays with it. The Follower is on the star’s back: Ctrl+P to watch it.',
   'Change the letter to [move | position | …] instead of set. Predict: does the star follow, or run away?', 'space'),
  ('behaviours/🏀 bouncing', 'Things that talk',
   'The edge is a reading; a team of robots differ only in the word they expect, and flipping a step is a ×−1 dropped on a number.',
   ['behaviours/🏃 moving'], 'Press SPACE on the star: it runs to the right edge, turns round, runs back, and keeps going. The team is on its back: Ctrl+P to go through its door and watch them take turns.',
   'Take the “at the right” robot out of the team. Predict what happens at the right edge.', 'space'),
  ('behaviours/🦋 wandering', 'Things that talk',
   'Randomness is a die: a die of 3, a −2 and a ×30 land on the turn in turn, then a yaw and a step go to the bird.',
   ['behaviours/🏀 bouncing'], 'Press SPACE on the star: it drifts about the table, turning at random. The Wanderer is on its back: Ctrl+P to watch the die land.',
   'In there, hold the die and type 5. Predict: which way does the star circle, and why?', 'space'),
  ('devices/⏱️ timer', 'Things that talk',
   'A stopwatch that is not built in: robots on the number’s own panel ask the computer the time and tell the number.',
   ['devices/🖱️ pointer'], 'Press SPACE on the number: it counts up the milliseconds; "." rests it, and SPACE goes on from there.',
   'Drop a 0 with a set badge on it and start it again. Predict what it counts from.', 'space'),
  ('devices/🖥️ computer', 'Things that talk',
   'The workshop’s own machine answers letters: [query | time | bird], [query | date | bird], [query | clock | bird].',
   ['devices/⏱️ timer'], 'Take a letter off a notebook page, put a bird of your own in its last hole, and give it to the bird to the computer: the answer — the time, the date or the clock — lands on your bird’s nest.',
   'Ask for the time twice a minute apart. Predict which holes change — and why the date would not.', 'load'),
  ('behaviours/🐢 turtle', 'Things that talk',
   'A Logo turtle that is not built in: a nest for orders, two robots, and a pen — forward and right are messages the turtle already answered.',
   ['behaviours/🏀 bouncing'], 'Drop the turtle pad on the shell’s EDGE — the middle makes it ride on the shell instead of steering it — and press SPACE; give the bird “pendown”, then [forward] and [right 90] four times: a square is drawn on the table.',
   'Give it [right | 120] instead of 90, three times. Predict the shape.', 'load'),
  ('behaviours/🐢 turtle3d', 'Things that talk',
   'The same turtle in its own frame: yaw, pitch and roll, so it can climb and draw in the air.',
   ['behaviours/🐢 turtle'], 'As the turtle, with pitch and roll orders on the table: give it a pitch and a forward and the line leaves the table and climbs.',
   'Pitch up 45, forward, pitch down 45, forward. Predict where the line ends up.', 'load'),
  ('behaviours/🪐 ellipse', 'Things that talk',
   'An orbit from two numbers: a position set each round from a growing angle, sine and cosine as letters.',
   ['behaviours/🦋 wandering'], 'Drop the ellipse pad on the star’s EDGE (the middle would only make it ride on the star) and press SPACE on the star: it goes round and round an ellipse; "." stops it, Ruby lets go.',
   'Change one of the two radii. Predict the shape before you look.', 'give'),
  # --------------------------------------------------------- numbers and data
  ('numbers/❗ factorial', 'Numbers and data',
   'A loop with a scale for its test: the count climbs to N, the beam comes level, and the product goes to a bird.',
   ['numbers/🔀 swap'], 'Give the two-hole box to the Factorial robot: the count climbs to 5, the scale comes level, and the product, 120, flies off with the bird.',
   'Change 5 to 8 before you start. Predict the answer, and how many rounds it takes.', 'give'),
  ('numbers/🐇 fibonacci', 'Numbers and data',
   'Recursion by houses: each call sends a copy of itself into two houses and the ones pile up on a nest to be summed.',
   ['numbers/❗ factorial'], 'Give the five-hole box to the Fib robot; when the smoke stops, give the [0, nest] box to the Sum robot: it adds the ones up and stops at 21.',
   'Ask for fib(5) instead of fib(8). Predict how many ones arrive.', 'give'),
  ('numbers/🐇 fibonacci-recursive', 'Numbers and data',
   'The same recursion with promises: each call makes two nests and dozes until both answer.',
   ['numbers/🐇 fibonacci'], 'Give the seven-hole box to the fib robot: houses appear and answer one another, and fib(6) arrives on the nest marked “the answer”.',
   'Watch which house answers first. Predict whether the order matters to the answer.', 'give'),
  ('numbers/🌡️ gauge', 'Numbers and data',
   'Live numbers: two numbers that listen to each other, each change landing on an event nest, newest underneath.',
   ['devices/🖥️ computer'], 'Pull both levers up; drop a +3 on A and a ×2 on B: each change lands on the event nest, the newest underneath, and the other number answers.',
   'Drop a +0 on A. Predict whether B moves — an update that changes nothing is swallowed.', 'lever'),
  ('lists/🔢 n-to-1', 'Numbers and data',
   'A lazy list, a link at a time: each round one link lands on a nest, and a box with no holes means the end.',
   ['numbers/❗ factorial'], 'Give the two-hole box to the FinishList robot: 5, 4, 3, 2, 1 land on the nest one a round, then a box with no holes.',
   'Start from 3 instead of 5. Predict the pile on the nest, top to bottom.', 'give'),
  ('lists/🔗 append', 'Numbers and data',
   'Two lazy lists joined: each link lands inside the promise the last one carried, so the answer grows from the outside in.',
   ['lists/🔢 n-to-1'], 'Give the three-hole box to the FinishAppend robot: the joined list grows on “both lists”, a link a round.',
   'Give it two empty lists. Predict what arrives on “both lists”.', 'give'),
  ('lists/🔁 reverse', 'Numbers and data',
   'Reversal by houses that wait on one another: the last link settles first.',
   ['lists/🔗 append'], 'Give the four-hole box to the Reverse robot: a house appears for each link, and the list comes back the other way round.',
   'Reverse a one-link list. Predict how many houses appear.', 'give'),
  ('words/🔤 grammar', 'Numbers and data',
   'A grammar read as data: a rule is a number, the robot splits a copy of the dictionary there and throws its die to choose.',
   ['lists/🔁 reverse', 'behaviours/🦋 wandering'], 'Pull the lever: sentences pile up on the nest, a new one each round; pull it again when you have enough.',
   'Add a word to one alternative in the dictionary and pull the lever. Predict which sentences change — the robot is untouched.', 'lever'),
  ('words/📝 sentence-generator', 'Numbers and data',
   'A sentence factory in a glass room: the same idea with the rules fixed in the robots.',
   ['words/🔤 grammar'], 'Pull the lever on the right wall: sentences come out of the room; click the door to step inside and watch the team make them.',
   'Step inside and read the team. Predict which robot would have to change to add an adjective.', 'lever'),
  # --------------------------------------------------------- houses and state
  ('accounts/💰 account', 'Houses and state',
   'A box with a nest for requests: the robot whose thought carries the word wakes, serves it, and dozes again.',
   ['devices/⌨️ keys'], 'Give the account box to the Teller, then drop a message on the “requests” bird: the balance changes and a slip comes back.',
   'Send [withdraw | 500]. Predict what the balance does, and what comes back.', 'give'),
  ('accounts/🏦 bank-account', 'Houses and state',
   'State sealed in a house: nothing outside can reach the balance; the only way in is a request by bird.',
   ['accounts/💰 account'], 'The house is switched on already. Drop a request on the bird marked “requests”: she flies it in, the Teller answers with a slip, and the balance stays out of reach.',
   'Try the −500 request. Predict which slip the Teller sends, and why the scale decides.', 'load'),
  ('accounts/💳 live-account', 'Houses and state',
   'A live number as the balance: two rooms deposit at once and every badge is applied whole, so the total is right however the rounds land.',
   ['accounts/🏦 bank-account', 'numbers/🌡️ gauge'], 'Pull both levers: the two rooms deposit at once and the balance settles on the same total however the rounds fall.',
   'Predict the final balance before you pull; then predict whether pulling one lever first changes it.', 'lever'),
  ('infinity/📮 zeno', 'Houses and state',
   'Two houses and a bird between them: a halver and a totaller, the totaller asleep until the post comes.',
   ['accounts/🏦 bank-account'], 'Pull the lever on each house: the bird carries halves from the halver to the totaller, and the total climbs toward 1 without reaching it.',
   'Pull only the totaller’s lever. Predict what it does with no post.', 'lever'),
  ('behaviours/📚 library', 'Houses and state',
   'A shelf of behaviours to drop on your own things: sixteen gadgets and a star to try them on.',
   ['behaviours/🏀 bouncing'], 'Drop a gadget on the star and press SPACE on it: the star does what the gadget says; "." stops it; Ruby lets go.',
   'Drop bouncing AND wandering on the star. Predict what happens when it reaches the right wall.', 'load'),
  ('yard/🦁 zoo', 'Houses and state',
   'The yard: seven animals on the grass behind the workshop, each a thing with a name.',
   ['behaviours/📚 library'], 'Go out through the green back door: seven animals stand on the grass, each with its name.',
   'Drop the wandering gadget on the lion and press SPACE. Predict where it goes.', 'yard'),
  ('yard/🦓 zoo-keeper', 'Houses and state',
   'A button that asks the yard who is there — [query | things | bird] — and gives every animal a wiggle.',
   ['yard/🦁 zoo'], 'Go outside and press SPACE on the keeper: every animal in the yard wiggles.',
   'Carry one animal indoors first. Predict how many wiggle.', 'yard'),
  ('models/✈️ airplane-flight', 'Houses and state',
   'A toy airplane that takes off, flies a loop and lands: position, up and facing as letters over time.',
   ['behaviours/🐢 turtle3d'], 'Press SPACE on the airplane: it takes off, flies a loop, and lands.',
   'Change the climb letter’s number. Predict how high the loop goes.', 'space'),
  ('models/✈️ airplane-with-pilot', 'Houses and state',
   'The same flight with a pilot aboard: a thing riding a thing, carried wherever it goes.',
   ['models/✈️ airplane-flight'], 'Press SPACE on the airplane: it flies its loop with the pilot aboard all the way.',
   'Take the pilot off before take-off. Predict whether the flight changes.', 'space'),
  ('sounds/🎹 tones', 'Houses and state',
   'What a sound is: a frequency, seconds and a shape, made by a box dropped on a silent sound.',
   ['numbers/🔀 swap'], 'Press SPACE on a sound to hear it; drop the box on the silent one and it sings too, the waveform on its screen.',
   'Change 440 to 880. Predict what you hear.', 'load'),
  ('sounds/🔉 transforms', 'Houses and state',
   'A number dropped on a sound remakes it: ×2 is faster and an octave up, ×−1 plays it backwards.',
   ['sounds/🎹 tones'], 'Drop the ×2 and the ×−1 on a sound, then SPACE to hear it: faster and an octave up, then backwards.',
   'Drop ×1/2 twice. Predict the pitch.', 'load'),
  ('sounds/🎵 melody', 'Houses and state',
   'A tune built the way a sentence is: a note longer each round, joined on the right edge.',
   ['sounds/🔉 transforms', 'devices/⌨️ keys'], 'Give the work box to the Singer: the tune plays, a note longer each round.',
   'Put the pitches on the nest in another order. Predict the tune.', 'give'),
  ('images/🖼️ pictures', 'Houses and state',
   'A picture is a pad: it takes the same letters, and rides on a pad like anything else.',
   ['behaviours/🏃 moving'], 'Pick a picture up: the card reads it as a picture. Hold one and press Ctrl with the up arrow: it grows, keeping its own proportions. Drop one in the empty box: it goes in like anything else.',
   'Take a letter such as [set | width | 2] off a notebook page, put a picture’s bird in its last hole, and send it. Predict what happens to the picture.', 'load'),
  ('images/📸 album', 'Houses and state',
   'A notebook files things and a picture is a thing, so a notebook of pictures is an album — and no album was ever written.',
   ['images/🖼️ pictures'], 'Point at the album and press the left and right arrow keys, or click its gold corner tabs: six pages, a picture on each. Click a picture to lift it off its page as an ordinary pad; drop it back to file it.',
   'Drop the spare star picture on a blank page. Predict whether the arrow keys reach it — then click the spine and pick up the whole album at once.', 'load'),
  ('images/🏷️ naming', 'Houses and state',
   'A team that names what it sees: seven pictures come off the nest and seven names pile up.',
   ['images/📸 album', 'behaviours/🏀 bouncing'], 'Give the work box to the team leader: seven pictures come off the nest and seven names pile up.',
   'Put the star on the nest twice. Predict how many names arrive.', 'give'),
  # ------------------------------------------------------------ games
  ('games/🏓 pong-classic', 'Games',
   'Pong from the ordinary parts: a ball, a bat that follows the pointer, a counter, a pitch.',
   ['behaviours/🏀 bouncing', 'behaviours/🐾 following'], 'Set Speed to Instant, point at the pitch and press ENTER, then SPACE: the ball is in play and the bat follows your pointer up and down.',
   'Make the ball’s step bigger. Predict whether the bat can keep up.', 'space'),
  ('games/🏓 pong-gadgets', 'Games',
   'The same game built by dropping behaviours from the shelf on the ball and the bat.',
   ['games/🏓 pong-classic', 'behaviours/📚 library'], 'Press SPACE on the ball, then on the bat: the ball bounces about the pitch and the bat follows the pointer.',
   'Take the bouncing gadget off the ball. Predict what the ball does at the wall.', 'space'),
  ('games/🏓 pong', 'Games',
   'Pong with collisions: the ball bounces off anything on the table, so first clear the court.',
   ['games/🏓 pong-gadgets'], 'Vacuum the pads away, set Speed to Instant, and press SPACE on the ball: it bounces off the walls and off the bat.',
   'Leave one pad on the court. Predict the rally.', 'space'),
  ('games/👾 space-invaders', 'Games',
   'A whole game to be read: a field, a ship on the arrow keys, bullets that vanish, invaders that are hit, a score.',
   ['games/🏓 pong', 'devices/⌨️ keys'], 'Point at the dark field and press SPACE; arrows move, up fires: the invaders march, hits take them out, and the score climbs.',
   'Open one invader’s panel. Predict which robot makes it drop down a row.', 'space'),
  # --------------------------------------------------------- infinity
  ('infinity/♾️ activity1-even-numbers', 'Infinity',
   'Exploring Infinity 1: three rooms in a pipeline, each waking as the first number reaches it, and the evens keep pace with the whole numbers.',
   ['infinity/📮 zeno'], 'Pull the lever on the Add 1 room: the numbers pass down the pipeline and the nests fill, doubles keeping pace with the whole numbers.',
   'Is there an even number on B that is not on doubled? Predict, then watch the two nests fill.', 'lever'),
  ('infinity/♾️ activity2-all-integers', 'Infinity',
   'Exploring Infinity 2: the negatives merged in, fairly — Merge waits for the matching negative.',
   ['infinity/♾️ activity1-even-numbers'], 'Pull the lever on the Add 1 room: positives and negatives arrive on the merged nest in turn; pull it again when you have seen enough.',
   'Predict the order on the merged nest before it fills.', 'lever'),
  ('infinity/♾️ activity3-sequences-and-pairs', 'Infinity',
   'Exploring Infinity 3: squares, and pairs [n, n²] — a sequence of boxes.',
   ['infinity/♾️ activity2-all-integers'], 'Pull the lever on the Add 1 room: squares and [n, n²] pairs land on their nests.',
   'Train a robot of your own for cubes and put it in the squarer’s place. Predict the pairs.', 'lever'),
  ('infinity/♾️ activity4-all-fractions', 'Infinity',
   'Exploring Infinity 4: every fraction between 0 and 1, the scale pans as holes.',
   ['infinity/♾️ activity3-sequences-and-pairs'], 'Pull the lever on the All Fractions room: fractions between 0 and 1 arrive on the nest, none missed.',
   'Does 2/4 appear, and 1/2 as well? Predict, then look.', 'lever'),
  ('infinity/♾️ activity5-above-one', 'Infinity',
   'Exploring Infinity 5: the fractions above one are the reciprocals of those below.',
   ['infinity/♾️ activity4-all-fractions'], 'Pull the lever on the All Fractions room: each fraction below one lands with its reciprocal on the other nest.',
   'Predict the first five on the reciprocals nest.', 'lever'),
  ('infinity/♾️ activity6-all-rationals', 'Infinity',
   'Exploring Infinity 6: every positive rational, five rooms waking in turn, Merge keeping it fair.',
   ['infinity/♾️ activity5-above-one'], 'Pull the lever on the All Fractions room: the five rooms wake in turn and the merged nest fills with the positive rationals, none missed.',
   'Predict where 3/2 comes in the merged order relative to 2/3.', 'lever'),
  ('infinity/♾️ activity7-any-interval', 'Infinity',
   'Exploring Infinity 7: three nests filling term by term, one for one — the pairing made visible (the post takes a moment, so the counts can differ briefly).',
   ['infinity/♾️ activity6-all-rationals'], 'Pull the lever on the All Fractions room: the three nests fill together, term for term.',
   'The argument is that ×2 can be undone. Predict what the halving room sends for 3/8.', 'lever'),
  ('infinity/♾️ activity8-counting-sequences', 'Infinity',
   'Exploring Infinity 8: the team takes the first term of the first sequence, the second of the second… a diagonal.',
   ['infinity/♾️ activity7-any-interval'], 'Give the three Sequence boxes to the All Sequences bird and pull the three levers: the team takes a term from each in turn and the diagonal piles up.',
   'Predict the first six terms the team takes, in order.', 'lever'),
  ('infinity/🏨 resort-infinity', 'Infinity',
   'Resort Infinity: cottages without end, guests to house and to move up five — the robots are yours to train.',
   ['infinity/♾️ activity8-counting-sequences'], 'Go outside. Train a robot on the practice letter and give it to the front desk’s bird: each guest is answered and walks to its cottage.',
   'Before you train: predict what the guest at cottage 1 must be told when five more arrive.', 'yard'),
  # ------------------------------------------------------------- meta
  ('meta/🎓 teacher', 'Meta',
   'A robot that trains a robot: the pupil takes a desk, is shown its step, and has its thought loosened by Ruby.',
   ['numbers/❗ factorial'], 'Give the four-hole box to the teacher and press Start: the pupil takes a desk and is taught; then click the pupil and press Start to see it do what it learned.',
   'Predict what the pupil’s thought says after the lesson, before you look.', 'give'),
  ('meta/🎓 telling', 'Meta',
   'A teacher whose pupil learns to write to the perch: [set | value | 5] lands on “what it told”.',
   ['meta/🎓 teacher', 'behaviours/🏃 moving'], 'Give the four-hole box to the teacher and press Start: the pupil is taught, and [set | value | 5] lands on “what it told”.',
   'Change the reading before the lesson. Predict the letter that lands.', 'give'),
  ('meta/🎓 timer-teacher', 'Meta',
   'A teacher that builds the stopwatch: robots that really ask the computer and really tell the number.',
   ['meta/🎓 telling', 'devices/⏱️ timer'], 'Give the eleven-hole box to the teacher and press Start: four pupils are trained in turn and go on to a number’s panel; take the number out and SPACE on it, and it counts.',
   'Predict which pupil asks and which tells, from their thoughts alone.', 'give'),
  ('meta/🎓 resort-teacher', 'Meta',
   'A robot solves Resort Infinity in front of you: it trains the two robots and gives them to the birds.',
   ['meta/🎓 timer-teacher', 'infinity/🏨 resort-infinity'], 'Go outside and give the teacher its box: it trains the two robots, gives them to the birds, and the guests are housed.',
   'Predict which of the two lessons it gives first, and why the order matters.', 'yard'),
]

# READABLE TITLES (Ken): the file names are for the folder; a card wants words.
TITLES = {
  'numbers/🔀 swap': 'Swap', 'behaviours/🏃 moving': 'Moving', 'lessons/🪐 step-and-turn-planet': 'A step-and-turn planet',
  'lessons/🌸 easy-flower': 'An easy flower', 'lessons/✨ jumping-spark': 'A jumping spark', 'behaviours/🎨 random-colour': 'Random colour',
  'devices/⌨️ keys': 'The keyboard', 'devices/🖱️ pointer': 'The pointer', 'behaviours/🐾 following': 'Following the pointer',
  'behaviours/🏀 bouncing': 'Bouncing', 'behaviours/🦋 wandering': 'Wandering', 'devices/⏱️ timer': 'A stopwatch',
  'devices/🖥️ computer': 'The computer', 'behaviours/🐢 turtle': 'A turtle', 'behaviours/🐢 turtle3d': 'A turtle in the air',
  'behaviours/🪐 ellipse': 'An ellipse', 'numbers/❗ factorial': 'Factorial', 'numbers/🐇 fibonacci': 'Fibonacci by houses',
  'numbers/🐇 fibonacci-recursive': 'Fibonacci by promises', 'numbers/🌡️ gauge': 'A gauge of live numbers', 'lists/🔢 n-to-1': 'A list from n to 1',
  'lists/🔗 append': 'Appending two lists', 'lists/🔁 reverse': 'Reversing a list', 'words/🔤 grammar': 'A grammar as data',
  'words/📝 sentence-generator': 'A sentence factory', 'accounts/💰 account': 'Sally\u2019s account', 'accounts/🏦 bank-account': 'A bank account in a house',
  'accounts/💳 live-account': 'A live account', 'infinity/📮 zeno': 'Zeno\u2019s postman', 'behaviours/📚 library': 'The shelf of behaviours',
  'yard/🦁 zoo': 'The zoo', 'yard/🦓 zoo-keeper': 'The zoo keeper', 'models/✈️ airplane-flight': 'An airplane\u2019s flight',
  'models/✈️ airplane-with-pilot': 'An airplane with its pilot', 'sounds/🎹 tones': 'Tones', 'sounds/🔉 transforms': 'Remaking a sound',
  'sounds/🎵 melody': 'A melody', 'images/🖼️ pictures': 'Pictures', 'images/📸 album': 'An album', 'images/🏷️ naming': 'Naming pictures',
  'games/🏓 pong-classic': 'Pong, from the parts', 'games/🏓 pong-gadgets': 'Pong, from the shelf', 'games/🏓 pong': 'Pong, with collisions',
  'games/👾 space-invaders': 'Space Invaders', 'infinity/♾️ activity1-even-numbers': 'Even numbers', 'infinity/♾️ activity2-all-integers': 'All the integers',
  'infinity/♾️ activity3-sequences-and-pairs': 'Sequences and pairs', 'infinity/♾️ activity4-all-fractions': 'All the fractions between 0 and 1',
  'infinity/♾️ activity5-above-one': 'The fractions above one', 'infinity/♾️ activity6-all-rationals': 'All the positive rationals',
  'infinity/♾️ activity7-any-interval': 'Any interval', 'infinity/♾️ activity8-counting-sequences': 'Counting the sequences',
  'infinity/🏨 resort-infinity': 'Resort Infinity', 'meta/🎓 teacher': 'The teacher', 'meta/🎓 telling': 'Telling',
  'meta/🎓 timer-teacher': 'The stopwatch teacher', 'meta/🎓 resort-teacher': 'The resort teacher',
}

# WHAT YOU DO, apart from how much is inside (ChatGPT's gallery review:
# "separate learning difficulty from program size"). Resort Infinity holds
# sixty-three robots, and asks you to train one.
DO_WORDS = {'try': 'try it', 'change': 'change it', 'read': 'read it', 'build': 'build it'}
DO = {}
for _n in ['numbers/🔀 swap', 'numbers/🐇 fibonacci-recursive', 'devices/🖥️ computer', 'accounts/🏦 bank-account', 'accounts/💳 live-account',
           'infinity/📮 zeno', 'images/📸 album', 'images/🏷️ naming', 'yard/🦓 zoo-keeper', 'infinity/♾️ activity1-even-numbers',
           'infinity/♾️ activity2-all-integers', 'infinity/♾️ activity4-all-fractions', 'infinity/♾️ activity5-above-one',
           'infinity/♾️ activity6-all-rationals', 'infinity/♾️ activity7-any-interval', 'infinity/♾️ activity8-counting-sequences']:
    DO[_n] = 'try'
for _n in ['words/📝 sentence-generator', 'games/👾 space-invaders', 'meta/🎓 teacher', 'meta/🎓 timer-teacher', 'meta/🎓 resort-teacher']:
    DO[_n] = 'read'
for _n in ['infinity/♾️ activity3-sequences-and-pairs', 'infinity/🏨 resort-infinity']:
    DO[_n] = 'build'
# ...and the one card on the beginner route that is a bigger jump than its neighbours
OPTIONAL = {
  'behaviours/🎨 random-colour': 'a bigger jump than the cards round it: a list split at a number to pick the Nth thing, and three letters to one pad. Skip it for now and come back after Things that talk.',
}

GROUP_NOTES = {
  'First steps': 'One visible change, a small robot, a predictable result.',
  'Things that talk': 'Nests that receive the world, and letters to birds that change it.',
  'Numbers and data': 'Loops, recursion, lists and a grammar — data a robot reads rather than rules it was taught.',
  'Houses and state': 'What a house keeps to itself, what a live number tells, and things that are not numbers.',
  'Games': 'The full games are the destination; open one behaviour at a time.',
  'Infinity': 'Each activity has a finite trace to inspect before the argument about its continuation.',
  'Meta': 'Robots that train robots. Read the pupil’s desired program first, then watch the teacher make it.',
}


def slug_of(name):
    return name.split('/', 1)[1].split(' ', 1)[1] if ' ' in name else name.replace('/', '-')


def count_robots(rec):
    """Every robot in the file -- on the bench, in teams, in houses and on panels -- and the longest program."""
    n, longest = 0, 0
    def walk(t):
        nonlocal n, longest
        if isinstance(t, dict):
            if t.get('kind') == 'robot' and 'program' in t:
                n += 1
                longest = max(longest, len(t.get('program') or []))
            for v in t.values():
                walk(v)
        elif isinstance(t, list):
            for v in t:
                walk(v)
    walk(rec)
    return n, longest


def size_word(robots, longest):
    if robots <= 1 and longest <= 8: return 'small'
    if robots <= 4 and longest <= 16: return 'medium'
    return 'large'


def main(copy_shots=False):
    if copy_shots:
        for i, _ in enumerate(ROUTE, 1):
            src = os.path.join(ROOT, 'captures', 'gallery-%02d.jpg' % i)
            if os.path.exists(src):
                shutil.copyfile(src, os.path.join(HERE, '%02d.jpg' % i))
        print('shots copied')
    cards = []
    warnings = []
    by_name = {name: i for i, (name, *_rest) in enumerate(ROUTE, 1)}
    groups = []
    for i, (name, group, teaches, needs, run, try_, shot) in enumerate(ROUTE, 1):
        path = os.path.join(ROOT, 'examples', name + '.world.json')
        rec = json.load(io.open(path, encoding='utf-8'))
        robots, longest = count_robots(rec)
        if robots == 0 and re.search(r'\brobot|work box', run + ' ' + try_):
            warnings.append('card %d %s: the card talks of a robot and the file has none' % (i, name))
        emoji = name.split('/', 1)[1].split(' ', 1)[0]
        title = emoji + ' ' + TITLES.get(name, name.split('/', 1)[1].split(' ', 1)[-1])
        folder = name.split('/', 1)[0]
        url = 'toontalk-3d.html?world=' + quote('examples/' + name + '.world.json')
        pic = '%02d.jpg' % i
        has_pic = os.path.exists(os.path.join(HERE, pic))
        needs_html = ''.join('<a class="chip" href="#e%d">%s</a>' % (by_name[n], html.escape(TITLES.get(n, n.split('/', 1)[1]))) for n in needs if n in by_name)
        do = DO.get(name, 'change')
        opt = OPTIONAL.get(name)
        open_label = 'Open %s in the workshop' % html.escape(title.split(' ', 1)[1])
        if group not in [g for g, _ in groups]:
            groups.append((group, []))
        groups[-1][1].append(f'''
<article class="card{' optional' if opt else ''}" id="e{i}" data-name="{html.escape(name)}">
  <a class="pic" href="{url}" target="toontalk-workshop" aria-label="{open_label}" title="{open_label} (the workshop tab)">{('<img src="gallery/' + pic + '" alt="" loading="lazy">') if has_pic else '<div class="nopic">no picture yet</div>'}</a>
  <div class="body">
    <h3><span class="n">{i}</span> {html.escape(title)} <span class="folder">{html.escape(folder)}</span></h3>
    {('<p class="opt"><b>Optional challenge</b> — ' + html.escape(opt) + '</p>') if opt else ''}
    <p class="teaches">{html.escape(teaches)}</p>
    <p class="meta"><span class="do do-{do}">{DO_WORDS[do]}</span> <span class="inside">inside: {('<b>' + size_word(robots, longest) + '</b>, ' + str(robots) + ' robot' + ('s' if robots != 1 else '') + ', the longest ' + str(longest) + ' step' + ('s' if longest != 1 else '')) if robots else 'no robots'}</span></p>
    {('<p class="needs"><b>Needs</b> ' + needs_html + '</p>') if needs_html else ''}
    <p class="run"><b>Run:</b> {html.escape(run)}</p>
    <p class="try"><b>Change and predict:</b> {html.escape(try_)}</p>
    <p class="open"><a class="btn" href="{url}" target="toontalk-workshop" aria-label="{open_label}" data-open="{html.escape(name)}">Open in the workshop ↗</a> <label class="tried"><input type="checkbox" data-tried="{html.escape(name)}"> tried</label></p>
  </div>
</article>''')
    sections = ''.join(f'''
<section>
  <h2 id="{html.escape(g.lower().replace(' ', '-'))}">{html.escape(g)}</h2>
  <p class="note">{html.escape(GROUP_NOTES.get(g, ''))}</p>
  <div class="grid">{''.join(cs)}</div>
</section>''' for g, cs in groups)
    toc = ''.join(f'<a href="#{html.escape(g.lower().replace(" ", "-"))}">{html.escape(g)}</a>' for g, _ in groups)
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ToonTalk 3D examples</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23b8241a'/%3E%3Crect x='5' y='5' width='10' height='10' rx='2' fill='%23fff'/%3E%3Crect x='17' y='5' width='10' height='10' rx='2' fill='%23ffd27a'/%3E%3Crect x='5' y='17' width='10' height='10' rx='2' fill='%237fe9ff'/%3E%3Crect x='17' y='17' width='10' height='10' rx='2' fill='%23fff'/%3E%3C/svg%3E">
<style>
  :root {{ --bg: #f6f2e8; --ink: #1f1a14; --dim: #6b6152; --card: #fffdf8; --line: #e3dccb; --accent: #2f6d3a; --btn: #2f6d3a; --btnink: #fff; }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg: #16171b; --ink: #ece7dc; --dim: #a39b8b; --card: #1f2126; --line: #33363d; --accent: #8fd19a; --btn: #3f8d4d; --btnink: #fff; }} }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.45 Georgia, "Times New Roman", serif; }}
  header {{ padding: 28px 16px 8px; max-width: 1100px; margin: 0 auto; }}
  h1 {{ font-size: 30px; margin: 0 0 6px; }}
  header p {{ margin: 6px 0; max-width: 70ch; }}
  .bar {{ position: sticky; top: 0; z-index: 2; background: var(--bg); border-bottom: 1px solid var(--line); font-family: system-ui, sans-serif; font-size: 14px; }}
  .bar .in {{ max-width: 1100px; margin: 0 auto; padding: 8px 16px; display: flex; flex-wrap: wrap; align-items: center; gap: 4px 14px; }}
  .bar a {{ color: var(--accent); text-decoration: none; }}
  .bar input {{ font: inherit; padding: 5px 8px; border: 1px solid var(--line); border-radius: 6px; background: var(--card); color: var(--ink); min-width: 200px; }}
  .bar .qn {{ color: var(--dim); }}
  .bar .top {{ margin-left: auto; }}
  .legend {{ font: 13px/1.5 system-ui, sans-serif; color: var(--dim); }}
  main {{ max-width: 1100px; margin: 0 auto; padding: 0 16px 60px; }}
  h2 {{ margin: 36px 0 4px; font-size: 22px; border-bottom: 1px solid var(--line); padding-bottom: 4px; }}
  .note {{ margin: 0 0 14px; color: var(--dim); }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }}
  .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; display: flex; flex-direction: column; }}
  .pic {{ display: block; aspect-ratio: 16 / 9; background: #0e1014; }}
  .pic img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .nopic {{ height: 100%; display: grid; place-items: center; color: #777; font-family: system-ui, sans-serif; font-size: 13px; }}
  .body {{ padding: 12px 14px 14px; display: flex; flex-direction: column; gap: 6px; }}
  h3 {{ margin: 0; font-size: 18px; }}
  .n {{ display: inline-block; min-width: 26px; text-align: center; background: var(--accent); color: #fff; border-radius: 13px; font: 600 13px/26px system-ui, sans-serif; margin-right: 4px; }}
  .folder {{ font: 12px system-ui, sans-serif; color: var(--dim); margin-left: 6px; }}
  p {{ margin: 0; }}
  .meta, .needs {{ font: 13px/1.6 system-ui, sans-serif; color: var(--dim); }}
  .do {{ display: inline-block; padding: 1px 8px; border-radius: 10px; font-weight: 600; color: #fff; background: var(--accent); margin-right: 6px; }}
  .do-try {{ background: #2f6d3a; }} .do-change {{ background: #8a5a12; }} .do-read {{ background: #35558a; }} .do-build {{ background: #8a2f5a; }}
  .chip {{ display: inline-block; padding: 0 8px; border: 1px solid var(--line); border-radius: 10px; color: var(--accent); text-decoration: none; margin: 1px 4px 1px 0; background: var(--bg); }}
  .opt {{ font: 13px/1.45 system-ui, sans-serif; color: var(--dim); border-left: 3px solid #8a5a12; padding-left: 8px; }}
  .card.optional {{ border-style: dashed; }}
  .tried {{ margin-left: 10px; color: var(--dim); cursor: pointer; }}
  .card.is-tried .n {{ background: var(--dim); }}
  .card.is-tried .n::after {{ content: ' ✓'; }}
  .hide {{ display: none; }}
  .run, .try {{ font-size: 15px; }}
  .open {{ margin-top: 6px; font: 13px system-ui, sans-serif; }}
  .btn {{ display: inline-block; background: var(--btn); color: var(--btnink); padding: 6px 10px; border-radius: 6px; text-decoration: none; }}
  .dim {{ color: var(--dim); margin-left: 6px; }}
  footer {{ max-width: 1100px; margin: 0 auto; padding: 0 16px 40px; color: var(--dim); font: 13px system-ui, sans-serif; }}
</style>
</head>
<body id="top">
<header>
  <h1>The examples, in the order to learn them</h1>
  <p>Every example world in <a href="https://github.com/ToonTalk/toontalk-3d/tree/main/examples">examples/</a>, as a route: what each one teaches, what it needs first, how to run it and what you should see, and one thing to change and predict before you run it again. Each opens in one <a href="toontalk-3d.html">workshop</a> tab, where the button <em>Start this world over</em> on the title card puts it back as it began; the <a href="manual.html">manual</a> explains the parts.</p>
  <p class="legend">Each card says what you do — <span class="do do-try">try it</span> run it and predict, <span class="do do-change">change it</span> change one thing and predict, <span class="do do-read">read it</span> read the robots to predict, <span class="do do-build">build it</span> train a robot of your own — and, apart from that, how much is inside. Tick <em>tried</em> on a card and this browser remembers it.</p>
</header>
<nav class="bar"><div class="in">{toc}<input type="search" id="q" placeholder="Search the {len(ROUTE)} examples…" aria-label="Search the examples"><span class="qn" id="qn"></span><a class="top" href="#top">↑ top</a></div></nav>
<main>{sections}</main>
<footer>The pictures are the worlds as they open, or after one run. Sizes are counted from the files: every robot, on the table, in a team, in a house or on a panel, and the longest program among them. Written by gallery/make_gallery.py.</footer>
<script>
(() => {{
  // THE SEARCH: the cards whose words match stay; a section with none left folds away.
  const q = document.getElementById('q'), qn = document.getElementById('qn');
  const cards = [...document.querySelectorAll('.card')];
  const words = new Map(cards.map(c => [c, c.textContent.toLowerCase()]));
  const filter = () => {{
    const s = q.value.trim().toLowerCase();
    let n = 0;
    for (const c of cards) {{ const on = !s || words.get(c).includes(s); c.classList.toggle('hide', !on); if (on) n++; }}
    for (const sec of document.querySelectorAll('main section')) sec.classList.toggle('hide', ![...sec.querySelectorAll('.card')].some(c => !c.classList.contains('hide')));
    qn.textContent = s ? (n + ' of ' + cards.length) : '';
  }};
  q.addEventListener('input', filter);
  // THE TRIED MARKS: this browser's, and nobody else's (localStorage may be off: then the ticks last the page)
  const KEY = 'tt3d.gallery.tried';
  const load = () => {{ try {{ return new Set(JSON.parse(localStorage.getItem(KEY) || '[]')); }} catch (e) {{ return new Set(); }} }};
  const tried = load();
  const save = () => {{ try {{ localStorage.setItem(KEY, JSON.stringify([...tried])); }} catch (e) {{}} }};
  const show = () => {{ for (const c of cards) {{ const on = tried.has(c.dataset.name); c.classList.toggle('is-tried', on); const box = c.querySelector('[data-tried]'); if (box) box.checked = on; }} }};
  document.addEventListener('change', e => {{ const n = e.target.dataset?.tried; if (!n) return; if (e.target.checked) tried.add(n); else tried.delete(n); save(); show(); }});
  document.addEventListener('click', e => {{ const n = e.target.closest?.('[data-open]')?.dataset.open; if (n && !tried.has(n)) {{ tried.add(n); save(); show(); }} }});
  show();
}})();
</script>
</body>
</html>
'''
    io.open(os.path.join(ROOT, 'gallery.html'), 'w', encoding='utf-8', newline='\n').write(page)
    io.open(os.path.join(HERE, 'route.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps([{'i': i, 'name': n, 'shot': s} for i, (n, _g, _t, _d, _r, _y, s) in enumerate(ROUTE, 1)], ensure_ascii=False, indent=1))
    for w in warnings:
        print('WARNING', w)
    print('wrote gallery.html with', len(ROUTE), 'examples')
    if warnings:
        sys.exit(1)


if __name__ == '__main__':
    main('--shots' in sys.argv)
