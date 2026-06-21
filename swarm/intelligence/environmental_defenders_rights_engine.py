"""
Caelum Partners — Environmental Defenders Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Droits des défenseurs de l'environnement — militants écologiques tués/emprisonnés,
poursuites SLAPP, criminalisation de la protection environnementale.

Les défenseurs de l'environnement font face à une violence croissante dans le monde :
meurtres, menaces, poursuites judiciaires abusives (SLAPP), arrestations arbitraires.
Selon Global Witness, plus de 1 700 défenseurs ont été tués entre 2012 et 2022, dont
une majorité de défenseurs autochtones protégeant leurs terres contre l'extractivisme.

La collusion entre entreprises extractives (minières, agro-industrielles, pétrolières)
et États complices crée un système où les défenseurs sont criminalisés pour avoir protégé
des forêts, des fleuves et des territoires. L'impunité des assassins reste quasi-totale,
atteignant 97% dans des pays comme la Colombie. Les poursuites SLAPP (Strategic Lawsuits
Against Public Participation) épuisent financièrement les militants et réduisent au silence
les communautés qui résistent au pillage de leurs ressources naturelles.

Risk levels (meurtres défenseurs, criminalisation, collusion état-entreprises) :
  critique  -> composite >= 60  (meurtres systémiques — impunité totale, collusion active)
  élevé     -> composite >= 40  (répression active — poursuites, menaces, corruption locale)
  modéré    -> composite >= 20  (criminalisation partielle — lois restrictives, pression judiciaire)
  faible    -> composite < 20   (cadre protecteur — jurisprudence favorable, société civile forte)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class EnvironmentalDefendersRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    environmental_defender_killings_impunity_score: float
    criminalization_protest_slapp_score: float
    state_corporate_collusion_repression_score: float
    legal_protection_whistleblower_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_environmental_defenders_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.environmental_defender_killings_impunity_score * 0.30
            + self.criminalization_protest_slapp_score * 0.25
            + self.state_corporate_collusion_repression_score * 0.25
            + self.legal_protection_whistleblower_gap_score * 0.20,
            2,
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_environmental_defenders_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "environmental_defender_killings_impunity_score": self.environmental_defender_killings_impunity_score,
            "criminalization_protest_slapp_score": self.criminalization_protest_slapp_score,
            "state_corporate_collusion_repression_score": self.state_corporate_collusion_repression_score,
            "legal_protection_whistleblower_gap_score": self.legal_protection_whistleblower_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_environmental_defenders_rights_index": self.estimated_environmental_defenders_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class EnvironmentalDefendersRightsEngineResult:
    agent: str = "Environmental Defenders Rights Engine Agent"
    domain: str = "environmental_defenders_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_environmental_defenders_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EnvironmentalDefendersRightsEntity] = field(default_factory=list)


def run_environmental_defenders_rights_engine() -> EnvironmentalDefendersRightsEngineResult:
    entities = [
        EnvironmentalDefendersRightsEntity(
            entity_id="EDR-001",
            name="Honduras — Berta Cáceres Assassinée, 14 Défenseurs Tués/An, Nexus DESA Corporation-État",
            country="Honduras",
            sector="Défense Fleuves & Terres Autochtones",
            environmental_defender_killings_impunity_score=96.0,
            criminalization_protest_slapp_score=93.0,
            state_corporate_collusion_repression_score=94.0,
            legal_protection_whistleblower_gap_score=91.0,
            primary_pattern="environmental_defender_killings_impunity",
            key_signals=[
                "Berta Cáceres assassinée 2016 par employés DESA",
                "14 défenseurs tués/an en moyenne",
                "Collusion directe état-entreprise documentée",
                "Impunité quasi-totale des commanditaires",
            ],
        ),
        EnvironmentalDefendersRightsEntity(
            entity_id="EDR-002",
            name="Philippines — 166 Défenseurs Tués 2016-2022, Lois Anti-Activistes Duterte, Red-Tagging",
            country="Philippines",
            sector="Défense Forêts & Mines",
            environmental_defender_killings_impunity_score=91.0,
            criminalization_protest_slapp_score=88.0,
            state_corporate_collusion_repression_score=89.0,
            legal_protection_whistleblower_gap_score=86.0,
            primary_pattern="state_corporate_collusion_repression",
            key_signals=[
                "166 défenseurs tués 2016-2022",
                "Red-tagging système de désignation terroriste",
                "Loi anti-terrorisme 2020 utilisée contre activistes",
                "Peuples Lumad déplacés pour mines de nickel",
            ],
        ),
        EnvironmentalDefendersRightsEntity(
            entity_id="EDR-003",
            name="Brésil/Amazonie — 342 Défenseurs Tués 2012-2022, Garimpeiros & Peuples Autochtones",
            country="Brésil",
            sector="Défense Amazonie & Peuples Autochtones",
            environmental_defender_killings_impunity_score=86.0,
            criminalization_protest_slapp_score=83.0,
            state_corporate_collusion_repression_score=84.0,
            legal_protection_whistleblower_gap_score=81.0,
            primary_pattern="environmental_defender_killings_impunity",
            key_signals=[
                "342 défenseurs tués 2012-2022",
                "Dom Phillips et Bruno Pereira assassinés 2022",
                "Garimpeiros armés menacent peuples Yanomami",
                "Démantèlement FUNAI sous Bolsonaro",
            ],
        ),
        EnvironmentalDefendersRightsEntity(
            entity_id="EDR-004",
            name="Colombie — 65+ Défenseurs Tués/An, Dissidents FARC Ciblent Militants, Impunité 97%",
            country="Colombie",
            sector="Défense Terres & Environnement Post-Conflit",
            environmental_defender_killings_impunity_score=81.0,
            criminalization_protest_slapp_score=78.0,
            state_corporate_collusion_repression_score=79.0,
            legal_protection_whistleblower_gap_score=76.0,
            primary_pattern="environmental_defender_killings_impunity",
            key_signals=[
                "65+ défenseurs tués/an — record mondial",
                "Impunité 97% pour meurtres défenseurs",
                "Dissidents FARC ciblent leaders communautaires",
                "Accords de paix non mis en oeuvre zones rurales",
            ],
        ),
        EnvironmentalDefendersRightsEntity(
            entity_id="EDR-005",
            name="Mexique — Mineurs Illégaux Menacent Communautés, 54 Meurtres 2022, Corruption Locale",
            country="Mexique",
            sector="Défense Eau & Terres vs Extractivisme",
            environmental_defender_killings_impunity_score=60.0,
            criminalization_protest_slapp_score=57.0,
            state_corporate_collusion_repression_score=58.0,
            legal_protection_whistleblower_gap_score=55.0,
            primary_pattern="state_corporate_collusion_repression",
            key_signals=[
                "54 défenseurs tués en 2022",
                "Cartels protègent intérêts miniers illégaux",
                "Comunidades nahua et maya criminalisées",
                "Mécanisme protection défenseurs sous-financé",
            ],
        ),
        EnvironmentalDefendersRightsEntity(
            entity_id="EDR-006",
            name="Inde/Jharkhand — Lois Sédition Contre Adivasis, Résistance Vedanta Copper Criminalisée",
            country="Inde",
            sector="Défense Terres Adivasi & Forêts",
            environmental_defender_killings_impunity_score=55.0,
            criminalization_protest_slapp_score=52.0,
            state_corporate_collusion_repression_score=53.0,
            legal_protection_whistleblower_gap_score=50.0,
            primary_pattern="criminalization_protest_slapp",
            key_signals=[
                "Lois sédition utilisées contre activistes Adivasi",
                "Vedanta copper plant fermé après protestation populaire",
                "Forest Rights Act 2006 mal appliqué",
                "POSCO steel resistance criminalisée Odisha",
            ],
        ),
        EnvironmentalDefendersRightsEntity(
            entity_id="EDR-007",
            name="Russie — ONG Environnementales Agents Étrangers, Team Écologiste Navalny Arrêtée",
            country="Russie",
            sector="Activisme Environnemental & Répression ONG",
            environmental_defender_killings_impunity_score=35.0,
            criminalization_protest_slapp_score=32.0,
            state_corporate_collusion_repression_score=33.0,
            legal_protection_whistleblower_gap_score=30.0,
            primary_pattern="criminalization_protest_slapp",
            key_signals=[
                "Loi agents étrangers dissout ONG environnementales",
                "Ekozaschita et Baikal Environmental Wave liquidées",
                "Journalistes écologistes sous surveillance FSB",
                "Gazprom et Rosneft protégés des poursuites civiles",
            ],
        ),
        EnvironmentalDefendersRightsEntity(
            entity_id="EDR-008",
            name="Pays-Bas/Urgenda — Modèle Référence, Shell Condamné, mais Financement Fossile 3e Mondial",
            country="Pays-Bas",
            sector="Contentieux Climatique & Droits Environnementaux",
            environmental_defender_killings_impunity_score=8.0,
            criminalization_protest_slapp_score=10.0,
            state_corporate_collusion_repression_score=9.0,
            legal_protection_whistleblower_gap_score=7.0,
            primary_pattern="legal_protection_whistleblower_gap",
            key_signals=[
                "Urgenda v. Netherlands 2019 — victoire historique climat",
                "Shell condamné à réduire émissions 45% d'ici 2030",
                "Défenseurs protégés — pas de meurtres documentés",
                "ING et ABN AMRO financement fossile 3e mondial reste problème",
            ],
        ),
    ]

    composites = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(composites), 2)

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    pattern_dist: dict = {}
    for e in entities:
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

    sorted_entities = sorted(entities, key=lambda x: x.composite_score, reverse=True)
    top_risk = [e.name for e in sorted_entities[:3]]
    alerts = [
        f"{e.name.split('—')[0].strip()}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    return EnvironmentalDefendersRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_environmental_defenders_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_witness_defenders_report_2023",
            "front_line_defenders_global_analysis_2023",
            "business_human_rights_resource_centre_2023",
            "un_special_rapporteur_environment_defenders_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_environmental_defenders_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_environmental_defenders_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
