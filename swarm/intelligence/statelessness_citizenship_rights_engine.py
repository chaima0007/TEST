from dataclasses import dataclass, field
from typing import List, Dict, Optional
import statistics


@dataclass
class StatelessnessCitizenshipRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    stateless_population_scale_severity_score: float = 0.0
    citizenship_deprivation_arbitrariness_score: float = 0.0
    documentation_access_birth_registration_deficit_score: float = 0.0
    stateless_rights_protection_mechanism_gap_score: float = 0.0
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: List[str] = field(init=False)
    estimated_statelessness_citizenship_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.stateless_population_scale_severity_score * 0.30 +
            self.citizenship_deprivation_arbitrariness_score * 0.25 +
            self.documentation_access_birth_registration_deficit_score * 0.25 +
            self.stateless_rights_protection_mechanism_gap_score * 0.20, 2
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
            "apatridie_population_masse": self.stateless_population_scale_severity_score,
            "privation_citoyennete_arbitraire": self.citizenship_deprivation_arbitrariness_score,
            "deficit_enregistrement_naissance": self.documentation_access_birth_registration_deficit_score,
            "absence_mecanisme_protection_apatrides": self.stateless_rights_protection_mechanism_gap_score,
        }
        self.primary_pattern = max(patterns_map, key=lambda k: patterns_map[k])

        self.key_signals = self._generate_signals()
        self.estimated_statelessness_citizenship_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def _generate_signals(self) -> List[str]:
        signals = []
        if self.stateless_population_scale_severity_score >= 60:
            signals.append(
                f"Apatridie massive de {self.name} — des centaines de milliers de personnes "
                f"privées de nationalité, sans accès à l'éducation, aux soins, à l'emploi "
                f"ou à la justice, constituant une violation grave de l'article 15 DUDH"
            )
        elif self.stateless_population_scale_severity_score >= 40:
            signals.append(
                f"Population apatride significative de {self.name} — groupes minoritaires "
                f"exposés à l'exclusion systémique faute de documents d'identité reconnus "
                f"par les autorités nationales"
            )
        if self.citizenship_deprivation_arbitrariness_score >= 60:
            signals.append(
                f"Privation arbitraire de nationalité — la déchéance de citoyenneté ciblant "
                f"des minorités ethniques ou religieuses constitue une violation directe de "
                f"la Convention de 1954 sur l'apatridie et du droit international coutumier"
            )
        if self.documentation_access_birth_registration_deficit_score >= 60:
            signals.append(
                f"Déficit d'enregistrement des naissances — l'absence d'état civil prive les "
                f"générations futures de tout accès à la nationalité, perpétuant un cycle "
                f"intergénérationnel d'apatridie et d'exclusion des services essentiels"
            )
        if self.stateless_rights_protection_mechanism_gap_score >= 40:
            signals.append(
                f"Impunité institutionnelle — l'absence de procédures d'identification et de "
                f"protection des apatrides expose ces populations aux détentions arbitraires "
                f"illimitées et aux expulsions vers des États qui les rejettent"
            )
        if not signals:
            signals.append(
                f"Protection relative des droits à la nationalité de {self.name} — "
                f"mécanismes partiels de prévention de l'apatridie et d'enregistrement civil"
            )
        return signals[:3]

    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "stateless_population_scale_severity_score": self.stateless_population_scale_severity_score,
            "citizenship_deprivation_arbitrariness_score": self.citizenship_deprivation_arbitrariness_score,
            "documentation_access_birth_registration_deficit_score": self.documentation_access_birth_registration_deficit_score,
            "stateless_rights_protection_mechanism_gap_score": self.stateless_rights_protection_mechanism_gap_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_statelessness_citizenship_rights_index": self.estimated_statelessness_citizenship_rights_index,
            "last_updated": self.last_updated,
        }


class StatelessnessCitizenshipRightsEngine:
    ENGINE_VERSION = "1.0.0"
    DOMAIN = "statelessness_citizenship_rights"

    def __init__(self):
        self.entities = self._load_entities()

    def _load_entities(self) -> List[StatelessnessCitizenshipRightsEntity]:
        return [
            StatelessnessCitizenshipRightsEntity(
                entity_id="SCR-001",
                name="Myanmar/Rohingyas 600 000 Apatrides",
                country="Asie du Sud-Est",
                sector="Loi Citoyenneté 1982 Exclut Rohingyas, 600 000 Sans Nationalité Au Myanmar, 1M+ Réfugiés Bangladesh & Génocide ONU 2018",
                stateless_population_scale_severity_score=98.0,
                citizenship_deprivation_arbitrariness_score=97.0,
                documentation_access_birth_registration_deficit_score=95.0,
                stateless_rights_protection_mechanism_gap_score=92.0,
            ),
            StatelessnessCitizenshipRightsEntity(
                entity_id="SCR-002",
                name="Koweït/Bidun 100 000 Sans Nationalité",
                country="MENA",
                sector="100 000 Bidun Sans Citoyenneté Depuis Indépendance 1961, Résidents Depuis Génération, Sans Emploi Public, Éducation & Soins",
                stateless_population_scale_severity_score=88.0,
                citizenship_deprivation_arbitrariness_score=90.0,
                documentation_access_birth_registration_deficit_score=85.0,
                stateless_rights_protection_mechanism_gap_score=88.0,
            ),
            StatelessnessCitizenshipRightsEntity(
                entity_id="SCR-003",
                name="République Dominicaine/Haïtiens Déchus 2013",
                country="Caraïbes",
                sector="Décision TC 168-13 Rétroactive Depuis 1929, 200 000 Haïtiens-Dominicains Déchus Nationalité, Génération Née Sur Place",
                stateless_population_scale_severity_score=85.0,
                citizenship_deprivation_arbitrariness_score=92.0,
                documentation_access_birth_registration_deficit_score=80.0,
                stateless_rights_protection_mechanism_gap_score=82.0,
            ),
            StatelessnessCitizenshipRightsEntity(
                entity_id="SCR-004",
                name="Thaïlande/Peuples Montagnards Highlanders",
                country="Asie du Sud-Est",
                sector="480 000 Peuples Autochtones Montagnards Sans Nationalité, Akha/Hmong/Karen, Sans Droit Vote, Travel & Services Publics",
                stateless_population_scale_severity_score=82.0,
                citizenship_deprivation_arbitrariness_score=78.0,
                documentation_access_birth_registration_deficit_score=88.0,
                stateless_rights_protection_mechanism_gap_score=80.0,
            ),
            StatelessnessCitizenshipRightsEntity(
                entity_id="SCR-005",
                name="Lettonie/Estonies Non-Citoyens Russophones",
                country="Europe du Nord",
                sector="220 000 Passeports Non-Citoyens Lettonie, 70 000 Estonie, Russophones Post-URSS, Droits Politiques Limités & Naturalisation Difficile",
                stateless_population_scale_severity_score=52.0,
                citizenship_deprivation_arbitrariness_score=48.0,
                documentation_access_birth_registration_deficit_score=35.0,
                stateless_rights_protection_mechanism_gap_score=55.0,
            ),
            StatelessnessCitizenshipRightsEntity(
                entity_id="SCR-006",
                name="Côte d'Ivoire/Populations Sans Actes Naissance",
                country="Afrique de l'Ouest",
                sector="750 000 Personnes Sans Actes Naissance, 25% Enfants Non Enregistrés, Conflit Post-Électoral 2010-2011 Aggravation",
                stateless_population_scale_severity_score=52.0,
                citizenship_deprivation_arbitrariness_score=45.0,
                documentation_access_birth_registration_deficit_score=65.0,
                stateless_rights_protection_mechanism_gap_score=52.0,
            ),
            StatelessnessCitizenshipRightsEntity(
                entity_id="SCR-007",
                name="UNHCR/Plan #IBelong 2024 Éradication Apatridie",
                country="Global",
                sector="Plan 10 Ans Fin Apatridie 2014-2024, 10M Apatrides Documentés, Conventions 1954 & 1961 & 92 États Parties",
                stateless_population_scale_severity_score=20.0,
                citizenship_deprivation_arbitrariness_score=18.0,
                documentation_access_birth_registration_deficit_score=22.0,
                stateless_rights_protection_mechanism_gap_score=28.0,
            ),
            StatelessnessCitizenshipRightsEntity(
                entity_id="SCR-008",
                name="UE/Droit Citoyenneté & Naturalisation Modèle",
                country="Europe",
                sector="Directive Longue Durée Résidents, Naturalisation 5-10 Ans, Double Nationalité & CJUE Protection Perte Citoyenneté EU",
                stateless_population_scale_severity_score=4.0,
                citizenship_deprivation_arbitrariness_score=5.0,
                documentation_access_birth_registration_deficit_score=3.0,
                stateless_rights_protection_mechanism_gap_score=6.0,
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
            "confidence_score": 0.88,
            "data_sources": [
                "unhcr_statelessness_report_2023",
                "institute_statelessness_inclusion",
                "human_rights_watch_citizenship_rights",
                "international_law_commission_nationality",
            ],
            "entities": results,
            "avg_estimated_statelessness_citizenship_rights_index": avg_index,
        }


if __name__ == "__main__":
    import json
    engine = StatelessnessCitizenshipRightsEngine()
    result = engine.analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nAvg composite: {result['avg_composite']}")
    print(f"Distribution: {result['risk_distribution']}")
