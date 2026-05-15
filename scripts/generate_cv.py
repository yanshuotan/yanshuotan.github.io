#!/usr/bin/env python3
"""
generate_cv.py
Reads all YAML data files and renders templates/cv.tex.j2 → output/cv.tex.

Usage:
    python scripts/generate_cv.py
"""

import yaml
import jinja2
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────

ROOT       = Path(__file__).parent.parent
DATA_DIR   = ROOT / "data"
TMPL_DIR   = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"

SELF_NAME  = "Tan, Yan Shuo"   # Must match exactly how it appears in authors

# ── YAML loading ─────────────────────────────────────────────────────────────

def load(name):
    with open(DATA_DIR / name) as f:
        return yaml.safe_load(f)

# ── LaTeX helpers ─────────────────────────────────────────────────────────────

_LATEX_ESCAPES = str.maketrans({
    "&":  r"\&",
    "%":  r"\%",
    "$":  r"\$",
    "#":  r"\#",
    "_":  r"\_",
    "^":  r"\^{}",
    "~":  r"\~{}",
    # don't escape backslash — caller controls LaTeX commands
})

def esc(text):
    """Escape special LaTeX characters in a plain-text string."""
    if text is None:
        return ""
    return str(text).translate(_LATEX_ESCAPES)


def first_last(last_first):
    """Convert 'Last, First' → 'First Last' for display."""
    if ", " in last_first:
        last, first = last_first.split(", ", 1)
        return f"{first} {last}"
    return last_first


def fmt_author(author):
    """
    Format one author entry for LaTeX.
    - Self name is bolded.
    - equal=True → appends \\eqc marker
    - supervised=True → appends \\sv marker
    - corresponding=True → appends \\corr marker
    """
    name = author["name"]
    display = first_last(name)

    if name == SELF_NAME:
        display = f"\\textbf{{{display}}}"

    markers = []
    if author.get("equal"):
        markers.append("\\eqc")
    if author.get("supervised"):
        markers.append("\\sv")
    if author.get("corresponding"):
        markers.append("\\corr")

    if markers:
        display += "".join(f"$^{{{m}}}$" for m in markers)

    return display


def fmt_author_list(authors):
    """Comma-separated author list with 'and' before last author."""
    parts = [fmt_author(a) for a in authors]
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return ", ".join(parts[:-1]) + ", and " + parts[-1]


def fmt_venue(pub):
    """
    Build the venue / status fragment for one publication.
    Returns a LaTeX string like:
        \\textit{JMLR}, vol. 24, no. 58, pp. 1--47, 2023
        \\textit{Annals of Statistics}, to appear
        submitted to \\textit{JASA}, 2023
        in revision, 2022
    """
    venue        = pub.get("venue", "")
    year         = pub.get("year", "")
    status       = pub.get("status", "published")
    review       = pub.get("review_status")
    notes        = pub.get("notes", "") or ""
    volume       = pub.get("volume")
    number       = pub.get("number")
    pages        = pub.get("pages")

    # Build venue + volume/number/pages fragment
    if venue and "arXiv" not in venue:
        venue_tex = f"\\textit{{{esc(venue)}}}"
        detail_parts = [venue_tex]
        if volume:
            detail_parts.append(f"vol.~{volume}")
        if number:
            detail_parts.append(f"no.~{number}")
        if pages:
            detail_parts.append(f"pp.~{esc(str(pages))}")
        detail = ", ".join(detail_parts)
    else:
        detail = ""

    # Status suffix
    if status == "published":
        return f"{detail}, {year}".strip(", ") if detail else str(year)
    if status == "accepted":
        return f"{detail}, to appear".strip(", ") if detail else "to appear"

    # Preprint statuses
    if review == "RR":
        target = (notes.replace("R&R at ", "").replace("R\\&R at ", "")).strip()
        if target:
            return f"in revision at \\textit{{{esc(target)}}}"
        return "in revision"
    if review == "major_revision":
        target = notes.replace("Major revision at ", "").strip()
        if target:
            return f"major revision at \\textit{{{esc(target)}}}"
        return "major revision"
    # under_review / minor_revision: show no label, just year
    if review in ("under_review", "minor_revision"):
        pass

    # In-preparation (no venue)
    if pub.get("type") == "inprep":
        return ""

    # Plain preprint
    return f"arXiv preprint, {year}" if year else "arXiv preprint"


def fmt_pub_entry(pub, number):
    """Render one full publication list item as LaTeX."""
    authors = fmt_author_list(pub.get("authors", []))
    title   = esc(pub["title"])
    venue   = fmt_venue(pub)
    url     = pub.get("url") or pub.get("doi") or ""
    awards  = pub.get("awards", []) or []

    # Wrap title in hyperlink if URL available
    if url:
        title_tex = f"\\href{{{url}}}{{``{title}''}}"
    else:
        title_tex = f"``{title}''"

    award_tex = ""
    if awards:
        award_tex = " \\textbf{(" + "; ".join(esc(a) for a in awards) + ")}"

    return f"    \\item {authors}, {title_tex}, \\textit{{{esc(venue)}}}{award_tex}."


# ── Sorting helpers ───────────────────────────────────────────────────────────

_TYPE_ORDER   = {"journal": 0, "conference": 1, "preprint": 2, "thesis": 3, "other": 4}
_STATUS_ORDER = {"accepted": 0, "published": 1, "preprint": 2}

def pub_sort_key(p):
    return (
        -(p.get("year") or 0),
        _STATUS_ORDER.get(p.get("status", "preprint"), 9),
    )

def split_pubs(all_pubs):
    """Return (journal_pubs, conf_pubs, preprints, inprep) sorted lists."""
    journals = sorted(
        [p for p in all_pubs
         if p["type"] == "journal" and p["status"] in ("published", "accepted")],
        key=pub_sort_key,
    )
    confs = sorted(
        [p for p in all_pubs
         if p["type"] == "conference" and p["status"] in ("published", "accepted")],
        key=pub_sort_key,
    )
    preprints = sorted(
        [p for p in all_pubs
         if p["type"] not in ("inprep", "thesis", "other")
         and p["status"] == "preprint"],
        key=pub_sort_key,
    )
    inprep = [p for p in all_pubs if p["type"] == "inprep"]
    return journals, confs, preprints, inprep


# ── Jinja2 environment ────────────────────────────────────────────────────────

def make_env():
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TMPL_DIR)),
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>",
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )
    env.filters["esc"]             = esc
    env.filters["first_last"]      = first_last
    env.filters["fmt_author_list"] = fmt_author_list
    env.filters["fmt_venue"]       = fmt_venue
    env.filters["fmt_pub_entry"]   = fmt_pub_entry
    return env


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Load all data
    profile  = load("profile.yaml")
    misc     = load("misc.yaml")
    pubs_raw = load("publications.yaml")["publications"]
    talks    = load("talks.yaml")["talks"]
    posters  = load("posters.yaml")["posters"]
    students = load("students.yaml")
    teaching = load("teaching.yaml")["teaching"]
    service  = load("service.yaml")

    # Compute year_range for each talk/poster dynamically from instance years
    for talk in talks + posters:
        years = [inst["year"] for inst in talk.get("instances", []) if inst.get("year")]
        talk["year_range"] = [min(years), max(years)] if years else [0, 0]

    # Process publications
    journals, confs, preprints, inprep = split_pubs(pubs_raw)

    # Assign continuous numbering (journals → confs → preprints → inprep)
    n = 1
    for pub in journals:
        pub["_num"] = n; n += 1
    for pub in confs:
        pub["_num"] = n; n += 1
    for pub in preprints:
        pub["_num"] = n; n += 1
    for pub in inprep:
        pub["_num"] = n; n += 1

    # Render
    env      = make_env()
    template = env.get_template("cv.tex.j2")
    rendered = template.render(
        profile       = profile,
        misc          = misc,
        journal_pubs  = journals,
        conf_pubs     = confs,
        preprints     = preprints,
        inprep_pubs   = inprep,
        talks         = talks,
        posters       = posters,
        students      = students,
        teaching      = teaching,
        service       = service,
        # helper functions also available as globals in template
        esc           = esc,
        fmt_author_list = fmt_author_list,
        fmt_venue     = fmt_venue,
        fmt_pub_entry = fmt_pub_entry,
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / "cv.tex"
    out.write_text(rendered)
    print(f"✓  CV written to {out}")
    print(f"   Compile with: pdflatex {out}")


if __name__ == "__main__":
    main()
