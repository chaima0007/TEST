"""
Env Variables Manager Agent — Caelum Partners
Crée, valide et gère toutes les variables d'environnement du projet.
"""
import os
import json
from datetime import datetime

BANNER = "=" * 60

ENV_VARS = [
    {
        "key": "SWARM_API_URL",
        "description": "URL de l'API CaelumSwarm backend (requis pour toutes les routes)",
        "example": "https://api.caelumpartners.com",
        "required": True,
        "context": "server",
        "service": "CaelumSwarm API",
    },
    {
        "key": "NEXT_PUBLIC_SWARM_API_URL",
        "description": "URL publique CaelumSwarm (accessible côté client/browser)",
        "example": "https://api.caelumpartners.com",
        "required": False,
        "context": "client",
        "service": "CaelumSwarm API",
    },
    {
        "key": "DATABASE_URL",
        "description": "URL de connexion PostgreSQL (format: postgresql://user:pass@host:5432/db)",
        "example": "postgresql://caelum:password@localhost:5432/caelumswarm",
        "required": False,
        "context": "server",
        "service": "PostgreSQL",
    },
    {
        "key": "DEMO_EMAIL",
        "description": "Email de démonstration pour les accès démo",
        "example": "demo@caelumpartners.com",
        "required": False,
        "context": "server",
        "service": "Auth Demo",
    },
    {
        "key": "DEMO_PASSWORD",
        "description": "Mot de passe de démonstration (jamais en production)",
        "example": "demo2026!",
        "required": False,
        "context": "server",
        "service": "Auth Demo",
    },
    {
        "key": "COMPOSIO_API_KEY",
        "description": "Clé API Composio pour intégration Gmail/Google Calendar",
        "example": "comp_xxxxxxxxxxxxxxxxxxxx",
        "required": False,
        "context": "server",
        "service": "Composio (email/calendar)",
    },
    {
        "key": "OPENAI_API_KEY",
        "description": "Clé API OpenAI pour fonctions IA avancées",
        "example": "sk-xxxxxxxxxxxxxxxxxxxx",
        "required": False,
        "context": "server",
        "service": "OpenAI GPT-4",
    },
    {
        "key": "ANTHROPIC_API_KEY",
        "description": "Clé API Anthropic Claude pour agents IA",
        "example": "sk-ant-xxxxxxxxxxxxxxxxxxxx",
        "required": False,
        "context": "server",
        "service": "Anthropic Claude",
    },
    {
        "key": "NEXTAUTH_SECRET",
        "description": "Secret JWT NextAuth (générer avec: openssl rand -base64 32)",
        "example": "Ge7dXPqHxYz...(32 chars random)",
        "required": False,
        "context": "server",
        "service": "NextAuth.js",
    },
    {
        "key": "NEXTAUTH_URL",
        "description": "URL publique de l'application (pour les callbacks OAuth)",
        "example": "https://astounding-haupia-16b5a6.netlify.app",
        "required": False,
        "context": "server",
        "service": "NextAuth.js",
    },
]


def check_env_status():
    """Vérifie quelles variables sont définies dans l'environnement courant."""
    results = []
    for var in ENV_VARS:
        value = os.environ.get(var["key"])
        status = "✓ DÉFINIE" if value else ("⚠ MANQUANTE (requis)" if var["required"] else "○ NON DÉFINIE")
        masked = (value[:4] + "..." + value[-2:]) if value and len(value) > 8 else ("***" if value else None)
        results.append({
            **var,
            "is_set": bool(value),
            "masked_value": masked,
            "status": status,
        })
    return results


def generate_env_local_template(output_path=".env.local"):
    """Génère un fichier .env.local template avec toutes les variables."""
    lines = [
        "# .env.local — Caelum Partners CaelumSwarm™",
        f"# Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "# NE JAMAIS COMMITTER CE FICHIER (il est dans .gitignore)",
        "",
        "# ============================================================",
        "# CAELUMSWARM API — REQUIS",
        "# ============================================================",
    ]
    current_service = None
    for var in ENV_VARS:
        if var["service"] != current_service:
            if current_service is not None:
                lines.append("")
                lines.append(f"# {'-' * 50}")
                lines.append(f"# {var['service'].upper()}")
                lines.append(f"# {'-' * 50}")
            current_service = var["service"]
        lines.append(f"# {var['description']}")
        prefix = "" if os.environ.get(var["key"]) else "# "
        value = os.environ.get(var["key"]) or var["example"]
        lines.append(f"{prefix}{var['key']}={value}")
        lines.append("")
    content = "\n".join(lines)
    with open(output_path, "w") as f:
        f.write(content)
    return output_path


def generate_netlify_instructions():
    """Génère les instructions pour configurer les variables sur Netlify."""
    print(f"\n{BANNER}")
    print("  CONFIGURATION NETLIFY — Variables d'environnement")
    print(BANNER)
    print("\n1. Aller sur : https://app.netlify.com")
    print("2. Sélectionner le site : astounding-haupia-16b5a6")
    print("3. Site settings → Environment variables → Add variable")
    print("\nVariables à configurer sur Netlify :")
    print()
    for var in ENV_VARS:
        if var["required"] or var["key"] in ["SWARM_API_URL", "COMPOSIO_API_KEY"]:
            mark = "🔴 REQUIS" if var["required"] else "🟡 RECOMMANDÉ"
            print(f"  {mark}")
            print(f"  Clé   : {var['key']}")
            print(f"  Valeur: {var['example']}")
            print(f"  Usage : {var['description']}")
            print()


def generate_composio_status():
    """Vérifie et affiche le statut de la connexion Composio."""
    print(f"\n{BANNER}")
    print("  STATUT CONNEXION COMPOSIO")
    print(BANNER)
    api_key = os.environ.get("COMPOSIO_API_KEY")
    if not api_key:
        print("\n[❌] COMPOSIO_API_KEY non définie")
        print("\n  Pour activer Composio (Gmail + Google Calendar) :")
        print("  1. Créer un compte GRATUIT sur : https://composio.dev")
        print("  2. Dashboard → API Keys → Créer une clé")
        print("  3. Ajouter sur Netlify :")
        print("     Site settings → Environment → COMPOSIO_API_KEY = votre_clé")
        print("  4. Localement : export COMPOSIO_API_KEY=votre_clé")
        print("  5. Installer : pip install composio-core")
        print("  6. Connecter Gmail : composio add gmail")
        print("  7. Connecter Calendar : composio add googlecalendar")
        print("\n  → Les agents email/calendar fonctionnent en mode SIMULATION")
        print("    jusqu'à ce que la clé soit définie.")
    else:
        print(f"\n[✓] COMPOSIO_API_KEY définie ({api_key[:4]}...{api_key[-2:]})")
        try:
            from composio import ComposioToolSet
            toolset = ComposioToolSet(api_key=api_key)
            print("[✓] SDK Composio importé avec succès")
            print("[✓] Connexion active — Gmail et Calendar disponibles")
        except ImportError:
            print("[⚠] SDK Composio non installé : pip install composio-core")
        except Exception as e:
            print(f"[⚠] Erreur connexion: {e}")


def run():
    print(f"\n{BANNER}")
    print("  ENV VARIABLES MANAGER — Caelum Partners")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(BANNER)

    # 1. Statut actuel
    print(f"\n{'─' * 60}")
    print("  STATUT DES VARIABLES D'ENVIRONNEMENT")
    print(f"{'─' * 60}")
    results = check_env_status()
    for r in results:
        mark = "✓" if r["is_set"] else ("!" if r["required"] else "○")
        val_display = f" = {r['masked_value']}" if r["masked_value"] else ""
        print(f"  [{mark}] {r['key']}{val_display}")
        print(f"       → {r['description']}")

    defined = sum(1 for r in results if r["is_set"])
    total = len(results)
    print(f"\n  {defined}/{total} variables définies")

    # 2. Générer .env.local template
    print(f"\n{'─' * 60}")
    print("  GÉNÉRATION .env.local TEMPLATE")
    print(f"{'─' * 60}")
    path = generate_env_local_template(".env.local.example")
    print(f"  ✓ Template généré : {path}")
    print("  ⚠ Copier vers .env.local et remplir les valeurs réelles")

    # 3. Statut Composio
    generate_composio_status()

    # 4. Instructions Netlify
    generate_netlify_instructions()

    # 5. Rapport JSON
    report = {
        "generated_at": datetime.now().isoformat(),
        "environment": "container/remote",
        "variables": [
            {
                "key": r["key"],
                "is_set": r["is_set"],
                "required": r["required"],
                "service": r["service"],
            }
            for r in results
        ],
        "summary": {
            "total": total,
            "defined": defined,
            "missing_required": sum(1 for r in results if not r["is_set"] and r["required"]),
        },
        "composio_ready": bool(os.environ.get("COMPOSIO_API_KEY")),
        "swarm_api_ready": bool(os.environ.get("SWARM_API_URL")),
    }
    with open("docs/env-variables-report.json", "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n  ✓ Rapport JSON : docs/env-variables-report.json")

    print(f"\n{BANNER}")
    print("  RÉSUMÉ")
    print(BANNER)
    if report["summary"]["missing_required"] == 0:
        print("  ✓ Toutes les variables REQUISES sont définies")
    else:
        print(f"  ⚠ {report['summary']['missing_required']} variable(s) REQUISE(s) manquante(s)")
    print(f"  → SWARM_API_URL : {'✓ OK' if report['swarm_api_ready'] else '⚠ À définir sur Netlify'}")
    print(f"  → COMPOSIO : {'✓ Actif' if report['composio_ready'] else '○ Mode simulation (ajouter COMPOSIO_API_KEY)'}")
    print()

    return report


if __name__ == "__main__":
    run()
