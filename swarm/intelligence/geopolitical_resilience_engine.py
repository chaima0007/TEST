"""
Module 258 — Geopolitical Resilience & Diplomatic Risk Assessment Engine
Monitors geopolitical exposure for business operations — sanctions risk,
diplomatic relationship quality, trade war exposure, regulatory sovereignty
shifts, political stability, and cross-border operational continuity.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class GeopoliticalRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class GeopoliticalPattern(str, Enum):
    none                  = "none"
    sanctions_cascade     = "sanctions_cascade"
    diplomatic_rupture    = "diplomatic_rupture"
    regulatory_decoupling = "regulatory_decoupling"
    conflict_spillover    = "conflict_spillover"
    sovereignty_erosion   = "sovereignty_erosion"


class GeopoliticalSeverity(str, Enum):
    stable   = "stable"
    cautious = "cautious"
    tense    = "tense"
    hostile  = "hostile"


class GeopoliticalAction(str, Enum):
    no_action            = "no_action"
    geopolitical_monitoring = "geopolitical_monitoring"
    exposure_reduction   = "exposure_reduction"
    diplomatic_engagement = "diplomatic_engagement"
    market_exit_plan     = "market_exit_plan"
    emergency_hedging    = "emergency_hedging"


class TerritoryType(str, Enum):
    bilateral_trade    = "bilateral_trade"
    multilateral_bloc  = "multilateral_bloc"
    sanctions_zone     = "sanctions_zone"
    emerging_market    = "emerging_market"
    strategic_corridor = "strategic_corridor"
    regulatory_union   = "regulatory_union"
    conflict_adjacent  = "conflict_adjacent"
    diplomatic_hub     = "diplomatic_hub"


@dataclass
class GeopoliticalInput:
    territory_id: str
    territory_type: str
    region: str
    political_stability_score: float        # 0-1
    sanctions_exposure_risk: float          # 0-1, higher=worse
    diplomatic_relationship_quality: float  # 0-1
    trade_agreement_coverage: float         # 0-1
    regulatory_alignment_score: float       # 0-1
    conflict_proximity_index: float         # 0-1, higher=worse
    supply_chain_geopolitical_risk: float   # 0-1, higher=worse
    currency_sovereignty_risk: float        # 0-1, higher=worse
    institutional_quality_score: float      # 0-1
    anti_corruption_score: float            # 0-1
    press_freedom_index: float              # 0-1
    rule_of_law_score: float                # 0-1
    foreign_investment_protection: float    # 0-1
    bilateral_tension_index: float          # 0-1, higher=worse
    technology_decoupling_risk: float       # 0-1, higher=worse
    energy_dependency_risk: float           # 0-1, higher=worse
    democratic_resilience_score: float      # 0-1


@dataclass
class GeopoliticalResult:
    territory_id: str
    territory_type: str
    region: str
    geopolitical_risk: str
    geopolitical_pattern: str
    geopolitical_severity: str
    recommended_action: str
    stability_score: float
    exposure_score: float
    governance_score: float
    sovereignty_score: float
    geopolitical_composite: float
    is_hostile_territory: bool
    requires_exit_plan: bool
    estimated_geopolitical_risk_index: float
    geopolitical_signal: str

    def to_dict(self) -> Dict:
        return {
            "territory_id":                       self.territory_id,
            "territory_type":                     self.territory_type,
            "region":                             self.region,
            "geopolitical_risk":                  self.geopolitical_risk,
            "geopolitical_pattern":               self.geopolitical_pattern,
            "geopolitical_severity":              self.geopolitical_severity,
            "recommended_action":                 self.recommended_action,
            "stability_score":                    self.stability_score,
            "exposure_score":                     self.exposure_score,
            "governance_score":                   self.governance_score,
            "sovereignty_score":                  self.sovereignty_score,
            "geopolitical_composite":             self.geopolitical_composite,
            "is_hostile_territory":               self.is_hostile_territory,
            "requires_exit_plan":                 self.requires_exit_plan,
            "estimated_geopolitical_risk_index":  self.estimated_geopolitical_risk_index,
        }


class GeopoliticalResilienceEngine:
    def __init__(self) -> None:
        self._results: List[GeopoliticalResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100, capped)                                          #
    # ------------------------------------------------------------------ #

    def _stability_score(self, i: GeopoliticalInput) -> float:
        """political_stability_score, rule_of_law_score, democratic_resilience_score — higher raw = worse risk."""
        avg = (i.political_stability_score + i.rule_of_law_score + i.democratic_resilience_score) / 3
        return min(round((1 - avg) * 100, 2), 100.0)

    def _exposure_score(self, i: GeopoliticalInput) -> float:
        """sanctions_exposure_risk (direct), conflict_proximity_index (direct), bilateral_tension_index (direct)."""
        avg = (i.sanctions_exposure_risk + i.conflict_proximity_index + i.bilateral_tension_index) / 3
        return min(round(avg * 100, 2), 100.0)

    def _governance_score(self, i: GeopoliticalInput) -> float:
        """institutional_quality_score, anti_corruption_score, foreign_investment_protection — higher raw = worse risk."""
        avg = (i.institutional_quality_score + i.anti_corruption_score + i.foreign_investment_protection) / 3
        return min(round((1 - avg) * 100, 2), 100.0)

    def _sovereignty_score(self, i: GeopoliticalInput) -> float:
        """technology_decoupling_risk (direct), energy_dependency_risk (direct), regulatory_alignment_score (inverted)."""
        avg = (i.technology_decoupling_risk + i.energy_dependency_risk + (1 - i.regulatory_alignment_score)) / 3
        return min(round(avg * 100, 2), 100.0)

    def _composite(self, stab: float, exp: float, gov: float, sov: float) -> float:
        return min(round(stab * 0.30 + exp * 0.25 + gov * 0.25 + sov * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> GeopoliticalRisk:
        if c >= 60: return GeopoliticalRisk.critical
        if c >= 40: return GeopoliticalRisk.high
        if c >= 20: return GeopoliticalRisk.moderate
        return GeopoliticalRisk.low

    def _severity(self, c: float) -> GeopoliticalSeverity:
        if c >= 60: return GeopoliticalSeverity.hostile
        if c >= 40: return GeopoliticalSeverity.tense
        if c >= 20: return GeopoliticalSeverity.cautious
        return GeopoliticalSeverity.stable

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: GeopoliticalInput) -> GeopoliticalPattern:
        if i.sanctions_exposure_risk >= 0.65:
            return GeopoliticalPattern.sanctions_cascade
        if i.conflict_proximity_index >= 0.60:
            return GeopoliticalPattern.conflict_spillover
        if i.bilateral_tension_index >= 0.65 and i.diplomatic_relationship_quality <= 0.35:
            return GeopoliticalPattern.diplomatic_rupture
        if i.regulatory_alignment_score <= 0.35 and i.technology_decoupling_risk >= 0.55:
            return GeopoliticalPattern.regulatory_decoupling
        if i.energy_dependency_risk >= 0.60 and i.currency_sovereignty_risk >= 0.55:
            return GeopoliticalPattern.sovereignty_erosion
        return GeopoliticalPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: GeopoliticalRisk, pat: GeopoliticalPattern) -> GeopoliticalAction:
        if risk == GeopoliticalRisk.critical:
            if pat == GeopoliticalPattern.sanctions_cascade: return GeopoliticalAction.market_exit_plan
            return GeopoliticalAction.emergency_hedging
        if risk == GeopoliticalRisk.high:
            if pat in (GeopoliticalPattern.diplomatic_rupture, GeopoliticalPattern.conflict_spillover):
                return GeopoliticalAction.diplomatic_engagement
            return GeopoliticalAction.exposure_reduction
        if risk == GeopoliticalRisk.moderate:
            return GeopoliticalAction.geopolitical_monitoring
        return GeopoliticalAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived flags & indices                                             #
    # ------------------------------------------------------------------ #

    def _is_hostile(self, comp: float) -> bool:
        return comp >= 60

    def _requires_exit_plan(self, risk: GeopoliticalRisk, act: GeopoliticalAction) -> bool:
        return act == GeopoliticalAction.market_exit_plan

    def _risk_index(self, i: GeopoliticalInput, comp: float) -> float:
        return round(
            min(comp / 100 * (i.sanctions_exposure_risk + i.conflict_proximity_index) / 2 * 10, 10.0),
            2,
        )

    def _signal(self, i: GeopoliticalInput, pat: GeopoliticalPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Zone géopolitique stable — relations diplomatiques solides, "
                "souveraineté préservée, risques maîtrisés"
            )
        labels = {
            GeopoliticalPattern.sanctions_cascade:     "Cascade de sanctions",
            GeopoliticalPattern.diplomatic_rupture:    "Rupture diplomatique",
            GeopoliticalPattern.regulatory_decoupling: "Découplage réglementaire",
            GeopoliticalPattern.conflict_spillover:    "Débordement conflictuel",
            GeopoliticalPattern.sovereignty_erosion:   "Érosion souveraineté",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — exposition sanctions {i.sanctions_exposure_risk:.2f}"
            f" — stabilité politique {i.political_stability_score:.2f}"
            f" — tension bilatérale {i.bilateral_tension_index:.2f}"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: GeopoliticalInput) -> GeopoliticalResult:
        stab = self._stability_score(i)
        exp  = self._exposure_score(i)
        gov  = self._governance_score(i)
        sov  = self._sovereignty_score(i)
        comp = self._composite(stab, exp, gov, sov)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        hostile = self._is_hostile(comp)
        exit_plan = self._requires_exit_plan(risk, act)
        result = GeopoliticalResult(
            territory_id=i.territory_id,
            territory_type=i.territory_type,
            region=i.region,
            geopolitical_risk=risk.value,
            geopolitical_pattern=pat.value,
            geopolitical_severity=sev.value,
            recommended_action=act.value,
            stability_score=stab,
            exposure_score=exp,
            governance_score=gov,
            sovereignty_score=sov,
            geopolitical_composite=comp,
            is_hostile_territory=hostile,
            requires_exit_plan=exit_plan,
            estimated_geopolitical_risk_index=self._risk_index(i, comp),
            geopolitical_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[GeopoliticalInput]) -> List[GeopoliticalResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_geopolitical_composite": 0.0,
                "hostile_count": 0,
                "exit_plan_count": 0,
                "avg_stability_score": 0.0,
                "avg_exposure_score": 0.0,
                "avg_governance_score": 0.0,
                "avg_sovereignty_score": 0.0,
                "avg_estimated_geopolitical_risk_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tstab = texp = tgov = tsov = tcomp = tridx = 0.0
        hostile_count = exit_plan_count = 0
        for r in self._results:
            rc[r.geopolitical_risk]     = rc.get(r.geopolitical_risk, 0)     + 1
            pc[r.geopolitical_pattern]  = pc.get(r.geopolitical_pattern, 0)  + 1
            sc[r.geopolitical_severity] = sc.get(r.geopolitical_severity, 0) + 1
            ac[r.recommended_action]    = ac.get(r.recommended_action, 0)    + 1
            tstab  += r.stability_score
            texp   += r.exposure_score
            tgov   += r.governance_score
            tsov   += r.sovereignty_score
            tcomp  += r.geopolitical_composite
            tridx  += r.estimated_geopolitical_risk_index
            if r.is_hostile_territory: hostile_count   += 1
            if r.requires_exit_plan:   exit_plan_count += 1
        return {
            "total":                                 n,
            "risk_counts":                           rc,
            "pattern_counts":                        pc,
            "severity_counts":                       sc,
            "action_counts":                         ac,
            "avg_geopolitical_composite":            round(tcomp / n, 1),
            "hostile_count":                         hostile_count,
            "exit_plan_count":                       exit_plan_count,
            "avg_stability_score":                   round(tstab / n, 1),
            "avg_exposure_score":                    round(texp / n, 1),
            "avg_governance_score":                  round(tgov / n, 1),
            "avg_sovereignty_score":                 round(tsov / n, 1),
            "avg_estimated_geopolitical_risk_index": round(tridx / n, 2),
        }
