import { createFrameBudgetProbe, createReorderModel, resolveSwipeAction, startSharedTransition } from "../js/glaze.motion.js";

/**
 * Representative Glaze Motion 0.3 consumer harness.
 * This is evidence for the design-system contract, not production certification for any GoreeCloud app.
 */
export function createReferenceQueue(items, options = {}) {
  const reorder = createReorderModel(items, { getKey: options.getKey });
  const performance = createFrameBudgetProbe(options.performance);
  let selectedKey = null;

  function reorderByKey(itemKey, key, inputOptions = {}) {
    return reorder.moveByKey(itemKey, key, inputOptions);
  }

  function classifySwipe(distancePx, extentPx, velocity = 0) {
    return resolveSwipeAction(distancePx, extentPx, { velocity });
  }

  function select(itemKey, transitionOptions = {}) {
    return startSharedTransition(() => {
      selectedKey = itemKey;
      return selectedKey;
    }, transitionOptions);
  }

  function snapshot() {
    return Object.freeze({ items: reorder.snapshot(), selectedKey, performance: performance.snapshot() });
  }

  return Object.freeze({ reorderByKey, classifySwipe, select, recordFrame: performance.recordFrame, recordLongTask: performance.recordLongTask, snapshot });
}
