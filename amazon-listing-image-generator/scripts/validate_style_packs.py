from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_FIELDS = (
    "id",
    "name",
    "categories",
    "audiences",
    "use_scenarios",
    "purchase_emotions",
    "not_for",
    "visual_direction",
    "consistency_rules",
    "prohibited_elements",
    "references",
)
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
JSON_BLOCK = re.compile(r"```json[ \t]*\r?\n(.*?)\r?\n```", re.DOTALL)


@dataclass(frozen=True)
class StylePack:
    pack_id: str
    name: str
    root: Path
    references: dict[str, tuple[Path, ...]]


@dataclass
class ValidationReport:
    packs: list[StylePack]
    errors: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "available_count": len(self.packs),
            "packs": [{"id": pack.pack_id, "name": pack.name} for pack in self.packs],
            "errors": self.errors,
        }


def _manifest_from(path: Path) -> tuple[dict[str, object] | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        return None, f"无法读取清单：{error}"
    blocks = JSON_BLOCK.findall(text)
    if len(blocks) != 1:
        return None, "必须包含且仅包含一个 json 代码块"
    try:
        manifest = json.loads(blocks[0])
    except json.JSONDecodeError as error:
        return None, f"JSON 无效：{error.msg}"
    if not isinstance(manifest, dict):
        return None, "JSON 清单必须是对象"
    return manifest, None


def _reference_paths(pack_root: Path, references: object, errors: list[str], directory: str) -> dict[str, tuple[Path, ...]]:
    if not isinstance(references, dict):
        errors.append(f"{directory} references 必须是对象")
        return {}

    resolved_references: dict[str, tuple[Path, ...]] = {}
    pack_root_resolved = pack_root.resolve()
    for role, values in references.items():
        if not isinstance(role, str) or not isinstance(values, list):
            errors.append(f"{directory} references 格式无效")
            continue
        paths: list[Path] = []
        for relative_path in values:
            if not isinstance(relative_path, str):
                errors.append(f"{directory} 参考图路径必须是字符串")
                continue
            candidate = (pack_root / relative_path).resolve()
            try:
                candidate.relative_to(pack_root_resolved)
            except ValueError:
                errors.append(f"{directory} 参考图必须位于样式包目录内：{relative_path}")
                continue
            if candidate.suffix.lower() not in IMAGE_EXTENSIONS:
                errors.append(f"{directory} 参考图格式不支持：{relative_path}")
                continue
            if not candidate.is_file():
                errors.append(f"{directory} 参考图不存在：{relative_path}")
                continue
            paths.append(candidate)
        resolved_references[role] = tuple(paths)
    return resolved_references


def validate_style_packs(root: Path) -> ValidationReport:
    """Ignore _template; parse every style-pack.md; return valid packs and Chinese errors."""
    root = Path(root)
    if not root.exists():
        return ValidationReport([], [f"Style Pack \u6839\u8def\u5f84\u4e0d\u5b58\u5728\uff1a{root}"])
    if not root.is_dir():
        return ValidationReport([], [f"Style Pack \u6839\u8def\u5f84\u5fc5\u987b\u662f\u76ee\u5f55\uff1a{root}"])

    packs: list[StylePack] = []
    errors: list[str] = []
    seen_ids: set[str] = set()
    for pack_root in sorted((path for path in root.iterdir() if path.is_dir() and path.name != "_template"), key=lambda path: path.name):
        directory = pack_root.name
        manifest_path = pack_root / "style-pack.md"
        if not manifest_path.is_file():
            errors.append(f"{directory} 缺少 style-pack.md")
            continue
        manifest, parse_error = _manifest_from(manifest_path)
        if parse_error:
            errors.append(f"{directory} {parse_error}")
            continue
        assert manifest is not None

        pack_errors: list[str] = []
        missing = [field for field in REQUIRED_FIELDS if field not in manifest]
        for field in missing:
            pack_errors.append(f"{directory} 缺少字段：{field}")
        for field in ("price", "price_positioning"):
            if field in manifest:
                pack_errors.append(f"{directory} 不支持字段：{field}")

        pack_id = manifest.get("id")
        name = manifest.get("name")
        if not isinstance(pack_id, str) or not pack_id:
            pack_errors.append(f"{directory} id 必须是非空字符串")
        elif pack_id in seen_ids:
            pack_errors.append(f"Style Pack ID 重复：{pack_id}")
        else:
            seen_ids.add(pack_id)
        if not isinstance(name, str) or not name:
            pack_errors.append(f"{directory} name 必须是非空字符串")

        references = _reference_paths(pack_root, manifest.get("references"), pack_errors, directory)
        if not references.get("generic"):
            pack_errors.append(f"{directory} 缺少 generic 参考图")

        if pack_errors:
            errors.extend(pack_errors)
            continue
        assert isinstance(pack_id, str) and isinstance(name, str)
        packs.append(StylePack(pack_id, name, pack_root, references))
    return ValidationReport(packs, errors)


def reference_for_role(pack: StylePack, role: str) -> Path:
    """Return role-specific reference first, otherwise the generic reference."""
    return (pack.references.get(role) or pack.references["generic"])[0]


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("用法：validate_style_packs.py <style-pack-root>", file=sys.stderr)
        return 2
    report = validate_style_packs(Path(arguments[0]))
    payload = json.dumps(report.to_dict(), ensure_ascii=False)
    sys.stdout.buffer.write((payload + "\n").encode("utf-8"))
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
