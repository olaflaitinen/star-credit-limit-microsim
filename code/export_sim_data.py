"""Export the per-loan arrays that simulator.html embeds as `const D = {...}`.

Usage:
    python3 export_sim_data.py out/reg_new.pkl out/sim_data.json
    python3 export_sim_data.py out/reg_new.pkl out/sim_data.json --inject ../simulator/simulator.html

Keys (one entry per new loan from a bank or MFO, n = 4284):
    dsr  debt-service ratio of the household in that quarter (6 significant digits, capped at 9.999)
    q    income quintile 1-5 (per-capita income, within year and quarter)
    te   region code (TE)
    e    1 if the loan is for basic needs (food, health/medicine, utility arrears)
    u    1 if the loan is for consumer durables (gets the "durables" limit in the simulator)
    a    loan amount in thousands of tenge, rounded

Reconstructed after the datathon from the simulator's embedded data; checked to match it exactly.
"""
import json
import sys

import pandas as pd


def build(reg_new: pd.DataFrame) -> dict:
    r = reg_new
    return {
        "dsr": [float(f"{min(v, 9.999):.6g}") for v in r.dsr],
        "q": r.quintile.astype(int).tolist(),
        "te": r.TE.astype(int).tolist(),
        "e": r.p_essential.astype(int).tolist(),
        "u": r.p_durables.astype(int).tolist(),
        "a": (r.new_amt / 1000).round().astype(int).tolist(),
    }


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    D = build(pd.read_pickle(src))
    with open(dst, "w") as f:
        json.dump(D, f, separators=(",", ":"))
    if "--inject" in sys.argv:
        html_path = sys.argv[sys.argv.index("--inject") + 1]
        html = open(html_path, encoding="utf-8").read()
        start = html.index("const D = ") + len("const D = ")
        _, length = json.JSONDecoder().raw_decode(html[start:])
        html = html[:start] + json.dumps(D, separators=(",", ":")) + html[start + length:]
        open(html_path, "w", encoding="utf-8").write(html)
    print(f"{len(D['dsr'])} loans written to {dst}")


if __name__ == "__main__":
    main()
