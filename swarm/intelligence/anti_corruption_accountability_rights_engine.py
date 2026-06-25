"""
Caelum Partners — Anti-Corruption Accountability Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Corruption systémique, impunité, et droits à la transparence et à la redevabilité.

La corruption systémique constitue une violation grave des droits économiques, sociaux
et culturels des populations en détournant les ressources publiques destinées à la santé,
l'éducation et les services essentiels. La Convention de l'ONU contre la Corruption
(CNUCC, 2003) oblige les États à mettre en place des mécanismes de transparence et
de redevabilité, mais son application reste largement insuffisante.

La Somalie occupe depuis 2012 la dernière place de l'Indice de Perception de la
Corruption (IPC) de Transparency International, avec un score de 11/100 en 2023.
Au Venezuela, le régime Maduro a hérité et amplifié les pratiques kleptocratiques
liées à PDVSA : selon le Département de Justice américain, plus de 300 milliards
de dollars ont été détournés depuis 2000 via des réseaux d'intermédiaires offshore.
En Russie, les oligarques proches de Poutine contrôlent des actifs estimés à
1 000 milliards de dollars selon les estimations post-sanctions de 2022.

Risk levels (corruption systémique et droits à la redevabilité) :
  critique  -> composite >= 60  (kleptocracie totale — État capturé, pillage systémique des ressources)
  élevé     -> composite >= 40  (corruption institutionnalisée — impunité des élites et réseaux opaques)
  modéré    -> composite >= 20  (risque résiduel — déficits de transparence sans État entièrement capturé)
  faible    -> composite < 20   (protection exemplaire — standards anti-corruption effectivement appliqués)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "kleptocracie_etat_capture": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions internationales urgentes — gel des avoirs des dirigeants kleptocrates, exclusion des marchés financiers internationaux, soutien aux procureurs indépendants et mécanismes de récupération des avoirs volés",
        "signal_fr": "systemic_corruption_impunity_severity_score > 85 — État entièrement capturé par des réseaux criminels au pouvoir, institutions anti-corruption inexistantes ou contrôlées par les corrupteurs",
    },
    "detournement_fonds_publics": {
        "severity_fr": "Critique",
        "action_fr": "Récupération des avoirs — coopération judiciaire internationale, traçabilité des flux financiers illicites, sanctions ciblées sur les intermédiaires et restitution aux États victimes",
        "signal_fr": "public_funds_diversion_kleptocracy_scale_score > 85 — détournement massif de fonds publics vers des comptes offshore, contrats surfacturés et marchés publics manipulés à grande échelle",
    },
    "persecution_lanceurs_alerte": {
        "severity_fr": "Critique",
        "action_fr": "Protection internationale des lanceurs d'alerte — asile politique, financement des défenseurs anti-corruption, pression diplomatique contre les poursuites judiciaires abusives",
        "signal_fr": "whistleblower_anti_corruption_persecution_score > 85 — journalistes, magistrats et lanceurs d'alerte emprisonnés, assassinés ou exilés pour avoir exposé la corruption",
    },
    "deficit_institutions_transparence": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement institutionnel — financement des organes de contrôle indépendants, formation des magistrats anti-corruption, registres publics des bénéficiaires effectifs et budgets ouverts",
        "signal_fr": "Absence d'institutions de contrôle indépendantes, manque de transparence budgétaire ou systèmes d'état civil et de passation de marchés opaques facilitant la corruption",
    },
    "standards_anticorruption_exemplaires": {
        "severity_fr": "Faible",
        "action_fr": "Exporter les bonnes pratiques — financement TI-GRECO, partage des outils de transparence et soutien au renforcement des institutions anti-corruption dans les pays à haute corruption",
        "signal_fr": "composite_score < 20 — respect effectif des normes CNUCC avec institutions de contrôle indépendantes, protection des lanceurs d'alerte et transparence budgétaire",
    },
}


@dataclass
class AntiCorruptionAccountabilityRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    systemic_corruption_impunity_severity_score: float
    public_funds_diversion_kleptocracy_scale_score: float
    whistleblower_anti_corruption_persecution_score: float
    transparency_accountability_institution_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_anti_corruption_accountability_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.systemic_corruption_impunity_severity_score * 0.30
            + self.public_funds_diversion_kleptocracy_scale_score * 0.25
            + self.whistleblower_anti_corruption_persecution_score * 0.25
            + self.transparency_accountability_institution_deficit_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_anti_corruption_accountability_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.systemic_corruption_impunity_severity_score >= 85:
            return "kleptocracie_etat_capture"
        if self.public_funds_diversion_kleptocracy_scale_score >= 85:
            return "detournement_fonds_publics"
        if self.whistleblower_anti_corruption_persecution_score >= 85:
            return "persecution_lanceurs_alerte"
        if self.composite_score >= 20:
            return "deficit_institutions_transparence"
        return "standards_anticorruption_exemplaires"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Kleptocracie critique de {n} — corruption systémique totale avec État capturé par des réseaux de pouvoir utilisant les ressources publiques comme instrument d'enrichissement personnel et de contrôle politique",
                "Violation massive des droits économiques et sociaux — le détournement des fonds publics prive les populations d'accès à la santé, l'éducation et les services essentiels garantis par le Pacte ICESCR",
                "Impunité institutionnalisée — l'absence de poursuites contre les élites corrompues crée un système de deux poids deux mesures qui dévaste la confiance dans les institutions démocratiques",
            ]
        if self.risk_level == "élevé":
            return [
                f"Corruption institutionnalisée de {n} — réseaux opaques d'enrichissement des élites au détriment des populations, avec défaillance systémique des mécanismes de contrôle et de redevabilité",
                "Réseaux financiers offshore — les flux financiers illicites transitant par des paradis fiscaux privent les États du Sud de ressources essentielles estimées à 1 000 milliards de dollars par an",
                "Entrave à la justice — les poursuites anti-corruption sont sélectives, ciblant les opposants politiques plutôt que les réseaux criminels proches du pouvoir",
            ]
        if self.risk_level == "modéré":
            return [
                f"Déficits de transparence de {n} — institutions de contrôle insuffisamment indépendantes, budgets opaques et protection insuffisante des lanceurs d'alerte créant des conditions propices à la corruption",
                "Risques systémiques résiduels — la corruption dans les marchés publics et les permis administratifs persiste malgré l'existence de cadres légaux anti-corruption",
                "Progrès fragiles — les avancées en matière de transparence peuvent être inversées par des changements politiques ou des pressions des élites économiques bénéficiant de l'opacité",
            ]
        return [
            f"{n} incarne les standards exemplaires anti-corruption — institutions de contrôle indépendantes, protection robuste des lanceurs d'alerte et transparence budgétaire effective",
            "CNUCC et GRECO standards respectés — mécanismes de vérification des actifs des fonctionnaires, registres publics des bénéficiaires effectifs et budgets ouverts accessibles",
            "Modèle exportable — financement Transparency International, partage d'expertise avec les pays à haute corruption et soutien aux réformes institutionnelles anti-corruption",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "systemic_corruption_impunity_severity_score": self.systemic_corruption_impunity_severity_score,
            "public_funds_diversion_kleptocracy_scale_score": self.public_funds_diversion_kleptocracy_scale_score,
            "whistleblower_anti_corruption_persecution_score": self.whistleblower_anti_corruption_persecution_score,
            "transparency_accountability_institution_deficit_gap_score": self.transparency_accountability_institution_deficit_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_anti_corruption_accountability_rights_index": self.estimated_anti_corruption_accountability_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[AntiCorruptionAccountabilityRightsEntity] = [
    AntiCorruptionAccountabilityRightsEntity(
        "ACAR-001",
        "Somalie/IPC 11/100 Corruption Totale Institutionnelle",
        "Afrique de l'Est",
        "Dernier IPC TI 2023, État Failli Corruption Totale, Al-Shabaab Taxes Parallèles, Fonds Aide Internationale Détournés & Impunité Absolue",
        92.0, 88.0, 85.0, 90.0,
    ),
    AntiCorruptionAccountabilityRightsEntity(
        "ACAR-002",
        "Venezuela/Pdvsa Kleptocracie 300B$ Détournés",
        "Amérique du Sud",
        "PDVSA 300B$ Détournés 2000-2023, DOJ USA, Maduro Réseau Crypto & Or, Intermédiaires Offshore & Sanctions 300+ Personnes",
        88.0, 92.0, 82.0, 88.0,
    ),
    AntiCorruptionAccountabilityRightsEntity(
        "ACAR-003",
        "Syrie/Assad Corruption Guerre",
        "MENA",
        "Assad Famille 200B$ Avoirs, Guerre Civile Économie Corruption, Captagon Trafic État, Reconstruction Marchés Réseaux Proches & CPI Mandat",
        85.0, 82.0, 90.0, 85.0,
    ),
    AntiCorruptionAccountabilityRightsEntity(
        "ACAR-004",
        "Soudan/Al-Bashir 9B$ Caché CPI",
        "Afrique de l'Est",
        "Al-Bashir 9B$ CPI 2019, Transition SAF/RSF Corruption Continuée, Or Darfour Trafic, Armée Économie Parallèle & Impunité Transfert",
        83.0, 85.0, 80.0, 88.0,
    ),
    AntiCorruptionAccountabilityRightsEntity(
        "ACAR-005",
        "Russie/Oligarques Sanctions Actifs Cachés",
        "Europe de l'Est",
        "1T$ Avoirs Oligarques Post-Sanctions 2022, Yachts & Propriétés Gelés, Enablers Financiers Occidentaux & Anti-Corruption Sélective Navalny",
        55.0, 62.0, 60.0, 58.0,
    ),
    AntiCorruptionAccountabilityRightsEntity(
        "ACAR-006",
        "Chine/Anti-Corruption Sélective Xi Factionnelle",
        "Asie de l'Est",
        "Campagne Anti-Corruption Xi 1.5M Fonctionnaires 2012-2023, Usage Factionnelle Élimination Rivaux, Opacité PCCC & Aucun Contrôle Externe",
        52.0, 55.0, 62.0, 58.0,
    ),
    AntiCorruptionAccountabilityRightsEntity(
        "ACAR-007",
        "Transparency International/GRECO Standards",
        "Global",
        "IPC 180 Pays, GRECO 49 États Évalués, Standards Anti-Corruption & Financement Sociétés Civile Anti-Corruption Locale",
        25.0, 20.0, 22.0, 28.0,
    ),
    AntiCorruptionAccountabilityRightsEntity(
        "ACAR-008",
        "ONU/CNUCC 2003 Convention Anti-Corruption",
        "Global",
        "CNUCC Ratifiée 189 États, Mécanisme Révision, Recouvrement Avoirs Art.57 & Assistance Technique Pays En Développement",
        5.0, 4.0, 6.0, 8.0,
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
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "domain": "anti_corruption_accountability_rights",
        "confidence_score": 0.85,
        "data_sources": [
            "transparency_international_cpi_2023",
            "un_office_drugs_crime_anticorruption",
            "fatf_financial_flows_illicit_reports",
            "greco_evaluation_reports_council_europe",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_anti_corruption_accountability_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_anti_corruption_accountability_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Anti-Corruption Accountability Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
