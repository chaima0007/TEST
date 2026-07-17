"""Module 344 — Psychopolitics & Mass Psychology Intelligence Engine"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class PsychopoliticsInput:
    entity_id: str
    political_domain: str
    region: str
    # 17 float fields (0-1)
    mass_anxiety_political_exploitation: float
    tribal_identity_weaponization: float
    emotional_contagion_amplification: float
    fear_architecture_deployment: float
    political_gaslighting_prevalence: float
    collective_trauma_manipulation: float
    populist_neuroscience_targeting: float
    scapegoating_mechanism_intensity: float
    authoritarian_personality_activation: float
    political_PTSD_induction: float
    cult_of_personality_formation: float
    manufactured_crisis_normalization: float
    democratic_disillusionment_weaponization: float
    political_nostalgia_manipulation: float
    shame_guilt_political_leverage: float
    mass_helplessness_cultivation: float
    political_identity_addiction: float


class PsychopoliticsEngine:
    MODULE_ID = 344
    MODULE_NAME = "Psychopolitics & Mass Psychology Intelligence Engine"

    def analyze(self, inp: PsychopoliticsInput) -> dict:
        # 4 sub-scores
        manipulation_score = (
            inp.mass_anxiety_political_exploitation * 0.4
            + inp.fear_architecture_deployment * 0.35
            + inp.political_gaslighting_prevalence * 0.25
        ) * 100

        identity_score = (
            inp.tribal_identity_weaponization * 0.4
            + inp.political_identity_addiction * 0.35
            + inp.cult_of_personality_formation * 0.25
        ) * 100

        trauma_score = (
            inp.collective_trauma_manipulation * 0.4
            + inp.political_PTSD_induction * 0.35
            + inp.mass_helplessness_cultivation * 0.25
        ) * 100

        structural_score = (
            inp.authoritarian_personality_activation * 0.4
            + inp.democratic_disillusionment_weaponization * 0.35
            + inp.manufactured_crisis_normalization * 0.25
        ) * 100

        composite_score = (
            manipulation_score * 0.30
            + identity_score * 0.25
            + trauma_score * 0.25
            + structural_score * 0.20
        )

        # Risk level
        if composite_score >= 60:
            risk_level = "critical"
        elif composite_score >= 40:
            risk_level = "high"
        elif composite_score >= 20:
            risk_level = "moderate"
        else:
            risk_level = "low"

        # 5 patterns
        psycho_pattern = "none"
        if inp.mass_anxiety_political_exploitation >= 0.70 and inp.emotional_contagion_amplification >= 0.65:
            psycho_pattern = "mass_psychosis_politics"
        elif inp.tribal_identity_weaponization >= 0.70 and inp.scapegoating_mechanism_intensity >= 0.65:
            psycho_pattern = "tribal_warfare_activation"
        elif inp.collective_trauma_manipulation >= 0.70 and inp.political_PTSD_induction >= 0.65:
            psycho_pattern = "trauma_based_control"
        elif inp.cult_of_personality_formation >= 0.70 and inp.authoritarian_personality_activation >= 0.65:
            psycho_pattern = "authoritarian_personality_cult"
        elif inp.democratic_disillusionment_weaponization >= 0.70 and inp.mass_helplessness_cultivation >= 0.65:
            psycho_pattern = "democratic_psychological_collapse"

        # Severity
        severity_map = {
            "critical": "psychopolitique_systémique_avancée",
            "high": "manipulation_masse_majeure",
            "moderate": "exploitation_psychologique_structurelle",
            "low": "politique_psychologie_contenue",
        }
        severity = severity_map[risk_level]

        # Recommended action
        action_map = {
            "critical": "résilience_psychologique_collective_urgente",
            "high": "contre-mesures_manipulation_psychopolitique",
            "moderate": "renforcement_pensée_critique_citoyenne",
            "low": "veille_psychopolitique_continue",
        }
        recommended_action = action_map[risk_level]

        # Signal (French)
        signal_map = {
            "critical": "🔴 Psychopolitique systémique — manipulation masse critique",
            "high": "🟠 Manipulation masse majeure détectée",
            "moderate": "🟡 Exploitation psychologique structurelle active",
            "low": "🟢 Psychologie politique relativement saine",
        }
        signal = signal_map[risk_level]

        return {
            "entity_id": inp.entity_id,
            "political_domain": inp.political_domain,
            "region": inp.region,
            "manipulation_score": round(manipulation_score, 2),
            "identity_score": round(identity_score, 2),
            "trauma_score": round(trauma_score, 2),
            "structural_score": round(structural_score, 2),
            "composite_score": round(composite_score, 2),
            "risk_level": risk_level,
            "psycho_pattern": psycho_pattern,
            "severity": severity,
            "recommended_action": recommended_action,
            "signal": signal,
            "mass_anxiety_political_exploitation": inp.mass_anxiety_political_exploitation,
            "democratic_disillusionment_weaponization": inp.democratic_disillusionment_weaponization,
        }

    def to_dict(self, inp: PsychopoliticsInput) -> dict:
        result = self.analyze(inp)
        assert len(result) == 15, f"to_dict must return exactly 15 keys, got {len(result)}"
        return result

    def summary(self, inputs: list[PsychopoliticsInput]) -> dict:
        results = [self.analyze(inp) for inp in inputs]
        total = len(results)

        risk_counts = {"critical": 0, "high": 0, "moderate": 0, "low": 0}
        severity_dist = {}
        action_dist = {}
        pattern_dist = {}
        composites = []

        for r in results:
            risk_counts[r["risk_level"]] += 1
            severity_dist[r["severity"]] = severity_dist.get(r["severity"], 0) + 1
            action_dist[r["recommended_action"]] = action_dist.get(r["recommended_action"], 0) + 1
            pattern_dist[r["psycho_pattern"]] = pattern_dist.get(r["psycho_pattern"], 0) + 1
            composites.append(r["composite_score"])

        avg_composite = round(sum(composites) / total, 2) if total > 0 else 0.0
        avg_estimated_psychopolitics_index = round(avg_composite / 100 * 10, 2)

        result = {
            "module_id": self.MODULE_ID,
            "module_name": self.MODULE_NAME,
            "total_entities": total,
            "critical_count": risk_counts["critical"],
            "high_count": risk_counts["high"],
            "moderate_count": risk_counts["moderate"],
            "low_count": risk_counts["low"],
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_dist,
            "risk_distribution": risk_counts,
            "severity_distribution": severity_dist,
            "action_distribution": action_dist,
            "avg_estimated_psychopolitics_index": avg_estimated_psychopolitics_index,
        }
        assert len(result) == 13, f"summary must return exactly 13 keys, got {len(result)}"
        return result
