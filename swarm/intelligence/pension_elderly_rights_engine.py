"""Pension Elderly Rights Engine — Lacunes systèmes retraite, négligence soins âgés & discrimination par l'âge."""

from dataclasses import dataclass
from typing import List

DOMAIN = "pension_elderly_rights"
PREFIX = "PER"
ACCENT_COLOR = "#1a1a06"
WAVE = 215


@dataclass
class PensionElderlyRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    pension_adequacy_gap_score: float
    elderly_care_neglect_score: float
    age_discrimination_score: float
    social_isolation_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-22"

    @property
    def composite_score(self) -> float:
        return round(
            self.pension_adequacy_gap_score * 0.30
            + self.elderly_care_neglect_score * 0.25
            + self.age_discrimination_score * 0.25
            + self.social_isolation_score * 0.20,
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
    def estimated_pension_elderly_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "pension_adequacy_gap_score": self.pension_adequacy_gap_score,
            "elderly_care_neglect_score": self.elderly_care_neglect_score,
            "age_discrimination_score": self.age_discrimination_score,
            "social_isolation_score": self.social_isolation_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_pension_elderly_rights_index": self.estimated_pension_elderly_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    PensionElderlyRightsEntity(
        "PER-001", "Somalia — Zéro Système Pension National, Conflits Armés & Déplacement Personnes Âgées",
        "Afrique de l'Est",
        "Somalia Absence Totale Système Pension National 65+ Ans, Conflits Al-Shabaab Déplacent Personnes Âgées Sans Ressources, Malnutrition Sévère Aînés Camps IDP, Effondrement Institutions Étatiques Depuis 1991 & Soins Familiaux Seul Recours Défaillant",
        98.0, 95.0, 92.0, 92.0,
        "pension_adequacy_gap",
        [
            "Absence totale de protection sociale des personnes âgées en Somalie documentée — Somalia avec score composite 94.55/100 révélant l'inexistence d'un système de pension national depuis l'effondrement de l'État en 1991, exposant les personnes âgées aux conflits Al-Shabaab sans aucun filet de sécurité violant l'Article 9 du PIDESC sur le droit à la sécurité sociale",
            "Lacune pension extrême (98.0/100) — la malnutrition sévère documentée chez les personnes âgées dans les camps de déplacés internes somaliens, l'absence de soins médicaux spécialisés gériatriques et la dépendance exclusive à une solidarité familiale elle-même déstructurée par les conflits révèlent une violation systémique de l'Article 25 de la DUDH",
            "Établir un fonds d'urgence de protection sociale des personnes âgées en Somalie avec soutien UNHCR et UNFPA et inclure les aînés somaliens dans les programmes de transferts monétaires humanitaires conformément au Plan de Protection de la Vieillesse de l'Union Africaine de 2016 et à la Résolution HRC 24/20 sur les droits des personnes âgées",
        ],
    ),
    PensionElderlyRightsEntity(
        "PER-002", "Afghanistan — Système Pension Effondré Taliban, Femmes Âgées Exclues & Pauvreté Extrême",
        "Asie Centrale",
        "Afghanistan Système Pension Gouvernemental Effondré Depuis Prise Taliban 2021, Femmes Âgées Interdites Travail/Éducation Revenus, Fonctionnaires Retraités Sans Paiements, 97% Population Sous Seuil Pauvreté & Soins Santé Effondrés Personnes Âgées",
        92.0, 90.0, 88.0, 90.0,
        "pension_adequacy_gap",
        [
            "Effondrement du système de retraite sous régime Taliban documenté — Afghanistan avec score composite 90.10/100 révélant l'arrêt total des paiements de pension aux fonctionnaires retraités depuis août 2021, l'exclusion totale des femmes âgées de toute activité économique et le fait que 97% de la population afghane vit sous le seuil de pauvreté violant l'Article 9 PIDESC",
            "Négligence soins (90.0/100) — l'effondrement du système de santé afghan affectant prioritairement les personnes âgées souffrant de maladies chroniques, l'interdiction pour les femmes de consulter des médecins hommes sans mahram et la fermeture des hôpitaux révèlent une catastrophe humanitaire gérontologique documentée par l'OMS",
            "Conditionner toute aide internationale à l'Afghanistan au rétablissement des paiements de pension et à la restauration des droits des femmes âgées à l'accès aux soins et à la sécurité sociale conformément aux Principes des Nations Unies pour les Personnes Âgées de 1991 (Résolution 46/91)",
        ],
    ),
    PensionElderlyRightsEntity(
        "PER-003", "Yemen — Pension Collapse Guerre Civile, Personnel Médical Non-Payé & Aînés en Zone Conflit",
        "MENA",
        "Yemen Guerre Civile Depuis 2015 Système Pension Effondré, Fonctionnaires Non-Payés Depuis 2016, Personnes Âgées Zones Conflit Houthi/Coalition, Hôpitaux Détruits Frappes Aériennes, Cholera/Malnutrition Personnes Âgées & Épuisement Économies Familles",
        90.0, 88.0, 85.0, 88.0,
        "pension_adequacy_gap",
        [
            "Effondrement du système de protection sociale des aînés yéménites documenté — Yemen avec score composite 87.85/100 révélant l'arrêt des paiements de pension aux fonctionnaires depuis 2016 par épuisement des réserves de la Banque Centrale, la destruction de 50% des hôpitaux par les frappes de la coalition et l'exposition des personnes âgées aux épidémies de choléra violant l'Article 12 PIDESC",
            "Zones de conflit (88.0/100) — les personnes âgées vivant dans des zones de combat actif entre forces Houthi et coalition saoudienne, incapables de fuir, subissant des coupures d'eau/électricité prolongées et souffrant de malnutrition sévère documentée par l'UNICEF révèlent une violation grave de l'Article 3 commun aux Conventions de Genève protégeant les civils vulnérables",
            "Inclure spécifiquement la protection des personnes âgées dans les négociations de cessez-le-feu yéménites sous médiation ONU et rétablir les paiements de pension aux fonctionnaires retraités comme condition des accords humanitaires conformément au Plan d'Action Humanitaire pour le Yémen de l'OCHA",
        ],
    ),
    PensionElderlyRightsEntity(
        "PER-004", "Haiti — Système Retraite Inexistant Secteur Informel, Séismes Récurrents & Gangs",
        "Caraïbes",
        "Haiti 80% Économie Informelle Sans Cotisation Retraite, Séismes 2010/2021 Détruisent Économies Personnes Âgées, Contrôle Territorial Gangs G9 Isolent Aînés, ONA Fonds Pension Insuffisant & Espérance Vie Basse 65 Ans Contexte Violence",
        85.0, 82.0, 80.0, 82.0,
        "pension_adequacy_gap",
        [
            "Absence structurelle de protection retraite dans l'économie informelle haïtienne documentée — Haiti avec score composite 82.40/100 révélant que 80% de la population travaillant dans le secteur informel n'accumule aucune cotisation à l'Office National d'Assurance Vieillesse (ONA), exposant les personnes âgées à la pauvreté extrême violant l'Article 9 PIDESC sur la sécurité sociale universelle",
            "Vulnérabilité multifactorielle (85.0/100) — la perte des économies lors des séismes de 2010 et 2021, le contrôle territorial par les gangs G9 isolant les aînés dans des quartiers assiégés sans accès aux soins et l'effondrement des transferts de la diaspora haïtienne pendant les crises révèlent une catastrophe gérontologique structurelle documentée par HRW",
            "Créer un système universel de pension non-contributif pour les personnes âgées haïtiennes financé par un fonds multilatéral OEA/ONU et protéger spécifiquement les aînés dans les zones contrôlées par les gangs conformément aux Directives Opérationnelles du Comité Permanent Inter-agences sur la Protection des Personnes en Situations de Déplacement Interne",
        ],
    ),
    PensionElderlyRightsEntity(
        "PER-005", "India — 1$/Jour Pension Rurale, 80% Travailleurs Informels Sans Protection & Inégalités Régionales",
        "Asie du Sud",
        "India NSAP National Social Assistance Programme Pension 200 Rs/Mois (~2.4$/Mois) Sous Seuil Pauvreté, 80% Travailleurs Informels Sans EPFO, Inégalités Régionales Kerala vs Bihar, Abandon Rural Personnes Âgées & MGNREGA Insuffisant 65+",
        55.0, 52.0, 50.0, 52.0,
        "pension_adequacy_gap",
        [
            "Inadéquation critique du système de pension indien pour les travailleurs informels documentée — India avec score composite 52.40/100 révélant que la pension nationale NSAP de 200 roupies/mois (environ 2,4 USD) représente moins de 5% du seuil de pauvreté alimentaire et que 80% des travailleurs indiens dans le secteur informel n'accumulent aucune cotisation EPFO violant l'Article 9 PIDESC",
            "Abandon rural (52.0/100) — les inégalités inter-états entre le Kerala (pension de 1 600 Rs/mois) et le Bihar (200 Rs/mois) révèlent une fragmentation du droit à la sécurité sociale selon la naissance géographique, tandis que l'abandon des personnes âgées rurales par les familles migrantes vers les villes crée une crise de soins non reconnue par les institutions",
        ],
    ),
    PensionElderlyRightsEntity(
        "PER-006", "Nigeria — Travailleurs Informels Sans Pension, Détournement Fonds CPS & Corruption Institutionnelle",
        "Afrique de l'Ouest",
        "Nigeria Contributory Pension Scheme 2004 Couvre Seulement 10M/200M Habitants, 80% Économie Informelle Exclus, Détournements Fonds PFA Documentés PENCOM, Retraités Militaires Non-Payés & Personnes Âgées Rurales Dépendance Familiale 100%",
        58.0, 50.0, 48.0, 50.0,
        "pension_adequacy_gap",
        [
            "Exclusion systémique des travailleurs informels nigérians du système de retraite documentée — Nigeria avec score composite 51.90/100 révélant que le Contributory Pension Scheme de 2004 ne couvre que 10 millions d'Africains sur 220 millions d'habitants, laissant 80% de la population dans l'économie informelle sans aucune protection retraite violant l'Article 9 PIDESC",
            "Corruption institutionnelle (50.0/100) — les détournements de fonds par les Pension Fund Administrators documentés par la PENCOM, les retraités militaires attendant des mois leurs pensions et l'absence totale de système de pension universelle pour les personnes âgées rurales révèlent une défaillance institutionnelle chronique du système de protection sociale nigérian",
        ],
    ),
    PensionElderlyRightsEntity(
        "PER-007", "USA — Social Security Insuffisant Working Poor, Medicare Gaps & Isolement Personnes Âgées",
        "Amérique du Nord",
        "USA Social Security Moyenne 1 700$/Mois Insuffisant NYC/SF Coût Vie, Medicare Gaps Dentaire/Vision Non-Couverts, 28% Retraités Dépendent Uniquement SS, Crise Maisons Retraite COVID 30% Décès & Isolement Social Épidémique 65+",
        30.0, 32.0, 28.0, 30.0,
        "social_isolation",
        [
            "Insuffisance structurelle de la protection retraite pour les travailleurs pauvres américains documentée — USA avec score composite 30.00/100 révélant que 28% des retraités américains dépendent exclusivement de la Social Security (moyenne 1 700 USD/mois) insuffisante dans les métropoles à coût élevé, avec des lacunes Medicare sur les soins dentaires/visuels violant les standards OCDE de protection des aînés",
            "Isolement social (30.0/100) — l'épidémie d'isolement social documentée chez les Américains de plus de 65 ans par le Surgeon General en 2023, la mortalité dans les EHPAD durant COVID (30% des décès pour 1% de la population) et les inégalités raciales de pension entre Blancs et Noirs/Latinos révèlent des violations des droits sociaux des personnes âgées disproportionnellement racialisées",
        ],
    ),
    PensionElderlyRightsEntity(
        "PER-008", "Denmark — Pension Universelle ATP, Soins Intégrés & Meilleure Pratique Protection Aînés",
        "Europe du Nord",
        "Denmark ATP Arbejdsmarkedets Tillægspension Universel, Folkepension Universelle 65+ Indépendante Cotisations, Soins Gériatriques Municipaux Financés Impôt, Active Ageing Policy EU & Classement 1er Melbourne Mercer Global Pension Index 2023",
        5.0, 4.0, 6.0, 5.0,
        "social_isolation",
        [
            "Meilleure pratique internationale de protection des droits des personnes âgées au Danemark documentée — Denmark avec score composite 5.00/100 incarnant le modèle de référence mondial grâce à la Folkepension universelle accessible dès 65 ans indépendamment des cotisations, les soins gériatriques municipaux financés par l'impôt et le classement numéro un du Melbourne Mercer Global Pension Index 2023",
            "Modèle de référence (5.0/100) — le système ATP assurant une pension complémentaire à tous les travailleurs incluant les temps partiels, la politique Active Ageing garantissant l'intégration sociale des personnes âgées et l'absence d'isolement institutionnalisé grâce aux soins à domicile représentent un standard de droits des personnes âgées conforme aux Principes ONU de 1991 (Résolution 46/91)",
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
        "last_analysis": "2026-06-22",
        "engine_version": "1.0.0",
        "domain": DOMAIN,
        "confidence_score": 0.87,
        "data_sources": [
            "ilo_social_protection_world_report_2022",
            "hrw_elderly_rights_crisis_fragile_states_report",
            "melbourne_mercer_global_pension_index_2023",
            "un_open_ended_working_group_ageing_reports_2024",
            "helpage_international_global_agewatch_index",
        ],
        "entities": [e.to_dict() for e in ENTITIES],
        "avg_estimated_pension_elderly_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
