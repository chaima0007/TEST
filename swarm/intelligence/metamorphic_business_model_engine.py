from __future__ import annotations
from dataclasses import dataclass
from typing import List
import math


@dataclass
class BusinessModelInput:
    entity_id: str
    transformation_stage: str
    region: str
    transformation_velocity: float
    identity_coherence_score: float
    legacy_anchor_risk: float
    new_capability_readiness: float
    revenue_model_clarity: float
    stakeholder_change_tolerance: float
    cultural_transformation_depth: float
    innovation_pipeline_richness: float
    organizational_grief_processing: float
    transformation_leadership_strength: float
    change_momentum_score: float
    resistance_to_change_index: float
    ecosystem_partner_alignment: float
    customer_migration_readiness: float
    financial_runway_adequacy: float
    metamorphic_vision_clarity: float
    post_transformation_market_fit: float


class BusinessModelAssessment:
    def __init__(
        self,
        entity_id: str,
        region: str,
        transformation_stage: str,
        transformation_risk: str,
        metamorphic_pattern: str,
        transformation_severity: str,
        recommended_action: str,
        stagnation_score: float,
        readiness_score: float,
        momentum_score: float,
        alignment_score: float,
        transformation_composite: float,
        is_in_metamorphic_crisis: bool,
        requires_immediate_intervention: bool,
        transformation_signal: str,
    ):
        self.entity_id = entity_id
        self.region = region
        self.transformation_stage = transformation_stage
        self.transformation_risk = transformation_risk
        self.metamorphic_pattern = metamorphic_pattern
        self.transformation_severity = transformation_severity
        self.recommended_action = recommended_action
        self.stagnation_score = stagnation_score
        self.readiness_score = readiness_score
        self.momentum_score = momentum_score
        self.alignment_score = alignment_score
        self.transformation_composite = transformation_composite
        self.is_in_metamorphic_crisis = is_in_metamorphic_crisis
        self.requires_immediate_intervention = requires_immediate_intervention
        self.transformation_signal = transformation_signal

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "transformation_stage": self.transformation_stage,
            "transformation_risk": self.transformation_risk,
            "metamorphic_pattern": self.metamorphic_pattern,
            "transformation_severity": self.transformation_severity,
            "recommended_action": self.recommended_action,
            "stagnation_score": self.stagnation_score,
            "readiness_score": self.readiness_score,
            "momentum_score": self.momentum_score,
            "alignment_score": self.alignment_score,
            "transformation_composite": self.transformation_composite,
            "is_in_metamorphic_crisis": self.is_in_metamorphic_crisis,
            "requires_immediate_intervention": self.requires_immediate_intervention,
            "transformation_signal": self.transformation_signal,
        }


class MetamorphicBusinessModelEngine:

    def assess_batch(self, inputs: List[BusinessModelInput]) -> List[dict]:
        results = []
        for inp in inputs:
            d = self._assess(inp).to_dict()
            # Store market fit for use in summary() risk index calculation
            d["_post_transformation_market_fit"] = inp.post_transformation_market_fit
            results.append(d)
        return results

    def _assess(self, inp: BusinessModelInput) -> BusinessModelAssessment:
        # --- Stagnation Score ---
        stagnation = 0.0
        if inp.legacy_anchor_risk >= 0.70:
            stagnation += 40
        elif inp.legacy_anchor_risk >= 0.50:
            stagnation += 22
        elif inp.legacy_anchor_risk >= 0.35:
            stagnation += 8

        if inp.resistance_to_change_index >= 0.70:
            stagnation += 35
        elif inp.resistance_to_change_index >= 0.50:
            stagnation += 18
        elif inp.resistance_to_change_index >= 0.35:
            stagnation += 6

        if inp.identity_coherence_score <= 0.30:
            stagnation += 25
        elif inp.identity_coherence_score <= 0.50:
            stagnation += 12

        stagnation_score = min(stagnation, 100.0)

        # --- Readiness Score ---
        readiness = 0.0
        if inp.new_capability_readiness <= 0.30:
            readiness += 40
        elif inp.new_capability_readiness <= 0.50:
            readiness += 22
        elif inp.new_capability_readiness <= 0.65:
            readiness += 8

        if inp.transformation_leadership_strength <= 0.30:
            readiness += 35
        elif inp.transformation_leadership_strength <= 0.50:
            readiness += 18
        elif inp.transformation_leadership_strength <= 0.65:
            readiness += 6

        if inp.financial_runway_adequacy <= 0.30:
            readiness += 25
        elif inp.financial_runway_adequacy <= 0.50:
            readiness += 12

        readiness_score = min(readiness, 100.0)

        # --- Momentum Score ---
        momentum = 0.0
        if inp.change_momentum_score <= 0.30:
            momentum += 40
        elif inp.change_momentum_score <= 0.50:
            momentum += 22
        elif inp.change_momentum_score <= 0.65:
            momentum += 8

        if inp.transformation_velocity <= 0.30:
            momentum += 35
        elif inp.transformation_velocity <= 0.50:
            momentum += 18
        elif inp.transformation_velocity <= 0.65:
            momentum += 6

        if inp.innovation_pipeline_richness <= 0.30:
            momentum += 25
        elif inp.innovation_pipeline_richness <= 0.50:
            momentum += 12

        momentum_score = min(momentum, 100.0)

        # --- Alignment Score ---
        alignment = 0.0
        if inp.ecosystem_partner_alignment <= 0.30:
            alignment += 40
        elif inp.ecosystem_partner_alignment <= 0.50:
            alignment += 22
        elif inp.ecosystem_partner_alignment <= 0.65:
            alignment += 8

        if inp.customer_migration_readiness <= 0.30:
            alignment += 35
        elif inp.customer_migration_readiness <= 0.50:
            alignment += 18
        elif inp.customer_migration_readiness <= 0.65:
            alignment += 6

        if inp.stakeholder_change_tolerance <= 0.30:
            alignment += 25
        elif inp.stakeholder_change_tolerance <= 0.50:
            alignment += 12

        alignment_score = min(alignment, 100.0)

        # --- Composite ---
        composite = (
            stagnation_score * 0.30
            + readiness_score * 0.25
            + momentum_score * 0.25
            + alignment_score * 0.20
        )
        composite = round(min(composite, 100.0), 2)

        # --- Pattern (first matching) ---
        if inp.legacy_anchor_risk >= 0.65 and inp.change_momentum_score <= 0.35:
            pattern = "metamorphic_stall"
        elif (
            inp.identity_coherence_score <= 0.30
            or (
                inp.resistance_to_change_index >= 0.65
                and inp.metamorphic_vision_clarity <= 0.35
            )
        ):
            pattern = "identity_crisis"
        elif (
            inp.new_capability_readiness <= 0.30
            and inp.innovation_pipeline_richness <= 0.35
        ):
            pattern = "capability_gap"
        elif (
            inp.ecosystem_partner_alignment <= 0.30
            and inp.customer_migration_readiness <= 0.35
        ):
            pattern = "ecosystem_rejection"
        elif (
            inp.metamorphic_vision_clarity <= 0.25
            and inp.transformation_leadership_strength <= 0.35
        ):
            pattern = "vision_collapse"
        else:
            pattern = "none"

        # --- Severity ---
        if composite >= 60:
            severity = "fossilized"
        elif composite >= 40:
            severity = "transitioning"
        elif composite >= 20:
            severity = "morphing"
        else:
            severity = "metamorphosed"

        # --- Risk ---
        if composite >= 60:
            risk = "critical"
        elif composite >= 40:
            risk = "high"
        elif composite >= 20:
            risk = "moderate"
        else:
            risk = "low"

        # --- Action ---
        if risk == "critical" and pattern == "metamorphic_stall":
            action = "transformation_emergency"
        elif risk == "critical":
            action = "identity_reconstruction"
        elif risk == "high" and pattern == "capability_gap":
            action = "capability_sprint"
        elif risk == "high":
            action = "ecosystem_rebuild"
        elif risk == "moderate":
            action = "transformation_monitoring"
        else:
            action = "no_action"

        # --- Boolean flags ---
        is_in_metamorphic_crisis = (
            composite >= 40
            or inp.legacy_anchor_risk >= 0.60
            or inp.resistance_to_change_index >= 0.60
            or inp.metamorphic_vision_clarity <= 0.25
        )

        requires_immediate_intervention = (
            composite >= 25
            or inp.transformation_leadership_strength <= 0.30
            or inp.financial_runway_adequacy <= 0.30
            or inp.post_transformation_market_fit <= 0.25
        )

        # --- French signal ---
        if composite < 20:
            signal = (
                "Métamorphose accomplie — modèle d'affaires réinventé, "
                "transformation intégrée, alignement écosystémique confirmé"
            )
        else:
            pattern_labels = {
                "metamorphic_stall": "Stagnation métamorphique",
                "identity_crisis": "Crise identitaire",
                "capability_gap": "Déficit capacitaire",
                "ecosystem_rejection": "Rejet écosystémique",
                "vision_collapse": "Effondrement visionnaire",
                "none": "Transformation en cours",
            }
            label = pattern_labels[pattern]
            signal = (
                f"{label} — vélocité {inp.transformation_velocity:.2f} "
                f"— vision {inp.metamorphic_vision_clarity:.0%} "
                f"— composite {composite:.0f}"
            )

        return BusinessModelAssessment(
            entity_id=inp.entity_id,
            region=inp.region,
            transformation_stage=inp.transformation_stage,
            transformation_risk=risk,
            metamorphic_pattern=pattern,
            transformation_severity=severity,
            recommended_action=action,
            stagnation_score=stagnation_score,
            readiness_score=readiness_score,
            momentum_score=momentum_score,
            alignment_score=alignment_score,
            transformation_composite=composite,
            is_in_metamorphic_crisis=is_in_metamorphic_crisis,
            requires_immediate_intervention=requires_immediate_intervention,
            transformation_signal=signal,
        )

    def summary(self, results: List[dict]) -> dict:
        total = len(results)

        risk_counts: dict = {}
        pattern_counts: dict = {}
        severity_counts: dict = {}
        action_counts: dict = {}

        composites = []
        stagnation_scores = []
        readiness_scores = []
        momentum_scores = []
        alignment_scores = []
        metamorphic_crisis_count = 0
        immediate_intervention_count = 0
        risk_indices = []

        for r in results:
            risk_counts[r["transformation_risk"]] = (
                risk_counts.get(r["transformation_risk"], 0) + 1
            )
            pattern_counts[r["metamorphic_pattern"]] = (
                pattern_counts.get(r["metamorphic_pattern"], 0) + 1
            )
            severity_counts[r["transformation_severity"]] = (
                severity_counts.get(r["transformation_severity"], 0) + 1
            )
            action_counts[r["recommended_action"]] = (
                action_counts.get(r["recommended_action"], 0) + 1
            )

            composites.append(r["transformation_composite"])
            stagnation_scores.append(r["stagnation_score"])
            readiness_scores.append(r["readiness_score"])
            momentum_scores.append(r["momentum_score"])
            alignment_scores.append(r["alignment_score"])

            if r["is_in_metamorphic_crisis"]:
                metamorphic_crisis_count += 1
            if r["requires_immediate_intervention"]:
                immediate_intervention_count += 1

        # avg_estimated_transformation_risk_index:
        # per entity: min(composite/100 * (1 - post_transformation_market_fit + 0.01) * 10, 10.0)
        # _post_transformation_market_fit is injected by assess_batch as a private key
        for r in results:
            composite = r["transformation_composite"]
            pmf = r.get("_post_transformation_market_fit", 0.5)
            idx = round(min(composite / 100.0 * (1 - pmf + 0.01) * 10, 10.0), 2)
            risk_indices.append(idx)

        def safe_avg(lst):
            if not lst:
                return 0.0
            return round(sum(lst) / len(lst), 2)

        return {
            "total": total,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_transformation_composite": safe_avg(composites),
            "metamorphic_crisis_count": metamorphic_crisis_count,
            "immediate_intervention_count": immediate_intervention_count,
            "avg_stagnation_score": safe_avg(stagnation_scores),
            "avg_readiness_score": safe_avg(readiness_scores),
            "avg_momentum_score": safe_avg(momentum_scores),
            "avg_alignment_score": safe_avg(alignment_scores),
            "avg_estimated_transformation_risk_index": safe_avg(risk_indices),
        }
