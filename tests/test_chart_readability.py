import subprocess
import sys
import unittest
from pathlib import Path

try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright
except ModuleNotFoundError:
    PlaywrightError = Exception
    sync_playwright = None


ROOT = Path(__file__).resolve().parents[1]


class ChartReadabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sync_playwright is None:
            raise unittest.SkipTest("Playwright is not installed")

        build = subprocess.run(
            [sys.executable, "src/build_explorer.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if build.returncode:
            raise AssertionError(build.stdout + build.stderr)

        cls.playwright = sync_playwright().start()
        launch_errors = []
        for options in ({}, {"channel": "msedge"}, {"channel": "chrome"}):
            try:
                cls.browser = cls.playwright.chromium.launch(headless=True, **options)
                break
            except PlaywrightError as error:
                launch_errors.append(str(error).splitlines()[0])
        else:
            cls.playwright.stop()
            raise unittest.SkipTest("No Playwright Chromium browser: " + "; ".join(launch_errors))

        cls.page = cls.browser.new_page(viewport={"width": 1180, "height": 900})
        cls.page.goto((ROOT / "docs" / "index.html").as_uri())
        cls.page.wait_for_load_state("load")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "browser"):
            cls.browser.close()
        if hasattr(cls, "playwright"):
            cls.playwright.stop()

    def activate(self, name):
        self.page.get_by_role("tab", name=name, exact=True).click()

    def test_historical_country_labels_fit_inside_the_chart(self):
        self.activate("1913 cities")
        names = [
            "Niederlande",
            "Großbritannien",
            "Belgien",
            "Schweiz",
            "Deutsches Reich",
            "Vereinigte Staaten",
            "Italien",
            "Frankreich",
            "Spanien",
            "Österreich-Ungarn",
            "Europäisches Rußland",
            "Britisch-Indien",
        ]
        result = self.page.evaluate(
            """names => {
                const svg = document.querySelector("#ct2 svg");
                const frame = svg.getBoundingClientRect();
                const labels = [...svg.querySelectorAll("text")]
                    .filter(node => names.includes(node.textContent.trim()));
                const outside = labels.filter(node => {
                    const box = node.getBoundingClientRect();
                    return box.left < frame.left - 0.5 || box.right > frame.right + 0.5 ||
                           box.top < frame.top - 0.5 || box.bottom > frame.bottom + 0.5;
                }).map(node => node.textContent.trim());
                return {count: labels.length, outside};
            }""",
            names,
        )
        self.assertEqual(len(names), result["count"])
        self.assertEqual([], result["outside"])

    def test_slopegraph_endpoint_labels_are_inside_and_do_not_overlap(self):
        self.activate("Modern cities")
        left_names = [
            "Niederlande",
            "Großbritannien",
            "Belgien",
            "Schweiz",
            "Deutsches Reich",
            "Vereinigte Staaten",
            "Italien",
            "Frankreich",
            "Spanien",
        ]
        result = self.page.evaluate(
            r"""leftNames => {
                const svg = document.querySelector("#cslope svg");
                const frame = svg.getBoundingClientRect();
                const texts = [...svg.querySelectorAll("text")];
                const left = texts.filter(node =>
                    leftNames.some(name => node.textContent.trim().startsWith(name + " ")));
                const right = texts.filter(node => /^[A-Z]{2} \d/.test(node.textContent.trim()));
                const outside = [...left, ...right].filter(node => {
                    const box = node.getBoundingClientRect();
                    return box.left < frame.left - 0.5 || box.right > frame.right + 0.5 ||
                           box.top < frame.top - 0.5 || box.bottom > frame.bottom + 0.5;
                }).map(node => node.textContent.trim());
                const overlaps = side => {
                    const rows = side.map(node => ({text: node.textContent.trim(), box: node.getBoundingClientRect()}));
                    const hits = [];
                    for (let i = 0; i < rows.length; i++) {
                        for (let j = i + 1; j < rows.length; j++) {
                            const a = rows[i].box, b = rows[j].box;
                            if (a.left < b.right - 0.5 && a.right > b.left + 0.5 &&
                                a.top < b.bottom - 0.5 && a.bottom > b.top + 0.5) {
                                hits.push([rows[i].text, rows[j].text]);
                            }
                        }
                    }
                    return hits;
                };
                return {
                    leftCount: left.length,
                    rightCount: right.length,
                    outside,
                    overlaps: [...overlaps(left), ...overlaps(right)],
                };
            }""",
            left_names,
        )
        self.assertEqual(9, result["leftCount"])
        self.assertEqual(9, result["rightCount"])
        self.assertEqual([], result["outside"])
        self.assertEqual([], result["overlaps"])

    def test_curve_annotations_stay_above_the_plotted_data(self):
        cases = (
            ("1913 cities", "#c1913 svg", ("MLE xi", "OLS xi", "rank-1/2 OLS")),
            ("Modern cities", "#cdeband svg", ("admin 57.4", "FUA 71.1")),
            ("Mountains", "#cmount svg", ("xi ", "lane: ")),
        )
        for tab, selector, prefixes in cases:
            with self.subTest(chart=selector):
                self.activate(tab)
                result = self.page.evaluate(
                    """({selector, prefixes}) => {
                        const svg = document.querySelector(selector);
                        const labels = [...svg.querySelectorAll("text")]
                            .filter(node => prefixes.some(prefix => node.textContent.trim().startsWith(prefix)));
                        const marks = [...svg.querySelectorAll("circle")];
                        return {
                            labelCount: labels.length,
                            legendBottom: Math.max(...labels.map(node => node.getBoundingClientRect().bottom)),
                            dataTop: Math.min(...marks.map(node => node.getBoundingClientRect().top)),
                        };
                    }""",
                    {"selector": selector, "prefixes": prefixes},
                )
                self.assertEqual(len(prefixes), result["labelCount"])
                self.assertLessEqual(result["legendBottom"] + 4, result["dataTop"])

    def test_every_mountain_arm_clips_curves_below_the_annotation_band(self):
        self.activate("Mountains")
        arm_values = self.page.locator("#armsel option").evaluate_all(
            "options => options.map(option => option.value)"
        )
        for viewport_width in (1180, 392):
            self.page.set_viewport_size({"width": viewport_width, "height": 900})
            for arm in arm_values:
                with self.subTest(viewport_width=viewport_width, arm=arm):
                    self.page.locator("#armsel").select_option(arm)
                    result = self.page.evaluate(
                        """() => {
                            const svg = document.querySelector("#cmount svg");
                            const labels = [...svg.querySelectorAll("text")]
                                .filter(node => ["xi ", "lane: "].some(
                                    prefix => node.textContent.trim().startsWith(prefix)));
                            const clipRect = svg.querySelector("clipPath rect");
                            const marks = svg.querySelector(".plot-marks");
                            if (!clipRect || !marks) return {hasClip: false};
                            const point = svg.createSVGPoint();
                            point.x = Number(clipRect.getAttribute("x"));
                            point.y = Number(clipRect.getAttribute("y"));
                            const clipTop = point.matrixTransform(clipRect.getScreenCTM()).y;
                            return {
                                hasClip: true,
                                clipPath: marks.getAttribute("clip-path"),
                                labelCount: labels.length,
                                legendBottom: Math.max(...labels.map(
                                    node => node.getBoundingClientRect().bottom)),
                                clipTop,
                                curveCount: marks.querySelectorAll("path").length,
                                pointCount: marks.querySelectorAll("circle").length,
                                thresholdCount: marks.querySelectorAll("line").length,
                            };
                        }"""
                    )
                    self.assertTrue(result["hasClip"])
                    self.assertEqual("url(#mountain-plot-clip)", result["clipPath"])
                    self.assertEqual(2, result["labelCount"])
                    self.assertLessEqual(result["legendBottom"] + 4, result["clipTop"])
                    self.assertEqual(2, result["curveCount"])
                    self.assertGreater(result["pointCount"], 0)
                    self.assertEqual(1, result["thresholdCount"])

    def test_every_chart_has_a_visible_heading_name_and_description(self):
        expected = {
            "1913 cities": ("#c1913", "#cak", "#cmc", "#ct2"),
            "Modern cities": ("#cslope", "#ctau", "#cde", "#cdeband"),
            "Mountains": ("#cmount", "#crail", "#creg"),
        }
        for tab, containers in expected.items():
            self.activate(tab)
            for container in containers:
                with self.subTest(tab=tab, chart=container):
                    result = self.page.locator(container + " svg").evaluate(
                        """svg => {
                            const labelledby = svg.getAttribute("aria-labelledby");
                            const describedby = svg.getAttribute("aria-describedby");
                            const label = labelledby && document.getElementById(labelledby);
                            const description = describedby && document.getElementById(describedby);
                            return {
                                role: svg.getAttribute("role"),
                                labelledby,
                                describedby,
                                labelText: label && label.textContent.trim(),
                                descriptionText: description && description.textContent.trim(),
                            };
                        }"""
                    )
                    self.assertEqual("img", result["role"])
                    self.assertTrue(result["labelledby"])
                    self.assertTrue(result["describedby"])
                    self.assertTrue(result["labelText"])
                    self.assertTrue(result["descriptionText"])

    def test_mobile_tabs_keep_overflow_local_to_accessible_table_regions(self):
        try:
            for width in (390, 392):
                self.page.set_viewport_size({"width": width, "height": 844})
                for tab in (
                    "Overview", "Full report", "Scoreboard", "1913 cities",
                    "Modern cities", "Mountains", "Data & custody",
                ):
                    with self.subTest(width=width, tab=tab):
                        self.activate(tab)
                        metrics = self.page.evaluate(
                            """() => ({
                                scrollWidth: document.documentElement.scrollWidth,
                                clientWidth: document.documentElement.clientWidth,
                            })"""
                        )
                        self.assertEqual(metrics["clientWidth"], metrics["scrollWidth"])

                self.activate("Mountains")
                table_region = self.page.locator("#tmodels").locator("xpath=..")
                self.assertEqual("region", table_region.get_attribute("role"))
                self.assertEqual("0", table_region.get_attribute("tabindex"))
                self.assertIn("scroll horizontally", table_region.get_attribute("aria-label"))
                scroll = table_region.evaluate(
                    "el => ({clientWidth: el.clientWidth, scrollWidth: el.scrollWidth})"
                )
                self.assertGreater(scroll["scrollWidth"], scroll["clientWidth"])
                table_region.evaluate("el => { el.scrollLeft = el.scrollWidth; }")
                self.assertGreater(table_region.evaluate("el => el.scrollLeft"), 0)
        finally:
            self.page.set_viewport_size({"width": 1180, "height": 900})

    def test_report_contents_jump_transfers_focus_and_keeps_tab_order_local(self):
        self.activate("Full report")
        link = self.page.get_by_role("link", name="3. The defensible claim", exact=True)
        target_id = link.get_attribute("href").removeprefix("#")
        link.click()
        self.page.wait_for_timeout(100)
        focused = self.page.evaluate("document.activeElement.id")
        self.assertEqual(target_id, focused)
        self.assertEqual("#rp-s4", self.page.evaluate("location.hash"))
        self.assertEqual("-1", self.page.locator("#" + target_id).get_attribute("tabindex"))
        self.page.keyboard.press("Tab")
        follows = self.page.evaluate(
            """targetId => {
                const target = document.getElementById(targetId);
                const active = document.activeElement;
                return active !== document.body && active !== target &&
                    Boolean(target.compareDocumentPosition(active) & Node.DOCUMENT_POSITION_FOLLOWING);
            }""",
            target_id,
        )
        self.assertTrue(follows)


if __name__ == "__main__":
    unittest.main()
