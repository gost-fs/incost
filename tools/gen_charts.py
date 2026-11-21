#!/usr/bin/env python3
"""Reference chart pages for incost.app (SEO): metric threads, tap drills, sheet metal gauges, clearance holes,
ISO 2768 tolerances, ball bearing sizes, steel grade equivalents, equal angle weights.
Data: tools/charts-data.json — exported from the InCost app library (the same tables the app uses).
Run: python3 tools/gen_charts.py   (writes the pages to the site root). Check: python3 tools/check_charts.py"""
import json, os, re, html, math

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = open(os.path.join(ROOT, 'tools', 'gen_calculators.py'), encoding='utf-8').read()
ns = {}
exec(SRC[:SRC.index('def page(')], ns)  # CSS, LOGO, BASE, DL, PAGES (calculators)
CSS, LOGO, BASE, DL, CALCS = ns['CSS'], ns['LOGO'], ns['BASE'], ns['DL'], ns['PAGES']
D = json.load(open(os.path.join(ROOT, 'tools', 'charts-data.json'), encoding='utf-8'))
E = html.escape

CSS += r'''
.tbl.wide table{min-width:720px}
.tbl td,.tbl th{font-variant-numeric:tabular-nums}
.tbl td.n,.tbl th.n{text-align:right;white-space:nowrap}
.tbl tbody tr:hover td{background:var(--bg-2)}
.tbl caption{caption-side:bottom;text-align:left;padding:8px 12px;font-size:13px;color:var(--ink-2)}
.find{display:flex;gap:10px;align-items:center;margin:22px 0 4px;flex-wrap:wrap}
.find input{min-height:42px;font:16px var(--font);padding:0 12px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink);width:min(320px,100%)}
.find input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.find small{color:var(--ink-2);font-size:13px}
.src{font-size:14px;color:var(--ink-2);border-left:3px solid var(--line);padding:4px 0 4px 12px;margin:14px 0}
.mk{color:var(--bad);font-weight:700}
main>h2.sec{font-size:26px;margin:40px 0 4px}
'''

def f(v, d=2):
    """number → text with up to d decimals, trailing zeros trimmed"""
    s = f'{v:.{d}f}'
    return s.rstrip('0').rstrip('.') if '.' in s else s

def table(head, rows, num_from=1, caption='', wide=False, tid=''):
    th = ''.join(f'<th{" class=\"n\"" if i >= num_from else ""} scope="col">{h}</th>' for i, h in enumerate(head))
    tb = ''.join('<tr>' + ''.join(f'<td{" class=\"n\"" if i >= num_from else ""}>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    cap = f'<caption>{caption}</caption>' if caption else ''
    return f'<div class="tbl{" wide" if wide else ""}"><table{f" id=\"{tid}\"" if tid else ""}>{cap}<thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'

FIND_JS = r'''
var q=document.getElementById("q");if(q){q.addEventListener("input",function(){var v=q.value.trim().toLowerCase().replace(/\s+/g,"");
[].forEach.call(document.querySelectorAll(".tbl tbody tr"),function(tr){tr.hidden=v&&tr.textContent.toLowerCase().replace(/\s+/g,"").indexOf(v)<0})})}
'''
def finder(ph):
    return f'<div class="find"><input id="q" type="search" placeholder="{E(ph)}" aria-label="{E(ph)}" autocomplete="off"><small>Filters every table on this page</small></div>'

TAIL = '''<script>document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[data-dl]");if(!a)return;try{navigator.sendBeacon("https://api.incost.app/dl?src="+encodeURIComponent(a.getAttribute("data-dl")),"")}catch(x){}});</script>
'''
# the visit counter and the phone handling are copied verbatim from a calculator page, so every page behaves the same
_calc = open(os.path.join(ROOT, 'metal-weight-calculator.html'), encoding='utf-8').read()
_i = _calc.index('<script>document.addEventListener("click"'); _j = _calc.rindex('</body>')
TAIL = _calc[_i:_j]

CHARTS = []  # (file, title, short)

def page(fname, title, h1, lead, body, faqs, meta_desc, seo_title, dl_src, article=''):
    others = [c for c in CHARTS if c[0] != fname]
    links = ''.join(f'<a href="{c[0]}"><b>{E(c[1])}</b><span>{E(c[2])}</span></a>' for c in others)
    calcs = ''.join(f'<a href="{p[0]}"><b>{E(p[1])}</b><span>{E(p[2])}</span></a>' for p in CALCS)
    strip = lambda s: re.sub('<[^>]+>', '', s)
    faq_html = ''.join(f'<details><summary>{E(q)}</summary><p>{a}</p></details>' for q, a in faqs)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": seo_title, "url": BASE + fname, "description": meta_desc, "inLanguage": "en",
         "isPartOf": {"@type": "WebSite", "name": "InCost", "url": BASE}, "dateModified": "2026-11-21"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "InCost", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Reference charts", "item": BASE + "#tools"},
            {"@type": "ListItem", "position": 3, "name": title, "item": BASE + fname}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}]}
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(seo_title)}</title>
<meta name="description" content="{E(meta_desc)}">
<link rel="canonical" href="{BASE}{fname}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#0B5CFF">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:site_name" content="InCost">
<meta property="og:url" content="{BASE}{fname}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(meta_desc)}">
<meta property="og:image" content="{BASE}og.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="wrap nav">
<a class="logo" href="./">{LOGO}InCost</a><span class="sp"></span>
<a class="lnk" href="./#tools">Charts &amp; calculators</a><a class="lnk" href="./#pricing">Pricing</a>
<a class="btn btn-primary" href="./#get">Download InCost</a>
</div></header>
<main class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="./">InCost</a> › <a href="./#tools">Reference charts</a> › {E(title)}</nav>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
{body}
<section class="cta">
<div><h2>These tables, plus the price of the part</h2><p>InCost has these charts built in — and uses them: tap holes found in your DXF go into the price and the routing card, fasteners go into the bill of materials at your prices, sheet gauge sets the cutting time. Free for Windows.</p></div>
<a class="btn btn-primary" href="{DL}" data-dl="{dl_src}">Download free for Windows</a>
</section>
<article>
{article}
<h2 id="faq">Frequently asked questions</h2>
<div class="faq">{faq_html}</div>
</article>
<h2 style="font-size:26px;margin-top:48px">More reference charts</h2>
<div class="tools">{links}</div>
<h2 style="font-size:26px;margin-top:8px">Free calculators</h2>
<div class="tools">{calcs}</div>
</main>
<footer><div class="wrap foot"><span>© 2026 InCost · hello@incost.app</span>
<nav><a href="./">Home</a><a href="./#tools">Charts &amp; calculators</a><a href="terms.html">Terms</a><a href="privacy.html">Privacy</a></nav></div></footer>
<script>(function(){{{FIND_JS}}})();</script>
{TAIL}</body>
</html>
'''

# ---------------------------------------------------------------- data helpers
THR = D['THR']
def thr_rows():
    for k, r in THR.items():
        d = float(k[1:]); P = r[0]
        d2 = d - 0.649519 * P; d3 = d - 1.226869 * P; D1 = d - 1.082532 * P
        As = math.pi / 4 * ((d2 + d3) / 2) ** 2
        yield k, d, P, r[1], d2, d3, D1, As, r
TAPM = {t[0]: t[2] for t in D['TAP_DRILL']}
def tap_mm(d, P):
    return TAPM.get(d, d - P) if abs(P - THR['M' + f(d)][0]) < 1e-9 else round(d - P, 2)
def frac(x):
    return x

# ---------------------------------------------------------------- 1. metric threads
def p_threads():
    rows = []
    for k, d, P, fine, d2, d3, D1, As, r in thr_rows():
        rows.append([f'<b>{k}</b>', f(P), ' · '.join(f(x) for x in fine), f'{d2:.3f}', f'{d3:.3f}', f'{D1:.3f}', f(tap_mm(d, P), 2), f'{As:.1f}', f(r[3]), f(r[4])])
    body = finder('Find a size, e.g. M8') + table(['Size', 'Coarse pitch P', 'Fine pitches', 'Pitch dia. d2', 'Minor dia. d3 (bolt)', 'Minor dia. D1 (nut)', 'Tap drill', 'Stress area As, mm²', 'Hex AF (ISO 4032)', 'Hex key (ISO 4762)'],
        rows, caption='All dimensions in mm. d2, d3 and D1 are basic dimensions per ISO 724 for the coarse pitch; As per ISO 898-1.', wide=True)
    art = '''<h2>How the numbers are calculated</h2>
<p>ISO 724 gives the basic profile of the metric thread from the nominal diameter <i>d</i> and the pitch <i>P</i>. Every value in the table is calculated from these two numbers, so you can check any row yourself:</p>
<div class="formula">pitch diameter      d2 = d − 0.649519·P
minor diameter bolt d3 = d − 1.226869·P
minor diameter nut  D1 = d − 1.082532·P
stress area         As = π/4 · ((d2 + d3)/2)²
tap drill (rule)    ≈ d − P</div>
<p>Example, M10 × 1.5: d2 = 10 − 0.974 = 9.026 mm, d3 = 8.160 mm, D1 = 8.376 mm, As = 58.0 mm². The tap drill is 8.5 mm.</p>
<h2>Coarse or fine pitch?</h2>
<p>Use the coarse pitch by default: it is faster to assemble, less sensitive to damage and every nut and tap is in stock. Fine pitches give a larger stress area, finer adjustment and better self-locking — use them for thin walls, adjusting screws and high-strength bolts where the extra strength counts.</p>
<h2>Wrench and key sizes</h2>
<p>Hex sizes are the ISO 4032 / ISO 4014 values. Older DIN 934 / DIN 933 hardware uses 17 mm for M10, 19 mm for M12, 22 mm for M14 and 32 mm for M22 — check which standard your supplier delivers.</p>'''
    faqs = [('What is the pitch of an M8 bolt?', 'The coarse (standard) pitch of M8 is 1.25 mm. Fine pitches are 1 mm and 0.75 mm, written as M8×1 or M8×0.75.'),
            ('What size drill for an M10 tap?', '8.5 mm for the standard M10×1.5 thread (d − P). For M10×1.25 use 8.75 mm, for M10×1 use 9 mm.'),
            ('What does M12×1.5 mean?', 'A metric thread with 12 mm nominal diameter and a fine pitch of 1.5 mm. Without the “×P” (just M12) the coarse pitch, 1.75 mm, is meant.'),
            ('What is the stress area used for?', 'The tensile stress area As is the cross-section used to calculate bolt strength: proof load = proof stress × As. For M12, As = 84.3 mm², so an 8.8 bolt (proof stress 580 MPa) carries about 48.9 kN before permanent stretch.')]
    return page('metric-thread-chart.html', 'Metric Thread Chart', 'Metric Thread Chart: pitch, minor diameter, tap drill',
        'ISO metric threads M2 to M48: coarse and fine pitches, pitch and minor diameters, tap drill, tensile stress area, wrench and hex key sizes — in one table.',
        body, faqs, 'Metric thread chart M2–M48 (ISO 261, ISO 724): coarse and fine pitch, pitch diameter, minor diameter, tap drill size, tensile stress area, hex wrench and Allen key size.',
        'Metric Thread Chart M2–M48 — Pitch, Minor Diameter, Tap Drill | InCost', 'chart-thread', art)

# ---------------------------------------------------------------- 2. tap drills
def pct_thread(D_in, tpi, drill_in):
    return (D_in - drill_in) * tpi / 0.01299
def p_tapdrill():
    m = []
    for k, d, P, fine, d2, d3, D1, As, r in thr_rows():
        m.append([f'<b>{k}×{f(P)}</b>', 'coarse', f(tap_mm(d, P), 2), f(tap_mm(d, P) / 25.4, 4)])
        for p in fine:
            m.append([f'{k}×{f(p)}', 'fine', f(d - p, 2), f((d - p) / 25.4, 4)])
    u = []
    for r in D['UNC']:
        name, dn, tc, tf, dc, dfn = r[0], r[1], r[2], r[3], r[4], r[5]
        u.append([f'<b>{name}-{tc} UNC</b>', f(dn, 4), f'{dc[0]}', f(dc[1], 4), f(dc[1] * 25.4, 2), f'{round(pct_thread(dn, tc, dc[1]))}%'])
        u.append([f'{name}-{tf} UNF', f(dn, 4), f'{dfn[0]}', f(dfn[1], 4), f(dfn[1] * 25.4, 2), f'{round(pct_thread(dn, tf, dfn[1]))}%'])
    body = finder('Find a size, e.g. M6 or 1/4') + '<h2 class="sec" id="metric">Metric (ISO)</h2>' + table(['Thread', 'Pitch', 'Tap drill, mm', 'Tap drill, in'], m,
        num_from=2, caption='Cutting taps. Coarse pitch: standard drill sizes (ISO 2306 practice); fine pitch: d − P. Forming taps need a larger drill.') + \
        '<h2 class="sec" id="unified">Unified inch (UNC / UNF)</h2>' + table(['Thread', 'Major dia., in', 'Drill', 'Drill, in', 'Drill, mm', 'Thread %'], u,
        caption='About 75% thread engagement (ASME B1.1 practice). Thread % = (D − drill) × TPI / 0.01299.')
    art = '''<h2>How to choose a tap drill</h2>
<p>For a metric cutting tap the rule is simple: <b>drill = nominal diameter − pitch</b>. M8×1.25 → 6.8 mm, M6×1 → 5 mm. A few sizes are rounded to the nearest standard drill (M12 → 10.2 mm, M2.5 → 2.05 mm).</p>
<p>For inch threads the drill is picked for about 75% of the full thread height — stronger than needed for most joints, but still easy on the tap. The percentage of thread for any drill is:</p>
<div class="formula">thread % = (major diameter − drill diameter) × TPI / 0.01299</div>
<p>Hard or tough materials (stainless, titanium) and deep holes: choose a drill that gives 60–65% of thread. Soft materials and short engagements: 75–80%.</p>
<h2>Forming taps</h2><p>Roll-forming taps do not cut chips and need a larger hole, roughly d − P/2. Use the tap maker’s table for the exact size.</p>'''
    faqs = [('What size drill for an M6 tap?', '5 mm for M6×1 (coarse). For M6×0.75 use 5.25 mm.'),
            ('What drill size for a 1/4-20 tap?', '#7 drill (0.201 in, 5.11 mm) — about 75% thread. A 13/64 in drill (0.203 in) is a close substitute.'),
            ('What drill for M8 tap?', '6.8 mm for M8×1.25. For M8×1 use 7 mm.'),
            ('Why is the tap drill smaller than the bolt?', 'The tap cuts the thread profile into the wall of the hole, so the hole must be about the size of the minor diameter of the thread: nominal diameter minus one pitch.')]
    return page('tap-drill-chart.html', 'Tap Drill Size Chart', 'Tap Drill Size Chart: metric and UNC/UNF',
        'Tap drill sizes for metric coarse and fine threads M2–M48 and Unified inch threads #4 to 1 in, with decimal inch, millimetres and percentage of thread.',
        body, faqs, 'Tap drill size chart for metric (M2–M48, coarse and fine pitch) and UNC/UNF threads (#4–1 in): drill in mm, inch and number/letter drills with thread percentage.',
        'Tap Drill Size Chart — Metric and UNC/UNF Drill Sizes | InCost', 'chart-tap', art)

# ---------------------------------------------------------------- 3. sheet metal gauge
GN = {'steel': 'Steel (MSG)', 'zn': 'Galvanized steel', 'inox': 'Stainless steel', 'al': 'Aluminum (AWG)'}
DENS = {'steel': 7.85, 'zn': 7.85, 'inox': 7.93, 'al': 2.70}
def p_gauge():
    G = D['GAUGES']
    allg = sorted({g[0] for t in G.values() for g in t})
    rows = []
    for n in allg:
        row = [f'<b>{n} ga</b>']
        for fam in GN:
            r = next((x for x in G[fam] if x[0] == n), None)
            row.append(f'{f(r[1], 4)}″<br><small>{f(r[1] * 25.4, 2)} mm</small>' if r else '—')
        rows.append(row)
    w = []
    for fam in GN:
        for n, t in G[fam]:
            mm = t * 25.4; kg = mm * DENS[fam]
            w.append([GN[fam], f'{n} ga', f(t, 4), f(mm, 2), f(kg, 2), f(kg * 0.204816, 3)])
    body = finder('Find a gauge, e.g. 16 ga') + table(['Gauge', *GN.values()], rows, caption='Thickness in inches and millimetres.', wide=True) + \
        '<h2 class="sec" id="weight">Weight per area</h2>' + table(['Material', 'Gauge', 'in', 'mm', 'kg/m²', 'lb/ft²'], w, num_from=2,
        caption='Weight from the nominal thickness and density: steel and galvanized 7.85 g/cm³, stainless 7.93 g/cm³, aluminum 2.70 g/cm³. The nominal Manufacturers’ Standard Gauge weights (41.82 lb/ft² per inch) are about 2.4% higher — they include a rolling allowance.')
    art = '''<h2>Why the same gauge has different thickness</h2>
<p>A gauge number is not a size — it is a convention, and each material has its own:</p>
<ul><li><b>Steel</b> uses the Manufacturers’ Standard Gauge, based on weight: 41.82 lb/ft² for each inch of thickness. 10 ga steel weighs 5.625 lb/ft², so it is 5.625 / 41.82 = 0.1345 in.</li>
<li><b>Galvanized steel</b> adds the zinc coating: 2.5 oz/ft² more weight, so the same gauge is a little thicker (10 ga = 0.1382 in).</li>
<li><b>Stainless steel</b> follows the older US Standard Gauge in fractions of an inch (16 ga = 1/16 in = 0.0625 in).</li>
<li><b>Aluminum</b> uses the American Wire Gauge (Brown &amp; Sharpe): d = 0.005 × 92<sup>(36 − n)/39</sup> in, so 10 ga = 0.1019 in.</li></ul>
<p>Always quote and order sheet by thickness, not gauge — and check the actual thickness with the supplier: mills deliver within a tolerance around the nominal value.</p>'''
    faqs = [('How thick is 16 gauge steel?', '0.0598 in (1.52 mm) for carbon steel. 16 ga stainless is 0.0625 in (1.59 mm), 16 ga aluminum is 0.0508 in (1.29 mm).'),
            ('How thick is 10 gauge steel in mm?', '3.42 mm (0.1345 in). Galvanized 10 ga is 3.51 mm.'),
            ('Is a higher gauge number thicker?', 'No — the higher the gauge number, the thinner the sheet. 22 ga is thinner than 16 ga.'),
            ('What metric thickness is close to 14 gauge?', '14 ga steel is 0.0747 in = 1.90 mm; the nearest common metric sheet is 2 mm.')]
    return page('sheet-metal-gauge-chart.html', 'Sheet Metal Gauge Chart', 'Sheet Metal Gauge Chart: thickness in inches and mm',
        'Gauge to thickness for steel, galvanized steel, stainless steel and aluminum, in inches and millimetres, with weight per square metre and per square foot.',
        body, faqs, 'Sheet metal gauge chart: gauge to thickness (inch and mm) for steel (MSG), galvanized, stainless and aluminum (AWG), with weight in kg/m² and lb/ft².',
        'Sheet Metal Gauge Chart — Gauge to mm and Inches, Steel, Stainless, Aluminum | InCost', 'chart-gauge', art)

# ---------------------------------------------------------------- 4. clearance holes
def p_clear():
    rows = []
    for k, r in THR.items():
        rows.append([f'<b>{k}</b>', f(r[2][0]), f(r[2][1]), f(r[2][2]), f(r[5][0]), f(r[5][1])])
    u = []
    for r in D['UNC']:
        u.append([f'<b>{r[0]}</b>', f(r[1], 4), f'{r[6][0]}', f(r[6][1], 4), f'{r[7][0]}', f(r[7][1], 4), f(r[7][1] * 25.4, 2)])
    body = finder('Find a size, e.g. M10') + '<h2 class="sec" id="metric">Metric: ISO 273</h2>' + table(['Bolt', 'Fine (close)', 'Medium (normal)', 'Coarse (loose)', 'Counterbore Ø', 'Counterbore depth'], rows,
        caption='Clearance hole diameters in mm per ISO 273. Counterbore for socket head cap screws ISO 4762 (Ø and depth for the head to sit flush).') + \
        '<h2 class="sec" id="inch">Inch (UNC/UNF)</h2>' + table(['Screw', 'Major dia., in', 'Close fit drill', 'in', 'Free fit drill', 'in', 'Free fit, mm'], u,
        caption='Close and free fit clearance drills for inch screws (ASME B18.2.8 practice).')
    art = '''<h2>Which series to use</h2>
<ul><li><b>Fine (close)</b> — precise location, few parts, holes drilled or reamed together.</li>
<li><b>Medium (normal)</b> — the default for most machined and laser-cut parts. If a drawing just says “clearance for M8”, use 9 mm.</li>
<li><b>Coarse (loose)</b> — large tolerances, welded frames, holes punched or cut separately in several parts.</li></ul>
<p>On laser-cut parts the medium series is usually right: the kerf and the hole quality on thick plate eat into the close fit.</p>
<h2>Counterbores</h2><p>The counterbore diameter and depth in the table let the head of an ISO 4762 socket head cap screw sit just below the surface. Add a little depth for a washer.</p>'''
    faqs = [('What size clearance hole for M8?', '9 mm for a normal fit (ISO 273 medium), 8.4 mm close fit, 10 mm loose fit.'),
            ('What size clearance hole for M6?', '6.6 mm normal, 6.4 mm close, 7 mm loose.'),
            ('What is the clearance hole for M10?', '11 mm normal (medium), 10.5 mm close (fine), 12 mm loose (coarse).'),
            ('What clearance hole for a 1/4 inch bolt?', 'Close fit: F drill (0.257 in). Free fit: H drill (0.266 in, 6.76 mm).')]
    return page('clearance-hole-chart.html', 'Clearance Hole Chart', 'Clearance Hole Chart: ISO 273 and inch screws',
        'Bolt clearance hole sizes M2–M48 in fine, medium and coarse series per ISO 273, counterbores for socket head cap screws, and close/free fit drills for inch screws.',
        body, faqs, 'Clearance hole chart for metric bolts M2–M48 (ISO 273 fine, medium, coarse), counterbore sizes for ISO 4762 cap screws, and close/free fit drills for UNC/UNF screws.',
        'Clearance Hole Chart — ISO 273 Bolt Hole Sizes M2–M48 and Inch | InCost', 'chart-clear', art)

# ---------------------------------------------------------------- 5. ISO 2768
def rng(r):
    a, b = r
    if b == 'inf': return f'over {f(a)}'
    return f'{f(a)} – {f(b)}' if a else f'up to {f(b)}'
def p_2768():
    T = D['T2768']
    pm = lambda v: '—' if v is None else '±' + f(v)
    lin = [[rng(r), pm(T['lin']['f'][i]), pm(T['lin']['m'][i]), pm(T['lin']['c'][i]), pm(T['lin']['v'][i])] for i, r in enumerate(T['lin']['r'])]
    rad = [[rng(r), pm(T['rad']['f'][i]), pm(T['rad']['m'][i]), pm(T['rad']['c'][i]), pm(T['rad']['v'][i])] for i, r in enumerate(T['rad']['r'])]
    ang = [[rng(r), '±' + T['ang']['f'][i], '±' + T['ang']['m'][i], '±' + T['ang']['c'][i], '±' + T['ang']['v'][i]] for i, r in enumerate(T['ang']['r'])]
    g = lambda key: [[rng(r), f(T[key]['H'][i]), f(T[key]['K'][i]), f(T[key]['L'][i])] for i, r in enumerate(T[key]['r'])]
    hd = ['Nominal size, mm', 'f (fine)', 'm (medium)', 'c (coarse)', 'v (very coarse)']
    body = '<h2 class="sec" id="linear">ISO 2768-1: linear dimensions</h2>' + table(hd, lin, caption='Permissible deviations in mm. “—” means no general tolerance in this class: give the tolerance on the drawing.') + \
        '<h2 class="sec" id="radius">Radii and chamfers</h2>' + table(hd, rad, caption='External radii and chamfer heights, mm.') + \
        '<h2 class="sec" id="angle">Angular dimensions</h2>' + table(['Length of the shorter side, mm', 'f', 'm', 'c', 'v'], ang, caption='Permissible deviations in degrees and minutes.') + \
        '<h2 class="sec" id="geo">ISO 2768-2: geometrical tolerances (H, K, L)</h2>' + table(['Straightness and flatness, length mm', 'H', 'K', 'L'], g('flat'), caption='mm') + \
        table(['Perpendicularity, shorter side mm', 'H', 'K', 'L'], g('perp'), caption='mm') + table(['Symmetry, length mm', 'H', 'K', 'L'], g('sym'), caption='mm') + \
        f'<p class="src">Circular run-out: H {f(T["run"]["H"])} mm, K {f(T["run"]["K"])} mm, L {f(T["run"]["L"])} mm.</p>'
    art = '''<h2>How to read “ISO 2768-mK” on a drawing</h2>
<p>The first letter is the class for linear and angular dimensions (ISO 2768-1), the second — for geometrical tolerances (ISO 2768-2). <b>mK</b> means: medium class for sizes, class K for flatness, straightness, perpendicularity, symmetry and run-out. A 100 mm dimension without its own tolerance may then be 99.7–100.3 mm.</p>
<h2>Which class for which process</h2>
<ul><li><b>f</b> — precision machining, ground parts.</li><li><b>m</b> — normal machining and laser cutting; the most common choice.</li>
<li><b>c</b> — welded frames, plasma cutting, rough machining.</li><li><b>v</b> — rough fabrication, flame cutting, castings before machining.</li></ul>
<p>Tighter general tolerances cost money on every dimension of the part — specify a fine tolerance only on the features that need it, and keep the general class as coarse as the function allows.</p>'''
    faqs = [('What is the ISO 2768-m tolerance for 100 mm?', '±0.3 mm (range 30–120 mm, medium class).'),
            ('What does ISO 2768-mK mean?', 'Medium class (m) for linear and angular dimensions per ISO 2768-1 and class K for geometrical tolerances per ISO 2768-2.'),
            ('What is the general tolerance for a 10 mm dimension in class f?', '±0.1 mm (range 6–30 mm, fine class).'),
            ('Is ISO 2768 still valid?', 'ISO 2768-2 was withdrawn in favour of ISO 22081, but ISO 2768 general tolerances are still widely used on drawings and in shop agreements.')]
    return page('iso-2768-tolerance-chart.html', 'ISO 2768 Tolerance Chart', 'ISO 2768 General Tolerances Chart (f, m, c, v and H, K, L)',
        'General tolerances for linear dimensions, radii, chamfers and angles (ISO 2768-1) and for flatness, perpendicularity, symmetry and run-out (ISO 2768-2).',
        body, faqs, 'ISO 2768 general tolerance chart: linear dimensions, radii, chamfers and angles in classes f, m, c, v (ISO 2768-1); straightness, flatness, perpendicularity, symmetry and run-out H, K, L (ISO 2768-2).',
        'ISO 2768 Tolerance Chart — General Tolerances f, m, c, v and H, K, L | InCost', 'chart-2768', art)

# ---------------------------------------------------------------- 6. bearings
def p_bearings():
    B = D['BRG_SER']; rows = []
    for i in range(len(B['62'])):
        row = []
        for ser in ('60', '62', '63'):
            d, Dd, w = B[ser][i]
            row += [f'<b>{ser}{i:02d}</b>', f'{d} × {Dd} × {w}']
        rows.append(row)
    body = finder('Find a bearing, e.g. 6204') + table(['6000 series', 'd × D × B, mm', '6200 series', 'd × D × B, mm', '6300 series', 'd × D × B, mm'], rows, num_from=9,
        caption='Boundary dimensions per ISO 15 (dimension series 10, 02, 03): bore d × outside diameter D × width B, mm. Suffixes (2RS, ZZ, C3) do not change the size.', wide=True)
    art = '''<h2>How to read a bearing number</h2>
<p><b>6</b> — single-row deep groove ball bearing. Second digit — the series: <b>0</b> extra light, <b>2</b> light, <b>3</b> medium. The last two digits give the bore: <b>00</b> = 10 mm, <b>01</b> = 12 mm, <b>02</b> = 15 mm, <b>03</b> = 17 mm, and from <b>04</b> on the bore is the number × 5 (6204 → 20 mm, 6310 → 50 mm).</p>
<p>Same bore, heavier series: larger outside diameter and width, higher load rating. 6004, 6204 and 6304 all fit a 20 mm shaft.</p>
<h2>Suffixes</h2><ul><li><b>ZZ / 2Z</b> — metal shields on both sides.</li><li><b>2RS / 2RSH</b> — rubber seals on both sides.</li><li><b>C3</b> — internal clearance larger than normal (hot running, interference fits).</li></ul>'''
    faqs = [('What size is a 6204 bearing?', '20 × 47 × 14 mm: 20 mm bore, 47 mm outside diameter, 14 mm wide.'),
            ('What are the dimensions of a 6205 bearing?', '25 × 52 × 15 mm.'),
            ('What size is a 6000 bearing?', '10 × 26 × 8 mm.'),
            ('What is the difference between 6204 and 6304?', 'Both have a 20 mm bore. 6304 is from the medium series: 52 mm outside and 15 mm wide versus 47 × 14 mm for 6204, and it carries more load.')]
    return page('ball-bearing-size-chart.html', 'Ball Bearing Size Chart', 'Ball Bearing Size Chart: 6000, 6200 and 6300 series',
        'Bore, outside diameter and width of deep groove ball bearings 6000–6020, 6200–6220 and 6300–6320 per ISO 15.',
        body, faqs, 'Deep groove ball bearing size chart: 6000, 6200 and 6300 series dimensions (bore × OD × width in mm, ISO 15). 6204 = 20×47×14, 6205 = 25×52×15.',
        'Ball Bearing Size Chart — 6000, 6200, 6300 Series Dimensions (6204, 6205) | InCost', 'chart-bearing', art)

# ---------------------------------------------------------------- 7. steel equivalents
def p_steel():
    rows = []
    for k, r in D['STEEL_EQ'].items():
        gost, en, num, us, exact = r[0], r[1], r[2], r[3], r[4]
        mark = '' if exact else ' <span class="mk" title="Equivalent by purpose only — compare chemistry and properties">≈</span>'
        rows.append([f'<b>{E(en)}</b>', E(num), E(us) + mark, E(gost)])
    body = finder('Find a grade, e.g. 1045 or S355') + table(['EN 10027-1', 'EN 10027-2 number', 'USA (AISI / ASTM)', 'GOST / DSTU'], rows, num_from=9,
        caption='≈ — equivalent by purpose only: chemistry and properties differ, compare before substituting. “—” — no common equivalent.')
    art = '''<h2>Equivalent does not mean identical</h2>
<p>Steels from different standards are made to different chemistry ranges and tested differently. Grades marked without ≈ have close chemistry and properties and are routinely substituted; grades marked ≈ only serve the same purpose. For a structural, pressure or safety-relevant part, check the mill certificate (EN 10204 3.1) against the drawing requirement, not the name.</p>
<h2>Common pairs</h2>
<ul><li><b>S235JR ↔ ASTM A36 ↔ Ст3сп</b> — general structural steel, easy to weld.</li>
<li><b>C45 ↔ AISI 1045 ↔ Сталь 45</b> — medium-carbon steel for shafts and machined parts, heat treatable.</li>
<li><b>X5CrNi18-10 (1.4301) ↔ AISI 304 ↔ 08Х18Н10</b> — the standard stainless steel.</li>
<li><b>X2CrNiMo17-12-2 (1.4404) ↔ AISI 316L</b> — stainless for chlorides and food.</li></ul>'''
    faqs = [('What is the US equivalent of S235JR?', 'ASTM A36 is the usual equivalent: both are general structural steels with about 235–250 MPa yield strength.'),
            ('What is C45 in AISI?', 'AISI 1045 (EN number 1.0503). In GOST it is Сталь 45.'),
            ('Is 1.4301 the same as 304?', 'Yes, X5CrNi18-10 / 1.4301 is the European designation of AISI 304 stainless steel.'),
            ('What is the AISI equivalent of 34CrNiMo6?', '34CrNiMo6 (1.6582) corresponds to AISI 4340 and GOST 40ХН2МА.')]
    return page('steel-grade-equivalents.html', 'Steel Grade Equivalents', 'Steel Grade Equivalents: EN, AISI/ASTM, GOST',
        'Cross-reference of common structural, carbon, alloy, tool and stainless steels between European (EN), American (AISI/ASTM) and GOST/DSTU designations.',
        body, faqs, 'Steel grade equivalents chart: EN 10027 names and numbers, AISI/ASTM and GOST/DSTU — S235JR = A36, C45 = 1045, 1.4301 = 304, 1.4404 = 316L, 34CrNiMo6 = 4340.',
        'Steel Grade Equivalents Chart — EN, AISI/ASTM, GOST Cross-Reference | InCost', 'chart-steel', art)

# ---------------------------------------------------------------- 8. equal angles
def ang_area(a, t, r1, r2):
    return t * (2 * a - t) + (1 - math.pi / 4) * (r1 * r1 - 2 * r2 * r2)
def p_angle():
    rows = []
    for a, t, r1, r2 in D['ANG_EN']:
        A = ang_area(a, t, r1, r2); kg = A * 7850e-6
        rows.append([f'<b>L{f(a)}×{f(a)}×{f(t)}</b>', f(t), f(r1), f(r2), f(A / 100, 2), f(kg, 2), f(kg * 0.671969, 2)])
    body = finder('Find a size, e.g. 50×5') + table(['Section', 't, mm', 'r1, mm', 'r2, mm', 'Area, cm²', 'Mass, kg/m', 'Weight, lb/ft'], rows,
        caption='Equal leg angles per EN 10056-1. Mass from the cross-section area with root and toe radii and density 7850 kg/m³.')
    art = '''<h2>How the weight is calculated</h2>
<p>The area of an equal angle is two leg rectangles minus their overlap, plus the root fillet, minus the rounded toes:</p>
<div class="formula">A = t·(2a − t) + (1 − π/4)·(r1² − 2·r2²)
mass per metre = A [mm²] × 7850 kg/m³ × 10⁻⁶</div>
<p>Example, L50×50×5 (r1 = 7, r2 = 3.5): A = 5 × 95 + 0.2146 × (49 − 24.5) = 480.3 mm² → 3.77 kg/m.</p>
<h2>Price of a profile</h2><p>Multiply the mass per metre by the length and your price per kilogram, and add the cutting: InCost does this in the “Profiles and cost” section and adds the profile to the product with your prices.</p>'''
    faqs = [('How much does a 50×50×5 angle weigh?', '3.77 kg per metre (2.53 lb/ft).'),
            ('What is the weight of angle 40×40×4?', '2.42 kg per metre.'),
            ('What do r1 and r2 mean?', 'r1 is the root radius between the legs, r2 the radius at the toes of the legs. They change the area slightly and are part of the EN 10056-1 designation.'),
            ('Do unequal angles follow the same formula?', 'Almost: replace 2a with a + b, the two leg lengths. This page covers equal angles only.')]
    return page('angle-steel-weight-chart.html', 'Equal Angle Weight Chart', 'Equal Angle Steel Weight Chart (EN 10056-1)',
        'Mass per metre, weight per foot and cross-section area of equal leg steel angles L20×20×3 to L150×150×15 per EN 10056-1.',
        body, faqs, 'Equal angle steel weight chart EN 10056-1: L20 to L150 — mass in kg/m, weight in lb/ft and cross-section area, with root and toe radii.',
        'Angle Steel Weight Chart — Equal Angles EN 10056-1, kg/m and lb/ft | InCost', 'chart-angle', art)

CHARTS += [('metric-thread-chart.html', 'Metric Thread Chart', 'Pitch, minor diameter, tap drill, stress area, M2–M48'),
           ('tap-drill-chart.html', 'Tap Drill Size Chart', 'Metric coarse and fine, UNC and UNF'),
           ('clearance-hole-chart.html', 'Clearance Hole Chart', 'ISO 273 fine, medium, coarse; counterbores; inch'),
           ('sheet-metal-gauge-chart.html', 'Sheet Metal Gauge Chart', 'Gauge to inch and mm, steel, stainless, aluminum'),
           ('iso-2768-tolerance-chart.html', 'ISO 2768 Tolerance Chart', 'General tolerances f, m, c, v and H, K, L'),
           ('ball-bearing-size-chart.html', 'Ball Bearing Size Chart', '6000, 6200, 6300 series dimensions'),
           ('steel-grade-equivalents.html', 'Steel Grade Equivalents', 'EN, AISI/ASTM and GOST cross-reference'),
           ('angle-steel-weight-chart.html', 'Equal Angle Weight Chart', 'EN 10056-1 angles: kg/m and lb/ft')]

if __name__ == '__main__':
    out = {}
    for fn in (p_threads, p_tapdrill, p_clear, p_gauge, p_2768, p_bearings, p_steel, p_angle):
        h = fn(); name = re.search(r'<link rel="canonical" href="https://incost.app/([^"]+)"', h).group(1); out[name] = h
    for n, h in out.items(): open(os.path.join(ROOT, n), 'w', encoding='utf-8').write(h)
    print('written', list(out))
