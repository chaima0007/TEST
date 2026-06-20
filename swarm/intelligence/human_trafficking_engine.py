"""
Human Trafficking Engine — Caelum Partners Intelligence Platform
Auteure: Chaima Mhadbi | Bruxelles
Moteur d'analyse de la traite des êtres humains : esclavage moderne, exploitation sexuelle et travail forcé
"""

from dataclasses import dataclass, field
from typing import List, Dict

PATTERNS: Dict[str, Dict[str, str]] = {
    "traite_sexuelle_industrielle": {
        "severity_fr": "Traite Sexuelle à Échelle Industrielle",
        "action_fr": "Activer le Protocole de Palerme et engager Interpol/Europol pour démantèlement des réseaux transnationaux identifiés",
        "signal_fr": "Traite sexuelle à échelle industrielle — exploitation sexuelle commerciale de masse avec réseaux organisés de recrutement, transport et contrôle par la dette et la violence",
    },
    "esclavage_moderne_etatique": {
        "severity_fr": "Esclavage Moderne Étatique",
        "action_fr": "Saisir le Comité ONU contre l'esclavage et activer les sanctions commerciales via le mécanisme de l'ILO contre le travail forcé étatique",
        "signal_fr": "Esclavage moderne étatique — système de travail forcé institutionnalisé par l'État avec contrôle des travailleurs par la dette, la menace et la privation de liberté de mouvement",
    },
    "trafic_organes_cible": {
        "severity_fr": "Trafic d'Organes sur Commande",
        "action_fr": "Engager l'OMS et Interpol pour démantèlement des filières de transplantation illégale et poursuite des chirurgiens complices",
        "signal_fr": "Trafic d'organes sur commande — prélèvement forcé d'organes sur des prisonniers, migrants vulnérables ou personnes réduites en esclavage avec complicité médicale documentée",
    },
    "traite_travail_force": {
        "severity_fr": "Traite à des Fins de Travail Forcé",
        "action_fr": "Engager l'ILO pour enquête urgente et activer la Convention 29 sur le travail forcé contre les États et entreprises complices",
        "signal_fr": "Traite à des fins de travail forcé — recrutement frauduleux de travailleurs migrants réduits en esclavage dans des secteurs comme la construction, l'agriculture ou la pêche",
    },
    "protection_victimes_exemplaire": {
        "severity_fr": "Protection Exemplaire des Victimes",
        "action_fr": "Partager les modèles de protection et soutenir le Fonds de l'ONU pour les victimes de la traite (UNOCT)",
        "signal_fr": "Protection exemplaire des victimes de la traite — identification proactive des victimes, assistance inconditionnelle et poursuites effectives des trafiquants sans criminalisation des victimes",
    },
}


@dataclass
class HumanTraffickingActor:
    entity_id: str
    name: str
    country: str
    sector: str
    sexual_exploitation_network_score: float
    forced_labor_system_score: float
    state_complicity_impunity_score: float
    victim_identification_failure_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.sexual_exploitation_network_score * 0.30
            + self.forced_labor_system_score * 0.25
            + self.state_complicity_impunity_score * 0.25
            + self.victim_identification_failure_score * 0.20,
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
            "traite_sexuelle_industrielle": self.sexual_exploitation_network_score,
            "traite_travail_force": self.forced_labor_system_score,
            "esclavage_moderne_etatique": self.state_complicity_impunity_score,
            "trafic_organes_cible": self.victim_identification_failure_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        p = PATTERNS.get(self.primary_pattern, PATTERNS["traite_travail_force"])
        base = p["signal_fr"]
        return [
            f"{base} de {self.name.split('/')[0] if '/' in self.name else self.name}",
            "Victimes vulnérables ciblées — femmes et enfants des zones de pauvreté et de conflit recrutés par la tromperie et maintenus en esclavage par la dette et la menace",
            p["action_fr"],
        ]

    @property
    def estimated_human_trafficking_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "sexual_exploitation_network_score": self.sexual_exploitation_network_score,
            "forced_labor_system_score": self.forced_labor_system_score,
            "state_complicity_impunity_score": self.state_complicity_impunity_score,
            "victim_identification_failure_score": self.victim_identification_failure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_human_trafficking_index": self.estimated_human_trafficking_index,
            "last_updated": "2026-06-20",
        }


ACTORS: List[HumanTraffickingActor] = [
    HumanTraffickingActor("HT-001", "Corée du Nord/RPDC — Travailleurs Forcés Export & Camps Kwanliso", "Asie du Nord-Est",
        "100 000+ Travailleurs Forcés Export Russie/Chine, Kwanliso Travail Forcé Prisonniers, Devises Étrangères État & ONU Sanctions",
        85.0, 95.0, 92.0, 88.0),
    HumanTraffickingActor("HT-002", "Chine/Xinjiang — Transferts Forcés Ouïghours & Travail Coton", "Asie",
        "500 000+ Ouïghours Transferts Usines, Chaînes Approvisionnement Nike/H&M, Coton Xinjiang 20% Mondial & UFLPA Sanctions USA",
        82.0, 92.0, 90.0, 80.0),
    HumanTraffickingActor("HT-003", "Thaïlande/Mekong — Traite Sexuelle Industrielle & Karaokés", "Asie du Sud-Est",
        "300 000+ Victimes Estimées, Réseau GMS Myanmar/Laos/Cambodge, Tier 2 Watch List USA & Corruption Policière Systémique",
        95.0, 75.0, 82.0, 85.0),
    HumanTraffickingActor("HT-004", "Libye/Milices — Marchés Esclaves Migrants & Torture Rançons", "MENA/Afrique",
        "CNN Marché Esclaves Documenté 2017, Migrants Sub-Sahariens Vendus, OIM 3000+ Victimes & Milices Impunité Totale",
        80.0, 82.0, 90.0, 85.0),
    HumanTraffickingActor("HT-005", "Inde/Bonded Labor — 18M Esclaves Modernes Estimés", "Asie du Sud",
        "18M Bonded Labor ILO Estimé, Briqueteries Rajasthan Enfants, Kamaiya Système Népal & Dalits Ciblés Travail Ancestral Dette",
        50.0, 62.0, 48.0, 58.0),
    HumanTraffickingActor("HT-006", "Golfe/Qatar-Émirats — Kafala Travailleurs Migrants & Chantiers", "MENA",
        "Kafala Confiscation Passeports, 6750 Migrants Morts Qatar Stades, 3M Travailleurs Contrats Abusifs & Réformes Insuffisantes",
        50.0, 62.0, 52.0, 58.0),
    HumanTraffickingActor("HT-007", "Mexique/Cartels — Réseaux Migration Forcée & Exploitation", "Amérique du Nord",
        "Cartels 13B$/An Traite, Zetas Séquestrations Migrants, San Fernando 72 Corps & Femmes Recrutées Faux Emplois",
        35.0, 28.0, 30.0, 32.0),
    HumanTraffickingActor("HT-008", "UNODC/ILO — Protocole Palerme & Convention Travail Forcé", "Global",
        "Protocole Palerme 2000 178 États, ILO Convention 29 Travail Forcé, Blue Heart Campaign & Fonds Victimes UNOCT",
        5.0, 4.0, 3.0, 6.0),
]


def analyze_human_trafficking() -> dict:
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
        "domain": "human_trafficking",
        "confidence_score": 0.82,
        "data_sources": [
            "unodc_global_report_trafficking_persons",
            "ilo_global_estimates_modern_slavery",
            "us_state_department_tip_report",
        ],
        "entities": entities,
        "avg_estimated_human_trafficking_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    result = analyze_human_trafficking()
    print(f"Human Trafficking Engine — {result['total_entities']} acteurs, avg risque: {result['avg_composite']}")
    for e in result["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:60]} — score {e['composite_score']}")
    print(f"Distribution: {result['risk_distribution']}")
