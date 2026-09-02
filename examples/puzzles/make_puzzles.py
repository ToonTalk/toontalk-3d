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


def table(materials, goal, post, reply, judge_, extra=()):
    """materials: things left to right across the front; the rest fixed."""
    n = len(materials)
    xs = [(-0.45 * (n - 1) / 2) + 0.45 * i for i in range(n)] if n > 1 else [0.0]
    bench = [{'thing': m, 'x': round(x, 2), 'z': FRONT} for m, x in zip(materials, xs)]
    bench += [{'thing': post, 'x': 0.0, 'z': MID},
              {'thing': reply, 'x': 0.55, 'z': MID},
              {'thing': goal, 'x': 1.15, 'z': BACK},
              {'thing': judge_, 'x': -1.25, 'z': BACK}]
    bench += list(extra)
    return bench


def next_note(text):
    return [take('given', 2), put('given', 1)]              # noqa: F405


ROBOT = {'kind': 'robot', 'name': None, 'program': [], 'team': []}

# Where it came down: on the floor beyond the far side of the table, nose
# toward the room, seven times hand size -- a ship Marty could sit in.
SCENERY = [{'thing': ship(), 'x': 2.3, 'y': 0.0, 'z': -1.6, 'ry': 35, 'sz': 7}]

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
    'three of them, on that nest. Train a robot to add them up: give it the '
    'box, take the top number off the nest and drop it on the zero. Its '
    'thought will want exactly that number, so wake Ruby and click the parts '
    'of its thought to loosen them; then give it the box again and it will '
    'work until the nest is empty. Give the bird the total.',
    'the total of the numbers on the nest',
    ['Give the robot the box with the nest in it. In its imagination, click '
     'the top number on the nest — the robot takes it — then click the zero '
     'to drop it there.',
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
    'Now the computer needs a box with six zeros. You have a box with two; '
    'boxes join when you drop one on the side of another, and Mimi copies '
    'boxes as happily as numbers.',
    'a box with six zeros in it',
    ['Set the box on Mimi’s platform and a copy of the whole box drops into '
     'her tray. Take the copy, and then the box itself comes back off the '
     'platform.',
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
    'The computer needs a million. You have a 10, and a 10 wearing a times '
    'badge — dropped on a number, it multiplies. But a badge number is used '
    'up when it lands, so Mimi is here to make more.',
    'a million',
    ['Times ten on 10 is 100 — and the times-ten is gone. Copy it with Mimi '
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
    'The computer needs more than numbers — it needs letters and words. Here '
    'are three blank pads: pick one up and type a capital A on it; then B and '
    'C. Put them in the box in order and give the box to the bird.',
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
                on_right=next_note(''),
                notes=['A, B, C — the computer can spell. Thank you! (More '
                       'puzzles are on the way.)'],
                sorry='Not quite — capital A, B and C, one to a pad, in that '
                      'order.')),
    scenery=SCENERY)
