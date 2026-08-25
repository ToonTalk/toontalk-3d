# transforms -- arithmetic you can hear.
#
# A number dropped on a thing is how everything in the workshop is changed, and
# a sound is no exception: it answers x and set, and refuses +. What x MEANS
# for a sound is playback rate, so x2 is an octave up and half as long, x1/2 an
# octave down and twice as long, and x-1 -- multiplying by a NEGATIVE -- turns
# time's arrow round and plays it backwards.
#
# That last one is the point of the world. "Negative" is not a special case
# anybody wrote for sounds; it is the same minus sign that makes a number
# subtract, applied to a thing whose axis happens to be time.
from _snd import *                                         # noqa: F403

# a little rising phrase, so speed and direction are both audible
PHRASE = [note('C4', 0.22), note('E4', 0.22), note('G4', 0.22),
          note('C5', 0.34)]

ABOUT = ('REMAKING A SOUND\n\n'
         'Drop a number on a sound\n'
         'and it is remade.\n\n'
         'x2 plays it twice as fast\n'
         '-- an octave up, and half\n'
         'as long. x1/2 stretches it\n'
         'the other way.\n\n'
         'x-1 plays it BACKWARDS.\n'
         'Nothing was written for\n'
         'that: it is the same minus\n'
         'sign that makes a number\n'
         'subtract, on a thing whose\n'
         'axis is time.')

RUN = ('TO TRY IT\n\n'
       'Press SPACE over the first\n'
       'speaker to hear the phrase.\n\n'
       'Drop the x2 on the second,\n'
       'the x1/2 on the third, the\n'
       'x-1 on the fourth. Each\n'
       'plays as it changes, and\n'
       'the screen shows what it\n'
       'has become.\n\n'
       'They stack: drop the x-1 on\n'
       'the one you already sped\n'
       'up.')

WHY = ('WHAT IS REFUSED\n\n'
       'Try dropping a +2 on a\n'
       'sound. It comes back with\n'
       '"adding to a sound has no\n'
       'meaning" -- type * on the\n'
       'number first.\n\n'
       'A thing is allowed to say\n'
       'no. Refusing a message you\n'
       'have no reading for is the\n'
       'honest answer, and it is\n'
       'how you learn what a kind\n'
       'understands.')

n = lambda v, d=1: num(v, d, '*')

bench = [
    {'thing': sound(*PHRASE, label='as made'), 'x': -1.50, 'z': 1.15},
    {'thing': sound(*PHRASE, label='faster'), 'x': -1.00, 'z': 1.15},
    {'thing': sound(*PHRASE, label='slower'), 'x': -0.50, 'z': 1.15},
    {'thing': sound(*PHRASE, label='backwards'), 'x': 0.00, 'z': 1.15},

    {'thing': n(2), 'x': -1.00, 'z': 1.62},
    {'thing': n(1, 2), 'x': -0.50, 'z': 1.62},
    {'thing': n(-1), 'x': 0.00, 'z': 1.62},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},
]

write_sounds('transforms', bench)
