# games

Worlds that are games, built from the workshop's ordinary parts and made to
be read as well as played.

## space-invaders.world.json

Eight invaders, a ship, a dark field and a score. Point at the field and
press SPACE; the left and right arrows move the ship, the up arrow fires.

Every picture is a pad with its behaviours on its BACK as cards whose faces
are sentences -- "I explode when a bullet hits me: a bang, and I vanish." --
the way the original ToonTalk's Space Behaviours laid its anima-gadgets out.
Point at an invader and press the gear: its panel comes out with the cards
on it; Enter looks straight down at it. Point at a card there and press the
gear again: the card's own panel, its robot and the box it works on. The
knob folds each one home.

What it is made of: the touch reading's name hole (the invader's card is
trained on "bullet"), `[drop | bullet | [0 | -1/3]]` for firing a working
copy, `[vanish]`, the keyboard nest, a speed, and the field's own
`[listen | touches | bird]` for the referee that keeps the score.

Regenerate with `python make_space_invaders.py`.
