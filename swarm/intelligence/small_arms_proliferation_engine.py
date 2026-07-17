"""
Caelum Partners — Small Arms Proliferation Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La prolifération des armes légères et de petit calibre (ALPC) comme
moteur primaire des conflits armés non-étatiques : contrairement aux
armes lourdes ou nucléaires, les ALPC sont les véritables armes de
destruction massive du quotidien. Bon marché, portables, durables,
elles alimentent les guerres civiles pendant des décennies après la fin
des conflits officiels.

Des Kalachnikovs du Sahel aux AR-15 de Haïti, des armes yougoslaves
inondant les Balkans aux surplus soviétiques arrosant l'Afrique, la
prolifération des ALPC crée des cycles de violence auto-entretenue où
les armes survivent aux conflits et alimentent les suivants. Le Traité
sur le Commerce des Armes (TCA) est systématiquement contourné. Les
flux illicites restent incontrôlables. Les groupes armés non-étatiques
se réarment en permanence. C'est la sécurité internationale à l'état pur.

Risk levels (prolifération ALPC et déstabilisation) :
  critique  → composite ≥ 60  (prolifération ALPC incontrôlable — insécurité systémique)
  élevé     → composite ≥ 40  (flux ALPC importants alimentant des conflits actifs)
  modéré    → composite ≥ 20  (risques de prolifération à surveiller)
  faible    → composite < 20  (contrôle ALPC efficace et marchés légaux régulés)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "proliferation_incontrôlable": {
        "severity_fr": "Critique",
        "action_fr": "Embargo total sur les armes et programme de désarmement-démobilisation-réintégration d'urgence",
        "signal_fr": "illicit_flow_score > 80 AND stockpile_leakage_score > 75 — prolifération ALPC incontrôlable",
    },
    "marche_gris_actif": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions sur les courtiers en armes et traçabilité obligatoire des transferts ALPC",
        "signal_fr": "Marché gris actif — transferts légaux détournés vers acteurs non-étatiques violents",
    },
    "flux_transfrontaliers": {
        "severity_fr": "Élevé",
        "action_fr": "Coopération régionale renforcée et contrôles frontaliers ciblés sur les corridors ALPC",
        "signal_fr": "Flux transfrontaliers significatifs — armes traversant les frontières alimentant les conflits voisins",
    },
    "risque_accumulation": {
        "severity_fr": "Modéré",
        "action_fr": "Programmes de collecte d'armes et renforcement des registres nationaux ALPC",
        "signal_fr": "Risque d'accumulation — stocks légaux mal sécurisés pouvant alimenter des marchés illicites",
    },
    "controle_efficace": {
        "severity_fr": "Faible",
        "action_fr": "Partage des meilleures pratiques de contrôle ALPC et soutien au Traité sur le Commerce des Armes",
        "signal_fr": "composite_score < 20 — contrôle ALPC efficace, registres à jour et transferts traçables",
    },
}


@dataclass
class SmallArmsProliferationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    illicit_flow_score: float
    stockpile_leakage_score: float
    non_state_actor_arming_score: float
    post_conflict_saturation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_arms_risk_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.illicit_flow_score * 0.30
            + self.stockpile_leakage_score * 0.25
            + self.non_state_actor_arming_score * 0.25
            + self.post_conflict_saturation_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_arms_risk_index = round(self.composite_score / 100 * 10, 2)

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
        if self.illicit_flow_score >= 80 and self.stockpile_leakage_score >= 75:
            return "proliferation_incontrôlable"
        if self.non_state_actor_arming_score >= 75:
            return "marche_gris_actif"
        if self.composite_score >= 40:
            return "flux_transfrontaliers"
        if self.composite_score >= 20:
            return "risque_accumulation"
        return "controle_efficace"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Prolifération ALPC incontrôlable dans {n} — flux illicites massifs alimentant violence et insécurité",
                "Armement des groupes non-étatiques — milices, gangs et groupes terroristes suréquipés en ALPC",
                "Saturation post-conflit — armes survivant aux conflits et recyclées dans de nouveaux cycles de violence",
            ]
        if self.risk_level == "élevé":
            return [
                f"Flux ALPC importants traversant {n} — corridors illicites alimentant les conflits régionaux",
                "Fuites de stocks étatiques — arsenaux mal sécurisés alimentant les marchés illicites locaux",
                "Acteurs non-étatiques armés — groupes criminels et paramilitaires en accès facilité aux ALPC",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risques de prolifération ALPC dans {n} — marchés légaux partiellement dérégulés",
                "Contrôle des stocks insuffisant — traçabilité limitée des armes légales pouvant être détournées",
                "Coopération régionale anti-ALPC insuffisante — corridors frontaliers sous-surveillés",
            ]
        return [
            f"{n} maintient un contrôle ALPC efficace — registres à jour et transferts traçables",
            "Cadre légal robuste sur les armes légères avec sanctions effectives contre les trafiquants",
            "Participation active au Traité sur le Commerce des Armes et partage de renseignements balistiques",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "illicit_flow_score": self.illicit_flow_score,
            "stockpile_leakage_score": self.stockpile_leakage_score,
            "non_state_actor_arming_score": self.non_state_actor_arming_score,
            "post_conflict_saturation_score": self.post_conflict_saturation_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_arms_risk_index": self.estimated_arms_risk_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SmallArmsProliferationEntity] = [
    SmallArmsProliferationEntity("SA-001", "Sahel — Zone de Saturation ALPC", "Afrique de l'Ouest", "Flux Libye-Mali-Niger-Burkina — Arsenaux Djihadistes", 92.0, 88.0, 90.0, 85.0),
    SmallArmsProliferationEntity("SA-002", "Haïti — Armes US Inondant les Gangs", "Amériques", "Trafic Floride-Haïti — Gangs Contrôlant Port-au-Prince", 85.0, 82.0, 92.0, 78.0),
    SmallArmsProliferationEntity("SA-003", "Yémen & Somalie — Arsenaux en Dérive", "MENA/Afrique de l'Est", "Blocus Contourné — Livraisons Maritimes Illicites d'ALPC", 88.0, 85.0, 82.0, 88.0),
    SmallArmsProliferationEntity("SA-004", "Balkans — Surplus Yougoslaves Persistants", "Europe du Sud-Est", "Armes des Guerres 90s Alimentant Crime Organisé Européen", 75.0, 80.0, 72.0, 90.0),
    SmallArmsProliferationEntity("SA-005", "Amérique Centrale — Armes US & Maras", "Amériques", "AR-15 & Pistolets US Alimentant Gangs Honduras-Guatemala-Salvador", 70.0, 65.0, 80.0, 68.0),
    SmallArmsProliferationEntity("SA-006", "Ukraine — Dispersion Post-Conflit", "Europe de l'Est", "ALPC Livrées par l'Ouest Risquant de Fuir vers Crime Organisé", 55.0, 62.0, 48.0, 70.0),
    SmallArmsProliferationEntity("SA-007", "Inde & Pakistan — Frontières Poreuses", "Asie du Sud", "Trafic ALPC aux Frontières — Alimentation Groupes Séparatistes", 42.0, 38.0, 45.0, 35.0),
    SmallArmsProliferationEntity("SA-008", "Japon & Australie — Contrôle Exemplaire", "Asie-Pacifique", "Registres Exhaustifs et Marchés Légaux Ultra-Régulés", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "small_arms",
        "confidence_score": 0.82,
        "data_sources": ["small_arms_survey_geneva", "un_register_conventional_arms", "interpol_illicit_arms_tracker"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_arms_risk_index": round(avg / 100 * 10, 2),
    }


def analyze_small_arms_proliferation() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Small Arms Proliferation Engine — {r['total_entities']} zones, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
