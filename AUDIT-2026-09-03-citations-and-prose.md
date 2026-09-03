# Citation and prose audit — 2026-09-03

**Status:** corrections applied after owner review. This is a bibliographic and
reader-facing audit, not a new statistical stage. It changes no raw data, derived data,
pre-registration, fitted receipt, claim verdict or quantitative conclusion.

## Scope and method

The audit covered `README.md`, `REPORT.md`, the generated site, its masthead and footer,
and every reference used there. Checks were made against the held 1913 scan, the held
February 2021 Ciccone working translation, the open 2023 publication, DOI registry
metadata, journal issue records, and official dataset or publication pages. The numerical
claim verifier was then rerun to ensure that the prose work did not disturb the analytical
record.

The audit distinguishes three questions that the earlier presentation sometimes merged:

1. Is the scientific finding stated within the pre-registered evidence boundary?
2. Is its bibliographic citation accurate and checkable?
3. Is its audit provenance useful at this point in the reading flow?

The third question drove the site redesign: provenance remains available, but no longer
interrupts the headline account.

## Citation corrections

### 1. Auerbach (1913): pages verified; unsupported issue omitted

The held scan shows the article beginning on printed page 74, ending on page 76, followed
by Tafel 14. It does not establish the issue designation `(I)`. Secondary records disagree
on the issue and first page: the SAGE page and translation use `59(I):74–76`, Rybski (2013)
prints `59, 73–76`, and Rybski and Ciccone (2023) print `59 (74):74–76`. The public citation
therefore now reads **volume 59, pages 74–76, with Tafel 14**, without an issue number.
“No DOI exists” was narrowed to the supportable statement “No DOI was found in Crossref.”

### 2. Ciccone: the working source and published release are separate records

The project worked from Ciccone's **February 2021 version 1.0 working translation**, which
contains Auerbach's Figures 1–3. Its official Mannheim URL is:

https://www.vwl.uni-mannheim.de/media/Lehrstuehle/vwl/Ciccone/auerbach_1913_translation_1.0.pdf

The openly available 2023 publication adds the translator's Figure 4 and its reported OLS
slope of −1.15:

https://doi.org/10.1177/23998083221147139

The project continues to treat the 1913 scan as ground truth for Auerbach's numerals. The
2023 release retains the documented mismatches against that scan. A fuller comparison of
the 2021 and 2023 versions is recorded below as future work rather than improvised here.

### 3. Vuong (1989): complete page range restored

The JSTOR issue record gives *Econometrica* **57**(2), **307–333**. The earlier note saying
that JSTOR carried only the start page was incorrect. DOI:

https://doi.org/10.2307/1912557

### 4. Holm (1979): issue and stable item restored

The JSTOR issue record gives *Scandinavian Journal of Statistics* **6**(2), **65–70**.
`10.2307/4615733` should not be presented as a DOI; the checkable record is the stable JSTOR
item URL:

https://www.jstor.org/stable/4615733

### 5. Degree of Urbanisation manual: ILO restored

The earlier citation omitted the **International Labour Organization (ILO)** from the six
organizations named by the official Eurostat record. The citation now names the European
Commission, FAO, UN-Habitat, ILO, OECD and the World Bank, and links the official record as
well as the DOI:

- https://ec.europa.eu/eurostat/web/products-manuals-and-guidelines/-/ks-02-20-499
- https://doi.org/10.2785/706535

The manual's CC BY-NC-SA 3.0 IGO notice was confirmed and did not require correction.

## References checked without a material correction

Publisher or registry metadata agreed with the existing author, year, title, journal,
volume and pagination or article number for the following works:

- Auerbach and Ciccone (2023); Batty (2023); Rybski (2013); Rybski and Ciccone (2023).
- Miškinis (2011); Allen (2023); Strahler (1952); Keylock et al. (2021).
- Soo (2005); Nitsch (2005); Berry and Okulicz-Kozaryn (2012).
- Clauset, Shalizi and Newman (2009); Virkar and Clauset (2014); Gabaix and
  Ibragimov (2011); Kendall (1938).

The official World Development Indicators record confirms CC BY 4.0, and Eurostat's
official reuse page supports the licence description used for its data. The 2012 date for
Berry and Okulicz-Kozaryn in the README is correct; the 2011 date survives only in the
dated Stage-0 search record and is not silently rewritten here.

## Prose and presentation corrections

- Added a concise **Overview** as the default site tab and renamed the prior landing tab
  **Full report**. The full technical report remains rendered verbatim from `REPORT.md`.
- Removed session numbers, katflow identifiers, SHA prefixes and verifier mechanics from
  the masthead. Detailed provenance remains in Data & custody, the audit files and the
  repository.
- Normalized the first attribution to **Kimi (Kimi K3), Codex (GPT-5.6 Sol), and Qoder
  (Qwen3.8-Max)**. `CREDITS.md` retains the important qualification that model mappings are
  the owner's attribution record while harness names are what the documents themselves
  attest.
- Replaced three stale statements that described the already published project as awaiting
  publication.
- Preserved the Stage-3 record that the Scaruffi path then probed returned 404, while
  correcting current-status passages to say that the page was later obtained and preserved
  but has not been ingested or analysed.
- Updated the ALZ wording from a “probable” separate project to the owner's actual split
  decision.
- Collapsed the long footer provenance and citation ledger by default. Nothing was deleted;
  the complete bibliography and audit trail remain one click away.

## Future sessions — notes only

These items were deliberately not analysed in this pass:

1. **Scaruffi comparator.** The page was captured after publication (HTTP 200, 568 table
   rows) for preservation only. Before it can enter DC-3c, a future session must add a dated
   `data/CONTRACT.md` addendum and then run the comparison as a new analysis.
2. **Ciccone source-version reconciliation.** Compare the February 2021 working translation
   with the open 2023 release, including its added Figure 4 and retained numerical
   mismatches. No new conclusion is claimed here.
3. **ALZ bibliometrics.** This remains a separate future project because it tests Rybski and
   Ciccone (2023), not Auerbach's 1913 empirical claims.

## Verification boundary

The existing 109-claim verifier passed with zero failures, and the complete unit suite passed
10/10. Two consecutive builds produced byte-identical, self-contained copies of
`results/explorer.html` and `docs/index.html` (187,154 bytes; SHA-256
`cdc3abdd1799e6df6af8811c93fb6570ed3810963c856d071aaf263eb41d8413`). Inline JavaScript
parsed successfully; all eight report anchors resolved; no duplicate IDs were present; and direct
browser QA covered the default Overview, all interactive tabs, a narrow mobile view and a
1440-pixel desktop view with no console errors. The tab bar's ARIA relationships, roving tab stop,
Left/Right/Home/End navigation and Overview-to-panel focus transfer were exercised directly after
independent review identified the initial accessibility gap. The live publication is updated only
after these gates and independent review.
