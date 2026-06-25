"""Personalized Learning Path Engine — detects missed-learning risk and tailors development interventions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LearningRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class LearningPattern(str, Enum):
    NONE = "none"
    PLATEAU_RISK = "plateau_risk"
    DISENGAGED_LEARNER = "disengaged_learner"
    HIGH_POTENTIAL_REDIRECT = "high_potential_redirect"
    KNOWLEDGE_HOARDING = "knowledge_hoarding"
    LEARNING_STYLE_CONFLICT = "learning_style_conflict"


class LearningSeverity(str, Enum):
    THRIVING = "thriving"
    PROGRESSING = "progressing"
    STALLING = "stalling"
    REGRESSING = "regressing"


class LearningAction(str, Enum):
    NO_ACTION = "no_action"
    PATH_MONITORING = "path_monitoring"
    CONTENT_REFRESH = "content_refresh"
    COACHING_SESSION = "coaching_session"
    CHALLENGE_ASSIGNMENT = "challenge_assignment"
    PEER_LEARNING_GROUP = "peer_learning_group"
    MENTORSHIP_MATCH = "mentorship_match"
    INTENSIVE_BOOTCAMP = "intensive_bootcamp"
    CAREER_PATH_REDESIGN = "career_path_redesign"


@dataclass
class LearningInput:
    learner_id: str
    role: str
    region: str
    learning_completion_rate_pct: float            # 0-1
    knowledge_retention_score: float               # 0-1
    skill_application_rate_pct: float              # 0-1, % skills applied on job
    learning_velocity_percentile: float            # 0-1, vs peers
    engagement_score: float                        # 0-1
    content_relevance_rating: float                # 0-1
    learning_streak_days: int
    assessment_pass_rate_pct: float                # 0-1
    peer_collaboration_score: float                # 0-1
    curiosity_index: float                         # 0-1
    ambition_alignment_score: float                # 0-1, match to stated goals
    strength_utilization_pct: float                # 0-1
    learning_style_mismatch_score: float           # 0-1, 1=bad mismatch
    time_since_last_learning_days: int
    manager_development_support_score: float       # 0-1
    external_learning_initiative_score: float      # 0-1, 1=proactive self-learning
    career_goal_clarity_score: float               # 0-1


@dataclass
class LearningResult:
    learner_id: str
    region: str
    learning_risk: LearningRisk
    learning_pattern: LearningPattern
    learning_severity: LearningSeverity
    recommended_action: LearningAction
    engagement_score_calc: float
    retention_score: float
    application_score: float
    alignment_score: float
    learning_composite: float
    has_learning_gap: bool
    requires_path_adjustment: bool
    estimated_learning_velocity_index: float       # 0-10
    learning_signal: str

    def to_dict(self) -> dict:
        return {
            "learner_id": self.learner_id,
            "region": self.region,
            "learning_risk": self.learning_risk.value,
            "learning_pattern": self.learning_pattern.value,
            "learning_severity": self.learning_severity.value,
            "recommended_action": self.recommended_action.value,
            "engagement_score_calc": self.engagement_score_calc,
            "retention_score": self.retention_score,
            "application_score": self.application_score,
            "alignment_score": self.alignment_score,
            "learning_composite": self.learning_composite,
            "has_learning_gap": self.has_learning_gap,
            "requires_path_adjustment": self.requires_path_adjustment,
            "estimated_learning_velocity_index": self.estimated_learning_velocity_index,
            "learning_signal": self.learning_signal,
        }


# ── sub-score calculators ─────────────────────────────────────────────────────

def _engagement_score_calc(inp: LearningInput) -> float:
    score = 0.0
    # learning_completion_rate_pct
    if inp.learning_completion_rate_pct <= 0.40:
        score += 40
    elif inp.learning_completion_rate_pct <= 0.65:
        score += 22
    elif inp.learning_completion_rate_pct <= 0.80:
        score += 8
    # engagement_score (input field)
    if inp.engagement_score <= 0.35:
        score += 35
    elif inp.engagement_score <= 0.55:
        score += 18
    elif inp.engagement_score <= 0.72:
        score += 6
    # time_since_last_learning_days
    if inp.time_since_last_learning_days >= 30:
        score += 25
    elif inp.time_since_last_learning_days >= 14:
        score += 12
    return round(min(score, 100.0), 2)


def _retention_score(inp: LearningInput) -> float:
    score = 0.0
    # knowledge_retention_score
    if inp.knowledge_retention_score <= 0.40:
        score += 40
    elif inp.knowledge_retention_score <= 0.60:
        score += 22
    elif inp.knowledge_retention_score <= 0.78:
        score += 8
    # assessment_pass_rate_pct
    if inp.assessment_pass_rate_pct <= 0.50:
        score += 35
    elif inp.assessment_pass_rate_pct <= 0.68:
        score += 18
    elif inp.assessment_pass_rate_pct <= 0.80:
        score += 6
    # learning_streak_days
    if inp.learning_streak_days <= 3:
        score += 25
    elif inp.learning_streak_days <= 10:
        score += 12
    return round(min(score, 100.0), 2)


def _application_score(inp: LearningInput) -> float:
    score = 0.0
    # skill_application_rate_pct
    if inp.skill_application_rate_pct <= 0.30:
        score += 45
    elif inp.skill_application_rate_pct <= 0.50:
        score += 25
    elif inp.skill_application_rate_pct <= 0.68:
        score += 10
    # learning_style_mismatch_score
    if inp.learning_style_mismatch_score >= 0.60:
        score += 30
    elif inp.learning_style_mismatch_score >= 0.35:
        score += 15
    # manager_development_support_score
    if inp.manager_development_support_score <= 0.30:
        score += 25
    elif inp.manager_development_support_score <= 0.55:
        score += 12
    return round(min(score, 100.0), 2)


def _alignment_score(inp: LearningInput) -> float:
    score = 0.0
    # ambition_alignment_score
    if inp.ambition_alignment_score <= 0.30:
        score += 40
    elif inp.ambition_alignment_score <= 0.50:
        score += 22
    elif inp.ambition_alignment_score <= 0.68:
        score += 8
    # career_goal_clarity_score
    if inp.career_goal_clarity_score <= 0.30:
        score += 35
    elif inp.career_goal_clarity_score <= 0.55:
        score += 18
    # curiosity_index
    if inp.curiosity_index <= 0.25:
        score += 25
    elif inp.curiosity_index <= 0.50:
        score += 12
    return round(min(score, 100.0), 2)


def _composite(eng: float, ret: float, app: float, aln: float) -> float:
    return round(eng * 0.30 + ret * 0.25 + app * 0.25 + aln * 0.20, 2)


def _risk(composite: float) -> LearningRisk:
    if composite >= 60:
        return LearningRisk.CRITICAL
    if composite >= 40:
        return LearningRisk.HIGH
    if composite >= 20:
        return LearningRisk.MODERATE
    return LearningRisk.LOW


def _severity(composite: float) -> LearningSeverity:
    if composite >= 60:
        return LearningSeverity.REGRESSING
    if composite >= 40:
        return LearningSeverity.STALLING
    if composite >= 20:
        return LearningSeverity.PROGRESSING
    return LearningSeverity.THRIVING


def _pattern(inp: LearningInput) -> LearningPattern:
    if inp.knowledge_retention_score <= 0.45 and inp.learning_velocity_percentile <= 0.40:
        return LearningPattern.PLATEAU_RISK
    if inp.engagement_score <= 0.35 and inp.time_since_last_learning_days >= 21:
        return LearningPattern.DISENGAGED_LEARNER
    if inp.learning_velocity_percentile >= 0.80 and inp.ambition_alignment_score <= 0.35:
        return LearningPattern.HIGH_POTENTIAL_REDIRECT
    if inp.peer_collaboration_score <= 0.25 and inp.external_learning_initiative_score >= 0.70:
        return LearningPattern.KNOWLEDGE_HOARDING
    if inp.learning_style_mismatch_score >= 0.55 and inp.assessment_pass_rate_pct <= 0.55:
        return LearningPattern.LEARNING_STYLE_CONFLICT
    return LearningPattern.NONE


def _action(risk: LearningRisk, pattern: LearningPattern) -> LearningAction:
    if risk == LearningRisk.CRITICAL:
        if pattern in (LearningPattern.PLATEAU_RISK, LearningPattern.DISENGAGED_LEARNER):
            return LearningAction.INTENSIVE_BOOTCAMP
        return LearningAction.CAREER_PATH_REDESIGN
    if risk == LearningRisk.HIGH:
        if pattern == LearningPattern.PLATEAU_RISK:
            return LearningAction.CONTENT_REFRESH
        if pattern == LearningPattern.DISENGAGED_LEARNER:
            return LearningAction.COACHING_SESSION
        if pattern == LearningPattern.HIGH_POTENTIAL_REDIRECT:
            return LearningAction.MENTORSHIP_MATCH
        if pattern == LearningPattern.KNOWLEDGE_HOARDING:
            return LearningAction.PEER_LEARNING_GROUP
        if pattern == LearningPattern.LEARNING_STYLE_CONFLICT:
            return LearningAction.CHALLENGE_ASSIGNMENT
        return LearningAction.PATH_MONITORING
    if risk == LearningRisk.MODERATE:
        return LearningAction.COACHING_SESSION
    return LearningAction.NO_ACTION


def _signal(inp: LearningInput, comp: float, risk: LearningRisk) -> str:
    if comp < 20:
        return "Learning engagement strong — completion, retention, application and alignment exceeding benchmarks"
    label = risk.value.replace("_", " ").title()
    return (
        f"{label} — {round(inp.learning_completion_rate_pct * 100)}% completion"
        f" — retention {round(inp.knowledge_retention_score * 100)}%"
        f" — {inp.time_since_last_learning_days}d since last learning"
        f" — composite {round(comp)}"
    )


class PersonalizedLearningPathEngine:
    """Detects missed-learning risk and recommends personalised path interventions."""

    def __init__(self) -> None:
        self._results: list[LearningResult] = []

    def analyze(self, inp: LearningInput) -> LearningResult:
        eng_s = _engagement_score_calc(inp)
        ret_s = _retention_score(inp)
        app_s = _application_score(inp)
        aln_s = _alignment_score(inp)
        learn_comp = _composite(eng_s, ret_s, app_s, aln_s)

        risk = _risk(learn_comp)
        severity = _severity(learn_comp)
        pattern = _pattern(inp)
        action = _action(risk, pattern)

        has_gap = learn_comp >= 40 or inp.learning_completion_rate_pct <= 0.55 or inp.time_since_last_learning_days >= 21
        requires_adjustment = learn_comp >= 25 or inp.ambition_alignment_score <= 0.45 or inp.learning_style_mismatch_score >= 0.45
        velocity_index = round(min((1 - inp.learning_velocity_percentile) * (learn_comp / 100 + 0.01) * 10, 10.0), 2)
        sig = _signal(inp, learn_comp, risk)

        result = LearningResult(
            learner_id=inp.learner_id,
            region=inp.region,
            learning_risk=risk,
            learning_pattern=pattern,
            learning_severity=severity,
            recommended_action=action,
            engagement_score_calc=eng_s,
            retention_score=ret_s,
            application_score=app_s,
            alignment_score=aln_s,
            learning_composite=learn_comp,
            has_learning_gap=has_gap,
            requires_path_adjustment=requires_adjustment,
            estimated_learning_velocity_index=velocity_index,
            learning_signal=sig,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[LearningInput]) -> list[LearningResult]:
        for inp in inputs:
            self.analyze(inp)
        self._results.sort(key=lambda r: r.learning_composite, reverse=True)
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
                "avg_learning_composite": 0.0,
                "learning_gap_count": 0,
                "path_adjustment_count": 0,
                "avg_engagement_score_calc": 0.0,
                "avg_retention_score": 0.0,
                "avg_application_score": 0.0,
                "avg_alignment_score": 0.0,
                "avg_estimated_learning_velocity_index": 0.0,
            }
        risk_counts: dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_comp = total_eng = total_ret = total_app = total_aln = total_vel = 0.0
        for r in self._results:
            risk_counts[r.learning_risk.value] = risk_counts.get(r.learning_risk.value, 0) + 1
            pattern_counts[r.learning_pattern.value] = pattern_counts.get(r.learning_pattern.value, 0) + 1
            severity_counts[r.learning_severity.value] = severity_counts.get(r.learning_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.learning_composite
            total_eng += r.engagement_score_calc
            total_ret += r.retention_score
            total_app += r.application_score
            total_aln += r.alignment_score
            total_vel += r.estimated_learning_velocity_index
        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_learning_composite": round(total_comp / n, 2),
            "learning_gap_count": sum(1 for r in self._results if r.has_learning_gap),
            "path_adjustment_count": sum(1 for r in self._results if r.requires_path_adjustment),
            "avg_engagement_score_calc": round(total_eng / n, 2),
            "avg_retention_score": round(total_ret / n, 2),
            "avg_application_score": round(total_app / n, 2),
            "avg_alignment_score": round(total_aln / n, 2),
            "avg_estimated_learning_velocity_index": round(total_vel / n, 2),
        }
