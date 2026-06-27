from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class ObjRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ObjPattern(str, Enum):
    none                = "none"
    price_caver         = "price_caver"
    status_quo_deflector = "status_quo_deflector"
    feature_objector    = "feature_objector"
    authority_blocker   = "authority_blocker"
    timing_deferrer     = "timing_deferrer"


class ObjSeverity(str, Enum):
    expert      = "expert"
    competent   = "competent"
    developing  = "developing"
    struggling  = "struggling"


class ObjAction(str, Enum):
    no_action                       = "no_action"
    price_objection_coaching        = "price_objection_coaching"
    reframe_coaching                = "reframe_coaching"
    feature_gap_coaching            = "feature_gap_coaching"
    multi_threading_coaching        = "multi_threading_coaching"
    urgency_creation_coaching       = "urgency_creation_coaching"
    objection_handling_intervention = "objection_handling_intervention"


@dataclass
class ObjInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    objection_encounter_rate_pct:        float   # % of deals where objections were raised (0–1)
    objection_resolution_rate_pct:       float   # % of objections resolved without concession (0–1)
    price_objection_rate_pct:            float   # % of all objections that are price-based (0–1)
    status_quo_objection_rate_pct:       float   # % that are "we don't need this" type (0–1)
    feature_objection_rate_pct:          float   # % that are feature/capability gaps (0–1)
    authority_objection_rate_pct:        float   # % "need to check with boss" (0–1)
    timing_objection_rate_pct:           float   # % "not the right time" (0–1)
    first_response_reframe_rate_pct:     float   # % of objections answered with reframe (0–1)
    objection_leads_to_loss_rate_pct:    float   # % of deals lost after key objection (0–1)
    unaddressed_objection_rate_pct:      float   # % of calls with objection left unaddressed (0–1)
    concession_after_objection_pct:      float   # % of price objections leading to discount (0–1)
    evidence_usage_rate_pct:             float   # % of objections where case study/data used (0–1)
    repeat_objection_rate_pct:           float   # % of deals where same objection raised 2+ times (0–1)
    avg_objections_per_deal:             float
    deal_stall_after_objection_rate_pct: float   # % of deals stalled >14d after objection (0–1)
    total_deals_closed:                  int
    avg_opportunity_value_usd:           float
    active_deal_count:                   int
    calls_with_recorded_objection:       int


@dataclass
class ObjResult:
    rep_id:                          str
    region:                          str
    obj_risk:                        ObjRisk
    obj_pattern:                     ObjPattern
    obj_severity:                    ObjSeverity
    recommended_action:              ObjAction
    resolution_effectiveness_score:  float
    objection_intelligence_score:    float
    resilience_score:                float
    evidence_utilization_score:      float
    obj_composite:                   float
    has_obj_gap:                     bool
    requires_obj_coaching:           bool
    estimated_deal_loss_usd:         float
    obj_signal:                      str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                          self.rep_id,
            "region":                          self.region,
            "obj_risk":                        self.obj_risk.value,
            "obj_pattern":                     self.obj_pattern.value,
            "obj_severity":                    self.obj_severity.value,
            "recommended_action":              self.recommended_action.value,
            "resolution_effectiveness_score":  self.resolution_effectiveness_score,
            "objection_intelligence_score":    self.objection_intelligence_score,
            "resilience_score":                self.resilience_score,
            "evidence_utilization_score":      self.evidence_utilization_score,
            "obj_composite":                   self.obj_composite,
            "has_obj_gap":                     self.has_obj_gap,
            "requires_obj_coaching":           self.requires_obj_coaching,
            "estimated_deal_loss_usd":         self.estimated_deal_loss_usd,
            "obj_signal":                      self.obj_signal,
        }


class SalesObjectionHandlingIntelligenceEngine:

    def __init__(self) -> None:
        self._results: List[ObjResult] = []

    def _resolution_effectiveness_score(self, inp: ObjInput) -> float:
        s = 0.0
        if inp.objection_resolution_rate_pct <= 0.35:
            s += 45
        elif inp.objection_resolution_rate_pct <= 0.55:
            s += 28
        elif inp.objection_resolution_rate_pct <= 0.70:
            s += 12
        if inp.objection_leads_to_loss_rate_pct >= 0.50:
            s += 35
        elif inp.objection_leads_to_loss_rate_pct >= 0.35:
            s += 18
        elif inp.objection_leads_to_loss_rate_pct >= 0.20:
            s += 6
        if inp.unaddressed_objection_rate_pct >= 0.35:
            s += 20
        elif inp.unaddressed_objection_rate_pct >= 0.20:
            s += 10
        return min(s, 100.0)

    def _objection_intelligence_score(self, inp: ObjInput) -> float:
        s = 0.0
        if inp.first_response_reframe_rate_pct <= 0.25:
            s += 40
        elif inp.first_response_reframe_rate_pct <= 0.45:
            s += 22
        elif inp.first_response_reframe_rate_pct <= 0.60:
            s += 8
        if inp.repeat_objection_rate_pct >= 0.50:
            s += 35
        elif inp.repeat_objection_rate_pct >= 0.35:
            s += 18
        elif inp.repeat_objection_rate_pct >= 0.20:
            s += 6
        if inp.deal_stall_after_objection_rate_pct >= 0.45:
            s += 25
        elif inp.deal_stall_after_objection_rate_pct >= 0.30:
            s += 12
        return min(s, 100.0)

    def _resilience_score(self, inp: ObjInput) -> float:
        s = 0.0
        if inp.concession_after_objection_pct >= 0.65:
            s += 45
        elif inp.concession_after_objection_pct >= 0.45:
            s += 28
        elif inp.concession_after_objection_pct >= 0.28:
            s += 12
        if inp.avg_objections_per_deal >= 4:
            s += 35
        elif inp.avg_objections_per_deal >= 2.5:
            s += 18
        elif inp.avg_objections_per_deal >= 1.5:
            s += 6
        if inp.price_objection_rate_pct >= 0.55:
            s += 20
        elif inp.price_objection_rate_pct >= 0.40:
            s += 10
        return min(s, 100.0)

    def _evidence_utilization_score(self, inp: ObjInput) -> float:
        s = 0.0
        if inp.evidence_usage_rate_pct <= 0.20:
            s += 50
        elif inp.evidence_usage_rate_pct <= 0.40:
            s += 30
        elif inp.evidence_usage_rate_pct <= 0.60:
            s += 12
        if inp.status_quo_objection_rate_pct >= 0.35:
            s += 30
        elif inp.status_quo_objection_rate_pct >= 0.20:
            s += 15
        if inp.feature_objection_rate_pct >= 0.30:
            s += 20
        elif inp.feature_objection_rate_pct >= 0.18:
            s += 10
        return min(s, 100.0)

    def _composite(self, re: float, oi: float, rs: float, eu: float) -> float:
        return round(re * 0.35 + oi * 0.25 + rs * 0.25 + eu * 0.15, 2)

    def _pattern(self, inp: ObjInput) -> ObjPattern:
        if inp.price_objection_rate_pct >= 0.50 and inp.concession_after_objection_pct >= 0.60:
            return ObjPattern.price_caver
        if inp.status_quo_objection_rate_pct >= 0.35 and inp.first_response_reframe_rate_pct <= 0.30:
            return ObjPattern.status_quo_deflector
        if inp.feature_objection_rate_pct >= 0.30 and inp.objection_leads_to_loss_rate_pct >= 0.40:
            return ObjPattern.feature_objector
        if inp.authority_objection_rate_pct >= 0.30 and inp.deal_stall_after_objection_rate_pct >= 0.40:
            return ObjPattern.authority_blocker
        if inp.timing_objection_rate_pct >= 0.30 and inp.repeat_objection_rate_pct >= 0.40:
            return ObjPattern.timing_deferrer
        return ObjPattern.none

    def _risk(self, composite: float) -> ObjRisk:
        if composite >= 60: return ObjRisk.critical
        if composite >= 40: return ObjRisk.high
        if composite >= 20: return ObjRisk.moderate
        return ObjRisk.low

    def _severity(self, composite: float) -> ObjSeverity:
        if composite >= 60: return ObjSeverity.struggling
        if composite >= 40: return ObjSeverity.developing
        if composite >= 20: return ObjSeverity.competent
        return ObjSeverity.expert

    def _action(self, risk: ObjRisk, pattern: ObjPattern) -> ObjAction:
        if risk == ObjRisk.critical:
            return ObjAction.objection_handling_intervention
        if risk == ObjRisk.high:
            if pattern == ObjPattern.price_caver:
                return ObjAction.price_objection_coaching
            if pattern == ObjPattern.status_quo_deflector:
                return ObjAction.reframe_coaching
            if pattern == ObjPattern.feature_objector:
                return ObjAction.feature_gap_coaching
            if pattern == ObjPattern.authority_blocker:
                return ObjAction.multi_threading_coaching
            if pattern == ObjPattern.timing_deferrer:
                return ObjAction.urgency_creation_coaching
            return ObjAction.reframe_coaching
        if risk == ObjRisk.moderate:
            return ObjAction.reframe_coaching
        return ObjAction.no_action

    def _has_gap(self, inp: ObjInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.objection_resolution_rate_pct <= 0.55
            or inp.concession_after_objection_pct >= 0.40
        )

    def _requires_coaching(self, inp: ObjInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.unaddressed_objection_rate_pct >= 0.20
            or inp.evidence_usage_rate_pct <= 0.45
        )

    def _deal_loss(self, inp: ObjInput, composite: float) -> float:
        return round(
            inp.active_deal_count
            * inp.avg_opportunity_value_usd
            * inp.objection_leads_to_loss_rate_pct
            * (composite / 100.0),
            2,
        )

    def _signal(self, inp: ObjInput, pattern: ObjPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Objection handling strong — resolution rate, reframe quality, "
                "and evidence use within benchmarks"
            )
        labels = {
            ObjPattern.price_caver:          "Price caver",
            ObjPattern.status_quo_deflector: "Status quo deflector",
            ObjPattern.feature_objector:     "Feature objector",
            ObjPattern.authority_blocker:    "Authority blocker",
            ObjPattern.timing_deferrer:      "Timing deferrer",
        }
        label    = labels.get(pattern, "Objection handling gap")
        res_pct  = round(inp.objection_resolution_rate_pct * 100)
        conc_pct = round(inp.concession_after_objection_pct * 100)
        ev_pct   = round(inp.evidence_usage_rate_pct * 100)
        comp_int = round(composite)
        return (
            f"{label} — {res_pct}% objections resolved — "
            f"{conc_pct}% concede after price obj — "
            f"{ev_pct}% use evidence — composite {comp_int}"
        )

    def assess(self, inp: ObjInput) -> ObjResult:
        re = self._resolution_effectiveness_score(inp)
        oi = self._objection_intelligence_score(inp)
        rs = self._resilience_score(inp)
        eu = self._evidence_utilization_score(inp)
        comp    = self._composite(re, oi, rs, eu)
        pattern = self._pattern(inp)
        risk    = self._risk(comp)
        sev     = self._severity(comp)
        action  = self._action(risk, pattern)
        result  = ObjResult(
            rep_id                         = inp.rep_id,
            region                         = inp.region,
            obj_risk                       = risk,
            obj_pattern                    = pattern,
            obj_severity                   = sev,
            recommended_action             = action,
            resolution_effectiveness_score = round(re, 2),
            objection_intelligence_score   = round(oi, 2),
            resilience_score               = round(rs, 2),
            evidence_utilization_score     = round(eu, 2),
            obj_composite                  = comp,
            has_obj_gap                    = self._has_gap(inp, comp),
            requires_obj_coaching          = self._requires_coaching(inp, comp),
            estimated_deal_loss_usd        = self._deal_loss(inp, comp),
            obj_signal                     = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ObjInput]) -> List[ObjResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        rr = self._results
        if not rr:
            return {
                "total": 0, "risk_counts": {}, "pattern_counts": {},
                "severity_counts": {}, "action_counts": {},
                "avg_obj_composite": 0.0, "obj_gap_count": 0,
                "coaching_count": 0, "avg_resolution_effectiveness_score": 0.0,
                "avg_objection_intelligence_score": 0.0,
                "avg_resilience_score": 0.0,
                "avg_evidence_utilization_score": 0.0,
                "total_estimated_deal_loss_usd": 0.0,
            }
        n = len(rr)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tre = toi = trs = teu = trev = 0.0
        gc = cc = 0
        for r in rr:
            rc[r.obj_risk.value]          = rc.get(r.obj_risk.value, 0) + 1
            pc[r.obj_pattern.value]       = pc.get(r.obj_pattern.value, 0) + 1
            sc[r.obj_severity.value]      = sc.get(r.obj_severity.value, 0) + 1
            ac[r.recommended_action.value]= ac.get(r.recommended_action.value, 0) + 1
            tre  += r.resolution_effectiveness_score
            toi  += r.objection_intelligence_score
            trs  += r.resilience_score
            teu  += r.evidence_utilization_score
            trev += r.estimated_deal_loss_usd
            gc   += r.has_obj_gap
            cc   += r.requires_obj_coaching
        return {
            "total":                               n,
            "risk_counts":                         rc,
            "pattern_counts":                      pc,
            "severity_counts":                     sc,
            "action_counts":                       ac,
            "avg_obj_composite":                   round(sum(r.obj_composite for r in rr) / n, 1),
            "obj_gap_count":                       gc,
            "coaching_count":                      cc,
            "avg_resolution_effectiveness_score":  round(tre / n, 1),
            "avg_objection_intelligence_score":    round(toi / n, 1),
            "avg_resilience_score":                round(trs / n, 1),
            "avg_evidence_utilization_score":      round(teu / n, 1),
            "total_estimated_deal_loss_usd":       round(trev, 2),
        }
