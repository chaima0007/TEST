"""
Caelum Partners — Freedom of Assembly Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Liberté de réunion et d'association (répression des protestations, suppression
de la société civile, détention arbitraire des manifestants, criminalisation des ONG).

La liberté de réunion pacifique et d'association est garantie par l'article 20
de la DUDH et l'article 21-22 du PIDCP. Pourtant, depuis 2020, on observe
une vague mondiale de répressions : la Biélorussie a arrêté 35 000 personnes
après les élections frauduleuses de 2020, l'Iran a tué 500+ manifestants lors
des protestations Mahsa Amini en 2022, et la Russie a criminalisé toute expression
d'opposition à l'invasion de l'Ukraine. Ces régressions globales constituent un
indicateur clé de l'effondrement des démocraties illibérales.

Risk levels (répression protestations, société civile, détention arbitraire, ONG) :
  critique  -> composite >= 60  (répression systémique — tirs sur manifestants, ONG bannies)
  élevé     -> composite >= 40  (répression documentée — arrestations massives, lois restrictives)
  modéré    -> composite >= 20  (restrictions partielles — maintien ordre critiqué, ONG sous pression)
  faible    -> composite < 20   (liberté de réunion protégée — manifestations légales, ONG libres)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class FreedomAssemblyRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    protest_repression_score: float
    civil_society_suppression_score: float
    arbitrary_detention_protesters_score: float
    ngo_criminalization_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_freedom_assembly_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.protest_repression_score * 0.30
            + self.civil_society_suppression_score * 0.25
            + self.arbitrary_detention_protesters_score * 0.25
            + self.ngo_criminalization_score * 0.20,
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
        self.estimated_freedom_assembly_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "protest_repression_score": self.protest_repression_score,
            "civil_society_suppression_score": self.civil_society_suppression_score,
            "arbitrary_detention_protesters_score": self.arbitrary_detention_protesters_score,
            "ngo_criminalization_score": self.ngo_criminalization_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_freedom_assembly_rights_index": self.estimated_freedom_assembly_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class FreedomAssemblyRightsEngineResult:
    agent: str = "Freedom Assembly Rights Engine Agent"
    domain: str = "freedom_assembly_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.90
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_freedom_assembly_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[FreedomAssemblyRightsEntity] = field(default_factory=list)


def run_freedom_assembly_rights_engine() -> FreedomAssemblyRightsEngineResult:
    entities = [
        FreedomAssemblyRightsEntity(
            entity_id="FAR-001",
            name="Biélorussie — Répressions Massives Post-2020, 35 000 Arrêtés Manifestations & Lukashenko Terreur d'État",
            country="Biélorussie",
            sector="Répression Politique & Autoritarisme Post-Electoral",
            protest_repression_score=90.0,
            civil_society_suppression_score=89.0,
            arbitrary_detention_protesters_score=90.0,
            ngo_criminalization_score=89.0,
            primary_pattern="protest_repression",
            key_signals=[
                "35 000+ arrestations manifestations post-élections 2020",
                "société civile entièrement détruite — ONG liquidées",
                "journalistes et militants condamnés peines lourdes",
                "exil forcé 200 000+ opposants Lukashenko",
            ],
        ),
        FreedomAssemblyRightsEntity(
            entity_id="FAR-002",
            name="Iran — Protestations Mahsa Amini 2022 Écrasées, 500+ Tués & 15 000 Arrêtés Gardiens Révolution",
            country="Iran",
            sector="Répression Mouvement Social & Droits Femmes",
            protest_repression_score=89.0,
            civil_society_suppression_score=87.0,
            arbitrary_detention_protesters_score=88.0,
            ngo_criminalization_score=87.0,
            primary_pattern="protest_repression",
            key_signals=[
                "500+ manifestants tués protestations Mahsa Amini 2022",
                "15 000+ arrêtés dont centaines mineurs",
                "peine de mort appliquée manifestants",
                "ONG féministes et syndicats interdits, criminalisés",
            ],
        ),
        FreedomAssemblyRightsEntity(
            entity_id="FAR-003",
            name="Russie — Loi 2022 Discrédit Armée Anti-Guerre, 16 000+ Arrestations & Société Civile Anéantie",
            country="Russie",
            sector="Répression Contestation & Criminalisation Opposition",
            protest_repression_score=92.0,
            civil_society_suppression_score=91.0,
            arbitrary_detention_protesters_score=92.0,
            ngo_criminalization_score=92.0,
            primary_pattern="civil_society_suppression",
            key_signals=[
                "16 000+ arrêtés manifestations anti-guerre Ukraine",
                "loi criminalisant discrédit armée — 15 ans prison",
                "ONG étrangères statut d'agent étranger",
                "Mémorial liquidé — histoire répression soviétique effacée",
            ],
        ),
        FreedomAssemblyRightsEntity(
            entity_id="FAR-004",
            name="Myanmar — Militaires Tirant sur Manifestants Post-Coup 2021, 3 000+ Civils Tués & NLD Criminalisée",
            country="Myanmar",
            sector="Coup Militaire & Répression Population Civile",
            protest_repression_score=93.0,
            civil_society_suppression_score=91.0,
            arbitrary_detention_protesters_score=92.0,
            ngo_criminalization_score=90.0,
            primary_pattern="protest_repression",
            key_signals=[
                "3 000+ civils tués par militaires depuis coup 2021",
                "NLD et partis politiques bannis, Aung San Suu Kyi emprisonnée",
                "ONG humanitaires expulsées ou contraintes à fermer",
                "manifestants pacifiques condamnés à mort par tribunaux militaires",
            ],
        ),
        FreedomAssemblyRightsEntity(
            entity_id="FAR-005",
            name="Éthiopie/Tigray — ONG Expulsées, Journalistes Arrêtés & Loi Anti-Terroriste Contre Militants Civils",
            country="Éthiopie",
            sector="Conflit & Restriction Société Civile",
            protest_repression_score=54.0,
            civil_society_suppression_score=55.0,
            arbitrary_detention_protesters_score=53.0,
            ngo_criminalization_score=54.0,
            primary_pattern="ngo_criminalization",
            key_signals=[
                "ONG internationales expulsées zones conflit Tigray",
                "journalistes arrêtés loi anti-terrorisme",
                "Internet coupé lors manifestations anti-gouvernementales",
                "Oromo Federalist Congress et OLF criminalisés",
            ],
        ),
        FreedomAssemblyRightsEntity(
            entity_id="FAR-006",
            name="Inde — UAPA Contre Militants CAA/Farmers, ONG Étrangères FCRA Bloquées & Arrestations Opposants",
            country="Inde",
            sector="Démocratie Illibérale & Restriction Société Civile",
            protest_repression_score=48.0,
            civil_society_suppression_score=50.0,
            arbitrary_detention_protesters_score=49.0,
            ngo_criminalization_score=51.0,
            primary_pattern="ngo_criminalization",
            key_signals=[
                "UAPA utilisé contre militants CAA et agriculteurs",
                "FCRA suspension Amnesty India, Greenpeace — blocage ONG",
                "journalistes critiques Modi arrêtés sédition",
                "manifestations farmers 2021 — internet coupé Punjab",
            ],
        ),
        FreedomAssemblyRightsEntity(
            entity_id="FAR-007",
            name="France — Mutilations LBD Gilets Jaunes, Maintien Ordre Critiqué CNCDH & COP Répression Manifestants",
            country="France",
            sector="Maintien de l'Ordre & Droits Manifestants",
            protest_repression_score=27.0,
            civil_society_suppression_score=24.0,
            arbitrary_detention_protesters_score=26.0,
            ngo_criminalization_score=22.0,
            primary_pattern="protest_repression",
            key_signals=[
                "30+ personnes éborgnées LBD Gilets Jaunes 2018-2019",
                "CNCDH et Défenseur des droits critiquent maintien ordre",
                "arrestations préventives COP21 — libertés restreintes",
                "schéma nassage controversé manifestations climatiques",
            ],
        ),
        FreedomAssemblyRightsEntity(
            entity_id="FAR-008",
            name="Costa Rica / Uruguay — Meilleure Pratique Liberté Réunion, Manifestations Protégées & ONG Libres",
            country="Costa Rica/Uruguay",
            sector="Démocratie Consolidée & Droits Réunion Protégés",
            protest_repression_score=6.0,
            civil_society_suppression_score=5.0,
            arbitrary_detention_protesters_score=5.0,
            ngo_criminalization_score=5.0,
            primary_pattern="civil_society_suppression",
            key_signals=[
                "manifestations légales protégées constitutionnellement",
                "ONG société civile librement actives sans restriction",
                "aucune détention arbitraire manifestants documentée",
                "indicateur liberté civile Freedom House top mondial",
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

    return FreedomAssemblyRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_freedom_assembly_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "civicus_monitor_civic_space_2024",
            "freedom_house_freedom_world_2024",
            "human_rights_watch_assembly_association_2024",
            "amnesty_international_civic_freedoms_2024",
            "ohchr_special_rapporteur_assembly_report_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_freedom_assembly_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_freedom_assembly_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
