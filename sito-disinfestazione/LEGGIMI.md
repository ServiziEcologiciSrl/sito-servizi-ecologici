# Sito Disinfestazione e Derattizzazione – Servizi Ecologici

Sito statico separato dal sito principale, dedicato a disinfestazione, derattizzazione,
allontanamento volatili, sanificazione e pacchetti multiservizio.
Si pubblica caricando **solo il contenuto di questa cartella** sull'hosting.

## Pagine (32)
- `index.html` – home: modulo preventivo, 12 infestanti, fascia urgenze, casa/azienda, servizi,
  "Cosa hai notato?" (riconoscimento dai segnali), settori, metodo, calendario stagionale,
  piani, pacchetti multiservizio, sicurezza, zone, domande frequenti
- `infestanti/*.html` – 12 schede (riconoscerli, segnali, rischi, intervento, prevenzione, FAQ)
- `servizi/*.html` – 7 servizi
- `settori/*.html` – 8 settori con il pacchetto consigliato
- `pacchetti.html` – 10 pacchetti multiservizio con le leggi di riferimento
- `consigli-prevenzione.html` – guida alla prevenzione
- `privacy.html`, `404.html`, `sitemap.xml`, `robots.txt`

## Modificare i testi
I testi sono in `../strumenti/dati_disinfestazione.py`; poi si lancia
`python3 strumenti/genera_sito_disinfestazione.py`, che riscrive tutte le pagine.
Stile e script (`assets/style.css`, `assets/main.js`) si modificano direttamente.

## Da verificare prima di andare online
1. **Indirizzo del sito**: nel file dati è impostato `disinfestazione.serviziecologici.it` (da confermare).
2. **Modulo preventivo**: in `assets/main.js` inserire `FORM_ENDPOINT` (es. Formspree), come nel sito principale.
3. **Riferimenti normativi** dei pacchetti (`LEGGI` nel file dati): farli controllare al consulente HACCP/sicurezza.
4. **Servizi confermati dai depliant aziendali**: Legionella (analisi e sanificazione tubazioni), igienizzazione
   impianti di condizionamento, allontanamento volatili (anche ultrasuoni e centraline), analisi e pulizia piscine,
   numero verde 800 015576 attivo 24/7. **Ancora da confermare**: trattamenti in quota (vespe, processionaria),
   cimici dei letti, lampade cattura-insetti, interventi a bordo.
5. **Certificazioni**: se l'azienda ha certificazioni del settore (es. UNI EN 16636) aggiungerle: sono un forte motivo di fiducia.
6. **Foto vere** di tecnici, mezzi ed erogatori, e recensioni Google reali.
