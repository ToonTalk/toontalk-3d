# space invaders -- built the way the original ToonTalk's "Space Behaviours"
# was, and readable the way it was.
#
# Every picture in that game carried its behaviours on its BACK as a row of
# anima-gadgets, each a small picture with a sentence beside it ("I explode
# when a white bullet hits me"); flip a gadget and you saw its own back: the
# sentence again, the robots, and the box they work on with its sensors.
#
# Here a picture is a pad, its back is its PANEL, and a gadget on the back is
# a CARD standing on that panel: a pad whose face IS the sentence, and whose
# own panel holds the robots and the box. Point at anything and press the
# gear to see its back; point at a card on that back and press the gear to
# see the card's; the knob folds each one home again. Nothing here is a new
# kind of thing, and nothing is a picture of a program: every card runs.
#
# What the game needs from the workshop, and where it came from:
#
#   the TOUCH reading   [touching | side | name | normal]  -- the original's
#                       "Touching Who?" sensor, matched by NAME in a hole
#   the EDGE reading    which wall a rider is against
#   a SPEED             a thing moving on the world's clock, switched with it
#   the KEYBOARD nest   one of the workshop's own senses
#   [drop | thing | [across | away]]   how the ship fires: a copy of the
#                       bullet, set down beside it, and it arrives working
#   [vanish]            a bullet at the top, an invader that was hit
#   [listen | touches | bird]   the field's own referee reading, for the score
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'behaviours'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'images'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'sounds'))
from _beh import *                                          # noqa: F403
from _img import _png_rgba                                  # noqa: F401
from _snd import seg, sound                                 # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))

# --- the pictures: pixel art, drawn to a data URL -----------------------------
INVADER = ['..X.....X..',
           '...X...X...',
           '..XXXXXXX..',
           '.XX.XXX.XX.',
           'XXXXXXXXXXX',
           'X.XXXXXXX.X',
           'X.X.....X.X',
           '...XX.XX...']
SHIP = ['.....X.....',
        '....XXX....',
        '....XXX....',
        '.XXXXXXXXX.',
        'XXXXXXXXXXX',
        'XXXXXXXXXXX',
        '.XXXXXXXXX.']
BULLET = ['.X.',
          'XXX',
          'XXX',
          'XXX',
          'XXX',
          'XXX',
          'XXX',
          'XXX',
          '.X.']


def sprite(rows, rgb, scale=8):
    """Nearest-neighbour pixel art on nothing: the corners are see-through,
    so a sprite on the field is the shape it is, not a tile."""
    out = []
    for r in rows:
        line = []
        for ch in r:
            line += [(rgb + (255,)) if ch == 'X' else (0, 0, 0, 0)] * scale
        out += [line] * scale
    return _png_rgba(out)


INVADER_IMG = sprite(INVADER, (0x7e, 0xe7, 0x87))
SHIP_IMG = sprite(SHIP, (0x7f, 0xd3, 0xff))
BULLET_IMG = sprite(BULLET, (0xff, 0xff, 0xff))

# --- names ---------------------------------------------------------------------
FIELD, SHIP_L, SCORE = 'P940', 'P941', 'P942'
BULLET_L = 'P943'                       # the prototype in the ship's work box
INVADERS = ['P95%d' % i for i in range(8)]

CARD = dict(bg='#2a2135', ink='#e8d7ff', font='sans', w=1.3, h=0.55)
CARD2 = dict(bg='#1f2f3f', ink='#dff1ff', font='sans', w=1.3, h=0.55)
CARD3 = dict(bg='#3a2416', ink='#ffe8d0', font='sans', w=1.3, h=0.55)

DROP_MSG = box(txt('drop'), None, box(num(0), num(-1, 3)))   # noqa: F405


def picture(img, label, lid, w, h, cards, extra=None, bg='#0b1020'):
    """A picture with cards on its back: a gadget whose panel groups the
    behaviours and has no robot of its own -- SPACE on it starts them all."""
    t = {'kind': 'text', 'text': '', 'img': img, 'gadget': True,
         'label': label, 'lid': lid, 'evt': 'evt-' + lid,
         'look': dict(bg=bg, w=w, h=h),
         'panelSize': [0.9, 0.62],
         'panel': {'kind': 'world', 'v': 3, 'active': None, 'stations': {},
                   'bench': [{'thing': c, 'x': 0, 'z': 1.7} for c in cards]}}
    if extra:
        t.update(extra)
    return t


def card(sentence, lid, bot, work, look=CARD, bench=None, bound=None):
    """A gadget whose face is its sentence."""
    g = gadget(sentence, lid, bot, work, look=look, bench=bench)   # noqa: F405
    if bound:
        g['boundTo'] = bound
    return g


def edge_nest(lid, nid, reading='none'):
    return {'kind': 'nest', 'id': nid, 'guid': 'evt-' + lid + '#edge',
            'hasEgg': False, 'label': 'edge', 'pile': [txt(reading)]}   # noqa: F405


# --- the invader's two cards ----------------------------------------------------
def march_card(lid, i):
    """I march across, and at the edge I drop down and turn round.
    The march is a SPEED; the card only turns it round at the walls."""
    nid = 9300 + i * 10
    left = msg('set', 'speed', box(num(-1, 4), None))           # noqa: F405
    right = msg('set', 'speed', box(num(1, 4), None))           # noqa: F405
    down = msg('move', 'away', num(1, 9))                       # noqa: F405
    nudge_l = msg('move', 'across', num(-1, 30))                # noqa: F405
    nudge_r = msg('move', 'across', num(1, 30))                 # noqa: F405
    #  0 my thing  1 edge  2 go left  3 go right  4 drop down  5 nudge left  6 nudge right
    work = box(to(lid, 'my thing'), edge_nest(lid, nid), left, right, down,   # noqa: F405
               nudge_l, nudge_r)
    trained = lambda e: box(to(lid), edge_nest(lid, nid, e), left, right, down,   # noqa: E731,F405
                            nudge_l, nudge_r)
    cond = lambda e: box(ANYBIRD, txt(e), ANYBOX, ANYBOX, ANYBOX, ANYBOX, ANYBOX)   # noqa: E731,F405
    at_right = robot('at the right wall', cond('right'),        # noqa: F405
                     [copy('given', 4), put('given', 0),        # noqa: F405
                      copy('given', 2), put('given', 0),        # noqa: F405
                      copy('given', 5), put('given', 0)],       # noqa: F405
                     trained_on=trained('right'),
                     note='Leads the pair. The edge reading says “right”: sends drop '
                          'down, go left, and a nudge left off the wall. The march '
                          'itself is a speed; this card only turns it at the walls.')
    at_left = robot('at the left wall', cond('left'),           # noqa: F405
                    [copy('given', 4), put('given', 0),         # noqa: F405
                     copy('given', 3), put('given', 0),         # noqa: F405
                     copy('given', 6), put('given', 0)],        # noqa: F405
                    trained_on=trained('left'),
                    note='The edge reading says “left”: sends drop down, go right, and '
                         'a nudge right off the wall.')
    at_right['team'] = [at_left]
    return card('I march across, and at a wall\nI drop down and turn round.',
                'G%d' % (nid + 1), at_right, work, bound=lid)


def explode_card(lid, i):
    """I explode when a bullet hits me: a bang, and I vanish."""
    nid = 9300 + i * 10 + 5
    bang = sound(seg(160, 0.12, 'square'), seg(80, 0.25, 'sawtooth'), label='bang')
    bang = dict(bang, lid='S%d' % nid, evt='evt-S%d' % nid)
    play = txt('play')                                          # noqa: F405
    gone = txt('vanish')                                        # noqa: F405
    #  0 my thing  1 touching  2 the bang  3 play  4 vanish
    work = box(to(lid, 'my thing'), touch_nest(lid, nid, empty=True),   # noqa: F405
               to('S%d' % nid, 'the bang'), play, gone)
    trained = lambda name: box(to(lid), touch_nest(lid, nid, to(BULLET_L), 'far', name),   # noqa: E731,F405
                               to('S%d' % nid), play, gone)
    hit = robot('hit by a bullet',                              # noqa: F405
                box(ANYBIRD, touch_cond(name='bullet'), ANYBIRD, WILDTEXT, WILDTEXT),   # noqa: F405
                [copy('given', 3), put('given', 2),             # noqa: F405
                 copy('given', 4), put('given', 0)],            # noqa: F405
                trained_on=trained('bullet'),
                note='Leads the pair. The touch reading names a bullet: gives “play” '
                     'to the bang, then sends my thing [vanish].')
    # anything else that touches me, or the end of a contact, is not news:
    # eaten, so the next reading can be seen
    other = robot('something else', box(ANYBIRD, touch_cond(), ANYBIRD, WILDTEXT, WILDTEXT),   # noqa: F405
                  [takeTop('given', 1), put('s0'), vac('s0')],  # noqa: F405
                  trained_on=trained('nothing'),
                  note='Anything else touching me, or a contact ending, is not news: '
                       'eats the reading so the next one can be seen.')
    hit['team'] = [other]
    return card('I explode when a bullet\nhits me: a bang, and I vanish.',
                'G%d' % (nid + 1), hit, work, look=CARD3,
                bench=[{'thing': bang, 'x': 0.9, 'z': 1.8}], bound=lid)


def invader(i):
    return picture(INVADER_IMG, 'invader', INVADERS[i], 0.36, 0.28,
                   [march_card(INVADERS[i], i), explode_card(INVADERS[i], i)],
                   extra={'speed': {'x': 0.25, 'z': 0}})


# --- the bullet's card ----------------------------------------------------------
def bullet_card():
    """I fly up; at the top, or when I hit an invader, I vanish."""
    nid = 9390
    gone = txt('vanish')                                        # noqa: F405
    #  0 my thing  1 edge  2 touching  3 vanish
    work = box(to(BULLET_L, 'my thing'), edge_nest(BULLET_L, nid),   # noqa: F405
               touch_nest(BULLET_L, nid + 1, empty=True), gone)
    trained = lambda e, name: box(to(BULLET_L), edge_nest(BULLET_L, nid, e),   # noqa: E731,F405
                                  touch_nest(BULLET_L, nid + 1, to(INVADERS[0]) if name != 'nothing' else None, 'far', name), gone)
    top = robot('at the top', box(ANYBIRD, txt('far'), WILD, WILDTEXT),   # noqa: F405
                [copy('given', 3), put('given', 0)],            # noqa: F405
                trained_on=trained('far', 'nothing'),
                note='Leads the team. The edge reading says “far” -- the top of the '
                     'field: sends my thing [vanish].')
    hit = robot('hit an invader', box(ANYBIRD, WILDTEXT, touch_cond(name='invader'), WILDTEXT),   # noqa: F405
                [copy('given', 3), put('given', 0)],            # noqa: F405
                trained_on=trained('none', 'invader'),
                note='The touch reading names an invader: sends my thing [vanish].')
    other = robot('something else', box(ANYBIRD, WILDTEXT, touch_cond(), WILDTEXT),   # noqa: F405
                  [takeTop('given', 2), put('s0'), vac('s0')],  # noqa: F405
                  trained_on=trained('none', 'nothing'),
                  note='Any other touch reading: eats it so the next one can be seen.')
    top['team'] = [hit, other]
    return card('I fly up. At the top, or when\nI hit an invader, I vanish.',
                'G9391', top, work, look=CARD2, bound=BULLET_L)


bullet = picture(BULLET_IMG, 'bullet', BULLET_L, 0.08, 0.26, [bullet_card()],
                 extra={'speed': {'x': 0, 'z': -0.9}})

# --- the ship's two cards -----------------------------------------------------------
KEYS_A, KEYS_B = 9401, 9411


def steer_card():
    """I move with the arrow keys."""
    left = msg('move', 'across', num(-1, 10))                   # noqa: F405
    right = msg('move', 'across', num(1, 10))                   # noqa: F405
    #  0 my thing  1 keyboard  2 a step left  3 a step right
    work = box(to(SHIP_L, 'my thing'), device(KEYS_A, DEV_KEYS, 'keyboard'), left, right)   # noqa: F405
    trained = lambda k: box(to(SHIP_L), dict(device(KEYS_A, DEV_KEYS, 'keyboard'), pile=[txt(k)]), left, right)   # noqa: E731,F405
    eat = [takeTop('given', 1), put('s0'), vac('s0')]           # noqa: F405
    go_left = robot('left arrow', box(ANYBIRD, txt('ArrowLeft'), ANYBOX, ANYBOX),   # noqa: F405
                    eat + [copy('given', 2), put('given', 0)], trained_on=trained('ArrowLeft'),   # noqa: F405
                    note='Leads the team. The key on the nest is ArrowLeft: eats it and '
                         'sends [move | across | -1/10].')
    go_right = robot('right arrow', box(ANYBIRD, txt('ArrowRight'), ANYBOX, ANYBOX),   # noqa: F405
                     eat + [copy('given', 3), put('given', 0)], trained_on=trained('ArrowRight'),   # noqa: F405
                     note='The key on the nest is ArrowRight: eats it and sends '
                          '[move | across | 1/10].')
    # every other key is somebody else's: off the nest, so the next can be seen
    other = robot('any other key', box(ANYBIRD, WILDTEXT, ANYBOX, ANYBOX),   # noqa: F405
                  eat, trained_on=trained('q'),
                  note='Any other key is somebody else’s: eats it so the next one can '
                       'be seen.')
    go_left['team'] = [go_right, other]
    return card('I move with the left and\nright arrow keys.', 'G9402', go_left, work, bound=SHIP_L)


def fire_card():
    """I fire a bullet with the up arrow: a copy of the bullet, dropped
    just above me, and off it goes."""
    #  0 my thing  1 keyboard  2 the bullet  3 [drop | _ | [0 | -1/3]]
    work = box(to(SHIP_L, 'my thing'), device(KEYS_B, DEV_KEYS, 'keyboard'), bullet, DROP_MSG)   # noqa: F405
    trained = lambda k: box(to(SHIP_L), dict(device(KEYS_B, DEV_KEYS, 'keyboard'), pile=[txt(k)]), bullet, DROP_MSG)   # noqa: E731,F405
    eat = [takeTop('given', 1), put('s0'), vac('s0')]           # noqa: F405
    fire = robot('up arrow', box(ANYBIRD, txt('ArrowUp'), WILD, ANYBOX),   # noqa: F405
                 eat + [copy('given', 3), put('s1'),            # noqa: F405
                        copy('given', 2), put('s1', 1),         # noqa: F405
                        take('s1'), put('given', 0)],           # noqa: F405
                 trained_on=trained('ArrowUp'),
                 note='Leads the pair. The key is ArrowUp: eats it, puts a copy of the '
                      'bullet into the [drop | _ | [0 | -1/3]] message, and sends it -- '
                      'a bullet set down just above me, arriving switched on.')
    other = robot('any other key', box(ANYBIRD, WILDTEXT, WILD, ANYBOX),   # noqa: F405
                  eat, trained_on=trained('q'),
                  note='Any other key is somebody else’s: eats it so the next one can '
                       'be seen.')
    fire['team'] = [other]
    return card('I fire a bullet with the up\narrow: a copy of the bullet,\ndropped just above me.',
                'G9412', fire, work, look=CARD2, bound=SHIP_L)


ship = picture(SHIP_IMG, 'ship', SHIP_L, 0.34, 0.24, [steer_card(), fire_card()])

# --- the field, and its referee ---------------------------------------------------
score = dict(live(num(0), SCORE), label='score')            # noqa: F405


def referee_card():
    """I keep the score: one for every bullet that meets an invader."""
    nid = 9420
    one = num(1)                                                # noqa: F405
    #  0 my thing (the field)  1 touches  2 one  3 the score
    work = box(to(FIELD, 'my thing'), touches_nest(FIELD, nid), one, to(SCORE, 'the score'))   # noqa: F405
    pair = lambda a, b: box(to(INVADERS[0]), txt(a), to(BULLET_L), txt(b),   # noqa: E731,F405
                            box(num(0), num(-1)))               # noqa: F405
    trained = lambda a, b: box(to(FIELD), dict(touches_nest(FIELD, nid), pile=[pair(a, b)]), one, to(SCORE))   # noqa: E731,F405
    eat = [takeTop('given', 1), put('s0'), vac('s0')]           # noqa: F405
    ib = robot('an invader and a bullet', box(ANYBIRD, touches_cond('invader', 'bullet'), ANYNUM, ANYBIRD),   # noqa: F405
               [copy('given', 2), put('given', 3)] + eat, trained_on=trained('invader', 'bullet'),   # noqa: F405
               note='Leads the team. The field’s touches reading names an invader and '
                    'a bullet: gives a +1 to the score’s bird, and eats the reading.')
    bi = robot('a bullet and an invader', box(ANYBIRD, touches_cond('bullet', 'invader'), ANYNUM, ANYBIRD),   # noqa: F405
               [copy('given', 2), put('given', 3)] + eat, trained_on=trained('bullet', 'invader'),   # noqa: F405
               note='The same pair named the other way round: a +1 to the score, and '
                    'eats the reading.')
    other = robot('anything else meeting', box(ANYBIRD, touches_cond(), ANYNUM, ANYBIRD),   # noqa: F405
                  eat, trained_on=trained('ship', 'bullet'),
                  note='Any other pair meeting on the field: eats the reading.')
    ib['team'] = [bi, other]
    return card('I keep the score: one for\nevery bullet that meets\nan invader.', 'G9421', ib, work,
                look=CARD3, bound=FIELD)


riders = [{'thing': ship, 'at': {'u': 0, 'v': 0.42}}]
for i in range(8):
    riders.append({'thing': invader(i),
                   'at': {'u': -0.42 + (i % 4) * 0.2, 'v': -0.55 + (i // 4) * 0.22}})

field = picture(None, 'space', FIELD, 3.2, 2.2, [referee_card()],
                extra={'subs': riders, 'panelSize': [0.8, 0.5]})
del field['img']

# --- the table --------------------------------------------------------------------------
ABOUT = ('SPACE INVADERS\n\n'
         'Every picture here carries\n'
         'its behaviours on its back,\n'
         'as cards that say what they\n'
         'do -- the way the original\n'
         'ToonTalk\'s Space Behaviours\n'
         'did.\n\n'
         'Point at an invader and press\n'
         'the gear to see its back.\n'
         'Point at a card there and\n'
         'press the gear again to see\n'
         'the card\'s: its robots, and\n'
         'the box they work on.')

RUN = ('TO PLAY\n\n'
       'Point at the dark field and\n'
       'press SPACE: everything on\n'
       'it starts.\n\n'
       'Left and right arrows move\n'
       'the ship. The up arrow fires.\n\n'
       'The score counts the bullets\n'
       'that meet an invader.\n\n'
       'Press "." on the field to\n'
       'stop the lot.')

HOW = ('HOW IT IS MADE\n\n'
       'Nothing in it is new. The\n'
       'touch reading says WHO ran\n'
       'into whom by name, so the\n'
       'invader\'s card is trained on\n'
       '"a bullet". The ship fires\n'
       'with [drop | bullet | ...]:\n'
       'a copy of the bullet in its\n'
       'work box, set down above it,\n'
       'and it arrives working.\n'
       '[vanish] takes a bullet or an\n'
       'invader out of the game. The\n'
       'field\'s own card listens to\n'
       'TOUCHES -- every pair that\n'
       'meets -- and keeps the score.')

bench = [
    {'thing': field, 'x': 0.0, 'z': 1.62},
    {'thing': score, 'x': 1.35, 'z': 1.25},
    {'thing': txt(ABOUT), 'x': -1.35, 'z': 1.45},               # noqa: F405
    {'thing': txt(RUN), 'x': -1.35, 'z': 2.12},                  # noqa: F405
    {'thing': txt(HOW), 'x': 1.35, 'z': 2.0},                    # noqa: F405
]

write('👾 space-invaders', bench, HERE)                             # noqa: F405
