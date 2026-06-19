from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GeneticPrivacyInput:
    entity_id: str
    data_type: str
    region: str
    informed_consent_quality: float
    data_re_identification_risk: float
    third_party_sharing_opacity: float
    law_enforcement_access: float
    insurance_discrimination_risk: float
    employment_discrimination_risk: float
    family_cascade_exposure: float
    cross_border_data_flow: float
    security_breach_vulnerability: float
    biobank_commercial_exploitation: float
    indigenous_genetic_sovereignty: float
    minors_data_collection: float
    genetic_genealogy_use: float
    research_benefit_sharing: float
    regulatory_framework_strength: float
    opt_out_effectiveness: float
    right_to_deletion: float


@dataclass
class GeneticPrivacyResult:
    entity_id: str
    data_type: str
    region: str
    consent_score: float
    data_security_score: float
    discrimination_score: float
    sovereignty_score: float
    composite_score: float
    risk_level: str
    genetic_pattern: str
    severity: str
    recommended_action: str
    signal: str
    informed_consent_quality: float
    indigenous_genetic_sovereignty: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "data_type": self.data_type,
            "region": self.region,
            "consent_score": self.consent_score,
            "data_security_score": self.data_security_score,
            "discrimination_score": self.discrimination_score,
            "sovereignty_score": self.sovereignty_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "genetic_pattern": self.genetic_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "informed_consent_quality": self.informed_consent_quality,
            "indigenous_genetic_sovereignty": self.indigenous_genetic_sovereignty,
        }


def _consent_score(e: GeneticPrivacyInput) -> float:
    raw = (
        (1 - e.informed_consent_quality) * 0.4
        + e.third_party_sharing_opacity * 0.35
        + (1 - e.opt_out_effectiveness) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _data_security_score(e: GeneticPrivacyInput) -> float:
    raw = (
        e.data_re_identification_risk * 0.4
        + e.security_breach_vulnerability * 0.35
        + e.cross_border_data_flow * 0.25
    ) * 100
    return round(raw * 100) / 100


def _discrimination_score(e: GeneticPrivacyInput) -> float:
    raw = (
        e.insurance_discrimination_risk * 0.4
        + e.employment_discrimination_risk * 0.35
        + e.law_enforcement_access * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sovereignty_score(e: GeneticPrivacyInput) -> float:
    raw = (
        e.indigenous_genetic_sovereignty * 0.4
        + e.biobank_commercial_exploitation * 0.35
        + (1 - e.research_benefit_sharing) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    consent: float,
    security: float,
    discrimination: float,
    sovereignty: float,
) -> float:
    return round(
        (consent * 0.30 + security * 0.25 + discrimination * 0.25 + sovereignty * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _genetic_pattern(e: GeneticPrivacyInput) -> str:
    if e.law_enforcement_access > 0.85 and e.genetic_genealogy_use > 0.80:
        return "law_enforcement_dna_dragnet"
    if e.insurance_discrimination_risk > 0.85 and e.employment_discrimination_risk > 0.80:
        return "insurance_genetic_discrimination"
    if e.biobank_commercial_exploitation > 0.80 and e.third_party_sharing_opacity > 0.75:
        return "corporate_biobank_exploitation"
    if e.family_cascade_exposure > 0.80 and e.minors_data_collection > 0.75:
        return "family_member_privacy_violation"
    if e.indigenous_genetic_sovereignty > 0.80 and e.cross_border_data_flow > 0.75:
        return "genetic_colonialism_extraction"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_confidentialité_génétique_systémique"
    if composite >= 40:
        return "violation_droits_génétiques_majeure"
    if composite >= 20:
        return "risque_discrimination_génétique_structurel"
    return "confidentialité_génétique_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_protection_données_génétiques"
    if risk == "high":
        return "audit_immédiat_banques_adn_et_consentement"
    if risk == "moderate":
        return "renforcement_cadre_réglementaire_génétique"
    return "veille_confidentialité_génétique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise confidentialité génétique systémique — droits fondamentaux en péril"
    if risk == "high":
        return "🟠 Violation droits génétiques majeure détectée"
    if risk == "moderate":
        return "🟡 Risque discrimination génétique structurel actif"
    return "🟢 Confidentialité génétique sous surveillance"


def analyze_genetic_privacy(e: GeneticPrivacyInput) -> GeneticPrivacyResult:
    consent = _consent_score(e)
    security = _data_security_score(e)
    discrimination = _discrimination_score(e)
    sovereignty = _sovereignty_score(e)
    composite = _composite_score(consent, security, discrimination, sovereignty)
    risk = _risk_level(composite)
    pattern = _genetic_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return GeneticPrivacyResult(
        entity_id=e.entity_id,
        data_type=e.data_type,
        region=e.region,
        consent_score=consent,
        data_security_score=security,
        discrimination_score=discrimination,
        sovereignty_score=sovereignty,
        composite_score=composite,
        risk_level=risk,
        genetic_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        informed_consent_quality=e.informed_consent_quality,
        indigenous_genetic_sovereignty=e.indigenous_genetic_sovereignty,
    )


class GeneticPrivacyEngine:
    def analyze(self, entities: List[GeneticPrivacyInput]) -> Dict[str, Any]:
        results = [analyze_genetic_privacy(e) for e in entities]

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
            pattern_distribution[r.genetic_pattern] = pattern_distribution.get(r.genetic_pattern, 0) + 1
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
        results: List[GeneticPrivacyResult] = None,
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
            "module_id": 431,
            "module_name": "Confidentialité Génétique & Banques de Données ADN Intelligence Engine",
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
            "avg_estimated_genetic_privacy_index": round(avg_composite / 100 * 10, 2),
        }
