from dataclasses import dataclass
from typing import List


@dataclass
class FractionalAssetInput:
    asset_id: str
    asset_category: str  # real_estate_token/art_nft/infrastructure_share/patent_royalty/sports_contract/music_rights/carbon_credit/data_cooperative
    region: str
    liquidity_fragmentation_risk: float
    ownership_concentration_index: float
    governance_token_participation: float
    revenue_distribution_efficiency: float
    smart_contract_audit_score: float
    fractional_valuation_accuracy: float
    secondary_market_depth: float
    holder_churn_rate: float  # higher = worse
    regulatory_tokenization_clarity: float
    custody_risk_score: float  # higher = worse
    cross_border_transfer_friction: float
    dividend_payment_reliability: float
    oracle_price_accuracy: float
    community_governance_health: float
    exit_mechanism_robustness: float
    fractional_liquidity_pool_depth: float
    token_utility_score: float


class FractionalOwnershipEngine:
    # ---------- sub-score helpers ----------

    @staticmethod
    def _liquidity_score(a: FractionalAssetInput) -> float:
        """Weight 0.30 — fragmentation risk (direct), secondary depth (inv), pool depth (inv)."""
        raw = (
            a.liquidity_fragmentation_risk * 0.40
            + (1.0 - a.secondary_market_depth) * 0.35
            + (1.0 - a.fractional_liquidity_pool_depth) * 0.25
        )
        return round(min(raw * 100, 100), 2)

    @staticmethod
    def _governance_score(a: FractionalAssetInput) -> float:
        """Weight 0.25 — participation (inv), community health (inv), concentration (direct)."""
        raw = (
            (1.0 - a.governance_token_participation) * 0.40
            + (1.0 - a.community_governance_health) * 0.35
            + a.ownership_concentration_index * 0.25
        )
        return round(min(raw * 100, 100), 2)

    @staticmethod
    def _trust_score(a: FractionalAssetInput) -> float:
        """Weight 0.25 — audit score (inv), oracle accuracy (inv), custody risk (direct)."""
        raw = (
            (1.0 - a.smart_contract_audit_score) * 0.40
            + (1.0 - a.oracle_price_accuracy) * 0.35
            + a.custody_risk_score * 0.25
        )
        return round(min(raw * 100, 100), 2)

    @staticmethod
    def _compliance_score(a: FractionalAssetInput) -> float:
        """Weight 0.20 — clarity (inv), friction (direct), exit robustness (inv)."""
        raw = (
            (1.0 - a.regulatory_tokenization_clarity) * 0.40
            + a.cross_border_transfer_friction * 0.35
            + (1.0 - a.exit_mechanism_robustness) * 0.25
        )
        return round(min(raw * 100, 100), 2)

    @staticmethod
    def _composite(liq: float, gov: float, tru: float, comp: float) -> float:
        return round(min(liq * 0.30 + gov * 0.25 + tru * 0.25 + comp * 0.20, 100), 2)

    # ---------- classification helpers ----------

    @staticmethod
    def _pattern(a: FractionalAssetInput) -> str:
        if a.liquidity_fragmentation_risk >= 0.70 and a.fractional_liquidity_pool_depth <= 0.30:
            return "liquidity_freeze"
        if a.ownership_concentration_index >= 0.70 and a.governance_token_participation <= 0.30:
            return "governance_capture"
        if a.oracle_price_accuracy <= 0.30 and a.fractional_valuation_accuracy <= 0.35:
            return "oracle_manipulation"
        if a.regulatory_tokenization_clarity <= 0.30 or a.cross_border_transfer_friction >= 0.70:
            return "regulatory_block"
        if a.holder_churn_rate >= 0.70 and a.secondary_market_depth <= 0.35:
            return "holder_exodus"
        return "none"

    @staticmethod
    def _risk(c: float) -> str:
        if c >= 60:
            return "critical"
        if c >= 40:
            return "high"
        if c >= 20:
            return "moderate"
        return "low"

    @staticmethod
    def _severity(c: float) -> str:
        if c >= 60:
            return "frozen"
        if c >= 40:
            return "illiquid"
        if c >= 20:
            return "maturing"
        return "liquid"

    @staticmethod
    def _action(risk: str, pattern: str) -> str:
        if risk == "critical":
            if pattern in ("liquidity_freeze", "holder_exodus"):
                return "emergency_liquidity"
            return "governance_reset"
        if risk == "high":
            if pattern in ("governance_capture",):
                return "governance_reset"
            if pattern in ("regulatory_block",):
                return "compliance_sprint"
            return "market_deepening"
        if risk == "moderate":
            return "token_monitoring"
        return "no_action"

    @staticmethod
    def _signal(a: FractionalAssetInput, pattern: str, composite: float) -> str:
        if composite < 20:
            return (
                "Actif fractionné en excellente santé — liquidité profonde, gouvernance décentralisée, "
                "conformité réglementaire assurée, oracles fiables"
            )
        labels: dict[str, str] = {
            "liquidity_freeze": "Gel de liquidité",
            "governance_capture": "Capture de gouvernance",
            "oracle_manipulation": "Manipulation d'oracle",
            "regulatory_block": "Blocage réglementaire",
            "holder_exodus": "Exode des détenteurs",
        }
        label = labels.get(pattern, pattern.replace("_", " "))
        return (
            f"{label} — fragmentation liquidité {a.liquidity_fragmentation_risk:.2f} — "
            f"profondeur marché {a.secondary_market_depth:.2f} — "
            f"participation gouvernance {a.governance_token_participation:.2f} — "
            f"clarté réglementaire {a.regulatory_tokenization_clarity:.2f} — "
            f"composite {round(composite)}"
        )

    # ---------- public API ----------

    def assess(self, a: FractionalAssetInput) -> dict:
        liq  = self._liquidity_score(a)
        gov  = self._governance_score(a)
        tru  = self._trust_score(a)
        comp = self._compliance_score(a)
        composite = self._composite(liq, gov, tru, comp)
        pattern   = self._pattern(a)
        risk      = self._risk(composite)
        severity  = self._severity(composite)
        action    = self._action(risk, pattern)
        sig       = self._signal(a, pattern, composite)
        illiquidity_index = round(
            min(composite / 100 * (1 - a.fractional_liquidity_pool_depth + 0.01) * 10, 10.0), 2
        )
        return self.to_dict(
            a, liq, gov, tru, comp, composite, pattern, risk, severity, action, sig,
            illiquidity_index,
        )

    @staticmethod
    def to_dict(
        a: FractionalAssetInput,
        liquidity_score: float,
        governance_score: float,
        trust_score: float,
        compliance_score: float,
        fractional_composite: float,
        ownership_pattern: str,
        ownership_risk: str,
        ownership_severity: str,
        recommended_action: str,
        ownership_signal: str,
        estimated_illiquidity_index: float,
    ) -> dict:
        # exactly 15 keys
        return {
            "asset_id":                   a.asset_id,
            "asset_category":             a.asset_category,
            "region":                     a.region,
            "ownership_risk":             ownership_risk,
            "ownership_pattern":          ownership_pattern,
            "ownership_severity":         ownership_severity,
            "recommended_action":         recommended_action,
            "liquidity_score":            liquidity_score,
            "governance_score":           governance_score,
            "trust_score":                trust_score,
            "compliance_score":           compliance_score,
            "fractional_composite":       fractional_composite,
            "has_freeze_signal":          fractional_composite >= 40 or a.liquidity_fragmentation_risk >= 0.60,
            "estimated_illiquidity_index": estimated_illiquidity_index,
            "ownership_signal":           ownership_signal,
        }

    def assess_batch(self, assets: List[FractionalAssetInput]) -> List[dict]:
        return [self.assess(a) for a in assets]

    def summary(self, results: List[dict]) -> dict:
        # exactly 13 keys
        n = len(results) or 1
        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_composite   = 0.0
        total_liq         = 0.0
        total_gov         = 0.0
        total_tru         = 0.0
        total_comp        = 0.0
        freeze_count      = 0
        total_illiquidity = 0.0

        for r in results:
            risk_counts[r["ownership_risk"]]         = risk_counts.get(r["ownership_risk"], 0) + 1
            pattern_counts[r["ownership_pattern"]]   = pattern_counts.get(r["ownership_pattern"], 0) + 1
            severity_counts[r["ownership_severity"]] = severity_counts.get(r["ownership_severity"], 0) + 1
            action_counts[r["recommended_action"]]   = action_counts.get(r["recommended_action"], 0) + 1
            total_composite   += r["fractional_composite"]
            total_liq         += r["liquidity_score"]
            total_gov         += r["governance_score"]
            total_tru         += r["trust_score"]
            total_comp        += r["compliance_score"]
            total_illiquidity += r["estimated_illiquidity_index"]
            if r["has_freeze_signal"]:
                freeze_count += 1

        return {
            "total":                        len(results),
            "risk_counts":                  risk_counts,
            "pattern_counts":               pattern_counts,
            "severity_counts":              severity_counts,
            "action_counts":                action_counts,
            "avg_fractional_composite":     round(total_composite / n, 1),
            "freeze_signal_count":          freeze_count,
            "avg_liquidity_score":          round(total_liq / n, 1),
            "avg_governance_score":         round(total_gov / n, 1),
            "avg_trust_score":              round(total_tru / n, 1),
            "avg_compliance_score":         round(total_comp / n, 1),
            "avg_estimated_illiquidity_index": round(total_illiquidity / n, 2),
            "emergency_action_count":       sum(
                1 for r in results if r["recommended_action"] in ("emergency_liquidity", "governance_reset")
            ),
        }
