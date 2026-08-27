import test from "node:test";
import assert from "node:assert/strict";

import {
  animate,
  createSpringKeyframes,
  detectCapabilities,
  prefersReducedMotion,
  resolveDuration,
  selectSpatialBackend,
} from "../js/glaze.motion.js";

test("reduced-motion detection is dependency-injectable", () => {
  assert.equal(prefersReducedMotion(() => ({ matches: true })), true);
  assert.equal(prefersReducedMotion(() => ({ matches: false })), false);
});

test("duration roles collapse to zero under reduced motion", () => {
  assert.equal(resolveDuration("medium", { reducedMotion: false }), 240);
  assert.equal(resolveDuration("medium", { reducedMotion: true }), 0);
  assert.throws(() => resolveDuration("unknown"), RangeError);
});

test("spring keyframes are deterministic and settle on the target", () => {
  const frames = createSpringKeyframes({ from: 10, to: 20, preset: "standard", samples: 12 });
  assert.equal(frames.length, 12);
  assert.deepEqual(frames[0], { offset: 0, value: 10 });
  assert.deepEqual(frames.at(-1), { offset: 1, value: 20 });
  assert.ok(frames.every((frame) => Number.isFinite(frame.value)));
});

test("animate delegates to Web Animations and strips travel under reduced motion", () => {
  const calls = [];
  const element = {
    animate(keyframes, options) {
      calls.push({ keyframes, options });
      return { cancel() {} };
    },
  };

  animate(element, [{ opacity: 0 }, { opacity: 1 }], {
    durationRole: "short",
    reducedMotion: true,
  });

  assert.equal(calls.length, 1);
  assert.deepEqual(calls[0].keyframes, [{ opacity: 1 }]);
  assert.equal(calls[0].options.duration, 0);
});

test("spatial backend selection degrades deterministically", () => {
  assert.equal(selectSpatialBackend({ webgpu: true, webgl2: true, canvas2d: true }), "webgpu");
  assert.equal(selectSpatialBackend({ webgpu: false, webgl2: true, canvas2d: true }), "webgl2");
  assert.equal(selectSpatialBackend({ webgpu: false, webgl2: false, canvas2d: true }), "canvas-svg-css");
  assert.equal(selectSpatialBackend({ webgpu: false, webgl2: false, canvas2d: false }), "static-accessible");
});

test("capability detection is side-effect free", () => {
  const capabilities = detectCapabilities({
    navigator: { gpu: {} },
    WebGL2RenderingContext: class {},
    CanvasRenderingContext2D: class {},
  });
  assert.equal(capabilities.webgpu, true);
  assert.equal(capabilities.webgl2, true);
  assert.equal(capabilities.canvas2d, true);
  assert.equal(capabilities.webAnimations, false);
});
