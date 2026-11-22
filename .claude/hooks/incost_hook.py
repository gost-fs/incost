#!/usr/bin/env python3
"""Claude Code hooks for the incost.app site.  Usage: incost_hook.py pre|post|stop  (event JSON on stdin)

pre  — before Edit/Write: blocks hand edits of generated pages
post — after Edit/Write: regenerates calculators / chart pages / features.html when their sources change
stop — when Claude finishes: runs tools/check_site.py if any site file changed, and asks Claude to fix problems
Exit code 2 = message on stderr goes back to Claude (pre: the edit is blocked).
"""
import json, os, re, subprocess, sys

ROOT = os.environ.get('CLAUDE_PROJECT_DIR') or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = sys.executable or 'python3'
CHART_PAGES = {'metric-thread-chart.html', 'tap-drill-chart.html', 'clearance-hole-chart.html', 'sheet-metal-gauge-chart.html',
               'iso-2768-tolerance-chart.html', 'ball-bearing-size-chart.html', 'steel-grade-equivalents.html',
               'angle-steel-weight-chart.html'}
CALC_PAGES = {'metal-weight-calculator.html', '3d-print-cost-calculator.html', 'laser-cutting-cost-calculator.html',
              'cnc-machining-cost-calculator.html'}


def rel(p):
    try:
        return os.path.relpath(os.path.abspath(p), ROOT).replace('\\', '/')
    except ValueError:
        return p


def run(*args):
    r = subprocess.run([PY, '-I', *args], cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def say(msg, code=2):
    print(msg, file=sys.stderr)
    sys.exit(code)


ev = sys.argv[1] if len(sys.argv) > 1 else ''
try:
    data = json.load(sys.stdin)
except Exception:
    data = {}
inp = data.get('tool_input') or {}
path = rel(inp.get('file_path', '')) if inp.get('file_path') else ''

if ev == 'pre':
    if path == 'features.html':
        say('Blocked: features.html is generated. Edit index.html or tools/features_main.html / tools/features_parts/*, '
            'then run python3 tools/gen_features.py (the post-edit hook does it for you).')
    if path in CALC_PAGES:
        say(f'Blocked: {path} is generated. Change tools/gen_calculators.py instead '
            '(the post-edit hook regenerates the calculators and the chart pages).')
    if path in CHART_PAGES:
        say(f'Blocked: {path} is generated. Change tools/charts-data.json or tools/gen_charts.py instead '
            '(the post-edit hook regenerates the pages and runs check_charts.py).')
    sys.exit(0)

if ev == 'post':
    out = []
    if path == 'index.html' or path.startswith('tools/features_') or path == 'tools/gen_features.py':
        c, o = run('tools/gen_features.py')
        out.append(('gen_features.py', c, o))
    if path == 'tools/gen_calculators.py':
        c, o = run('tools/gen_calculators.py', '.')
        out.append(('gen_calculators.py', c, o))
    if path in ('tools/charts-data.json', 'tools/gen_charts.py', 'tools/gen_calculators.py'):
        c, o = run('tools/gen_charts.py')
        out.append(('gen_charts.py', c, o))
        if c == 0:
            c, o = run('tools/check_charts.py')
            out.append(('check_charts.py', c, o))
    bad = [x for x in out if x[1]]
    if bad:
        say('\n'.join(f'{n} failed:\n{o[-1500:]}' for n, c, o in bad))
    if out:
        print('Regenerated: ' + ', '.join(n for n, c, o in out))
    sys.exit(0)

if ev == 'stop':
    if data.get('stop_hook_active'):
        sys.exit(0)  # already asked once — don't loop
    r = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True)
    changed = [l[3:] for l in r.stdout.splitlines()]
    if not any(re.search(r'\.(html|xml|json|py)$', f) for f in changed):
        sys.exit(0)
    c, o = run('tools/check_site.py')
    if c:
        say('tools/check_site.py found problems — fix them before finishing:\n' + o[-2500:])
    sys.exit(0)
