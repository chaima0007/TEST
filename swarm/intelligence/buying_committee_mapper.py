from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CommitteeCoverage(str, Enum):
    FULL_COVERAGE   = "full_coverage"
    PARTIAL         = "partial"
    THIN            = "thin"
    SINGLE_THREADED = "single_threaded"


class CommitteeRisk(str, Enum):
    LOW         = "low"
    MODERATE    = "moderate"
    HIGH        = "high"
    CRITICAL    = "critical"


class DealComplexity(str, Enum):
    SIMPLE      = "simple"
    STANDARD    = "standard"
    COMPLEX     = "complex"
    ENTERPRISE  = "enterprise"


class CommitteeAction(str, Enum):
    MAINTAIN            = "maintain"
    EXPAND_COVERAGE     = "expand_coverage"
    NEUTRALIZE_BLOCKER  = "neutralize_blocker"
    EXECUTIVE_ALIGNMENT = "executive_alignment"


@dataclass
class BuyingCommitteeInput:
    deal_id:                        str
    deal_name:                      str
    rep_id:                         str
    economic_buyer_identified:      int     # 1 if economic buyer known
    economic_buyer_engaged:         int     # 1 if economic buyer actively engaged
    champion_identified:            int     # 1 if champion identified
    champion_engaged:               int     # 1 if champion engaged
    technical_evaluator_identified: int     # 1 if technical evaluator identified
    technical_evaluator_engaged:    int     # 1 if technical eval engaged
    end_user_identified:            int     # 1 if end user identified
    end_user_engaged:               int     # 1 if end user engaged
    blocker_identified:             int     # 1 if known blocker exists
    blocker_neutralized:            int     # 1 if blocker has been neutralized
    total_stakeholders_mapped:      int     # total stakeholders in deal
    total_stakeholders_engaged:     int     # stakeholders actively engaged
    exec_sponsor_exists:            int     # 1 if exec sponsor engaged
    procurement_involved:           int     # 1 if procurement is involved
    legal_involved:                 int     # 1 if legal is involved
    deal_size_usd:                  float
    deal_stage_numeric:             int     # 1-6
    days_to_close:                  int
    last_new_stakeholder_days_ago:  int     # days since a new stakeholder was added


@dataclass
class BuyingCommitteeResult:
    deal_id:                    str
    deal_name:                  str
    committee_coverage:         CommitteeCoverage
    committee_risk:             CommitteeRisk
    deal_complexity:            DealComplexity
    committee_action:           CommitteeAction
    role_coverage_score:        float   # 0-100
    engagement_breadth_score:   float   # 0-100
    blocker_management_score:   float   # 0-100
    late_stage_alignment_score: float   # 0-100
    committee_composite:        float   # 0-100
    coverage_ratio:             float   # engaged / mapped
    missing_role_count:         int     # # of key roles not yet identified
    is_well_covered:            bool
    needs_expansion:            bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                      self.deal_id,
            "deal_name":                    self.deal_name,
            "committee_coverage":           self.committee_coverage.value,
            "committee_risk":               self.committee_risk.value,
            "deal_complexity":              self.deal_complexity.value,
            "committee_action":             self.committee_action.value,
            "role_coverage_score":          self.role_coverage_score,
            "engagement_breadth_score":     self.engagement_breadth_score,
            "blocker_management_score":     self.blocker_management_score,
            "late_stage_alignment_score":   self.late_stage_alignment_score,
            "committee_composite":          self.committee_composite,
            "coverage_ratio":               self.coverage_ratio,
            "missing_role_count":           self.missing_role_count,
            "is_well_covered":              self.is_well_covered,
            "needs_expansion":              self.needs_expansion,
        }


class BuyingCommitteeMapper:
    def __init__(self) -> None:
        self._results: list[BuyingCommitteeResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def map(self, inp: BuyingCommitteeInput) -> BuyingCommitteeResult:
        role_cov    = self._role_coverage_score(inp)
        breadth     = self._engagement_breadth_score(inp)
        blocker_mgmt = self._blocker_management_score(inp)
        late_align  = self._late_stage_alignment_score(inp)
        composite   = self._composite(role_cov, breadth, blocker_mgmt, late_align)
        coverage    = self._committee_coverage(composite, inp)
        risk        = self._committee_risk(composite, inp)
        complexity  = self._deal_complexity(inp)
        cov_ratio   = (
            inp.total_stakeholders_engaged / inp.total_stakeholders_mapped
            if inp.total_stakeholders_mapped > 0 else 0.0
        )
        missing = self._missing_role_count(inp)
        is_covered  = composite >= 65 and missing == 0
        needs_exp   = composite < 50 or missing >= 2 or inp.total_stakeholders_engaged < 3
        action = self._committee_action(risk, needs_exp, inp)

        result = BuyingCommitteeResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            committee_coverage=coverage,
            committee_risk=risk,
            deal_complexity=complexity,
            committee_action=action,
            role_coverage_score=role_cov,
            engagement_breadth_score=breadth,
            blocker_management_score=blocker_mgmt,
            late_stage_alignment_score=late_align,
            committee_composite=composite,
            coverage_ratio=round(cov_ratio, 2),
            missing_role_count=missing,
            is_well_covered=is_covered,
            needs_expansion=needs_exp,
        )
        self._results.append(result)
        return result

    def map_batch(self, inputs: list[BuyingCommitteeInput]) -> list[BuyingCommitteeResult]:
        return [self.map(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def well_covered_deals(self) -> list[BuyingCommitteeResult]:
        return [r for r in self._results if r.is_well_covered]

    @property
    def expansion_needed_queue(self) -> list[BuyingCommitteeResult]:
        return [r for r in self._results if r.needs_expansion]

    @property
    def avg_committee_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.committee_composite for r in self._results) / len(self._results), 1)

    @property
    def avg_coverage_ratio(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.coverage_ratio for r in self._results) / len(self._results), 2)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _role_coverage_score(self, inp: BuyingCommitteeInput) -> float:
        score = 0.0
        # Economic buyer (critical, 30 pts)
        if inp.economic_buyer_identified:
            score += 15.0
        if inp.economic_buyer_engaged:
            score += 15.0
        # Champion (critical, 25 pts)
        if inp.champion_identified:
            score += 12.0
        if inp.champion_engaged:
            score += 13.0
        # Technical evaluator (20 pts)
        if inp.technical_evaluator_identified:
            score += 10.0
        if inp.technical_evaluator_engaged:
            score += 10.0
        # End user (15 pts)
        if inp.end_user_identified:
            score += 7.0
        if inp.end_user_engaged:
            score += 8.0
        # Exec sponsor bonus (10 pts)
        if inp.exec_sponsor_exists:
            score = min(100.0, score + 10.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _engagement_breadth_score(self, inp: BuyingCommitteeInput) -> float:
        score = 0.0
        # Total engaged
        engaged = inp.total_stakeholders_engaged
        if engaged >= 8:
            score += 40.0
        elif engaged >= 5:
            score += 28.0
        elif engaged >= 3:
            score += 16.0
        elif engaged >= 2:
            score += 8.0
        elif engaged >= 1:
            score += 3.0
        # Coverage ratio
        if inp.total_stakeholders_mapped > 0:
            ratio = inp.total_stakeholders_engaged / inp.total_stakeholders_mapped
            if ratio >= 0.8:
                score += 35.0
            elif ratio >= 0.6:
                score += 22.0
            elif ratio >= 0.4:
                score += 12.0
        # New stakeholder added recently
        if inp.last_new_stakeholder_days_ago <= 14:
            score += 15.0
        elif inp.last_new_stakeholder_days_ago <= 30:
            score += 8.0
        # Exec sponsor bonus
        if inp.exec_sponsor_exists:
            score = min(100.0, score + 10.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _blocker_management_score(self, inp: BuyingCommitteeInput) -> float:
        # No known blocker = good baseline
        if not inp.blocker_identified:
            return 75.0
        # Blocker identified and neutralized
        if inp.blocker_neutralized:
            return 80.0
        # Blocker identified but NOT neutralized
        base = 20.0
        # Late stage with un-neutralized blocker = very dangerous
        if inp.deal_stage_numeric >= 4:
            base -= 10.0
        # Near close with blocker = critical
        if inp.days_to_close <= 14:
            base -= 10.0
        return round(max(0.0, min(100.0, base)), 1)

    def _late_stage_alignment_score(self, inp: BuyingCommitteeInput) -> float:
        score = 0.0
        stage = inp.deal_stage_numeric
        # Economic buyer engaged in late stage
        if inp.economic_buyer_engaged and stage >= 4:
            score += 35.0
        elif inp.economic_buyer_engaged:
            score += 20.0
        # Exec sponsor in late stage
        if inp.exec_sponsor_exists and stage >= 4:
            score += 25.0
        elif inp.exec_sponsor_exists:
            score += 12.0
        # Procurement/legal signaling real process
        if inp.procurement_involved:
            score += 20.0
        if inp.legal_involved:
            score += 10.0
        # All 4 key roles engaged
        all_engaged = (
            inp.economic_buyer_engaged + inp.champion_engaged
            + inp.technical_evaluator_engaged + inp.end_user_engaged
        )
        if all_engaged == 4:
            score = min(100.0, score + 10.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        role_cov: float,
        breadth: float,
        blocker_mgmt: float,
        late_align: float,
    ) -> float:
        composite = role_cov * 0.35 + breadth * 0.30 + blocker_mgmt * 0.20 + late_align * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _missing_role_count(self, inp: BuyingCommitteeInput) -> int:
        missing = 0
        if not inp.economic_buyer_identified:
            missing += 1
        if not inp.champion_identified:
            missing += 1
        if not inp.technical_evaluator_identified:
            missing += 1
        if not inp.end_user_identified:
            missing += 1
        return missing

    def _committee_coverage(self, composite: float, inp: BuyingCommitteeInput) -> CommitteeCoverage:
        engaged = inp.total_stakeholders_engaged
        if composite >= 70 and engaged >= 5:
            return CommitteeCoverage.FULL_COVERAGE
        if composite >= 55 and engaged >= 3:
            return CommitteeCoverage.PARTIAL
        if engaged >= 2:
            return CommitteeCoverage.THIN
        return CommitteeCoverage.SINGLE_THREADED

    def _committee_risk(self, composite: float, inp: BuyingCommitteeInput) -> CommitteeRisk:
        if inp.total_stakeholders_engaged <= 1 or composite < 20:
            return CommitteeRisk.CRITICAL
        if composite < 35 or (inp.blocker_identified and not inp.blocker_neutralized and inp.deal_stage_numeric >= 4):
            return CommitteeRisk.HIGH
        if composite < 55:
            return CommitteeRisk.MODERATE
        return CommitteeRisk.LOW

    def _deal_complexity(self, inp: BuyingCommitteeInput) -> DealComplexity:
        if inp.deal_size_usd >= 500_000 or inp.total_stakeholders_mapped >= 10:
            return DealComplexity.ENTERPRISE
        if inp.deal_size_usd >= 150_000 or inp.total_stakeholders_mapped >= 6:
            return DealComplexity.COMPLEX
        if inp.deal_size_usd >= 50_000 or inp.total_stakeholders_mapped >= 3:
            return DealComplexity.STANDARD
        return DealComplexity.SIMPLE

    def _committee_action(
        self,
        risk: CommitteeRisk,
        needs_exp: bool,
        inp: BuyingCommitteeInput,
    ) -> CommitteeAction:
        if inp.blocker_identified and not inp.blocker_neutralized:
            return CommitteeAction.NEUTRALIZE_BLOCKER
        if not inp.economic_buyer_engaged and inp.deal_stage_numeric >= 3:
            return CommitteeAction.EXECUTIVE_ALIGNMENT
        if needs_exp or risk in (CommitteeRisk.HIGH, CommitteeRisk.CRITICAL):
            return CommitteeAction.EXPAND_COVERAGE
        return CommitteeAction.MAINTAIN

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "coverage_counts":              {},
                "risk_counts":                  {},
                "complexity_counts":            {},
                "action_counts":                {},
                "avg_committee_composite":      0.0,
                "avg_coverage_ratio":           0.0,
                "well_covered_count":           0,
                "expansion_needed_count":       0,
                "avg_role_coverage_score":      0.0,
                "avg_engagement_breadth_score": 0.0,
                "avg_blocker_management_score": 0.0,
                "avg_late_stage_alignment_score": 0.0,
            }

        coverage_counts:    dict[str, int] = {}
        risk_counts:        dict[str, int] = {}
        complexity_counts:  dict[str, int] = {}
        action_counts:      dict[str, int] = {}
        total_comp  = 0.0; total_cov  = 0.0; total_role = 0.0
        total_brd   = 0.0; total_blk  = 0.0; total_lat  = 0.0

        for r in self._results:
            coverage_counts[r.committee_coverage.value]  = coverage_counts.get(r.committee_coverage.value, 0) + 1
            risk_counts[r.committee_risk.value]          = risk_counts.get(r.committee_risk.value, 0) + 1
            complexity_counts[r.deal_complexity.value]   = complexity_counts.get(r.deal_complexity.value, 0) + 1
            action_counts[r.committee_action.value]      = action_counts.get(r.committee_action.value, 0) + 1
            total_comp += r.committee_composite
            total_cov  += r.coverage_ratio
            total_role += r.role_coverage_score
            total_brd  += r.engagement_breadth_score
            total_blk  += r.blocker_management_score
            total_lat  += r.late_stage_alignment_score

        return {
            "total":                            n,
            "coverage_counts":                  coverage_counts,
            "risk_counts":                      risk_counts,
            "complexity_counts":                complexity_counts,
            "action_counts":                    action_counts,
            "avg_committee_composite":          round(total_comp / n, 1),
            "avg_coverage_ratio":               round(total_cov / n, 2),
            "well_covered_count":               len(self.well_covered_deals),
            "expansion_needed_count":           len(self.expansion_needed_queue),
            "avg_role_coverage_score":          round(total_role / n, 1),
            "avg_engagement_breadth_score":     round(total_brd / n, 1),
            "avg_blocker_management_score":     round(total_blk / n, 1),
            "avg_late_stage_alignment_score":   round(total_lat / n, 1),
        }
