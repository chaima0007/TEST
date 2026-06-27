"""
Module 353 — Digital Twins & Physical-Digital Infrastructure Intelligence Engine
Monitors digital twin infrastructure for synchronisation failures, adversarial attacks,
physical dependency risks, vendor lock-in, and cascading collapse scenarios.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DigitalTwinsInput:
    entity_id: str
    twin_domain: str
    region: str
    # 17 float fields 0-1
    digital_physical_synchronization_gap: float
    twin_data_integrity_risk: float
    adversarial_twin_manipulation_risk: float
    twin_sovereignty_capture_index: float
    real_time_feedback_latency_risk: float
    twin_divergence_crisis_probability: float
    proprietary_lock_in_twin_vendor: float
    simulation_accuracy_degradation: float
    cascading_twin_failure_risk: float
    AI_decision_twin_autonomy_risk: float
    twin_cybersecurity_vulnerability: float
    physical_dependency_on_twin_decisions: float
    twin_data_monopoly_concentration: float
    regulatory_twin_gap: float
    twin_workforce_displacement: float
    cross_sector_twin_interdependency: float
    emergency_twin_override_capability: float


@dataclass
class DigitalTwinsResult:
    entity_id: str
    twin_domain: str
    region: str
    sync_score: float
    security_score: float
    dependency_score: float
    sovereignty_score: float
    composite_score: float
    risk_level: str
    twin_pattern: str
    severity: str
    recommended_action: str
    signal: str
    digital_physical_synchronization_gap: float
    adversarial_twin_manipulation_risk: float

    def to_dict(self) -> Dict:
        return {
            "entity_id":                            self.entity_id,
            "twin_domain":                          self.twin_domain,
            "region":                               self.region,
            "sync_score":                           self.sync_score,
            "security_score":                       self.security_score,
            "dependency_score":                     self.dependency_score,
            "sovereignty_score":                    self.sovereignty_score,
            "composite_score":                      self.composite_score,
            "risk_level":                           self.risk_level,
            "twin_pattern":                         self.twin_pattern,
            "severity":                             self.severity,
            "recommended_action":                   self.recommended_action,
            "signal":                               self.signal,
            "digital_physical_synchronization_gap": self.digital_physical_synchronization_gap,
            "adversarial_twin_manipulation_risk":   self.adversarial_twin_manipulation_risk,
        }


class DigitalTwinsInfrastructureEngine:
    def __init__(self) -> None:
        self._results: List[DigitalTwinsResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _sync_score(self, i: DigitalTwinsInput) -> float:
        s = (
            i.digital_physical_synchronization_gap * 0.40
            + i.twin_divergence_crisis_probability * 0.35
            + i.real_time_feedback_latency_risk * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _security_score(self, i: DigitalTwinsInput) -> float:
        s = (
            i.adversarial_twin_manipulation_risk * 0.40
            + i.twin_cybersecurity_vulnerability * 0.35
            + i.AI_decision_twin_autonomy_risk * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _dependency_score(self, i: DigitalTwinsInput) -> float:
        s = (
            i.physical_dependency_on_twin_decisions * 0.40
            + i.cascading_twin_failure_risk * 0.35
            + i.cross_sector_twin_interdependency * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _sovereignty_score(self, i: DigitalTwinsInput) -> float:
        s = (
            i.twin_sovereignty_capture_index * 0.40
            + i.proprietary_lock_in_twin_vendor * 0.35
            + i.twin_data_monopoly_concentration * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _composite(self, sync: float, sec: float, dep: float, sov: float) -> float:
        return min(
            round(sync * 0.30 + sec * 0.25 + dep * 0.25 + sov * 0.20, 2),
            100.0,
        )

    # ------------------------------------------------------------------ #
    #  Risk                                                                #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> str:
        if c >= 60:
            return "critical"
        if c >= 40:
            return "high"
        if c >= 20:
            return "moderate"
        return "low"

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: DigitalTwinsInput) -> str:
        if (
            i.digital_physical_synchronization_gap >= 0.70
            and i.twin_divergence_crisis_probability >= 0.65
        ):
            return "twin_divergence_catastrophe"
        if (
            i.adversarial_twin_manipulation_risk >= 0.70
            and i.twin_cybersecurity_vulnerability >= 0.65
        ):
            return "adversarial_twin_attack"
        if (
            i.physical_dependency_on_twin_decisions >= 0.70
            and i.emergency_twin_override_capability <= 0.35
        ):
            return "physical_twin_lock"
        if (
            i.proprietary_lock_in_twin_vendor >= 0.70
            and i.twin_data_monopoly_concentration >= 0.65
        ):
            return "twin_vendor_monopoly"
        if (
            i.cascading_twin_failure_risk >= 0.70
            and i.cross_sector_twin_interdependency >= 0.65
        ):
            return "cascading_twin_collapse"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity & action & signal                                          #
    # ------------------------------------------------------------------ #

    def _severity(self, risk: str) -> str:
        return {
            "critical": "effondrement_jumeau_numérique_critique",
            "high":     "crise_infrastructure_jumeau_majeure",
            "moderate": "fragilité_jumeau_numérique_structurelle",
            "low":      "jumeau_numérique_stable",
        }[risk]

    def _action(self, risk: str) -> str:
        return {
            "critical": "intervention_urgente_résilience_jumeau",
            "high":     "sécurisation_accélérée_infrastructure_jumeau",
            "moderate": "renforcement_indépendance_jumeau_numérique",
            "low":      "veille_jumeau_numérique_continue",
        }[risk]

    def _signal(self, risk: str) -> str:
        return {
            "critical": "🔴 Effondrement jumeau numérique — infrastructure critique compromise",
            "high":     "🟠 Crise infrastructure jumeau majeure détectée",
            "moderate": "🟡 Fragilité jumeau numérique structurelle active",
            "low":      "🟢 Infrastructure jumeau numérique stable",
        }[risk]

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: DigitalTwinsInput) -> DigitalTwinsResult:
        sync = self._sync_score(i)
        sec  = self._security_score(i)
        dep  = self._dependency_score(i)
        sov  = self._sovereignty_score(i)
        comp = self._composite(sync, sec, dep, sov)
        risk = self._risk(comp)
        pat  = self._pattern(i)
        sev  = self._severity(risk)
        act  = self._action(risk)
        sig  = self._signal(risk)
        result = DigitalTwinsResult(
            entity_id=i.entity_id,
            twin_domain=i.twin_domain,
            region=i.region,
            sync_score=sync,
            security_score=sec,
            dependency_score=dep,
            sovereignty_score=sov,
            composite_score=comp,
            risk_level=risk,
            twin_pattern=pat,
            severity=sev,
            recommended_action=act,
            signal=sig,
            digital_physical_synchronization_gap=i.digital_physical_synchronization_gap,
            adversarial_twin_manipulation_risk=i.adversarial_twin_manipulation_risk,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[DigitalTwinsInput]) -> List[DigitalTwinsResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "module_id":                    353,
                "module_name":                  "Digital Twins & Physical-Digital Infrastructure Intelligence Engine",
                "total_entities":               0,
                "critical_count":               0,
                "high_count":                   0,
                "moderate_count":               0,
                "low_count":                    0,
                "avg_composite":                0.0,
                "pattern_distribution":         {},
                "risk_distribution":            {},
                "severity_distribution":        {},
                "action_distribution":          {},
                "avg_estimated_twin_risk_index": 0.0,
            }
        n = len(self._results)
        pat_dist:  Dict[str, int] = {}
        risk_dist: Dict[str, int] = {}
        sev_dist:  Dict[str, int] = {}
        act_dist:  Dict[str, int] = {}
        total_comp = 0.0
        critical_c = high_c = moderate_c = low_c = 0
        for r in self._results:
            pat_dist[r.twin_pattern]       = pat_dist.get(r.twin_pattern, 0) + 1
            risk_dist[r.risk_level]        = risk_dist.get(r.risk_level, 0) + 1
            sev_dist[r.severity]           = sev_dist.get(r.severity, 0) + 1
            act_dist[r.recommended_action] = act_dist.get(r.recommended_action, 0) + 1
            total_comp += r.composite_score
            if r.risk_level == "critical":
                critical_c  += 1
            elif r.risk_level == "high":
                high_c      += 1
            elif r.risk_level == "moderate":
                moderate_c  += 1
            else:
                low_c       += 1
        avg_comp = round(total_comp / n, 1)
        return {
            "module_id":                    353,
            "module_name":                  "Digital Twins & Physical-Digital Infrastructure Intelligence Engine",
            "total_entities":               n,
            "critical_count":               critical_c,
            "high_count":                   high_c,
            "moderate_count":               moderate_c,
            "low_count":                    low_c,
            "avg_composite":                avg_comp,
            "pattern_distribution":         pat_dist,
            "risk_distribution":            risk_dist,
            "severity_distribution":        sev_dist,
            "action_distribution":          act_dist,
            "avg_estimated_twin_risk_index": round(avg_comp / 100 * 10, 2),
        }
