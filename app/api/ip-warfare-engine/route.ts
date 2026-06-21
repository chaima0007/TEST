import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // IPW-001 — state_IP_espionage_campaign + patent_monopoly_capture → critical
  {
    id: "IPW-001", ip_domain: "patents_trade_secrets", region: "APAC",
    patent_trolling_scale: 0.82,
    state_IP_theft_intensity: 0.90,
    standard_essential_patent_abuse: 0.78,
    pharmaceutical_evergreening: 0.70,
    AI_patent_monopolization: 0.88,
    trade_secret_theft: 0.86,
    copyright_maximalism_harm: 0.72,
    WIPO_governance_capture: 0.68,
    developing_nation_IP_exclusion: 0.72,
    technology_transfer_blockade: 0.70,
    innovation_suppression_via_patents: 0.84,
    open_source_patent_attack: 0.78,
    geopolitical_IP_weaponization: 0.75,
    patent_litigation_cost_barrier: 0.72,
    generic_medicine_access_block: 0.68,
    technology_dependency_IP: 0.70,
    digital_content_monopoly: 0.74,
  },
  // IPW-002 — pharmaceutical_access_blockade → critical
  {
    id: "IPW-002", ip_domain: "pharmaceutical_patents", region: "NOAM",
    patent_trolling_scale: 0.75,
    state_IP_theft_intensity: 0.70,
    standard_essential_patent_abuse: 0.72,
    pharmaceutical_evergreening: 0.92,
    AI_patent_monopolization: 0.74,
    trade_secret_theft: 0.68,
    copyright_maximalism_harm: 0.70,
    WIPO_governance_capture: 0.68,
    developing_nation_IP_exclusion: 0.72,
    technology_transfer_blockade: 0.70,
    innovation_suppression_via_patents: 0.72,
    open_source_patent_attack: 0.68,
    geopolitical_IP_weaponization: 0.72,
    patent_litigation_cost_barrier: 0.75,
    generic_medicine_access_block: 0.88,
    technology_dependency_IP: 0.72,
    digital_content_monopoly: 0.70,
  },
  // IPW-003 — geopolitical_IP_warfare → high
  {
    id: "IPW-003", ip_domain: "technology_transfer", region: "EMEA",
    patent_trolling_scale: 0.55,
    state_IP_theft_intensity: 0.60,
    standard_essential_patent_abuse: 0.52,
    pharmaceutical_evergreening: 0.50,
    AI_patent_monopolization: 0.55,
    trade_secret_theft: 0.58,
    copyright_maximalism_harm: 0.50,
    WIPO_governance_capture: 0.60,
    developing_nation_IP_exclusion: 0.55,
    technology_transfer_blockade: 0.82,
    innovation_suppression_via_patents: 0.52,
    open_source_patent_attack: 0.50,
    geopolitical_IP_weaponization: 0.85,
    patent_litigation_cost_barrier: 0.55,
    generic_medicine_access_block: 0.52,
    technology_dependency_IP: 0.58,
    digital_content_monopoly: 0.50,
  },
  // IPW-004 — global_south_IP_exclusion → high
  {
    id: "IPW-004", ip_domain: "global_south_access", region: "SSA",
    patent_trolling_scale: 0.52,
    state_IP_theft_intensity: 0.50,
    standard_essential_patent_abuse: 0.55,
    pharmaceutical_evergreening: 0.58,
    AI_patent_monopolization: 0.52,
    trade_secret_theft: 0.50,
    copyright_maximalism_harm: 0.55,
    WIPO_governance_capture: 0.80,
    developing_nation_IP_exclusion: 0.85,
    technology_transfer_blockade: 0.58,
    innovation_suppression_via_patents: 0.55,
    open_source_patent_attack: 0.52,
    geopolitical_IP_weaponization: 0.60,
    patent_litigation_cost_barrier: 0.72,
    generic_medicine_access_block: 0.68,
    technology_dependency_IP: 0.70,
    digital_content_monopoly: 0.52,
  },
  // IPW-005 — patent_monopoly_capture → high
  {
    id: "IPW-005", ip_domain: "AI_patents", region: "NOAM",
    patent_trolling_scale: 0.60,
    state_IP_theft_intensity: 0.55,
    standard_essential_patent_abuse: 0.62,
    pharmaceutical_evergreening: 0.50,
    AI_patent_monopolization: 0.90,
    trade_secret_theft: 0.55,
    copyright_maximalism_harm: 0.58,
    WIPO_governance_capture: 0.55,
    developing_nation_IP_exclusion: 0.60,
    technology_transfer_blockade: 0.55,
    innovation_suppression_via_patents: 0.85,
    open_source_patent_attack: 0.62,
    geopolitical_IP_weaponization: 0.55,
    patent_litigation_cost_barrier: 0.68,
    generic_medicine_access_block: 0.52,
    technology_dependency_IP: 0.62,
    digital_content_monopoly: 0.60,
  },
  // IPW-006 — moderate risk, no patterns
  {
    id: "IPW-006", ip_domain: "copyright", region: "LATAM",
    patent_trolling_scale: 0.30,
    state_IP_theft_intensity: 0.28,
    standard_essential_patent_abuse: 0.32,
    pharmaceutical_evergreening: 0.30,
    AI_patent_monopolization: 0.28,
    trade_secret_theft: 0.30,
    copyright_maximalism_harm: 0.35,
    WIPO_governance_capture: 0.28,
    developing_nation_IP_exclusion: 0.32,
    technology_transfer_blockade: 0.30,
    innovation_suppression_via_patents: 0.28,
    open_source_patent_attack: 0.30,
    geopolitical_IP_weaponization: 0.32,
    patent_litigation_cost_barrier: 0.35,
    generic_medicine_access_block: 0.30,
    technology_dependency_IP: 0.32,
    digital_content_monopoly: 0.35,
  },
  // IPW-007 — low risk
  {
    id: "IPW-007", ip_domain: "open_source", region: "EMEA",
    patent_trolling_scale: 0.10,
    state_IP_theft_intensity: 0.08,
    standard_essential_patent_abuse: 0.10,
    pharmaceutical_evergreening: 0.08,
    AI_patent_monopolization: 0.10,
    trade_secret_theft: 0.08,
    copyright_maximalism_harm: 0.12,
    WIPO_governance_capture: 0.08,
    developing_nation_IP_exclusion: 0.10,
    technology_transfer_blockade: 0.08,
    innovation_suppression_via_patents: 0.10,
    open_source_patent_attack: 0.12,
    geopolitical_IP_weaponization: 0.08,
    patent_litigation_cost_barrier: 0.10,
    generic_medicine_access_block: 0.08,
    technology_dependency_IP: 0.10,
    digital_content_monopoly: 0.12,
  },
  // IPW-008 — moderate risk, geopolitical_IP_warfare
  {
    id: "IPW-008", ip_domain: "semiconductor_IP", region: "APAC",
    patent_trolling_scale: 0.42,
    state_IP_theft_intensity: 0.40,
    standard_essential_patent_abuse: 0.45,
    pharmaceutical_evergreening: 0.38,
    AI_patent_monopolization: 0.42,
    trade_secret_theft: 0.40,
    copyright_maximalism_harm: 0.38,
    WIPO_governance_capture: 0.50,
    developing_nation_IP_exclusion: 0.45,
    technology_transfer_blockade: 0.78,
    innovation_suppression_via_patents: 0.40,
    open_source_patent_attack: 0.42,
    geopolitical_IP_weaponization: 0.82,
    patent_litigation_cost_barrier: 0.45,
    generic_medicine_access_block: 0.38,
    technology_dependency_IP: 0.48,
    digital_content_monopoly: 0.40,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function theftScore(e: Entity): number {
  const raw = (
    e.state_IP_theft_intensity
    + e.trade_secret_theft
    + e.patent_trolling_scale
    + e.open_source_patent_attack
  ) / 4 * 100;
  return Math.round(raw * 100) / 100;
}

function monopolyScore(e: Entity): number {
  const raw = (
    e.AI_patent_monopolization
    + e.standard_essential_patent_abuse
    + e.pharmaceutical_evergreening
    + e.copyright_maximalism_harm
    + e.digital_content_monopoly
    + e.innovation_suppression_via_patents
  ) / 6 * 100;
  return Math.round(raw * 100) / 100;
}

function accessScore(e: Entity): number {
  const raw = (
    e.developing_nation_IP_exclusion
    + e.generic_medicine_access_block
    + e.patent_litigation_cost_barrier
    + e.technology_dependency_IP
    + e.technology_transfer_blockade
  ) / 5 * 100;
  return Math.round(raw * 100) / 100;
}

function geopoliticalScore(e: Entity): number {
  const raw = (
    e.geopolitical_IP_weaponization
    + e.WIPO_governance_capture
  ) / 2 * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(theft: number, monopoly: number, access: number, geo: number): number {
  return Math.round((theft * 0.30 + monopoly * 0.25 + access * 0.25 + geo * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function patternsDetected(e: Entity): string[] {
  const patterns: string[] = [];
  if (e.state_IP_theft_intensity > 0.85 && e.trade_secret_theft > 0.80) patterns.push("state_IP_espionage_campaign");
  if (e.AI_patent_monopolization > 0.85 && e.innovation_suppression_via_patents > 0.80) patterns.push("patent_monopoly_capture");
  if (e.pharmaceutical_evergreening > 0.85 && e.generic_medicine_access_block > 0.80) patterns.push("pharmaceutical_access_blockade");
  if (e.geopolitical_IP_weaponization > 0.80 && e.technology_transfer_blockade > 0.75) patterns.push("geopolitical_IP_warfare");
  if (e.developing_nation_IP_exclusion > 0.80 && e.WIPO_governance_capture > 0.75) patterns.push("global_south_IP_exclusion");
  return patterns;
}

function severity(risk: string): string {
  if (risk === "critical") return "Critique";
  if (risk === "high")     return "Élevé";
  if (risk === "moderate") return "Modéré";
  return "Faible";
}

function actionRequired(risk: string): string {
  if (risk === "critical") return "Intervention immédiate requise";
  if (risk === "high")     return "Surveillance renforcée recommandée";
  if (risk === "moderate") return "Monitoring continu conseillé";
  return "Surveillance standard";
}

function signal(risk: string): string {
  if (risk === "critical") return "ALERTE ROUGE — Guerre IP active";
  if (risk === "high")     return "ALERTE ORANGE — Risque IP majeur";
  if (risk === "moderate") return "VIGILANCE — Tensions IP modérées";
  return "NORMAL — Situation IP stable";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const theft       = theftScore(e);
      const monopoly    = monopolyScore(e);
      const access      = accessScore(e);
      const geo         = geopoliticalScore(e);
      const comp        = compositeScore(theft, monopoly, access, geo);
      const risk        = riskLevel(comp);
      const patterns    = patternsDetected(e);
      const sev         = severity(risk);
      const action      = actionRequired(risk);
      const sig         = signal(risk);

      return {
        id:                    e.entity_id,
        ip_domain:                    e.ip_domain,
        region:                       e.region,
        theft_score:                  theft,
        monopoly_score:               monopoly,
        access_score:                 access,
        geopolitical_score:           geo,
        composite_score:              comp,
        risk_level:                   risk,
        patterns_detected:            patterns,
        severity:                     sev,
        action_required:              action,
        signal:                       sig,
        estimated_ip_warfare_index:   Math.round(comp / 100 * 10 * 100) / 100,
        metadata: {
          state_IP_theft_intensity:       e.state_IP_theft_intensity,
          geopolitical_IP_weaponization:  e.geopolitical_IP_weaponization,
          pharmaceutical_evergreening:    e.pharmaceutical_evergreening,
        },
      };
    });

    const risk_distribution: Record<string, number>    = {};
    const pattern_distribution: Record<string, number> = {};
    let tTheft = 0, tMonopoly = 0, tAccess = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level] = (risk_distribution[ent.risk_level] || 0) + 1;
      for (const pat of ent.patterns_detected) {
        pattern_distribution[pat] = (pattern_distribution[pat] || 0) + 1;
      }
      tTheft    += ent.theft_score;
      tMonopoly += ent.monopoly_score;
      tAccess   += ent.access_score;
      tComp     += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                      389,
      module_name:                    "Intellectual Property War & Patent Warfare Intelligence Engine",
      total:                          n,
      critical:                       criticalCount,
      high:                           highCount,
      moderate:                       moderateCount,
      low:                            lowCount,
      avg_composite:                  avgComposite,
      distributions: {
        risk:    risk_distribution,
        pattern: pattern_distribution,
      },
      avg_estimated_ip_warfare_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
      theft_avg:                      Math.round(tTheft / n * 10) / 10,
      monopoly_avg:                   Math.round(tMonopoly / n * 10) / 10,
      access_avg:                     Math.round(tAccess / n * 10) / 10,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "ip-warfare-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/ip-warfare-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "ip-warfare-engine"));
  } catch {
    return NextResponse.json(sealResponse({ error: "Upstream unavailable" }, "ip-warfare-engine"), { status: 502 });
  }
}
