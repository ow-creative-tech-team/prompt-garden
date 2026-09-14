# AI tools catalogue

This static page turns every row in `catalogue.csv` into a card. It requires no
build step and can be hosted on GitHub Pages, SharePoint, or any basic web
server.

## Update the catalogue

1. Maintain the catalogue in Excel or Google Sheets.
2. Keep the existing column names unchanged.
3. Export the sheet as CSV.
4. Replace `catalogue.csv` with the new export.

Cards, filters, counts, and platform buttons update automatically. Empty link
cells are simply omitted from the corresponding card.

## Preview locally

From the repository root, serve the folder with any local web server, then open
the URL it provides. For example:

```sh
python3 -m http.server 8000 --directory catalogue
```

Then visit `http://localhost:8000`.

Opening `index.html` directly from Finder will not load the CSV because browsers
block local file requests.
