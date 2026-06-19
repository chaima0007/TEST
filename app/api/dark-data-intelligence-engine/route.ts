import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ASSETS = [
  // DDI-001 legacy_archive EMEA — critical governance_blindspot
  { asset_id:"DDI-001", data_domain:"legacy_archive",    region:"EMEA",  data_discovery_coverage:0.18, monetization_potential:0.55, governance_gap_severity:0.82, data_quality_latency:0.60, dark_data_ratio:0.78, ai_readiness_score:0.22, cross_departmental_silos:0.72, metadata_completeness:0.20, regulatory_dark_risk:0.80, hidden_value_estimate:0.62, extraction_complexity:0.70, data_lineage_clarity:0.18, retention_policy_compliance:0.22, privacy_exposure_risk:0.75, integration_readiness:0.20, analyst_accessibility_score:0.18, insight_generation_velocity:0.15 },
  // DDI-002 sensor_exhaust NAMER — low illuminated
  { asset_id:"DDI-002", data_domain:"sensor_exhaust",    region:"NAMER", data_discovery_coverage:0.92, monetization_potential:0.88, governance_gap_severity:0.10, data_quality_latency:0.08, dark_data_ratio:0.10, ai_readiness_score:0.90, cross_departmental_silos:0.12, metadata_completeness:0.92, regulatory_dark_risk:0.08, hidden_value_estimate:0.85, extraction_complexity:0.12, data_lineage_clarity:0.90, retention_policy_compliance:0.95, privacy_exposure_risk:0.08, integration_readiness:0.90, analyst_accessibility_score:0.92, insight_generation_velocity:0.88 },
  // DDI-003 shadow_it APAC — high value_burial
  { asset_id:"DDI-003", data_domain:"shadow_it",         region:"APAC",  data_discovery_coverage:0.35, monetization_potential:0.72, governance_gap_severity:0.52, data_quality_latency:0.48, dark_data_ratio:0.72, ai_readiness_score:0.30, cross_departmental_silos:0.55, metadata_completeness:0.38, regulatory_dark_risk:0.45, hidden_value_estimate:0.75, extraction_complexity:0.68, data_lineage_clarity:0.32, retention_policy_compliance:0.45, privacy_exposure_risk:0.50, integration_readiness:0.28, analyst_accessibility_score:0.30, insight_generation_velocity:0.28 },
  // DDI-004 unstructured_text LATAM — low emerging
  { asset_id:"DDI-004", data_domain:"unstructured_text", region:"LATAM", data_discovery_coverage:0.72, monetization_potential:0.65, governance_gap_severity:0.22, data_quality_latency:0.25, dark_data_ratio:0.28, ai_readiness_score:0.70, cross_departmental_silos:0.30, metadata_completeness:0.75, regulatory_dark_risk:0.20, hidden_value_estimate:0.60, extraction_complexity:0.30, data_lineage_clarity:0.72, retention_policy_compliance:0.80, privacy_exposure_risk:0.22, integration_readiness:0.68, analyst_accessibility_score:0.72, insight_generation_velocity:0.65 },
  // DDI-005 video_metadata EMEA — critical compliance_exposure
  { asset_id:"DDI-005", data_domain:"video_metadata",    region:"EMEA",  data_discovery_coverage:0.25, monetization_potential:0.48, governance_gap_severity:0.72, data_quality_latency:0.55, dark_data_ratio:0.65, ai_readiness_score:0.28, cross_departmental_silos:0.60, metadata_completeness:0.25, regulatory_dark_risk:0.78, hidden_value_estimate:0.45, extraction_complexity:0.65, data_lineage_clarity:0.22, retention_policy_compliance:0.28, privacy_exposure_risk:0.82, integration_readiness:0.25, analyst_accessibility_score:0.22, insight_generation_velocity:0.20 },
  // DDI-006 IoT_stream NAMER — moderate none
  { asset_id:"DDI-006", data_domain:"IoT_stream",        region:"NAMER", data_discovery_coverage:0.58, monetization_potential:0.55, governance_gap_severity:0.38, data_quality_latency:0.42, dark_data_ratio:0.45, ai_readiness_score:0.55, cross_departmental_silos:0.42, metadata_completeness:0.58, regulatory_dark_risk:0.35, hidden_value_estimate:0.50, extraction_complexity:0.45, data_lineage_clarity:0.55, retention_policy_compliance:0.60, privacy_exposure_risk:0.38, integration_readiness:0.52, analyst_accessibility_score:0.55, insight_generation_velocity:0.50 },
  // DDI-007 behavioral_trace APAC — high silo_fragmentation
  { asset_id:"DDI-007", data_domain:"behavioral_trace",  region:"APAC",  data_discovery_coverage:0.28, monetization_potential:0.68, governance_gap_severity:0.55, data_quality_latency:0.50, dark_data_ratio:0.60, ai_readiness_score:0.35, cross_departmental_silos:0.78, metadata_completeness:0.35, regulatory_dark_risk:0.48, hidden_value_estimate:0.65, extraction_complexity:0.55, data_lineage_clarity:0.38, retention_policy_compliance:0.42, privacy_exposure_risk:0.52, integration_readiness:0.32, analyst_accessibility_score:0.30, insight_generation_velocity:0.28 },
  // DDI-008 contractual_data MEA — critical data_rot
  { asset_id:"DDI-008", data_domain:"contractual_data",  region:"MEA",   data_discovery_coverage:0.20, monetization_potential:0.40, governance_gap_severity:0.65, data_quality_latency:0.82, dark_data_ratio:0.72, ai_readiness_score:0.18, cross_departmental_silos:0.62, metadata_completeness:0.18, regulatory_dark_risk:0.60, hidden_value_estimate:0.38, extraction_complexity:0.72, data_lineage_clarity:0.15, retention_policy_compliance:0.20, privacy_exposure_risk:0.65, integration_readiness:0.18, analyst_accessibility_score:0.15, insight_generation_velocity:0.12 },
];

type Asset = typeof MOCK_ASSETS[0];

function governanceScore(a: Asset): number {
  const raw = (a.governance_gap_severity + a.regulatory_dark_risk + a.privacy_exposure_risk) / 3.0;
  return Math.round(raw * 100 * 100) / 100;
}
function discoveryScore(a: Asset): number {
  const invCoverage = 1.0 - a.data_discovery_coverage;
  const raw = (a.dark_data_ratio + invCoverage + a.cross_departmental_silos) / 3.0;
  return Math.round(raw * 100 * 100) / 100;
}
function qualityScore(a: Asset): number {
  const invMetadata = 1.0 - a.metadata_completeness;
  const invLineage  = 1.0 - a.data_lineage_clarity;
  const raw = (a.data_quality_latency + invMetadata + invLineage) / 3.0;
  return Math.round(raw * 100 * 100) / 100;
}
function valueScore(a: Asset): number {
  const invAi    = 1.0 - a.ai_readiness_score;
  const invInteg = 1.0 - a.integration_readiness;
  const raw = (a.extraction_complexity + invAi + invInteg) / 3.0;
  return Math.round(raw * 100 * 100) / 100;
}
function composite(gov: number, disc: number, qual: number, val: number): number {
  return Math.min(Math.round((gov * 0.30 + disc * 0.25 + qual * 0.25 + val * 0.20) * 100) / 100, 100);
}
function darkPattern(a: Asset): string {
  if (a.governance_gap_severity >= 0.70 && a.regulatory_dark_risk >= 0.65)       return "governance_blindspot";
  if (a.privacy_exposure_risk  >= 0.70 && a.regulatory_dark_risk >= 0.60)        return "compliance_exposure";
  if (a.dark_data_ratio        >= 0.70 && a.hidden_value_estimate >= 0.60)       return "value_burial";
  if (a.cross_departmental_silos >= 0.65 && a.data_discovery_coverage <= 0.40)   return "silo_fragmentation";
  if (a.data_quality_latency   >= 0.70 && a.metadata_completeness <= 0.35)       return "data_rot";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "critical_exposure"; if (c >= 40) return "obscured"; if (c >= 20) return "emerging"; return "illuminated"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "governance_blindspot") return "data_governance_emergency";
    if (p === "compliance_exposure")  return "privacy_audit";
    return "data_governance_emergency";
  }
  if (r === "high") {
    if (p === "value_burial")       return "dark_data_excavation";
    if (p === "silo_fragmentation") return "silo_bridge";
    return "dark_data_excavation";
  }
  if (r === "moderate") return "data_monitoring";
  return "no_action";
}
function signal(a: Asset, pat: string, comp: number): string {
  if (comp < 20) return "Données bien gouvernées — actifs découverts, valeur accessible, conformité assurée, siloes réduits";
  const labels: Record<string,string> = {
    governance_blindspot: "Zone aveugle de gouvernance",
    value_burial:         "Enfouissement de valeur cachée",
    silo_fragmentation:   "Fragmentation en silos",
    compliance_exposure:  "Exposition réglementaire",
    data_rot:             "Dégradation des données",
  };
  const label = labels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — ratio données sombres ${Math.round(a.dark_data_ratio*100)}% — risque gouvernance ${Math.round(a.governance_gap_severity*100)}% — valeur cachée estimée ${Math.round(a.hidden_value_estimate*100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const assets = MOCK_ASSETS.map(a => {
      const gov  = governanceScore(a), disc = discoveryScore(a), qual = qualityScore(a), val = valueScore(a);
      const comp = composite(gov, disc, qual, val), pat = darkPattern(a), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        asset_id: a.asset_id, data_domain: a.data_domain, region: a.region,
        dark_data_risk: r, dark_data_pattern: pat, dark_data_severity: sev, recommended_action: act,
        governance_score: gov, discovery_score: disc, quality_score: qual, value_score: val,
        dark_data_composite: comp,
        has_hidden_value_signal: comp >= 40 || a.dark_data_ratio >= 0.55 || a.hidden_value_estimate >= 0.60 || a.data_discovery_coverage <= 0.35,
        requires_immediate_governance: comp >= 25 || a.governance_gap_severity >= 0.60 || a.regulatory_dark_risk >= 0.55 || a.privacy_exposure_risk >= 0.60,
        estimated_hidden_value_index: Math.min(Math.round(comp/100*(a.hidden_value_estimate+0.01)*10*100)/100, 10.0),
        dark_data_signal: signal(a, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tgov=0, tdisc=0, tqual=0, tval=0, tcomp=0, thvi=0, hvC=0, igC=0;
    for (const res of assets) {
      rc[res.dark_data_risk]      = (rc[res.dark_data_risk]      || 0) + 1;
      pc[res.dark_data_pattern]   = (pc[res.dark_data_pattern]   || 0) + 1;
      sc[res.dark_data_severity]  = (sc[res.dark_data_severity]  || 0) + 1;
      ac[res.recommended_action]  = (ac[res.recommended_action]  || 0) + 1;
      tgov  += res.governance_score; tdisc += res.discovery_score;
      tqual += res.quality_score;    tval  += res.value_score;
      tcomp += res.dark_data_composite; thvi += res.estimated_hidden_value_index;
      if (res.has_hidden_value_signal)       hvC++;
      if (res.requires_immediate_governance) igC++;
    }
    const n = assets.length;
    return NextResponse.json({ assets, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_dark_data_composite:          Math.round(tcomp / n * 10) / 10,
      hidden_value_signal_count:        hvC,
      immediate_governance_count:       igC,
      avg_governance_score:             Math.round(tgov  / n * 10) / 10,
      avg_discovery_score:              Math.round(tdisc / n * 10) / 10,
      avg_quality_score:                Math.round(tqual / n * 10) / 10,
      avg_value_score:                  Math.round(tval  / n * 10) / 10,
      avg_estimated_hidden_value_index: Math.round(thvi  / n * 100) / 100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/dark-data-intelligence-engine`)).json());
}
