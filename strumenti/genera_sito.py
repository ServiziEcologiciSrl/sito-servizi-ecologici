#!/usr/bin/env python3
"""Genera le pagine HTML del sito Servizi Ecologici nella cartella ../sito.

Uso:  python3 strumenti/genera_sito.py
Tutti i testi stanno qui sotto (DATI, SERVIZI, PACCHETTI, FAQ): si modificano qui
e si rilancia lo script, così menu, footer e moduli restano uguali su ogni pagina.
"""
import html
import json
import os

QUI = os.path.dirname(os.path.abspath(__file__))
SITO = os.path.join(QUI, "..", "sito")

DATI = {
    "nome": "Servizi Ecologici S.r.l.",
    "dominio": "https://www.serviziecologici.it",
    "tel": "019 690774",
    "tel_link": "+39019690774",
    "cell": "329 591 5142",
    "verde": "800 015576",
    "verde_link": "+39800015576",
    "whatsapp": "393295915142",
    "email": "servizi@serviziecologici.it",
    "sede_op": "Via Fiume 3, 17024 Finalborgo – Finale Ligure (SV)",
    "sede_legale": "Via Fieno 3, 20123 Milano (MI)",
    "impianto": "Impianto V.A.L. – Località Cenesi, 17035 Cisano sul Neva (SV)",
    "piva": "09843370157",
    "cf": "00365040096",
    "albo": "MI03807",
}

# ---------------------------------------------------------------- icone
ICONE = {
    "amianto": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/><path d="M4 4l16 16"/>',
    "cassone": '<path d="M2 8h15l3 4v6H2z"/><path d="M17 8v4h3"/><circle cx="6" cy="18" r="2"/><circle cx="16" cy="18" r="2"/>',
    "spurgo": '<path d="M12 2s6 7 6 12a6 6 0 0 1-12 0c0-5 6-12 6-12z"/><path d="M9 15a3 3 0 0 0 3 3"/>',
    "camino": '<path d="M7 21V9h4v12"/><path d="M3 21h18"/><path d="M9 6c0-2 2-2 2-4M12 7c0-2 2-2 2-4"/><path d="M13 21v-8h6v8"/>',
    "insetto": '<ellipse cx="12" cy="14" rx="5" ry="6"/><path d="M12 8V5M9 5l-2-2M15 5l2-2M7 12H3M21 12h-4M7 17l-3 2M17 17l3 2"/>',
    "bonifica": '<path d="M12 22c4-2 8-6 8-12V5l-8-3-8 3v5c0 6 4 10 8 12z"/><path d="M8.5 12l2.5 2.5L16 9.5"/>',
    "barca": '<path d="M3 17l2 4h14l2-4z"/><path d="M12 3v14"/><path d="M12 4l7 10H12"/>',
    "analisi": '<path d="M9 3h6M10 3v6L4 20h16L14 9V3"/><path d="M7 15h10"/>',
    "telefono": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "documento": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "orologio": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "euro": '<path d="M18 7a7 7 0 1 0 0 10"/><path d="M4 10h10M4 14h10"/>',
    "mappa": '<path d="M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "persone": '<circle cx="9" cy="8" r="3.5"/><path d="M2 21c0-4 3-6.5 7-6.5s7 2.5 7 6.5"/><path d="M16 4a3.5 3.5 0 0 1 0 7M22 21c0-3-1.5-5.2-4-6"/>',
    "freccia": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "posta": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
}
WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8.2 8.2 0 0 1-4.1-3.6c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.8.4 3.5 3.5 0 0 0-1.1 2.6 6 6 0 0 0 1.3 3.2 13.8 13.8 0 0 0 5.3 4.7c2 .8 2.7.9 3.7.8a3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.2-.3-.3-.6-.4z"/>'
          '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>')


def icona(nome, cls=""):
    return (f'<svg{(" class=" + chr(34) + cls + chr(34)) if cls else ""} viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONE[nome]}</svg>')


LOGO_SVG = ('<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#1d5fbf"/>'
            '<path d="M14 32c0-11 8-18 21-18 0 13-7 21-18 21-1.2 0-2.2-.2-3-.5" fill="#4fb3ff"/>'
            '<path d="M13 36c4-7 9-12 16-15" stroke="#0b3a7e" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>')

# ---------------------------------------------------------------- servizi
# Ordine = servizi più richiesti nel registro chiamate 2026 (rifiuti, amianto, pulizie, canne fumarie).
SERVIZI = [
    {
        "slug": "cassoni-scarrabili-smaltimento-rifiuti",
        "valore": "Cassoni e rifiuti",
        "icona": "cassone",
        "titolo": "Cassoni scarrabili e smaltimento rifiuti",
        "breve": "Noleggio cassoni per cantieri e sgomberi, ritiro e smaltimento di rifiuti pericolosi e non pericolosi, con FIR digitale.",
        "richiesto": True,
        "seo_title": "Noleggio cassoni scarrabili e smaltimento rifiuti a Savona, Imperia e Genova",
        "seo_desc": "Cassoni scarrabili per cantieri, sgomberi e aziende. Smaltimento rifiuti pericolosi e non pericolosi, inerti e terre da scavo, FIR digitale RENTRI. Preventivo gratuito.",
        "h1": "Cassoni scarrabili e smaltimento rifiuti, <em>senza pensieri</em>",
        "intro": "Ti portiamo il cassone, lo ritiriamo quando è pieno e smaltiamo il rifiuto in impianti autorizzati. Ti consegniamo il formulario (FIR) e tutti i documenti di legge.",
        "sezioni": [
            ("Cosa facciamo", [
                "Noleggio di <strong>cassoni scarrabili</strong> di diverse misure, a giornata o a mese",
                "Ritiro e smaltimento di <strong>rifiuti speciali pericolosi e non pericolosi</strong>",
                "Trasporto di <strong>inerti, macerie e terre e rocce da scavo</strong>, anche al nostro impianto V.A.L. di Cisano sul Neva",
                "<strong>Sgomberi</strong> di cantine, solai, magazzini e capannoni, con ritiro degli ingombranti",
                "<strong>Microraccolta</strong> programmata per officine, artigiani e piccole aziende (oli, filtri, imballaggi, toner…)",
            ]),
            ("Per chi", ["Imprese edili e cantieri", "Privati che ristrutturano o svuotano casa", "Aziende, officine, enti e porti", "Condomini"]),
            ("I documenti che ricevi", [
                "<strong>FIR</strong> – formulario di identificazione del rifiuto, digitale RENTRI dove previsto",
                "Copia con il <strong>peso verificato a destino</strong>",
                "Omologa dell'impianto e, se serve, <strong>analisi di caratterizzazione</strong> del rifiuto",
            ]),
        ],
        "riquadro": "<strong>Consiglio:</strong> dicci subito che tipo di rifiuto metterai nel cassone. Rifiuti diversi non si possono mescolare: scegliere il codice giusto all'inizio ti evita costi extra.",
        "faq": [
            ("Serve un permesso per mettere il cassone in strada?", "Sì: se il cassone occupa suolo pubblico serve l'autorizzazione del Comune. Ti diciamo noi cosa chiedere e le misure del cassone da indicare."),
            ("Quanto tempo posso tenere il cassone?", "Il noleggio può essere a giornata o a mese. Quando è pieno ci chiami e lo sostituiamo o lo ritiriamo."),
            ("Che cos'è il RENTRI?", "È il nuovo registro elettronico nazionale dei rifiuti. Siamo iscritti e gestiamo il formulario digitale: tu ricevi i documenti già pronti."),
        ],
    },
    {
        "slug": "rimozione-smaltimento-amianto-eternit",
        "valore": "Amianto",
        "icona": "amianto",
        "titolo": "Rimozione e smaltimento amianto – eternit",
        "breve": "Coperture in eternit, canne fumarie, serbatoi e pavimenti: censimento, analisi, piano di lavoro ASL, rimozione e smaltimento.",
        "richiesto": True,
        "seo_title": "Rimozione e smaltimento amianto ed eternit in Liguria",
        "seo_desc": "Bonifica amianto ed eternit chiavi in mano: sopralluogo gratuito, analisi, piano di lavoro ASL, rimozione, trasporto e smaltimento. Impresa iscritta all'Albo cat. 10B.",
        "h1": "Rimozione amianto ed eternit, <em>chiavi in mano</em>",
        "intro": "Dal sopralluogo allo smaltimento finale pensiamo a tutto noi: pratiche con l'ASL, rimozione in sicurezza, trasporto e smaltimento autorizzato. E se serve, rifacciamo la copertura.",
        "sezioni": [
            ("Cosa facciamo", [
                "<strong>Sopralluogo</strong> e censimento dei materiali contenenti amianto",
                "<strong>Analisi</strong> dei campioni (MOCF o SEM) per capire se c'è amianto",
                "Preparazione e invio del <strong>piano di lavoro all'ASL</strong>",
                "<strong>Rimozione, incapsulamento o confinamento</strong> di lastre, canne fumarie, serbatoi, pavimenti in vinil-amianto",
                "<strong>Trasporto e smaltimento</strong> in impianti autorizzati, con formulario",
                "Rifacimento della copertura con materiali nuovi",
            ]),
            ("Per chi", ["Privati: tettoie, box, capanni, canne fumarie", "Condomini", "Aziende agricole e capannoni", "Enti pubblici"]),
            ("Le nostre autorizzazioni", [
                "Iscrizione all'<strong>Albo Nazionale Gestori Ambientali n. MI03807</strong>",
                "<strong>Categoria 10B</strong> – bonifica di beni contenenti amianto",
                "<strong>Categoria 5</strong> – trasporto di rifiuti pericolosi",
                "Personale formato secondo la normativa sull'amianto, con sorveglianza sanitaria",
            ]),
        ],
        "riquadro": "<strong>Quanto tempo ci vuole?</strong> Il piano di lavoro va inviato all'ASL almeno 30 giorni prima dell'inizio dei lavori (salvo urgenze). Chiamaci per tempo: prima ci contatti, prima partiamo.",
        "faq": [
            ("Come faccio a sapere se il mio tetto è in eternit?", "Facciamo un sopralluogo e, se serve, prendiamo un campione da far analizzare in laboratorio. Così sai con certezza cosa hai e come intervenire."),
            ("Posso togliere da solo una piccola lastra di eternit?", "No. La rimozione dell'amianto deve essere fatta da un'impresa iscritta all'Albo in categoria 10, con piano di lavoro e smaltimento tracciato. Il fai-da-te è pericoloso per la salute e punito dalla legge."),
            ("Quanto costa rimuovere l'eternit?", "Dipende da quantità, accessibilità e tipo di materiale. Dopo il sopralluogo ricevi un preventivo gratuito e chiaro, con piano di lavoro e smaltimento già compresi."),
        ],
    },
    {
        "slug": "spurghi-fognature-fosse-biologiche",
        "valore": "Spurghi e fognature",
        "icona": "spurgo",
        "titolo": "Spurghi, fosse biologiche e videoispezioni",
        "breve": "Autospurgo canaljet per fosse biologiche, fognature, pozzetti e degrassatori. Videoispezioni, ricerca perdite e relining.",
        "richiesto": False,
        "seo_title": "Autospurgo, pulizia fosse biologiche e videoispezioni fognature",
        "seo_desc": "Autospurgo canaljet per fosse biologiche, fognature, pozzetti e degrassatori. Disostruzioni, videoispezioni, ricerca perdite e risanamento tubazioni senza scavi.",
        "h1": "Spurghi e fognature: <em>interveniamo subito</em>",
        "intro": "Scarichi intasati, fossa biologica piena, cattivi odori? Con i nostri autospurghi canaljet liberiamo e puliamo la rete e ti diamo il formulario per lo smaltimento dei fanghi.",
        "sezioni": [
            ("Cosa facciamo", [
                "<strong>Svuotamento e pulizia fosse biologiche</strong>, pozzi neri e pozzetti",
                "<strong>Disostruzione</strong> di fognature, colonne di scarico e caditoie",
                "Pulizia dei <strong>degrassatori</strong> di ristoranti e mense",
                "<strong>Videoispezioni</strong> delle tubazioni con rapporto, foto e video",
                "<strong>Ricerca perdite</strong> con relazione tecnica, utile anche per l'assicurazione",
                "<strong>Relining</strong>: risanamento delle tubazioni senza rompere muri e pavimenti",
                "<strong>Noleggio bagni chimici</strong> per cantieri ed eventi",
            ]),
            ("Per chi", ["Privati e villette", "Condomini e amministratori", "Ristoranti, hotel e aziende", "Comuni ed enti"]),
            ("I documenti che ricevi", [
                "<strong>FIR</strong> per lo smaltimento dei fanghi",
                "Rapporto di <strong>videoispezione</strong> con immagini e planimetria",
                "Relazione tecnica per pratiche assicurative",
            ]),
        ],
        "riquadro": "<strong>Pronto intervento:</strong> per scarichi bloccati e allagamenti chiamaci allo <a href=\"tel:+39019690774\">019 690774</a>. Interveniamo anche il sabato, nei festivi e di notte.",
        "faq": [
            ("Ogni quanto va svuotata la fossa biologica?", "In genere una volta l'anno, ma dipende da quante persone la usano e dal regolamento del tuo Comune. Possiamo programmare noi l'intervento ogni anno."),
            ("Che cos'è la videoispezione?", "Una telecamera entra nel tubo e mostra dove è rotto o intasato. Così si interviene solo dove serve, senza scavare a caso."),
            ("Il relining evita di rompere i pavimenti?", "Sì: il tubo viene risanato dall'interno con una guaina in resina. Prima e dopo facciamo la videoispezione per controllare il risultato."),
        ],
    },
    {
        "slug": "pulizia-canne-fumarie-cappe",
        "valore": "Canne fumarie e cappe",
        "icona": "camino",
        "titolo": "Canne fumarie, cappe e impianti aria",
        "breve": "Pulizia e videoispezione di canne fumarie, cappe di cucine professionali, canalizzazioni dell'aria e condizionatori.",
        "richiesto": True,
        "seo_title": "Pulizia e videoispezione canne fumarie, cappe e canalizzazioni aria",
        "seo_desc": "Pulizia e videoispezione di canne fumarie per case, pizzerie e ristoranti, igienizzazione cappe e canalizzazioni dell'aria. Rapporto con foto prima e dopo.",
        "h1": "Canne fumarie e cappe <em>pulite e sicure</em>",
        "intro": "Una canna fumaria sporca è un rischio di incendio. Puliamo e controlliamo con la telecamera canne fumarie, cappe e condotti dell'aria, e ti lasciamo un rapporto con le foto.",
        "sezioni": [
            ("Cosa facciamo", [
                "<strong>Videoispezione</strong> delle canne fumarie con telecamera",
                "<strong>Pulizia canne fumarie</strong> di camini, stufe, caldaie e forni a legna",
                "Pulizia e igienizzazione delle <strong>cappe</strong> di cucine civili e industriali",
                "Pulizia delle <strong>canalizzazioni dell'aria</strong> e dei condizionatori, anche sulle barche",
                "<strong>Prove di tenuta</strong>, <strong>risanamento con sistemi non invasivi</strong> e <strong>intubamento</strong> delle canne fumarie",
                "<strong>Certificazione di conformità</strong> della canna fumaria",
            ]),
            ("Per chi", ["Privati con camino o stufa", "Pizzerie, ristoranti, mense e hotel", "Uffici e strutture ricettive", "Condomini"]),
            ("I documenti che ricevi", [
                "<strong>Rapporto di intervento</strong> con foto prima e dopo",
                "Documentazione utile per i controlli <strong>HACCP</strong>, per la prevenzione incendi e per l'assicurazione",
            ]),
        ],
        "riquadro": "<strong>Per pizzerie e ristoranti:</strong> con un contratto di pulizia periodica delle cappe hai sempre i documenti pronti per i controlli.",
        "faq": [
            ("Ogni quanto va pulita la canna fumaria?", "Per camini e stufe a legna almeno una volta l'anno, prima dell'inverno. Per forni di pizzerie e cappe professionali anche ogni 3–6 mesi, in base all'uso."),
            ("A cosa serve la videoispezione della canna fumaria?", "A vedere crepe, ostruzioni e depositi che dall'esterno non si vedono. È utile anche quando si compra casa o si installa una nuova stufa."),
        ],
    },
    {
        "slug": "disinfestazione-derattizzazione",
        "valore": "Disinfestazione",
        "icona": "insetto",
        "titolo": "Disinfestazione, derattizzazione e sanificazione",
        "breve": "Topi, blatte, zanzare, vespe e piccioni: interventi rapidi e piani HACCP per ristoranti e aziende alimentari.",
        "richiesto": False,
        "seo_title": "Disinfestazione, derattizzazione e sanificazione a Savona e Imperia",
        "seo_desc": "Derattizzazione, disinfestazione da insetti, sanificazione e allontanamento volatili per case, condomini, ristoranti e aziende. Piani HACCP con report.",
        "h1": "Disinfestazione e derattizzazione, <em>problema risolto</em>",
        "intro": "Usiamo solo prodotti autorizzati e ti lasciamo la scheda di ogni intervento. Per i condomini e le attività alimentari prepariamo piani di controllo periodici.",
        "sezioni": [
            ("Cosa facciamo", [
                "<strong>Derattizzazione</strong> con erogatori di sicurezza",
                "<strong>Disinfestazione</strong> da blatte, formiche, zanzare, vespe, cimici e altri insetti",
                "<strong>Disinfezione e sanificazione</strong> di ambienti",
                "<strong>Allontanamento di piccioni e gabbiani</strong> con sistemi incruenti (reti, dissuasori) e pulizia del guano",
                "<strong>Pest control HACCP</strong> con monitoraggio periodico per ristoranti e industrie alimentari",
            ]),
            ("Per chi", ["Privati", "Condomini e amministratori", "Ristoranti, bar e aziende alimentari", "Aziende, enti e imbarcazioni"]),
            ("I documenti che ricevi", [
                "<strong>Scheda di intervento</strong> con prodotti usati, dosi e aree trattate",
                "Per l'HACCP: <strong>piano di monitoraggio</strong> con planimetria delle postazioni e report periodici",
            ]),
        ],
        "riquadro": "<strong>Per gli amministratori di condominio:</strong> un unico contratto annuale con passaggi programmati e un report pronto per l'assemblea.",
        "faq": [
            ("I prodotti sono pericolosi per bambini e animali?", "Usiamo solo prodotti autorizzati e, per i topi, erogatori chiusi a cui bambini e animali non possono accedere. Ti diciamo sempre come comportarti dopo il trattamento."),
            ("Quanti passaggi servono per la derattizzazione?", "Di solito un ciclo di più passaggi a distanza di qualche settimana, per controllare e rinnovare le esche. Per le attività alimentari il controllo è periodico tutto l'anno."),
        ],
    },
    {
        "slug": "bonifiche-pulizia-cisterne",
        "valore": "Bonifiche e cisterne",
        "icona": "bonifica",
        "titolo": "Bonifiche ambientali e pulizia cisterne",
        "breve": "Bonifica di siti e discariche abusive, pulizia e dismissione di cisterne e serbatoi di gasolio con certificato gas-free.",
        "richiesto": False,
        "seo_title": "Bonifiche ambientali e pulizia cisterne e serbatoi gasolio",
        "seo_desc": "Bonifica di siti contaminati e discariche abusive, pulizia, bonifica e dismissione di cisterne di gasolio con certificato gas-free. Impresa iscritta all'Albo cat. 9.",
        "h1": "Bonifiche e cisterne, <em>in tutta sicurezza</em>",
        "intro": "Passi dal gasolio al metano o alla pompa di calore? Svuotiamo, puliamo e bonifichiamo la vecchia cisterna e ti rilasciamo il certificato. Ci occupiamo anche della bonifica di terreni e discariche abusive.",
        "sezioni": [
            ("Cosa facciamo", [
                "<strong>Pulizia, bonifica e dismissione</strong> di cisterne e serbatoi interrati e fuori terra",
                "<strong>Certificato gas-free</strong> e di avvenuta bonifica a fine lavori",
                "<strong>Pulizia di serbatoi di acqua potabile</strong> e vasche: aspirazione dei fondami con canaljet, pulizia manuale e disinfezione delle pareti",
                "Inertizzazione dei serbatoi",
                "<strong>Bonifica di siti contaminati</strong> e rimozione di <strong>discariche abusive</strong>",
                "Smaltimento dei residui oleosi e dei rifiuti pericolosi",
            ]),
            ("Per chi", ["Condomini con vecchia caldaia a gasolio", "Privati", "Aziende e distributori", "Comuni ed enti"]),
            ("Le nostre autorizzazioni", [
                "Albo Gestori Ambientali n. MI03807 – <strong>categoria 9</strong> (bonifica di siti)",
                "<strong>Categorie 4 e 5</strong> per il trasporto di rifiuti non pericolosi e pericolosi",
                "Personale qualificato per i lavori in spazi confinati",
            ]),
        ],
        "riquadro": "<strong>Lavori in spazi confinati:</strong> entrare in una cisterna è pericoloso e si può fare solo con personale qualificato e attrezzature apposite. Non improvvisare: chiamaci.",
        "faq": [
            ("Devo per forza togliere la vecchia cisterna del gasolio?", "Non sempre: spesso basta svuotarla, bonificarla e renderla inerte. Dopo il sopralluogo ti diciamo qual è la soluzione più semplice ed economica per il tuo caso."),
            ("Che cos'è il certificato gas-free?", "È il documento che attesta che nella cisterna non ci sono più vapori pericolosi. Serve per dismetterla o per lavorarci in sicurezza."),
        ],
    },
    {
        "slug": "nautica-pulizia-serbatoi-barche",
        "valore": "Nautica",
        "icona": "barca",
        "titolo": "Servizi per la nautica",
        "breve": "Svuotamento e pulizia di serbatoi acque nere e grigie, sentine e casse gasolio di barche e yacht, direttamente in porto.",
        "richiesto": False,
        "seo_title": "Pulizia serbatoi barche e yacht: acque nere, sentine e casse gasolio",
        "seo_desc": "Svuotamento e pulizia di casse acque nere e grigie, sentine e serbatoi gasolio di barche e yacht in Liguria. Gas-free, pulizia tubazioni e smaltimento con formulario.",
        "h1": "La tua barca, <em>pulita e in regola</em>",
        "intro": "Interveniamo in porto e nei cantieri navali per svuotare e pulire i serbatoi, con smaltimento tracciato dei rifiuti e ricevuta per l'imbarcazione.",
        "sezioni": [
            ("Cosa facciamo", [
                "Svuotamento e lavaggio delle <strong>casse acque nere e grigie</strong>",
                "Pulizia delle <strong>sentine</strong> e smaltimento degli oli",
                "Bonifica delle <strong>casse gasolio</strong> con certificato gas-free",
                "Pulizia e controllo delle <strong>tubazioni</strong>",
                "Derattizzazione delle imbarcazioni e pulizia delle canalizzazioni dell'aria",
            ]),
            ("Per chi", ["Armatori e proprietari", "Marina e porti turistici", "Cantieri navali", "Equipaggi e comandanti"]),
            ("I documenti che ricevi", ["<strong>FIR</strong> o ricevuta di conferimento dei rifiuti", "Rapporto di intervento e certificato gas-free"]),
        ],
        "riquadro": "<strong>Per marina e cantieri:</strong> possiamo concordare interventi programmati per tutta la stagione.",
        "faq": [
            ("Venite direttamente al posto barca?", "Sì, interveniamo in porto o in cantiere con i nostri mezzi, nel rispetto delle regole del porto."),
        ],
    },
    {
        "slug": "analisi-consulenze-ambientali",
        "valore": "Analisi e consulenza",
        "icona": "analisi",
        "titolo": "Analisi e consulenze ambientali",
        "breve": "Analisi di rifiuti, amianto e acque potabili. Supporto per RENTRI, formulari, MUD, terre e rocce da scavo.",
        "richiesto": False,
        "seo_title": "Analisi rifiuti, amianto e acque e consulenza ambientale RENTRI e MUD",
        "seo_desc": "Analisi di caratterizzazione dei rifiuti, analisi amianto e acque potabili con laboratori accreditati. Consulenza per RENTRI, FIR digitale, MUD e terre e rocce da scavo.",
        "h1": "Analisi e pratiche ambientali, <em>ci pensiamo noi</em>",
        "intro": "Le regole sui rifiuti cambiano spesso. Ti aiutiamo a classificare correttamente i rifiuti e a tenere in ordine registri e formulari, così eviti sanzioni.",
        "sezioni": [
            ("Cosa facciamo", [
                "<strong>Analisi di caratterizzazione</strong> dei rifiuti solidi e liquidi",
                "<strong>Analisi amianto</strong> (MOCF e SEM)",
                "Analisi delle <strong>acque potabili</strong> (rischio chimico-fisico e batteriologico) e <strong>controllo del rischio Legionella</strong>",
                "<strong>Sanificazione delle tubazioni</strong> e dei raccordi idraulici contro la Legionella",
                "<strong>Analisi e pulizia dell'acqua delle piscine</strong>",
                "Prelievo dei campioni da parte di un nostro operatore e <strong>relazione tecnica</strong> finale",
                "Analisi degli inerti e delle terre e rocce da scavo",
                "Supporto per <strong>RENTRI</strong>, FIR digitale, registro di carico e scarico e <strong>MUD</strong>",
            ]),
            ("Per chi", ["Aziende e officine", "Imprese edili", "Ristoranti, hotel e strutture ricettive", "Condomini ed enti"]),
            ("Perché conviene", ["Analisi eseguite da laboratori accreditati", "Un solo referente per analisi, trasporto e smaltimento", "Promemoria delle scadenze"]),
        ],
        "riquadro": "<strong>Novità RENTRI:</strong> il formulario dei rifiuti sta diventando digitale. Se hai dubbi su cosa devi fare, chiamaci: ti spieghiamo tutto in modo semplice.",
        "faq": [
            ("Quando serve l'analisi del rifiuto?", "Quando il codice del rifiuto non è certo o quando l'impianto di destinazione la richiede, ad esempio per grandi quantità di inerti. Ti diciamo noi se serve prima di iniziare."),
        ],
    },
]

PACCHETTI = [
    {"nome": "Casa Serena", "per": "Privati", "evidenza": False,
     "voci": ["Svuotamento fossa biologica e pozzetti", "Videoispezione di controllo degli scarichi", "1 disinfestazione o derattizzazione", "Promemoria annuale: ti chiamiamo noi"],
     "problema": "La fossa biologica va svuotata con regolarità e i fanghi smaltiti con formulario."},
    {"nome": "Condominio Programmato", "per": "Amministratori", "evidenza": True,
     "voci": ["Spurgo colonne e pozzetti", "Derattizzazione programmata delle parti comuni", "Videoispezione della rete", "Allontanamento volatili", "Cassone per sgombero cantine", "Report unico annuale per l'assemblea"],
     "problema": "Un solo contratto, un solo referente e i documenti pronti per l'assemblea e per l'assicurazione."},
    {"nome": "HACCP Completo", "per": "Ristoranti e alimentari", "evidenza": False,
     "voci": ["Pest control HACCP con monitoraggio periodico", "Pulizia degrassatore", "Pulizia cappe e canne fumarie", "Analisi dell'acqua potabile"],
     "problema": "Superi i controlli ASL con tutti i documenti già in ordine."},
    {"nome": "Cantiere Chiavi in Mano", "per": "Imprese edili", "evidenza": False,
     "voci": ["Cassoni scarrabili", "Trasporto inerti all'impianto V.A.L.", "Bagni chimici", "Rimozione amianto con piano di lavoro", "Gestione terre e rocce da scavo"],
     "problema": "Codici dei rifiuti corretti, analisi quando servono e un solo fornitore per tutto il cantiere."},
    {"nome": "Azienda in Regola", "per": "Aziende e officine", "evidenza": False,
     "voci": ["Ritiri programmati dei rifiuti", "Classificazione e analisi", "FIR digitale e supporto RENTRI", "Promemoria MUD", "Pulizia cisterne"],
     "problema": "Pensiamo noi a formulari, registri e scadenze: tu pensi al tuo lavoro."},
    {"nome": "Nautica", "per": "Barche, marina e cantieri", "evidenza": False,
     "voci": ["Svuotamento acque nere e grigie", "Pulizia sentine e casse gasolio", "Gas-free", "Derattizzazione e pulizia impianti aria"],
     "problema": "Smaltimento tracciato dei rifiuti di bordo, direttamente in porto."},
]

FAQ_HOME = [
    ("Il preventivo è davvero gratuito?", "Sì. Il preventivo e, quando serve, il sopralluogo sono gratuiti e senza impegno. Il prezzo che ti diamo comprende già trasporto, smaltimento e documenti, senza sorprese."),
    ("In quali zone lavorate?", "In tutta la Liguria, nelle province di Savona, Imperia, Genova e La Spezia, e nel basso Piemonte. La nostra sede operativa è a Finalborgo (Finale Ligure)."),
    ("Quanto tempo ci vuole per avere un intervento?", "Per spurghi urgenti e scarichi bloccati interveniamo il prima possibile, anche nei festivi. Per i lavori programmati concordiamo con te la data. Per l'amianto bisogna aspettare i 30 giorni del piano di lavoro ASL."),
    ("Mi date i documenti per lo smaltimento?", "Sempre. Per ogni rifiuto ritirato ricevi il formulario (FIR), digitale RENTRI dove previsto. Per videoispezioni, disinfestazioni e pulizie ricevi il rapporto di intervento."),
    ("Siete autorizzati a trattare rifiuti pericolosi e amianto?", "Sì. Siamo iscritti all'Albo Nazionale Gestori Ambientali con il n. MI03807, nelle categorie per i rifiuti urbani, non pericolosi, pericolosi, intermediazione, bonifica di siti e bonifica dell'amianto."),
    ("Lavorate anche per i privati?", "Certo. Molti nostri clienti sono famiglie: svuotamento della fossa biologica, rimozione della tettoia in eternit, pulizia della canna fumaria, disinfestazioni e sgomberi."),
]

ZONE = ["Finale Ligure", "Savona", "Albenga", "Loano", "Pietra Ligure", "Alassio", "Spotorno", "Noli", "Varazze", "Vado Ligure",
        "Andora", "Imperia", "Sanremo", "Ventimiglia", "Taggia", "Genova", "Cairo Montenotte", "Basso Piemonte"]


# ---------------------------------------------------------------- blocchi comuni
def esc(s):
    return html.escape(s, quote=True)


def testa(titolo, desc, percorso, base, schema):
    url = DATI["dominio"] + "/" + percorso
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
<meta property="og:site_name" content="Servizi Ecologici">
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
  <span><span class="pulse"></span>Numero verde <a href="tel:{DATI['verde_link']}">{DATI['verde']}</a> · servizi 24 ore su 24, 7 giorni su 7</span>
  <span class="solo-desktop">Chiamaci: <a href="tel:{DATI['tel_link']}">{DATI['tel']}</a> · <a href="mailto:{DATI['email']}">{DATI['email']}</a></span>
</div></div>
<header class="header"><div class="wrap">
  <a class="logo" href="{base}index.html" aria-label="Servizi Ecologici – home">{LOGO_SVG}<span>Servizi Ecologici<small>Servizi per l'ambiente dal 1975</small></span></a>
  <nav class="nav" aria-label="Menu principale">
    <a href="{base}index.html#servizi">Servizi</a>
    <a href="{base}index.html#soluzioni">Soluzioni</a>
    <a href="{base}index.html#perche-noi">Perché noi</a>
    <a href="{base}index.html#zone">Zone</a>
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
    servizi = "\n".join(f'<li><a href="{base}servizi/{s["slug"]}.html">{esc(s["titolo"])}</a></li>' for s in SERVIZI)
    wa = f"https://wa.me/{DATI['whatsapp']}?text=" + "Buongiorno%2C%20vorrei%20un%20preventivo%20per%3A%20"
    return f"""</main>
<footer class="footer"><div class="wrap">
  <div>
    <a class="logo" href="{base}index.html">{LOGO_SVG}<span>Servizi Ecologici S.r.l.<small>Servizi per l'ambiente dal 1975</small></span></a>
    <p>Rifiuti, amianto, spurghi, bonifiche, disinfestazioni e igiene degli impianti in Liguria e nel basso Piemonte.</p>
    <p>Iscrizione Albo Nazionale Gestori Ambientali n. {DATI['albo']}</p>
  </div>
  <div><h4>Servizi</h4><ul>{servizi}</ul></div>
  <div><h4>Contatti</h4><ul>
    <li><a href="tel:{DATI['verde_link']}">Numero verde {DATI['verde']}</a></li>
    <li><a href="tel:{DATI['tel_link']}">Tel. {DATI['tel']}</a></li>
    <li><a href="{wa}">WhatsApp {DATI['cell']}</a></li>
    <li><a href="mailto:{DATI['email']}">{DATI['email']}</a></li>
  </ul></div>
  <div><h4>Dove siamo</h4><ul>
    <li><strong>Sede operativa</strong><br>{DATI['sede_op']}</li>
    <li><strong>Sede legale</strong><br>{DATI['sede_legale']}</li>
    <li>{DATI['impianto']}</li>
  </ul></div>
  <div class="legale">
    <span>© <span data-anno>2026</span> {DATI['nome']} · P. IVA {DATI['piva']} · C.F. {DATI['cf']}</span>
    <span><a href="{base}privacy.html">Privacy e cookie</a></span>
  </div>
</div></footer>
<a class="wa-flottante" href="{wa}" aria-label="Scrivici su WhatsApp" target="_blank" rel="noopener">{WA_SVG}</a>
<nav class="barra-mobile" aria-label="Contatti rapidi">
  <a class="chiama" href="tel:{DATI['tel_link']}">{icona('telefono')}Chiama</a>
  <a class="wa" href="{wa}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a>
  <a class="prev" href="#preventivo">{icona('documento')}Preventivo</a>
</nav>
<script src="{base}assets/main.js" defer></script>
</body>
</html>
"""


def modulo(base, preselezionato=None):
    scelte = "".join(
        f'<div class="scelta"><input type="radio" name="servizio" id="s{i}" value="{esc(s["valore"])}"'
        f'{" checked" if s["valore"] == preselezionato else ""}><label for="s{i}">{icona(s["icona"])}{esc(s["valore"])}</label></div>'
        for i, s in enumerate(SERVIZI))
    scelte += '<div class="scelta"><input type="radio" name="servizio" id="s-altro" value="Altro"><label for="s-altro">Altro servizio</label></div>'
    tipi = ["Privato", "Condominio", "Azienda", "Impresa edile", "Ristorante / hotel", "Ente pubblico"]
    tipi_html = "".join(f'<div class="scelta"><input type="radio" name="tipo" id="t{i}" value="{t}"><label for="t{i}">{t}</label></div>' for i, t in enumerate(tipi))
    primo = 1 if preselezionato else 0
    passi_attivi = "".join(f'<span{" class=" + chr(34) + "attivo" + chr(34) if i <= primo else ""}></span>' for i in range(3))
    return f"""<div class="card-form" id="preventivo">
  <h2>Preventivo gratuito</h2>
  <p class="nota">3 domande, 1 minuto. Ti richiamiamo noi.</p>
  <form id="form-preventivo" novalidate>
    <div class="passi" aria-hidden="true">{passi_attivi}</div>
    <fieldset class="passo{' attivo' if primo == 0 else ''}" style="border:0;padding:0;margin:0">
      <legend class="campo" style="font-weight:700;margin-bottom:10px">Di cosa hai bisogno?</legend>
      <div class="scelte">{scelte}</div>
    </fieldset>
    <fieldset class="passo{' attivo' if primo == 1 else ''}" style="border:0;padding:0;margin:0">
      <legend class="campo" style="font-weight:700;margin-bottom:10px">Chi sei?</legend>
      <div class="scelte">{tipi_html}</div>
      <div class="azioni-form"><button class="btn btn-bordo" data-indietro>Indietro</button></div>
    </fieldset>
    <fieldset class="passo" style="border:0;padding:0;margin:0">
      <legend class="campo" style="font-weight:700;margin-bottom:10px">Dove ti richiamiamo?</legend>
      <div class="campo"><label for="f-nome">Nome e cognome *</label><input id="f-nome" name="nome" autocomplete="name" required data-nome="Nome e cognome"></div>
      <div class="campo"><label for="f-tel">Telefono *</label><input id="f-tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel" required data-nome="Telefono"></div>
      <div class="campo"><label for="f-comune">Comune dell'intervento *</label><input id="f-comune" name="comune" autocomplete="address-level2" required data-nome="Comune"></div>
      <div class="campo"><label for="f-email">Email (facoltativa)</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
      <div class="campo"><label for="f-note">Descrivi in breve il lavoro (facoltativo)</label><textarea id="f-note" name="note" placeholder="Es. tettoia in eternit di circa 20 m², fossa biologica da svuotare…"></textarea></div>
      <input type="text" name="sito_web" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
      <label class="consenso"><input type="checkbox" name="privacy" required data-nome="Privacy"> <span>Acconsento al trattamento dei miei dati per ricevere il preventivo, come indicato nell'<a href="{base}privacy.html" target="_blank">informativa privacy</a>.</span></label>
      <div class="azioni-form"><button class="btn btn-bordo" data-indietro>Indietro</button><button class="btn btn-primario" type="submit">Invia la richiesta</button></div>
    </fieldset>
    <p class="errore" role="alert"></p>
  </form>
  <p class="form-sicuro">🔒 Gratis e senza impegno · Preferisci parlare? <a href="tel:{DATI['tel_link']}">{DATI['tel']}</a></p>
</div>"""


def faq_html(voci):
    return '<div class="faq">' + "".join(f"<details><summary>{esc(d)}</summary><p>{esc(r)}</p></details>" for d, r in voci) + "</div>"


def schema_azienda():
    return {
        "@type": "LocalBusiness",
        "@id": DATI["dominio"] + "/#azienda",
        "name": DATI["nome"],
        "url": DATI["dominio"] + "/",
        "telephone": "+39 019 690774",
        "email": DATI["email"],
        "foundingDate": "1975",
        "vatID": "IT" + DATI["piva"],
        "address": {"@type": "PostalAddress", "streetAddress": "Via Fiume 3", "addressLocality": "Finale Ligure",
                    "postalCode": "17024", "addressRegion": "SV", "addressCountry": "IT"},
        "areaServed": ["Provincia di Savona", "Provincia di Imperia", "Città metropolitana di Genova", "Provincia della Spezia", "Piemonte"],
        "priceRange": "€€",
    }


def schema_faq(voci):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": d, "acceptedAnswer": {"@type": "Answer", "text": r}} for d, r in voci]}


def cta_finale(base):
    return f"""<section><div class="wrap"><div class="cta-finale appare">
  <h2>Hai un problema da risolvere? Ci pensiamo noi.</h2>
  <p>Raccontaci di cosa hai bisogno: ricevi un preventivo gratuito, chiaro e con tutti i costi già compresi.</p>
  <div class="hero-cta">
    <a class="btn btn-primario btn-grande" href="#preventivo">Richiedi il preventivo gratuito</a>
    <a class="btn btn-bianco btn-grande" href="tel:{DATI['tel_link']}">{icona('telefono')}Chiama {DATI['tel']}</a>
  </div>
</div></div></section>"""


# ---------------------------------------------------------------- pagine
def home():
    base = ""
    card_servizi = "".join(
        f'<a class="servizio appare" href="servizi/{s["slug"]}.html">'
        f'{"<span class=" + chr(34) + "badge-richiesto" + chr(34) + ">Tra i più richiesti</span>" if s["richiesto"] else ""}'
        f'<div class="icona">{icona(s["icona"])}</div><h3>{esc(s["titolo"])}</h3><p>{esc(s["breve"])}</p><span class="vai">Scopri di più</span></a>'
        for s in SERVIZI)
    card_servizi += (f'<a class="servizio appare" href="tel:{DATI["tel_link"]}" style="background:var(--verde-chiaro)">'
                     f'<div class="icona" style="background:#fff">{icona("telefono")}</div><h3>Non trovi quello che cerchi?</h3>'
                     f'<p>Facciamo anche pulizia facciate e rimozione graffiti, controllo acque, linee vita e molto altro. Chiamaci e ti diciamo subito se possiamo aiutarti.</p>'
                     f'<span class="vai">Chiama {DATI["tel"]}</span></a>')
    pacchetti = "".join(
        f'<div class="pacchetto appare{" evidenza" if p["evidenza"] else ""}">'
        f'{"<span class=" + chr(34) + "nastro" + chr(34) + ">Il più scelto</span>" if p["evidenza"] else ""}'
        f'<span class="per">{esc(p["per"])}</span><h3>{esc(p["nome"])}</h3>'
        f'<ul>{"".join("<li>" + esc(v) + "</li>" for v in p["voci"])}</ul>'
        f'<div class="problema">{esc(p["problema"])}</div>'
        f'<a class="btn {"btn-primario" if p["evidenza"] else "btn-verde"}" href="#preventivo">Chiedi un preventivo</a></div>'
        for p in PACCHETTI)
    zone = "".join(f'<span{" class=" + chr(34) + "principale" + chr(34) if z == "Finale Ligure" else ""}>{z}</span>' for z in ZONE)

    schema = {"@context": "https://schema.org", "@graph": [schema_azienda(), schema_faq(FAQ_HOME)]}
    corpo = f"""
<section class="hero"><div class="wrap">
  <div>
    <span class="etichetta">♻ Oltre 50 anni al servizio dell'ambiente in Liguria</span>
    <h1>Rifiuti, amianto e spurghi: <em>risolviamo tutto noi</em>, in regola e senza sorprese.</h1>
    <p class="sotto">Dallo svuotamento della fossa biologica alla bonifica dell'eternit: un solo referente, prezzi chiari e tutti i documenti di legge per privati, condomini e aziende.</p>
    <div class="hero-cta">
      <a class="btn btn-primario btn-grande" href="#preventivo">Preventivo gratuito in 1 minuto</a>
      <a class="btn btn-bordo btn-grande" href="tel:{DATI['tel_link']}">{icona('telefono')}{DATI['tel']}</a>
    </div>
    <ul class="spunte">
      <li>Sopralluogo gratuito</li>
      <li>Iscritti all'Albo Gestori Ambientali</li>
      <li>FIR digitale RENTRI</li>
      <li>Pronto intervento spurghi</li>
    </ul>
  </div>
  {modulo(base)}
</div></section>

<div class="fiducia"><div class="wrap">
  <div><strong>1975</strong><span>l'anno in cui abbiamo iniziato</span></div>
  <div><strong>7</strong><span>categorie Albo Gestori Ambientali</span></div>
  <div><strong>4</strong><span>province liguri + basso Piemonte</span></div>
  <div><strong>0 €</strong><span>per preventivo e sopralluogo</span></div>
</div></div>

<section id="servizi"><div class="wrap">
  <div class="intestazione appare">
    <span class="sopratitolo">I nostri servizi</span>
    <h2>Tutto quello che serve, con un'unica telefonata</h2>
    <p>Mezzi nostri, personale formato e autorizzazioni in regola: seguiamo il lavoro dall'inizio alla fine.</p>
  </div>
  <div class="griglia-servizi">{card_servizi}</div>
</div></section>

<section id="soluzioni" class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare">
    <span class="sopratitolo">Soluzioni su misura</span>
    <h2>Scegli il pacchetto fatto per te</h2>
    <p>Mettiamo insieme i servizi di cui hai bisogno ogni anno: un solo contratto, interventi programmati e documenti sempre in ordine.</p>
  </div>
  <div class="griglia-pacchetti">{pacchetti}</div>
</div></section>

<section><div class="wrap">
  <div class="intestazione appare">
    <span class="sopratitolo">Come lavoriamo</span>
    <h2>Dalla chiamata al lavoro finito in 4 passi</h2>
  </div>
  <div class="passi-lavoro">
    <div class="passo-lavoro appare"><h3>Ci contatti</h3><p>Al telefono, su WhatsApp o con il modulo. Ti richiamiamo al più presto.</p></div>
    <div class="passo-lavoro appare"><h3>Sopralluogo gratuito</h3><p>Se serve veniamo a vedere il lavoro e ti consigliamo la soluzione migliore.</p></div>
    <div class="passo-lavoro appare"><h3>Preventivo chiaro</h3><p>Un prezzo con trasporto, smaltimento e pratiche già compresi.</p></div>
    <div class="passo-lavoro appare"><h3>Lavoro e documenti</h3><p>Eseguiamo l'intervento e ti consegniamo formulari, rapporti e certificati.</p></div>
  </div>
</div></section>

<section id="perche-noi" class="sezione-grigia"><div class="wrap due-colonne">
  <div class="appare">
    <span class="sopratitolo">Perché sceglierci</span>
    <h2>Un'azienda seria, che si prende la responsabilità del lavoro</h2>
    <div class="vantaggi">
      <div class="vantaggio"><div class="icona">{icona('documento')}</div><div><h3>Pensiamo noi alle pratiche</h3><p>Piano di lavoro ASL, formulari, RENTRI, analisi: tu non devi occuparti di nulla.</p></div></div>
      <div class="vantaggio"><div class="icona">{icona('euro')}</div><div><h3>Prezzi chiari, senza sorprese</h3><p>Nel preventivo trovi già trasporto, smaltimento e documenti.</p></div></div>
      <div class="vantaggio"><div class="icona">{icona('orologio')}</div><div><h3>Veloci quando serve</h3><p>Pronto intervento per spurghi e scarichi bloccati, anche nei festivi.</p></div></div>
      <div class="vantaggio"><div class="icona">{icona('persone')}</div><div><h3>Un solo referente</h3><p>Dal cassone all'amianto alla disinfestazione: un'unica azienda per tutto.</p></div></div>
    </div>
  </div>
  <div class="pannello-albo appare">
    <h3>Autorizzati e in regola</h3>
    <p>Iscrizione all'Albo Nazionale Gestori Ambientali <strong>n. {DATI['albo']}</strong></p>
    <table>
      <tr><td>Cat. 1</td><td>Raccolta e trasporto di rifiuti urbani</td></tr>
      <tr><td>Cat. 2-bis</td><td>Trasporto in conto proprio dei propri rifiuti</td></tr>
      <tr><td>Cat. 4</td><td>Raccolta e trasporto di rifiuti speciali non pericolosi</td></tr>
      <tr><td>Cat. 5</td><td>Raccolta e trasporto di rifiuti speciali pericolosi</td></tr>
      <tr><td>Cat. 8</td><td>Intermediazione e commercio di rifiuti</td></tr>
      <tr><td>Cat. 9</td><td>Bonifica di siti</td></tr>
      <tr><td>Cat. 10B</td><td>Bonifica di beni contenenti amianto</td></tr>
    </table>
    <p class="piccolo">Iscritti al RENTRI, il registro elettronico nazionale per la tracciabilità dei rifiuti. Impianto di recupero inerti V.A.L. a Cisano sul Neva (SV).</p>
  </div>
</div></section>

<section id="zone"><div class="wrap">
  <div class="intestazione appare">
    <span class="sopratitolo">Dove lavoriamo</span>
    <h2>In tutta la Liguria e nel basso Piemonte</h2>
    <p>Partiamo da Finalborgo (Finale Ligure) e raggiungiamo ogni giorno le province di Savona, Imperia, Genova e La Spezia.</p>
  </div>
  <div class="zone appare">{zone}</div>
</div></section>

<section id="domande" class="sezione-grigia"><div class="wrap">
  <div class="intestazione appare"><span class="sopratitolo">Domande frequenti</span><h2>Le risposte alle domande più comuni</h2></div>
  {faq_html(FAQ_HOME)}
</div></section>

{cta_finale(base)}
"""
    titolo = "Servizi Ecologici – Rifiuti, amianto, spurghi e bonifiche in Liguria"
    desc = ("Smaltimento rifiuti, cassoni scarrabili, rimozione amianto ed eternit, spurghi, canne fumarie e disinfestazioni "
            "a Savona, Imperia e Genova. Dal 1975, iscritti all'Albo Gestori Ambientali. Preventivo gratuito.")
    return testa(titolo, desc, "", base, schema) + corpo + piede(base)


def pagina_servizio(s):
    base = "../"
    sezioni = ""
    for titolo, voci in s["sezioni"]:
        sezioni += f"<h2>{esc(titolo)}</h2><ul>" + "".join(f"<li>{v}</li>" for v in voci) + "</ul>"
    altri = "".join(f'<li><a href="{o["slug"]}.html">{esc(o["titolo"])}</a></li>' for o in SERVIZI if o is not s)
    schema = {"@context": "https://schema.org", "@graph": [
        schema_azienda(),
        {"@type": "Service", "name": s["titolo"], "description": s["seo_desc"], "provider": {"@id": DATI["dominio"] + "/#azienda"},
         "areaServed": "Liguria"},
        schema_faq(s["faq"]),
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DATI["dominio"] + "/"},
            {"@type": "ListItem", "position": 2, "name": s["titolo"], "item": f'{DATI["dominio"]}/servizi/{s["slug"]}.html'}]},
    ]}
    corpo = f"""
<section class="hero-servizio"><div class="wrap">
  <div class="briciole"><a href="../index.html">Home</a> › <a href="../index.html#servizi">Servizi</a> › {esc(s['titolo'])}</div>
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
    {sezioni}
    <div class="riquadro">{s['riquadro']}</div>
    <h2>Domande frequenti</h2>
    {faq_html(s['faq'])}
    <h2>Altri servizi</h2>
    <ul>{altri}</ul>
  </article>
  <aside>{modulo(base, s['valore'])}</aside>
</div></section>
{cta_finale(base)}
"""
    return testa(s["seo_title"] + " | Servizi Ecologici", s["seo_desc"], f"servizi/{s['slug']}.html", base, schema) + corpo + piede(base)


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
<p>Con il modulo di richiesta preventivo raccogliamo nome, telefono, comune dell'intervento e, se li inserisci, email e descrizione del lavoro.</p>
<h2>Perché li usiamo</h2>
<p>Solo per ricontattarti e preparare il preventivo che hai chiesto (art. 6, par. 1, lett. b del Regolamento UE 2016/679). Non usiamo i tuoi dati per pubblicità senza il tuo consenso e non li vendiamo a nessuno.</p>
<h2>Per quanto tempo</h2>
<p>Per il tempo necessario a gestire la richiesta e, se diventi cliente, per la durata del rapporto e gli obblighi di legge (ad esempio fiscali e sui rifiuti).</p>
<h2>I tuoi diritti</h2>
<p>Puoi chiedere in qualsiasi momento di vedere, correggere o cancellare i tuoi dati, limitarne l'uso od opporti al trattamento, scrivendo a <a href="mailto:{DATI['email']}">{DATI['email']}</a>. Puoi anche presentare reclamo al Garante per la protezione dei dati personali (www.garanteprivacy.it).</p>
<h2>Cookie</h2>
<p>Questo sito usa solo cookie tecnici necessari al funzionamento. I caratteri del sito sono caricati da Google Fonts. Se in futuro verranno aggiunti strumenti di statistica o pubblicità (es. Google Analytics, Google Ads), questa informativa verrà aggiornata e verrà chiesto il tuo consenso.</p>
</div></section>
"""
    return testa("Privacy e cookie | Servizi Ecologici", "Informativa sul trattamento dei dati personali e sui cookie del sito Servizi Ecologici S.r.l.", "privacy.html", base, schema) + corpo + piede(base)


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
    for s in SERVIZI:
        scrivi(f"servizi/{s['slug']}.html", pagina_servizio(s))
    scrivi("privacy.html", privacy())
    scrivi("404.html", pagina_404())
    url = [""] + [f"servizi/{s['slug']}.html" for s in SERVIZI] + ["privacy.html"]
    scrivi("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join(f"  <url><loc>{DATI['dominio']}/{u}</loc></url>\n" for u in url) + "</urlset>\n")
    scrivi("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DATI['dominio']}/sitemap.xml\n")
    scrivi("assets/favicon.svg", LOGO_SVG.replace('<svg viewBox', '<svg xmlns="http://www.w3.org/2000/svg" viewBox').replace(' aria-hidden="true"', ""))


if __name__ == "__main__":
    main()
