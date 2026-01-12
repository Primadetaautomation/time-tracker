#!/bin/bash
# =============================================================================
# Build script voor macOS
# Maakt een standalone Tijdregistratie.app
# =============================================================================

set -e  # Stop bij errors

# Kleuren
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "  ======================================"
echo "    TIJDREGISTRATIE - macOS BUILD"
echo "  ======================================"
echo ""

# Ga naar script directory
cd "$(dirname "$0")"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3 is niet geïnstalleerd${NC}"
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Python3 gevonden: $(python3 --version)"

# Check/installeer PyInstaller
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo -e "${BLUE}[..]${NC} PyInstaller installeren..."
    pip3 install pyinstaller
fi
echo -e "${GREEN}[OK]${NC} PyInstaller beschikbaar"

# Installeer dependencies
echo -e "${BLUE}[..]${NC} Dependencies installeren..."
pip3 install customtkinter pillow psutil pyobjc-framework-Quartz pyobjc-framework-Cocoa --quiet
echo -e "${GREEN}[OK]${NC} Dependencies geïnstalleerd"

# Clean vorige build
echo -e "${BLUE}[..]${NC} Opruimen vorige build..."
rm -rf build dist

# Build
echo -e "${BLUE}[..]${NC} Applicatie bouwen (dit kan 1-2 minuten duren)..."
python3 -m PyInstaller build_mac.spec --noconfirm

if [ ! -d "dist/Tijdregistratie.app" ]; then
    echo -e "${RED}[ERROR] Build mislukt - geen .app gevonden${NC}"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Build succesvol!"

# Maak DMG voor makkelijke distributie
echo -e "${BLUE}[..]${NC} DMG maken..."

DMG_NAME="Tijdregistratie-macOS"
DMG_PATH="dist/${DMG_NAME}.dmg"

# Verwijder oude DMG
rm -f "$DMG_PATH"

# Maak tijdelijke folder voor DMG inhoud
DMG_TEMP="dist/dmg_temp"
rm -rf "$DMG_TEMP"
mkdir -p "$DMG_TEMP"

# Kopieer app
cp -R "dist/Tijdregistratie.app" "$DMG_TEMP/"

# Maak symlink naar Applications
ln -s /Applications "$DMG_TEMP/Applications"

# Maak DMG
hdiutil create -volname "Tijdregistratie" -srcfolder "$DMG_TEMP" -ov -format UDZO "$DMG_PATH"

# Cleanup
rm -rf "$DMG_TEMP"

echo -e "${GREEN}[OK]${NC} DMG gemaakt: $DMG_PATH"

# Maak ook een ZIP
echo -e "${BLUE}[..]${NC} ZIP maken..."
cd dist
zip -r "${DMG_NAME}.zip" "Tijdregistratie.app"
cd ..
echo -e "${GREEN}[OK]${NC} ZIP gemaakt: dist/${DMG_NAME}.zip"

# Toon resultaat
echo ""
echo "  ======================================"
echo "    BUILD VOLTOOID!"
echo "  ======================================"
echo ""
echo "  Bestanden in dist/:"
ls -lh dist/*.dmg dist/*.zip dist/*.app 2>/dev/null | awk '{print "    " $9 " (" $5 ")"}'
echo ""
echo "  Volgende stappen:"
echo "  1. Test de app: open dist/Tijdregistratie.app"
echo "  2. Upload DMG of ZIP naar GitHub Releases"
echo ""
