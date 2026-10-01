#!/usr/bin/env python3
"""Genera il sito Disinfestazione e Derattizzazione di Servizi Ecologici nella cartella ../sito-disinfestazione.

Uso:  python3 strumenti/genera_sito_disinfestazione.py
I testi stanno in dati_disinfestazione.py: si modificano lì e si rilancia questo script.
"""
import html
import json
import os

from dati_disinfestazione import (DATI, FAQ_HOME, GUIDA, INFESTANTI, LEGGI, PACCHETTI_MULTI, PIANI, SEGNI, SERVIZI,
                                  SETTORI, ZONE)

QUI = os.path.dirname(os.path.abspath(__file__))
SITO = os.path.join(QUI, "..", "sito-disinfestazione")
MESI = ["G", "F", "M", "A", "M", "G", "L", "A", "S", "O", "N", "D"]
MESI_LUNGHI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]

# ---------------------------------------------------------------- icone (24x24, tratto)
ICONE = {
    "topo": '<path d="M2 16c0-4 4-7.5 9-7.5 4.5 0 7.5 2.5 8.5 5.5l2.5 1-2.5 1.2C18.5 18 15.5 19 11 19H5"/><circle cx="16.5" cy="12.5" r=".9"/><path d="M13.5 9a2.7 2.7 0 1 1 4-2.4"/><path d="M2 16c-.5 2 .5 3.5 3 3"/>',
    "blatta": '<ellipse cx="12" cy="13.5" rx="4.5" ry="6.5"/><path d="M12 7V3M10 4L7.5 1.5M14 4l2.5-2.5M7.5 10.5H3M21 10.5h-4.5M7.5 14.5l-4 1.5M16.5 14.5l4 1.5M8.5 18.5l-3 3M15.5 18.5l3 3M12 9v11"/>',
    "formica": '<circle cx="12" cy="4.5" r="2"/><ellipse cx="12" cy="10" rx="1.8" ry="2.3"/><ellipse cx="12" cy="17.5" rx="3" ry="4"/><path d="M10.3 9.5L5 7.5M13.7 9.5l5.3-2M10.3 11L5 13M13.7 11l5.3 2M9.5 15l-4 4.5M14.5 15l4 4.5M11 2.8L9.5 1M13 2.8L14.5 1"/>',
    "zanzara": '<circle cx="12" cy="6" r="1.8"/><path d="M12 8v11M11 4.8L7 1.5"/><path d="M12 10C9 6 4 6 3 8s4 4 9 4M12 10c3-4 8-4 9-2s-4 4-9 4"/><path d="M11 13.5l-5 7M13 13.5l5 7M11 16.5l-6.5 1M13 16.5l6.5 1"/>',
    "vespa": '<ellipse cx="12" cy="15" rx="3.5" ry="5.5"/><circle cx="12" cy="6.5" r="2"/><path d="M8.6 13h6.8M8.6 16.5h6.8M12 20.5V23"/><path d="M10.5 9c-3-3-7-3-7-1s3 3 6 3M13.5 9c3-3 7-3 7-1s-3 3-6 3"/>',
    "cimice": '<path d="M12 5c4 0 7 3.5 7 8.5S16 21 12 21s-7-2.5-7-7.5S8 5 12 5z"/><path d="M9.5 5.5C9.5 3.8 10.5 3 12 3s2.5.8 2.5 2.5M12 9v12M6 10H3M18 10h3M5.2 15H2M18.8 15H22M7 19l-2 2M17 19l2 2"/>',
    "zecca": '<circle cx="12" cy="6.5" r="2"/><ellipse cx="12" cy="15" rx="5" ry="6"/><path d="M7.5 12L3 9M16.5 12L21 9M7 15H2M17 15h5M7.5 18L4 21M16.5 18l3.5 3"/>',
    "mosca": '<ellipse cx="12" cy="14.5" rx="3" ry="5"/><circle cx="12" cy="7.5" r="2.2"/><path d="M10 11C6 7 2 9 3 12s5 2 7 1M14 11c4-4 8-2 7 1s-5 2-7 1M10.5 18.5l-2.5 3M13.5 18.5l2.5 3"/>',
    "uccello": '<path d="M3 13c2 0 3-1 4-3 1-3 3-5 6-5 2 0 3 1 3.5 3H20l-3 2c0 5-4 9-10 9H4l3-3"/><circle cx="14" cy="7.5" r=".8"/><path d="M8 14c2 1 5 0 7-2"/>',
    "bruco": '<circle cx="5" cy="15.5" r="2.5"/><circle cx="9.5" cy="14.5" r="2.5"/><circle cx="14" cy="14.5" r="2.5"/><circle cx="18.5" cy="15.5" r="2.5"/><path d="M5 13v-2.5M9.5 12V9.5M14 12V9.5M18.5 13v-2.5M3.5 13.5L2 11"/>',
    "barattolo": '<path d="M7 3h10M8 3v3L6 9v11a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V9l-2-3V3"/><path d="M12 14l-3-2v4zM12 14l3-2v4z"/>',
    "pesciolino": '<path d="M4 12c3-4 9-5 13-3l3-2-1 5 1 5-3-2c-4 2-10 1-13-3z"/><path d="M4 12l-2-2M4 12l-2 2M9 10v4M12 9.5v5"/>',
    "erogatore": '<rect x="3" y="10" width="18" height="9" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/><circle cx="12" cy="14.5" r="1.5"/>',
    "spruzzino": '<path d="M8 9h7v12H8z"/><path d="M9.5 9V6h4v3M13.5 6H17M19.5 4v.01M19.5 7v.01M21.5 5.5v.01"/>',
    "scudo": '<path d="M12 22c4-2 8-6 8-12V5l-8-3-8 3v5c0 6 4 10 8 12z"/><path d="M8.5 12l2.5 2.5L16 9.5"/>',
    "registro": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 3v2h6V3M9 12l2 2 4-4M9 17h6"/>',
    "casa": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
    "palazzo": '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M11 21v-3h2v3"/>',
    "posate": '<path d="M7 2v9M4.5 2v5a2.5 2.5 0 0 0 5 0V2M7 11v11"/><path d="M17 22V2c-2.5 1.5-3.5 4-3.5 8h3.5"/>',
    "fabbrica": '<path d="M2 21V10l6 4V10l6 4V6h4l1 15z"/><path d="M6 17h2M11 17h2M16 17h2"/>',
    "letto": '<path d="M2 18V6M2 14h20v4M22 18v-5a3 3 0 0 0-3-3h-8v4"/><circle cx="6.5" cy="11" r="2"/>',
    "croce": '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M12 8v8M8 12h8"/>',
    "negozio": '<path d="M3 9l1.5-5h15L21 9"/><path d="M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M5 11v10h14V11M10 21v-5h4v5"/>',
    "barca": '<path d="M3 17l2 4h14l2-4z"/><path d="M12 3v14"/><path d="M12 4l7 10H12"/>',
    "tazza": '<path d="M4 8h12v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M16 9h2a2.5 2.5 0 0 1 0 5h-2M8 2c0 2 2 2 2 4M12 2c0 2 2 2 2 4M3 22h14"/>',
    "ombrellone": '<path d="M12 3a9 9 0 0 1 9 9H3a9 9 0 0 1 9-9z"/><path d="M12 12v8M8 21h8M12 3v9"/>',
    "telefono": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "documento": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "orologio": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "euro": '<path d="M18 7a7 7 0 1 0 0 10"/><path d="M4 10h10M4 14h10"/>',
    "persone": '<circle cx="9" cy="8" r="3.5"/><path d="M2 21c0-4 3-6.5 7-6.5s7 2.5 7 6.5"/><path d="M16 4a3.5 3.5 0 0 1 0 7M22 21c0-3-1.5-5.2-4-6"/>',
    "foglia": '<path d="M5 19c0-9 6-15 15-15 0 9-6 15-15 15z"/><path d="M5 19l8-8"/>',
    "lente": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',
    "legge": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
    "pacco": '<path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
}
WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8.2 8.2 0 0 1-4.1-3.6c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.8.4 3.5 3.5 0 0 0-1.1 2.6 6 6 0 0 0 1.3 3.2 13.8 13.8 0 0 0 5.3 4.7c2 .8 2.7.9 3.7.8a3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.2-.3-.3-.6-.4z"/>'
          '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>')
LOGO_SVG = ('<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#1d5fbf"/>'
            '<path d="M24 9l12 4.5v8.5c0 8-5.2 14.2-12 17-6.8-2.8-12-9-12-17v-8.5z" fill="#4fb3ff"/>'
            '<path d="M18.5 23.5l4 4 7.5-8" stroke="#0b3a7e" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def icona(nome):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{ICONE[nome]}</svg>')


def esc(s):
    return html.escape(s, quote=True)


def wa_link(testo="Buongiorno, vorrei un preventivo per una disinfestazione: "):
    from urllib.parse import quote
    return f"https://wa.me/{DATI['whatsapp']}?text=" + quote(testo)


def per_slug(lista, slug):
    return next(x for x in lista if x["slug"] == slug)


# ---------------------------------------------------------------- blocchi comuni
def testa(titolo, desc, percorso, base, schema):
    url = DATI["dominio"] + "/" + percorso
    inf = "".join(f'<a href="{base}infestanti/{i["slug"]}.html">{icona(i["icona"])}{esc(i["nome"])}</a>' for i in INFESTANTI)
    sett = "".join(f'<a href="{base}settori/{s["slug"]}.html">{icona(s["icona"])}{esc(s["nome"])}</a>' for s in SETTORI)
    serv = "".join(f'<a href="{base}servizi/{s["slug"]}.html">{icona(s["icona"])}{esc(s["nome"])}</a>' for s in SERVIZI)
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titolo)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#1d5fbf">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Servizi Ecologici – Disinfestazione">
<meta property="og:title" content="{esc(titolo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
<a class="sr-only" href="#contenuto">Vai al contenuto</a>
<div class="topbar"><div class="wrap">
  <span><span class="pulse"></span>Preventivo gratuito · Nidi di vespe e calabroni: interventi prioritari</span>
  <span class="solo-desktop">Chiamaci: <a href="tel:{DATI['tel_link']}">{DATI['tel']}</a> · <a href="mailto:{DATI['email']}">{DATI['email']}</a></span>
</div></div>
<header class="header"><div class="wrap">
  <a class="logo" href="{base}index.html" aria-label="Servizi Ecologici Disinfestazione – home">{LOGO_SVG}<span>Servizi Ecologici<small>{DATI['sottotitolo']}</small></span></a>
  <nav class="nav" aria-label="Menu principale">
    <div class="voce-menu"><a href="{base}index.html#infestanti">Infestanti</a><div class="sottomenu griglia-3">{inf}</div></div>
    <div class="voce-menu"><a href="{base}index.html#servizi">Servizi</a><div class="sottomenu">{serv}</div></div>
    <div class="voce-menu"><a href="{base}index.html#settori">Settori</a><div class="sottomenu">{sett}</div></div>
    <a href="{base}pacchetti.html">Pacchetti</a>
    <a href="{base}consigli-prevenzione.html">Consigli</a>
    <a href="{base}index.html#domande">Domande</a>
  </nav>
  <div class="header-cta">
    <a class="btn btn-bordo btn-piccolo" href="tel:{DATI['tel_link']}">{icona('telefono')}{DATI['tel']}</a>
    <a class="btn btn-primario btn-piccolo" href="#preventivo">Preventivo gratis</a>
    <button class="menu-btn" aria-label="Apri il menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</div></header>
<main id="contenuto">
"""


def piede(base):
    inf = "".join(f'<li><a href="{base}infestanti/{i["slug"]}.html">{esc(i["nome"])}</a></li>' for i in INFESTANTI)
    serv = "".join(f'<li><a href="{base}servizi/{s["slug"]}.html">{esc(s["nome"])}</a></li>' for s in SERVIZI)
    sett = "".join(f'<li><a href="{base}settori/{s["slug"]}.html">{esc(s["nome"])}</a></li>' for s in SETTORI)
    wa = wa_link()
    return f"""</main>
<footer class="footer"><div class="wrap footer-5">
  <div>
    <a class="logo" href="{base}index.html">{LOGO_SVG}<span>Servizi Ecologici S.r.l.<small>{DATI['sottotitolo']}</small></span></a>
    <p>Disinfestazione, derattizzazione, allontanamento volatili e sanificazione in Liguria e nel basso Piemonte. Servizi per l'ambiente dal 1975.</p>
    <ul>
      <li><a href="tel:{DATI['tel_link']}">Tel. {DATI['tel']}</a></li>
      <li><a href="{wa}">WhatsApp {DATI['cell']}</a></li>
      <li><a href="mailto:{DATI['email']}">{DATI['email']}</a></li>
      <li>{DATI['sede_op']}</li>
    </ul>
  </div>
  <div><h4>Infestanti</h4><ul>{inf}</ul></div>
  <div><h4>Servizi</h4><ul>{serv}<li><a href="{base}pacchetti.html">Pacchetti multiservizio</a></li><li><a href="{base}consigli-prevenzione.html">Guida alla prevenzione</a></li></ul></div>
  <div><h4>Settori</h4><ul>{sett}</ul></div>
  <div><h4>Anche per te</h4><ul>
    <li><a href="{DATI['sito_principale']}/">Tutti i servizi di Servizi Ecologici</a></li>
    <li>Rifiuti e cassoni scarrabili</li><li>Rimozione amianto</li><li>Spurghi e fosse biologiche</li><li>Canne fumarie e cappe</li><li>Analisi ambientali e acque</li>
  </ul></div>
  <div class="legale">
    <span>© <span data-anno>2026</span> {DATI['nome']} · Sede legale {DATI['sede_legale']} · P. IVA {DATI['piva']} · Albo Gestori Ambientali n. {DATI['albo']}</span>
    <span><a href="{base}privacy.html">Privacy e cookie</a></span>
  </div>
</div></footer>
<a class="wa-flottante" href="{wa}" aria-label="Scrivici su WhatsApp" target="_blank" rel="noopener">{WA_SVG}</a>
<nav class="barra-mobile" aria-label="Contatti rapidi">
  <a class="chiama" href="tel:{DATI['tel_link']}">{icona('telefono')}Chiama</a>
  <a class="wa" href="{wa}" target="_blank" rel="noopener">{WA_SVG}Foto su WhatsApp</a>
  <a class="prev" href="#preventivo">{icona('documento')}Preventivo</a>
</nav>
<script src="{base}assets/main.js" defer></script>
</body>
</html>
"""


SCELTE_FORM = [("Topi e ratti", "topo"), ("Blatte", "blatta"), ("Formiche", "formica"), ("Zanzare", "zanzara"),
               ("Vespe e calabroni", "vespa"), ("Cimici dei letti", "cimice"), ("Piccioni e gabbiani", "uccello"),
               ("Pulci e zecche", "zecca"), ("Processionaria", "bruco"), ("Sanificazione", "scudo"),
               ("Contratto HACCP", "registro"), ("Pacchetto multiservizio", "pacco")]


def modulo(base, preselezionato=None):
    valori = [v for v, _ in SCELTE_FORM]
    if preselezionato and preselezionato not in valori:
        preselezionato = None
    scelte = "".join(
        f'<div class="scelta"><input type="radio" name="servizio" id="s{i}" value="{esc(v)}"{" checked" if v == preselezionato else ""}>'
        f'<label for="s{i}">{icona(ic)}{esc(v)}</label></div>' for i, (v, ic) in enumerate(SCELTE_FORM))
    scelte += '<div class="scelta"><input type="radio" name="servizio" id="s-altro" value="Altro / non so cos\'è"><label for="s-altro">Altro / non so cos\'è</label></div>'
    tipi = ["Privato", "Condominio", "Ristorante / bar", "Hotel / B&B", "Azienda / industria", "Ente o scuola"]
    tipi_html = "".join(f'<div class="scelta"><input type="radio" name="tipo" id="t{i}" value="{t}"><label for="t{i}">{t}</label></div>' for i, t in enumerate(tipi))
    primo = 1 if preselezionato else 0
    barre = "".join(f'<span{" class=" + chr(34) + "attivo" + chr(34) if i <= primo else ""}></span>' for i in range(3))
    return f"""<div class="card-form" id="preventivo">
  <h2>Preventivo gratuito</h2>
  <p class="nota">3 domande, 1 minuto. Ti richiamiamo noi.</p>
  <form id="form-preventivo" novalidate>
    <div class="passi" aria-hidden="true">{barre}</div>
    <fieldset class="passo{' attivo' if primo == 0 else ''}" style="border:0;padding:0;margin:0">
      <legend class="campo" style="font-weight:700;margin-bottom:10px">Che problema hai?</legend>
      <div class="scelte">{scelte}</div>
    </fieldset>
    <fieldset class="passo{' attivo' if primo == 1 else ''}" style="border:0;padding:0;margin:0">
      <legend class="campo" style="font-weight:700;margin-bottom:10px">Dove si trova il problema?</legend>
      <div class="scelte">{tipi_html}</div>
      <div class="azioni-form"><button class="btn btn-bordo" data-indietro>Indietro</button></div>
    </fieldset>
    <fieldset class="passo" style="border:0;padding:0;margin:0">
      <legend class="campo" style="font-weight:700;margin-bottom:10px">Dove ti richiamiamo?</legend>
      <div class="campo"><label for="f-nome">Nome e cognome *</label><input id="f-nome" name="nome" autocomplete="name" required data-nome="Nome e cognome"></div>
      <div class="campo"><label for="f-tel">Telefono *</label><input id="f-tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel" required data-nome="Telefono"></div>
      <div class="campo"><label for="f-comune">Comune dell'intervento *</label><input id="f-comune" name="comune" autocomplete="address-level2" required data-nome="Comune"></div>
      <div class="campo"><label for="f-email">Email (facoltativa)</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
      <div class="campo"><label for="f-note">Cosa hai notato? (facoltativo)</label><textarea id="f-note" name="note" placeholder="Es. escrementi in cantina, nido di vespe nella tapparella del 2° piano…"></textarea></div>
      <input type="text" name="sito_web" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
      <label class="consenso"><input type="checkbox" name="privacy" required data-nome="Privacy"> <span>Acconsento al trattamento dei miei dati per ricevere il preventivo, come indicato nell'<a href="{base}privacy.html" target="_blank">informativa privacy</a>.</span></label>
      <div class="azioni-form"><button class="btn btn-bordo" data-indietro>Indietro</button><button class="btn btn-primario" type="submit">Invia la richiesta</button></div>
    </fieldset>
    <p class="errore" role="alert"></p>
  </form>
  <p class="form-sicuro">🔒 Gratis e senza impegno · Hai una foto? <a href="{wa_link()}" target="_blank" rel="noopener">Mandala su WhatsApp</a></p>
</div>"""


def faq_html(voci):
    return '<div class="faq">' + "".join(f"<details><summary>{esc(d)}</summary><p>{esc(r)}</p></details>" for d, r in voci) + "</div>"


def schema_azienda():
    return {
        "@type": "LocalBusiness", "@id": DATI["dominio"] + "/#azienda", "name": DATI["nome"] + " – Disinfestazione e derattizzazione",
        "url": DATI["dominio"] + "/", "telephone": "+39 019 690774", "email": DATI["email"], "foundingDate": "1975",
        "vatID": "IT" + DATI["piva"],
        "address": {"@type": "PostalAddress", "streetAddress": "Via Fiume 3", "addressLocality": "Finale Ligure",
                    "postalCode": "17024", "addressRegion": "SV", "addressCountry": "IT"},
        "areaServed": ["Provincia di Savona", "Provincia di Imperia", "Città metropolitana di Genova", "Provincia della Spezia", "Piemonte"],
        "priceRange": "€€",
    }


def schema_faq(voci):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": d, "acceptedAnswer": {"@type": "Answer", "text": r}} for d, r in voci]}


def briciole_schema(voci):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DATI["dominio"] + "/" + u} for i, (n, u) in enumerate(voci)]}


def cta_finale(base, titolo="Hai notato qualcosa di strano? Non aspettare che peggiori."):
    return f"""<section><div class="wrap"><div class="cta-finale appare">
  <h2>{esc(titolo)}</h2>
  <p>Più si aspetta, più l'infestazione cresce. Raccontaci cosa hai visto: ti richiamiamo e ti diamo un preventivo gratuito.</p>
  <div class="hero-cta">
    <a class="btn btn-primario btn-grande" href="#preventivo">Richiedi il preventivo gratuito</a>
    <a class="btn btn-bianco btn-grande" href="tel:{DATI['tel_link']}">{icona('telefono')}Chiama {DATI['tel']}</a>
  </div>
</div></div></section>"""


def card_infestante(i, base):
    return (f'<a class="card-inf appare" href="{base}infestanti/{i["slug"]}.html"><span class="ico-inf">{icona(i["icona"])}</span>'
            f'<strong>{esc(i["nome"])}</strong><span>{esc(i["breve"])}</span></a>')


def card_generica(x, base, cartella, testo_vai="Scopri di più"):
    return (f'<a class="servizio appare" href="{base}{cartella}/{x["slug"]}.html"><div class="icona">{icona(x["icona"])}</div>'
            f'<h3>{esc(x["nome"])}</h3><p>{esc(x["breve"])}</p><span class="vai">{testo_vai}</span></a>')


def calendario(base):
    righe = ""
    for i in INFESTANTI:
        celle = "".join(f'<td class="l{v}" title="{esc(i["nome"])} – {MESI_LUNGHI[m]}"><span class="sr-only">{["assente", "bassa", "media", "alta"][v]}</span></td>'
                        for m, v in enumerate(i["mesi"]))
        righe += f'<tr><th scope="row"><a href="{base}infestanti/{i["slug"]}.html">{esc(i["nome"])}</a></th>{celle}</tr>'
    testa_mesi = "".join(f'<th scope="col" data-mese="{m}">{l}</th>' for m, l in enumerate(MESI))
    return f"""<div class="tabella-scroll appare"><table class="calendario" id="calendario">
<thead><tr><th scope="col">Infestante</th>{testa_mesi}</tr></thead><tbody>{righe}</tbody></table></div>
<div class="legenda"><span><i class="l1"></i>presenza bassa</span><span><i class="l2"></i>media</span><span><i class="l3"></i>picco</span><span><i class="oggi"></i>mese corrente</span></div>"""


def identificatore(base):
    chip = "".join(
        f'<button type="button" class="chip-segno" data-slug="{slug}" data-nome="{esc(per_slug(INFESTANTI, slug)["nome"])}" '
        f'data-url="{base}infestanti/{slug}.html" data-breve="{esc(per_slug(INFESTANTI, slug)["breve"])}">{esc(t)}</button>'
        for t, slug in SEGNI)
    return f"""<div class="identifica appare">
  <div class="chips">{chip}</div>
  <div class="risultato" id="risultato-segno" aria-live="polite">
    <p class="vuoto">👆 Tocca quello che hai notato: ti diciamo di cosa si tratta probabilmente.</p>
  </div>
</div>"""


def legge_html(chiave):
    nome, testo = LEGGI[chiave]
    return f'<li><strong>{esc(nome)}</strong><span>{esc(testo)}</span></li>'


def card_pacchetto_multi(p, base, completo=False):
    servizi = "".join(f"<li>{esc(s)}</li>" for s in p["servizi"])
    leggi = "".join(f'<span class="tag-legge" title="{esc(LEGGI[k][1])}">{esc(LEGGI[k][0])}</span>' for k in p["leggi"])
    extra = ""
    if completo:
        extra = (f'<details class="dettagli-leggi"><summary>Cosa dicono le leggi</summary><ul class="lista-leggi">{"".join(legge_html(k) for k in p["leggi"])}</ul></details>'
                 f'<div class="problema"><strong>Cosa ricevi:</strong> {esc(p["ricevi"])}</div>')
    return f"""<div class="pacchetto multi appare{' evidenza' if p['evidenza'] else ''}" id="{p['slug']}">
  {'<span class="nastro">Il più richiesto</span>' if p['evidenza'] else ''}
  <div class="testa-pacchetto"><div class="icona">{icona(p['icona'])}</div><div><h3>{esc(p['nome'])}</h3><span class="per">{esc(p['per'])}</span></div></div>
  <ul>{servizi}</ul>
  <div class="leggi-tag">{icona('legge')}<div>{leggi}</div></div>
  {extra}
  <p class="perche">{esc(p['perche'])}</p>
  <a class="btn {'btn-primario' if p['evidenza'] else 'btn-verde'}" href="#preventivo" data-servizio="Pacchetto multiservizio">Chiedi il pacchetto</a>
</div>"""


# ---------------------------------------------------------------- pagine
def home():
    base = ""
    infest = "".join(card_infestante(i, base) for i in INFESTANTI)
    servizi = "".join(card_generica(s, base, "servizi") for s in SERVIZI)
    settori = "".join(card_generica(s, base, "settori", "Soluzioni per te") for s in SETTORI)
    piani = "".join(
        f'<div class="pacchetto appare{" evidenza" if p["evidenza"] else ""}">{"<span class=" + chr(34) + "nastro" + chr(34) + ">Il più scelto</span>" if p["evidenza"] else ""}'
        f'<span class="per">{esc(p["per"])}</span><h3>{esc(p["nome"])}</h3><ul>{"".join("<li>" + esc(v) + "</li>" for v in p["voci"])}</ul>'
        f'<div class="problema">{esc(p["nota"])}</div><a class="btn {"btn-primario" if p["evidenza"] else "btn-verde"}" href="#preventivo">Chiedi un preventivo</a></div>'
        for p in PIANI)
    multi = "".join(card_pacchetto_multi(p, base) for p in PACCHETTI_MULTI[:3])
    zone = "".join(f'<span{" class=" + chr(34) + "principale" + chr(34) if z == "Finale Ligure" else ""}>{z}</span>' for z in ZONE)
    schema = {"@context": "https://schema.org", "@graph": [schema_azienda(), schema_faq(FAQ_HOME)]}
    corpo = f"""
<section class="hero hero-pest"><div class="wrap">
  <div>
    <span class="etichetta">🛡️ Pest control professionale in Liguria · dal 1975</span>
    <h1>Topi, insetti, vespe e piccioni? <em>Li allontaniamo noi</em>, in sicurezza.</h1>
    <p class="sotto">Disinfestazione e derattizzazione per case, condomini, ristoranti, hotel e aziende. Prodotti autorizzati, metodi sicuri per bambini e animali, documenti pronti per l'ASL.</p>
    <div class="hero-cta">
      <a class="btn btn-primario btn-grande" href="#preventivo">Preventivo gratuito in 1 minuto</a>
      <a class="btn btn-bordo btn-grande" href="tel:{DATI['tel_link']}">{icona('telefono')}{DATI['tel']}</a>
    </div>
    <ul class="spunte">
      <li>Sopralluogo gratuito</li>
      <li>Prodotti autorizzati</li>
      <li>Sicuro per bambini e animali</li>
      <li>Documenti HACCP</li>
    </ul>
    <div class="hero-infestanti" aria-hidden="true">{''.join(f'<span title="{esc(i["nome"])}">{icona(i["icona"])}</span>' for i in INFESTANTI[:8])}</div>
  </div>
  {modulo(base)}
</div></section>

<div class="fiducia"><div class="wrap">
  <div><strong>50+</strong><span>anni di servizi per l'ambiente</span></div>
  <div><strong>12</strong><span>infestanti che trattiamo ogni giorno</span></div>
  <div><strong>4</strong><span>province liguri + basso Piemonte</span></div>
  <div><strong>0 €</strong><span>per preventivo e sopralluogo</span></div>
</div></div>

<section id="infestanti"><div class="wrap">
  <div class="intestazione appare">
    <span class="sopratitolo">Che infestante hai?</span>
    <h2>Scegli il problema, ti spieghiamo come risolverlo</h2>
    <p>Per ogni infestante trovi come riconoscerlo, i rischi, come interveniamo e cosa puoi fare tu per prevenirlo.</p>
  </div>
  <div class="griglia-inf">{infest}</div>
</div></section>

<section class="fascia-urgenza"><div class="wrap">
  <div class="urgenza-testo">
    <span class="ico-urg">{icona('vespa')}</span>
    <div><h2>Nido di vespe o calabroni? Topo in casa?</h2><p>Non toccare nulla e non usare veleni a caso. Mandaci una foto su WhatsApp: ti diciamo subito cos'è e quando possiamo intervenire.</p></div>
  </div>
  <div class="urgenza-cta">
    <a class="btn btn-whatsapp btn-grande" href="{wa_link('Buongiorno, vi mando la foto di un problema di infestanti: ')}" target="_blank" rel="noopener">{WA_SVG}Invia una foto</a>
    <a class="btn btn-bianco btn-grande" href="tel:{DATI['tel_link']}">{icona('telefono')}{DATI['tel']}</a>
  </div>
</div></section>

<section id="casa-azienda"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Per chi lavoriamo</span><h2>Soluzioni diverse per la casa e per l'azienda</h2></div>
  <div class="split">
    <div class="split-card appare">
      <div class="icona">{icona('casa')}</div>
      <h3>Per la tua casa</h3>
      <p>Un problema preciso da risolvere in fretta e bene, con prodotti sicuri per la famiglia.</p>
      <ul class="spunte-col"><li>Topi in cantina o in soffitta</li><li>Blatte e formiche in cucina</li><li>Nidi di vespe e calabroni</li><li>Zanzare in giardino</li><li>Cimici dei letti e pulci</li></ul>
      <a class="btn btn-verde" href="settori/casa-privati.html">Soluzioni per la casa</a>
    </div>
    <div class="split-card scura appare">
      <div class="icona">{icona('fabbrica')}</div>
      <h3>Per la tua attività</h3>
      <p>Controllo continuo, documenti per l'ASL e per gli audit, interventi che non fermano il lavoro.</p>
      <ul class="spunte-col"><li>Piano HACCP con planimetria e report</li><li>Controlli fuori orario</li><li>Lampade cattura-insetti</li><li>Contratti per condomini</li><li>Pacchetti con cappe, canne fumarie e analisi acque</li></ul>
      <a class="btn btn-primario" href="settori/ristoranti-bar.html">Soluzioni per le aziende</a>
    </div>
  </div>
</div></section>

<section id="servizi" class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">I nostri servizi</span><h2>Tutto il pest control, da un'unica azienda</h2>
  <p>Personale formato, mezzi nostri e prodotti autorizzati per l'uso professionale.</p></div>
  <div class="griglia-servizi griglia-4">{servizi}
    <a class="servizio appare servizio-evidenza" href="pacchetti.html"><div class="icona">{icona('pacco')}</div><h3>Pacchetti multiservizio</h3>
    <p>Disinfestazione + pulizia cappe + canne fumarie + analisi acque + spurghi, in un unico contratto per hotel, pizzerie, condomini e aziende.</p><span class="vai">Vedi i pacchetti</span></a>
  </div>
</div></section>

<section id="identifica"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Riconosci i segnali</span><h2>Cosa hai notato?</h2>
  <p>Molte infestazioni si scoprono da piccoli segni. Tocca quello che hai visto e scopri di cosa si tratta.</p></div>
  {identificatore(base)}
</div></section>

<section id="settori" class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Settori</span><h2>Conosciamo il tuo settore e le sue regole</h2>
  <p>Ogni ambiente ha rischi e obblighi diversi: ristoranti, hotel, condomini, scuole, industrie, porti.</p></div>
  <div class="griglia-servizi griglia-4">{settori}</div>
</div></section>

<section id="metodo"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Il nostro metodo</span><h2>Difesa integrata: meno chimica, più risultati</h2>
  <p>Non spruzziamo prodotti a caso. Seguiamo il metodo della difesa integrata (IPM): capire, prevenire e intervenire solo dove serve.</p></div>
  <div class="timeline">
    <div class="tappa appare"><div class="icona">{icona('lente')}</div><h3>1. Ispezione</h3><p>Troviamo l'infestante, i nidi, i punti di ingresso e le cause.</p></div>
    <div class="tappa appare"><div class="icona">{icona('documento')}</div><h3>2. Piano su misura</h3><p>Ti spieghiamo cosa faremo, con quali prodotti e quanti passaggi.</p></div>
    <div class="tappa appare"><div class="icona">{icona('erogatore')}</div><h3>3. Trattamento mirato</h3><p>Esche in erogatori chiusi, gel, trappole: solo dove serve.</p></div>
    <div class="tappa appare"><div class="icona">{icona('casa')}</div><h3>4. Prevenzione</h3><p>Chiudiamo i passaggi e ti diamo consigli pratici per non farli tornare.</p></div>
    <div class="tappa appare"><div class="icona">{icona('registro')}</div><h3>5. Monitoraggio e report</h3><p>Controlliamo nel tempo e ti lasciamo i documenti di ogni intervento.</p></div>
  </div>
</div></section>

<section id="calendario" class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Calendario degli infestanti</span><h2>Quando agiscono, mese per mese</h2>
  <p>In Liguria il clima mite allunga la stagione di molti insetti. Prevenire nel mese giusto costa meno che intervenire dopo.</p></div>
  {calendario(base)}
</div></section>

<section id="piani"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Piani di disinfestazione</span><h2>Scegli il piano fatto per te</h2>
  <p>Dal singolo intervento al contratto annuale: prezzi chiari, tutto scritto nel preventivo.</p></div>
  <div class="griglia-pacchetti">{piani}</div>
</div></section>

<section id="multiservizio" class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Pacchetti multiservizio</span><h2>Un solo fornitore per tutti gli obblighi igienici</h2>
  <p>Disinfestazione, derattizzazione, pulizia di cappe e canne fumarie, analisi delle acque, spurghi e rifiuti: li uniamo in un unico contratto, con le scadenze di legge sotto controllo.</p></div>
  <div class="griglia-pacchetti">{multi}</div>
  <p style="text-align:center;margin-top:30px"><a class="btn btn-verde btn-grande" href="pacchetti.html">Vedi tutti i 10 pacchetti, con le leggi di riferimento</a></p>
</div></section>

<section id="perche-noi"><div class="wrap due-colonne">
  <div class="appare">
    <span class="sopratitolo">Perché sceglierci</span>
    <h2>Un'azienda locale, seria, che conosce il territorio</h2>
    <div class="vantaggi">
      <div class="vantaggio"><div class="icona">{icona('scudo')}</div><div><h3>Sicuri per famiglia e animali</h3><p>Erogatori chiusi a chiave, gel nei punti nascosti, prodotti autorizzati e indicazioni chiare.</p></div></div>
      <div class="vantaggio"><div class="icona">{icona('documento')}</div><div><h3>Documenti sempre in ordine</h3><p>Scheda di ogni intervento, planimetrie e report per HACCP, ASL e audit.</p></div></div>
      <div class="vantaggio"><div class="icona">{icona('orologio')}</div><div><h3>Rapidi quando serve</h3><p>Priorità a vespe e calabroni vicino alle persone e alle attività alimentari.</p></div></div>
      <div class="vantaggio"><div class="icona">{icona('persone')}</div><div><h3>Un solo referente</h3><p>Disinfestazione, spurghi, cappe, canne fumarie, rifiuti e analisi: un'unica azienda.</p></div></div>
    </div>
  </div>
  <div class="pannello-albo appare">
    <h3>Sicurezza prima di tutto</h3>
    <table>
      <tr><td>Prodotti</td><td>Solo biocidi e presidi medico-chirurgici autorizzati, usati da personale formato</td></tr>
      <tr><td>Roditori</td><td>Esche in erogatori chiusi, fissati, numerati e segnalati</td></tr>
      <tr><td>Insetti</td><td>Gel ed esche mirate al posto degli spray dove possibile</td></tr>
      <tr><td>Volatili</td><td>Solo sistemi incruenti: reti, aghi, cavi</td></tr>
      <tr><td>Documenti</td><td>Scheda di intervento e schede di sicurezza dei prodotti</td></tr>
    </table>
    <p class="piccolo">Servizi Ecologici S.r.l. è iscritta all'Albo Nazionale Gestori Ambientali n. {DATI['albo']} e gestisce anche i rifiuti prodotti dagli interventi.</p>
  </div>
</div></section>

<section id="zone" class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Dove interveniamo</span><h2>In tutta la Liguria e nel basso Piemonte</h2>
  <p>Partiamo da Finalborgo (Finale Ligure) e raggiungiamo ogni giorno le province di Savona, Imperia, Genova e La Spezia.</p></div>
  <div class="zone appare">{zone}</div>
</div></section>

<section id="domande"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Domande frequenti</span><h2>Le risposte alle domande più comuni</h2></div>
  {faq_html(FAQ_HOME)}
</div></section>

{cta_finale(base)}
"""
    titolo = "Disinfestazione e derattizzazione in Liguria | Servizi Ecologici"
    desc = ("Disinfestazione, derattizzazione, rimozione nidi di vespe e calabroni, zanzare, cimici e piccioni a Savona, Imperia e Genova. "
            "Pest control HACCP per ristoranti e hotel. Preventivo gratuito.")
    return testa(titolo, desc, "", base, schema) + corpo + piede(base)


def pagina_infestante(i):
    base = "../"
    specie = "".join(f'<div class="specie"><h3>{esc(n)}</h3><p>{esc(t)}</p></div>' for n, t in i["specie"])
    segni = "".join(f"<li>{esc(s)}</li>" for s in i["segni"])
    rischi = "".join(f"<li>{esc(s)}</li>" for s in i["rischi"])
    passi = "".join(f'<li><strong>{esc(t)}</strong><span>{esc(d)}</span></li>' for t, d in i["intervento"])
    prev = "".join(f"<li>{esc(s)}</li>" for s in i["prevenzione"])
    mesi = "".join(f'<span class="l{v}" title="{MESI_LUNGHI[m]}">{MESI[m]}</span>' for m, v in enumerate(i["mesi"]))
    altri = "".join(card_infestante(o, base) for o in INFESTANTI if o is not i)
    schema = {"@context": "https://schema.org", "@graph": [
        schema_azienda(),
        {"@type": "Service", "name": "Disinfestazione: " + i["nome"], "description": i["seo_desc"], "provider": {"@id": DATI["dominio"] + "/#azienda"}, "areaServed": "Liguria"},
        schema_faq(i["faq"]),
        briciole_schema([("Home", ""), ("Infestanti", "index.html#infestanti"), (i["nome"], f"infestanti/{i['slug']}.html")]),
    ]}
    corpo = f"""
<section class="hero-servizio"><div class="wrap">
  <div class="briciole"><a href="../index.html">Home</a> › <a href="../index.html#infestanti">Infestanti</a> › {esc(i['nome'])}</div>
  <div class="hero-inf">
    <div>
      <h1>{i['h1']}</h1>
      <p class="sotto" style="font-size:1.15rem;color:var(--testo-2);max-width:760px">{esc(i['intro'])}</p>
      <div class="hero-cta">
        <a class="btn btn-primario btn-grande" href="#preventivo">Preventivo gratuito</a>
        <a class="btn btn-bordo btn-grande" href="tel:{DATI['tel_link']}">{icona('telefono')}{DATI['tel']}</a>
      </div>
      <div class="mini-cal"><span class="mini-cal-titolo">Quando sono più attivi:</span>{mesi}</div>
    </div>
    <div class="ico-grande" aria-hidden="true">{icona(i['icona'])}</div>
  </div>
</div></section>
<nav class="indice"><div class="wrap">
  <a href="#riconoscerli">Come riconoscerli</a><a href="#segni">Segnali</a><a href="#rischi">Rischi</a><a href="#intervento">Come interveniamo</a><a href="#prevenzione">Prevenzione</a><a href="#faq">Domande</a>
</div></nav>
<section style="padding-top:36px"><div class="wrap contenuto">
  <article>
    <h2 id="riconoscerli">Come riconoscerli</h2>
    <div class="griglia-specie">{specie}</div>
    <div class="due-box">
      <div class="box-segni" id="segni"><h2>{icona('lente')} I segnali da non ignorare</h2><ul class="lista-check">{segni}</ul></div>
      <div class="box-rischi" id="rischi"><h2>{icona('scudo')} Perché sono un problema</h2><ul class="lista-allerta">{rischi}</ul></div>
    </div>
    <h2 id="intervento">Come interveniamo</h2>
    <ol class="passi-num">{passi}</ol>
    <div class="riquadro"><strong>Sicurezza:</strong> usiamo solo prodotti autorizzati per l'uso professionale, nelle dosi e nei punti giusti. Al termine ti lasciamo la scheda di intervento con prodotti, aree trattate e indicazioni su come comportarti.</div>
    <h2 id="prevenzione">Cosa puoi fare tu per prevenirli</h2>
    <ul class="lista-check">{prev}</ul>
    <div class="box-wa">
      <div><strong>Non sei sicuro di cosa sia?</strong><p>Mandaci una foto: lo riconosciamo e ti diciamo come procedere.</p></div>
      <a class="btn btn-whatsapp" href="{wa_link('Buongiorno, vi mando la foto di un possibile problema di ' + i['nome'].lower() + ': ')}" target="_blank" rel="noopener">{WA_SVG}Invia foto su WhatsApp</a>
    </div>
    <h2 id="faq">Domande frequenti</h2>
    {faq_html(i['faq'])}
  </article>
  <aside>{modulo(base, i['valore'])}</aside>
</div></section>
<section class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Altri infestanti</span><h2>Ti potrebbe interessare anche</h2></div>
  <div class="griglia-inf">{altri}</div>
</div></section>
{cta_finale(base)}
"""
    return testa(i["seo_title"] + " | Servizi Ecologici", i["seo_desc"], f"infestanti/{i['slug']}.html", base, schema) + corpo + piede(base)


def pagina_servizio(s):
    base = "../"
    cosa = "".join(f"<li>{v}</li>" for v in s["cosa"])
    per_chi = "".join(f"<span>{esc(p)}</span>" for p in s["per_chi"])
    doc = "".join(f"<li>{esc(d)}</li>" for d in s["documenti"])
    altri = "".join(card_generica(o, base, "servizi") for o in SERVIZI if o is not s)
    schema = {"@context": "https://schema.org", "@graph": [
        schema_azienda(),
        {"@type": "Service", "name": s["nome"], "description": s["seo_desc"], "provider": {"@id": DATI["dominio"] + "/#azienda"}, "areaServed": "Liguria"},
        schema_faq(s["faq"]),
        briciole_schema([("Home", ""), ("Servizi", "index.html#servizi"), (s["nome"], f"servizi/{s['slug']}.html")]),
    ]}
    corpo = f"""
<section class="hero-servizio"><div class="wrap">
  <div class="briciole"><a href="../index.html">Home</a> › <a href="../index.html#servizi">Servizi</a> › {esc(s['nome'])}</div>
  <div class="icona">{icona(s['icona'])}</div>
  <h1>{s['h1']}</h1>
  <p class="sotto" style="font-size:1.15rem;color:var(--testo-2);max-width:760px">{esc(s['intro'])}</p>
  <div class="hero-cta">
    <a class="btn btn-primario btn-grande" href="#preventivo">Preventivo gratuito</a>
    <a class="btn btn-bordo btn-grande" href="tel:{DATI['tel_link']}">{icona('telefono')}{DATI['tel']}</a>
  </div>
</div></section>
<section style="padding-top:20px"><div class="wrap contenuto">
  <article>
    <h2>Cosa comprende il servizio</h2>
    <ul class="lista-check">{cosa}</ul>
    <h2>Per chi è pensato</h2>
    <div class="zone sinistra">{per_chi}</div>
    <h2>Come lavoriamo</h2>
    <ol class="passi-num">
      <li><strong>Sopralluogo gratuito</strong><span>Valutiamo il problema e l'ambiente.</span></li>
      <li><strong>Preventivo scritto</strong><span>Con prodotti, numero di passaggi e prezzo chiaro.</span></li>
      <li><strong>Intervento</strong><span>Nei giorni e negli orari concordati.</span></li>
      <li><strong>Controllo e documenti</strong><span>Verifichiamo il risultato e ti lasciamo la documentazione.</span></li>
    </ol>
    <h2>I documenti che ricevi</h2>
    <ul class="lista-check">{doc}</ul>
    <div class="riquadro"><strong>Vuoi unire più servizi?</strong> Con i nostri <a href="../pacchetti.html">pacchetti multiservizio</a> abbini disinfestazione, pulizia cappe e canne fumarie, analisi delle acque e spurghi in un solo contratto.</div>
    <h2>Domande frequenti</h2>
    {faq_html(s['faq'])}
  </article>
  <aside>{modulo(base, s['valore'])}</aside>
</div></section>
<section class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Altri servizi</span><h2>Scopri gli altri servizi</h2></div>
  <div class="griglia-servizi">{altri}</div>
</div></section>
{cta_finale(base)}
"""
    return testa(s["seo_title"] + " | Servizi Ecologici", s["seo_desc"], f"servizi/{s['slug']}.html", base, schema) + corpo + piede(base)


def pagina_settore(s):
    base = "../"
    probl = "".join(f"<li>{esc(p)}</li>" for p in s["problemi"])
    sol = "".join(f"<li>{esc(p)}</li>" for p in s["soluzioni"])
    doc = "".join(f"<li>{esc(d)}</li>" for d in s["documenti"])
    pacc = [p for p in PACCHETTI_MULTI if p["slug"] == s["slug"] or p["icona"] == s["icona"]]
    pacc_html = ""
    if pacc:
        pacc_html = ('<h2>Il pacchetto consigliato per te</h2><div class="pacchetto-inline">'
                     + "".join(card_pacchetto_multi(p, base, completo=True) for p in pacc[:1]) + "</div>")
    altri = "".join(card_generica(o, base, "settori", "Soluzioni per te") for o in SETTORI if o is not s)
    schema = {"@context": "https://schema.org", "@graph": [
        schema_azienda(), schema_faq(s["faq"]),
        briciole_schema([("Home", ""), ("Settori", "index.html#settori"), (s["nome"], f"settori/{s['slug']}.html")]),
    ]}
    corpo = f"""
<section class="hero-servizio"><div class="wrap">
  <div class="briciole"><a href="../index.html">Home</a> › <a href="../index.html#settori">Settori</a> › {esc(s['nome'])}</div>
  <div class="icona">{icona(s['icona'])}</div>
  <h1>{s['h1']}</h1>
  <p class="sotto" style="font-size:1.15rem;color:var(--testo-2);max-width:760px">{esc(s['intro'])}</p>
  <div class="hero-cta">
    <a class="btn btn-primario btn-grande" href="#preventivo">Preventivo gratuito</a>
    <a class="btn btn-bordo btn-grande" href="tel:{DATI['tel_link']}">{icona('telefono')}{DATI['tel']}</a>
  </div>
</div></section>
<section style="padding-top:20px"><div class="wrap contenuto">
  <article>
    <div class="due-box">
      <div class="box-rischi"><h2>{icona('lente')} I problemi più comuni</h2><ul class="lista-allerta">{probl}</ul></div>
      <div class="box-segni"><h2>{icona('scudo')} Come ti aiutiamo</h2><ul class="lista-check">{sol}</ul></div>
    </div>
    <h2>I documenti che ricevi</h2>
    <ul class="lista-check">{doc}</ul>
    {pacc_html}
    <h2>Domande frequenti</h2>
    {faq_html(s['faq'])}
  </article>
  <aside>{modulo(base)}</aside>
</div></section>
<section class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Altri settori</span><h2>Lavoriamo anche per</h2></div>
  <div class="griglia-servizi griglia-4">{altri}</div>
</div></section>
{cta_finale(base)}
"""
    return testa(s["seo_title"] + " | Servizi Ecologici", s["seo_desc"], f"settori/{s['slug']}.html", base, schema) + corpo + piede(base)


def pagina_pacchetti():
    base = ""
    indice = "".join(f'<a href="#{p["slug"]}">{icona(p["icona"])}{esc(p["nome"])}</a>' for p in PACCHETTI_MULTI)
    carte = "".join(card_pacchetto_multi(p, base, completo=True) for p in PACCHETTI_MULTI)
    leggi = "".join(legge_html(k) for k in LEGGI)
    faq = [
        ("Posso togliere o aggiungere servizi a un pacchetto?", "Certo: i pacchetti sono un punto di partenza. Dopo il sopralluogo li adattiamo alla tua attività, togliendo quello che non ti serve e aggiungendo il resto."),
        ("Quanto si risparmia con un pacchetto?", "Unendo i servizi organizziamo meglio uscite e mezzi: il prezzo complessivo è più conveniente rispetto agli interventi chiamati uno per volta, e non rischi di dimenticare una scadenza."),
        ("Chi mi ricorda le scadenze?", "Noi. Ogni pacchetto ha un calendario annuale e ti avvisiamo prima di ogni intervento."),
        ("I documenti sono validi per i controlli?", "Ricevi certificati, schede di intervento, rapporti di analisi e formulari dei rifiuti. I riferimenti normativi indicati sono una guida: per obblighi specifici della tua attività confrontati anche con il tuo consulente."),
    ]
    schema = {"@context": "https://schema.org", "@graph": [schema_azienda(), schema_faq(faq),
                                                              briciole_schema([("Home", ""), ("Pacchetti multiservizio", "pacchetti.html")])]}
    corpo = f"""
<section class="hero-servizio"><div class="wrap">
  <div class="briciole"><a href="index.html">Home</a> › Pacchetti multiservizio</div>
  <div class="icona">{icona('pacco')}</div>
  <h1>Pacchetti multiservizio: <em>tutti gli obblighi igienici, un solo contratto</em></h1>
  <p class="sotto" style="font-size:1.15rem;color:var(--testo-2);max-width:820px">Derattizzazione, disinfestazione, pulizia di cappe e canne fumarie, canalizzazioni dell'aria, analisi delle acque, spurghi e rifiuti. Li uniamo in pacchetti pensati per ogni tipo di attività, con le leggi di riferimento e un calendario annuale delle scadenze.</p>
  <div class="hero-cta">
    <a class="btn btn-primario btn-grande" href="#preventivo" data-servizio="Pacchetto multiservizio">Chiedi il tuo pacchetto</a>
    <a class="btn btn-bordo btn-grande" href="tel:{DATI['tel_link']}">{icona('telefono')}{DATI['tel']}</a>
  </div>
</div></section>
<nav class="indice indice-pacchetti"><div class="wrap">{indice}</div></nav>
<section style="padding-top:36px"><div class="wrap">
  <div class="vantaggi-fascia appare">
    <div><div class="icona">{icona('persone')}</div><strong>Un solo referente</strong><span>per tutti i servizi igienici</span></div>
    <div><div class="icona">{icona('orologio')}</div><strong>Scadenze sotto controllo</strong><span>ti avvisiamo noi prima di ogni intervento</span></div>
    <div><div class="icona">{icona('euro')}</div><strong>Prezzo più conveniente</strong><span>rispetto agli interventi singoli</span></div>
    <div><div class="icona">{icona('documento')}</div><strong>Una cartella unica</strong><span>con certificati, analisi e formulari</span></div>
  </div>
  <div class="griglia-pacchetti griglia-2 pacchetti-pagina">{carte}</div>
</div></section>
<section class="sezione-grigia"><div class="wrap contenuto">
  <article>
    <span class="sopratitolo">Le leggi di riferimento</span>
    <h2 style="margin-top:0">Cosa chiede la normativa, in parole semplici</h2>
    <p>Ecco le principali norme a cui fanno riferimento i servizi dei nostri pacchetti. Non devi conoscerle a memoria: ce ne occupiamo noi e ti lasciamo i documenti che le dimostrano.</p>
    <ul class="lista-leggi grande">{leggi}</ul>
    <p class="nota-legale">I riferimenti normativi sono indicativi e possono cambiare. Gli obblighi precisi dipendono dal tipo di attività, dalle dimensioni e dai regolamenti locali: confrontati anche con il tuo consulente HACCP o per la sicurezza.</p>
    <h2>Domande frequenti</h2>
    {faq_html(faq)}
  </article>
  <aside>{modulo(base, 'Pacchetto multiservizio')}</aside>
</div></section>
{cta_finale(base, "Vuoi un pacchetto su misura per la tua attività?")}
"""
    return testa("Pacchetti multiservizio per hotel, pizzerie, condomini e aziende | Servizi Ecologici",
                 "Disinfestazione, derattizzazione, pulizia cappe e canne fumarie, analisi acque e spurghi in un unico contratto, con le leggi di riferimento. Pacchetti per pizzerie, hotel, bar, condomini, industrie e scuole.",
                 "pacchetti.html", base, schema) + corpo + piede(base)


def pagina_guida():
    base = ""
    blocchi = "".join(
        f'<div class="blocco-guida appare{" attenzione" if t == "Cosa non fare mai" else ""}"><h2>{esc(t)}</h2><ul class="{"lista-allerta" if t == "Cosa non fare mai" else "lista-check"}">'
        + "".join(f"<li>{esc(v)}</li>" for v in voci) + "</ul></div>" for t, voci in GUIDA)
    stagioni = [
        ("Inverno", "Controlla i pini per i nidi di processionaria, chiudi i passaggi dei roditori che cercano riparo al caldo, ispeziona sottotetti e cantine."),
        ("Primavera", "Controlla tapparelle e sottotetti per i primi nidi di vespe, avvia il programma antizanzare, attenzione alle processioni di bruchi sotto i pini."),
        ("Estate", "Elimina i ristagni d'acqua ogni settimana, proteggi la cucina da mosche e blatte, controlla le valigie al rientro dalle vacanze."),
        ("Autunno", "Programma il trattamento preventivo della processionaria, chiudi fessure prima che entrino topi e cimici asiatiche, pulisci grondaie e caditoie."),
    ]
    stag = "".join(f'<div class="stagione appare"><h3>{esc(n)}</h3><p>{esc(t)}</p></div>' for n, t in stagioni)
    inf = "".join(card_infestante(i, base) for i in INFESTANTI)
    schema = {"@context": "https://schema.org", "@graph": [schema_azienda(),
              {"@type": "Article", "headline": "Guida alla prevenzione degli infestanti in casa e in azienda", "author": {"@id": DATI["dominio"] + "/#azienda"}},
              briciole_schema([("Home", ""), ("Consigli di prevenzione", "consigli-prevenzione.html")])]}
    corpo = f"""
<section class="hero-servizio"><div class="wrap">
  <div class="briciole"><a href="index.html">Home</a> › Consigli di prevenzione</div>
  <div class="icona">{icona('foglia')}</div>
  <h1>Guida alla prevenzione: <em>tienili lontani</em> prima che arrivino</h1>
  <p class="sotto" style="font-size:1.15rem;color:var(--testo-2);max-width:760px">Pochi gesti semplici riducono di molto il rischio di infestazioni. Ecco i consigli dei nostri tecnici, stanza per stanza e stagione per stagione.</p>
</div></section>
<section style="padding-top:20px"><div class="wrap">
  <div class="griglia-guida">{blocchi}</div>
</div></section>
<section class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Stagione per stagione</span><h2>Cosa controllare durante l'anno</h2></div>
  <div class="griglia-stagioni">{stag}</div>
  <div style="margin-top:40px">{calendario(base)}</div>
</div></section>
<section><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Approfondisci</span><h2>Schede degli infestanti</h2></div>
  <div class="griglia-inf">{inf}</div>
</div></section>
<section class="sezione-grigia"><div class="wrap contenuto">
  <article><h2 style="margin-top:0">Il problema c'è già?</h2><p>Se hai già notato segni di infestazione, la prevenzione non basta più. Chiamaci o compila il modulo: il sopralluogo è gratuito.</p>
  <div class="box-wa"><div><strong>Hai una foto?</strong><p>Inviala su WhatsApp, ti rispondiamo con un consiglio.</p></div><a class="btn btn-whatsapp" href="{wa_link()}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a></div></article>
  <aside>{modulo(base)}</aside>
</div></section>
"""
    return testa("Consigli per prevenire topi, insetti e infestanti | Servizi Ecologici",
                 "Guida pratica alla prevenzione di topi, blatte, formiche, zanzare, vespe e altri infestanti in casa, in giardino e in azienda, stagione per stagione.",
                 "consigli-prevenzione.html", base, schema) + corpo + piede(base)


def privacy():
    base = ""
    schema = {"@context": "https://schema.org", "@graph": [schema_azienda()]}
    corpo = f"""
<section class="hero-servizio"><div class="wrap"><h1>Informativa privacy e cookie</h1></div></section>
<section style="padding-top:10px"><div class="wrap" style="max-width:820px">
<p><em>Bozza da far verificare al consulente privacy dell'azienda prima della pubblicazione.</em></p>
<h2>Titolare del trattamento</h2>
<p>{DATI['nome']}, sede legale {DATI['sede_legale']}, P. IVA {DATI['piva']}. Email: <a href="mailto:{DATI['email']}">{DATI['email']}</a>.</p>
<h2>Quali dati raccogliamo</h2>
<p>Con il modulo di richiesta preventivo raccogliamo nome, telefono, comune dell'intervento e, se li inserisci, email e descrizione del problema. Se ci scrivi su WhatsApp riceviamo il tuo numero e i messaggi o le foto che invii.</p>
<h2>Perché li usiamo</h2>
<p>Solo per ricontattarti e preparare il preventivo che hai chiesto (art. 6, par. 1, lett. b del Regolamento UE 2016/679). Non usiamo i tuoi dati per pubblicità senza il tuo consenso e non li vendiamo a nessuno.</p>
<h2>Per quanto tempo</h2>
<p>Per il tempo necessario a gestire la richiesta e, se diventi cliente, per la durata del rapporto e gli obblighi di legge.</p>
<h2>I tuoi diritti</h2>
<p>Puoi chiedere in qualsiasi momento di vedere, correggere o cancellare i tuoi dati, limitarne l'uso od opporti al trattamento, scrivendo a <a href="mailto:{DATI['email']}">{DATI['email']}</a>. Puoi anche presentare reclamo al Garante per la protezione dei dati personali (www.garanteprivacy.it).</p>
<h2>Cookie</h2>
<p>Questo sito usa solo cookie tecnici necessari al funzionamento. I caratteri del sito sono caricati da Google Fonts. Se verranno aggiunti strumenti di statistica o pubblicità, questa informativa verrà aggiornata e verrà chiesto il tuo consenso.</p>
</div></section>
"""
    return testa("Privacy e cookie | Servizi Ecologici Disinfestazione", "Informativa sul trattamento dei dati personali e sui cookie.", "privacy.html", base, schema) + corpo + piede(base)


def pagina_404():
    base = "/"
    corpo = f"""
<section class="hero"><div class="wrap" style="display:block;text-align:center">
  <h1>Pagina non trovata</h1>
  <p class="sotto" style="margin:0 auto">La pagina che cerchi non esiste più o è stata spostata.</p>
  <div class="hero-cta" style="justify-content:center"><a class="btn btn-verde btn-grande" href="/">Torna alla home</a>
  <a class="btn btn-bordo btn-grande" href="tel:{DATI['tel_link']}">{icona('telefono')}{DATI['tel']}</a></div>
</div></section>"""
    schema = {"@context": "https://schema.org", "@graph": [schema_azienda()]}
    return testa("Pagina non trovata | Servizi Ecologici", "Pagina non trovata.", "404.html", base, schema).replace(
        '<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"') + corpo + piede(base)


def scrivi(percorso, testo):
    p = os.path.join(SITO, percorso)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(testo)
    print("scritto", percorso)


def main():
    scrivi("index.html", home())
    for i in INFESTANTI:
        scrivi(f"infestanti/{i['slug']}.html", pagina_infestante(i))
    for s in SERVIZI:
        scrivi(f"servizi/{s['slug']}.html", pagina_servizio(s))
    for s in SETTORI:
        scrivi(f"settori/{s['slug']}.html", pagina_settore(s))
    scrivi("pacchetti.html", pagina_pacchetti())
    scrivi("consigli-prevenzione.html", pagina_guida())
    scrivi("privacy.html", privacy())
    scrivi("404.html", pagina_404())
    url = ([""] + [f"infestanti/{i['slug']}.html" for i in INFESTANTI] + [f"servizi/{s['slug']}.html" for s in SERVIZI]
           + [f"settori/{s['slug']}.html" for s in SETTORI] + ["pacchetti.html", "consigli-prevenzione.html", "privacy.html"])
    scrivi("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join(f"  <url><loc>{DATI['dominio']}/{u}</loc></url>\n" for u in url) + "</urlset>\n")
    scrivi("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DATI['dominio']}/sitemap.xml\n")
    scrivi("assets/favicon.svg", LOGO_SVG.replace('<svg viewBox', '<svg xmlns="http://www.w3.org/2000/svg" viewBox').replace(' aria-hidden="true"', ""))


if __name__ == "__main__":
    main()
