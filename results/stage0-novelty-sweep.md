# Stage 0 novelty sweep — dated 2026-09-01 (Kimi)

Purpose: establish, with receipts, (a) whether Auerbach's mountain-summit claim has
been formally tested, and (b) where the city-side arms sit against the modern
literature. This anchors the writeup's novelty statement; it is a dated snapshot,
not a living claim.

## Queries and findings

**"rank-size distribution mountain summit heights power law Zipf"** —
No Auerbach-connected test found. General rank-size literature is cities/words/firms.

**"'distribution of mountain heights' / 'summit elevations' statistical distribution power law lognormal"** —
- **Miškinis, P. (2011), "Mathematical modelling of mountain height distribution on
  the Earth's surface," *Geologija* 53(1):21–26.** Compiled/verified a 548-summit
  list (> 3,500 m, from Scaruffi 2008); fit height-vs-rank; **concludes the
  distribution "is approximated by the exponential and not the power function"**;
  deviations ≈ 1/f² noise; estimates a maximum possible mountain height. No mention
  of Auerbach; no prominence control; no uncertainty calibration.
- **"Derivation of a Formula for Mountain Height as a Function of Rank in Height,"
  *J Applied Mathematics and Physics* (SCIRP), 2023-11.** Derives a CIR-type SDE
  for elevation dynamics (steady uplift + stochastic erosion) ⇒ gamma-like tail
  `p(h) ∝ h^(b−1)·exp(−a·h)`; MLE fit on six regional mountain classifications
  (British Isles Simms, Continental Europe, North Africa, North America);
  comparators: generalized Pareto with finite endpoint and the Miškinis function
  `h(i) = h_max·exp(−β(i−1)^(1/α))`. Excellent fits reported; chi-square GoF does
  not reject. No Auerbach framing, no exponent-vs-1 question, no prominence
  treatment. Venue quality noted (SCIRP); used as prior art on *model families*,
  not as authority.

**"Auerbach 1913 'mountain' summit heights claim tested"** —
No work found testing or even citing the mountain sentence for empirical content.
Citations of Auerbach 1913 in modern literature are all city-side. The ALZ naming
proposal (Rybski–Ciccone 2023) is being picked up (e.g. arXiv:2407.19874 adopts
"Auerbach-Lotka-Zipf's law").

**"geomorphology hypsometric distribution summit elevation frequency"** —
Geomorphology's elevation-distribution tradition is **hypsometry** (Strahler 1952):
area-frequency of DEM *cells*, used to fingerprint glacial vs. fluvial erosion.
Different object than discrete summits — not prior art on the claim, but a
neighboring literature to cite for mechanism context (erosion-dominated
equilibration).

**"'specific concentration' Auerbach Sp.K. modern recomputation"** —
Nothing found recomputing Auerbach's tables from independent data or re-running his
twelve-country Sp.K. on modern data. Found instead: **Ciccone's translation already
contains a translator-added Fig. 4: log-log OLS on Auerbach's 94 cities, slope
−1.15 (robust SE 0.03)** — the one existing exponent estimate on the 1913 data,
now inventoried as EXT-C1. Also found: Michael Batty's companion editorial in the
same EPB issue discussing K and S_n.

## Conclusions (dated)

1. **The mountain claim as Auerbach's claim is untested** — the two rank-height
   papers that exist (Miškinis 2011; JAMP 2023) neither cite him nor ask the
   directional question, and both fit bounded/exponential-type families rather than
   testing a power-law exponent against 1 with calibrated uncertainty and
   prominence-controlled data. The surviving delta is real but narrower than
   "nobody looked": *nobody looked with Auerbach's question, prominence-aware data,
   and modern GoF/alternative testing.*
2. **The city side's delta:** no independent recomputation of Table 1 from census
   data, no modern Sp.K. persistence test on his twelve countries, and no MLE
   treatment of his 94 cities (only Ciccone's OLS). Positioning literature for
   Stage 2: Soo 2005 (cross-country OLS estimates, mean ≈ 1.1), Nitsch 2005
   meta-analysis (mean ≈ 1.08), Berry & Okulicz-Kozaryn 2011 (consistent
   definitions → law holds) — the definition-sensitivity axis Auerbach himself
   flagged in 1910 (AU-C9).

**Dated correction — 2026-09-03:** the Berry and Okulicz-Kozaryn paper's
year of record is 2012 (**2012**) (*Cities* 29(S1):S17–S23); December 2011 is its
online-publication date. The 2011 label above is retained as part of this
2026-09-01 search record and is superseded by this correction.
3. Model-set consequence (prereg §5.2): truncated PL, cutoff PL, gamma-type tail,
   and the Miškinis stretched-exponential rank curve are mandatory alternatives —
   the two prior studies both point away from a pure power law for summits.

## Sources

- Miškinis 2011, *Geologija* 53(1):21–26 — https://www.lmaleidykla.lt/ojs/index.php/geologija/article/download/1615/632/0
- JAMP 2023 rank-height formula — https://www.scirp.org/journal/paperinformation?paperid=129216
- Ciccone translation PDFs (incl. Fig. 4 OLS and Batty editorial) — https://www.vwl.uni-mannheim.de/media/Lehrstuehle/vwl/Ciccone/
- ALZ adoption example — https://arxiv.org/html/2407.19874v1
- Hypsometry context — Strahler 1952 tradition, e.g. https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020JF005765
