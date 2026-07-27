#!/usr/bin/env python3
"""Create a structured output folder for Amazon JP image generation work."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "amazon-jp-image-project"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create folders and a manifest for Amazon JP image projects."
    )
    parser.add_argument("name", help="Project or product name.")
    parser.add_argument(
        "--root",
        default=".",
        help="Output root directory. Defaults to the current directory.",
    )
    parser.add_argument(
        "--competitor-url",
        action="append",
        default=[],
        help="Amazon.co.jp competitor URL. Can be passed multiple times.",
    )
    args = parser.parse_args()

    project_dir = Path(args.root).expanduser().resolve() / slugify(args.name)
    subdirs = [
        "01-competitor-images",
        "02-competitor-screenshots",
        "03-analysis",
        "04-user-product-assets",
        "05-generated-images",
        "06-prompts",
    ]
    for subdir in subdirs:
        (project_dir / subdir).mkdir(parents=True, exist_ok=True)

    manifest = {
        "project": args.name,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "competitor_urls": args.competitor_url,
        "folders": subdirs,
        "notes": [
            "Store competitor images for reference only.",
            "Generated images must use user-owned or permissible assets.",
        ],
    }
    manifest_path = project_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(project_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
