from __future__ import annotations
from dataclasses import dataclass


@dataclass
class UXInput:
    interface_id: str
    ux_domain: str
    region: str
    cognitive_load_score: float
    task_completion_rate: float
    attention_retention_score: float
    error_recovery_efficiency: float
    adaptive_personalization_score: float
    emotional_resonance_index: float
    decision_fatigue_risk: float
    information_density_balance: float
    flow_state_facilitation: float
    sensory_overload_risk: float
    accessibility_compliance_score: float
    cross_modal_coherence: float
    feedback_loop_responsiveness: float
    user_agency_score: float
    cognitive_bias_mitigation: float
    engagement_depth_score: float
    neuroadaptive_accuracy: float


def _cognitive_score(u: UXInput) -> float:
    s = 0
    if   u.cognitive_load_score >= 0.75: s += 40
    elif u.cognitive_load_score >= 0.55: s += 22
    elif u.cognitive_load_score >= 0.40: s += 8
    if   u.decision_fatigue_risk >= 0.70: s += 35
    elif u.decision_fatigue_risk >= 0.50: s += 18
    elif u.decision_fatigue_risk >= 0.35: s += 6
    if   u.sensory_overload_risk >= 0.65: s += 25
    elif u.sensory_overload_risk >= 0.45: s += 12
    return min(float(s), 100.0)


def _engagement_score(u: UXInput) -> float:
    s = 0
    if   u.attention_retention_score <= 0.35: s += 40
    elif u.attention_retention_score <= 0.55: s += 22
    elif u.attention_retention_score <= 0.70: s += 8
    if   u.flow_state_facilitation <= 0.30: s += 35
    elif u.flow_state_facilitation <= 0.50: s += 18
    elif u.flow_state_facilitation <= 0.65: s += 6
    if   u.engagement_depth_score <= 0.35: s += 25
    elif u.engagement_depth_score <= 0.55: s += 12
    return min(float(s), 100.0)


def _adaptation_score(u: UXInput) -> float:
    s = 0
    if   u.adaptive_personalization_score <= 0.30: s += 40
    elif u.adaptive_personalization_score <= 0.50: s += 22
    elif u.adaptive_personalization_score <= 0.65: s += 8
    if   u.neuroadaptive_accuracy <= 0.30: s += 35
    elif u.neuroadaptive_accuracy <= 0.50: s += 18
    elif u.neuroadaptive_accuracy <= 0.65: s += 6
    if   u.feedback_loop_responsiveness <= 0.35: s += 25
    elif u.feedback_loop_responsiveness <= 0.55: s += 12
    return min(float(s), 100.0)


def _accessibility_score(u: UXInput) -> float:
    s = 0
    if   u.accessibility_compliance_score <= 0.50: s += 40
    elif u.accessibility_compliance_score <= 0.70: s += 22
    elif u.accessibility_compliance_score <= 0.80: s += 8
    if   u.user_agency_score <= 0.35: s += 35
    elif u.user_agency_score <= 0.55: s += 18
    elif u.user_agency_score <= 0.70: s += 6
    if   u.cognitive_bias_mitigation <= 0.30: s += 25
    elif u.cognitive_bias_mitigation <= 0.50: s += 12
    return min(float(s), 100.0)


def _composite(cog: float, eng: float, adp: float, acc: float) -> float:
    return min(round(cog * 0.30 + eng * 0.25 + adp * 0.25 + acc * 0.20, 2), 100.0)


def _pattern(u: UXInput) -> str:
    if u.cognitive_load_score >= 0.75 and u.sensory_overload_risk >= 0.65:
        return "cognitive_overload"
    if u.attention_retention_score <= 0.35 and u.flow_state_facilitation <= 0.40:
        return "attention_fragmentation"
    if u.adaptive_personalization_score <= 0.30 and u.neuroadaptive_accuracy <= 0.30:
        return "adaptation_failure"
    if u.engagement_depth_score <= 0.30 and u.task_completion_rate <= 0.40:
        return "engagement_collapse"
    if u.accessibility_compliance_score <= 0.50 and u.user_agency_score <= 0.40:
        return "accessibility_gap"
    return "none"


def _risk(c: float) -> str:
    if c >= 60: return "critical"
    if c >= 40: return "high"
    if c >= 20: return "moderate"
    return "low"


def _severity(c: float) -> str:
    if c >= 60: return "critical_load"
    if c >= 40: return "strained"
    if c >= 20: return "optimizing"
    return "neuroptimal"


def _action(risk: str, pat: str) -> str:
    if risk == "critical":
        return "ux_redesign" if pat == "cognitive_overload" else "load_shedding"
    if risk == "high":
        return "adaptation_sprint" if pat == "attention_fragmentation" else "accessibility_audit"
    if risk == "moderate":
        return "ux_monitoring"
    return "no_action"


def _signal(u: UXInput, pat: str, comp: float) -> str:
    if comp < 20:
        return "Interface neuroadaptive optimale — charge cognitive maîtrisée, engagement élevé, adaptation précise"
    labels: dict[str, str] = {
        "cognitive_overload":      "Surcharge cognitive",
        "attention_fragmentation": "Fragmentation attentionnelle",
        "adaptation_failure":      "Échec adaptation",
        "engagement_collapse":     "Effondrement engagement",
        "accessibility_gap":       "Lacune accessibilité",
    }
    label = labels.get(pat, pat.replace("_", " "))
    return (
        f"{label} — charge cog. {round(u.cognitive_load_score * 100)}%"
        f" — rétention att. {round(u.attention_retention_score * 100)}%"
        f" — adapt. neuro {round(u.neuroadaptive_accuracy * 100)}%"
        f" — composite {round(comp)}"
    )


def _assess(u: UXInput) -> dict:
    cog = _cognitive_score(u)
    eng = _engagement_score(u)
    adp = _adaptation_score(u)
    acc = _accessibility_score(u)
    comp = _composite(cog, eng, adp, acc)
    pat = _pattern(u)
    r = _risk(comp)
    sev = _severity(comp)
    act = _action(r, pat)
    return {
        "interface_id":         u.interface_id,
        "ux_domain":            u.ux_domain,
        "region":               u.region,
        "cognitive_score":      cog,
        "engagement_score":     eng,
        "adaptation_score":     adp,
        "accessibility_score":  acc,
        "ux_composite":         comp,
        "ux_risk":              r,
        "ux_pattern":           pat,
        "ux_severity":          sev,
        "recommended_action":   act,
        "has_load_signal":      (comp >= 40 or u.cognitive_load_score >= 0.60
                                 or u.sensory_overload_risk >= 0.55
                                 or u.decision_fatigue_risk >= 0.60),
        "requires_intervention": (comp >= 25 or u.adaptive_personalization_score <= 0.35
                                  or u.neuroadaptive_accuracy <= 0.35
                                  or u.accessibility_compliance_score <= 0.55),
        "ux_signal":            _signal(u, pat, comp),
    }


class NeuroadaptiveUXEngine:
    def assess_batch(self, inputs: list[UXInput]) -> list[dict]:
        return [_assess(u) for u in inputs]

    def summary(self, results: list[dict]) -> dict:
        rc: dict[str, int] = {}
        pc: dict[str, int] = {}
        sc: dict[str, int] = {}
        ac: dict[str, int] = {}
        t_comp = t_cog = t_eng = t_adp = t_acc = t_fri = 0.0
        load_c = interv_c = 0

        for r in results:
            rc[r["ux_risk"]]          = rc.get(r["ux_risk"], 0) + 1
            pc[r["ux_pattern"]]       = pc.get(r["ux_pattern"], 0) + 1
            sc[r["ux_severity"]]      = sc.get(r["ux_severity"], 0) + 1
            ac[r["recommended_action"]] = ac.get(r["recommended_action"], 0) + 1
            t_comp += r["ux_composite"]
            t_cog  += r["cognitive_score"]
            t_eng  += r["engagement_score"]
            t_adp  += r["adaptation_score"]
            t_acc  += r["accessibility_score"]
            fri = min(r["ux_composite"] / 100 * (1 - r["adaptation_score"] / 100 + 0.01) * 10, 10.0)
            t_fri += fri
            if r["has_load_signal"]:      load_c += 1
            if r["requires_intervention"]: interv_c += 1

        n = len(results) or 1
        return {
            "total":                              len(results),
            "risk_counts":                        rc,
            "pattern_counts":                     pc,
            "severity_counts":                    sc,
            "action_counts":                      ac,
            "avg_ux_composite":                   round(t_comp / n, 1),
            "load_signal_count":                  load_c,
            "intervention_required_count":        interv_c,
            "avg_cognitive_score":                round(t_cog / n, 1),
            "avg_engagement_score":               round(t_eng / n, 1),
            "avg_adaptation_score":               round(t_adp / n, 1),
            "avg_accessibility_score":            round(t_acc / n, 1),
            "avg_estimated_cognitive_friction_index": round(t_fri / n, 2),
        }
