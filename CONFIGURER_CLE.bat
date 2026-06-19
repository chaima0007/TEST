@echo off
echo ============================================
echo   CONFIGURATION CLE GEMINI — Caelum Partners
echo ============================================
echo.
echo Ta cle API se trouve sur : aistudio.google.com
echo Rubrique : Get API Key
echo.
set /p CLE="Colle ta cle Gemini ici et appuie sur Entree : "
echo.
setx GEMINI_API_KEY "%CLE%"
echo.
echo ============================================
echo   CLE ENREGISTREE DEFINITIVEMENT !
echo   Ferme ce CMD et relance DEMARRER.bat
echo ============================================
pause
