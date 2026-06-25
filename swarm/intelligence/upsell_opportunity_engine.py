"""
Upsell Opportunity Intelligence Engine — Caelum Partners

Detects and scores upsell/expansion opportunities across the client portfolio.
Composite scoring weights upsell probability, revenue delta, engagement, and tenure.
"""

from __future__ import annotations

from typing import Any


# ── Opportunity patterns (French) ─────────────────────────────────────────────

UPSELL_PATTERNS: list[str] = [
    "opportunité premium détectée",
    "client stagnant depuis 6+ mois",
    "signal d'engagement élevé",
    "décideur accessible",
    "expansion de contrat imminente",
]


# ── Engine ────────────────────────────────────────────────────────────────────

class UpsellOpportunityEngine:
    """
    Analyses client portfolio for upsell and expansion opportunities.

    Each opportunity dict has exactly 15 keys:
      id, client_name, sector, current_plan, current_mrr_eur,
      recommended_upgrade, potential_mrr_eur, delta_mrr_eur,
      months_on_current_plan, last_upsell_attempt_days,
      engagement_signals, decision_maker_access, upsell_probability,
      composite_score, risk_level

    composite_score formula (capped at 100, rounded to 2 decimals):
      upsell_probability * 0.35
      + (delta_mrr_eur / 500 * 100) * 0.30
      + engagement_signals * 10 * 0.20
      + (months_on_current_plan / 24 * 100) * 0.15

    risk_level (= opportunity priority):
      composite >= 60 → "critique"
      composite >= 40 → "élevé"
      composite >= 20 → "modéré"
      else            → "faible"
    """

    # ── private helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _composite(
        upsell_probability: float,
        delta_mrr_eur: float,
        engagement_signals: float,
        months_on_current_plan: float,
    ) -> float:
        raw = (
            upsell_probability * 0.35
            + (delta_mrr_eur / 500 * 100) * 0.30
            + engagement_signals * 10 * 0.20
            + (months_on_current_plan / 24 * 100) * 0.15
        )
        return round(min(raw, 100), 2)

    @staticmethod
    def _risk(composite: float) -> str:
        if composite >= 60:
            return "critique"
        if composite >= 40:
            return "élevé"
        if composite >= 20:
            return "modéré"
        return "faible"

    # ── mock data ─────────────────────────────────────────────────────────────

    def _build_opportunities(self) -> list[dict[str, Any]]:
        """
        8 mock clients covering all 5 patterns and all 4 risk levels:
          ≥3 critique, ≥2 élevé, ≥1 modéré, ≥2 faible
        """
        raw: list[dict[str, Any]] = [
            # ── critique ──────────────────────────────────────────────────────
            {
                "id": "OPP-001",
                "client_name": "Immobilier Dubois & Associés",
                "sector": "Immobilier",
                "current_plan": "essentiel",
                "current_mrr_eur": 149,
                "recommended_upgrade": "performance",
                "potential_mrr_eur": 299,
                "delta_mrr_eur": 150,
                "months_on_current_plan": 18,
                "last_upsell_attempt_days": 45,
                "engagement_signals": 9.0,
                "decision_maker_access": True,
                "upsell_probability": 82,
                # patterns: opportunité premium détectée, décideur accessible
            },
            {
                "id": "OPP-002",
                "client_name": "Restaurant Le Bocage",
                "sector": "Restauration & Hôtellerie",
                "current_plan": "performance",
                "current_mrr_eur": 299,
                "recommended_upgrade": "premium",
                "potential_mrr_eur": 490,
                "delta_mrr_eur": 191,
                "months_on_current_plan": 20,
                "last_upsell_attempt_days": 90,
                "engagement_signals": 8.5,
                "decision_maker_access": True,
                "upsell_probability": 78,
                # patterns: signal d'engagement élevé, expansion de contrat imminente
            },
            {
                "id": "OPP-003",
                "client_name": "Cabinet Médical Vaillant",
                "sector": "Médical & Cabinets de Soin",
                "current_plan": "essentiel",
                "current_mrr_eur": 149,
                "recommended_upgrade": "entreprise",
                "potential_mrr_eur": 890,
                "delta_mrr_eur": 741,
                "months_on_current_plan": 14,
                "last_upsell_attempt_days": 30,
                "engagement_signals": 7.5,
                "decision_maker_access": True,
                "upsell_probability": 71,
                # patterns: opportunité premium détectée, décideur accessible, expansion de contrat imminente
            },
            # ── élevé ─────────────────────────────────────────────────────────
            {
                "id": "OPP-004",
                "client_name": "Plomberie Martin & Fils",
                "sector": "Artisans & Bâtiment",
                "current_plan": "performance",
                "current_mrr_eur": 299,
                "recommended_upgrade": "premium",
                "potential_mrr_eur": 490,
                "delta_mrr_eur": 191,
                "months_on_current_plan": 8,
                "last_upsell_attempt_days": 60,
                "engagement_signals": 6.0,
                "decision_maker_access": False,
                "upsell_probability": 54,
                # patterns: signal d'engagement élevé
            },
            {
                "id": "OPP-005",
                "client_name": "Auto Garage Renard",
                "sector": "Garages & Concessionnaires",
                "current_plan": "essentiel",
                "current_mrr_eur": 149,
                "recommended_upgrade": "performance",
                "potential_mrr_eur": 299,
                "delta_mrr_eur": 150,
                "months_on_current_plan": 16,
                "last_upsell_attempt_days": 120,
                "engagement_signals": 5.0,
                "decision_maker_access": False,
                "upsell_probability": 48,
                # patterns: client stagnant depuis 6+ mois
            },
            # ── modéré ────────────────────────────────────────────────────────
            {
                "id": "OPP-006",
                "client_name": "Coiffure Salon Élégance",
                "sector": "Beauté & Bien-être",
                "current_plan": "essentiel",
                "current_mrr_eur": 149,
                "recommended_upgrade": "performance",
                "potential_mrr_eur": 299,
                "delta_mrr_eur": 150,
                "months_on_current_plan": 10,
                "last_upsell_attempt_days": 200,
                "engagement_signals": 4.0,
                "decision_maker_access": False,
                "upsell_probability": 32,
                # patterns: client stagnant depuis 6+ mois
            },
            # ── faible ────────────────────────────────────────────────────────
            {
                "id": "OPP-007",
                "client_name": "Boulangerie Artisan Dupain",
                "sector": "Alimentation & Commerce",
                "current_plan": "essentiel",
                "current_mrr_eur": 149,
                "recommended_upgrade": "performance",
                "potential_mrr_eur": 299,
                "delta_mrr_eur": 100,
                "months_on_current_plan": 2,
                "last_upsell_attempt_days": 5,
                "engagement_signals": 1.5,
                "decision_maker_access": False,
                "upsell_probability": 15,
                # patterns: (none dominant — too early in plan lifecycle)
            },
            {
                "id": "OPP-008",
                "client_name": "École Privée Lumière",
                "sector": "Éducation & Formation",
                "current_plan": "performance",
                "current_mrr_eur": 299,
                "recommended_upgrade": "premium",
                "potential_mrr_eur": 490,
                "delta_mrr_eur": 80,
                "months_on_current_plan": 1,
                "last_upsell_attempt_days": 3,
                "engagement_signals": 1.0,
                "decision_maker_access": False,
                "upsell_probability": 10,
                # patterns: (none dominant — brand new client)
            },
        ]

        result: list[dict[str, Any]] = []
        for opp in raw:
            composite = self._composite(
                upsell_probability=opp["upsell_probability"],
                delta_mrr_eur=opp["delta_mrr_eur"],
                engagement_signals=opp["engagement_signals"],
                months_on_current_plan=opp["months_on_current_plan"],
            )
            result.append(
                {
                    "id": opp["id"],
                    "client_name": opp["client_name"],
                    "sector": opp["sector"],
                    "current_plan": opp["current_plan"],
                    "current_mrr_eur": opp["current_mrr_eur"],
                    "recommended_upgrade": opp["recommended_upgrade"],
                    "potential_mrr_eur": opp["potential_mrr_eur"],
                    "delta_mrr_eur": opp["delta_mrr_eur"],
                    "months_on_current_plan": opp["months_on_current_plan"],
                    "last_upsell_attempt_days": opp["last_upsell_attempt_days"],
                    "engagement_signals": opp["engagement_signals"],
                    "decision_maker_access": opp["decision_maker_access"],
                    "upsell_probability": opp["upsell_probability"],
                    "composite_score": composite,
                    "risk_level": self._risk(composite),
                }
            )
        return result

    # ── public API ────────────────────────────────────────────────────────────

    def get_opportunities(self) -> list[dict[str, Any]]:
        """Return the 8 mock client opportunity dicts (15 keys each)."""
        return self._build_opportunities()

    def to_dict(self, opportunity: dict[str, Any]) -> dict[str, Any]:
        """Return opportunity with exactly 15 keys (identity, for protocol compliance)."""
        return {
            "id": opportunity["id"],
            "client_name": opportunity["client_name"],
            "sector": opportunity["sector"],
            "current_plan": opportunity["current_plan"],
            "current_mrr_eur": opportunity["current_mrr_eur"],
            "recommended_upgrade": opportunity["recommended_upgrade"],
            "potential_mrr_eur": opportunity["potential_mrr_eur"],
            "delta_mrr_eur": opportunity["delta_mrr_eur"],
            "months_on_current_plan": opportunity["months_on_current_plan"],
            "last_upsell_attempt_days": opportunity["last_upsell_attempt_days"],
            "engagement_signals": opportunity["engagement_signals"],
            "decision_maker_access": opportunity["decision_maker_access"],
            "upsell_probability": opportunity["upsell_probability"],
            "composite_score": opportunity["composite_score"],
            "risk_level": opportunity["risk_level"],
        }

    def summary(self) -> dict[str, Any]:
        """
        Return summary with exactly 13 keys:
          total_opportunities, avg_current_mrr, avg_potential_mrr,
          total_delta_mrr, opps_critique, opps_eleve, opps_modere,
          opps_faible, top_opportunity_client, top_opportunity_score,
          patterns_detected, avg_composite, avg_estimated_upsell_index
        """
        opps = self._build_opportunities()
        n = len(opps)

        avg_current_mrr = round(sum(o["current_mrr_eur"] for o in opps) / n, 2)
        avg_potential_mrr = round(sum(o["potential_mrr_eur"] for o in opps) / n, 2)
        total_delta_mrr = sum(o["delta_mrr_eur"] for o in opps)
        avg_composite = round(sum(o["composite_score"] for o in opps) / n, 2)

        levels = [o["risk_level"] for o in opps]
        opps_critique = levels.count("critique")
        opps_eleve = levels.count("élevé")
        opps_modere = levels.count("modéré")
        opps_faible = levels.count("faible")

        top = max(opps, key=lambda o: o["composite_score"])

        avg_estimated_upsell_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_opportunities": n,
            "avg_current_mrr": avg_current_mrr,
            "avg_potential_mrr": avg_potential_mrr,
            "total_delta_mrr": total_delta_mrr,
            "opps_critique": opps_critique,
            "opps_eleve": opps_eleve,
            "opps_modere": opps_modere,
            "opps_faible": opps_faible,
            "top_opportunity_client": top["client_name"],
            "top_opportunity_score": top["composite_score"],
            "patterns_detected": UPSELL_PATTERNS,
            "avg_composite": avg_composite,
            "avg_estimated_upsell_index": avg_estimated_upsell_index,
        }
