"""Build a standalone preview.html for a deck folder (main_18, final_9 or speech_9).

Usage:
    python3 build_preview.py main_18
    python3 build_preview.py final_9

Each deck is a `deck.json` manifest (title, slide order,
font faces) plus one `<section>` per file in `slides/`. Each slide is a fixed 1920x1080 canvas
with inline styles; the speaker notes are the `<aside>` at the end of each section.

This script stacks the slides into one page that opens offline in a browser:
- fonts: the Ubuntu files in ../assets/fonts/Ubuntu (deck.json points at uploaded blobs)
- images: /_blob/<id> is rewritten to assets/<id>.png or .svg when that file exists
- notes: shown under each slide (press N to hide or show)
`<x-icon>` elements belong to the original slide editor's icon set and render empty here.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "assets", "fonts", "Ubuntu")
BLANK = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
FACE_FILES = {
    "Ubuntu": "Ubuntu-Regular.ttf",
    "Ubuntu Medium": "Ubuntu-Medium.ttf",
    "Ubuntu Bold": "Ubuntu-Bold.ttf",
    "Ubuntu Condensed": "Ubuntu-Regular.ttf",  # condensed cut not in the font pack
}


def main() -> None:
    deck_dir = os.path.join(HERE, sys.argv[1])
    deck = json.load(open(os.path.join(deck_dir, "deck.json"), encoding="utf-8"))
    faces = "\n".join(
        f"@font-face{{font-family:'{fam}';src:url('../../assets/fonts/Ubuntu/{fn}');}}"
        for fam, fn in FACE_FILES.items()
    )
    assets = os.path.join(deck_dir, "assets")
    have = set(os.listdir(assets)) if os.path.isdir(assets) else set()

    def blob(m: re.Match) -> str:
        bid = m.group(1)
        for ext in (".png", ".svg", ".jpg", ".webp"):
            if bid + ext in have:
                return f'src="assets/{bid}{ext}"'
        # image not exported: transparent pixel, shown as a neutral placeholder box
        return f'src="{BLANK}" data-missing-blob="{bid}"'

    parts = []
    for i, sid in enumerate(deck["order"], 1):
        html = open(os.path.join(deck_dir, "slides", f"{sid}.html"), encoding="utf-8").read()
        html = re.sub(r'src="/_blob/([0-9a-f]+)"', blob, html)
        note = re.search(r"<aside>(.*?)</aside>", html, re.S)
        html = re.sub(r"<aside>.*?</aside>", "", html, flags=re.S)
        parts.append(
            f'<div class="frame"><div class="scaler">{html}</div></div>'
            f'<p class="note"><b>{i}. {sid}</b> {note.group(1).strip() if note else ""}</p>'
        )

    page = f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{deck['title']}</title>
<style>
{faces}
body{{margin:0;background:#2b2b30;color:#eee;font-family:Ubuntu,Arial,sans-serif;padding:16px}}
.frame{{width:min(100%,1280px);aspect-ratio:16/9;margin:24px auto 8px;overflow:hidden;position:relative;background:#fff}}
.scaler{{width:1920px;height:1080px;transform-origin:0 0;position:absolute;top:0;left:0}}
.scaler>section{{width:1920px;height:1080px;box-sizing:border-box;position:relative;overflow:hidden}}
.scaler *{{margin:0;box-sizing:border-box}}
.note{{max-width:1280px;margin:0 auto 32px;font-size:15px;line-height:1.5;color:#ccc}}
body.hide-notes .note{{display:none}}
img[data-missing-blob]{{background:#E6ECEF}}
</style></head><body>
{''.join(parts)}
<script>
function fit(){{document.querySelectorAll('.frame').forEach(f=>{{f.firstChild.style.transform='scale('+(f.clientWidth/1920)+')';}});}}
addEventListener('resize',fit);fit();
addEventListener('keydown',e=>{{if(e.key==='n'||e.key==='N')document.body.classList.toggle('hide-notes');}});
</script></body></html>"""
    out = os.path.join(deck_dir, "preview.html")
    open(out, "w", encoding="utf-8").write(page)
    print("wrote", out)


if __name__ == "__main__":
    main()
