# Data contract — Auerbach (1913) cities + mountains

v1.0.0 — 2026-09-01 (Kimi, Stage 0). Versioned like axtell-zipf-susb's
`data/CONTRACT.md`: sources, required fields, custody rules, assertions. Sources
are *candidates vetted at Stage 0*, not yet landed; landing them is Stage 1–3 work,
and each landed source gets a dated addendum with retrieval date, byte size, and
SHA-256. Raw files are preserved unchanged under `data/raw/<source>/`; derived
tables under `data/derived/` must be reproducible from raw + code.

## Custody rules (all sources)

1. Raw files immutable after ingest; manifest with URL, retrieval date, bytes, SHA-256.
2. Every derived table regenerable by `src/` code alone; asserted invariants per table.
3. Encoding: UTF-8, LF; any transcription from the scan is double-entered (prereg §3.1).
4. Licensing/ToS checked *before* ingest and recorded in the manifest row.

## DC-1 — Stage 1 (historical)

| ID | Data | Candidate source | Required fields | Status |
|---|---|---|---|---|
| DC-1a | Auerbach Tables 1–3 (94 German places; 12 countries; 6 Prussian provinces; Europe complex) | Scan in `paper/` (in-container) | place, rank, E.Z. (thousands), printed A.K. | staged (scan present) |
| DC-1b | Full 1910 German census place list (≥10,000 and ≥20,000 cutoffs; 481/236 places) for AU-C3 + AU-C8 | Gemeindeverzeichnis 1910 digitizations (e.g. Deutsche Digitale Bibliothek / library scans); fallback: marked unverifiable per prereg §3.5 | place, population 1910 (also 1895/1900/1905 for the time-series limb if obtainable) | open |
| DC-1c | Saibante 1928 17-country underlying census counts | Metron 7(2) scan (archive.org or library) + the national censuses Saibante cites, 1911–1925 | city, population, country, census year | open |
| DC-1d | Lotka 1925 US city data (EXT-C3, optional) | *Elements of Physical Biology*, public domain (archive.org) | city, population, census year | open |

## DC-2 — Stage 2 (modern cities)

| ID | Data | Candidate source | Required fields | Status |
|---|---|---|---|---|
| DC-2a | Modern German municipality populations | Destatis GENESIS-Online (Gemeindeverzeichnis / "Gebiet und Bevölkerung") | Amtlicher Gemeindeschlüssel, name, population, reference date, area | open |
| DC-2b | Modern counterparts of Auerbach's other 11 complexes | Eurostat (LAU/cities) for EU members; national census tables elsewhere; compiled fallback: citypopulation.de (licensing checked first) | place, population, date, definition level | open |
| DC-2c | Topographic-definition layer | Eurostat/OECD Functional Urban Areas (FUA) | FUA id, population, member municipalities | open |
| DC-2d | Multi-decade German municipal series (AU-C8 modern analog, optional) | Destatis time series / historical-statistical compilations | as DC-2a, per decade | open |

Boundary decisions for defunct complexes (Austria-Hungary, European Russia in 1913
borders, British India) are documented per country *before* fitting (prereg §4.1).

## DC-3 — Stage 3 (mountains)

| ID | Data | Candidate source | Required fields | Status |
|---|---|---|---|---|
| DC-3a | Global ultra-prominence list (P ≥ 1,500 m) | peaklist.org ultras; fallback: Wikipedia "List of Ultras" (CC-BY-SA) | summit, elevation m, prominence m, range, coordinates | open |
| DC-3b | Regional prominence lists: Alps, Himalayas, Rockies | peaklist.org regional lists; peakbagger (ToS check mandatory — no scraping if prohibited; manual export or fallback to Wikipedia lists) | as DC-3a | open |
| DC-3c | Elevation-only deep list (sensitivity arm) | Scaruffi-style compiled lists / Wikipedia lists of highest mountains; Miškinis 2011's 548-summit list as historical comparator | summit, elevation m | open |

Coverage notes (prereg §5.4): prominence lists are climbing-community products —
climbed peaks overrepresented, remote ranges underrepresented. The sweep across
prominence thresholds and the per-list coverage note are part of the deliverable,
not fine print.

## Assertion sketches (to be instantiated on landing)

- DC-1a: 94 rows; printed A.K. = round(rank × E.Z. / 100) within ±1 unit (rounding
  conventions recorded); Berlin is rank 1.
- DC-2a: sum of municipality populations = national total per Destatis (exact match).
- DC-3a: prominence ≤ elevation for every row; Everest elevation 8848.86 m present;
  duplicate-detection on coordinates within 1 km.

## Addendum 1 — 2026-09-02 (Kimi, Stage 1)

- **DC-1a landed.** Tables 1–3 + Europe-complex + Tafel-14 annotations transcribed by
  double entry (pass A: pre-existing OCR markdown; pass B: fresh manual reading of the
  scan at native resolution). One cell corrected against both prior passes: Table 2
  Schweiz A.K. **2,8** (pass A and Ciccone print 2,6 — glyph and arithmetic evidence
  in `results/stage1-transcription-diff.md`). Derived CSVs + SHA-256 manifest in
  `data/derived/`.
- **DC-1c partially landed.** Saibante 1928 (Metron 7(2)) retrieved 2026-09-02 from
  https://ebiblio.istat.it/digibib/Metron/MetronV7N2_1928.pdf (3,100,716 bytes,
  SHA-256 e1a2082dd710bc7ad629a6fec78cb0ece600669c21da72273d9f67fd41f46b64), stored
  at `data/raw/saibante-1928/MetronV7N2_1928.pdf`. The 17-country α table (p. 59)
  transcribed to `data/derived/saibante-1928-alpha.csv`. The **underlying era census
  city counts are not landed** — the re-fit is data-blocked for all 17 countries this
  stage; per-country census tables (1920–1925) are the retrieval target for a later
  session.
- **DC-1b not landed** (budget-capped, prereg §3.5 invoked for AU-C3). Retrieval path
  identified for a later session: Statistik des Deutschen Reichs Bd. 240 (1915),
  Anhang pp. 2 ff. ("Gemeinden mit mehr als 2.000 Einwohnern", systematic +
  alphabetical); possible machine-readable shortcut: GESIS dbk study 67930 (compiled
  Gemeinde-level series 1867–1910 from exactly these tables; registration wall);
  Schubert's gemeindeverzeichnis.de survives only in the Wayback Machine (per-Kreis
  HTML, hundreds of pages — a crawl, not a fetch).
- **EXT-C3 (Lotka)** skipped per the work order's "skip rather than rush".
- **Source note for EXT-C1:** the local Ciccone PDF (Mannheim Feb-2021 version)
  contains only Auerbach's Figures 1–3; the translator-added OLS figure (−1.15, robust
  SE 0.03, receipt D1b) is in the EPB published version
  (doi:10.1177/23998083221147139), not on disk here.

## Addendum 2 — 2026-09-02 (Qoder, Stage 2)

DC-2a/2b/2c landed. Raw under `data/raw/modern-2026-09-02/`, derived tables
`data/derived/modern-*.csv` (in `MANIFEST.sha256`). Retrieval 2026-09-02.

| File | Bytes | SHA-256 | Licence / source |
|---|---|---|---|
| eurostat-urb_cpop1.json | 10,120,263 | 09651cfa…e438 | Eurostat open API, dataset `urb_cpop1` (city populations); Eurostat reuse policy (free with source attribution) |
| eurostat-urb_lpop1.json | 7,630,065 | 85b1fcb7…df3 | Eurostat open API, dataset `urb_lpop1` (functional urban areas); same policy |
| wikipedia-us.wiki | 142,945 | 29819e35…5729 | Wikipedia wikitext, CC-BY-SA 4.0 (List of United States cities by population; Census Bureau estimates 2025-07-01) |
| wikipedia-ru.wiki | 56,496 | 05597182…617c | Wikipedia wikitext, CC-BY-SA 4.0 (2021 census) |
| wikipedia-in.wiki | 86,849 | c6b3238c…a6e2 | Wikipedia wikitext, CC-BY-SA 4.0 (2011 census) |
| wikipedia-at.wiki | 167,645 | 4f5de2a2…91b4 | Wikipedia wikitext, CC-BY-SA 4.0 (Statistik Austria 2024) |

National populations: Eurostat `demo_pjan` (sex=T, age=TOTAL) fetched per country at its
city reference year (NL/BE/CH/DE/IT/FR/ES/HU/UK); World Bank `SP.POP.TOTL` (CC-BY 4.0) at
the city reference year for US (2024 vs city 2025 — one-year mismatch, recorded), RU (2021),
IN (2011), AT (2024). Values in `modern-national-pop.csv` with year + source per row.

**Reference years and thresholds (recorded before fitting, per plan §2):** DE 2025 (149
cities ≥ 50 k; 89 FUAs), NL 2024, BE 2024, CH 2025, IT 2025, FR 2022, ES 2024, HU 2024,
UK 2018, US 2025, RU 2021, IN 2011, AT 2024. Twelve-country table uses a **common
threshold of 100,000** for cross-country comparability; Germany additionally reported at
50,000 to mirror Table 1. Auerbach's own twelve-country table is topographic (p. 75), so the
modern administrative arm is a downward-biased counterpart; the FUA arm is the like-for-like
one (available for DE and the Eurostat countries).

**Deviations from the Stage-0 candidate list (reasons):** Destatis GENESIS downloads are
account-walled, so DC-2a uses Eurostat `urb_cpop1` (administrative city core, official) with
the Wikipedia municipal list retained only as a cross-check source of record; citypopulation.de
was not used (not needed once Eurostat + Wikipedia covered all twelve successors); AT city
series in Eurostat is stale (2014) so AT comes from Wikipedia/Statistik Austria; the US table
contains 350 data rows against the article's stated 348 — the article's lead/footer count is
stale; all 350 verified row-level against the raw wikitext (audit F5). DC-2d (multi-decade
series) not landed: AU-C8 modern analog reported open.

**Addendum 2 amendment — 2026-09-02 (Kimi, audit corrections F1–F4/F6, user-approved):**

- `modern-de-admin.csv`, `modern-cities-12.csv`, `modern-national-pop.csv` regenerated by the
  newly landed raw→derived parser `src/stage2_parse_raw.py` (audit F2); corrected change set:
  DE admin now the true 2025 cross-section (n = 131); AT main-table only (n = 6, year 2025);
  IN artifact rows removed (n = 339); AT national pop to 2025. Full record in
  `results/stage2-summary.md` § Correction record.
- National-population pulls now have raw custody (audit F6), retrieved 2026-09-02:

  | File | Bytes | SHA-256 | Licence / source |
  |---|---|---|---|
  | eurostat-demo_pjan.json | 3,361 | b9c07c29…e73d | Eurostat open API, `demo_pjan` (sex=T, age=TOTAL; 9 geos × 2018/2022/2024/2025); Eurostat reuse policy |
  | worldbank-SP.POP.TOTL.json | 12,122 | f1f365a8…5002 | World Bank `SP.POP.TOTL` (US/RU/IN/AT, 2011–2025); CC-BY 4.0 |

## Addendum 3 — 2026-09-02 (Qoder, Stage 3 mountains; katflow #989)

**DC-3a/b/c landed.** Raw under `data/raw/mountains-2026-09-02/` (immutable after ingest;
22 files, machine-readable custody in `_manifest.json` there — URL, retrieval timestamp,
revid, bytes, SHA-256 per file). Retrieved 2026-09-02T22:13:27Z. Licence:
CC-BY-SA 4.0 (Wikipedia wikitext via the MediaWiki `action=parse` API) and CC0 (Wikidata
SPARQL snapshot). Derived tables are regenerated only by `src/stage3_parse_raw.py`
(contract rule 2, as enforced since the Stage-2 audit F2); parse diagnostics and every
assertion result land in `results/stage3-parse-report.txt`.

| File | Bytes | SHA-256 | revid | index-stated count |
|---|---|---|---|---|
| list-of-ultras-of-africa.wiki | 8,941 | bd2716e1...2960 | 1368216705 | 84 |
| list-of-ultras-of-antarctica.wiki | 5,150 | ecf8358c...fb36 | 1209857984 | 41 |
| list-of-ultras-of-central-asia.wiki | 7,950 | de07e245...6bae | 1338368062 | 75 |
| list-of-ultra-prominent-peaks-of-japan.wiki | 2,429 | b462cd53...8303 | 1261252933 | 21 |
| list-of-ultras-of-northeast-asia.wiki | 5,215 | 3d5fc44c...a851 | 1303712446 | 51 |
| list-of-ultras-of-southeast-asia.wiki | 7,104 | ff005b63...2a64 | 1253769785 | 42 |
| list-of-ultras-of-the-himalayas.wiki | 8,674 | 00a7dfe5...bdc4 | 1340133505 | 76 |
| list-of-ultras-of-the-karakoram-and-hindu-kush.wiki | 5,990 | e9477f4b...c387 | 1232240339 | 61 |
| list-of-ultras-of-the-malay-archipelago.wiki | 14,438 | 53d9e1c0...ef1e | 1369448150 | 91 |
| list-of-ultras-of-the-philippines.wiki | 3,382 | 211fef71...e783 | 1264527034 | 29 |
| list-of-ultras-of-tibet-east-asia-and-neighbouring-areas.wiki | 11,806 | 24b92e0f...4fc3 | 1368659005 | 112 |
| list-of-ultras-of-west-asia.wiki | 12,313 | 973adfff...b09c | 1358690304 | 88 |
| list-of-european-ultra-prominent-peaks.wiki | 24,819 | 0b1c3c60...a978 | 1350185670 | 120 |
| list-of-ultras-of-north-america.wiki | 200,098 | 3f5502f4...397c | 1329110872 | 356 |
| list-of-ultras-of-oceania.wiki | 13,234 | 9721193b...255a | 1367878817 | 69 |
| list-of-ultras-of-south-america.wiki | 19,006 | 51586b69...5f0f | 1329268903 | 211 |
| ultra-prominent-peak.wiki | 7,198 | 6d1a8263...65d2 | 1355687063 | 1516 |
| list-of-alpine-peaks-by-prominence.wiki | 10,196 | 595af34a...90af | 1339033889 | 44 |
| list-of-mountain-peaks-by-prominence.wiki | 39,787 | a9168fff...7c29 | 1369929025 | 125 |
| list-of-highest-mountains-on-earth.wiki | 56,629 | e43ab3a3...bed0 | 1371921577 | - |
| most-prominent-mountain-peaks-of-the-rocky-mountains.wiki | 73,055 | f3a30ba9...1854 | 1351055327 | - |
| wikidata-p2660-ge1500.json | 1,033,092 | 980cd7d8...72e9 | - | - |

**Source decisions (deviation D6).** peaklist.org — the contract's named DC-3a primary —
was unreachable (HTTPS connection failure on both `www.` and the bare host; HTTP 404), and
peakbagger.com returned HTTP 403 for its own terms page, so the contract's mandatory ToS
check could not be satisfied and it was not scraped. The contract's own fallback
(Wikipedia ultra lists, CC-BY-SA) is therefore the DC-3a primary. Miškinis's 548-summit
Scaruffi list is not obtainable (scaruffi.com 404), so DC-3c's historical comparator
stays open (deviation D7); the elevation-only arm uses Wikipedia's
"List of highest mountains on Earth" instead.

**Landed tables (row counts are the parser's, asserted per article against the index).**

| ID | Derived file | Rows | Membership rule |
|---|---|---|---|
| DC-3a | mountains-global-ultras.csv | 1,522 | prominence >= 1,500 m, union of 16 Wikipedia ultra lists, de-duplicated on resolved link target |
| DC-3b | mountains-alps.csv | 44 | prominence >= 1,500 m, `List of Alpine peaks by prominence` |
| DC-3b | mountains-himalayas.csv | 77 | prominence >= 1,500 m, `List of ultras of the Himalayas` (incl. Sino-Nepal provinces) |
| DC-3b | mountains-rockies.csv | 36 | prominence >= 1,500 m, the NA article's Canadian Rockies (19) + US Rocky Mountains (17) sub-tables |
| DC-3c | mountains-highest-by-elevation.csv | 120 | elevation-ordered (108 ranked summits + 12 rows the source flags "S" as sub-prominences) |
| cross-check | mountains-wikidata-crosscheck.csv | 1,543 | Wikidata `P2660 >= 1500` distinct QIDs; **not fitted** (see below) |

**Integrity results.** `Ultra-prominent peak` (revid 1355687063) states a world total of
**1,516** ultras with a per-list index; the parsed, de-duplicated union is **1,522**
(+6, inside the pre-frozen tolerance [1490, 1540] in `results/stage3-plan.md` §3 A4).
Everest is present (A2) at **8,848 m** — the lists carry the rounded value, not the
contract's 8,848.86 m; recorded, not corrected. Coordinate-based duplicate detection
(A3-ii) runs on the 440 A0 rows that carry coordinates and finds no pair within 1 km; on
the Wikidata set it finds 10 such pairs (adjudicated individually in the parse report:
Vinson Massif/Mount Vinson and Nun-Kun Massif/Nun are duplicate items, Serra
Dolcedorme/Pollino and Kawaikini/Mount Waialeale are genuinely distinct summits).

**Wikidata is a cross-check, not a fitted arm (deviation D8).** The SPARQL pull is
unit-contaminated: 276 QIDs carry an impossible elevation (max 16,390 m), 95 carry
prominence above elevation (feet ingested as metres), 73 have no elevation at all. Only
1,085 of 1,543 pass assertion A1. Cleaning it would require per-row judgment about which
value is right — the un-asserted-decision class the Stage-2 audit punished — so it is
reported, not fitted.

**Known source discrepancies recorded, not hidden (deviation D5).** The North America
master table's own caption says 353 summits where the index says 356; Asia's ten lists sum
to 646 against a stated 635; per-article deltas against the index range from −2 (South
America) to +14 (West Asia) and are printed line by line in `results/stage3-parse-report.txt`.
Two range sub-tables in the North America article emit region and mountain range in a
single cell, i.e. their rows are one cell shorter than their header; the parser applies a
documented *structural* repair (never a value-driven one) and reports it. One Himalaya row
(Khyarisatam) has an empty prominence cell in the source and is dropped under A6, named in
the report. The `range` field exists row-level only for 535 of 1,522 A0 rows (deviation D1).

## Addendum 4 — Ciccone source-version reconciliation

Retrieved and inspected 2026-09-03. Both source PDFs remain private under the ignored
`paper/` directory and are not redistributed. Public custody consists only of URLs,
bibliographic identity, byte sizes, SHA-256 hashes, and paraphrased observations in
`results/ciccone-2021-2023-source-reconciliation.md`.

| Version | Official source and retrieval route | Private filename | Bytes | SHA-256 | Redistribution status |
|---|---|---|---:|---|---|
| February 2021 working translation, version 1.0 | University of Mannheim: https://www.vwl.uni-mannheim.de/media/Lehrstuehle/vwl/Ciccone/auerbach_1913_translation_1.0.pdf | `paper/Ciccone 2021 — Auerbach translation v1.0.pdf` | 3,146,817 | `1a9954bd8071c1519fa2c6e8a51facddd0862e0a8ad2cd088b04a110063057c6` | Private source copy; not added to Git or redistributed. The PDF's note licenses the reproduced figure images CC0 1.0, but this project does not rely on that note as a licence for the translation as a whole. |
| 2023 published article | DOI: https://doi.org/10.1177/23998083221147139 (SAGE); published-version bytes retrieved from the University of Mannheim repository: https://madoc.bib.uni-mannheim.de/64096/1/23998083221147139.pdf | `paper/Auerbach and Ciccone 2023 — The Law of Population Concentration.pdf` | 1,648,753 | `4935515fc8a41d9c07c82200f204adf24279115ea0812cb8b89b0c2982ceeaad` | The article states CC BY 4.0, but this project's private-source policy still excludes the PDF bytes from Git and redistribution. |

This addendum supersedes the filename implication of the previously held private file
`paper/Auerbach 1913 — The Law of Population Concentration (Ciccone trans. 2023).pdf`.
Content inspection identified those exact bytes as the February 2021 working translation,
and the file was renamed accordingly. Addendum 1's substantive statement that the then-held
PDF was the Mannheim February 2021 version remains correct; its statement that the 2023
release was not on disk is now historical. The 2023 publication is now held privately and
its added regression plot is formally labeled Appendix Figure A1 (the fourth figure), not
Figure 4.

The reconciliation record is
`results/ciccone-2021-2023-source-reconciliation.md`. Its source enum is a Task 1
proposal pending the fresh-context Task 2 audit; it is not independently confirmed here.

**Task 2 disposition — 2026-09-03:** the fresh-context source-version audit completed
with **STANDS WITH CORRECTION**: source-description corrections only. It confirmed the source enum and inverse-axis
orientation, corrected the formal plot label to Appendix Figure A1, and kept the
source's printed facts distinct from the project's reproduction and ξ/ζ mapping. The
audit record is `AUDIT-CICCONE-SOURCE-RECONCILIATION.md`.

## Addendum 5 — Scaruffi dual-source follow-up governance — 2026-09-04

This dated addendum freezes governance before any Scaruffi parser, fit, receipt, or
result exists. `data/scaruffi-followup-plan.json` is the machine-readable authority;
`results/scaruffi-source-audit.md` is the evidence authority. No fit had been run when
these rules were frozen.

| Source ID | Private custody path | Identity | Target rows | Provenance metadata |
|---|---|---|---:|---|
| `arquivo_pt_20091008014619` | `data/raw/scaruffi-2026-09-03/historical-evidence/scaruffi-tallest-20091008014619.html` | 100,381 bytes; SHA-256 `813731ac6000d00cab2c7d7915a294a8b2dbf6551b0a5fc4a34f9aa0d882a571` | 555 | Arquivo.pt `2009-10-08T01:46:19Z`; original Last-Modified `2009-03-30T02:49:20Z`; replay URL recorded in the JSON contract; ignored `_manifest.json` is 910 bytes, SHA-256 `552c29fbe850d5e7b2aa730d9a1eca733551c89ab064389eba6b13d6a6440519`. |
| `scaruffi_20260903_current` | `data/raw/scaruffi-2026-09-03/tallest.html` | 102,018 bytes; SHA-256 `4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe` | 565 | dated 2026-09-03 current capture; no archival manifest or archive metadata. |

Both are third-party copyrighted compilations with no recorded redistribution licence.
The HTML, historical `_manifest.json`, private trace, names, parsed rows, row sequences,
and reconstructed row lists remain ignored and private: none may enter Git, releases,
Pages, fixtures, or public generated output. The public boundary permits only hashes,
counts, aggregate diagnostics, rule IDs, aggregate mapping counts, fingerprints,
receipts, and dispositions. The documentary URL is
`http://www.scaruffi.com/travel/tallest.html`; capture bytes prove the frozen content
identity, not the URL from which the bytes originated.

The two contracts use `scaruffi-source-contract-v2`, exact headers `Mountain`,
`Height`, `Country`, and `Continent`, `scaruffi-height-lexical-v1`, and
`scaruffi-anomaly-report-v1`. A unique exact-header table is mandatory. Names are NFKC
normalized with collapsed whitespace and casefolded only for comparison; source ordinal
is retained; analytical rank is descending normalized metres, normalized casefold name,
then source ordinal. Decimal `^[0-9]+\.[0-9]+$` heights in [3.5, 9.0] are kilometres
times 1,000, while digit-only `^[0-9]+$` heights in [3500, 9000] are metres. Unsupported
schema IDs, byte/hash/content-identity failures, manifest identity failures, table or
row-count failures, missing fields, invalid heights, and nonblank extra cells hard-fail
before fitting. The anomaly report emits, in order, kilometre conversions, metre
conversions, repeated casefold-name groups, same-name/different-height groups, exact
name-height groups, height ties, source-order inversions, missing fields, blank extra
cells, and nonblank extra cells.

Historical/current mapping is deterministic diagnostics only: exhaust exact
`(normalized casefold name, canonical metres)` pairs one-to-one by source ordinal;
then pair remaining same-name/different-height rows one-to-one by source ordinal; then
emit `historical_only` and `current_only`. Fuzzy matching, aliases, inferred
substitutions, and mapping-driven deletion are prohibited. The ignored private trace is
`data/raw/scaruffi-2026-09-03/reconstruction-membership.json` under
`scaruffi-private-trace-v1`, with the canonical row, assignment, ordering, and
fingerprint encodings frozen in the JSON authority.

The sole archival candidate is the all-row, 555-row
`arquivo_pt_20091008014619_as_archived` (`as_archived_all_rows_v1`): every historical
ordinal is retained and none is excluded. It is not Miškinis's unidentified 548-row
sample. The dated 2026-09-03 current arms are S0 (all 565 rows as listed) and S1
(564-row exact-name-and-height duplicate sensitivity retaining the earliest source
ordinal); same-name/different-height rows are never merged. Their later analysis is
separately labelled sensitivity evidence and cannot revise the original Stage-3 verdict.

## Addendum 6 — Owner-approved Scaruffi pre-fit correction — 2026-09-04

This correction resolves fresh-audit findings PF-1 through PF-3 before any parser or fit.
`data/scaruffi-followup-plan.json` remains the machine-readable authority and
`results/scaruffi-source-audit.md` remains the evidence authority. No fit had been run
when this correction was frozen.

The correct Miškinis relation is `ln(h_1 / h(x)) = βx^α`, obtained from
`h(x) = h_1 exp(-βx^α)`; in double-log coordinates it is
`ln(ln(h_1 / h(x))) = ln(β) + α ln(x)`. This correction retains the separate,
unresolved rank-origin convention and the paper's non-identified fitting recipe. It does
not authorize an inferred objective or a favorable recipe choice.

The parser contract now fixes `Decimal` conversion and canonical metre text, every
diagnostic value type, field key, grouping key, group/member ordering, and one-record-per-
cell semantics for trailing blank cells. Thus the current capture's 565 affected rows mean
1,130 blank-cell records and the historical capture's 555 affected rows mean 1,110 such
records. The JSON authority supplies public synthetic vectors covering every anomaly field
without reproducing source rows.

The private-trace contract now fixes all nested keys, types, and insertion orders for
source identities, candidate, included ordinals, per-source row identities, assignments,
aggregate counts, and fingerprints. Its public synthetic oracle fixes all eleven row
hashes, membership and mapping hashes, and a 6,901-byte canonical trace hash. This is a
conformance oracle only; neither a private trace nor row-level source derivative was
created or made public.
