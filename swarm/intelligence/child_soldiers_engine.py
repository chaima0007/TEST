"""
Caelum Partners — Child Soldiers Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Enfants soldats : le recrutement forcé d'enfants comme arme de guerre systémique.
Le recrutement d'enfants soldats constitue l'un des crimes de guerre les plus
documentés et les moins poursuivis de l'histoire contemporaine. La Convention
relative aux droits de l'enfant (CRC, 1989) et ses protocoles optionnels
interdisent formellement le recrutement de toute personne de moins de 18 ans
dans les forces armées, mais des dizaines de groupes armés et plusieurs États
violent systématiquement ces normes.

La Lord's Resistance Army (LRA) d'Ouganda a recruté de force plus de 30 000
enfants depuis 1987, les contraignant à commettre des atrocités contre leurs
propres familles pour briser tout lien communautaire — une stratégie de
conditionnement psychologique documentée par Human Rights Watch et l'ONU.
Joseph Kony est sous mandat d'arrêt de la CPI depuis 2005.

Au Myanmar, la Tatmadaw (armée nationale) est listée par le Secrétaire général
de l'ONU comme recruteur systématique d'enfants soldats depuis 2002. En 2021,
malgré ses engagements formels, l'armée birmane a intensifié le recrutement
dans le contexte du coup d'État. Les groupes armés Houthis au Yémen ont recruté
plus de 3 500 enfants depuis 2014 selon l'UNICEF, dont des enfants de moins
de 10 ans déployés comme guetteurs et porteurs de munitions.

Risk levels (recrutement d'enfants soldats et militarisation des mineurs) :
  critique  -> composite >= 60  (recrutement systémique — enfants utilisés comme combattants réguliers)
  élevé     -> composite >= 40  (exploitation active — groupes armés recrutant des mineurs)
  modéré    -> composite >= 20  (risque résiduel — incidents documentés sans institutionnalisation)
  faible    -> composite < 20   (protection exemplaire — respect effectif des protocoles CRC)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "recrutement_force_enfants": {
        "severity_fr": "Critique",
        "action_fr": "Mandats CPI immédiats — poursuites des commandants recruteurs, libération forcée via mécanismes ONU et programme DDR renforcé avec soutien psychosocial",
        "signal_fr": "forced_child_recruitment_score > 85 — recrutement forcé massif d'enfants par enlèvement, coercition ou enrôlement direct, crime de guerre selon le Statut de Rome",
    },
    "enfants_soldats_combattants": {
        "severity_fr": "Critique",
        "action_fr": "Opérations libération — missions spéciales pour libération des enfants combattants, conditionnalité aide États complices et liste noire ONU",
        "signal_fr": "child_combat_deployment_score > 85 — enfants déployés activement comme combattants dans des opérations militaires avec formation aux armes",
    },
    "militarisation_enfants_proxy": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions ciblées États sponsors — gel avoirs officiers commandants, embargo armes et mécanisme vérification âge pour transferts d'armes",
        "signal_fr": "state_armed_group_complicity_score > 85 — complicité étatique dans recrutement d'enfants par groupes armés proxies financés ou entraînés par des États",
    },
    "exploitation_enfants_guerre": {
        "severity_fr": "Élevé",
        "action_fr": "Engagement conditionnel — suspension aide militaire aux États listés ONU, renforcement capacités judiciaires et programmes accès à l'éducation",
        "signal_fr": "Exploitation d'enfants dans les conflits — utilisation de mineurs comme porteurs, guetteurs ou boucliers sans déploiement direct comme combattants",
    },
    "protection_enfants_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter standards protection — financement UNICEF, transfert Principes Paris aux États vulnérables et aide aux programmes de démobilisation",
        "signal_fr": "composite_score < 20 — respect effectif des conventions CRC et Principes de Paris sur les enfants associés aux forces armées",
    },
}


@dataclass
class ChildSoldiersEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    forced_child_recruitment_score: float
    child_combat_deployment_score: float
    state_armed_group_complicity_score: float
    child_soldier_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_child_soldiers_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.forced_child_recruitment_score * 0.30
            + self.child_combat_deployment_score * 0.25
            + self.state_armed_group_complicity_score * 0.25
            + self.child_soldier_impunity_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_child_soldiers_index = round(self.composite_score / 100 * 10, 2)

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
        if self.forced_child_recruitment_score >= 85:
            return "recrutement_force_enfants"
        if self.child_combat_deployment_score >= 85:
            return "enfants_soldats_combattants"
        if self.state_armed_group_complicity_score >= 85:
            return "militarisation_enfants_proxy"
        if self.composite_score >= 20:
            return "exploitation_enfants_guerre"
        return "protection_enfants_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Recrutement d'enfants soldats critique de {n} — enfants enrôlés de force, contraints à combattre ou utilisés comme boucliers humains dans des violations graves du droit international humanitaire",
                "Crime de guerre documenté — le recrutement d'enfants de moins de 15 ans constitue un crime de guerre selon le Statut de Rome, avec responsabilité pénale individuelle des commandants",
                "Trauma générationnel irréversible — les enfants soldats subissent des traumatismes psychologiques profonds et une exclusion sociale à vie compromettant leur réintégration",
            ]
        if self.risk_level == "élevé":
            return [
                f"Exploitation d'enfants dans les conflits de {n} — utilisation de mineurs dans des rôles de soutien militaire avec risques d'escalade vers des rôles combattants directs",
                "Impunité des recruteurs — l'absence de poursuites judiciaires crée un effet d'aubaine pour les groupes armés ciblant les enfants des communautés vulnérables",
                "Fragilité post-conflit — les enfants associés aux forces armées rencontrent des obstacles majeurs à la démobilisation, réhabilitation et réintégration communautaire",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque résiduel enfants soldats de {n} — incidents isolés sans stratégie active de recrutement institutionnalisée par les forces étatiques ou groupes armés",
                "Vulnérabilités structurelles — pauvreté, déplacement interne et absence de perspectives économiques rendent les enfants vulnérables au recrutement",
                "Progrès fragiles — les acquis de la démobilisation peuvent être inversés par la résurgence de conflits ou la prolifération d'armes légères",
            ]
        return [
            f"{n} incarne la protection exemplaire des enfants dans les conflits — respect effectif des Protocoles facultatifs à la CRC et mécanismes de vérification de l'âge",
            "Standards de Paris appliqués — programme DDR opérationnel avec soutien psychosocial et accès à l'éducation garantis aux anciens enfants soldats",
            "Modèle de protection à exporter — financement UNICEF, formation des forces armées aux obligations CRC et coopération avec les mécanismes ONU",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "forced_child_recruitment_score": self.forced_child_recruitment_score,
            "child_combat_deployment_score": self.child_combat_deployment_score,
            "state_armed_group_complicity_score": self.state_armed_group_complicity_score,
            "child_soldier_impunity_score": self.child_soldier_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_child_soldiers_index": self.estimated_child_soldiers_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[ChildSoldiersEntity] = [
    ChildSoldiersEntity("CS-001", "LRA/Ouganda — Lord's Resistance Army & Enfants Otages Kony", "Afrique Centrale", "30 000+ Enfants Recrutés Force, Atrocités Imposées, CPI Mandat Kony 2005 & Financement Réseaux Criminels", 92.0, 90.0, 85.0, 88.0),
    ChildSoldiersEntity("CS-002", "Myanmar/Tatmadaw — Armée Birmane & Coup d'État 2021", "Asie du Sud-Est", "Listée ONU Recruteurs 2002, 7000+ Enfants Tatmadaw, Coup État 2021 Intensification & Groupes Ethniques Armés", 83.0, 90.0, 82.0, 80.0),
    ChildSoldiersEntity("CS-003", "Houthis/Yémen — 3500+ Enfants Soldats & Iran Proxy", "MENA", "3500+ Enfants UNICEF 2023, Enfants <10 Ans Guetteurs, Iran Formation & Financement & ONU Liste Noire Persistante", 80.0, 75.0, 90.0, 82.0),
    ChildSoldiersEntity("CS-004", "RDC/ADF/M23 — Congo Est & Multiples Groupes Armés", "Afrique Centrale", "M23 Recrutement Force, ADF Enfants Boucliers, FARDC Implication Documentée & 15 000 Enfants Libérés 2023", 78.0, 82.0, 80.0, 88.0),
    ChildSoldiersEntity("CS-005", "Nigéria/Boko Haram — ISWAP & Filles de Chibok Soldates", "Afrique de l'Ouest", "Boko Haram Filles Soldates, ISWAP Kamikazes Enfants, Nord-Est 2200+ Enfants & Impunité Locale Élevée", 55.0, 52.0, 58.0, 62.0),
    ChildSoldiersEntity("CS-006", "Somalie/Al-Shabaab — Recrutement Écoles & Camps Réfugiés", "Afrique de l'Est", "Al-Shabaab Recrutement Madrassas, 7000+ Enfants Documentés, Camps Dadaab Ciblés & Mogadiscio Attaques", 52.0, 48.0, 55.0, 58.0),
    ChildSoldiersEntity("CS-007", "Colombie/FARC Résiduels — Dissidences & Mineurs Vulnérables", "Amérique du Sud", "FARC Dissidences Post-Accord 2016, ELN Recrutement Indigènes, 30% Recrues Mineurs Estimés", 28.0, 25.0, 32.0, 35.0),
    ChildSoldiersEntity("CS-008", "UNICEF/Principes Paris — Protection Internationale Enfants", "Global", "Protocoles Facultatifs CRC 2000, Principes Paris 2007, Mécanismes Surveillance ONU & DDR 58 Pays", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "child_soldiers",
        "confidence_score": 0.83,
        "data_sources": ["unicef_children_armed_conflict_report", "un_secretary_general_children_war_annex", "child_soldiers_international_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_child_soldiers_index": round(avg / 100 * 10, 2),
    }


def analyze_child_soldiers() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Child Soldiers Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
