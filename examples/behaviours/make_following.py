# following -- move with the pointer.
#
# The pointer device delivers [across | away]. A thing's bird takes
# [set | position | [across | away]]. The box the device gives is EXACTLY the
# box the message wants, so the robot's whole job is to put one inside the
# other and hand it over:
#
#     copy the template   [set | position | _ ]
#     take the reading    [across | away]
#     put it in the hole  [set | position | [across | away]]
#     give it to the bird on the perch
#
# Four steps, and none of them is about pointers. Two vocabularies that were
# designed a week apart happen to fit, which is the test of whether they were
# designed as data or as features.
from _beh import *                                          # noqa: F403

STAR = 'L9521'
POINT = 9522

star = live(pad('*', bg='#2b1b33', ink='#7ee787', font='sans'), STAR)
template = box(txt('set'), txt('position'), None)            # noqa: F405

follower = robot(
    'Follower', box(ANYBOX, ANYBOX),
    [
        copy('given', 1), put('s0'),         # a template to fill in
        takeTop('given', 0), put('s0', 2),   # the reading, into its empty hole
        take('s0'), put('perch'),            # and away to my thing, by the bird on the perch
    ],
    trained_on=box(device(POINT, DEV_POINT, 'pointer'), template),
    note='Copies the [set | position | _] template, takes the pointer’s '
         '[across | away] off the nest, puts it in the empty hole, and gives the '
         'message to the bird on the perch. Nothing in it is about pointers: it dozes until '
         'a reading arrives.')

work = box(device(POINT, DEV_POINT, 'pointer'), template)

ABOUT = ('FOLLOWING\n\n'
         'The pointer device delivers\n'
         '[across | away].\n\n'
         'A thing\'s bird takes\n'
         '[set | position | [x | z]].\n\n'
         'The box the device gives is\n'
         'exactly the box the message\n'
         'wants, so the robot only has\n'
         'to put one inside the other.')

RUN = ('TO RUN IT\n\n'
       'Press SPACE on the star, then\n'
       'move the pointer over the\n'
       'table: it follows your hand.\n'
       '"." stops it.\n\n'
       'THE ROBOT IS ON ITS BACK.\nHold the star and press\nCtrl+P (or the gear on the\nholding card) to go through\nits door and watch the\nrobot at work. Escape\ncomes back out.\n\n'
       'It dozes between moves: with\n'
       'nothing on the pointer nest\n'
       'there is nothing to match.')

WHY = ('THE TEST OF A DESIGN\n\n'
       'Nothing in these four steps\n'
       'is about pointers, and\n'
       'nothing is about position.\n'
       'The robot copies a box, moves\n'
       'a thing into a hole, and\n'
       'gives it to the bird on the\n'
       'perch -- three gestures it\n'
       'could already do.\n\n'
       'The device and the message\n'
       'were designed a week apart\n'
       'and fit because both are\n'
       'DATA and neither is a\n'
       'feature.')

# PACKAGED (Ken, 19 Sep): the Follower and its box on the star's own panel.
bench = [
    {'thing': gadget('*', STAR, follower, work, look=dict(bg='#2b1b33', ink='#7ee787', font='sans')), 'x': -1.30, 'z': 1.40},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},           # noqa: F405
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},             # noqa: F405
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},             # noqa: F405
]

write_beh('🐾 following', bench)
