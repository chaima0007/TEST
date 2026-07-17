from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class PharmaceuticalAccessInput:
    entity_id: str
    therapeutic_area: str
    region: str
    drug_price_index: float
    patent_monopoly_duration: float
    generic_availability: float
    insurance_coverage_gap: float
    out_of_pocket_burden: float
    compulsory_license_use: float
    clinical_trial_inclusion: float
    off_label_access: float
    essential_medicine_gap: float
    black_market_penetration: float
    counterfeiting_risk: float
    research_neglected_diseases: float
    export_restriction: float
    regulatory_pathway_speed: float
    local_manufacturing: float
    treatment_adherence: float
    quality_assurance_gap: float


@dataclass
class PharmaceuticalAccessResult:
    entity_id: str
    therapeutic_area: str
    region: str
    affordability_score: float
    monopoly_score: float
    availability_score: float
    innovation_score: float
    composite_score: float
    risk_level: str
    pharma_pattern: str
    severity: str
    recommended_action: str
    signal: str
    drug_price_index: float
    counterfeiting_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "therapeutic_area": self.therapeutic_area,
            "region": self.region,
            "affordability_score": self.affordability_score,
            "monopoly_score": self.monopoly_score,
            "availability_score": self.availability_score,
            "innovation_score": self.innovation_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "pharma_pattern": self.pharma_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "drug_price_index": self.drug_price_index,
            "counterfeiting_risk": self.counterfeiting_risk,
        }


def _affordability_score(e: PharmaceuticalAccessInput) -> float:
    raw = (
        e.drug_price_index * 0.4
        + e.out_of_pocket_burden * 0.35
        + e.insurance_coverage_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _monopoly_score(e: PharmaceuticalAccessInput) -> float:
    raw = (
        e.patent_monopoly_duration * 0.4
        + e.export_restriction * 0.35
        + e.compulsory_license_use * 0.25
    ) * 100
    return round(raw * 100) / 100


def _availability_score(e: PharmaceuticalAccessInput) -> float:
    raw = (
        e.essential_medicine_gap * 0.4
        + e.generic_availability * 0.35
        + e.black_market_penetration * 0.25
    ) * 100
    return round(raw * 100) / 100


def _innovation_score(e: PharmaceuticalAccessInput) -> float:
    raw = (
        e.research_neglected_diseases * 0.4
        + e.clinical_trial_inclusion * 0.35
        + e.quality_assurance_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    affordability: float,
    monopoly: float,
    availability: float,
    innovation: float,
) -> float:
    return round(
        (affordability * 0.30 + monopoly * 0.25 + availability * 0.25 + innovation * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _pharma_pattern(e: PharmaceuticalAccessInput) -> str:
    if e.drug_price_index > 0.85 and e.out_of_pocket_burden > 0.80:
        return "life_saving_drug_unaffordability"
    if e.patent_monopoly_duration > 0.85 and e.export_restriction > 0.80:
        return "patent_monopoly_abuse"
    if e.generic_availability > 0.85 and e.essential_medicine_gap > 0.80:
        return "generic_market_suppression"
    if e.clinical_trial_inclusion > 0.80 and e.research_neglected_diseases > 0.75:
        return "clinical_trial_exclusion"
    if e.counterfeiting_risk > 0.80 and e.black_market_penetration > 0.75:
        return "counterfeit_drug_proliferation"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_accès_médicaments_systémique"
    if composite >= 40:
        return "crise_prix_pharmaceutiques_majeure"
    if composite >= 20:
        return "inégalité_accès_médicaments_structurelle"
    return "accès_pharmaceutique_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_accès_médicaments_essentiels"
    if risk == "high":
        return "négociation_prix_licences_obligatoires_accélérée"
    if risk == "moderate":
        return "renforcement_politiques_accès_génériques"
    return "veille_marché_pharmaceutique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise accès médicaments systémique — santé publique en péril"
    if risk == "high":
        return "🟠 Crise prix pharmaceutiques majeure détectée"
    if risk == "moderate":
        return "🟡 Inégalité accès médicaments structurelle active"
    return "🟢 Accès pharmaceutique sous surveillance"


def analyze_pharmaceutical_access(e: PharmaceuticalAccessInput) -> PharmaceuticalAccessResult:
    affordability = _affordability_score(e)
    monopoly = _monopoly_score(e)
    availability = _availability_score(e)
    innovation = _innovation_score(e)
    composite = _composite_score(affordability, monopoly, availability, innovation)
    risk = _risk_level(composite)
    pattern = _pharma_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return PharmaceuticalAccessResult(
        entity_id=e.entity_id,
        therapeutic_area=e.therapeutic_area,
        region=e.region,
        affordability_score=affordability,
        monopoly_score=monopoly,
        availability_score=availability,
        innovation_score=innovation,
        composite_score=composite,
        risk_level=risk,
        pharma_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        drug_price_index=e.drug_price_index,
        counterfeiting_risk=e.counterfeiting_risk,
    )


class PharmaceuticalAccessEngine:
    def analyze(self, entities: List[PharmaceuticalAccessInput]) -> Dict[str, Any]:
        results = [analyze_pharmaceutical_access(e) for e in entities]

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
            pattern_distribution[r.pharma_pattern] = pattern_distribution.get(r.pharma_pattern, 0) + 1
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
        results: List[PharmaceuticalAccessResult] = None,
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
            "module_id": 411,
            "module_name": "Accès Médicaments & Prix Pharmaceutiques Intelligence Engine",
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
            "avg_estimated_pharma_access_index": round(avg_composite / 100 * 10, 2),
        }
