from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class FairTrialDueProcessRightsEntity:
    entity_id: str
    name: str
    country: str
    military_secret_court_civilian_trial_score: float
    legal_representation_access_denial_score: float
    mass_trials_procedural_rights_violation_score: float
    torture_confession_evidence_admissibility_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_fair_trial_due_process_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.military_secret_court_civilian_trial_score * 0.30
            + self.legal_representation_access_denial_score * 0.25
            + self.mass_trials_procedural_rights_violation_score * 0.25
            + self.torture_confession_evidence_admissibility_score * 0.20,
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
        self.estimated_fair_trial_due_process_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class FairTrialDueProcessRightsEngineResult:
    agent: str = "Fair Trial Due Process Rights Engine Agent"
    domain: str = "fair_trial_due_process_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_fair_trial_due_process_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[FairTrialDueProcessRightsEntity] = field(default_factory=list)

def run_fair_trial_due_process_rights_engine() -> FairTrialDueProcessRightsEngineResult:
    entities = [
        FairTrialDueProcessRightsEntity(
            entity_id="FT-001",
            name="Chine — Tribunaux Militaires Dissidents Civils, Procès TV Aveux Forcés, Xinjiang Juridictions Secrètes & Avocats 709 Arrêtés",
            country="Asie du Nord-Est",
            military_secret_court_civilian_trial_score=96.0,
            legal_representation_access_denial_score=94.0,
            mass_trials_procedural_rights_violation_score=92.0,
            torture_confession_evidence_admissibility_score=95.0,
            primary_pattern="military_secret_court_civilian_trial",
        ),
        FairTrialDueProcessRightsEntity(
            entity_id="FT-002",
            name="Égypte/Sissi — 60K+ Prisonniers Politiques, Tribunaux Exception, Procès Masse 700+ en 1 Journée & Confessions Torture",
            country="Afrique du Nord",
            military_secret_court_civilian_trial_score=90.0,
            legal_representation_access_denial_score=88.0,
            mass_trials_procedural_rights_violation_score=94.0,
            torture_confession_evidence_admissibility_score=92.0,
            primary_pattern="mass_trials_procedural_rights_violation",
        ),
        FairTrialDueProcessRightsEntity(
            entity_id="FT-003",
            name="Arabie Saoudite — Cour Terrorisme Spéciale SCC Blogueurs Condamnés, Loujain al-Hathloul & Adultes Exécutés Crimes Mineurs",
            country="MENA",
            military_secret_court_civilian_trial_score=88.0,
            legal_representation_access_denial_score=85.0,
            mass_trials_procedural_rights_violation_score=82.0,
            torture_confession_evidence_admissibility_score=90.0,
            primary_pattern="military_secret_court_civilian_trial",
        ),
        FairTrialDueProcessRightsEntity(
            entity_id="FT-004",
            name="Russie/2022-2024 — Procès Anti-Guerre Fermés Public, Navalny Tribunaux Délocalisés Prison & 0 Acquittements Terrorisme",
            country="Europe de l'Est",
            military_secret_court_civilian_trial_score=85.0,
            legal_representation_access_denial_score=82.0,
            mass_trials_procedural_rights_violation_score=80.0,
            torture_confession_evidence_admissibility_score=78.0,
            primary_pattern="military_secret_court_civilian_trial",
        ),
        FairTrialDueProcessRightsEntity(
            entity_id="FT-005",
            name="Turquie — Post-Coup 2016: 150K+ Poursuites, Juges Purges, Tribunaux Pénaux Paix TPP Contestés & KHK Décrets Urgence",
            country="Moyen-Orient",
            military_secret_court_civilian_trial_score=58.0,
            legal_representation_access_denial_score=55.0,
            mass_trials_procedural_rights_violation_score=62.0,
            torture_confession_evidence_admissibility_score=52.0,
            primary_pattern="mass_trials_procedural_rights_violation",
        ),
        FairTrialDueProcessRightsEntity(
            entity_id="FT-006",
            name="Cambodge — ECCC Héritage KR = Progrès, Mais Hun Sen = Procès Opposition Kim Sokha & Liberté Conditionnelle Imposée",
            country="Asie du Sud-Est",
            military_secret_court_civilian_trial_score=52.0,
            legal_representation_access_denial_score=48.0,
            mass_trials_procedural_rights_violation_score=50.0,
            torture_confession_evidence_admissibility_score=45.0,
            primary_pattern="legal_representation_access_denial",
        ),
        FairTrialDueProcessRightsEntity(
            entity_id="FT-007",
            name="Mexique — Cartels Corrompent Tribunaux, 95% Impunité Homicides & Femmes Victimes Féminicide Sans Justice",
            country="Amérique Centrale",
            military_secret_court_civilian_trial_score=28.0,
            legal_representation_access_denial_score=32.0,
            mass_trials_procedural_rights_violation_score=25.0,
            torture_confession_evidence_admissibility_score=30.0,
            primary_pattern="legal_representation_access_denial",
        ),
        FairTrialDueProcessRightsEntity(
            entity_id="FT-008",
            name="Allemagne/Rechtsstaat — Indépendance Judiciaire Constitutionnelle, Bundesverfassungsgericht Puissant & Acquittements Possibles",
            country="Europe de l'Ouest",
            military_secret_court_civilian_trial_score=3.0,
            legal_representation_access_denial_score=4.0,
            mass_trials_procedural_rights_violation_score=3.0,
            torture_confession_evidence_admissibility_score=4.0,
            primary_pattern="military_secret_court_civilian_trial",
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

    return FairTrialDueProcessRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_fair_trial_due_process_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "fair_trials_international_justice_index_2023",
            "amnesty_international_fair_trial_violations_2023",
            "human_rights_watch_arbitrary_detention_2023",
            "un_special_rapporteur_independence_judges_2023",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_fair_trial_due_process_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_fair_trial_due_process_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
