#!/usr/bin/env python3
"""
Composio Workflow Agent — Caelum Partners
Agent de workflows automatisés combinant email + calendrier.

Orchestre les workflows : nouveau_appel_financement, suivi_hebdomadaire, onboarding_prospect.
Sauvegarde les logs dans docs/composio-logs.json.
"""

import os
import json
from datetime import datetime, timedelta, date
from pathlib import Path

# ---------------------------------------------------------------------------
# Workflows pré-configurés
# ---------------------------------------------------------------------------
WORKFLOWS = {
    "nouveau_appel_financement": {
        "description": (
            "Quand un nouvel appel est détecté → créer événement deadline "
            "+ préparer email de candidature"
        ),
        "étapes": [
            "1. Lire opportunities_tracker.json",
            "2. Pour chaque appel 'nouveau' → créer événement deadline dans Calendar",
            "3. Générer draft email de candidature",
            "4. Créer rappels J-30, J-14, J-7, J-1",
            "5. Marquer appel comme 'en_cours' dans tracker",
        ],
    },
    "suivi_hebdomadaire": {
        "description": (
            "Chaque lundi → rapport des deadlines de la semaine "
            "+ emails à préparer"
        ),
        "étapes": [
            "1. Vérifier deadlines dans les 7 prochains jours",
            "2. Générer rapport des actions prioritaires",
            "3. Préparer brouillons emails si deadline < 7 jours",
            "4. Afficher KPIs de la semaine (MRR, clients, engines)",
        ],
    },
    "onboarding_prospect": {
        "description": (
            "Nouveau prospect CSDDD → email de bienvenue + réunion calendrier"
        ),
        "étapes": [
            "1. Générer email prospection_client personnalisé",
            "2. Proposer créneaux disponibles (simulation)",
            "3. Créer événement 'Appel découverte {prospect}'",
            "4. Créer rappel J-1 et J-0 (1h avant)",
        ],
    },
}

# ---------------------------------------------------------------------------
# Chemins
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
TRACKER_PATH = REPO_ROOT / "docs" / "candidatures" / "opportunities_tracker.json"
LOGS_PATH = REPO_ROOT / "docs" / "composio-logs.json"

# ---------------------------------------------------------------------------
# Utilitaires partagés (version allégée, sans dépendances croisées)
# ---------------------------------------------------------------------------

def _load_tracker() -> list[dict]:
    """Charge opportunities_tracker.json si disponible."""
    if TRACKER_PATH.exists():
        try:
            data = json.loads(TRACKER_PATH.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "opportunities" in data:
                return data["opportunities"]
            return []
        except (json.JSONDecodeError, KeyError):
            return []
    return []


def _format_email(template_key: str, variables: dict) -> dict:
    """
    Mini-formateur d'email (copie locale pour éviter la dépendance circulaire).
    """
    templates = {
        "candidature_financement": {
            "sujet": "Candidature {nom_appel} — Caelum Partners SPRL",
            "corps": (
                "Madame, Monsieur,\n\n"
                "Je me permets de vous contacter au nom de Caelum Partners SPRL.\n\n"
                "Dans le cadre de {nom_appel}, nous souhaitons soumettre notre candidature "
                "pour {montant_demandé} EUR afin de {objectif_principal}.\n\n"
                "Cordialement,\nChaima Mhadbi\nCaelum Partners SPRL"
            ),
        },
        "prospection_client": {
            "sujet": "CaelumSwarm™ — Solution conformité CSDDD pour {nom_entreprise}",
            "corps": (
                "Bonjour {prénom},\n\n"
                "Votre entreprise {nom_entreprise} sera concernée par la directive CSDDD "
                "(EU 2024/1760) applicable dès 2027.\n\n"
                "CaelumSwarm™ est la première plateforme IA dédiée à cette conformité : "
                "{nb_engines}+ engines d'analyse automatisés.\n\n"
                "Seriez-vous disponible pour un appel de 20 minutes cette semaine ?\n\n"
                "Cordialement,\nChaima Mhadbi | Caelum Partners"
            ),
        },
    }
    tmpl = templates.get(template_key, {"sujet": "(template inconnu)", "corps": ""})
    return {
        "sujet": tmpl["sujet"].format(**variables),
        "corps": tmpl["corps"].format(**variables),
    }


def _make_event(titre: str, date_str: str, heure: str, durée_h: float, rappel_jours: list = None) -> dict:
    """Crée un dict événement calendrier."""
    rappel_jours = rappel_jours or []
    from datetime import datetime, timedelta
    dt_start = datetime.strptime(f"{date_str} {heure}", "%Y-%m-%d %H:%M")
    dt_end = dt_start + timedelta(hours=durée_h)
    rappels = [
        {
            "date": (dt_start - timedelta(days=j)).strftime("%Y-%m-%d"),
            "label": f"Rappel J-{j} : {titre}",
        }
        for j in rappel_jours
    ]
    return {
        "titre": titre,
        "date_debut": dt_start.strftime("%Y-%m-%d %H:%M"),
        "date_fin": dt_end.strftime("%Y-%m-%d %H:%M"),
        "rappels": rappels,
    }


# ---------------------------------------------------------------------------
# Fonctions principales
# ---------------------------------------------------------------------------

def run_workflow(workflow_key: str, params: dict) -> dict:
    """
    Exécute un workflow complet en simulation.

    Args:
        workflow_key : Clé du workflow (voir WORKFLOWS)
        params       : Paramètres spécifiques au workflow

    Retourne un dict avec le résultat détaillé.
    """
    if workflow_key not in WORKFLOWS:
        raise ValueError(
            f"Workflow '{workflow_key}' inconnu. Disponibles : {list(WORKFLOWS.keys())}"
        )

    wf = WORKFLOWS[workflow_key]
    print(f"\n{'=' * 60}")
    print(f"WORKFLOW : {workflow_key}")
    print(f"  {wf['description']}")
    print("=" * 60)
    for etape in wf["étapes"]:
        print(f"  {etape}")
    print()

    output = {}

    # -----------------------------------------------------------------------
    if workflow_key == "nouveau_appel_financement":
        nom_appel = params.get("nom_appel", "Appel inconnu")
        deadline = params.get("deadline", "2026-12-31")
        heure_deadline = params.get("heure_deadline", "17:00")
        montant = params.get("montant_demandé", "75 000")
        objectif = params.get("objectif_principal", "accélérer notre développement")
        destinataire = params.get("destinataire", "")

        # Étape 1 : Lire le tracker
        opportunités = _load_tracker()
        print(f"[Étape 1] Tracker chargé — {len(opportunités)} opportunité(s) existante(s)")

        # Étape 2 : Créer événement deadline
        evt = _make_event(
            titre=f"DEADLINE {nom_appel}",
            date_str=deadline,
            heure=heure_deadline,
            durée_h=1,
            rappel_jours=[30, 14, 7, 1],
        )
        print(f"[Étape 2] Événement créé : {evt['titre']} — {evt['date_debut']}")

        # Étape 3 : Générer email de candidature
        email = _format_email(
            "candidature_financement",
            {
                "nom_appel": nom_appel,
                "nb_engines": "58",
                "montant_demandé": montant,
                "objectif_principal": objectif,
            },
        )
        print(f"[Étape 3] Email préparé : {email['sujet']}")
        print(f"          Destinataire : {destinataire or '(à définir)'}")

        # Étape 4 : Afficher rappels
        print(f"[Étape 4] Rappels programmés :")
        for r in evt["rappels"]:
            print(f"          - {r['date']} : {r['label']}")

        # Étape 5 : Mise à jour tracker (simulation)
        print(f"[Étape 5] Appel '{nom_appel}' marqué 'en_cours' dans le tracker (simulation)")

        output = {
            "événement": evt,
            "email": email,
            "rappels": evt["rappels"],
            "tracker_mis_à_jour": True,
        }

    # -----------------------------------------------------------------------
    elif workflow_key == "suivi_hebdomadaire":
        today = datetime.now().date()
        horizon = today + timedelta(days=7)
        print(f"[Étape 1] Vérification deadlines du {today} au {horizon}")

        # Données statiques de référence
        deadlines_refs = [
            {"nom": "Innoviris Proof of Concept", "deadline": date(2026, 9, 15)},
            {"nom": "EIC Accelerator Session 2", "deadline": date(2026, 10, 1)},
            {"nom": "FEDER Bruxelles", "deadline": date(2026, 10, 15)},
        ]

        urgentes = [d for d in deadlines_refs if today <= d["deadline"] <= horizon]
        prochaines = [d for d in deadlines_refs if horizon < d["deadline"]]

        print(f"[Étape 2] Rapport des actions prioritaires :")
        print(f"          Deadlines urgentes (< 7j) : {len(urgentes)}")
        for d in urgentes:
            jours_restants = (d["deadline"] - today).days
            print(f"          !! {d['nom']} — dans {jours_restants} jour(s)")

        print(f"          Deadlines prochaines : {len(prochaines)}")
        for d in prochaines:
            jours_restants = (d["deadline"] - today).days
            print(f"          -> {d['nom']} — dans {jours_restants} jour(s)")

        # KPIs de la semaine
        kpis = params.get("kpis", {
            "mrr": "0 EUR (pre-revenue)",
            "clients": "0 (MVP en cours)",
            "engines": "58 engines déployés",
            "waves": "Wave 58+ en cours",
        })
        print(f"[Étape 4] KPIs de la semaine :")
        for k, v in kpis.items():
            print(f"          {k.upper():<15} : {v}")

        output = {
            "deadlines_urgentes": len(urgentes),
            "deadlines_prochaines": len(prochaines),
            "kpis": kpis,
        }

    # -----------------------------------------------------------------------
    elif workflow_key == "onboarding_prospect":
        prospect = params.get("prospect", "Prospect CSDDD")
        prénom = params.get("prénom", "Madame/Monsieur")
        entreprise = params.get("entreprise", prospect)
        email_dest = params.get("email", "")

        # Étape 1 : Email de prospection
        email = _format_email(
            "prospection_client",
            {
                "prénom": prénom,
                "nom_entreprise": entreprise,
                "nb_engines": "58",
            },
        )
        print(f"[Étape 1] Email généré : {email['sujet']}")
        print(f"          Pour : {email_dest or '(à définir)'}")

        # Étape 2 : Créneaux disponibles (simulation)
        base_date = datetime.now() + timedelta(days=3)
        créneaux = []
        for i in range(3):
            slot = base_date + timedelta(days=i)
            créneaux.append(f"{slot.strftime('%Y-%m-%d')} à 10h00 (Europe/Brussels)")
        print(f"[Étape 2] Créneaux proposés :")
        for c in créneaux:
            print(f"          - {c}")

        # Étape 3 : Événement découverte
        call_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        evt = _make_event(
            titre=f"Appel découverte {entreprise}",
            date_str=call_date,
            heure="10:00",
            durée_h=0.5,
            rappel_jours=[1],
        )
        print(f"[Étape 3] Événement créé : {evt['titre']} — {evt['date_debut']}")

        # Étape 4 : Rappels
        rappel_1h = {
            "date": evt["date_debut"],
            "label": f"Rappel 1h avant : {evt['titre']}",
        }
        print(f"[Étape 4] Rappels :")
        for r in evt["rappels"]:
            print(f"          - {r['date']} : {r['label']}")
        print(f"          - {rappel_1h['date']} (1h avant) : {rappel_1h['label']}")

        output = {
            "email": email,
            "créneaux": créneaux,
            "événement": evt,
            "rappels": evt["rappels"] + [rappel_1h],
        }

    # -----------------------------------------------------------------------
    log_workflow_execution(workflow_key, "success", output)
    print(f"\n[OK] Workflow '{workflow_key}' terminé avec succès.")
    return output


def schedule_weekly_review() -> dict:
    """
    Programme le rapport hebdomadaire (chaque lundi).
    Retourne la configuration de la tâche récurrente.
    """
    config = {
        "workflow": "suivi_hebdomadaire",
        "récurrence": "hebdomadaire",
        "jour": "lundi",
        "heure": "09:00",
        "fuseau": "Europe/Brussels",
        "activation": "simulation — COMPOSIO_API_KEY requise pour l'automation réelle",
        "prochaine_execution": _next_monday().strftime("%Y-%m-%d 09:00"),
    }

    print("\n" + "=" * 60)
    print("  PROGRAMMATION RAPPORT HEBDOMADAIRE")
    print("=" * 60)
    for k, v in config.items():
        print(f"  {k:<25} : {v}")
    print()
    print("[INFO] Pour automatiser avec Composio :")
    print("       composio triggers add GOOGLECALENDAR_EVENT_TRIGGERED")
    print("       Ou utiliser un scheduler cron : '0 9 * * 1 python3 scripts/composio-workflow-agent.py'")
    print()

    log_workflow_execution("schedule_weekly_review", "scheduled", config)
    return config


def log_workflow_execution(workflow: str, status: str, output: dict) -> None:
    """
    Sauvegarde l'exécution d'un workflow dans docs/composio-logs.json.

    Args:
        workflow : Nom du workflow exécuté
        status   : 'success', 'error', 'scheduled', 'skipped'
        output   : Résultat de l'exécution
    """
    LOGS_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Charger les logs existants
    logs = []
    if LOGS_PATH.exists():
        try:
            logs = json.loads(LOGS_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            logs = []

    # Ajouter la nouvelle entrée
    entry = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "workflow": workflow,
        "status": status,
        "output_summary": _summarize_output(output),
    }
    logs.append(entry)

    # Garder les 100 dernières entrées
    logs = logs[-100:]

    LOGS_PATH.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")


def _summarize_output(output: dict) -> dict:
    """Crée un résumé léger du résultat pour les logs."""
    summary = {}
    for k, v in output.items():
        if isinstance(v, dict):
            summary[k] = f"(dict, {len(v)} clé(s))"
        elif isinstance(v, list):
            summary[k] = f"(list, {len(v)} élément(s))"
        elif isinstance(v, bool):
            summary[k] = v
        elif isinstance(v, str) and len(v) > 80:
            summary[k] = v[:80] + "..."
        else:
            summary[k] = v
    return summary


def _next_monday() -> datetime:
    """Retourne la date du prochain lundi."""
    today = datetime.now()
    days_ahead = (7 - today.weekday()) % 7 or 7
    return today + timedelta(days=days_ahead)


# ---------------------------------------------------------------------------
# Point d'entrée — démo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("COMPOSIO WORKFLOW AGENT — Caelum Partners")
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Liste des workflows disponibles
    print(f"\nWorkflows disponibles ({len(WORKFLOWS)}) :")
    for key, wf in WORKFLOWS.items():
        print(f"  [{key}]")
        print(f"    {wf['description']}")
    print()

    # Vérification Composio
    api_key = os.environ.get("COMPOSIO_API_KEY", "")
    if api_key:
        print("[OK] COMPOSIO_API_KEY détectée — mode Composio disponible")
    else:
        print("[INFO] Mode simulation — COMPOSIO_API_KEY absente")
    print()

    # -----------------------------------------------------------------------
    # Démo : workflow "nouveau_appel_financement" pour Innoviris Bridge
    # -----------------------------------------------------------------------
    result_1 = run_workflow(
        workflow_key="nouveau_appel_financement",
        params={
            "nom_appel": "Innoviris Bridge",
            "deadline": "2026-09-15",
            "heure_deadline": "17:00",
            "montant_demandé": "75 000",
            "objectif_principal": (
                "finaliser notre MVP CaelumSwarm™ et valider le product-market fit "
                "sur le marché B2B CSDDD en Belgique"
            ),
            "destinataire": "financement@innoviris.brussels",
        },
    )

    # -----------------------------------------------------------------------
    # Démo : rapport hebdomadaire
    # -----------------------------------------------------------------------
    result_2 = run_workflow(
        workflow_key="suivi_hebdomadaire",
        params={
            "kpis": {
                "mrr": "0 EUR (pre-revenue)",
                "clients": "0 (MVP en cours)",
                "engines": "58 engines déployés",
                "waves": "Wave 58+ en cours",
                "candidatures": "3 en préparation (Innoviris, EIC, FEDER)",
            }
        },
    )

    # -----------------------------------------------------------------------
    # Programmation rapport hebdomadaire
    # -----------------------------------------------------------------------
    schedule_weekly_review()

    # -----------------------------------------------------------------------
    # Résumé des logs
    # -----------------------------------------------------------------------
    if LOGS_PATH.exists():
        logs = json.loads(LOGS_PATH.read_text(encoding="utf-8"))
        print(f"\n[LOGS] {len(logs)} entrée(s) dans {LOGS_PATH}")
        for entry in logs[-3:]:
            print(f"       {entry['timestamp']}  {entry['workflow']}  [{entry['status']}]")

    print()
    print("[DONE] Workflows Caelum simulés avec succès.")
    print(f"       Logs sauvegardés : {LOGS_PATH}")
