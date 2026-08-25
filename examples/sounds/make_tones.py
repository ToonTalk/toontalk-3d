# tones -- where a sound comes from.
#
# A sound arrives silent: a speaker with a flat line on its little screen. It
# is MADE by dropping a [frequency, seconds, shape] box on it, and that box is
# an ordinary box you can edit -- so the four waveshapes are laid out as pads
# to swap into its third hole, and the frequency is a number to type on.
#
# Nothing here is a program. It is the vocabulary the other two worlds use.
from _snd import *                                         # noqa: F403

ABOUT = ('MAKING A SOUND\n\n'
         'A sound starts silent -- a\n'
         'flat line on its screen.\n\n'
         'Drop the [frequency,\n'
         'seconds, shape] box on one\n'
         'and it sings: the number is\n'
         'hertz, the fraction is how\n'
         'long, the pad is which of\n'
         'the four waveshapes.\n\n'
         'The waveform on the screen\n'
         'is what it will sound like.')

RUN = ('TO TRY IT\n\n'
       'Press SPACE with a sound in\n'
       'your hand, or under the\n'
       'pointer, to play it; "." to\n'
       'stop it.\n\n'
       'Drop the box on the silent\n'
       'speaker. Then pick the box\n'
       'up again, type a different\n'
       'number on its frequency,\n'
       'swap a shape pad into its\n'
       'third hole, and drop it on\n'
       'the next one.\n\n'
       'Every sound here was made\n'
       'exactly this way.')

WHY = ('THE FOUR SHAPES\n\n'
       'Same pitch, same length --\n'
       'four different instruments.\n'
       'A sine is a whistle, a\n'
       'square a game console, a\n'
       'sawtooth a brass section, a\n'
       'triangle something between\n'
       'a flute and a bell.\n\n'
       'Anything else in that hole\n'
       'is read as "sine".')

bench = [
    # The workshop's own notebook sits at about x 0.95, so everything a world
    # lays out keeps to the left of it -- otherwise the bench shoves things
    # aside to make room and the arrangement you wrote is not the one you get.
    {'thing': tone_box(440, (1, 2), 'sine'), 'x': -1.50, 'z': 1.15},
    {'thing': silent(), 'x': -0.90, 'z': 1.15},

    # the same note, sine and square, to hear the difference side by side
    {'thing': sound(seg(NOTES['A4'], 0.6, 'sine'), label='sine'),
     'x': -0.40, 'z': 1.15},
    {'thing': sound(seg(NOTES['A4'], 0.6, 'square'), label='square'),
     'x': 0.10, 'z': 1.15},

    # and the four shape words, to swap into the recipe's third hole
    {'thing': txt('sine'), 'x': -1.50, 'z': 1.60},
    {'thing': txt('square'), 'x': -1.05, 'z': 1.60},
    {'thing': txt('sawtooth'), 'x': -0.60, 'z': 1.60},
    {'thing': txt('triangle'), 'x': -0.15, 'z': 1.60},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},
]

write_sounds('tones', bench)
