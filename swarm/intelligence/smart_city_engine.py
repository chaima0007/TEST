"""
Module 388 — Smart City & Urban Surveillance Intelligence Engine
Monitors smart city threats — surveillance infrastructures, authoritarian
export patterns, IoT cyber vulnerabilities, predictive policing bias,
and urban data sovereignty loss across global cities.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SmartCityInput:
    entity_id: str
    city_type: str
    region: str
    # 17 float fields 0-1
    camera_surveillance_density: float
    facial_recognition_deployment: float
    movement_tracking_intensity: float
    predictive_policing_bias: float
    IoT_data_vulnerability: float
    smart_grid_cyber_exposure: float
    digital_twin_city_control: float
    behavioral_nudging_scale: float
    private_tech_city_capture: float
    citizen_data_monetization: float
    democratic_accountability_gap: float
    algorithmic_urban_discrimination: float
    fiveG_surveillance_integration: float
    CCP_smart_city_export: float
    dissent_suppression_capacity: float
    urban_data_sovereignty_loss: float
    smart_home_surveillance_integration: float


@dataclass
class SmartCityResult:
    entity_id: str
    city_type: str
    region: str
    surveillance_score: float
    control_score: float
    vulnerability_score: float
    sovereignty_score: float
    composite_score: float
    risk_level: str
    total_surveillance_city: bool
    authoritarian_smart_city_export: bool
    private_tech_city_capture_pattern: bool
    predictive_policing_dystopia: bool
    IoT_city_cyber_catastrophe: bool
    patterns_detected: List[str]

    def to_dict(self) -> Dict:
        return {
            "entity_id":                         self.entity_id,
            "city_type":                         self.city_type,
            "region":                            self.region,
            "surveillance_score":                self.surveillance_score,
            "control_score":                     self.control_score,
            "vulnerability_score":               self.vulnerability_score,
            "sovereignty_score":                 self.sovereignty_score,
            "composite_score":                   self.composite_score,
            "risk_level":                        self.risk_level,
            "total_surveillance_city":           self.total_surveillance_city,
            "authoritarian_smart_city_export":   self.authoritarian_smart_city_export,
            "private_tech_city_capture_pattern": self.private_tech_city_capture_pattern,
            "predictive_policing_dystopia":      self.predictive_policing_dystopia,
            "IoT_city_cyber_catastrophe":        self.IoT_city_cyber_catastrophe,
            "patterns_detected":                 self.patterns_detected,
        }


class SmartCityEngine:
    def __init__(self) -> None:
        self._results: List[SmartCityResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _surveillance_score(self, i: SmartCityInput) -> float:
        s = (
            i.camera_surveillance_density
            + i.facial_recognition_deployment
            + i.movement_tracking_intensity
            + i.fiveG_surveillance_integration
            + i.smart_home_surveillance_integration
        ) / 5 * 100
        return min(round(s, 2), 100.0)

    def _control_score(self, i: SmartCityInput) -> float:
        s = (
            i.predictive_policing_bias
            + i.digital_twin_city_control
            + i.behavioral_nudging_scale
            + i.CCP_smart_city_export
            + i.dissent_suppression_capacity
        ) / 5 * 100
        return min(round(s, 2), 100.0)

    def _vulnerability_score(self, i: SmartCityInput) -> float:
        s = (
            i.IoT_data_vulnerability
            + i.smart_grid_cyber_exposure
            + i.algorithmic_urban_discrimination
        ) / 3 * 100
        return min(round(s, 2), 100.0)

    def _sovereignty_score(self, i: SmartCityInput) -> float:
        s = (
            i.private_tech_city_capture
            + i.citizen_data_monetization
            + i.democratic_accountability_gap
            + i.urban_data_sovereignty_loss
        ) / 4 * 100
        return min(round(s, 2), 100.0)

    def _composite(self, surv: float, ctrl: float, vuln: float, sov: float) -> float:
        return min(round(surv * 0.30 + ctrl * 0.25 + vuln * 0.25 + sov * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity / action / signal                                   #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> str:
        if c >= 60: return "critical"
        if c >= 40: return "high"
        if c >= 20: return "moderate"
        return "low"

    def _severity(self, c: float) -> str:
        if c >= 60: return "surveillance_urbaine_systémique"
        if c >= 40: return "crise_contrôle_ville_intelligente_majeure"
        if c >= 20: return "érosion_souveraineté_urbaine"
        return "surveillance_urbaine_limitée"

    def _action(self, c: float) -> str:
        if c >= 60: return "intervention_démocratie_numérique_urbaine_urgente"
        if c >= 40: return "stratégie_souveraineté_données_ville_accélérée"
        if c >= 20: return "renforcement_gouvernance_données_urbaines"
        return "veille_ville_intelligente_continue"

    def _signal(self, c: float) -> str:
        if c >= 60:
            return "🔴 Surveillance urbaine systémique — souveraineté citoyenne compromise"
        if c >= 40:
            return "🟠 Crise contrôle ville intelligente majeure détectée"
        if c >= 20:
            return "🟡 Érosion souveraineté données urbaines active"
        return "🟢 Surveillance urbaine relativement contenue"

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _patterns(self, i: SmartCityInput) -> Dict[str, bool]:
        return {
            "total_surveillance_city": (
                i.camera_surveillance_density > 0.85
                and i.facial_recognition_deployment > 0.80
            ),
            "authoritarian_smart_city_export": (
                i.CCP_smart_city_export > 0.85
                and i.dissent_suppression_capacity > 0.80
            ),
            "private_tech_city_capture_pattern": (
                i.private_tech_city_capture > 0.85
                and i.citizen_data_monetization > 0.80
            ),
            "predictive_policing_dystopia": (
                i.predictive_policing_bias > 0.80
                and i.algorithmic_urban_discrimination > 0.75
            ),
            "IoT_city_cyber_catastrophe": (
                i.IoT_data_vulnerability > 0.80
                and i.smart_grid_cyber_exposure > 0.75
            ),
        }

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: SmartCityInput) -> SmartCityResult:
        surv = self._surveillance_score(i)
        ctrl = self._control_score(i)
        vuln = self._vulnerability_score(i)
        sov  = self._sovereignty_score(i)
        comp = self._composite(surv, ctrl, vuln, sov)
        risk = self._risk(comp)
        pats = self._patterns(i)
        detected = [name for name, flag in pats.items() if flag]
        result = SmartCityResult(
            entity_id=i.entity_id,
            city_type=i.city_type,
            region=i.region,
            surveillance_score=surv,
            control_score=ctrl,
            vulnerability_score=vuln,
            sovereignty_score=sov,
            composite_score=comp,
            risk_level=risk,
            total_surveillance_city=pats["total_surveillance_city"],
            authoritarian_smart_city_export=pats["authoritarian_smart_city_export"],
            private_tech_city_capture_pattern=pats["private_tech_city_capture_pattern"],
            predictive_policing_dystopia=pats["predictive_policing_dystopia"],
            IoT_city_cyber_catastrophe=pats["IoT_city_cyber_catastrophe"],
            patterns_detected=detected,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[SmartCityInput]) -> List[SmartCityResult]:
        return [self.assess(i) for i in inputs]

    def reset(self) -> None:
        self._results.clear()

    def summary(self, results: List[Dict] = None) -> Dict:
        data = results if results is not None else [r.to_dict() for r in self._results]
        if not data:
            return {
                "module_id":                                   388,
                "module_name":                                 "Smart City & Urban Surveillance Intelligence Engine",
                "total":                                       0,
                "critical":                                    0,
                "high":                                        0,
                "moderate":                                    0,
                "low":                                         0,
                "avg_composite":                               0.0,
                "distributions":                               {},
                "avg_estimated_smart_city_surveillance_index": 0.0,
                "avg_surveillance_score":                      0.0,
                "avg_control_score":                           0.0,
                "avg_vulnerability_score":                     0.0,
            }
        n = len(data)
        dist: Dict[str, int] = {}
        total_comp = 0.0
        total_surv = 0.0
        total_ctrl = 0.0
        total_vuln = 0.0
        critical = high = moderate = low = 0
        for r in data:
            rl = r["risk_level"]
            dist[rl] = dist.get(rl, 0) + 1
            total_comp += r["composite_score"]
            total_surv += r["surveillance_score"]
            total_ctrl += r["control_score"]
            total_vuln += r["vulnerability_score"]
            if rl == "critical":   critical += 1
            elif rl == "high":     high     += 1
            elif rl == "moderate": moderate += 1
            else:                  low      += 1
        avg_composite = round(total_comp / n, 2)
        return {
            "module_id":                                   388,
            "module_name":                                 "Smart City & Urban Surveillance Intelligence Engine",
            "total":                                       n,
            "critical":                                    critical,
            "high":                                        high,
            "moderate":                                    moderate,
            "low":                                         low,
            "avg_composite":                               avg_composite,
            "distributions":                               dist,
            "avg_estimated_smart_city_surveillance_index": round(avg_composite / 100 * 10, 2),
            "avg_surveillance_score":                      round(total_surv / n, 2),
            "avg_control_score":                           round(total_ctrl / n, 2),
            "avg_vulnerability_score":                     round(total_vuln / n, 2),
        }
