@echo off
title Tijdregistratie Installer
color 0A

echo.
echo  ======================================
echo    TIJDREGISTRATIE INSTALLER
echo  ======================================
echo.

:: Check of Node.js geinstalleerd is
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] Node.js is niet geinstalleerd.
    echo.
    echo     Download Node.js van: https://nodejs.org
    echo     Kies de LTS versie en installeer deze.
    echo     Start daarna dit script opnieuw.
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js gevonden
for /f "tokens=*" %%i in ('node -v') do echo     Versie: %%i
echo.

:: Ga naar project directory
cd /d "%~dp0.."

echo [..] Dependencies installeren...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [!] Fout bij installeren dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies geinstalleerd
echo.

echo [..] Desktop applicatie bouwen...
call npm run build:win
if %ERRORLEVEL% NEQ 0 (
    echo [!] Fout bij bouwen applicatie
    pause
    exit /b 1
)
echo [OK] Applicatie gebouwd
echo.

echo  ======================================
echo    INSTALLATIE VOLTOOID!
echo  ======================================
echo.
echo  De installer vind je in: dist\
echo.
echo  - Tijdregistratie Setup.exe  (installer)
echo  - Tijdregistratie.exe        (portable)
echo.
echo  Dubbelklik op een van deze bestanden
echo  om de applicatie te starten.
echo.

:: Open dist folder
explorer dist

pause
