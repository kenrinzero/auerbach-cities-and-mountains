# Ciccone 2021/2023 source reconciliation

This record separates direct source observations from the project's regression
reproduction. PDF text extraction was used only to locate relevant pages; every
page of both versions was rendered and inspected visually. The PDFs remain under
the ignored private `paper/` directory and are not redistributed.

## Sources and custody

| Version | Source of record | Local private file | Bytes | SHA-256 | Inspected pages |
|---|---|---|---:|---|---|
| February 2021 working translation, version 1.0 | [University of Mannheim working-copy URL](https://www.vwl.uni-mannheim.de/media/Lehrstuehle/vwl/Ciccone/auerbach_1913_translation_1.0.pdf); title page identifies Felix Auerbach's 1913 article and Antonio Ciccone's translation and introduction, dated February 2021 | `paper/Ciccone 2021 — Auerbach translation v1.0.pdf` | 3,146,817 | `1a9954bd8071c1519fa2c6e8a51facddd0862e0a8ad2cd088b04a110063057c6` | PDF pp. 1-11; title page, bilingual text, tables, and Figures 1-3 |
| 2023 EPB publication | [DOI 10.1177/23998083221147139](https://doi.org/10.1177/23998083221147139), resolving to the SAGE article; bytes retrieved from the [University of Mannheim repository's published-version record](https://madoc.bib.uni-mannheim.de/64096/1/23998083221147139.pdf). Felix Auerbach and Antonio Ciccone, *The Law of Population Concentration*, *EPB: Urban Analytics and City Science* 50(2), 290-298 (2023) | `paper/Auerbach and Ciccone 2023 — The Law of Population Concentration.pdf` | 1,648,753 | `4935515fc8a41d9c07c82200f204adf24279115ea0812cb8b89b0c2982ceeaad` | All nine PDF pages, journal pp. 290-298; title, alternating running headers, Tables 1-3, Figures 1-3, note 6, and Appendix Figure A1 |

The held 3,146,817-byte PDF was previously named
`paper/Auerbach 1913 — The Law of Population Concentration (Ciccone trans. 2023).pdf`.
Its own title page, February 2021 date, 11-page bilingual layout, and absence of
an appendix identify it as the 2021 working translation. It was renamed to the
2021 private filename above. A fresh download from the official Mannheim URL is
byte-identical. Neither version has a separate figure list. The 2021 file has no
running journal headers; the 2023 file alternates `Auerbach and Ciccone` with the
journal header and printed pages 290-298.

The companion
`paper/Auerbach 1913 — The Law of Population Concentration (Ciccone trans. 2023).md`
was also inspected. It is a project-created English-only derivative whose own
header says “February 2021”; it matches the working translation's text and has no
Figure A1. It was used as a locator and cross-check, not as evidence of source
identity or as a numeric source. The task supplied no replacement private Markdown
filename, so only the misidentified PDF was renamed.

## Version differences relevant to this project

| Question | February 2021 working translation | 2023 EPB publication | Consequence |
|---|---|---|---|
| Identity and layout | Dated February 2021; 11 pages; a short introduction followed by facing German and English text; Figures 1-3 appear as separate plates on PDF pp. 9-11 | Published in EPB 50(2), pp. 290-298, DOI `10.1177/23998083221147139`; nine journal pages; English translation only, with an expanded introduction, notes, and appendix | The formerly held PDF was the working version despite its old filename. Bibliographic claims must distinguish the two versions. |
| Added regression | No OLS estimate, regression plot, or fourth figure | The introduction reports an OLS slope of -1.15 and points to the appendix. Journal p. 298 adds the fourth figure, formally labeled **Figure A1**, not Figure 4. | Existing references to “Fig. 4” identify the fourth figure informally but not by its published label; current-state prose should use “Appendix Figure A1 (the fourth figure).” |
| Regression orientation | Not stated because the regression is absent | Journal p. 290 defines Lotka's approach as log rank on the vertical axis against log city size on the horizontal axis, then says the appendix re-examination uses that approach. Figure A1 visually labels the axes `Log Rank` and `Log Population` and prints the matching equation. | The source itself explicitly establishes the inverse orientation; the project's point-estimate match is corroboration, not the sole basis for choosing the orientation. |
| Regression method and weights | Not stated | Ordinary least squares is named on pp. 290 and 298. Note 6 on pp. 297-298 says the regression line gives the estimate and weights all cities equally. | The source specifies OLS and equal observation weights. It does not name the robust covariance estimator. |
| A.K. sentence after the cutoff discussion | The facing German and English text print 47.2 where the 1913 scan and reproduced Figure 1 carry 47.8 | The English translation still prints 47.2 while reproduced Figure 1 carries 47.8 | The first known translation slip is unchanged in 2023. Neither translation version is the numeric ground truth. |
| German population normalizer | The text prints 64.6 million but divides by 0.645; reproduced Figure 1 carries 64.5 | The text still prints 64.6 million but divides by 0.645; reproduced Figure 1 carries 64.5 | The second known translation slip is unchanged in 2023. |
| Switzerland A.K. in Table 2 | Prints 2.6 | Prints 2.6 | The third known translation slip is unchanged in 2023; the double-entered 1913 scan reads 2.8. |

## Figure 4 inspection

The project and plan called the added plot “Figure 4” because it is the fourth
figure in the 2023 article. Direct inspection shows that the publication's formal
label is **Figure A1**.

| Field | Direct observation | Page/figure location |
|---|---|---|
| x-axis | Population, horizontal axis, printed as `Log Population` | Journal p. 298, Appendix Figure A1 |
| y-axis | Rank, vertical axis, printed as `Log Rank` | Journal p. 298, Appendix Figure A1 |
| transforms | Both variables are logarithmically transformed. The logarithm base is not stated in the inspected source. | Journal pp. 290 and 298, Figure A1 |
| slope | The plot prints `log(Rank) = -1.15 log(Population) + 9.19` and `R² = 0.9827`; the caption also identifies the OLS slope as -1.15. | Journal p. 298, Figure A1 and caption |
| uncertainty label | `robust standard error`, value 0.03. The HC or sandwich convention is not stated in the inspected source. | Journal p. 298, Figure A1 caption |
| sample | Auerbach's German cities in 1910; 94 cities. Note 6 states that all cities receive equal weight. | Journal pp. 297-298, note 6; p. 298, Figure A1 caption |
| method statement | The introduction describes Lotka as plotting log rank vertically against log size horizontally and calculating an ordinary-least-squares slope, then says Ciccone re-examines Auerbach's data using that approach. Note 6 identifies the Figure A1 line as the basis of the OLS estimate. | Journal p. 290, introduction; pp. 297-298, note 6 |

The February 2021 working translation lacks Figure A1, the -1.15 estimate, and
the associated method discussion. It contains only Auerbach's Figures 1-3.

## Adjudication

**Conclusion:** confirmed-explicit

**What the source prints.** The 2023 publication explicitly places log rank on
the vertical axis and log population on the horizontal axis, labels the appendix
plot the same way, and prints an equal-weight OLS slope of -1.15 for 94 German
cities in 1910 with a “robust standard error” of 0.03. Direct inspection therefore
confirms the inverse-axis orientation. The fourth figure's published label is
Figure A1, not Figure 4.

**What the project's fresh regression reproduces.** A fresh run of
`src/stage1_recompute.py` on the double-entered 94-city transcription gives the
inverse OLS slope -1.1489 (HC3 standard error 0.0328), which rounds to the source's
-1.15 (0.03). The direct rank-size regression instead gives -0.8553 (HC3 standard
error 0.0291). The uncertainty value cannot identify orientation because both HC3
values round to about 0.03; the source's explicit axes and method statement do.

**What remains an inference.** The article does not use the project's ξ/ζ
notation, compute `ξ = 1/1.1489 = 0.8704`, state the logarithm base, or identify
the robust covariance convention. Calling the magnitude 1.15 an estimate of the
count-law exponent ζ, mapping it to ξ approximately 0.87, and labeling 0.0328 as
HC3 are project-side interpretation and reproduction, not printed source facts.

This is a Task 1 evidence record, not an independent confirmation. Task 2 must
audit the enum and every direct observation against the held 2023 source before
public claim wording changes.

## Required claim propagation

| File | Exact sentence-level implication after Task 2 accepts this record |
|---|---|
| `CLAIM_INVENTORY.md` | Preserve the frozen EXT-C1 row and append a dated adjudication note: direct inspection of 2023 Appendix Figure A1 explicitly confirms log rank on log population; -1.15 is therefore the inverse-axis slope, while the project's -1.1489 reproduction maps it to ζ and ξ approximately 0.87. Correct the formal figure label without silently rewriting the frozen row. |
| `results/stage0-novelty-sweep.md` | Preserve the dated sweep and add a dated correction beside the EXT-C1 passage: the published label is Appendix Figure A1, and its axes and p. 290 method paragraph explicitly establish orientation. |
| `README.md` | Replace the current inference-only and “future reconciliation” language with the audited direct-source result; distinguish the printed -1.15/0.03 from the project's -1.1489/0.0328 reproduction and ξ mapping; call the plot Appendix Figure A1 (the fourth figure). |
| `REPORT.md` | Remove “source-provisional,” “re-read,” and “awaits a dedicated source-version reconciliation” from current-state EXT-C1 prose. State that direct 2023 inspection explicitly confirms the inverse orientation, then separately report the project's reproduction and the still-unstated log base/robust-SE convention. Correct current-state Figure 4 labels to Appendix Figure A1 while leaving dated audit history intact. |
| `src/build_explorer.py` | Propagate the same audited distinction to the Overview, detailed EXT-C1 text, and source/footer prose; generated `results/explorer.html` and `docs/index.html` must inherit the wording from the builder. |
| `src/verify_report_numbers.py` | If Report wording changes break textual needles, update only labels/needles (including Figure A1 naming); preserve the numerical recomputation and 109-claim set. |
| `tests/test_reader_facing_site.py` | Pin the accepted direct-inspection wording and source/version distinction as specified in Task 5; do not turn the test into a new numerical derivation. |
| `CREDITS.md` | This additional current-state public surface says the open 2023 release adds “Fig. 4.” Change that label to Appendix Figure A1 (the fourth figure) when Task 5 propagates the accepted verdict. |

Historical artifacts (`PREREGISTRATION.md`, `results/stage1-summary.md`, audit
files, and generated receipts) record what was known at their dates. They should
not be silently rewritten; any needed clarification should be a dated
cross-reference to this reconciliation and the Task 2 audit.
