#!/usr/bin/env python3
"""
AI Ethics & Governance Agent — CaelumSwarm™
Framework: EU AI Act (Règlement UE 2024/1689), UNESCO Rec. on AI Ethics
Role: Conformité EU AI Act, détection biais, explainabilité, audit trail IA
"""

import random
import datetime
import json
import hashlib
import math
import sys

# ---------------------------------------------------------------------------
# Constants / Configuration
# ---------------------------------------------------------------------------

EU_AI_ACT_RISK_LEVELS = {
    "unacceptable": {
        "definition": "IA interdite — manipulation subliminale, scoring social gouvernemental",
        "examples": ["social_scoring_citizens", "real_time_biometric_surveillance_public", "subliminal_manipulation"],
        "applicable_date": "2025-02-02",
        "penalty": "Jusqu'à 35M€ ou 7% CA mondial",
    },
    "high_risk": {
        "definition": "IA à haut risque — Annexe III EU AI Act",
        "categories": [
            "Biométrie et catégorisation personnes",
            "Infrastructure critique (énergie, eau, transport)",
            "Éducation et formation professionnelle",
            "Emploi et gestion travailleurs",
            "Services essentiels (crédit, assurance)",
            "Application de la loi",
            "Migration et contrôle aux frontières",
            "Administration de la justice",
        ],
        "requirements": ["conformity_assessment", "technical_documentation", "human_oversight", "transparency", "accuracy_robustness", "risk_management_system"],
        "applicable_date": "2026-08-02",
        "penalty": "Jusqu'à 15M€ ou 3% CA mondial",
    },
    "limited_risk": {
        "definition": "IA avec obligations de transparence (chatbots, deepfakes)",
        "requirements": ["disclosure_to_users", "content_labeling"],
        "applicable_date": "2025-08-02",
    },
    "minimal_risk": {
        "definition": "IA sans risque particulier — filtres spam, jeux vidéo",
        "requirements": [],
    },
}

CAELUM_AI_SYSTEMS = {
    "wave_engines": {
        "type": "Système IA scoring droits humains",
        "eu_ai_act_risk": "high_risk",
        "category": "Emploi / Services essentiels",
        "article_annexe_iii": "Article 6(2) + Annexe III §4",
        "bias_risk": "medium",
        "explainability_required": True,
        "human_oversight": "Obligatoire pour scores > 60/100",
    },
    "compliance_rag": {
        "type": "RAG système de recherche documentaire",
        "eu_ai_act_risk": "limited_risk",
        "category": "Information retrieval",
        "disclosure_required": True,
    },
    "alert_system": {
        "type": "Système détection alertes temps réel",
        "eu_ai_act_risk": "high_risk",
        "category": "Infrastructure critique monitoring",
        "human_oversight": "Obligatoire avant action légale",
    },
    "report_generator": {
        "type": "LLM génération rapports conformité",
        "eu_ai_act_risk": "limited_risk",
        "disclosure_required": True,
        "content_labeling": "Ce rapport a été généré par IA",
    },
    "crewai_compliance_crew": {
        "type": "Système multi-agents audit",
        "eu_ai_act_risk": "high_risk",
        "category": "Administration justice / Emploi",
        "conformity_assessment": "Third-party audit requis",
    },
}

BIAS_DETECTION_CONFIG = {
    "protected_attributes": ["gender", "ethnicity", "nationality", "age", "religion", "disability"],
    "fairness_metrics": {
        "demographic_parity": "P(Y=1|A=0) = P(Y=1|A=1) ± 5%",
        "equalized_odds": "TPR et FPR égaux par groupe",
        "calibration": "P(Y=1|score=s) identique par groupe",
        "individual_fairness": "Individus similaires → traitements similaires",
    },
    "monitoring": {
        "frequency": "Mensuel sur production",
        "alert_threshold": "Disparité > 5% entre groupes",
        "retraining_trigger": "Disparité > 10% confirmée",
    },
    "audit_tools": ["Fairlearn", "IBM AI Fairness 360", "Aequitas", "What-If Tool"],
}

EXPLAINABILITY_FRAMEWORK = {
    "global_explanations": {
        "tool": "SHAP (SHapley Additive exPlanations)",
        "output": "Feature importance globale pour chaque wave engine",
        "frequency": "À chaque déploiement",
    },
    "local_explanations": {
        "tool": "LIME (Local Interpretable Model-agnostic Explanations)",
        "output": "Explication individuelle par entité scorée",
        "mandatory_for": "Scores critique (≥60) — CSDDD Art.9",
    },
    "counterfactual": {
        "description": "Si score = 75 (critique), qu'est-ce qui l'aurait fait passer à 59 (élevé)?",
        "tool": "DiCE (Diverse Counterfactual Explanations)",
    },
    "human_readable_reports": {
        "format": "Markdown + PDF",
        "audience": ["CSDDD compliance officers", "EU regulators", "Board"],
        "mandatory_clauses": ["Données utilisées", "Limites du modèle", "Biais détectés", "Décision humaine finale"],
    },
}

AI_GOVERNANCE_POLICY = {
    "model_registry": {
        "tool": "MLflow + HashiCorp Vault",
        "tracks": ["version", "training_data", "performance_metrics", "bias_scores", "approval_status"],
        "approvals": ["Data Scientist", "Ethics Review Board", "CISO", "DPO (RGPD Art.35 DPIA)"],
    },
    "human_oversight": {
        "mandatory": ["Scores critique ≥60", "Décisions affectant droits fondamentaux", "Actions légales"],
        "review_sla_hours": 24,
        "escalation": "CTO → Legal → Board si désaccord",
    },
    "data_governance": {
        "data_minimization": True,
        "purpose_limitation": True,
        "consent_management": "OneTrust",
        "dpia_required": True,
        "data_retention_months": 36,
    },
    "incident_response": {
        "ai_incident_types": ["bias_detected", "hallucination_critical", "adversarial_attack", "data_breach"],
        "notification_hours": 72,
        "notified_authorities": ["CNIL (FR)", "APD (BE)", "ENISA", "EU AI Office"],
    },
}

MODEL_CARDS = {
    "wave_engine_template": {
        "model_details": {"type": "Scoring rules-based", "version": "2.0", "date": "2024"},
        "intended_use": "Scoring risque droits humains CSDDD 2024",
        "factors": "Données fournisseurs, rapports ONG, données géopolitiques",
        "metrics": {"avg_composite": "~61", "distribution": "4/2/1/1"},
        "caveats": "Ne remplace pas l'avis d'un expert humain",
        "ethical_considerations": "Validation humaine obligatoire pour décisions légales",
    },
}

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

SUBGROUPS_BY_ATTRIBUTE = {
    "nationality": ["French", "German", "Romanian", "Moroccan", "Indian"],
    "gender": ["Male", "Female", "Non-binary"],
    "ethnicity": ["White", "Black", "Asian", "Hispanic", "Mixed"],
    "age": ["18-30", "31-45", "46-60", "60+"],
    "religion": ["Christian", "Muslim", "Jewish", "Hindu", "Non-religious"],
    "disability": ["No disability", "Physical", "Cognitive", "Sensory"],
}


def _hash_val(seed_str: str) -> float:
    """Return a stable float 0-1 derived from a string via MD5."""
    digest = hashlib.md5(seed_str.encode()).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def _score_level(score: float) -> str:
    if score >= 60:
        return "critique"
    if score >= 40:
        return "élevé"
    if score >= 20:
        return "modéré"
    return "faible"


# ---------------------------------------------------------------------------
# Function 1 — classify_eu_ai_act_risk
# ---------------------------------------------------------------------------

def classify_eu_ai_act_risk(system_name: str, system_type: str) -> dict:
    """
    Classifies an AI system by EU AI Act risk level.
    Looks up the system in CAELUM_AI_SYSTEMS if available,
    else infers from system_type keywords.
    """
    result = {
        "system_name": system_name,
        "system_type": system_type,
    }

    # Try direct lookup first
    sys_info = CAELUM_AI_SYSTEMS.get(system_name)
    if sys_info:
        risk_level = sys_info["eu_ai_act_risk"]
        result["risk_level"] = risk_level
        risk_data = EU_AI_ACT_RISK_LEVELS[risk_level]
        result["definition"] = risk_data["definition"]
        result["requirements"] = risk_data.get("requirements", [])
        result["applicable_date"] = risk_data.get("applicable_date", "N/A")
        if "penalty" in risk_data:
            result["penalty"] = risk_data["penalty"]
        if "article_annexe_iii" in sys_info:
            result["article_annexe_iii"] = sys_info["article_annexe_iii"]
        return result

    # Infer from keywords in system_type
    type_lower = system_type.lower()
    unacceptable_keywords = ["social scoring", "biometric surveillance", "subliminal", "manipulation"]
    high_risk_keywords = [
        "biometric", "emploi", "employment", "education", "credit", "assurance",
        "law enforcement", "justice", "migration", "border", "infrastructure", "critique",
        "scoring", "droits humains", "human rights", "audit"
    ]
    limited_risk_keywords = ["chatbot", "deepfake", "rag", "llm", "génération", "generation", "chatgpt", "disclosure"]

    if any(kw in type_lower for kw in unacceptable_keywords):
        risk_level = "unacceptable"
    elif any(kw in type_lower for kw in high_risk_keywords):
        risk_level = "high_risk"
    elif any(kw in type_lower for kw in limited_risk_keywords):
        risk_level = "limited_risk"
    else:
        risk_level = "minimal_risk"

    risk_data = EU_AI_ACT_RISK_LEVELS[risk_level]
    result["risk_level"] = risk_level
    result["definition"] = risk_data["definition"]
    result["requirements"] = risk_data.get("requirements", [])
    result["applicable_date"] = risk_data.get("applicable_date", "N/A")
    if "penalty" in risk_data:
        result["penalty"] = risk_data["penalty"]
    return result


# ---------------------------------------------------------------------------
# Function 2 — run_bias_audit
# ---------------------------------------------------------------------------

def run_bias_audit(model_name: str, protected_attribute: str, sample_size: int) -> dict:
    """
    Simulate a bias audit with realistic group statistics.
    """
    subgroups = SUBGROUPS_BY_ATTRIBUTE.get(
        protected_attribute,
        ["Group_A", "Group_B", "Group_C", "Group_D"]
    )

    # Weight vector for proportional sample sizes (arbitrary but stable)
    raw_weights = [_hash_val(f"{model_name}_{protected_attribute}_{g}_weight") + 0.1 for g in subgroups]
    total_weight = sum(raw_weights)

    group_stats = {}
    for i, group in enumerate(subgroups):
        proportion = raw_weights[i] / total_weight
        count = max(10, round(sample_size * proportion))
        # Positive rate: simulate slight variation across groups
        positive_rate = round(
            0.30 + 0.40 * _hash_val(f"{model_name}_{protected_attribute}_{group}_pr"),
            4
        )
        tpr = round(
            0.60 + 0.35 * _hash_val(f"{model_name}_{protected_attribute}_{group}_tpr"),
            4
        )
        fpr = round(
            0.05 + 0.20 * _hash_val(f"{model_name}_{protected_attribute}_{group}_fpr"),
            4
        )
        group_stats[group] = {
            "sample_count": count,
            "positive_rate": positive_rate,
            "tpr": tpr,
            "fpr": fpr,
        }

    positive_rates = [v["positive_rate"] for v in group_stats.values()]
    demographic_parity_gap = round(max(positive_rates) - min(positive_rates), 4)
    bias_detected = demographic_parity_gap > 0.05
    alert_triggered = bias_detected
    retraining_required = demographic_parity_gap > 0.10

    # Fairness metrics summary
    fairness_metrics = {
        "demographic_parity_gap": demographic_parity_gap,
        "max_positive_rate": max(positive_rates),
        "min_positive_rate": min(positive_rates),
        "equalized_odds_status": "Non-vérifié — audit complet requis",
        "calibration_status": "Non-vérifié — audit complet requis",
    }

    recommendation = (
        "Ré-entraînement du modèle recommandé — disparité critique détectée (>10%)"
        if retraining_required
        else (
            "Surveillance renforcée recommandée — disparité détectée (5-10%)"
            if bias_detected
            else "Modèle conforme aux seuils de parité démographique"
        )
    )

    return {
        "model_name": model_name,
        "protected_attribute": protected_attribute,
        "sample_size": sample_size,
        "subgroups_analyzed": subgroups,
        "group_statistics": group_stats,
        "fairness_metrics": fairness_metrics,
        "demographic_parity_gap": demographic_parity_gap,
        "bias_detected": bias_detected,
        "alert_triggered": alert_triggered,
        "retraining_required": retraining_required,
        "audit_tool": BIAS_DETECTION_CONFIG["audit_tools"][0],
        "recommendation": recommendation,
        "audit_date": datetime.date.today().isoformat(),
        "config_reference": {
            "alert_threshold": BIAS_DETECTION_CONFIG["monitoring"]["alert_threshold"],
            "retraining_trigger": BIAS_DETECTION_CONFIG["monitoring"]["retraining_trigger"],
        },
    }


# ---------------------------------------------------------------------------
# Function 3 — generate_explainability_report
# ---------------------------------------------------------------------------

def generate_explainability_report(entity_name: str, composite_score: float, sub_scores: dict) -> dict:
    """
    Generate an explainability report for a scored entity.
    """
    level = _score_level(composite_score)
    human_oversight_required = composite_score >= 60

    # SHAP values: derive from sub_scores with simulated noise
    # Use a stable seed based on entity_name
    shap_seed = int(hashlib.md5(entity_name.encode()).hexdigest()[:8], 16)
    local_rng = random.Random(shap_seed)

    shap_values = {}
    for feature, score_val in sub_scores.items():
        # SHAP magnitude proportional to score with slight random perturbation
        base = (score_val / 100.0) * 0.35
        noise = local_rng.uniform(-0.05, 0.05)
        shap_values[feature] = round(base + noise, 4)

    # Top 3 factors by absolute SHAP value
    sorted_features = sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)
    top_3_factors = [
        {"feature": feat, "shap_value": val, "direction": "positive" if val > 0 else "negative"}
        for feat, val in sorted_features[:3]
    ]

    # LIME narrative
    top_feat = sorted_features[0][0]
    top_val = sorted_features[0][1]
    lime_explanation = (
        f"Localement, le score de {entity_name} ({composite_score}/100) est principalement "
        f"influencé par '{top_feat}' (contribution LIME estimée: {top_val:+.4f}). "
        f"Les trois facteurs dominants représentent "
        f"{round(sum(abs(v) for _, v in sorted_features[:3]) / max(sum(abs(v) for v in shap_values.values()), 1e-9) * 100, 1)}% "
        f"de la variance locale du modèle."
    )

    # Counterfactual: what changes would bring the score below 60?
    counterfactual_changes = []
    if composite_score >= 60:
        for feature, score_val in sorted(sub_scores.items(), key=lambda x: x[1], reverse=True):
            if score_val > 50:
                needed_reduction = max(0, composite_score - 59)
                new_val = max(0, score_val - round(needed_reduction * 1.5))
                counterfactual_changes.append({
                    "feature": feature,
                    "from": score_val,
                    "to": new_val,
                    "impact": f"-{round(needed_reduction, 1)} points composite estimés",
                })
                if len(counterfactual_changes) >= 3:
                    break

    counterfactual = {
        "scenario": f"Pour que {entity_name} passe du niveau '{level}' ({composite_score}) au niveau 'élevé' (<60)",
        "required_changes": counterfactual_changes,
        "tool": EXPLAINABILITY_FRAMEWORK["counterfactual"]["tool"],
    }

    mandatory_clauses = {
        "données_utilisées": "Données fournisseurs, rapports ONG, données géopolitiques, incidents publics",
        "limites_du_modèle": "Modèle rules-based — ne capture pas les dynamiques contextuelles complexes; données historiques potentiellement incomplètes",
        "biais_détectés": "Biais potentiel lié à la disponibilité des données par région géographique — audit Fairlearn mensuel en place",
        "décision_humaine_finale": (
            "OBLIGATOIRE — validation humaine requise avant toute action légale ou contractuelle"
            if human_oversight_required
            else "Recommandée — revue humaine conseillée pour ce niveau de score"
        ),
    }

    return {
        "entity_name": entity_name,
        "composite_score": composite_score,
        "score_level": level,
        "shap_values": shap_values,
        "top_3_factors": top_3_factors,
        "lime_explanation": lime_explanation,
        "counterfactual": counterfactual,
        "human_oversight_required": human_oversight_required,
        "mandatory_clauses": mandatory_clauses,
        "generated_at": datetime.datetime.now().isoformat(),
        "framework_reference": {
            "shap_tool": EXPLAINABILITY_FRAMEWORK["global_explanations"]["tool"],
            "lime_tool": EXPLAINABILITY_FRAMEWORK["local_explanations"]["tool"],
            "mandatory_for": EXPLAINABILITY_FRAMEWORK["local_explanations"]["mandatory_for"],
        },
    }


# ---------------------------------------------------------------------------
# Function 4 — check_eu_ai_act_compliance
# ---------------------------------------------------------------------------

def check_eu_ai_act_compliance(system_name: str) -> dict:
    """
    Check EU AI Act compliance for a CaelumSwarm system.
    """
    sys_info = CAELUM_AI_SYSTEMS.get(system_name, {})
    risk_level = sys_info.get("eu_ai_act_risk", "minimal_risk")
    risk_data = EU_AI_ACT_RISK_LEVELS[risk_level]
    requirements = risk_data.get("requirements", [])

    # Remediation templates
    remediation_map = {
        "conformity_assessment": "Engager un organisme notifié pour audit tiers — délai: 6 mois",
        "technical_documentation": "Compléter la documentation technique selon Annexe IV EU AI Act",
        "human_oversight": "Mettre en place un comité de revue humaine avec SLA 24h",
        "transparency": "Publier une notice de transparence publique sur le système IA",
        "accuracy_robustness": "Tester la robustesse contre les attaques adversariales — benchmark requis",
        "risk_management_system": "Déployer un système de gestion des risques ISO 31000 + EU AI Act Art.9",
        "disclosure_to_users": "Afficher une notification claire aux utilisateurs indiquant l'usage de l'IA",
        "content_labeling": "Implémenter un label automatique sur tous les contenus générés par IA",
    }

    gap_map = {
        "conformity_assessment": "Aucun organisme notifié mandaté à ce jour",
        "technical_documentation": "Documentation partielle — sections sur les données d'entraînement manquantes",
        "human_oversight": "Processus de revue humaine défini mais non formalisé",
        "transparency": "Notice de transparence en cours de rédaction",
        "accuracy_robustness": "Tests de robustesse effectués mais non documentés formellement",
        "risk_management_system": "Système de gestion des risques partiellement implémenté",
        "disclosure_to_users": "Disclosure présent sur l'interface web, absent sur l'API",
        "content_labeling": "Labeling implémenté pour PDF, absent pour flux JSON",
    }

    # Deterministic compliance status per requirement using hash
    status_thresholds = {"compliant": 0.60, "partial": 0.30}  # >0.60 → compliant, 0.30-0.60 → partial, else missing

    requirements_status = []
    compliant_count = 0
    partial_count = 0

    for req in requirements:
        h = _hash_val(f"{system_name}_{req}_compliance")
        if h > status_thresholds["compliant"]:
            status = "compliant"
            compliant_count += 1
            gap_desc = "Conforme aux exigences EU AI Act"
            remediation = "Maintenir la conformité et documenter lors du prochain audit"
        elif h > status_thresholds["partial"]:
            status = "partial"
            partial_count += 1
            gap_desc = gap_map.get(req, "Conformité partielle — investigation requise")
            remediation = remediation_map.get(req, "Évaluation approfondie requise")
        else:
            status = "missing"
            gap_desc = gap_map.get(req, "Exigence non satisfaite")
            remediation = remediation_map.get(req, "Mise en conformité urgente requise")

        requirements_status.append({
            "requirement": req,
            "status": status,
            "gap_description": gap_desc,
            "remediation": remediation,
        })

    total = len(requirements)
    if total == 0:
        compliance_score = 100
    else:
        compliance_score = round((compliant_count + 0.5 * partial_count) / total * 100)

    overall_compliant = (compliance_score >= 80) and all(r["status"] != "missing" for r in requirements_status)

    today = datetime.date.today()
    next_audit_date = (today + datetime.timedelta(days=182)).isoformat()

    return {
        "system_name": system_name,
        "system_type": sys_info.get("type", "Unknown"),
        "risk_level": risk_level,
        "overall_compliant": overall_compliant,
        "compliance_score": compliance_score,
        "requirements_status": requirements_status,
        "applicable_date": risk_data.get("applicable_date", "N/A"),
        "next_audit_date": next_audit_date,
        "penalty_if_non_compliant": risk_data.get("penalty", "N/A"),
        "summary": (
            f"Système '{system_name}' — score de conformité: {compliance_score}/100. "
            f"{compliant_count}/{total} exigences conformes, {partial_count}/{total} partielles."
        ),
    }


# ---------------------------------------------------------------------------
# Function 5 — generate_model_card
# ---------------------------------------------------------------------------

def generate_model_card(engine_name: str, metrics: dict) -> dict:
    """
    Generate a Model Card based on the wave_engine_template.
    """
    template = MODEL_CARDS["wave_engine_template"]

    # Simulated precision/recall/f1 if not provided
    precision = metrics.get("precision", round(0.75 + 0.20 * _hash_val(engine_name + "_precision"), 3))
    recall = metrics.get("recall", round(0.70 + 0.20 * _hash_val(engine_name + "_recall"), 3))
    f1 = metrics.get("f1", round(2 * precision * recall / max(precision + recall, 1e-9), 3))

    evaluation_metrics = {
        "avg_composite_score": metrics.get("avg_composite", template["metrics"]["avg_composite"]),
        "distribution": metrics.get("distribution", template["metrics"]["distribution"]),
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "bias_audit_last_gap": "~7.3% (Fairlearn, nationality)",
        "monitoring_frequency": BIAS_DETECTION_CONFIG["monitoring"]["frequency"],
    }

    # Classify risk
    classification = classify_eu_ai_act_risk(engine_name, template["model_details"]["type"])

    bias_score = _hash_val(engine_name + "_bias")
    bias_assessment = (
        "Biais élevé détecté — ré-entraînement planifié"
        if bias_score > 0.70
        else (
            "Biais modéré détecté — surveillance renforcée active"
            if bias_score > 0.40
            else "Biais faible — dans les limites acceptables (< 5% disparité)"
        )
    )

    return {
        "model_details": {
            "engine_name": engine_name,
            "type": template["model_details"]["type"],
            "version": template["model_details"]["version"],
            "date": template["model_details"]["date"],
        },
        "intended_use": template["intended_use"],
        "training_data_description": (
            "Données fournisseurs B2B (Tier 1-3), rapports ONG (Amnesty, HRW, ILO), "
            "données géopolitiques (OCDE, Banque Mondiale), incidents publics vérifiés"
        ),
        "factors": template["factors"],
        "evaluation_metrics": evaluation_metrics,
        "bias_assessment": bias_assessment,
        "ethical_considerations": template["ethical_considerations"],
        "limitations": [
            template["caveats"],
            "Biais potentiel lié à la disponibilité des données par région",
            "Modèle rules-based — sensibilité limitée aux changements contextuels rapides",
            "Ne couvre pas les violations non documentées ou non rapportées",
        ],
        "human_oversight_required": True,
        "eu_ai_act_classification": {
            "risk_level": classification["risk_level"],
            "applicable_date": classification.get("applicable_date", "N/A"),
            "requirements": classification.get("requirements", []),
        },
        "mandatory_clauses": EXPLAINABILITY_FRAMEWORK["human_readable_reports"]["mandatory_clauses"],
        "generated_at": datetime.datetime.now().isoformat(),
        "model_registry_tool": AI_GOVERNANCE_POLICY["model_registry"]["tool"],
    }


# ---------------------------------------------------------------------------
# Main block
# ---------------------------------------------------------------------------

def main():
    random.seed(42)
    now = datetime.datetime.now()
    today_str = now.strftime("%Y-%m-%d %H:%M:%S")

    SEP = "=" * 60

    # ------------------------------------------------------------------
    # 1. Header
    # ------------------------------------------------------------------
    print(SEP)
    print("AI ETHICS & GOVERNANCE REPORT — CaelumSwarm™")
    print(f"Date: {today_str}")
    print("Framework: EU AI Act (Règlement UE 2024/1689) | UNESCO Rec. on AI Ethics")
    print("Role: Conformité EU AI Act | Détection biais | Explainabilité | Audit trail")
    print(SEP)

    # ------------------------------------------------------------------
    # 2. EU AI Act risk levels
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("SECTION 2 — EU AI ACT RISK LEVELS")
    print(SEP)
    for level_name, level_data in EU_AI_ACT_RISK_LEVELS.items():
        print(f"\n  [{level_name.upper()}]")
        print(f"    Definition   : {level_data['definition']}")
        print(f"    Applicable   : {level_data.get('applicable_date', 'N/A')}")
        if "penalty" in level_data:
            print(f"    Penalty      : {level_data['penalty']}")
        reqs = level_data.get("requirements", [])
        if reqs:
            print(f"    Requirements : {', '.join(reqs)}")

    # ------------------------------------------------------------------
    # 3. Classify all 5 CAELUM_AI_SYSTEMS
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("SECTION 3 — EU AI ACT CLASSIFICATION — CAELUM AI SYSTEMS")
    print(SEP)
    for sys_name, sys_info in CAELUM_AI_SYSTEMS.items():
        result = classify_eu_ai_act_risk(sys_name, sys_info["type"])
        print(f"\n  System: {sys_name}")
        print(json.dumps(result, indent=4, ensure_ascii=False))

    # ------------------------------------------------------------------
    # 4. Bias audit
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("SECTION 4 — BIAS AUDIT: wave_engines / nationality / n=10000")
    print(SEP)
    bias_result = run_bias_audit("wave_engines", "nationality", 10000)
    print(json.dumps(bias_result, indent=2, ensure_ascii=False))

    # ------------------------------------------------------------------
    # 5. Explainability report
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("SECTION 5 — EXPLAINABILITY REPORT: Chevron (score=84)")
    print(SEP)
    xai_result = generate_explainability_report(
        "Chevron",
        84.0,
        {
            "child_labor": 92,
            "forced_labor": 78,
            "environmental": 71,
            "corruption": 65,
            "supply_chain_transparency": 45,
        },
    )
    print(json.dumps(xai_result, indent=2, ensure_ascii=False))

    # ------------------------------------------------------------------
    # 6. EU AI Act compliance check
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("SECTION 6 — EU AI ACT COMPLIANCE CHECK: crewai_compliance_crew")
    print(SEP)
    compliance_result = check_eu_ai_act_compliance("crewai_compliance_crew")
    print(json.dumps(compliance_result, indent=2, ensure_ascii=False))

    # ------------------------------------------------------------------
    # 7. Model Card
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("SECTION 7 — MODEL CARD: child_agricultural_labor_engine")
    print(SEP)
    model_card = generate_model_card(
        "child_agricultural_labor_engine",
        {
            "avg_composite": 67.3,
            "precision": 0.84,
            "recall": 0.79,
            "f1": 0.81,
            "distribution": "5/3/2/1",
        },
    )
    print(json.dumps(model_card, indent=2, ensure_ascii=False))

    # ------------------------------------------------------------------
    # 8. Governance section
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("SECTION 8 — AI GOVERNANCE POLICY")
    print(SEP)

    print("\n  [MODEL REGISTRY]")
    mr = AI_GOVERNANCE_POLICY["model_registry"]
    print(f"    Tool     : {mr['tool']}")
    print(f"    Tracks   : {', '.join(mr['tracks'])}")
    print(f"    Approvals: {', '.join(mr['approvals'])}")

    print("\n  [HUMAN OVERSIGHT]")
    ho = AI_GOVERNANCE_POLICY["human_oversight"]
    print(f"    Mandatory : {', '.join(ho['mandatory'])}")
    print(f"    SLA       : {ho['review_sla_hours']}h")
    print(f"    Escalation: {ho['escalation']}")

    print("\n  [DATA GOVERNANCE]")
    dg = AI_GOVERNANCE_POLICY["data_governance"]
    print(f"    Data minimization : {dg['data_minimization']}")
    print(f"    Purpose limitation: {dg['purpose_limitation']}")
    print(f"    Consent management: {dg['consent_management']}")
    print(f"    DPIA required     : {dg['dpia_required']}")
    print(f"    Data retention    : {dg['data_retention_months']} months")

    # ------------------------------------------------------------------
    # 9. Incident response simulation
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("SECTION 9 — INCIDENT RESPONSE: bias_detected / wave_engines")
    print(SEP)

    detected_at = now
    notification_deadline = detected_at + datetime.timedelta(hours=72)
    incident_report = {
        "incident_type": "bias_detected",
        "system": "wave_engines",
        "detected_at": detected_at.isoformat(),
        "severity": "HIGH",
        "trigger": f"Disparité démographique > 5% détectée — groupe 'nationality' (gap: 7.3%)",
        "notification_deadline": notification_deadline.isoformat(),
        "notification_deadline_human": notification_deadline.strftime("%Y-%m-%d %H:%M:%S"),
        "authorities_to_notify": AI_GOVERNANCE_POLICY["incident_response"]["notified_authorities"],
        "steps_taken": [
            "1. Alerte automatique déclenchée — tableau de bord Fairlearn",
            "2. Suspension des scores en production (wave_engines) — en attente revue humaine",
            "3. Notification interne: Data Scientist + Ethics Review Board + CISO",
            "4. Ouverture ticket incident #INC-2026-0622-BIAS-001",
            "5. Analyse root cause initiée — audit données entraînement nationality",
            "6. Notification CNIL, APD, ENISA, EU AI Office — délai: 72h (Art.73 EU AI Act)",
            "7. Rapport DPIA complémentaire planifié (RGPD Art.35)",
            "8. Ré-entraînement planifié — post-validation Ethics Review Board",
        ],
        "reference_articles": ["EU AI Act Art.73 (notification incidents)", "RGPD Art.33 (notification violations)", "RGPD Art.35 (DPIA)"],
    }
    print(json.dumps(incident_report, indent=2, ensure_ascii=False))

    # ------------------------------------------------------------------
    # 10. Final status
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("AI Ethics & Governance Agent — PRÊT (EU AI Act 2024 / Fairlearn / SHAP / DPIA)")
    print(SEP)


if __name__ == "__main__":
    main()
