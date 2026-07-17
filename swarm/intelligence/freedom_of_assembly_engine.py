"""Freedom of Assembly Engine — Wave 35"""

from dataclasses import dataclass, field
from typing import List
import json


@dataclass
class FreedomOfAssemblyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    protest_criminalization_score: float
    excessive_force_dispersal_score: float
    organizer_persecution_score: float
    emergency_law_abuse_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.protest_criminalization_score * 0.30
            + self.excessive_force_dispersal_score * 0.25
            + self.organizer_persecution_score * 0.25
            + self.emergency_law_abuse_score * 0.20,
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
            "criminalisation_manifestation": self.protest_criminalization_score,
            "force_excessive_dispersion": self.excessive_force_dispersal_score,
            "persecution_organisateurs": self.organizer_persecution_score,
            "abus_lois_urgence": self.emergency_law_abuse_score,
        }
        return max(scores, key=scores.get)

    @property
    def estimated_freedom_of_assembly_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "protest_criminalization_score": self.protest_criminalization_score,
            "excessive_force_dispersal_score": self.excessive_force_dispersal_score,
            "organizer_persecution_score": self.organizer_persecution_score,
            "emergency_law_abuse_score": self.emergency_law_abuse_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_freedom_of_assembly_index": self.estimated_freedom_of_assembly_index,
            "last_updated": "2026-06-20",
        }

    @property
    def key_signals(self) -> List[str]:
        signals = [
            f"Violation du droit de réunion documentée — {self.name} avec score composite {self.composite_score}/100 révélant une restriction systémique violant l'Article 20 de la DUDH et l'Article 21 du PIDCP sur le droit de réunion pacifique",
            f"Criminalisation des manifestations ({self.protest_criminalization_score}/100) — la répression légale ou de facto des rassemblements pacifiques constitue une violation directe du droit à la liberté de réunion garanti par le droit international des droits humains",
            "Activer le Rapporteur Spécial ONU sur les droits de réunion pacifique et d'association (Clément Nyaletsossi Voule) pour enquête urgente et exiger l'abrogation des lois restrictives incompatibles avec les normes PIDCP",
        ]
        return signals


ENTITIES = [
    FreedomOfAssemblyEntity("FA-001", "Chine/Hong Kong — NSL 2020, 10 000+ Arrestations Manifestants & Assemblée Interdite", "Asie du Nord-Est", "China National Security Law 2020 HK 10 000+ Arrestés, 55 Dirigeants Pro-Démocratie Condamnés, Article 23 2024 & Manifestations Place Tiananmen Interdites Continent", 95, 88, 95, 90),
    FreedomOfAssemblyEntity("FA-002", "Biélorussie/Loukachenko — 35 000 Arrestations 2020, Manifestants Torturés & ONG Dissoutes", "Europe de l'Est", "Biélorussie 2020 Fraude Électorale 35 000 Manifestants Arrêtés Loukachenko, Torture Documentée HRW, Syndicats/ONG Dissous & Lukashenko Réfugié Moscou", 90, 92, 88, 88),
    FreedomOfAssemblyEntity("FA-003", "Iran/Mahsa Amini — 20 000+ Arrestations 2022, 500+ Tués & Manifestants Pendus", "MENA", "Iran Révolution Femme-Vie-Liberté 2022 Mahsa Amini 500+ Morts, 20 000+ Arrestations, Manifestants Exécutés Pendaison & IRGC Tirs Balles Réelles Foules", 92, 88, 85, 90),
    FreedomOfAssemblyEntity("FA-004", "Myanmar/Tatmadaw — 5 000+ Tués Manifestants, CRPH & Coup État 2021", "Asie du Sud-Est", "Myanmar Coup 2021 Tatmadaw 5 000+ Manifestants Tués, 25 000+ Arrêtés, CRPH Gouvernement Parallèle & Tirs Balles Réelles Rassemblements Pacifiques CDM", 88, 95, 82, 85),
    FreedomOfAssemblyEntity("FA-005", "Russie/Anti-Guerre — 16 000+ Arrestations 2022, Loi Anti-Protestation & OVD-Info", "Europe de l'Est", "Russie Anti-Guerre Ukraine 16 000+ Arrestations 2022 OVD-Info, Loi 15 Ans Prison Anti-Armée, Manifestants Condamnés & Espace Public Réprimé Krasnodar/Moscou", 55, 52, 58, 62),
    FreedomOfAssemblyEntity("FA-006", "Éthiopie/Oromo-Amhara — Manifestants Tués, État Urgence 2021-23 & Restrictions", "Afrique de l'Est", "Éthiopie Manifestations Oromo Amhara 2021-23 Centaines Tués, États Urgence Répétés, Internet Coupé & NISS Arrestations Défenseurs Droits Réunion", 52, 55, 48, 58),
    FreedomOfAssemblyEntity("FA-007", "France/Gilets Jaunes-Retraites — LBD Mutilés, 11 000+ Gardes à Vue & ACAT Rapport", "Europe de l'Ouest", "France Gilets Jaunes 2018-19 + Réforme Retraites 2023, 11 000+ Gardes à Vue, LBD 300+ Blessés Graves Yeux/Mains & Conseil Constitutionnel Critiques", 28, 32, 25, 30),
    FreedomOfAssemblyEntity("FA-008", "OSCE/ODIHR-ONU — Rapporteur Spécial Réunion Pacifique & Guidelines Manifestations", "Global", "OSCE ODIHR Guidelines Liberté Réunion Pacifique, Rapporteur Spécial ONU Réunion Clément Nyaletsossi Voule, ICCPR Article 21 & Déclaration ONU Défenseurs Droits 1998", 5, 4, 3, 6),
]


def summary() -> dict:
    entities_data = [e.to_dict() for e in ENTITIES]
    avg = round(sum(e.composite_score for e in ENTITIES) / len(ENTITIES), 2)
    risk_dist = {}
    pattern_dist = {}
    for e in ENTITIES:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
    top = sorted(ENTITIES, key=lambda x: x.composite_score, reverse=True)[:3]
    critical = [e for e in ENTITIES if e.risk_level == "critique"]
    return {
        "total_entities": len(ENTITIES),
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": [e.name for e in top],
        "critical_alerts": [f"{e.name.split('—')[0].strip()}: {e.primary_pattern.replace('_', ' ')}" for e in critical],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "freedom_of_assembly",
        "confidence_score": 0.84,
        "data_sources": [
            "osce_odihr_freedom_of_assembly_reports",
            "un_special_rapporteur_peaceful_assembly_association",
            "civicus_monitor_civic_space_ratings",
        ],
        "entities": entities_data,
        "avg_estimated_freedom_of_assembly_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
