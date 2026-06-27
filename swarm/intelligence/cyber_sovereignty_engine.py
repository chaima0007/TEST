"""
Module 357 — Cyber Sovereignty & Internet Fragmentation Intelligence Engine
Monitors cyber sovereignty threats — internet splinternet progression,
DNS sovereignty erosion, undersea cable geopolitical vulnerability,
cloud infrastructure foreign dependency, BGP hijacking exposure,
cyber weapons proliferation, and digital sovereignty deficits.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class CyberSovereigntyInput:
    entity_id: str
    cyber_domain: str
    region: str
    # 17 float fields 0-1
    internet_splinternet_progression: float
    national_internet_firewall_density: float
    DNS_sovereignty_erosion: float
    undersea_cable_geopolitical_vulnerability: float
    cloud_infrastructure_foreign_dependency: float
    data_localization_fragmentation: float
    internet_shutdown_weaponization_frequency: float
    BGP_hijacking_exposure: float
    cyber_deterrence_capability_gap: float
    critical_infrastructure_cyber_exposure: float
    zero_day_stockpiling_arms_race: float
    AI_enhanced_cyber_attack_capability: float
    supply_chain_software_poisoning_risk: float
    cyber_mercenary_proliferation: float
    internet_governance_capture: float
    election_infrastructure_cyber_risk: float
    digital_sovereignty_deficit_index: float


@dataclass
class CyberSovereigntyResult:
    entity_id: str
    cyber_domain: str
    region: str
    fragmentation_score: float
    infrastructure_score: float
    attack_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    cyber_pattern: str
    severity: str
    recommended_action: str
    signal: str
    internet_splinternet_progression: float
    digital_sovereignty_deficit_index: float

    def to_dict(self) -> Dict:
        return {
            "entity_id":                           self.entity_id,
            "cyber_domain":                        self.cyber_domain,
            "region":                              self.region,
            "fragmentation_score":                 self.fragmentation_score,
            "infrastructure_score":                self.infrastructure_score,
            "attack_score":                        self.attack_score,
            "governance_score":                    self.governance_score,
            "composite_score":                     self.composite_score,
            "risk_level":                          self.risk_level,
            "cyber_pattern":                       self.cyber_pattern,
            "severity":                            self.severity,
            "recommended_action":                  self.recommended_action,
            "signal":                              self.signal,
            "internet_splinternet_progression":    self.internet_splinternet_progression,
            "digital_sovereignty_deficit_index":   self.digital_sovereignty_deficit_index,
        }


class CyberSovereigntyEngine:
    def __init__(self) -> None:
        self._results: List[CyberSovereigntyResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _fragmentation_score(self, i: CyberSovereigntyInput) -> float:
        s = (
            i.internet_splinternet_progression * 0.40
            + i.national_internet_firewall_density * 0.35
            + i.data_localization_fragmentation * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _infrastructure_score(self, i: CyberSovereigntyInput) -> float:
        s = (
            i.undersea_cable_geopolitical_vulnerability * 0.40
            + i.cloud_infrastructure_foreign_dependency * 0.35
            + i.critical_infrastructure_cyber_exposure * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _attack_score(self, i: CyberSovereigntyInput) -> float:
        s = (
            i.AI_enhanced_cyber_attack_capability * 0.40
            + i.zero_day_stockpiling_arms_race * 0.35
            + i.supply_chain_software_poisoning_risk * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _governance_score(self, i: CyberSovereigntyInput) -> float:
        s = (
            i.digital_sovereignty_deficit_index * 0.40
            + i.internet_governance_capture * 0.35
            + i.cyber_mercenary_proliferation * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _composite(self, frag: float, infra: float, atk: float, gov: float) -> float:
        return min(round(frag * 0.30 + infra * 0.25 + atk * 0.25 + gov * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity / action / signal                                   #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> str:
        if c >= 60: return "critical"
        if c >= 40: return "high"
        if c >= 20: return "moderate"
        return "low"

    def _severity(self, c: float) -> str:
        if c >= 60: return "fragmentation_internet_systémique"
        if c >= 40: return "crise_souveraineté_cyber_majeure"
        if c >= 20: return "erosion_souveraineté_numérique"
        return "cyber_souveraineté_relative"

    def _action(self, c: float) -> str:
        if c >= 60: return "intervention_souveraineté_cyber_urgente"
        if c >= 40: return "stratégie_cyber_souveraineté_accélérée"
        if c >= 20: return "renforcement_infrastructure_cyber_nationale"
        return "veille_souveraineté_cyber_continue"

    def _signal(self, c: float) -> str:
        if c >= 60:
            return "🔴 Fragmentation internet systémique — souveraineté numérique compromise"
        if c >= 40:
            return "🟠 Crise souveraineté cyber majeure détectée"
        if c >= 20:
            return "🟡 Érosion souveraineté numérique active"
        return "🟢 Cyber souveraineté relativement maintenue"

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: CyberSovereigntyInput) -> str:
        if i.internet_splinternet_progression >= 0.70 and i.DNS_sovereignty_erosion >= 0.65:
            return "splinternet_collapse"
        if i.undersea_cable_geopolitical_vulnerability >= 0.70 and i.cloud_infrastructure_foreign_dependency >= 0.65:
            return "undersea_cable_crisis"
        if i.zero_day_stockpiling_arms_race >= 0.70 and i.AI_enhanced_cyber_attack_capability >= 0.65:
            return "cyber_weapons_proliferation"
        if i.internet_shutdown_weaponization_frequency >= 0.70 and i.national_internet_firewall_density >= 0.65:
            return "internet_shutdown_authoritarianism"
        if i.supply_chain_software_poisoning_risk >= 0.70 and i.BGP_hijacking_exposure >= 0.65:
            return "supply_chain_cyber_poisoning"
        return "none"

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: CyberSovereigntyInput) -> CyberSovereigntyResult:
        frag = self._fragmentation_score(i)
        infra = self._infrastructure_score(i)
        atk  = self._attack_score(i)
        gov  = self._governance_score(i)
        comp = self._composite(frag, infra, atk, gov)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        act  = self._action(comp)
        pat  = self._pattern(i)
        sig  = self._signal(comp)
        result = CyberSovereigntyResult(
            entity_id=i.entity_id,
            cyber_domain=i.cyber_domain,
            region=i.region,
            fragmentation_score=frag,
            infrastructure_score=infra,
            attack_score=atk,
            governance_score=gov,
            composite_score=comp,
            risk_level=risk,
            cyber_pattern=pat,
            severity=sev,
            recommended_action=act,
            signal=sig,
            internet_splinternet_progression=i.internet_splinternet_progression,
            digital_sovereignty_deficit_index=i.digital_sovereignty_deficit_index,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[CyberSovereigntyInput]) -> List[CyberSovereigntyResult]:
        return [self.assess(i) for i in inputs]

    def summary(self, results: List[Dict] = None) -> Dict:
        data = results if results is not None else [r.to_dict() for r in self._results]
        if not data:
            return {
                "module_id":                             357,
                "module_name":                           "Cyber Sovereignty & Internet Fragmentation Intelligence Engine",
                "total_entities":                        0,
                "critical_count":                        0,
                "high_count":                            0,
                "moderate_count":                        0,
                "low_count":                             0,
                "avg_composite":                         0.0,
                "pattern_distribution":                  {},
                "risk_distribution":                     {},
                "severity_distribution":                 {},
                "action_distribution":                   {},
                "avg_estimated_cyber_sovereignty_index": 0.0,
            }
        n = len(data)
        pat_dist: Dict[str, int]  = {}
        risk_dist: Dict[str, int] = {}
        sev_dist: Dict[str, int]  = {}
        act_dist: Dict[str, int]  = {}
        total_comp = 0.0
        critical = high = moderate = low = 0
        for r in data:
            pat_dist[r["cyber_pattern"]]       = pat_dist.get(r["cyber_pattern"], 0) + 1
            risk_dist[r["risk_level"]]         = risk_dist.get(r["risk_level"], 0) + 1
            sev_dist[r["severity"]]            = sev_dist.get(r["severity"], 0) + 1
            act_dist[r["recommended_action"]]  = act_dist.get(r["recommended_action"], 0) + 1
            total_comp += r["composite_score"]
            if r["risk_level"] == "critical":        critical  += 1
            elif r["risk_level"] == "high":          high      += 1
            elif r["risk_level"] == "moderate":      moderate  += 1
            else:                                    low       += 1
        avg_composite = round(total_comp / n, 1)
        return {
            "module_id":                             357,
            "module_name":                           "Cyber Sovereignty & Internet Fragmentation Intelligence Engine",
            "total_entities":                        n,
            "critical_count":                        critical,
            "high_count":                            high,
            "moderate_count":                        moderate,
            "low_count":                             low,
            "avg_composite":                         avg_composite,
            "pattern_distribution":                  pat_dist,
            "risk_distribution":                     risk_dist,
            "severity_distribution":                 sev_dist,
            "action_distribution":                   act_dist,
            "avg_estimated_cyber_sovereignty_index": round(avg_composite / 100 * 10, 2),
        }
