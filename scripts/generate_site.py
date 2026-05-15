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

# ── Talk processing ───────────────────────────────────────────────────────────

def enrich_talk(talk):
    t = dict(talk)
    t["year_display"] = (
        str(talk["year_range"][0])
        if talk["year_range"][0] == talk["year_range"][1]
        else f"{talk['year_range'][0]}–{talk['year_range'][1]}"
    )
    return t

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Generating site/_data/ …")

    # Pass-through files (minimal processing)
    for fname in ("profile.yaml", "misc.yaml"):
        dump(load(fname), SITE_DATA / fname)

    # Students — pass through
    dump(load("students.yaml"), SITE_DATA / "students.yaml")

    # Teaching — pass through
    dump(load("teaching.yaml"), SITE_DATA / "teaching.yaml")

    # Service — pass through
    dump(load("service.yaml"), SITE_DATA / "service.yaml")

    # Talks — add display fields
    talks_raw = load("talks.yaml")["talks"]
    dump({"talks": [enrich_talk(t) for t in talks_raw]}, SITE_DATA / "talks.yaml")

    # Publications — split into three lists with HTML formatting
    all_pubs = load("publications.yaml")["publications"]
    journals, confs, preprints = split_and_enrich(all_pubs)
    dump({"publications": journals},  SITE_DATA / "journal_pubs.yaml")
    dump({"publications": confs},     SITE_DATA / "conf_pubs.yaml")
    dump({"publications": preprints}, SITE_DATA / "preprints.yaml")

    print("Done.")

if __name__ == "__main__":
    main()
