const LINK_COLUMNS = [
  ["ChatGPT Skill", "ChatGPT"],
  ["Claude Skill", "Claude"],
  ["LenAI Agent", "LenAI"],
  ["GitHub Source", "GitHub"],
];

const CATEGORY_SLUGS = {
  "Brand Voice": "brand-voice",
  "Translation": "translation",
  Presentation: "presentation",
  "Creative Production": "creative",
  "Image Generation": "image-generation",
  "Workflow Automation": "workflow",
  "Translation Quality Assurance": "qa",
  "Prompt Development": "prompt-dev",
};

const CATEGORY_LABELS = {
  "Brand Voice": "Brand voice",
  "Creative Production": "Creative",
  "Workflow Automation": "Workflow",
  "Translation Quality Assurance": "QA",
  "Prompt Development": "Prompt dev",
};

const state = { rows: [], search: "", category: "" };
const elements = {
  cards: document.querySelector("#cards"),
  search: document.querySelector("#search"),
  categoryTabs: document.querySelector("#category-tabs"),
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

  if (value || row.length) rows.push([...row, value.trim()]);
  const [headers, ...records] = rows;
  return records.map((record) => Object.fromEntries(headers.map((header, index) => [header, record[index] ?? ""])));
}

function safeUrl(value) {
  try {
    const url = new URL(value);
    return ["https:", "http:"].includes(url.protocol) ? url.href : null;
  } catch {
    return null;
  }
}

function makePill(value, active) {
  const button = document.createElement("button");
  button.className = `tab-pill${active ? " tab-pill--active" : ""}`;
  button.type = "button";
  button.dataset.value = value === "All" ? "" : value;
  button.setAttribute("aria-pressed", String(active));
  button.textContent = value === "All" ? "All" : (CATEGORY_LABELS[value] ?? value);
  button.addEventListener("click", () => {
    state.category = button.dataset.value;
    elements.categoryTabs.querySelectorAll(".tab-pill").forEach((pill) => {
      const selected = pill === button;
      pill.classList.toggle("tab-pill--active", selected);
      pill.setAttribute("aria-pressed", String(selected));
    });
    render();
  });
  return button;
}

function populateFilters(rows) {
  const categories = [...new Set(rows.map((row) => row.Category).filter(Boolean))].sort();
  elements.categoryTabs.replaceChildren(makePill("All", true), ...categories.map((value) => makePill(value, false)));
}

function createLink(url, label, name) {
  const link = document.createElement("a");
  link.className = "card__link";
  link.href = url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = label;
  link.setAttribute("aria-label", `${label}: ${name} (opens in a new tab)`);
  return link;
}

function createCard(row) {
  const article = document.createElement("article");
  article.className = "card";

  const heading = document.createElement("div");
  heading.className = "card__heading";
  const title = document.createElement("h2");
  title.textContent = row.Name;
  const category = document.createElement("span");
  category.className = `tag tag--${CATEGORY_SLUGS[row.Category] ?? "default"}`;
  category.textContent = CATEGORY_LABELS[row.Category] ?? row.Category;
  heading.append(title, category);

  const purpose = document.createElement("p");
  purpose.className = "card__purpose";
  purpose.textContent = row.Purpose;

  const audience = document.createElement("p");
  audience.className = "card__audience";
  audience.textContent = row.Audience;

  const links = document.createElement("div");
  links.className = "card__links";
  LINK_COLUMNS.forEach(([column, label]) => {
    const url = safeUrl(row[column]);
    if (url) links.append(createLink(url, label, row.Name));
  });

  article.append(heading, purpose, audience, links);
  return article;
}

function filterRows() {
  const query = state.search.toLocaleLowerCase();
  return state.rows.filter((row) => {
    const searchable = [row.Name, row.Purpose, row.Category, row.Audience, row["Available as"]]
      .join(" ")
      .toLocaleLowerCase();
    return (!query || searchable.includes(query)) && (!state.category || row.Category === state.category);
  });
}

function render() {
  const rows = filterRows();
  elements.cards.replaceChildren(...rows.map(createCard));
  elements.count.textContent = String(rows.length);
  elements.count.setAttribute("aria-label", `${rows.length} matching tools`);
  elements.empty.hidden = rows.length !== 0;
  elements.clear.hidden = !(state.search || state.category);
}

function bindControls() {
  elements.search.addEventListener("input", (event) => {
    state.search = event.target.value.trim();
    render();
  });
  elements.clear.addEventListener("click", () => {
    state.search = "";
    state.category = "";
    elements.search.value = "";
    elements.categoryTabs.querySelector('[data-value=""]').click();
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
    elements.count.textContent = "–";
    elements.error.hidden = false;
  }
}

start();
