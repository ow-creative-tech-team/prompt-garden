# Finding classification and readiness

This replaces numerical scoring. The designer-facing action group is separate from the internal severity, confidence, ownership, visibility, and readiness fields.

## Designer-facing action groups

- `Fix before delivery`: a clear error or delivery blocker.
- `Check with the content owner`: a question the designer should not resolve by guessing.
- `Recommended improvement`: an important correction that does not block delivery.
- `Optional polish`: a minor consistency or refinement point.

Show these groups as the primary report structure. Keep the classifications below in collapsed review details or machine-readable output.

## Severity

- `Critical`: demonstrably wrong protected content, legal/compliance risk, or content that cannot be read/delivered.
- `High`: a clear delivery blocker supported by deterministic evidence or reliable rendering.
- `Medium`: should be fixed before delivery but does not invalidate the deck.
- `Low`: minor polish or consistency issue.
- `Needs decision`: an alternative, placeholder, WIP item, conflict, or requester choice that cannot be resolved by proofing.

Unsupported visual judgment cannot be Critical or High when render or font fidelity is uncertain.

## Confidence

- `high`: direct XML, source/output, or unambiguous rendered evidence.
- `medium`: evidence is strong but inherited/template context is incomplete.
- `low`: candidate requiring designer confirmation.

## Ownership

- `designer_introduced`: absent from the mapped source and created in the designed output.
- `inherited_from_source`: already present in the mapped source.
- `requester_decision`: an intentional option or unresolved requester choice.
- `template_or_system`: inherited from the approved template/theme/system behavior.
- `unresolved`: ownership cannot be established.

Ownership never determines severity. An inherited error may block delivery; an off-canvas designer artifact never does.

## Visibility

- `in_frame`: intersects the slide canvas.
- `off_canvas`: does not intersect the canvas.
- `hidden`: hidden object/slide content.
- `notes`: speaker notes.
- `comment`: PowerPoint comment.

Only in-frame content affects readiness by default.

## Readiness

1. `Not ready`: a required fix or in-frame content decision remains.
2. `Ready after minor fixes`: only recommended improvements or optional polish remain.
3. `Ready`: no open findings in assessed areas.

## Coverage

Each review area is one of:

- `Assessed`: the necessary evidence was inspected.
- `Partially assessed`: some checks ran, but evidence/assets were incomplete.
- `Not assessed`: the required evidence was unavailable or outside scope.

Never convert missing coverage into a clean result.
