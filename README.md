# Image Ads Starter. Make image ads with AI, the whole flow

You give it research and a headline. It finds a proven ad format, puts your photo and your words inside that exact frame, makes ten versions, and puts them all on one page for you to keep, edit or kill. Then you ship the keepers.

From this video: [How I Make Image Ads With AI: The Whole Flow](https://www.youtube.com/@Hamzaouladd)

## What you get

- `skills/ads/SKILL.md` is the process. Claude Code reads it and runs the seven steps with you.
- `clone_ad.py` makes the picture. It takes a real winning ad and swaps in your photo and your words. Nothing else moves.
- `review_page.py` builds one page with every render on it. Keep, edit or kill each one, add a note, copy the review, paste it back to Claude.
- `example_spec.json` is a filled in spec so you can see the shape.
- `SETUP_PROMPT.md` is the prompt you paste into Claude Code. It walks you through the whole thing.

## The flow

1. Research. What does your buyer say, in their own words?
2. Concept. One line per ad: what it claims and what proves it.
3. Copy. The headline, the body, the button. Short and plain.
4. Format. Find an ad that has run for months. That one is proven.
5. Generate. Clone that ad with your content inside it. Make ten.
6. Review. Every render on one page. Keep, edit or kill.
7. Ship. Run the keepers. Write down why the rest died.

## Set up OpenRouter (5 minutes)

The picture maker runs on [OpenRouter](https://openrouter.ai). One key gives you every image model.

1. Make an account at openrouter.ai.
2. Go to Credits and put in ten dollars.
3. Turn on auto top up so a batch never dies half way.
4. Go to Keys and make one. Copy it.
5. Give it to Claude when it asks. It writes it into a `.env` file. The key never goes in the code.

A render costs cents on the paid models. Prices move every month, so check the model page on OpenRouter before you budget a batch.

## How to run it

**Get Claude Code.** Install it from [claude.com/claude-code](https://claude.com/claude-code). Open it inside this folder and paste `SETUP_PROMPT.md`. It does everything below with you.

**Or by hand.**

Make one render:

```bash
python3 clone_ad.py example_spec.json
```

Make ten (this is the rule, see below):

```bash
python3 clone_ad.py example_spec.json --n 10
```

Build the review page for a folder of renders:

```bash
python3 review_page.py renders/
open renders/review.html
```

Mark each one keep, edit or kill. Write a note. Press Copy review JSON. Paste it to Claude.

## The spec file

`clone_ad.py` reads one JSON file per ad:

```json
{
  "source": "swipes/proven_ad.jpg",
  "face": "faces/founder.png",
  "out": "renders/ad01.png",
  "aspect": "4:5 portrait, 1024 by 1280",
  "keep": ["the crop", "the font", "the colours", "the button"],
  "change": ["the person becomes IMAGE 2", "headline becomes: Your words here"],
  "ban": ["no readable numbers on the screen"]
}
```

- `source` is the real ad you are cloning. Required.
- `face` is a photo of the person who should appear. Optional. It is used for identity only.
- `out` is where the render lands. With `--n 10` you get `ad01_v01.png` to `ad01_v10.png`.
- `aspect` is the size. Say it every time or the model picks square.
- `keep` is what must not move. Be specific.
- `change` is the photo and the words. Only those.
- `ban` is anything extra that must not show up.

Four guardrails are added to every prompt on their own. Aspect, lighting, no invented numbers, no logos. Two of them still slip through sometimes, so open every render at full size before it goes anywhere.

## The bulk rule

Always make ten. Image models miss. One render is a coin flip. Ten renders of the same spec give you two or three good ones, and picking is cheap. If all ten are wrong, the spec is wrong. Fix the spec.

## One rule

Do not design ads. Find ads that have run long enough to be proven. Put your content in their frame. Only the photo and the words change.

MIT license. Use it, change it, sell with it.
