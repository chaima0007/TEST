"""
Module 250 — Singularity Economy & Post-Rare Asset Valuation Engine
Monitors economic assets in post-scarcity and post-rare contexts — digital twins,
synthetic commodities, attention tokens, AI-generated IP, quantum-encrypted assets —
assessing valuation dynamics, singularity readiness, and market disruption potential.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class EconomyRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class EconomyPattern(str, Enum):
    none                 = "none"
    speculative_bubble   = "speculative_bubble"
    regulatory_collapse  = "regulatory_collapse"
    liquidity_crisis     = "liquidity_crisis"
    value_evaporation    = "value_evaporation"
    paradigm_displacement = "paradigm_displacement"


class EconomySeverity(str, Enum):
    stable      = "stable"
    speculative = "speculative"
    volatile    = "volatile"
    bubble      = "bubble"


class EconomyAction(str, Enum):
    no_action                = "no_action"
    valuation_monitoring     = "valuation_monitoring"
    portfolio_rebalancing    = "portfolio_rebalancing"
    risk_hedging             = "risk_hedging"
    emergency_liquidation    = "emergency_liquidation"
    regulatory_intervention  = "regulatory_intervention"


@dataclass
class AssetInput:
    asset_id: str
    asset_class: str                  # digital_twin/synthetic_commodity/attention_token/ai_generated_ip/quantum_asset/post_rare_material/consciousness_token/data_sovereignty
    region: str
    scarcity_index: float             # 0=infinite supply, 1=extremely scarce
    valuation_volatility: float       # higher=worse
    singularity_readiness_score: float
    ai_creation_rate: float           # pace of AI-generated competing assets
    network_effect_strength: float
    token_liquidity_score: float
    regulatory_uncertainty: float     # higher=worse
    post_rare_transition_score: float
    value_store_resilience: float
    market_manipulation_risk: float   # higher=worse
    consensus_legitimacy_score: float
    speculative_premium_ratio: float  # higher=riskier
    decentralization_score: float
    sovereignty_alignment: float
    quantum_security_level: float
    adoption_velocity: float
    paradigm_disruption_index: float  # higher=more disruptive


@dataclass
class AssetResult:
    asset_id: str
    asset_class: str
    region: str
    economy_risk: str
    economy_pattern: str
    economy_severity: str
    recommended_action: str
    valuation_score: float
    market_score: float
    resilience_score: float
    disruption_score: float
    singularity_composite: float
    has_bubble_signal: bool
    estimated_bubble_risk_index: float
    economy_signal: str

    def to_dict(self) -> Dict:
        return {
            "asset_id":                    self.asset_id,
            "asset_class":                 self.asset_class,
            "region":                      self.region,
            "economy_risk":                self.economy_risk,
            "economy_pattern":             self.economy_pattern,
            "economy_severity":            self.economy_severity,
            "recommended_action":          self.recommended_action,
            "valuation_score":             self.valuation_score,
            "market_score":                self.market_score,
            "resilience_score":            self.resilience_score,
            "disruption_score":            self.disruption_score,
            "singularity_composite":       self.singularity_composite,
            "has_bubble_signal":           self.has_bubble_signal,
            "estimated_bubble_risk_index": self.estimated_bubble_risk_index,
            "economy_signal":              self.economy_signal,
        }


class SingularityEconomyEngine:
    def __init__(self) -> None:
        self._results: List[AssetResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _valuation_score(self, i: AssetInput) -> float:
        s = 0
        # valuation_volatility inverted (high=worse → high score)
        if   i.valuation_volatility >= 0.75: s += 40
        elif i.valuation_volatility >= 0.55: s += 22
        elif i.valuation_volatility >= 0.35: s += 8
        # speculative_premium_ratio inverted (high=riskier → high score)
        if   i.speculative_premium_ratio >= 0.70: s += 35
        elif i.speculative_premium_ratio >= 0.50: s += 18
        elif i.speculative_premium_ratio >= 0.30: s += 6
        # scarcity_index (high=scarce → contributes to valuation distortion)
        if   i.scarcity_index >= 0.75: s += 25
        elif i.scarcity_index >= 0.50: s += 12
        return min(s, 100)

    def _market_score(self, i: AssetInput) -> float:
        s = 0
        # market_manipulation_risk inverted
        if   i.market_manipulation_risk >= 0.70: s += 40
        elif i.market_manipulation_risk >= 0.50: s += 22
        elif i.market_manipulation_risk >= 0.30: s += 8
        # regulatory_uncertainty inverted
        if   i.regulatory_uncertainty >= 0.70: s += 35
        elif i.regulatory_uncertainty >= 0.50: s += 18
        elif i.regulatory_uncertainty >= 0.30: s += 6
        # token_liquidity_score inverted (low liquidity = high risk)
        if   i.token_liquidity_score <= 0.25: s += 25
        elif i.token_liquidity_score <= 0.50: s += 12
        return min(s, 100)

    def _resilience_score(self, i: AssetInput) -> float:
        s = 0
        # value_store_resilience inverted (low=worse)
        if   i.value_store_resilience <= 0.25: s += 40
        elif i.value_store_resilience <= 0.50: s += 22
        elif i.value_store_resilience <= 0.70: s += 8
        # quantum_security_level inverted (low=worse)
        if   i.quantum_security_level <= 0.25: s += 35
        elif i.quantum_security_level <= 0.50: s += 18
        elif i.quantum_security_level <= 0.70: s += 6
        # decentralization_score inverted (low=more centralized=riskier)
        if   i.decentralization_score <= 0.25: s += 25
        elif i.decentralization_score <= 0.50: s += 12
        return min(s, 100)

    def _disruption_score(self, i: AssetInput) -> float:
        s = 0
        # paradigm_disruption_index (high=more disruptive=destabilizing)
        if   i.paradigm_disruption_index >= 0.75: s += 40
        elif i.paradigm_disruption_index >= 0.55: s += 22
        elif i.paradigm_disruption_index >= 0.35: s += 8
        # ai_creation_rate inverted for stability (high rate = more competition = instability)
        if   i.ai_creation_rate >= 0.70: s += 35
        elif i.ai_creation_rate >= 0.50: s += 18
        elif i.ai_creation_rate >= 0.30: s += 6
        # adoption_velocity inverted (very high=speculative rush=riskier)
        if   i.adoption_velocity >= 0.75: s += 25
        elif i.adoption_velocity >= 0.55: s += 12
        return min(s, 100)

    def _composite(self, val: float, mkt: float, res: float, dis: float) -> float:
        return min(round(val * 0.30 + mkt * 0.25 + res * 0.25 + dis * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> EconomyRisk:
        if c >= 60: return EconomyRisk.critical
        if c >= 40: return EconomyRisk.high
        if c >= 20: return EconomyRisk.moderate
        return EconomyRisk.low

    def _severity(self, c: float) -> EconomySeverity:
        if c >= 60: return EconomySeverity.bubble
        if c >= 40: return EconomySeverity.volatile
        if c >= 20: return EconomySeverity.speculative
        return EconomySeverity.stable

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: AssetInput) -> EconomyPattern:
        if (i.regulatory_uncertainty >= 0.70
                and i.sovereignty_alignment < 0.30):
            return EconomyPattern.regulatory_collapse
        if (i.speculative_premium_ratio >= 0.70
                and i.consensus_legitimacy_score <= 0.35):
            return EconomyPattern.speculative_bubble
        if (i.token_liquidity_score <= 0.25
                or i.network_effect_strength <= 0.20):
            return EconomyPattern.liquidity_crisis
        if (i.value_store_resilience <= 0.25
                and i.valuation_volatility >= 0.65):
            return EconomyPattern.value_evaporation
        if (i.paradigm_disruption_index >= 0.75
                and i.ai_creation_rate >= 0.65):
            return EconomyPattern.paradigm_displacement
        return EconomyPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: EconomyRisk, pat: EconomyPattern) -> EconomyAction:
        if risk == EconomyRisk.critical:
            if pat == EconomyPattern.speculative_bubble: return EconomyAction.emergency_liquidation
            if pat == EconomyPattern.regulatory_collapse: return EconomyAction.regulatory_intervention
            return EconomyAction.emergency_liquidation
        if risk == EconomyRisk.high:
            if pat == EconomyPattern.liquidity_crisis:      return EconomyAction.portfolio_rebalancing
            if pat == EconomyPattern.value_evaporation:     return EconomyAction.risk_hedging
            if pat == EconomyPattern.paradigm_displacement: return EconomyAction.portfolio_rebalancing
            return EconomyAction.risk_hedging
        if risk == EconomyRisk.moderate:
            return EconomyAction.valuation_monitoring
        return EconomyAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived booleans & indices                                          #
    # ------------------------------------------------------------------ #

    def _has_bubble_signal(self, i: AssetInput, comp: float) -> bool:
        return (comp >= 40
                or i.speculative_premium_ratio >= 0.60
                or i.market_manipulation_risk >= 0.65
                or i.consensus_legitimacy_score <= 0.30)

    def _bubble_risk_index(self, i: AssetInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.consensus_legitimacy_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: AssetInput, pat: EconomyPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Actif post-rare stable — valorisation cohérente, marché liquide, "
                "résilience forte, singularité maîtrisée"
            )
        labels = {
            EconomyPattern.speculative_bubble:    "Bulle spéculative",
            EconomyPattern.regulatory_collapse:   "Effondrement réglementaire",
            EconomyPattern.liquidity_crisis:      "Crise de liquidité",
            EconomyPattern.value_evaporation:     "Évaporation de valeur",
            EconomyPattern.paradigm_displacement: "Déplacement paradigmatique",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — volatilité {i.valuation_volatility:.2f}"
            f" — manipulation {i.market_manipulation_risk:.2f}"
            f" — résilience {i.value_store_resilience:.2f}"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: AssetInput) -> AssetResult:
        val  = self._valuation_score(i)
        mkt  = self._market_score(i)
        res  = self._resilience_score(i)
        dis  = self._disruption_score(i)
        comp = self._composite(val, mkt, res, dis)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = AssetResult(
            asset_id=i.asset_id,
            asset_class=i.asset_class,
            region=i.region,
            economy_risk=risk.value,
            economy_pattern=pat.value,
            economy_severity=sev.value,
            recommended_action=act.value,
            valuation_score=val,
            market_score=mkt,
            resilience_score=res,
            disruption_score=dis,
            singularity_composite=comp,
            has_bubble_signal=self._has_bubble_signal(i, comp),
            estimated_bubble_risk_index=self._bubble_risk_index(i, comp),
            economy_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[AssetInput]) -> List[AssetResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_singularity_composite": 0.0,
                "bubble_alert_count": 0,
                "emergency_count": 0,
                "avg_valuation_score": 0.0,
                "avg_market_score": 0.0,
                "avg_resilience_score": 0.0,
                "avg_disruption_score": 0.0,
                "avg_estimated_bubble_risk_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tval = tmkt = tres = tdis = tcomp = tbri = 0.0
        bubble_count = emergency_count = 0
        for r in self._results:
            rc[r.economy_risk]      = rc.get(r.economy_risk, 0)      + 1
            pc[r.economy_pattern]   = pc.get(r.economy_pattern, 0)   + 1
            sc[r.economy_severity]  = sc.get(r.economy_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tval  += r.valuation_score
            tmkt  += r.market_score
            tres  += r.resilience_score
            tdis  += r.disruption_score
            tcomp += r.singularity_composite
            tbri  += r.estimated_bubble_risk_index
            if r.has_bubble_signal: bubble_count += 1
            if r.recommended_action in ("emergency_liquidation", "regulatory_intervention"):
                emergency_count += 1
        return {
            "total":                           n,
            "risk_counts":                     rc,
            "pattern_counts":                  pc,
            "severity_counts":                 sc,
            "action_counts":                   ac,
            "avg_singularity_composite":       round(tcomp / n, 1),
            "bubble_alert_count":              bubble_count,
            "emergency_count":                 emergency_count,
            "avg_valuation_score":             round(tval / n, 1),
            "avg_market_score":                round(tmkt / n, 1),
            "avg_resilience_score":            round(tres / n, 1),
            "avg_disruption_score":            round(tdis / n, 1),
            "avg_estimated_bubble_risk_index": round(tbri / n, 2),
        }


# ---------------------------------------------------------------------------
# Mock data for development / testing
# ---------------------------------------------------------------------------

MOCK_ASSETS = [
    # AS-001 digital_twin EMEA — critical speculative_bubble
    AssetInput(
        asset_id="AS-001", asset_class="digital_twin", region="EMEA",
        scarcity_index=0.85, valuation_volatility=0.88, singularity_readiness_score=0.72,
        ai_creation_rate=0.78, network_effect_strength=0.60, token_liquidity_score=0.30,
        regulatory_uncertainty=0.75, post_rare_transition_score=0.65,
        value_store_resilience=0.20, market_manipulation_risk=0.80,
        consensus_legitimacy_score=0.15, speculative_premium_ratio=0.90,
        decentralization_score=0.22, sovereignty_alignment=0.30,
        quantum_security_level=0.25, adoption_velocity=0.82, paradigm_disruption_index=0.80,
    ),
    # AS-002 synthetic_commodity NAMER — low stable
    AssetInput(
        asset_id="AS-002", asset_class="synthetic_commodity", region="NAMER",
        scarcity_index=0.30, valuation_volatility=0.18, singularity_readiness_score=0.55,
        ai_creation_rate=0.22, network_effect_strength=0.80, token_liquidity_score=0.88,
        regulatory_uncertainty=0.15, post_rare_transition_score=0.70,
        value_store_resilience=0.85, market_manipulation_risk=0.12,
        consensus_legitimacy_score=0.90, speculative_premium_ratio=0.10,
        decentralization_score=0.78, sovereignty_alignment=0.85,
        quantum_security_level=0.80, adoption_velocity=0.45, paradigm_disruption_index=0.20,
    ),
    # AS-003 attention_token APAC — high liquidity_crisis
    AssetInput(
        asset_id="AS-003", asset_class="attention_token", region="APAC",
        scarcity_index=0.55, valuation_volatility=0.62, singularity_readiness_score=0.48,
        ai_creation_rate=0.60, network_effect_strength=0.18, token_liquidity_score=0.20,
        regulatory_uncertainty=0.55, post_rare_transition_score=0.42,
        value_store_resilience=0.45, market_manipulation_risk=0.58,
        consensus_legitimacy_score=0.40, speculative_premium_ratio=0.55,
        decentralization_score=0.45, sovereignty_alignment=0.50,
        quantum_security_level=0.40, adoption_velocity=0.62, paradigm_disruption_index=0.55,
    ),
    # AS-004 ai_generated_ip LATAM — low stable
    AssetInput(
        asset_id="AS-004", asset_class="ai_generated_ip", region="LATAM",
        scarcity_index=0.20, valuation_volatility=0.15, singularity_readiness_score=0.65,
        ai_creation_rate=0.18, network_effect_strength=0.75, token_liquidity_score=0.82,
        regulatory_uncertainty=0.20, post_rare_transition_score=0.72,
        value_store_resilience=0.88, market_manipulation_risk=0.10,
        consensus_legitimacy_score=0.85, speculative_premium_ratio=0.08,
        decentralization_score=0.80, sovereignty_alignment=0.78,
        quantum_security_level=0.75, adoption_velocity=0.38, paradigm_disruption_index=0.18,
    ),
    # AS-005 quantum_asset EMEA — critical regulatory_collapse
    AssetInput(
        asset_id="AS-005", asset_class="quantum_asset", region="EMEA",
        scarcity_index=0.78, valuation_volatility=0.80, singularity_readiness_score=0.85,
        ai_creation_rate=0.55, network_effect_strength=0.40, token_liquidity_score=0.35,
        regulatory_uncertainty=0.88, post_rare_transition_score=0.55,
        value_store_resilience=0.30, market_manipulation_risk=0.70,
        consensus_legitimacy_score=0.20, speculative_premium_ratio=0.72,
        decentralization_score=0.28, sovereignty_alignment=0.18,
        quantum_security_level=0.88, adoption_velocity=0.70, paradigm_disruption_index=0.72,
    ),
    # AS-006 post_rare_material MEA — moderate speculative
    AssetInput(
        asset_id="AS-006", asset_class="post_rare_material", region="MEA",
        scarcity_index=0.50, valuation_volatility=0.45, singularity_readiness_score=0.38,
        ai_creation_rate=0.40, network_effect_strength=0.52, token_liquidity_score=0.55,
        regulatory_uncertainty=0.48, post_rare_transition_score=0.45,
        value_store_resilience=0.55, market_manipulation_risk=0.42,
        consensus_legitimacy_score=0.58, speculative_premium_ratio=0.40,
        decentralization_score=0.50, sovereignty_alignment=0.55,
        quantum_security_level=0.48, adoption_velocity=0.42, paradigm_disruption_index=0.38,
    ),
    # AS-007 consciousness_token NAMER — high value_evaporation
    AssetInput(
        asset_id="AS-007", asset_class="consciousness_token", region="NAMER",
        scarcity_index=0.70, valuation_volatility=0.72, singularity_readiness_score=0.60,
        ai_creation_rate=0.65, network_effect_strength=0.38, token_liquidity_score=0.40,
        regulatory_uncertainty=0.62, post_rare_transition_score=0.50,
        value_store_resilience=0.22, market_manipulation_risk=0.68,
        consensus_legitimacy_score=0.35, speculative_premium_ratio=0.65,
        decentralization_score=0.38, sovereignty_alignment=0.42,
        quantum_security_level=0.38, adoption_velocity=0.68, paradigm_disruption_index=0.62,
    ),
    # AS-008 data_sovereignty APAC — low stable
    AssetInput(
        asset_id="AS-008", asset_class="data_sovereignty", region="APAC",
        scarcity_index=0.25, valuation_volatility=0.20, singularity_readiness_score=0.60,
        ai_creation_rate=0.25, network_effect_strength=0.72, token_liquidity_score=0.78,
        regulatory_uncertainty=0.18, post_rare_transition_score=0.68,
        value_store_resilience=0.82, market_manipulation_risk=0.15,
        consensus_legitimacy_score=0.88, speculative_premium_ratio=0.12,
        decentralization_score=0.75, sovereignty_alignment=0.90,
        quantum_security_level=0.70, adoption_velocity=0.40, paradigm_disruption_index=0.22,
    ),
]


if __name__ == "__main__":
    engine = SingularityEconomyEngine()
    results = engine.assess_batch(MOCK_ASSETS)
    for r in results:
        d = r.to_dict()
        print(f"{d['asset_id']} | {d['economy_risk']:8s} | {d['economy_pattern']:22s} | composite={d['singularity_composite']:.1f}")
    print("\nSummary:", engine.summary())
