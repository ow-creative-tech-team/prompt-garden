# Prompt & Skill Catalogue

This dependency-free static site turns each row in `catalogue.csv` into a searchable card. It is deployed from the `feature/ai-tools-catalogue` branch and is intended for authenticated internal users only.

## Update the catalogue

1. Maintain the approved inventory in the team spreadsheet.
2. Export it as CSV, keeping these headers exactly: `Prompt ID`, `Name`, `Purpose`, `Category`, `Audience`, `Available as`, `ChatGPT Skill`, `Claude Skill`, `LenAI Agent`, `GitHub Source`, and `Usage Example`.
3. Replace `catalogue/catalogue.csv` with the export.
4. Run `node catalogue/validate-catalogue.mjs` from the repository root.
5. Preview the site locally, review the changes, then commit and push to `feature/ai-tools-catalogue`.

The deployment workflow validates the CSV before publishing. Do not share the Pages URL until repository administrators have restricted GitHub Pages to authenticated organization or enterprise users; the catalogue includes internal LenAI links.

## Preview locally

From the repository root, run:

```sh
python3 -m http.server 8000 --directory catalogue
```

Then visit `http://localhost:8000`.
