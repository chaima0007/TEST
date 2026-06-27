"""Right to Education Engine — Droit à l'éducation, exclusions & destructions d'écoles."""

from dataclasses import dataclass
from typing import List


@dataclass
class RightToEducationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    school_exclusion_rate_score: float
    gender_education_barrier_score: float
    quality_infrastructure_failure_score: float
    conflict_education_destruction_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.school_exclusion_rate_score * 0.30
            + self.gender_education_barrier_score * 0.25
            + self.quality_infrastructure_failure_score * 0.25
            + self.conflict_education_destruction_score * 0.20,
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
            "exclusion_scolaire_massive": self.school_exclusion_rate_score,
            "barriere_genre_education": self.gender_education_barrier_score,
            "defaillance_infrastructure_qualite": self.quality_infrastructure_failure_score,
            "destruction_ecoles_conflit": self.conflict_education_destruction_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Violation du droit à l'éducation documentée — {self.name} avec score composite {self.composite_score}/100 révélant une exclusion scolaire massive violant l'Article 26 de la DUDH et l'Article 28 de la Convention des Droits de l'Enfant",
            f"Barrière de genre à l'éducation ({self.gender_education_barrier_score}/100) — l'exclusion des filles de l'éducation constitue une discrimination fondée sur le sexe violant la CEDAW et l'ODD 4 d'éducation inclusive et équitable",
            f"Activer l'UNESCO/Rapporteur Spécial ONU sur le Droit à l'Éducation pour enquête urgente et mobiliser le Fonds UNICEF d'Éducation en Situation d'Urgence (ESU) pour rétablir l'accès scolaire",
        ]

    @property
    def estimated_right_to_education_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "school_exclusion_rate_score": self.school_exclusion_rate_score,
            "gender_education_barrier_score": self.gender_education_barrier_score,
            "quality_infrastructure_failure_score": self.quality_infrastructure_failure_score,
            "conflict_education_destruction_score": self.conflict_education_destruction_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_right_to_education_index": self.estimated_right_to_education_index,
            "last_updated": "2026-06-20",
        }


class RightToEducationEngine:
    ENGINE_VERSION = "1.0.0"
    CONFIDENCE_SCORE = 0.86
    DATA_SOURCES = [
        "unesco_global_education_monitoring_report",
        "unicef_out_of_school_children_database",
        "global_coalition_to_protect_education_from_attack_gcpea",
    ]

    def __init__(self):
        self.entities: List[RightToEducationEntity] = [
            RightToEducationEntity(
                "RE-001", "Afghanistan/Taliban — 4M Filles Interdites École 2021, Université Fermée & Éducation Femmes",
                "Asie du Sud",
                "Taliban 4M+ Filles Interdites École Afghanistan 2021, Universités Femmes Fermées 2022, Écoles Secrètes Clandestines & UNICEF 6.2M Enfants Hors École 2023",
                95, 95, 88, 85,
            ),
            RightToEducationEntity(
                "RE-002", "Yémen/Conflit — 8M Enfants Hors École, 2 400 Écoles Détruites & Enseignants Non-Payés",
                "MENA",
                "Yemen 8M Enfants Hors École 2023 UNICEF, 2 400+ Écoles Détruites/Endommagées, Enseignants Non-Payés 8 Ans, Houthis Recrutement Écoles & Financement Urgence Insuffisant",
                88, 85, 90, 92,
            ),
            RightToEducationEntity(
                "RE-003", "Mali/Burkina Faso — 1M Enfants Hors École, 1 200+ Écoles Fermées & Djihadistes",
                "Afrique de l'Ouest",
                "Mali/Burkina Faso 1M+ Enfants Hors École Conflit, 1 200+ Écoles Fermées Menaces Djihadistes, Enseignants Tués/Kidnappés & MINUSMA Retrait Impact Éducation",
                85, 82, 85, 90,
            ),
            RightToEducationEntity(
                "RE-004", "Nigeria/Nord — 10.5M Out-of-School, Boko Haram Chibok & Pauvreté Structurelle",
                "Afrique de l'Ouest",
                "Nigeria 10.5M Enfants Hors École Plus Grand Monde, Boko Haram 276 Lycéennes Chibok 2014, ASCE Nord Nigeria & Pauvreté Structurelle Barrières Éducation",
                82, 80, 85, 82,
            ),
            RightToEducationEntity(
                "RE-005", "Pakistan/FATA/Baloutchistan — 20M Hors École, Filles Zones Tribales & Madrasa",
                "Asie du Sud",
                "Pakistan 20M Enfants Hors École Statistique Mondiale, Filles Zones Tribales FATA/Baloutchistan Accès Limité, Madrasa Éducation Formelle Gap & Malala Yousafzai Cas Emblématique",
                55, 58, 52, 50,
            ),
            RightToEducationEntity(
                "RE-006", "Soudan/Gaza — 1M+ Enfants Déplacés Sans École, RSF Attaques Établissements",
                "Afrique de l'Est/MENA",
                "Soudan 19M Enfants Hors École Post-Conflit 2023, RSF Attaques Écoles Khartoum, Gaza 600 000 Enfants Sans École 2024 & GCPEA Rapport Attaques Éducation",
                52, 48, 58, 55,
            ),
            RightToEducationEntity(
                "RE-007", "Haïti/Gangs — 700 000 Enfants Hors École, Contrôle Territorial Gangs & Instabilité",
                "Caraïbes",
                "Haïti 700 000 Enfants Hors École 2024 UNICEF, Gangs Contrôle 80% Port-au-Prince, Écoles Converties Bases & Enseignants Exilés Insécurité",
                30, 28, 32, 25,
            ),
            RightToEducationEntity(
                "RE-008", "UNESCO/SDG4 — ODD4 Éducation Qualité, CDE Art 28 & Education Cannot Wait",
                "Global",
                "UNESCO ODD4 Éducation Qualité Inclusive 2030, CDE Article 28 Droit Éducation, Education Cannot Wait Fonds Urgence & Rapporteur Spécial ONU Droit Éducation",
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
            "domain": "right_to_education",
            "confidence_score": self.CONFIDENCE_SCORE,
            "data_sources": self.DATA_SOURCES,
            "entities": data,
            "avg_estimated_right_to_education_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = RightToEducationEngine()
    result = engine.summary()
    print(json.dumps({
        "total": result["total_entities"],
        "avg": result["avg_composite"],
        "distribution": result["risk_distribution"],
        "top3": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
    for e in engine.entities:
        print(f"  {e.entity_id}: {e.composite_score:.2f} → {e.risk_level}")
