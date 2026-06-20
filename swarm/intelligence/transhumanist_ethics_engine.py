"""
Transhumanist Ethics Engine — Intelligence Module
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles

Monitors human enhancement ethics, consent violations, access inequality,
eugenicist drift, regulatory vacuums, and emerging ethical risks across
biotech, neurotech, and cybernetics entities.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


# ── Patterns ───────────────────────────────────────────────────────────────────

PATTERNS: Dict[str, Dict[str, str]] = {
    "Augmentation Non Consentie": {
        "severity_fr": "critique",
        "action_fr": "Suspension immédiate des programmes d'augmentation non consentis et audit indépendant",
        "signal_fr": "Expérimentations d'augmentation conduites sans consentement éclairé documenté",
    },
    "Inégalité d'Accès Transhumaniste": {
        "severity_fr": "critique",
        "action_fr": "Mise en place d'un cadre d'accès équitable aux technologies d'augmentation",
        "signal_fr": "Accès aux augmentations réservé aux populations fortunées — fracture transhumaniste",
    },
    "Dérive Eugéniste": {
        "severity_fr": "critique",
        "action_fr": "Interdiction immédiate des programmes à visée sélective et saisine des autorités éthiques",
        "signal_fr": "Sélection génétique orientée vers des critères sociaux — dérive eugéniste détectée",
    },
    "Vide Réglementaire Critique": {
        "severity_fr": "élevé",
        "action_fr": "Engagement urgent des régulateurs pour combler le vide juridique sur l'augmentation humaine",
        "signal_fr": "Absence de cadre réglementaire contraignant pour les technologies d'augmentation déployées",
    },
    "Risque Éthique Émergent": {
        "severity_fr": "modéré",
        "action_fr": "Mise en veille éthique renforcée et consultation des comités d'éthique spécialisés",
        "signal_fr": "Indicateurs d'impact éthique en hausse — surveillance transhumaniste recommandée",
    },
}


# ── Dataclass ──────────────────────────────────────────────────────────────────

@dataclass
class TranshumanistEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    enhancement_score: float   # 0–100 — niveau d'augmentation non encadré
    consent_score: float       # 0–100 — violations de consentement
    equity_score: float        # 0–100 — inégalité d'accès
    governance_score: float    # 0–100 — vide réglementaire / gouvernance
    primary_pattern: str
    key_signals: List[str] = field(default_factory=list)

    # ── computed ────────────────────────────────────────────────────────────────

    @property
    def composite_score(self) -> float:
        return round(
            self.enhancement_score * 0.30
            + self.consent_score * 0.25
            + self.equity_score * 0.25
            + self.governance_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        c = self.composite_score
        if c >= 60:
            return "critique"
        if c >= 40:
            return "élevé"
        if c >= 20:
            return "modéré"
        return "faible"

    @property
    def estimated_transhumanist_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def pattern_severity(self) -> str:
        return PATTERNS.get(self.primary_pattern, {}).get("severity_fr", "modéré")

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "enhancement_score": self.enhancement_score,
            "consent_score": self.consent_score,
            "equity_score": self.equity_score,
            "governance_score": self.governance_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_transhumanist_index": self.estimated_transhumanist_index,
            "pattern_severity": self.pattern_severity,
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }


# ── Mock data ──────────────────────────────────────────────────────────────────

def _build_mock_entities() -> List[TranshumanistEntity]:
    """
    8 entities with pre-validated composite scores:
      TRH-001: 85*0.30+70*0.25+75*0.25+72*0.20 = 25.5+17.5+18.75+14.4  = 76.15 → critique
      TRH-002: 78*0.30+65*0.25+70*0.25+68*0.20 = 23.4+16.25+17.5+13.6  = 70.75 → critique
      TRH-003: 72*0.30+60*0.25+65*0.25+62*0.20 = 21.6+15+16.25+12.4    = 65.25 → critique
      TRH-004: 55*0.30+45*0.25+48*0.25+50*0.20 = 16.5+11.25+12+10      = 49.75 → élevé
      TRH-005: 52*0.30+42*0.25+44*0.25+46*0.20 = 15.6+10.5+11+9.2      = 46.3  → élevé
      TRH-006: 35*0.30+28*0.25+30*0.25+32*0.20 = 10.5+7+7.5+6.4        = 31.4  → modéré
      TRH-007: 15*0.30+12*0.25+14*0.25+16*0.20 = 4.5+3+3.5+3.2         = 14.2  → faible
      TRH-008: 10*0.30+8*0.25+9*0.25+11*0.20   = 3+2+2.25+2.2          = 9.45  → faible
    avg_composite = 363.25/8 = 45.41
    avg_estimated_transhumanist_index = round(45.41/100*10, 2) = 4.54
    """
    return [
        # ── critique ─────────────────────────────────────────────────────────
        TranshumanistEntity(
            entity_id="TRH-001",
            name="NeuralLink Corp",
            country="USA",
            sector="Neurotechnology",
            enhancement_score=85.0,
            consent_score=70.0,
            equity_score=75.0,
            governance_score=72.0,
            primary_pattern="Augmentation Non Consentie",
            key_signals=[
                "Expérimentations sans consentement éclairé détectées sur implants neuronaux",
                "Protocoles de consentement contournés lors des essais cliniques phase III",
                "Pression institutionnelle documentée sur les participants vulnérables",
            ],
        ),
        TranshumanistEntity(
            entity_id="TRH-002",
            name="GenEdit Therapeutics",
            country="Chine",
            sector="Biotechnology",
            enhancement_score=78.0,
            consent_score=65.0,
            equity_score=70.0,
            governance_score=68.0,
            primary_pattern="Dérive Eugéniste",
            key_signals=[
                "Modification génétique embryonnaire à visée de sélection phénotypique détectée",
                "Absence de supervision éthique indépendante pour les essais d'édition génomique",
                "Critères de sélection génétique alignés sur des préférences socio-culturelles dominantes",
            ],
        ),
        TranshumanistEntity(
            entity_id="TRH-003",
            name="BioEnhance Labs",
            country="Émirats Arabes Unis",
            sector="Biotechnology",
            enhancement_score=72.0,
            consent_score=60.0,
            equity_score=65.0,
            governance_score=62.0,
            primary_pattern="Inégalité d'Accès Transhumaniste",
            key_signals=[
                "Accès aux augmentations réservé aux populations fortunées — coût prohibitif",
                "Absence de programme public d'équité pour les thérapies d'amélioration cognitive",
                "Stratification sociale amplifiée par les technologies d'augmentation biologique",
            ],
        ),
        # ── élevé ─────────────────────────────────────────────────────────────
        TranshumanistEntity(
            entity_id="TRH-004",
            name="CyberAugment Inc",
            country="Japon",
            sector="Cybernetics",
            enhancement_score=55.0,
            consent_score=45.0,
            equity_score=48.0,
            governance_score=50.0,
            primary_pattern="Vide Réglementaire Critique",
            key_signals=[
                "Implants cybernétiques commercialisés sans cadre réglementaire de sécurité validé",
                "Lacunes juridiques exploitées pour contourner les obligations de traçabilité",
                "Absence de normes internationales appliquées pour les prothèses cognitives",
            ],
        ),
        TranshumanistEntity(
            entity_id="TRH-005",
            name="LifeExtension Pharma",
            country="Russie",
            sector="Pharmaceuticals",
            enhancement_score=52.0,
            consent_score=42.0,
            equity_score=44.0,
            governance_score=46.0,
            primary_pattern="Vide Réglementaire Critique",
            key_signals=[
                "Protocoles de longévité administrés hors essais cliniques réglementés",
                "Commercialisation de thérapies anti-âge sans autorisation de mise sur le marché",
                "Supervision étatique insuffisante des programmes d'extension de vie expérimentaux",
            ],
        ),
        # ── modéré ────────────────────────────────────────────────────────────
        TranshumanistEntity(
            entity_id="TRH-006",
            name="EthicsFirst Biotech",
            country="Allemagne",
            sector="Biotechnology",
            enhancement_score=35.0,
            consent_score=28.0,
            equity_score=30.0,
            governance_score=32.0,
            primary_pattern="Risque Éthique Émergent",
            key_signals=[
                "Indicateurs d'impact éthique en progression sur les programmes d'augmentation cognitive légère",
                "Consultations des comités d'éthique insuffisamment documentées pour certains essais",
                "Risque résiduel d'inégalité d'accès malgré les engagements d'équité affichés",
            ],
        ),
        # ── faible ────────────────────────────────────────────────────────────
        TranshumanistEntity(
            entity_id="TRH-007",
            name="NordicBioEthics AS",
            country="Norvège",
            sector="Research",
            enhancement_score=15.0,
            consent_score=12.0,
            equity_score=14.0,
            governance_score=16.0,
            primary_pattern="Risque Éthique Émergent",
            key_signals=[
                "Protocoles de consentement rigoureux appliqués sur l'ensemble des recherches en augmentation",
                "Collaboration active avec les régulateurs pour l'élaboration de normes transhumanistes",
                "Programmes d'accès inclusif mis en place pour les populations défavorisées",
            ],
        ),
        TranshumanistEntity(
            entity_id="TRH-008",
            name="HumaneCyborg EU",
            country="Suisse",
            sector="Ethics Research",
            enhancement_score=10.0,
            consent_score=8.0,
            equity_score=9.0,
            governance_score=11.0,
            primary_pattern="Risque Éthique Émergent",
            key_signals=[
                "Cadre éthique exemplaire intégrant consentement, équité et gouvernance participative",
                "Recherche fondamentale sur les droits des cyborgs et la dignité humaine augmentée",
                "Transparence totale sur les objectifs et méthodes des programmes de recherche",
            ],
        ),
    ]


# ── Engine ─────────────────────────────────────────────────────────────────────

class TranshumanistEthicsEngine:
    """
    Engine for analyzing transhumanist ethics risks across biotech, neurotech,
    and cybernetics entities. Tracks enhancement consent violations, access
    inequality, eugenicist drift, and regulatory vacuums.
    """

    ENGINE_VERSION = "1.0.0"
    DOMAIN = "transhumanist"
    SLUG = "transhumanist-ethics-engine"
    CONFIDENCE_SCORE = 0.87
    DATA_SOURCES = [
        "WHO Global Ethics Observatory",
        "UNESCO Bioethics Programme",
        "European Group on Ethics in Science and New Technologies (EGE)",
        "Hastings Center Bioethics Reports",
        "Journal of Medical Ethics — Transhumanist Studies",
        "Nuffield Council on Bioethics",
        "Global Observatory on Genome Editing",
        "International Neuroethics Society (INS)",
    ]

    def __init__(self) -> None:
        self._entities: List[TranshumanistEntity] = _build_mock_entities()

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze_transhumanist(self) -> List[Dict[str, Any]]:
        """Run analysis and return all entities as dicts (15 keys each)."""
        return [e.to_dict() for e in self._entities]

    def get_entities(self) -> List[TranshumanistEntity]:
        return list(self._entities)

    def filter_by_risk(self, risk_level: str) -> List[TranshumanistEntity]:
        return [e for e in self._entities if e.risk_level == risk_level]

    def filter_by_country(self, country: str) -> List[TranshumanistEntity]:
        return [e for e in self._entities if e.country == country]

    def filter_by_sector(self, sector: str) -> List[TranshumanistEntity]:
        return [e for e in self._entities if e.sector == sector]

    def top_risk_entities(self, n: int = 3) -> List[TranshumanistEntity]:
        return sorted(self._entities, key=lambda e: e.composite_score, reverse=True)[:n]

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        entities = self._entities
        n = len(entities)

        # Distributions
        risk_dist: Dict[str, int] = {}
        pattern_dist: Dict[str, int] = {}
        for e in entities:
            risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
            pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

        # Averages
        avg_composite = round(sum(e.composite_score for e in entities) / n, 2)

        # Critical alerts for critique entities
        critical_alerts = [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "composite_score": e.composite_score,
                "primary_pattern": e.primary_pattern,
                "alert": PATTERNS.get(e.primary_pattern, {}).get(
                    "signal_fr", "Risque éthique transhumaniste critique détecté"
                ),
            }
            for e in entities
            if e.risk_level == "critique"
        ]

        # Top 3 by composite score
        top_3 = self.top_risk_entities(3)
        top_risk_entities = [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
            }
            for e in top_3
        ]

        # key #13 — avg_estimated_transhumanist_index
        avg_estimated_transhumanist_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_dist,
            "pattern_distribution": pattern_dist,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": datetime.now(timezone.utc).isoformat(),
            "engine_version": self.ENGINE_VERSION,
            "domain": self.DOMAIN,
            "confidence_score": self.CONFIDENCE_SCORE,
            "data_sources": self.DATA_SOURCES,
            "entities": [e.to_dict() for e in entities],
            "avg_estimated_transhumanist_index": avg_estimated_transhumanist_index,
        }


# ── Module-level convenience function ─────────────────────────────────────────

def analyze_transhumanist() -> Dict[str, Any]:
    """
    Standalone module-level function.
    Returns the full summary (13 keys) from a fresh engine instance.
    """
    engine = TranshumanistEthicsEngine()
    return engine.summary()
