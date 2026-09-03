# The first puzzles, after the originals: fix the ship's computer.
#
#   p1  a box with 1 and 2 in it, from a 1, a 2 and an empty box
#   p2  a 4, from two 2s (a number dropped on a number adds)
#   p3  a box with 8, 16 and 32 in it -- boxes join by dropping one on the
#       side of another
#   p4  a zero -- a number below zero adds itself and takes away
#   p5  a box with two zeros, made by a ROBOT you train, with Mimi to copy
#   p6  the sum of the numbers on a nest -- a robot that runs until the nest
#       is empty, and the first thought Ruby has to loosen
#   p7  exactly 1024 -- a robot that doubles and never stops by itself, so
#       YOU have to stop it in time
#   p8  a box inside a box inside a box
#   p9  a box of three zeros in the second hole of a box (Mimi copies)
#   p10 a box of six zeros from a box of two (copies joined side by side)
#   p11 the door code, 77, from a box of powers of two (a sum, by choosing)
#   p12 a half -- a 2 wearing a divide badge
#   p13 a million from a 10 and a times-ten badge, copied five times
#   p14 A, B and C on pads, in a box -- the first that lets you type
#   p15 the seconds in a year: 365 x 24 x 60 x 60, four numbers with badges
#   p16 a word from two pads joined at the edge -- order matters
#   p17 three quarters: a 1, a divide-by-four and a times-three
#   p18 which is bigger, 3/4 or 2/3: on a scale, the bigger on the left
#   p19 a box of 24 zeros from a box of three, doubled by copying and joining
#   p20 a robot moves stuck numbers across into a second box, in reverse
#       (a round that empties what it reads stops by itself)
#   p21 the same robot, other numbers: its thought is too fussy, so Ruby
#   p22 a robot counts the letters in the post, with Dusty and the number
#       stack; it dozes when the nest is empty
#   p23 a robot makes a box of exactly ten zeros, one more hole a round --
#       another one you have to stop in time
#   p24 the same robot with a SCALE: it counts the holes it makes against a
#       number in the other pan and stops by itself when the pans balance
#   p25 1,024 again, by a doubler that weighs itself against 1,000 and stops
#   p26 the biggest of three, found with a scale by hand
#   p27 a pair sorted into a box, smaller first, by hand
#   p28 a robot sorts a scale's pans -- stuck numbers, one run
#   p29 a box of letters poured onto a blank pad becomes the word
#   p30 a word dropped into a box with no holes comes apart, a letter a hole
#   p31 the third letter of "Marty": a pad dropped on a number picks it out
#   p32 down to one
#   p33 sort three: a team of four robots, trained on a practice box: a halver that weighs itself against 1 and stops
#
# Each is its own world file; the app carries the whole set by name (see
# embed_puzzles.py), and a server can fetch any of them.
#
# THE LAYOUT, the same on every table: what you work with at the FRONT (near
# you), the bird in the middle, the reply nest beside her, the goal and the
# judge at the back where they are seen and not in the way -- and Marty's
# ship, lying where it came down on the floor behind the table, big enough
# for him to have travelled in, so the story has something to point at.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _pz import *                                           # noqa: F403

FRONT = 2.05          # near the camera
MID = 1.55
BACK = 1.2


def ship():
    """Marty's ship, on its side on the floor behind the table: the reason
    for every puzzle. It came down HARD (Ken: "the broken spaceship can look
    more broken"): the nose is scorched and bent off the line of the hull,
    a gash runs along the side, the hull is dented, one fin snapped off and
    lies where it fell, a stripe is torn, bits of it are scattered about, and
    it still smokes. Scenery -- nothing runs into it, and nobody lifts it.
    Built at hand size and scaled up in SCENERY."""
    white, scorch, red, dark, glass = '#e9e4d8', '#3a3a3a', '#c0392b', '#1a1a1a', '#7fd4ff'
    parts = [
        # the hull, on its side
        {'shape': 'cylinder', 'size': [0.055, 0.05, 0.30], 'at': [0, 0.06, 0],
         'rot': [0, 0, 90], 'color': white},
        # a scorched band where the nose burnt
        {'shape': 'cylinder', 'size': [0.057, 0.052, 0.07], 'at': [0.12, 0.06, 0],
         'rot': [0, 0, 90], 'color': '#5a4a3a'},
        # the nose: bent up and to one side, off the line of the hull
        {'shape': 'cone', 'size': [0.05, 0.12], 'at': [0.21, 0.08, 0.02],
         'rot': [10, 0, -70], 'color': scorch},
        # a gash torn along the side, three dark slivers
        {'shape': 'box', 'size': [0.10, 0.012, 0.03], 'at': [-0.02, 0.085, 0.045],
         'rot': [0, 0, 8], 'color': dark},
        {'shape': 'box', 'size': [0.06, 0.012, 0.03], 'at': [0.07, 0.10, 0.03],
         'rot': [0, 0, -14], 'color': dark},
        {'shape': 'box', 'size': [0.04, 0.010, 0.03], 'at': [-0.10, 0.07, 0.05],
         'rot': [0, 0, 20], 'color': dark},
        # dents: dark flattened bumps on the hull
        {'shape': 'sphere', 'size': [0.022], 'at': [0.04, 0.045, -0.04], 'color': '#6b6b6b'},
        {'shape': 'sphere', 'size': [0.018], 'at': [-0.07, 0.10, -0.02], 'color': '#6b6b6b'},
        # one fin still on, bent
        {'shape': 'box', 'size': [0.08, 0.02, 0.12], 'at': [-0.15, 0.06, 0.05],
         'rot': [0, 0, 32], 'color': red},
        # ...the other snapped off, lying on the ground behind
        {'shape': 'box', 'size': [0.08, 0.02, 0.12], 'at': [-0.26, 0.012, -0.14],
         'rot': [0, 35, 0], 'color': red},
        # the stripe, torn in two
        {'shape': 'box', 'size': [0.06, 0.03, 0.10], 'at': [-0.05, 0.06, 0], 'color': red},
        {'shape': 'box', 'size': [0.05, 0.03, 0.10], 'at': [0.04, 0.062, 0.006],
         'rot': [0, 0, 6], 'color': red},
        # a porthole, cracked (a dark line across it)
        {'shape': 'sphere', 'size': [0.028], 'at': [0.05, 0.10, 0.045], 'color': glass},
        {'shape': 'box', 'size': [0.05, 0.004, 0.004], 'at': [0.05, 0.115, 0.06],
         'rot': [0, 0, 30], 'color': dark},
        # bits of it scattered where it slid
        {'shape': 'box', 'size': [0.03, 0.01, 0.02], 'at': [0.30, 0.005, 0.10],
         'rot': [0, 25, 0], 'color': white},
        {'shape': 'box', 'size': [0.025, 0.01, 0.02], 'at': [0.24, 0.005, -0.12],
         'rot': [0, -40, 0], 'color': scorch},
        {'shape': 'box', 'size': [0.02, 0.008, 0.035], 'at': [-0.05, 0.004, 0.16],
         'rot': [0, 60, 0], 'color': red},
        # smoke, still rising from the nose
        {'shape': 'sphere', 'size': [0.05], 'at': [0.24, 0.16, 0.02], 'color': '#5e5e5e'},
        {'shape': 'sphere', 'size': [0.038], 'at': [0.29, 0.24, -0.02], 'color': '#7a7a7a'},
        {'shape': 'sphere', 'size': [0.026], 'at': [0.33, 0.31, 0.01], 'color': '#939393'},
    ]
    return {'kind': 'model', 'parts': parts, 'fixed': True, 'ghost': True,
            'label': 'Marty’s ship'}


def width_of(thing):
    """How wide a thing stands on the table, in metres, the way the app draws
    it: a number is a cube, a box is its holes and walls (holes shrink to a
    floor as the count grows, then the box widens), a pad its face."""
    k = thing.get('kind')
    if k == 'box':
        n = len(thing.get('holes') or [])
        wall = 0.032
        hole_w = max(0.12, min(0.19, (0.62 - (n + 1) * wall) / max(1, n)))
        return n * hole_w + (n + 1) * wall
    if k == 'number':
        return 0.24
    if k == 'text':
        return 0.34
    return 0.26                                           # a mini robot, a nest


def table(materials, goal, post, reply, judge_, extra=()):
    """materials: things left to right across the front, spaced by how wide
    each one is (Ken: puzzle 9's boxes overlapped); the rest fixed."""
    widths = [width_of(m) for m in materials]
    gap = 0.14
    total = sum(widths) + gap * (len(widths) - 1)
    xs, x = [], -total / 2
    for w in widths:
        xs.append(x + w / 2)
        x += w + gap
    bench = [{'thing': m, 'x': round(x, 2), 'z': FRONT} for m, x in zip(materials, xs)]
    # THE GOAL AND THE POST KEEP OUT OF EACH OTHER'S WAY. The goal stands at
    # the back on the right, its right edge fixed, so it grows leftward; the
    # bird and her nest sit in the middle row on the left. A goal too wide for
    # that (24 zeros) is centred and the post moves to the front right, where
    # nothing stands in front of it. A small goal -- one number, one pad --
    # is shown half again as large (Ken: "tinier than need be").
    gw = width_of(goal)
    goal_rec = {'thing': goal, 'z': BACK}
    if gw < 0.5:
        goal_rec['thing'] = dict(goal, size=1.5)    # on the thing: that is where the reader looks
        gw *= 1.5
    if gw <= 1.3:
        goal_rec['x'] = round(1.45 - gw / 2, 2)
        post_x, post_z = -0.55, MID
    else:
        goal_rec['x'] = 0.1
        post_x, post_z = 1.05, FRONT
    bench += [{'thing': post, 'x': post_x, 'z': post_z},
              {'thing': reply, 'x': round(post_x + 0.5, 2), 'z': post_z},
              goal_rec,
              {'thing': judge_, 'x': -1.35, 'z': BACK}]
    bench += list(extra)
    return bench


def next_note(text):
    return [take('given', 2), put('given', 1)]              # noqa: F405


ROBOT = {'kind': 'robot', 'name': None, 'program': [], 'team': []}

# Where it came down: on the floor beyond the far side of the table, nose
# toward the room, seven times hand size -- a ship Marty could sit in.
SCENERY = [{'thing': ship(), 'x': 3.1, 'y': 0.0, 'z': -3.4, 'ry': 35, 'sz': 7}]

# --- p7: exactly 1024 -- and it is you who has to stop the robot ------------
# No box: a robot can set a thing down on its own desk where its given thing
# was (Ken: "why do we need a box -- original ToonTalk did but we don't").
P7 = puzzle(
    'p7',
    'Last of all the computer needs exactly 1,024 — and there is only a 1. A '
    'robot can double a number, but a doubling robot never stops by itself: '
    'you will have to stop it in time. Ask me for a hint if you need one.',
    'exactly 1,024',
    ['Give the robot the 1. In its imagination: click the 1 to pick it up, '
     'click Mimi to set it on her platform, click the copy in her tray, and '
     'click the robot’s desk to put the copy where the 1 was.',
     'Now click the original on Mimi’s platform and click the number on the '
     'desk: a number dropped on a number adds, and 1 on 1 is 2. Leave the '
     'thought bubble.',
     'Its thought wants exactly a 1. Wake Ruby and click the 1 in its thought '
     'until it says “any number”. Then give it the number and press Run.',
     'It doubles every round and will not stop by itself. Stop lets it finish '
     'the round it is in, so press Stop — or the full stop key — when the '
     'number says 512. Stopped at 512? Run and then Stop straight away is one '
     'more round. Past 1,024 is 2,048, and there is no way back but Start over.',
     'Here’s what I’d do. Drop the 1 on the robot; take the 1, set it on '
     'Mimi, take the copy and put it on the desk, take the original off the '
     'platform and drop it on the copy. Leave the thought bubble; wake Ruby '
     'and loosen the 1 in its thought. Give it the number, press Run, and '
     'press Stop when it reads 512; if it stops at 512, Run and Stop again '
     'for one more round. Take the 1,024 and give it to the bird.'],
    rules(tools=['mimi', 'ruby']),
    table([num(1), ROBOT],                                   # noqa: F405
          fixed(num(1024), 'we need this'),                  # noqa: F405
          bird(9971, 'p7-post', 'give me your answer'),      # noqa: F405
          nest(9972, 'p7-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9971, 'p7-post', 9972, 'p7-reply',
                right=num(1024),                             # noqa: F405
                on_right=next_note('') + [load('p8')],
                notes=['1,024 exactly — the computer is working again. '
                       'Next: boxes inside boxes.'],
                sorry='Not quite — it has to be exactly 1,024. Too small? Run '
                      'and Stop is one more round. Too big? Start over.')),
    scenery=SCENERY)

# --- p6: the sum of what came in the post -------------------------------------
P6 = puzzle(
    'p6',
    'The computer needs the total of the numbers that came in the post — '
    'three of them, on that nest. Train a robot to add them up, one a round, '
    'and give the bird the total. Ruby is here if its thought is too fussy.',
    'the total of the numbers on the nest',
    ['Give the robot the box with the nest in it. In its imagination, click '
     'the top number on the nest — the robot takes it — then click the zero '
     'to drop it there. A number dropped on a number adds.',
     'Look at its thought: it wants exactly the number it saw, and exactly '
     'a zero. Wake Ruby and click those parts until they say “any number”.',
     'With the thought loosened, give the robot the box again. It adds one '
     'number per round and dozes when the nest is empty.',
     'Here’s what I’d do. Drop the box on the robot; click the top number on '
     'the nest, then click the zero; leave the thought bubble. Wake Ruby, '
     'click the number in its thought and the zero in its thought. Give it '
     'the box, press Run, and when the nest is empty pick the total out of '
     'the box and give it to the bird.'],
    rules(tools=['ruby']),
    table([box(nest(9961, 'p6-pile', 'the post', pile=[num(2), num(3), num(4)]),   # noqa: F405
               dict(num(0), label='the total')),             # noqa: F405
           ROBOT],
          fixed(num(9), 'we need this'),                     # noqa: F405
          bird(9963, 'p6-post', 'give me your answer'),      # noqa: F405
          nest(9964, 'p6-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9963, 'p6-post', 9964, 'p6-reply',
                right=num(9),                                # noqa: F405
                on_right=next_note('') + [load('p7')],
                notes=['The total is in — the computer can count its post now. '
                       'Last: exactly 1,024.'])),
    scenery=SCENERY)

# --- p5: a robot makes a box with two zeros ----------------------------------
P5 = puzzle(
    'p5',
    'Sometimes to get things done I have to train robots to do work for me. '
    'See if you can train a robot to make a box with two zeros in it. Mimi the '
    'copier is here to help. Give the box to the bird when you have it.',
    'a box with two zeros in it',
    ['You can train the robot if you give it the box with the zero in it. '
     'You’ll end up in its imagination, and it remembers whatever you do.',
     'Set the box on Mimi’s platform: a copy drops into the tray.',
     'Drop the copy on the side of the box and they join into one box.',
     'Here’s what I’d do. I’d drop the box on the robot. Then I’d have it '
     'set the box on Mimi, take the copy, and drop the copy on the side of '
     'the box. When I leave its thought bubble, I’d give it the box and let '
     'it work — then give the bird the box it made.'],
    rules(tools=['mimi']),      # no cap: there is no lazy way to make this box
    table([box(num(0)), ROBOT],                              # noqa: F405
          fixed(box(num(0), num(0)), 'we need this'),      # noqa: F405
          bird(9951, 'p5-post', 'give me your answer'),    # noqa: F405
          nest(9952, 'p5-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 9951, 'p5-post', 9952, 'p5-reply',
                right=box(num(0), num(0)),                  # noqa: F405
                on_right=next_note('') + [load('p6')],
                notes=['You trained a robot! The computer has its zeros. '
                       'Next: the post.'])),
    scenery=SCENERY)

# --- p4: a zero --------------------------------------------------------------
P4 = puzzle(
    'p4',
    'The computer’s going to need a zero to work. One of these numbers is '
    'below zero — a minus three. A number dropped on another adds itself, '
    'and adding a minus three takes three away. Give the bird a zero.',
    'a zero',
    ['One of the 3s is a MINUS three. Dropping a number on a number adds them.',
     'Drop the minus three on the plain 3 — or the 3 on the minus three; either '
     'way they add up to nothing.',
     'Here’s what I’d do: pick up the minus three and drop it on the plain 3. '
     'That leaves a 0. Give the 0 to the bird.'],
    rules(),
    table([num(3), num(-3)],                                 # noqa: F405
          fixed(num(0), 'we need this'),                     # noqa: F405
          bird(9941, 'p4-post', 'give me your answer'),      # noqa: F405
          nest(9942, 'p4-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9941, 'p4-post', 9942, 'p4-reply',
                right=num(0),                                # noqa: F405
                on_right=next_note('') + [load('p5')],
                notes=['A zero — just what the computer needed. Next: robots.'])),
    scenery=SCENERY)

# --- p3: a box with 8, 16 and 32 ----------------------------------------------
P3 = puzzle(
    'p3',
    'Thanks. Now see if you can make a box with 8, 16 and 32 inside, and give '
    'it to the bird.',
    'a box with 8, 16 and 32 in it',
    ['Did you know that boxes click together when you drop one on the side '
     'of another?',
     'A 16 dropped on a 16 makes a 32 — right there in its box.',
     'OK, here’s what I’d do. I’d drop the loose 16 on the 16 in the box on '
     'the right, which turns it into 32. Then I’d drop the box with 8 on the '
     'LEFT side of the box with 16, and the box with 32 on the RIGHT side of '
     'that. Then I’d give the whole box to the bird.'],
    rules(),
    table([box(num(8)), box(num(16)), box(num(16)), num(16)],   # noqa: F405
          fixed(box(num(8), num(16), num(32)), 'we need this'),  # noqa: F405
          bird(9931, 'p3-post', 'give me your answer'),      # noqa: F405
          nest(9932, 'p3-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9931, 'p3-post', 9932, 'p3-reply',
                right=box(num(8), num(16), num(32)),         # noqa: F405
                on_right=next_note('') + [load('p4')],
                notes=['Three numbers in a row — the computer is filling up. '
                       'Next: a zero.'])),
    scenery=SCENERY)

# --- p2: we need a 4 ---------------------------------------------------------
P2 = puzzle(
    'p2',
    'Did you notice that things wiggle when they are ready to be picked up? '
    'OK, now we’ll need a 4. Give it to the bird when you have one.',
    'a 4',
    ['Try putting the twos together.',
     'Drop a 2 on a 2 and wait until it turns into a 4.',
     'OK, here’s all you have to do: drop one 2 on the other. When it '
     'turns into a 4, pick up the 4 and give it to the bird.'],
    rules(),
    table([num(2), num(2)],                                  # noqa: F405
          fixed(num(4), 'we need this'),                     # noqa: F405
          bird(9911, 'p2-post', 'give me your answer'),      # noqa: F405
          nest(9912, 'p2-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9911, 'p2-post', 9912, 'p2-reply',
                right=num(4),                                # noqa: F405
                on_right=next_note('') + [load('p3')],
                notes=['That’s it! The computer has its 4. Next: a box of three.'])),
    scenery=SCENERY)

# --- p1: we need a box with 1 and 2 in it -----------------------------------
puzzle(
    'p1',
    'Thanks for coming to help me. My ship came down hard — that’s it lying '
    'on the floor behind the table with its nose burnt — and its computer is broken. First it '
    'needs numbers to work. Can you make a box with 1 and 2 in it, and give '
    'it to the bird? If you get stuck, ask me for a hint.',
    'a box with 1 and 2 in it, in that order',
    ['Did you notice that you can pick up numbers and let go of them over '
     'holes in the box?',
     'Put the 1 in the first hole and the 2 in the second — the order '
     'matters, the judge reads a box hole by hole. Then pick up the whole '
     'box and give it to the bird.',
     'OK, here’s what I’d do if I could. I’d pick up the 1 and '
     'drop it in the first hole. Then I’d pick up the 2 and drop it in '
     'the second hole. Then I’d grab the whole box and give it to the '
     'bird.'],
    rules(),
    table([num(1), num(2), empty_box(2)],                    # noqa: F405
          fixed(box(num(1), num(2)), 'we need this'),        # noqa: F405
          bird(9901, 'p1-post', 'give me your answer'),      # noqa: F405
          nest(9902, 'p1-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9901, 'p1-post', 9902, 'p1-reply',
                right=box(num(1), num(2)),                   # noqa: F405
                on_right=next_note('') + [load('p2')],
                notes=['Well done — the computer has its first numbers. '
                       'Press Next when you are ready.'])),
    scenery=SCENERY)

# ============================================================================
# The second seven, after the originals' next steps: boxes in boxes, more
# zeros, numbers made by choosing, dividing and multiplying, and letters.

# --- p8: a box inside a box inside a box --------------------------------------
puzzle(
    'p8',
    'Now the computer wants boxes with boxes inside. To practise, put a box '
    'inside a box inside a box — three boxes, each in the FIRST hole of the '
    'next — and give the outside one to the bird.',
    'a box inside a box inside a box, each in the first hole of the next',
    ['A box goes into a hole like anything else.',
     'Drop one box into the first hole of another. Then pick up THAT box and '
     'drop it into the first hole of the third.',
     'Here’s what I’d do: drop the first box into the second box’s left hole; '
     'pick up the second box and drop it into the third box’s left hole; give the '
     'third box to the bird.'],
    rules(),
    table([empty_box(2), empty_box(2), empty_box(2)],
          fixed(box(box(box(None, None), None), None), 'we need this'),      # noqa: F405
          bird(9981, 'p8-post', 'give me your answer'),      # noqa: F405
          nest(9982, 'p8-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9981, 'p8-post', 9982, 'p8-reply',
                right=box(box(box(None, None), None), None),                   # noqa: F405
                on_right=next_note('') + [load('p9')],
                notes=['Three deep — the computer likes that. Next: zeros '
                       'in a box in a box.'])),
    scenery=SCENERY)

# --- p9: three zeros, in the second hole of a box ------------------------------
puzzle(
    'p9',
    'See if you can make a box with three zeros in it, and put it in the '
    'SECOND hole of the other box. There is only one zero; Mimi makes more.',
    'a box with three zeros in the second hole of a two-hole box',
    ['Set the zero on Mimi’s platform and a copy drops into her tray — take '
     'the copy, and the original comes back off the platform.',
     'Fill the three-hole box with zeros first. Then drop that box into the '
     'second hole of the two-hole box — the right-hand one.',
     'Here’s what I’d do: copy the zero twice with Mimi, drop the three zeros '
     'into the three-hole box, drop that box into the right-hand hole of the '
     'two-hole box, and give the two-hole box to the bird.'],
    rules(tools=['mimi']),
    table([num(0), empty_box(3), empty_box(2)],              # noqa: F405
          fixed(box(None, box(num(0), num(0), num(0))), 'we need this'),   # noqa: F405
          bird(9991, 'p9-post', 'give me your answer'),      # noqa: F405
          nest(9992, 'p9-reply', 'from the judge'),          # noqa: F405
          judge('the judge', 9991, 'p9-post', 9992, 'p9-reply',
                right=box(None, box(num(0), num(0), num(0))),   # noqa: F405
                on_right=next_note('') + [load('p10')],
                notes=['Zeros in the second hole — just so. Next: six of '
                       'them.'])),
    scenery=SCENERY)

# --- p10: six zeros -----------------------------------------------------------
puzzle(
    'p10',
    'Now the computer needs a box with six zeros. You have a box with two, '
    'and Mimi.',
    'a box with six zeros in it',
    ['Mimi copies boxes as happily as numbers: set the box on her platform '
     'and a copy of the whole box drops into her tray. Take the copy, and '
     'then the box itself comes back off the platform.',
     'Boxes join when you drop one on the side of another — or set one down '
     'with its edge over the other’s edge.',
     'Two zeros and two zeros and two zeros: three boxes joined side by side '
     'is six holes.',
     'Here’s what I’d do: set the box on Mimi, take the copy out of the tray '
     'and set it down, take the box back off the platform, and drop one on '
     'the side of the other. Once more for the third pair of zeros, and give '
     'the long box to the bird.'],
    rules(tools=['mimi']),
    table([box(num(0), num(0))],                             # noqa: F405
          fixed(box(*[num(0) for _ in range(6)]), 'we need this'),   # noqa: F405
          bird(10001, 'p10-post', 'give me your answer'),    # noqa: F405
          nest(10002, 'p10-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10001, 'p10-post', 10002, 'p10-reply',
                right=box(*[num(0) for _ in range(6)]),      # noqa: F405
                on_right=next_note('') + [load('p11')],
                notes=['Six zeros in a row. Next: a number made by '
                       'choosing.'])),
    scenery=SCENERY)

# --- p11: the door code -------------------------------------------------------
puzzle(
    'p11',
    'With ones, twos, fours and so on the computer can make any number at '
    'all. The ship’s door code is 77 — make it from the numbers in this box. '
    'A number dropped on a number adds, and each of these may be used once.',
    'exactly 77',
    ['Every number is a sum of some of these, each used at most once. Start '
     'with the biggest that fits under 77.',
     '64 fits, and 77 take away 64 is 13. Which of these make 13?',
     'Here’s what I’d do: take the 64 out, drop the 8 on it, then the 4, '
     'then the 1 — 64, 72, 76, 77 — and give the 77 to the bird.'],
    rules(),
    table([box(num(1), num(2), num(4), num(8), num(16), num(32), num(64))],   # noqa: F405
          fixed(num(77), 'we need this'),                    # noqa: F405
          bird(10011, 'p11-post', 'give me your answer'),    # noqa: F405
          nest(10012, 'p11-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10011, 'p11-post', 10012, 'p11-reply',
                right=num(77),                               # noqa: F405
                on_right=next_note('') + [load('p12')],
                notes=['77 — the door opens. Next: a number smaller than '
                       'one.'],
                sorry='Not quite — the code is exactly 77. Each number in '
                      'the box may be used once.')),
    scenery=SCENERY)

# --- p12: a half --------------------------------------------------------------
puzzle(
    'p12',
    'The computer divides as well as adds. That 2 wears a divide badge: '
    'dropped on a number, it divides the number by 2 instead of adding. We '
    'need a half.',
    'a half',
    ['Look at the badge on the 2: that is what it does when it lands on a '
     'number.',
     'Drop the 2 on the 1 — not the 1 on the 2.',
     'Here’s what I’d do: pick up the 2 with the divide badge, drop it on the '
     '1, and give the half to the bird.'],
    rules(),
    table([num(1), num(2, op='/')],                          # noqa: F405
          fixed(num(1, 2), 'we need this'),                  # noqa: F405
          bird(10021, 'p12-post', 'give me your answer'),    # noqa: F405
          nest(10022, 'p12-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10021, 'p12-post', 10022, 'p12-reply',
                right=num(1, 2),                             # noqa: F405
                on_right=next_note('') + [load('p13')],
                notes=['A half — the computer can share now. Next: a '
                       'million.'])),
    scenery=SCENERY)

# --- p13: a million -----------------------------------------------------------
puzzle(
    'p13',
    'The computer needs a million. You have a 10, a 10 wearing a times '
    'badge, and Mimi.',
    'a million',
    ['A times badge multiplies the number it lands on — and the badge '
     'number is used up when it lands.',
     'Times ten on 10 is 100 — and the times-ten is gone. Copy it with Mimi '
     'before you use it.',
     '10, 100, 1,000, 10,000, 100,000, 1,000,000: that is five times-tens.',
     'Here’s what I’d do: set the times-ten on Mimi and take a copy; do that '
     'until there are five; drop them on the 10 one after another; give the '
     'bird the million.'],
    rules(tools=['mimi']),
    table([num(10), num(10, op='*')],                        # noqa: F405
          fixed(num(1000000), 'we need this'),               # noqa: F405
          bird(10031, 'p13-post', 'give me your answer'),    # noqa: F405
          nest(10032, 'p13-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10031, 'p13-post', 10032, 'p13-reply',
                right=num(1000000),                          # noqa: F405
                on_right=next_note('') + [load('p14')],
                notes=['A million! Next: the computer wants letters.'],
                sorry='Not quite — exactly one million, six figures of it.')),
    scenery=SCENERY)

# --- p14: A, B and C ----------------------------------------------------------
puzzle(
    'p14',
    'The computer needs more than numbers — it needs letters and words. Put '
    'a capital A, a B and a C on these blank pads, in the box in that order, '
    'and give the box to the bird.',
    'a box with A, B and C on pads, in that order',
    ['Hold a pad and press a letter key: the keyboard writes on what you '
     'hold.',
     'A capital letter — hold Shift. Backspace takes a letter back.',
     'Here’s what I’d do: pick up a pad, press Shift and A, drop it in the '
     'first hole; the same with B into the second and C into the third; give '
     'the box to the bird.'],
    rules(typing={'numbers': False, 'pads': True}),
    table([pad(''), pad(''), pad(''), empty_box(3)],         # noqa: F405
          fixed(box(txt('A'), txt('B'), txt('C')), 'we need this'),   # noqa: F405
          bird(10041, 'p14-post', 'give me your answer'),    # noqa: F405
          nest(10042, 'p14-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10041, 'p14-post', 10042, 'p14-reply',
                right=box(txt('A'), txt('B'), txt('C')),     # noqa: F405
                on_right=next_note('') + [load('p15')],
                notes=['A, B, C — the computer can spell. Next: a whole '
                       'year, in seconds.'],
                sorry='Not quite — capital A, B and C, one to a pad, in that '
                      'order.')),
    scenery=SCENERY)

# ============================================================================
# The third batch: multiplying, words, fractions, a scale, and doubling boxes.

# --- p15: the seconds in a year -----------------------------------------------
puzzle(
    'p15',
    'The computer keeps time in seconds, and it wants to know how many there '
    'are in a year: 365 days, 24 hours in a day, 60 minutes in an hour, 60 '
    'seconds in a minute. Three of these wear times badges. Give the bird '
    'the answer.',
    'the seconds in a year',
    ['A number wearing a times badge multiplies the number it lands on.',
     'Start with the 365 and drop the badge numbers on it, one after another: '
     'days, then hours, then minutes, then seconds.',
     'Here’s what I’d do: drop the ×24 on the 365 (8,760), then the first ×60 '
     'on that (525,600), then the other ×60 (31,536,000). Give the bird the '
     '31,536,000.'],
    rules(),
    table([num(365), num(24, op='*'), num(60, op='*'), num(60, op='*')],   # noqa: F405
          fixed(num(31536000), 'we need this'),              # noqa: F405
          bird(10051, 'p15-post', 'give me your answer'),    # noqa: F405
          nest(10052, 'p15-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10051, 'p15-post', 10052, 'p15-reply',
                right=num(31536000),                         # noqa: F405
                on_right=next_note('') + [load('p16')],
                notes=['31,536,000 seconds — the computer can keep a '
                       'calendar. Next: a word.'],
                sorry='Not quite — 365 × 24 × 60 × 60. Each badge lands '
                      'once; Start over if one is spent.')),
    scenery=SCENERY)

# --- p16: a word ------------------------------------------------------------
puzzle(
    'p16',
    'The computer needs a word, and it needs it on one pad: “ToonTalk”. '
    'Give the bird the pad.',
    'one pad that says ToonTalk',
    ['Drop a pad on the edge of another pad — or set it down with its edge '
     'over the other’s — and the words join into one.',
     'Which edge matters: “Talk” dropped on the RIGHT edge of “Toon” reads '
     'ToonTalk; on the left edge it reads TalkToon.',
     'Here’s what I’d do: pick up the Talk pad and drop it on the right-hand '
     'edge of the Toon pad. Give the bird the ToonTalk pad.'],
    rules(),
    table([pad('Toon'), pad('Talk')],                        # noqa: F405
          fixed(pad('ToonTalk'), 'we need this'),            # noqa: F405
          bird(10061, 'p16-post', 'give me your answer'),    # noqa: F405
          nest(10062, 'p16-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10061, 'p16-post', 10062, 'p16-reply',
                right=txt('ToonTalk'),                       # noqa: F405
                on_right=next_note('') + [load('p17')],
                notes=['ToonTalk, on one pad. Next: three quarters.'],
                sorry='Not quite — one pad reading exactly ToonTalk; the '
                      'right-hand edge puts Talk after Toon.')),
    scenery=SCENERY)

# --- p17: three quarters ------------------------------------------------------
puzzle(
    'p17',
    'The computer needs three quarters. You have a 1, a 4 wearing a divide '
    'badge and a 3 wearing a times badge. Dividing and multiplying are '
    'badges here — the number underneath is what changes.',
    'three quarters',
    ['A divide badge divides the number it lands on; a times badge multiplies '
     'it.',
     'One divided by four is a quarter; a quarter times three is three '
     'quarters.',
     'Here’s what I’d do: drop the ÷4 on the 1 — it reads ¼ — then drop the ×3 '
     'on that. Give the bird the ¾.'],
    rules(),
    table([num(1), num(4, op='/'), num(3, op='*')],          # noqa: F405
          fixed(num(3, 4), 'we need this'),                  # noqa: F405
          bird(10071, 'p17-post', 'give me your answer'),    # noqa: F405
          nest(10072, 'p17-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10071, 'p17-post', 10072, 'p17-reply',
                right=num(3, 4),                             # noqa: F405
                on_right=next_note('') + [load('p18')],
                notes=['Three quarters. Next: which is bigger?'])),
    scenery=SCENERY)

# --- p18: which is bigger ------------------------------------------------------
puzzle(
    'p18',
    'The computer cannot tell which is bigger, three quarters or two thirds. '
    'Put them on the scale — the bigger one on the LEFT — and give the bird '
    'the scale.',
    'a scale with the bigger of ¾ and ⅔ on the left',
    ['A scale has two pans. Drop a number in each and it tips toward the '
     'bigger one.',
     'Try them one way; if the scale tips to the right, swap them.',
     'Here’s what I’d do: drop the ¾ in the left pan and the ⅔ in the right — '
     'the scale tips left. Give the bird the scale.'],
    rules(),
    table([num(3, 4), num(2, 3), scale(None, None)],         # noqa: F405
          fixed(scale(num(3, 4), num(2, 3)), 'we need this'),   # noqa: F405
          bird(10081, 'p18-post', 'give me your answer'),    # noqa: F405
          nest(10082, 'p18-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10081, 'p18-post', 10082, 'p18-reply',
                right=scale(num(3, 4), num(2, 3)),           # noqa: F405
                on_right=next_note('') + [load('p19')],
                notes=['Three quarters it is — the scale says so. Next: a '
                       'long box of zeros.'],
                sorry='Not quite — the bigger number goes in the LEFT pan.')),
    scenery=SCENERY)

# --- p19: twenty-four zeros ------------------------------------------------------
puzzle(
    'p19',
    'The computer needs a box with exactly 24 zeros. You have a box of three, '
    'and Mimi.',
    'a box with exactly 24 zeros in it',
    ['Mimi copies a whole box. Set it on her platform and take the copy; '
     'take the box back off the platform.',
     'Boxes join side to side: a box of three and a copy of it make six.',
     'Three, six, twelve, twenty-four: three doublings.',
     'Here’s what I’d do: copy and join to make six; copy and join to make '
     'twelve; copy and join to make twenty-four; give the bird the box. A box '
     'that long shows its ends and says how many holes are between.'],
    rules(tools=['mimi']),
    table([box(num(0), num(0), num(0))],                     # noqa: F405
          fixed(box(*[num(0) for _ in range(24)]), 'we need this'),   # noqa: F405
          bird(10091, 'p19-post', 'give me your answer'),    # noqa: F405
          nest(10092, 'p19-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10091, 'p19-post', 10092, 'p19-reply',
                right=box(*[num(0) for _ in range(24)]),     # noqa: F405
                on_right=next_note('') + [load('p20')],
                notes=['Twenty-four zeros exactly. Next: a robot that turns '
                       'a box round.'],
                sorry='Not quite — exactly 24 zeros. Too few? Copy and join '
                      'again. Too many? Start over.')),
    scenery=SCENERY)

# ============================================================================
# The fourth batch: robots. One plans, one counts and stops by itself, one
# has to be stopped.

# --- p20: turn the numbers round ------------------------------------------------
# Two boxes: the numbers are moved ACROSS, last to first. A round that empties
# the box it reads cannot fit its own thought again, so the robot stops by
# itself -- where a swap inside one box would reverse it back for ever.
puzzle(
    'p20',
    'The computer wants these numbers the other way round — 1, 2, 3 — in the '
    'empty box beside them. They are stuck fast in their holes: your fingers '
    'cannot shift them, but a robot’s claw can. Train the robot and give the '
    'bird what it makes.',
    'a box holding an empty box and a box that reads 1, 2, 3',
    ['Drop the box on the robot and you are inside its imagination, where you '
     'move things by clicking: click a number, then click the hole it should '
     'go to. Its claw is stronger than your fingers.',
     'Last first: the 3 goes to the LAST hole of the empty box, the 2 to the '
     'middle, the 1 to the first.',
     'Here’s what I’d do. Drop the box on the robot. In its imagination: '
     'click the 3, click the last hole of the empty box; click the 2, click '
     'its middle hole; click the 1, click its first hole. Leave the thought '
     'bubble and give the bird the box.'],
    rules(),
    table([box(box(stuck(num(3)), stuck(num(2)), stuck(num(1))), empty_box(3)),   # noqa: F405
           ROBOT],
          fixed(box(empty_box(3), box(stuck(num(1)), stuck(num(2)), stuck(num(3)))),   # noqa: F405
                'we need this'),
          bird(10101, 'p20-post', 'give me your answer'),    # noqa: F405
          nest(10102, 'p20-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10101, 'p20-post', 10102, 'p20-reply',
                right=box(empty_box(3), box(stuck(num(1)), stuck(num(2)), stuck(num(3)))),   # noqa: F405
                on_right=next_note('') + [load('p21')],
                notes=['1, 2, 3 — the robot turned them round. Next: the '
                       'same robot, other numbers.'],
                sorry='Not quite — 1, 2, 3 in the second box, in that order, '
                      'and the first box empty.')),
    scenery=SCENERY)

# --- p21: the same robot, other numbers ----------------------------------------
# The robot from p20, already trained -- and too fussy: its thought names the
# very numbers it first saw. Ruby is the whole puzzle.
REVERSER = robot(                                             # noqa: F405
    'the turner',
    box(box(num(3), num(2), num(1)), empty_box(3)),           # noqa: F405
    [take('given', 0, 0), put('given', 1, 2),                 # noqa: F405
     take('given', 0, 1), put('given', 1, 1),                 # noqa: F405
     take('given', 0, 2), put('given', 1, 0)],                # noqa: F405
    trained_on=box(box(num(3), num(2), num(1)), empty_box(3)))   # noqa: F405

puzzle(
    'p21',
    'Here is the robot you trained, and three different numbers — stuck fast '
    'again. Give it the box and see what happens: it remembers exactly the '
    'numbers it first saw. Ruby is here. The computer wants 4, 6, 8 in that '
    'order.',
    'a box holding an empty box and a box that reads 4, 6, 8',
    ['Give the robot the box and look at its thought: the parts that do not '
     'fit are marked red.',
     'Wake Ruby and click a red number in the thought: it forgets which '
     'number that was and says “any number” instead. Do that for each.',
     'The moment its thought fits, it runs by itself.',
     'Here’s what I’d do. Drop the box on the robot; it refuses and shows '
     'its thought. Wake Ruby, click each red number until it says any '
     'number. It runs; give the bird the box.'],
    rules(tools=['ruby']),
    table([box(box(stuck(num(8)), stuck(num(6)), stuck(num(4))), empty_box(3)),   # noqa: F405
           REVERSER],
          fixed(box(empty_box(3), box(stuck(num(4)), stuck(num(6)), stuck(num(8)))),   # noqa: F405
                'we need this'),
          bird(10131, 'p21-post', 'give me your answer'),    # noqa: F405
          nest(10132, 'p21-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10131, 'p21-post', 10132, 'p21-reply',
                right=box(empty_box(3), box(stuck(num(4)), stuck(num(6)), stuck(num(8)))),   # noqa: F405
                on_right=next_note('') + [load('p22')],
                notes=['4, 6, 8 — one robot, any numbers. Next: counting '
                       'the post.'],
                sorry='Not quite — 4, 6, 8 in the second box, in that order, '
                      'and the first box empty.')),
    scenery=SCENERY)

# --- p22: count the post --------------------------------------------------------
# Dusty rather than a bird: a bird has to fly home between rounds, and the
# robot's thought wants her back in her hole. What the robot holds IS its own
# thing, so Dusty may take it even in a lesson.
puzzle(
    'p22',
    'Letters keep arriving for the computer, and it wants to know how many. '
    'There are four on that nest. Train a robot to count them and give the '
    'bird the count. Dusty and Ruby are here, and the robot may take a '
    'number from the stack.',
    'the number of letters on the nest',
    ['Counting is adding one for each letter — and the letter itself has to '
     'go, or the robot will count it again.',
     'One round: wake Dusty and click the top letter on the nest — gone. '
     'Then click the number stack for a fresh 1 and drop it on the count.',
     'Its thought will want exactly the letter it saw and exactly the count '
     'it saw. Wake Ruby and click each until they say “any pad” and “any '
     'number”.',
     'Here’s what I’d do. Drop the box on the robot; wake Dusty and click '
     'the top letter on the nest; put Dusty back to sleep; click the number '
     'stack, click the count. Leave the thought bubble; '
     'wake Ruby and loosen the letter and the count. Give it the box, press '
     'Run, and when it dozes take the 4 out and give it to the bird.'],
    rules(stacks=['numbers'], tools=['dusty', 'ruby']),
    table([box(nest(10213, 'p22-pile', 'the post',
                    pile=[pad('A'), pad('B'), pad('C'), pad('D')]),   # noqa: F405
               dict(num(0), label='the count')),            # noqa: F405
           ROBOT],
          fixed(num(4), 'we need this'),                     # noqa: F405
          bird(10211, 'p22-post', 'give me your answer'),    # noqa: F405
          nest(10212, 'p22-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10211, 'p22-post', 10212, 'p22-reply',
                right=num(4),                                # noqa: F405
                on_right=next_note('') + [load('p23')],
                notes=['Four letters — counted by a robot. Next: ten '
                       'zeros, and you have to stop it.'],
                sorry='Not quite — the count of the letters on the nest, '
                      'a plain 4.')),
    scenery=SCENERY)

# --- p23: exactly ten zeros ------------------------------------------------------
# The given box holds the growing box in its first hole and a SEED box of one
# zero in its second: a round copies the seed and joins the copy on, so the
# box grows by one hole a round -- and never stops.
puzzle(
    'p23',
    'The computer wants a box with exactly ten zeros, made by a robot. In '
    'the first hole of this box is a box of one zero to grow; in the second, '
    'another to copy from. A robot that makes a box longer never stops by '
    'itself — you will have to stop it in time.',
    'a box with exactly ten zeros, made by a robot',
    ['One round should make the box in the first hole one hole longer. The '
     'box in the second hole is the seed: copy it, never spend it.',
     'In its imagination: click the seed box, click Mimi, click the copy in '
     'the tray, click the right-hand edge of the box in the first hole — they '
     'join; click the seed on Mimi’s platform, click the second hole.',
     'Its thought wants exactly the boxes it saw, and the first one grows. '
     'Wake Ruby and click the first box in its thought until it says “any '
     'box — any number of holes”; loosen the second too. Give it the box and '
     'press Run.',
     'Stop lets it finish the round it is in. Press Stop — or the full stop '
     'key — when the first box reads nine. Stopped at nine? Run and then '
     'Stop straight away is one more round: ten.',
     'Here’s what I’d do. Drop the box on the robot; click the seed, click '
     'Mimi, click the copy, click the right edge of the growing box; click '
     'the seed on the platform, click the second hole. Leave the thought '
     'bubble; wake Ruby and click the first box in its thought until it says '
     'any box, and the second once or twice. Give it the box, press Run, '
     'press Stop when it reads nine — Run and Stop again if it stopped at '
     'nine. Take the box of ten out of the first hole and give it to the '
     'bird.'],
    rules(tools=['mimi', 'ruby']),
    table([box(box(num(0)), box(num(0))), ROBOT],             # noqa: F405
          fixed(box(*[num(0) for _ in range(10)]), 'we need this'),   # noqa: F405
          bird(10231, 'p23-post', 'give me your answer'),    # noqa: F405
          nest(10232, 'p23-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10231, 'p23-post', 10232, 'p23-reply',
                right=box(*[num(0) for _ in range(10)]),     # noqa: F405
                on_right=next_note('') + [load('p24')],
                notes=['Ten zeros exactly, by robot. Next: a robot that '
                       'knows when to stop.'],
                sorry='Not quite — exactly ten zeros, the box itself out of '
                      'the first hole. Too few? Run and Stop is one more '
                      'round. Too many? Start over.')),
    scenery=SCENERY)

# --- p24: a robot that knows when to stop ------------------------------------------
# The grower again, with a scale in the third hole: a count in the left pan
# and the number wanted in the right. While the scale tips right the thought
# fits; when the pans balance it does not, and the robot stops on its own --
# which is how a robot makes a box of ANY number of zeros: change the number
# in the right pan.
puzzle(
    'p24',
    'Last time you had to stop the robot yourself. This time it should know '
    'when to stop: the computer wants seven zeros, and the box has a scale in '
    'its third hole with a count in one pan and the 7 in the other. A robot '
    'only runs while its thought fits — and a scale in a thought remembers '
    'which way it tipped.',
    'a box with exactly seven zeros, made by a robot that stopped by itself',
    ['The scale tips toward the bigger number. Right now the count is 1 and '
     'the 7 is bigger, so it tips right. The robot should count every hole '
     'it adds — a fresh 1 from the number stack, dropped on the count.',
     'Train the round as before — copy the seed, join the copy on, put the '
     'seed back — and then take a 1 from the stack and drop it on the count '
     'in the left pan. Leave the thought bubble.',
     'Its thought says the scale tips RIGHT. Wake Ruby and loosen the growing '
     'box and the count to “any”; the tilt stays. Now it runs while the count '
     'is smaller than 7 and stops when the pans balance.',
     'Here’s what I’d do. Drop the box on the robot; click the seed, click '
     'Mimi, click the copy, click the right edge of the growing box; click the '
     'seed on the platform, click the second hole; click the number stack, '
     'click the count in the scale’s left pan. Leave the thought bubble. Wake '
     'Ruby; click the first box in its thought until it says any box, and the '
     'count until it says any number. Press Run — it still has the box — and wait: '
     'it stops at seven. Take the box of seven out and give it to the bird.'],
    rules(stacks=['numbers'], tools=['mimi', 'ruby']),
    table([box(box(num(0)), box(num(0)), scale(num(1), num(7))), ROBOT],   # noqa: F405
          fixed(box(*[num(0) for _ in range(7)]), 'we need this'),   # noqa: F405
          bird(10241, 'p24-post', 'give me your answer'),    # noqa: F405
          nest(10242, 'p24-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10241, 'p24-post', 10242, 'p24-reply',
                right=box(*[num(0) for _ in range(7)]),      # noqa: F405
                on_right=next_note('') + [load('p25')],
                notes=['Seven zeros, and the robot stopped by itself. Change '
                       'the number in the pan and it would make any number '
                       'of them. Next: 1,024 again — hands off this time.'],
                sorry='Not quite — exactly seven zeros, the box itself out of '
                      'the first hole.')),
    scenery=SCENERY)

# ============================================================================
# The fifth batch: scales that stop robots, scales by hand, and letters.

# --- p25: 1,024, hands off -------------------------------------------------------
puzzle(
    'p25',
    'Remember 1,024, and how you had to stop the robot yourself? This time '
    'the robot should stop on its own. The number is in the left pan of a '
    'scale and 1,000 is in the right; the computer wants the first doubling '
    'that tips the scale the other way — which is 1,024.',
    'exactly 1,024, from a robot that stopped by itself',
    ['The scale tips right while the number is smaller than 1,000. A thought '
     'that says “tipping right” fits only then.',
     'Train the doubling round on the number in the pan: take it, set it on '
     'Mimi, take the copy, put it back in the pan, take the original, drop it '
     'on the copy. Leave the thought bubble.',
     'Wake Ruby and loosen the number in the thought to “any number”; the '
     'tilt stays. Press Run — it still has the box: it doubles until the scale '
     'tips left, and that is 1,024.',
     'Here’s what I’d do. Drop the box on the robot; click the 1 in the pan, '
     'click Mimi, click the copy, click the empty left pan, click the '
     'original on the platform, click the number in the pan. Leave the '
     'thought bubble; wake Ruby and loosen the number. Give it the box, press '
     'Run, and wait. Take the 1,024 out of the pan and give it to the bird.'],
    rules(tools=['mimi', 'ruby']),
    table([box(scale(num(1), num(1000))), ROBOT],             # noqa: F405
          fixed(num(1024), 'we need this'),                  # noqa: F405
          bird(10251, 'p25-post', 'give me your answer'),    # noqa: F405
          nest(10252, 'p25-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10251, 'p25-post', 10252, 'p25-reply',
                right=num(1024),                             # noqa: F405
                on_right=next_note('') + [load('p26')],
                notes=['1,024, and nobody had to watch it. Next: the '
                       'biggest of three.'],
                sorry='Not quite — 1,024 exactly, the first doubling past a '
                      'thousand.')),
    scenery=SCENERY)

# --- p26: the biggest of three ---------------------------------------------------
# Fractions close enough that nobody can tell by eye (Ken: with 23, 31 and 29
# most players already knew which way the scale would tilt).
puzzle(
    'p26',
    'The computer wants the biggest of these three fractions, and neither it '
    'nor you can tell by looking which that is — but a scale can. Give the '
    'bird the biggest.',
    'the biggest of the three fractions',
    ['A scale tips toward the bigger number, fractions included. Put two in '
     'its pans.',
     'Keep the heavier one on the scale and try it against the third.',
     'Here’s what I’d do: put the 5/7 and the 8/11 on the scale — it tips '
     'toward the 8/11; take the 5/7 off and put the 13/18 in its place — it '
     'still tips toward the 8/11. Give the bird the 8/11.'],
    rules(),
    table([num(5, 7), num(8, 11), num(13, 18), scale(None, None)],    # noqa: F405
          fixed(num(8, 11), 'we need this'),                 # noqa: F405
          bird(10261, 'p26-post', 'give me your answer'),    # noqa: F405
          nest(10262, 'p26-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10261, 'p26-post', 10262, 'p26-reply',
                right=num(8, 11),                            # noqa: F405
                on_right=next_note('') + [load('p27')],
                notes=['8/11 — the scale knew. Next: two in order.'])),
    scenery=SCENERY)

# --- p27: a pair in order ---------------------------------------------------------
puzzle(
    'p27',
    'The computer wants these two numbers in a box, the smaller one first. '
    'Which is smaller is for the scale to say.',
    'a box with the smaller number first',
    ['Put both numbers on the scale and see which way it tips.',
     'The lighter pan holds the smaller number; that one goes in the first '
     'hole.',
     'Here’s what I’d do: put the 47 and the 43 on the scale — it tips toward '
     'the 47, so the 43 is smaller. Put the 43 in the first hole and the 47 '
     'in the second, and give the bird the box.'],
    rules(),
    table([num(47), num(43), scale(None, None), empty_box(2)],   # noqa: F405
          fixed(box(num(43), num(47)), 'we need this'),     # noqa: F405
          bird(10271, 'p27-post', 'give me your answer'),    # noqa: F405
          nest(10272, 'p27-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10271, 'p27-post', 10272, 'p27-reply',
                right=box(num(43), num(47)),                 # noqa: F405
                on_right=next_note('') + [load('p28')],
                notes=['43 then 47. Next: a robot that sorts.'],
                sorry='Not quite — the smaller number in the first hole.')),
    scenery=SCENERY)

# --- p28: a robot sorts the pans ------------------------------------------------------
# Sorting is swapping what is out of order, and this is the smallest piece of
# it: two stuck fractions in the pans of a scale, tipping left; the robot
# swaps them through the spare hole. One run: once swapped, the scale tips
# right and the thought no longer fits. Puzzle 33 sorts three with a team
# built round this robot.
puzzle(
    'p28',
    'Sorting is swapping what is out of order, over and over — and this is '
    'the smallest piece of it. Two fractions are stuck in a scale’s pans, '
    'the bigger one on the left, and the computer wants the smaller one on '
    'the left. They are too close to tell apart by eye, and stuck too fast '
    'for your fingers — the scale says which is bigger, and only a robot’s '
    'claw can swap them. The box has a spare hole. A team of these will '
    'sort three, soon.',
    'a box holding a scale with the smaller fraction in its left pan',
    ['A pan holds one thing, like a hole. To swap two things you need '
     'somewhere to put one of them first.',
     'Move the left one to the spare hole; move the right one to the left '
     'pan; move the spare one to the right pan.',
     'Here’s what I’d do. Drop the box on the robot. In its imagination: '
     'click the 7/9, click the spare hole; click the 5/7, click the left '
     'pan; click the 7/9 in the spare hole, click the right pan. Leave the '
     'thought bubble and give the bird the box.'],
    rules(),
    table([box(scale(stuck(num(7, 9)), stuck(num(5, 7))), None), ROBOT],   # noqa: F405
          fixed(box(scale(stuck(num(5, 7)), stuck(num(7, 9))), None), 'we need this'),   # noqa: F405
          bird(10281, 'p28-post', 'give me your answer'),    # noqa: F405
          nest(10282, 'p28-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10281, 'p28-post', 10282, 'p28-reply',
                right=box(scale(stuck(num(5, 7)), stuck(num(7, 9))), None),   # noqa: F405
                on_right=next_note('') + [load('p29')],
                notes=['5/7 on the left, 7/9 on the right — sorted by robot. '
                       'Next: letters into a word.'],
                sorry='Not quite — the smaller fraction in the LEFT pan, and '
                      'the spare hole empty.')),
    scenery=SCENERY)

# --- p29: letters into a word -------------------------------------------------------
puzzle(
    'p29',
    'The computer has the letters of a word, one to a hole, and it wants the '
    'word on one pad. There is a blank pad here.',
    'one pad that says Toon',
    ['A box of letters poured onto a blank pad becomes the word.',
     'Pick up the box and drop it on the blank pad.',
     'Here’s what I’d do: drop the box of letters on the blank pad, and give '
     'the bird the pad that says Toon.'],
    rules(),
    table([box(pad('T'), pad('o'), pad('o'), pad('n')), pad('')],   # noqa: F405
          fixed(pad('Toon'), 'we need this'),                # noqa: F405
          bird(10291, 'p29-post', 'give me your answer'),    # noqa: F405
          nest(10292, 'p29-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10291, 'p29-post', 10292, 'p29-reply',
                right=txt('Toon'),                           # noqa: F405
                on_right=next_note('') + [load('p30')],
                notes=['Toon, on one pad. Next: the other way round.'])),
    scenery=SCENERY)

# --- p30: a word into letters ---------------------------------------------------------
puzzle(
    'p30',
    'Now the computer wants a word taken apart: one letter to a hole. Here '
    'is the word, and a box with no holes at all.',
    'a box with T, a, l, k in its holes',
    ['A box with no holes is a mould: pour something into it and it comes '
     'apart, one part to a hole.',
     'Drop the pad on the box with no holes.',
     'Here’s what I’d do: drop the Talk pad on the empty box, and give the '
     'bird the box of four letters.'],
    rules(),
    table([pad('Talk'), box()],                              # noqa: F405
          fixed(box(pad('T'), pad('a'), pad('l'), pad('k')), 'we need this'),   # noqa: F405
          bird(10301, 'p30-post', 'give me your answer'),    # noqa: F405
          nest(10302, 'p30-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10301, 'p30-post', 10302, 'p30-reply',
                right=box(txt('T'), txt('a'), txt('l'), txt('k')),   # noqa: F405
                on_right=next_note('') + [load('p31')],
                notes=['T, a, l, k — four holes. Next: one letter out of '
                       'a word.'])),
    scenery=SCENERY)

# --- p31: the third letter -----------------------------------------------------------
puzzle(
    'p31',
    'The computer wants one letter out of a word: the third letter of '
    '“Marty”. A number can pick a letter out of a pad.',
    'a pad that says r',
    ['Drop a pad on a whole number and the number picks out that letter: 1 '
     'for the first, 2 for the second…',
     'The third letter wants a 3. Drop the Marty pad on the 3.',
     'Here’s what I’d do: pick up the Marty pad, drop it on the 3 — the 3 '
     'becomes an r — and give the bird the r.'],
    rules(),
    table([pad('Marty'), num(3)],                            # noqa: F405
          fixed(pad('r'), 'we need this'),                   # noqa: F405
          bird(10311, 'p31-post', 'give me your answer'),    # noqa: F405
          nest(10312, 'p31-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10311, 'p31-post', 10312, 'p31-reply',
                right=txt('r'),                              # noqa: F405
                on_right=next_note('') + [load('p32')],
                notes=['r — the third letter. Next: halving down to one.'],
                sorry='Not quite — the third letter of Marty, on its own '
                      'pad.')),
    scenery=SCENERY)

# --- p32: down to one --------------------------------------------------------------------
# The 64 and the 1 are stuck (Ken: "too easy to cheat and grab the 1 from the
# scale"), and a stuck thing can only be moved by a claw INSIDE what the robot
# was given -- so the robot cannot pull the 1 out for you either. The answer
# is the whole box, its scale balanced.
puzzle(
    'p32',
    'The computer wants this box with its 64 halved down to 1, so that the '
    'scale balances: 1 against 1. The 64 and the 1 are stuck fast, so only a '
    'robot can work on them — and the 2 wearing a divide badge, in the third '
    'hole, halves whatever it lands on. A robot that halves the number every '
    'round will get there, and the scale can tell it when to stop.',
    'the box, its scale balanced at 1 against 1 and the ÷2 back in its hole',
    ['The scale tips left while the number is bigger than 1. A thought that '
     'says “tipping left” fits only then.',
     'A badge number is used up when it lands, so the robot needs a copy of '
     'the ÷2 every round: set it on Mimi, take the copy, drop the copy on the '
     'number in the pan, take the badge back off the platform, put it in its '
     'hole.',
     'Wake Ruby and loosen the number in the left pan to “any number”. The '
     'tilt stays; the robot halves until the pans balance.',
     'Here’s what I’d do. Drop the box on the robot; click the ÷2, click '
     'Mimi, click the copy, click the 64; click the ÷2 on the platform, click '
     'its hole. Leave the thought bubble; wake Ruby and loosen the 64. Press '
     'Run — it still has the box — and wait: it stops at 1. Take the box '
     'and give it to the bird.'],
    rules(tools=['mimi', 'ruby']),
    table([box(scale(stuck(num(64)), stuck(num(1))), num(2, op='/')), ROBOT],   # noqa: F405
          fixed(box(scale(stuck(num(1)), stuck(num(1))), num(2, op='/')), 'we need this'),   # noqa: F405
          bird(10321, 'p32-post', 'give me your answer'),    # noqa: F405
          nest(10322, 'p32-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10321, 'p32-post', 10322, 'p32-reply',
                right=box(scale(stuck(num(1)), stuck(num(1))), num(2, op='/')),   # noqa: F405
                on_right=next_note('') + [load('p33')],
                notes=['Down to one, and it knew where to stop. Next: a '
                       'team of robots sorts three.'],
                sorry='Not quite — the whole box, its scale balanced at 1 '
                      'against 1, and the ÷2 back in its hole.')),
    scenery=SCENERY)

# --- p33: sort three ---------------------------------------------------------------------
# The sorting challenge Ken expected after 28. Four robots make a team: the
# swapper from 28 (scale tipping LEFT: swap the pans through hole 5, the spare
# that stays empty in every phase -- hole 4 is where the biggest number parks), and
# three movers, each keyed on which hole is full and a scale tipping RIGHT:
#   hole 2 full: left pan -> hole 3, hole 2 -> left pan
#   hole 3 full: right pan -> hole 4, hole 3 -> right pan
#   hole 4 full: left pan -> hole 2, right pan -> hole 3
# Three compare-and-swaps, and the team stops by itself when the scale is
# empty. Trained on a practice box; judged on a box of other, stuck fractions.
PRACTICE = box(scale(num(2, 3), num(3, 5)), num(5, 8), None, None, None)     # noqa: F405
TO_SORT = box(scale(stuck(num(11, 15)), stuck(num(7, 9))), stuck(num(4, 5)), None, None, None)   # noqa: F405
SORTED = box(scale(None, None), stuck(num(11, 15)), stuck(num(7, 9)), stuck(num(4, 5)), None)   # noqa: F405
puzzle(
    'p33',
    'The sorting challenge. The computer wants the box on the middle row '
    'sorted: its three fractions in holes 2, 3 and 4, smallest first, the '
    'scale empty, and the fifth hole — the swapper’s spare — empty too. They '
    'are stuck fast, and too close to tell apart by '
    'eye. A team of four robots can do it — the swapper from puzzle 28 and '
    'three that each move a number — trained on the practice box at the '
    'front, which holds other fractions.',
    'the box with its three fractions in order after the empty scale, '
    'smallest first',
    ['Sorting three is three compare-and-swaps. The scale compares; the '
     'swapper swaps when it tips left. Three more robots move numbers in and '
     'out of the pans, and each knows its turn by which hole is full: 2, 3 '
     'or 4. Hole 5 is the swapper’s spare, and stays empty.',
     'The swapper first, on the practice box (its scale tips left): left pan '
     'to hole 5, right pan to the left pan, hole 5 to the right pan. Leave. '
     'Wake Ruby and loosen both pans to “any number”; wake Dusty and take '
     'hole 2 out of its thought, so anything or nothing may be there.',
     'Run the swapper on the practice box: the smaller fraction is now on '
     'the left. Train the second robot on that: left pan to hole 3, then '
     'hole 2 to the left pan. Ruby: loosen both pans and hole 2 to any '
     'number. Its thought says tipping RIGHT — keep that.',
     'Run the second robot once. Train the third on what you see: right pan '
     'to hole 4, then hole 3 to the right pan. Ruby: both pans and hole 3.',
     'Run the third once, then the swapper once more, since the scale tips '
     'left again. Train the fourth: left pan to hole 2, right pan to hole 3. '
     'Ruby: both pans and hole 4.',
     'Drop the robots on one another to make a team. Give the team the '
     'middle box and press Run: it swaps and moves until the scale is empty '
     'and the three are in order. Give the bird the box.'],
    rules(tools=['ruby', 'dusty']),
    table([PRACTICE, ROBOT, ROBOT, ROBOT, ROBOT],
          fixed(SORTED, 'we need this'),
          bird(10331, 'p33-post', 'give me your answer'),    # noqa: F405
          nest(10332, 'p33-reply', 'from the judge'),        # noqa: F405
          judge('the judge', 10331, 'p33-post', 10332, 'p33-reply',
                right=SORTED,
                on_right=next_note(''),
                notes=['11/15, 7/9, 4/5 — sorted by a team of four. Thank '
                       'you! (More puzzles are on the way.)'],
                sorry='Not quite — the three fractions in holes 2, 3 and 4, '
                      'smallest first, both pans empty, and hole 5 empty.'),
          extra=[{'thing': TO_SORT, 'x': 0.75, 'z': MID}]),
    scenery=SCENERY)
