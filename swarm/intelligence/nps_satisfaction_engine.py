"""
NPS & Customer Satisfaction Intelligence Engine — Caelum Partners Swarm Module

Tracks client NPS scores, satisfaction levels and churn risk, then computes a
composite risk score to identify at-risk accounts and trigger retention actions.

Risk levels:
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20

Usage:
    from intelligence.nps_satisfaction_engine import NPSSatisfactionEngine
    engine = NPSSatisfactionEngine()
    print(engine.summary())
    for client in engine.clients:
        print(client.to_dict())
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

logger = logging.getLogger("swarm.nps_satisfaction")


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class ClientRecord:
    id: str
    name: str
    sector: str
    nps_score: float                  # 0–10
    satisfaction_level: float         # 0–100
    churn_risk: float                 # 0–100
    response_time_days: float
    last_contact_date: str            # ISO date string
    total_spent_eur: float
    project_count: int
    support_tickets: int
    recommendation_likelihood: float  # 0–100
    contract_renewal_months: int
    composite_risk_score: float = field(init=False)
    risk_level: str = field(init=False)

    def __post_init__(self) -> None:
        self.composite_risk_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()

    def _compute_composite(self) -> float:
        """
        Weighted composite risk formula (weights sum to 1.00):
          churn_risk × 0.35
          + (100 − nps_score × 10) × 0.30
          + (100 − satisfaction_level) × 0.25
          + (support_tickets / 10 × 100) × 0.10
        """
        score = (
            self.churn_risk * 0.35
            + (100 - self.nps_score * 10) * 0.30
            + (100 - self.satisfaction_level) * 0.25
            + (self.support_tickets / 10 * 100) * 0.10
        )
        return round(score, 2)

    def _compute_risk_level(self) -> str:
        if self.composite_risk_score >= 60:
            return "critique"
        if self.composite_risk_score >= 40:
            return "élevé"
        if self.composite_risk_score >= 20:
            return "modéré"
        return "faible"

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        return {
            "id": self.id,
            "name": self.name,
            "sector": self.sector,
            "nps_score": self.nps_score,
            "satisfaction_level": self.satisfaction_level,
            "churn_risk": self.churn_risk,
            "response_time_days": self.response_time_days,
            "last_contact_date": self.last_contact_date,
            "total_spent_eur": self.total_spent_eur,
            "project_count": self.project_count,
            "support_tickets": self.support_tickets,
            "recommendation_likelihood": self.recommendation_likelihood,
            "contract_renewal_months": self.contract_renewal_months,
            "composite_risk_score": self.composite_risk_score,
            "risk_level": self.risk_level,
        }


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "id": "P1",
        "name": "Décrochage NPS",
        "severity": "critique",
        "description": "NPS inférieur à 5 combiné à une satisfaction en chute — risque de désabonnement imminent.",
        "action": "Appel de rétention sous 48h par le responsable de compte senior.",
        "signal": "nps_score < 5",
    },
    {
        "id": "P2",
        "name": "Churn Risk Élevé",
        "severity": "élevé",
        "description": "Score de churn supérieur à 70 — le client évalue activement des alternatives concurrentes.",
        "action": "Proposer un audit gratuit et une offre de renouvellement anticipé avec remise fidélité.",
        "signal": "churn_risk > 70",
    },
    {
        "id": "P3",
        "name": "Surcharge Support",
        "severity": "élevé",
        "description": "Volume de tickets support anormalement élevé indiquant des frictions produit répétées.",
        "action": "Session de formation dédiée + escalade vers l'équipe technique pour correction durable.",
        "signal": "support_tickets >= 7",
    },
    {
        "id": "P4",
        "name": "Silence Prolongé",
        "severity": "modéré",
        "description": "Aucun contact depuis plus de 60 jours — le client se désengage silencieusement.",
        "action": "Envoyer un rapport de valeur personnalisé et planifier un check-in trimestriel.",
        "signal": "response_time_days > 60",
    },
    {
        "id": "P5",
        "name": "Faible Recommandation",
        "severity": "modéré",
        "description": "Probabilité de recommandation inférieure à 40 — le client ne génère pas de bouche-à-oreille positif.",
        "action": "Programme ambassadeur + cas client co-rédigé pour renforcer l'engagement.",
        "signal": "recommendation_likelihood < 40",
    },
]


# ── Engine ────────────────────────────────────────────────────────────────────

class NPSSatisfactionEngine:
    """
    Swarm Intelligence module for NPS and customer satisfaction tracking.

    Computes composite risk scores, detects retention patterns,
    and surfaces actionable insights for the Caelum Partners CRM.
    """

    def __init__(self) -> None:
        self.clients: List[ClientRecord] = self._build_mock_clients()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "NPSSatisfactionEngine initialised — %d clients, %d patterns",
            len(self.clients),
            len(self.patterns),
        )

    # ── Mock data ─────────────────────────────────────────────────────────────

    def _build_mock_clients(self) -> List[ClientRecord]:
        """
        8 mock clients covering all 5 patterns and all 4 risk levels.
        Distribution: ≥3 critique, ≥2 élevé, ≥1 modéré, ≥2 faible.

        Composite formula verification:
          CLI-001: 85*0.35 + (100-2*10)*0.30 + (100-22)*0.25 + (9/10*100)*0.10
                 = 29.75 + 24.0 + 19.5 + 9.0 = 82.25  → critique ✓  (P1, P2, P3)
          CLI-002: 78*0.35 + (100-3*10)*0.30 + (100-28)*0.25 + (8/10*100)*0.10
                 = 27.3 + 21.0 + 18.0 + 8.0 = 74.30   → critique ✓  (P1, P2, P3, P5)
          CLI-003: 72*0.35 + (100-4*10)*0.30 + (100-30)*0.25 + (10/10*100)*0.10
                 = 25.2 + 18.0 + 17.5 + 10.0 = 70.70  → critique ✓  (P1, P2, P3, P5)
          CLI-004: 55*0.35 + (100-5*10)*0.30 + (100-50)*0.25 + (4/10*100)*0.10
                 = 19.25 + 15.0 + 12.5 + 4.0 = 50.75  → élevé ✓    (P4)
          CLI-005: 50*0.35 + (100-5.5*10)*0.30 + (100-52)*0.25 + (5/10*100)*0.10
                 = 17.5 + 13.5 + 12.0 + 5.0 = 48.00   → élevé ✓    (P5)
          CLI-006: 30*0.35 + (100-6.5*10)*0.30 + (100-65)*0.25 + (3/10*100)*0.10
                 = 10.5 + 10.5 + 8.75 + 3.0 = 32.75   → modéré ✓
          CLI-007: 8*0.35  + (100-9*10)*0.30  + (100-91)*0.25 + (1/10*100)*0.10
                 = 2.8 + 3.0 + 2.25 + 1.0 = 9.05      → faible ✓
          CLI-008: 12*0.35 + (100-8.5*10)*0.30 + (100-88)*0.25 + (2/10*100)*0.10
                 = 4.2 + 4.5 + 3.0 + 2.0 = 13.70      → faible ✓
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            # P1 (nps<5) + P2 (churn>70) + P3 (tickets>=7)
            {
                "id": "CLI-001",
                "name": "TechVision SARL",
                "sector": "Logiciels & SaaS",
                "nps_score": 2.0,
                "satisfaction_level": 22.0,
                "churn_risk": 85.0,
                "response_time_days": 4.0,
                "last_contact_date": "2026-05-10",
                "total_spent_eur": 48000.0,
                "project_count": 3,
                "support_tickets": 9,
                "recommendation_likelihood": 15.0,
                "contract_renewal_months": 2,
            },
            # P1 (nps<5) + P2 (churn>70) + P3 (tickets>=7) + P5 (rec<40)
            {
                "id": "CLI-002",
                "name": "Groupe Médical Arcen",
                "sector": "Santé & Médical",
                "nps_score": 3.0,
                "satisfaction_level": 28.0,
                "churn_risk": 78.0,
                "response_time_days": 12.0,
                "last_contact_date": "2026-04-28",
                "total_spent_eur": 92000.0,
                "project_count": 5,
                "support_tickets": 8,
                "recommendation_likelihood": 20.0,
                "contract_renewal_months": 1,
            },
            # P1 (nps<5) + P2 (churn>70) + P3 (tickets>=7) + P5 (rec<40)
            {
                "id": "CLI-003",
                "name": "Immobilière Bruxelles Est",
                "sector": "Immobilier & Promotion",
                "nps_score": 4.0,
                "satisfaction_level": 30.0,
                "churn_risk": 72.0,
                "response_time_days": 8.0,
                "last_contact_date": "2026-05-20",
                "total_spent_eur": 67000.0,
                "project_count": 4,
                "support_tickets": 10,
                "recommendation_likelihood": 28.0,
                "contract_renewal_months": 3,
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            # P4 (response_time>60) — Silence Prolongé
            {
                "id": "CLI-004",
                "name": "Hôtel Le Méridien Bruges",
                "sector": "Hôtellerie & Tourisme",
                "nps_score": 5.0,
                "satisfaction_level": 50.0,
                "churn_risk": 55.0,
                "response_time_days": 75.0,
                "last_contact_date": "2026-04-05",
                "total_spent_eur": 115000.0,
                "project_count": 6,
                "support_tickets": 4,
                "recommendation_likelihood": 45.0,
                "contract_renewal_months": 5,
            },
            # P5 (rec<40) — Faible Recommandation
            {
                "id": "CLI-005",
                "name": "Cabinet Juridique Vandermeer",
                "sector": "Services Juridiques",
                "nps_score": 5.5,
                "satisfaction_level": 52.0,
                "churn_risk": 50.0,
                "response_time_days": 18.0,
                "last_contact_date": "2026-05-30",
                "total_spent_eur": 78000.0,
                "project_count": 4,
                "support_tickets": 5,
                "recommendation_likelihood": 30.0,
                "contract_renewal_months": 6,
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            # Mixed signals, no major pattern triggered
            {
                "id": "CLI-006",
                "name": "Brasserie Artisan Namur",
                "sector": "Restauration & Alimentation",
                "nps_score": 6.5,
                "satisfaction_level": 65.0,
                "churn_risk": 30.0,
                "response_time_days": 21.0,
                "last_contact_date": "2026-06-01",
                "total_spent_eur": 34000.0,
                "project_count": 2,
                "support_tickets": 3,
                "recommendation_likelihood": 55.0,
                "contract_renewal_months": 9,
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            # Happy, loyal flagship client
            {
                "id": "CLI-007",
                "name": "FinTech Capitale SA",
                "sector": "Finance & Assurance",
                "nps_score": 9.0,
                "satisfaction_level": 91.0,
                "churn_risk": 8.0,
                "response_time_days": 2.0,
                "last_contact_date": "2026-06-15",
                "total_spent_eur": 210000.0,
                "project_count": 12,
                "support_tickets": 1,
                "recommendation_likelihood": 92.0,
                "contract_renewal_months": 24,
            },
            # Excellent satisfaction, long-term partner
            {
                "id": "CLI-008",
                "name": "EduTech Benelux ASBL",
                "sector": "Éducation & Formation",
                "nps_score": 8.5,
                "satisfaction_level": 88.0,
                "churn_risk": 12.0,
                "response_time_days": 3.0,
                "last_contact_date": "2026-06-10",
                "total_spent_eur": 56000.0,
                "project_count": 7,
                "support_tickets": 2,
                "recommendation_likelihood": 85.0,
                "contract_renewal_months": 18,
            },
        ]

        return [ClientRecord(**d) for d in raw]  # type: ignore[arg-type]

    # ── Aggregates ────────────────────────────────────────────────────────────

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(self.clients)
        avg_nps = round(sum(c.nps_score for c in self.clients) / n, 2)
        avg_sat = round(sum(c.satisfaction_level for c in self.clients) / n, 2)
        avg_churn = round(sum(c.churn_risk for c in self.clients) / n, 2)
        avg_composite = round(sum(c.composite_risk_score for c in self.clients) / n, 2)

        clients_critique = sum(1 for c in self.clients if c.risk_level == "critique")
        clients_eleve = sum(1 for c in self.clients if c.risk_level == "élevé")
        clients_modere = sum(1 for c in self.clients if c.risk_level == "modéré")
        clients_faible = sum(1 for c in self.clients if c.risk_level == "faible")

        top = max(self.clients, key=lambda c: c.composite_risk_score)
        patterns_detected = self._count_patterns_detected()
        avg_esi = round(avg_composite / 100 * 10, 2)

        return {
            "total_clients": n,
            "avg_nps": avg_nps,
            "avg_satisfaction": avg_sat,
            "avg_churn_risk": avg_churn,
            "clients_critique": clients_critique,
            "clients_eleve": clients_eleve,
            "clients_modere": clients_modere,
            "clients_faible": clients_faible,
            "top_risk_client": top.name,
            "top_risk_score": top.composite_risk_score,
            "patterns_detected": patterns_detected,
            "avg_composite": avg_composite,
            "avg_estimated_satisfaction_index": avg_esi,
        }

    def _count_patterns_detected(self) -> int:
        """Count how many distinct patterns are triggered across the client base."""
        triggered: Set[str] = set()
        for c in self.clients:
            if c.nps_score < 5:
                triggered.add("P1")
            if c.churn_risk > 70:
                triggered.add("P2")
            if c.support_tickets >= 7:
                triggered.add("P3")
            if c.response_time_days > 60:
                triggered.add("P4")
            if c.recommendation_likelihood < 40:
                triggered.add("P5")
        return len(triggered)

    # ── Convenience ───────────────────────────────────────────────────────────

    def get_clients_by_risk(self, risk_level: str) -> List[ClientRecord]:
        return [c for c in self.clients if c.risk_level == risk_level]

    def get_client_patterns(self, client: ClientRecord) -> List[Dict[str, str]]:
        """Return the list of pattern dicts triggered for a given client."""
        matched = []
        if client.nps_score < 5:
            matched.append(PATTERNS[0])
        if client.churn_risk > 70:
            matched.append(PATTERNS[1])
        if client.support_tickets >= 7:
            matched.append(PATTERNS[2])
        if client.response_time_days > 60:
            matched.append(PATTERNS[3])
        if client.recommendation_likelihood < 40:
            matched.append(PATTERNS[4])
        return matched

    def export(self) -> Dict[str, Any]:
        return {
            "entities": [c.to_dict() for c in self.clients],
            "summary": self.summary(),
            "patterns": self.patterns,
        }
