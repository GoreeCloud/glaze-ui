/* GLAZE UI V1.1 optical runtime controls. No telemetry or network access. */

export const GLAZE_UI_VERSION = "1.1.0";

const AURAS = new Set(["neutral", "teal", "amber", "dual"]);
const DENSITIES = new Set(["comfortable", "standard", "productive", "immersive"]);
const PERFORMANCE = new Set(["standard", "constrained"]);

function requireElement(root) {
  if (!root || typeof root.setAttribute !== "function") {
    throw new TypeError("GLAZE UI V1.1 requires an Element-like root");
  }
  return root;
}

export function setGlazeAura(root, aura = "teal") {
  requireElement(root);
  if (!AURAS.has(aura)) throw new RangeError(`Unsupported Glaze Aura: ${aura}`);
  root.setAttribute("data-glz-aura", aura);
  return aura;
}

export function setGlazeDensity(root, density = "standard") {
  requireElement(root);
  if (!DENSITIES.has(density)) throw new RangeError(`Unsupported Glaze density: ${density}`);
  root.setAttribute("data-glz-density", density);
  return density;
}

export function setGlazePerformance(root, mode = "standard") {
  requireElement(root);
  if (!PERFORMANCE.has(mode)) throw new RangeError(`Unsupported Glaze performance mode: ${mode}`);
  root.setAttribute("data-glz-performance", mode);
  return mode;
}

export function setEnvironmentalColor(root, color) {
  requireElement(root);
  if (typeof color !== "string" || color.trim() === "") {
    throw new TypeError("Environmental color must be a non-empty CSS color string");
  }
  if (globalThis.CSS?.supports && !globalThis.CSS.supports("color", color)) {
    throw new RangeError(`Unsupported CSS color: ${color}`);
  }
  root.style.setProperty("--glz1-environment-color", color);
  return color;
}

export function clearEnvironmentalColor(root) {
  requireElement(root);
  root.style.removeProperty("--glz1-environment-color");
}
