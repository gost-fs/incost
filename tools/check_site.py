#!/usr/bin/env python3
"""Whole-site check for incost.app. Run before every push:  python3 tools/check_site.py
Exit code 0 = all good, 1 = something to fix (each problem is printed as FAIL ...).

Checks:
  1. sitemap.xml lists every indexable page, and every <loc> exists
  2. local links and images (href/src) point to files that exist
  3. <link rel="canonical"> matches the file name
  4. every page has the visit counter; every download button has the data-dl beacon
  5. translations: each data-i key exists in uk, de, es, pl; MODS has the same cards in all 5 languages;
     every card key in FGK exists in MODS
  6. generated pages are up to date (gen_calculators.py, gen_charts.py, gen_features.py run in a temp copy → no difference)
"""
import os, re, sys, glob, shutil, tempfile, subprocess, filecmp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://incost.app/'
LANGS = ['en', 'uk', 'de', 'es', 'pl']
fails = 0


def fail(msg):
    global fails
    fails += 1
    print('FAIL', msg)


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8').read()


pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, '*.html')))
src = {p: rd(p) for p in pages}

# 1. sitemap
locs = re.findall(r'<loc>([^<]+)</loc>', rd('sitemap.xml'))
in_map = set()
for u in locs:
    f = 'index.html' if u == BASE else u.replace(BASE, '')
    in_map.add(f)
    if f not in src:
        fail(f'sitemap: {u} has no file')
for p, s in src.items():
    noindex = re.search(r'<meta name="robots" content="[^"]*noindex', s)
    if not noindex and p not in in_map:
        fail(f'sitemap: {p} is indexable but missing from sitemap.xml')
    if noindex and p in in_map:
        fail(f'sitemap: {p} is noindex but listed in sitemap.xml')

# 2. local links
for p, s in src.items():
    markup = re.sub(r'<script\b.*?</script>', '', s, flags=re.S)
    for t in re.findall(r'(?:href|src)="([^"#?]+)', markup):
        if re.match(r'^(https?:|mailto:|tel:|data:|javascript:|//)', t) or t in ('./', '/'):
            continue
        if not os.path.exists(os.path.join(ROOT, t.lstrip('/'))):
            fail(f'link: {p} → {t} (file does not exist)')

# 3. canonical
for p, s in src.items():
    m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    want = BASE if p == 'index.html' else BASE + p
    if not m:
        fail(f'canonical: {p} has none')
    elif m.group(1) != want:
        fail(f'canonical: {p} is {m.group(1)}, expected {want}')

# 4. analytics
for p, s in src.items():
    if 'api.incost.app/hit' not in s:
        fail(f'analytics: {p} has no visit counter (api.incost.app/hit)')
    for a in re.findall(r'<a [^>]*InCost-win\.zip[^>]*>', s):
        if 'data-dl' not in a:
            fail(f'analytics: {p} download link without data-dl: {a[:90]}')

# 5. translations (index.html and features.html share the same script)
for p in ('index.html', 'features.html'):
    s = src[p]
    for k in sorted(set(re.findall(r'data-i="([^"]+)"', s))):
        n = s.count(f'"{k}":')
        if n < len(LANGS) - 1:
            fail(f'i18n: {p} key "{k}" translated {n}× (need uk, de, es, pl)')
    i, j = s.find('var MODS='), s.find('var FGK=')
    if i < 0 or j < 0:
        continue
    block = s[i:j]
    starts = [(l, block.find(('\n    ' if l != 'en' else '') + l + ':[')) for l in LANGS]
    keys = {}
    for n, (l, a) in enumerate(starts):
        b = starts[n + 1][1] if n + 1 < len(starts) else len(block)
        keys[l] = re.findall(r'\["([a-z0-9]+)",', block[a:b])
    for l in LANGS[1:]:
        if set(keys[l]) != set(keys['en']):
            fail(f'i18n: {p} MODS {l} differs from en: missing {sorted(set(keys["en"]) - set(keys[l]))}, '
                 f'extra {sorted(set(keys[l]) - set(keys["en"]))}')
    fgk = s[j:s.index('};', j)]
    for k in re.findall(r'"([a-z0-9]+)"', ''.join(re.findall(r'\[([^\]]*)\]', fgk))):
        if k not in keys['en']:
            fail(f'i18n: {p} FGK lists "{k}" but MODS has no such card')

# 6. generated pages are fresh
tmp = tempfile.mkdtemp()
try:
    work = os.path.join(tmp, 'site')
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns('.git', '.claude'))
    for script in ('gen_calculators.py', 'gen_charts.py', 'gen_features.py'):
        r = subprocess.run([sys.executable, '-I', os.path.join(work, 'tools', script), *(['.'] if script == 'gen_calculators.py' else [])], cwd=work,
                           capture_output=True, text=True)
        if r.returncode:
            fail(f'generate: {script} failed: {(r.stderr or r.stdout).strip().splitlines()[-1:]}')
    for p in pages:
        if not filecmp.cmp(os.path.join(ROOT, p), os.path.join(work, p), shallow=False):
            fail(f'generate: {p} is out of date — run the generator (see CLAUDE.md) and commit the result')
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f'check_site: {len(pages)} pages, {"OK" if not fails else str(fails) + " problem(s)"}')
sys.exit(1 if fails else 0)
