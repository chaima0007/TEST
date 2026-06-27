"""Refugee Rights Engine — droits des réfugiés, asile & Convention 1951."""

from dataclasses import dataclass
from typing import List


@dataclass
class RefugeeRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    refugee_protection_failure_score: float
    pushback_refoulement_score: float
    detention_conditions_score: float
    integration_rights_denial_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-20"

    @property
    def composite_score(self) -> float:
        return round(
            self.refugee_protection_failure_score * 0.30
            + self.pushback_refoulement_score * 0.25
            + self.detention_conditions_score * 0.25
            + self.integration_rights_denial_score * 0.20,
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
    def estimated_refugee_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "refugee_protection_failure_score": self.refugee_protection_failure_score,
            "pushback_refoulement_score": self.pushback_refoulement_score,
            "detention_conditions_score": self.detention_conditions_score,
            "integration_rights_denial_score": self.integration_rights_denial_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_refugee_rights_index": self.estimated_refugee_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    RefugeeRightsEntity(
        "RF-001", "Syrie/Liban — 5.9M Réfugiés Syriens, Retours Forcés & Statut Apatridie",
        "MENA",
        "Liban 1.5M Réfugiés Syriens 25% Population, Pression Retours Forcés 2023-24, Enfants Apatrides Non-Enregistrés, Restrictions Déplacement Liban & HCR Alertes Refoulement Zones Dangereuses",
        90.0, 85.0, 88.0, 92.0,
        "integration_rights_denial",
        [
            "Violation des droits des réfugiés documentée — Syrie/Liban avec score composite 88.65/100 révélant des violations systémiques de la Convention de Genève 1951 avec des pressions de retours forcés vers une Syrie encore dangereuse, violant le principe de non-refoulement",
            "Déni intégration/Droits (92.0/100) — les restrictions de déplacement imposées aux réfugiés syriens au Liban et les enfants apatrides non-enregistrés constituent des violations de l'Article 26 (liberté de circulation) et de l'Article 28 (documents de voyage) de la Convention de 1951",
            "Activer le Haut-Commissariat aux Réfugiés (HCR) pour surveillance des retours syriens et exiger du Liban le respect du principe de non-refoulement (Article 33 Convention 1951) en tant qu'obligation de droit international coutumier contraignante même sans ratification",
        ],
    ),
    RefugeeRightsEntity(
        "RF-002", "Rohingya/Bangladesh — 1M Cox's Bazar, Apatridie Myanmar & Retours Impossibles",
        "Asie du Sud/Asie du Sud-Est",
        "Bangladesh 1M+ Rohingyas Cox's Bazar, Apatridie Myanmar Citoyenneté Refusée, Retours Impossibles Conditions Myanmar, Bangladesh Non-Signataire Convention 1951 & HCR Accès Limité",
        92.0, 88.0, 90.0, 85.0,
        "refugee_protection_failure",
        [
            "Violation des droits des réfugiés documentée — Rohingya/Bangladesh avec score composite 89.10/100 révélant la situation d'un million de Rohingyas apatrides dans les camps de Cox's Bazar, le Bangladesh n'ayant pas ratifié la Convention de 1951 et refusant leur intégration permanente",
            "Défaillance protection réfugiés (92.0/100) — la privation de citoyenneté des Rohingyas par le Myanmar (Loi de 1982) et l'impossibilité de retour créent une population d'1 million d'apatrides sans aucun cadre juridique de protection efficace, violant le droit international des réfugiés",
            "Activer le Haut-Commissariat aux Réfugiés (HCR) pour surveillance et pression sur le Bangladesh pour ratifier la Convention 1951 et sur le Myanmar pour restaurer la citoyenneté rohingya conformément aux résolutions de la CIJ dans l'affaire Gambie c. Myanmar",
        ],
    ),
    RefugeeRightsEntity(
        "RF-003", "Venezuela/Colombie — 7.7M Déplacés, Criminalisation Migration & Xénophobie",
        "Amérique Latine",
        "Venezuela 7.7M Personnes Déplacées 2024 Plus Grande Crise Am. Latine, Colombie 2.4M Vénézuéliens, Criminalisation Migration Équateur/Pérou/Chili, Xénophobie Montante & Accès Santé Bloqué",
        88.0, 82.0, 80.0, 85.0,
        "refugee_protection_failure",
        [
            "Violation des droits des réfugiés documentée — Venezuela/Colombie avec score composite 83.90/100 révélant la plus grande crise de déplacement d'Amérique latine avec 7.7 millions de Vénézuéliens et une montée de xénophobie violant la Convention de Carthagène de 1984",
            "Défaillance protection réfugiés (88.0/100) — la criminalisation des migrants vénézuéliens en Équateur, Pérou et Chili et les obstacles d'accès aux soins de santé constituent des violations de la Convention de Carthagène de 1984 offrant une protection élargie aux réfugiés en Amérique latine",
            "Activer le Haut-Commissariat aux Réfugiés (HCR) pour surveillance et pression sur les États d'accueil pour respecter la Convention de Carthagène et le Pacte mondial sur les réfugiés en garantissant l'accès à l'asile et aux services essentiels aux Vénézuéliens déplacés",
        ],
    ),
    RefugeeRightsEntity(
        "RF-004", "Afghanistan/Pakistan — 3.7M Réfugiés, Expulsions Forcées & Taliban Persécution",
        "Asie Centrale/Asie du Sud",
        "Pakistan Expulsion Forcée 1.7M Afghans 2023-24, Afghanistan 3.7M Déplacés Internes Taliban, Femmes/Journalistes Persécutés, Frontière Iran Fermée & Retours Sans Garanties Sécurité",
        90.0, 88.0, 85.0, 82.0,
        "refugee_protection_failure",
        [
            "Violation des droits des réfugiés documentée — Afghanistan/Pakistan avec score composite 86.65/100 révélant les expulsions forcées de 1.7 million d'Afghans depuis le Pakistan vers un pays contrôlé par les Taliban, violant le principe absolu de non-refoulement de la Convention 1951",
            "Défaillance protection réfugiés (90.0/100) — les expulsions forcées massives de réfugiés afghans depuis le Pakistan et l'Iran vers l'Afghanistan taliban constituent une violation du principe de non-refoulement (Article 33 Convention 1951), obligation de jus cogens ne souffrant aucune dérogation",
            "Activer le Haut-Commissariat aux Réfugiés (HCR) pour surveillance des expulsions pakistanaises et exiger la suspension immédiate des expulsions vers l'Afghanistan conformément au principe absolu de non-refoulement reconnu comme norme impérative du droit international (jus cogens)",
        ],
    ),
    RefugeeRightsEntity(
        "RF-005", "Méditerranée — 28 000 Morts 2014-24, Push-Backs Grèce/Italie & Frontex Complicité",
        "Europe/MENA",
        "Méditerranée 28 000 Personnes Noyées 2014-24 OIM, Push-Backs Illégaux Grèce/Croatie/Italie, Frontex Complicité Documentée OLAF, Accord UE-Tunisie/Libye Externalisation & Triton Réduit",
        55.0, 62.0, 52.0, 50.0,
        "pushback_refoulement",
        [
            "Violation des droits des réfugiés documentée — Méditerranée avec score composite 55.00/100 révélant 28 000 personnes noyées depuis 2014 et des push-backs illégaux documentés par l'OLAF impliquant directement Frontex, violant l'Article 33 de la Convention de 1951",
            "Push-back/Refoulement (62.0/100) — les opérations de push-back illégales en Mer Égée et Adriatique conduisant à des noyades et violant le principe absolu de non-refoulement (Article 33 Convention 1951) et l'Article 3 CEDH sur l'interdiction des traitements inhumains",
            "Activer le Haut-Commissariat aux Réfugiés (HCR) pour surveillance et pression sur l'UE pour respecter le principe de non-refoulement, mettre fin aux accords d'externalisation avec la Libye et la Tunisie et établir des voies légales d'accès à l'asile en Europe",
        ],
    ),
    RefugeeRightsEntity(
        "RF-006", "USA/Mexique — Titre 42, Séparation Familles & Centres Rétention Privés",
        "Amérique du Nord",
        "USA Titre 42 Expulsions 2.5M 2020-23 Sans Procédure Asile, Séparation Familles 5 500 Enfants Séparés, Centres Rétention ICE Privés 34 000 Places & Décisions Asile 3-5 Ans Attente",
        52.0, 55.0, 58.0, 48.0,
        "detention_conditions",
        [
            "Violation des droits des réfugiés documentée — USA/Mexique avec score composite 53.45/100 révélant l'utilisation du Titre 42 pour expulser 2.5 millions de personnes sans procédure d'asile et la séparation de 5 500 enfants de leurs parents, violant la Convention de 1951",
            "Détention/Conditions (58.0/100) — les 34 000 places de rétention ICE dans des centres privés et les délais d'attente de 3-5 ans pour les décisions d'asile constituent des violations du droit à un recours effectif et des standards humanitaires minimaux pour les demandeurs d'asile",
            "Activer le Haut-Commissariat aux Réfugiés (HCR) pour surveillance et pression sur les USA pour ratifier le Protocole de 1967 de la Convention de 1951 et mettre fin aux politiques de détention arbitraire des demandeurs d'asile contraires aux standards internationaux",
        ],
    ),
    RefugeeRightsEntity(
        "RF-007", "Australie — Offshore Nauru/PNG, Internement Indéfini & Pacific Solution II",
        "Pacifique",
        "Australie Offshore Detention Nauru/PNG Illégal ONU 2016, Internement Indéfini Réfugiés, Pacific Solution II Morrison, 1 000+ Personnes Détenues 10+ Ans & Coûts 500 000$/Réfugié/An",
        28.0, 32.0, 35.0, 25.0,
        "detention_conditions",
        [
            "Violation des droits des réfugiés documentée — Australie avec score composite 30.15/100 révélant le système offshore de détention à Nauru et en Papouasie-Nouvelle-Guinée déclaré illégal par l'ONU en 2016 mais maintenu, violant la Convention de 1951 et les standards du Comité contre la torture",
            "Détention/Conditions (35.0/100) — l'internement indéfini de réfugiés dans des centres offshore à Nauru et PNG coûtant 500 000 AUD par personne par an constitue une violation de l'Article 31 de la Convention 1951 prohibant les pénalités pour entrée irrégulière des réfugiés",
            "Mettre fin au système de détention offshore australien conformément aux décisions ONU 2016 et adopter des voies légales d'accès à la protection conforme à la Convention de 1951 et aux recommandations du HCR sur la gestion humaine des arrivées maritimes",
        ],
    ),
    RefugeeRightsEntity(
        "RF-008", "HCR/Convention 1951 — Non-Refoulement, Protocole 1967 & Pacte Mondial Réfugiés",
        "Global",
        "HCR Convention Statut Réfugiés 1951, Protocole 1967 Extension Universelle, Principes Non-Refoulement, Pacte Mondial Réfugiés 2018 & Agenda Protection Globale Déplacés",
        5.0, 4.0, 3.0, 6.0,
        "integration_rights_denial",
        [
            "HCR/Convention 1951 incarne le cadre normatif exemplaire des droits des réfugiés — principe de non-refoulement et 42 droits garantis par la Convention créant une architecture internationale de protection que 149 États ont ratifiée, définissant le statut et les droits des personnes déracinées",
            "Convention de 1951 Article 33 — interdit de manière absolue le refoulement d'un réfugié vers un territoire où il risque des persécutions, constituant une norme impérative du droit international (jus cogens) s'appliquant à tous les États même non-signataires",
            "Universaliser la ratification de la Convention de 1951 et de son Protocole de 1967, renforcer le financement du HCR et mettre en œuvre le Pacte mondial sur les réfugiés de 2018 incluant des mécanismes de partage des responsabilités entre États pour les situations de déplacement massif",
        ],
    ),
]


def summary() -> dict:
    avg = round(sum(e.composite_score for e in ENTITIES) / len(ENTITIES), 2)
    risk_dist: dict = {}
    pattern_dist: dict = {}
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
        "domain": "refugee_rights",
        "confidence_score": 0.85,
        "data_sources": [
            "unhcr_global_trends_forced_displacement_annual_report",
            "iom_missing_migrants_project_mediterranean_database",
            "refworld_committee_against_torture_individual_communications",
        ],
        "entities": [e.to_dict() for e in ENTITIES],
        "avg_estimated_refugee_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
