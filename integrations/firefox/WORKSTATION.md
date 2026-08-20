# Firefox Glaze UI Workstation Acceptance Target

## Purpose

This document records the primary GoreeCloud Linux workstation target for Firefox Glaze UI runtime acceptance. It does not represent a passed runtime test. Actual Release and ESR results must still be recorded through `ACCEPTANCE.md` and `collect_acceptance.py`.

## Target Workstation

| Item | Target |
| --- | --- |
| Device | Lenovo IdeaPad 3 15IIL05 |
| Processor | Intel Core i3-1005G1, 10th Generation |
| Memory | 8 GB RAM |
| Graphics | Intel UHD Graphics, Ice Lake GT1 |
| Storage | 256 GB SSD |
| Operating system | Zorin OS 17.3 Pro |
| Architecture | 64-bit |
| Display server | Wayland |

## Acceptance Philosophy

The workstation is a dependable daily-use system rather than an experimental desktop-customization platform. Firefox Glaze acceptance must therefore prefer conservative, reversible changes and low operational overhead.

The runtime test must:

- Use the supported Firefox theme as the primary layer.
- Treat `userChrome.css` as optional and removable.
- Require an explicitly selected Firefox profile path before copying or removing `userChrome.css`.
- Avoid modifying unrelated desktop settings, Wayland configuration, graphics configuration, system services, or Firefox profile data.
- Avoid running unnecessary background tools during acceptance on the 8 GB system.
- Preserve Firefox security, identity, permissions, update, private-browsing, certificate, warning, and download indicators.
- Record failures instead of compensating with unsupported security or browser-behavior changes.

## Recommended Test Order

1. Update Zorin OS and the intended Firefox installation through its normal trusted update path.
2. Close unnecessary applications and browser sessions before testing to reduce memory pressure.
3. Record the exact Firefox Release or ESR version.
4. Build the deterministic local theme package and record its SHA-256.
5. Test the supported theme layer first, without `userChrome.css`.
6. Complete light/dark, tabs, URL/search, menus/panels, bookmarks, sidebar, downloads, private browsing, security/identity indicators, keyboard focus, reduced motion, contrast/forced-colors where available, and rollback checks.
7. Only after the supported theme passes, explicitly enable and install the optional `userChrome.css` layer for deeper chrome testing.
8. Repeat the browser-chrome and accessibility checks with `userChrome.css` enabled.
9. Remove `userChrome.css`, restart Firefox, and verify the supported theme still operates independently.
10. Remove the theme and confirm ordinary Firefox appearance and profile data are intact.

## Wayland and Graphics Checks

Because the target uses Wayland and Intel UHD graphics, acceptance should explicitly note any visual artifacts involving translucent navigation chrome, popup layering, URL-bar focus treatment, tab painting, scaling, window maximization, fullscreen transitions, or display-server-specific rendering. If translucency produces instability or unreadable rendering, the Glaze solid fallback is preferred over compositor or graphics-driver workarounds.

## Performance Checks

The customization should not create noticeable idle CPU load or browser-chrome responsiveness regressions. Testing should compare ordinary Firefox against the supported theme and then against the optional `userChrome.css` layer using normal browsing behavior rather than synthetic stress workloads. Any material responsiveness or memory regression attributable to the optional layer is grounds to keep that layer disabled while retaining the supported theme.

## Acceptance Boundary

Passing on this workstation establishes the primary GoreeCloud Linux workstation result for the tested Firefox version only. Firefox Release and ESR remain separate tracks, and later browser or operating-system updates may require revalidation because `userChrome.css` relies on browser-chrome selectors that Mozilla does not expose as a stable public API.
