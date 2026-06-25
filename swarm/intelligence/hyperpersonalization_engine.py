"""
Module 271 — Hyperpersonalization & Revenue Intelligence Engine
Measures personalization depth, revenue attribution to personalization,
and hyper-targeting effectiveness across channels and segments.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class PersonalizationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class PersonalizationPattern(str, Enum):
    none                  = "none"
    personalization_blindspot = "personalization_blindspot"
    audience_fatigue      = "audience_fatigue"
    privacy_breach        = "privacy_breach"
    relevance_decay       = "relevance_decay"
    attribution_chaos     = "attribution_chaos"


class PersonalizationSeverity(str, Enum):
    irrelevant       = "irrelevant"
    generic          = "generic"
    personalizing    = "personalizing"
    hyperpersonalized = "hyperpersonalized"


class PersonalizationAction(str, Enum):
    no_action                = "no_action"
    personalization_monitoring = "personalization_monitoring"
    segment_refresh          = "segment_refresh"
    fatigue_recovery         = "fatigue_recovery"
    personalization_reset    = "personalization_reset"
    consent_audit            = "consent_audit"


@dataclass
class PersonalizationInput:
    segment_id: str
    channel_type: str   # email_sequence / in_app_experience / sales_outreach /
                        # content_recommendation / pricing_adaptation /
                        # product_bundling / timing_optimization / channel_mix
    region: str
    # 17 numeric fields (0.0–1.0)
    personalization_depth_score: float
    contextual_relevance_accuracy: float
    behavioral_signal_utilization: float
    privacy_consent_compliance: float
    real_time_adaptation_speed: float
    segment_granularity_score: float
    cross_channel_coherence: float
    propensity_model_accuracy: float
    fatigue_risk_score: float              # higher = worse
    value_proposition_fit: float
    emotional_resonance_score: float
    next_best_action_precision: float
    attribution_clarity_score: float
    lifetime_value_impact: float
    churn_prevention_effectiveness: float
    conversion_lift_estimate: float
    recommendation_diversity_score: float


@dataclass
class PersonalizationResult:
    segment_id: str
    channel_type: str
    region: str
    personalization_risk: str
    personalization_pattern: str
    personalization_severity: str
    recommended_action: str
    relevance_score: float
    fatigue_score: float
    privacy_score: float
    impact_score: float
    personalization_composite: float
    has_targeting_gap: bool
    requires_consent_review: bool
    estimated_personalization_gap_index: float
    personalization_signal: str

    def to_dict(self) -> Dict:
        return {
            "segment_id":                         self.segment_id,
            "channel_type":                       self.channel_type,
            "region":                             self.region,
            "personalization_risk":               self.personalization_risk,
            "personalization_pattern":            self.personalization_pattern,
            "personalization_severity":           self.personalization_severity,
            "recommended_action":                 self.recommended_action,
            "relevance_score":                    self.relevance_score,
            "fatigue_score":                      self.fatigue_score,
            "privacy_score":                      self.privacy_score,
            "impact_score":                       self.impact_score,
            "personalization_composite":          self.personalization_composite,
            "has_targeting_gap":                  self.has_targeting_gap,
            "requires_consent_review":            self.requires_consent_review,
            "estimated_personalization_gap_index": self.estimated_personalization_gap_index,
        }


class HyperpersonalizationEngine:
    def __init__(self) -> None:
        self._results: List[PersonalizationResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _relevance_score(self, i: PersonalizationInput) -> float:
        """Weight 0.30 — high = low relevance (risk metric, inverted inputs)"""
        s = 0.0
        # contextual_relevance_accuracy: low = relevance gap
        if   i.contextual_relevance_accuracy <= 0.25: s += 40
        elif i.contextual_relevance_accuracy <= 0.50: s += 22
        elif i.contextual_relevance_accuracy <= 0.70: s += 8

        # propensity_model_accuracy: low = poor propensity
        if   i.propensity_model_accuracy <= 0.25: s += 35
        elif i.propensity_model_accuracy <= 0.50: s += 18
        elif i.propensity_model_accuracy <= 0.70: s += 6

        # next_best_action_precision: low = poor NBA
        if   i.next_best_action_precision <= 0.25: s += 25
        elif i.next_best_action_precision <= 0.50: s += 12
        return min(s, 100.0)

    def _fatigue_score(self, i: PersonalizationInput) -> float:
        """Weight 0.25 — high = fatigue risk"""
        s = 0.0
        # fatigue_risk_score: high = bad
        if   i.fatigue_risk_score >= 0.75: s += 40
        elif i.fatigue_risk_score >= 0.50: s += 22
        elif i.fatigue_risk_score >= 0.30: s += 8

        # personalization_depth_score inverted for risk: over-personalization
        if   i.personalization_depth_score >= 0.90: s += 35
        elif i.personalization_depth_score >= 0.75: s += 18
        elif i.personalization_depth_score >= 0.60: s += 6

        # cross_channel_coherence: low coherence = fatigue amplifier
        if   i.cross_channel_coherence <= 0.25: s += 25
        elif i.cross_channel_coherence <= 0.50: s += 12
        return min(s, 100.0)

    def _privacy_score(self, i: PersonalizationInput) -> float:
        """Weight 0.25 — high = privacy risk"""
        s = 0.0
        # privacy_consent_compliance: low = high risk
        if   i.privacy_consent_compliance <= 0.25: s += 40
        elif i.privacy_consent_compliance <= 0.50: s += 22
        elif i.privacy_consent_compliance <= 0.70: s += 8

        # attribution_clarity_score: low = opaque attribution
        if   i.attribution_clarity_score <= 0.25: s += 35
        elif i.attribution_clarity_score <= 0.50: s += 18
        elif i.attribution_clarity_score <= 0.70: s += 6

        # behavioral_signal_utilization: over-use = privacy risk
        if   i.behavioral_signal_utilization >= 0.90: s += 25
        elif i.behavioral_signal_utilization >= 0.75: s += 12
        return min(s, 100.0)

    def _impact_score(self, i: PersonalizationInput) -> float:
        """Weight 0.20 — high = low business impact (inverted inputs)"""
        s = 0.0
        # conversion_lift_estimate: low = poor impact
        if   i.conversion_lift_estimate <= 0.20: s += 40
        elif i.conversion_lift_estimate <= 0.40: s += 22
        elif i.conversion_lift_estimate <= 0.60: s += 8

        # lifetime_value_impact: low = low LTV contribution
        if   i.lifetime_value_impact <= 0.20: s += 35
        elif i.lifetime_value_impact <= 0.40: s += 18
        elif i.lifetime_value_impact <= 0.60: s += 6

        # churn_prevention_effectiveness: low = ineffective retention
        if   i.churn_prevention_effectiveness <= 0.20: s += 25
        elif i.churn_prevention_effectiveness <= 0.40: s += 12
        return min(s, 100.0)

    def _composite(self, rel: float, fat: float, priv: float, imp: float) -> float:
        return min(round(rel * 0.30 + fat * 0.25 + priv * 0.25 + imp * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> PersonalizationRisk:
        if c >= 60: return PersonalizationRisk.critical
        if c >= 40: return PersonalizationRisk.high
        if c >= 20: return PersonalizationRisk.moderate
        return PersonalizationRisk.low

    def _severity(self, c: float) -> PersonalizationSeverity:
        if c >= 60: return PersonalizationSeverity.irrelevant
        if c >= 40: return PersonalizationSeverity.generic
        if c >= 20: return PersonalizationSeverity.personalizing
        return PersonalizationSeverity.hyperpersonalized

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: PersonalizationInput) -> PersonalizationPattern:
        # Privacy breach: low consent + high behavioral utilization
        if (i.privacy_consent_compliance <= 0.30
                and i.behavioral_signal_utilization >= 0.75):
            return PersonalizationPattern.privacy_breach
        # Attribution chaos: very low attribution clarity
        if i.attribution_clarity_score <= 0.25 and i.conversion_lift_estimate <= 0.30:
            return PersonalizationPattern.attribution_chaos
        # Personalization blindspot: low depth + poor relevance accuracy
        if (i.personalization_depth_score <= 0.25
                and i.contextual_relevance_accuracy <= 0.30):
            return PersonalizationPattern.personalization_blindspot
        # Audience fatigue: high fatigue + low coherence
        if (i.fatigue_risk_score >= 0.65
                and i.cross_channel_coherence <= 0.45):
            return PersonalizationPattern.audience_fatigue
        # Relevance decay: low propensity + low NBA precision
        if (i.propensity_model_accuracy <= 0.35
                and i.next_best_action_precision <= 0.35):
            return PersonalizationPattern.relevance_decay
        return PersonalizationPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(
        self, risk: PersonalizationRisk, pat: PersonalizationPattern
    ) -> PersonalizationAction:
        if risk == PersonalizationRisk.critical:
            if pat == PersonalizationPattern.privacy_breach:
                return PersonalizationAction.consent_audit
            return PersonalizationAction.personalization_reset
        if risk == PersonalizationRisk.high:
            if pat == PersonalizationPattern.audience_fatigue:
                return PersonalizationAction.fatigue_recovery
            return PersonalizationAction.segment_refresh
        if risk == PersonalizationRisk.moderate:
            return PersonalizationAction.personalization_monitoring
        return PersonalizationAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived flags & indices                                             #
    # ------------------------------------------------------------------ #

    def _has_targeting_gap(self, i: PersonalizationInput, comp: float) -> bool:
        return (
            comp >= 35
            or i.segment_granularity_score <= 0.30
            or i.next_best_action_precision <= 0.30
            or i.propensity_model_accuracy <= 0.30
        )

    def _requires_consent_review(self, i: PersonalizationInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.privacy_consent_compliance <= 0.40
            or i.behavioral_signal_utilization >= 0.80
            or i.attribution_clarity_score <= 0.30
        )

    def _gap_index(self, i: PersonalizationInput, comp: float) -> float:
        return round(
            min(comp / 100 * (1 - i.attribution_clarity_score + 0.01) * 10, 10.0), 2
        )

    def _signal(
        self, i: PersonalizationInput, pat: PersonalizationPattern, comp: float
    ) -> str:
        if comp < 20:
            return (
                "Hyperpersonnalisation efficace — ciblage précis, consentement respecté, "
                "impact revenus confirmé, modèles propensity performants"
            )
        labels: Dict[PersonalizationPattern, str] = {
            PersonalizationPattern.personalization_blindspot: "Point aveugle personnalisation",
            PersonalizationPattern.audience_fatigue:          "Fatigue audience",
            PersonalizationPattern.privacy_breach:            "Risque vie privée",
            PersonalizationPattern.relevance_decay:           "Dégradation pertinence",
            PersonalizationPattern.attribution_chaos:         "Chaos attribution revenus",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — profondeur {i.personalization_depth_score:.2f}"
            f" — pertinence {i.contextual_relevance_accuracy * 100:.0f}%"
            f" — consentement {i.privacy_consent_compliance * 100:.0f}%"
            f" — lift conversion {i.conversion_lift_estimate * 100:.0f}%"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: PersonalizationInput) -> PersonalizationResult:
        rel  = self._relevance_score(i)
        fat  = self._fatigue_score(i)
        priv = self._privacy_score(i)
        imp  = self._impact_score(i)
        comp = self._composite(rel, fat, priv, imp)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = PersonalizationResult(
            segment_id=i.segment_id,
            channel_type=i.channel_type,
            region=i.region,
            personalization_risk=risk.value,
            personalization_pattern=pat.value,
            personalization_severity=sev.value,
            recommended_action=act.value,
            relevance_score=rel,
            fatigue_score=fat,
            privacy_score=priv,
            impact_score=imp,
            personalization_composite=comp,
            has_targeting_gap=self._has_targeting_gap(i, comp),
            requires_consent_review=self._requires_consent_review(i, comp),
            estimated_personalization_gap_index=self._gap_index(i, comp),
            personalization_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[PersonalizationInput]) -> List[PersonalizationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_personalization_composite": 0.0,
                "targeting_gap_count": 0,
                "consent_review_required_count": 0,
                "avg_relevance_score": 0.0,
                "avg_fatigue_score": 0.0,
                "avg_privacy_score": 0.0,
                "avg_impact_score": 0.0,
                "avg_estimated_personalization_gap_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        trel = tfat = tpriv = timp = tcomp = tgap = 0.0
        gap_count = consent_count = 0
        for r in self._results:
            rc[r.personalization_risk]    = rc.get(r.personalization_risk, 0)    + 1
            pc[r.personalization_pattern] = pc.get(r.personalization_pattern, 0) + 1
            sc[r.personalization_severity]= sc.get(r.personalization_severity, 0)+ 1
            ac[r.recommended_action]      = ac.get(r.recommended_action, 0)      + 1
            trel  += r.relevance_score
            tfat  += r.fatigue_score
            tpriv += r.privacy_score
            timp  += r.impact_score
            tcomp += r.personalization_composite
            tgap  += r.estimated_personalization_gap_index
            if r.has_targeting_gap:        gap_count     += 1
            if r.requires_consent_review:  consent_count += 1
        return {
            "total":                                   n,
            "risk_counts":                             rc,
            "pattern_counts":                          pc,
            "severity_counts":                         sc,
            "action_counts":                           ac,
            "avg_personalization_composite":           round(tcomp / n, 1),
            "targeting_gap_count":                     gap_count,
            "consent_review_required_count":           consent_count,
            "avg_relevance_score":                     round(trel / n, 1),
            "avg_fatigue_score":                       round(tfat / n, 1),
            "avg_privacy_score":                       round(tpriv / n, 1),
            "avg_impact_score":                        round(timp / n, 1),
            "avg_estimated_personalization_gap_index": round(tgap / n, 2),
        }
