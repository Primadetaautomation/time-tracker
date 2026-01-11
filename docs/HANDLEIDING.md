# Tijdregistratie - Handleiding

Een complete handleiding voor het installeren en gebruiken van de Tijdregistratie app.

---

## Inhoudsopgave

1. [Installatie](#installatie)
   - [Windows](#windows-installatie)
   - [Mac](#mac-installatie)
   - [Browser (zonder installatie)](#browser-zonder-installatie)
2. [Eerste keer starten](#eerste-keer-starten)
3. [Projecten aanmaken](#projecten-aanmaken)
4. [Uren registreren](#uren-registreren)
   - [Met de timer](#met-de-timer)
   - [Handmatig invoeren](#handmatig-invoeren)
5. [Overzichten bekijken](#overzichten-bekijken)
6. [Exporteren naar Excel](#exporteren-naar-excel)
7. [Tips & Tricks](#tips--tricks)
8. [Problemen oplossen](#problemen-oplossen)

---

## Installatie

### Windows Installatie

#### Stap 1: Node.js installeren

1. Ga naar [nodejs.org](https://nodejs.org)
2. Klik op de grote groene knop **"LTS"** (aanbevolen voor de meeste gebruikers)
3. Open het gedownloade bestand
4. Klik steeds op "Next" en daarna "Install"
5. Wacht tot de installatie klaar is en klik op "Finish"

#### Stap 2: Tijdregistratie downloaden

1. Ga naar de GitHub pagina van dit project
2. Klik op de groene knop **"Code"**
3. Klik op **"Download ZIP"**
4. Open de Downloads map
5. Klik met rechts op het ZIP bestand → **"Alles uitpakken"**
6. Kies een locatie (bijvoorbeeld je Documenten map)

#### Stap 3: Installeren

1. Open de uitgepakte map
2. Ga naar de map `installers`
3. **Dubbelklik** op `install-windows.bat`
4. Een zwart venster opent - wacht tot het klaar is
5. De `dist` map opent automatisch met je nieuwe app!

#### Stap 4: App starten

- **Installer versie**: Dubbelklik op `Tijdregistratie Setup.exe` en volg de stappen
- **Portable versie**: Dubbelklik op `Tijdregistratie.exe` (geen installatie nodig)

> 💡 **Tip**: Na installatie vind je "Tijdregistratie" in je Start menu

---

### Mac Installatie

#### Stap 1: Node.js installeren

**Optie A - Met Homebrew (aanbevolen):**
1. Open Terminal (zoek naar "Terminal" in Spotlight)
2. Plak dit commando en druk Enter:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Daarna:
   ```
   brew install node
   ```

**Optie B - Handmatig:**
1. Ga naar [nodejs.org](https://nodejs.org)
2. Download de **LTS** versie voor Mac
3. Open het .pkg bestand en volg de installatie

#### Stap 2: Tijdregistratie downloaden

1. Ga naar de GitHub pagina van dit project
2. Klik op **"Code"** → **"Download ZIP"**
3. Het bestand komt in je Downloads map
4. Dubbelklik op het ZIP bestand om uit te pakken

#### Stap 3: Installeren

1. Open de uitgepakte map in Finder
2. Ga naar de map `installers`
3. **Dubbelklik** op `install-mac.command`
4. Als je een waarschuwing krijgt:
   - Ga naar Systeemvoorkeuren → Beveiliging
   - Klik op "Toch openen"
5. Wacht tot het script klaar is

#### Stap 4: App installeren

1. De `dist` map opent automatisch
2. Open `Tijdregistratie.dmg`
3. Sleep de app naar de **Applications** map
4. Open de app vanuit Launchpad of Applications

---

### Browser (zonder installatie)

Wil je geen software installeren? Geen probleem!

1. Open de uitgepakte map
2. **Dubbelklik** op `index.html`
3. De app opent in je browser - klaar!

#### Als app installeren vanuit browser (Chrome/Edge):

1. Open `index.html` in Chrome of Edge
2. Klik op het **menu** (drie puntjes rechtsboven)
3. Klik op **"Tijdregistratie installeren"** of **"App installeren"**
4. Je hebt nu een app-icoon op je bureaublad!

---

## Eerste keer starten

Als je de app voor het eerst opent, zie je:

```
┌─────────────────────────────────────────────────────┐
│  Tijdregistratie                    [Exporteer CSV] │
├─────────────┬───────────────────────────────────────┤
│ Projecten   │                                       │
│ [+ Nieuw]   │           00:00:00                    │
│             │        [Start] [Stop]                 │
│             │                                       │
│             │    ┌─ Handmatige invoer ─┐            │
│             │    │ ...                 │            │
│             │    └─────────────────────┘            │
│             │                                       │
│             │    Geregistreerde uren                │
│             │    (nog geen uren)                    │
└─────────────┴───────────────────────────────────────┘
```

**Eerste stap**: Maak een project aan!

---

## Projecten aanmaken

Voordat je uren kunt registreren, moet je minstens één project hebben.

### Nieuw project maken

1. Klik op **"+ Nieuw"** in de linkerzijbalk
2. Vul de gegevens in:

| Veld | Beschrijving | Voorbeeld |
|------|--------------|-----------|
| **Projectnaam** | Naam van het project of de klant | "Website Bakker BV" |
| **Kleur** | Kies een kleur voor herkenning | 🔵 Blauw |
| **Uurtarief** | Je uurtarief (optioneel) | 75.00 |

3. Klik op **"Opslaan"**

### Projecten beheren

- **Bewerken**: Hover over een project → klik op ✏️
- **Verwijderen**: Hover over een project → klik op 🗑️

> ⚠️ **Let op**: Als je een project verwijdert, worden ook alle uren voor dat project verwijderd!

---

## Uren registreren

Er zijn twee manieren om uren te registreren:

### Met de timer

Dit is de makkelijkste manier als je nu aan het werk bent.

1. **Selecteer een project** in de dropdown
2. *(Optioneel)* Typ een beschrijving van wat je gaat doen
3. Klik op **"Start"**
4. De timer begint te lopen: `00:00:00` → `00:01:23` → ...
5. Als je klaar bent, klik op **"Stop"**
6. Je uren worden automatisch opgeslagen!

**Handige weetjes:**
- Je kunt de pagina sluiten - de timer blijft lopen
- Bij heropenen gaat de timer verder waar je was
- Keyboard shortcut: **Ctrl+T** (Windows) of **Cmd+T** (Mac)

### Handmatig invoeren

Handig voor uren van gisteren of vorige week.

1. Scroll naar **"Handmatige invoer"**
2. Vul de velden in:

| Veld | Wat invullen |
|------|--------------|
| **Project** | Kies je project |
| **Datum** | Selecteer de datum |
| **Uren** | Aantal uren (bijv. 2.5 voor 2,5 uur) |
| **Beschrijving** | Wat heb je gedaan? |

3. Klik op **"Toevoegen"**

> 💡 **Tip**: Gebruik 0.25 voor een kwartier, 0.5 voor een half uur

---

## Overzichten bekijken

Onder "Geregistreerde uren" zie je al je registraties.

### Filteren

Gebruik de dropdowns rechtsboven:

| Filter | Opties |
|--------|--------|
| **Project** | Alle projecten, of één specifiek |
| **Periode** | Deze week, Deze maand, Alles |

### Wat je ziet

| Kolom | Betekenis |
|-------|-----------|
| **Datum** | Wanneer gewerkt |
| **Project** | Voor welk project |
| **Beschrijving** | Wat je deed |
| **Uren** | Hoeveel uur |
| **Acties** | Verwijder-knop |

### Totaal

Onderaan zie je **"Totaal uren"** - het totaal van alle gefilterde uren.

---

## Exporteren naar Excel

Voor facturatie of administratie kun je je uren exporteren.

### Hoe exporteren

1. Klik op **"Exporteer CSV"** (rechtsboven)
2. Een bestand `tijdregistratie_DATUM.csv` wordt gedownload

### Openen in Excel

1. Open Excel
2. Ga naar **Bestand** → **Openen**
3. Selecteer het gedownloade CSV bestand
4. Het bestand opent met alle kolommen netjes gesorteerd

### Wat staat er in de export?

| Kolom | Voorbeeld |
|-------|-----------|
| Datum | 2024-01-15 |
| Project | Website Bakker BV |
| Beschrijving | Homepage ontwerp |
| Uren | 3.50 |
| Tarief | 75.00 |
| Bedrag | 262.50 |

> 💡 **Tip**: Het "Bedrag" wordt automatisch berekend als je een uurtarief hebt ingesteld!

---

## Tips & Tricks

### Keyboard shortcuts

| Actie | Windows | Mac |
|-------|---------|-----|
| Start/Stop timer | Ctrl+T | Cmd+T |
| Nieuw project | Ctrl+N | Cmd+N |
| Exporteer | Ctrl+E | Cmd+E |

### Beste werkwijze

1. **Start de dag** met de timer starten
2. **Switch van taak?** Stop de timer, kies ander project, start weer
3. **Einde van de week**: Exporteer naar CSV voor je administratie
4. **Maak duidelijke beschrijvingen** - handig voor facturatie later

### Backup maken

Je data staat lokaal op je computer. Maak regelmatig een backup:

1. Klik op "Exporteer CSV"
2. Bewaar het bestand op een veilige plek (cloud, externe schijf)

---

## Problemen oplossen

### "Mijn uren zijn weg!"

**Browser versie:**
- Heb je je browser cache gewist? Dan zijn de uren helaas weg.
- Tip: Exporteer regelmatig naar CSV als backup.

**Desktop app:**
- Controleer of je dezelfde app opent (niet per ongeluk de browser versie).

### "De timer stopt niet"

1. Ververs de pagina (F5)
2. Controleer of je een project geselecteerd had
3. Probeer opnieuw

### "Export werkt niet"

1. Controleer of er überhaupt uren zijn om te exporteren
2. Probeer een andere browser
3. Check of downloads niet geblokkeerd worden

### "App opent niet (Mac)"

1. Klik rechts op de app → "Open"
2. Of: Systeemvoorkeuren → Beveiliging → "Toch openen"

### "Installatie mislukt (Windows)"

1. Controleer of Node.js correct geïnstalleerd is:
   - Open Command Prompt
   - Typ: `node --version`
   - Je moet een versienummer zien (bijv. v18.17.0)
2. Herstart de computer en probeer opnieuw

---

## Meer hulp nodig?

- Check de [README](../README.md) voor technische details
- Meld problemen op de GitHub Issues pagina

---

*Laatste update: Januari 2024*
