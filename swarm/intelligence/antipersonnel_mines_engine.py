"""
Antipersonnel Mines Engine — Caelum Partners Intelligence Platform
Auteure: Chaima Mhadbi | Bruxelles
Moteur d'analyse des mines antipersonnel, armes à sous-munitions et munitions non explosées
"""

from dataclasses import dataclass, field
from typing import List, Dict

PATTERNS: Dict[str, Dict[str, str]] = {
    "contamination_massive_civils": {
        "severity_fr": "Contamination Massive Zones Civiles",
        "action_fr": "Activer le mécanisme d'urgence de déminage humanitaire UNMAS et saisir le Comité de mise en œuvre du Traité d'Ottawa",
        "signal_fr": "Contamination massive de zones civiles par mines/sous-munitions — déploiement délibéré d'engins explosifs aveugles dans des zones peuplées générant des victimes civiles durables",
    },
    "refus_traite_minage": {
        "severity_fr": "Refus du Traité d'Ottawa & Production Active",
        "action_fr": "Engager une pression diplomatique multilatérale et activer les mécanismes de la Convention sur les armes conventionnelles pour contraindre l'adhésion",
        "signal_fr": "Refus du Traité d'Ottawa avec production active — fabrication et stockage massif de mines antipersonnel par des États non signataires sans obligation de déminage ni transparence",
    },
    "sous_munitions_urbaines": {
        "severity_fr": "Armes à Sous-Munitions en Zone Urbaine",
        "action_fr": "Saisir le mécanisme de la Convention d'Oslo sur les armes à sous-munitions et demander cessation immédiate des frappes en zones peuplées",
        "signal_fr": "Usage d'armes à sous-munitions en zones urbaines — déploiement de bombes à fragmentation dans des agglomérations civiles avec taux de ratés élevé créant une pollution explosive durable",
    },
    "engins_improvises_massifs": {
        "severity_fr": "IED Massifs & Engins Improvisés",
        "action_fr": "Renforcer les capacités CIED (Counter-IED) via OTAN/UNMAS et activer les mécanismes de sanction contre les fournisseurs de matériaux explosifs aux groupes armés",
        "signal_fr": "Engins explosifs improvisés massifs — fabrication et déploiement à grande échelle d'IED ciblant les populations civiles et les forces de sécurité avec effets durables sur la mobilité",
    },
    "deminage_exemplaire": {
        "severity_fr": "Déminage Humanitaire Exemplaire",
        "action_fr": "Partager les méthodologies de déminage et augmenter les contributions au Fonds GICHD pour accélérer la dépollution dans les pays les plus affectés",
        "signal_fr": "Programme de déminage exemplaire — adhésion au Traité d'Ottawa, financement actif du déminage humanitaire et assistance aux victimes selon les standards IMAS",
    },
}


@dataclass
class AntipersonnelMinesActor:
    entity_id: str
    name: str
    country: str
    sector: str
    active_mine_deployment_score: float
    civilian_contamination_area_score: float
    treaty_noncompliance_production_score: float
    victim_clearance_impunity_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.active_mine_deployment_score * 0.30
            + self.civilian_contamination_area_score * 0.25
            + self.treaty_noncompliance_production_score * 0.25
            + self.victim_clearance_impunity_score * 0.20,
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
            "contamination_massive_civils": self.active_mine_deployment_score,
            "sous_munitions_urbaines": self.civilian_contamination_area_score,
            "refus_traite_minage": self.treaty_noncompliance_production_score,
            "engins_improvises_massifs": self.victim_clearance_impunity_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        p = PATTERNS.get(self.primary_pattern, PATTERNS["contamination_massive_civils"])
        base = p["signal_fr"]
        return [
            f"{base} de {self.name.split('/')[0] if '/' in self.name else self.name}",
            "Victimes civiles longue durée — les mines et sous-munitions non explosées continuent de tuer et mutiler des civils des décennies après la fin des conflits",
            p["action_fr"],
        ]

    @property
    def estimated_antipersonnel_mines_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "active_mine_deployment_score": self.active_mine_deployment_score,
            "civilian_contamination_area_score": self.civilian_contamination_area_score,
            "treaty_noncompliance_production_score": self.treaty_noncompliance_production_score,
            "victim_clearance_impunity_score": self.victim_clearance_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_antipersonnel_mines_index": self.estimated_antipersonnel_mines_index,
            "last_updated": "2026-06-20",
        }


ACTORS: List[AntipersonnelMinesActor] = [
    AntipersonnelMinesActor("AM-001", "Russie/Ukraine — Mines OZM-72 & Sous-Munitions Zones Civiles", "Europe de l'Est",
        "Mines Pétales POM-3 Kherson, MLRS BM-21 Sous-Munitions Villes, 174 000 km² Contaminés HRW & Non Signataire Ottawa",
        95.0, 92.0, 90.0, 85.0),
    AntipersonnelMinesActor("AM-002", "Yémen/Houthis — Mines Maritimes & IED Résidentiels", "MENA",
        "Mines Maritimes Détroit Bab-el-Mandeb, IED Routes Civiles Taiz, 100 000+ Zones Contaminées & ONU Liste Noire Persistante",
        88.0, 85.0, 82.0, 90.0),
    AntipersonnelMinesActor("AM-003", "Myanmar/Tatmadaw — Mines Villages Ethniques & Champs Cultivés", "Asie du Sud-Est",
        "Mines Frontières Karen/Kachin, Villages Ethniques Contaminés, HRW 2020-24 Documentation & Non Signataire Ottawa",
        85.0, 88.0, 82.0, 80.0),
    AntipersonnelMinesActor("AM-004", "Syrie/Assad — Barils Explosifs & Sous-Munitions Alep", "MENA",
        "Su-25 Sous-Munitions Alep/Idlib, Barils Explosifs Hmeimim, 700+ km² Contaminés & OIAC Documentation",
        82.0, 85.0, 80.0, 88.0),
    AntipersonnelMinesActor("AM-005", "Afghanistan/Taliban — Mines Soviétiques Résiduelles & IED", "Asie Centrale",
        "10M Mines Résiduelles Guerre 1979-89, Taliban IED Routes, HALO Trust 2M Mines Neutralisées & 2400 Victimes/An Pic",
        55.0, 72.0, 50.0, 62.0),
    AntipersonnelMinesActor("AM-006", "Colombie/FARC Résiduels — Mines Zones Rurales & Démineurs Tués", "Amérique du Sud",
        "FARC Mines Plantations Cocaïne, 12 000+ Victimes Mines 1990-2023, Accords 2016 Déminage & ELN Poursuit Déploiement",
        50.0, 58.0, 52.0, 55.0),
    AntipersonnelMinesActor("AM-007", "Angola/Post-Conflit — 15M Mines Héritées Guerre Civile", "Afrique Australe",
        "15M Mines Estimées Guerre 27 Ans, 84 000 Victimes Enregistrées, NPA Déminage Actif & Ottawa Signataire 2002",
        28.0, 32.0, 22.0, 35.0),
    AntipersonnelMinesActor("AM-008", "UNMAS/HALO Trust — Déminage & Traité Ottawa", "Global",
        "Ottawa Treaty 164 États Parties, UNMAS 40+ Pays, HALO Trust 3M Mines Neutralisées & Landmine Monitor Annuel",
        5.0, 4.0, 3.0, 6.0),
]


def analyze_antipersonnel_mines() -> dict:
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
        "domain": "antipersonnel_mines",
        "confidence_score": 0.85,
        "data_sources": [
            "landmine_cluster_munition_monitor_annual",
            "unmas_annual_report_mine_action",
            "hrw_explosive_weapons_civilian_harm",
        ],
        "entities": entities,
        "avg_estimated_antipersonnel_mines_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    result = analyze_antipersonnel_mines()
    print(f"Antipersonnel Mines Engine — {result['total_entities']} acteurs, avg risque: {result['avg_composite']}")
    for e in result["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:60]} — score {e['composite_score']}")
    print(f"Distribution: {result['risk_distribution']}")
