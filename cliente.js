  // Cuestionarios compartidos. Cada respuesta se guarda en el Worker «guzel-datos» (worker/src/index.js), una fila por
  // pregunta, así la ven todas desde cualquier navegador. localStorage queda como copia en el dispositivo: sirve sin
  // conexión, y lo que no se pudo subir (marcado con «s:») se sube cuando vuelve.
  (function () {
    var local = location.hostname === 'localhost' && new URLSearchParams(location.search).get('api');
    var API = local || 'https://guzel-datos.mflowsuite.workers.dev';
    var KEY = 'guzel-ia:';
    function leer(id) { try { return localStorage.getItem(KEY + id) || ''; } catch (e) { return ''; } }
    function guardar(id, v) { try { v ? localStorage.setItem(KEY + id, v) : localStorage.removeItem(KEY + id); } catch (e) {} }
    function esc(t) { return t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

    document.querySelectorAll('[data-form]').forEach(function (form) {
      var id = form.dataset.form, campos = [].slice.call(form.querySelectorAll('textarea'));
      var n = form.querySelector('[data-n]'), ok = form.querySelector('[data-ok]');
      var ultimo = 0, primera = true, relojes = {};
      form.querySelector('[data-t]').textContent = campos.length;
      function contar() { n.textContent = campos.filter(function (c) { var v = c.value.trim(); return v && v !== (c.dataset.esq || '').trim(); }).length; }
      function aviso(txt) { ok.textContent = '· ' + txt; ok.hidden = false; }
      function sucio(c, v) { if (v === undefined) return !!leer('s:' + c.id); guardar('s:' + c.id, v ? '1' : ''); }
      function pendientes() { return campos.filter(function (c) { return sucio(c); }); }

      function subir(c) {
        var v = c.value;
        return fetch(API + '/r/' + id + '/' + c.id, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ v: v }) })
          .then(function (r) { if (!r.ok) throw 0; return r.json(); })
          .then(function () {
            if (c.value === v) sucio(c, false);
            aviso(pendientes().length ? 'Guardando…' : 'Guardado');
          })
          .catch(function () { aviso('Sin conexión: quedó guardado en este dispositivo'); });
      }
      // Trae lo que cambió en el servidor. Lo que esta persona escribió y todavía no subió no se pisa.
      function bajar() {
        return fetch(API + '/r/' + id + '?desde=' + ultimo)
          .then(function (r) { if (!r.ok) throw 0; return r.json(); })
          .then(function (j) {
            var vistos = {};
            j.filas.forEach(function (f) {
              var c = document.getElementById(f.campo);
              if (!c || !form.contains(c)) return;
              vistos[c.id] = 1;
              if (sucio(c)) return;
              if (c.value !== f.valor) { c.value = f.valor; guardar(c.id, f.valor); }
            });
            // Primera carga: lo escrito en este dispositivo que el servidor no tiene (sin conexión, o de antes) se sube.
            if (primera) campos.forEach(function (c) { if (c.value.trim() && !vistos[c.id]) sucio(c, true); });
            primera = false;
            ultimo = Math.max(ultimo, j.t);
            contar();
            pendientes().forEach(subir);
          })
          .catch(function () {});
      }

      campos.forEach(function (c) {
        c.value = leer(c.id);
        c.addEventListener('input', function () {
          guardar(c.id, c.value); sucio(c, true); contar(); aviso('Guardando…');
          clearTimeout(relojes[c.id]); relojes[c.id] = setTimeout(function () { subir(c); }, 1500);
        });
        c.addEventListener('blur', function () { if (sucio(c)) { clearTimeout(relojes[c.id]); subir(c); } });
      });
      contar();
      bajar();
      setInterval(function () { if (document.visibilityState === 'visible') bajar(); }, 20000);
      document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') bajar(); });

      form.querySelectorAll('[data-esq-btn]').forEach(function (b) {
        b.addEventListener('click', function () {
          var c = b.previousElementSibling;
          if (!c.value.trim()) { c.value = c.dataset.esq; c.dispatchEvent(new Event('input')); }
          c.focus();
        });
      });

      // Recorre grupos y preguntas en orden: sirve para el texto a copiar y para el Word.
      function recorrer(fn) {
        form.querySelectorAll('[data-grupo], textarea').forEach(function (el) {
          el.dataset.grupo ? fn('g', el.dataset.grupo) : fn('q', el.dataset.q, el.value.trim());
        });
      }
      form.querySelector('[data-copiar]').addEventListener('click', function (e) {
        var txt = 'GUZEL · ' + form.dataset.titulo + '\n';
        recorrer(function (k, a, b) { txt += k === 'g' ? '\n== ' + a + ' ==\n' : '\n' + a + '\n' + (b || '(sin responder)') + '\n'; });
        var btn = e.currentTarget, fin = function (m) { btn.textContent = m; setTimeout(function () { btn.textContent = 'Copiar todo'; }, 2500); };
        if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { fin('Copiado'); }, function () { fin('No se pudo copiar'); });
        else fin('No se pudo copiar');
      });
      form.querySelector('[data-bajar]').addEventListener('click', function () {
        var h = '<html><head><meta charset="utf-8"><title>Guzel</title></head><body style="font-family:Calibri,Arial,sans-serif">' +
          '<h1>Guzel · ' + esc(form.dataset.titulo) + '</h1>';
        recorrer(function (k, a, b) {
          h += k === 'g' ? '<h2>' + esc(a) + '</h2>' : '<p><b>' + esc(a) + '</b></p><p>' + (b ? esc(b).replace(/\n/g, '<br>') : '&nbsp;<br>&nbsp;') + '</p>';
        });
        var a = document.createElement('a');
        a.href = URL.createObjectURL(new Blob(['﻿' + h + '</body></html>'], { type: 'application/msword' }));
        a.download = form.dataset.archivo; document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      });
    });
  })();
