from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CarbonBorderInput:
    entity_id: str
    sector_type: str
    region: str
    carbon_leakage_risk: float
    import_emission_intensity: float
    domestic_carbon_price: float
    border_price_equivalence: float
    compliance_verification_gap: float
    developing_country_impact: float
    wto_compatibility_risk: float
    industry_lobbying_capture: float
    measurement_accuracy: float
    data_availability: float
    third_country_retaliation: float
    green_industrial_policy_alignment: float
    renewable_transition_support: float
    supply_chain_decarbonization: float
    tariff_circumvention_risk: float
    political_stability: float
    administrative_capacity: float


@dataclass
class CarbonBorderResult:
    entity_id: str
    sector_type: str
    region: str
    leakage_score: float
    competitiveness_score: float
    compliance_score: float
    geopolitical_score: float
    composite_score: float
    risk_level: str
    cbam_pattern: str
    severity: str
    recommended_action: str
    signal: str
    carbon_leakage_risk: float
    compliance_verification_gap: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "sector_type": self.sector_type,
            "region": self.region,
            "leakage_score": self.leakage_score,
            "competitiveness_score": self.competitiveness_score,
            "compliance_score": self.compliance_score,
            "geopolitical_score": self.geopolitical_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "cbam_pattern": self.cbam_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "carbon_leakage_risk": self.carbon_leakage_risk,
            "compliance_verification_gap": self.compliance_verification_gap,
        }


def _leakage_score(e: CarbonBorderInput) -> float:
    raw = (
        e.carbon_leakage_risk * 0.40
        + e.import_emission_intensity * 0.35
        + e.tariff_circumvention_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _competitiveness_score(e: CarbonBorderInput) -> float:
    raw = (
        e.industry_lobbying_capture * 0.40
        + e.green_industrial_policy_alignment * 0.35
        + e.supply_chain_decarbonization * 0.25
    ) * 100
    return round(raw * 100) / 100


def _compliance_score(e: CarbonBorderInput) -> float:
    raw = (
        e.compliance_verification_gap * 0.40
        + e.measurement_accuracy * 0.35
        + e.data_availability * 0.25
    ) * 100
    return round(raw * 100) / 100


def _geopolitical_score(e: CarbonBorderInput) -> float:
    raw = (
        e.third_country_retaliation * 0.40
        + e.wto_compatibility_risk * 0.35
        + e.developing_country_impact * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    leakage: float,
    competitiveness: float,
    compliance: float,
    geopolitical: float,
) -> float:
    return round(
        (leakage * 0.30 + competitiveness * 0.25 + compliance * 0.25 + geopolitical * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _cbam_pattern(e: CarbonBorderInput) -> str:
    if e.carbon_leakage_risk > 0.85 and e.import_emission_intensity > 0.80:
        return "carbon_leakage_acceleration"
    if e.third_country_retaliation > 0.85 and e.wto_compatibility_risk > 0.80:
        return "trade_war_escalation"
    if e.developing_country_impact > 0.85 and e.renewable_transition_support < 0.20:
        return "developing_country_exclusion"
    if e.compliance_verification_gap > 0.80 and e.measurement_accuracy > 0.75:
        return "measurement_fraud_crisis"
    if e.administrative_capacity > 0.80 and e.political_stability < 0.20:
        return "implementation_collapse"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_mécanisme_carbone_frontière_systémique"
    if composite >= 40:
        return "risque_fuite_carbone_majeur_détecté"
    if composite >= 20:
        return "non_conformité_cbam_structurelle"
    return "ajustement_carbone_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_mécanisme_carbone_frontière_critique"
    if risk == "high":
        return "renforcement_vérification_conformité_cbam_accélérée"
    if risk == "moderate":
        return "mise_en_conformité_cbam_progressive"
    return "veille_ajustement_carbone_frontière_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise mécanisme ajustement carbone frontière — fuite carbone systémique"
    if risk == "high":
        return "🟠 Risque fuite carbone majeur détecté — conformité CBAM compromise"
    if risk == "moderate":
        return "🟡 Non-conformité CBAM structurelle — surveillance renforcée requise"
    return "🟢 Ajustement carbone frontière sous surveillance continue"


def analyze_carbon_border(e: CarbonBorderInput) -> CarbonBorderResult:
    leakage = _leakage_score(e)
    competitiveness = _competitiveness_score(e)
    compliance = _compliance_score(e)
    geopolitical = _geopolitical_score(e)
    composite = _composite_score(leakage, competitiveness, compliance, geopolitical)
    risk = _risk_level(composite)
    pattern = _cbam_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return CarbonBorderResult(
        entity_id=e.entity_id,
        sector_type=e.sector_type,
        region=e.region,
        leakage_score=leakage,
        competitiveness_score=competitiveness,
        compliance_score=compliance,
        geopolitical_score=geopolitical,
        composite_score=composite,
        risk_level=risk,
        cbam_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        carbon_leakage_risk=e.carbon_leakage_risk,
        compliance_verification_gap=e.compliance_verification_gap,
    )


class CarbonBorderEngine:
    def analyze(self, entities: List[CarbonBorderInput]) -> Dict[str, Any]:
        results = [analyze_carbon_border(e) for e in entities]

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
            pattern_distribution[r.cbam_pattern] = pattern_distribution.get(r.cbam_pattern, 0) + 1
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
        results: List[CarbonBorderResult] = None,
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
            "module_id": 413,
            "module_name": "Mécanisme Ajustement Carbone Frontière Intelligence Engine",
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
            "avg_estimated_cbam_effectiveness_index": round(avg_composite / 100 * 10, 2),
        }
