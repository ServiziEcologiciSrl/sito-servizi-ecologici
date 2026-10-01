/* Servizi Ecologici S.r.l. — script del sito Disinfestazione */
(function () {
  "use strict";

  /* ===== CONFIGURAZIONE =====
     FORM_ENDPOINT: indirizzo che riceve le richieste di preventivo
     (es. Formspree, Getform o il modulo di Italiaonline).
     Se resta vuoto, la richiesta parte via email con il programma di posta del cliente. */
  var CONFIG = {
    FORM_ENDPOINT: "",
    EMAIL: "servizi@serviziecologici.it",
    WHATSAPP: "393295915142"
  };

  /* Menu mobile */
  var btn = document.querySelector(".menu-btn");
  var nav = document.querySelector(".nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var aperto = nav.classList.toggle("aperto");
      btn.setAttribute("aria-expanded", aperto ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { nav.classList.remove("aperto"); });
    });
  }

  /* Anno nel footer */
  document.querySelectorAll("[data-anno]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* Comparsa elementi allo scroll */
  var elementi = document.querySelectorAll(".appare");
  if ("IntersectionObserver" in window) {
    var oss = new IntersectionObserver(function (voci) {
      voci.forEach(function (v) {
        if (v.isIntersecting) { v.target.classList.add("visibile"); oss.unobserve(v.target); }
      });
    }, { threshold: 0.12 });
    elementi.forEach(function (el) { oss.observe(el); });
  } else {
    elementi.forEach(function (el) { el.classList.add("visibile"); });
  }

  /* Link "Richiedi preventivo" con servizio preselezionato: <a data-servizio="Amianto"> */
  document.querySelectorAll("[data-servizio]").forEach(function (a) {
    a.addEventListener("click", function () {
      var radio = document.querySelector('input[name="servizio"][value="' + a.getAttribute("data-servizio") + '"]');
      if (radio) radio.checked = true;
    });
  });

  /* Mese corrente evidenziato nel calendario degli infestanti */
  var mese = new Date().getMonth();
  document.querySelectorAll(".calendario").forEach(function (t) {
    var th = t.querySelector('thead th[data-mese="' + mese + '"]');
    if (th) th.classList.add("oggi");
    t.querySelectorAll("tbody tr").forEach(function (tr) {
      var td = tr.querySelectorAll("td")[mese];
      if (td) td.classList.add("oggi-col");
    });
  });

  /* "Cosa hai notato?": dal segnale all'infestante */
  var risultato = document.getElementById("risultato-segno");
  document.querySelectorAll(".chip-segno").forEach(function (c) {
    c.addEventListener("click", function () {
      document.querySelectorAll(".chip-segno").forEach(function (x) { x.classList.remove("attivo"); });
      c.classList.add("attivo");
      if (!risultato) return;
      var nome = c.getAttribute("data-nome");
      risultato.innerHTML =
        '<span class="prob">Probabilmente si tratta di</span><h3></h3><p></p>' +
        '<div class="azioni"><a class="btn btn-verde btn-piccolo" href="#">Leggi la scheda</a>' +
        '<a class="btn btn-primario btn-piccolo" href="#preventivo">Preventivo gratuito</a></div>';
      risultato.querySelector("h3").textContent = nome;
      risultato.querySelector("p").textContent = c.getAttribute("data-breve");
      risultato.querySelector(".btn-verde").setAttribute("href", c.getAttribute("data-url"));
      risultato.querySelector(".btn-primario").addEventListener("click", function () {
        var radio = Array.prototype.find.call(document.querySelectorAll('input[name="servizio"]'), function (r) {
          return nome.toLowerCase().indexOf(r.value.toLowerCase().split(" ")[0]) === 0;
        });
        if (radio) radio.checked = true;
      });
    });
  });

  /* ===== Modulo preventivo a passi ===== */
  var form = document.getElementById("form-preventivo");
  if (!form) return;

  var passi = form.querySelectorAll(".passo");
  var barre = form.querySelectorAll(".passi span");
  var errore = form.querySelector(".errore");
  var corrente = 0;

  function mostra(n) {
    passi.forEach(function (p, i) { p.classList.toggle("attivo", i === n); });
    barre.forEach(function (b, i) { b.classList.toggle("attivo", i <= n); });
    corrente = n;
    errore.textContent = "";
  }

  function valida(n) {
    var p = passi[n];
    var radio = p.querySelectorAll('input[type="radio"]');
    if (radio.length && !p.querySelector('input[type="radio"]:checked')) {
      return "Seleziona un'opzione per continuare.";
    }
    var richiesti = p.querySelectorAll("[required]");
    for (var i = 0; i < richiesti.length; i++) {
      var c = richiesti[i];
      if (c.type === "checkbox" && !c.checked) return "Per inviare la richiesta serve il consenso al trattamento dei dati.";
      if (c.type !== "checkbox" && !c.value.trim()) return "Compila il campo “" + c.getAttribute("data-nome") + "”.";
    }
    var tel = p.querySelector('input[name="telefono"]');
    if (tel && tel.value.replace(/[^0-9]/g, "").length < 8) return "Controlla il numero di telefono.";
    return "";
  }

  form.addEventListener("click", function (e) {
    var t = e.target.closest("[data-avanti],[data-indietro]");
    if (!t) return;
    e.preventDefault();
    if (t.hasAttribute("data-indietro")) { mostra(Math.max(0, corrente - 1)); return; }
    var msg = valida(corrente);
    if (msg) { errore.textContent = msg; return; }
    mostra(Math.min(passi.length - 1, corrente + 1));
  });

  /* Al click su una scelta si passa da soli al passo successivo */
  form.querySelectorAll('.passo input[type="radio"]').forEach(function (r) {
    r.addEventListener("change", function () {
      setTimeout(function () { if (corrente < passi.length - 1) mostra(corrente + 1); }, 220);
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var msg = valida(corrente);
    if (msg) { errore.textContent = msg; return; }
    if (form.querySelector('input[name="sito_web"]').value) return; /* campo trappola anti-spam */

    var d = new FormData(form);
    var testo =
      "Richiesta di preventivo dal sito\n\n" +
      "Servizio: " + (d.get("servizio") || "") + "\n" +
      "Cliente: " + (d.get("tipo") || "") + "\n" +
      "Nome: " + (d.get("nome") || "") + "\n" +
      "Telefono: " + (d.get("telefono") || "") + "\n" +
      "Email: " + (d.get("email") || "") + "\n" +
      "Comune: " + (d.get("comune") || "") + "\n" +
      "Note: " + (d.get("note") || "");

    function fatto() {
      form.innerHTML =
        '<div class="grazie"><div class="icona-ok">✓</div>' +
        "<h2>Richiesta inviata!</h2>" +
        "<p>Grazie " + escapeHtml(d.get("nome") || "") + ", ti richiamiamo al più presto.</p>" +
        '<p>Hai fretta? <a href="tel:+39019690774"><strong>Chiama lo 019 690774</strong></a></p></div>';
      if (typeof window.gtag === "function") window.gtag("event", "generate_lead", { servizio: d.get("servizio") });
    }

    if (CONFIG.FORM_ENDPOINT) {
      var bottone = form.querySelector('button[type="submit"]');
      bottone.disabled = true; bottone.textContent = "Invio in corso…";
      fetch(CONFIG.FORM_ENDPOINT, { method: "POST", body: d, headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error(); fatto(); })
        .catch(function () {
          bottone.disabled = false; bottone.textContent = "Invia la richiesta";
          errore.textContent = "Invio non riuscito. Chiamaci allo 019 690774 o scrivici su WhatsApp.";
        });
    } else {
      window.location.href = "mailto:" + CONFIG.EMAIL +
        "?subject=" + encodeURIComponent("Richiesta preventivo: " + (d.get("servizio") || "")) +
        "&body=" + encodeURIComponent(testo);
      fatto();
    }
  });

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
})();
