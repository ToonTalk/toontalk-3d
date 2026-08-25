# naming -- robots that recognise pictures.
#
# A robot's thought is a picture of what it expects, and for a pad that
# comparison includes the IMAGE on its face. So a robot can be trained on the
# red circle and will wake for the red circle and for nothing else -- the same
# dispatch-by-matching that `account` uses on words and `grammar` on numbers,
# with no new machinery at all.
#
# Six robots stand in a team. Pictures land on the nest in front of them; each
# round exactly one of the six has a thought that fits, and it answers with the
# name of what it saw. The team walks through a slideshow naming every frame,
# and nobody wrote a lookup table.
from _img import *                                         # noqa: F403

SEEN = 9701                                     # what arrives
SAID = 9702                                     # what is said about it

newtext = {'type': 'newText'}
settext = lambda t: {'type': 'setText', 'text': t}         # noqa: E731

# The order they are dealt: the top of a pile is its LAST entry, so this list
# is written in the order they will be seen and reversed on the way in.
SHOWN = ['star', 'circle', 'heart', 'square', 'ring', 'triangle', 'star']


def namer(name):
    """One robot: sees its own picture, says its own name.

    It discards the picture it read -- put it down on a work spot and let Dusty
    take it -- because a nest that is never emptied would hand the same picture
    back for ever."""
    return robot(
        name, box({'kind': 'text', 'text': '', 'img': BY_NAME[name]}, ANYBIRD),
        [
            takeTop('given', 0), put('s0'), vac('s0'),     # read it, drop it
            newtext, settext(name), put('given', 1),       # and say what it was
        ],
        trained_on=box(nest(SEEN, 'img-seen'), bird(SAID, 'img-said')))


robots = [namer(n) for n, _ in PICTURES]
team = robots[0]
team['team'] = robots[1:]

work = box(
    nest(SEEN, 'img-seen', 'pictures',
         pile=[pic(n) for n in reversed(SHOWN)]),
    bird(SAID, 'img-said', 'names'))

answers = nest(SAID, 'img-said', 'names')

ABOUT = ('NAMING\n\n'
         'Six robots, one team. Each\n'
         'one\'s thought holds a\n'
         'PICTURE, and a thought that\n'
         'holds a picture matches that\n'
         'picture and no other.\n\n'
         'So the dispatch is the\n'
         'matching. There is no table\n'
         'of names anywhere: each\n'
         'robot knows one shape and\n'
         'says one word.')

RUN = ('TO RUN IT\n\n'
       'Set Rounds to 10 and give\n'
       'the work box to the team\n'
       'leader.\n\n'
       'Seven pictures come off the\n'
       'nest -- star appears twice --\n'
       'and seven names pile up on\n'
       'the answers nest, newest\n'
       'underneath.\n\n'
       'When the pile runs out the\n'
       'team shrinks and dozes,\n'
       'waiting for another picture.')

WHY = ('THEN TRY THIS\n\n'
       'Drop one of the spare\n'
       'pictures on the "pictures"\n'
       'bird: it flies to the nest,\n'
       'the team wakes, and the name\n'
       'arrives. The program is a\n'
       'SERVICE, not a run.\n\n'
       'Now write a word on one of\n'
       'the spares before you send\n'
       'it. Nobody wakes -- a pad\'s\n'
       'words are part of what it is,\n'
       'so a captioned circle is not\n'
       'the circle they know.')

spare_bird = bird(SEEN, 'img-seen', 'pictures')

bench = [
    {'thing': team, 'x': -1.50, 'z': 1.25},
    {'thing': work, 'x': -0.70, 'z': 1.30},
    {'thing': answers, 'x': 0.10, 'z': 1.25},

    {'thing': spare_bird, 'x': -1.35, 'z': 1.72},
    {'thing': pic('star'), 'x': -0.85, 'z': 1.72},
    {'thing': pic('heart'), 'x': -0.40, 'z': 1.72},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.18},
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.18},
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.18},
]

write_images('naming', bench)
