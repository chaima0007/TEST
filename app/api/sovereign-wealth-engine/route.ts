import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SWF-001 — critical, critical_asset_foreign_capture (infra>0.85, tech>0.80)
  {
    entity_id: "SWF-001", fund_type: "stabilisation", region: "MENA",
    aum_concentration: 0.92, governance_transparency: 0.15, political_independence: 0.08,
    investment_opacity: 0.80, critical_infrastructure_acquisition: 0.90, media_influence_buying: 0.70,
    real_estate_strategic_purchase: 0.78, tech_sector_control: 0.85, sovereign_debt_leverage: 0.72,
    democracy_index_target: 0.68, esg_compliance: 0.10, wealth_distribution_domestic: 0.15,
    fossil_fuel_dependence: 0.88, diversification_quality: 0.12, accountability_mechanism: 0.10,
    international_treaty_compliance: 0.12, geopolitical_alignment: 0.80,
  },
  // SWF-002 — critical, democratic_influence_buying (media>0.85, democracy_idx>0.80)
  {
    entity_id: "SWF-002", fund_type: "développement", region: "APAC",
    aum_concentration: 0.85, governance_transparency: 0.12, political_independence: 0.08,
    investment_opacity: 0.82, critical_infrastructure_acquisition: 0.70, media_influence_buying: 0.90,
    real_estate_strategic_purchase: 0.75, tech_sector_control: 0.72, sovereign_debt_leverage: 0.80,
    democracy_index_target: 0.85, esg_compliance: 0.08, wealth_distribution_domestic: 0.12,
    fossil_fuel_dependence: 0.75, diversification_quality: 0.10, accountability_mechanism: 0.08,
    international_treaty_compliance: 0.10, geopolitical_alignment: 0.82,
  },
  // SWF-003 — critical, opacity_money_laundering_nexus (opacity>0.85, 1-governance>0.80)
  {
    entity_id: "SWF-003", fund_type: "réserve", region: "EMEA",
    aum_concentration: 0.88, governance_transparency: 0.10, political_independence: 0.05,
    investment_opacity: 0.92, critical_infrastructure_acquisition: 0.72, media_influence_buying: 0.65,
    real_estate_strategic_purchase: 0.80, tech_sector_control: 0.68, sovereign_debt_leverage: 0.75,
    democracy_index_target: 0.70, esg_compliance: 0.05, wealth_distribution_domestic: 0.10,
    fossil_fuel_dependence: 0.82, diversification_quality: 0.08, accountability_mechanism: 0.08,
    international_treaty_compliance: 0.10, geopolitical_alignment: 0.78,
  },
  // SWF-004 — high, resource_curse_recycling (fossil>0.80, wealth_dist<0.25)
  {
    entity_id: "SWF-004", fund_type: "stabilisation", region: "MENA",
    aum_concentration: 0.55, governance_transparency: 0.35, political_independence: 0.30,
    investment_opacity: 0.52, critical_infrastructure_acquisition: 0.48, media_influence_buying: 0.50,
    real_estate_strategic_purchase: 0.55, tech_sector_control: 0.45, sovereign_debt_leverage: 0.55,
    democracy_index_target: 0.52, esg_compliance: 0.20, wealth_distribution_domestic: 0.18,
    fossil_fuel_dependence: 0.88, diversification_quality: 0.25, accountability_mechanism: 0.30,
    international_treaty_compliance: 0.35, geopolitical_alignment: 0.55,
  },
  // SWF-005 — high, geoeconomic_coercion_tool (debt_leverage>0.80, geo_align>0.75)
  {
    entity_id: "SWF-005", fund_type: "développement", region: "APAC",
    aum_concentration: 0.35, governance_transparency: 0.52, political_independence: 0.45,
    investment_opacity: 0.38, critical_infrastructure_acquisition: 0.32, media_influence_buying: 0.30,
    real_estate_strategic_purchase: 0.45, tech_sector_control: 0.28, sovereign_debt_leverage: 0.85,
    democracy_index_target: 0.35, esg_compliance: 0.38, wealth_distribution_domestic: 0.50,
    fossil_fuel_dependence: 0.40, diversification_quality: 0.48, accountability_mechanism: 0.52,
    international_treaty_compliance: 0.55, geopolitical_alignment: 0.82,
  },
  // SWF-006 — moderate, none
  {
    entity_id: "SWF-006", fund_type: "épargne", region: "NOAM",
    aum_concentration: 0.30, governance_transparency: 0.60, political_independence: 0.55,
    investment_opacity: 0.32, critical_infrastructure_acquisition: 0.28, media_influence_buying: 0.30,
    real_estate_strategic_purchase: 0.28, tech_sector_control: 0.25, sovereign_debt_leverage: 0.30,
    democracy_index_target: 0.28, esg_compliance: 0.55, wealth_distribution_domestic: 0.60,
    fossil_fuel_dependence: 0.35, diversification_quality: 0.58, accountability_mechanism: 0.60,
    international_treaty_compliance: 0.62, geopolitical_alignment: 0.30,
  },
  // SWF-007 — low, none
  {
    entity_id: "SWF-007", fund_type: "épargne", region: "NOAM",
    aum_concentration: 0.10, governance_transparency: 0.88, political_independence: 0.85,
    investment_opacity: 0.10, critical_infrastructure_acquisition: 0.08, media_influence_buying: 0.10,
    real_estate_strategic_purchase: 0.08, tech_sector_control: 0.08, sovereign_debt_leverage: 0.10,
    democracy_index_target: 0.08, esg_compliance: 0.85, wealth_distribution_domestic: 0.88,
    fossil_fuel_dependence: 0.10, diversification_quality: 0.88, accountability_mechanism: 0.88,
    international_treaty_compliance: 0.90, geopolitical_alignment: 0.10,
  },
  // SWF-008 — low, none
  {
    entity_id: "SWF-008", fund_type: "retraite", region: "EMEA",
    aum_concentration: 0.12, governance_transparency: 0.85, political_independence: 0.82,
    investment_opacity: 0.12, critical_infrastructure_acquisition: 0.10, media_influence_buying: 0.10,
    real_estate_strategic_purchase: 0.10, tech_sector_control: 0.10, sovereign_debt_leverage: 0.10,
    democracy_index_target: 0.10, esg_compliance: 0.82, wealth_distribution_domestic: 0.85,
    fossil_fuel_dependence: 0.12, diversification_quality: 0.85, accountability_mechanism: 0.85,
    international_treaty_compliance: 0.88, geopolitical_alignment: 0.12,
  },
];

type SWFInput = typeof MOCK_ENTITIES[0];

function concentrationScore(e: SWFInput): number {
  return Math.round((e.aum_concentration * 0.4 + e.critical_infrastructure_acquisition * 0.35 + e.tech_sector_control * 0.25) * 100 * 100) / 100;
}
function opacityScore(e: SWFInput): number {
  return Math.round((e.investment_opacity * 0.4 + (1.0 - e.governance_transparency) * 0.35 + e.media_influence_buying * 0.25) * 100 * 100) / 100;
}
function geopoliticalScore(e: SWFInput): number {
  return Math.round((e.geopolitical_alignment * 0.4 + e.sovereign_debt_leverage * 0.35 + e.real_estate_strategic_purchase * 0.25) * 100 * 100) / 100;
}
function accountabilityScore(e: SWFInput): number {
  return Math.round(((1.0 - e.accountability_mechanism) * 0.4 + (1.0 - e.international_treaty_compliance) * 0.35 + e.democracy_index_target * 0.25) * 100 * 100) / 100;
}
function compositeScore(con: number, opa: number, geo: number, acc: number): number {
  return Math.round((con * 0.30 + opa * 0.25 + geo * 0.25 + acc * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function sovereignPattern(e: SWFInput): string {
  if (e.critical_infrastructure_acquisition > 0.85 && e.tech_sector_control > 0.80) return "critical_asset_foreign_capture";
  if (e.media_influence_buying > 0.85 && e.democracy_index_target > 0.80) return "democratic_influence_buying";
  if (e.investment_opacity > 0.85 && (1.0 - e.governance_transparency) > 0.80) return "opacity_money_laundering_nexus";
  if (e.fossil_fuel_dependence > 0.80 && e.wealth_distribution_domestic < 0.25) return "resource_curse_recycling";
  if (e.sovereign_debt_leverage > 0.80 && e.geopolitical_alignment > 0.75) return "geoeconomic_coercion_tool";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "menace_souveraineté_systémique_critique";
  if (composite >= 40) return "risque_géopolitique_majeur_détecté";
  if (composite >= 20) return "influence_opaque_structurelle";
  return "fonds_souverain_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_contrôle_actifs_stratégiques";
  if (risk === "high") return "audit_géopolitique_accéléré_fonds_souverain";
  if (risk === "moderate") return "renforcement_transparence_gouvernance_fonds";
  return "veille_fonds_souverain_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Menace souveraineté systémique — capture d'actifs critiques en cours";
  if (risk === "high") return "🟠 Risque géopolitique majeur détecté — influence opaque élevée";
  if (risk === "moderate") return "🟡 Influence opaque structurelle — surveillance renforcée requise";
  return "🟢 Fonds souverain sous surveillance standard";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const con  = concentrationScore(e);
      const opa  = opacityScore(e);
      const geo  = geopoliticalScore(e);
      const acc  = accountabilityScore(e);
      const comp = compositeScore(con, opa, geo, acc);
      const risk = riskLevel(comp);
      const pat  = sovereignPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:                               e.entity_id,
        fund_type:                               e.fund_type,
        region:                                  e.region,
        concentration_score:                     con,
        opacity_score:                           opa,
        geopolitical_score:                      geo,
        accountability_score:                    acc,
        composite_score:                         comp,
        risk_level:                              risk,
        sovereign_pattern:                       pat,
        severity:                                sev,
        recommended_action:                      action,
        signal:                                  sig,
        aum_concentration:                       e.aum_concentration,
        geopolitical_alignment:                  e.geopolitical_alignment,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tCon = 0, tOpa = 0, tGeo = 0, tAcc = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]             = (risk_distribution[ent.risk_level]             || 0) + 1;
      pattern_distribution[ent.sovereign_pattern]   = (pattern_distribution[ent.sovereign_pattern]   || 0) + 1;
      severity_distribution[ent.severity]           = (severity_distribution[ent.severity]           || 0) + 1;
      action_distribution[ent.recommended_action]   = (action_distribution[ent.recommended_action]   || 0) + 1;
      tCon  += ent.concentration_score;
      tOpa  += ent.opacity_score;
      tGeo  += ent.geopolitical_score;
      tAcc  += ent.accountability_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite       = Math.round(tComp / n * 10) / 10;
    const avgConcentration   = Math.round(tCon  / n * 10) / 10;

    const summary = {
      module_id:                              432,
      module_name:                            "Fonds Souverains & Pouvoir Géopolitique Intelligence Engine",
      total:                                  n,
      critical:                               criticalCount,
      high:                                   highCount,
      moderate:                               moderateCount,
      low:                                    lowCount,
      avg_composite:                          avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_sovereign_wealth_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_concentration: avgConcentration }, "sovereign-wealth-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/sovereign-wealth-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "sovereign-wealth-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "sovereign-wealth-engine"),
      { status: 502 }
    );
  }
}
