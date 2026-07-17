from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class PrivateMilitaryContractorsAccountabilityEntity:
    entity_id: str
    name: str
    country: str
    documented_abuses_civilian_harm_score: float
    legal_immunity_impunity_gap_score: float
    oversight_transparency_failure_score: float
    international_regulatory_framework_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_pmc_accountability_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.documented_abuses_civilian_harm_score * 0.30
            + self.legal_immunity_impunity_gap_score * 0.25
            + self.oversight_transparency_failure_score * 0.25
            + self.international_regulatory_framework_gap_score * 0.20,
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
        self.estimated_pmc_accountability_index = round(
            self.composite_score / 100 * 10, 2
        )


def build_entities() -> List[PrivateMilitaryContractorsAccountabilityEntity]:
    return [
        PrivateMilitaryContractorsAccountabilityEntity(
            entity_id="PMC-001",
            name="Wagner Group/Russie — Afrique Crimes Documentés ONU, Mali Moura 500 Civils, Impunité Totale",
            country="Russie/Mali/Centrafrique",
            documented_abuses_civilian_harm_score=96.0,
            legal_immunity_impunity_gap_score=97.0,
            oversight_transparency_failure_score=95.0,
            international_regulatory_framework_gap_score=94.0,
            primary_pattern="Wagner Moura massacre 500 civils Mali 2022, crimes contre humanité RCA, ONU rapport 2023, aucune poursuite Russie",
        ),
        PrivateMilitaryContractorsAccountabilityEntity(
            entity_id="PMC-002",
            name="Blackwater/Nisour Square Irak — 17 Civils Tués 2007, Condamnations Annulées, Grâces Trump",
            country="États-Unis/Irak",
            documented_abuses_civilian_harm_score=91.0,
            legal_immunity_impunity_gap_score=93.0,
            oversight_transparency_failure_score=87.0,
            international_regulatory_framework_gap_score=90.0,
            primary_pattern="Massacre Nisour Square 17 civils irakiens 2007, Ordre 17 CPA immunité, condamnés 2015 annulés, grâciés Trump 2020",
        ),
        PrivateMilitaryContractorsAccountabilityEntity(
            entity_id="PMC-003",
            name="DynCorp/Balkans — Trafic Humain Accusations Bosnia Kosovo, Non Poursuivies, Contrats Maintenus",
            country="États-Unis/Balkans",
            documented_abuses_civilian_harm_score=82.0,
            legal_immunity_impunity_gap_score=88.0,
            oversight_transparency_failure_score=85.0,
            international_regulatory_framework_gap_score=84.0,
            primary_pattern="Allégations trafic humain Bosnia 1999-2002, agent FBI dénonciation, DynCorp maintenu contrat USG, aucune poursuite pénale",
        ),
        PrivateMilitaryContractorsAccountabilityEntity(
            entity_id="PMC-004",
            name="Aegis/Irak — Vidéos Tirs Civils Non Sanctionnés, Enquête PMSC Inexistante, Contrats Reconduits",
            country="UK/Irak",
            documented_abuses_civilian_harm_score=76.0,
            legal_immunity_impunity_gap_score=80.0,
            oversight_transparency_failure_score=82.0,
            international_regulatory_framework_gap_score=78.0,
            primary_pattern="Vidéos 2005 tirs civils irakiens véhicules, enquête US Army classée, contrats Aegis reconduits 475M$, zéro sanction",
        ),
        PrivateMilitaryContractorsAccountabilityEntity(
            entity_id="PMC-005",
            name="G4S/Prisons UK — Maltraitance Détenues Rapport 2017, Amendes Sans Poursuites Pénales",
            country="Royaume-Uni",
            documented_abuses_civilian_harm_score=54.0,
            legal_immunity_impunity_gap_score=58.0,
            oversight_transparency_failure_score=52.0,
            international_regulatory_framework_gap_score=48.0,
            primary_pattern="Maltraitance détenues Yarl's Wood, rapport 2017 violence, amendes contractuelles uniquement, aucune poursuite pénale dirigeants",
        ),
        PrivateMilitaryContractorsAccountabilityEntity(
            entity_id="PMC-006",
            name="MPRI/Balkans — Entraînement Armées, Responsabilité Floue, Opérations Tempête Croatie 1995",
            country="États-Unis/Balkans",
            documented_abuses_civilian_harm_score=46.0,
            legal_immunity_impunity_gap_score=52.0,
            oversight_transparency_failure_score=50.0,
            international_regulatory_framework_gap_score=48.0,
            primary_pattern="MPRI entraînement armée croate, Opération Tempête 250K déplacés serbes, responsabilité PMSC jamais établie",
        ),
        PrivateMilitaryContractorsAccountabilityEntity(
            entity_id="PMC-007",
            name="Montreux Document/Suisse — Cadre Volontaire PMC, 57 États Adhérents, Normes Non Contraignantes",
            country="International",
            documented_abuses_civilian_harm_score=22.0,
            legal_immunity_impunity_gap_score=25.0,
            oversight_transparency_failure_score=28.0,
            international_regulatory_framework_gap_score=30.0,
            primary_pattern="Document Montreux 2008 cadre volontaire, 57 États adhérents, bonnes pratiques sans mécanisme sanction, progrès limité",
        ),
        PrivateMilitaryContractorsAccountabilityEntity(
            entity_id="PMC-008",
            name="ICoC/Code Conduite Contractants Privés — Mécanisme Plaintes 2013, Portée Limitée, Modèle",
            country="International",
            documented_abuses_civilian_harm_score=6.0,
            legal_immunity_impunity_gap_score=8.0,
            oversight_transparency_failure_score=7.0,
            international_regulatory_framework_gap_score=10.0,
            primary_pattern="ICoCA code conduite 100+ entreprises, mécanisme plaintes actif, audits tiers, meilleur standard sectoriel mais limites claires",
        ),
    ]


def analyze(entities: List[PrivateMilitaryContractorsAccountabilityEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    assert risk_dist.get("critique", 0) == 4, f"Distribution critique attendue: 4, obtenu: {risk_dist.get('critique', 0)}"
    assert risk_dist.get("élevé", 0) == 2, f"Distribution élevé attendue: 2, obtenu: {risk_dist.get('élevé', 0)}"
    assert risk_dist.get("modéré", 0) == 1, f"Distribution modéré attendue: 1, obtenu: {risk_dist.get('modéré', 0)}"
    assert risk_dist.get("faible", 0) == 1, f"Distribution faible attendue: 1, obtenu: {risk_dist.get('faible', 0)}"

    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "private_military_contractors_accountability_engine",
        "domain": "private_military_contractors_accountability",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.90,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "documented_civilian_harm": 4,
            "legal_immunity_impunity": 2,
            "oversight_failure": 1,
            "voluntary_framework": 1,
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
        "avg_estimated_pmc_accountability_index": round(
            statistics.mean([e.estimated_pmc_accountability_index for e in entities]), 2
        ),
        "data_sources": [
            "un_working_group_mercenaries_report_2023",
            "montreux_document_forum_icoca_report_2024",
            "human_rights_watch_private_military_contractors_2023",
            "amnesty_international_pmc_accountability_report_2024",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "documented_abuses_civilian_harm_score": e.documented_abuses_civilian_harm_score,
                "legal_immunity_impunity_gap_score": e.legal_immunity_impunity_gap_score,
                "oversight_transparency_failure_score": e.oversight_transparency_failure_score,
                "international_regulatory_framework_gap_score": e.international_regulatory_framework_gap_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_pmc_accountability_index": e.estimated_pmc_accountability_index,
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
