"""
Religious Persecution Engine — Caelum Partners Intelligence Platform
Auteure: Chaima Mhadbi | Bruxelles
Moteur d'analyse des persécutions religieuses systémiques : minorités, blasphème et génocide confessionnel
"""

from dataclasses import dataclass, field
from typing import List, Dict

PATTERNS: Dict[str, Dict[str, str]] = {
    "genocide_confessionnel": {
        "severity_fr": "Génocide Confessionnel",
        "action_fr": "Saisir la CPI pour crime contre l'humanité à caractère religieux et activer la Convention pour la Prévention du Génocide",
        "signal_fr": "Génocide confessionnel — destruction systématique d'une communauté religieuse par l'État incluant massacres, déportations et destruction des lieux de culte",
    },
    "blaspheme_peine_mort": {
        "severity_fr": "Lois Blasphème Peine de Mort",
        "action_fr": "Engager le Conseil des droits de l'homme de l'ONU pour résolution contraignante abolissant les lois de blasphème létales",
        "signal_fr": "Lois de blasphème à peine de mort — criminalisation de l'apostasie et du blasphème punissable de mort créant une terreur religieuse institutionnalisée",
    },
    "discrimination_institutionnelle_religieuse": {
        "severity_fr": "Discrimination Institutionnelle Religieuse",
        "action_fr": "Activer le Rapporteur Spécial ONU sur la liberté de religion pour mission d'enquête urgente",
        "signal_fr": "Discrimination institutionnelle religieuse — exclusion systémique des minorités confessionnelles des droits civiques, emplois publics et protections légales",
    },
    "persecution_religieus_active": {
        "severity_fr": "Persécution Religieuse Active",
        "action_fr": "Sanctionner les responsables via Global Magnitsky Act et saisir la Commission internationale pour la liberté religieuse",
        "signal_fr": "Persécution religieuse active — harcèlement, arrestations arbitraires et destruction de lieux de culte de minorités religieuses avec impunité étatique",
    },
    "liberte_religieuse_exemplaire": {
        "severity_fr": "Liberté Religieuse Exemplaire",
        "action_fr": "Partager les modèles législatifs de protection de la liberté religieuse et financer les mécanismes ONU de surveillance",
        "signal_fr": "Liberté religieuse exemplaire — toutes les confessions protégées légalement, lieux de culte respectés et aucune criminalisation de l'apostasie ou du blasphème",
    },
}


@dataclass
class ReligiousPersecutionActor:
    entity_id: str
    name: str
    country: str
    sector: str
    state_religious_violence_score: float
    blasphemy_apostasy_criminalization_score: float
    minority_institutional_exclusion_score: float
    religious_persecution_impunity_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.state_religious_violence_score * 0.30
            + self.blasphemy_apostasy_criminalization_score * 0.25
            + self.minority_institutional_exclusion_score * 0.25
            + self.religious_persecution_impunity_score * 0.20,
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
            "genocide_confessionnel": self.state_religious_violence_score,
            "blaspheme_peine_mort": self.blasphemy_apostasy_criminalization_score,
            "discrimination_institutionnelle_religieuse": self.minority_institutional_exclusion_score,
            "persecution_religieus_active": self.religious_persecution_impunity_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        p = PATTERNS.get(self.primary_pattern, PATTERNS["persecution_religieus_active"])
        base = p["signal_fr"]
        return [
            f"{base} de {self.name.split('/')[0] if '/' in self.name else self.name}",
            "Minorités religieuses ciblées — communautés confessionnelles subissant des violences systémiques, destructions de lieux de culte et exclusion des droits fondamentaux",
            p["action_fr"],
        ]

    @property
    def estimated_religious_persecution_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "state_religious_violence_score": self.state_religious_violence_score,
            "blasphemy_apostasy_criminalization_score": self.blasphemy_apostasy_criminalization_score,
            "minority_institutional_exclusion_score": self.minority_institutional_exclusion_score,
            "religious_persecution_impunity_score": self.religious_persecution_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_religious_persecution_index": self.estimated_religious_persecution_index,
            "last_updated": "2026-06-20",
        }


ACTORS: List[ReligiousPersecutionActor] = [
    ReligiousPersecutionActor("RP-001", "RPDC — Bibles Contrebande, Exécutions Culte & Christianisme Interdit", "Asie du Nord-Est",
        "Christianisme Peine de Mort, Bibles Contrebande Exécution, 70 000 Chrétiens Camps & Aucune Religion Autorisée Hors Culte Kim",
        95.0, 92.0, 90.0, 88.0),
    ReligiousPersecutionActor("RP-002", "Pakistan — Loi Blasphème 295-C & Minorités Chrétiennes/Ahmadis", "Asie du Sud",
        "295-C Peine Mort Blasphème, Ahmadis Non-Musulmans Légalement, Asia Bibi Condamnée & 4000+ Accusés Blasphème 1987-2023",
        85.0, 95.0, 85.0, 80.0),
    ReligiousPersecutionActor("RP-003", "Myanmar/Rohingyas — Génocide Musulmans & Mosquées Détruites", "Asie du Sud-Est",
        "Rohingyas Apatrides Loi 1982, 750+ Mosquées Détruites, Monjes Nationalistes Ma Ba Tha & ONU Génocide Déclaré 2018",
        92.0, 78.0, 85.0, 90.0),
    ReligiousPersecutionActor("RP-004", "Chine/Falun Gong-Chrétiens — Église Maison Interdite & Prélèvement Organes", "Asie",
        "10 000 Lieux Culte Démolis 2014-2020, Croix Abattues Zhejiang, Falun Gong Organes & Ouïghours Islam Interdit",
        82.0, 82.0, 88.0, 80.0),
    ReligiousPersecutionActor("RP-005", "Iran — Baha'is Persécutés, Apostasie Mort & Minorités", "MENA",
        "Baha'is 300+ Exécutés Révolution, Apostasie Peine Mort Fatwas, Chrétiens Convertis Emprisonnés & Dervishes Gonabadi",
        52.0, 65.0, 55.0, 52.0),
    ReligiousPersecutionActor("RP-006", "Inde/BJP — Lois Anti-Conversion & Violences Anti-Musulmans", "Asie du Sud",
        "Lois Anti-Conversion 12 États, Lynchages Vache Sacrée Impunis, Mosquées Démolies Gujarat & RSS Violences Documentées",
        55.0, 52.0, 58.0, 60.0),
    ReligiousPersecutionActor("RP-007", "Égypte/Coptes — Discrimination Institutionnelle & Attaques Églises", "MENA/Afrique",
        "Coptes 10% Population 0% Gouverneurs, Attentats Église Tanta 2017, Permis Construction Refusés & Quotas Discriminatoires",
        28.0, 25.0, 38.0, 30.0),
    ReligiousPersecutionActor("RP-008", "USCIRF/Rapporteur ONU — Liberté Religieuse & Dialogue Interconfessionnel", "Global",
        "USCIRF Rapport Annuel 180 Pays, Rapporteur ONU Liberté Religion Article 18 & Alliance Civilisations ONU Dialogue",
        5.0, 4.0, 3.0, 6.0),
]


def analyze_religious_persecution() -> dict:
    entities = [a.to_dict() for a in ACTORS]
    avg = round(sum(e["composite_score"] for e in entities) / len(entities), 2)
    risk_dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: Dict[str, int] = {}
    for e in entities:
        risk_dist[e["risk_level"]] = risk_dist.get(e["risk_level"], 0) + 1
        pattern_dist[e["primary_pattern"]] = pattern_dist.get(e["primary_pattern"], 0) + 1

    top_risk = sorted(entities, key=lambda x: x["composite_score"], reverse=True)[:3]
    critiques = [e for e in entities if e["risk_level"] == "critique"]

    return {
        "total_entities": len(entities),
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": [e["name"] for e in top_risk],
        "critical_alerts": [f"{e['name'].split('—')[0].strip()}: {PATTERNS.get(e['primary_pattern'], {}).get('severity_fr', e['primary_pattern'])}" for e in critiques],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "religious_persecution",
        "confidence_score": 0.83,
        "data_sources": [
            "uscirf_annual_report_countries_concern",
            "open_doors_world_watch_list",
            "un_special_rapporteur_religion_belief_reports",
        ],
        "entities": entities,
        "avg_estimated_religious_persecution_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    result = analyze_religious_persecution()
    print(f"Religious Persecution Engine — {result['total_entities']} acteurs, avg risque: {result['avg_composite']}")
    for e in result["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:60]} — score {e['composite_score']}")
    print(f"Distribution: {result['risk_distribution']}")
