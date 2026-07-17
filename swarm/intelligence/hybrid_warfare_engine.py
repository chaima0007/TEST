"""
Caelum Partners — Hybrid Warfare Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La guerre hybride : l'art de faire la guerre sans la déclarer.
Les États autoritaires ont développé une doctrine de conflit qui exploite
les zones grises entre la paix et la guerre conventionnelle — combinant
désinformation, cyberattaques, sabotage d'infrastructures, milices mandataires
et manipulation juridique pour déstabiliser les adversaires sans franchir
le seuil de la réponse militaire collective.

La Russie a systématisé la doctrine Gerasimov : ingérence électorale (USA
2016, France 2017, Allemagne 2021), sabotage de gazoducs (Nord Stream),
poisonnements (Skripal), cyberattaques NotPetya (10Md$ de dégâts mondiaux),
et proxies en Syrie, en Ukraine, au Mali et en Libye. La Chine orchestre
des campagnes d'influence cognitives à travers TikTok, WeChat et les médias
diasporiques, des vols de propriété intellectuelle via APT10/APT41, et des
milices maritimes pour les disputes en mer de Chine. L'Iran coordonne
le Hezbollah (Liban), les Houthis (Yémen), les milices irakiennes et les
Gardiens de la Révolution (IRGC) comme réseau proxy régional.

La Corée du Nord finance son programme nucléaire via des cyberattaques bancaires
(1.2Md$ volé en 2023 selon l'ONU) et des groupes comme Lazarus qui ciblent
les cryptomonnaies, les banques et les infrastructures critiques mondiales.

Risk levels (guerre hybride et menaces multi-domaines) :
  critique  → composite ≥ 60  (guerre hybride intégrée — attaques systémiques multi-domaines)
  élevé     → composite ≥ 40  (opérations cognitives offensives — campagnes actives de déstabilisation)
  modéré    → composite ≥ 20  (vulnérabilité hybride — exposition partielle sans contre-mesures)
  faible    → composite < 20  (résilience hybride — défenses solides et dissuasion efficace)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "guerre_hybride_integree": {
        "severity_fr": "Critique",
        "action_fr": "Doctrine de contre-hybride intégré — réponse coordonnée cyber+info+diplomatique et renforcement de la résilience sociétale",
        "signal_fr": "information_warfare_score > 85 AND cyber_sabotage_score > 85 — guerre hybride intégrée systémique avérée",
    },
    "sabotage_cyber_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Hardening des infrastructures critiques et attribution publique des cyberattaques d'État avec sanctions ciblées",
        "signal_fr": "Sabotage cyber systémique — attaques coordonnées contre infrastructures critiques, réseaux électoraux et systèmes bancaires",
    },
    "guerre_par_procuration": {
        "severity_fr": "Critique",
        "action_fr": "Désignation des groupes proxy comme organisations terroristes et sanctions contre les États commanditaires de milices déstabilisatrices",
        "signal_fr": "Guerre par procuration — réseau de milices, mercenaires et mandataires coordonnés pour déstabiliser sans engagement direct",
    },
    "operations_cognitives_offensives": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcer la résilience informationnelle — éducation aux médias, transparence algorithmique et coordination internationale anti-désinformation",
        "signal_fr": "Opérations cognitives offensives — campagnes de désinformation, manipulation narrative et ingérence dans les espaces informationnels",
    },
    "resilience_democratique": {
        "severity_fr": "Faible",
        "action_fr": "Partager les modèles de résilience hybride et renforcer la coopération OTAN/UE sur la contre-hybride et la sécurité informationnelle",
        "signal_fr": "composite_score < 20 — résilience hybride solide — défenses multi-domaines et dissuasion efficace contre les menaces hybrides",
    },
}


@dataclass
class HybridWarfareEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    information_warfare_score: float
    cyber_sabotage_score: float
    proxy_warfare_score: float
    legal_warfare_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_hybrid_warfare_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.information_warfare_score * 0.30
            + self.cyber_sabotage_score * 0.25
            + self.proxy_warfare_score * 0.25
            + self.legal_warfare_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_hybrid_warfare_index = round(self.composite_score / 100 * 10, 2)

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
        if self.information_warfare_score >= 85 and self.cyber_sabotage_score >= 85:
            return "guerre_hybride_integree"
        if self.cyber_sabotage_score >= 85:
            return "sabotage_cyber_systemique"
        if self.proxy_warfare_score >= 85:
            return "guerre_par_procuration"
        if self.composite_score >= 20:
            return "operations_cognitives_offensives"
        return "resilience_democratique"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Guerre hybride systémique de {n} — opérations multi-domaines coordonnées contre adversaires sans déclaration de guerre formelle",
                "Doctrine de la zone grise — exploitation des seuils légaux et militaires pour éviter la réponse collective de l'OTAN/ONU",
                "Déni plausible institutionnalisé — proxies, mercenaires et hackers sans uniforme permettant la dénégation étatique",
            ]
        if self.risk_level == "élevé":
            return [
                f"Opérations cognitives offensives de {n} — campagnes actives de désinformation et manipulation narrative ciblées",
                "Influence sur les élections et le débat public — bots, fermes à trolls et médias pro-régime dans les pays cibles",
                "Exploitation des fractures sociales — amplification des divisions identitaires et politiques pour déstabiliser les sociétés",
            ]
        if self.risk_level == "modéré":
            return [
                f"Vulnérabilité hybride de {n} — exposition aux opérations d'influence sans contre-mesures systémiques",
                "Déficit de résilience informationnelle — sociétés polarisées vulnérables aux narratifs adversaires",
                "Lacunes de coordination défensive — absence de doctrine nationale cohérente de contre-hybride",
            ]
        return [
            f"{n} maintient une résilience hybride exemplaire — défenses multi-domaines et dissuasion intégrée efficaces",
            "Éducation aux médias et résilience informationnelle — populations formées à identifier la désinformation étrangère",
            "Modèle de contre-hybride à partager — coopération intelligence+cyber+info dans un cadre démocratique",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "information_warfare_score": self.information_warfare_score,
            "cyber_sabotage_score": self.cyber_sabotage_score,
            "proxy_warfare_score": self.proxy_warfare_score,
            "legal_warfare_score": self.legal_warfare_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_hybrid_warfare_index": self.estimated_hybrid_warfare_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[HybridWarfareEntity] = [
    HybridWarfareEntity("HW-001", "Russie — Doctrine Gerasimov & Opérations GRU", "Europe de l'Est", "NotPetya 10Md$, Skripal, Nord Stream & Proxies Wagner/Syrie/Ukraine/Mali", 92.0, 88.0, 90.0, 75.0),
    HybridWarfareEntity("HW-002", "Chine — APT41, TikTok & Milices Maritimes", "Asie", "APT10/APT41, Ingérence TikTok/WeChat & Milice Maritime Mer de Chine du Sud", 88.0, 90.0, 72.0, 85.0),
    HybridWarfareEntity("HW-003", "Iran — IRGC, Hezbollah & Proxies Régionaux", "MENA", "IRGC + Hezbollah + Houthis + Milices Irakiennes — Réseau Proxy Régional Intégré", 80.0, 75.0, 88.0, 65.0),
    HybridWarfareEntity("HW-004", "Corée du Nord — Lazarus & Cyberfinancement Nucléaire", "Asie", "Groupe Lazarus, 1.2Md$ Cryptos Volés & Cyberattaques Bancaires SWIFT pour Nucléaire", 75.0, 88.0, 68.0, 58.0),
    HybridWarfareEntity("HW-005", "Turquie — Opérations Cognitives & Diasporas", "MENA/Europe", "Trolls AKP, DITIB Diaspora & Opérations Info Syrie/Libye/Azerbaïdjan", 58.0, 52.0, 62.0, 45.0),
    HybridWarfareEntity("HW-006", "Inde/Pakistan — Guerre Hybride Sous-Continentale", "Asie du Sud", "ISI Proxies Cachemire, RAW Contre-Opérations & Cyberguerre Indo-Pak Permanente", 52.0, 48.0, 58.0, 42.0),
    HybridWarfareEntity("HW-007", "UE — Fragmentation Contre-Hybride Nationale", "Europe", "IA Act sans Volet Hybride, Positions OTAN Divisées & Insuffisance Résilience Info", 28.0, 32.0, 22.0, 30.0),
    HybridWarfareEntity("HW-008", "Estonie & Finlande — Résilience Hybride Intégrée", "Europe du Nord", "StratCom COE, X-Road Cyber Résilience & Education Médias Anti-Désinformation", 5.0, 8.0, 4.0, 6.0),
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
        "domain": "hybrid_warfare",
        "confidence_score": 0.83,
        "data_sources": ["hybrid_coe_helsinki_monitor", "bellingcat_hybrid_warfare_tracker", "icds_tallinn_strategic_review"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_hybrid_warfare_index": round(avg / 100 * 10, 2),
    }


def analyze_hybrid_warfare() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Hybrid Warfare Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
