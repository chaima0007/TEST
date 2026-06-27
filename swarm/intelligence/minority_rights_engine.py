"""Minority Rights Engine — Droits des minorités & suppression culturelle systémique."""

from dataclasses import dataclass
from typing import List


@dataclass
class MinorityRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    cultural_linguistic_suppression_score: float
    political_exclusion_score: float
    economic_marginalization_score: float
    physical_security_threat_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.cultural_linguistic_suppression_score * 0.30
            + self.political_exclusion_score * 0.25
            + self.economic_marginalization_score * 0.25
            + self.physical_security_threat_score * 0.20,
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
            "suppression_culturelle_linguistique": self.cultural_linguistic_suppression_score,
            "exclusion_politique_minorites": self.political_exclusion_score,
            "marginalisation_economique": self.economic_marginalization_score,
            "menace_securite_physique": self.physical_security_threat_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Violation des droits des minorités documentée — {self.name} avec score composite {self.composite_score}/100 révélant une suppression systémique violant l'Article 27 du PIDCP et la Déclaration ONU sur les droits des minorités de 1992",
            f"Suppression culturelle-linguistique ({self.cultural_linguistic_suppression_score}/100) — l'effacement de la langue et de la culture constitue une forme de génocide culturel selon la définition élargie de la Convention de 1948",
            f"Activer le Comité consultatif du Conseil des droits de l'homme sur les minorités et exiger l'application effective de la Déclaration ONU 1992 sur les droits des personnes appartenant à des minorités nationales, ethniques, religieuses et linguistiques",
        ]

    @property
    def estimated_minority_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "cultural_linguistic_suppression_score": self.cultural_linguistic_suppression_score,
            "political_exclusion_score": self.political_exclusion_score,
            "economic_marginalization_score": self.economic_marginalization_score,
            "physical_security_threat_score": self.physical_security_threat_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_minority_rights_index": self.estimated_minority_rights_index,
            "last_updated": "2026-06-20",
        }


class MinorityRightsEngine:
    ENGINE_VERSION = "1.0.0"
    CONFIDENCE_SCORE = 0.81
    DATA_SOURCES = [
        "minority_rights_group_international_peoples_under_threat",
        "un_declaration_minority_rights_implementation_reports",
        "hrw_world_report_minority_discrimination",
    ]

    def __init__(self):
        self.entities: List[MinorityRightsEntity] = [
            MinorityRightsEntity(
                "MR-001", "Chine/Ouïghours — 1M+ Rééducation Xinjiang, Langue/Religion Interdites & Surveillance Totale",
                "Asie du Nord-Est",
                "1M+ Ouïghours Internés Camps Rééducation Xinjiang, Langue Arabe/Ouïghoure Interdite École, Mosquées Démolies, Surveillance Biométrique Totale & Transferts Forcés Usines",
                95, 92, 90, 95,
            ),
            MinorityRightsEntity(
                "MR-002", "Russie/Tatars Crimée-Minorités — Langues Supprimées, Déportations & Répression Post-2014",
                "Europe de l'Est",
                "Tatars Crimée Langue/Médias Interdits Post-2014, Medjlis Banni Organisation, Déportations Activistes, Tchétchénie Minorités Linguitiques Supprimées & Minorités Sibériennes Marginalisées",
                88, 85, 85, 88,
            ),
            MinorityRightsEntity(
                "MR-003", "Myanmar/Rohingya-Karen — Langues Effacées, Apatridie & Cultures Détruites",
                "Asie du Sud-Est",
                "Rohingya Langue/Culture Effacées État Rakhine, Karen/Kachin Langues Supprimées Écoles, Apatridie Institutionnalisée & Tatmadaw Attaques Villages Minoritaires Documentées",
                85, 88, 85, 82,
            ),
            MinorityRightsEntity(
                "MR-004", "Turquie/Kurdes — Langue Kurde Restrictions, HDP/DEM Réprimé & 40 000 Morts Conflit",
                "MENA/Europe",
                "Langue Kurde Interdite Éducation Publique Partiellement, HDP/DEM Parti Pro-Kurde 12 Ministres Emprisonnés, 40 000 Morts Conflit PKK 1984-2024 & Maires Kurdes Élus Révoqués",
                82, 85, 82, 80,
            ),
            MinorityRightsEntity(
                "MR-005", "Éthiopie/Tigréens — Langue Tigrigna Marginalisée Post-Conflit, Blocus & Discrimination",
                "Afrique de l'Est",
                "Tigréens Post-Conflit 2020-22 Langue Tigrigna Marginalisée Administration, Blocus Économique, Accès Services Réduit & Diaspora Tigréenne Poursuite Hors Frontières",
                55, 52, 58, 50,
            ),
            MinorityRightsEntity(
                "MR-006", "Espagne/Catalogne — Langue Catalane, Représailles Indépendantistes & Droits Culturels",
                "Europe de l'Ouest",
                "Langue Catalane Restrictions Certains Contextes, Leaders Indépendantistes Condamnés 9-13 Ans Prison 2017, Llarena Mandat Européen & Amnistie 2024 Débat Constitutionnel",
                52, 55, 50, 48,
            ),
            MinorityRightsEntity(
                "MR-007", "Kosovo/Serbes — Post-Indépendance Minorités, Protections EULEX & Tensions Persistantes",
                "Europe de l'Est",
                "Serbes Kosovo Minorité 5% Post-2008, Protections Constitutionnelles Partielles, Nord Kosovo Tensions KFOR, EULEX Mission & Intégration UE Conditionnée Droits Minorités",
                30, 28, 25, 30,
            ),
            MinorityRightsEntity(
                "MR-008", "CCPR/FCNM — Pacte Civil Art 27 Minorités & Convention-Cadre Minorités Nationales",
                "Global",
                "PIDCP Article 27 Droits Minorités, Convention-Cadre Protection Minorités Nationales CoE, Déclaration ONU 1992 Minorités Nationales & Comité Consultatif ONU Minorités",
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
            "domain": "minority_rights",
            "confidence_score": self.CONFIDENCE_SCORE,
            "data_sources": self.DATA_SOURCES,
            "entities": data,
            "avg_estimated_minority_rights_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = MinorityRightsEngine()
    result = engine.summary()
    print(json.dumps({
        "total": result["total_entities"],
        "avg": result["avg_composite"],
        "distribution": result["risk_distribution"],
        "top3": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
    for e in engine.entities:
        print(f"  {e.entity_id}: {e.composite_score:.2f} → {e.risk_level}")
