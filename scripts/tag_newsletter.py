#!/usr/bin/env python3
"""
tag_newsletter.py — keyword-score newsletter items against the DA Capability Map.

Usage:
    python3 scripts/tag_newsletter.py [RUN_DIR]

If RUN_DIR is omitted, finds the most recent dated run directory under the
newsletter root.  Writes two files into RUN_DIR:
    capability_tags.json     — structured per-item capability linkages
    capability_summary.txt   — plain-text summary of most-active domains
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

NEWSLETTER_ROOT = Path("/home/pi/.openclaw/workspace/newsletters/digital-assets-custody")
DB_PATH = Path("/home/pi/.openclaw/workspace/projects/da-capability-map/data/capabilities.db")

# Words too common to be useful for matching
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "can", "that", "this", "these",
    "those", "it", "its", "as", "not", "no", "if", "so", "than", "then",
    "when", "where", "which", "who", "what", "how", "all", "any", "each",
    "more", "also", "into", "about", "over", "after", "before", "under",
    "between", "through", "during", "such", "per", "up", "out", "off",
    "their", "they", "them", "we", "our", "you", "your", "i", "my",
    "he", "she", "his", "her", "via", "within", "across", "without",
}


def find_latest_run() -> Path:
    """Return the most recent date-stamped run directory."""
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}$")
    candidates = sorted(
        (d for d in NEWSLETTER_ROOT.iterdir()
         if d.is_dir() and pattern.match(d.name)),
        key=lambda d: d.name,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(f"No dated run dirs found under {NEWSLETTER_ROOT}")
    return candidates[0]


def load_l2_capabilities() -> list[dict]:
    """Load all L2 capabilities with id, domain_id, name, description."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, domain_id, name, description FROM capabilities_l2")
    rows = cur.fetchall()
    conn.close()
    return [
        {"id": r[0], "domain_id": r[1], "name": r[2], "description": r[3] or ""}
        for r in rows
    ]


def tokenize(text: str) -> set[str]:
    """Lower-case word tokens, drop stopwords and short tokens."""
    tokens = re.findall(r"[a-zA-Z]+", text.lower())
    return {t for t in tokens if t not in STOPWORDS and len(t) > 2}


def build_capability_index(capabilities: list[dict]) -> list[dict]:
    """Precompute token sets for each L2 capability."""
    indexed = []
    for cap in capabilities:
        text = f"{cap['name']} {cap['description']}"
        indexed.append({**cap, "tokens": tokenize(text)})
    return indexed


def score_item(item_tokens: set[str], cap_index: list[dict]) -> list[dict]:
    """Score each L2 capability against the item tokens by overlap count."""
    scored = []
    for cap in cap_index:
        overlap = len(item_tokens & cap["tokens"])
        if overlap > 0:
            scored.append({"cap": cap, "score": overlap})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


def top_caps_unique_domains(scored: list[dict], n: int = 3) -> list[dict]:
    """Return top n scored capabilities, one per domain."""
    seen_domains: set[str] = set()
    result = []
    for entry in scored:
        domain = entry["cap"]["domain_id"]
        if domain not in seen_domains:
            seen_domains.add(domain)
            result.append(entry["cap"])
        if len(result) >= n:
            break
    return result


def parse_news_items(text: str) -> list[dict]:
    """
    Parse newsletter.txt into structured news items.

    Each item block starts with a numbered heading like "1. Headline - Readiness"
    and ends before the next numbered item or a section header.
    """
    # Split on numbered item headers: "1. Some Headline - Readiness tag"
    item_pattern = re.compile(
        r"^(\d+)\.\s+(.+?)\s+-\s+([^\n]+)$",
        re.MULTILINE,
    )
    # Also extract Strategic read from TLDR block
    tldr_pattern = re.compile(
        r"^-\s+(.+?)\.\s+Strategic read:\s+(.+?)\s+Readiness:\s+(.+?)\.$",
        re.MULTILINE,
    )

    # Build a map from headline (lower) -> strategic_read text from TLDR
    strategic_reads: dict[str, str] = {}
    for m in tldr_pattern.finditer(text):
        headline_hint = m.group(1).strip().lower()[:60]
        strategic_reads[headline_hint] = m.group(2).strip()

    items = []
    matches = list(item_pattern.finditer(text))
    for i, m in enumerate(matches):
        number = int(m.group(1))
        headline = m.group(2).strip()
        readiness = m.group(3).strip()

        # Extract body text between this match and next
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()

        # Try to find matching strategic read from TLDR
        headline_key = headline.lower()[:60]
        strategic_read = ""
        for key, val in strategic_reads.items():
            if key[:30] in headline_key or headline_key[:30] in key:
                strategic_read = val
                break

        items.append({
            "number": number,
            "headline": headline,
            "readiness": readiness,
            "body": body,
            "strategic_read": strategic_read,
        })

    return items


def tag_items(items: list[dict], cap_index: list[dict]) -> list[dict]:
    """Score each item and attach top-3 L2 capabilities."""
    tagged = []
    for item in items:
        search_text = f"{item['headline']} {item['strategic_read']} {item['body']}"
        item_tokens = tokenize(search_text)
        scored = score_item(item_tokens, cap_index)
        top = top_caps_unique_domains(scored, n=3)

        tagged.append({
            "headline": item["headline"],
            "readiness": item["readiness"],
            "l2_ids": [c["id"] for c in top],
            "l2_names": [c["name"] for c in top],
            "domains": [c["domain_id"] for c in top],
        })
    return tagged


def build_domain_summary(tagged_items: list[dict]) -> tuple[Counter, Counter]:
    """Count domain and L2 frequency across all tagged items."""
    domain_counter: Counter = Counter()
    l2_counter: Counter = Counter()
    for item in tagged_items:
        for domain in item["domains"]:
            domain_counter[domain] += 1
        for l2_id, l2_name in zip(item["l2_ids"], item["l2_names"]):
            l2_counter[f"{l2_id}: {l2_name}"] += 1
    return domain_counter, l2_counter


DOMAIN_LABELS = {
    "custody": "Custody",
    "wallets": "Wallets",
    "stablecoins": "Stablecoins",
    "cbdc": "CBDC & Digital Money",
    "settlement": "Settlement & Clearing",
    "tokenisation": "Tokenisation & RWAs",
    "defi_protocols": "DeFi Protocols",
    "security": "Security",
    "ai_agentic": "AI & Agentic",
    "compliance_regulation": "Compliance & Regulation",
}


def write_capability_summary(
    run_dir: Path,
    tagged_items: list[dict],
    domain_counter: Counter,
    l2_counter: Counter,
    issue_name: str,
) -> Path:
    lines = [
        f"Capability Map Linkages — {issue_name}",
        "=" * 60,
        "",
        "Most-active domains this issue:",
        "-" * 36,
    ]
    for domain, count in domain_counter.most_common():
        label = DOMAIN_LABELS.get(domain, domain)
        bar = "#" * count
        lines.append(f"  {label:<30} {bar} ({count})")

    lines += [
        "",
        "Top L2 capabilities (by frequency):",
        "-" * 36,
    ]
    for l2_label, count in l2_counter.most_common(10):
        lines.append(f"  [{count}x] {l2_label}")

    lines += [
        "",
        "Per-item linkages:",
        "-" * 36,
    ]
    for item in tagged_items:
        lines.append(f"  • {item['headline'][:70]}")
        lines.append(f"    Readiness: {item['readiness']}")
        if item["l2_names"]:
            lines.append("    L2 capabilities: " + " | ".join(item["l2_names"]))
        else:
            lines.append("    L2 capabilities: (none matched)")
        lines.append("")

    out_path = run_dir / "capability_summary.txt"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv

    if args:
        run_dir = Path(args[0])
        if not run_dir.is_absolute():
            run_dir = NEWSLETTER_ROOT / run_dir
    else:
        run_dir = find_latest_run()

    newsletter_txt = run_dir / "newsletter.txt"
    if not newsletter_txt.exists():
        print(f"ERROR: {newsletter_txt} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Tagging newsletter run: {run_dir.name}")

    text = newsletter_txt.read_text(encoding="utf-8")
    capabilities = load_l2_capabilities()
    cap_index = build_capability_index(capabilities)

    items = parse_news_items(text)
    if not items:
        print("WARNING: No news items parsed from newsletter.txt", file=sys.stderr)

    print(f"  Parsed {len(items)} news items")
    tagged = tag_items(items, cap_index)

    # Write capability_tags.json
    tags_path = run_dir / "capability_tags.json"
    tags_path.write_text(json.dumps({"items": tagged}, indent=2), encoding="utf-8")
    print(f"  Wrote {tags_path}")

    # Domain / L2 frequency
    domain_counter, l2_counter = build_domain_summary(tagged)

    # Write capability_summary.txt
    issue_name = run_dir.name
    summary_path = write_capability_summary(run_dir, tagged, domain_counter, l2_counter, issue_name)
    print(f"  Wrote {summary_path}")

    # Print summary to stdout for convenience
    print()
    print(summary_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
