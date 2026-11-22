---
name: site-check
description: Full pre-publish check of incost.app — run before any push to main or when asked to "check the site". Runs the automatic checks, then reviews US-market copy, prices and translations.
---

# Site check before publishing

1. Run the automatic checks and fix every FAIL:
   ```
   python3 tools/check_site.py
   python3 tools/check_charts.py
   ```
2. Look at what changed: `git status` and `git diff --stat`, then read the diff of each changed page.
3. For each changed page, check by hand:
   - **US English** spelling (aluminum, color, center, gauge) and US units first (in, lb, ga, $).
   - Prices and the Free/Pro split match between `index.html` (pricing section) and `features.html`.
     The Freemius checkout is still wired up (`freemius.com/js/v1/`).
   - Download buttons point to `releases/latest/download/InCost-win.zip` and have `data-dl`.
   - Every changed English string is also changed in **uk, de, es, pl** (`data-i` dictionaries and `MODS`).
     The translations should mean the same thing, not just exist.
   - Savings and accuracy numbers are honest and come from what the app really does.
   - `lastmod` in `sitemap.xml` is updated for each changed page.
4. Report: a short list of what you checked, what you fixed, and anything the owner has to decide
   (copy, prices, claims). Do not push — the owner pushes.
