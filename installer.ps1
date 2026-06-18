# ════════════════════════════════════════════════════════════
# CAELUM PARTNERS — Installateur PowerShell
# Clic droit → "Exécuter avec PowerShell"
# ════════════════════════════════════════════════════════════

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "Caelum Partners — Installation"

Write-Host ""
Write-Host "  ══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "    CAELUM PARTNERS — Installation complète" -ForegroundColor Cyan
Write-Host "  ══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ── Autoriser l'exécution des scripts PowerShell ─────────────
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq "Restricted") {
    Write-Host "  Configuration de la politique d'exécution..." -ForegroundColor Yellow
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "  ✅ Politique mise à jour." -ForegroundColor Green
}

# ── Vérifier Python ──────────────────────────────────────────
Write-Host "  Vérification Python..." -ForegroundColor Gray
try {
    $ver = python --version 2>&1
    Write-Host "  ✅ $ver" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python non installé." -ForegroundColor Red
    Write-Host ""
    Write-Host "  1. Va sur https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  2. Télécharge la version Windows" -ForegroundColor Yellow
    Write-Host "  3. IMPORTANT : coche 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host "  4. Relance ce script après installation" -ForegroundColor Yellow
    Read-Host "  [Entrée pour quitter]"
    exit 1
}

# ── Installer google-generativeai ─────────────────────────────
Write-Host ""
Write-Host "  Installation de google-generativeai..." -ForegroundColor Yellow
pip install google-generativeai --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Échec. Essaie : pip install --upgrade pip" -ForegroundColor Red
    Read-Host "[Entrée pour quitter]"
    exit 1
}
Write-Host "  ✅ google-generativeai installé." -ForegroundColor Green

# ── Configurer la clé API ─────────────────────────────────────
Write-Host ""
Write-Host "  ══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "    CONFIGURATION CLÉ API GEMINI" -ForegroundColor Cyan
Write-Host "    1. Va sur : https://aistudio.google.com" -ForegroundColor Yellow
Write-Host "    2. Clique 'Get API key' → 'Create API key'" -ForegroundColor Yellow
Write-Host "    3. Copie la clé (commence par AIza...)" -ForegroundColor Yellow
Write-Host "    4. Colle-la ici avec clic droit" -ForegroundColor Yellow
Write-Host "  ══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$cle = Read-Host "  Colle ta clé API Gemini ici"

if ([string]::IsNullOrWhiteSpace($cle)) {
    Write-Host "  ❌ Clé vide. Relance et colle ta vraie clé." -ForegroundColor Red
    Read-Host "  [Entrée pour quitter]"
    exit 1
}

# Sauvegarder définitivement pour l'utilisateur
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", $cle, "User")
$env:GEMINI_API_KEY = $cle
Write-Host "  ✅ Clé sauvegardée définitivement." -ForegroundColor Green

# ── Tester la connexion ───────────────────────────────────────
Write-Host ""
Write-Host "  Test de la connexion Gemini..." -ForegroundColor Gray
$test = python -c "
import google.generativeai as g
g.configure(api_key='$cle')
print('OK')
" 2>&1

if ($test -eq "OK") {
    Write-Host "  ✅ Connexion Gemini réussie !" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Test échoué. Vérifie ta clé sur aistudio.google.com" -ForegroundColor Yellow
}

# ── Fin ───────────────────────────────────────────────────────
Write-Host ""
Write-Host "  ══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "    ✅ INSTALLATION TERMINÉE !" -ForegroundColor Green
Write-Host "    Lance maintenant : demarrer.ps1" -ForegroundColor Cyan
Write-Host "    Ou double-clique sur : demarrer.bat" -ForegroundColor Cyan
Write-Host "  ══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Read-Host "  [Entrée pour fermer]"
