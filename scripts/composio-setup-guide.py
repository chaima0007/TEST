#!/usr/bin/env python3
"""
Composio Setup Guide — Caelum Partners
Guide d'installation et de configuration Composio.

Affiche le guide en console et sauvegarde docs/composio-setup.md.
"""

import os
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Contenu du guide
# ---------------------------------------------------------------------------
GUIDE_CONTENT = """# GUIDE COMPOSIO — CAELUM PARTNERS
Généré le {date}
=================================

## ÉTAPE 1 — Créer un compte Composio
  → composio.dev/signup (gratuit, pas de carte bancaire)
  → Choisir plan "Free" (100 actions/mois offertes)

## ÉTAPE 2 — Installer le SDK Python
  → pip install composio-core composio-openai

## ÉTAPE 3 — Authentification
  → composio login
  → Copier l'API key depuis le dashboard

## ÉTAPE 4 — Connecter Gmail
  → composio add gmail
  → Autoriser l'accès OAuth Google
  → Tester : composio actions --app gmail

## ÉTAPE 5 — Connecter Google Calendar
  → composio add googlecalendar
  → Autoriser l'accès OAuth
  → Tester : composio actions --app googlecalendar

## ÉTAPE 6 — Variables d'environnement
  → export COMPOSIO_API_KEY=your_key_here
  → Ajouter dans .env.local (JAMAIS committer ce fichier)

## ÉTAPE 7 — Tester avec les agents Caelum
  → python3 scripts/composio-email-agent.py
  → python3 scripts/composio-calendar-agent.py
  → python3 scripts/composio-workflow-agent.py

---

## INTÉGRATIONS DISPONIBLES VIA COMPOSIO

  ✓ Gmail — lecture/envoi/recherche emails
  ✓ Google Calendar — création/modification événements
  ✓ Outlook / Office 365 — alternative Microsoft
  ✓ Slack — notifications équipe
  ✓ Notion — documentation
  ✓ Linear / Jira — gestion de tâches
  ✓ HubSpot CRM — suivi prospects
  ✓ LinkedIn — prospection B2B

---

## PLAN CAELUM RECOMMANDÉ

  Phase 1 (maintenant)  : Gmail + Google Calendar
  Phase 2 (Q3 2026)     : Slack équipe + Notion docs
  Phase 3 (Q4 2026)     : HubSpot CRM prospects CSDDD

---

## SCRIPTS DISPONIBLES

  scripts/composio-email-agent.py     — Envoi d'emails (candidatures, prospection)
  scripts/composio-calendar-agent.py  — Gestion du calendrier + export .ics
  scripts/composio-setup-guide.py     — Ce guide (génère aussi ce fichier .md)
  scripts/composio-workflow-agent.py  — Workflows automatisés email + calendrier

---

## VÉRIFICATION RAPIDE DE L'INSTALLATION

```bash
# Vérifier que la clé est présente
echo $COMPOSIO_API_KEY

# Vérifier les apps connectées
composio apps connected

# Tester une action Gmail
composio actions --app gmail --query "send email"

# Tester une action Google Calendar
composio actions --app googlecalendar --query "create event"
```

---

## EN CAS DE PROBLÈME

  Erreur OAuth       → composio logout && composio login
  App non connectée  → composio add gmail (refaire l'autorisation)
  SDK introuvable    → pip install --upgrade composio-core composio-openai
  Quota dépassé      → vérifier plan sur composio.dev/dashboard

---

## SÉCURITÉ

  ✗ Ne jamais committer COMPOSIO_API_KEY dans le code source
  ✗ Ne jamais inclure la clé dans les logs ou prints
  ✓ Utiliser .env.local (ajouté dans .gitignore)
  ✓ Faire tourner les agents en local uniquement
  ✓ Renouveler la clé si compromission suspectée

---

Contact : retrouvetonsmile@gmail.com
Caelum Partners SPRL — Bruxelles, Belgique
"""

# ---------------------------------------------------------------------------
# Checklist de vérification de l'installation
# ---------------------------------------------------------------------------
CHECKLIST_ITEMS = [
    ("COMPOSIO_API_KEY", "Variable d'environnement COMPOSIO_API_KEY"),
    ("composio", "CLI Composio installée (composio --version)"),
    ("composio-core", "SDK Python composio-core"),
    ("composio-openai", "SDK Python composio-openai"),
]


def check_environment() -> dict:
    """
    Vérifie l'état de l'installation Composio sur le système.
    Retourne un dict avec le statut de chaque composant.
    """
    status = {}

    # Vérification clé API
    api_key = os.environ.get("COMPOSIO_API_KEY", "")
    status["api_key"] = {
        "label": "COMPOSIO_API_KEY",
        "ok": bool(api_key),
        "value": "***définie***" if api_key else "MANQUANTE",
    }

    # Vérification SDK Python
    for pkg in ["composio", "composio_openai"]:
        try:
            import importlib
            importlib.import_module(pkg.replace("-", "_"))
            status[pkg] = {"label": pkg, "ok": True, "value": "installé"}
        except ImportError:
            status[pkg] = {"label": pkg, "ok": False, "value": "non installé"}

    return status


def print_checklist() -> None:
    """Affiche la checklist de vérification en console."""
    print("\n" + "=" * 60)
    print("  CHECKLIST D'INSTALLATION COMPOSIO")
    print("=" * 60)
    status = check_environment()
    all_ok = True
    for key, info in status.items():
        icon = "[OK]" if info["ok"] else "[--]"
        print(f"  {icon}  {info['label']:<30} {info['value']}")
        if not info["ok"]:
            all_ok = False
    print("-" * 60)
    if all_ok:
        print("  Tout est configuré — les agents Composio sont opérationnels.")
    else:
        print("  Certains composants manquent — voir le guide ci-dessous.")
    print()


def save_guide(output_path: str = None) -> str:
    """
    Sauvegarde le guide en fichier Markdown.

    Args:
        output_path : Chemin de sortie (défaut : docs/composio-setup.md)

    Retourne le chemin absolu du fichier créé.
    """
    if output_path is None:
        output_path = str(
            Path(__file__).parent.parent / "docs" / "composio-setup.md"
        )

    content = GUIDE_CONTENT.format(date=datetime.now().strftime("%Y-%m-%d %H:%M"))
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(f"[OK] Guide sauvegardé : {output_path}")
    return output_path


def print_guide() -> None:
    """Affiche le guide complet en console."""
    content = GUIDE_CONTENT.format(date=datetime.now().strftime("%Y-%m-%d %H:%M"))
    print(content)


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("COMPOSIO SETUP GUIDE — Caelum Partners")
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Checklist d'installation
    print_checklist()

    # Affichage du guide
    print_guide()

    # Sauvegarde du guide en Markdown
    guide_path = save_guide()

    print()
    print("[DONE] Guide Composio prêt.")
    print(f"       Fichier : {guide_path}")
    print()
    print("Prochaine étape :")
    print("  python3 scripts/composio-email-agent.py")
    print("  python3 scripts/composio-calendar-agent.py")
