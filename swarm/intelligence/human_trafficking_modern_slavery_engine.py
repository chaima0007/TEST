from dataclasses import dataclass, field
from typing import List, Dict, Optional
import statistics


@dataclass
class HumanTraffickingModernSlaveryEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    trafficking_victim_scale_vulnerability_score: float = 0.0
    labor_exploitation_debt_bondage_severity_score: float = 0.0
    sex_trafficking_prosecution_impunity_score: float = 0.0
    victim_identification_support_deficit_score: float = 0.0
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: List[str] = field(init=False)
    estimated_human_trafficking_modern_slavery_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.trafficking_victim_scale_vulnerability_score * 0.30 +
            self.labor_exploitation_debt_bondage_severity_score * 0.25 +
            self.sex_trafficking_prosecution_impunity_score * 0.25 +
            self.victim_identification_support_deficit_score * 0.20, 2
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
            "trafic_victimes_echelle_massive": self.trafficking_victim_scale_vulnerability_score,
            "exploitation_travail_servitude_dette": self.labor_exploitation_debt_bondage_severity_score,
            "trafic_sexuel_impunite_poursuite": self.sex_trafficking_prosecution_impunity_score,
            "deficit_identification_soutien_victimes": self.victim_identification_support_deficit_score,
        }
        self.primary_pattern = max(patterns_map, key=lambda k: patterns_map[k])

        self.key_signals = self._generate_signals()
        self.estimated_human_trafficking_modern_slavery_index = round(
            self.composite_score / 100 * 10, 2
        )

    def _generate_signals(self) -> List[str]:
        signals = []
        if self.trafficking_victim_scale_vulnerability_score >= 60:
            signals.append(
                f"Trafic humain massif de {self.name} — des millions de personnes victimes "
                f"de traite, exploitées dans les secteurs du travail forcé, de la prostitution "
                f"et des mariages forcés, en violation de l'article 4 DUDH et du Protocole de Palerme"
            )
        elif self.trafficking_victim_scale_vulnerability_score >= 40:
            signals.append(
                f"Vulnérabilité élevée au trafic de {self.name} — populations en situation "
                f"de pauvreté extrême, conflit ou déplacement exposées aux réseaux de traite "
                f"qui exploitent l'absence de protection légale et sociale"
            )
        if self.labor_exploitation_debt_bondage_severity_score >= 60:
            signals.append(
                f"Servitude pour dettes systémique — l'exploitation par la dette constitue "
                f"une forme d'esclavage moderne reconnue par le droit international, piégeant "
                f"les travailleurs migrants dans des conditions de travail forcé sans issue légale"
            )
        if self.sex_trafficking_prosecution_impunity_score >= 60:
            signals.append(
                f"Impunité du trafic sexuel — le faible taux de poursuites judiciaires et "
                f"de condamnations pour trafic à des fins d'exploitation sexuelle renforce "
                f"la normalisation de cette violence et décourage les victimes de témoigner"
            )
        if self.victim_identification_support_deficit_score >= 40:
            signals.append(
                f"Déficit de protection des victimes — l'absence de mécanismes d'identification "
                f"et de soutien aux victimes conduit à leur re-victimisation par les autorités, "
                f"notamment via leur criminalisation plutôt que leur protection"
            )
        if not signals:
            signals.append(
                f"Engagement relatif contre le trafic humain de {self.name} — "
                f"mécanismes partiels d'identification des victimes et de poursuites judiciaires"
            )
        return signals[:3]

    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "trafficking_victim_scale_vulnerability_score": self.trafficking_victim_scale_vulnerability_score,
            "labor_exploitation_debt_bondage_severity_score": self.labor_exploitation_debt_bondage_severity_score,
            "sex_trafficking_prosecution_impunity_score": self.sex_trafficking_prosecution_impunity_score,
            "victim_identification_support_deficit_score": self.victim_identification_support_deficit_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_human_trafficking_modern_slavery_index": self.estimated_human_trafficking_modern_slavery_index,
            "last_updated": self.last_updated,
        }


class HumanTraffickingModernSlaveryEngine:
    ENGINE_VERSION = "1.0.0"
    DOMAIN = "human_trafficking_modern_slavery"

    def __init__(self):
        self.entities = self._load_entities()

    def _load_entities(self) -> List[HumanTraffickingModernSlaveryEntity]:
        return [
            HumanTraffickingModernSlaveryEntity(
                entity_id="HTMS-001",
                name="Corée du Nord/Travail Forcé Exporté 100 000",
                country="Asie du Nord-Est",
                sector="100 000 Travailleurs Exportés Qatar/Russie/Chine, Salaires Confisqués État, Camp Kwalliso Travail Forcé & Rapport ONU 2014 Crimes Contre Humanité",
                trafficking_victim_scale_vulnerability_score=96.0,
                labor_exploitation_debt_bondage_severity_score=98.0,
                sex_trafficking_prosecution_impunity_score=88.0,
                victim_identification_support_deficit_score=99.0,
            ),
            HumanTraffickingModernSlaveryEntity(
                entity_id="HTMS-002",
                name="Qatar/Kafala 1.8M Travailleurs Migrants",
                country="MENA",
                sector="Système Kafala Confiscation Passeports, 1.8M Travailleurs Migrants, Décès Chantiers Mondial 2022 & Walk Free Index Score Élevé",
                trafficking_victim_scale_vulnerability_score=85.0,
                labor_exploitation_debt_bondage_severity_score=92.0,
                sex_trafficking_prosecution_impunity_score=78.0,
                victim_identification_support_deficit_score=88.0,
            ),
            HumanTraffickingModernSlaveryEntity(
                entity_id="HTMS-003",
                name="Inde/Esclavage Moderne 8M Walk Free Index",
                country="Asie du Sud",
                sector="8 Millions Esclaves Modernes Walk Free 2023, Servitude Castes, Travail Enfants Bonded Labor & Secteur Agricole Exploitation",
                trafficking_victim_scale_vulnerability_score=88.0,
                labor_exploitation_debt_bondage_severity_score=90.0,
                sex_trafficking_prosecution_impunity_score=82.0,
                victim_identification_support_deficit_score=78.0,
            ),
            HumanTraffickingModernSlaveryEntity(
                entity_id="HTMS-004",
                name="Myanmar/Trafic Centres Arnaque Cyber Scam",
                country="Asie du Sud-Est",
                sector="100 000+ Trafiqués Centres Scam Frontières Thaïlande, 80 000 Réseaux Karen National Army, Electrocution & Crimes Cyber Forcés",
                trafficking_victim_scale_vulnerability_score=90.0,
                labor_exploitation_debt_bondage_severity_score=88.0,
                sex_trafficking_prosecution_impunity_score=85.0,
                victim_identification_support_deficit_score=92.0,
            ),
            HumanTraffickingModernSlaveryEntity(
                entity_id="HTMS-005",
                name="Russie/Trafic Femmes Europe Est Post-URSS",
                country="Europe de l'Est",
                sector="Principal Pays Origine Trafic Sexuel Europe, 2ème Mondiale Après Mexique, Réseaux Organisés & Faible Taux Condamnation",
                trafficking_victim_scale_vulnerability_score=50.0,
                labor_exploitation_debt_bondage_severity_score=48.0,
                sex_trafficking_prosecution_impunity_score=58.0,
                victim_identification_support_deficit_score=52.0,
            ),
            HumanTraffickingModernSlaveryEntity(
                entity_id="HTMS-006",
                name="Mexique/Trafic Fentanyl Cartels Exploitation",
                country="Amérique Centrale",
                sector="Cartels Sinaloa & CJNG Diversification Trafic Humain, Femmes Migrantes Frontière, Exploitation Sexuelle & Travail Forcé Cannabis",
                trafficking_victim_scale_vulnerability_score=55.0,
                labor_exploitation_debt_bondage_severity_score=50.0,
                sex_trafficking_prosecution_impunity_score=52.0,
                victim_identification_support_deficit_score=48.0,
            ),
            HumanTraffickingModernSlaveryEntity(
                entity_id="HTMS-007",
                name="ONU/Protocole Palerme & UNODC Monitoring",
                country="Global",
                sector="Protocole Palerme 2000 Ratifié 180+ États, UNODC Rapport Mondial 2022, 49 000 Victimes Identifiées & 90 000 $ Profit/Victime/An",
                trafficking_victim_scale_vulnerability_score=22.0,
                labor_exploitation_debt_bondage_severity_score=20.0,
                sex_trafficking_prosecution_impunity_score=25.0,
                victim_identification_support_deficit_score=28.0,
            ),
            HumanTraffickingModernSlaveryEntity(
                entity_id="HTMS-008",
                name="UE/Directive Anti-Traite 2011 & Mécanisme NRM",
                country="Europe",
                sector="Directive 2011/36/EU Anti-Traite, NRM National Referral Mechanism, GRETA Monitoring & Plan Action 2021-2025 Prévention",
                trafficking_victim_scale_vulnerability_score=5.0,
                labor_exploitation_debt_bondage_severity_score=6.0,
                sex_trafficking_prosecution_impunity_score=8.0,
                victim_identification_support_deficit_score=10.0,
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
            "confidence_score": 0.89,
            "data_sources": [
                "unodc_global_report_trafficking_2022",
                "walk_free_global_slavery_index_2023",
                "us_state_dept_tip_report_2023",
                "ilo_forced_labour_statistics_2022",
            ],
            "entities": results,
            "avg_estimated_human_trafficking_modern_slavery_index": avg_index,
        }


if __name__ == "__main__":
    import json
    engine = HumanTraffickingModernSlaveryEngine()
    result = engine.analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nAvg composite: {result['avg_composite']}")
    print(f"Distribution: {result['risk_distribution']}")
