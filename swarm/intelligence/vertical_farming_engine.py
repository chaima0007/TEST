"""
Vertical Farming Engine — analyse les opérations d'agriculture verticale pour identifier
les risques de rendement, consommation énergétique, durabilité et scalabilité.

Score composite :
  yield_score(30%) + energy_score(25%) + sustainability_score(25%) + scalability_score(20%)
  → Niveau de risque : critique / élevé / modéré / faible
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional


# ─── Patterns ────────────────────────────────────────────────────────────────

_PATTERNS: List[Dict[str, str]] = [
    {
        "name": "Rendement Insuffisant Critique",
        "severity_fr": "critique",
        "action_fr": "Revoir immédiatement le protocole de culture — ajuster densité de plantation, cycle lumineux et nutrition hydroponique pour restaurer les rendements au seuil de viabilité économique.",
        "signal_fr": "Rendement en kg/m² inférieur de plus de 40% aux benchmarks sectoriels sur les 3 derniers cycles de production.",
    },
    {
        "name": "Consommation Énergie Excessive",
        "severity_fr": "critique",
        "action_fr": "Auditer immédiatement le système d'éclairage LED et HVAC — migrer vers des solutions basse consommation et optimiser les plages horaires d'éclairage pour réduire le coût énergétique par kg produit.",
        "signal_fr": "Consommation électrique par kg produit supérieure de 60% à la moyenne sectorielle, menaçant directement la rentabilité de l'opération.",
    },
    {
        "name": "Échec Scalabilité",
        "severity_fr": "élevé",
        "action_fr": "Revoir l'architecture modulaire des tours de culture et la logistique interne — identifier les goulots d'étranglement humains et technologiques avant toute tentative d'expansion de superficie.",
        "signal_fr": "Incapacité à augmenter la production proportionnellement à la surface disponible — rendement par module stagnant ou décroissant lors des extensions.",
    },
    {
        "name": "Impact Carbone Élevé",
        "severity_fr": "modéré",
        "action_fr": "Planifier la transition vers des sources d'énergie renouvelable (PPA solaire/éolien) et optimiser la chaîne logistique de distribution pour réduire l'empreinte carbone globale de l'opération.",
        "signal_fr": "Bilan carbone net supérieur aux cibles ESG — mix énergétique fossile dominant et transport longue distance réduisant l'avantage environnemental de l'agriculture verticale.",
    },
    {
        "name": "Risque Rentabilité",
        "severity_fr": "faible",
        "action_fr": "Diversifier le portefeuille de cultures vers des variétés à haute valeur ajoutée (microgreens, herbes aromatiques premium) et explorer les partenariats avec la grande distribution pour sécuriser les débouchés commerciaux.",
        "signal_fr": "Marge brute en compression progressive — coûts opérationnels croissants non compensés par une montée en gamme suffisante du mix produit.",
    },
]

_PATTERN_MAP: Dict[str, Dict[str, str]] = {p["name"]: p for p in _PATTERNS}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _composite(yield_score: float, energy_score: float,
                sustainability_score: float, scalability_score: float) -> float:
    return round(
        yield_score * 0.30
        + energy_score * 0.25
        + sustainability_score * 0.25
        + scalability_score * 0.20,
        2,
    )


def _risk_level(composite_score: float) -> str:
    if composite_score >= 60:
        return "critique"
    if composite_score >= 40:
        return "élevé"
    if composite_score >= 20:
        return "modéré"
    return "faible"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ─── Entity dataclass ─────────────────────────────────────────────────────────

@dataclass
class FarmingEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    yield_score: float
    energy_score: float
    sustainability_score: float
    scalability_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str

    @property
    def composite_score(self) -> float:
        return _composite(
            self.yield_score,
            self.energy_score,
            self.sustainability_score,
            self.scalability_score,
        )

    @property
    def risk_level(self) -> str:
        return _risk_level(self.composite_score)

    @property
    def estimated_farming_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        cs = self.composite_score
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "domain": VerticalFarmingEngine.DOMAIN,
            "composite_score": cs,
            "yield_score": self.yield_score,
            "energy_score": self.energy_score,
            "sustainability_score": self.sustainability_score,
            "scalability_score": self.scalability_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_farming_index": self.estimated_farming_index,
            "last_updated": self.last_updated,
        }


# ─── Mock entities ────────────────────────────────────────────────────────────

def _build_mock_entities(ts: str) -> List[FarmingEntity]:
    return [
        # ── CRITIQUE (composite ≥ 60) ──────────────────────────────────────
        FarmingEntity(
            entity_id="VF-001",
            name="AeroFarm Detroit",
            country="USA",
            sector="Vertical Farming",
            yield_score=72.0,
            energy_score=68.0,
            sustainability_score=58.0,
            scalability_score=62.0,
            primary_pattern="Rendement Insuffisant Critique",
            key_signals=[
                "Rendement en kg/m² inférieur de 45% aux benchmarks sectoriels américains",
                "Coût de production unitaire non compétitif face aux importations mexicaines",
                "Turnover opérateur de 38% sur 12 mois fragilisant la continuité des cycles",
            ],
            last_updated=ts,
        ),
        FarmingEntity(
            entity_id="VF-002",
            name="UrbanCrop Asia",
            country="Bangladesh",
            sector="Urban Agriculture",
            yield_score=65.0,
            energy_score=78.0,
            sustainability_score=62.0,
            scalability_score=55.0,
            primary_pattern="Consommation Énergie Excessive",
            key_signals=[
                "Consommation électrique de 28 kWh/kg — plus de 2x la moyenne sectorielle asiatique",
                "Réseau électrique local instable provoquant 14% de pertes de cycles sur l'année",
                "Absence de contrat PPA solaire malgré un ensoleillement potentiel de 5,2 kWh/m²/j",
            ],
            last_updated=ts,
        ),
        FarmingEntity(
            entity_id="VF-003",
            name="GrowTech Africa",
            country="Nigeria",
            sector="AgriTech",
            yield_score=70.0,
            energy_score=60.0,
            sustainability_score=65.0,
            scalability_score=63.0,
            primary_pattern="Rendement Insuffisant Critique",
            key_signals=[
                "Infrastructure d'irrigation hydroponique vieillissante causant 22% de perte nutritive",
                "Chaîne du froid insuffisante entraînant 18% de pertes post-récolte avant distribution",
                "Manque de techniciens spécialisés en agriculture verticale sur le marché local nigérian",
            ],
            last_updated=ts,
        ),
        # ── ÉLEVÉ (composite 40–59) ────────────────────────────────────────
        FarmingEntity(
            entity_id="VF-004",
            name="VerticalVeg UK",
            country="United Kingdom",
            sector="Horticulture",
            yield_score=48.0,
            energy_score=44.0,
            sustainability_score=52.0,
            scalability_score=38.0,
            primary_pattern="Échec Scalabilité",
            key_signals=[
                "Croissance de la surface cultivée de 40% non suivie d'une hausse proportionnelle du rendement",
                "Systèmes de contrôle climatique non centralisés limitant la gestion multi-sites",
                "Brexit complexifiant l'approvisionnement en intrants et équipements spécialisés européens",
            ],
            last_updated=ts,
        ),
        FarmingEntity(
            entity_id="VF-005",
            name="FarmBot EU GmbH",
            country="Germany",
            sector="AgriTech",
            yield_score=45.0,
            energy_score=50.0,
            sustainability_score=42.0,
            scalability_score=47.0,
            primary_pattern="Impact Carbone Élevé",
            key_signals=[
                "Mix énergétique à 61% fossile malgré les objectifs ESG déclarés pour 2025",
                "Empreinte carbone de 3,8 kgCO₂eq/kg produit — dépassant les seuils de labellisation bio",
                "Pression réglementaire croissante de la nouvelle directive européenne sur l'agriculture durable",
            ],
            last_updated=ts,
        ),
        # ── MODÉRÉ (composite 20–39) ───────────────────────────────────────
        FarmingEntity(
            entity_id="VF-006",
            name="HydroFarm SARL",
            country="France",
            sector="Hydroponic",
            yield_score=28.0,
            energy_score=32.0,
            sustainability_score=35.0,
            scalability_score=30.0,
            primary_pattern="Risque Rentabilité",
            key_signals=[
                "Marge brute en baisse de 8 points sur 18 mois sous pression des coûts énergétiques",
                "Portefeuille produits concentré sur la laitue (72% du CA) — diversification insuffisante",
                "Contrats grande distribution à prix fixes ne reflétant pas la hausse des coûts opérationnels",
            ],
            last_updated=ts,
        ),
        # ── FAIBLE (composite < 20) ────────────────────────────────────────
        FarmingEntity(
            entity_id="VF-007",
            name="Nordic GreenFarm AS",
            country="Norway",
            sector="Sustainable Agriculture",
            yield_score=12.0,
            energy_score=15.0,
            sustainability_score=18.0,
            scalability_score=14.0,
            primary_pattern="Risque Rentabilité",
            key_signals=[
                "Modèle économique solide avec marge brute de 42% grâce à l'énergie hydraulique locale",
                "Certification Nordic Swan obtenue — prime prix de 25% sur les marchés premium nordiques",
                "Partenariat stratégique avec NorgesGruppen couvrant 35% de la capacité de production",
            ],
            last_updated=ts,
        ),
        FarmingEntity(
            entity_id="VF-008",
            name="EcoFarm Netherlands BV",
            country="Netherlands",
            sector="Sustainable Agriculture",
            yield_score=10.0,
            energy_score=8.0,
            sustainability_score=14.0,
            scalability_score=12.0,
            primary_pattern="Risque Rentabilité",
            key_signals=[
                "Leader sectoriel : rendement de 42 kg/m²/an en laitue — 2,3x la moyenne européenne",
                "100% énergie renouvelable via PPA éolien offshore — coût électrique de 0,04 €/kWh",
                "Expansion planifiée de 12 000 m² supplémentaires financée par Rabobank Agri-Finance",
            ],
            last_updated=ts,
        ),
    ]


# ─── Engine ───────────────────────────────────────────────────────────────────

class VerticalFarmingEngine:
    DOMAIN = "farming"
    SLUG = "vertical-farming-engine"
    ENGINE_VERSION = "1.0.0"

    def __init__(self) -> None:
        self._entities: List[FarmingEntity] = []
        self._last_analysis: Optional[str] = None

    def analyze_farming(self, entities: Optional[List[FarmingEntity]] = None) -> List[FarmingEntity]:
        """Analyse les entités d'agriculture verticale fournies, ou charge les données mock."""
        ts = _now_iso()
        if entities is not None:
            self._entities = entities
        else:
            self._entities = _build_mock_entities(ts)
        self._last_analysis = ts
        return self._entities

    def get(self, entity_id: str) -> Optional[FarmingEntity]:
        for e in self._entities:
            if e.entity_id == entity_id:
                return e
        return None

    def by_risk(self, risk_level: str) -> List[FarmingEntity]:
        return [e for e in self._entities if e.risk_level == risk_level]

    def critique_entities(self) -> List[FarmingEntity]:
        return self.by_risk("critique")

    def all_entities(self) -> List[FarmingEntity]:
        return sorted(self._entities, key=lambda e: e.composite_score, reverse=True)

    def summary(self) -> dict:
        entities = self._entities
        count = len(entities)

        if count == 0:
            return {
                "total_entities": 0,
                "avg_composite": 0.0,
                "risk_distribution": {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0},
                "pattern_distribution": {p["name"]: 0 for p in _PATTERNS},
                "top_risk_entities": [],
                "critical_alerts": [],
                "last_analysis": self._last_analysis,
                "engine_version": self.ENGINE_VERSION,
                "domain": self.DOMAIN,
                "confidence_score": 0.0,
                "data_sources": [],
                "entities": [],
                "avg_estimated_farming_index": 0.0,
            }

        avg_composite = round(sum(e.composite_score for e in entities) / count, 2)

        risk_dist: Dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
        pattern_dist: Dict[str, int] = {p["name"]: 0 for p in _PATTERNS}
        for e in entities:
            risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
            if e.primary_pattern in pattern_dist:
                pattern_dist[e.primary_pattern] += 1

        top_risk = sorted(
            [e for e in entities if e.composite_score >= 40],
            key=lambda e: e.composite_score,
            reverse=True,
        )[:5]

        critical_alerts = [
            f"{e.name} ({e.country}) — score composite {e.composite_score:.0f}/100 — {e.primary_pattern}"
            for e in entities
            if e.risk_level == "critique"
        ]

        avg_estimated_farming_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": count,
            "avg_composite": avg_composite,
            "risk_distribution": risk_dist,
            "pattern_distribution": pattern_dist,
            "top_risk_entities": [e.to_dict() for e in top_risk],
            "critical_alerts": critical_alerts,
            "last_analysis": self._last_analysis,
            "engine_version": self.ENGINE_VERSION,
            "domain": self.DOMAIN,
            "confidence_score": round(min(100.0, count / 10 * 100), 1),
            "data_sources": [
                "FAO Vertical Farming Statistics 2024",
                "USDA Urban Agriculture Report",
                "EU Farm to Fork Strategy Data",
                "IEA Energy in Agriculture 2024",
            ],
            "entities": [e.to_dict() for e in entities],
            "avg_estimated_farming_index": avg_estimated_farming_index,
        }

    def reset(self) -> None:
        self._entities = []
        self._last_analysis = None


def summary() -> dict:
    """Module-level summary — returns the canonical 13-key dict."""
    return VerticalFarmingEngine().summary()


def analyze_farming() -> dict:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()
