# Testing "your hand, by word" — instructions for a tester

These are instructions for an agent driving a browser (Claude in Chrome,
Codex, a person) to test the *hand by word* feature of ToonTalk 3D's next
build, with a real language model behind it. The automated suite already
proves the hand's own moves with a stand-in brain; what only a real brain
can test is **whether the brain turns sentences into the right plan**.
That is what this is for.

## Before the tester starts (the person does this, not the agent)

1. Open **https://toontalk.github.io/toontalk-3d/toontalk-3d-next.html**
   in a tab of its own. (Locally: `node serve.js 8311`, then
   `http://localhost:8311/toontalk-3d-next.html`.)
2. Type a name on the "Who is working here?" card and choose **Free play**.
3. Open Marty's card (the green Martian, bottom left, or the Marty button),
   then **How Marty thinks**: choose the provider and **enter the API key
   yourself**. The tester must never type, read, copy or be told an API
   key. Keys live only in this browser's localStorage and go only to the
   provider's own API.
4. ⋮ menu → **☑ 🖐 Move my hand by word**. A line appears at the top centre
   of the screen ("Tell your hand what to do…"). If it does not appear,
   the provider has no key yet.
5. Hand the tab to the tester. To test another provider, come back to
   step 3; the switch stays on.

## What the tester may and may not do

- Type sentences into the **top line** (press Enter) and read what comes
  back. The **▾** at the right end of the line shows a log of every
  sentence and answer; scroll it for older ones.
- Read the line under the table (the workshop's own messages) and Marty's
  log if a sentence was typed to him.
- Take screenshots after each sentence.
- Do **not** touch Settings → How Marty thinks, the key box, or the
  provider selector. Do not type into any field marked as a key.
- Do not use the microphone (voice is tested by a person); everything
  here is typed.
- Between sections, reload the tab with `?fresh` added to the address
  (`toontalk-3d-next.html?fresh`) so each section begins with a clean
  table; the name and the switch are remembered. (The title card's
  *Start this world over* is for a loaded world, not a clean table.)

## How to read a result

Every sentence produces one of:

- **✓ line** — the plan ran to the end. Then check the table against the
  expected outcome below; a ✓ with the wrong thing on the table is a
  **brain error** (wrong plan).
- **✗ Step N (verb …) did not work: reason — K steps before it did.** —
  the hand refused a step and stopped. Read the reason. If the sentence
  was reasonable and the reason names something the hand should have
  understood, it is a **hand error**; if the brain asked for something
  that is not there ("thing 7" when there are three things), it is a
  **brain error**.
- **✗ The brain found nothing for the hand to do** / a plain refusal in
  words — the brain declined; note whether it should have.

Record, for every sentence: the sentence, ✓/✗, the reported line, what
is actually on the table afterwards, and your verdict (correct / brain
error / hand error / unclear). Screenshots help most for brain errors.

## The sentences, in order

Type each exactly, one at a time, and wait for ✓/✗ before the next.

### Section A — fresh things (reload with `?fresh` first)

| # | Sentence | Expected on the table afterwards |
|---|---|---|
| A1 | `put a box on the table` | a box with 2 holes |
| A2 | `pick up a 1 and put it in a 3-hole box` | a second box, 3 holes, a 1 in its left hole; the first box untouched |
| A3 | `create a text pad with ToonTalk on it` | a pad saying ToonTalk |
| A4 | `make a 12` | a number 12 (a fresh 1 typed 12 — not 112) |
| A5 | `put a -5 on the table` | a number −5 |
| A6 | `give a robot a scale with 1 and 100 on it` | a robot at the bench with a scale on its desk, 1 in the left pan, 100 in the right; the line says you are inside its thought bubble |
| A7 | `leave` | back at the table; the scale still on the desk |

### Section B — "a" and "the" (reload with `?fresh`, then A1 first)

The brain, not a rule, decides whether a sentence means a fresh thing or
one already on the table. With one 2-hole box on the table:

| # | Sentence | Expected |
|---|---|---|
| B1 | `put a 1 in the box` | a fresh 1 in the existing box's left hole (no second box) |
| B2 | `put a 3 in the box` | a 3 in its right hole |
| B3 | `pick up the box and put it down again` | the same box, still one box, still holding 1 and 3 |
| B4 | `put the 3 on the 1` | the 1 becomes 4 (the 3 is consumed); the right hole empty |
| B5 | `take a 1 and add it to the 4` | 5 in the left hole |

### Section C — Mimi and Dusty (reload with `?fresh` first)

| # | Sentence | Expected |
|---|---|---|
| C1 | `make a 7` | a 7 on the table |
| C2 | `copy the 7` | a 7 on the table (the copy) and the original 7 on Mimi's platform |
| C3 | `take the original back` | two 7s on the table, the platform empty |
| C4 | `vacuum one of the 7s` | one 7 left; Dusty asleep again |
| C5 | `give the 7 to Mimi` | the 7 on the platform, a copy in the hand or on the table (either is fine — note which) |

### Section D — robots (reload with `?fresh` first)

| # | Sentence | Expected |
|---|---|---|
| D1 | `put a robot on the table` | a mini robot on the table |
| D2 | `give it a 1` | the robot at the bench with the 1 on its desk; the line says you are inside its thought bubble |
| D3 | `add a 1 to the number on the desk` | the desk shows 2 (this is a lesson: the robot is learning) |
| D4 | `leave` | back at the table; the desk shows 1 again (leaving rewinds the daydream; the robot keeps the lesson) |
| D5 | `run the robot` | the desk shows 2 (it did what it learned, once — its condition was a 1) |
| D6 | `put another robot on the table` then `give it a 5` | with two robots on the table the hand should ask which — unless the brain names one; either way note what happened |

### Section E — inside a thought bubble (reload with `?fresh`, then D1, D2)

| # | Sentence | Expected |
|---|---|---|
| E1 | `copy it` | the 1 goes from the desk to Mimi's platform, and the copy is set on one of the robot's little spots |
| E2 | `put a 2 in a box` | a box with 2 holes and a 2 in it, on a spot |
| E3 | `take a robot` | refused: a robot cannot make robots inside its thought |
| E4 | `leave` | refused while the claw holds something; empty the claw first (`put it down`), then `leave` works and the world rewinds |

### Section F — refusals and edge cases (reload with `?fresh` first)

| # | Sentence | Expected |
|---|---|---|
| F1 | `drop it on the table` | refused: nothing in the hand |
| F2 | `put a 1 in the box` (no box on the table) | the brain should either fetch a box first (✓, a box with a 1) or say there is no box — both are acceptable; note which |
| F3 | `vacuum the robot` (no robot) | a refusal naming the missing thing |
| F4 | `what is a nest?` | the hand should decline politely — it only moves things. (Marty answers questions; this line does not.) |
| F5 | `put a bird on the table` | a nest with its bird (birds come with nests); note what the brain fetched |

### Section G — the same sentence said to Marty

With the switch on, a sentence typed into **Marty's** box that tells him
to move something should be handed to the hand: he says "Your hand is on
it" (or similar) and the thing moves. Type into Marty's box:

| # | Sentence | Expected |
|---|---|---|
| G1 | `put a box on the table` | Marty's short line, and a box on the table |
| G2 | `what does Dusty do?` | an ordinary Marty answer, nothing moves |

Then ⋮ → untick **Move my hand by word**, and again to Marty:

| G3 | `put a box on the table` | Marty says he cannot move your hand and names the switch; nothing moves |

## What to report

A short report with:

1. Provider and model tested (as shown on Marty's card; never the key).
2. The table of sentences with ✓/✗, the reported line, and the verdict.
3. For each **brain error**: the sentence, the listing the brain had (the
   log shows what was on the table), and what plan would have been right.
4. For each **hand error**: the sentence and the refusal reason.
5. Anything that did not fit these categories: the hand claiming a move
   that did not happen (the worst kind — look for it), a plan that ran
   but left the workshop in a strange state, a line that never came back.
6. Rough timing: seconds from Enter to the first move, per provider.

## Known limits (not bugs)

- Naming things by word (a nest called "orders") is not done yet.
- Ruby (erasing parts of a thought) and Dusty on parts of a thought are
  not reachable by word.
- Going through a panel door, the yard, and the notebook are not
  reachable by word.
- Inside a thought bubble the stacks give the robot's own things (no
  robots), things go on the robot's spots, and leaving rewinds the
  table — that is how ToonTalk lessons work.
