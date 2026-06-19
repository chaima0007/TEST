"""
Module 252 — Memetic Resonance & Viral Idea Propagation Engine
Analyzes idea propagation dynamics across organizational and market networks —
meme velocity, narrative virality, belief system resilience, counter-meme
exposure, and cultural adoption curves.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class MemeticRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class MemeticPattern(str, Enum):
    none                  = "none"
    viral_cascade         = "viral_cascade"
    echo_chamber_lock     = "echo_chamber_lock"
    narrative_hijack      = "narrative_hijack"
    counter_meme_collapse = "counter_meme_collapse"
    belief_crystallization = "belief_crystallization"


class MemeticSeverity(str, Enum):
    contained  = "contained"
    seeding    = "seeding"
    spreading  = "spreading"
    epidemic   = "epidemic"


class MemeticAction(str, Enum):
    no_action               = "no_action"
    meme_monitoring         = "meme_monitoring"
    narrative_steering      = "narrative_steering"
    influence_mapping       = "influence_mapping"
    crisis_narrative_reset  = "crisis_narrative_reset"
    counter_meme_injection  = "counter_meme_injection"


@dataclass
class MemeticInput:
    meme_id: str
    meme_type: str   # brand_narrative/product_concept/cultural_movement/crisis_narrative/
                     # political_ideology/scientific_paradigm/organizational_value/market_sentiment
    region: str
    # 17 numeric fields (0.0–1.0)
    virality_coefficient: float           # R0 analog, 0=no spread, 1=explosive
    resonance_depth_score: float
    adoption_velocity: float
    network_penetration_rate: float
    counter_meme_resistance: float        # higher=more resistant
    emotional_hook_strength: float
    cognitive_load_barrier: float         # higher=harder to adopt
    platform_amplification_factor: float
    influencer_alignment_score: float
    narrative_coherence_score: float
    temporal_stickiness_score: float
    cross_cultural_adaptation_score: float
    belief_entrenchment_level: float
    social_proof_density: float
    fear_uncertainty_doubt_index: float   # FUD, higher=destabilizing
    memetic_mutation_rate: float          # higher=degrading
    echo_chamber_intensity: float


@dataclass
class MemeticResult:
    meme_id: str
    meme_type: str
    region: str
    memetic_risk: str
    memetic_pattern: str
    memetic_severity: str
    recommended_action: str
    virality_score: float
    resonance_score: float
    persistence_score: float
    reach_score: float
    memetic_composite: float
    is_epidemic_threat: bool
    requires_active_intervention: bool
    estimated_viral_disruption_index: float
    memetic_signal: str

    def to_dict(self) -> Dict:
        return {
            "meme_id":                          self.meme_id,
            "meme_type":                        self.meme_type,
            "region":                           self.region,
            "memetic_risk":                     self.memetic_risk,
            "memetic_pattern":                  self.memetic_pattern,
            "memetic_severity":                 self.memetic_severity,
            "recommended_action":               self.recommended_action,
            "virality_score":                   self.virality_score,
            "resonance_score":                  self.resonance_score,
            "persistence_score":                self.persistence_score,
            "reach_score":                      self.reach_score,
            "memetic_composite":                self.memetic_composite,
            "is_epidemic_threat":               self.is_epidemic_threat,
            "requires_active_intervention":     self.requires_active_intervention,
            "estimated_viral_disruption_index": self.estimated_viral_disruption_index,
            "memetic_signal":                   self.memetic_signal,
        }


class MemeticResonanceEngine:
    def __init__(self) -> None:
        self._results: List[MemeticResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100, capped)                                          #
    # ------------------------------------------------------------------ #

    def _virality_score(self, i: MemeticInput) -> float:
        """virality_coefficient + platform_amplification_factor + adoption_velocity"""
        raw = (i.virality_coefficient + i.platform_amplification_factor + i.adoption_velocity) / 3.0
        return min(round(raw * 100, 2), 100.0)

    def _resonance_score(self, i: MemeticInput) -> float:
        """emotional_hook_strength + narrative_coherence_score + resonance_depth_score"""
        raw = (i.emotional_hook_strength + i.narrative_coherence_score + i.resonance_depth_score) / 3.0
        return min(round(raw * 100, 2), 100.0)

    def _persistence_score(self, i: MemeticInput) -> float:
        """temporal_stickiness_score + belief_entrenchment_level + counter_meme_resistance"""
        raw = (i.temporal_stickiness_score + i.belief_entrenchment_level + i.counter_meme_resistance) / 3.0
        return min(round(raw * 100, 2), 100.0)

    def _reach_score(self, i: MemeticInput) -> float:
        """network_penetration_rate + influencer_alignment_score + cross_cultural_adaptation_score"""
        raw = (i.network_penetration_rate + i.influencer_alignment_score + i.cross_cultural_adaptation_score) / 3.0
        return min(round(raw * 100, 2), 100.0)

    def _composite(self, vir: float, res: float, per: float, rch: float) -> float:
        return min(round(vir * 0.30 + res * 0.25 + per * 0.25 + rch * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> MemeticRisk:
        if c >= 60: return MemeticRisk.critical
        if c >= 40: return MemeticRisk.high
        if c >= 20: return MemeticRisk.moderate
        return MemeticRisk.low

    def _severity(self, c: float) -> MemeticSeverity:
        if c >= 60: return MemeticSeverity.epidemic
        if c >= 40: return MemeticSeverity.spreading
        if c >= 20: return MemeticSeverity.seeding
        return MemeticSeverity.contained

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: MemeticInput) -> MemeticPattern:
        if i.virality_coefficient >= 0.75 and i.platform_amplification_factor >= 0.70:
            return MemeticPattern.viral_cascade
        if i.echo_chamber_intensity >= 0.70 and i.cross_cultural_adaptation_score <= 0.35:
            return MemeticPattern.echo_chamber_lock
        if i.memetic_mutation_rate >= 0.65 and i.narrative_coherence_score <= 0.40:
            return MemeticPattern.narrative_hijack
        if i.counter_meme_resistance <= 0.25 and i.fear_uncertainty_doubt_index >= 0.60:
            return MemeticPattern.counter_meme_collapse
        if i.belief_entrenchment_level >= 0.70 and i.cognitive_load_barrier <= 0.35:
            return MemeticPattern.belief_crystallization
        return MemeticPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: MemeticRisk, pat: MemeticPattern) -> MemeticAction:
        if risk == MemeticRisk.critical:
            if pat in (MemeticPattern.viral_cascade, MemeticPattern.echo_chamber_lock):
                return MemeticAction.crisis_narrative_reset
            return MemeticAction.counter_meme_injection
        if risk == MemeticRisk.high:
            if pat in (MemeticPattern.narrative_hijack, MemeticPattern.counter_meme_collapse):
                return MemeticAction.narrative_steering
            return MemeticAction.influence_mapping
        if risk == MemeticRisk.moderate:
            return MemeticAction.meme_monitoring
        return MemeticAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived fields                                                      #
    # ------------------------------------------------------------------ #

    def _is_epidemic(self, comp: float) -> bool:
        return comp >= 60

    def _requires_intervention(self, comp: float) -> bool:
        return comp >= 40

    def _viral_disruption_index(self, i: MemeticInput, comp: float) -> float:
        return round(
            min(comp / 100 * (i.virality_coefficient + i.echo_chamber_intensity) / 2 * 10, 10.0),
            2,
        )

    def _signal(self, i: MemeticInput, pat: MemeticPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Mème stabilisé — propagation maîtrisée, narration cohérente, résonance contrôlée"
            )
        pat_labels: Dict[MemeticPattern, str] = {
            MemeticPattern.viral_cascade:          "Cascade virale",
            MemeticPattern.echo_chamber_lock:      "Verrouillage chambre d'écho",
            MemeticPattern.narrative_hijack:       "Détournement narratif",
            MemeticPattern.counter_meme_collapse:  "Effondrement contre-mème",
            MemeticPattern.belief_crystallization: "Cristallisation des croyances",
            MemeticPattern.none:                   "Propagation active",
        }
        label = pat_labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — viralité {i.virality_coefficient:.2f}"
            f" — pénétration réseau {i.network_penetration_rate:.2f}"
            f" — résonance {i.resonance_depth_score:.2f}"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: MemeticInput) -> MemeticResult:
        vir  = self._virality_score(i)
        res  = self._resonance_score(i)
        per  = self._persistence_score(i)
        rch  = self._reach_score(i)
        comp = self._composite(vir, res, per, rch)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = MemeticResult(
            meme_id=i.meme_id,
            meme_type=i.meme_type,
            region=i.region,
            memetic_risk=risk.value,
            memetic_pattern=pat.value,
            memetic_severity=sev.value,
            recommended_action=act.value,
            virality_score=vir,
            resonance_score=res,
            persistence_score=per,
            reach_score=rch,
            memetic_composite=comp,
            is_epidemic_threat=self._is_epidemic(comp),
            requires_active_intervention=self._requires_intervention(comp),
            estimated_viral_disruption_index=self._viral_disruption_index(i, comp),
            memetic_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[MemeticInput]) -> List[MemeticResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_memetic_composite": 0.0,
                "epidemic_count": 0,
                "active_intervention_count": 0,
                "avg_virality_score": 0.0,
                "avg_resonance_score": 0.0,
                "avg_persistence_score": 0.0,
                "avg_reach_score": 0.0,
                "avg_estimated_viral_disruption_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tvir = tres = tper = trch = tcomp = tdis = 0.0
        epidemic_count = intervention_count = 0
        for r in self._results:
            rc[r.memetic_risk]      = rc.get(r.memetic_risk, 0)      + 1
            pc[r.memetic_pattern]   = pc.get(r.memetic_pattern, 0)   + 1
            sc[r.memetic_severity]  = sc.get(r.memetic_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tvir  += r.virality_score
            tres  += r.resonance_score
            tper  += r.persistence_score
            trch  += r.reach_score
            tcomp += r.memetic_composite
            tdis  += r.estimated_viral_disruption_index
            if r.is_epidemic_threat:            epidemic_count     += 1
            if r.requires_active_intervention:  intervention_count += 1
        return {
            "total":                               n,
            "risk_counts":                         rc,
            "pattern_counts":                      pc,
            "severity_counts":                     sc,
            "action_counts":                       ac,
            "avg_memetic_composite":               round(tcomp / n, 1),
            "epidemic_count":                      epidemic_count,
            "active_intervention_count":           intervention_count,
            "avg_virality_score":                  round(tvir / n, 1),
            "avg_resonance_score":                 round(tres / n, 1),
            "avg_persistence_score":               round(tper / n, 1),
            "avg_reach_score":                     round(trch / n, 1),
            "avg_estimated_viral_disruption_index": round(tdis / n, 2),
        }
