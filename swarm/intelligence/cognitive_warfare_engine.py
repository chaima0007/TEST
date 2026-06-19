from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

ThreatDomain = Literal[
    "narrative_warfare", "deepfake_campaign", "astroturfing",
    "algorithmic_amplification", "influence_operation", "epistemic_attack",
    "memory_hole", "perception_hacking",
]

@dataclass
class InfoIntegrityInput:
    target_id: str
    threat_domain: ThreatDomain
    region: str
    disinformation_exposure_rate: float        # higher = worse
    source_credibility_score: float
    narrative_coherence_score: float
    deepfake_detection_capability: float
    echo_chamber_penetration: float            # higher = worse
    adversarial_bot_density: float             # higher = worse
    information_decay_velocity: float          # higher = worse
    fact_checking_coverage: float
    cognitive_bias_exploitation_risk: float    # higher = worse
    media_literacy_score: float
    counter_narrative_strength: float
    epistemic_resilience_score: float
    institutional_trust_level: float
    cross_source_verification_rate: float
    manipulation_detection_latency: float      # higher = worse
    information_sovereignty_score: float
    strategic_communication_clarity: float


class CognitiveWarfareEngine:

    # ── sub-scores (0–100, higher = worse) ──────────────────────────────────

    @staticmethod
    def _exposure_score(inp: InfoIntegrityInput) -> float:
        """Weight 0.30 — disinformation_exposure_rate, echo_chamber_penetration, adversarial_bot_density (all higher=worse)"""
        s = 0.0
        # disinformation_exposure_rate
        if   inp.disinformation_exposure_rate >= 0.70: s += 40
        elif inp.disinformation_exposure_rate >= 0.45: s += 22
        elif inp.disinformation_exposure_rate >= 0.25: s += 8
        # echo_chamber_penetration
        if   inp.echo_chamber_penetration >= 0.70: s += 35
        elif inp.echo_chamber_penetration >= 0.45: s += 18
        elif inp.echo_chamber_penetration >= 0.25: s += 6
        # adversarial_bot_density
        if   inp.adversarial_bot_density >= 0.65: s += 25
        elif inp.adversarial_bot_density >= 0.40: s += 12
        return min(s, 100.0)

    @staticmethod
    def _detection_score(inp: InfoIntegrityInput) -> float:
        """Weight 0.25 — deepfake_detection_capability(inv), fact_checking_coverage(inv), cross_source_verification_rate(inv)"""
        s = 0.0
        # deepfake_detection_capability — LOW = worse
        if   inp.deepfake_detection_capability <= 0.25: s += 40
        elif inp.deepfake_detection_capability <= 0.50: s += 22
        elif inp.deepfake_detection_capability <= 0.70: s += 8
        # fact_checking_coverage — LOW = worse
        if   inp.fact_checking_coverage <= 0.25: s += 35
        elif inp.fact_checking_coverage <= 0.50: s += 18
        elif inp.fact_checking_coverage <= 0.70: s += 6
        # cross_source_verification_rate — LOW = worse
        if   inp.cross_source_verification_rate <= 0.30: s += 25
        elif inp.cross_source_verification_rate <= 0.55: s += 12
        return min(s, 100.0)

    @staticmethod
    def _resilience_score(inp: InfoIntegrityInput) -> float:
        """Weight 0.25 — epistemic_resilience_score(inv), media_literacy_score(inv), counter_narrative_strength(inv)"""
        s = 0.0
        # epistemic_resilience_score — LOW = worse
        if   inp.epistemic_resilience_score <= 0.25: s += 40
        elif inp.epistemic_resilience_score <= 0.50: s += 22
        elif inp.epistemic_resilience_score <= 0.70: s += 8
        # media_literacy_score — LOW = worse
        if   inp.media_literacy_score <= 0.25: s += 35
        elif inp.media_literacy_score <= 0.50: s += 18
        elif inp.media_literacy_score <= 0.70: s += 6
        # counter_narrative_strength — LOW = worse
        if   inp.counter_narrative_strength <= 0.30: s += 25
        elif inp.counter_narrative_strength <= 0.55: s += 12
        return min(s, 100.0)

    @staticmethod
    def _sovereignty_score(inp: InfoIntegrityInput) -> float:
        """Weight 0.20 — information_sovereignty_score(inv), institutional_trust_level(inv), manipulation_detection_latency(higher=worse)"""
        s = 0.0
        # information_sovereignty_score — LOW = worse
        if   inp.information_sovereignty_score <= 0.25: s += 40
        elif inp.information_sovereignty_score <= 0.50: s += 22
        elif inp.information_sovereignty_score <= 0.70: s += 8
        # institutional_trust_level — LOW = worse
        if   inp.institutional_trust_level <= 0.25: s += 35
        elif inp.institutional_trust_level <= 0.50: s += 18
        elif inp.institutional_trust_level <= 0.70: s += 6
        # manipulation_detection_latency — HIGH = worse
        if   inp.manipulation_detection_latency >= 0.70: s += 25
        elif inp.manipulation_detection_latency >= 0.45: s += 12
        return min(s, 100.0)

    @staticmethod
    def _composite(exp: float, det: float, res: float, sov: float) -> float:
        return min(round(exp * 0.30 + det * 0.25 + res * 0.25 + sov * 0.20, 2), 100.0)

    @staticmethod
    def _pattern(inp: InfoIntegrityInput) -> str:
        if inp.disinformation_exposure_rate >= 0.7 and inp.narrative_coherence_score <= 0.3:
            return "narrative_capture"
        if inp.deepfake_detection_capability <= 0.3 and inp.threat_domain in ("deepfake_campaign", "perception_hacking"):
            return "deepfake_assault"
        if inp.epistemic_resilience_score <= 0.25 and inp.cognitive_bias_exploitation_risk >= 0.7:
            return "epistemic_collapse"
        if inp.adversarial_bot_density >= 0.7 and inp.echo_chamber_penetration >= 0.65:
            return "bot_swarm_attack"
        if inp.institutional_trust_level <= 0.3 and inp.source_credibility_score <= 0.35:
            return "trust_erosion"
        return "none"

    @staticmethod
    def _risk(comp: float) -> str:
        if comp >= 60: return "critical"
        if comp >= 40: return "high"
        if comp >= 20: return "moderate"
        return "low"

    @staticmethod
    def _severity(comp: float) -> str:
        if comp >= 60: return "captured"
        if comp >= 40: return "compromised"
        if comp >= 20: return "resistant"
        return "sovereign"

    @staticmethod
    def _action(risk: str, pattern: str) -> str:
        if risk == "critical":
            return "cognitive_defense_protocol" if pattern == "narrative_capture" else "narrative_counterstrike"
        if risk == "high":
            return "bot_neutralization" if pattern == "bot_swarm_attack" else "epistemic_reinforcement"
        if risk == "moderate":
            return "info_monitoring"
        return "no_action"

    @staticmethod
    def _signal(inp: InfoIntegrityInput, pattern: str, comp: float) -> str:
        if comp < 20:
            return (
                "Intégrité informationnelle forte — souveraineté épistémique active, "
                "faible exposition aux menaces cognitives"
            )
        labels: dict[str, str] = {
            "narrative_capture":  "Capture narrative",
            "deepfake_assault":   "Assaut deepfake",
            "epistemic_collapse": "Effondrement épistémique",
            "bot_swarm_attack":   "Attaque essaim de bots",
            "trust_erosion":      "Érosion de confiance",
        }
        label = labels.get(pattern, pattern.replace("_", " "))
        return (
            f"{label} — exposition désinformation {inp.disinformation_exposure_rate:.2f} "
            f"— densité bots {inp.adversarial_bot_density:.2f} "
            f"— résilience épistémique {inp.epistemic_resilience_score:.2f} "
            f"— composite {round(comp)}"
        )

    def _assess(self, inp: InfoIntegrityInput) -> tuple[dict, float]:
        exp = self._exposure_score(inp)
        det = self._detection_score(inp)
        res = self._resilience_score(inp)
        sov = self._sovereignty_score(inp)
        comp = self._composite(exp, det, res, sov)
        pat  = self._pattern(inp)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        act  = self._action(risk, pat)
        sig  = self._signal(inp, pat, comp)
        vuln = min(round(comp / 100 * (1 - inp.epistemic_resilience_score + 0.01) * 10, 2), 10.0)
        d = {
            "target_id":                     inp.target_id,
            "region":                        inp.region,
            "threat_domain":                 inp.threat_domain,
            "cognitive_warfare_risk":        risk,
            "warfare_pattern":               pat,
            "cognitive_severity":            sev,
            "recommended_action":            act,
            "exposure_score":                exp,
            "detection_score":               det,
            "resilience_score":              res,
            "sovereignty_score":             sov,
            "cognitive_warfare_composite":   comp,
            "has_active_threat":             comp >= 40 or inp.disinformation_exposure_rate >= 0.6 or inp.adversarial_bot_density >= 0.6,
            "requires_immediate_response":   comp >= 25 or inp.manipulation_detection_latency >= 0.65 or inp.epistemic_resilience_score <= 0.3,
            "cognitive_warfare_signal":      sig,
        }
        return d, vuln

    def assess_batch(self, inputs: list[InfoIntegrityInput]) -> list[dict]:
        results = []
        for inp in inputs:
            d, vuln = self._assess(inp)
            d["estimated_cognitive_vulnerability_index"] = vuln
            results.append(d)
        return results

    def summary(self, results: list[dict]) -> dict:
        n = len(results)
        risk_counts: dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        t_comp = t_exp = t_det = t_res = t_sov = t_vuln = 0.0
        active_threat_count = 0
        immediate_response_count = 0
        for r in results:
            risk_counts[r["cognitive_warfare_risk"]]   = risk_counts.get(r["cognitive_warfare_risk"], 0) + 1
            pattern_counts[r["warfare_pattern"]]       = pattern_counts.get(r["warfare_pattern"], 0) + 1
            severity_counts[r["cognitive_severity"]]   = severity_counts.get(r["cognitive_severity"], 0) + 1
            action_counts[r["recommended_action"]]     = action_counts.get(r["recommended_action"], 0) + 1
            t_comp += r["cognitive_warfare_composite"]
            t_exp  += r["exposure_score"]
            t_det  += r["detection_score"]
            t_res  += r["resilience_score"]
            t_sov  += r["sovereignty_score"]
            t_vuln += r.get("estimated_cognitive_vulnerability_index", 0.0)
            if r["has_active_threat"]:           active_threat_count += 1
            if r["requires_immediate_response"]: immediate_response_count += 1
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_cognitive_warfare_composite":      round(t_comp / n, 1),
            "active_threat_count":                  active_threat_count,
            "immediate_response_count":             immediate_response_count,
            "avg_exposure_score":                   round(t_exp / n, 1),
            "avg_detection_score":                  round(t_det / n, 1),
            "avg_resilience_score":                 round(t_res / n, 1),
            "avg_sovereignty_score":                round(t_sov / n, 1),
            "avg_estimated_cognitive_vulnerability_index": round(t_vuln / n, 2),
        }
