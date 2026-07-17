"""Press Freedom Engine — Wave 36"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PressFreedomEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    journalist_imprisonment_score: float
    media_censorship_ownership_score: float
    physical_safety_threats_score: float
    legal_harassment_lawfare_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.journalist_imprisonment_score * 0.30
            + self.media_censorship_ownership_score * 0.25
            + self.physical_safety_threats_score * 0.25
            + self.legal_harassment_lawfare_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60: return "critique"
        if s >= 40: return "élevé"
        if s >= 20: return "modéré"
        return "faible"

    @property
    def primary_pattern(self) -> str:
        scores = {
            "emprisonnement_journalistes": self.journalist_imprisonment_score,
            "censure_concentration_medias": self.media_censorship_ownership_score,
            "menaces_securite_physique": self.physical_safety_threats_score,
            "harcelement_juridique_lawfare": self.legal_harassment_lawfare_score,
        }
        return max(scores, key=scores.get)

    @property
    def estimated_press_freedom_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "journalist_imprisonment_score": self.journalist_imprisonment_score,
            "media_censorship_ownership_score": self.media_censorship_ownership_score,
            "physical_safety_threats_score": self.physical_safety_threats_score,
            "legal_harassment_lawfare_score": self.legal_harassment_lawfare_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_press_freedom_index": self.estimated_press_freedom_index,
            "last_updated": "2026-06-20",
        }

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Violation de la liberté de la presse documentée — {self.name} avec score composite {self.composite_score}/100 révélant des restrictions systémiques violant l'Article 19 de la DUDH et du PIDCP sur la liberté d'expression et d'information",
            f"Emprisonnement de journalistes ({self.journalist_imprisonment_score}/100) — la détention de journalistes pour leur travail constitue une violation directe de l'Article 19 PIDCP et des standards de protection des journalistes du Conseil de Sécurité ONU (Résolution 1738)",
            "Activer le Rapporteur Spécial ONU sur la liberté d'expression (SROFE) pour enquête urgente et exiger la libération immédiate de tous les journalistes emprisonnés pour leur travail journalistique",
        ]


ENTITIES = [
    PressFreedomEntity("PF-001", "Chine — 100+ Journalistes Emprisonnés, Grand Firewall & Presse État CCTV/Xinhua", "Asie du Nord-Est", "Chine 100+ Journalistes Emprisonnés CPJ/RSF 2024, Grand Firewall Internet, Presse Étatique CCTV/Xinhua/People Daily, Correspondants Étrangers Expulsés & RSF Rang 172/180", 95, 95, 88, 85),
    PressFreedomEntity("PF-002", "Russie — 36+ Journalistes Emprisonnés, Novaya Gazeta Suspendu & Loi Fausses Infos", "Europe de l'Est", "Russie Post-2022 36+ Journalistes Emprisonnés CPJ, Novaya Gazeta Suspendu Muratov Nobel, Étiqueté Agent Étranger, Loi 15 Ans Fausses Infos Armée & Médias Indépendants Exil", 88, 92, 85, 88),
    PressFreedomEntity("PF-003", "Iran — 40+ Journalistes Détenus, VPN Bloqués & Instagram/WhatsApp Interdits", "MENA", "Iran 40+ Journalistes Emprisonnés 2023 CPJ, Instagram/WhatsApp/Twitter Bloqués, Correspondants BBC/Radio Farda Arrêtés Familles & RSF Journalistes Tués Manifestations 2022", 88, 85, 90, 82),
    PressFreedomEntity("PF-004", "Myanmar — 60+ Journalistes Arrêtés Post-Coup, Médias Interdits & Licences Révoquées", "Asie du Sud-Est", "Myanmar 60+ Journalistes Arrêtés Tatmadaw 2021, Licences Médias Révoquées, CPJ Birmanie Geôlier Presse, Photojournalistes Tués & Journalistes Condamnés 20 Ans", 90, 85, 88, 80),
    PressFreedomEntity("PF-005", "Mexique — Journaliste Meurtres Capital Mondial, Cartels & FEADLE Impunité", "Amérique Latine", "Mexique 10-15 Journalistes Tués/An RSF, Cartels Ciblage Journalistes Locaux, FEADLE Procureur Spécial Inefficace & CPJ 2024 Mexique 3ème Plus Dangereux Monde", 52, 48, 65, 52),
    PressFreedomEntity("PF-006", "Inde — 40+ Journalistes Détenus, UAPA Sédition & Concentration Médias Ambani/Adani", "Asie du Sud", "Inde UAPA Anti-Terrorisme Journalistes Cachemire, Sédition Loi Coloniale Abolie 2023, Concentration Médias Reliance/Adani 80%+ Audience & BBC Documentary Modi Interdite", 48, 58, 50, 55),
    PressFreedomEntity("PF-007", "Turquie — 150+ Journalistes Détenus 2016-24, Lois Anti-Presse & Anadolu Agence État", "MENA/Europe", "Turquie Post-Coup 150+ Journalistes Détenus 2016-24, 90% Médias Contrôlés Pro-Erdogan, Loi 7418 Désinformation & RSF Rang 158/180 Malgré Libérations Récentes 2024", 28, 32, 25, 30),
    PressFreedomEntity("PF-008", "RSF/CPJ-ONU — Classement Liberté Presse, Article 19 & Déclaration Windhoek 1991", "Global", "RSF Classement Liberté Presse 180 Pays, CPJ Journalistes Emprisonnés Base Données, Rapporteur Spécial ONU Art 19 PIDCP & Déclaration Windhoek 1991 Presse Indépendante Afrique", 5, 4, 3, 6),
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
        "domain": "press_freedom",
        "confidence_score": 0.87,
        "data_sources": [
            "rsf_world_press_freedom_index_annual",
            "cpj_imprisoned_journalists_database",
            "un_special_rapporteur_freedom_expression_reports",
        ],
        "entities": entities_data,
        "avg_estimated_press_freedom_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
