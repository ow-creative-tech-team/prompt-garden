# Internal installation

This skill contains Oliver Wyman brand materials and approved logo assets. It is for authorized internal use only and must not be published or redistributed externally.

Install the extracted `powerpoint-proofing` folder in the Codex skills directory for the intended user or managed workspace. Preserve the folder name and its internal structure:

```text
powerpoint-proofing/
├── SKILL.md
├── agents/
├── assets/
├── references/
└── scripts/
```

Restart or refresh Codex after installation, then invoke the skill with:

```text
Use $powerpoint-proofing to proof this PowerPoint.
```

The distributed package intentionally excludes the source repository's tests, development fixtures, application code, and input-materials directory.
