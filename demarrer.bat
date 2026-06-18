@echo off
chcp 65001 >nul
title Caelum Partners — Bras Droit IA

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║       CAELUM PARTNERS — BRAS DROIT IA           ║
echo  ║       contact@caelumpartners.agency              ║
echo  ╚══════════════════════════════════════════════════╝
echo.

:: ── Vérifier Python ──────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERREUR] Python n'est pas installe.
    echo  Telecharge-le sur : https://www.python.org/downloads/
    echo  Coche "Add Python to PATH" pendant l'installation.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo  Python detecte : %PYTHON_VER%

:: ── Vérifier la clé API ──────────────────────────────────
if "%GEMINI_API_KEY%"=="" (
    echo.
    echo  [ATTENTION] Cle API Gemini manquante.
    set /p GEMINI_API_KEY="  Entre ta cle API Gemini → "
    if "%GEMINI_API_KEY%"=="" (
        echo  [ERREUR] Cle API obligatoire. Recupere-la sur : aistudio.google.com
        pause
        exit /b 1
    )
)

echo  Cle API : OK

:: ── Installer les dépendances ────────────────────────────
echo.
echo  Verification des dependances...
python -c "import google.generativeai" >nul 2>&1
if errorlevel 1 (
    echo  Installation de google-generativeai...
    pip install google-generativeai --quiet
    if errorlevel 1 (
        echo  [ERREUR] Echec installation. Lance : pip install google-generativeai
        pause
        exit /b 1
    )
    echo  Installation reussie.
) else (
    echo  Dependances OK.
)

:: ── Lancer le menu principal ─────────────────────────────
echo.
echo  Lancement en cours...
echo.
python lancer.py

echo.
echo  Session terminee. A bientot !
pause
