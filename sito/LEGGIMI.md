# Sito Servizi Ecologici

Sito statico (HTML + CSS + JS, nessun programma da installare). Si pubblica caricando
**solo il contenuto di questa cartella `sito/`** sull'hosting (Vercel, Netlify, Aruba, Italiaonline…).

> Non caricare online i file nella cartella principale del repository (rubriche, listino interno,
> contratti, bilancio): contengono dati personali e riservati.

## Pagine
- `index.html` – home con modulo preventivo, servizi, pacchetti, Albo, zone, domande frequenti
- `servizi/*.html` – una pagina per ogni servizio, pensata per farsi trovare su Google
- `privacy.html`, `404.html`, `sitemap.xml`, `robots.txt`

## Modificare i testi
Tutti i testi sono in `../strumenti/genera_sito.py`. Si modificano lì e poi si lancia
`python3 strumenti/genera_sito.py`, che riscrive tutte le pagine.

## Da fare prima di andare online
1. **Modulo preventivo**: in `assets/main.js` inserire in `FORM_ENDPOINT` l'indirizzo di un servizio
   di ricezione moduli (es. Formspree). Finché resta vuoto, la richiesta si apre come email nel
   programma di posta del cliente (funziona, ma si perdono alcuni contatti).
2. **Verificare i dati**: numero WhatsApp (329 591 5142, preso dal contratto Italiaonline), anno di
   fondazione 1975, zone servite, pronto intervento nei festivi.
3. **Certificazioni ISO 9001 / 14001**: se sono ancora valide, aggiungerle (sono un forte motivo di fiducia).
4. **Foto vere** di mezzi, squadre e cantieri (prima/dopo): aumentano molto le richieste.
5. **Recensioni Google**: aggiungere solo recensioni reali, con nome e link alla scheda Google.
6. **Privacy**: far controllare `privacy.html` al consulente; se si aggiungono Google Analytics/Ads
   serve il banner per il consenso ai cookie.
7. Dopo la pubblicazione: inviare `sitemap.xml` a Google Search Console e mettere il link del sito
   nella scheda Google Business.
