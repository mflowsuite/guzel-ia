// Respuestas compartidas de los cuestionarios «Guzel y las IA».
// La página es estática (GitHub Pages), así que este Worker es donde se guardan: una fila por pregunta, para que
// Caro, Rita y marketing puedan completar desde cualquier navegador sin pisarse entre preguntas distintas.
//   GET /r/<form>?desde=<t>     → { t, filas: [{ campo, valor, t }] } (solo lo que cambió después de <t>)
//   PUT /r/<form>/<campo> {v}   → { t }
// Es público, como un documento compartido «con el link»: por eso cada cambio queda además en `historial`,
// y nada se pierde si alguien borra o pisa una respuesta.
const ORIGENES = [/^https:\/\/mflowsuite\.github\.io$/, /^http:\/\/localhost:\d+$/];
const FORMS = new Set(["direccion", "marketing"]);
const CAMPO = /^[dm]-[a-z0-9-]{1,40}$/;
const MAX = 6000;

let listo;
const preparar = (db) => (listo ??= db.batch([
  db.prepare("CREATE TABLE IF NOT EXISTS respuestas (form TEXT NOT NULL, campo TEXT NOT NULL, valor TEXT NOT NULL, t INTEGER NOT NULL, PRIMARY KEY (form, campo))"),
  db.prepare("CREATE TABLE IF NOT EXISTS historial (form TEXT NOT NULL, campo TEXT NOT NULL, valor TEXT NOT NULL, t INTEGER NOT NULL)"),
]));

export default {
  async fetch(req, env) {
    const origen = req.headers.get("Origin") || "";
    const permitido = ORIGENES.some((r) => r.test(origen));
    const cors = { Vary: "Origin", ...(permitido ? { "Access-Control-Allow-Origin": origen, "Access-Control-Allow-Methods": "GET, PUT, OPTIONS", "Access-Control-Allow-Headers": "Content-Type", "Access-Control-Max-Age": "86400" } : {}) };
    const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...cors } });
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });

    const url = new URL(req.url);
    const [, raiz, form, campo] = url.pathname.split("/");
    if (raiz === "salud") return json({ ok: true });
    if (raiz !== "r" || !FORMS.has(form)) return json({ error: "no existe" }, 404);
    await preparar(env.DB);

    if (req.method === "GET" && !campo) {
      const desde = Number(url.searchParams.get("desde")) || 0;
      const { results } = await env.DB.prepare("SELECT campo, valor, t FROM respuestas WHERE form = ? AND t > ? ORDER BY t").bind(form, desde).all();
      return json({ t: results.length ? results[results.length - 1].t : desde, filas: results });
    }

    if (req.method === "PUT" && campo) {
      if (!permitido) return json({ error: "origen no permitido" }, 403);
      if (!CAMPO.test(campo)) return json({ error: "campo inválido" }, 400);
      const cuerpo = await req.json().catch(() => null);
      const valor = cuerpo && typeof cuerpo.v === "string" ? cuerpo.v : null;
      if (valor === null || valor.length > MAX) return json({ error: "respuesta inválida o demasiado larga" }, 400);
      const antes = await env.DB.prepare("SELECT valor, t FROM respuestas WHERE form = ? AND campo = ?").bind(form, campo).first();
      if (antes && antes.valor === valor) return json({ t: antes.t });
      const t = Math.max(Date.now(), (antes?.t ?? 0) + 1);
      await env.DB.batch([
        env.DB.prepare("INSERT INTO respuestas (form, campo, valor, t) VALUES (?, ?, ?, ?) ON CONFLICT (form, campo) DO UPDATE SET valor = excluded.valor, t = excluded.t").bind(form, campo, valor, t),
        env.DB.prepare("INSERT INTO historial (form, campo, valor, t) VALUES (?, ?, ?, ?)").bind(form, campo, valor, t),
      ]);
      return json({ t });
    }
    return json({ error: "método no permitido" }, 405);
  },
};
