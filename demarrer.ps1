# ════════════════════════════════════════════════════════════
# CAELUM PARTNERS — Lanceur PowerShell
# Usage : .\demarrer.ps1
# ════════════════════════════════════════════════════════════

$Host.UI.RawUI.WindowTitle = "Caelum Partners — Bras Droit IA"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "  ╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║       CAELUM PARTNERS — BRAS DROIT IA           ║" -ForegroundColor Cyan
Write-Host "  ║       contact@caelumpartners.agency              ║" -ForegroundColor Cyan
Write-Host "  ╚══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Vérifier Python ──────────────────────────────────────────
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✅ Python détecté : $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python non trouvé." -ForegroundColor Red
    Write-Host "  Télécharge-le sur : https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  Coche 'Add Python to PATH' pendant l'installation." -ForegroundColor Yellow
    Read-Host "  [Entrée pour quitter]"
    exit 1
}

# ── Vérifier / Demander la clé API ───────────────────────────
if (-not $env:GEMINI_API_KEY) {
    Write-Host ""
    Write-Host "  ⚠️  Clé API Gemini manquante." -ForegroundColor Yellow
    Write-Host "  Récupère-la sur : https://aistudio.google.com" -ForegroundColor Yellow
    Write-Host ""
    $apiKey = Read-Host "  Entre ta clé API Gemini"

    if ([string]::IsNullOrWhiteSpace($apiKey)) {
        Write-Host "  ❌ Clé API obligatoire." -ForegroundColor Red
        Read-Host "  [Entrée pour quitter]"
        exit 1
    }

    $env:GEMINI_API_KEY = $apiKey

    # Proposer de la sauvegarder pour les prochaines fois
    Write-Host ""
    $sauvegarder = Read-Host "  Sauvegarder la clé pour ne plus la retaper ? (o/n)"
    if ($sauvegarder -eq "o" -or $sauvegarder -eq "O") {
        [System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", $apiKey, "User")
        Write-Host "  ✅ Clé sauvegardée — tu n'auras plus à la retaper." -ForegroundColor Green
    }
}

Write-Host "  ✅ Clé API : OK" -ForegroundColor Green

# ── Installer les dépendances ─────────────────────────────────
Write-Host ""
Write-Host "  Vérification des dépendances..." -ForegroundColor Gray

$check = python -c "import google.generativeai; print('ok')" 2>&1
if ($check -ne "ok") {
    Write-Host "  Installation de google-generativeai..." -ForegroundColor Yellow
    pip install google-generativeai --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ❌ Échec installation. Lance manuellement : pip install google-generativeai" -ForegroundColor Red
        Read-Host "  [Entrée pour quitter]"
        exit 1
    }
    Write-Host "  ✅ Installation réussie." -ForegroundColor Green
} else {
    Write-Host "  ✅ Dépendances OK." -ForegroundColor Green
}

# ── Lancer le menu principal ──────────────────────────────────
Write-Host ""
Write-Host "  Lancement du Bras Droit IA..." -ForegroundColor Cyan
Write-Host ""

python lancer.py

Write-Host ""
Write-Host "  Session terminée. À bientôt !" -ForegroundColor Cyan
Read-Host "  [Entrée pour fermer]"
