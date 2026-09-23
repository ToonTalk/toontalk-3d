# Testing "your hand, by word" — instructions for a tester

These are instructions for an agent driving a browser (Claude in Chrome,
Codex, a person) to test the *hand by word* feature of ToonTalk 3D's next
build, with a real language model behind it. The automated suite already
proves the hand's own moves with a stand-in brain; what only a real brain
can test is **whether the brain turns sentences into the right plan**.
That is what this is for.

**This version is for the Gemini Nano rerun** (23 September). The first
Nano run got 1 sentence in 25 right; the hand has changed since (below),
and the question now is how far those changes carry a small on-device
model. The same instructions work for any provider.

## What changed since the first Nano run

- **The hand forgives wording.** `pickup boxes` (a stack's name) is read as
  taking a fresh one; `take` with `what` is read as `take from`; a kind's
  name ("box", "number", "robot") means the only thing of that kind in the
  listing — or a fresh one if there is none; `#3` means thing 3. A take
  with no stack now names the stacks.
- **Failed plans no longer go into the brain's history.** Only plans that
  worked are kept as context, and five worked examples sit in the prompt.
- **The listing labels things `#1, #2…`**, so a thing cannot be confused
  with the number one. Things in a box's holes get labels of their own
  ("in hole 1 of #1"; holes count from 1, left to right, as the robot's own steps do). In the yard it says "the ground", and that the
  notebook stayed inside.
- **Marty passes your own sentence to the hand**, not his paraphrase, and
  his card then shows how it went (✓ or ✗ and the hand's line). A question
  to him never moves anything.
- **The prompt no longer contains the stray word "inHand()".**
- **Two bugs from the first GPT run are fixed:** typing "+" on a fresh 1
  no longer turns it into +0 (B5 and D3 added nothing, reported as done),
  and "run" now fails with ✗ when nothing can run — inside a bubble, an
  untrained robot, an empty desk — instead of reporting ✓.
- The prompt now tells the brain to do only what was said (the first GPT
  run's D3 added a "leave" nobody asked for).
- Also new since the first run (tested in Section I): a set-down finds
  clear table and says so if it lands on something; things riding on a
  pad survive a thought bubble; "desk", "platform" and "tray" are places;
  a full desk is refused before the gift; birds come with nests; "give it
  to Mimi" means copy; panels can be opened and entered; a **What was
  said** button on the title card shows everything said.

## Before the tester starts (the person does this, not the agent)

1. Open **https://toontalk.github.io/toontalk-3d/toontalk-3d-next.html**
   in a tab of its own, in **desktop Chrome** with its built-in AI
   available. (Locally: `node serve.js 8311`, then
   `http://localhost:8311/toontalk-3d-next.html`.)
2. Type a name on the "Who is working here?" card and choose **Free play**.
3. Open Marty's card (the green Martian, bottom left), then **How Marty
   thinks**, and choose **Gemini Nano (in Chrome, no key)**. If Chrome has
   not fetched the model yet, press **Fetch his brain — a big download,
   once** and wait until the panel says it is ready (gigabytes, once).
   For a cloud provider instead, choose it and **enter the API key
   yourself** — the tester must never type, read, copy or be told a key.
4. ⋮ menu → **☑ 🖐 Move my hand by word**. A line appears at the top centre
   ("Tell your hand what to do…"). If it does not appear, the brain is not
   ready yet.
5. Hand the tab to the tester. The switch stays on across reloads.

## What the tester may and may not do

- Type sentences into the **top line** (press Enter) and read what comes
  back. The **▾** at the right end of the line shows a log of every
  sentence and answer; **What was said** on the title card shows the same
  log with the workshop's own lines too.
- Read the line under the table and Marty's log if a sentence was typed
  to him.
- Take screenshots after each sentence.
- As in the first run, you may wrap `LanguageModel.create`/`prompt` in the
  page **to log only** what the brain was sent and what it returned. Never
  change what it is sent; a reload removes the wrapper. Include the raw
  plan for every failure in the report.
- Do **not** touch Settings → How Marty thinks, a key box, or the provider
  selector. Do not use the microphone; everything here is typed.
- Between sections, reload with `?fresh` added to the address
  (`toontalk-3d-next.html?fresh`) so each section begins with a clean
  table; the name and the switch are remembered.

## How to read a result

- **✓ line** — the plan ran to the end. Check the table against the
  expected outcome; a ✓ with the wrong table is a **brain error**. A ✓ that
  claims a move that did not happen is the worst kind — look for it.
- **✗ Step N (verb …) did not work: reason — K steps before it did.** — the
  hand refused a step. If the plan was reasonable and the hand should have
  understood it, it is a **hand error** (include the raw plan: the hand is
  now meant to forgive wording); if the plan asked for something that is
  not there, it is a **brain error**.
- **✗ The brain found nothing for the hand to do** / a plain refusal —
  the brain declined; note whether it should have.

Record, for every sentence: the sentence, ✓/✗, the reported line, what is
on the table afterwards, and your verdict (correct / brain error / hand
error / unclear).

## Order for the Nano rerun

1. **Sections A, B, F, G and H first** — the ones the first run sampled —
   so the scorecard compares like with like (first run: 1 of 25).
2. Then C, D and E, which the first run skipped.
3. Then **Section I**, the new functionality.

Type each sentence exactly, one at a time, and wait for ✓/✗ before the next.

### Section A — fresh things (reload with `?fresh` first)

| # | Sentence | Expected on the table afterwards |
|---|---|---|
| A1 | `put a box on the table` | a box with 2 holes |
| A2 | `pick up a 1 and put it in a 3-hole box` | a second box, 3 holes, a 1 in its left hole; the first box untouched and not joined to it |
| A3 | `create a text pad with ToonTalk on it` | a pad saying ToonTalk |
| A4 | `make a 12` | a number 12, on the table — not riding on the pad |
| A5 | `put a -5 on the table` | a number −5, on the table |
| A6 | `give a robot a scale with 1 and 100 on it` | a robot at the bench with a scale on its desk, 1 in the left pan, 100 in the right; the line says you are inside its thought bubble |
| A7 | `leave` | back at the table; the scale still on the desk |

### Section B — "a" and "the" (reload with `?fresh`, then A1 first)

With one 2-hole box on the table:

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
| C5 | `give the 7 to Mimi` | read as copy: the 7 on the platform, a copy in the hand or on the table (note which) |

### Section D — robots (reload with `?fresh` first)

| # | Sentence | Expected |
|---|---|---|
| D1 | `put a robot on the table` | a mini robot on the table |
| D2 | `give it a 1` | the robot at the bench with the 1 on its desk; the line says you are inside its thought bubble |
| D3 | `add a 1 to the number on the desk` | the desk shows 2 (this is a lesson: the robot is learning) |
| D4 | `leave` | back at the table; the desk shows 1 again (leaving rewinds the daydream; the robot keeps the lesson) |
| D5 | `run the robot` | the desk shows 2 — its thought is "the number 1", so it stops after one round |
| D6 | `put another robot on the table` then `give it a 5` | with two robots on the table the hand asks which — unless the brain names one; note what happened |

### Section E — inside a thought bubble (reload with `?fresh`, then D1, D2)

| # | Sentence | Expected |
|---|---|---|
| E1 | `copy it` | the 1 goes from the desk to Mimi's platform, and the copy is set on one of the robot's little spots |
| E2 | `put a 2 in a box` | a box with 2 holes and a 2 in it, on a spot |
| E3 | `take a robot` | refused: a robot's steps cannot make robots; note the wording |
| E4 | `leave` | back at the table, the world rewound; note what happened to anything the claw held |

### Section F — refusals and edge cases (reload with `?fresh` first)

| # | Sentence | Expected |
|---|---|---|
| F1 | `drop it on the table` | refused: nothing in the hand |
| F2 | `put a 1 in the box` (no box on the table) | either a fresh box with a 1 in it, or a plain "there is no box"; note which |
| F3 | `vacuum the robot` (no robot) | a refusal naming the missing thing |
| F4 | `what is a nest?` | the hand declines — it only moves things; **nothing moves** (the first run vacuumed something here) |
| F5 | `put a bird on the table` | a nest with its bird (birds come with nests) |

### Section G — the same sentence said to Marty

Type into **Marty's** box (not the top line):

| # | Sentence | Expected |
|---|---|---|
| G1 | `put a box on the table` | Marty's short line, then a ✓ line on his card with the hand's report, and a box on the table |
| G2 | `what does Dusty do?` | an ordinary answer about Dusty; **nothing moves** |

Then ⋮ → untick **Move my hand by word**, and again to Marty:

| # | Sentence | Expected |
|---|---|---|
| G3 | `put a box on the table` | he says he cannot move your hand and names the switch; nothing moves |

Tick the switch again afterwards.

### Section H — names, the thought, doors, the notebook (reload with `?fresh` first)

| # | Sentence | Expected |
|---|---|---|
| H1 | `take a nest and call it orders` | a nest named "orders" (its bird takes the name too) |
| H2 | `file the nest in the notebook` | the nest gone from the table, an entry "orders" in the notebook |
| H3 | `take orders out of the notebook` | a copy of the nest; the notebook keeps its entry |
| H4 | `go out to the yard` | the ground in the table's place |
| H5 | `come back in` | the table is back |
| H6 | `put a robot on the table` then `give it a 3` | the 3 on the desk, inside the bubble |
| H7 | `erase the 3 so it works for any number` | the robot's thought reads "any number" (Ruby); the 3 stays on the desk |
| H7b | `add a 1 to the 3 on the desk` | the desk shows 4 — the lesson has a step (a robot with no steps is retrained by its next gift, which would undo H7) |
| H8 | `leave`, then `take the 3 off the desk and give the robot a 5` | the 3 comes off first (the desk holds one thing); the robot is trained, so it starts at once and — its thought being "any number" — **keeps going**: 6, 7, 8… Stop it by typing "." (or "stop") into the line and note that it counted on |

### Section I — new since the first run (reload with `?fresh` first)

| # | Sentence | Expected |
|---|---|---|
| I1 | `create a pad with ToonTalk on it`, then `put a box on the table`, then `make a 12` | three separate things: the 12 does not ride on the pad and the box does not join anything. If the table is crowded, the hand says where it landed instead of ✓ |
| I2 | `put a 7 on the pad` | the 7 rides on the pad ("It rides on the pad now") |
| I3 | `put a robot on the table`, `give it a 1`, then `leave` | the pad still carries its 7 after leaving (the rewind used to drop riders) |
| I4 | `give the robot a 5` (the 1 still on its desk) | refused before anything moves: the desk already holds the number 1, take that first |
| I5 | `take what is on the desk and put it on the table` | the 1 from the desk on the table; the desk empty |
| I6 | `put a 1 and a 3 in a box`, then `put the 3 on the 1` | the box holds 4 and an empty hole |
| I7 | `open the pad's panel` | the pad's panel comes out as a tray on the table |
| I8 | `go into the pad's panel`, then `come back out` | inside the pad's own little world, then back at the table |
| I9 | `put a robot on the table`, `give it a 1`, `take a number`, then `leave` | leaving works with the claw holding something; back at the table, hand empty |
| I10 | press **What was said** on the title card | a log of the workshop's lines and every sentence and answer, scrollable |
| I11 | `put a robot on the table`, `give it a 1`, then `run the robot` | ✗: the hand is inside the robot's thought bubble — leave it first (never ✓) |
| I12 | `leave`, then `run the robot` | ✗: the robot has not been trained yet (nothing was taught, so leaving kept nothing) |
| I13 | `put a 7 on the pad`, then (log the listing) | the listing shows the 7 as a thing of its own, "riding on" the pad |
| I14 | `open the pad's panel` (log the listing) | the tray is listed as "the panel (tray) of a pad…", not "a room" |
| I15 | `make a 7`, `copy the 7`, then `vacuum the 7 on the table` | the hand ends empty after each sentence, and Dusty takes the 7 without a refusal |

## What to report

1. Provider and model tested (as shown on Marty's card; never a key).
2. The table of sentences with ✓/✗, the reported line and the verdict.
3. **A scorecard for A, B, F, G, H against the first Nano run (1 of 25).**
4. For each **brain error**: the sentence, the listing the brain had, its
   raw plan, and what plan would have been right.
5. For each **hand error**: the sentence, the raw plan and the refusal —
   especially any plan whose meaning was clear but the hand still refused.
6. Anything that fits no category: a claimed move that did not happen, a
   strange state left behind, a line that never came back.
7. Timing: seconds from Enter to the first move.

## Known limits (not bugs)

- Inside a thought bubble the stacks give the robot's own things (no
  robots: there is no "make a robot" step for a robot), things go on the
  robot's spots, and leaving rewinds the table — that is how ToonTalk
  lessons work.
- A trained robot whose thought still fits after a round keeps going
  (H8); that is ToonTalk, not the hand.
- A panel's contents are listed only once the hand is inside it.
- Nano is small: it cannot hold the whole manual, and a long listing
  inside a thought bubble is where it is most likely to struggle.
