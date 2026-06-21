import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // MEE-001 — EMEA, social_media → critical, epistemic_collapse
  // epistemic_collapse: source_trust_collapse_index>=0.70 AND truth_fatigue_index>=0.65
  // composite >=60 → critical
  {
    id: "MEE-001", info_domain: "social_media", region: "EMEA",
    viral_misinformation_velocity: 0.82,
    fact_checking_infrastructure_gap: 0.80,
    platform_amplification_bias: 0.75,
    coordinated_inauthentic_behavior_level: 0.60,
    epistemic_bubble_density: 0.72,
    source_trust_collapse_index: 0.88,
    AI_generated_misinformation_volume: 0.70,
    bot_network_coordination_intensity: 0.58,
    media_literacy_deficit: 0.75,
    state_sponsored_disinformation_scale: 0.55,
    scientific_consensus_attack_rate: 0.60,
    health_misinformation_mortality: 0.50,
    financial_misinformation_market_impact: 0.58,
    algorithmic_rabbit_hole_depth: 0.55,
    truth_fatigue_index: 0.80,
    influencer_misinformation_amplification: 0.62,
    counter_narrative_suppression: 0.70,
  },
  // MEE-002 — APAC, local_news → low, none
  // composite < 20 → low; no pattern triggers
  {
    id: "MEE-002", info_domain: "local_news", region: "APAC",
    viral_misinformation_velocity: 0.08,
    fact_checking_infrastructure_gap: 0.10,
    platform_amplification_bias: 0.10,
    coordinated_inauthentic_behavior_level: 0.08,
    epistemic_bubble_density: 0.12,
    source_trust_collapse_index: 0.12,
    AI_generated_misinformation_volume: 0.12,
    bot_network_coordination_intensity: 0.10,
    media_literacy_deficit: 0.12,
    state_sponsored_disinformation_scale: 0.08,
    scientific_consensus_attack_rate: 0.10,
    health_misinformation_mortality: 0.08,
    financial_misinformation_market_impact: 0.10,
    algorithmic_rabbit_hole_depth: 0.08,
    truth_fatigue_index: 0.10,
    influencer_misinformation_amplification: 0.10,
    counter_narrative_suppression: 0.08,
  },
  // MEE-003 — NOAM, digital_platform → high, AI_disinfo_saturation
  // AI_disinfo_saturation: AI_generated>=0.70 AND platform_amplification_bias>=0.65
  // epistemic_collapse must NOT fire: source_trust_collapse_index<0.70
  // composite >=40 and <60 → high
  {
    id: "MEE-003", info_domain: "digital_platform", region: "NOAM",
    viral_misinformation_velocity: 0.55,
    fact_checking_infrastructure_gap: 0.55,
    platform_amplification_bias: 0.72,
    coordinated_inauthentic_behavior_level: 0.42,
    epistemic_bubble_density: 0.48,
    source_trust_collapse_index: 0.45,
    AI_generated_misinformation_volume: 0.78,
    bot_network_coordination_intensity: 0.38,
    media_literacy_deficit: 0.50,
    state_sponsored_disinformation_scale: 0.30,
    scientific_consensus_attack_rate: 0.35,
    health_misinformation_mortality: 0.30,
    financial_misinformation_market_impact: 0.40,
    algorithmic_rabbit_hole_depth: 0.42,
    truth_fatigue_index: 0.50,
    influencer_misinformation_amplification: 0.45,
    counter_narrative_suppression: 0.48,
  },
  // MEE-004 — LATAM, community_media → low, none
  // composite < 20 → low; no pattern triggers
  {
    id: "MEE-004", info_domain: "community_media", region: "LATAM",
    viral_misinformation_velocity: 0.08,
    fact_checking_infrastructure_gap: 0.10,
    platform_amplification_bias: 0.10,
    coordinated_inauthentic_behavior_level: 0.08,
    epistemic_bubble_density: 0.12,
    source_trust_collapse_index: 0.12,
    AI_generated_misinformation_volume: 0.12,
    bot_network_coordination_intensity: 0.10,
    media_literacy_deficit: 0.12,
    state_sponsored_disinformation_scale: 0.08,
    scientific_consensus_attack_rate: 0.10,
    health_misinformation_mortality: 0.08,
    financial_misinformation_market_impact: 0.10,
    algorithmic_rabbit_hole_depth: 0.08,
    truth_fatigue_index: 0.10,
    influencer_misinformation_amplification: 0.10,
    counter_narrative_suppression: 0.08,
  },
  // MEE-005 — MEA, state_media → critical, state_info_warfare
  // state_info_warfare: state_sponsored>=0.70 AND coordinated_inauthentic>=0.65
  // epistemic_collapse must NOT fire: source_trust_collapse_index<0.70
  // AI_disinfo_saturation must NOT fire: AI_generated<0.70
  // composite >=60 → critical
  {
    id: "MEE-005", info_domain: "state_media", region: "MEA",
    viral_misinformation_velocity: 0.72,
    fact_checking_infrastructure_gap: 0.75,
    platform_amplification_bias: 0.60,
    coordinated_inauthentic_behavior_level: 0.78,
    epistemic_bubble_density: 0.62,
    source_trust_collapse_index: 0.55,
    AI_generated_misinformation_volume: 0.58,
    bot_network_coordination_intensity: 0.72,
    media_literacy_deficit: 0.68,
    state_sponsored_disinformation_scale: 0.85,
    scientific_consensus_attack_rate: 0.58,
    health_misinformation_mortality: 0.50,
    financial_misinformation_market_impact: 0.55,
    algorithmic_rabbit_hole_depth: 0.48,
    truth_fatigue_index: 0.60,
    influencer_misinformation_amplification: 0.55,
    counter_narrative_suppression: 0.70,
  },
  // MEE-006 — EMEA, broadcast_media → moderate, none
  // composite >=20 and <40 → moderate; no pattern triggers
  {
    id: "MEE-006", info_domain: "broadcast_media", region: "EMEA",
    viral_misinformation_velocity: 0.28,
    fact_checking_infrastructure_gap: 0.35,
    platform_amplification_bias: 0.32,
    coordinated_inauthentic_behavior_level: 0.28,
    epistemic_bubble_density: 0.32,
    source_trust_collapse_index: 0.35,
    AI_generated_misinformation_volume: 0.30,
    bot_network_coordination_intensity: 0.25,
    media_literacy_deficit: 0.30,
    state_sponsored_disinformation_scale: 0.22,
    scientific_consensus_attack_rate: 0.25,
    health_misinformation_mortality: 0.20,
    financial_misinformation_market_impact: 0.28,
    algorithmic_rabbit_hole_depth: 0.25,
    truth_fatigue_index: 0.30,
    influencer_misinformation_amplification: 0.28,
    counter_narrative_suppression: 0.28,
  },
  // MEE-007 — APAC, health_media → high, health_disinfo_crisis
  // health_disinfo_crisis: health_misinformation_mortality>=0.70 AND scientific_consensus_attack_rate>=0.65
  // epistemic_collapse must NOT fire: source_trust<0.70
  // AI_disinfo must NOT fire: AI_generated<0.70
  // state_info_warfare must NOT fire: state_sponsored<0.70
  // composite >=40 and <60 → high
  {
    id: "MEE-007", info_domain: "health_media", region: "APAC",
    viral_misinformation_velocity: 0.50,
    fact_checking_infrastructure_gap: 0.58,
    platform_amplification_bias: 0.48,
    coordinated_inauthentic_behavior_level: 0.42,
    epistemic_bubble_density: 0.45,
    source_trust_collapse_index: 0.52,
    AI_generated_misinformation_volume: 0.45,
    bot_network_coordination_intensity: 0.40,
    media_literacy_deficit: 0.52,
    state_sponsored_disinformation_scale: 0.38,
    scientific_consensus_attack_rate: 0.72,
    health_misinformation_mortality: 0.80,
    financial_misinformation_market_impact: 0.40,
    algorithmic_rabbit_hole_depth: 0.42,
    truth_fatigue_index: 0.48,
    influencer_misinformation_amplification: 0.45,
    counter_narrative_suppression: 0.48,
  },
  // MEE-008 — NOAM, influencer_ecosystem → critical, algorithmic_radicalization
  // algorithmic_radicalization: algorithmic_rabbit_hole_depth>=0.70 AND influencer_misinformation_amplification>=0.65
  // epistemic_collapse must NOT fire: source_trust<0.70
  // AI_disinfo must NOT fire: AI_generated<0.70
  // state_info_warfare must NOT fire: state_sponsored<0.70
  // health_disinfo must NOT fire: health_mortality<0.70
  // composite >=60 → critical
  {
    id: "MEE-008", info_domain: "influencer_ecosystem", region: "NOAM",
    viral_misinformation_velocity: 0.72,
    fact_checking_infrastructure_gap: 0.72,
    platform_amplification_bias: 0.60,
    coordinated_inauthentic_behavior_level: 0.55,
    epistemic_bubble_density: 0.70,
    source_trust_collapse_index: 0.60,
    AI_generated_misinformation_volume: 0.55,
    bot_network_coordination_intensity: 0.52,
    media_literacy_deficit: 0.68,
    state_sponsored_disinformation_scale: 0.48,
    scientific_consensus_attack_rate: 0.38,
    health_misinformation_mortality: 0.42,
    financial_misinformation_market_impact: 0.60,
    algorithmic_rabbit_hole_depth: 0.82,
    truth_fatigue_index: 0.58,
    influencer_misinformation_amplification: 0.78,
    counter_narrative_suppression: 0.65,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function velocityScore(e: Entity): number {
  const raw = (
    e.viral_misinformation_velocity * 0.4 +
    e.platform_amplification_bias * 0.35 +
    e.AI_generated_misinformation_volume * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function coordinationScore(e: Entity): number {
  const raw = (
    e.coordinated_inauthentic_behavior_level * 0.4 +
    e.bot_network_coordination_intensity * 0.35 +
    e.state_sponsored_disinformation_scale * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function erosionScore(e: Entity): number {
  const raw = (
    e.source_trust_collapse_index * 0.4 +
    e.truth_fatigue_index * 0.35 +
    e.epistemic_bubble_density * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function defenseScore(e: Entity): number {
  const raw = (
    e.fact_checking_infrastructure_gap * 0.4 +
    e.media_literacy_deficit * 0.35 +
    e.counter_narrative_suppression * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(vel: number, coord: number, eros: number, def: number): number {
  return Math.round((vel * 0.30 + coord * 0.25 + eros * 0.25 + def * 0.20) * 100) / 100;
}

function misinoPattern(e: Entity): string {
  if (e.source_trust_collapse_index >= 0.70 && e.truth_fatigue_index >= 0.65)
    return "epistemic_collapse";
  if (e.AI_generated_misinformation_volume >= 0.70 && e.platform_amplification_bias >= 0.65)
    return "AI_disinfo_saturation";
  if (e.state_sponsored_disinformation_scale >= 0.70 && e.coordinated_inauthentic_behavior_level >= 0.65)
    return "state_info_warfare";
  if (e.health_misinformation_mortality >= 0.70 && e.scientific_consensus_attack_rate >= 0.65)
    return "health_disinfo_crisis";
  if (e.algorithmic_rabbit_hole_depth >= 0.70 && e.influencer_misinformation_amplification >= 0.65)
    return "algorithmic_radicalization";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(comp: number): string {
  if (comp >= 60) return "effondrement_vérité_systémique";
  if (comp >= 40) return "crise_désinformation_majeure";
  if (comp >= 20) return "écosystème_désinformation_actif";
  return "désinformation_contenue";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_médias_urgente";
  if (risk === "high") return "contre-mesures_désinformation_activées";
  if (risk === "moderate") return "renforcement_littératie_médiatique";
  return "veille_désinformation_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Effondrement vérité systémique — désinformation critique";
  if (risk === "high") return "🟠 Crise désinformation majeure détectée";
  if (risk === "moderate") return "🟡 Écosystème désinformation actif";
  return "🟢 Désinformation relativement contenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const vel   = velocityScore(e);
      const coord = coordinationScore(e);
      const eros  = erosionScore(e);
      const def   = defenseScore(e);
      const comp  = compositeScore(vel, coord, eros, def);
      const pat   = misinoPattern(e);
      const risk  = riskLevel(comp);
      const sev   = severity(comp);
      const act   = recommendedAction(risk);
      const sig   = signal(risk);
      return {
        id:                         e.entity_id,
        info_domain:                       e.info_domain,
        region:                            e.region,
        velocity_score:                    vel,
        coordination_score:                coord,
        erosion_score:                     eros,
        defense_score:                     def,
        composite_score:                   comp,
        risk_level:                        risk,
        misinfo_pattern:                   pat,
        severity:                          sev,
        recommended_action:                act,
        signal:                            sig,
        viral_misinformation_velocity:     e.viral_misinformation_velocity,
        source_trust_collapse_index:       e.source_trust_collapse_index,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tVel = 0, tCoord = 0, tEros = 0, tDef = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      rc[ent.risk_level]         = (rc[ent.risk_level]         || 0) + 1;
      pc[ent.misinfo_pattern]    = (pc[ent.misinfo_pattern]    || 0) + 1;
      sc[ent.severity]           = (sc[ent.severity]           || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tVel   += ent.velocity_score;
      tCoord += ent.coordination_score;
      tEros  += ent.erosion_score;
      tDef   += ent.defense_score;
      tComp  += ent.composite_score;
      if (ent.risk_level === "critical")  criticalCount++;
      else if (ent.risk_level === "high") highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else lowCount++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;
    const summary = {
      module_id:                    355,
      module_name:                  "Misinformation Ecosystem & Truth Collapse Intelligence Engine",
      total_entities:               n,
      critical_count:               criticalCount,
      high_count:                   highCount,
      moderate_count:               moderateCount,
      low_count:                    lowCount,
      avg_composite:                avgComp,
      pattern_distribution:         pc,
      risk_distribution:            rc,
      severity_distribution:        sc,
      action_distribution:          ac,
      avg_estimated_misinfo_index:  Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "misinformation-ecosystem-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/misinformation-ecosystem-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "misinformation-ecosystem-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream misinformation ecosystem engine unavailable" }, "misinformation-ecosystem-engine"),
      { status: 502 }
    );
  }
}
