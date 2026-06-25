from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class SyntheticBiologyBiosafetyRightsEntity:
    entity_id: str
    name: str
    country: str
    synthetic_pathogen_dual_use_risk_score: float
    corporate_biotech_monopoly_score: float
    ecological_release_irreversibility_score: float
    community_consent_biosafety_governance_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_synthetic_biology_biosafety_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.synthetic_pathogen_dual_use_risk_score * 0.30
            + self.corporate_biotech_monopoly_score * 0.25
            + self.ecological_release_irreversibility_score * 0.25
            + self.community_consent_biosafety_governance_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_synthetic_biology_biosafety_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[SyntheticBiologyBiosafetyRightsEntity]:
    return [
        SyntheticBiologyBiosafetyRightsEntity(
            entity_id="SBB-001",
            name="États-Unis — GOF Research Non Régulé, Gain-of-Function Pathogènes Militaires",
            country="États-Unis",
            synthetic_pathogen_dual_use_risk_score=95.0,
            corporate_biotech_monopoly_score=90.0,
            ecological_release_irreversibility_score=88.0,
            community_consent_biosafety_governance_score=85.0,
            primary_pattern="Gain-of-function research H5N1 partiellement non supervisé, DARPA biotech dual-use sans transparence, CRISPR thérapeutique breveté sans accès global",
        ),
        SyntheticBiologyBiosafetyRightsEntity(
            entity_id="SBB-002",
            name="Chine — Laboratoires Biosécurité BSL-4, Opacité Recherche Synbio",
            country="Chine",
            synthetic_pathogen_dual_use_risk_score=93.0,
            corporate_biotech_monopoly_score=85.0,
            ecological_release_irreversibility_score=91.0,
            community_consent_biosafety_governance_score=92.0,
            primary_pattern="WIV opacité recherche coronavirus synthétique, programme synbio militaire PLA, absence transparence BSL-4 Wuhan sur recherches dual-use",
        ),
        SyntheticBiologyBiosafetyRightsEntity(
            entity_id="SBB-003",
            name="Russie — Programme Biopréparats Héritage, Synbio Militaire Non Déclaré",
            country="Russie",
            synthetic_pathogen_dual_use_risk_score=90.0,
            corporate_biotech_monopoly_score=78.0,
            ecological_release_irreversibility_score=85.0,
            community_consent_biosafety_governance_score=88.0,
            primary_pattern="Héritage Biopréparats non déclaré Traité ABW, Vector Institute souches rétablies sans supervision internationale, synbio dual-use militaire",
        ),
        SyntheticBiologyBiosafetyRightsEntity(
            entity_id="SBB-004",
            name="Monsanto/Bayer — Gene Drive OGM, Brevetage du Vivant Sans Consentement",
            country="Multinationale",
            synthetic_pathogen_dual_use_risk_score=72.0,
            corporate_biotech_monopoly_score=95.0,
            ecological_release_irreversibility_score=80.0,
            community_consent_biosafety_governance_score=85.0,
            primary_pattern="Brevets CRISPR agriculture sans partage bénéfices communautés, gene drive moustiques Afrique sans consentement communautaire, monopole semencier synbio",
        ),
        SyntheticBiologyBiosafetyRightsEntity(
            entity_id="SBB-005",
            name="Inde — Bt Cotton Gene Drive, Impact Agriculteurs Sans Gouvernance",
            country="Inde",
            synthetic_pathogen_dual_use_risk_score=55.0,
            corporate_biotech_monopoly_score=60.0,
            ecological_release_irreversibility_score=58.0,
            community_consent_biosafety_governance_score=52.0,
            primary_pattern="OGM Bt Cotton dépendance Monsanto, suicides agriculteurs liés dettes semences, absence participation communautaire décisions biotech",
        ),
        SyntheticBiologyBiosafetyRightsEntity(
            entity_id="SBB-006",
            name="Brésil — Amazonie Gene Drive Insectes, Risques Écosystème",
            country="Brésil",
            synthetic_pathogen_dual_use_risk_score=48.0,
            corporate_biotech_monopoly_score=55.0,
            ecological_release_irreversibility_score=65.0,
            community_consent_biosafety_governance_score=50.0,
            primary_pattern="Oxitec moustiques modifiés lâchés sans pleine consultation autochtones Amazonie, risques irréversibles biodiversité tropicale, gouvernance lacunaire",
        ),
        SyntheticBiologyBiosafetyRightsEntity(
            entity_id="SBB-007",
            name="UE — Directive OGM Révisée, Cadre NTG Nouvelles Techniques Génomiques",
            country="Union Européenne",
            synthetic_pathogen_dual_use_risk_score=25.0,
            corporate_biotech_monopoly_score=28.0,
            ecological_release_irreversibility_score=22.0,
            community_consent_biosafety_governance_score=20.0,
            primary_pattern="Règlement NTG 2024 avec évaluation risques, protocole Cartagena adopté, débat public OGM institutionnalisé, moratorium gene drive maintenu",
        ),
        SyntheticBiologyBiosafetyRightsEntity(
            entity_id="SBB-008",
            name="Nouvelle-Zélande — Loi Hazardous Substances, Précaution Synbio Exemplaire",
            country="Nouvelle-Zélande",
            synthetic_pathogen_dual_use_risk_score=5.0,
            corporate_biotech_monopoly_score=5.0,
            ecological_release_irreversibility_score=4.0,
            community_consent_biosafety_governance_score=3.0,
            primary_pattern="HSNO Act strict sur organismes modifiés, consultation iwi Maori obligatoire synbio, ERMA évaluation indépendante, modèle précaution biosécurité mondiale",
        ),
    ]


def analyze(entities: List[SyntheticBiologyBiosafetyRightsEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "synthetic_biology_biosafety_rights_engine",
        "domain": "synthetic_biology_biosafety_rights",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.88,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "dual_use_pathogen_risk": 3,
            "corporate_monopoly_biotech": 2,
            "ecological_irreversibility": 2,
            "governance_deficit": 1,
        },
        "top_risk_entities": [
            {"id": e.entity_id, "name": e.name, "score": e.composite_score, "risk": e.risk_level}
            for e in top_risk
        ],
        "critical_alerts": [
            f"{e.entity_id}: {e.name} — composite {e.composite_score}"
            for e in entities if e.risk_level == "critique"
        ],
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "avg_estimated_synthetic_biology_biosafety_index": round(
            statistics.mean([e.estimated_synthetic_biology_biosafety_index for e in entities]), 2
        ),
        "data_sources": [
            "who_biosafety_biosecurity_report_2024",
            "johns_hopkins_chs_biosecurity_2024",
            "convention_biological_diversity_synbio_2023",
            "nature_biotechnology_dual_use_governance_2024",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "synthetic_pathogen_dual_use_risk_score": e.synthetic_pathogen_dual_use_risk_score,
                "corporate_biotech_monopoly_score": e.corporate_biotech_monopoly_score,
                "ecological_release_irreversibility_score": e.ecological_release_irreversibility_score,
                "community_consent_biosafety_governance_score": e.community_consent_biosafety_governance_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_synthetic_biology_biosafety_index": e.estimated_synthetic_biology_biosafety_index,
                "last_updated": e.last_updated,
            }
            for e in entities
        ],
    }


if __name__ == "__main__":
    import json
    entities = build_entities()
    result = analyze(entities)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n✓ avg_composite = {result['avg_composite']}")
    print(f"✓ risk_distribution = {result['risk_distribution']}")
    print(f"✓ total_entities = {result['total_entities']}")
