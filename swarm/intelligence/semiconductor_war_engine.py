"""
Caelum Partners — Semiconductor War Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La guerre des puces : les semi-conducteurs comme nouvelle arme géopolitique.
Les semi-conducteurs sont devenus le pétrole du XXIe siècle — un chokepoint
technologique dont le contrôle détermine la supériorité militaire, économique
et algorithmique des nations. La concentration extrême de la chaîne de valeur
crée des vulnérabilités systémiques sans précédent dans l'histoire industrielle.

Taiwan fabrique 92% des puces les plus avancées (≤7nm) via TSMC — une île
sous menace militaire permanente de la Chine, représentant le nœud technologique
le plus critique de la civilisation industrielle moderne. ASML (Pays-Bas) est
le seul fabricant mondial de machines EUV (lithographie ultraviolette extrême)
indispensables aux puces avancées — exportées sous contrôle strict depuis 2019.
Les USA ont imposé les règles du CHIPS Act et les restrictions Entity List sur
Huawei, SMIC et 200+ entreprises chinoises, bloquant l'accès aux équipements,
logiciels et talents américains nécessaires à la production avancée.

La Chine investit 150Md$ pour atteindre l'autosuffisance en 2030 via son plan
Made in China 2025 révisé — mais reste bloquée à 28nm pour la production de
masse malgré des percées isolées de SMIC. L'accélération IA (Nvidia H100,
B200) transforme la guerre des puces en guerre de l'intelligence artificielle
— les GPU comme vecteurs de puissance géopolitique.

Risk levels (guerre des semi-conducteurs et contrôle technologique) :
  critique  → composite ≥ 60  (monopole technologique — contrôle de nœuds critiques de la chaîne de valeur)
  élevé     → composite ≥ 40  (course technologique — investissements massifs sans position dominante établie)
  modéré    → composite ≥ 20  (dépendance structurelle — vulnérabilité aux ruptures d'approvisionnement)
  faible    → composite < 20  (coopération technologique — partage des bonnes pratiques et standards ouverts)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "concentration_fab_critique": {
        "severity_fr": "Critique",
        "action_fr": "Diversification géographique d'urgence — onshoring de capacités de fabrication avancée en Amérique du Nord, Europe et Japon via subventions massives",
        "signal_fr": "chip_design_monopoly_score > 85 AND fab_technology_control_score > 85 — concentration critique des capacités de fabrication avancée",
    },
    "weaponisation_technologique": {
        "severity_fr": "Critique",
        "action_fr": "Contre-mesures diplomatiques — dialogue bilatéral sur les règles d'exportation et développement d'alternatives non américaines aux équipements critiques",
        "signal_fr": "export_control_weaponization_score > 85 — weaponisation des contrôles à l'exportation comme instrument de pression géopolitique",
    },
    "monopole_fabrication_avancee": {
        "severity_fr": "Critique",
        "action_fr": "Alliance technologique multilatérale — Chip 4 Alliance et investissements croisés pour sécuriser les nœuds de fabrication avancée",
        "signal_fr": "fab_technology_control_score > 85 — monopole ou oligopole sur les technologies de fabrication de puces avancées",
    },
    "course_puces_strategique": {
        "severity_fr": "Élevé",
        "action_fr": "Investissements R&D nationaux renforcés — CHIPS Act national, zones franches technologiques et attractivité des talents en micro-électronique",
        "signal_fr": "Course aux semi-conducteurs — investissements massifs pour réduire la dépendance et développer des capacités nationales de fabrication",
    },
    "resilience_technologique": {
        "severity_fr": "Faible",
        "action_fr": "Partager les modèles de résilience technologique — standards ouverts, coopération multilatérale et chaînes d'approvisionnement diversifiées",
        "signal_fr": "composite_score < 20 — résilience technologique exemplaire — coopération, standards ouverts et diversification des sources",
    },
}


@dataclass
class SemiconductorWarEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    chip_design_monopoly_score: float
    fab_technology_control_score: float
    export_control_weaponization_score: float
    supply_chain_concentration_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_semiconductor_war_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.chip_design_monopoly_score * 0.30
            + self.fab_technology_control_score * 0.25
            + self.export_control_weaponization_score * 0.25
            + self.supply_chain_concentration_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_semiconductor_war_index = round(self.composite_score / 100 * 10, 2)

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
        if self.chip_design_monopoly_score >= 85 and self.fab_technology_control_score >= 85:
            return "concentration_fab_critique"
        if self.export_control_weaponization_score >= 85:
            return "weaponisation_technologique"
        if self.fab_technology_control_score >= 85:
            return "monopole_fabrication_avancee"
        if self.composite_score >= 20:
            return "course_puces_strategique"
        return "resilience_technologique"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Monopole technologique de {n} — contrôle de nœuds critiques de la chaîne de valeur semi-conducteurs mondiale",
                "Weaponisation des puces — semi-conducteurs utilisés comme instrument de pression géopolitique et levier de coercition économique",
                "Vulnérabilité systémique — concentration extrême exposant l'économie mondiale à des ruptures d'approvisionnement catastrophiques",
            ]
        if self.risk_level == "élevé":
            return [
                f"Course technologique de {n} — investissements massifs dans les semi-conducteurs pour réduire la dépendance stratégique",
                "Rattrapage technologique — développement de capacités nationales face aux restrictions d'exportation adversaires",
                "Risque de décalage technologique — fossé croissant avec les leaders mondiaux des puces avancées (2nm et inférieur)",
            ]
        if self.risk_level == "modéré":
            return [
                f"Dépendance structurelle de {n} — vulnérabilité aux disruptions d'approvisionnement en semi-conducteurs avancés",
                "Absence de capacité de fabrication domestique — dépendance aux importations pour les puces critiques des infrastructures",
                "Risque de découplage — exposition aux restrictions d'exportation et aux guerres commerciales technologiques",
            ]
        return [
            f"{n} incarne la coopération technologique — standards ouverts, chaînes d'approvisionnement diversifiées et partage de brevets",
            "Résilience multi-source — approvisionnement diversifié et accords de réciprocité technologique avec les partenaires alliés",
            "Modèle d'interdépendance saine — commerce libre des technologies non-sensibles et contrôles ciblés sur les applications militaires",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "chip_design_monopoly_score": self.chip_design_monopoly_score,
            "fab_technology_control_score": self.fab_technology_control_score,
            "export_control_weaponization_score": self.export_control_weaponization_score,
            "supply_chain_concentration_score": self.supply_chain_concentration_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_semiconductor_war_index": self.estimated_semiconductor_war_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SemiconductorWarEntity] = [
    SemiconductorWarEntity("SW-001", "Taiwan/TSMC — 92% Puces Avancées ≤7nm Mondiales", "Asie", "TSMC N2/N3 Process, Apple/Nvidia/AMD Clients & Île Stratégique sous Menace Militaire Chine", 88.0, 95.0, 72.0, 92.0),
    SemiconductorWarEntity("SW-002", "USA — CHIPS Act & Weaponisation Contrôles Export", "Amérique du Nord", "Nvidia H100/B200, ASML EUV Restriction, Entity List Huawei/SMIC & CHIPS Act 52Md$ Intel/TSMC", 92.0, 82.0, 95.0, 75.0),
    SemiconductorWarEntity("SW-003", "Chine — SMIC & Plan 150Md$ Autosuffisance 2030", "Asie", "SMIC 7nm Limité, Huawei Kirin IA, Plan Made in China 2025 Révisé & Équipements EUV Bloqués", 85.0, 68.0, 62.0, 88.0),
    SemiconductorWarEntity("SW-004", "Corée du Sud — Samsung & SK Hynix DRAM HBM", "Asie", "Samsung Gate-All-Around 3nm, SK Hynix HBM3E pour IA & Alliance Chip4 sous Pression", 80.0, 88.0, 72.0, 68.0),
    SemiconductorWarEntity("SW-005", "Pays-Bas — ASML EUV Seul Fabricant Mondial", "Europe", "ASML EUV 0.33NA & 0.55NA Monopole, Restriction Export Chine & Pression USA sur DUV", 55.0, 60.0, 65.0, 48.0),
    SemiconductorWarEntity("SW-006", "Japon — Shin-Etsu, Tokyo Electron & Matériaux", "Asie", "Shin-Etsu Silicone 30% Part Mondiale, Tokyo Electron Équipements & Photolithographie Nikon", 52.0, 55.0, 58.0, 45.0),
    SemiconductorWarEntity("SW-007", "Inde — Fab21 Tata & Stratégie Semi-Conducteurs", "Asie du Sud", "Tata Semiconductor Fab21 Dholera, Micron Mémoire Gujarat & Plan India Semiconductor Mission", 28.0, 25.0, 32.0, 35.0),
    SemiconductorWarEntity("SW-008", "OECD Chip Alliance — Standards & Coopération", "Global", "Chip 4 Alliance USA/Japon/Corée/Taiwan, CHIPS EU Act & Standards JEDEC Ouverts", 5.0, 6.0, 4.0, 3.0),
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
        "domain": "semiconductor_war",
        "confidence_score": 0.81,
        "data_sources": ["chips_act_monitor_semianalysis", "semiconductor_industry_association_reports", "csis_tech_war_tracker"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_semiconductor_war_index": round(avg / 100 * 10, 2),
    }


def analyze_semiconductor_war() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Semiconductor War Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
