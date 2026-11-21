# Slides

Three decks, all in Russian, built as HTML slide sections with a `deck.json` manifest.

| Folder | Title | Slides | Status |
|---|---|---|---|
| `main_18/` | Кредитный лимит: кто проиграет | 18 | **The deck presented in the final (20 Oct 2026).** Speech in the speaker notes, timed for 7 minutes. |
| `final_9/` | STAR: финал | 9 | Shorter redesign (sky and gold style). The team chose the 18-slide deck instead. |
| `speech_9/` | STAR: финал, текст выступления | 9 | Speech pages for `final_9` (slide image plus text). Superseded by the speaker notes in `main_18`. |

Online previews (GitHub Pages):
- main_18: https://olaflaitinen.github.io/star-credit-limit-microsim/slides/main_18/preview.html
- final_9: https://olaflaitinen.github.io/star-credit-limit-microsim/slides/final_9/preview.html
- speech_9: https://olaflaitinen.github.io/star-credit-limit-microsim/slides/speech_9/preview.html
- simulator: https://olaflaitinen.github.io/star-credit-limit-microsim/simulator/simulator.html

## Format

- `deck.json`: title, `order` (slide ids), `sections`, `faces` (fonts as uploaded blobs).
- `slides/<id>.html`: exactly one `<section>`, a fixed 1920x1080 canvas, inline styles only. The speaker notes are the `<aside>` (last child).
- `assets/`: images that slides reference as `/_blob/<id>`. `main_18` has the simulator screenshot; `final_9` has the simulator screenshot and three 10x10 grid SVGs ("35 из 100", "24 из 100", "14 из 100"). The nine images of `speech_9` (thumbnails of the `final_9` slides) were not exported, so its preview shows the text only.

## Preview offline

```
python3 slides/build_preview.py main_18     # writes slides/main_18/preview.html
```

Open `preview.html` in a browser; press N to hide or show the notes. The preview is close but not pixel-exact: table padding and `<x-icon>` icons come from the original slide editor and are missing here.

## Design rules the team set

- Fonts: Ubuntu and Ubuntu Medium only, for text **and** numbers (Mozilla Headline was tried and dropped: it has no Cyrillic, so it is not included).
- Palette (main_18): purple-shifted Google colours. Dark #1E1847, light #F7F5FB, purple-blue #4F46C8 / #6C63F0, magenta #B0306A / #C8336B / #E0457B, amber #F6B24A, teal #1F9C86 / #2BB39A.
- No em dashes, no emoji.
- Nothing may overlap or run off the slide.
- Affiliations exactly as in the top-level `README.md`; Nazpari is in Baku, not Moscow.

## main_18 slide order and timing (7 minutes)

| # | id | Content | Speaker, time |
|---|---|---|---|
| 1 | cover | Title, team, affiliations | 1, 0:00-0:15 |
| 2 | summary | Three findings for the regulator | 1, 0:15-0:45 |
| 3 | context | Policy context: 50% КДН, 2027 КДД limit, IMF | 1, 0:45-1:10 |
| 4 | data | Data and method | 1, 1:10-1:30 |
| 5 | r1 | Descriptives: 28% repay, median КДН 15.5% | 1, 1:30-1:50 |
| 6 | r1b | Loan purpose and source | 1, 1:50-2:10 |
| 7 | hyp | Four hypotheses, two confirmed | 1, 2:10-2:30 |
| 8 | h1 | Г1: 33.1% vs 4.1% above 50% | 1, 2:30-2:55 |
| 9 | h3 | Г3: odds ratio 3.5 (handover) | 1, 2:55-3:20 |
| 10 | sim | Flat limits by quintile | 2, 3:20-3:50 |
| 11 | persp | Four perspectives | 2, 3:50-4:15 |
| 12 | regions | Region tile map | 2, 4:15-4:35 |
| 13 | target | Targeted limit (main result) | 2, 4:35-5:10 |
| 14 | recs | Five recommendations | 2, 5:10-5:40 |
| 15 | demo | Live simulator demo | 2, 5:40-6:15 |
| 16 | limits | Limitations | 2, 6:15-6:30 |
| 17 | roadmap | Next step: local LLM layer | 2, 6:30-6:45 |
| 18 | team | Thank you, contacts | 2, 6:45-6:50 |
