"""
Caelum Partners — Diaspora Geopolitics Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Les diasporas comme acteurs géopolitiques à part entière : les communautés
transnationales jouent un rôle croissant dans les conflits, les élections
et les politiques étrangères — tantôt comme vecteurs d'influence du pays
d'origine (soft power, financement de partis, renseignement), tantôt comme
forces de résistance contre des régimes oppresseurs.

La diaspora iranienne influence la politique des démocraties occidentales.
La diaspora chinoise est ciblée par des opérations d'influence de Pékin.
La diaspora russe est à la fois persécutée et instrumentalisée par Moscou.
Les diasporas africaines envoient plus d'argent à leur pays que l'aide
internationale combinée. Comprendre les dynamiques diasporiques, c'est
comprendre la politique étrangère du XXIe siècle.

Risk levels (intensité des dynamiques diasporiques géopolitiques) :
  critique  → composite ≥ 60  (instrumentalisation majeure de la diaspora)
  élevé     → composite ≥ 40  (tensions diasporiques géopolitiques sévères)
  modéré    → composite ≥ 20  (dynamiques diasporiques à surveiller)
  faible    → composite < 20  (diaspora intégrée et non-instrumentalisée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "instrumentalisation_etatique": {
        "severity_fr": "Critique",
        "action_fr": "Contre-mesures contre les opérations d'influence et protection des communautés diasporiques ciblées",
        "signal_fr": "state_coercion > 80 AND transnational_repression > 75 — instrumentalisation étatique totale",
    },
    "repression_transnationale": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions contre les États pratiquant la répression transnationale et asile politique renforcé",
        "signal_fr": "Répression transnationale — État ciblant ses propres citoyens à l'étranger via la diaspora",
    },
    "influence_geopolitique_active": {
        "severity_fr": "Élevé",
        "action_fr": "Contre-ingérence renforcée et transparence des financements politiques diasporiques",
        "signal_fr": "Influence géopolitique active — diaspora instrumentalisée dans les politiques des pays d'accueil",
    },
    "tensions_identitaires": {
        "severity_fr": "Modéré",
        "action_fr": "Politiques d'intégration renforcées et dialogue interculturel pour désamorcer les tensions",
        "signal_fr": "Tensions identitaires diasporiques — communautés entre fidélité au pays d'origine et intégration",
    },
    "diaspora_integree": {
        "severity_fr": "Faible",
        "action_fr": "Valorisation des diasporas comme ponts culturels et économiques entre pays d'origine et d'accueil",
        "signal_fr": "composite_score < 20 — diaspora intégrée, influence positive sans instrumentalisation géopolitique",
    },
}


@dataclass
class DiasporaGeopoliticsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    state_coercion_score: float
    transnational_repression_score: float
    political_influence_score: float
    diaspora_radicalization_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_diaspora_risk_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.state_coercion_score * 0.30
            + self.transnational_repression_score * 0.25
            + self.political_influence_score * 0.25
            + self.diaspora_radicalization_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_diaspora_risk_index = round(self.composite_score / 100 * 10, 2)

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
        if self.state_coercion_score >= 80 and self.transnational_repression_score >= 75:
            return "instrumentalisation_etatique"
        if self.transnational_repression_score >= 70:
            return "repression_transnationale"
        if self.composite_score >= 45:
            return "influence_geopolitique_active"
        if self.composite_score >= 25:
            return "tensions_identitaires"
        return "diaspora_integree"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Instrumentalisation étatique totale de la diaspora {n} — coercition et surveillance des citoyens à l'étranger",
                "Répression transnationale active — intimidation, menaces sur familles restées au pays et agents du régime",
                "Opérations d'influence dans les pays d'accueil — manipulation des communautés diasporiques à des fins géopolitiques",
            ]
        if self.risk_level == "élevé":
            return [
                f"Influence géopolitique active de la diaspora {n} — financement partis et lobbying dans pays d'accueil",
                "Tensions entre communautés diasporiques et gouvernements d'accueil — suspicion d'ingérence étrangère",
                "Surveillance diasporique par le pays d'origine — réseaux de renseignement dans les communautés expatriées",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tensions identitaires diasporiques pour {n} — communautés tiraillées entre fidélité et intégration",
                "Influence politique partielle — organisations diasporiques actives dans les débats du pays d'accueil",
                "Risques de radicalisation à surveiller — communautés isolées et en contact avec des réseaux extrémistes",
            ]
        return [
            f"Diaspora {n} intégrée et non-instrumentalisée — pont culturel et économique positif",
            "Transferts financiers au pays d'origine favorisant le développement sans ingérence politique",
            "Modèle d'intégration diasporique à valoriser — contribution positive aux deux pays",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "state_coercion_score": self.state_coercion_score,
            "transnational_repression_score": self.transnational_repression_score,
            "political_influence_score": self.political_influence_score,
            "diaspora_radicalization_score": self.diaspora_radicalization_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_diaspora_risk_index": self.estimated_diaspora_risk_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[DiasporaGeopoliticsEntity] = [
    DiasporaGeopoliticsEntity("DG-001", "Diaspora Chinoise — Opérations Pékin", "Global", "Overseas Police Stations & Influence CPC à l'Étranger", 92.0, 88.0, 85.0, 80.0),
    DiasporaGeopoliticsEntity("DG-002", "Diaspora Russe — Post-2022 Sous Pression", "Europe/Global", "FSB Ciblant Opposants Russes à l'Étranger", 85.0, 90.0, 72.0, 78.0),
    DiasporaGeopoliticsEntity("DG-003", "Diaspora Iranienne — Dualité Régime/Résistance", "Global", "Mollahs vs Diaspora Pro-Démocratie — Guerre Froide Transnationale", 80.0, 85.0, 78.0, 72.0),
    DiasporaGeopoliticsEntity("DG-004", "Diaspora Turque — AKP & Mosquées Politiques", "Europe", "DITIB comme Bras Politique d'Ankara dans les Diasporas", 72.0, 68.0, 80.0, 65.0),
    DiasporaGeopoliticsEntity("DG-005", "Diaspora Saoudienne & Golf — Influence Islamiste", "Global", "Financement Wahhabite des Communautés Musulmanes Diasporiques", 58.0, 52.0, 72.0, 60.0),
    DiasporaGeopoliticsEntity("DG-006", "Diaspora Indienne — Lobby NRI & Modi", "Global", "NRI Influence sur la Politique Étrangère Américaine et UK", 45.0, 35.0, 68.0, 42.0),
    DiasporaGeopoliticsEntity("DG-007", "Diaspora Africaine — Remittances & Influence", "Global", "Transferts Supérieurs à l'Aide Internationale — Soft Power", 25.0, 18.0, 38.0, 22.0),
    DiasporaGeopoliticsEntity("DG-008", "Diaspora Scandinave & Canadienne — Intégration", "Global", "Modèles d'Intégration Diasporique Exemplaires", 5.0, 4.0, 12.0, 6.0),
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
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "diaspora_geo",
        "confidence_score": 0.77,
        "data_sources": ["freedom_house_transnational_repression", "globsec_diaspora_monitor", "ifri_diaspora_geopolitics"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_diaspora_risk_index": round(avg / 100 * 10, 2),
    }


def analyze_diaspora_geopolitics() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Diaspora Geopolitics Engine — {r['total_entities']} diasporas, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
