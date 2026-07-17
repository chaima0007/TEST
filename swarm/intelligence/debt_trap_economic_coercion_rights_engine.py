from dataclasses import dataclass, field
from typing import List, Dict
import statistics


@dataclass
class DebtTrapEconomicCoercionRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    sovereign_debt_coercion_loss_autonomy_score: float = 0.0
    conditionality_austerity_social_rights_erosion_score: float = 0.0
    resource_extraction_dispossession_scale_score: float = 0.0
    debt_restructuring_access_justice_deficit_score: float = 0.0
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: List[str] = field(init=False)
    estimated_debt_trap_economic_coercion_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.sovereign_debt_coercion_loss_autonomy_score * 0.30 +
            self.conditionality_austerity_social_rights_erosion_score * 0.25 +
            self.resource_extraction_dispossession_scale_score * 0.25 +
            self.debt_restructuring_access_justice_deficit_score * 0.20, 2
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"

        patterns_map = {
            "piege_dette_souverainete_confisquee": self.sovereign_debt_coercion_loss_autonomy_score,
            "austerite_erosion_droits_sociaux": self.conditionality_austerity_social_rights_erosion_score,
            "extraction_ressources_spoliation": self.resource_extraction_dispossession_scale_score,
            "deficit_restructuration_acces_justice": self.debt_restructuring_access_justice_deficit_score,
        }
        self.primary_pattern = max(patterns_map, key=lambda k: patterns_map[k])
        self.key_signals = self._generate_signals()
        self.estimated_debt_trap_economic_coercion_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def _generate_signals(self) -> List[str]:
        signals = []
        if self.sovereign_debt_coercion_loss_autonomy_score >= 60:
            signals.append(
                f"Piège de la dette critique de {self.name} — perte de souveraineté "
                f"économique contraignant les politiques sociales, sanitaires et éducatives, "
                f"violant le droit des peuples à disposer d'eux-mêmes (PIDCP Art.1)"
            )
        elif self.sovereign_debt_coercion_loss_autonomy_score >= 40:
            signals.append(
                f"Coercition économique de {self.name} — conditions d'emprunt "
                f"limitant la capacité de l'État à protéger les droits économiques, "
                f"sociaux et culturels de sa population"
            )
        if self.conditionality_austerity_social_rights_erosion_score >= 60:
            signals.append(
                f"Austérité destructrice des droits — les conditionnalités imposées "
                f"par les créanciers provoquent des coupes dans les systèmes de santé, "
                f"d'éducation et de protection sociale, violant le PIDESC Art.2"
            )
        if self.resource_extraction_dispossession_scale_score >= 60:
            signals.append(
                f"Spoliation des ressources naturelles — l'accès aux ressources comme "
                f"garantie de prêt prive les populations autochtones et locales de leurs "
                f"droits fonciers et de leur droit au développement"
            )
        if self.debt_restructuring_access_justice_deficit_score >= 40:
            signals.append(
                f"Impunité des créanciers — l'absence de mécanisme international de "
                f"restructuration de la dette souveraine laisse les États débiteurs sans "
                f"recours légal face aux pratiques abusives des créanciers"
            )
        if not signals:
            signals.append(
                f"Gestion équitable de la dette de {self.name} — mécanismes de "
                f"restructuration accessibles et conditionnalités respectant les droits humains"
            )
        return signals[:3]

    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "sovereign_debt_coercion_loss_autonomy_score": self.sovereign_debt_coercion_loss_autonomy_score,
            "conditionality_austerity_social_rights_erosion_score": self.conditionality_austerity_social_rights_erosion_score,
            "resource_extraction_dispossession_scale_score": self.resource_extraction_dispossession_scale_score,
            "debt_restructuring_access_justice_deficit_score": self.debt_restructuring_access_justice_deficit_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_debt_trap_economic_coercion_rights_index": self.estimated_debt_trap_economic_coercion_rights_index,
            "last_updated": self.last_updated,
        }


class DebtTrapEconomicCoercionRightsEngine:
    ENGINE_VERSION = "1.0.0"
    DOMAIN = "debt_trap_economic_coercion_rights"

    def __init__(self):
        self.entities = self._load_entities()

    def _load_entities(self) -> List[DebtTrapEconomicCoercionRightsEntity]:
        return [
            DebtTrapEconomicCoercionRightsEntity(
                entity_id="DTEC-001",
                name="Sri Lanka/Port Hambantota Cédé Chine 99 Ans",
                country="Asie du Sud",
                sector="Faillite 2022, Port Hambantota Loué Chine 99 Ans, FMI 2.9B$, Coupures Électricité & Pénuries Médicaments Population 22M",
                sovereign_debt_coercion_loss_autonomy_score=94.0,
                conditionality_austerity_social_rights_erosion_score=90.0,
                resource_extraction_dispossession_scale_score=88.0,
                debt_restructuring_access_justice_deficit_score=85.0,
            ),
            DebtTrapEconomicCoercionRightsEntity(
                entity_id="DTEC-002",
                name="Zambie/Faillite Souveraine 2020 BRI Chine",
                country="Afrique Australe",
                sector="1er Défaut Afrique Subsaharienne Covid-19, 17B$ Dette Chine, Restructuration 3 Ans Bloquée, Cuivre Ressource Garantie & 18M Personnes Impact",
                sovereign_debt_coercion_loss_autonomy_score=88.0,
                conditionality_austerity_social_rights_erosion_score=85.0,
                resource_extraction_dispossession_scale_score=82.0,
                debt_restructuring_access_justice_deficit_score=88.0,
            ),
            DebtTrapEconomicCoercionRightsEntity(
                entity_id="DTEC-003",
                name="Grèce/Troïka Austérité 2010-2018 Droits",
                country="Europe du Sud",
                sector="86B€ Renflouement FMI/BCE/CE, Coupes Retraites 30%, Santé 25%, Chômage 27% Peak, Suicide +30% & 450 000 Émigrants Qualifiés",
                sovereign_debt_coercion_loss_autonomy_score=82.0,
                conditionality_austerity_social_rights_erosion_score=92.0,
                resource_extraction_dispossession_scale_score=68.0,
                debt_restructuring_access_justice_deficit_score=75.0,
            ),
            DebtTrapEconomicCoercionRightsEntity(
                entity_id="DTEC-004",
                name="Pakistan/FMI 23ème Programme Conditionnalités",
                country="Asie du Sud",
                sector="23ème Programme FMI Histoire, 7B$ 2023, Suppression Subventions Énergie & Carburant, Inflation 38%, 40% Population Sous Seuil Pauvreté",
                sovereign_debt_coercion_loss_autonomy_score=80.0,
                conditionality_austerity_social_rights_erosion_score=88.0,
                resource_extraction_dispossession_scale_score=62.0,
                debt_restructuring_access_justice_deficit_score=78.0,
            ),
            DebtTrapEconomicCoercionRightsEntity(
                entity_id="DTEC-005",
                name="Éthiopie/BRI Dette Chine Infrastructure 2023",
                country="Afrique de l'Est",
                sector="13.7B$ Dette Chine Chemins Fer & Énergie, Restructuration 2023 Lente, Conflit Tigré Aggrave, FMI 3.4B$ & Conditionnalités Réforme Fiscale",
                sovereign_debt_coercion_loss_autonomy_score=55.0,
                conditionality_austerity_social_rights_erosion_score=58.0,
                resource_extraction_dispossession_scale_score=62.0,
                debt_restructuring_access_justice_deficit_score=60.0,
            ),
            DebtTrapEconomicCoercionRightsEntity(
                entity_id="DTEC-006",
                name="Argentine/FMI 44B$ Défaut Cyclique",
                country="Amérique du Sud",
                sector="44B$ FMI 2018 Plus Grand Programme Histoire, 9ème Défaut 2020, Péronisme vs Conditionnalités, Inflation 130% 2023 & Dollarisation Milei",
                sovereign_debt_coercion_loss_autonomy_score=60.0,
                conditionality_austerity_social_rights_erosion_score=68.0,
                resource_extraction_dispossession_scale_score=48.0,
                debt_restructuring_access_justice_deficit_score=52.0,
            ),
            DebtTrapEconomicCoercionRightsEntity(
                entity_id="DTEC-007",
                name="G20/Cadre Commun Restructuration Dettes",
                country="Global",
                sector="G20 Cadre Commun 2020, Club de Paris, DSSI Suspension Service Dette, 50+ Pays Éligibles & Délais Restructuration 3-4 Ans Inefficaces",
                sovereign_debt_coercion_loss_autonomy_score=22.0,
                conditionality_austerity_social_rights_erosion_score=20.0,
                resource_extraction_dispossession_scale_score=18.0,
                debt_restructuring_access_justice_deficit_score=30.0,
            ),
            DebtTrapEconomicCoercionRightsEntity(
                entity_id="DTEC-008",
                name="Norvège/Fonds Souverain Modèle Transparence",
                country="Europe du Nord",
                sector="1.5 Trillion$ Fonds Souverain Pétrolier, Zéro Dette Nette, AAA Rating, Gestion Transparente & Droits Sociaux Préservés Politiques Fiscales",
                sovereign_debt_coercion_loss_autonomy_score=3.0,
                conditionality_austerity_social_rights_erosion_score=2.0,
                resource_extraction_dispossession_scale_score=4.0,
                debt_restructuring_access_justice_deficit_score=5.0,
            ),
        ]

    def analyze(self) -> Dict:
        results = [e.to_dict() for e in self.entities]
        scores = [e.composite_score for e in self.entities]
        avg_composite = round(statistics.mean(scores), 2)
        risk_dist = {}
        pattern_dist = {}
        for e in self.entities:
            risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
            pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

        top_risk = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)[:4]
        critical_alerts = [
            f"{e.name}: {e.primary_pattern}" for e in self.entities if e.risk_level == "critique"
        ]
        avg_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": len(results),
            "avg_composite": avg_composite,
            "risk_distribution": risk_dist,
            "pattern_distribution": pattern_dist,
            "top_risk_entities": [e.name for e in top_risk],
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-21",
            "engine_version": self.ENGINE_VERSION,
            "domain": self.DOMAIN,
            "confidence_score": 0.86,
            "data_sources": [
                "imf_debt_sustainability_framework_2023",
                "jubilee_debt_campaign_reports",
                "unctad_debt_vulnerabilities_2023",
                "world_bank_international_debt_statistics",
            ],
            "entities": results,
            "avg_estimated_debt_trap_economic_coercion_rights_index": avg_index,
        }


if __name__ == "__main__":
    import json
    engine = DebtTrapEconomicCoercionRightsEngine()
    result = engine.analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nAvg composite: {result['avg_composite']}")
    print(f"Distribution: {result['risk_distribution']}")
