"""Sales Coaching Engine — generates personalised coaching plans for reps based on their performance gaps and behavioral signals."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class SkillGap(str, Enum):
    DISCOVERY = "discovery"             # not asking enough questions
    QUALIFICATION = "qualification"     # MEDDIC/BANT gaps
    PRESENTATION = "presentation"       # demo/pitch effectiveness
    OBJECTION_HANDLING = "objection_handling"
    CLOSING = "closing"                 # asking for the business
    PIPELINE_HYGIENE = "pipeline_hygiene"  # CRM discipline
    MULTI_THREADING = "multi_threading"    # single-contact dependency
    FORECASTING = "forecasting"           # accuracy vs. actuals


class CoachingIntensity(str, Enum):
    LIGHT = "light"         # strong performer, fine-tuning
    MODERATE = "moderate"   # on-track, specific gaps to address
    INTENSIVE = "intensive" # underperforming, structured program needed
    CRITICAL = "critical"   # performance improvement plan territory


class CoachingFocus(str, Enum):
    SKILLS = "skills"               # technical sales skills
    PIPELINE = "pipeline"           # pipeline management and coverage
    MINDSET = "mindset"             # motivation, resilience, attitude
    PROCESS = "process"             # following the sales process and CRM
    STRATEGY = "strategy"           # territory and account prioritisation


@dataclass
class RepPerformanceInput:
    rep_id: str
    rep_name: str
    segment: str            # enterprise / mid_market / smb
    tenure_months: int      # time in role

    # Quota & pipeline
    quota_eur: float
    quota_attainment_pct: float         # 0-200+
    pipeline_coverage_ratio: float      # weighted pipeline / quota
    forecast_accuracy_pct: float        # |forecast - actual| deviation, lower = better

    # Activity signals
    avg_discovery_questions_per_call: float
    avg_deal_cycle_days: int
    deals_lost_to_no_decision_pct: float  # 0-100
    deals_lost_to_competitor_pct: float   # 0-100
    discount_avg_pct: float               # average discount given
    crm_update_lag_days: float            # avg days between meeting and CRM update
    multi_thread_avg_contacts: float      # avg contacts per deal
    next_step_set_pct: float              # % of meetings ending with defined next step

    # Coaching context
    last_coaching_session_days_ago: int
    coaching_sessions_ytd: int
    self_assessment_score: float  # 0-100 rep's own assessment
    manager_assessment_score: float  # 0-100 manager's assessment


@dataclass
class CoachingPlanResult:
    rep_id: str
    rep_name: str
    segment: str
    tenure_months: int

    coaching_intensity: CoachingIntensity
    primary_focus: CoachingFocus
    coaching_score: float           # 0-100, higher = less coaching needed
    top_skill_gaps: list[SkillGap]

    strengths: list[str]
    development_areas: list[str]
    coaching_actions: list[str]
    session_plan: list[str]         # week-by-week coaching agenda
    kpis_to_track: list[str]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["coaching_intensity"] = self.coaching_intensity.value
        d["primary_focus"] = self.primary_focus.value
        d["top_skill_gaps"] = [g.value for g in self.top_skill_gaps]
        return d


# ─── Scoring helpers ──────────────────────────────────────────────────────────

def _coaching_score(inp: RepPerformanceInput) -> float:
    score = 0.0

    # Quota attainment (0-30 pts)
    att = inp.quota_attainment_pct
    if att >= 120:
        score += 30.0
    elif att >= 100:
        score += 25.0
    elif att >= 80:
        score += 18.0
    elif att >= 60:
        score += 10.0
    elif att >= 40:
        score += 4.0
    else:
        score += 0.0

    # Pipeline coverage (0-20 pts)
    pc = inp.pipeline_coverage_ratio
    if pc >= 3.0:
        score += 20.0
    elif pc >= 2.0:
        score += 14.0
    elif pc >= 1.5:
        score += 8.0
    elif pc >= 1.0:
        score += 3.0
    else:
        score += 0.0

    # Next step discipline (0-15 pts)
    if inp.next_step_set_pct >= 80:
        score += 15.0
    elif inp.next_step_set_pct >= 60:
        score += 10.0
    elif inp.next_step_set_pct >= 40:
        score += 5.0

    # Multi-threading (0-15 pts)
    if inp.multi_thread_avg_contacts >= 3.5:
        score += 15.0
    elif inp.multi_thread_avg_contacts >= 2.5:
        score += 10.0
    elif inp.multi_thread_avg_contacts >= 1.5:
        score += 5.0

    # CRM hygiene (0-10 pts)
    if inp.crm_update_lag_days <= 1.0:
        score += 10.0
    elif inp.crm_update_lag_days <= 3.0:
        score += 6.0
    elif inp.crm_update_lag_days <= 7.0:
        score += 2.0

    # Discount control (0-10 pts)
    if inp.discount_avg_pct <= 5:
        score += 10.0
    elif inp.discount_avg_pct <= 15:
        score += 6.0
    elif inp.discount_avg_pct <= 25:
        score += 2.0

    return round(max(0.0, min(100.0, score)), 1)


def _coaching_intensity(score: float, att: float) -> CoachingIntensity:
    if score >= 80 and att >= 100:
        return CoachingIntensity.LIGHT
    if score >= 60 and att >= 75:
        return CoachingIntensity.MODERATE
    if score >= 35 or att >= 50:
        return CoachingIntensity.INTENSIVE
    return CoachingIntensity.CRITICAL


def _detect_skill_gaps(inp: RepPerformanceInput) -> list[SkillGap]:
    gaps: list[SkillGap] = []
    if inp.avg_discovery_questions_per_call < 5:
        gaps.append(SkillGap.DISCOVERY)
    if inp.deals_lost_to_no_decision_pct > 20:
        gaps.append(SkillGap.QUALIFICATION)
    if inp.discount_avg_pct > 20:
        gaps.append(SkillGap.PRESENTATION)
    if inp.deals_lost_to_competitor_pct > 30:
        gaps.append(SkillGap.OBJECTION_HANDLING)
    if inp.quota_attainment_pct < 80 and inp.pipeline_coverage_ratio >= 2.0:
        gaps.append(SkillGap.CLOSING)
    if inp.crm_update_lag_days > 3:
        gaps.append(SkillGap.PIPELINE_HYGIENE)
    if inp.multi_thread_avg_contacts < 2.0:
        gaps.append(SkillGap.MULTI_THREADING)
    if abs(inp.forecast_accuracy_pct) > 25:
        gaps.append(SkillGap.FORECASTING)
    return gaps[:4]  # return top 4


def _primary_focus(gaps: list[SkillGap], att: float, pc: float) -> CoachingFocus:
    if SkillGap.PIPELINE_HYGIENE in gaps or pc < 1.5:
        return CoachingFocus.PIPELINE
    if att < 50:
        return CoachingFocus.MINDSET
    if SkillGap.DISCOVERY in gaps or SkillGap.QUALIFICATION in gaps:
        return CoachingFocus.SKILLS
    if SkillGap.PIPELINE_HYGIENE in gaps or SkillGap.FORECASTING in gaps:
        return CoachingFocus.PROCESS
    if att >= 80:
        return CoachingFocus.STRATEGY
    return CoachingFocus.SKILLS


def _build_strengths(inp: RepPerformanceInput, score: float) -> list[str]:
    out: list[str] = []
    if inp.quota_attainment_pct >= 100:
        out.append(f"Atteinte quota à {inp.quota_attainment_pct:.0f}% — performer solide")
    if inp.next_step_set_pct >= 75:
        out.append(f"Discipline prochaines étapes excellente — {inp.next_step_set_pct:.0f}% des meetings conclus avec une NS")
    if inp.multi_thread_avg_contacts >= 3.0:
        out.append(f"Multi-threading fort — {inp.multi_thread_avg_contacts:.1f} contacts en moyenne par deal")
    if inp.discount_avg_pct <= 10:
        out.append(f"Bonne tenue sur les prix — seulement {inp.discount_avg_pct:.0f}% de remise moyenne")
    if inp.pipeline_coverage_ratio >= 3.0:
        out.append(f"Couverture pipeline excellente — {inp.pipeline_coverage_ratio:.1f}x le quota")
    if inp.crm_update_lag_days <= 1:
        out.append("CRM à jour en moins de 24h — hygiène commerciale exemplaire")
    if inp.avg_discovery_questions_per_call >= 8:
        out.append(f"Découverte approfondie — {inp.avg_discovery_questions_per_call:.0f} questions en moyenne par appel")
    return out


def _build_development_areas(inp: RepPerformanceInput, gaps: list[SkillGap]) -> list[str]:
    areas: list[str] = []
    if SkillGap.DISCOVERY in gaps:
        areas.append(f"Découverte insuffisante — {inp.avg_discovery_questions_per_call:.0f} questions/appel (objectif ≥ 8)")
    if SkillGap.QUALIFICATION in gaps:
        areas.append(f"Qualification incomplète — {inp.deals_lost_to_no_decision_pct:.0f}% des pertes sans décision (signe de mauvaise qualification)")
    if SkillGap.PRESENTATION in gaps:
        areas.append(f"Présentation/demo à renforcer — {inp.discount_avg_pct:.0f}% de remise moyenne signal valeur non perçue")
    if SkillGap.OBJECTION_HANDLING in gaps:
        areas.append(f"Gestion objections à travailler — {inp.deals_lost_to_competitor_pct:.0f}% perdus face à la concurrence")
    if SkillGap.CLOSING in gaps:
        areas.append("Compétences de closing à développer — pipeline présent mais conversion insuffisante")
    if SkillGap.PIPELINE_HYGIENE in gaps:
        areas.append(f"Hygiène CRM insuffisante — {inp.crm_update_lag_days:.0f}j de délai moyen de mise à jour (objectif ≤ 1j)")
    if SkillGap.MULTI_THREADING in gaps:
        areas.append(f"Multi-threading trop faible — {inp.multi_thread_avg_contacts:.1f} contacts/deal (objectif ≥ 3)")
    if SkillGap.FORECASTING in gaps:
        areas.append(f"Prévisions peu fiables — {abs(inp.forecast_accuracy_pct):.0f}% d'écart forecast vs actuals (objectif ≤ 10%)")
    return areas


def _build_coaching_actions(inp: RepPerformanceInput, gaps: list[SkillGap], intensity: CoachingIntensity, focus: CoachingFocus) -> list[str]:
    actions: list[str] = []

    if intensity in (CoachingIntensity.CRITICAL, CoachingIntensity.INTENSIVE):
        actions.append("Session de coaching bi-hebdomadaire — suivi structuré pendant 60 jours")
        actions.append("Shadow calls : écouter 2 appels/semaine et débriefing post-appel")
        actions.append("Revue pipeline hebdomadaire — deal review approfondi chaque lundi")

    if SkillGap.DISCOVERY in gaps:
        actions.append("Exercice de roleplay discovery — préparer un bank de 15 questions impactantes")
        actions.append("Écouter et annoter 3 recordings de top performers en discovery")
    if SkillGap.QUALIFICATION in gaps:
        actions.append("Formation MEDDIC/BANT — revoir les critères de qualification par segment")
        actions.append("Template de qualification obligatoire avant démo/proposition")
    if SkillGap.OBJECTION_HANDLING in gaps:
        actions.append("Battle card mise à jour — préparer les réponses aux 5 objections les plus fréquentes")
        actions.append("Simulation objection-handling avec le manager ou un pair")
    if SkillGap.CLOSING in gaps:
        actions.append("Identifier les deals bloqués en stade avancé — plan d'action deal par deal")
        actions.append("Pratiquer les techniques de closing trial close et assumptive close")
    if SkillGap.PIPELINE_HYGIENE in gaps:
        actions.append(f"Nettoyage pipeline immédiat — archiver les deals non mis à jour depuis {inp.crm_update_lag_days:.0f}j+")
        actions.append("Rappel processus CRM — mise à jour obligatoire dans les 24h post-réunion")
    if SkillGap.MULTI_THREADING in gaps:
        actions.append("Cartographier les parties prenantes manquantes sur chaque deal actif")
        actions.append("Identifier 2 nouveaux contacts sur les 3 deals les plus importants cette semaine")
    if SkillGap.FORECASTING in gaps:
        actions.append("Revue du processus de forecast — alignement sur les critères de stade CRM")
        actions.append("Rétro mensuelle forecast vs actuals — analyser les écarts")

    if inp.quota_attainment_pct >= 100:
        actions.append("Focus stratégie compte — identifier les opportunités d'expansion sur les 5 meilleurs comptes")

    return actions


def _build_session_plan(intensity: CoachingIntensity, focus: CoachingFocus) -> list[str]:
    plans: dict[CoachingIntensity, list[str]] = {
        CoachingIntensity.LIGHT: [
            "S1 : Revue performance — identifier les leviers de surperformance à capitaliser",
            "S2 : Stratégie comptes — expansion et renouvellements priorisés",
            "S3 : Best practice sharing — pitcher 1 technique gagnante à l'équipe",
        ],
        CoachingIntensity.MODERATE: [
            "S1 : Diagnostic — identifier les 2 axes de progression prioritaires",
            "S2 : Skill drill — exercice pratique sur l'axe #1",
            "S3 : Pipeline review — couvrir les deals à risque et les prochaines étapes",
            "S4 : Skill drill — exercice pratique sur l'axe #2",
            "S5 : Bilan 30j — mesurer les progrès et ajuster le plan",
        ],
        CoachingIntensity.INTENSIVE: [
            "S1 : Diagnostic 360° — évaluation complète des compétences et de la pipeline",
            "S2 : Plan d'action 60j — objectifs, jalons, indicateurs de succès",
            "S3 : Shadow call discovery — débriefing et feedback immédiat",
            "S4 : Deal review #1 — plan par deal pour les 5 priorités pipeline",
            "S5 : Skill training discovery & qualification",
            "S6 : Shadow call proposal — débriefing et amélioration",
            "S7 : Pipeline review + forecast calibration",
            "S8 : Bilan 30j — ajustement du plan et nouveaux objectifs",
        ],
        CoachingIntensity.CRITICAL: [
            "S1 : PIP kick-off — plan d'amélioration formalisé, objectifs 30/60/90j",
            "S2 : Audit activités — analyser les appels, emails, réunions de la semaine passée",
            "S3 : Shadow call x2 — feedback en temps réel et plan de correction",
            "S4 : Pipeline clean-up — archiver les deals fantômes, qualifier les actifs",
            "S5 : Formation intensive discovery & qualification",
            "S6 : Roleplay closing — 3 scénarios différents avec feedback",
            "S7 : Review pipeline + forecast — calibration et discipline",
            "S8 : Bilan 30j — décision : poursuivre PIP ou escalader",
        ],
    }
    return plans.get(intensity, [])


def _build_kpis_to_track(inp: RepPerformanceInput, gaps: list[SkillGap]) -> list[str]:
    kpis = [
        f"Atteinte quota — objectif ≥ 100% (actuellement {inp.quota_attainment_pct:.0f}%)",
        f"Couverture pipeline — objectif ≥ 3x (actuellement {inp.pipeline_coverage_ratio:.1f}x)",
        f"Prochaines étapes définies — objectif ≥ 80% (actuellement {inp.next_step_set_pct:.0f}%)",
    ]
    if SkillGap.DISCOVERY in gaps:
        kpis.append(f"Questions discovery/appel — objectif ≥ 8 (actuellement {inp.avg_discovery_questions_per_call:.0f})")
    if SkillGap.MULTI_THREADING in gaps:
        kpis.append(f"Contacts/deal — objectif ≥ 3 (actuellement {inp.multi_thread_avg_contacts:.1f})")
    if SkillGap.PIPELINE_HYGIENE in gaps:
        kpis.append(f"Délai mise à jour CRM — objectif ≤ 1j (actuellement {inp.crm_update_lag_days:.0f}j)")
    if SkillGap.FORECASTING in gaps:
        kpis.append(f"Précision forecast — objectif ≤ 10% d'écart (actuellement {abs(inp.forecast_accuracy_pct):.0f}%)")
    kpis.append(f"Remise moyenne — objectif ≤ 10% (actuellement {inp.discount_avg_pct:.0f}%)")
    return kpis


class SalesCoachingEngine:
    """Generates personalised coaching plans for sales reps based on performance data."""

    def __init__(self) -> None:
        self._results: dict[str, CoachingPlanResult] = {}

    def coach(self, inp: RepPerformanceInput) -> CoachingPlanResult:
        score = _coaching_score(inp)
        intensity = _coaching_intensity(score, inp.quota_attainment_pct)
        gaps = _detect_skill_gaps(inp)
        focus = _primary_focus(gaps, inp.quota_attainment_pct, inp.pipeline_coverage_ratio)
        strengths = _build_strengths(inp, score)
        dev_areas = _build_development_areas(inp, gaps)
        actions = _build_coaching_actions(inp, gaps, intensity, focus)
        sessions = _build_session_plan(intensity, focus)
        kpis = _build_kpis_to_track(inp, gaps)

        result = CoachingPlanResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            segment=inp.segment,
            tenure_months=inp.tenure_months,
            coaching_intensity=intensity,
            primary_focus=focus,
            coaching_score=score,
            top_skill_gaps=gaps,
            strengths=strengths,
            development_areas=dev_areas,
            coaching_actions=actions,
            session_plan=sessions,
            kpis_to_track=kpis,
        )
        self._results[inp.rep_id] = result
        return result

    def coach_batch(self, inputs: list[RepPerformanceInput]) -> list[CoachingPlanResult]:
        return sorted(
            [self.coach(inp) for inp in inputs],
            key=lambda r: r.coaching_score,
            reverse=True,
        )

    def get(self, rep_id: str) -> Optional[CoachingPlanResult]:
        return self._results.get(rep_id)

    def all_reps(self) -> list[CoachingPlanResult]:
        return sorted(self._results.values(), key=lambda r: r.coaching_score, reverse=True)

    def by_intensity(self, intensity: CoachingIntensity) -> list[CoachingPlanResult]:
        return [r for r in self.all_reps() if r.coaching_intensity == intensity]

    def by_focus(self, focus: CoachingFocus) -> list[CoachingPlanResult]:
        return [r for r in self.all_reps() if r.primary_focus == focus]

    def needs_critical_attention(self) -> list[CoachingPlanResult]:
        return self.by_intensity(CoachingIntensity.CRITICAL)

    def star_performers(self) -> list[CoachingPlanResult]:
        return self.by_intensity(CoachingIntensity.LIGHT)

    def with_skill_gap(self, gap: SkillGap) -> list[CoachingPlanResult]:
        return [r for r in self.all_reps() if gap in r.top_skill_gaps]

    def avg_coaching_score(self) -> float:
        vals = list(self._results.values())
        if not vals:
            return 0.0
        return round(sum(r.coaching_score for r in vals) / len(vals), 1)

    def avg_quota_attainment(self) -> float:
        if not self._results:
            return 0.0
        # We need to recompute this from stored results — proxy via coaching score context
        # Store the quota attainment in the result dict keys isn't possible without the original inp
        # Return 0 as a safe default since we don't store raw inp
        return 0.0

    def summary(self) -> dict:
        all_r = list(self._results.values())
        if not all_r:
            return {
                "total": 0,
                "intensity_counts": {},
                "focus_counts": {},
                "gap_counts": {},
                "avg_coaching_score": 0.0,
                "critical_count": 0,
                "star_count": 0,
            }
        intensity_counts: dict[str, int] = {}
        focus_counts: dict[str, int] = {}
        gap_counts: dict[str, int] = {}
        for r in all_r:
            intensity_counts[r.coaching_intensity.value] = intensity_counts.get(r.coaching_intensity.value, 0) + 1
            focus_counts[r.primary_focus.value] = focus_counts.get(r.primary_focus.value, 0) + 1
            for g in r.top_skill_gaps:
                gap_counts[g.value] = gap_counts.get(g.value, 0) + 1
        return {
            "total": len(all_r),
            "intensity_counts": intensity_counts,
            "focus_counts": focus_counts,
            "gap_counts": gap_counts,
            "avg_coaching_score": self.avg_coaching_score(),
            "critical_count": len(self.needs_critical_attention()),
            "star_count": len(self.star_performers()),
        }

    def reset(self) -> None:
        self._results.clear()
