const DEFAULTS = {
  enabled: true,
  density: "comfortable",
  translucency: true,
  expression: true,
};

const controls = {
  enabled: document.querySelector("#enabled"),
  density: document.querySelector("#density"),
  translucency: document.querySelector("#translucency"),
  expression: document.querySelector("#expression"),
  status: document.querySelector("#status"),
  openOptions: document.querySelector("#open-options"),
};

function showStatus(message) {
  controls.status.textContent = message;
  window.setTimeout(() => {
    if (controls.status.textContent === message) controls.status.textContent = "";
  }, 1400);
}

async function load() {
  const values = await browser.storage.local.get(DEFAULTS);
  controls.enabled.checked = values.enabled;
  controls.density.value = values.density;
  controls.translucency.checked = values.translucency;
  controls.expression.checked = values.expression;
}

async function save() {
  await browser.storage.local.set({
    enabled: controls.enabled.checked,
    density: controls.density.value,
    translucency: controls.translucency.checked,
    expression: controls.expression.checked,
  });
  showStatus("Saved locally");
}

for (const control of [controls.enabled, controls.density, controls.translucency, controls.expression]) {
  control.addEventListener("change", save);
}

controls.openOptions.addEventListener("click", () => browser.runtime.openOptionsPage());
load();
