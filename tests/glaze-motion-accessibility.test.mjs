import test from "node:test";
import assert from "node:assert/strict";
import { createAccessibleReorderController, createSettlingBudget, resolveReorderCommand } from "../js/glaze.motion.accessibility.js";

test("reorder commands map arrows and edges without localized copy", () => {
  assert.deepEqual(resolveReorderCommand("ArrowUp"), { type: "move", delta: -1 });
  assert.deepEqual(resolveReorderCommand("Home"), { type: "edge", edge: "start" });
  assert.deepEqual(resolveReorderCommand("Enter"), { type: "none" });
});

test("accessible reorder controller returns semantic position metadata", () => {
  const controller = createAccessibleReorderController([{ id: "a" }, { id: "b" }, { id: "c" }]);
  const result = controller.moveByCommand("b", "End");
  assert.equal(result.moved, true);
  assert.equal(result.fromIndex, 1);
  assert.equal(result.toIndex, 2);
  assert.equal(result.position, 3);
  assert.equal(result.total, 3);
  assert.deepEqual(result.items.map((item) => item.id), ["a", "c", "b"]);
  assert.equal("announcement" in result, false);
});

test("horizontal directional semantics preserve input parity", () => {
  const controller = createAccessibleReorderController([{ id: "a" }, { id: "b" }]);
  assert.deepEqual(controller.moveByCommand("a", "ArrowRight", { orientation: "horizontal" }).items.map((item) => item.id), ["b", "a"]);
});

test("settling budget caps concurrent nonessential motion", () => {
  const budget = createSettlingBudget({ maxConcurrent: 2 });
  const first = budget.acquire(); const second = budget.acquire(); const third = budget.acquire();
  assert.equal(first.accepted, true); assert.equal(second.accepted, true);
  assert.deepEqual({ accepted: third.accepted, reason: third.reason }, { accepted: false, reason: "budget-exhausted" });
  assert.equal(budget.snapshot().activeCount, 2);
  first.release();
  assert.equal(budget.snapshot().activeCount, 1);
  assert.equal(budget.acquire().accepted, true);
});

test("reduced motion refuses settling animation without blocking semantic state work", () => {
  const budget = createSettlingBudget({ reducedMotion: true });
  const ticket = budget.acquire();
  assert.deepEqual({ accepted: ticket.accepted, reason: ticket.reason }, { accepted: false, reason: "reduced-motion" });
  assert.equal(budget.snapshot().activeCount, 0);
});
