# Tijdregistratie

Een gratis tijdregistratie app met **automatische activity tracking** en **handmatige invoer**.

## Snel Starten (Mac)

```bash
# 1. Clone de repository
git clone https://github.com/Primadetaautomation/test.git tijdregistratie
cd tijdregistratie
git checkout claude/create-time-tracking-repo-bqNVW

# 2. Installeer Python dependencies
pip3 install customtkinter pillow psutil pyobjc-framework-Quartz pyobjc-framework-Cocoa

# 3. Start de app
cd tracker
python3 desktop_app.py
```

## Snel Starten (Windows)

```bash
# 1. Clone de repository
git clone https://github.com/Primadetaautomation/test.git tijdregistratie
cd tijdregistratie
git checkout claude/create-time-tracking-repo-bqNVW

# 2. Installeer Python dependencies
pip install customtkinter pillow psutil pywin32

# 3. Start de app
cd tracker
python desktop_app.py
```

## Drie Manieren om te Starten

### Optie 1: Python Desktop App (Aanbevolen)
Moderne UI met alle features.

```bash
cd tracker
python3 desktop_app.py
```

Of dubbelklik op `tracker/Tijdregistratie.command` (Mac)

### Optie 2: Browser Interface
Open `index.html` in je browser. Geen installatie nodig!

### Optie 3: Electron Desktop App
```bash
npm install
npm start
```

---

## Features

| Feature | Desktop App | Browser | Electron |
|---------|-------------|---------|----------|
| Timer met start/stop | ✅ | ✅ | ✅ |
| Handmatige invoer | ✅ | ✅ | ✅ |
| Automatische activity tracking | ✅ | ❌ | ❌ |
| Browser URL tracking | ✅ | ❌ | ❌ |
| Email tracking | ✅ | ❌ | ❌ |
| Idle detection | ✅ | ❌ | ❌ |
| Projecten beheer | ✅ | ✅ | ✅ |
| CSV export | ✅ | ✅ | ✅ |
| Statistieken dashboard | ✅ | ✅ | ✅ |
| Dark mode | ✅ | ❌ | ❌ |
| System tray | ❌ | ❌ | ✅ |

---

## Automatische Activity Tracking

De app kan automatisch bijhouden wat je doet:

```bash
# Start alleen de tracker (zonder UI)
cd tracker
python3 activity_tracker_enhanced.py start

# Bekijk samenvatting van vandaag
python3 activity_tracker_enhanced.py summary

# Bekijk specifieke dag
python3 activity_tracker_enhanced.py summary --date 2026-01-10
```

### Wat wordt gelogd?

| Activiteit | Wat je ziet in CSV |
|------------|-------------------|
| Gmail checken | `Chrome` / `https://mail.google.com` / `email` |
| LinkedIn bekijken | `Chrome` / `https://linkedin.com/jobs` / `social_media` |
| VSCode coderen | `Code` / `project.ts` / `development` |
| Zoom meeting | `zoom.us` / `meeting` |

### Project Auto-Tagging

```bash
# Voeg regels toe om automatisch projecten te taggen
python3 activity_tracker_enhanced.py add-rule "bakker" "Klant Bakker BV"
python3 activity_tracker_enhanced.py add-rule "orbit" "Vacature ORBIT"
python3 activity_tracker_enhanced.py add-rule "gymly" "Klant Gymly"

# Bekijk regels
python3 activity_tracker_enhanced.py list-rules
```

Nu wordt alles met "bakker" in de window titel automatisch getagd als "Klant Bakker BV"!

---

## CSV Export

### Automatisch gelogde uren
```
tracker/data/activity_log_detailed.csv
```

Kolommen:
- Datum, Starttijd, Eindtijd, Duur (sec), Duur (uren)
- Applicatie, Venstertitel, URL, Categorie
- Email Subject, Email Van, Project, Was Idle

### Handmatige uren
Export via de app: klik "Export CSV"

---

## macOS Permissies

De eerste keer vraagt macOS om permissies:

1. **Systeemvoorkeuren → Privacy & Beveiliging → Toegankelijkheid**
   - Voeg Terminal of je IDE toe

2. **Systeemvoorkeuren → Privacy & Beveiliging → Automatisering**
   - Sta toegang toe tot Chrome/Safari/Mail (voor URL tracking)

---

## Projectstructuur

```
tijdregistratie/
├── tracker/
│   ├── desktop_app.py              # Python Desktop UI
│   ├── activity_tracker_enhanced.py # Automatische tracking
│   ├── tray_app.py                 # System tray app
│   ├── Tijdregistratie.command     # Mac launcher
│   └── data/                       # Opgeslagen data
├── index.html                      # Browser interface
├── js/                             # JavaScript voor browser
├── electron/                       # Electron desktop app
└── Tijdregistratie.app/            # macOS app bundle
```

---

## Vereisten

### Python Desktop App
- Python 3.9+
- customtkinter
- pillow
- psutil
- pyobjc (Mac) of pywin32 (Windows)

### Browser Interface
- Moderne browser (Chrome, Firefox, Safari, Edge)

### Electron App
- Node.js 18+

---

## Data & Privacy

**Al je data blijft lokaal op je computer.**

- Geen cloud sync
- Geen account nodig
- Geen tracking door derden
- 100% offline werkbaar

---

## Licentie

MIT License - Vrij te gebruiken, aanpassen en distribueren.

---

Gemaakt met ❤️ voor freelancers en kleine bedrijven.
