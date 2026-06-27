"""Knowledge Gap & Skills Analysis Engine — identifies skill gaps, market misalignment, and development needs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SkillRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class SkillPattern(str, Enum):
    NONE = "none"
    CRITICAL_SKILL_GAP = "critical_skill_gap"
    MARKET_MISMATCH = "market_mismatch"
    OBSOLESCENCE_RISK = "obsolescence_risk"
    LEADERSHIP_VOID = "leadership_void"
    DIGITAL_LITERACY_GAP = "digital_literacy_gap"


class SkillSeverity(str, Enum):
    PROFICIENT = "proficient"
    DEVELOPING = "developing"
    GAP = "gap"
    CRITICAL = "critical"


class SkillAction(str, Enum):
    NO_ACTION = "no_action"
    SKILL_MONITORING = "skill_monitoring"
    TARGETED_TRAINING = "targeted_training"
    MENTORING_PROGRAM = "mentoring_program"
    EXTERNAL_HIRING = "external_hiring"
    RESKILLING_INITIATIVE = "reskilling_initiative"
    LEADERSHIP_DEVELOPMENT = "leadership_development"
    DIGITAL_UPSKILLING = "digital_upskilling"
    EMERGENCY_CAPABILITY_BUILD = "emergency_capability_build"


@dataclass
class SkillInput:
    employee_id: str
    department: str
    region: str
    core_skill_proficiency_avg: float          # 0-1
    skill_assessment_score: float              # 0-1
    market_relevant_skills_pct: float          # 0-1
    emerging_skill_adoption_rate: float        # 0-1
    technical_skill_gap_score: float           # 0-1, 1=large gap
    soft_skill_gap_score: float                # 0-1
    leadership_readiness_score: float          # 0-1, 1=ready
    digital_tool_proficiency: float            # 0-1
    learning_velocity_score: float             # 0-1, speed of skill acquisition
    training_completion_rate_pct: float        # 0-1
    peer_knowledge_sharing_score: float        # 0-1
    industry_benchmark_gap_pct: float          # 0-1
    role_evolution_readiness: float            # 0-1, 1=ready for role changes
    certification_coverage_pct: float          # 0-1
    mentoring_engagement_score: float          # 0-1
    performance_trajectory: float              # 0-1, 1=improving
    time_in_role_months: int


@dataclass
class SkillResult:
    employee_id: str
    region: str
    skill_risk: SkillRisk
    skill_pattern: SkillPattern
    skill_severity: SkillSeverity
    recommended_action: SkillAction
    competency_score: float
    market_alignment_score: float
    leadership_score: float
    digital_score: float
    skill_composite: float
    has_skill_gap: bool
    requires_intervention: bool
    estimated_performance_impact: float        # 0-10
    skill_signal: str

    def to_dict(self) -> dict:
        return {
            "employee_id": self.employee_id,
            "region": self.region,
            "skill_risk": self.skill_risk.value,
            "skill_pattern": self.skill_pattern.value,
            "skill_severity": self.skill_severity.value,
            "recommended_action": self.recommended_action.value,
            "competency_score": self.competency_score,
            "market_alignment_score": self.market_alignment_score,
            "leadership_score": self.leadership_score,
            "digital_score": self.digital_score,
            "skill_composite": self.skill_composite,
            "has_skill_gap": self.has_skill_gap,
            "requires_intervention": self.requires_intervention,
            "estimated_performance_impact": self.estimated_performance_impact,
            "skill_signal": self.skill_signal,
        }


# ── sub-score calculators ─────────────────────────────────────────────────────

def _competency_score(inp: SkillInput) -> float:
    score = 0.0
    # core_skill_proficiency_avg
    if inp.core_skill_proficiency_avg <= 0.50:
        score += 40
    elif inp.core_skill_proficiency_avg <= 0.65:
        score += 22
    elif inp.core_skill_proficiency_avg <= 0.78:
        score += 8
    # training_completion_rate_pct
    if inp.training_completion_rate_pct <= 0.40:
        score += 35
    elif inp.training_completion_rate_pct <= 0.65:
        score += 18
    elif inp.training_completion_rate_pct <= 0.80:
        score += 6
    # performance_trajectory
    if inp.performance_trajectory <= 0.40:
        score += 25
    elif inp.performance_trajectory <= 0.60:
        score += 12
    return round(min(score, 100.0), 2)


def _market_alignment_score(inp: SkillInput) -> float:
    score = 0.0
    # market_relevant_skills_pct
    if inp.market_relevant_skills_pct <= 0.40:
        score += 40
    elif inp.market_relevant_skills_pct <= 0.60:
        score += 22
    elif inp.market_relevant_skills_pct <= 0.75:
        score += 8
    # industry_benchmark_gap_pct
    if inp.industry_benchmark_gap_pct >= 0.35:
        score += 35
    elif inp.industry_benchmark_gap_pct >= 0.20:
        score += 18
    elif inp.industry_benchmark_gap_pct >= 0.10:
        score += 6
    # emerging_skill_adoption_rate
    if inp.emerging_skill_adoption_rate <= 0.25:
        score += 25
    elif inp.emerging_skill_adoption_rate <= 0.50:
        score += 12
    return round(min(score, 100.0), 2)


def _leadership_score(inp: SkillInput) -> float:
    score = 0.0
    # leadership_readiness_score
    if inp.leadership_readiness_score <= 0.30:
        score += 45
    elif inp.leadership_readiness_score <= 0.50:
        score += 25
    elif inp.leadership_readiness_score <= 0.70:
        score += 10
    # peer_knowledge_sharing_score
    if inp.peer_knowledge_sharing_score <= 0.30:
        score += 30
    elif inp.peer_knowledge_sharing_score <= 0.55:
        score += 15
    # mentoring_engagement_score
    if inp.mentoring_engagement_score <= 0.20:
        score += 25
    elif inp.mentoring_engagement_score <= 0.45:
        score += 12
    return round(min(score, 100.0), 2)


def _digital_score(inp: SkillInput) -> float:
    score = 0.0
    # digital_tool_proficiency
    if inp.digital_tool_proficiency <= 0.35:
        score += 40
    elif inp.digital_tool_proficiency <= 0.55:
        score += 22
    elif inp.digital_tool_proficiency <= 0.72:
        score += 8
    # technical_skill_gap_score
    if inp.technical_skill_gap_score >= 0.60:
        score += 35
    elif inp.technical_skill_gap_score >= 0.40:
        score += 18
    elif inp.technical_skill_gap_score >= 0.20:
        score += 6
    # certification_coverage_pct
    if inp.certification_coverage_pct <= 0.30:
        score += 25
    elif inp.certification_coverage_pct <= 0.55:
        score += 12
    return round(min(score, 100.0), 2)


def _composite(comp: float, mkt: float, lead: float, dig: float) -> float:
    return round(comp * 0.30 + mkt * 0.25 + lead * 0.25 + dig * 0.20, 2)


def _risk(composite: float) -> SkillRisk:
    if composite >= 60:
        return SkillRisk.CRITICAL
    if composite >= 40:
        return SkillRisk.HIGH
    if composite >= 20:
        return SkillRisk.MODERATE
    return SkillRisk.LOW


def _severity(composite: float) -> SkillSeverity:
    if composite >= 60:
        return SkillSeverity.CRITICAL
    if composite >= 40:
        return SkillSeverity.GAP
    if composite >= 20:
        return SkillSeverity.DEVELOPING
    return SkillSeverity.PROFICIENT


def _pattern(inp: SkillInput) -> SkillPattern:
    if inp.core_skill_proficiency_avg <= 0.45 and inp.performance_trajectory <= 0.50:
        return SkillPattern.CRITICAL_SKILL_GAP
    if inp.market_relevant_skills_pct <= 0.45 and inp.industry_benchmark_gap_pct >= 0.30:
        return SkillPattern.MARKET_MISMATCH
    if inp.emerging_skill_adoption_rate <= 0.20 and inp.technical_skill_gap_score >= 0.55:
        return SkillPattern.OBSOLESCENCE_RISK
    if inp.leadership_readiness_score <= 0.35 and inp.peer_knowledge_sharing_score <= 0.35:
        return SkillPattern.LEADERSHIP_VOID
    if inp.digital_tool_proficiency <= 0.40 and inp.certification_coverage_pct <= 0.35:
        return SkillPattern.DIGITAL_LITERACY_GAP
    return SkillPattern.NONE


def _action(risk: SkillRisk, pattern: SkillPattern) -> SkillAction:
    if risk == SkillRisk.CRITICAL:
        if pattern in (SkillPattern.CRITICAL_SKILL_GAP, SkillPattern.MARKET_MISMATCH):
            return SkillAction.EMERGENCY_CAPABILITY_BUILD
        return SkillAction.RESKILLING_INITIATIVE
    if risk == SkillRisk.HIGH:
        if pattern == SkillPattern.CRITICAL_SKILL_GAP:
            return SkillAction.TARGETED_TRAINING
        if pattern == SkillPattern.MARKET_MISMATCH:
            return SkillAction.RESKILLING_INITIATIVE
        if pattern == SkillPattern.OBSOLESCENCE_RISK:
            return SkillAction.DIGITAL_UPSKILLING
        if pattern == SkillPattern.LEADERSHIP_VOID:
            return SkillAction.LEADERSHIP_DEVELOPMENT
        if pattern == SkillPattern.DIGITAL_LITERACY_GAP:
            return SkillAction.DIGITAL_UPSKILLING
        return SkillAction.SKILL_MONITORING
    if risk == SkillRisk.MODERATE:
        return SkillAction.MENTORING_PROGRAM
    return SkillAction.NO_ACTION


def _signal(inp: SkillInput, comp: float, risk: SkillRisk) -> str:
    if comp < 20:
        return "Skills profile strong — competency, market alignment, leadership and digital literacy meeting benchmarks"
    label = risk.value.replace("_", " ").title()
    return (
        f"{label} — {round(inp.core_skill_proficiency_avg * 100)}% core proficiency"
        f" — {round(inp.market_relevant_skills_pct * 100)}% market aligned"
        f" — digital {round(inp.digital_tool_proficiency * 100)}%"
        f" — composite {round(comp)}"
    )


class KnowledgeGapSkillsAnalysisEngine:
    """Identifies knowledge gaps, skill misalignments, and targeted development actions."""

    def __init__(self) -> None:
        self._results: list[SkillResult] = []

    def analyze(self, inp: SkillInput) -> SkillResult:
        comp_s = _competency_score(inp)
        mkt_s = _market_alignment_score(inp)
        lead_s = _leadership_score(inp)
        dig_s = _digital_score(inp)
        skill_comp = _composite(comp_s, mkt_s, lead_s, dig_s)

        risk = _risk(skill_comp)
        severity = _severity(skill_comp)
        pattern = _pattern(inp)
        action = _action(risk, pattern)

        has_gap = skill_comp >= 40 or inp.core_skill_proficiency_avg <= 0.60 or inp.industry_benchmark_gap_pct >= 0.25
        requires_intervention = skill_comp >= 25 or inp.leadership_readiness_score <= 0.45 or inp.digital_tool_proficiency <= 0.50
        perf_impact = round(min(skill_comp / 100 * (1 - inp.performance_trajectory + 0.01) * 10, 10.0), 2)
        sig = _signal(inp, skill_comp, risk)

        result = SkillResult(
            employee_id=inp.employee_id,
            region=inp.region,
            skill_risk=risk,
            skill_pattern=pattern,
            skill_severity=severity,
            recommended_action=action,
            competency_score=comp_s,
            market_alignment_score=mkt_s,
            leadership_score=lead_s,
            digital_score=dig_s,
            skill_composite=skill_comp,
            has_skill_gap=has_gap,
            requires_intervention=requires_intervention,
            estimated_performance_impact=perf_impact,
            skill_signal=sig,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[SkillInput]) -> list[SkillResult]:
        for inp in inputs:
            self.analyze(inp)
        self._results.sort(key=lambda r: r.skill_composite, reverse=True)
        return self._results

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
                "avg_skill_composite": 0.0,
                "skill_gap_count": 0,
                "intervention_count": 0,
                "avg_competency_score": 0.0,
                "avg_market_alignment_score": 0.0,
                "avg_leadership_score": 0.0,
                "avg_digital_score": 0.0,
                "avg_estimated_performance_impact": 0.0,
            }
        risk_counts: dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_comp = total_competency = total_market = total_leadership = total_digital = total_impact = 0.0
        for r in self._results:
            risk_counts[r.skill_risk.value] = risk_counts.get(r.skill_risk.value, 0) + 1
            pattern_counts[r.skill_pattern.value] = pattern_counts.get(r.skill_pattern.value, 0) + 1
            severity_counts[r.skill_severity.value] = severity_counts.get(r.skill_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.skill_composite
            total_competency += r.competency_score
            total_market += r.market_alignment_score
            total_leadership += r.leadership_score
            total_digital += r.digital_score
            total_impact += r.estimated_performance_impact
        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_skill_composite": round(total_comp / n, 2),
            "skill_gap_count": sum(1 for r in self._results if r.has_skill_gap),
            "intervention_count": sum(1 for r in self._results if r.requires_intervention),
            "avg_competency_score": round(total_competency / n, 2),
            "avg_market_alignment_score": round(total_market / n, 2),
            "avg_leadership_score": round(total_leadership / n, 2),
            "avg_digital_score": round(total_digital / n, 2),
            "avg_estimated_performance_impact": round(total_impact / n, 2),
        }
