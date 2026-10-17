"""Builds the new RESET homepage.
  python3 tools/build_home.py           -> preview/index.html (noindex, for review)
  python3 tools/build_home.py --live    -> index.html (replaces the live homepage)
Reuses the head, nav, styles and footer from the current index.html shell, so the RESET look stays identical."""
import re, sys, pathlib, html as H
ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE = "--live" in sys.argv
SRC = ROOT / "index.html" if not (ROOT / "tools/_shell.html").exists() else ROOT / "tools/_shell.html"
shell = SRC.read_text()
if not (ROOT / "tools/_shell.html").exists():
    (ROOT / "tools/_shell.html").write_text(shell)   # freeze the original shell once
r = "" if LIVE else "../"

head_end = shell.index('<section class="dark hero" id="programs">')
foot_start = shell.index("<footer>")
head = shell[:head_end]
foot = shell[foot_start:]

def fix_paths(s):
    if LIVE: return s
    s = re.sub(r'(href|src)="(?!https?:|#|data:|mailto:|tel:|/)([^"]*)"', lambda m: f'{m.group(1)}="../{m.group(2)}"', s)
    return s.replace('href="../"', 'href="../"')
head = fix_paths(head); foot = fix_paths(foot)
if not LIVE:
    head = head.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">')

FAQ = [
 ("Who are RESET programs for?", "Adults dealing with back, neck, knee, shoulder or hip pain, athletes who want to perform and stay healthy, and anyone ready to lose fat and keep muscle. Each program meets you where you are."),
 ("Do I need a gym?", "No. Every exercise has a home version using a band and a pair of dumbbells or a kettlebell. Gym options are listed for every exercise."),
 ("How long is a program?", "Each block is 12 weeks in four phases. A full track is four blocks, one year, because strength you stop building fades."),
 ("What's the difference between the tiers?", "Self-Guided is the full Block 01 guide and video library, yours for life. Custom adds an onboarding call, programming tailored to you and weekly guidance. Doctor-Led adds weekly meetings with Dr. Urrutia."),
 ("Is RESET medical care?", "No. RESET programs are education and exercise. They don't diagnose or treat any condition. The check-in screens for warning signs that need a doctor first."),
 ("Can I cancel?", "Yes. Custom and Doctor-Led are month to month. Cancel anytime before your next billing date."),
 ("Is it available in Spanish?", "Yes. Every program is available in English and Spanish."),
]
faq_html = "".join(f"<details><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>" for q, a in FAQ)
faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

PROGRAMS = [
 ("Rehab", "Get out of pain and build it back stronger.", [
   ("back", "Low Back", "Recurring low back pain, stiffness and flare-ups."),
   ("neck", "Neck", "Desk neck, stiffness, tension headaches and arm symptoms."),
   ("knee", "Knee", "Front-of-knee pain, stiff or arthritic knees, post-injury rebuilding."),
   ("shoulder", "Shoulder", "Painful overhead reach, rotator cuff irritation, stiff shoulders."),
   ("hip", "Hip", "Side-of-hip pain, groin pain and stiff or arthritic hips.")]),
 ("Performance", "Train the body your sport needs.", [
   ("golf", "Golf", "More distance, a swing that doesn't hurt, a body that lasts 18 holes."),
   ("pickleball", "Pickleball", "Faster feet, fewer tweaks, a body that plays several days a week."),
   ("dance", "Dance", "Return to dance after injury, then build strength, jumps and stamina."),
   ("student-athlete", "Student Athlete", "Off-season to post-season training for young athletes.")]),
 ("Nutrition", "Lose fat, keep muscle, keep it off.", [
   ("nutrition", "Nutrition", "Lose fat without losing muscle, then keep it off for good.")]),
]
n = 0; finder = ""
for g, d, items in PROGRAMS:
    tiles = ""
    for slug, name, desc in items:
        n += 1
        tiles += f'<a class="rv-prog" href="{r}{slug}/"><span class="num">{n:02d}</span><h3>{name}</h3><p>{H.escape(desc)}</p><span class="go">See the program <span class="arr">→</span></span></a>'
    finder += f'<div class="rv-group"><div class="rv-gh"><h3>{g}</h3><p>{d}</p></div><div class="rv-progs">{tiles}</div></div>'

import json
ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [faq_ld]}) + "</script>"

CSS = """<style>
/* ---------- RESET home v2: video hero, floating boxes, section labels ---------- */
.rst .nav{background:rgba(17,20,16,.78);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
.rst .rv-hero{position:relative;overflow:hidden;color:var(--cream);background:var(--night);min-height:min(58svh,540px);display:flex;align-items:flex-end;padding:0}
.rst .rv-hero video,.rst .rv-hero .poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.rst .rv-hero:after{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(17,20,16,.62),rgba(17,20,16,.46) 45%,rgba(17,20,16,.78)),linear-gradient(90deg,rgba(17,20,16,.5),rgba(17,20,16,0) 70%)}
.rst .rv-hero:before{content:"";position:absolute;inset:-48px;z-index:1;background-image:linear-gradient(rgba(164,170,146,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(164,170,146,.09) 1px,transparent 1px);background-size:48px 48px;animation:rvGrid 22s linear infinite;pointer-events:none}
@keyframes rvGrid{to{transform:translate(48px,48px)}}
.rst .rv-hero .wrap{position:relative;z-index:2;width:100%;padding-top:56px;padding-bottom:84px}
.rst .rv-hero .scan{position:absolute;left:0;right:0;height:120px;top:-120px;z-index:1;background:linear-gradient(180deg,transparent,rgba(164,170,146,.07),transparent);animation:rvScan 7s ease-in-out infinite;pointer-events:none}
@keyframes rvScan{0%{top:-120px}60%,100%{top:100%}}
.rst .rv-hero .eyebrow:before{animation:rvLine 1s .2s both cubic-bezier(.2,.7,.2,1)}
@keyframes rvLine{from{width:0}to{width:22px}}
.rst.js .rv-hero .rv-offer{animation:rstFade .8s ease .8s both}
.rst .rv-hero h1{margin-top:16px;max-width:16ch;font-size:clamp(36px,5.4vw,66px)}
.rst .rv-hero .ctas{margin-top:22px}
.rst .rv-hero .sub{max-width:54ch;font-size:17px;color:#DAD4C7;margin-top:14px}
.rst .rv-hero .ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.rst .rv-hero .btn{background:var(--cream);color:var(--night);border-color:var(--cream)}
.rst .rv-hero .btn:hover{background:transparent;color:var(--cream)}
.rst .rv-hero .btn.ghost{background:transparent;color:var(--cream);border-color:rgba(237,230,218,.55)}
.rst .rv-hero .btn.ghost:hover{background:var(--cream);color:var(--night)}
.rst .rv-offer{margin-top:20px;max-width:620px;display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;padding:14px 18px;background:rgba(17,20,16,.45);border:1px solid rgba(237,230,218,.18);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);font-size:15px}
.rst .rv-offer b{font-family:var(--mono);font-weight:500;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--sage)}
.rst .rv-offer a{color:var(--cream);font-weight:700}
.rst .rv-trust{position:relative;z-index:3;margin-top:-52px;background:var(--paper);border:1px solid var(--hair);box-shadow:0 30px 60px -36px rgba(17,20,16,.6);display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0}
.rst .rv-trust div{padding:20px 20px;border-right:1px solid var(--hair)}
.rst .rv-trust div:last-child{border-right:0}
.rst .rv-trust b{display:block;font-family:var(--display);font-weight:500;font-size:clamp(22px,2.4vw,30px);text-transform:uppercase;line-height:1}
.rst .rv-trust span{display:block;font-size:13.5px;color:var(--grey);margin-top:6px;line-height:1.35}
.rst section.rv{padding-block:clamp(40px,5.5vw,72px)}
.rst .rv-box{position:relative;overflow:hidden;background:#fff;border:1px solid var(--hair);padding:clamp(24px,4vw,52px);box-shadow:0 40px 70px -55px rgba(17,20,16,.55)}
.rst .rv-box + .rv-box{margin-top:clamp(18px,2.4vw,28px)}
.rst .rv-box.night{background-color:var(--night);color:var(--cream);border-color:#262A21;background-image:linear-gradient(#1C2019 1px,transparent 1px),linear-gradient(90deg,#1C2019 1px,transparent 1px);background-size:48px 48px}
.rst .rv-box.mark:after{content:"";position:absolute;right:-30px;bottom:-14px;width:min(520px,70%);height:110px;background:var(--logo) no-repeat right bottom/contain;opacity:.06;pointer-events:none}
.rst .rv-box.night.mark:after{opacity:.09;filter:brightness(3)}
.rst .rv-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px 48px;align-items:end;margin-bottom:clamp(22px,3vw,34px)}
.rst .rv-head h2{margin-top:12px}
.rst .rv-head p{color:var(--grey);max-width:50ch}
.rst .night .rv-head p{color:#B8B3A6}
.rst .rv-group + .rv-group{margin-top:28px}
.rst .rv-gh{display:flex;flex-wrap:wrap;gap:4px 16px;align-items:baseline;border-top:1px solid var(--ink);padding-top:14px}
.rst .rv-gh h3{font-size:24px}
.rst .rv-gh p{color:var(--grey);font-size:15px}
.rst .rv-progs{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-top:14px}
.rst .rv-prog{background:var(--paper);border:1px solid var(--hair);padding:22px 20px 18px;display:flex;flex-direction:column;gap:10px;min-height:190px;text-decoration:none;transition:background .25s,color .25s}
.rst .rv-prog .num{font-family:var(--mono);font-size:12px;color:var(--olive)}
.rst .rv-prog h3{font-size:24px}
.rst .rv-prog p{color:var(--grey);font-size:14px;line-height:1.45}
.rst .rv-prog .go{margin-top:auto;font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid var(--hair);padding-top:12px}
.rst .rv-prog:hover{background:var(--olive-d);color:var(--cream)}
.rst .rv-prog:hover p{color:#D6D1C4}.rst .rv-prog:hover .num{color:var(--sage)}.rst .rv-prog:hover .go{border-color:#5A5E4C}
.rst .rv-prog:hover .arr{display:inline-block;transform:translateX(4px)}
.rst .rv-split{margin-top:clamp(28px,4vw,44px);padding-top:clamp(24px,3vw,36px);border-top:1px solid #2E3229}
.rst .rv-bar{display:flex;height:84px;margin-top:20px;background:#22261E;overflow:hidden}
.rst .rv-bar .seg{display:flex;align-items:flex-end;padding:12px 16px;font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;width:0;transition:width 1.6s cubic-bezier(.2,.7,.2,1)}
.rst .rv-bar .seg b{display:block;font-family:var(--display);font-size:34px;font-weight:500;letter-spacing:0;line-height:1;margin-bottom:4px}
.rst .rv-bar .a{background:var(--cream);color:var(--night)}
.rst .rv-bar .b{background:var(--olive);color:var(--cream);transition-delay:.35s}
.rst .rv-bar.seen .a{width:35%}.rst .rv-bar.seen .b{width:65%}
.rst .rv-legend{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:16px;font-size:15px;color:#B8B3A6}
.rst .rv-legend b{color:var(--cream)}
.rst .rv-doc{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(24px,5vw,56px);align-items:center}
.rst .rv-doc img{width:100%;max-height:540px;aspect-ratio:4/5;object-fit:cover;object-position:center 20%}
.rst .rv-doc p{color:var(--grey);margin-top:14px;font-size:16.5px}
.rst .rv-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px;padding:0;list-style:none}
.rst .rv-chips li{font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--hair);padding:7px 11px;color:var(--olive-d)}
.rst .rv-faq{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.4fr);gap:clamp(24px,5vw,64px);align-items:start}
.rst .rv-faq .faq{margin-top:0}
.rst .rv-faq > div:first-child p{color:var(--grey);margin:14px 0 22px}
.rst .rv-cta{display:grid;grid-template-columns:minmax(0,1.4fr) auto;gap:24px;align-items:center}
.rst .rv-cta p{color:#B8B3A6;margin-top:12px;max-width:52ch}
.rst .rv-cta .btns{display:flex;flex-wrap:wrap;gap:12px;position:relative;z-index:1}
.rst .rv-cta .btn.ghost{color:var(--cream);border-color:rgba(237,230,218,.5)}
.rst .rv-score{font-family:var(--display);font-weight:500;font-size:28px;color:var(--ink);display:inline-flex;align-items:center;gap:8px;margin-right:6px;vertical-align:middle}
.rst .rv-score .mini{display:inline-flex;gap:2px;color:#B4935A}.rst .rv-score .mini svg{width:14px;height:14px;animation:rvTw 3.2s ease-in-out infinite}
.rst .rv-score .mini svg:nth-child(2){animation-delay:.2s}.rst .rv-score .mini svg:nth-child(3){animation-delay:.4s}.rst .rv-score .mini svg:nth-child(4){animation-delay:.6s}.rst .rv-score .mini svg:nth-child(5){animation-delay:.8s}
@keyframes rvTw{0%,70%,100%{transform:none}80%{transform:scale(1.3)}}
.rst .rv-quotes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.rst .rv-q{position:relative;overflow:hidden;margin:0;background:var(--paper);border:1px solid var(--hair);padding:24px;display:flex;flex-direction:column;gap:14px;transition:transform .7s cubic-bezier(.2,.7,.2,1),border-color .7s,box-shadow .7s}
.rst .rv-q:before{content:"“";position:absolute;right:14px;top:-22px;font:500 130px/1 var(--serif);color:#B4935A;opacity:.14}
.rst .rv-q .stars{display:flex;gap:3px;color:#B4935A}.rst .rv-q .stars svg{width:15px;height:15px;opacity:0;transform:scale(.3) rotate(-30deg);transition:opacity .4s,transform .6s cubic-bezier(.34,1.56,.64,1)}
.rst .rv-q.in .stars svg{opacity:1;transform:none}
.rst .rv-q.in .stars svg:nth-child(2){transition-delay:.1s}.rst .rv-q.in .stars svg:nth-child(3){transition-delay:.2s}.rst .rv-q.in .stars svg:nth-child(4){transition-delay:.3s}.rst .rv-q.in .stars svg:nth-child(5){transition-delay:.4s}
.rst .rv-q p{font-family:var(--serif);font-size:22px;line-height:1.3}
.rst .rv-q cite{font-style:normal;font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--grey);margin-top:auto}
.rst .rv-q.lit{transform:translateY(-6px);border-color:rgba(180,147,90,.6);box-shadow:0 30px 50px -30px rgba(17,20,16,.5)}
.rst .rv-q:after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(180,147,90,.14) 50%,transparent 70%);transform:translateX(-120%);pointer-events:none}
.rst .rv-q.lit:after{animation:rvSheen 1.4s cubic-bezier(.2,.7,.2,1)}
@keyframes rvSheen{to{transform:translateX(120%)}}
@media (max-width:860px){.rst .rv-quotes{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){.rst .rv-q .stars svg{opacity:1;transform:none}.rst .rv-score .mini svg,.rst .rv-q.lit:after{animation:none}}
.rst .tiers{margin-top:0}
.rst{background:#E2E0D5}
.rst .rv-box{border-color:#CFCDC1}
.rst .rv-trust{background:#fff;border-color:#CFCDC1}
.rst .rv-trust div{border-color:#E2E0D5}
.rst .rv-q{background:#F4F2EB;border-color:#D3D1C5}
/* program tiles: green, rounded-but-sharp, lifted, animated on hover */
.rst .rv-progs{gap:14px}
.rst .rv-prog{position:relative;overflow:hidden;border-radius:6px;border:1px solid #50553F;background:linear-gradient(160deg,#4A4E3C 0%,#3F4335 55%,#363A2D 100%);color:var(--cream);box-shadow:0 1px 0 rgba(255,255,255,.06) inset,0 14px 24px -14px rgba(17,20,16,.55),0 4px 8px -4px rgba(17,20,16,.3);transition:transform .45s cubic-bezier(.2,.8,.2,1),box-shadow .45s cubic-bezier(.2,.8,.2,1),border-color .3s,opacity .6s ease}
.rst .rv-prog p{color:#CFCABD}
.rst .rv-prog .num{color:var(--sage)}
.rst .rv-prog .go{border-color:rgba(237,230,218,.18);color:var(--cream)}
.rst .rv-prog .arr{display:inline-block;transition:transform .35s cubic-bezier(.2,.8,.2,1)}
.rst .rv-prog:before{content:"";position:absolute;inset:0;background:linear-gradient(115deg,transparent 35%,rgba(237,230,218,.12) 50%,transparent 65%);transform:translateX(-120%);transition:transform .9s cubic-bezier(.2,.8,.2,1);pointer-events:none}
.rst .rv-prog:after{content:"";position:absolute;left:0;bottom:0;height:2px;width:0;background:var(--sage);transition:width .5s cubic-bezier(.2,.8,.2,1)}
.rst .rv-prog:hover,.rst .rv-prog:focus-visible{transform:translateY(-8px);background:linear-gradient(160deg,#565B46 0%,#4A4E3C 55%,#3F4335 100%);color:var(--cream);border-color:#6A6F57;box-shadow:0 1px 0 rgba(255,255,255,.08) inset,0 34px 44px -22px rgba(17,20,16,.6),0 10px 18px -8px rgba(17,20,16,.35)}
.rst .rv-prog:hover:before{transform:translateX(120%)}
.rst .rv-prog:hover:after{width:100%}
.rst .rv-prog:hover .num{color:var(--cream)}
.rst .rv-prog:hover p{color:#E2DDD0}
.rst .rv-prog:hover .go{border-color:rgba(237,230,218,.35)}
.rst .rv-prog:hover .arr{transform:translateX(6px)}
.rst .rv-prog:active{transform:translateY(-3px)}
@media (prefers-reduced-motion:reduce){.rst .rv-prog,.rst .rv-prog:hover{transform:none}.rst .rv-prog:before{display:none}}
.rst .rv-gh{border-color:#2A2E25}
.rst .rv-box .tier:not(.pop){background:#fff}
.rst.js .rv-box,.rst.js .rv-trust{opacity:0;transform:translateY(26px);transition:opacity .9s cubic-bezier(.2,.7,.2,1),transform .9s cubic-bezier(.2,.7,.2,1)}
.rst.js .rv-box.in,.rst.js .rv-trust.in{opacity:1;transform:none}
.rst.js .rv-prog,.rst.js .rv-path li,.rst.js .rv-trust > div{opacity:0;transform:translateY(14px);transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1),background .25s,color .25s}
.rst.js .in .rv-prog,.rst.js .in .rv-path li,.rst.js .rv-trust.in > div{opacity:1;transform:none}
.rst .rv-path{list-style:none;padding:0;margin:26px 0 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;position:relative;border-top:1px solid var(--hair)}
.rst .rv-path:before{content:"";position:absolute;left:0;top:-1px;height:1px;width:0;background:var(--olive);transition:width 1.6s cubic-bezier(.6,.1,.2,1) .3s}
.rst .in .rv-path:before{width:100%}
.rst .rv-path li{padding:16px 16px 0 0}
.rst .rv-path .k{font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--olive)}
.rst .rv-path b{display:block;font-family:var(--display);font-weight:500;font-size:20px;text-transform:uppercase;margin-top:6px}
.rst .rv-path span{display:block;color:var(--grey);font-size:14px;margin-top:6px;line-height:1.45}
.rst .rv-path li.now b{color:var(--olive-d)}
.rst .rv-path li.now .k:after{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--olive);margin-left:8px;vertical-align:middle;animation:rvPulse 1.8s ease-in-out infinite}
@keyframes rvPulse{50%{opacity:.25;transform:scale(1.6)}}
@media (max-width:860px){.rst .rv-path{grid-template-columns:1fr 1fr;gap:4px 0}}
@media (prefers-reduced-motion:reduce){.rst.js .rv-box,.rst.js .rv-trust,.rst.js .rv-prog,.rst.js .rv-path li,.rst.js .rv-trust > div{opacity:1;transform:none}.rst .rv-hero:before,.rst .rv-hero .scan{animation:none}}
.rst .rv-box.night .btn{background:var(--cream);color:var(--night);border-color:var(--cream)}
.rst .rv-box.night .btn:hover{background:transparent;color:var(--cream)}
.rst .rv-box.night .btn.ghost{background:transparent;color:var(--cream);border-color:rgba(237,230,218,.5)}
.rst .rv-box.night .btn.ghost:hover{background:var(--cream);color:var(--night)}
@media (max-width:860px){
 .rst .rv-trust{grid-template-columns:1fr 1fr}.rst .rv-trust div{border-bottom:1px solid var(--hair)}.rst .rv-trust div:nth-child(2n){border-right:0}.rst .rv-trust div:last-child{grid-column:span 2;border-bottom:0}
 .rst .rv-head,.rst .rv-doc,.rst .rv-faq,.rst .rv-cta,.rst .rv-legend{grid-template-columns:1fr}
 .rst .rv-hero .wrap{padding-bottom:76px;padding-top:44px}
 .rst .rv-progs{grid-template-columns:1fr 1fr}.rst .rv-prog{min-height:0;padding:16px 14px}.rst .rv-prog h3{font-size:20px}.rst .rv-prog p{font-size:13px}
}
@media (prefers-reduced-motion:reduce){.rst .rv-bar .seg{transition:none}.rst .rv-bar .a{width:35%}.rst .rv-bar .b{width:65%}}
</style>"""

TIERS = f"""<div class="tiers">
 <div class="tier"><div class="tag">Tier 01</div><h3>Self-Guided</h3><div class="price">$197<span class="unit">one time</span></div><div class="note">Nutrition: $147 · Lifetime access to Block 01</div>
  <ul><li>The full Block 01 guide</li><li>Exercise video library</li><li>Check-in and tracking tools</li><li>12 weekly lessons</li></ul><a class="btn ghost" href="#programs">Choose your program</a></div>
 <div class="tier pop"><span class="badge">Most popular</span><div class="tag">Tier 02</div><h3>Custom</h3><div class="price">$133<span class="unit">per month</span></div><div class="note">$399 per 12-week block · cancel anytime</div>
  <ul><li>Everything in Self-Guided</li><li>Onboarding call to set up your plan</li><li>Programming tailored to you</li><li>Weekly guidance and adjustments</li></ul><a class="btn" href="#programs">Choose your program</a></div>
 <div class="tier"><span class="badge">Limited spots</span><div class="tag">Tier 03</div><h3>Doctor-Led</h3><div class="price">$333<span class="unit">per month</span></div><div class="note">$999 per 12-week block · cancel anytime</div>
  <ul><li>Everything in Custom</li><li>Onboarding call with Dr. Urrutia</li><li>Weekly meeting with Dr. Urrutia</li><li>Personalized progressions</li></ul><a class="btn ghost" href="#programs">Choose your program</a></div>
</div><p class="tiers-foot">Custom and Doctor-Led renew into your next 12-week block until you cancel. That's how the progress sticks.</p>"""

BODY = f"""{CSS}
<section class="rv-hero hero" aria-label="Welcome"><span class="scan" aria-hidden="true"></span>
  <div class="poster" style="background:url({r}assets/hero-poster.webp) center/cover"></div>
  <video autoplay muted loop playsinline preload="metadata" poster="{r}assets/hero-poster.webp" aria-hidden="true" tabindex="-1"><source src="{r}assets/hero.mp4" type="video/mp4"></video>
  <div class="wrap">
    <div class="eyebrow" style="color:var(--sage)">Rehab + Performance</div>
    <h1>Rebuild the body you live in.</h1>
    <p class="sub">Doctor-built 12-week programs for pain, performance and fat loss. Train at home or in the gym, in English or Spanish.</p>
    <div class="ctas"><a class="btn" href="#programs">Find your program <span class="arr">→</span></a><a class="btn ghost" href="{r}quiz/">Take the 2-minute quiz</a></div>
    <div class="rv-offer"><b>Not sure where to start?</b><span>Answer 10 quick questions and get your program and support level. Or <a href="{r}free-guides/">start with a free guide</a>.</span></div>
  </div>
</section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-trust" aria-label="Why RESET">
    <div><b>Doctor-Built</b><span>Every program, every phase</span></div>
    <div><b>10 Years</b><span>Active duty, U.S. Coast Guard</span></div>
    <div><b>10 Programs</b><span>Rehab, sport + nutrition</span></div>
    <div><b>Home or Gym</b><span>Every exercise has both</span></div>
    <div><b>EN + ES</b><span>Every program in Spanish</span></div>
  </div>
</div></section>

<section class="rv" id="programs" style="padding-top:8px"><div class="wrap">
  <div class="rv-box mark">
    <div class="rv-head"><div><div class="eyebrow">Find Your Program</div><h2>Where are you starting?</h2></div><p>Pick the closest match. Each program page shows exactly what's inside, week by week, and all three ways to do it. Not sure? <a href="{r}quiz/" style="color:var(--olive-d);font-weight:700">Take the quiz</a>.</p></div>
    {finder}
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box night mark">
    <div class="rv-head"><div><div class="eyebrow">How It Works</div><h2>12 weeks. 4 phases.</h2></div><p>You move to the next phase when you pass its test, not when the calendar says so.</p></div>
    <div class="phases"><div class="phase"><div class="n">01</div><h3>Calm</h3><div class="w">Weeks 1–2</div><p>Get out of pain fast. Find where it's coming from and the movements that ease it.</p></div><div class="phase"><div class="n">02</div><h3>Restore</h3><div class="w">Weeks 3–5</div><p>Clean up how you move and start real strength work.</p></div><div class="phase"><div class="n">03</div><h3>Reinforce</h3><div class="w">Weeks 6–9</div><p>Add real load. Strength is what turns the alarm down.</p></div><div class="phase"><div class="n">04</div><h3>Return</h3><div class="w">Weeks 10–12</div><p>Back to the things you've been avoiding.</p></div></div>
    <div class="rv-split">
      <div class="eyebrow">The 35 / 65 Rule</div>
      <h3 style="font-size:clamp(24px,3vw,34px);margin-top:10px;color:var(--cream)">Treatment is 35%. RESET is built for the other 65%.</h3>
      <div class="rv-bar" role="img" aria-label="35 percent of recovery happens in treatment, 65 percent in the rest of your life"><div class="seg a"><span><b>35%</b>Treatment + rehab</span></div><div class="seg b"><span><b>65%</b>The rest of your life</span></div></div>
      <div class="rv-legend"><p><b>The 35%:</b> treatment and rehab. The spark that gets things moving.</p><p><b>The 65%:</b> how you train, sleep, eat and move between sessions. That's where the change sticks, and it's what RESET coaches.</p></div>
    </div>
  </div>
</div></section>

<section class="rv" id="reviews" style="padding-top:0"><div class="wrap">
  <div class="rv-box">
    <div class="rv-head"><div><div class="eyebrow">Patient Reviews</div><h2>What people say about working with Dr. Urrutia</h2></div><p><b class="rv-score">5.0 <span class="mini"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg></span></b> from 80 Google reviews by people he's worked with in person. RESET brings that same coaching online.</p></div>
    <div class="rv-quotes"><blockquote class="rv-q"><div class="stars" aria-label="5 out of 5 stars"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg></div><p>&ldquo;Doctor is extremely compassionate. Explains everything so well.&rdquo;</p><cite>Trisha M., Google review</cite></blockquote><blockquote class="rv-q"><div class="stars" aria-label="5 out of 5 stars"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg></div><p>&ldquo;Excellent intake appointment.&rdquo;</p><cite>John S., Google review</cite></blockquote><blockquote class="rv-q"><div class="stars" aria-label="5 out of 5 stars"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg></div><p>&ldquo;Excellent service.&rdquo;</p><cite>Rahila V., Google review</cite></blockquote></div>
  </div>
</div></section>

<section class="rv" id="tiers" style="padding-top:0"><div class="wrap">
  <div class="rv-box">
    <div class="rv-head"><div><div class="eyebrow">Choose Your Support</div><h2>Three ways to do it</h2></div><p>Same program, three levels of help. Start on your own or work with us every week.</p></div>
    {TIERS}
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box mark rv-doc">
    <img src="{r}assets/founder-540.webp" srcset="{r}assets/founder-540.webp 540w, {r}assets/founder-900.webp 900w" sizes="(max-width:860px) 92vw, 40vw" width="900" height="1352" alt="Dr. Jonathan Urrutia, founder of RESET" loading="lazy" decoding="async">
    <div>
      <div class="eyebrow">The Founder</div>
      <h2 style="margin-top:12px">Dr. Jonathan Urrutia</h2>
      <p>Ten years on active duty in the Coast Guard. A former bodybuilding competitor. A doctor who works with people in pain and athletes every week, and a husband and father who trains around a full life like you do.</p>
      <p>The same story kept coming up: "I felt better, then I was right back where I started." The pain left, the work stopped, and nothing else changed. RESET is what I built to fix that, so the progress keeps going after week 12.</p>
      <ol class="rv-path">
        <li><span class="k">Served</span><b>U.S. Coast Guard</b><span>10 years active duty.</span></li>
        <li><span class="k">Trained</span><b>Doctorate, 2022</b><span>Parker University in Dallas.</span></li>
        <li><span class="k">Built</span><b>His own practice</b><span>Treating pain and training athletes every week.</span></li>
        <li class="now"><span class="k">Now</span><b>Building RESET</b><span>10 programs in English and Spanish, coaching Doctor-Led members each week.</span></li>
      </ol>
      <p style="margin-top:24px"><a class="btn ghost" href="{r}about/">Read the full story <span class="arr">→</span></a></p>
    </div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box rv-faq">
    <div><div class="eyebrow">FAQs</div><h2 style="margin-top:12px">Questions</h2><p>Straight answers before you start. Still unsure? Send us a message.</p><a class="btn ghost" href="{r}contact/">Contact us</a></div>
    <div class="faq">{faq_html}</div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box night mark rv-cta">
    <div><div class="eyebrow">Start Today</div><h2 style="margin-top:12px">We don't have weak bodies. We have weak systems.</h2><p>Your body is built to be resilient. RESET gives it a way to get there.</p></div>
    <div class="btns"><a class="btn" href="#programs">Find your program <span class="arr">→</span></a><a class="btn ghost" href="{r}quiz/">Take the quiz</a></div>
  </div>
</div></section>
@@JS@@
"""
JS = r"""<script>
(function(){var b=document.querySelector(".rv-bar");if(!b)return;if(!("IntersectionObserver" in window)){b.classList.add("seen");return}
new IntersectionObserver(function(es,o){es.forEach(function(e){if(e.isIntersecting){b.classList.add("seen");o.disconnect()}})},{threshold:.4}).observe(b);
var v=document.querySelector(".rv-hero video");if(v){var rm=matchMedia("(prefers-reduced-motion: reduce)").matches,sd=navigator.connection&&navigator.connection.saveData;if(rm||sd){v.removeAttribute("autoplay");v.pause()}else{new IntersectionObserver(function(es){es[0].isIntersecting?v.play().catch(function(){}):v.pause()}).observe(v)}}
(function(){var els=document.querySelectorAll(".rv-box,.rv-trust");if(!("IntersectionObserver" in window)){els.forEach(function(e){e.classList.add("in")});return}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var t=e.target;t.classList.add("in");io.unobserve(t);setTimeout(function(){t.querySelectorAll(".rv-prog,.rv-path li,:scope > div").forEach(function(c){c.style.transitionDelay=""})},1800)}})},{threshold:.12});
els.forEach(function(e){io.observe(e);e.querySelectorAll(".rv-prog,.rv-path li,:scope > div").forEach(function(c,i){c.style.transitionDelay=(Math.min(i,10)*0.06)+"s"})})})();
var qs=[].slice.call(document.querySelectorAll(".rv-q"));if(qs.length){var rm2=matchMedia("(prefers-reduced-motion: reduce)").matches,i=0,t=null;
function step(){qs.forEach(function(q){q.classList.remove("lit")});qs[i%qs.length].classList.add("lit");i++}
new IntersectionObserver(function(es){var e=es[0];if(e.isIntersecting){qs.forEach(function(q){q.classList.add("in")});if(!rm2&&!t){setTimeout(step,1200);t=setInterval(step,3600)}}else if(t){clearInterval(t);t=null;qs.forEach(function(q){q.classList.remove("lit")})}},{threshold:.35}).observe(qs[0].parentElement)}
document.addEventListener("click",function(e){var a=e.target.closest("a");if(!a||typeof gtag!=="function")return;var h=a.getAttribute("href")||"";
if(h.indexOf("free-guide")>-1)gtag("event","free_guide_click",{link_text:a.textContent.trim().slice(0,60)});else if(/checkout|fastpaydirect/.test(h))gtag("event","begin_checkout",{link_url:a.href});else if(h.indexOf("#programs")>-1)gtag("event","find_program_click",{link_text:a.textContent.trim().slice(0,60)})},true)})();
</script>"""
BODY = BODY.replace("@@JS@@", JS)
page = head.replace("</head>", ld + "\n</head>", 1) + BODY + foot
out = ROOT / ("index.html" if LIVE else "preview/index.html")
out.parent.mkdir(exist_ok=True)
out.write_text(page)
print("wrote", out.relative_to(ROOT))
