#!/usr/bin/env python3
"""
CaelumSwarm™ — Regulatory Compliance Monitoring Agent
Surveillance conformité réglementaire automatisée (CSDDD / EU AI Act / GDPR / NIS2 / DORA)
Stdlib Python uniquement.
"""

import json
import datetime
import random
import time
import sys
from typing import Any

# ─── Configuration ────────────────────────────────────────────────────────────

AGENT_ID = "RCMA-001"
AGENT_NAME = "Regulatory Compliance Monitoring Agent"
VERSION = "1.0.0"

FRAMEWORKS = {
    "CSDDD_2024": {
        "name": "Corporate Sustainability Due Diligence Directive",
        "jurisdiction": "EU",
        "entry_into_force": "2024-07-25",
        "compliance_deadline": "2027-07-26",
        "articles_monitored": ["Art.5", "Art.7", "Art.8", "Art.9", "Art.11", "Art.22"],
        "risk_domains": ["supply_chain", "human_rights", "environment"],
    },
    "EU_AI_ACT": {
        "name": "EU Artificial Intelligence Act",
        "jurisdiction": "EU",
        "entry_into_force": "2024-08-01",
        "compliance_deadline": "2026-08-02",
        "articles_monitored": ["Art.6", "Art.9", "Art.10", "Art.13", "Art.17", "Art.43"],
        "risk_domains": ["high_risk_ai", "transparency", "human_oversight"],
    },
    "GDPR": {
        "name": "General Data Protection Regulation",
        "jurisdiction": "EU",
        "entry_into_force": "2018-05-25",
        "compliance_deadline": "2018-05-25",
        "articles_monitored": ["Art.5", "Art.13", "Art.17", "Art.25", "Art.30", "Art.35"],
        "risk_domains": ["data_processing", "data_rights", "data_transfers"],
    },
    "NIS2": {
        "name": "Network and Information Security Directive 2",
        "jurisdiction": "EU",
        "entry_into_force": "2023-01-16",
        "compliance_deadline": "2024-10-18",
        "articles_monitored": ["Art.18", "Art.20", "Art.21", "Art.23", "Art.24"],
        "risk_domains": ["cybersecurity", "incident_reporting", "supply_chain_security"],
    },
    "DORA": {
        "name": "Digital Operational Resilience Act",
        "jurisdiction": "EU",
        "entry_into_force": "2023-01-16",
        "compliance_deadline": "2025-01-17",
        "articles_monitored": ["Art.5", "Art.9", "Art.11", "Art.17", "Art.19", "Art.26"],
        "risk_domains": ["ict_risk", "operational_resilience", "third_party_ict"],
    },
}

COMPLIANCE_SCORES: dict[str, int] = {
    "CSDDD_2024": 72,
    "EU_AI_ACT": 68,
    "GDPR": 91,
    "NIS2": 79,
    "DORA": 81,
}

ACTIVE_ALERTS = [
    {
        "alert_id": "ALT-2026-001",
        "framework": "CSDDD_2024",
        "severity": "critique",
        "title": "Transposition nationale incomplète — 7 États membres",
        "description": (
            "Allemagne, France, Italie, Pologne, Hongrie, Roumanie, Grèce n'ont pas "
            "encore transposé la CSDDD en droit national. Risque de fragmentation "
            "réglementaire pour les entreprises opérant dans plusieurs juridictions."
        ),
        "article": "Art.37 CSDDD",
        "detected_at": "2026-06-18T09:15:00Z",
        "ecj_referral_risk": "élevé",
        "recommended_action": "Surveiller les projets de loi nationaux; adapter les politiques DD par juridiction",
    },
    {
        "alert_id": "ALT-2026-002",
        "framework": "EU_AI_ACT",
        "severity": "élevé",
        "title": "Nouvelles lignes directrices GPAI — Clarifications systèmes généraux",
        "description": (
            "L'AI Office publie des lignes directrices révisées sur les obligations "
            "des fournisseurs de modèles GPAI (General Purpose AI). Nouvelles exigences "
            "de documentation et d'évaluation des risques systémiques."
        ),
        "article": "Art.52-55 EU AI Act",
        "detected_at": "2026-06-20T14:30:00Z",
        "ecj_referral_risk": "modéré",
        "recommended_action": "Réviser les registres de systèmes IA; mettre à jour les notices de transparence",
    },
    {
        "alert_id": "ALT-2026-003",
        "framework": "GDPR",
        "severity": "modéré",
        "title": "Décision CEPD — Transferts données vers pays tiers (mécanisme SCC révisé)",
        "description": (
            "Le Comité Européen de la Protection des Données publie une décision "
            "contraignante sur les Clauses Contractuelles Types révisées pour les "
            "transferts vers les États-Unis post-Privacy Shield 2."
        ),
        "article": "Art.46 GDPR",
        "detected_at": "2026-06-21T11:00:00Z",
        "ecj_referral_risk": "faible",
        "recommended_action": "Auditer les contrats de transfert existants; mettre à jour les SCC si nécessaire",
    },
]

ECJ_CASES = [
    {
        "case_id": "C-2025-341",
        "title": "Commission v. Allemagne — Non-transposition CSDDD",
        "status": "procédure_précontentieuse",
        "filed": "2025-11-15",
        "relevance": "CSDDD_2024",
        "potential_fine": "EUR 85M/jour",
    },
    {
        "case_id": "C-2024-892",
        "title": "Schrems IV — Transferts données personnelles",
        "status": "instruction",
        "filed": "2024-09-03",
        "relevance": "GDPR",
        "potential_fine": "N/A (annulation décision adéquation)",
    },
    {
        "case_id": "C-2026-118",
        "title": "Meta Platforms — Traitement données comportementales à grande échelle",
        "status": "arrêt_rendu",
        "filed": "2025-03-22",
        "relevance": "GDPR",
        "potential_fine": "EUR 1.2Md (arrêt confirmé)",
    },
]


# ─── Core agent functions ─────────────────────────────────────────────────────

def compute_global_score(scores: dict[str, int]) -> int:
    """Calcule le score de conformité global pondéré."""
    weights = {
        "CSDDD_2024": 0.30,
        "EU_AI_ACT": 0.20,
        "GDPR": 0.25,
        "NIS2": 0.15,
        "DORA": 0.10,
    }
    total = sum(scores[fw] * w for fw, w in weights.items())
    return round(total)


def risk_label(score: int) -> str:
    if score >= 80:
        return "CONFORME"
    if score >= 60:
        return "PARTIELLEMENT CONFORME"
    if score >= 40:
        return "NON-CONFORME PARTIEL"
    return "NON-CONFORME"


def monitor_frameworks() -> list[dict[str, Any]]:
    """Simule une passe de surveillance des frameworks réglementaires."""
    results = []
    now = datetime.datetime.utcnow().isoformat() + "Z"
    for fw_key, fw in FRAMEWORKS.items():
        score = COMPLIANCE_SCORES.get(fw_key, 75)
        # Légère variation simulée (±2 pts)
        score = max(0, min(100, score + random.randint(-2, 2)))
        results.append({
            "framework": fw_key,
            "name": fw["name"],
            "jurisdiction": fw["jurisdiction"],
            "compliance_score": score,
            "status": risk_label(score),
            "articles_monitored": fw["articles_monitored"],
            "last_check": now,
        })
    return results


def check_alerts() -> list[dict[str, Any]]:
    """Retourne les alertes réglementaires actives."""
    return ACTIVE_ALERTS


def track_ecj_cases() -> list[dict[str, Any]]:
    """Retourne le suivi des affaires ECJ (Cour de Justice Européenne)."""
    return ECJ_CASES


def generate_compliance_report(
    monitoring_results: list[dict[str, Any]],
    alerts: list[dict[str, Any]],
    ecj_cases: list[dict[str, Any]],
) -> dict[str, Any]:
    """Génère un rapport de conformité structuré."""
    global_score = compute_global_score(COMPLIANCE_SCORES)
    now = datetime.datetime.utcnow()

    critical_alerts = [a for a in alerts if a["severity"] == "critique"]
    elevated_alerts = [a for a in alerts if a["severity"] == "élevé"]
    moderate_alerts = [a for a in alerts if a["severity"] == "modéré"]

    return {
        "report_id": f"RCMA-RPT-{now.strftime('%Y%m%d-%H%M%S')}",
        "agent": AGENT_NAME,
        "agent_id": AGENT_ID,
        "version": VERSION,
        "generated_at": now.isoformat() + "Z",
        "reporting_period": {
            "start": (now - datetime.timedelta(days=1)).isoformat() + "Z",
            "end": now.isoformat() + "Z",
        },
        "executive_summary": {
            "global_compliance_score": global_score,
            "global_status": risk_label(global_score),
            "frameworks_monitored": len(FRAMEWORKS),
            "active_alerts": len(alerts),
            "critical_alerts": len(critical_alerts),
            "elevated_alerts": len(elevated_alerts),
            "ecj_cases_tracked": len(ecj_cases),
        },
        "framework_scores": monitoring_results,
        "alerts": {
            "critique": critical_alerts,
            "élevé": elevated_alerts,
            "modéré": moderate_alerts,
        },
        "ecj_case_tracking": ecj_cases,
        "recommendations": [
            "Prioriser la mise en conformité CSDDD_2024 — délai 2027",
            "Accélérer l'audit EU AI Act sur les systèmes IA à haut risque",
            "Mettre à jour les SCC en attente de la décision CEPD finale",
            "Renforcer les capacités NIS2 de détection/réponse incidents",
        ],
        "next_review": (now + datetime.timedelta(hours=6)).isoformat() + "Z",
    }


def print_banner() -> None:
    print("=" * 72)
    print(f"  CaelumSwarm™ — {AGENT_NAME}")
    print(f"  Agent ID: {AGENT_ID} | Version: {VERSION}")
    print(f"  Démarrage: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 72)
    print()


def print_report(report: dict[str, Any]) -> None:
    es = report["executive_summary"]
    print(f"  ┌─ RAPPORT DE CONFORMITÉ RÉGLEMENTAIRE ─────────────────────────┐")
    print(f"  │  ID rapport   : {report['report_id']}")
    print(f"  │  Généré le    : {report['generated_at']}")
    print(f"  ├─ SCORE GLOBAL ────────────────────────────────────────────────┤")
    print(f"  │  Score        : {es['global_compliance_score']}/100")
    print(f"  │  Statut       : {es['global_status']}")
    print(f"  │  Frameworks   : {es['frameworks_monitored']}")
    print(f"  ├─ ALERTES ─────────────────────────────────────────────────────┤")
    print(f"  │  Totales      : {es['active_alerts']}")
    print(f"  │  Critiques    : {es['critical_alerts']}")
    print(f"  │  Élevées      : {es['elevated_alerts']}")
    print(f"  │  Affaires ECJ : {es['ecj_cases_tracked']}")
    print(f"  └───────────────────────────────────────────────────────────────┘")
    print()

    print("  SCORES PAR FRAMEWORK :")
    for fw in report["framework_scores"]:
        bar_len = fw["compliance_score"] // 5
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"    {fw['framework']:<20} {bar} {fw['compliance_score']:>3}/100  [{fw['status']}]")
    print()

    print("  ALERTES RÉGLEMENTAIRES ACTIVES :")
    all_alerts = (
        report["alerts"]["critique"]
        + report["alerts"]["élevé"]
        + report["alerts"]["modéré"]
    )
    for alert in all_alerts:
        severity_marker = {"critique": "🔴", "élevé": "🟠", "modéré": "🟡"}.get(alert["severity"], "⚪")
        print(f"    {severity_marker} [{alert['severity'].upper()}] {alert['alert_id']}")
        print(f"       {alert['title']}")
        print(f"       Framework: {alert['framework']} | Article: {alert['article']}")
        print(f"       Action: {alert['recommended_action']}")
        print()

    print("  SUIVI AFFAIRES ECJ :")
    for case in report["ecj_case_tracking"]:
        print(f"    ▸ {case['case_id']} — {case['title']}")
        print(f"      Statut: {case['status']} | Amende potentielle: {case['potential_fine']}")
        print()

    print("  RECOMMANDATIONS :")
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"    {i}. {rec}")
    print()
    print(f"  Prochaine révision : {report['next_review']}")
    print()


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    print_banner()

    print("  [1/4] Initialisation des frameworks réglementaires…")
    time.sleep(0.3)
    print(f"         {len(FRAMEWORKS)} frameworks chargés : {', '.join(FRAMEWORKS.keys())}")
    print()

    print("  [2/4] Surveillance des frameworks en cours…")
    time.sleep(0.5)
    monitoring_results = monitor_frameworks()
    print(f"         {len(monitoring_results)} frameworks analysés avec succès")
    print()

    print("  [3/4] Vérification des alertes réglementaires…")
    time.sleep(0.3)
    alerts = check_alerts()
    print(f"         {len(alerts)} alertes détectées ({sum(1 for a in alerts if a['severity'] == 'critique')} critiques)")
    print()

    print("  [4/4] Suivi des affaires ECJ…")
    time.sleep(0.3)
    ecj_cases = track_ecj_cases()
    print(f"         {len(ecj_cases)} affaires suivies")
    print()

    print("  Génération du rapport de conformité…")
    time.sleep(0.2)
    report = generate_compliance_report(monitoring_results, alerts, ecj_cases)
    print()

    print_report(report)

    # Sortie JSON pour intégration pipeline
    output_path = f"/tmp/rcma_report_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"  Rapport JSON exporté : {output_path}")
    print()

    global_score = report["executive_summary"]["global_compliance_score"]
    print("=" * 72)
    print(f"  SCORE GLOBAL CONFORMITÉ : {global_score}/100 — {risk_label(global_score)}")
    print(f"  {len(alerts)} alertes actives | {len(ecj_cases)} affaires ECJ suivies")
    print("=" * 72)

    return 0


if __name__ == "__main__":
    sys.exit(main())
