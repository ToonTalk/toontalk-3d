# Generates grammar.world.json -- a sentence factory that READS ITS GRAMMAR
# as data, after the "Sentences" notebook in ToonTalk 3.
#
# The grammar is boxes, not robots. Change the boxes and the language
# changes -- no retraining, no new robots.
#
#   a symbol is either a WORD (a text pad, said as it stands)
#              or a RULE   (a number, looked up and expanded)
#   rule k lives in hole k of the dictionary as [alternatives, die]
#   an alternative is a box of symbols; the die has one face per alternative
#
#   1 sentence     -> noun-phrase verb noun-phrase . | noun-phrase verb .
#   2 noun phrase  -> noun | adjective noun-phrase        (recursive!)
#   3 verb         -> rule | kick | walk
#   4 noun         -> girls | boys | dogs | cats
#   5 adjective    -> big | pink | silly
#
# The work box has six holes:
#   0 the symbols still to say   1 the sentence so far   2 the dictionary
#   3 the bird to send it to     4 the symbol in hand    5 the starting symbol
#
# The team, first thought that matches wins:
#   say it     [hole 4 holds a word]  -- join it onto the sentence
#   expand it  [hole 4 holds a rule]  -- look the rule up by SPLITTING a copy
#              of the dictionary at that number, throw its die to choose an
#              alternative the same way, and join those symbols onto the FRONT
#              of what is still to say
#   send it    [nothing left to say]  -- give the sentence to the bird, then
#              start the next one
#   take one   [otherwise]            -- split the first symbol off the front
#
# Splitting a box on a number is how everything is indexed here, exactly as
# PickOne does it in the original; the empty box is the base case, exactly as
# MakeExamplestop matches it.
import json, io, os

NEST_ID, NEST_GUID = 9301, 'grammar-nest'

num = lambda n: {'kind': 'number', 'value': {'n': str(n), 'd': '1'}, 'op': '+'}
txt = lambda t: {'kind': 'text', 'text': t}
box = lambda *items: {'kind': 'box', 'holes': list(items)}
die = lambda faces: {'kind': 'die', 'faces': faces}

at = lambda *p: {'c': 'given', 'path': list(p)}
spot = lambda i, *p: {'c': 's' + str(i), 'path': list(p)}
take = lambda a: {'type': 'take', 'at': a}
put = lambda a, side=None: ({'type': 'put', 'at': a, 'side': side} if side
                            else {'type': 'put', 'at': a})
copy = lambda a: {'type': 'copy', 'at': a}
vac = lambda a: {'type': 'vacuum', 'at': a}
newnum = {'type': 'newNumber'}
newtext = {'type': 'newText'}
minus1 = {'type': 'setValue', 'value': {'n': '1', 'd': '1'}, 'op': '-'}

WILDN, WILDT = {'kind': 'wildNumber'}, {'kind': 'wildText'}
ANYBOX, ANYBIRD = {'kind': 'anyBox'}, {'kind': 'anyBird'}
EMPTYBOX = {'kind': 'box', 'holes': []}

def cond(todo, head):
    return {'kind': 'box', 'holes': [todo, WILDT, None, ANYBIRD, head, None]}

# --- a word: join it onto the sentence --------------------------------------
say_it = {'kind': 'robot', 'name': 'say it',
          'condition': cond(ANYBOX, WILDT),
          'program': [take(at(4)), put(at(1), 'R')],
          'trainedOn': None, 'team': []}

# --- a rule: look it up, throw its die, and put its symbols in front --------
expand = {'kind': 'robot', 'name': 'expand it',
          'condition': cond(ANYBOX, WILDN),
          'program': [
              # the rule number, less one: where to cut the dictionary
              take(at(4)), put(spot(0)),
              newnum, minus1, put(spot(0)),
              copy(at(2)), put(spot(0)),        # a copy of the dictionary, split there
              take(spot(1, 0)), put(spot(2)),   # rule k is the first of what is left
              vac(spot(0)), vac(spot(1)),
              # throw the rule's own die to choose an alternative
              newnum, put(spot(0)),
              copy(spot(2, 1)), put(spot(0)),   # the die lands on the 1: it re-rolls
              newnum, minus1, put(spot(0)),     # one less: where to cut again
              take(spot(2, 0)), put(spot(0)),   # the alternatives, split there
              take(spot(1, 0)), put(spot(3)),   # the chosen alternative
              vac(spot(0)), vac(spot(1)), vac(spot(2)),
              # its symbols go in front of everything still to say
              take(spot(3)), put(at(0), 'L'),
          ],
          'trainedOn': None, 'team': []}

# --- nothing left to say: send it off and begin again -----------------------
send_it = {'kind': 'robot', 'name': 'send it',
           'condition': cond(EMPTYBOX, None),
           'program': [
               copy(at(1)), put(at(3)),         # the sentence flies to the nest
               vac(at(1)), newtext, put(at(1)), # a clean sheet
               vac(at(0)), copy(at(5)), put(at(0)),
           ],
           'trainedOn': None, 'team': []}

# --- otherwise: split the first symbol off the front ------------------------
take_one = {'kind': 'robot', 'name': 'take one',
            'condition': cond(ANYBOX, None),
            'program': [
                newnum, put(spot(0)),           # a 1 to cut at
                take(at(0)), put(spot(0)),      # the box splits: head here, rest next door
                take(spot(1)), put(at(0)),      # what is left is still to say
                take(spot(0, 0)), put(at(4)),   # the first symbol, in hand
                vac(spot(0)),
            ],
            'trainedOn': None, 'team': []}

scribe = dict(say_it, name='Scribe', team=[expand, send_it, take_one])

WORDS = lambda *ws: [box(txt(w)) for w in ws]
rule = lambda alts: box(box(*alts), die(len(alts)))

dictionary = box(
    rule([box(num(2), num(3), num(2), txt('.')),
          box(num(2), num(3), txt('.'))]),                       # 1 sentence
    rule([box(num(4)), box(num(5), num(2))]),                    # 2 noun phrase
    rule(WORDS(' rule', ' kick', ' walk')),                      # 3 verb
    rule(WORDS(' girls', ' boys', ' dogs', ' cats')),            # 4 noun
    rule(WORDS(' big', ' pink', ' silly')),                      # 5 adjective
)

work = box(
    box(num(1)),                      # still to say: the sentence symbol
    txt(''),                          # the sentence so far
    dictionary,
    {'kind': 'bird', 'nestId': NEST_ID, 'nestGuid': NEST_GUID},
    None,                             # the symbol in hand
    box(num(1)),                      # what to start over with
)

scribe['trainedOn'] = work     # reaching into its thought hands you one

grammar_house = {'kind': 'world', 'v': 1, 'bench': [],
                 'stations': {'stand': work}, 'active': scribe}

world = {'kind': 'world', 'v': 1, 'bench': [
    {'thing': {'kind': 'room', 'label': 'Grammar', 'opaque': False,
               'dirty': False, 'world': grammar_house}, 'x': -0.45, 'z': 1.55},
    {'thing': {'kind': 'nest', 'id': NEST_ID, 'guid': NEST_GUID, 'hasEgg': False,
               'pile': [], 'label': 'sentences'}, 'x': 1.15, 'z': 1.70},
    {'thing': txt('A GRAMMAR, AS DATA\n\nThe robots here know nothing\n'
                  'about nouns or verbs. The\ngrammar is the dictionary\n'
                  'box on the desk inside:\n\n'
                  '  1 sentence → 2 3 2 . | 2 3 .\n'
                  '  2 phrase   → 4 | 5 2\n'
                  '  3 verb     → rule|kick|walk\n'
                  '  4 noun     → girls|boys|...\n'
                  '  5 adjective→ big|pink|silly\n\n'
                  'Rule 2 mentions itself, so\nadjectives can pile up.'),
     'x': -1.05, 'z': 2.15},
    {'thing': txt('TO RUN IT\n\nSet Rounds to 200 and pull\nthe lever. Sentences arrive\n'
                  'on the nest.\n\nA number is a rule: the\nrobot SPLITS a copy of the\n'
                  'dictionary at that number\nto find it, throws the die\n'
                  'kept with it to choose one\nalternative, and joins those\n'
                  'symbols onto the front of\nwhat is still to say.\n\n'
                  'A word it simply joins on.\nAn empty box means the\n'
                  'sentence is finished.'),
     'x': 0.05, 'z': 2.15},
    {'thing': txt('CHANGE THE LANGUAGE\n\nWalk in through the door and\n'
                  'edit the dictionary: type\nnew words on the pads, or\n'
                  'give a rule another\nalternative (and add a face\n'
                  'to its die to match).\n\nNo robot needs retraining —\n'
                  'they only ever read.'),
     'x': 1.15, 'z': 2.15},
], 'stations': {}, 'active': None}

out = os.path.join(os.path.dirname(__file__), 'grammar.world.json')
io.open(out, 'w', encoding='utf-8').write(json.dumps(world, indent=1))
print('wrote', out)
