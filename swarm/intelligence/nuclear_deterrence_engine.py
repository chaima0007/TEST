"""
Caelum Partners — Nuclear Deterrence Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La dissuasion nucléaire : équilibre de la terreur ou course vers l'abîme ?
Les neuf États nucléaires mondiaux détiennent environ 12 500 ogives — une
capacité de destruction civilisationnelle maintenue comme instrument de
politique étrangère. La doctrine de la destruction mutuelle assurée (MAD)
a jusqu'ici prévenu une guerre nucléaire, mais l'érosion des traités de
contrôle des armements, la modernisation des arsenaux et la multiplication
des vecteurs hypersoniques réduisent dangereusement les seuils d'emploi.

La Russie modernise ses missiles Sarmat (RS-28), déploie des torpilles
Poseidon et maintient la doctrine Perimeter (Dead Hand) pour une riposte
automatisée. Les USA investissent 1 700Md$ sur 30 ans pour moderniser
la triade nucléaire (B21-Raider, Sentinel ICBM, Columbia SSBN). La Chine
quintuple son arsenal pour atteindre 1 000 ogives d'ici 2030 selon le
Pentagone. La RPDC a testé des missiles ICBM capables d'atteindre la côte
Est américaine. Le retrait du traité INF, la suspension de New START par
Moscou et l'absence de l'Inde/Pakistan/Israël du TNP fragilisent l'architecture
globale de non-prolifération.

Risk levels (dissuasion nucléaire et prolifération) :
  critique  → composite ≥ 60  (dissuasion offensive — arsenaux modernisés, doctrines escalatoires)
  élevé     → composite ≥ 40  (course armements nucléaires — accumulation sans régime vérification)
  modéré    → composite ≥ 20  (ambiguïté nucléaire — programme potentiel et incertitude stratégique)
  faible    → composite < 20  (désarmement coopératif — traités de vérification et transparence)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "dissuasion_nucleaire_offensive": {
        "severity_fr": "Critique",
        "action_fr": "Réactivation des négociations de contrôle des armements — New START successor, dialogue P5 sur les doctrines nucléaires et transparence des arsenaux",
        "signal_fr": "nuclear_arsenal_modernization_score > 85 AND second_strike_capability_score > 85 — dissuasion nucléaire offensive intégrée",
    },
    "proliferation_clandestine": {
        "severity_fr": "Critique",
        "action_fr": "Renforcement du régime de vérification AIEA — protocole additionnel obligatoire et sanctions ciblées contre les États proliférants",
        "signal_fr": "npt_violation_risk_score > 85 — programme nucléaire clandestin en violation du Traité sur la Non-Prolifération",
    },
    "modernisation_arsenal_strategique": {
        "severity_fr": "Critique",
        "action_fr": "Dialogue stratégique d'urgence — mécanismes de déconfliction et limitation des vecteurs hypersoniques dans les négociations bilatérales",
        "signal_fr": "nuclear_doctrine_escalation_score > 85 — doctrine d'escalade nucléaire avec abaissement des seuils d'emploi",
    },
    "course_armements_nucleaires": {
        "severity_fr": "Élevé",
        "action_fr": "Réengagement dans les traités multilatéraux — TIAN, CTBT et négociations régionales de dénucléarisation sous égide ONU",
        "signal_fr": "Accumulation d'arsenaux nucléaires sans mécanismes de vérification internationale — risque d'escalade régionale",
    },
    "desarmement_cooperatif": {
        "severity_fr": "Faible",
        "action_fr": "Amplifier les modèles de désarmement vérifiable — partager les bonnes pratiques de transparence nucléaire et renforcer le TNP",
        "signal_fr": "composite_score < 20 — engagement actif dans le désarmement nucléaire vérifiable et la non-prolifération coopérative",
    },
}


@dataclass
class NuclearDeterrenceEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    nuclear_arsenal_modernization_score: float
    second_strike_capability_score: float
    nuclear_doctrine_escalation_score: float
    npt_violation_risk_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_nuclear_deterrence_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.nuclear_arsenal_modernization_score * 0.30
            + self.second_strike_capability_score * 0.25
            + self.nuclear_doctrine_escalation_score * 0.25
            + self.npt_violation_risk_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_nuclear_deterrence_index = round(self.composite_score / 100 * 10, 2)

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
        if self.nuclear_arsenal_modernization_score >= 85 and self.second_strike_capability_score >= 85:
            return "dissuasion_nucleaire_offensive"
        if self.npt_violation_risk_score >= 85:
            return "proliferation_clandestine"
        if self.nuclear_doctrine_escalation_score >= 85:
            return "modernisation_arsenal_strategique"
        if self.composite_score >= 20:
            return "course_armements_nucleaires"
        return "desarmement_cooperatif"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Dissuasion nucléaire offensive de {n} — modernisation arsenaux, postures de première frappe et réduction des seuils d'emploi",
                "Course aux armements nucléaires — missiles hypersoniques, MIRV et miniaturisation des charges nucléaires tactiques",
                "Érosion du droit international nucléaire — remise en cause des traités de contrôle des armements et suspension des vérifications AIEA",
            ]
        if self.risk_level == "élevé":
            return [
                f"Prolifération nucléaire régionale par {n} — accumulation d'arsenaux non soumis aux régimes de vérification internationale",
                "Instabilité stratégique — doctrines d'emploi en premier et tensions bilatérales accroissant le risque de guerre nucléaire accidentelle",
                "Zones de crise à risque nucléaire — théâtres d'opérations où l'escalade nucléaire n'est pas exclue comme option militaire",
            ]
        if self.risk_level == "modéré":
            return [
                f"Ambiguïté nucléaire de {n} — programme potentiel maintenant une incertitude stratégique délibérée",
                "Dépendance aux garanties de sécurité étendues — couverture nucléaire d'alliés créant des vulnérabilités structurelles",
                "Capacités balistiques duales — vecteurs pouvant emporter des charges conventionnelles ou nucléaires selon les circonstances",
            ]
        return [
            f"{n} incarne le désarmement coopératif — traités de vérification, transparence des arsenaux et dialogue multilatéral",
            "Réduction vérifiable des arsenaux — mécanismes d'inspection réciproque et démantèlement documenté des ogives",
            "Modèle de non-prolifération à universaliser — adhésion au CTBT, TNP renforcé et zones dénucléarisées régionales",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "nuclear_arsenal_modernization_score": self.nuclear_arsenal_modernization_score,
            "second_strike_capability_score": self.second_strike_capability_score,
            "nuclear_doctrine_escalation_score": self.nuclear_doctrine_escalation_score,
            "npt_violation_risk_score": self.npt_violation_risk_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_nuclear_deterrence_index": self.estimated_nuclear_deterrence_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[NuclearDeterrenceEntity] = [
    NuclearDeterrenceEntity("ND-001", "Russie — Sarmat, Poseidon & Doctrine Perimeter", "Europe de l'Est", "RS-28 Sarmat, Torpille Poseidon, Avangard Hypersonique & Dead Hand Auto-Riposte", 90.0, 88.0, 92.0, 85.0),
    NuclearDeterrenceEntity("ND-002", "USA — Triade Nucléaire & 1700Md$ Modernisation", "Amérique du Nord", "B21-Raider, Sentinel ICBM, Columbia SSBN & Bombes B61-12 OTAN Modernisées", 85.0, 92.0, 78.0, 75.0),
    NuclearDeterrenceEntity("ND-003", "RPDC — ICBM Hwasong & Arsenal Clandestin", "Asie", "Hwasong-17 ICBM, Ogives Miniaturisées & Sous-Marins Nucléaires SINPO en Développement", 62.0, 55.0, 95.0, 90.0),
    NuclearDeterrenceEntity("ND-004", "Chine — Triple Arsenal 1000 Ogives 2030", "Asie", "DF-41 ICBM, JL-3 SLBM, H-20 Bombardier Furtif & Silos Wyoming Stratégie", 78.0, 72.0, 75.0, 80.0),
    NuclearDeterrenceEntity("ND-005", "Pakistan — TNW Tactiques & Doctrine Première Frappe", "Asie du Sud", "Nasr TNW Tactique, Babur ALCM & Doctrine Emploi en Premier contre Supériorité Conventionnelle", 65.0, 58.0, 68.0, 72.0),
    NuclearDeterrenceEntity("ND-006", "Inde — Triade & No First Use sous Révision", "Asie du Sud", "Agni-V ICBM, INS Arihant SSBN & Révision Doctrine No First Use sous Modi", 62.0, 60.0, 65.0, 55.0),
    NuclearDeterrenceEntity("ND-007", "Iran — Seuil Nucléaire & Uranium 60% Enrichi", "MENA", "Enrichissement 60% Fordow, Centrifugeuses IR-6 & Breakout Time Estimé <2 Semaines AIEA", 35.0, 30.0, 42.0, 52.0),
    NuclearDeterrenceEntity("ND-008", "AIEA & Traité NPT — Vérification Multilatérale", "Global", "Protocole Additionnel AIEA, NPT 191 États Parties & CTBT 186 Signataires", 5.0, 4.0, 3.0, 2.0),
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
        "domain": "nuclear_deterrence",
        "confidence_score": 0.78,
        "data_sources": ["sipri_nuclear_forces_database", "arms_control_association_npt_monitor", "bulletin_atomic_scientists_doomsday_clock"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_nuclear_deterrence_index": round(avg / 100 * 10, 2),
    }


def analyze_nuclear_deterrence() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Nuclear Deterrence Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
