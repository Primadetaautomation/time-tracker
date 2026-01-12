# Tijdregistratie

Een gratis tijdregistratie app met **automatische activity tracking** en **handmatige invoer**.

---

## Download & Installeer

### macOS

1. **Download** [Tijdregistratie-macOS.dmg](https://github.com/Primadetaautomation/test/releases/latest/download/Tijdregistratie-macOS.dmg)
2. **Open** de .dmg
3. **Sleep** Tijdregistratie naar Applications
4. **Open** de app (eerste keer: rechtermuisknop → Open)

> **Permissies:** De app vraagt om Toegankelijkheid permissies voor activity tracking.
> Ga naar Systeeminstellingen → Privacy & Beveiliging → Toegankelijkheid

### Windows

1. **Download** [Tijdregistratie-Windows.zip](https://github.com/Primadetaautomation/test/releases/latest/download/Tijdregistratie-Windows.zip)
2. **Pak uit** de ZIP
3. **Dubbelklik** op `Tijdregistratie.exe`

> **Windows Defender:** Bij eerste keer kan Windows een waarschuwing tonen.
> Klik "Meer info" → "Toch uitvoeren"

---

## Features

| Feature | Beschrijving |
|---------|-------------|
| Timer met start/stop | Tijd bijhouden met 1 klik |
| Handmatige invoer | Achteraf uren registreren |
| Auto activity tracking | Automatisch bijhouden wat je doet |
| Browser URL tracking | Welke websites je bezoekt |
| Email tracking | Email activiteit (Mail app) |
| Idle detection | Pauzes automatisch detecteren |
| Project auto-tagging | Automatisch project toewijzen |
| CSV export | Export naar Excel/spreadsheet |
| Statistieken | Dagelijks/wekelijks/maandelijks overzicht |
| Dark mode | Prettig voor je ogen |

---

## Screenshots

```
+------------------------------------------+
|  Tijdregistratie           [ - ] [ x ]   |
+------------------------------------------+
|  Nu actief:        |  Vandaag    8.5 uur |
|  VS Code           |  Week      32.0 uur |
|  project.py        |  Maand    128.5 uur |
|                    |  Bedrag   €4,285.00 |
|  Timer  02:15:33   +----------------------+
|  [Klant A    v]    |                      |
|  [Start] [Stop]    |  Geregistreerde Uren |
|                    |  2026-01-12  2.5u    |
|  Projecten         |  2026-01-11  8.0u    |
|  ● Klant A  €85/u  |  2026-01-10  7.5u    |
|  ● Klant B  €75/u  |                      |
|  ● Intern         |  [Export CSV]        |
+------------------------------------------+
```

---

## Data & Privacy

**Al je data blijft lokaal op je computer.**

- Geen cloud sync
- Geen account nodig
- Geen tracking door derden
- 100% offline werkbaar

Data locatie: `~/tijdregistratie/tracker/data/`

---

## Ontwikkelaars

### Bouwen vanaf broncode

**macOS:**
```bash
git clone https://github.com/Primadetaautomation/test.git
cd test/tracker
pip3 install pyinstaller customtkinter pillow psutil pyobjc-framework-Quartz pyobjc-framework-Cocoa
./build-mac.sh
```

**Windows:**
```bash
git clone https://github.com/Primadetaautomation/test.git
cd test\tracker
pip install pyinstaller customtkinter pillow psutil pywin32
build-windows.bat
```

### Direct uitvoeren (zonder build)

**macOS:**
```bash
cd tracker
pip3 install customtkinter pillow psutil pyobjc-framework-Quartz pyobjc-framework-Cocoa
python3 desktop_app.py
```

**Windows:**
```bash
cd tracker
pip install customtkinter pillow psutil pywin32
python desktop_app.py
```

---

## Vereisten (alleen voor ontwikkelaars)

- Python 3.9+
- customtkinter
- pillow
- psutil
- pyobjc (macOS) of pywin32 (Windows)

---

## Licentie

MIT License - Vrij te gebruiken, aanpassen en distribueren.

---

Gemaakt voor freelancers en kleine bedrijven.
