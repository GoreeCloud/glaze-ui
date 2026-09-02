import test from 'node:test';
import assert from 'node:assert/strict';

import {
  evaluateSystemGlazeBudget,
  resolveSystemMotion,
  resolveSystemPreferences,
  resolveSystemSurface,
} from '../js/glaze-2.2.candidate.mjs';

const PROFILE_MAX = Object.freeze({ full: 32, balanced: 28, constrained: 14, minimal: 0 });
const BASE_BLUR = Object.freeze({
  workspace: 0,
  application: 0,
  'system-overlay': 22,
  'system-panel': 28,
  'critical-system': 0,
});

test('performance profiles cap every system surface deterministically', () => {
  for (const [profile, maxBlurPx] of Object.entries(PROFILE_MAX)) {
    const prefs = resolveSystemPreferences({ performanceProfile: profile });
    for (const [surface, baseBlur] of Object.entries(BASE_BLUR)) {
      const resolved = resolveSystemSurface(surface, prefs);
      assert.equal(resolved.blurPx, Math.min(baseBlur, maxBlurPx), `${profile} ${surface}`);
      assert.ok(resolved.blurPx <= maxBlurPx, `${profile} ${surface} exceeds profile cap`);
    }
  }
});

test('Reduced Transparency and Forced Colors force zero system blur', () => {
  for (const input of [{ reducedTransparency: true }, { forcedColors: true }]) {
    const prefs = resolveSystemPreferences(input);
    for (const surface of Object.keys(BASE_BLUR)) {
      assert.equal(resolveSystemSurface(surface, prefs).blurPx, 0, `${surface} must be effects-free`);
    }
  }
});

test('critical system is always solid and effects-free', () => {
  for (const profile of Object.keys(PROFILE_MAX)) {
    const surface = resolveSystemSurface('critical-system', resolveSystemPreferences({ performanceProfile: profile }));
    assert.equal(surface.blurPx, 0);
    assert.equal(surface.solid, true);
    assert.equal(surface.critical, true);
  }
});

test('Glaze budget accepts normal composition and rejects excess without explicit exception', () => {
  assert.equal(evaluateSystemGlazeBudget({ dominantPanels: 1, smallFloatingControls: 3 }).accepted, true);
  assert.equal(evaluateSystemGlazeBudget({ dominantPanels: 2, smallFloatingControls: 3 }).accepted, false);
  assert.equal(evaluateSystemGlazeBudget({ dominantPanels: 1, smallFloatingControls: 4 }).accepted, false);
  assert.equal(evaluateSystemGlazeBudget({ dominantPanels: 2, smallFloatingControls: 4, explicitException: true }).accepted, true);
});

test('reduced motion keeps semantic interaction immediate', () => {
  const prefs = resolveSystemPreferences({ reducedMotion: true });
  for (const role of ['popover', 'panel', 'search', 'workspace', 'unlock']) {
    const motion = resolveSystemMotion(role, prefs);
    assert.equal(motion.keyboardTraversalWaitsForAnimation, false);
    assert.equal(motion.directManipulationTracksInput, true);
    assert.equal(motion.reduced, true);
    assert.ok(motion.durationMs <= 120);
  }
});
