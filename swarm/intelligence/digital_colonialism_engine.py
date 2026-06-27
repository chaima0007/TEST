"""
Module 371 — Digital Colonialism & Tech Sovereignty Intelligence Engine
Monitors digital colonialism threats — platform imperial capture,
data extraction empires, AI dependency traps, surveillance export
colonialism, and structural digital divides across global markets.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DigitalColonialismInput:
    entity_id: str
    tech_domain: str
    region: str
    # 17 float fields 0-1
    platform_dependency_ratio: float
    data_extraction_intensity: float
    algorithmic_bias_export: float
    digital_infrastructure_control: float
    content_moderation_dominance: float
    payment_system_capture: float
    cloud_sovereignty_erosion: float
    AI_dependency_trap: float
    surveillance_export_risk: float
    economic_value_extraction: float
    local_industry_displacement: float
    regulatory_capture_risk: float
    digital_divide_amplification: float
    language_digital_exclusion: float
    tech_debt_accumulation: float
    data_localization_failure: float
    geopolitical_tech_leverage: float


@dataclass
class DigitalColonialismResult:
    entity_id: str
    tech_domain: str
    region: str
    dependency_score: float
    extraction_score: float
    sovereignty_score: float
    exclusion_score: float
    composite_score: float
    risk_level: str
    colonial_pattern: str
    severity: str
    recommended_action: str
    signal: str
    platform_dependency_ratio: float
    data_localization_failure: float

    def to_dict(self) -> Dict:
        return {
            "entity_id":                    self.entity_id,
            "tech_domain":                  self.tech_domain,
            "region":                       self.region,
            "dependency_score":             self.dependency_score,
            "extraction_score":             self.extraction_score,
            "sovereignty_score":            self.sovereignty_score,
            "exclusion_score":              self.exclusion_score,
            "composite_score":              self.composite_score,
            "risk_level":                   self.risk_level,
            "colonial_pattern":             self.colonial_pattern,
            "severity":                     self.severity,
            "recommended_action":           self.recommended_action,
            "signal":                       self.signal,
            "platform_dependency_ratio":    self.platform_dependency_ratio,
            "data_localization_failure":    self.data_localization_failure,
        }


class DigitalColonialismEngine:
    def __init__(self) -> None:
        self._results: List[DigitalColonialismResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _dependency_score(self, i: DigitalColonialismInput) -> float:
        s = (
            i.platform_dependency_ratio * 0.40
            + i.AI_dependency_trap * 0.35
            + i.payment_system_capture * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _extraction_score(self, i: DigitalColonialismInput) -> float:
        s = (
            i.data_extraction_intensity * 0.40
            + i.economic_value_extraction * 0.35
            + i.local_industry_displacement * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _sovereignty_score(self, i: DigitalColonialismInput) -> float:
        s = (
            i.cloud_sovereignty_erosion * 0.40
            + i.digital_infrastructure_control * 0.35
            + i.regulatory_capture_risk * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _exclusion_score(self, i: DigitalColonialismInput) -> float:
        s = (
            i.digital_divide_amplification * 0.40
            + i.language_digital_exclusion * 0.35
            + i.tech_debt_accumulation * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _composite(self, dep: float, ext: float, sov: float, exc: float) -> float:
        return min(round(dep * 0.30 + ext * 0.25 + sov * 0.25 + exc * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity / action / signal                                   #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> str:
        if c >= 60: return "critical"
        if c >= 40: return "high"
        if c >= 20: return "moderate"
        return "low"

    def _severity(self, c: float) -> str:
        if c >= 60: return "colonialisme_numérique_systémique"
        if c >= 40: return "crise_souveraineté_tech_majeure"
        if c >= 20: return "erosion_autonomie_numérique"
        return "souveraineté_tech_relative"

    def _action(self, c: float) -> str:
        if c >= 60: return "intervention_décolonisation_numérique_urgente"
        if c >= 40: return "stratégie_souveraineté_tech_accélérée"
        if c >= 20: return "renforcement_industrie_numérique_locale"
        return "veille_souveraineté_numérique_continue"

    def _signal(self, c: float) -> str:
        if c >= 60:
            return "🔴 Colonialisme numérique systémique — souveraineté tech compromise"
        if c >= 40:
            return "🟠 Crise souveraineté technologique majeure détectée"
        if c >= 20:
            return "🟡 Érosion autonomie numérique active"
        return "🟢 Souveraineté tech relativement maintenue"

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: DigitalColonialismInput) -> str:
        if i.platform_dependency_ratio > 0.85 and i.economic_value_extraction > 0.80:
            return "platform_imperial_capture"
        if i.data_extraction_intensity > 0.85 and i.data_localization_failure > 0.80:
            return "data_extraction_empire"
        if i.AI_dependency_trap > 0.85 and i.cloud_sovereignty_erosion > 0.80:
            return "AI_dependency_trap_system"
        if i.surveillance_export_risk > 0.80 and i.algorithmic_bias_export > 0.75:
            return "surveillance_export_colonialism"
        if i.digital_divide_amplification > 0.80 and i.language_digital_exclusion > 0.75:
            return "digital_divide_structural"
        return "none"

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: DigitalColonialismInput) -> DigitalColonialismResult:
        dep  = self._dependency_score(i)
        ext  = self._extraction_score(i)
        sov  = self._sovereignty_score(i)
        exc  = self._exclusion_score(i)
        comp = self._composite(dep, ext, sov, exc)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        act  = self._action(comp)
        pat  = self._pattern(i)
        sig  = self._signal(comp)
        result = DigitalColonialismResult(
            entity_id=i.entity_id,
            tech_domain=i.tech_domain,
            region=i.region,
            dependency_score=dep,
            extraction_score=ext,
            sovereignty_score=sov,
            exclusion_score=exc,
            composite_score=comp,
            risk_level=risk,
            colonial_pattern=pat,
            severity=sev,
            recommended_action=act,
            signal=sig,
            platform_dependency_ratio=i.platform_dependency_ratio,
            data_localization_failure=i.data_localization_failure,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[DigitalColonialismInput]) -> List[DigitalColonialismResult]:
        return [self.assess(i) for i in inputs]

    def summary(self, results: List[Dict] = None) -> Dict:
        data = results if results is not None else [r.to_dict() for r in self._results]
        if not data:
            return {
                "module_id":                                371,
                "module_name":                              "Digital Colonialism & Tech Sovereignty Intelligence Engine",
                "total":                                    0,
                "critical":                                 0,
                "high":                                     0,
                "moderate":                                 0,
                "low":                                      0,
                "avg_composite":                            0.0,
                "pattern_distribution":                     {},
                "risk_distribution":                        {},
                "severity_distribution":                    {},
                "action_distribution":                      {},
                "avg_estimated_digital_colonial_index":     0.0,
            }
        n = len(data)
        pat_dist:  Dict[str, int] = {}
        risk_dist: Dict[str, int] = {}
        sev_dist:  Dict[str, int] = {}
        act_dist:  Dict[str, int] = {}
        total_comp = 0.0
        critical = high = moderate = low = 0
        for r in data:
            pat_dist[r["colonial_pattern"]]      = pat_dist.get(r["colonial_pattern"], 0) + 1
            risk_dist[r["risk_level"]]           = risk_dist.get(r["risk_level"], 0) + 1
            sev_dist[r["severity"]]              = sev_dist.get(r["severity"], 0) + 1
            act_dist[r["recommended_action"]]    = act_dist.get(r["recommended_action"], 0) + 1
            total_comp += r["composite_score"]
            if r["risk_level"] == "critical":        critical  += 1
            elif r["risk_level"] == "high":          high      += 1
            elif r["risk_level"] == "moderate":      moderate  += 1
            else:                                    low       += 1
        avg_composite = round(total_comp / n, 1)
        return {
            "module_id":                                371,
            "module_name":                              "Digital Colonialism & Tech Sovereignty Intelligence Engine",
            "total":                                    n,
            "critical":                                 critical,
            "high":                                     high,
            "moderate":                                 moderate,
            "low":                                      low,
            "avg_composite":                            avg_composite,
            "pattern_distribution":                     pat_dist,
            "risk_distribution":                        risk_dist,
            "severity_distribution":                    sev_dist,
            "action_distribution":                      act_dist,
            "avg_estimated_digital_colonial_index":     round(avg_composite / 100 * 10, 2),
        }
