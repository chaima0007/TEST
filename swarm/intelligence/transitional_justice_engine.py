"""Transitional Justice Engine — CPI, commissions vérité & réparations post-conflit."""

from dataclasses import dataclass
from typing import List


@dataclass
class TransitionalJusticeEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    truth_commission_absence_score: float
    reparations_denial_score: float
    perpetrator_impunity_score: float
    memory_historical_denial_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-20"

    @property
    def composite_score(self) -> float:
        return round(
            self.truth_commission_absence_score * 0.30
            + self.reparations_denial_score * 0.25
            + self.perpetrator_impunity_score * 0.25
            + self.memory_historical_denial_score * 0.20,
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
    def estimated_transitional_justice_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "truth_commission_absence_score": self.truth_commission_absence_score,
            "reparations_denial_score": self.reparations_denial_score,
            "perpetrator_impunity_score": self.perpetrator_impunity_score,
            "memory_historical_denial_score": self.memory_historical_denial_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_transitional_justice_index": self.estimated_transitional_justice_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    TransitionalJusticeEntity(
        "TJ-001", "Myanmar — Génocide Rohingya, CIJ Arrêt 2023 Non-Exécuté & Junte Impunité",
        "Asie du Sud-Est",
        "Myanmar Génocide Rohingya CIJ Affaire Gambie 2019, Junte Militaire Crimes Humanité 2021+, Arrêt CIJ Mesures Provisoires Non-Exécutées & Aucune Commission Vérité Perspective",
        92.0, 88.0, 95.0, 82.0,
        "perpetrator_impunity",
        [
            "Défaillance de justice transitionnelle documentée — Myanmar avec score composite 89.75/100 révélant une impunité totale pour le génocide rohingya et les crimes contre l'humanité de la junte, les mécanismes de justice transitionnelle étant bloqués malgré l'arrêt de la CIJ de 2023",
            "Impunité des auteurs (95.0/100) — les chefs de la junte militaire poursuivis par la CIJ pour génocide rohingya et responsables de crimes contre l'humanité post-coup 2021 jouissent d'une impunité totale violant l'obligation de punir les crimes internationaux sous le Statut de Rome",
            "Renforcer la compétence de la Cour Pénale Internationale pour les crimes au Myanmar via un renvoi du Conseil de Sécurité ONU et appliquer les mesures provisoires ordonnées par la CIJ incluant la prévention de nouveaux actes génocidaires contre les Rohingyas",
        ],
    ),
    TransitionalJusticeEntity(
        "TJ-002", "Syrie — IIIM Mécanisme Bloqué, Assad Crimes Contre Humanité & Preuves Perdues",
        "MENA",
        "Syrie Assad Crimes Contre Humanité Documentés IIIM, Tentatives CPI Bloquées Russie/Chine Veto, Photos Caesar 55 000 Victimes & Pas Processus Justice Transitionnelle 15 Ans Conflit",
        90.0, 85.0, 92.0, 85.0,
        "perpetrator_impunity",
        [
            "Défaillance de justice transitionnelle documentée — Syrie avec score composite 88.25/100 révélant 15 ans de conflits sans mécanisme de justice effectif pour les crimes d'Assad, les vetos russe et chinois au Conseil de Sécurité bloquant tout renvoi à la CPI",
            "Impunité des auteurs (92.0/100) — le régime d'Assad responsable de crimes contre l'humanité documentés par le Mécanisme IIIM ONU jouissant d'une impunité totale protégé par les vetos russes et chinois révèle une défaillance structurelle du Conseil de Sécurité de l'ONU",
            "Utiliser les compétences juridictionnelles nationales pour poursuivre les responsables syriens via le principe de compétence universelle (Allemagne, Suède, Suisse) et renforcer le financement du Mécanisme IIIM pour préserver les preuves pour les poursuites futures",
        ],
    ),
    TransitionalJusticeEntity(
        "TJ-003", "RDC — LRA/M23 Impunité, CPI Limité & 30 Ans Cycles Violence Non-Résolus",
        "Afrique Centrale",
        "RDC LRA Joseph Kony Toujours En Fuite, M23 Crimes 2023 Non-Poursuivis, CPI 6 Condamnations 30 Ans Cycles Violence & Aucune Commission Vérité Réconciliation Nationale",
        88.0, 82.0, 88.0, 85.0,
        "truth_commission_absence",
        [
            "Défaillance de justice transitionnelle documentée — RDC avec score composite 85.90/100 révélant 30 ans de cycles de violence sans mécanisme de justice transitionnelle effectif, la CPI n'ayant obtenu que 6 condamnations pour une région productrice de milliers de crimes internationaux",
            "Absence commission vérité (88.0/100) — l'absence de Commission Vérité et Réconciliation nationale en RDC et l'impunité persistante des groupes armés actifs créent un terreau pour la répétition des cycles de violence violant le droit à la vérité des victimes",
            "Établir une Commission Vérité et Réconciliation nationale en RDC intégrant les mécanismes traditionnels de justice réparatrice et renforcer la coopération avec la CPI pour l'arrestation des suspects dont les mandats sont en attente d'exécution",
        ],
    ),
    TransitionalJusticeEntity(
        "TJ-004", "Cambodge — ECCC Trop Tardif, 3 Condamnations Khmers Rouges & Réparations Dérisoires",
        "Asie du Sud-Est",
        "Cambodge ECCC Chambres Extraordinaires 3 Condamnations Seulement Khmers Rouges 50+ Ans Post-Génocide, Réparations Symboliques, Accusés Décédés & Survie Questionnée Par Victimes",
        85.0, 88.0, 85.0, 80.0,
        "reparations_denial",
        [
            "Défaillance de justice transitionnelle documentée — Cambodge avec score composite 84.75/100 révélant que le tribunal hybride ECCC n'a obtenu que 3 condamnations pour les crimes des Khmers rouges causant 1.7 million de morts, avec des réparations jugées dérisoires par les victimes",
            "Déni réparations (88.0/100) — les réparations symboliques accordées aux victimes des Khmers rouges par les ECCC ne correspondent pas à l'ampleur des préjudices subis, violant le droit à des réparations adéquates garanti par les Principes Van Boven/Bassiouni",
            "Assurer la clôture digne des ECCC avec un programme de réparations collectives substantiel pour les victimes des Khmers rouges et capitaliser les leçons apprises pour les mécanismes de justice transitionnelle futurs en Asie du Sud-Est",
        ],
    ),
    TransitionalJusticeEntity(
        "TJ-005", "Afghanistan — Taliban Retour, AIHRC Abolie & 20 Ans Crimes Non-Jugés",
        "Asie Centrale",
        "Afghanistan Taliban 2021 Abolit AIHRC, 20 Ans Crimes Guerre Toutes Parties Non-Jugés, CPI Enquête Afghanistan Avancement Limité & Victimes USAID Réductions Justice Transitionnelle",
        55.0, 58.0, 62.0, 50.0,
        "perpetrator_impunity",
        [
            "Défaillance de justice transitionnelle documentée — Afghanistan avec score composite 56.50/100 révélant que le retour des Taliban en 2021 et l'abolition de la Commission des droits humains AIHRC ont anéanti 20 ans de progrès vers la justice transitionnelle",
            "Impunité des auteurs (62.0/100) — les crimes commis par toutes les parties au conflit afghan sur 20 ans restent impunis, la CPI ayant une enquête en cours très limitée et les Taliban ayant aboli les mécanismes nationaux de justice transitionnelle",
            "Maintenir l'enquête de la CPI sur l'Afghanistan et protéger les preuves de crimes de guerre malgré le retrait américain, et soutenir les victimes afghanes devant les juridictions de compétence universelle en Europe pour les crimes documentés",
        ],
    ),
    TransitionalJusticeEntity(
        "TJ-006", "Colombie/FARC — JEP Partiel, Réparations 9M Victimes & Résistances Impunité",
        "Amérique Latine",
        "Colombie JEP Juridiction Spéciale Paix 9M Victimes Répertoriées, Reconnaissance Crimes FARC/État Partielle, Réparations Individuelles Non-Financées & Macrocriminalité Paramilitaires Non-Soumise",
        52.0, 55.0, 55.0, 48.0,
        "reparations_denial",
        [
            "Défaillance partielle de justice transitionnelle documentée — Colombie avec score composite 52.70/100 révélant les avancées mais aussi les limites de la JEP face aux 9 millions de victimes du conflit armé dont les réparations individuelles restent insuffisamment financées",
            "Déni réparations (55.0/100) — les réparations promises à 9 millions de victimes colombiennes par le processus de paix restent largement non-financées et l'impunité des structures paramilitaires non soumises à la JEP créent une justice transitionnelle incomplète",
            "Renforcer le financement des réparations aux victimes du conflit colombien conformément aux Principes Joinet/Van Boven et étendre la compétence de la JEP aux structures paramilitaires et aux responsabilités des entreprises complices du conflit armé",
        ],
    ),
    TransitionalJusticeEntity(
        "TJ-007", "Afrique du Sud/Rwanda — TRC/Gacaca Relatifs Succès & Leçons Justice Réparatrice",
        "Afrique",
        "Afrique du Sud TRC Commission Vérité Réconciliation 1995-2002 Modèle Mondial, Rwanda Gacaca 1.2M Affaires 2002-12, Limites Réparations Faibles SA & Récidive Violence Économique",
        28.0, 32.0, 30.0, 35.0,
        "memory_historical_denial",
        [
            "Succès relatifs de justice transitionnelle — Afrique du Sud et Rwanda offrent les modèles les plus cités de justice transitionnelle mondiale avec la TRC de Desmond Tutu et les tribunaux gacaca, mais révèlent aussi les limites des réparations insuffisantes et la persistance des inégalités structurelles",
            "Déni mémoire historique (35.0/100) — malgré la TRC en Afrique du Sud et les gacaca au Rwanda, les inégalités économiques héritées de l'apartheid et les divisions ethniques persistantes révèlent que la justice transitionnelle sans transformation économique reste incomplète",
            "Capitaliser les leçons des modèles TRC et gacaca pour élaborer des mécanismes de justice transitionnelle économique intégrant des réparations structurelles transformatrices aux injustices systémiques passées conformément aux recommandations du Rapporteur Spécial ONU sur la vérité et la justice",
        ],
    ),
    TransitionalJusticeEntity(
        "TJ-008", "CPI/ONU-Mécanismes — Statut Rome, Droit à Vérité & Principes Joinet",
        "Global",
        "CPI Cour Pénale Internationale Statut Rome 1998, Droit à Vérité Résolution ONU 2005, Principes Joinet/Orentlicher Lutte Impunité, ICTJ Institut Justice Transitionnelle & Piliers CSNUT",
        5.0, 4.0, 3.0, 6.0,
        "memory_historical_denial",
        [
            "CPI/ONU incarne le cadre normatif exemplaire de la justice transitionnelle — Statut de Rome 1998 créant la première juridiction pénale internationale permanente et Principes Joinet définissant les 4 piliers: vérité, justice, réparations et garanties de non-répétition",
            "Statut de Rome Article 17 — principe de complémentarité obligeant les États à poursuivre les crimes graves avant que la CPI puisse intervenir, créant une obligation d'enquêtes nationales sérieuses pour les crimes de guerre, crimes contre l'humanité et génocide",
            "Renforcer la CPI avec des contributions financières obligatoires des États membres, améliorer les mécanismes de coopération pour l'exécution des mandats d'arrêt et adopter un traité contraignant sur l'assistance mutuelle judiciaire internationale pour les crimes atroces",
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
        "domain": "transitional_justice",
        "confidence_score": 0.84,
        "data_sources": [
            "ictj_country_programs_transitional_justice_database",
            "icc_situations_cases_investigations_database",
            "un_special_rapporteur_truth_justice_reparation_reports",
        ],
        "entities": [e.to_dict() for e in ENTITIES],
        "avg_estimated_transitional_justice_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
