"""Validate deterministic visual-style-director output packages."""

import json
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError


CANVAS_SIZE = (1500, 1500)
IMAGE_ARTIFACTS = ("visual-plate.png", "typography-overlay.png", "final-image.png")
MANIFEST_ARTIFACT = "composition.json"
COMPOSITION_FIELDS = ("canvas", "style_id", "font_rights", "layers")
ROUTES = {
    "product-truth": "regenerate-visual-plate",
    "visual-composition": "regenerate-visual-plate",
    "text-accuracy": "rerender-typography-overlay",
    "typography-harmony": "redesign-composition",
    "style-id": "restart-direction-selection",
}


def _validate_composition(composition: Any, manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if not isinstance(composition, dict):
        return ["composition.json 必须为对象"]
    canvas = composition.get("canvas")
    if not isinstance(canvas, dict) or (canvas.get("width"), canvas.get("height")) != CANVAS_SIZE:
        errors.append("composition.json canvas 必须为 1500x1500")
    if not isinstance(composition.get("style_id"), str) or not composition["style_id"].strip():
        errors.append("composition.json style_id 必须为非空字符串")
    rights = composition.get("font_rights")
    if not isinstance(rights, dict) or rights.get("status") not in {"user-provided", "open-license"} or not rights.get("path"):
        errors.append("composition.json font_rights 格式无效")
    if not isinstance(composition.get("layers"), list):
        errors.append("composition.json layers 必须为列表")
    for field in COMPOSITION_FIELDS:
        if field not in manifest:
            errors.append(f"传入 manifest 缺少 {field}")
    for field, expected in manifest.items():
        if field == "renderer":
            continue
        if composition.get(field) != expected:
            errors.append(f"composition.json 与传入 manifest 的 {field} 不一致")
    return errors


def validate_output(package: Path, manifest: dict[str, object]) -> list[str]:
    """Return Chinese output-package contract violations without raising."""
    errors: list[str] = []
    if not isinstance(manifest, dict):
        errors.append("manifest 必须为字典")
        manifest = {}
    if not package.is_dir():
        return [*errors, "输出包目录不存在"]

    for artifact in (*IMAGE_ARTIFACTS, MANIFEST_ARTIFACT):
        if not (package / artifact).is_file():
            errors.append(f"缺少 {artifact}")

    for artifact in IMAGE_ARTIFACTS:
        image_path = package / artifact
        if not image_path.is_file():
            continue
        try:
            with Image.open(image_path) as image:
                if image.size != CANVAS_SIZE:
                    errors.append(f"{artifact} 尺寸必须为 1500x1500")
                if artifact == "typography-overlay.png" and image.mode != "RGBA":
                    errors.append("typography-overlay.png 必须为 RGBA 模式")
        except (OSError, UnidentifiedImageError):
            errors.append(f"无法读取 {artifact}")

    composition_path = package / MANIFEST_ARTIFACT
    if composition_path.is_file():
        try:
            composition = json.loads(composition_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            errors.append("composition.json 不是有效 JSON")
        else:
            errors.extend(_validate_composition(composition, manifest))
    return errors


def route_failure(category: str) -> str:
    """Return the deterministic rework action for one failed QA category."""
    return ROUTES[category]


def should_stop_retry(completed_attempts: int) -> bool:
    """Stop automatic rework after two completed attempts."""
    return completed_attempts >= 2