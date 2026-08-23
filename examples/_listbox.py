# A team that reads a lazy list and builds the same thing as a flat box, so
# both forms of an answer can be looked at side by side.
#
# A list here is the pair [first, the rest], and "the rest" is usually a NEST --
# an answer that has not arrived yet. That is what makes it lazy, and it is also
# what makes it hard to READ: [1,[2,[3,[]]]] on the table is a box holding a
# nest holding a box holding a nest, three deep, and you cannot see the shape
# of it at a glance. A box with three holes you can.
#
#   Link   [list-nest, box so far, bird]   the nest's top is a TWO-hole box
#          takes the link off, puts a one-hole box holding its first onto the
#          end of the box so far, and hangs the link's REST in hole 0 --
#          so the next round watches the next nest along.
#   End    [list-nest, box so far, bird]   the nest's top is a box with NO holes
#          the empty list: hands the finished box to the bird and sweeps its
#          own box away, which ends the team for good.
#
# The team tries its leader first, so the finisher leads: a two-hole box and a
# no-hole box are told apart by their shape alone, and the worker would happily
# take either.
#
# It runs ALONGSIDE the program it is watching rather than after it. Its nest is
# a twin of the answer nest -- same name, so every bird delivers to both -- and
# a copied nest joins the original's delivery group, so the copy of each link
# carries a copy of the next nest and the chain follows itself. The original is
# never touched: both forms fill at once, link by link.

at = lambda c, *p: {'c': c, 'path': list(p)}
top = lambda c, *p: {'c': c, 'path': list(p), 'nest': True}
take = lambda a: {'type': 'take', 'at': a}
put = lambda a, side=None: (dict({'type': 'put', 'at': a}, side=side)
                            if side else {'type': 'put', 'at': a})
vac = lambda a: {'type': 'vacuum', 'at': a}
holes = lambda n: {'type': 'setHoles', 'n': n}
NEWBOX = {'type': 'newBox'}

WILD = {'kind': 'wild'}
ANYBOX = {'kind': 'anyBox'}
ANYBIRD = {'kind': 'anyBird'}
box = lambda *hs: {'kind': 'box', 'holes': list(hs)}


def list_to_box_team(name='List to Box'):
    """The team itself. Give it [a nest carrying a list, an empty box, a bird]."""
    end = {
        'kind': 'robot', 'name': name,
        # hole 0's nest shows the EMPTY list: a box with no holes at all
        'condition': box(box(), ANYBOX, ANYBIRD),
        'program': [
            take(at('given', 1)),          # the box that has been filling up
            put(at('given', 2)),           # off to the bird
            vac(at('given')),              # and its own box: finished, for good
        ],
        'trainedOn': None, 'team': [],
    }
    link = {
        'kind': 'robot', 'name': 'Link',
        # ... and here it shows a link: [something, the rest]
        'condition': box(box(WILD, WILD), ANYBOX, ANYBIRD),
        'program': [
            take(top('given', 0)),         # the link, off the top of the pile
            put(at('s0')),
            NEWBOX, holes(1), put(at('s1')),
            take(at('s0', 0)), put(at('s1', 0)),      # its first, in a box of one
            take(at('s1')), put(at('given', 1), 'R'),  # joined on at the END
            vac(at('given', 0)),           # the nest just read is spent
            take(at('s0', 1)), put(at('given', 0)),   # the REST takes its place
            vac(at('s0')),                 # the emptied link
        ],
        'trainedOn': None, 'team': [],
    }
    end['team'] = [link]
    return end


def list_to_box_room(nest_id, nest_guid, out_id, out_guid, label='List to Box'):
    """The team, its box and a room to stand in -- ready to be put on a bench.

    The nest here is a TWIN of the one the program answers on: same guid, so a
    bird delivers to both at once and neither takes anything from the other.
    """
    return {
        'kind': 'room', 'label': label, 'opaque': False, 'dirty': True,
        'world': {
            'kind': 'world', 'v': 3, 'bench': [],
            'stations': {'stand': box(
                {'kind': 'nest', 'id': nest_id, 'guid': nest_guid,
                 'hasEgg': False, 'pile': [], 'label': 'the list'},
                box(),                                     # the box, still empty
                {'kind': 'bird', 'nestId': out_id, 'nestGuid': out_guid,
                 'label': 'as a box'},
            )},
            'active': list_to_box_team(),
        },
    }
