# Glaze UI Visual Identity Contract

Status: **Pending approved canonical artwork**

Glaze UI 1.4.0 is the current Stable GoreeCloud design-system baseline. Its public design site currently uses a text-first identity. No icon, logo, favicon, or product mark is approved as canonical Glaze UI artwork at this time.

## Purpose

This document defines the acceptance boundary for future Glaze UI visual identity work. Artwork must be reviewed as a distinct identity project and must not become canonical merely because it is committed, generated, rendered, or displayed on the public website.

## Identity role

Glaze UI is a GoreeCloud platform/design-system identity, not an ordinary Suite application. Its mark should communicate a reusable visual and interaction language: layered hierarchy, selective translucency, calm structure, expressive geometry where meaningful, adaptive composition, accessibility, privacy, and resilience.

The mark must remain visually distinct from:

- the GoreeCloud platform logo;
- GoreeCloud Browser;
- Privacy Shield;
- Wardveil Security;
- ordinary GoreeCloud application icons;
- common vendor or platform marks, including obvious Google-style or generic lettermark treatments.

## Required qualities

A candidate must:

- use original GoreeCloud-controlled artwork;
- have a distinctive primary symbol recognizable by shape or concept rather than color alone;
- remain understandable without accompanying text;
- remain recognizable at compact 16–24 px presentation sizes;
- work in light and dark Glaze UI environments;
- support full-color and monochrome presentation;
- use clean scalable vector geometry;
- avoid unnecessary detail that collapses at small sizes;
- remain compatible with Glaze UI geometry, depth, rendering treatment, and family character without becoming interchangeable with other GoreeCloud identities;
- contain no scriptable SVG behavior, embedded remote resources, or external runtime dependencies.

## Rejected directions

The following are not acceptable as final Glaze UI identity without an explicit exception:

- a plain letter G or GU monogram;
- a GoreeCloud platform-logo derivative used as the primary symbol;
- a generic rounded gradient square;
- a generic ring, loop, orb, sparkle, droplet, shield, checkmark, or glass pane with no distinctive Glaze-specific concept;
- recoloring an existing GoreeCloud product symbol;
- a mark that reads primarily as Google, Material Design, Apple, Samsung, Firefox, or another external product/vendor identity;
- automatically generated artwork that has not been visually reviewed and explicitly approved.

The previously tested G-shaped rounded-loop mark is explicitly rejected and must not be restored as canonical artwork.

## Candidate workflow

1. Develop multiple materially different concepts rather than near-identical color or geometry variants.
2. Store candidates under a non-canonical review path.
3. Render each candidate at large presentation size and at practical small icon sizes.
4. Review light, dark, and monochrome presentation.
5. Review distinction from the GoreeCloud platform logo, Browser, Privacy Shield, Wardveil Security, and nearby Suite identities.
6. Record explicit administrator approval for the exact selected candidate bytes.
7. Only after approval, promote the exact reviewed source to the canonical identity path and derive favicon/platform representations from that source.
8. Bind canonical and generated assets to recorded hashes and validate that derivatives remain traceable to the approved source.

## Canonical path boundary

Until explicit approval occurs, no canonical Glaze UI artwork path is authorized for production use. The public design site must remain text-first and must not ship an unapproved favicon or identity mark as a substitute.

When artwork is approved, the repository should establish an authoritative scalable source under a documented `branding/` path, plus reproducibly derived web representations appropriate to the supported public surfaces.

## Approval criteria

Visual approval must confirm all of the following:

- distinctive concept and silhouette;
- small-size legibility;
- light/dark usability;
- monochrome viability;
- Glaze UI family coherence;
- separation from GoreeCloud platform, product, privacy, and security identities;
- no obvious external-vendor resemblance;
- technical SVG safety and portability;
- exact source/derivative traceability;
- explicit administrator acceptance.

Technical validation is necessary but does not constitute aesthetic approval.

## Current public-site state

`design.goreecloud.com` intentionally uses the text identity `GoreeCloud · Glaze UI` and no canonical Glaze UI icon. That is the approved interim state until this contract is satisfied.