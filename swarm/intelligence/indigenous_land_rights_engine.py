"""Indigenous Land Rights Engine — Droits fonciers autochtones & dépossession territoriale."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class IndigenousLandRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    territorial_dispossession_score: float
    resource_extraction_impact_score: float
    legal_recognition_failure_score: float
    environmental_destruction_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.territorial_dispossession_score * 0.30
            + self.resource_extraction_impact_score * 0.25
            + self.legal_recognition_failure_score * 0.25
            + self.environmental_destruction_score * 0.20,
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
            "depossession_territoriale": self.territorial_dispossession_score,
            "extraction_ressources_illegale": self.resource_extraction_impact_score,
            "non_reconnaissance_juridique": self.legal_recognition_failure_score,
            "destruction_ecosystemes_sacres": self.environmental_destruction_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Dépossession territoriale autochtone — {self.name} avec score composite {self.composite_score}/100 révélant une violation systémique des droits fonciers ancestraux protégés par la DNUDPA (Article 26) et les conventions OIT 169",
            f"Extraction sans consentement — le score d'impact d'extraction ({self.resource_extraction_impact_score}/100) indique des activités extractives conduites sans Consentement Libre, Préalable et Éclairé (CLPE) des communautés autochtones",
            f"Activer le Mécanisme Expert ONU sur les Droits des Peuples Autochtones pour enquête urgente et exiger le respect du CLPE dans tous les projets d'extraction sur terres ancestrales conformément à la DNUDPA 2007",
        ]

    @property
    def estimated_indigenous_land_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "territorial_dispossession_score": self.territorial_dispossession_score,
            "resource_extraction_impact_score": self.resource_extraction_impact_score,
            "legal_recognition_failure_score": self.legal_recognition_failure_score,
            "environmental_destruction_score": self.environmental_destruction_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_indigenous_land_rights_index": self.estimated_indigenous_land_rights_index,
            "last_updated": "2026-06-20",
        }


class IndigenousLandRightsEngine:
    ENGINE_VERSION = "1.0.0"
    CONFIDENCE_SCORE = 0.83
    DATA_SOURCES = [
        "un_sr_indigenous_peoples_2023",
        "forest_peoples_programme_2022",
        "cultural_survival_2023",
        "land_rights_now_2022",
    ]

    def __init__(self):
        self.entities: List[IndigenousLandRightsEntity] = [
            IndigenousLandRightsEntity(
                "IL-001", "Brésil/Amazonie — 1 000+ Terres Autochtones Menacées, Garimpos Illégaux & Défenseurs Assassinés",
                "Amérique du Sud",
                "1 000+ Terres Autochtones Démarcation Bloquée Bolsonaro 2019-22, Garimpos Or Illégaux Yanomami 30 000 Contaminés Mercure, 60+ Défenseurs Tués/An Global Witness & FUNAI Démantelée",
                95, 92, 88, 95,
            ),
            IndigenousLandRightsEntity(
                "IL-002", "Canada/Premières Nations — Traités Non-Respectés, Pipeline Trans Mountain & RCAANC",
                "Amérique du Nord",
                "Traités Territoriaux Historiques Canada Non-Respectés, Pipeline Trans Mountain Terres Wet'suwet'en Sans CLPE, 215+ Corps Enfants Kamloops 2021 & RCAANC Consultation Factice",
                88, 85, 92, 85,
            ),
            IndigenousLandRightsEntity(
                "IL-003", "Papouasie/Indonésie — Déforestation Forêts Papouanes, Transmigration & Mines Freeport",
                "Asie du Sud-Est",
                "Forêts Papouanes Déforestées Mine Freeport-McMoRan Grasberg, Transmigration Javanaise 1M+ Colons Terres Ancestrales, PT Freeport Royalties Insuffisantes & Militarisation Résistance",
                85, 90, 88, 88,
            ),
            IndigenousLandRightsEntity(
                "IL-004", "Philippines/Lumad — IPRA Non-Appliqué, Mines Mindanao & Déplacements Forcés",
                "Asie du Sud-Est",
                "IPRA 1997 Droits Ancêtres Lumad Non-Appliqué, Mines Nickel/Or Mindanao Terres Ancestrales, 3 000+ Déplacements Forcés Conflits & Militarisation Écoles Autochtones Documentée",
                82, 85, 82, 85,
            ),
            IndigenousLandRightsEntity(
                "IL-005", "Kenya/Maasaï — Ngorongoro Expulsions, Terres Touristiques & Consentement Absent",
                "Afrique de l'Est",
                "Maasaï Ngorongoro Conservation Area Expulsions 2022 Sans CLPE, Terres Ancestrales Cédées Tourisme Safari, USAID Financements Réinstallation & Opposition Internationale Ignorée",
                55, 52, 58, 50,
            ),
            IndigenousLandRightsEntity(
                "IL-006", "Australie/Autochtones — Fracking Northern Territory, Sites Sacrés & Land Rights Act",
                "Océanie",
                "Aboriginal Land Rights Act 1976 Contourné Fracking NT, Juukan Gorge Sites Sacrés Rio Tinto Détruites 2020, Northern Territory Intervention & Lacunes Native Title Act Veto Minier",
                52, 55, 50, 55,
            ),
            IndigenousLandRightsEntity(
                "IL-007", "Nouvelle-Zélande/Māori — Waitangi Partiellement Respecté & Progrès He Puapua",
                "Océanie",
                "Traité Waitangi 1840 Application Partielle 60% Terres Ancestrales Perdues, He Puapua Plan Droits Autochtones 2021, Whanganui River Personnalité Juridique & Co-Gouvernance Progrès",
                28, 30, 25, 30,
            ),
            IndigenousLandRightsEntity(
                "IL-008", "UNPFII/UNDRIP — Déclaration ONU 2007 Droits Peuples Autochtones & Mécanisme Expert",
                "Global",
                "DNUDPA 2007 147 Votes Pour, UNPFII Forum Permanent ONU, Mécanisme Expert Droits Peuples Autochtones & CLPE Standard International Consentement Libre Préalable Éclairé",
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
            "domain": "indigenous_land_rights",
            "confidence_score": self.CONFIDENCE_SCORE,
            "data_sources": self.DATA_SOURCES,
            "entities": data,
            "avg_estimated_indigenous_land_rights_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = IndigenousLandRightsEngine()
    result = engine.summary()
    print(json.dumps({
        "total": result["total_entities"],
        "avg": result["avg_composite"],
        "distribution": result["risk_distribution"],
        "top3": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
    for e in engine.entities:
        print(f"  {e.entity_id}: {e.composite_score:.2f} → {e.risk_level}")
