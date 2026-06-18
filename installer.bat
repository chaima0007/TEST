@echo off
chcp 65001 >nul
title Caelum Partners — Installation

echo.
echo  ══════════════════════════════════════════════════
echo    CAELUM PARTNERS — Installation des agents
echo  ══════════════════════════════════════════════════
echo.

:: ── Vérifier Python ──────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERREUR] Python manquant. Va sur https://www.python.org/downloads/
    echo  Coche "Add Python to PATH" pendant l'installation.
    pause
    exit /b 1
)
echo  [OK] Python installe

:: ── Installer google-genai (nouvelle API officielle) ──────
echo.
echo  Installation de google-genai...
pip install google-genai
if errorlevel 1 (
    echo  [ERREUR] Echec. Essaie : pip install --upgrade pip  puis relance.
    pause
    exit /b 1
)
echo.
echo  [OK] google-genai installe

:: ── Configurer la clé API ────────────────────────────────
echo.
echo  ══════════════════════════════════════════════════
echo    CONFIGURATION CLE API GEMINI
echo    Recupere ta cle sur : aistudio.google.com
echo    Menu : "Get API key" → copie la cle
echo  ══════════════════════════════════════════════════
echo.
set /p CLE="  Colle ta cle API Gemini ici → "

if "%CLE%"=="" (
    echo  [ERREUR] Cle vide. Relance et colle ta vraie cle.
    pause
    exit /b 1
)

:: Sauvegarder la clé pour l'utilisateur courant (permanente)
setx GEMINI_API_KEY "%CLE%"
echo.
echo  [OK] Cle sauvegardee definitivement

:: ── Vérifier que tout fonctionne ─────────────────────────
echo.
echo  Test de la cle API...
set GEMINI_API_KEY=%CLE%
python -c "from google import genai; c=genai.Client(api_key='%CLE%'); print('[OK] Connexion Gemini reussie')" 2>nul
if errorlevel 1 (
    echo  [ATTENTION] Test echoue. Verifie que ta cle est correcte.
    echo  Retourne sur aistudio.google.com et copie la vraie cle.
)

echo.
echo  ══════════════════════════════════════════════════
echo    INSTALLATION TERMINEE !
echo    Lance maintenant : demarrer.bat
echo    Ou double-clique sur demarrer.bat
echo  ══════════════════════════════════════════════════
echo.
pause
