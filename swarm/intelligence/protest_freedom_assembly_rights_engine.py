"""
Caelum Partners — Protest Freedom Assembly Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Liberté de réunion et répression des manifestations — criminalisation de la protestation,
balles en caoutchouc, arrestations massives.

Le droit de se réunir pacifiquement constitue l'un des droits fondamentaux les plus
attaqués dans le monde contemporain. Des régimes autoritaires aux démocraties libérales,
les gouvernements recourent à une gamme croissante d'outils pour réprimer la contestation
sociale : armes moins létales causant des mutilations permanentes, lois anti-protestation
criminalisant l'expression légitime, détentions arbitraires massives et impunité quasi
systématique des forces de sécurité.

Les données du CIVICUS Monitor révèlent que moins de 4% de la population mondiale vit
dans des pays où l'espace civique est ouvert. Les manifestants iraniens d'octobre 2022,
les Biélorusses de 2020 ou les opposants russes à la guerre d'Ukraine paient de leur
liberté, voire de leur vie, l'exercice d'un droit consacré par l'article 20 de la DUDH.
Même dans les démocraties, les excès policiers contre les manifestants des gilets jaunes
en France ou BLM aux États-Unis illustrent les déficits persistants d'accountability.

Risk levels (répression manifestations et liberté de réunion) :
  critique  -> composite >= 60  (répression létale systémique — manifestants tués, impunité totale)
  élevé     -> composite >= 40  (violences documentées — arrestations massives, lois répressives)
  modéré    -> composite >= 20  (abus documentés — réformes insuffisantes)
  faible    -> composite < 20   (cadre protecteur — manifestations encadrées légalement)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class ProtestFreedomAssemblyRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    violent_protest_repression_score: float
    mass_arrest_detention_protesters_score: float
    anti_protest_laws_criminalization_score: float
    impunity_security_forces_protest_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_protest_freedom_assembly_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.violent_protest_repression_score * 0.30
            + self.mass_arrest_detention_protesters_score * 0.25
            + self.anti_protest_laws_criminalization_score * 0.25
            + self.impunity_security_forces_protest_score * 0.20,
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
        self.estimated_protest_freedom_assembly_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "violent_protest_repression_score": self.violent_protest_repression_score,
            "mass_arrest_detention_protesters_score": self.mass_arrest_detention_protesters_score,
            "anti_protest_laws_criminalization_score": self.anti_protest_laws_criminalization_score,
            "impunity_security_forces_protest_score": self.impunity_security_forces_protest_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_protest_freedom_assembly_rights_index": self.estimated_protest_freedom_assembly_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class ProtestFreedomAssemblyRightsEngineResult:
    agent: str = "Protest Freedom Assembly Rights Engine Agent"
    domain: str = "protest_freedom_assembly_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_protest_freedom_assembly_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ProtestFreedomAssemblyRightsEntity] = field(default_factory=list)


def run_protest_freedom_assembly_rights_engine() -> ProtestFreedomAssemblyRightsEngineResult:
    entities = [
        ProtestFreedomAssemblyRightsEntity(
            entity_id="PFAR-001",
            name="Iran/2022-2023 — Mahsa Amini 500+ Tués, 18000+ Arrêtés, Internet Coupé, Pendaisons Manifestants",
            country="Iran",
            sector="Répression Mouvement Protestataire",
            violent_protest_repression_score=97.0,
            mass_arrest_detention_protesters_score=96.0,
            anti_protest_laws_criminalization_score=95.0,
            impunity_security_forces_protest_score=94.0,
            primary_pattern="violent_protest_repression",
            key_signals=[
                "500+ manifestants tués durant protestation Mahsa Amini 2022-2023",
                "18 000+ arrêtés dont mineurs condamnés à mort",
                "Internet et réseaux sociaux coupés systématiquement durant répressions",
                "Exécutions publiques manifestants comme avertissement — Mohsen Shekari pendu",
            ],
        ),
        ProtestFreedomAssemblyRightsEntity(
            entity_id="PFAR-002",
            name="Birmanie/Myanmar Post-Coup 2021 — 3000+ Tués, CRPH Dissous, Manifestants Fusillés Rue",
            country="Myanmar",
            sector="Répression Post-Coup Militaire",
            violent_protest_repression_score=96.0,
            mass_arrest_detention_protesters_score=93.0,
            anti_protest_laws_criminalization_score=91.0,
            impunity_security_forces_protest_score=92.0,
            primary_pattern="violent_protest_repression",
            key_signals=[
                "3000+ civils tués par armée depuis coup d'état février 2021",
                "CDM — mouvement désobéissance civile — réprimé avec fusillades de rue",
                "CRPH reconstitué en NUG mais sans pouvoir arrêter la junta",
                "Loi urgence décrétée annulant tous droits fondamentaux de réunion",
            ],
        ),
        ProtestFreedomAssemblyRightsEntity(
            entity_id="PFAR-003",
            name="Biélorussie/2020 — 35000+ Arrêtés, Loukachenko, OMON Torture Systématique, Tikhanovskaïa Exil",
            country="Biélorussie",
            sector="Répression Post-Électorale",
            violent_protest_repression_score=92.0,
            mass_arrest_detention_protesters_score=95.0,
            anti_protest_laws_criminalization_score=88.0,
            impunity_security_forces_protest_score=89.0,
            primary_pattern="mass_arrest_detention_protesters",
            key_signals=[
                "35 000+ personnes arrêtées lors des manifestations post-élections 2020",
                "Torture systématique documentée dans centres de détention OMON",
                "Sviatlana Tikhanovskaïa contrainte à l'exil après tentative candidature",
                "Journalistes et médecins arrêtés pour couverture des manifestations",
            ],
        ),
        ProtestFreedomAssemblyRightsEntity(
            entity_id="PFAR-004",
            name="Russie/Anti-Guerre 2022 — 16000+ Arrêtés, Loi 15 Ans Prison Discrédit Armée, OVD-Info Rapport",
            country="Russie",
            sector="Répression Antiwar & Dissidence",
            violent_protest_repression_score=86.0,
            mass_arrest_detention_protesters_score=91.0,
            anti_protest_laws_criminalization_score=95.0,
            impunity_security_forces_protest_score=88.0,
            primary_pattern="anti_protest_laws_criminalization",
            key_signals=[
                "16 000+ arrêtés pour protestation anti-guerre selon OVD-Info",
                "Loi mars 2022 : jusqu'à 15 ans prison pour discrédit forces armées",
                "Pancartes blanches et mimes arrêtés — manifestation symbolique criminalisée",
                "Alexeï Navalny et milliers opposants emprisonnés pour activisme pacifique",
            ],
        ),
        ProtestFreedomAssemblyRightsEntity(
            entity_id="PFAR-005",
            name="USA/BLM 2020 — National Guard Déployé, 14000 Arrêtés, Rubber Bullets Yeux, ACLU Lawsuit",
            country="USA",
            sector="Répression Mouvement Racial Justice",
            violent_protest_repression_score=58.0,
            mass_arrest_detention_protesters_score=62.0,
            anti_protest_laws_criminalization_score=50.0,
            impunity_security_forces_protest_score=53.0,
            primary_pattern="mass_arrest_detention_protesters",
            key_signals=[
                "14 000+ arrêtés en deux semaines manifestations BLM post-Floyd",
                "Balles en caoutchouc et gaz lacrymo contre manifestants pacifiques documentés",
                "National Guard déployée dans 23 états — militarisation réponse policière",
                "ACLU lawsuits contre usage force excessive — peu de condamnations policiers",
            ],
        ),
        ProtestFreedomAssemblyRightsEntity(
            entity_id="PFAR-006",
            name="France/Gilets Jaunes — 25 Yeux Perdus LBD40, IGPN Inefficace, Macron Défenseur Droits Critiqué",
            country="France",
            sector="Répression Mouvement Social",
            violent_protest_repression_score=54.0,
            mass_arrest_detention_protesters_score=50.0,
            anti_protest_laws_criminalization_score=48.0,
            impunity_security_forces_protest_score=55.0,
            primary_pattern="impunity_security_forces_protest",
            key_signals=[
                "25 manifestants ayant perdu un oeil suite aux LBD40 — chiffre sans précédent Europe",
                "5 mains arrachées par grenades de désencerclement — mutilations permanentes",
                "IGPN — police des polices — critiquée pour manque d'indépendance",
                "Conseil d'État rejette recours contre LBD40 malgré ONU et Amnesty critiques",
            ],
        ),
        ProtestFreedomAssemblyRightsEntity(
            entity_id="PFAR-007",
            name="Chili/Estallido Social 2019 — 460 Yeux Perdus, INDH Condamne, Piñera Réforme Constitutionnelle",
            country="Chili",
            sector="Répression Mouvement Social",
            violent_protest_repression_score=30.0,
            mass_arrest_detention_protesters_score=27.0,
            anti_protest_laws_criminalization_score=25.0,
            impunity_security_forces_protest_score=28.0,
            primary_pattern="violent_protest_repression",
            key_signals=[
                "460 personnes ayant perdu un oeil — record mondial chevillot caoutchouc",
                "INDH dénonce violations — processus constitutionnel entamé puis rejeté",
                "Carabineros réformés partiellement après rapport accablant Human Rights Watch",
                "Transition vers processus constitutionnel — répression malgré réformes",
            ],
        ),
        ProtestFreedomAssemblyRightsEntity(
            entity_id="PFAR-008",
            name="Allemagne/Droit Manifestation — Grundgesetz Art.8 Protège, Police Encadrée, Procédures Claires",
            country="Allemagne",
            sector="Cadre Protecteur Référence",
            violent_protest_repression_score=7.0,
            mass_arrest_detention_protesters_score=6.0,
            anti_protest_laws_criminalization_score=8.0,
            impunity_security_forces_protest_score=7.0,
            primary_pattern="anti_protest_laws_criminalization",
            key_signals=[
                "Grundgesetz article 8 garanti constitutionnellement le droit de manifestation",
                "Police sous contrôle civil strict — procédures d'usage de la force encadrées",
                "Manifestations Anti-AfD et Fridays for Future — espace civique préservé",
                "Modèle européen cité pour équilibre maintien ordre et libertés fondamentales",
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

    return ProtestFreedomAssemblyRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_protest_freedom_assembly_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "civicus_monitor_civic_space_2023",
            "amnesty_international_protest_rights_2023",
            "human_rights_watch_protest_repression_2023",
            "un_special_rapporteur_peaceful_assembly_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_protest_freedom_assembly_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_protest_freedom_assembly_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
