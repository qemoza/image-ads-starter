# The prompt you give Claude Code

Open Claude Code inside this folder. Copy everything below the line and paste it in.

---

I want to make a batch of image ads for my business with the process in this repo. Read `skills/ads/SKILL.md` first. That is the process. Follow it step by step and do not skip a step. Talk to me in plain words.

**Step 0. Setup.** Check that Python 3 works and that `python3 clone_ad.py` prints its help. Ask me for my OpenRouter key. Write it into a `.env` file in this folder as `OPENROUTER_API_KEY=...`. Never print it back to me and never put it in any other file. Make a `renders/`, a `swipes/` and a `faces/` folder.

**Step 1. Research.** Ask me who my buyer is and what I sell. Ask me to paste anything I have in the buyer's own words: reviews, sales call notes, support tickets, comments. Pull out the pains, the wants and the exact words they use. Save it to `research.md`. Then ask me how aware my buyer is: of the problem, of solutions, or of my product. Write that in one line at the top of the file.

**Step 2. Concept.** From the research, make three lists and save them to `concepts.md`: ten angles, ten desires, ten emotional triggers. Then propose five ads. For each one write a single line: what this ad claims, and what proves it. Show me the five. I will pick. Do not make a picture until I have picked.

**Step 3. Copy.** For each ad I picked, write ten headlines. Pick your best two and tell me why. Then write the body and the button text. Short sentences. Plain words. No dashes as punctuation, no quotation marks, no invented numbers. Every number must trace to something in `research.md`. Save the copy to `copy.md`. Show me. Wait for my edits.

**Step 4. Format.** Ask me to put screenshots of two or three proven ads into `swipes/`. If I have none, tell me how to find them: open the Meta Ad Library, search my market, look for image ads that have been running for months. Old is good. For each one, write a note in `swipes/notes.md` on why it works and which of my ads it fits. Ask me to put a photo of the person who should appear in the ads into `faces/`.

**Step 5. Generate.** For each ad, write a spec file like `example_spec.json`. Be very specific in `keep`. In `change` list only the photo and the words. Tell me the batch size and the cost before you run anything. Then run `python3 clone_ad.py specs/ad01.json --n 10` for each one. Make ten of each.

**Step 6. Review.** Run `python3 review_page.py renders/` and open the page for me. I will mark each one keep, edit or kill and write notes. Then I will press Copy review JSON and paste it to you. Read every note. For every edit, fix the spec and rerun. For every kill, write the reason into `swipes/notes.md` so we never propose that format again. Before you show me anything, open each render at full size yourself and check the five things in the skill: readable numbers we did not put there, wrong aspect, studio light on the face, anything left from the source's business, and whether the picture argues the same thing as the words.

**Step 7. Ship.** Give me the final keepers as a list of file paths with the headline, the copy and the format next to each one. Save it to `shipped.md`.

Go one step at a time. Ask before you spend money. Never tell me an ad is done before you have looked at it at full size.
