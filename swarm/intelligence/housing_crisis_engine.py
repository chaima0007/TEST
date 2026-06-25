from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class HousingCrisisInput:
    entity_id: str
    market_type: str
    region: str
    price_to_income_ratio: float
    rent_burden_rate: float
    homelessness_prevalence: float
    speculative_investment_share: float
    vacancy_rate: float
    social_housing_stock: float
    construction_deficit: float
    eviction_rate: float
    landlord_monopolization: float
    first_buyer_exclusion: float
    geographic_segregation: float
    displacement_intensity: float
    zoning_restrictiveness: float
    tenant_protection_gap: float
    mortgage_debt_burden: float
    public_housing_waitlist: float
    financialization_intensity: float


@dataclass
class HousingCrisisResult:
    entity_id: str
    market_type: str
    region: str
    affordability_score: float
    speculation_score: float
    supply_score: float
    homelessness_score: float
    composite_score: float
    risk_level: str
    housing_pattern: str
    severity: str
    recommended_action: str
    signal: str
    price_to_income_ratio: float
    rent_burden_rate: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "market_type": self.market_type,
            "region": self.region,
            "affordability_score": self.affordability_score,
            "speculation_score": self.speculation_score,
            "supply_score": self.supply_score,
            "homelessness_score": self.homelessness_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "housing_pattern": self.housing_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "price_to_income_ratio": self.price_to_income_ratio,
            "rent_burden_rate": self.rent_burden_rate,
        }


def _affordability_score(e: HousingCrisisInput) -> float:
    raw = (
        e.price_to_income_ratio * 0.4
        + e.rent_burden_rate * 0.35
        + e.first_buyer_exclusion * 0.25
    ) * 100
    return round(raw * 100) / 100


def _speculation_score(e: HousingCrisisInput) -> float:
    raw = (
        e.speculative_investment_share * 0.4
        + e.financialization_intensity * 0.35
        + e.landlord_monopolization * 0.25
    ) * 100
    return round(raw * 100) / 100


def _supply_score(e: HousingCrisisInput) -> float:
    raw = (
        e.construction_deficit * 0.4
        + e.zoning_restrictiveness * 0.35
        + e.vacancy_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _homelessness_score(e: HousingCrisisInput) -> float:
    raw = (
        e.homelessness_prevalence * 0.4
        + e.eviction_rate * 0.35
        + e.public_housing_waitlist * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    affordability: float,
    speculation: float,
    supply: float,
    homelessness: float,
) -> float:
    return round(
        (affordability * 0.30 + speculation * 0.25 + supply * 0.25 + homelessness * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _housing_pattern(e: HousingCrisisInput) -> str:
    if e.homelessness_prevalence > 0.85 and e.eviction_rate > 0.80:
        return "homelessness_crisis_explosion"
    if e.financialization_intensity > 0.85 and e.speculative_investment_share > 0.80:
        return "financialization_speculation_trap"
    if e.tenant_protection_gap > 0.85 and e.rent_burden_rate > 0.80:
        return "rental_market_collapse"
    if e.displacement_intensity > 0.80 and e.geographic_segregation > 0.75:
        return "displacement_gentrification"
    if e.social_housing_stock > 0.80 and e.public_housing_waitlist > 0.75:
        return "social_housing_defunding"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_logement_systémique_critique"
    if composite >= 40:
        return "crise_accessibilité_immobilière_majeure"
    if composite >= 20:
        return "tension_marché_immobilier_structurelle"
    return "marché_logement_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_crise_logement_systémique"
    if risk == "high":
        return "régulation_marché_immobilier_accélérée"
    if risk == "moderate":
        return "renforcement_politiques_accessibilité_logement"
    return "veille_marché_logement_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise logement systémique — accessibilité immobilière en péril"
    if risk == "high":
        return "🟠 Crise accessibilité immobilière majeure détectée"
    if risk == "moderate":
        return "🟡 Tension marché immobilier structurelle active"
    return "🟢 Marché logement sous surveillance"


def analyze_housing_crisis(e: HousingCrisisInput) -> HousingCrisisResult:
    affordability = _affordability_score(e)
    speculation = _speculation_score(e)
    supply = _supply_score(e)
    homelessness = _homelessness_score(e)
    composite = _composite_score(affordability, speculation, supply, homelessness)
    risk = _risk_level(composite)
    pattern = _housing_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return HousingCrisisResult(
        entity_id=e.entity_id,
        market_type=e.market_type,
        region=e.region,
        affordability_score=affordability,
        speculation_score=speculation,
        supply_score=supply,
        homelessness_score=homelessness,
        composite_score=composite,
        risk_level=risk,
        housing_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        price_to_income_ratio=e.price_to_income_ratio,
        rent_burden_rate=e.rent_burden_rate,
    )


class HousingCrisisEngine:
    def analyze(self, entities: List[HousingCrisisInput]) -> Dict[str, Any]:
        results = [analyze_housing_crisis(e) for e in entities]

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
            pattern_distribution[r.housing_pattern] = pattern_distribution.get(r.housing_pattern, 0) + 1
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
        results: List[HousingCrisisResult] = None,
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
            "module_id": 422,
            "module_name": "Crise Logement & Accessibilité Immobilière Intelligence Engine",
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
            "avg_estimated_housing_affordability_index": round(avg_composite / 100 * 10, 2),
        }
