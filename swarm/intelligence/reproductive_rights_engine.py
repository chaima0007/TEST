"""
Module 396 — Droits Reproductifs & Autonomie Corporelle Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ReproductiveRightsInput:
    entity_id: str
    rights_domain: str
    region: str
    legal_access: float
    healthcare_access: float
    coercion_index: float
    criminalization_risk: float
    maternal_mortality_rate: float
    contraception_coverage: float
    sex_education_quality: float
    poverty_intersection: float
    racial_disparity: float
    geographic_inequality: float
    provider_shortage: float
    stigma_index: float
    data_surveillance: float
    political_restriction: float
    international_compliance: float
    youth_access: float
    disability_inclusion: float


@dataclass
class ReproductiveRightsResult:
    entity_id: str
    region: str
    rights_domain: str
    reproductive_risk: str
    reproductive_pattern: str
    reproductive_severity: str
    recommended_action: str
    access_score: float
    legal_score: float
    coercion_score: float
    disparity_score: float
    reproductive_composite: float
    is_in_reproductive_crisis: bool
    requires_reproductive_intervention: bool
    reproductive_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "rights_domain": self.rights_domain,
            "reproductive_risk": self.reproductive_risk,
            "reproductive_pattern": self.reproductive_pattern,
            "reproductive_severity": self.reproductive_severity,
            "recommended_action": self.recommended_action,
            "access_score": self.access_score,
            "legal_score": self.legal_score,
            "coercion_score": self.coercion_score,
            "disparity_score": self.disparity_score,
            "reproductive_composite": self.reproductive_composite,
            "is_in_reproductive_crisis": self.is_in_reproductive_crisis,
            "requires_reproductive_intervention": self.requires_reproductive_intervention,
            "reproductive_signal": self.reproductive_signal,
        }


def _access_score(e: ReproductiveRightsInput) -> float:
    raw = (
        (1 - e.healthcare_access) * 0.40
        + (1 - e.contraception_coverage) * 0.35
        + e.provider_shortage * 0.25
    ) * 100
    return round(raw * 100) / 100


def _legal_score(e: ReproductiveRightsInput) -> float:
    raw = (
        (1 - e.legal_access) * 0.40
        + e.criminalization_risk * 0.35
        + e.political_restriction * 0.25
    ) * 100
    return round(raw * 100) / 100


def _coercion_score(e: ReproductiveRightsInput) -> float:
    raw = (
        e.coercion_index * 0.40
        + e.stigma_index * 0.35
        + e.data_surveillance * 0.25
    ) * 100
    return round(raw * 100) / 100


def _disparity_score(e: ReproductiveRightsInput) -> float:
    raw = (
        e.racial_disparity * 0.40
        + e.geographic_inequality * 0.35
        + e.poverty_intersection * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(access: float, legal: float, coercion: float, disparity: float) -> float:
    return round((access * 0.30 + legal * 0.25 + coercion * 0.25 + disparity * 0.20) * 100) / 100


def _reproductive_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _reproductive_pattern(e: ReproductiveRightsInput) -> str:
    if e.criminalization_risk >= 0.75 and e.legal_access <= 0.20:
        return "total_abortion_ban_crisis"
    if e.coercion_index >= 0.70 and e.racial_disparity >= 0.65:
        return "coercive_sterilization_pattern"
    if e.maternal_mortality_rate >= 0.70 and e.healthcare_access <= 0.30:
        return "maternal_mortality_collapse"
    if (1 - e.contraception_coverage) >= 0.65 and e.provider_shortage >= 0.60:
        return "contraception_access_barrier"
    if e.data_surveillance >= 0.70 and e.political_restriction >= 0.65:
        return "reproductive_surveillance_state"
    return "none"


def _reproductive_severity(composite: float) -> str:
    if composite >= 75:
        return "urgence_reproductive"
    if composite >= 50:
        return "risque_reproductif_élevé"
    if composite >= 25:
        return "stress_reproductif"
    return "autonomie_corporelle_préservée"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "intervention_d_urgence_reproductive"
    if risk == "high" and pattern == "maternal_mortality_collapse":
        return "sauvetage_maternel_prioritaire"
    if risk == "high":
        return "renforcement_droits_reproductifs"
    if risk == "moderate":
        return "surveillance_reproductive"
    return "aucune_action"


def _reproductive_signal(e: ReproductiveRightsInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — accès légal {int(e.legal_access * 100)}% "
            f"— risque criminalisation {int(e.criminalization_risk * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — couverture contraception {int(e.contraception_coverage * 100)}% "
            f"— mortalité maternelle {int(e.maternal_mortality_rate * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — accès soins {int(e.healthcare_access * 100)}% "
            f"— composite {comp_int}"
        )
    return "Droits reproductifs protégés — autonomie corporelle respectée, accès universel garanti"


def analyze_entity(e: ReproductiveRightsInput) -> ReproductiveRightsResult:
    access = _access_score(e)
    legal = _legal_score(e)
    coercion = _coercion_score(e)
    disparity = _disparity_score(e)
    comp = _composite(access, legal, coercion, disparity)
    risk = _reproductive_risk(comp)
    pattern = _reproductive_pattern(e)
    severity = _reproductive_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _reproductive_signal(e, risk, comp)

    return ReproductiveRightsResult(
        entity_id=e.entity_id,
        region=e.region,
        rights_domain=e.rights_domain,
        reproductive_risk=risk,
        reproductive_pattern=pattern,
        reproductive_severity=severity,
        recommended_action=action,
        access_score=access,
        legal_score=legal,
        coercion_score=coercion,
        disparity_score=disparity,
        reproductive_composite=comp,
        is_in_reproductive_crisis=comp >= 60,
        requires_reproductive_intervention=comp >= 40,
        reproductive_signal=signal,
    )


MOCK_ENTITIES = [
    # RRE-001 — LATAM, avortement → critical, total_abortion_ban_crisis
    ReproductiveRightsInput(
        entity_id="RRE-001", rights_domain="avortement", region="LATAM",
        legal_access=0.05, healthcare_access=0.20, coercion_index=0.60,
        criminalization_risk=0.92, maternal_mortality_rate=0.75, contraception_coverage=0.30,
        sex_education_quality=0.18, poverty_intersection=0.78, racial_disparity=0.55,
        geographic_inequality=0.68, provider_shortage=0.72, stigma_index=0.75,
        data_surveillance=0.42, political_restriction=0.88, international_compliance=0.12,
        youth_access=0.15, disability_inclusion=0.10,
    ),
    # RRE-002 — APAC, stérilisation → critical, coercive_sterilization_pattern
    ReproductiveRightsInput(
        entity_id="RRE-002", rights_domain="stérilisation", region="APAC",
        legal_access=0.22, healthcare_access=0.35, coercion_index=0.82,
        criminalization_risk=0.55, maternal_mortality_rate=0.48, contraception_coverage=0.40,
        sex_education_quality=0.22, poverty_intersection=0.70, racial_disparity=0.80,
        geographic_inequality=0.60, provider_shortage=0.58, stigma_index=0.72,
        data_surveillance=0.50, political_restriction=0.65, international_compliance=0.18,
        youth_access=0.20, disability_inclusion=0.15,
    ),
    # RRE-003 — SSA, santé maternelle → critical, maternal_mortality_collapse
    ReproductiveRightsInput(
        entity_id="RRE-003", rights_domain="santé_maternelle", region="SSA",
        legal_access=0.28, healthcare_access=0.12, coercion_index=0.55,
        criminalization_risk=0.60, maternal_mortality_rate=0.90, contraception_coverage=0.22,
        sex_education_quality=0.20, poverty_intersection=0.85, racial_disparity=0.65,
        geographic_inequality=0.75, provider_shortage=0.88, stigma_index=0.60,
        data_surveillance=0.30, political_restriction=0.58, international_compliance=0.20,
        youth_access=0.18, disability_inclusion=0.08,
    ),
    # RRE-004 — MEA, contraception → high, contraception_access_barrier
    ReproductiveRightsInput(
        entity_id="RRE-004", rights_domain="contraception", region="MEA",
        legal_access=0.38, healthcare_access=0.35, coercion_index=0.50,
        criminalization_risk=0.45, maternal_mortality_rate=0.52, contraception_coverage=0.20,
        sex_education_quality=0.25, poverty_intersection=0.62, racial_disparity=0.48,
        geographic_inequality=0.55, provider_shortage=0.72, stigma_index=0.58,
        data_surveillance=0.38, political_restriction=0.55, international_compliance=0.28,
        youth_access=0.22, disability_inclusion=0.18,
    ),
    # RRE-005 — EMEA, surveillance → high, reproductive_surveillance_state
    ReproductiveRightsInput(
        entity_id="RRE-005", rights_domain="surveillance_reproductive", region="EMEA",
        legal_access=0.42, healthcare_access=0.55, coercion_index=0.58,
        criminalization_risk=0.48, maternal_mortality_rate=0.32, contraception_coverage=0.60,
        sex_education_quality=0.40, poverty_intersection=0.42, racial_disparity=0.38,
        geographic_inequality=0.42, provider_shortage=0.45, stigma_index=0.55,
        data_surveillance=0.82, political_restriction=0.78, international_compliance=0.35,
        youth_access=0.38, disability_inclusion=0.30,
    ),
    # RRE-006 — NOAM, éducation sexuelle → moderate, none
    ReproductiveRightsInput(
        entity_id="RRE-006", rights_domain="éducation_sexuelle", region="NOAM",
        legal_access=0.65, healthcare_access=0.62, coercion_index=0.30,
        criminalization_risk=0.25, maternal_mortality_rate=0.28, contraception_coverage=0.68,
        sex_education_quality=0.38, poverty_intersection=0.35, racial_disparity=0.40,
        geographic_inequality=0.30, provider_shortage=0.32, stigma_index=0.35,
        data_surveillance=0.28, political_restriction=0.30, international_compliance=0.62,
        youth_access=0.42, disability_inclusion=0.40,
    ),
    # RRE-007 — NOAM, avortement → low, none
    ReproductiveRightsInput(
        entity_id="RRE-007", rights_domain="avortement", region="NOAM",
        legal_access=0.90, healthcare_access=0.88, coercion_index=0.08,
        criminalization_risk=0.05, maternal_mortality_rate=0.10, contraception_coverage=0.92,
        sex_education_quality=0.85, poverty_intersection=0.12, racial_disparity=0.10,
        geographic_inequality=0.08, provider_shortage=0.10, stigma_index=0.08,
        data_surveillance=0.05, political_restriction=0.08, international_compliance=0.95,
        youth_access=0.88, disability_inclusion=0.82,
    ),
    # RRE-008 — EU, droits reproductifs → low, none
    ReproductiveRightsInput(
        entity_id="RRE-008", rights_domain="droits_reproductifs", region="EU",
        legal_access=0.88, healthcare_access=0.90, coercion_index=0.05,
        criminalization_risk=0.04, maternal_mortality_rate=0.08, contraception_coverage=0.90,
        sex_education_quality=0.88, poverty_intersection=0.10, racial_disparity=0.08,
        geographic_inequality=0.06, provider_shortage=0.08, stigma_index=0.06,
        data_surveillance=0.04, political_restriction=0.05, international_compliance=0.98,
        youth_access=0.90, disability_inclusion=0.85,
    ),
]


class ReproductiveRightsEngine:
    def run(self, inputs: List[ReproductiveRightsInput]) -> Dict[str, Any]:
        results = [analyze_entity(e) for e in inputs]
        entities = [r.to_dict() for r in results]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_access = 0.0
        total_legal = 0.0
        total_coercion = 0.0
        total_disparity = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.reproductive_risk] = risk_counts.get(r.reproductive_risk, 0) + 1
            pattern_counts[r.reproductive_pattern] = pattern_counts.get(r.reproductive_pattern, 0) + 1
            severity_counts[r.reproductive_severity] = severity_counts.get(r.reproductive_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.reproductive_composite
            total_access += r.access_score
            total_legal += r.legal_score
            total_coercion += r.coercion_score
            total_disparity += r.disparity_score
            if r.is_in_reproductive_crisis:
                crisis_count += 1
            if r.requires_reproductive_intervention:
                intervention_count += 1

        n = len(results)
        avg_composite = round(total_composite / n * 10) / 10 if n else 0.0

        summary = {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_reproductive_composite": avg_composite,
            "reproductive_crisis_count": crisis_count,
            "reproductive_intervention_count": intervention_count,
            "avg_access_score": round(total_access / n * 10) / 10 if n else 0.0,
            "avg_legal_score": round(total_legal / n * 10) / 10 if n else 0.0,
            "avg_coercion_score": round(total_coercion / n * 10) / 10 if n else 0.0,
            "avg_disparity_score": round(total_disparity / n * 10) / 10 if n else 0.0,
            "avg_estimated_reproductive_rights_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": entities, "summary": summary}


if __name__ == "__main__":
    engine = ReproductiveRightsEngine()
    output = engine.run(MOCK_ENTITIES)
    import json
    print(json.dumps(output, ensure_ascii=False, indent=2))
