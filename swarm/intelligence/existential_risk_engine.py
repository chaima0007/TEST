from dataclasses import dataclass
from typing import List, Dict, Any, Literal

RiskCategory = Literal[
    "civilizational_collapse", "pandemics_biosecurity", "ai_misalignment",
    "nuclear_risk", "climate_tipping", "financial_system_failure",
    "democratic_erosion", "technology_singularity"
]

@dataclass
class ExistentialRiskInput:
    entity_id: str
    risk_category: RiskCategory
    region: str
    existential_exposure_score: float          # higher = worse
    continuity_plan_robustness: float
    black_swan_preparedness: float
    cascade_failure_vulnerability: float       # higher = worse
    civilizational_resilience_score: float
    institutional_trust_erosion_rate: float    # higher = worse
    strategic_optionality_reserve: float
    antifragility_score: float
    early_warning_system_quality: float
    societal_cohesion_index: float
    technological_dependency_risk: float       # higher = worse
    resource_sovereignty_score: float
    emergency_governance_readiness: float
    knowledge_preservation_score: float
    regenerative_recovery_capacity: float
    strategic_redundancy_depth: float
    existential_hedge_ratio: float


def _exposure_score(e: ExistentialRiskInput) -> float:
    """0.30 weight — higher raw values = worse exposure"""
    raw = (e.existential_exposure_score + e.cascade_failure_vulnerability + e.technological_dependency_risk) / 3.0
    return round(raw * 100, 2)


def _preparedness_score(e: ExistentialRiskInput) -> float:
    """0.25 weight — inverted: high preparedness = low risk"""
    raw = ((1 - e.black_swan_preparedness) + (1 - e.early_warning_system_quality) + (1 - e.emergency_governance_readiness)) / 3.0
    return round(raw * 100, 2)


def _resilience_score(e: ExistentialRiskInput) -> float:
    """0.25 weight — inverted: high resilience = low risk"""
    raw = ((1 - e.civilizational_resilience_score) + (1 - e.antifragility_score) + (1 - e.regenerative_recovery_capacity)) / 3.0
    return round(raw * 100, 2)


def _continuity_score(e: ExistentialRiskInput) -> float:
    """0.20 weight — inverted: high continuity readiness = low risk"""
    raw = ((1 - e.continuity_plan_robustness) + (1 - e.strategic_redundancy_depth) + (1 - e.knowledge_preservation_score)) / 3.0
    return round(raw * 100, 2)


def _composite(exp: float, prep: float, res: float, cont: float) -> float:
    return round(exp * 0.30 + prep * 0.25 + res * 0.25 + cont * 0.20, 2)


def _pattern(e: ExistentialRiskInput) -> str:
    if e.existential_exposure_score >= 0.75 and e.cascade_failure_vulnerability >= 0.70:
        return "existential_cascade"
    if e.institutional_trust_erosion_rate >= 0.70 and e.societal_cohesion_index <= 0.30:
        return "institutional_collapse"
    if e.institutional_trust_erosion_rate >= 0.50 and e.societal_cohesion_index <= 0.50:
        return "civilizational_drift"
    if e.black_swan_preparedness <= 0.25 and e.early_warning_system_quality <= 0.30:
        return "black_swan_blindspot"
    if e.continuity_plan_robustness <= 0.25 and e.strategic_redundancy_depth <= 0.30:
        return "continuity_failure"
    return "none"


def _severity(comp: float) -> str:
    if comp >= 65: return "existential"
    if comp >= 45: return "critical_systemic"
    if comp >= 25: return "high_alert"
    return "resilient"


def _risk_level(comp: float) -> str:
    if comp >= 65: return "critical"
    if comp >= 45: return "high"
    if comp >= 25: return "moderate"
    return "low"


def _action(risk: str, pattern: str) -> str:
    if risk == "critical":
        if pattern in ("existential_cascade", "black_swan_blindspot"):
            return "existential_continuity_protocol"
        return "civilizational_hedge"
    if risk == "high":
        if pattern in ("institutional_collapse", "civilizational_drift"):
            return "resilience_reinforcement"
        return "cascade_prevention"
    if risk == "moderate":
        return "existential_monitoring"
    return "no_action"


def _signal(e: ExistentialRiskInput, pattern: str, comp: float) -> str:
    resilience_pct = round(e.civilizational_resilience_score * 100)
    antifragility_pct = round(e.antifragility_score * 100)
    continuity_pct = round(e.continuity_plan_robustness * 100)
    if comp < 25:
        return (
            f"Risque existentiel maîtrisé — résilience civilisationnelle {resilience_pct}% "
            f"— antifragilité {antifragility_pct}% — continuité stratégique {continuity_pct}%"
        )
    labels: Dict[str, str] = {
        "existential_cascade":    "Cascade existentielle",
        "institutional_collapse": "Effondrement institutionnel",
        "civilizational_drift":   "Dérive civilisationnelle",
        "black_swan_blindspot":   "Angle mort cygne noir",
        "continuity_failure":     "Défaillance continuité",
    }
    label = labels.get(pattern, pattern.replace("_", " "))
    return (
        f"{label} — exposition {round(e.existential_exposure_score * 100)}% "
        f"— vulnérabilité cascade {round(e.cascade_failure_vulnerability * 100)}% "
        f"— résilience {resilience_pct}% — composite {round(comp)}"
    )


class ExistentialRiskEngine:
    def __init__(self, entities: List[ExistentialRiskInput]):
        self.entities = entities
        self._results: List[Dict[str, Any]] = []

    def assess_batch(self) -> List[Dict[str, Any]]:
        self._results = [self._assess(e) for e in self.entities]
        return self._results

    def _assess(self, e: ExistentialRiskInput) -> Dict[str, Any]:
        exp  = _exposure_score(e)
        prep = _preparedness_score(e)
        res  = _resilience_score(e)
        cont = _continuity_score(e)
        comp = _composite(exp, prep, res, cont)
        pat  = _pattern(e)
        risk = _risk_level(comp)
        sev  = _severity(comp)
        act  = _action(risk, pat)
        sig  = _signal(e, pat, comp)
        return {
            "entity_id":                     e.entity_id,
            "region":                         e.region,
            "risk_category":                  e.risk_category,
            "existential_risk_level":         risk,
            "existential_pattern":            pat,
            "systemic_severity":              sev,
            "recommended_protocol":           act,
            "exposure_score":                 exp,
            "preparedness_score":             prep,
            "resilience_score":               res,
            "continuity_score":               cont,
            "existential_composite":          comp,
            "has_cascade_signal":             comp >= 45 or e.cascade_failure_vulnerability >= 0.60 or e.existential_exposure_score >= 0.65,
            "requires_continuity_protocol":   comp >= 30 or e.continuity_plan_robustness <= 0.30 or e.strategic_redundancy_depth <= 0.25,
            "estimated_existential_risk_index": round(min(comp / 100 * (1 - e.antifragility_score + 0.01) * 10, 10.0), 2),
            "existential_signal":             sig,
        }

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        if not self._results:
            self.assess_batch()
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        t_exp = t_prep = t_res = t_cont = t_comp = t_eri = 0.0
        cascade_c = continuity_c = 0
        for r in self._results:
            rc[r["existential_risk_level"]]  = rc.get(r["existential_risk_level"], 0) + 1
            pc[r["existential_pattern"]]     = pc.get(r["existential_pattern"], 0) + 1
            sc[r["systemic_severity"]]       = sc.get(r["systemic_severity"], 0) + 1
            ac[r["recommended_protocol"]]    = ac.get(r["recommended_protocol"], 0) + 1
            t_exp  += r["exposure_score"]
            t_prep += r["preparedness_score"]
            t_res  += r["resilience_score"]
            t_cont += r["continuity_score"]
            t_comp += r["existential_composite"]
            t_eri  += r["estimated_existential_risk_index"]
            if r["has_cascade_signal"]:      cascade_c += 1
            if r["requires_continuity_protocol"]: continuity_c += 1
        n = len(self._results)
        return {
            "total":                           n,
            "risk_counts":                     rc,
            "pattern_counts":                  pc,
            "severity_counts":                 sc,
            "protocol_counts":                 ac,
            "avg_existential_composite":       round(t_comp / n, 1),
            "cascade_signal_count":            cascade_c,
            "continuity_protocol_required_count": continuity_c,
            "avg_exposure_score":              round(t_exp / n, 1),
            "avg_preparedness_score":          round(t_prep / n, 1),
            "avg_resilience_score":            round(t_res / n, 1),
            "avg_continuity_score":            round(t_cont / n, 1),
            "avg_estimated_existential_risk_index": round(t_eri / n, 2),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        if not self._results:
            self.assess_batch()
        s = self.summary()
        return {
            "entities":                        self._results,
            "summary":                         s,
            "total":                           s["total"],
            "risk_counts":                     s["risk_counts"],
            "pattern_counts":                  s["pattern_counts"],
            "severity_counts":                 s["severity_counts"],
            "protocol_counts":                 s["protocol_counts"],
            "avg_existential_composite":       s["avg_existential_composite"],
            "cascade_signal_count":            s["cascade_signal_count"],
            "continuity_protocol_required_count": s["continuity_protocol_required_count"],
            "avg_exposure_score":              s["avg_exposure_score"],
            "avg_preparedness_score":          s["avg_preparedness_score"],
            "avg_resilience_score":            s["avg_resilience_score"],
            "avg_continuity_score":            s["avg_continuity_score"],
            "avg_estimated_existential_risk_index": s["avg_estimated_existential_risk_index"],
        }
