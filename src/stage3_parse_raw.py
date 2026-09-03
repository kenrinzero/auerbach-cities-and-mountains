#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stage 3 raw -> derived parser (mountains). Contract rule 2: every derived table is
regenerated here from data/raw/mountains-2026-09-02/ with the plan's assertions A1-A7
instantiated (results/stage3-plan.md section 3). No hand-produced CSVs.

Run from the paper-folder root:  python src/stage3_parse_raw.py
"""
import sys, re, json, csv, io, math, pathlib, hashlib, itertools, collections

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "mountains-2026-09-02"
DER = ROOT / "data" / "derived"

ULTRA_CUTOFF = 1500.0
EARTH_MAX = 8848.86          # prereg F2 physical bound; assertion A1 ceiling 8850
A1_ELEV_CEIL = 8850.0

# A0 sampling frame: article slug -> (index-stated count, role)
A0_ARTICLES = [
    ("list-of-ultras-of-africa", 84),
    ("list-of-ultras-of-antarctica", 41),
    ("list-of-ultras-of-central-asia", 75),
    ("list-of-ultra-prominent-peaks-of-japan", 21),
    ("list-of-ultras-of-northeast-asia", 51),
    ("list-of-ultras-of-southeast-asia", 42),
    ("list-of-ultras-of-the-himalayas", 76),
    ("list-of-ultras-of-the-karakoram-and-hindu-kush", 61),
    ("list-of-ultras-of-the-malay-archipelago", 91),
    ("list-of-ultras-of-the-philippines", 29),
    ("list-of-ultras-of-tibet-east-asia-and-neighbouring-areas", 112),
    ("list-of-ultras-of-west-asia", 88),
    ("list-of-european-ultra-prominent-peaks", 120),
    ("list-of-ultras-of-north-america", 356),
    ("list-of-ultras-of-oceania", 69),
    ("list-of-ultras-of-south-america", 211),
]
WORLD_TOTAL_STATED = 1516
UNION_TOLERANCE = (1490, 1540)          # assertion A4

REPORT = []
REPAIRS = []
def say(msg=""):
    REPORT.append(str(msg))
    print(msg)


# ---------------------------------------------------------------- wikitext plumbing
def split_tables(w):
    """Stack-based {| ... |} scanner (handles nesting); returns [(section_heading, body)]."""
    out, depth, buf, section = [], 0, [], ""
    for line in w.split("\n"):
        s = line.strip()
        hm = re.match(r"^(={2,6})\s*(.+?)\s*\1$", s)
        if hm and depth == 0:
            section = re.sub(r"\[\[([^\]|]*\|)?|\]\]|<[^>]+>", "", hm.group(2)).strip()
            continue
        if s.startswith("{|"):
            if depth == 0:
                buf = [line]
            else:
                buf.append(line)
            depth += 1
        elif s.startswith("|}") and depth > 0:
            depth -= 1
            buf.append(line)
            if depth == 0:
                out.append((section, "\n".join(buf)))
        elif depth > 0:
            buf.append(line)
    return out


def tpl_args(cell, name):
    """Positional + keyword args of {{name|...}} with bracket-depth-aware splitting."""
    m = re.search(r"\{\{\s*" + re.escape(name) + r"\s*(\|.*?)?\}\}", cell, re.S)
    if not m:
        return None
    body = m.group(1) or ""
    if body.startswith("|"):
        body = body[1:]
    args, depth, cur = [], 0, ""
    for ch in body:
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "|" and depth <= 0:
            args.append(cur)
            cur = ""
        else:
            cur += ch
    args.append(cur)
    return args


def positional(args):
    return [a.strip() for a in (args or []) if a.strip() and "=" not in a.split("|")[0][:24]]


def strip_refs(c):
    return re.sub(r"<ref[^>]*/>|<ref.*?</ref>", "", c, flags=re.S)


def clean_cell(c):
    """Drop a leading HTML-ish attribute prefix (align=right|4,810) repeatedly."""
    c = c.strip()
    while "|" in c:
        head, rest = c.split("|", 1)
        if re.match(r'^\s*[a-zA-Z-]+\s*=\s*"[^"]*"\s*$', head) or \
           re.match(r"^\s*[a-zA-Z-]+\s*=\s*[^{}|\[\]]*\s*$", head):
            c = rest.strip()
        else:
            break
    return c


def num(c):
    """First plain number in a cell, after stripping refs/templates/commas/bold."""
    if c is None:
        return None
    c = strip_refs(c)
    c = re.sub(r"\{\{efn[^}]*\}\}", "", c)
    c = re.sub(r"\{\{note[^}]*\}\}", "", c, flags=re.I)
    c = c.replace("'''", "").replace("''", "").replace(",", "").replace("&nbsp;", " ")
    m = re.search(r"-?\d+(?:\.\d+)?", c)
    return float(m.group(0)) if m else None


def link_target(c):
    """(target, display) of the first wikilink; falls back to template/plain text."""
    c = strip_refs(c)
    m = re.search(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]", c)
    if m:
        return m.group(1).strip(), (m.group(2) or m.group(1)).strip()
    args = tpl_args(c, "Mountain table cell")
    if args:
        pos = positional(args)
        if pos:
            return None, pos[0]
    for tpl in ("cmtr", "flag", "flagicon"):
        a = tpl_args(c, tpl)
        if a:
            pos = positional(a)
            if pos:
                return None, pos[0]
    txt = re.sub(r"\{\{[^{}]*\}\}", "", c)
    txt = re.sub(r"<[^>]+>", "", txt).strip()
    return None, txt


def row_cells(rowlines):
    """Cells of one row, expanding {{Mountain table cell}} (1 cell) and {{epi}} (3 cells)."""
    cells, pending = [], None
    for ln in rowlines:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("{{epi|") or s.startswith("{{epi |"):
            args = tpl_args(s, "epi")
            pos = positional(args)
            cells.extend(pos[:3] if len(pos) >= 3 else pos + [""] * (3 - len(pos)))
            continue
        if s.startswith("{{Mountain table cell"):
            args = tpl_args(s, "Mountain table cell")
            pos = positional(args)
            cells.append(pos[0] if pos else "")
            continue
        if s.startswith("|"):
            body = s[1:]
            for piece in body.split("||"):
                cells.append(clean_cell(piece))
            continue
        if s.startswith("!"):
            continue
        if cells:
            cells[-1] = cells[-1] + " " + s        # continuation of the previous cell
        else:
            cells.append(s)
    return cells


def header_cells(hdrlines):
    txt = "\n".join(hdrlines)
    parts = re.split(r"\n!|!!|^!", txt)
    out = []
    for p in parts:
        p = p.strip()
        if p:
            out.append(clean_cell(p))
    return out


def colmap(hdr):
    m = {}
    def put(key, i):
        m.setdefault(key, i)
    for i, h in enumerate(hdr):
        hl = re.sub(r"\{\{abbr\|([^|}]*)\|([^}]*)\}\}", r"\1 \2", h, flags=re.I)
        hl = re.sub(r"\[\[([^\]|]*\|)?|\]\]|<[^>]+>|\{\{[^}]*\}\}", "", hl).lower()
        hl = hl.replace("<br />", " ").strip()
        if "rank" in hl or hl.strip().startswith("no"):
            put("rank", i)
        elif "prominence" in hl:
            put("prom", i)
        elif "elevation" in hl or "height" in hl:
            put("elev", i)
        elif "range" in hl:
            put("range", i)
        elif "col" in hl:
            put("col", i)
        elif "peak" in hl or "summit" in hl or "mountain name" in hl:
            put("name", i)
        elif "coordinate" in hl:
            put("coord", i)
        elif "country" in hl or "region" in hl or "location" in hl or "island" in hl \
                or "landmass" in hl:
            put("region", i)
    return m


def parse_tables(slug):
    """All tables of one raw article -> list of dicts with caption + parsed rows."""
    p = RAW / (slug + ".wiki")
    w = p.read_text(encoding="utf-8")
    tabs = split_tables(w)
    assert w.count("{|") == w.count("|}"), "%s: unbalanced table braces" % slug
    out = []
    for section, t in tabs:
        lines = t.split("\n")
        attrs = lines[0]
        cap = ""
        cm = re.search(r"\|\+(.*?)\n", t, re.S)
        if cm:
            cap = re.sub(r"<[^>]+>|\{\{[^}]*\}\}|\[\[([^\]|]*\|)?|\]\]|'''", "", cm.group(1))
            cap = cap.replace("&nbsp;", " ").strip()
        hdrlines, rows, cur, inhead = [], [], [], True
        for ln in lines[1:]:
            s = ln.strip()
            if s.startswith("|}"):
                break
            if s.startswith("|+"):
                continue
            if s.startswith("|-"):
                if inhead:
                    inhead = False
                elif cur:
                    rows.append(cur)
                cur = []
                continue
            if inhead:
                hdrlines.append(ln)
            else:
                cur.append(ln)
        if cur:
            rows.append(cur)
        hdr = header_cells(hdrlines)
        cm2 = colmap(hdr)
        allcells = [row_cells(r) for r in rows]
        counts = collections.Counter(len(c) for c in allcells if c)
        modal = counts.most_common(1)[0][0] if counts else 0
        repair = ""
        if modal and modal == len(hdr) - 1 and "region" in cm2 and "range" in cm2 \
                and cm2["range"] == cm2["region"] + 1:
            repair = ("rows carry %d cells for %d header columns: region+range are emitted "
                      "in one cell, so columns after index %d shift left by one"
                      % (modal, len(hdr), cm2["range"]))
            cm2 = {k: (cm2["region"] if k == "range" else (i - 1 if i > cm2["range"] else i))
                   for k, i in cm2.items()}
        parsed = []
        for cells in allcells:
            rec = {"_cells": cells, "_hdr": hdr}
            for key, idx in cm2.items():
                rec[key] = cells[idx] if idx < len(cells) else None
            parsed.append(rec)
        out.append(dict(attrs=attrs, caption=cap, section=section, hdr=hdr, colmap=cm2,
                        repair=repair, rows=parsed, nrows=len(parsed)))
    return out


# ---------------------------------------------------------------- value extraction
def rec_numbers(rec):
    elev = num(rec.get("elev"))
    prom = num(rec.get("prom"))
    return elev, prom


def rec_name(rec):
    tgt, disp = link_target(rec.get("name") or "")
    return tgt, disp


def rec_coords(rec):
    """(lat, lon, qid) from the mapped coordinate cell, else from any cell of the row."""
    cands = []
    if rec.get("coord"):
        cands.append(rec["coord"])
    cands.extend(rec.get("_cells") or [])
    qid = None
    for c in cands:
        if not c:
            continue
        args = tpl_args(c, "coord") or tpl_args(c, "coord-")
        if args:
            pos = positional(args)
            if len(pos) >= 2:
                try:
                    return float(pos[0]), float(pos[1]), qid
                except ValueError:
                    pass
            for a in args:
                if a.strip().startswith("qid="):
                    qid = qid or a.split("=", 1)[1].strip()
        m = re.search(r"qid\s*=\s*(Q\d+)", c)
        if m:
            qid = qid or m.group(1)
        m = re.search(r"(\d+(?:\.\d+)?)\s*°?\s*([NS])\s*(?:<br\s*/?>)?\s*(\d+(?:\.\d+)?)\s*°?\s*([EW])", c)
        if m:
            lat = float(m.group(1)) * (1 if m.group(2) == "N" else -1)
            lon = float(m.group(3)) * (1 if m.group(4) == "E" else -1)
            return lat, lon, qid
    return None, None, qid


def normkey(disp):
    d = disp.lower()
    d = re.sub(r"\s*\(.*?\)\s*", " ", d)
    d = re.sub(r"[^a-z0-9]+", "", d)
    return d


def keep_row(rec, cutoff=ULTRA_CUTOFF):
    elev, prom = rec_numbers(rec)
    if elev is None or prom is None:
        return None, "missing elev/prom"
    if prom < cutoff:
        return None, "prominence below cutoff"
    if prom > elev + 0.5:                       # A1: prominence <= elevation
        return None, "A1 violation prom>elev"
    if not (0 < elev <= A1_ELEV_CEIL):           # A1: impossible elevation
        return None, "A1 violation elevation out of range"
    return dict(elev=elev, prom=prom), None


def build_rows(slug, tables=None, cutoff=ULTRA_CUTOFF, caption_filter=None):
    """Parse one article, apply the membership rule, return (rows, reject_counter, unparsed)."""
    tabs = tables if tables is not None else parse_tables(slug)
    rows, rejects, unparsed = [], collections.Counter(), []
    for t in tabs:
        if caption_filter and not caption_filter(t["caption"]):
            continue
        if "prom" not in t["colmap"] or "elev" not in t["colmap"] or "name" not in t["colmap"]:
            rejects["table without elev+prom+name header"] += 1
            continue
        for rec in t["rows"]:
            got, why = keep_row(rec, cutoff)
            if got is None:
                rejects[why] += 1
                if why == "missing elev/prom":
                    _, disp = link_target(rec.get("name") or "")
                    raw = [str(c)[:28] for c in rec.get("_cells", [])[:3]]
                    unparsed.append("%s [elev=%r prom=%r] cells=%s"
                                    % (disp or "(no name)", rec.get("elev"), rec.get("prom"), raw))
                continue
            tgt, disp = rec_name(rec)
            lat, lon, qid = rec_coords(rec)
            rng = link_target(rec["range"])[1] if rec.get("range") else None
            region = link_target(rec["region"])[1] if rec.get("region") else None
            if t.get("repair"):
                REPAIRS.append("%s | %s | %s" % (slug, (t["section"] or t["caption"])[:34], t["repair"]))
            colv = num(rec.get("col")) if rec.get("col") is not None else None
            rows.append(dict(name=disp, link_target=tgt, key=(tgt or normkey(disp)),
                             region=region, rng=rng, elev=got["elev"], prom=got["prom"],
                             col=colv, lat=lat, lon=lon, qid=qid, source=slug,
                             caption=t["caption"][:60]))
    return rows, rejects, unparsed


def dedupe(rows, sources_label):
    """A3(i): de-duplicate on resolved link target (else normalized name).
    Merge rule: keep the largest prominence; record every source article."""
    best = {}
    for r in rows:
        k = r["key"] or normkey(r["name"])
        cur = best.get(k)
        if cur is None:
            r = dict(r)
            r["sources"] = [r["source"]]
            best[k] = r
        else:
            if r["source"] not in cur["sources"]:
                cur["sources"].append(r["source"])
            if r["prom"] > cur["prom"]:
                for f in ("elev", "prom", "col", "name", "link_target", "lat", "lon", "qid",
                          "region", "rng"):
                    if r.get(f) is not None:
                        cur[f] = r[f]
    out = list(best.values())
    for r in out:
        r["sources"] = ";".join(sorted(set(r["sources"])))
    say("   [%s] parsed rows %d -> distinct summits %d (merged %d)"
        % (sources_label, len(rows), len(out), len(rows) - len(out)))
    return out


def fill_qid_coords(rows, wd):
    """Coordinate donor: join rows carrying a Wikidata qid to the CC0 SPARQL snapshot."""
    joined = 0
    for r in rows:
        if r.get("lat") is None and r.get("qid") and r["qid"] in wd:
            lat, lon = wd[r["qid"]]
            if lat is not None:
                r["lat"], r["lon"], joined = lat, lon, joined + 1
    say("   coordinates filled from the Wikidata snapshot by qid: %d rows" % joined)


def write_csv(path, rows, cols):
    buf = io.StringIO()
    wcsv = csv.writer(buf, lineterminator="\n")
    wcsv.writerow(cols)
    for r in rows:
        wcsv.writerow([("" if r.get(c) is None else r.get(c)) for c in cols])
    data = buf.getvalue().encode("utf-8")
    assert b"\r\n" not in data, "CRLF in %s" % path.name
    assert not data.startswith(b"\xef\xbb\xbf"), "BOM in %s" % path.name
    path.write_bytes(data)
    data.decode("utf-8")
    say("   wrote %s  (%d rows, %d bytes, sha256 %s)"
        % (path.name, len(rows), len(data), hashlib.sha256(data).hexdigest()[:16]))


# ---------------------------------------------------------------- Wikidata snapshot
def load_wikidata():
    d = json.loads((RAW / "wikidata-p2660-ge1500.json").read_text(encoding="utf-8"))
    b = d["results"]["bindings"]
    g = collections.defaultdict(list)
    for r in b:
        g[r["i"]["value"].rsplit("/", 1)[-1]].append(r)
    coord = {}
    recs = []
    viol = collections.Counter()
    for q, rs in g.items():
        def pick(field, agg=max):
            vals = []
            for r in rs:
                if field in r:
                    try:
                        vals.append(float(r[field]["value"]))
                    except ValueError:
                        pass
            return agg(vals) if vals else None
        prom = pick("prom")
        elev = pick("elev")
        cs = sorted({r["coord"]["value"] for r in rs if "coord" in r})
        lab = sorted({r["label"]["value"] for r in rs if "label" in r})
        lat = lon = None
        if cs:
            m = re.match(r"Point\(([-\d.]+) ([-\d.]+)\)", cs[0])
            if m:
                lat, lon = float(m.group(2)), float(m.group(1))
        coord[q] = (lat, lon)
        viol["rows"] += len(rs)
        viol["qids"] += 1
        if elev is None:
            viol["no elevation"] += 1
        else:
            if elev > A1_ELEV_CEIL:
                viol["A1 elevation impossible"] += 1
            if prom is not None and prom > elev + 0.5:
                viol["A1 prom>elev"] += 1
        recs.append(dict(qid=q, name=lab[0] if lab else "", key=normkey(lab[0]) if lab else "",
                         elev=elev, prom=prom, lat=lat, lon=lon,
                         link_target="", region="", rng="", col=None, qid2=q,
                         source="wikidata", sources="wikidata-sparql"))
    return recs, coord, viol, len(b)


def haversine_km(a, b):
    (lat1, lon1), (lat2, lon2) = a, b
    dx = (lat1 - lat2) * 111.32
    dy = (lon1 - lon2) * 111.32 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dx, dy)


def coord_duplicate_pairs(rows, label):
    """A3(ii): report every pair of retained summits within 1 km; never auto-merge."""
    have = [r for r in rows if r.get("lat") is not None and r.get("lon") is not None]
    buckets = collections.defaultdict(list)
    for i, r in enumerate(have):
        buckets[(round(r["lat"], 1), round(r["lon"], 1))].append(i)
    pairs = []
    for _, idxs in buckets.items():
        for i, j in itertools.combinations(idxs, 2):
            d = haversine_km((have[i]["lat"], have[i]["lon"]), (have[j]["lat"], have[j]["lon"]))
            if d <= 1.0:
                pairs.append((have[i]["name"], have[j]["name"], round(d, 3),
                              have[i]["elev"], have[j]["elev"]))
    say("   [%s] coordinate-bearing rows %d/%d; pairs within 1 km: %d"
        % (label, len(have), len(rows), len(pairs)))
    for p in pairs[:15]:
        say("      %-28s | %-28s %6.3f km  elev %.0f/%.0f" % (p[0][:28], p[1][:28], p[2], p[3], p[4]))
    return pairs, len(have)


# ---------------------------------------------------------------- main
def main():
    say("=" * 78)
    say("Stage 3 raw -> derived (contract rule 2). Raw: %s" % RAW.name)
    man = json.loads((RAW / "_manifest.json").read_text(encoding="utf-8"))
    for f in man["files"]:
        h = hashlib.sha256((RAW / f["file"]).read_bytes()).hexdigest()
        assert h == f["sha256"], "raw hash mismatch: %s" % f["file"]
    say("   raw custody verified: %d/%d files match _manifest.json sha256" % (len(man["files"]), len(man["files"])))
    say("   retrieved %s | licence %s" % (man["retrieved_utc"], man["licence"]))
    say("   recon notes: %s" % man["recon_notes"])

    wd_recs, wd_coord, wd_viol, wd_rows = load_wikidata()
    say("")
    say("[X1 Wikidata cross-check] raw rows %d, distinct qids %d" % (wd_rows, wd_viol["qids"]))
    for k in ("no elevation", "A1 elevation impossible", "A1 prom>elev"):
        say("   %-26s %d" % (k, wd_viol[k]))

    # ---- A0 global ultra set
    say("")
    say("[A0] global ultra set: union of %d Wikipedia lists, membership prominence >= %.0f m"
        % (len(A0_ARTICLES), ULTRA_CUTOFF))
    allrows, percounts = [], []
    for slug, stated in A0_ARTICLES:
        if slug == "list-of-ultras-of-north-america":
            tabs = parse_tables(slug)
            master = [t for t in tabs if re.search(r"ultra-prominent.*greater North", t["caption"], re.I)]
            assert len(master) == 1, "NA master table not uniquely identified (%d)" % len(master)
            rows, rej, unp = build_rows(slug, tables=master)
            say("   %-52s master-table rows %d, kept %d (caption 353, index %d)"
                % (slug[:52], master[0]["nrows"], len(rows), stated))
            assert 340 <= len(rows) <= 370, "NA master parse out of range: %d" % len(rows)
        else:
            rows, rej, unp = build_rows(slug)
            distinct = len({(r["key"] or normkey(r["name"])) for r in rows})
            say("   %-52s kept %4d distinct %4d (index %d, delta %+d) rejected: %s"
                % (slug[:52], len(rows), distinct, stated, distinct - stated, dict(rej)))
        for u in unp:
            say("      A6 dropped (unparsable elev/prom): %s" % u)
        percounts.append((slug, len(rows), stated))
        allrows.extend(rows)
    union = dedupe(allrows, "A0")
    lo, hi = UNION_TOLERANCE
    assert lo <= len(union) <= hi, "A4 union %d outside [%d,%d]" % (len(union), lo, hi)
    say("   A4 union %d vs index-stated world total %d (delta %+d, tolerance [%d,%d])"
        % (len(union), WORLD_TOTAL_STATED, len(union) - WORLD_TOTAL_STATED, lo, hi))

    # A2 Everest
    ev = [r for r in union if "everest" in normkey(r["name"])]
    assert ev, "A2 Everest absent from A0"
    say("   A2 Everest present: %s elev %.2f prom %.2f (sources %s)"
        % (ev[0]["name"], ev[0]["elev"], ev[0]["prom"], ev[0]["sources"]))
    assert abs(ev[0]["elev"] - EARTH_MAX) <= 1.0, "A2 Everest elevation %.2f" % ev[0]["elev"]

    # coordinate donor join (top-125 list carries qids) + coordinate duplicate check
    coord_tabs = parse_tables("list-of-mountain-peaks-by-prominence")
    coord_rows, coord_rej, _unp = build_rows("list-of-mountain-peaks-by-prominence", tables=coord_tabs)
    say("")
    say("[coord donor] list-of-mountain-peaks-by-prominence kept %d rows (stated 125)" % len(coord_rows))
    fill_qid_coords(coord_rows, wd_coord)
    bykey = {(r["key"] or normkey(r["name"])): r for r in coord_rows}
    joined = 0
    for r in union:
        k = r["key"] or normkey(r["name"])
        if r.get("lat") is None and k in bykey and bykey[k].get("lat") is not None:
            r["lat"], r["lon"] = bykey[k]["lat"], bykey[k]["lon"]
            joined += 1
        if r.get("rng") is None and k in bykey and bykey[k].get("rng"):
            r["rng"] = bykey[k]["rng"]
    say("   A0 rows receiving coordinates via the donor join: %d of %d (deviation D2)"
        % (joined, len(union)))
    pairsA0, ncoordA0 = coord_duplicate_pairs(union, "A0")
    pairsWD, ncoordWD = coord_duplicate_pairs(wd_recs, "X1 Wikidata")

    # ---- R1 Alps
    say("")
    say("[R1] Alps — list-of-alpine-peaks-by-prominence, membership prominence >= 1500 m")
    alps, rej, unp = build_rows("list-of-alpine-peaks-by-prominence")
    for u in unp:
        say("      A6 dropped (unparsable elev/prom): %s" % u)
    alps = dedupe(alps, "R1")
    say("   rejects: %s ; index states 44" % dict(rej))
    eur_tabs = parse_tables("list-of-european-ultra-prominent-peaks")
    eur_alps = []
    for t in eur_tabs:
        if re.search(r"\bAlps\b", t["section"] or "", re.I) or re.search(r"\bAlps\b", t["caption"], re.I):
            eur_alps.extend(t["rows"])
    say("   cross-check: Europe article Alps-section rows %d vs dedicated Alps list %d"
        % (len(eur_alps), len(alps)))

    # ---- R2 Himalayas
    say("[R2] Himalayas — list-of-ultras-of-the-himalayas (index states 76)")
    him, rej, unp = build_rows("list-of-ultras-of-the-himalayas")
    for u in unp:
        say("      A6 dropped (unparsable elev/prom): %s" % u)
    him = dedupe(him, "R2")
    say("   rejects: %s" % dict(rej))

    # ---- R3 Rockies (from the NA article's two dedicated sub-tables)
    say("[R3] Rockies — NA article sub-tables 'Canadian Rockies' + 'Rocky Mountains of the United States'")
    na_tabs = parse_tables("list-of-ultras-of-north-america")
    cands = [t for t in na_tabs
             if (re.search(r"Rocky Mountains", t["caption"], re.I)
                 or re.search(r"Rocky Mountains", t["section"] or "", re.I)) and t["nrows"] <= 60]
    for t in cands:
        say("   candidate sub-table: section=%r caption=%r rows=%d"
            % (t["section"][:40], t["caption"][:52], t["nrows"]))
    assert len(cands) == 2, "expected 2 Rockies sub-tables, found %d" % len(cands)
    assert sorted(t["nrows"] for t in cands) == [17, 19], \
        "Rockies sub-table row counts %s != [17, 19]" % sorted(t["nrows"] for t in cands)
    rock_tabs = cands
    rock, rej, _unp = build_rows("list-of-ultras-of-north-america", tables=rock_tabs)
    rock = dedupe(rock, "R3")
    say("   sub-table rows %s -> %d distinct (expected 19 + 17 = 36)"
        % ([t["nrows"] for t in rock_tabs], len(rock)))
    master = [t for t in na_tabs if re.search(r"ultra-prominent.*greater North", t["caption"], re.I)][0]
    mrows, _rej, _unp2 = build_rows("list-of-ultras-of-north-america", tables=[master])
    mrock = [r for r in mrows if r.get("rng") and re.search(r"rock", r["rng"], re.I)]
    say("   cross-check: master-table rows whose Mountain range mentions 'Rock*': %d" % len(mrock))
    rk_names = {normkey(r["name"]) for r in rock}
    mr_names = {normkey(r["name"]) for r in mrock}
    say("   cross-check overlap: %d of %d sub-table peaks also flagged Rocky in the master table"
        % (len(rk_names & mr_names), len(rk_names)))
    a0names = {(r["name"] or "").lower() for r in union} | {(r["link_target"] or "").lower() for r in union}
    inA0 = sum(1 for r in rock if r["name"].lower() in a0names
               or (r["link_target"] or "").lower() in a0names)
    say("   cross-check: %d of %d Rockies-arm peaks are also in the A0 union by name/link"
        % (inA0, len(rock)))

    # ---- E1 elevation-only arm
    say("")
    say("[E1] elevation-only arm — list-of-highest-mountains-on-earth")
    e1_tabs = parse_tables("list-of-highest-mountains-on-earth")
    say("   caption: %s" % (e1_tabs[0]["caption"][:120] if e1_tabs else "(none)"))
    e1_all, e1, e1_s = [], [], []
    for t in e1_tabs:
        if "elev" not in t["colmap"] or "name" not in t["colmap"]:
            continue
        for rec in t["rows"]:
            rank = (rec.get("rank") or "").strip()
            elev = num(rec.get("elev"))
            prom = num(rec.get("prom"))
            if elev is None:
                continue
            tgt, disp = link_target(rec.get("name") or "")
            row = dict(name=disp, link_target=tgt, key=(tgt or normkey(disp)), region="",
                       rng="", elev=elev, prom=prom, col=None, lat=None, lon=None, qid=None,
                       source="list-of-highest-mountains-on-earth", rank=rank,
                       subprominence=(not rank.isdigit()))
            e1_all.append(row)
            (e1_s if row["subprominence"] else e1).append(row)
    say("   rows with an elevation: %d ; numeric-rank rows %d (E1 primary) ; 'S' sub-prominence rows %d (E1b)"
        % (len(e1_all), len(e1), len(e1_s)))
    say("   E1 elevation range %.0f..%.0f m (dynamic range %.2fx)"
        % (min(r["elev"] for r in e1), max(r["elev"] for r in e1),
           max(r["elev"] for r in e1) / min(r["elev"] for r in e1)))
    noprom = sum(1 for r in e1_all if r["prom"] is None or r["prom"] > r["elev"] + 0.5)
    say("   E1 rows with missing/A1-violating prominence: %d (prominence is not the E1 membership rule)" % noprom)

    # ---- derived CSVs
    say("")
    say("[derived] writing CSVs (bytes, UTF-8, LF, no BOM)")
    cols = ["name", "link_target", "region", "rng", "elev", "prom", "col", "lat", "lon", "sources"]
    def prep(rows, sort_by="prom"):
        out = []
        for r in rows:
            out.append({k: r.get(k) for k in cols} | {"name": r["name"]})
        out.sort(key=lambda r: (-float(r[sort_by]), r["name"]))
        return out
    write_csv(DER / "mountains-global-ultras.csv", prep(union), cols)
    write_csv(DER / "mountains-alps.csv", prep(alps), cols)
    write_csv(DER / "mountains-himalayas.csv", prep(him), cols)
    write_csv(DER / "mountains-rockies.csv", prep(rock), cols)
    e1cols = ["name", "link_target", "rank", "elev", "prom", "subprominence"]
    e1rows = [{k: r.get(k) for k in e1cols} for r in
              sorted(e1_all, key=lambda r: (r["subprominence"], -r["elev"]))]
    write_csv(DER / "mountains-highest-by-elevation.csv", e1rows, e1cols)
    wdcols = ["name", "qid", "prom", "elev", "lat", "lon"]
    wdout = [{"name": r["name"], "qid": r["qid"], "prom": r["prom"], "elev": r["elev"],
              "lat": r["lat"], "lon": r["lon"]} for r in sorted(wd_recs, key=lambda r: -(r["prom"] or 0))]
    write_csv(DER / "mountains-wikidata-crosscheck.csv", wdout, wdcols)

    # ---- A0 vs Wikidata overlap (coverage cross-check)
    a0keys = {(r["key"] or normkey(r["name"])) for r in union}
    wdusable = {r["key"] for r in wd_recs if r["elev"] and r["prom"] and r["prom"] <= r["elev"] + 0.5
                and r["elev"] <= A1_ELEV_CEIL}
    say("")
    say("[coverage] A0 distinct %d ; Wikidata qids %d ; Wikidata qids passing A1 %d ; name overlap %d"
        % (len(a0keys), len(wd_recs), len(wdusable), len(a0keys & wdusable)))

    # ---- A5 monotonicity + A6/A7 report
    say("")
    say("[A5] within-source prominence monotonicity:")
    bad = 0
    for slug, _stated in A0_ARTICLES + [("list-of-alpine-peaks-by-prominence", 44),
                                        ("list-of-ultras-of-the-himalayas", 76)]:
        for t in parse_tables(slug):
            seq = [rec_numbers(r)[1] for r in t["rows"]]
            seq = [x for x in seq if x is not None]
            if seq and any(seq[i] < seq[i + 1] - 0.5 for i in range(len(seq) - 1)):
                bad += 1
    say("   tables with a non-monotone prominence column: %d (reported, not enforced: the "
        "source tables order by different keys)" % bad)
    say("[A6] rows dropped for missing elevation are counted in the per-article reject "
        "lines above ('missing elev/prom').")
    say("[A7] every derived CSV above was written from raw + this parser; hashes printed.")
    say("")
    say("[structural repairs] %d table(s) re-aligned (rows shorter than their header):" % len(set(REPAIRS)))
    for r in sorted(set(REPAIRS)):
        say("   %s" % r)
    say("[deviation] contract A2 names Everest 8848.86 m; the ultra lists carry %.0f m "
        "(rounded). The 8848.86 value appears in the coordinate-donor list and Wikidata. "
        "The primary set keeps the lists' rounded value." % ev[0]["elev"])

    out = ROOT / "results" / "stage3-parse-report.txt"
    out.write_bytes(("\n".join(REPORT) + "\n").encode("utf-8"))
    b = out.read_bytes()
    b.decode("utf-8")
    assert b"\r\n" not in b
    print("\nwrote", out, len(REPORT), "lines")


if __name__ == "__main__":
    main()
