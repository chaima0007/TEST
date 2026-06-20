"""Child Labor Engine — Travail des enfants & exploitation économique infantile."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ChildLaborEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    hazardous_child_labor_rate_score: float
    forced_labor_recruitment_score: float
    school_access_deprivation_score: float
    regulatory_enforcement_failure_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.hazardous_child_labor_rate_score * 0.30
            + self.forced_labor_recruitment_score * 0.25
            + self.school_access_deprivation_score * 0.25
            + self.regulatory_enforcement_failure_score * 0.20,
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
            "travail_dangereux_enfants": self.hazardous_child_labor_rate_score,
            "recrutement_force_mineur": self.forced_labor_recruitment_score,
            "privation_acces_education": self.school_access_deprivation_score,
            "defaillance_application_loi": self.regulatory_enforcement_failure_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Exploitation économique infantile documentée — {self.name} avec score composite {self.composite_score}/100 révélant des conditions de travail dangereuses violant la Convention OIT 182 sur les pires formes de travail des enfants",
            f"Privation d'éducation structurelle — le score d'accès à l'éducation ({self.school_access_deprivation_score}/100) indique que le travail infantile prive les enfants de leur droit fondamental à l'éducation (Article 28 CRC)",
            f"Activer les mécanismes OIT/IPEC pour inspection du travail renforcée et soutenir Alliance 8.7 pour élimination pires formes travail enfants d'ici 2025 conformément à l'ODD 8.7",
        ]

    @property
    def estimated_child_labor_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "hazardous_child_labor_rate_score": self.hazardous_child_labor_rate_score,
            "forced_labor_recruitment_score": self.forced_labor_recruitment_score,
            "school_access_deprivation_score": self.school_access_deprivation_score,
            "regulatory_enforcement_failure_score": self.regulatory_enforcement_failure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_child_labor_index": self.estimated_child_labor_index,
            "last_updated": "2026-06-20",
        }


class ChildLaborEngine:
    ENGINE_VERSION = "1.0.0"
    CONFIDENCE_SCORE = 0.85
    DATA_SOURCES = [
        "ilo_ipec_child_labour_global_estimates",
        "unicef_multiple_indicator_cluster_surveys",
        "us_dol_bureau_international_labor_affairs_reports",
    ]

    def __init__(self):
        self.entities: List[ChildLaborEntity] = [
            ChildLaborEntity(
                "CL-001", "Mali/Mines d'Or — 200 000 Enfants Artisanaux, Mercure/Cyanure & Décès Documentés",
                "Afrique de l'Ouest",
                "200 000 Enfants Mines Artisanales Or Mali, Exposition Mercure/Cyanure Documentée HRW, Décès Et Blessures Carrières & Exportation Or Chaîne Approvisionnement Non-Tracée",
                92, 85, 90, 88,
            ),
            ChildLaborEntity(
                "CL-002", "RDC/Cobalt — 40 000 Enfants Mines Kasaï, Tesla/Apple Supply Chain & Zéro Sanction",
                "Afrique Centrale",
                "40 000 Enfants Mines Cobalt Artisanales Kasaï/Katanga, Blessures Éboulements Documentées Amnesty, Batteries Électriques Tesla/Apple & Due Diligence Marques Insuffisante",
                90, 88, 85, 90,
            ),
            ChildLaborEntity(
                "CL-003", "Bangladesh/Garment — 4.8M Enfants Travailleurs, Rana Plaza & Travail Nocturne",
                "Asie du Sud",
                "4.8M Enfants Travailleurs Bangladesh, Rana Plaza 2013 1134 Morts Dont Enfants, Garment Secteur Travail Nocturne Illegal & Accord Bangladesh 2013 Progrès Limités",
                88, 85, 88, 85,
            ),
            ChildLaborEntity(
                "CL-004", "Inde/Travail Bonded — 5.8M Enfants, Briqueteries Bihar & Servitude Héréditaire",
                "Asie du Sud",
                "5.8M Enfants Travailleurs Inde Officiels, Briqueteries Bihar Travail Bonded Familial, Kamaiya/Haliya Servitude Héréditaire & Child Labour Act 2016 Application Insuffisante",
                85, 90, 82, 85,
            ),
            ChildLaborEntity(
                "CL-005", "Éthiopie/Plantations — 4M Enfants Agriculture Café/Thé, Travail Saisonnier Caché",
                "Afrique de l'Est",
                "4M Enfants Travailleurs Éthiopie Agriculture, Plantations Café/Thé Travail Saisonnier, Exportation Café Éthiopien Starbucks/Nespresso & Audit Social Insuffisant",
                55, 52, 58, 50,
            ),
            ChildLaborEntity(
                "CL-006", "Brésil/Agrobusiness — Enfants Canne à Sucre/Soja, Travail Rural Informel Familial",
                "Amérique du Sud",
                "Brésil 1.8M Enfants Travailleurs Rural, Canne à Sucre/Soja Enfants Travail Saisonnier, Travail Familial Légal Brésil <14 Ans & Dérogations Pire Formes",
                52, 48, 55, 55,
            ),
            ChildLaborEntity(
                "CL-007", "Mexique/Travail Agricole Saisonnier — Légumes/Fraises Exportation & Mineurs Documentés",
                "Amérique du Nord",
                "Mexique Enfants Champs Agricoles Légaux Via Exception Familiale, Fraises/Tomates Export USA, Enquête NYT 2023 & USMCA Clauses Travail Enfants Insuffisantes",
                30, 28, 32, 28,
            ),
            ChildLaborEntity(
                "CL-008", "OIT/Alliance 8.7 — Convention 182, SDG 8.7 Élimination & IPEC Programme",
                "Global",
                "OIT Convention 182 Pires Formes Travail Enfants Ratifiée 187 États, Alliance 8.7 ODD Élimination 2025, IPEC Programme International & Rapport Mondial Travail Enfants 2022",
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
            "domain": "child_labor",
            "confidence_score": self.CONFIDENCE_SCORE,
            "data_sources": self.DATA_SOURCES,
            "entities": data,
            "avg_estimated_child_labor_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = ChildLaborEngine()
    result = engine.summary()
    print(json.dumps({
        "total": result["total_entities"],
        "avg": result["avg_composite"],
        "distribution": result["risk_distribution"],
        "top3": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
    for e in engine.entities:
        print(f"  {e.entity_id}: {e.composite_score:.2f} → {e.risk_level}")
