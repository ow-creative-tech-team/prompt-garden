#!/usr/bin/env python3
"""Create portable proofing report artifacts from a text or Markdown report.

This script creates report files only. It does not read, modify, or write
PowerPoint decks.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import sys
import textwrap
from pathlib import Path


PAGE_WIDTH = 595
PAGE_HEIGHT = 842
MARGIN_X = 50
MARGIN_Y = 50
FONT_SIZE = 10
LINE_HEIGHT = 13
CHARS_PER_LINE = 92


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    if str(path) == "-":
        return sys.stdin.read()
    if not path.exists():
        die(f"file not found: {path}")
    return path.read_text(encoding="utf-8")


def write_html_report(text: str, out_path: Path, title: str) -> None:
    generated = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    body = html.escape(text)
    title_html = html.escape(title)
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title_html}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #202124;
      --muted: #5f6368;
      --rule: #dadce0;
      --paper: #ffffff;
      --bg: #f8f9fa;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.45 Arial, Helvetica, sans-serif;
    }}
    main {{
      max-width: 880px;
      margin: 32px auto;
      padding: 40px 48px;
      background: var(--paper);
      border: 1px solid var(--rule);
    }}
    h1 {{
      margin: 0 0 4px;
      font-size: 24px;
      line-height: 1.2;
    }}
    .meta {{
      margin: 0 0 24px;
      color: var(--muted);
      font-size: 12px;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      font: 13px/1.5 Arial, Helvetica, sans-serif;
    }}
    @media print {{
      body {{ background: #ffffff; }}
      main {{ margin: 0; border: 0; padding: 0; max-width: none; }}
    }}
  </style>
</head>
<body>
  <main>
    <h1>{title_html}</h1>
    <p class="meta">Generated {generated}</p>
    <pre>{body}</pre>
  </main>
</body>
</html>
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(document, encoding="utf-8")


def pdf_escape(text: str) -> str:
    data = text.encode("cp1252", errors="replace")
    escaped = bytearray()
    for byte in data:
        if byte in (0x28, 0x29, 0x5C):
            escaped.extend((0x5C, byte))
        elif byte in (0x09,):
            escaped.extend(b"    ")
        elif byte < 0x20 or byte == 0x7F:
            escaped.extend(f"\\{byte:03o}".encode("ascii"))
        else:
            escaped.append(byte)
    return escaped.decode("latin-1")


def wrapped_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        if not raw_line.strip():
            lines.append("")
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        subsequent = " " * min(indent + 2, 12)
        wrapped = textwrap.wrap(
            raw_line,
            width=CHARS_PER_LINE,
            replace_whitespace=False,
            drop_whitespace=False,
            subsequent_indent=subsequent,
        )
        lines.extend(wrapped or [""])
    return lines


def paginate(lines: list[str]) -> list[list[str]]:
    usable_height = PAGE_HEIGHT - (2 * MARGIN_Y)
    lines_per_page = max(1, usable_height // LINE_HEIGHT)
    return [lines[i : i + lines_per_page] for i in range(0, len(lines), lines_per_page)]


def content_stream(page_lines: list[str]) -> bytes:
    x = MARGIN_X
    y = PAGE_HEIGHT - MARGIN_Y
    commands = [
        "BT",
        f"/F1 {FONT_SIZE} Tf",
        f"{LINE_HEIGHT} TL",
        f"{x} {y} Td",
    ]
    for line in page_lines:
        commands.append(f"({pdf_escape(line)}) Tj")
        commands.append("T*")
    commands.append("ET")
    return ("\n".join(commands) + "\n").encode("latin-1")


def build_pdf(text: str, title: str) -> bytes:
    generated = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    all_lines = [title, f"Generated {generated}", ""] + wrapped_lines(text)
    pages = paginate(all_lines)

    objects: list[bytes] = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")

    page_object_numbers = [4 + index * 2 for index in range(len(pages))]
    kids = " ".join(f"{number} 0 R" for number in page_object_numbers)
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode("ascii"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")

    for index, page_lines in enumerate(pages):
        page_number = 4 + index * 2
        content_number = page_number + 1
        page_object = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_number} 0 R >>"
        )
        stream = content_stream(page_lines)
        content_object = (
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"endstream"
        )
        objects.append(page_object.encode("ascii"))
        objects.append(content_object)

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref_start = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(output)


def write_pdf_report(text: str, out_path: Path, title: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(build_pdf(text, title))


def infer_format(out_path: Path, explicit_format: str | None) -> str:
    if explicit_format:
        return explicit_format
    suffix = out_path.suffix.lower()
    if suffix == ".pdf":
        return "pdf"
    if suffix in {".html", ".htm"}:
        return "html"
    die("could not infer format from --out; use --format pdf or --format html")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="text/Markdown report path, or '-' for stdin")
    parser.add_argument("--out", type=Path, required=True, help="output .pdf or .html report")
    parser.add_argument("--title", default="PowerPoint Proofing Report")
    parser.add_argument("--format", choices=["pdf", "html"], help="default: infer from --out")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    report_text = read_text(args.input)
    output_format = infer_format(args.out, args.format)
    if output_format == "pdf":
        write_pdf_report(report_text, args.out, args.title)
    else:
        write_html_report(report_text, args.out, args.title)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
