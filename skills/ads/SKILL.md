---
name: ads
description: Build a batch of paid image ads end to end. Start from research, pin the idea, write the copy, pick a proven format, clone that format image-to-image so the render IS the source frame with your content in it, generate in bulk, review every ad on one page, then ship the keepers. Use when the user says make new ads, build the next ad batch, find ad concepts, or hands over headlines and wants creatives.
---

# /ads. From research to a shipped creative

This is the process. Seven steps, in order:

research > concept > copy > format > generate > review > ship

**The one rule that governs everything:** we do not design ads. We find ads that
have run long enough to be proven, then put our content in their frame. A render
that is inspired by the source is a failure. Only two things ever change: the
photo and the words.

---

## Pre-Flight

1. **Read the voice rules.** Ask the user for theirs. If they have none, use
   these: never put words in the reader's mouth, no invented numbers, no dashes
   as punctuation, no quotation marks on a creative.
2. **Know the buyer.** Write one line: who they are, what they earn, and how
   aware they are. Aware of the problem? Aware that solutions exist? Aware of
   your product? An ad written for the wrong level of awareness gets cut. Most
   buyers who see paid ads already know solutions exist. Ads that prove the
   problem exists are a waste on them.
3. **Confirm a source of proven ads.** You need a place to see ads that have
   been running for months. The Meta Ad Library is free. Paid ad spy tools show
   run time. A swipe folder of screenshots works too. Confirm you can reach it
   before promising anything.

---

## Step 1. Research

Collect what the buyer says, in their own words. Reviews, sales calls, support
tickets, comments under competitor ads. Pull out the pains, the wants, and the
words they use. Save it to a file in the project. This is where every headline
comes from.

- **Every number must trace to a real quote.** Check the source before letting a
  figure onto a creative. A round number that sounds good is a lie waiting to be
  found. The honest number from a real quote is often bigger.
- **If the user supplies headlines, improve them. Do not replace them.** Change
  the smallest thing that fixes the fault, and say which word you changed and
  why.
- **Watch for a command where they wrote a promise.** Home by six describes a
  state. Stop working at 8pm orders the reader around. The first one wins.

---

## Step 2. Concept. Pin the idea BEFORE anything renders

**This is the step that gets skipped and it is the expensive one.** One ad in an
early batch burned four renders and was then scratched. Nobody had written down
what the ad was arguing.

For each ad, write one line: **what does this ad claim, and what proves it?**
Then check the picture and the proof argue the *same* thing. The scratched ad
had a headline about getting your evenings back, sitting above a receipt about
how fast an email gets written. The text made no sense.

Make lists. Ten angles. Ten desires. Ten emotional triggers. Each ad picks one
of each. The lists are the vocabulary for the whole account, so keep them in a
file and reuse them.

If you cannot state the idea in one sentence, do not render. Ask.

---

## Step 3. Copy

Write the headline, the body, and the call to action for each concept. Short.
Plain words. Read it out loud. If you stumble, rewrite it.

Write ten headlines for each concept. Pick the best two. Most of writing is
picking.

---

## Step 4. Format

Two doors. Prefer door B when the swipe folder already has something that fits.

**A. Sweep an ad library for a new one.** Only ever study winners. Sort by how
long the ad has been running. Duration is the signal. An image ad still live
after months is one somebody kept paying for. Save anything worth keeping to
your own swipe folder with a note on why it works, because ad libraries rotate
and the link will die.

**B. Pull from your swipe folder.** Each saved format carries a description, why
it works, how you would adapt it, and any past verdict. Retired formats stay in
the folder with the reason they were killed, so they do not get proposed again
three months later.

---

## Step 5. Generate

### Three ways to make the picture

1. **Words to image.** Describe the picture, the model draws it. Fast and cheap.
   It reinterprets the layout on every render, so use it only for a photo that
   goes INSIDE a frame. The frame itself needs door 2.
2. **Image to image.** Hand the model the real source ad plus an optional face
   photo, and list what must not move. This is the default. It is what turns
   inspired by into that is the source with our words in it.
3. **Code with no model.** A flat colour card with big text needs no AI at all.
   Write it as HTML, screenshot it. Zero cost, perfect text, and the
   longest-running direct-response image ad we ever found was exactly this.

### Clone the frame, image to image

```bash
python3 clone_ad.py spec.json
```

**Never describe the layout in words and hope.** Hand the model the real creative
and list what must not move. Keep the crop, the type, the colour grade, the
chips, the pills, the buttons, the props. Change only the photograph and the
words.

The script bakes in four guardrails. Each one has failed silently before. Read
its docstring. Do not remove them:

1. **Aspect.** A portrait source came back square. State the ratio every time.
2. **Lighting.** A studio headshot imports its rim light, so the face is lit like
   a portrait inside a dim room. That mismatch is what reads as AI.
3. **Invented figures.** Any screen or table gets filled with plausible, legible,
   fake money. Telling the model not to does not hold. **Fix it structurally**:
   crop the screen to a fragment that cuts through cells on every edge, so there
   is physically nowhere for a header or a totals row to sit.
4. **Wordmarks.** The source advertiser's own logo burns through a ban by name.
   One source card put its client's logo on our render twice.

Guardrails 3 and 4 survive being forbidden in the prompt. Nothing replaces
opening the result at full size.

### The bulk rule. Generate 10

Image models miss. A single render is a coin flip. Ten renders of the same spec
give you two or three that are right, and picking is cheap. So:

- One spec per ad, ten outputs per spec. Name them `ad01_v01.png` through
  `ad01_v10.png`.
- Change one thing between variants if you want: the headline, the face, the
  crop. Keep everything else fixed so you can see what moved.
- Get a green light on the batch size before spending. Renders cost about 15
  cents each on the premium model, so ten ads at ten variants is about 15
  dollars. Say the number before you run it.
- Never silently re-roll. If the first ten are all wrong, the spec is wrong.
  Fix the spec.

---

## Step 6. Review

### Verify every render at full size

Non-negotiable. Open it. Do not glance at a thumbnail. Check, in order:

1. Is any number, label or logo legible that we did not put there?
2. Is the aspect ratio the same as the source?
3. Is the face lit by the room, or is it wearing the studio light from its
   reference photo? The second is what reads as AI.
4. Did anything from the source's business survive? One render carried the sales
   numbers out of a shopping ad before anyone looked.
5. Does the picture argue the same thing as the words?

**A render regresses when you re-roll it for an unrelated reason.** Swapping a
face re-generates the whole image and old faults come back. Re-check all five
every time.

### One page, every ad, keep or edit or kill

A stage never ends in a terminal list of file paths. It ends in one HTML page
with every variant on it at a size you can read.

```bash
python3 review_page.py renders/ --out renders/review.html
```

Under each image: keep, edit, or kill, plus a note box. Notes save on their own
so a refresh loses nothing. When the user is done they press Copy review JSON and
paste it back to you. Read it. Every kill has a reason. Every edit has a note.
Act on each one.

Say plainly which of the five checks failed and why. The user uses that.

**One ad at a time when it matters.** The grid narrows the set. For a final
call, put the source on the left and ours on the right at full size. Do not
present six and ask which one they like.

---

## Step 7. Ship

Record every decision in the swipe folder. The status ladder is
`idea | shortlisted | adapted | testing | retired`.

- Picked: `shortlisted`, with a note naming which ad it carries and what is
  still open.
- Killed: `retired`, **never deleted**, with the reason. The row is the record
  of why we are not running it.

Keep one row per shipped ad in a sheet or a file, with the angle, the desire,
the trigger, the format, the headline, the copy, the image, and a link to the
live ad once it is up. Use the same vocabulary from the Step 2 lists, or the
columns stop being filterable.

---

## Rules

- **Idea before render, every time.** Step 2 is the one that saves money.
- **Never invent a number that lands on a creative**, and never let a
  half-legible one through. Sharp or genuinely unreadable, nothing between.
- **Retire, do not delete.** A killed format with its reason is worth more than
  a missing row.
- **Always ten.** A single render is a guess.
- **Grid to choose, side by side to decide.** Nothing is approved without the
  source next to ours at full size.
- **Generation costs money.** Say the number before a batch.
- **Nothing ships off this pipeline unseen at full size.** Two of the four
  failure modes survive being forbidden in the prompt.

## Learnings

- **The cheapest creative had the longest life.** Across a sweep of 44
  advertisers, the longest-running direct-response image ad was a flat red card
  with yellow text, 1,621 days, zero design. A second unrelated advertiser runs
  the same shape in black.
- **The B2C tell.** Most formats in a swipe file come from creators selling to
  creators. Street photos, drinks, consumer palettes. Keep the structure, strip
  every consumer signal, or it reads wrong to a business buyer.
- **Weird has to resolve.** A pattern-interrupt image only works if the joke
  lands within a second. A printed email popping out of a toaster beat a vending
  machine, a conveyor belt, a buried desk and a shredder. The shredder was cut
  even though it argued the claim best, because shredding CVs in front of people
  who employ people reads as cruel.
