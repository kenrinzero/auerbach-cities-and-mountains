# Investigation checklist — standing lens for every paper

Adopted 2026-07-24 (ARIS doctrine item 8 —
`.atelier/suggestions/archive/2026-07-21-aris-doctrine-adoption.md`; ARIS's
self-audit taxonomies inverted into an audit lens for *published* papers;
credit wanshuiyin/Auto-claude-code-research-in-sleep, MIT). Each new paper
folder's `AGENTS.md` references this file. Walk it during step 1 (claim
inventory) and again before any defensible-claim writeup.

## Failure-mode lenses (from `paper-claim-audit`, inverted)

- [ ] **Number inflation** — headline numbers larger than what the tables and
      figures support; check abstract/intro claims against the actual result
      tables.
- [ ] **Best-seed cherry-pick** — single-run or best-of-N results presented as
      typical; look for missing variance, missing seed counts, suspiciously
      clean curves.
- [ ] **Config mismatch** — the described setup (architecture, hyperparams,
      data splits) doesn't match what the results require or what appendix /
      code fragments reveal.
- [ ] **Aggregation mismatch** — means, medians, and maxes mixed or swapped
      between text and tables; per-task vs averaged numbers conflated.
- [ ] **Delta arithmetic error** — claimed improvements that don't equal the
      difference of the two numbers cited; recompute every delta.
- [ ] **Caption–table mismatch** — captions or prose claiming what the panel
      doesn't show (the steerable-lens case: prose says "moves smoothly in the
      intended direction," pixels show deform-and-flip).
- [ ] **Scope overclaim** — general claims from narrow evidence (one dataset,
      one metric, one regime); map each claim to the exact evidence backing it.

## Fraud-pattern screens (from `experiment-integrity`, inverted)

- [ ] **Fake ground truth from model outputs** — "labels" or references that
      are themselves model-generated, then scored against.
- [ ] **Self-normalized scores** — metrics normalized by the method's own
      quantities, so improvement is built into the denominator.
- [ ] **Phantom results** — numbers, panels, or baselines referenced but never
      shown, or shown but traceable to no described procedure.
- [ ] **Pilot-called-comprehensive** — small exploratory runs narrated as full
      evaluations ("we evaluate extensively on…").

## Usage notes

- These are **lenses, not verdicts**: a checked box means "screened," and any
  hit still needs the full evidence chain (reproduction, measurement,
  pre-registered predictions) before it lands in a writeup.
- No intent language anywhere — findings are stated as incompatibilities and
  unsupported claims, per the project's honesty ceiling.
