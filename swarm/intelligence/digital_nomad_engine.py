from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class DigitalNomadInput:
    entity_id: str
    destination_type: str
    region: str
    housing_price_spike: float
    local_displacement_rate: float
    rental_market_distortion: float
    tax_contribution_gap: float
    visa_fee_revenue: float
    local_wage_disparity: float
    cultural_commodification: float
    service_sector_overload: float
    co_working_space_monopoly: float
    brain_gain_local_benefit: float
    digital_infrastructure_strain: float
    social_cohesion_impact: float
    regulatory_clarity: float
    income_inequality_amplification: float
    seasonal_volatility: float
    environmental_footprint: float
    integration_quality: float


@dataclass
class DigitalNomadResult:
    entity_id: str
    destination_type: str
    region: str
    gentrification_score: float
    tax_evasion_score: float
    inequality_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    nomad_pattern: str
    severity: str
    recommended_action: str
    signal: str
    housing_price_spike: float
    local_displacement_rate: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "destination_type": self.destination_type,
            "region": self.region,
            "gentrification_score": self.gentrification_score,
            "tax_evasion_score": self.tax_evasion_score,
            "inequality_score": self.inequality_score,
            "governance_score": self.governance_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "nomad_pattern": self.nomad_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "housing_price_spike": self.housing_price_spike,
            "local_displacement_rate": self.local_displacement_rate,
        }


def _gentrification_score(e: DigitalNomadInput) -> float:
    raw = (
        e.housing_price_spike * 0.4
        + e.local_displacement_rate * 0.35
        + e.rental_market_distortion * 0.25
    ) * 100
    return round(raw * 100) / 100


def _tax_evasion_score(e: DigitalNomadInput) -> float:
    raw = (
        e.tax_contribution_gap * 0.4
        + e.visa_fee_revenue * 0.35
        + e.local_wage_disparity * 0.25
    ) * 100
    return round(raw * 100) / 100


def _inequality_score(e: DigitalNomadInput) -> float:
    raw = (
        e.cultural_commodification * 0.4
        + e.service_sector_overload * 0.35
        + e.co_working_space_monopoly * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: DigitalNomadInput) -> float:
    raw = (
        e.brain_gain_local_benefit * 0.4
        + e.digital_infrastructure_strain * 0.35
        + e.social_cohesion_impact * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    gentrification: float,
    tax_evasion: float,
    inequality: float,
    governance: float,
) -> float:
    return round(
        (gentrification * 0.30 + tax_evasion * 0.25 + inequality * 0.25 + governance * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _nomad_pattern(e: DigitalNomadInput) -> str:
    if e.housing_price_spike > 0.85 and e.local_displacement_rate > 0.80:
        return "housing_gentrification_explosion"
    if e.tax_contribution_gap > 0.85 and e.visa_fee_revenue > 0.80:
        return "tax_base_erosion_crisis"
    if e.cultural_commodification > 0.85 and e.service_sector_overload > 0.80:
        return "cultural_displacement_trap"
    if e.local_wage_disparity > 0.80 and e.income_inequality_amplification > 0.75:
        return "two_tier_economy_formation"
    if e.regulatory_clarity > 0.80 and e.seasonal_volatility > 0.75:
        return "regulatory_arbitrage_race"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_gentrification_nomade_systémique"
    if composite >= 40:
        return "crise_impact_local_majeure"
    if composite >= 20:
        return "inégalité_économique_structurelle"
    return "impact_nomade_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_protection_résidents_locaux"
    if risk == "high":
        return "régulation_accélérée_marché_immobilier_nomade"
    if risk == "moderate":
        return "renforcement_politiques_intégration_économique"
    return "veille_impact_nomade_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise gentrification nomade systémique — impact local en péril"
    if risk == "high":
        return "🟠 Crise impact local majeure détectée"
    if risk == "moderate":
        return "🟡 Inégalité économique structurelle active"
    return "🟢 Impact nomade sous surveillance"


def analyze_digital_nomad(e: DigitalNomadInput) -> DigitalNomadResult:
    gentrification = _gentrification_score(e)
    tax_evasion = _tax_evasion_score(e)
    inequality = _inequality_score(e)
    governance = _governance_score(e)
    composite = _composite_score(gentrification, tax_evasion, inequality, governance)
    risk = _risk_level(composite)
    pattern = _nomad_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return DigitalNomadResult(
        entity_id=e.entity_id,
        destination_type=e.destination_type,
        region=e.region,
        gentrification_score=gentrification,
        tax_evasion_score=tax_evasion,
        inequality_score=inequality,
        governance_score=governance,
        composite_score=composite,
        risk_level=risk,
        nomad_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        housing_price_spike=e.housing_price_spike,
        local_displacement_rate=e.local_displacement_rate,
    )


class DigitalNomadEngine:
    def analyze(self, entities: List[DigitalNomadInput]) -> Dict[str, Any]:
        results = [analyze_digital_nomad(e) for e in entities]

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
            pattern_distribution[r.nomad_pattern] = pattern_distribution.get(r.nomad_pattern, 0) + 1
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
        results: List[DigitalNomadResult] = None,
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
            "module_id": 430,
            "module_name": "Économie Nomades Numériques & Impact Local Intelligence Engine",
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
            "avg_estimated_nomad_impact_index": round(avg_composite / 100 * 10, 2),
        }
