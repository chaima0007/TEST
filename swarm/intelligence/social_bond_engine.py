"""Caelum Partners — Social Bond Intelligence Engine
Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger("swarm.social_bond")


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name": "impact_fraud",
        "severity_fr": "Fraude à l'Impact Social",
        "action_fr": "Audit d'impact indépendant et restructuration des métriques ESG",
        "signal_fr": "Déficit critique de mesure d'impact social réel",
    },
    {
        "name": "social_washing",
        "severity_fr": "Social Washing Systémique",
        "action_fr": "Certification tierce partie et transparence totale des données d'impact",
        "signal_fr": "Pratiques de social washing détectées",
    },
    {
        "name": "investor_confidence_collapse",
        "severity_fr": "Effondrement Confiance Investisseurs",
        "action_fr": "Communication de crise et plan de restauration de la confiance",
        "signal_fr": "Érosion sévère de la confiance des investisseurs",
    },
    {
        "name": "regulatory_breach",
        "severity_fr": "Violation Réglementaire ESG",
        "action_fr": "Mise en conformité urgente SFDR et taxonomie UE",
        "signal_fr": "Non-conformité réglementaire obligations sociales",
    },
    {
        "name": "bond_performing",
        "severity_fr": "Obligation Sociale Performante",
        "action_fr": "Maintien des standards et extension des programmes d'impact",
        "signal_fr": "Obligation sociale à impact conforme aux objectifs",
    },
]

_PATTERN_MAP: Dict[str, Dict[str, str]] = {p["name"]: p for p in PATTERNS}


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class EntityRecord:
    entity_id: str
    name: str
    country: str
    sector: str
    impact_measurement_deficit_score: float   # 0-100, weight 0.30
    greenwashing_risk_score: float             # 0-100, weight 0.25
    investor_trust_erosion_score: float        # 0-100, weight 0.25
    regulatory_compliance_gap_score: float     # 0-100, weight 0.20
    confidence_level: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()

    def _compute_composite(self) -> float:
        """
        Weighted composite formula (weights sum to 1.00):
          impact_measurement_deficit_score × 0.30
          + greenwashing_risk_score × 0.25
          + investor_trust_erosion_score × 0.25
          + regulatory_compliance_gap_score × 0.20
        """
        score = (
            self.impact_measurement_deficit_score * 0.30
            + self.greenwashing_risk_score * 0.25
            + self.investor_trust_erosion_score * 0.25
            + self.regulatory_compliance_gap_score * 0.20
        )
        return round(score, 2)

    def _compute_risk_level(self) -> str:
        if self.composite_score >= 60:
            return "critique"
        if self.composite_score >= 40:
            return "élevé"
        if self.composite_score >= 20:
            return "modéré"
        return "faible"

    def _primary_pattern(self) -> str:
        if self.impact_measurement_deficit_score >= 70:
            return "impact_fraud"
        if self.greenwashing_risk_score >= 70:
            return "social_washing"
        if self.investor_trust_erosion_score >= 70:
            return "investor_confidence_collapse"
        if self.regulatory_compliance_gap_score >= 70:
            return "regulatory_breach"
        return "bond_performing"

    def _key_signals(self) -> List[str]:
        """3 domain-specific signals per entity."""
        pattern = self._primary_pattern()
        pat = _PATTERN_MAP[pattern]
        risk = self.risk_level
        return [
            f"{pat['signal_fr']} — {self.name}",
            f"Indice composite obligation sociale: {self.composite_score}/100 ({risk})",
            pat["action_fr"],
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        pattern = self._primary_pattern()
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "impact_measurement_deficit_score": self.impact_measurement_deficit_score,
            "greenwashing_risk_score": self.greenwashing_risk_score,
            "investor_trust_erosion_score": self.investor_trust_erosion_score,
            "regulatory_compliance_gap_score": self.regulatory_compliance_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": pattern,
            "key_signals": self._key_signals(),
            "estimated_bond_index": round(self.composite_score / 100 * 10, 2),
            "last_updated": "2026-06-20",
            "confidence_level": self.confidence_level,
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class SocialBondEngine:
    """
    Swarm Intelligence module for Social Bond risk tracking.

    Computes composite risk scores across impact measurement, greenwashing risk,
    investor trust and regulatory compliance dimensions to surface actionable
    insights for Caelum Partners ESG advisory.
    """

    def __init__(self) -> None:
        self.entities: List[EntityRecord] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "SocialBondEngine initialised — %d entities, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    # ── Mock data ─────────────────────────────────────────────────────────────

    def _build_mock_entities(self) -> List[EntityRecord]:
        """
        8 mock bond issuers covering all 5 patterns and all 4 risk levels.
        Distribution: ≥3 critique, ≥2 élevé, ≥1 modéré, ≥2 faible.

        Composite formula verification (imd*0.30 + gr*0.25 + ite*0.25 + rcg*0.20):
          BON-001: 55*0.30 + 78*0.25 + 65*0.25 + 68*0.20 = 16.5+19.5+16.25+13.6 = 65.85 → critique (social_washing: imd<70, gr=78>=70)
          BON-002: 75*0.30 + 62*0.25 + 60*0.25 + 58*0.20 = 22.5+15.5+15+11.6 = 64.60 → critique (impact_fraud: imd=75>=70)
          BON-003: 55*0.30 + 58*0.25 + 62*0.25 + 72*0.20 = 16.5+14.5+15.5+14.4 = 60.90 → critique (regulatory_breach: imd<70,gr<70,ite<70,rcg=72>=70)
          BON-004: 48*0.30 + 52*0.25 + 72*0.25 + 38*0.20 = 14.4+13+18+7.6 = 53.00 → élevé (investor_confidence_collapse: imd<70,gr<70,ite=72>=70)
          BON-005: 60*0.30 + 42*0.25 + 38*0.25 + 36*0.20 = 18+10.5+9.5+7.2 = 45.20 → élevé (bond_performing: no score>=70)
          BON-006: 32*0.30 + 28*0.25 + 26*0.25 + 22*0.20 = 9.6+7+6.5+4.4 = 27.50 → modéré (bond_performing)
          BON-007: 12*0.30 + 10*0.25 + 14*0.25 + 8*0.20 = 3.6+2.5+3.5+1.6 = 11.20 → faible (bond_performing)
          BON-008:  8*0.30 +  6*0.25 + 10*0.25 +  5*0.20 = 2.4+1.5+2.5+1.0 =  7.40 → faible (bond_performing)
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            # social_washing: imd<70 so pattern walks to greenwashing_risk_score=78>=70
            {
                "entity_id": "BON-001",
                "name": "Obligation Sociale SNCF 2025",
                "country": "France",
                "sector": "Infrastructure",
                "impact_measurement_deficit_score": 55.0,
                "greenwashing_risk_score": 78.0,
                "investor_trust_erosion_score": 65.0,
                "regulatory_compliance_gap_score": 68.0,
                "confidence_level": 0.84,
            },
            # impact_fraud: impact_measurement_deficit_score=75>=70
            {
                "entity_id": "BON-002",
                "name": "UK Social Housing Bond",
                "country": "UK",
                "sector": "Real Estate",
                "impact_measurement_deficit_score": 75.0,
                "greenwashing_risk_score": 62.0,
                "investor_trust_erosion_score": 60.0,
                "regulatory_compliance_gap_score": 58.0,
                "confidence_level": 0.80,
            },
            # regulatory_breach: regulatory_compliance_gap_score >= 70
            {
                "entity_id": "BON-003",
                "name": "Bundesanleihe Social Bond",
                "country": "Germany",
                "sector": "Government",
                "impact_measurement_deficit_score": 55.0,
                "greenwashing_risk_score": 58.0,
                "investor_trust_erosion_score": 62.0,
                "regulatory_compliance_gap_score": 72.0,
                "confidence_level": 0.76,
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            # investor_confidence_collapse: investor_trust_erosion_score >= 70
            {
                "entity_id": "BON-004",
                "name": "ABN AMRO ESG Bond",
                "country": "Netherlands",
                "sector": "Finance",
                "impact_measurement_deficit_score": 48.0,
                "greenwashing_risk_score": 52.0,
                "investor_trust_erosion_score": 72.0,
                "regulatory_compliance_gap_score": 38.0,
                "confidence_level": 0.79,
            },
            # bond_performing pattern (no sub-score >= 70), élevé composite
            {
                "entity_id": "BON-005",
                "name": "BNP Paribas Social Bond",
                "country": "Belgium",
                "sector": "Finance",
                "impact_measurement_deficit_score": 60.0,
                "greenwashing_risk_score": 42.0,
                "investor_trust_erosion_score": 38.0,
                "regulatory_compliance_gap_score": 36.0,
                "confidence_level": 0.77,
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            {
                "entity_id": "BON-006",
                "name": "Nordic Green Social Bond",
                "country": "Sweden",
                "sector": "Environment",
                "impact_measurement_deficit_score": 32.0,
                "greenwashing_risk_score": 28.0,
                "investor_trust_erosion_score": 26.0,
                "regulatory_compliance_gap_score": 22.0,
                "confidence_level": 0.82,
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            {
                "entity_id": "BON-007",
                "name": "UBS Impact Bond",
                "country": "Switzerland",
                "sector": "Finance",
                "impact_measurement_deficit_score": 12.0,
                "greenwashing_risk_score": 10.0,
                "investor_trust_erosion_score": 14.0,
                "regulatory_compliance_gap_score": 8.0,
                "confidence_level": 0.91,
            },
            {
                "entity_id": "BON-008",
                "name": "European Investment Bank Social Bond",
                "country": "Luxembourg",
                "sector": "Finance",
                "impact_measurement_deficit_score": 8.0,
                "greenwashing_risk_score": 6.0,
                "investor_trust_erosion_score": 10.0,
                "regulatory_compliance_gap_score": 5.0,
                "confidence_level": 0.94,
            },
        ]

        return [EntityRecord(**d) for d in raw]  # type: ignore[arg-type]

    # ── Aggregates ────────────────────────────────────────────────────────────

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(self.entities)
        avg_composite = round(sum(e.composite_score for e in self.entities) / n, 2)

        risk_distribution = {
            "critique": sum(1 for e in self.entities if e.risk_level == "critique"),
            "élevé":    sum(1 for e in self.entities if e.risk_level == "élevé"),
            "modéré":   sum(1 for e in self.entities if e.risk_level == "modéré"),
            "faible":   sum(1 for e in self.entities if e.risk_level == "faible"),
        }

        pattern_distribution = {p["name"]: 0 for p in PATTERNS}
        for e in self.entities:
            pat = e._primary_pattern()
            pattern_distribution[pat] = pattern_distribution.get(pat, 0) + 1

        sorted_by_composite = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)
        top_risk_entities = [e.name for e in sorted_by_composite[:3]]
        critical_alerts = [e.name for e in self.entities if e.risk_level == "critique"]

        avg_confidence = round(
            sum(e.confidence_level for e in self.entities) / n, 2
        )

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20T00:00:00Z",
            "engine_version": "1.0.0",
            "domain": "bond",
            "confidence_score": avg_confidence,
            "data_sources": [
                "ICMA Social Bond Principles",
                "EU Social Taxonomy Reports",
                "Bloomberg ESG Data",
            ],
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_bond_index": round(avg_composite / 100 * 10, 2),
        }

    # ── Convenience ───────────────────────────────────────────────────────────

    def get_entities_by_risk(self, risk_level: str) -> List[EntityRecord]:
        return [e for e in self.entities if e.risk_level == risk_level]

    def export(self) -> Dict[str, Any]:
        return {
            "entities": [e.to_dict() for e in self.entities],
            "summary": self.summary(),
            "patterns": self.patterns,
        }


# ── Module-level function ─────────────────────────────────────────────────────

def analyze_bond() -> dict:
    return SocialBondEngine().summary()
