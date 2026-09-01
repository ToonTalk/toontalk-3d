# pong -- the capstone, and nothing in it is new.
#
# The table IS the court. Three of its walls are the table's own edges; the
# fourth, on the right, is yours to guard. The ball, the bat and the counter
# are three ordinary things standing on the table, and two of them carry their
# own program on their own panel: the ball knows how to be a ball, the bat
# knows how to be a bat. Nothing anywhere knows the game is Pong.
#
# Every part was built for something else:
#
#   [move | across | n]   Stage 5, so a behaviour could move its thing
#   the EDGE reading      Stage 5, so bouncing could be written at all
#   the TOUCH reading     the same shape again: what am I against?
#   the POINTER device    Stage 4, the workshop's own senses
#   a badged number
#     given to a bird     Stage 2, how a live number is changed
#   [set | width | n]     Stage 3's appearance API -- which is the whole of
#                         why the bat is a bat and the ball is a ball
#
# Two panels run at once, which is what makes it a game rather than a demo:
# the ball's team and the bat's follower are separate programs on separate
# benches, sharing only the table they move things on.
from _beh import *                                          # noqa: F403

BALL, BAT, SCORE = 'P901', 'P902', 'P903'
EDGE_N, TOUCH_N, POINT_N = 9101, 9102, 9103

# --- the three things -------------------------------------------------------
# w and h are the appearance API, in tablets: the ball is half a tablet square,
# the bat a quarter wide and a tablet and a third deep. That is the only
# difference between them and any other pad.
ball = live(pad('', bg='#ffd23f', ink='#1b2233', font='sans', w=0.5, h=0.5),
            BALL)
bat = live(pad('', bg='#7ee787', ink='#1b2233', font='sans', w=0.25, h=1.3),
           BAT)
score = dict(live(num(0), SCORE), label='misses')            # noqa: F405


def edge_nest(lid, nid, reading='none'):
    return {'kind': 'nest', 'id': nid, 'guid': 'evt-' + lid + '#edge',
            'hasEgg': False, 'label': 'edge', 'pile': [txt(reading)]}   # noqa: F405


def touch_nest(lid, nid, thing=None, side='none'):
    """A box of two: what I have run into, and which side of me it is on."""
    return {'kind': 'nest', 'id': nid, 'guid': 'evt-' + lid + '#touch',
            'hasEgg': False, 'label': 'touching',
            'pile': [box(thing or txt('nothing'), txt(side))]}   # noqa: F405


# --- the ball ---------------------------------------------------------------
#  0 my thing        1 across step   2 away step   3 edge   4 touching
#  5 back to the middle              6 the counter's bird   7 one more
across = msg('move', 'across', num(1, 55))                   # noqa: F405
away = msg('move', 'away', num(1, 140))                      # noqa: F405
middle = msg('set', 'position', box(num(0), num(17, 10)))    # noqa: F405
one = num(1)                                                 # noqa: F405

ball_work = box(to(BALL, 'my thing'), across, away,          # noqa: F405
                edge_nest(BALL, EDGE_N), touch_nest(BALL, TOUCH_N),
                middle, to(SCORE, 'the counter'), one)

fly = [copy('given', 1), put('given', 0),                    # noqa: F405
       copy('given', 2), put('given', 0)]                    # both steps, sent

# At a WALL, turning round is a x-1 dropped on the step, exactly as you would
# drop one by hand -- and it is safe there because the wall has clamped the
# ball exactly on the line, so one flip takes it off.
flip_across = drop(-1, '*', 'given', 1, 2)                   # noqa: F405
flip_away = drop(-1, '*', 'given', 2, 2)                     # noqa: F405


def head(hole, n, d):
    """Against something you have RUN INTO, flipping is not safe: it reverses
    whatever you were doing, which half the time is into the thing you have
    just hit. So say which way to go instead -- sweep the old step away and
    drop in a new one. Sending it twice does no harm, which matters, because a
    contact lasts several rounds."""
    return [vac('given', hole, 2), newnum,                   # noqa: F405
            setv(n, '+', d), put('given', hole, 2)]          # noqa: F405


go_right = head(1, 1, 55)
go_left = head(1, -1, 55)
go_near = head(2, 1, 140)
go_far = head(2, -1, 140)


def ball_bot(name, edge, side, program):
    """edge: a word, or None for any. side: which side of the ball the thing
    it has run into is on -- or None for "never mind what it has run into"."""
    trained = box(to(BALL), across, away,                    # noqa: F405
                  edge_nest(BALL, EDGE_N, edge or 'none'),
                  touch_nest(BALL, TOUCH_N,
                             to(BALL) if side else None, side or 'none'),
                  middle, to(SCORE), one)
    cond = box(ANYBIRD, ANYBOX, ANYBOX,                      # noqa: F405
               txt(edge) if edge else WILDTEXT,              # noqa: F405
               box(ANYBIRD if side else WILD,                # noqa: F405
                   txt(side) if side else WILDTEXT),         # noqa: F405
               ANYBOX, ANYBIRD, ANYNUM)                      # noqa: F405
    return robot(name, cond, program, trained_on=trained)    # noqa: F405


# In order, and the order is the game. The WALLS come first, because a wall
# PINS you: a ball held against the near wall and touching a pad on its left
# will turn round across for ever unless the member that gets it off the wall
# is allowed a turn. Nothing is lost by asking in this order, because the bat
# stands clear of the wall it guards -- the ball can be touching one or at the
# other, never both.
#
# None of them can doze: both nests are READINGS, so neither is ever empty and
# every member can be decided every round -- which matters, because the member
# that does the moving is last.
ball_team = ball_bot('at the far wall', 'far', None, flip_away + fly)
ball_team['team'] = [
    ball_bot('at the near wall', 'near', None, flip_away + fly),
    ball_bot('at the left wall', 'left', None, flip_across + fly),
    # the fourth wall is yours. Reaching it means you missed.
    ball_bot('past the bat', 'right', None,
             [copy('given', 7), put('given', 6)]             # noqa: F405
             + flip_across
             + [copy('given', 5), put('given', 0)]),         # noqa: F405
    ball_bot('hit on my left', None, 'left', go_right + fly),
    ball_bot('hit on my right', None, 'right', go_left + fly),
    ball_bot('hit on my far side', None, 'far', go_near + fly),
    ball_bot('hit on my near side', None, 'near', go_far + fly),
    ball_bot('flying', None, None, fly),
]

# --- the bat ----------------------------------------------------------------
#  0 my thing        1 the pointer   2 [set | away | _]
# The pointer hands over [across | away] and the bat wants only the away of
# it -- so it takes that one hole out, drops it in the message, and has Dusty
# clean up what is left. Its across never changes, which is why it stays a
# wall and does not wander off after your hand.
bat_msg = box(txt('set'), txt('away'), None)                 # noqa: F405
bat_work = box(to(BAT, 'my thing'),                          # noqa: F405
               device(POINT_N, DEV_POINT, 'pointer'), bat_msg)
bat_bot = robot(                                             # noqa: F405
    'Bat', box(ANYBIRD, ANYBOX, ANYBOX),                     # noqa: F405
    [
        copy('given', 2), put('s0'),        # a [set | away | _] to fill in
        takeTop('given', 1), put('s1'),     # what the pointer just said
        take('s1', 1), put('s0', 2),        # the AWAY of it, into the hole
        vac('s1'),                          # and the husk to Dusty
        take('s0'), put('given', 0),        # away to my thing
    ],
    trained_on=box(to(BAT),                                  # noqa: F405
                   device(POINT_N, DEV_POINT, 'pointer'), bat_msg))


def gadget(thing, bot, work):
    return dict(thing, gadget=True,
                panel={'kind': 'world', 'v': 3, 'bench': [],
                       'stations': {'stand': work}, 'active': bot})


# --- the world --------------------------------------------------------------
ABOUT = ('PONG\n\n'
         'The table is the court.\n'
         'Three of its walls are the\n'
         'table\'s own edges. The\n'
         'fourth, on the right, is\n'
         'yours.\n\n'
         'The ball and the bat each\n'
         'carry their own program on\n'
         'their own panel. Click\n'
         'either to read it.')

RUN = ('TO PLAY\n\n'
       '1. CLEAR THE COURT. The ball\n'
       '   bounces off ANYTHING on\n'
       '   the table, so vacuum\n'
       '   these four pads away\n'
       '   with Dusty -- he gives\n'
       '   them back -- and slide\n'
       '   your own notebook into a\n'
       '   corner. Leave the ball,\n'
       '   the bat and the counter.\n\n'
       '2. Set Speed to Instant.\n\n'
       '3. Point at the BAT and\n'
       '   press SPACE. Then at the\n'
       '   BALL, and press SPACE.\n\n'
       'Both keep going until you\n'
       'press "." on them.\n\n'
       'Move your pointer up and\n'
       'down the table: the bat\n'
       'follows.\n\n'
       'Every time the ball gets\n'
       'past you the counter goes\n'
       'up and the ball starts\n'
       'again in the middle.')

WHY = ('NOTHING HERE IS NEW\n\n'
       '[move | across | 1/55] moves\n'
       'the ball. The EDGE reading\n'
       'says which wall it is\n'
       'against. The TOUCH reading\n'
       'hands it a bird to whatever\n'
       'it has run into. The pointer\n'
       'device drives the bat. A +1\n'
       'given to the counter\'s bird\n'
       'counts a miss.\n\n'
       'Every one of those was built\n'
       'for something else, and none\n'
       'of them has heard of Pong.')

HOW = ('THE BALL\'S TEAM\n\n'
       'Nine robots that differ only\n'
       'in what they expect in two\n'
       'holes -- the edge, and what\n'
       'it has run into:\n\n'
       '  hit on my left or right\n'
       '     -> flip the across step\n'
       '  hit on my far or near side\n'
       '     -> flip the away step\n'
       '  far or near wall\n'
       '     -> flip the away step\n'
       '  left wall\n'
       '     -> flip the across step\n'
       '  right wall  -> count a miss,\n'
       '     flip, start again in\n'
       '     the middle\n'
       '  anything else -> just fly\n\n'
       'Flipping is a x-1 dropped on\n'
       'a number, exactly as you\n'
       'would drop one by hand.\n\n'
       'The touching reading is a box\n'
       'of two: WHAT, and which SIDE\n'
       'of the ball it is on. Without\n'
       'the side there is only one\n'
       'way to turn, and a ball that\n'
       'meets the flat of a pad turns\n'
       'round and round against it.')

bench = [
    {'thing': gadget(ball, ball_team, ball_work), 'x': 0.00, 'z': 1.70},
    {'thing': gadget(bat, bat_bot, bat_work), 'x': 1.45, 'z': 1.70},
    {'thing': score, 'x': -1.58, 'z': 1.13},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.28},           # noqa: F405
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.28},             # noqa: F405
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.28},             # noqa: F405
    {'thing': txt(HOW), 'x': 0.65, 'z': 2.28},              # noqa: F405
]

write_beh('pong', bench)
