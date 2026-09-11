#!/usr/bin/env python3
"""Clone a winning ad's frame image to image, swapping only the photo and the words.

    python3 clone_ad.py spec.json
    python3 clone_ad.py spec.json --n 10      # ten variants, the bulk rule

The whole point is that the output is the SOURCE ad with your content in it. Not
an ad inspired by it. Describing a layout in words does not work. The model
reinterprets it every render. Hand it the real creative and list what must not
move. See skills/ads/SKILL.md for where this sits in the process.

spec.json:
{
  "source":  "swipes/the-real-ad.jpg",       # required, the frame we are keeping
  "face":    "faces/person.png",             # optional, identity ONLY
  "out":     "renders/ad01.png",             # with --n, becomes renders/ad01_v01.png ...
  "aspect":  "4:5 portrait, 1024 by 1280",   # REQUIRED, see GUARDRAILS
  "keep":    ["...", "..."],                 # what must not change
  "change":  ["...", "..."],                 # the photo and the words
  "ban":     ["..."]                         # extra per-source bans
}

Needs one environment variable: OPENROUTER_API_KEY. Put it in a .env file next
to this script, or export it in your shell. Never paste it into the code.

Four guardrails are appended to every prompt automatically because each one has
failed silently in production. Do not remove them:

  1. ASPECT. A portrait source came back square, which destroys the composition.
  2. LIGHTING. A studio headshot imports its rim light, so the face is lit like
     a portrait inside a dim room. That mismatch is what reads as AI.
  3. FIGURES. Any screen or table gets filled with plausible legible invented
     money. Instructions alone do NOT stop this. Crop the surface away instead.
  4. WORDMARKS. The source advertiser's own logo burns through a ban.

Guardrails 3 and 4 survive being explicitly forbidden, so ALWAYS open the result
at full size before it goes anywhere. Nothing here replaces looking at it.
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))
except ImportError:
    pass  # fine, the key can come from the shell instead

MODEL = os.environ.get('CLONE_AD_MODEL', 'google/gemini-3-pro-image')  # aspect-capable, reliable in-image text
URL = 'https://openrouter.ai/api/v1/chat/completions'

GUARDRAILS = """
NON-NEGOTIABLE, these have all failed silently before:
- ASPECT RATIO: output must be {aspect}. Never square unless that is stated.
- LIGHTING: if a face reference is supplied, use it for FACE AND IDENTITY ONLY.
  Ignore its lighting, clothing, background and colour grade completely. The face
  must be lit by the same light as the scene around it. If the face looks
  brighter, warmer or more polished than the wall behind it, it is wrong.
- NO INVENTED FIGURES: any screen, table, chart or document in frame carries
  marks that suggest text, never readable words or digits. No totals row, no
  currency symbols, no month names, no column headers. Never render text
  mirrored or reversed. If a viewer zooming in can read a number, it is wrong.
- NO WORDMARKS: no brand name, logo or watermark anywhere, including any that
  appear in the source image.
- No quotation marks in any on-image copy.
"""


def data_uri(path):
    mime = 'image/png' if path.lower().endswith('.png') else 'image/jpeg'
    with open(path, 'rb') as fh:
        return f"data:{mime};base64,{base64.b64encode(fh.read()).decode()}"


def build_prompt(spec):
    has_face = bool(spec.get('face'))
    who = ("IMAGE 1 is an existing ad creative. IMAGE 2 is a photograph of a person."
           if has_face else "IMAGE 1 is an existing ad creative.")
    parts = [
        who,
        "\nRebuild IMAGE 1 exactly. Treat it as a template to be filled, never as "
        "inspiration. Change ONLY what is listed under CHANGE.",
        "\nKEEP IDENTICAL to IMAGE 1. Do not reinterpret any of this:",
    ]
    parts += [f"- {k}" for k in spec.get('keep', [])]
    parts.append("\nCHANGE ONLY THESE:")
    parts += [f"- {c}" for c in spec.get('change', [])]
    if spec.get('ban'):
        parts.append("\nBANNED in this render:")
        parts += [f"- {b}" for b in spec['ban']]
    parts.append(GUARDRAILS.format(aspect=spec.get('aspect', '4:5 portrait, 1024 by 1280')))
    parts.append("Spell every word of on-image copy exactly as given. No other text anywhere.")
    return "\n".join(parts)


def render(spec):
    key = os.environ.get('OPENROUTER_API_KEY')
    if not key:
        raise SystemExit("OPENROUTER_API_KEY is not set. Put it in .env or export it. See README.md.")
    content = [{'type': 'text', 'text': build_prompt(spec)},
               {'type': 'image_url', 'image_url': {'url': data_uri(spec['source'])}}]
    if spec.get('face'):
        content.append({'type': 'image_url', 'image_url': {'url': data_uri(spec['face'])}})
    body = json.dumps({'model': MODEL, 'modalities': ['image', 'text'],
                       'messages': [{'role': 'user', 'content': content}]}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        'Authorization': f"Bearer {key}",
        'Content-Type': 'application/json',
        'X-Title': 'image-ads-starter'})
    for attempt in range(3):
        try:
            return json.load(urllib.request.urlopen(req, timeout=240))
        except urllib.error.HTTPError as ex:
            if ex.code in (429, 502, 503) and attempt < 2:
                time.sleep(8)
                continue
            raise RuntimeError(f'HTTP {ex.code}: {ex.read()[:250]!r}')


def render_one(spec, out):
    started = time.time()
    res = render(spec)
    images = res['choices'][0]['message'].get('images') or []
    if not images:
        raise SystemExit(f"no image returned: {str(res['choices'][0])[:300]}")
    url = images[0]['image_url']['url']
    raw = (base64.b64decode(url.partition(',')[2]) if url.startswith('data:')
           else urllib.request.urlopen(url).read())
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    with open(out, 'wb') as fh:
        fh.write(raw)
    print(f"{out}  {len(raw)//1024} KB  {time.time()-started:.0f}s")


def main(spec_path, n):
    spec = json.load(open(spec_path))
    for key in ('source', 'out', 'aspect'):
        if not spec.get(key):
            raise SystemExit(f"spec is missing {key!r}. See the docstring at the top of this file.")
    out = spec['out']
    if n == 1:
        render_one(spec, out)
    else:
        stem, ext = os.path.splitext(out)
        for i in range(1, n + 1):
            render_one(spec, f"{stem}_v{i:02d}{ext or '.png'}")
    print("NOW OPEN EVERY ONE AT FULL SIZE. Guardrails 3 and 4 survive being forbidden.")
    print("Then: python3 review_page.py <folder> to review them on one page.")


if __name__ == '__main__':
    args = sys.argv[1:]
    n = 1
    if '--n' in args:
        i = args.index('--n')
        n = int(args[i + 1])
        del args[i:i + 2]
    if len(args) != 1:
        raise SystemExit(__doc__)
    main(args[0], n)
