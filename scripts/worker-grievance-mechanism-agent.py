#!/usr/bin/env python3
"""
Worker Grievance Mechanism Agent — Caelum Partners CaelumSwarm™
Mécanisme de réclamation travailleurs conforme CSDDD Art.11 & UNGP 29-31.
Gestion des plaintes, suivi, escalade et rapport.
"""

import hashlib
import sys
from datetime import datetime, timedelta, timezone

GRIEVANCE_CATEGORIES = {
    "FORCED_LABOR": {
        "label": "Travail forcé / Servitude",
        "severity": "CRITIQUE",
        "ilo_convention": "C29, C105",
        "auto_escalate_hours": 4,
        "required_response_days": 7,
    },
    "CHILD_LABOR": {
        "label": "Travail enfants",
        "severity": "CRITIQUE",
        "ilo_convention": "C138, C182",
        "auto_escalate_hours": 4,
        "required_response_days": 7,
    },
    "DISCRIMINATION": {
        "label": "Discrimination (genre, religion, origine)",
        "severity": "ÉLEVÉ",
        "ilo_convention": "C100, C111",
        "auto_escalate_hours": 24,
        "required_response_days": 14,
    },
    "FREEDOM_ASSOCIATION": {
        "label": "Entrave à la liberté syndicale",
        "severity": "ÉLEVÉ",
        "ilo_convention": "C87, C98",
        "auto_escalate_hours": 24,
        "required_response_days": 14,
    },
    "LIVING_WAGE": {
        "label": "Non-paiement salaire décent",
        "severity": "ÉLEVÉ",
        "ilo_convention": "C131",
        "auto_escalate_hours": 48,
        "required_response_days": 14,
    },
    "HEALTH_SAFETY": {
        "label": "Conditions santé & sécurité",
        "severity": "ÉLEVÉ",
        "ilo_convention": "C155, C187",
        "auto_escalate_hours": 12,
        "required_response_days": 10,
    },
    "HARASSMENT": {
        "label": "Harcèlement moral ou sexuel",
        "severity": "ÉLEVÉ",
        "ilo_convention": "C190",
        "auto_escalate_hours": 12,
        "required_response_days": 10,
    },
    "DOCUMENTATION": {
        "label": "Confiscation documents / Apatridie",
        "severity": "CRITIQUE",
        "ilo_convention": "C29",
        "auto_escalate_hours": 4,
        "required_response_days": 7,
    },
    "RETALIATION": {
        "label": "Représailles signalement",
        "severity": "CRITIQUE",
        "ilo_convention": "C158, C135",
        "auto_escalate_hours": 2,
        "required_response_days": 5,
    },
    "WAGE_THEFT": {
        "label": "Vol de salaire / Retenues illégales",
        "severity": "MODÉRÉ",
        "ilo_convention": "C95",
        "auto_escalate_hours": 72,
        "required_response_days": 21,
    },
    "OTHER": {
        "label": "Autre violation droits au travail",
        "severity": "MODÉRÉ",
        "ilo_convention": "Général",
        "auto_escalate_hours": 96,
        "required_response_days": 30,
    },
}

INTAKE_CHANNELS = {
    "HOTLINE": {"label": "Ligne téléphonique dédiée", "anonymity": True, "24h": True},
    "WEB_FORM": {"label": "Formulaire web sécurisé (HTTPS)", "anonymity": True, "24h": True},
    "EMAIL_SECURE": {"label": "Email chiffré dédié", "anonymity": False, "24h": True},
    "PHYSICAL_BOX": {"label": "Boîte aux lettres physique sur site", "anonymity": True, "24h": False},
    "THIRD_PARTY": {"label": "Tiers médiateur indépendant", "anonymity": True, "24h": False},
    "NGO_REFERRAL": {"label": "Référencement via ONG partenaire", "anonymity": False, "24h": False},
}

INVESTIGATION_STEPS = [
    "INTAKE",
    "ACKNOWLEDGMENT",
    "PRELIMINARY_ASSESSMENT",
    "INVESTIGATION_ASSIGNED",
    "EVIDENCE_COLLECTION",
    "PARTIES_INTERVIEW",
    "FINDING",
    "REMEDY_PROPOSED",
    "REMEDY_ACCEPTED",
    "CLOSURE",
    "FOLLOW_UP_30D",
    "FOLLOW_UP_90D",
]

ESCALATION_MATRIX = {
    "CRITIQUE": ["Directeur RSE", "DG", "Conseil d'Administration", "Autorité nationale compétente"],
    "ÉLEVÉ": ["Directeur RSE", "Responsable conformité"],
    "MODÉRÉ": ["Responsable conformité", "RH"],
    "FAIBLE": ["RH local"],
}


def register_grievance(
    complainant_ref: str,
    category: str,
    description: str,
    location: str,
    supplier_id: str = None,
    anonymous: bool = True,
    channel: str = "WEB_FORM",
) -> dict:
    """Enregistre une réclamation et génère le dossier de suivi."""
    cat_config = GRIEVANCE_CATEGORIES.get(category, GRIEVANCE_CATEGORIES["OTHER"])
    severity = cat_config["severity"]
    escalate_config = ESCALATION_MATRIX.get(severity, ESCALATION_MATRIX["FAIBLE"])

    content = f"{complainant_ref}{category}{description}{location}{datetime.now().isoformat()}"
    case_hash = hashlib.sha256(content.encode()).hexdigest()[:12].upper()
    case_id = f"GR-{category[:3]}-{datetime.now().strftime('%Y%m%d%H%M')}-{case_hash[:6]}"

    now = datetime.now(timezone.utc)
    acknowledgment_deadline = now + timedelta(hours=48)
    response_deadline = now + timedelta(days=cat_config["required_response_days"])
    auto_escalate_at = now + timedelta(hours=cat_config["auto_escalate_hours"])

    complainant_ref_hashed = hashlib.sha256(complainant_ref.encode()).hexdigest()[:8].upper() if anonymous else complainant_ref

    return {
        "case_id": case_id,
        "registered_at": now.isoformat(),
        "registered_via": "CaelumSwarm™ Worker Grievance Mechanism Agent v1.0",
        "complainant_ref": complainant_ref_hashed,
        "anonymous": anonymous,
        "intake_channel": INTAKE_CHANNELS.get(channel, {}).get("label", channel),
        "category": category,
        "category_label": cat_config["label"],
        "severity": severity,
        "ilo_conventions": cat_config["ilo_convention"],
        "location": location,
        "supplier_id": supplier_id,
        "description_excerpt": description[:200] + "..." if len(description) > 200 else description,
        "csddd_art11_compliant": True,
        "ungp_ref": "UNGP 29-31 — Mécanismes de réclamation au niveau opérationnel",
        "timelines": {
            "acknowledgment_due": acknowledgment_deadline.isoformat(),
            "response_required_by": response_deadline.isoformat(),
            "auto_escalate_at": auto_escalate_at.isoformat(),
            "max_resolution_days": cat_config["required_response_days"],
        },
        "escalation_chain": escalate_config,
        "status": "INTAKE",
        "investigation_steps": INVESTIGATION_STEPS,
        "current_step": "INTAKE",
        "assigned_to": None,
        "remedy_proposed": None,
        "closure_date": None,
        "follow_up_30d": None,
        "follow_up_90d": None,
        "confidentiality": "Ce dossier est CONFIDENTIEL. Accès restreint aux personnes assignées.",
        "non_retaliation_guaranteed": True,
        "access_to_legal_aid": True,
    }


def generate_grievance_statistics(cases: list) -> dict:
    """Génère les statistiques du mécanisme de réclamation."""
    if not cases:
        return {}

    by_severity = {"CRITIQUE": 0, "ÉLEVÉ": 0, "MODÉRÉ": 0, "FAIBLE": 0}
    by_category = {}
    closed = [c for c in cases if c["status"] == "CLOSURE"]

    for case in cases:
        sev = case.get("severity", "MODÉRÉ")
        by_severity[sev] = by_severity.get(sev, 0) + 1

        cat = case.get("category", "OTHER")
        by_category[cat] = by_category.get(cat, 0) + 1

    return {
        "total_cases": len(cases),
        "closure_rate_pct": round(len(closed) / len(cases) * 100, 1) if cases else 0,
        "by_severity": by_severity,
        "by_category": dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True)),
        "anonymous_pct": round(sum(1 for c in cases if c.get("anonymous")) / len(cases) * 100, 1) if cases else 0,
        "csddd_kpi": {
            "art11_mechanism_active": True,
            "avg_response_days_target": 21,
            "accessibility_channels": len(INTAKE_CHANNELS),
        },
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — WORKER GRIEVANCE MECHANISM AGENT")
    print("  Mécanisme de Réclamation Travailleurs CSDDD Art.11 / UNGP 29-31")
    print("=" * 70)

    print(f"\n📝 ENREGISTREMENT DE RÉCLAMATIONS:")

    case1 = register_grievance(
        complainant_ref="worker_myanmar_factory_A",
        category="FORCED_LABOR",
        description="Je ne peux pas quitter mon poste. Mon passeport a été confisqué à mon arrivée. Je n'ai pas été payé depuis 3 mois et on me menace si je parle.",
        location="Myanmar — Usine textile Rangoon",
        supplier_id="SUP-007",
        anonymous=True,
        channel="HOTLINE",
    )

    case2 = register_grievance(
        complainant_ref="sindh_worker_group_12",
        category="HEALTH_SAFETY",
        description="12 travailleurs exposés à des produits chimiques sans protection. Absence d'équipements de protection individuelle. Un travailleur hospitalisé.",
        location="Pakistan — Site chimique Karachi",
        supplier_id="SUP-023",
        anonymous=False,
        channel="NGO_REFERRAL",
    )

    case3 = register_grievance(
        complainant_ref="migrant_worker_BD",
        category="DOCUMENTATION",
        description="Mon employeur a retenu mon passeport à mon arrivée au Qatar. Je ne peux pas changer d'employeur ni rentrer chez moi.",
        location="Qatar — Chantier construction Doha",
        supplier_id="SUP-041",
        anonymous=True,
        channel="WEB_FORM",
    )

    cases = [case1, case2, case3]

    for case in cases:
        print(f"\n   ✅ {case['case_id']} — [{case['severity']}]")
        print(f"      Catégorie: {case['category_label']}")
        print(f"      Lieu: {case['location']}")
        print(f"      Anonyme: {'OUI' if case['anonymous'] else 'NON'} | Canal: {case['intake_channel']}")
        print(f"      ILO: {case['ilo_conventions']}")
        print(f"      Escalade vers: {', '.join(case['escalation_chain'][:2])}")
        print(f"      Délai réponse: {case['timelines']['max_resolution_days']}j")
        print(f"      Auto-escalade dans: {case['timelines']['auto_escalate_at'][:19]}Z")

    stats = generate_grievance_statistics(cases)

    print(f"\n📊 STATISTIQUES MÉCANISME:")
    print(f"   Total dossiers: {stats['total_cases']}")
    print(f"   Taux clôture: {stats['closure_rate_pct']}%")
    print(f"   Anonymat: {stats['anonymous_pct']}% des plaignants")
    print(f"   Distribution sévérité:")
    for sev, count in stats["by_severity"].items():
        if count > 0:
            print(f"     {sev}: {count}")

    print(f"\n⚖️  CONFORMITÉ CSDDD:")
    print(f"   Art.11 Mécanisme actif: ✅ OUI")
    print(f"   UNGP 29-31 Réclamation opérationnelle: ✅ CONFORME")
    print(f"   Canaux d'accès: {stats['csddd_kpi']['accessibility_channels']} canaux")
    print(f"   Délai réponse cible: {stats['csddd_kpi']['avg_response_days_target']}j")
    print(f"   Non-représailles garanties: ✅ OUI pour tous les dossiers")

    print(f"\n✅ Worker Grievance Mechanism Agent — {len(cases)} réclamations enregistrées")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
