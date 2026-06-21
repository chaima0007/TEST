"""
Caelum Partners — Freedom of Assembly & Protest Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Liberté de réunion pacifique et droit de manifester face à la répression étatique.
La liberté de réunion et le droit de manifester constituent le fondement de toute
démocratie vivante. Consacrés à l'article 20 de la Déclaration Universelle des Droits
de l'Homme et à l'article 21 du PIDCP, ces droits sont systématiquement bafoués par
les régimes autoritaires et de plus en plus restreints dans certaines démocraties.

Le Belarus a arrêté plus de 35 000 personnes lors des manifestations post-électorales
de 2020-2021, torturant systématiquement les manifestants dans des centres de détention
comme Akrescina. La junte birmane a tué plus de 3 000 manifestants depuis le coup d'État
de 2021 et interdit tous les syndicats indépendants. À Hong Kong, la Loi sur la Sécurité
Nationale de 2020 a criminalisé toute assemblée critiquant Pékin, et 47 militants pro-
démocratie ont été condamnés sous l'Article 23. En Égypte, la loi 107 de 2013 sur les
rassemblements soumet toute manifestation à l'autorisation préalable de la police.

En Europe et aux États-Unis, de nouvelles législations restreignent progressivement
le droit de manifester : Loi Sécurité Globale en France, Police, Crime, Sentencing and
Courts Act au Royaume-Uni, et plus de 34 États américains ont adopté des lois anti-BLM.

Risk levels (liberté de réunion et droit de manifester) :
  critique  → composite ≥ 60  (répression systémique — massacres, arrestations massives et criminalisation totale)
  élevé     → composite ≥ 40  (restrictions graves — lois anti-manifestation et usage disproportionné de la force)
  modéré    → composite ≥ 20  (dérive sécuritaire — surveillance accrue et restrictions croissantes)
  faible    → composite < 20  (protection du droit — cadre légal solide et supervision indépendante)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "repression_violente_manifestants": {
        "severity_fr": "Critique",
        "action_fr": "Tribunal pénal international — poursuites pour crimes contre l'humanité des dirigeants responsables de massacres de manifestants et sanctions ciblées",
        "signal_fr": "protest_violent_repression_score > 85 AND protest_leader_arrest_score > 85 — répression violente massive avec arrestations de masse et torture documentée",
    },
    "criminalisation_totale_assemblee": {
        "severity_fr": "Critique",
        "action_fr": "Abrogation des lois d'exception — pression internationale pour l'abrogation des lois de sécurité nationale criminalisant l'assemblée pacifique",
        "signal_fr": "assembly_ban_score > 85 — criminalisation totale de l'assemblée pacifique via lois sécuritaires et état d'urgence permanent",
    },
    "persecution_leaders_protestataires": {
        "severity_fr": "Critique",
        "action_fr": "Protection défenseurs des droits — visas d'urgence pour leaders protestataires persécutés et mécanismes de protection internationale",
        "signal_fr": "protest_leader_arrest_score > 80 — persécution systématique des leaders protestataires par arrestation, exil forcé et poursuites judiciaires",
    },
    "legislation_anti_manifestation": {
        "severity_fr": "Élevé",
        "action_fr": "Réforme législative — révision constitutionnelle et conventionnelle des lois anti-manifestation incompatibles avec l'article 11 CEDH et l'article 21 PIDCP",
        "signal_fr": "Législation anti-manifestation — nouvelles lois restreignant le droit de manifester, criminalisant les blocages et permettant des dispersions préventives",
    },
    "protection_droit_assemblee": {
        "severity_fr": "Faible",
        "action_fr": "Modèle à diffuser — promouvoir les standards de protection du droit de manifester via les mécanismes du Conseil des droits de l'homme de l'ONU",
        "signal_fr": "composite_score < 20 — protection exemplaire du droit de manifester — cadre légal solide et supervision indépendante effective",
    },
}


@dataclass
class FreedomOfAssemblyProtestRightsEntity:
    entity_id: str
    name: str
    country: str
    protest_violent_repression_severity_score: float
    assembly_ban_criminalization_scale_score: float
    protest_leader_arrest_persecution_score: float
    counter_terrorism_law_assembly_misuse_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_freedom_of_assembly_protest_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.protest_violent_repression_severity_score * 0.30
            + self.assembly_ban_criminalization_scale_score * 0.25
            + self.protest_leader_arrest_persecution_score * 0.25
            + self.counter_terrorism_law_assembly_misuse_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_freedom_of_assembly_protest_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.protest_violent_repression_severity_score >= 85 and self.protest_leader_arrest_persecution_score >= 85:
            return "repression_violente_manifestants"
        if self.assembly_ban_criminalization_scale_score >= 85:
            return "criminalisation_totale_assemblee"
        if self.protest_leader_arrest_persecution_score >= 80:
            return "persecution_leaders_protestataires"
        if self.composite_score >= 20:
            return "legislation_anti_manifestation"
        return "protection_droit_assemblee"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Répression systémique par {n} — massacres, arrestations de masse et torture documentée des manifestants pacifiques",
                "Criminalisation totale de l'opposition — lois d'exception transformant toute assemblée critique en crime passible de prison",
                "Exil forcé des leaders — persécution judiciaire et physique forçant les dirigeants protestataires à fuir le pays",
            ]
        if self.risk_level == "élevé":
            return [
                f"Restrictions graves imposées par {n} — législation anti-manifestation et usage disproportionné de la force par les forces de l'ordre",
                "Lois antiterroristes détournées — utilisation des lois de sécurité nationale pour criminaliser les mouvements sociaux légitimes",
                "Poursuites RICO contre manifestants — instrumentalisation du droit pénal pour décourager la participation aux mobilisations",
            ]
        if self.risk_level == "modéré":
            return [
                f"Monitoring et plaidoyer par {n} — documentation des violations et lobbying pour des réformes législatives protectrices",
                "Espace civique sous pression — organisations de la société civile documentant le rétrécissement des libertés d'assemblée",
                "Standards internationaux — promotion des lignes directrices ONU sur le maintien de l'ordre lors des manifestations",
            ]
        return [
            f"{n} protège le droit de manifester — cadre normatif universel consacrant la liberté de réunion pacifique",
            "Article 20 DUDH et Article 21 PIDCP — fondements juridiques internationaux de la liberté de réunion et d'association",
            "Rapporteur Spécial ONU — mécanisme de responsabilité internationale pour les violations du droit de manifester",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "composite_score": self.composite_score,
            "protest_violent_repression_severity_score": self.protest_violent_repression_severity_score,
            "assembly_ban_criminalization_scale_score": self.assembly_ban_criminalization_scale_score,
            "protest_leader_arrest_persecution_score": self.protest_leader_arrest_persecution_score,
            "counter_terrorism_law_assembly_misuse_gap_score": self.counter_terrorism_law_assembly_misuse_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_freedom_of_assembly_protest_rights_index": self.estimated_freedom_of_assembly_protest_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[FreedomOfAssemblyProtestRightsEntity] = [
    FreedomOfAssemblyProtestRightsEntity(
        "FAP-001",
        "Belarus/Loukachenko — 35 000 Arrestations Post-2020, Manifestants Torturés, Dirigeants Exilés & Lois Anti-Extrémisme",
        "Belarus",
        96.0, 90.0, 92.0, 90.0,
    ),
    FreedomOfAssemblyProtestRightsEntity(
        "FAP-002",
        "Myanmar/Junta — Manifestants Tués 3 000+, Syndicats Bannis, Couvre-Feu Permanent & Internet Coupé",
        "Myanmar",
        95.0, 88.0, 85.0, 88.0,
    ),
    FreedomOfAssemblyProtestRightsEntity(
        "FAP-003",
        "Chine/HK — NSL Hong Kong Manifestants, Article 23 Assemblées Illégales, Dirigeants 47 Condamnés & Tiananmen Commémoration Interdite",
        "Chine/Hong Kong",
        82.0, 92.0, 88.0, 85.0,
    ),
    FreedomOfAssemblyProtestRightsEntity(
        "FAP-004",
        "Égypte/Sissi — Loi 107/2013 Rassemblements, 60 000 Prisonniers Politiques, Sit-In Rabaa 2013 Massacre & ONG Étrangères Interdites",
        "Égypte",
        88.0, 82.0, 80.0, 82.0,
    ),
    FreedomOfAssemblyProtestRightsEntity(
        "FAP-005",
        "France/UK — Loi Sécurité Globale, Anti-Protest Policing Powers UK, BRAV-M Violences & Extinction Rebellion Interdit",
        "France/Royaume-Uni",
        52.0, 58.0, 50.0, 55.0,
    ),
    FreedomOfAssemblyProtestRightsEntity(
        "FAP-006",
        "USA — Anti-BLM Laws 34 États, COINTELPRO Legacy, Poursuites RICO Manifestants & Stand Your Ground Contre Protestataires",
        "États-Unis",
        55.0, 52.0, 48.0, 50.0,
    ),
    FreedomOfAssemblyProtestRightsEntity(
        "FAP-007",
        "CIVICUS/FIDH — Monitor Espace Civique, Rapports Liberté Réunion, Défense Manifestants & Lobbying Nations Unies",
        "International",
        25.0, 26.0, 28.0, 24.0,
    ),
    FreedomOfAssemblyProtestRightsEntity(
        "FAP-008",
        "ONU/Art.20 DUDH — Liberté Réunion Pacifique, Rapporteur Spécial & SDG 16.7 Gouvernance Inclusive",
        "International",
        4.0, 3.0, 4.0, 5.0,
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
        "agent": "freedom_of_assembly_protest_rights_engine",
        "domain": "freedom_of_assembly_protest_rights",
        "total_entities": n,
        "avg_composite": avg,
        "confidence_score": 0.86,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "avg_estimated_freedom_of_assembly_protest_rights_index": round(avg / 100 * 10, 2),
        "data_sources": [
            "civicus_monitor_civic_space_annual_report",
            "amnesty_protest_repression_crackdown_documentation",
            "human_rights_watch_assembly_criminalization_report",
        ],
        "entities": [e.to_dict() for e in entities],
    }


def analyze_freedom_of_assembly_protest_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    import json
    r = summary()
    print(f"Freedom of Assembly & Protest Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    print(f"Distribution: {r['risk_distribution']}")
    print(f"avg_estimated_index: {r['avg_estimated_freedom_of_assembly_protest_rights_index']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name[:60]} → {e.risk_level} ({e.composite_score})")
