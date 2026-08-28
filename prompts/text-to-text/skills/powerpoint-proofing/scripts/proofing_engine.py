#!/usr/bin/env python3
"""Run deterministic, findings-only PowerPoint proofing.

The engine reads presentations and emits JSON/Markdown. It never edits decks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

sys.dont_write_bytecode = True
import pptx_text  # noqa: E402


SEVERITIES = {"Critical", "High", "Medium", "Low", "Needs decision"}
CONFIDENCES = {"high", "medium", "low"}
OWNERS = {"designer_introduced", "inherited_from_source", "requester_decision", "template_or_system", "unresolved"}
VISIBILITIES = {"in_frame", "off_canvas", "hidden", "notes", "comment"}
ACTION_GROUPS = ("fix_before_delivery", "check_with_owner", "recommended_improvement", "optional_polish")
ALLOWED_FONT_PREFIXES = ("marsh serif", "noto sans", "georgia", "arial", "+mn", "+mj")
LOGO_ASSET_DIR = Path(__file__).resolve().parent.parent / "assets" / "logos"
TYPO_MAP = {"markting": "marketing"}
DECISION_RE = re.compile(r"\b(option|alternative|alt\.?|wip|work in progress|placeholder|choose|select)\b", re.I)
GUIDANCE_RE = re.compile(
    r"@DTP\b|\badd\s+icon\b|\bplease\s+(?:add|change|replace|remove|update|move|use|create|insert|beautify|check|review)\b",
    re.I,
)
REPEATED_RE = re.compile(r"\b([A-Za-z][\w'-]*)\s+\1\b", re.I)
CURRENCY_AFTER_RE = re.compile(r"\b\d[\d,.]*\s*[$€£¥]")
AMPERSAND_JOIN_RE = re.compile(r"\w&\w")


def load_rules() -> dict[str, dict[str, Any]]:
    path = Path(__file__).resolve().parent.parent / "references" / "rules.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return {rule["id"]: rule for rule in data["rules"]}


RULES = load_rules()


def stable_id(slide: int | None, object_id: str | None, rule_id: str, evidence: str) -> str:
    payload = f"{slide}|{object_id}|{rule_id}|{pptx_text.normalize_text(evidence)}"
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:8].upper()
    return f"PPT-{slide or 0:03d}-{digest}"


def finding(
    *, slide: int | None, obj: dict[str, Any] | None, rule_id: str, observed: str,
    action: str, severity: str, confidence: str, ownership: str,
    readiness_impact: bool, comparison: dict[str, Any] | None = None,
    evidence: dict[str, Any] | None = None, category: str | None = None,
) -> dict[str, Any]:
    rule = RULES.get(rule_id, RULES["VISUAL-001"])
    object_id = str(obj.get("object_id")) if obj and obj.get("object_id") is not None else None
    action_group = (
        "check_with_owner" if severity == "Needs decision"
        else "fix_before_delivery" if severity in {"Critical", "High"}
        else "recommended_improvement" if severity == "Medium"
        else "optional_polish"
    )
    result = {
        "finding_id": stable_id(slide, object_id, rule_id, observed),
        "slide_number": slide,
        "object_id": object_id,
        "object_name": obj.get("object_name") if obj else None,
        "visibility": obj.get("visibility", "in_frame") if obj else "in_frame",
        "category": category or rule["category"],
        "rule_id": rule_id,
        "rule_version": rule.get("version", "1.0"),
        "observed_evidence": observed,
        "expected_rule": rule.get("expected", "Follow the supplied proofing rule."),
        "required_action": action,
        "action_group": action_group,
        "severity": severity,
        "confidence": confidence,
        "ownership": ownership,
        "readiness_impact": bool(readiness_impact),
        "comparison": comparison,
        "evidence": evidence,
    }
    if result["visibility"] != "in_frame":
        result["readiness_impact"] = False
    return result


def source_contexts(mapping: dict[str, Any] | None, source_inventory: dict[str, Any] | None) -> list[str]:
    if not mapping or not source_inventory:
        return []
    numbers = [c["source_slide"] for c in mapping.get("source_candidates", [])]
    result = []
    for slide in source_inventory["slides"]:
        if slide["slide_number"] in numbers:
            result.append(pptx_text.visible_slide_text(slide))
    return result


def ownership_for_text(observed: str, mapping: dict[str, Any] | None, source_inventory: dict[str, Any] | None) -> tuple[str, dict[str, Any] | None]:
    if source_inventory is None:
        return "unresolved", None
    needle = pptx_text.normalize_text(observed)
    contexts = source_contexts(mapping, source_inventory)
    matched = next((text for text in contexts if needle and needle in pptx_text.normalize_text(text)), None)
    if matched is not None:
        return "inherited_from_source", {
            "source_slides": [c["source_slide"] for c in (mapping or {}).get("source_candidates", [])],
            "source_evidence": observed,
            "designed_evidence": observed,
        }
    return "designer_introduced", {
        "source_slides": [c["source_slide"] for c in (mapping or {}).get("source_candidates", [])],
        "source_evidence": None,
        "designed_evidence": observed,
    }


def paragraph_candidates(text: str) -> Iterable[tuple[str, str, str, str]]:
    """Yield rule, observed, action, severity tuples."""
    for match in REPEATED_RE.finditer(text):
        yield "COPY-002", match.group(), f"Remove the accidental repeated word “{match.group(1)}” while preserving meaning.", "Medium"
    for match in CURRENCY_AFTER_RE.finditer(text):
        yield "COPY-004", match.group(), "Place the currency symbol before the number, unless the requester confirms a local convention.", "Medium"
    for match in AMPERSAND_JOIN_RE.finditer(text):
        yield "COPY-003", match.group(), "Restore whitespace around the ampersand or confirm the intended official styling.", "Medium"
    words = re.finditer(r"\b[A-Za-z][A-Za-z'-]*\b", text)
    for match in words:
        replacement = TYPO_MAP.get(match.group().casefold())
        if replacement:
            yield "COPY-001", match.group(), f"Correct “{match.group()}” to “{replacement}”.", "High"


def mapping_by_slide(comparison: dict[str, Any] | None) -> dict[int, dict[str, Any]]:
    return {m["designed_slide"]: m for m in comparison.get("mappings", [])} if comparison else {}


def review_copy(inventory: dict[str, Any], source_inventory: dict[str, Any] | None, comparison: dict[str, Any] | None) -> list[dict[str, Any]]:
    findings = []
    mappings = mapping_by_slide(comparison)
    for slide in inventory["slides"]:
        slide_number = slide["slide_number"]
        mapping = mappings.get(slide_number)
        for obj in slide["objects"]:
            if obj.get("visibility") != "in_frame" or pptx_text.is_working_object(obj):
                continue
            for paragraph in obj.get("paragraphs", []):
                for rule_id, observed, action, severity in paragraph_candidates(paragraph["text"]):
                    owner, comp = ownership_for_text(observed, mapping, source_inventory)
                    findings.append(finding(
                        slide=slide_number, obj=obj, rule_id=rule_id, observed=observed,
                        action=action, severity=severity, confidence="high", ownership=owner,
                        readiness_impact=True, comparison=comp,
                    ))
    return findings


def review_decisions_and_geometry(inventory: dict[str, Any], comparison: dict[str, Any] | None) -> list[dict[str, Any]]:
    findings = []
    total = len(inventory["slides"])
    mappings = mapping_by_slide(comparison)
    for slide in inventory["slides"]:
        slide_number = slide["slide_number"]
        in_frame_content = [o for o in slide["objects"] if o["visibility"] == "in_frame" and (o.get("text") or o["object_type"] in {"picture", "chart", "table"})]
        for obj in slide["objects"]:
            label = obj.get("text", "")
            if obj["visibility"] == "off_canvas":
                label = " ".join(filter(None, [obj.get("object_name"), label]))
            if label and GUIDANCE_RE.search(label) and obj["visibility"] != "hidden":
                continue
            if label and DECISION_RE.search(label) and obj["visibility"] != "hidden":
                findings.append(finding(
                    slide=slide_number, obj=obj, rule_id="DECISION-001", observed=label[:240],
                    action="Confirm which option should be delivered, then remove or retain working material as directed.",
                    severity="Needs decision", confidence="high", ownership="requester_decision",
                    readiness_impact=obj["visibility"] == "in_frame",
                ))
            if obj.get("partially_clipped") and obj.get("text") and obj["visibility"] == "in_frame":
                findings.append(finding(
                    slide=slide_number, obj=obj, rule_id="LAYOUT-001",
                    observed=f"Text object intersects the slide boundary: {obj.get('text','')[:160]}",
                    action="Inspect the rendered slide and confirm the text is not unintentionally clipped.",
                    severity="Low", confidence="medium", ownership="unresolved", readiness_impact=True,
                ))
        if not in_frame_content:
            has_decorative_in_frame = any(
                o["visibility"] == "in_frame" and (
                    o["object_type"] in {"picture", "group"}
                    or (o["object_type"] == "shape" and o.get("style", {}).get("fill"))
                )
                for o in slide["objects"]
            )
            is_back_cover = slide_number == total and bool(slide.get("background") or has_decorative_in_frame)
            mapping = mappings.get(slide_number, {})
            inherited_blank = bool(mapping.get("best_source_slide") and not pptx_text.normalize_text(mapping.get("source_text", "")))
            if not is_back_cover and not inherited_blank:
                findings.append(finding(
                    slide=slide_number, obj=None, rule_id="DECISION-001",
                    observed="The slide has no in-frame text, picture, chart, or table content.",
                    action="Confirm whether the blank slide is intentional or should be removed.",
                    severity="Needs decision", confidence="high", ownership="requester_decision", readiness_impact=True,
                ))
    return findings


def iter_explicit_colors(obj: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    fill = obj.get("style", {}).get("fill")
    if fill:
        yield "fill", fill
    line = obj.get("style", {}).get("line", {}).get("color")
    if line:
        yield "line", line
    for paragraph in obj.get("paragraphs", []):
        for run in paragraph.get("runs", []):
            color = run.get("style", {}).get("text_color")
            if color:
                yield "text", color


def approved_logo_assets(asset_dir: Path = LOGO_ASSET_DIR) -> dict[str, dict[str, Any]]:
    """Return authoritative logo hashes and natural aspect ratios."""
    result = {}
    for path in sorted(asset_dir.glob("ow-logo-rgb-*.png")) if asset_dir.is_dir() else []:
        data = path.read_bytes()
        if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
            continue
        width = int.from_bytes(data[16:20], "big")
        height = int.from_bytes(data[20:24], "big")
        result[hashlib.sha256(data).hexdigest()] = {
            "variant": path.stem.removeprefix("ow-logo-rgb-"),
            "filename": path.name,
            "aspect_ratio": width / height if height else None,
        }
    return result


def review_logos(inventory: dict[str, Any], assets: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    findings = []
    for slide in inventory["slides"]:
        for obj in slide["objects"]:
            if obj.get("visibility") != "in_frame" or obj.get("object_type") != "picture":
                continue
            linked = obj.get("linked_content") or {}
            approved = assets.get(linked.get("sha256"))
            if not approved:
                continue
            geometry = obj.get("geometry") or {}
            height = geometry.get("height_in") or 0
            displayed_ratio = (geometry.get("width_in") or 0) / height if height else None
            natural_ratio = approved.get("aspect_ratio")
            if displayed_ratio and natural_ratio and abs(displayed_ratio / natural_ratio - 1) > 0.01:
                findings.append(finding(
                    slide=slide["slide_number"], obj=obj, rule_id="BRAND-003",
                    observed=(f"Approved {approved['variant']} logo is distorted: displayed aspect ratio "
                              f"{displayed_ratio:.3f}, master aspect ratio {natural_ratio:.3f}."),
                    action="Restore the approved logo's original aspect ratio without stretching or compressing it.",
                    severity="High", confidence="high", ownership="designer_introduced", readiness_impact=True,
                    evidence={"approved_asset": approved["filename"], "embedded_sha256": linked.get("sha256")},
                ))
    return findings


def review_brand(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    findings = []
    logo_assets = approved_logo_assets()
    template_colors = set(inventory.get("template_colors", {}))
    approved_colors = set(pptx_text.BRAND_COLORS_BY_HEX)
    for slide in inventory["slides"]:
        for obj in slide["objects"]:
            if obj["visibility"] != "in_frame" or pptx_text.is_working_object(obj):
                continue
            seen_fonts = set()
            for paragraph in obj.get("paragraphs", []):
                for run in paragraph.get("runs", []):
                    face = run.get("style", {}).get("font_face")
                    faces = face.values() if isinstance(face, dict) else [face]
                    for value in faces:
                        if value and value.casefold() not in seen_fonts:
                            seen_fonts.add(value.casefold())
                            if not value.casefold().startswith(ALLOWED_FONT_PREFIXES):
                                findings.append(finding(
                                    slide=slide["slide_number"], obj=obj, rule_id="BRAND-001",
                                    observed=f"Explicit font: {value}",
                                    action="Use the approved role font or confirm this is an approved template/system substitution.",
                                    severity="Medium", confidence="medium", ownership="unresolved", readiness_impact=True,
                                ))
            for role, color in iter_explicit_colors(obj):
                value = color.get("value")
                if color.get("type") != "srgb" or not value or value in approved_colors or value in template_colors:
                    continue
                findings.append(finding(
                    slide=slide["slide_number"], obj=obj, rule_id="BRAND-002",
                    observed=f"Explicit {role} color {value} is neither in the supplied palette nor traced to the theme/layout/master.",
                    action="Confirm the color against the approved template or replace it with the applicable approved token.",
                    severity="Medium", confidence="medium", ownership="unresolved", readiness_impact=True,
                ))
    return findings + review_logos(inventory, logo_assets)


def review_fidelity(comparison: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not comparison:
        return []
    findings = []
    for mapping in comparison["mappings"]:
        candidates = mapping.get("source_candidates", [])
        confidence = candidates[0]["similarity"] if candidates else 0
        slide = mapping["designed_slide"]
        if confidence >= 0.55 and mapping.get("missing_protected_tokens"):
            tokens = mapping["missing_protected_tokens"]
            findings.append(finding(
                slide=slide, obj=None, rule_id="FIDELITY-001",
                observed="Protected source token(s) not found in the mapped output: " + ", ".join(tokens[:12]),
                action="Compare the mapped source slide and restore or explicitly approve each protected-content change.",
                severity="Medium", confidence="medium", ownership="designer_introduced", readiness_impact=True,
                comparison={"source_slides": [c["source_slide"] for c in candidates], "missing": tokens, "added": mapping.get("added_protected_tokens", [])},
            ))
        drift = mapping.get("format_fidelity", {})
        if confidence >= 0.80 and drift:
            pieces = [f"{key.replace('_', ' ')}: {', '.join(values[:16])}" for key, values in drift.items()]
            findings.append(finding(
                slide=slide, obj=None, rule_id="FIDELITY-002",
                observed="Source emphasis is missing in the designed slide (" + "; ".join(pieces) + ").",
                action="Restore the mapped source bold/italic emphasis unless the requester approved the change.",
                severity="Medium", confidence="medium", ownership="designer_introduced", readiness_impact=True,
                comparison={"source_slides": [c["source_slide"] for c in candidates], "format_fidelity": drift},
            ))
    return findings


def render_for_slide(render_dir: Path | None, number: int) -> str | None:
    if not render_dir or not render_dir.exists():
        return None
    patterns = [f"slide-{number}.png", f"slide{number}.png", f"{number}.png", f"slide-{number:02d}.png", f"{number:02d}.png"]
    lower = {path.name.casefold(): path for path in render_dir.iterdir() if path.is_file()}
    for pattern in patterns:
        if pattern.casefold() in lower:
            return str(lower[pattern.casefold()].resolve())
    return None


def validate_visual_findings(path: Path | None, renders: Path | None) -> tuple[list[dict[str, Any]], list[str], list[int]]:
    if not path:
        return [], [], []
    data = json.loads(path.read_text(encoding="utf-8"))
    result, warnings = [], []
    required = {"slide_number", "visibility", "category", "rule_id", "rule_version", "observed_evidence", "expected_rule", "required_action", "severity", "confidence", "ownership", "readiness_impact", "evidence"}
    for index, raw in enumerate(data.get("findings", []), 1):
        missing = sorted(required - set(raw))
        if missing:
            raise ValueError(f"visual finding {index} missing: {', '.join(missing)}")
        if raw["severity"] not in SEVERITIES or raw["confidence"] not in CONFIDENCES or raw["ownership"] not in OWNERS or raw["visibility"] not in VISIBILITIES:
            raise ValueError(f"visual finding {index} contains an invalid enum value")
        evidence = raw.get("evidence") or {}
        has_render = bool(evidence.get("render") or render_for_slide(renders, raw["slide_number"]))
        if raw["severity"] in {"Critical", "High"} and not has_render:
            warnings.append(f"Visual finding {index} downgraded to Medium because render evidence was unavailable.")
            raw["severity"] = "Medium"
            raw["confidence"] = "low"
        obj = {"object_id": raw.get("object_id"), "object_name": raw.get("object_name"), "visibility": raw["visibility"]}
        built = finding(
            slide=raw["slide_number"], obj=obj, rule_id=raw["rule_id"], observed=raw["observed_evidence"],
            action=raw["required_action"], severity=raw["severity"], confidence=raw["confidence"], ownership=raw["ownership"],
            readiness_impact=raw["readiness_impact"], comparison=raw.get("comparison"), evidence=evidence, category=raw["category"],
        )
        built["expected_rule"] = raw["expected_rule"]
        built["rule_version"] = raw["rule_version"]
        result.append(built)
    return result, warnings, sorted({int(number) for number in data.get("slides_reviewed", [])})


def dedupe_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {}
    for item in findings:
        by_id[item["finding_id"]] = item
    order = {"fix_before_delivery": 0, "check_with_owner": 1, "recommended_improvement": 2, "optional_polish": 3}
    return sorted(by_id.values(), key=lambda f: (order[f["action_group"]], f["slide_number"] or 0, f["finding_id"]))


def readiness(findings: list[dict[str, Any]]) -> tuple[str, str]:
    active = [f for f in findings if f["readiness_impact"]]
    blockers = [f for f in active if f["severity"] in {"Critical", "High"}]
    decisions = [f for f in active if f["severity"] == "Needs decision"]
    if blockers or decisions:
        parts = []
        if blockers:
            parts.append(f"{len(blockers)} fix{'es' if len(blockers) != 1 else ''}")
        if decisions:
            parts.append(f"{len(decisions)} content decision{'s' if len(decisions) != 1 else ''}")
        return "Not ready", f"Before delivery: {' and '.join(parts)} {'are' if sum(map(len, (blockers, decisions))) != 1 else 'is'} required."
    fixes = [f for f in active if f["severity"] in {"Medium", "Low"}]
    if fixes:
        return "Ready after minor fixes", f"Review {len(fixes)} recommended improvement{'s' if len(fixes) != 1 else ''} before delivery."
    return "Ready", "No outstanding issues were found in the areas reviewed."


def coverage(source: bool, visual_complete: bool, notes: bool = False) -> list[dict[str, str]]:
    logo_assets = approved_logo_assets()
    return [
        {"area": "Deck inventory and canvas visibility", "status": "Assessed", "detail": "OOXML slide/layout/master, geometry, objects, notes/comments inventory."},
        {"area": "Copy mechanics", "status": "Assessed", "detail": "Traceable high-confidence deterministic rules."},
        {"area": "Source/output fidelity", "status": "Assessed" if source else "Not assessed", "detail": "Source deck supplied." if source else "No source deck supplied."},
        {"area": "Typography and colors", "status": "Partially assessed", "detail": "Explicit and theme/template provenance checked; inherited styles are partial."},
        {"area": "Rendered visual clarity", "status": "Assessed" if visual_complete else "Not assessed", "detail": "Every slide was declared reviewed with render evidence." if visual_complete else "A complete rendered-slide model review was not supplied."},
        {"area": "Logo identity/aspect ratio", "status": "Partially assessed" if logo_assets else "Not assessed", "detail": "Exact approved embedded logo assets and aspect-ratio distortion are checked; recreated, recolored, or raster-altered logos require visual review." if logo_assets else "Authoritative logo assets are unavailable."},
        {"area": "Chart/table component compliance", "status": "Not assessed", "detail": "Approved component examples are not supplied."},
        {"area": "Marsh Serif render fidelity", "status": "Not assessed", "detail": "Licensed files are bundled, but renderer availability/substitution must be verified by the review application."},
        {"area": "Speaker notes", "status": "Partially assessed" if notes else "Not assessed", "detail": "Excluded by default." if not notes else "Inventoried but excluded from readiness."},
    ]


def review_deck(designed: Path, source: Path | None, visual_path: Path | None, render_dir: Path | None, options: dict[str, Any]) -> dict[str, Any]:
    inventory = pptx_text.extract_inventory(designed, include_notes=options.get("include_notes", False))
    source_inventory = pptx_text.extract_inventory(source) if source else None
    comparison = pptx_text.compare_inventories(source_inventory, inventory) if source_inventory else None
    visual, warnings, slides_reviewed = validate_visual_findings(visual_path, render_dir)
    findings = dedupe_findings(
        review_copy(inventory, source_inventory, comparison)
        + review_decisions_and_geometry(inventory, comparison)
        + review_brand(inventory)
        + review_fidelity(comparison)
        + visual
    )
    state, reason = readiness(findings)
    slides = [{"slide_number": s["slide_number"], "thumbnail_path": render_for_slide(render_dir, s["slide_number"])} for s in inventory["slides"]]
    expected_slides = {s["slide_number"] for s in inventory["slides"]}
    visual_complete = bool(expected_slides and set(slides_reviewed) == expected_slides and all(s["thumbnail_path"] for s in slides))
    counts = {severity: sum(f["severity"] == severity for f in findings) for severity in ["Critical", "High", "Medium", "Low", "Needs decision"]}
    action_counts = {group: sum(f["action_group"] == group for f in findings) for group in ACTION_GROUPS}
    return {
        "schema_version": "1.1",
        "title": f"{designed.stem} — PowerPoint proofing report",
        "inputs": {"designed": str(designed), "source": str(source) if source else None},
        "assumptions": {
            "stage": options["stage"], "audience": options["audience"], "language": options["language"],
            "scope": options["scope"], "speaker_notes": "included" if options.get("include_notes") else "excluded",
            "off_canvas_readiness": "excluded", "findings_only": True,
        },
        "readiness": state,
        "readiness_reason": reason,
        "summary": {"finding_count": len(findings), "counts_by_severity": counts, "counts_by_action": action_counts},
        "coverage": coverage(bool(source), visual_complete, options.get("include_notes", False)),
        "slides": slides,
        "visual_review": {"slides_reviewed": slides_reviewed, "complete": visual_complete},
        "findings": findings,
        "comparison": comparison,
        "validation_warnings": warnings,
        "limitations": [
            "Chart and table styling was not checked against approved examples because none were supplied.",
            "The final appearance of Marsh Serif and Noto Sans must be confirmed in the review environment; font substitution can change line wrapping.",
            "Approved embedded logos and stretching are checked, but recreated, recolored, or otherwise altered logos still need visual review.",
            "Layout and other visual qualities are not assessed unless slide renders and validated visual findings are available.",
        ],
    }


def review_to_markdown(review: dict[str, Any]) -> str:
    a = review["assumptions"]
    action_labels = [
        ("fix_before_delivery", "Fix before delivery"),
        ("check_with_owner", "Check with the content owner"),
        ("recommended_improvement", "Recommended improvements"),
        ("optional_polish", "Optional polish"),
    ]
    first_slides = sorted({
        f["slide_number"] for f in review["findings"]
        if f["action_group"] in {"fix_before_delivery", "check_with_owner"} and f["readiness_impact"] and f["slide_number"] is not None
    })
    start = f" Start with slide{'s' if len(first_slides) != 1 else ''} {', '.join(map(str, first_slides))}." if first_slides else ""
    lines = [f"# {review['title']}", "", f"## {review['readiness']}", "", f"{review['readiness_reason']}{start}"]
    for group, label in action_labels:
        items = [f for f in review["findings"] if f["action_group"] == group]
        lines.extend(["", f"## {label}", ""])
        if not items:
            lines.append("- None.")
            continue
        for item in items:
            lines.extend([
                f"### Slide {item['slide_number']} — {item['category'].replace('_', ' ').title()}", "",
                f"**Found:** {item['observed_evidence']}",
                f"**Action:** {item['required_action']}",
                f"**Priority:** {label}",
                f"**Reference:** `{item['finding_id']}`", "",
            ])
    lines.append("")
    scope = str(a["scope"]).replace("_", " ").capitalize()
    notes = "included" if a["speaker_notes"] == "included" else "not included"
    lines.extend([
        "## Review context", "",
        f"- Reviewed before delivery for an internal, {'US-English' if a['language'] == 'en-US' else a['language']} presentation.",
        f"- Scope: {scope}; speaker notes were {notes}.",
    ])
    if not review.get("inputs", {}).get("source"):
        lines.append("- No source deck was supplied, so the review cannot determine where most issues originated.")
    lines.extend(["", "## Important limitations", ""] + [f"- {item}" for item in review["limitations"]])
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("designed", type=Path)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--visual-findings", type=Path)
    parser.add_argument("--renders", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--stage", default="pre_delivery")
    parser.add_argument("--audience", default="internal")
    parser.add_argument("--language", default="en-US")
    parser.add_argument("--scope", default="all slides")
    parser.add_argument("--include-notes", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    review = review_deck(args.designed, args.source, args.visual_findings, args.renders, vars(args))
    text = review_to_markdown(review) if args.format == "markdown" else json.dumps(review, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
