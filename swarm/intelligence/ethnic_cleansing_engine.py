"""
Ethnic Cleansing Engine — Caelum Partners Intelligence Platform
Auteure: Chaima Mhadbi | Bruxelles
Moteur d'analyse du nettoyage ethnique : déplacements forcés, massacres et épuration démographique
"""

from dataclasses import dataclass, field
from typing import List, Dict

PATTERNS: Dict[str, Dict[str, str]] = {
    "epuration_ethnique_totale": {
        "severity_fr": "Épuration Ethnique Totale",
        "action_fr": "Activer d'urgence le mécanisme R2P (Responsabilité de Protéger) au Conseil de Sécurité et déclencher enquête CPI immédiate",
        "signal_fr": "Épuration ethnique totale — programme étatique délibéré visant à rendre un territoire ethniquement homogène par la violence, la terreur et les déplacements massifs forcés",
    },
    "massacre_demographique": {
        "severity_fr": "Massacre Démographique Ciblé",
        "action_fr": "Saisir la CPI pour génocide et demander déploiement force d'interposition onusienne d'urgence",
        "signal_fr": "Massacre démographique ciblé — élimination physique systématique d'une population ethnique avec intention documentée de destruction partielle ou totale du groupe",
    },
    "deplacement_force_massif": {
        "severity_fr": "Déplacement Forcé Massif",
        "action_fr": "Engager le HCR pour protection d'urgence et activer les principes directeurs relatifs au déplacement interne (Principes Deng)",
        "signal_fr": "Déplacement forcé massif — expulsion par la terreur de populations ethniques de leurs terres ancestrales créant des réfugiés et déplacés internes en violation du DIH",
    },
    "segregation_ethnique_institutionnalisee": {
        "severity_fr": "Ségrégation Ethnique Institutionnalisée",
        "action_fr": "Activer les mécanismes conventionnels CERD et demander mission d'enquête urgente du Comité pour l'élimination des discriminations raciales",
        "signal_fr": "Ségrégation ethnique institutionnalisée — système légal ou pratique administrative créant des citoyens de seconde zone fondé sur l'origine ethnique avec discrimination systémique",
    },
    "coexistence_ethnique_exemplaire": {
        "severity_fr": "Coexistence Ethnique Exemplaire",
        "action_fr": "Partager les bonnes pratiques de réconciliation interethnique et financer les programmes UNESCO de dialogue et coexistence",
        "signal_fr": "Coexistence ethnique exemplaire — égalité de droits pour toutes les ethnies, réconciliation post-conflit active et protections constitutionnelles des minorités effectives",
    },
}


@dataclass
class EthnicCleansingActor:
    entity_id: str
    name: str
    country: str
    sector: str
    forced_displacement_scale_score: float
    ethnic_massacre_documentation_score: float
    demographic_engineering_state_score: float
    ethnic_cleansing_impunity_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.forced_displacement_scale_score * 0.30
            + self.ethnic_massacre_documentation_score * 0.25
            + self.demographic_engineering_state_score * 0.25
            + self.ethnic_cleansing_impunity_score * 0.20,
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
            "deplacement_force_massif": self.forced_displacement_scale_score,
            "massacre_demographique": self.ethnic_massacre_documentation_score,
            "epuration_ethnique_totale": self.demographic_engineering_state_score,
            "segregation_ethnique_institutionnalisee": self.ethnic_cleansing_impunity_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        p = PATTERNS.get(self.primary_pattern, PATTERNS["deplacement_force_massif"])
        base = p["signal_fr"]
        return [
            f"{base} de {self.name.split('/')[0] if '/' in self.name else self.name}",
            "Populations ethniques déracinées — communautés expulsées de leurs terres ancestrales avec destruction systématique de leurs villages, archives et marqueurs identitaires",
            p["action_fr"],
        ]

    @property
    def estimated_ethnic_cleansing_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "forced_displacement_scale_score": self.forced_displacement_scale_score,
            "ethnic_massacre_documentation_score": self.ethnic_massacre_documentation_score,
            "demographic_engineering_state_score": self.demographic_engineering_state_score,
            "ethnic_cleansing_impunity_score": self.ethnic_cleansing_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_ethnic_cleansing_index": self.estimated_ethnic_cleansing_index,
            "last_updated": "2026-06-20",
        }


ACTORS: List[EthnicCleansingActor] = [
    EthnicCleansingActor("EC2-001", "Myanmar/Rohingyas — Opération Clearance & 700 000 Expulsés Bangladesh", "Asie du Sud-Est",
        "700 000 Rohingyas Expulsés 2017, Tula Toli Massacre 200+ Civils, Villages Brûlés Satellites Documentés & CPI Enquête 2019",
        95.0, 92.0, 90.0, 88.0),
    EthnicCleansingActor("EC2-002", "Bosnie/Serbes — Srebrenica 8000 Hommes & Épuration Nettoyée", "Europe",
        "Srebrenica 8372 Hommes Tués TPIY, 2M Déplacés Guerre 1992-95, Karadžić Condamné 40 Ans & Fosses Communes 570+",
        88.0, 95.0, 88.0, 80.0),
    EthnicCleansingActor("EC2-003", "Russie/Ukraine — Deportation Civils & Russification Occupée", "Europe de l'Est",
        "CPI Mandat Poutine Enfants, Marioupol Population Déportée, Territoires Occupés Russifiés & Civils Ukrainiens Filtration Camps",
        85.0, 80.0, 90.0, 82.0),
    EthnicCleansingActor("EC2-004", "Soudan/Darfour-Masalit — RSF Génocide 2023 & 11M Déplacés", "Afrique",
        "RSF Masalit Massacres El Fasher 2024, 11M Déplacés Plus Grand Crise Monde, Omar Al-Bashir CPI Génocide & Répétition Pattern",
        90.0, 88.0, 80.0, 85.0),
    EthnicCleansingActor("EC2-005", "Éthiopie/Tigré-Amhara — Famine Induite & Déplacements Ethniques", "Afrique de l'Est",
        "500 000 Morts Conflit 2020-22, 2M Déplacés Tigré, Famine Induite ONU & Amhara-Tigré Violence Ethnique Réciproque",
        55.0, 58.0, 52.0, 62.0),
    EthnicCleansingActor("EC2-006", "Israël/Gaza-Cisjordanie — Colonisation Cisjordanie & Déplacements", "MENA",
        "700 000 Colons Cisjordanie Illégaux, Maisons Démolies 55 000+ Depuis 1967, 1.7M Gaza Déplacés 2023-24 & CIJ Ordonnances",
        55.0, 52.0, 58.0, 60.0),
    EthnicCleansingActor("EC2-007", "Centrafrique/Anti-Balaka — Violences Intercommunautaires Cycliques", "Afrique Centrale",
        "Musulmans Expulsés Bangui 2013-14, Anti-Balaka Chrétiennes Attaques, MINUSCA Protection Partielle & Impunité Locale Haute",
        28.0, 25.0, 32.0, 35.0),
    EthnicCleansingActor("EC2-008", "TPIY/TPIR/CPI — Justice Transitionnelle & Prévention Génocide", "Global",
        "TPIY 161 Mis en Examen, TPIR 93 Condamnés, Mécanisme ONU 2010 & Réseau Alerte Précoce Atrocités OSAPG",
        5.0, 4.0, 3.0, 6.0),
]


def analyze_ethnic_cleansing() -> dict:
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
        "domain": "ethnic_cleansing",
        "confidence_score": 0.87,
        "data_sources": [
            "icty_ictr_icc_case_database",
            "unhcr_global_displacement_report",
            "un_osapg_atrocity_prevention_framework",
        ],
        "entities": entities,
        "avg_estimated_ethnic_cleansing_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    result = analyze_ethnic_cleansing()
    print(f"Ethnic Cleansing Engine — {result['total_entities']} acteurs, avg risque: {result['avg_composite']}")
    for e in result["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:60]} — score {e['composite_score']}")
    print(f"Distribution: {result['risk_distribution']}")
