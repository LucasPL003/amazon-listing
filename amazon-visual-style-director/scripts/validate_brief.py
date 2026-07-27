"""Validate image creative briefs before visual direction begins."""

from typing import Any


REQUIRED_FIELDS = {
    "image_id", "image_type", "sales_task", "product_truth_lock", "exact_copy",
    "prompt_skeleton", "prohibited_content", "font_rights", "target_user_and_scene",
}
ALLOWED_IMAGE_TYPES = {"main", "secondary"}
NONEMPTY_FIELDS = {"image_id", "sales_task", "product_truth_lock", "target_user_and_scene", "prompt_skeleton", "prohibited_content"}


def _is_nonempty(value: Any) -> bool:
    return bool(value.strip()) if isinstance(value, str) else bool(value)


def _sample_candidate_selected(value: Any) -> bool:
    """Normalize Listing Agent boolean and Chinese affirmative marker values."""
    if isinstance(value, str):
        return value.strip().casefold() in {"true", "yes", "y", "1", "是"}
    return value is True or value == 1


def validate_brief(brief: dict[str, Any]) -> list[str]:
    """Return contract violations for one Listing Agent image brief."""
    if not isinstance(brief, dict):
        return ["简报必须为字典"]
    errors = [f"缺少 {field}" for field in sorted(REQUIRED_FIELDS - set(brief))]
    if brief.get("image_type") not in ALLOWED_IMAGE_TYPES:
        errors.append("image_type 必须为 main 或 secondary")
    for field in sorted(NONEMPTY_FIELDS):
        if field in brief and not _is_nonempty(brief[field]):
            errors.append(f"{field} 不能为空")
    copy = brief.get("exact_copy")
    if not isinstance(copy, dict) or not _is_nonempty(copy.get("language")):
        errors.append("exact_copy 必须包含 language")
    elif brief.get("image_type") == "main":
        if any(_is_nonempty(value) for key, value in copy.items() if key != "language"):
            errors.append("主图 exact_copy 除 language 外必须全部为空")
    elif brief.get("image_type") == "secondary" and not _is_nonempty(copy.get("headline")):
        errors.append("副图 exact_copy 必须包含 headline 和 language")
    rights = brief.get("font_rights", {})
    if not isinstance(rights, dict) or rights.get("status") not in {"user-provided", "open-license"} or not _is_nonempty(rights.get("path")):
        errors.append("font_rights 必须包含允许状态和字体路径")
    return errors


def validate_briefs(briefs: list[dict[str, Any]]) -> list[list[str]]:
    """Validate the ordered brief collection, including unique image IDs."""
    if not isinstance(briefs, list):
        raise ValueError("briefs 必须为列表")
    seen: set[str] = set()
    results: list[list[str]] = []
    for brief in briefs:
        errors = validate_brief(brief)
        image_id = brief.get("image_id") if isinstance(brief, dict) else None
        if isinstance(image_id, str) and image_id.strip():
            if image_id in seen:
                errors.append(f"image_id 重复: {image_id}")
            seen.add(image_id)
        results.append(errors)
    return results


def select_sample_candidate(briefs: list[dict[str, Any]]) -> dict[str, Any]:
    """Select the marked secondary sample, or the first secondary brief."""
    marked = [brief for brief in briefs if brief.get("image_type") == "secondary" and _sample_candidate_selected(brief.get("sample_candidate"))]
    secondary = [brief for brief in briefs if brief.get("image_type") == "secondary"]
    if marked:
        return marked[0]
    if secondary:
        return secondary[0]
    raise ValueError("至少需要一张副图作为三方向样张任务")