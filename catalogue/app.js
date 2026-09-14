const LINK_COLUMNS = [
  ["ChatGPT Skill", "ChatGPT skill", true],
  ["Claude Skill", "Claude skill", false],
  ["LenAI Agent", "LenAI agent", false],
  ["CustomGPT", "Custom GPT", false],
  ["GitHub Source", "GitHub source", false],
];

const state = { rows: [], search: "", category: "", audience: "", platform: "" };

const elements = {
  cards: document.querySelector("#cards"),
  search: document.querySelector("#search"),
  category: document.querySelector("#category"),
  audience: document.querySelector("#audience"),
  platform: document.querySelector("#platform"),
  count: document.querySelector("#result-count"),
  clear: document.querySelector("#clear-filters"),
  empty: document.querySelector("#empty-state"),
  error: document.querySelector("#error-state"),
};

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];
    const next = text[index + 1];

    if (character === '"' && quoted && next === '"') {
      value += '"';
      index += 1;
    } else if (character === '"') {
      quoted = !quoted;
    } else if (character === "," && !quoted) {
      row.push(value.trim());
      value = "";
    } else if ((character === "\n" || character === "\r") && !quoted) {
      if (character === "\r" && next === "\n") index += 1;
      row.push(value.trim());
      if (row.some(Boolean)) rows.push(row);
      row = [];
      value = "";
    } else {
      value += character;
    }
  }

  if (value || row.length) {
    row.push(value.trim());
    rows.push(row);
  }

  const [headers, ...records] = rows;
  return records.map((record) =>
    Object.fromEntries(headers.map((header, index) => [header, record[index] ?? ""])),
  );
}

function makeOption(value) {
  const option = document.createElement("option");
  option.value = value;
  option.textContent = value;
  return option;
}

function populateFilters(rows) {
  const unique = (column) => [...new Set(rows.map((row) => row[column]).filter(Boolean))].sort();
  unique("Category").forEach((value) => elements.category.append(makeOption(value)));
  unique("Audience").forEach((value) => elements.audience.append(makeOption(value)));

  LINK_COLUMNS.forEach(([column, label]) => {
    if (rows.some((row) => row[column])) elements.platform.append(makeOption(label));
  });
}

function safeUrl(value) {
  try {
    const url = new URL(value);
    return ["https:", "http:"].includes(url.protocol) ? url.href : null;
  } catch {
    return null;
  }
}

function createCard(row) {
  const article = document.createElement("article");
  article.className = "card";

  const meta = document.createElement("div");
  meta.className = "card__meta";
  [[row.Category, "tag"], [row.Audience, "tag tag--audience"]].forEach(([text, className]) => {
    if (!text) return;
    const tag = document.createElement("span");
    tag.className = className;
    tag.textContent = text;
    meta.append(tag);
  });

  const title = document.createElement("h2");
  title.textContent = row.Name;

  const purpose = document.createElement("p");
  purpose.className = "card__purpose";
  purpose.textContent = row.Purpose;

  const links = document.createElement("div");
  links.className = "card__links";
  LINK_COLUMNS.forEach(([column, label, primary]) => {
    const url = safeUrl(row[column]);
    if (!url) return;
    const link = document.createElement("a");
    link.className = `card__link${primary ? " card__link--primary" : ""}`;
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = label;
    link.setAttribute("aria-label", `${label}: ${row.Name} (opens in a new tab)`);
    links.append(link);
  });

  article.append(meta, title, purpose, links);
  return article;
}

function filterRows() {
  const query = state.search.toLocaleLowerCase();
  return state.rows.filter((row) => {
    const searchable = [row.Name, row.Purpose, row.Category, row.Audience, row["Available as"]]
      .join(" ")
      .toLocaleLowerCase();
    const platformColumn = LINK_COLUMNS.find(([, label]) => label === state.platform)?.[0];
    return (
      (!query || searchable.includes(query)) &&
      (!state.category || row.Category === state.category) &&
      (!state.audience || row.Audience === state.audience) &&
      (!platformColumn || Boolean(row[platformColumn]))
    );
  });
}

function render() {
  const rows = filterRows();
  elements.cards.replaceChildren(...rows.map(createCard));
  elements.count.textContent = `${rows.length} ${rows.length === 1 ? "tool" : "tools"}`;
  elements.empty.hidden = rows.length !== 0;
  elements.clear.hidden = !(state.search || state.category || state.audience || state.platform);
}

function bindControls() {
  elements.search.addEventListener("input", (event) => {
    state.search = event.target.value.trim();
    render();
  });

  ["category", "audience", "platform"].forEach((key) => {
    elements[key].addEventListener("change", (event) => {
      state[key] = event.target.value;
      render();
    });
  });

  elements.clear.addEventListener("click", () => {
    state.search = "";
    state.category = "";
    state.audience = "";
    state.platform = "";
    elements.search.value = "";
    elements.category.value = "";
    elements.audience.value = "";
    elements.platform.value = "";
    render();
    elements.search.focus();
  });
}

async function start() {
  try {
    const response = await fetch("catalogue.csv");
    if (!response.ok) throw new Error(`Catalogue request failed: ${response.status}`);
    state.rows = parseCsv(await response.text());
    populateFilters(state.rows);
    bindControls();
    render();
  } catch (error) {
    console.error(error);
    elements.count.textContent = "Catalogue unavailable";
    elements.error.hidden = false;
  }
}

start();
