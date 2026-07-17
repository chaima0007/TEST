"""
Client Retention Intelligence Engine — Caelum Partners Swarm Module

Analyses client health and loyalty to detect churn risk and upsell opportunities.
Produces composite risk scores, loyalty tiers, and actionable retention patterns.
"""

from __future__ import annotations

from typing import Dict, List


# ── Risk thresholds ────────────────────────────────────────────────────────────

def _risk_level(score: float) -> str:
    if score >= 60:
        return "critique"
    if score >= 40:
        return "élevé"
    if score >= 20:
        return "modéré"
    return "faible"


def _composite_risk(
    missed_meetings: int,
    delayed_payments: int,
    renewal_probability: int,
    engagement_score: int,
) -> float:
    """
    Weighted composite risk (0-100, 2 decimals).
    Weights: (missed_meetings×10) × 0.30
           + (delayed_payments×15) × 0.25
           + (100-renewal_prob)    × 0.25
           + (100-engagement)      × 0.20
    """
    raw = (
        (missed_meetings * 10) * 0.30
        + (delayed_payments * 15) * 0.25
        + (100 - renewal_probability) * 0.25
        + (100 - engagement_score) * 0.20
    )
    return round(min(raw, 100.0), 2)


# ── Mock dataset ───────────────────────────────────────────────────────────────
# 8 clients covering all 5 patterns and all 4 risk levels:
#   - ≥3 critique  (CLT-001, CLT-002, CLT-003)
#   - ≥2 élevé     (CLT-004, CLT-005)
#   - ≥1 modéré    (CLT-006)
#   - ≥2 faible    (CLT-007, CLT-008)

_RAW_CLIENTS = [
    # ── CRITIQUE ──────────────────────────────────────────────────────────────
    {
        "id": "CLT-001",
        "name": "Brasserie Le Vieux Port",
        "sector": "Restauration",
        "months_active": 14,
        "contract_value_eur": 2990,
        "last_invoice_days_ago": 62,   # → inactivité prolongée
        "missed_meetings": 4,           # → relation à risque de rupture
        "delayed_payments": 5,          # → paiements retardés répétés
        "upsell_opportunities": 2,
        "support_ticket_frequency": 0.8,
        "engagement_score": 18,         # → désengagement progressif
        "loyalty_tier": "bronze",
        "renewal_probability": 22,      # → relation à risque de rupture
    },
    {
        "id": "CLT-002",
        "name": "Garage Renaud Automobiles",
        "sector": "Auto & Garage",
        "months_active": 8,
        "contract_value_eur": 1490,
        "last_invoice_days_ago": 50,   # → inactivité prolongée
        "missed_meetings": 4,
        "delayed_payments": 4,          # → paiements retardés répétés
        "upsell_opportunities": 1,
        "support_ticket_frequency": 1.2,
        "engagement_score": 20,         # → désengagement progressif
        "loyalty_tier": "bronze",
        "renewal_probability": 25,      # → relation à risque de rupture
    },
    {
        "id": "CLT-003",
        "name": "Institut Beauté Céleste",
        "sector": "Beauté & Bien-être",
        "months_active": 6,
        "contract_value_eur": 990,
        "last_invoice_days_ago": 78,   # → inactivité prolongée
        "missed_meetings": 5,
        "delayed_payments": 3,          # → paiements retardés répétés
        "upsell_opportunities": 3,      # → opportunité upsell ignorée (engag<50)
        "support_ticket_frequency": 0.5,
        "engagement_score": 15,         # → désengagement progressif
        "loyalty_tier": "bronze",
        "renewal_probability": 18,      # → relation à risque de rupture
    },
    # ── ÉLEVÉ ─────────────────────────────────────────────────────────────────
    {
        "id": "CLT-004",
        "name": "Cabinet Notarial Marcelin",
        "sector": "Services Juridiques",
        "months_active": 22,
        "contract_value_eur": 4900,
        "last_invoice_days_ago": 30,
        "missed_meetings": 2,
        "delayed_payments": 3,          # → paiements retardés répétés
        "upsell_opportunities": 4,      # → opportunité upsell ignorée (engag<50)
        "support_ticket_frequency": 0.3,
        "engagement_score": 42,
        "loyalty_tier": "silver",
        "renewal_probability": 48,
    },
    {
        "id": "CLT-005",
        "name": "Résidence Hôtelière Les Pins",
        "sector": "Hôtellerie",
        "months_active": 18,
        "contract_value_eur": 3490,
        "last_invoice_days_ago": 22,
        "missed_meetings": 1,
        "delayed_payments": 4,          # → paiements retardés répétés
        "upsell_opportunities": 2,
        "support_ticket_frequency": 0.6,
        "engagement_score": 38,         # → désengagement progressif
        "loyalty_tier": "silver",
        "renewal_probability": 52,
    },
    # ── MODÉRÉ ────────────────────────────────────────────────────────────────
    {
        "id": "CLT-006",
        "name": "École Primaire Les Peupliers",
        "sector": "Éducation",
        "months_active": 30,
        "contract_value_eur": 1990,
        "last_invoice_days_ago": 10,
        "missed_meetings": 1,
        "delayed_payments": 1,
        "upsell_opportunities": 2,
        "support_ticket_frequency": 0.2,
        "engagement_score": 60,
        "loyalty_tier": "silver",
        "renewal_probability": 65,
    },
    # ── FAIBLE ────────────────────────────────────────────────────────────────
    {
        "id": "CLT-007",
        "name": "Clinique Vétérinaire Saintignon",
        "sector": "Médical & Vétérinaire",
        "months_active": 36,
        "contract_value_eur": 5900,
        "last_invoice_days_ago": 5,
        "missed_meetings": 0,
        "delayed_payments": 0,
        "upsell_opportunities": 3,
        "support_ticket_frequency": 0.1,
        "engagement_score": 88,
        "loyalty_tier": "gold",
        "renewal_probability": 92,
    },
    {
        "id": "CLT-008",
        "name": "Immobilier Duplessis & Associés",
        "sector": "Immobilier",
        "months_active": 48,
        "contract_value_eur": 8900,
        "last_invoice_days_ago": 3,
        "missed_meetings": 0,
        "delayed_payments": 0,
        "upsell_opportunities": 5,
        "support_ticket_frequency": 0.05,
        "engagement_score": 96,
        "loyalty_tier": "platinum",
        "renewal_probability": 98,
    },
]


# ── Retention patterns (French) ────────────────────────────────────────────────

_PATTERNS = [
    "inactivité prolongée",
    "paiements retardés répétés",
    "désengagement progressif",
    "opportunité upsell ignorée",
    "relation à risque de rupture",
]


def _detect_patterns(client: dict) -> List[str]:
    """Return applicable pattern labels for a given client."""
    detected = []
    if client["last_invoice_days_ago"] >= 45:
        detected.append("inactivité prolongée")
    if client["delayed_payments"] >= 3:
        detected.append("paiements retardés répétés")
    if client["engagement_score"] < 40:
        detected.append("désengagement progressif")
    if client["upsell_opportunities"] >= 2 and client["engagement_score"] < 50:
        detected.append("opportunité upsell ignorée")
    if client["renewal_probability"] < 35:
        detected.append("relation à risque de rupture")
    return detected


# ── Engine ─────────────────────────────────────────────────────────────────────

class ClientRetentionEngine:
    """
    Analyses Caelum Partners' active client portfolio for churn and retention signals.
    """

    def __init__(self) -> None:
        self._clients: List[Dict] = []
        for raw in _RAW_CLIENTS:
            composite = _composite_risk(
                raw["missed_meetings"],
                raw["delayed_payments"],
                raw["renewal_probability"],
                raw["engagement_score"],
            )
            self._clients.append({
                **raw,
                "composite_risk_score": composite,
                "risk_level": _risk_level(composite),
            })

    # ── Public interface ───────────────────────────────────────────────────────

    @property
    def clients(self) -> List[Dict]:
        return self._clients

    @property
    def patterns(self) -> List[str]:
        return _PATTERNS

    def to_dict(self, client: dict) -> dict:
        """Return exactly 15 keys for a client record."""
        return {
            "id": client["id"],
            "name": client["name"],
            "sector": client["sector"],
            "months_active": client["months_active"],
            "contract_value_eur": client["contract_value_eur"],
            "last_invoice_days_ago": client["last_invoice_days_ago"],
            "missed_meetings": client["missed_meetings"],
            "delayed_payments": client["delayed_payments"],
            "upsell_opportunities": client["upsell_opportunities"],
            "support_ticket_frequency": client["support_ticket_frequency"],
            "engagement_score": client["engagement_score"],
            "loyalty_tier": client["loyalty_tier"],
            "renewal_probability": client["renewal_probability"],
            "composite_risk_score": client["composite_risk_score"],
            "risk_level": client["risk_level"],
        }

    def all_dicts(self) -> List[dict]:
        return [self.to_dict(c) for c in self._clients]

    def summary(self) -> dict:
        """Return exactly 13 summary keys."""
        clients = self._clients
        n = len(clients)

        avg_months = round(sum(c["months_active"] for c in clients) / n, 2)
        avg_value = round(sum(c["contract_value_eur"] for c in clients) / n, 2)
        avg_renewal = round(sum(c["renewal_probability"] for c in clients) / n, 2)
        avg_composite = round(sum(c["composite_risk_score"] for c in clients) / n, 2)

        counts: Dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
        for c in clients:
            counts[c["risk_level"]] += 1

        top = max(clients, key=lambda c: c["composite_risk_score"])

        detected_set: set = set()
        for c in clients:
            for p in _detect_patterns(c):
                detected_set.add(p)

        avg_retention_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_clients": n,
            "avg_months_active": avg_months,
            "avg_contract_value": avg_value,
            "avg_renewal_probability": avg_renewal,
            "clients_critique": counts["critique"],
            "clients_eleve": counts["élevé"],
            "clients_modere": counts["modéré"],
            "clients_faible": counts["faible"],
            "top_risk_client": top["name"],
            "top_risk_score": top["composite_risk_score"],
            "patterns_detected": list(detected_set),
            "avg_composite": avg_composite,
            "avg_estimated_retention_index": avg_retention_index,
        }


# ── CLI smoke-test ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    engine = ClientRetentionEngine()
    print("=== Clients ===")
    for d in engine.all_dicts():
        assert len(d) == 15, f"Expected 15 keys, got {len(d)} for {d['id']}"
        print(
            f"  {d['id']} | {d['name']:<42} | "
            f"risk={d['risk_level']:<8} | composite={d['composite_risk_score']}"
        )

    print("\n=== Summary ===")
    s = engine.summary()
    assert len(s) == 13, f"Expected 13 keys, got {len(s)}"
    print(json.dumps(s, ensure_ascii=False, indent=2))
