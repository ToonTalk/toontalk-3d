# album -- a notebook of pictures.
#
# A notebook files things, and a picture is a thing, so a picture album is a
# notebook with pictures on its pages. There is nothing else to it -- which is
# the point. The album is here because it is the shortest proof that pictures
# went in at the bottom: no album kind was added, no picture-viewer was
# written, and the arrow keys turn these pages exactly as they turn pages of
# numbers in any other notebook.
from _img import *                                         # noqa: F403

title = txt('SHAPES\n\nan album\n\nSix pages, six pictures.\n\n'
            'Point at the notebook and\npress the left and right\n'
            'arrow keys, or click the\ngold corner tabs.')

album = {'kind': 'notebook', 'page': 0,
         'label': 'shapes',
         'pages': [title] + [pic(n, n) for n, _ in PICTURES]}

ABOUT = ('AN ALBUM\n\n'
         'A notebook files things. A\n'
         'picture is a thing. So this\n'
         'is a picture album, and no\n'
         'album was ever written.\n\n'
         'Point at it and press the\n'
         'left and right arrow keys\n'
         'to turn the pages; the gold\n'
         'corner tabs do the same.')

RUN = ('TO TRY IT\n\n'
       'Click a picture on a page to\n'
       'lift it off -- it comes out\n'
       'as an ordinary pad, and the\n'
       'page is empty behind it.\n'
       'Drop it back to file it.\n\n'
       'Drop the spare picture on a\n'
       'blank page to add it.\n\n'
       'Click the SPINE and you pick\n'
       'up the album itself rather\n'
       'than what is on its pages.')

WHY = ('AND DUSTY\n\n'
       'Wake Dusty and point him at\n'
       'a page: he flies over and\n'
       'takes that entry away.\n\n'
       'Point him at the SPINE and\n'
       'he takes the whole album,\n'
       'entries and all. Your own\n'
       'notebook is the exception --\n'
       'it stays on the desk, and he\n'
       'says so.')

bench = [
    {'thing': album, 'x': -1.15, 'z': 1.35},
    {'thing': pic('star', 'a spare'), 'x': -0.35, 'z': 1.30},

    {'thing': txt(ABOUT), 'x': -1.45, 'z': 2.15},
    {'thing': txt(RUN), 'x': -0.75, 'z': 2.15},
    {'thing': txt(WHY), 'x': -0.05, 'z': 2.15},
]

write_images('album', bench)
