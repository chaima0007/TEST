#!/usr/bin/env python3
"""
Training & Awareness Agent — Caelum Partners CaelumSwarm™
Expert formation et sensibilisation droits humains & conformité CSDDD.
Génère des programmes de formation personnalisés selon le profil et domaine.
"""

import sys
from datetime import datetime, timezone

TRAINING_MODULES = {
    "CSDDD_FUNDAMENTALS": {
        "title": "Fondamentaux CSDDD 2024",
        "duration_hours": 4,
        "level": "TOUS",
        "content": [
            "Histoire & genèse de la directive EU 2024/1760",
            "Champ d'application : entreprises concernées (>1000 sal., >450M€)",
            "Les 6 obligations CSDDD : Art.8 à Art.13",
            "Chaîne de valeur : amont, aval, relations d'affaires établies",
            "Mécanismes de sanction : amende jusqu'à 5% du CA mondial",
        ],
        "assessment": "QCM 20 questions — Seuil: 75%",
        "certification": "Certificat de formation CSDDD — Caelum Partners",
        "mandatory_for": ["Conseil d'administration", "Direction", "RSE", "Juridique", "Achats"],
    },
    "HUMAN_RIGHTS_DILIGENCE": {
        "title": "Diligence Raisonnable Droits Humains",
        "duration_hours": 8,
        "level": "INTERMÉDIAIRE",
        "content": [
            "UNGP 2011 — Les 31 Principes directeurs ONU",
            "Identifier et hiérarchiser les impacts négatifs",
            "Méthodes d'évaluation terrain : interviews, audits sociaux",
            "Indicateurs de performance droits humains (KPIs)",
            "Rapport & communication publique CSDDD Art.13",
        ],
        "assessment": "Étude de cas pratique — Analyse d'un fournisseur à risque",
        "certification": "Certification Expert Diligence RH — Caelum Partners",
        "mandatory_for": ["RSE", "Achats", "Audit", "Conformité"],
    },
    "SECTOR_RISK_AWARENESS": {
        "title": "Risques Sectoriels Droits Humains",
        "duration_hours": 3,
        "level": "OPÉRATIONNEL",
        "content": [
            "Cartographie des risques par secteur (extractif, textile, tech, finance)",
            "Signaux d'alerte terrain : indicateurs visibles",
            "Procédures de remontée d'information",
            "Mécanisme de réclamation interne — Comment ça marche ?",
            "Cas pratiques : travail forcé, enfants, discrimination",
        ],
        "assessment": "Quiz interactif + jeu de rôle",
        "certification": "Attestation Sensibilisation Secteur — Caelum Partners",
        "mandatory_for": ["Managers", "Responsables achats", "Chefs de projet"],
    },
    "DIGITAL_RIGHTS_MODULE": {
        "title": "Droits Numériques & IA — Risques Émergents",
        "duration_hours": 5,
        "level": "AVANCÉ",
        "content": [
            "AI Act 2024 — Systèmes à haut risque et obligations",
            "Deepfakes & droits à l'identité numérique",
            "Surveillance de masse et vie privée (RGPD + Charte EU)",
            "Responsabilité des plateformes (DSA 2022)",
            "Algorithmes et discrimination systémique",
        ],
        "assessment": "Analyse de cas réel + rapport écrit",
        "certification": "Expert Droits Numériques — Caelum Partners",
        "mandatory_for": ["IT", "Data", "Innovation", "Juridique"],
    },
    "STATELESSNESS_AWARENESS": {
        "title": "Apatridie & Droits Documentaires — Sensibilisation",
        "duration_hours": 2,
        "level": "SENSIBILISATION",
        "content": [
            "Comprendre l'apatridie : définition, causes, ampleur mondiale",
            "Impact sur l'accès aux droits : santé, éducation, travail",
            "Rôle des entreprises dans les chaînes incluant populations vulnérables",
            "Conventions internationales : Convention 1954 & 1961",
            "Bonnes pratiques : vérification fournisseurs à risque",
        ],
        "assessment": "Quiz 10 questions",
        "certification": "Attestation Apatridie — Caelum Partners",
        "mandatory_for": ["RH", "Achats", "Relations publiques"],
    },
}

AUDIENCE_PROFILES = {
    "BOARD": {
        "label": "Conseil d'administration",
        "priority_modules": ["CSDDD_FUNDAMENTALS"],
        "format": "Séminaire 1/2 journée présentiel",
        "frequency": "Annuel",
        "languages": ["FR", "EN", "NL"],
    },
    "RSE_COMPLIANCE": {
        "label": "Équipes RSE & Conformité",
        "priority_modules": ["CSDDD_FUNDAMENTALS", "HUMAN_RIGHTS_DILIGENCE"],
        "format": "Formation intensive 2 jours",
        "frequency": "Semestriel",
        "languages": ["FR", "EN"],
    },
    "OPERATIONS": {
        "label": "Équipes opérationnelles",
        "priority_modules": ["SECTOR_RISK_AWARENESS"],
        "format": "E-learning + atelier 1/2 journée",
        "frequency": "Annuel",
        "languages": ["FR", "NL", "DE"],
    },
    "TECH_IT": {
        "label": "Équipes IT & Data",
        "priority_modules": ["DIGITAL_RIGHTS_MODULE"],
        "format": "Workshop technique 1 journée",
        "frequency": "Annuel",
        "languages": ["FR", "EN"],
    },
}

PEDAGOGICAL_METHODS = {
    "CASE_STUDIES": "Études de cas réels CaelumSwarm™ (anonymisés)",
    "SIMULATIONS": "Simulation d'audit droits humains terrain",
    "ROLE_PLAY": "Jeux de rôle : entreprise vs. NGO vs. régulateur",
    "GAMIFICATION": "Quiz compétitifs + tableau de bord progression",
    "EXPERT_TALKS": "Conférenciers experts : juristes, terrain ONG",
    "ELEARNING": "Modules e-learning asynchrones avec évaluation",
}


def generate_training_plan(company_profile: dict, domain_risks: list) -> dict:
    """Génère un plan de formation personnalisé."""
    size = company_profile.get("size", "medium")
    sector = company_profile.get("sector", "general")
    csddd_scope = company_profile.get("employees", 0) >= 1000 and company_profile.get("revenue_M", 0) >= 450

    selected_modules = []
    if csddd_scope:
        selected_modules.append("CSDDD_FUNDAMENTALS")
        selected_modules.append("HUMAN_RIGHTS_DILIGENCE")

    selected_modules.append("SECTOR_RISK_AWARENESS")

    if any("digital" in d or "deepfake" in d or "ai" in d for d in domain_risks):
        selected_modules.append("DIGITAL_RIGHTS_MODULE")
    if any("stateless" in d or "document" in d for d in domain_risks):
        selected_modules.append("STATELESSNESS_AWARENESS")

    total_hours = sum(TRAINING_MODULES[m]["duration_hours"] for m in selected_modules if m in TRAINING_MODULES)

    plan_modules = []
    for month_idx, module_key in enumerate(selected_modules, 1):
        module = TRAINING_MODULES.get(module_key, {})
        plan_modules.append({
            "sequence": month_idx,
            "module_id": module_key,
            "title": module.get("title", module_key),
            "duration_hours": module.get("duration_hours", 0),
            "level": module.get("level", "TOUS"),
            "format": PEDAGOGICAL_METHODS.get("ELEARNING"),
            "target_audience": module.get("mandatory_for", []),
            "assessment": module.get("assessment", ""),
            "certification": module.get("certification", ""),
            "scheduled_month": f"M+{month_idx}",
        })

    return {
        "plan_id": f"TP-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Training & Awareness Agent v1.0",
        "company_profile": company_profile,
        "csddd_in_scope": csddd_scope,
        "domain_risks_covered": domain_risks,
        "training_plan": {
            "total_modules": len(plan_modules),
            "total_hours": total_hours,
            "rollout_months": len(plan_modules),
            "modules": plan_modules,
        },
        "kpis_to_track": {
            "completion_rate_target": "95%",
            "assessment_pass_rate_target": "80%",
            "awareness_survey_improvement": "+20 pts NPS",
            "incident_reduction_target": "-30% signalements non-conformes",
        },
        "budget_estimate": {
            "per_employee_EUR": 250 if csddd_scope else 150,
            "total_estimate_EUR": (company_profile.get("employees", 100)) * (250 if csddd_scope else 150),
            "roi_note": "Évite sanctions CSDDD jusqu'à 5% CA mondial + protection réputation",
        },
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — TRAINING & AWARENESS AGENT")
    print("  Expert Formation & Sensibilisation Droits Humains")
    print("=" * 70)

    company = {
        "name": "Caelum Partners SPRL",
        "sector": "legal-tech-compliance",
        "employees": 1500,
        "revenue_M": 600,
        "country": "Belgique",
        "operating_countries": ["BE", "FR", "DE", "NL", "LU"],
    }

    domain_risks = ["statelessness-document-rights", "deepfake-synthetic-media", "offshore-tax-haven"]

    plan = generate_training_plan(company, domain_risks)

    print(f"\n📚 PLAN DE FORMATION: {plan['plan_id']}")
    print(f"   Entreprise: {company['name']}")
    print(f"   CSDDD en scope: {'✅ OUI' if plan['csddd_in_scope'] else '❌ NON'}")
    print(f"   Total modules: {plan['training_plan']['total_modules']}")
    print(f"   Total heures: {plan['training_plan']['total_hours']}h")
    print(f"   Budget estimé: {plan['budget_estimate']['total_estimate_EUR']:,}€")

    print(f"\n📋 MODULES PLANIFIÉS:")
    for m in plan["training_plan"]["modules"]:
        print(f"\n   {m['sequence']}. [{m['scheduled_month']}] {m['title']}")
        print(f"      Durée: {m['duration_hours']}h | Niveau: {m['level']}")
        print(f"      Public cible: {', '.join(m['target_audience'][:3])}")
        print(f"      Évaluation: {m['assessment'][:60]}...")

    print(f"\n📊 KPIs CIBLES:")
    for kpi, target in plan["kpis_to_track"].items():
        print(f"   • {kpi.replace('_', ' ').title()}: {target}")

    print(f"\n💰 ROI: {plan['budget_estimate']['roi_note']}")
    print(f"\n✅ Training Agent — Plan de formation généré avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
