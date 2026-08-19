# Generates bank-account.world.json -- message-passing account, ToonTalk style.
#
# The account is a box [balance, request-nest] worked by the Teller. A request
# is a box [amount, reply-bird]: drop one on the request bird and she files it
# on the teller's nest. The dozing Teller wakes, moves the amount onto the
# balance (a negative amount is a withdrawal), sends a COPY of the new balance
# back with the request's own bird, vacuums the emptied request away, and
# dozes again. The reply nest piles up a history of balances.
#
# Copy a request box on Mimi for more requests -- a copied bird serves the
# same reply nest.
import json, io, os

REQ_GUID, REQ_ID = 'bank-request-nest', 9201
REP_GUID, REP_ID = 'bank-reply-nest', 9202

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
at = lambda c, *p: {'c': c, 'path': list(p)}
copy = lambda c, *p: {'type': 'copy', 'at': at(c, *p)}
put = lambda c, *p: {'type': 'put', 'at': at(c, *p)}
vac = lambda c, *p: {'type': 'vacuum', 'at': at(c, *p)}

teller = {'kind': 'robot', 'name': 'Teller',
    'condition': {'kind': 'box', 'holes': [
        {'kind': 'wildNumber'},
        {'kind': 'box', 'holes': [{'kind': 'wildNumber'}, {'kind': 'anyBird'}]},
    ]},
    'program': [
        {'type': 'take', 'at': {'c': 'given', 'path': [1], 'nest': True}},
        put('s0'),                     # the request, parked
        {'type': 'take', 'at': at('s0', 0)},
        put('given', 0),               # amount joins the balance
        copy('given', 0),              # a copy of the new balance...
        put('s0', 1),                  # ...flies home with the request's bird
        vac('s0'),                     # the emptied request is swept away
    ],
    'trainedOn': None, 'team': []}

reply_bird = lambda: {'kind': 'bird', 'nestId': REP_ID, 'nestGuid': REP_GUID}

account = {'kind': 'box', 'holes': [
    num(100),
    {'kind': 'nest', 'id': REQ_ID, 'guid': REQ_GUID, 'hasEgg': False, 'pile': []},
]}

request = lambda amount: {'kind': 'box', 'holes': [num(amount), reply_bird()]}

txt = lambda t: {'kind': 'text', 'text': t}

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': account, 'x': -0.05, 'z': 1.50},
    {'thing': teller, 'x': -1.15, 'z': 1.30},
    {'thing': {'kind': 'bird', 'nestId': REQ_ID, 'nestGuid': REQ_GUID,
               'label': 'requests'}, 'x': 0.70, 'z': 1.55},
    {'thing': {'kind': 'nest', 'id': REP_ID, 'guid': REP_GUID, 'hasEgg': False,
               'pile': [], 'label': 'statements'}, 'x': 1.25, 'z': 1.80},
    {'thing': request(50), 'x': -1.15, 'z': 2.15},
    {'thing': request(-30), 'x': -0.55, 'z': 2.15},
    {'thing': txt('THE BANK ACCOUNT\n\nThe box holds the balance\n'
                  'and a nest for requests.\nA request is a box: an\n'
                  'amount and a bird to reply\nto. Negative means\ntake money out.'),
     'x': 0.35, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\n1. Give the [100, nest] box\n   to the Teller. He dozes:\n'
                  '   the nest is empty.\n'
                  '2. Drop a request on the\n   bird marked "requests".\n'
                  '3. He wakes, banks it, and\n   sends the new balance to\n'
                  '   the statements nest.\n\n'
                  'Copy a request on Mimi for\nmore of them.'),
     'x': 1.15, 'z': 2.15},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'bank-account.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
