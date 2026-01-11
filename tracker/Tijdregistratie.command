#!/bin/bash
# Tijdregistratie Desktop App
# Dubbelklik om te starten

cd "$(dirname "$0")"

# Check dependencies
python3 -c "import customtkinter" 2>/dev/null || {
    echo "Installing dependencies..."
    pip3 install customtkinter pillow
}

# Start de app
python3 desktop_app.py
