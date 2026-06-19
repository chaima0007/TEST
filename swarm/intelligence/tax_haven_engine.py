from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class TaxHavenInput:
    entity_id: str
    haven_type: str
    region: str
    secrecy_score: float
    corporate_tax_rate: float
    beneficial_ownership_opacity: float
    treaty_network_abuse: float
    profit_shifting_intensity: float
    illicit_flow_volume: float
    regulatory_compliance: float
    automatic_info_exchange: float
    beneficial_ownership_register: float
    politically_exposed_persons: float
    real_estate_opacity: float
    trust_structure_opacity: float
    shell_company_ease: float
    enforcement_effectiveness: float
    civil_society_access: float
    multilateral_cooperation: float
    domestic_tax_erosion: float


@dataclass
class TaxHavenResult:
    entity_id: str
    haven_type: str
    region: str
    evasion_score: float
    opacity_score: float
    harm_score: float
    enforcement_score: float
    composite_score: float
    risk_level: str
    tax_haven_pattern: str
    severity: str
    recommended_action: str
    signal: str
    secrecy_score: float
    illicit_flow_volume: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "haven_type": self.haven_type,
            "region": self.region,
            "evasion_score": self.evasion_score,
            "opacity_score": self.opacity_score,
            "harm_score": self.harm_score,
            "enforcement_score": self.enforcement_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "tax_haven_pattern": self.tax_haven_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "secrecy_score": self.secrecy_score,
            "illicit_flow_volume": self.illicit_flow_volume,
        }


def _evasion_score(e: TaxHavenInput) -> float:
    raw = (
        e.secrecy_score * 0.4
        + e.beneficial_ownership_opacity * 0.35
        + e.treaty_network_abuse * 0.25
    ) * 100
    return round(raw * 100) / 100


def _opacity_score(e: TaxHavenInput) -> float:
    raw = (
        e.trust_structure_opacity * 0.4
        + e.real_estate_opacity * 0.35
        + e.shell_company_ease * 0.25
    ) * 100
    return round(raw * 100) / 100


def _harm_score(e: TaxHavenInput) -> float:
    raw = (
        e.illicit_flow_volume * 0.4
        + e.profit_shifting_intensity * 0.35
        + e.domestic_tax_erosion * 0.25
    ) * 100
    return round(raw * 100) / 100


def _enforcement_score(e: TaxHavenInput) -> float:
    raw = (
        (1.0 - e.enforcement_effectiveness) * 0.4
        + (1.0 - e.automatic_info_exchange) * 0.35
        + (1.0 - e.multilateral_cooperation) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    evasion: float,
    opacity: float,
    harm: float,
    enforcement: float,
) -> float:
    return round(
        (evasion * 0.30 + opacity * 0.25 + harm * 0.25 + enforcement * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _tax_haven_pattern(e: TaxHavenInput) -> str:
    if e.beneficial_ownership_opacity > 0.85 and e.politically_exposed_persons > 0.80:
        return "sovereign_wealth_capture"
    if e.profit_shifting_intensity > 0.85 and e.treaty_network_abuse > 0.80:
        return "corporate_profit_shifting"
    if e.illicit_flow_volume > 0.85 and e.shell_company_ease > 0.80:
        return "illicit_financial_flows"
    if e.secrecy_score > 0.80 and e.regulatory_compliance < 0.25:
        return "regulatory_arbitrage_network"
    if e.domestic_tax_erosion > 0.80 and e.civil_society_access < 0.25:
        return "democratic_fiscal_erosion"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_paradis_fiscal_systémique"
    if composite >= 40:
        return "opacité_financière_majeure_détectée"
    if composite >= 20:
        return "érosion_fiscale_structurelle"
    return "surveillance_conformité_fiscale"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_paradis_fiscal_critique"
    if risk == "high":
        return "renforcement_échange_informations_automatique"
    if risk == "moderate":
        return "audit_conformité_fiscale_approfondi"
    return "veille_transparence_fiscale_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise paradis fiscal systémique — évasion fiscale en péril démocratique"
    if risk == "high":
        return "🟠 Opacité financière majeure détectée — flux illicites significatifs"
    if risk == "moderate":
        return "🟡 Érosion fiscale structurelle active — risque modéré"
    return "🟢 Conformité fiscale sous surveillance"


def analyze_tax_haven(e: TaxHavenInput) -> TaxHavenResult:
    evasion = _evasion_score(e)
    opacity = _opacity_score(e)
    harm = _harm_score(e)
    enforcement = _enforcement_score(e)
    composite = _composite_score(evasion, opacity, harm, enforcement)
    risk = _risk_level(composite)
    pattern = _tax_haven_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return TaxHavenResult(
        entity_id=e.entity_id,
        haven_type=e.haven_type,
        region=e.region,
        evasion_score=evasion,
        opacity_score=opacity,
        harm_score=harm,
        enforcement_score=enforcement,
        composite_score=composite,
        risk_level=risk,
        tax_haven_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        secrecy_score=e.secrecy_score,
        illicit_flow_volume=e.illicit_flow_volume,
    )


class TaxHavenEngine:
    def analyze(self, entities: List[TaxHavenInput]) -> Dict[str, Any]:
        results = [analyze_tax_haven(e) for e in entities]

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
            pattern_distribution[r.tax_haven_pattern] = pattern_distribution.get(r.tax_haven_pattern, 0) + 1
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
        results: List[TaxHavenResult] = None,
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
            "module_id": 405,
            "module_name": "Paradis Fiscaux & Centres Financiers Offshore Intelligence Engine",
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
            "avg_estimated_tax_haven_index": round(avg_composite / 100 * 10, 2),
        }


# ── 8 Mock entities covering all 5 patterns + all 4 risk levels ───────────────
# 3 critical, 2 high, 1 moderate, 2 low — all 5 patterns covered

MOCK_ENTITIES: List[TaxHavenInput] = [
    # THE-001 — EMEA, juridiction_offshore → critical, sovereign_wealth_capture
    # beneficial_ownership_opacity>0.85 AND politically_exposed_persons>0.80
    # composite≥60 → critical
    TaxHavenInput(
        entity_id="THE-001", haven_type="juridiction_offshore", region="EMEA",
        secrecy_score=0.90,
        corporate_tax_rate=0.05,
        beneficial_ownership_opacity=0.92,
        treaty_network_abuse=0.75,
        profit_shifting_intensity=0.70,
        illicit_flow_volume=0.78,
        regulatory_compliance=0.15,
        automatic_info_exchange=0.12,
        beneficial_ownership_register=0.10,
        politically_exposed_persons=0.88,
        real_estate_opacity=0.80,
        trust_structure_opacity=0.85,
        shell_company_ease=0.78,
        enforcement_effectiveness=0.10,
        civil_society_access=0.15,
        multilateral_cooperation=0.12,
        domestic_tax_erosion=0.82,
    ),
    # THE-002 — APAC, centre_financier_offshore → critical, corporate_profit_shifting
    # profit_shifting_intensity>0.85 AND treaty_network_abuse>0.80
    # beneficial_ownership_opacity=0.72 → avoids sovereign_wealth_capture
    # composite≥60 → critical
    TaxHavenInput(
        entity_id="THE-002", haven_type="centre_financier_offshore", region="APAC",
        secrecy_score=0.85,
        corporate_tax_rate=0.02,
        beneficial_ownership_opacity=0.72,
        treaty_network_abuse=0.88,
        profit_shifting_intensity=0.90,
        illicit_flow_volume=0.68,
        regulatory_compliance=0.18,
        automatic_info_exchange=0.15,
        beneficial_ownership_register=0.20,
        politically_exposed_persons=0.70,
        real_estate_opacity=0.72,
        trust_structure_opacity=0.80,
        shell_company_ease=0.75,
        enforcement_effectiveness=0.12,
        civil_society_access=0.18,
        multilateral_cooperation=0.15,
        domestic_tax_erosion=0.78,
    ),
    # THE-003 — LATAM, paradis_fiscal_insulaire → critical, illicit_financial_flows
    # illicit_flow_volume>0.85 AND shell_company_ease>0.80
    # beneficial_ownership_opacity=0.78 → avoids sovereign_wealth_capture
    # profit_shifting_intensity=0.75 → avoids corporate_profit_shifting
    # composite≥60 → critical
    TaxHavenInput(
        entity_id="THE-003", haven_type="paradis_fiscal_insulaire", region="LATAM",
        secrecy_score=0.88,
        corporate_tax_rate=0.00,
        beneficial_ownership_opacity=0.78,
        treaty_network_abuse=0.72,
        profit_shifting_intensity=0.75,
        illicit_flow_volume=0.92,
        regulatory_compliance=0.12,
        automatic_info_exchange=0.10,
        beneficial_ownership_register=0.08,
        politically_exposed_persons=0.75,
        real_estate_opacity=0.78,
        trust_structure_opacity=0.82,
        shell_company_ease=0.88,
        enforcement_effectiveness=0.08,
        civil_society_access=0.12,
        multilateral_cooperation=0.10,
        domestic_tax_erosion=0.80,
    ),
    # THE-004 — NOAM, zone_franche_financière → high, regulatory_arbitrage_network
    # secrecy_score>0.80 AND regulatory_compliance<0.25
    # beneficial_ownership_opacity=0.55 → avoids sovereign_wealth_capture
    # profit_shifting_intensity=0.42 → avoids corporate_profit_shifting
    # illicit_flow_volume=0.45 → avoids illicit_financial_flows
    # composite≈50.3 → high [40,60)
    TaxHavenInput(
        entity_id="THE-004", haven_type="zone_franche_financière", region="NOAM",
        secrecy_score=0.82,
        corporate_tax_rate=0.08,
        beneficial_ownership_opacity=0.55,
        treaty_network_abuse=0.45,
        profit_shifting_intensity=0.42,
        illicit_flow_volume=0.45,
        regulatory_compliance=0.22,
        automatic_info_exchange=0.45,
        beneficial_ownership_register=0.40,
        politically_exposed_persons=0.45,
        real_estate_opacity=0.48,
        trust_structure_opacity=0.52,
        shell_company_ease=0.45,
        enforcement_effectiveness=0.60,
        civil_society_access=0.48,
        multilateral_cooperation=0.42,
        domestic_tax_erosion=0.40,
    ),
    # THE-005 — MEA, juridiction_secrète → high, democratic_fiscal_erosion
    # domestic_tax_erosion>0.80 AND civil_society_access<0.25
    # beneficial_ownership_opacity=0.52 → avoids sovereign_wealth_capture
    # profit_shifting_intensity=0.45 AND treaty_network_abuse=0.48 → avoids corporate_profit_shifting
    # illicit_flow_volume=0.42 → avoids illicit_financial_flows
    # secrecy_score=0.60 → avoids regulatory_arbitrage_network (not >0.80)
    # composite≈50.2 → high [40,60)
    TaxHavenInput(
        entity_id="THE-005", haven_type="juridiction_secrète", region="MEA",
        secrecy_score=0.60,
        corporate_tax_rate=0.10,
        beneficial_ownership_opacity=0.52,
        treaty_network_abuse=0.48,
        profit_shifting_intensity=0.45,
        illicit_flow_volume=0.42,
        regulatory_compliance=0.40,
        automatic_info_exchange=0.52,
        beneficial_ownership_register=0.48,
        politically_exposed_persons=0.50,
        real_estate_opacity=0.45,
        trust_structure_opacity=0.50,
        shell_company_ease=0.42,
        enforcement_effectiveness=0.55,
        civil_society_access=0.18,
        multilateral_cooperation=0.42,
        domestic_tax_erosion=0.82,
    ),
    # THE-006 — EMEA, territoire_autonome_fiscal → moderate, none
    # composite in [20,40), no pattern triggered
    TaxHavenInput(
        entity_id="THE-006", haven_type="territoire_autonome_fiscal", region="EMEA",
        secrecy_score=0.38,
        corporate_tax_rate=0.15,
        beneficial_ownership_opacity=0.35,
        treaty_network_abuse=0.30,
        profit_shifting_intensity=0.32,
        illicit_flow_volume=0.28,
        regulatory_compliance=0.55,
        automatic_info_exchange=0.52,
        beneficial_ownership_register=0.50,
        politically_exposed_persons=0.28,
        real_estate_opacity=0.32,
        trust_structure_opacity=0.35,
        shell_company_ease=0.30,
        enforcement_effectiveness=0.55,
        civil_society_access=0.58,
        multilateral_cooperation=0.52,
        domestic_tax_erosion=0.30,
    ),
    # THE-007 — APAC, microjuridiction_offshore → low, none
    # All low values → composite<20, no pattern triggered
    TaxHavenInput(
        entity_id="THE-007", haven_type="microjuridiction_offshore", region="APAC",
        secrecy_score=0.12,
        corporate_tax_rate=0.25,
        beneficial_ownership_opacity=0.10,
        treaty_network_abuse=0.08,
        profit_shifting_intensity=0.10,
        illicit_flow_volume=0.08,
        regulatory_compliance=0.88,
        automatic_info_exchange=0.85,
        beneficial_ownership_register=0.90,
        politically_exposed_persons=0.08,
        real_estate_opacity=0.10,
        trust_structure_opacity=0.08,
        shell_company_ease=0.10,
        enforcement_effectiveness=0.85,
        civil_society_access=0.90,
        multilateral_cooperation=0.88,
        domestic_tax_erosion=0.10,
    ),
    # THE-008 — NOAM, centre_services_financiers → low, none
    # All low values → composite<20, no pattern triggered
    TaxHavenInput(
        entity_id="THE-008", haven_type="centre_services_financiers", region="NOAM",
        secrecy_score=0.10,
        corporate_tax_rate=0.22,
        beneficial_ownership_opacity=0.08,
        treaty_network_abuse=0.10,
        profit_shifting_intensity=0.08,
        illicit_flow_volume=0.10,
        regulatory_compliance=0.90,
        automatic_info_exchange=0.88,
        beneficial_ownership_register=0.85,
        politically_exposed_persons=0.10,
        real_estate_opacity=0.08,
        trust_structure_opacity=0.10,
        shell_company_ease=0.08,
        enforcement_effectiveness=0.88,
        civil_society_access=0.85,
        multilateral_cooperation=0.90,
        domestic_tax_erosion=0.08,
    ),
]
