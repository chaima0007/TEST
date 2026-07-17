"""
Caelum Partners — Treaty Erosion & International Order Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'érosion de l'ordre international fondé sur les règles : quand les grandes
puissances se retirent des traités multilatéraux, violent le droit international
ou contournent les institutions comme l'ONU, l'OMC et la CPI, c'est l'architecture
de paix construite depuis 1945 qui se fissure.

La désinstitutionnalisation du monde n'est pas un repli vers la souveraineté —
c'est une régression vers la loi du plus fort où les rapports de force
remplacent les normes juridiques. La fragmentation du droit international
est la condition préalable à tous les autres risques géopolitiques.

Risk levels (intensité de l'érosion de l'ordre international) :
  critique  → composite ≥ 60  (désintégration de l'ordre multilatéral)
  élevé     → composite ≥ 40  (fragilisation systémique des traités)
  modéré    → composite ≥ 20  (tensions sur les normes internationales)
  faible    → composite < 20  (ancrage multilatéral solide)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "desintegration_multilaterale": {
        "severity_fr": "Critique",
        "action_fr": "Coalition de défense du multilatéralisme — réforme urgente des institutions et sanctions des violations",
        "signal_fr": "treaty_withdrawal_score > 80 AND un_veto_abuse > 75 — désintégration de l'ordre multilatéral",
    },
    "erosion_systematique": {
        "severity_fr": "Critique",
        "action_fr": "Renforcement des mécanismes de contrôle du droit international et accountability des violations",
        "signal_fr": "Érosion systématique des traités — violations répétées sans sanction effective",
    },
    "fragmentation_normative": {
        "severity_fr": "Élevé",
        "action_fr": "Diplomatie multilatérale renforcée et soutien aux institutions internationales fragilisées",
        "signal_fr": "Fragmentation normative — blocs géopolitiques créant des ordres juridiques concurrents",
    },
    "tensions_institutionnelles": {
        "severity_fr": "Modéré",
        "action_fr": "Réforme graduelle des institutions multilatérales pour restaurer leur légitimité et efficacité",
        "signal_fr": "Tensions institutionnelles — pressions sur les traités mais cadre multilatéral préservé",
    },
    "ancrage_multilateral": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de l'engagement multilatéral actif et leadership dans la réforme des institutions",
        "signal_fr": "composite_score < 20 — ancrage multilatéral exemplaire, respect des traités et institutions",
    },
}


@dataclass
class TreatyErosionEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    treaty_withdrawal_score: float
    international_law_violation_score: float
    multilateral_institution_undermining_score: float
    normative_fragmentation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_erosion_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.treaty_withdrawal_score * 0.30
            + self.international_law_violation_score * 0.25
            + self.multilateral_institution_undermining_score * 0.25
            + self.normative_fragmentation_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_erosion_index = round(self.composite_score / 100 * 10, 2)

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
        if self.treaty_withdrawal_score >= 80 and self.multilateral_institution_undermining_score >= 75:
            return "desintegration_multilaterale"
        if self.international_law_violation_score >= 70:
            return "erosion_systematique"
        if self.composite_score >= 45:
            return "fragmentation_normative"
        if self.composite_score >= 25:
            return "tensions_institutionnelles"
        return "ancrage_multilateral"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Désintégration de l'ordre multilatéral par {n} — retrait systématique des traités fondateurs",
                "Violations répétées du droit international sans accountability — impunité normative",
                "Sabotage des institutions multilatérales — ONU, OMC, CPI neutralisées par veto ou boycott",
            ]
        if self.risk_level == "élevé":
            return [
                f"Fragmentation normative grave dans {n} — ordres juridiques concurrents en construction",
                "Sélectivité dans l'application du droit international — deux poids deux mesures institutionnalisés",
                "Institutions multilatérales fragilisées — légitimité et capacité d'action en déclin",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tensions institutionnelles dans {n} — pressions sur les traités mais ordre préservé",
                "Remise en question partielle du multilatéralisme — réformes nécessaires pour restaurer la confiance",
                "Fragmentation normative naissante — blocs régionaux testant les limites du droit international",
            ]
        return [
            f"{n} maintient un ancrage multilatéral exemplaire — respect des traités et des institutions",
            "Investissement actif dans le système multilatéral — réformateur constructif de l'ordre international",
            "Modèle de diplomatie multilatérale à valoriser et à diffuser pour renforcer la paix",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "treaty_withdrawal_score": self.treaty_withdrawal_score,
            "international_law_violation_score": self.international_law_violation_score,
            "multilateral_institution_undermining_score": self.multilateral_institution_undermining_score,
            "normative_fragmentation_score": self.normative_fragmentation_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_erosion_index": self.estimated_erosion_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[TreatyErosionEntity] = [
    TreatyErosionEntity("TE-001", "Russie — Droit International Baffoué", "Europe de l'Est", "Violations du Droit International & Veto ONU", 90.0, 95.0, 88.0, 85.0),
    TreatyErosionEntity("TE-002", "USA — Unilatéralisme Sélectif", "Amérique du Nord", "Retrait Traités & Sanctions Extraterritoriales", 85.0, 75.0, 80.0, 82.0),
    TreatyErosionEntity("TE-003", "Chine — Droit de la Mer Contesté", "Asie", "Rejet UNCLOS & Prétentions Unilatérales", 78.0, 82.0, 75.0, 80.0),
    TreatyErosionEntity("TE-004", "Turquie — OTAN & Droit Humanitaire", "Europe/MENA", "Réinterprétation Sélective des Obligations Traités", 65.0, 68.0, 70.0, 62.0),
    TreatyErosionEntity("TE-005", "Israël — CPI & Résolutions ONU", "MENA", "Non-Reconnaissance des Juridictions Internationales", 60.0, 72.0, 65.0, 55.0),
    TreatyErosionEntity("TE-006", "Brésil — Accord de Paris & Amazon", "Amériques", "Tension Souveraineté Nationale vs Engagements Climato", 45.0, 38.0, 40.0, 42.0),
    TreatyErosionEntity("TE-007", "Inde — Multilatéralisme Pragmatique", "Asie du Sud", "Engagement Sélectif selon les Intérêts Nationaux", 30.0, 28.0, 32.0, 25.0),
    TreatyErosionEntity("TE-008", "Union Européenne — Défenseur Multilatéral", "Europe", "Champion du Multilatéralisme & du Droit International", 12.0, 10.0, 15.0, 8.0),
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
        "domain": "treaty_erosion",
        "confidence_score": 0.85,
        "data_sources": ["un_treaty_registry", "icj_case_tracker", "multilateral_commitment_index"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_erosion_index": round(avg / 100 * 10, 2),
    }


def analyze_treaty_erosion() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Treaty Erosion Engine — {r['total_entities']} acteurs, avg érosion: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
