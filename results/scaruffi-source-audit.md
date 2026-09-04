# Scaruffi / Miškinis source audit — 2026-09-04

## Question and non-fitting boundary

This audit establishes what the primary paper prints, the custody and rights status of the preserved 2026-09-03 Scaruffi capture, and whether independently preserved row-level evidence exists for the historical comparator. It does not fit the current capture, reconstruct Miškinis's sample, select rows to reproduce a benchmark, or alter any accepted Stage-3 source, receipt, multiplicity family, or verdict. Benchmark evidence is not membership evidence: a repeated count or coefficient cannot identify which summits were included.

## Primary-paper benchmarks

The publisher-hosted source is Paulius Miškinis, “Mathematical modelling of mountain height distribution on the Earth's surface,” *Geologija* 53, no. 1(73) (2011): 21–26, ISSN 1392-110X. The article records receipt on 22 December 2009 and acceptance on 3 March 2011 (p. 21). No DOI is printed. The PDF's displayed pagination, not the PDF page index, is used below.

On p. 21, the introduction says that the study first compiles and verifies a list of the 548 highest continental mountains, those higher than 3,500 m. Under “Materials and methods — Approximation” on p. 22, it identifies a list compiled by P. Scaruffi (Scaruffi, 2008) as the information source and again states that it comprises 548 mountains higher than 3,500 m. Reference 10 on p. 26 is “Scaruffi P. 2008. Highest mountains in the world” followed by `http://www.scaruffi.com/travel/tallest.html`.

The printed rank curve is, on p. 22, equations (1)–(2):

`h(x) = h_1 exp(-βx^α)`, with `α = 0.54044`, `β = 3.1170 × 10^-2`, and `h_1 = 8,848 m`. Its power relation is `ln(h_1 / h(x)) = βx^α`; its double-log linearization is `ln(ln(h_1 / h(x))) = ln(β) + α ln(x)`. Direct evaluation gives 3,291.265 m at rank 600 and 3,020.302 m at rank 700, confirming the paper's printed integer benchmarks 3,291 m and 3,020 m. It describes `n = 1` as Everest on p. 23, while equation (6), the inverse count expression, adds one “for the purpose of numeration.” The paper does not state a fitting objective, weighting scheme, coefficient constraints, optimizer, or enough detail to resolve the equation-(2)/equation-(6) rank-origin convention into a unique fitting recipe.

The remaining printed fit and comparison benchmarks are:

- Figure 2b and its text (pp. 22–23): residual mean `-19.8 m` and standard deviation `155.5 m`, displayed again as approximately `156 m`.
- Equation (5) and text (p. 23): `|a_m| ≈ (1.613 × 10^3) / f^0.9837`; therefore the spectral density is described as proportional to `1 / f^1.967`, close to `1 / f^2`. The calculation averages 10 random Fourier transformations after reducing 548 harmonics to 500 and uses the first 50 members.
- Equations (6)–(7) (p. 23): `N = {ln(h_1/h)/β}^{1/α} + 1` and `δN_th = 1.6388 × 10^6 {ln(8848/h)}^0.85034`.
- The paragraph following Table 1 (p. 24): mean theoretical relative error `14.5%` and mean real relative error `13.3%`.
- Power/exponential comparison (p. 25): the text prints a power-function parameter `a = 4.513 × 10^-2`. Table 3 prints, for `N = 30`, standard deviations `75` for equation (2) and `51` for the parenthesized power comparator, with correlations `0.97` and `0.99`; for the column headed `N = 540`, it prints standard deviations `156` and `591`, with correlations `0.99` and `0.91`. The adjacent prose instead calls the larger interval `N = 548` and gives the comparison `591 : 156 ≈ 4`, an internal count-label inconsistency that prevents silent substitution of one value for the other.
- Conclusion 1 (p. 25) says the height distribution from 3,500 to 8,848 m is approximated by the exponential and not the power function.

Table 1 (p. 23) supplies the row-count benchmarks that can be evaluated without inventing membership. In descending threshold order it prints:

| `h`, km | 8.0 | 7.5 | 7.0 | 6.5 | 6.0 | 5.5 | 5.0 | 4.5 | 4.0 | 3.5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| theoretical `N_TH` | 10 | 23 | 43 | 70 | 107 | 156 | 218 | 298 | 401 | 534 |
| observed `N` | 14 | 34 | 53 | 77 | 119 | 157 | 206 | 248 | 416 | 548 |
| theoretical `δN_TH` | 3.1 | 5.1 | 7.3 | 10 | 13 | 17 | 22 | 28 | 36 | 47 |
| observed `δN` | 4 | 11 | 10 | 7 | 12 | 1 | 12 | 50 | 15 | 14 |
| theoretical `ε_TH`, % | 32 | 22 | 17 | 14 | 12 | 11 | 10 | 9.4 | 9.0 | 8.8 |
| observed `ε`, % | 30 | 33 | 19 | 8.5 | 10 | 0.8 | 5.8 | 20 | 3.7 | 2.6 |

The prose immediately above Table 1 prints “`548–53 = 4`” while the same sentence uses `14 / 548 = 2.6%` and the table gives theoretical 534, observed 548, and observed difference 14. This is a printed arithmetic inconsistency, not authority to repair the source benchmark.

Integers above are exact-match benchmarks. Every decimal benchmark has acceptance tolerance equal to half one unit in its last printed decimal place: `α` ±0.000005; `β` ±0.0000005 after expanding `3.1170 × 10^-2`; residual mean and standard deviation ±0.05 m; the mantissa `1.613` ±0.0005 (equivalently ±0.5 after multiplication by `10^3`); spectral exponent ±0.0005; equation-(7) mantissa `1.6388` ±0.00005 (equivalently ±50 after multiplication by `10^6`) and exponent ±0.000005; mean errors `14.5%` and `13.3%` ±0.05 percentage point; power-comparator mantissa `4.513` ±0.0005 (equivalently ±0.000005 after multiplication by `10^-2`); Table 3 correlations ±0.005; Table 1 threshold decimals ±0.05 km; its one-decimal error entries ±0.05 in their printed units. The exact `β` expansion is `0.031170`, so its half-last-printed-digit tolerance is `0.0000005`.

Table 2 (p. 24) extrapolates equations (6)–(7) below the observed source floor; it is not empirical membership evidence. Preserving the displayed precision, the complete printed table is:

| `η`, m | 3,500 | 3,000 | 2,000 | 1,000 | 914.4 | 610 | 600 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `N` | 534 | 709 | 1,277 | 2,591 | 2,793 | 3,782 | 3,826 |
| `δN` | 47 | 63 | 123 | 342 | 387 | 667 | 682 |
| `ε`, % | 8.85 | 8.86 | 9.67 | 13.2 | 13.9 | 17.6 | 177.8 |

The 3,500 m count repeats equation (6)'s 534; the lower-threshold entries cannot be checked against the preserved page, which states a 3,500 m floor. Counts, whole-metre thresholds, and `δN` values are exact-match benchmarks. The `914.4 m` threshold has tolerance ±0.05 m; `8.85%`, `8.86%`, and `9.67%` have tolerance ±0.005 percentage point; and `13.2%`, `13.9%`, `17.6%`, and `177.8%` have tolerance ±0.05 percentage point. The source-visible `177.8` at 600 m is preserved rather than silently repaired, even though `682 / 3,826 × 100` is about `17.8%`.

The paper supplies no mountain names, row appendix, supplementary dataset, content-dated Scaruffi URL, or reproducible rule that maps a later page to the 548 memberships. The bibliographic year “2008” is not an archive timestamp. Figures 1a, 1b, 2a, and 2b show aggregate curves or residuals and do not expose row identities.

## Current capture custody

The private capture is `data/raw/scaruffi-2026-09-03/tallest.html`, from `http://www.scaruffi.com/travel/tallest.html`, retrieved once at `2026-09-03T09:09:13Z`. It is 102,018 bytes and has SHA-256 `4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe`. Git attributes its exclusion to `.gitignore`, and `git ls-files --error-unmatch` confirms that the file is not tracked.

Direct structural inspection finds 568 literal `<tr>` elements across three tables. The unique target table has the normalized leading header tuple `("Mountain", "Height", "Country", "Continent")`, followed by 565 data rows. These are custody and structure facts only; the present capture is not identified as Miškinis's 548-row object.

## Rights and nonredistribution boundary

The page is a third-party copyrighted compilation with no recorded redistribution licence. The HTML and every row-complete derivative remain private: they must not enter Git, releases, Pages, fixtures, generated public HTML, or another public row-level representation. Public records may retain source identifiers, hashes, aggregate diagnostics, and conclusions that do not reproduce the compilation.

## Frozen parser rules and anomaly taxonomy

The parser contract for any later owner-authorized work is fixed independently of fit results. Select the unique table whose first four normalized cell texts are exactly `Mountain`, `Height`, `Country`, and `Continent`; an absent or ambiguous match is a hard failure. Normalize names with Unicode NFKC and collapsed whitespace, using casefold only for duplicate comparison. Parse accepted height tokens directly as `Decimal`, never binary float: a finite base-10 decimal token in `[3.5, 9.0]` is multiplied exactly by `Decimal('1000')`, and a digit-only integer in `[3500, 9000]` remains exact metres; `canonical_metres` uses fixed-decimal formatting, strips trailing fractional zeros and the trailing point, and maps empty or `-0` to `0`. Every other token hard-fails. Preserve source ordinal. Analytical rank sorts by descending normalized metres, then normalized casefold name, then source ordinal, so height ties are deterministic and source order is never treated as analytical rank.

Report without silently resolving repeated normalized name-and-height keys, repeated case-insensitive names, same-name/different-height records, height ties, source-order inversions, missing fields, blank extra cells, nonblank extra cells, and every kilometre/metre conversion. The exact value schemas, keys, types, group/member sort order, and public synthetic conformance vectors are governed by `data/scaruffi-followup-plan.json`. In particular, blank extra cells are one record per cell, not one record per affected row; any nonblank unexpected cell is a hard failure after deterministic diagnostic classification.

Direct inspection of the current capture provisionally finds 564 decimal-kilometre conversions, one integer-metre conversion, one repeated normalized name-and-height key class (one excess row), eight repeated case-insensitive name classes (eight excess rows), seven same-name/different-height classes, 60 tied height values involving 136 rows, seven adjacent source-order increases, no missing required fields, 565 affected rows containing 1,130 blank extra cells, and no nonblank extra cells. The historical capture has 555 affected rows containing 1,110 blank extra cells. These anomaly counts are provisional until Task 3 appends the deterministic parser summary; no row content is reproduced here.

**Owner-approved pre-fit correction — 2026-09-04 (PF-1/PF-2/PF-3).** The power relation and double-log linearization above correct the prior mistranscription without altering the rank-origin or fitting-recipe non-identifiability. The machine-readable authority now freezes exact `Decimal` conversion, anomaly output schemas and ordering, cell-level extra-cell semantics, full nested private-trace order/types, and public synthetic byte/hash conformance vectors. No parser, fit, receipt, private trace, or result was run or generated by this correction.

## Historical membership evidence search

The bounded search used only the publisher record, archival indexes, and the cited author URL. On access date 2026-09-04 (Europe/Budapest), the publisher article page at `https://mokslozurnalai.lmaleidykla.lt/geologija/2011/1/6162` exposed issue metadata and the article, but no supplement or row list. The publisher PDF and reference 10 supplied the Scaruffi URL but no dated capture or row appendix. Searches for the exact title, exact cited URL, and the phrase “548 mountains” located repetitions of the paper's aggregate count and the current author page; those are benchmark evidence, not membership evidence.

The Internet Archive availability query `https://archive.org/wayback/available?url=http%3A%2F%2Fwww.scaruffi.com%2Ftravel%2Ftallest.html&timestamp=20111231` returned an empty `archived_snapshots` object. Direct Internet Archive CDX requests for the `www` and bare-host forms, restricted through 2011, returned HTTP 403 in this environment and therefore supplied no positive evidence.

Arquivo.pt's CDX endpoint `https://arquivo.pt/wayback/cdx?url=www.scaruffi.com%2Ftravel%2Ftallest.html&from=1996&to=2011&output=json` returned one row-level capture: original URL `http://www.scaruffi.com/travel/tallest.html`, archive timestamp `2009-10-08T01:46:19Z`, original `Last-Modified` header `2009-03-30T02:49:20Z`, HTTP 200, media type `text/html`. The original-byte replay URL is `https://arquivo.pt/wayback/20091008014619id_/http://www.scaruffi.com/travel/tallest.html`.

The replay was retrieved at `2026-09-03T23:11:09Z` and preserved only under ignored private custody as `historical-evidence/scaruffi-tallest-20091008014619.html`: 100,381 bytes, SHA-256 `813731ac6000d00cab2c7d7915a294a8b2dbf6551b0a5fc4a34f9aa0d882a571`, media type `text/html`. Its ignored private `_manifest.json` records URL, archive and retrieval timestamps, size, hash, media type, and rights status. Direct inspection provisionally finds a target table with 555 data rows, not 548. That count does not invalidate the capture as historical membership evidence, but it does prevent equating the as-archived page with Miškinis's later compiled-and-verified 548-row object.

## Evidence-supported candidate rules

The sole evidence-supported rule identifier is `arquivo_pt_20091008014619_as_archived`: the membership expressed by the target table in the independently preserved 2009-10-08 Arquivo.pt capture, without additions, exclusions, de-duplication, or reordering. This identifier records an evidence object, not an authorization to parse or fit it. No rule is supported for selecting 548 of its provisionally observed 555 rows, mapping its rows to the present capture, removing historical rows absent from the present page, or resolving apparent duplicates.

Because row-level historical evidence is present, the controlling plan requires a stop and an owner-approved evidence-specific amendment before Task 2. That amendment must define the archived HTML parser, identity mapping to current rows, treatment of historical rows absent from the current page, and a private membership interface. Numerical proximity to 548 or to any printed coefficient cannot fill those missing decisions.

## Identifiability consequence

The cited 2008 list is not yet exactly reconstructable as Miškinis used it. The surviving 2009 snapshot supplies independently dated row-level evidence, but its provisional 555-row target table differs from the paper's 548, and the paper does not disclose the seven exclusions, a dated retrieval, or a unique fitting recipe. Accordingly, historical exactness is presently non-identified. This is a controlled stop-and-amend-plan outcome, not permission to infer membership or proceed with the current-capture analysis.

## Sources and hashes

- Miškinis publisher PDF: `https://www.lmaleidykla.lt/ojs/index.php/geologija/article/download/1615/632/0`; accessed 2026-09-04; 442,264 bytes; SHA-256 `a94e215892fb4cf86ca4e14e986d1212dc3252e798654317867ef5f88b9e7e83`.
- Publisher article record: `https://mokslozurnalai.lmaleidykla.lt/geologija/2011/1/6162`; accessed 2026-09-04.
- Current private capture: `http://www.scaruffi.com/travel/tallest.html`; retrieved `2026-09-03T09:09:13Z`; 102,018 bytes; SHA-256 `4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe`.
- Arquivo.pt historical replay: `https://arquivo.pt/wayback/20091008014619id_/http://www.scaruffi.com/travel/tallest.html`; archive timestamp `2009-10-08T01:46:19Z`; retrieved `2026-09-03T23:11:09Z`; 100,381 bytes; SHA-256 `813731ac6000d00cab2c7d7915a294a8b2dbf6551b0a5fc4a34f9aa0d882a571`.

```text
membership_evidence: present
evidence_supported_candidate_rules: [arquivo_pt_20091008014619_as_archived]
```
