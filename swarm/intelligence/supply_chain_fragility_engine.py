"""
Module 311 — Global Supply Chain Fragility Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles

Evaluates global supply chain fragility across concentration risk,
operational fragility, multi-dimensional threat exposure, and
structural adaptation capacity for sovereign supply intelligence.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List


# ─── Input ────────────────────────────────────────────────────────────────────

@dataclass
class SupplyChainFragilityInput:
    entity_id: str
    chain_type: str
    region: str
    # 17 fragility dimensions (0.0–1.0)
    single_source_dependency: float
    just_in_time_vulnerability: float
    geopolitical_chokepoint_exposure: float
    logistics_network_fragility: float
    supplier_financial_fragility: float
    inventory_buffer_adequacy: float          # inverse: high=good
    demand_shock_sensitivity: float
    nearshoring_readiness: float              # inverse: high=good
    digital_supply_chain_risk: float
    counterfeit_infiltration_risk: float
    port_concentration_risk: float
    regulatory_divergence_burden: float
    natural_disaster_exposure: float
    cybersecurity_supply_risk: float
    ESG_compliance_gap: float
    labor_disruption_potential: float
    cross_border_friction: float


# ─── Result ───────────────────────────────────────────────────────────────────

@dataclass
class SupplyChainFragilityResult:
    entity_id: str
    region: str
    chain_type: str
    chain_risk: str
    chain_pattern: str
    chain_severity: str
    recommended_action: str
    concentration_score: float
    fragility_score: float
    risk_score: float
    adaptation_score: float
    chain_composite: float
    is_chain_crisis: bool
    requires_chain_intervention: bool
    chain_signal: str

    def to_dict(self) -> dict:
        return {
            "entity_id":                   self.entity_id,
            "region":                      self.region,
            "chain_type":                  self.chain_type,
            "chain_risk":                  self.chain_risk,
            "chain_pattern":               self.chain_pattern,
            "chain_severity":              self.chain_severity,
            "recommended_action":          self.recommended_action,
            "concentration_score":         round(self.concentration_score, 2),
            "fragility_score":             round(self.fragility_score, 2),
            "risk_score":                  round(self.risk_score, 2),
            "adaptation_score":            round(self.adaptation_score, 2),
            "chain_composite":             round(self.chain_composite, 2),
            "is_chain_crisis":             self.is_chain_crisis,
            "requires_chain_intervention": self.requires_chain_intervention,
            "chain_signal":                self.chain_signal,
        }


# ─── Engine ───────────────────────────────────────────────────────────────────

class SupplyChainFragilityEngine:
    """Module 311 — Global Supply Chain Fragility Intelligence Engine."""

    MODULE  = "Module 311"
    ENGINE  = "Global Supply Chain Fragility Intelligence Engine"
    ANALYST = "Chaima Mhadbi, Fondatrice, Caelum Partners, Bruxelles"

    def __init__(self) -> None:
        self._results: list[SupplyChainFragilityResult] = []

    # ── Sub-scores ─────────────────────────────────────────────────────────────

    @staticmethod
    def _concentration_score(inp: SupplyChainFragilityInput) -> float:
        """Concentration & chokepoint risk — weight 0.30."""
        return (
            inp.single_source_dependency * 0.40
            + inp.port_concentration_risk * 0.35
            + inp.geopolitical_chokepoint_exposure * 0.25
        ) * 100

    @staticmethod
    def _fragility_score(inp: SupplyChainFragilityInput) -> float:
        """Operational fragility & buffer risk — weight 0.25."""
        return (
            inp.just_in_time_vulnerability * 0.40
            + inp.logistics_network_fragility * 0.35
            + (1 - inp.inventory_buffer_adequacy) * 0.25
        ) * 100

    @staticmethod
    def _risk_score(inp: SupplyChainFragilityInput) -> float:
        """Multi-dimensional threat exposure — weight 0.25."""
        return (
            inp.cybersecurity_supply_risk * 0.40
            + inp.counterfeit_infiltration_risk * 0.35
            + inp.supplier_financial_fragility * 0.25
        ) * 100

    @staticmethod
    def _adaptation_score(inp: SupplyChainFragilityInput) -> float:
        """Structural adaptation capacity — weight 0.20."""
        return (
            (1 - inp.nearshoring_readiness) * 0.40
            + inp.regulatory_divergence_burden * 0.35
            + inp.cross_border_friction * 0.25
        ) * 100

    @staticmethod
    def _composite(
        concentration: float,
        fragility: float,
        risk: float,
        adaptation: float,
    ) -> float:
        return (
            concentration * 0.30
            + fragility   * 0.25
            + risk        * 0.25
            + adaptation  * 0.20
        )

    # ── Classification ─────────────────────────────────────────────────────────

    @staticmethod
    def _chain_risk(composite: float) -> str:
        if composite >= 60: return "critical"
        if composite >= 40: return "high"
        if composite >= 20: return "moderate"
        return "low"

    @staticmethod
    def _chain_pattern(inp: SupplyChainFragilityInput) -> str:
        if (inp.single_source_dependency >= 0.70
                and inp.geopolitical_chokepoint_exposure >= 0.65):
            return "single_source_crisis"
        if (inp.just_in_time_vulnerability >= 0.70
                and inp.demand_shock_sensitivity >= 0.65):
            return "jit_shock_cascade"
        if (inp.supplier_financial_fragility >= 0.70
                and inp.inventory_buffer_adequacy <= 0.40):
            return "supplier_bankruptcy_wave"
        if (inp.cybersecurity_supply_risk >= 0.70
                and inp.digital_supply_chain_risk >= 0.65):
            return "cyber_supply_attack"
        if (inp.regulatory_divergence_burden >= 0.70
                and inp.cross_border_friction >= 0.65):
            return "regulatory_fragmentation"
        return "none"

    @staticmethod
    def _chain_severity(composite: float) -> str:
        if composite >= 75: return "supply_emergency"
        if composite >= 50: return "high_fragility"
        if composite >= 25: return "supply_tension"
        return "chain_robust"

    @staticmethod
    def _recommended_action(chain_risk: str, chain_pattern: str) -> str:
        if chain_risk == "critical":
            return "emergency_supply_rerouting"
        if chain_risk == "high" and chain_pattern == "single_source_crisis":
            return "supply_diversification"
        if chain_risk == "high":
            return "resilience_buffer_program"
        if chain_risk == "moderate":
            return "supply_monitoring"
        return "no_action"

    @staticmethod
    def _chain_signal(
        inp: SupplyChainFragilityInput,
        chain_pattern: str,
        chain_risk: str,
        composite: float,
    ) -> str:
        if chain_risk == "low":
            return (
                f"Chaîne d'approvisionnement {inp.chain_type} résiliente — "
                f"composite fragilité {composite:.0f} — aucune rupture détectée"
            )
        pattern_signals: dict[str, str] = {
            "single_source_crisis": (
                f"Crise source unique détectée — dépendance mono-fournisseur "
                f"{inp.single_source_dependency:.2f} combinée à exposition goulot géopolitique "
                f"{inp.geopolitical_chokepoint_exposure:.2f} — risque rupture totale"
            ),
            "jit_shock_cascade": (
                f"Cascade JIT sous choc — vulnérabilité flux tendu "
                f"{inp.just_in_time_vulnerability:.2f}, sensibilité choc demande "
                f"{inp.demand_shock_sensitivity:.2f} — effondrement synchronisé probable"
            ),
            "supplier_bankruptcy_wave": (
                f"Vague de défaillances fournisseurs — fragilité financière "
                f"{inp.supplier_financial_fragility:.2f}, buffer stocks insuffisant "
                f"{inp.inventory_buffer_adequacy:.2f} — risque rupture critique"
            ),
            "cyber_supply_attack": (
                f"Attaque cybersécurité chaîne — risque cyber {inp.cybersecurity_supply_risk:.2f}, "
                f"exposition numérique {inp.digital_supply_chain_risk:.2f} — "
                f"compromission infrastructure approvisionnement"
            ),
            "regulatory_fragmentation": (
                f"Fragmentation réglementaire — divergence normative "
                f"{inp.regulatory_divergence_burden:.2f}, friction transfrontalière "
                f"{inp.cross_border_friction:.2f} — blocage flux commerciaux"
            ),
        }
        base = pattern_signals.get(
            chain_pattern,
            f"Fragilité chaîne {inp.chain_type} détectée — composite {composite:.0f}",
        )
        return f"{base} — risque {chain_risk} — région {inp.region}"

    # ── Public API ─────────────────────────────────────────────────────────────

    def _assess_one(self, inp: SupplyChainFragilityInput) -> SupplyChainFragilityResult:
        concentration = self._concentration_score(inp)
        fragility     = self._fragility_score(inp)
        risk          = self._risk_score(inp)
        adaptation    = self._adaptation_score(inp)
        composite     = self._composite(concentration, fragility, risk, adaptation)

        chain_risk    = self._chain_risk(composite)
        chain_pattern = self._chain_pattern(inp)
        chain_severity = self._chain_severity(composite)
        action        = self._recommended_action(chain_risk, chain_pattern)
        chain_signal  = self._chain_signal(inp, chain_pattern, chain_risk, composite)

        return SupplyChainFragilityResult(
            entity_id=inp.entity_id,
            region=inp.region,
            chain_type=inp.chain_type,
            chain_risk=chain_risk,
            chain_pattern=chain_pattern,
            chain_severity=chain_severity,
            recommended_action=action,
            concentration_score=concentration,
            fragility_score=fragility,
            risk_score=risk,
            adaptation_score=adaptation,
            chain_composite=composite,
            is_chain_crisis=(composite >= 60),
            requires_chain_intervention=(composite >= 40),
            chain_signal=chain_signal,
        )

    def assess(self, entities: List[SupplyChainFragilityInput]) -> dict:
        """Assess a list of supply chain entities and return a full summary dict."""
        self._results.clear()
        for inp in entities:
            self._results.append(self._assess_one(inp))

        n = len(self._results)
        risk_distribution: dict[str, int] = {"low": 0, "moderate": 0, "high": 0, "critical": 0}
        pattern_counts: dict[str, int] = {}
        total_composite = 0.0
        critical_count = 0
        high_count = 0
        crisis_count = 0
        intervention_count = 0

        for r in self._results:
            risk_distribution[r.chain_risk] = risk_distribution.get(r.chain_risk, 0) + 1
            pattern_counts[r.chain_pattern] = pattern_counts.get(r.chain_pattern, 0) + 1
            total_composite += r.chain_composite
            if r.chain_risk == "critical":
                critical_count += 1
            if r.chain_risk == "high":
                high_count += 1
            if r.is_chain_crisis:
                crisis_count += 1
            if r.requires_chain_intervention:
                intervention_count += 1

        avg_composite = total_composite / n if n else 0.0
        dominant_pattern = (
            max(pattern_counts, key=lambda k: pattern_counts[k])
            if pattern_counts else "none"
        )
        avg_fragility_index = round(avg_composite / 100 * 10, 2)

        return {
            "module":                            self.MODULE,
            "engine":                            self.ENGINE,
            "analyst":                           self.ANALYST,
            "timestamp":                         datetime.now(timezone.utc).isoformat(),
            "total_entities_assessed":           n,
            "critical_chains":                   critical_count,
            "high_risk_chains":                  high_count,
            "chain_crises_detected":             crisis_count,
            "requires_intervention":             intervention_count,
            "dominant_pattern":                  dominant_pattern,
            "avg_estimated_chain_fragility_index": avg_fragility_index,
            "risk_distribution":                 risk_distribution,
            "entities":                          [r.to_dict() for r in self._results],
        }
