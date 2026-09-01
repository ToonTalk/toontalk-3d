# pong-classic -- Pong the way the original played it.
#
# Ken sent the original: My Programs/pong.tt, saved out of ToonTalk 3. Opening
# it up, the differences from our first Pong are three, and all three are about
# the same idea -- that a game is made of things, not of robots doing things:
#
#   1. It is played on a FIELD.  The whole game is one green rectangle, and the
#      ball, the bat and the score ride on it as pictures riding on a picture.
#      Not on the table, which is the workshop's floor.
#
#   2. The ball has a SPEED.  SpeedToRight=500, SpeedToTop=-600 are properties
#      of the picture in the original file. The ball moves on the world's own
#      clock, smoothly, whether or not any robot is doing anything -- and the
#      robots' whole job is to change the speed when it hits something.
#
#   3. Collision says WHICH SIDE.  The original's ball carries two robots, both
#      called Bounce, whose thoughts differ only in reading "Right Collide?"
#      versus "Up Collide?". Ours differ only in the word they expect in the
#      touching reading's second hole.
#
# So the ball's whole program is: whatever you have run into, and whichever
# side of you it is on, send yourself the message that turns you away from it.
# Four messages, four robots, and none of them has heard of Pong.
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'images'))
from _beh import *                                          # noqa: F403
from _img import draw_rgba, hue                             # noqa: F401

BALL, BAT, SCORE, FIELD = 'Q901', 'Q902', 'Q903', 'Q904'
EDGE_N, TOUCH_N, POINT_N = 9201, 9202, 9203

# --- the field, and where it sits -------------------------------------------
# 6 tablets across and 3.2 deep, which is 2.04 by 1.088 of the workshop's own
# steps -- close to the shape of the original's board, and a great deal better
# to play on than the letterbox it was. It stands LEFT of centre, because the
# notebook is furniture at x 0.52 to 1.38 and this way the pitch never touches
# it; that leaves the right-hand strip of the table for the pads that explain
# the game.
#
# Its middle is 7/4 from the front of the table, and that 7/4 is the only thing
# in this world that knows where the pitch stands -- the bat's robot is the
# only thing that uses it.
FIELD_X, FIELD_Z = -0.62, 1.75
# Named, because the PITCH is what you point at to start the game: SPACE on a
# pad switches on everything riding it, and "." stops the lot.
field = dict(live(pad('', bg='#0b4d18', ink='#cfe8d2', font='sans', w=6.0, h=3.2),
                  FIELD), label='the pitch')

# --- the ball and the bat, painted ------------------------------------------
# The original's are a rainbow ball and a rainbow bat, so these are too: the
# same sixth-of-the-wheel-per-unit sweep, diagonal on the ball and top-to-
# bottom on the bat. Drawn with alpha, so the ball is ROUND on the field
# rather than a square of green with a circle in it.
ball_png = draw_rgba(lambda u, v: u * u + v * v <= 0.94 ** 2,
                     lambda u, v: hue((u + v) * 0.55 + 0.5))


# A picture is drawn to FIT its pad, so the bat is painted at the pad's own
# proportions -- a square bat on a pad twice as deep as it is wide comes out
# squat, with empty field above and below it.
BAT_TALL = 2.0 / 0.9


def rounded(u, v, r=0.30):
    """A bat: a tall rounded rectangle, about a twelfth of the field wide."""
    au, av = abs(u), abs(v)
    if au > 0.92 or av > 0.98:
        return False
    cu, cv = 0.92 - r, 0.98 - r / BAT_TALL
    if au <= cu or av <= cv:
        return True
    du, dv = (au - cu) / r, (av - cv) / (r / BAT_TALL)
    return du * du + dv * dv <= 1.0


bat_png = draw_rgba(rounded, lambda u, v: hue(v * 0.5 + 0.5), n=48, tall=BAT_TALL)

# Said outright, both of them. A pad with nothing said about its shape is a
# TABLET -- wider than it is deep -- and a ball has to be told it is round or
# it bounces off the far wall a finger early on one axis and not the other.
ball = dict(live(pad('', w=0.6, h=0.6), BALL), img=ball_png)  # noqa: F405
bat = dict(live(pad('', w=0.9, h=2.0), BAT), img=bat_png)    # noqa: F405


def edge_nest(lid, nid, reading='none'):
    return {'kind': 'nest', 'id': nid, 'guid': 'evt-' + lid + '#edge',
            'hasEgg': False, 'label': 'edge', 'pile': [txt(reading)]}   # noqa: F405


def touch_nest(lid, nid, what=None, side='none'):
    """The reading is a box of two: what I ran into, and which side of me."""
    return {'kind': 'nest', 'id': nid, 'guid': 'evt-' + lid + '#touch',
            'hasEgg': False, 'label': 'touching',
            'pile': [box(what or txt('nothing'), txt(side))]}   # noqa: F405


# --- the four messages that turn a ball ------------------------------------
# An EMPTY hole leaves that one alone, which is the whole trick: "go left" says
# nothing about up and down, so a ball that bounces off the bat keeps climbing
# or falling exactly as it was. No arithmetic, nothing to flip, and sending the
# same one twice does no harm -- which matters, because a contact lasts several
# rounds and the robot will act on every one of them.
ACROSS, AWAY = (3, 7), (2, 9)


def go(dx=None, dz=None):
    return msg('set', 'speed',                                # noqa: F405
               box(num(*dx) if dx else None,                  # noqa: F405
                   num(*dz) if dz else None))                 # noqa: F405


go_right = go(dx=(ACROSS[0], ACROSS[1]))
go_left = go(dx=(-ACROSS[0], ACROSS[1]))
go_near = go(dz=(AWAY[0], AWAY[1]))
go_far = go(dz=(-AWAY[0], AWAY[1]))
serve = msg('set', 'position', box(num(0), num(0)))          # noqa: F405

#  0 my thing   1 go right   2 go left   3 come near   4 go far
#  5 the edge   6 what I have run into   7 back to the middle
#  8 the counter's bird       9 one more
ball_work = box(to(BALL, 'my thing'), go_right, go_left, go_near, go_far,  # noqa: F405
                edge_nest(BALL, EDGE_N), touch_nest(BALL, TOUCH_N),
                serve, to(SCORE, 'the counter'), num(1))     # noqa: F405

send = lambda i: [copy('given', i), put('given', 0)]         # noqa: E731,F405


def ball_bot(name, edge, side, program):
    trained = box(to(BALL), go_right, go_left, go_near, go_far,   # noqa: F405
                  edge_nest(BALL, EDGE_N, edge or 'none'),
                  touch_nest(BALL, TOUCH_N,
                             to(BALL) if side else None, side or 'none'),
                  serve, to(SCORE), num(1))                  # noqa: F405
    cond = box(ANYBIRD, ANYBOX, ANYBOX, ANYBOX, ANYBOX,      # noqa: F405
               txt(edge) if edge else WILDTEXT,              # noqa: F405
               box(ANYBIRD if side else WILD,                # noqa: F405
                   txt(side) if side else WILDTEXT),         # noqa: F405
               ANYBOX, ANYBIRD, ANYNUM)                      # noqa: F405
    return robot(name, cond, program, trained_on=trained)    # noqa: F405


# In order. Running into something beats reaching a wall, because the bat
# stands just inside the wall it is guarding.
ball_team = ball_bot('hit on my left', None, 'left', send(1))
ball_team['team'] = [
    ball_bot('hit on my right', None, 'right', send(2)),
    ball_bot('hit on my far side', None, 'far', send(3)),
    ball_bot('hit on my near side', None, 'near', send(4)),
    ball_bot('the right wall', 'right', None, send(2)),
    ball_bot('the far wall', 'far', None, send(3)),
    ball_bot('the near wall', 'near', None, send(4)),
    # the left wall is the one you are guarding: getting there is a miss
    ball_bot('past the bat', 'left', None,
             [copy('given', 9), put('given', 8)]             # noqa: F405
             + [copy('given', 7), put('given', 0)]
             + send(1)),
    # and one that does nothing, because most rounds there is nothing to do
    ball_bot('flying', None, None, []),
]

# --- the bat ----------------------------------------------------------------
#  0 my thing   1 the pointer   2 [set | away | _]
# The pointer says where your hand is on the TABLE; the bat lives on the pitch,
# whose middle is 7/4 further back. So the robot takes the away out of the
# reading, drops a -7/4 on it, and posts the difference. That is not a
# workaround: a place is always measured from the middle of whatever you are
# standing on, and this robot is doing the only sum that follows from it.
bat_msg = box(txt('set'), txt('away'), None)                 # noqa: F405
bat_work = box(to(BAT, 'my thing'),                          # noqa: F405
               device(POINT_N, DEV_POINT, 'pointer'), bat_msg)
bat_bot = robot(                                             # noqa: F405
    'Bat', box(ANYBIRD, ANYBOX, ANYBOX),                     # noqa: F405
    [
        copy('given', 2), put('s0'),        # a [set | away | _] to fill in
        takeTop('given', 1), put('s1'),     # where the pointer is on the table
        newnum, setv(-7, '+', 4), put('s1', 1),   # ...measured from the pitch
        take('s1', 1), put('s0', 2),
        vac('s1'),                          # and the husk to Dusty
        take('s0'), put('given', 0),
    ],
    trained_on=box(to(BAT),                                  # noqa: F405
                   device(POINT_N, DEV_POINT, 'pointer'), bat_msg))


def gadget(thing, bot, work):
    return dict(thing, gadget=True,
                panel={'kind': 'world', 'v': 3, 'bench': [],
                       'stations': {'stand': work}, 'active': bot})


# --- the world --------------------------------------------------------------
# The ball and the bat RIDE on the field: a thing riding on a pad has a place
# of its own, measured from that pad's middle, and its walls are that pad's
# edges. Which is why nothing on the table is in the way of this one.
# The score rides on the board, top right, the way the original's does -- and
# it is SCENERY: [set | solid | no] once, and the ball goes straight through it
# instead of bouncing off the counter that is keeping its score.
score = dict(live(num(0), SCORE), label='misses', ghost=True)   # noqa: F405

field_with_players = dict(field, subs=[
    {'at': {'u': 0.0, 'v': 0.0},
     'thing': dict(gadget(ball, ball_team, ball_work),
                   speed={'x': 0.42, 'z': 0.26})},
    {'at': {'u': -0.42, 'v': 0.0},
     'thing': gadget(bat, bat_bot, bat_work)},
    {'at': {'u': 0.36, 'v': -0.34}, 'thing': score},
])


ABOUT = ('PONG, THE ORIGINAL WAY\n\n'
         'The game is the green\n'
         'FIELD, and the ball and the\n'
         'bat ride on it -- a picture\n'
         'on a picture. The table is\n'
         'only the floor it stands on.\n\n'
         'A thing riding on a pad has\n'
         'a place of its own, measured\n'
         'from that pad\'s middle, and\n'
         'its walls are that pad\'s\n'
         'edges.')

RUN = ('TO PLAY\n\n'
       'Set Speed to Instant.\n\n'
       'Point at the green PITCH and\n'
       'press ENTER: the whole board\n'
       'fills the screen, straight\n'
       'on, and the workshop gets\n'
       'out of the way. Escape\n'
       'comes back.\n\n'
       'Then press SPACE: everything\n'
       'on the pitch starts together.\n'
       '"." on the pitch stops the\n'
       'lot.\n\n'
       'They keep going until you\n'
       'stop them -- a behaviour is\n'
       'switched on and off, not\n'
       'counted in rounds. The Pause\n'
       'button in the bar holds the\n'
       'whole world still.\n\n'
       'Move your pointer up and\n'
       'down: the bat follows. Keep\n'
       'the ball off the LEFT wall.\n\n'
       'Nothing needs clearing away\n'
       'first. The ball is on the\n'
       'FIELD, and only what is on\n'
       'the field is in its way --\n'
       'not these pads, not your\n'
       'notebook.\n\n'
       'To take the ball or the bat\n'
       'off the pitch, wake DUSTY\n'
       'and click it. Clicking Dusty\n'
       'gives it back, and dropping\n'
       'it on the green puts it\n'
       'where you drop it.')

WHY = ('THE BALL MOVES ITSELF\n\n'
       'It carries a SPEED, the way\n'
       'the original\'s did:\n\n'
       '  [set | speed | [3/5 | 1/4]]\n\n'
       'and then it travels on the\n'
       'world\'s clock, smoothly,\n'
       'whether or not any robot is\n'
       'doing anything.\n\n'
       'So its robots are not\n'
       'responsible for moving it.\n'
       'They are left with the only\n'
       'interesting question: what\n'
       'to do when it hits something.')

HOW = ('FOUR MESSAGES, EIGHT ROBOTS\n\n'
       'An EMPTY hole leaves that\n'
       'one alone, so\n\n'
       '  [set | speed | [-3/5 | ]]\n\n'
       'means "go left" and says\n'
       'nothing about up and down.\n'
       'That is a bounce, in one\n'
       'message, with no arithmetic\n'
       'and nothing to flip.\n\n'
       'The robots differ only in\n'
       'the word they expect -- from\n'
       'the edge reading, or from\n'
       'the second hole of what it\n'
       'has run into, which says\n'
       'WHICH SIDE of the ball the\n'
       'thing is on.\n\n'
       'The original had exactly the\n'
       'same pair: "Right Collide?"\n'
       'and "Up Collide?", one\n'
       'Bounce robot each.')

bench = [
    {'thing': field_with_players, 'x': FIELD_X, 'z': FIELD_Z},

    {'thing': txt(ABOUT), 'x': 0.75, 'z': 2.15},            # noqa: F405
    {'thing': txt(RUN), 'x': 1.25, 'z': 2.15},              # noqa: F405
    {'thing': txt(WHY), 'x': 0.75, 'z': 1.75},              # noqa: F405
    {'thing': txt(HOW), 'x': 1.25, 'z': 1.75},              # noqa: F405
]

write_beh('pong-classic', bench)
