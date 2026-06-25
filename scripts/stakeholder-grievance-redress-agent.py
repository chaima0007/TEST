#!/usr/bin/env python3
"""
CaelumSwarm™ — Stakeholder Grievance Redress Agent
Mécanisme de réclamation parties prenantes (CSDDD Art.9)
UNGP Pillar III Remedy | ISO 37002 Whistleblowing
Stdlib Python uniquement.
"""

import json
import datetime
import random
import time
import sys
import uuid
from typing import Any

# ─── Configuration ────────────────────────────────────────────────────────────

AGENT_ID = "SGRA-001"
AGENT_NAME = "Stakeholder Grievance Redress Agent"
VERSION = "1.0.0"

COMPLIANCE_FRAMEWORKS = [
    "CSDDD Art.9 — Mécanisme de Réclamation",
    "UNGP Pillar III — Remedy & Access to Justice",
    "ISO 37002:2021 — Whistleblowing Management Systems",
    "ILO Core Conventions — Liberté Syndicale & Négociation",
]

CHANNELS = {
    "digital_form": {
        "id": "CH-001",
        "name": "Formulaire Digital Sécurisé",
        "description": "Portail web chiffré, accessible 24h/24, multilingue (EN/FR/ES/ZH/AR)",
        "anonymity": True,
        "languages": ["fr", "en", "es", "zh", "ar"],
        "avg_response_time_h": 4,
    },
    "hotline": {
        "id": "CH-002",
        "name": "Hotline Téléphonique",
        "description": "Ligne dédiée +33 1 XX XX XX XX, disponible Lu-Ve 8h-20h CET",
        "anonymity": True,
        "languages": ["fr", "en"],
        "avg_response_time_h": 2,
    },
    "community_liaison": {
        "id": "CH-003",
        "name": "Liaison Communautaire",
        "description": "Points de contact locaux sur sites de production — Afrique/Asie/Amérique Latine",
        "anonymity": False,
        "languages": ["fr", "en", "es", "sw", "id"],
        "avg_response_time_h": 24,
    },
    "ngo_partner": {
        "id": "CH-004",
        "name": "Partenaire ONG",
        "description": "Réclamations via ONG tierces indépendantes (RAID, SOMO, ECCHR)",
        "anonymity": True,
        "languages": ["fr", "en", "de", "nl"],
        "avg_response_time_h": 48,
    },
}

WORKFLOW_STAGES = [
    "Réception",
    "Triage",
    "Investigation",
    "Résolution",
    "Clôture",
]

SLA_HOURS = {
    "critique": 48,
    "élevé": 120,   # 5 jours
    "standard": 360,  # 15 jours
}

# Simulation : 12 réclamations actives, 3 résolues, 2 escaladées
SIMULATED_GRIEVANCES = [
    # Actives
    {"id": "GRV-2026-001", "channel": "digital_form", "severity": "critique", "stage": "Investigation",
     "subject": "Travail forcé — chaîne approvisionnement cobalt RDC",
     "submitter_type": "travailleur", "country": "RDC",
     "filed_at": "2026-06-20T08:30:00Z", "escalated": True, "resolved": False,
     "assigned_to": "Équipe Due Diligence RH"},
    {"id": "GRV-2026-002", "channel": "ngo_partner", "severity": "critique", "stage": "Triage",
     "subject": "Violations sécurité mineurs — site minier Katanga",
     "submitter_type": "communauté", "country": "RDC",
     "filed_at": "2026-06-21T10:15:00Z", "escalated": True, "resolved": False,
     "assigned_to": "Direction Conformité"},
    {"id": "GRV-2026-003", "channel": "hotline", "severity": "élevé", "stage": "Investigation",
     "subject": "Harcèlement managérial — usine Bangladesh",
     "submitter_type": "travailleur", "country": "Bangladesh",
     "filed_at": "2026-06-18T14:00:00Z", "escalated": False, "resolved": False,
     "assigned_to": "Équipe Relations Sociales"},
    {"id": "GRV-2026-004", "channel": "community_liaison", "severity": "élevé", "stage": "Investigation",
     "subject": "Pollution rivière — décharge déchets industriels non traitée",
     "submitter_type": "communauté", "country": "Ghana",
     "filed_at": "2026-06-17T09:00:00Z", "escalated": False, "resolved": False,
     "assigned_to": "Équipe Environnement"},
    {"id": "GRV-2026-005", "channel": "digital_form", "severity": "élevé", "stage": "Résolution",
     "subject": "Discrimination embauche — critères ethniques allégués",
     "submitter_type": "travailleur", "country": "France",
     "filed_at": "2026-06-15T11:30:00Z", "escalated": False, "resolved": False,
     "assigned_to": "DRH France"},
    {"id": "GRV-2026-006", "channel": "digital_form", "severity": "standard", "stage": "Réception",
     "subject": "Non-paiement heures supplémentaires — prestataire logistique",
     "submitter_type": "travailleur", "country": "Pologne",
     "filed_at": "2026-06-22T07:45:00Z", "escalated": False, "resolved": False,
     "assigned_to": None},
    {"id": "GRV-2026-007", "channel": "hotline", "severity": "standard", "stage": "Triage",
     "subject": "Absence équipements protection individuelle — entrepôt",
     "submitter_type": "travailleur", "country": "Mexique",
     "filed_at": "2026-06-21T16:20:00Z", "escalated": False, "resolved": False,
     "assigned_to": "HSE Mexico"},
    {"id": "GRV-2026-008", "channel": "ngo_partner", "severity": "élevé", "stage": "Investigation",
     "subject": "Déplacement forcé communauté — projet infrastructure",
     "submitter_type": "communauté", "country": "Mozambique",
     "filed_at": "2026-06-14T08:00:00Z", "escalated": False, "resolved": False,
     "assigned_to": "Équipe Droits Humains"},
    {"id": "GRV-2026-009", "channel": "community_liaison", "severity": "standard", "stage": "Investigation",
     "subject": "Restriction accès eau potable — zone industrielle",
     "submitter_type": "communauté", "country": "Inde",
     "filed_at": "2026-06-13T10:00:00Z", "escalated": False, "resolved": False,
     "assigned_to": "Équipe Environnement"},
    {"id": "GRV-2026-010", "channel": "digital_form", "severity": "critique", "stage": "Triage",
     "subject": "Représailles après signalement — licenciement abusif présumé",
     "submitter_type": "lanceur_alerte", "country": "Roumanie",
     "filed_at": "2026-06-22T06:00:00Z", "escalated": False, "resolved": False,
     "assigned_to": "Direction Juridique"},
    {"id": "GRV-2026-011", "channel": "hotline", "severity": "standard", "stage": "Résolution",
     "subject": "Conditions sanitaires insuffisantes dortoirs travailleurs migrants",
     "submitter_type": "travailleur", "country": "Qatar",
     "filed_at": "2026-06-10T09:30:00Z", "escalated": False, "resolved": False,
     "assigned_to": "Équipe DD Moyen-Orient"},
    {"id": "GRV-2026-012", "channel": "ngo_partner", "severity": "élevé", "stage": "Investigation",
     "subject": "Travail enfants — sous-traitant coton niveau 3 chaîne valeur",
     "submitter_type": "ong_partenaire", "country": "Pakistan",
     "filed_at": "2026-06-12T11:00:00Z", "escalated": False, "resolved": False,
     "assigned_to": "Équipe Supply Chain"},
    # Résolues
    {"id": "GRV-2026-R01", "channel": "digital_form", "severity": "standard", "stage": "Clôture",
     "subject": "Retard paiement salaires — prestataire nettoyage",
     "submitter_type": "travailleur", "country": "Portugal",
     "filed_at": "2026-06-01T08:00:00Z", "escalated": False, "resolved": True,
     "resolution": "Rappel au prestataire + paiement arriérés confirmé + audit mensuel programmé",
     "resolved_at": "2026-06-14T15:30:00Z"},
    {"id": "GRV-2026-R02", "channel": "community_liaison", "severity": "élevé", "stage": "Clôture",
     "subject": "Nuisances sonores — riverains usine de production",
     "submitter_type": "communauté", "country": "Allemagne",
     "filed_at": "2026-05-28T09:00:00Z", "escalated": False, "resolved": True,
     "resolution": "Installation insonorisation + mesures acoustiques mensuelles + dialogue communautaire",
     "resolved_at": "2026-06-18T10:00:00Z"},
    {"id": "GRV-2026-R03", "channel": "hotline", "severity": "standard", "stage": "Clôture",
     "subject": "Discrimination promotion — genre/nationalité",
     "submitter_type": "travailleur", "country": "Belgique",
     "filed_at": "2026-06-03T14:00:00Z", "escalated": False, "resolved": True,
     "resolution": "Enquête RH conclue, biais identifié dans processus notation, formation DRH programmée",
     "resolved_at": "2026-06-20T16:00:00Z"},
]


# ─── Core agent functions ─────────────────────────────────────────────────────

def get_active_grievances() -> list[dict[str, Any]]:
    return [g for g in SIMULATED_GRIEVANCES if not g.get("resolved", False)]


def get_resolved_grievances() -> list[dict[str, Any]]:
    return [g for g in SIMULATED_GRIEVANCES if g.get("resolved", False)]


def get_escalated_grievances() -> list[dict[str, Any]]:
    return [g for g in SIMULATED_GRIEVANCES if g.get("escalated", False)]


def compute_sla_status(grievance: dict[str, Any]) -> dict[str, Any]:
    """Calcule le statut SLA d'une réclamation."""
    if grievance.get("resolved"):
        return {"status": "closed", "remaining_h": 0, "overdue": False}
    try:
        filed = datetime.datetime.fromisoformat(grievance["filed_at"].replace("Z", "+00:00"))
        now = datetime.datetime.now(datetime.timezone.utc)
        elapsed_h = (now - filed).total_seconds() / 3600
        sla_h = SLA_HOURS.get(grievance["severity"], SLA_HOURS["standard"])
        remaining_h = max(0, sla_h - elapsed_h)
        overdue = elapsed_h > sla_h
        return {
            "status": "overdue" if overdue else "on_track",
            "elapsed_h": round(elapsed_h, 1),
            "sla_h": sla_h,
            "remaining_h": round(remaining_h, 1),
            "overdue": overdue,
            "progress_pct": min(100, round(elapsed_h / sla_h * 100)),
        }
    except (ValueError, KeyError):
        return {"status": "unknown", "remaining_h": None, "overdue": False}


def intake_grievance(
    subject: str,
    channel: str,
    severity: str,
    submitter_type: str,
    country: str,
) -> dict[str, Any]:
    """Enregistre une nouvelle réclamation dans le système."""
    now = datetime.datetime.utcnow()
    grievance_id = f"GRV-{now.year}-{str(uuid.uuid4())[:8].upper()}"
    return {
        "id": grievance_id,
        "channel": channel,
        "severity": severity,
        "stage": "Réception",
        "subject": subject,
        "submitter_type": submitter_type,
        "country": country,
        "filed_at": now.isoformat() + "Z",
        "escalated": False,
        "resolved": False,
        "assigned_to": None,
        "sla_deadline": (
            now + datetime.timedelta(hours=SLA_HOURS.get(severity, 360))
        ).isoformat() + "Z",
    }


def triage_grievance(grievance: dict[str, Any]) -> dict[str, Any]:
    """Effectue le triage automatique d'une réclamation."""
    severity = grievance.get("severity", "standard")
    auto_escalate = severity == "critique"
    assigned_team = {
        "critique": "Direction Conformité + Équipe Droits Humains",
        "élevé": "Équipe Due Diligence",
        "standard": "Équipe Relations Stakeholders",
    }.get(severity, "Équipe Relations Stakeholders")

    grievance["stage"] = "Triage"
    grievance["escalated"] = auto_escalate
    grievance["assigned_to"] = assigned_team
    grievance["triage_notes"] = (
        f"Triage automatique: sévérité {severity}, "
        f"escalade={'oui' if auto_escalate else 'non'}, "
        f"équipe={assigned_team}"
    )
    return grievance


def generate_dashboard(
    active: list[dict[str, Any]],
    resolved: list[dict[str, Any]],
    escalated: list[dict[str, Any]],
) -> dict[str, Any]:
    """Génère le tableau de bord du mécanisme de réclamation."""
    now = datetime.datetime.utcnow()

    by_stage: dict[str, int] = {}
    for g in active:
        by_stage[g["stage"]] = by_stage.get(g["stage"], 0) + 1

    by_severity: dict[str, int] = {}
    for g in active:
        by_severity[g["severity"]] = by_severity.get(g["severity"], 0) + 1

    by_channel: dict[str, int] = {}
    for g in active:
        by_channel[g["channel"]] = by_channel.get(g["channel"], 0) + 1

    by_country: dict[str, int] = {}
    for g in active:
        by_country[g["country"]] = by_country.get(g["country"], 0) + 1

    overdue = [
        g for g in active
        if compute_sla_status(g)["overdue"]
    ]

    return {
        "dashboard_id": f"SGRA-DASH-{now.strftime('%Y%m%d-%H%M%S')}",
        "agent": AGENT_NAME,
        "agent_id": AGENT_ID,
        "generated_at": now.isoformat() + "Z",
        "compliance_frameworks": COMPLIANCE_FRAMEWORKS,
        "summary": {
            "total_active": len(active),
            "total_resolved": len(resolved),
            "total_escalated": len(escalated),
            "overdue": len(overdue),
            "channels_active": len(CHANNELS),
        },
        "by_stage": by_stage,
        "by_severity": by_severity,
        "by_channel": by_channel,
        "top_countries": dict(sorted(by_country.items(), key=lambda x: -x[1])[:5]),
        "escalated_grievances": [
            {
                "id": g["id"],
                "subject": g["subject"],
                "severity": g["severity"],
                "country": g["country"],
                "stage": g["stage"],
                "sla": compute_sla_status(g),
            }
            for g in escalated
        ],
        "overdue_grievances": [
            {
                "id": g["id"],
                "subject": g["subject"],
                "severity": g["severity"],
                "sla": compute_sla_status(g),
            }
            for g in overdue
        ],
        "sla_config": SLA_HOURS,
        "channels": CHANNELS,
    }


def print_banner() -> None:
    print("=" * 72)
    print(f"  CaelumSwarm™ — {AGENT_NAME}")
    print(f"  Agent ID: {AGENT_ID} | Version: {VERSION}")
    print(f"  CSDDD Art.9 | UNGP Pillar III | ISO 37002")
    print(f"  Démarrage: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 72)
    print()


def print_dashboard(dash: dict[str, Any]) -> None:
    s = dash["summary"]
    print("  ┌─ TABLEAU DE BORD RÉCLAMATIONS (CSDDD Art.9) ──────────────────┐")
    print(f"  │  Dashboard ID   : {dash['dashboard_id']}")
    print(f"  │  Généré le      : {dash['generated_at']}")
    print(f"  ├─ STATISTIQUES GLOBALES ───────────────────────────────────────┤")
    print(f"  │  Actives        : {s['total_active']}")
    print(f"  │  Résolues       : {s['total_resolved']}")
    print(f"  │  Escaladées     : {s['total_escalated']}")
    print(f"  │  En retard SLA  : {s['overdue']}")
    print(f"  │  Canaux actifs  : {s['channels_active']}")
    print(f"  └───────────────────────────────────────────────────────────────┘")
    print()

    print("  RÉPARTITION PAR ÉTAPE WORKFLOW :")
    for stage in WORKFLOW_STAGES:
        count = dash["by_stage"].get(stage, 0)
        bar = "▓" * count + "░" * max(0, 12 - count)
        print(f"    {stage:<20} {bar} ({count})")
    print()

    print("  RÉPARTITION PAR SÉVÉRITÉ :")
    severity_colors = {"critique": "●", "élevé": "◉", "standard": "○"}
    for sev, count in dash["by_severity"].items():
        marker = severity_colors.get(sev, "·")
        print(f"    {marker} {sev:<12} : {count} réclamation(s)")
    print()

    print("  CANAUX DE RÉCEPTION :")
    for ch_key, count in dash["by_channel"].items():
        ch_name = CHANNELS.get(ch_key, {}).get("name", ch_key)
        print(f"    ▸ {ch_name:<35} : {count}")
    print()

    print("  TOP PAYS D'ORIGINE :")
    for country, count in dash["top_countries"].items():
        print(f"    ▸ {country:<25} : {count} réclamation(s)")
    print()

    if dash["escalated_grievances"]:
        print("  RÉCLAMATIONS ESCALADÉES :")
        for g in dash["escalated_grievances"]:
            sla = g["sla"]
            sla_info = f"SLA: {sla.get('elapsed_h', '?')}h/{sla.get('sla_h', '?')}h"
            if sla.get("overdue"):
                sla_info += " ⚠ EN RETARD"
            print(f"    ⬆ [{g['severity'].upper()}] {g['id']} — {g['subject'][:55]}")
            print(f"      Pays: {g['country']} | Étape: {g['stage']} | {sla_info}")
        print()

    if dash["overdue_grievances"]:
        print("  RÉCLAMATIONS EN RETARD SLA :")
        for g in dash["overdue_grievances"]:
            sla = g["sla"]
            print(f"    ⚠ {g['id']} [{g['severity']}] — {g['subject'][:55]}")
            print(f"      Retard: {sla.get('elapsed_h', '?')}h (SLA: {sla.get('sla_h', '?')}h)")
        print()

    print("  CONFORMITÉ RÉGLEMENTAIRE :")
    for fw in dash["compliance_frameworks"]:
        print(f"    ✓ {fw}")
    print()

    print("  CANAUX DISPONIBLES :")
    for ch_key, ch in dash["channels"].items():
        anon = "Anonyme" if ch["anonymity"] else "Non-anonyme"
        langs = ", ".join(ch["languages"])
        print(f"    ▸ {ch['name']}")
        print(f"      {anon} | Langues: {langs} | Délai moyen: {ch['avg_response_time_h']}h")
    print()


def print_sla_matrix() -> None:
    print("  MATRICE SLA PAR SÉVÉRITÉ :")
    print(f"    {'Sévérité':<12} {'Délai':<12} {'Conformité'}")
    print(f"    {'─'*40}")
    sla_compliance = {
        "critique": "UNGP + CSDDD Art.9(3)",
        "élevé": "CSDDD Art.9 + ISO 37002",
        "standard": "CSDDD Art.9",
    }
    for sev, hours in SLA_HOURS.items():
        days = hours // 24
        print(f"    {sev:<12} {hours}h ({days}j){'':<4} {sla_compliance.get(sev, '')}")
    print()


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    print_banner()

    print("  [1/5] Initialisation des canaux de réclamation…")
    time.sleep(0.3)
    print(f"         {len(CHANNELS)} canaux configurés : {', '.join(c['name'] for c in CHANNELS.values())}")
    print()

    print("  [2/5] Chargement des réclamations en cours…")
    time.sleep(0.4)
    active = get_active_grievances()
    resolved = get_resolved_grievances()
    escalated = get_escalated_grievances()
    print(f"         {len(active)} actives | {len(resolved)} résolues | {len(escalated)} escaladées")
    print()

    print("  [3/5] Vérification des SLA…")
    time.sleep(0.3)
    overdue = [g for g in active if compute_sla_status(g)["overdue"]]
    print(f"         {len(overdue)} réclamation(s) en retard SLA")
    if overdue:
        for g in overdue:
            sla = compute_sla_status(g)
            print(f"         ⚠ {g['id']} [{g['severity']}] — retard {sla['elapsed_h']}h / SLA {sla['sla_h']}h")
    print()

    print("  [4/5] Simulation réception nouvelle réclamation…")
    time.sleep(0.3)
    new_grievance = intake_grievance(
        subject="Bruit excessif et poussière — riverains carrière test",
        channel="digital_form",
        severity="standard",
        submitter_type="communauté",
        country="Maroc",
    )
    new_grievance = triage_grievance(new_grievance)
    print(f"         Nouvelle réclamation enregistrée : {new_grievance['id']}")
    print(f"         Triage: {new_grievance['triage_notes']}")
    print()

    print("  [5/5] Génération tableau de bord…")
    time.sleep(0.3)
    dashboard = generate_dashboard(active, resolved, escalated)
    print()

    print_dashboard(dashboard)
    print_sla_matrix()

    # Export JSON
    output_path = f"/tmp/sgra_dashboard_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    export_data = {
        "dashboard": dashboard,
        "new_grievance_demo": new_grievance,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
    print(f"  Dashboard JSON exporté : {output_path}")
    print()

    print("=" * 72)
    print(f"  STATUT MÉCANISME RÉCLAMATION : OPÉRATIONNEL")
    print(f"  {len(active)} réclamations actives | {len(resolved)} résolues | {len(escalated)} escaladées")
    print(f"  Conformité CSDDD Art.9 : ACTIVE | UNGP Pillar III : ACTIVE")
    print("=" * 72)

    return 0


if __name__ == "__main__":
    sys.exit(main())
