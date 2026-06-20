"""LGBTQ+ Rights Engine — Criminalisation LGBT+, violence étatique & droits fondamentaux."""

from dataclasses import dataclass
from typing import List


@dataclass
class LgbtqRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    criminalization_severity_score: float
    violence_impunity_score: float
    legal_recognition_denial_score: float
    forced_conversion_repression_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.criminalization_severity_score * 0.30
            + self.violence_impunity_score * 0.25
            + self.legal_recognition_denial_score * 0.25
            + self.forced_conversion_repression_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    @property
    def primary_pattern(self) -> str:
        scores = {
            "criminalisation_lgbtq_etat": self.criminalization_severity_score,
            "violence_impunite_etatique": self.violence_impunity_score,
            "deni_reconnaissance_juridique": self.legal_recognition_denial_score,
            "repression_conversion_forcee": self.forced_conversion_repression_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Violation des droits LGBT+ documentée — {self.name} avec score composite {self.composite_score}/100 révélant une criminalisation ou une violence systémique violant les Principes de Jogjakarta et l'Article 2 du PIDCP",
            f"Criminalisation étatique ({self.criminalization_severity_score}/100) — la pénalisation de l'orientation sexuelle ou de l'identité de genre constitue une violation directe du droit à la vie privée (Article 17 PIDCP) et à la non-discrimination",
            f"Activer le Rapporteur Spécial ONU sur l'Orientation Sexuelle et l'Identité de Genre (IE SOGI) pour enquête urgente et exiger la dépénalisation conformément aux résolutions du Conseil des Droits de l'Homme ONU",
        ]

    @property
    def estimated_lgbtq_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "criminalization_severity_score": self.criminalization_severity_score,
            "violence_impunity_score": self.violence_impunity_score,
            "legal_recognition_denial_score": self.legal_recognition_denial_score,
            "forced_conversion_repression_score": self.forced_conversion_repression_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_lgbtq_rights_index": self.estimated_lgbtq_rights_index,
            "last_updated": "2026-06-20",
        }


class LgbtqRightsEngine:
    ENGINE_VERSION = "1.0.0"
    CONFIDENCE_SCORE = 0.83
    DATA_SOURCES = [
        "ilga_world_state_sponsored_homophobia_report",
        "human_rights_watch_lgbt_rights_database",
        "un_ie_sogi_reports_sexual_orientation_gender_identity",
    ]

    def __init__(self):
        self.entities: List[LgbtqRightsEntity] = [
            LgbtqRightsEntity(
                "LG-001", "Iran/IRGC — 75+ Exécutions LGBT 1979-2024, Pendaison Homosexuels & Code Pénal Islamique",
                "MENA",
                "Code Pénal Islamique Iran Peine Mort Homosexualité Masculine, 75+ Exécutions Documentées ILGA 1979-2024, Femmes Flagellation & Thérapies Conversion Forcée IRGC",
                92, 88, 95, 90,
            ),
            LgbtqRightsEntity(
                "LG-002", "Ouganda/Anti-Homosexuality Act — Peine Mort 2023, Museveni & Fermeture ONG",
                "Afrique de l'Est",
                "Ouganda Anti-Homosexuality Act 2023 Peine Mort Récidive Museveni, 500+ Arrestations, ONG LGBT Fermées & USA Sanctions Partielles Conditionnées",
                88, 85, 92, 88,
            ),
            LgbtqRightsEntity(
                "LG-003", "Chéchénie/Russie — Camps Purge 2017-19, Kadyrov & Loi Propagande Homosexuelle",
                "Europe de l'Est",
                "Purges Anti-LGBT Chetchénie 2017-19 Camps Clandestins HRW, Kadyrov Déni Total, Loi Propagande Homosexuelle Russie 2013/2023 Élargie & Criminalisation Trans Proposée",
                85, 90, 88, 82,
            ),
            LgbtqRightsEntity(
                "LG-004", "Arabie Saoudite — Flagellation/Prison LGBT, Criminalisation Totale & Meurtre Honneur",
                "MENA",
                "Arabie Saoudite Criminalisation LGBT Totale Charia, Flagellation/Prison Homosexualité, Meurtre Honneur Impuni & Surveillance Digitale Applications Grindr LGBTQ+",
                82, 85, 88, 80,
            ),
            LgbtqRightsEntity(
                "LG-005", "Pologne/Zones Libres LGBT — Résolutions Anti-LGBT 2019-21 & Réversion Partielle 2024",
                "Europe de l'Ouest",
                "100 Zones Libres LGBT Pologne 2019-21 Résolutions Municipales, Droits UE Pression Tusk 2024 Réversion, PiS Propagande Anti-LGBT & Fonds UE Conditionné",
                55, 52, 58, 50,
            ),
            LgbtqRightsEntity(
                "LG-006", "Ghana/Human Sexual Rights Bill — Criminalisation Renforcée 2021 & ONG Fermées",
                "Afrique de l'Ouest",
                "Ghana Human Sexual Rights and Family Values Bill 2021 Prison 3-10 Ans LGBT, Défenseurs LGBT Arrêtés, ONG Accra LGBT+ Regional Conference Interdite & Pression Religieuse",
                52, 48, 58, 55,
            ),
            LgbtqRightsEntity(
                "LG-007", "Hongrie/Fidesz — Loi Anti-Propagande 2021, Adoption Interdite & Referendum 2022",
                "Europe de l'Ouest",
                "Hongrie Loi Anti-Propagande LGBT 2021 Mineurs, Adoption Homosexuels Interdite, Referendum 2022 Anti-LGBT & Commission UE Infringement Procedure 2022",
                28, 30, 32, 25,
            ),
            LgbtqRightsEntity(
                "LG-008", "ILGA World/HRC — Rapporteur Spécial ONU SOGI & Principes Jogjakarta",
                "Global",
                "ILGA World State Sponsored Homophobia Report Annuel, Rapporteur Spécial ONU Orientation Sexuelle Identité Genre IE SOGI, Principes Jogjakarta 2006/2017 & Résolutions CDH-ONU",
                5, 4, 3, 6,
            ),
        ]

    def summary(self) -> dict:
        data = [e.to_dict() for e in self.entities]
        avg = round(sum(e.composite_score for e in self.entities) / len(self.entities), 2)
        risk_dist: dict = {}
        pattern_dist: dict = {}
        for e in self.entities:
            risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
            pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        critical = [e for e in self.entities if e.risk_level == "critique"]
        return {
            "total_entities": len(self.entities),
            "avg_composite": avg,
            "risk_distribution": risk_dist,
            "pattern_distribution": pattern_dist,
            "top_risk_entities": [e.name for e in sorted(critical, key=lambda x: -x.composite_score)[:3]],
            "critical_alerts": [f"{e.name}: {e.primary_pattern}" for e in critical],
            "last_analysis": "2026-06-20",
            "engine_version": self.ENGINE_VERSION,
            "domain": "lgbtq_rights",
            "confidence_score": self.CONFIDENCE_SCORE,
            "data_sources": self.DATA_SOURCES,
            "entities": data,
            "avg_estimated_lgbtq_rights_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = LgbtqRightsEngine()
    result = engine.summary()
    print(json.dumps({
        "total": result["total_entities"],
        "avg": result["avg_composite"],
        "distribution": result["risk_distribution"],
        "top3": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
    for e in engine.entities:
        print(f"  {e.entity_id}: {e.composite_score:.2f} → {e.risk_level}")
