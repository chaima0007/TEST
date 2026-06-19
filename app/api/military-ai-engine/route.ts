import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // MAI-001 critical / autonomous_kill_chain (alwd>=0.70, hcei>=0.65)
  { entity_id:"MAI-001", military_domain:"drone_warfare", region:"EMEA",
    autonomous_lethal_weapon_deployment:0.85, AI_command_authority_level:0.80, algorithmic_targeting_autonomy:0.78,
    human_control_erosion_index:0.75, AI_arms_race_intensity:0.70, drone_swarm_capability:0.72,
    cyber_warfare_AI_integration:0.65, AI_escalation_risk:0.75, military_AI_regulatory_vacuum:0.80,
    predictive_warfare_capability:0.70, AI_nuclear_integration_risk:0.60, defense_AI_monopoly_risk:0.65,
    lethal_autonomous_weapon_proliferation:0.72, military_AI_accountability_gap:0.78,
    AI_military_capability_gap:0.60, AI_strategic_surprise_risk:0.68, autonomous_warfare_threshold_lowering:0.75 },
  // MAI-002 low / none
  { entity_id:"MAI-002", military_domain:"logistics_support", region:"NAMER",
    autonomous_lethal_weapon_deployment:0.10, AI_command_authority_level:0.08, algorithmic_targeting_autonomy:0.12,
    human_control_erosion_index:0.10, AI_arms_race_intensity:0.12, drone_swarm_capability:0.08,
    cyber_warfare_AI_integration:0.10, AI_escalation_risk:0.10, military_AI_regulatory_vacuum:0.10,
    predictive_warfare_capability:0.12, AI_nuclear_integration_risk:0.05, defense_AI_monopoly_risk:0.08,
    lethal_autonomous_weapon_proliferation:0.10, military_AI_accountability_gap:0.08,
    AI_military_capability_gap:0.10, AI_strategic_surprise_risk:0.08, autonomous_warfare_threshold_lowering:0.10 },
  // MAI-003 high / AI_escalation_cascade (aer>=0.70, assr>=0.65)
  { entity_id:"MAI-003", military_domain:"cyber_operations", region:"APAC",
    autonomous_lethal_weapon_deployment:0.42, AI_command_authority_level:0.40, algorithmic_targeting_autonomy:0.45,
    human_control_erosion_index:0.38, AI_arms_race_intensity:0.48, drone_swarm_capability:0.42,
    cyber_warfare_AI_integration:0.55, AI_escalation_risk:0.75, military_AI_regulatory_vacuum:0.45,
    predictive_warfare_capability:0.50, AI_nuclear_integration_risk:0.38, defense_AI_monopoly_risk:0.42,
    lethal_autonomous_weapon_proliferation:0.45, military_AI_accountability_gap:0.42,
    AI_military_capability_gap:0.45, AI_strategic_surprise_risk:0.68, autonomous_warfare_threshold_lowering:0.60 },
  // MAI-004 low / none
  { entity_id:"MAI-004", military_domain:"medical_triage_AI", region:"LATAM",
    autonomous_lethal_weapon_deployment:0.08, AI_command_authority_level:0.12, algorithmic_targeting_autonomy:0.10,
    human_control_erosion_index:0.08, AI_arms_race_intensity:0.10, drone_swarm_capability:0.12,
    cyber_warfare_AI_integration:0.08, AI_escalation_risk:0.12, military_AI_regulatory_vacuum:0.10,
    predictive_warfare_capability:0.10, AI_nuclear_integration_risk:0.10, defense_AI_monopoly_risk:0.08,
    lethal_autonomous_weapon_proliferation:0.08, military_AI_accountability_gap:0.08,
    AI_military_capability_gap:0.10, AI_strategic_surprise_risk:0.10, autonomous_warfare_threshold_lowering:0.08 },
  // MAI-005 critical / lethal_AI_proliferation (lawp>=0.70, aari>=0.65; aer<0.70 to avoid AI_escalation_cascade)
  { entity_id:"MAI-005", military_domain:"autonomous_weapons_export", region:"MEA",
    autonomous_lethal_weapon_deployment:0.75, AI_command_authority_level:0.70, algorithmic_targeting_autonomy:0.72,
    human_control_erosion_index:0.60, AI_arms_race_intensity:0.78, drone_swarm_capability:0.75,
    cyber_warfare_AI_integration:0.68, AI_escalation_risk:0.60, military_AI_regulatory_vacuum:0.70,
    predictive_warfare_capability:0.72, AI_nuclear_integration_risk:0.60, defense_AI_monopoly_risk:0.68,
    lethal_autonomous_weapon_proliferation:0.82, military_AI_accountability_gap:0.68,
    AI_military_capability_gap:0.65, AI_strategic_surprise_risk:0.62, autonomous_warfare_threshold_lowering:0.68 },
  // MAI-006 moderate / none
  { entity_id:"MAI-006", military_domain:"surveillance_AI", region:"EMEA",
    autonomous_lethal_weapon_deployment:0.30, AI_command_authority_level:0.32, algorithmic_targeting_autonomy:0.28,
    human_control_erosion_index:0.25, AI_arms_race_intensity:0.30, drone_swarm_capability:0.28,
    cyber_warfare_AI_integration:0.32, AI_escalation_risk:0.28, military_AI_regulatory_vacuum:0.28,
    predictive_warfare_capability:0.30, AI_nuclear_integration_risk:0.25, defense_AI_monopoly_risk:0.28,
    lethal_autonomous_weapon_proliferation:0.32, military_AI_accountability_gap:0.30,
    AI_military_capability_gap:0.28, AI_strategic_surprise_risk:0.25, autonomous_warfare_threshold_lowering:0.30 },
  // MAI-007 high / governance_collapse (marv>=0.70, maag>=0.65)
  { entity_id:"MAI-007", military_domain:"command_control_AI", region:"NAMER",
    autonomous_lethal_weapon_deployment:0.42, AI_command_authority_level:0.38, algorithmic_targeting_autonomy:0.40,
    human_control_erosion_index:0.35, AI_arms_race_intensity:0.42, drone_swarm_capability:0.40,
    cyber_warfare_AI_integration:0.38, AI_escalation_risk:0.40, military_AI_regulatory_vacuum:0.78,
    predictive_warfare_capability:0.42, AI_nuclear_integration_risk:0.48, defense_AI_monopoly_risk:0.40,
    lethal_autonomous_weapon_proliferation:0.45, military_AI_accountability_gap:0.72,
    AI_military_capability_gap:0.38, AI_strategic_surprise_risk:0.42, autonomous_warfare_threshold_lowering:0.38 },
  // MAI-008 critical / nuclear_AI_entanglement (anir>=0.70, ata>=0.72; hcei<0.65 to avoid autonomous_kill_chain)
  { entity_id:"MAI-008", military_domain:"nuclear_command_AI", region:"APAC",
    autonomous_lethal_weapon_deployment:0.80, AI_command_authority_level:0.75, algorithmic_targeting_autonomy:0.72,
    human_control_erosion_index:0.55, AI_arms_race_intensity:0.52, drone_swarm_capability:0.65,
    cyber_warfare_AI_integration:0.68, AI_escalation_risk:0.60, military_AI_regulatory_vacuum:0.65,
    predictive_warfare_capability:0.68, AI_nuclear_integration_risk:0.82, defense_AI_monopoly_risk:0.65,
    lethal_autonomous_weapon_proliferation:0.55, military_AI_accountability_gap:0.62,
    AI_military_capability_gap:0.65, AI_strategic_surprise_risk:0.58, autonomous_warfare_threshold_lowering:0.68 },
];

type MilitaryAIEntity = typeof MOCK_ENTITIES[0];

function autonomyScore(e: MilitaryAIEntity): number {
  const v = e.autonomous_lethal_weapon_deployment * 0.40
          + e.algorithmic_targeting_autonomy * 0.35
          + e.AI_command_authority_level * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function escalationScore(e: MilitaryAIEntity): number {
  const v = e.AI_escalation_risk * 0.40
          + e.AI_strategic_surprise_risk * 0.35
          + e.autonomous_warfare_threshold_lowering * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function proliferationScore(e: MilitaryAIEntity): number {
  const v = e.lethal_autonomous_weapon_proliferation * 0.40
          + e.AI_arms_race_intensity * 0.35
          + e.drone_swarm_capability * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function governanceScore(e: MilitaryAIEntity): number {
  const v = e.military_AI_regulatory_vacuum * 0.40
          + e.military_AI_accountability_gap * 0.35
          + e.AI_nuclear_integration_risk * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function compositeScore(a: number, es: number, p: number, g: number): number {
  return Math.min(Math.round((a * 0.30 + es * 0.25 + p * 0.25 + g * 0.20) * 100) / 100, 100);
}
function militaryPattern(e: MilitaryAIEntity): string {
  if (e.autonomous_lethal_weapon_deployment >= 0.70 && e.human_control_erosion_index >= 0.65) return "autonomous_kill_chain";
  if (e.AI_escalation_risk >= 0.70 && e.AI_strategic_surprise_risk >= 0.65)                   return "AI_escalation_cascade";
  if (e.lethal_autonomous_weapon_proliferation >= 0.70 && e.AI_arms_race_intensity >= 0.65)    return "lethal_AI_proliferation";
  if (e.AI_nuclear_integration_risk >= 0.70 && e.algorithmic_targeting_autonomy >= 0.65)       return "nuclear_AI_entanglement";
  if (e.military_AI_regulatory_vacuum >= 0.70 && e.military_AI_accountability_gap >= 0.65)     return "governance_collapse";
  return "none";
}
function riskLevel(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string {
  if (c >= 60) return "guerre_autonome_systémique";
  if (c >= 40) return "escalade_IA_militaire_majeure";
  if (c >= 20) return "militarisation_IA_active";
  return "IA_militaire_contenue";
}
function recommendedAction(c: number): string {
  if (c >= 60) return "interdiction_armes_autonomes_urgente";
  if (c >= 40) return "régulation_IA_militaire_stricte";
  if (c >= 20) return "renforcement_contrôle_humain_IA";
  return "veille_IA_militaire_continue";
}
function signal(c: number): string {
  if (c >= 60) return "🔴 Guerre autonome systémique — IA létale hors contrôle humain";
  if (c >= 40) return "🟠 Escalade IA militaire majeure détectée";
  if (c >= 20) return "🟡 Militarisation IA active — surveillance requise";
  return "🟢 IA militaire sous contrôle relatif";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const aut = autonomyScore(e), esc = escalationScore(e), pro = proliferationScore(e), gov = governanceScore(e);
      const comp = compositeScore(aut, esc, pro, gov);
      const pat = militaryPattern(e), risk = riskLevel(comp);
      return {
        entity_id: e.entity_id,
        military_domain: e.military_domain,
        region: e.region,
        autonomy_score: aut,
        escalation_score: esc,
        proliferation_score: pro,
        governance_score: gov,
        composite_score: comp,
        risk_level: risk,
        military_ai_pattern: pat,
        severity: severity(comp),
        recommended_action: recommendedAction(comp),
        signal: signal(comp),
        autonomous_lethal_weapon_deployment: e.autonomous_lethal_weapon_deployment,
        AI_nuclear_integration_risk: e.AI_nuclear_integration_risk,
      };
    });

    const patDist: Record<string,number>  = {};
    const riskDist: Record<string,number> = {};
    const sevDist: Record<string,number>  = {};
    const actDist: Record<string,number>  = {};
    let totalComp = 0, critical = 0, high = 0, moderate = 0, low = 0;
    for (const en of entities) {
      patDist[en.military_ai_pattern]  = (patDist[en.military_ai_pattern]  || 0) + 1;
      riskDist[en.risk_level]          = (riskDist[en.risk_level]          || 0) + 1;
      sevDist[en.severity]             = (sevDist[en.severity]             || 0) + 1;
      actDist[en.recommended_action]   = (actDist[en.recommended_action]   || 0) + 1;
      totalComp += en.composite_score;
      if (en.risk_level === "critical")       critical++;
      else if (en.risk_level === "high")      high++;
      else if (en.risk_level === "moderate")  moderate++;
      else                                    low++;
    }
    const n = entities.length;
    const avgComposite = Math.round(totalComp / n * 10) / 10;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 337,
        module_name: "Military AI & Autonomous Weapons Intelligence Engine",
        total_entities: n,
        critical_count: critical,
        high_count: high,
        moderate_count: moderate,
        low_count: low,
        avg_composite: avgComposite,
        pattern_distribution: patDist,
        risk_distribution: riskDist,
        severity_distribution: sevDist,
        action_distribution: actDist,
        avg_estimated_military_ai_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
      } as Record<string, unknown>,
    } as Record<string, unknown>, "military-ai-engine") as Parameters<typeof NextResponse.json>[0]);
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/military-ai-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>, "military-ai-engine") as Parameters<typeof NextResponse.json>[0]);
  } catch {
    return NextResponse.json(
      sealResponse({ error: "upstream_unavailable" } as Record<string, unknown>, "military-ai-engine") as Parameters<typeof NextResponse.json>[0],
      { status: 502 }
    );
  }
}
