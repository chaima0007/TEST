"""
Caelum Partners — Healthcare Access Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Couverture universelle, effondrement infrastructures, pénurie personnel médical et accès médicaments essentiels.

Le droit à la santé est consacré par l'article 12 du Pacte international relatif aux droits
économiques, sociaux et culturels (PIDESC, 1966) et l'Objectif de Développement Durable n°3
(ODD-3 : Bonne santé et bien-être). La Couverture Sanitaire Universelle (CSU/UHC) constitue
le cadre opérationnel adopté par l'Assemblée générale des Nations Unies en 2019.

La Somalie compte 1 médecin pour 100 000 habitants, l'un des ratios les plus bas au monde
selon l'OMS 2023, avec une mortalité maternelle de 692 décès pour 100 000 naissances vivantes
— 25 fois supérieure à la moyenne mondiale. La République centrafricaine n'a que 3 médecins
pour 100 000 habitants et un taux de mortalité maternelle de 829 pour 100 000, le plus
élevé au monde selon l'OMS (2023). En Thaïlande, le système UHC introduit en 2002 couvre
99,5 % de la population avec une accessibilité financière totale — modèle de référence
mondiale cité par l'OMS comme exemple de couverture universelle effective dans un pays
à revenu intermédiaire.

Risk levels (accès aux soins de santé et droits à la vie) :
  critique  -> composite >= 60  (effondrement sanitaire total — mortalité évitable massive, droit à la vie violé)
  élevé     -> composite >= 40  (déficit structurel grave — inégalités d'accès persistantes et sous-financement chronique)
  modéré    -> composite >= 20  (couverture partielle — lacunes géographiques ou spécialisées avec système fonctionnel)
  faible    -> composite < 20   (UHC effective — couverture universelle équitable et accès aux soins garanti)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "effondrement_systeme_sante": {
        "severity_fr": "Critique",
        "action_fr": "Aide humanitaire d'urgence — déploiement MSF/OMS/UNICEF, reconstruction infrastructures hospitalières, formation accélérée personnels paramédicaux, fonds d'urgence médicaments essentiels et corridors humanitaires",
        "signal_fr": "universal_coverage_gap_score > 85 — absence quasi-totale de couverture sanitaire avec mortalité évitable massive et effondrement des systèmes de santé publique",
    },
    "infrastructure_sante_detruite": {
        "severity_fr": "Critique",
        "action_fr": "Reconstruction d'urgence — financement Banque Mondiale/BAD pour réhabilitation hôpitaux, protection infrastructures de santé en zones de conflit (DIH), déploiement hôpitaux de campagne et télémédecine d'urgence",
        "signal_fr": "healthcare_infrastructure_collapse_score > 85 — hôpitaux détruits par conflits ou négligence chronique, équipements obsolètes et chaîne du froid médicaments brisée",
    },
    "desert_medical_severe": {
        "severity_fr": "Critique",
        "action_fr": "Plan d'urgence ressources humaines — formation médecins communautaires, incitations financières pour zones rurales, programmes de retour diaspora médicale, partenariats facultés de médecine internationales",
        "signal_fr": "medical_personnel_shortage_score > 85 — ratio médecin/population inférieur à 5/100 000 (norme OMS : 44.5/100 000), déserts médicaux couvrant plus de 50% du territoire",
    },
    "acces_medicaments_bloque": {
        "severity_fr": "Élevé",
        "action_fr": "Approvisionnement médicaments — fonds OMS médicaments essentiels, négociation prix avec laboratoires pharmaceutiques, licences obligatoires génériques, renforcement chaîne logistique et stockage d'urgence",
        "signal_fr": "Ruptures chroniques de médicaments essentiels, prix prohibitifs pour les populations vulnérables et chaîne d'approvisionnement défaillante créant des traitements inaccessibles",
    },
    "uhc_effective_modele": {
        "severity_fr": "Faible",
        "action_fr": "Exporter les bonnes pratiques — financement OMS pour transférer les modèles UHC effectifs aux pays à faible revenu, partage d'expertise sur la tarification des soins, formation gestionnaires systèmes de santé",
        "signal_fr": "composite_score < 20 — couverture sanitaire universelle effective avec accès financier, géographique et qualitatif aux soins de santé primaires et spécialisés",
    },
}


@dataclass
class HealthcareAccessRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    universal_coverage_gap_score: float
    healthcare_infrastructure_collapse_score: float
    medical_personnel_shortage_score: float
    essential_medicines_access_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_healthcare_access_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.universal_coverage_gap_score * 0.30
            + self.healthcare_infrastructure_collapse_score * 0.25
            + self.medical_personnel_shortage_score * 0.25
            + self.essential_medicines_access_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_healthcare_access_rights_index = round(self.composite_score / 100 * 10, 2)

    def _risk(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    def _pattern(self) -> str:
        if self.universal_coverage_gap_score >= 85:
            return "effondrement_systeme_sante"
        if self.healthcare_infrastructure_collapse_score >= 85:
            return "infrastructure_sante_detruite"
        if self.medical_personnel_shortage_score >= 85:
            return "desert_medical_severe"
        if self.composite_score >= 20:
            return "acces_medicaments_bloque"
        return "uhc_effective_modele"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Effondrement sanitaire critique de {n} — absence quasi-totale d'accès aux soins de santé primaires violant le droit à la vie et à la santé garanti par l'article 12 du PIDESC et l'ODD-3",
                "Mortalité maternelle et infantile évitable — des centaines à des milliers de décès par an résultant de l'absence de personnel médical qualifié, d'équipements obstétriques et de médicaments essentiels",
                "Cercle vicieux santé-pauvreté — l'absence de système de santé fonctionnel perpétue la pauvreté en exposant les populations à des dépenses catastrophiques de santé ou à la mortalité prématurée",
            ]
        if self.risk_level == "élevé":
            return [
                f"Déficit structurel grave de {n} — inégalités d'accès persistantes entre zones urbaines et rurales, sous-financement chronique du système de santé public et dépendance aux financements extérieurs",
                "Fracture sanitaire géographique — les populations rurales et les communautés marginalisées n'ont pas accès aux spécialistes, équipements diagnostiques et médicaments disponibles dans les centres urbains",
                "Sous-financement systémique — les dépenses publiques de santé inférieures au seuil OMS de 86 dollars par habitant/an créent des déficits de soins chroniques malgré l'existence de structures formelles",
            ]
        if self.risk_level == "modéré":
            return [
                f"Couverture partielle de {n} — système de santé fonctionnel avec lacunes géographiques ou spécialisées nécessitant des réformes ciblées pour atteindre l'universalité effective",
                "Inégalités d'accès résiduelles — les populations rurales, ethniques et à faibles revenus subissent des barrières d'accès financières et géographiques que le système formel ne compense pas entièrement",
                "Réforme en cours — les programmes d'extension de couverture progressent mais l'universalité reste conditionnelle à la capacité contributive dans certains segments de la population",
            ]
        return [
            f"{n} incarne la couverture sanitaire universelle effective — accès financier, géographique et qualitatif aux soins garanti pour 99%+ de la population avec protection contre les dépenses catastrophiques",
            "Modèle UHC OMS — le système d'assurance universelle couvre soins primaires, hospitalisations et médicaments essentiels sans barrières financières, cité par l'OMS comme référence mondiale",
            "Impact santé publique — réduction drastique de la mortalité évitable, espérance de vie alignée sur les pays à revenus élevés malgré un PIB par habitant intermédiaire",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "universal_coverage_gap_score": self.universal_coverage_gap_score,
            "healthcare_infrastructure_collapse_score": self.healthcare_infrastructure_collapse_score,
            "medical_personnel_shortage_score": self.medical_personnel_shortage_score,
            "essential_medicines_access_score": self.essential_medicines_access_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_healthcare_access_rights_index": self.estimated_healthcare_access_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[HealthcareAccessRightsEntity] = [
    HealthcareAccessRightsEntity(
        "HAR-001",
        "Somalia/1 Médecin 100 000 Hab Infrastructure Effondrée",
        "Afrique de l'Est",
        "Ratio Médecin 1/100 000 (OMS: 44.5/1 000), Mortalité Maternelle 692/100k, Al-Shabaab Zones Inaccessibles, Hôpitaux Détruits & Épidémies Choléra Permanentes",
        92.0, 90.0, 94.0, 88.0,
    ),
    HealthcareAccessRightsEntity(
        "HAR-002",
        "Central African Republic/3 Médecins 100 000 Mortalité 829/100k",
        "Afrique Centrale",
        "3 Médecins/100 000, Mortalité Maternelle 829/100k (Plus Haute Monde OMS 2023), Groupes Armés Attaquent Hôpitaux, 80% Population Sans Accès Soins & Paludisme/VIH Épidémiques",
        88.0, 86.0, 88.0, 84.0,
    ),
    HealthcareAccessRightsEntity(
        "HAR-003",
        "Chad/0.4 Médecins 1 000 Déserts Médicaux 80% Territoire",
        "Afrique Centrale",
        "0.4 Médecins/1 000 Habitants, Déserts Médicaux 80% Territoire, Mortalité Maternelle 1 140/100k (2e Mondiale), Réfugiés Soudanais Pression Système & Épidémies Récurrentes",
        84.0, 82.0, 88.0, 80.0,
    ),
    HealthcareAccessRightsEntity(
        "HAR-004",
        "Sierra Leone/Mortalité Maternelle 443 Ebola Legacy",
        "Afrique de l'Ouest",
        "Mortalité Maternelle 443/100k, Ebola 2014-16 Détruit Personnel Médical, 2 Médecins/100 000, Accès Médicaments VIH/Paludisme Insuffisant & Infrastructure Post-Conflit Fragile",
        78.0, 76.0, 82.0, 74.0,
    ),
    HealthcareAccessRightsEntity(
        "HAR-005",
        "Haiti/Post-Ariel Henry Hôpitaux Détruits Choléra Retour",
        "Caraïbes",
        "Gangs Contrôlent 80% Port-au-Prince, Hôpitaux Principal HUP Non Fonctionnel, Choléra Retour 2022-2024, 0.3 Médecins/1 000 & Aide Humanitaire Bloquée Gangs",
        54.0, 56.0, 52.0, 50.0,
    ),
    HealthcareAccessRightsEntity(
        "HAR-006",
        "Indonesia/JKN Coverage Gaps Zones Rurales Spécialistes Urbains",
        "Asie du Sud-Est",
        "JKN Couverture 98% Nominale Mais Gaps Ruraux, Spécialistes Concentrés Java, Médicaments Listes Restrictives, Puskesmas Sous-Équipés & File Attente Chronique",
        48.0, 45.0, 50.0, 52.0,
    ),
    HealthcareAccessRightsEntity(
        "HAR-007",
        "Brazil/SUS Sous-Financé Inégalités Régionales Nord Sud",
        "Amérique du Sud",
        "SUS Constitutionnel Universel Mais Sous-Financé, Inégalités Nord/Amazonie Vs São Paulo, Files Attente Spécialistes 18 Mois, Dual System Public/Privé & Déficit Dentaires",
        30.0, 28.0, 32.0, 26.0,
    ),
    HealthcareAccessRightsEntity(
        "HAR-008",
        "Thailand/UHC 2002 Meilleure Pratique Mondiale OMS Citée",
        "Asie du Sud-Est",
        "UHC 2002 Couverture 99.5%, 0 Paiement Soins Primaires, Mortalité Maternelle 37/100k, 8 Médecins/10 000 & Cité OMS Modèle Pays Revenu Intermédiaire",
        10.0, 8.0, 12.0, 9.0,
    ),
]


def summary() -> dict[str, Any]:
    entities = MOCK_ENTITIES
    n = len(entities)
    avg = round(sum(e.composite_score for e in entities) / n, 2)

    risk_dist: dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: dict[str, int] = {k: 0 for k in PATTERNS}
    critical_alerts: list[str] = []
    top_risk: list[str] = []

    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        if e.risk_level == "critique":
            critical_alerts.append(f"{e.name}: {e.primary_pattern.replace('_', ' ')}")
            top_risk.append(e.name)

    return {
        "total_entities": n,
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-22",
        "engine_version": "1.0.0",
        "domain": "healthcare_access_rights",
        "confidence_score": 0.88,
        "data_sources": [
            "who_world_health_statistics_2023",
            "unicef_maternal_mortality_estimates_2023",
            "world_bank_universal_health_coverage_index",
            "msf_access_medicines_campaign_reports",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_healthcare_access_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_healthcare_access_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Healthcare Access Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
