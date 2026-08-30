const MATERIAL_LEVELS = Object.freeze({
  canvas: { opacity: 1, blurPx: 0 },
  surface: { opacity: 1, blurPx: 0 },
  'soft-glaze': { opacity: 0.88, blurPx: 18 },
  glaze: { opacity: 0.80, blurPx: 24 },
  'deep-glaze': { opacity: 0.86, blurPx: 32 },
  'live-glaze': { opacity: 0.84, blurPx: 28 },
});

const CLARITY = Object.freeze({
  clear: { opacityBias: -0.05, blurMultiplier: 1 },
  balanced: { opacityBias: 0, blurMultiplier: 0.85 },
  solid: { opacityBias: 0.18, blurMultiplier: 0 },
});

const PERFORMANCE = Object.freeze({
  full: { maxBlurPx: 40 },
  balanced: { maxBlurPx: 28 },
  constrained: { maxBlurPx: 16 },
  minimal: { maxBlurPx: 0 },
});

export const MATERIAL_BUDGETS = Object.freeze({
  productivity: { maxPercent: 22, maxDeepGlazeSurfaces: 2, maxLiveGlazeSurfaces: 1 },
  communication: { maxPercent: 30, maxDeepGlazeSurfaces: 2, maxLiveGlazeSurfaces: 2 },
  media: { maxPercent: 45, maxDeepGlazeSurfaces: 3, maxLiveGlazeSurfaces: 2 },
  administration: { maxPercent: 16, maxDeepGlazeSurfaces: 2, maxLiveGlazeSurfaces: 1 },
  creative: { maxPercent: 32, maxDeepGlazeSurfaces: 3, maxLiveGlazeSurfaces: 2 },
});

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

export function resolvePreferences(input = {}) {
  const materialClarity = ['clear', 'balanced', 'solid'].includes(input.materialClarity)
    ? input.materialClarity
    : 'balanced';
  const expressionLevel = ['calm', 'balanced', 'expressive'].includes(input.expressionLevel)
    ? input.expressionLevel
    : 'balanced';
  const density = ['comfortable', 'standard', 'compact', 'far-view'].includes(input.density)
    ? input.density
    : 'standard';
  const performanceProfile = ['full', 'balanced', 'constrained', 'minimal'].includes(input.performanceProfile)
    ? input.performanceProfile
    : 'balanced';
  const textScalePercent = Number.isFinite(Number(input.textScalePercent))
    ? Math.max(100, Number(input.textScalePercent))
    : 100;

  const forcedColors = Boolean(input.forcedColors);
  const reducedTransparency = Boolean(input.reducedTransparency);
  const reducedMotion = Boolean(input.reducedMotion);
  const increasedContrast = Boolean(input.increasedContrast);
  const showBoundaries = Boolean(input.showBoundaries);
  const largeText = Boolean(input.largeText) || textScalePercent >= 200;
  const touchAssistance = Boolean(input.touchAssistance);

  let effectiveMaterialClarity = materialClarity;
  let motionExpression = expressionLevel;
  let effectiveDensity = density;

  if (forcedColors || reducedTransparency) effectiveMaterialClarity = 'solid';
  if (reducedMotion) motionExpression = 'calm';
  if (largeText && density === 'compact') effectiveDensity = 'standard';

  return Object.freeze({
    materialClarity,
    effectiveMaterialClarity,
    expressionLevel,
    motionExpression,
    density,
    effectiveDensity,
    performanceProfile,
    textScalePercent: largeText ? Math.max(200, textScalePercent) : textScalePercent,
    reflowRequired: largeText,
    touchHitAreaMinPx: touchAssistance ? 56 : 48,
    boundaryStrength: forcedColors || increasedContrast || showBoundaries ? 'strong' : 'standard',
    focusVisibility: forcedColors || increasedContrast || showBoundaries ? 'strong' : 'standard',
    ambientColor: forcedColors || reducedTransparency ? 'off' : 'on',
    customSemanticColorMapping: forcedColors ? 'platform' : 'semantic',
    accentMayOverrideProtectedSemantics: false,
    accentMayOverridePlatformForcedColors: false,
    forcedColors,
    reducedTransparency,
    reducedMotion,
    increasedContrast,
    showBoundaries,
    largeText,
    touchAssistance,
  });
}

export function resolveMaterial(level, preferences) {
  if (!MATERIAL_LEVELS[level]) throw new TypeError(`Unknown Glaze material level: ${level}`);
  const prefs = preferences || resolvePreferences();
  const base = MATERIAL_LEVELS[level];
  const clarity = CLARITY[prefs.effectiveMaterialClarity] || CLARITY.balanced;
  const performance = PERFORMANCE[prefs.performanceProfile] || PERFORMANCE.balanced;
  const forceSolid = prefs.forcedColors || prefs.reducedTransparency || prefs.effectiveMaterialClarity === 'solid';
  const blurPx = forceSolid ? 0 : Math.min(base.blurPx * clarity.blurMultiplier, performance.maxBlurPx);
  const opacity = forceSolid ? 1 : clamp(base.opacity + clarity.opacityBias, 0, 1);
  return Object.freeze({
    level,
    opacity: Number(opacity.toFixed(3)),
    blurPx: Number(blurPx.toFixed(2)),
    solid: forceSolid || performance.maxBlurPx === 0,
    refractionEnabled: !forceSolid && prefs.performanceProfile !== 'constrained' && prefs.performanceProfile !== 'minimal',
    distortionEnabled: !forceSolid && prefs.performanceProfile !== 'constrained' && prefs.performanceProfile !== 'minimal' && ['glaze', 'deep-glaze', 'live-glaze'].includes(level),
  });
}

export function evaluateMaterialBudget({
  recipe = 'productivity',
  viewportArea,
  highIntensityArea,
  deepGlazeSurfaces = 0,
  liveGlazeSurfaces = 0,
}) {
  const budget = MATERIAL_BUDGETS[recipe];
  if (!budget) throw new TypeError(`Unknown Glaze recipe: ${recipe}`);
  const safeViewport = Math.max(1, Number(viewportArea) || 0);
  const safeHighIntensity = Math.max(0, Number(highIntensityArea) || 0);
  const percent = (safeHighIntensity / safeViewport) * 100;
  const reasons = [];
  if (percent > budget.maxPercent + 0.01) reasons.push(`high-intensity area ${percent.toFixed(2)}% exceeds ${budget.maxPercent}%`);
  if (deepGlazeSurfaces > budget.maxDeepGlazeSurfaces) reasons.push(`Deep Glaze count ${deepGlazeSurfaces} exceeds ${budget.maxDeepGlazeSurfaces}`);
  if (liveGlazeSurfaces > budget.maxLiveGlazeSurfaces) reasons.push(`Live Glaze count ${liveGlazeSurfaces} exceeds ${budget.maxLiveGlazeSurfaces}`);
  return Object.freeze({
    recipe,
    accepted: reasons.length === 0,
    percent: Number(percent.toFixed(2)),
    maxPercent: budget.maxPercent,
    deepGlazeSurfaces,
    maxDeepGlazeSurfaces: budget.maxDeepGlazeSurfaces,
    liveGlazeSurfaces,
    maxLiveGlazeSurfaces: budget.maxLiveGlazeSurfaces,
    reasons,
  });
}

function visibleIntersectionArea(rect, width, height) {
  const left = Math.max(0, rect.left);
  const top = Math.max(0, rect.top);
  const right = Math.min(width, rect.right);
  const bottom = Math.min(height, rect.bottom);
  return Math.max(0, right - left) * Math.max(0, bottom - top);
}

export function measureVisibleMaterialBudget(root = document, recipe = 'productivity') {
  const width = root.defaultView?.innerWidth || window.innerWidth;
  const height = root.defaultView?.innerHeight || window.innerHeight;
  let highIntensityArea = 0;
  let deepGlazeSurfaces = 0;
  let liveGlazeSurfaces = 0;
  for (const node of root.querySelectorAll('[data-glaze-material-level]')) {
    const level = node.dataset.glazeMaterialLevel;
    if (!['glaze', 'deep-glaze', 'live-glaze'].includes(level)) continue;
    const rect = node.getBoundingClientRect();
    const area = visibleIntersectionArea(rect, width, height);
    if (area <= 0) continue;
    highIntensityArea += area;
    if (level === 'deep-glaze') deepGlazeSurfaces += 1;
    if (level === 'live-glaze') liveGlazeSurfaces += 1;
  }
  return evaluateMaterialBudget({
    recipe,
    viewportArea: width * height,
    highIntensityArea,
    deepGlazeSurfaces,
    liveGlazeSurfaces,
  });
}

export function applyReferenceRuntime({ root = document.documentElement, shell, recipe = 'productivity', input = {} } = {}) {
  if (!shell) throw new TypeError('Glaze UI 2.1 reference runtime requires a shell element');
  const prefs = resolvePreferences(input);
  root.dataset.glazeAppearance = input.appearance || 'light';
  root.dataset.glazeClarity = prefs.effectiveMaterialClarity;
  root.dataset.glazeExpression = prefs.expressionLevel;
  root.dataset.glazeMotionExpression = prefs.motionExpression;
  root.dataset.glazeDensity = prefs.effectiveDensity;
  root.dataset.glazePerformance = prefs.performanceProfile;
  root.dataset.glazeBoundaryStrength = prefs.boundaryStrength;
  root.style.setProperty('--g21-motion-scale', prefs.reducedMotion ? '0.2' : '1');
  root.style.setProperty('--g21-touch-min', `${prefs.touchHitAreaMinPx}px`);
  root.style.setProperty('--g21-text-scale', String(prefs.textScalePercent / 100));
  shell.dataset.effectiveClarity = prefs.effectiveMaterialClarity;
  shell.dataset.effectiveDensity = prefs.effectiveDensity;
  shell.dataset.mode = input.mode || 'normal';
  shell.dataset.recipe = recipe;

  for (const node of document.querySelectorAll('[data-glaze-material-level]')) {
    const resolved = resolveMaterial(node.dataset.glazeMaterialLevel, prefs);
    node.style.setProperty('--g21-blur', `${resolved.blurPx}px`);
    node.dataset.effectiveBlur = String(resolved.blurPx);
    node.dataset.effectiveSolid = resolved.solid ? 'true' : 'false';
    node.dataset.refraction = resolved.refractionEnabled ? 'on' : 'off';
    node.dataset.distortion = resolved.distortionEnabled ? 'on' : 'off';
  }
  return prefs;
}

export function modeToPreferenceInput(mode, defaults = {}) {
  const input = { ...defaults, mode };
  if (mode === 'reduced-transparency') input.reducedTransparency = true;
  if (mode === 'reduced-motion') input.reducedMotion = true;
  if (mode === 'increased-contrast') input.increasedContrast = true;
  if (mode === 'show-boundaries') input.showBoundaries = true;
  if (mode === 'large-text') { input.largeText = true; input.textScalePercent = 200; }
  if (mode === 'touch-assistance') input.touchAssistance = true;
  if (mode === 'forced-colors') input.forcedColors = true;
  return input;
}
