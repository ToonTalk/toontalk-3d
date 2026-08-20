# Examples

Saved worlds. Load one with the **Import file** button (or drag the file onto
the page). Each world lays two text pads on the table — what the program is,
and how to run it — so the instructions arrive with the program. They are
ordinary pads: vacuum them away with Dusty once you know the drill.

## sentence-generator.world.json

A random-sentence factory — the first program to use the recursion-era pieces
(dice, robot teams branching on a roll, a room working while you do something
else).

A glass room called **Scriptorium** holds a team of twenty robots and their
state box; a nest sits outside on the table. Pull the big lever on the room's
right wall and sentences start arriving on the nest, one text pad each:

> the frog dreams of the witch.
> the cat chases the robot.

**How it works.** The state box holds a phase number, a die-roll slot, the
sentence under construction, two dictionary boxes (six nouns, six verbs), a
bird, and the pads "the" and ".". Each round exactly one team member's
thought matches the box:

- **Scribe** (phase 0) copies "the" into the sentence, throws a die onto the
  roll slot, and advances the phase.
- **noun1-1 … noun1-6** each match one roll and copy their noun onto the
  sentence's right edge, then roll again.
- **verb-1 … verb-6** append their verb (each ends with "the"), roll again.
- **noun2-1 … noun2-6** append the second noun.
- **post** appends ".", hands the finished sentence to the bird — who flies
  it out of the room to the nest — and resets the phase, so the whole team
  starts over.

Five rounds per sentence; the Rounds control decides how many the room makes
per pull of the lever. Open the door to walk in and watch, or click the roof
to make the walls opaque and let it work in private — the chimney smokes
while it's busy.

Regenerate the file with `python make_sentence_generator.py`.

## fibonacci.world.json

Doubly-recursive Fibonacci — the recursion stress test. fib(n) is computed
as the number of leaves of the call tree, so no reply channels are needed:
every leaf mails a **1** to one shared nest, and their sum is the answer.

The work box holds `[n, bird, spare-robot, empty, empty]`. Hand it to the
**Fib** robot:

- **leaf-1** and **leaf-2** (matching an exact 1 or 2) mail a 1 to the bird
  and empty the number hole, which stops the team.
- **branch** (matching any other number) drops a "−1" pad on n, carries the
  whole box to Mimi and takes the copy; does it again for n−2; then builds
  two rooms, installs a copy of the spare robot in each, drops one copied
  box into each, and stows both rooms in its own box's last two holes.

The box comes back to the table carrying two smoking rooms — the two
recursive calls — and each room's robot does exactly the same thing one
level down. For n = 8 that grows 40 rooms nested 6 deep, and 21 ones land
on the nest. When the smoke stops, hand the `[0, nest]` box to **Sum**: it
moves the pile onto the total one a round (dozing whenever the nest is
bare) and the total reads **21**.

Regenerate with `python make_fibonacci.py` (edit `N` for other inputs;
keep the room-nesting depth n−2 within the engine's cap of 12).

## fibonacci-recursive.world.json

The same function written the way the definition reads, with answers coming
back rather than leaves being counted:

> to fib n: n is 1 → answer 1; n is 2 → answer 1;
> otherwise → ask fib(n−1) and fib(n−2), then answer their sum.

"Answer" means *give the number to the bird you were handed*. The work box is
`[n, bird, spare team, nestA, nestB, houseA, houseB]`. The recursive robot
makes a fresh nest for each child — the egg hatches on its work spot, and that
bird travels with the child — builds a house for each, and then simply
**dozes**: a robot facing a bare nest waits, so no waiting machinery is
needed. When both nests hold a number, the adder robot takes them, drops one
on the other, and answers.

This is the faithful one, and since worlds became live (see `DIVERGENCE.md`)
it is also fast: `fib(7)` answers in under a second, and `fib(10) = 55` —
109 houses nested eight deep — in about three. Edit `N` in the generator to
push it further.

Regenerate with `python make_fibonacci_recursive.py`.

## bank-account.world.json

A bank account as a message-passing object, **sealed inside a house**. The
account box sits on the Teller's desk in there, so nothing on the table can
reach the balance: the only way in is to send a request to the bird marked
*requests*. That is encapsulation you can walk around and look at.

A request is a box `[amount, a bird to reply to]` — negative takes money out.
Drop one on the requests bird and she flies it into the house, onto the nest
in the account box. The Teller wakes and his team decides **with a scale
rather than a counter**:

- **take one** — the nest holds a request: lift it off, fetch a scale, and
  weigh what the balance *would* be (a copy of the balance with the amount
  added) against nothing at all.
- **Teller / ok too** — the scale tips left or sits level, so the sum is zero
  or better: bank the amount and send the new balance home with the request's
  own bird.
- **sorry** — the scale tips right: copy the *not enough money* slip and send
  that instead. The balance is not touched.

Each verdict robot carries a **tilted scale in its thought bubble**, and a
thought only matches a scale leaning the same way — so the weighing is the
decision, and the tilt is what is tested. With no scale on the desk only
*take one* can match, and with one there only the three verdicts can, so the
team walks through weigh-then-decide without any step counter: the scale
itself is the state. Walk in through the door and you can watch the four of
them hand the floor to one another, one robot per round.

Try the −500 request. Withdrawing *exactly* the balance is allowed (the scale
balances), which is the boundary worth checking by hand.

Regenerate with `python make_bank_account.py`.


## grammar.world.json

The sentence factory again, but this time **the robots do not know the
grammar — they read it**. Modelled on the *Sentences* notebook in ToonTalk 3.

Inside the house, the work box holds `[still to say, the sentence so far, the
dictionary, a bird, the symbol in hand, what to start over with]`. A symbol is
either a **word** (a text pad, said as it stands) or a **rule** (a number,
looked up and expanded). Rule *k* lives in hole *k* of the dictionary as
`[alternatives, die]` — the die has one face per alternative:

```
1 sentence    -> noun-phrase verb noun-phrase . | noun-phrase verb .
2 noun phrase -> noun | adjective noun-phrase        (mentions itself!)
3 verb        -> rule | kick | walk
4 noun        -> girls | boys | dogs | cats
5 adjective   -> big | pink | silly
```

Four robots run the whole language:

- **take one** splits the first symbol off the front of what is still to say.
- **say it** (the symbol in hand is a word) joins it onto the sentence.
- **expand it** (a number) splits a *copy* of the dictionary at that number to
  find the rule, throws the die kept with it, splits the alternatives at the
  roll to choose one, and joins its symbols onto the **front** of what is
  still to say.
- **send it** (nothing left to say — an empty box) gives the sentence to the
  bird and starts the next one.

Splitting a box on a number is how everything is indexed here, exactly as
*PickOne* does it in the original, and the empty box is the base case exactly
as *MakeExamplestop* matches it. Because rule 2 mentions itself, adjectives
pile up as deep as the dice allow: *"pink silly big big boys kick silly silly
dogs."*

Set Rounds to 200 and pull the lever. Then walk in through the door and edit
the dictionary — type new words on the pads, or give a rule another
alternative and add a face to its die. The language changes; no robot is
retrained, because none of them ever knew the language.

Regenerate with `python make_grammar.py`.

## account.world.json

Sally's account — an object that answers messages **by name**, after the
ToonTalk 3 notebook of the same shape. Where `bank-account` is a server
behind a door, this one sits open on the table and shows the idiom bare.

The account is a three-hole box: `[Request, Balance, Owner]`, and a request
is a box whose first hole is a *word* saying what to do:

```
[ "deposit",  50 ]      put 50 in
[ "withdraw", 30 ]      take 30 out
[ "query",  a bird ]    tell me the balance
```

Give the account box to the Teller, then drop a request into its first hole.
The robot whose thought carries that word does the work and vacuums the
request away, leaving the hole empty for the next one — **the dispatch is the
pattern matching**, nothing more. Deposit drops the amount on the balance;
withdraw does the same but types a minus sign on the amount first, exactly as
the original does — typing only an operation is remembered as *"make it
subtract"*, so the robot takes away whatever amount it is handed, not the 30
it was taught on; query copies the balance and hands the copy to the bird that
came with the request, which flies it to the nest marked *answers*.

The three robots are a **team**, and you can watch them take turns: the Teller
stands at the desk and *withdraw* and *query* wait in line behind him, each
with its own small thought over its head. Drop in a withdrawal and *withdraw*
walks up, does the work, and steps back.

The Owner pad is part of every thought, so these robots serve Sally's account
and nobody else's. Rewrite the name on the pad and they all stop recognising
it — which is the point of putting it there.

Regenerate with `python make_account.py`.
