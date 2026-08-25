# pictures -- a picture is a pad.
#
# That is the whole claim, and everything on this table is there to test it.
# The six shapes are pads with an image on the face; two of them also carry
# words, because the words and the picture live on the same pad and a caption
# is not a second thing. They copy, they file, they go in boxes, Dusty takes
# them, and Ctrl+arrows make them bigger -- all of that is pad behaviour that
# nobody had to write again for pictures.
from _img import *                                         # noqa: F403

ABOUT = ('PICTURES\n\n'
         'A picture is a PAD -- the\n'
         'same tablet you write words\n'
         'on, with an image on its\n'
         'face.\n\n'
         'So it copies, files into a\n'
         'notebook, goes in a box,\n'
         'and Dusty takes it away,\n'
         'exactly as a word does.\n'
         'None of that was written\n'
         'again for pictures.')

RUN = ('TO TRY IT\n\n'
       'Drag an image file from\n'
       'your machine onto the page:\n'
       'it lands as a pad WHERE YOU\n'
       'DROPPED IT.\n\n'
       'Drop it on a pad that is\n'
       'already there and the\n'
       'picture covers that pad\n'
       'instead.\n\n'
       'Hold one and press Ctrl and\n'
       'the up arrow to make it\n'
       'bigger; a picture keeps its\n'
       'own proportions.')

WHY = ('WORDS ON A PICTURE\n\n'
       'Two of these say something.\n'
       'Pick one up and type: the\n'
       'words are drawn over the\n'
       'picture, on the one pad.\n\n'
       'Which matters for robots. A\n'
       'thought that holds a picture\n'
       'matches that picture and no\n'
       'other -- see naming.world.\n'
       'The words count too, so a\n'
       'captioned picture and a bare\n'
       'one are different things.')

bench = [
    {'thing': pic('circle'), 'x': -1.50, 'z': 1.15},
    {'thing': pic('square'), 'x': -1.05, 'z': 1.15},
    {'thing': pic('triangle'), 'x': -0.60, 'z': 1.15},
    {'thing': pic('star'), 'x': -0.15, 'z': 1.15},

    {'thing': pic('heart', 'love'), 'x': -1.30, 'z': 1.62},
    {'thing': pic('ring', 'a ring'), 'x': -0.70, 'z': 1.62},
    # an empty box to pour a picture into, and one to keep them in
    {'thing': box(None, None, None), 'x': -0.05, 'z': 1.62},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},
]

write_images('pictures', bench)
