/* Glaze UI 2.0 Candidate interaction runtime.
 * No telemetry, networking, storage, or remote dependencies.
 */

const ROOT = document.documentElement;
const VALID_CLARITY = new Set(["clear", "balanced", "solid"]);
const VALID_EXPRESSION = new Set(["calm", "balanced", "expressive"]);
const VALID_APPEARANCE = new Set(["light", "dark", "deep-dark"]);

function setEnumAttribute(name, value, allowed) {
  if (!allowed.has(value)) throw new TypeError(`Invalid ${name}: ${value}`);
  ROOT.dataset[name] = value;
}

function interactionPoint(event, element) {
  const rect = element.getBoundingClientRect();
  const x = rect.width ? ((event.clientX - rect.left) / rect.width) * 100 : 50;
  const y = rect.height ? ((event.clientY - rect.top) / rect.height) * 100 : 50;
  return {
    x: Math.max(0, Math.min(100, x)),
    y: Math.max(0, Math.min(100, y)),
  };
}

function setLive(element, live) {
  if (!(element instanceof HTMLElement)) return;
  element.dataset.glazeLive = String(Boolean(live));
}

function bindLiveSurface(element) {
  if (!(element instanceof HTMLElement) || element.dataset.glazeBound === "true") return;
  element.dataset.glazeBound = "true";

  element.addEventListener("pointerdown", (event) => {
    const point = interactionPoint(event, element);
    element.style.setProperty("--glaze-highlight-x", `${point.x.toFixed(2)}%`);
    element.style.setProperty("--glaze-highlight-y", `${point.y.toFixed(2)}%`);
    setLive(element, true);
    if (element.setPointerCapture) {
      try { element.setPointerCapture(event.pointerId); } catch { /* non-capturable target */ }
    }
  });

  const clearPointer = () => setLive(element, false);
  element.addEventListener("pointerup", clearPointer);
  element.addEventListener("pointercancel", clearPointer);
  element.addEventListener("lostpointercapture", clearPointer);
  element.addEventListener("focusin", () => setLive(element, true));
  element.addEventListener("focusout", () => setLive(element, false));
}

function bindAll(root = document) {
  root.querySelectorAll("[data-glaze-interactive], .glaze-button, .glaze-material-live").forEach(bindLiveSurface);
}

function setNavigationScrollState(capsule, direction) {
  if (!(capsule instanceof HTMLElement)) throw new TypeError("Navigation Capsule element is required");
  if (!new Set(["forward", "reverse", "idle"]).has(direction)) throw new TypeError(`Invalid scroll direction: ${direction}`);
  if (direction === "idle") delete capsule.dataset.scroll;
  else capsule.dataset.scroll = direction;
}

async function connectedTransform({ source, target, mutate, name = "glaze-connected" }) {
  if (!(source instanceof HTMLElement)) throw new TypeError("Connected Transformation source is required");
  if (target != null && !(target instanceof HTMLElement)) throw new TypeError("Connected Transformation target must be an HTMLElement");
  if (typeof mutate !== "function") throw new TypeError("Connected Transformation mutate callback is required");

  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const transitionName = `${name}-${Math.random().toString(36).slice(2)}`;
  source.style.setProperty("--glaze-connected-name", transitionName);
  if (target) target.style.setProperty("--glaze-connected-name", transitionName);

  const applyMutation = () => {
    mutate();
    if (target) target.hidden = false;
  };

  if (!reducedMotion && typeof document.startViewTransition === "function") {
    const transition = document.startViewTransition(applyMutation);
    try { await transition.finished; } finally {
      source.style.removeProperty("--glaze-connected-name");
      if (target) target.style.removeProperty("--glaze-connected-name");
    }
    return;
  }

  applyMutation();
  source.style.removeProperty("--glaze-connected-name");
  if (target) target.style.removeProperty("--glaze-connected-name");
}

function observeNewInteractiveSurfaces() {
  const observer = new MutationObserver((records) => {
    for (const record of records) {
      for (const node of record.addedNodes) {
        if (!(node instanceof HTMLElement)) continue;
        if (node.matches("[data-glaze-interactive], .glaze-button, .glaze-material-live")) bindLiveSurface(node);
        bindAll(node);
      }
    }
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });
  return observer;
}

export const GlazeUI2 = Object.freeze({
  setClarity(value) { setEnumAttribute("glazeClarity", value, VALID_CLARITY); },
  setExpression(value) { setEnumAttribute("glazeExpression", value, VALID_EXPRESSION); },
  setAppearance(value) { setEnumAttribute("glazeAppearance", value, VALID_APPEARANCE); },
  bindLiveSurface,
  bindAll,
  setNavigationScrollState,
  connectedTransform,
  observeNewInteractiveSurfaces,
});

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => bindAll(), { once: true });
} else {
  bindAll();
}
