#!/bin/bash
# ===========================================
#   BEKIJK JE GEWERKTE UREN
# ===========================================

cd "$(dirname "$0")"

echo ""
echo "  =========================================="
echo "    OVERZICHT GEWERKTE UREN"
echo "  =========================================="

python3 activity_tracker.py summary

echo ""
echo ""
read -p "Druk Enter om af te sluiten..."
