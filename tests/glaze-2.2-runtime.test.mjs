import test from 'node:test';
import assert from 'node:assert/strict';

import {
  evaluateSystemGlazeBudget,
  modeToSystemPreferences,
  resolveSystemMotion,
  resolveSystemPreferences,
  resolveSystemSurface,
} from '../js/glaze-2.2.candidate.mjs';

test('2.2 defaults preserve the 2.1 Stable boundary and accessible shell floor', () => {
  const prefs = resolveSystemPreferences();
  assert.equal(prefs.touchHitAreaMinPx, 48);
  assert.equal(prefs.systemTransparency, 'glaze');
  assert.equal(prefs.wallpaperMayOverrideSemanticColor, false);
});

test('Reduced Transparency makes system panels opaque and effects-free', () => {
  const prefs = resolveSystemPreferences({ reducedTransparency: true });
  const overlay = resolveSystemSurface('system-overlay', prefs);
  const panel = resolveSystemSurface('system-panel', prefs);
  assert.equal(overlay.blurPx, 0);
  assert.equal(panel.blurPx, 0);
  assert.equal(overlay.opacity, 1);
  assert.equal(panel.opacity, 1);
  assert.equal(overlay.solid, true);
  assert.equal(panel.solid, true);
});

test('Critical System is solid even when transparency is otherwise enabled', () => {
  const prefs = resolveSystemPreferences({ reducedTransparency: false });
  const critical = resolveSystemSurface('critical-system', prefs);
  assert.equal(critical.critical, true);
  assert.equal(critical.blurPx, 0);
  assert.equal(critical.opacity, 1);
  assert.equal(critical.nestedBackdropBlurAllowed, false);
});

test('Constrained and Minimal profiles reduce optional shell blur without changing semantics', () => {
  const constrained = resolveSystemSurface(
    'system-panel',
    resolveSystemPreferences({ performanceProfile: 'constrained' }),
  );
  const minimal = resolveSystemSurface(
    'system-panel',
    resolveSystemPreferences({ performanceProfile: 'minimal' }),
  );
  assert.equal(constrained.blurPx, 14);
  assert.equal(constrained.material, 'thick-glaze');
  assert.equal(minimal.blurPx, 0);
  assert.equal(minimal.solid, true);
});

test('Touch Assistance raises the shell target floor to 56px', () => {
  const prefs = resolveSystemPreferences({ touchAssistance: true });
  assert.equal(prefs.touchHitAreaMinPx, 56);
});

test('Reduced Motion keeps direct manipulation immediate and shortens spatial transitions', () => {
  const prefs = resolveSystemPreferences({ reducedMotion: true });
  const workspace = resolveSystemMotion('workspace', prefs);
  const search = resolveSystemMotion('search', prefs);
  assert.equal(workspace.reduced, true);
  assert.equal(workspace.durationMs, 120);
  assert.equal(search.durationMs, 100);
  assert.equal(workspace.keyboardTraversalWaitsForAnimation, false);
  assert.equal(workspace.directManipulationTracksInput, true);
});

test('normal system motion remains inside the documented 2.2 envelopes', () => {
  const prefs = resolveSystemPreferences();
  assert.ok(resolveSystemMotion('popover', prefs).durationMs >= 160);
  assert.ok(resolveSystemMotion('popover', prefs).durationMs <= 200);
  assert.ok(resolveSystemMotion('panel', prefs).durationMs >= 220);
  assert.ok(resolveSystemMotion('panel', prefs).durationMs <= 280);
  assert.ok(resolveSystemMotion('search', prefs).durationMs >= 240);
  assert.ok(resolveSystemMotion('search', prefs).durationMs <= 320);
  assert.ok(resolveSystemMotion('workspace', prefs).durationMs >= 320);
  assert.ok(resolveSystemMotion('workspace', prefs).durationMs <= 420);
  assert.ok(resolveSystemMotion('unlock', prefs).durationMs >= 280);
  assert.ok(resolveSystemMotion('unlock', prefs).durationMs <= 420);
});

test('system Glaze budget rejects excessive simultaneous shell glass', () => {
  assert.equal(evaluateSystemGlazeBudget({ dominantPanels: 1, smallFloatingControls: 3 }).accepted, true);
  const tooManyPanels = evaluateSystemGlazeBudget({ dominantPanels: 2, smallFloatingControls: 1 });
  assert.equal(tooManyPanels.accepted, false);
  assert.match(tooManyPanels.reasons[0], /dominant Glaze panel count/);
  const tooManyControls = evaluateSystemGlazeBudget({ dominantPanels: 1, smallFloatingControls: 4 });
  assert.equal(tooManyControls.accepted, false);
  assert.match(tooManyControls.reasons[0], /small floating Glaze control count/);
});

test('explicit exceptional shell context may exceed the ordinary Glaze budget', () => {
  const result = evaluateSystemGlazeBudget({
    dominantPanels: 2,
    smallFloatingControls: 4,
    explicitException: true,
  });
  assert.equal(result.accepted, true);
  assert.equal(result.explicitException, true);
});

test('mode mapping does not silently enable unrelated accessibility preferences', () => {
  const forced = resolveSystemPreferences(modeToSystemPreferences('forced-colors'));
  assert.equal(forced.forcedColors, true);
  assert.equal(forced.reducedMotion, false);
  assert.equal(forced.systemTransparency, 'solid');

  const large = resolveSystemPreferences(modeToSystemPreferences('large-text'));
  assert.equal(large.largeText, true);
  assert.equal(large.textScalePercent, 200);
});

test('unknown system surface and motion roles fail closed', () => {
  assert.throws(() => resolveSystemSurface('mystery-surface'), TypeError);
  assert.throws(() => resolveSystemMotion('cinematic'), TypeError);
});
