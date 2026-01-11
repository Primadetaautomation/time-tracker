#!/bin/bash
# ===========================================
#   ACTIVITY TRACKER - START SCRIPT
#   Dubbelklik om automatisch tracking te starten
# ===========================================

cd "$(dirname "$0")"

echo ""
echo "  =========================================="
echo "    AUTOMATISCHE ACTIVITY TRACKER"
echo "  =========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 is niet geinstalleerd."
    echo "Installeer via: brew install python3"
    echo ""
    read -p "Druk Enter om af te sluiten..."
    exit 1
fi

# Installeer dependencies als nodig
echo "Dependencies controleren..."
pip3 install --quiet pyobjc-framework-Quartz pyobjc-framework-AppKit psutil 2>/dev/null

# Vraag om Accessibility permissions
echo ""
echo "BELANGRIJK: De tracker heeft 'Toegankelijkheid' permissies nodig."
echo ""
echo "Als dit de eerste keer is:"
echo "  1. Ga naar Systeeminstellingen > Privacy en beveiliging"
echo "  2. Klik op 'Toegankelijkheid'"
echo "  3. Klik op '+' en voeg Terminal toe"
echo "     (of de app waarmee je dit draait)"
echo ""
read -p "Druk Enter als je klaar bent..."

# Start de tracker
echo ""
echo "Tracker wordt gestart..."
echo "Sluit dit venster NIET - de tracker draait hier."
echo "Druk Ctrl+C om te stoppen."
echo ""

python3 activity_tracker.py start
