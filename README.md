# Кредитный лимит: кто проиграет? / Credit limit: who loses?

**Team STAR, STAT.DATATHON-2026, track Data to Policy. 1st place.**

[![checks](https://github.com/olaflaitinen/star-credit-limit-microsim/actions/workflows/checks.yml/badge.svg)](https://github.com/olaflaitinen/star-credit-limit-microsim/actions/workflows/checks.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A household-level microsimulation of tightening Kazakhstan's consumer-credit debt-service limit (КДН, currently 50% of income), using the Bureau of National Statistics' synthetic D-004 household survey (2023-2024). It shows who loses access to credit under a flat 30% limit, and proposes a targeted limit that gives the regulator the same cut in consumer credit without blocking more loans for food and medicine.

**Online:** [project page](https://olaflaitinen.github.io/star-credit-limit-microsim/) | [interactive simulator](https://olaflaitinen.github.io/star-credit-limit-microsim/simulator/simulator.html) | [final deck with speaker notes](https://olaflaitinen.github.io/star-credit-limit-microsim/slides/main_18/preview.html)

## Team

1. **Джафарли Искендер Анар оглы** (Руководитель команды). Университет АДА, Школа информационных технологий и инженерии (SITE), Баку, Азербайджан. ijafarli14955@ada.edu.az
2. **Садыгова Назпери Агали гызы**. Московский государственный университет имени М. В. Ломоносова, Факультет менеджмента, Баку, Азербайджан. sadigova.nazpari@gmail.com
3. **Иманов Юнус Фариз оглы**. Хельсинкский университет, Департамент математики и статистики, Хельсинки, Финляндия. yunus.z.imanov@helsinki.fi

## Key results

Synthetic data: the directions are reliable, the magnitudes are to be confirmed on real data.

- 28% of households repay loans; median КДН of repayers 15.5%; 14.4% of repayers pay more than half their income.
- Regressive burden: 33.1% of repayers in the poorest fifth are above 50% КДН, against 4.1% in the richest (8x).
- Basic-needs borrowers (food, medicine, utility arrears) have 3.5x higher odds of borrowing from private persons and pawnshops (31.7% vs 11.6%).
- A flat 30% limit blocks 19.4% of new bank and MFO loans (now 11.2%): 34.5% for the poorest fifth, 8.5% for the richest, and 24.2% of basic-needs loans (now 14.0%).
- **Targeted limit** (30% for consumer durables, 50% for other loans): the same 13.4% cut in durables credit, with basic-needs loans blocked at 14.2%, the same as today. With a social exemption: 0%.

All numbers, definitions and caveats: [`docs/FINDINGS.md`](docs/FINDINGS.md).

## Method in one paragraph

КДН = loan repayments in a quarter / household income in that quarter (D-004 kv_vopr12 and kv_vopr11, merged on NOMER). Households are ranked into per-capita income quintiles within each quarter. Each of the 4,284 new loans from banks and MFOs is blocked if the household's КДН is above the limit (static rule, no behavioural response). Hypotheses are tested with OLS (region and quarter fixed effects) and logits, standard errors clustered by household. T-001 enters only at region level because it shares no key with the D series.

## Quick start

```bash
pip install -r requirements.txt
bash run_all.sh /path/to/synthetic_microdata_2021-2024_20260921 out
```

The pipeline takes about 20 seconds and reproduces `code/results.json` exactly. The raw data is not in this repository; see [`data/README.md`](data/README.md) for where it comes from and which files the code reads.

Open `simulator/simulator.html` in any browser. The loan data is embedded, so it needs no server; without internet it falls back from the Ubuntu web font to a system font. To rebuild a slide preview:

```bash
python3 slides/build_preview.py main_18   # then open slides/main_18/preview.html
```

## Repository layout

```
README.md                  this file
LICENSE                    MIT (code); fonts keep their own licence
CITATION.cff               how to cite the project
index.html                 project page served by GitHub Pages
run_all.sh                 full pipeline (about 20 s)
requirements.txt
code/                      analysis pipeline (Python: pandas, numpy, statsmodels)
  build_panel.py           D-004 + D-008 + D-002 -> household-quarter panel
  analyze.py               descriptives, hypotheses Г1-Г4, flat-limit simulation -> results.json
  extra.py                 T-001 regional labour context
  scenarios.py             current vs flat 30% vs targeted vs targeted + social exemption
  export_sim_data.py       per-loan arrays embedded in the simulator
  results.json             saved results
  README.md                run notes (Russian)
  _early_versions/         first drafts of build_panel.py and analyze.py (superseded)
simulator/
  simulator.html           final interactive simulator, single self-contained file
  simulator_first_version.html   first version, kept as submitted with the code archive
slides/                    the three decks (HTML sections + deck.json) and previews, see slides/README.md
  main_18/                 the deck presented in the final, with the 7-minute speech in speaker notes
  final_9/  speech_9/      shorter 9-slide versions that were not used
  build_preview.py         builds an offline preview.html for a deck
speech/
  STAR_speech_7min.txt     the speech, plain text, two speakers, timed
  QA_prep_ru.md            31 likely jury questions with Russian answers
  explainers_en.md         the project and the simulator in plain English
docs/
  FINDINGS.md              every number, definition, hypothesis, scenario and limitation
  d004-form-notes.html     organisers' notes on reading D-004 (kv_vopr12, NOMVOPR, GR columns)
  synthetic_data_README_organisers.md, synthetic_data_MANIFEST.csv
data/README.md             where the data comes from, how the subset was cut (data itself not included)
assets/fonts/Ubuntu/       Ubuntu font family used by the slides, with its licence
.github/workflows/         checks run on every push
```

## Limitations

- Payment codes 2.1.1.4.1 and 2.1.1.4.2 are assumed to be loan repayments; this needs the codebook.
- No survey weights.
- The simulation is static: households do not change their behaviour in response to the limit.
- The data is synthetic, and cross-form associations are attenuated by about half.

## Timeline

- 11 Oct 2026: topic chosen, data subset cut, analysis and first deck built.
- 12 Oct 2026: final submission deadline (deck, code, simulator).
- 19-20 Oct 2026: final; 18-slide deck with speech in speaker notes, 7-minute talk with live demo.
- Result: 1st place.

## Roadmap

A local open LLM on GH200 (CSC Roihu) that turns a policy described in plain text into simulator parameters and writes a four-perspective brief from the simulator's numbers only (slide 17). Not built yet.

## Licence

Code and documentation written by the team: [MIT](LICENSE). The Ubuntu fonts in `assets/fonts/Ubuntu/` are under the Ubuntu Font Licence (`UFL.txt`). The files in `docs/` marked as organisers' material belong to the STAT.DATATHON-2026 organisers. The raw microdata is not distributed here.
