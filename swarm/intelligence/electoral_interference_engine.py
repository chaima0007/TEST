"""
Caelum Partners — Electoral Interference Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'ingérence électorale : la démocratie comme cible de la guerre hybride.
Les États autoritaires ont identifié les processus électoraux démocratiques
comme leur principale vulnérabilité à exploiter — et paradoxalement, comme
leur principal vecteur de déstabilisation des adversaires. Corrompre une
élection n'exige pas de tanks : un algorithme bien conçu, quelques milliers
de faux profils et des fuites de données ciblées suffisent à créer le doute,
amplifier la polarisation et éroder la confiance dans les institutions.

La Russie (GRU/SVR/FSB) a interféré dans l'élection américaine de 2016
(Opération Active Measures, Fancy Bear, DC Leaks), la présidentielle française
2017 (MacronLeaks), le Brexit (financements opaques, bots pro-Leave), les
législatives allemandes 2021, et maintenant systématiquement via RT/Sputnik,
les fermes à trolls de l'IRA (Internet Research Agency) et Telegram. La
Chine (APT41/APT10) cible les financements de campagne via des sociétés
écrans, infiltre les réseaux de partis politiques et inonde TikTok/WeChat
avec des contenus pro-Beijing dans les communautés diasporiques. L'Iran
cible spécifiquement les électeurs musulmans américains via des campagnes
d'email et des opérations de cyberharcèlement.

En Europe, le réseau Tenet de campagnes d'influence coordonnées a été
documenté dans 55 pays touchant 65 élections. NSO Group (Pegasus) a ciblé
des journalistes et opposants politiques dans 50+ pays pour le compte de
36 États clients selon CitizenLab. L'ingérence est devenue industrielle.

Risk levels (ingérence électorale étrangère et manipulation démocratique) :
  critique  → composite ≥ 60  (ingérence systémique — campagnes documentées affectant les processus démocratiques)
  élevé     → composite ≥ 40  (manipulation narrative électorale — opérations actives sans attribution formelle)
  modéré    → composite ≥ 20  (vulnérabilité électorale — exposition sans contre-mesures adéquates)
  faible    → composite < 20  (intégrité électorale — systèmes robustes et résilience démocratique)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "ingérence_systémique": {
        "severity_fr": "Critique",
        "action_fr": "Attribution publique des ingérences et sanctions ciblées — expulsion des agents d'influence et interdiction des plateformes complices",
        "signal_fr": "foreign_influence_operation_score > 85 AND disinformation_campaign_score > 85 — ingérence électorale systémique documentée",
    },
    "financement_occulte_campagnes": {
        "severity_fr": "Critique",
        "action_fr": "Transparence totale des financements politiques et interdiction des dons étrangers via des sociétés écrans — audit obligatoire des partis",
        "signal_fr": "Financement occulte de campagnes — infiltration des partis politiques via des sociétés écrans et des donateurs étrangers masqués",
    },
    "sabotage_infrastructure_electorale": {
        "severity_fr": "Critique",
        "action_fr": "Hardening des systèmes électoraux numériques — air gap, audit de code source et certification internationale des machines à voter",
        "signal_fr": "Sabotage infrastructure électorale — attaques cyber sur les registres électoraux, machines à voter et systèmes de dépouillement",
    },
    "manipulation_narrative_électorale": {
        "severity_fr": "Élevé",
        "action_fr": "Obligation de transparence algorithmique pour les plateformes et financement de la vérification des faits électoraux indépendante",
        "signal_fr": "Manipulation narrative électorale — campagnes de désinformation ciblant les candidats, les électeurs ou la légitimité du scrutin",
    },
    "intégrité_electorale": {
        "severity_fr": "Faible",
        "action_fr": "Partager les modèles d'intégrité électorale et soutenir les observateurs internationaux dans les processus électoraux vulnérables",
        "signal_fr": "composite_score < 20 — intégrité électorale préservée — systèmes robustes, transparence et résilience face aux ingérences étrangères",
    },
}


@dataclass
class ElectoralInterferenceEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    foreign_influence_operation_score: float
    disinformation_campaign_score: float
    campaign_finance_infiltration_score: float
    electoral_infrastructure_attack_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_electoral_interference_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.foreign_influence_operation_score * 0.30
            + self.disinformation_campaign_score * 0.25
            + self.campaign_finance_infiltration_score * 0.25
            + self.electoral_infrastructure_attack_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_electoral_interference_index = round(self.composite_score / 100 * 10, 2)

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
        if self.foreign_influence_operation_score >= 85 and self.disinformation_campaign_score >= 85:
            return "ingérence_systémique"
        if self.campaign_finance_infiltration_score >= 85:
            return "financement_occulte_campagnes"
        if self.electoral_infrastructure_attack_score >= 85:
            return "sabotage_infrastructure_electorale"
        if self.composite_score >= 20:
            return "manipulation_narrative_électorale"
        return "intégrité_electorale"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Ingérence électorale systémique de {n} — opérations coordonnées ciblant les processus démocratiques de multiples États",
                "Active Measures 2.0 — fermes à trolls, fuites de données et amplification algorithmique comme armes électorales industrielles",
                "Corruption de la souveraineté populaire — manipulation de l'opinion publique étrangère via la désinformation ciblée à grande échelle",
            ]
        if self.risk_level == "élevé":
            return [
                f"Manipulation narrative électorale par {n} — campagnes actives de désinformation sans attribution formelle établie",
                "Polarisation instrumentalisée — amplification des fractures sociales pour fragiliser la cohésion pré-électorale des sociétés cibles",
                "Écosystèmes informationnels corrompus — médias pro-régime, influenceurs rémunérés et campagnes coordonnées inautentiques",
            ]
        if self.risk_level == "modéré":
            return [
                f"Vulnérabilité électorale dans {n} — exposition aux ingérences étrangères sans contre-mesures systémiques adéquates",
                "Réglementation insuffisante — lacunes dans la transparence des financements politiques et la sécurité des systèmes électoraux",
                "Risque d'influence étrangère — plateformes non régulées permettant des campagnes d'influence sans obligation de traçabilité",
            ]
        return [
            f"{n} maintient une intégrité électorale exemplaire — systèmes robustes et résilience face aux ingérences étrangères",
            "Transparence des financements politiques — déclarations exhaustives et interdiction des dons étrangers appliquée",
            "Modèle d'intégrité à exporter — observateurs internationaux, vérification des faits et éducation civique institutionnalisés",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "foreign_influence_operation_score": self.foreign_influence_operation_score,
            "disinformation_campaign_score": self.disinformation_campaign_score,
            "campaign_finance_infiltration_score": self.campaign_finance_infiltration_score,
            "electoral_infrastructure_attack_score": self.electoral_infrastructure_attack_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_electoral_interference_index": self.estimated_electoral_interference_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[ElectoralInterferenceEntity] = [
    ElectoralInterferenceEntity("EI-001", "Russie — GRU/IRA & Active Measures Mondiales", "Europe de l'Est", "IRA Trolls, Fancy Bear USA 2016, MacronLeaks & RT/Sputnik 65+ Élections Ciblées", 92.0, 90.0, 82.0, 85.0),
    ElectoralInterferenceEntity("EI-002", "Chine — APT41 & Financement Partis Occulte", "Asie", "Sociétés Écrans Dons Partis, APT10 Réseaux Politiques & TikTok Ingérence Diaspora", 85.0, 82.0, 88.0, 75.0),
    ElectoralInterferenceEntity("EI-003", "Iran — IRGC & Cyberciblage Électeurs Musulmans", "MENA", "Campagnes Email Électeurs Musulmans USA, Hack-and-Leak & Cyberharcèlement Opposants", 80.0, 78.0, 72.0, 85.0),
    ElectoralInterferenceEntity("EI-004", "EAU & Israël — NSO Pegasus & Surveillance Politique", "MENA", "Pegasus 50+ Pays, Ciblage Journalistes/Politiques & Dark PR Campagnes Influence", 75.0, 72.0, 88.0, 68.0),
    ElectoralInterferenceEntity("EI-005", "Turquie — AKP & Ingérence Diaspora Européenne", "MENA/Europe", "DITIB Mobilisation Électorale, Bots Turcs & Financement Partis Européens Pro-Erdoğan", 55.0, 58.0, 52.0, 48.0),
    ElectoralInterferenceEntity("EI-006", "Hongrie — Orbán & Réseau Anti-Démocrate Européen", "Europe", "Financement Partis Européens Via Fondations, RT Relay & Propaganda Souverainiste", 48.0, 52.0, 55.0, 42.0),
    ElectoralInterferenceEntity("EI-007", "UE — Fragmentation Réglementaire Anti-Ingérence", "Europe", "Digital Services Act Insuffisant, Positions Nationales Divisées & Absence FARA Européen", 30.0, 28.0, 25.0, 22.0),
    ElectoralInterferenceEntity("EI-008", "Islande & Canada — Intégrité Électorale Modèle", "Global", "CRTC Régulation, Loi Élections Canada & Islande Résilience Info Modèle Mondial", 5.0, 4.0, 6.0, 3.0),
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
        "confidence_score": 0.85,
        "data_sources": ["freedom_house_election_integrity", "atlantic_council_dfrlab_election_watch", "ndi_democracy_interference_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_electoral_interference_index": round(avg / 100 * 10, 2),
    }


def analyze_electoral_interference() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Electoral Interference Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
