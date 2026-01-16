"""
PyInstaller runtime hook for macOS 26+ Tk compatibility.
This runs BEFORE the main script to fix Tk menu crashes.

The crash occurs in Tk_CreateConsoleWindow -> tkSetMainMenu -> NSMenuItem
when macOS 26 validates keyEquivalent strings more strictly.
"""
import sys
import os

if sys.platform == 'darwin':
    # Silence Tk deprecation warnings
    os.environ['TK_SILENCE_DEPRECATION'] = '1'

    # Prevent Tk from trying to create console window
    # This is the root cause of the menu crash on macOS 26+
    os.environ['TK_CONSOLE'] = '0'

    # Don't write bytecode
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

    if hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle
        # Set TCL/TK library paths
        tcl_path = os.path.join(sys._MEIPASS, 'tcl')
        tk_path = os.path.join(sys._MEIPASS, 'tk')

        if os.path.exists(tcl_path):
            os.environ['TCL_LIBRARY'] = tcl_path
        if os.path.exists(tk_path):
            os.environ['TK_LIBRARY'] = tk_path
