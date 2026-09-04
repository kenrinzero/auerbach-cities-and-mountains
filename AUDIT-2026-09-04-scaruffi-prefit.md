# Independent Scaruffi pre-fit audit — 2026-09-04

**Terminal status at `2a3e8bed95878c9c1f770e08e09c70f2ed671e57`:
RETIRED BEFORE FIT — the pre-fit gate did not advance.** The final fresh-context
re-audit found that production trace bindings remained declarative rather than fully
enforced. The owner elected retirement instead of another validator redesign. No
parser, fit, private trace, or current-snapshot analysis was run; the historical
disposition remains `not_identifiable`. See `results/scaruffi-followup-closure.md`.

**Earlier verdict at `8ef9bfbcdc93cedca21fa92ae52354fdf481b11d`: PASS AFTER
OWNER-APPROVED CORRECTION — retained below as audit history and superseded by the later
fresh-context re-audit.**

**Historical verdict at `eee031dd1a724d538c3d2f302eab680842e58d08`: FAIL —
retained below as the original audit record.**

## Initial audit — historical record

**Verdict: FAIL — the pre-fit gate is not passed.**

This was a fresh-context scientific audit of the governance freeze at commit
`eee031dd1a724d538c3d2f302eab680842e58d08`. No model was fitted, no Scaruffi
row-level content was reproduced, and no governance, test, code, receipt, public
report/site, or private-evidence file was modified.

## Findings

### PF-1 — HIGH — the transformed benchmark relation is mathematically mistranscribed

- **Files/lines:** `results/scaruffi-source-audit.md:13-15` and
  `data/scaruffi-followup-plan.json:166-170`.
- **Evidence:** The official publisher PDF, p. 22, prints
  `h(x) = h_1 exp(-beta x^alpha)`, with `alpha = 0.54044`,
  `beta = 3.1170 x 10^-2`, and `h_1 = 8848 m`. It follows directly that
  `ln(h_1 / h(x)) = beta x^alpha`; in the displayed double-log coordinates the
  linearization is
  `ln(ln(h_1 / h(x))) = ln(beta) + alpha ln(x)`. The freeze instead states
  `ln(h_1 / h_n) = alpha x + beta in double-log coordinates`. That statement is
  incompatible with the correctly transcribed rank curve and parameters. Direct
  evaluation of the printed curve gives 3291.265 m at rank 600 and 3020.302 m at
  rank 700, confirming the printed integer benchmarks.
- **Expected correction:** Before implementation or fitting, make a dated,
  owner-adjudicated governance correction that states the power relation and its
  double-log linearization exactly. Preserve the existing rank-origin and fitting-
  recipe non-identifiability; do not infer an objective or choose a favorable
  recipe.

### PF-2 — HIGH — the parser/anomaly contract does not determine one diagnostic output

- **Files/lines:** `data/scaruffi-followup-plan.json:64-111`, especially
  `:81-91`; `results/scaruffi-source-audit.md:63-69`.
- **Evidence:** The plan fixes anomaly field names and their order, but not the
  value type, member fields, grouping key, group/member sort order, or whether
  `blank_extra_cells` counts cells, rows, or emits records. This is observable in
  the held captures: each target row has two blank trailing cells, so the current
  capture has 565 affected rows but 1,130 blank extra cells (the historical capture
  has 555 affected rows and 1,110 cells). The evidence audit reports only "blank
  extra cells on all 565 target rows." Both 565 and 1,130 are compatible with the
  frozen wording. The contract also does not freeze exact decimal arithmetic or a
  rounding rule for kilometre-to-metre conversion before `canonical_metres` is
  used for duplicate and mapping keys. Therefore independently written parsers can
  produce different anomaly values or keys while satisfying the prose.
- **Expected correction:** Freeze the complete anomaly value schema, exact group
  and member keys, ordering, row-versus-cell counting semantics, and exact decimal
  conversion/canonicalization before implementation. Add public synthetic
  conformance vectors that exercise every anomaly field without reproducing source
  rows.

### PF-3 — HIGH — the private trace and fingerprint freeze is incomplete

- **Files/lines:** `data/scaruffi-followup-plan.json:453-506`, especially
  `:493-506`; approved design
  `docs/superpowers/specs/2026-09-04-scaruffi-followup-design.md:142`.
- **Evidence:** The plan names the top-level trace keys and specifies row-object and
  mapping-assignment key order, but it does not define the required inner fields,
  types, and key order for `source_identities`, `candidate`, `row_identities`,
  `aggregate_counts`, or `fingerprints`. It also contains no synthetic expected row,
  membership, mapping, or trace hashes. The approved design explicitly requires
  exact field order, decimal canonicalization, JSON encoding, and synthetic expected
  hashes to be frozen before fitting. Multiple byte-distinct trace objects can
  therefore satisfy the current plan, and there is no pre-fit oracle for an
  independently implemented fingerprint encoder.
- **Expected correction:** Freeze the complete nested trace schema and ordering,
  including every required source identity, candidate field, ordinal list,
  per-source row list, aggregate-count field, and fingerprint field. Add synthetic
  input vectors and exact expected hashes/trace bytes, then obtain a new genuinely
  fresh-context audit before parser or fitting work.

## Checks that were otherwise clean

- The official six-page publisher PDF was independently retrieved from
  `https://www.lmaleidykla.lt/ojs/index.php/geologija/article/download/1615/632/0`:
  442,264 bytes, SHA-256
  `a94e215892fb4cf86ca4e14e986d1212dc3252e798654317867ef5f88b9e7e83`.
  Pages 21-25 were visually inspected. Apart from PF-1, every frozen printed value
  and half-last-digit tolerance is correct, including Tables 1-3, equations (2),
  (5)-(7), residuals, correlations, and the preserved `177.8` and `N=540`/`N=548`
  source inconsistencies.
- Arquivo.pt's live CDX record and replay independently confirmed the 2009 capture,
  archive time, original URL, original Last-Modified header, 100,381-byte replay,
  and SHA-256
  `813731ac6000d00cab2c7d7915a294a8b2dbf6551b0a5fc4a34f9aa0d882a571`.
  Independent private structural inspection found one exact-header target table and
  555 rows. The current capture independently matched 102,018 bytes, SHA-256
  `4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe`,
  and 565 target rows.
- The historical candidate contains all 555 source ordinals and no exclusion. The
  frozen plan contains `excluded_ordinals: []`, prohibits top-548, mapping-based,
  and benchmark-based selection, and prevents benchmark proximity from upgrading
  `not_identifiable`. Independent diagnostic mapping assigned 554 exact pairs, one
  same-name/different-height pair, zero historical-only rows, and ten current-only
  rows without filtering membership.
- S0 is the complete 565-row current snapshot. S1 deterministically retains 564 rows
  under the exact normalized-name-and-height key. Both bootstrap counts are 500;
  seeds are 20260904 and 20260915. The freeze expressly excludes both arms from the
  original Stage-3 Holm family and bars changes to accepted Stage-3 verdicts.
- `git ls-files data/raw/scaruffi-2026-09-03` is empty; the raw captures, archive
  manifest, and private-trace path are ignored. No tracked row-level Scaruffi source
  or row-complete substitute was found.
- Governance commit `eee031dd1a724d538c3d2f302eab680842e58d08` is `HEAD`, has
  no descendant commit, contains only the three governance documents, JSON plan,
  and focused plan test, and predates all Scaruffi parser/fitting implementation and
  receipts, which are absent. Original protected data and Stage-0 through Stage-3
  artifacts are unchanged from `4c43cc4`; `results/stage3-recompute.txt` remains
  SHA-256 `6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7`.
  The independently recomputed 59-file governance digest is
  `40c9de30bc603a40441391d2e3554e60395272d880f9c41ddfd14c7a530fdce1`,
  matching the freeze.

Because the verdict is not PASS, the conditional focused/full acceptance suite,
report verifier, and audit commit were not run. Task 3 must not start from this
freeze.

## Fresh-context re-audit after owner-approved correction

**Re-audit verdict: PASS AFTER OWNER-APPROVED CORRECTION.**

This re-audit was performed independently against corrected governance commit
`8ef9bfbcdc93cedca21fa92ae52354fdf481b11d`, whose parent is the originally audited
freeze. The uncommitted initial audit above was preserved before this edit at 7,212
bytes and SHA-256
`3f66440e066ca8d9f4be6894b477380f7f23244a5c5435b3bb5214572bec9fb6`.
The fresh auditor did not author either governance commit and did not rely on the
initial audit until after independently reviewing the approved design, source audit,
three governance documents, machine-readable plan, focused tests, Task 2 Step 7,
the held private sources, and the official Miškinis paper.

### PF-1 re-audit — RESOLVED

- The official publisher PDF was retrieved independently: 442,264 bytes, SHA-256
  `a94e215892fb4cf86ca4e14e986d1212dc3252e798654317867ef5f88b9e7e83`.
  Visual inspection of displayed pp. 22–25 confirms equation (2),
  `h(x) = h_1 exp(-βx^α)`, and equation (14),
  `ln(h_1 / h) = βx^α`. Therefore the corrected double-log relation is
  `ln(ln(h_1 / h(x))) = ln(β) + α ln(x)`.
- The corrected formulas are frozen in
  `data/scaruffi-followup-plan.json:555-557`, stated in the source evidence at
  `results/scaruffi-source-audit.md:15`, and carried by the dated correction
  amendments in the three prose authorities. They leave rank-origin and fitting-
  recipe ambiguity unresolved, as required.
- Independent calculation with `h_1 = 8848`, `α = 0.54044`, and `β = 0.031170`
  gives 3,291.265 m at rank 600 and 3,020.302 m at rank 700. Independent literal
  comparison against the PDF confirmed the complete frozen benchmark set and
  half-last-printed-digit tolerances: sample/floor, curve parameters, residuals,
  spectral expression, inverse-count expression, mean errors, Tables 1–3,
  correlations, and the preserved `177.8` and `N = 540`/`N = 548` source
  inconsistencies. Printed integers remain exact-match benchmarks.

### PF-2 re-audit — RESOLVED

- Exact `Decimal` parsing, kilometre/metre conversion, and canonical-metre text are
  now fixed at `data/scaruffi-followup-plan.json:93-98`. The ten anomaly arrays have
  complete record/member fields, grouping keys, inclusion rules, group/member order,
  and deterministic hard-fail classification under the schema beginning at line 99.
  Blank extras are explicitly one record per cell; targets are 1,110 historical and
  1,130 current cell records.
- The valid and failure vectors at line 218 exercise every anomaly field. An
  independent implementation reproduced the valid vector counts
  `3,1,1,1,1,2,1,0,2,0` and failure-vector counts
  `3,0,0,0,0,0,2,1,0,1` in frozen field order, including the ordered hard-fail
  reasons `missing_required_field`, `nonblank_extra_cell`.
- Independent private structural parsing confirmed both unique target tables and
  their contract-bound aggregates. Historical: 555 rows, 554 kilometre tokens, one
  metre token, eight repeated-name groups, seven same-name/different-height groups,
  one exact-name-height group, 59 height-tie groups involving 134 rows, seven
  adjacent inversions, no missing/nonblank-extra cells, and 1,110 blank-extra-cell
  records. Current: 565 rows, 564 kilometre tokens, one metre token, eight repeated-
  name groups, seven same-name/different-height groups, one exact-name-height group,
  60 height-tie groups involving 136 rows, seven adjacent inversions, no missing/
  nonblank-extra cells, and 1,130 blank-extra-cell records.

### PF-3 re-audit — RESOLVED

- The private-trace authority now fixes row-identity encoding, key order, assignment
  key/order, membership and mapping encodings, all top-level keys, all nested keys,
  ordinal and row-list types, aggregate/fingerprint keys, and canonical JSON
  serialization at `data/scaruffi-followup-plan.json:859-945`.
- From the public synthetic input—not from the focused test—the re-audit independently
  derived all eleven row hashes, the exact-first/name-second mapping, membership hash
  `f7fee5af6130cc782f140d159b56364349d37be14ea502e9e8cd42e99b2a3ac6`,
  mapping hash
  `f5f8bc4c04fd4883cb60b67d26eb5d3f9de360f61df83d943eeebc3d4c47348e`,
  and the canonical 6,901-byte trace SHA-256
  `78d4f66a82da94ab51d699bcbfbf96302e4cca9b59f668649a2fc03903de7ee6`.
  Every result exactly matches the oracle at lines 946–1117.

### Remaining pre-fit checks — PASS

- The historical capture matches its 100,381-byte SHA-256 contract, and its
  independently verified 910-byte manifest has SHA-256
  `552c29fbe850d5e7b2aa730d9a1eca733551c89ab064389eba6b13d6a6440519`.
  The current capture matches its 102,018-byte SHA-256 contract. Each recomputed
  content identity matches the frozen ASCII identity.
- The evidence-supported candidate includes source ordinals 1–555 and has
  `excluded_ordinals: []`. No top-548, mapping-based, or benchmark-driven selection
  exists. `not_identifiable` is fixed and cannot be upgraded by benchmark proximity.
  Independent mapping gave 554 exact, one same-name/different-height, zero
  historical-only, and ten current-only assignments; both source sides form total
  partitions and the 555-row membership is unchanged.
- S0 is all 565 current rows; S1 keeps the earliest ordinal for the sole exact-name-
  and-height excess row and therefore has 564 rows. Joint and GoF bootstraps are 500
  each, with analysis seed 20260904 and jitter seed 20260915. The current arms do not
  join the original Stage-3 Holm family and cannot alter an accepted verdict lane.
- The published baseline digest was independently recomputed at `4c43cc4` as 59 files,
  SHA-256 `4821ab10a6ad62ff7bea2e9f8f876730a7d98fd9fef6d98ba67dce5606e29110`.
  At corrected HEAD the immutable 57-file digest is
  `60ac68e50e32d51c85d8536fafe073cf8005a64b7585e7ce76902a61c568c62f`,
  the governance 59-file digest is
  `0f3f403ff726cb14f8ce7831c4e3f9e75ba025f1fb678ed2cde9a3bc2319bdcd`,
  and `results/stage3-recompute.txt` remains SHA-256
  `6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7`.
- Git chronology from `4c43cc4` through corrected HEAD contains only plans, source
  audit, ignore rules, governance, and the focused governance test for this follow-up.
  The original freeze `eee031d` precedes correction `8ef9bfb`; neither history nor
  the tree contains a Scaruffi parser, fitter, private trace, or fit receipt.
- `git ls-files data/raw/scaruffi-2026-09-03` is empty, and `git check-ignore -v`
  confirms both captures, the historical manifest, and the prospective private trace
  are excluded. No tracked row-complete Scaruffi source or substitute was found.

The corrected governance freeze is scientifically complete and deterministic for the
authorized pre-fit boundary. This verdict authorizes eligibility for Task 3 only under
the frozen contracts; it does not implement or pre-approve any parser or fit result.

## Final re-audit and owner disposition — terminal record

A later fresh-context, read-only re-audit at
`2a3e8bed95878c9c1f770e08e09c70f2ed671e57` reproduced the 14/14 focused tests,
52/52 full tests, 109/109 number verifier, source aggregates, privacy boundary, and
protected hashes. It nevertheless returned **FAIL** on one remaining Important finding:
the executable validator accepted production-shaped traces with wrong exact source
identities, candidate ID/rule, shifted ordinal ranges, or reordered assignments when
their dependent hashes were recomputed consistently. The written production invariants
were therefore stronger than their executable enforcement.

The owner accepted the audit and chose retirement rather than another conformance-only
correction. That choice is now terminal: status `retired_before_fit`, historical
disposition `not_identifiable`, current-snapshot analysis `not_run`. Task 3 was never
started. Reopening requires new independent evidence identifying the exact historical
548-row membership/exclusions or the unique Miškinis fitting recipe; validator work by
itself is not a reopening condition.
