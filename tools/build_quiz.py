"""Builds the RESET program quiz at /quiz/ (10 questions -> program + support tier).
Run: python3 tools/build_quiz.py   (add --index to allow search engines once the new homepage is live)"""
import re, sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = "--index" in sys.argv
shell = (ROOT / "tools/_shell.html").read_text()
head = shell[:shell.index('<section class="dark hero" id="programs">')]
foot = shell[shell.index("<footer>"):]
def fix(s): return re.sub(r'(href|src)="(?!https?:|#|data:|mailto:|tel:|/)([^"]*)"', lambda m: f'{m.group(1)}="../{m.group(2)}"', s)
head, foot = fix(head), fix(foot)
T = "Which RESET Program Is Right for You? | 2-Minute Quiz"
D = "Answer 10 quick questions and get the RESET program and support level that fits your pain, sport or goal. Doctor-built, home or gym, English or Spanish."
head = re.sub(r"<title>.*?</title>", f"<title>{T}</title>", head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{D}">', head, count=1)
head = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="https://resethybridrecovery.com/quiz/">', head, count=1)
head = re.sub(r'<link rel="alternate" hreflang[^\n]*?>(<link rel="alternate" hreflang[^>]*>)?', '', head, count=1)
head = re.sub(r'property="og:title" content="[^"]*"', f'property="og:title" content="{T}"', head)
head = re.sub(r'property="og:description" content="[^"]*"', f'property="og:description" content="{D}"', head)
head = re.sub(r'property="og:url" content="[^"]*"', 'property="og:url" content="https://resethybridrecovery.com/quiz/"', head)
if not INDEX: head = head.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">', 1)

PROGRAMS = {
 "back": ("Low Back", "Recurring low back pain, stiffness and flare-ups.", "6acfd40f075ea22a20cde7ec", 197),
 "neck": ("Neck", "Desk neck, stiffness, tension headaches and arm symptoms.", "6acfd452075ea22a20cde7ed", 197),
 "knee": ("Knee", "Front-of-knee pain, stiff or arthritic knees, post-injury rebuilding.", "6acfd496c0e70c7fefb749fe", 197),
 "shoulder": ("Shoulder", "Painful overhead reach, rotator cuff irritation, stiff shoulders.", "6acfd4da075ea22a20cde7ef", 197),
 "hip": ("Hip", "Side-of-hip pain, groin pain and stiff or arthritic hips.", "6acfd518c0e70c7fefb74a01", 197),
 "golf": ("Golf", "More distance, a swing that doesn't hurt, a body that lasts 18 holes.", "6acfd555075ea22a20cde7f1", 197),
 "pickleball": ("Pickleball", "Faster feet, fewer tweaks, a body that plays several days a week.", "6acfd592c0e70c7fefb74a04", 197),
 "dance": ("Dance", "Return to dance after injury, then build strength, jumps and stamina.", "6acfd5ce075ea22a20cde7f3", 197),
 "student-athlete": ("Student Athlete", "Off-season to post-season training for young athletes.", "6acfd606075ea22a20cde7f5", 197),
 "nutrition": ("Nutrition", "Lose fat without losing muscle, then keep it off for good.", "6acfd63fc0e70c7fefb74a05", 147),
}
data = json.dumps({k: {"name": v[0], "desc": v[1], "pay": "https://link.fastpaydirect.com/payment-link/" + v[2], "self": v[3]} for k, v in PROGRAMS.items()})

CSS = """<style>
.rst{background:#E2E0D5}
.rst .qz-hero{padding-block:56px 40px}
.rst .qz-hero h1{font-size:clamp(34px,5vw,60px);margin-top:14px;max-width:18ch}
.rst .qz-hero .sub{max-width:56ch;font-size:17px;color:#DAD4C7;margin-top:14px}
.rst .qz-wrap{max-width:860px;margin:-28px auto 0;position:relative;z-index:2;padding-inline:20px}
.rst .qz{background:#fff;border:1px solid #CFCDC1;box-shadow:0 40px 70px -50px rgba(17,20,16,.55);padding:clamp(22px,4vw,48px);min-height:420px}
.rst .qz-top{display:flex;justify-content:space-between;align-items:center;gap:16px;font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey)}
.rst .qz-bar{height:3px;background:#E4E2D8;margin:14px 0 28px;overflow:hidden}
.rst .qz-bar i{display:block;height:100%;width:0;background:var(--olive);transition:width .5s cubic-bezier(.2,.7,.2,1)}
.rst .qz h2{font-size:clamp(26px,3.4vw,40px)}
.rst .qz .hint{color:var(--grey);margin-top:10px;font-size:15px}
.rst .qz-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-top:24px}
.rst .qz-opt{text-align:left;font:inherit;cursor:pointer;background:#F6F4EE;border:1px solid #D3D1C5;padding:16px 18px;display:flex;flex-direction:column;gap:4px;transition:background .2s,border-color .2s,transform .2s;color:var(--ink)}
.rst .qz-opt b{font-family:var(--display);font-weight:500;font-size:20px;text-transform:uppercase;letter-spacing:.01em}
.rst .qz-opt span{font-size:14px;color:var(--grey)}
.rst .qz-opt:hover,.rst .qz-opt:focus-visible{border-color:var(--olive);background:#fff;transform:translateY(-2px)}
.rst .qz-opt.sel{background:var(--olive-d);border-color:var(--olive-d);color:var(--cream)}.rst .qz-opt.sel span{color:#D6D1C4}
.rst .qz-why{margin-top:22px;padding:14px 16px;border-left:2px solid var(--olive);background:#F6F4EE;font-size:14.5px;color:var(--grey)}
.rst .qz-why b{font-family:var(--mono);font-weight:500;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--olive);display:block;margin-bottom:4px}
.rst .qz-nav{display:flex;justify-content:space-between;align-items:center;margin-top:26px}
.rst .qz-back{background:none;border:0;font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--grey);cursor:pointer;padding:6px 0}
.rst .qz-step{animation:qzIn .45s cubic-bezier(.2,.7,.2,1)}
@keyframes qzIn{from{opacity:0;transform:translateX(18px)}to{opacity:1;transform:none}}
.rst .qz-flag{margin-top:20px;padding:16px 18px;background:#F4EDE0;border:1px solid #D9C7A3;font-size:15px}
.rst .qz-res .eyebrow{margin-bottom:10px}
.rst .qz-cards{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:22px}
.rst .qz-card{border:1px solid #D3D1C5;background:#F6F4EE;padding:22px;display:flex;flex-direction:column;gap:8px}
.rst .qz-card.dark{background-color:var(--night);color:var(--cream);border-color:#262A21;background-image:linear-gradient(#1C2019 1px,transparent 1px),linear-gradient(90deg,#1C2019 1px,transparent 1px);background-size:48px 48px}
.rst .qz-card .k{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--olive)}
.rst .qz-card.dark .k{color:var(--sage)}
.rst .qz-card h3{font-size:32px}
.rst .qz-card p{color:var(--grey);font-size:15px}.rst .qz-card.dark p{color:#B8B3A6}
.rst .qz-card .price{font-family:var(--display);font-size:40px;line-height:1}
.rst .qz-card .price small{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;margin-left:6px;color:var(--sage)}
.rst .qz-card .btn{margin-top:auto;align-self:flex-start}
.rst .qz-card.dark .btn{background:var(--cream);color:var(--night);border-color:var(--cream)}
.rst .qz-why-list{list-style:none;padding:0;margin:22px 0 0;display:grid;gap:10px}
.rst .qz-why-list li{padding-left:22px;position:relative;font-size:15.5px}
.rst .qz-why-list li:before{content:"";position:absolute;left:0;top:.7em;width:12px;height:1px;background:var(--olive)}
.rst .qz-help{margin-top:30px;padding-top:24px;border-top:1px solid #D3D1C5}
.rst .qz-help h3{font-size:24px}
.rst .qz-phases{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:14px}
.rst .qz-phases div{border-top:2px solid var(--olive);padding-top:10px;font-size:14px;color:var(--grey)}
.rst .qz-phases b{display:block;font-family:var(--display);font-weight:500;font-size:18px;text-transform:uppercase;color:var(--ink)}
.rst .qz-more{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px;align-items:center}
.rst .qz-more a.link{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase}
@media (max-width:700px){.rst .qz-cards,.rst .qz-phases{grid-template-columns:1fr 1fr}.rst .qz-cards{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){.rst .qz-step{animation:none}}
</style>"""

BODY = """<section class="dark qz-hero"><div class="wrap">
  <div class="eyebrow">2-Minute Quiz</div>
  <h1>Find your program.</h1>
  <p class="sub">Ten quick questions. You'll get the RESET program that fits where you're starting, the level of support that fits how you work, and what the next 12 weeks look like.</p>
</div></section>
<div class="qz-wrap"><div class="qz" id="qz" aria-live="polite"></div></div>
<section style="padding-block:40px 64px"><div class="wrap" style="max-width:860px"><p style="font-size:13px;color:var(--grey)">This quiz is education, not a diagnosis. If you have warning signs like numbness or weakness that keeps spreading, loss of bladder or bowel control, chest pain, or unexplained fever or weight loss, see a healthcare provider first.</p></div></section>
<script>
(function(){
var P=@@DATA@@, R="../";
var A={}, i=0;
function g(){return A.goal||"pain"}
var Q=[
 {id:"goal",q:"What brings you to RESET?",why:"Rehab, sport and fat loss all use the same phased system, but the programming is very different.",o:[["pain","Get out of pain","Back, neck, knee, shoulder or hip"],["sport","Perform better","Golf, pickleball, dance or school sports"],["fat","Lose fat, keep muscle","And keep it off this time"]]},
 {id:"area",q:function(){return g()=="pain"?"Where do you feel it most?":g()=="sport"?"What do you train for?":"What's gotten in the way before?"},
  why:function(){return g()=="pain"?"Pain is real, but where you feel it isn't always where it starts. Each program begins by finding what eases it.":g()=="sport"?"Each sport loads the body differently. Your program trains the positions and speeds your sport actually asks for.":"Most diets fail because they cost muscle. Keeping muscle is what keeps your metabolism and the results."},
  o:function(){return g()=="pain"?[["back","Low back",""],["neck","Neck",""],["knee","Knee",""],["shoulder","Shoulder",""],["hip","Hip",""]]:g()=="sport"?[["golf","Golf",""],["pickleball","Pickleball",""],["dance","Dance",""],["student-athlete","School sports","Student athlete"]]:[["noplan","No real plan","I wing it"],["muscle","I lose muscle","And feel weak"],["regain","It comes back","I regain the weight"],["time","Not enough time","Life gets busy"]]}},
 {id:"dur",q:function(){return g()=="pain"?"How long has this been going on?":"How long have you been working on this?"},why:"Longer-running problems usually need more structure, not more rest. Rest is the trap.",o:function(){return g()=="pain"?[["new","Under 6 weeks",""],["mid","6 weeks to 6 months",""],["long","Over 6 months",""],["recur","It comes and goes",""]]:[["new","Just starting",""],["mid","A few months",""],["long","Over a year",""],["recur","On and off",""]]}},
 {id:"flag",q:"Do any of these apply to you right now?",hint:"Numbness or weakness that keeps spreading, loss of bladder or bowel control, chest pain, unexplained fever or weight loss, or surgery in the last 12 weeks.",why:"This is the safety check. Some things need a provider's eyes before any exercise program.",o:[["no","No, none of these",""],["unsure","Not sure",""],["yes","Yes, one or more",""]]},
 {id:"tried",q:function(){return g()=="pain"?"Have you tried treatment or exercises for this?":"Have you followed a program before?"},why:"Treatment and rehab are about 35% of the work. The other 65% is what you do after, and that's what RESET is built for.",o:[["no","Not yet",""],["came","Yes, it helped, then it came back",""],["didnt","Yes, it didn't really help",""]]},
 {id:"where",q:"Where will you train?",why:"Every exercise has a home version with a band and a pair of dumbbells or a kettlebell, plus gym options.",o:[["home","At home",""],["gym","At a gym",""],["both","Both",""]]},
 {id:"days",q:"How many days a week can you realistically train?",why:"Consistency beats intensity. Every plan works with what you can actually keep doing.",o:[["2","2 days",""],["3","3 days",""],["4","4 or more",""]]},
 {id:"style",q:"How do you like to work?",why:"Same program, three levels of help. This is the biggest factor in which one fits you.",o:[["self","On my own","Give me the plan and I'll run it"],["guided","With a coach","A plan built for me, with weekly check-ins"],["doctor","With the doctor","Weekly meetings with Dr. Urrutia"]]},
 {id:"form",q:"How confident are you doing exercises with good form?",why:"Sets are done at 7 to 8 out of 10 effort. Good form is what makes that safe and productive.",o:[["very","Very confident",""],["some","Somewhat",""],["not","Not very",""]]},
 {id:"win",q:"What would make the next 12 weeks a win?",why:"You move to each phase when you pass its test, not when the calendar says so. This is the test you're working toward.",o:[["life","Everyday life without thinking about it",""],["active","Back to my sport or workouts",""],["strong","Stronger than before",""],["lean","Leaner, and keeping it",""]]}
];
var el=document.getElementById("qz");
function val(x){return typeof x=="function"?x():x}
function track(n,p){if(typeof gtag=="function")gtag("event",n,p||{})}
function render(){
 if(i>=Q.length) return result();
 var q=Q[i], opts=val(q.o);
 var h='<div class="qz-step"><div class="qz-top"><span>Question '+(i+1)+' of '+Q.length+'</span><span>'+Math.round(i/Q.length*100)+'%</span></div><div class="qz-bar"><i style="width:'+(i/Q.length*100)+'%"></i></div>';
 h+='<h2>'+val(q.q)+'</h2>'+(q.hint?'<p class="hint">'+q.hint+'</p>':'')+'<div class="qz-opts">';
 opts.forEach(function(o){h+='<button type="button" class="qz-opt'+(A[q.id]==o[0]?' sel':'')+'" data-v="'+o[0]+'"><b>'+o[1]+'</b>'+(o[2]?'<span>'+o[2]+'</span>':'')+'</button>'});
 h+='</div><div class="qz-why"><b>Why we ask</b>'+val(q.why)+'</div><div class="qz-nav">'+(i>0?'<button type="button" class="qz-back">← Back</button>':'<span></span>')+'</div></div>';
 el.innerHTML=h;
 setTimeout(function(){var bar=el.querySelector(".qz-bar i");if(bar)bar.style.width=((i+1)/Q.length*100)+"%"},30);
 el.querySelectorAll(".qz-opt").forEach(function(b){b.onclick=function(){
   if(q.id=="goal"&&A.goal!=b.dataset.v){delete A.area}
   A[q.id]=b.dataset.v;b.classList.add("sel");if(i==0)track("quiz_start");
   setTimeout(function(){i++;render();el.scrollIntoView({behavior:"smooth",block:"start"})},220)}});
 var bk=el.querySelector(".qz-back");if(bk)bk.onclick=function(){i--;render()};
}
function result(){
 var slug=g()=="pain"?A.area:g()=="sport"?A.area:"nutrition"; if(!P[slug])slug="back";
 var p=P[slug];
 // How they want to work decides the tier. Other answers can only nudge Self-Guided up to Custom.
 var s=({very:0,some:1,not:2})[A.form]+({no:0,came:1,didnt:2})[A.tried]+({new:0,mid:1,long:2,recur:1})[A.dur];
 var tier=({self:"self",guided:"custom",doctor:"doctor"})[A.style]||"custom";
 var bumped=false; if(tier=="self"&&s>=4){tier="custom";bumped=true}
 var T={self:{name:"Self-Guided",price:"$"+p.self,unit:"one time",href:p.pay,cta:"Get the guide",desc:"The full Block 01 guide, exercise video library, tracking tools and 12 weekly lessons. Yours for life."},
  custom:{name:"Custom",price:"$133",unit:"per month",href:R+slug+"/checkout/?plan=2",cta:"Start Custom",desc:"An onboarding call, programming tailored to you, and weekly guidance and adjustments. $399 per 12-week block, cancel anytime."},
  doctor:{name:"Doctor-Led",price:"$333",unit:"per month",href:R+slug+"/checkout/?plan=3",cta:"Apply for a spot",desc:"Everything in Custom, plus an onboarding call and weekly meetings with Dr. Urrutia. $999 per 12-week block, cancel anytime."}};
 var t=T[tier];
 var why=[];
 why.push(g()=="pain"?"You said your "+p.name.toLowerCase()+" is what's bothering you most, so we start by finding what eases it, then build strength around it.":g()=="sport"?"You train for "+(slug=="student-athlete"?"school sports":p.name.toLowerCase())+", so the program trains the positions and speed it asks for.":"You want to lose fat and keep muscle, so the plan protects strength while the weight comes off.");
 if(A.tried=="came")why.push("It helped before, then came back. That usually means the strength phase never happened. Phases 3 and 4 are where this program earns its keep.");
 if(A.tried=="didnt")why.push("What you tried didn't stick, so more support matters. That's part of why we matched your support level the way we did.");
 if(A.dur=="long"||A.dur=="recur")why.push("This has been around a while. Longer-running problems respond to structure and progressive load, not more rest.");
 why.push(({home:"You'll train at home: every exercise has a band and dumbbell or kettlebell version.",gym:"You'll train at a gym, so every exercise includes a gym option.",both:"You can train at home or the gym. Every exercise has both."})[A.where]);
 why.push(({"2":"Two days a week is enough to start. The plan is built for what you'll actually keep doing.","3":"Three days a week is the sweet spot for most people.","4":"Four or more days lets you move through each phase with room to spare."})[A.days]);
 if(bumped)why.push("You'd rather work on your own, but with how long this has been going on and how past attempts went, a plan built for you with weekly check-ins gives you the best shot. Self-Guided is still an option below.");
 if(tier=="custom"&&s>=5)why.push("If you want the most hands-on help, Doctor-Led adds weekly meetings with Dr. Urrutia.");
 if(A.form=="not")why.push("You're not fully confident with form yet, so coaching and feedback will speed things up and keep it safe.");
 var flag=A.flag=="yes"?'<div class="qz-flag"><b>Before you start:</b> based on your answer, please get checked by a healthcare provider first. Once you\\'re cleared, this is your best fit.</div>':A.flag=="unsure"?'<div class="qz-flag"><b>Not sure about the safety check?</b> Every program starts with a short check-in that screens for warning signs. If anything comes up, we\\'ll point you to a provider first.</div>':"";
 var others=["self","custom","doctor"].filter(function(k){return k!=tier}).map(function(k){return '<a class="link" href="'+T[k].href+'">'+T[k].name+' ('+T[k].price+')</a>'}).join(" · ");
 el.innerHTML='<div class="qz-step qz-res"><div class="qz-bar"><i style="width:100%"></i></div><div class="eyebrow">Your Match</div><h2>'+p.name+' + '+t.name+'</h2>'+flag+
 '<div class="qz-cards"><div class="qz-card"><span class="k">Your program</span><h3>'+p.name+'</h3><p>'+p.desc+'</p><a class="btn ghost" href="'+R+slug+'/">See the program →</a></div>'+
 '<div class="qz-card dark"><span class="k">Your support level</span><h3>'+t.name+'</h3><div class="price">'+t.price+'<small>'+t.unit+'</small></div><p>'+t.desc+'</p><a class="btn" href="'+t.href+'">'+t.cta+' →</a></div></div>'+
 '<ul class="qz-why-list">'+why.map(function(w){return "<li>"+w+"</li>"}).join("")+'</ul>'+
 '<div class="qz-help"><div class="eyebrow">How RESET Helps</div><h3>Your next 12 weeks</h3><div class="qz-phases"><div><b>Calm</b>Weeks 1–2. Find what eases it.</div><div><b>Restore</b>Weeks 3–5. Clean up how you move.</div><div><b>Reinforce</b>Weeks 6–9. Add real load.</div><div><b>Return</b>Weeks 10–12. Back to what you love.</div></div>'+
 '<p style="margin-top:16px;color:var(--grey);font-size:15px">You move on when you pass each phase\\'s test, not when the calendar says so. Then Block 02 picks up where this one ends, because strength you stop building fades.</p></div>'+
 '<div class="qz-more"><span style="font-size:14px;color:var(--grey)">Other options: '+others+'</span></div>'+
 '<div class="qz-more"><a class="btn ghost" href="'+R+slug+'/free-guide/">Not ready? Get the free '+p.name+' guide</a><button type="button" class="qz-back" id="qz-re">↺ Retake the quiz</button></div></div>';
 document.getElementById("qz-re").onclick=function(){A={};i=0;render()};
 track("quiz_complete",{program:slug,tier:tier,safety_flag:A.flag});
}
render();
})();
</script>"""
page = head + CSS + BODY.replace("@@DATA@@", data) + foot
out = ROOT / "quiz/index.html"; out.parent.mkdir(exist_ok=True); out.write_text(page)
print("wrote", out.relative_to(ROOT))
