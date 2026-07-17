from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class WhistleblowerLeakerProtectionEntity:
    entity_id: str
    name: str
    country: str
    retaliation_prosecution_espionage_severity_score: float
    source_journalist_surveillance_exposure_scale_score: float
    whistleblower_legal_protection_absence_score: float
    public_interest_disclosure_mechanism_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_whistleblower_leaker_protection_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.retaliation_prosecution_espionage_severity_score * 0.30
            + self.source_journalist_surveillance_exposure_scale_score * 0.25
            + self.whistleblower_legal_protection_absence_score * 0.25
            + self.public_interest_disclosure_mechanism_deficit_gap_score * 0.20,
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
        self.estimated_whistleblower_leaker_protection_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class WhistleblowerLeakerProtectionEngineResult:
    entities: List[WhistleblowerLeakerProtectionEntity]
    avg_composite: float
    distribution: dict
    data_sources: List[str]
    agent: str


def run_whistleblower_leaker_protection_engine() -> WhistleblowerLeakerProtectionEngineResult:
    entities = [
        WhistleblowerLeakerProtectionEntity(
            entity_id="WLP-001",
            name="USA/Snowden — NSA PRISM Révélé 2013, Snowden Exilé Russie, Manning 35 Ans Prison & Espionage Act Poursuite 14 Lanceurs",
            country="USA",
            retaliation_prosecution_espionage_severity_score=94.0,
            source_journalist_surveillance_exposure_scale_score=92.0,
            whistleblower_legal_protection_absence_score=93.0,
            public_interest_disclosure_mechanism_deficit_gap_score=91.0,
            primary_pattern="retaliation_prosecution_espionage_severity",
        ),
        WhistleblowerLeakerProtectionEntity(
            entity_id="WLP-002",
            name="UK/Julian Assange — WikiLeaks Extradition 14 Ans, Section 23 Official Secrets, Journalistes GCHQ Espionnés & Guardian Disques Durs Détruits",
            country="UK",
            retaliation_prosecution_espionage_severity_score=90.0,
            source_journalist_surveillance_exposure_scale_score=92.0,
            whistleblower_legal_protection_absence_score=88.0,
            public_interest_disclosure_mechanism_deficit_gap_score=90.0,
            primary_pattern="source_journalist_surveillance_exposure_scale",
        ),
        WhistleblowerLeakerProtectionEntity(
            entity_id="WLP-003",
            name="Russie/FSB — Système Filtrage Internet, Journalistes Empoisonnés/Tués, Sources Livraison FSB & Lanceurs Trahison 20 Ans",
            country="Russie",
            retaliation_prosecution_espionage_severity_score=87.0,
            source_journalist_surveillance_exposure_scale_score=85.0,
            whistleblower_legal_protection_absence_score=88.0,
            public_interest_disclosure_mechanism_deficit_gap_score=86.0,
            primary_pattern="retaliation_prosecution_espionage_severity",
        ),
        WhistleblowerLeakerProtectionEntity(
            entity_id="WLP-004",
            name="Chine/Cybersec — Lois Secrets État Larges, Journalistes Weibo Arrêtés, VPN Criminalisé & Dissident Chiffrement 10 Ans",
            country="Chine",
            retaliation_prosecution_espionage_severity_score=84.0,
            source_journalist_surveillance_exposure_scale_score=82.0,
            whistleblower_legal_protection_absence_score=83.0,
            public_interest_disclosure_mechanism_deficit_gap_score=85.0,
            primary_pattern="whistleblower_legal_protection_absence",
        ),
        WhistleblowerLeakerProtectionEntity(
            entity_id="WLP-005",
            name="France/HADOPI — Secret Défense Journalistes Visés, Terry Gontier Affaire, DGSI Sources & Loi 2019 Renseignement Sources Affaiblies",
            country="France",
            retaliation_prosecution_espionage_severity_score=55.0,
            source_journalist_surveillance_exposure_scale_score=54.0,
            whistleblower_legal_protection_absence_score=57.0,
            public_interest_disclosure_mechanism_deficit_gap_score=56.0,
            primary_pattern="source_journalist_surveillance_exposure_scale",
        ),
        WhistleblowerLeakerProtectionEntity(
            entity_id="WLP-006",
            name="Inde/OSA — Official Secrets Act Colonial 1923, RTI Activistes Tués 80, Journalistes Séditieux Arrêtés & UAPA Lanceurs",
            country="Inde",
            retaliation_prosecution_espionage_severity_score=52.0,
            source_journalist_surveillance_exposure_scale_score=51.0,
            whistleblower_legal_protection_absence_score=53.0,
            public_interest_disclosure_mechanism_deficit_gap_score=54.0,
            primary_pattern="public_interest_disclosure_mechanism_deficit_gap",
        ),
        WhistleblowerLeakerProtectionEntity(
            entity_id="WLP-007",
            name="CPJ/RSF — Comité Protection Journalistes, Reporters Sans Frontières Sources, Government Accountability Project & Whistleblower Aid",
            country="Global",
            retaliation_prosecution_espionage_severity_score=27.0,
            source_journalist_surveillance_exposure_scale_score=26.0,
            whistleblower_legal_protection_absence_score=28.0,
            public_interest_disclosure_mechanism_deficit_gap_score=25.0,
            primary_pattern="public_interest_disclosure_mechanism_deficit_gap",
        ),
        WhistleblowerLeakerProtectionEntity(
            entity_id="WLP-008",
            name="ONU/PACE — Résolution ONU Lanceurs Alerte 2015, PACE Recommandation 2006, Principes Tshwane & Standards Juridiques Protection",
            country="Global",
            retaliation_prosecution_espionage_severity_score=4.0,
            source_journalist_surveillance_exposure_scale_score=4.0,
            whistleblower_legal_protection_absence_score=4.0,
            public_interest_disclosure_mechanism_deficit_gap_score=4.0,
            primary_pattern="whistleblower_legal_protection_absence",
        ),
    ]

    scores = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(scores), 2)

    distribution = {}
    for e in entities:
        distribution[e.risk_level] = distribution.get(e.risk_level, 0) + 1

    return WhistleblowerLeakerProtectionEngineResult(
        entities=entities,
        avg_composite=avg_composite,
        distribution=distribution,
        data_sources=[
            "government_accountability_project_report",
            "cpj_journalist_source_protection_report",
            "un_special_rapporteur_whistleblower_protection",
        ],
        agent="Whistleblower Leaker Protection Engine Agent",
    )


if __name__ == "__main__":
    result = run_whistleblower_leaker_protection_engine()
    print(f"Agent: {result.agent}")
    print(f"avg_composite: {result.avg_composite}")
    print(f"Distribution: {result.distribution}")
    print()
    for e in result.entities:
        print(
            f"  [{e.entity_id}] {e.risk_level.upper():8s} | composite={e.composite_score:5.2f} | index={e.estimated_whistleblower_leaker_protection_index} | {e.name[:60]}"
        )
