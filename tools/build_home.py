"""Builds the RESET homepage in English (/) and Spanish (/es/).
  python3 tools/build_home.py            -> writes index.html and es/index.html
  python3 tools/build_home.py --preview  -> writes preview/index.html (English, noindex) instead
Reuses the original head, nav and footer (frozen in tools/_shell.html and tools/_shell_es.html),
plus the shared styles and scripts in tools/home.css.html and tools/home.js.html."""
import re, sys, json, pathlib, html as H
ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
PREVIEW = "--preview" in sys.argv
CSS = (TOOLS / "home.css.html").read_text()
JS = (TOOLS / "home.js.html").read_text()
STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg>'

def shell_for(lang):
    f = TOOLS / ("_shell.html" if lang == "en" else "_shell_es.html")
    if not f.exists():
        f.write_text((ROOT / ("index.html" if lang == "en" else "es/index.html")).read_text())
    return f.read_text()

L = {
"en": dict(
  r="", prog="", assets="assets/", quiz="quiz/", guides="free-guides/", about="about/", contact="contact/",
  eyebrow="Rehab + Performance", h1="Rebuild the body you live in.",
  sub="Doctor-built 12-week programs for pain, performance and fat loss. Train at home or in the gym, in English or Spanish.",
  cta1="Find your program", cta2="Take the 2-minute quiz",
  offer_b="Not sure where to start?", offer='Answer 10 quick questions and get your program and support level. Or <a href="{guides}">start with a free guide</a>.',
  trust=[("Doctor-Built", "Every program, every phase"), ("10 Years", "Active duty, U.S. Coast Guard"), ("10 Programs", "Rehab, sport + nutrition"), ("Home or Gym", "Every exercise has both"), ("EN + ES", "Every program in Spanish")],
  find_l="Find Your Program", find_h="Where are you starting?",
  find_p='Pick the closest match. Each program page shows exactly what\'s inside, week by week, and all three ways to do it. Not sure? <a href="{quiz}" style="color:var(--olive-d);font-weight:700">Take the quiz</a>.',
  see="See the program",
  groups=[("Rehab", "Get out of pain and build it back stronger.", [
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
      ("nutrition", "Nutrition", "Lose fat without losing muscle, then keep it off for good.")])],
  how_l="How It Works", how_h="12 weeks. 4 phases.", how_p="You move to the next phase when you pass its test, not when the calendar says so.",
  phases=[("Calm", "Weeks 1–2", "Get out of pain fast. Find where it's coming from and the movements that ease it."),
          ("Restore", "Weeks 3–5", "Clean up how you move and start real strength work."),
          ("Reinforce", "Weeks 6–9", "Add real load. Strength is what turns the alarm down."),
          ("Return", "Weeks 10–12", "Back to the things you've been avoiding.")],
  split_l="The 35 / 65 Rule", split_h="Treatment is 35%. RESET is built for the other 65%.",
  split_aria="35 percent of recovery happens in treatment, 65 percent in the rest of your life",
  seg_a="Treatment + rehab", seg_b="The rest of your life",
  leg_a="<b>The 35%:</b> treatment and rehab. The spark that gets things moving.",
  leg_b="<b>The 65%:</b> how you train, sleep, eat and move between sessions. That's where the change sticks, and it's what RESET coaches.",
  rev_l="Patient Reviews", rev_h="What people say about working with Dr. Urrutia",
  rev_p="from 80 Google reviews by people he's worked with in person. RESET brings that same coaching online.",
  reviews=[("Doctor is extremely compassionate. Explains everything so well.", "Trisha M."), ("Excellent intake appointment.", "John S."), ("Excellent service.", "Rahila V.")],
  review_word="Google review", stars_aria="5 out of 5 stars",
  tiers_l="Choose Your Support", tiers_h="Three ways to do it", tiers_p="Same program, three levels of help. Start on your own or work with us every week.",
  tiers=[("Tier 01", "Self-Guided", "$197", "one time", "Nutrition: $147 · Lifetime access to Block 01", ["The full Block 01 guide", "Exercise video library", "Check-in and tracking tools", "12 weekly lessons"], ""),
         ("Tier 02", "Custom", "$133", "per month", "$399 per 12-week block · cancel anytime", ["Everything in Self-Guided", "Onboarding call to set up your plan", "Programming tailored to you", "Weekly guidance and adjustments"], "Most popular"),
         ("Tier 03", "Doctor-Led", "$333", "per month", "$999 per 12-week block · cancel anytime", ["Everything in Custom", "Onboarding call with Dr. Urrutia", "Weekly meeting with Dr. Urrutia", "Personalized progressions"], "Limited spots")],
  choose="Choose your program", tiers_foot="Custom and Doctor-Led renew into your next 12-week block until you cancel. That's how the progress sticks.",
  doc_l="The Founder", doc_alt="Dr. Jonathan Urrutia, founder of RESET",
  doc_p1="Ten years on active duty in the Coast Guard. A former bodybuilding competitor. A doctor who works with people in pain and athletes every week, and a husband and father who trains around a full life like you do.",
  doc_p2='The same story kept coming up: "I felt better, then I was right back where I started." The pain left, the work stopped, and nothing else changed. RESET is what I built to fix that, so the progress keeps going after week 12.',
  path=[("Served", "U.S. Coast Guard", "10 years active duty."), ("Trained", "Doctorate, 2022", "Parker University in Dallas."),
        ("Built", "His own practice", "Treating pain and training athletes every week."), ("Now", "Building RESET", "10 programs in English and Spanish, coaching Doctor-Led members each week.")],
  story="Read the full story",
  faq_l="FAQs", faq_h="Questions", faq_p="Straight answers before you start. Still unsure? Send us a message.", contact_btn="Contact us",
  faq=[("Who are RESET programs for?", "Adults dealing with back, neck, knee, shoulder or hip pain, athletes who want to perform and stay healthy, and anyone ready to lose fat and keep muscle. Each program meets you where you are."),
       ("Do I need a gym?", "No. Every exercise has a home version using a band and a pair of dumbbells or a kettlebell. Gym options are listed for every exercise."),
       ("How long is a program?", "Each block is 12 weeks in four phases. A full track is four blocks, one year, because strength you stop building fades."),
       ("What's the difference between the tiers?", "Self-Guided is the full Block 01 guide and video library, yours for life. Custom adds an onboarding call, programming tailored to you and weekly guidance. Doctor-Led adds weekly meetings with Dr. Urrutia."),
       ("Is RESET medical care?", "No. RESET programs are education and exercise. They don't diagnose or treat any condition. The check-in screens for warning signs that need a doctor first."),
       ("Can I cancel?", "Yes. Custom and Doctor-Led are month to month. Cancel anytime before your next billing date."),
       ("Is it available in Spanish?", "Yes. Every program is available in English and Spanish.")],
  end_l="Start Today", end_h="We don't have weak bodies. We have weak systems.", end_p="Your body is built to be resilient. RESET gives it a way to get there.",
  end_quiz="Take the quiz", hero_aria="Welcome", trust_aria="Why RESET", out="index.html"),

"es": dict(
  r="../", prog="", assets="../assets/", quiz="cuestionario/", guides="guias-gratis/", about="nosotros/", contact="contacto/",
  eyebrow="Rehabilitación + Rendimiento", h1="Reconstruya el cuerpo en el que vive.",
  sub="Programas de 12 semanas creados por un doctor para el dolor, el rendimiento y la pérdida de grasa. Entrene en casa o en el gimnasio, en español o en inglés.",
  cta1="Encuentre su programa", cta2="Haga el cuestionario de 2 minutos",
  offer_b="¿No sabe por dónde empezar?", offer='Responda 10 preguntas rápidas y reciba su programa y su nivel de apoyo. O <a href="{guides}">empiece con una guía gratis</a>.',
  trust=[("Creado por un doctor", "Cada programa, cada fase"), ("10 años", "Servicio activo, Guardia Costera de EE. UU."), ("10 programas", "Rehabilitación, deporte + nutrición"), ("Casa o gimnasio", "Cada ejercicio tiene ambas opciones"), ("ES + EN", "Todos los programas en español")],
  find_l="Encuentre su programa", find_h="¿Dónde empieza usted?",
  find_p='Elija la opción más cercana. Cada programa muestra exactamente lo que incluye, semana por semana, y las tres formas de hacerlo. ¿No está seguro? <a href="{quiz}" style="color:var(--olive-d);font-weight:700">Haga el cuestionario</a>.',
  see="Ver el programa",
  groups=[("Rehabilitación", "Salga del dolor y vuelva más fuerte.", [
      ("espalda", "Espalda baja", "Dolor de espalda baja que regresa, rigidez y recaídas."),
      ("cuello", "Cuello", "Cuello de escritorio, rigidez, dolores de cabeza por tensión y síntomas en el brazo."),
      ("rodilla", "Rodilla", "Dolor al frente de la rodilla, rodillas rígidas o con artritis, recuperación tras una lesión."),
      ("hombro", "Hombro", "Dolor al levantar el brazo, irritación del manguito rotador, hombros rígidos."),
      ("cadera", "Cadera", "Dolor al costado de la cadera, en la ingle y caderas rígidas o con artritis.")]),
    ("Rendimiento", "Entrene el cuerpo que su deporte necesita.", [
      ("golf", "Golf", "Más distancia, un swing sin dolor y un cuerpo que aguanta 18 hoyos."),
      ("pickleball", "Pickleball", "Pies más rápidos, menos molestias y un cuerpo que juega varios días por semana."),
      ("danza", "Danza", "Vuelva a bailar después de una lesión y gane fuerza, salto y resistencia."),
      ("atleta-estudiante", "Atleta estudiante", "Entrenamiento de pretemporada a postemporada para atletas jóvenes.")]),
    ("Nutrición", "Pierda grasa, conserve músculo y no la recupere.", [
      ("nutricion", "Nutrición", "Pierda grasa sin perder músculo y mantenga el resultado.")])],
  how_l="Cómo funciona", how_h="12 semanas. 4 fases.", how_p="Pasa a la siguiente fase cuando supera su prueba, no cuando lo dice el calendario.",
  phases=[("Calmar", "Semanas 1–2", "Salga del dolor rápido. Encuentre de dónde viene y los movimientos que lo alivian."),
          ("Restaurar", "Semanas 3–5", "Mejore cómo se mueve y empiece el trabajo de fuerza real."),
          ("Reforzar", "Semanas 6–9", "Agregue carga real. La fuerza es lo que apaga la alarma."),
          ("Regresar", "Semanas 10–12", "Vuelva a lo que ha estado evitando.")],
  split_l="La regla 35 / 65", split_h="El tratamiento es el 35%. RESET está hecho para el otro 65%.",
  split_aria="El 35 por ciento de la recuperación ocurre en el tratamiento y el 65 por ciento en el resto de su vida",
  seg_a="Tratamiento + rehabilitación", seg_b="El resto de su vida",
  leg_a="<b>El 35%:</b> tratamiento y rehabilitación. La chispa que pone todo en marcha.",
  leg_b="<b>El 65%:</b> cómo entrena, duerme, come y se mueve entre sesiones. Ahí es donde el cambio se queda, y es lo que RESET entrena.",
  rev_l="Reseñas de pacientes", rev_h="Lo que dicen de trabajar con el Dr. Urrutia",
  rev_p="de 80 reseñas en Google de personas con las que ha trabajado en persona. RESET lleva ese mismo acompañamiento en línea.",
  reviews=[("Doctor is extremely compassionate. Explains everything so well.", "Trisha M."), ("Excellent intake appointment.", "John S."), ("Excellent service.", "Rahila V.")],
  review_word="reseña en Google", stars_aria="5 de 5 estrellas",
  tiers_l="Elija su apoyo", tiers_h="Tres formas de hacerlo", tiers_p="El mismo programa, tres niveles de apoyo. Empiece por su cuenta o trabaje con nosotros cada semana.",
  tiers=[("Nivel 01", "Autoguiado", "$197", "pago único", "Nutrición: $147 · Acceso de por vida al Bloque 01", ["La guía completa del Bloque 01", "Biblioteca de videos de ejercicios", "Herramientas de seguimiento", "12 lecciones semanales"], ""),
         ("Nivel 02", "Personalizado", "$133", "al mes", "$399 por bloque de 12 semanas · cancele cuando quiera", ["Todo lo del Autoguiado", "Llamada inicial para armar su plan", "Programación hecha para usted", "Guía y ajustes semanales"], "El más popular"),
         ("Nivel 03", "Con el doctor", "$333", "al mes", "$999 por bloque de 12 semanas · cancele cuando quiera", ["Todo lo del Personalizado", "Llamada inicial con el Dr. Urrutia", "Reunión semanal con el Dr. Urrutia", "Progresiones personalizadas"], "Cupos limitados")],
  choose="Elija su programa", tiers_foot="Personalizado y Con el doctor se renuevan en su siguiente bloque de 12 semanas hasta que cancele. Así es como el progreso se mantiene.",
  doc_l="El fundador", doc_alt="Dr. Jonathan Urrutia, fundador de RESET",
  doc_p1="Diez años de servicio activo en la Guardia Costera. Excompetidor de fisicoculturismo. Un doctor que trabaja cada semana con personas con dolor y con atletas, y un esposo y padre que entrena alrededor de una vida ocupada, igual que usted.",
  doc_p2='La misma historia se repetía: "Me sentí mejor y luego volví a donde empecé." El dolor se fue, el trabajo se detuvo y nada más cambió. Creé RESET para resolver eso, para que el progreso siga después de la semana 12.',
  path=[("Sirvió", "Guardia Costera de EE. UU.", "10 años de servicio activo."), ("Se formó", "Doctorado, 2022", "Parker University en Dallas."),
        ("Construyó", "Su propia práctica", "Trata el dolor y entrena atletas cada semana."), ("Ahora", "Construye RESET", "10 programas en español e inglés, con reuniones semanales para miembros Con el doctor.")],
  story="Lea la historia completa",
  faq_l="Preguntas", faq_h="Preguntas", faq_p="Respuestas directas antes de empezar. ¿Todavía tiene dudas? Envíenos un mensaje.", contact_btn="Contáctenos",
  faq=[("¿Para quién son los programas RESET?", "Adultos con dolor de espalda, cuello, rodilla, hombro o cadera, atletas que quieren rendir y mantenerse sanos, y cualquier persona lista para perder grasa y conservar músculo. Cada programa empieza donde usted está."),
       ("¿Necesito un gimnasio?", "No. Cada ejercicio tiene una versión para casa con una banda y un par de mancuernas o una pesa rusa. También hay opciones de gimnasio para cada ejercicio."),
       ("¿Cuánto dura un programa?", "Cada bloque dura 12 semanas en cuatro fases. Un programa completo son cuatro bloques, un año, porque la fuerza que deja de construir se pierde."),
       ("¿Cuál es la diferencia entre los niveles?", "Autoguiado es la guía completa del Bloque 01 y la biblioteca de videos, suyas para siempre. Personalizado agrega una llamada inicial, programación hecha para usted y guía semanal. Con el doctor agrega reuniones semanales con el Dr. Urrutia."),
       ("¿RESET es atención médica?", "No. Los programas RESET son educación y ejercicio. No diagnostican ni tratan ninguna condición. La evaluación inicial busca señales de alerta que requieren ver a un doctor primero."),
       ("¿Puedo cancelar?", "Sí. Personalizado y Con el doctor son mes a mes. Cancele cuando quiera antes de su próxima fecha de cobro."),
       ("¿Está disponible en inglés?", "Sí. Todos los programas están disponibles en español y en inglés.")],
  end_l="Empiece hoy", end_h="No tenemos cuerpos débiles. Tenemos sistemas débiles.", end_p="Su cuerpo está hecho para ser resistente. RESET le da el camino para lograrlo.",
  end_quiz="Haga el cuestionario", hero_aria="Bienvenida", trust_aria="Por qué RESET", out="es/index.html"),
}

def build(lang):
    t = L[lang]
    shell = shell_for(lang)
    head = shell[:shell.index('<section class="dark hero" id="programs">')]
    foot = shell[shell.index("<footer>"):]
    pre = "../" if PREVIEW else ""          # preview lives one folder deeper
    def P(x): return pre + x
    if PREVIEW:
        fix = lambda s: re.sub(r'(href|src)="(?!https?:|#|data:|mailto:|tel:|/)([^"]*)"', lambda m: f'{m.group(1)}="../{m.group(2)}"', s)
        head, foot = fix(head), fix(foot)
        head = head.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 1)
    q, gd = P(t["quiz"]), P(t["guides"])
    A = P(t["assets"])
    n = 0; finder = ""
    for g, d, items in t["groups"]:
        tiles = ""
        for slug, name, desc in items:
            n += 1
            tiles += f'<a class="rv-prog" href="{P(slug)}/"><span class="num">{n:02d}</span><h3>{name}</h3><p>{H.escape(desc)}</p><span class="go">{t["see"]} <span class="arr">→</span></span></a>'
        finder += f'<div class="rv-group"><div class="rv-gh"><h3>{g}</h3><p>{d}</p></div><div class="rv-progs">{tiles}</div></div>'
    trust = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in t["trust"])
    phases = "".join(f'<div class="phase"><div class="n">{i+1:02d}</div><h3>{a}</h3><div class="w">{b}</div><p>{H.escape(c)}</p></div>' for i, (a, b, c) in enumerate(t["phases"]))
    reviews = "".join(f'<blockquote class="rv-q"><div class="stars" aria-label="{t["stars_aria"]}">{STAR*5}</div><p>&ldquo;{a}&rdquo;</p><cite>{b}, {t["review_word"]}</cite></blockquote>' for a, b in t["reviews"])
    tiers = ""
    for tag, name, price, unit, note, items, badge in t["tiers"]:
        pop = name in ("Custom", "Personalizado")
        tiers += (f'<div class="tier{" pop" if pop else ""}">' + (f'<span class="badge">{badge}</span>' if badge else "") +
                  f'<div class="tag">{tag}</div><h3>{name}</h3><div class="price">{price}<span class="unit">{unit}</span></div><div class="note">{note}</div>'
                  f'<ul>{"".join(f"<li>{i}</li>" for i in items)}</ul><a class="btn{"" if pop else " ghost"}" href="#programs">{t["choose"]}</a></div>')
    path = "".join(f'<li{" class=\"now\"" if i == 3 else ""}><span class="k">{a}</span><b>{b}</b><span>{c}</span></li>' for i, (a, b, c) in enumerate(t["path"]))
    faq_html = "".join(f"<details><summary>{H.escape(a)}</summary><p>{H.escape(b)}</p></details>" for a, b in t["faq"])
    ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [{"@type": "FAQPage", "inLanguage": lang,
          "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in t["faq"]]}]}, ensure_ascii=False) + "</script>"
    body = f"""{CSS}
<section class="rv-hero hero" aria-label="{t['hero_aria']}"><span class="scan" aria-hidden="true"></span>
  <div class="poster" style="background:url({A}hero-poster.webp) center/cover"></div>
  <video autoplay muted loop playsinline preload="metadata" poster="{A}hero-poster.webp" aria-hidden="true" tabindex="-1"><source src="{A}hero.mp4" type="video/mp4"></video>
  <div class="wrap">
    <div class="eyebrow" style="color:var(--sage)">{t['eyebrow']}</div>
    <h1>{t['h1']}</h1>
    <p class="sub">{t['sub']}</p>
    <div class="ctas"><a class="btn" href="#programs">{t['cta1']} <span class="arr">→</span></a><a class="btn ghost" href="{q}">{t['cta2']}</a></div>
    <div class="rv-offer"><b>{t['offer_b']}</b><span>{t['offer'].format(guides=gd)}</span></div>
  </div>
</section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-trust" aria-label="{t['trust_aria']}">{trust}</div>
</div></section>

<section class="rv" id="programs" style="padding-top:8px"><div class="wrap">
  <div class="rv-box mark">
    <div class="rv-head"><div><div class="eyebrow">{t['find_l']}</div><h2>{t['find_h']}</h2></div><p>{t['find_p'].format(quiz=q)}</p></div>
    {finder}
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box night mark">
    <div class="rv-head"><div><div class="eyebrow">{t['how_l']}</div><h2>{t['how_h']}</h2></div><p>{t['how_p']}</p></div>
    <div class="phases">{phases}</div>
    <div class="rv-split">
      <div class="eyebrow">{t['split_l']}</div>
      <h3 style="font-size:clamp(24px,3vw,34px);margin-top:10px;color:var(--cream)">{t['split_h']}</h3>
      <div class="rv-bar" role="img" aria-label="{t['split_aria']}"><div class="seg a"><span><b>35%</b>{t['seg_a']}</span></div><div class="seg b"><span><b>65%</b>{t['seg_b']}</span></div></div>
      <div class="rv-legend"><p>{t['leg_a']}</p><p>{t['leg_b']}</p></div>
    </div>
  </div>
</div></section>

<section class="rv" id="reviews" style="padding-top:0"><div class="wrap">
  <div class="rv-box">
    <div class="rv-head"><div><div class="eyebrow">{t['rev_l']}</div><h2>{t['rev_h']}</h2></div><p><b class="rv-score">5.0 <span class="mini">{STAR*5}</span></b> {t['rev_p']}</p></div>
    <div class="rv-quotes">{reviews}</div>
  </div>
</div></section>

<section class="rv" id="tiers" style="padding-top:0"><div class="wrap">
  <div class="rv-box">
    <div class="rv-head"><div><div class="eyebrow">{t['tiers_l']}</div><h2>{t['tiers_h']}</h2></div><p>{t['tiers_p']}</p></div>
    <div class="tiers">{tiers}</div><p class="tiers-foot">{t['tiers_foot']}</p>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box mark rv-doc">
    <img src="{A}founder-540.webp" srcset="{A}founder-540.webp 540w, {A}founder-900.webp 900w" sizes="(max-width:860px) 92vw, 40vw" width="900" height="1352" alt="{t['doc_alt']}" loading="lazy" decoding="async">
    <div>
      <div class="eyebrow">{t['doc_l']}</div>
      <h2 style="margin-top:12px">Dr. Jonathan Urrutia</h2>
      <p>{t['doc_p1']}</p>
      <p>{t['doc_p2']}</p>
      <ol class="rv-path">{path}</ol>
      <p style="margin-top:24px"><a class="btn ghost" href="{P(t['about'])}">{t['story']} <span class="arr">→</span></a></p>
    </div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box rv-faq">
    <div><div class="eyebrow">{t['faq_l']}</div><h2 style="margin-top:12px">{t['faq_h']}</h2><p>{t['faq_p']}</p><a class="btn ghost" href="{P(t['contact'])}">{t['contact_btn']}</a></div>
    <div class="faq">{faq_html}</div>
  </div>
</div></section>

<section class="rv" style="padding-top:0"><div class="wrap">
  <div class="rv-box night mark rv-cta">
    <div><div class="eyebrow">{t['end_l']}</div><h2 style="margin-top:12px">{t['end_h']}</h2><p>{t['end_p']}</p></div>
    <div class="btns"><a class="btn" href="#programs">{t['cta1']} <span class="arr">→</span></a><a class="btn ghost" href="{q}">{t['end_quiz']}</a></div>
  </div>
</div></section>
{JS}
"""
    page = head.replace("</head>", ld + "\n</head>", 1) + body + foot
    out = ROOT / ("preview/index.html" if PREVIEW else t["out"])
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)
    print("wrote", out.relative_to(ROOT))

if PREVIEW:
    build("en")
else:
    build("en"); build("es")
