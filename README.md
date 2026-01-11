# Tijdregistratie

Een gratis, makkelijk te installeren tijdregistratie app voor Windows en Mac.

![Screenshot](assets/screenshot.png)

## Installeren (Makkelijk!)

### Optie 1: Desktop App (Aanbevolen)

**Windows:**
1. Download en installeer [Node.js](https://nodejs.org) (LTS versie)
2. Download deze repository als ZIP en pak uit
3. Dubbelklik op `installers/install-windows.bat`
4. Volg de instructies - klaar!

**Mac:**
1. Installeer Node.js: `brew install node` (of download van [nodejs.org](https://nodejs.org))
2. Download deze repository als ZIP en pak uit
3. Dubbelklik op `installers/install-mac.command`
4. Sleep de app naar Applications - klaar!

### Optie 2: Direct in Browser

Gewoon `index.html` openen in je browser. Werkt meteen!

> **Tip:** In Chrome/Edge kun je de app "installeren" via het menu (drie puntjes) → "Installeer Tijdregistratie". Dan krijg je een echte app-icoon.

### Optie 3: Draagbare Versie (Portable)

1. Download de repository
2. Open een terminal in de folder
3. `npm install && npm start`

## Hoe werkt het?

### Timer gebruiken
1. Maak eerst een **project** aan (klik "+ Nieuw" in de sidebar)
2. Selecteer je project in de dropdown
3. Klik **Start** - de timer loopt!
4. Klik **Stop** wanneer je klaar bent
5. Je uren worden automatisch opgeslagen

### Handmatig invoeren
- Vul het formulier in onder "Handmatige invoer"
- Handig voor uren van gisteren of vorige week

### Exporteren voor facturatie
- Klik "Exporteer CSV"
- Open in Excel of Google Sheets
- Inclusief berekende bedragen (als je een uurtarief hebt ingesteld)

## Features

| Feature | Beschikbaar |
|---------|-------------|
| Timer met start/stop | ✅ |
| Handmatige invoer | ✅ |
| Meerdere projecten | ✅ |
| Uurtarieven per project | ✅ |
| Export naar CSV/Excel | ✅ |
| Werkt offline | ✅ |
| Desktop app (Windows/Mac) | ✅ |
| System tray icoon | ✅ |
| Keyboard shortcuts | ✅ |
| Data sync tussen apparaten | ❌ (lokaal alleen) |

## Keyboard Shortcuts

| Actie | Windows | Mac |
|-------|---------|-----|
| Start/Stop timer | Ctrl+T | Cmd+T |
| Nieuw project | Ctrl+N | Cmd+N |
| Exporteer CSV | Ctrl+E | Cmd+E |
| Volledig scherm | F11 | Cmd+Ctrl+F |

## Waar worden mijn uren opgeslagen?

- **Browser versie:** In je browser (LocalStorage)
- **Desktop app:** In je browser engine (Chromium)

Al je data blijft **lokaal op je computer**. Er wordt niets naar externe servers gestuurd.

### Backup maken
Gebruik de "Exporteer CSV" functie om regelmatig een backup te maken van je uren.

## Technisch

### Vereisten voor bouwen
- Node.js 18 of hoger
- npm

### Development
```bash
# Installeer dependencies
npm install

# Start in development mode
npm start

# Bouw voor productie
npm run build        # Alle platforms
npm run build:win    # Alleen Windows
npm run build:mac    # Alleen Mac
npm run build:linux  # Alleen Linux
```

### Projectstructuur
```
tijdregistratie/
├── index.html          # Hoofdpagina
├── manifest.json       # PWA configuratie
├── sw.js               # Service worker (offline)
├── package.json        # Node.js configuratie
├── css/
│   └── style.css
├── js/
│   ├── app.js          # Hoofdlogica
│   ├── storage.js      # Data opslag
│   └── utils.js        # Hulpfuncties
├── electron/
│   ├── main.js         # Desktop app main process
│   └── preload.js      # Security bridge
├── installers/
│   ├── install-windows.bat
│   └── install-mac.command
└── assets/
    └── icons...
```

## Veelgestelde vragen

**Kan ik dit gebruiken op meerdere computers?**
Ja, maar de data synchroniseert niet automatisch. Gebruik de CSV export om data over te zetten.

**Is het echt gratis?**
Ja, 100% gratis en open-source. Geen verborgen kosten of abonnementen.

**Kan ik de broncode aanpassen?**
Absoluut! Het is open-source onder de MIT licentie.

**Werkt het op Linux?**
Ja! Gebruik `npm run build:linux` om een AppImage of .deb te maken.

## Licentie

MIT License - Vrij te gebruiken, aanpassen en distribueren.

---

Gemaakt met ❤️ voor freelancers en kleine bedrijven die een simpele, gratis oplossing zoeken.
