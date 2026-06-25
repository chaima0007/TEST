"""
Caelum Partners — Torture Prevention Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Prévention de la torture et droits des victimes (torture systématique, conditions de détention,
impunité des auteurs, réhabilitation des victimes).

La Convention des Nations Unies contre la torture (CAT, 1984) constitue l'un des
traités de droits humains les plus ratifiés — pourtant sa mise en œuvre demeure
profondément inégale. Des États comme la Corée du Nord et la Syrie maintiennent
des systèmes de torture institutionnalisés à grande échelle, tandis que des régimes
comme l'Égypte d'al-Sissi documentent des milliers de cas de torture en détention.
L'impunité des auteurs de torture reste la règle, et les victimes se voient souvent
dénier tout accès à la réhabilitation ou à la justice.

Risk levels (torture systématique, conditions détention, impunité et réhabilitation) :
  critique  -> composite >= 60  (torture institutionnalisée — camps, sites noirs, impunité totale)
  élevé     -> composite >= 40  (torture documentée — impunité significative, réhabilitation absente)
  modéré    -> composite >= 20  (abus documentés — quelques mécanismes, lacunes importantes)
  faible    -> composite < 20   (mécanismes préventifs effectifs — plaintes instruites, réhabilitation)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class TorturePreventionRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    systematic_torture_score: float
    detention_conditions_score: float
    impunity_perpetrators_score: float
    rehabilitation_victims_denial_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_torture_prevention_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.systematic_torture_score * 0.30
            + self.detention_conditions_score * 0.25
            + self.impunity_perpetrators_score * 0.25
            + self.rehabilitation_victims_denial_score * 0.20,
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
        self.estimated_torture_prevention_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "systematic_torture_score": self.systematic_torture_score,
            "detention_conditions_score": self.detention_conditions_score,
            "impunity_perpetrators_score": self.impunity_perpetrators_score,
            "rehabilitation_victims_denial_score": self.rehabilitation_victims_denial_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_torture_prevention_rights_index": self.estimated_torture_prevention_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class TorturePreventionRightsEngineResult:
    agent: str = "Torture Prevention Rights Engine Agent"
    domain: str = "torture_prevention_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.91
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_torture_prevention_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[TorturePreventionRightsEntity] = field(default_factory=list)


def run_torture_prevention_rights_engine() -> TorturePreventionRightsEngineResult:
    entities = [
        TorturePreventionRightsEntity(
            entity_id="TPR-001",
            name="Corée du Nord — Camps Kwanliso Torture Institutionnalisée, 200 000+ Prisonniers Politiques & Expériences Humaines",
            country="Corée du Nord",
            sector="Camps Politiques & Détention Extrajudiciaire",
            systematic_torture_score=92.0,
            detention_conditions_score=91.0,
            impunity_perpetrators_score=92.0,
            rehabilitation_victims_denial_score=92.0,
            primary_pattern="systematic_torture",
            key_signals=[
                "200 000+ prisonniers politiques camps Kwanliso",
                "torture systémique documentée Commission ONU 2014",
                "expériences médicales sur prisonniers politiques",
                "réhabilitation victimes inexistante, retour impossible",
            ],
        ),
        TorturePreventionRightsEntity(
            entity_id="TPR-002",
            name="Syrie — Centres Détention Assad Torture Industrielle, 55 000+ Photos César & 14 000 Morts Documentes",
            country="Syrie",
            sector="Détention Politique & Torture d'État",
            systematic_torture_score=91.0,
            detention_conditions_score=90.0,
            impunity_perpetrators_score=91.0,
            rehabilitation_victims_denial_score=90.0,
            primary_pattern="systematic_torture",
            key_signals=[
                "55 000+ photos César documentant torture à mort",
                "14 000+ morts en détention enregistrés",
                "viols systématiques arme de guerre",
                "impunité totale régime Assad — aucune poursuite interne",
            ],
        ),
        TorturePreventionRightsEntity(
            entity_id="TPR-003",
            name="Égypte — Torture Régime Al-Sissi Documentée HRW, 3 000+ Disparitions Forcées & Électrochocs Prisons Scorpion",
            country="Égypte",
            sector="Sécurité d'État & Détention Politique",
            systematic_torture_score=91.0,
            detention_conditions_score=90.0,
            impunity_perpetrators_score=92.0,
            rehabilitation_victims_denial_score=91.0,
            primary_pattern="impunity_perpetrators",
            key_signals=[
                "3 000+ disparitions forcées depuis 2013",
                "prisons Scorpion/Tora conditions de torture documentées",
                "électrochocs et noyade téléphone signalés HRW",
                "aucun tortionnaire poursuivi — impunité institutionnalisée",
            ],
        ),
        TorturePreventionRightsEntity(
            entity_id="TPR-004",
            name="Chine — Torture Camps Xinjiang 1M+ Ouïghours, Organ Harvesting Prisonniers & Aveux Forcés Télévisés",
            country="Chine",
            sector="Détention Masse & Torture Ethnique/Politique",
            systematic_torture_score=90.0,
            detention_conditions_score=89.0,
            impunity_perpetrators_score=91.0,
            rehabilitation_victims_denial_score=90.0,
            primary_pattern="systematic_torture",
            key_signals=[
                "1 million+ Ouïghours camps rééducation Xinjiang",
                "organ harvesting prisonniers condamnés documenté",
                "aveux forcés télévisés avocats droits humains",
                "réhabilitation victimes interdite — surveillance continue libérés",
            ],
        ),
        TorturePreventionRightsEntity(
            entity_id="TPR-005",
            name="Arabie Saoudite — Torture Dissidents Khashoggi & MBS, Conditions Détention Femmes Militantes & Impunité Totale",
            country="Arabie Saoudite",
            sector="Détention Politique & Sécurité d'État",
            systematic_torture_score=51.0,
            detention_conditions_score=50.0,
            impunity_perpetrators_score=52.0,
            rehabilitation_victims_denial_score=51.0,
            primary_pattern="impunity_perpetrators",
            key_signals=[
                "assassinat torture Jamal Khashoggi Istanbul 2018",
                "militantes droits femmes torturées détention 2018-2019",
                "conditions détention inhumaines Riyad documentées",
                "impunité totale — aucune poursuite interne MBS",
            ],
        ),
        TorturePreventionRightsEntity(
            entity_id="TPR-006",
            name="USA — Guantanamo Waterboarding CIA, 80 000 Détenus Isolement & Sites Noirs Sans Poursuites Tortionnaires",
            country="USA",
            sector="Détention Sécurité Nationale & Prisons",
            systematic_torture_score=50.0,
            detention_conditions_score=51.0,
            impunity_perpetrators_score=54.0,
            rehabilitation_victims_denial_score=52.0,
            primary_pattern="impunity_perpetrators",
            key_signals=[
                "waterboarding CIA — rapport Senate Intelligence 2014",
                "80 000+ détenus en isolement cellulaire USA",
                "réseau mondial black sites CIA documenté",
                "aucune poursuite pénale tortionnaires CIA — impunité légale",
            ],
        ),
        TorturePreventionRightsEntity(
            entity_id="TPR-007",
            name="ONU CAT — Convention Contre la Torture Application Limitée, Comité Monitoring & États Non-Coopératifs",
            country="International",
            sector="Mécanisme International de Surveillance",
            systematic_torture_score=30.0,
            detention_conditions_score=28.0,
            impunity_perpetrators_score=32.0,
            rehabilitation_victims_denial_score=29.0,
            primary_pattern="rehabilitation_victims_denial",
            key_signals=[
                "CAT ratifiée 173 États — application inégale",
                "Comité CAT rapports sans mécanisme coercitif",
                "États parties refusant visites SPT",
                "lacunes réhabilitation victimes — art.14 CAT insuffisant",
            ],
        ),
        TorturePreventionRightsEntity(
            entity_id="TPR-008",
            name="ACAT / Amnesty International — Meilleure Pratique Documentation Torture, Soutien Victimes & Plaidoyer Global",
            country="International",
            sector="Société Civile & ONG Droits Humains",
            systematic_torture_score=6.0,
            detention_conditions_score=5.0,
            impunity_perpetrators_score=5.0,
            rehabilitation_victims_denial_score=6.0,
            primary_pattern="systematic_torture",
            key_signals=[
                "documentation mondiale torture — base données vérifiée",
                "soutien légal et psychologique victimes torture",
                "plaidoyer CAT — pression États ratificateurs",
                "campagnes impunité zéro — poursuites tortionnaires",
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

    return TorturePreventionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_torture_prevention_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_committee_against_torture_cat_annual_report_2024",
            "amnesty_international_torture_global_report_2024",
            "human_rights_watch_torture_detention_2024",
            "acat_france_rapport_torture_mondial_2023",
            "irct_international_rehabilitation_council_torture_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_torture_prevention_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_torture_prevention_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
