"""Builds the RESET program quiz in English (/quiz/) and Spanish (/es/cuestionario/).
10 questions -> program + support tier, with a safety screen and short education along the way.
Run: python3 tools/build_quiz.py"""
import re, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
CSS = (TOOLS / "quiz.css.html").read_text()
PAY = "https://link.fastpaydirect.com/payment-link/"

def shell_parts(lang):
    shell = (TOOLS / ("_shell.html" if lang == "en" else "_shell_es.html")).read_text()
    head = shell[:shell.index('<section class="dark hero" id="programs">')]
    foot = shell[shell.index("<footer>"):]
    fix = lambda s: re.sub(r'(href|src)="(?!https?:|#|data:|mailto:|tel:|/)([^"]*)"', lambda m: f'{m.group(1)}="../{m.group(2)}"', s)
    return fix(head), fix(foot)

L = {
"en": dict(
  out="quiz/index.html", url="https://resethybridrecovery.com/quiz/", alt="https://resethybridrecovery.com/es/cuestionario/",
  title="Which RESET Program Is Right for You? | 2-Minute Quiz",
  desc="Answer 10 quick questions and get the RESET program and support level that fits your pain, sport or goal. Doctor-built, home or gym, English or Spanish.",
  R="../", eyebrow="2-Minute Quiz", h1="Find your program.",
  sub="Ten quick questions. You'll get the RESET program that fits where you're starting, the level of support that fits how you work, and what the next 12 weeks look like.",
  disclaimer="This quiz is education, not a diagnosis. If you have warning signs like numbness or weakness that keeps spreading, loss of bladder or bowel control, chest pain, or unexplained fever or weight loss, see a healthcare provider first.",
  programs={"back": ("back", "Low Back", "Recurring low back pain, stiffness and flare-ups.", "6acfd40f075ea22a20cde7ec", 197),
    "neck": ("neck", "Neck", "Desk neck, stiffness, tension headaches and arm symptoms.", "6acfd452075ea22a20cde7ed", 197),
    "knee": ("knee", "Knee", "Front-of-knee pain, stiff or arthritic knees, post-injury rebuilding.", "6acfd496c0e70c7fefb749fe", 197),
    "shoulder": ("shoulder", "Shoulder", "Painful overhead reach, rotator cuff irritation, stiff shoulders.", "6acfd4da075ea22a20cde7ef", 197),
    "hip": ("hip", "Hip", "Side-of-hip pain, groin pain and stiff or arthritic hips.", "6acfd518c0e70c7fefb74a01", 197),
    "golf": ("golf", "Golf", "More distance, a swing that doesn't hurt, a body that lasts 18 holes.", "6acfd555075ea22a20cde7f1", 197),
    "pickleball": ("pickleball", "Pickleball", "Faster feet, fewer tweaks, a body that plays several days a week.", "6acfd592c0e70c7fefb74a04", 197),
    "dance": ("dance", "Dance", "Return to dance after injury, then build strength, jumps and stamina.", "6acfd5ce075ea22a20cde7f3", 197),
    "student": ("student-athlete", "Student Athlete", "Off-season to post-season training for young athletes.", "6acfd606075ea22a20cde7f5", 197),
    "nutrition": ("nutrition", "Nutrition", "Lose fat without losing muscle, then keep it off for good.", "6acfd63fc0e70c7fefb74a05", 147)},
  checkout="checkout", guide="free-guide",
  S=dict(qof="Question {n} of {t}", why="Why we ask", back="← Back", match="Your Match", yprog="Your program", ysup="Your support level", see="See the program →",
    nextH="Your next 12 weeks", helps="How RESET Helps", other="Other options:", notready="Not ready? Get the free {p} guide", retake="↺ Retake the quiz",
    phases=[["Calm", "Weeks 1–2. Find what eases it."], ["Restore", "Weeks 3–5. Clean up how you move."], ["Reinforce", "Weeks 6–9. Add real load."], ["Return", "Weeks 10–12. Back to what you love."]],
    phasesNote="You move on when you pass each phase's test, not when the calendar says so. Then Block 02 picks up where this one ends, because strength you stop building fades.",
    flagYes="<b>Before you start:</b> based on your answer, please get checked by a healthcare provider first. Once you're cleared, this is your best fit.",
    flagUnsure="<b>Not sure about the safety check?</b> Every program starts with a short check-in that screens for warning signs. If anything comes up, we'll point you to a provider first.",
    tiers={"self": ["Self-Guided", "one time", "Get the guide", "The full Block 01 guide, exercise video library, tracking tools and 12 weekly lessons. Yours for life."],
           "custom": ["Custom", "per month", "Start Custom", "An onboarding call, programming tailored to you, and weekly guidance and adjustments. $399 per 12-week block, cancel anytime."],
           "doctor": ["Doctor-Led", "per month", "Apply for a spot", "Everything in Custom, plus an onboarding call and weekly meetings with Dr. Urrutia. $999 per 12-week block, cancel anytime."]},
    whyPain="You said your {p} is what's bothering you most, so we start by finding what eases it, then build strength around it.",
    whySport="You train for {p}, so the program trains the positions and speed it asks for.", schoolSports="school sports",
    whyFat="You want to lose fat and keep muscle, so the plan protects strength while the weight comes off.",
    whyCame="It helped before, then came back. That usually means the strength phase never happened. Phases 3 and 4 are where this program earns its keep.",
    whyDidnt="What you tried didn't stick, so more support matters. That's part of why we matched your support level the way we did.",
    whyLong="This has been around a while. Longer-running problems respond to structure and progressive load, not more rest.",
    where={"home": "You'll train at home: every exercise has a band and dumbbell or kettlebell version.", "gym": "You'll train at a gym, so every exercise includes a gym option.", "both": "You can train at home or the gym. Every exercise has both."},
    days={"2": "Two days a week is enough to start. The plan is built for what you'll actually keep doing.", "3": "Three days a week is the sweet spot for most people.", "4": "Four or more days lets you move through each phase with room to spare."},
    bumped="You'd rather work on your own, but with how long this has been going on and how past attempts went, a plan built for you with weekly check-ins gives you the best shot. Self-Guided is still an option below.",
    doctorHint="If you want the most hands-on help, Doctor-Led adds weekly meetings with Dr. Urrutia.",
    form="You're not fully confident with form yet, so coaching and feedback will speed things up and keep it safe."),
  Q=[
   {"id": "goal", "q": "What brings you to RESET?", "why": "Rehab, sport and fat loss all use the same phased system, but the programming is very different.",
    "o": [["pain", "Get out of pain", "Back, neck, knee, shoulder or hip"], ["sport", "Perform better", "Golf, pickleball, dance or school sports"], ["fat", "Lose fat, keep muscle", "And keep it off this time"]]},
   {"id": "area", "q": {"pain": "Where do you feel it most?", "sport": "What do you train for?", "fat": "What's gotten in the way before?"},
    "why": {"pain": "Pain is real, but where you feel it isn't always where it starts. Each program begins by finding what eases it.", "sport": "Each sport loads the body differently. Your program trains the positions and speeds your sport actually asks for.", "fat": "Most diets fail because they cost muscle. Keeping muscle is what keeps your metabolism and the results."},
    "o": {"pain": [["back", "Low back", ""], ["neck", "Neck", ""], ["knee", "Knee", ""], ["shoulder", "Shoulder", ""], ["hip", "Hip", ""]],
          "sport": [["golf", "Golf", ""], ["pickleball", "Pickleball", ""], ["dance", "Dance", ""], ["student", "School sports", "Student athlete"]],
          "fat": [["noplan", "No real plan", "I wing it"], ["muscle", "I lose muscle", "And feel weak"], ["regain", "It comes back", "I regain the weight"], ["time", "Not enough time", "Life gets busy"]]}},
   {"id": "dur", "q": {"pain": "How long has this been going on?", "other": "How long have you been working on this?"}, "why": "Longer-running problems usually need more structure, not more rest. Rest is the trap.",
    "o": {"pain": [["new", "Under 6 weeks", ""], ["mid", "6 weeks to 6 months", ""], ["long", "Over 6 months", ""], ["recur", "It comes and goes", ""]],
          "other": [["new", "Just starting", ""], ["mid", "A few months", ""], ["long", "Over a year", ""], ["recur", "On and off", ""]]}},
   {"id": "flag", "q": "Do any of these apply to you right now?", "hint": "Numbness or weakness that keeps spreading, loss of bladder or bowel control, chest pain, unexplained fever or weight loss, or surgery in the last 12 weeks.",
    "why": "This is the safety check. Some things need a provider's eyes before any exercise program.", "o": [["no", "No, none of these", ""], ["unsure", "Not sure", ""], ["yes", "Yes, one or more", ""]]},
   {"id": "tried", "q": {"pain": "Have you tried treatment or exercises for this?", "other": "Have you followed a program before?"}, "why": "Treatment and rehab are about 35% of the work. The other 65% is what you do after, and that's what RESET is built for.",
    "o": [["no", "Not yet", ""], ["came", "Yes, it helped, then it came back", ""], ["didnt", "Yes, it didn't really help", ""]]},
   {"id": "where", "q": "Where will you train?", "why": "Every exercise has a home version with a band and a pair of dumbbells or a kettlebell, plus gym options.", "o": [["home", "At home", ""], ["gym", "At a gym", ""], ["both", "Both", ""]]},
   {"id": "days", "q": "How many days a week can you realistically train?", "why": "Consistency beats intensity. Every plan works with what you can actually keep doing.", "o": [["2", "2 days", ""], ["3", "3 days", ""], ["4", "4 or more", ""]]},
   {"id": "style", "q": "How do you like to work?", "why": "Same program, three levels of help. This is the biggest factor in which one fits you.",
    "o": [["self", "On my own", "Give me the plan and I'll run it"], ["guided", "With a coach", "A plan built for me, with weekly check-ins"], ["doctor", "With the doctor", "Weekly meetings with Dr. Urrutia"]]},
   {"id": "form", "q": "How confident are you doing exercises with good form?", "why": "Sets are done at 7 to 8 out of 10 effort. Good form is what makes that safe and productive.", "o": [["very", "Very confident", ""], ["some", "Somewhat", ""], ["not", "Not very", ""]]},
   {"id": "win", "q": "What would make the next 12 weeks a win?", "why": "You move to each phase when you pass its test, not when the calendar says so. This is the test you're working toward.",
    "o": [["life", "Everyday life without thinking about it", ""], ["active", "Back to my sport or workouts", ""], ["strong", "Stronger than before", ""], ["lean", "Leaner, and keeping it", ""]]}]),

"es": dict(
  out="es/cuestionario/index.html", url="https://resethybridrecovery.com/es/cuestionario/", alt="https://resethybridrecovery.com/quiz/",
  title="¿Qué programa RESET es para usted? | Cuestionario de 2 minutos",
  desc="Responda 10 preguntas rápidas y reciba el programa RESET y el nivel de apoyo que se ajustan a su dolor, su deporte o su meta. Creado por un doctor, en casa o en el gimnasio.",
  R="../", eyebrow="Cuestionario de 2 minutos", h1="Encuentre su programa.",
  sub="Diez preguntas rápidas. Recibirá el programa RESET que se ajusta a donde usted empieza, el nivel de apoyo que va con su forma de trabajar y cómo serán sus próximas 12 semanas.",
  disclaimer="Este cuestionario es educativo, no un diagnóstico. Si tiene señales de alerta como adormecimiento o debilidad que sigue extendiéndose, pérdida del control de la vejiga o del intestino, dolor de pecho, o fiebre o pérdida de peso sin explicación, vea primero a un profesional de la salud.",
  programs={"back": ("espalda", "Espalda baja", "Dolor de espalda baja que regresa, rigidez y recaídas.", "6acfd40f075ea22a20cde7ec", 197),
    "neck": ("cuello", "Cuello", "Cuello de escritorio, rigidez, dolores de cabeza por tensión y síntomas en el brazo.", "6acfd452075ea22a20cde7ed", 197),
    "knee": ("rodilla", "Rodilla", "Dolor al frente de la rodilla, rodillas rígidas o con artritis, recuperación tras una lesión.", "6acfd496c0e70c7fefb749fe", 197),
    "shoulder": ("hombro", "Hombro", "Dolor al levantar el brazo, irritación del manguito rotador, hombros rígidos.", "6acfd4da075ea22a20cde7ef", 197),
    "hip": ("cadera", "Cadera", "Dolor al costado de la cadera, en la ingle y caderas rígidas o con artritis.", "6acfd518c0e70c7fefb74a01", 197),
    "golf": ("golf", "Golf", "Más distancia, un swing sin dolor y un cuerpo que aguanta 18 hoyos.", "6acfd555075ea22a20cde7f1", 197),
    "pickleball": ("pickleball", "Pickleball", "Pies más rápidos, menos molestias y un cuerpo que juega varios días por semana.", "6acfd592c0e70c7fefb74a04", 197),
    "dance": ("danza", "Danza", "Vuelva a bailar después de una lesión y gane fuerza, salto y resistencia.", "6acfd5ce075ea22a20cde7f3", 197),
    "student": ("atleta-estudiante", "Atleta estudiante", "Entrenamiento de pretemporada a postemporada para atletas jóvenes.", "6acfd606075ea22a20cde7f5", 197),
    "nutrition": ("nutricion", "Nutrición", "Pierda grasa sin perder músculo y mantenga el resultado.", "6acfd63fc0e70c7fefb74a05", 147)},
  checkout="pago", guide="guia-gratis",
  S=dict(qof="Pregunta {n} de {t}", why="Por qué preguntamos", back="← Atrás", match="Su resultado", yprog="Su programa", ysup="Su nivel de apoyo", see="Ver el programa →",
    nextH="Sus próximas 12 semanas", helps="Cómo le ayuda RESET", other="Otras opciones:", notready="¿Todavía no? Reciba la guía gratis de {p}", retake="↺ Repetir el cuestionario",
    phases=[["Calmar", "Semanas 1–2. Encuentre lo que lo alivia."], ["Restaurar", "Semanas 3–5. Mejore cómo se mueve."], ["Reforzar", "Semanas 6–9. Agregue carga real."], ["Regresar", "Semanas 10–12. Vuelva a lo que ama."]],
    phasesNote="Avanza cuando supera la prueba de cada fase, no cuando lo dice el calendario. Luego el Bloque 02 sigue donde termina este, porque la fuerza que deja de construir se pierde.",
    flagYes="<b>Antes de empezar:</b> según su respuesta, vea primero a un profesional de la salud. Cuando le den el visto bueno, esta es su mejor opción.",
    flagUnsure="<b>¿No está seguro de la evaluación de seguridad?</b> Cada programa empieza con una evaluación corta que busca señales de alerta. Si aparece algo, le indicaremos que vea a un profesional primero.",
    tiers={"self": ["Autoguiado", "pago único", "Obtener la guía", "La guía completa del Bloque 01, la biblioteca de videos, herramientas de seguimiento y 12 lecciones semanales. Suya para siempre."],
           "custom": ["Personalizado", "al mes", "Empezar Personalizado", "Una llamada inicial, programación hecha para usted y guía y ajustes cada semana. $399 por bloque de 12 semanas, cancele cuando quiera."],
           "doctor": ["Con el doctor", "al mes", "Solicitar un cupo", "Todo lo del Personalizado, más una llamada inicial y reuniones semanales con el Dr. Urrutia. $999 por bloque de 12 semanas, cancele cuando quiera."]},
    whyPain="Dijo que lo que más le molesta es: {p}. Empezamos por encontrar lo que lo alivia y luego construimos fuerza alrededor.",
    whySport="Entrena para {p}, así que el programa trabaja las posiciones y la velocidad que su deporte exige.", schoolSports="deportes escolares",
    whyFat="Quiere perder grasa y conservar músculo, así que el plan protege su fuerza mientras baja de peso.",
    whyCame="Le ayudó antes y luego regresó. Eso casi siempre significa que nunca llegó la fase de fuerza. Las fases 3 y 4 son donde este programa marca la diferencia.",
    whyDidnt="Lo que intentó no funcionó, así que el apoyo importa más. Por eso elegimos su nivel de apoyo así.",
    whyLong="Esto lleva tiempo. Los problemas de larga duración responden a estructura y carga progresiva, no a más descanso.",
    where={"home": "Entrenará en casa: cada ejercicio tiene una versión con banda y mancuernas o pesa rusa.", "gym": "Entrenará en un gimnasio, así que cada ejercicio incluye una opción de gimnasio.", "both": "Puede entrenar en casa o en el gimnasio. Cada ejercicio tiene ambas opciones."},
    days={"2": "Dos días por semana bastan para empezar. El plan está hecho para lo que realmente va a mantener.", "3": "Tres días por semana es el punto ideal para la mayoría.", "4": "Cuatro días o más le permiten avanzar por cada fase con margen."},
    bumped="Prefiere trabajar por su cuenta, pero por el tiempo que lleva esto y cómo le fue antes, un plan hecho para usted con revisiones semanales le da la mejor oportunidad. Autoguiado sigue siendo una opción abajo.",
    doctorHint="Si quiere el apoyo más cercano, Con el doctor agrega reuniones semanales con el Dr. Urrutia.",
    form="Todavía no se siente seguro con la técnica, así que el acompañamiento acelera el progreso y lo mantiene seguro."),
  Q=[
   {"id": "goal", "q": "¿Qué lo trae a RESET?", "why": "La rehabilitación, el deporte y la pérdida de grasa usan el mismo sistema por fases, pero la programación es muy distinta.",
    "o": [["pain", "Salir del dolor", "Espalda, cuello, rodilla, hombro o cadera"], ["sport", "Rendir mejor", "Golf, pickleball, danza o deportes escolares"], ["fat", "Perder grasa, conservar músculo", "Y no recuperarla esta vez"]]},
   {"id": "area", "q": {"pain": "¿Dónde lo siente más?", "sport": "¿Para qué entrena?", "fat": "¿Qué se lo ha impedido antes?"},
    "why": {"pain": "El dolor es real, pero donde lo siente no siempre es donde empieza. Cada programa comienza por encontrar lo que lo alivia.", "sport": "Cada deporte carga el cuerpo de forma distinta. Su programa entrena las posiciones y velocidades que su deporte exige.", "fat": "La mayoría de las dietas fallan porque cuestan músculo. Conservar músculo es lo que mantiene su metabolismo y sus resultados."},
    "o": {"pain": [["back", "Espalda baja", ""], ["neck", "Cuello", ""], ["knee", "Rodilla", ""], ["shoulder", "Hombro", ""], ["hip", "Cadera", ""]],
          "sport": [["golf", "Golf", ""], ["pickleball", "Pickleball", ""], ["dance", "Danza", ""], ["student", "Deportes escolares", "Atleta estudiante"]],
          "fat": [["noplan", "No tengo un plan", "Improviso"], ["muscle", "Pierdo músculo", "Y me siento débil"], ["regain", "Lo recupero", "Vuelvo a subir de peso"], ["time", "No tengo tiempo", "La vida se complica"]]}},
   {"id": "dur", "q": {"pain": "¿Cuánto tiempo lleva con esto?", "other": "¿Cuánto tiempo lleva trabajando en esto?"}, "why": "Los problemas de larga duración necesitan más estructura, no más descanso. El descanso es la trampa.",
    "o": {"pain": [["new", "Menos de 6 semanas", ""], ["mid", "De 6 semanas a 6 meses", ""], ["long", "Más de 6 meses", ""], ["recur", "Va y viene", ""]],
          "other": [["new", "Apenas empiezo", ""], ["mid", "Unos meses", ""], ["long", "Más de un año", ""], ["recur", "A ratos", ""]]}},
   {"id": "flag", "q": "¿Le aplica alguno de estos ahora mismo?", "hint": "Adormecimiento o debilidad que sigue extendiéndose, pérdida del control de la vejiga o del intestino, dolor de pecho, fiebre o pérdida de peso sin explicación, o cirugía en las últimas 12 semanas.",
    "why": "Esta es la evaluación de seguridad. Algunas cosas necesitan la revisión de un profesional antes de cualquier programa de ejercicio.", "o": [["no", "No, ninguno", ""], ["unsure", "No estoy seguro", ""], ["yes", "Sí, uno o más", ""]]},
   {"id": "tried", "q": {"pain": "¿Ha probado tratamiento o ejercicios para esto?", "other": "¿Ha seguido un programa antes?"}, "why": "El tratamiento y la rehabilitación son cerca del 35% del trabajo. El otro 65% es lo que hace después, y para eso está hecho RESET.",
    "o": [["no", "Todavía no", ""], ["came", "Sí, me ayudó y luego regresó", ""], ["didnt", "Sí, pero no me ayudó mucho", ""]]},
   {"id": "where", "q": "¿Dónde va a entrenar?", "why": "Cada ejercicio tiene una versión para casa con una banda y un par de mancuernas o una pesa rusa, además de opciones de gimnasio.", "o": [["home", "En casa", ""], ["gym", "En un gimnasio", ""], ["both", "En ambos", ""]]},
   {"id": "days", "q": "¿Cuántos días por semana puede entrenar de verdad?", "why": "La constancia le gana a la intensidad. Cada plan funciona con lo que usted realmente puede mantener.", "o": [["2", "2 días", ""], ["3", "3 días", ""], ["4", "4 o más", ""]]},
   {"id": "style", "q": "¿Cómo prefiere trabajar?", "why": "El mismo programa, tres niveles de apoyo. Esto es lo que más decide cuál le conviene.",
    "o": [["self", "Por mi cuenta", "Denme el plan y yo lo sigo"], ["guided", "Con un coach", "Un plan hecho para mí, con revisiones semanales"], ["doctor", "Con el doctor", "Reuniones semanales con el Dr. Urrutia"]]},
   {"id": "form", "q": "¿Qué tan seguro se siente haciendo ejercicios con buena técnica?", "why": "Las series se hacen a un esfuerzo de 7 u 8 de 10. La buena técnica es lo que lo hace seguro y productivo.", "o": [["very", "Muy seguro", ""], ["some", "Algo", ""], ["not", "Poco", ""]]},
   {"id": "win", "q": "¿Qué haría de las próximas 12 semanas un éxito?", "why": "Pasa a cada fase cuando supera su prueba, no cuando lo dice el calendario. Esta es la meta hacia la que trabaja.",
    "o": [["life", "Vivir el día sin pensar en ello", ""], ["active", "Volver a mi deporte o entrenamiento", ""], ["strong", "Estar más fuerte que antes", ""], ["lean", "Estar más delgado y mantenerlo", ""]]}]),
}

JS = r"""<script>
(function(){
var C=@@CFG@@, P=C.programs, S=C.S, Q=C.Q, R=C.R;
var A={}, i=0, el=document.getElementById("qz");
function g(){return A.goal||"pain"}
function pick(x,key){ if(x&&typeof x=="object"&&!Array.isArray(x)){ return x[key]!==undefined?x[key]:(x[g()]!==undefined?x[g()]:(g()=="pain"?x.pain:x.other)); } return x; }
function val(q,f){var x=q[f]; if(x&&typeof x=="object"&&!Array.isArray(x)){return x[g()]!==undefined?x[g()]:(g()=="pain"?x.pain:x.other)} return x}
function track(n,p){if(typeof gtag=="function")gtag("event",n,p||{})}
function render(){
 if(i>=Q.length) return result();
 var q=Q[i], opts=val(q,"o");
 var h='<div class="qz-step"><div class="qz-top"><span>'+S.qof.replace("{n}",i+1).replace("{t}",Q.length)+'</span><span>'+Math.round(i/Q.length*100)+'%</span></div><div class="qz-bar"><i style="width:'+(i/Q.length*100)+'%"></i></div>';
 h+='<h2>'+val(q,"q")+'</h2>'+(q.hint?'<p class="hint">'+q.hint+'</p>':'')+'<div class="qz-opts">';
 opts.forEach(function(o){h+='<button type="button" class="qz-opt'+(A[q.id]==o[0]?' sel':'')+'" data-v="'+o[0]+'"><b>'+o[1]+'</b>'+(o[2]?'<span>'+o[2]+'</span>':'')+'</button>'});
 h+='</div><div class="qz-why"><b>'+S.why+'</b>'+val(q,"why")+'</div><div class="qz-nav">'+(i>0?'<button type="button" class="qz-back">'+S.back+'</button>':'<span></span>')+'</div></div>';
 el.innerHTML=h;
 setTimeout(function(){var bar=el.querySelector(".qz-bar i");if(bar)bar.style.width=((i+1)/Q.length*100)+"%"},30);
 el.querySelectorAll(".qz-opt").forEach(function(b){b.onclick=function(){
   if(q.id=="goal"&&A.goal!=b.dataset.v){delete A.area}
   A[q.id]=b.dataset.v;b.classList.add("sel");if(i==0)track("quiz_start",{language:C.lang});
   setTimeout(function(){i++;render();el.scrollIntoView({behavior:"smooth",block:"start"})},220)}});
 var bk=el.querySelector(".qz-back");if(bk)bk.onclick=function(){i--;render()};
}
function result(){
 var key=g()=="fat"?"nutrition":A.area; if(!P[key])key="back";
 var p=P[key], slug=p.slug;
 // How they want to work decides the tier. Other answers can only nudge Self-Guided up to Custom.
 var s=({very:0,some:1,not:2})[A.form]+({no:0,came:1,didnt:2})[A.tried]+({new:0,mid:1,long:2,recur:1})[A.dur];
 var tier=({self:"self",guided:"custom",doctor:"doctor"})[A.style]||"custom";
 var bumped=false; if(tier=="self"&&s>=4){tier="custom";bumped=true}
 var href={self:p.pay,custom:R+slug+"/"+C.checkout+"/?plan=2",doctor:R+slug+"/"+C.checkout+"/?plan=3"};
 var price={self:"$"+p.self,custom:"$133",doctor:"$333"};
 var t=S.tiers[tier];
 var why=[];
 why.push(g()=="pain"?S.whyPain.replace("{p}",p.name.toLowerCase()):g()=="sport"?S.whySport.replace("{p}",key=="student"?S.schoolSports:p.name.toLowerCase()):S.whyFat);
 if(A.tried=="came")why.push(S.whyCame);
 if(A.tried=="didnt")why.push(S.whyDidnt);
 if(A.dur=="long"||A.dur=="recur")why.push(S.whyLong);
 why.push(S.where[A.where]); why.push(S.days[A.days]);
 if(bumped)why.push(S.bumped);
 if(tier=="custom"&&s>=5)why.push(S.doctorHint);
 if(A.form=="not")why.push(S.form);
 var flag=A.flag=="yes"?'<div class="qz-flag">'+S.flagYes+'</div>':A.flag=="unsure"?'<div class="qz-flag">'+S.flagUnsure+'</div>':"";
 var others=["self","custom","doctor"].filter(function(k){return k!=tier}).map(function(k){return '<a class="link" href="'+href[k]+'">'+S.tiers[k][0]+' ('+price[k]+')</a>'}).join(" · ");
 var ph=S.phases.map(function(x){return '<div><b>'+x[0]+'</b>'+x[1]+'</div>'}).join("");
 el.innerHTML='<div class="qz-step qz-res"><div class="qz-bar"><i style="width:100%"></i></div><div class="eyebrow">'+S.match+'</div><h2>'+p.name+' + '+t[0]+'</h2>'+flag+
 '<div class="qz-cards"><div class="qz-card"><span class="k">'+S.yprog+'</span><h3>'+p.name+'</h3><p>'+p.desc+'</p><a class="btn ghost" href="'+R+slug+'/">'+S.see+'</a></div>'+
 '<div class="qz-card dark"><span class="k">'+S.ysup+'</span><h3>'+t[0]+'</h3><div class="price">'+price[tier]+'<small>'+t[1]+'</small></div><p>'+t[3]+'</p><a class="btn" href="'+href[tier]+'">'+t[2]+' →</a></div></div>'+
 '<ul class="qz-why-list">'+why.map(function(w){return "<li>"+w+"</li>"}).join("")+'</ul>'+
 '<div class="qz-help"><div class="eyebrow">'+S.helps+'</div><h3>'+S.nextH+'</h3><div class="qz-phases">'+ph+'</div>'+
 '<p style="margin-top:16px;color:var(--grey);font-size:15px">'+S.phasesNote+'</p></div>'+
 '<div class="qz-more"><span style="font-size:14px;color:var(--grey)">'+S.other+' '+others+'</span></div>'+
 '<div class="qz-more"><a class="btn ghost" href="'+R+slug+'/'+C.guide+'/">'+S.notready.replace("{p}",p.name)+'</a><button type="button" class="qz-back" id="qz-re">'+S.retake+'</button></div></div>';
 document.getElementById("qz-re").onclick=function(){A={};i=0;render()};
 track("quiz_complete",{program:slug,tier:tier,safety_flag:A.flag,language:C.lang});
}
render();
})();
</script>"""

def build(lang):
    t = L[lang]
    head, foot = shell_parts(lang)
    head = re.sub(r"<title>.*?</title>", f"<title>{t['title']}</title>", head, count=1)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{t["desc"]}">', head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{t["url"]}">', head, count=1)
    en_url, es_url = (t["url"], t["alt"]) if lang == "en" else (t["alt"], t["url"])
    head = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="{en_url}">', head, count=1)
    head = re.sub(r'<link rel="alternate" hreflang="es" href="[^"]*">', f'<link rel="alternate" hreflang="es" href="{es_url}">', head, count=1)
    head = re.sub(r'property="og:title" content="[^"]*"', f'property="og:title" content="{t["title"]}"', head)
    head = re.sub(r'property="og:description" content="[^"]*"', f'property="og:description" content="{t["desc"]}"', head)
    head = re.sub(r'property="og:url" content="[^"]*"', f'property="og:url" content="{t["url"]}"', head)
    # the Spanish quiz sits two folders deep (/es/cuestionario/), so its links back into /es/ need one more ../
    R = "../" if lang == "en" else "../"
    cfg = {"lang": lang, "R": R, "checkout": t["checkout"], "guide": t["guide"], "S": t["S"], "Q": t["Q"],
           "programs": {k: {"slug": v[0], "name": v[1], "desc": v[2], "pay": PAY + v[3], "self": v[4]} for k, v in t["programs"].items()}}
    body = f"""<section class="dark qz-hero"><div class="wrap">
  <div class="eyebrow">{t['eyebrow']}</div>
  <h1>{t['h1']}</h1>
  <p class="sub">{t['sub']}</p>
</div></section>
<div class="qz-wrap"><div class="qz" id="qz" aria-live="polite"></div></div>
<section style="padding-block:40px 64px"><div class="wrap" style="max-width:860px"><p style="font-size:13px;color:var(--grey)">{t['disclaimer']}</p></div></section>
""" + JS.replace("@@CFG@@", json.dumps(cfg, ensure_ascii=False))
    out = ROOT / t["out"]; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head + CSS + body + foot)
    print("wrote", out.relative_to(ROOT))

build("en"); build("es")
