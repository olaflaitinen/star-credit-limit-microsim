"""Сравнение сценариев лимита КДН: единый vs адресный.
Usage: python3 scenarios.py out/reg_new.pkl
"""
import sys, pandas as pd
rn = pd.read_pickle(sys.argv[1])
def run(cap_dur, cap_other, exempt_essential):
    cap = rn.p_durables.map({True: cap_dur, False: cap_other}) / 100
    b = rn.dsr > cap
    if exempt_essential: b &= ~rn.p_essential
    q = rn.assign(b=b).groupby("quintile").b.mean() * 100
    return {"всего": round(100 * b.mean(), 1),
            "кредит на технику, % объема": round(100 * rn[b & rn.p_durables].new_amt.sum() / rn[rn.p_durables].new_amt.sum(), 1),
            "еда/лечение/ЖКУ блок, %": round(100 * (b & rn.p_essential).sum() / rn.p_essential.sum(), 1),
            "К1": round(q[1], 1), "К5": round(q[5], 1)}
for name, args in {"Действующий 50%": (50, 50, False), "Единый 30%": (30, 30, False),
                   "Адресный": (30, 50, False), "Адресный + соцзащита": (30, 50, True)}.items():
    print(name, run(*args))
