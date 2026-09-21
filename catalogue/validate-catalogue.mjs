import fs from "node:fs";

const file = new URL("./catalogue.csv", import.meta.url);
const requiredHeaders = [
  "Prompt ID", "Name", "Purpose", "Category", "Audience", "Available as",
  "ChatGPT Skill", "Claude Skill", "LenAI Agent", "GitHub Source", "Usage Example",
];
const linkHeaders = ["ChatGPT Skill", "Claude Skill", "LenAI Agent", "GitHub Source"];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];
    const next = text[index + 1];
    if (character === '"' && quoted && next === '"') { value += '"'; index += 1; }
    else if (character === '"') quoted = !quoted;
    else if (character === "," && !quoted) { row.push(value.trim()); value = ""; }
    else if ((character === "\n" || character === "\r") && !quoted) {
      if (character === "\r" && next === "\n") index += 1;
      row.push(value.trim());
      if (row.some(Boolean)) rows.push(row);
      row = []; value = "";
    } else value += character;
  }
  if (value || row.length) rows.push([...row, value.trim()]);
  const [headers, ...records] = rows;
  return { headers, records: records.map((record) => Object.fromEntries(headers.map((header, index) => [header, record[index] ?? ""]))) };
}

const { headers, records } = parseCsv(fs.readFileSync(file, "utf8"));
const errors = [];
for (const header of requiredHeaders) if (!headers.includes(header)) errors.push(`Missing required header: ${header}`);
if (errors.length) throw new Error(errors.join("\n"));

const ids = new Set();
for (const [index, row] of records.entries()) {
  const rowNumber = index + 2;
  for (const header of ["Prompt ID", "Name", "Purpose", "Category", "Audience", "Available as"]) {
    if (!row[header].trim()) errors.push(`Row ${rowNumber}: ${header} is required.`);
  }
  if (ids.has(row["Prompt ID"])) errors.push(`Row ${rowNumber}: duplicate Prompt ID '${row["Prompt ID"]}'.`);
  ids.add(row["Prompt ID"]);
  const links = linkHeaders.filter((header) => row[header].trim());
  if (!links.length) errors.push(`Row ${rowNumber}: provide at least one platform or GitHub link.`);
  for (const header of links) {
    try {
      const url = new URL(row[header]);
      if (!['http:', 'https:'].includes(url.protocol)) throw new Error("unsupported protocol");
    } catch { errors.push(`Row ${rowNumber}: ${header} must be an http(s) URL.`); }
  }
}
if (errors.length) throw new Error(`Catalogue validation failed:\n${errors.join("\n")}`);
console.log(`Catalogue valid: ${records.length} unique tools.`);
