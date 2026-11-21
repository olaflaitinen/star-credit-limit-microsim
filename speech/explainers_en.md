# Plain-English explainers

## What the project is about

Kazakhstan's regulator wants to tighten the rule on consumer loans. Today, a household's loan payments can't exceed 50% of its income (КДН, the debt-service ratio), and they're considering lowering that to something like 30%. The project asks who gets hurt if they do.

**What we did:** took survey data on 12,000 households (96,000 household-quarters, D-004, 2023-2024) and calculated how much of each family's income goes to loan payments. Then we simulated the stricter limit on about 4,300 new bank and MFO loans to see which ones would be refused.

**What we found:**
- A flat 30% limit hits the poorest hardest. A third of their loans get blocked, against about 8% for the richest.
- Some of those loans are for food and medicine. People refused those loans don't stop needing the money; they're much more likely to go to pawnshops and private lenders.

**What we propose:** a targeted limit. Apply 30% only to loans for appliances and furniture, and keep 50% for everything else. The regulator gets the same cut in consumer credit, and loans for basic needs are blocked no more than today.

**Extras:** a browser simulator where anyone can try different limits, and a plan to add a local AI that turns a policy written in plain words into simulator settings.

**In one line:** a stricter loan limit can reach the regulator's goal without pushing poor families toward pawnshops, if it's targeted.

## What "Займов на еду и лечение заблокировано" means (simulator KPI)

It shows what share of loans for food, medicine or overdue utility bills would be refused under the chosen limit.

That's the cost of the policy. People refused these loans still need the money, so they go to pawnshops and private lenders.

The flat 30% limit pushes it from 14% to 24%. The targeted limit keeps it at 14%, the same as today, and still cuts appliance credit just as much. Adding the social exemption takes it to 0%.

| Scenario | Food/medicine loans blocked | Appliance credit cut (% of volume) |
|---|---|---|
| Today (50%) | 14.0% | 7.9% |
| Flat limit 30% | 24.2% | 13.4% |
| Targeted (30% durables, 50% other) | 14.2% | 13.4% |
| Targeted + social exemption | 0% | 13.3% |

The simulator shows two numbers side by side: "Сокращение кредита на технику" is what the regulator wants; "Займов на еду и лечение заблокировано" is the side effect.

Russian one-liner for the jury: «Это цена меры для людей: какая доля займов на еду и лечение будет отклонена. Наш адресный лимит держит ее на сегодняшнем уровне.»
