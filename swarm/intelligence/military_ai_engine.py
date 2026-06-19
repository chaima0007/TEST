"""
Module 337 — Military AI & Autonomous Weapons Intelligence Engine
Monitors military AI deployments for autonomous weapon proliferation,
escalation risk, governance collapse, and lethal autonomy thresholds.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MilitaryAIInput:
    entity_id: str
    military_domain: str
    region: str
    # 17 float fields 0-1
    autonomous_lethal_weapon_deployment: float
    AI_command_authority_level: float
    algorithmic_targeting_autonomy: float
    human_control_erosion_index: float
    AI_arms_race_intensity: float
    drone_swarm_capability: float
    cyber_warfare_AI_integration: float
    AI_escalation_risk: float
    military_AI_regulatory_vacuum: float
    predictive_warfare_capability: float
    AI_nuclear_integration_risk: float
    defense_AI_monopoly_risk: float
    lethal_autonomous_weapon_proliferation: float
    military_AI_accountability_gap: float
    AI_military_capability_gap: float
    AI_strategic_surprise_risk: float
    autonomous_warfare_threshold_lowering: float


@dataclass
class MilitaryAIResult:
    entity_id: str
    military_domain: str
    region: str
    autonomy_score: float
    escalation_score: float
    proliferation_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    military_ai_pattern: str
    severity: str
    recommended_action: str
    signal: str
    autonomous_lethal_weapon_deployment: float
    AI_nuclear_integration_risk: float

    def to_dict(self) -> Dict:
        return {
            "entity_id":                              self.entity_id,
            "military_domain":                        self.military_domain,
            "region":                                 self.region,
            "autonomy_score":                         self.autonomy_score,
            "escalation_score":                       self.escalation_score,
            "proliferation_score":                    self.proliferation_score,
            "governance_score":                       self.governance_score,
            "composite_score":                        self.composite_score,
            "risk_level":                             self.risk_level,
            "military_ai_pattern":                    self.military_ai_pattern,
            "severity":                               self.severity,
            "recommended_action":                     self.recommended_action,
            "signal":                                 self.signal,
            "autonomous_lethal_weapon_deployment":    self.autonomous_lethal_weapon_deployment,
            "AI_nuclear_integration_risk":            self.AI_nuclear_integration_risk,
        }


class MilitaryAIEngine:
    def __init__(self) -> None:
        self._results: List[MilitaryAIResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _autonomy_score(self, i: MilitaryAIInput) -> float:
        s = (
            i.autonomous_lethal_weapon_deployment * 0.40
            + i.algorithmic_targeting_autonomy * 0.35
            + i.AI_command_authority_level * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _escalation_score(self, i: MilitaryAIInput) -> float:
        s = (
            i.AI_escalation_risk * 0.40
            + i.AI_strategic_surprise_risk * 0.35
            + i.autonomous_warfare_threshold_lowering * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _proliferation_score(self, i: MilitaryAIInput) -> float:
        s = (
            i.lethal_autonomous_weapon_proliferation * 0.40
            + i.AI_arms_race_intensity * 0.35
            + i.drone_swarm_capability * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _governance_score(self, i: MilitaryAIInput) -> float:
        s = (
            i.military_AI_regulatory_vacuum * 0.40
            + i.military_AI_accountability_gap * 0.35
            + i.AI_nuclear_integration_risk * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _composite(self, aut: float, esc: float, pro: float, gov: float) -> float:
        return min(round(aut * 0.30 + esc * 0.25 + pro * 0.25 + gov * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity / action / signal                                   #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> str:
        if c >= 60: return "critical"
        if c >= 40: return "high"
        if c >= 20: return "moderate"
        return "low"

    def _severity(self, c: float) -> str:
        if c >= 60: return "guerre_autonome_systémique"
        if c >= 40: return "escalade_IA_militaire_majeure"
        if c >= 20: return "militarisation_IA_active"
        return "IA_militaire_contenue"

    def _action(self, c: float) -> str:
        if c >= 60: return "interdiction_armes_autonomes_urgente"
        if c >= 40: return "régulation_IA_militaire_stricte"
        if c >= 20: return "renforcement_contrôle_humain_IA"
        return "veille_IA_militaire_continue"

    def _signal(self, c: float) -> str:
        if c >= 60:
            return "🔴 Guerre autonome systémique — IA létale hors contrôle humain"
        if c >= 40:
            return "🟠 Escalade IA militaire majeure détectée"
        if c >= 20:
            return "🟡 Militarisation IA active — surveillance requise"
        return "🟢 IA militaire sous contrôle relatif"

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: MilitaryAIInput) -> str:
        if i.autonomous_lethal_weapon_deployment >= 0.70 and i.human_control_erosion_index >= 0.65:
            return "autonomous_kill_chain"
        if i.AI_escalation_risk >= 0.70 and i.AI_strategic_surprise_risk >= 0.65:
            return "AI_escalation_cascade"
        if i.lethal_autonomous_weapon_proliferation >= 0.70 and i.AI_arms_race_intensity >= 0.65:
            return "lethal_AI_proliferation"
        if i.AI_nuclear_integration_risk >= 0.70 and i.algorithmic_targeting_autonomy >= 0.65:
            return "nuclear_AI_entanglement"
        if i.military_AI_regulatory_vacuum >= 0.70 and i.military_AI_accountability_gap >= 0.65:
            return "governance_collapse"
        return "none"

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: MilitaryAIInput) -> MilitaryAIResult:
        aut  = self._autonomy_score(i)
        esc  = self._escalation_score(i)
        pro  = self._proliferation_score(i)
        gov  = self._governance_score(i)
        comp = self._composite(aut, esc, pro, gov)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        act  = self._action(comp)
        pat  = self._pattern(i)
        sig  = self._signal(comp)
        result = MilitaryAIResult(
            entity_id=i.entity_id,
            military_domain=i.military_domain,
            region=i.region,
            autonomy_score=aut,
            escalation_score=esc,
            proliferation_score=pro,
            governance_score=gov,
            composite_score=comp,
            risk_level=risk,
            military_ai_pattern=pat,
            severity=sev,
            recommended_action=act,
            signal=sig,
            autonomous_lethal_weapon_deployment=i.autonomous_lethal_weapon_deployment,
            AI_nuclear_integration_risk=i.AI_nuclear_integration_risk,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[MilitaryAIInput]) -> List[MilitaryAIResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "module_id":                       337,
                "module_name":                     "Military AI & Autonomous Weapons Intelligence Engine",
                "total_entities":                  0,
                "critical_count":                  0,
                "high_count":                      0,
                "moderate_count":                  0,
                "low_count":                       0,
                "avg_composite":                   0.0,
                "pattern_distribution":            {},
                "risk_distribution":               {},
                "severity_distribution":           {},
                "action_distribution":             {},
                "avg_estimated_military_ai_index": 0.0,
            }
        n = len(self._results)
        pat_dist: Dict[str, int]  = {}
        risk_dist: Dict[str, int] = {}
        sev_dist: Dict[str, int]  = {}
        act_dist: Dict[str, int]  = {}
        total_comp = 0.0
        critical = high = moderate = low = 0
        for r in self._results:
            pat_dist[r.military_ai_pattern]  = pat_dist.get(r.military_ai_pattern, 0) + 1
            risk_dist[r.risk_level]          = risk_dist.get(r.risk_level, 0) + 1
            sev_dist[r.severity]             = sev_dist.get(r.severity, 0) + 1
            act_dist[r.recommended_action]   = act_dist.get(r.recommended_action, 0) + 1
            total_comp += r.composite_score
            if r.risk_level == "critical":   critical  += 1
            elif r.risk_level == "high":     high      += 1
            elif r.risk_level == "moderate": moderate  += 1
            else:                            low       += 1
        avg_composite = round(total_comp / n, 1)
        return {
            "module_id":                       337,
            "module_name":                     "Military AI & Autonomous Weapons Intelligence Engine",
            "total_entities":                  n,
            "critical_count":                  critical,
            "high_count":                      high,
            "moderate_count":                  moderate,
            "low_count":                       low,
            "avg_composite":                   avg_composite,
            "pattern_distribution":            pat_dist,
            "risk_distribution":               risk_dist,
            "severity_distribution":           sev_dist,
            "action_distribution":             act_dist,
            "avg_estimated_military_ai_index": round(avg_composite / 100 * 10, 2),
        }
