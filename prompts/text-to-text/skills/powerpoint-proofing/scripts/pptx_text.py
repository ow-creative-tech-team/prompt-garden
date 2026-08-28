#!/usr/bin/env python3
"""Create deterministic PowerPoint inventories and source/output comparisons.

The helper reads OOXML only. It never modifies a presentation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
import zipfile
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
EMU_PER_INCH = 914400
EMU_PER_POINT = 12700
SHAPE_TAGS = {"sp", "graphicFrame", "cxnSp", "pic", "grpSp"}
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
    "#2F7500": "Support Green 1000",
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
    "#D1CEC9": "Neutral (extended)",
    "#F7F3EE": "Neutral 250",
    "#14853D": "Traffic success",
    "#FFBE00": "Traffic caution",
    "#C53532": "Traffic critical",
}
REL_SLIDE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
PROTECTED_RE = re.compile(
    r"https?://\S+|(?:[$€£¥]\s*\d[\d,.]*|\d[\d,.]*\s*(?:%|bps?|x|[$€£¥]))|"
    r"\b(?:19|20)\d{2}\b|\b[A-Z][A-Z0-9&.-]{1,}\b|\[[0-9]+\]",
    re.UNICODE,
)


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalize_target(base_part: str, target: str) -> str:
    pieces: list[str] = []
    for piece in (Path(base_part).parent / target).as_posix().split("/"):
        if piece in ("", "."):
            continue
        if piece == "..":
            if pieces:
                pieces.pop()
        else:
            pieces.append(piece)
    return "/".join(pieces)


def rels_part(part: str) -> str:
    path = Path(part)
    return f"{path.parent}/_rels/{path.name}.rels"


def read_xml(zf: zipfile.ZipFile, part: str) -> ET.Element:
    try:
        return ET.fromstring(zf.read(part))
    except KeyError:
        die(f"missing part in pptx: {part}")
    except ET.ParseError as exc:
        die(f"malformed XML in {part}: {exc}")


def relationships(zf: zipfile.ZipFile, part: str) -> dict[str, dict[str, str]]:
    rel_part = rels_part(part)
    if rel_part not in zf.namelist():
        return {}
    result: dict[str, dict[str, str]] = {}
    for rel in read_xml(zf, rel_part):
        rel_id = rel.attrib.get("Id")
        if not rel_id:
            continue
        target = rel.attrib.get("Target", "")
        external = rel.attrib.get("TargetMode") == "External"
        result[rel_id] = {
            "type": rel.attrib.get("Type", ""),
            "target": target if external else normalize_target(part, target),
            "external": external,
        }
    return result


def slide_parts_in_order(zf: zipfile.ZipFile) -> list[str]:
    names = set(zf.namelist())
    if "ppt/presentation.xml" in names:
        rels = relationships(zf, "ppt/presentation.xml")
        root = read_xml(zf, "ppt/presentation.xml")
        ordered = []
        for slide_id in root.findall(".//p:sldIdLst/p:sldId", NS):
            rel_id = slide_id.attrib.get(f"{{{NS['r']}}}id")
            rel = rels.get(rel_id or "", {})
            if rel.get("type") == REL_SLIDE and rel.get("target") in names:
                ordered.append(rel["target"])
        if ordered:
            return ordered
    return sorted(
        (n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
        key=lambda n: int(re.search(r"\d+", Path(n).stem).group()),
    )


def slide_size(zf: zipfile.ZipFile) -> dict[str, Any]:
    if "ppt/presentation.xml" not in zf.namelist():
        return {"width_emu": 0, "height_emu": 0}
    elem = read_xml(zf, "ppt/presentation.xml").find("p:sldSz", NS)
    if elem is None:
        return {"width_emu": 0, "height_emu": 0}
    width = int(elem.attrib.get("cx", 0))
    height = int(elem.attrib.get("cy", 0))
    ratio = width / height if height else None
    return {
        "width_emu": width,
        "height_emu": height,
        "width_in": round(width / EMU_PER_INCH, 3),
        "height_in": round(height / EMU_PER_INCH, 3),
        "ratio": round(ratio, 5) if ratio else None,
        "is_16_9": bool(ratio and abs(ratio - 16 / 9) < 0.01),
    }


def normalize_hex(value: str) -> str:
    return "#" + value.strip().lstrip("#").upper()


def theme_colors(zf: zipfile.ZipFile) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for part in sorted(n for n in zf.namelist() if re.fullmatch(r"ppt/theme/theme\d+\.xml", n)):
        root = read_xml(zf, part)
        scheme = root.find(".//a:clrScheme", NS)
        if scheme is None:
            continue
        colors: dict[str, Any] = {}
        for child in scheme:
            rgb = child.find("a:srgbClr", NS)
            sys_color = child.find("a:sysClr", NS)
            value = (rgb.attrib.get("val") if rgb is not None else None) or (
                sys_color.attrib.get("lastClr") if sys_color is not None else None
            )
            if value:
                hex_value = normalize_hex(value)
                colors[local_name(child.tag)] = {
                    "hex": hex_value,
                    "brand_color": BRAND_COLORS_BY_HEX.get(hex_value),
                }
        result[part] = colors
    return result


def template_colors(zf: zipfile.ZipFile) -> dict[str, list[str]]:
    sources: dict[str, set[str]] = {}
    prefixes = ("ppt/theme/", "ppt/slideMasters/", "ppt/slideLayouts/")
    for part in sorted(n for n in zf.namelist() if n.endswith(".xml") and n.startswith(prefixes)):
        try:
            root = read_xml(zf, part)
        except SystemExit:
            raise
        values = {
            normalize_hex(elem.attrib["val"])
            for elem in root.iter()
            if local_name(elem.tag) == "srgbClr" and elem.attrib.get("val")
        }
        for value in values:
            sources.setdefault(value, set()).add(part)
    return {key: sorted(value) for key, value in sorted(sources.items())}


def primary_theme(themes: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return next(iter(themes.values()), {})


def color_info(parent: ET.Element | None, theme: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    if parent is None:
        return None
    solid = parent.find("a:solidFill", NS)
    if solid is None:
        return None
    rgb = solid.find("a:srgbClr", NS)
    if rgb is not None and rgb.attrib.get("val"):
        value = normalize_hex(rgb.attrib["val"])
        return {"type": "srgb", "value": value, "brand_color": BRAND_COLORS_BY_HEX.get(value)}
    scheme = solid.find("a:schemeClr", NS)
    if scheme is not None and scheme.attrib.get("val"):
        value = scheme.attrib["val"]
        result: dict[str, Any] = {"type": "scheme", "value": value}
        if value in theme:
            result["resolved"] = theme[value].get("hex")
            result["brand_color"] = theme[value].get("brand_color")
        modifiers = [{"type": local_name(e.tag), **e.attrib} for e in scheme if e.attrib]
        if modifiers:
            result["modifiers"] = modifiers
        return result
    return {"type": "solidFill", "value": None}


def line_style(sp_pr: ET.Element | None, theme: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    line = sp_pr.find("a:ln", NS) if sp_pr is not None else None
    if line is None:
        return None
    result: dict[str, Any] = {}
    if line.attrib.get("w"):
        result["width_pt"] = round(int(line.attrib["w"]) / EMU_PER_POINT, 3)
    color = color_info(line, theme)
    if color:
        result["color"] = color
    for marker in ("headEnd", "tailEnd"):
        elem = line.find(f"a:{marker}", NS)
        if elem is not None:
            result[marker] = dict(elem.attrib)
    return result or None


def shape_style(elem: ET.Element, theme: dict[str, dict[str, Any]]) -> dict[str, Any]:
    sp_pr = elem.find("p:spPr", NS)
    if sp_pr is None and local_name(elem.tag) == "pic":
        sp_pr = elem.find("p:spPr", NS)
    result: dict[str, Any] = {}
    fill = color_info(sp_pr, theme)
    if fill:
        result["fill"] = fill
    line = line_style(sp_pr, theme)
    if line:
        result["line"] = line
    if sp_pr is not None:
        for effect in ("gradFill", "effectLst", "effectDag"):
            if sp_pr.find(f"a:{effect}", NS) is not None:
                result.setdefault("effects", []).append(effect)
    return result


def run_style(rpr: ET.Element | None, theme: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if rpr is None:
        return {}
    result: dict[str, Any] = {}
    if rpr.attrib.get("sz"):
        result["font_size_pt"] = round(int(rpr.attrib["sz"]) / 100, 2)
    for attr, key in (("b", "bold"), ("i", "italic")):
        if attr in rpr.attrib:
            result[key] = rpr.attrib[attr].lower() in {"1", "true", "on"}
    if rpr.attrib.get("u"):
        result["underline"] = rpr.attrib["u"]
    faces = {}
    for tag, label in (("latin", "latin"), ("ea", "east_asian"), ("cs", "complex")):
        font = rpr.find(f"a:{tag}", NS)
        if font is not None and font.attrib.get("typeface"):
            faces[label] = font.attrib["typeface"]
    if faces:
        result["font_face"] = next(iter(faces.values())) if len(set(faces.values())) == 1 else faces
    color = color_info(rpr, theme)
    if color:
        result["text_color"] = color
    return result


def xfrm_for(elem: ET.Element) -> ET.Element | None:
    kind = local_name(elem.tag)
    if kind == "graphicFrame":
        return elem.find("p:xfrm", NS)
    if kind == "grpSp":
        return elem.find("p:grpSpPr/a:xfrm", NS)
    return elem.find("p:spPr/a:xfrm", NS)


def xfrm_numbers(xfrm: ET.Element | None) -> dict[str, int]:
    if xfrm is None:
        return {}
    result = {}
    for tag, prefix in (("off", ""), ("ext", ""), ("chOff", "ch_"), ("chExt", "ch_")):
        elem = xfrm.find(f"a:{tag}", NS)
        if elem is None:
            continue
        if "x" in elem.attrib:
            result[prefix + "x"] = int(elem.attrib["x"])
        if "y" in elem.attrib:
            result[prefix + "y"] = int(elem.attrib["y"])
        if "cx" in elem.attrib:
            result[prefix + "cx"] = int(elem.attrib["cx"])
        if "cy" in elem.attrib:
            result[prefix + "cy"] = int(elem.attrib["cy"])
    if xfrm.attrib.get("rot"):
        result["rotation_deg"] = int(xfrm.attrib["rot"]) / 60000
    return result


def apply_transform(value: dict[str, int], transform: tuple[float, float, float, float]) -> dict[str, Any] | None:
    if not {"x", "y", "cx", "cy"}.issubset(value):
        return None
    sx, sy, tx, ty = transform
    left = tx + sx * value["x"]
    top = ty + sy * value["y"]
    width = abs(sx * value["cx"])
    height = abs(sy * value["cy"])
    return {
        "left_emu": round(left), "top_emu": round(top), "width_emu": round(width), "height_emu": round(height),
        "left_in": round(left / EMU_PER_INCH, 3), "top_in": round(top / EMU_PER_INCH, 3),
        "width_in": round(width / EMU_PER_INCH, 3), "height_in": round(height / EMU_PER_INCH, 3),
        "rotation_deg": value.get("rotation_deg", 0),
    }


def group_transform(value: dict[str, int], parent: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    psx, psy, ptx, pty = parent
    if not {"x", "y", "cx", "cy", "ch_x", "ch_y", "ch_cx", "ch_cy"}.issubset(value):
        return parent
    sx = value["cx"] / value["ch_cx"] if value["ch_cx"] else 1.0
    sy = value["cy"] / value["ch_cy"] if value["ch_cy"] else 1.0
    return (
        psx * sx,
        psy * sy,
        ptx + psx * (value["x"] - value["ch_x"] * sx),
        pty + psy * (value["y"] - value["ch_y"] * sy),
    )


def visibility(geometry: dict[str, Any] | None, size: dict[str, Any], hidden: bool) -> tuple[str, bool]:
    if hidden:
        return "hidden", False
    if not geometry or not size.get("width_emu") or not size.get("height_emu"):
        return "in_frame", False
    left, top = geometry["left_emu"], geometry["top_emu"]
    right = left + geometry["width_emu"]
    bottom = top + geometry["height_emu"]
    intersects = right > 0 and bottom > 0 and left < size["width_emu"] and top < size["height_emu"]
    clipped = intersects and (left < 0 or top < 0 or right > size["width_emu"] or bottom > size["height_emu"])
    return ("in_frame" if intersects else "off_canvas"), clipped


def paragraph_runs(paragraph: ET.Element, theme: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    default_rpr = paragraph.find("a:pPr/a:defRPr", NS)
    for child in paragraph:
        tag = local_name(child.tag)
        if tag in {"r", "fld"}:
            rpr = child.find("a:rPr", NS)
            if rpr is None:
                rpr = default_rpr
            text = "".join((t.text or "") for t in child.findall(".//a:t", NS))
            if text:
                result.append({"text": text, "style": run_style(rpr, theme)})
        elif tag == "br":
            rpr = child.find("a:rPr", NS)
            if rpr is None:
                rpr = default_rpr
            result.append({"text": "\n", "break": True, "style": run_style(rpr, theme)})
        elif tag == "tab":
            result.append({"text": "\t", "break": True, "style": {}})
    return result


def object_paragraphs(elem: ET.Element, theme: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for index, paragraph in enumerate(elem.findall(".//a:p", NS)):
        runs = paragraph_runs(paragraph, theme)
        text = "".join(run["text"] for run in runs)
        if text:
            result.append({"paragraph_index": index, "text": text, "runs": runs})
    return result


def object_name_id(elem: ET.Element) -> tuple[str | None, str | None, bool]:
    c_nv_pr = elem.find(".//p:cNvPr", NS)
    if c_nv_pr is None:
        return None, None, False
    hidden = c_nv_pr.attrib.get("hidden", "0").lower() in {"1", "true", "on"}
    return c_nv_pr.attrib.get("name"), c_nv_pr.attrib.get("id"), hidden


def object_kind(elem: ET.Element) -> str:
    kind = local_name(elem.tag)
    if kind == "graphicFrame":
        if elem.find(".//a:tbl", NS) is not None:
            return "table"
        if any(local_name(e.tag) == "chart" for e in elem.iter()):
            return "chart"
        if any(local_name(e.tag) in {"relIds", "dataModelExt"} for e in elem.iter()):
            return "diagram"
        return "graphic_frame"
    return {"sp": "shape", "cxnSp": "connector", "pic": "picture", "grpSp": "group"}.get(kind, kind)


def placeholder_info(elem: ET.Element) -> dict[str, Any] | None:
    ph = elem.find(".//p:nvPr/p:ph", NS)
    return dict(ph.attrib) if ph is not None else None


def linked_content(elem: ET.Element, rels: dict[str, dict[str, str]], zf: zipfile.ZipFile) -> dict[str, Any] | None:
    for node in elem.iter():
        rel_id = node.attrib.get(f"{{{NS['r']}}}embed") or node.attrib.get(f"{{{NS['r']}}}id")
        if not rel_id or rel_id not in rels:
            continue
        rel = rels[rel_id]
        info: dict[str, Any] = {"relationship_id": rel_id, **rel}
        target = rel.get("target")
        if target in zf.namelist() and not target.endswith(".xml"):
            data = zf.read(target)
            info["sha256"] = hashlib.sha256(data).hexdigest()
            info["bytes"] = len(data)
            info["extension"] = Path(target).suffix.lower()
        return info
    return None


def iter_objects(
    tree: ET.Element,
    size: dict[str, Any],
    theme: dict[str, dict[str, Any]],
    rels: dict[str, dict[str, str]],
    zf: zipfile.ZipFile,
    transform: tuple[float, float, float, float] = (1.0, 1.0, 0.0, 0.0),
    group_path: tuple[str, ...] = (),
) -> Iterable[dict[str, Any]]:
    z_order = 0
    for elem in list(tree):
        tag = local_name(elem.tag)
        if tag not in SHAPE_TAGS:
            continue
        z_order += 1
        name, object_id, hidden = object_name_id(elem)
        values = xfrm_numbers(xfrm_for(elem))
        geometry = apply_transform(values, transform)
        state, clipped = visibility(geometry, size, hidden)
        info: dict[str, Any] = {
            "object_id": object_id,
            "object_name": name,
            "object_type": object_kind(elem),
            "z_order": z_order,
            "group_path": list(group_path),
            "visibility": state,
            "partially_clipped": clipped,
            "geometry": geometry,
            "placeholder": placeholder_info(elem),
            "paragraphs": object_paragraphs(elem, theme) if tag != "grpSp" else [],
            "style": shape_style(elem, theme) if tag != "grpSp" else {},
        }
        text = "\n".join(p["text"] for p in info["paragraphs"])
        if text:
            info["text"] = text
        link = linked_content(elem, rels, zf)
        if link:
            info["linked_content"] = link
        if info["object_type"] == "connector":
            info["line_applicability"] = "connector"
        elif info["style"].get("line"):
            info["line_applicability"] = f"{info['object_type']}_border"
        yield info
        if tag == "grpSp":
            child_transform = group_transform(values, transform)
            child_path = group_path + ((object_id or name or f"group-{z_order}"),)
            yield from iter_objects(elem, size, theme, rels, zf, child_transform, child_path)


def direct_background(root: ET.Element, theme: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    bg = root.find("p:cSld/p:bg", NS)
    if bg is None:
        return None
    fill = color_info(bg.find("p:bgPr", NS), theme)
    if fill:
        return fill
    bg_ref = bg.find("p:bgRef", NS)
    if bg_ref is not None:
        result = color_info(bg_ref, theme) or {"type": "bgRef"}
        result.update(bg_ref.attrib)
        return result
    return None


def inheritance_for_slide(zf: zipfile.ZipFile, slide_part: str) -> dict[str, Any]:
    slide_rels = relationships(zf, slide_part)
    layout = next((r["target"] for r in slide_rels.values() if r["type"].endswith("/slideLayout")), None)
    layout_rels = relationships(zf, layout) if layout else {}
    master = next((r["target"] for r in layout_rels.values() if r["type"].endswith("/slideMaster")), None)
    return {"layout_part": layout, "master_part": master}


def resolved_background(zf: zipfile.ZipFile, slide_part: str, inheritance: dict[str, Any], theme: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [(slide_part, "slide"), (inheritance.get("layout_part"), "layout"), (inheritance.get("master_part"), "master")]
    for part, provenance in candidates:
        if part and part in zf.namelist():
            bg = direct_background(read_xml(zf, part), theme)
            if bg:
                return {**bg, "provenance": provenance, "part": part}
    return None


def comments_for_slide(zf: zipfile.ZipFile, slide_part: str, slide_number: int) -> list[dict[str, Any]]:
    result = []
    for rel in relationships(zf, slide_part).values():
        if "comment" not in rel["type"].lower() or rel.get("target") not in zf.namelist():
            continue
        part = rel["target"]
        root = read_xml(zf, part)
        texts = [t.text.strip() for t in root.iter() if t.text and t.text.strip()]
        if texts:
            result.append({"slide_number": slide_number, "part": part, "visibility": "comment", "text": " ".join(texts)})
    return result


def notes_for_slide(zf: zipfile.ZipFile, slide_part: str, slide_number: int, theme: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    for rel in relationships(zf, slide_part).values():
        if rel["type"].endswith("/notesSlide") and rel.get("target") in zf.namelist():
            root = read_xml(zf, rel["target"])
            paragraphs = []
            for p in root.findall(".//a:p", NS):
                runs = paragraph_runs(p, theme)
                text = "".join(r["text"] for r in runs)
                if text:
                    paragraphs.append({"text": text, "runs": runs})
            return [{"slide_number": slide_number, "part": rel["target"], "visibility": "notes", "paragraphs": paragraphs}]
    return []


def parse_slide_spec(spec: str | None) -> set[int] | None:
    if not spec:
        return None
    result: set[int] = set()
    for item in spec.split(","):
        if "-" in item:
            start, end = map(int, item.split("-", 1))
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return result


def extract_inventory(pptx_path: Path, include_notes: bool = False, selected_slides: set[int] | None = None, include_style: bool = True) -> dict[str, Any]:
    if not pptx_path.exists():
        die(f"file not found: {pptx_path}")
    try:
        zf = zipfile.ZipFile(pptx_path)
    except zipfile.BadZipFile:
        die(f"not a valid pptx package: {pptx_path}")
    with zf:
        size = slide_size(zf)
        themes = theme_colors(zf)
        theme = primary_theme(themes)
        slides = []
        comments = []
        notes = []
        for number, part in enumerate(slide_parts_in_order(zf), 1):
            if selected_slides and number not in selected_slides:
                continue
            root = read_xml(zf, part)
            inheritance = inheritance_for_slide(zf, part)
            tree = root.find("p:cSld/p:spTree", NS)
            if tree is None:
                tree = root
            objects = list(iter_objects(tree, size, theme, relationships(zf, part), zf))
            slide_hidden = root.attrib.get("show", "1").lower() in {"0", "false", "off"}
            if slide_hidden:
                for obj in objects:
                    obj["visibility"] = "hidden"
            slide = {
                "slide_number": number,
                "part": part,
                "hidden": slide_hidden,
                "inheritance": inheritance,
                "background": resolved_background(zf, part, inheritance, theme),
                "objects": objects,
            }
            slides.append(slide)
            comments.extend(comments_for_slide(zf, part, number))
            if include_notes:
                notes.extend(notes_for_slide(zf, part, number, theme))
        return {
            "schema_version": "2.0",
            "source": str(pptx_path),
            "deck_sha256": hashlib.sha256(pptx_path.read_bytes()).hexdigest(),
            "assessed_scope": {"slides": sorted(selected_slides) if selected_slides else "all", "speaker_notes": include_notes},
            "slide_size": size,
            "theme_colors": themes if include_style else {},
            "template_colors": template_colors(zf) if include_style else {},
            "slides": slides,
            "notes": notes,
            "comments": comments,
            "resolution": {
                "slide_order": "resolved", "layout_master_relationships": "resolved", "theme_colors": "resolved",
                "geometry": "resolved_best_effort", "group_transforms": "resolved_best_effort",
                "inherited_text_styles": "partial", "comments": "inventory_only", "speaker_notes": "included" if include_notes else "excluded",
            },
        }


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    return " ".join(text.split())


def is_working_object(obj: dict[str, Any]) -> bool:
    label = " ".join(filter(None, [obj.get("object_name"), obj.get("text")]))
    return bool(
        re.search(r"\bsticky\s*note\b|\boption\s*\d+\b|\bwork in progress\b|\bwip\b", label, re.I)
        or re.match(r"\s*20\d{2}-\d{2}-\d{2}\s+\d{2}:\d{2}", obj.get("text", ""))
        or re.search(r"@DTP\b", label, re.I)
    )


def visible_slide_text(slide: dict[str, Any]) -> str:
    return "\n".join(
        obj.get("text", "") for obj in slide["objects"]
        if obj.get("visibility") == "in_frame" and obj.get("text") and not is_working_object(obj)
    )


def emphasized_tokens(slide: dict[str, Any], key: str) -> set[str]:
    result: set[str] = set()
    for obj in slide["objects"]:
        if obj.get("visibility") != "in_frame" or is_working_object(obj):
            continue
        for paragraph in obj.get("paragraphs", []):
            word_runs = [run for run in paragraph.get("runs", []) if re.search(r"\w", run.get("text", ""))]
            states = {bool(run.get("style", {}).get(key)) for run in word_runs}
            # Mixed emphasis is deliberate run-level evidence. Whole-paragraph
            # emphasis is commonly a layout role and is not compared here.
            if states != {False, True}:
                continue
            for run in paragraph.get("runs", []):
                if run.get("style", {}).get(key):
                    result.update(re.findall(r"\w+", normalize_text(run["text"])))
    return result


def similarity(left: str, right: str) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    seq = SequenceMatcher(None, left, right).ratio()
    a, b = set(left.split()), set(right.split())
    jaccard = len(a & b) / len(a | b) if a | b else 0
    return round(0.65 * seq + 0.35 * jaccard, 5)


def protected_tokens(text: str) -> list[str]:
    return [unicodedata.normalize("NFKC", m.group()).strip() for m in PROTECTED_RE.finditer(text)]


def protected_tokens_for_slide(slide: dict[str, Any], slide_height_in: float | None) -> list[str]:
    """Exclude likely footer metadata while protecting delivered slide content."""
    tokens: list[str] = []
    footer_top = (slide_height_in or 0) - 0.65
    for obj in slide["objects"]:
        if obj.get("visibility") != "in_frame" or not obj.get("text") or is_working_object(obj):
            continue
        top = (obj.get("geometry") or {}).get("top_in")
        if top is not None and slide_height_in and top >= footer_top:
            continue
        tokens.extend(protected_tokens(obj["text"]))
    return tokens


def compare_inventories(source: dict[str, Any], designed: dict[str, Any]) -> dict[str, Any]:
    source_text = {s["slide_number"]: visible_slide_text(s) for s in source["slides"]}
    designed_text = {s["slide_number"]: visible_slide_text(s) for s in designed["slides"]}
    mappings = []
    for out_slide in designed["slides"]:
        out_num = out_slide["slide_number"]
        out_norm = normalize_text(designed_text[out_num])
        scores = sorted(
            ((s["slide_number"], similarity(out_norm, normalize_text(source_text[s["slide_number"]]))) for s in source["slides"]),
            key=lambda item: (-item[1], item[0]),
        )
        best = scores[0][1] if scores else 0
        candidates = [{"source_slide": n, "similarity": score} for n, score in scores if score >= max(0.16, best - 0.08)][:4]
        if not candidates and out_num in source_text:
            candidates = [{"source_slide": out_num, "similarity": scores[[n for n, _ in scores].index(out_num)][1]}]
        best_source = candidates[0]["source_slide"] if candidates else None
        source_raw = source_text.get(best_source, "")
        src_slide_obj = next((s for s in source["slides"] if s["slide_number"] == best_source), None)
        missing = list((Counter(protected_tokens_for_slide(src_slide_obj, source.get("slide_size", {}).get("height_in"))) - Counter(protected_tokens_for_slide(out_slide, designed.get("slide_size", {}).get("height_in")))).elements()) if src_slide_obj else []
        added = list((Counter(protected_tokens_for_slide(out_slide, designed.get("slide_size", {}).get("height_in"))) - Counter(protected_tokens_for_slide(src_slide_obj, source.get("slide_size", {}).get("height_in")))).elements()) if src_slide_obj else []
        emphasis = {}
        if best_source is not None:
            src_slide = src_slide_obj
            common_words = set(normalize_text(source_raw).split()) & set(out_norm.split())
            for key in ("bold", "italic"):
                lost = sorted((emphasized_tokens(src_slide, key) & common_words) - emphasized_tokens(out_slide, key))
                if lost:
                    emphasis[f"missing_{key}_tokens"] = lost
        mappings.append({
            "designed_slide": out_num,
            "source_candidates": candidates,
            "best_source_slide": best_source,
            "source_text": source_raw,
            "designed_text": designed_text[out_num],
            "missing_protected_tokens": missing,
            "added_protected_tokens": added,
            "format_fidelity": emphasis,
        })
    return {
        "schema_version": "1.0",
        "source": source["source"],
        "designed": designed["source"],
        "normalization": "Unicode NFKC, casefold, whitespace collapse",
        "mappings": mappings,
    }


def compare_decks(source_path: Path, designed_path: Path) -> dict[str, Any]:
    return compare_inventories(extract_inventory(source_path), extract_inventory(designed_path))


def inventory_to_markdown(inventory: dict[str, Any]) -> str:
    size = inventory["slide_size"]
    lines = [f"# {Path(inventory['source']).name}", "", f"- Slides: {len(inventory['slides'])}", f"- Size: {size.get('width_in')} × {size.get('height_in')} in", ""]
    for slide in inventory["slides"]:
        lines.extend([f"## Slide {slide['slide_number']}", ""])
        lines.append(f"- Layout: {slide['inheritance'].get('layout_part') or 'unresolved'}")
        lines.append(f"- Master: {slide['inheritance'].get('master_part') or 'unresolved'}")
        for obj in slide["objects"]:
            label = obj.get("object_name") or obj.get("object_id") or "unnamed"
            text = obj.get("text", "").replace("\n", " ⏎ ")
            lines.append(f"- [{obj['visibility']}] {obj['object_type']} `{label}`: {text}".rstrip())
        lines.append("")
    return "\n".join(lines)


def write_output(data: Any, out: Path | None, output_format: str = "json") -> None:
    text = inventory_to_markdown(data) if output_format == "markdown" else json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    extract = commands.add_parser("extract", help="create a normalized deck inventory")
    extract.add_argument("input", type=Path)
    extract.add_argument("--out", type=Path)
    extract.add_argument("--format", choices=["json", "markdown"], default="json")
    extract.add_argument("--slides")
    extract.add_argument("--include-notes", action="store_true")
    extract.add_argument("--include-style", action="store_true", help="retained for compatibility; style inspection is on by default")
    extract.add_argument("--no-style", action="store_true")
    compare = commands.add_parser("compare", help="compare a source and designed deck")
    compare.add_argument("source", type=Path)
    compare.add_argument("designed", type=Path)
    compare.add_argument("--out", type=Path)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.command == "extract":
        inventory = extract_inventory(args.input, args.include_notes, parse_slide_spec(args.slides), not args.no_style)
        write_output(inventory, args.out, args.format)
    else:
        write_output(compare_decks(args.source, args.designed), args.out)


if __name__ == "__main__":
    main()
