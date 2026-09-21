@echo off
REM ============================================================
REM  ATLAS — apprendre : reconstruit l'IA locale "atlas-memoire"
REM  = memoire du depot (telechargee) + TES notes locales.
REM  Tes notes restent sur TA machine. Rien n'est envoye nulle part.
REM  Usage : double-clic, ou dans l'Invite de commandes :
REM          %USERPROFILE%\atlas-apprendre.bat
REM ============================================================
setlocal EnableExtensions
chcp 65001 >nul
set "BASE=%USERPROFILE%\ATLAS"
set "CORPUS=%BASE%\corpus"
set "TETE=%BASE%\memoire-depot.txt"
set "SORTIE=%BASE%\atlas-memoire-local.Modelfile"
set "URL=https://raw.githubusercontent.com/chaima0007/TEST/claude/nifty-shannon-u87dv8/codex/atlas/memoire/atlas-memoire.tete.txt"

if not exist "%CORPUS%" mkdir "%CORPUS%"

echo.
echo [1/4] Telechargement de la memoire du depot...
curl -L -f -s -S -o "%TETE%" "%URL%"
if errorlevel 1 (
  echo ECHEC du telechargement. Verifie ta connexion, puis relance.
  pause
  exit /b 1
)

echo [2/4] Lecture de tes notes locales dans %CORPUS%
set /a TOTAL=0
set /a N=0
for %%F in ("%CORPUS%\*.md" "%CORPUS%\*.txt") do (
  set /a TOTAL+=%%~zF
  set /a N+=1
  echo    - %%~nxF
)
if %N%==0 echo    ^(aucune note pour l'instant : mets des fichiers .md ou .txt dans ce dossier^)

echo [3/4] Construction du modele ^(%N% notes, %TOTAL% octets^)...
if %TOTAL% GTR 30000 (
  echo    ATTENTION : plus de 30000 octets de notes. Le modele peut en oublier une partie.
  echo    Marque les anciennes [PERIME] et deplace-les dans un sous-dossier "archive".
)
> "%SORTIE%" (
  type "%TETE%"
  echo =====
  echo NOTES LOCALES DE CHAIMA ^(dossier corpus sur sa machine, une note = un fichier date^)
  echo Ces notes font partie de la memoire : tu peux les citer, en nommant le fichier.
  for %%F in ("%CORPUS%\*.md" "%CORPUS%\*.txt") do (
    echo.
    echo --- NOTE : %%~nxF ---
    type "%%F"
    echo.
  )
  echo =====
  echo Fin de la memoire. Tout ce qui n'est pas ci-dessus : "Ce n'est pas dans ma memoire."
  echo """
)

ollama create atlas-memoire -f "%SORTIE%"
if errorlevel 1 (
  echo ECHEC de ollama create. Ollama est-il lance ? Envoie une capture a ATLAS.
  pause
  exit /b 1
)

echo [4/4] Termine. Ton IA locale connait maintenant le depot + %N% note^(s^).
echo        Elle demarre. La 1re reponse est lente ^(elle relit toute la memoire^), les suivantes sont rapides.
echo        Pour sortir : /bye
echo.
ollama run atlas-memoire
