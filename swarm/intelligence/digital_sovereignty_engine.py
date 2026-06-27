"""
Module 256 — Digital Sovereignty & Proprietary Identity Protection Engine
Monitors digital sovereignty threats — brand impersonation, identity theft,
IP ownership risks, data residency compliance, algorithm ownership claims,
proprietary data leakage, and digital identity integrity across platforms.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class SovereigntyRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class SovereigntyPattern(str, Enum):
    none               = "none"
    identity_theft     = "identity_theft"
    ip_expropriation   = "ip_expropriation"
    platform_capture   = "platform_capture"
    data_leakage       = "data_leakage"
    deepfake_attack    = "deepfake_attack"


class SovereigntySeverity(str, Enum):
    sovereign    = "sovereign"
    monitored    = "monitored"
    threatened   = "threatened"
    compromised  = "compromised"


class SovereigntyAction(str, Enum):
    no_action                = "no_action"
    sovereignty_monitoring   = "sovereignty_monitoring"
    ip_enforcement           = "ip_enforcement"
    platform_exit_strategy   = "platform_exit_strategy"
    legal_injunction         = "legal_injunction"
    emergency_identity_lock  = "emergency_identity_lock"


@dataclass
class SovereigntyInput:
    asset_id: str
    asset_domain: str   # brand_identity/intellectual_property/data_sovereignty/
                        # platform_identity/algorithm_ownership/creative_authorship/
                        # biometric_data/digital_estate
    region: str
    # 17 numeric fields (0.0–1.0)
    identity_integrity_score: float           # 0-1, 1=fully intact
    brand_impersonation_risk: float           # 0-1, higher=worse
    ip_ownership_clarity: float               # 0-1, 1=crystal clear
    data_residency_compliance: float          # 0-1, 1=fully compliant
    platform_dependency_risk: float           # 0-1, higher=worse
    algorithmic_attribution_score: float      # 0-1, 1=fully attributed
    proprietary_data_exposure_risk: float     # 0-1, higher=worse
    digital_footprint_control: float          # 0-1, 1=full control
    access_credential_security: float         # 0-1, 1=fully secure
    content_authenticity_score: float         # 0-1, 1=fully authentic
    deepfake_vulnerability_index: float       # 0-1, higher=worse
    namespace_ownership_score: float          # 0-1, 1=full ownership
    cross_border_jurisdiction_risk: float     # 0-1, higher=worse
    succession_plan_coverage: float           # 0-1, 1=fully covered
    legal_protection_strength: float          # 0-1, 1=strong protection
    monitoring_coverage_score: float          # 0-1, 1=full monitoring
    incident_response_readiness: float        # 0-1, 1=fully ready


@dataclass
class SovereigntyResult:
    asset_id: str
    asset_domain: str
    region: str
    sovereignty_risk: str
    sovereignty_pattern: str
    sovereignty_severity: str
    recommended_actions: List[str]
    identity_score: float
    ownership_score: float
    protection_score: float
    resilience_score: float
    sovereignty_composite: float
    estimated_sovereignty_breach_index: float
    sovereignty_signal: str
    is_legally_actionable: bool

    def to_dict(self) -> Dict:
        return {
            "asset_id":                              self.asset_id,
            "asset_domain":                          self.asset_domain,
            "region":                                self.region,
            "sovereignty_risk":                      self.sovereignty_risk,
            "sovereignty_pattern":                   self.sovereignty_pattern,
            "sovereignty_severity":                  self.sovereignty_severity,
            "recommended_actions":                   self.recommended_actions,
            "identity_score":                        self.identity_score,
            "ownership_score":                       self.ownership_score,
            "protection_score":                      self.protection_score,
            "resilience_score":                      self.resilience_score,
            "sovereignty_composite":                 self.sovereignty_composite,
            "estimated_sovereignty_breach_index":    self.estimated_sovereignty_breach_index,
            "sovereignty_signal":                    self.sovereignty_signal,
            "is_legally_actionable":                 self.is_legally_actionable,
        }


class DigitalSovereigntyEngine:
    def __init__(self) -> None:
        self._results: List[SovereigntyResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100, capped)                                          #
    # ------------------------------------------------------------------ #

    def _identity_score(self, i: SovereigntyInput) -> float:
        # brand_impersonation_risk (inverted), deepfake_vulnerability_index (inverted),
        # identity_integrity_score
        raw = (
            (1.0 - i.brand_impersonation_risk) * 100 / 3
            + (1.0 - i.deepfake_vulnerability_index) * 100 / 3
            + i.identity_integrity_score * 100 / 3
        )
        # Invert: high raw = sovereign (low risk), so for the composite (higher=worse)
        # we want a score where higher means MORE threatened.
        # identity dimension threat = inverted identity quality
        return min(round((1.0 - (raw / 100)) * 100, 2), 100.0)

    def _ownership_score(self, i: SovereigntyInput) -> float:
        # ip_ownership_clarity, algorithmic_attribution_score, namespace_ownership_score
        # Higher raw = better ownership; for composite (higher=worse) invert
        raw = (
            i.ip_ownership_clarity * 100 / 3
            + i.algorithmic_attribution_score * 100 / 3
            + i.namespace_ownership_score * 100 / 3
        )
        return min(round((1.0 - (raw / 100)) * 100, 2), 100.0)

    def _protection_score(self, i: SovereigntyInput) -> float:
        # proprietary_data_exposure_risk (inverted-inverted=direct),
        # platform_dependency_risk (inverted-inverted=direct),
        # legal_protection_strength (inverted)
        raw = (
            i.proprietary_data_exposure_risk * 100 / 3
            + i.platform_dependency_risk * 100 / 3
            + (1.0 - i.legal_protection_strength) * 100 / 3
        )
        return min(round(raw, 2), 100.0)

    def _resilience_score(self, i: SovereigntyInput) -> float:
        # incident_response_readiness, monitoring_coverage_score,
        # access_credential_security — all higher=better, so invert for risk score
        raw = (
            (1.0 - i.incident_response_readiness) * 100 / 3
            + (1.0 - i.monitoring_coverage_score) * 100 / 3
            + (1.0 - i.access_credential_security) * 100 / 3
        )
        return min(round(raw, 2), 100.0)

    def _composite(self, id_s: float, own_s: float, prot_s: float, res_s: float) -> float:
        return min(round(id_s * 0.30 + own_s * 0.25 + prot_s * 0.25 + res_s * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> SovereigntyRisk:
        if c >= 60: return SovereigntyRisk.critical
        if c >= 40: return SovereigntyRisk.high
        if c >= 20: return SovereigntyRisk.moderate
        return SovereigntyRisk.low

    def _severity(self, c: float) -> SovereigntySeverity:
        if c >= 60: return SovereigntySeverity.compromised
        if c >= 40: return SovereigntySeverity.threatened
        if c >= 20: return SovereigntySeverity.monitored
        return SovereigntySeverity.sovereign

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: SovereigntyInput) -> SovereigntyPattern:
        if i.brand_impersonation_risk >= 0.65 or i.identity_integrity_score <= 0.35:
            return SovereigntyPattern.identity_theft
        if i.ip_ownership_clarity <= 0.35 or i.algorithmic_attribution_score <= 0.35:
            return SovereigntyPattern.ip_expropriation
        if i.platform_dependency_risk >= 0.65:
            return SovereigntyPattern.platform_capture
        if i.proprietary_data_exposure_risk >= 0.60 or i.data_residency_compliance <= 0.40:
            return SovereigntyPattern.data_leakage
        if i.deepfake_vulnerability_index >= 0.60:
            return SovereigntyPattern.deepfake_attack
        return SovereigntyPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _actions(self, risk: SovereigntyRisk, pat: SovereigntyPattern) -> List[str]:
        if risk == SovereigntyRisk.critical:
            return [
                SovereigntyAction.emergency_identity_lock.value,
                SovereigntyAction.legal_injunction.value,
            ]
        if risk == SovereigntyRisk.high:
            return [
                SovereigntyAction.ip_enforcement.value,
                SovereigntyAction.platform_exit_strategy.value,
            ]
        if risk == SovereigntyRisk.moderate:
            return [SovereigntyAction.sovereignty_monitoring.value]
        return [SovereigntyAction.no_action.value]

    # ------------------------------------------------------------------ #
    #  Breach index & signal                                               #
    # ------------------------------------------------------------------ #

    def _breach_index(self, i: SovereigntyInput, comp: float) -> float:
        return round(
            min(
                comp / 100 * (i.brand_impersonation_risk + i.proprietary_data_exposure_risk) / 2 * 10,
                10.0,
            ),
            2,
        )

    def _signal(self, i: SovereigntyInput, pat: SovereigntyPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Souveraineté numérique maîtrisée — identité protégée, "
                "propriété intellectuelle sécurisée, données souveraines"
            )
        labels: Dict[SovereigntyPattern, str] = {
            SovereigntyPattern.identity_theft:   "Vol d'identité numérique",
            SovereigntyPattern.ip_expropriation: "Expropriation propriété intellectuelle",
            SovereigntyPattern.platform_capture: "Capture par la plateforme",
            SovereigntyPattern.data_leakage:     "Fuite de données propriétaires",
            SovereigntyPattern.deepfake_attack:  "Attaque deepfake détectée",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — impersonation {i.brand_impersonation_risk:.2f}"
            f" — clarté IP {i.ip_ownership_clarity:.2f}"
            f" — exposition données {i.proprietary_data_exposure_risk:.2f}"
            f" — composite {comp:.0f}"
        )

    def _is_legally_actionable(self, risk: SovereigntyRisk) -> bool:
        return risk in (SovereigntyRisk.critical, SovereigntyRisk.high)

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: SovereigntyInput) -> SovereigntyResult:
        id_s   = self._identity_score(i)
        own_s  = self._ownership_score(i)
        prot_s = self._protection_score(i)
        res_s  = self._resilience_score(i)
        comp   = self._composite(id_s, own_s, prot_s, res_s)
        risk   = self._risk(comp)
        sev    = self._severity(comp)
        pat    = self._pattern(i)
        acts   = self._actions(risk, pat)
        result = SovereigntyResult(
            asset_id=i.asset_id,
            asset_domain=i.asset_domain,
            region=i.region,
            sovereignty_risk=risk.value,
            sovereignty_pattern=pat.value,
            sovereignty_severity=sev.value,
            recommended_actions=acts,
            identity_score=id_s,
            ownership_score=own_s,
            protection_score=prot_s,
            resilience_score=res_s,
            sovereignty_composite=comp,
            estimated_sovereignty_breach_index=self._breach_index(i, comp),
            sovereignty_signal=self._signal(i, pat, comp),
            is_legally_actionable=self._is_legally_actionable(risk),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[SovereigntyInput]) -> List[SovereigntyResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_sovereignty_composite": 0.0,
                "compromised_count": 0,
                "legal_action_count": 0,
                "avg_identity_score": 0.0,
                "avg_ownership_score": 0.0,
                "avg_protection_score": 0.0,
                "avg_resilience_score": 0.0,
                "avg_estimated_sovereignty_breach_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tid = town = tprot = tres = tcomp = tbreach = 0.0
        compromised_count = legal_count = 0
        for r in self._results:
            rc[r.sovereignty_risk]     = rc.get(r.sovereignty_risk, 0)     + 1
            pc[r.sovereignty_pattern]  = pc.get(r.sovereignty_pattern, 0)  + 1
            sc[r.sovereignty_severity] = sc.get(r.sovereignty_severity, 0) + 1
            for a in r.recommended_actions:
                ac[a] = ac.get(a, 0) + 1
            tid    += r.identity_score
            town   += r.ownership_score
            tprot  += r.protection_score
            tres   += r.resilience_score
            tcomp  += r.sovereignty_composite
            tbreach += r.estimated_sovereignty_breach_index
            if r.sovereignty_severity == SovereigntySeverity.compromised.value:
                compromised_count += 1
            if r.is_legally_actionable:
                legal_count += 1
        return {
            "total":                                  n,
            "risk_counts":                            rc,
            "pattern_counts":                         pc,
            "severity_counts":                        sc,
            "action_counts":                          ac,
            "avg_sovereignty_composite":              round(tcomp / n, 1),
            "compromised_count":                      compromised_count,
            "legal_action_count":                     legal_count,
            "avg_identity_score":                     round(tid / n, 1),
            "avg_ownership_score":                    round(town / n, 1),
            "avg_protection_score":                   round(tprot / n, 1),
            "avg_resilience_score":                   round(tres / n, 1),
            "avg_estimated_sovereignty_breach_index": round(tbreach / n, 2),
        }
