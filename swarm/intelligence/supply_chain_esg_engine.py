from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SupplyChainESGInput:
    entity_id: str
    industry_type: str
    region: str
    supply_visibility: float
    forced_labor_risk: float
    child_labor_exposure: float
    carbon_footprint: float
    deforestation_link: float
    water_pollution: float
    conflict_mineral_use: float
    audit_independence: float
    reporting_quality: float
    certification_credibility: float
    subcontractor_risk: float
    living_wage_compliance: float
    gender_equality: float
    biodiversity_impact: float
    data_integrity: float
    regulatory_compliance: float
    third_party_verification: float


@dataclass
class SupplyChainESGResult:
    entity_id: str
    industry_type: str
    region: str
    visibility_score: float
    labor_score: float
    environmental_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    esg_pattern: str
    severity: str
    recommended_action: str
    signal: str
    supply_visibility: float
    forced_labor_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "industry_type": self.industry_type,
            "region": self.region,
            "visibility_score": self.visibility_score,
            "labor_score": self.labor_score,
            "environmental_score": self.environmental_score,
            "governance_score": self.governance_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "esg_pattern": self.esg_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "supply_visibility": self.supply_visibility,
            "forced_labor_risk": self.forced_labor_risk,
        }


def _visibility_score(e: SupplyChainESGInput) -> float:
    raw = (
        e.supply_visibility * 0.40
        + e.subcontractor_risk * 0.35
        + e.data_integrity * 0.25
    ) * 100
    return round(raw * 100) / 100


def _labor_score(e: SupplyChainESGInput) -> float:
    raw = (
        e.forced_labor_risk * 0.40
        + e.child_labor_exposure * 0.35
        + e.living_wage_compliance * 0.25
    ) * 100
    return round(raw * 100) / 100


def _environmental_score(e: SupplyChainESGInput) -> float:
    raw = (
        e.carbon_footprint * 0.40
        + e.deforestation_link * 0.35
        + e.water_pollution * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: SupplyChainESGInput) -> float:
    raw = (
        e.audit_independence * 0.40
        + e.reporting_quality * 0.35
        + e.certification_credibility * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    visibility: float,
    labor: float,
    environmental: float,
    governance: float,
) -> float:
    return round(
        (visibility * 0.30 + labor * 0.25 + environmental * 0.25 + governance * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _esg_pattern(e: SupplyChainESGInput) -> str:
    if e.forced_labor_risk > 0.85 and e.child_labor_exposure > 0.80:
        return "forced_labor_opacity"
    if e.carbon_footprint > 0.85 and e.reporting_quality < 0.20:
        return "greenwashing_deception"
    if e.conflict_mineral_use > 0.85 and e.supply_visibility < 0.20:
        return "conflict_mineral_complicity"
    if e.carbon_footprint > 0.80 and e.deforestation_link > 0.75:
        return "carbon_laundering_scheme"
    if e.audit_independence > 0.80 and e.certification_credibility > 0.75:
        return "supplier_audit_capture"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_opacité_chaîne_approvisionnement_critique"
    if composite >= 40:
        return "risque_esg_majeur_détecté"
    if composite >= 20:
        return "non_conformité_esg_structurelle"
    return "transparence_esg_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "audit_urgence_chaîne_approvisionnement_intégrale"
    if risk == "high":
        return "renforcement_contrôle_fournisseurs_tier2_tier3"
    if risk == "moderate":
        return "mise_en_conformité_esg_progressive"
    return "veille_transparence_chaîne_approvisionnement"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise opacité chaîne d'approvisionnement — violation ESG systémique"
    if risk == "high":
        return "🟠 Risque ESG majeur détecté dans la chaîne fournisseurs"
    if risk == "moderate":
        return "🟡 Non-conformité ESG structurelle — surveillance renforcée requise"
    return "🟢 Transparence ESG sous surveillance continue"


def analyze_supply_chain_esg(e: SupplyChainESGInput) -> SupplyChainESGResult:
    visibility = _visibility_score(e)
    labor = _labor_score(e)
    environmental = _environmental_score(e)
    governance = _governance_score(e)
    composite = _composite_score(visibility, labor, environmental, governance)
    risk = _risk_level(composite)
    pattern = _esg_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return SupplyChainESGResult(
        entity_id=e.entity_id,
        industry_type=e.industry_type,
        region=e.region,
        visibility_score=visibility,
        labor_score=labor,
        environmental_score=environmental,
        governance_score=governance,
        composite_score=composite,
        risk_level=risk,
        esg_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        supply_visibility=e.supply_visibility,
        forced_labor_risk=e.forced_labor_risk,
    )


class SupplyChainESGEngine:
    def analyze(self, entities: List[SupplyChainESGInput]) -> Dict[str, Any]:
        results = [analyze_supply_chain_esg(e) for e in entities]

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
            pattern_distribution[r.esg_pattern] = pattern_distribution.get(r.esg_pattern, 0) + 1
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
        results: List[SupplyChainESGResult] = None,
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
            "module_id": 397,
            "module_name": "Transparence Chaîne d'Approvisionnement ESG Intelligence Engine",
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
            "avg_estimated_esg_transparency_index": round(avg_composite / 100 * 10, 2),
        }
