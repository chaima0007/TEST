from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PersonaDriftSeverity(str, Enum):
    ALIGNED    = "aligned"
    MINOR_DRIFT = "minor_drift"
    MODERATE_DRIFT = "moderate_drift"
    SEVERE_DRIFT = "severe_drift"


class DriftPattern(str, Enum):
    NO_DRIFT        = "no_drift"
    LEVEL_DOWNGRADE  = "level_downgrade"    # C-suite → manager
    FUNCTION_SHIFT   = "function_shift"     # technical → business or vice versa
    SPONSOR_LOSS     = "sponsor_loss"       # exec sponsor gone quiet
    COMMITTEE_DILUTION = "committee_dilution"  # decision committee expanded, diluted influence
    MULTI_DRIFT      = "multi_drift"        # multiple drift signals


class BuyerAlignment(str, Enum):
    STRONGLY_ALIGNED  = "strongly_aligned"
    PARTIALLY_ALIGNED = "partially_aligned"
    MISALIGNED        = "misaligned"
    DISCONNECTED      = "disconnected"


class DriftAction(str, Enum):
    MAINTAIN      = "maintain"
    REQUALIFY     = "requalify"
    RE_ENGAGE_EXEC = "re_engage_exec"
    REALIGN_NOW   = "realign_now"


@dataclass
class BuyerPersonaDriftInput:
    deal_id:                        str
    deal_name:                      str
    rep_id:                         str
    target_persona_level:           str   # e.g. "C-suite", "VP", "Director", "Manager"
    target_persona_function:        str   # e.g. "technical", "business", "finance", "operations"
    current_primary_contact_level:  str   # actual person engaging
    current_primary_contact_function: str
    original_exec_sponsor_active:   int   # 1 if original exec sponsor still engaged
    exec_sponsor_last_active_days:  int   # days since exec sponsor engaged
    decision_committee_size_initial: int  # committee size at qualification
    decision_committee_size_current: int  # committee size now
    c_suite_meetings_initial_30d:   int   # C-suite/VP meetings in first 30 days
    c_suite_meetings_recent_30d:    int   # C-suite/VP meetings in last 30 days
    technical_contacts_engaged:     int   # number of technical contacts engaged
    business_contacts_engaged:      int   # number of business decision makers engaged
    deal_value:                     float
    days_since_qualification:       int   # how long since deal was qualified
    persona_match_score_at_open:    float # 0-100, how well initial contact matched ICP
    current_persona_match_score:    float # 0-100, how well current contacts match ICP
    budget_authority_confirmed:     int   # 1 if budget authority confirmed with current contacts
    champion_is_target_persona:     int   # 1 if champion matches target persona level/function
    blockers_are_non_target:        int   # 1 if the main blockers are people outside target persona


@dataclass
class BuyerPersonaDriftResult:
    deal_id:                    str
    deal_name:                  str
    drift_severity:             PersonaDriftSeverity
    drift_pattern:              DriftPattern
    buyer_alignment:            BuyerAlignment
    drift_action:               DriftAction
    level_drift_score:          float   # 0-100
    function_drift_score:       float   # 0-100
    exec_disengagement_score:   float   # 0-100
    committee_dilution_score:   float   # 0-100
    persona_drift_composite:    float   # 0-100
    deal_misalignment_risk:     float   # $ at risk due to persona drift
    realignment_probability:    float   # 0-100
    is_drifted:                 bool
    needs_exec_reengagement:    bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                  self.deal_id,
            "deal_name":                self.deal_name,
            "drift_severity":           self.drift_severity.value,
            "drift_pattern":            self.drift_pattern.value,
            "buyer_alignment":          self.buyer_alignment.value,
            "drift_action":             self.drift_action.value,
            "level_drift_score":        self.level_drift_score,
            "function_drift_score":     self.function_drift_score,
            "exec_disengagement_score": self.exec_disengagement_score,
            "committee_dilution_score": self.committee_dilution_score,
            "persona_drift_composite":  self.persona_drift_composite,
            "deal_misalignment_risk":   self.deal_misalignment_risk,
            "realignment_probability":  self.realignment_probability,
            "is_drifted":               self.is_drifted,
            "needs_exec_reengagement":  self.needs_exec_reengagement,
        }


_LEVEL_RANK = {
    "c-suite": 4, "c_suite": 4, "csuite": 4,
    "vp": 3, "vice president": 3,
    "director": 2,
    "manager": 1,
    "individual contributor": 0, "ic": 0, "individual_contributor": 0,
}


def _level_rank(level: str) -> int:
    return _LEVEL_RANK.get(level.lower().strip(), 1)


_FUNC_GROUPS = {
    "technical": {"technical", "engineering", "it", "devops", "security", "data"},
    "business":  {"business", "sales", "marketing", "product", "strategy", "operations", "ops"},
    "finance":   {"finance", "procurement", "legal", "compliance", "accounting"},
}


def _func_group(func: str) -> str:
    f = func.lower().strip()
    for group, members in _FUNC_GROUPS.items():
        if f in members or f == group:
            return group
    return "other"


class BuyerPersonaDriftEngine:
    def __init__(self) -> None:
        self._results: list[BuyerPersonaDriftResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: BuyerPersonaDriftInput) -> BuyerPersonaDriftResult:
        lvl_drift   = self._level_drift_score(inp)
        func_drift  = self._function_drift_score(inp)
        exec_dis    = self._exec_disengagement_score(inp)
        comm_dil    = self._committee_dilution_score(inp)
        composite   = self._composite(lvl_drift, func_drift, exec_dis, comm_dil)
        severity    = self._drift_severity(composite)
        pattern     = self._drift_pattern(lvl_drift, func_drift, exec_dis, comm_dil)
        alignment   = self._buyer_alignment(inp, composite)
        is_drifted  = composite >= 50.0
        needs_exec  = exec_dis >= 60.0 or (not inp.original_exec_sponsor_active and inp.deal_value >= 100_000)
        action      = self._drift_action(severity, is_drifted, needs_exec)
        realign_p   = self._realignment_probability(inp, composite)
        at_risk     = inp.deal_value * (composite / 100.0)

        result = BuyerPersonaDriftResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            drift_severity=severity,
            drift_pattern=pattern,
            buyer_alignment=alignment,
            drift_action=action,
            level_drift_score=lvl_drift,
            function_drift_score=func_drift,
            exec_disengagement_score=exec_dis,
            committee_dilution_score=comm_dil,
            persona_drift_composite=composite,
            deal_misalignment_risk=round(at_risk, 2),
            realignment_probability=realign_p,
            is_drifted=is_drifted,
            needs_exec_reengagement=needs_exec,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[BuyerPersonaDriftInput]) -> list[BuyerPersonaDriftResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def drifted_deals(self) -> list[BuyerPersonaDriftResult]:
        return [r for r in self._results if r.is_drifted]

    @property
    def exec_reengagement_needed(self) -> list[BuyerPersonaDriftResult]:
        return [r for r in self._results if r.needs_exec_reengagement]

    @property
    def total_misalignment_risk(self) -> float:
        return round(sum(r.deal_misalignment_risk for r in self._results), 2)

    @property
    def avg_realignment_probability(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.realignment_probability for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _level_drift_score(self, inp: BuyerPersonaDriftInput) -> float:
        target_rank  = _level_rank(inp.target_persona_level)
        current_rank = _level_rank(inp.current_primary_contact_level)
        gap = target_rank - current_rank
        if gap <= 0:
            score = 0.0
        elif gap == 1:
            score = 35.0
        elif gap == 2:
            score = 65.0
        else:
            score = 90.0
        # Amplify if exec meetings dropped sharply
        if inp.c_suite_meetings_initial_30d > 0:
            drop_ratio = (inp.c_suite_meetings_initial_30d - inp.c_suite_meetings_recent_30d) / inp.c_suite_meetings_initial_30d
            if drop_ratio > 0:
                score = min(100.0, score + drop_ratio * 20.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _function_drift_score(self, inp: BuyerPersonaDriftInput) -> float:
        target_grp  = _func_group(inp.target_persona_function)
        current_grp = _func_group(inp.current_primary_contact_function)
        if target_grp == current_grp:
            base = 0.0
        elif target_grp == "other" or current_grp == "other":
            base = 20.0
        else:
            base = 55.0
        # Penalty: blocker outside target persona
        if inp.blockers_are_non_target:
            base = min(100.0, base + 25.0)
        # Penalty: no budget authority with current contacts
        if not inp.budget_authority_confirmed:
            base = min(100.0, base + 20.0)
        return round(max(0.0, min(100.0, base)), 1)

    def _exec_disengagement_score(self, inp: BuyerPersonaDriftInput) -> float:
        score = 0.0
        if not inp.original_exec_sponsor_active:
            score += 45.0
        days = inp.exec_sponsor_last_active_days
        if days >= 30:
            score += min(35.0, days * 0.7)
        elif days >= 14:
            score += days * 0.5
        # C-suite meeting collapse
        if inp.c_suite_meetings_initial_30d > 0:
            drop = (inp.c_suite_meetings_initial_30d - inp.c_suite_meetings_recent_30d) / inp.c_suite_meetings_initial_30d
            if drop > 0:
                score += min(20.0, drop * 30.0)
        elif inp.c_suite_meetings_recent_30d == 0:
            score += 15.0
        return round(max(0.0, min(100.0, score)), 1)

    def _committee_dilution_score(self, inp: BuyerPersonaDriftInput) -> float:
        score = 0.0
        if inp.decision_committee_size_initial > 0:
            growth = (inp.decision_committee_size_current - inp.decision_committee_size_initial) / inp.decision_committee_size_initial
            if growth > 0.5:
                score += min(50.0, growth * 60.0)
        # Champion not matching target persona
        if not inp.champion_is_target_persona:
            score += 30.0
        # Persona match score drop
        match_drop = inp.persona_match_score_at_open - inp.current_persona_match_score
        if match_drop > 0:
            score += min(20.0, match_drop * 0.4)
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        lvl: float,
        func: float,
        exec_dis: float,
        comm: float,
    ) -> float:
        composite = lvl * 0.30 + exec_dis * 0.30 + func * 0.25 + comm * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _drift_severity(self, composite: float) -> PersonaDriftSeverity:
        if composite >= 65:
            return PersonaDriftSeverity.SEVERE_DRIFT
        if composite >= 45:
            return PersonaDriftSeverity.MODERATE_DRIFT
        if composite >= 25:
            return PersonaDriftSeverity.MINOR_DRIFT
        return PersonaDriftSeverity.ALIGNED

    def _drift_pattern(
        self,
        lvl: float,
        func: float,
        exec_dis: float,
        comm: float,
    ) -> DriftPattern:
        signals = sum([lvl >= 50, func >= 50, exec_dis >= 50, comm >= 40])
        if signals >= 2:
            return DriftPattern.MULTI_DRIFT
        if exec_dis >= 50:
            return DriftPattern.SPONSOR_LOSS
        if lvl >= 50:
            return DriftPattern.LEVEL_DOWNGRADE
        if func >= 50:
            return DriftPattern.FUNCTION_SHIFT
        if comm >= 40:
            return DriftPattern.COMMITTEE_DILUTION
        return DriftPattern.NO_DRIFT

    def _buyer_alignment(self, inp: BuyerPersonaDriftInput, composite: float) -> BuyerAlignment:
        if composite >= 65 or (not inp.budget_authority_confirmed and composite >= 45):
            return BuyerAlignment.DISCONNECTED
        if composite >= 45:
            return BuyerAlignment.MISALIGNED
        if composite >= 25 or not inp.champion_is_target_persona:
            return BuyerAlignment.PARTIALLY_ALIGNED
        return BuyerAlignment.STRONGLY_ALIGNED

    def _realignment_probability(self, inp: BuyerPersonaDriftInput, composite: float) -> float:
        base = max(0.0, 100.0 - composite)
        if inp.budget_authority_confirmed:
            base = min(100.0, base + 10.0)
        if inp.champion_is_target_persona:
            base = min(100.0, base + 8.0)
        base -= inp.exec_sponsor_last_active_days * 0.5
        if not inp.original_exec_sponsor_active:
            base -= 15.0
        return round(max(0.0, min(100.0, base)), 1)

    def _drift_action(
        self,
        severity: PersonaDriftSeverity,
        is_drifted: bool,
        needs_exec: bool,
    ) -> DriftAction:
        if needs_exec or severity == PersonaDriftSeverity.SEVERE_DRIFT:
            return DriftAction.REALIGN_NOW
        if is_drifted or severity == PersonaDriftSeverity.MODERATE_DRIFT:
            return DriftAction.RE_ENGAGE_EXEC
        if severity == PersonaDriftSeverity.MINOR_DRIFT:
            return DriftAction.REQUALIFY
        return DriftAction.MAINTAIN

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "severity_counts":              {},
                "pattern_counts":               {},
                "alignment_counts":             {},
                "action_counts":                {},
                "avg_persona_drift_composite":  0.0,
                "total_misalignment_risk":      0.0,
                "drifted_count":                0,
                "exec_reengagement_count":      0,
                "avg_level_drift_score":        0.0,
                "avg_function_drift_score":     0.0,
                "avg_exec_disengagement_score": 0.0,
                "avg_realignment_probability":  0.0,
            }

        severity_counts:  dict[str, int] = {}
        pattern_counts:   dict[str, int] = {}
        alignment_counts: dict[str, int] = {}
        action_counts:    dict[str, int] = {}
        total_comp  = 0.0
        total_lvl   = 0.0
        total_func  = 0.0
        total_exec  = 0.0
        total_real  = 0.0

        for r in self._results:
            severity_counts[r.drift_severity.value]  = severity_counts.get(r.drift_severity.value, 0) + 1
            pattern_counts[r.drift_pattern.value]    = pattern_counts.get(r.drift_pattern.value, 0) + 1
            alignment_counts[r.buyer_alignment.value] = alignment_counts.get(r.buyer_alignment.value, 0) + 1
            action_counts[r.drift_action.value]      = action_counts.get(r.drift_action.value, 0) + 1
            total_comp += r.persona_drift_composite
            total_lvl  += r.level_drift_score
            total_func += r.function_drift_score
            total_exec += r.exec_disengagement_score
            total_real += r.realignment_probability

        return {
            "total":                        n,
            "severity_counts":              severity_counts,
            "pattern_counts":               pattern_counts,
            "alignment_counts":             alignment_counts,
            "action_counts":                action_counts,
            "avg_persona_drift_composite":  round(total_comp / n, 1),
            "total_misalignment_risk":      self.total_misalignment_risk,
            "drifted_count":                len(self.drifted_deals),
            "exec_reengagement_count":      len(self.exec_reengagement_needed),
            "avg_level_drift_score":        round(total_lvl / n, 1),
            "avg_function_drift_score":     round(total_func / n, 1),
            "avg_exec_disengagement_score": round(total_exec / n, 1),
            "avg_realignment_probability":  round(total_real / n, 1),
        }
