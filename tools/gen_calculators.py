#!/usr/bin/env python3
"""Generates the free calculator pages for incost.app (SEO landing pages)."""
import json, os, sys, html

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
BASE = 'https://incost.app/'
DL = 'https://github.com/gost-fs/incost/releases/latest/download/InCost-win.zip'

PAGES = [
    ('metal-weight-calculator.html', 'Metal Weight Calculator', 'Steel, aluminum, stainless, brass and copper weight for plate, bar, tube and angle'),
    ('3d-print-cost-calculator.html', '3D Print Cost Calculator', 'Filament, electricity, machine wear, labor and selling price per print'),
    ('laser-cutting-cost-calculator.html', 'Laser Cutting Cost Calculator', 'Sheet metal part price from cut length, pierces, material and machine rate'),
    ('cnc-machining-cost-calculator.html', 'CNC Machining Cost Calculator', 'Stock, cycle time, setup and price per part at any quantity'),
]

CSS = r'''
:root{--bg:#FFFFFF;--bg-2:#F5F7FA;--ink:#111418;--ink-2:#5B6472;--line:#E3E7ED;--accent:#0B5CFF;--accent-ink:#FFFFFF;--accent-soft:#EBF1FF;--good:#0C8A5B;--bad:#C2410C;
--font:"Segoe UI Variable Text","Segoe UI",-apple-system,BlinkMacSystemFont,"SF Pro Text",Roboto,"Helvetica Neue",Arial,sans-serif;
--font-display:"Segoe UI Variable Display","Segoe UI",-apple-system,BlinkMacSystemFont,"SF Pro Display",Roboto,Arial,sans-serif;
--font-mono:"Cascadia Mono",Consolas,ui-monospace,"SF Mono",Menlo,monospace}
@media (prefers-color-scheme:dark){:root{--bg:#0E1013;--bg-2:#161A20;--ink:#EEF1F5;--ink-2:#9AA3B0;--line:#262C35;--accent:#4C86FF;--accent-soft:#16233F;--good:#34C78A;--bad:#F08A4B;color-scheme:dark}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 var(--font);-webkit-font-smoothing:antialiased}
[hidden]{display:none!important}
a{color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:6px}
.wrap{max-width:1100px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
header.top{border-bottom:1px solid var(--line);background:var(--bg);position:sticky;top:0;z-index:10}
.nav{display:flex;align-items:center;gap:16px;height:60px}
.logo{display:flex;align-items:center;gap:9px;font:700 19px/1 var(--font-display);text-decoration:none;color:var(--ink);letter-spacing:-.02em}
.nav .sp{flex:1}
.nav a.lnk{color:var(--ink-2);text-decoration:none;font-size:15px}
.nav a.lnk:hover{color:var(--ink)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px;padding:0 20px;border-radius:12px;font:600 15px/1.2 var(--font);text-decoration:none;border:1px solid transparent;cursor:pointer;white-space:nowrap}
.btn-primary{background:var(--accent);color:var(--accent-ink)}
.btn-primary:hover{filter:brightness(1.08)}
.btn-secondary{border-color:var(--line);background:var(--bg);color:var(--ink)}
@media (max-width:640px){.nav a.lnk{display:none}.nav .btn{padding:0 14px}}
.crumbs{font-size:14px;color:var(--ink-2);padding-top:22px}
.crumbs a{color:var(--ink-2);text-decoration:none}
h1,h2,h3{font-family:var(--font-display);letter-spacing:-.02em;line-height:1.12;text-wrap:balance;margin:0}
h1{font-size:clamp(32px,4.6vw,46px);margin:10px 0 12px}
.lead{font-size:19px;color:var(--ink-2);max-width:44em;margin:0}
.calc{display:grid;grid-template-columns:1.1fr .9fr;gap:0;border:1px solid var(--line);border-radius:18px;overflow:hidden;margin:28px 0 20px;background:var(--bg)}
.calc>*{min-width:0}
.inputs{padding:24px;display:grid;gap:14px;align-content:start;border-right:1px solid var(--line)}
.out{padding:24px;background:var(--bg-2);display:grid;gap:14px;align-content:start}
.f{display:grid;gap:5px;align-content:start}
.f label{font-size:13px;font-weight:600;color:var(--ink-2)}
.f input,.f select{width:100%;min-height:42px;font:16px var(--font);padding:0 11px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink)}
.f input:focus,.f select:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.f small{font-size:12px;color:var(--ink-2)}
.r2{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start}
.r3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;align-items:start}
.seg{display:inline-flex;padding:3px;border-radius:10px;background:var(--bg-2);border:1px solid var(--line);justify-self:start}
.seg button{all:unset;cursor:pointer;padding:6px 14px;border-radius:8px;font:600 14px var(--font);color:var(--ink-2)}
.seg button[aria-pressed="true"]{background:var(--bg);color:var(--ink);box-shadow:0 1px 4px rgba(10,30,80,.15)}
.seg button:focus-visible{outline:2px solid var(--accent)}
.big{font:700 clamp(34px,4.4vw,46px)/1 var(--font-display);letter-spacing:-.03em;color:var(--accent);font-variant-numeric:tabular-nums}
.big small{font:500 16px var(--font);color:var(--ink-2);letter-spacing:0}
.lbl{font-size:13px;font-weight:600;color:var(--ink-2)}
.lines{display:grid;gap:7px;font-size:15px;font-variant-numeric:tabular-nums}
.lines div{display:flex;justify-content:space-between;gap:10px;color:var(--ink-2);border-bottom:1px dashed var(--line);padding-bottom:6px}
.lines b{color:var(--ink);font-weight:600;text-align:right}
.err{color:var(--bad);font-size:14px;font-weight:600}
.bar{display:flex;height:10px;border-radius:999px;overflow:hidden;background:var(--line)}
.bar i{display:block;height:100%}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px;color:var(--ink-2)}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{width:10px;height:10px;border-radius:3px;display:inline-block}
table.q{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}
table.q th,table.q td{padding:7px 8px;border-bottom:1px solid var(--line);text-align:right}
table.q th:first-child,table.q td:first-child{text-align:left}
table.q th{color:var(--ink-2);font-weight:600}
@media (max-width:820px){.calc{grid-template-columns:1fr}.inputs{border-right:0;border-bottom:1px solid var(--line)}}
@media (max-width:420px){.r3{grid-template-columns:1fr 1fr}}
.cta{display:grid;grid-template-columns:1fr auto;gap:20px;align-items:center;border-radius:18px;padding:24px;background:var(--accent-soft);border:1px solid color-mix(in srgb,var(--accent) 30%,transparent);margin:8px 0 48px}
.cta>*{min-width:0}
.cta h2{font-size:22px;margin-bottom:6px}
.cta p{margin:0;color:var(--ink-2)}
@media (max-width:700px){.cta{grid-template-columns:1fr}}
article{max-width:760px}
article h2{font-size:28px;margin:44px 0 12px}
article h3{font-size:20px;margin:26px 0 8px}
article p,article li{color:var(--ink)}
article ul,article ol{padding-left:22px}
.formula{font-family:var(--font-mono);font-size:14px;background:var(--bg-2);border:1px solid var(--line);border-radius:10px;padding:12px 14px;overflow-x:auto;white-space:pre}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:12px;margin:12px 0}
.tbl table{width:100%;border-collapse:collapse;font-size:15px;min-width:460px}
.tbl th,.tbl td{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left}
.tbl tr:last-child td{border-bottom:0}
.tbl th{background:var(--bg-2);font-size:13px;color:var(--ink-2)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px;padding:16px 0;font-weight:600}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--accent);font-size:20px;line-height:1}
.faq details[open] summary::after{content:"–"}
.faq p{margin:0 0 16px;color:var(--ink-2)}
.tools{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:14px 0 56px}
.tools a{display:grid;gap:4px;padding:16px;border:1px solid var(--line);border-radius:14px;text-decoration:none;color:var(--ink);background:var(--bg)}
.tools a:hover{border-color:var(--accent)}
.tools b{font-size:16px}
.tools span{font-size:14px;color:var(--ink-2)}
footer{border-top:1px solid var(--line);padding-block:26px 40px;font-size:14px;color:var(--ink-2)}
.foot{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px}
.foot nav{display:flex;flex-wrap:wrap;gap:18px}
.foot a{color:var(--ink-2);text-decoration:none}
'''

LOGO = '<svg width="26" height="26" viewBox="0 0 28 28" aria-hidden="true"><rect width="28" height="28" rx="8" fill="#0B5CFF"/><path d="M9.5 20V8m5 12v-7.5h3.4a3.4 3.4 0 0 1 0 6.8" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'

COMMON_JS = r'''
var $=function(id){return document.getElementById(id)};
function num(id){var v=parseFloat(String($(id).value).replace(",","."));return isFinite(v)?v:NaN}
function f(v,d){return v.toLocaleString("en-US",{minimumFractionDigits:d,maximumFractionDigits:d})}
function money(v){return "$"+f(v,2)}
function row(a,b){return "<div><span>"+a+"</span><b>"+b+"</b></div>"}
function seg(id,cb){var s=$(id);[].forEach.call(s.querySelectorAll("button"),function(b){b.addEventListener("click",function(){[].forEach.call(s.querySelectorAll("button"),function(x){x.setAttribute("aria-pressed",x===b)});cb(b.dataset.v)})})}
function setSeg(id,v){[].forEach.call($(id).querySelectorAll("button"),function(x){x.setAttribute("aria-pressed",x.dataset.v===v)})}
function store(k,v){try{localStorage.setItem(k,v)}catch(e){}}
function load(k){try{return localStorage.getItem(k)}catch(e){return null}}
function defaultUnits(){var l=(navigator.language||"en-US");return /^en-(US|LR)|^my/i.test(l)?"in":"mm"}
'''

def page(fname, title, short, h1, lead, calc_html, calc_js, article_html, faqs, meta_desc, keywords_title):
    others = [p for p in PAGES if p[0] != fname]
    tools = ''.join(f'<a href="{p[0]}"><b>{p[1]}</b><span>{p[2]}</span></a>' for p in others)
    tools += '<a href="./"><b>InCost for Windows</b><span>Quote parts from DXF and STEP files, nesting and shop drawings</span></a>'
    faq_html = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{a}</p></details>' for q, a in faqs)
    import re
    strip = lambda s: re.sub('<[^>]+>', '', s)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": title, "url": BASE + fname, "applicationCategory": "BusinessApplication",
         "operatingSystem": "Any (web browser)", "browserRequirements": "Requires JavaScript",
         "description": meta_desc, "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "publisher": {"@type": "Organization", "name": "InCost", "url": BASE}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "InCost", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Free calculators", "item": BASE + "#tools"},
            {"@type": "ListItem", "position": 3, "name": title, "item": BASE + fname}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}]}
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(keywords_title)}</title>
<meta name="description" content="{html.escape(meta_desc)}">
<link rel="canonical" href="{BASE}{fname}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#0B5CFF">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="InCost">
<meta property="og:url" content="{BASE}{fname}">
<meta property="og:title" content="{html.escape(title)} — free online">
<meta property="og:description" content="{html.escape(meta_desc)}">
<meta property="og:image" content="{BASE}og.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
<!--ANALYTICS-->
</head>
<body>
<header class="top"><div class="wrap nav">
<a class="logo" href="./">{LOGO}InCost</a><span class="sp"></span>
<a class="lnk" href="./#tools">Free calculators</a><a class="lnk" href="./#pricing">Pricing</a>
<a class="btn btn-primary" href="./#get">Download InCost</a>
</div></header>
<main class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="./">InCost</a> › <a href="./#tools">Free calculators</a> › {html.escape(title)}</nav>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
{calc_html}
<section class="cta">
<div><h2>Quote real parts in seconds</h2><p>InCost does this automatically from your DXF, STEP and STL files: cut length, weight, nesting, machine time, PDF quotes and shop drawings. Free for Windows.</p></div>
<a class="btn btn-primary" href="{DL}">Download free for Windows</a>
</section>
<article>
{article_html}
<h2 id="faq">Frequently asked questions</h2>
<div class="faq">{faq_html}</div>
</article>
<h2 style="font-size:26px;margin-top:48px">More free calculators</h2>
<div class="tools">{tools}</div>
</main>
<footer><div class="wrap foot"><span>© 2026 InCost · hello@incost.app</span>
<nav><a href="./">Home</a><a href="./#tools">Calculators</a><a href="terms.html">Terms</a><a href="privacy.html">Privacy</a></nav></div></footer>
<script>(function(){{{COMMON_JS}{calc_js}}})();</script>
</body>
</html>
'''

# ============================ 1. METAL WEIGHT ============================
MATS_W = [  # name, density g/cm3, default price $/lb
    ('Carbon steel (A36, 1018)', 7.85, 0.75), ('Stainless steel 304', 7.93, 2.40), ('Stainless steel 316', 8.00, 3.20),
    ('Aluminum 6061', 2.70, 3.50), ('Aluminum 5052', 2.68, 3.20), ('Brass C360', 8.50, 4.20), ('Copper C110', 8.94, 5.00),
    ('Bronze C932', 8.93, 6.00), ('Titanium Grade 5', 4.43, 25.0), ('Cast iron (gray)', 7.20, 1.00), ('Zinc', 7.13, 2.00), ('Lead', 11.34, 1.50)]
mat_opts = ''.join(f'<option value="{i}">{n} · {d} g/cm³</option>' for i, (n, d, p) in enumerate(MATS_W))
metal_calc = f'''
<section class="calc" aria-label="Metal weight calculator">
<div class="inputs">
<div class="seg" id="units" role="group" aria-label="Units"><button type="button" data-v="in" aria-pressed="true">Inches · lb</button><button type="button" data-v="mm" aria-pressed="false">Millimeters · kg</button></div>
<div class="f"><label for="shape">Shape</label><select id="shape">
<option value="plate">Plate / sheet / flat bar</option><option value="round">Round bar</option><option value="square">Square bar</option><option value="hex">Hex bar</option>
<option value="tube">Round tube / pipe</option><option value="rect">Square / rectangular tube</option><option value="angle">Angle</option></select></div>
<div class="f"><label for="mat">Material</label><select id="mat">{mat_opts}<option value="c">Custom density…</option></select></div>
<div class="f" id="customF" hidden><label for="dens">Density, g/cm³</label><input id="dens" type="number" inputmode="decimal" step="0.01" value="7.85"></div>
<div class="r3" id="dims"></div>
<div class="r2"><div class="f"><label for="qty">Quantity</label><input id="qty" type="number" inputmode="numeric" min="1" step="1" value="1"></div>
<div class="f"><label for="price" id="priceL">Price per lb, $ (optional)</label><input id="price" type="number" inputmode="decimal" step="0.01" min="0" value=""></div></div>
</div>
<div class="out" aria-live="polite">
<div><div class="lbl">Weight per piece</div><div class="big" id="w1">—</div></div>
<div class="lines" id="lines"></div>
<p class="err" id="err" hidden></p>
</div>
</section>'''
metal_js = r'''
var MATS=''' + json.dumps([[n, d, p] for n, d, p in MATS_W]) + r''';
var SH={plate:[["l","Length",24,600],["w","Width",12,300],["t","Thickness",0.25,6]],
round:[["d","Diameter",1,25],["l","Length",12,300]],
square:[["a","Side",1,25],["l","Length",12,300]],
hex:[["s","Across flats",1,25],["l","Length",12,300]],
tube:[["d","Outside diameter",2,50],["t","Wall thickness",0.12,3],["l","Length",120,3000]],
rect:[["w","Width",2,50],["h","Height",2,50],["t","Wall thickness",0.12,3],["l","Length",120,3000]],
angle:[["a","Leg A",2,50],["b","Leg B",2,50],["t","Thickness",0.25,6],["l","Length",120,3000]]};
var U=load("incost-units")||defaultUnits();
function build(){
  var s=$("shape").value,u=U==="in"?"in":"mm";
  $("dims").innerHTML=SH[s].map(function(d){return '<div class="f"><label for="d_'+d[0]+'">'+d[1]+', '+u+'</label><input id="d_'+d[0]+'" type="number" inputmode="decimal" min="0" step="any" value="'+(U==="in"?d[2]:d[3])+'"></div>'}).join("");
  [].forEach.call($("dims").querySelectorAll("input"),function(i){i.addEventListener("input",calc)});
  $("priceL").textContent=U==="in"?"Price per lb, $ (optional)":"Price per kg, $ (optional)";
  calc();
}
function calc(){
  var s=$("shape").value,k=U==="in"?2.54:0.1,g=function(n){return num("d_"+n)*k},err="";
  var mi=$("mat").value,rho=mi==="c"?num("dens"):MATS[+mi][1],A,L=g("l");
  $("customF").hidden=mi!=="c";
  if(s==="plate"){A=g("w")*g("t")}
  else if(s==="round"){A=Math.PI*Math.pow(g("d"),2)/4}
  else if(s==="square"){A=Math.pow(g("a"),2)}
  else if(s==="hex"){A=Math.sqrt(3)/2*Math.pow(g("s"),2)}
  else if(s==="tube"){var D=g("d"),t=g("t");if(t*2>=D)err="Wall thickness must be less than half the outside diameter.";A=Math.PI/4*(D*D-Math.pow(D-2*t,2))}
  else if(s==="rect"){var W=g("w"),H=g("h"),t2=g("t");if(t2*2>=Math.min(W,H))err="Wall thickness must be less than half the smaller side.";A=W*H-(W-2*t2)*(H-2*t2)}
  else if(s==="angle"){var a=g("a"),b=g("b"),t3=g("t");if(t3>=Math.min(a,b))err="Thickness must be less than both legs.";A=t3*(a+b-t3)}
  var q=Math.max(1,Math.round(num("qty")||1));
  if(!err&&!(A>0&&L>0&&rho>0))err="Enter all dimensions as positive numbers.";
  $("err").hidden=!err;$("err").textContent=err;
  if(err){$("w1").innerHTML="—";$("lines").innerHTML="";return}
  var vol=A*L,kg=vol*rho/1000,lb=kg*2.2046226,pr=num("price"),out="";
  var main=U==="in"?f(lb,lb<10?3:2)+' <small>lb</small>':f(kg,kg<10?3:2)+' <small>kg</small>';
  $("w1").innerHTML=main;
  out+=row("Weight per piece",U==="in"?f(kg,3)+" kg":f(lb,3)+" lb");
  if(q>1)out+=row("Total for "+q+" pcs",U==="in"?f(lb*q,2)+" lb · "+f(kg*q,2)+" kg":f(kg*q,2)+" kg · "+f(lb*q,2)+" lb");
  if(s!=="plate")out+=row(U==="in"?"Weight per foot":"Weight per meter",U==="in"?f(lb/(L/2.54)*12,3)+" lb/ft":f(kg/(L/100),3)+" kg/m");
  else out+=row(U==="in"?"Weight per sq ft":"Weight per m²",U==="in"?f(lb/((L/2.54)*(g("w")/2.54))*144,3)+" lb/ft²":f(kg/(L*g("w")/1e4),2)+" kg/m²");
  out+=row("Cross-section area",U==="in"?f(A/6.4516,4)+" in²":f(A*100,1)+" mm²");
  out+=row("Volume",U==="in"?f(vol/16.387064,3)+" in³":f(vol,1)+" cm³");
  out+=row("Density",f(rho,2)+" g/cm³ · "+f(rho*0.0361273,4)+" lb/in³");
  if(pr>0){var c=U==="in"?lb*pr:kg*pr;out+=row("Material cost",money(c)+(q>1?" · "+money(c*q)+" total":""))}
  $("lines").innerHTML=out;
}
$("mat").addEventListener("change",function(){var mi=this.value;if(mi!=="c"){var p=MATS[+mi][2];$("price").placeholder=U==="in"?"e.g. "+p.toFixed(2):"e.g. "+(p*2.2046).toFixed(2)}calc()});
["qty","price","dens"].forEach(function(i){$(i).addEventListener("input",calc)});
$("shape").addEventListener("change",build);
seg("units",function(v){U=v;store("incost-units",v);build()});
setSeg("units",U);build();
'''
dens_rows = ''.join(f'<tr><td>{n}</td><td>{d}</td><td>{d*0.0361273:.4f}</td><td>{d*1000:.0f}</td></tr>' for n, d, p in MATS_W)
metal_article = f'''
<h2>How metal weight is calculated</h2>
<p>Weight is volume multiplied by density. The calculator finds the cross-section area of the shape, multiplies it by the length, then by the density of the material you pick.</p>
<div class="formula">Weight = Cross-section area × Length × Density

Plate        A = W × T
Round bar    A = π × D² / 4
Square bar   A = S²
Hex bar      A = 0.866 × F²          (F = across flats)
Round tube   A = π / 4 × (OD² − (OD − 2t)²)
Rect. tube   A = W × H − (W − 2t)(H − 2t)
Angle        A = t × (A + B − t)</div>
<p>Example: a 24 × 12 in plate, 1/4 in thick, in A36 steel. Volume is 24 × 12 × 0.25 = 72 in³. Steel weighs 0.2836 lb/in³, so the plate weighs about <b>20.4 lb (9.26 kg)</b>.</p>
<h2>Metal density chart</h2>
<p>Typical densities used by the calculator. Real alloys vary by a percent or two, so use the mill certificate when weight must be exact.</p>
<div class="tbl"><table><thead><tr><th>Material</th><th>g/cm³</th><th>lb/in³</th><th>kg/m³</th></tr></thead><tbody>{dens_rows}</tbody></table></div>
<h2>Weight of steel plate per square foot</h2>
<p>A quick rule for carbon steel plate: each 1/8 in of thickness weighs about <b>5.1 lb per square foot</b> (40.8 lb/ft² per inch of thickness). In metric, steel sheet weighs <b>7.85 kg per m² for every millimeter</b> of thickness.</p>
<h2>From weight to a price</h2>
<p>Material is only part of the cost of a finished part. Cutting, bending, machining, setup and scrap usually cost more than the metal itself. <a href="laser-cutting-cost-calculator.html">Laser cutting cost</a> and <a href="cnc-machining-cost-calculator.html">CNC machining cost</a> calculators add those steps, and InCost does it for real drawings.</p>
'''
metal_faq = [
    ('How much does a 4×8 sheet of steel weigh?', 'A 4×8 ft sheet of 16 gauge (0.0598 in) carbon steel weighs about 78 lb (35 kg). A 1/4 in thick 4×8 plate weighs about 327 lb (148 kg). Weight grows directly with thickness.'),
    ('How much does steel weigh per cubic inch?', 'Carbon steel weighs about 0.2836 lb per cubic inch (7.85 g/cm³). Stainless 304 is slightly heavier at 0.286 lb/in³, and aluminum 6061 is about a third of steel at 0.0975 lb/in³.'),
    ('Is aluminum lighter than steel?', 'Yes. Aluminum is about 2.9 times lighter than steel for the same size part: 2.70 g/cm³ versus 7.85 g/cm³.'),
    ('How do I calculate the weight of a steel pipe?', 'Choose “Round tube / pipe”, enter the outside diameter, wall thickness and length. The calculator subtracts the hollow inside from the outside area and multiplies by length and density.'),
    ('Can I calculate the weight of parts from a DXF or STEP file?', 'Yes, with InCost for Windows. It reads DXF and STEP files, calculates weight and area automatically, and turns them into a priced quote.'),
]

# ============================ 2. 3D PRINT COST ============================
FIL = [('PLA', 20), ('PETG', 22), ('ABS', 20), ('ASA', 28), ('TPU', 32), ('Nylon (PA12)', 45), ('PC', 40), ('Carbon fiber PLA', 38), ('Resin (SLA)', 40)]
fil_opts = ''.join(f'<option value="{p}">{n} · ${p}/kg</option>' for n, p in FIL)
print_calc = f'''
<section class="calc" aria-label="3D print cost calculator">
<div class="inputs">
<div class="r2"><div class="f"><label for="fil">Material</label><select id="fil">{fil_opts}</select></div>
<div class="f"><label for="spool">Spool price, $</label><input id="spool" type="number" inputmode="decimal" step="0.01" min="0" value="20"></div></div>
<div class="r2"><div class="f"><label for="spoolg">Spool weight, g</label><input id="spoolg" type="number" inputmode="numeric" step="1" min="1" value="1000"></div>
<div class="f"><label for="wt">Part weight, g</label><input id="wt" type="number" inputmode="decimal" step="0.1" min="0" value="45"><small>From your slicer, including supports</small></div></div>
<div class="r2"><div class="f"><label for="hh">Print time, hours</label><input id="hh" type="number" inputmode="numeric" step="1" min="0" value="3"></div>
<div class="f"><label for="mm">+ minutes</label><input id="mm" type="number" inputmode="numeric" step="1" min="0" max="59" value="20"></div></div>
<div class="r3"><div class="f"><label for="pw">Printer power, W</label><input id="pw" type="number" inputmode="numeric" step="1" min="0" value="150"></div>
<div class="f"><label for="kwh">Electricity, $/kWh</label><input id="kwh" type="number" inputmode="decimal" step="0.01" min="0" value="0.17"></div>
<div class="f"><label for="fail">Failure rate, %</label><input id="fail" type="number" inputmode="numeric" step="1" min="0" max="90" value="5"></div></div>
<div class="r2"><div class="f"><label for="pp">Printer price, $</label><input id="pp" type="number" inputmode="decimal" step="1" min="0" value="800"></div>
<div class="f"><label for="life">Printer life, hours</label><input id="life" type="number" inputmode="numeric" step="100" min="1" value="5000"></div></div>
<div class="r3"><div class="f"><label for="lab">Labor, minutes</label><input id="lab" type="number" inputmode="numeric" step="1" min="0" value="10"><small>Prep and post-processing</small></div>
<div class="f"><label for="rate">Labor rate, $/h</label><input id="rate" type="number" inputmode="decimal" step="1" min="0" value="25"></div>
<div class="f"><label for="mk">Markup, %</label><input id="mk" type="number" inputmode="numeric" step="1" min="0" value="40"></div></div>
<div class="f"><label for="qty">Quantity</label><input id="qty" type="number" inputmode="numeric" step="1" min="1" value="1"></div>
</div>
<div class="out" aria-live="polite">
<div><div class="lbl">Selling price per part</div><div class="big" id="price">—</div></div>
<div class="bar" id="bar" aria-hidden="true"></div>
<div class="legend" id="legend"></div>
<div class="lines" id="lines"></div>
<p class="err" id="err" hidden></p>
</div>
</section>'''
print_js = r'''
var C=["#0B5CFF","#7A5CFF","#0C8A5B","#F59E0B","#C2410C"];
$("fil").addEventListener("change",function(){$("spool").value=this.value;calc()});
function calc(){
  var g=num("wt"),sp=num("spool"),sg=num("spoolg"),h=(num("hh")||0)+(num("mm")||0)/60,pw=num("pw")||0,kwh=num("kwh")||0,fail=Math.min(90,Math.max(0,num("fail")||0))/100,
      pp=num("pp")||0,life=num("life")||1,lab=num("lab")||0,rate=num("rate")||0,mk=num("mk")||0,q=Math.max(1,Math.round(num("qty")||1));
  var err=(g>0&&sp>=0&&sg>0)?"":"Enter part weight, spool price and spool weight.";
  $("err").hidden=!err;$("err").textContent=err;if(err){$("price").textContent="—";$("lines").innerHTML="";$("bar").innerHTML="";$("legend").innerHTML="";return}
  var k=1/(1-fail);
  var mat=g/sg*sp*k, el=pw/1000*h*kwh*k, mach=pp/life*h*k, labor=lab/60*rate;
  var cost=mat+el+mach+labor, price=cost*(1+mk/100);
  $("price").textContent=money(price);
  var parts=[["Filament",mat],["Electricity",el],["Machine wear",mach],["Labor",labor],["Profit",price-cost]];
  $("bar").innerHTML=parts.map(function(p,i){return '<i style="width:'+(price>0?p[1]/price*100:0)+'%;background:'+C[i]+'"></i>'}).join("");
  $("legend").innerHTML=parts.map(function(p,i){return '<span><i style="background:'+C[i]+'"></i>'+p[0]+'</span>'}).join("");
  var o=row("Filament ("+f(g*k,1)+" g incl. failures)",money(mat))+row("Electricity ("+f(pw/1000*h*k,2)+" kWh)",money(el))+row("Machine wear ("+f(h,2)+" h)",money(mach))+row("Labor",money(labor))+row("Total cost",money(cost))+row("Profit ("+f(mk,0)+"%)",money(price-cost));
  if(q>1)o+=row("Order of "+q+" parts",money(price*q));
  o+=row("Cost per hour of printing",money(h>0?cost/h:0));
  $("lines").innerHTML=o;
}
[].forEach.call(document.querySelectorAll(".inputs input"),function(i){i.addEventListener("input",calc)});
calc();
'''
fil_rows = ''.join(f'<tr><td>{n}</td><td>${p}</td><td>${p/1000*45:.2f}</td></tr>' for n, p in FIL)
print_article = f'''
<h2>How 3D printing cost is calculated</h2>
<p>A print costs more than the filament it uses. This calculator adds the four costs that matter for FDM and resin printing, then applies your markup.</p>
<div class="formula">Filament     = part weight ÷ spool weight × spool price ÷ (1 − failure rate)
Electricity  = printer power (kW) × print hours × $/kWh ÷ (1 − failure rate)
Machine wear = printer price ÷ printer life (h) × print hours ÷ (1 − failure rate)
Labor        = prep and post-processing minutes ÷ 60 × labor rate
Price        = (filament + electricity + machine wear + labor) × (1 + markup)</div>
<p>Failed prints are spread over the good ones: with a 5% failure rate, every good part carries about 5% extra filament, power and machine time.</p>
<h3>Example</h3>
<p>A 45 g PLA bracket that prints in 3 h 20 min on a 150 W printer: filament $0.95, electricity $0.09, machine wear $0.56, 10 minutes of labor $4.17. Total cost is about <b>$5.77</b>, and with a 40% markup the price is about <b>$8.08</b>. Labor is often the biggest cost on small parts.</p>
<h2>Filament prices</h2>
<p>Typical prices per kilogram used as presets. Change the spool price to match what you pay.</p>
<div class="tbl"><table><thead><tr><th>Material</th><th>Price per kg</th><th>Cost of 45 g</th></tr></thead><tbody>{fil_rows}</tbody></table></div>
<h2>How much should I charge for 3D printing?</h2>
<p>Most print shops price at cost plus 30–100%, with a minimum order of $10–25 to cover setup and handling. Charge more for engineering materials, tight tolerances, rush jobs and finishing such as sanding, painting or inserts.</p>
<p>To quote faster, load the STL, 3MF or STEP file into <a href="./">InCost</a>. It finds the volume and filament weight, estimates print time for 31 printer models, picks the best orientation and prints a PDF quote.</p>
'''
print_faq = [
    ('How much does it cost to 3D print something?', 'For a typical small PLA part of 20–100 g, the material costs $0.40–2.00 and electricity a few cents. With machine wear and labor, the real cost is usually $2–10, and shops charge $5–30.'),
    ('How much electricity does a 3D printer use?', 'A typical FDM printer uses 100–250 W while printing, mostly for the heated bed. A 5-hour print at 150 W uses 0.75 kWh, about 13 cents at $0.17 per kWh.'),
    ('How do I know how much filament a print uses?', 'Your slicer (Cura, PrusaSlicer, Bambu Studio, OrcaSlicer) shows the filament weight in grams and the print time after slicing. Use those numbers, including supports.'),
    ('Should I include failed prints in the price?', 'Yes. If one print in twenty fails, every good print should carry a share of the wasted material and machine time. Enter your failure rate and the calculator spreads it automatically.'),
    ('Can InCost calculate print cost from an STL file?', 'Yes. InCost reads STL, 3MF and STEP files, calculates volume, filament weight and print time, suggests the best orientation and profile, and creates a quote.'),
]

# ============================ 3. LASER CUTTING ============================
LMAT = [('Mild steel (CRS / A36)', 0.2836, 0.75, 1.00), ('Stainless steel 304', 0.2865, 2.40, 0.75), ('Aluminum 5052', 0.0968, 3.20, 0.85), ('Galvanized steel', 0.2836, 0.95, 0.95)]
lmat_opts = ''.join(f'<option value="{i}">{n}</option>' for i, (n, d, p, k) in enumerate(LMAT))
THK_IN = [('24 ga · 0.024 in', 0.0239), ('20 ga · 0.036 in', 0.0359), ('18 ga · 0.048 in', 0.0478), ('16 ga · 0.060 in', 0.0598), ('14 ga · 0.075 in', 0.0747), ('12 ga · 0.105 in', 0.1046), ('11 ga · 0.120 in', 0.1196), ('3/16 in', 0.1875), ('1/4 in', 0.25), ('3/8 in', 0.375), ('1/2 in', 0.5)]
THK_MM = [0.5, 0.8, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12]
laser_calc = f'''
<section class="calc" aria-label="Laser cutting cost calculator">
<div class="inputs">
<div class="seg" id="units" role="group" aria-label="Units"><button type="button" data-v="in" aria-pressed="true">Inches · lb</button><button type="button" data-v="mm" aria-pressed="false">Millimeters · kg</button></div>
<div class="r2"><div class="f"><label for="mat">Material</label><select id="mat">{lmat_opts}</select></div>
<div class="f"><label for="th">Thickness</label><select id="th"></select></div></div>
<div class="r2"><div class="f"><label for="w" id="wL">Part width</label><input id="w" type="number" inputmode="decimal" step="any" min="0"></div>
<div class="f"><label for="h" id="hL">Part height</label><input id="h" type="number" inputmode="decimal" step="any" min="0"></div></div>
<div class="r3"><div class="f"><label for="holes">Holes</label><input id="holes" type="number" inputmode="numeric" step="1" min="0" value="4"></div>
<div class="f"><label for="hd" id="hdL">Hole diameter</label><input id="hd" type="number" inputmode="decimal" step="any" min="0"></div>
<div class="f"><label for="extra" id="exL">Extra cut length</label><input id="extra" type="number" inputmode="decimal" step="any" min="0" value="0"><small>Slots, cutouts</small></div></div>
<div class="r3"><div class="f"><label for="qty">Quantity</label><input id="qty" type="number" inputmode="numeric" step="1" min="1" value="50"></div>
<div class="f"><label for="rate">Laser rate, $/h</label><input id="rate" type="number" inputmode="decimal" step="1" min="0" value="120"></div>
<div class="f"><label for="setup">Setup, $</label><input id="setup" type="number" inputmode="decimal" step="1" min="0" value="35"></div></div>
<div class="r3"><div class="f"><label for="mp" id="mpL">Material $/lb</label><input id="mp" type="number" inputmode="decimal" step="0.01" min="0"></div>
<div class="f"><label for="scrap">Scrap, %</label><input id="scrap" type="number" inputmode="numeric" step="1" min="0" value="15"></div>
<div class="f"><label for="mg">Margin, %</label><input id="mg" type="number" inputmode="numeric" step="1" min="0" value="20"></div></div>
<div class="f"><label for="spd" id="spdL">Cutting speed</label><input id="spd" type="number" inputmode="decimal" step="any" min="0"><small id="spdH">Filled from thickness and material; change it to match your machine</small></div>
</div>
<div class="out" aria-live="polite">
<div><div class="lbl">Price per part</div><div class="big" id="price">—</div></div>
<div class="lines" id="lines"></div>
<p class="err" id="err" hidden></p>
</div>
</section>'''
laser_js = r'''
var LM=''' + json.dumps([[n, d, p, k] for n, d, p, k in LMAT]) + r''',TI=''' + json.dumps(THK_IN) + r''',TM=''' + json.dumps(THK_MM) + r''';
var SP=[[.024,330],[.036,300],[.048,260],[.06,220],[.075,180],[.105,130],[.12,110],[.1875,70],[.25,50],[.375,30],[.5,20]];
function speedIn(t){if(t<=SP[0][0])return SP[0][1];for(var i=1;i<SP.length;i++)if(t<=SP[i][0]){var a=SP[i-1],b=SP[i];return a[1]+(b[1]-a[1])*(t-a[0])/(b[0]-a[0])}return 20*0.5/t}
var U=load("incost-units")||defaultUnits(),spdTouched=false;
function thkIn(){var v=+$("th").value;return U==="in"?v:v/25.4}
function setUnits(conv){
  var mm=U==="mm",u=mm?"mm":"in",idx=$("th").selectedIndex;
  $("th").innerHTML=mm?TM.map(function(t){return '<option value="'+t+'">'+t+' mm</option>'}).join(""):TI.map(function(t){return '<option value="'+t[1]+'">'+t[0]+'</option>'}).join("");
  $("th").selectedIndex=idx>=0?Math.min(idx,$("th").options.length-1):(mm?3:3);
  [["wL","Part width"],["hL","Part height"],["hdL","Hole diameter"],["exL","Extra cut length"]].forEach(function(x){$(x[0]).textContent=x[1]+", "+u});
  if(conv){["w","h","hd","extra"].forEach(function(id){var v=num(id);if(isFinite(v))$(id).value=mm?+(v*25.4).toFixed(1):+(v/25.4).toFixed(3)});var p=num("mp");if(isFinite(p))$("mp").value=mm?+(p*2.2046).toFixed(2):+(p/2.2046).toFixed(2)}
  $("mpL").textContent=mm?"Material $/kg":"Material $/lb";
  $("spdL").textContent=mm?"Cutting speed, mm/min":"Cutting speed, in/min";
  spdTouched=false;autoSpeed();calc();
}
function autoSpeed(){if(spdTouched)return;var s=speedIn(thkIn())*LM[+$("mat").value][3];$("spd").value=U==="mm"?Math.round(s*25.4):Math.round(s)}
function calc(){
  var mm=U==="mm",k=mm?1/25.4:1,m=LM[+$("mat").value];
  var w=num("w")*k,h=num("h")*k,n=Math.max(0,Math.round(num("holes")||0)),hd=(num("hd")||0)*k,ex=(num("extra")||0)*k,t=thkIn();
  var q=Math.max(1,Math.round(num("qty")||1)),rate=num("rate")||0,setup=num("setup")||0,mp=num("mp"),scrap=(num("scrap")||0)/100,mg=(num("mg")||0)/100,spd=num("spd")*k;
  var err="";if(!(w>0&&h>0))err="Enter the part width and height.";else if(n&&!(hd>0))err="Enter the hole diameter.";else if(!(spd>0))err="Enter a cutting speed.";
  $("mp").placeholder=(mm?(m[2]*2.2046).toFixed(2):m[2].toFixed(2))+" (typical)";
  if(!(mp>=0))mp=mm?m[2]*2.2046:m[2];
  $("err").hidden=!err;$("err").textContent=err;if(err){$("price").textContent="—";$("lines").innerHTML="";return}
  var mpLb=mm?mp/2.2046:mp;
  var lb=w*h*t*m[1], area=w*h-n*Math.PI*hd*hd/4, netLb=Math.max(0,area)*t*m[1];
  var cut=2*(w+h)+n*Math.PI*hd+ex, pierces=1+n+(ex>0?1:0), pierceS=0.5+8*t;
  var minutes=cut/spd+pierces*pierceS/60;
  var matC=lb*(1+scrap)*mpLb, cutC=minutes/60*rate, setC=setup/q, cost=matC+cutC+setC, price=cost*(1+mg);
  $("price").textContent=money(price);
  var o=row("Material ("+(mm?f(lb*0.4536*(1+scrap),3)+" kg":f(lb*(1+scrap),3)+" lb")+" with scrap)",money(matC))
   +row("Cut length",mm?f(cut*25.4,0)+" mm":f(cut,1)+" in")+row("Pierces",pierces)
   +row("Laser time",f(minutes,2)+" min · "+money(cutC))+row("Setup per part",money(setC))+row("Cost per part",money(cost))
   +row("Finished part weight",mm?f(netLb*0.4536,3)+" kg":f(netLb,3)+" lb")+row("Order total ("+q+" pcs)",money(price*q));
  $("lines").innerHTML=o;
}
$("mat").addEventListener("change",function(){$("mp").value="";autoSpeed();calc()});
$("th").addEventListener("change",function(){autoSpeed();calc()});
$("spd").addEventListener("input",function(){spdTouched=true;calc()});
["w","h","holes","hd","extra","qty","rate","setup","mp","scrap","mg"].forEach(function(i){$(i).addEventListener("input",calc)});
seg("units",function(v){if(v!==U){U=v;store("incost-units",v);setUnits(true)}});
setSeg("units",U);
if(U==="mm"){$("w").value=150;$("h").value=100;$("hd").value=6}else{$("w").value=6;$("h").value=4;$("hd").value=0.25}
setUnits(false);
'''
laser_article = '''
<h2>How laser cutting is priced</h2>
<p>Laser shops price a flat part from three things: the material in the blank, the time the laser spends cutting and piercing, and the setup spread over the order.</p>
<div class="formula">Material   = blank W × H × thickness × density × (1 + scrap) × $/lb
Cut length = perimeter + holes × π × d + other cutouts
Laser time = cut length ÷ cutting speed + pierces × pierce time
Cutting    = laser time × machine rate
Setup      = setup cost ÷ quantity
Price      = (material + cutting + setup) × (1 + margin)</div>
<h3>Why cut length matters more than size</h3>
<p>A small bracket with many holes can cost more than a larger plain plate. Every hole adds cut length and a pierce, and piercing thick plate takes several seconds. Fewer, larger cutouts cut faster than many small ones.</p>
<h3>Typical fiber laser cutting speeds for mild steel</h3>
<div class="tbl"><table><thead><tr><th>Thickness</th><th>Speed, in/min</th><th>Speed, mm/min</th></tr></thead><tbody>
<tr><td>18 ga (1.2 mm)</td><td>260</td><td>6,600</td></tr><tr><td>16 ga (1.5 mm)</td><td>220</td><td>5,600</td></tr>
<tr><td>11 ga (3 mm)</td><td>110</td><td>2,800</td></tr><tr><td>1/4 in (6 mm)</td><td>50</td><td>1,270</td></tr><tr><td>1/2 in (12 mm)</td><td>20</td><td>510</td></tr></tbody></table></div>
<p>These are conservative values for a 3–6 kW fiber laser. Stainless is cut about 25% slower here and aluminum about 15% slower. Use your own machine's speeds for real quotes.</p>
<h2>Typical laser cutting rates</h2>
<p>Most US job shops charge $80–200 per hour of laser time, plus a setup or minimum order charge of $25–75. High-power fiber lasers cut thin sheet several times faster than CO₂ lasers, so the price per part drops even when the hourly rate is higher.</p>
<p>Measuring cut length by hand is the slow part. <a href="./">InCost</a> reads the DXF, finds every contour, counts pierces, nests the parts on a standard sheet and prices them with your own rates.</p>
'''
laser_faq = [
    ('How much does laser cutting cost per hour?', 'Shop rates for fiber laser cutting are usually $80–200 per hour of machine time in the US, and €60–150 in Europe. The price per part also includes material, setup and margin.'),
    ('How is laser cutting priced per inch?', 'Divide the hourly rate by the cutting speed. At $120/h and 220 in/min on 16 gauge steel, cutting costs about $0.009 per inch, plus a fraction of a cent per pierce.'),
    ('Why do small parts have a minimum price?', 'Every job needs programming, loading the sheet and unloading parts. A setup charge spread over the order makes small quantities cost more per part.'),
    ('What is a pierce and why does it cost extra?', 'Before cutting each contour, the laser burns a starting hole through the material. On thick plate this takes several seconds, so parts with many holes take longer to cut.'),
    ('Can I get the cut length from a DXF file?', 'Yes. InCost reads DXF files and measures cut length and pierces automatically, including tabs, lead-ins and nested parts.'),
]

# ============================ 4. CNC MACHINING ============================
CMAT = [('Aluminum 6061-T6', 2.70, 4.50), ('Aluminum 7075-T6', 2.81, 9.00), ('Steel 1018', 7.87, 1.20), ('Steel 4140', 7.85, 2.00), ('Stainless 304', 7.93, 3.50), ('Stainless 316', 8.00, 4.50), ('Brass C360', 8.50, 4.50), ('Titanium Gr 5', 4.43, 30.0), ('Delrin (POM)', 1.41, 5.00), ('Nylon 6/6', 1.14, 4.00), ('PEEK', 1.31, 60.0)]
cmat_opts = ''.join(f'<option value="{i}">{n} · ${p}/lb</option>' for i, (n, d, p) in enumerate(CMAT))
cnc_calc = f'''
<section class="calc" aria-label="CNC machining cost calculator">
<div class="inputs">
<div class="seg" id="units" role="group" aria-label="Units"><button type="button" data-v="in" aria-pressed="true">Inches · lb</button><button type="button" data-v="mm" aria-pressed="false">Millimeters · kg</button></div>
<div class="r2"><div class="f"><label for="mat">Material</label><select id="mat">{cmat_opts}</select></div>
<div class="f"><label for="stock">Stock</label><select id="stock"><option value="block">Block / plate</option><option value="bar">Round bar</option></select></div></div>
<div class="r3" id="dims"></div>
<div class="r3"><div class="f"><label for="cyc">Cycle time, min</label><input id="cyc" type="number" inputmode="decimal" step="any" min="0" value="12"><small>Machine time per part</small></div>
<div class="f"><label for="setup">Setup, min</label><input id="setup" type="number" inputmode="numeric" step="1" min="0" value="60"><small>Per order</small></div>
<div class="f"><label for="prog">Programming, min</label><input id="prog" type="number" inputmode="numeric" step="1" min="0" value="45"><small>One time</small></div></div>
<div class="r3"><div class="f"><label for="rate">Shop rate, $/h</label><input id="rate" type="number" inputmode="decimal" step="1" min="0" value="85"></div>
<div class="f"><label for="fin">Finishing, $/part</label><input id="fin" type="number" inputmode="decimal" step="0.01" min="0" value="0"><small>Anodize, plating</small></div>
<div class="f"><label for="mg">Margin, %</label><input id="mg" type="number" inputmode="numeric" step="1" min="0" value="20"></div></div>
<div class="r2"><div class="f"><label for="qty">Quantity</label><input id="qty" type="number" inputmode="numeric" step="1" min="1" value="10"></div>
<div class="f"><label for="mp" id="mpL">Material price, $/lb</label><input id="mp" type="number" inputmode="decimal" step="0.01" min="0" value="4.50"></div></div>
</div>
<div class="out" aria-live="polite">
<div><div class="lbl">Price per part</div><div class="big" id="price">—</div></div>
<div class="lines" id="lines"></div>
<div><div class="lbl" style="margin-bottom:6px">Price per part by quantity</div><table class="q" id="qt"></table></div>
<p class="err" id="err" hidden></p>
</div>
</section>'''
cnc_js = r'''
var CM=''' + json.dumps([[n, d, p] for n, d, p in CMAT]) + r''';
var ST={block:[["l","Length",4,100],["w","Width",3,75],["h","Height",1,25]],bar:[["d","Diameter",1.5,40],["l","Length",3,75]]};
var U=load("incost-units")||defaultUnits();
function build(conv){
  var s=$("stock").value,u=U==="in"?"in":"mm";
  $("dims").innerHTML=ST[s].map(function(d){return '<div class="f"><label for="d_'+d[0]+'">Stock '+d[1].toLowerCase()+', '+u+'</label><input id="d_'+d[0]+'" type="number" inputmode="decimal" step="any" min="0" value="'+(U==="in"?d[2]:d[3])+'"></div>'}).join("");
  [].forEach.call($("dims").querySelectorAll("input"),function(i){i.addEventListener("input",calc)});
  $("mpL").textContent=U==="in"?"Material price, $/lb":"Material price, $/kg";
  if(conv){var p=num("mp");if(isFinite(p))$("mp").value=U==="mm"?(p*2.2046).toFixed(2):(p/2.2046).toFixed(2)}
  calc();
}
function unitPrice(q,c){return (c.mat+c.cyc/60*c.rate+(c.setup+c.prog)/60*c.rate/q+c.fin)*(1+c.mg)}
function calc(){
  var mm=U==="mm",k=mm?0.1:2.54,g=function(n){return num("d_"+n)*k},m=CM[+$("mat").value],vol;
  vol=$("stock").value==="block"?g("l")*g("w")*g("h"):Math.PI/4*Math.pow(g("d"),2)*g("l");
  var err=vol>0?"":"Enter the stock size.";
  $("err").hidden=!err;$("err").textContent=err;if(err){$("price").textContent="—";$("lines").innerHTML="";$("qt").innerHTML="";return}
  var kg=vol*m[1]/1000*1.05,lb=kg*2.2046,mp=num("mp")||0,matC=mm?kg*mp:lb*mp;
  var c={mat:matC,cyc:num("cyc")||0,setup:num("setup")||0,prog:num("prog")||0,rate:num("rate")||0,fin:num("fin")||0,mg:(num("mg")||0)/100};
  var q=Math.max(1,Math.round(num("qty")||1)),price=unitPrice(q,c);
  $("price").textContent=money(price);
  $("lines").innerHTML=row("Stock ("+(mm?f(kg,3)+" kg":f(lb,3)+" lb")+" incl. 5% saw cut)",money(matC))
    +row("Machining ("+f(c.cyc,1)+" min)",money(c.cyc/60*c.rate))
    +row("Setup + programming per part",money((c.setup+c.prog)/60*c.rate/q))
    +(c.fin?row("Finishing",money(c.fin)):"")
    +row("Order total ("+q+" pcs)",money(price*q))
    +row("Lead cost share of setup",f((c.setup+c.prog)/60*c.rate/q/(price/(1+c.mg))*100,0)+"%");
  var qs=[1,5,10,25,50,100,500];
  $("qt").innerHTML="<tr><th>Qty</th><th>Per part</th><th>Order</th></tr>"+qs.map(function(x){var p=unitPrice(x,c);return "<tr"+(x===q?' style="font-weight:700"':"")+"><td>"+x+"</td><td>"+money(p)+"</td><td>"+money(p*x)+"</td></tr>"}).join("");
}
$("mat").addEventListener("change",function(){var p=CM[+this.value][2];$("mp").value=U==="mm"?(p*2.2046).toFixed(2):p.toFixed(2);calc()});
$("stock").addEventListener("change",function(){build(false)});
["cyc","setup","prog","rate","fin","mg","qty","mp"].forEach(function(i){$(i).addEventListener("input",calc)});
seg("units",function(v){if(v!==U){U=v;store("incost-units",v);build(true)}});
setSeg("units",U);if(U==="mm")$("mp").value=(4.5*2.2046).toFixed(2);build(false);
'''
cnc_article = '''
<h2>How CNC machining cost is calculated</h2>
<p>A machined part costs the stock it is cut from, the machine time per part, and the setup and programming time shared across the order.</p>
<div class="formula">Material   = stock volume × density × 1.05 × $/lb
Machining  = cycle time × shop rate
Setup      = (setup + programming time) × shop rate ÷ quantity
Price      = (material + machining + setup + finishing) × (1 + margin)</div>
<h3>Why one part costs so much more than ten</h3>
<p>Programming and setting up a job can take one to two hours. On a single part that time is all yours; on a hundred parts it is a few cents each. The quantity table shows how fast the unit price falls.</p>
<h3>Typical CNC shop rates</h3>
<div class="tbl"><table><thead><tr><th>Machine</th><th>Typical US rate</th></tr></thead><tbody>
<tr><td>Manual mill or lathe</td><td>$50–75 / h</td></tr><tr><td>3-axis CNC mill</td><td>$75–120 / h</td></tr>
<tr><td>CNC lathe</td><td>$70–110 / h</td></tr><tr><td>5-axis CNC mill</td><td>$120–200 / h</td></tr><tr><td>Swiss-type lathe</td><td>$90–150 / h</td></tr></tbody></table></div>
<h2>How to estimate cycle time</h2>
<p>Add the time of each operation: roughing, finishing, drilling and tapping, plus tool changes and part loading. For a quick first estimate, divide the volume of material removed by a realistic removal rate, for example 1–3 in³/min in aluminum on a typical 3-axis mill and 0.2–0.5 in³/min in steel.</p>
<p><a href="./">InCost</a> estimates milling and turning from stock size and operations, keeps your shop rates and materials, and prints quotes and travelers with setup and cycle times.</p>
'''
cnc_faq = [
    ('How much does CNC machining cost per hour?', 'In the US, 3-axis CNC milling typically costs $75–120 per hour and 5-axis $120–200 per hour. In Europe rates are usually €50–100 per hour.'),
    ('Why is a single CNC part so expensive?', 'Programming and setup can take 1–2 hours regardless of quantity. On one part the whole setup cost is in the price; on 100 parts it is spread thin.'),
    ('How much stock should I add around the part?', 'Usually 1/8 in (3 mm) per side for blocks and 1/16–1/8 in on diameter for round bar, plus the saw cut. The calculator adds 5% to the stock weight for the saw cut.'),
    ('Which is cheaper to machine, aluminum or steel?', 'Aluminum is usually cheaper overall. It costs more per pound than mild steel, but it machines three to five times faster, so machine time, the biggest cost, is much lower.'),
    ('Can InCost estimate machining from a STEP file?', 'InCost reads STEP models, recognizes turned, milled and sheet metal parts, and estimates cost. It can also create shop drawings from the model.'),
]

out = {
  'metal-weight-calculator.html': page('metal-weight-calculator.html', 'Metal Weight Calculator', '', 'Metal Weight Calculator',
     'Calculate the weight of steel, aluminum, stainless, brass and other metals for plate, bar, tube and angle. Inches or millimeters, pounds or kilograms.',
     metal_calc, metal_js, metal_article, metal_faq,
     'Free metal weight calculator for steel, aluminum, stainless, brass and copper plate, round bar, tube, pipe and angle. Weight per piece, per foot and per meter, in lb and kg.',
     'Metal Weight Calculator — Steel, Aluminum, Stainless Plate, Bar & Tube | InCost'),
  '3d-print-cost-calculator.html': page('3d-print-cost-calculator.html', '3D Print Cost Calculator', '', '3D Print Cost Calculator',
     'Work out what a 3D print really costs: filament, electricity, machine wear, failed prints and labor, then the price to charge.',
     print_calc, print_js, print_article, print_faq,
     'Free 3D printing cost calculator. Filament cost, electricity, printer wear, failure rate, labor and markup to find the price per print for PLA, PETG, ABS, TPU, nylon and resin.',
     '3D Print Cost Calculator — Filament, Electricity & Price per Print | InCost'),
  'laser-cutting-cost-calculator.html': page('laser-cutting-cost-calculator.html', 'Laser Cutting Cost Calculator', '', 'Laser Cutting Cost Calculator',
     'Estimate the price of a laser-cut sheet metal part from its size, holes, material, thickness and your machine rate.',
     laser_calc, laser_js, laser_article, laser_faq,
     'Free laser cutting cost calculator for sheet metal. Price per part from cut length, pierces, material, gauge or thickness, laser rate, setup and margin. Steel, stainless and aluminum.',
     'Laser Cutting Cost Calculator — Sheet Metal Price per Part | InCost'),
  'cnc-machining-cost-calculator.html': page('cnc-machining-cost-calculator.html', 'CNC Machining Cost Calculator', '', 'CNC Machining Cost Calculator',
     'Estimate the cost of a CNC milled or turned part from stock, cycle time, setup and shop rate, and see how the price changes with quantity.',
     cnc_calc, cnc_js, cnc_article, cnc_faq,
     'Free CNC machining cost calculator. Stock material, cycle time, setup, programming, shop rate and margin, with price per part from 1 to 500 pieces. Aluminum, steel, stainless, brass, plastics.',
     'CNC Machining Cost Calculator — Price per Part by Quantity | InCost'),
}
for fn, txt in out.items():
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(txt)
print('written', list(out))
