#!/usr/bin/env python3
"""Check the Amazon Listing TXT delivery contract."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
TEMPLATE = ROOT / "references" / "listing-output-template.md"
REQUIRED = ("output/", "listing.txt", "main-secondary-images.txt", "aplus-plan.txt")
REQUIRED_PLAN_TOKENS = (
    "产品全部卖点",
    "核心卖点",
    "A+ 1",
    "核心卖点对应的问答",
)
FORBIDDEN_PLAN_TOKENS = (
    "## 图片创意简报",
    "## 图片创意简报要求",
    "画面建议。",
    "图中文字方向。",
)


def require_tokens(label: str, text: str) -> list[str]:
    return [f"{label}: missing {token}" for token in REQUIRED if token not in text]


def main() -> int:
    skill_text = SKILL.read_text(encoding="utf-8")
    template_text = TEMPLATE.read_text(encoding="utf-8")
    errors = require_tokens("SKILL.md", skill_text)
    errors += require_tokens("listing-output-template.md", template_text)
    for heading in ("产品卖点分析", "附图策划"):
        if heading not in template_text:
            errors.append(f"listing-output-template.md: missing {heading}")
    for token in REQUIRED_PLAN_TOKENS:
        if token not in skill_text:
            errors.append(f"SKILL.md: missing {token}")
        if token not in template_text:
            errors.append(f"listing-output-template.md: missing {token}")
    for token in FORBIDDEN_PLAN_TOKENS:
        if token in skill_text:
            errors.append(f"SKILL.md: forbidden legacy token {token}")
        if token in template_text:
            errors.append(f"listing-output-template.md: forbidden legacy token {token}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("TXT delivery contract is present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
