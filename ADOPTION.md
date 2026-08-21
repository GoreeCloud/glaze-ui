# Adopting Glaze UI

This guide describes how GoreeCloud applications should consume Glaze UI without unnecessary redesign or loss of product personality.

## 1. Record the target version

Record the Glaze UI version used by the application in its project documentation or source metadata. Stable products should state their conformance status and any approved exceptions.

Glaze UI 1.3.0 is the current Stable baseline. Consumers should record the exact Glaze UI version and, when practical, the canonical source revision used for validation.

## 2. Map semantics before replacing visuals

Start with semantic roles rather than copying literal CSS values. Map the application's existing canvas, surfaces, text, status colors, spacing, radii, focus treatment, motion, breakpoints, form states, selection controls, and feedback patterns to Glaze UI tokens and primitives.

Do not replace a successful product-specific composition merely to make it look like another GoreeCloud application.

## 3. Use the material hierarchy intentionally

- Canvas provides the atmospheric background.
- Solid prioritizes readability and is the normal content default.
- Raised separates important content with restrained elevation.
- Glaze adds selective translucency and depth.
- Overlay is reserved for attention-priority surfaces.
- Functional Glass is primarily for navigation, controls, toolbars, floating actions, and transient chrome.
- Clear Glass is reserved for controls over visually rich media such as photos, video, artwork, or maps.

A screen made entirely of translucent cards is not a Glaze UI requirement. Do not migrate ordinary content to glass solely because 1.3 adds richer material roles.

## 4. Adopt expression by role, not decoration

Map Compact, Standard, Expressive, Hero, and Pressed shape roles according to hierarchy and interaction purpose. Keep repeated utility controls calm. Reserve stronger geometry, hero typography, and expressive spatial motion for important actions, selected containers, product-defining moments, and meaningful transitions.

Use effects motion for color, opacity, border, and glow changes. Use spatial motion for position, geometry, layout, size, navigation, and container transformations. Reduced-motion behavior must remove nonessential scaling, shape morphing, and spatial transformation.

## 5. Adopt controls as semantic units

Treat labels, fields, help/error text, selection controls, switches, segmented controls, progress, and banners as complete behavioral units rather than isolated visual decorations.

Prefer native platform controls when they already provide the required semantics and ergonomics. Apply Glaze UI through tokens, spacing, typography, focus treatment, state feedback, and surrounding composition before replacing proven native accessibility behavior with custom controls.

## 6. Preserve accessibility from the beginning

Adopt visible keyboard focus, practical 44px minimum actionable targets, semantic names and states, persistent field labels, programmatically related error/help text, reduced-motion behavior, reduced-transparency behavior, increased-contrast handling, forced-colors support, and solid translucency fallbacks as part of the first implementation rather than as a later styling pass.

## 7. Adapt navigation, grouping, and reachability by available space

Use the four shared ranges:

- Compact: <= 599px
- Medium: 600–1023px
- Expanded: 1024–1439px
- Wide: >= 1440px

Transform navigation and information density when crossing ranges. Do not simply compress desktop layouts onto smaller screens.

On compact touch layouts, frequent actions may move into a lower visual reachability zone when useful, but document order, keyboard order, reading order, and programmatic relationships must remain intact. Adaptive button groups may give high-emphasis actions more space, but visual allocation must not change action meaning or access to sibling actions.

## 8. Design explicitly for phone, tablet, and desktop

Responsive width is not, by itself, sufficient evidence of good cross-platform design. GoreeCloud applications must treat phone, tablet, and desktop as distinct form-factor experiences when those targets are supported.

### Phone UI

Phone interfaces must be deliberately mobile. They should prioritize touch, reachability, one-handed use where practical, compact information hierarchy, mobile navigation, sheets and full-screen flows where appropriate, and content presentation that works without desktop-style multi-column assumptions. A phone application must not look or behave like a desktop or tablet interface that has merely been scaled down.

### Tablet UI

Tablet interfaces must use the additional space intentionally. They may use navigation rails, side panels, split views, master-detail layouts, contextual panes, larger previews, richer drag-and-drop, and denser but still touch-appropriate controls when useful. A tablet application must not simply stretch a phone layout across a larger canvas or preserve phone-only navigation when a tablet-specific composition would materially improve usability.

### Desktop UI

Desktop interfaces must take advantage of pointer and keyboard input, larger work areas, resizable windows, denser information presentation where useful, persistent navigation or toolbars, multi-pane workflows, contextual menus, keyboard shortcuts, hover states, drag-and-drop, and desktop window behavior when supported. A desktop application must not present a phone-first shell enlarged to fill a desktop window.

### Form-factor selection

Breakpoint ranges are implementation tools, not product identities. The application should choose the appropriate phone, tablet, or desktop composition from the available window, input model, platform conventions, and product role. Foldables, desktop window resizing, Stage Manager-style windows, DeX-like environments, and other variable-window contexts may move between compositions dynamically, but the selected composition must still feel native to the effective form factor.

## 9. Keep appearance preferences local by default

Theme or appearance preferences should remain on the client unless a documented product requirement justifies account-level synchronization. Glaze UI itself does not require analytics, remote fonts, remote icons, or third-party UI runtimes.

## 10. Add an application-level contract test

Each stable application should validate the subset of Glaze UI that it actually implements. Tests should focus on durable contracts—semantic tokens, accessible states, form relationships, selection semantics, material boundaries, expressive roles, fallbacks, form-factor behavior, and dependency boundaries—rather than fragile screenshots or exact DOM structure unless those are truly required.

Where an application targets multiple form factors, automated or reproducible acceptance should verify that representative phone, tablet, and desktop viewports activate the intended navigation, composition, density, and interaction patterns instead of only verifying that no horizontal overflow occurs.

## 11. Perform visual acceptance

Before a stable release, manually review representative phone/Compact, tablet/Medium, desktop/Expanded, and Wide layouts for every supported target, in both light and dark appearances where applicable. Confirm that forms, focus, errors, selection controls, progress, banners, overlays, navigation, Functional Glass, Clear Glass where used, expressive geometry, adaptive groups, reachability, motion, and information density remain polished and usable.

Visual acceptance must specifically reject a phone experience that looks like a shrunken tablet or desktop interface, a tablet experience that looks like a stretched phone interface, and a desktop experience that looks like an enlarged mobile interface. Confirm that each supported form factor feels purpose-built while remaining recognizably GoreeCloud and Glaze UI.

## Platform-native clients

Native Android, iOS, Linux, or other platform implementations do not need to reproduce web CSS. They should map the same Glaze UI semantic roles into native components while respecting platform ergonomics, accessibility conventions, and the form-factor-specific requirements above.
