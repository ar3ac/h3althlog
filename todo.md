# h3althlog — To‑Do List
_Aggiornato: 2025-08-19 11:16_

> Obiettivo: rendere la dashboard **mobile‑first**, con **navigazione settimanale**, vista **mensile**, e UX più pulita senza cambiare i contenuti.

---

## M1 — Struttura & Navigazione (priorità)
- [ ] **Dashboard settimanale con navigazione**
  - [ ] Route `/dashboard?start=YYYY-MM-DD` con calcolo di `monday_of(start)`
  - [ ] Parametri: `prev_start`, `next_start`, `today`
  - [ ] Pulsanti: ← Settimana precedente · Oggi · Settimana successiva →
  - [ ] Evidenziazione **Oggi** nella lista giorni
- [ ] **Lista giorni in griglia (3 colonne)**
  - [ ] Colonne: *Giorno+data* · *Stato* (✔️ Compilato / ➕ Vuoto) · *Azione*
  - [ ] Unifica l’azione in un solo bottone **Apri**
  - [ ] Route helper `open_day(date)` → se esiste **edit**, altrimenti **new**
- [ ] **Pulizia testuale**
  - [ ] Rimuovi “Ciao / Benvenuto…” in cima
  - [ ] Titolo pagina: **Settimana DD MMM – DD MMM YYYY**
- [ ] **Stile mobile‑first**
  - [ ] CSS base per `.btn`, `.badge`, `.card`, `.days` (griglia responsive)
  - [ ] **FAB** “➕ Aggiungi giornata” fisso in basso a dx su mobile
  - [ ] “Logout” compatto in alto a destra
- [ ] **Card riassunti**
  - [ ] Card 1: *Qualità pasti (media)* → Colazione / Pranzo / Cena
  - [ ] Card 2: *Benessere* → Umore medio (valore+emoji) / Passi medi
  - [ ] Scala colori coerente (verde buono, giallo ok, rosso scarso) — mappa alla tua scala reale

---

## M2 — Vista Mensile & UX dati
- [ ] **Vista mensile**
  - [ ] Route `/month/<int:year>/<int:month>`
  - [ ] Griglia calendario lun→dom, badge ✔️/➕ per giorno
  - [ ] Click su giorno → `open_day(date)`
  - [ ] Link “Torna alla settimana corrente”
- [ ] **Form & scelte**
  - [ ] Placeholder “— seleziona —” con salvataggio `None` (no 0)
  - [ ] Scelte dieta con icone **compatte** (🌱 vegano · 🥛🧀🥚 vegetariano · 🐟 pescetariano · 🥩 carnivoro)
  - [ ] Umore come `SelectField` con 😃 😐 😞 (label + emoji)
- [ ] **Averages**
  - [ ] Calcolo medie settimanali (pasti, umore, passi) con esclusione `None`
  - [ ] Formattazione numerica passi (separatore migliaia)

---

## M3 — Extra utili
- [ ] **Trend vs settimana precedente** (freccia ↑/↓ su pasti, umore, passi)
- [ ] **Export dati**
  - [ ] `/export.csv` (periodo opzionale via query)
  - [ ] `/export.json` (periodo opzionale via query)
- [ ] **Edit rapido (opzionale)**
  - [ ] Modale o inline edit dalla dashboard settimanale
- [ ] **Test & migrazioni**
  - [ ] Attiva Flask‑Migrate
  - [ ] Test: creazione/modifica entry, `0 → None`, calcolo settimana/mese, `open_day()`
- [ ] **Qualità**
  - [ ] Accessibilità: focus state visibili, label associate, aria‑label sui bottoni icona
  - [ ] Gestione errori: messaggi flash chiari e non intrusivi

---

## Criteri di accettazione (Definition of Done)
- [ ] Navigazione tra settimane funzionante via query `start`; bottone **Oggi** ripristina la settimana corrente
- [ ] Lista giorni leggibile **senza bullet**, con badge ✔️/➕ e unico bottone **Apri**
- [ ] **Mobile‑first**: nessuno scroll orizzontale, tap target ≥ 40px, FAB presente
- [ ] Medie settimanali visibili in due card e coerenti con i dati inseriti
- [ ] Vista **mensile** cliccabile che porta alle giornate
- [ ] Export CSV scaricabile con intestazioni chiare

---

## Note operative
- Suggerito: creare branch `feature/dashboard-m1` → PR → merge.
- Mantieni le route vecchie attive finché la nuova dashboard non è pronta, poi reindirizza.
- Evita di hardcodare colori/emoji nei dati: tieni una mappa nel template o in util.
