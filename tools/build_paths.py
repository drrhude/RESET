"""Builds the "pick your path" pages (English):
  /rehab/         hub: the 5 rehab programs
  /performance/   hub: the 4 sport programs (+ nutrition pointer)
  /go/<slug>/     single-focus sales pages for ads (noindex, no main nav, checkout on the page)
  python3 tools/build_paths.py
Program facts (why-it-comes-back, phases, what's inside, FAQs, payment and booking links) are read
from each live program page and its checkout page, so editing those keeps these pages in sync.
Ad copy (headline, "sound familiar" list) lives in TRACKS below. Same head, fonts and footer as the
homepage (tools/_shell.html), plus tools/home.css.html and tools/paths.css.html."""
import re, json, pathlib, html as H
ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
SHELL = (TOOLS / "_shell.html").read_text()
HOME_CSS = (TOOLS / "home.css.html").read_text()
CSS = (TOOLS / "paths.css.html").read_text()
SITE = "https://resethybridrecovery.com/"
E = H.escape

# ---------------------------------------------------------------- copy
TRACKS = {
 "back": dict(name="Low Back", short="Back", go="back", group="rehab",
   desc="Recurring low back pain, stiffness and flare-ups.",
   chips=["Flare-ups", "Sitting & bending", "Stiff mornings"],
   ad_h="Stop babying your back. Start building it back.",
   ad_sub="A doctor-built 12-week plan for low back pain that keeps coming back. Calm it down, rebuild the strength that protects it, and break the flare-up cycle. Home or gym.",
   familiar=["It flares up every few months, usually from something small", "Sitting, bending or lifting sets it off",
             "You got treatment or did PT, felt better, and it came back", "You were told to rest it, and it only got stiffer",
             "You avoid things you used to do without thinking"]),
 "neck": dict(name="Neck", short="Neck", go="neck", group="rehab",
   desc="Desk neck, stiffness, tension headaches and arm symptoms.",
   chips=["Desk neck", "Tension headaches", "Tight traps"],
   ad_h="Your neck doesn't need another stretch. It needs strength.",
   ad_sub="A doctor-built 12-week plan for stiff, achy necks and tension headaches. Find your pattern, then build back the deep neck and upper back strength that holds you up all day.",
   familiar=["Your neck is tight and stiff by the end of every workday", "Headaches start at the base of your skull",
             "Your upper traps feel like rocks no matter how much you rub them", "Checking your blind spot or looking up hurts",
             "Stretching helps for an hour, then it's right back"]),
 "knee": dict(name="Knee", short="Knee", go="knee", group="rehab",
   desc="Front-of-knee pain, stiff or arthritic knees, post-injury rebuilding.",
   chips=["Stairs & squats", "Arthritis", "After an injury"],
   ad_h="Stairs shouldn't be the hardest part of your day.",
   ad_sub="A doctor-built 12-week plan for knee pain. Calm it down first, then rebuild the quads and hips that protect it, so you can trust your knee again.",
   familiar=["Stairs, squats or getting out of a chair hurt", "You were told it's “wear and tear” and to take it easy",
             "It aches after a walk, a run or a hike", "You've stopped doing things because you don't trust it",
             "It's stiff in the morning or after sitting"]),
 "shoulder": dict(name="Shoulder", short="Shoulder", go="shoulder", group="rehab",
   desc="Painful overhead reach, rotator cuff irritation, stiff shoulders.",
   chips=["Overhead reach", "Rotator cuff", "Night pain"],
   ad_h="Reaching overhead shouldn't make you wince.",
   ad_sub="A doctor-built 12-week plan for shoulder pain. Rest makes the rotator cuff weaker. Loading it the right way makes it stronger and calmer.",
   familiar=["It pinches when you reach up, behind you or into the back seat", "It wakes you up when you lie on that side",
             "Pressing, pulling or carrying makes it ache", "An MRI said “tear” or “impingement” and you're not sure what's next",
             "You've rested it for weeks and it's no better"]),
 "hip": dict(name="Hip", short="Hip", go="hip", group="rehab",
   desc="Side-of-hip pain, groin pain and stiff or arthritic hips.",
   chips=["Side of hip", "Groin & front", "Arthritis"],
   ad_h="Sitting, sleeping, walking. Your hip shouldn't run the show.",
   ad_sub="A doctor-built 12-week plan for hip pain. Find where it's coming from, take the pressure off, and build strength back in every direction.",
   familiar=["Pain on the side of your hip, especially lying on it", "Groin or front-of-hip pain getting up from a chair",
             "Stiff hips first thing in the morning", "You've stretched your hip flexors for months with little change",
             "Walks and stairs keep getting shorter and harder"]),
 "golf": dict(name="Golf", short="Golf", go="golf", group="performance",
   desc="More distance, a swing that doesn't hurt, a body that lasts 18 holes.",
   chips=["Distance", "Rotation", "Low back"],
   ad_h="More distance. Less back pain. Feel good on the 18th hole.",
   ad_sub="A doctor-built 12-week strength plan for golfers of any handicap. Hips, upper back, grip and rotational power, so your body can keep up with your swing.",
   familiar=["Your low back is sore after a round or a range session", "You've lost distance and lessons alone won't bring it back",
             "Your hips and upper back feel stuck in the turn", "Elbow or shoulder aches creep in as the season goes on",
             "You want to play more rounds, not fewer"]),
 "pickleball": dict(name="Pickleball", short="Pickleball", go="pickleball", group="performance",
   desc="Faster feet, fewer tweaks, a body that plays several days a week.",
   chips=["First step", "Calves & Achilles", "Shoulder"],
   ad_h="Stay on the court. Stop getting tweaked.",
   ad_sub="A doctor-built 12-week strength plan for pickleball players. Calves, hips, shoulder and first-step quickness, scheduled around the days you play.",
   familiar=["Calf, Achilles or knee tightness after you play", "A lateral step that doesn't feel quick anymore",
             "Your shoulder aches on overheads", "You play several days a week and never train for it",
             "You've had one strain and you're worried about the next"]),
 "dance": dict(name="Dance", short="Dance", go="dance", group="performance",
   desc="Return to dance after injury, then build strength, jumps and stamina.",
   chips=["Return from injury", "Jumps & landings", "Strength"],
   ad_h="Get back on the floor. Then come back stronger.",
   ad_sub="A doctor-built 12-week plan for dancers. Block 01 gets you back after a foot, ankle, hip or back injury. The strength work builds what class doesn't.",
   familiar=["A foot, ankle, hip or back injury pulled you out of class", "You're flexible but don't feel strong or stable",
             "Jumps and landings feel heavy or unsure", "Turnout or relevés keep aggravating the same spot",
             "You want strength work that won't make you bulky"]),
 "student-athlete": dict(name="Student Athlete", short="Student Athlete", go="student", group="performance",
   desc="Off-season to post-season training for young athletes.",
   chips=["Ages 13+", "Season-based", "Parent guide"],
   ad_h="Build the athlete, not just the player.",
   ad_sub="A doctor-built training plan for young athletes, organized around the season: strength, landing, speed and injury prevention. Parent guidance and consent built into every block.",
   familiar=["Your athlete plays one sport almost all year", "Practice builds skill, but not strength or landing mechanics",
             "Knee, ankle or back pain keeps coming up", "They stop lifting in-season and finish weaker than they started",
             "You want a plan that's safe, supervised and built by a doctor"]),
 "nutrition": dict(name="Nutrition", short="Nutrition", go="nutrition", group="nutrition",
   desc="Lose fat without losing muscle, then keep it off for good.",
   chips=["Fat loss", "Keep muscle", "Real food"],
   ad_h="Lose the fat. Keep the muscle. Keep your life.",
   ad_sub="A doctor-built 12-week fat-loss plan: protein first, real strength training, enough steps, and a plan for weekends and restaurants.",
   familiar=["You've lost weight before and it came back", "The plan works until the weekend, the restaurant, or 8 PM",
             "You're losing muscle along with the fat", "You're not sure how much protein you actually need",
             "You want a plan that fits family, work and eating out"]),
}
REVIEWS = [("Doctor is extremely compassionate. Explains everything so well.", "Trisha M."),
           ("Excellent intake appointment.", "John S."), ("Excellent service.", "Rahila V.")]
STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg>'

# ---------------------------------------------------------------- read live program facts
def txt(x): return H.unescape(re.sub(r"<[^>]+>", "", x)).strip()
def facts(slug):
    s = (ROOT / slug / "index.html").read_text()
    c = (ROOT / slug / "checkout" / "index.html").read_text()
    sec = lambda start: s[s.index(start):s.index("</section>", s.index(start))]
    f = {}
    f["eyebrow"] = txt(re.search(r'<section class="dark hero".*?class="eyebrow[^"]*"[^>]*>(.*?)</', s, re.S).group(1))
    f["why_h"] = txt(re.search(r'class="chain"', s) and re.findall(r'<h2[^>]*>(.*?)</h2>', s, re.S)[0])
    ch = s[s.index('class="chain"'):s.index("</section>", s.index('class="chain"'))]
    f["why"] = [(txt(a), txt(b)) for a, b in re.findall(r"<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>", ch, re.S)]
    f["gets"] = [(txt(a), txt(b)) for a, b in re.findall(r"<b>(.*?)</b><span>(.*?)</span>", sec("What you get</h2>"), re.S)]
    f["phases"] = [(txt(a), txt(b), txt(cc)) for a, b, cc in re.findall(r'<h3>(.*?)</h3>\s*<div class="w">(.*?)</div>\s*<p>(.*?)</p>', sec('class="phases"'), re.S)]
    d = sec("Meet your doctor")
    f["doc_h"] = txt(re.search(r"<h2[^>]*>(.*?)</h2>", d, re.S).group(1))
    f["doc_p"] = [txt(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", d, re.S)][:2]
    f["faq"] = [(txt(a), txt(b)) for a, b in re.findall(r"<details><summary>(.*?)</summary>\s*<p>(.*?)</p>", s, re.S)]
    f["price"] = re.search(r"Self-Guided.*?(\$\d+)", re.sub(r"<[^>]+>", " ", s), re.S).group(1)
    pay = re.findall(r"https://link\.fastpaydirect\.com/payment-link/\w+", c)
    f["pay"] = pay[0] if pay else f"{SITE}{slug}/checkout/"
    f["guide"] = (ROOT / slug / "free-guide" / "index.html").exists()
    return f

# ---------------------------------------------------------------- page shell
HEAD_END = SHELL.index("</head>")
BODY_START = SHELL.index('<div class="rst"')
NAV_END = SHELL.index('<section class="dark hero" id="programs">')
FOOT = SHELL[SHELL.index("<footer>"):]

def fixpaths(s, depth):
    pre = "../" * depth
    return re.sub(r'(href|src)="(?!https?:|#|data:|mailto:|tel:|/)([^"]*)"', lambda m: f'{m.group(1)}="{pre}{m.group(2)}"', s)

def head(title, desc, path, depth, noindex=False):
    h = SHELL[:HEAD_END]
    url = SITE + path
    h = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", h, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', h)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h)
    h = re.sub(r'<link rel="alternate" hreflang[^>]*>', "", h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(desc)}">', h)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', h)
    if noindex:
        h = h.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">', 1)
    return fixpaths(h, depth) + "\n</head>\n"

def write(path, page):
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print("wrote", out.relative_to(ROOT))

REVEAL = """<script>(function(){var els=document.querySelectorAll(".rv-box");if(!("IntersectionObserver" in window)){els.forEach(function(e){e.classList.add("in")});return}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.08});els.forEach(function(e){io.observe(e)})})();</script>"""

# ---------------------------------------------------------------- hubs
HUBS = {
 "rehab": dict(title="Rehab Programs for Back, Neck, Knee, Shoulder & Hip Pain | RESET",
   desc="Doctor-built 12-week rehab programs for low back, neck, knee, shoulder and hip pain. Pick where it hurts. Home or gym.",
   eyebrow="Rehab", h1="Where does it hurt?",
   sub="Pick the closest match. Every rehab program follows the same four phases: calm it down, clean up how you move, build real strength, and get back to what you've been avoiding.",
   other=("Not hurt? Train for your sport", "performance/"), other2=("Want to lose fat?", "nutrition/")),
 "performance": dict(title="Sports Performance Training Programs: Golf, Pickleball, Dance | RESET",
   desc="Doctor-built 12-week strength programs for golf, pickleball, dance and student athletes. Perform better and get hurt less.",
   eyebrow="Performance", h1="What do you want to be better at?",
   sub="Pick your sport. Every performance program builds the body that plays it: strength, power and the prehab your sport needs, planned around your season.",
   other=("Hurting right now? Start with rehab", "rehab/"), other2=("Want to lose fat?", "nutrition/")),
}

def build_hub(key):
    h = HUBS[key]; depth = 1
    slugs = [s for s, t in TRACKS.items() if t["group"] == key]
    cards = ""
    for i, s in enumerate(slugs, 1):
        t, f = TRACKS[s], facts(s)
        chips = "".join(f"<li>{E(c)}</li>" for c in t["chips"])
        guide = f'<a class="free" href="{s}/free-guide/">Free guide →</a>' if f["guide"] else ""
        cards += (f'<div class="pd-card"><div><span class="num">{i:02d}</span><h3>{E(t["name"])}</h3><p>{E(t["desc"])}</p></div>'
                  f'<ul aria-label="Common reasons people start">{chips}</ul>'
                  f'<div class="acts"><span class="from">From {f["price"]} · 12 weeks</span><a class="btn" href="{s}/">See the program <span class="arr">→</span></a>{guide}</div></div>')
    phases = "".join(f'<div class="phase"><div class="n">{i+1:02d}</div><h3>{E(a)}</h3><div class="w">{E(b)}</div><p>{E(c)}</p></div>' for i, (a, b, c) in enumerate(facts(slugs[0])["phases"]))
    nut = ""
    if key == "performance":
        nut = '<p style="margin-top:18px;color:var(--grey)">Pair it with <a href="nutrition/" style="color:var(--olive-d);font-weight:700">RESET Nutrition</a> if you also want to lose fat and keep muscle.</p>'
    body = f"""{HOME_CSS}{CSS}
<section class="pd-hero"><div class="wrap">
  <div class="crumb"><a href="./">Home</a> / {h['eyebrow']}</div>
  <div class="eyebrow" style="color:var(--sage);margin-top:18px">{h['eyebrow']} · {len(slugs)} programs</div>
  <h1>{h['h1']}</h1>
  <p>{h['sub']}</p>
  <div class="ctas"><a class="btn" href="#list">Show me the programs <span class="arr">→</span></a><a class="btn ghost" href="quiz/">Not sure? Take the 2-minute quiz</a></div>
</div></section>

<section class="rv" id="list" style="padding-top:0"><div class="wrap pd-lift">
  <div class="rv-box mark">
    <div class="rv-head"><div><div class="eyebrow">Pick one</div><h2>{h['eyebrow']} programs</h2></div><p>Each program page shows exactly what's inside, week by week, and all three ways to do it.</p></div>
    <div class="pd-cards">{cards}</div>{nut}
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box night mark">
    <div class="rv-head"><div><div class="eyebrow">How it works</div><h2>12 weeks. 4 phases.</h2></div><p>You move to the next phase when you pass its test, not when the calendar says so.</p></div>
    <div class="phases">{phases}</div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box">
    <div class="rv-head"><div><div class="eyebrow">Choose your support</div><h2>Same program, three ways to do it</h2></div><p>Start on your own or work with us every week. You pick on the program page.</p></div>
    <div class="pd-mini">
      <div><b>Self-Guided</b><span class="p">$197 one time</span><span>The full Block 01 guide, video library and tracking tools. Yours for life.</span></div>
      <div><b>Custom</b><span class="p">$133 / month</span><span>Onboarding call, programming tailored to you, weekly guidance and adjustments.</span></div>
      <div><b>Doctor-Led</b><span class="p">$333 / month</span><span>Everything in Custom, plus a weekly meeting with Dr. Urrutia.</span></div>
    </div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box night mark rv-cta">
    <div><div class="eyebrow">Still deciding?</div><h2 style="margin-top:12px">Answer 10 questions. Get your program.</h2><p>The quiz matches you to a program and a support level based on where you're starting.</p></div>
    <div class="btns"><a class="btn" href="quiz/">Take the quiz <span class="arr">→</span></a><a class="btn ghost" href="{h['other'][1]}">{h['other'][0]}</a></div>
  </div>
</div></section>
{REVEAL}
"""
    nav = SHELL[BODY_START:NAV_END]
    page = head(h["title"], h["desc"], key + "/", depth) + "<body>\n" + fixpaths(SHELL[SHELL.index("<body>") + 6:BODY_START] + nav + body + FOOT, depth)
    write(key, page)

# ---------------------------------------------------------------- /go/ sales pages
GO_JS = """<script>(function(){
var bar=document.querySelector(".gp-sticky"),hero=document.querySelector(".gp-hero"),buy=document.getElementById("start");
if(bar&&"IntersectionObserver" in window){var hv=true,bv=false;function u(){bar.classList.toggle("on",!hv&&!bv)}
new IntersectionObserver(function(e){hv=e[0].isIntersecting;u()}).observe(hero);new IntersectionObserver(function(e){bv=e[0].isIntersecting;u()}).observe(buy)}
var name=document.body.getAttribute("data-track"),price=parseFloat(document.body.getAttribute("data-price"));
if(typeof fbq==="function")fbq("track","ViewContent",{content_name:name,value:price,currency:"USD"});
document.addEventListener("click",function(e){var a=e.target.closest("a");if(!a)return;var h=a.getAttribute("href")||"";
if(/fastpaydirect/.test(h)){if(typeof fbq==="function")fbq("track","InitiateCheckout",{content_name:name,value:price,currency:"USD"});if(typeof gtag==="function")gtag("event","begin_checkout",{item_name:name,value:price,currency:"USD"})}
else if(/checkout\\//.test(h)&&typeof gtag==="function")gtag("event","book_call_click",{item_name:name})},true)})();</script>"""

def build_go(slug):
    t, f = TRACKS[slug], facts(slug); depth = 2
    price = f["price"]; pnum = price.strip("$")
    familiar = "".join(f"<li>{E(x)}</li>" for x in t["familiar"])
    why = "".join(f'<div><span class="n">{i+1:02d}</span><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, (a, b) in enumerate(f["why"]))
    gets = "".join(f"<li><span><b>{E(a)}.</b> {E(b)}</span></li>" for a, b in f["gets"])
    phases = "".join(f'<div class="phase"><div class="n">{i+1:02d}</div><h3>{E(a)}</h3><div class="w">{E(b)}</div><p>{E(c)}</p></div>' for i, (a, b, c) in enumerate(f["phases"]))
    reviews = "".join(f'<blockquote class="rv-q in"><div class="stars" aria-label="5 out of 5 stars">{STAR*5}</div><p>&ldquo;{E(a)}&rdquo;</p><cite>{E(b)}, Google review</cite></blockquote>' for a, b in REVIEWS)
    faq = list(f["faq"])
    faq.insert(0, ("What happens after I buy?", "Your Block 01 guide and video library arrive by email right after checkout. Start the check-in, find your starting point, and begin week 1."))
    faq_html = "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faq)
    incl = "".join(f"<li>{E(a)}</li>" for a, _ in f["gets"])
    rehab = t["group"] == "rehab"
    why_h = f["why_h"] if f["why_h"] else "Why it keeps happening"
    pay = f["pay"]
    title = f"RESET {t['short']}: {t['ad_h']}"
    top = f"""<div class="rst" lang="en"><header class="gp-top"><div class="wrap">
  <a href="../../" aria-label="RESET home"><span class="lg" role="img" aria-label="RESET"></span></a>
  <span class="note mono" style="color:#B8B3A6;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase">{E(f['eyebrow'])}</span>
  <a class="btn" href="#start">Start · {price}</a>
</div></header>"""
    body = f"""{HOME_CSS}{CSS}
{top}
<section class="gp-hero"><div class="wrap grid">
  <div>
    <div class="eyebrow" style="color:var(--sage)">{E(f['eyebrow'])}</div>
    <h1>{E(t['ad_h'])}</h1>
    <p class="sub">{E(t['ad_sub'])}</p>
    <div class="ctas"><a class="btn" href="#start">Start today · {price} <span class="arr">→</span></a><span class="note">One payment · lifetime access</span></div>
    <ul class="chips"><li>Built by a doctor</li><li>Home or gym</li><li>12 weeks</li><li>English &amp; Spanish</li></ul>
  </div>
  <!-- Swap this photo for a 30-60 sec video of Dr. Urrutia: replace the <img> with
       <video controls playsinline preload="metadata" poster="../../assets/founder-900.webp"><source src="../../assets/go/{t['go']}.mp4" type="video/mp4"></video> -->
  <div class="gp-media"><img src="../../assets/founder-540.webp" srcset="../../assets/founder-540.webp 540w, ../../assets/founder-900.webp 900w" sizes="(max-width:860px) 92vw, 34vw" width="900" height="1352" alt="Dr. Jonathan Urrutia, founder of RESET" fetchpriority="high"><div class="cap">Dr. Jonathan Urrutia, DC · Coast Guard veteran</div></div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap gp-lift">
  <div class="rv-box mark">
    <div class="rv-head"><div><div class="eyebrow">Sound familiar?</div><h2>{'If this is you, this program is for you.' if rehab else 'If this is you, keep reading.'}</h2></div><p>{'Pain is always real. The question is where it is coming from and what your body needs to handle more.' if rehab else 'Practicing your sport builds skill. It rarely builds the body that plays it.'}</p></div>
    <ul class="gp-checks">{familiar}</ul>
    <p class="gp-turn">{'You don&rsquo;t have a weak body. You have a weak system, and systems can be rebuilt.' if slug != 'nutrition' else 'You don&rsquo;t lack discipline. You lack a system. That&rsquo;s fixable.'}</p>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box">
    <div class="rv-head"><div><div class="eyebrow">The real problem</div><h2>{E(why_h)}</h2></div><p>None of these get fixed by resting and waiting. They get fixed with the right work, in the right order.</p></div>
    <div class="gp-why">{why}</div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box night mark">
    <div class="rv-head"><div><div class="eyebrow">What you get</div><h2>Everything you need for 12 weeks.</h2></div><p>No guessing what to do next. Every week is laid out for you.</p></div>
    <ul class="gp-gets">{gets}</ul>
    <div class="phases" style="margin-top:clamp(28px,4vw,44px)">{phases}</div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box mark rv-doc" style="grid-template-columns:1fr">
    <div style="max-width:68ch">
      <div class="eyebrow">Meet your doctor</div>
      <h2 style="margin-top:12px">{E(f['doc_h'])}</h2>
      {''.join(f'<p>{E(p)}</p>' for p in f['doc_p'])}
      <p style="font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--olive)">Dr. Jonathan Urrutia, DC · 10 years U.S. Coast Guard</p>
    </div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box">
    <div class="rv-head"><div><div class="eyebrow">Reviews</div><h2>What people say about working with Dr. Urrutia</h2></div><p><b class="rv-score">5.0 <span class="mini">{STAR*5}</span></b> from 80 Google reviews by people he's worked with in person.</p></div>
    <div class="rv-quotes">{reviews}</div>
  </div>
</div></section>

<section class="rv" id="start" style="padding-top:0"><div class="wrap">
  <div class="rv-box mark">
    <div class="rv-head"><div><div class="eyebrow">Start today</div><h2>Get RESET {E(t['short'])}.</h2></div><p>One payment. Your guide and video library arrive by email right after checkout.</p></div>
    <div class="gp-buy">
      <div class="gp-main">
        <div class="tag">Self-Guided · Block 01</div>
        <h3>RESET {E(t['short'])}</h3>
        <div class="price">{price}<small>one time</small></div>
        <ul>{incl}<li>Lifetime access</li></ul>
        <a class="btn" href="{pay}">Get instant access · {price} <span class="arr">→</span></a>
        <p class="fine">Secure checkout. Card, Apple Pay or Google Pay where available.</p>
      </div>
      <div class="gp-up">
        <h3>Want a coach in your corner?</h3>
        <p>Same program, tailored to you, with weekly check-ins. Book a short onboarding call and we'll set it up.</p>
        <div class="opt"><b>Custom</b><span class="p">$133/mo</span><span>Onboarding call, programming tailored to you, weekly guidance and adjustments.</span></div>
        <div class="opt"><b>Doctor-Led</b><span class="p">$333/mo</span><span>Everything in Custom, plus a weekly meeting with Dr. Urrutia. Limited spots.</span></div>
        <a class="btn ghost" href="../../{slug}/checkout/">Book your onboarding call <span class="arr">→</span></a>
        <p style="margin-top:14px;font-size:14px;color:var(--grey)">Custom and Doctor-Led are month to month. Cancel anytime. Not sure which program fits? <a href="../../quiz/" style="color:var(--olive-d);font-weight:700">Take the 2-minute quiz</a>.</p>
      </div>
    </div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box rv-faq">
    <div><div class="eyebrow">FAQ</div><h2 style="margin-top:12px">Questions</h2><p>Straight answers before you start.</p><a class="btn" href="#start">Start · {price}</a></div>
    <div class="faq">{faq_html}</div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box night mark rv-cta">
    <div><div class="eyebrow">Movement is medicine</div><h2 style="margin-top:12px">Your body is built to be resilient. Give it a plan.</h2><p>Twelve weeks from now you can be stronger than you are today. Start this week.</p></div>
    <div class="btns"><a class="btn" href="#start">Start today · {price} <span class="arr">→</span></a><a class="btn ghost" href="../../{slug}/">See the full program</a></div>
  </div>
</div></section>

<div class="gp-sticky" aria-hidden="false"><span>RESET {E(t['short'])}<br>{price} · lifetime access</span><a class="btn" href="{pay}">Get started</a></div>

<footer class="gp-foot"><div class="wrap">
  <a href="../../">RESET home</a><a href="../../{slug}/">Full program</a><a href="../../privacy/">Privacy</a><a href="../../terms/">Terms</a><a href="../../contact/">Contact</a>
  <p>RESET programs are education and exercise programs. They are not medical care and do not diagnose or treat any condition. Check-ins are coaching and education, not medical treatment. Talk to your healthcare provider before starting if you have a medical condition, recent surgery or injury, or symptoms like chest pain, numbness, weakness, or loss of bladder or bowel control. Results vary.</p>
  <p>Created by Dr. Jonathan Urrutia, DC · resethybridrecovery.com</p>
</div></footer></div>
{GO_JS}
"""
    pre_body = SHELL[SHELL.index("<body>") + 6:BODY_START]  # fonts + base styles
    page = (head(title, t["ad_sub"], f"go/{t['go']}/", depth, noindex=True)
            + f'<body data-track="RESET {E(t["short"])}" data-price="{pnum}">\n' + fixpaths(pre_body, depth) + body + "\n</body>\n</html>\n")
    write(f"go/{t['go']}", page)

if __name__ == "__main__":
    for k in HUBS: build_hub(k)
    for s in TRACKS: build_go(s)
