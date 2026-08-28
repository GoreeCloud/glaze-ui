/* Glaze UI 2.0 Candidate wearable/spatial runtime.
 * No telemetry, networking, storage, or remote dependencies.
 */

const ROTARY_SELECTOR = '[data-glaze-rotary-item]';

function rotaryItems(nav) {
  if (!(nav instanceof HTMLElement)) throw new TypeError('Wearable rotary navigation element is required');
  return [...nav.querySelectorAll(ROTARY_SELECTOR)].filter(item => item instanceof HTMLElement);
}

function normalizedIndex(index, length) {
  if (!length) return -1;
  return ((index % length) + length) % length;
}

function setRotarySelection(nav, index, { focus = true } = {}) {
  const items = rotaryItems(nav);
  if (!items.length) throw new TypeError('Wearable rotary navigation requires at least one item');
  const selected = normalizedIndex(index, items.length);

  items.forEach((item, itemIndex) => {
    const current = itemIndex === selected;
    item.setAttribute('aria-current', current ? 'true' : 'false');
    item.tabIndex = current ? 0 : -1;
  });

  nav.dataset.rotaryIndex = String(selected);
  const active = items[selected];
  active.scrollIntoView({ block: 'center', inline: 'nearest', behavior: 'auto' });
  if (focus) active.focus({ preventScroll: true });
  return active;
}

function moveRotarySelection(nav, delta) {
  const items = rotaryItems(nav);
  const current = Math.max(0, items.findIndex(item => item.getAttribute('aria-current') === 'true'));
  return setRotarySelection(nav, current + delta);
}

function bindRotaryNavigation(nav) {
  if (!(nav instanceof HTMLElement)) throw new TypeError('Wearable rotary navigation element is required');
  if (nav.dataset.glazeRotaryBound === 'true') return nav;
  nav.dataset.glazeRotaryBound = 'true';

  const items = rotaryItems(nav);
  if (!items.length) throw new TypeError('Wearable rotary navigation requires at least one item');
  const initial = Math.max(0, items.findIndex(item => item.getAttribute('aria-current') === 'true'));
  setRotarySelection(nav, initial, { focus: false });

  nav.addEventListener('wheel', event => {
    if (!event.deltaY && !event.deltaX) return;
    event.preventDefault();
    moveRotarySelection(nav, (event.deltaY || event.deltaX) > 0 ? 1 : -1);
  }, { passive: false });

  nav.addEventListener('keydown', event => {
    let next = null;
    if (event.key === 'ArrowDown' || event.key === 'ArrowRight') next = 1;
    else if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') next = -1;
    else if (event.key === 'Home') next = 'home';
    else if (event.key === 'End') next = 'end';
    if (next == null) return;
    event.preventDefault();
    if (next === 'home') setRotarySelection(nav, 0);
    else if (next === 'end') setRotarySelection(nav, items.length - 1);
    else moveRotarySelection(nav, next);
  });

  nav.addEventListener('click', event => {
    const item = event.target instanceof Element ? event.target.closest(ROTARY_SELECTOR) : null;
    if (!(item instanceof HTMLElement)) return;
    const index = rotaryItems(nav).indexOf(item);
    if (index >= 0) setRotarySelection(nav, index);
  });

  return nav;
}

function setSpatialDepth(element, depth) {
  if (!(element instanceof HTMLElement)) throw new TypeError('Spatial surface element is required');
  const value = Number(depth);
  if (!Number.isFinite(value) || value < -2 || value > 3) throw new TypeError(`Invalid spatial depth: ${depth}`);
  element.dataset.spatialDepth = String(value);
  element.style.setProperty('--glaze-spatial-depth', String(value));
  return element;
}

function setSpatialFlat(root, flat) {
  if (!(root instanceof HTMLElement)) throw new TypeError('Spatial root element is required');
  root.dataset.glazeSpatialFlat = String(Boolean(flat));
  return root;
}

export const GlazeUI2Emerging = Object.freeze({
  bindRotaryNavigation,
  setRotarySelection,
  moveRotarySelection,
  setSpatialDepth,
  setSpatialFlat,
});
