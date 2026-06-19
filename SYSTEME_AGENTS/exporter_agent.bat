@echo off
chcp 65001 >nul
title Caelum Partners — Export Agent Souverain

echo.
echo  ══════════════════════════════════════════════════
echo    SYSTÈME AGENTS SOUVERAIN — Caelum Partners
echo    Export vers presse-papiers ou fichier
echo  ══════════════════════════════════════════════════
echo.
echo  Agents disponibles :
echo  01 Orchestrateur   02 Commercial     03 Veille
echo  04 Facturation     05 Recrutement    06 Professeur
echo  07 Migration       08 Securite       09 Reference
echo  10 Juridique       11 Support Client 12 Chef Projet
echo  13 Guide           14 Watchdog       15 Fantome
echo  16 Commandant      17 Resolveur      18 CRM
echo  19 Email           20 Dashboard CEO  21 Memoire
echo  22 Autopilot       23 Growth         24 Empire
echo  25 TITAN           INDEX (tous)
echo.
set /p CHOIX="  Numero de l'agent (ex: 13) ou INDEX → "

if "%CHOIX%"=="INDEX" goto :export_index

:: Trouver le fichier correspondant
for %%f in (%~dp0%CHOIX%_*.md) do (
    echo.
    echo  ✅ Agent trouve : %%f
    echo.
    echo  [1] Afficher dans le terminal
    echo  [2] Copier dans presse-papiers
    echo  [3] Sauvegarder dans un nouveau fichier
    echo.
    set /p ACTION="  Choix → "

    if "!ACTION!"=="1" (
        type "%%f"
    )
    if "!ACTION!"=="2" (
        type "%%f" | clip
        echo  ✅ Copie dans presse-papiers — colle dans Claude, Ollama ou ChatGPT
    )
    if "!ACTION!"=="3" (
        set /p DEST="  Nom du fichier destination → "
        copy "%%f" "!DEST!" >nul
        echo  ✅ Sauvegarde → !DEST!
    )
    goto :fin
)

echo  ❌ Agent %CHOIX% non trouve. Verifie le numero.
goto :fin

:export_index
type "%~dp0INDEX.md"
type "%~dp0INDEX.md" | clip
echo  ✅ Index copie dans presse-papiers

:fin
echo.
pause
