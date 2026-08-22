# Glaze Sans Visual Review

Status: Experimental review protocol

This checklist is intentionally stricter than a font build succeeding. A Glaze Sans candidate must be visually convincing in real GoreeCloud interface conditions before it can become Candidate or Stable.

## Review sequence

### 1. Word recognition

Review familiar English text at normal UI sizes before inspecting stylistic details.

Required specimen phrases include:

- GoreeCloud — private, polished, independent.
- The quick brown fox jumps over 13 lazy dogs.
- Calendar · Contacts · Notes · Tasks · Search
- Security, privacy, recovery, and control.
- Beautiful defaults. Advanced control when needed.

Pass condition: words are recognized immediately and no letter appears constructed, handwritten, symbolic, or ambiguous.

### 2. UI-size review

Review at representative CSS-equivalent sizes:

- 12–13 px metadata/caption
- 14–16 px dense UI/body
- 17–20 px prominent labels and titles
- 24–32 px section headings
- 40–64 px display/hero text

Pass condition: counters remain open, spacing remains calm, and rounded details do not blur or disappear unpredictably.

### 3. Confusing-glyph review

Explicitly compare:

`I l 1 | O 0 | rn m | cl d | a o | c e | 5 S | 2 Z | 6 G | 8 B`

Pass condition: each pair or cluster remains distinguishable without context.

### 4. Weight progression

Review 400, 500, 600, 700, and 800 together.

Pass condition:

- weights become progressively stronger without sudden width jumps;
- Regular is not fragile;
- Medium is visibly distinct from Regular;
- SemiBold remains useful for interface emphasis;
- Bold is strong without losing counters;
- ExtraBold remains readable and does not become a novelty display face.

### 5. Rounded-character review

Rounded character should appear primarily through terminals, joins, bowls, shoulders, punctuation, and selected signatures rather than through inflated circular proportions.

Pass condition: the family feels softer than a generic grotesk but less playful than a geometric bubble font.

### 6. Product-context review

Render the same candidate in representative GoreeCloud contexts:

- application navigation;
- settings forms;
- data tables and dashboards;
- notes and body copy;
- calendar labels;
- media titles;
- security/privacy surfaces;
- public website hero copy;
- Android/mobile UI;
- desktop UI;
- TV/far-view UI where applicable.

Pass condition: the family improves the experience without reducing clarity or product-specific personality.

### 7. Accessibility and resilience

Review high zoom, high DPI, forced-colors/high-contrast contexts where the platform exposes them, reduced-transparency surfaces, and common rasterization environments.

Pass condition: no styling decision depends on translucency, color, antialiasing quirks, or subpixel rendering to make the text legible.

## Automatic rejection conditions

Reject the candidate if any of the following occur:

- ordinary Latin text resembles handwriting, symbols, pseudo-language, or a constructed alphabet;
- rounded forms make the typeface look childish, bubbly, toy-like, or casual;
- the family is visually indistinguishable from its scaffold/reference with only a renamed metadata table;
- spacing or kerning produces visibly irregular word texture;
- a distinctive glyph is difficult to identify without context;
- body text is less readable than the current Glaze UI system-font fallback;
- a third-party network dependency is required to render the font;
- provenance or license obligations are unclear.

## Human approval gate

The GoreeCloud owner must explicitly approve the visual direction before Glaze Sans can advance from Experimental to Candidate. Automated font QA can detect technical defects, but it cannot replace this visual acceptance decision.
