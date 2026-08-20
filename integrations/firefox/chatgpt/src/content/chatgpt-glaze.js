(() => {
  const root = document.documentElement;
  const defaults = {
    enabled: true,
    density: "comfortable",
    translucency: true,
    expressive: true
  };

  function apply(settings) {
    const state = { ...defaults, ...settings };
    root.dataset.goreecloudGlazeUi = state.enabled ? "enabled" : "disabled";
    root.dataset.goreecloudGlazeDensity = state.density;
    root.dataset.goreecloudGlazeTranslucency = state.translucency ? "on" : "off";
    root.dataset.goreecloudGlazeExpression = state.expressive ? "on" : "off";
  }

  function readPreferences() {
    if (!globalThis.browser?.storage?.local) {
      apply(defaults);
      return;
    }

    browser.storage.local.get(defaults).then(apply, () => apply(defaults));
  }

  readPreferences();

  if (globalThis.browser?.storage?.onChanged) {
    browser.storage.onChanged.addListener((changes, areaName) => {
      if (areaName !== "local") return;
      browser.storage.local.get(defaults).then(apply, () => apply(defaults));
    });
  }
})();
