# Pong rebuilt from the SHELF -- the capstone clause, honoured late.
#
# The plan said Pong should be "built only from pads, sub-pads and library
# behaviours -- no bespoke robots", and the first Pong diverged because four
# of the needed gadgets did not exist. All twelve exist now, so this world is
# the honest follow-up: a ball that is nothing but a pad with THREE SHELF
# GADGETS bound to it, a bat that is a pad with ONE, and not a single robot
# written for the occasion.
#
#   the ball = bouncing at a speed        (walls -- all four)
#            + reverse a speed on collision (the bat)
#            + send 1 to the score          (a rally counter)
#   the bat  = following up and down
#
# The gadgets here are the shelf's own, rebound at authoring time exactly as
# dropping them on the ball would rebind them: every reference to the
# gadget's own name is renamed to the ball's, channels included, and boundTo
# says so. Open any panel and compare it with the shelf's -- the robots are
# the same robots.
#
# WHAT THE COMPOSITION TEACHES (and its honest seams): each mover-gadget
# carries its own steps, so two bound movers ADD -- the ball's velocity is
# bouncing's step plus reverse's step, and after a wall bounce the two can
# briefly disagree. And the score counts HITS on the bat (touch is what the
# shelf gadget hears), where classic Pong counts misses. Both are recorded in
# BACKS.md: step-movers compose by addition; a miss-counter wants the edge
# reading, which is a shelf gadget nobody has asked for yet.
import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beh import *                                          # noqa: F403

import make_library2                                        # noqa: F401  (builds the six)
from make_library import gliding, following_v, SIX          # noqa: E402


def scenery(thing):
    """Not solid: the ball passes through it and never counts it as a hit.

    Solid is the right default -- it is what makes a ball bounce off a bat --
    but a title, a rally counter and four cards of documentation are things
    to READ. Left solid they are things to hit, and the ball scored against
    the instructions."""
    return dict(thing, ghost=True)

BALL, BAT, SCORE = 'V901', 'V902', 'V905'


def rebound(gadget_spec, own_lid, target_lid, fresh_lid):
    """The gadget, rebound to a target -- the same rename a drop performs:
    every reference to its own name becomes the target's, channels included,
    and the gadget itself takes a fresh name so three of them can coexist."""
    j = json.dumps(gadget_spec)
    j = j.replace(own_lid, target_lid)          # lid and evt-lid(#chan) alike
    g = json.loads(j)
    g['lid'] = fresh_lid
    g['evt'] = 'evt-' + fresh_lid
    g['boundTo'] = target_lid
    return g


ball = dict(live(pad('', bg='#ffd23f', ink='#1b2233', font='sans',   # noqa: F405
                     w=0.5, h=0.5), BALL), label='the ball')
bat = dict(live(pad('', bg='#7ee787', ink='#1b2233', font='sans',    # noqa: F405
                    w=0.25, h=1.3), BAT), label='the bat')
score = dict(live(num(0), SCORE), label='rally')                     # noqa: F405

# THE BALL MOVES ON THE WORLD'S CLOCK, not on anybody's turn. The
# step-based pair (bouncing + reverse on collision) each ran a mover robot
# every round -- a cycle builds a message box and flies a bird, about 10ms --
# so three gadgets on one ball came to 26ms a frame and the ball moved as
# unevenly as the frames arrived. Their speed-based siblings set a speed and
# then SLEEP until a wall or a contact: 0.1ms a frame, and a step that is the
# same size every frame.
b_bounce = rebound(gliding, 'G916', BALL, 'V911')
b_reverse = rebound(SIX['reversing_speed'], 'G917', BALL, 'V912')
# Re-aim ONLY THE BIRD at our score; the tally riding in the work box keeps a
# private name of its own. The first attempt renamed the whole of 'G912S' to
# the score's id -- whereupon TWO things claimed that name and the inner one,
# registered last, quietly took all the mail: the copies-clash bug,
# re-created by hand in authoring. And the suffixed id is renamed before the
# bare one, or 'G912' eats its prefix.
b_score = json.dumps(SIX['scoring'])
b_score = b_score.replace('"liveId": "G912S"', '"liveId": "' + SCORE + '"')
b_score = json.loads(b_score.replace('G912S', 'V913S'))
b_score = rebound(b_score, 'G912', BALL, 'V913')
# The bat takes the THIRTEENTH shelf gadget, not the fifth: following up and
# down sends the pointer's AWAY only, so the bat keeps its own place across
# the table (a bat that wanders sideways is not a wall) and can still be
# pointed at when you want to stop it.
bt_follow = rebound(following_v, 'G915', BAT, 'V914')

ABOUT = ('PONG, FROM THE SHELF\n\n'
         'No robot here was written\n'
         'for Pong. The ball is a pad\n'
         'with three shelf gadgets\n'
         'bound to it:\n\n'
         '  bouncing at a speed\n'
         '    (the walls)\n'
         '  reverse a speed on\n'
         '    collision (the bat)\n'
         '  send 1 to the score\n\n'
         'The bat is a pad with\n'
         '"following up and down".')

RUN = ('TO PLAY\n\n'
       'Press SPACE on THE BALL --\n'
       'everything bound to it\n'
       'starts as one. SPACE on the\n'
       'bat starts its follower.\n'
       '"." stops either.\n\n'
       'The bat tracks your pointer\n'
       'UP AND DOWN only, so it\n'
       'stays a wall -- and so you\n'
       'can point at it to stop it.\n\n'
       'The rally counter climbs\n'
       'each time the ball meets\n'
       'the bat. Everything else\n'
       'here is scenery: the ball\n'
       'passes through the cards.')

SEAMS = ('THE HONEST SEAMS\n\n'
         'The ball moves on the\n'
         'CLOCK, not on a robot\n'
         'turn: its gadgets set a\n'
         'speed and then sleep until\n'
         'a wall or a contact. The\n'
         'step-based pair is still\n'
         'on the shelf -- bind those\n'
         'instead and watch it\n'
         'stutter, and add up.\n\n'
         'Everything but the ball and\n'
         'the bat is SCENERY --\n'
         '[set | solid | no] -- or\n'
         'the ball collides with the\n'
         'documentation and scores\n'
         'against it.\n\n'
         'And the counter scores\n'
         'HITS (touch is what the\n'
         'shelf gadget hears), where\n'
         'classic Pong scores\n'
         'misses. A miss-counter\n'
         'would listen to the edge\n'
         'reading -- a shelf gadget\n'
         'nobody has asked for yet.')

ASK = ('ASK MARTY\n\n'
       'Open Marty and ask:\n\n'
       '  "what does the ball do?"\n'
       '  "what happens when the\n'
       '   ball meets the bat?"\n\n'
       'He reads the panels of the\n'
       'bound gadgets and answers\n'
       'with the PURPOSE of the\n'
       'whole loop -- the steps only\n'
       'if you ask how.')

bench = [
    # the bat stands in the clear front-right, away from the desk notebook's
    # home; the score in the clear front-left; the ball has the middle
    {'thing': ball, 'x': 0.10, 'z': 1.50},
    {'thing': bat, 'x': 1.42, 'z': 1.95},
    {'thing': scenery(score), 'x': -0.90, 'z': 1.95},

    {'thing': scenery(b_bounce), 'x': -1.50, 'z': 1.15},
    {'thing': scenery(b_reverse), 'x': -1.50, 'z': 1.50},
    {'thing': scenery(b_score), 'x': -1.50, 'z': 1.85},
    {'thing': scenery(bt_follow), 'x': -1.05, 'z': 1.15},

    {'thing': scenery(txt(ABOUT)), 'x': -0.55, 'z': 2.30},  # noqa: F405
    {'thing': scenery(txt(RUN)), 'x': 0.15, 'z': 2.30},     # noqa: F405
    {'thing': scenery(txt(SEAMS)), 'x': 0.85, 'z': 2.30},   # noqa: F405
    {'thing': scenery(txt(ASK)), 'x': 1.50, 'z': 2.30},     # noqa: F405
]

write_beh('pong-gadgets', bench)
