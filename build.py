# Arma index.html: toma los estilos base y el badge de MflowSuite de la guía de filmación (C:\dev\videos-guzel)
# y genera los dos cuestionarios desde las listas de abajo. Uso: python build.py
import html
import re

BASE = open(r'C:\dev\videos-guzel\index.html', encoding='utf-8').read()
base_css = re.search(r'<style>(.*?)</style>', BASE, re.S).group(1)
badge_html = re.search(r'(<div class="hl-pw-wrap">.*?)</footer>', BASE, re.S).group(1).rstrip()
badge_js = re.search(r'(setTimeout\(function\(\) \{.*?)</script>', BASE, re.S).group(1).rstrip()

SERVICIO = "Dura:\nCada cuánto volver:\nCuidados después:\nNo se recomienda si:"
EJ_SERVICIO = ("Dura: 3 a 4 semanas.\nCada cuánto volver: cada 3 o 4 semanas.\n"
               "Cuidados después: no maquillar ni tomar sol en la zona por 24 horas.\n"
               "No se recomienda si: la piel está irritada o lastimada.")

# (id, pregunta, ayuda, ejemplo, esqueleto)
DIRECCION = [
    ("La historia", "Lo que ya sabemos por la web actual: empezaron en 2015, fueron el primer brow bar de Argentina, «Guzel» significa belleza en turco y las fundadoras son Rita y Carola. Falta esto:", [
        ("d-primer-local", "¿Dónde abrió el primer local y cómo fue creciendo Guzel?", "Con fechas aproximadas alcanza.",
         "El primer local abrió en 2015 en Palermo. En 2018 ya éramos 5 y hoy somos 14, en Capital, Gran Buenos Aires y Tucumán.", ""),
        ("d-idea", "¿Cómo nació la idea?", "Dos o tres líneas, como se lo contarías a una clienta.",
         "Rita conoció el threading viviendo afuera y vio que en Argentina no existía un lugar dedicado solo a las cejas. Con Carola armaron el primer local.", ""),
    ]),
    ("El equipo", "", [
        ("d-equipo", "¿Cuántas profesionales trabajan hoy en Guzel?", "Un número aproximado.",
         "Unas 60 entre las 14 sucursales.", ""),
        ("d-formacion", "¿Cómo se forma una profesional antes de atender?", "Cuánto dura la capacitación y quién la da.",
         "Todas pasan por una capacitación interna de 3 meses, con práctica supervisada, antes de atender a una clienta.", ""),
        ("d-referente", "¿A quién podemos citar como experta de Guzel?", "Nombre, cargo y años de experiencia. Las IA confían más en un texto cuando lo firma una persona.",
         "María Pérez, jefa de capacitación, 9 años haciendo threading.", ""),
    ]),
    ("Cada servicio", "Ya tenemos el nombre, el precio y los minutos de cada uno. Falta lo que solo ustedes saben. En cada casilla podés tocar «Poner la estructura» y completar.", [
        ("d-s-perfilado", "Perfilado de cejas con hilo", "", EJ_SERVICIO, SERVICIO),
        ("d-s-laminado", "Laminado de cejas", "", "", SERVICIO),
        ("d-s-alisado", "Alisado de cejas", "", "", SERVICIO),
        ("d-s-tinte-cejas", "Tinte de cejas", "", "", SERVICIO),
        ("d-s-decoloracion", "Decoloración", "", "", SERVICIO),
        ("d-s-lifting", "Lifting de pestañas", "", "", SERVICIO),
        ("d-s-tinte-pestanas", "Tinte de pestañas", "", "", SERVICIO),
        ("d-s-shock", "Shock de nutrición (cejas y pestañas)", "", "", SERVICIO),
        ("d-s-rostro", "Bozo, mentón y rostro completo con hilo", "", "", SERVICIO),
    ]),
    ("Por qué Guzel", "", [
        ("d-hilo", "¿Por qué hilo y no cera o pinza?", "Las ventajas que le explican a una clienta nueva.",
         "El hilo saca el vello de raíz sin tirar de la piel, así que no irrita ni mancha. Permite definir la forma con más precisión que la cera.", ""),
        ("d-refectocil", "¿Por qué trabajan con RefectoCil?", "",
         "Es la marca profesional que usan los salones de Europa. Los tintes duran más y están probados para la zona de los ojos.", ""),
        ("d-valoran", "¿Qué es lo que más valoran las clientas?", "Lo que más escuchan en el local.",
         "Que no hace falta turno, que en 10 minutos están listas y que el resultado se ve natural.", ""),
        ("d-edad", "¿Atienden a menores y a hombres? ¿Con alguna condición?", "",
         "Atendemos a hombres en todas las sucursales. A menores de 16, con un adulto que acompañe.", ""),
    ]),
    ("Prensa y aclaraciones", "", [
        ("d-prensa", "Notas, premios o menciones de Guzel", "Pegá los links que tengas. Si no hay, dejalo vacío.",
         "Nota en La Nación, 2019: https://…", ""),
        ("d-no-decir", "¿Hay algo que no hay que decir de Guzel, o que la gente suele confundir?", "",
         "No hacemos extensiones de pestañas ni microblading. No somos una depiladora: solo trabajamos el rostro.", ""),
    ]),
]

MARKETING = [
    ("La marca", "", [
        ("m-nombres", "¿Cómo nombra la marca cada servicio? ¿Qué palabras no se usan?", "",
         "Decimos «perfilado con hilo», nunca «depilación de cejas». Decimos «clientas y clientes», no «pacientes».", ""),
        ("m-frase", "¿Cómo describen a Guzel en una frase?", "La que usarían en la biografía de Instagram.",
         "El primer brow bar de Argentina: cejas y pestañas en 10 minutos, sin turno.", ""),
        ("m-tono", "¿Cómo le habla Guzel a su público?", "",
         "De vos, cercano y simple. Sin tecnicismos y sin diminutivos.", ""),
    ]),
    ("Lo que ya existe", "Las IA no leen solo la web: también miran redes, videos y notas. Todo lo que ya esté publicado suma.", [
        ("m-cuentas", "Cuentas oficiales", "Instagram, TikTok, YouTube, Facebook y cualquier otra. Con el link.",
         "Instagram: https://instagram.com/…\nTikTok: https://tiktok.com/@…", ""),
        ("m-videos", "Videos o posteos donde se explique un servicio", "Los que mejor funcionaron. Con el link.",
         "Reel «Qué es el laminado de cejas»: https://…", ""),
        ("m-colaboraciones", "Colaboraciones, influencers o notas donde aparezca Guzel", "",
         "Colaboración con @… en marzo de 2026: https://…", ""),
    ]),
    ("Pruebas", "", [
        ("m-testimonios", "Testimonios o reseñas que se puedan citar", "El texto y el nombre de pila. Tres o cuatro alcanzan.",
         "«Entré sin turno y en 10 minutos salí con las cejas perfectas.» Sofía, Palermo.", ""),
        ("m-fotos", "Fotos de antes y después", "No hace falta subirlas acá: pegá el link a la carpeta donde están.",
         "Carpeta de Drive: https://…", ""),
    ]),
    ("Lo que buscan las clientas", "", [
        ("m-preguntas", "¿Qué preguntan más por Instagram o en los comentarios?", "Ya tenemos las preguntas que le hacen a Sofi. Sumá las que veas vos en redes.",
         "Si duele, cuánto dura el laminado y si pueden ir embarazadas.", ""),
        ("m-zonas", "¿Hay sucursales o servicios que quieran empujar más?", "",
         "Las dos sucursales nuevas y el lifting de pestañas.", ""),
    ]),
]


def esc(t):
    return html.escape(t, quote=True)


def campo(q):
    qid, preg, ayuda, ej, esq = q
    out = [f'<div class="q reveal">', f'<label for="{qid}">{esc(preg)}<span class="tilde" aria-hidden="true"></span></label>']
    if ayuda:
        out.append(f'<p class="hint">{esc(ayuda)}</p>')
    if ej:
        out.append(f'<div class="ej"><span>Ejemplo</span><p>{esc(ej).replace(chr(10), "<br>")}</p></div>')
    filas = 5 if esq else 3
    out.append(f'<textarea id="{qid}" rows="{filas}" data-q="{esc(preg)}"{f" data-esq=\"{esc(esq)}\"" if esq else ""} placeholder="Tu respuesta"></textarea>')
    if esq:
        out.append('<button type="button" class="mini" data-esq-btn>Poner la estructura</button>')
    out.append('</div>')
    return '\n'.join(out)


def cuestionario(fid, titulo, kicker, intro, grupos, archivo):
    out = [f'<section class="form" id="{fid}" data-form="{fid}" data-archivo="{archivo}" data-titulo="{esc(titulo)}">', '<div class="wrap narrow">',
           f'<p class="kicker reveal">{esc(kicker)}</p>', '<div class="rule"></div>', f'<h2 class="reveal">{esc(titulo)}</h2>',
           f'<p class="lead reveal" style="margin-top:18px">{esc(intro)}</p>']
    for nombre, nota, qs in grupos:
        out.append(f'<h3 class="grupo reveal" data-grupo="{esc(nombre)}">{esc(nombre)}</h3>')
        if nota:
            out.append(f'<p class="nota reveal">{esc(nota)}</p>')
        out += [campo(q) for q in qs]
    out.append('''<div class="fin reveal">
  <div class="anillo">
    <svg viewBox="0 0 80 80" aria-hidden="true"><circle class="pista" cx="40" cy="40" r="34"/><circle class="avance" data-anillo cx="40" cy="40" r="34" pathLength="100"/></svg>
    <b data-n>0</b>
  </div>
  <div class="fin-txt">
    <p class="cuenta" aria-live="polite"><span class="sr">Respondidas: </span>de <span data-t>0</span> respondidas</p>
    <p class="hint" data-msg></p>
    <div class="fin-acc">
      <button type="button" class="btn" data-ir>Ir a la que falta ↓</button>
      <button type="button" class="copia" data-bajar>Descargar una copia en Word</button>
    </div>
  </div>
</div>''')
    out.append('</div></section>')
    return '\n'.join(out)


CSS = '''
  /* Página de datos para las IA */
  :root { --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1); }
  [hidden] { display: none !important; }
  .wrap.narrow { width: min(820px, 100% - 32px); }
  .hero.small { min-height: 68svh; }
  .hero.small .content { padding-top: 120px; }
  .hero .poster { object-position: 62% 40%; }
  .marcha { margin-top: 44px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; counter-reset: m; }
  .marcha .card { counter-increment: m; background: #fff; border: 1px solid var(--line); border-radius: 22px; padding: 26px 24px; }
  .marcha .card .st { display: inline-block; padding: 3px 12px; border-radius: 999px; font-size: .72rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; background: var(--teal); color: var(--ink); }
  .marcha .card .st.falta { background: var(--pink); }
  .marcha .card h3 { margin-top: 14px; }
  .marcha .card p { margin-top: 8px; color: var(--ash); }
  .marcha .card .con { margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--line); display: flex; align-items: center; gap: 8px; font-size: .88rem; }
  .marcha .card .con b { color: var(--ink); }
  .como { background: var(--cream); }
  .pasos { margin: 32px 0 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; counter-reset: p; }
  .pasos li { counter-increment: p; background: #fff; border-radius: 20px; padding: 22px; color: var(--ash); }
  .pasos li::before { content: counter(p); display: grid; place-items: center; width: 36px; height: 36px; border-radius: 50%; background: var(--teal-deep); color: #fff; font-weight: 700; margin-bottom: 12px; }
  .pasos b { color: var(--ink); display: block; }
  .quien { margin-top: 32px; display: flex; flex-wrap: wrap; gap: 12px; }
  .form + .form { background: var(--cream); }
  .form .grupo { margin-top: 56px; font-size: 1.6rem; padding-top: 22px; border-top: 1px solid var(--line); }
  .form .nota { margin-top: 10px; color: var(--ash); }
  .q { margin-top: 28px; }
  .q label { display: block; font-weight: 700; font-size: 1.08rem; line-height: 1.35; }
  .hint { margin-top: 4px; color: var(--ash); font-size: .93rem; }
  .ej { margin-top: 12px; padding: 12px 16px; border-left: 4px solid var(--teal); background: #fff; border-radius: 0 12px 12px 0; }
  .form + .form .ej { background: var(--paper); }
  .ej span { font-size: .7rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--teal-deep); }
  .ej p { margin-top: 2px; color: var(--ash); font-style: italic; font-size: .97rem; }
  textarea { display: block; width: 100%; margin-top: 12px; padding: 14px 16px; border-radius: 16px; border: 1px solid #cfc7b8; background: #fff; font: inherit; color: var(--ink); resize: vertical; min-height: 96px; }
  textarea:focus-visible { outline: 3px solid var(--teal); outline-offset: 1px; border-color: var(--teal-deep); }
  .mini { margin-top: 8px; min-height: 40px; padding: 0 16px; border-radius: 999px; border: 1px solid var(--teal-deep); background: transparent; color: var(--teal-deep); font: inherit; font-weight: 700; font-size: .9rem; cursor: pointer; }
  .sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
  .form { scroll-margin-top: 56px; }
  .q { scroll-margin-top: 76px; }
  .tilde { display: inline-block; width: 22px; height: 22px; margin-left: 8px; vertical-align: -4px; border-radius: 50%; background: var(--teal-deep) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23fff' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 12.5l4 4 8-9'/%3E%3C/svg%3E") center / 14px no-repeat; opacity: 0; transform: scale(.6); transition: opacity .2s var(--ease-out), transform .2s var(--ease-out); }
  .q.hecha .tilde { opacity: 1; transform: none; }
  .q.hecha textarea { border-color: var(--teal); }

  .barra { position: fixed; top: 0; left: 0; right: 0; z-index: 50; background: rgba(255,253,249,.94); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); box-shadow: 0 8px 24px -18px rgba(0,0,0,.45); transform: translateY(-110%); transition: transform .25s var(--ease-out); }
  .barra.on { transform: none; }
  .barra-in { width: min(820px, 100% - 24px); margin-inline: auto; height: 52px; display: flex; align-items: center; gap: 12px; }
  .tabs { display: flex; gap: 4px; padding: 3px; border-radius: 999px; background: var(--cream); margin-right: auto; }
  .tabs a { padding: 6px 14px; border-radius: 999px; font-size: .85rem; font-weight: 700; color: var(--ash); text-decoration: none; transition: background-color .2s ease, color .2s ease; }
  .tabs a.on { background: var(--teal-deep); color: #fff; }
  .barra-ok { font-size: .82rem; font-weight: 700; color: var(--teal-deep); white-space: nowrap; display: inline-flex; align-items: center; gap: 6px; }
  .barra-ok::before { content: ''; width: 8px; height: 8px; border-radius: 50%; background: var(--teal); }
  .barra-ok:empty { display: none; }
  .barra-ok[data-tipo="espera"] { color: var(--ash); }
  .barra-ok[data-tipo="espera"]::before { background: var(--butter); }
  .barra-ok[data-tipo="mal"] { color: #a13a2a; }
  .barra-ok[data-tipo="mal"]::before { background: #e0705c; }
  .barra-n { font-size: .9rem; font-weight: 600; white-space: nowrap; }
  .barra-n b { display: inline-block; font-family: var(--display); font-weight: 400; font-size: 1.35rem; color: var(--teal-deep); }
  .barra-ir { min-height: 36px; padding: 0 14px; border-radius: 999px; border: 0; background: var(--pink); color: var(--ink); font: inherit; font-size: .85rem; font-weight: 700; cursor: pointer; white-space: nowrap; }
  .barra-linea { height: 4px; background: var(--line); }
  .barra-linea span { display: block; height: 100%; background: linear-gradient(90deg, var(--teal-deep), var(--teal)); transform: scaleX(0); transform-origin: left; transition: transform .5s var(--ease-in-out); }
  .barra.completo .barra-linea span { background: linear-gradient(90deg, var(--teal-deep), var(--teal), var(--pink)); }

  .fin { margin-top: 64px; padding: 28px; border-radius: 28px; background: #fff; border: 1px solid var(--line); box-shadow: 0 24px 50px -34px rgba(0,0,0,.4); display: grid; grid-template-columns: auto 1fr; gap: 24px; align-items: center; }
  .anillo { position: relative; width: 112px; height: 112px; }
  .anillo svg { width: 100%; height: 100%; transform: rotate(-90deg); }
  .anillo circle { fill: none; stroke-width: 7; }
  .anillo .pista { stroke: var(--cream); }
  .anillo .avance { stroke: var(--teal-deep); stroke-linecap: round; stroke-dasharray: 100; stroke-dashoffset: 100; transition: stroke-dashoffset .6s var(--ease-in-out), stroke .3s ease; }
  .anillo b { position: absolute; inset: 0; display: grid; place-items: center; font-family: var(--display); font-weight: 400; font-size: 2.4rem; color: var(--teal-deep); }
  .fin.completo .anillo .avance { stroke: var(--teal); }
  .fin .cuenta { font-weight: 700; font-size: 1.1rem; }
  .fin-acc { margin-top: 14px; display: flex; flex-wrap: wrap; align-items: center; gap: 6px 18px; }
  .fin-acc .btn { border: 0; font: inherit; font-weight: 700; cursor: pointer; min-height: 44px; }
  .copia { padding: 8px 0; border: 0; background: none; font: inherit; font-size: .9rem; font-weight: 600; color: var(--teal-deep); text-decoration: underline; text-underline-offset: 3px; cursor: pointer; }
  :is(.barra-ir, .copia, .tabs a, .fin-acc .btn):focus-visible { outline: 3px solid var(--teal); outline-offset: 2px; }
  @media (prefers-reduced-motion: reduce) { .barra, .barra-linea span, .tilde, .anillo .avance { transition-duration: .01s; } }
  .aviso { margin-top: 26px; padding: 14px 18px; border-radius: 14px; background: #fff; border: 1px dashed #cfc7b8; color: var(--ash); font-size: .95rem; }
  @media (max-width: 900px) { .marcha, .pasos { grid-template-columns: 1fr; } }
  @media (max-width: 560px) {
    .fin { grid-template-columns: 1fr; justify-items: center; text-align: center; padding: 24px 20px; }
    .fin-acc { justify-content: center; }
    .fin-acc .btn { width: 100%; justify-content: center; }
    .barra-in { gap: 8px; }
    .tabs a { padding: 6px 10px; font-size: .78rem; }
    .barra-ok { font-size: 0; gap: 0; }
    .barra-ir { padding: 0 10px; font-size: .78rem; }
    .quien .btn { width: 100%; justify-content: center; }
  }
'''

JS = open('cliente.js', encoding='utf-8').read()

page = f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guzel · Que las IA recomienden a Guzel</title>
<meta name="description" content="Qué estamos haciendo para que ChatGPT, Gemini y Google recomienden a Guzel, y qué datos necesitamos.">
<meta name="robots" content="noindex">
<meta property="og:title" content="Que las IA recomienden a Guzel">
<meta property="og:description" content="Qué ya está en marcha y qué datos necesitamos de ustedes.">
<meta property="og:image" content="https://mflowsuite.github.io/guzel-ia/img/og.jpg">
<link rel="icon" href="favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Quicksand:wght@400;500;600;700&family=Fira+Sans:wght@600&display=swap" rel="stylesheet">
<style>{base_css}{CSS}</style>
</head>
<body>

<header class="hero small">
  <img class="poster" src="img/resultado-d.webp" alt="">
  <div class="top"><div class="wrap">
    <img class="logo" src="img/logo.png" alt="Guzel" width="120" height="56">
    <span class="tag">Guzel y las IA</span>
  </div></div>
  <div class="content wrap">
    <h1>Que las IA <em>recomienden</em> a Guzel</h1>
    <p>Cada vez más gente le pregunta a ChatGPT o a Gemini dónde hacerse las cejas. Esto es lo que ya está en marcha y lo que necesitamos de ustedes.</p>
    <div class="ctas">
      <a class="btn" href="#direccion">Soy de dirección ↓</a>
      <a class="btn ghost" href="#marketing">Soy de marketing ↓</a>
    </div>
  </div>
</header>

<nav class="barra" id="barra" aria-label="Avance del cuestionario">
  <div class="barra-in">
    <div class="tabs"><a href="#direccion" data-tab="direccion">Dirección</a><a href="#marketing" data-tab="marketing">Marketing</a></div>
    <span class="barra-ok" data-bok aria-hidden="true"></span>
    <p class="barra-n" aria-hidden="true"><b data-bn></b> de <span data-bt>0</span></p>
    <button type="button" class="barra-ir" data-ir aria-label="Ir a la primera pregunta sin responder">Falta <span aria-hidden="true">↓</span></button>
  </div>
  <div class="barra-linea" aria-hidden="true"><span data-bl></span></div>
</nav>

<main>

<section id="marcha">
  <div class="wrap">
    <p class="kicker reveal">Cómo eligen las IA a quién recomendar</p>
    <div class="rule"></div>
    <h2 class="reveal">Cuatro cosas, y tres ya están en marcha</h2>
    <p class="lead reveal" style="margin-top:18px">Una IA recomienda a quien puede leer, a quien tiene buenas reseñas y a quien responde con datos concretos lo que la gente pregunta.</p>
    <div class="marcha">
      <div class="card reveal"><span class="st">En marcha</span><h3>Una web que las IA pueden leer</h3><p>La web nueva tiene cada página también en texto simple, pensado para las IA. Los precios, los horarios y las sucursales se actualizan solos desde el panel, así que siempre leen el dato del día.</p></div>
      <div class="card reveal"><span class="st">En marcha</span><h3>Reseñas en Google de cada sucursal</h3><p>Después de cada visita, el programa de fidelización le pregunta a la clienta cómo le fue y la invita a dejar su reseña. Ya está sumando reseñas en cada sucursal, y lo que salió mal les llega primero a ustedes.</p><p class="con"><img src="img/recompensalo.svg" alt="" width="22" height="22"><span>Con <b>Recompensalo</b>, de MflowSuite</span></p></div>
      <div class="card reveal"><span class="st">En marcha</span><h3>Las preguntas reales de las clientas</h3><p>Sofi responde todos los días por WhatsApp, Instagram y la web. De esas conversaciones sale la lista de lo que la gente de verdad pregunta, sin nombres ni datos personales. La guía responde eso.</p><p class="con"><img src="img/respondelo.svg" alt="" width="22" height="22"><span>Con <b>Respondelo</b>, de MflowSuite</span></p></div>
      <div class="card reveal"><span class="st falta">Falta</span><h3>Lo que solo ustedes saben</h3><p>Cuánto dura un laminado, qué cuidados lleva, cómo se forma una profesional. Con esos datos armamos la guía de cejas y pestañas de Guzel, que es lo que las IA citan cuando alguien pregunta.</p></div>
    </div>
  </div>
</section>

<section class="como" id="como">
  <div class="wrap">
    <p class="kicker reveal">Cómo completar</p>
    <div class="rule"></div>
    <h2 class="reveal">No hace falta hacerlo de una vez</h2>
    <ol class="pasos">
      <li class="reveal"><b>Respondé lo que sepas</b>Cada pregunta trae un ejemplo. Corto y como lo dirías hablando está perfecto.</li>
      <li class="reveal"><b>Se guarda solo, para todas</b>Lo que escribís lo ve cualquiera que abra este link. Podés seguir otro día, desde otro celular o compu, y otra persona puede completar lo que falte.</li>
      <li class="reveal"><b>No hay que mandar nada</b>Martín ve las respuestas a medida que se completan. Si querés una copia, al final la podés descargar en Word.</li>
    </ol>
    <p class="aviso reveal">Los ejemplos son inventados, solo para mostrar cómo responder. No son datos reales de Guzel. Lo que no sepas, dejalo vacío. Si dos personas escriben la misma respuesta a la vez, queda la última.</p>
    <div class="quien reveal">
      <a class="btn" href="#direccion">Preguntas para dirección</a>
      <a class="btn" href="#marketing">Preguntas para marketing</a>
    </div>
  </div>
</section>

{cuestionario("direccion", "Preguntas para dirección", "Para Caro y Rita", "Son datos del negocio que no están en ningún lado y que solo ustedes pueden confirmar.", DIRECCION, "guzel-direccion.doc")}

{cuestionario("marketing", "Preguntas para marketing", "Para quien maneja la marca", "Todo lo que ya tengan publicado o armado sirve. Si hay más material del que entra acá, mejor: mandalo igual.", MARKETING, "guzel-marketing.doc")}

<section class="resumen">
  <div class="wrap">
    <p class="kicker reveal">Además</p>
    <div class="rule"></div>
    <h2 class="reveal">Los videos de la web nueva</h2>
    <p class="lead reveal" style="margin-top:18px;color:rgba(255,255,255,.85)">La guía de filmación explica qué tomas necesitamos, cómo filmarlas y por qué.</p>
    <a class="btn reveal" href="https://mflowsuite.github.io/videos-guzel/">Ver la guía de filmación →</a>
  </div>
</section>

</main>

<footer>
  <p>Guzel y las IA · Datos para la web nueva</p>
{badge_html}
</footer>

<script>
  // Aparición suave de cada bloque al entrar en pantalla.
  var io = new IntersectionObserver(function (es) {{
    es.forEach(function (e) {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }});
  }}, {{ threshold: 0.08 }});
  document.querySelectorAll('.reveal').forEach(function (el) {{ io.observe(el); }});
{JS}
{badge_js}
</script>
</body>
</html>
'''
open('index.html', 'w', encoding='utf-8', newline='\n').write(page)
n = lambda g: sum(len(q) for _, _, q in g)
print(len(page), 'bytes ·', n(DIRECCION), 'preguntas dirección ·', n(MARKETING), 'preguntas marketing')
