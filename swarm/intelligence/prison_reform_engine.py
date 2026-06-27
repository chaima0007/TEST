from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class PrisonReformInput:
    entity_id: str
    justice_system_type: str
    region: str
    incarceration_rate_excess: float
    pretrial_detention_rate: float
    racial_sentencing_disparity: float
    mandatory_minimum_overuse: float
    private_prison_profit_motive: float
    recidivism_rate_high: float
    rehabilitation_program_gap: float
    solitary_confinement_use: float
    prison_labor_exploitation: float
    mental_health_treatment_gap: float
    overcrowding_rate: float
    bail_system_inequality: float
    public_defender_underresourcing: float
    reentry_program_deficit: float
    voting_rights_disenfranchisement: float
    family_separation_impact: float
    drug_offense_overincarceration: float


@dataclass
class PrisonReformResult:
    entity_id: str
    justice_system_type: str
    region: str
    incarceration_score: float
    racial_score: float
    rehabilitation_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    justice_pattern: str
    severity: str
    recommended_action: str
    signal: str
    incarceration_rate_excess: float
    racial_sentencing_disparity: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "justice_system_type": self.justice_system_type,
            "region": self.region,
            "incarceration_score": self.incarceration_score,
            "racial_score": self.racial_score,
            "rehabilitation_score": self.rehabilitation_score,
            "systemic_score": self.systemic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "justice_pattern": self.justice_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "incarceration_rate_excess": self.incarceration_rate_excess,
            "racial_sentencing_disparity": self.racial_sentencing_disparity,
        }


def _incarceration_score(e: PrisonReformInput) -> float:
    raw = (
        e.incarceration_rate_excess * 0.4
        + e.pretrial_detention_rate * 0.35
        + e.drug_offense_overincarceration * 0.25
    ) * 100
    return round(raw * 100) / 100


def _racial_score(e: PrisonReformInput) -> float:
    raw = (
        e.racial_sentencing_disparity * 0.4
        + e.mandatory_minimum_overuse * 0.35
        + e.bail_system_inequality * 0.25
    ) * 100
    return round(raw * 100) / 100


def _rehabilitation_score(e: PrisonReformInput) -> float:
    raw = (
        e.recidivism_rate_high * 0.4
        + e.rehabilitation_program_gap * 0.35
        + e.reentry_program_deficit * 0.25
    ) * 100
    return round(raw * 100) / 100


def _systemic_score(e: PrisonReformInput) -> float:
    raw = (
        e.private_prison_profit_motive * 0.4
        + e.solitary_confinement_use * 0.35
        + e.prison_labor_exploitation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    incarceration: float,
    racial: float,
    rehabilitation: float,
    systemic: float,
) -> float:
    return round(
        (incarceration * 0.30 + racial * 0.25 + rehabilitation * 0.25 + systemic * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _justice_pattern(e: PrisonReformInput) -> str:
    if e.incarceration_rate_excess > 0.85 and e.drug_offense_overincarceration > 0.80:
        return "mass_incarceration_industrial"
    if e.racial_sentencing_disparity > 0.85 and e.mandatory_minimum_overuse > 0.80:
        return "racial_disparity_sentencing"
    if e.recidivism_rate_high > 0.85 and e.rehabilitation_program_gap > 0.80:
        return "recidivism_rehabilitation_gap"
    if e.private_prison_profit_motive > 0.80 and e.prison_labor_exploitation > 0.75:
        return "prison_privatization_abuse"
    if e.solitary_confinement_use > 0.80 and e.mental_health_treatment_gap > 0.75:
        return "solitary_confinement_torture"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_justice_pénale_systémique"
    if composite >= 40:
        return "crise_droits_fondamentaux_majeure"
    if composite >= 20:
        return "inégalité_carcérale_structurelle"
    return "système_pénal_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_réforme_pénale_critique"
    if risk == "high":
        return "réforme_systémique_accélérée_droits_détenus"
    if risk == "moderate":
        return "renforcement_politiques_justice_réparatrice"
    return "veille_système_pénal_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise justice pénale systémique — droits fondamentaux en péril"
    if risk == "high":
        return "🟠 Crise droits fondamentaux majeure détectée"
    if risk == "moderate":
        return "🟡 Inégalité carcérale structurelle active"
    return "🟢 Système pénal sous surveillance"


def analyze_prison_reform(e: PrisonReformInput) -> PrisonReformResult:
    incarceration = _incarceration_score(e)
    racial = _racial_score(e)
    rehabilitation = _rehabilitation_score(e)
    systemic = _systemic_score(e)
    composite = _composite_score(incarceration, racial, rehabilitation, systemic)
    risk = _risk_level(composite)
    pattern = _justice_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return PrisonReformResult(
        entity_id=e.entity_id,
        justice_system_type=e.justice_system_type,
        region=e.region,
        incarceration_score=incarceration,
        racial_score=racial,
        rehabilitation_score=rehabilitation,
        systemic_score=systemic,
        composite_score=composite,
        risk_level=risk,
        justice_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        incarceration_rate_excess=e.incarceration_rate_excess,
        racial_sentencing_disparity=e.racial_sentencing_disparity,
    )


class PrisonReformEngine:
    def analyze(self, entities: List[PrisonReformInput]) -> Dict[str, Any]:
        results = [analyze_prison_reform(e) for e in entities]

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            pattern_distribution[r.justice_pattern] = pattern_distribution.get(r.justice_pattern, 0) + 1
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

        n = len(results) or 1
        avg_composite = round(total_composite / n * 10) / 10

        return self.summary(
            results=results,
            risk_distribution=risk_distribution,
            pattern_distribution=pattern_distribution,
            severity_distribution=severity_distribution,
            action_distribution=action_distribution,
            avg_composite=avg_composite,
            critical_count=critical_count,
            high_count=high_count,
            moderate_count=moderate_count,
            low_count=low_count,
        )

    def summary(
        self,
        results: List[PrisonReformResult] = None,
        risk_distribution: Dict[str, int] = None,
        pattern_distribution: Dict[str, int] = None,
        severity_distribution: Dict[str, int] = None,
        action_distribution: Dict[str, int] = None,
        avg_composite: float = 0.0,
        critical_count: int = 0,
        high_count: int = 0,
        moderate_count: int = 0,
        low_count: int = 0,
    ) -> Dict[str, Any]:
        results = results or []
        return {
            "module_id": 443,
            "module_name": "Réforme Pénale & Justice Systémique Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution or {},
            "risk_distribution": risk_distribution or {},
            "severity_distribution": severity_distribution or {},
            "action_distribution": action_distribution or {},
            "avg_estimated_justice_reform_index": round(avg_composite / 100 * 10, 2),
        }
