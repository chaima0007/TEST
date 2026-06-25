"""
Caelum Partners — Undersea Cable Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Les câbles sous-marins : artères numériques vulnérables de la mondialisation.
99% du trafic Internet intercontinental transite par 400+ câbles sous-marins
représentant 10 000Md$ de transactions financières quotidiennes et les
communications militaires de l'OTAN. Ces infrastructures critiques, posées
à des profondeurs de 8 000m, sont protégées par le seul droit international
de la mer — sans mécanisme de défense active.

La Chine via HMN Technologies (ex-Huawei Marine Networks) construit 20%+
des nouveaux câbles sous-marins mondiaux et a été exclue de plusieurs projets
occidentaux (PEACE Cable alternative, Pacific Light Cable Network bloqué par
FCC). La Russie dispose du navire AS-12 Losharik capable de couper des câbles
à 6 000m de profondeur — une capacité que les experts attribuent aux coupures
mystérieuses de câbles en mer Baltique (BCS East-West Interlink, octobre 2023,
Arelion câble suédois). La NSA (USA) a intercepté des communications via des
taps sur les câbles sous-marins selon les révélations Snowden (programme OAKSTAR).

Les Cinq Eyes partagent l'accès aux landing stations britanniques (GCHQ/UKUSA).
La concentration géographique crée des chokepoints critiques : Détroit de
Malacca (90% du trafic Asie-Europe), Suez Canal câbles, Bosphore et Gibraltar.
Taïwan dispose de 14 câbles essentiels pour son économie — dont 2 ont été
sectionnés par des navires chinois en 2023 selon les autorités taïwanaises.

Risk levels (câbles sous-marins et infrastructure numérique critique) :
  critique  → composite ≥ 60  (contrôle actif ou sabotage — capacité avérée d'attaque sur l'infrastructure câbles)
  élevé     → composite ≥ 40  (course à la domination numérique — investissements stratégiques dans les câbles)
  modéré    → composite ≥ 20  (vulnérabilité câbles — dépendance critique sans protection adéquate)
  faible    → composite < 20  (gouvernance multilatérale — cadres de protection et coopération internationale)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "controle_infrastructure_internet": {
        "severity_fr": "Critique",
        "action_fr": "Sécurisation des landing stations — accords de réciprocité sur les propriétaires de câbles, exclusion des équipementiers à risque et diversification des routes",
        "signal_fr": "cable_chokepoint_control_score > 85 AND landing_station_surveillance_score > 85 — contrôle stratégique des infrastructures câbles et des points d'atterrissage",
    },
    "sabotage_sous_marin_strategique": {
        "severity_fr": "Critique",
        "action_fr": "Doctrine de défense des câbles — patrouilles sous-marines OTAN, système d'alerte sismique des coupures et attribution rapide des actes de sabotage",
        "signal_fr": "submarine_sabotage_capability_score > 85 — capacité avérée de sabotage des câbles sous-marins par des submersibles spécialisés",
    },
    "monopole_construction_cables": {
        "severity_fr": "Critique",
        "action_fr": "Diversifier les constructeurs de câbles — soutenir SubCom, Alcatel Submarine Networks et consortiums alliés face à la montée de HMN Technologies",
        "signal_fr": "cable_build_monopoly_score > 85 — monopolisation croissante du marché de construction des câbles sous-marins par des acteurs à risque",
    },
    "course_domination_numerique": {
        "severity_fr": "Élevé",
        "action_fr": "Investissements alliés dans les câbles — financement G7 de routes alternatives et résilience des infrastructures numériques critiques mondiales",
        "signal_fr": "Course à la domination des infrastructures numériques — investissements stratégiques dans les câbles comme levier de contrôle informationnel",
    },
    "gouvernance_multilaterale_cables": {
        "severity_fr": "Faible",
        "action_fr": "Renforcer le cadre ITU — Convention sur la protection des câbles sous-marins modernisée et mécanismes d'intervention rapide en cas de coupure",
        "signal_fr": "composite_score < 20 — engagement actif dans la gouvernance multilatérale des câbles et la protection de l'infrastructure numérique mondiale",
    },
}


@dataclass
class UnderseaCableEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    cable_chokepoint_control_score: float
    submarine_sabotage_capability_score: float
    landing_station_surveillance_score: float
    cable_build_monopoly_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_undersea_cable_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.cable_chokepoint_control_score * 0.30
            + self.submarine_sabotage_capability_score * 0.25
            + self.landing_station_surveillance_score * 0.25
            + self.cable_build_monopoly_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_undersea_cable_index = round(self.composite_score / 100 * 10, 2)

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
        if self.cable_chokepoint_control_score >= 85 and self.landing_station_surveillance_score >= 85:
            return "controle_infrastructure_internet"
        if self.submarine_sabotage_capability_score >= 85:
            return "sabotage_sous_marin_strategique"
        if self.cable_build_monopoly_score >= 85:
            return "monopole_construction_cables"
        if self.composite_score >= 20:
            return "course_domination_numerique"
        return "gouvernance_multilaterale_cables"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Contrôle des infrastructures numériques critiques par {n} — maîtrise des chokepoints câbles et des landing stations mondiales",
                "Weaponisation des câbles sous-marins — capacité de sabotage, d'interception et de coupure des artères numériques intercontinentales",
                "Vulnérabilité systémique mondiale — les coupures ciblées pourraient paralyser les marchés financiers et les communications militaires",
            ]
        if self.risk_level == "élevé":
            return [
                f"Course à la domination numérique de {n} — investissements stratégiques dans les câbles comme levier de contrôle informationnel",
                "Diplomatie des câbles — utilisation de la construction de câbles comme outil d'influence et de dépendance des pays partenaires",
                "Risque de concentration — dépendance croissante à des opérateurs de câbles non alliés pour les flux de données critiques",
            ]
        if self.risk_level == "modéré":
            return [
                f"Vulnérabilité câbles de {n} — dépendance critique aux câbles sous-marins sans capacité de protection ou redondance adéquate",
                "Absence de redondance — rupture d'un seul câble peut isoler une région entière des communications numériques mondiales",
                "Risque d'interception — landing stations peu sécurisées exposant les données nationales à des taps par des puissances adverses",
            ]
        return [
            f"{n} contribue à la gouvernance multilatérale des câbles — protection légale, coopération internationale et normes de sécurité",
            "Cadre juridique international — Convention ITU sur la protection des câbles modernisée et attribution rapide des actes de sabotage",
            "Modèle de résilience à partager — redondance des routes, diversification des propriétaires et plans d'urgence documentés",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "cable_chokepoint_control_score": self.cable_chokepoint_control_score,
            "submarine_sabotage_capability_score": self.submarine_sabotage_capability_score,
            "landing_station_surveillance_score": self.landing_station_surveillance_score,
            "cable_build_monopoly_score": self.cable_build_monopoly_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_undersea_cable_index": self.estimated_undersea_cable_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[UnderseaCableEntity] = [
    UnderseaCableEntity("UC-001", "Chine — HMN Tech & 20% Câbles Sous-Marins Mondiaux", "Asie", "HMN Technologies Ex-Huawei Marine, PEACE Cable Afrique-Asie & Exclusion Projets USA/EU", 88.0, 82.0, 85.0, 92.0),
    UnderseaCableEntity("UC-002", "USA — SubCom & Five Eyes Surveillance Câbles", "Amérique du Nord", "SubCom 500K km Câbles, GCHQ/NSA Taps Câbles Transatlantiques & FCC Exclusion HMN", 85.0, 80.0, 90.0, 82.0),
    UnderseaCableEntity("UC-003", "Russie — AS-12 Losharik & Sabotage Baltique", "Europe de l'Est", "Losharik Sous-Marin Spécial 6000m, BCS East-West Interlink Coupure Oct 2023 & Yantar Navire", 75.0, 92.0, 80.0, 65.0),
    UnderseaCableEntity("UC-004", "UK & France — GCHQ, Alcatel & Surveillance UKUSA", "Europe", "GCHQ Programme Tempora, Alcatel Submarine 200K km & Five Eyes Landing Stations UK", 72.0, 68.0, 88.0, 78.0),
    UnderseaCableEntity("UC-005", "Turquie & Détroit Bosphore — Chokepoint Maritime", "MENA/Europe", "Bosphore 0km Câbles Alternatifs, Transit Obligatoire & Contrôle Passage Naval Convention Montreux", 58.0, 52.0, 48.0, 55.0),
    UnderseaCableEntity("UC-006", "Singapour & Dubaï — Hubs Régionaux Câbles", "Asie/MENA", "Singapore Cable Hub Asie-Pacifique, Equinix LD5 London & Dubaï Télécom Landing Stations", 52.0, 45.0, 55.0, 50.0),
    UnderseaCableEntity("UC-007", "Taïwan — 14 Câbles Essentiels & Vulnérabilité Stratégique", "Asie", "14 Câbles Sous-Marins Vitaux, 2 Coupés par Navires Chinois 2023 & Aucune Redondance Terrestre", 30.0, 28.0, 35.0, 25.0),
    UnderseaCableEntity("UC-008", "ITU & ICPC — Gouvernance Internationale Câbles", "Global", "ITU Convention Câbles 1884 Révisée, ICPC Standards & Zones Protection Câbles IMO", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "undersea_cable",
        "confidence_score": 0.77,
        "data_sources": ["telegeography_submarine_cable_map", "submarine_cable_networks_pctelecommunications", "csis_undersea_cable_security"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_undersea_cable_index": round(avg / 100 * 10, 2),
    }


def analyze_undersea_cable() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Undersea Cable Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
