#!/usr/bin/env python3
"""Extract slide text from a PPTX package.

Uses only the Python standard library. Output is Markdown by default.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def natural_slide_key(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def extract_text(xml_bytes: bytes) -> list[str]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []
    texts: list[str] = []
    for node in root.findall(".//a:t", NS):
        if node.text and node.text.strip():
            texts.append(node.text.strip())
    return texts


def extract_deck(path: Path) -> list[dict[str, object]]:
    with zipfile.ZipFile(path) as zf:
        slide_names = sorted(
            [n for n in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=natural_slide_key,
        )
        slides: list[dict[str, object]] = []
        for slide_name in slide_names:
            number = natural_slide_key(slide_name)
            slide_text = extract_text(zf.read(slide_name))
            slides.append(
                {
                    "slide": number,
                    "text": slide_text,
                }
            )
        return slides


def print_markdown(slides: list[dict[str, object]]) -> None:
    for slide in slides:
        print(f"## Slide {slide['slide']}")
        print()
        print("### Slide text")
        text = slide["text"]
        if isinstance(text, list) and text:
            for item in text:
                print(f"- {item}")
        else:
            print("- [No extractable slide text]")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract slide text from a PPTX.")
    parser.add_argument("pptx", type=Path, help="Path to a .pptx file")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown")
    args = parser.parse_args()

    if not args.pptx.exists():
        print(f"File not found: {args.pptx}", file=sys.stderr)
        return 2
    if args.pptx.suffix.lower() != ".pptx":
        print("Expected a .pptx file", file=sys.stderr)
        return 2

    slides = extract_deck(args.pptx)
    if args.json:
        print(json.dumps(slides, indent=2, ensure_ascii=False))
    else:
        print_markdown(slides)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
