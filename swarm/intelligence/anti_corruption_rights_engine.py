"""
Caelum Partners — Anti-Corruption Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Corruption par pots-de-vin, détournement fonds publics, corruption judiciaire et faiblesse institutionnelle.

La corruption systémique constitue une violation grave des droits économiques, civils et
politiques des populations, consacrés par la Convention des Nations Unies contre la corruption
(CNUCC, 2003) et les Principes directeurs de l'OCDE sur la gouvernance d'entreprise.
Transparency International publie depuis 1995 l'Indice de Perception de la Corruption (IPC)
mesurant les niveaux perçus de corruption dans le secteur public de 180 pays.

La Somalie occupe depuis 2012 la dernière place de l'IPC avec un score de 11/100 en 2023,
reflétant un État défaillant total où les institutions publiques sont soit inexistantes soit
entièrement capturées par des réseaux claniques et des milices armées.
Au Venezuela, la corruption pétrolière systémique autour de PDVSA a permis le détournement
de plus de 300 milliards de dollars selon le Département de Justice américain (DOJ), plaçant
le pays au 170e rang sur 180 de l'IPC 2023.
Au Mexique, 97 % des crimes restent impunis selon le think tank IMCO (2023), avec des cartels
corrompant fonctionnaires, forces de l'ordre, procureurs et juges à tous les niveaux.
Le Danemark, la Finlande et la Nouvelle-Zélande occupent conjointement les premiers rangs
de l'IPC (87-90/100), incarnant les meilleures pratiques mondiales de gouvernance intègre.

Risk levels (corruption systémique et droits civiques et économiques) :
  critique  -> composite >= 60  (capture totale de l'État — kleptocracie, impunité absolue, pillage systématique)
  élevé     -> composite >= 40  (corruption institutionnalisée — pots-de-vin structurels et détournements récurrents)
  modéré    -> composite >= 20  (déficits de gouvernance — lacunes institutionnelles sans capture totale de l'État)
  faible    -> composite < 20   (gouvernance intègre — standards anti-corruption effectivement appliqués et sanctionnés)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "etat_capturé_kleptocracie": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions internationales ciblées — gel avoirs dirigeants kleptocrates, exclusion marchés financiers internationaux, soutien juridictions universelles pour poursuites, mécanismes CNUCC recouvrement avoirs Art.57 et pression diplomatique maximale",
        "signal_fr": "bribery_systemic_score > 85 — État entièrement capturé par des réseaux criminels au pouvoir utilisant les institutions comme instruments d'enrichissement et d'oppression politique",
    },
    "detournement_massif_fonds_publics": {
        "severity_fr": "Critique",
        "action_fr": "Traçabilité financière internationale — GAFI renforcé sur flux illicites, coopération judiciaire internationale accélérée, sanctions des intermédiaires financiers complices, registres publics bénéficiaires effectifs et restitution aux États victimes",
        "signal_fr": "public_fund_embezzlement_score > 85 — détournement massif de fonds publics via contrats surfacturés, marchés manipulés et transferts offshore vers paradis fiscaux",
    },
    "corruption_judiciaire_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Réforme judiciaire d'urgence — financement international cours anti-corruption spécialisées indépendantes, protection physique magistrats intègres, formation judiciaire, sanctions pays refusant extraditions pour corruption",
        "signal_fr": "judicial_corruption_score > 85 — corruption de la magistrature permettant l'impunité des réseaux criminels et des élites politiques, neutralisant tout mécanisme de redevabilité",
    },
    "deficit_institutions_anticorruption": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement institutionnel — financement organes contrôle indépendants (auditeurs, procureurs, ombudsman), formation agents publics éthique, registres patrimoniaux obligatoires élus et hauts fonctionnaires, budgets ouverts",
        "signal_fr": "Institutions anti-corruption formellement existantes mais insuffisamment indépendantes, sous-financées ou politiquement neutralisées par les réseaux qu'elles sont censées contrôler",
    },
    "gouvernance_integre_modele": {
        "severity_fr": "Faible",
        "action_fr": "Exporter les bonnes pratiques — financement Transparency International et GRECO, partage systèmes déclaration patrimoine et registres bénéficiaires, soutien renforcement institutions anti-corruption pays IPC bas",
        "signal_fr": "composite_score < 20 — gouvernance intègre avec institutions anti-corruption indépendantes, protection lanceurs d'alerte, transparence budgétaire et IPC supérieur à 75/100",
    },
}


@dataclass
class AntiCorruptionRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    bribery_systemic_score: float
    public_fund_embezzlement_score: float
    judicial_corruption_score: float
    anti_corruption_institution_weakness_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_anti_corruption_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.bribery_systemic_score * 0.30
            + self.public_fund_embezzlement_score * 0.25
            + self.judicial_corruption_score * 0.25
            + self.anti_corruption_institution_weakness_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_anti_corruption_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.bribery_systemic_score >= 85:
            return "etat_capturé_kleptocracie"
        if self.public_fund_embezzlement_score >= 85:
            return "detournement_massif_fonds_publics"
        if self.judicial_corruption_score >= 85:
            return "corruption_judiciaire_systemique"
        if self.composite_score >= 20:
            return "deficit_institutions_anticorruption"
        return "gouvernance_integre_modele"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Corruption critique de {n} — capture totale ou quasi-totale de l'État par des réseaux kleptocrates violant le droit à la bonne gouvernance, à l'égalité devant la loi et aux droits économiques et sociaux garantis par la CNUCC et le PIDESC",
                "Pillage systématique des ressources publiques — le détournement des fonds destinés à la santé, l'éducation et les infrastructures prive les populations de leurs droits économiques fondamentaux et perpétue la pauvreté",
                "Impunité institutionnalisée — l'absence de poursuites contre les réseaux corrompus au pouvoir crée un système de deux poids deux mesures qui dévaste la confiance dans les institutions démocratiques et l'État de droit",
            ]
        if self.risk_level == "élevé":
            return [
                f"Corruption institutionnalisée de {n} — pots-de-vin structurels dans les marchés publics, permis administratifs et services essentiels créant une économie parallèle illicite au détriment des populations vulnérables",
                "Défaillance institutionnelle partielle — les organes anti-corruption formellement existants sont insuffisamment indépendants ou sous-financés pour contrer efficacement les réseaux de corruption des élites",
                "Flux financiers illicites — les transferts offshore vers des paradis fiscaux privent les budgets publics de ressources essentielles estimées à plus de 1 000 milliards de dollars par an au niveau mondial",
            ]
        if self.risk_level == "modéré":
            return [
                f"Déficits de gouvernance de {n} — lacunes institutionnelles dans les mécanismes de contrôle et de transparence créant des espaces de corruption résiduelle sans capture totale de l'État",
                "Risques systémiques partiels — la corruption dans certains secteurs ou régions persiste malgré l'existence de cadres légaux anti-corruption insuffisamment appliqués",
                "Réformes en cours — des progrès en matière de transparence et de redevabilité sont observables mais restent fragiles face aux pressions des élites économiques et politiques bénéficiant de l'opacité",
            ]
        return [
            f"{n} incarne les standards exemplaires de gouvernance intègre — institutions anti-corruption indépendantes, transparence budgétaire systématique et protection robuste des lanceurs d'alerte",
            "IPC top mondial — scores supérieurs à 85/100 reflétant des systèmes de contrôle effectifs, des déclarations de patrimoine obligatoires et des poursuites systématiques contre la corruption à tous les niveaux",
            "Modèle exportable — financement Transparency International et GRECO, partage d'expertise sur les registres de bénéficiaires effectifs, la transparence budgétaire et la protection des lanceurs d'alerte",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "bribery_systemic_score": self.bribery_systemic_score,
            "public_fund_embezzlement_score": self.public_fund_embezzlement_score,
            "judicial_corruption_score": self.judicial_corruption_score,
            "anti_corruption_institution_weakness_score": self.anti_corruption_institution_weakness_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_anti_corruption_rights_index": self.estimated_anti_corruption_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[AntiCorruptionRightsEntity] = [
    AntiCorruptionRightsEntity(
        "ACR-001",
        "Somalia/IPC 11/100 Dernier Rang Monde État Défaillant Total",
        "Afrique de l'Est",
        "IPC 2023 11/100 Dernier Rang 180 Pays TI, Clans Armés Collectent Taxes Parallèles, Al-Shabaab Financement Illicite, Fonds Aide Détournés & Institutions Gouvernementales Inexistantes",
        92.0, 88.0, 90.0, 94.0,
    ),
    AntiCorruptionRightsEntity(
        "ACR-002",
        "Syria/Corruption Guerre Civile Fonds Humanitaires Détournés",
        "MENA",
        "Assad Réseau Captagon 2B$/An, Fonds Humanitaires ONU Détournés Réseaux Proches, Reconstruction Marchés Corrompus, IPC 13/100 & Mandat CPI Actifs",
        88.0, 86.0, 90.0, 88.0,
    ),
    AntiCorruptionRightsEntity(
        "ACR-003",
        "Venezuela/Corruption PDVSA 300B$ Détournés CPI 170/180",
        "Amérique du Sud",
        "PDVSA 300B$ Détournés 2000-2023 DOJ USA, Maduro Réseau Or/Crypto, IPC 2023 13/100 Rang 170/180, Sanctions 300+ Personnes & Économie Criminalisée",
        90.0, 92.0, 86.0, 88.0,
    ),
    AntiCorruptionRightsEntity(
        "ACR-004",
        "Libya/Corruption Milices Pétrole Pillé Institutions Inexistantes",
        "Afrique du Nord",
        "Milices Rivales Pillent NOC Pétrole 10B$/An, Deux Gouvernements Corrompus Est/Ouest, IPC 17/100, Trafics Migrants/Armes Corrompent Forces Armées & Aucun Contrôle Institutionnel",
        85.0, 88.0, 84.0, 86.0,
    ),
    AntiCorruptionRightsEntity(
        "ACR-005",
        "Mexico/Cartels Corrompent Fonctionnaires Impunité 97% Crimes",
        "Amérique Centrale",
        "97% Crimes Impunis IMCO 2023, Cartels Corrompent Police/Procureurs/Juges, IPC 31/100, Journalistes Anti-Corruption Assassinés & Candidats Politiques Tués Campagnes",
        55.0, 52.0, 58.0, 54.0,
    ),
    AntiCorruptionRightsEntity(
        "ACR-006",
        "Brazil/Lava Jato Petrobras Recul Anticorruption 2019-2023",
        "Amérique du Sud",
        "Lava Jato Révèle 2B$ Corruption Petrobras 2014-2016, Recul 2019-2023 Bolsonaro Affaiblit CGU/TCU, IPC 36/100 2023, Lula Réforme Partielle & Corruption Municipale Persistante",
        48.0, 52.0, 44.0, 50.0,
    ),
    AntiCorruptionRightsEntity(
        "ACR-007",
        "EU Anticorruption/OLAF Partiellement Efficace Lacunes États Est",
        "Europe",
        "OLAF Enquêtes Fraudes Fonds EU Limitées, Hongrie/Roumanie Lacunes Indépendance Judiciaire, IPC Moyenne EU 66/100, Mécanisme Coopération Justice & Fonds Conditionnalité",
        28.0, 30.0, 32.0, 26.0,
    ),
    AntiCorruptionRightsEntity(
        "ACR-008",
        "Denmark Finland New Zealand/IPC 1-3 Meilleure Pratique Mondiale",
        "Europe/Pacifique",
        "IPC 87-90/100 TI 2023, Déclarations Patrimoine Obligatoires Élus, Lanceurs Alerte Protégés, Registres Bénéficiaires Effectifs Publics & Tolérance Zéro Corruption Institutionnelle",
        8.0, 6.0, 9.0, 10.0,
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
        "domain": "anti_corruption_rights",
        "confidence_score": 0.86,
        "data_sources": [
            "transparency_international_cpi_2023",
            "unodc_corruption_crime_statistics_2023",
            "fatf_illicit_financial_flows_reports",
            "greco_council_europe_evaluation_rounds",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_anti_corruption_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_anti_corruption_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Anti-Corruption Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
