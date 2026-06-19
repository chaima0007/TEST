from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CBDCSovereigntyInput:
    entity_id: str
    currency_type: str
    region: str
    # 17 float fields (0-1)
    surveillance_intensity: float
    transaction_monitoring: float
    programmability_risk: float
    privacy_preservation: float
    financial_inclusion: float
    sovereignty_risk: float
    interoperability: float
    cross_border_control: float
    offline_capability: float
    user_autonomy: float
    censorship_resistance: float
    foreign_dependence: float
    monetary_policy_independence: float
    digital_literacy_gap: float
    infrastructure_resilience: float
    regulatory_capture: float
    geopolitical_leverage: float


@dataclass
class CBDCSovereigntyResult:
    entity_id: str
    currency_type: str
    region: str
    surveillance_score: float
    exclusion_score: float
    sovereignty_score: float
    programmability_score: float
    composite_score: float
    risk_level: str
    cbdc_pattern: str
    severity: str
    recommended_action: str
    signal: str
    surveillance_intensity: float
    foreign_dependence: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "currency_type": self.currency_type,
            "region": self.region,
            "surveillance_score": self.surveillance_score,
            "exclusion_score": self.exclusion_score,
            "sovereignty_score": self.sovereignty_score,
            "programmability_score": self.programmability_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "cbdc_pattern": self.cbdc_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "surveillance_intensity": self.surveillance_intensity,
            "foreign_dependence": self.foreign_dependence,
        }


def _surveillance_score(e: CBDCSovereigntyInput) -> float:
    raw = (
        e.surveillance_intensity * 0.40
        + e.transaction_monitoring * 0.35
        + (1.0 - e.censorship_resistance) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _exclusion_score(e: CBDCSovereigntyInput) -> float:
    raw = (
        (1.0 - e.financial_inclusion) * 0.40
        + e.digital_literacy_gap * 0.35
        + (1.0 - e.offline_capability) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sovereignty_score(e: CBDCSovereigntyInput) -> float:
    raw = (
        e.sovereignty_risk * 0.40
        + e.foreign_dependence * 0.35
        + (1.0 - e.monetary_policy_independence) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _programmability_score(e: CBDCSovereigntyInput) -> float:
    raw = (
        e.programmability_risk * 0.40
        + e.regulatory_capture * 0.35
        + (1.0 - e.user_autonomy) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    surveillance: float,
    exclusion: float,
    sovereignty: float,
    programmability: float,
) -> float:
    return round(
        (surveillance * 0.30 + exclusion * 0.25 + sovereignty * 0.25 + programmability * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _cbdc_pattern(e: CBDCSovereigntyInput) -> str:
    if e.surveillance_intensity > 0.85 and e.transaction_monitoring > 0.80:
        return "financial_surveillance_state"
    if e.programmability_risk > 0.85 and e.regulatory_capture > 0.80:
        return "programmable_money_control"
    if e.sovereignty_risk > 0.85 and e.foreign_dependence > 0.80:
        return "monetary_sovereignty_capture"
    if (1.0 - e.financial_inclusion) > 0.80 and e.digital_literacy_gap > 0.75:
        return "financial_exclusion_crisis"
    if e.geopolitical_leverage > 0.80 and (1.0 - e.monetary_policy_independence) > 0.75:
        return "digital_dollarization_trap"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_souveraineté_monétaire_numérique_systémique"
    if composite >= 40:
        return "crise_contrôle_monnaie_programmable_majeure"
    if composite >= 20:
        return "tension_exclusion_financière_numérique_active"
    return "surveillance_monnaie_numérique_continue"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_souveraineté_monétaire_numérique"
    if risk == "high":
        return "renforcement_cadre_protection_monnaie_numérique"
    if risk == "moderate":
        return "surveillance_renforcée_cbdc_inclusion_financière"
    return "veille_souveraineté_monnaie_numérique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise souveraineté monétaire numérique systémique — contrôle financier total imminent"
    if risk == "high":
        return "🟠 Crise contrôle monnaie programmable majeure détectée"
    if risk == "moderate":
        return "🟡 Tension exclusion financière numérique active"
    return "🟢 Souveraineté monnaie numérique sous surveillance"


def analyze_cbdc_sovereignty(e: CBDCSovereigntyInput) -> CBDCSovereigntyResult:
    surveillance = _surveillance_score(e)
    exclusion = _exclusion_score(e)
    sovereignty = _sovereignty_score(e)
    programmability = _programmability_score(e)
    composite = _composite_score(surveillance, exclusion, sovereignty, programmability)
    risk = _risk_level(composite)
    pattern = _cbdc_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return CBDCSovereigntyResult(
        entity_id=e.entity_id,
        currency_type=e.currency_type,
        region=e.region,
        surveillance_score=surveillance,
        exclusion_score=exclusion,
        sovereignty_score=sovereignty,
        programmability_score=programmability,
        composite_score=composite,
        risk_level=risk,
        cbdc_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        surveillance_intensity=e.surveillance_intensity,
        foreign_dependence=e.foreign_dependence,
    )


MOCK_ENTITIES: List[CBDCSovereigntyInput] = [
    # CBDC-001 — Digital Yuan, APAC → critical, financial_surveillance_state
    CBDCSovereigntyInput(
        entity_id="CBDC-001", currency_type="digital_yuan", region="APAC",
        surveillance_intensity=0.92, transaction_monitoring=0.88,
        programmability_risk=0.78, privacy_preservation=0.08,
        financial_inclusion=0.72, sovereignty_risk=0.60,
        interoperability=0.65, cross_border_control=0.80,
        offline_capability=0.55, user_autonomy=0.15,
        censorship_resistance=0.10, foreign_dependence=0.20,
        monetary_policy_independence=0.85, digital_literacy_gap=0.35,
        infrastructure_resilience=0.80, regulatory_capture=0.75,
        geopolitical_leverage=0.70,
    ),
    # CBDC-002 — Digital Dollar, AMER → critical, programmable_money_control
    CBDCSovereigntyInput(
        entity_id="CBDC-002", currency_type="digital_dollar", region="AMER",
        surveillance_intensity=0.80, transaction_monitoring=0.82,
        programmability_risk=0.92, privacy_preservation=0.15,
        financial_inclusion=0.60, sovereignty_risk=0.58,
        interoperability=0.65, cross_border_control=0.78,
        offline_capability=0.55, user_autonomy=0.08,
        censorship_resistance=0.15, foreign_dependence=0.18,
        monetary_policy_independence=0.85, digital_literacy_gap=0.30,
        infrastructure_resilience=0.80, regulatory_capture=0.88,
        geopolitical_leverage=0.82,
    ),
    # CBDC-003 — e-Naira Nigeria, AFRICA → low, financial_exclusion_crisis (low adoption, low risk scores)
    CBDCSovereigntyInput(
        entity_id="CBDC-003", currency_type="e_naira", region="AFRICA",
        surveillance_intensity=0.10, transaction_monitoring=0.08,
        programmability_risk=0.12, privacy_preservation=0.80,
        financial_inclusion=0.10, sovereignty_risk=0.12,
        interoperability=0.30, cross_border_control=0.10,
        offline_capability=0.15, user_autonomy=0.80,
        censorship_resistance=0.82, foreign_dependence=0.12,
        monetary_policy_independence=0.80, digital_literacy_gap=0.85,
        infrastructure_resilience=0.20, regulatory_capture=0.10,
        geopolitical_leverage=0.08,
    ),
    # CBDC-004 — Digital Ruble, EMEA → critical, monetary_sovereignty_capture
    CBDCSovereigntyInput(
        entity_id="CBDC-004", currency_type="digital_ruble", region="EMEA",
        surveillance_intensity=0.80, transaction_monitoring=0.75,
        programmability_risk=0.72, privacy_preservation=0.12,
        financial_inclusion=0.55, sovereignty_risk=0.88,
        interoperability=0.40, cross_border_control=0.85,
        offline_capability=0.50, user_autonomy=0.18,
        censorship_resistance=0.15, foreign_dependence=0.85,
        monetary_policy_independence=0.20, digital_literacy_gap=0.40,
        infrastructure_resilience=0.60, regulatory_capture=0.78,
        geopolitical_leverage=0.75,
    ),
    # CBDC-005 — Digital Euro, EMEA → high, digital_dollarization_trap
    CBDCSovereigntyInput(
        entity_id="CBDC-005", currency_type="digital_euro", region="EMEA",
        surveillance_intensity=0.55, transaction_monitoring=0.50,
        programmability_risk=0.58, privacy_preservation=0.52,
        financial_inclusion=0.68, sovereignty_risk=0.60,
        interoperability=0.72, cross_border_control=0.60,
        offline_capability=0.65, user_autonomy=0.50,
        censorship_resistance=0.55, foreign_dependence=0.45,
        monetary_policy_independence=0.22, digital_literacy_gap=0.35,
        infrastructure_resilience=0.70, regulatory_capture=0.58,
        geopolitical_leverage=0.82,
    ),
    # CBDC-006 — Petro Venezuela, LATAM → high, none
    CBDCSovereigntyInput(
        entity_id="CBDC-006", currency_type="petro_venezuela", region="LATAM",
        surveillance_intensity=0.58, transaction_monitoring=0.52,
        programmability_risk=0.55, privacy_preservation=0.38,
        financial_inclusion=0.48, sovereignty_risk=0.58,
        interoperability=0.42, cross_border_control=0.60,
        offline_capability=0.45, user_autonomy=0.40,
        censorship_resistance=0.42, foreign_dependence=0.52,
        monetary_policy_independence=0.48, digital_literacy_gap=0.45,
        infrastructure_resilience=0.48, regulatory_capture=0.50,
        geopolitical_leverage=0.48,
    ),
    # CBDC-007 — Sand Dollar Bahamas, CARIB → low, none
    CBDCSovereigntyInput(
        entity_id="CBDC-007", currency_type="sand_dollar", region="CARIB",
        surveillance_intensity=0.12, transaction_monitoring=0.10,
        programmability_risk=0.15, privacy_preservation=0.85,
        financial_inclusion=0.88, sovereignty_risk=0.12,
        interoperability=0.82, cross_border_control=0.10,
        offline_capability=0.85, user_autonomy=0.88,
        censorship_resistance=0.90, foreign_dependence=0.10,
        monetary_policy_independence=0.88, digital_literacy_gap=0.12,
        infrastructure_resilience=0.80, regulatory_capture=0.10,
        geopolitical_leverage=0.08,
    ),
    # CBDC-008 — JAM-DEX Jamaica, CARIB → low, none
    CBDCSovereigntyInput(
        entity_id="CBDC-008", currency_type="jam_dex", region="CARIB",
        surveillance_intensity=0.14, transaction_monitoring=0.12,
        programmability_risk=0.15, privacy_preservation=0.85,
        financial_inclusion=0.85, sovereignty_risk=0.15,
        interoperability=0.78, cross_border_control=0.12,
        offline_capability=0.80, user_autonomy=0.85,
        censorship_resistance=0.88, foreign_dependence=0.12,
        monetary_policy_independence=0.82, digital_literacy_gap=0.14,
        infrastructure_resilience=0.75, regulatory_capture=0.12,
        geopolitical_leverage=0.10,
    ),
]


class CBDCSovereigntyEngine:
    def analyze(self, entities: List[CBDCSovereigntyInput]) -> Dict[str, Any]:
        results = [analyze_cbdc_sovereignty(e) for e in entities]

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
            pattern_distribution[r.cbdc_pattern] = pattern_distribution.get(r.cbdc_pattern, 0) + 1
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
        results: List[CBDCSovereigntyResult] = None,
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
            "module_id": 395,
            "module_name": "CBDC & Souveraineté Monnaie Numérique Intelligence Engine",
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
            "avg_estimated_cbdc_sovereignty_index": round(avg_composite / 100 * 10, 2),
        }
