# Glaze UI 1.3 Component Contract

Glaze UI standardizes component semantics and interaction quality without forcing every GoreeCloud application into the same composition.

## Universal component rules

Every interactive component must have a clear accessible name, a visible focus state, a minimum 44px practical pointer/touch target when directly actionable, and predictable disabled/loading behavior. Components should use semantic tokens instead of product-local literal colors, radii, spacing, icon sizes, state-layer opacity, focus colors, material values, or motion values when a corresponding token exists.

State vocabulary, where relevant: **default, hover, pressed, focused, selected, disabled, loading, info, success, warning, error, destructive**.

Glaze UI defines shared state-layer semantics for hover, pressed, focus, and selected presentation so feedback remains recognizable across products without requiring identical component artwork.

## Material and glass

Ordinary content should default to Solid or Raised surfaces. Functional Glass is reserved primarily for navigation, controls, toolbars, floating action regions, and transient chrome where translucency reinforces hierarchy. Clear Glass is reserved for controls over visually rich media such as photos, video, artwork, or maps.

Glass must never become the default treatment for every card or content container. All translucent components require a readable solid fallback for reduced-transparency preferences, unsupported backdrop filtering, increased contrast, forced colors, and contexts where the background would make the foreground difficult to read.

## Shape and expression

The shared expressive shape scale is **Compact, Standard, Expressive, Hero, and Pressed**. Shape communicates role, hierarchy, grouping, selection, and state; it is not arbitrary decoration.

Utility controls should normally use Compact or Standard shapes. Expressive shapes may identify prominent actions, selected containers, product-defining moments, or adaptive groups. Hero shapes are reserved for high-value visual moments. Pressed geometry may temporarily tighten during direct interaction when motion preferences permit.

Circular icon controls, pill-shaped search and action controls, and rounded card or panel containers are characteristic Glaze forms when they fit the component role. These forms should remain internally consistent within a surface and must not be applied so aggressively that unrelated controls become visually indistinguishable.

## Visual depth, adaptive color, and grouping

Glaze components should participate in a coherent visual field rather than appear as isolated widgets. Layering may use restrained blur, translucency, subtle highlight or reflection cues, soft shadow, borders, and floating separation to make the relationship between Canvas, Solid, Raised, Functional Glass, Clear Glass, and Overlay immediately understandable.

Color should adapt to the surrounding canvas and product accent through semantic roles. Soft tints, deeper accents, and neutral surfaces may shift between light and dark appearances or product contexts, but readable foreground contrast, semantic status meaning, focus visibility, and destructive-state clarity remain authoritative.

Complex screens should use deliberate whitespace, rounded grouping, aligned control clusters, and clear container hierarchy so information feels organized without becoming crowded. Data-dense products may use tighter density, but they should preserve recognizable grouping, scan paths, and separation between primary, supporting, and transient information.

Important content may use stronger weight, larger hero or display typography, and additional spacing to establish immediate hierarchy. Supporting content should remain quieter and readable so oversized type does not become the default for ordinary information.

## Motion

Effects motion governs changes such as color, opacity, border, glow, and subtle emphasis. Spatial motion governs geometry, layout, position, size, container transformation, navigation, and hero transitions. Prominent or hero interactions may use stronger spatial motion; repetitive utility controls should remain calm and quick.

Where appropriate, expressive controls may feel physical through bounded stretch, shift, compression, rebound, or shape morphing. Spring-like or bounce-like feedback should be brief and purposeful, should never interfere with task completion or target stability, and should not be used continuously across repetitive utility interactions.

Reduced-motion mode removes nonessential shape morphing, scaling, spring/rebound behavior, and spatial transformation rather than merely speeding them up.

## Buttons and adaptive action groups

Primary buttons use the Glaze accent treatment and may use the characteristic accent-to-secondary gradient. Secondary buttons use a quieter surface. Destructive actions use the danger semantic and must not rely on color alone. Loading buttons retain their label context and expose busy state to assistive technology. Compact density may reduce horizontal padding, but it must not reduce the minimum actionable target.

Expressive actions may use the expressive shape role and bounded press morphing. Adaptive button groups may allocate more horizontal space to a high-emphasis action while preserving document order, focus order, accessible names, and equivalent access to sibling actions. Layout emphasis must not imply that a destructive action is safer than it is.

## Icon buttons and icons

Icon-only controls require an accessible name. They use compact rounded geometry, minimum target sizing, visible focus, and optional tooltip support for unfamiliar actions. Shared icon sizes are 16, 20, 24, and 32 pixels or documented platform-native equivalents. Product icons and security/privacy identities remain governed by their separate GoreeCloud branding standards.

## Fields, inputs, search, textareas, and selects

Every user-editable field must have a persistent accessible label. Placeholder text is supplementary and never substitutes for a label. Help and error messages must be associated programmatically with their field when the platform supports that relationship. Error presentation uses the semantic danger role plus explanatory text; color alone is insufficient.

Textareas preserve readable line height and user-resizable behavior unless a documented product requirement justifies another approach. Search may use pill geometry where appropriate but must preserve normal keyboard, screen-reader, autofill, and browser behavior.

## Selection controls

Checkboxes and radio controls should prefer platform-native controls with Glaze accent semantics whenever native behavior satisfies the product need. Custom visual controls must preserve checked state, focus, disabled behavior, target sizing, and forced-colors resilience.

Switches represent immediate binary settings, not arbitrary action buttons. Their labels remain visible, their checked state is programmatic, and their visual track/thumb state is not the sole indication of the value.

Segmented controls and tabs expose a single selected item within a small related set. Tabs must preserve tab/list semantics and keyboard interaction when implemented as a tab interface; segmented action groups must use the appropriate pressed/selected semantics for their platform. Expressive selected-state geometry may be used when it remains stable, legible, and predictable.

## Cards, panels, and expressive tiles

Cards may use Solid, Raised, or Glaze surfaces only when the material role is intentional. A card is not automatically translucent. Interactive cards must have a clear focus/hover affordance and cannot hide separate nested actions behind one ambiguous click target.

Expressive tiles may use stronger shape hierarchy for selected, featured, or product-defining content. Ordinary dense data and repeated lists should generally use quieter geometry to avoid visual noise.

## Navigation and toolbars

Compact layouts may use bottom navigation, compact headers, drawers, or sheets. Expanded layouts may use sidebars or navigation rails. Current location must be visually and semantically identifiable using `aria-current`, selected state, or a platform-native equivalent. Navigation transforms by breakpoint rather than simply shrinking. Toolbars group related actions and preserve target sizing even when visual density is compact.

Functional Glass is particularly appropriate for navigation and toolbars that float above scrolling content because it creates separation without visually replacing the content layer.

## Dialogs, menus, sheets, overlays, and scrims

Overlays use the Overlay surface level, trap focus only while modal, restore focus on close, support Escape when appropriate, expose a programmatic name, and remain readable without blur/translucency. Modal experiences use the semantic scrim role rather than arbitrary product-local backdrop colors. Dialogs and sheets must account for safe areas and viewport bounds on mobile devices.

## Progress and loading

Progress indicators communicate determinate progress when a meaningful value is known and indeterminate loading only when duration or completion is unknown. Progress bars require an accessible name and value semantics when they represent measurable progress. Loading states must not silently remove the user's task context or make destructive actions appear available while work is pending.

## Tables and dense data

Tables prioritize scanability and accessible header relationships. Compact layouts may transform tables into card/list presentations when horizontal compression would harm readability. Status must not be communicated by color alone. Dense administrative surfaces may use compact spacing while keeping interactive targets accessible.

## Feedback and banners

Toasts, banners, badges, status indicators, loading states, empty states, and errors are first-class components. Feedback is concise, actionable when possible, and announced to assistive technology when the state change requires it. `info`, `success`, `warning`, `error`, and `destructive` are distinct semantic states.

Banners are persistent or semi-persistent in-context feedback and may include a concise action or dismissal control. Destructive or security-sensitive banners must explain the condition in text rather than relying only on a red border or icon.

## Hero typography and hierarchy

Hero typography may use stronger scale, weight, and tighter display spacing to establish a memorable product moment. It should remain concise and is paired with readable supporting text. Hero typography must respect user font scaling, localization, reflow, and platform accessibility behavior.

## Safe areas, reachability, and mobile ergonomics

Client interfaces must account for display cutouts, system bars, gesture regions, and platform safe-area insets where applicable. Glaze UI safe-area helpers are additive; platform-native clients should map them to the operating system's native inset APIs.

On compact touch layouts, frequent actions may be composed in a lower reachability zone when that improves one-handed use. This visual placement must not reorder the DOM, keyboard sequence, reading order, or programmatic relationship of the interface.

## Product-specific expression

Applications may vary accent emphasis, artwork, information density, navigation composition, hero treatments, data visualization, and specialized components. The goal is a family resemblance, not identical screens. Expression should strengthen a product's Role and Purpose rather than exist only to make the interface busier.
