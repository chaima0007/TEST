from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ENGINE_VERSION = "1.0.0"

@dataclass
class AcademicFreedomScholarPersecutionEntity:
    entity_id: str
    name: str
    country: str
    scholar_imprisonment_persecution_score: float
    university_autonomy_state_interference_score: float
    banned_research_censorship_score: float
    academic_self_censorship_chilling_effect_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_academic_freedom_scholar_persecution_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.scholar_imprisonment_persecution_score * 0.30
            + self.university_autonomy_state_interference_score * 0.25
            + self.banned_research_censorship_score * 0.25
            + self.academic_self_censorship_chilling_effect_score * 0.20,
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
        self.estimated_academic_freedom_scholar_persecution_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class AcademicFreedomScholarPersecutionEngineResult:
    agent: str = "Academic Freedom Scholar Persecution Engine Agent"
    domain: str = "academic_freedom_scholar_persecution"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = ENGINE_VERSION
    avg_estimated_academic_freedom_scholar_persecution_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AcademicFreedomScholarPersecutionEntity] = field(default_factory=list)


def run_academic_freedom_scholar_persecution_engine() -> AcademicFreedomScholarPersecutionEngineResult:
    entities = [
        AcademicFreedomScholarPersecutionEntity(
            entity_id="AFSP-001",
            name="Chine/Universités Parti — Chercheurs Xinjiang Incarcérés, Comités Parti Contrôlent Curricula, Recherche IA Militaire Obligatoire, Autocensure 90%+ Sondages & Historiens Tiananmen Interdits",
            country="Chine",
            scholar_imprisonment_persecution_score=92.0,
            university_autonomy_state_interference_score=95.0,
            banned_research_censorship_score=90.0,
            academic_self_censorship_chilling_effect_score=88.0,
            primary_pattern="interference_etat_universite",
        ),
        AcademicFreedomScholarPersecutionEntity(
            entity_id="AFSP-002",
            name="Iran/Purges Universitaires — 700+ Professeurs Licenciés Post-2022, Étudiantes Empoisonnées Suspectes, Sociologues Emprisonnés, Femmes Exclues Certaines Disciplines & Sciences Humaines Épurées",
            country="Iran",
            scholar_imprisonment_persecution_score=88.0,
            university_autonomy_state_interference_score=85.0,
            banned_research_censorship_score=82.0,
            academic_self_censorship_chilling_effect_score=90.0,
            primary_pattern="persecution_chercheurs_dissidents",
        ),
        AcademicFreedomScholarPersecutionEntity(
            entity_id="AFSP-003",
            name="Turquie/Post-Coup 2016 — 6000+ Académiciens Suspendus Passeports Confisqués, Pétition Paix 2000 Signataires Poursuivis, Universités Recteurs Nommés État & Kurdologie Interdite",
            country="Turquie",
            scholar_imprisonment_persecution_score=85.0,
            university_autonomy_state_interference_score=88.0,
            banned_research_censorship_score=80.0,
            academic_self_censorship_chilling_effect_score=82.0,
            primary_pattern="persecution_chercheurs_dissidents",
        ),
        AcademicFreedomScholarPersecutionEntity(
            entity_id="AFSP-004",
            name="Russie/Guerre Ukraine — Sociologues Lev Gudkov Menacés, Historiens Mémorial Liquidé, Enseigner Guerre Interdite, Physiciens Nucléaires Arrêtés Espionnage & Exode Cerveaux 500K+ Post-2022",
            country="Russie",
            scholar_imprisonment_persecution_score=82.0,
            university_autonomy_state_interference_score=80.0,
            banned_research_censorship_score=85.0,
            academic_self_censorship_chilling_effect_score=88.0,
            primary_pattern="censure_recherche_interdite",
        ),
        AcademicFreedomScholarPersecutionEntity(
            entity_id="AFSP-005",
            name="Hongrie/Modèle Orbán — CEU Expulsée Budapest Vienne, Académie Sciences Restructurée Politique, Gender Studies Interdits Universités, Financement ONG Académique Coupé & Loi Anti-LGBTQ Curricula",
            country="Hongrie",
            scholar_imprisonment_persecution_score=38.0,
            university_autonomy_state_interference_score=60.0,
            banned_research_censorship_score=55.0,
            academic_self_censorship_chilling_effect_score=45.0,
            primary_pattern="interference_etat_universite",
        ),
        AcademicFreedomScholarPersecutionEntity(
            entity_id="AFSP-006",
            name="USA/Lois Anti-DEI 2023-2024 — 18 États Interdisent Études Critiques Race, Professeurs Licenciés Floride, Bibliothèques Épurées Livres Interdits & Chaires Histoire Noire Défundées Législatures",
            country="USA",
            scholar_imprisonment_persecution_score=30.0,
            university_autonomy_state_interference_score=48.0,
            banned_research_censorship_score=52.0,
            academic_self_censorship_chilling_effect_score=45.0,
            primary_pattern="censure_recherche_interdite",
        ),
        AcademicFreedomScholarPersecutionEntity(
            entity_id="AFSP-007",
            name="Allemagne/Tendances Autocensure — Débat Gaza Campus Réprimé, Chercheurs Pro-Palestiniens Invitations Annulées, Contrats Conditionnels Déclaration Anti-BDS & Pressions Financement Politique",
            country="Allemagne",
            scholar_imprisonment_persecution_score=10.0,
            university_autonomy_state_interference_score=22.0,
            banned_research_censorship_score=25.0,
            academic_self_censorship_chilling_effect_score=30.0,
            primary_pattern="censure_recherche_interdite",
        ),
        AcademicFreedomScholarPersecutionEntity(
            entity_id="AFSP-008",
            name="Finlande/Liberté Académique Référence — Universités Autonomes Loi 558/2009, Aucun Chercheur Emprisonné, Liberté Recherche Constitutionnelle, Financement Public Indépendant & Accès Ouvert Publications",
            country="Finlande",
            scholar_imprisonment_persecution_score=2.0,
            university_autonomy_state_interference_score=3.0,
            banned_research_censorship_score=3.0,
            academic_self_censorship_chilling_effect_score=5.0,
            primary_pattern="interference_etat_universite",
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

    return AcademicFreedomScholarPersecutionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_academic_freedom_scholar_persecution_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "scholars_at_risk_network_monitoring_project_2023",
            "academic_freedom_index_fau_erlangen_2023",
            "human_rights_watch_academic_freedom_reports",
            "aaup_annual_report_academic_freedom_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_academic_freedom_scholar_persecution_engine()
    print(f"Agent: {result.agent}")
    print(f"Engine version: {result.engine_version}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Confidence score: {result.confidence_score}")
    print(f"Avg index: {result.avg_estimated_academic_freedom_scholar_persecution_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print(f"Data sources: {result.data_sources}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — index={e.estimated_academic_freedom_scholar_persecution_index}")
