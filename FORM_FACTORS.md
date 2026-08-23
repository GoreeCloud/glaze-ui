# Glaze UI 1.4 Form-Factor Contract

Glaze UI 1.4 treats **Mobile, Tablet, Desktop, and TV** as purpose-built interaction environments. A viewport breakpoint is an implementation signal, not a device identity. Products choose composition from the effective app window, primary input model, viewing distance, platform conventions, posture, and product Role and Purpose.

The same product should feel recognizably GoreeCloud across form factors without forcing the same navigation, density, pane structure, or interaction model everywhere.

## Shared rules

Every supported form factor must preserve:

- the Glaze UI semantic color, material, shape, typography, state, and motion vocabulary;
- accessible names, semantic states, visible focus, readable contrast, and platform accessibility behavior;
- task continuity when the window, posture, orientation, or input context changes;
- stable reading order, keyboard/focus order, and equivalent access to critical actions;
- product identity and Role-and-Purpose-specific personality;
- local-first presentation dependencies and Glaze UI privacy boundaries;
- explicit fallback behavior when blur, transparency, animation, hover, touch, or pointer input is unavailable.

Form-factor adaptation may change navigation placement, number of visible panes, density, hierarchy, control placement, menu model, selection model, and information architecture when those changes improve the target experience.

## Selecting a form-factor composition

Use the following signals together rather than relying on a device-name check:

1. **App window** — available width, height, aspect ratio, and resizability.
2. **Primary input** — touch, stylus, pointer, keyboard, directional remote/D-pad, or a combination.
3. **Viewing distance** — near personal-device viewing versus far living-room viewing.
4. **Platform conventions** — native windowing, navigation, safe areas, focus systems, and system chrome.
5. **Posture and orientation** — folded/unfolded state, portrait/landscape, docked presentation, and multi-window state.
6. **Product task** — quick capture, reading, creation, administration, media browsing, monitoring, or another dominant workflow.

A large window does not automatically mean Desktop, and a 1920-pixel display does not automatically mean TV. TV is defined primarily by far viewing distance and directional focus input.

## Mobile UI

Mobile is **touch-first, reachability-first, and task-focused**.

### Composition

- Prefer one primary task or content stream at a time.
- Use intentionally stacked content instead of desktop-style multi-column compression.
- Keep the highest-frequency actions reachable, including lower action zones when useful.
- Preserve safe areas around cutouts, system bars, hinges, and gesture regions.
- Use sheets or full-screen flows when a desktop dialog would feel cramped.
- Transform dense tables into readable cards, lists, or progressive detail when horizontal compression would harm scanability.
- Keep persistent chrome compact so content remains dominant.

### Navigation

- Bottom navigation, compact top bars, drawers, and sheets are appropriate when they fit the product.
- Primary destinations should remain easy to reach with one hand where practical.
- Back behavior must match platform conventions and preserve task state.

### Controls and density

- Touch targets must remain practical even when visual density is compact.
- Frequently used actions should not depend on hover or precision pointing.
- Text entry, selection, and destructive actions need clear mobile-safe confirmation and recovery paths.

### Mobile anti-patterns

Reject:

- desktop sidebars compressed into narrow strips;
- wide toolbars wrapped into multiple rows of tiny controls;
- desktop tables requiring routine horizontal scrolling;
- tiny icon-only actions without labels or discoverability;
- modal windows that exceed the dynamic viewport;
- a desktop or tablet layout merely scaled down.

## Tablet UI

Tablet is **touch-capable, pane-aware, posture-aware, and spacious without becoming sparse**.

### Composition

- Use the larger canvas to reduce unnecessary navigation between related information.
- Introduce split views, master-detail relationships, contextual panes, larger previews, or comparison layouts when they improve the task.
- Allow panes to collapse, reconfigure, or become modal as the app window narrows.
- Preserve touch-appropriate controls even when information density increases.
- Use landscape and portrait intentionally rather than assuming one tablet orientation.
- Account for foldable postures, hinges, tabletop modes, and resizable multi-window states when the platform exposes them.

### Navigation

- Navigation rails, side panels, adaptive navigation suites, and persistent contextual regions are preferred when they reduce repeated transitions.
- Navigation should not remain phone-only merely because it still technically fits.

### Input

- Touch remains first-class.
- Pointer, keyboard, and stylus input should receive useful enhancement rather than being ignored.
- Drag-and-drop, hover previews, shortcuts, and context actions may be added when supported without making touch users second-class.

### Tablet anti-patterns

Reject:

- a phone layout centered inside large unused margins;
- phone-only navigation stretched across a wide canvas;
- huge single-column cards that waste available space;
- desktop-density controls that become uncomfortable for touch;
- fixed panes that cannot adapt when the window is resized.

## Desktop UI

Desktop is **workspace-first, pointer-and-keyboard-first, resizable, and productivity-oriented**.

### Composition

- Use persistent navigation, toolbars, inspectors, sidebars, multi-pane workspaces, and denser information presentation when useful.
- Keep the main working region visually dominant while allowing supporting panes to remain available.
- Support useful window resizing rather than optimizing only for maximized/full-screen windows.
- Allow panels to collapse, resize, detach, or reconfigure when the product benefits from user-controlled workspace density.
- Avoid unbounded content stretching; preserve readable line lengths and purposeful maximum widths.

### Input and commands

- Keyboard navigation and shortcuts should cover frequent workflows where appropriate.
- Hover may reveal previews or secondary affordances, but core actions must remain discoverable without hover alone.
- Context menus, right-click actions, precise selection, multi-select, drag-and-drop, and scrollbars may be used when they improve desktop productivity.
- Focus order and shortcut behavior must remain coherent across resizable panes.

### Desktop anti-patterns

Reject:

- a phone-first shell enlarged to fill the window;
- oversized touch-only controls dominating dense administrative work;
- hidden menus that force mobile-style navigation for routine desktop tasks;
- fixed full-screen assumptions that break in resizable windows;
- wide text columns or stretched buttons simply because space exists.

## TV UI

TV is **far-viewing, landscape-first, focus-first, and remote-friendly**. TV must never be treated as Wide Desktop.

### Viewing and safe composition

- Design for a living-room viewing distance rather than near-screen reading.
- Use larger typography, icons, controls, and spacing than personal-device interfaces.
- Keep critical interactive content inside an overscan-safe region. Glaze UI uses a 5% safe-margin semantic with 1080p reference insets of 48 dp horizontally and 27 dp vertically.
- Background artwork may extend beyond the safe region; essential labels and controls may not.
- Prefer short, scannable copy over dense paragraphs.
- Keep hierarchy simple enough to understand from across a room.

### Directional focus model

- Every actionable TV element must be reachable with directional input using a remote, D-pad, game controller, or keyboard arrows.
- Focus must always be obvious. Glaze TV focus may use coordinated scale, lift, border/halo, color, and elevation.
- Focus movement should be spatially predictable. Avoid dead ends, surprising jumps, and controls placed outside a clear directional path.
- Focus and selection are distinct: moving to an item must not unexpectedly activate it.
- When a focused item disappears, move focus only to a nearby predictable replacement when the platform focus system supports it.
- Do not require a pointer for primary TV navigation.

### TV navigation and content

- Prefer simple side navigation or clearly grouped top-level destinations rather than phone action bars or pull-down menu patterns.
- Horizontal rows may browse items while vertical movement changes sections, producing a predictable two-axis model when appropriate.
- Keep nested focus hierarchies shallow.
- Search and text input should be minimized; when required, use platform-native TV input and voice/search capabilities where available.
- Media controls should remain operable by remote and should not depend on swipe gestures.

### TV motion and materials

- Focus movement may use stronger depth than desktop hover because focus is the user's primary location indicator.
- Scale/lift must remain bounded so focused items do not overlap nearby content or cause layout instability.
- Reduced-motion mode removes focus scaling/lift and preserves a high-contrast static focus treatment.
- Rich backgrounds may use Clear Glass for readable controls, but Solid/Raised fallbacks remain mandatory.

### TV anti-patterns

Reject:

- reused phone or tablet layouts;
- Wide Desktop layouts with a remote bolted on;
- pointer-dependent primary navigation;
- swipe-only flows;
- tiny labels, dense tables, long paragraphs, and nested settings trees;
- focusable controls with no clear directional path;
- focused-item growth that clips, overlaps, or shifts surrounding layout;
- essential controls placed outside the overscan-safe region.

## Transition behavior

When a product can move between Mobile, Tablet, and Desktop compositions through resizing, folding, docking, or desktop-mode windowing:

- preserve the active object, draft, scroll position, selection, and task context when practical;
- avoid reordering content merely for visual convenience when it would change reading or keyboard order;
- do not infer TV solely from a large external display; require a TV/far-viewing or directional-input context;
- prefer a small number of stable composition modes over continuous layout churn;
- allow platform-native window and focus systems to remain authoritative when they provide stronger accessibility or predictability.

## Required acceptance matrix

Glaze UI 1.4 Stable form-factor acceptance requires representative acceptance for every supported profile. The canonical reference matrix includes:

| Profile | Reference size | Primary interaction |
| --- | ---: | --- |
| Mobile | 390 × 844 | Touch / keyboard accessibility |
| Tablet | 820 × 1180 | Touch + optional pointer/keyboard |
| Desktop | 1280 × 900 | Pointer + keyboard |
| Wide Desktop | 1600 × 1000 | Pointer + keyboard |
| TV | 1920 × 1080 | Directional focus / remote-style navigation |

Unsupported is an explicit state. Untested is not equivalent to unsupported or accepted.
