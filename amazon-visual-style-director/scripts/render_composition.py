"""Render deterministic Amazon listing composition artifacts."""

from dataclasses import dataclass
import base64
import html
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFilter, ImageFont


CANVAS_SIZE = (1500, 1500)
ALLOWED_FONT_STATUSES = {"user-provided", "open-license"}
ALLOWED_KINDS = {"text", "icon", "shape", "line", "color-block", "shadow"}


@dataclass(frozen=True)
class RenderResult:
    visual_plate: Path
    overlay: Path
    final_image: Path
    manifest: Path


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _box(layer: dict[str, Any]) -> tuple[float, float, float, float]:
    box = layer.get("box")
    if not isinstance(box, (list, tuple)) or len(box) != 4 or not all(_number(v) for v in box):
        raise ValueError("文字图层格式无效")
    x, y, width, height = box
    if x < 0 or y < 0 or width <= 0 or height <= 0 or x + width > CANVAS_SIZE[0] or y + height > CANVAS_SIZE[1]:
        raise ValueError("文字图层超出画布")
    return float(x), float(y), float(width), float(height)


def _text_fits(layer: dict[str, Any], font_path: Path) -> bool:
    x, y, width, height = _box(layer)
    font = ImageFont.truetype(font_path, size=layer["size"])
    draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    left, top, right, bottom = draw.multiline_textbbox((0, 0), layer["text"], font=font, spacing=4)
    return right - left <= width and bottom - top <= height


def _validate_layer(layer: dict[str, Any], font_path: Path) -> None:
    if not isinstance(layer, dict):
        raise ValueError("文字图层格式无效")
    kind = layer.get("kind")
    if kind not in ALLOWED_KINDS:
        raise ValueError("不支持的图层类型")
    _box(layer)
    if "opacity" in layer and (not _number(layer["opacity"]) or not 0 <= layer["opacity"] <= 1):
        raise ValueError("图形图层格式无效")
    if kind == "text":
        if not isinstance(layer.get("text"), str) or not isinstance(layer.get("size"), int) or isinstance(layer.get("size"), bool) or layer["size"] <= 0 or not isinstance(layer.get("fill"), str):
            raise ValueError("文字图层格式无效")
        if not _text_fits(layer, font_path):
            raise ValueError("文字内容超出声明框")
    elif kind in {"color-block", "shadow"}:
        if not isinstance(layer.get("fill"), str):
            raise ValueError("图形图层格式无效")
        if "opacity" in layer and (not _number(layer["opacity"]) or not 0 <= layer["opacity"] <= 1):
            raise ValueError("图形图层格式无效")
        if kind == "shadow" and (not _number(layer.get("blur", 0)) or layer.get("blur", 0) < 0):
            raise ValueError("图形图层格式无效")
    elif kind == "shape":
        if layer.get("shape", "rect") not in {"rect", "ellipse"} or not isinstance(layer.get("fill"), str) or ("opacity" in layer and (not _number(layer["opacity"]) or not 0 <= layer["opacity"] <= 1)):
            raise ValueError("图形图层格式无效")
    elif kind == "icon":
        if layer.get("icon") not in {"check", "plus", "info"} or not isinstance(layer.get("stroke"), str) or not _number(layer.get("width", 1)) or layer.get("width", 1) <= 0:
            raise ValueError("图形图层格式无效")
    elif kind == "line":
        start, end = layer.get("start"), layer.get("end")
        if not isinstance(start, (list, tuple)) or not isinstance(end, (list, tuple)) or len(start) != 2 or len(end) != 2 or not all(_number(v) for v in (*start, *end)) or not isinstance(layer.get("stroke"), str) or not _number(layer.get("width", 1)) or layer.get("width", 1) <= 0:
            raise ValueError("图形图层格式无效")


def _validate_manifest(manifest: dict[str, Any]) -> Path:
    canvas = manifest.get("canvas")
    if not isinstance(canvas, dict) or (canvas.get("width"), canvas.get("height")) != CANVAS_SIZE:
        raise ValueError("画布必须为 1500x1500")
    if not isinstance(manifest.get("style_id"), str) or not manifest["style_id"].strip():
        raise ValueError("style_id 不能为空")
    rights = manifest.get("font_rights")
    if not isinstance(rights, dict) or rights.get("status") not in ALLOWED_FONT_STATUSES:
        raise ValueError("字体许可状态不允许渲染")
    font_path = Path(str(rights.get("path", "")))
    if not font_path.is_file():
        raise ValueError("字体文件不存在")
    try:
        ImageFont.truetype(font_path, size=1)
    except (OSError, ValueError) as error:
        raise ValueError("字体文件无法加载") from error
    layers = manifest.get("layers")
    if not isinstance(layers, list):
        raise ValueError("文字图层格式无效")
    for layer in layers:
        _validate_layer(layer, font_path)
    return font_path


def _color(layer: dict[str, Any]) -> str:
    return html.escape(layer.get("fill", layer.get("stroke", "#000000")), quote=True)


def _svg_layer(layer: dict[str, Any], index: int) -> str:
    x, y, width, height = _box(layer)
    kind = layer["kind"]
    opacity = layer.get("opacity", 1)
    if kind == "text":
        lines = html.escape(layer["text"]).split("\n")
        tspans = "".join(f'<tspan x="{x}" dy="{layer["size"] if i else 0}">{line}</tspan>' for i, line in enumerate(lines))
        return f'<clipPath id="clip-{index}"><rect x="{x}" y="{y}" width="{width}" height="{height}"/></clipPath><text x="{x}" y="{y + layer["size"]}" clip-path="url(#clip-{index})" font-family="ApprovedFont" font-size="{layer["size"]}" fill="{_color(layer)}">{tspans}</text>'
    if kind == "color-block":
        return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{_color(layer)}" opacity="{opacity}"/>'
    if kind == "shadow":
        blur = layer.get("blur", 0)
        return f'<filter id="shadow-{index}"><feGaussianBlur stdDeviation="{blur}"/></filter><rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{_color(layer)}" opacity="{opacity}" filter="url(#shadow-{index})"/>'
    if kind == "shape":
        if layer.get("shape", "rect") == "ellipse":
            return f'<ellipse cx="{x + width / 2}" cy="{y + height / 2}" rx="{width / 2}" ry="{height / 2}" fill="{_color(layer)}" opacity="{opacity}"/>'
        return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{_color(layer)}" opacity="{opacity}"/>'
    if kind == "line":
        sx, sy = layer["start"]
        ex, ey = layer["end"]
        return f'<line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}" stroke="{_color(layer)}" stroke-width="{layer["width"]}" opacity="{opacity}"/>'
    stroke, stroke_width = _color(layer), layer["width"]
    if layer["icon"] == "check":
        return f'<polyline points="{x + width*.15},{y + height*.55} {x + width*.42},{y + height*.8} {x + width*.85},{y + height*.2}" fill="none" stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity}"/>'
    if layer["icon"] == "plus":
        return f'<path d="M{x + width/2} {y + height*.2} V{y + height*.8} M{x + width*.2} {y + height/2} H{x + width*.8}" stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity}"/>'
    return f'<circle cx="{x + width/2}" cy="{y + height/2}" r="{min(width, height)*.42}" fill="none" stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity}"/><line x1="{x + width/2}" y1="{y + height*.42}" x2="{x + width/2}" y2="{y + height*.62}" stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity}"/>'


def _svg_markup(layers: list[dict[str, Any]], font_path: Path) -> str:
    embedded_font = base64.b64encode(font_path.read_bytes()).decode("ascii")
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1500" viewBox="0 0 1500 1500"><style>@font-face { font-family: ApprovedFont; src: url("data:font/ttf;base64,%s"); }</style>%s</svg>' % (embedded_font, "".join(_svg_layer(layer, index) for index, layer in enumerate(layers)))


def _opacity_layer(layer: Image.Image, opacity: float) -> Image.Image:
    if opacity >= 1:
        return layer
    alpha = layer.getchannel("A").point(lambda value: round(value * opacity))
    layer.putalpha(alpha)
    return layer


def _render_with_pillow(layers: list[dict[str, Any]], font_path: Path) -> Image.Image:
    overlay = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    for layer in layers:
        x, y, width, height = _box(layer)
        kind = layer["kind"]
        color = layer.get("fill", layer.get("stroke", "#000000"))
        if kind == "text":
            text_layer = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
            ImageDraw.Draw(text_layer).multiline_text((x, y), layer["text"], font=ImageFont.truetype(font_path, size=layer["size"]), fill=color, spacing=4)
            clip = Image.new("L", CANVAS_SIZE, 0)
            ImageDraw.Draw(clip).rectangle((x, y, x + width - 1, y + height - 1), fill=255)
            text_layer.putalpha(ImageChops.multiply(text_layer.getchannel("A"), clip))
            overlay.alpha_composite(text_layer)
        elif kind == "shadow":
            shadow = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
            ImageDraw.Draw(shadow).rectangle((x, y, x + width, y + height), fill=color)
            overlay.alpha_composite(_opacity_layer(shadow, layer.get("opacity", 1)).filter(ImageFilter.GaussianBlur(layer.get("blur", 0))))
        else:
            graphic = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
            draw = ImageDraw.Draw(graphic)
            if kind in {"color-block", "shape"}:
                if kind == "shape" and layer.get("shape", "rect") == "ellipse":
                    draw.ellipse((x, y, x + width, y + height), fill=color)
                else:
                    draw.rectangle((x, y, x + width, y + height), fill=color)
            elif kind == "line":
                draw.line((*layer["start"], *layer["end"]), fill=color, width=int(layer["width"]))
            elif kind == "icon":
                stroke_width = int(layer["width"])
                if layer["icon"] == "check":
                    draw.line([(x + width*.15, y + height*.55), (x + width*.42, y + height*.8), (x + width*.85, y + height*.2)], fill=color, width=stroke_width, joint="curve")
                elif layer["icon"] == "plus":
                    draw.line((x + width/2, y + height*.2, x + width/2, y + height*.8), fill=color, width=stroke_width)
                    draw.line((x + width*.2, y + height/2, x + width*.8, y + height/2), fill=color, width=stroke_width)
                else:
                    draw.ellipse((x + width*.08, y + height*.08, x + width*.92, y + height*.92), outline=color, width=stroke_width)
                    draw.line((x + width/2, y + height*.42, x + width/2, y + height*.62), fill=color, width=stroke_width)
            overlay.alpha_composite(_opacity_layer(graphic, layer.get("opacity", 1)))
    return overlay


def render_composition(plate_path: Path, manifest: dict[str, Any], output_dir: Path) -> RenderResult:
    """Write visual-plate.png, typography-overlay.png, final-image.png, and composition.json."""
    font_path = _validate_manifest(manifest)
    with Image.open(plate_path) as source:
        if source.size != CANVAS_SIZE:
            raise ValueError("画布必须为 1500x1500")
        visual_plate = source.convert("RGBA")
    output_dir.mkdir(parents=True, exist_ok=True)
    visual_plate_path, overlay_path, final_image_path, manifest_path = (output_dir / name for name in ("visual-plate.png", "typography-overlay.png", "final-image.png", "composition.json"))
    visual_plate.save(visual_plate_path)
    layers = manifest["layers"]
    try:
        import cairosvg
    except ImportError:
        renderer = "pillow-fallback"
        overlay = _render_with_pillow(layers, font_path)
        overlay.save(overlay_path)
    else:
        svg_path = output_dir / "typography-overlay.svg"
        svg_path.write_text(_svg_markup(layers, font_path), encoding="utf-8")
        try:
            cairosvg.svg2png(url=str(svg_path), write_to=str(overlay_path), output_width=1500, output_height=1500)
            with Image.open(overlay_path) as rendered_overlay:
                overlay = rendered_overlay.convert("RGBA")
                overlay.save(overlay_path)
            renderer = "cairosvg"
        except Exception:
            renderer = "pillow-fallback"
            overlay = _render_with_pillow(layers, font_path)
            overlay.save(overlay_path)
    Image.alpha_composite(visual_plate, overlay).convert("RGB").save(final_image_path)
    composition = dict(manifest)
    composition["renderer"] = renderer
    manifest_path.write_text(json.dumps(composition, ensure_ascii=False, indent=2), encoding="utf-8")
    return RenderResult(visual_plate_path, overlay_path, final_image_path, manifest_path)