/**
 * Glaze Motion 0.1 Experimental runtime primitives.
 *
 * This module is dependency-free and intentionally limited to Motion Core.
 * Motion Studio and Motion Spatial remain planned capability tiers.
 */

export const GLAZE_MOTION_VERSION = "0.1.0";
export const GLAZE_MOTION_STATUS = "experimental";

export const durations = Object.freeze({
  instant: 0,
  micro: 90,
  short: 160,
  medium: 240,
  long: 360,
  ambient: 700,
});

export const easings = Object.freeze({
  standard: "cubic-bezier(0.2, 0, 0, 1)",
  enter: "cubic-bezier(0, 0, 0, 1)",
  exit: "cubic-bezier(0.3, 0, 1, 1)",
  emphasized: "cubic-bezier(0.2, 0, 0, 1)",
  linear: "linear",
});

export const springs = Object.freeze({
  restrained: Object.freeze({ mass: 1, stiffness: 520, damping: 44, initialVelocity: 0, settleMs: 260 }),
  standard: Object.freeze({ mass: 1, stiffness: 420, damping: 32, initialVelocity: 0, settleMs: 340 }),
  expressive: Object.freeze({ mass: 1, stiffness: 360, damping: 24, initialVelocity: 0, settleMs: 460 }),
  spatial: Object.freeze({ mass: 1, stiffness: 300, damping: 28, initialVelocity: 0, settleMs: 520 }),
});

function resolveReducedMotion(explicit, matchMediaFn) {
  if (typeof explicit === "boolean") return explicit;
  const matcher = matchMediaFn ?? globalThis.matchMedia;
  if (typeof matcher !== "function") return false;
  return Boolean(matcher("(prefers-reduced-motion: reduce)")?.matches);
}

export function prefersReducedMotion(matchMediaFn) {
  return resolveReducedMotion(undefined, matchMediaFn);
}

export function resolveDuration(role = "medium", options = {}) {
  if (!(role in durations)) {
    throw new RangeError(`Unknown Glaze Motion duration role: ${role}`);
  }

  return resolveReducedMotion(options.reducedMotion, options.matchMedia) ? 0 : durations[role];
}

export function createSpringKeyframes(options = {}) {
  const {
    from = 0,
    to = 1,
    preset = "standard",
    samples = 36,
  } = options;

  const spring = springs[preset];
  if (!spring) throw new RangeError(`Unknown Glaze Motion spring preset: ${preset}`);
  if (!Number.isInteger(samples) || samples < 2 || samples > 240) {
    throw new RangeError("samples must be an integer between 2 and 240");
  }

  const { mass, stiffness, damping, initialVelocity, settleMs } = spring;
  const omega0 = Math.sqrt(stiffness / mass);
  const zeta = damping / (2 * Math.sqrt(stiffness * mass));
  const durationSeconds = settleMs / 1000;
  const frames = [];

  for (let index = 0; index < samples; index += 1) {
    const progress = index / (samples - 1);
    const t = progress * durationSeconds;
    let normalized;

    if (zeta < 1) {
      const omegaD = omega0 * Math.sqrt(1 - zeta * zeta);
      const envelope = Math.exp(-zeta * omega0 * t);
      const coefficient = (zeta * omega0 - initialVelocity) / omegaD;
      normalized = 1 - envelope * (Math.cos(omegaD * t) + coefficient * Math.sin(omegaD * t));
    } else {
      const envelope = Math.exp(-omega0 * t);
      normalized = 1 - envelope * (1 + (omega0 - initialVelocity) * t);
    }

    const value = from + (to - from) * normalized;
    frames.push({ offset: progress, value });
  }

  frames[0] = { offset: 0, value: from };
  frames[frames.length - 1] = { offset: 1, value: to };
  return frames;
}

export function animate(element, keyframes, options = {}) {
  if (!element || typeof element.animate !== "function") {
    throw new TypeError("Glaze Motion animate() requires an element with Web Animations API support");
  }

  if (!Array.isArray(keyframes) || keyframes.length === 0) {
    throw new TypeError("keyframes must be a non-empty array");
  }

  const reducedMotion = resolveReducedMotion(options.reducedMotion, options.matchMedia);
  const duration = resolveDuration(options.durationRole ?? "medium", { reducedMotion });
  const easingRole = options.easingRole ?? "standard";
  const easing = easings[easingRole];
  if (!easing) throw new RangeError(`Unknown Glaze Motion easing role: ${easingRole}`);

  const resolvedKeyframes = reducedMotion ? [keyframes[keyframes.length - 1]] : keyframes;
  return element.animate(resolvedKeyframes, {
    duration,
    easing,
    fill: options.fill ?? "both",
    iterations: options.iterations ?? 1,
    direction: options.direction ?? "normal",
  });
}

export function detectCapabilities(environment = globalThis) {
  const navigatorObject = environment.navigator ?? {};
  return Object.freeze({
    webAnimations: typeof environment.Element !== "undefined" && typeof environment.Element?.prototype?.animate === "function",
    webgpu: Boolean(navigatorObject.gpu),
    webgl2: typeof environment.WebGL2RenderingContext !== "undefined",
    canvas2d: typeof environment.CanvasRenderingContext2D !== "undefined",
  });
}

export function selectSpatialBackend(capabilities = detectCapabilities()) {
  if (capabilities.webgpu) return "webgpu";
  if (capabilities.webgl2) return "webgl2";
  if (capabilities.canvas2d) return "canvas-svg-css";
  return "static-accessible";
}
