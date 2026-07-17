from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SkillLevel(str, Enum):
    EXPERT      = "expert"
    ADVANCED    = "advanced"
    PROFICIENT  = "proficient"
    DEVELOPING  = "developing"
    BEGINNER    = "beginner"


class SkillGap(str, Enum):
    NONE        = "none"
    MINOR       = "minor"
    MODERATE    = "moderate"
    SIGNIFICANT = "significant"
    CRITICAL    = "critical"


class CoachingPriority(str, Enum):
    IMMEDIATE = "immediate"
    HIGH      = "high"
    MEDIUM    = "medium"
    LOW       = "low"
    MAINTAIN  = "maintain"


class DevelopmentPath(str, Enum):
    ADVANCED_TRAINING = "advanced_training"
    SKILLS_COACHING   = "skills_coaching"
    PEER_MENTORING    = "peer_mentoring"
    SELF_DIRECTED     = "self_directed"
    MAINTAIN          = "maintain"


@dataclass
class SalesSkillsInput:
    rep_id: str
    rep_name: str
    manager_id: str
    # Core sales skills (0-100)
    discovery_score: float
    demo_effectiveness: float
    objection_handling: float
    negotiation_skill: float
    closing_technique: float
    # Operational skills (0-100)
    prospecting_score: float
    pipeline_management: float
    crm_discipline: float
    # Performance indicators
    quota_attainment_pct: float      # 0-1, 1.0 = 100% quota
    win_rate: float                  # 0-1
    avg_deal_size_vs_team: float     # ratio, 1.0 = team average
    avg_sales_cycle_vs_team: float   # ratio, 1.0 = average, <1 = faster
    call_connect_rate: float         # 0-1
    email_reply_rate: float          # 0-1
    meetings_set_per_week: float
    # Context
    months_at_company: int
    months_in_role: int
    training_hours_completed: int
    coaching_sessions_90d: int
    top_performer_last_quarter: bool


@dataclass
class SalesSkillsResult:
    rep_id: str
    rep_name: str
    manager_id: str
    overall_skill_score: float
    technical_score: float
    operational_score: float
    results_score: float
    weakest_area: str
    skill_level: SkillLevel
    skill_gap: SkillGap
    coaching_priority: CoachingPriority
    development_path: DevelopmentPath
    strengths: list[str]
    gaps: list[str]
    recommended_actions: list[str]

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "manager_id": self.manager_id,
            "overall_skill_score": self.overall_skill_score,
            "technical_score": self.technical_score,
            "operational_score": self.operational_score,
            "results_score": self.results_score,
            "weakest_area": self.weakest_area,
            "skill_level": self.skill_level.value,
            "skill_gap": self.skill_gap.value,
            "coaching_priority": self.coaching_priority.value,
            "development_path": self.development_path.value,
            "strengths": self.strengths,
            "gaps": self.gaps,
            "recommended_actions": self.recommended_actions,
        }


class SalesSkillsEngine:
    def __init__(self) -> None:
        self.results: list[SalesSkillsResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _technical_score(self, inp: SalesSkillsInput) -> float:
        raw = (
            inp.discovery_score +
            inp.demo_effectiveness +
            inp.objection_handling +
            inp.negotiation_skill +
            inp.closing_technique
        ) / 5.0
        return round(max(0.0, min(100.0, raw)), 1)

    def _operational_score(self, inp: SalesSkillsInput) -> float:
        raw = (
            inp.prospecting_score +
            inp.pipeline_management +
            inp.crm_discipline
        ) / 3.0
        return round(max(0.0, min(100.0, raw)), 1)

    def _results_score(self, inp: SalesSkillsInput) -> float:
        # Quota attainment (40%)
        quota_component = min(40.0, inp.quota_attainment_pct * 40.0)
        # Win rate (25%)
        win_component = inp.win_rate * 25.0
        # Deal size vs team (15%) — above average is good
        deal_component = min(15.0, inp.avg_deal_size_vs_team * 15.0)
        # Sales cycle vs team (10%) — faster is better
        if inp.avg_sales_cycle_vs_team > 0:
            cycle_component = min(10.0, (1.0 / inp.avg_sales_cycle_vs_team) * 10.0)
        else:
            cycle_component = 10.0
        # Prospecting metrics (10%)
        connect_component = inp.call_connect_rate * 5.0 + inp.email_reply_rate * 5.0
        raw = quota_component + win_component + deal_component + cycle_component + connect_component
        return round(max(0.0, min(100.0, raw)), 1)

    def _overall_skill_score(
        self, technical: float, operational: float, results: float
    ) -> float:
        raw = technical * 0.40 + operational * 0.25 + results * 0.35
        return round(max(0.0, min(100.0, raw)), 1)

    def _weakest_area(self, inp: SalesSkillsInput, technical: float, operational: float, results: float) -> str:
        areas = {
            "Découverte client": inp.discovery_score,
            "Démonstration produit": inp.demo_effectiveness,
            "Gestion des objections": inp.objection_handling,
            "Négociation": inp.negotiation_skill,
            "Technique de closing": inp.closing_technique,
            "Prospection": inp.prospecting_score,
            "Gestion du pipeline": inp.pipeline_management,
            "Discipline CRM": inp.crm_discipline,
        }
        return min(areas, key=lambda k: areas[k])

    def _skill_level(self, overall: float) -> SkillLevel:
        if overall >= 85:
            return SkillLevel.EXPERT
        if overall >= 70:
            return SkillLevel.ADVANCED
        if overall >= 55:
            return SkillLevel.PROFICIENT
        if overall >= 35:
            return SkillLevel.DEVELOPING
        return SkillLevel.BEGINNER

    def _skill_gap(self, overall: float, results: float) -> SkillGap:
        # Gap is based on how far from excellence
        avg = (overall + results) / 2.0
        if avg >= 80:
            return SkillGap.NONE
        if avg >= 65:
            return SkillGap.MINOR
        if avg >= 50:
            return SkillGap.MODERATE
        if avg >= 30:
            return SkillGap.SIGNIFICANT
        return SkillGap.CRITICAL

    def _coaching_priority(
        self,
        inp: SalesSkillsInput,
        overall: float,
        gap: SkillGap,
    ) -> CoachingPriority:
        if gap == SkillGap.CRITICAL:
            return CoachingPriority.IMMEDIATE
        if gap == SkillGap.SIGNIFICANT:
            return CoachingPriority.HIGH
        if inp.top_performer_last_quarter and gap == SkillGap.NONE:
            return CoachingPriority.MAINTAIN
        if gap == SkillGap.MODERATE:
            return CoachingPriority.MEDIUM
        if gap == SkillGap.MINOR:
            return CoachingPriority.LOW
        return CoachingPriority.MAINTAIN

    def _development_path(
        self,
        inp: SalesSkillsInput,
        level: SkillLevel,
        gap: SkillGap,
        priority: CoachingPriority,
    ) -> DevelopmentPath:
        if priority == CoachingPriority.MAINTAIN:
            return DevelopmentPath.MAINTAIN
        if level in (SkillLevel.BEGINNER, SkillLevel.DEVELOPING):
            if inp.coaching_sessions_90d >= 3:
                return DevelopmentPath.SKILLS_COACHING
            return DevelopmentPath.SKILLS_COACHING
        if level == SkillLevel.PROFICIENT:
            if inp.months_at_company >= 12:
                return DevelopmentPath.PEER_MENTORING
            return DevelopmentPath.SKILLS_COACHING
        if level == SkillLevel.ADVANCED:
            if inp.training_hours_completed >= 20:
                return DevelopmentPath.ADVANCED_TRAINING
            return DevelopmentPath.SELF_DIRECTED
        # EXPERT
        return DevelopmentPath.ADVANCED_TRAINING

    def _build_strengths(self, inp: SalesSkillsInput) -> list[str]:
        strengths: list[str] = []
        if inp.discovery_score >= 80:
            strengths.append(f"Découverte client excellente ({round(inp.discovery_score)}/100) — écoute et qualification au top")
        if inp.demo_effectiveness >= 80:
            strengths.append(f"Démos très efficaces ({round(inp.demo_effectiveness)}/100) — présentation convaincante")
        if inp.objection_handling >= 80:
            strengths.append(f"Gestion des objections solide ({round(inp.objection_handling)}/100) — réponses précises et pertinentes")
        if inp.negotiation_skill >= 80:
            strengths.append(f"Négociation avancée ({round(inp.negotiation_skill)}/100) — bon contrôle des concessions")
        if inp.closing_technique >= 80:
            strengths.append(f"Technique de closing maîtrisée ({round(inp.closing_technique)}/100) — sait créer l'urgence")
        if inp.prospecting_score >= 80:
            strengths.append(f"Prospection efficace ({round(inp.prospecting_score)}/100) — pipeline bien rempli")
        if inp.pipeline_management >= 80:
            strengths.append(f"Gestion du pipeline rigoureuse ({round(inp.pipeline_management)}/100) — prévisions fiables")
        if inp.crm_discipline >= 80:
            strengths.append(f"Discipline CRM exemplaire ({round(inp.crm_discipline)}/100) — données à jour")
        if inp.quota_attainment_pct >= 1.0:
            strengths.append(f"Quota dépassé ({round(inp.quota_attainment_pct * 100)}%) — objectifs commerciaux atteints")
        if inp.win_rate >= 0.40:
            strengths.append(f"Taux de victoire élevé ({round(inp.win_rate * 100)}%) — conversion deals supérieure")
        if inp.top_performer_last_quarter:
            strengths.append("Top performer Q précédent — excellence commerciale confirmée")
        return strengths

    def _build_gaps(self, inp: SalesSkillsInput) -> list[str]:
        gaps: list[str] = []
        if inp.discovery_score < 55:
            gaps.append(f"Découverte client insuffisante ({round(inp.discovery_score)}/100) — qualification trop superficielle")
        if inp.demo_effectiveness < 55:
            gaps.append(f"Démos peu convaincantes ({round(inp.demo_effectiveness)}/100) — adapter au persona acheteur")
        if inp.objection_handling < 55:
            gaps.append(f"Objections mal gérées ({round(inp.objection_handling)}/100) — manque de réponses préparées")
        if inp.negotiation_skill < 55:
            gaps.append(f"Négociation à améliorer ({round(inp.negotiation_skill)}/100) — risque de concessions excessives")
        if inp.closing_technique < 55:
            gaps.append(f"Technique de closing faible ({round(inp.closing_technique)}/100) — deals qui s'étirent sans décision")
        if inp.prospecting_score < 55:
            gaps.append(f"Prospection insuffisante ({round(inp.prospecting_score)}/100) — pipeline sous-alimenté")
        if inp.pipeline_management < 55:
            gaps.append(f"Pipeline mal géré ({round(inp.pipeline_management)}/100) — prévisions peu fiables")
        if inp.crm_discipline < 55:
            gaps.append(f"Hygiène CRM à améliorer ({round(inp.crm_discipline)}/100) — données manquantes ou obsolètes")
        if inp.quota_attainment_pct < 0.70:
            gaps.append(f"Quota sous-atteint ({round(inp.quota_attainment_pct * 100)}%) — objectifs commerciaux non réalisés")
        if inp.win_rate < 0.20:
            gaps.append(f"Taux de victoire bas ({round(inp.win_rate * 100)}%) — qualification ou closing à renforcer")
        return gaps

    def _build_actions(
        self,
        inp: SalesSkillsInput,
        path: DevelopmentPath,
        priority: CoachingPriority,
    ) -> list[str]:
        actions: list[str] = []
        if path == DevelopmentPath.MAINTAIN:
            actions.append("Conserver le rythme — partager les meilleures pratiques avec l'équipe")
            actions.append("Envisager un rôle de mentor pour les commerciaux en développement")
        elif path == DevelopmentPath.SKILLS_COACHING:
            actions.append("Planifier un coaching individuel hebdomadaire avec le manager")
            actions.append("Travailler les appels d'entraînement et les jeux de rôle sur les points faibles")
        elif path == DevelopmentPath.PEER_MENTORING:
            actions.append("Associer à un top performer pour du mentoring pair-à-pair")
            actions.append("Participer à des revues de deals en équipe pour observer les bonnes pratiques")
        elif path == DevelopmentPath.SELF_DIRECTED:
            actions.append("S'inscrire aux formations en ligne sur les domaines identifiés")
            actions.append("Utiliser les ressources de la bibliothèque de formation interne")
        else:  # ADVANCED_TRAINING
            actions.append("Inscription à une formation avancée sur les techniques de vente complexe")
            actions.append("Participer à des conférences sectorielles et programmes certifiants")
        if priority in (CoachingPriority.IMMEDIATE, CoachingPriority.HIGH):
            actions.append(f"Plan de développement 30-60-90j à mettre en place avec le manager immédiatement")
        return actions

    # ── public API ────────────────────────────────────────────────────────────

    def analyze(self, inp: SalesSkillsInput) -> SalesSkillsResult:
        tech  = self._technical_score(inp)
        ops   = self._operational_score(inp)
        res   = self._results_score(inp)
        overall = self._overall_skill_score(tech, ops, res)
        weakest = self._weakest_area(inp, tech, ops, res)
        level   = self._skill_level(overall)
        gap     = self._skill_gap(overall, res)
        priority = self._coaching_priority(inp, overall, gap)
        path     = self._development_path(inp, level, gap, priority)
        result = SalesSkillsResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            manager_id=inp.manager_id,
            overall_skill_score=overall,
            technical_score=tech,
            operational_score=ops,
            results_score=res,
            weakest_area=weakest,
            skill_level=level,
            skill_gap=gap,
            coaching_priority=priority,
            development_path=path,
            strengths=self._build_strengths(inp),
            gaps=self._build_gaps(inp),
            recommended_actions=self._build_actions(inp, path, priority),
        )
        self.results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[SalesSkillsInput]
    ) -> list[SalesSkillsResult]:
        for inp in inputs:
            self.analyze(inp)
        self.results.sort(key=lambda r: r.overall_skill_score, reverse=True)
        return self.results

    def reset(self) -> None:
        self.results = []

    # ── helpers ───────────────────────────────────────────────────────────────

    @property
    def top_performers(self) -> list[SalesSkillsResult]:
        return [r for r in self.results if r.skill_level in (SkillLevel.EXPERT, SkillLevel.ADVANCED)]

    @property
    def needs_immediate_coaching(self) -> list[SalesSkillsResult]:
        return [r for r in self.results if r.coaching_priority == CoachingPriority.IMMEDIATE]

    @property
    def at_risk_reps(self) -> list[SalesSkillsResult]:
        return [r for r in self.results if r.skill_gap in (SkillGap.CRITICAL, SkillGap.SIGNIFICANT)]

    @property
    def ready_for_mentoring(self) -> list[SalesSkillsResult]:
        return [r for r in self.results if r.development_path == DevelopmentPath.PEER_MENTORING]

    def summary(self) -> dict:
        n = len(self.results)
        if n == 0:
            return {
                "total": 0,
                "level_counts": {},
                "gap_counts": {},
                "priority_counts": {},
                "path_counts": {},
                "avg_overall_score": 0.0,
                "avg_technical_score": 0.0,
                "avg_operational_score": 0.0,
                "avg_results_score": 0.0,
                "top_performer_count": 0,
                "immediate_coaching_count": 0,
                "at_risk_count": 0,
            }
        level_counts: dict[str, int] = {}
        gap_counts:   dict[str, int] = {}
        prio_counts:  dict[str, int] = {}
        path_counts:  dict[str, int] = {}
        total_o = total_t = total_op = total_r = 0.0
        for res in self.results:
            level_counts[res.skill_level.value]        = level_counts.get(res.skill_level.value, 0) + 1
            gap_counts[res.skill_gap.value]             = gap_counts.get(res.skill_gap.value, 0) + 1
            prio_counts[res.coaching_priority.value]    = prio_counts.get(res.coaching_priority.value, 0) + 1
            path_counts[res.development_path.value]     = path_counts.get(res.development_path.value, 0) + 1
            total_o  += res.overall_skill_score
            total_t  += res.technical_score
            total_op += res.operational_score
            total_r  += res.results_score
        return {
            "total": n,
            "level_counts": level_counts,
            "gap_counts": gap_counts,
            "priority_counts": prio_counts,
            "path_counts": path_counts,
            "avg_overall_score":     round(total_o / n, 1),
            "avg_technical_score":   round(total_t / n, 1),
            "avg_operational_score": round(total_op / n, 1),
            "avg_results_score":     round(total_r / n, 1),
            "top_performer_count":   len(self.top_performers),
            "immediate_coaching_count": len(self.needs_immediate_coaching),
            "at_risk_count":         len(self.at_risk_reps),
        }
