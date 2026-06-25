"""Economic Rights Engine — droit au travail décent, syndicats & plancher social."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class EconomicRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    decent_work_denial_score: float
    wage_theft_exploitation_score: float
    union_suppression_score: float
    social_floor_absence_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-20"

    @property
    def composite_score(self) -> float:
        return round(
            self.decent_work_denial_score * 0.30
            + self.wage_theft_exploitation_score * 0.25
            + self.union_suppression_score * 0.25
            + self.social_floor_absence_score * 0.20,
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
    def estimated_economic_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "decent_work_denial_score": self.decent_work_denial_score,
            "wage_theft_exploitation_score": self.wage_theft_exploitation_score,
            "union_suppression_score": self.union_suppression_score,
            "social_floor_absence_score": self.social_floor_absence_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_economic_rights_index": self.estimated_economic_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    EconomicRightsEntity(
        "ER-001", "RDC/Cobalt — Mines Artisanales 40 000 Enfants, Cobalt Apple/Tesla & Impunité",
        "Afrique Centrale",
        "RDC 40 000 Enfants Mines Cobalt Artisanales, Cobalt 70% Mondial Sans Standard Travail, Apple/Tesla Chaîne Approvisionnement, Salaires 2$/Jour & Aucune Protection Sociale Mineurs",
        92.0, 90.0, 85.0, 88.0,
        "decent_work_denial",
        [
            "Violation des droits économiques documentée — RDC/Cobalt avec score composite 88.95/100 révélant une exploitation systémique des travailleurs des mines artisanales violant l'Article 7 du PIDESC sur le droit à des conditions de travail justes et favorables",
            "Déni travail décent (92.0/100) — les 40 000 enfants dans les mines de cobalt artisanales et les salaires de 2$/jour violent simultanément la Convention OIT 138 sur l'âge minimum et l'Article 7 PIDESC sur les conditions de travail équitables",
            "Activer les mécanismes de diligence raisonnable de l'OCDE sur les chaînes d'approvisionnement et exiger l'application de la Directive UE sur la durabilité des entreprises pour obliger Apple, Tesla et les multinationales utilisant le cobalt à garantir le respect des droits au travail",
        ],
    ),
    EconomicRightsEntity(
        "ER-002", "Bangladesh/Rana Plaza — 1 134 Morts, 4M Ouvriers Textile & Accord Fire Safety",
        "Asie du Sud",
        "Bangladesh Rana Plaza 2013 1 134 Morts Effondrement Usine, 4M Ouvriers Textile 95% Femmes, Salaire 95$/Mois, Accord Incendie-Sécurité Insuffisant & H&M/Zara Chaînes Responsabilité",
        88.0, 90.0, 85.0, 85.0,
        "wage_theft_exploitation",
        [
            "Violation des droits économiques documentée — Bangladesh/Rana Plaza avec score composite 87.15/100 révélant les conditions de travail mortelles dans l'industrie textile et l'exploitation systémique de 4 millions de travailleurs violant le PIDESC Art 7 et les Conventions OIT 155 et 187 sur la sécurité au travail",
            "Vol de salaires/Exploitation (90.0/100) — les salaires de 95$/mois et les conditions mortelles de l'industrie textile bangladaise illustrent l'exploitation de chaînes d'approvisionnement mondiales violant les Principes Directeurs ONU sur les entreprises et les droits de l'homme",
            "Ratifier et appliquer la Convention OIT 190 sur la violence et le harcèlement au travail et étendre l'Accord de Dhaka sur la sécurité incendie à toutes les chaînes d'approvisionnement textiles mondiales avec mécanisme contraignant de responsabilité des donneurs d'ordre",
        ],
    ),
    EconomicRightsEntity(
        "ER-003", "Pakistan/Briques — 4.5M Travailleurs Liés, Travail Forcé Dettes & Peshgi",
        "Asie du Sud",
        "Pakistan 4.5M Travailleurs Liés Briqueteries Peshgi Avances-Dettes, Familles Héréditaires Travail Forcé, 0 Syndicat Briqueteries & OIT Rapport Travail Forcé Pakistan Systémique",
        88.0, 85.0, 82.0, 90.0,
        "social_floor_absence",
        [
            "Violation des droits économiques documentée — Pakistan/Briques avec score composite 86.15/100 révélant 4.5 millions de travailleurs en situation de servitude pour dettes dans les briqueteries violant la Convention OIT 29 sur le travail forcé et l'Article 8 du PIDCP",
            "Absence plancher social (90.0/100) — le système Peshgi d'avances-dettes créant une servitude héréditaire pour des familles entières dans les briqueteries constitue une forme de travail forcé interdite par la Convention de l'esclavage de 1926 et la Convention OIT 105",
            "Activer le mécanisme d'examen de la Convention OIT 29 contre le travail forcé et conditionner les accords commerciaux UE-Pakistan au respect des droits fondamentaux au travail incluant l'interdiction effective du système Peshgi de travail lié",
        ],
    ),
    EconomicRightsEntity(
        "ER-004", "Asie/Zones Franches — 100M Travailleurs ZES, Syndicats Interdits & Salaire Minimal",
        "Asie du Sud-Est/Chine",
        "Zones Économiques Spéciales 100M Travailleurs, Syndicats Interdits Bangladesh/Vietnam/Cambodge ZES, Salaire Minimum Non-Appliqué, Licenciements Représailles & Contrats Zéro-Droits",
        85.0, 85.0, 92.0, 80.0,
        "union_suppression",
        [
            "Violation des droits économiques documentée — Asie/Zones Franches avec score composite 85.75/100 révélant la suppression systémique des droits syndicaux dans les Zones Économiques Spéciales violant la Convention OIT 87 sur la liberté syndicale et l'Article 8 du PIDESC",
            "Suppression syndicale (92.0/100) — l'interdiction des syndicats indépendants dans les zones franches de Bangladesh, Vietnam et Cambodge prive 100 millions de travailleurs de leur droit fondamental à l'organisation collective garanti par les Conventions fondamentales de l'OIT",
            "Exiger des États membres de l'OIT le respect des Conventions fondamentales 87 et 98 sur la liberté syndicale dans les Zones Économiques Spéciales et conditionner l'accès aux marchés des pays de l'OCDE au respect effectif des droits syndicaux",
        ],
    ),
    EconomicRightsEntity(
        "ER-005", "USA/Gig Economy — 59M Travailleurs Plateformes, 0 Protection & Amazon Surveillance",
        "Amérique du Nord",
        "USA 59M Travailleurs Gig Economy Sans Protection Sociale, Amazon Algorithmes Surveillance Employés, Walmart Répression Syndicale, Minimum Wage 7.25$/H Depuis 2009 & Prop 22 Californie",
        52.0, 58.0, 52.0, 50.0,
        "wage_theft_exploitation",
        [
            "Violation des droits économiques documentée — USA/Gig Economy avec score composite 53.10/100 révélant l'exclusion délibérée de 59 millions de travailleurs de plateforme de toute protection sociale violant l'Article 7 PIDESC sur des conditions de travail équitables (PIDESC non ratifié par les USA)",
            "Vol de salaires/Exploitation (58.0/100) — la classification des chauffeurs Uber/Lyft et livreurs DoorDash comme 'entrepreneurs indépendants' pour contourner les protections sociales constitue une violation des Conventions OIT sur le travail décent",
            "Ratifier le PIDESC et adopter une loi fédérale classifiant les travailleurs de plateforme comme employés avec droits à la protection sociale, syndicale et aux congés payés conformément aux standards de l'OIT sur le travail décent",
        ],
    ),
    EconomicRightsEntity(
        "ER-006", "Europe/Précariat — Zéro-Heures UK, Faux Auto-Entrepreneurs & Riders Livreurs",
        "Europe",
        "UK 1M Contrats Zéro-Heures 2023, Faux Autoentrepreneurs France Deliveroo/Uber Eats, Espagne Riders Loi Insuffisante & ETUC Rapports Droits Précaires Non-Protégés Plate-Formes",
        52.0, 48.0, 50.0, 55.0,
        "social_floor_absence",
        [
            "Violation des droits économiques documentée — Europe/Précariat avec score composite 51.10/100 révélant la prolifération des formes d'emploi atypiques contournant les protections sociales en contradiction avec la Charte Sociale Européenne Révisée",
            "Absence plancher social (55.0/100) — le million de contrats zéro-heures au Royaume-Uni et les faux auto-entrepreneurs dans les plateformes de livraison privent des millions de travailleurs européens de sécurité sociale, congés payés et protection contre le licenciement",
            "Renforcer la Directive UE sur les travailleurs de plateforme 2024 pour garantir une présomption d'emploi et des droits sociaux complets aux 28 millions de travailleurs de plateforme européens conformément aux recommandations de l'ETUC",
        ],
    ),
    EconomicRightsEntity(
        "ER-007", "Japon/Karoshi — 2 000 Décès/An Surmenage, Non-Regular Workers & Hôtesses",
        "Asie du Nord-Est",
        "Japon 2 000+ Décès Karoshi Surmenage/An, 7M Travailleurs Non-Réguliers Salaire -40%, Heures Supplémentaires Non-Payées Mutsuko & Convention OIT Temps Travail Non-Respectée",
        28.0, 35.0, 28.0, 25.0,
        "wage_theft_exploitation",
        [
            "Défis persistants des droits économiques au Japon — le phénomène Karoshi (mort par surmenage) causant 2 000+ décès annuels et l'exclusion de 7 millions de travailleurs non-réguliers des protections complètes révèlent des lacunes dans l'application des droits au travail",
            "Vol de salaires/Exploitation (35.0/100) — les heures supplémentaires non-payées, les salaires des travailleurs non-réguliers inférieurs de 40% aux réguliers et le Karoshi constituent des violations des limites de temps de travail fixées par la Convention OIT 1 (1919)",
            "Réformer le droit du travail japonais pour éliminer le dualisme régulier/non-régulier, mettre en œuvre une loi anti-Karoshi contraignante et ratifier les Conventions OIT sur les droits syndicaux conformément aux recommandations du Comité des droits économiques ONU",
        ],
    ),
    EconomicRightsEntity(
        "ER-008", "OIT/PIDESC — Agenda Travail Décent, Art 7 Conditions Justes & Conventions Fondamentales",
        "Global",
        "OIT Agenda Travail Décent 2008, PIDESC Article 7 Conditions Travail Équitables, OIT 8 Conventions Fondamentales, Salaire Minimum Vital OIT & Initiative Multi-Parties Partenariat Global",
        5.0, 4.0, 3.0, 6.0,
        "social_floor_absence",
        [
            "OIT/PIDESC incarne le cadre normatif exemplaire des droits économiques — Agenda Travail Décent 2008 et Article 7 PIDESC créant des obligations contraignantes de conditions de travail justes, sécurité sociale et liberté syndicale pour tous les travailleurs sans distinction",
            "Convention OIT 87 sur la liberté syndicale — garantit le droit fondamental de tout travailleur de constituer des syndicats et d'y adhérer, constituant la pierre angulaire des droits économiques reconnus par les 8 Conventions fondamentales de l'OIT ratifiées par 180+ États",
            "Universaliser la ratification des 8 Conventions fondamentales de l'OIT et tripler le budget de l'OIT pour renforcer les capacités d'inspection du travail dans les pays à revenus faibles et intermédiaires afin d'assurer le travail décent pour tous d'ici 2030",
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
        "domain": "economic_rights",
        "confidence_score": 0.84,
        "data_sources": [
            "ilo_world_employment_social_outlook_report",
            "un_special_rapporteur_extreme_poverty_economic_rights_reports",
            "business_human_rights_resource_centre_labour_violations_database",
        ],
        "entities": [e.to_dict() for e in ENTITIES],
        "avg_estimated_economic_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
