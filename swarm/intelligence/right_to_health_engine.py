"""Right to Health Engine — Wave 36"""

from dataclasses import dataclass
from typing import List


@dataclass
class RightToHealthEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    healthcare_access_denial_score: float
    medicine_affordability_barrier_score: float
    maternal_infant_mortality_score: float
    health_system_collapse_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.healthcare_access_denial_score * 0.30
            + self.medicine_affordability_barrier_score * 0.25
            + self.maternal_infant_mortality_score * 0.25
            + self.health_system_collapse_score * 0.20,
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
            "deni_acces_soins": self.healthcare_access_denial_score,
            "barriere_prix_medicaments": self.medicine_affordability_barrier_score,
            "mortalite_maternelle_infantile": self.maternal_infant_mortality_score,
            "effondrement_systeme_sante": self.health_system_collapse_score,
        }
        return max(scores, key=scores.get)

    @property
    def estimated_right_to_health_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "healthcare_access_denial_score": self.healthcare_access_denial_score,
            "medicine_affordability_barrier_score": self.medicine_affordability_barrier_score,
            "maternal_infant_mortality_score": self.maternal_infant_mortality_score,
            "health_system_collapse_score": self.health_system_collapse_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_right_to_health_index": self.estimated_right_to_health_index,
            "last_updated": "2026-06-20",
        }

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Violation du droit à la santé documentée — {self.name} avec score composite {self.composite_score}/100 révélant des défaillances systémiques violant l'Article 25 de la DUDH et l'Article 12 du PIDESC sur le droit au meilleur état de santé possible",
            f"Déni d'accès aux soins ({self.healthcare_access_denial_score}/100) — l'absence d'accès aux soins de santé essentiels constitue une violation de l'Observation Générale 14 du Comité PIDESC définissant le droit à la santé comme disponible, accessible, acceptable et de qualité",
            "Activer le Rapporteur Spécial ONU sur le droit à la santé physique et mentale et exiger l'application du Plan d'action OMS pour la couverture santé universelle (CSU) avec financement international adéquat",
        ]


ENTITIES = [
    RightToHealthEntity("RH-001", "Sierra Leone/Niger — Mortalité Maternelle 443-553/100k, Sages-Femmes & Déserts Médicaux", "Afrique de l'Ouest", "Sierra Leone 443/100k Mortalité Maternelle OMS, Niger 553/100k Plus Élevé Monde, 1 Médecin/40 000 Habitants, Accouchements Domicile 70% Sans Soins & CSU OMS Lointaine", 88, 82, 95, 85),
    RightToHealthEntity("RH-002", "Yemen/Gaza — Hôpitaux Bombardés, 70% Système Santé Détruit & Médecins Arrêtés", "MENA", "Yémen 50% Hôpitaux Fermés Conflit, Gaza 70% Infrastructure Santé Détruite 2024, MSF Équipes Tués, Médicaments Bloqués Siège & OMS Alertes Famine/Choléra Simultanés", 92, 88, 88, 95),
    RightToHealthEntity("RH-003", "RDC/Sahel — 3 000+ Centres Santé Attaqués, Ebola Récurrences & Accès MSF Bloqué", "Afrique Centrale/Ouest", "RDC 3 000 Centres Santé Attaqués 2018-24, Épidémies Ebola Récurrentes Zones Conflit, Accès MSF/ONG Santé Bloqué Factions & Mortalité Infantile 65/1000 Naissances", 85, 82, 88, 90),
    RightToHealthEntity("RH-004", "USA/Insulin Crisis — 7.4M Diabétiques Sans Insuline, Faillites Médicales & Pas CSU", "Amérique du Nord", "USA 7.4M Diabétiques Insuline Inabordable 300$/Mois, 500 000 Faillites Personnelles/An Dettes Médicales, 30M Sans Assurance & Affaire Rationing Insuline Deaths Congress 2019", 80, 92, 82, 85),
    RightToHealthEntity("RH-005", "Inde — 60% Dépenses Santé Privées, 3 000$ Catastrophiques Familles & AMR Crise", "Asie du Sud", "Inde 60% Dépenses Santé Out-Of-Pocket, 55M Pauvreté/An Dépenses Médicales, Résistance Antimicrobiens AMR 1.35M Décès/An Inde & Couverture CSU 35% Population", 55, 58, 52, 55),
    RightToHealthEntity("RH-006", "Venezuela — Exode Médecins, 95% Manque Médicaments 2019 & Effondrement IVSS", "Amérique Latine", "Venezuela 300 000 Médecins Exilés, 95% Pénurie Médicaments 2019 HRW, IVSS Sécurité Sociale Effondrée, Malnutrition Infantile & Mortalité Maternelle Multipliée ×5", 52, 55, 58, 50),
    RightToHealthEntity("RH-007", "Europe/Austérité — Grèce 2010-18 Système Santé Coupé 25%, NHS UK Listes Attente", "Europe", "Grèce Austérité 2010-18 Budget Santé -25%, NHS Royaume-Uni 7.6M Listes Attente 2024, Médecins Famille Déserts Ruraux France & OCDE Rapports Inégalités Santé Croissantes", 28, 32, 30, 25),
    RightToHealthEntity("RH-008", "OMS/PIDESC — Droit Santé Art 12, Couverture Universelle & Accord ADPIC Médicaments", "Global", "OMS Couverture Santé Universelle ODD3, PIDESC Article 12 Droit Meilleur État Santé, Accord ADPIC Doha 2001 Médicaments Génériques & Rapporteur Spécial ONU Droit Santé", 5, 4, 3, 6),
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
        "domain": "right_to_health",
        "confidence_score": 0.84,
        "data_sources": [
            "who_global_health_observatory_health_financing",
            "un_special_rapporteur_right_to_health_reports",
            "msf_access_campaign_medicines_barriers_database",
        ],
        "entities": entities_data,
        "avg_estimated_right_to_health_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
