#!/usr/bin/env python3
"""Extract text and style metadata from PowerPoint .pptx files.

This helper intentionally works at the OOXML text-node level. It is meant for
findings-only proofing of existing decks, not for editing, generating, or
redesigning slides.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

REL_SLIDE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
REL_NOTES = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide"
A_T = f"{{{NS['a']}}}t"
A_P = f"{{{NS['a']}}}p"
A_R = f"{{{NS['a']}}}r"
A_FLD = f"{{{NS['a']}}}fld"
A_RPR = f"{{{NS['a']}}}rPr"
A_LATIN = f"{{{NS['a']}}}latin"
A_EA = f"{{{NS['a']}}}ea"
A_CS = f"{{{NS['a']}}}cs"
A_SOLID_FILL = f"{{{NS['a']}}}solidFill"
A_SRGB_CLR = f"{{{NS['a']}}}srgbClr"
A_SCHEME_CLR = f"{{{NS['a']}}}schemeClr"
A_LN = f"{{{NS['a']}}}ln"
P_CNVPR = f"{{{NS['p']}}}cNvPr"
P_SPPR = f"{{{NS['p']}}}spPr"
P_BG = f"{{{NS['p']}}}bg"
P_BGPR = f"{{{NS['p']}}}bgPr"
P_BGREF = f"{{{NS['p']}}}bgRef"
SHAPE_TAGS = {"sp", "graphicFrame", "cxnSp", "pic"}

BRAND_COLORS_BY_HEX = {
    "#000F47": "Midnight Blue 1000",
    "#CEECFF": "Sky Blue 250",
    "#FFFFFF": "White",
    "#CB7E03": "Gold 1000",
    "#FFBF00": "Gold 750",
    "#FFD98A": "Gold 500",
    "#FFF3DA": "Gold 250",
    "#0B4BFF": "Active Blue 750",
    "#82BAFF": "Blue 500",
    "#2F7500": "Green 1000 / Success green",
    "#6ABF30": "Green 750",
    "#B0DC92": "Green 500",
    "#DFECD7": "Green 250",
    "#5E017F": "Purple 1000",
    "#8F20DE": "Purple 750",
    "#DEB1FF": "Purple 500",
    "#F5E8FF": "Purple 250",
    "#3D3C37": "Neutral 1000",
    "#7B7974": "Neutral 750",
    "#B9B6B1": "Neutral 500",
    "#F7F3EE": "Neutral 250",
    "#C53532": "Danger crimson",
    "#FFBE00": "Warning yellow",
}

for prefix, uri in NS.items():
    if prefix != "rel":
        ET.register_namespace(prefix, uri)


@dataclass(frozen=True)
class PartInfo:
    slide_number: int | None
    kind: str
    part: str
    label: str


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_slide_spec(spec: str | None) -> set[int] | None:
    if not spec:
        return None
    selected: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            start_s, end_s = chunk.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start > end:
                die(f"invalid slide range: {chunk}")
            selected.update(range(start, end + 1))
        else:
            selected.add(int(chunk))
    return selected


def numeric_key(path: str) -> tuple[int, str]:
    match = re.search(r"(\d+)(?=\.xml$)", path)
    return (int(match.group(1)) if match else 10**9, path)


def normalize_target(base_part: str, target: str) -> str:
    base_dir = Path(base_part).parent
    combined = base_dir / target
    pieces: list[str] = []
    for piece in combined.as_posix().split("/"):
        if piece in ("", "."):
            continue
        if piece == "..":
            if pieces:
                pieces.pop()
            continue
        pieces.append(piece)
    return "/".join(pieces)


def read_xml(zf: zipfile.ZipFile, part: str) -> ET.Element:
    try:
        data = zf.read(part)
    except KeyError:
        die(f"missing part in pptx: {part}")
    return ET.fromstring(data)


def slide_parts_in_order(zf: zipfile.ZipFile) -> list[str]:
    names = set(zf.namelist())
    if "ppt/presentation.xml" in names and "ppt/_rels/presentation.xml.rels" in names:
        pres = read_xml(zf, "ppt/presentation.xml")
        rels = read_xml(zf, "ppt/_rels/presentation.xml.rels")
        rel_targets: dict[str, str] = {}
        for rel in rels.findall("rel:Relationship", NS):
            if rel.attrib.get("Type") == REL_SLIDE:
                rel_id = rel.attrib.get("Id")
                target = rel.attrib.get("Target")
                if rel_id and target:
                    rel_targets[rel_id] = normalize_target("ppt/presentation.xml", target)
        ordered: list[str] = []
        for slide_id in pres.findall(".//p:sldIdLst/p:sldId", NS):
            rel_id = slide_id.attrib.get(f"{{{NS['r']}}}id")
            target = rel_targets.get(rel_id or "")
            if target in names:
                ordered.append(target)
        if ordered:
            return ordered
    return sorted(
        [name for name in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)],
        key=numeric_key,
    )


def notes_part_for_slide(zf: zipfile.ZipFile, slide_part: str) -> str | None:
    rel_part = f"{Path(slide_part).parent}/_rels/{Path(slide_part).name}.rels"
    if rel_part not in zf.namelist():
        return None
    rels = read_xml(zf, rel_part)
    for rel in rels.findall("rel:Relationship", NS):
        if rel.attrib.get("Type") == REL_NOTES:
            target = rel.attrib.get("Target")
            if target:
                normalized = normalize_target(slide_part, target)
                if normalized in zf.namelist():
                    return normalized
    return None


def text_nodes(root: ET.Element) -> list[ET.Element]:
    return list(root.iter(A_T))


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.iter(A_T))


def attr_bool(value: str) -> bool:
    return value.lower() in {"1", "true", "on"}


def hundredths_to_points(value: str) -> float | None:
    try:
        return round(int(value) / 100, 2)
    except ValueError:
        return None


def emu_to_points(value: str) -> float | None:
    try:
        return round(int(value) / 12700, 2)
    except ValueError:
        return None


def normalize_hex(value: str) -> str:
    return f"#{value.strip().lstrip('#').upper()}"


def annotate_brand_color(info: dict[str, Any], hex_value: str) -> None:
    brand_name = BRAND_COLORS_BY_HEX.get(normalize_hex(hex_value))
    if brand_name:
        info["brand_color"] = brand_name


def theme_colors(zf: zipfile.ZipFile) -> dict[str, dict[str, str]]:
    theme_parts = sorted(
        name for name in zf.namelist() if re.fullmatch(r"ppt/theme/theme\d+\.xml", name)
    )
    if not theme_parts:
        return {}
    root = read_xml(zf, theme_parts[0])
    colors: dict[str, dict[str, str]] = {}
    for clr_scheme in root.findall(".//a:clrScheme", NS):
        for child in list(clr_scheme):
            key = child.tag.rsplit("}", 1)[-1]
            srgb = child.find(A_SRGB_CLR)
            sys_clr = child.find(f"{{{NS['a']}}}sysClr")
            hex_value = None
            if srgb is not None and srgb.attrib.get("val"):
                hex_value = normalize_hex(srgb.attrib["val"])
            elif sys_clr is not None and sys_clr.attrib.get("lastClr"):
                hex_value = normalize_hex(sys_clr.attrib["lastClr"])
            if hex_value:
                info = {"hex": hex_value}
                brand_name = BRAND_COLORS_BY_HEX.get(hex_value)
                if brand_name:
                    info["brand_color"] = brand_name
                colors[key] = info
        break
    return colors


def color_info(
    parent: ET.Element | None, theme_color_map: dict[str, dict[str, str]] | None = None
) -> dict[str, Any] | None:
    if parent is None:
        return None
    solid_fill = parent.find(A_SOLID_FILL)
    if solid_fill is None:
        return None
    srgb = solid_fill.find(A_SRGB_CLR)
    if srgb is not None and srgb.attrib.get("val"):
        hex_value = normalize_hex(srgb.attrib["val"])
        info: dict[str, Any] = {"type": "srgb", "value": hex_value}
        annotate_brand_color(info, hex_value)
        return info
    scheme = solid_fill.find(A_SCHEME_CLR)
    if scheme is not None and scheme.attrib.get("val"):
        modifiers = [
            {"type": child.tag.rsplit("}", 1)[-1], **child.attrib}
            for child in list(scheme)
            if child.attrib
        ]
        scheme_value = scheme.attrib["val"]
        info = {"type": "scheme", "value": scheme_value}
        if theme_color_map and scheme_value in theme_color_map:
            theme_info = dict(theme_color_map[scheme_value])
            info["theme_color"] = theme_info
            if not modifiers and theme_info.get("hex"):
                info["resolved"] = theme_info["hex"]
                annotate_brand_color(info, theme_info["hex"])
        if modifiers:
            info["modifiers"] = modifiers
        return info
    return {"type": "solidFill"}


def run_style(
    rpr: ET.Element | None, theme_color_map: dict[str, dict[str, str]] | None = None
) -> dict[str, Any]:
    if rpr is None:
        return {}
    style: dict[str, Any] = {}
    if rpr.attrib.get("sz"):
        size = hundredths_to_points(rpr.attrib["sz"])
        if size is not None:
            style["font_size_pt"] = size
    if rpr.attrib.get("b") is not None:
        style["bold"] = attr_bool(rpr.attrib["b"])
    if rpr.attrib.get("i") is not None:
        style["italic"] = attr_bool(rpr.attrib["i"])
    if rpr.attrib.get("u"):
        style["underline"] = rpr.attrib["u"]
    fonts: dict[str, str] = {}
    for label, tag in (("latin", A_LATIN), ("east_asian", A_EA), ("complex", A_CS)):
        font = rpr.find(tag)
        if font is not None and font.attrib.get("typeface"):
            fonts[label] = font.attrib["typeface"]
    if fonts:
        unique_fonts = set(fonts.values())
        if len(unique_fonts) == 1:
            style["font_face"] = next(iter(unique_fonts))
        else:
            style["font_faces"] = fonts
    text_color = color_info(rpr, theme_color_map)
    if text_color:
        style["text_color"] = text_color
    return style


def line_style(
    sp_pr: ET.Element | None, theme_color_map: dict[str, dict[str, str]] | None = None
) -> dict[str, Any] | None:
    if sp_pr is None:
        return None
    line = sp_pr.find(A_LN)
    if line is None:
        return None
    style: dict[str, Any] = {}
    if line.attrib.get("w"):
        width = emu_to_points(line.attrib["w"])
        if width is not None:
            style["width_pt"] = width
    line_color = color_info(line, theme_color_map)
    if line_color:
        style["color"] = line_color
    for marker in ("headEnd", "tailEnd"):
        marker_elem = line.find(f"{{{NS['a']}}}{marker}")
        if marker_elem is not None and marker_elem.attrib:
            style[marker] = marker_elem.attrib
    return style or None


def shape_style(
    elem: ET.Element, theme_color_map: dict[str, dict[str, str]] | None = None
) -> dict[str, Any]:
    sp_pr = elem.find(P_SPPR)
    style: dict[str, Any] = {}
    fill = color_info(sp_pr, theme_color_map)
    if fill:
        style["fill"] = fill
    line = line_style(sp_pr, theme_color_map)
    if line:
        style["line"] = line
    return style


def slide_background_style(
    root: ET.Element, theme_color_map: dict[str, dict[str, str]] | None = None
) -> dict[str, Any] | None:
    bg = root.find(f".//{P_BG}")
    if bg is None:
        return None
    bg_pr = bg.find(P_BGPR)
    fill = color_info(bg_pr, theme_color_map)
    if fill:
        return fill
    bg_ref = bg.find(P_BGREF)
    if bg_ref is not None:
        ref_fill = color_info(bg_ref, theme_color_map)
        if ref_fill:
            if bg_ref.attrib.get("idx"):
                ref_fill["background_ref_idx"] = bg_ref.attrib["idx"]
            return ref_fill
        if bg_ref.attrib:
            return {"type": "bgRef", **bg_ref.attrib}
    return None


def nearest_shape_info(
    elem: ET.Element,
    include_style: bool = False,
    theme_color_map: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any] | None:
    c_nv_pr = elem.find(f".//{P_CNVPR}")
    if c_nv_pr is None:
        return None
    info: dict[str, Any] = {}
    if c_nv_pr.attrib.get("name"):
        info["name"] = c_nv_pr.attrib["name"]
    if c_nv_pr.attrib.get("id"):
        info["id"] = c_nv_pr.attrib["id"]
    if include_style:
        style = shape_style(elem, theme_color_map)
        if style:
            info["style"] = style
    return info or None


def shape_text(elem: ET.Element) -> str:
    return " ".join(
        " ".join(node.text.split()) for node in elem.iter(A_T) if node.text
    ).strip()


def collect_shape_inventory(
    root: ET.Element,
    theme_color_map: dict[str, dict[str, str]] | None = None,
) -> list[dict[str, Any]]:
    shapes: list[dict[str, Any]] = []
    for elem in root.iter():
        tag = elem.tag.rsplit("}", 1)[-1]
        if tag not in SHAPE_TAGS:
            continue
        info = nearest_shape_info(
            elem, include_style=True, theme_color_map=theme_color_map
        )
        if not info:
            continue
        info["kind"] = tag
        text = shape_text(elem)
        if text:
            info["text"] = text[:160]
        if info.get("style"):
            shapes.append(info)
    return shapes


def iter_paragraphs_with_shape(
    elem: ET.Element,
    shape: dict[str, Any] | None = None,
    include_style: bool = False,
    theme_color_map: dict[str, dict[str, str]] | None = None,
) -> Iterable[tuple[ET.Element, dict[str, Any] | None]]:
    next_shape = shape
    tag = elem.tag.rsplit("}", 1)[-1]
    if tag in SHAPE_TAGS:
        next_shape = (
            nearest_shape_info(
                elem, include_style=include_style, theme_color_map=theme_color_map
            )
            or shape
        )
    if elem.tag == A_P:
        yield elem, next_shape
    for child in list(elem):
        yield from iter_paragraphs_with_shape(
            child, next_shape, include_style, theme_color_map
        )


def iter_text_runs(
    paragraph: ET.Element,
    node_indexes: dict[int, int],
    include_style: bool,
    theme_color_map: dict[str, dict[str, str]] | None = None,
) -> Iterable[dict[str, Any]]:
    for child in list(paragraph):
        if child.tag in {A_R, A_FLD}:
            rpr = child.find(A_RPR)
            for node in child.iter(A_T):
                run: dict[str, Any] = {
                    "text_index": node_indexes[id(node)],
                    "text": node.text or "",
                }
                if include_style:
                    style = run_style(rpr, theme_color_map)
                    if style:
                        run["style"] = style
                yield run
        else:
            for node in child.iter(A_T):
                yield {
                    "text_index": node_indexes[id(node)],
                    "text": node.text or "",
                }


def slide_size(zf: zipfile.ZipFile) -> dict[str, Any] | None:
    if "ppt/presentation.xml" not in zf.namelist():
        return None
    pres = read_xml(zf, "ppt/presentation.xml")
    sld_sz = pres.find("p:sldSz", NS)
    if sld_sz is None:
        return None
    try:
        width_emu = int(sld_sz.attrib["cx"])
        height_emu = int(sld_sz.attrib["cy"])
    except (KeyError, ValueError):
        return None
    width_in = round(width_emu / 914400, 2)
    height_in = round(height_emu / 914400, 2)
    ratio = round(width_in / height_in, 4) if height_in else None
    return {
        "width_in": width_in,
        "height_in": height_in,
        "ratio": ratio,
        "is_16_9": ratio is not None and abs(ratio - (16 / 9)) < 0.01,
    }


def inventory_part(
    part_info: PartInfo,
    root: ET.Element,
    include_style: bool = False,
    theme_color_map: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    nodes = text_nodes(root)
    node_indexes = {id(node): index for index, node in enumerate(nodes)}
    paragraphs: list[dict[str, Any]] = []
    background = (
        slide_background_style(root, theme_color_map) if include_style else None
    )
    shapes = collect_shape_inventory(root, theme_color_map) if include_style else []
    for paragraph_index, (paragraph, shape) in enumerate(
        iter_paragraphs_with_shape(
            root, include_style=include_style, theme_color_map=theme_color_map
        )
    ):
        runs = []
        for run in iter_text_runs(
            paragraph, node_indexes, include_style, theme_color_map
        ):
            runs.append(run)
        text = "".join(run["text"] for run in runs)
        if text:
            paragraphs.append(
                {
                    "paragraph_index": paragraph_index,
                    "paragraph_id": f"p{paragraph_index}",
                    "shape": shape,
                    "text": text,
                    "runs": runs,
                }
            )
    item = {
        "slide_number": part_info.slide_number,
        "kind": part_info.kind,
        "part": part_info.part,
        "label": part_info.label,
        "text_nodes": [
            {"text_index": index, "text": node.text or ""}
            for index, node in enumerate(nodes)
            if node.text
        ],
        "paragraphs": paragraphs,
    }
    if background:
        item["background"] = background
    if shapes:
        item["shapes"] = shapes
    return item


def collect_parts(
    zf: zipfile.ZipFile, include_notes: bool, selected_slides: set[int] | None
) -> list[PartInfo]:
    parts: list[PartInfo] = []
    for slide_number, slide_part in enumerate(slide_parts_in_order(zf), start=1):
        if selected_slides is not None and slide_number not in selected_slides:
            continue
        parts.append(
            PartInfo(
                slide_number=slide_number,
                kind="slide",
                part=slide_part,
                label=f"Slide {slide_number}",
            )
        )
        if include_notes:
            notes_part = notes_part_for_slide(zf, slide_part)
            if notes_part:
                parts.append(
                    PartInfo(
                        slide_number=slide_number,
                        kind="notes",
                        part=notes_part,
                        label=f"Slide {slide_number} notes",
                    )
                )
    return parts


def extract_inventory(
    pptx_path: Path,
    include_notes: bool,
    selected_slides: set[int] | None,
    include_style: bool,
) -> dict[str, Any]:
    if not pptx_path.exists():
        die(f"file not found: {pptx_path}")
    with zipfile.ZipFile(pptx_path) as zf:
        parts = collect_parts(zf, include_notes, selected_slides)
        theme_color_map = theme_colors(zf) if include_style else {}
        items = [
            inventory_part(
                part,
                read_xml(zf, part.part),
                include_style=include_style,
                theme_color_map=theme_color_map,
            )
            for part in parts
        ]
        size = slide_size(zf)
    return {
        "source": str(pptx_path),
        "include_notes": include_notes,
        "include_style": include_style,
        "slides_filter": sorted(selected_slides) if selected_slides else None,
        "slide_size": size,
        "theme_colors": theme_color_map if include_style else {},
        "items": items,
    }


def style_label(value: Any) -> str:
    if isinstance(value, dict):
        if value.get("type") and value.get("value"):
            brand = f" ({value['brand_color']})" if value.get("brand_color") else ""
            resolved = f" -> {value['resolved']}" if value.get("resolved") else ""
            suffix = ""
            if value.get("modifiers"):
                suffix = f" {value['modifiers']}"
            return f"{value['type']}:{value['value']}{resolved}{brand}{suffix}"
        return json.dumps(value, sort_keys=True)
    return str(value)


def unique_labels(values: Iterable[Any]) -> list[str]:
    labels = sorted({style_label(value) for value in values if value is not None})
    return labels


def paragraph_style_summary(paragraph: dict[str, Any]) -> str:
    runs = paragraph.get("runs") or []
    run_styles = [run.get("style") or {} for run in runs]
    pieces: list[str] = []
    for key, label in (
        ("font_face", "font"),
        ("font_size_pt", "size"),
        ("text_color", "text color"),
    ):
        values = unique_labels(style.get(key) for style in run_styles)
        if values:
            pieces.append(f"{label}={', '.join(values)}")
    bold_values = unique_labels(style.get("bold") for style in run_styles if "bold" in style)
    if bold_values:
        pieces.append(f"bold={', '.join(bold_values)}")
    shape = paragraph.get("shape") or {}
    shape_style_info = shape.get("style") or {}
    if shape_style_info.get("fill"):
        pieces.append(f"shape fill={style_label(shape_style_info['fill'])}")
    if shape_style_info.get("line"):
        line = shape_style_info["line"]
        line_bits = []
        if line.get("width_pt") is not None:
            line_bits.append(f"{line['width_pt']} pt")
        if line.get("color"):
            line_bits.append(style_label(line["color"]))
        if line.get("headEnd"):
            line_bits.append(f"headEnd={line['headEnd']}")
        if line.get("tailEnd"):
            line_bits.append(f"tailEnd={line['tailEnd']}")
        if line_bits:
            pieces.append(f"line={' / '.join(line_bits)}")
    return "; ".join(pieces)


def shape_style_summary(shape: dict[str, Any]) -> str:
    style = shape.get("style") or {}
    pieces: list[str] = []
    if style.get("fill"):
        pieces.append(f"fill={style_label(style['fill'])}")
    if style.get("line"):
        line = style["line"]
        line_bits = []
        if line.get("width_pt") is not None:
            line_bits.append(f"{line['width_pt']} pt")
        if line.get("color"):
            line_bits.append(style_label(line["color"]))
        if line.get("headEnd"):
            line_bits.append(f"headEnd={line['headEnd']}")
        if line.get("tailEnd"):
            line_bits.append(f"tailEnd={line['tailEnd']}")
        if line_bits:
            pieces.append(f"line={' / '.join(line_bits)}")
    return "; ".join(pieces)


def inventory_to_markdown(inventory: dict[str, Any]) -> str:
    lines = [f"# {Path(inventory['source']).name}", ""]
    if inventory.get("slide_size"):
        size = inventory["slide_size"]
        lines.extend(
            [
                "## Deck setup",
                "",
                (
                    f"- Slide size: {size['width_in']} x {size['height_in']} in; "
                    f"ratio {size['ratio']}; 16:9={size['is_16_9']}"
                ),
                "",
            ]
        )
    if inventory.get("theme_colors"):
        colors = ", ".join(
            f"{key}={value['hex']}"
            + (f" ({value['brand_color']})" if value.get("brand_color") else "")
            for key, value in sorted(inventory["theme_colors"].items())
        )
        lines.extend(["- Theme colors: " + colors, ""])
    current_label: str | None = None
    for item in inventory["items"]:
        if item["label"] != current_label:
            lines.extend([f"## {item['label']}", ""])
            current_label = item["label"]
        if item.get("background"):
            lines.append(f"- Slide background: {style_label(item['background'])}")
        shape_lines = []
        for shape in item.get("shapes") or []:
            summary = shape_style_summary(shape)
            if not summary:
                continue
            name = shape.get("name") or "unnamed shape"
            text = f"; text={shape['text']}" if shape.get("text") else ""
            shape_lines.append(f"- Shape `{name}` ({shape.get('kind')}): {summary}{text}")
        if shape_lines:
            lines.append("- Shape/style inventory:")
            lines.extend(f"  {line}" for line in shape_lines)
        if item.get("background") or shape_lines:
            lines.append("")
        if not item["paragraphs"]:
            lines.extend(["(No text found.)", ""])
            continue
        for paragraph in item["paragraphs"]:
            shape = paragraph.get("shape") or {}
            shape_label = shape.get("name") or "unnamed shape"
            line = (
                f"- `{item['part']}#{paragraph['paragraph_id']}` "
                f"({shape_label}): {paragraph['text']}"
            )
            style_summary = paragraph_style_summary(paragraph)
            if style_summary:
                line += f" [{style_summary}]"
            lines.append(line)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_json(data: Any, out_path: Path | None) -> None:
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if out_path:
        out_path.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def command_extract(args: argparse.Namespace) -> None:
    selected_slides = parse_slide_spec(args.slides)
    inventory = extract_inventory(
        args.input, args.include_notes, selected_slides, args.include_style
    )
    if args.format == "json":
        write_json(inventory, args.out)
    else:
        text = inventory_to_markdown(inventory)
        if args.out:
            args.out.write_text(text, encoding="utf-8")
        else:
            print(text, end="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract = subparsers.add_parser("extract", help="extract text inventory")
    extract.add_argument("input", type=Path, help="input .pptx file")
    extract.add_argument("--out", type=Path, help="output file; defaults to stdout")
    extract.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="json",
        help="output format; default: json",
    )
    extract.add_argument(
        "--slides",
        help="slide numbers to include, such as 1,3-5; defaults to all slides",
    )
    extract.add_argument(
        "--include-notes",
        action="store_true",
        help="include speaker notes linked to selected slides",
    )
    extract.add_argument(
        "--include-style",
        action="store_true",
        help="include explicit text and shape style metadata for brand checks",
    )
    extract.set_defaults(func=command_extract)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
