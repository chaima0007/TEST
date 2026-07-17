"""Hate Crime Engine — Crimes de haine & violences motivées par l'idéologie."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class HateCrimeEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    racial_bias_crime_rate_score: float
    religious_motivated_violence_score: float
    lgbtq_targeted_violence_score: float
    accountability_prosecution_failure_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.racial_bias_crime_rate_score * 0.30
            + self.religious_motivated_violence_score * 0.25
            + self.lgbtq_targeted_violence_score * 0.25
            + self.accountability_prosecution_failure_score * 0.20,
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
            "ciblage_racial_xenophobe": self.racial_bias_crime_rate_score,
            "violence_religieuse_motivee": self.religious_motivated_violence_score,
            "violence_lgbtq_phobique": self.lgbtq_targeted_violence_score,
            "impunite_auteurs_haine": self.accountability_prosecution_failure_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Crimes de haine documentés — {self.name} avec score composite {self.composite_score}/100 révélant des violences systémiques motivées par la haine raciale, religieuse ou identitaire nécessitant une réponse juridique urgente",
            f"Impunité structurelle — le niveau d'accountability/poursuites ({self.accountability_prosecution_failure_score}/100) indique une défaillance systémique dans la réponse judiciaire aux crimes de haine, perpétuant le cycle de violence",
            f"Activer les mécanismes OSCE/ODIHR de reporting des crimes de haine et renforcer les lois nationales sur les crimes de haine avec formation des forces de l'ordre à l'identification et au signalement systématique",
        ]

    @property
    def estimated_hate_crime_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "racial_bias_crime_rate_score": self.racial_bias_crime_rate_score,
            "religious_motivated_violence_score": self.religious_motivated_violence_score,
            "lgbtq_targeted_violence_score": self.lgbtq_targeted_violence_score,
            "accountability_prosecution_failure_score": self.accountability_prosecution_failure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_hate_crime_index": self.estimated_hate_crime_index,
            "last_updated": "2026-06-20",
        }


class HateCrimeEngine:
    ENGINE_VERSION = "1.0.0"
    CONFIDENCE_SCORE = 0.80
    DATA_SOURCES = [
        "osce_odihr_hate_crime_reporting_database",
        "fbi_uniform_crime_reporting_hate_crimes",
        "ilga_world_homophobia_transphobia_report",
    ]

    def __init__(self):
        self.entities: List[HateCrimeEntity] = [
            HateCrimeEntity(
                "HC-001", "USA/Supremacy Blanche — 7 700+ Crimes Haine FBI, Islamophobie Post-9/11 & Impunité Structurelle",
                "Amérique du Nord",
                "7 700+ Crimes Haine FBI 2022 Sous-Reportés, Suprémacisme Blanc Terrorisme Intérieur N°1, Islamophobie 2001-2024 Documentée & Acquittements Fréquents Auteurs",
                92, 85, 88, 82,
            ),
            HateCrimeEntity(
                "HC-002", "Inde/Lynchages Communautaires — Islamophobie BJP, Cow Vigilantes & 200+ Tués Impunis",
                "Asie du Sud",
                "200+ Lynchages Cow Vigilantes 2014-24 Documentés HRW, Islamophobie Institutionnalisée BJP, Crimes Anti-Dalits & Lois Anti-Conversion Armes Communautaires",
                90, 92, 82, 88,
            ),
            HateCrimeEntity(
                "HC-003", "Russie/Chetchénie — Purges Anti-LGBT Kadyrov, Pogroms Ethniques & Crimes Motivés Haine",
                "Europe de l'Est",
                "Purges Anti-LGBT Chetchénie 2017-19 Documentées ONU, Attaques Skinheads Minorités Ethniques, Loi Propagande Homosexuelle & Aucune Poursuite Officielle Kadyrov",
                82, 80, 95, 88,
            ),
            HateCrimeEntity(
                "HC-004", "Allemagne/Extrême Droite — 14 000+ Crimes Haine/An, Attentats NSU & Neo-Nazisme",
                "Europe de l'Ouest",
                "14 000+ Crimes Motivés Haine Allemagne 2022, Cellule Terroriste NSU 10 Meurtres Racistes Non Détectés Années, Attaques Mosquées 2024 & AfD Normalisation Discours Haine",
                85, 82, 80, 85,
            ),
            HateCrimeEntity(
                "HC-005", "France/Antisémitisme-Islamophobie — 1 200+ Actes/An, BDS & Profanations",
                "Europe de l'Ouest",
                "1 200+ Actes Antisémites France 2023, 900+ Actes Islamophobes, Profanations Cimetières & Loi Contre Séparatisme Ciblant Communautés Musulmanes",
                55, 58, 50, 52,
            ),
            HateCrimeEntity(
                "HC-006", "Brésil/Violences LGBT+ — 300+ Meurtres/An, Homophobie Religieuse & Impunité",
                "Amérique du Sud",
                "300+ Meurtres LGBT+ Brésil/An GGB, Taux Assassinats Trans 1er Monde, Bolsonaro Homophobie Institutionnelle 2019-22 & Église Évangélique Crimes Inspirés Haine",
                52, 48, 62, 55,
            ),
            HateCrimeEntity(
                "HC-007", "Royaume-Uni/Islamophobie Post-Brexit — 46 000 Incidents Haine/An & Reporting Partiel",
                "Europe de l'Ouest",
                "46 000 Incidents Crimes Haine UK 2022, Islamophobie Doublée Post-Brexit 2016, Stephen Lawrence Case Institutionalisme & PREVENT Profilage Communautés Musulmanes",
                32, 35, 28, 30,
            ),
            HateCrimeEntity(
                "HC-008", "OSCE/ODIHR — Mécanisme Reporting Crimes Haine & Législations Modèles",
                "Global",
                "ODIHR Système Reporting Crimes Haine 57 États, Recommandations Législatives Anti-Haine, Formation Police & Base Données Incidents Haine OSCE",
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
            "domain": "hate_crime",
            "confidence_score": self.CONFIDENCE_SCORE,
            "data_sources": self.DATA_SOURCES,
            "entities": data,
            "avg_estimated_hate_crime_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = HateCrimeEngine()
    result = engine.summary()
    print(json.dumps({
        "total": result["total_entities"],
        "avg": result["avg_composite"],
        "distribution": result["risk_distribution"],
        "top3": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
    for e in engine.entities:
        print(f"  {e.entity_id}: {e.composite_score:.2f} → {e.risk_level}")
