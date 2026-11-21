# Data

The raw data is **not** in this package and should **not** be committed to the repo (organisers' synthetic microdata, about 280 MB unpacked). Keep it outside the repo or in a git-ignored `data/raw/`.

## Source

`synthetic_microdata_2021-2024_20260921.zip` (4.4 GB) from STAT.DATATHON-2026 (Bureau of National Statistics of Kazakhstan, synthetic stand-ins for the deidentified survey microdata). The organisers' own README and file manifest are copied to `docs/synthetic_data_README_organisers.md` and `docs/synthetic_data_MANIFEST.csv`. Read point 3 there: cross-form associations are attenuated by about half.

The team worked from a 37.7 MB subset, `datathon_secim.zip` (on the team lead's Desktop), with this layout:

```
synthetic_microdata_2021-2024_20260921/
  README.md  MANIFEST.csv  MANIFEST.json
  d002/2021..2024/subject.csv          life satisfaction (1-10)
  d004/2023/{1kv..4kv}/kv_vopr*.csv    household budget survey, quarterly
  d004/2024/{1kv..4kv}/kv_vopr*.csv
  d006/2021..2024/
  d008/2021..2024/kontr_k.csv          household roster (size, urban/rural)
  t001/2024/baza.csv                   individual labour survey
```

What the code reads:
- `d004/<year>/<q>kv/kv_vopr0.csv`: region (TE), urban/rural
- `kv_vopr11.csv`: income (GR1-GR23, without GR17)
- `kv_vopr12.csv`: loans: purpose (question 2.1, NOMVNEW 21), source (2.2, NOMVNEW 22), repayments (KODNU 2.1.1.4.1, 2.1.1.4.2), new loans (KODNU 59-62)
- `kv_vopr1-7.csv`: non-food spending, health spending
- `d008/<year>/kontr_k.csv`: household size, merged on NOMER
- `d002/<year>/subject.csv`: life satisfaction, merged on NOMER
- `t001/2024/baza.csv`: regional employment, joined only by region (no shared key with the D series)

Gotcha: in the 2021-2023 files of kv_vopr12 there is no NOMVOPR column; split questions with NOMVNEW (21 = purpose, 22 = source) before counting KOD.

The code lists for loan purpose and source are in `docs/d004-form-notes.html`.

## How the subset was made (Windows PowerShell)

1. Schema of the big zip (sizes per folder, three levels deep):

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [IO.Compression.ZipFile]::OpenRead("C:\Users\yunus\Documents\Downloads\synthetic_microdata_2021-2024_20260921.zip")
$rows = $zip.Entries | Where-Object { $_.Name -ne "" } | ForEach-Object {
  $p = $_.FullName -split "[\\/]"
  if ($p.Count -eq 1) { $d = "(kok)" } else { $d = ($p[0..([Math]::Min($p.Count-2,2))]) -join "/" }
  [pscustomobject]@{Dir=$d; Size=$_.Length}
}
$zip.Dispose()
$out = $rows | Group-Object Dir | Sort-Object Name | ForEach-Object {
  "{0,8:N1} MB {1,5} dosya  {2}" -f (($_.Group | Measure-Object Size -Sum).Sum/1MB), $_.Count, $_.Name
}
$out += "TOPLAM {0:N1} MB" -f (($rows | Measure-Object Size -Sum).Sum/1MB)
$desk = [Environment]::GetFolderPath("Desktop")
$out | Set-Content "$desk\zip_sema.txt" -Encoding UTF8
$out | Set-Clipboard
"Hazir: panoya kopyalandi"
```

2. Build `datathon_secim.zip` with only the needed folders:

```powershell
Add-Type -AssemblyName System.IO.Compression, System.IO.Compression.FileSystem
$src  = "C:\Users\yunus\Documents\Downloads\synthetic_microdata_2021-2024_20260921.zip"
$desk = [Environment]::GetFolderPath("Desktop")
$dst  = "$desk\datathon_secim.zip"
$keep = @("d002/","d006/","d008/","d004/2023/","d004/2024/","t001/2024/")
if (Test-Path $dst) { Remove-Item $dst }
$in  = [IO.Compression.ZipFile]::OpenRead($src)
$out = [IO.Compression.ZipFile]::Open($dst, "Create")
foreach ($e in $in.Entries) {
  if ($e.Name -eq "") { continue }
  $n = $e.FullName -replace "\\","/"
  $rel = $n -replace "^synthetic_microdata_2021-2024_20260921/",""
  $ok = ($rel -notmatch "/") -or ($keep | Where-Object { $rel.StartsWith($_) })
  if ($ok) {
    $ne = $out.CreateEntry($n, [IO.Compression.CompressionLevel]::Optimal)
    $s = $e.Open(); $d = $ne.Open(); $s.CopyTo($d); $d.Dispose(); $s.Dispose()
  }
}
$in.Dispose(); $out.Dispose()
"Hazir: {0:N1} MB" -f ((Get-Item $dst).Length/1MB)
```

3. Show it in Explorer: `explorer.exe /select,"$([Environment]::GetFolderPath('Desktop'))\datathon_secim.zip"`
