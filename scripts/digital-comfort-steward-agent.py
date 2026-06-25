"""
Agent Intendant de Confort Digital — optimise l'expérience utilisateur digitale de
CaelumSwarm™ : UX/UI, accessibilité, performance perçue, onboarding, satisfaction
client et bien-être numérique des équipes conformité.

Caelum Partners — CaelumSwarm™
"""

from __future__ import annotations

import math
from typing import Any

# ---------------------------------------------------------------------------
# DATA CONSTANTS
# ---------------------------------------------------------------------------

UX_METRICS: dict[str, dict[str, Any]] = {
    "time_to_first_value_minutes": {
        "current": 18.5,
        "target": 8.0,
        "industry_benchmark": 12.0,
        "priority": "CRITICAL",
    },
    "task_completion_rate_pct": {
        "current": 71.2,
        "target": 90.0,
        "industry_benchmark": 82.0,
        "priority": "CRITICAL",
    },
    "error_rate_pct": {
        "current": 8.4,
        "target": 2.0,
        "industry_benchmark": 4.5,
        "priority": "CRITICAL",
    },
    "support_ticket_rate_per_user": {
        "current": 2.3,
        "target": 0.5,
        "industry_benchmark": 1.1,
        "priority": "HIGH",
    },
    "nps_score": {
        "current": 28,
        "target": 55,
        "industry_benchmark": 42,
        "priority": "HIGH",
    },
    "feature_adoption_rate_pct": {
        "current": 44.6,
        "target": 75.0,
        "industry_benchmark": 60.0,
        "priority": "HIGH",
    },
    "session_duration_avg_minutes": {
        "current": 22.1,
        "target": 35.0,
        "industry_benchmark": 28.0,
        "priority": "MEDIUM",
    },
    "return_rate_7d_pct": {
        "current": 58.3,
        "target": 85.0,
        "industry_benchmark": 70.0,
        "priority": "MEDIUM",
    },
}

ACCESSIBILITY_STANDARDS: dict[str, dict[str, Any]] = {
    "WCAG_2_1_AA": {
        "label": "Directives pour l'accessibilité du contenu Web 2.1 niveau AA",
        "eu_mandatory": True,
        "compliance_level": "PARTIAL",
        "remediation_effort_days": 14,
    },
    "EN_301_549": {
        "label": "Norme européenne d'accessibilité numérique (obligatoire secteur public EU)",
        "eu_mandatory": True,
        "compliance_level": "PARTIAL",
        "remediation_effort_days": 21,
    },
    "ARIA_ATTRIBUTES": {
        "label": "Attributs ARIA pour technologies d'assistance",
        "eu_mandatory": False,
        "compliance_level": "PASS",
        "remediation_effort_days": 0,
    },
    "KEYBOARD_NAVIGATION": {
        "label": "Navigation complète au clavier (sans souris)",
        "eu_mandatory": True,
        "compliance_level": "PARTIAL",
        "remediation_effort_days": 7,
    },
    "COLOR_CONTRAST": {
        "label": "Contraste couleur minimum 4.5:1 (texte normal) / 3:1 (texte large)",
        "eu_mandatory": True,
        "compliance_level": "FAIL",
        "remediation_effort_days": 5,
    },
    "SCREEN_READER_COMPAT": {
        "label": "Compatibilité lecteurs d'écran (NVDA, JAWS, VoiceOver)",
        "eu_mandatory": False,
        "compliance_level": "PARTIAL",
        "remediation_effort_days": 10,
    },
}

ONBOARDING_FLOWS: dict[str, dict[str, Any]] = {
    "RSE_DIRECTOR_ONBOARDING": {
        "steps": [
            {
                "step_name": "Création du compte & SSO",
                "duration_minutes": 5,
                "completion_rate_pct": 94.0,
                "drop_off_points": ["Configuration MFA complexe", "Délai email de vérification"],
            },
            {
                "step_name": "Paramétrage profil RSE",
                "duration_minutes": 12,
                "completion_rate_pct": 78.5,
                "drop_off_points": ["Trop de champs obligatoires", "Taxonomie sectorielle peu claire"],
            },
            {
                "step_name": "Import données ESG existantes",
                "duration_minutes": 25,
                "completion_rate_pct": 52.3,
                "drop_off_points": ["Format fichier non documenté", "Validation erreurs cryptiques", "Timeout sur gros fichiers"],
            },
            {
                "step_name": "Configuration tableaux de bord",
                "duration_minutes": 18,
                "completion_rate_pct": 61.0,
                "drop_off_points": ["Interface de personnalisation peu intuitive", "Vocabulaire technique ESG non expliqué"],
            },
            {
                "step_name": "Première analyse swarm",
                "duration_minutes": 10,
                "completion_rate_pct": 73.2,
                "drop_off_points": ["Résultats sans contexte interprétatif", "Actions recommandées peu claires"],
            },
            {
                "step_name": "Partage rapport équipe",
                "duration_minutes": 8,
                "completion_rate_pct": 80.0,
                "drop_off_points": ["Gestion des permissions complexe"],
            },
        ],
        "total_duration_minutes": 78,
        "success_metric": "Première analyse ESG complète partagée avec l'équipe",
    },
    "LEGAL_COUNSEL_ONBOARDING": {
        "steps": [
            {
                "step_name": "Création compte & vérification juridique",
                "duration_minutes": 6,
                "completion_rate_pct": 91.0,
                "drop_off_points": ["Conditions d'utilisation longues", "Processus KYC"],
            },
            {
                "step_name": "Paramétrage périmètre réglementaire",
                "duration_minutes": 15,
                "completion_rate_pct": 69.0,
                "drop_off_points": ["Sélection juridictions trop granulaire", "Manque de guidance par secteur"],
            },
            {
                "step_name": "Configuration alertes réglementaires",
                "duration_minutes": 20,
                "completion_rate_pct": 55.0,
                "drop_off_points": ["Volume d'alertes par défaut trop élevé", "Catégorisation peu adaptée au droit"],
            },
            {
                "step_name": "Intégration base documentaire",
                "duration_minutes": 30,
                "completion_rate_pct": 48.0,
                "drop_off_points": ["Format DMS non supporté", "Absence de connecteur SharePoint natif"],
            },
            {
                "step_name": "Premier audit conformité",
                "duration_minutes": 22,
                "completion_rate_pct": 66.5,
                "drop_off_points": ["Terminologie juridique non standardisée", "Manque de références réglementaires cliquables"],
            },
        ],
        "total_duration_minutes": 93,
        "success_metric": "Premier rapport d'audit conformité généré et validé",
    },
    "ESG_ANALYST_ONBOARDING": {
        "steps": [
            {
                "step_name": "Création compte & intégration équipe",
                "duration_minutes": 4,
                "completion_rate_pct": 96.0,
                "drop_off_points": ["Invitation email dans spams"],
            },
            {
                "step_name": "Configuration périmètre d'analyse",
                "duration_minutes": 10,
                "completion_rate_pct": 83.0,
                "drop_off_points": ["Mapping indicateurs GRI/SASB peu clair"],
            },
            {
                "step_name": "Exploration modules swarm",
                "duration_minutes": 15,
                "completion_rate_pct": 75.0,
                "drop_off_points": ["Navigation entre modules non linéaire", "Documentation technique insuffisante"],
            },
            {
                "step_name": "Première collecte de données terrain",
                "duration_minutes": 20,
                "completion_rate_pct": 68.0,
                "drop_off_points": ["Formulaires mobiles non optimisés", "Absence de mode hors-ligne"],
            },
            {
                "step_name": "Analyse et visualisation résultats",
                "duration_minutes": 12,
                "completion_rate_pct": 79.0,
                "drop_off_points": ["Options export limitées"],
            },
        ],
        "total_duration_minutes": 61,
        "success_metric": "Premier jeu de données ESG collecté, analysé et exporté",
    },
    "ADMIN_SETUP": {
        "steps": [
            {
                "step_name": "Configuration organisation",
                "duration_minutes": 8,
                "completion_rate_pct": 88.0,
                "drop_off_points": ["Hiérarchie entités complexe", "Manque de template sectoriel"],
            },
            {
                "step_name": "Gestion utilisateurs & rôles",
                "duration_minutes": 14,
                "completion_rate_pct": 72.0,
                "drop_off_points": ["Matrice de droits peu lisible", "Absence d'import CSV utilisateurs"],
            },
            {
                "step_name": "Intégrations SI existant",
                "duration_minutes": 45,
                "completion_rate_pct": 41.0,
                "drop_off_points": ["Documentation API insuffisante", "Environnement sandbox absent", "Support technique lent"],
            },
            {
                "step_name": "Configuration sécurité & conformité data",
                "duration_minutes": 20,
                "completion_rate_pct": 63.0,
                "drop_off_points": ["Paramètres RGPD peu guidés", "Politique rétention données complexe"],
            },
            {
                "step_name": "Formation équipe & déploiement",
                "duration_minutes": 30,
                "completion_rate_pct": 57.0,
                "drop_off_points": ["Matériel de formation insuffisant", "Pas de plan de déploiement suggéré"],
            },
        ],
        "total_duration_minutes": 117,
        "success_metric": "Organisation opérationnelle avec toutes les intégrations actives",
    },
}

DIGITAL_WELLBEING_FACTORS: dict[str, dict[str, Any]] = {
    "information_overload_score": {
        "current_state": 7.8,  # sur 10, 10 = surcharge maximale
        "target_state": 3.5,
        "improvement_action": (
            "Implémenter un système de prioritisation intelligente basé sur le rôle "
            "et le contexte réglementaire ; regrouper les informations par thématique "
            "avec des résumés exécutifs automatiques"
        ),
    },
    "alert_fatigue_level": {
        "current_state": "CRITIQUE",  # FAIBLE / MODÉRÉ / ÉLEVÉ / CRITIQUE
        "target_state": "FAIBLE",
        "improvement_action": (
            "Réduire les alertes de 40+ à 8-12 par jour via agrégation intelligente ; "
            "introduire un score de criticité réglementaire pour trier ; "
            "proposer un mode digest quotidien personnalisé"
        ),
    },
    "cognitive_load_assessment": {
        "current_state": "ÉLEVÉ",  # FAIBLE / MODÉRÉ / ÉLEVÉ
        "target_state": "MODÉRÉ",
        "improvement_action": (
            "Simplifier les interfaces en réduisant le nombre d'options visibles ; "
            "utiliser la divulgation progressive ; ajouter des wizards contextuels "
            "pour les tâches réglementaires complexes"
        ),
    },
    "notification_frequency_optimal": {
        "current_state": False,
        "target_state": True,
        "improvement_action": (
            "Déployer un moteur de timing des notifications basé sur les patterns "
            "d'activité individuels ; respecter les heures de focus et les réunions "
            "détectées via intégration calendrier"
        ),
    },
    "dark_mode_available": {
        "current_state": False,
        "target_state": True,
        "improvement_action": (
            "Implémenter le mode sombre avec détection automatique des préférences "
            "système ; réduire la fatigue oculaire pour les professionnels en "
            "sessions longues de révision documentaire"
        ),
    },
    "focus_mode_available": {
        "current_state": False,
        "target_state": True,
        "improvement_action": (
            "Créer un mode concentration masquant les éléments non essentiels ; "
            "bloquer les notifications non critiques pendant les plages de travail "
            "intense ; intégrer un minuteur Pomodoro adapté aux cycles réglementaires"
        ),
    },
}

# ---------------------------------------------------------------------------
# HELPER UTILITIES
# ---------------------------------------------------------------------------

_COMPLIANCE_FRICTION_MAP: dict[str, list[str]] = {
    "RSE_DIRECTOR": [
        "Tableaux de bord surchargés de KPI sans hiérarchisation",
        "Absence de vue synthétique 'état de la conformité RSE'",
        "Navigation entre modules sans fil d'Ariane clair",
        "Données brutes sans interprétation contextuelle",
        "Exports non conformes aux formats de reporting CSRD",
    ],
    "LEGAL_COUNSEL": [
        "Terminologie réglementaire non standardisée selon les juridictions",
        "Absence de liens vers les textes officiels (EUR-Lex, Légifrance)",
        "Alertes sans classement par niveau de risque juridique",
        "Workflow de validation sans traçabilité d'audit",
        "Interface non adaptée à la lecture longue de documents",
    ],
    "ESG_ANALYST": [
        "Formulaires de collecte non optimisés pour usage terrain/mobile",
        "Manque de mode hors-ligne pour les visites de sites",
        "Absence de templates de collecte par secteur d'activité",
        "Visualisations non exportables en formats BI standards",
        "Mapping indicateurs GRI/SASB/SFDR peu intuitif",
    ],
    "ADMIN": [
        "Matrice de droits trop complexe sans vue simplifiée",
        "Absence de tableau de bord d'adoption par utilisateur",
        "Logs d'audit difficiles à filtrer et exporter",
        "Configuration RGPD sans assistant pas-à-pas",
    ],
    "DEFAULT": [
        "Temps de chargement trop longs sur les rapports volumineux",
        "Messages d'erreur peu explicites",
        "Absence de raccourcis clavier pour les actions fréquentes",
    ],
}

_COGNITIVE_LOAD_WEIGHTS: dict[str, float] = {
    "error_rate_pct": 0.30,
    "task_completion_rate_pct": 0.25,
    "time_to_first_value_minutes": 0.20,
    "support_ticket_rate_per_user": 0.15,
    "feature_adoption_rate_pct": 0.10,
}

# ---------------------------------------------------------------------------
# CORE FUNCTIONS
# ---------------------------------------------------------------------------


def audit_user_experience(flow_name: str, user_type: str) -> dict[str, Any]:
    """
    Réalise un audit UX complet pour un flux utilisateur spécifique.

    Paramètres
    ----------
    flow_name : str
        Identifiant du flux dans ONBOARDING_FLOWS.
    user_type : str
        Profil utilisateur (RSE_DIRECTOR, LEGAL_COUNSEL, ESG_ANALYST, ADMIN).

    Retourne
    --------
    dict contenant : friction_points, cognitive_load_score, time_waste_minutes,
    quick_fixes, redesign_candidates, accessibility_score.
    """
    flow = ONBOARDING_FLOWS.get(flow_name, {})
    steps = flow.get("steps", [])

    # --- Friction points ---
    friction_points: list[str] = []
    user_key = user_type.upper().replace(" ", "_")
    friction_points.extend(_COMPLIANCE_FRICTION_MAP.get(user_key, []))
    friction_points.extend(_COMPLIANCE_FRICTION_MAP["DEFAULT"])

    for step in steps:
        if step["completion_rate_pct"] < 65.0:
            for dp in step.get("drop_off_points", []):
                entry = f"[{step['step_name']}] {dp}"
                if entry not in friction_points:
                    friction_points.append(entry)

    # --- Cognitive load score (0-10) ---
    # Basé sur les métriques UX globales + structure du flux
    m = UX_METRICS
    raw_error = m["error_rate_pct"]["current"] / 20.0               # 0-1 (20% = max)
    raw_completion = 1.0 - m["task_completion_rate_pct"]["current"] / 100.0
    raw_tti = min(m["time_to_first_value_minutes"]["current"] / 30.0, 1.0)
    raw_tickets = min(m["support_ticket_rate_per_user"]["current"] / 5.0, 1.0)
    raw_adoption = 1.0 - m["feature_adoption_rate_pct"]["current"] / 100.0

    step_difficulty = 0.0
    if steps:
        avg_completion = sum(s["completion_rate_pct"] for s in steps) / len(steps)
        step_difficulty = (1.0 - avg_completion / 100.0) * 2.0  # 0-2 contribution

    cognitive_load_score = round(
        (
            raw_error * _COGNITIVE_LOAD_WEIGHTS["error_rate_pct"]
            + raw_completion * _COGNITIVE_LOAD_WEIGHTS["task_completion_rate_pct"]
            + raw_tti * _COGNITIVE_LOAD_WEIGHTS["time_to_first_value_minutes"]
            + raw_tickets * _COGNITIVE_LOAD_WEIGHTS["support_ticket_rate_per_user"]
            + raw_adoption * _COGNITIVE_LOAD_WEIGHTS["feature_adoption_rate_pct"]
        )
        * 8.0  # scale to 0-8
        + step_difficulty,
        2,
    )
    cognitive_load_score = min(10.0, cognitive_load_score)

    # --- Time waste estimation ---
    target_total = sum(s["duration_minutes"] for s in steps) * 0.60 if steps else 0.0
    current_total = flow.get("total_duration_minutes", 0)
    time_waste_minutes = round(max(0.0, current_total - target_total), 1)

    # --- Quick fixes (impact rapide, < 1 semaine) ---
    quick_fixes: list[str] = [
        "Ajouter une barre de progression visible sur chaque étape du flux",
        "Remplacer les messages d'erreur techniques par des libellés métier clairs",
        "Précharger les valeurs par défaut selon le secteur déclaré à l'inscription",
        "Ajouter des infobulles contextuelles sur les champs réglementaires complexes",
        "Optimiser la détection des emails d'invitation (whitelist domaines courants)",
    ]

    if user_key == "RSE_DIRECTOR":
        quick_fixes.append("Ajouter un template 'démarrage rapide CSRD' pré-configuré")
    elif user_key == "LEGAL_COUNSEL":
        quick_fixes.append("Intégrer des liens EUR-Lex sur chaque référence réglementaire")
    elif user_key == "ESG_ANALYST":
        quick_fixes.append("Activer le mode formulaire mobile optimisé par défaut")
    elif user_key == "ADMIN":
        quick_fixes.append("Fournir un assistant de configuration des droits par rôle-type")

    # --- Redesign candidates (effort moyen-long terme) ---
    redesign_candidates: list[str] = []
    for step in steps:
        if step["completion_rate_pct"] < 55.0:
            redesign_candidates.append(
                f"Refonte complète de l'étape '{step['step_name']}' "
                f"(taux de complétion actuel : {step['completion_rate_pct']}%)"
            )

    if m["time_to_first_value_minutes"]["current"] > m["time_to_first_value_minutes"]["target"] * 1.5:
        redesign_candidates.append(
            "Architecture de navigation : réduire les étapes obligatoires avant la première valeur"
        )

    # --- Accessibility score ---
    compliance_scores = {"PASS": 1.0, "PARTIAL": 0.5, "FAIL": 0.0}
    eu_mandatory_count = sum(
        1 for s in ACCESSIBILITY_STANDARDS.values() if s["eu_mandatory"]
    )
    eu_mandatory_score = sum(
        compliance_scores[s["compliance_level"]]
        for s in ACCESSIBILITY_STANDARDS.values()
        if s["eu_mandatory"]
    )
    non_mandatory_score = sum(
        compliance_scores[s["compliance_level"]]
        for s in ACCESSIBILITY_STANDARDS.values()
        if not s["eu_mandatory"]
    )
    non_mandatory_count = len(ACCESSIBILITY_STANDARDS) - eu_mandatory_count

    if eu_mandatory_count > 0 and non_mandatory_count > 0:
        accessibility_score = round(
            (eu_mandatory_score / eu_mandatory_count) * 0.70 * 100
            + (non_mandatory_score / non_mandatory_count) * 0.30 * 100,
            1,
        )
    elif eu_mandatory_count > 0:
        accessibility_score = round(eu_mandatory_score / eu_mandatory_count * 100, 1)
    else:
        accessibility_score = 0.0

    return {
        "flow_name": flow_name,
        "user_type": user_type,
        "friction_points": friction_points,
        "cognitive_load_score": cognitive_load_score,
        "cognitive_load_label": (
            "FAIBLE" if cognitive_load_score < 3.5
            else "MODÉRÉ" if cognitive_load_score < 6.0
            else "ÉLEVÉ"
        ),
        "time_waste_minutes": time_waste_minutes,
        "quick_fixes": quick_fixes,
        "redesign_candidates": redesign_candidates,
        "accessibility_score": accessibility_score,
        "accessibility_grade": (
            "CONFORME" if accessibility_score >= 80
            else "PARTIEL" if accessibility_score >= 50
            else "NON CONFORME"
        ),
    }


def generate_onboarding_optimization(
    flow: dict[str, Any], target_completion_rate: float
) -> dict[str, Any]:
    """
    Analyse les points d'abandon d'un flux d'onboarding et génère un plan
    d'optimisation avec hypothèses A/B, personnalisation et indicateurs de lift.

    Paramètres
    ----------
    flow : dict
        Un flux issu de ONBOARDING_FLOWS.
    target_completion_rate : float
        Taux de complétion global visé (ex : 85.0 pour 85 %).

    Retourne
    --------
    dict avec A/B_test_hypotheses, personalization_opportunities,
    tooltip_suggestions, progress_indicator_design, estimated_lift_pct.
    """
    steps: list[dict] = flow.get("steps", [])
    current_completion = math.prod(
        s["completion_rate_pct"] / 100.0 for s in steps
    ) * 100.0 if steps else 0.0

    # Identifier les étapes critiques (< 65 % de complétion)
    critical_steps = [s for s in steps if s["completion_rate_pct"] < 65.0]

    # --- Hypothèses A/B test ---
    ab_hypotheses: list[dict[str, str]] = []

    for step in critical_steps:
        for dp in step.get("drop_off_points", [])[:2]:
            ab_hypotheses.append({
                "étape": step["step_name"],
                "hypothèse": f"Résoudre '{dp}' augmentera le taux de complétion de cette étape",
                "variante_A": "Expérience actuelle (contrôle)",
                "variante_B": _generate_ab_variant(dp),
                "métrique_primaire": "Taux de complétion de l'étape",
                "durée_test_jours": "14",
                "taille_échantillon_minimale": "200 utilisateurs par variante",
            })

    # Hypothèses structurelles globales
    ab_hypotheses.append({
        "étape": "Flux global",
        "hypothèse": "Réduire les étapes obligatoires avant la première valeur augmente l'activation",
        "variante_A": f"Flux actuel ({len(steps)} étapes séquentielles)",
        "variante_B": "Flux réduit (3 étapes essentielles + config optionnelle différée)",
        "métrique_primaire": "Taux d'activation J+1 (premier usage valeur)",
        "durée_test_jours": "21",
        "taille_échantillon_minimale": "300 utilisateurs par variante",
    })
    ab_hypotheses.append({
        "étape": "Flux global",
        "hypothèse": "Un onboarding guidé par IA (questions → configuration automatique) "
                     "réduit le time-to-value vs formulaires manuels",
        "variante_A": "Formulaires de configuration actuels",
        "variante_B": "Assistant conversationnel IA : 5 questions → pré-configuration personnalisée",
        "métrique_primaire": "Time-to-first-value (minutes)",
        "durée_test_jours": "21",
        "taille_échantillon_minimale": "250 utilisateurs par variante",
    })

    # --- Opportunités de personnalisation ---
    personalization_opportunities: list[str] = [
        "Détecter le secteur d'activité dès l'inscription → pré-charger référentiels réglementaires pertinents (CSRD, Taxonomie UE, SFDR...)",
        "Adapter le vocabulaire de l'interface selon le rôle (RSE vs Juridique vs Finance)",
        "Proposer des templates de tableaux de bord pré-configurés par profil-type",
        "Personnaliser les alertes réglementaires selon les pays d'opération déclarés",
        "Mémoriser les préférences de navigation et raccourcis fréquents par utilisateur",
        "Adapter le niveau de détail des explications selon l'expertise auto-déclarée",
    ]

    # --- Suggestions de tooltips contextuels ---
    tooltip_suggestions: list[dict[str, str]] = [
        {
            "déclencheur": "Premier contact avec la taxonomie ESG",
            "contenu": "💡 Ce champ utilise la nomenclature GRI 2021. "
                       "Cliquez ici pour voir la correspondance avec votre reporting existant.",
            "format": "Bulle d'aide persistante avec lien documentation",
        },
        {
            "déclencheur": "Inactivité > 90s sur un formulaire complexe",
            "contenu": "Besoin d'aide ? Voir un exemple complété pour une entreprise similaire →",
            "format": "Bannière contextuelle non intrusive (dismiss possible)",
        },
        {
            "déclencheur": "Première erreur de validation",
            "contenu": "Format attendu : [exemple concret]. Conseil : "
                       "exportez votre fichier depuis [ERP courant] en sélectionnant...",
            "format": "Message inline sous le champ concerné avec exemple visuel",
        },
        {
            "déclencheur": "Tentative de quitter le flux avant complétion",
            "contenu": "Votre progression est sauvegardée. Vous reprendrez exactement ici à votre retour.",
            "format": "Modal de confirmation avec résumé de la progression",
        },
        {
            "déclencheur": "Survol des indicateurs de risque",
            "contenu": "Score basé sur [N] critères réglementaires. Voir le détail du calcul →",
            "format": "Tooltip enrichi avec graphique mini synthèse",
        },
    ]

    # --- Design de l'indicateur de progression ---
    progress_indicator_design: dict[str, Any] = {
        "type": "Barre de progression segmentée avec jalons nommés",
        "composants": [
            "Indicateur visuel de l'étape courante (numéro + label court)",
            "Temps estimé restant (recalculé dynamiquement selon le rythme utilisateur)",
            "Checkbox de complétion par étape (persistante entre sessions)",
            "Badge 'Gain débloqué' à chaque étape clé franchie",
        ],
        "persistance": "Sauvegarde automatique toutes les 30 secondes + au changement d'étape",
        "récupération": "Reprise de session au dernier point exact (pas à l'étape, au champ)",
        "motivation": "Message de renforcement positif à chaque étape complétée "
                      "(ex : 'Configuration terminée — vous économiserez 2h/semaine sur vos reportings')",
        "accessibilité": "Annonces ARIA pour lecteurs d'écran à chaque changement d'étape",
    }

    # --- Estimation du lift ---
    gap = target_completion_rate - current_completion
    # Hypothèse : chaque intervention capture ~40 % du gap résiduel
    # (loi des rendements décroissants)
    ab_impact = gap * 0.40
    personalization_impact = gap * 0.20
    tooltip_impact = gap * 0.15
    progress_impact = gap * 0.10
    estimated_lift_pct = round(
        min(ab_impact + personalization_impact + tooltip_impact + progress_impact, gap),
        1,
    )
    projected_completion_rate = round(
        min(current_completion + estimated_lift_pct, target_completion_rate), 1
    )

    return {
        "flux_analysé": flow.get("success_metric", "Non défini"),
        "taux_completion_actuel_pct": round(current_completion, 1),
        "taux_completion_cible_pct": target_completion_rate,
        "gap_pct": round(gap, 1),
        "A/B_test_hypotheses": ab_hypotheses,
        "personalization_opportunities": personalization_opportunities,
        "tooltip_suggestions": tooltip_suggestions,
        "progress_indicator_design": progress_indicator_design,
        "estimated_lift_pct": estimated_lift_pct,
        "projected_completion_rate_pct": projected_completion_rate,
        "implementation_priority": "HAUTE" if gap > 30 else "MOYENNE" if gap > 15 else "STANDARD",
    }


def _generate_ab_variant(drop_off_point: str) -> str:
    """Génère une suggestion de variante B basée sur un point d'abandon."""
    keywords_to_solutions: list[tuple[list[str], str]] = [
        (
            ["format", "fichier", "import", "csv", "dms"],
            "Interface d'import avec détection automatique du format + guide interactif pas-à-pas",
        ),
        (
            ["mfa", "authentication", "sécurité", "vérification", "email"],
            "Authentification simplifiée : lien magique email en 1 clic + MFA optionnel en phase initiale",
        ),
        (
            ["champs", "formulaire", "obligatoire", "saisie"],
            "Formulaire adaptatif : 3 champs essentiels visibles, reste accessible via 'Configurer plus tard'",
        ),
        (
            ["timeout", "performance", "lent", "chargement"],
            "Upload asynchrone avec barre de progression et notification email à la fin",
        ),
        (
            ["permission", "droits", "rôle", "accès"],
            "Matrice de droits simplifiée avec 4 rôles-types pré-configurés + mode expert optionnel",
        ),
        (
            ["documentation", "api", "intégration", "connecteur"],
            "Sandbox interactif avec exemples de code par cas d'usage + support chat dédié API",
        ),
        (
            ["terminologie", "vocabulaire", "classification", "taxonomie"],
            "Glossaire intégré avec définitions contextuelles + mapping vers référentiels connus",
        ),
    ]

    dp_lower = drop_off_point.lower()
    for keywords, solution in keywords_to_solutions:
        if any(kw in dp_lower for kw in keywords):
            return solution

    return "Interface repensée avec divulgation progressive et validation contextuelle en temps réel"


def design_notification_system(
    user_type: str, alert_volume: int
) -> dict[str, Any]:
    """
    Conçoit un système de notification optimal pour prévenir la fatigue d'alertes,
    adapté au profil de professionnel conformité et au volume d'alertes reçues.

    Paramètres
    ----------
    user_type : str
        Profil utilisateur (RSE_DIRECTOR, LEGAL_COUNSEL, ESG_ANALYST, ADMIN).
    alert_volume : int
        Volume d'alertes quotidiennes actuelles.

    Retourne
    --------
    dict avec notification_tiers, batching_rules, quiet_hours,
    digest_format, estimated_alert_fatigue_reduction_pct.
    """
    user_key = user_type.upper().replace(" ", "_")

    # --- Tier definitions par profil ---
    tier_definitions: dict[str, dict[str, Any]] = {
        "RSE_DIRECTOR": {
            "CRITIQUE": {
                "label": "Action requise immédiatement",
                "exemples": [
                    "Deadline réglementaire CSRD < 48h",
                    "Score conformité < seuil critique (rouge)",
                    "Incident ESG matériel détecté",
                ],
                "canal": "Push mobile + email + bannière in-app",
                "délai_max_livraison": "< 5 minutes",
                "volume_max_par_jour": 3,
            },
            "IMPORTANT": {
                "label": "Action requise dans la semaine",
                "exemples": [
                    "Nouveau règlement impactant le périmètre",
                    "Rapport en attente de validation",
                    "Score ESG dégradé d'un fournisseur clé",
                ],
                "canal": "Email + in-app (regroupé)",
                "délai_max_livraison": "< 2 heures",
                "volume_max_par_jour": 8,
            },
            "FYI": {
                "label": "Information de veille — aucune action urgente",
                "exemples": [
                    "Mise à jour du calendrier réglementaire",
                    "Benchmarks sectoriels disponibles",
                    "Tendances ESG du mois",
                ],
                "canal": "Digest hebdomadaire uniquement",
                "délai_max_livraison": "Hebdomadaire (lundi 9h)",
                "volume_max_par_jour": 0,  # groupé en digest
            },
        },
        "LEGAL_COUNSEL": {
            "CRITIQUE": {
                "label": "Risque juridique immédiat",
                "exemples": [
                    "Décision de justice impactant la conformité",
                    "Mise en demeure réglementaire reçue",
                    "Deadline légale < 24h",
                ],
                "canal": "Push mobile + email + SMS si disponible",
                "délai_max_livraison": "< 2 minutes",
                "volume_max_par_jour": 5,
            },
            "IMPORTANT": {
                "label": "Évolution réglementaire structurante",
                "exemples": [
                    "Nouveau texte législatif en vigueur",
                    "Consultation publique ouverte (ESMA, EBA...)",
                    "Modification d'un seuil réglementaire",
                ],
                "canal": "Email structuré + in-app",
                "délai_max_livraison": "< 4 heures",
                "volume_max_par_jour": 10,
            },
            "FYI": {
                "label": "Veille et jurisprudence",
                "exemples": [
                    "Articles de doctrine pertinents",
                    "Positions des autorités de régulation",
                    "Jurisprudence internationale",
                ],
                "canal": "Digest quotidien (format rapport)",
                "délai_max_livraison": "Quotidien (8h)",
                "volume_max_par_jour": 0,
            },
        },
        "ESG_ANALYST": {
            "CRITIQUE": {
                "label": "Anomalie données critique",
                "exemples": [
                    "Données incohérentes détectées dans le reporting",
                    "Indicateur ESG hors seuil matérialité",
                    "Source de données indisponible avant deadline",
                ],
                "canal": "Push mobile + in-app",
                "délai_max_livraison": "< 15 minutes",
                "volume_max_par_jour": 4,
            },
            "IMPORTANT": {
                "label": "Action d'analyse requise",
                "exemples": [
                    "Nouveau jeu de données disponible à valider",
                    "Score ESG fournisseur mis à jour",
                    "Rapport d'analyse en attente de révision",
                ],
                "canal": "In-app + email",
                "délai_max_livraison": "< 1 heure",
                "volume_max_par_jour": 12,
            },
            "FYI": {
                "label": "Mises à jour et benchmarks",
                "exemples": [
                    "Nouveaux datasets sectoriels disponibles",
                    "Mise à jour des méthodologies",
                    "Résultats de pairs pour comparaison",
                ],
                "canal": "Digest hebdomadaire",
                "délai_max_livraison": "Hebdomadaire (vendredi 16h)",
                "volume_max_par_jour": 0,
            },
        },
    }

    notification_tiers = tier_definitions.get(
        user_key,
        tier_definitions["ESG_ANALYST"],
    )

    # --- Règles de regroupement (batching) ---
    batching_rules: list[dict[str, str]] = [
        {
            "règle": "Agrégation thématique",
            "description": "Les alertes sur un même règlement/thème sont regroupées en une seule notification enrichie",
            "seuil_déclenchement": "2 alertes sur le même sujet dans un délai de 30 minutes",
        },
        {
            "règle": "Fenêtre de livraison glissante",
            "description": "Les notifications IMPORTANT sont accumulées et livrées en 3 vagues quotidiennes",
            "vagues": "9h00 · 13h00 · 17h00 (heure locale utilisateur)",
        },
        {
            "règle": "Suppression des doublons",
            "description": "Une alerte déjà lue ou actionnée n'est jamais renvoyée sous un autre format",
            "logique": "Fingerprint sur (type_alerte + entité + date_validité)",
        },
        {
            "règle": "Escalade contrôlée",
            "description": "Un FYI non lu pendant 3 jours reste FYI — pas d'escalade automatique en IMPORTANT",
            "exception": "Sauf si une action devient requise (deadline approchante détectée)",
        },
    ]

    # --- Heures calmes ---
    quiet_hours_config: dict[str, Any] = {
        "plages_protégées": [
            {"label": "Nuit", "début": "20:00", "fin": "07:30", "exception": "CRITIQUE uniquement"},
            {"label": "Déjeuner", "début": "12:30", "fin": "13:30", "exception": "Aucune"},
            {"label": "Focus déclaré", "début": "Selon calendrier utilisateur", "fin": "Selon calendrier utilisateur", "exception": "CRITIQUE uniquement"},
        ],
        "détection_réunion": "Intégration calendrier → silence automatique pendant les réunions",
        "mode_urgence": "Déblocage possible par l'utilisateur pour 1h en cas de besoin",
        "jours_semaine": "Lundi–Vendredi (week-end : CRITIQUE uniquement, sauf opt-in)",
    }

    # --- Format digest ---
    digest_format: dict[str, Any] = {
        "fréquence": "Quotidien (FYI urgents) + Hebdomadaire (veille complète)",
        "structure": [
            "📊 Tableau de bord synthèse (score conformité + variation J-1)",
            "⚡ Actions en attente classées par priorité et deadline",
            "📋 Nouvelles réglementations impactant votre périmètre (résumé 3 lignes + lien)",
            "📈 Évolutions indicateurs ESG clés (sparklines)",
            "📌 Rappels d'échéances à 7 jours",
        ],
        "personnalisation": "Filtrable par domaine réglementaire, entité, et niveau de risque",
        "format_email": "HTML responsive + version texte pour lecteurs d'écran",
        "format_in_app": "Panel latéral collapsible avec badges de comptage",
        "archivage": "Tous les digests archivés et consultables 24 mois",
    }

    # --- Estimation réduction fatigue ---
    # Basé sur : volume actuel → volume cible après système de tiers
    tier_volumes = notification_tiers
    max_daily_delivered = (
        tier_volumes.get("CRITIQUE", {}).get("volume_max_par_jour", 3)
        + tier_volumes.get("IMPORTANT", {}).get("volume_max_par_jour", 8)
        + 1  # digest FYI = 1 notification agrégée
    )
    reduction = round(
        max(0.0, (alert_volume - max_daily_delivered) / alert_volume * 100), 1
    ) if alert_volume > 0 else 0.0

    # Bonus de qualité : moins de bruit = meilleure attention sur ce qui compte
    signal_quality_improvement = round(
        min(reduction * 1.3, 95.0), 1
    )

    return {
        "user_type": user_type,
        "alert_volume_actuel_par_jour": alert_volume,
        "alert_volume_cible_par_jour": max_daily_delivered,
        "notification_tiers": notification_tiers,
        "batching_rules": batching_rules,
        "quiet_hours": quiet_hours_config,
        "digest_format": digest_format,
        "estimated_alert_fatigue_reduction_pct": reduction,
        "signal_quality_improvement_pct": signal_quality_improvement,
        "recommandation_prioritaire": (
            "URGENT — réduire immédiatement le volume d'alertes brutes "
            "via agrégation intelligente avant tout autre optimisation UX"
            if alert_volume >= 30
            else "Optimisation progressive du système de notification recommandée"
        ),
    }


def calculate_comfort_score(metrics: dict[str, Any]) -> dict[str, Any]:
    """
    Calcule l'indice de confort digital global (0–100) à partir des métriques UX,
    de la conformité accessibilité, du succès de l'onboarding et des facteurs de bien-être.

    Paramètres
    ----------
    metrics : dict
        Dictionnaire de métriques UX (format UX_METRICS).

    Retourne
    --------
    dict avec score, grade, weakest_areas, priority_improvements.
    """
    # Composante 1 : Score UX (40 % du total)
    ux_component_scores: dict[str, float] = {}

    def normalize_metric(name: str, current: float, target: float, higher_is_better: bool) -> float:
        """Normalise une métrique entre 0 et 1."""
        benchmark = metrics.get(name, {}).get("industry_benchmark", target)
        if higher_is_better:
            ref_max = max(target, benchmark) * 1.1
            return min(current / ref_max, 1.0) if ref_max > 0 else 0.0
        else:
            ref_max = max(target, benchmark) * 2.0
            return max(0.0, 1.0 - (current - target) / (ref_max - target)) if ref_max > target else 1.0

    metric_configs = [
        ("time_to_first_value_minutes", False),   # moins = mieux
        ("task_completion_rate_pct", True),        # plus = mieux
        ("error_rate_pct", False),                 # moins = mieux
        ("support_ticket_rate_per_user", False),   # moins = mieux
        ("nps_score", True),                       # plus = mieux
        ("feature_adoption_rate_pct", True),       # plus = mieux
        ("session_duration_avg_minutes", True),    # plus = mieux (engagement)
        ("return_rate_7d_pct", True),              # plus = mieux
    ]

    for metric_name, higher_is_better in metric_configs:
        m = metrics.get(metric_name, {})
        current = m.get("current", 0)
        target = m.get("target", 1)
        ux_component_scores[metric_name] = normalize_metric(
            metric_name, current, target, higher_is_better
        )

    ux_score = (sum(ux_component_scores.values()) / len(ux_component_scores)) * 100

    # Composante 2 : Score accessibilité (25 % du total)
    compliance_map = {"PASS": 1.0, "PARTIAL": 0.5, "FAIL": 0.0}
    accessibility_raw = [
        compliance_map[s["compliance_level"]] for s in ACCESSIBILITY_STANDARDS.values()
    ]
    accessibility_score = (sum(accessibility_raw) / len(accessibility_raw)) * 100 if accessibility_raw else 0.0

    # Composante 3 : Score onboarding (20 % du total)
    flow_completion_rates: list[float] = []
    for flow in ONBOARDING_FLOWS.values():
        steps = flow.get("steps", [])
        if steps:
            overall_completion = math.prod(
                s["completion_rate_pct"] / 100.0 for s in steps
            ) * 100.0
            flow_completion_rates.append(overall_completion)
    onboarding_score = (
        sum(flow_completion_rates) / len(flow_completion_rates)
        if flow_completion_rates else 0.0
    )

    # Composante 4 : Score bien-être numérique (15 % du total)
    wellbeing_individual_scores: list[float] = []
    bool_factors = ["notification_frequency_optimal", "dark_mode_available", "focus_mode_available"]
    level_map = {
        "CRITIQUE": 0.0, "ÉLEVÉ": 0.25, "MODÉRÉ": 0.5, "FAIBLE": 1.0,
        False: 0.0, True: 1.0,
    }

    for factor_name, factor_data in DIGITAL_WELLBEING_FACTORS.items():
        current_state = factor_data["current_state"]
        target_state = factor_data["target_state"]
        if factor_name in bool_factors:
            score = level_map.get(current_state, 0.0)
        elif factor_name == "information_overload_score":
            # Current state is 0-10 where 10 = max overload
            score = max(0.0, 1.0 - current_state / 10.0)
        elif factor_name in ("alert_fatigue_level", "cognitive_load_assessment"):
            score = level_map.get(current_state, 0.5)
        else:
            score = 0.5  # valeur neutre si non déterminable
        wellbeing_individual_scores.append(score)

    wellbeing_score = (
        sum(wellbeing_individual_scores) / len(wellbeing_individual_scores) * 100
        if wellbeing_individual_scores else 0.0
    )

    # --- Score global pondéré ---
    comfort_score = round(
        ux_score * 0.40
        + accessibility_score * 0.25
        + onboarding_score * 0.20
        + wellbeing_score * 0.15,
        1,
    )

    # --- Grade ---
    def score_to_grade(s: float) -> str:
        if s >= 85:
            return "A"
        elif s >= 70:
            return "B"
        elif s >= 55:
            return "C"
        elif s >= 40:
            return "D"
        return "F"

    grade = score_to_grade(comfort_score)

    # --- Zones faibles ---
    component_breakdown = {
        "UX & Performance perçue": round(ux_score, 1),
        "Accessibilité numérique": round(accessibility_score, 1),
        "Succès d'onboarding": round(onboarding_score, 1),
        "Bien-être numérique des équipes": round(wellbeing_score, 1),
    }
    weakest_areas = sorted(component_breakdown.items(), key=lambda x: x[1])[:2]

    # --- Améliorations prioritaires ---
    priority_improvements: list[dict[str, str]] = []

    # Métriques UX les plus éloignées de la cible
    ux_gaps = []
    for name, higher in metric_configs:
        m = metrics.get(name, {})
        current = m.get("current", 0)
        target = m.get("target", 1)
        priority = m.get("priority", "MEDIUM")
        if higher:
            gap_pct = max(0.0, (target - current) / target * 100) if target else 0.0
        else:
            gap_pct = max(0.0, (current - target) / current * 100) if current else 0.0
        ux_gaps.append((name, gap_pct, priority))

    ux_gaps.sort(key=lambda x: (0 if x[2] == "CRITICAL" else 1 if x[2] == "HIGH" else 2, -x[1]))
    for name, gap, prio in ux_gaps[:3]:
        m = metrics.get(name, {})
        priority_improvements.append({
            "domaine": "UX",
            "indicateur": name,
            "priorité": m.get("priority", prio),
            "écart_cible_pct": f"{gap:.1f}%",
            "action_recommandée": _ux_action_for(name),
        })

    # Accessibilité non conforme
    for std_name, std in ACCESSIBILITY_STANDARDS.items():
        if std["compliance_level"] in ("FAIL", "PARTIAL") and std["eu_mandatory"]:
            priority_improvements.append({
                "domaine": "Accessibilité",
                "indicateur": std_name,
                "priorité": "CRITIQUE" if std["compliance_level"] == "FAIL" else "HAUTE",
                "écart_cible_pct": "100% (obligation légale EU)",
                "action_recommandée": (
                    f"Mettre en conformité {std['label']} "
                    f"(effort estimé : {std['remediation_effort_days']} jours)"
                ),
            })

    # Bien-être numérique
    if DIGITAL_WELLBEING_FACTORS["alert_fatigue_level"]["current_state"] == "CRITIQUE":
        priority_improvements.append({
            "domaine": "Bien-être numérique",
            "indicateur": "alert_fatigue_level",
            "priorité": "CRITIQUE",
            "écart_cible_pct": "N/A (qualitatif)",
            "action_recommandée": DIGITAL_WELLBEING_FACTORS["alert_fatigue_level"]["improvement_action"],
        })

    # Limiter à 6 améliorations prioritaires max
    priority_improvements = priority_improvements[:6]

    return {
        "comfort_score": comfort_score,
        "grade": grade,
        "grade_label": {
            "A": "Excellent — expérience digitale exemplaire",
            "B": "Bon — quelques axes d'optimisation identifiés",
            "C": "Satisfaisant — améliorations significatives recommandées",
            "D": "Insuffisant — plan de remédiation prioritaire requis",
            "F": "Critique — expérience utilisateur dégradée, action immédiate nécessaire",
        }.get(grade, "Non défini"),
        "component_breakdown": component_breakdown,
        "weakest_areas": [{"zone": k, "score": v} for k, v in weakest_areas],
        "priority_improvements": priority_improvements,
        "interpretation": (
            f"L'indice de confort digital CaelumSwarm™ est de {comfort_score}/100 (grade {grade}). "
            f"Les équipes conformité sous pression réglementaire méritent une expérience fluide et "
            f"accessible. Les zones prioritaires sont : "
            f"{weakest_areas[0][0]} ({weakest_areas[0][1]}/100) "
            f"et {weakest_areas[1][0]} ({weakest_areas[1][1]}/100)."
        ),
    }


def _ux_action_for(metric_name: str) -> str:
    """Retourne une action recommandée pour une métrique UX donnée."""
    actions = {
        "time_to_first_value_minutes": (
            "Repenser le flux d'activation : réduire à 3 étapes avant la première valeur concrète"
        ),
        "task_completion_rate_pct": (
            "Audit des abandons de tâches + simplification des workflows les plus utilisés"
        ),
        "error_rate_pct": (
            "Validation temps réel des formulaires + messages d'erreur contextuels et actionnables"
        ),
        "support_ticket_rate_per_user": (
            "Self-service amélioré : base de connaissance contextuelle + assistant IA in-app"
        ),
        "nps_score": (
            "Programme Voice of Customer : entretiens utilisateurs mensuels + suivi des verbatims"
        ),
        "feature_adoption_rate_pct": (
            "Campagnes de découverte guidée : tooltips progressifs + emails de feature spotlight"
        ),
        "session_duration_avg_minutes": (
            "Augmenter l'engagement : recommandations d'actions contextuelles + tableaux de bord actionnables"
        ),
        "return_rate_7d_pct": (
            "Programme de rétention : digests personnalisés + rappels d'actions en attente"
        ),
    }
    return actions.get(metric_name, "Analyser et optimiser selon les retours utilisateurs")


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------


def run_demo() -> bool:
    """
    Démonstration complète de l'agent Intendant de Confort Digital.

    Exécute et affiche :
    1. Audit UX du flux directeur RSE
    2. Conception système de notifications pour officier conformité (40+ alertes/jour)
    3. Optimisation onboarding avec propositions A/B test
    4. Score de confort global
    """
    separator = "─" * 72

    print(separator)
    print("  AGENT INTENDANT DE CONFORT DIGITAL — CaelumSwarm™")
    print("  Caelum Partners · Rapport de diagnostic UX/Accessibilité/Bien-être")
    print(separator)

    # -----------------------------------------------------------------------
    # 1. Audit UX — Flux RSE Director
    # -----------------------------------------------------------------------
    print("\n[1/4] AUDIT UX — FLUX DIRECTEUR RSE")
    print(separator)

    audit = audit_user_experience("RSE_DIRECTOR_ONBOARDING", "RSE_DIRECTOR")

    print(f"Flux analysé       : {audit['flow_name']}")
    print(f"Profil utilisateur : {audit['user_type']}")
    print(f"Charge cognitive   : {audit['cognitive_load_score']}/10 ({audit['cognitive_load_label']})")
    print(f"Temps perdu        : {audit['time_waste_minutes']} minutes sur le flux complet")
    print(f"Score accessibilité: {audit['accessibility_score']}/100 ({audit['accessibility_grade']})")

    print(f"\nPoints de friction identifiés ({len(audit['friction_points'])}) :")
    for i, fp in enumerate(audit["friction_points"][:6], 1):
        print(f"  {i}. {fp}")
    if len(audit["friction_points"]) > 6:
        print(f"  ... et {len(audit['friction_points']) - 6} autres points")

    print(f"\nCorrections rapides (< 1 semaine) :")
    for qf in audit["quick_fixes"]:
        print(f"  ✓ {qf}")

    print(f"\nCandidats à la refonte ({len(audit['redesign_candidates'])}) :")
    for rc in audit["redesign_candidates"]:
        print(f"  ! {rc}")

    # -----------------------------------------------------------------------
    # 2. Système de notifications — Officier conformité, 40+ alertes/jour
    # -----------------------------------------------------------------------
    print(f"\n[2/4] SYSTÈME DE NOTIFICATIONS — OFFICIER CONFORMITÉ (40 ALERTES/JOUR)")
    print(separator)

    notif = design_notification_system("LEGAL_COUNSEL", 43)

    print(f"Profil             : {notif['user_type']}")
    print(f"Volume actuel      : {notif['alert_volume_actuel_par_jour']} alertes/jour")
    print(f"Volume cible       : {notif['alert_volume_cible_par_jour']} alertes/jour")
    print(f"Réduction fatigue  : {notif['estimated_alert_fatigue_reduction_pct']}%")
    print(f"Amélioration signal: {notif['signal_quality_improvement_pct']}%")
    print(f"\n⚠ {notif['recommandation_prioritaire']}")

    print("\nTiers de notification :")
    for tier_name, tier_data in notif["notification_tiers"].items():
        print(f"\n  [{tier_name}] {tier_data['label']}")
        print(f"    Canal  : {tier_data['canal']}")
        print(f"    Délai  : {tier_data['délai_max_livraison']}")
        print(f"    Volume : max {tier_data['volume_max_par_jour']}/jour" if tier_data['volume_max_par_jour'] > 0 else f"    Volume : groupé en digest")
        print(f"    Exemples conformité :")
        for ex in tier_data["exemples"][:2]:
            print(f"      · {ex}")

    print("\nRègles de regroupement :")
    for rule in notif["batching_rules"][:3]:
        print(f"  · {rule['règle']} : {rule['description']}")

    print("\nHeures calmes protégées :")
    for plage in notif["quiet_hours"]["plages_protégées"]:
        print(f"  · {plage['label']} ({plage['début']}–{plage['fin']}) — Exception : {plage['exception']}")

    print(f"\nFormat digest :")
    for section in notif["digest_format"]["structure"]:
        print(f"  {section}")

    # -----------------------------------------------------------------------
    # 3. Optimisation onboarding — Conseiller juridique
    # -----------------------------------------------------------------------
    print(f"\n[3/4] OPTIMISATION ONBOARDING — CONSEIL JURIDIQUE (CIBLE 85 %)")
    print(separator)

    opt = generate_onboarding_optimization(
        ONBOARDING_FLOWS["LEGAL_COUNSEL_ONBOARDING"],
        target_completion_rate=85.0,
    )

    print(f"Métrique de succès    : {opt['flux_analysé']}")
    print(f"Complétion actuelle   : {opt['taux_completion_actuel_pct']}%")
    print(f"Cible                 : {opt['taux_completion_cible_pct']}%")
    print(f"Écart                 : {opt['gap_pct']} points de pourcentage")
    print(f"Lift estimé           : +{opt['estimated_lift_pct']} pp")
    print(f"Projection post-optim : {opt['projected_completion_rate_pct']}%")
    print(f"Priorité              : {opt['implementation_priority']}")

    print(f"\nHypothèses A/B test ({len(opt['A/B_test_hypotheses'])}) :")
    for i, hyp in enumerate(opt["A/B_test_hypotheses"][:3], 1):
        print(f"\n  Test #{i} — Étape : {hyp['étape']}")
        print(f"    Hypothèse  : {hyp['hypothèse']}")
        print(f"    Variante A : {hyp['variante_A']}")
        print(f"    Variante B : {hyp['variante_B']}")
        print(f"    Métrique   : {hyp['métrique_primaire']} | Durée : {hyp['durée_test_jours']} jours")

    print(f"\nOpportunités de personnalisation :")
    for opp in opt["personalization_opportunities"][:4]:
        print(f"  · {opp}")

    print(f"\nSuggestions de tooltips contextuels :")
    for tip in opt["tooltip_suggestions"][:3]:
        print(f"  [{tip['format']}]")
        print(f"    Déclencheur : {tip['déclencheur']}")
        print(f"    Contenu     : {tip['contenu']}")

    print(f"\nDesign indicateur de progression :")
    for comp in opt["progress_indicator_design"]["composants"]:
        print(f"  · {comp}")

    # -----------------------------------------------------------------------
    # 4. Score de confort global
    # -----------------------------------------------------------------------
    print(f"\n[4/4] SCORE DE CONFORT DIGITAL GLOBAL — CaelumSwarm™")
    print(separator)

    comfort = calculate_comfort_score(UX_METRICS)

    print(f"INDICE DE CONFORT DIGITAL : {comfort['comfort_score']}/100")
    print(f"GRADE                     : {comfort['grade']} — {comfort['grade_label']}")

    print("\nDétail par composante :")
    for comp, score in comfort["component_breakdown"].items():
        bar_len = int(score / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {comp:<38} [{bar}] {score:.1f}/100")

    print(f"\nZones les plus faibles :")
    for area in comfort["weakest_areas"]:
        print(f"  ! {area['zone']} : {area['score']}/100")

    print(f"\nAméliorations prioritaires :")
    for i, imp in enumerate(comfort["priority_improvements"][:5], 1):
        print(f"\n  [{imp['priorité']}] {imp['domaine']} — {imp['indicateur']}")
        print(f"    Action : {imp['action_recommandée']}")

    print(f"\nInterprétation :")
    print(f"  {comfort['interpretation']}")

    print(f"\n{separator}")
    print("  Diagnostic terminé — Agent Intendant de Confort Digital")
    print("  CaelumSwarm™ · Caelum Partners")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_demo()
