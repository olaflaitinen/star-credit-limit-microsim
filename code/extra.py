import sys, json, pandas as pd, numpy as np
root, out = sys.argv[1], sys.argv[2]
R = json.load(open(f"{out}/results.json"))
t = pd.read_csv(f"{root}/t001/2024/baza.csv", dtype=str)
t["age"] = pd.to_numeric(t.vosr, errors="coerce")
w = t[(t.age >= 15) & (t.age <= 64)]
lab = w.groupby("TE").apply(lambda g: pd.Series({
  "emp_rate": round(100*(g.ZAN_RABOTA=="1").mean(),1),
  "no_contract_of_employees": round(100*(g[g.ORB_STATUS=="1"].ORB_TRDDOG=="2").mean(),1),
  "searching": round(100*(g.PSK_RABOTA=="1").mean(),1)})).reset_index()
print(lab.describe())
R["labour_by_TE"] = lab.to_dict("records")
# simulation grid for dashboard
rn = pd.read_pickle(f"{out}/reg_new.pkl")
H = pd.read_pickle(f"{out}/hh_quarter.pkl")
REG = {r["region"]: r["TE"] for r in R["regions"]}
grid = {}
for cap in range(20, 75, 5):
    b = rn.dsr > cap/100
    grid[cap] = {
      "blocked": round(100*b.mean(),1),
      "q": rn.assign(b=b).groupby("quintile").b.mean().mul(100).round(1).tolist(),
      "urban": round(100*b[rn.urban].mean(),1), "rural": round(100*b[~rn.urban].mean(),1),
      "ess": round(100*rn[b].p_essential.mean(),1) if b.any() else 0,
      "dur": round(100*rn[b].p_durables.mean(),1) if b.any() else 0,
      "vol": round(100*rn[b].new_amt.sum()/rn.new_amt.sum(),1),
      "region": rn.assign(b=b).groupby("TE").b.mean().mul(100).round(1).to_dict()}
R["grid"] = grid
json.dump(R, open(f"{out}/results.json","w"), ensure_ascii=False, indent=1, default=str)
print(grid[30]["q"], grid[50]["blocked"])
