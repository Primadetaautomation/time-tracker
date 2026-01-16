# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec voor macOS
Bouwt een standalone .app bundle die gebruikers kunnen downloaden en direct gebruiken.
"""

from PyInstaller.utils.hooks import collect_all, collect_data_files
import sys
import os

# Bepaal of we op macOS draaien
is_macos = sys.platform == 'darwin'

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

# macOS specifieke imports
if is_macos:
    hiddenimports += [
        'AppKit',
        'Foundation',
        'Quartz',
        'Cocoa',
        'objc',
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
    runtime_hooks=['runtime_hook_macos.py'],  # macOS 26+ Tk fix
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

# Executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Tijdregistratie',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Geen terminal venster
    disable_windowed_traceback=False,
    argv_emulation=False,  # Disable - veroorzaakt Tk_CreateConsoleWindow crash op macOS 26
    target_arch=None,  # Universal binary indien mogelijk
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.icns' if os.path.exists('assets/icon.icns') else None,
)

# Verzamel alle bestanden
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Tijdregistratie',
)

# macOS App Bundle
app = BUNDLE(
    coll,
    name='Tijdregistratie.app',
    icon='assets/icon.icns' if os.path.exists('assets/icon.icns') else None,
    bundle_identifier='com.primadata.tijdregistratie',
    info_plist={
        'CFBundleName': 'Tijdregistratie',
        'CFBundleDisplayName': 'Tijdregistratie',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'NSAppleEventsUsageDescription': 'Tijdregistratie heeft toegang nodig tot andere apps om activiteit te tracken.',
        'NSAccessibilityUsageDescription': 'Tijdregistratie heeft Toegankelijkheid nodig om venster informatie te lezen.',
        'LSMinimumSystemVersion': '10.15',
        'LSApplicationCategoryType': 'public.app-category.productivity',
    },
)
