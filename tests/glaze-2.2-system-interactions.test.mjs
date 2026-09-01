import test from 'node:test';
import assert from 'node:assert/strict';

import {
  activateSystemPanel,
  createControlCenterState,
  createSystemPanelState,
  createUniversalSearchState,
  orderUniversalSearchGroups,
  reduceControlCenter,
  reduceUniversalSearch,
} from '../js/glaze-2.2.system-interactions.candidate.mjs';

test('Universal Search opens with no implicit result selection', () => {
  const start = createUniversalSearchState({ resultCount: 3 });
  const { state } = reduceUniversalSearch(start, { type: 'open' });
  assert.equal(state.open, true);
  assert.equal(state.selectedIndex, -1);
  assert.equal(state.confirmationIndex, null);
});

test('Universal Search keyboard traversal enters deterministic first result then advances', () => {
  let state = reduceUniversalSearch(createUniversalSearchState({ resultCount: 3 }), { type: 'open' }).state;
  state = reduceUniversalSearch(state, { type: 'move', direction: 'next' }).state;
  assert.equal(state.selectedIndex, 0);
  state = reduceUniversalSearch(state, { type: 'move', direction: 'next' }).state;
  assert.equal(state.selectedIndex, 1);
  state = reduceUniversalSearch(state, { type: 'move', direction: 'previous' }).state;
  assert.equal(state.selectedIndex, 0);
});

test('Universal Search destructive action requires a second explicit execute', () => {
  let state = reduceUniversalSearch(createUniversalSearchState({ resultCount: 3 }), { type: 'open' }).state;
  state = reduceUniversalSearch(state, { type: 'select', index: 2 }).state;
  let outcome = reduceUniversalSearch(state, { type: 'execute', index: 2, destructive: true });
  assert.equal(outcome.effect.type, 'confirm');
  assert.equal(outcome.state.lastExecutedIndex, null);
  assert.equal(outcome.state.confirmationIndex, 2);
  outcome = reduceUniversalSearch(outcome.state, { type: 'execute', index: 2, destructive: true });
  assert.equal(outcome.effect.type, 'execute');
  assert.equal(outcome.state.lastExecutedIndex, 2);
  assert.equal(outcome.state.confirmationIndex, null);
});

test('Universal Search Escape cancels confirmation before closing', () => {
  let state = reduceUniversalSearch(createUniversalSearchState({ resultCount: 1 }), { type: 'open' }).state;
  state = reduceUniversalSearch(state, { type: 'select', index: 0 }).state;
  state = reduceUniversalSearch(state, { type: 'execute', index: 0, destructive: true }).state;
  let outcome = reduceUniversalSearch(state, { type: 'escape' });
  assert.equal(outcome.effect.type, 'cancel-confirmation');
  assert.equal(outcome.state.open, true);
  outcome = reduceUniversalSearch(outcome.state, { type: 'escape' });
  assert.equal(outcome.effect.type, 'close');
  assert.equal(outcome.state.open, false);
});

test('Universal Search preserves deterministic sources before generated answers', () => {
  const ordered = orderUniversalSearchGroups({
    'generated-answer': { text: 'Interpretation' },
    actions: [{ title: 'Open' }],
    files: [{ title: 'Project Brief' }],
    'best-match': [{ title: 'Project Brief' }],
  });
  assert.deepEqual(ordered.map((group) => group.key), ['best-match', 'files', 'actions', 'generated-answer']);
});

test('Control Center toggles semantic controls without changing unrelated controls', () => {
  const start = createControlCenterState({ wifi: true, bluetooth: false, focus: false });
  const next = reduceControlCenter(start, { type: 'toggle', control: 'wifi' });
  assert.equal(next.wifi, false);
  assert.equal(next.bluetooth, false);
  assert.equal(next.focus, false);
});

test('Control Center clamps brightness and volume to native percent ranges', () => {
  let state = createControlCenterState({ brightness: 64, volume: 64 });
  state = reduceControlCenter(state, { type: 'set', control: 'brightness', value: 140 });
  assert.equal(state.brightness, 100);
  state = reduceControlCenter(state, { type: 'set', control: 'volume', value: -12 });
  assert.equal(state.volume, 0);
});

test('Control Center Escape closes without mutating module values', () => {
  const start = createControlCenterState({ open: true, wifi: true, brightness: 72 });
  const next = reduceControlCenter(start, { type: 'escape' });
  assert.equal(next.open, false);
  assert.equal(next.wifi, true);
  assert.equal(next.brightness, 72);
});

test('system panel coordinator state admits only one dominant panel identity', () => {
  let state = createSystemPanelState();
  assert.equal(state.active, null);
  state = activateSystemPanel(state, 'search');
  assert.equal(state.active, 'search');
  state = activateSystemPanel(state, 'control-center');
  assert.equal(state.active, 'control-center');
  state = activateSystemPanel(state, null);
  assert.equal(state.active, null);
});

test('unknown system interaction events fail closed', () => {
  assert.throws(() => reduceUniversalSearch(createUniversalSearchState(), { type: 'mystery' }), /Unknown Universal Search event/);
  assert.throws(() => reduceControlCenter(createControlCenterState(), { type: 'toggle', control: 'unknown' }), /Unknown Control Center toggle/);
  assert.throws(() => activateSystemPanel(createSystemPanelState(), 'unknown'), /Unknown system panel/);
});
