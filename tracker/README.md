# Automatische Activity Tracker

Houdt automatisch bij welke programma's en websites je gebruikt, en hoeveel tijd je eraan besteedt.

## Starten op Mac

1. **Dubbelklik** op `START-TRACKER.command`
2. Bij eerste keer: geef toestemming in Systeeminstellingen (zie onder)
3. Laat het venster open - de tracker loopt op de achtergrond
4. Druk **Ctrl+C** om te stoppen

## Permissies instellen (eenmalig)

De tracker moet weten welk venster actief is. Daarvoor heeft macOS toestemming nodig:

1. Ga naar **Systeeminstellingen** → **Privacy en beveiliging**
2. Klik op **Toegankelijkheid**
3. Klik op het **+** icoon
4. Voeg **Terminal** toe (of iTerm als je dat gebruikt)
5. Zorg dat het vinkje aan staat

## Je uren bekijken

**Dubbelklik** op `BEKIJK-UREN.command`

Je ziet dan een overzicht:
```
=== Activiteit Samenvatting voor 2024-01-15 ===

Safari                                   2.50u ( 35.0%)
Visual Studio Code                       3.25u ( 45.5%)
Slack                                    1.40u ( 19.5%)

Totaal                                   7.15u
```

## Projecten automatisch toewijzen

Je kunt regels instellen om activiteiten automatisch aan projecten te koppelen:

```bash
# Open Terminal en ga naar de tracker folder
cd tracker

# Voeg regel toe: als "klantnaam" in de titel staat → project "Klant X"
python3 activity_tracker.py add-rule "klantnaam" "Klant X"

# Als je in Figma werkt → project "Design"
python3 activity_tracker.py add-rule "figma" "Design"

# Bekijk alle regels
python3 activity_tracker.py list-rules
```

## Waar wordt de data opgeslagen?

- `tracker/data/activity_log.csv` - Alle gelogde activiteiten
- `tracker/data/config.json` - Je instellingen en regels

## Tips

1. **Start de tracker 's ochtends** - laat hem de hele dag draaien
2. **Maak regels** voor je belangrijkste klanten/projecten
3. **Bekijk je uren** aan het einde van de dag
4. De data is een CSV bestand - je kunt het openen in Excel!

## Problemen?

**"Operation not permitted"**
→ Je hebt de Toegankelijkheid permissies niet ingesteld (zie boven)

**Tracker stopt meteen**
→ Python3 is niet geïnstalleerd. Run: `brew install python3`

**Geen data in het overzicht**
→ Je moet de tracker minimaal 30 seconden draaien
