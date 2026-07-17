"""
Caelum Partners — Enforced Disappearances & Extrajudicial Executions Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Disparitions forcées & exécutions extrajudiciaires — impunité d'État, vérité,
justice transitionnelle, droits des familles des victimes.

Les disparitions forcées constituent l'une des violations les plus graves des droits humains.
Selon la Convention internationale pour la protection de toutes les personnes contre
les disparitions forcées (CPPED, 2010), un acte de disparition forcée est commis lorsqu'une
personne est arrêtée ou détenue par des agents de l'État — ou avec leur complicité — suivie
d'un refus de reconnaître cette privation de liberté ou de révéler le sort de la victime.

Plus de 50 000 cas de disparitions forcées ont été officiellement communiqués au Groupe
de travail de l'ONU sur les disparitions forcées ou involontaires depuis 1980. Le chiffre
réel est estimé à plusieurs centaines de milliers. Au Mexique seul, plus de 100 000 personnes
sont portées disparues. Les exécutions extrajudiciaires — tirs à vue, meurtre en détention,
assassinats politiques — perpétuent la même culture de l'impunité.

Risk levels (taux disparitions, impunité, reddition de comptes État, vérité-justice-réparation) :
  critique  -> composite >= 60  (disparitions massives — impunité totale, État impliqué directement)
  élevé     -> composite >= 40  (disparitions significatives — reddition partielle, justice défaillante)
  modéré    -> composite >= 20  (cas historiques — processus transitionnels en cours)
  faible    -> composite < 20   (cadre protecteur — mécanismes reddition comptes fonctionnels)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class EnforcedDisappearancesExtrajudicialEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    disappearance_rate_impunity_score: float
    extrajudicial_killing_score: float
    state_accountability_deficit_score: float
    truth_justice_reparation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_disappearances_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.disappearance_rate_impunity_score * 0.30
            + self.extrajudicial_killing_score * 0.25
            + self.state_accountability_deficit_score * 0.25
            + self.truth_justice_reparation_score * 0.20,
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
        self.estimated_disappearances_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "disappearance_rate_impunity_score": self.disappearance_rate_impunity_score,
            "extrajudicial_killing_score": self.extrajudicial_killing_score,
            "state_accountability_deficit_score": self.state_accountability_deficit_score,
            "truth_justice_reparation_score": self.truth_justice_reparation_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_disappearances_index": self.estimated_disappearances_index,
            "last_updated": self.last_updated,
        }


@dataclass
class EnforcedDisappearancesExtrajudicialEngineResult:
    agent: str = "Enforced Disappearances Extrajudicial Engine Agent"
    domain: str = "enforced_disappearances_extrajudicial"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_disappearances_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EnforcedDisappearancesExtrajudicialEntity] = field(default_factory=list)


def run_enforced_disappearances_extrajudicial_engine() -> EnforcedDisappearancesExtrajudicialEngineResult:
    entities = [
        EnforcedDisappearancesExtrajudicialEntity(
            entity_id="EDE-001",
            name="Mexique — 100 000+ Personnes Disparues, Cartels & Complicité État, Fosses Communes Massives",
            country="Mexique",
            sector="Disparitions Forcées Cartels & Impunité Institutionnelle",
            disappearance_rate_impunity_score=96.0,
            extrajudicial_killing_score=93.0,
            state_accountability_deficit_score=94.0,
            truth_justice_reparation_score=91.0,
            primary_pattern="disappearance_rate_impunity",
            key_signals=[
                "100 000+ personnes enregistrées disparues officiellement",
                "Fosses communes: plus de 4 000 découvertes 2006-2023",
                "Complicité documentée police et armée avec cartels",
                "Ayotzinapa: 43 étudiants — emblème de l'impunité systémique",
            ],
        ),
        EnforcedDisappearancesExtrajudicialEntity(
            entity_id="EDE-002",
            name="Syrie — Régime Assad: 150 000+ Détenus Disparus, Torture Industrielle, Charnel Saydnaya",
            country="Syrie",
            sector="Disparitions Forcées Régime Totalitaire",
            disappearance_rate_impunity_score=98.0,
            extrajudicial_killing_score=97.0,
            state_accountability_deficit_score=98.0,
            truth_justice_reparation_score=97.0,
            primary_pattern="state_accountability_deficit",
            key_signals=[
                "150 000+ personnes disparues dans prisons secrètes Assad",
                "Prison Saydnaya: exécutions industrielles 13 000+ morts estimés",
                "Photos César: 55 000 clichés de cadavres de détenus",
                "Aucun mécanisme reddition de comptes malgré preuves massives",
            ],
        ),
        EnforcedDisappearancesExtrajudicialEntity(
            entity_id="EDE-003",
            name="Philippines — Guerre Duterte Drogue: 7 000-30 000 Morts Extrajudiciaires 2016-2022",
            country="Philippines",
            sector="Exécutions Extrajudiciaires Guerre Drogue",
            disappearance_rate_impunity_score=89.0,
            extrajudicial_killing_score=93.0,
            state_accountability_deficit_score=88.0,
            truth_justice_reparation_score=86.0,
            primary_pattern="extrajudicial_killing",
            key_signals=[
                "7 000 morts officiels — ONG estiment 30 000 extrajudiciaires",
                "Tokhang: opérations police tirs à vue sans procédure",
                "Duterte renvoyé devant CPI pour crimes contre l'humanité 2023",
                "Témoins et famille victimes intimidés, peu de poursuites locales",
            ],
        ),
        EnforcedDisappearancesExtrajudicialEntity(
            entity_id="EDE-004",
            name="Égypte — 2 000+ Disparitions Forcées Depuis 2013, Détention Secrète, Sisi Impunité Totale",
            country="Égypte",
            sector="Disparitions Forcées Régime Autoritaire Post-Coup",
            disappearance_rate_impunity_score=86.0,
            extrajudicial_killing_score=82.0,
            state_accountability_deficit_score=87.0,
            truth_justice_reparation_score=83.0,
            primary_pattern="state_accountability_deficit",
            key_signals=[
                "2 000+ disparitions forcées documentées depuis coup 2013",
                "Détention secrète centres non officiels — torture systématique",
                "Opponents politiques, journalistes et défenseurs droits ciblés",
                "Loi anti-terrorisme 2015 légalise détention prolongée sans charge",
            ],
        ),
        EnforcedDisappearancesExtrajudicialEntity(
            entity_id="EDE-005",
            name="Colombie Post-FARC — 85 000+ Disparus Conflit, Faux Positifs Armée, JEP Vérité Partielle",
            country="Colombie",
            sector="Disparitions Post-Conflit & Justice Transitionnelle",
            disappearance_rate_impunity_score=55.0,
            extrajudicial_killing_score=53.0,
            state_accountability_deficit_score=50.0,
            truth_justice_reparation_score=48.0,
            primary_pattern="disappearance_rate_impunity",
            key_signals=[
                "85 000+ disparus conflit armé 1985-2016 — Unidad Búsqueda",
                "Faux positifs (falsos positivos): 6 400+ civils tués armée présentés combattants",
                "JEP justice spéciale pour la paix — verdicts partiels en cours",
                "Dissidences FARC continuent disparitions zones rurales post-accord",
            ],
        ),
        EnforcedDisappearancesExtrajudicialEntity(
            entity_id="EDE-006",
            name="Sri Lanka — 65 000-100 000 Disparus Guerre Civile, Lassana Manel Oubliées, Commission Vérité",
            country="Sri Lanka",
            sector="Disparitions Guerre Civile & Justice Transitionnelle Incomplète",
            disappearance_rate_impunity_score=53.0,
            extrajudicial_killing_score=50.0,
            state_accountability_deficit_score=55.0,
            truth_justice_reparation_score=49.0,
            primary_pattern="state_accountability_deficit",
            key_signals=[
                "65 000-100 000 Tamouls et Cingalais disparus conflit 1983-2009",
                "OMP Office of Missing Persons — mandat limité, lenteur process",
                "Familles Vanni attendent réponses 15+ ans pour leurs proches",
                "Gouvernement résiste à mécanisme international enquête crédible",
            ],
        ),
        EnforcedDisappearancesExtrajudicialEntity(
            entity_id="EDE-007",
            name="Argentine — Modèle CONADEP: 30 000 Disparus Junte 1976-1983, Procès Emblématiques",
            country="Argentine",
            sector="Justice Transitionnelle — Modèle de Référence",
            disappearance_rate_impunity_score=30.0,
            extrajudicial_killing_score=27.0,
            state_accountability_deficit_score=25.0,
            truth_justice_reparation_score=22.0,
            primary_pattern="truth_justice_reparation",
            key_signals=[
                "CONADEP 1984: premier modèle mondial commission vérité post-dictature",
                "Procès Junta militaire 1985 — condamnations historiques",
                "Mères de la Plaza de Mayo — référence mondiale résistance familles",
                "Nouveaux procès en cours (Lesa Humanidad) — justice continue 40 ans après",
            ],
        ),
        EnforcedDisappearancesExtrajudicialEntity(
            entity_id="EDE-008",
            name="Espagne — 114 000 Disparus Franquisme, Loi Mémoire Démocratique 2022, Amnistie 1977 Obstacle",
            country="Espagne",
            sector="Disparitions Historiques & Récupération Mémoire Tardive",
            disappearance_rate_impunity_score=14.0,
            extrajudicial_killing_score=11.0,
            state_accountability_deficit_score=18.0,
            truth_justice_reparation_score=15.0,
            primary_pattern="state_accountability_deficit",
            key_signals=[
                "114 000 personnes disparues guerre civile et franquisme 1936-1975",
                "Loi Amnistie 1977 — obstacle juridique poursuites franquistes",
                "Loi Mémoire Démocratique 2022 — exhumations financées État",
                "Valle de los Caídos renommé mais résistance politique de droite",
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

    return EnforcedDisappearancesExtrajudicialEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_disappearances_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_working_group_enforced_disappearances_2023",
            "amnesty_international_disappearances_report_2023",
            "human_rights_watch_extrajudicial_killings_2023",
            "icc_enforced_disappearances_jurisprudence_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_enforced_disappearances_extrajudicial_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_disappearances_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
