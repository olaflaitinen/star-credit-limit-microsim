import sys, json
import pandas as pd, numpy as np
import statsmodels.formula.api as smf

H = pd.read_pickle(sys.argv[1]); out = sys.argv[2]
R = {}
REG = {"10":"Abai","11":"Akmola","15":"Aktobe","19":"Almaty obl.","23":"Atyrau","27":"West Kaz.","31":"Zhambyl",
       "33":"Zhetisu","35":"Karaganda","39":"Kostanay","43":"Kyzylorda","47":"Mangystau","55":"Pavlodar",
       "59":"North Kaz.","61":"Turkistan","62":"Ulytau","63":"East Kaz.","71":"Astana","75":"Almaty city","79":"Shymkent"}
H["region"] = H.TE.map(REG)
pct = lambda s: round(100 * s.mean(), 1)

# ---------- Result 1: descriptives ----------
R["n_hh_quarters"] = len(H)
R["share_repaying"] = pct(H.has_repay)
R["share_newloan"] = pct(H.new_loan)
rp = H[H.has_repay & H.income.gt(0)]
R["dsr_median_repayers"] = round(100 * rp.dsr.median(), 1)
R["repayers_dsr_gt50"] = pct(rp.dsr > .5)
R["repayers_dsr_gt30"] = pct(rp.dsr > .3)
R["by_quintile"] = H.groupby("quintile").apply(lambda g: pd.Series({
    "repaying": pct(g.has_repay),
    "dsr_med_repayers": round(100 * g[g.has_repay & g.income.gt(0)].dsr.median(), 1),
    "dsr_gt50_of_repayers": pct(g[g.has_repay & g.income.gt(0)].dsr > .5),
    "newloan": pct(g.new_loan),
    "essential_of_newloans": pct(g[g.new_loan].p_essential),
    "informal_of_newloans": pct(g[g.new_loan].s_informal),
    "life_sat": round(g.life_sat.mean(), 2)})).reset_index().to_dict("records")
R["by_urban"] = H.groupby("urban").apply(lambda g: pd.Series({
    "repaying": pct(g.has_repay), "newloan": pct(g.new_loan),
    "essential_of_newloans": pct(g[g.new_loan].p_essential),
    "informal_of_newloans": pct(g[g.new_loan].s_informal),
    "dsr_gt50_of_repayers": pct(g[g.has_repay & g.income.gt(0)].dsr > .5)})).reset_index().to_dict("records")
NL = H[H.new_loan]
PUR = {"1":"Build house","2":"Buy housing/land","3":"Food","4":"Start business","5":"Education",
       "6":"Consumer durables","7":"Health/medicine","8":"Utility arrears","9":"Other"}
SRC = {"1":"Microcredit org.","2":"Commercial bank","3":"SME fund","5":"Intl. org.","6":"Edu. fin. centre",
       "7":"Private person","8":"Pawnshop","9":"Other"}
def explode(col, m):
    s = NL[col].dropna().str.split(",").explode()
    return (s.map(m).value_counts(normalize=True) * 100).round(1).to_dict()
R["purpose_dist"] = explode("purpose", PUR)
R["source_dist"] = explode("source", SRC)

# ---------- Result 2: hypotheses ----------
H["dsr_c"] = H.dsr.clip(upper=2)
H["lninc"] = np.log1p(H.income_pc)
m1 = smf.ols("dsr_c ~ C(quintile) + urban + C(TE) + C(GOD):C(KVARTAL)",
             data=H[H.has_repay & H.income.gt(0)]).fit(cov_type="cluster", cov_kwds={"groups": H[H.has_repay & H.income.gt(0)].NOMER})
m2 = smf.logit("p_essential ~ C(quintile) + urban + C(GOD)", data=NL.assign(p_essential=NL.p_essential.astype(int))).fit(disp=0)
NL2 = NL.assign(infml=NL.s_informal.astype(int), ess=NL.p_essential.astype(int))
m3 = smf.logit("infml ~ ess + C(quintile) + urban + C(GOD)", data=NL2).fit(disp=0)
hy = H[H.life_sat.notna() & H.income.gt(0)].copy()
hy["dsr_hi"] = (hy.dsr > .5).astype(int)
m4 = smf.ols("life_sat ~ dsr_hi + has_repay + lninc + urban + C(TE) + C(GOD)", data=hy.assign(has_repay=hy.has_repay.astype(int))).fit(
    cov_type="cluster", cov_kwds={"groups": hy.NOMER})
def co(m, k): return {"coef": round(float(m.params[k]), 3), "p": round(float(m.pvalues[k]), 4)}
R["H1_dsr_q1_vs_q5"] = {"Q2": co(m1, "C(quintile)[T.2]"), "Q3": co(m1, "C(quintile)[T.3]"),
                         "Q4": co(m1, "C(quintile)[T.4]"), "Q5": co(m1, "C(quintile)[T.5]"),
                         "rural_vs_urban(urban coef)": co(m1, "urban[T.True]")}
R["H2_essential_logit"] = {"Q5": co(m2, "C(quintile)[T.5]"), "urban": co(m2, "urban[T.True]")}
R["H3_informal_given_essential"] = {"ess": co(m3, "ess"), "OR": round(float(np.exp(m3.params["ess"])), 2)}
R["H4_lifesat_dsr50"] = {"dsr_hi": co(m4, "dsr_hi"), "has_repay": co(m4, "has_repay")}

# ---------- Policy simulation ----------
# Rule applies to regulated lenders (banks, MFOs). A new regulated loan is blocked if borrower's DSR > cap.
reg_new = NL[NL.s_regulated & NL.income.gt(0)].copy()
sims = {}
for cap in [0.5, 0.4, 0.3]:
    b = reg_new.dsr > cap
    blocked = reg_new[b]
    sims[str(int(cap * 100))] = {
        "blocked_share_of_regulated_newloans": pct(b),
        "blocked_hh_share_of_all_hh": round(100 * b.sum() / len(H), 2),
        "blocked_essential_share": pct(blocked.p_essential) if len(blocked) else 0,
        "blocked_durables_share": pct(blocked.p_durables) if len(blocked) else 0,
        "blocked_by_quintile": reg_new.assign(b=b).groupby("quintile").b.mean().mul(100).round(1).to_dict(),
        "blocked_by_urban": reg_new.assign(b=b).groupby("urban").b.mean().mul(100).round(1).to_dict(),
        "blocked_by_region": reg_new.assign(b=b).groupby("region").b.mean().mul(100).round(1).sort_values(ascending=False).to_dict(),
        "blocked_newloan_volume_share": round(100 * blocked.new_amt.sum() / max(reg_new.new_amt.sum(), 1), 1),
        "blocked_durables_volume_kzt_per_quarter": round(blocked[blocked.p_durables].new_amt.sum() / 8),
    }
R["sim"] = sims
# who already borrows above 50% (current rule)? -> evidence of leakage
R["regulated_newloans_dsr_gt50_now"] = pct(reg_new.dsr > .5)
R["n_regulated_newloans"] = len(reg_new)

# region table for dashboard
reg = H.groupby("region").apply(lambda g: pd.Series({
    "TE": g.TE.iloc[0], "hh_q": len(g), "repaying": pct(g.has_repay),
    "dsr_gt50_of_repayers": pct(g[g.has_repay & g.income.gt(0)].dsr > .5),
    "newloan": pct(g.new_loan),
    "essential_of_newloans": pct(g[g.new_loan].p_essential),
    "informal_of_newloans": pct(g[g.new_loan].s_informal),
    "income_pc_med": round(g.income_pc.median()), "life_sat": round(g.life_sat.mean(), 2)})).reset_index()
R["regions"] = reg.to_dict("records")
reg_new.to_pickle(f"{out}/reg_new.pkl")
json.dump(R, open(f"{out}/results.json", "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in R.items() if k != "regions"}, ensure_ascii=False, indent=1, default=str))
