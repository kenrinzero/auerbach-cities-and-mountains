import html
import re
import subprocess
import sys
import unittest
from pathlib import Path


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
        for heading in ("What we found", "1913 cities", "Modern cities", "Mountains"):
            self.assertIn(heading, text)
        self.assertIn("Read the full report", text)
        self.assertGreaterEqual(len(text.split()), 220)
        self.assertLessEqual(len(text.split()), 520)
        for provenance_term in ("katflow", "session #", "SHA-256", "receipt", "harness"):
            self.assertNotIn(provenance_term.lower(), text.lower())

    def test_overview_claims_and_qualifiers_are_pinned(self):
        text = visible_text(element(self.page, "section", "tab-overview"))
        for expected in (
            "rank 15",
            "ξ = 0.9801",
            "all four primary arms",
            "bounded or cutoff families win in the global, lower-prominence and Himalaya arms",
            "supports no tectonic causal mechanism",
            "Coverage bias in summit lists points toward the mountain result",
        ):
            self.assertIn(expected, text)

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

    def test_data_tab_reports_scaruffi_as_preserved_but_not_ingested(self):
        custody = visible_text(element(self.page, "section", "tab-data"))
        self.assertIn("Scaruffi", custody)
        self.assertIn("obtained and preserved", custody)
        self.assertIn("not yet ingested or analysed", custody)
        self.assertIn("data-contract addendum", custody)
        self.assertNotIn("comparator not obtainable", custody)

    def test_public_report_does_not_claim_the_live_project_is_unpublished(self):
        for stale in (
            "Publishing: none",
            "publication still requires the user's separate signal",
            "no publication of any kind",
            "probable separate project",
        ):
            self.assertNotIn(stale, visible_text(self.page))

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


if __name__ == "__main__":
    unittest.main()
