"""
Caelum Partners — Social Cohesion Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Analyse de la cohésion sociale comme infrastructure invisible de la stabilité
civilisationnelle — la colle qui maintient les sociétés ensemble.

La cohésion sociale mesure la capacité d'une société à fonctionner comme un
tout : confiance interpersonnelle, sentiment d'appartenance commune, solidarité
et capacité à résoudre les conflits de manière pacifique.

Risk levels:
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "dissolution_sociale": {
        "severity_fr": "Critique",
        "action_fr": "Plan d'urgence de cohésion nationale — dialogue inter-communautaire et réforme des inégalités",
        "signal_fr": "trust_deficit > 85 AND polarization_score > 80 — effondrement du tissu social imminent",
    },
    "fragmentation_identitaire": {
        "severity_fr": "Critique",
        "action_fr": "Programmes de réconciliation nationale et réforme des systèmes d'inégalité structurelle",
        "signal_fr": "Fractures identitaires profondes — tribalisations politique, ethnique ou économique",
    },
    "polarisation_croissante": {
        "severity_fr": "Élevé",
        "action_fr": "Investissements dans les espaces de délibération commune et réduction des inégalités",
        "signal_fr": "Polarisation politique et économique en hausse — cohésion sous pression croissante",
    },
    "tensions_latentes": {
        "severity_fr": "Modéré",
        "action_fr": "Renforcement du dialogue civique et politiques sociales préventives",
        "signal_fr": "Tensions sociales gérables — cohésion maintenue avec surveillance active",
    },
    "cohesion_consolidee": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des investissements dans le capital social et la confiance institutionnelle",
        "signal_fr": "composite_score < 30 — société cohésive avec forte confiance interpersonnelle",
    },
}


@dataclass
class SocialCohesionEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    trust_deficit_score: float
    polarization_score: float
    inequality_fracture_score: float
    identity_fragmentation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_cohesion_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.trust_deficit_score * 0.30
            + self.polarization_score * 0.25
            + self.inequality_fracture_score * 0.25
            + self.identity_fragmentation_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_cohesion_index = round(self.composite_score / 100 * 10, 2)

    def _risk(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    def _pattern(self) -> str:
        if self.trust_deficit_score >= 85 and self.polarization_score >= 80:
            return "dissolution_sociale"
        if self.identity_fragmentation_score >= 75 and self.inequality_fracture_score >= 70:
            return "fragmentation_identitaire"
        if self.composite_score >= 45:
            return "polarisation_croissante"
        if self.composite_score >= 25:
            return "tensions_latentes"
        return "cohesion_consolidee"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Dissolution sociale critique pour {n} — tissu social en rupture systémique",
                "Déficit de confiance et polarisation au-delà des seuils de réconciliation normale",
                "Fractures identitaires et économiques se renforçant mutuellement",
            ]
        if self.risk_level == "élevé":
            return [
                f"Cohésion sociale sous haute pression pour {n} — fragmentation croissante",
                "Polarisation politique et économique réduisant la capacité de compromis",
                "Confiance institutionnelle en érosion — investissements sociaux urgents",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tensions sociales modérées pour {n} — vigilance et politiques préventives",
                "Fractures identifiables mais maîtrisables par le dialogue civique",
                "Cohésion maintenue avec risques émergents à surveiller",
            ]
        return [
            f"{n} présente une cohésion sociale forte et un capital de confiance élevé",
            "Confiance interpersonnelle et institutionnelle dans les normes saines",
            "Société résiliente — capacité de résolution des conflits préservée",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "trust_deficit_score": self.trust_deficit_score,
            "polarization_score": self.polarization_score,
            "inequality_fracture_score": self.inequality_fracture_score,
            "identity_fragmentation_score": self.identity_fragmentation_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_cohesion_index": self.estimated_cohesion_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SocialCohesionEntity] = [
    SocialCohesionEntity("SC-001", "États-Unis — Polarisation Extrême", "Amérique du Nord", "Démocratie Fracturée", 88.0, 92.0, 75.0, 80.0),
    SocialCohesionEntity("SC-002", "Brésil — Inégalités Structurelles", "Amériques", "Société Polarisée", 80.0, 78.0, 85.0, 72.0),
    SocialCohesionEntity("SC-003", "Liban — Collapse Communitaire", "MENA", "Fragmentation Multi-Confessionnelle", 92.0, 85.0, 82.0, 90.0),
    SocialCohesionEntity("SC-004", "Afrique du Sud — Post-Apartheid", "Afrique", "Fractures Raciales & Économiques", 75.0, 70.0, 88.0, 68.0),
    SocialCohesionEntity("SC-005", "Royaume-Uni — Post-Brexit", "Europe", "Fracture Identitaire Nationale", 58.0, 65.0, 55.0, 62.0),
    SocialCohesionEntity("SC-006", "France — Gilets Jaunes Persistants", "Europe", "Fracture Territoriale", 52.0, 58.0, 62.0, 48.0),
    SocialCohesionEntity("SC-007", "Allemagne & Europe Centrale", "Europe", "Cohésion Institutionnelle", 28.0, 32.0, 35.0, 25.0),
    SocialCohesionEntity("SC-008", "Scandinavie — Modèle Social", "Europe du Nord", "Haute Cohésion Sociale", 10.0, 8.0, 12.0, 6.0),
]


def summary() -> dict[str, Any]:
    entities = MOCK_ENTITIES
    n = len(entities)
    avg = round(sum(e.composite_score for e in entities) / n, 2)

    risk_dist: dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: dict[str, int] = {k: 0 for k in PATTERNS}
    critical_alerts: list[str] = []
    top_risk: list[str] = []

    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        if e.risk_level == "critique":
            critical_alerts.append(f"{e.name}: {e.primary_pattern.replace('_', ' ')}")
            top_risk.append(e.name)

    return {
        "total_entities": n,
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "cohesion",
        "confidence_score": 0.83,
        "data_sources": ["social_cohesion_index", "trust_barometer", "polarization_tracker"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_cohesion_index": round(avg / 100 * 10, 2),
    }


def analyze_social_cohesion() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Social Cohesion Engine — {r['total_entities']} sociétés, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
