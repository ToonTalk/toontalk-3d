# -*- coding: utf-8 -*-
# THE KEEPER'S ROUND: the zoo, with a button on the grass that asks the yard
# what is out there and gives every animal a wiggle.
#
# The yard is a thing with a name, so a robot can write to it. The button is
# a behaviour whose work box holds a bird to the yard, a nest for the yard's
# answer, the wiggle behaviour to hand out, and a [bind | _] letter to hand it
# out in. Two robots:
#
#   Ask the yard      sends [query | each | bird-to-my-nest] -- the yard
#                     answers with ONE delivery per thing on the grass, oldest
#                     first off the nest: [a bird to it | name | place | kind]
#   Give it a wiggle  takes an entry whose kind is "model" (an animal, not the
#                     welcome sign), puts a copy of the wiggle behaviour in a
#                     [bind | _] letter and gives it to the bird in the entry
#   Not an animal     lets any other entry go, so the next one can be reached
#
# One animal a round: that is how a robot walks a list here. Nothing counts.
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'behaviours'))
from _beh import *                                          # noqa: F403
import make_zoo as Z                                        # noqa: E402

YARD = 'YARD1'
WIGGLE = 'W901'
KEEPER = 'K901'
REPORT = (9950, 'zoo-report')

# --- the wiggle: yaw a little one way, then the other, every round --------
# ONE turn a round, the other way the next: both turns in one round land a
# split second apart and the animal sits still to the eye. A token pad moves
# between two holes, and whichever hole holds it says which robot's turn it is.
#  0 [move | yaw | 25]   1 [move | yaw | -25]   2 tick   3 (tock)
# (my thing is the bird on the perch: whatever the panel is the back of)
wiggle_work = box(msg('move', 'yaw', num(25)),              # noqa: F405
                  msg('move', 'yaw', num(-25)),             # noqa: F405
                  txt('tick'), None)                        # noqa: F405
one_way = robot(                                            # noqa: F405
    'one way', box(ANYBOX, ANYBOX, WILDTEXT, None),         # noqa: F405
    [copy('given', 0), put('perch'),                        # noqa: F405
     take('given', 2), put('given', 3)],                    # the token crosses over  # noqa: F405
    trained_on=box(msg('move', 'yaw', num(25)), msg('move', 'yaw', num(-25)), txt('tick'), None),   # noqa: F405
    note='The token is in hole 3: turn 25 degrees this way (a copy of the turn to the bird on the perch), and move the token to hole 4.')
other_way = robot(                                          # noqa: F405
    'the other way', box(ANYBOX, ANYBOX, None, WILDTEXT),   # noqa: F405
    [copy('given', 1), put('perch'),                        # noqa: F405
     take('given', 3), put('given', 2)],                    # noqa: F405
    note='The token is in hole 4: turn 25 degrees back, and move the token to hole 3.')
wiggle = gadget('wiggle', WIGGLE, dict(one_way, team=[other_way]), wiggle_work,   # noqa: F405
                look=dict(bg='#2f3a55', ink='#dfe8ff', font='sans', h=0.34))

# --- the button --------------------------------------------------------------
#  0 the yard   1 the report nest   2 the wiggle   3 [bind | _]   4 [go]
#  5 [query | each | _]   6 a bird to the report nest
keeper_work = box(to(YARD, 'the yard'),                     # noqa: F405
                  nest(*REPORT, label='the report'),        # noqa: F405
                  wiggle,
                  box(txt('bind'), None),                   # noqa: F405
                  box(txt('go')),                           # the "go": a box, which a vacuum takes whole  # noqa: F405
                  box(txt('query'), txt('each'), None),     # noqa: F405
                  bird(*REPORT, label='to my report'))      # noqa: F405
ANY7 = lambda **at: box(*[at.get('h%d' % i, d) for i, d in enumerate(   # noqa: E731,F405
    [ANYBIRD, None, None, ANYBOX, None, ANYBOX, ANYBIRD])])             # noqa: F405

ask = robot(                                                # noqa: F405
    'Ask the yard', ANY7(h4=ANYBOX),                        # noqa: F405
    [take('given', 4), put('s0'), vac('s0'),               # the "go" is spent first, so this asks ONCE  # noqa: F405
     copy('given', 5), put('s0'),                           # the letter  # noqa: F405
     copy('given', 6), put('s0', 2),                        # ...with a bird to my report in it  # noqa: F405
     take('s0'), put('given', 0)],                          # to the yard  # noqa: F405
    trained_on=keeper_work,
    note='While "go" lies in hole 5 there is a round to make: sends the yard [query | each | a bird to my report] and spends the go, so it asks once. Put any pad back in that hole to ask again.')

entry = lambda kind: box(ANYBIRD, WILDTEXT, ANYBOX, kind)   # noqa: E731,F405
give = robot(                                               # noqa: F405
    'Give it a wiggle', ANY7(h1=entry(txt('model'))),       # noqa: F405
    [takeTop('given', 1), put('s0'),                        # the entry: [bird | name | place | kind]  # noqa: F405
     copy('given', 3), put('s1'),                           # a [bind | _] letter  # noqa: F405
     copy('given', 2), put('s1', 1),                        # ...with a copy of the wiggle in it  # noqa: F405
     take('s1'), put('s0', 0),                              # given to the bird to the animal  # noqa: F405
     vac('s0')],                                            # noqa: F405
    note='An entry on the report whose kind is "model" is an animal. Takes it off the nest, puts a copy of the wiggle in a [bind | _] letter, and gives the letter to the bird to that animal -- which is dropping the wiggle on it, by mail.')
skip = robot(                                               # noqa: F405
    'Not an animal', ANY7(h1=entry(WILDTEXT)),              # noqa: F405
    [takeTop('given', 1), put('s0'), vac('s0')],            # noqa: F405
    note='Any other entry -- the welcome sign, a pad, this very button -- is let go, so the next entry can be reached.')

button = gadget('wiggle the animals', KEEPER,               # noqa: F405
                dict(ask, team=[give, skip]), keeper_work,
                look=dict(bg='#4a2a1a', ink='#ffe3c4', font='sans', h=0.42))
button['note'] = ('The keeper’s round. SPACE here asks the yard for every thing on the grass, one '
                  'at a time, and gives each animal a wiggle by mail. Open its panel to see the three '
                  'robots and the letters they send.')

sign = {'kind': 'text', 'text': ('Welcome to the zoo!\n\n'
                                 'Press SPACE on the brown\n'
                                 'pad by the door: the keeper\n'
                                 'asks the yard who is here\n'
                                 'and every animal gets a\n'
                                 'wiggle. Open the pad\'s\n'
                                 'panel to see how.')}
HOW = {'kind': 'text', 'text': ('HOW THE KEEPER KNOWS\n\n'
                                'The yard is a thing with a\n'
                                'name. Write to it:\n\n'
                                '[query | each | bird]\n'
                                'answers one letter per thing\n'
                                'on the grass -- a bird to it,\n'
                                'its name, its place, its kind.\n\n'
                                'An entry whose kind is\n'
                                '"model" is an animal. The\n'
                                'keeper puts the wiggle in a\n'
                                '[bind | _] letter and gives it\n'
                                'to that bird: dropping the\n'
                                'behaviour on the animal, by\n'
                                'mail. One animal a round.')}

animals = [Z.elephant, Z.giraffe, Z.lion, Z.zebra, Z.penguin, Z.crocodile, Z.flamingo]
places = [(-1.6, 2.4), (0.4, 2.2), (2.2, 2.6), (-0.6, 4.2), (1.4, 4.4), (3.2, 4.2), (-2.8, 2.8)]

world = {
    'kind': 'world', 'v': 4, 'stations': {}, 'active': None,
    'name': 'zoo keeper',
    'bench': [],
    'yard': {'lid': YARD, 'evt': 'evt-' + YARD, 'bench': [
        {'thing': sign, 'x': -3.4, 'z': 6.0},
        {'thing': HOW, 'x': -3.4, 'z': 7.0},
        *[Z.on_ground(a, x, z) for a, (x, z) in zip(animals, places)],
        {'thing': button, 'x': -2.4, 'z': 6.4},
    ]},
}
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '🦓 zoo-keeper.world.json')
io.open(out, 'w', encoding='utf-8', newline='').write(json.dumps(world, ensure_ascii=False))
print('wrote', out)
