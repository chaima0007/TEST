from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AlgorithmicJusticeInput:
    entity_id: str
    justice_domain: str
    region: str
    recidivism_AI_racial_bias_index: float
    pretrial_detention_algorithmic_amplification: float
    sentencing_AI_disparity_rate: float
    parole_AI_discrimination_index: float
    predictive_policing_racial_profiling: float
    facial_recognition_justice_error_rate: float
    algorithmic_opacity_in_courts: float
    AI_due_process_violation_rate: float
    criminal_justice_AI_accountability_gap: float
    poverty_AI_bias_amplification: float
    immigration_AI_detention_bias: float
    data_quality_justice_impact: float
    AI_legal_representation_inequality: float
    wrongful_conviction_AI_contribution: float
    justice_outcome_wealth_AI_correlation: float
    AI_rehabilitation_assessment_bias: float
    systemic_racism_AI_reproduction: float


@dataclass
class AlgorithmicJusticeResult:
    entity_id: str
    justice_domain: str
    region: str
    bias_score: float
    opacity_score: float
    discrimination_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    justice_pattern: str
    severity: str
    recommended_action: str
    signal: str
    recidivism_AI_racial_bias_index: float
    systemic_racism_AI_reproduction: float

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "justice_domain": self.justice_domain,
            "region": self.region,
            "bias_score": self.bias_score,
            "opacity_score": self.opacity_score,
            "discrimination_score": self.discrimination_score,
            "systemic_score": self.systemic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "justice_pattern": self.justice_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "recidivism_AI_racial_bias_index": self.recidivism_AI_racial_bias_index,
            "systemic_racism_AI_reproduction": self.systemic_racism_AI_reproduction,
        }


class AlgorithmicJusticeEngine:
    def __init__(self) -> None:
        self._results: list[AlgorithmicJusticeResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: AlgorithmicJusticeInput) -> AlgorithmicJusticeResult:
        bias           = self._bias_score(inp)
        opacity        = self._opacity_score(inp)
        discrimination = self._discrimination_score(inp)
        systemic       = self._systemic_score(inp)
        composite      = self._composite(bias, opacity, discrimination, systemic)
        risk_level     = self._risk_level(composite)
        pattern        = self._justice_pattern(inp)
        severity       = self._severity(risk_level)
        action         = self._recommended_action(risk_level)
        signal         = self._signal(risk_level)

        result = AlgorithmicJusticeResult(
            entity_id=inp.entity_id,
            justice_domain=inp.justice_domain,
            region=inp.region,
            bias_score=bias,
            opacity_score=opacity,
            discrimination_score=discrimination,
            systemic_score=systemic,
            composite_score=composite,
            risk_level=risk_level,
            justice_pattern=pattern,
            severity=severity,
            recommended_action=action,
            signal=signal,
            recidivism_AI_racial_bias_index=inp.recidivism_AI_racial_bias_index,
            systemic_racism_AI_reproduction=inp.systemic_racism_AI_reproduction,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[AlgorithmicJusticeInput]) -> list[AlgorithmicJusticeResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _bias_score(self, inp: AlgorithmicJusticeInput) -> float:
        score = (
            inp.recidivism_AI_racial_bias_index * 0.4
            + inp.sentencing_AI_disparity_rate * 0.35
            + inp.predictive_policing_racial_profiling * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _opacity_score(self, inp: AlgorithmicJusticeInput) -> float:
        score = (
            inp.algorithmic_opacity_in_courts * 0.4
            + inp.AI_due_process_violation_rate * 0.35
            + inp.criminal_justice_AI_accountability_gap * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _discrimination_score(self, inp: AlgorithmicJusticeInput) -> float:
        score = (
            inp.poverty_AI_bias_amplification * 0.4
            + inp.AI_legal_representation_inequality * 0.35
            + inp.justice_outcome_wealth_AI_correlation * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _systemic_score(self, inp: AlgorithmicJusticeInput) -> float:
        score = (
            inp.systemic_racism_AI_reproduction * 0.4
            + inp.wrongful_conviction_AI_contribution * 0.35
            + inp.facial_recognition_justice_error_rate * 0.25
        ) * 100
        return round(max(0.0, min(100.0, score)), 2)

    def _composite(
        self,
        bias: float,
        opacity: float,
        discrimination: float,
        systemic: float,
    ) -> float:
        composite = (
            bias * 0.30
            + opacity * 0.25
            + discrimination * 0.25
            + systemic * 0.20
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

    def _justice_pattern(self, inp: AlgorithmicJusticeInput) -> str:
        if inp.recidivism_AI_racial_bias_index >= 0.70 and inp.systemic_racism_AI_reproduction >= 0.65:
            return "racial_algorithm_bias"
        if inp.algorithmic_opacity_in_courts >= 0.70 and inp.AI_due_process_violation_rate >= 0.65:
            return "justice_opacity_crisis"
        if inp.poverty_AI_bias_amplification >= 0.70 and inp.AI_legal_representation_inequality >= 0.65:
            return "poverty_discrimination_cascade"
        if inp.wrongful_conviction_AI_contribution >= 0.70 and inp.facial_recognition_justice_error_rate >= 0.65:
            return "wrongful_AI_conviction"
        if inp.predictive_policing_racial_profiling >= 0.70 and inp.pretrial_detention_algorithmic_amplification >= 0.65:
            return "predictive_persecution"
        return "none"

    def _severity(self, risk_level: str) -> str:
        return {
            "critical": "injustice_algorithmique_systémique",
            "high":     "biais_judiciaire_IA_majeur",
            "moderate": "discrimination_algorithmique_active",
            "low":      "biais_algorithmique_contenu",
        }[risk_level]

    def _recommended_action(self, risk_level: str) -> str:
        return {
            "critical": "réforme_urgente_justice_algorithmique",
            "high":     "audit_systémique_IA_judiciaire",
            "moderate": "renforcement_équité_algorithmique",
            "low":      "veille_biais_judiciaire_IA",
        }[risk_level]

    def _signal(self, risk_level: str) -> str:
        return {
            "critical": "🔴 Injustice algorithmique systémique — biais judiciaire IA critique",
            "high":     "🟠 Biais judiciaire IA majeur détecté",
            "moderate": "🟡 Discrimination algorithmique active",
            "low":      "🟢 Biais algorithmique judiciaire contenu",
        }[risk_level]

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "module_id": 346,
                "module_name": "Algorithmic Justice & Criminal AI Bias Intelligence Engine",
                "total_entities": 0,
                "critical_count": 0,
                "high_count": 0,
                "moderate_count": 0,
                "low_count": 0,
                "avg_composite": 0.0,
                "pattern_distribution": {},
                "risk_distribution": {},
                "severity_distribution": {},
                "action_distribution": {},
                "avg_estimated_justice_bias_index": 0.0,
            }

        pattern_distribution: dict[str, int] = {}
        risk_distribution: dict[str, int] = {}
        severity_distribution: dict[str, int] = {}
        action_distribution: dict[str, int] = {}
        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in self._results:
            pattern_distribution[r.justice_pattern] = pattern_distribution.get(r.justice_pattern, 0) + 1
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            severity_distribution[r.severity] = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action] = action_distribution.get(r.recommended_action, 0) + 1
            total_composite += r.composite_score
            if r.risk_level == "critical":
                critical_count += 1
            elif r.risk_level == "high":
                high_count += 1
            elif r.risk_level == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        avg_composite = round(total_composite / n, 2)

        return {
            "module_id": 346,
            "module_name": "Algorithmic Justice & Criminal AI Bias Intelligence Engine",
            "total_entities": n,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_justice_bias_index": round(avg_composite / 100 * 10, 2),
        }
