import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ASSETS = [
  // DS-001 brand_identity EMEA — critical identity_theft
  { asset_id:"DS-001", asset_domain:"brand_identity",      region:"EMEA",  identity_integrity_score:0.15, brand_impersonation_risk:0.92, ip_ownership_clarity:0.70, data_residency_compliance:0.65, platform_dependency_risk:0.45, algorithmic_attribution_score:0.72, proprietary_data_exposure_risk:0.55, digital_footprint_control:0.30, access_credential_security:0.35, content_authenticity_score:0.20, deepfake_vulnerability_index:0.75, namespace_ownership_score:0.60, cross_border_jurisdiction_risk:0.55, succession_plan_coverage:0.40, legal_protection_strength:0.55, monitoring_coverage_score:0.42, incident_response_readiness:0.28 },
  // DS-002 intellectual_property NAMER — low
  { asset_id:"DS-002", asset_domain:"intellectual_property", region:"NAMER", identity_integrity_score:0.92, brand_impersonation_risk:0.08, ip_ownership_clarity:0.95, data_residency_compliance:0.95, platform_dependency_risk:0.10, algorithmic_attribution_score:0.92, proprietary_data_exposure_risk:0.05, digital_footprint_control:0.92, access_credential_security:0.95, content_authenticity_score:0.90, deepfake_vulnerability_index:0.08, namespace_ownership_score:0.95, cross_border_jurisdiction_risk:0.05, succession_plan_coverage:0.90, legal_protection_strength:0.95, monitoring_coverage_score:0.92, incident_response_readiness:0.92 },
  // DS-003 data_sovereignty APAC — high data_leakage
  { asset_id:"DS-003", asset_domain:"data_sovereignty",    region:"APAC",  identity_integrity_score:0.60, brand_impersonation_risk:0.30, ip_ownership_clarity:0.65, data_residency_compliance:0.28, platform_dependency_risk:0.50, algorithmic_attribution_score:0.60, proprietary_data_exposure_risk:0.72, digital_footprint_control:0.45, access_credential_security:0.55, content_authenticity_score:0.58, deepfake_vulnerability_index:0.35, namespace_ownership_score:0.62, cross_border_jurisdiction_risk:0.68, succession_plan_coverage:0.50, legal_protection_strength:0.48, monitoring_coverage_score:0.40, incident_response_readiness:0.42 },
  // DS-004 platform_identity LATAM — low
  { asset_id:"DS-004", asset_domain:"platform_identity",   region:"LATAM", identity_integrity_score:0.88, brand_impersonation_risk:0.12, ip_ownership_clarity:0.85, data_residency_compliance:0.88, platform_dependency_risk:0.15, algorithmic_attribution_score:0.85, proprietary_data_exposure_risk:0.10, digital_footprint_control:0.85, access_credential_security:0.88, content_authenticity_score:0.85, deepfake_vulnerability_index:0.12, namespace_ownership_score:0.90, cross_border_jurisdiction_risk:0.12, succession_plan_coverage:0.82, legal_protection_strength:0.88, monitoring_coverage_score:0.85, incident_response_readiness:0.88 },
  // DS-005 algorithm_ownership EMEA — critical ip_expropriation
  { asset_id:"DS-005", asset_domain:"algorithm_ownership", region:"EMEA",  identity_integrity_score:0.55, brand_impersonation_risk:0.48, ip_ownership_clarity:0.12, data_residency_compliance:0.60, platform_dependency_risk:0.55, algorithmic_attribution_score:0.10, proprietary_data_exposure_risk:0.60, digital_footprint_control:0.40, access_credential_security:0.45, content_authenticity_score:0.50, deepfake_vulnerability_index:0.45, namespace_ownership_score:0.15, cross_border_jurisdiction_risk:0.65, succession_plan_coverage:0.30, legal_protection_strength:0.22, monitoring_coverage_score:0.35, incident_response_readiness:0.30 },
  // DS-006 creative_authorship MEA — moderate
  { asset_id:"DS-006", asset_domain:"creative_authorship", region:"MEA",   identity_integrity_score:0.68, brand_impersonation_risk:0.32, ip_ownership_clarity:0.62, data_residency_compliance:0.58, platform_dependency_risk:0.42, algorithmic_attribution_score:0.65, proprietary_data_exposure_risk:0.38, digital_footprint_control:0.60, access_credential_security:0.65, content_authenticity_score:0.62, deepfake_vulnerability_index:0.38, namespace_ownership_score:0.60, cross_border_jurisdiction_risk:0.40, succession_plan_coverage:0.55, legal_protection_strength:0.58, monitoring_coverage_score:0.55, incident_response_readiness:0.55 },
  // DS-007 biometric_data NAMER — high deepfake_attack
  { asset_id:"DS-007", asset_domain:"biometric_data",      region:"NAMER", identity_integrity_score:0.50, brand_impersonation_risk:0.45, ip_ownership_clarity:0.68, data_residency_compliance:0.70, platform_dependency_risk:0.40, algorithmic_attribution_score:0.65, proprietary_data_exposure_risk:0.50, digital_footprint_control:0.42, access_credential_security:0.48, content_authenticity_score:0.40, deepfake_vulnerability_index:0.82, namespace_ownership_score:0.65, cross_border_jurisdiction_risk:0.38, succession_plan_coverage:0.45, legal_protection_strength:0.52, monitoring_coverage_score:0.42, incident_response_readiness:0.38 },
  // DS-008 digital_estate APAC — low
  { asset_id:"DS-008", asset_domain:"digital_estate",      region:"APAC",  identity_integrity_score:0.90, brand_impersonation_risk:0.10, ip_ownership_clarity:0.88, data_residency_compliance:0.92, platform_dependency_risk:0.12, algorithmic_attribution_score:0.88, proprietary_data_exposure_risk:0.08, digital_footprint_control:0.90, access_credential_security:0.92, content_authenticity_score:0.88, deepfake_vulnerability_index:0.10, namespace_ownership_score:0.92, cross_border_jurisdiction_risk:0.08, succession_plan_coverage:0.88, legal_protection_strength:0.92, monitoring_coverage_score:0.90, incident_response_readiness:0.92 },
];

type Asset = typeof MOCK_ASSETS[0];

function identityScore(a: Asset): number {
  const raw = (
    (1 - a.brand_impersonation_risk) * 100 / 3
    + (1 - a.deepfake_vulnerability_index) * 100 / 3
    + a.identity_integrity_score * 100 / 3
  );
  return Math.min(Math.round((1 - raw / 100) * 100 * 100) / 100, 100);
}
function ownershipScore(a: Asset): number {
  const raw = (
    a.ip_ownership_clarity * 100 / 3
    + a.algorithmic_attribution_score * 100 / 3
    + a.namespace_ownership_score * 100 / 3
  );
  return Math.min(Math.round((1 - raw / 100) * 100 * 100) / 100, 100);
}
function protectionScore(a: Asset): number {
  const raw = (
    a.proprietary_data_exposure_risk * 100 / 3
    + a.platform_dependency_risk * 100 / 3
    + (1 - a.legal_protection_strength) * 100 / 3
  );
  return Math.min(Math.round(raw * 100) / 100, 100);
}
function resilienceScore(a: Asset): number {
  const raw = (
    (1 - a.incident_response_readiness) * 100 / 3
    + (1 - a.monitoring_coverage_score) * 100 / 3
    + (1 - a.access_credential_security) * 100 / 3
  );
  return Math.min(Math.round(raw * 100) / 100, 100);
}
function composite(id: number, own: number, prot: number, res: number): number {
  return Math.min(Math.round((id * 0.30 + own * 0.25 + prot * 0.25 + res * 0.20) * 100) / 100, 100);
}
function sovereigntyRisk(c: number): string {
  if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low";
}
function sovereigntySeverity(c: number): string {
  if (c >= 60) return "compromised"; if (c >= 40) return "threatened"; if (c >= 20) return "monitored"; return "sovereign";
}
function sovereigntyPattern(a: Asset): string {
  if (a.brand_impersonation_risk >= 0.65 || a.identity_integrity_score <= 0.35) return "identity_theft";
  if (a.ip_ownership_clarity <= 0.35 || a.algorithmic_attribution_score <= 0.35) return "ip_expropriation";
  if (a.platform_dependency_risk >= 0.65) return "platform_capture";
  if (a.proprietary_data_exposure_risk >= 0.60 || a.data_residency_compliance <= 0.40) return "data_leakage";
  if (a.deepfake_vulnerability_index >= 0.60) return "deepfake_attack";
  return "none";
}
function recommendedActions(risk: string): string[] {
  if (risk === "critical") return ["emergency_identity_lock", "legal_injunction"];
  if (risk === "high")     return ["ip_enforcement", "platform_exit_strategy"];
  if (risk === "moderate") return ["sovereignty_monitoring"];
  return ["no_action"];
}
function breachIndex(a: Asset, comp: number): number {
  return Math.round(Math.min(comp / 100 * (a.brand_impersonation_risk + a.proprietary_data_exposure_risk) / 2 * 10, 10.0) * 100) / 100;
}
function sovereigntySignal(a: Asset, pat: string, comp: number): string {
  if (comp < 20) {
    return "Souveraineté numérique maîtrisée — identité protégée, propriété intellectuelle sécurisée, données souveraines";
  }
  const labels: Record<string, string> = {
    identity_theft:   "Vol d'identité numérique",
    ip_expropriation: "Expropriation propriété intellectuelle",
    platform_capture: "Capture par la plateforme",
    data_leakage:     "Fuite de données propriétaires",
    deepfake_attack:  "Attaque deepfake détectée",
  };
  const label = labels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — impersonation ${a.brand_impersonation_risk.toFixed(2)} — clarté IP ${a.ip_ownership_clarity.toFixed(2)} — exposition données ${a.proprietary_data_exposure_risk.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const assets = MOCK_ASSETS.map(a => {
      const id_s = identityScore(a), own_s = ownershipScore(a), prot_s = protectionScore(a), res_s = resilienceScore(a);
      const comp = composite(id_s, own_s, prot_s, res_s);
      const risk = sovereigntyRisk(comp), sev = sovereigntySeverity(comp), pat = sovereigntyPattern(a);
      const acts = recommendedActions(risk);
      return {
        asset_id: a.asset_id, asset_domain: a.asset_domain, region: a.region,
        sovereignty_risk: risk, sovereignty_pattern: pat, sovereignty_severity: sev,
        recommended_actions: acts,
        identity_score: id_s, ownership_score: own_s, protection_score: prot_s, resilience_score: res_s,
        sovereignty_composite: comp,
        estimated_sovereignty_breach_index: breachIndex(a, comp),
        sovereignty_signal: sovereigntySignal(a, pat, comp),
        is_legally_actionable: risk === "critical" || risk === "high",
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tid=0, town=0, tprot=0, tres=0, tcomp=0, tbreach=0, compCnt=0, legalCnt=0;
    for (const asset of assets) {
      rc[asset.sovereignty_risk]     = (rc[asset.sovereignty_risk]||0)+1;
      pc[asset.sovereignty_pattern]  = (pc[asset.sovereignty_pattern]||0)+1;
      sc[asset.sovereignty_severity] = (sc[asset.sovereignty_severity]||0)+1;
      for (const act of asset.recommended_actions) { ac[act] = (ac[act]||0)+1; }
      tid    += asset.identity_score;
      town   += asset.ownership_score;
      tprot  += asset.protection_score;
      tres   += asset.resilience_score;
      tcomp  += asset.sovereignty_composite;
      tbreach += asset.estimated_sovereignty_breach_index;
      if (asset.sovereignty_severity === "compromised") compCnt++;
      if (asset.is_legally_actionable) legalCnt++;
    }
    const n = assets.length;
    return NextResponse.json(sealResponse({ assets, summary: {
      total: n,
      risk_counts: rc,
      pattern_counts: pc,
      severity_counts: sc,
      action_counts: ac,
      avg_sovereignty_composite: Math.round(tcomp/n*10)/10,
      compromised_count: compCnt,
      legal_action_count: legalCnt,
      avg_identity_score: Math.round(tid/n*10)/10,
      avg_ownership_score: Math.round(town/n*10)/10,
      avg_protection_score: Math.round(tprot/n*10)/10,
      avg_resilience_score: Math.round(tres/n*10)/10,
      avg_estimated_sovereignty_breach_index: Math.round(tbreach/n*100)/100,
    } as Record<string, unknown>}, "digital-sovereignty-engine") as Parameters<typeof NextResponse.json>[0]);
  }
  return NextResponse.json(sealResponse(await (await fetch(`${process.env.SWARM_API_URL}/digital-sovereignty-engine`)).json(), "digital-sovereignty-engine") as Parameters<typeof NextResponse.json>[0]);
}
