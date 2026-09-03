# Stage 1 transcription — double-entry protocol record (2026-09-02, Kimi)

Per PREREGISTRATION.md §3.1: Tables 1–3 + Europe-complex numbers transcribed from the
scan (`paper/Auerbach 1913 — Das Gesetz ….pdf`) by double entry. The 2023 Ciccone
translation was never used as a numeric source.

- **Pass A** = the OCR markdown already in `paper/` (tesseract `deu`, cross-checked
  against the Ciccone parallel transcription by the Stage-0 session).
- **Pass B** = fresh manual reading of the scan image (2026-09-02, Kimi): pages
  rendered at native scan resolution (300 dpi; Tafel 14 at its native 4057×5740),
  every table cell read from full-resolution crops, Fraktur digit ambiguities
  (3/8, 5/6, 6/8) resolved by side-by-side glyph comparison against known-reference
  digits on the same page plus arithmetic consistency (implied complex population =
  A.K./Sp.K. vs. the era census figure).

## Diff outcome

| Cell | Pass A | Pass B (scan) | Resolution |
|---|---|---|---|
| Table 2, Schweiz A.K. | 2,6 | **2,8** | Scan wins. Glyph has the closed upper loop of the reference 8 (cf. Österreich-Ungarn 16,8), not the open top of the reference 6 (cf. Spanien 8,6). Arithmetic: 2.8/0.75 implies pop. 3.73 Mill. vs. actual 1910 census 3.753 Mill.; 2,6 would imply 3.47 Mill. — off. Ciccone prints 2.6; pass A was cross-checked against Ciccone, so their agreement is not independent. Third Ciccone-side numeric slip (after 47,2/64,6, receipt D2). |
| Table 2, Britisch-Indien A.K. | 36,0 | 36,0 | Glyph visually 3/9-ambiguous; resolved arithmetically (96,0 could never yield Sp.K. 11). |
| Tafel 14 Abb. 1 annotation | note said "4503/94 = 47,9; 100·47,9/62,2 = 77" | **Mittelwert 4503/94 = 47,8; Sp.K. 100·47,8/64,5 = 74** | Pass A's figure-placeholder note misrecorded the Tafel; the Tafel agrees with the text (47,8 / 64,5 / 74). Note: 4503/94 = 47.90 arithmetically — the printed 47,8 vs. the 4503 numerator is analyzed in stage1-recompute.txt. |
| All other cells (Table 1: 94×3; Table 2 remaining; Table 3; Europe text numbers; time-series prose; AU-C3 cutoff values 47,2/48,1) | — | identical | No discrepancy. Table 1 rows 1–47, 48–94, and the bottom rows 46/47/93/94 read at full resolution; the printed A.K. column additionally verified against round(rank × E.Z./100) — see the assertion table in stage1-recompute.txt. |

Pass-B reads of Tafel 14 Abb. 3 annotations (administrative time series): 1910 A.K. 49,5 /
Sp.K. 77; 1905 42,2 / 70; 1900 34,2 / 61; 1895 28,7 / 55 — match pass A's notes, adding the
1905 row (42,2 / 70) which pass A had not recorded.

## Files landed

- `data/derived/auerbach-1913-table1.csv` — 94 rows (rank, place, E.Z. thousands, printed A.K.)
- `data/derived/auerbach-1913-table2.csv` — 12 states (A.K., Sp.K.; Schweiz = 2,8 per scan)
- `data/derived/auerbach-1913-table3.csv` — 6 Prussian provinces
- `data/derived/auerbach-1913-europe.csv` — Europe-complex numbers (334 places, A.K. 169, 432 Mill., Sp.K. 39)
- `data/derived/auerbach-1913-tafel14-and-text.csv` — Tafel 14 annotations + text-stated numbers (AU-C3 cutoffs, time series)
- `data/derived/MANIFEST.sha256` — hashes of the above
