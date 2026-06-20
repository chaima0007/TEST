"""
Caelum Partners — Sportwashing Geopolitics Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Le sportwashing : utiliser le sport mondial comme blanchiment géopolitique.
Des régimes autoritaires investissent des milliards dans le sport mondial
non pour la passion sportive, mais pour acheter une légitimité internationale,
détourner l'attention des violations des droits humains, et projeter une
image de modernité et de puissance sur la scène mondiale.

Le Qatar a dépensé 220 milliards de dollars pour la Coupe du Monde 2022 —
le plus grand investissement sportif de l'histoire. 6 500 travailleurs
migrants sont morts sur les chantiers selon The Guardian. L'Arabie Saoudite
a créé le LIV Golf (2022), acheté Newcastle United, sponsorisé la F1 (ARAMCO),
recruté Cristiano Ronaldo (75M€/an) et Karim Benzema — tout en exécutant
196 personnes en 2022. Les Émirats ont fait du PSG (Paris Saint-Germain)
un instrument de soft power qatari et d'Abu Dhabi City Football Group un
empire sportif mondial (Manchester City, Melbourne City, Mumbai City, NY
City FC...). La Chine a organisé deux JO (2008, 2022) pour se présenter
au monde comme grande puissance bienveillante — malgré le Tibet et Xinjiang.

Le sport est devenu l'équivalent du pétrole comme vecteur de légitimation
internationale : acheter des clubs, des droits de diffusion, des fédérations
et des athlètes, c'est acheter des narratifs et du silence.

Risk levels (sportwashing et instrumentalisation géopolitique du sport) :
  critique  → composite ≥ 60  (sportwashing systémique — blanchiment d'image à grande échelle)
  élevé     → composite ≥ 40  (manipulation sportive — instrumentalisation politisée du sport)
  modéré    → composite ≥ 20  (soft power sportif — projection d'image sans droits humains)
  faible    → composite < 20  (sport éthique — valeurs démocratiques et transparence)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "sportwashing_systematique": {
        "severity_fr": "Critique",
        "action_fr": "Conditionner l'attribution des droits sportifs au respect des droits humains et sanctions contre les organisateurs complices",
        "signal_fr": "sportwashing_investment_score > 85 AND sports_rights_acquisition_score > 85 — sportwashing systémique avéré",
    },
    "soft_power_sport_offensif": {
        "severity_fr": "Critique",
        "action_fr": "Régulation internationale des droits de diffusion sportifs et transparence des financements étatiques dans le sport mondial",
        "signal_fr": "Soft power sportif offensif — utilisation du sport comme vecteur de manipulation narrative et de légitimation autoritaire",
    },
    "manipulation_sportive": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcer l'intégrité sportive et les mécanismes de sanction contre les États manipulant les compétitions internationales",
        "signal_fr": "Manipulation sportive — dopage d'État, corruption des fédérations ou instrumentalisation politique des compétitions",
    },
    "puissance_douce_sportive": {
        "severity_fr": "Modéré",
        "action_fr": "Distinguer soft power sportif légitime et sportwashing — critères de transparence et de respect des droits pour les événements majeurs",
        "signal_fr": "Puissance douce sportive — utilisation du sport pour la projection culturelle sans violations graves documentées",
    },
    "sport_valeurs_democratiques": {
        "severity_fr": "Faible",
        "action_fr": "Soutenir et promouvoir les modèles sportifs fondés sur les valeurs démocratiques et l'intégrité compétitive",
        "signal_fr": "composite_score < 20 — sport éthique et transparent — modèle de gouvernance sportive respectueux des droits humains",
    },
}


@dataclass
class SportwashingGeopoliticsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    sportwashing_investment_score: float
    sports_rights_acquisition_score: float
    soft_power_narrative_score: float
    human_rights_whitewash_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_sport_geopolitics_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.sportwashing_investment_score * 0.30
            + self.sports_rights_acquisition_score * 0.25
            + self.soft_power_narrative_score * 0.25
            + self.human_rights_whitewash_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_sport_geopolitics_index = round(self.composite_score / 100 * 10, 2)

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
        if self.sportwashing_investment_score >= 85 and self.sports_rights_acquisition_score >= 85:
            return "sportwashing_systematique"
        if self.soft_power_narrative_score >= 80:
            return "soft_power_sport_offensif"
        if self.composite_score >= 40:
            return "manipulation_sportive"
        if self.composite_score >= 20:
            return "puissance_douce_sportive"
        return "sport_valeurs_democratiques"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Sportwashing systémique de {n} — investissements massifs dans le sport mondial pour blanchir l'image du régime",
                "Achats de légitimité sportive — clubs, droits de diffusion et événements utilisés pour contourner les critiques diplomatiques",
                "Silence sportif sur les droits humains — athlètes et institutions achetés ou intimidés pour éviter toute condamnation publique",
            ]
        if self.risk_level == "élevé":
            return [
                f"Manipulation sportive significative de {n} — instrumentalisation politisée des compétitions et des institutions sportives",
                "Dopage d'État ou corruption sportive — manipulation des règles compétitives pour des objectifs de prestige national",
                "Sport comme exutoire national — détournement de l'attention populaire des problèmes internes via la victoire sportive",
            ]
        if self.risk_level == "modéré":
            return [
                f"Soft power sportif de {n} — utilisation du sport comme vecteur de projection culturelle et d'influence mondiale",
                "Diplomatie sportive active — organisation d'événements et investissements dans les fédérations pour améliorer l'image",
                "Ambiguïté éthique — distinction floue entre soft power sportif légitime et sportwashing sans droits humains",
            ]
        return [
            f"{n} incarne un modèle de sport éthique — compétitions transparentes et gouvernance respectueuse des droits",
            "Sport comme vecteur de valeurs démocratiques — fair play, inclusion et intégrité compétitive institutionnalisés",
            "Modèle de gouvernance sportive à diffuser — résistance au sportwashing et conditionnalité droits humains dans l'attribution",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "sportwashing_investment_score": self.sportwashing_investment_score,
            "sports_rights_acquisition_score": self.sports_rights_acquisition_score,
            "soft_power_narrative_score": self.soft_power_narrative_score,
            "human_rights_whitewash_score": self.human_rights_whitewash_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_sport_geopolitics_index": self.estimated_sport_geopolitics_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SportwashingGeopoliticsEntity] = [
    SportwashingGeopoliticsEntity("SG-001", "Qatar — Coupe du Monde 2022 & PSG Soft Power", "MENA", "220Md$ CDM 2022, 6500 Morts Migrants & PSG comme Instrument d'Influence", 95.0, 90.0, 88.0, 92.0),
    SportwashingGeopoliticsEntity("SG-002", "Arabie Saoudite — LIV Golf, Newcastle & PIF Sport", "MENA", "LIV Golf, Newcastle United, F1 ARAMCO & Ronaldo 75M€/an malgré 196 Exécutions", 92.0, 95.0, 85.0, 90.0),
    SportwashingGeopoliticsEntity("SG-003", "Émirats Arabes — Manchester City & City Football Group", "MENA", "ADCB Manchester City, 12 Clubs Mondiaux & Formule 1 Abu Dhabi GP", 88.0, 92.0, 82.0, 85.0),
    SportwashingGeopoliticsEntity("SG-004", "Chine — JO Pékin 2008/2022 & Soft Power Global", "Asie", "2 JO pour Légitimer PCC, Achats Clubs Européens & Droits Diffusion Mondiaux", 80.0, 82.0, 85.0, 78.0),
    SportwashingGeopoliticsEntity("SG-005", "Russie — Dopage d'État & Manipulation CAS", "Europe de l'Est", "Programme Dopage McLaren, Exclusion Partielle & Corruption WADA/FIFA", 55.0, 60.0, 52.0, 65.0),
    SportwashingGeopoliticsEntity("SG-006", "Azerbaïdjan/Belarus — JO Bakou & Sports Autoritaires", "Caucase/Europe", "Bakou 2015 JO Européens & Belarus Sport Mobilisé pour Légitimer Loukachenko", 50.0, 48.0, 55.0, 60.0),
    SportwashingGeopoliticsEntity("SG-007", "USA — NBA/NFL Mondialisation Culturelle", "Amérique du Nord", "NBA Chine, FIFA World Cup 2026 & Soft Power Culturel par le Sport Global", 25.0, 30.0, 40.0, 20.0),
    SportwashingGeopoliticsEntity("SG-008", "Finlande & Nouvelle-Zélande — Sport Éthique", "Europe/Pacifique", "Politique Sport Transparente, Droits Humains dans Attribution & Gouvernance", 5.0, 4.0, 8.0, 3.0),
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
        "domain": "sport_geopolitics",
        "confidence_score": 0.86,
        "data_sources": ["amnesty_sport_washing_tracker", "play_the_game_integrity_monitor", "human_rights_watch_sport_political_use"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_sport_geopolitics_index": round(avg / 100 * 10, 2),
    }


def analyze_sportwashing_geopolitics() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Sportwashing Geopolitics Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
