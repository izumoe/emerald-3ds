# Upstream pull request review

Review of open ZallaxDev/emerald-3ds pull requests on 2026-11-12 for the cinematic-camera fork. Changes were cherry-picked individually to avoid bringing unrelated branch history into the fork.

| PR | Decision | Reason |
|---|---|---|
| [#263](https://github.com/ZallaxDev/emerald-3ds/pull/263), [#262](https://github.com/ZallaxDev/emerald-3ds/pull/262) | Not applicable yet | These test fixtures target newer renderer changes; this fork's corresponding runtime and draft tests already pass. |
| [#261](https://github.com/ZallaxDev/emerald-3ds/pull/261) | Applied | Friendlier message for a mistaken Pinball ROM. |
| [#210](https://github.com/ZallaxDev/emerald-3ds/pull/210), [#208](https://github.com/ZallaxDev/emerald-3ds/pull/208), [#207](https://github.com/ZallaxDev/emerald-3ds/pull/207), [#206](https://github.com/ZallaxDev/emerald-3ds/pull/206) | Applied | Four dependent sets of interior model corrections, including the Elite Four rooms. Status table conflicts were reconciled with this fork's later outdoor review notes. |
| [#209](https://github.com/ZallaxDev/emerald-3ds/pull/209) | Deferred | Useful startup translations, but conflicts with this fork's data error handling and needs a separate locale review. |
| [#199](https://github.com/ZallaxDev/emerald-3ds/pull/199) | Applied | Avoids black walls around underground rooms. |
| [#190](https://github.com/ZallaxDev/emerald-3ds/pull/190) | Applied | Clearer Linux and macOS installation instructions and corrected links. |
| [#148](https://github.com/ZallaxDev/emerald-3ds/pull/148) | Deferred | Large conflicting introduction and naming UI change; needs touch-screen and localization testing. |
| [#140](https://github.com/ZallaxDev/emerald-3ds/pull/140) | Deferred | Conflicting RNG and settings change depends on the earlier RNG implementation; needs gameplay and save-settings review. |
| [#122](https://github.com/ZallaxDev/emerald-3ds/pull/122) | Deferred | Optional battle crop cuts off the sides of the scene; needs separate double-battle and UI review. |
| [#111](https://github.com/ZallaxDev/emerald-3ds/pull/111) | Deferred | Worth revisiting, but conflicts with the current terrain renderer and changes coastal height and battle staging. Upstream also calls for coastal visual and hardware testing. |
| [#70](https://github.com/ZallaxDev/emerald-3ds/pull/70) | Deferred | Useful model ideas, but the older generator conflicts and some models, including Sootopolis houses, now overlap existing fork geometry. Port remaining placements individually after checking overlap. |
| [#68](https://github.com/ZallaxDev/emerald-3ds/pull/68) | Deferred | Large stereoscopic battle feature with hardware dependencies and optional external data packs; requires separate hardware and battle testing. |
| [#39](https://github.com/ZallaxDev/emerald-3ds/pull/39) | Deferred | macOS release packaging conflicts with the newer multilingual release script and needs testing on macOS. |
