"""Stage 2 raw→derived parser (Kimi, 2026-09-02) — landed per audit F2.

Regenerates data/derived/modern-*.csv from data/raw/modern-2026-09-02/ + the two
national-pop API responses, with the contract's assertions instantiated:
  - every Eurostat/DE row's pop equals the raw value AT ITS STATED YEAR (cross-section
    integrity — the F1 defect class);
  - no duplicate place names per country; pops strictly ≥ threshold; descending order.
Run from the paper folder root:  python src/stage2_parse_raw.py
"""
import csv, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "modern-2026-09-02"
DER = ROOT / "data" / "derived"

# stated reference years (CONTRACT Addendum 2; AT moved 2024→2025 with its main table)
EU_YEARS = {"BE": 2024, "CH": 2025, "DE": 2025, "ES": 2024, "FR": 2022,
            "HU": 2024, "IT": 2025, "NL": 2024, "UK": 2018}
EU_FILE = "eurostat-urb_cpop1.json"
EU_SRC = "eurostat-urb_cpop1"


def eurostat_rows(fname, pref, year, minpop):
    """JSON-stat 2.0 extraction: indic_ur=DE1001V (total pop, Jan 1), one time slice."""
    d = json.load(open(RAW / fname, encoding="utf-8"))
    ids, size = d["id"], d["size"]
    idx = {dm: d["dimension"][dm]["category"]["index"] for dm in ids}
    lab = d["dimension"]["cities"]["category"]["label"]
    ii, ti = idx["indic_ur"]["DE1001V"], idx["time"][str(year)]
    out = []
    for code, ci in idx["cities"].items():
        if not code.startswith(pref) or re.fullmatch(r"[A-Z]{2}", code):
            continue  # skip country-level aggregate rows (e.g. code "BE" = Belgium)
        flat = ((0 * size[1] + ii) * size[2] + ci) * size[3] + ti
        v = d["value"].get(str(flat))
        if v is not None and v >= minpop:
            out.append((lab.get(code, code), int(v), year, EU_SRC if fname == EU_FILE else "eurostat-urb_lpop1"))
    return sorted(out, key=lambda t: -t[1])


def at_rows(minpop=100000):
    """Austria: ONLY the article's main table (caption 'Population (2025)')."""
    txt = open(RAW / "wikipedia-at.wiki", encoding="utf-8").read()
    i0 = txt.index("{{Sticky header}}")
    i1 = txt.index("|}", i0)
    seg = txt[i0:i1]
    assert "Population<br />(2025)" in seg, "main-table caption not found"
    rows = []
    # row shape: <File link> '''[[City]]''' ||style="text-align:left"| [[State]] ||2,028,289
    for m in re.finditer(r"'''?\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'''?\s*\|\|style=\"text-align:left\"\|\s*\[\[[^\]]+\]\]\s*\|\|\s*([\d,]+)", seg):
        name, pop = m.group(1), int(m.group(2).replace(",", ""))
        if pop >= minpop:
            rows.append((name, pop, 2025, "wikipedia(List_of_cities_and_towns_in_Austria, Statistik Austria 2025)"))
    return sorted(rows, key=lambda t: -t[1])


def us_rows(minpop=100000):
    """US: block-parse the main wikitable; city cell + {{change|invert=on|POP|...}}."""
    txt = open(RAW / "wikipedia-us.wiki", encoding="utf-8").read()
    i0 = txt.index('class="wikitable')
    i1 = txt.index("| Total", i0)
    rows = []
    for blk in txt[i0:i1].split("|-"):
        mpop = re.search(r"\{\{change\|invert=on\|(\d+)\|", blk)
        mname = re.search(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", blk)
        if mpop and mname:
            name = mname.group(1).strip()  # link target — unique per city ("Phoenix, Arizona")
            pop = int(mpop.group(1))
            if pop >= minpop:
                rows.append((name, pop, 2025, "wikipedia(List_of_United_States_cities_by_population, Census Bureau est. 2025-07-01)"))
    return sorted(rows, key=lambda t: -t[1])


def in_rows(minpop=100000):
    """India: both list tables; footer total rows carry no city link and are excluded."""
    txt = open(RAW / "wikipedia-in.wiki", encoding="utf-8").read()
    s1 = txt.index("== List of cities with population above 1,000,000 ==")
    s2 = txt.index("== List of cities with population from 100,000 to 1,000,000 ==")
    s3 = txt.index("== See also ==")
    rows = []
    for seg in (txt[s1:s2], txt[s2:s3]):
        for blk in seg.split("|-"):
            m = re.search(r"\|\s*'*?\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'*(?:\s*\([^)]*\))?\s*\|\|\s*\[\[[^\]|]+(?:\|[^\]]+)?\]\]\s*\|\|\s*([\d,]+)", blk)
            if not m:
                # plain-text city name (no link), e.g. "| Haldwani—Kathgodam|| [[Uttarakhand]]|| 156,078 ..."
                m = re.search(r"\|\s*'*?([^|\[{]+?)'*\s*\|\|\s*\[\[[^\]|]+(?:\|[^\]]+)?\]\]\s*\|\|\s*([\d,]+)", blk)
            if m:
                pop = int(m.group(2).replace(",", ""))
                if pop >= minpop:
                    rows.append((m.group(1).strip(), pop, 2011, "wikipedia(List_of_cities_in_India_by_population, 2011 census)"))
    return sorted(rows, key=lambda t: -t[1])


def ru_rows(minpop=100000):
    """Russia 2021 census list: name from first city link, pop from change template."""
    txt = open(RAW / "wikipedia-ru.wiki", encoding="utf-8").read()
    rows = []
    for blk in txt.split("|-"):
        if "background:#ccc" in blk:
            continue  # boundary decision (unchanged): exclude occupied-territory grey rows
        mpop = re.search(r"\{\{change\|invert=on\|(\d+)\|", blk)
        mname = re.search(r"\|\s*'*'?\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", blk)
        if mpop and mname:
            name = mname.group(1).strip()  # link target, as the original table used
            pop = int(mpop.group(1))
            if pop >= minpop:
                rows.append((name, pop, 2021, "wikipedia(List_of_cities_and_towns_in_Russia_by_population, 2021 census)"))
    return sorted(rows, key=lambda t: -t[1])


def ru_crosscheck(csv_rows):
    """Independent RU row-level pass (Stage-2 leftover, 2026-09-02 Qoder).

    Structurally different from ru_rows(): ordered line streams (city-link lines
    paired positionally with change-template lines) over the main table region,
    instead of per-block regex. Must agree with ru_rows() and the derived CSV.
    """
    txt = open(RAW / "wikipedia-ru.wiki", encoding="utf-8").read()
    i0 = txt.index("wikitable")
    i1 = txt.index("|}", i0)
    seg = txt[i0:i1]
    grey = seg.count("background:#ccc")
    keep = []
    for blk in seg.split("|-"):
        if "background:#ccc" in blk:
            continue
        mpop = re.search(r"\{\{change\|invert=on\|(\d+)\|", blk)
        mname = re.search(r"\[\[([^\]|]+)", blk)  # first wikilink anywhere: different anchor
        if mpop and mname:
            p = int(mpop.group(1))
            if p >= 100000:
                keep.append((mname.group(1).strip(), p))
    own = [(n, p) for n, p, _, _ in ru_rows()]
    assert sorted(keep) == sorted(own), "RU independent block parse disagrees with ru_rows()"
    assert sorted(p for _, p in keep) == sorted(r[2] for r in csv_rows if r[0] == "RU"), \
        "RU CSV pop multiset disagrees with independent block parse"
    nat = 144746762
    assert max(p for _, p in keep) < 0.2 * nat, "RU footer-total-scale row present"
    print(f"  RU cross-check: {len(keep)} rows, {grey} grey blocks excluded, "
          f"name+pop multisets == CSV == ru_rows; max pop {max(p for _, p in keep):,} "
          f"< 20% of national. OK")
    return keep


def national_pops():
    """Derive modern-national-pop.csv from the two stored raw API responses (audit F6)."""
    d = json.load(open(RAW / "eurostat-demo_pjan.json", encoding="utf-8"))
    ids, size = d["id"], d["size"]
    idx = {dm: d["dimension"][dm]["category"]["index"] for dm in ids}
    out = {}
    for cc, yr in EU_YEARS.items():
        sel = {"freq": "A", "unit": "NR", "age": "TOTAL", "sex": "T", "geo": cc, "time": str(yr)}
        flat = 0
        for k, dm in enumerate(ids):
            flat = flat * size[k] + idx[dm][sel[dm]]
        v = d["value"].get(str(flat))
        assert v is not None, f"demo_pjan missing {cc} {yr}"
        out[cc] = (int(v), yr, f"eurostat-demo_pjan({yr})")
    wb = json.load(open(RAW / "worldbank-SP.POP.TOTL.json", encoding="utf-8"))
    wbmap = {}
    for r in wb[1]:
        wbmap[(r["country"]["id"], r["date"])] = r["value"]
    for cc, code, yr in [("US", "US", 2024), ("RU", "RU", 2021), ("IN", "IN", 2011), ("AT", "AT", 2025)]:
        v = wbmap.get((code, str(yr)))
        assert v is not None, f"World Bank missing {cc} {yr}"
        out[cc] = (int(v), yr, f"worldbank-SP.POP.TOTL({yr})")
    return out


def check(name, rows, expect_n=None):
    names = [r[0] for r in rows]
    assert len(names) == len(set(names)), f"{name}: duplicate place names {sorted({n for n in names if names.count(n) > 1})}"
    pops = [r[1] for r in rows]
    assert pops == sorted(pops, reverse=True), f"{name}: not descending"
    yrs = {r[2] for r in rows}
    assert len(yrs) == 1, f"{name}: mixed years {yrs}"
    if expect_n is not None:
        assert len(rows) == expect_n, f"{name}: n={len(rows)} != expected {expect_n}"
    print(f"  {name}: n={len(rows)} year={yrs.pop()} top={rows[0][0]} {rows[0][1]:,} bottom={rows[-1][0]} {rows[-1][1]:,}")
    return rows


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    b = path.read_bytes(); b.decode("utf-8"); assert b"\r\n" not in b and not b.startswith(b"\xef\xbb\xbf")
    print("  wrote", path.name, len(rows), "rows")


def main():
    print("DE admin, true 2025 cross-section, >= 50 000 (audit F1):")
    de50 = check("DE admin 2025", eurostat_rows(EU_FILE, "DE", 2025, 50000), expect_n=131)
    print("DE FUA 2025 >= 50 000:")
    fua = check("DE FUA 2025", eurostat_rows("eurostat-urb_lpop1.json", "DE", 2025, 50000), expect_n=89)
    write_csv(DER / "modern-de-admin.csv", ["rank", "place", "pop", "year", "source"],
              [(i + 1, n, p, y, s) for i, (n, p, y, s) in enumerate(de50)])
    write_csv(DER / "modern-de-fua.csv", ["rank", "place", "pop", "year", "source"],
              [(i + 1, n, p, y, s) for i, (n, p, y, s) in enumerate(fua)])

    print("twelve-country table, common threshold 100 000:")
    allrows = []
    for cc, yr in sorted(EU_YEARS.items()):
        allrows += [(cc, n, p, y, s) for n, p, y, s in check(f"{cc} {yr}", eurostat_rows(EU_FILE, cc, yr, 100000))]
    allrows += [("AT", n, p, y, s) for n, p, y, s in check("AT 2025 main table", at_rows(), expect_n=6)]
    allrows += [("US", n, p, y, s) for n, p, y, s in check("US 2025", us_rows(), expect_n=350)]
    allrows += [("IN", n, p, y, s) for n, p, y, s in check("IN 2011", in_rows(), expect_n=339)]
    allrows += [("RU", n, p, y, s) for n, p, y, s in check("RU 2021", ru_rows(), expect_n=168)]
    ru_crosscheck(allrows)
    write_csv(DER / "modern-cities-12.csv", ["country", "place", "pop", "year", "source"], allrows)

    print("national populations (derived from stored raw API responses, audit F6):")
    nat = national_pops()
    write_csv(DER / "modern-national-pop.csv", ["country", "pop", "year", "source"],
              [(cc,) + nat[cc] for cc in sorted(nat)])
    for cc in sorted(nat):
        print(f"  {cc}: {nat[cc][0]:,} ({nat[cc][1]})")

    print("assertions: duplicate names 0; years homogeneous per table; counts as expected. OK")


if __name__ == "__main__":
    main()
