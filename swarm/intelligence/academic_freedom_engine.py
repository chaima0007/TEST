"""
Caelum Partners — Academic Freedom Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'érosion de la liberté académique comme indicateur de dérive autoritaire :
quand les universités deviennent des institutions d'endoctrinement, quand
les chercheurs s'autocensurent sous pression politique, quand les étudiants
sont surveillés et les professeurs licenciés pour leurs idées, c'est la
capacité d'innovation et de vérité d'une société qui s'effondre.

La liberté académique n'est pas un privilège des élites — c'est
l'infrastructure épistémique sans laquelle aucune société ne peut
se corriger, innover ou résister aux dérives du pouvoir. La répression
académique précède toujours l'autoritarisme complet : les régimes qui
brûlent les livres brûlent ensuite les gens.

Risk levels (intensité de la répression académique) :
  critique  → composite ≥ 60  (répression académique totale)
  élevé     → composite ≥ 40  (pression systémique sur les universités)
  modéré    → composite ≥ 20  (tensions sur l'indépendance académique)
  faible    → composite < 20  (liberté académique préservée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "repression_academique_totale": {
        "severity_fr": "Critique",
        "action_fr": "Corridors humanitaires pour académiques persécutés et sanctions contre les régimes répresseurs",
        "signal_fr": "political_censorship > 80 AND researcher_persecution > 75 — répression académique totale",
    },
    "controle_ideologique_universitaire": {
        "severity_fr": "Critique",
        "action_fr": "Soutien aux universités en exil et protection internationale des chercheurs menacés",
        "signal_fr": "Contrôle idéologique des universités — enseignement aligné sur la doctrine politique dominante",
    },
    "pression_systemique": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement de l'indépendance des institutions académiques et protection des lanceurs d'alerte",
        "signal_fr": "Pression systémique sur les académiques — autocensure généralisée et financements conditionnels",
    },
    "tensions_academiques": {
        "severity_fr": "Modéré",
        "action_fr": "Politiques de protection de l'indépendance académique et financement public non-conditionnel",
        "signal_fr": "Tensions sur l'indépendance académique — pressions politiques mais institutions résistantes",
    },
    "liberte_academique_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des protections légales et soutien aux universités dans d'autres pays sous pression",
        "signal_fr": "composite_score < 20 — liberté académique exemplaire, recherche indépendante garantie",
    },
}


@dataclass
class AcademicFreedomEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    political_censorship_score: float
    researcher_persecution_score: float
    brain_drain_severity_score: float
    institutional_autonomy_loss_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_repression_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.political_censorship_score * 0.30
            + self.researcher_persecution_score * 0.25
            + self.brain_drain_severity_score * 0.25
            + self.institutional_autonomy_loss_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_repression_index = round(self.composite_score / 100 * 10, 2)

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
        if self.political_censorship_score >= 80 and self.researcher_persecution_score >= 75:
            return "repression_academique_totale"
        if self.institutional_autonomy_loss_score >= 70:
            return "controle_ideologique_universitaire"
        if self.composite_score >= 45:
            return "pression_systemique"
        if self.composite_score >= 25:
            return "tensions_academiques"
        return "liberte_academique_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Répression académique totale dans {n} — chercheurs emprisonnés, universités sous contrôle étatique",
                "Censure politique systémique — thèmes de recherche interdits, auto-censure généralisée",
                "Fuite des cerveaux massive — talents académiques quittant le pays pour préserver leur liberté",
            ]
        if self.risk_level == "élevé":
            return [
                f"Pression systémique sur les académiques dans {n} — financements conditionnels et ingérence politique",
                "Autonomie institutionnelle érodée — gouvernance universitaire contrôlée par le politique",
                "Brain drain accéléré — chercheurs fuyant vers des environnements académiques libres",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tensions sur l'indépendance académique dans {n} — pressions politiques mais institutions résistantes",
                "Autocensure partielle — certains sujets difficiles à étudier sans risques professionnels",
                "Financement académique partiellement conditionné — risque d'orientation de la recherche",
            ]
        return [
            f"{n} préserve une liberté académique exemplaire — recherche indépendante garantie légalement",
            "Universités autonomes et chercheurs protégés — innovation intellectuelle florissante",
            "Modèle d'infrastructure épistémique à préserver et exporter pour soutenir la démocratie mondiale",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "political_censorship_score": self.political_censorship_score,
            "researcher_persecution_score": self.researcher_persecution_score,
            "brain_drain_severity_score": self.brain_drain_severity_score,
            "institutional_autonomy_loss_score": self.institutional_autonomy_loss_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_repression_index": self.estimated_repression_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[AcademicFreedomEntity] = [
    AcademicFreedomEntity("AF-001", "Chine — Universités Sous Contrôle CPC", "Asie", "Censure Politique Totale & Endoctrinement Xi Jinping", 95.0, 88.0, 85.0, 92.0),
    AcademicFreedomEntity("AF-002", "Russie — Académiques Emprisonnés & Exil", "Europe de l'Est", "Répression Post-2022 & Universités en Exil", 90.0, 92.0, 88.0, 85.0),
    AcademicFreedomEntity("AF-003", "Iran — Sciences sous Révolution Islamique", "MENA", "Purge des Chercheurs & Contrôle Idéologique Total", 88.0, 85.0, 82.0, 88.0),
    AcademicFreedomEntity("AF-004", "Turquie — Purges Post-Coup 2016", "Europe/MENA", "5000 Académiques Licenciés & Universités Fermées", 80.0, 78.0, 75.0, 80.0),
    AcademicFreedomEntity("AF-005", "Hongrie — Capture Académique Orban", "Europe", "CEU Expulsée & Contrôle Politique des Universités", 65.0, 60.0, 55.0, 70.0),
    AcademicFreedomEntity("AF-006", "USA — Campus Wars & Financement Conditionnel", "Amérique du Nord", "Pressions Politiques des Deux Bords & Autocensure", 42.0, 28.0, 22.0, 38.0),
    AcademicFreedomEntity("AF-007", "France & Allemagne — Tensions Académiques", "Europe", "Pression sur les Études Postcoloniales & Genre", 25.0, 12.0, 18.0, 22.0),
    AcademicFreedomEntity("AF-008", "Pays Nordiques & Suisse — Modèles Académiques", "Europe du Nord", "Liberté Académique Constitutionnelle & Financement Public", 5.0, 3.0, 8.0, 4.0),
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
        "domain": "academic_freedom",
        "confidence_score": 0.87,
        "data_sources": ["scholars_at_risk_network", "academic_freedom_index", "university_world_news_tracker"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_repression_index": round(avg / 100 * 10, 2),
    }


def analyze_academic_freedom() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Academic Freedom Engine — {r['total_entities']} zones, avg répression: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
