"""Synthetic Asset Liquidation Engine — monitors synthetic asset portfolios,
DeFi liquidation risks, collateral health, and decentralized protocol exposure
across tokenized debt, collateralized derivatives, liquidity pools, and more."""

from __future__ import annotations

import dataclasses
from enum import Enum


class LiquidationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class LiquidationPattern(str, Enum):
    none                = "none"
    collateral_cascade  = "collateral_cascade"
    oracle_attack       = "oracle_attack"
    liquidity_crunch    = "liquidity_crunch"
    protocol_exploit    = "protocol_exploit"
    peg_destabilization = "peg_destabilization"


class LiquidationSeverity(str, Enum):
    secured    = "secured"
    monitored  = "monitored"
    at_risk    = "at_risk"
    liquidating = "liquidating"


class LiquidationAction(str, Enum):
    no_action                = "no_action"
    defi_monitoring          = "defi_monitoring"
    risk_rebalancing         = "risk_rebalancing"
    oracle_diversification   = "oracle_diversification"
    liquidity_reinforcement  = "liquidity_reinforcement"
    emergency_deleveraging   = "emergency_deleveraging"
    collateral_injection     = "collateral_injection"
    protocol_pause           = "protocol_pause"


@dataclasses.dataclass
class SyntheticAssetInput:
    portfolio_id:                  str
    asset_class:                   str   # synthetic_equity / tokenized_debt / collateralized_derivative /
                                         # liquidity_pool / structured_product / algorithmic_stablecoin /
                                         # yield_vault / cross_chain_bridge
    region:                        str
    # 17 numeric fields (0.0 – 1.0)
    collateral_health_ratio:       float
    liquidation_threshold_proximity: float
    counterparty_default_risk:     float
    smart_contract_audit_score:    float
    protocol_liquidity_depth:      float
    oracle_manipulation_risk:      float
    slippage_exposure:             float
    impermanent_loss_risk:         float
    governance_attack_surface:     float
    cross_chain_bridge_risk:       float
    flash_loan_vulnerability:      float
    regulatory_seizure_risk:       float
    defi_protocol_concentration:   float
    synthetic_peg_stability:       float
    on_chain_transparency_score:   float
    insurance_coverage_ratio:      float
    exit_liquidity_score:          float


@dataclasses.dataclass
class SyntheticAssetResult:
    portfolio_id:                     str
    asset_class:                      str
    region:                           str
    liquidation_risk:                 LiquidationRisk
    liquidation_pattern:              LiquidationPattern
    liquidation_severity:             LiquidationSeverity
    recommended_action:               LiquidationAction
    collateral_score:                 float
    protocol_score:                   float
    liquidity_score:                  float
    systemic_score:                   float
    liquidation_composite:            float
    is_liquidation_imminent:          bool
    requires_collateral_top_up:       bool
    estimated_liquidation_risk_index: float
    liquidation_signal:               str

    def to_dict(self) -> dict:
        return {
            "portfolio_id":                     self.portfolio_id,
            "region":                           self.region,
            "liquidation_risk":                 self.liquidation_risk.value,
            "liquidation_pattern":              self.liquidation_pattern.value,
            "liquidation_severity":             self.liquidation_severity.value,
            "recommended_action":               self.recommended_action.value,
            "collateral_score":                 round(self.collateral_score, 1),
            "protocol_score":                   round(self.protocol_score, 1),
            "liquidity_score":                  round(self.liquidity_score, 1),
            "systemic_score":                   round(self.systemic_score, 1),
            "liquidation_composite":            round(self.liquidation_composite, 1),
            "is_liquidation_imminent":          self.is_liquidation_imminent,
            "requires_collateral_top_up":       self.requires_collateral_top_up,
            "estimated_liquidation_risk_index": round(self.estimated_liquidation_risk_index, 2),
            "liquidation_signal":               self.liquidation_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SyntheticAssetLiquidationEngine:
    """Assesses synthetic asset portfolios for DeFi liquidation risk, collateral
    health, and decentralized protocol exposure."""

    def __init__(self) -> None:
        self._results: list[SyntheticAssetResult] = []

    # ── sub-scores (HIGHER = more risk) ─────────────────────────────────────

    def _collateral_score(self, inp: SyntheticAssetInput) -> float:
        """Weight 0.30 — collateral health (inverted), liquidation proximity, counterparty default."""
        s = 0.0
        # collateral_health_ratio inverted: low ratio → high risk
        if inp.collateral_health_ratio <= 0.20:
            s += 40.0
        elif inp.collateral_health_ratio <= 0.40:
            s += 25.0
        elif inp.collateral_health_ratio <= 0.60:
            s += 10.0
        # liquidation_threshold_proximity: high value → near threshold → high risk
        if inp.liquidation_threshold_proximity >= 0.80:
            s += 35.0
        elif inp.liquidation_threshold_proximity >= 0.60:
            s += 20.0
        elif inp.liquidation_threshold_proximity >= 0.40:
            s += 8.0
        # counterparty_default_risk
        if inp.counterparty_default_risk >= 0.70:
            s += 25.0
        elif inp.counterparty_default_risk >= 0.50:
            s += 14.0
        elif inp.counterparty_default_risk >= 0.30:
            s += 5.0
        return _clamp(s)

    def _protocol_score(self, inp: SyntheticAssetInput) -> float:
        """Weight 0.25 — audit score (inverted), oracle manipulation, flash loan vulnerability."""
        s = 0.0
        # smart_contract_audit_score inverted: low score → high risk
        if inp.smart_contract_audit_score <= 0.20:
            s += 40.0
        elif inp.smart_contract_audit_score <= 0.45:
            s += 24.0
        elif inp.smart_contract_audit_score <= 0.65:
            s += 10.0
        # oracle_manipulation_risk
        if inp.oracle_manipulation_risk >= 0.70:
            s += 35.0
        elif inp.oracle_manipulation_risk >= 0.50:
            s += 20.0
        elif inp.oracle_manipulation_risk >= 0.30:
            s += 8.0
        # flash_loan_vulnerability
        if inp.flash_loan_vulnerability >= 0.65:
            s += 25.0
        elif inp.flash_loan_vulnerability >= 0.45:
            s += 14.0
        elif inp.flash_loan_vulnerability >= 0.25:
            s += 5.0
        return _clamp(s)

    def _liquidity_score(self, inp: SyntheticAssetInput) -> float:
        """Weight 0.25 — liquidity depth (inverted), slippage exposure, exit liquidity (inverted)."""
        s = 0.0
        # protocol_liquidity_depth inverted: low depth → high risk
        if inp.protocol_liquidity_depth <= 0.20:
            s += 40.0
        elif inp.protocol_liquidity_depth <= 0.40:
            s += 25.0
        elif inp.protocol_liquidity_depth <= 0.60:
            s += 10.0
        # slippage_exposure
        if inp.slippage_exposure >= 0.70:
            s += 35.0
        elif inp.slippage_exposure >= 0.50:
            s += 20.0
        elif inp.slippage_exposure >= 0.30:
            s += 8.0
        # exit_liquidity_score inverted: low score → high risk
        if inp.exit_liquidity_score <= 0.20:
            s += 25.0
        elif inp.exit_liquidity_score <= 0.45:
            s += 14.0
        elif inp.exit_liquidity_score <= 0.65:
            s += 5.0
        return _clamp(s)

    def _systemic_score(self, inp: SyntheticAssetInput) -> float:
        """Weight 0.20 — DeFi concentration, cross-chain bridge risk, regulatory seizure."""
        s = 0.0
        # defi_protocol_concentration
        if inp.defi_protocol_concentration >= 0.75:
            s += 40.0
        elif inp.defi_protocol_concentration >= 0.55:
            s += 24.0
        elif inp.defi_protocol_concentration >= 0.35:
            s += 10.0
        # cross_chain_bridge_risk
        if inp.cross_chain_bridge_risk >= 0.70:
            s += 35.0
        elif inp.cross_chain_bridge_risk >= 0.50:
            s += 20.0
        elif inp.cross_chain_bridge_risk >= 0.30:
            s += 8.0
        # regulatory_seizure_risk
        if inp.regulatory_seizure_risk >= 0.65:
            s += 25.0
        elif inp.regulatory_seizure_risk >= 0.45:
            s += 14.0
        elif inp.regulatory_seizure_risk >= 0.25:
            s += 5.0
        return _clamp(s)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> LiquidationRisk:
        if composite >= 60:
            return LiquidationRisk.critical
        if composite >= 40:
            return LiquidationRisk.high
        if composite >= 20:
            return LiquidationRisk.moderate
        return LiquidationRisk.low

    def _classify_severity(self, composite: float) -> LiquidationSeverity:
        if composite >= 60:
            return LiquidationSeverity.liquidating
        if composite >= 40:
            return LiquidationSeverity.at_risk
        if composite >= 20:
            return LiquidationSeverity.monitored
        return LiquidationSeverity.secured

    def _classify_pattern(
        self,
        inp: SyntheticAssetInput,
        col: float,
        prot: float,
        liq: float,
        sys: float,
    ) -> LiquidationPattern:
        if inp.collateral_health_ratio <= 0.25 and inp.liquidation_threshold_proximity >= 0.70:
            return LiquidationPattern.collateral_cascade
        if inp.oracle_manipulation_risk >= 0.65 or inp.flash_loan_vulnerability >= 0.65:
            return LiquidationPattern.oracle_attack
        if inp.protocol_liquidity_depth <= 0.25 and inp.slippage_exposure >= 0.60:
            return LiquidationPattern.liquidity_crunch
        if inp.smart_contract_audit_score <= 0.30 and prot >= 35:
            return LiquidationPattern.protocol_exploit
        if inp.synthetic_peg_stability <= 0.30 and inp.asset_class in (
            "algorithmic_stablecoin", "collateralized_derivative", "structured_product"
        ):
            return LiquidationPattern.peg_destabilization
        return LiquidationPattern.none

    def _recommended_action(
        self, risk: LiquidationRisk, pattern: LiquidationPattern
    ) -> LiquidationAction:
        if risk == LiquidationRisk.critical:
            if pattern == LiquidationPattern.collateral_cascade:
                return LiquidationAction.emergency_deleveraging
            if pattern == LiquidationPattern.protocol_exploit:
                return LiquidationAction.protocol_pause
            return LiquidationAction.collateral_injection
        if risk == LiquidationRisk.high:
            if pattern == LiquidationPattern.oracle_attack:
                return LiquidationAction.oracle_diversification
            if pattern == LiquidationPattern.liquidity_crunch:
                return LiquidationAction.liquidity_reinforcement
            return LiquidationAction.risk_rebalancing
        if risk == LiquidationRisk.moderate:
            return LiquidationAction.defi_monitoring
        return LiquidationAction.no_action

    def _signal(
        self,
        inp: SyntheticAssetInput,
        pattern: LiquidationPattern,
        composite: float,
    ) -> str:
        if composite < 20:
            return (
                "Portefeuille synthétique sécurisé — ratio collatéral sain, "
                "protocoles audités, liquidité DeFi suffisante"
            )
        labels: dict[str, str] = {
            "collateral_cascade":  "Cascade de collatéral",
            "oracle_attack":       "Attaque oracle",
            "liquidity_crunch":    "Crise de liquidité",
            "protocol_exploit":    "Exploit protocole",
            "peg_destabilization": "Déstabilisation du peg",
        }
        label = labels.get(pattern.value, pattern.value.replace("_", " "))
        return (
            f"{label} — collatéral {inp.collateral_health_ratio:.2f} "
            f"(seuil liq. {inp.liquidation_threshold_proximity:.2f}) "
            f"— oracle risk {inp.oracle_manipulation_risk:.2f} "
            f"— liquidité {inp.protocol_liquidity_depth:.2f} "
            f"— composite {composite:.0f}"
        )

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: SyntheticAssetInput) -> SyntheticAssetResult:
        col  = self._collateral_score(inp)
        prot = self._protocol_score(inp)
        liq  = self._liquidity_score(inp)
        sys  = self._systemic_score(inp)

        composite = _clamp(
            col  * 0.30
            + prot * 0.25
            + liq  * 0.25
            + sys  * 0.20
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp, col, prot, liq, sys)
        action   = self._recommended_action(risk, pattern)

        is_liquidation_imminent = (
            composite >= 60
            or inp.collateral_health_ratio <= 0.15
            or inp.liquidation_threshold_proximity >= 0.90
        )
        requires_collateral_top_up = (
            composite >= 40
            or inp.collateral_health_ratio <= 0.35
            or inp.liquidation_threshold_proximity >= 0.65
        )

        estimated_liquidation_risk_index = round(
            min((composite / 100.0) * (1.0 - inp.insurance_coverage_ratio + 0.01) * 10.0, 10.0),
            2,
        )

        result = SyntheticAssetResult(
            portfolio_id=inp.portfolio_id,
            asset_class=inp.asset_class,
            region=inp.region,
            liquidation_risk=risk,
            liquidation_pattern=pattern,
            liquidation_severity=severity,
            recommended_action=action,
            collateral_score=col,
            protocol_score=prot,
            liquidity_score=liq,
            systemic_score=sys,
            liquidation_composite=composite,
            is_liquidation_imminent=is_liquidation_imminent,
            requires_collateral_top_up=requires_collateral_top_up,
            estimated_liquidation_risk_index=estimated_liquidation_risk_index,
            liquidation_signal=self._signal(inp, pattern, composite),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[SyntheticAssetInput]
    ) -> list[SyntheticAssetResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                              0,
                "risk_counts":                        {},
                "pattern_counts":                     {},
                "severity_counts":                    {},
                "action_counts":                      {},
                "avg_liquidation_composite":          0.0,
                "liquidation_imminent_count":         0,
                "collateral_top_up_count":            0,
                "avg_collateral_score":               0.0,
                "avg_protocol_score":                 0.0,
                "avg_liquidity_score":                0.0,
                "avg_systemic_score":                 0.0,
                "avg_estimated_liquidation_risk_index": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_col = total_prot = total_liq = total_sys = total_idx = 0.0
        imminent = top_up = 0

        for r in self._results:
            risk_counts[r.liquidation_risk.value]       = risk_counts.get(r.liquidation_risk.value, 0) + 1
            pattern_counts[r.liquidation_pattern.value] = pattern_counts.get(r.liquidation_pattern.value, 0) + 1
            severity_counts[r.liquidation_severity.value] = severity_counts.get(r.liquidation_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.liquidation_composite
            total_col  += r.collateral_score
            total_prot += r.protocol_score
            total_liq  += r.liquidity_score
            total_sys  += r.systemic_score
            total_idx  += r.estimated_liquidation_risk_index
            if r.is_liquidation_imminent:
                imminent += 1
            if r.requires_collateral_top_up:
                top_up += 1

        n = len(self._results)
        return {
            "total":                              n,
            "risk_counts":                        risk_counts,
            "pattern_counts":                     pattern_counts,
            "severity_counts":                    severity_counts,
            "action_counts":                      action_counts,
            "avg_liquidation_composite":          round(total_comp / n, 1),
            "liquidation_imminent_count":         imminent,
            "collateral_top_up_count":            top_up,
            "avg_collateral_score":               round(total_col  / n, 1),
            "avg_protocol_score":                 round(total_prot / n, 1),
            "avg_liquidity_score":                round(total_liq  / n, 1),
            "avg_systemic_score":                 round(total_sys  / n, 1),
            "avg_estimated_liquidation_risk_index": round(total_idx / n, 2),
        }
