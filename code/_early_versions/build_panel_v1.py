"""Build household-quarter panel from D-004 (2023-2024) + D-008 + D-002.
Usage: python3 -I build_panel.py <data_root> <out_dir>
"""
import sys, glob, os
import pandas as pd
import numpy as np

root, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
rd = lambda f: pd.read_csv(f, dtype=str)
num = lambda s: pd.to_numeric(s, errors="coerce").fillna(0)

REPAY = {"2.1.1.4.1", "2.1.1.4.2"}          # assumed: loan repayments (low link to purpose/source rows)
NEWLOAN = {"59", "60", "61", "62"}           # assumed: borrowed funds received
GR = [f"GR{i}" for i in range(1, 24) if i != 17]  # GR17 excluded: rare, extreme (median 18M), likely asset sale

frames = []
for y in ["2023", "2024"]:
    for q in ["1kv", "2kv", "3kv", "4kv"]:
        p = f"{root}/d004/{y}/{q}"
        base = rd(f"{p}/kv_vopr0.csv")[["NOMER", "TE", "K", "KVARTAL", "GOD"]]
        inc = rd(f"{p}/kv_vopr11.csv")
        inc["inc"] = inc[GR].apply(num).sum(axis=1)
        inc_h = inc.groupby("NOMER").agg(income=("inc", "sum"),
                                         earners=("inc", lambda s: (s > 0).sum())).reset_index()
        spend = []
        for t in ["kv_vopr1", "kv_vopr2", "kv_vopr3", "kv_vopr4", "kv_vopr5", "kv_vopr6", "kv_vopr7"]:
            d = rd(f"{p}/{t}.csv")
            d["v"] = num(d["STOIMK"])
            spend.append(d.groupby("NOMER")["v"].sum().rename(t))
        spend = pd.concat(spend, axis=1).fillna(0)
        spend["nonfood_spend"] = spend.sum(axis=1)
        L = rd(f"{p}/kv_vopr12.csv")
        L["v"] = num(L["STOIMK"])
        it = L[L.NOMVNEW == "20"]
        repay = it[it.KODNU.isin(REPAY)].groupby("NOMER")["v"].sum().rename("repay")
        newamt = it[it.KODNU.isin(NEWLOAN)].groupby("NOMER")["v"].sum().rename("new_amt")
        pur = L[L.NOMVNEW == "21"].groupby("NOMER")["KOD"].agg(lambda s: ",".join(sorted(set(s)))).rename("purpose")
        src = L[L.NOMVNEW == "22"].groupby("NOMER")["KOD"].agg(lambda s: ",".join(sorted(set(s)))).rename("source")
        h = (base.merge(inc_h, on="NOMER", how="left")
                 .merge(spend[["nonfood_spend", "kv_vopr5"]].rename(columns={"kv_vopr5": "health_spend"}),
                        left_on="NOMER", right_index=True, how="left")
                 .merge(repay, left_on="NOMER", right_index=True, how="left")
                 .merge(newamt, left_on="NOMER", right_index=True, how="left")
                 .merge(pur, left_on="NOMER", right_index=True, how="left")
                 .merge(src, left_on="NOMER", right_index=True, how="left"))
        for c in ["income", "earners", "nonfood_spend", "health_spend", "repay", "new_amt"]:
            h[c] = h[c].fillna(0)
        frames.append(h)

H = pd.concat(frames, ignore_index=True)
H["GOD"] = H.GOD.astype(int); H["KVARTAL"] = H.KVARTAL.astype(int)

# household size from D-008 (annual)
sz = []
for y in ["2023", "2024"]:
    d8 = rd(f"{root}/d008/{y}/kontr_k.csv")
    s = d8.groupby("NOMER")["KOL_CHL"].first().astype(int).rename("hh_size").reset_index()
    sz.append(s)
H = H.merge(pd.concat(sz), on="NOMER", how="left")
H["hh_size"] = H.hh_size.fillna(H.hh_size.median())

H["income_pc"] = H.income / H.hh_size
H["quintile"] = H.groupby(["GOD", "KVARTAL"]).income_pc.transform(
    lambda s: pd.qcut(s.rank(method="first"), 5, labels=[1, 2, 3, 4, 5])).astype(int)
H["has_repay"] = H.repay > 0
H["dsr"] = np.where(H.income > 0, H.repay / H.income, np.nan)
H["new_loan"] = H.purpose.notna()
pset = lambda codes: H.purpose.fillna("").apply(lambda s: any(c in s.split(",") for c in codes))
sset = lambda codes: H.source.fillna("").apply(lambda s: any(c in s.split(",") for c in codes))
H["p_essential"] = pset(["3", "7", "8"])      # food, health, utility arrears
H["p_durables"] = pset(["6"])
H["s_bank"] = sset(["2"])
H["s_mfo"] = sset(["1"])
H["s_informal"] = sset(["7", "8"])            # private person, pawnshop
H["s_regulated"] = sset(["1", "2"])
H["urban"] = H.K == "1"

# D-002 life satisfaction (GR1, 1-10; 89 = no answer), household mean
sat = []
for y in ["2023", "2024"]:
    s = rd(f"{root}/d002/{y}/subject.csv")
    s["g"] = pd.to_numeric(s.GR1, errors="coerce")
    s = s[(s.g >= 1) & (s.g <= 10)]
    sat.append(s.groupby("NOMER").g.mean().rename("life_sat").reset_index())
H = H.merge(pd.concat(sat), on="NOMER", how="left")

H.to_parquet(f"{out}/hh_quarter.parquet", index=False)
print(H.shape)
print(H.describe(include="all").T[["count", "mean", "50%"]].to_string())
