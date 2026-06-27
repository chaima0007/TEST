"""
Caelum Partners — Lawfare Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Le lawfare : quand le droit devient une arme de guerre géopolitique.
Les États puissants ont découvert que le droit international peut être weaponisé
aussi efficacement que les missiles — sans déclencher de riposte armée. La
manipulation des tribunaux internationaux, l'extraterritorialité judiciaire
abusive, les pièges de traités d'investissement et les vetos au Conseil de
Sécurité constituent le nouveau visage du conflit interétatique.

Les USA exercent une compétence judiciaire universelle via le Foreign Corrupt
Practices Act (FCPA) condamnant des entreprises européennes et asiatiques pour
des actes commis hors du territoire américain (BNP Paribas 8.9Md$, Alstom
772M$, Airbus 3.9Md$). L'OFAC impose ses sanctions unilatéralement au monde
entier via la menace de couper les banques de SWIFT. La Russie bloque tout
mécanisme onusien via son veto au CSNU : 50+ résolutions vetoes depuis 2011.

La Chine a rejeté la sentence arbitrale de La Haye sur la Mer de Chine du
Sud (2016) et construit une architecture d'arbitrage alternative via ses
tribunaux d'investissement Belt and Road. Israël combat les procédures de la
CPI depuis les affaires Gaza. La guerre juridique est devenue un domaine de
confrontation aussi intense que le cyber ou l'espace.

Risk levels (lawfare et weaponisation du droit international) :
  critique  → composite ≥ 60  (lawfare systémique — instrumentalisation active du droit comme arme de puissance)
  élevé     → composite ≥ 40  (manœuvres juridiques offensives — procédures et traités utilisés à fins géopolitiques)
  modéré    → composite ≥ 20  (forum shopping — exploitation des gaps juridictionnels sans stratégie cohérente)
  faible    → composite < 20  (état de droit coopératif — respect et renforcement du droit international)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "lawfare_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Coalition anti-lawfare — réforme du CSNU, protocole de réponse coordonnée aux procédures abusives et renforcement des mécanismes de sanctions aux abus juridictionnels",
        "signal_fr": "international_court_manipulation_score > 85 AND sanctions_legal_weaponization_score > 85 — lawfare systémique combinant manipulation judiciaire et weaponisation des sanctions",
    },
    "extraterritorialite_hegemonique": {
        "severity_fr": "Critique",
        "action_fr": "Contre-mesures d'extraterritorialité — législations nationales bloquantes, recours OMC et coalition européenne anti-FCPA pour défendre la souveraineté judiciaire",
        "signal_fr": "extraterritoriality_abuse_score > 85 — extraterritorialité hégémonique: application du droit national aux acteurs étrangers comme outil de coercition",
    },
    "pieges_traites": {
        "severity_fr": "Critique",
        "action_fr": "Audit des traités ISDS — renégociation des accords BIT asymétriques et création d'une cour multilatérale d'investissement pour limiter les abus",
        "signal_fr": "treaty_weaponization_score > 85 — weaponisation des traités d'investissement comme mécanisme de capture des politiques publiques étrangères",
    },
    "manœuvres_juridiques_offensives": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des capacités juridiques nationales — formation aux litiges internationaux et construction d'alliances judiciaires défensives",
        "signal_fr": "Manœuvres juridiques offensives — utilisation active des procédures internationales à des fins géopolitiques sans qualification de lawfare systémique",
    },
    "etat_de_droit_cooperatif": {
        "severity_fr": "Faible",
        "action_fr": "Partager les modèles de coopération juridique — financement des institutions internationales et promotion du règlement pacifique des différends",
        "signal_fr": "composite_score < 20 — engagement sincère dans l'état de droit international et le règlement multilatéral des différends",
    },
}


@dataclass
class LawfareEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    international_court_manipulation_score: float
    sanctions_legal_weaponization_score: float
    extraterritoriality_abuse_score: float
    treaty_weaponization_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_lawfare_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.international_court_manipulation_score * 0.30
            + self.sanctions_legal_weaponization_score * 0.25
            + self.extraterritoriality_abuse_score * 0.25
            + self.treaty_weaponization_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_lawfare_index = round(self.composite_score / 100 * 10, 2)

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
        if self.international_court_manipulation_score >= 85 and self.sanctions_legal_weaponization_score >= 85:
            return "lawfare_systemique"
        if self.extraterritoriality_abuse_score >= 85:
            return "extraterritorialite_hegemonique"
        if self.treaty_weaponization_score >= 85:
            return "pieges_traites"
        if self.composite_score >= 20:
            return "manœuvres_juridiques_offensives"
        return "etat_de_droit_cooperatif"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Lawfare systémique de {n} — instrumentalisation active du droit international comme arme de pression géopolitique",
                "Weaponisation judiciaire — manipulation des cours internationales, extraterritorialité abusive et pièges de traités d'investissement",
                "Érosion de l'ordre juridique international — asymétrie délibérée entre puissants capables d'imposer leur droit et États soumis à ses effets",
            ]
        if self.risk_level == "élevé":
            return [
                f"Manœuvres juridiques offensives de {n} — utilisation des procédures internationales à fins géopolitiques",
                "Forum shopping agressif — sélection opportuniste des juridictions les plus favorables pour maximiser l'effet de pression",
                "Contre-droit comme stratégie — création de normes alternatives et contestation des mécanismes universels de règlement des différends",
            ]
        if self.risk_level == "modéré":
            return [
                f"Forum shopping de {n} — exploitation des lacunes juridictionnelles sans stratégie lawfare cohérente",
                "Fragmentation normative — multiplication des règles spéciales au détriment de la cohérence du droit international",
                "Déficit de capacités juridiques — exposition aux procédures adversaires faute de ressources contentieuses suffisantes",
            ]
        return [
            f"{n} incarne l'état de droit coopératif — contribution sincère aux institutions juridiques internationales et respect des décisions",
            "Règlement pacifique des différends — recours aux mécanismes de médiation, arbitrage et juridictions multilatérales de bonne foi",
            "Modèle de coopération juridique à diffuser — financement des cours internationales et formation au droit international pour les États vulnérables",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "international_court_manipulation_score": self.international_court_manipulation_score,
            "sanctions_legal_weaponization_score": self.sanctions_legal_weaponization_score,
            "extraterritoriality_abuse_score": self.extraterritoriality_abuse_score,
            "treaty_weaponization_score": self.treaty_weaponization_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_lawfare_index": self.estimated_lawfare_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[LawfareEntity] = [
    LawfareEntity("LW-001", "USA — FCPA, OFAC & Extraterritorialité Judiciaire Mondiale", "Amérique du Nord", "FCPA BNP 8.9Md$/Alstom 772M$/Airbus 3.9Md$, OFAC Mondial & Juridiction Universelle DOJ", 88.0, 82.0, 95.0, 85.0),
    LawfareEntity("LW-002", "Russie — Veto CSNU & Procédures CIJ Détournées", "Europe de l'Est", "50+ Vetos CSNU 2011-2024, CIJ Affaire Ukraine Blockage & Réclusions Arbitrales Sélectives", 90.0, 85.0, 78.0, 80.0),
    LawfareEntity("LW-003", "Chine — Rejet La Haye & Arbitrage BRI Alternatif", "Asie", "Rejet CPA 2016 Mer Chine Sud, Tribunaux BRI Alternatifs & ISDS Asymétrique Partenaires", 85.0, 80.0, 75.0, 88.0),
    LawfareEntity("LW-004", "Israël & Hamas — Guerre Juridique Gaza CIJ/CPI", "MENA", "Procédures CIJ Génocide Afrique du Sud, Mandat CPI Netanyahu & Contre-Lawfare Légitimité", 82.0, 78.0, 80.0, 72.0),
    LawfareEntity("LW-005", "Turquie & Hongrie — Vetos Juridiques OTAN/UE", "MENA/Europe", "Veto Adhésion Suède OTAN, Blocages Fonds UE Hongrois & Violation État de Droit Documentée", 58.0, 55.0, 48.0, 52.0),
    LawfareEntity("LW-006", "Qatar & EAU — Arbitrage ISDS & Lobbying Juridique", "MENA", "700+ Traités BIT, Arbitrages CIRDI Offensifs & Sports/Cultura Soft Power via Droit", 52.0, 48.0, 55.0, 58.0),
    LawfareEntity("LW-007", "UE — Forum Shopping & Fragmentation Normative", "Europe", "RGPD Extraterritorialité Limitée, DSA/DMA Régulation & Tensions Juridictions USA/UE Tech", 28.0, 32.0, 35.0, 25.0),
    LawfareEntity("LW-008", "CIJ & CPA — Gouvernance Juridique Internationale", "Global", "CIJ 15 Juges, CPA 157 États Parties & Cour Pénale Internationale 124 États Membres", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "lawfare",
        "confidence_score": 0.80,
        "data_sources": ["icc_international_criminal_court_monitor", "pcacases_arbitration_tracker", "us_doj_fcpa_resource_guide"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_lawfare_index": round(avg / 100 * 10, 2),
    }


def analyze_lawfare() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Lawfare Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
