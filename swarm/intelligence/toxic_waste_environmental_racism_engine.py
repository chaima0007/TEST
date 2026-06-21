"""Toxic Waste & Environmental Racism Engine — Wave 167"""

from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class ToxicWasteEnvironmentalRacismEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    sub1_toxic_exposure_communities: float
    sub2_regulatory_failure: float
    sub3_health_impact: float
    sub4_remediation_absence: float
    primary_pattern: str = ""
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.sub1_toxic_exposure_communities * 0.30
            + self.sub2_regulatory_failure * 0.25
            + self.sub3_health_impact * 0.25
            + self.sub4_remediation_absence * 0.20,
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
        self.estimated_environmental_racism_index = round(self.composite_score / 100 * 10, 2)
        if not self.primary_pattern:
            scores = {
                "exposition_communautes_toxiques": self.sub1_toxic_exposure_communities,
                "defaillances_reglementaires": self.sub2_regulatory_failure,
                "impact_sante_documente": self.sub3_health_impact,
                "absence_depollution": self.sub4_remediation_absence,
            }
            self.primary_pattern = max(scores, key=scores.get)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "sub1_toxic_exposure_communities": self.sub1_toxic_exposure_communities,
            "sub2_regulatory_failure": self.sub2_regulatory_failure,
            "sub3_health_impact": self.sub3_health_impact,
            "sub4_remediation_absence": self.sub4_remediation_absence,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_environmental_racism_index": self.estimated_environmental_racism_index,
            "last_updated": self.last_updated,
        }

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Racisme environnemental documenté — {self.name} avec score composite {self.composite_score}/100 révélant une exposition différentielle aux toxiques fondée sur la race/classe, violant les Principes de Durban (2001) et les rapporteurs spéciaux ONU sur les déchets toxiques et les droits humains",
            f"Exposition communautés vulnérables ({self.sub1_toxic_exposure_communities}/100) — la concentration délibérée ou négligente de sites toxiques dans des zones habitées par des minorités constitue une violation du Principe 10 de la Déclaration de Rio et des droits à la santé (Article 12 PIDESC) et à un environnement sain",
            "Exiger l'application immédiate des Principes Directeurs ONU sur l'élimination des déchets dangereux et la dépollution des sites affectant les communautés vulnérables, conformément aux résolutions du Conseil des droits de l'homme 37/8 et 46/7 sur les droits humains et l'environnement",
        ]


@dataclass
class ToxicWasteEnvironmentalRacismEngineResult:
    agent: str = "Toxic Waste & Environmental Racism Engine Agent"
    domain: str = "toxic_waste_environmental_racism"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_environmental_racism_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ToxicWasteEnvironmentalRacismEntity] = field(default_factory=list)


def run_toxic_waste_environmental_racism_engine() -> ToxicWasteEnvironmentalRacismEngineResult:
    entities = [
        ToxicWasteEnvironmentalRacismEntity(
            entity_id="TWE-001",
            name="Nigeria Delta Niger — Shell Legacy, Ogoniland Pollué & UNEP Report Nettoyage 25 Ans",
            country="Nigeria",
            sector="Industrie pétrolière / communautés autochtones",
            sub1_toxic_exposure_communities=95.0,
            sub2_regulatory_failure=92.0,
            sub3_health_impact=90.0,
            sub4_remediation_absence=94.0,
            primary_pattern="absence_depollution",
        ),
        ToxicWasteEnvironmentalRacismEntity(
            entity_id="TWE-002",
            name="Inde Bhopal — Union Carbide Impunité 40 Ans, 20K Morts & Sol Contaminé",
            country="Inde",
            sector="Catastrophe industrielle / impunité corporative",
            sub1_toxic_exposure_communities=90.0,
            sub2_regulatory_failure=88.0,
            sub3_health_impact=92.0,
            sub4_remediation_absence=86.0,
            primary_pattern="impact_sante_documente",
        ),
        ToxicWasteEnvironmentalRacismEntity(
            entity_id="TWE-003",
            name="Ghana Agbogbloshie — Décharge E-Waste Mondiale, Enfants Brûlent Câbles & Métaux Lourds",
            country="Ghana",
            sector="Déchets électroniques / travail enfant",
            sub1_toxic_exposure_communities=85.0,
            sub2_regulatory_failure=82.0,
            sub3_health_impact=80.0,
            sub4_remediation_absence=84.0,
            primary_pattern="exposition_communautes_toxiques",
        ),
        ToxicWasteEnvironmentalRacismEntity(
            entity_id="TWE-004",
            name="USA Cancer Alley Louisiane — 150 Usines Pétrochimiques, Afro-Américains & EPA Inaction",
            country="États-Unis",
            sector="Racisme environnemental / communautés noires",
            sub1_toxic_exposure_communities=76.0,
            sub2_regulatory_failure=74.0,
            sub3_health_impact=78.0,
            sub4_remediation_absence=70.0,
            primary_pattern="impact_sante_documente",
        ),
        ToxicWasteEnvironmentalRacismEntity(
            entity_id="TWE-005",
            name="Chine Zones Pollution Industrielle — Villages Cancer, Déchets Métallurgie & Migration Forcée",
            country="Chine",
            sector="Industrie lourde / zones de sacrifice",
            sub1_toxic_exposure_communities=58.0,
            sub2_regulatory_failure=56.0,
            sub3_health_impact=60.0,
            sub4_remediation_absence=52.0,
            primary_pattern="impact_sante_documente",
        ),
        ToxicWasteEnvironmentalRacismEntity(
            entity_id="TWE-006",
            name="Bangladesh Tanneries Hazaribagh — Chrome Hexavalent, Travailleurs Malades & Relocalisation Lente",
            country="Bangladesh",
            sector="Industrie textile / travailleurs informels",
            sub1_toxic_exposure_communities=50.0,
            sub2_regulatory_failure=48.0,
            sub3_health_impact=52.0,
            sub4_remediation_absence=46.0,
            primary_pattern="impact_sante_documente",
        ),
        ToxicWasteEnvironmentalRacismEntity(
            entity_id="TWE-007",
            name="France Outre-Mer Chlordécone — Pesticide Banane Interdit, Antilles Contaminées & Cancer Prostate",
            country="France",
            sector="Agriculture coloniale / populations ultramarines",
            sub1_toxic_exposure_communities=32.0,
            sub2_regulatory_failure=30.0,
            sub3_health_impact=34.0,
            sub4_remediation_absence=26.0,
            primary_pattern="impact_sante_documente",
        ),
        ToxicWasteEnvironmentalRacismEntity(
            entity_id="TWE-008",
            name="Pays-Bas Droit Environnemental Avancé — Urgenda, Klimaatakkoord & PFAS Réglementation Stricte",
            country="Pays-Bas",
            sector="Modèle réglementation environnementale",
            sub1_toxic_exposure_communities=10.0,
            sub2_regulatory_failure=8.0,
            sub3_health_impact=9.0,
            sub4_remediation_absence=7.0,
            primary_pattern="exposition_communautes_toxiques",
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
    critical = [e for e in entities if e.risk_level == "critique"]
    alerts = [
        f"{e.name.split('—')[0].strip()}: {e.primary_pattern.replace('_', ' ')}"
        for e in critical
    ]

    return ToxicWasteEnvironmentalRacismEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_environmental_racism_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unep_ogoniland_environmental_assessment_2011",
            "amnesty_international_toxic_waste_human_rights_reports",
            "ejatlas_environmental_justice_atlas_cases",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_toxic_waste_environmental_racism_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_environmental_racism_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    dist = result.risk_distribution
    assert dist.get("critique", 0) == 4, f"Expected 4 critique, got {dist.get('critique', 0)}"
    assert dist.get("élevé", 0) == 2, f"Expected 2 élevé, got {dist.get('élevé', 0)}"
    assert dist.get("modéré", 0) == 1, f"Expected 1 modéré, got {dist.get('modéré', 0)}"
    assert dist.get("faible", 0) == 1, f"Expected 1 faible, got {dist.get('faible', 0)}"
    print("Distribution assertion PASSED: 4 critique / 2 élevé / 1 modéré / 1 faible")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score:.2f} [{e.risk_level}] {e.name[:60]}")
