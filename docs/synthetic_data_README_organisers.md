# Synthetic stand-ins for the deidentified survey microdata

Every file here is SYNTHETIC. No real record appears in any table. The layout
mirrors the deidentified input -- `<form>/<year>[/<quarter>]/<table>.csv` --
and each file keeps its source table's name, so a synthetic table lines up with
the real one by path alone. UTF-8, no BOM.

`MANIFEST.csv` lists every table with its synthetic and real row and column
counts.

## Read this before analysing

These tables are built to reproduce the STRUCTURE of the originals -- schemas,
joinable keys, and over-time structure. They are not a substitute for the real
data, and the following are measured limitations, not suspicions.

1. **Row counts differ slightly from the originals.** Coverage and rows-per-unit
   are MODELLED, not copied: enterprise tables (1-T, 2-T) drift a median
   +0.13%, the rest -0.23%, and 7.9% in the worst single table. A synthetic
   table having exactly as many rows as its source would mean the count had
   been imposed rather than learned.

2. **T-001 ships at 40 of ~154 modellable columns.** The full-width fit needs
   more memory than the machine that produced this has. Every other form ships
   at full width. T-001 is also the only form here with no fidelity score.

3. **Cross-form associations are attenuated by about half.** In the D-series,
   dwelling area on household size reads 0.100 against a real 0.171, and on
   child share -0.020 against -0.128. SIGNS are reproduced in every case
   measured; treat MAGNITUDES as lower bounds.

4. **The 1-T panel keeps about half its real persistence.** Within-firm
   autoregression: 0.488 (headcount) and 0.238 (pay) against a real 0.926 and
   0.792. Over-time structure is present and is weaker than the truth.

5. **2021 D-series: the respondent's age is not tied to the named person.**
   The 2021 roster carries no birth year at all (d008 gained it in 2022), so
   `VOZ` is drawn from household context. It is faithful as a distribution but
   does not agree with the person `NOMP` identifies. 2021 also has no
   household age composition for the same reason.

6. **Standard errors computed on these tables are too small.** One synthetic
   table per original table, with no replicates, so tests are liberal and the
   false-positive rate is elevated. Use these data to develop and scope an
   analysis; estimate the final numbers on the real records.

7. **Value codebooks are missing for D-008, T-001 and 1-T's classifier
   columns.** Those values are unlabelled codes in the source too.

8. **kv_vopr1 (D-004) repeats items within a household** at 15% of rows against
   a real 2.4%.

## What is not here

- **D-001** (time-use diary) is not included. It is a per-person diary of 144
  ten-minute slots per day, which needs a different representation from the
  other forms.
