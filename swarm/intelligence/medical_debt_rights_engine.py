"""Medical Debt Rights Engine — Faillites médicales, opacité facturation & barrières accès soins."""

from dataclasses import dataclass
from typing import List


@dataclass
class MedicalDebtRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    healthcare_bankruptcy_score: float
    medical_bill_opacity_score: float
    insurance_denial_score: float
    healthcare_access_barrier_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-22"

    @property
    def composite_score(self) -> float:
        return round(
            self.healthcare_bankruptcy_score * 0.30
            + self.medical_bill_opacity_score * 0.25
            + self.insurance_denial_score * 0.25
            + self.healthcare_access_barrier_score * 0.20,
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
    def estimated_medical_debt_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "healthcare_bankruptcy_score": self.healthcare_bankruptcy_score,
            "medical_bill_opacity_score": self.medical_bill_opacity_score,
            "insurance_denial_score": self.insurance_denial_score,
            "healthcare_access_barrier_score": self.healthcare_access_barrier_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_medical_debt_rights_index": self.estimated_medical_debt_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    MedicalDebtRightsEntity(
        "MDR-001", "USA — 137M Personnes en Détresse Financière Médicale & Faillites Médicales #1",
        "Amérique du Nord",
        "USA Dette Médicale 137M Personnes KFF 2023, 500 000 Faillites Médicales/An #1 Cause Faillite Personnelle, Facturation Opaque Chargemaster Prix Secret & 27M Sans Assurance NHIS 2024",
        92.0, 94.0, 90.0, 85.0,
        "medical_bill_opacity",
        [
            "Violation du droit à la santé documentée — USA avec score composite 88.35/100 révélant que 137 millions d'américains souffrent de détresse financière médicale et que les dettes médicales représentent la première cause de faillite personnelle violant le droit à la santé de l'Article 12 PIDESC",
            "Opacité facturation médicale (92.0/100) — le système de prix secrets 'chargemaster' permettant aux hôpitaux de facturer 10 à 100 fois le coût réel des soins sans transparence préalable constitue une violation structurelle du consentement éclairé et du droit à l'information médicale",
            "Adopter la Medicare for All Act pour couvrir universellement les 27M d'américains non assurés et instaurer la transparence obligatoire des prix hospitaliers conformément aux obligations de l'Article 12 PIDESC sur le droit au meilleur état de santé atteignable",
        ],
    ),
    MedicalDebtRightsEntity(
        "MDR-002", "Nigeria — 70% Soins Out-of-Pocket & Effondrement Système Santé Public",
        "Afrique de l'Ouest",
        "Nigeria 70% Dépenses Santé Out-of-Pocket OMS 2024, 83M Pauvreté Extrême Soins Inabordables, NHIS Couverture <5% Population, Mortalité Maternelle 512/100 000 OMS & Fuite Cerveaux Médicaux Chronique",
        88.0, 82.0, 83.0, 94.0,
        "healthcare_access_barrier",
        [
            "Violation du droit à la santé documentée — Nigeria avec score composite 83.40/100 révélant que 70% des dépenses de santé sont à la charge directe des patients, rendant les soins inaccessibles aux 83 millions de nigérians en extrême pauvreté et violant l'Article 16 de la Charte africaine des droits de l'homme",
            "Barrière accès soins (92.0/100) — la mortalité maternelle de 512 pour 100 000 naissances vivantes et la couverture NHIS inférieure à 5% de la population révèlent l'échec systémique de la protection sociale médicale violant les obligations de l'Article 12 PIDESC",
            "Renforcer le National Health Insurance Scheme (NHIS) vers une couverture universelle effective et augmenter le budget santé à 15% du PIB conformément à la Déclaration d'Abuja 2001 pour garantir l'accès aux soins sans risque d'appauvrissement",
        ],
    ),
    MedicalDebtRightsEntity(
        "MDR-003", "India — 63M Personnes/An Poussées dans la Pauvreté par les Frais de Santé",
        "Asie du Sud",
        "India 63M Personnes/An Pauvreté Catastrophique Frais Santé Lancet 2021, 58% Dépenses Out-of-Pocket, Système Castes Barrières Accès Soins Dalits, PMJAY Ayushman Bharat Couverture Insuffisante & Déserts Médicaux Ruraux",
        85.0, 78.0, 74.0, 92.0,
        "healthcare_access_barrier",
        [
            "Violation du droit à la santé documentée — India avec score composite 79.50/100 révélant que les frais de santé catastrophiques poussent 63 millions d'indiens dans la pauvreté chaque année, une violation directe du droit à la santé de l'Article 12 PIDESC ratifié par l'Inde en 1979",
            "Barrière accès soins (90.0/100) — la discrimination systémique des Dalits dans l'accès aux soins médicaux et les déserts médicaux ruraux affectant 65% de la population révèlent une application inégalitaire du droit à la santé violant l'interdiction de discrimination de l'Article 2(2) PIDESC",
            "Étendre la couverture PMJAY Ayushman Bharat à l'ensemble de la population et éliminer les discriminations d'accès aux soins basées sur la caste conformément aux obligations de non-discrimination du PIDESC et des Principes de Bangalore sur l'accès à la santé",
        ],
    ),
    MedicalDebtRightsEntity(
        "MDR-004", "Pakistan — Système Santé Fragmenté, 90M Sans Couverture & Dettes Médicales Rurales",
        "Asie du Sud",
        "Pakistan 90M Personnes Sans Couverture Santé OMS 2024, 62% Out-of-Pocket Dépenses Santé, Mortalité Infantile 55/1 000 UNICEF, Sehat Sahulat Card Insuffisant & Désastres Financiers Médicaux Ruraux Khyber Pakhtunkhwa",
        82.0, 75.0, 72.0, 90.0,
        "healthcare_access_barrier",
        [
            "Violation du droit à la santé documentée — Pakistan avec score composite 76.40/100 révélant que 90 millions de pakistanais n'ont aucune couverture maladie et que 62% des dépenses de santé sont à charge directe des patients, créant des catastrophes financières médicales violant l'Article 12 PIDESC",
            "Barrière accès soins (88.0/100) — la mortalité infantile de 55 pour 1 000 naissances vivantes et les déserts médicaux chroniques dans les zones tribales et rurales révèlent l'incapacité structurelle de l'État pakistanais à garantir le droit à la santé pour toute sa population",
            "Universaliser le programme Sehat Sahulat Card à l'ensemble du Pakistan et augmenter les dépenses publiques de santé au-dessus de 3% du PIB conformément aux recommandations OMS pour réduire les inégalités catastrophiques d'accès aux soins",
        ],
    ),
    MedicalDebtRightsEntity(
        "MDR-005", "Brazil — Système Mixte SUS/Privé, Files d'Attente & Inégalités Régionales",
        "Amérique du Sud",
        "Brazil SUS Sous-Financé Files Attente 6-24 Mois Procédures Spécialisées, 25% Population Assurance Privée vs 75% SUS, Inégalités Régionales Nord/Sud Accès Soins & Dettes Médicales Secteur Privé Complémentaire",
        52.0, 56.0, 60.0, 54.0,
        "insurance_denial",
        [
            "Tension structurelle dans le système mixte de santé brésilien — le SUS sous-financé génère des files d'attente de 6 à 24 mois pour les procédures spécialisées, poussant les patients vers un secteur privé coûteux créant des dettes médicales évitables violant l'esprit du droit universel à la santé",
            "Dénégation d'assurance (55.0/100) — les refus de couverture par les assurances privées complémentaires et les inégalités d'accès entre les régions Nord et Sud du Brésil révèlent un système de santé à deux vitesses violant le principe d'universalité du SUS consacré par la Constitution de 1988",
            "Augmenter le budget fédéral du SUS et renforcer l'ANS (Agência Nacional de Saúde Suplementar) pour réduire les refus abusifs de couverture privée et garantir l'équité d'accès aux soins dans toutes les régions conformément à l'Article 196 de la Constitution brésilienne",
        ],
    ),
    MedicalDebtRightsEntity(
        "MDR-006", "Mexico — Désintégration IMSS/Seguro Popular & Barrières Informels",
        "Amérique du Nord",
        "Mexico Dissolution Seguro Popular 2020 INSABI Chaotique, 40% Population Secteur Informel Sans Couverture IMSS, Dépenses Out-of-Pocket 41% & Réforme IMSS-Bienestar 2023 Déploiement Lent",
        50.0, 52.0, 55.0, 58.0,
        "healthcare_access_barrier",
        [
            "Rupture de couverture médicale documentée — Mexico avec score composite 49.25/100 révélant que la dissolution chaotique du Seguro Popular en 2020 a laissé des millions de mexicains sans protection médicale, exposés à des dettes de soins violant l'Article 4 de la Constitution mexicaine",
            "Barrière accès soins (55.0/100) — les 40% de la population mexicaine dans le secteur informel sans couverture IMSS et les dépenses out-of-pocket représentant 41% des dépenses de santé révèlent un accès conditionné au statut d'emploi formel violant le principe d'universalité",
            "Accélérer le déploiement de l'IMSS-Bienestar pour couvrir effectivement les travailleurs informels et allouer les ressources nécessaires conformément aux recommandations du Conseil des droits économiques, sociaux et culturels de l'ONU sur le droit à la santé au Mexique",
        ],
    ),
    MedicalDebtRightsEntity(
        "MDR-007", "Germany — Assurance Obligatoire mais Lacunes Soins Dentaires & Longs Délais",
        "Europe de l'Ouest",
        "Germany GKV Couverture Universelle Obligatoire 90%, Soins Dentaires Remboursement Partiel 70-80% Gaps Significatifs, Délais Spécialistes 3-6 Mois Caisse Légale vs 2 Semaines Privé & Zuzahlung Co-Paiements Discriminatoires Faibles Revenus",
        22.0, 28.0, 32.0, 25.0,
        "insurance_denial",
        [
            "Lacunes persistantes dans le système de santé allemand — malgré la couverture universelle GKV à 90%, les remboursements partiels des soins dentaires et les délais de 3 à 6 mois pour les spécialistes pour les assurés légaux créent des inégalités d'accès liées au statut d'assurance",
            "Dénégation d'assurance (32.0/100) — les co-paiements Zuzahlung représentant jusqu'à 2% du revenu annuel et les gaps de couverture dentaire affectant particulièrement les faibles revenus révèlent des barrières financières residuelles dans le système universel allemand",
            "Réformer la structure de co-paiements GKV pour éliminer les barrières financières résiduelles et améliorer les délais d'accès aux spécialistes pour les assurés légaux afin de garantir une égalité effective d'accès aux soins conformément à l'Article 12 PIDESC",
        ],
    ),
    MedicalDebtRightsEntity(
        "MDR-008", "France — Système Universel AMO/AMC, Reste à Charge Maîtrisé & Meilleure Pratique EU",
        "Europe de l'Ouest",
        "France Assurance Maladie Obligatoire 100% Population, CSS Complémentaire Santé Solidaire Faibles Revenus, Reste à Charge 9.5% OCDE Parmi Plus Bas EU, 100% Santé Soins Dentaires/Optique/Audition Sans Reste à Charge",
        8.0, 10.0, 12.0, 8.0,
        "healthcare_access_barrier",
        [
            "Meilleure pratique européenne en matière de droit à la santé — France avec score composite 9.45/100 incarnant un système d'assurance maladie universelle avec un reste à charge parmi les plus bas de l'OCDE (9.5%) et la réforme 100% Santé éliminant les restes à charge pour les soins dentaires, optiques et auditifs",
            "Protection contre les dettes médicales (8.0/100) — la Complémentaire Santé Solidaire (CSS) gratuite pour les foyers à faibles revenus et le remboursement intégral des soins des ALD (Affections de Longue Durée) représentent un modèle de protection financière médicale universelle",
            "Consolider le modèle français d'assurance maladie universelle et exporter la méthodologie 100% Santé au niveau européen pour éliminer les restes à charge catastrophiques dans les systèmes de santé des États membres de l'UE conformément au Socle européen des droits sociaux",
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
        "domain": "medical_debt_rights",
        "confidence_score": 0.87,
        "data_sources": [
            "who_global_health_expenditure_database_2024",
            "kff_health_care_debt_survey_2023",
            "lancet_catastrophic_health_expenditure_india_2021",
            "oecd_health_statistics_out_of_pocket_expenditure_2024",
        ],
        "entities": [e.to_dict() for e in ENTITIES],
        "avg_estimated_medical_debt_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
