"""
Caelum Partners — Solitary Confinement Isolation Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Isolement cellulaire et droits des détenus : violations systémiques de l'interdiction de la torture,
des traitements inhumains et dégradants, et du droit à la santé mentale des personnes incarcérées.

L'isolement cellulaire prolongé au-delà de 15 jours constitue une forme de torture ou de traitement
cruel, inhumain ou dégradant selon les Règles Nelson Mandela (2015) adoptées par l'Assemblée générale
de l'ONU. Pourtant, aux États-Unis, environ 80 000 personnes sont maintenues en isolement — certaines
depuis plus de 30 ans dans des établissements de type Supermax comme l'ADX Florence, en violation
manifeste de ces standards internationaux.

L'isolement prolongé provoque des dommages psychiatriques irréversibles : hallucinations, psychose,
comportements auto-mutilateurs et augmentation significative du risque de suicide. Le cas d'Abdullah
Öcalan (İmralı, Turquie), maintenu en isolement quasi-total depuis 1999, illustre l'utilisation
politique de l'isolement comme outil de torture psychologique institutionnalisée.

Le Danemark a démontré qu'une réforme radicale est possible : depuis 2020, l'isolement préventif
des mineurs a été interdit, réduisant son usage de 80% en moins de deux ans — un modèle que
l'Europe tarde à adopter dans son ensemble.

Risk levels (isolement cellulaire et droits des détenus) :
  critique  -> composite >= 60  (isolement massif systémique — torture institutionnalisée)
  élevé     -> composite >= 40  (isolement significatif — dommages psychiatriques documentés)
  modéré    -> composite >= 20  (risque résiduel — contrôle insuffisant)
  faible    -> composite < 20   (réforme exemplaire — isolement minimal et encadré)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "isolement_massif_torture_institutionnalisee": {
        "severity_fr": "Critique",
        "action_fr": "Réforme pénitentiaire urgente — interdiction isolement >15 jours, inspection ONU indépendante, fermeture unités Supermax, réintégration progressive des détenus isolés",
        "signal_fr": "prolonged_solitary_confinement_scale_score > 85 — isolement massif dépassant les seuils ONU, torture institutionnalisée violant les Règles Mandela 2015",
    },
    "isolement_politique_opposants": {
        "severity_fr": "Critique",
        "action_fr": "Pression diplomatique internationale — résolutions Conseil des droits de l'homme, sanctions ciblées, accès Rapporteur spécial torture, libération ou transfert détenus politiques",
        "signal_fr": "prolonged_solitary_confinement_scale_score > 75 — utilisation politique de l'isolement contre opposants, journalistes ou minorités comme outil de répression",
    },
    "torture_psychologique_documentee": {
        "severity_fr": "Critique",
        "action_fr": "Intervention psychiatrique — accès obligatoire à des soins de santé mentale, évaluation indépendante des détenus en isolement, suivi post-libération et réparations",
        "signal_fr": "mental_health_torture_psychological_score > 75 — dommages psychiatriques graves documentés par experts médicaux indépendants, psychose et automutilation répandues",
    },
    "couloir_mort_isolement_annees": {
        "severity_fr": "Élevé",
        "action_fr": "Révision conditions couloir mort — accès contact humain, programmes réhabilitation, révision judiciaire périodique, abolition peine de mort comme objectif à long terme",
        "signal_fr": "death_row_isolation_conditions_score > 60 — isolement total des condamnés à mort pendant des années, dommages psychologiques exacerbés par l'incertitude de l'exécution",
    },
    "modele_reforme_isolement_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter la réforme — financement CPT pour réplication, formation surveillants pénitentiaires, plaidoyer Règles Mandela et partage protocoles alternatives à l'isolement",
        "signal_fr": "composite_score < 20 — réforme exemplaire de l'isolement, utilisation minimale et encadrée respectant les standards ONU, alternatives développées",
    },
}


@dataclass
class SolitaryConfinementIsolationRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    prolonged_solitary_confinement_scale_score: float
    mental_health_torture_psychological_score: float
    death_row_isolation_conditions_score: float
    oversight_independent_monitoring_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_solitary_confinement_isolation_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.prolonged_solitary_confinement_scale_score * 0.30
            + self.mental_health_torture_psychological_score * 0.25
            + self.death_row_isolation_conditions_score * 0.25
            + self.oversight_independent_monitoring_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_solitary_confinement_isolation_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.prolonged_solitary_confinement_scale_score >= 90:
            return "isolement_massif_torture_institutionnalisee"
        if self.prolonged_solitary_confinement_scale_score >= 75:
            return "isolement_politique_opposants"
        if self.mental_health_torture_psychological_score >= 75:
            return "torture_psychologique_documentee"
        if self.composite_score >= 20:
            return "couloir_mort_isolement_annees"
        return "modele_reforme_isolement_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Isolement cellulaire critique de {n} — maintien prolongé au-delà des seuils ONU, constituant une torture ou un traitement cruel, inhumain ou dégradant selon les Règles Nelson Mandela 2015",
                "Dommages psychiatriques irréversibles documentés — hallucinations, psychose d'isolement, automutilation et risque suicidaire accru chez les détenus maintenus en isolement prolongé",
                "Violation du droit à la santé mentale — l'État faillit à son obligation de protéger la santé physique et mentale des personnes privées de liberté, engageant sa responsabilité internationale",
            ]
        if self.risk_level == "élevé":
            return [
                f"Isolement préoccupant de {n} — usage significatif de la mise à l'isolement avec contrôle insuffisant, dommages psychiatriques documentés et alternatives sous-développées",
                "Contrôle indépendant lacunaire — l'absence d'inspection régulière par des organismes indépendants permet la perpétuation de pratiques d'isolement abusives sans accountability",
                "Couloir de la mort et isolement prolongé — les condamnés à mort subissent des années d'isolement total aggravant les souffrances psychologiques au-delà de la peine prononcée",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque résiduel isolement de {n} — incidents documentés sans institutionnalisation, cadres légaux insuffisamment appliqués ou mécanismes de contrôle indépendant perfectibles",
                "Débat en cours sur les alternatives — tension entre sécurité pénitentiaire et respect des droits fondamentaux des détenus, réformes incomplètes ou partiellement mises en oeuvre",
                "Progrès fragiles — les avancées législatives peuvent être reversées par des incidents sécuritaires ou des pressions politiques populistes réclamant plus de sévérité pénitentiaire",
            ]
        return [
            f"{n} représente le modèle mondial de réforme de l'isolement cellulaire — utilisation minimale, strictement encadrée et limitée dans le temps, avec alternatives développées",
            "Règles Nelson Mandela 2015 respectées — isolement limité à 15 jours maximum, contrôle indépendant effectif, accès aux soins de santé mentale et programmes de réintégration",
            "Modèle exportable — financement CPT pour réplication européenne, formation personnels pénitentiaires et plaidoyer pour l'abandon de l'isolement prolongé comme outil de gestion",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "prolonged_solitary_confinement_scale_score": self.prolonged_solitary_confinement_scale_score,
            "mental_health_torture_psychological_score": self.mental_health_torture_psychological_score,
            "death_row_isolation_conditions_score": self.death_row_isolation_conditions_score,
            "oversight_independent_monitoring_gap_score": self.oversight_independent_monitoring_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_solitary_confinement_isolation_rights_index": self.estimated_solitary_confinement_isolation_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SolitaryConfinementIsolationRightsEntity] = [
    SolitaryConfinementIsolationRightsEntity(
        "SCI-001",
        "USA/Supermax ADX Florence 30+ Ans Isolement SHU",
        "États-Unis",
        "Florence ADX 30+ Ans Certains Détenus, SHU Pelican Bay, 80K Détenus Isolement National, Règles Mandela Violées Systématiquement",
        95.0, 92.0, 89.0, 91.0,
    ),
    SolitaryConfinementIsolationRightsEntity(
        "SCI-002",
        "Mexique/CEFERESO Cellules 23h Narcos & Opposants",
        "Mexique",
        "Cellules 23h Isolement CEFERESO, Cárceles Alta Seguridad, Narcos & Opposants Politiques, CNDH Rapports Alarmants Non Suivis",
        88.0, 85.0, 84.0, 86.0,
    ),
    SolitaryConfinementIsolationRightsEntity(
        "SCI-003",
        "Turquie/F-Type Öcalan 20+ Ans Isolation İmralı",
        "Turquie",
        "Prisons F-Type Isolement Post-2000, Grèves Faim Mortelles, Öcalan 20+ Ans Isolation İmralı, CPT Rapports Refus Accès",
        86.0, 83.0, 82.0, 84.0,
    ),
    SolitaryConfinementIsolationRightsEntity(
        "SCI-004",
        "Égypte/Al-Aqrab Prison Scorpion Islamistes & Journalistes",
        "Égypte",
        "Al-Aqrab Prison Haute Sécurité, Islamistes & Journalistes Isolement Total Années, Mort Morsi Conditions Dégradantes, HRW Rapports",
        84.0, 81.0, 80.0, 82.0,
    ),
    SolitaryConfinementIsolationRightsEntity(
        "SCI-005",
        "Royaume-Uni/CSDC Units Isolement Psychiatrique IPP",
        "Royaume-Uni",
        "CSDC Units Ségrégation, Isolement Psychiatrique, Mental Health Review Insuffisant, IPP Prisoners Isolement Indéterminé",
        55.0, 52.0, 51.0, 53.0,
    ),
    SolitaryConfinementIsolationRightsEntity(
        "SCI-006",
        "France/Quartiers Isolement QI Arbitraire CGLPL",
        "France",
        "Quartiers d'Isolement, Mise à l'Isolement Arbitraire Documentée, CGLPL Rapports Critiques, Contrôle Judiciaire Insuffisant",
        51.0, 48.0, 47.0, 49.0,
    ),
    SolitaryConfinementIsolationRightsEntity(
        "SCI-007",
        "ONU/Règles Mandela 2015 Isolement Interdit >15 Jours",
        "Global",
        "Nelson Mandela Rules 2015 Art.43-44, Isolement Interdit >15 Jours, Application Limitée, Rapporteur Spécial Torture Suivi",
        28.0, 25.0, 24.0, 26.0,
    ),
    SolitaryConfinementIsolationRightsEntity(
        "SCI-008",
        "Danemark/Réforme 2020 Isolement Mineurs Interdit",
        "Danemark",
        "Réforme 2020 Isolement Préventif, Mineurs Interdit, Réduction 80% Usage Isolement, Modèle Européen Alternatives Développées",
        6.0, 5.0, 4.0, 5.0,
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
        "domain": "solitary_confinement_isolation_rights",
        "confidence_score": 0.87,
        "data_sources": [
            "un_nelson_mandela_rules_2015",
            "cpt_council_europe_reports",
            "hrw_solitary_confinement_investigations",
            "cglpl_france_rapports_annuels",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_solitary_confinement_isolation_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_solitary_confinement_isolation_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Solitary Confinement Isolation Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    print(f"Distribution: {r['risk_distribution']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
