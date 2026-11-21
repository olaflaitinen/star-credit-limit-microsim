#!/usr/bin/env bash
# Full pipeline. Usage: ./run_all.sh /path/to/synthetic_microdata_2021-2024_20260921 [out_dir]
# Takes about 20 seconds. Reproduces code/results.json exactly.
set -euo pipefail
DATA="${1:?path to synthetic_microdata_2021-2024_20260921}"
OUT="${2:-out}"
mkdir -p "$OUT"
python3 code/build_panel.py "$DATA" "$OUT"            # -> hh_quarter.pkl (96,000 household-quarters)
python3 code/analyze.py "$OUT/hh_quarter.pkl" "$OUT"  # -> results.json, reg_new.pkl (4,284 new regulated loans)
python3 code/extra.py "$DATA" "$OUT"                  # -> adds T-001 regional labour context to results.json
python3 code/scenarios.py "$OUT/reg_new.pkl"          # prints flat vs targeted vs targeted + social exemption
python3 code/export_sim_data.py "$OUT/reg_new.pkl" "$OUT/sim_data.json"   # data embedded in simulator.html
