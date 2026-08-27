import test from "node:test";
import assert from "node:assert/strict";
import { createReferenceQueue } from "../reference/glaze-motion-consumer.mjs";

test("reference consumer proves keyboard reorder without production-app claims", () => {
  const queue = createReferenceQueue([{ id: "one" }, { id: "two" }, { id: "three" }]);
  assert.deepEqual(queue.reorderByKey("two", "ArrowUp").map((item) => item.id), ["two", "one", "three"]);
});

test("reference consumer preserves state when shared transitions are unavailable", () => {
  const queue = createReferenceQueue([{ id: "one" }]);
  const result = queue.select("one", { document: {}, reducedMotion: false });
  assert.equal(result.usedViewTransition, false);
  assert.equal(queue.snapshot().selectedKey, "one");
});

test("reference consumer collects local performance evidence only", () => {
  const queue = createReferenceQueue([{ id: "one" }]);
  queue.recordFrame(0); queue.recordFrame(17); queue.recordLongTask(55);
  const metrics = queue.snapshot().performance;
  assert.equal(metrics.frameCount, 1);
  assert.equal(metrics.overBudgetFrames, 1);
  assert.equal(metrics.longTaskCount, 1);
  assert.equal("send" in metrics, false);
});
