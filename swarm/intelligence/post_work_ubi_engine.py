from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PostWorkUBIInput:
    entity_id: str
    economic_sector: str
    region: str
    automation_displacement_rate: float
    UBI_fiscal_sustainability: float
    retraining_program_failure: float
    social_contract_breakdown: float
    gig_worker_precariousness: float
    cognitive_job_extinction: float
    labor_market_polarization: float
    meaning_crisis_intensity: float
    political_instability_unemployment: float
    welfare_state_collapse: float
    automation_tax_resistance: float
    UBI_inflation_risk: float
    skills_gap_acceleration: float
    inequality_amplification_AI: float
    union_power_collapse: float
    middle_class_extinction: float
    social_cohesion_erosion: float


@dataclass
class PostWorkUBIResult:
    entity_id: str
    economic_sector: str
    region: str
    displacement_score: float
    social_score: float
    economic_score: float
    political_score: float
    composite_score: float
    risk_level: str
    post_work_pattern: str
    severity: str
    recommended_action: str
    signal: str
    automation_displacement_rate: float
    middle_class_extinction: float

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "economic_sector": self.economic_sector,
            "region": self.region,
            "displacement_score": self.displacement_score,
            "social_score": self.social_score,
            "economic_score": self.economic_score,
            "political_score": self.political_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "post_work_pattern": self.post_work_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "automation_displacement_rate": self.automation_displacement_rate,
            "middle_class_extinction": self.middle_class_extinction,
        }


class PostWorkUBIEngine:
    def __init__(self) -> None:
        self._results: list[PostWorkUBIResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: PostWorkUBIInput) -> PostWorkUBIResult:
        displacement = self._displacement_score(inp)
        social       = self._social_score(inp)
        economic     = self._economic_score(inp)
        political    = self._political_score(inp)
        composite    = self._composite(displacement, social, economic, political)
        risk_level   = self._risk_level(composite)
        pattern      = self._post_work_pattern(inp)
        severity     = self._severity(risk_level)
        action       = self._recommended_action(risk_level)
        signal       = self._signal(risk_level)

        result = PostWorkUBIResult(
            entity_id=inp.entity_id,
            economic_sector=inp.economic_sector,
            region=inp.region,
            displacement_score=displacement,
            social_score=social,
            economic_score=economic,
            political_score=political,
            composite_score=composite,
            risk_level=risk_level,
            post_work_pattern=pattern,
            severity=severity,
            recommended_action=action,
            signal=signal,
            automation_displacement_rate=inp.automation_displacement_rate,
            middle_class_extinction=inp.middle_class_extinction,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[PostWorkUBIInput]) -> list[PostWorkUBIResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _displacement_score(self, inp: PostWorkUBIInput) -> float:
        score = (
            inp.automation_displacement_rate * 0.4
            + inp.cognitive_job_extinction * 0.35
            + inp.skills_gap_acceleration * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _social_score(self, inp: PostWorkUBIInput) -> float:
        score = (
            inp.social_contract_breakdown * 0.4
            + inp.social_cohesion_erosion * 0.35
            + inp.meaning_crisis_intensity * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _economic_score(self, inp: PostWorkUBIInput) -> float:
        score = (
            inp.UBI_fiscal_sustainability * 0.4
            + inp.welfare_state_collapse * 0.35
            + inp.UBI_inflation_risk * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _political_score(self, inp: PostWorkUBIInput) -> float:
        score = (
            inp.political_instability_unemployment * 0.4
            + inp.automation_tax_resistance * 0.35
            + inp.inequality_amplification_AI * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _composite(
        self,
        displacement: float,
        social: float,
        economic: float,
        political: float,
    ) -> float:
        composite = (
            displacement * 0.30
            + social * 0.25
            + economic * 0.25
            + political * 0.20
        )
        return round(max(0.0, min(100.0, composite)), 2)

    def _risk_level(self, composite: float) -> str:
        if composite >= 60:
            return "critical"
        if composite >= 40:
            return "high"
        if composite >= 20:
            return "moderate"
        return "low"

    def _post_work_pattern(self, inp: PostWorkUBIInput) -> str:
        if inp.automation_displacement_rate > 0.85 and inp.cognitive_job_extinction > 0.80:
            return "mass_automation_displacement"
        if inp.welfare_state_collapse > 0.85 and inp.UBI_fiscal_sustainability > 0.80:
            return "welfare_state_implosion"
        if inp.social_contract_breakdown > 0.85 and inp.social_cohesion_erosion > 0.80:
            return "social_contract_collapse"
        if inp.middle_class_extinction > 0.80 and inp.labor_market_polarization > 0.75:
            return "middle_class_extinction_event"
        if inp.political_instability_unemployment > 0.80 and inp.automation_tax_resistance > 0.75:
            return "political_automation_revolt"
        return "none"

    def _severity(self, risk_level: str) -> str:
        return {
            "critical": "effondrement_post_travail_systémique",
            "high":     "disruption_emploi_revenu_majeure",
            "moderate": "transition_post_travail_active",
            "low":      "risque_post_travail_contenu",
        }[risk_level]

    def _recommended_action(self, risk_level: str) -> str:
        return {
            "critical": "intervention_urgente_revenu_universel",
            "high":     "audit_systémique_transition_emploi",
            "moderate": "renforcement_filets_protection_sociale",
            "low":      "veille_disruption_marché_travail",
        }[risk_level]

    def _signal(self, risk_level: str) -> str:
        return {
            "critical": "🔴 Effondrement post-travail systémique — disruption emploi IA critique",
            "high":     "🟠 Disruption emploi & revenu universel majeure détectée",
            "moderate": "🟡 Transition post-travail active en cours",
            "low":      "🟢 Risque post-travail contenu",
        }[risk_level]

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "module_id": 374,
                "module_name": "Post-Work Society & Universal Basic Income Intelligence Engine",
                "total": 0,
                "critical": 0,
                "high": 0,
                "moderate": 0,
                "low": 0,
                "avg_composite": 0.0,
                "distributions": {},
                "avg_estimated_post_work_disruption_index": 0.0,
                "pattern_distribution": {},
                "risk_distribution": {},
                "severity_distribution": {},
            }

        pattern_distribution: dict[str, int] = {}
        risk_distribution: dict[str, int] = {}
        severity_distribution: dict[str, int] = {}
        action_distribution: dict[str, int] = {}
        total_composite = 0.0
        critical = 0
        high = 0
        moderate = 0
        low = 0

        for r in self._results:
            pattern_distribution[r.post_work_pattern] = pattern_distribution.get(r.post_work_pattern, 0) + 1
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            severity_distribution[r.severity] = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action] = action_distribution.get(r.recommended_action, 0) + 1
            total_composite += r.composite_score
            if r.risk_level == "critical":
                critical += 1
            elif r.risk_level == "high":
                high += 1
            elif r.risk_level == "moderate":
                moderate += 1
            else:
                low += 1

        avg_composite = round(total_composite / n, 2)

        return {
            "module_id": 374,
            "module_name": "Post-Work Society & Universal Basic Income Intelligence Engine",
            "total": n,
            "critical": critical,
            "high": high,
            "moderate": moderate,
            "low": low,
            "avg_composite": avg_composite,
            "distributions": {
                "pattern": pattern_distribution,
                "risk": risk_distribution,
                "severity": severity_distribution,
                "action": action_distribution,
            },
            "avg_estimated_post_work_disruption_index": round(avg_composite / 100 * 10, 2),
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
        }
