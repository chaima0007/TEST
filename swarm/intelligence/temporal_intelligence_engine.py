"""
Module 257 — Temporal Intelligence & Strategic Timing Optimization Engine
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class TimingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class TimingPattern(str, Enum):
    timing_miss      = "timing_miss"
    window_collapse  = "window_collapse"
    premature_action = "premature_action"
    delayed_response = "delayed_response"
    timing_conflict  = "timing_conflict"
    none             = "none"


class TimingSeverity(str, Enum):
    optimal = "optimal"
    watch   = "watch"
    closing = "closing"
    missed  = "missed"


class TimingAction(str, Enum):
    no_action               = "no_action"
    timing_monitoring       = "timing_monitoring"
    timing_recalibration    = "timing_recalibration"
    window_capture          = "window_capture"
    emergency_acceleration  = "emergency_acceleration"
    strategic_pause         = "strategic_pause"


@dataclass
class TemporalInput:
    decision_id: str
    decision_type: str   # market_entry/product_launch/acquisition/regulatory_filing/fundraising/talent_hiring/partnership/market_exit
    region: str
    timing_window_score: float            # 0.0–1.0
    market_cycle_alignment: float         # 0.0–1.0
    competitor_vulnerability_index: float # 0.0–1.0
    regulatory_window_score: float        # 0.0–1.0
    seasonal_demand_fit: float            # 0.0–1.0
    capital_market_receptivity: float     # 0.0–1.0
    first_mover_advantage_score: float    # 0.0–1.0
    execution_readiness_score: float      # 0.0–1.0
    macro_momentum_alignment: float       # 0.0–1.0
    stakeholder_availability_score: float # 0.0–1.0
    opportunity_decay_rate: float         # 0.0–1.0
    counter_timing_risk: float            # 0.0–1.0
    information_freshness_score: float    # 0.0–1.0
    decision_urgency_index: float         # 0.0–1.0
    resource_alignment_score: float       # 0.0–1.0
    geopolitical_stability_window: float  # 0.0–1.0
    timing_confidence_score: float        # 0.0–1.0


@dataclass
class TemporalResult:
    decision_id: str
    decision_type: str
    region: str
    temporal_risk: str
    timing_pattern: str
    timing_severity: str
    recommended_action: str
    opportunity_score: float
    readiness_score: float
    alignment_score: float
    risk_score: float
    temporal_composite: float
    missed_window: bool
    acceleration_required: bool
    estimated_timing_loss_index: float
    timing_signal: str

    def to_dict(self) -> Dict:
        return {
            "decision_id":                   self.decision_id,
            "decision_type":                 self.decision_type,
            "region":                        self.region,
            "temporal_risk":                 self.temporal_risk,
            "timing_pattern":                self.timing_pattern,
            "timing_severity":               self.timing_severity,
            "recommended_action":            self.recommended_action,
            "opportunity_score":             self.opportunity_score,
            "readiness_score":               self.readiness_score,
            "alignment_score":               self.alignment_score,
            "risk_score":                    self.risk_score,
            "temporal_composite":            self.temporal_composite,
            "missed_window":                 self.missed_window,
            "acceleration_required":         self.acceleration_required,
            "estimated_timing_loss_index":   self.estimated_timing_loss_index,
        }


class TemporalIntelligenceEngine:
    def __init__(self) -> None:
        self._results: List[TemporalResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _opportunity_score(self, i: TemporalInput) -> float:
        avg = (i.timing_window_score + i.market_cycle_alignment + i.first_mover_advantage_score) / 3
        return min(avg * 100, 100.0)

    def _readiness_score(self, i: TemporalInput) -> float:
        avg = (i.execution_readiness_score + i.resource_alignment_score + i.stakeholder_availability_score) / 3
        return min(avg * 100, 100.0)

    def _alignment_score(self, i: TemporalInput) -> float:
        avg = (i.regulatory_window_score + i.macro_momentum_alignment + i.capital_market_receptivity) / 3
        return min(avg * 100, 100.0)

    def _risk_score(self, i: TemporalInput) -> float:
        avg = (i.counter_timing_risk + i.opportunity_decay_rate + i.decision_urgency_index) / 3
        return min(avg * 100, 100.0)

    def _composite(self, opp: float, rdy: float, aln: float, rsk: float) -> float:
        return min(round(opp * 0.30 + rdy * 0.25 + aln * 0.25 + rsk * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> TimingRisk:
        if c >= 60: return TimingRisk.critical
        if c >= 40: return TimingRisk.high
        if c >= 20: return TimingRisk.moderate
        return TimingRisk.low

    def _severity(self, risk: TimingRisk) -> TimingSeverity:
        if risk == TimingRisk.critical: return TimingSeverity.missed
        if risk == TimingRisk.high:     return TimingSeverity.closing
        if risk == TimingRisk.moderate: return TimingSeverity.watch
        return TimingSeverity.optimal

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: TemporalInput) -> TimingPattern:
        if i.timing_window_score < 0.30 and i.market_cycle_alignment < 0.30:
            return TimingPattern.timing_miss
        if i.opportunity_decay_rate > 0.70 and i.timing_window_score < 0.40:
            return TimingPattern.window_collapse
        if i.execution_readiness_score < 0.30 and i.timing_window_score > 0.70:
            return TimingPattern.premature_action
        if i.decision_urgency_index > 0.70 and i.timing_window_score < 0.30:
            return TimingPattern.delayed_response
        if i.counter_timing_risk > 0.60 and i.timing_window_score > 0.50:
            return TimingPattern.timing_conflict
        return TimingPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: TimingRisk, pat: TimingPattern) -> TimingAction:
        if risk == TimingRisk.critical:
            if pat == TimingPattern.window_collapse: return TimingAction.emergency_acceleration
            return TimingAction.strategic_pause
        if risk == TimingRisk.high:
            if pat == TimingPattern.timing_miss: return TimingAction.timing_recalibration
            return TimingAction.window_capture
        if risk == TimingRisk.moderate:
            return TimingAction.timing_monitoring
        return TimingAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived booleans & indices                                          #
    # ------------------------------------------------------------------ #

    def _missed_window(self, i: TemporalInput, comp: float) -> bool:
        return comp >= 60 or (i.timing_window_score < 0.25 and i.opportunity_decay_rate > 0.60)

    def _acceleration_required(self, i: TemporalInput, comp: float) -> bool:
        return comp >= 40 and i.decision_urgency_index > 0.60

    def _loss_index(self, i: TemporalInput, comp: float) -> float:
        return round(min(comp / 100 * (i.opportunity_decay_rate + i.counter_timing_risk) / 2 * 10, 10.0), 2)

    def _signal(self, i: TemporalInput, pat: TimingPattern, comp: float) -> str:
        if comp < 20:
            return "Fenêtre temporelle optimale — timing parfait, alignement marché, préparation maximale"
        labels = {
            TimingPattern.timing_miss:      "Fenêtre manquée",
            TimingPattern.window_collapse:  "Effondrement fenêtre",
            TimingPattern.premature_action: "Action prématurée",
            TimingPattern.delayed_response: "Réponse tardive",
            TimingPattern.timing_conflict:  "Conflit temporel",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — fenêtre {i.timing_window_score:.2f}"
            f" — decay {i.opportunity_decay_rate:.2f}"
            f" — préparation {i.execution_readiness_score:.2f}"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: TemporalInput) -> TemporalResult:
        opp  = self._opportunity_score(i)
        rdy  = self._readiness_score(i)
        aln  = self._alignment_score(i)
        rsk  = self._risk_score(i)
        comp = self._composite(opp, rdy, aln, rsk)
        risk = self._risk(comp)
        sev  = self._severity(risk)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = TemporalResult(
            decision_id=i.decision_id,
            decision_type=i.decision_type,
            region=i.region,
            temporal_risk=risk.value,
            timing_pattern=pat.value,
            timing_severity=sev.value,
            recommended_action=act.value,
            opportunity_score=opp,
            readiness_score=rdy,
            alignment_score=aln,
            risk_score=rsk,
            temporal_composite=comp,
            missed_window=self._missed_window(i, comp),
            acceleration_required=self._acceleration_required(i, comp),
            estimated_timing_loss_index=self._loss_index(i, comp),
            timing_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[TemporalInput]) -> List[TemporalResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_temporal_composite": 0.0,
                "missed_window_count": 0,
                "acceleration_required_count": 0,
                "avg_opportunity_score": 0.0,
                "avg_readiness_score": 0.0,
                "avg_alignment_score": 0.0,
                "avg_risk_score": 0.0,
                "avg_estimated_timing_loss_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        topp = trdy = taln = trsk = tcomp = tloss = 0.0
        missed_count = accel_count = 0
        for r in self._results:
            rc[r.temporal_risk]       = rc.get(r.temporal_risk, 0)       + 1
            pc[r.timing_pattern]      = pc.get(r.timing_pattern, 0)      + 1
            sc[r.timing_severity]     = sc.get(r.timing_severity, 0)     + 1
            ac[r.recommended_action]  = ac.get(r.recommended_action, 0)  + 1
            topp  += r.opportunity_score
            trdy  += r.readiness_score
            taln  += r.alignment_score
            trsk  += r.risk_score
            tcomp += r.temporal_composite
            tloss += r.estimated_timing_loss_index
            if r.missed_window:          missed_count += 1
            if r.acceleration_required:  accel_count  += 1
        return {
            "total":                           n,
            "risk_counts":                     rc,
            "pattern_counts":                  pc,
            "severity_counts":                 sc,
            "action_counts":                   ac,
            "avg_temporal_composite":          round(tcomp / n, 1),
            "missed_window_count":             missed_count,
            "acceleration_required_count":     accel_count,
            "avg_opportunity_score":           round(topp / n, 1),
            "avg_readiness_score":             round(trdy / n, 1),
            "avg_alignment_score":             round(taln / n, 1),
            "avg_risk_score":                  round(trsk / n, 1),
            "avg_estimated_timing_loss_index": round(tloss / n, 2),
        }
