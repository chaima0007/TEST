from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RareDiseaseInput:
    entity_id: str
    disease_category: str
    region: str
    diagnostic_delay_years: float
    misdiagnosis_rate: float
    treatment_availability_gap: float
    orphan_drug_price_index: float
    research_investment_gap: float
    clinical_trial_access: float
    regulatory_approval_delay: float
    patient_registry_gap: float
    off_label_use_risk: float
    compassionate_use_barrier: float
    insurance_coverage_gap: float
    biobank_access_restriction: float
    patient_group_funding_capture: float
    cross_border_access_barrier: float
    genetic_test_availability: float
    newborn_screening_gap: float
    specialist_density_gap: float


@dataclass
class RareDiseaseResult:
    entity_id: str
    disease_category: str
    region: str
    access_score: float
    research_score: float
    affordability_score: float
    regulatory_score: float
    composite_score: float
    risk_level: str
    rare_disease_pattern: str
    severity: str
    recommended_action: str
    signal: str
    orphan_drug_price_index: float
    diagnostic_delay_years: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "disease_category": self.disease_category,
            "region": self.region,
            "access_score": self.access_score,
            "research_score": self.research_score,
            "affordability_score": self.affordability_score,
            "regulatory_score": self.regulatory_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "rare_disease_pattern": self.rare_disease_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "orphan_drug_price_index": self.orphan_drug_price_index,
            "diagnostic_delay_years": self.diagnostic_delay_years,
        }


def _access_score(e: RareDiseaseInput) -> float:
    raw = (
        e.treatment_availability_gap * 0.4
        + e.specialist_density_gap * 0.35
        + e.clinical_trial_access * 0.25
    ) * 100
    return round(raw * 100) / 100


def _research_score(e: RareDiseaseInput) -> float:
    raw = (
        e.research_investment_gap * 0.4
        + e.biobank_access_restriction * 0.35
        + e.patient_registry_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _affordability_score(e: RareDiseaseInput) -> float:
    raw = (
        e.orphan_drug_price_index * 0.4
        + e.insurance_coverage_gap * 0.35
        + e.compassionate_use_barrier * 0.25
    ) * 100
    return round(raw * 100) / 100


def _regulatory_score(e: RareDiseaseInput) -> float:
    raw = (
        e.regulatory_approval_delay * 0.4
        + e.cross_border_access_barrier * 0.35
        + e.off_label_use_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    access: float,
    research: float,
    affordability: float,
    regulatory: float,
) -> float:
    return round(
        (access * 0.30 + research * 0.25 + affordability * 0.25 + regulatory * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _rare_disease_pattern(e: RareDiseaseInput) -> str:
    if e.orphan_drug_price_index > 0.85 and e.insurance_coverage_gap > 0.80:
        return "orphan_drug_pricing_crisis"
    if e.diagnostic_delay_years > 0.85 and e.misdiagnosis_rate > 0.80:
        return "diagnostic_odyssey_barrier"
    if e.research_investment_gap > 0.85 and e.patient_registry_gap > 0.80:
        return "research_funding_desert"
    if e.regulatory_approval_delay > 0.80 and e.cross_border_access_barrier > 0.75:
        return "regulatory_pathway_blockade"
    if e.patient_group_funding_capture > 0.80 and e.newborn_screening_gap > 0.75:
        return "patient_advocacy_capture"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_accès_médicaments_orphelins_systémique"
    if composite >= 40:
        return "crise_recherche_maladies_rares_majeure"
    if composite >= 20:
        return "inégalité_accès_thérapeutique_structurelle"
    return "surveillance_maladies_rares_active"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_accès_médicaments_orphelins"
    if risk == "high":
        return "renforcement_parcours_diagnostic_et_recherche"
    if risk == "moderate":
        return "amélioration_politiques_accès_thérapeutique"
    return "veille_maladies_rares_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise accès médicaments orphelins systémique — patients en danger"
    if risk == "high":
        return "🟠 Crise recherche maladies rares majeure détectée"
    if risk == "moderate":
        return "🟡 Inégalité accès thérapeutique structurelle active"
    return "🟢 Surveillance maladies rares active"


def analyze_rare_disease(e: RareDiseaseInput) -> RareDiseaseResult:
    access = _access_score(e)
    research = _research_score(e)
    affordability = _affordability_score(e)
    regulatory = _regulatory_score(e)
    composite = _composite_score(access, research, affordability, regulatory)
    risk = _risk_level(composite)
    pattern = _rare_disease_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return RareDiseaseResult(
        entity_id=e.entity_id,
        disease_category=e.disease_category,
        region=e.region,
        access_score=access,
        research_score=research,
        affordability_score=affordability,
        regulatory_score=regulatory,
        composite_score=composite,
        risk_level=risk,
        rare_disease_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        orphan_drug_price_index=e.orphan_drug_price_index,
        diagnostic_delay_years=e.diagnostic_delay_years,
    )


class RareDiseaseEngine:
    def analyze(self, entities: List[RareDiseaseInput]) -> Dict[str, Any]:
        results = [analyze_rare_disease(e) for e in entities]

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
            pattern_distribution[r.rare_disease_pattern] = pattern_distribution.get(r.rare_disease_pattern, 0) + 1
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
        results: List[RareDiseaseResult] = None,
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
            "module_id": 435,
            "module_name": "Maladies Rares & Médicaments Orphelins Intelligence Engine",
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
            "avg_estimated_rare_disease_access_index": round(avg_composite / 100 * 10, 2),
        }
