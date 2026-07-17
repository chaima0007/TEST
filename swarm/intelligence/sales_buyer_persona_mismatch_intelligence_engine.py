from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class PersonaRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class PersonaPattern(str, Enum):
    none                  = "none"
    wrong_level           = "wrong_level"
    wrong_department      = "wrong_department"
    influencer_only       = "influencer_only"
    technical_gatekeeper  = "technical_gatekeeper"
    budget_blind          = "budget_blind"


class PersonaSeverity(str, Enum):
    aligned      = "aligned"
    misaligned   = "misaligned"
    disconnected = "disconnected"
    invisible    = "invisible"


class PersonaAction(str, Enum):
    no_action                       = "no_action"
    persona_alignment_check         = "persona_alignment_check"
    stakeholder_mapping_coaching    = "stakeholder_mapping_coaching"
    executive_access_coaching       = "executive_access_coaching"
    budget_holder_introduction      = "budget_holder_introduction"
    persona_reset_intervention      = "persona_reset_intervention"
    deal_re_qualification           = "deal_re_qualification"


@dataclass
class PersonaInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    primary_contact_level_score:         float  # 0-1 (1=C-suite, 0=individual contributor)
    economic_buyer_contact_rate_pct:     float  # 0-1 (% deals with EB contact)
    it_only_contact_rate_pct:            float  # 0-1 (% deals only engaging IT)
    business_unit_alignment_score:       float  # 0-1 (right dept for the use case)
    decision_maker_access_rate_pct:      float  # 0-1 (% deals with DM access)
    influencer_only_rate_pct:            float  # 0-1 (% deals stuck with influencers)
    procurement_first_contact_rate_pct:  float  # 0-1 (% deals entering via procurement)
    avg_seniority_of_contacts:           float  # 0-1 (weighted avg seniority)
    sponsor_identification_rate_pct:     float  # 0-1 (% deals with identified sponsor)
    cross_functional_coverage_score:     float  # 0-1 (breadth across depts)
    persona_to_use_case_fit_score:       float  # 0-1 (contact role matches solution)
    budget_authority_confirmed_rate_pct: float  # 0-1 (% deals budget confirmed)
    vp_plus_engagement_rate_pct:         float  # 0-1 (% deals with VP or above)
    champion_seniority_score:            float  # 0-1 (1=senior champion)
    technical_blockers_rate_pct:         float  # 0-1 (% deals blocked by technical stakeholders)
    wrong_entry_point_rate_pct:          float  # 0-1 (entered via non-ideal contact)
    referral_to_right_person_rate_pct:   float  # 0-1 (% times successfully redirected)
    lost_due_to_persona_mismatch_pct:    float  # 0-1 (% historical losses due to persona)
    total_deals_evaluated:               int
    avg_deal_value_usd:                  float


@dataclass
class PersonaResult:
    rep_id:                         str
    region:                         str
    persona_risk:                   PersonaRisk
    persona_pattern:                PersonaPattern
    persona_severity:               PersonaSeverity
    recommended_action:             PersonaAction
    access_score:                   float
    alignment_score:                float
    authority_score:                float
    coverage_score:                 float
    persona_composite:              float
    has_persona_gap:                bool
    requires_persona_coaching:      bool
    estimated_lost_deal_value_usd:  float
    persona_signal:                 str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "persona_risk":                     self.persona_risk.value,
            "persona_pattern":                  self.persona_pattern.value,
            "persona_severity":                 self.persona_severity.value,
            "recommended_action":               self.recommended_action.value,
            "access_score":                     self.access_score,
            "alignment_score":                  self.alignment_score,
            "authority_score":                  self.authority_score,
            "coverage_score":                   self.coverage_score,
            "persona_composite":                self.persona_composite,
            "has_persona_gap":                  self.has_persona_gap,
            "requires_persona_coaching":        self.requires_persona_coaching,
            "estimated_lost_deal_value_usd":    self.estimated_lost_deal_value_usd,
            "persona_signal":                   self.persona_signal,
        }


class SalesBuyerPersonaMismatchIntelligenceEngine:
    """Detects when reps sell to the wrong person — wrong level, department, or decision-maker type."""

    def __init__(self) -> None:
        self._results: List[PersonaResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _access_score(self, inp: PersonaInput) -> float:
        s = 0.0
        if   inp.decision_maker_access_rate_pct  <= 0.30: s += 40
        elif inp.decision_maker_access_rate_pct  <= 0.55: s += 22
        elif inp.decision_maker_access_rate_pct  <= 0.75: s += 8
        if   inp.vp_plus_engagement_rate_pct     <= 0.20: s += 35
        elif inp.vp_plus_engagement_rate_pct     <= 0.45: s += 18
        if   inp.primary_contact_level_score     <= 0.25: s += 25
        elif inp.primary_contact_level_score     <= 0.50: s += 12
        return min(s, 100.0)

    def _alignment_score(self, inp: PersonaInput) -> float:
        s = 0.0
        if   inp.persona_to_use_case_fit_score   <= 0.30: s += 40
        elif inp.persona_to_use_case_fit_score   <= 0.55: s += 22
        elif inp.persona_to_use_case_fit_score   <= 0.75: s += 8
        if   inp.business_unit_alignment_score   <= 0.30: s += 35
        elif inp.business_unit_alignment_score   <= 0.55: s += 18
        if   inp.wrong_entry_point_rate_pct      >= 0.50: s += 25
        elif inp.wrong_entry_point_rate_pct      >= 0.30: s += 12
        return min(s, 100.0)

    def _authority_score(self, inp: PersonaInput) -> float:
        s = 0.0
        if   inp.economic_buyer_contact_rate_pct         <= 0.25: s += 40
        elif inp.economic_buyer_contact_rate_pct         <= 0.50: s += 22
        elif inp.economic_buyer_contact_rate_pct         <= 0.70: s += 8
        if   inp.budget_authority_confirmed_rate_pct     <= 0.25: s += 35
        elif inp.budget_authority_confirmed_rate_pct     <= 0.50: s += 18
        if   inp.influencer_only_rate_pct                >= 0.50: s += 25
        elif inp.influencer_only_rate_pct                >= 0.30: s += 12
        return min(s, 100.0)

    def _coverage_score(self, inp: PersonaInput) -> float:
        s = 0.0
        if   inp.cross_functional_coverage_score         <= 0.25: s += 45
        elif inp.cross_functional_coverage_score         <= 0.50: s += 25
        elif inp.cross_functional_coverage_score         <= 0.70: s += 10
        if   inp.sponsor_identification_rate_pct         <= 0.30: s += 30
        elif inp.sponsor_identification_rate_pct         <= 0.55: s += 15
        if   inp.technical_blockers_rate_pct             >= 0.45: s += 25
        elif inp.technical_blockers_rate_pct             >= 0.25: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────────

    def _composite(self, ac: float, al: float, au: float, co: float) -> float:
        return min(round(ac * 0.30 + al * 0.25 + au * 0.30 + co * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, inp: PersonaInput) -> PersonaPattern:
        if inp.primary_contact_level_score <= 0.30 and inp.vp_plus_engagement_rate_pct <= 0.20:
            return PersonaPattern.wrong_level
        if inp.business_unit_alignment_score <= 0.35 and inp.persona_to_use_case_fit_score <= 0.40:
            return PersonaPattern.wrong_department
        if inp.influencer_only_rate_pct >= 0.50 and inp.decision_maker_access_rate_pct <= 0.35:
            return PersonaPattern.influencer_only
        if inp.it_only_contact_rate_pct >= 0.55 and inp.technical_blockers_rate_pct >= 0.40:
            return PersonaPattern.technical_gatekeeper
        if inp.economic_buyer_contact_rate_pct <= 0.25 and inp.budget_authority_confirmed_rate_pct <= 0.25:
            return PersonaPattern.budget_blind
        return PersonaPattern.none

    # ── thresholds ────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> PersonaRisk:
        if   composite >= 60: return PersonaRisk.critical
        elif composite >= 40: return PersonaRisk.high
        elif composite >= 20: return PersonaRisk.moderate
        return PersonaRisk.low

    def _severity(self, composite: float) -> PersonaSeverity:
        if   composite >= 60: return PersonaSeverity.invisible
        elif composite >= 40: return PersonaSeverity.disconnected
        elif composite >= 20: return PersonaSeverity.misaligned
        return PersonaSeverity.aligned

    def _action(self, risk: PersonaRisk, pattern: PersonaPattern) -> PersonaAction:
        if risk == PersonaRisk.critical:
            if pattern in (PersonaPattern.wrong_level, PersonaPattern.influencer_only):
                return PersonaAction.deal_re_qualification
            return PersonaAction.persona_reset_intervention
        if risk == PersonaRisk.high:
            if pattern == PersonaPattern.wrong_level:
                return PersonaAction.executive_access_coaching
            if pattern == PersonaPattern.wrong_department:
                return PersonaAction.stakeholder_mapping_coaching
            if pattern == PersonaPattern.influencer_only:
                return PersonaAction.executive_access_coaching
            if pattern == PersonaPattern.technical_gatekeeper:
                return PersonaAction.budget_holder_introduction
            if pattern == PersonaPattern.budget_blind:
                return PersonaAction.budget_holder_introduction
            return PersonaAction.stakeholder_mapping_coaching
        if risk == PersonaRisk.moderate:
            return PersonaAction.persona_alignment_check
        return PersonaAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: PersonaInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.economic_buyer_contact_rate_pct <= 0.50
            or inp.decision_maker_access_rate_pct  <= 0.55
        )

    def _requires_coaching(self, inp: PersonaInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.lost_due_to_persona_mismatch_pct >= 0.20
            or inp.influencer_only_rate_pct          >= 0.35
        )

    # ── lost deal value ───────────────────────────────────────────────────────

    def _lost_deal_value(self, inp: PersonaInput, composite: float) -> float:
        loss_rate = min(inp.lost_due_to_persona_mismatch_pct + (composite / 200), 1.0)
        return round(inp.total_deals_evaluated * inp.avg_deal_value_usd * loss_rate, 2)

    # ── signal ────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        PersonaPattern.wrong_level:          "Wrong contact level",
        PersonaPattern.wrong_department:     "Wrong department",
        PersonaPattern.influencer_only:      "Influencer-only access",
        PersonaPattern.technical_gatekeeper: "Technical gatekeeper block",
        PersonaPattern.budget_blind:         "Budget-blind engagement",
    }

    def _signal(self, inp: PersonaInput, pattern: PersonaPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Buyer persona alignment strong — decision-maker access, budget authority, "
                "and cross-functional coverage within benchmarks"
            )
        label    = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        dm_pct   = round(inp.decision_maker_access_rate_pct * 100)
        eb_pct   = round(inp.economic_buyer_contact_rate_pct * 100)
        vp_pct   = round(inp.vp_plus_engagement_rate_pct * 100)
        comp_int = round(composite)
        return (
            f"{label} — {dm_pct}% DM access — {eb_pct}% EB contact — "
            f"{vp_pct}% VP+ engagement — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, inp: PersonaInput) -> PersonaResult:
        ac   = self._access_score(inp)
        al   = self._alignment_score(inp)
        au   = self._authority_score(inp)
        co   = self._coverage_score(inp)
        comp = self._composite(ac, al, au, co)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = PersonaResult(
            rep_id                          = inp.rep_id,
            region                          = inp.region,
            persona_risk                    = risk,
            persona_pattern                 = pattern,
            persona_severity                = severity,
            recommended_action              = action,
            access_score                    = ac,
            alignment_score                 = al,
            authority_score                 = au,
            coverage_score                  = co,
            persona_composite               = comp,
            has_persona_gap                 = self._has_gap(inp, comp),
            requires_persona_coaching       = self._requires_coaching(inp, comp),
            estimated_lost_deal_value_usd   = self._lost_deal_value(inp, comp),
            persona_signal                  = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[PersonaInput]) -> List[PersonaResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_persona_composite": 0.0,
                "persona_gap_count": 0,
                "coaching_count": 0,
                "avg_access_score": 0.0,
                "avg_alignment_score": 0.0,
                "avg_authority_score": 0.0,
                "avg_coverage_score": 0.0,
                "total_estimated_lost_deal_value_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_ac = total_al = total_au = total_co = total_lv = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.persona_risk.value]         = risk_counts.get(res.persona_risk.value, 0) + 1
            pattern_counts[res.persona_pattern.value]   = pattern_counts.get(res.persona_pattern.value, 0) + 1
            severity_counts[res.persona_severity.value] = severity_counts.get(res.persona_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.persona_composite
            total_ac   += res.access_score
            total_al   += res.alignment_score
            total_au   += res.authority_score
            total_co   += res.coverage_score
            total_lv   += res.estimated_lost_deal_value_usd
            if res.has_persona_gap:          gap_count      += 1
            if res.requires_persona_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_persona_composite":                round(total_comp / n, 1),
            "persona_gap_count":                    gap_count,
            "coaching_count":                       coaching_count,
            "avg_access_score":                     round(total_ac / n, 1),
            "avg_alignment_score":                  round(total_al / n, 1),
            "avg_authority_score":                  round(total_au / n, 1),
            "avg_coverage_score":                   round(total_co / n, 1),
            "total_estimated_lost_deal_value_usd":  round(total_lv, 2),
        }
