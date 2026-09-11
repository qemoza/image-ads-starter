#!/usr/bin/env python3
"""Build one HTML page to review a folder of ad renders.

    python3 review_page.py renders/
    python3 review_page.py renders/ --out renders/review.html

Every image in the folder goes on one page in a grid at a readable size. Click
an image to see it full size. Under each: keep, edit or kill, plus a note box.
Notes save in the browser so a refresh loses nothing. When you are done, press
Copy review JSON and paste it to Claude, or Download review to get a file.

No dependencies. Plain HTML and JS. Open the page straight from disk.
"""
import html
import json
import os
import re
import sys

EXTS = ('.png', '.jpg', '.jpeg', '.webp', '.gif')

PAGE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title><link rel="icon" href="data:,">
<style>
:root{--bg:#0d0f14;--card:#161a22;--line:#232936;--txt:#e8eaf0;--dim:#8b93a7;--acc:#8b5cf6;--ok:#22c55e;--warn:#eab308;--bad:#ef4444}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font:14px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif}
header{position:sticky;top:0;z-index:50;background:rgba(13,15,20,.95);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:14px 22px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
h1{font-size:17px;font-weight:800}h1 span{color:var(--acc)}
.help{color:var(--dim);font-size:12.5px}
button{cursor:pointer;border:1px solid var(--line);background:var(--card);color:var(--txt);border-radius:8px;padding:7px 14px;font-size:13px;font-weight:600}
button.primary{background:var(--acc);border-color:var(--acc);color:#fff}
button:hover{border-color:var(--acc)}
main{padding:20px 22px 90px;max-width:1750px;margin:0 auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.card{background:var(--card);border:2px solid var(--line);border-radius:12px;overflow:hidden}
.card.keep{border-color:var(--ok)}.card.edit{border-color:var(--warn)}.card.kill{border-color:var(--bad);opacity:.55}
.card img{width:100%;max-height:520px;object-fit:contain;background:#000;display:block;cursor:zoom-in}
.cb{padding:10px 12px;display:flex;flex-direction:column;gap:8px}
.fname{font-size:12px;color:var(--dim);word-break:break-all}
select{background:#10131a;border:1px solid var(--line);border-radius:8px;color:var(--txt);font-family:inherit;font-size:13px;padding:7px 9px;width:100%}
select.keep{border-color:var(--ok)}select.edit{border-color:var(--warn)}select.kill{border-color:var(--bad)}
textarea{background:#10131a;border:1px solid var(--line);border-radius:8px;color:var(--txt);font-family:inherit;font-size:12.5px;padding:7px 9px;resize:vertical;min-height:34px;width:100%}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:200;display:none;align-items:center;justify-content:center;cursor:zoom-out}
#lb.open{display:flex}#lb img{max-width:96vw;max-height:96vh}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--ok);color:#fff;font-weight:700;padding:10px 22px;border-radius:10px;z-index:300;display:none}
.sum{position:fixed;bottom:0;left:0;right:0;background:rgba(13,15,20,.96);border-top:1px solid var(--line);padding:10px 22px;font-size:13px;color:var(--dim)}
.sum b{color:var(--txt)}
</style></head><body>
<header><h1>Ad <span>Review</span></h1><div class="help">Keep = run it. Edit = keep with changes, say what in the note. Kill = drop it, say why. Click an image for full size.</div>
<div style="margin-left:auto;display:flex;gap:8px"><button onclick="exp(false)">Copy review JSON</button><button class="primary" onclick="exp(true)">Download review</button></div></header>
<main><div class="grid" id="grid"></div></main>
<div class="sum" id="sum"></div>
<div id="lb" onclick="this.classList.remove('open')"><img id="lbimg" alt=""></div>
<div class="toast" id="toast"></div>
<script>
const FILES = __FILES__;
const KEY = __KEY__;
let st = {};
try { st = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { st = {}; }
function save(){ try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} sum(); }
function g(f){ return st[f] || (st[f] = {status:'', note:''}); }
const grid = document.getElementById('grid');
FILES.forEach(f => {
  const s = g(f);
  const c = document.createElement('div'); c.className = 'card ' + (s.status || '');
  const img = document.createElement('img'); img.loading = 'lazy'; img.src = f; img.alt = f;
  img.onclick = () => { document.getElementById('lbimg').src = f; document.getElementById('lb').classList.add('open'); };
  const cb = document.createElement('div'); cb.className = 'cb';
  const name = document.createElement('div'); name.className = 'fname'; name.textContent = f;
  const sel = document.createElement('select'); sel.className = s.status || '';
  [['', 'Not reviewed'], ['keep', 'Keep'], ['edit', 'Edit'], ['kill', 'Kill']].forEach(([v, l]) => {
    const o = document.createElement('option'); o.value = v; o.textContent = l; if (s.status === v) o.selected = true; sel.appendChild(o);
  });
  sel.onchange = () => { s.status = sel.value; sel.className = s.status; c.className = 'card ' + (s.status || ''); save(); };
  const ta = document.createElement('textarea'); ta.placeholder = 'Notes. What to change, or why it dies.'; ta.value = s.note || '';
  ta.oninput = () => { s.note = ta.value; save(); };
  cb.appendChild(name); cb.appendChild(sel); cb.appendChild(ta);
  c.appendChild(img); c.appendChild(cb); grid.appendChild(c);
});
function sum(){
  let k = 0, e = 0, x = 0, n = 0;
  FILES.forEach(f => { const s = st[f]; if (!s) return; if (s.status === 'keep') k++; if (s.status === 'edit') e++; if (s.status === 'kill') x++; if (s.note && s.note.trim()) n++; });
  document.getElementById('sum').innerHTML = '<b>' + k + '</b> keep, <b>' + e + '</b> edit, <b>' + x + '</b> kill, <b>' + n + '</b> notes, ' + FILES.length + ' total. Saved as you go. Export when done.';
}
function payload(){
  return JSON.stringify({ exported_at: new Date().toISOString(), folder: KEY,
    reviews: FILES.map(f => ({ file: f, status: (st[f] || {}).status || 'unreviewed', note: (st[f] || {}).note || '' })) }, null, 1);
}
function exp(dl){
  const s = payload();
  if (dl) {
    const b = new Blob([s], { type: 'application/json' }), u = URL.createObjectURL(b), l = document.createElement('a');
    l.href = u; l.download = 'review.json'; l.click(); toast('Downloaded. Give the file to Claude.');
  } else if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(s).then(() => toast('Copied. Paste it to Claude.'), () => fallbackCopy(s));
  } else { fallbackCopy(s); }
}
function fallbackCopy(s){
  const ta = document.createElement('textarea'); ta.value = s; document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); toast('Copied. Paste it to Claude.'); } catch (e) { toast('Copy failed. Use Download instead.'); }
  document.body.removeChild(ta);
}
function toast(m){ const t = document.getElementById('toast'); t.textContent = m; t.style.display = 'block'; setTimeout(() => t.style.display = 'none', 3000); }
sum();
</script></body></html>"""


def main(folder, out):
    folder = os.path.abspath(folder)
    if not os.path.isdir(folder):
        raise SystemExit(f"not a folder: {folder}")
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith(EXTS))
    if not files:
        raise SystemExit(f"no images found in {folder}")
    out = os.path.abspath(out or os.path.join(folder, 'review.html'))
    out_dir = os.path.dirname(out)
    os.makedirs(out_dir, exist_ok=True)
    rel = [os.path.relpath(os.path.join(folder, f), out_dir).replace(os.sep, '/') for f in files]
    key = 'ad_review_' + re.sub(r'[^a-z0-9]+', '_', os.path.basename(folder).lower()).strip('_')
    page = (PAGE.replace('__TITLE__', html.escape('Ad review: ' + os.path.basename(folder)))
                .replace('__FILES__', json.dumps(rel))
                .replace('__KEY__', json.dumps(key)))
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write(page)
    print(f"{out}  {len(files)} images")
    print("Open it in a browser. Review, then press Copy review JSON and paste it to Claude.")


if __name__ == '__main__':
    args = sys.argv[1:]
    out = None
    if '--out' in args:
        i = args.index('--out')
        out = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1:
        raise SystemExit(__doc__)
    main(args[0], out)
