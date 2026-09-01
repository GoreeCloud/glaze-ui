# Glaze UI 2.2 Visual Direction — GoreeCloud Optical Reachability

**Lifecycle:** Candidate visual direction  
**Stable boundary:** Glaze UI 2.1.0 remains current Stable until 2.2 promotion completes.  
**Target:** Glaze UI 2.2.0 Candidate refinement.

## Direction

Glaze UI 2.2 combines two families of interaction principles into an original GoreeCloud system:

1. **Reachable modular UI** — large touchable controls, deliberate grouping, adaptive layouts, floating/split views, thumb-friendly mobile placement, clear selected states, and strong form-factor adaptation.
2. **Optical Glaze** — translucent interaction chrome, layered foreground/background separation, bright optical edges, restrained internal highlights, soft depth shadows, context-aware tint, and continuous capsule/morph identities.

The result must be recognizably GoreeCloud. It must not reproduce Samsung or Apple layouts, icons, branding, proprietary assets, or exact component geometry.

The current external reference direction is broadly informed by contemporary One UI 8.5 reachability/modularity and modern layered-glass interfaces. These references are inspiration only; the implementation is governed by GoreeCloud contracts, semantics, accessibility rules, performance limits, and identity.

## Core composition rule

> **Content is calm and structurally solid. Interaction is layered, reachable, and glazed.**

Durable reading/editing surfaces remain visually stable. Navigation, command bars, search, temporary controls, active selections, live status, and system panels may use optical Glaze where it improves hierarchy.

## Required visual characteristics

### 1. Sculpted interaction chrome

Primary system controls use generous rounded geometry rather than small rectangular controls.

- standard interactive radius: approximately 18–24 px depending on size;
- dominant floating panels: approximately 28–34 px;
- navigation/status capsules: pill geometry where identity is continuous;
- 48 px default target floor;
- 56 px Touch Assistance floor.

Rounded geometry must never reduce usable target size or create decorative ambiguity.

### 2. Optical edge construction

Glazed surfaces use a three-part depth cue:

- a subtle bright upper/near edge;
- a restrained internal highlight or lower-edge shade;
- a soft external depth shadow.

This replaces flat translucent rectangles with more tangible optical surfaces without requiring physically accurate refraction.

### 3. Layer hierarchy

The intended visual hierarchy is:

**Wallpaper / Ambient Field → Durable Content → Application Chrome → Floating Interaction → System Panel → Critical System**

Higher temporary interaction layers may become more optically distinct, but critical/authentication surfaces remain explicit and solid.

### 4. Selected-state capsules

Navigation and selection must be obvious without relying on color alone.

A selected item should combine:

- contained/capsule geometry;
- semantic or accent tint;
- a visible edge/ring or fill difference;
- preserved label/icon identity.

Core navigation destinations do not move when contextual tools appear.

### 5. Reachability and adaptive placement

Mobile layouts prioritize the reachable half of the screen for common actions when context permits. Large text may stack controls and convert horizontal tool groups into vertical modules.

Tablet/desktop layouts may use floating views, sidebars, docks, split panes, and layered command surfaces while preserving the same semantic hierarchy.

### 6. Context-aware glass

Optical surfaces may derive subtle tint from nearby content, application identity, or semantic accent, but semantic colors stay authoritative.

Glass must not wash out:

- critical/destructive color;
- success/warning state;
- active privacy/recording state;
- current selection;
- focus indication.

### 7. Motion

Motion reinforces connected transformation and continuity rather than spectacle.

- direct manipulation remains immediate;
- panels expand/contract from their invoking identity where practical;
- selection capsules move continuously rather than teleporting;
- Reduced Motion removes nonessential spatial/depth motion.

### 8. Accessibility precedence

The visual direction is invalid if it depends on blur, translucency, low contrast, or motion for meaning.

- Reduced Transparency: solid system surfaces, no optical blur dependency;
- Forced Colors: platform colors, no decorative Glaze requirement;
- Increased Contrast: clearer boundaries and focus;
- 200% text: reflow, no clipping, no status/system-bar overlap;
- Touch Assistance: 56 px/dp minimum targets;
- Reduced Motion: direct/crossfade behavior where motion would otherwise convey continuity.

## System-shell application

### Workspace

Use ambient depth and layered application chrome, but keep the primary work canvas readable and calm.

### Universal Search

Treat Search as a strong floating command surface: prominent search capsule, deterministic Best Match first, generously rounded result rows, clear selected state, and generated interpretation visually distinct from source-backed results.

### Control Center

Use large modular controls, strong active/off differentiation, broad range controls, and one dominant panel budget. Mobile modules should favor thumb reachability.

### Intelligence

AI surfaces remain quiet and subordinate to user intent. Generated content can use subtle Aurora/optical treatment, but never default neon/glow effects.

### Critical System

Critical System remains solid, explicit, high-contrast, and visually outside the decorative glass language.

## Performance boundary

This direction does not increase the existing 2.2 blur caps. Optical richness should come first from layering, edge highlights, tint, geometry, and shadow. The established degradation order remains authoritative:

1. remove morphing;
2. remove ambient gradients;
3. remove decorative shadows;
4. reduce blur;
5. preserve semantics, targets, focus, contrast, and legibility.

## Promotion boundary

This document establishes visual direction, not Stable acceptance. Any visual refinement that changes the reviewed presentation invalidates the previous Human Visual Excellence review target and requires new exact-revision visual evidence before Glaze UI 2.2 can become Stable.
