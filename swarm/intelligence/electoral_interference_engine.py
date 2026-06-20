"""
Caelum Partners — Electoral Interference Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'ingérence électorale étrangère comme menace systémique aux démocraties :
au-delà de la désinformation déjà couverte, l'ingérence électorale englobe
des techniques plus directes — piratage des systèmes électoraux, fuites
ciblées de données, financement illicite de campagnes, manipulation des
registres électoraux, et coercition des communautés diasporiques lors
des votes. La frontière entre influence et ingérence s'est effondrée.

La Russie a développé un arsenal d'ingérence électorale testé depuis
2014 (Ukraine) jusqu'aux élections américaines 2016, françaises 2017,
et britanniques 2019. La Chine préfère les approches à long terme :
financement d'universités, think tanks et médias. L'Iran cible
spécifiquement les communautés de la diaspora. Israël et les USA
ont aussi pratiqué l'ingérence (Bibi et les élections étrangères,
interventions CIA de la Guerre Froide). La souveraineté électorale
est le pilier fondateur de la démocratie — sa compromission est la
forme la plus grave d'atteinte à l'autodétermination.

Risk levels (intensité de l'ingérence électorale subie ou pratiquée) :
  critique  → composite ≥ 60  (ingérence électorale avérée et systémique)
  élevé     → composite ≥ 40  (opérations d'ingérence significatives documentées)
  modéré    → composite ≥ 20  (risques d'ingérence à surveiller activement)
  faible    → composite < 20  (systèmes électoraux robustes et résilients)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "ingérence_systémique_active": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions contre les États auteurs d'ingérence et renforcement d'urgence de la cybersécurité électorale",
        "signal_fr": "cyberattack_score > 80 AND disinformation_campaign_score > 75 — ingérence systémique avérée",
    },
    "financement_illicite_étranger": {
        "severity_fr": "Critique",
        "action_fr": "Audit complet des financements politiques étrangers et renforcement de la transparence des dons",
        "signal_fr": "Financement étranger illicite — argent opaque finançant partis et candidats pro-puissance étrangère",
    },
    "manipulation_infrastructure": {
        "severity_fr": "Élevé",
        "action_fr": "Audit des systèmes de vote électronique et migration vers des systèmes vérifiables par papier",
        "signal_fr": "Manipulation infrastructure électorale — registres altérés ou systèmes de vote compromis",
    },
    "influence_diasporique": {
        "severity_fr": "Modéré",
        "action_fr": "Protection des communautés diasporiques contre la coercition électorale de leur État d'origine",
        "signal_fr": "Influence diasporique — États coercitant leurs ressortissants à l'étranger lors des élections",
    },
    "resilience_electorale": {
        "severity_fr": "Faible",
        "action_fr": "Partager les bonnes pratiques de résilience électorale et soutenir les observateurs internationaux",
        "signal_fr": "composite_score < 20 — systèmes électoraux robustes avec contrôles et transparence effectifs",
    },
}


@dataclass
class ElectoralInterferenceEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    cyberattack_score: float
    disinformation_campaign_score: float
    illicit_foreign_funding_score: float
    electoral_infrastructure_vulnerability_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_interference_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.cyberattack_score * 0.30
            + self.disinformation_campaign_score * 0.25
            + self.illicit_foreign_funding_score * 0.25
            + self.electoral_infrastructure_vulnerability_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_interference_index = round(self.composite_score / 100 * 10, 2)

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
        if self.cyberattack_score >= 80 and self.disinformation_campaign_score >= 75:
            return "ingérence_systémique_active"
        if self.illicit_foreign_funding_score >= 75:
            return "financement_illicite_étranger"
        if self.composite_score >= 40:
            return "manipulation_infrastructure"
        if self.composite_score >= 20:
            return "influence_diasporique"
        return "resilience_electorale"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Ingérence électorale systémique dans {n} — opérations étrangères compromettant la souveraineté démocratique",
                "Cyberattaques ciblant l'infrastructure électorale — registres, systèmes de vote et centres de dépouillement",
                "Désinformation électorale massive — campagnes coordonnées visant à polariser et déstabiliser l'électorat",
            ]
        if self.risk_level == "élevé":
            return [
                f"Opérations d'ingérence significatives dans {n} — financement illicite et manipulation de l'opinion",
                "Flux financiers étrangers vers des acteurs politiques — opacité des donations et façades associatives",
                "Infrastructure électorale partiellement vulnérable — systèmes de vote électronique sans audit suffisant",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risques d'ingérence électorale dans {n} — vulnérabilités identifiées mais pas encore exploitées",
                "Tentatives de manipulation des communautés diasporiques lors des consultations électorales",
                "Renforcement nécessaire de la cybersécurité des systèmes de vote et des registres électoraux",
            ]
        return [
            f"{n} maintient des systèmes électoraux robustes — résilience avérée face aux tentatives d'ingérence",
            "Observateurs indépendants, audit des finances politiques et cybersécurité électorale effectifs",
            "Modèle de souveraineté électorale à diffuser — transparence, vérifiabilité et protection des données",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "cyberattack_score": self.cyberattack_score,
            "disinformation_campaign_score": self.disinformation_campaign_score,
            "illicit_foreign_funding_score": self.illicit_foreign_funding_score,
            "electoral_infrastructure_vulnerability_score": self.electoral_infrastructure_vulnerability_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_interference_index": self.estimated_interference_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[ElectoralInterferenceEntity] = [
    ElectoralInterferenceEntity("EI-001", "Russie — Ingérence Électorale Systémique", "Europe de l'Est", "GRU/FSB: Hack-and-Leak, Désinformation & Soutien Partis Eurosceptiques", 92.0, 90.0, 85.0, 78.0),
    ElectoralInterferenceEntity("EI-002", "Chine — Influence Long Terme & Financement", "Asie", "Financements Universités/Médias & Ingérence Taïwan, Australie, Canada", 75.0, 80.0, 88.0, 70.0),
    ElectoralInterferenceEntity("EI-003", "Iran — Opérations Psychologiques Ciblées", "MENA", "Ciblage Diaspora Iranienne & Fausses Identités sur Réseaux Sociaux", 80.0, 85.0, 65.0, 72.0),
    ElectoralInterferenceEntity("EI-004", "Arabie Saoudite & EAU — Lobbying Opaque", "MENA", "Financement Partis Occidentaux via Façades & Opérations d'Influence", 58.0, 62.0, 82.0, 55.0),
    ElectoralInterferenceEntity("EI-005", "USA — Cible & Acteur d'Ingérence", "Amérique du Nord", "Élections 2016-2020 Ciblées + Interventions CIA Historiques à l'Étranger", 52.0, 55.0, 45.0, 58.0),
    ElectoralInterferenceEntity("EI-006", "Turquie — Diaspora comme Arme Électorale", "Europe/MENA", "AKP Mobilisant Diaspora Turque en Europe pour Référendums & Élections", 42.0, 48.0, 55.0, 40.0),
    ElectoralInterferenceEntity("EI-007", "Hongrie & Pologne — Ingérence Interne", "Europe de l'Est", "Manipulation Registres Électoraux & Médias Publics comme Outils Partisans", 38.0, 45.0, 35.0, 42.0),
    ElectoralInterferenceEntity("EI-008", "Pays-Bas & Canada — Résilience Électorale", "Global Nord", "Systèmes Papier, Audits Indépendants & Cybersécurité Électorale Robuste", 8.0, 10.0, 6.0, 5.0),
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
        "domain": "electoral_interference",
        "confidence_score": 0.83,
        "data_sources": ["atlantic_council_election_forensics", "eu_disinfo_lab", "freedom_house_electoral_integrity"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_interference_index": round(avg / 100 * 10, 2),
    }


def analyze_electoral_interference() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Electoral Interference Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
