from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ENGINE_VERSION = "1.0.0"

@dataclass
class GenocidePreventionAccountabilityEntity:
    entity_id: str
    name: str
    country: str
    mass_atrocity_risk_early_warning_score: float
    impunity_accountability_deficit_score: float
    incitement_hate_speech_dehumanization_score: float
    prevention_mechanism_international_response_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_genocide_prevention_accountability_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.mass_atrocity_risk_early_warning_score * 0.30
            + self.impunity_accountability_deficit_score * 0.25
            + self.incitement_hate_speech_dehumanization_score * 0.25
            + self.prevention_mechanism_international_response_gap_score * 0.20,
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
        self.estimated_genocide_prevention_accountability_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class GenocidePreventionAccountabilityEngineResult:
    agent: str = "Genocide Prevention Accountability Engine Agent"
    domain: str = "genocide_prevention_accountability"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.89
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = ENGINE_VERSION
    avg_estimated_genocide_prevention_accountability_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[GenocidePreventionAccountabilityEntity] = field(default_factory=list)


def run_genocide_prevention_accountability_engine() -> GenocidePreventionAccountabilityEngineResult:
    entities = [
        GenocidePreventionAccountabilityEntity(
            entity_id="GPA-001",
            name="Myanmar/Génocide Rohingya 2017 — ICJ Procédures Actives, CPI Enquête Ouverte, 700K Réfugiés Bangladesh, Déshumanisation Systémique 'Kafirs' & Impunité Tatmadaw Totale",
            country="Myanmar",
            mass_atrocity_risk_early_warning_score=88.0,
            impunity_accountability_deficit_score=92.0,
            incitement_hate_speech_dehumanization_score=90.0,
            prevention_mechanism_international_response_gap_score=85.0,
            primary_pattern="risque_atrocites_masse_actif",
        ),
        GenocidePreventionAccountabilityEntity(
            entity_id="GPA-002",
            name="Darfour/Soudan RSF 2023 — Atrocités Génocidaires Répétées, Villages Masla Brûlés, Rhétorique Ethnique Anti-Masalit & Conseil Sécurité Bloqué Russie Chine Veto",
            country="Soudan",
            mass_atrocity_risk_early_warning_score=90.0,
            impunity_accountability_deficit_score=85.0,
            incitement_hate_speech_dehumanization_score=88.0,
            prevention_mechanism_international_response_gap_score=82.0,
            primary_pattern="echec_prevention_internationale",
        ),
        GenocidePreventionAccountabilityEntity(
            entity_id="GPA-003",
            name="Gaza/Rapporteurs Spéciaux ONU 2024 — Qualification Génocide Débattue ICJ Mesures Provisoires, Blocus Humanitaire, Discours Déshumanisation Officiels & Veto USA CS",
            country="Palestine/Gaza",
            mass_atrocity_risk_early_warning_score=86.0,
            impunity_accountability_deficit_score=80.0,
            incitement_hate_speech_dehumanization_score=82.0,
            prevention_mechanism_international_response_gap_score=88.0,
            primary_pattern="echec_prevention_internationale",
        ),
        GenocidePreventionAccountabilityEntity(
            entity_id="GPA-004",
            name="Chine/Ouïghours — Convention Génocide Débat Juridique, 1M+ Détenus Xinjiang, Propagande Déshumanisation Islamophobie État & Aucun Mécanisme International Accès",
            country="Chine",
            mass_atrocity_risk_early_warning_score=82.0,
            impunity_accountability_deficit_score=85.0,
            incitement_hate_speech_dehumanization_score=88.0,
            prevention_mechanism_international_response_gap_score=78.0,
            primary_pattern="impunite_auteurs_crimes_masse",
        ),
        GenocidePreventionAccountabilityEntity(
            entity_id="GPA-005",
            name="Bosnie/Srebrenica — Génocide Jugé TPIY, Impunité Partielle Dirigeants RS Toujours Actifs, Négationnisme État Srpska & Mémorialisation Contestée 30 Ans Après",
            country="Bosnie-Herzégovine",
            mass_atrocity_risk_early_warning_score=45.0,
            impunity_accountability_deficit_score=68.0,
            incitement_hate_speech_dehumanization_score=55.0,
            prevention_mechanism_international_response_gap_score=58.0,
            primary_pattern="impunite_auteurs_crimes_masse",
        ),
        GenocidePreventionAccountabilityEntity(
            entity_id="GPA-006",
            name="Rwanda/Post-Génocide 1994 — Justice Gacaca 1.9M Dossiers, Mémoire Nationale Institutionnalisée, Reconciliation Partielle & Risques Régionalisation Résiduel Est RDC",
            country="Rwanda",
            mass_atrocity_risk_early_warning_score=25.0,
            impunity_accountability_deficit_score=58.0,
            incitement_hate_speech_dehumanization_score=50.0,
            prevention_mechanism_international_response_gap_score=52.0,
            primary_pattern="impunite_auteurs_crimes_masse",
        ),
        GenocidePreventionAccountabilityEntity(
            entity_id="GPA-007",
            name="Cambodge/ECCC — Procès Khmers Rouges Partiels, Accusés Vieillissants Décédés, Justice Limitée 3 Condamnations Définitives & Mémoire Institutionnelle Fragile Jeunes Générations",
            country="Cambodge",
            mass_atrocity_risk_early_warning_score=15.0,
            impunity_accountability_deficit_score=38.0,
            incitement_hate_speech_dehumanization_score=28.0,
            prevention_mechanism_international_response_gap_score=30.0,
            primary_pattern="impunite_auteurs_crimes_masse",
        ),
        GenocidePreventionAccountabilityEntity(
            entity_id="GPA-008",
            name="CPI/Cour Pénale Internationale — Modèle Responsabilité Structurellement Limité, 3 États Non-Membres Permanents CS, 44 Situations Enquêtées & Seuls Africains Condamnés Biais Perçu",
            country="International",
            mass_atrocity_risk_early_warning_score=5.0,
            impunity_accountability_deficit_score=8.0,
            incitement_hate_speech_dehumanization_score=6.0,
            prevention_mechanism_international_response_gap_score=12.0,
            primary_pattern="echec_prevention_internationale",
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

    return GenocidePreventionAccountabilityEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_genocide_prevention_accountability_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "genocide_watch_early_warning_indicators_2023",
            "un_office_genocide_prevention_report_2023",
            "international_criminal_court_annual_report_2023",
            "minority_rights_group_peoples_under_threat",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_genocide_prevention_accountability_engine()
    print(f"Agent: {result.agent}")
    print(f"Engine version: {result.engine_version}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Confidence score: {result.confidence_score}")
    print(f"Avg index: {result.avg_estimated_genocide_prevention_accountability_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print(f"Data sources: {result.data_sources}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — index={e.estimated_genocide_prevention_accountability_index}")
