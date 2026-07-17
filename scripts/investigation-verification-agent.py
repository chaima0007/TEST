#!/usr/bin/env python3
"""
Investigation & Verification Agent — Caelum Partners CaelumSwarm™
Enquêteur expert : vérifie et valide les signalements droits humains.
Méthode structurée : collecte preuves, corroboration, finding officiel.
"""

import hashlib
import sys
from datetime import datetime, timedelta, timezone

INVESTIGATION_PHASES = {
    "INTAKE_SCREENING": {
        "duration_days": 2,
        "actions": ["Réception signalement", "Vérification non-doublon", "Tri par sévérité", "Attribution enquêteur"],
        "output": "Décision ouverture enquête",
    },
    "PRELIMINARY_ASSESSMENT": {
        "duration_days": 5,
        "actions": ["Revue sources existantes", "Évaluation crédibilité initiale", "Plan d'enquête"],
        "output": "Rapport préliminaire",
    },
    "EVIDENCE_COLLECTION": {
        "duration_days": 21,
        "actions": ["Collecte documents", "Interviews témoins", "Analyse satellite/photos", "Croisement données CaelumSwarm™"],
        "output": "Dossier de preuves",
    },
    "CORROBORATION": {
        "duration_days": 10,
        "actions": ["Tri-angulation 3 sources minimum", "Validation expert tier", "Vérification faits contradictoires"],
        "output": "Rapport de corroboration",
    },
    "ADVERSARIAL_REVIEW": {
        "duration_days": 7,
        "actions": ["Notification partie mise en cause", "Droit de réponse", "Révision si nouveaux éléments"],
        "output": "Réponse partie mise en cause",
    },
    "FINDING": {
        "duration_days": 5,
        "actions": ["Rédaction finding officiel", "Qualification juridique", "Recommandations"],
        "output": "Finding officiel signé",
    },
    "REMEDIATION_MONITORING": {
        "duration_days": 90,
        "actions": ["Suivi plan correctif", "Vérification mise en œuvre", "Rapport d'avancement 30/60/90j"],
        "output": "Rapport clôture enquête",
    },
}

VERIFICATION_STANDARDS = {
    "CREDIBILITY_THRESHOLD": 0.65,
    "CORROBORATION_SOURCES_MIN": 3,
    "RESPONSE_TIME_DAYS": 30,
    "FINDING_CONFIDENCE_MIN": 0.70,
}

EVIDENCE_SCORING = {
    "physical_document": 0.90,
    "signed_testimony": 0.80,
    "photographic_evidence": 0.75,
    "witness_interview": 0.70,
    "statistical_data": 0.85,
    "satellite_imagery": 0.92,
    "ngo_report": 0.78,
    "media_report": 0.55,
    "anonymous_tip": 0.30,
    "social_media": 0.25,
}

FINDING_TYPES = {
    "SUBSTANTIATED": {
        "label": "Signalement fondé",
        "description": "Les preuves établissent la violation avec un niveau de confiance ≥70%",
        "action": "Rapport officiel + Plan correctif obligatoire",
        "csddd_trigger": True,
    },
    "PARTIALLY_SUBSTANTIATED": {
        "label": "Partiellement fondé",
        "description": "Certains éléments confirmés, d'autres pas suffisamment documentés",
        "action": "Enquête complémentaire + Mesures préventives",
        "csddd_trigger": True,
    },
    "UNSUBSTANTIATED": {
        "label": "Non fondé",
        "description": "Les preuves ne supportent pas les allégations",
        "action": "Classement avec documentation — rester en veille",
        "csddd_trigger": False,
    },
    "INCONCLUSIVE": {
        "label": "Inconclusive",
        "description": "Preuves insuffisantes pour trancher",
        "action": "Enquête rouverte si nouvelles preuves",
        "csddd_trigger": False,
    },
}

INVESTIGATOR_PROFILES = [
    {"id": "INV-001", "name": "Expert Travail ILO certifié", "specialties": ["forced_labor", "child_labor", "living_wage"]},
    {"id": "INV-002", "name": "Expert Droits Numériques", "specialties": ["deepfake", "surveillance", "data_rights"]},
    {"id": "INV-003", "name": "Expert Finance & Corruption", "specialties": ["offshore", "money_laundering", "bribery"]},
    {"id": "INV-004", "name": "Expert Apatridie & Migration", "specialties": ["statelessness", "documentation", "refugees"]},
    {"id": "INV-005", "name": "Expert Environnement & Droits", "specialties": ["land_grabbing", "pollution", "indigenous"]},
]


def assign_investigator(category: str) -> dict:
    """Assigne l'enquêteur le plus approprié selon la catégorie."""
    category_lower = category.lower()
    for inv in INVESTIGATOR_PROFILES:
        if any(spec in category_lower for spec in inv["specialties"]):
            return inv
    return INVESTIGATOR_PROFILES[0]


def open_investigation(
    case_id: str,
    allegation: str,
    category: str,
    severity: str,
    evidence_list: list,
    entity_id: str,
) -> dict:
    """Ouvre une enquête formelle sur un signalement."""
    now = datetime.now(timezone.utc)
    total_duration = sum(p["duration_days"] for p in INVESTIGATION_PHASES.values())
    expected_close = now + timedelta(days=total_duration)
    investigator = assign_investigator(category)

    evidence_scores = []
    for ev in evidence_list:
        ev_type = ev.get("type", "anonymous_tip")
        score = EVIDENCE_SCORING.get(ev_type, 0.30)
        evidence_scores.append(score)

    avg_evidence_strength = sum(evidence_scores) / len(evidence_scores) if evidence_scores else 0
    credible = avg_evidence_strength >= VERIFICATION_STANDARDS["CREDIBILITY_THRESHOLD"]
    corroborated = len(evidence_list) >= VERIFICATION_STANDARDS["CORROBORATION_SOURCES_MIN"]

    investigation_id = f"INV-{entity_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    inv_hash = hashlib.sha256(f"{investigation_id}{allegation}".encode()).hexdigest()[:12].upper()

    phases_schedule = []
    current_day = 0
    for phase_name, phase_config in INVESTIGATION_PHASES.items():
        phases_schedule.append({
            "phase": phase_name,
            "start_day": current_day,
            "end_day": current_day + phase_config["duration_days"],
            "actions": phase_config["actions"],
            "output": phase_config["output"],
        })
        current_day += phase_config["duration_days"]

    return {
        "investigation_id": investigation_id,
        "case_id": case_id,
        "integrity_hash": f"SHA256:{inv_hash}",
        "opened_at": now.isoformat(),
        "opened_by": "CaelumSwarm™ Investigation Agent v1.0",
        "entity_id": entity_id,
        "allegation": allegation,
        "category": category,
        "severity": severity,
        "assigned_investigator": investigator,
        "evidence_assessment": {
            "evidence_count": len(evidence_list),
            "avg_strength": round(avg_evidence_strength, 3),
            "credible": credible,
            "corroborated": corroborated,
            "sources_min_met": corroborated,
            "preliminary_finding": (
                "PROMISING" if credible and corroborated
                else "NEEDS_MORE_EVIDENCE" if credible
                else "WEAK_BASIS"
            ),
        },
        "timeline": {
            "opened": now.isoformat(),
            "expected_finding": (now + timedelta(days=43)).isoformat(),
            "expected_close": expected_close.isoformat(),
            "total_days": total_duration,
        },
        "phases_schedule": phases_schedule,
        "csddd_implications": {
            "art8_identification": True,
            "art9_prevention": severity in ("CRITIQUE", "ÉLEVÉ"),
            "art10_cessation": severity == "CRITIQUE",
            "art11_grievance": case_id is not None,
        },
        "status": "INTAKE_SCREENING",
        "confidentiality": "CONFIDENTIEL — Équipe enquête uniquement",
        "right_of_reply_deadline": (now + timedelta(days=35)).isoformat(),
    }


def generate_finding(investigation: dict, confidence: float) -> dict:
    """Génère un finding officiel d'enquête."""
    ev_strength = investigation["evidence_assessment"]["avg_strength"]
    credible = investigation["evidence_assessment"]["credible"]
    corroborated = investigation["evidence_assessment"]["corroborated"]

    if confidence >= 0.80 and credible and corroborated:
        finding_type = "SUBSTANTIATED"
    elif confidence >= 0.60 and credible:
        finding_type = "PARTIALLY_SUBSTANTIATED"
    elif confidence < 0.40:
        finding_type = "UNSUBSTANTIATED"
    else:
        finding_type = "INCONCLUSIVE"

    finding_config = FINDING_TYPES[finding_type]

    return {
        "finding_id": f"FIND-{investigation['investigation_id'][-8:]}",
        "investigation_id": investigation["investigation_id"],
        "finding_type": finding_type,
        "finding_label": finding_config["label"],
        "description": finding_config["description"],
        "confidence_score": confidence,
        "evidence_strength": ev_strength,
        "csddd_trigger": finding_config["csddd_trigger"],
        "required_action": finding_config["action"],
        "signed_by": investigation["assigned_investigator"]["name"],
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "appeal_deadline_days": 30,
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — INVESTIGATION & VERIFICATION AGENT")
    print("  Enquêteur Expert Signalements Droits Humains")
    print("=" * 70)

    evidence_list = [
        {"type": "satellite_imagery", "description": "Images UNOSAT destruction villages"},
        {"type": "ngo_report", "description": "Rapport HRW Myanmar 2024"},
        {"type": "statistical_data", "description": "UNHCR données 1.08M apatrides"},
        {"type": "signed_testimony", "description": "Témoignage signé 12 survivants"},
    ]

    investigation = open_investigation(
        case_id="GR-DOC-202412-A3F8B2",
        allegation="Confiscation systématique documents identité Rohingyas, privation citoyenneté, travail forcé dans camps",
        category="documentation_statelessness_forced_labor",
        severity="CRITIQUE",
        evidence_list=evidence_list,
        entity_id="SDR-001",
    )

    print(f"\n🔍 ENQUÊTE OUVERTE: {investigation['investigation_id']}")
    print(f"   Dossier: {investigation['case_id']}")
    print(f"   Hash intégrité: {investigation['integrity_hash']}")
    print(f"   Entité: {investigation['entity_id']}")
    print(f"   Sévérité: {investigation['severity']}")
    print(f"\n   Enquêteur assigné: {investigation['assigned_investigator']['name']}")
    print(f"   Spécialités: {', '.join(investigation['assigned_investigator']['specialties'])}")

    ev = investigation["evidence_assessment"]
    print(f"\n📋 ÉVALUATION DES PREUVES:")
    print(f"   Nombre de preuves: {ev['evidence_count']}")
    print(f"   Force moyenne: {ev['avg_strength']*100:.1f}%")
    print(f"   Crédible: {'✅ OUI' if ev['credible'] else '❌ NON'}")
    print(f"   Corroborée (≥3 sources): {'✅ OUI' if ev['corroborated'] else '❌ NON'}")
    print(f"   Évaluation préliminaire: {ev['preliminary_finding']}")

    t = investigation["timeline"]
    print(f"\n📅 CALENDRIER ENQUÊTE:")
    print(f"   Ouverture: {t['opened'][:10]}")
    print(f"   Finding attendu: {t['expected_finding'][:10]}")
    print(f"   Clôture prévue: {t['expected_close'][:10]}")
    print(f"   Durée totale: {t['total_days']} jours")

    print(f"\n📊 PHASES:")
    for phase in investigation["phases_schedule"][:4]:
        print(f"   J{phase['start_day']:3d}-J{phase['end_day']:3d} — {phase['phase']}")
        print(f"      Output: {phase['output']}")

    print(f"\n⚖️  IMPLICATIONS CSDDD:")
    for art, triggered in investigation["csddd_implications"].items():
        icon = "✅" if triggered else "➖"
        print(f"   {icon} {art.replace('_', ' ').upper()}")

    finding = generate_finding(investigation, confidence=0.85)
    print(f"\n📋 FINDING SIMULÉ (confiance 85%):")
    print(f"   Type: {finding['finding_type']} — {finding['finding_label']}")
    print(f"   Description: {finding['description']}")
    print(f"   Action requise: {finding['required_action']}")
    print(f"   CSDDD Art.10 déclenché: {'✅ OUI' if finding['csddd_trigger'] else '❌ NON'}")

    print(f"\n✅ Investigation & Verification Agent — Enquête ouverte avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
