from datetime import datetime
from typing import Any

DOMAIN = "telemedicine"
SLUG = "telemedicine-engine"
ENGINE_VERSION = "1.0.0"

PATTERNS = [
    {
        "name": "Désert Médical Numérique",
        "severity_fr": "critique",
        "action_fr": "Déploiement d'urgence d'infrastructures de télémédecine dans les zones non desservies",
        "signal_fr": "Absence de connectivité et de dispositifs médicaux numériques dans les régions isolées",
    },
    {
        "name": "Fraude Téléconsultation",
        "severity_fr": "critique",
        "action_fr": "Audit immédiat des plateformes de téléconsultation et renforcement des contrôles d'identité",
        "signal_fr": "Facturation frauduleuse et identités usurpées détectées sur les flux de téléconsultation",
    },
    {
        "name": "Faille Sécurité Données Santé",
        "severity_fr": "élevé",
        "action_fr": "Mise en conformité RGPD et chiffrement bout-en-bout des dossiers médicaux numériques",
        "signal_fr": "Exposition de données de santé sensibles et accès non autorisés aux systèmes médicaux",
    },
    {
        "name": "Adoption Insuffisante",
        "severity_fr": "modéré",
        "action_fr": "Campagne de sensibilisation et programme de formation des professionnels de santé",
        "signal_fr": "Faible taux d'utilisation des outils de télémédecine malgré la disponibilité des infrastructures",
    },
    {
        "name": "Qualité Consultation Dégradée",
        "severity_fr": "faible",
        "action_fr": "Révision des protocoles de consultation à distance et amélioration des interfaces cliniques",
        "signal_fr": "Satisfaction patient en baisse et taux d'erreur diagnostique élevé en téléconsultation",
    },
]


class TelemedicineEntity:
    def __init__(
        self,
        entity_id: str,
        name: str,
        country: str,
        sector: str,
        access_score: float,
        quality_score: float,
        security_score: float,
        adoption_score: float,
        primary_pattern: str,
        key_signals: list,
    ):
        self.entity_id = entity_id
        self.name = name
        self.country = country
        self.sector = sector
        self.access_score = access_score
        self.quality_score = quality_score
        self.security_score = security_score
        self.adoption_score = adoption_score
        self.composite_score = round(
            access_score * 0.30
            + quality_score * 0.25
            + security_score * 0.25
            + adoption_score * 0.20,
            2,
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.primary_pattern = primary_pattern
        self.key_signals = key_signals
        self.estimated_telemedicine_index = round(self.composite_score / 100 * 10, 2)
        self.last_updated = "2026-06-20"
        _pattern_map = {p["name"]: p["severity_fr"] for p in PATTERNS}
        self.pattern_severity = _pattern_map.get(primary_pattern, "inconnu")

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "access_score": self.access_score,
            "quality_score": self.quality_score,
            "security_score": self.security_score,
            "adoption_score": self.adoption_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "pattern_severity": self.pattern_severity,
            "key_signals": self.key_signals,
            "estimated_telemedicine_index": self.estimated_telemedicine_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES = [
    TelemedicineEntity(
        entity_id="TLM-001",
        name="CHU Afrique Sub-Saharienne",
        country="Senegal",
        sector="Healthcare",
        access_score=85.0,
        quality_score=78.0,
        security_score=72.0,
        adoption_score=80.0,
        primary_pattern="Désert Médical Numérique",
        key_signals=[
            "Couverture réseau mobile inférieure à 30% dans les zones rurales périphériques",
            "Absence de dispositifs de diagnostic connectés dans 68% des centres de santé",
            "Délai moyen de téléconsultation supérieur à 72 heures faute d'infrastructure",
        ],
    ),
    TelemedicineEntity(
        entity_id="TLM-002",
        name="Clinique Rurale Myanmar",
        country="Myanmar",
        sector="Healthcare",
        access_score=90.0,
        quality_score=82.0,
        security_score=68.0,
        adoption_score=75.0,
        primary_pattern="Désert Médical Numérique",
        key_signals=[
            "Ratio médecin-patient de 1 pour 12 000 habitants en zone rurale",
            "Infrastructure électrique défaillante rendant inutilisables 40% des équipements télé-médicaux",
            "Barrière linguistique critique affectant la qualité des consultations à distance",
        ],
    ),
    TelemedicineEntity(
        entity_id="TLM-003",
        name="TeleSanté Haïti",
        country="Haiti",
        sector="Healthcare",
        access_score=88.0,
        quality_score=75.0,
        security_score=65.0,
        adoption_score=70.0,
        primary_pattern="Fraude Téléconsultation",
        key_signals=[
            "Multiplication des plateformes non agréées proposant des consultations médicales frauduleuses",
            "Usurpation d'identité de médecins détectée dans 23% des sessions de téléconsultation auditées",
            "Facturation illicite de médicaments non prescrits via des canaux de télémédecine parallèles",
        ],
    ),
    TelemedicineEntity(
        entity_id="TLM-004",
        name="Hopital District Maroc",
        country="Morocco",
        sector="Healthcare",
        access_score=55.0,
        quality_score=48.0,
        security_score=42.0,
        adoption_score=50.0,
        primary_pattern="Faille Sécurité Données Santé",
        key_signals=[
            "Dossiers médicaux électroniques stockés sans chiffrement sur des serveurs locaux vulnérables",
            "Absence de protocole d'authentification multifacteur pour les accès aux systèmes médicaux distants",
            "Trois incidents de fuite de données patients signalés au cours des six derniers mois",
        ],
    ),
    TelemedicineEntity(
        entity_id="TLM-005",
        name="DocConnect India Rural",
        country="India",
        sector="HealthTech",
        access_score=58.0,
        quality_score=45.0,
        security_score=40.0,
        adoption_score=52.0,
        primary_pattern="Faille Sécurité Données Santé",
        key_signals=[
            "API de partage de données médicales exposées sans authentification sur des endpoints publics",
            "Conformité PDPA insuffisante avec stockage de données biométriques hors consentement",
            "Vulnérabilités zero-day non corrigées dans l'application mobile de téléconsultation",
        ],
    ),
    TelemedicineEntity(
        entity_id="TLM-006",
        name="MedTech SARL",
        country="France",
        sector="HealthTech",
        access_score=30.0,
        quality_score=28.0,
        security_score=25.0,
        adoption_score=22.0,
        primary_pattern="Adoption Insuffisante",
        key_signals=[
            "Taux d'utilisation de la plateforme de télémédecine inférieur à 15% parmi les praticiens inscrits",
            "Résistance au changement des équipes médicales formées aux pratiques de consultation présentielle",
            "Absence de remboursement systématique des téléconsultations par les organismes de sécurité sociale partenaires",
        ],
    ),
    TelemedicineEntity(
        entity_id="TLM-007",
        name="TeleClinic Nordic",
        country="Sweden",
        sector="Healthcare",
        access_score=12.0,
        quality_score=10.0,
        security_score=8.0,
        adoption_score=15.0,
        primary_pattern="Qualité Consultation Dégradée",
        key_signals=[
            "Score de satisfaction patient en baisse de 18 points suite à la dégradation de la qualité audio-vidéo",
            "Taux de rediagnostic post-téléconsultation de 8% indiquant des erreurs d'évaluation à distance",
            "Durée moyenne de consultation réduite à 4 minutes en raison de la surcharge des files d'attente virtuelles",
        ],
    ),
    TelemedicineEntity(
        entity_id="TLM-008",
        name="DigitalHealth AG",
        country="Switzerland",
        sector="HealthTech",
        access_score=10.0,
        quality_score=8.0,
        security_score=12.0,
        adoption_score=10.0,
        primary_pattern="Qualité Consultation Dégradée",
        key_signals=[
            "Latence réseau moyenne de 340ms dégradant significativement la qualité des consultations spécialisées",
            "Taux d'abandon en cours de téléconsultation de 22% lié à des problèmes de connectivité",
            "Manque d'intégration avec les systèmes HIS hospitaliers entraînant des doublons de prescriptions",
        ],
    ),
]


def analyze_telemedicine() -> dict[str, Any]:
    entities = [e.to_dict() for e in MOCK_ENTITIES]

    risk_distribution: dict[str, int] = {}
    pattern_distribution: dict[str, int] = {}
    top_risk_entities: list[dict[str, Any]] = []
    critical_alerts: list[str] = []
    total_composite = 0.0

    for e in entities:
        risk = e["risk_level"]
        pattern = e["primary_pattern"]
        risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
        pattern_distribution[pattern] = pattern_distribution.get(pattern, 0) + 1
        total_composite += e["composite_score"]
        if risk == "critique":
            top_risk_entities.append(
                {
                    "entity_id": e["entity_id"],
                    "name": e["name"],
                    "composite_score": e["composite_score"],
                    "risk_level": e["risk_level"],
                }
            )
            critical_alerts.append(
                f"{e['entity_id']} — {e['name']} ({e['country']}): {e['primary_pattern']} [composite={e['composite_score']}]"
            )

    n = len(entities) or 1
    avg_composite = round(total_composite / n, 2)

    return {
        "total_entities": n,
        "avg_composite": avg_composite,
        "risk_distribution": risk_distribution,
        "pattern_distribution": pattern_distribution,
        "top_risk_entities": top_risk_entities,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-20",
        "engine_version": ENGINE_VERSION,
        "domain": DOMAIN,
        "confidence_score": 0.91,
        "data_sources": [
            "WHO Telemedicine Registry",
            "ITU Digital Health Index",
            "GSMA Mobile Health Report",
        ],
        "entities": entities,
        "avg_estimated_telemedicine_index": round(avg_composite / 100 * 10, 2),
    }


def summary() -> dict:
    """Module-level summary alias for swarm orchestrator compatibility."""
    return analyze_telemedicine()
