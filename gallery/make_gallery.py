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
import io, json, os, sys, glob, shutil, html
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# (file under examples/, group, teaches, needs, how to run, change and predict, shot recipe)
ROUTE = [
  # ---------------------------------------------------------------- first steps
  ('numbers/🔀 swap', 'First steps',
   'A robot does one thing to what it is given, and stops when its thought no longer fits.',
   [], 'Give the leaning scale to the Swap robot.',
   'Give it the OTHER scale, the one already the right way round. Predict: does it run, and why not?', 'give'),
  ('behaviours/🏃 moving', 'First steps',
   'A behaviour is a letter to a bird: [move | across | 1/60] every round, and the star slides.',
   ['numbers/🔀 swap'], 'Set Speed to 8× and give the work box to the Mover.',
   'Pick up the step, type a minus. Predict which way the star goes — then make the number bigger.', 'give'),
  ('lessons/🪐 step-and-turn-planet', 'First steps',
   'Repeated motion: walk a little, turn a little, thirty-six times, and a ring appears. Two robots share the work box.',
   ['behaviours/🏃 moving'], 'Press Start the robot. Instant shows the ring at once.',
   'Change steps left to 9 before you start. How much of the ring will be drawn? Then try 18.', 'run'),
  ('lessons/🌸 easy-flower', 'First steps',
   'A repeat inside a repeat: four sides make a square petal, six petals on spokes make a flower — and invisible ink keeps it one drawing.',
   ['lessons/🪐 step-and-turn-planet'], 'Press Start the robot. Click the condition line to see each team member.',
   'Set petals left to 3 and next spoke from 240° to 300°. Predict the flower; then sweep it up with Dusty — one thing.', 'run'),
  ('lessons/✨ jumping-spark', 'First steps',
   'A movement amount that changes over time: gravity shrinks the upward step inside the letter each jump, and the dots draw an arch.',
   ['lessons/🪐 step-and-turn-planet'], 'Press Start the robot. The world opens from the side, where the arch reads.',
   'Set gravity to 0. Predict the shape before running; then try −1/200.', 'run'),
  ('behaviours/🎨 random-colour', 'First steps',
   'A pad with a robot on its back: a die picks the Nth colour from a list by splitting the list there, and three letters paint the pad.',
   ['behaviours/🏃 moving'], 'Press SPACE on the pad; "." stops it. Ctrl+P on it shows the robot at work.',
   'Open the panel and join another [name | ink] pair on the list, then give the die a face. Predict how often the new colour comes up.', 'space'),
  # ------------------------------------------------------- things that talk
  ('devices/⌨️ keys', 'Things that talk',
   'The keyboard is a nest: every key lands on it, and a robot dozing on the nest wakes per key.',
   ['behaviours/🏃 moving'], 'Give the work box to the Scribe, then type.',
   'Type a space, then Backspace. Predict what the pad says — the Scribe joins whatever arrives.', 'give'),
  ('devices/🖱️ pointer', 'Things that talk',
   'The pointer is a nest too: a reading of [across | away] each move, and three steps keep a box up to date.',
   ['devices/⌨️ keys'], 'Give the work box to the Watcher and move the pointer over the table.',
   'Stop moving. Predict whether the robot keeps running — an empty nest is a robot asleep.', 'give'),
  ('behaviours/🐾 following', 'Things that talk',
   'The pointer reading put inside a [set | position | …] letter: the star follows your hand.',
   ['devices/🖱️ pointer', 'behaviours/🏃 moving'], 'Set Speed to Instant, give the work box to the Follower, and move the pointer.',
   'Change the letter to [move | position | …] instead of set. Predict: does the star follow, or run away?', 'give'),
  ('behaviours/🏀 bouncing', 'Things that talk',
   'The edge is a reading; a team of robots differ only in the word they expect, and flipping a step is a ×−1 dropped on a number.',
   ['behaviours/🏃 moving'], 'Set Speed to 8× and give the work box to the team leader.',
   'Take the “at the right” robot out of the team. Predict what happens at the right edge.', 'give'),
  ('behaviours/🦋 wandering', 'Things that talk',
   'Randomness is a die: a die of 3, a −2 and a ×30 land on the turn in turn, then a yaw and a step go to the bird.',
   ['behaviours/🏀 bouncing'], 'Set Speed to Instant and give the work box to the Wanderer.',
   'Hold the die and type 5. Predict: which way does the star circle, and why?', 'give'),
  ('devices/⏱️ timer', 'Things that talk',
   'A stopwatch that is not built in: robots on the number’s own panel ask the computer the time and tell the number.',
   ['devices/🖱️ pointer'], 'Press SPACE on the number; "." rests it.',
   'Drop a 0 with a set badge on it and start it again. Predict what it counts from.', 'space'),
  ('devices/🖥️ computer', 'Things that talk',
   'The workshop’s own machine answers letters: [query | time | bird], [query | date | bird], [query | clock | bird].',
   ['devices/⏱️ timer'], 'Take a letter off a notebook page, put a bird of your own in its last hole, and give it to the bird to the computer.',
   'Ask for the date twice a minute apart. Predict which holes change.', 'load'),
  ('behaviours/🐢 turtle', 'Things that talk',
   'A Logo turtle that is not built in: a nest for orders, two robots, and a pen — forward and right are messages the turtle already answered.',
   ['behaviours/🏀 bouncing'], 'Drop the turtle on the shell and press SPACE; give the bird “pendown”, then [forward] and [right 90] four times.',
   'Give it [right | 120] instead of 90, three times. Predict the shape.', 'load'),
  ('behaviours/🐢 turtle3d', 'Things that talk',
   'The same turtle in its own frame: yaw, pitch and roll, so it can climb and draw in the air.',
   ['behaviours/🐢 turtle'], 'As the turtle, with pitch and roll orders on the table.',
   'Pitch up 45, forward, pitch down 45, forward. Predict where the line ends up.', 'load'),
  ('behaviours/🪐 ellipse', 'Things that talk',
   'An orbit from two numbers: a position set each round from a growing angle, sine and cosine as letters.',
   ['behaviours/🦋 wandering'], 'Set Speed to Instant and give the work box to the robot.',
   'Change one of the two radii. Predict the shape before you look.', 'give'),
  # --------------------------------------------------------- numbers and data
  ('numbers/❗ factorial', 'Numbers and data',
   'A loop with a scale for its test: the count climbs to N, the beam comes level, and the product goes to a bird.',
   ['numbers/🔀 swap'], 'Give the two-hole box to the Factorial robot.',
   'Change 5 to 8 before you start. Predict the answer, and how many rounds it takes.', 'give'),
  ('numbers/🐇 fibonacci', 'Numbers and data',
   'Recursion by houses: each call sends a copy of itself into two houses and the ones pile up on a nest to be summed.',
   ['numbers/❗ factorial'], 'Give the five-hole box to the Fib robot; when the smoke stops, give the [0, nest] box to the Sum robot.',
   'Ask for fib(5) instead of fib(8). Predict how many ones arrive.', 'give'),
  ('numbers/🐇 fibonacci-recursive', 'Numbers and data',
   'The same recursion with promises: each call makes two nests and dozes until both answer.',
   ['numbers/🐇 fibonacci'], 'Give the seven-hole box to the fib robot.',
   'Watch which house answers first. Predict whether the order matters to the answer.', 'give'),
  ('numbers/🌡️ gauge', 'Numbers and data',
   'Live numbers: two numbers that listen to each other, each change landing on an event nest, newest underneath.',
   ['devices/🖥️ computer'], 'Pull both levers up; drop a +3 on A and a ×2 on B.',
   'Drop a +0 on A. Predict whether B moves — an update that changes nothing is swallowed.', 'lever'),
  ('lists/🔢 n-to-1', 'Numbers and data',
   'A lazy list, a link at a time: each round one link lands on a nest, and a box with no holes means the end.',
   ['numbers/❗ factorial'], 'Give the two-hole box to the FinishList robot.',
   'Start from 3 instead of 5. Predict the pile on the nest, top to bottom.', 'give'),
  ('lists/🔗 append', 'Numbers and data',
   'Two lazy lists joined: each link lands inside the promise the last one carried, so the answer grows from the outside in.',
   ['lists/🔢 n-to-1'], 'Give the three-hole box to the FinishAppend robot.',
   'Give it two empty lists. Predict what arrives on “both lists”.', 'give'),
  ('lists/🔁 reverse', 'Numbers and data',
   'Reversal by houses that wait on one another: the last link settles first.',
   ['lists/🔗 append'], 'Give the four-hole box to the Reverse robot.',
   'Reverse a one-link list. Predict how many houses appear.', 'give'),
  ('words/🔤 grammar', 'Numbers and data',
   'A grammar read as data: a rule is a number, the robot splits a copy of the dictionary there and throws its die to choose.',
   ['lists/🔁 reverse', 'behaviours/🦋 wandering'], 'Pull the lever; pull it again when you have enough sentences.',
   'Add a word to one alternative in the dictionary and pull the lever. Predict which sentences change — the robot is untouched.', 'lever'),
  ('words/📝 sentence-generator', 'Numbers and data',
   'A sentence factory in a glass room: the same idea with the rules fixed in the robots.',
   ['words/🔤 grammar'], 'Pull the lever on the right wall; click the door to step inside and watch.',
   'Step inside and read the team. Predict which robot would have to change to add an adjective.', 'lever'),
  # --------------------------------------------------------- houses and state
  ('accounts/💰 account', 'Houses and state',
   'A box with a nest for requests: the robot whose thought carries the word wakes, serves it, and dozes again.',
   ['devices/⌨️ keys'], 'Give the account box to the Teller, then drop a message on the “requests” bird.',
   'Send [withdraw | 500]. Predict what the balance does, and what comes back.', 'give'),
  ('accounts/🏦 bank-account', 'Houses and state',
   'State sealed in a house: nothing outside can reach the balance; the only way in is a request by bird.',
   ['accounts/💰 account'], 'Drop a request on the bird marked “requests”.',
   'Try the −500 request. Predict which slip the Teller sends, and why the scale decides.', 'load'),
  ('accounts/💳 live-account', 'Houses and state',
   'A live number as the balance: two rooms deposit at once and every badge is applied whole, so the total is right however the rounds land.',
   ['accounts/🏦 bank-account', 'numbers/🌡️ gauge'], 'Pull both levers.',
   'Predict the final balance before you pull; then predict whether pulling one lever first changes it.', 'lever'),
  ('infinity/📮 zeno', 'Houses and state',
   'Two houses and a bird between them: a halver and a totaller, the totaller asleep until the post comes.',
   ['accounts/🏦 bank-account'], 'Pull the lever on each house.',
   'Pull only the totaller’s lever. Predict what it does with no post.', 'lever'),
  ('behaviours/📚 library', 'Houses and state',
   'A shelf of behaviours to drop on your own things: sixteen gadgets and a star to try them on.',
   ['behaviours/🏀 bouncing'], 'Drop a gadget on the star and press SPACE on it; "." stops it; Ruby lets go.',
   'Drop bouncing AND wandering on the star. Predict what happens when it reaches the right wall.', 'load'),
  ('yard/🦁 zoo', 'Houses and state',
   'The yard: seven animals on the grass behind the workshop, each a thing with a name.',
   ['behaviours/📚 library'], 'Go out through the green back door.',
   'Drop the wandering gadget on the lion and press SPACE. Predict where it goes.', 'yard'),
  ('yard/🦓 zoo-keeper', 'Houses and state',
   'A button that asks the yard who is there — [query | things | bird] — and gives every animal a wiggle.',
   ['yard/🦁 zoo'], 'Go outside and press SPACE on the keeper.',
   'Carry one animal indoors first. Predict how many wiggle.', 'yard'),
  ('models/✈️ airplane-flight', 'Houses and state',
   'A toy airplane that takes off, flies a loop and lands: position, up and facing as letters over time.',
   ['behaviours/🐢 turtle3d'], 'Press SPACE on the airplane.',
   'Change the climb letter’s number. Predict how high the loop goes.', 'space'),
  ('models/✈️ airplane-with-pilot', 'Houses and state',
   'The same flight with a pilot aboard: a thing riding a thing, carried wherever it goes.',
   ['models/✈️ airplane-flight'], 'Press SPACE on the airplane.',
   'Take the pilot off before take-off. Predict whether the flight changes.', 'space'),
  ('sounds/🎹 tones', 'Houses and state',
   'What a sound is: a frequency, seconds and a shape, made by a box dropped on a silent sound.',
   ['numbers/🔀 swap'], 'Press SPACE on a sound to hear it; drop the box on the silent one.',
   'Change 440 to 880. Predict what you hear.', 'load'),
  ('sounds/🔉 transforms', 'Houses and state',
   'A number dropped on a sound remakes it: ×2 is faster and an octave up, ×−1 plays it backwards.',
   ['sounds/🎹 tones'], 'Drop the ×2 and the ×−1 on a sound.',
   'Drop ×1/2 twice. Predict the pitch.', 'load'),
  ('sounds/🎵 melody', 'Houses and state',
   'A tune built the way a sentence is: a note longer each round, joined on the right edge.',
   ['sounds/🔉 transforms', 'devices/⌨️ keys'], 'Give the work box to the Singer.',
   'Put the pitches on the nest in another order. Predict the tune.', 'give'),
  ('images/🖼️ pictures', 'Houses and state',
   'A picture is a pad: it takes the same letters, and rides on a pad like anything else.',
   ['behaviours/🏃 moving'], 'Look; then give the pictures the letters on the table.',
   'Send [set | width | 2]. Predict what happens to the picture on it.', 'load'),
  ('images/📸 album', 'Houses and state',
   'Pictures on a nest, taken off one at a time by a robot.',
   ['images/🖼️ pictures'], 'Give the work box to the robot.',
   'Add a picture of your own to the nest. Predict where it ends up.', 'give'),
  ('images/🏷️ naming', 'Houses and state',
   'A team that names what it sees: seven pictures come off the nest and seven names pile up.',
   ['images/📸 album', 'behaviours/🏀 bouncing'], 'Give the work box to the team leader.',
   'Put the star on the nest twice. Predict how many names arrive.', 'give'),
  # ------------------------------------------------------------ games
  ('games/🏓 pong-classic', 'Games',
   'Pong from the ordinary parts: a ball, a bat that follows the pointer, a counter, a pitch.',
   ['behaviours/🏀 bouncing', 'behaviours/🐾 following'], 'Set Speed to Instant, point at the pitch and press ENTER, then SPACE.',
   'Make the ball’s step bigger. Predict whether the bat can keep up.', 'space'),
  ('games/🏓 pong-gadgets', 'Games',
   'The same game built by dropping behaviours from the shelf on the ball and the bat.',
   ['games/🏓 pong-classic', 'behaviours/📚 library'], 'Press SPACE on the ball, then on the bat.',
   'Take the bouncing gadget off the ball. Predict what the ball does at the wall.', 'space'),
  ('games/🏓 pong', 'Games',
   'Pong with collisions: the ball bounces off anything on the table, so first clear the court.',
   ['games/🏓 pong-gadgets'], 'Vacuum the pads away, set Speed to Instant, and press SPACE on the ball.',
   'Leave one pad on the court. Predict the rally.', 'space'),
  ('games/👾 space-invaders', 'Games',
   'A whole game to be read: a field, a ship on the arrow keys, bullets that vanish, invaders that are hit, a score.',
   ['games/🏓 pong', 'devices/⌨️ keys'], 'Point at the dark field and press SPACE; arrows move, up fires.',
   'Open one invader’s panel. Predict which robot makes it drop down a row.', 'space'),
  # --------------------------------------------------------- infinity
  ('infinity/♾️ activity1-even-numbers', 'Infinity',
   'Exploring Infinity 1: three rooms in a pipeline, each waking as the first number reaches it, and the evens keep pace with the whole numbers.',
   ['infinity/📮 zeno'], 'Pull the lever on the Add 1 room.',
   'Is there an even number on B that is not on doubled? Predict, then watch the two nests fill.', 'lever'),
  ('infinity/♾️ activity2-all-integers', 'Infinity',
   'Exploring Infinity 2: the negatives merged in, fairly — Merge waits for the matching negative.',
   ['infinity/♾️ activity1-even-numbers'], 'Pull the lever on the Add 1 room; pull it again when you have seen enough.',
   'Predict the order on the merged nest before it fills.', 'lever'),
  ('infinity/♾️ activity3-sequences-and-pairs', 'Infinity',
   'Exploring Infinity 3: squares, and pairs [n, n²] — a sequence of boxes.',
   ['infinity/♾️ activity2-all-integers'], 'Pull the lever on the Add 1 room.',
   'Train a robot of your own for cubes and put it in the squarer’s place. Predict the pairs.', 'lever'),
  ('infinity/♾️ activity4-all-fractions', 'Infinity',
   'Exploring Infinity 4: every fraction between 0 and 1, the scale pans as holes.',
   ['infinity/♾️ activity3-sequences-and-pairs'], 'Pull the lever on the All Fractions room.',
   'Does 2/4 appear, and 1/2 as well? Predict, then look.', 'lever'),
  ('infinity/♾️ activity5-above-one', 'Infinity',
   'Exploring Infinity 5: the fractions above one are the reciprocals of those below.',
   ['infinity/♾️ activity4-all-fractions'], 'Pull the lever on the All Fractions room.',
   'Predict the first five on the reciprocals nest.', 'lever'),
  ('infinity/♾️ activity6-all-rationals', 'Infinity',
   'Exploring Infinity 6: all the rationals, five rooms waking in turn, Merge keeping it fair.',
   ['infinity/♾️ activity5-above-one'], 'Pull the lever on the All Fractions room.',
   'Predict where 3/2 comes in the merged order relative to 2/3.', 'lever'),
  ('infinity/♾️ activity7-any-interval', 'Infinity',
   'Exploring Infinity 7: three nests filling at exactly the same rate — the pairing made visible.',
   ['infinity/♾️ activity6-all-rationals'], 'Pull the lever on the All Fractions room.',
   'The argument is that ×2 can be undone. Predict what the halving room sends for 3/8.', 'lever'),
  ('infinity/♾️ activity8-counting-sequences', 'Infinity',
   'Exploring Infinity 8: the team takes the first term of the first sequence, the second of the second… a diagonal.',
   ['infinity/♾️ activity7-any-interval'], 'Give the three Sequence boxes to the All Sequences bird and pull the three levers.',
   'Predict the first six terms the team takes, in order.', 'lever'),
  ('infinity/🏨 resort-infinity', 'Infinity',
   'Resort Infinity: cottages without end, guests to house and to move up five — the robots are yours to train.',
   ['infinity/♾️ activity8-counting-sequences'], 'Go outside. Train a robot on the practice letter and give it to the front desk’s bird.',
   'Before you train: predict what the guest at cottage 1 must be told when five more arrive.', 'yard'),
  # ------------------------------------------------------------- meta
  ('meta/🎓 teacher', 'Meta',
   'A robot that trains a robot: the pupil takes a desk, is shown its step, and has its thought loosened by Ruby.',
   ['numbers/❗ factorial'], 'Give the four-hole box to the teacher and press Start; then click the pupil and press Start.',
   'Predict what the pupil’s thought says after the lesson, before you look.', 'give'),
  ('meta/🎓 telling', 'Meta',
   'A teacher whose pupil learns to write to the perch: [set | value | 5] lands on “what it told”.',
   ['meta/🎓 teacher', 'behaviours/🏃 moving'], 'Give the four-hole box to the teacher and press Start.',
   'Change the reading before the lesson. Predict the letter that lands.', 'give'),
  ('meta/🎓 timer-teacher', 'Meta',
   'A teacher that builds the stopwatch: robots that really ask the computer and really tell the number.',
   ['meta/🎓 telling', 'devices/⏱️ timer'], 'Give the eleven-hole box to the teacher and press Start.',
   'Predict which pupil asks and which tells, from their thoughts alone.', 'give'),
  ('meta/🎓 resort-teacher', 'Meta',
   'A robot solves Resort Infinity in front of you: it trains the two robots and gives them to the birds.',
   ['meta/🎓 timer-teacher', 'infinity/🏨 resort-infinity'], 'Go outside and give the teacher its box.',
   'Predict which of the two lessons it gives first, and why the order matters.', 'yard'),
]

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
    by_name = {name: i for i, (name, *_rest) in enumerate(ROUTE, 1)}
    groups = []
    for i, (name, group, teaches, needs, run, try_, shot) in enumerate(ROUTE, 1):
        path = os.path.join(ROOT, 'examples', name + '.world.json')
        rec = json.load(io.open(path, encoding='utf-8'))
        robots, longest = count_robots(rec)
        title = name.split('/', 1)[1]
        folder = name.split('/', 1)[0]
        url = 'toontalk-3d.html?world=' + quote('examples/' + name + '.world.json')
        pic = '%02d.jpg' % i
        has_pic = os.path.exists(os.path.join(HERE, pic))
        needs_html = ''.join('<a href="#e%d">%s</a>' % (by_name[n], html.escape(n.split('/', 1)[1])) for n in needs if n in by_name)
        if group not in [g for g, _ in groups]:
            groups.append((group, []))
        groups[-1][1].append(f'''
<article class="card" id="e{i}">
  <a class="pic" href="{url}" target="_blank" title="Open in the workshop">{('<img src="gallery/' + pic + '" alt="" loading="lazy">') if has_pic else '<div class="nopic">no picture yet</div>'}</a>
  <div class="body">
    <h3><span class="n">{i}</span> {html.escape(title)} <span class="folder">{html.escape(folder)}</span></h3>
    <p class="teaches">{html.escape(teaches)}</p>
    <p class="meta"><b>{size_word(robots, longest)}</b> — {robots} robot{'s' if robots != 1 else ''}, the longest {longest} step{'s' if longest != 1 else ''}{(' · <b>needs</b> ' + needs_html) if needs_html else ''}</p>
    <p class="run"><b>Run:</b> {html.escape(run)}</p>
    <p class="try"><b>Change and predict:</b> {html.escape(try_)}</p>
    <p class="open"><a class="btn" href="{url}" target="_blank">Open in the workshop</a> <span class="dim">Start over is on the card at the right.</span></p>
  </div>
</article>''')
    sections = ''.join(f'''
<section>
  <h2 id="{html.escape(g.lower().replace(' ', '-'))}">{html.escape(g)}</h2>
  <p class="note">{html.escape(GROUP_NOTES.get(g, ''))}</p>
  <div class="grid">{''.join(cs)}</div>
</section>''' for g, cs in groups)
    toc = ' · '.join(f'<a href="#{html.escape(g.lower().replace(" ", "-"))}">{html.escape(g)}</a>' for g, _ in groups)
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ToonTalk 3D examples</title>
<style>
  :root {{ --bg: #f6f2e8; --ink: #1f1a14; --dim: #6b6152; --card: #fffdf8; --line: #e3dccb; --accent: #2f6d3a; --btn: #2f6d3a; --btnink: #fff; }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg: #16171b; --ink: #ece7dc; --dim: #a39b8b; --card: #1f2126; --line: #33363d; --accent: #8fd19a; --btn: #3f8d4d; --btnink: #fff; }} }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.45 Georgia, "Times New Roman", serif; }}
  header {{ padding: 28px 16px 8px; max-width: 1100px; margin: 0 auto; }}
  h1 {{ font-size: 30px; margin: 0 0 6px; }}
  header p {{ margin: 6px 0; max-width: 70ch; }}
  .toc {{ font-family: system-ui, sans-serif; font-size: 14px; color: var(--dim); }}
  .toc a {{ color: var(--accent); text-decoration: none; }}
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
  .meta {{ font: 13px/1.4 system-ui, sans-serif; color: var(--dim); }}
  .meta a {{ color: var(--accent); text-decoration: none; margin-right: 6px; }}
  .run, .try {{ font-size: 15px; }}
  .open {{ margin-top: 6px; font: 13px system-ui, sans-serif; }}
  .btn {{ display: inline-block; background: var(--btn); color: var(--btnink); padding: 6px 10px; border-radius: 6px; text-decoration: none; }}
  .dim {{ color: var(--dim); margin-left: 6px; }}
  footer {{ max-width: 1100px; margin: 0 auto; padding: 0 16px 40px; color: var(--dim); font: 13px system-ui, sans-serif; }}
</style>
</head>
<body>
<header>
  <h1>The examples, in the order to learn them</h1>
  <p>Every example world in <a href="https://github.com/ToonTalk/toontalk-3d/tree/main/examples">examples/</a>, as a route: what each one teaches, what it needs first, how big it is, how to run it, and one thing to change and predict before you run it again. Each opens in the <a href="toontalk-3d.html">workshop</a> with <em>Start this world over</em> on the card at the right; the <a href="manual.html">manual</a> explains the parts.</p>
  <p class="toc">{toc}</p>
</header>
<main>{sections}</main>
<footer>The pictures are the worlds as they open, or after one run. Sizes are counted from the files: every robot, on the table, in a team, in a house or on a panel, and the longest program among them. Written by gallery/make_gallery.py.</footer>
</body>
</html>
'''
    io.open(os.path.join(ROOT, 'gallery.html'), 'w', encoding='utf-8', newline='\n').write(page)
    io.open(os.path.join(HERE, 'route.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps([{'i': i, 'name': n, 'shot': s} for i, (n, _g, _t, _d, _r, _y, s) in enumerate(ROUTE, 1)], ensure_ascii=False, indent=1))
    print('wrote gallery.html with', len(ROUTE), 'examples')


if __name__ == '__main__':
    main('--shots' in sys.argv)
