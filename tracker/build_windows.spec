# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec voor Windows
Bouwt een standalone .exe die gebruikers kunnen downloaden en direct gebruiken.
"""

from PyInstaller.utils.hooks import collect_all, collect_data_files
import sys
import os

# Verzamel alle customtkinter bestanden
datas = []
binaries = []
hiddenimports = [
    'customtkinter',
    'PIL',
    'PIL.Image',
    'psutil',
    'json',
    'csv',
    'threading',
]

# CustomTkinter data files
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# Pillow data files
tmp_ret = collect_all('PIL')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# Windows specifieke imports
hiddenimports += [
    'win32api',
    'win32con',
    'win32gui',
    'win32process',
    'pywintypes',
]

# Voeg de activity_tracker_enhanced.py toe als data
datas += [('activity_tracker_enhanced.py', '.')]

# Analyse
a = Analysis(
    ['desktop_app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'pytest',
        'IPython',
    ],
    noarchive=False,
    optimize=1,
)

# PYZ archief
pyz = PYZ(a.pure)

# Executable - onefile voor makkelijke distributie
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Tijdregistratie',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Geen terminal venster
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    version='assets/version_info.txt' if os.path.exists('assets/version_info.txt') else None,
)
