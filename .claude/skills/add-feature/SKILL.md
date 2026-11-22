---
name: add-feature
description: Add or change a feature card on incost.app (home page + features.html) in all 5 site languages. Use when a new InCost app feature should appear on the website.
---

# Add a feature card

Feature cards are rendered by the shared script in `index.html` from `var MODS`, grouped by `var FGK`.
`features.html` is generated from `index.html`, so never edit it by hand.

1. Ask (or take from the request) what the feature does, who it is for, and whether it is **Free or Pro**.
   Don't make up capabilities — if unsure what the app does, ask.
2. Pick a short lowercase key (`[a-z0-9]+`) that no other card uses. Check with `grep -o '\["KEY",' index.html`.
3. In `index.html`, add `["key","Title","Text"]` to **every** language array in `MODS`: `en`, `uk`, `de`, `es`, `pl`,
   at the same position in each.
   - en: US English, shop-floor wording, one or two sentences, concrete (what you open → what you get).
   - uk/de/es/pl: natural translations, the same meaning and the same units.
4. Put the key into the right group in `FGK` (`quote`, `sheet`, `3d`, `design`, `shop`, …). Otherwise it lands in "More".
5. Pro items are marked by appending the `PRO` badge variable to the string (`"Automatic nesting ..."+PRO`).
   Check how nearby Pro items are marked and do the same in all 5 languages.
6. The post-edit hook regenerates `features.html`. If hooks are off, run `python3 tools/gen_features.py`.
7. Update `lastmod` for `/` and `/features.html` in `sitemap.xml`, then run `python3 tools/check_site.py`.
8. Show the owner the English text and the list of changed files.
