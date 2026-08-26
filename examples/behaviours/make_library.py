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

LOOK = dict(bg='#2a2135', ink='#e8d7ff', font='sans', h=0.42)


def gadget(name, lid, bot, work, look=None):
    """A pad whose panel holds one robot and the box it works on."""
    return {'kind': 'text', 'text': name, 'gadget': True,
            'lid': lid, 'evt': 'evt-' + lid,
            'look': dict(look or LOOK),
            'panel': {'kind': 'world', 'v': 3, 'bench': [],
                      'stations': {'stand': work}, 'active': bot}}


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
BOUNCE = 'G903'
b_step = msg('move', 'across', num(1, 40))                   # noqa: F405
b_work = box(to(BOUNCE, 'my thing'), b_step, edge_nest(BOUNCE, 9031))   # noqa: F405
b_trained = box(to(BOUNCE), b_step, edge_nest(BOUNCE, 9031))            # noqa: F405
b_cond = lambda w: box(ANYBIRD, ANYBOX,                       # noqa: E731,F405
                       txt(w) if w else WILDTEXT)             # noqa: F405
flip_and_go = drop(-1, '*', 'given', 1, 2) + give             # noqa: F405
b_lead = robot('at the left', b_cond('left'), flip_and_go, trained_on=b_trained)   # noqa: F405
b_lead['team'] = [
    robot('at the right', b_cond('right'), flip_and_go, trained_on=b_trained),     # noqa: F405
    robot('moving', b_cond(None), give, trained_on=b_trained),                     # noqa: F405
]
bouncing = gadget('bouncing', BOUNCE, b_lead, b_work)

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

# ----------------------------------------------------------------------------
ABOUT = ('THE SHELF\n\n'
         'Six behaviours. Each is one\n'
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

star = live(pad('*', bg='#1b2233', ink='#ffd23f', font='sans'), 'L9599')   # noqa: F405

bench = [
    {'thing': star, 'x': -0.30, 'z': 1.15},

    {'thing': moving_right, 'x': -1.50, 'z': 1.15},
    {'thing': moving_left, 'x': -1.50, 'z': 1.52},
    {'thing': bouncing, 'x': -1.50, 'z': 1.89},
    {'thing': wrapping, 'x': -0.95, 'z': 1.15},
    {'thing': following, 'x': -0.95, 'z': 1.52},
    {'thing': arrows, 'x': -0.95, 'z': 1.89},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.28},           # noqa: F405
    {'thing': txt(USE), 'x': -0.75, 'z': 2.28},             # noqa: F405
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.28},             # noqa: F405
]

write_beh('library', bench)
