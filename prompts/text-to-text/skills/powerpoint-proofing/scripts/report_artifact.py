#!/usr/bin/env python3
"""Create self-contained HTML or optional PDF proofing reports.

The script consumes review JSON from proofing_engine.py (or legacy text) and
creates report artifacts only. It never opens or changes a presentation.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import html
import json
import sys
import textwrap
from pathlib import Path
from typing import Any


PAGE_WIDTH, PAGE_HEIGHT = 595, 842
MARGIN_X, MARGIN_Y = 50, 50
FONT_SIZE, LINE_HEIGHT, CHARS_PER_LINE = 9, 12, 96


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_input(path: Path) -> tuple[dict[str, Any] | None, str]:
    if str(path) == "-":
        text = sys.stdin.read()
    elif path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        die(f"file not found: {path}")
    try:
        data = json.loads(text)
        if isinstance(data, dict) and isinstance(data.get("findings"), list):
            return data, text
    except json.JSONDecodeError:
        pass
    return None, text


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def data_uri(path_text: str | None) -> str | None:
    if not path_text:
        return None
    path = Path(path_text)
    if not path.exists() or not path.is_file():
        return None
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(path.suffix.lower())
    if not mime:
        return None
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def option_values(findings: list[dict[str, Any]], key: str) -> str:
    values = sorted({str(item.get(key)) for item in findings if item.get(key) is not None})
    return "".join(f'<option value="{esc(value)}">{esc(value)}</option>' for value in values)


ACTION_LABELS = {
    "fix_before_delivery": "Fix before delivery",
    "check_with_owner": "Check with the content owner",
    "recommended_improvement": "Recommended improvements",
    "optional_polish": "Optional polish",
}


def action_group(item: dict[str, Any]) -> str:
    if item.get("action_group") in ACTION_LABELS:
        return item["action_group"]
    severity = item.get("severity")
    if severity == "Needs decision":
        return "check_with_owner"
    if severity in {"Critical", "High"}:
        return "fix_before_delivery"
    if severity == "Medium":
        return "recommended_improvement"
    return "optional_polish"


def plain_ownership(value: str | None) -> str:
    return {
        "designer_introduced": "Added during design",
        "inherited_from_source": "Present in the source",
        "requester_decision": "Check with the requester",
        "template_or_system": "Comes from the template or system",
        "unresolved": "Source not provided or origin unknown",
    }.get(value or "", value or "Not established")


def plain_assumption(key: str, value: Any) -> tuple[str, str] | None:
    labels = {
        "stage": "Review stage", "audience": "Audience", "language": "Language",
        "scope": "Slides reviewed", "speaker_notes": "Speaker notes",
    }
    if key not in labels:
        return None
    plain_value = {
        "pre_delivery": "Before delivery", "internal": "Internal", "all slides": "All slides",
        "excluded": "Not included", "included": "Included",
    }.get(str(value), str(value).replace("_", " ").capitalize())
    return labels[key], plain_value


def finding_card(item: dict[str, Any]) -> str:
    comparison = item.get("comparison")
    comparison_html = ""
    if comparison:
        comparison_html = f"<details><summary>Source/output comparison</summary><pre>{esc(json.dumps(comparison, indent=2, ensure_ascii=False))}</pre></details>"
    evidence = item.get("evidence")
    evidence_html = ""
    if evidence:
        evidence_html = f"<details><summary>Visual evidence</summary><pre>{esc(json.dumps(evidence, indent=2, ensure_ascii=False))}</pre></details>"
    slide = item.get("slide_number")
    group = action_group(item)
    return f"""
<article class="finding" id="{esc(item['finding_id'])}"
  data-slide="{esc(slide)}" data-action="{esc(group)}" data-category="{esc(item['category'])}">
  <header>
    <span class="pill">Slide {esc(slide)}</span>
    <span class="pill action {esc(group)}">{esc(ACTION_LABELS[group])}</span>
  </header>
  <h3>{esc(item['category'].replace('_', ' ').title())}</h3>
  <p class="action-copy">{esc(item['required_action'])}</p>
  <p class="found"><b>Found:</b> {esc(item['observed_evidence'])}</p>
  <details class="technical"><summary>Review details</summary><dl>
    <dt>Reference</dt><dd><a class="finding-id" href="#{esc(item['finding_id'])}">{esc(item['finding_id'])}</a></dd>
    <dt>Expected</dt><dd>{esc(item['expected_rule'])}</dd>
    <dt>Object</dt><dd>{esc(item.get('object_name') or 'Slide-level')} · {esc(item.get('object_id') or 'n/a')}</dd>
    <dt>Visibility</dt><dd>{esc(item['visibility'].replace('_', ' '))}</dd>
    <dt>Rule</dt><dd>{esc(item['rule_id'])} v{esc(item['rule_version'])}</dd>
    <dt>Severity</dt><dd>{esc(item['severity'])}</dd>
    <dt>Confidence</dt><dd>{esc(item['confidence'])}</dd>
    <dt>Issue origin</dt><dd>{esc(plain_ownership(item.get('ownership')))}</dd>
    <dt>Affects readiness</dt><dd>{'Yes' if item['readiness_impact'] else 'No'}</dd>
  </dl>{comparison_html}{evidence_html}</details>
</article>"""


def write_structured_html(review: dict[str, Any], out_path: Path, title: str | None) -> None:
    findings = review["findings"]
    report_title = title or review.get("title") or "PowerPoint Proofing Report"
    generated = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    assumption_pairs = [plain_assumption(key, value) for key, value in review.get("assumptions", {}).items()]
    assumptions = "".join(f'<span class="assumption"><b>{esc(label)}</b> {esc(value)}</span>' for pair in assumption_pairs if pair for label, value in [pair])
    action_counts = {group: sum(action_group(item) == group for item in findings) for group in ACTION_LABELS}
    count_cards = "".join(f'<a class="metric" href="#{esc(group)}"><span>{esc(label)}</span><strong>{esc(action_counts[group])}</strong></a>' for group, label in ACTION_LABELS.items())
    coverage_rows = "".join(f'<tr><th>{esc(item["area"])}</th><td><span class="coverage {esc(item["status"]).lower().replace(" ", "-")}">{esc(item["status"])}</span></td><td>{esc(item.get("detail"))}</td></tr>' for item in review.get("coverage", []))
    thumbnails = []
    for slide in review.get("slides", []):
        uri = data_uri(slide.get("thumbnail_path"))
        if uri:
            thumbnails.append(f'<a class="thumb-link" data-slide="{esc(slide["slide_number"])}" href="#filters"><figure><img src="{uri}" alt="Slide {slide["slide_number"]} thumbnail"><figcaption>Show findings for slide {slide["slide_number"]}</figcaption></figure></a>')
    sections = []
    for group, label in ACTION_LABELS.items():
        cards = "".join(finding_card(item) for item in findings if action_group(item) == group)
        sections.append(f'<section class="finding-section" id="{group}" data-section-action="{group}"><h2>{label}</h2><p class="empty">No findings in this section.</p><div class="cards">{cards}</div></section>')
    limitations = "".join(f"<li>{esc(item)}</li>" for item in review.get("limitations", []))
    warnings = "".join(f"<li>{esc(item)}</li>" for item in review.get("validation_warnings", []))
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(report_title)}</title>
<style>
:root{{--midnight:#000f47;--sky:#ceecff;--paper:#fff;--canvas:#f7f3ee;--ink:#19213c;--muted:#667085;--rule:#d9dce5;--red:#c53532;--gold:#cb7e03;--green:#14853d;--purple:#5e017f}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}} body{{margin:0;background:var(--canvas);color:var(--ink);font:14px/1.5 Arial,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:32px}} .hero{{background:var(--midnight);color:white;padding:32px;border-radius:2px}}
h1{{font:400 34px/1.12 Georgia,serif;margin:0 0 10px}} h2{{font:400 25px/1.2 Georgia,serif;color:var(--midnight);margin:34px 0 14px}} h3{{margin:12px 0 8px;font-size:17px}}
.meta{{opacity:.75;margin:0}} .readiness{{display:flex;gap:20px;align-items:flex-start;margin-top:26px}} .status{{background:var(--sky);color:var(--midnight);padding:8px 12px;font-weight:700;border-radius:2px;white-space:nowrap}}
.assumptions{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}} .assumption{{background:#f6f7fa;border:1px solid var(--rule);padding:7px 9px;border-radius:2px}}
.metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:18px 0}} .metric{{background:white;border:1px solid var(--rule);padding:14px;text-decoration:none;color:inherit}} .metric span{{color:var(--muted);display:block}} .metric strong{{font-size:26px;color:var(--midnight)}}
.panel{{background:white;border:1px solid var(--rule);padding:20px;margin-top:18px}} table{{width:100%;border-collapse:collapse}} th,td{{text-align:left;padding:10px;border-bottom:1px solid var(--rule);vertical-align:top}} th{{width:28%}}
.coverage{{font-weight:700}} .coverage.assessed{{color:var(--green)}} .coverage.partially-assessed{{color:var(--gold)}} .coverage.not-assessed{{color:var(--muted)}}
.filters{{position:sticky;top:0;z-index:3;display:flex;flex-wrap:wrap;gap:10px;background:#fffffff2;border:1px solid var(--rule);padding:12px;margin:24px 0;backdrop-filter:blur(8px)}} select,button{{font:inherit;border:1px solid #aab0c0;background:white;color:var(--ink);padding:8px 10px}} button{{background:var(--midnight);color:white;cursor:pointer}}
.thumbs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}} .thumb-link{{text-decoration:none;color:inherit}} figure{{margin:0;background:white;border:1px solid var(--rule);padding:8px}} .thumb-link:hover figure{{border-color:var(--midnight)}} figure img{{display:block;width:100%;height:auto}} figcaption{{padding-top:5px;color:var(--muted)}}
.cards{{display:grid;gap:12px}} .finding{{background:white;border:1px solid var(--rule);border-left:5px solid var(--midnight);padding:18px;break-inside:avoid}} .finding header{{display:flex;flex-wrap:wrap;gap:7px;align-items:center}}
.finding-id{{font-weight:700;color:var(--midnight)}} .pill{{font-size:12px;background:#eef0f5;padding:3px 7px;border-radius:999px}} .action.fix_before_delivery{{background:#f8dddd;color:#761d1b}} .action.check_with_owner{{background:#eee3f6;color:var(--purple)}} .action.recommended_improvement{{background:#fff0cf;color:#6d4700}} .action.optional_polish{{background:#e8f3ff;color:#164e7a}}
.action-copy{{font-size:17px;font-weight:700;margin:10px 0 6px}} .found{{margin:0;color:var(--muted)}} dl{{display:grid;grid-template-columns:150px 1fr;margin:10px 0 0}} dt,dd{{padding:5px 0;border-top:1px solid #eef0f3}} dt{{font-weight:700;color:var(--muted)}} dd{{margin:0}} details{{margin-top:12px}} details summary{{cursor:pointer;font-weight:700;color:var(--muted)}} pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#f6f7fa;padding:10px}}
.empty{{display:none;color:var(--muted)}} .finding-section.no-visible .empty{{display:block}} .hidden{{display:none!important}} footer{{color:var(--muted);margin-top:40px}}
@media(max-width:680px){{main{{padding:14px}}.readiness{{display:block}}dl{{grid-template-columns:1fr}}dt{{padding-bottom:0}}dd{{border-top:0}}}}
@media print{{body{{background:white}}main{{max-width:none;padding:0}}.hero{{print-color-adjust:exact}}.filters{{display:none}}.finding.hidden,.finding-section.hidden{{display:none!important}}.panel,.finding{{border-color:#bbb}}a{{color:inherit;text-decoration:none}}}}
</style></head><body><main>
<section class="hero"><h1>{esc(report_title)}</h1><p class="meta">Generated {esc(generated)} · findings-only review</p><div class="readiness"><span class="status">{esc(review.get('readiness'))}</span><p>{esc(review.get('readiness_reason'))}</p></div></section>
<section><h2>What you need to do</h2><div class="metrics">{count_cards}</div></section>
<nav class="filters" id="filters" aria-label="Finding filters">
<select id="slide"><option value="">All slides</option>{option_values(findings,'slide_number')}</select>
<select id="action"><option value="">All priorities</option>{''.join(f'<option value="{esc(group)}">{esc(label)}</option>' for group, label in ACTION_LABELS.items())}</select>
<select id="category"><option value="">All categories</option>{option_values(findings,'category')}</select>
<button type="button" id="reset">Reset filters</button><span id="visible-count" aria-live="polite"></span></nav>
{''.join(sections)}
{f'<section><h2>Slides reviewed</h2><div class="thumbs">{"".join(thumbnails)}</div></section>' if thumbnails else ''}
<section class="panel"><details><summary>What was reviewed</summary><div class="assumptions">{assumptions}</div><table><tbody>{coverage_rows}</tbody></table></details></section>
<section class="panel"><h2>Important review limitations</h2><ul>{limitations}</ul>{f'<h3>Validation warnings</h3><ul>{warnings}</ul>' if warnings else ''}</section>
<footer>Reference a stable finding ID when responding in Codex. Use the browser print command to print this report.</footer>
</main><script>
const controls=['slide','action','category'];
function applyFilters(){{let visible=0;document.querySelectorAll('.finding').forEach(card=>{{const show=controls.every(id=>!document.getElementById(id).value||card.dataset[id]===document.getElementById(id).value);card.classList.toggle('hidden',!show);if(show)visible++;}});document.querySelectorAll('.finding-section').forEach(s=>s.classList.toggle('no-visible',!s.querySelector('.finding:not(.hidden)')));document.getElementById('visible-count').textContent=visible+' finding'+(visible===1?'':'s')+' shown';}}
controls.forEach(id=>document.getElementById(id).addEventListener('change',applyFilters));document.getElementById('reset').addEventListener('click',()=>{{controls.forEach(id=>document.getElementById(id).value='');applyFilters();}});applyFilters();
document.querySelectorAll('.thumb-link').forEach(link=>link.addEventListener('click',()=>{{document.getElementById('slide').value=link.dataset.slide;applyFilters();}}));
</script></body></html>"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(document, encoding="utf-8")


def write_legacy_html(text: str, out_path: Path, title: str) -> None:
    document = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{esc(title)}</title><style>body{{font:14px/1.5 Arial;max-width:900px;margin:40px auto;padding:0 24px}}pre{{white-space:pre-wrap}}</style></head><body><h1>{esc(title)}</h1><pre>{esc(text)}</pre></body></html>"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(document, encoding="utf-8")


def review_as_text(review: dict[str, Any]) -> str:
    lines = [review.get("title", "PowerPoint Proofing Report"), f"Readiness: {review.get('readiness')} — {review.get('readiness_reason')}"]
    for group, label in ACTION_LABELS.items():
        lines.extend(["", label])
        items = [item for item in review.get("findings", []) if action_group(item) == group]
        lines.extend(f"- Slide {item['slide_number']}: {item['required_action']} ({item['finding_id']})" for item in items)
        if not items:
            lines.append("- None.")
    lines.extend(["", "What was reviewed"])
    lines.extend(f"- {item['area']}: {item['status']} — {item.get('detail','')}" for item in review.get("coverage", []))
    lines.extend(["Review limitations"] + [f"- {item}" for item in review.get("limitations", [])])
    return "\n".join(lines)


def pdf_escape(text: str) -> str:
    data = text.encode("cp1252", errors="replace")
    output = bytearray()
    for byte in data:
        if byte in (0x28, 0x29, 0x5C): output.extend((0x5C, byte))
        elif byte == 0x09: output.extend(b"    ")
        elif byte < 0x20 or byte == 0x7F: output.extend(f"\\{byte:03o}".encode("ascii"))
        else: output.append(byte)
    return output.decode("latin-1")


def wrapped_lines(text: str) -> list[str]:
    result = []
    for raw in text.splitlines():
        result.extend(textwrap.wrap(raw, width=CHARS_PER_LINE, replace_whitespace=False, drop_whitespace=False) or [""])
    return result


def build_pdf(text: str, title: str) -> bytes:
    lines = [title, ""] + wrapped_lines(text)
    per_page = (PAGE_HEIGHT - 2 * MARGIN_Y) // LINE_HEIGHT
    pages = [lines[i:i + per_page] for i in range(0, len(lines), per_page)] or [[title]]
    objects: list[bytes] = [b"<< /Type /Catalog /Pages 2 0 R >>"]
    page_numbers = [4 + i * 2 for i in range(len(pages))]
    objects.append(f"<< /Type /Pages /Kids [{' '.join(f'{n} 0 R' for n in page_numbers)}] /Count {len(pages)} >>".encode("ascii"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    for i, page in enumerate(pages):
        page_no = 4 + i * 2
        commands = ["BT", f"/F1 {FONT_SIZE} Tf", f"{LINE_HEIGHT} TL", f"{MARGIN_X} {PAGE_HEIGHT-MARGIN_Y} Td"]
        for line in page:
            commands.extend([f"({pdf_escape(line)}) Tj", "T*"])
        commands.append("ET")
        stream = ("\n".join(commands) + "\n").encode("latin-1")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] /Resources << /Font << /F1 3 0 R >> >> /Contents {page_no+1} 0 R >>".encode("ascii"))
        objects.append(f"<< /Length {len(stream)} >>\nstream\n".encode("ascii") + stream + b"endstream")
    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(output)); output.extend(f"{index} 0 obj\n".encode()); output.extend(obj); output.extend(b"\nendobj\n")
    xref = len(output); output.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]: output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return bytes(output)


def infer_format(path: Path, explicit: str | None) -> str:
    if explicit: return explicit
    if path.suffix.lower() == ".pdf": return "pdf"
    if path.suffix.lower() in {".html", ".htm"}: return "html"
    die("could not infer output format; use --format")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--title")
    parser.add_argument("--format", choices=["html", "pdf"])
    args = parser.parse_args(argv)
    review, raw = read_input(args.input)
    output_format = infer_format(args.out, args.format)
    if output_format == "html":
        write_structured_html(review, args.out, args.title) if review else write_legacy_html(raw, args.out, args.title or "PowerPoint Proofing Report")
    else:
        text = review_as_text(review) if review else raw
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_bytes(build_pdf(text, args.title or (review or {}).get("title", "PowerPoint Proofing Report")))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
