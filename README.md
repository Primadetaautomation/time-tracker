# Tijdregistratie Applicatie

Een gratis, open-source tijdregistratie systeem dat volledig lokaal draait. Perfect voor freelancers en kleine bedrijven die hun uren willen bijhouden zonder abonnementskosten.

## Functies

### Web Interface
- **Projecten beheren**: Maak en beheer verschillende projecten met kleuren en uurtarieven
- **Timer functie**: Start/stop timer voor real-time tijdregistratie
- **Handmatige invoer**: Voer handmatig uren in als dat handiger is
- **Overzichten**: Bekijk dagelijkse, wekelijkse en maandelijkse rapportages
- **Export naar CSV**: Exporteer je uren voor facturatie (Excel-compatible)
- **Offline gebruik**: Werkt volledig offline met lokale opslag in je browser

### Desktop Tray App (Windows & Mac)
- **Menubalk integratie**: Snel switchen tussen projecten vanuit je menubalk/systray
- **Automatische tracking**: Zie in één oogopslag hoeveel uur je vandaag hebt gewerkt
- **Timer in menubalk**: Lopende timer zichtbaar in je menubalk

### Activity Tracker (Optioneel)
- **Automatisch loggen**: Houdt bij welke applicaties je gebruikt
- **Slimme regels**: Koppel automatisch activiteiten aan projecten
- **Privacy-first**: Alles blijft lokaal op je computer

## Aan de slag

### 1. Web Interface (Simpelste optie)

Open gewoon `index.html` in je webbrowser. Klaar!

```bash
# Of start een lokale server:
python -m http.server 8000
# Ga naar http://localhost:8000
```

### 2. Desktop Tray App (Aanbevolen)

Installeer de dependencies en start de tray app:

```bash
cd tracker
pip install -r requirements.txt

# Start de tray applicatie
python tray_app.py
```

Je ziet nu een klok-icoon in je menubalk/systray. Klik erop om:
- Snel een project te selecteren en timer te starten
- Je dagelijkse uren te zien
- De timer te stoppen

### 3. Automatische Activity Tracking (Geavanceerd)

```bash
cd tracker
pip install -r requirements.txt

# Extra dependencies voor je platform:
# Windows:
pip install pywin32

# macOS:
pip install pyobjc-framework-Quartz pyobjc-framework-AppKit

# Start tracking
python activity_tracker.py start
```

## Projectstructuur

```
tijdregistratie/
├── index.html              # Web interface
├── css/
│   └── style.css           # Styling
├── js/
│   ├── app.js              # Hoofdapplicatie logica
│   ├── storage.js          # Browser LocalStorage
│   └── utils.js            # Hulpfuncties
├── tracker/                # Desktop tools
│   ├── activity_tracker.py # Automatische activity logging
│   ├── tray_app.py         # Menubalk/systray applicatie
│   ├── requirements.txt    # Python dependencies
│   └── data/               # Lokale data opslag
└── README.md
```

## Gebruik

### Web Interface

1. **Project aanmaken**: Klik op "+ Nieuw" in de sidebar
2. **Timer starten**:
   - Selecteer een project in de dropdown
   - Klik op "Start"
   - Werk aan je taak
   - Klik op "Stop" als je klaar bent
3. **Handmatig invoeren**: Vul het formulier in onder "Handmatige invoer"
4. **Exporteren**: Klik op "Exporteer CSV" voor een Excel-compatible bestand

### Tray App

1. Klik op het klok-icoon in je menubalk
2. Selecteer een project om de timer te starten
3. De timer loopt zichtbaar in je menubalk
4. Klik op "Stop Timer" als je klaar bent

### Activity Tracker Commando's

```bash
# Start tracking
python activity_tracker.py start

# Bekijk samenvatting van vandaag
python activity_tracker.py summary

# Bekijk samenvatting van specifieke dag
python activity_tracker.py summary --date 2024-01-15

# Voeg automatische regel toe
python activity_tracker.py add-rule "klantnaam" "Project X"

# Bekijk alle regels
python activity_tracker.py list-rules
```

## Automatische toewijzingsregels

De activity tracker kan automatisch activiteiten aan projecten koppelen:

```bash
# Als de window titel "ACME" bevat → koppel aan "ACME Project"
python activity_tracker.py add-rule "acme" "ACME Project"

# Als je in Visual Studio Code werkt → koppel aan "Development"
python activity_tracker.py add-rule "visual studio code" "Development"
```

## Data opslag

- **Web interface**: Opgeslagen in browser LocalStorage
- **Tray app & Tracker**: Opgeslagen in `tracker/data/` als JSON/CSV bestanden

Je data blijft altijd lokaal. Niets wordt naar externe servers gestuurd.

## Platformondersteuning

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Web Interface | ✅ | ✅ | ✅ |
| Tray App | ✅ | ✅ | ✅ |
| Activity Tracker | ✅ | ✅ | ✅* |

\* Linux vereist `xdotool` voor window tracking

## Voordelen

- **100% gratis**: Geen abonnementskosten
- **Privacy-first**: Alle data blijft lokaal
- **Volledig aanpasbaar**: Open-source, pas aan naar wens
- **Facturatie-ready**: Export naar CSV voor Excel/Google Sheets
- **Geen internet nodig**: Werkt volledig offline

## Tips

1. **Snelheid**: Gebruik de tray app voor snel switchen tussen projecten
2. **Backup**: Kopieer periodiek de `tracker/data/` map voor backup
3. **Facturatie**: Exporteer wekelijks je uren naar CSV en importeer in Excel
4. **Uurtarief**: Stel je uurtarief in per project voor automatische bedragberekening

## Licentie

MIT License - Vrij te gebruiken en aan te passen.
