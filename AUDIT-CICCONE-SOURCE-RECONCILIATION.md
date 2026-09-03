# AUDIT - Ciccone source reconciliation

## Verdict

**STANDS WITH CORRECTION**

The scientific interpretation stands: the 2023 source explicitly reports an inverse-axis regression, and the project's mapping of its slope magnitude to the count-law exponent is consistent with those axes. The corrections are source-description corrections only: the regression is absent from the February 2021 working translation, its formal 2023 label is Appendix Figure A1 rather than Figure 4, its orientation is explicit in the source rather than inferred from the project's reproduction, and its unspecified robust-error convention must not be labeled HC3 as a source fact.

The contradiction stop gate does not fire because these corrections do not change the project's scientific interpretation.

## Independent source extraction

Before opening the reconciliation record or current EXT-C1 wording, the reviewer visually inspected only Ciccone 2021 PDF pp. 1 and 9 and Auerbach and Ciccone 2023 PDF pp. 1 and 9. PDF text extraction was used only to locate those pages. The observations below are limited to that rendered-page inspection.

| Source | Field | Reviewer observation | Page/figure location |
|---|---|---|---|
| Ciccone 2021 working translation | x-axis | Rank number. | PDF p. 9, Figure 1 |
| Ciccone 2021 working translation | y-axis | Population in thousands on the left axis and absolute concentration on the right axis. | PDF p. 9, Figure 1 |
| Ciccone 2021 working translation | transform | No logarithmic transform is labeled. | PDF p. 9, Figure 1 |
| Ciccone 2021 working translation | slope | No fitted regression slope is reported; the introduction describes Auerbach's city-size law as a power law with exponent -1. | PDF pp. 1 and 9 |
| Ciccone 2021 working translation | uncertainty label | None for a fitted slope. | PDF pp. 1 and 9 |
| Ciccone 2021 working translation | sample | Germany; the Figure 1 average annotation uses a denominator of 94 and the plotted ranks extend through 94. | PDF p. 9, Figure 1 |
| Ciccone 2021 working translation | method | Figure 1 plots population and absolute concentration against rank; no OLS fit is shown. | PDF p. 9, Figure 1 |
| Ciccone 2021 working translation | figure label | `Figure 1: Population and Absolute Concentration`. | PDF p. 9 |
| Auerbach and Ciccone 2023 publication | x-axis | `Log Population`. | PDF p. 9 / journal p. 298, Figure A1 |
| Auerbach and Ciccone 2023 publication | y-axis | `Log Rank`. | PDF p. 9 / journal p. 298, Figure A1 |
| Auerbach and Ciccone 2023 publication | transform | Log-log; the axes do not name a log base. | PDF p. 9 / journal p. 298, Figure A1 |
| Auerbach and Ciccone 2023 publication | slope | -1.15 for log rank on log population; the displayed equation is `log(Rank) = -1.15 log(Population) + 9.19`, with `R^2 = 0.9827`. | PDF pp. 1 and 9 / journal pp. 290 and 298, introduction and Figure A1 |
| Auerbach and Ciccone 2023 publication | uncertainty label | `robust standard error`, 0.03, for the OLS slope. | PDF p. 9 / journal p. 298, Figure A1 caption and embedded notes |
| Auerbach and Ciccone 2023 publication | sample | 94 German cities in 1910, using Auerbach's data. | PDF p. 9 / journal p. 298, Figure A1 caption and embedded notes |
| Auerbach and Ciccone 2023 publication | method | Ordinary least squares. | PDF pp. 1 and 9 / journal pp. 290 and 298, introduction and Figure A1 caption |
| Auerbach and Ciccone 2023 publication | figure label | `Figure A1. Log-log plot using Auerbach's data for German cities in 1910.` | PDF p. 9 / journal p. 298 |

## Post-comparison source check

After the independent extraction and comparison were complete, the reviewer rendered and visually inspected Auerbach and Ciccone 2023 PDF p. 8 / journal p. 297 and re-rendered p. 9 / journal p. 298. Note 6 begins on p. 297 and continues on p. 298. It identifies the Appendix Figure A1 regression line as the basis of the -1.15 log-log OLS estimate, then states that it "weights all cities equally" and that limiting the regression to cities with rank 20 or lower would move the slope closer to -1. This post-comparison check supplies the source basis for `equal-weight` in the allowed wording; it is not part of the fresh pre-comparison extraction.

The same post-comparison check shows note 6 writing `log(rank) = 3` for rank 20. That numerically indicates natural logs to the shown precision, but the source still does not expressly name the log base.

## Comparison with the reconciliation record

Agreements:

- The 2021 working translation has Auerbach's Figures 1-3 and no OLS appendix figure, slope estimate, or robust standard error.
- The 2023 publication explicitly puts log population on the horizontal axis and log rank on the vertical axis.
- The displayed and captioned slope is -1.15, the displayed intercept is 9.19, and the displayed `R^2` is 0.9827.
- The uncertainty is labeled only as a robust standard error of 0.03; the source does not name an HC or sandwich convention.
- The sample is Auerbach's 94 German cities in 1910, and the method is equal-weight ordinary least squares.
- The formal published label is Appendix Figure A1, not Figure 4.
- The source itself establishes the regression orientation. The project's -1.1489 reproduction corroborates that source fact but is not needed to infer it.
- The source does not use the project's ξ/ζ notation or state ξ approximately 0.87; that mapping is project interpretation.

Qualified discrepancy:

- The reconciliation says the log base is not stated. That is correct as a matter of express labeling. The post-comparison source check of note 6 makes the natural-log base inferable from its rank-20 example, but this remains an inference rather than an explicit source label.

Discrepancies in current public wording:

- `CLAIM_INVENTORY.md`, `results/stage0-novelty-sweep.md`, `README.md`, `REPORT.md`, `src/build_explorer.py`, and `CREDITS.md` use the informal `Fig. 4` or `Figure 4`; the publication labels it Appendix Figure A1.
- `README.md` and `REPORT.md` retain future-reconciliation or inference-only language even though the 2023 source makes the orientation explicit.
- `REPORT.md` calls log size on log rank "Ciccone's recipe" and says only the point estimate can discriminate the orientations. Ciccone's stated and plotted specification is log rank on log population, and direct source inspection discriminates the orientations.
- `src/build_explorer.py` calls the reported 0.03 an "HC3-type value" without consistently separating the source's generic robust-SE label from the project's HC3 comparison. HC3 is a project-side reproduction choice, not a source label.
- Some current wording blurs the February 2021 working translation, which has no regression, with the 2023 publication that adds Appendix Figure A1.

## Allowed public wording

### Exact Overview sentence

> Direct inspection of Appendix Figure A1 in Auerbach and Ciccone (2023) confirms that its reported −1.15 slope is equal-weight OLS of log rank on log population for 94 German cities in 1910 (robust SE 0.03); under this project's notation, its magnitude estimates ζ = 1/ξ, corresponding to ξ approximately 0.87.

### Exact technical REPORT formulation

> Direct inspection of Appendix Figure A1 and note 6 in Auerbach and Ciccone (2023) shows log population on the horizontal axis and log rank on the vertical axis and reports an equal-weight ordinary-least-squares slope of −1.15 (robust standard error 0.03; 94 German cities, 1910). The project's separate reproduction of that inverse specification is −1.1489 (HC3 SE 0.0328), whose magnitude the project maps to ζ = 1/ξ and thus ξ = 1/1.1489 = 0.8704; the source does not state the robust covariance convention, use the ξ/ζ notation, or report a population-on-rank OLS coefficient.

### Rule for all other public surfaces

Apply all of the following together:

1. Call the plot `Appendix Figure A1 (the fourth figure)`, never `Fig. 4` or `Figure 4` as though that were the published label.
2. Attribute Appendix Figure A1 and its regression only to the 2023 publication; state that the February 2021 working translation contains Figures 1-3 and no regression appendix.
3. Treat −1.15, robust SE 0.03, 94 German cities in 1910, equal-weight OLS, x = log population, and y = log rank as source facts; note 6 across journal pp. 297-298 is the source basis for equal weighting.
4. Treat -1.1489, HC3 SE 0.0328, ζ = 1/ξ, and ξ = 0.8704 as project reproduction or interpretation. Never describe 0.8704 as a reverse OLS estimate; it is the reciprocal mapping of the inverse fitted-line slope magnitude.
5. Do not call population-on-rank OLS "Ciccone's recipe", do not say that only the matching point estimate identifies orientation, and do not attribute HC3 to the source.
6. For dated or frozen artifacts such as `CLAIM_INVENTORY.md` and `results/stage0-novelty-sweep.md`, preserve the historical text and add a dated correction or adjudication note rather than silently rewriting it. Current-state prose may be corrected directly.
7. In `CREDITS.md`, replace the version/figure sentence with: `The project consulted the February 2021 working version; the open 2023 publication by Auerbach and Ciccone adds Appendix Figure A1 (the fourth figure), which reports equal-weight OLS of log rank on log population, and retains the mismatches. Neither version is used as a numeric source for Auerbach's tables.`

## Residual uncertainty

- The axes say only `Log`; a post-comparison visual check makes natural logs inferable from note 6's rank-20 example, but they are not expressly named.
- The robust standard error convention is not specified, so the source's 0.03 cannot be labeled HC3.
- Figure A1 does not estimate the reverse population-on-rank OLS regression. Because OLS is not invariant to swapping dependent and independent variables, the reciprocal -1/1.15 is an algebraic fitted-line mapping, not a reverse-regression coefficient.
- The source does not define ξ or ζ. The statement that the magnitude 1.15 estimates ζ = 1/ξ and maps to ξ approximately 0.87 belongs to the project's notation and interpretation.
- This audit directly adjudicates the source description. It did not independently rerun the project's numerical regression; the reconciliation record's -1.1489/0.0328 reproduction was used only after the source extraction was complete.
