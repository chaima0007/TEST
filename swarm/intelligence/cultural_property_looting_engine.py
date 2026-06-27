"""Cultural Property Looting Engine — Caelum Partners Intelligence Swarm"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class CulturalPropertyLootingActor:
    entity_id: str
    name: str
    country: str
    sector: str
    systematic_heritage_destruction_score: float
    illicit_antiquities_trafficking_score: float
    museum_archive_seizure_score: float
    restitution_refusal_impunity_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.systematic_heritage_destruction_score * 0.30 +
            self.illicit_antiquities_trafficking_score * 0.25 +
            self.museum_archive_seizure_score * 0.25 +
            self.restitution_refusal_impunity_score * 0.20,
            2
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60: return "critique"
        if s >= 40: return "élevé"
        if s >= 20: return "modéré"
        return "faible"

    @property
    def estimated_cultural_property_looting_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def primary_pattern(self) -> str:
        scores = {
            "destruction_patrimoine_systematique": self.systematic_heritage_destruction_score,
            "trafic_antiquites_illicite": self.illicit_antiquities_trafficking_score,
            "saisie_musees_archives": self.museum_archive_seizure_score,
            "refus_restitution": self.restitution_refusal_impunity_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        SIGNAL_MAP = {
            "destruction_patrimoine_systematique": f"Destruction systématique du patrimoine par {self.name} — élimination délibérée des vestiges culturels et identitaires des populations comme forme d'effacement de la mémoire collective",
            "trafic_antiquites_illicite": f"Trafic illicite d'antiquités par {self.name} — extraction et vente de biens culturels vers les marchés internationaux finançant les conflits et privant les peuples de leur héritage",
            "saisie_musees_archives": f"Saisie de musées et archives par {self.name} — pillage institutionnalisé des collections nationales et archives historiques lors d'occupations ou de conflits armés",
            "refus_restitution": f"Refus de restitution par {self.name} — rétention de biens culturels pillés malgré les demandes légitimes des pays d'origine et les résolutions UNESCO contraignantes",
        }
        return [
            SIGNAL_MAP.get(self.primary_pattern, f"Pillage culturel de {self.name}"),
            "Crime de guerre et crime culturel — la destruction et le pillage délibérés du patrimoine constituent des crimes de guerre selon le Protocole II de La Haye 1954 et l'Article 8 du Statut de Rome",
            "Activer l'UNESCO et INTERPOL Works of Art pour listes noires et demandes de restitution urgentes via la Convention UNIDROIT 1995 sur les biens culturels volés",
        ]

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "systematic_heritage_destruction_score": self.systematic_heritage_destruction_score,
            "illicit_antiquities_trafficking_score": self.illicit_antiquities_trafficking_score,
            "museum_archive_seizure_score": self.museum_archive_seizure_score,
            "restitution_refusal_impunity_score": self.restitution_refusal_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_cultural_property_looting_index": self.estimated_cultural_property_looting_index,
            "last_updated": "2026-06-20",
        }


ACTORS = [
    CulturalPropertyLootingActor("CP-001", "Daech/ISIS — Palmyre Destruction, Mossoul Musée & Trafic Financement Territorial", "MENA", "Palmyre Colonnes Dynamitées 2015, Musée Mossoul Bulldozer, 100M$ Antiquités Vendues Daesh & Louvre Abu Dhabi Provenance Enquête", 95, 92, 88, 82),
    CulturalPropertyLootingActor("CP-002", "Russie/Ukraine — Musées Marioupol Pillés, Archives Kherson & Crimée Collections", "Europe de l'Est", "Musée Marioupol 2000 Œuvres Volées, Kherson Musée Pillé 2022, Crimée Collections Transférées Moscou & Heritage Mapping UA 50 000 Sites", 88, 80, 92, 90),
    CulturalPropertyLootingActor("CP-003", "Afghanistan/Taliban — Musée Kaboul, Bouddhas Bamiyan & Sites Préislamiques", "Asie Centrale", "Bouddhas Bamiyan Explosés 2001, Musée Kaboul 70% Collection Volée, Sites Bactres/Aï Khanoum Pillés & Taliban Ban Archéologie Étrangère", 92, 85, 82, 80),
    CulturalPropertyLootingActor("CP-004", "Irak/Post-2003 — Musée Baghdad Pillage, Ninive & Sites Sumériens Creusés", "MENA", "Musée National Baghdad 15 000 Pièces Pillées 2003, Ninive Sites Lourd, Ur Ziggurat Endommagé Base US & Christie's Provenance Enquêtes", 85, 90, 88, 80),
    CulturalPropertyLootingActor("CP-005", "Royaume-Uni/France — Marbres Elgin, Buste Néfertiti & Restitutions Refusées", "Europe", "Marbres Elgin British Museum Refus Grèce, Buste Néfertiti Berlin Refus Égypte, Benin Bronzes Partiellement Restitués & Loi 2002 Inaliénabilité", 52, 55, 48, 88),
    CulturalPropertyLootingActor("CP-006", "Mali/Sahel — Tombouctou Mosquées Détruites & Trafic Via Réseaux Sahara", "Afrique de l'Ouest", "Tombouctou Mosquées CPI Condamnation 2016, Manuscrits Sauvés ONG, Trafic Via Niger/Algérie & Sites Dogon Fouilles Clandestines", 58, 62, 48, 52),
    CulturalPropertyLootingActor("CP-007", "Chine/Tibet-Xinjiang — Monastères Rasés & Effacement Patrimoine Culturel", "Asie", "Monastères Tibétains Détruits Révolution Culturelle, Mosquées Xinjiang Démolies 2017-22, Lhassa Urbanisation Effacement & Littérature Interdite", 32, 28, 35, 28),
    CulturalPropertyLootingActor("CP-008", "UNESCO/INTERPOL — Convention La Haye 1954 & Protection Patrimoine", "Global", "Convention La Haye 133 États, INTERPOL Works Art Database, CPI Condamnation Tombouctou 2016 & UNESCO Liste Rouge Urgence", 5, 4, 3, 6),
]


def summary() -> dict:
    entities = [a.to_dict() for a in ACTORS]
    scores = [a.composite_score for a in ACTORS]
    avg = round(sum(scores) / len(scores), 2)
    risk_dist: dict = {}
    pattern_dist: dict = {}
    for a in ACTORS:
        risk_dist[a.risk_level] = risk_dist.get(a.risk_level, 0) + 1
        pattern_dist[a.primary_pattern] = pattern_dist.get(a.primary_pattern, 0) + 1
    top3 = sorted(ACTORS, key=lambda x: x.composite_score, reverse=True)[:3]
    critiques = [a for a in ACTORS if a.risk_level == "critique"]
    return {
        "total_entities": len(ACTORS),
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": [a.name for a in top3],
        "critical_alerts": [f"{a.name.split(' —')[0]}: {a.primary_pattern.replace('_', ' ')}" for a in critiques],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "cultural_property_looting",
        "confidence_score": 0.80,
        "data_sources": ["interpol_works_of_art_database", "unesco_cultural_heritage_protection_reports", "asor_cultural_heritage_initiatives_reports"],
        "entities": entities,
        "avg_estimated_cultural_property_looting_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Cultural Property Looting Engine — {s['total_entities']} acteurs, avg risque: {s['avg_composite']}")
    for e in s["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:50]} — score {e['composite_score']}")
    print(f"Distribution: {s['risk_distribution']}")
