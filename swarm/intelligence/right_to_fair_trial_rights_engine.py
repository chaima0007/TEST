from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#6366f1"


@dataclass
class RightToFairTrialRightsEntity:
    entity_id: str
    name: str
    country: str
    judicial_independence_score: float
    fair_trial_guarantee_score: float
    legal_aid_access_score: float
    arbitrary_detention_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_fair_trial_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.judicial_independence_score * 0.30
            + self.fair_trial_guarantee_score * 0.25
            + self.legal_aid_access_score * 0.25
            + self.arbitrary_detention_score * 0.20,
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
        self.estimated_right_to_fair_trial_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class RightToFairTrialRightsEngineResult:
    agent: str = "Right To Fair Trial Rights Engine Agent"
    domain: str = "right_to_fair_trial_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_fair_trial_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToFairTrialRightsEntity] = field(default_factory=list)


def run_right_to_fair_trial_rights_engine() -> RightToFairTrialRightsEngineResult:
    entities = [
        RightToFairTrialRightsEntity(
            entity_id="RFT-001",
            name="Arabie Saoudite — Cours Spéciales Terrorisme Sans Défenseurs, Aveux Sous Contrainte & Zéro Indépendance Judiciaire",
            country="Arabie Saoudite",
            judicial_independence_score=90.0,
            fair_trial_guarantee_score=89.0,
            legal_aid_access_score=88.0,
            arbitrary_detention_score=91.0,
            primary_pattern="arbitrary_detention_score",
        ),
        RightToFairTrialRightsEntity(
            entity_id="RFT-002",
            name="Chine — Justice Contrôlée par le PCC, Aveux Forcés Télévisés & Taux Condamnation 99,9%",
            country="Chine",
            judicial_independence_score=88.0,
            fair_trial_guarantee_score=87.0,
            legal_aid_access_score=85.0,
            arbitrary_detention_score=89.0,
            primary_pattern="judicial_independence_score",
        ),
        RightToFairTrialRightsEntity(
            entity_id="RFT-003",
            name="Russie — Tribunaux Politiques Kremlin, Procès Navalny & Taux Acquittement 0,3% Historique",
            country="Russie",
            judicial_independence_score=85.0,
            fair_trial_guarantee_score=84.0,
            legal_aid_access_score=82.0,
            arbitrary_detention_score=87.0,
            primary_pattern="fair_trial_guarantee_score",
        ),
        RightToFairTrialRightsEntity(
            entity_id="RFT-004",
            name="Biélorussie — Procès Politiques Loukachenko, Avocats Défenseurs Emprisonnés & Cours Secrètes",
            country="Biélorussie",
            judicial_independence_score=83.0,
            fair_trial_guarantee_score=82.0,
            legal_aid_access_score=80.0,
            arbitrary_detention_score=84.0,
            primary_pattern="judicial_independence_score",
        ),
        RightToFairTrialRightsEntity(
            entity_id="RFT-005",
            name="Iran — Tribunaux Révolutionnaires Islamiques, Condamnations à Mort Express & Avocats Exclus",
            country="Iran",
            judicial_independence_score=55.0,
            fair_trial_guarantee_score=54.0,
            legal_aid_access_score=50.0,
            arbitrary_detention_score=57.0,
            primary_pattern="arbitrary_detention_score",
        ),
        RightToFairTrialRightsEntity(
            entity_id="RFT-006",
            name="Turquie — Purge Judiciaire Post-2016, 4000 Juges Révoqués & Procès Journalistes Massifs",
            country="Turquie",
            judicial_independence_score=48.0,
            fair_trial_guarantee_score=47.0,
            legal_aid_access_score=44.0,
            arbitrary_detention_score=50.0,
            primary_pattern="judicial_independence_score",
        ),
        RightToFairTrialRightsEntity(
            entity_id="RFT-007",
            name="Inde — Lenteur Judiciaire Chronique, 50 Millions Affaires en Attente & Détention Préventive Prolongée",
            country="Inde",
            judicial_independence_score=30.0,
            fair_trial_guarantee_score=28.0,
            legal_aid_access_score=32.0,
            arbitrary_detention_score=29.0,
            primary_pattern="legal_aid_access_score",
        ),
        RightToFairTrialRightsEntity(
            entity_id="RFT-008",
            name="Danemark — Indépendance Judiciaire Référence Mondiale, Aide Juridique Universelle & Acquittements Respectés",
            country="Danemark",
            judicial_independence_score=11.0,
            fair_trial_guarantee_score=10.0,
            legal_aid_access_score=12.0,
            arbitrary_detention_score=10.0,
            primary_pattern="legal_aid_access_score",
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

    return RightToFairTrialRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_fair_trial_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_independence_judges_annual_report",
            "fair_trials_international_global_justice_barometer",
            "hrw_justice_system_violations_documentation",
            "amnesty_international_unfair_trials_report",
            "icj_judicial_independence_global_assessment",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_right_to_fair_trial_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
