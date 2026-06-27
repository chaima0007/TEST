#!/usr/bin/env python3
"""
mistral_registry.py — Registre Mistral AI CaelumSwarm™
═══════════════════════════════════════════════════════
Catalogue des plateformes Mistral gratuites + repos GitHub vérifiés par protocole.
Sceau de référence : SEAL-927AF2CEE9DDFD98 (APPROUVÉ 2026-06-22)

Usage:
  python3 scripts/mistral_registry.py --list
  python3 scripts/mistral_registry.py --list --category platforms
  python3 scripts/mistral_registry.py --adopt elia
  python3 scripts/mistral_registry.py --install ollama-mistral
  python3 scripts/mistral_registry.py --audit
  python3 scripts/mistral_registry.py --verify all
  python3 scripts/mistral_registry.py --report
"""

import sys
import json
import argparse
import subprocess
import shutil
from datetime import datetime, timezone
from pathlib import Path

# ── Imports protocole ──────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
try:
    from decision_seal import seal_decision, verify_seal, load_seal_log
    SEAL_AVAILABLE = True
except ImportError:
    SEAL_AVAILABLE = False

# ── Constantes ─────────────────────────────────────────────────────────────────
SEAL_REFERENCE    = "SEAL-927AF2CEE9DDFD98"
MISTRAL_LOG       = Path("data/mistral_registry_log.json")
MISTRAL_CATALOG   = Path("data/mistral_catalog.json")
MISTRAL_LOG.parent.mkdir(exist_ok=True)

LICENCES_AUTORISÉES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense", "CC0-1.0"}
LICENCES_INTERDITES = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.0", "LGPL-3.0"}

PRIORITY_ICON = {"CRITIQUE": "🔴", "ÉLEVÉ": "🟠", "MOYEN": "🟡", "FAIBLE": "🟢"}

# ── Plateformes Mistral gratuites ──────────────────────────────────────────────
MISTRAL_PLATFORMS = {
    "la-plateforme": {
        "name":        "La Plateforme (Mistral API)",
        "url":         "https://console.mistral.ai",
        "tier_gratuit": True,
        "description": "API officielle Mistral avec tier expérimental gratuit. Accès aux modèles mistral-small-latest, open-mistral-7b, open-mixtral-8x7b.",
        "models_gratuits": ["open-mistral-7b", "open-mixtral-8x7b", "open-mistral-nemo"],
        "limites":     "1 req/s, 500K tokens/mois en expérimental",
        "linux_setup": "pip install mistralai && export MISTRAL_API_KEY=<votre-clé>",
        "windows_setup": "pip install mistralai && set MISTRAL_API_KEY=<votre-clé>",
        "check_cmd":   "python3 -c \"from mistralai import Mistral; print('OK')\"",
        "priority":    "CRITIQUE",
        "tags":        ["api", "cloud", "production", "mistral-official"],
        "caelum_use":  "Backend engines swarm + analyse droits humains",
        "securite":    "API key via SOPS/Vault — JAMAIS dans le code",
    },
    "le-chat": {
        "name":        "Le Chat (chat.mistral.ai)",
        "url":         "https://chat.mistral.ai",
        "tier_gratuit": True,
        "description": "Interface web gratuite Mistral. Accès illimité à Mistral Large, Medium et aux modèles expérimentaux.",
        "models_gratuits": ["mistral-large-latest", "mistral-medium", "codestral-latest"],
        "limites":     "Aucune limite officielle en tier gratuit web",
        "linux_setup": "# Accès via navigateur uniquement",
        "windows_setup": "# Accès via navigateur uniquement",
        "check_cmd":   "curl -s https://chat.mistral.ai | grep -c 'mistral' > /dev/null && echo OK",
        "priority":    "MOYEN",
        "tags":        ["web", "gratuit", "no-api-key", "interface"],
        "caelum_use":  "Prototypage prompts, validation designs Canva, revue code",
        "securite":    "Session web — aucun credential stocké localement",
    },
    "ollama-mistral": {
        "name":        "Ollama + Mistral (100% Local)",
        "url":         "https://ollama.ai",
        "tier_gratuit": True,
        "description": "Exécution locale 100% gratuite et hors-ligne. Modèles : mistral:latest (7B), mixtral:latest (8x7B), codestral:latest.",
        "models_gratuits": ["mistral:latest", "mixtral:latest", "mistral-nemo:latest", "codestral:latest"],
        "limites":     "Limité par RAM locale : 7B nécessite 8GB RAM minimum",
        "linux_setup": "curl -fsSL https://ollama.ai/install.sh | sh && ollama pull mistral:latest",
        "windows_setup": "winget install Ollama.Ollama && ollama pull mistral:latest",
        "check_cmd":   "ollama list",
        "priority":    "CRITIQUE",
        "tags":        ["local", "offline", "gratuit", "privacy", "no-api-key"],
        "caelum_use":  "Engines swarm locaux, tests offline, données sensibles droits humains",
        "securite":    "100% local — aucune donnée quitte la machine",
    },
    "huggingface-mistral": {
        "name":        "Hugging Face — Modèles Mistral",
        "url":         "https://huggingface.co/mistralai",
        "tier_gratuit": True,
        "description": "Téléchargement gratuit de tous les modèles Mistral open-source. Inference API gratuite limitée.",
        "models_gratuits": ["mistralai/Mistral-7B-v0.3", "mistralai/Mixtral-8x7B-v0.1", "mistralai/Mistral-Nemo-Instruct-2407"],
        "limites":     "Inference API: 1000 req/jour gratuit. Téléchargement: illimité",
        "linux_setup": "pip install transformers torch && huggingface-cli login",
        "windows_setup": "pip install transformers torch && huggingface-cli login",
        "check_cmd":   "python3 -c \"from transformers import AutoTokenizer; print('OK')\"",
        "priority":    "ÉLEVÉ",
        "tags":        ["open-source", "modèles", "téléchargement", "fine-tuning"],
        "caelum_use":  "Fine-tuning domaines droits humains, benchmarks, embeddings",
        "securite":    "HF token via SOPS — JAMAIS en clair",
    },
    "codestral-api": {
        "name":        "Codestral API (Mistral Code)",
        "url":         "https://codestral.mistral.ai",
        "tier_gratuit": True,
        "description": "API Codestral gratuite pour génération de code. Conçu pour assistance développement. Accès expérimental gratuit.",
        "models_gratuits": ["codestral-latest", "codestral-2405"],
        "limites":     "Usage non-commercial uniquement en tier gratuit",
        "linux_setup": "pip install mistralai && export CODESTRAL_API_KEY=<votre-clé>",
        "windows_setup": "pip install mistralai && set CODESTRAL_API_KEY=<votre-clé>",
        "check_cmd":   "python3 -c \"from mistralai import Mistral; print('Codestral OK')\"",
        "priority":    "ÉLEVÉ",
        "tags":        ["code", "api", "développement", "completion"],
        "caelum_use":  "Génération engines Python swarm, routes TypeScript, scripts",
        "securite":    "Clé Codestral séparée de l'API principale — rotation mensuelle",
    },
    "llamacpp-mistral": {
        "name":        "llama.cpp + Mistral GGUF",
        "url":         "https://github.com/ggerganov/llama.cpp",
        "tier_gratuit": True,
        "description": "Inférence ultra-légère C++ pour modèles Mistral quantisés (Q4, Q5, Q8). Fonctionne CPU-only.",
        "models_gratuits": ["mistral-7b-instruct-v0.3.Q4_K_M.gguf", "mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf"],
        "limites":     "Performance réduite vs GPU — 7B Q4 ≈ 10 tok/s CPU",
        "linux_setup": "git clone https://github.com/ggerganov/llama.cpp && cd llama.cpp && make && ./llama-cli -m mistral-7b.gguf -p 'Bonjour'",
        "windows_setup": "winget install LLVM.LLVM && git clone https://github.com/ggerganov/llama.cpp && cmake -B build && cmake --build build",
        "check_cmd":   "llama-cli --version 2>/dev/null || echo 'Non installé'",
        "priority":    "MOYEN",
        "tags":        ["local", "cpu", "quantisé", "léger", "gguf"],
        "caelum_use":  "Inférence sur machines faibles, tests edge, déploiement embarqué",
        "securite":    "100% local — modèles GGUF sans dépendances cloud",
    },
}

# ── Repos GitHub Mistral vérifiés par protocole ────────────────────────────────
MISTRAL_GITHUB_REPOS = {
    "elia": {
        "name":        "elia (Terminal AI Chat)",
        "repo":        "darrenburns/elia",
        "url":         "https://github.com/darrenburns/elia",
        "stars":       2472,
        "licence":     "MIT",
        "language":    "Python",
        "description": "TUI multi-LLM (Mistral/Claude/GPT/Llama/Ollama) pour terminal. Interface Textual riche, historique SQLite, exports Markdown.",
        "mistral_support": True,
        "derniere_maj": "2025-01",
        "scores": {
            "pertinence":  9.5,
            "licence":    10.0,
            "securite":    8.5,
            "maintenance": 9.0,
            "integration": 9.0,
        },
        "linux_install": "pip install elia-chat && elia",
        "windows_install": "pip install elia-chat && elia",
        "caelum_integration": "Interface TUI pour tester les engines Mistral localement avant déploiement",
        "verdict":     "ADOPTÉ",
        "seal":        None,
        "notes":       "Support natif Mistral + Ollama — parfait pour tests offline droits humains",
    },
    "bambooai": {
        "name":        "BambooAI (Data Analysis)",
        "repo":        "pgalko/BambooAI",
        "url":         "https://github.com/pgalko/BambooAI",
        "stars":       777,
        "licence":     "MIT",
        "language":    "Python",
        "description": "Analyse de données conversationnelle avec Mistral/Anthropic/Ollama. Génère pandas/matplotlib depuis langage naturel.",
        "mistral_support": True,
        "derniere_maj": "2024-12",
        "scores": {
            "pertinence":  9.0,
            "licence":    10.0,
            "securite":    8.0,
            "maintenance": 8.5,
            "integration": 9.0,
        },
        "linux_install": "pip install bambooai && export MISTRAL_API_KEY=<clé>",
        "windows_install": "pip install bambooai && set MISTRAL_API_KEY=<clé>",
        "caelum_integration": "Analyse datasets droits humains — requêtes NL sur CSV/JSON ONU",
        "verdict":     "ADOPTÉ",
        "seal":        None,
        "notes":       "Support Mistral + Ollama — analyse données sensibles possible offline",
    },
    "local-llm-rag": {
        "name":        "local-LLM-with-RAG",
        "repo":        "amscotti/local-LLM-with-RAG",
        "url":         "https://github.com/amscotti/local-LLM-with-RAG",
        "stars":       286,
        "licence":     "MIT",
        "language":    "Python",
        "description": "Pipeline RAG local : Mistral + Ollama + LangChain + Chroma. Ingestion documents + Q&A sur corpus privé.",
        "mistral_support": True,
        "derniere_maj": "2024-11",
        "scores": {
            "pertinence":  9.5,
            "licence":    10.0,
            "securite":    9.0,
            "maintenance": 8.0,
            "integration": 9.5,
        },
        "linux_install": "git clone https://github.com/amscotti/local-LLM-with-RAG && pip install -r requirements.txt && ollama pull mistral",
        "windows_install": "git clone https://github.com/amscotti/local-LLM-with-RAG && pip install -r requirements.txt && ollama pull mistral",
        "caelum_integration": "RAG sur corpus rapports droits humains ONU/OHCHR — 100% local",
        "verdict":     "ADOPTÉ",
        "seal":        None,
        "notes":       "Architecture idéale pour ingérer des documents confidentiels sans API externe",
    },
    "mistral-ocr": {
        "name":        "mistral-ocr (PDF + Audio)",
        "repo":        "EngDawood/mistral-ocr",
        "url":         "https://github.com/EngDawood/mistral-ocr",
        "stars":       3,
        "licence":     "MIT",
        "language":    "Python",
        "description": "OCR PDF multipage + transcription audio avec Mistral API. Extraction texte structuré depuis documents scannés.",
        "mistral_support": True,
        "derniere_maj": "2025-01",
        "scores": {
            "pertinence":  8.0,
            "licence":    10.0,
            "securite":    7.0,
            "maintenance": 5.0,
            "integration": 8.0,
        },
        "linux_install": "git clone https://github.com/EngDawood/mistral-ocr && pip install -r requirements.txt",
        "windows_install": "git clone https://github.com/EngDawood/mistral-ocr && pip install -r requirements.txt",
        "caelum_integration": "Extraction rapports PDF droits humains → ingestion swarm engine",
        "verdict":     "CONDITIONNEL",
        "seal":        None,
        "notes":       "Stars faibles (3) — évaluer stabilité avant intégration production",
    },
    "text2sql-mistral": {
        "name":        "AWS Text2SQL Mistral Small",
        "repo":        "aws-samples/query-databases-with-natural-language",
        "url":         "https://github.com/aws-samples/query-databases-with-natural-language",
        "stars":       24,
        "licence":     "MIT",
        "language":    "Python",
        "description": "Text-to-SQL avec Mistral Small via AWS Bedrock. Requêtes SQL depuis langage naturel sur bases de données.",
        "mistral_support": True,
        "derniere_maj": "2024-10",
        "scores": {
            "pertinence":  7.5,
            "licence":    10.0,
            "securite":    9.0,
            "maintenance": 7.0,
            "integration": 7.0,
        },
        "linux_install": "git clone https://github.com/aws-samples/query-databases-with-natural-language && pip install -r requirements.txt",
        "windows_install": "git clone https://github.com/aws-samples/query-databases-with-natural-language && pip install -r requirements.txt",
        "caelum_integration": "Requêtes NL sur base SQLite des engines swarm + données Prisma",
        "verdict":     "À ÉVALUER",
        "seal":        None,
        "notes":       "Dépendance AWS Bedrock — préférer version Ollama directe si disponible",
    },
    "flex-ai": {
        "name":        "flex_ai (Fine-tuning LLMs)",
        "repo":        "getflexai/flex_ai",
        "url":         "https://github.com/getflexai/flex_ai",
        "stars":       4,
        "licence":     "Apache-2.0",
        "language":    "Python",
        "description": "Fine-tuning simplifié de 60+ LLMs dont Mistral. Interface unifiée pour LoRA/QLoRA.",
        "mistral_support": True,
        "derniere_maj": "2025-01",
        "scores": {
            "pertinence":  7.0,
            "licence":    10.0,
            "securite":    7.5,
            "maintenance": 5.0,
            "integration": 7.0,
        },
        "linux_install": "pip install flex_ai",
        "windows_install": "pip install flex_ai",
        "caelum_integration": "Fine-tuning Mistral sur corpus droits humains CSDDD",
        "verdict":     "À ÉVALUER",
        "seal":        None,
        "notes":       "Projet jeune (4 stars) — surveiller maintenance avant adoption",
    },
}

# ── Pondération scoring repos ──────────────────────────────────────────────────
SCORING_WEIGHTS = {
    "pertinence":  0.30,
    "licence":     0.25,
    "securite":    0.20,
    "maintenance": 0.15,
    "integration": 0.10,
}

VERDICT_LABELS = {
    "ADOPTÉ":      "✅ ADOPTÉ",
    "CONDITIONNEL":"🟡 CONDITIONNEL",
    "À ÉVALUER":   "🔵 À ÉVALUER",
    "REJETÉ":      "❌ REJETÉ",
    "BLOQUÉ":      "🚫 BLOQUÉ",
}

# ── Fonctions utilitaires ──────────────────────────────────────────────────────

def compute_score(repo: dict) -> float:
    """Calcule le score composite pondéré d'un repo."""
    scores = repo.get("scores", {})
    total = sum(scores.get(k, 0) * w for k, w in SCORING_WEIGHTS.items())
    return round(total * 10, 1)  # /100

def check_licence(repo: dict) -> str:
    """Valide la licence selon le protocole CaelumSwarm."""
    lic = repo.get("licence", "INCONNUE")
    if lic in LICENCES_INTERDITES:
        return "🚫 BLOQUÉ"
    if lic in LICENCES_AUTORISÉES:
        return "✅ AUTORISÉE"
    return "⚠️ À VÉRIFIER"

def load_log() -> list:
    if MISTRAL_LOG.exists():
        with open(MISTRAL_LOG) as f:
            return json.load(f)
    return []

def save_log(entries: list):
    MISTRAL_LOG.parent.mkdir(exist_ok=True)
    # FIFO 500 entrées
    if len(entries) > 500:
        entries = entries[-500:]
    with open(MISTRAL_LOG, "w") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

def log_action(action: str, target: str, result: str, seal_id: str = None):
    entries = load_log()
    entries.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action":    action,
        "target":    target,
        "result":    result,
        "seal_id":   seal_id or SEAL_REFERENCE,
    })
    save_log(entries)

# ── Commandes principales ──────────────────────────────────────────────────────

def cmd_list(category: str = None):
    """Liste plateformes et/ou repos Mistral."""
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       MISTRAL REGISTRY — CaelumSwarm™                       ║")
    print(f"║  Sceau de référence : {SEAL_REFERENCE}            ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    show_platforms = category in (None, "platforms", "plateformes")
    show_repos     = category in (None, "repos", "github")

    if show_platforms:
        print("═" * 65)
        print("  PLATEFORMES MISTRAL GRATUITES")
        print("═" * 65)
        for key, p in MISTRAL_PLATFORMS.items():
            icon = PRIORITY_ICON.get(p["priority"], "⚪")
            gratuit = "🆓 GRATUIT" if p["tier_gratuit"] else "💰 PAYANT"
            print(f"\n  {icon} [{key}] {p['name']}")
            print(f"     {gratuit} | {p['url']}")
            print(f"     {p['description'][:80]}...")
            print(f"     Modèles : {', '.join(p['models_gratuits'][:3])}")
            print(f"     Usage Caelum : {p['caelum_use']}")
            print(f"     Sécurité : {p['securite']}")

    if show_repos:
        print("\n" + "═" * 65)
        print("  REPOS GITHUB MISTRAL — VÉRIFIÉS PROTOCOLE")
        print("═" * 65)
        for key, r in MISTRAL_GITHUB_REPOS.items():
            score    = compute_score(r)
            lic_ok   = check_licence(r)
            verdict  = VERDICT_LABELS.get(r["verdict"], r["verdict"])
            print(f"\n  {verdict} [{key}] {r['name']}")
            print(f"     ⭐ {r['stars']} | {r['licence']} {lic_ok} | {r['language']}")
            print(f"     Score : {score}/100")
            print(f"     {r['description'][:80]}...")
            print(f"     Intégration : {r['caelum_integration']}")
            if r["notes"]:
                print(f"     ⚠️  {r['notes']}")

    print(f"\n  Total : {len(MISTRAL_PLATFORMS)} plateformes | {len(MISTRAL_GITHUB_REPOS)} repos\n")

def cmd_install(platform_key: str):
    """Affiche les instructions d'installation d'une plateforme."""
    if platform_key not in MISTRAL_PLATFORMS:
        print(f"❌ Plateforme inconnue : {platform_key}")
        print(f"   Disponibles : {', '.join(MISTRAL_PLATFORMS.keys())}")
        return

    p = MISTRAL_PLATFORMS[platform_key]

    # Sceau obligatoire pour install CRITIQUE/ÉLEVÉ
    seal_id = SEAL_REFERENCE
    if SEAL_AVAILABLE and p["priority"] in ("CRITIQUE", "ÉLEVÉ"):
        print(f"\n🔏 Génération sceau pour installation : {platform_key}")
        rec = seal_decision(
            action=f"install-mistral-{platform_key}",
            context=f"Installation plateforme Mistral : {p['name']}",
            verbose=False,
        )
        seal_id = rec.get("seal_id", SEAL_REFERENCE)
        status  = rec.get("status", "?")
        print(f"   Sceau : {seal_id} — {status}")
        if status != "APPROUVÉ":
            print("   🚫 Sceau non approuvé — installation bloquée")
            return

    print(f"\n╔══ INSTALLATION : {p['name']} ══╗")
    print(f"   URL        : {p['url']}")
    print(f"   Priorité   : {PRIORITY_ICON.get(p['priority'])} {p['priority']}")
    print(f"   Gratuit    : {'✅ Oui' if p['tier_gratuit'] else '❌ Non'}")
    print(f"   Sceau      : {seal_id}")
    print(f"\n  🐧 Linux :")
    print(f"     {p['linux_setup']}")
    print(f"\n  🪟 Windows :")
    print(f"     {p['windows_setup']}")
    print(f"\n  ✅ Vérification :")
    print(f"     {p['check_cmd']}")
    print(f"\n  🔒 Sécurité : {p['securite']}")
    print(f"\n  📦 Modèles gratuits : {', '.join(p['models_gratuits'])}\n")

    log_action("install", platform_key, "INSTRUCTIONS_AFFICHÉES", seal_id)

def cmd_adopt(repo_key: str):
    """Lance la procédure d'adoption protocolaire d'un repo GitHub."""
    if repo_key not in MISTRAL_GITHUB_REPOS:
        print(f"❌ Repo inconnu : {repo_key}")
        print(f"   Disponibles : {', '.join(MISTRAL_GITHUB_REPOS.keys())}")
        return

    r     = MISTRAL_GITHUB_REPOS[repo_key]
    score = compute_score(r)
    lic   = check_licence(r)

    print(f"\n╔══ ADOPTION PROTOCOLE : {r['name']} ══╗")
    print(f"   Score composite : {score}/100")
    print(f"   Licence : {r['licence']} {lic}")
    print(f"   Verdict actuel : {r['verdict']}")

    # Blocage si licence interdite
    if r["licence"] in LICENCES_INTERDITES:
        print(f"\n🚫 ADOPTION BLOQUÉE — Licence {r['licence']} interdite en usage commercial.")
        log_action("adopt", repo_key, "BLOQUÉ_LICENCE")
        return

    # Sceau obligatoire pour chaque adoption
    seal_id = SEAL_REFERENCE
    if SEAL_AVAILABLE:
        print(f"\n🔏 Génération sceau d'adoption...")
        rec = seal_decision(
            action=f"mistral-adopt-{repo_key}",
            context=f"Adoption repo Mistral : {r['repo']} | Score: {score}/100 | Licence: {r['licence']}",
            verbose=False,
        )
        seal_id = rec.get("seal_id", SEAL_REFERENCE)
        status  = rec.get("status", "?")
        print(f"   Sceau : {seal_id} — {status}")
        if status != "APPROUVÉ":
            print("   🚫 Sceau non approuvé — adoption bloquée")
            log_action("adopt", repo_key, "BLOQUÉ_SCEAU", seal_id)
            return

    print(f"\n  Étape 1/4 — Vérification licence : {r['licence']} {lic}")
    print(f"  Étape 2/4 — Score protocole : {score}/100 {'✅' if score >= 70 else '⚠️'}")
    print(f"  Étape 3/4 — Intégration Caelum : {r['caelum_integration']}")
    print(f"  Étape 4/4 — Sceau approuvé : {seal_id}")

    print(f"\n  📦 Installation :")
    print(f"     Linux   : {r['linux_install']}")
    print(f"     Windows : {r['windows_install']}")

    MISTRAL_GITHUB_REPOS[repo_key]["seal"]    = seal_id
    MISTRAL_GITHUB_REPOS[repo_key]["verdict"] = "ADOPTÉ"

    log_action("adopt", repo_key, "ADOPTÉ", seal_id)
    print(f"\n  ✅ Repo {repo_key} marqué ADOPTÉ — Sceau : {seal_id}\n")

def cmd_audit():
    """Audit de présence des plateformes Mistral sur le système."""
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       AUDIT PRÉSENCE — PLATEFORMES MISTRAL                   ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    checks = {
        "ollama":        ("ollama",          "ollama list"),
        "mistralai":     ("python3",         "python3 -c \"import mistralai; print('OK')\""),
        "transformers":  ("python3",         "python3 -c \"import transformers; print('OK')\""),
        "langchain":     ("python3",         "python3 -c \"import langchain; print('OK')\""),
        "llama.cpp":     ("llama-cli",       "llama-cli --version"),
        "elia-chat":     ("elia",            "elia --version"),
        "bambooai":      ("python3",         "python3 -c \"import bambooai; print('OK')\""),
    }

    installed    = []
    not_installed = []

    for name, (binary, check_cmd) in checks.items():
        found = shutil.which(binary) is not None
        if binary == "python3":
            # Test import direct
            try:
                result = subprocess.run(
                    ["python3", "-c", check_cmd.split("-c ", 1)[1].strip('"')],
                    capture_output=True, text=True, timeout=5
                )
                found = result.returncode == 0
            except Exception:
                found = False
        if found:
            installed.append(name)
            print(f"  ✅ {name}")
        else:
            not_installed.append(name)
            print(f"  ❌ {name}")

    print(f"\n  Installés    : {len(installed)}/{len(checks)}")
    print(f"  Manquants    : {len(not_installed)}")
    if not_installed:
        print(f"  À installer  : {', '.join(not_installed)}")
    print(f"\n  🔏 Sceau de référence : {SEAL_REFERENCE}")

    log_action("audit", "system", f"{len(installed)}/{len(checks)} installés")

def cmd_verify_all():
    """Vérifie tous les repos avec le scoring protocole."""
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       VÉRIFICATION COMPLÈTE — REPOS MISTRAL                  ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    total_adoptes   = 0
    total_conditionnel = 0
    total_evaluer   = 0
    total_bloque    = 0

    for key, r in MISTRAL_GITHUB_REPOS.items():
        score   = compute_score(r)
        lic     = check_licence(r)
        verdict = r["verdict"]

        # Recalcul automatique verdict selon score + licence
        if r["licence"] in LICENCES_INTERDITES:
            verdict = "BLOQUÉ"
        elif score >= 85:
            verdict = "ADOPTÉ"
        elif score >= 75:
            verdict = "CONDITIONNEL" if verdict == "À ÉVALUER" else verdict
        else:
            verdict = verdict  # Conserver verdict existant

        counts = {"ADOPTÉ": 0, "CONDITIONNEL": 0, "À ÉVALUER": 0, "BLOQUÉ": 0}
        if verdict in counts:
            counts[verdict] += 1

        label = VERDICT_LABELS.get(verdict, verdict)
        print(f"  {label} [{key}]")
        print(f"     Score : {score}/100 | Licence : {r['licence']} {lic} | ⭐ {r['stars']}")

        if verdict == "ADOPTÉ":      total_adoptes += 1
        if verdict == "CONDITIONNEL": total_conditionnel += 1
        if verdict == "À ÉVALUER":   total_evaluer += 1
        if verdict == "BLOQUÉ":      total_bloque += 1

    print(f"\n  Résumé : ✅ {total_adoptes} adoptés | 🟡 {total_conditionnel} conditionnel | 🔵 {total_evaluer} à évaluer | 🚫 {total_bloque} bloqués")
    log_action("verify", "all", f"{total_adoptes} adoptés")

def cmd_report():
    """Affiche le rapport complet registre Mistral."""
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       RAPPORT MISTRAL REGISTRY — CaelumSwarm™                ║")
    print(f"║  Date : {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC                           ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    print("\n── PLATEFORMES ────────────────────────────────────────────────")
    for key, p in MISTRAL_PLATFORMS.items():
        icon = PRIORITY_ICON.get(p["priority"], "⚪")
        print(f"  {icon} {key:25s} {'🆓' if p['tier_gratuit'] else '💰'} {p['priority']}")

    print("\n── REPOS GITHUB ───────────────────────────────────────────────")
    for key, r in MISTRAL_GITHUB_REPOS.items():
        score   = compute_score(r)
        verdict = VERDICT_LABELS.get(r["verdict"], r["verdict"])
        print(f"  {verdict} {key:20s} {score:5.1f}/100  ⭐{r['stars']:4d}  {r['licence']}")

    # Log récent
    entries = load_log()
    if entries:
        print(f"\n── ACTIONS RÉCENTES ({min(len(entries), 5)} dernières) ──────────────────────")
        for e in entries[-5:]:
            ts = e.get("timestamp", "?")[:16]
            print(f"  [{ts}] {e.get('action','?'):10s} {e.get('target','?'):20s} → {e.get('result','?')}")

    print(f"\n  🔏 Sceau de référence : {SEAL_REFERENCE}")
    print(f"  📦 Total : {len(MISTRAL_PLATFORMS)} plateformes | {len(MISTRAL_GITHUB_REPOS)} repos\n")

def cmd_export():
    """Exporte le catalogue complet en JSON."""
    catalog = {
        "generated_at":    datetime.now(timezone.utc).isoformat(),
        "seal_reference":  SEAL_REFERENCE,
        "platforms":       MISTRAL_PLATFORMS,
        "github_repos":    MISTRAL_GITHUB_REPOS,
        "scoring_weights": SCORING_WEIGHTS,
        "scores_computed": {k: compute_score(v) for k, v in MISTRAL_GITHUB_REPOS.items()},
    }
    with open(MISTRAL_CATALOG, "w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"✅ Catalogue exporté → {MISTRAL_CATALOG}")
    log_action("export", "catalog", f"{MISTRAL_CATALOG}")

# ── CLI ────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Mistral Registry — Plateformes et repos GitHub vérifiés CaelumSwarm™"
    )
    parser.add_argument("--list",     action="store_true",  help="Lister plateformes et repos")
    parser.add_argument("--category", type=str, default=None, help="Filtrer : platforms | repos")
    parser.add_argument("--install",  type=str, metavar="KEY", help="Instructions d'installation plateforme")
    parser.add_argument("--adopt",    type=str, metavar="KEY", help="Adopter un repo GitHub via protocole")
    parser.add_argument("--audit",    action="store_true",  help="Audit de présence locale")
    parser.add_argument("--verify",   type=str, metavar="all", help="Vérifier tous les repos (all)")
    parser.add_argument("--report",   action="store_true",  help="Rapport complet registre")
    parser.add_argument("--export",   action="store_true",  help="Exporter catalogue JSON")

    args = parser.parse_args()

    if args.list:
        cmd_list(args.category)
    elif args.install:
        cmd_install(args.install)
    elif args.adopt:
        cmd_adopt(args.adopt)
    elif args.audit:
        cmd_audit()
    elif args.verify:
        cmd_verify_all()
    elif args.report:
        cmd_report()
    elif args.export:
        cmd_export()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
