"""Strategic Foresight & Advanced Simulation Engine — anticipates future shocks and scenario preparedness."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ForesightRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class ScenarioPattern(str, Enum):
    NONE = "none"
    BLACK_SWAN = "black_swan"
    DISRUPTION_WAVE = "disruption_wave"
    COMPETITIVE_COLLAPSE = "competitive_collapse"
    REGULATORY_SHOCK = "regulatory_shock"
    GEOPOLITICAL_SHIFT = "geopolitical_shift"


class ForesightSeverity(str, Enum):
    PREPARED = "prepared"
    MONITORING = "monitoring"
    VULNERABLE = "vulnerable"
    BLIND_SPOT = "blind_spot"


class ForesightAction(str, Enum):
    NO_ACTION = "no_action"
    SCENARIO_MONITORING = "scenario_monitoring"
    SIGNAL_AMPLIFICATION = "signal_amplification"
    STRATEGIC_HEDGE = "strategic_hedge"
    CONTINGENCY_ACTIVATION = "contingency_activation"
    CRISIS_SIMULATION = "crisis_simulation"
    SCENARIO_REPLAN = "scenario_replan"
    STRATEGIC_PIVOT = "strategic_pivot"
    EMERGENCY_REPLAN = "emergency_replan"


@dataclass
class ForesightInput:
    scenario_id: str
    domain: str                               # technology/geopolitics/economy/climate/regulatory/social
    region: str
    signal_detection_score: float             # 0-1, 1=strong signals
    trend_alignment_score: float              # 0-1, 1=aligned
    scenario_probability: float               # 0-1
    impact_severity_if_materialized: float    # 0-1, 1=catastrophic
    time_horizon_readiness: float             # 0-1, 1=well prepared
    strategic_option_coverage: float          # 0-1, 1=all options covered
    simulation_iteration_count: int           # # of simulations run
    model_accuracy_score: float               # 0-1
    stakeholder_scenario_literacy: float      # 0-1, 1=fully literate
    competitive_scenario_advantage: float     # 0-1, 1=strong advantage
    early_warning_system_score: float         # 0-1
    adaptive_capacity_score: float            # 0-1, 1=highly adaptive
    cross_scenario_resilience: float          # 0-1
    black_swan_preparedness: float            # 0-1, 1=prepared
    geopolitical_exposure_score: float        # 0-1, 1=highly exposed
    technology_disruption_readiness: float    # 0-1, 1=ready
    resource_scenario_buffer_pct: float       # 0-1, 1=ample buffer


@dataclass
class ForesightResult:
    scenario_id: str
    region: str
    foresight_risk: ForesightRisk
    scenario_pattern: ScenarioPattern
    foresight_severity: ForesightSeverity
    recommended_action: ForesightAction
    signal_score: float
    readiness_score: float
    simulation_score: float
    exposure_score: float
    foresight_composite: float
    has_blind_spot_risk: bool
    requires_immediate_simulation: bool
    estimated_scenario_risk_index: float      # 0-10
    foresight_signal: str

    def to_dict(self) -> dict:
        return {
            "scenario_id": self.scenario_id,
            "region": self.region,
            "foresight_risk": self.foresight_risk.value,
            "scenario_pattern": self.scenario_pattern.value,
            "foresight_severity": self.foresight_severity.value,
            "recommended_action": self.recommended_action.value,
            "signal_score": self.signal_score,
            "readiness_score": self.readiness_score,
            "simulation_score": self.simulation_score,
            "exposure_score": self.exposure_score,
            "foresight_composite": self.foresight_composite,
            "has_blind_spot_risk": self.has_blind_spot_risk,
            "requires_immediate_simulation": self.requires_immediate_simulation,
            "estimated_scenario_risk_index": self.estimated_scenario_risk_index,
            "foresight_signal": self.foresight_signal,
        }


# ── sub-score calculators ─────────────────────────────────────────────────────

def _signal_score(inp: ForesightInput) -> float:
    """0.30 weight — penalize low signal_detection_score, low trend_alignment_score, low early_warning_system_score."""
    score = 0.0
    if inp.signal_detection_score <= 0.25:
        score += 45
    elif inp.signal_detection_score <= 0.50:
        score += 25
    elif inp.signal_detection_score <= 0.70:
        score += 10
    if inp.trend_alignment_score <= 0.25:
        score += 35
    elif inp.trend_alignment_score <= 0.50:
        score += 18
    elif inp.trend_alignment_score <= 0.70:
        score += 7
    if inp.early_warning_system_score <= 0.25:
        score += 20
    elif inp.early_warning_system_score <= 0.50:
        score += 10
    elif inp.early_warning_system_score <= 0.70:
        score += 4
    return round(min(score, 100.0), 2)


def _readiness_score(inp: ForesightInput) -> float:
    """0.25 weight — penalize low time_horizon_readiness, low strategic_option_coverage, low adaptive_capacity_score."""
    score = 0.0
    if inp.time_horizon_readiness <= 0.25:
        score += 40
    elif inp.time_horizon_readiness <= 0.50:
        score += 22
    elif inp.time_horizon_readiness <= 0.70:
        score += 9
    if inp.strategic_option_coverage <= 0.25:
        score += 35
    elif inp.strategic_option_coverage <= 0.50:
        score += 18
    elif inp.strategic_option_coverage <= 0.70:
        score += 7
    if inp.adaptive_capacity_score <= 0.25:
        score += 25
    elif inp.adaptive_capacity_score <= 0.50:
        score += 12
    elif inp.adaptive_capacity_score <= 0.70:
        score += 5
    return round(min(score, 100.0), 2)


def _simulation_score(inp: ForesightInput) -> float:
    """0.25 weight — penalize low simulation_iteration_count (scaled 0-100), low model_accuracy_score, low black_swan_preparedness."""
    score = 0.0
    # simulation_iteration_count: 0..100 scaled; 0 iters = worst
    iter_scaled = min(inp.simulation_iteration_count, 100) / 100.0
    if iter_scaled <= 0.10:
        score += 40
    elif iter_scaled <= 0.30:
        score += 22
    elif iter_scaled <= 0.60:
        score += 9
    if inp.model_accuracy_score <= 0.25:
        score += 35
    elif inp.model_accuracy_score <= 0.50:
        score += 18
    elif inp.model_accuracy_score <= 0.70:
        score += 7
    if inp.black_swan_preparedness <= 0.25:
        score += 25
    elif inp.black_swan_preparedness <= 0.50:
        score += 12
    elif inp.black_swan_preparedness <= 0.70:
        score += 5
    return round(min(score, 100.0), 2)


def _exposure_score(inp: ForesightInput) -> float:
    """0.20 weight — penalize high geopolitical_exposure_score, high impact_severity_if_materialized, low cross_scenario_resilience."""
    score = 0.0
    if inp.geopolitical_exposure_score >= 0.75:
        score += 40
    elif inp.geopolitical_exposure_score >= 0.50:
        score += 22
    elif inp.geopolitical_exposure_score >= 0.30:
        score += 8
    if inp.impact_severity_if_materialized >= 0.75:
        score += 35
    elif inp.impact_severity_if_materialized >= 0.50:
        score += 18
    elif inp.impact_severity_if_materialized >= 0.30:
        score += 7
    if inp.cross_scenario_resilience <= 0.25:
        score += 25
    elif inp.cross_scenario_resilience <= 0.50:
        score += 12
    elif inp.cross_scenario_resilience <= 0.70:
        score += 5
    return round(min(score, 100.0), 2)


def _composite(sig: float, read: float, sim: float, exp: float) -> float:
    return round(sig * 0.30 + read * 0.25 + sim * 0.25 + exp * 0.20, 2)


def _risk(composite: float) -> ForesightRisk:
    if composite >= 60:
        return ForesightRisk.CRITICAL
    if composite >= 40:
        return ForesightRisk.HIGH
    if composite >= 20:
        return ForesightRisk.MODERATE
    return ForesightRisk.LOW


def _severity(composite: float) -> ForesightSeverity:
    if composite >= 60:
        return ForesightSeverity.BLIND_SPOT
    if composite >= 40:
        return ForesightSeverity.VULNERABLE
    if composite >= 20:
        return ForesightSeverity.MONITORING
    return ForesightSeverity.PREPARED


def _pattern(inp: ForesightInput) -> ScenarioPattern:
    # Priority order: black_swan → disruption_wave → competitive_collapse → regulatory_shock → geopolitical_shift → none
    if inp.black_swan_preparedness <= 0.3 or (inp.impact_severity_if_materialized >= 0.8 and inp.scenario_probability >= 0.3):
        return ScenarioPattern.BLACK_SWAN
    if inp.technology_disruption_readiness <= 0.4 and inp.geopolitical_exposure_score >= 0.5:
        return ScenarioPattern.DISRUPTION_WAVE
    if inp.competitive_scenario_advantage <= 0.3 and inp.strategic_option_coverage <= 0.4:
        return ScenarioPattern.COMPETITIVE_COLLAPSE
    if inp.domain in ("regulatory", "economy") and inp.signal_detection_score <= 0.4:
        return ScenarioPattern.REGULATORY_SHOCK
    if inp.geopolitical_exposure_score >= 0.6 and inp.time_horizon_readiness <= 0.5:
        return ScenarioPattern.GEOPOLITICAL_SHIFT
    return ScenarioPattern.NONE


def _action(risk: ForesightRisk, pattern: ScenarioPattern) -> ForesightAction:
    if risk == ForesightRisk.CRITICAL:
        if pattern == ScenarioPattern.BLACK_SWAN:
            return ForesightAction.EMERGENCY_REPLAN
        if pattern == ScenarioPattern.DISRUPTION_WAVE:
            return ForesightAction.STRATEGIC_PIVOT
        return ForesightAction.CRISIS_SIMULATION
    if risk == ForesightRisk.HIGH:
        if pattern == ScenarioPattern.BLACK_SWAN:
            return ForesightAction.CRISIS_SIMULATION
        if pattern == ScenarioPattern.DISRUPTION_WAVE:
            return ForesightAction.SCENARIO_REPLAN
        return ForesightAction.CONTINGENCY_ACTIVATION
    if risk == ForesightRisk.MODERATE:
        return ForesightAction.STRATEGIC_HEDGE
    return ForesightAction.NO_ACTION


def _signal(inp: ForesightInput, comp: float, risk: ForesightRisk) -> str:
    if comp < 20:
        return "Anticipation stratégique robuste — signaux bien captés, scénarios maîtrisés, capacité adaptative forte"
    label = risk.value.replace("_", " ").title()
    return (
        f"{label} — détection signaux {round(inp.signal_detection_score * 100)}%"
        f" — préparation {round(inp.time_horizon_readiness * 100)}%"
        f" — résilience {round(inp.cross_scenario_resilience * 100)}%"
        f" — composite {round(comp)}"
    )


# ── Mock scenarios ─────────────────────────────────────────────────────────────

_MOCK_SCENARIOS: list[ForesightInput] = [
    # FS-001 technology EMEA critical black_swan (very bad all scores)
    ForesightInput("FS-001", "technology", "EMEA",
                   0.05, 0.05, 0.85, 0.95, 0.05, 0.05, 0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.90, 0.05, 0.05),
    # FS-002 economy NAMER low prepared
    ForesightInput("FS-002", "economy", "NAMER",
                   0.90, 0.85, 0.10, 0.10, 0.90, 0.88, 80, 0.90, 0.85, 0.90, 0.88, 0.85, 0.88, 0.10, 0.15, 0.88, 0.90),
    # FS-003 geopolitics APAC high disruption_wave
    ForesightInput("FS-003", "geopolitics", "APAC",
                   0.35, 0.30, 0.55, 0.70, 0.35, 0.30, 12, 0.35, 0.40, 0.35, 0.30, 0.35, 0.30, 0.72, 0.38, 0.78, 0.35),
    # FS-004 climate LATAM low monitoring
    ForesightInput("FS-004", "climate", "LATAM",
                   0.75, 0.70, 0.20, 0.25, 0.72, 0.70, 55, 0.75, 0.68, 0.70, 0.75, 0.70, 0.72, 0.20, 0.25, 0.70, 0.20, 0.75, 0.70),
    # FS-005 regulatory EMEA critical regulatory_shock
    ForesightInput("FS-005", "regulatory", "EMEA",
                   0.20, 0.25, 0.75, 0.80, 0.20, 0.18, 3, 0.20, 0.25, 0.20, 0.22, 0.25, 0.20, 0.35, 0.22, 0.55, 0.22),
    # FS-006 social NAMER moderate
    ForesightInput("FS-006", "social", "NAMER",
                   0.55, 0.50, 0.35, 0.45, 0.52, 0.55, 28, 0.58, 0.50, 0.55, 0.52, 0.55, 0.50, 0.40, 0.48, 0.35, 0.50, 0.55, 0.52),
    # FS-007 technology APAC high competitive_collapse
    ForesightInput("FS-007", "technology", "APAC",
                   0.40, 0.38, 0.60, 0.65, 0.40, 0.25, 8, 0.35, 0.28, 0.38, 0.35, 0.40, 0.35, 0.42, 0.35, 0.55, 0.75, 0.25, 0.38),
    # FS-008 geopolitics MEA critical geopolitical_shift
    ForesightInput("FS-008", "geopolitics", "MEA",
                   0.22, 0.20, 0.80, 0.85, 0.18, 0.15, 2, 0.20, 0.22, 0.18, 0.20, 0.22, 0.20, 0.80, 0.18, 0.72, 0.20),
]


class StrategicForesightSimulationEngine:
    """Anticipates future shocks, evaluates scenario preparedness, and routes strategic response."""

    def __init__(self) -> None:
        self._results: list[ForesightResult] = []

    def assess(self, inp: ForesightInput) -> ForesightResult:
        sig_s = _signal_score(inp)
        read_s = _readiness_score(inp)
        sim_s = _simulation_score(inp)
        exp_s = _exposure_score(inp)
        comp = _composite(sig_s, read_s, sim_s, exp_s)

        risk = _risk(comp)
        severity = _severity(comp)
        pattern = _pattern(inp)
        action = _action(risk, pattern)

        has_blind_spot = comp >= 40 or inp.black_swan_preparedness <= 0.3 or inp.signal_detection_score <= 0.3
        requires_sim = comp >= 25 or inp.simulation_iteration_count < 10 or inp.adaptive_capacity_score <= 0.35
        risk_index = round(min(comp / 100 * (1 - inp.adaptive_capacity_score + 0.01) * 10, 10.0), 2)
        sig = _signal(inp, comp, risk)

        result = ForesightResult(
            scenario_id=inp.scenario_id,
            region=inp.region,
            foresight_risk=risk,
            scenario_pattern=pattern,
            foresight_severity=severity,
            recommended_action=action,
            signal_score=sig_s,
            readiness_score=read_s,
            simulation_score=sim_s,
            exposure_score=exp_s,
            foresight_composite=comp,
            has_blind_spot_risk=has_blind_spot,
            requires_immediate_simulation=requires_sim,
            estimated_scenario_risk_index=risk_index,
            foresight_signal=sig,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ForesightInput]) -> list[ForesightResult]:
        for inp in inputs:
            self.assess(inp)
        self._results.sort(key=lambda r: r.foresight_composite, reverse=True)
        return self._results

    def load_mock_scenarios(self) -> list[ForesightResult]:
        self._results.clear()
        return self.assess_batch(_MOCK_SCENARIOS)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_foresight_composite": 0.0,
                "blind_spot_risk_count": 0,
                "immediate_simulation_count": 0,
                "avg_signal_score": 0.0,
                "avg_readiness_score": 0.0,
                "avg_simulation_score": 0.0,
                "avg_exposure_score": 0.0,
                "avg_estimated_scenario_risk_index": 0.0,
            }
        risk_counts: dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_comp = total_sig = total_read = total_sim = total_exp = total_idx = 0.0
        for r in self._results:
            risk_counts[r.foresight_risk.value] = risk_counts.get(r.foresight_risk.value, 0) + 1
            pattern_counts[r.scenario_pattern.value] = pattern_counts.get(r.scenario_pattern.value, 0) + 1
            severity_counts[r.foresight_severity.value] = severity_counts.get(r.foresight_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.foresight_composite
            total_sig += r.signal_score
            total_read += r.readiness_score
            total_sim += r.simulation_score
            total_exp += r.exposure_score
            total_idx += r.estimated_scenario_risk_index
        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_foresight_composite": round(total_comp / n, 2),
            "blind_spot_risk_count": sum(1 for r in self._results if r.has_blind_spot_risk),
            "immediate_simulation_count": sum(1 for r in self._results if r.requires_immediate_simulation),
            "avg_signal_score": round(total_sig / n, 2),
            "avg_readiness_score": round(total_read / n, 2),
            "avg_simulation_score": round(total_sim / n, 2),
            "avg_exposure_score": round(total_exp / n, 2),
            "avg_estimated_scenario_risk_index": round(total_idx / n, 2),
        }
