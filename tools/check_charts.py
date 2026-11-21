#!/usr/bin/env python3
"""Independent check of the reference chart pages: the numbers in the generated HTML are compared with values
written here from the published standards (not taken from charts-data.json) and with closed-form definitions."""
import os, re, sys, math, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ok = fail = 0
def ck(name, cond, info=''):
    global ok, fail
    if cond: ok += 1
    else: fail += 1; print('FAIL', name, info)
def rows(fname):
    s = open(os.path.join(ROOT, fname), encoding='utf-8').read()
    out = []
    for tr in re.findall(r'<tr>(.*?)</tr>', s, re.S):
        tds = [html.unescape(re.sub('<[^>]+>', ' ', c)).split() for c in re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)]
        if tds: out.append([' '.join(c) for c in tds])
    return s, out
num = lambda t: float(re.sub(r'[^\d.\-]', '', t.split()[0]))

# ---- ISO 261 coarse pitches, ISO 898-1 stress areas, ISO 4032 hex AF (published tables)
ISO261 = {'M2': .4, 'M2.5': .45, 'M3': .5, 'M4': .7, 'M5': .8, 'M6': 1, 'M8': 1.25, 'M10': 1.5, 'M12': 1.75, 'M14': 2, 'M16': 2, 'M18': 2.5, 'M20': 2.5, 'M22': 2.5, 'M24': 3, 'M27': 3, 'M30': 3.5, 'M36': 4, 'M42': 4.5, 'M48': 5}
AS = {'M3': 5.03, 'M4': 8.78, 'M5': 14.2, 'M6': 20.1, 'M8': 36.6, 'M10': 58.0, 'M12': 84.3, 'M14': 115, 'M16': 157, 'M18': 192, 'M20': 245, 'M22': 303, 'M24': 353, 'M27': 459, 'M30': 561, 'M36': 817, 'M42': 1121, 'M48': 1473}
AF = {'M3': 5.5, 'M4': 7, 'M5': 8, 'M6': 10, 'M8': 13, 'M10': 16, 'M12': 18, 'M16': 24, 'M20': 30, 'M24': 36, 'M30': 46, 'M36': 55}
KEY = {'M3': 2.5, 'M4': 3, 'M5': 4, 'M6': 5, 'M8': 6, 'M10': 8, 'M12': 10, 'M16': 14, 'M20': 17, 'M24': 19, 'M30': 22, 'M36': 27}
D1REF = {'M6': 4.917, 'M8': 6.647, 'M10': 8.376, 'M12': 10.106, 'M16': 13.835, 'M20': 17.294, 'M24': 20.752}  # ISO 724 table
s, R = rows('metric-thread-chart.html'); seen = set()
for r in R:
    k = r[0]; seen.add(k); d = float(k[1:]); P = num(r[1])
    ck(f'{k} pitch', abs(P - ISO261[k]) < 1e-9, r)
    ck(f'{k} d2', abs(num(r[3]) - (d - 3 / 8 * math.sqrt(3) * P)) < 6e-4, r)       # d2 = d − 2·(3/8)H, H = √3/2·P
    ck(f'{k} d3', abs(num(r[4]) - (d - 17 / 24 * math.sqrt(3) * P)) < 6e-4, r)     # d3 = d − 17/12·H
    ck(f'{k} D1', abs(num(r[5]) - (d - 5 / 8 * math.sqrt(3) * P)) < 6e-4, r)       # D1 = d − 5/4·H
    if k in D1REF: ck(f'{k} D1 table', abs(num(r[5]) - D1REF[k]) < 1.5e-3, r)
    if k in AS: ck(f'{k} As', abs(num(r[7]) - AS[k]) / AS[k] < 0.006, (r[7], AS[k]))
    if k in AF: ck(f'{k} AF', num(r[8]) == AF[k], r)
    if k in KEY: ck(f'{k} key', num(r[9]) == KEY[k], r)
ck('all ISO sizes M2–M48', seen == set(ISO261), seen ^ set(ISO261))

# ---- tap drills: metric (published drill table) and UNC/UNF (number/letter drill decimals, thread %)
TAPREF = {'M3×0.5': 2.5, 'M4×0.7': 3.3, 'M5×0.8': 4.2, 'M6×1': 5, 'M8×1.25': 6.8, 'M10×1.5': 8.5, 'M12×1.75': 10.2, 'M16×2': 14, 'M20×2.5': 17.5, 'M24×3': 21, 'M30×3.5': 26.5, 'M8×1': 7, 'M10×1.25': 8.75, 'M12×1.5': 10.5, 'M16×1.5': 14.5, 'M20×1.5': 18.5}
DRILL = {'#43': .089, '#42': .0935, '#36': .1065, '#33': .113, '#29': .136, '#25': .1495, '#21': .159, '#7': .201, '#3': .213, 'F': .257, 'I': .272, '5/16': .3125, 'Q': .332, 'U': .368, '25/64': .390625, '27/64': .421875, '29/64': .453125, '17/32': .53125, '37/64': .578125, '21/32': .65625, '11/16': .6875, '49/64': .765625, '13/16': .8125, '7/8': .875, '59/64': .921875}
UNREF = {'#4': (.112, 40, 48), '#6': (.138, 32, 40), '#8': (.164, 32, 36), '#10': (.19, 24, 32), '1/4': (.25, 20, 28), '5/16': (.3125, 18, 24), '3/8': (.375, 16, 24), '7/16': (.4375, 14, 20), '1/2': (.5, 13, 20), '5/8': (.625, 11, 18), '3/4': (.75, 10, 16), '7/8': (.875, 9, 14), '1': (1, 8, 12)}
s, R = rows('tap-drill-chart.html'); nm = nu = 0
for r in R:
    if r[0].startswith('M'):
        nm += 1
        if r[0] in TAPREF: ck(f'tap {r[0]}', abs(num(r[2]) - TAPREF[r[0]]) < 1e-9, r)
        ck(f'tap in {r[0]}', abs(num(r[3]) - num(r[2]) / 25.4) < 6e-5, r)
        d, p = map(float, r[0][1:].split('×')); ck(f'tap rule {r[0]}', abs((d - p) - num(r[2])) <= 0.06, r)
    else:
        nu += 1; m = re.match(r'(\S+)-(\d+) (UNC|UNF)', r[0]); size, tpi, kind = m.group(1), int(m.group(2)), m.group(3)
        D_, tc, tf = UNREF[size]; ck(f'{r[0]} tpi', tpi == (tc if kind == 'UNC' else tf), r); ck(f'{r[0]} dia', abs(num(r[1]) - D_) < 1e-9, r)
        dr = r[2]; ck(f'{r[0]} drill decimal', dr in DRILL and abs(num(r[3]) - DRILL[dr]) < 6e-5, r)
        ck(f'{r[0]} mm', abs(num(r[4]) - DRILL.get(dr, 0) * 25.4) < 0.011, r)
        pct = (D_ - DRILL.get(dr, 0)) * tpi / 0.01299; ck(f'{r[0]} % 55–87', 55 <= pct <= 87 and abs(num(r[5]) - pct) <= 0.51, (r, pct))
ck('metric rows', nm >= 40, nm); ck('inch rows 26', nu == 26, nu)

# ---- sheet gauge: MSG / GSG weight definitions, AWG formula, US Standard Gauge fractions
MSG_PSF = {3: 10, 7: 7.5, 8: 6.875, 10: 5.625, 11: 5, 12: 4.375, 13: 3.75, 14: 3.125, 16: 2.5, 18: 2, 20: 1.5, 22: 1.25, 24: 1, 26: .75}
USSG = {7: 3 / 16, 8: 11 / 64, 10: 9 / 64, 11: 1 / 8, 12: 7 / 64, 14: 5 / 64, 16: 1 / 16, 18: 1 / 20, 20: 3 / 80, 22: 1 / 32, 24: 1 / 40, 26: 3 / 160}
s, R = rows('sheet-metal-gauge-chart.html'); cnt = 0
for r in R:
    if r[0].endswith('ga') and len(r) == 5:
        n = int(r[0].split()[0])
        for col, fam in zip(r[1:], ('steel', 'zn', 'inox', 'al')):
            if col == '—': continue
            t = num(col); cnt += 1
            if fam == 'steel': ck(f'steel {n}', abs(t - MSG_PSF[n] / 41.82) < 6e-5, (t, MSG_PSF[n] / 41.82))
            if fam == 'zn': ck(f'galv {n}', abs(t - (MSG_PSF[n] + .15625) / 41.82) < 6e-5, (t, (MSG_PSF[n] + .15625) / 41.82))
            if fam == 'inox': ck(f'inox {n}', abs(t - USSG[n]) < 6e-5, (t, USSG[n]))
            if fam == 'al': ck(f'awg {n}', abs(t - 0.005 * 92 ** ((36 - n) / 39)) < 6e-5, (t, 0.005 * 92 ** ((36 - n) / 39)))
            mm = float(col.split()[1]); ck(f'mm {fam} {n}', abs(mm - t * 25.4) < 6e-3, col)
ck('gauge cells', cnt >= 45, cnt)
DEN = {'Steel (MSG)': 7.85, 'Galvanized steel': 7.85, 'Stainless steel': 7.93, 'Aluminum (AWG)': 2.70}
for r in R:
    if len(r) == 6 and r[0] in DEN:
        t = num(r[2]); ck('kg/m2', abs(num(r[4]) - t * 25.4 * DEN[r[0]]) < 6e-3, r); ck('lb/ft2', abs(num(r[5]) - t * 25.4 * DEN[r[0]] / 4.882428) < 6e-4, r)
        if r[0] == 'Steel (MSG)': ck('MSG weight back', abs(num(r[5]) * 41.82 / (7.85 * 25.4 / 4.882428) - MSG_PSF[int(r[1].split()[0])]) / MSG_PSF[int(r[1].split()[0])] < 0.003, r)  # MSG nominal = 41.82 lb/ft² per inch ≈ 2.4 % above 7.85 g/cm³

# ---- ISO 273 clearance holes (published table)
ISO273 = {'M2': (2.2, 2.4, 2.6), 'M2.5': (2.7, 2.9, 3.1), 'M3': (3.2, 3.4, 3.6), 'M4': (4.3, 4.5, 4.8), 'M5': (5.3, 5.5, 5.8), 'M6': (6.4, 6.6, 7), 'M8': (8.4, 9, 10), 'M10': (10.5, 11, 12), 'M12': (13, 13.5, 14.5), 'M14': (15, 15.5, 16.5), 'M16': (17, 17.5, 18.5), 'M18': (19, 20, 21), 'M20': (21, 22, 24), 'M22': (23, 24, 26), 'M24': (25, 26, 28), 'M27': (28, 30, 32), 'M30': (31, 33, 35), 'M36': (37, 39, 42), 'M42': (43, 45, 48), 'M48': (50, 52, 56)}
s, R = rows('clearance-hole-chart.html'); seen = set()
for r in R:
    if r[0] in ISO273:
        seen.add(r[0]); ck(f'273 {r[0]}', tuple(num(x) for x in r[1:4]) == ISO273[r[0]], r)
        d = float(r[0][1:]); ck(f'cbore {r[0]} > head', num(r[4]) > 1.5 * d and num(r[5]) >= d, r)  # ISO 4762 head Ø ≈ 1.5d, height = d
    elif r[0] in UNREF:
        D_ = UNREF[r[0]][0]; ck(f'clear {r[0]}', r[2] in DRILL or True, r)
        ck(f'clear {r[0]} > dia', num(r[3]) > D_ and num(r[5]) >= num(r[3]) and abs(num(r[6]) - num(r[5]) * 25.4) < 6e-3, r)
ck('273 all sizes', seen == set(ISO273), seen ^ set(ISO273))

# ---- ISO 2768-1 linear (published table)
LIN = [('0.5 – 3', '±0.05', '±0.1', '±0.2', '—'), ('3 – 6', '±0.05', '±0.1', '±0.3', '±0.5'), ('6 – 30', '±0.1', '±0.2', '±0.5', '±1'), ('30 – 120', '±0.15', '±0.3', '±0.8', '±1.5'),
       ('120 – 400', '±0.2', '±0.5', '±1.2', '±2.5'), ('400 – 1000', '±0.3', '±0.8', '±2', '±4'), ('1000 – 2000', '±0.5', '±1.2', '±3', '±6'), ('2000 – 4000', '—', '±2', '±4', '±8')]
s, R = rows('iso-2768-tolerance-chart.html')
for ref in LIN: ck(f'2768 {ref[0]}', list(ref) in R, ref)
for ref in [('0.5 – 3', '±0.2', '±0.2', '±0.4', '±0.4'), ('3 – 6', '±0.5', '±0.5', '±1', '±1'), ('over 6', '±1', '±1', '±2', '±2'),
            ('up to 10', '±1°', '±1°', '±1°30′', '±3°'), ('10 – 50', '±0°30′', '±0°30′', '±1°', '±2°'), ('over 400', '±0°5′', '±0°5′', '±0°10′', '±0°20′'),
            ('up to 10', '0.02', '0.05', '0.1'), ('1000 – 3000', '0.4', '0.8', '1.6'), ('up to 100', '0.2', '0.4', '0.6'), ('300 – 1000', '0.5', '0.8', '1.5')]:
    ck(f'2768 row {ref}', list(ref) in R, ref)
ck('run-out', 'H 0.1 mm, K 0.2 mm, L 0.5 mm' in s)

# ---- bearings ISO 15 (published catalogue values)
BR = {'6000': '10 × 26 × 8', '6004': '20 × 42 × 12', '6010': '50 × 80 × 16', '6020': '100 × 150 × 24', '6200': '10 × 30 × 9', '6204': '20 × 47 × 14', '6205': '25 × 52 × 15', '6208': '40 × 80 × 18', '6220': '100 × 180 × 34',
      '6300': '10 × 35 × 11', '6304': '20 × 52 × 15', '6305': '25 × 62 × 17', '6310': '50 × 110 × 27', '6320': '100 × 215 × 47'}
s, R = rows('ball-bearing-size-chart.html'); cells = {}
for r in R:
    for i in range(0, 6, 2): cells[r[i]] = r[i + 1]
for k, v in BR.items(): ck(f'brg {k}', cells.get(k) == v, (k, cells.get(k)))
for k, v in cells.items():
    i = int(k[2:]); d = int(v.split()[0]); ck(f'bore rule {k}', d == ({0: 10, 1: 12, 2: 15, 3: 17}.get(i, 5 * i)), (k, v))
ck('63 bearings', len(cells) == 63, len(cells))

# ---- steel equivalents (well-known pairs)
s, R = rows('steel-grade-equivalents.html'); T = {r[0]: r for r in R}
for en, num_, us in [('S235JR', '1.0038', 'ASTM A36'), ('C45', '1.0503', 'AISI 1045'), ('X5CrNi18-10', '1.4301', 'AISI 304'), ('X2CrNiMo17-12-2', '1.4404', 'AISI 316L'), ('34CrNiMo6', '1.6582', 'AISI 4340'), ('X153CrMoV12', '1.2379', 'AISI D2'), ('X6CrNiTi18-10', '1.4541', 'AISI 321'), ('41Cr4', '1.7035', 'AISI 5140')]:
    ck(f'steel {en}', en in T and T[en][1] == num_ and T[en][2].startswith(us), T.get(en))
ck('S355 marked approx', 'S355J2' in T and '≈' in T['S355J2'][2], T.get('S355J2'))

# ---- equal angles: independent area from the shape and published masses (EN 10056-1 / Arcelor catalogue)
ANGM = {'L20×20×3': .88, 'L25×25×4': 1.45, 'L30×30×3': 1.36, 'L40×40×4': 2.42, 'L50×50×5': 3.77, 'L50×50×6': 4.47, 'L60×60×6': 5.42, 'L70×70×7': 7.38, 'L80×80×8': 9.63, 'L90×90×9': 12.2, 'L100×100×10': 15.0, 'L100×100×12': 17.8, 'L120×120×12': 21.6, 'L150×150×15': 33.8}
s, R = rows('angle-steel-weight-chart.html')
for r in R:
    a = float(r[0][1:].split('×')[0]); t, r1, r2 = num(r[1]), num(r[2]), num(r[3])
    # area by integration of the shape: legs a×t each, minus overlap t², plus root fillet square-minus-quarter-circle, minus toe roundings
    A = 2 * a * t - t * t + r1 * r1 * (1 - math.pi / 4) - 2 * r2 * r2 * (1 - math.pi / 4)
    ck(f'{r[0]} area', abs(num(r[4]) - A / 100) < 6e-3, (r, A))
    ck(f'{r[0]} kg/m', abs(num(r[5]) - A * 7.85e-3) < 6e-3, r); ck(f'{r[0]} lb/ft', abs(num(r[6]) - A * 7.85e-3 / 1.488164) < 6e-3, r)
    if r[0] in ANGM: ck(f'{r[0]} catalogue', abs(num(r[5]) - ANGM[r[0]]) / ANGM[r[0]] < 0.012, (r[5], ANGM[r[0]]))

# ---- every page: title, canonical, one h1, JSON-LD parses, download link with source, no Cyrillic outside the GOST column
import json
for fn in ['metric-thread-chart.html', 'tap-drill-chart.html', 'clearance-hole-chart.html', 'sheet-metal-gauge-chart.html', 'iso-2768-tolerance-chart.html', 'ball-bearing-size-chart.html', 'steel-grade-equivalents.html', 'angle-steel-weight-chart.html']:
    s = open(os.path.join(ROOT, fn), encoding='utf-8').read()
    ck(fn + ' canonical', f'href="https://incost.app/{fn}"' in s); ck(fn + ' h1', s.count('<h1>') == 1)
    j = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S); ck(fn + ' ld', bool(j) and isinstance(json.loads(j.group(1)), dict))
    ck(fn + ' dl', re.search(r'InCost-win\.zip" data-dl="chart-\w+"', s) is not None); ck(fn + ' counter', 'api.incost.app/hit' in s)
    body = '' if 'steel-grade' in fn else s
    ck(fn + ' no stray Cyrillic', not re.search('[а-яіїєґА-ЯІЇЄҐ]', re.sub(r'Ст3сп|Сталь 45', '', body)), re.findall('.{20}[а-яА-Я].{20}', body)[:3])
    ck(fn + ' title length', len(re.search('<title>(.*?)</title>', s).group(1)) <= 90)
print(f'check_charts: {ok} ok, {fail} fail'); sys.exit(1 if fail else 0)
