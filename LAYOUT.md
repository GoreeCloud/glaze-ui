# GLAZE UI V1.0 — Layout

**Lifecycle boundary:** GLAZE UI V1.0 remains the current official baseline. Production-readiness claims require exact-revision revalidation; this layout contract does not independently establish Stable release or production acceptance.

V1 layout prioritizes task hierarchy, reachability, readable density, responsive adaptation, and predictable spatial relationships. Durable content uses stable surfaces; transient navigation and controls may use bounded Glaze where contrast and performance remain acceptable.

Layouts must tolerate large text, RTL, keyboard focus, touch assistance, split/foldable postures, resizing, and platform safe areas without clipping critical actions or creating inaccessible interaction targets.

The canonical spacing scale is 2, 4, 8, 12, 16, 24, 32, 48, 64, and 96px, with semantic roles for hairline, control, cluster, content, section, region, and page spacing. Responsive gutters are 16px compact, 24px medium, 32px expanded, and 48px large-screen unless a more specific platform contract governs.

Density modifies inter-element spacing and padding only; it must not shrink required accessibility targets, change semantic order, or use viewport width alone as a proxy for user intent. Compact and spacious density preserve minimum interactive targets.

Horizontal scrolling is reserved for content that is semantically horizontal, such as wide data, timelines, or deliberately scrollable rails. Root-level horizontal overflow is forbidden. Ordinary responsive layouts must reflow rather than hiding critical content outside the viewport.

Layout and focus order must remain semantically aligned. Large text and localization expansion must reflow without clipping important content. Safe areas and platform insets are first-class constraints rather than decorative padding.

Glaze UI owns layout, spacing, density, and responsive presentation. Privacy Shield remains authoritative for privacy truth, Wardveil Security for security truth, Everkeep for resilience truth, and GoreeCloud Mesh for coordination truth. Layout must surface those producer-authoritative states without manufacturing or reinterpreting them.
