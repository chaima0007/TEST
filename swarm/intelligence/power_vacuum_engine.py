"""
Caelum Partners — Power Vacuum Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Les crises de succession dans les régimes autoritaires et les vides de pouvoir
géopolitiques : quand un dictateur meurt, quand un empire recule, quand une
puissance hégémonique se retire, le vide créé devient le théâtre des guerres
par procuration, des coups d'État et des fragmentations territoriales.

Le vide de pouvoir n'est pas l'absence de pouvoir — c'est la compétition
chaotique entre multiples acteurs pour remplir l'espace laissé vacant.
De la succession de Kim Jong-un à la retraite américaine du Moyen-Orient,
en passant par la décomposition post-soviétique, les vides de puissance
sont les incubateurs des crises géopolitiques de la prochaine décennie.

Risk levels (intensité du vide de pouvoir géopolitique) :
  critique  → composite ≥ 60  (vide de pouvoir catastrophique)
  élevé     → composite ≥ 40  (instabilité de succession sévère)
  modéré    → composite ≥ 20  (transition de pouvoir fragile)
  faible    → composite < 20  (succession institutionnalisée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "vide_catastrophique": {
        "severity_fr": "Critique",
        "action_fr": "Engagement diplomatique d'urgence — médiation internationale et stabilisation par forces multilatérales",
        "signal_fr": "succession_crisis_score > 80 AND institutional_vacuum > 75 — vide de pouvoir catastrophique",
    },
    "guerre_succession": {
        "severity_fr": "Critique",
        "action_fr": "Soutien aux institutions légitimes et prévention des guerres par procuration régionales",
        "signal_fr": "Guerre de succession en cours — factions rivales se disputant le pouvoir dans le vide",
    },
    "competition_hegemonique": {
        "severity_fr": "Élevé",
        "action_fr": "Diplomatie préventive et construction de cadres régionaux de sécurité collective",
        "signal_fr": "Compétition hégémonique — grandes puissances comblant le vide laissé par la puissance sortante",
    },
    "transition_fragile": {
        "severity_fr": "Modéré",
        "action_fr": "Accompagnement de la transition et renforcement des institutions pour éviter la dérive autoritaire",
        "signal_fr": "Transition de pouvoir fragile — succession incertaine mais institutions partiellement stables",
    },
    "succession_institutionnalisee": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des institutions démocratiques et des mécanismes de transfert pacifique du pouvoir",
        "signal_fr": "composite_score < 20 — succession institutionnalisée, transfert de pouvoir pacifique garanti",
    },
}


@dataclass
class PowerVacuumEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    succession_crisis_score: float
    institutional_vacuum_score: float
    proxy_war_attraction_score: float
    regional_destabilization_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_vacuum_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.succession_crisis_score * 0.30
            + self.institutional_vacuum_score * 0.25
            + self.proxy_war_attraction_score * 0.25
            + self.regional_destabilization_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_vacuum_index = round(self.composite_score / 100 * 10, 2)

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
        if self.succession_crisis_score >= 80 and self.institutional_vacuum_score >= 75:
            return "vide_catastrophique"
        if self.proxy_war_attraction_score >= 70:
            return "guerre_succession"
        if self.composite_score >= 45:
            return "competition_hegemonique"
        if self.composite_score >= 25:
            return "transition_fragile"
        return "succession_institutionnalisee"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Vide de pouvoir catastrophique dans {n} — compétition chaotique entre factions armées",
                "Guerre par procuration imminente — puissances régionales et mondiales mobilisant leurs alliés",
                "Effondrement institutionnel total — aucun mécanisme de succession légitime opérationnel",
            ]
        if self.risk_level == "élevé":
            return [
                f"Instabilité de succession sévère dans {n} — factions rivales sans arbitre institutionnel",
                "Attraction pour les guerres par procuration — acteurs extérieurs mobilisant des proxies internes",
                "Déstabilisation régionale en cours — le vide débordant au-delà des frontières nationales",
            ]
        if self.risk_level == "modéré":
            return [
                f"Transition de pouvoir fragile dans {n} — succession incertaine mais conflit armé évité",
                "Institutions partiellement fonctionnelles — cadre de succession existant mais sous pression",
                "Risque de compétition hégémonique externe si la transition s'enlise",
            ]
        return [
            f"{n} maintient une succession institutionnalisée — transfert de pouvoir pacifique garanti",
            "Institutions démocratiques solides absorbant les transitions politiques sans violence",
            "Modèle de gouvernance à fort capital institutionnel — résistant aux crises de succession",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "succession_crisis_score": self.succession_crisis_score,
            "institutional_vacuum_score": self.institutional_vacuum_score,
            "proxy_war_attraction_score": self.proxy_war_attraction_score,
            "regional_destabilization_score": self.regional_destabilization_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_vacuum_index": self.estimated_vacuum_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[PowerVacuumEntity] = [
    PowerVacuumEntity("PV-001", "Corée du Nord — Succession Kim", "Asie du Nord-Est", "Succession Dynastique & Arsenal Nucléaire", 95.0, 92.0, 90.0, 88.0),
    PowerVacuumEntity("PV-002", "Syrie — Post-Conflit & Fragmentation", "MENA", "Vide Hégémonique & Zones de Contrôle Multiples", 88.0, 85.0, 92.0, 82.0),
    PowerVacuumEntity("PV-003", "Sahel — Effritement Souveraineté Étatique", "Afrique", "Coups d'État en Cascade & Retrait Français", 82.0, 88.0, 85.0, 80.0),
    PowerVacuumEntity("PV-004", "Libye — Dualisme Étatique Permanent", "Afrique du Nord", "Deux Gouvernements & Proxies Étrangers Multiples", 80.0, 85.0, 88.0, 75.0),
    PowerVacuumEntity("PV-005", "Venezuela — Pouvoir Contesté", "Amériques", "Légitimité Duale & Compétition USA/Russie/Chine", 68.0, 65.0, 72.0, 60.0),
    PowerVacuumEntity("PV-006", "Irak — Souveraineté Fragmentée", "MENA", "État Faible entre Iran, USA & Milices Armées", 62.0, 68.0, 65.0, 58.0),
    PowerVacuumEntity("PV-007", "Bolivie & Nicaragua — Démocratie Érodée", "Amériques", "Dérive Autoritaire & Institutions Fragilisées", 38.0, 35.0, 30.0, 32.0),
    PowerVacuumEntity("PV-008", "Suède & Canada — Démocraties Résilientes", "Europe/Amériques", "Succession Institutionnelle Exemplaire", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "power_vacuum",
        "confidence_score": 0.79,
        "data_sources": ["fragile_states_index", "succession_crisis_tracker", "proxy_conflict_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_vacuum_index": round(avg / 100 * 10, 2),
    }


def analyze_power_vacuum() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Power Vacuum Engine — {r['total_entities']} zones, avg vide: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
