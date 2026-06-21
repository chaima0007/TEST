"""
Caelum Partners — Enforced Disappearance Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Disparitions forcées et droits des familles : violations systémiques du droit international
humanitaire et des droits de l'homme liées à l'enlèvement, à la détention secrète et à la
disparition de personnes par des agents étatiques ou des groupes armés avec leur complicité.

La disparition forcée constitue un crime de droit international continu tant que le sort
de la victime reste inconnu. La Convention internationale pour la protection de toutes les
personnes contre les disparitions forcées (2006) en fait l'un des crimes les plus graves,
particulièrement quand pratiqué de manière systématique, pouvant constituer un crime contre
l'humanité selon le Statut de Rome.

L'Amérique latine reste la région la plus touchée historiquement — plus de 30 000 disparus
sous la dictature argentine (1976-1983), environ 40 000 victimes en Colombie, et le Mexique
avec plus de 111 000 personnes disparues dont des milliers liées au narcotrafic. En Syrie,
plus de 100 000 personnes ont disparu depuis 2011 dans les geôles du régime Assad.

Le droit à la vérité — savoir ce qu'il est advenu des proches disparus — est reconnu comme
droit fondamental autonome par le Conseil des droits de l'homme. Pourtant, les familles
attendent des décennies sans réponse, victimes d'une double disparition : celle de leur proche
et celle de la vérité sur son sort.

Risk levels (disparitions forcées et droits) :
  critique  -> composite >= 60  (disparitions systémiques — crime contre l'humanité actif)
  élevé     -> composite >= 40  (disparitions significatives — impunité structurelle)
  modéré    -> composite >= 20  (risque résiduel — mécanismes vérité insuffisants)
  faible    -> composite < 20   (cadre protecteur — vérité et réparations effectifs)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "disparitions_systeme_etat_crime_humanite": {
        "severity_fr": "Critique",
        "action_fr": "Tribunal pénal international — référé CPI, gel avoirs responsables, sanctions ciblées dirigeants, accès Comité ONU disparitions forcées, libération détenus lieux secrets identifiés",
        "signal_fr": "state_enforced_disappearance_scale_score > 85 — disparitions forcées systémiques organisées par l'État, constituant des crimes contre l'humanité selon le Statut de Rome",
    },
    "narcotrafic_disparitions_complicite": {
        "severity_fr": "Critique",
        "action_fr": "Réforme justice pénale — unités spéciales enquêtes disparitions, protection témoins familles, audit forces sécurité complicité, coopération judiciaire internationale narcotrafic",
        "signal_fr": "criminal_network_disappearance_score > 80 — disparitions forcées liées à des cartels ou groupes armés avec complicité étatique documentée, impunité systémique des auteurs",
    },
    "detention_secrete_torture_incommunicado": {
        "severity_fr": "Critique",
        "action_fr": "Inspection indépendante — accès CICR toutes places de détention, registre détention habeas corpus effectif, prohibition absolue détention incommunicado, sanctions violateurs",
        "signal_fr": "secret_detention_torture_score > 75 — détentions secrètes prolongées sans accès avocat ni famille, lieu de détention dissimulé, torture fréquente et risque disparition définitive",
    },
    "impunite_familles_sans_verite": {
        "severity_fr": "Élevé",
        "action_fr": "Commissions vérité et réconciliation — accès archives sécurité, identification restes ADN, réparations familles, loi amnistie levée, formation magistrats disparitions forcées",
        "signal_fr": "truth_accountability_gap_score > 60 — impunité des auteurs de disparitions, familles sans information sur le sort des proches, archives fermées, processus vérité bloqué",
    },
    "modele_verite_reparation_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter les bonnes pratiques — soutenir mécanismes vérité autres pays, financement banques ADN identifications, formation enquêteurs disparitions, plaidoyer ratification Convention 2006",
        "signal_fr": "composite_score < 20 — processus vérité effectif, restes identifiés, réparations versées, archives ouvertes, ratification Convention 2006 et rapport régulier Comité ONU",
    },
}


@dataclass
class EnforcedDisappearanceRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    state_enforced_disappearance_scale_score: float
    criminal_network_disappearance_score: float
    secret_detention_torture_score: float
    truth_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_enforced_disappearance_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.state_enforced_disappearance_scale_score * 0.30
            + self.criminal_network_disappearance_score * 0.25
            + self.secret_detention_torture_score * 0.25
            + self.truth_accountability_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_enforced_disappearance_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.state_enforced_disappearance_scale_score >= 85:
            return "disparitions_systeme_etat_crime_humanite"
        if self.criminal_network_disappearance_score >= 80:
            return "narcotrafic_disparitions_complicite"
        if self.secret_detention_torture_score >= 75:
            return "detention_secrete_torture_incommunicado"
        if self.composite_score >= 20:
            return "impunite_familles_sans_verite"
        return "modele_verite_reparation_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Disparitions forcées critiques de {n} — disparitions systémiques orchestrées par l'État ou des groupes armés avec complicité étatique, constituant des crimes contre l'humanité continus",
                "Détentions secrètes et torture documentées — lieux de détention dissimulés, accès CICR refusé, familles sans information, double crime : la disparition et le déni de vérité",
                "Violation du droit à la vérité et aux réparations — les familles des disparus sont victimes d'une torture psychologique prolongée, leur droit fondamental à connaître le sort des proches nié",
            ]
        if self.risk_level == "élevé":
            return [
                f"Risque élevé disparitions forcées de {n} — impunité structurelle des auteurs, archives sécurité fermées, mécanismes vérité bloqués, familles sans réparations adéquates ni information",
                "Lacunes dans les enquêtes — les forces de sécurité impliquées ne sont pas poursuivies, les restes des victimes non identifiés faute de banque ADN et de volonté politique",
                "Convention 2006 non ratifiée ou non appliquée — l'absence de mécanisme de rapport au Comité ONU sur les disparitions forcées permet la perpétuation de l'impunité nationale",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque résiduel disparitions de {n} — processus vérité en cours mais incomplet, archives partiellement accessibles, quelques réparations versées sans mécanisme systémique effectif",
                "Réconciliation fragile — les commissions vérité ont documenté des cas mais les poursuites judiciaires restent limitées et les familles sans réparations intégrales ni garanties de non-répétition",
                "Progrès insuffisants — l'identification des restes par ADN avance lentement faute de ressources, et les archives sécuritaires restent partiellement classifiées retardant la vérité",
            ]
        return [
            f"{n} représente un modèle de vérité et réparations pour les disparitions forcées — archives ouvertes, restes identifiés, réparations versées, poursuites judiciaires abouties",
            "Convention internationale 2006 ratifiée et appliquée — rapports réguliers au Comité ONU, habeas corpus effectif, prohibition détention secrète, CICR accès toutes prisons",
            "Modèle banco ADN exportable — identification systématique des restes des victimes, mémorial national, formation magistrats et processus réconciliation nationale reconnu internationalement",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "state_enforced_disappearance_scale_score": self.state_enforced_disappearance_scale_score,
            "criminal_network_disappearance_score": self.criminal_network_disappearance_score,
            "secret_detention_torture_score": self.secret_detention_torture_score,
            "truth_accountability_gap_score": self.truth_accountability_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_enforced_disappearance_rights_index": self.estimated_enforced_disappearance_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[EnforcedDisappearanceRightsEntity] = [
    EnforcedDisappearanceRightsEntity(
        "EDR-001",
        "Syrie/Assad 100K+ Disparus Geôles Régime Depuis 2011",
        "Syrie",
        "Régime Assad 100K+ Disparus Depuis 2011, Geôles Secrètes Saydnaya, Torture Systémique, Documentation Caesar Project, IIMM Enquêtes",
        97.0, 90.0, 95.0, 92.0,
    ),
    EnforcedDisappearanceRightsEntity(
        "EDR-002",
        "Mexique/111K Disparus Narcotrafic Complicité Institutionnelle",
        "Mexique",
        "111K Disparus Registre RNPDNO, Cartels Jalisco Sinaloa, Complicité Forces Sécurité, Ayotzinapa 43 Étudiants Non Résolus, CNDH Impuissance",
        88.0, 92.0, 82.0, 90.0,
    ),
    EnforcedDisappearanceRightsEntity(
        "EDR-003",
        "Corée Nord/Détentions Camps Kwanliso Système Songbun Opposants",
        "Corée du Nord",
        "Camps Kwanliso Système Songbun, Disparitions Famille Entière, Accès CICR Refusé Total, Défecteurs Témoignages, COI ONU 2014 Crimes Humanité",
        95.0, 88.0, 93.0, 85.0,
    ),
    EnforcedDisappearanceRightsEntity(
        "EDR-004",
        "Argentine/CONADEP 30K Disparus Juicio Verdad Réparations",
        "Argentine",
        "30K Disparus Junte 1976-1983, CONADEP Nunca Más, Juicios Verdad En Cours, Réparations Partielles, ADN Banco Identifications Restes",
        75.0, 65.0, 80.0, 88.0,
    ),
    EnforcedDisappearanceRightsEntity(
        "EDR-005",
        "Turquie/Kurdes Disparus Années 90 JİTEM Gendarmes Impunité",
        "Turquie",
        "Kurdes Disparus Années 1990 Conflit, JİTEM Gendarmerie Accusée, Procès Tardifs Faibles Peines, CEDH Condamnations Répétées, Archives Classifiées",
        62.0, 58.0, 65.0, 70.0,
    ),
    EnforcedDisappearanceRightsEntity(
        "EDR-006",
        "Sri Lanka/Post-Guerre 2009 Tamil Disparus Truth Commission Bloquée",
        "Sri Lanka",
        "Tamil Disparus Post-Conflit 2009, OMP Office Missing Persons Blocages, Familles Nord Manifestations Quotidiennes, HRC ONU Recommandations Ignorées",
        58.0, 52.0, 60.0, 65.0,
    ),
    EnforcedDisappearanceRightsEntity(
        "EDR-007",
        "Colombie/JEP 40K Disparus FARC Para Vérité Partielle",
        "Colombie",
        "40K Disparus Conflits Armés, JEP Juridiction Spéciale Paix, Vérité Partielle Accord 2016, Réparations En Cours, UBPD Recherche Disparus",
        32.0, 35.0, 28.0, 40.0,
    ),
    EnforcedDisappearanceRightsEntity(
        "EDR-008",
        "Chili/Comisión Valech Reparaciones ADN Pinochet Victimes",
        "Chili",
        "Valech Commission 1991 Réparations, ADN Identifications Restes, Pinochet Jugé Partiellement, Archives Ouvertes, Musée Mémoire Santiago",
        8.0, 6.0, 7.0, 10.0,
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
        "domain": "enforced_disappearance_rights",
        "confidence_score": 0.91,
        "data_sources": [
            "un_convention_enforced_disappearances_2006",
            "icrc_missing_persons_reports",
            "amnesty_international_disappearances",
            "iimm_syria_investigations",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_enforced_disappearance_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_enforced_disappearance_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Enforced Disappearance Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    print(f"Distribution: {r['risk_distribution']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
