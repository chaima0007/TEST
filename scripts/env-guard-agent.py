"""
env-guard-agent.py — Caelum Partners
Vérifie que toutes les variables d'environnement critiques sont définies
avant un build ou un déploiement. Détecte les oublis AVANT qu'ils causent un crash.
"""

import os
import sys

REQUIRED = {
    "SWARM_API_URL": {
        "description": "URL de l'API Swarm upstream",
        "severity": "warn",
        "fallback": "Mock data utilisé si absent (comportement attendu en dev)",
    },
    "NEXTAUTH_SECRET": {
        "description": "Secret NextAuth pour sessions utilisateurs",
        "severity": "critical",
        "fallback": "L'authentification sera cassée en production",
    },
    "NEXTAUTH_URL": {
        "description": "URL de base de l'application (pour NextAuth)",
        "severity": "warn",
        "fallback": "Peut causer des redirections incorrectes",
    },
}

OPTIONAL = {
    "DATABASE_URL": "Connection string base de données (Turso/LibSQL en prod)",
    "TURSO_DATABASE_URL": "URL Turso pour LibSQL en production",
    "TURSO_AUTH_TOKEN": "Token auth Turso",
    "NEXT_TELEMETRY_DISABLED": "Désactive télémétrie Next.js (recommandé: '1')",
}

BUILD_CRITICAL = [
    ("prisma generate", "lib/generated/prisma", "Client Prisma non généré → crash build"),
]


def check_env():
    print("=" * 60)
    print("🔐  Env Guard Agent — Caelum Partners")
    print("=" * 60)

    errors = []
    warnings = []

    for var, meta in REQUIRED.items():
        val = os.environ.get(var)
        if not val:
            if meta["severity"] == "critical":
                errors.append(f"CRITIQUE: {var} — {meta['description']}")
                print(f"  ✗ {var} ABSENT — {meta['fallback']}")
            else:
                warnings.append(f"WARN: {var} — {meta['description']}")
                print(f"  ⚠ {var} absent — {meta['fallback']}")
        else:
            masked = val[:4] + "..." if len(val) > 4 else "***"
            print(f"  ✓ {var} défini ({masked})")

    print()
    for var, desc in OPTIONAL.items():
        val = os.environ.get(var)
        status = "✓" if val else "○"
        print(f"  {status} {var} {'(défini)' if val else '(optionnel)'}")

    print()

    for cmd, path, risk in BUILD_CRITICAL:
        if not os.path.exists(path):
            errors.append(f"BUILD: '{cmd}' requis — {risk}")
            print(f"  ✗ {path} MANQUANT → ajouter '{cmd}' au build command")
        else:
            print(f"  ✓ {path} présent")

    print()
    if errors:
        print(f"❌  {len(errors)} erreur(s) critique(s) :")
        for e in errors:
            print(f"   • {e}")
        sys.exit(1)
    elif warnings:
        print(f"⚠️  {len(warnings)} avertissement(s) — build peut fonctionner mais vérifier")
        sys.exit(0)
    else:
        print("✅  Toutes les variables d'environnement sont en ordre")
        sys.exit(0)


if __name__ == "__main__":
    check_env()
