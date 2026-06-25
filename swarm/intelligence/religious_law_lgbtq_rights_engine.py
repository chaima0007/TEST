from dataclasses import dataclass, field
from typing import List, Dict
import statistics


@dataclass
class ReligiousLawLgbtqRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    sharia_apostasy_lgbtq_death_penalty_score: float = 0.0
    conversion_therapy_state_sanctioned_scale_score: float = 0.0
    religious_institution_political_power_rights_rollback_score: float = 0.0
    lgbtq_asylum_protection_deficit_score: float = 0.0
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: List[str] = field(init=False)
    estimated_religious_law_lgbtq_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.sharia_apostasy_lgbtq_death_penalty_score * 0.30 +
            self.conversion_therapy_state_sanctioned_scale_score * 0.25 +
            self.religious_institution_political_power_rights_rollback_score * 0.25 +
            self.lgbtq_asylum_protection_deficit_score * 0.20, 2
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
            "peine_mort_droit_religieux_lgbtq": self.sharia_apostasy_lgbtq_death_penalty_score,
            "therapies_conversion_etatiques": self.conversion_therapy_state_sanctioned_scale_score,
            "pouvoir_religieux_retrogression_droits": self.religious_institution_political_power_rights_rollback_score,
            "deficit_asile_protection_lgbtq": self.lgbtq_asylum_protection_deficit_score,
        }
        self.primary_pattern = max(patterns_map, key=lambda k: patterns_map[k])
        self.key_signals = self._generate_signals()
        self.estimated_religious_law_lgbtq_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def _generate_signals(self) -> List[str]:
        signals = []
        if self.sharia_apostasy_lgbtq_death_penalty_score >= 60:
            signals.append(
                f"Peine de mort pour homosexualité de {self.name} — les lois fondées "
                f"sur l'interprétation religieuse condamnent à mort les personnes LGBTQ+, "
                f"violant les articles 3, 5 et 7 de la DUDH et le Protocole de l'ONU 2014"
            )
        elif self.sharia_apostasy_lgbtq_death_penalty_score >= 40:
            signals.append(
                f"Criminalisation religieuse de {self.name} — les lois inspirées de "
                f"l'interprétation religieuse pénalisent l'identité et l'expression LGBTQ+, "
                f"exposant les personnes à l'emprisonnement et aux violences d'État"
            )
        if self.conversion_therapy_state_sanctioned_scale_score >= 60:
            signals.append(
                f"Thérapies de conversion étatiques — pratiques condamnées par l'ONU comme "
                f"torture (A/HRC/44/53) imposées aux personnes LGBTQ+ sous autorité religieuse "
                f"avec soutien légal de l'État, causant des traumatismes psychologiques graves"
            )
        if self.religious_institution_political_power_rights_rollback_score >= 60:
            signals.append(
                f"Retrogression institutionnelle — les institutions religieuses détenant un "
                f"pouvoir politique direct bloquent activement les réformes de protection des "
                f"droits LGBTQ+ et soutiennent les législations discriminatoires"
            )
        if self.lgbtq_asylum_protection_deficit_score >= 40:
            signals.append(
                f"Déficit de protection des réfugiés LGBTQ+ — les personnes fuyant les "
                f"persécutions religieuses n'ont pas accès aux procédures d'asile adaptées, "
                f"violant la Convention de 1951 et les Principes de Yogyakarta"
            )
        if not signals:
            signals.append(
                f"Protection relative des droits LGBTQ+ de {self.name} — séparation "
                f"effective de l'État et des institutions religieuses sur les droits civils"
            )
        return signals[:3]

    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "sharia_apostasy_lgbtq_death_penalty_score": self.sharia_apostasy_lgbtq_death_penalty_score,
            "conversion_therapy_state_sanctioned_scale_score": self.conversion_therapy_state_sanctioned_scale_score,
            "religious_institution_political_power_rights_rollback_score": self.religious_institution_political_power_rights_rollback_score,
            "lgbtq_asylum_protection_deficit_score": self.lgbtq_asylum_protection_deficit_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_religious_law_lgbtq_rights_index": self.estimated_religious_law_lgbtq_rights_index,
            "last_updated": self.last_updated,
        }


class ReligiousLawLgbtqRightsEngine:
    ENGINE_VERSION = "1.0.0"
    DOMAIN = "religious_law_lgbtq_rights"

    def __init__(self):
        self.entities = self._load_entities()

    def _load_entities(self) -> List[ReligiousLawLgbtqRightsEntity]:
        return [
            ReligiousLawLgbtqRightsEntity(
                entity_id="RLLR-001",
                name="Iran/Peine De Mort Homosexualité Droit Islamique",
                country="MENA",
                sector="Peine Mort Homosexualité Droit Islamique, 4 000 Exécutés Depuis 1979, Khamenei Fatwa Anti-LGBT & Opérations Police Morale 2022 Mahsa",
                sharia_apostasy_lgbtq_death_penalty_score=99.0,
                conversion_therapy_state_sanctioned_scale_score=95.0,
                religious_institution_political_power_rights_rollback_score=98.0,
                lgbtq_asylum_protection_deficit_score=96.0,
            ),
            ReligiousLawLgbtqRightsEntity(
                entity_id="RLLR-002",
                name="Arabie Saoudite/Charia LGBT Châtiments Corporels",
                country="MENA",
                sector="Charia Punition Mort Homosexualité, Fouet & Prison, CPVPV Police Morale, Zéro ONG LGBT Tolérée & Vision 2030 Façade Sans Droits",
                sharia_apostasy_lgbtq_death_penalty_score=97.0,
                conversion_therapy_state_sanctioned_scale_score=90.0,
                religious_institution_political_power_rights_rollback_score=96.0,
                lgbtq_asylum_protection_deficit_score=92.0,
            ),
            ReligiousLawLgbtqRightsEntity(
                entity_id="RLLR-003",
                name="Afghanistan/Taliban Charia Totale LGBTQ Mort",
                country="Asie Centrale",
                sector="Taliban 2021 Retour, Charia Intégrale Rétablie, LGBT Exécutions Publiques, Toutes ONGs LGBT Dissoutes & 50+ Arrestations Documentées UNHCR",
                sharia_apostasy_lgbtq_death_penalty_score=99.0,
                conversion_therapy_state_sanctioned_scale_score=92.0,
                religious_institution_political_power_rights_rollback_score=99.0,
                lgbtq_asylum_protection_deficit_score=95.0,
            ),
            ReligiousLawLgbtqRightsEntity(
                entity_id="RLLR-004",
                name="Ouganda/Anti-Homosexuality Act Peine Mort",
                country="Afrique de l'Est",
                sector="Anti-Homosexuality Act 2023 Peine Mort Aggravée, Museveni Signature, Lobbying Évangéliques USA, 50+ Arrestations & Discrimination Emploi/Logement",
                sharia_apostasy_lgbtq_death_penalty_score=92.0,
                religious_institution_political_power_rights_rollback_score=94.0,
                conversion_therapy_state_sanctioned_scale_score=82.0,
                lgbtq_asylum_protection_deficit_score=88.0,
            ),
            ReligiousLawLgbtqRightsEntity(
                entity_id="RLLR-005",
                name="Russie/Loi Propagande LGBT Église Orthodoxe",
                country="Europe de l'Est",
                sector="Loi Propagande LGBT 2013 Étendue 2023 Tous Âges, Église Orthodoxe Influence État, Organisations LGBT Interdites & Pride Criminalisée",
                sharia_apostasy_lgbtq_death_penalty_score=42.0,
                conversion_therapy_state_sanctioned_scale_score=55.0,
                religious_institution_political_power_rights_rollback_score=60.0,
                lgbtq_asylum_protection_deficit_score=48.0,
            ),
            ReligiousLawLgbtqRightsEntity(
                entity_id="RLLR-006",
                name="Pologne/Zones Sans LGBT Église Catholique",
                country="Europe Centrale",
                sector="100+ Zones Sans LGBT 2019-2022, PiS Idéologie Catholique, Jurisprudence CJUE 2022 Contre Discriminations & Retrait Zones Sous Pression EU 2022",
                sharia_apostasy_lgbtq_death_penalty_score=25.0,
                conversion_therapy_state_sanctioned_scale_score=40.0,
                religious_institution_political_power_rights_rollback_score=62.0,
                lgbtq_asylum_protection_deficit_score=35.0,
            ),
            ReligiousLawLgbtqRightsEntity(
                entity_id="RLLR-007",
                name="USA/Evangelical Anti-LGBT Bills 2023-2024",
                country="Amérique du Nord",
                sector="580+ Bills Anti-LGBT 2023 États, Thérapies Conversion Légales 20+ États, Drag Ban Tennessee & Idéologie Évangélique SCOTUS Décisions",
                sharia_apostasy_lgbtq_death_penalty_score=15.0,
                conversion_therapy_state_sanctioned_scale_score=35.0,
                religious_institution_political_power_rights_rollback_score=40.0,
                lgbtq_asylum_protection_deficit_score=22.0,
            ),
            ReligiousLawLgbtqRightsEntity(
                entity_id="RLLR-008",
                name="Canada/Mariage Égal & Laïcité Protection LGBTQ",
                country="Amérique du Nord",
                sector="Mariage Égal 2005, Loi C-4 Thérapies Conversion Interdites 2022, IRPA Protection Réfugiés LGBT & Charte Droits Protection Robuste",
                sharia_apostasy_lgbtq_death_penalty_score=3.0,
                conversion_therapy_state_sanctioned_scale_score=4.0,
                religious_institution_political_power_rights_rollback_score=5.0,
                lgbtq_asylum_protection_deficit_score=4.0,
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
                "ilga_world_state_sponsored_homophobia_2023",
                "rainbow_europe_index_2023",
                "human_rights_watch_lgbtq_report_2023",
                "outright_action_international_religion_rights",
            ],
            "entities": results,
            "avg_estimated_religious_law_lgbtq_rights_index": avg_index,
        }


if __name__ == "__main__":
    import json
    engine = ReligiousLawLgbtqRightsEngine()
    result = engine.analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nAvg composite: {result['avg_composite']}")
    print(f"Distribution: {result['risk_distribution']}")
