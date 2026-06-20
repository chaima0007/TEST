"""Social Protection Engine — Wave 37"""

from dataclasses import dataclass
from typing import List


@dataclass
class SocialProtectionEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    social_security_coverage_gap_score: float
    pension_system_collapse_score: float
    child_poverty_welfare_failure_score: float
    informal_worker_exclusion_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.social_security_coverage_gap_score * 0.30
            + self.pension_system_collapse_score * 0.25
            + self.child_poverty_welfare_failure_score * 0.25
            + self.informal_worker_exclusion_score * 0.20,
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
    def primary_pattern(self) -> str:
        scores = {
            "lacune_couverture_securite_sociale": self.social_security_coverage_gap_score,
            "effondrement_systeme_pension": self.pension_system_collapse_score,
            "pauvrete_enfants_defaillance_aide": self.child_poverty_welfare_failure_score,
            "exclusion_travailleurs_informels": self.informal_worker_exclusion_score,
        }
        return max(scores, key=scores.get)

    @property
    def estimated_social_protection_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.sector,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "social_security_coverage_gap_score": self.social_security_coverage_gap_score,
            "pension_system_collapse_score": self.pension_system_collapse_score,
            "child_poverty_welfare_failure_score": self.child_poverty_welfare_failure_score,
            "informal_worker_exclusion_score": self.informal_worker_exclusion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_social_protection_index": self.estimated_social_protection_index,
            "last_updated": "2026-06-20",
        }

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Défaillance de la protection sociale documentée — {self.name} avec score composite {self.composite_score}/100 révélant des lacunes systémiques violant l'Article 22 de la DUDH et l'Article 9 du PIDESC sur le droit à la sécurité sociale",
            f"Lacune de couverture sécurité sociale ({self.social_security_coverage_gap_score}/100) — l'exclusion massive de travailleurs de toute protection sociale constitue une violation de l'Observation Générale 19 du Comité PIDESC sur le droit à la sécurité sociale",
            "Activer le Rapporteur Spécial ONU sur l'extrême pauvreté et les droits humains et exiger l'application des Recommandations OIT 202 sur les Socles de Protection Sociale pour garantir un minimum de protection à chaque personne",
        ]


ENTITIES = [
    SocialProtectionEntity("SP-001", "Afrique Sub-Saharienne — 85% Travailleurs Secteur Informel Exclus, Pensions 5% & Aléas", "Afrique de l'Ouest/Est", "Afrique Sub-Saharienne 85% Emploi Informel OIT, Pensions Formelles <5% Population, Transferts Sociaux 1-2% PIB Insuffisants & 400M Personnes Zéro Protection Sociale", 92, 88, 88, 92),
    SocialProtectionEntity("SP-002", "Inde — 93% Informels Non-Couverts, MGNREGA Coupures & Aadhaar Exclusion Numérique", "Asie du Sud", "Inde 93% Informels Non-Couverts Sécurité Sociale, MGNREGA Budget Coupé Pandémie, Aadhaar Exclusion Biométrique 200M Bénéficiaires Potentiels & PM Kisan Couverture Lacunaire", 88, 82, 88, 92),
    SocialProtectionEntity("SP-003", "Haïti/Centrafrique — Zéro Système Sécurité Sociale Fonctionnel, Fonds International Bloqué", "Caraïbes/Afrique Centrale", "Haïti Système Sécurité Sociale Effondré Instabilité, Centrafrique 0% Couverture Santé/Retraite, Dons Internationaux Détournés & Population 90%+ Sans Protection Formelle", 85, 88, 90, 82),
    SocialProtectionEntity("SP-004", "Brésil/Amérique Latine — Bolsa Familia Coupures Bolsonaro, Inégalités GINI & Informels", "Amérique Latine", "Brésil Bolsa Familia Coupures 2021-22 Bolsonaro 3M Exclus, GINI 0.53 Inégalités Extrêmes, 40% Travailleurs Informels Non-Couverts INSS & Reforma Previdência Coupes", 82, 88, 82, 82),
    SocialProtectionEntity("SP-005", "USA — Medicaid Cliffs, Aucun Congé Parental Fédéral & 11% Sans Assurance Maladie", "Amérique du Nord", "USA Seul Pays OCDE Sans Congé Parental Fédéral, 11% Population 37M Sans Assurance Maladie 2022, Medicaid Cliff Traps Travailleurs Pauvres & SNAP Benefits Conditionnalité Sévère", 52, 48, 62, 55),
    SocialProtectionEntity("SP-006", "Europe/Austérité — Grèce Retraites -45%, Espagne Chômage 28% 2013 & Precariat", "Europe", "Grèce Retraites Coupées -45% Troïka, Espagne Chômage 28% 2013 Jeunes 55%, Austérité UK Universal Credit Dysfonctionnel & Précariat Européen Gig Economy Non-Couvert", 52, 55, 50, 55),
    SocialProtectionEntity("SP-007", "Japon/Corée — Working Poor, Kiso Seikatsu Faillite & Non-Regular Workers Exclus", "Asie du Nord-Est", "Japon 7M Non-Regular Workers Non-Couverts Pension/Santé, Kiso Seikatsu (Aide Sociale) Stigmate, Corée Working Poor 5M & Personnes Âgées Pauvreté 40% Retraites Insuffisantes", 28, 32, 28, 30),
    SocialProtectionEntity("SP-008", "OIT/PIDESC — Recommandation 202 Socles Protection Sociale & Plancher Social Mondial", "Global", "OIT Recommandation 202 Socles Protection Sociale 2012, PIDESC Article 9 Sécurité Sociale, OIT Rapport Mondial Protection Sociale 2020-22 & Rapport ONU Rapporteur Extrême Pauvreté", 5, 4, 3, 6),
]


def summary() -> dict:
    entities_data = [e.to_dict() for e in ENTITIES]
    avg = round(sum(e.composite_score for e in ENTITIES) / len(ENTITIES), 2)
    risk_dist = {}
    pattern_dist = {}
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
        "domain": "social_protection",
        "confidence_score": 0.81,
        "data_sources": [
            "ilo_world_social_protection_report",
            "un_special_rapporteur_extreme_poverty_human_rights",
            "world_bank_aspire_social_protection_database",
        ],
        "entities": entities_data,
        "avg_estimated_social_protection_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
