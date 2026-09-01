# library -- the starter shelf of anima-gadgets.
#
# Each gadget is ONE pad. Its face says what it does, its panel carries the
# robots that do it, and those robots speak about "my thing" through a live
# bird addressed to the gadget itself. So a gadget set down on the table does
# its own thing -- not as a demonstration mode, but because that is what "my
# thing" means when nobody has said otherwise.
#
# To use one: drop it on your thing (its bird is re-pointed and NOTHING else
# changes), then press SPACE. "." stops it. Ruby lets it go again.
#
# Nothing here is built in. There is no move, no bounce, no follow: there are
# messages a thing already answers, and robots that send them.
from _beh import *                                          # noqa: F403

def edge_nest(lid, nid, reading='none'):
    return {'kind': 'nest', 'id': nid, 'guid': 'evt-' + lid + '#edge',
            'hasEgg': False, 'label': 'edge', 'pile': [txt(reading)]}   # noqa: F405


def keys_nest(nid):
    return device(nid, DEV_KEYS, 'keyboard')


def point_nest(nid):
    return device(nid, DEV_POINT, 'pointer')


give = [copy('given', 1), put('given', 0)]                   # noqa: F405

# ---------------------------------------------------------------- 1 & 2
def straight(name, lid, dx):
    step = msg('move', 'across', num(dx[0], dx[1]))          # noqa: F405
    work = box(to(lid, 'my thing'), step)                    # noqa: F405
    bot = robot('Mover', box(ANYBIRD, ANYBOX), give,         # noqa: F405
                trained_on=box(to(lid), step))               # noqa: F405
    return gadget(name, lid, bot, work)


moving_right = straight('moving right', 'G901', (1, 60))
moving_left = straight('moving left', 'G902', (-1, 60))

# ---------------------------------------------------------------- 3 bouncing
# Both axes since 28 Aug: rebuilding Pong from the shelf exposed that a ball
# with only an across step pinned at the near and far walls. Five robots now,
# differing only in the word they expect from the edge reading.
BOUNCE = 'G903'
b_across = msg('move', 'across', num(1, 40))                 # noqa: F405
b_away = msg('move', 'away', num(1, 64))                     # noqa: F405
b_work = box(to(BOUNCE, 'my thing'), b_across, b_away,       # noqa: F405
             edge_nest(BOUNCE, 9031))
b_trained = box(to(BOUNCE), b_across, b_away,                # noqa: F405
                edge_nest(BOUNCE, 9031))
b_cond = lambda w: box(ANYBIRD, ANYBOX, ANYBOX,               # noqa: E731,F405
                       txt(w) if w else WILDTEXT)             # noqa: F405
b_go = [copy('given', 1), put('given', 0),                    # noqa: F405
        copy('given', 2), put('given', 0)]                    # noqa: F405
b_flip = lambda hole: drop(-1, '*', 'given', hole, 2) + b_go  # noqa: E731,F405
b_lead = robot('at the left', b_cond('left'), b_flip(1), trained_on=b_trained)   # noqa: F405
b_lead['team'] = [
    robot('at the right', b_cond('right'), b_flip(1), trained_on=b_trained),     # noqa: F405
    robot('at the near wall', b_cond('near'), b_flip(2), trained_on=b_trained),  # noqa: F405
    robot('at the far wall', b_cond('far'), b_flip(2), trained_on=b_trained),    # noqa: F405
    robot('moving', b_cond(None), b_go, trained_on=b_trained),                   # noqa: F405
]
bouncing = gadget('bouncing', BOUNCE, b_lead, b_work)

# ------------------------------------------------- 14 bouncing AT A SPEED
# The same behaviour with the world's clock doing the moving. Hole 1 is the
# whole message -- [set | speed | [across | away]] -- so flipping a bounce is
# still a x-1 dropped on a number, just one box deeper. Every robot EATS the
# edge reading it acted on, which leaves the nest bare and puts the team to
# sleep until the next wall: a gadget that costs nothing while the ball
# crosses the table.
GLIDE = 'G916'
g_speed = box(num(9, 20), num(11, 40))                       # noqa: F405
g_msg = msg('set', 'speed', g_speed)                         # noqa: F405
g_work = box(to(GLIDE, 'my thing'), g_msg, edge_nest(GLIDE, 9161))    # noqa: F405
g_trained = box(to(GLIDE), g_msg, edge_nest(GLIDE, 9161))    # noqa: F405
g_cond = lambda w: box(ANYBIRD, ANYBOX,                      # noqa: E731,F405
                       txt(w) if w else WILDTEXT)            # noqa: F405
# hand the speed over, then eat the reading and doze on the bare nest
g_send = [copy('given', 1), put('given', 0),                 # noqa: F405
          takeTop('given', 2), put('s0'), vac('s0')]         # noqa: F405
# the across of the speed is given[1][2][0]; the away is given[1][2][1]
g_flip = lambda hole: drop(-1, '*', 'given', 1, 2, hole) + g_send   # noqa: E731,F405
g_lead = robot('at the left', g_cond('left'), g_flip(0), trained_on=g_trained)    # noqa: F405
g_lead['team'] = [
    robot('at the right', g_cond('right'), g_flip(0), trained_on=g_trained),     # noqa: F405
    robot('at the near wall', g_cond('near'), g_flip(1), trained_on=g_trained),  # noqa: F405
    robot('at the far wall', g_cond('far'), g_flip(1), trained_on=g_trained),    # noqa: F405
    # 'none' is what the nest holds before anything has happened: setting off
    robot('setting off', g_cond('none'), g_send, trained_on=g_trained),          # noqa: F405
]
gliding = gadget('bouncing at a speed', GLIDE, g_lead, g_work)

# ---------------------------------------------------------------- 4 wrapping
WRAP = 'G904'
w_step = msg('move', 'across', num(1, 40))                   # noqa: F405
w_left = msg('set', 'across', num(-3, 2))                    # noqa: F405
w_right = msg('set', 'across', num(3, 2))                    # noqa: F405
w_work = box(to(WRAP, 'my thing'), w_step,                   # noqa: F405
             edge_nest(WRAP, 9041), w_left, w_right)
w_cond = lambda w: box(ANYBIRD, ANYBOX,                      # noqa: E731,F405
                       txt(w) if w else WILDTEXT, ANYBOX, ANYBOX)   # noqa: F405
w_lead = robot('off the right', w_cond('right'),             # noqa: F405
               [copy('given', 3), put('given', 0)],          # noqa: F405
               trained_on=box(to(WRAP), w_step, edge_nest(WRAP, 9041), w_left, w_right))  # noqa: F405
w_lead['team'] = [
    robot('off the left', w_cond('left'),                    # noqa: F405
          [copy('given', 4), put('given', 0)],               # noqa: F405
          trained_on=box(to(WRAP), w_step, edge_nest(WRAP, 9041), w_left, w_right)),      # noqa: F405
    robot('moving', w_cond(None), give,                      # noqa: F405
          trained_on=box(to(WRAP), w_step, edge_nest(WRAP, 9041), w_left, w_right)),      # noqa: F405
]
wrapping = gadget('wrapping at the edges', WRAP, w_lead, w_work)

# ---------------------------------------------------------------- 5 pointer
FOLLOW = 'G905'
f_template = box(txt('set'), txt('position'), None)          # noqa: F405
f_work = box(to(FOLLOW, 'my thing'), point_nest(9051), f_template)   # noqa: F405
f_bot = robot(                                                # noqa: F405
    'Follower', box(ANYBIRD, ANYBOX, ANYBOX),                 # noqa: F405
    [copy('given', 2), put('s0'),                             # noqa: F405
     takeTop('given', 1), put('s0', 2),                       # noqa: F405
     take('s0'), put('given', 0)],                            # noqa: F405
    trained_on=box(to(FOLLOW), point_nest(9051), f_template))  # noqa: F405
following = gadget('following the pointer', FOLLOW, f_bot, f_work)

# ------------------------------------------------------- 13 pointer, one axis
# The same idea with one axis held still: the pointer hands over
# [across | away] and this one takes only the AWAY out of it, so the thing
# keeps its own place across the table. That is what a bat wants -- it stays
# a wall instead of wandering off after your hand -- and it is also the only
# way a following thing can be POINTED AT to stop it, since a thing that
# tracks both axes sits under the cursor for ever.
FOLLOWV = 'G915'
fv_template = box(txt('set'), txt('away'), None)             # noqa: F405
fv_work = box(to(FOLLOWV, 'my thing'), point_nest(9151), fv_template)   # noqa: F405
fv_bot = robot(                                              # noqa: F405
    'Follower', box(ANYBIRD, ANYBOX, ANYBOX),                # noqa: F405
    [copy('given', 2), put('s0'),            # a [set | away | _] to fill in  # noqa: F405
     takeTop('given', 1), put('s1'),         # what the pointer just said     # noqa: F405
     take('s1', 1), put('s0', 2),            # the AWAY of it, into the hole  # noqa: F405
     vac('s1'),                              # and the husk to Dusty          # noqa: F405
     take('s0'), put('given', 0)],           # away to my thing               # noqa: F405
    trained_on=box(to(FOLLOWV), point_nest(9151), fv_template))   # noqa: F405
following_v = gadget('following up and down', FOLLOWV, fv_bot, fv_work)

# ---------------------------------------------------------------- 6 arrows
ARROW = 'G906'
a_steps = [msg('move', 'across', num(-1, 20)),               # noqa: F405
           msg('move', 'across', num(1, 20)),
           msg('move', 'away', num(-1, 20)),
           msg('move', 'away', num(1, 20))]
a_work = box(to(ARROW, 'my thing'), keys_nest(9061), *a_steps)        # noqa: F405
a_trained = box(to(ARROW), keys_nest(9061), *a_steps)                 # noqa: F405
a_cond = lambda w: box(ANYBIRD, txt(w) if w else WILDTEXT,   # noqa: E731,F405
                       ANYBOX, ANYBOX, ANYBOX, ANYBOX)       # noqa: F405
# read the key off the nest and sweep it away, then send the step for it
eat = [takeTop('given', 1), put('s0'), vac('s0')]            # noqa: F405


def arrow(name, word, hole):
    return robot(name, a_cond(word),                          # noqa: F405
                 eat + [copy('given', hole), put('given', 0)],  # noqa: F405
                 trained_on=a_trained)


a_lead = arrow('left', 'ArrowLeft', 2)
a_lead['team'] = [
    arrow('right', 'ArrowRight', 3),
    arrow('up', 'ArrowUp', 4),
    arrow('down', 'ArrowDown', 5),
    # anything else is swallowed, so one stray key does not stop the team
    robot('any other key', a_cond(None), eat, trained_on=a_trained),   # noqa: F405
]
arrows = gadget('moving with the arrow keys', ARROW, a_lead, a_work)

# ---------------------------------------------------------------- 7..12
from make_library2 import SIX                                # noqa: E402

# ----------------------------------------------------------------------------
ABOUT = ('THE SHELF\n\n'
         'Twelve behaviours. Each is one\n'
         'pad; its panel carries the\n'
         'robots.\n\n'
         'Set one down and press SPACE\n'
         'and it does its thing to\n'
         'ITSELF -- because "my thing"\n'
         'means itself until somebody\n'
         'says otherwise. That is the\n'
         'self-demonstration, and it\n'
         'costs nothing.')

USE = ('TO USE ONE\n\n'
       '1. drop it on your thing\n'
       '2. press SPACE on it\n\n'
       'Nothing inside it is edited.\n'
       'Only which thing its bird is\n'
       'addressed to.\n\n'
       '"." stops it. Wake Ruby and\n'
       'click it and it works on\n'
       'itself again.\n\n'
       'Open its panel to read the\n'
       'robots; they are ordinary\n'
       'robots doing ordinary steps.')

WHY = ('WHAT IS NOT BUILT IN\n\n'
       'There is no move, no bounce,\n'
       'no follow. There are messages\n'
       'a thing already answers:\n\n'
       '  [move | across | 1/60]\n'
       '  [set | position | [x|z]]\n\n'
       'and robots that send them.\n\n'
       'Bouncing is three robots that\n'
       'differ only in the word they\n'
       'expect from the edge reading.\n'
       'Flipping is a x-1 dropped on\n'
       'a number.')

NEW = ('THE SECOND SIX\n\n'
       'and a fifteenth:\n'
       'reverse a speed on\n'
       'collision -- fills in ONE\n'
       'hole of the speed and\n'
       'leaves the other EMPTY, so\n'
       'it shares a thing with\n'
       'bouncing at a speed without\n'
       'the two arguing\n\n'
       'and a fourteenth:\n'
       'bouncing at a speed --\n'
       '  sets a speed once, then\n'
       '  sleeps until a wall, where\n'
       '  one x-1 flips one number.\n'
       '  The clock does the moving,\n'
       '  so it never stutters and\n'
       '  costs nothing between\n'
       '  bounces\n\n'
       'and a thirteenth:\n'
       'following up and down --\n'
       '  the pointer\'s AWAY only,\n'
       '  so it keeps its own place\n'
       '  across the table (a bat),\n'
       '  and can still be pointed\n'
       '  at to stop it\n\n'
       'grow / shrink when bumped\n'
       '  doze on the bump channel;\n'
       '  a hit is [move | size | 1/4]\n\n'
       'make a sound on hit\n'
       '  gives "play" to its bell\n\n'
       'reverse on collision\n'
       '  sets the step away from\n'
       '  what it hit, like the ball\n\n'
       'speed limit\n'
       '  weighs the speed against\n'
       '  the limit on a SCALE: the\n'
       '  scale is the if\n\n'
       'send 1 to the score on hit\n'
       '  a badged +1 to its bird')

star = live(pad('*', bg='#1b2233', ink='#ffd23f', font='sans'), 'L9599')   # noqa: F405

bench = [
    {'thing': star, 'x': 0.35, 'z': 1.15},

    {'thing': moving_right, 'x': -1.50, 'z': 1.15},
    {'thing': moving_left, 'x': -1.50, 'z': 1.48},
    {'thing': bouncing, 'x': -1.50, 'z': 1.81},
    {'thing': wrapping, 'x': -0.95, 'z': 1.15},
    {'thing': following, 'x': -0.95, 'z': 1.48},
    {'thing': following_v, 'x': 0.70, 'z': 1.81},
    {'thing': gliding, 'x': 0.15, 'z': 1.15},
    {'thing': arrows, 'x': -0.95, 'z': 1.81},

    {'thing': SIX['growing'], 'x': -0.40, 'z': 1.15},
    {'thing': SIX['shrinking'], 'x': -0.40, 'z': 1.48},
    {'thing': SIX['sounding'], 'x': -0.40, 'z': 1.81},
    {'thing': SIX['reversing'], 'x': 0.15, 'z': 1.48},
    {'thing': SIX['limiting'], 'x': 0.15, 'z': 1.81},
    {'thing': SIX['scoring'], 'x': 0.70, 'z': 1.48},
    {'thing': SIX['reversing_speed'], 'x': 0.15, 'z': 1.48},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.28},           # noqa: F405
    {'thing': txt(USE), 'x': -0.75, 'z': 2.28},             # noqa: F405
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.28},             # noqa: F405
    {'thing': txt(NEW), 'x': 0.65, 'z': 2.28},              # noqa: F405
]

write_beh('library', bench)
