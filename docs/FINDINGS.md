# Findings and numbers (single source of truth)

Every number on the slides, in the speech and in the simulator comes from the pipeline in `code/`. Rerunning it on the same data reproduces `code/results.json` exactly (checked on 21 Nov 2026).

Data: D-004 synthetic household survey, 2023-2024, 8 quarters, 12,000 households, **96,000 household-quarters**, 20 regions. Unweighted (sample estimates, not population estimates).

## Definitions

- **КДН (DSR, debt-service ratio)** = loan repayments in the quarter / household income in the same quarter.
  - Repayments: kv_vopr12 KODNU codes 2.1.1.4.1 and 2.1.1.4.2 (assumed from the data structure; to be checked against the codebook).
  - Income: sum of GR1-GR23 in kv_vopr11, without GR17.
- **New loan:** a loan received in the quarter (KODNU 59-62), with purpose (question 2.1) and source (question 2.2) from kv_vopr12.
- **Basic needs ("еда, лечение, ЖКУ"):** purpose = food, health/medicine or utility arrears.
- **Informal source:** private person or pawnshop.
- **Regulated lender:** commercial bank or MFO. The limit is simulated only for these loans (n = **4,284** new loans).
- **Quintiles (К1 to К5):** per-capita income (household size from D-008), computed within each year and quarter.
- **Blocking rule (static):** a new regulated loan is blocked if the household's КДН in that quarter is above the limit. The new loan's own payment is mostly not yet in that quarter's КДН, so blocking shares are closer to a lower bound.

## Result 1: descriptives

| Indicator | Value |
|---|---|
| Households repaying loans in a quarter | 28.0% |
| Median КДН of repayers | 15.5% |
| Repayers with КДН above 30% | 27.5% |
| Repayers with КДН above 50% | 14.4% (about 1 in 7) |
| Households taking a new loan per quarter | 5.9% |
| New regulated loans already issued above the 50% limit | 11.2% |

Purpose of new loans: consumer durables 51.1%, other 24.6%, food 9.7%, building a house 4.6%, health/medicine 3.6%, buying housing/land 2.9%, education 2.2%, utility arrears 1.0%. Basic needs together: about 14% (1 in 7).

Source of new loans: commercial bank 71.8%, private person 13.5%, MFO 7.7%, other 4.8%, pawnshop 1.8%. Informal together: about 15%.

By quintile (К1 to К5): share of repayers above 50% КДН is 33.1, 14.7, 11.5, 8.0, 4.1%. Median КДН of repayers: К1 30.9%, К5 8.9%.

## Result 2: hypotheses

| # | Hypothesis | Result | Verdict |
|---|---|---|---|
| Г1 | Poorer households carry a heavier debt burden | КДН 37 p.p. lower in К5 than К1 (OLS with region and quarter fixed effects), p<0.001 | Confirmed |
| Г2 | The poor borrow more for basic needs | No difference by quintile (logit), p=0.27 | Not confirmed |
| Г3 | Borrowers for basic needs go more often to private lenders and pawnshops | Odds ratio 3.54 (logit with quintile, urban/rural, year), p<0.001. Raw rates 31.7% vs 11.6% (about 2.7x) | Confirmed |
| Г4 | High КДН lowers life satisfaction (D-002) | -0.03 points, p=0.26 | Not confirmed |

Standard errors clustered by household; on synthetic data they are understated. Synthetic data weakens associations by about half, so the null results for Г2 and Г4 do not prove there is no effect.

**Wording trap:** 3.5 is an odds ratio. Never say "в 3,5 раза чаще". Say "шансы выше в 3,5 раза" or "32% против 12%".

The 37 p.p. gap (mean, from OLS) is larger than the median gap (31% vs 9%) because К1 has a long tail of very low incomes.

## Simulation: flat limits

| КДН limit | All | К1 | К2 | К3 | К4 | К5 |
|---|---|---|---|---|---|---|
| 50% (current) | 11.2 | 25.4 | 11.4 | 8.5 | 5.6 | 2.7 |
| 40% | 14.5 | 30.1 | 15.4 | 11.6 | 8.5 | 4.4 |
| 30% | 19.4 | 34.5 | 22.0 | 15.4 | 13.5 | 8.5 |

% of new regulated loans blocked. At 30%: urban 20.4%, rural 18.0%; less than 1% of all households per quarter (0.86%); 14.5% of new regulated loan volume.

## Scenarios (the main result)

| % of loans | Current 50% | Flat 30% | Targeted | Targeted + social exemption |
|---|---|---|---|---|
| Durables credit cut (% of volume) | 7.9 | 13.4 | **13.4** | 13.3 |
| Food, health, utilities: blocked | 14.0 | 24.2 | **14.2** | **0** |
| Poorest (К1): blocked | 25.4 | 34.5 | **30.2** | 26.5 |
| Total blocked | 11.2 | 19.4 | **15.6** | 13.9 |

- **Targeted:** КДН 30% for consumer-durables loans, 50% for all other loans.
- **Social exemption:** loans for food, health and utility arrears are never blocked.
- Under the flat limit, К1 is blocked about 4 times as often as К5 (34.5 vs 8.5).

Do not confuse two different metrics: "share of basic-needs loans that are blocked" (14.0 / 24.2, from `scenarios.py`) and "share of blocked loans that are for basic needs" (about 15%, `blocked_essential_share` in `results.json`).

## Regions (flat 30%)

Highest blocking: Akmola 32.3%, Aktobe 31.4%, Astana 24.9%. Lowest: Mangystau 10.7%, Almaty region 10.4%. About a 3x spread.

Aktobe: 56% of new loans come from private persons and pawnshops, and 67.5% are for basic needs. Both look like synthetic-data artefacts and must be checked on real data.

Regional employment rate (T-001, ages 15-64) is not related to blocking risk (r = 0.00). T-001 has no key shared with the D series, so it is joined only at region level.

## Policy context used on the slides

- Current rule: КДН at most 50%.
- From 1 Jan 2027: debt-to-income (КДД) limit, total debt at most 8 annual incomes; the regulator (АРРФР) proposed going stricter for unsecured loans (bes.media, May 2026).
- IMF 2025 Article IV concluding statement (Nov 2025): measures should be targeted so that lending does not leave the regulated sector.

## Recommendations (slide 14)

1. Targeted limit instead of a flat one.
2. A channel for basic needs (small social loans or emergency help), so a bank refusal does not lead to a pawnshop.
3. Monitor informal borrowing by region; pilot in Aktobe and Akmola.
4. Check compliance with the current 50% rule (11% of new loans are above it).
5. For the Bureau: add one question on outstanding debt to D-004; without it the 2027 КДД limit cannot be measured.

## Limitations (slide 16)

- Synthetic data: associations weakened by about half, errors understated. Signs are reliable, magnitudes are not.
- Static simulation: no reaction by borrowers or banks; the shift to pawnshops is estimated through Г3, not modelled.
- Payment codes 2.1.1.4.1 and 2.1.1.4.2 assumed to be loan repayments; needs a codebook check.
- No survey weights; food spending (D-003) is not in the archive.
