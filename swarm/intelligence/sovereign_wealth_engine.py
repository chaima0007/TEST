from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SovereignWealthInput:
    entity_id: str
    fund_type: str
    region: str
    aum_concentration: float
    governance_transparency: float
    political_independence: float
    investment_opacity: float
    critical_infrastructure_acquisition: float
    media_influence_buying: float
    real_estate_strategic_purchase: float
    tech_sector_control: float
    sovereign_debt_leverage: float
    democracy_index_target: float
    esg_compliance: float
    wealth_distribution_domestic: float
    fossil_fuel_dependence: float
    diversification_quality: float
    accountability_mechanism: float
    international_treaty_compliance: float
    geopolitical_alignment: float


@dataclass
class SovereignWealthResult:
    entity_id: str
    fund_type: str
    region: str
    concentration_score: float
    opacity_score: float
    geopolitical_score: float
    accountability_score: float
    composite_score: float
    risk_level: str
    sovereign_pattern: str
    severity: str
    recommended_action: str
    signal: str
    aum_concentration: float
    geopolitical_alignment: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "fund_type": self.fund_type,
            "region": self.region,
            "concentration_score": self.concentration_score,
            "opacity_score": self.opacity_score,
            "geopolitical_score": self.geopolitical_score,
            "accountability_score": self.accountability_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "sovereign_pattern": self.sovereign_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "aum_concentration": self.aum_concentration,
            "geopolitical_alignment": self.geopolitical_alignment,
        }


def _concentration_score(e: SovereignWealthInput) -> float:
    raw = (
        e.aum_concentration * 0.4
        + e.critical_infrastructure_acquisition * 0.35
        + e.tech_sector_control * 0.25
    ) * 100
    return round(raw * 100) / 100


def _opacity_score(e: SovereignWealthInput) -> float:
    raw = (
        e.investment_opacity * 0.4
        + (1.0 - e.governance_transparency) * 0.35
        + e.media_influence_buying * 0.25
    ) * 100
    return round(raw * 100) / 100


def _geopolitical_score(e: SovereignWealthInput) -> float:
    raw = (
        e.geopolitical_alignment * 0.4
        + e.sovereign_debt_leverage * 0.35
        + e.real_estate_strategic_purchase * 0.25
    ) * 100
    return round(raw * 100) / 100


def _accountability_score(e: SovereignWealthInput) -> float:
    raw = (
        (1.0 - e.accountability_mechanism) * 0.4
        + (1.0 - e.international_treaty_compliance) * 0.35
        + e.democracy_index_target * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    concentration: float,
    opacity: float,
    geopolitical: float,
    accountability: float,
) -> float:
    return round(
        (
            concentration * 0.30
            + opacity * 0.25
            + geopolitical * 0.25
            + accountability * 0.20
        )
        * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _sovereign_pattern(e: SovereignWealthInput) -> str:
    if e.critical_infrastructure_acquisition > 0.85 and e.tech_sector_control > 0.80:
        return "critical_asset_foreign_capture"
    if e.media_influence_buying > 0.85 and e.democracy_index_target > 0.80:
        return "democratic_influence_buying"
    if e.investment_opacity > 0.85 and (1.0 - e.governance_transparency) > 0.80:
        return "opacity_money_laundering_nexus"
    if e.fossil_fuel_dependence > 0.80 and e.wealth_distribution_domestic < 0.25:
        return "resource_curse_recycling"
    if e.sovereign_debt_leverage > 0.80 and e.geopolitical_alignment > 0.75:
        return "geoeconomic_coercion_tool"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "menace_souveraineté_systémique_critique"
    if composite >= 40:
        return "risque_géopolitique_majeur_détecté"
    if composite >= 20:
        return "influence_opaque_structurelle"
    return "fonds_souverain_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_contrôle_actifs_stratégiques"
    if risk == "high":
        return "audit_géopolitique_accéléré_fonds_souverain"
    if risk == "moderate":
        return "renforcement_transparence_gouvernance_fonds"
    return "veille_fonds_souverain_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Menace souveraineté systémique — capture d'actifs critiques en cours"
    if risk == "high":
        return "🟠 Risque géopolitique majeur détecté — influence opaque élevée"
    if risk == "moderate":
        return "🟡 Influence opaque structurelle — surveillance renforcée requise"
    return "🟢 Fonds souverain sous surveillance standard"


def analyze_sovereign_wealth(e: SovereignWealthInput) -> SovereignWealthResult:
    concentration = _concentration_score(e)
    opacity = _opacity_score(e)
    geopolitical = _geopolitical_score(e)
    accountability = _accountability_score(e)
    composite = _composite_score(concentration, opacity, geopolitical, accountability)
    risk = _risk_level(composite)
    pattern = _sovereign_pattern(e)
    sev = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return SovereignWealthResult(
        entity_id=e.entity_id,
        fund_type=e.fund_type,
        region=e.region,
        concentration_score=concentration,
        opacity_score=opacity,
        geopolitical_score=geopolitical,
        accountability_score=accountability,
        composite_score=composite,
        risk_level=risk,
        sovereign_pattern=pattern,
        severity=sev,
        recommended_action=action,
        signal=sig,
        aum_concentration=e.aum_concentration,
        geopolitical_alignment=e.geopolitical_alignment,
    )


class SovereignWealthEngine:
    def analyze(self, entities: List[SovereignWealthInput]) -> Dict[str, Any]:
        results = [analyze_sovereign_wealth(e) for e in entities]

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
            pattern_distribution[r.sovereign_pattern] = pattern_distribution.get(r.sovereign_pattern, 0) + 1
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
        results: List[SovereignWealthResult] = None,
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
            "module_id": 432,
            "module_name": "Fonds Souverains & Pouvoir Géopolitique Intelligence Engine",
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
            "avg_estimated_sovereign_wealth_index": round(avg_composite / 100 * 10, 2),
        }
