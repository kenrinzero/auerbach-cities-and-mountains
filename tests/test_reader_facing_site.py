import html
import re
import subprocess
import sys
import unittest
from pathlib import Path

from src import build_explorer


ROOT = Path(__file__).resolve().parents[1]


def element(source, tag, element_id=None):
    identifier = "" if element_id is None else rf'(?=[^>]*\bid="{re.escape(element_id)}")'
    match = re.search(
        rf"<{tag}\b{identifier}[^>]*>(.*?)</{tag}>",
        source,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        raise AssertionError(f"missing <{tag}> element {element_id or ''}".strip())
    return match.group(0)


def visible_text(fragment):
    without_tags = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(without_tags)).strip()


def css_properties(source, selector):
    match = re.search(rf"{re.escape(selector)}\{{([^}}]+)\}}", source)
    if not match:
        raise AssertionError(f"missing CSS selector {selector}")
    return {
        name.strip(): value.strip()
        for declaration in match.group(1).split(";")
        if ":" in declaration
        for name, value in [declaration.split(":", 1)]
    }


class ReaderFacingSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build = subprocess.run(
            [sys.executable, "src/build_explorer.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if build.returncode:
            raise AssertionError(build.stdout + build.stderr)
        cls.page = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.builder = (ROOT / "src" / "build_explorer.py").read_text(encoding="utf-8")

    def test_overview_is_the_short_default_landing_page(self):
        overview = element(self.page, "section", "tab-overview")
        text = visible_text(overview)
        self.assertLess(self.page.index('id="tab-overview"'), self.page.index('id="tab-report"'))
        self.assertRegex(self.page, r'\["overview","Overview"\],\["report","Full report"\]')
        self.assertIn('show("overview")', self.page)
        self.assertNotIn(" hidden", overview.split(">", 1)[0])
        for heading in ("What we found", "What is new here", "1913 cities", "Modern cities", "Mountains"):
            self.assertIn(heading, text)
        self.assertIn("Read the full report", text)
        self.assertGreaterEqual(len(text.split()), 320)
        self.assertLessEqual(len(text.split()), 620)
        for provenance_term in ("katflow", "session #", "SHA-256", "receipt", "harness"):
            self.assertNotIn(provenance_term.lower(), text.lower())

    def test_overview_claims_and_qualifiers_are_pinned(self):
        overview = element(self.page, "section", "tab-overview")
        text = visible_text(overview)
        for expected in (
            "rank 15",
            "ξ = 0.9801",
            "ξ ∈ [0.911, 1.089]",
            "all 94",
            "roughly 70%",
            "nine-complex",
            "exploratory",
            "all four primary arms",
            "bounded support",
            "bounded or cutoff families win in the global, lower-prominence and Himalaya arms",
            "supports no tectonic causal mechanism",
            "Coverage bias in summit lists points toward the mountain result",
        ):
            self.assertIn(expected, text)

        new_here_match = re.search(
            r'<div class="card"><h3>What is new here</h3>.*?</div>',
            overview,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(new_here_match)
        new_here = visible_text(new_here_match.group(0))
        self.assertIn("Appendix Figure A1", new_here)
        self.assertIn("−1.15", new_here)
        self.assertIn("log rank on log population", new_here)

    def test_a4_lane_explains_the_frozen_rule_and_companion_evidence(self):
        report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
        overview = visible_text(element(self.page, "section", "tab-overview"))
        scoreboard = " ".join(
            description
            for prediction, _, description in build_explorer.PREDICTIONS
            if prediction in {"P5", "P6"}
        )
        mountains = visible_text(element(self.page, "section", "tab-mount"))

        for artifact, text in (
            ("REPORT.md", report),
            ("README.md", self.readme),
            ("Overview", overview),
            ("Mountains", mountains),
        ):
            with self.subTest(artifact=artifact):
                self.assertIn("A4", text)
                self.assertIn("−25.47", text)
                self.assertIn("0.5619", text)
                self.assertIn("0.0020", text)
                self.assertIn("0.7665", text)

        for artifact, text in (
            ("REPORT.md", report),
            ("Overview", overview),
            ("Mountains", mountains),
        ):
            with self.subTest(artifact=artifact, rule="D9 comparison"):
                self.assertIn(
                    "no bounded alternative wins on the preregistered favorable Vuong comparison at p < 0.05",
                    text,
                )

        for artifact, text in (("REPORT.md", report), ("Mountains", mountains)):
            with self.subTest(artifact=artifact, rule="frozen H-MB rule"):
                self.assertIn(
                    "at least one of M3, M2, M5, or M6b beats M1 on a favorable Vuong comparison at p < 0.05",
                    text,
                )
                self.assertIn(
                    "M1 is rejected on GoF while at least one alternative is not",
                    text,
                )
                self.assertIn("AICc is companion evidence", text)
                self.assertNotIn("M3 beats M1 on the LRT", text)
                self.assertNotIn("requires a preregistered bounded alternative to have both lower AICc", text)

        self.assertNotIn("has both lower AICc and significant Vuong", report)
        self.assertNotIn("M6b GoF p = 0.0020 keep it out", report)
        for expected in ("A4", "-25.47", "0.5619", "0.0020", "0.7665",
                         "no bounded alternative wins on the preregistered favorable Vuong comparison at p < 0.05"):
            self.assertIn(expected, scoreboard)
        self.assertNotIn("M6b GoF p 0.0020 keep", scoreboard)
        self.assertNotIn("M6b GoF p 0.0020 keep", mountains)

        self.assertIn("lower AICc alone does not switch the lane", report)
        self.assertIn("lower AICc alone does not switch the lane", mountains)
        self.assertIn("A0/R1/R2/R3/A4", report)

    def test_self_containment_allows_only_the_exact_data_favicon_link(self):
        self.assertTrue(
            hasattr(build_explorer, "assert_self_contained_html"),
            "builder must expose its real self-containment boundary for pressure testing",
        )
        validate = build_explorer.assert_self_contained_html
        validate('<link rel="icon" href="data:,">')
        for forbidden in (
            '<link rel="stylesheet" href="//cdn.example/style.css">',
            '<link rel="stylesheet" href="style.css">',
            '<link rel="icon" href="data:image/svg+xml,<svg></svg>">',
        ):
            with self.subTest(forbidden=forbidden):
                with self.assertRaises(AssertionError):
                    validate(forbidden)

    def test_reader_text_measures_match_the_approved_axtell_like_layout(self):
        overview = css_properties(self.page, ".overview")
        overview_lede = css_properties(self.page, ".overview-lede")
        report = css_properties(self.page, ".rp-measure")
        report_code = css_properties(self.page, ".rp code")

        self.assertEqual("980px", overview["max-width"])
        self.assertEqual("none", overview_lede["max-width"])
        self.assertEqual("800px", report["max-width"])
        self.assertEqual("auto", report["margin-inline"])
        self.assertEqual("anywhere", report_code["overflow-wrap"])

    def test_tabs_have_keyboard_semantics_and_overview_actions_transfer_focus(self):
        for code in (
            'b.id="navtab-"+t[0]',
            'b.setAttribute("aria-controls","tab-"+t[0])',
            'panel.setAttribute("aria-labelledby",b.id)',
            'b.tabIndex=t[0]===id?0:-1',
            'if(!["ArrowLeft","ArrowRight","Home","End"].includes(ev.key))return',
            "activateFromOverview('report')",
            "activateFromOverview('score')",
            "panel.focus()",
        ):
            self.assertIn(code, self.page)

        details = element(self.page, "details")
        self.assertNotIn(" open", details.split(">", 1)[0])
        self.assertIn("report_html, report_toc = render_report_md(V.REPORT_PATH)", self.builder)
        self.assertIn('.replace("__REPORT__", report_html)', self.builder)

    def test_masthead_maps_harness_names_to_models_without_receipt_clutter(self):
        header = visible_text(element(self.page, "header"))
        for attribution in (
            "Kimi (Kimi K3)",
            "Codex (GPT-5.6 Sol)",
            "Qoder (Qwen3.8-Max)",
        ):
            self.assertIn(attribution, header)
        for provenance_term in ("Stage-4", "SHA-256", "receipt", "katflow", "session"):
            self.assertNotIn(provenance_term, header)

    def test_data_tab_reports_scaruffi_as_retired_before_fit(self):
        custody = visible_text(element(self.page, "section", "tab-data"))
        self.assertIn("Scaruffi", custody)
        self.assertIn("retired before ingestion or fitting", custody)
        self.assertIn("not identifiable", custody)
        self.assertNotIn("not yet ingested or analysed", custody)
        self.assertNotIn("pending a dated data-contract addendum", custody)
        self.assertNotIn("comparator not obtainable", custody)

        report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("retired before ingestion or fitting", report)
        self.assertIn("controlled disposition **`not_identifiable`**", report)
        possibilities_line = next(
            line for line in report.splitlines()
            if line.startswith("Unpursued possibilities, not open project work:")
        )
        self.assertNotIn("548-summit comparator", possibilities_line)
        self.assertNotIn("Still open and non-blocking:", report)

    def test_public_report_does_not_claim_the_live_project_is_unpublished(self):
        for stale in (
            "Publishing: none",
            "publication still requires the user's separate signal",
            "no publication of any kind",
            "probable separate project",
        ):
            self.assertNotIn(stale, visible_text(self.page))

    def test_full_report_opens_as_a_finished_publication(self):
        report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("**Project links:**", report)
        project_links = report.index("**Project links:**")
        abstract = report.index("## Abstract")
        notation = report.index("Notation is the preregistration's §1")
        question = report.index("## 1. The question")
        audit = report.index("## 7. Audit and provenance")
        reproducibility = report.index("## 8. Reproducibility")
        self.assertLess(project_links, abstract)
        self.assertLess(abstract, notation)
        self.assertLess(notation, question)
        self.assertLess(question, audit)
        self.assertLess(audit, reproducibility)
        self.assertNotRegex(report[audit + 1:reproducibility], r"(?m)^## ")
        opening = report[:question]
        self.assertNotIn("katflow #", opening)
        self.assertNotIn("Deliver stage", opening)

    def test_report_headings_are_sequential_after_the_editorial_move(self):
        report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
        numbered = re.findall(r"(?m)^## ([1-8])\. ", report)
        self.assertEqual(list("12345678"), numbered)
        self.assertIn("## 2. Results", report)
        for subsection in ("2.1", "2.2", "2.3", "2.4"):
            self.assertRegex(report, rf"(?m)^### {re.escape(subsection)} ")
        self.assertIn("## 7. Audit and provenance", report)
        self.assertIn("All three are pre-registered and all three are reported (§2.3).", report)
        self.assertIn("against the draft of this report before §3 was finalized", report)

    def test_current_provenance_includes_addendum_4_and_the_source_audit(self):
        report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
        contract = (ROOT / "data" / "CONTRACT.md").read_text(encoding="utf-8")
        historical = (
            "Its source enum began as a Task 1\n"
            "proposal; the completed fresh-context Task 2 disposition is recorded immediately below."
        )
        disposition = "**Task 2 disposition — 2026-09-03:**"
        self.assertIn(historical, contract)
        self.assertIn(disposition, contract)
        self.assertLess(contract.index(historical), contract.index(disposition))
        current_disposition = contract[contract.index(disposition):]
        self.assertIn("STANDS WITH CORRECTION", current_disposition)
        self.assertIn("source-description corrections only", current_disposition)
        self.assertIn("AUDIT-CICCONE-SOURCE-RECONCILIATION.md", current_disposition)
        self.assertNotIn("pending the fresh-context Task 2 audit", current_disposition)
        self.assertNotIn("it is not independently confirmed here", current_disposition)

        for artifact, text in (
            ("README.md", self.readme),
            ("REPORT.md", report),
            ("src/build_explorer.py", self.builder),
        ):
            with self.subTest(artifact=artifact):
                self.assertNotIn("Addenda 1–3", text)
                self.assertNotIn("Addenda 1&ndash;3", text)
        self.assertIn("Addenda 1–4", self.readme)
        self.assertIn("Addenda 1–4", report)
        self.assertIn("Addenda 1&ndash;4", self.builder)
        for path in (
            "results/ciccone-2021-2023-source-reconciliation.md",
            "AUDIT-CICCONE-SOURCE-RECONCILIATION.md",
        ):
            self.assertIn(path, self.readme)
            self.assertIn(path, report)

    def test_report_closes_completed_reviewer_followup_statuses(self):
        report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
        self.assertNotIn("the one browser-QA limitation of this environment", report)
        self.assertNotIn("a one-line guard for the latent (never-firing) edge case", report)
        self.assertIn("**Reviewer-follow-up closure — 2026-09-03.**", report)
        self.assertIn("all-ties/non-identification guard", report)
        self.assertIn("browser QA is closed", report)
        self.assertIn("throughout this report", report)
        self.assertIn("the verifier itself performs no refitting", report)
        self.assertNotIn("every quantitative statement below", report)
        self.assertNotIn("this stage refits nothing", report)

    def test_receipt_reconciles_the_protected_scope_from_branch_base(self):
        receipt = (ROOT / "results" / "final-correction-receipt.md").read_text(encoding="utf-8")
        followup = receipt[receipt.index("## reviewer-followup/prepublication-reader-gate") :]
        for expected in (
            "ec9502bb3dd5e2f6369a89e1ff7310c73ed368a145a1436d4536f4e869ea2979",
            "cef09a2e1bdd0a061ea8f0ca4457d2f3ce156a933c2bd4a81a3c700825010e66",
            "4821ab10a6ad62ff7bea2e9f8f876730a7d98fd9fef6d98ba67dce5606e29110",
            "05081d1f5a27a1565fabc1fca9f4f867f9332726",
            "1e1c4597fa997f6097cf59f805721f40c608d1c2",
            "CLAIM_INVENTORY.md",
            "authorized source-audit adjudication",
        ):
            self.assertIn(expected, followup)
        self.assertNotIn("protected-scope recipe remains", followup)

        closure_heading = "## post-review/final-candidate closure — 2026-09-03"
        self.assertEqual(1, receipt.count(closure_heading))
        closure = receipt[receipt.index(closure_heading) :]
        closure_flat = " ".join(closure.split())
        for expected in (
            "09c2e29aebc0163feadc161253c9e1166f19bbe1",
            "final whole-branch review returned **APPROVED** with no new findings",
            "109/109",
            "38/38",
            "201,693 bytes",
            "3b848f1b5d03a45c73fc8c8c5394bac31b981cb429b2f25c9667b06b64f37d0b",
            "6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7",
            "16/16",
            "22/22",
            "4821ab10a6ad62ff7bea2e9f8f876730a7d98fd9fef6d98ba67dce5606e29110",
            "base and historical-value reconciliation is already explained above",
            "UTF-8/LF/no-BOM",
            "inline JavaScript",
            "git diff --check",
            "browser and accessibility coverage",
            "changes only receipt and test evidence",
            "public candidate bytes remain those of `09c2e29`",
            "no push, deployment, or merge occurred",
            "publication still awaits the user's signal",
        ):
            self.assertIn(expected, closure_flat)

    def test_project_report_links_render_as_clickable_anchors(self):
        report_tab = element(self.page, "section", "tab-report")
        self.assertIn("Project links:", visible_text(report_tab))
        self.assertNotIn("Published:", visible_text(report_tab))
        for label, url in (
            ("live site", "https://kenrinzero.github.io/auerbach-cities-and-mountains/"),
            ("public source", "https://github.com/kenrinzero/auerbach-cities-and-mountains"),
        ):
            self.assertIn(f'<a href="{url}">{label}</a>', report_tab)
            self.assertNotIn(f"[{label}]({url})", report_tab)

    def test_report_rule_favicon_and_source_audit_label_are_publication_ready(self):
        report_tab = element(self.page, "section", "tab-report")
        self.assertIn("<hr>", report_tab)
        self.assertNotIn("<p>---</p>", report_tab)
        self.assertRegex(self.page, r'<link\s+rel="icon"\s+href="data:[^"]*">')
        self.assertIn("cross-agent source-version audit", self.readme)
        self.assertNotIn("its independent audit", self.readme)

    def test_current_public_prose_has_no_work_order_voice(self):
        current = visible_text(self.page)
        for stale in (
            "Publishing: none",
            "publication still requires the user's separate signal",
            "this deliverable awaits",
            "probable separate project",
        ):
            self.assertNotIn(stale, current)
        self.assertIn("current regression suite", self.readme)
        self.assertNotRegex(self.readme, r"(?m)^python -m unittest discover -s tests -q # 3 tests$")

    def test_method_provenance_distinguishes_framework_from_implementation(self):
        public_text = self.readme + visible_text(self.page)
        self.assertIn("continuous-data cutoff selector was implemented separately", public_text)
        self.assertIn("statistical framework", public_text)
        self.assertNotIn("imported here by design", public_text.lower())

    def test_public_bibliography_uses_verified_citation_fields(self):
        for expected in (
            "**59**, 74–76, mit Tafel 14",
            "**Ciccone, A. (2021, February).**",
            "**57**(2), 307–333",
            "**6**(2), 65–70",
            "International Labour Organization (ILO)",
        ):
            self.assertIn(expected, self.readme)
        self.assertIn("https://www.jstor.org/stable/4615733", self.readme)
        self.assertIn(
            "https://ec.europa.eu/eurostat/web/products-manuals-and-guidelines/-/ks-02-20-499",
            self.readme,
        )
        self.assertNotIn("**59**(I), 74–76", self.readme)
        self.assertNotIn("59(I): 74–76", visible_text(self.page))
        self.assertNotIn("No DOI exists (confirmed absent from Crossref)", self.readme)

    def test_known_historical_statuses_are_corrected_where_first_encountered(self):
        sweep = (ROOT / "results" / "stage0-novelty-sweep.md").read_text(encoding="utf-8")
        report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("Dated correction — 2026-09-03", sweep)
        self.assertIn("year of record is **2012**", sweep)
        audit_start = report.index("## 7. Audit and provenance")
        stage3_start = report.index("**Stage 3", audit_start)
        stage3 = report[stage3_start:report.index("**Stage 4", stage3_start)]
        normalized_stage3 = re.sub(r"\s+", " ", stage3).strip()
        historical = "the Scaruffi path probed returned 404, so Miškinis's 548-summit list was not obtainable within Stage 3)."
        corrective = "The correct page was subsequently obtained and preserved, but the historical 548-row membership and unique fitting recipe proved not identifiable; the follow-up was retired before ingestion or fitting, with no current-snapshot analysis run."
        self.assertIn(historical + " " + corrective, normalized_stage3)


if __name__ == "__main__":
    unittest.main()
