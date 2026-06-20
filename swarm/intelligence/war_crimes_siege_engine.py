"""
War Crimes Siege Engine — Caelum Partners Intelligence Platform
Auteure: Chaima Mhadbi | Bruxelles
Moteur d'analyse des crimes de guerre : sièges, famine induite, attaques hôpitaux et boucliers humains
"""

from dataclasses import dataclass, field
from typing import List, Dict

PATTERNS: Dict[str, Dict[str, str]] = {
    "siege_famine_arme": {
        "severity_fr": "Siège & Famine Comme Arme de Guerre",
        "action_fr": "Activer en urgence la résolution 2417 du CS-ONU sur la famine comme arme de guerre et saisir la CPI pour crimes contre l'humanité",
        "signal_fr": "Siège et famine comme arme de guerre — blocus délibéré de populations civiles privées de nourriture, eau et soins médicaux pour obtenir une reddition, crime de guerre selon l'Article 8 du Statut de Rome",
    },
    "attaques_hopitaux_protegees": {
        "severity_fr": "Attaques Systématiques d'Infrastructures Protégées",
        "action_fr": "Engager le mécanisme de dénonciation ICRC et demander ouverture d'une enquête CPI pour violations graves des Conventions de Genève",
        "signal_fr": "Attaques systématiques d'hôpitaux et écoles — bombardement délibéré d'infrastructures civiles protégées par le droit international humanitaire générant des victimes civiles massives",
    },
    "boucliers_humains_forces": {
        "severity_fr": "Utilisation de Boucliers Humains",
        "action_fr": "Documenter via UNAMI/OCHA et saisir le Comité International de la Croix-Rouge pour médiation urgente",
        "signal_fr": "Utilisation de boucliers humains — placement délibéré de civils ou de prisonniers de guerre dans des sites militaires pour décourager les frappes adverses, violation grave du DIH",
    },
    "execution_prisonniers_guerre": {
        "severity_fr": "Exécutions Sommaires de Prisonniers de Guerre",
        "action_fr": "Activer la Convention de Genève III et saisir la CPI pour crimes de guerre visant les prisonniers de guerre",
        "signal_fr": "Exécutions sommaires de prisonniers de guerre — meurtres documentés de combattants capturés en violation de la Convention de Genève III avec impunité totale des auteurs",
    },
    "droit_humanitaire_respecte": {
        "severity_fr": "Respect Exemplaire du Droit Humanitaire",
        "action_fr": "Partager les manuels opérationnels de respect du DIH et former les forces armées partenaires aux obligations des Conventions de Genève",
        "signal_fr": "Respect exemplaire du droit international humanitaire — forces armées respectant les principes de distinction, proportionnalité et précaution avec enquêtes indépendantes sur tout incident",
    },
}


@dataclass
class WarCrimesSiegeActor:
    entity_id: str
    name: str
    country: str
    sector: str
    deliberate_civilian_targeting_score: float
    siege_starvation_tactics_score: float
    protected_site_attack_score: float
    war_crimes_impunity_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.deliberate_civilian_targeting_score * 0.30
            + self.siege_starvation_tactics_score * 0.25
            + self.protected_site_attack_score * 0.25
            + self.war_crimes_impunity_score * 0.20,
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
            "siege_famine_arme": self.siege_starvation_tactics_score,
            "attaques_hopitaux_protegees": self.protected_site_attack_score,
            "boucliers_humains_forces": self.deliberate_civilian_targeting_score,
            "execution_prisonniers_guerre": self.war_crimes_impunity_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        p = PATTERNS.get(self.primary_pattern, PATTERNS["siege_famine_arme"])
        base = p["signal_fr"]
        return [
            f"{base} de {self.name.split('/')[0] if '/' in self.name else self.name}",
            "Violations graves des Conventions de Genève — les crimes de guerre documentés créent une responsabilité pénale individuelle pour les commandants selon le principe de responsabilité de commandement",
            p["action_fr"],
        ]

    @property
    def estimated_war_crimes_siege_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "deliberate_civilian_targeting_score": self.deliberate_civilian_targeting_score,
            "siege_starvation_tactics_score": self.siege_starvation_tactics_score,
            "protected_site_attack_score": self.protected_site_attack_score,
            "war_crimes_impunity_score": self.war_crimes_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_war_crimes_siege_index": self.estimated_war_crimes_siege_index,
            "last_updated": "2026-06-20",
        }


ACTORS: List[WarCrimesSiegeActor] = [
    WarCrimesSiegeActor("WC-001", "Russie/Ukraine — Marioupol Siège, Hôpitaux Bombardés & Civils Ciblés", "Europe de l'Est",
        "Marioupol Siège 80 Jours, 100+ Hôpitaux Bombardés OMS, Bucha Exécutions Civils & Mandat CPI Poutine 2023",
        95.0, 92.0, 90.0, 88.0),
    WarCrimesSiegeActor("WC-002", "Syrie/Assad — Siège Yarmouk, Armes Chimiques & Hôpitaux Rasés", "MENA",
        "Siège Yarmouk 560 Jours, 50+ Hôpitaux Détruits MSF, Sarin Ghouta 2013 & Double Tap Tactique Documentée",
        90.0, 95.0, 92.0, 85.0),
    WarCrimesSiegeActor("WC-003", "Gaza/Israël — Hôpitaux Al-Shifa, Famine Induite & Infrastructure Détruite", "MENA",
        "Al-Shifa Hôpital Assiégé, 2M Déplacés Nord/Sud, 70% Infrastructure Détruite & CIJ Mesures Provisoires Ordonnées 2024",
        88.0, 90.0, 88.0, 85.0),
    WarCrimesSiegeActor("WC-004", "Soudan/RSF — Khartoum Pillages, Civils Massa & Famine 2024", "Afrique",
        "RSF Khartoum Pillages Hôpitaux, Massacre Massa 1000+ Civils, Famine IPC5 Déclarée & 11M Déplacés Urgence Mondiale",
        85.0, 88.0, 82.0, 90.0),
    WarCrimesSiegeActor("WC-005", "Éthiopie/Tigré — Siège Alimentaire, Viol Arme & Ambulances Attaquées", "Afrique de l'Est",
        "Siège Alimentaire Tigré 2021, Viols Systémiques Arme Guerre, MSF Ambulances Attaquées & 500 000 Morts Estimés",
        55.0, 62.0, 52.0, 62.0),
    WarCrimesSiegeActor("WC-006", "Yémen/Coalition — Frappes Mariages, Ports Bloqués & Cholera", "MENA",
        "Frappes 140 Mariages/Funérailles, Hodeida Port Bloqué Famine, ONU Panel d'Experts Violations & Cholera 2.5M Cas",
        55.0, 58.0, 62.0, 55.0),
    WarCrimesSiegeActor("WC-007", "Afghanistan/Taliban — Restrictions Femmes & Aide Humanitaire Bloquée", "Asie Centrale",
        "Femmes Bannie ONG Humanitaires, Aide ONU Bloquée Décret, Education Filles Interdite & Famine 15M Personnes",
        28.0, 38.0, 22.0, 32.0),
    WarCrimesSiegeActor("WC-008", "CICR/CPI — Conventions Genève & Justice Humanitaire Internationale", "Global",
        "4 Conventions Genève 196 États, CPI 124 États, Résolution 2417 CS-ONU Famine & ICRC Accès Humanitaire",
        5.0, 4.0, 3.0, 6.0),
]


def analyze_war_crimes_siege() -> dict:
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
        "domain": "war_crimes_siege",
        "confidence_score": 0.88,
        "data_sources": [
            "icc_otp_situation_reports",
            "un_commission_inquiry_reports",
            "airwars_civilian_harm_database",
        ],
        "entities": entities,
        "avg_estimated_war_crimes_siege_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    result = analyze_war_crimes_siege()
    print(f"War Crimes Siege Engine — {result['total_entities']} acteurs, avg risque: {result['avg_composite']}")
    for e in result["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:60]} — score {e['composite_score']}")
    print(f"Distribution: {result['risk_distribution']}")
