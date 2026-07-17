from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CryptoEconomicInput:
    entity_id: str
    defi_segment: str
    region: str
    protocol_governance_quality: float
    tvl_concentration: float
    smart_contract_audit_coverage: float
    oracle_manipulation_risk: float
    liquidity_depth: float
    cross_protocol_contagion: float
    regulatory_clarity: float
    rug_pull_risk: float
    mev_extraction_rate: float
    bridge_security_score: float
    stablecoin_depeg_risk: float
    governance_token_concentration: float
    flash_loan_attack_surface: float
    protocol_upgrade_risk: float
    community_coordination_quality: float
    revenue_sustainability: float
    defi_insurance_coverage: float


@dataclass
class CryptoEconomicResult:
    entity_id: str
    region: str
    defi_segment: str
    defi_risk: str
    defi_pattern: str
    defi_severity: str
    recommended_action: str
    governance_score: float
    security_score: float
    liquidity_score: float
    regulatory_score: float
    defi_composite: float
    is_in_defi_crisis: bool
    requires_defi_intervention: bool
    defi_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "defi_segment": self.defi_segment,
            "defi_risk": self.defi_risk,
            "defi_pattern": self.defi_pattern,
            "defi_severity": self.defi_severity,
            "recommended_action": self.recommended_action,
            "governance_score": self.governance_score,
            "security_score": self.security_score,
            "liquidity_score": self.liquidity_score,
            "regulatory_score": self.regulatory_score,
            "defi_composite": self.defi_composite,
            "is_in_defi_crisis": self.is_in_defi_crisis,
            "requires_defi_intervention": self.requires_defi_intervention,
            "defi_signal": self.defi_signal,
        }


def _governance_score(inp: CryptoEconomicInput) -> float:
    return (
        (1 - inp.protocol_governance_quality) * 0.4
        + inp.governance_token_concentration * 0.35
        + (1 - inp.community_coordination_quality) * 0.25
    ) * 100


def _security_score(inp: CryptoEconomicInput) -> float:
    return (
        (1 - inp.smart_contract_audit_coverage) * 0.35
        + inp.oracle_manipulation_risk * 0.35
        + inp.flash_loan_attack_surface * 0.30
    ) * 100


def _liquidity_score(inp: CryptoEconomicInput) -> float:
    return (
        (1 - inp.liquidity_depth) * 0.4
        + inp.tvl_concentration * 0.35
        + inp.stablecoin_depeg_risk * 0.25
    ) * 100


def _regulatory_score(inp: CryptoEconomicInput) -> float:
    return (
        (1 - inp.regulatory_clarity) * 0.4
        + inp.rug_pull_risk * 0.35
        + (1 - inp.defi_insurance_coverage) * 0.25
    ) * 100


def _composite(gov: float, sec: float, liq: float, reg: float) -> float:
    return gov * 0.30 + sec * 0.25 + liq * 0.25 + reg * 0.20


def _defi_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _defi_pattern(inp: CryptoEconomicInput) -> str:
    if (1 - inp.protocol_governance_quality) >= 0.65 and inp.governance_token_concentration >= 0.60:
        return "governance_attack"
    if (1 - inp.smart_contract_audit_coverage) >= 0.65 and inp.flash_loan_attack_surface >= 0.55:
        return "smart_contract_exploit"
    if (1 - inp.liquidity_depth) >= 0.65 and inp.cross_protocol_contagion >= 0.60:
        return "liquidity_cascade"
    if inp.stablecoin_depeg_risk >= 0.70 and inp.tvl_concentration >= 0.60:
        return "stablecoin_depeg_crisis"
    if (1 - inp.regulatory_clarity) >= 0.70 and inp.rug_pull_risk >= 0.60:
        return "regulatory_crackdown"
    return "none"


def _defi_severity(composite: float) -> str:
    if composite >= 75:
        return "defi_collapse"
    if composite >= 50:
        return "high_systemic_risk"
    if composite >= 25:
        return "protocol_stress"
    return "defi_stable"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "defi_emergency_shutdown"
    if risk == "high" and pattern == "liquidity_cascade":
        return "liquidity_backstop"
    if risk == "high":
        return "protocol_hardening"
    if risk == "moderate":
        return "defi_monitoring"
    return "no_action"


def _defi_signal(inp: CryptoEconomicInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — qualité gouvernance {int(inp.protocol_governance_quality * 100)}%"
            f" — concentration TVL {int(inp.tvl_concentration * 100)}%"
            f" — composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — couverture audit {int(inp.smart_contract_audit_coverage * 100)}%"
            f" — profondeur liquidité {int(inp.liquidity_depth * 100)}%"
            f" — composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — risque dépeg stablecoin {int(inp.stablecoin_depeg_risk * 100)}%"
            f" — composite {comp_int}"
        )
    return "Protocole DeFi stable — gouvernance solide, sécurité vérifiée, liquidité profonde"


def analyze(inp: CryptoEconomicInput) -> CryptoEconomicResult:
    gov = _governance_score(inp)
    sec = _security_score(inp)
    liq = _liquidity_score(inp)
    reg = _regulatory_score(inp)
    comp = _composite(gov, sec, liq, reg)

    risk = _defi_risk(comp)
    pattern = _defi_pattern(inp)
    severity = _defi_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _defi_signal(inp, risk, comp)

    return CryptoEconomicResult(
        entity_id=inp.entity_id,
        region=inp.region,
        defi_segment=inp.defi_segment,
        defi_risk=risk,
        defi_pattern=pattern,
        defi_severity=severity,
        recommended_action=action,
        governance_score=round(gov, 2),
        security_score=round(sec, 2),
        liquidity_score=round(liq, 2),
        regulatory_score=round(reg, 2),
        defi_composite=round(comp, 2),
        is_in_defi_crisis=comp >= 60,
        requires_defi_intervention=comp >= 40,
        defi_signal=signal,
    )


class CryptoEconomicGovernanceEngine:
    def run(self, inputs: List[CryptoEconomicInput]) -> Dict[str, Any]:
        results = [analyze(inp) for inp in inputs]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_governance = 0.0
        total_security = 0.0
        total_liquidity = 0.0
        total_regulatory = 0.0
        defi_crisis_count = 0
        defi_intervention_count = 0

        for r in results:
            risk_counts[r.defi_risk] = risk_counts.get(r.defi_risk, 0) + 1
            pattern_counts[r.defi_pattern] = pattern_counts.get(r.defi_pattern, 0) + 1
            severity_counts[r.defi_severity] = severity_counts.get(r.defi_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1

            total_composite += r.defi_composite
            total_governance += r.governance_score
            total_security += r.security_score
            total_liquidity += r.liquidity_score
            total_regulatory += r.regulatory_score

            if r.is_in_defi_crisis:
                defi_crisis_count += 1
            if r.requires_defi_intervention:
                defi_intervention_count += 1

        n = len(results)
        avg_composite = total_composite / n if n else 0.0

        summary = {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_defi_composite": round(avg_composite, 1),
            "defi_crisis_count": defi_crisis_count,
            "defi_intervention_count": defi_intervention_count,
            "avg_governance_score": round(total_governance / n, 1) if n else 0.0,
            "avg_security_score": round(total_security / n, 1) if n else 0.0,
            "avg_liquidity_score": round(total_liquidity / n, 1) if n else 0.0,
            "avg_regulatory_score": round(total_regulatory / n, 1) if n else 0.0,
            "avg_estimated_defi_risk_index": round(avg_composite / 100 * 10, 2),
        }

        return {
            "entities": [r.to_dict() for r in results],
            "summary": summary,
        }
