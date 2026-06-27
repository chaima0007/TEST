from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class DataAssetInput:
    asset_id: str
    data_domain: str  # legacy_archive / sensor_exhaust / shadow_it / unstructured_text / video_metadata / IoT_stream / behavioral_trace / contractual_data
    region: str
    data_discovery_coverage: float          # 0.0–1.0
    monetization_potential: float           # 0.0–1.0
    governance_gap_severity: float          # higher = worse
    data_quality_latency: float             # higher = worse
    dark_data_ratio: float                  # higher = worse
    ai_readiness_score: float               # 0.0–1.0
    cross_departmental_silos: float         # higher = worse
    metadata_completeness: float            # 0.0–1.0
    regulatory_dark_risk: float             # higher = worse
    hidden_value_estimate: float            # 0.0–1.0
    extraction_complexity: float            # higher = worse
    data_lineage_clarity: float             # 0.0–1.0
    retention_policy_compliance: float      # 0.0–1.0
    privacy_exposure_risk: float            # higher = worse
    integration_readiness: float            # 0.0–1.0
    analyst_accessibility_score: float      # 0.0–1.0
    insight_generation_velocity: float      # 0.0–1.0


class DarkDataIntelligenceEngine:
    # ---------- sub-score helpers ----------

    @staticmethod
    def _governance_score(a: DataAssetInput) -> float:
        """Higher raw = worse governance. Score 0–100 (higher = more risk)."""
        raw = (a.governance_gap_severity + a.regulatory_dark_risk + a.privacy_exposure_risk) / 3.0
        return round(raw * 100, 2)

    @staticmethod
    def _discovery_score(a: DataAssetInput) -> float:
        """dark_data_ratio (bad), data_discovery_coverage inverted (low coverage = bad),
        cross_departmental_silos (bad). Higher = more risk."""
        inv_coverage = 1.0 - a.data_discovery_coverage
        raw = (a.dark_data_ratio + inv_coverage + a.cross_departmental_silos) / 3.0
        return round(raw * 100, 2)

    @staticmethod
    def _quality_score(a: DataAssetInput) -> float:
        """data_quality_latency (bad), metadata_completeness inverted, data_lineage_clarity inverted.
        Higher = more risk."""
        inv_metadata = 1.0 - a.metadata_completeness
        inv_lineage  = 1.0 - a.data_lineage_clarity
        raw = (a.data_quality_latency + inv_metadata + inv_lineage) / 3.0
        return round(raw * 100, 2)

    @staticmethod
    def _value_score(a: DataAssetInput) -> float:
        """extraction_complexity (bad), ai_readiness_score inverted, integration_readiness inverted.
        Higher = more risk / burial."""
        inv_ai    = 1.0 - a.ai_readiness_score
        inv_integ = 1.0 - a.integration_readiness
        raw = (a.extraction_complexity + inv_ai + inv_integ) / 3.0
        return round(raw * 100, 2)

    @staticmethod
    def _composite(gov: float, disc: float, qual: float, val: float) -> float:
        return round(min(gov * 0.30 + disc * 0.25 + qual * 0.25 + val * 0.20, 100.0), 2)

    # ---------- classification helpers ----------

    @staticmethod
    def _dark_pattern(a: DataAssetInput) -> str:
        if a.governance_gap_severity >= 0.70 and a.regulatory_dark_risk >= 0.65:
            return "governance_blindspot"
        if a.privacy_exposure_risk >= 0.70 and a.regulatory_dark_risk >= 0.60:
            return "compliance_exposure"
        if a.dark_data_ratio >= 0.70 and a.hidden_value_estimate >= 0.60:
            return "value_burial"
        if a.cross_departmental_silos >= 0.65 and a.data_discovery_coverage <= 0.40:
            return "silo_fragmentation"
        if a.data_quality_latency >= 0.70 and a.metadata_completeness <= 0.35:
            return "data_rot"
        return "none"

    @staticmethod
    def _severity(composite: float) -> str:
        if composite >= 60:
            return "critical_exposure"
        if composite >= 40:
            return "obscured"
        if composite >= 20:
            return "emerging"
        return "illuminated"

    @staticmethod
    def _risk(composite: float) -> str:
        if composite >= 60:
            return "critical"
        if composite >= 40:
            return "high"
        if composite >= 20:
            return "moderate"
        return "low"

    @staticmethod
    def _action(risk: str, pattern: str) -> str:
        if risk == "critical":
            if pattern in ("governance_blindspot",):
                return "data_governance_emergency"
            if pattern in ("compliance_exposure",):
                return "privacy_audit"
            return "data_governance_emergency"
        if risk == "high":
            if pattern in ("value_burial",):
                return "dark_data_excavation"
            if pattern in ("silo_fragmentation",):
                return "silo_bridge"
            return "dark_data_excavation"
        if risk == "moderate":
            return "data_monitoring"
        return "no_action"

    @staticmethod
    def _signal(a: DataAssetInput, pattern: str, composite: float) -> str:
        if composite < 20:
            return (
                "Données bien gouvernées — actifs découverts, valeur accessible, "
                "conformité assurée, siloes réduits"
            )
        labels: Dict[str, str] = {
            "governance_blindspot": "Zone aveugle de gouvernance",
            "value_burial":         "Enfouissement de valeur cachée",
            "silo_fragmentation":   "Fragmentation en silos",
            "compliance_exposure":  "Exposition réglementaire",
            "data_rot":             "Dégradation des données",
        }
        label = labels.get(pattern, pattern.replace("_", " "))
        return (
            f"{label} — ratio données sombres {round(a.dark_data_ratio * 100)}% — "
            f"risque gouvernance {round(a.governance_gap_severity * 100)}% — "
            f"valeur cachée estimée {round(a.hidden_value_estimate * 100)}% — "
            f"composite {round(composite)}"
        )

    # ---------- public API ----------

    def _assess_one(self, a: DataAssetInput) -> Dict[str, Any]:
        gov  = self._governance_score(a)
        disc = self._discovery_score(a)
        qual = self._quality_score(a)
        val  = self._value_score(a)
        comp = self._composite(gov, disc, qual, val)
        pat  = self._dark_pattern(a)
        sev  = self._severity(comp)
        r    = self._risk(comp)
        act  = self._action(r, pat)
        return {
            "asset_id":                       a.asset_id,
            "data_domain":                    a.data_domain,
            "region":                         a.region,
            "dark_data_risk":                 r,
            "dark_data_pattern":              pat,
            "dark_data_severity":             sev,
            "recommended_action":             act,
            "governance_score":               gov,
            "discovery_score":                disc,
            "quality_score":                  qual,
            "value_score":                    val,
            "dark_data_composite":            comp,
            "has_hidden_value_signal":        (
                comp >= 40
                or a.dark_data_ratio >= 0.55
                or a.hidden_value_estimate >= 0.60
                or a.data_discovery_coverage <= 0.35
            ),
            "requires_immediate_governance":  (
                comp >= 25
                or a.governance_gap_severity >= 0.60
                or a.regulatory_dark_risk >= 0.55
                or a.privacy_exposure_risk >= 0.60
            ),
            "estimated_hidden_value_index":   round(
                min(comp / 100 * (a.hidden_value_estimate + 0.01) * 10, 10.0), 2
            ),
            "dark_data_signal":               self._signal(a, pat, comp),
        }

    def assess_batch(self, assets: List[DataAssetInput]) -> List[Dict[str, Any]]:
        return [self._assess_one(a) for a in assets]

    def summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        t_gov = t_disc = t_qual = t_val = t_comp = t_hvi = 0.0
        hv_count = ig_count = 0

        for r in results:
            rc[r["dark_data_risk"]]      = rc.get(r["dark_data_risk"], 0)      + 1
            pc[r["dark_data_pattern"]]   = pc.get(r["dark_data_pattern"], 0)   + 1
            sc[r["dark_data_severity"]]  = sc.get(r["dark_data_severity"], 0)  + 1
            ac[r["recommended_action"]]  = ac.get(r["recommended_action"], 0)  + 1
            t_gov  += r["governance_score"]
            t_disc += r["discovery_score"]
            t_qual += r["quality_score"]
            t_val  += r["value_score"]
            t_comp += r["dark_data_composite"]
            t_hvi  += r["estimated_hidden_value_index"]
            if r["has_hidden_value_signal"]:
                hv_count += 1
            if r["requires_immediate_governance"]:
                ig_count += 1

        n = len(results) or 1
        return {
            "total":                           len(results),
            "risk_counts":                     rc,
            "pattern_counts":                  pc,
            "severity_counts":                 sc,
            "action_counts":                   ac,
            "avg_dark_data_composite":         round(t_comp / n, 1),
            "hidden_value_signal_count":       hv_count,
            "immediate_governance_count":      ig_count,
            "avg_governance_score":            round(t_gov  / n, 1),
            "avg_discovery_score":             round(t_disc / n, 1),
            "avg_quality_score":               round(t_qual / n, 1),
            "avg_value_score":                 round(t_val  / n, 1),
            "avg_estimated_hidden_value_index": round(t_hvi / n, 2),
        }

    def to_dict(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Return exactly 15 keys for a single assessed result."""
        return {
            "asset_id":                      result["asset_id"],
            "data_domain":                   result["data_domain"],
            "region":                        result["region"],
            "dark_data_risk":                result["dark_data_risk"],
            "dark_data_pattern":             result["dark_data_pattern"],
            "dark_data_severity":            result["dark_data_severity"],
            "recommended_action":            result["recommended_action"],
            "governance_score":              result["governance_score"],
            "discovery_score":              result["discovery_score"],
            "quality_score":                 result["quality_score"],
            "value_score":                   result["value_score"],
            "dark_data_composite":           result["dark_data_composite"],
            "has_hidden_value_signal":       result["has_hidden_value_signal"],
            "estimated_hidden_value_index":  result["estimated_hidden_value_index"],
            "dark_data_signal":              result["dark_data_signal"],
        }
