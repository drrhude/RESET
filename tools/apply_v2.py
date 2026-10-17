"""Applies the v2 look to the 20 program pages (English + Spanish): links assets/v2.css,
adds a quiz prompt box before the closing section, and a small scroll-reveal script.
Safe to re-run: everything it adds is wrapped in <!--v2--> markers and replaced each time."""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
EN = ["back", "neck", "knee", "shoulder", "hip", "golf", "pickleball", "dance", "student-athlete", "nutrition"]
ES = ["espalda", "cuello", "rodilla", "hombro", "cadera", "golf", "pickleball", "danza", "atleta-estudiante", "nutricion"]
QUIZ = {"en": ("Not sure this is the one?", "Take the 2-minute quiz", "10 questions. Get the program and support level that fit where you're starting.", "../quiz/", "Take the quiz"),
        "es": ("¿No está seguro de que sea este?", "Haga el cuestionario de 2 minutos", "10 preguntas. Reciba el programa y el nivel de apoyo que se ajustan a donde usted empieza.", "../cuestionario/", "Hacer el cuestionario")}
JS = """<script>(function(){var r=document.querySelector(".rst");if(!r||!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion: reduce)").matches)return;r.classList.add("v2r");
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.08});
r.querySelectorAll("section:not(.hero) > .wrap").forEach(function(w){io.observe(w)})})();</script>"""
def apply(path, lang, depth):
    s = path.read_text()
    s = re.sub(r"<!--v2-->.*?<!--/v2-->", "", s, flags=re.S)
    css = f'<!--v2--><link rel="stylesheet" href="{"../" * depth}assets/v2.css"><!--/v2-->'
    i = s.index('<div class="rst"'); s = s[:i] + css + s[i:]
    e, h, p, href, b = QUIZ[lang]
    box = f'<!--v2--><section class="v2-quiz"><div class="wrap"><div><div class="eyebrow">{e}</div><h2>{h}</h2><p>{p}</p></div><a class="btn" href="{href}">{b} <span class="arr">→</span></a></div></section><!--/v2-->\n'
    j = s.index('<section class="dark belief">'); s = s[:j] + box + s[j:]
    k = s.rindex("</body>"); s = s[:k] + "<!--v2-->" + JS + "<!--/v2-->\n" + s[k:]
    path.write_text(s)
for d in EN: apply(ROOT / d / "index.html", "en", 1)
for d in ES: apply(ROOT / "es" / d / "index.html", "es", 2)
print("applied to", len(EN) + len(ES), "pages")
