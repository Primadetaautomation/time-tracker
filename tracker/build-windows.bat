@echo off
REM =============================================================================
REM Build script voor Windows
REM Maakt een standalone Tijdregistratie.exe
REM =============================================================================

echo.
echo   ======================================
echo     TIJDREGISTRATIE - Windows BUILD
echo   ======================================
echo.

REM Ga naar script directory
cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is niet geinstalleerd
    echo Download van: https://python.org
    pause
    exit /b 1
)
echo [OK] Python gevonden

REM Check/installeer PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [..] PyInstaller installeren...
    pip install pyinstaller
)
echo [OK] PyInstaller beschikbaar

REM Installeer dependencies
echo [..] Dependencies installeren...
pip install customtkinter pillow psutil pywin32 --quiet
echo [OK] Dependencies geinstalleerd

REM Clean vorige build
echo [..] Opruimen vorige build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build
echo [..] Applicatie bouwen (dit kan 1-2 minuten duren)...
python -m PyInstaller build_windows.spec --noconfirm

if not exist "dist\Tijdregistratie.exe" (
    echo [ERROR] Build mislukt - geen .exe gevonden
    pause
    exit /b 1
)

echo [OK] Build succesvol!

REM Toon resultaat
echo.
echo   ======================================
echo     BUILD VOLTOOID!
echo   ======================================
echo.
echo   Bestand: dist\Tijdregistratie.exe
echo.
dir /b dist\*.exe
echo.
echo   Volgende stappen:
echo   1. Test de app: dist\Tijdregistratie.exe
echo   2. Upload naar GitHub Releases
echo.
pause
