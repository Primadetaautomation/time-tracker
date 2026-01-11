#!/bin/bash

# Kleuren
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

clear
echo ""
echo "  ======================================"
echo "    TIJDREGISTRATIE INSTALLER"
echo "  ======================================"
echo ""

# Ga naar project directory
cd "$(dirname "$0")/.."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}[!] Node.js is niet geïnstalleerd.${NC}"
    echo ""
    echo "    Installeer via Homebrew:"
    echo "    brew install node"
    echo ""
    echo "    Of download van: https://nodejs.org"
    echo ""
    read -p "Druk op Enter om af te sluiten..."
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Node.js gevonden"
echo "     Versie: $(node -v)"
echo ""

# Installeer dependencies
echo -e "${BLUE}[..]${NC} Dependencies installeren..."
npm install
if [ $? -ne 0 ]; then
    echo -e "${RED}[!] Fout bij installeren dependencies${NC}"
    read -p "Druk op Enter om af te sluiten..."
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Dependencies geïnstalleerd"
echo ""

# Bouw de app
echo -e "${BLUE}[..]${NC} Desktop applicatie bouwen..."
npm run build:mac
if [ $? -ne 0 ]; then
    echo -e "${RED}[!] Fout bij bouwen applicatie${NC}"
    read -p "Druk op Enter om af te sluiten..."
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Applicatie gebouwd"
echo ""

echo "  ======================================"
echo "    INSTALLATIE VOLTOOID!"
echo "  ======================================"
echo ""
echo "  De app vind je in: dist/"
echo ""
echo "  - Tijdregistratie.dmg"
echo ""
echo "  Open de .dmg en sleep de app naar"
echo "  je Applications folder."
echo ""

# Open dist folder
open dist

read -p "Druk op Enter om af te sluiten..."
