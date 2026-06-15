#!/usr/bin/env python3
"""
post_process_newsletter.py — run the newsletter generator then capability-tag the output.

Usage:
    python3 scripts/post_process_newsletter.py [-- NEWSLETTER_ARGS...]

Any arguments after '--' are forwarded to run_deterministic_newsletter.py.
The script:
  1. Runs run_deterministic_newsletter.py (in the newsletter root)
  2. Finds the most recent run directory produced
  3. Calls tag_newsletter.py against it
  4. Appends a "Capability Map Linkages" section to newsletter.txt
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

NEWSLETTER_ROOT = Path("/home/pi/.openclaw/workspace/newsletters/digital-assets-custody")
NEWSLETTER_SCRIPT = NEWSLETTER_ROOT / "run_deterministic_newsletter.py"
CAPABILITY_MAP_SCRIPTS = Path("/home/pi/.openclaw/workspace/projects/da-capability-map/scripts")
TAG_SCRIPT = CAPABILITY_MAP_SCRIPTS / "tag_newsletter.py"

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


def append_capability_linkages(run_dir: Path) -> None:
    """Read capability_tags.json and append a section to newsletter.txt."""
    tags_path = run_dir / "capability_tags.json"
    if not tags_path.exists():
        print(f"WARNING: {tags_path} not found — skipping append", file=sys.stderr)
        return

    data = json.loads(tags_path.read_text(encoding="utf-8"))
    items = data.get("items", [])

    # Count L2 frequency across all items
    l2_counter: Counter = Counter()
    for item in items:
        for l2_id, l2_name in zip(item.get("l2_ids", []), item.get("l2_names", [])):
            l2_counter[f"{l2_name} [{l2_id}]"] += 1

    # Build the section text
    lines = [
        "",
        "---",
        "Capability Map Linkages",
        "",
        "Top 5 L2 capabilities most referenced in this issue:",
    ]
    for l2_label, count in l2_counter.most_common(5):
        lines.append(f"  [{count}x] {l2_label}")

    lines += [
        "",
        "Per-item capability linkages:",
    ]
    for item in items:
        headline = item.get("headline", "")[:72]
        readiness = item.get("readiness", "")
        l2_names = item.get("l2_names", [])
        domains = item.get("domains", [])
        domain_labels = [DOMAIN_LABELS.get(d, d) for d in domains]
        lines.append(f"  • {headline}")
        if l2_names:
            lines.append(f"    Capabilities: {' | '.join(l2_names)}")
            lines.append(f"    Domains: {' | '.join(domain_labels)}")
        else:
            lines.append("    Capabilities: (none matched)")
        lines.append(f"    Readiness: {readiness}")
        lines.append("")

    section = "\n".join(lines)

    newsletter_txt = run_dir / "newsletter.txt"
    existing = newsletter_txt.read_text(encoding="utf-8")

    # Idempotency: don't append twice
    if "Capability Map Linkages" in existing:
        print("  Capability Map Linkages section already present — skipping append")
        return

    newsletter_txt.write_text(existing + section, encoding="utf-8")
    print(f"  Appended Capability Map Linkages section to {newsletter_txt}")


def main() -> int:
    # Split off args meant for the newsletter script
    argv = sys.argv[1:]
    newsletter_args: list[str] = []
    if "--" in argv:
        sep = argv.index("--")
        newsletter_args = argv[sep + 1:]
        argv = argv[:sep]

    # Step 1: run the newsletter generator
    print(f"Running newsletter generator: {NEWSLETTER_SCRIPT}")
    cmd = [sys.executable, str(NEWSLETTER_SCRIPT)] + newsletter_args
    result = subprocess.run(cmd, cwd=str(NEWSLETTER_ROOT))
    if result.returncode not in (0, 1):
        print(f"Newsletter script exited with code {result.returncode}", file=sys.stderr)
        # Don't abort — still try to tag whatever was written

    # Step 2: find the run directory that was just produced
    try:
        run_dir = find_latest_run()
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"\nPost-processing run: {run_dir.name}")

    # Step 3: capability-tag the newsletter
    tag_cmd = [sys.executable, str(TAG_SCRIPT), str(run_dir)]
    tag_result = subprocess.run(tag_cmd)
    if tag_result.returncode != 0:
        print("WARNING: tag_newsletter.py exited non-zero", file=sys.stderr)

    # Step 4: append capability linkages section to newsletter.txt
    append_capability_linkages(run_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
