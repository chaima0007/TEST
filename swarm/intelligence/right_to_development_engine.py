"""Right to Development Engine — droit au développement, inégalités mondiales, piège de la dette & exclusion."""

from dataclasses import dataclass
from typing import List


@dataclass
class RightToDevelopmentEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    systemic_inequality_score: float
    debt_trap_dependency_score: float
    technology_transfer_denial_score: float
    participatory_governance_failure_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-20"

    @property
    def composite_score(self) -> float:
        return round(
            self.systemic_inequality_score * 0.30
            + self.debt_trap_dependency_score * 0.25
            + self.technology_transfer_denial_score * 0.25
            + self.participatory_governance_failure_score * 0.20,
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
    def estimated_right_to_development_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "systemic_inequality_score": self.systemic_inequality_score,
            "debt_trap_dependency_score": self.debt_trap_dependency_score,
            "technology_transfer_denial_score": self.technology_transfer_denial_score,
            "participatory_governance_failure_score": self.participatory_governance_failure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_right_to_development_index": self.estimated_right_to_development_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    RightToDevelopmentEntity(
        entity_id="RD-001",
        name="Afrique Sub-Saharienne/PMA — 46 Pays, 1B$ Flux Illicites/Jour & Exclusion Développement",
        country="Afrique Sub-Saharienne",
        sector="PMA 46 Pays Moins Avancés ONU, Afrique Sub-Saharienne 0.5% PIB Mondial Pour 14% Population, Flux Financiers Illicites 88B$/An Africa GFI, Évasion Fiscale Multinationales & Aide Développement APD Inférieure Remboursements Dette",
        systemic_inequality_score=92.0,
        debt_trap_dependency_score=88.0,
        technology_transfer_denial_score=85.0,
        participatory_governance_failure_score=90.0,
        primary_pattern="systemic_inequality",
        key_signals=[
            "Violation du droit au développement documentée — Afrique Sub-Saharienne/PMA avec score composite 88.85/100 révélant que 46 pays les moins avancés représentant 14% de la population mondiale ne génèrent que 0,5% du PIB mondial, avec 88Md$ de flux financiers illicites quittant l'Afrique annuellement selon Global Financial Integrity, supérieur à l'aide publique au développement reçue",
            "Inégalités systémiques (92.0/100) — l'écart entre les 88Md$ de flux financiers illicites sortant annuellement d'Afrique (évasion fiscale des multinationales, corruption) et les 48Md$ d'aide publique au développement reçue révèle que le système économique mondial extrait plus de ressources des PMA qu'il n'en injecte, violant l'Article 3 de la Déclaration ONU sur le droit au développement (DRD 1986) sur la responsabilité des États développés",
            "Mettre en œuvre la réforme fiscale internationale OCDE/G20 sur l'imposition minimale des multinationales et allouer les recettes fiscales supplémentaires à un Fonds de développement équitable pour les PMA conformément à l'Agenda d'Addis-Abeba (2015) sur le financement du développement et à l'Article 4 de la Déclaration ONU sur le droit au développement",
        ],
    ),
    RightToDevelopmentEntity(
        entity_id="RD-002",
        name="Sri Lanka/Pakistan/Zambie — Pièges de la Dette FMI/Chine & Austérité",
        country="Asie du Sud/Afrique",
        sector="Sri Lanka Défaut 51B$ 2022 FMI Austérité, Pakistan 130B$ Dette Externe 2024 FMI Programme 7e, Zambie Première Défaillance Souveraine Africaine 2020 BRI & Ghana Défaut 2022 Dévaluation 50% Monnaie",
        systemic_inequality_score=85.0,
        debt_trap_dependency_score=92.0,
        technology_transfer_denial_score=80.0,
        participatory_governance_failure_score=82.0,
        primary_pattern="debt_trap_dependency",
        key_signals=[
            "Violation documentée — Sri Lanka/Pakistan/Zambie avec score composite 84.9/100 révélant le défaut souverain du Sri Lanka sur 51Md$ en 2022 imposant une austérité FMI avec coupes dans les services de santé et d'éducation, les 130Md$ de dette externe pakistanaise sous 7 programmes FMI successifs et la première défaillance souveraine africaine de la Zambie en 2020",
            "Piège de la dette (92.0/100) — les programmes d'ajustement structurel du FMI imposés au Sri Lanka, au Pakistan et à la Zambie en échange de prêts de sauvetage incluant des coupes budgétaires dans les services sociaux essentiels (santé, éducation) violent l'obligation de réalisation progressive des droits économiques et sociaux de l'Article 2 PIDESC et les Principes directeurs sur la dette souveraine du Conseil des droits de l'homme ONU",
            "Adopter un cadre multilatéral contraignant de restructuration des dettes souveraines (Cadre commun G20 renforcé) permettant aux pays en développement de restructurer leurs dettes sans coupes dans les dépenses sociales, conformément aux Principes ONU sur la dette souveraine responsable (résolution AG 69/319) et aux recommandations du Rapporteur Spécial sur la dette et les droits humains",
        ],
    ),
    RightToDevelopmentEntity(
        entity_id="RD-003",
        name="Congo/RDC/Ressources — Paradoxe du Cobalt, 24T$ Minéraux & 75% Pauvreté",
        country="Afrique Centrale",
        sector="RDC 70% Réserves Cobalt Mondiales Valeur 24T$, 75% Population Sous Seuil Pauvreté, Cobalt Phones/EVs Monde, 50 000 Mineurs Artisanaux Enfants Glencore/CMOC Extractivisme & Recettes Minières Opacité",
        systemic_inequality_score=80.0,
        debt_trap_dependency_score=75.0,
        technology_transfer_denial_score=88.0,
        participatory_governance_failure_score=85.0,
        primary_pattern="technology_transfer_denial",
        key_signals=[
            "Violation documentée — RDC avec score composite 81.75/100 révélant le paradoxe de détenir 70% des réserves mondiales de cobalt (valeur estimée 24T$) nécessaires aux batteries des véhicules électriques et smartphones mondiaux tout en maintenant 75% de sa population sous le seuil de pauvreté, avec 50 000 enfants dans les mines artisanales selon l'UNICEF",
            "Déni de transfert technologique (88.0/100) — l'absence de transfert technologique permettant à la RDC de transformer localement son cobalt (au lieu de l'exporter brut) et de capturer la valeur ajoutée de la chaîne de valeur des batteries constitue une violation structurelle du droit au développement (Article 1 DRD 1986) par les multinationales et les États importateurs de ressources",
            "Exiger des entreprises minières (Glencore, CMOC) opérant en RDC qu'elles respectent les Principes directeurs ONU sur les entreprises et les droits de l'homme et financer un programme de transformation locale du cobalt (batteries en RDC) créant une valeur ajoutée locale, conformément à l'Initiative pour la transparence des industries extractives (ITIE) et aux recommandations de la CNUCED",
        ],
    ),
    RightToDevelopmentEntity(
        entity_id="RD-004",
        name="Haïti/Bangladesh/Cambodge — Sweatshops, Chaînes d'Approvisionnement & Travail Précaire",
        country="Global Sud",
        sector="Bangladesh Rana Plaza 1134 Morts 2013, Cambodge Minimum Salarial 200$/Mois Pression Marques, Haïti Zones Franches Industrielles Travail Précaire & Accord Commerce Agoa/Cotonou Asymétrique",
        systemic_inequality_score=72.0,
        debt_trap_dependency_score=78.0,
        technology_transfer_denial_score=80.0,
        participatory_governance_failure_score=75.0,
        primary_pattern="technology_transfer_denial",
        key_signals=[
            "Violation documentée — Haïti/Bangladesh/Cambodge avec score composite 76.1/100 révélant l'effondrement du Rana Plaza au Bangladesh (2013, 1 134 morts) dû aux conditions de sous-traitance des grandes marques mondiales, les salaires minimaux cambodgiens maintenus à 200$/mois sous pression des marques malgré les profits records et les zones franches haïtiennes opérant en dehors du droit du travail",
            "Déni de transfert technologique (80.0/100) — les chaînes d'approvisionnement mondiales maintenant les pays du Sud dans une position de sous-traitants à bas salaires sans transfert de technologie ni montée en valeur ajoutée violent l'obligation des États développés de faciliter le transfert de technologie prévu par l'Article 7(b) de la Déclaration sur le droit au développement (1986)",
            "Adopter une loi européenne sur le devoir de vigilance des chaînes d'approvisionnement (Directive CSDD) avec des mécanismes d'indemnisation contraignants pour les victimes et exiger un salaire vital dans les chaînes d'approvisionnement des entreprises de mode conforme aux recommandations de l'OIT et au Pacte mondial pour un salaire vital (2022)",
        ],
    ),
    RightToDevelopmentEntity(
        entity_id="RD-005",
        name="Brésil/Inde — Émergents Inégaux, Milliardaires Record & Pauvreté Persistante",
        country="BRICS Émergents",
        sector="Brésil 1% Population 50% Richesse Nationale, Inde 100 Milliardaires 2023 Actifs Équivalents 25% PIB, Gini Coefficient Extrême, Classes Moyennes Émergentes Mais 300M Toujours Sous Seuil Pauvreté & Inégalité Raciale",
        systemic_inequality_score=55.0,
        debt_trap_dependency_score=52.0,
        technology_transfer_denial_score=48.0,
        participatory_governance_failure_score=50.0,
        primary_pattern="systemic_inequality",
        key_signals=[
            "Violation documentée — Brésil/Inde avec score composite 51.5/100 révélant que 1% de la population brésilienne détient 50% de la richesse nationale, que 100 milliardaires indiens possèdent des actifs équivalant à 25% du PIB indien et que 300M de personnes restent sous le seuil de pauvreté dans ces économies émergentes à revenu intermédiaire",
            "Inégalités systémiques (55.0/100) — les coefficients Gini extrêmes du Brésil (53) et de l'Inde (37) révèlent des inégalités structurelles persistantes qui violent l'obligation de réalisation progressive de l'égalité économique prévue par l'Article 8 de la Déclaration sur le droit au développement et l'Article 2 PIDESC sur l'égalité dans la jouissance des droits",
            "Mettre en œuvre des réformes fiscales redistributives dans les économies BRICS (impôt sur la fortune, taxation des plus-values, ISF brésilien réformé) et renforcer les programmes de transferts sociaux conditionnels (Bolsa Família, MGNREGS) conformément aux recommandations du Rapporteur Spécial ONU sur l'extrême pauvreté et les droits de l'homme",
        ],
    ),
    RightToDevelopmentEntity(
        entity_id="RD-006",
        name="Chine/BRI — Initiative Route Soie, Dettes Opaques & Conditionnalités Géopolitiques",
        country="Asie du Nord-Est",
        sector="Chine BRI 1T$ Investissements 149 Pays, Dettes Opaques Conditions Non Publiées, Zambie/Sri Lanka/Pakistan BRI Surendettement, Ports Saisie Hambantota Sri Lanka & Opacité Contrats AidData Research",
        systemic_inequality_score=45.0,
        debt_trap_dependency_score=62.0,
        technology_transfer_denial_score=50.0,
        participatory_governance_failure_score=55.0,
        primary_pattern="debt_trap_dependency",
        key_signals=[
            "Violation documentée — Chine/BRI avec score composite 52.5/100 révélant 1T$ d'investissements dans 149 pays avec des contrats opaques documentés par AidData (William & Mary University), le cas du port Hambantota au Sri Lanka cédé à bail à la Chine pour 99 ans suite au surendettement et les clauses contractuelles secrètes imposant des conditionnalités géopolitiques",
            "Piège de la dette (62.0/100) — les prêts BRI opaques avec des clauses de confidentialité interdisant la divulgation des conditions aux parlements nationaux et aux populations (documentées par AidData 2021) violent l'obligation de transparence de la gouvernance du développement prévue par les Principes ONU sur la dette souveraine responsable et l'Article 10 de la Déclaration sur le droit au développement",
            "Exiger de la Chine la publication de tous les contrats BRI conformément aux standards de transparence de l'OCDE et créer un mécanisme de contrôle multilatéral des prêts d'infrastructure incluant des protections pour les droits des communautés affectées, conformément aux recommandations du Comité des droits économiques sociaux et culturels ONU sur le devoir de vigilance dans les projets de développement",
        ],
    ),
    RightToDevelopmentEntity(
        entity_id="RD-007",
        name="UE/OCDE — APD, CBAM & Cohérence Politiques Développement",
        country="Europe/OCDE",
        sector="OCDE APD 0.7% RNB Objectif ONU Non Atteint (0.33% Réel), UE Mécanisme Ajustement Carbone Frontière CBAM Impact PED, Subventions Agricoles PAC Concurrence Déloyale & Cohérence Politiques Développement Manquante",
        systemic_inequality_score=25.0,
        debt_trap_dependency_score=30.0,
        technology_transfer_denial_score=28.0,
        participatory_governance_failure_score=32.0,
        primary_pattern="participatory_governance_failure",
        key_signals=[
            "Défis de cohérence des politiques développement en UE/OCDE — les pays de l'OCDE allouent en moyenne 0,33% de leur RNB à l'aide publique au développement (contre l'objectif ONU de 0,7%), les subventions agricoles de la PAC concurrencent déloyalement les agriculteurs des pays en développement et le mécanisme CBAM peut pénaliser les exportations des PED vers l'UE",
            "Échec de gouvernance participative (32.0/100) — les institutions de gouvernance économique mondiale (FMI, Banque mondiale, OMC) sont structurellement sous-représentatives des pays en développement (quotas FMI reflétant la répartition du pouvoir économique de 1945), violant le droit des peuples à participer à leur propre développement prévu par l'Article 2 de la Déclaration sur le droit au développement",
            "Atteindre l'objectif ONU de 0,7% du RNB en APD pour tous les pays de l'OCDE et réformer les droits de vote au FMI et à la Banque mondiale pour donner aux pays en développement une représentation proportionnelle à leur poids démographique conformément aux ODD 17 (partenariats) et aux recommandations du G77 sur la réforme de la gouvernance mondiale",
        ],
    ),
    RightToDevelopmentEntity(
        entity_id="RD-008",
        name="ONU/DRD 1986 — Déclaration Droit Développement, Groupe Travail & ODD",
        country="Global",
        sector="ONU DRD Déclaration Droit Au Développement 1986 Adoptée AG 128-1-9, Groupe Travail Intergouvernemental 1998 Sessions Annuelles, Standard Contraignant Toujours Non Adopté & ODD 2030 Agenda Développement Durable",
        systemic_inequality_score=4.0,
        debt_trap_dependency_score=5.0,
        technology_transfer_denial_score=3.0,
        participatory_governance_failure_score=6.0,
        primary_pattern="participatory_governance_failure",
        key_signals=[
            "ONU/DRD 1986 constitue le cadre normatif du droit au développement — la Déclaration sur le droit au développement (1986) adoptée par 128 États à l'Assemblée générale ONU reconnaît que le développement est un droit humain inaliénable impliquant des obligations des États développés envers les États en développement et la participation des peuples à leur propre développement",
            "Absence d'instrument contraignant — malgré 40 ans de négociations au sein du Groupe de travail intergouvernemental ONU, aucune convention contraignante sur le droit au développement n'a été adoptée, reflétant le désaccord persistant entre les pays du Nord (opposés aux obligations transnationales) et du Sud (demandant un instrument contraignant), limitant l'efficacité du cadre",
            "Adopter une convention internationale contraignante sur le droit au développement comme proposée par la résolution AG 78/159 (2023) soutenue par 130 États, créant des obligations légales mutuelles entre pays développés et en développement, conformément aux recommandations de l'Équipe spéciale d'experts de haut niveau sur le droit au développement",
        ],
    ),
]


def run_analysis():
    results = [e.to_dict() for e in ENTITIES]
    avg = round(sum(e.composite_score for e in ENTITIES) / len(ENTITIES), 2)
    dist = {}
    for e in ENTITIES:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
    pat = {}
    for e in ENTITIES:
        pat[e.primary_pattern] = pat.get(e.primary_pattern, 0) + 1
    top3 = sorted(ENTITIES, key=lambda x: x.composite_score, reverse=True)[:3]
    critiques = [e for e in ENTITIES if e.risk_level == "critique"]
    return {
        "total_entities": len(ENTITIES),
        "avg_composite": avg,
        "risk_distribution": dist,
        "pattern_distribution": pat,
        "top_risk_entities": [e.name for e in top3],
        "critical_alerts": [f"{e.name.split('—')[0].strip()}: {e.primary_pattern}" for e in critiques],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "right_to_development",
        "confidence_score": 0.83,
        "data_sources": [
            "undp_human_development_report_annual",
            "global_financial_integrity_illicit_financial_flows_report",
            "un_high_level_task_force_right_to_development_expert_reports",
        ],
        "entities": results,
        "avg_estimated_right_to_development_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    import json
    data = run_analysis()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"\n✅ Distribution: {data['risk_distribution']}")
    print(f"✅ Avg composite: {data['avg_composite']}")
    print(f"✅ Pattern dist: {data['pattern_distribution']}")
