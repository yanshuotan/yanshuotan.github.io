#!/usr/bin/env python3
"""
generate_site.py
Processes YAML data files and populates site/_data/ for Jekyll.

Pre-computes HTML-formatted strings (author lists, venue lines) so that
Jekyll's Liquid templates don't need complex string manipulation.

Usage:
    python scripts/generate_site.py
"""

import yaml
import re
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT      = Path(__file__).parent.parent
DATA_DIR  = ROOT / "data"
SITE_DATA = ROOT / "site" / "_data"

SELF_NAME = "Tan, Yan Shuo"

# ── YAML helpers ──────────────────────────────────────────────────────────────

def load(name):
    with open(DATA_DIR / name) as f:
        return yaml.safe_load(f)

def dump(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    print(f"  ✓  {path.relative_to(ROOT)}")

# ── HTML formatting helpers ───────────────────────────────────────────────────

def html_escape(text):
    if text is None:
        return ""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))

def first_last(last_first):
    """'Last, First' → 'First Last'"""
    if ", " in last_first:
        last, first = last_first.split(", ", 1)
        return f"{first} {last}"
    return last_first

def fmt_author_html(author):
    """Format one author as HTML with bold + superscript markers."""
    name    = author["name"]
    display = html_escape(first_last(name))

    if name == SELF_NAME:
        display = f"<strong>{display}</strong>"

    markers = []
    if author.get("equal"):
        markers.append("*")
    if author.get("supervised"):
        markers.append("†")
    if author.get("corresponding"):
        markers.append("‡")

    if markers:
        display += f"<sup>{''.join(markers)}</sup>"

    return display

def fmt_author_list_html(authors):
    parts = [fmt_author_html(a) for a in authors]
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return ", ".join(parts[:-1]) + ", and " + parts[-1]

def fmt_venue_html(pub):
    """Build an HTML venue / status string."""
    venue   = pub.get("venue", "")
    year    = pub.get("year", "")
    status  = pub.get("status", "published")
    review  = pub.get("review_status")
    notes   = pub.get("notes", "") or ""
    volume  = pub.get("volume")
    number  = pub.get("number")
    pages   = pub.get("pages")

    if venue and "arXiv" not in venue:
        detail_parts = [f"<em>{html_escape(venue)}</em>"]
        if volume:
            detail_parts.append(f"vol.&nbsp;{volume}")
        if number:
            detail_parts.append(f"no.&nbsp;{number}")
        if pages:
            detail_parts.append(f"pp.&nbsp;{html_escape(str(pages))}")
        detail = ", ".join(detail_parts)
    else:
        detail = ""

    if status == "published":
        return f"{detail}, {year}".strip(", ") if detail else str(year)
    if status == "accepted":
        suffix = f"{detail}, <em>to appear</em>".strip(", ")
        return suffix if suffix else "<em>to appear</em>"

    if review == "RR":
        target = notes.replace("R&R at ", "").strip()
        if target:
            return f"<em>in revision</em> at <em>{html_escape(target)}</em>"
        return "<em>in revision</em>"
    if review == "major_revision":
        target = notes.replace("Major revision at ", "").strip()
        if target:
            return f"<em>major revision</em> at <em>{html_escape(target)}</em>"
        return "<em>major revision</em>"

    return f"arXiv preprint, {year}" if year else "arXiv preprint"

def pub_url(pub):
    if pub.get("url"):
        return pub["url"]
    if pub.get("arxiv"):
        return f"https://arxiv.org/abs/{pub['arxiv']}"
    if pub.get("doi"):
        return f"https://doi.org/{pub['doi']}"
    return None

# ── Publication processing ────────────────────────────────────────────────────

_TYPE_ORDER   = {"journal": 0, "conference": 1, "preprint": 2, "thesis": 3, "other": 4}
_STATUS_ORDER = {"accepted": 0, "published": 1, "preprint": 2}

def pub_sort_key(p):
    return (-(p.get("year") or 0), _STATUS_ORDER.get(p.get("status", "preprint"), 9))

def enrich_pub(pub, number):
    """Add pre-computed display fields to a publication dict."""
    p = dict(pub)
    p["number"]       = number
    p["author_html"]  = fmt_author_list_html(pub.get("authors", []))
    p["venue_html"]   = fmt_venue_html(pub)
    p["link"]         = pub_url(pub)
    p["has_equal"]    = any(a.get("equal") for a in pub.get("authors", []))
    p["has_supervised"] = any(a.get("supervised") for a in pub.get("authors", []))
    p["title_escaped"] = html_escape(pub.get("title", ""))
    return p

def split_and_enrich(all_pubs):
    journals  = sorted([p for p in all_pubs if p["type"] == "journal"
                        and p["status"] in ("published", "accepted")], key=pub_sort_key)
    confs     = sorted([p for p in all_pubs if p["type"] == "conference"
                        and p["status"] in ("published", "accepted")], key=pub_sort_key)
    preprints = sorted([p for p in all_pubs if p["status"] == "preprint"], key=pub_sort_key)

    n = 1
    for p in journals:
        p["_num"] = n; n += 1
    for p in confs:
        p["_num"] = n; n += 1
    for p in preprints:
        p["_num"] = n; n += 1

    journals  = [enrich_pub(p, p["_num"]) for p in journals]
    confs     = [enrich_pub(p, p["_num"]) for p in confs]
    preprints = [enrich_pub(p, p["_num"]) for p in preprints]

    return journals, confs, preprints

# ── Service processing ───────────────────────────────────────────────────────

def aggregate_reviewing(flat_list):
    """
    Convert flat per-paper reviewing entries → grouped per-venue entries.
    Strips the private 'title' field. Output matches the old years-list schema
    so templates need no changes.
    """
    groups = {}
    for entry in flat_list:
        venue = entry["venue"]
        if venue not in groups:
            groups[venue] = {
                "venue":       venue,
                "venue_short": entry.get("venue_short"),
                "type":        entry.get("type", "journal"),
                "years":       [],
            }
        year = entry.get("year")
        if year and year not in groups[venue]["years"]:
            groups[venue]["years"].append(year)
    # Sort years within each venue, return in original venue order
    result = []
    seen = []
    for entry in flat_list:
        venue = entry["venue"]
        if venue not in seen:
            seen.append(venue)
            groups[venue]["years"].sort()
            result.append(groups[venue])
    return result

# ── Talk processing ───────────────────────────────────────────────────────────

_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def fmt_date(year, month=None):
    """Return 'Mon YYYY' if month given, else 'YYYY'."""
    if month:
        return f"{_MONTHS[int(month) - 1]} {year}"
    return str(year)

def enrich_talk(talk):
    t = dict(talk)
    years = [inst["year"] for inst in talk.get("instances", []) if inst.get("year")]
    t["year_range"] = [min(years), max(years)] if years else [0, 0]
    # Add date_display to each instance
    instances = []
    for inst in talk.get("instances", []):
        i = dict(inst)
        i["date_display"] = fmt_date(inst.get("year", ""), inst.get("month"))
        instances.append(i)
    t["instances"] = instances
    return t

def enrich_poster(poster):
    """Same enrichment as talks."""
    return enrich_talk(poster)

# ── Stats computation ─────────────────────────────────────────────────────────

def compute_stats(all_pubs, reviewing_flat, talks_raw, posters_raw, students_data):
    from collections import Counter
    import datetime
    current_year = datetime.date.today().year

    # ── Collaborators ──────────────────────────────────────────────────────────
    coauthor_counts = Counter()
    for pub in all_pubs:
        if pub.get("type") == "inprep":
            continue
        for author in pub.get("authors", []):
            name = author["name"]
            if name != SELF_NAME:
                coauthor_counts[first_last(name)] += 1
    collaborators = [
        {"name": name, "papers": count}
        for name, count in sorted(coauthor_counts.items(), key=lambda x: -x[1])
    ]

    # ── Publications ───────────────────────────────────────────────────────────
    pub_counts = {"journal": 0, "conference": 0, "preprint": 0, "total": 0}
    for pub in all_pubs:
        if pub.get("type") == "inprep":
            continue
        t = pub.get("type", "other")
        status = pub.get("status", "preprint")
        if t == "journal" and status in ("published", "accepted"):
            pub_counts["journal"] += 1
        elif t == "conference" and status in ("published", "accepted"):
            pub_counts["conference"] += 1
        elif status == "preprint":
            pub_counts["preprint"] += 1
        pub_counts["total"] += 1

    # ── Reviewing ─────────────────────────────────────────────────────────────
    journal_rev  = sum(1 for r in reviewing_flat if r.get("type") == "journal")
    conf_rev     = sum(1 for r in reviewing_flat if r.get("type") == "conference")

    # ── Talks ─────────────────────────────────────────────────────────────────
    talk_instances   = sum(len(t.get("instances", [])) for t in talks_raw)
    poster_instances = sum(len(p.get("instances", [])) for p in posters_raw)
    locations = sorted({
        inst["location"]
        for collection in (talks_raw, posters_raw)
        for item in collection
        for inst in item.get("instances", [])
        if inst.get("location")
    })

    # ── Students ──────────────────────────────────────────────────────────────
    students = students_data.get("students", [])
    current   = [s for s in students if s.get("expected") and (s.get("year_end") or 0) >= current_year]
    graduated = [s for s in students if not s.get("expected") or (s.get("year_end") or 0) < current_year]
    def count_by_degree(lst):
        c = Counter(s.get("degree", "Other") for s in lst)
        return dict(c)

    return {
        "collaborators": collaborators,
        "publications": pub_counts,
        "reviewing": {
            "total":      journal_rev + conf_rev,
            "journal":    journal_rev,
            "conference": conf_rev,
        },
        "talks": {
            "total_instances":   talk_instances,
            "poster_instances":  poster_instances,
            "unique_locations":  locations,
            "num_locations":     len(locations),
        },
        "students": {
            "current_count":    len(current),
            "graduated_count":  len(graduated),
            "current_by_degree":   count_by_degree(current),
            "graduated_by_degree": count_by_degree(graduated),
        },
    }

# ── News feed ────────────────────────────────────────────────────────────────

def fmt_news_date(date_str):
    """Format 'YYYY-MM' or 'YYYY-MM-DD' → 'Mon YYYY'; 'YYYY' → 'YYYY'."""
    parts = str(date_str).split("-")
    if len(parts) >= 2:
        try:
            return f"{_MONTHS[int(parts[1]) - 1]} {parts[0]}"
        except (ValueError, IndexError):
            pass
    return date_str

def build_news_feed(news_manual, all_pubs, students_data, cutoff_year):
    """
    Merge manual news entries with auto-generated items from publications
    and new students. Returns list sorted by date descending.
    """
    items = []

    # ── Manual entries (awards, hiring, etc.) ─────────────────────────────────
    for entry in news_manual.get("news", []):
        items.append({
            "date":         str(entry["date"]),
            "date_display": fmt_news_date(str(entry["date"])),
            "category":     entry.get("category", "other"),
            "text":         entry.get("text", ""),
            "url":          entry.get("url"),
        })

    # ── Auto: recent paper acceptances / publications ─────────────────────────
    for pub in all_pubs:
        year = pub.get("year") or 0
        if year < cutoff_year:
            continue
        status = pub.get("status", "preprint")
        if status not in ("published", "accepted"):
            continue
        if pub.get("type") in ("thesis", "other", "inprep"):
            continue
        venue = pub.get("venue_short") or pub.get("venue", "")
        date_str = f"{year}-07"   # mid-year proxy
        verb = "published in" if status == "published" else "accepted at"
        url = pub.get("url") or (
            f"https://arxiv.org/abs/{pub['arxiv']}" if pub.get("arxiv") else None
        )
        items.append({
            "date":         date_str,
            "date_display": str(year),
            "category":     "paper",
            "text":         f"Paper {verb} <em>{html_escape(venue)}</em>.",
            "title":        pub.get("title"),
            "url":          url,
        })

    items.sort(key=lambda x: x["date"], reverse=True)
    return items

# ── Teaching processing ───────────────────────────────────────────────────────

def enrich_teaching(course):
    """Add semesters_enriched: list of {name, url} for each semester."""
    c = dict(course)
    links = course.get("semester_links") or {}
    c["semesters_enriched"] = [
        {"name": s, "url": links.get(s)}
        for s in course.get("semesters", [])
    ]
    return c

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Generating site/_data/ …")

    # Pass-through files (minimal processing)
    for fname in ("profile.yaml", "misc.yaml", "photos.yaml"):
        dump(load(fname), SITE_DATA / fname)

    # Students — pass through
    dump(load("students.yaml"), SITE_DATA / "students.yaml")

    # Teaching — enrich with per-semester links
    teaching_raw = load("teaching.yaml")["teaching"]
    dump({"teaching": [enrich_teaching(c) for c in teaching_raw]}, SITE_DATA / "teaching.yaml")

    # Service — aggregate flat reviewing list into per-venue groups
    service_raw = load("service.yaml")
    service_out = dict(service_raw)
    service_out["reviewing"] = aggregate_reviewing(service_raw.get("reviewing", []))
    dump(service_out, SITE_DATA / "service.yaml")

    # Talks — add display fields
    talks_raw = load("talks.yaml")["talks"]
    dump({"talks": [enrich_talk(t) for t in talks_raw]}, SITE_DATA / "talks.yaml")

    # Posters — same enrichment as talks
    posters_raw = load("posters.yaml")["posters"]
    dump({"posters": [enrich_poster(p) for p in posters_raw]}, SITE_DATA / "posters.yaml")

    # Publications — split into three lists with HTML formatting
    all_pubs = load("publications.yaml")["publications"]
    journals, confs, preprints = split_and_enrich(all_pubs)
    dump({"publications": journals},  SITE_DATA / "journal_pubs.yaml")
    dump({"publications": confs},     SITE_DATA / "conf_pubs.yaml")
    dump({"publications": preprints}, SITE_DATA / "preprints.yaml")

    # News feed — manual entries merged with auto-generated items
    import datetime
    cutoff_year = datetime.date.today().year - 2
    news_manual = load("news.yaml")
    news_items  = build_news_feed(news_manual, load("publications.yaml")["publications"],
                                  load("students.yaml"), cutoff_year)
    dump({"news": news_items}, SITE_DATA / "news.yaml")

    # Stats — computed from all data sources
    stats = compute_stats(
        all_pubs      = load("publications.yaml")["publications"],
        reviewing_flat= load("service.yaml").get("reviewing", []),
        talks_raw     = talks_raw,
        posters_raw   = posters_raw,
        students_data = load("students.yaml"),
    )
    dump(stats, SITE_DATA / "stats.yaml")

    print("Done.")

if __name__ == "__main__":
    main()
