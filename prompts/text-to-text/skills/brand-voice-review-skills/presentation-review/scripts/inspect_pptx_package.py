#!/usr/bin/env python3
"""Inspect a PPTX package for review-relevant metadata.

This does not prove visual compliance. It gives signals to guide review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def read_xml(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(zf.read(name))
    except Exception:
        return None


def extract_text_from_xml(zf: zipfile.ZipFile, name: str) -> list[str]:
    root = read_xml(zf, name)
    if root is None:
        return []
    return [
        node.text.strip()
        for node in root.findall(".//a:t", NS)
        if node.text and node.text.strip()
    ]


def theme_fonts_and_colors(zf: zipfile.ZipFile) -> dict[str, object]:
    theme_names = [n for n in zf.namelist() if re.match(r"ppt/theme/theme\d+\.xml$", n)]
    fonts: Counter[str] = Counter()
    colors: Counter[str] = Counter()

    for theme in theme_names:
        root = read_xml(zf, theme)
        if root is None:
            continue
        for node in root.findall(".//*[@typeface]"):
            value = node.attrib.get("typeface")
            if value:
                fonts[value] += 1
        for node in root.findall(".//a:srgbClr", NS):
            value = node.attrib.get("val")
            if value:
                colors[f"#{value.upper()}"] += 1

    return {
        "theme_files": theme_names,
        "theme_fonts": dict(fonts.most_common()),
        "theme_colors": dict(colors.most_common()),
    }


def slide_size(zf: zipfile.ZipFile) -> dict[str, object] | None:
    root = read_xml(zf, "ppt/presentation.xml")
    if root is None:
        return None
    size = root.find(".//p:sldSz", NS)
    if size is None:
        return None
    cx = int(size.attrib.get("cx", "0"))
    cy = int(size.attrib.get("cy", "0"))
    ratio = round(cx / cy, 4) if cy else None
    return {
        "cx": cx,
        "cy": cy,
        "ratio": ratio,
        "is_16_9_likely": ratio is not None and abs(ratio - 1.7778) < 0.02,
    }


def inspect(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        slide_files = sorted(
            [n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=lambda n: int(re.search(r"slide(\d+)\.xml$", n).group(1)),
        )
        media_files = [n for n in names if n.startswith("ppt/media/")]
        master_files = [n for n in names if re.match(r"ppt/slideMasters/slideMaster\d+\.xml$", n)]
        layout_files = [n for n in names if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", n)]

        all_text: list[str] = []
        for name in slide_files:
            all_text.extend(extract_text_from_xml(zf, name))
        joined_text = "\n".join(all_text)

        brand_signals = {
            "contains_oliver_wyman": bool(re.search(r"\bOliver Wyman\b", joined_text, re.I)),
            "contains_ow": bool(re.search(r"\bOW\b", joined_text)),
            "contains_marsh": bool(re.search(r"\bMarsh\b", joined_text, re.I)),
            "contains_a_marsh_business": bool(re.search(r"A Marsh business", joined_text, re.I)),
        }

        return {
            "file": str(path),
            "slide_count": len(slide_files),
            "slide_size": slide_size(zf),
            "masters_count": len(master_files),
            "layouts_count": len(layout_files),
            "media_count": len(media_files),
            "media_extensions": dict(Counter(Path(n).suffix.lower() for n in media_files)),
            "brand_text_signals": brand_signals,
            **theme_fonts_and_colors(zf),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a PPTX package for review-relevant metadata.")
    parser.add_argument("pptx", type=Path, help="Path to a .pptx file")
    args = parser.parse_args()

    if not args.pptx.exists():
        print(f"File not found: {args.pptx}", file=sys.stderr)
        return 2
    if args.pptx.suffix.lower() != ".pptx":
        print("Expected a .pptx file", file=sys.stderr)
        return 2

    print(json.dumps(inspect(args.pptx), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
