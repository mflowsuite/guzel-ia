  // Cuestionarios compartidos. Cada respuesta se guarda en el Worker «guzel-datos» (worker/src/index.js), una fila por
  // pregunta, así la ven todas desde cualquier navegador. localStorage queda como copia en el dispositivo: sirve sin
  // conexión, y lo que no se pudo subir (marcado con «s:») se sube cuando vuelve.
  (function () {
    // En localhost nunca se escribe en la base real: se usa el Worker local (cf dev) u otro que se pase con ?api=.
    var API = location.hostname === 'localhost' ? new URLSearchParams(location.search).get('api') || 'http://localhost:8787' : 'https://guzel-datos.mflowsuite.workers.dev';
    var KEY = 'guzel-ia:';
    var quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;
    function leer(id) { try { return localStorage.getItem(KEY + id) || ''; } catch (e) { return ''; } }
    function guardar(id, v) { try { v ? localStorage.setItem(KEY + id, v) : localStorage.removeItem(KEY + id); } catch (e) {} }
    function esc(t) { return t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

    // Barra de arriba: acompaña mientras se completa un cuestionario y muestra el avance del que está en pantalla.
    var barra = document.getElementById('barra');
    var bn = barra.querySelector('[data-bn]'), bt = barra.querySelector('[data-bt]'), bok = barra.querySelector('[data-bok]');
    var linea = barra.querySelector('[data-bl]'), bir = barra.querySelector('[data-ir]');
    var estados = {}, activo = null;
    function pintarBarra() {
      var e = estados[activo];
      barra.classList.toggle('on', !!e);
      if (!e) return;
      if (bn.textContent !== String(e.n) && bn.textContent !== '' && !quieto) bn.animate([{ transform: 'scale(1.35)' }, { transform: 'scale(1)' }], { duration: 250, easing: 'cubic-bezier(0.23, 1, 0.32, 1)' });
      bn.textContent = e.n; bt.textContent = e.total;
      bok.textContent = e.aviso; bok.dataset.tipo = e.tipo;
      linea.style.transform = 'scaleX(' + (e.total ? e.n / e.total : 0) + ')';
      barra.classList.toggle('completo', e.n === e.total);
      bir.hidden = e.n === e.total;
      barra.querySelectorAll('[data-tab]').forEach(function (a) { a.classList.toggle('on', a.dataset.tab === activo); });
    }
    bir.addEventListener('click', function () { if (estados[activo]) estados[activo].ir(); });

    document.querySelectorAll('[data-form]').forEach(function (form) {
      var id = form.dataset.form, campos = [].slice.call(form.querySelectorAll('textarea'));
      var n = form.querySelector('[data-n]'), anillo = form.querySelector('[data-anillo]'), msg = form.querySelector('[data-msg]');
      var irBtn = form.querySelector('.fin [data-ir]'), fin = form.querySelector('.fin');
      var ultimo = 0, primera = true, relojes = {};
      var e = estados[id] = { n: 0, total: campos.length, aviso: '', tipo: '', ir: irALaQueFalta };
      form.querySelector('[data-t]').textContent = campos.length;

      function respondida(c) { var v = c.value.trim(); return !!v && v !== (c.dataset.esq || '').trim(); }
      function contar() {
        var antes = e.n;
        campos.forEach(function (c) { c.closest('.q').classList.toggle('hecha', respondida(c)); });
        e.n = campos.filter(respondida).length;
        n.textContent = e.n;
        anillo.style.strokeDashoffset = 100 - (e.total ? (e.n / e.total) * 100 : 0);
        var completo = e.n === e.total;
        fin.classList.toggle('completo', completo);
        irBtn.hidden = completo;
        msg.textContent = completo ? 'Completaste todo. Gracias: con esto armamos la guía.' : 'No hace falta enviar nada: se guarda solo y Martín lo ve a medida que se completa.';
        if (completo && antes < e.total && antes > 0 && !quieto) fin.querySelector('.anillo').animate([{ transform: 'scale(1)' }, { transform: 'scale(1.12)' }, { transform: 'scale(1)' }], { duration: 500, easing: 'cubic-bezier(0.23, 1, 0.32, 1)' });
        pintarBarra();
      }
      function aviso(txt, tipo) { e.aviso = txt; e.tipo = tipo; pintarBarra(); }
      function sucio(c, v) { if (v === undefined) return !!leer('s:' + c.id); guardar('s:' + c.id, v ? '1' : ''); }
      function pendientes() { return campos.filter(function (c) { return sucio(c); }); }
      function irALaQueFalta() {
        var c = campos.filter(function (x) { return !respondida(x); })[0];
        if (!c) return;
        c.closest('.q').scrollIntoView({ behavior: quieto ? 'auto' : 'smooth', block: 'start' });
        c.focus({ preventScroll: true });
      }
      irBtn.addEventListener('click', irALaQueFalta);

      function subir(c) {
        var v = c.value;
        return fetch(API + '/r/' + id + '/' + c.id, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ v: v }) })
          .then(function (r) { if (!r.ok) throw 0; return r.json(); })
          .then(function () {
            if (c.value === v) sucio(c, false);
            pendientes().length ? aviso('Guardando…', 'espera') : aviso('Guardado', 'ok');
          })
          .catch(function () { aviso('Sin conexión', 'mal'); });
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
          guardar(c.id, c.value); sucio(c, true); contar(); aviso('Guardando…', 'espera');
          clearTimeout(relojes[c.id]); relojes[c.id] = setTimeout(function () { subir(c); }, 1500);
        });
        c.addEventListener('blur', function () { if (sucio(c)) { clearTimeout(relojes[c.id]); subir(c); } });
      });
      contar();
      bajar();
      setInterval(function () { if (document.visibilityState === 'visible') bajar(); }, 20000);
      document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') bajar(); });

      // El cuestionario que cruza la mitad de la pantalla es el que muestra la barra.
      new IntersectionObserver(function (es) {
        es.forEach(function (x) { if (x.isIntersecting) activo = id; else if (activo === id) activo = null; });
        pintarBarra();
      }, { rootMargin: '-50% 0px -50% 0px' }).observe(form);

      form.querySelectorAll('[data-esq-btn]').forEach(function (b) {
        b.addEventListener('click', function () {
          var c = b.previousElementSibling;
          if (!c.value.trim()) { c.value = c.dataset.esq; c.dispatchEvent(new Event('input')); }
          c.focus();
        });
      });

      // Copia en Word: recorre grupos y preguntas en orden.
      form.querySelector('[data-bajar]').addEventListener('click', function () {
        var h = '<html><head><meta charset="utf-8"><title>Guzel</title></head><body style="font-family:Calibri,Arial,sans-serif">' +
          '<h1>Guzel · ' + esc(form.dataset.titulo) + '</h1>';
        form.querySelectorAll('[data-grupo], textarea').forEach(function (el) {
          var b = el.value ? el.value.trim() : '';
          h += el.dataset.grupo ? '<h2>' + esc(el.dataset.grupo) + '</h2>' : '<p><b>' + esc(el.dataset.q) + '</b></p><p>' + (b ? esc(b).replace(/\n/g, '<br>') : '&nbsp;<br>&nbsp;') + '</p>';
        });
        var a = document.createElement('a');
        a.href = URL.createObjectURL(new Blob(['﻿' + h + '</body></html>'], { type: 'application/msword' }));
        a.download = form.dataset.archivo; document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      });
    });
  })();
