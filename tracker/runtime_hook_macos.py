"""
PyInstaller runtime hook for macOS 26+ Tk compatibility.
This runs BEFORE the main script to fix Tk menu crashes.
"""
import sys
import os

if sys.platform == 'darwin':
    # Voorkom Tk console window crash
    os.environ['TK_SILENCE_DEPRECATION'] = '1'

    # Force Tk to skip menu initialization that crashes on macOS 26+
    # Dit werkt door de Tcl library path aan te passen
    if hasattr(sys, '_MEIPASS'):
        # We draaien in een PyInstaller bundle
        # Zet TCL/TK library paden
        tcl_path = os.path.join(sys._MEIPASS, 'tcl')
        tk_path = os.path.join(sys._MEIPASS, 'tk')

        if os.path.exists(tcl_path):
            os.environ['TCL_LIBRARY'] = tcl_path
        if os.path.exists(tk_path):
            os.environ['TK_LIBRARY'] = tk_path

        # Voorkom dat Tk een console window probeert te maken
        # Dit is de root cause van de crash
        os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
