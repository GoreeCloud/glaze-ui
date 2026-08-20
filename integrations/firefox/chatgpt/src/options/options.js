const defaults = {
  enabled: true,
  density: "comfortable",
  translucency: true,
  expressive: true
};

const controls = {
  enabled: document.querySelector("#enabled"),
  density: document.querySelector("#density"),
  translucency: document.querySelector("#translucency"),
  expressive: document.querySelector("#expressive")
};
const status = document.querySelector("#status");

async function load() {
  const settings = await browser.storage.local.get(defaults);
  controls.enabled.checked = settings.enabled;
  controls.density.value = settings.density;
  controls.translucency.checked = settings.translucency;
  controls.expressive.checked = settings.expressive;
}

async function save() {
  await browser.storage.local.set({
    enabled: controls.enabled.checked,
    density: controls.density.value,
    translucency: controls.translucency.checked,
    expressive: controls.expressive.checked
  });
  status.textContent = "Saved locally.";
  window.setTimeout(() => {
    status.textContent = "";
  }, 1800);
}

Object.values(controls).forEach((control) => control.addEventListener("change", save));
load().catch(() => {
  status.textContent = "Settings could not be loaded.";
});
