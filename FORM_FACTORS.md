# GLAZE UI V1.0 — Form Factors

GLAZE UI V1.0 is adaptive rather than layout-identical across devices. Supported mappings may include mobile, tablet, desktop, TV/far-view, watch, foldable, and other user-facing platforms where an accepted platform contract exists.

Core rules: preserve semantic hierarchy; adapt navigation and density to reachability and viewing distance; use at least 48 px touch targets and 56 px for Touch Assistance/far-view where applicable; support keyboard, pointer, touch, and assistive input; and prefer stable solid reading surfaces when performance or accessibility makes Glaze effects inappropriate.

## Mobile Web Priority

Mobile is the highest-priority visual acceptance surface for GoreeCloud websites that can reasonably be used on a phone. A desktop or tablet composition that merely fits inside a narrow viewport is not a Mobile UI.

A conforming Mobile UI must intentionally transform navigation, typography, hierarchy, spacing, density, controls, reading surfaces, safe-area behavior, and touch ergonomics for narrow portrait use. Disproportionate navigation chrome, viewport-filled marketing or documentation blocks, oversized headings or cards, excessive empty vertical space, edge-aligned control labels, horizontal page scrolling, and compressed desktop composition are release-blocking mobile defects.

Exact-revision mobile acceptance requires rendered browser evidence at representative narrow portrait widths, including a 320 px-class viewport and at least one modern phone-width viewport, plus supported appearance modes. Automated source or breakpoint inspection may supplement but does not replace rendered visual review.

A platform is not production-supported until its V1 evidence is accepted. A website is not production-complete when desktop or tablet acceptance passes but the Mobile UI remains materially unpolished, awkward, incomplete, or visually degraded.
