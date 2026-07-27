from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


MOBILE_SIZE = (1200, 900)
PC_SIZE = (1464, 600)
MOBILE_LABEL = "移动端"
PC_LABEL = "PC端"
ASSET_PATTERN = re.compile(
    r"^(?P<core>.+)\+(?P<index>0[1-7])_(?P<device>移动端|PC端)_(?P<size>1200x900|1464x600)\.(?P<extension>png|jpg|jpeg)$",
    re.IGNORECASE,
)


@dataclass
class ValidationReport:
    errors: list[str]
    warnings: list[str]


def parse_asset(path: Path) -> dict[str, str] | None:
    match = ASSET_PATTERN.match(path.name)
    return match.groupdict() if match else None


def validate_asset(path: Path, expected_size: tuple[int, int], expected_device: str) -> list[str]:
    parsed = parse_asset(path)
    if parsed is None:
        return [f"文件名不符合规则：{path.name}"]

    errors: list[str] = []
    if parsed["device"] != expected_device:
        errors.append(f"设备标识错误：{path.name}")
    if parsed["size"] != f"{expected_size[0]}x{expected_size[1]}":
        errors.append(f"文件名尺寸标识错误：{path.name}")
    try:
        with Image.open(path) as image:
            if image.mode != "RGB":
                errors.append(f"图片必须为 RGB：{path.name}")
            if image.size != expected_size:
                errors.append(f"尺寸必须为 {expected_size[0]}x{expected_size[1]}：{path.name}")
    except OSError:
        errors.append(f"无法读取图片：{path.name}")
    return errors


def stitch(images: list[Path], output: Path, size: tuple[int, int]) -> None:
    canvas = Image.new("RGB", (size[0], size[1] * len(images)), "white")
    for row, path in enumerate(images):
        with Image.open(path) as image:
            canvas.paste(image.convert("RGB"), (0, row * size[1]))
    canvas.save(output, quality=95)


def write_checklist_if_missing(package: Path, assets: list[Path]) -> None:
    checklist = package / "上传清单.md"
    if checklist.exists():
        return

    rows = ["# 上传清单", "", "| 序号 | 文件名 | Alt text | 原生标题 | 原生正文 | 状态 |", "|---|---|---|---|---|---|"]
    for path in assets:
        index = parse_asset(path)["index"]
        rows.append(f"| {index} | {path.name} | 待填写 | 待填写 | 待填写 | 待确认 |")
    checklist.write_text("\n".join(rows) + "\n", encoding="utf-8")


def write_report(package: Path, report: ValidationReport) -> None:
    rows = ["# 验证报告", ""]
    if report.errors:
        rows.extend(f"- {error}" for error in report.errors)
    else:
        rows.append("- 验证通过")
    if report.warnings:
        rows.extend(f"- 警告：{warning}" for warning in report.warnings)
    (package / "验证报告.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def validate_package(package: Path, phase: str, prepare: bool) -> ValidationReport:
    expected_sets = [(MOBILE_LABEL, MOBILE_SIZE, "移动端整页预览_1200x6300.jpg")]
    if phase == "final":
        expected_sets.append((PC_LABEL, PC_SIZE, "PC端整页预览_1464x4200.jpg"))

    errors: list[str] = []
    image_paths = [
        path
        for path in package.iterdir()
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"} and "+" in path.name
    ]
    parsed_assets: list[tuple[Path, dict[str, str]]] = []
    for path in image_paths:
        parsed = parse_asset(path)
        if parsed is None:
            errors.append(f"文件名不符合规则：{path.name}")
        else:
            parsed_assets.append((path, parsed))

    mobile_assets: list[Path] = []
    for device, size, preview_name in expected_sets:
        assets = [path for path, parsed in parsed_assets if parsed["device"] == device]
        if device == MOBILE_LABEL:
            mobile_assets = assets
        if len(assets) != 7:
            errors.append(f"{device}图片数量应为 7，实际为 {len(assets)}")
        core_counts: dict[str, int] = {}
        for path in assets:
            core = parse_asset(path)["core"]
            core_counts[core] = core_counts.get(core, 0) + 1
        for core, count in core_counts.items():
            if count > 1:
                errors.append(f"图片核心表达不能重复：{core}")
        ordered = sorted(assets, key=lambda path: parse_asset(path)["index"])
        device_error_count = len(errors)
        for path in ordered:
            errors.extend(validate_asset(path, size, device))
        if prepare and len(ordered) == 7 and len(errors) == device_error_count:
            stitch(ordered, package / preview_name, size)

    if phase == "final" and not (package / "A+内容.md").is_file():
        errors.append("缺少 A+内容.md")

    report = ValidationReport(errors=errors, warnings=[])
    if prepare:
        write_checklist_if_missing(package, sorted(mobile_assets, key=lambda path: parse_asset(path)["index"]))
    write_report(package, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="验证 Amazon Premium A+ 图片包")
    parser.add_argument("package", type=Path, help="A+ 输出目录")
    parser.add_argument("--phase", choices=("mobile", "final"), required=True)
    parser.add_argument("--prepare", action="store_true", help="生成预览、清单和报告")
    args = parser.parse_args()

    report = validate_package(args.package, args.phase, args.prepare)
    print("验证通过" if not report.errors else "\n".join(report.errors))
    return 0 if not report.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
