# Generates account.world.json -- Sally's account, after the ToonTalk 3
# "divisiontester" notebook: an object that answers messages by NAME.
#
# The account is a three-hole box with labelled holes:
#
#     [ Request: ...,   Balance: 100,   Owner: "Sally" ]
#
# A request is a box whose FIRST hole is a word saying what to do:
#
#     [ "deposit",  50 ]      put 50 in
#     [ "withdraw", 30 ]      take 30 out
#     [ "query",    a bird ]  tell me the balance
#
# Drop a request into the Request hole and the robot whose thought matches
# that word does the work and vacuums the request away, leaving the hole
# empty for the next one. Nothing else is needed: the dispatch IS the
# pattern matching, exactly as in the original.
#
#   Deposit  sees [["deposit", any number], any number, "Sally"]
#            take the amount, drop it on the balance, sweep the request away
#   Withdraw sees [["withdraw", any number], any number, "Sally"]
#            the same, but the amount is negated on the way -- a robot types
#            the minus sign, as you would
#   Query    sees [["query", a bird], any number, "Sally"]
#            copy the balance, hand the copy to the bird, sweep up
#
# The Owner pad is part of every thought, so these robots serve Sally's
# account and no one else's. Write a different name on the pad and they all
# stop recognising it -- which is the point of putting it there.
import json, io, os

REP_ID, REP_GUID = 9401, 'account-reply-nest'
START = 100

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
box = lambda *holes: {'kind': 'box', 'holes': list(holes)}
at = lambda *p: {'c': 'given', 'path': list(p)}
take = lambda *p: {'type': 'take', 'at': at(*p)}
put = lambda *p: {'type': 'put', 'at': at(*p)}
copy = lambda *p: {'type': 'copy', 'at': at(*p)}
vac = lambda *p: {'type': 'vacuum', 'at': at(*p)}

WILD, ANYBIRD = {'kind': 'wildNumber'}, {'kind': 'anyBird'}
OWNER = 'Sally'

def account_cond(request):
    """[Request, Balance, Owner] -- the owner's name is part of the thought."""
    return {'kind': 'box', 'holes': [request, WILD, {'kind': 'text', 'text': OWNER}]}

def robot(name, word, second, program):
    return {'kind': 'robot', 'name': name,
            'condition': account_cond({'kind': 'box',
                                       'holes': [{'kind': 'text', 'text': word}, second]}),
            'program': program, 'trainedOn': None, 'team': []}

deposit = robot('deposit', 'deposit', WILD, [
    take(0, 1), put(1),          # the amount joins the balance
    vac(0),                      # the served request is swept away
])

# A withdrawal is a deposit of the opposite. The original types a minus sign
# on the amount in hand; here the robot turns it round by dropping a "times
# -1" on it, which works whatever the amount turns out to be.
spot = lambda i=0: {'c': 's' + str(i), 'path': []}
withdraw = robot('withdraw', 'withdraw', WILD, [
    take(0, 1), {'type': 'put', 'at': spot()},        # the amount, on a work spot
    {'type': 'newNumber'},
    {'type': 'setValue', 'value': {'n': '-1', 'd': '1'}, 'op': '*'},
    {'type': 'put', 'at': spot()},                    # times -1: now it is a debt
    {'type': 'take', 'at': spot()},
    put(1),                                           # and that joins the balance
    vac(0),
])

query = robot('query', 'query', ANYBIRD, [
    copy(1), put(0, 1),          # a copy of the balance, into the bird's wings
    vac(0),
])

teller = dict(deposit, name='Teller', team=[withdraw, query])

account = box(None, num(START), txt(OWNER))
teller['trainedOn'] = box(box(txt('deposit'), num(50)), num(START), txt(OWNER))

reply_bird = {'kind': 'bird', 'nestId': REP_ID, 'nestGuid': REP_GUID}

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': account, 'x': -0.10, 'z': 1.55},
    {'thing': teller, 'x': -1.15, 'z': 1.30},
    {'thing': box(txt('deposit'), num(50)), 'x': -1.20, 'z': 2.15},
    {'thing': box(txt('withdraw'), num(30)), 'x': -0.55, 'z': 2.15},
    {'thing': box(txt('query'), reply_bird), 'x': 0.10, 'z': 2.15},
    {'thing': {'kind': 'nest', 'id': REP_ID, 'guid': REP_GUID, 'hasEgg': False,
               'pile': [], 'label': 'answers'}, 'x': 1.20, 'z': 1.70},
    {'thing': txt('SALLY\'S ACCOUNT\n\nThe box is\n\n [ Request, Balance,\n   Owner ]\n\n'
                  'and a request is a box\nthat says what to do:\n\n'
                  ' [ "deposit",  50 ]\n [ "withdraw", 30 ]\n [ "query", a bird ]'),
     'x': 0.75, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\nGive the account box to the\nTeller, then drop a request\n'
                  'into its first hole. The\nrobot whose thought matches\n'
                  'that word does the work and\nsweeps the request away.\n\n'
                  'The query one answers on the\nnest marked "answers".\n\n'
                  'The Owner pad is in every\nthought, so they serve\n'
                  'Sally\'s account and no\nother. Rewrite the name and\n'
                  'they all stop knowing it.'),
     'x': 1.35, 'z': 2.15},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'account.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
