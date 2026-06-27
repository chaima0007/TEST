#!/usr/bin/env python3
"""
Composio Email Agent — Caelum Partners
Agent de préparation et d'envoi d'emails via Composio (Gmail/Outlook).

Mode simulation : génère des templates d'emails prêts à envoyer.
Mode Composio   : appelle l'API Composio réelle si COMPOSIO_API_KEY est définie.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Templates d'emails pré-configurés pour Caelum Partners
# ---------------------------------------------------------------------------
EMAIL_TEMPLATES = {
    "candidature_financement": {
        "sujet": "Candidature {nom_appel} — Caelum Partners SPRL",
        "corps": """Madame, Monsieur,

Je me permets de vous contacter au nom de Caelum Partners SPRL, startup bruxelloise spécialisée dans la conformité droits humains et ESG via intelligence artificielle.

Notre plateforme CaelumSwarm™ est la première solution IA multi-agents dédiée à la directive CSDDD (EU 2024/1760), couvrant {nb_engines} domaines droits humains avec des moteurs d'analyse automatisés.

Dans le cadre de {nom_appel}, nous souhaitons soumettre notre candidature pour {montant_demandé} EUR afin de {objectif_principal}.

Vous trouverez en pièce jointe notre dossier de candidature complet.

Dans l'attente de votre retour,
Chaima Mhadbi
Fondatrice, Caelum Partners SPRL
retrouvetonsmile@gmail.com
Bruxelles, Belgique""",
        "destinataires": [],
        "pj_suggérées": [
            "dossier_candidature.pdf",
            "presentation_caelumswarm.pdf",
            "kbis_sprl.pdf",
        ],
    },
    "prospection_client": {
        "sujet": "CaelumSwarm™ — Solution conformité CSDDD pour {nom_entreprise}",
        "corps": """Bonjour {prénom},

Votre entreprise {nom_entreprise} sera concernée par la directive CSDDD (EU 2024/1760) applicable dès 2027.

CaelumSwarm™ est la première plateforme IA dédiée à cette conformité : {nb_engines}+ engines d'analyse automatisés, couverture complète de la chaîne d'approvisionnement, rapportage CSRD intégré.

Seriez-vous disponible pour un appel de 20 minutes cette semaine ?

Cordialement,
Chaima Mhadbi | Caelum Partners""",
        "destinataires": [],
    },
    "suivi_candidature": {
        "sujet": "Suivi candidature {nom_appel} — Caelum Partners",
        "corps": (
            "Madame, Monsieur,\n\n"
            "Suite à notre candidature du {date_envoi} pour {nom_appel}, "
            "nous souhaitons vérifier la bonne réception de notre dossier et "
            "vous demander si des informations complémentaires seraient nécessaires.\n\n"
            "Nous restons à votre disposition pour tout renseignement.\n\n"
            "Cordialement,\n"
            "Chaima Mhadbi\n"
            "Fondatrice, Caelum Partners SPRL\n"
            "retrouvetonsmile@gmail.com"
        ),
    },
    "partenariat_academia": {
        "sujet": "Proposition de partenariat recherche — Caelum Partners x {institution}",
        "corps": (
            "Madame, Monsieur,\n\n"
            "Dans le cadre de notre candidature Horizon Europe, nous recherchons un "
            "partenaire académique belge spécialisé en droit des affaires/ESG.\n\n"
            "Caelum Partners SPRL développe CaelumSwarm™, une plateforme IA multi-agents "
            "pour la conformité CSDDD. Un partenariat avec {institution} nous permettrait "
            "d'ancrer notre approche dans la rigueur académique et de co-publier des "
            "travaux de recherche appliquée.\n\n"
            "Seriez-vous ouverts à explorer cette collaboration ?\n\n"
            "Cordialement,\n"
            "Chaima Mhadbi\n"
            "Fondatrice, Caelum Partners SPRL\n"
            "retrouvetonsmile@gmail.com"
        ),
    },
}

COMPOSIO_INSTRUCTIONS = """
Pour activer l'envoi réel :
1. Créer un compte sur composio.dev (gratuit)
2. Générer une API key dans le dashboard
3. export COMPOSIO_API_KEY=your_key
4. composio add gmail  (ou outlook)
5. Relancer ce script
"""

# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def _format_template(template_key: str, variables: dict) -> dict:
    """Retourne une copie du template avec les variables substituées."""
    if template_key not in EMAIL_TEMPLATES:
        raise ValueError(
            f"Template '{template_key}' inconnu. Disponibles : {list(EMAIL_TEMPLATES.keys())}"
        )
    tmpl = EMAIL_TEMPLATES[template_key]
    result = {}
    for key, value in tmpl.items():
        if isinstance(value, str):
            result[key] = value.format(**variables)
        else:
            result[key] = value
    return result


def prepare_email(template_key: str, variables_dict: dict) -> dict:
    """
    Prépare un email formaté prêt à envoyer.

    Retourne un dict avec : sujet, corps, destinataires, pj_suggérées (si définie).
    """
    email = _format_template(template_key, variables_dict)
    return email


def list_templates() -> list[str]:
    """Liste tous les templates disponibles."""
    return list(EMAIL_TEMPLATES.keys())


def simulate_send(template_key: str, to: list[str], variables: dict) -> None:
    """
    Affiche l'email formaté sans l'envoyer (mode test).
    """
    email = prepare_email(template_key, variables)
    separator = "=" * 60
    print(separator)
    print(f"[SIMULATION] Template : {template_key}")
    print(separator)
    print(f"A          : {', '.join(to) if to else '(non défini)'}")
    print(f"Sujet      : {email['sujet']}")
    if "pj_suggérées" in email:
        print(f"PJ         : {', '.join(email['pj_suggérées'])}")
    print("-" * 60)
    print(email["corps"])
    print(separator)
    print("[OK] Email prêt — aucun envoi effectué (mode simulation)")
    print()


def connect_composio() -> bool:
    """
    Vérifie si COMPOSIO_API_KEY est présente.
    Affiche les instructions si absente.
    Retourne True si la clé est disponible, False sinon.
    """
    api_key = os.environ.get("COMPOSIO_API_KEY", "")
    if api_key:
        print("[OK] COMPOSIO_API_KEY détectée — mode Composio actif")
        return True
    else:
        print("[INFO] COMPOSIO_API_KEY absente — mode simulation uniquement")
        print(COMPOSIO_INSTRUCTIONS)
        return False


def send_via_composio(template_key: str, to: list[str], variables: dict) -> dict:
    """
    Envoie un email via l'API Composio.
    Nécessite COMPOSIO_API_KEY dans l'environnement.

    Retourne un dict avec le résultat de l'opération.
    """
    if not connect_composio():
        return {"status": "skipped", "reason": "COMPOSIO_API_KEY manquante"}

    email = prepare_email(template_key, variables)

    # Import conditionnel du SDK Composio (optionnel)
    try:
        from composio_openai import ComposioToolSet, App  # type: ignore

        toolset = ComposioToolSet(api_key=os.environ["COMPOSIO_API_KEY"])
        tools = toolset.get_tools(apps=[App.GMAIL])

        # Payload d'envoi Gmail via Composio
        payload = {
            "to": to,
            "subject": email["sujet"],
            "body": email["corps"],
        }
        result = toolset.execute_action(
            action="GMAIL_SEND_EMAIL",
            params=payload,
        )
        print(f"[OK] Email envoyé via Composio/Gmail : {email['sujet']}")
        return {"status": "sent", "result": result}

    except ImportError:
        print("[WARN] SDK composio-openai non installé — pip install composio-openai")
        print("[INFO] Basculement en mode simulation")
        simulate_send(template_key, to, variables)
        return {"status": "simulated", "reason": "SDK non installé"}
    except Exception as exc:
        print(f"[ERROR] Echec envoi Composio : {exc}")
        return {"status": "error", "error": str(exc)}


# ---------------------------------------------------------------------------
# Point d'entrée — démo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("COMPOSIO EMAIL AGENT — Caelum Partners")
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()

    # Vérification connexion Composio
    connected = connect_composio()

    # Liste des templates disponibles
    print(f"Templates disponibles ({len(list_templates())}) :")
    for t in list_templates():
        print(f"  - {t}")
    print()

    # Démo 1 — candidature financement (Innoviris)
    simulate_send(
        template_key="candidature_financement",
        to=["financement@innoviris.brussels"],
        variables={
            "nom_appel": "Innoviris Proof of Concept 2026",
            "nb_engines": "58",
            "montant_demandé": "75 000",
            "objectif_principal": "finaliser notre MVP et valider notre product-market fit sur le marché B2B CSDDD",
        },
    )

    # Démo 2 — prospection client (grande entreprise belge)
    simulate_send(
        template_key="prospection_client",
        to=["sustainability@solvay.com"],
        variables={
            "prénom": "Marie",
            "nom_entreprise": "Solvay SA",
            "nb_engines": "58",
        },
    )

    print("[DONE] Démo terminée.")
    print()
    if not connected:
        print("Pour passer en mode envoi réel, suivre les instructions ci-dessus.")
