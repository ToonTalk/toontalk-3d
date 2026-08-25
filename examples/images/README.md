# Images

Three worlds. Load one with **Import file** (or drag the file onto the page).
Each lays its instructions on the table as ordinary pads.

**A picture is a pad.** Not a new kind of thing: the same tablet you write
words on, with an image on its face. So a picture copies, files into a
notebook, goes in a box, joins other pads, is vacuumed by Dusty, and is
recognised by a robot's thought — all of it behaviour that already existed and
that nobody wrote again for pictures. Words and image can share the one pad, and
a pad can carry other pads riding on it.

Drag an image file onto the page and it lands as a pad **where you dropped
it**; drop it on a pad that is already there and the picture covers that pad
instead.

**Captions are labels, not a caption feature.** Where a picture here carries a
word, that word is a second pad *riding* on the picture: grey paper, white
writing, wide and short, made with the appearance API and nothing else —

```
[set | background | #3a3f47]   [set | colour | white]
[set | font       | sans]      [set | height | 0.26]
```

sent to the pad's own bird. So a robot can build one, Dusty can take the label
off without taking the picture, and you can pick the label up and read it on
its own. `label()` in `_img.py` is the same four properties as data.

## pictures.world.json

The vocabulary, with nothing running: six shapes, two of them captioned, and an
empty box to put them in. Hold one and press **Ctrl** with the up arrow to make
it bigger — a picture keeps its own proportions rather than being squeezed into
the tablet's.

Regenerate with `python make_pictures.py`.

## naming.world.json

Six robots in a team, each one's thought holding a **picture**. A thought that
holds a pad matches that pad's words *and* its image, so a robot trained on the
red circle wakes for the red circle and for nothing else.

Pictures land on a nest; each round exactly one of the six fits; it discards
what it read and answers with the name of what it saw. Set Rounds to 10 and
give the work box to the leader: seven pictures go in, seven names come out.
**The dispatch is the matching** — there is no table of names anywhere, the
same way `account` dispatches on words and `grammar` on numbers.

Then drop one of the spare pictures on the *pictures* bird: she flies it to the
nest, the team wakes, and a name arrives. The program is a service, not a run.
Now write a word on a spare before you send it, and nobody wakes — a pad's
words are part of what it is, so a captioned circle is not the circle they
know.

Regenerate with `python make_naming.py`.

## album.world.json

A notebook files things; a picture is a thing; so this is a picture album, and
no album was ever written. Point at it and press the left and right arrow keys
to turn the pages, or click the gold corner tabs. Click a picture to lift it
off the page as an ordinary pad; click the **spine** and you pick up the album
itself instead of what is on its pages — and that is also the grip Dusty
accepts on a full notebook.

Regenerate with `python make_album.py`.

## Writing another one

`_img.py` carries the six pictures and a **PNG writer** — about forty lines of
`zlib` and `struct` — so regenerating these needs no drawing library. A shape
is a function of `(u, v)` over `[-1, 1]`, sampled 3×3 a pixel so the edges are
not a staircase; each finished picture is a data URL of one or two kilobytes.
`pic(name, caption)` makes a pad out of one.

A world file carries every picture inline, which is why these are 128 pixels
square and flat-coloured. A photograph would work exactly the same way and make
a much bigger file.
