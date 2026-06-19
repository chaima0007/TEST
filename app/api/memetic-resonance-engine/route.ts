import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_MEMES = [
  // MM-001 brand_narrative EMEA — critical/viral_cascade
  { meme_id:"MM-001", meme_type:"brand_narrative",      region:"EMEA",  virality_coefficient:0.88, resonance_depth_score:0.82, adoption_velocity:0.85, network_penetration_rate:0.78, counter_meme_resistance:0.20, emotional_hook_strength:0.80, cognitive_load_barrier:0.15, platform_amplification_factor:0.90, influencer_alignment_score:0.75, narrative_coherence_score:0.78, temporal_stickiness_score:0.72, cross_cultural_adaptation_score:0.68, belief_entrenchment_level:0.65, social_proof_density:0.82, fear_uncertainty_doubt_index:0.70, memetic_mutation_rate:0.45, echo_chamber_intensity:0.60 },
  // MM-002 cultural_movement NAMER — low
  { meme_id:"MM-002", meme_type:"cultural_movement",    region:"NAMER", virality_coefficient:0.08, resonance_depth_score:0.12, adoption_velocity:0.10, network_penetration_rate:0.10, counter_meme_resistance:0.85, emotional_hook_strength:0.15, cognitive_load_barrier:0.80, platform_amplification_factor:0.08, influencer_alignment_score:0.12, narrative_coherence_score:0.10, temporal_stickiness_score:0.15, cross_cultural_adaptation_score:0.12, belief_entrenchment_level:0.10, social_proof_density:0.08, fear_uncertainty_doubt_index:0.05, memetic_mutation_rate:0.08, echo_chamber_intensity:0.10 },
  // MM-003 crisis_narrative APAC — high/narrative_hijack
  { meme_id:"MM-003", meme_type:"crisis_narrative",     region:"APAC",  virality_coefficient:0.55, resonance_depth_score:0.45, adoption_velocity:0.52, network_penetration_rate:0.50, counter_meme_resistance:0.32, emotional_hook_strength:0.48, cognitive_load_barrier:0.35, platform_amplification_factor:0.48, influencer_alignment_score:0.42, narrative_coherence_score:0.32, temporal_stickiness_score:0.42, cross_cultural_adaptation_score:0.38, belief_entrenchment_level:0.40, social_proof_density:0.45, fear_uncertainty_doubt_index:0.65, memetic_mutation_rate:0.72, echo_chamber_intensity:0.42 },
  // MM-004 organizational_value LATAM — low
  { meme_id:"MM-004", meme_type:"organizational_value", region:"LATAM", virality_coefficient:0.10, resonance_depth_score:0.15, adoption_velocity:0.08, network_penetration_rate:0.12, counter_meme_resistance:0.88, emotional_hook_strength:0.12, cognitive_load_barrier:0.75, platform_amplification_factor:0.08, influencer_alignment_score:0.10, narrative_coherence_score:0.12, temporal_stickiness_score:0.18, cross_cultural_adaptation_score:0.14, belief_entrenchment_level:0.12, social_proof_density:0.10, fear_uncertainty_doubt_index:0.08, memetic_mutation_rate:0.10, echo_chamber_intensity:0.12 },
  // MM-005 market_sentiment EMEA — critical/echo_chamber_lock
  { meme_id:"MM-005", meme_type:"market_sentiment",     region:"EMEA",  virality_coefficient:0.72, resonance_depth_score:0.70, adoption_velocity:0.78, network_penetration_rate:0.68, counter_meme_resistance:0.22, emotional_hook_strength:0.72, cognitive_load_barrier:0.20, platform_amplification_factor:0.68, influencer_alignment_score:0.70, narrative_coherence_score:0.65, temporal_stickiness_score:0.68, cross_cultural_adaptation_score:0.22, belief_entrenchment_level:0.75, social_proof_density:0.78, fear_uncertainty_doubt_index:0.68, memetic_mutation_rate:0.40, echo_chamber_intensity:0.82 },
  // MM-006 scientific_paradigm MEA — moderate
  { meme_id:"MM-006", meme_type:"scientific_paradigm",  region:"MEA",   virality_coefficient:0.28, resonance_depth_score:0.32, adoption_velocity:0.25, network_penetration_rate:0.28, counter_meme_resistance:0.55, emotional_hook_strength:0.30, cognitive_load_barrier:0.68, platform_amplification_factor:0.22, influencer_alignment_score:0.25, narrative_coherence_score:0.35, temporal_stickiness_score:0.30, cross_cultural_adaptation_score:0.28, belief_entrenchment_level:0.28, social_proof_density:0.25, fear_uncertainty_doubt_index:0.30, memetic_mutation_rate:0.25, echo_chamber_intensity:0.28 },
  // MM-007 political_ideology NAMER — high/belief_crystallization
  { meme_id:"MM-007", meme_type:"political_ideology",   region:"NAMER", virality_coefficient:0.50, resonance_depth_score:0.52, adoption_velocity:0.48, network_penetration_rate:0.50, counter_meme_resistance:0.40, emotional_hook_strength:0.55, cognitive_load_barrier:0.28, platform_amplification_factor:0.48, influencer_alignment_score:0.45, narrative_coherence_score:0.52, temporal_stickiness_score:0.50, cross_cultural_adaptation_score:0.42, belief_entrenchment_level:0.75, social_proof_density:0.48, fear_uncertainty_doubt_index:0.45, memetic_mutation_rate:0.32, echo_chamber_intensity:0.45 },
  // MM-008 product_concept APAC — low
  { meme_id:"MM-008", meme_type:"product_concept",      region:"APAC",  virality_coefficient:0.10, resonance_depth_score:0.14, adoption_velocity:0.12, network_penetration_rate:0.12, counter_meme_resistance:0.82, emotional_hook_strength:0.18, cognitive_load_barrier:0.72, platform_amplification_factor:0.10, influencer_alignment_score:0.14, narrative_coherence_score:0.12, temporal_stickiness_score:0.16, cross_cultural_adaptation_score:0.15, belief_entrenchment_level:0.12, social_proof_density:0.14, fear_uncertainty_doubt_index:0.10, memetic_mutation_rate:0.12, echo_chamber_intensity:0.14 },
];

type Meme = typeof MOCK_MEMES[0];

function viralityScore(m: Meme): number {
  const raw = (m.virality_coefficient + m.platform_amplification_factor + m.adoption_velocity) / 3;
  return Math.min(Math.round(raw * 10000) / 100, 100);
}
function resonanceScore(m: Meme): number {
  const raw = (m.emotional_hook_strength + m.narrative_coherence_score + m.resonance_depth_score) / 3;
  return Math.min(Math.round(raw * 10000) / 100, 100);
}
function persistenceScore(m: Meme): number {
  const raw = (m.temporal_stickiness_score + m.belief_entrenchment_level + m.counter_meme_resistance) / 3;
  return Math.min(Math.round(raw * 10000) / 100, 100);
}
function reachScore(m: Meme): number {
  const raw = (m.network_penetration_rate + m.influencer_alignment_score + m.cross_cultural_adaptation_score) / 3;
  return Math.min(Math.round(raw * 10000) / 100, 100);
}
function composite(vir: number, res: number, per: number, rch: number): number {
  return Math.min(Math.round((vir * 0.30 + res * 0.25 + per * 0.25 + rch * 0.20) * 100) / 100, 100);
}
function memeticRisk(c: number): string {
  if (c >= 60) return "critical";
  if (c >= 40) return "high";
  if (c >= 20) return "moderate";
  return "low";
}
function memeticSeverity(c: number): string {
  if (c >= 60) return "epidemic";
  if (c >= 40) return "spreading";
  if (c >= 20) return "seeding";
  return "contained";
}
function memeticPattern(m: Meme): string {
  if (m.virality_coefficient >= 0.75 && m.platform_amplification_factor >= 0.70) return "viral_cascade";
  if (m.echo_chamber_intensity >= 0.70 && m.cross_cultural_adaptation_score <= 0.35) return "echo_chamber_lock";
  if (m.memetic_mutation_rate >= 0.65 && m.narrative_coherence_score <= 0.40) return "narrative_hijack";
  if (m.counter_meme_resistance <= 0.25 && m.fear_uncertainty_doubt_index >= 0.60) return "counter_meme_collapse";
  if (m.belief_entrenchment_level >= 0.70 && m.cognitive_load_barrier <= 0.35) return "belief_crystallization";
  return "none";
}
function memeticAction(risk: string, pat: string): string {
  if (risk === "critical") {
    if (pat === "viral_cascade" || pat === "echo_chamber_lock") return "crisis_narrative_reset";
    return "counter_meme_injection";
  }
  if (risk === "high") {
    if (pat === "narrative_hijack" || pat === "counter_meme_collapse") return "narrative_steering";
    return "influence_mapping";
  }
  if (risk === "moderate") return "meme_monitoring";
  return "no_action";
}
function memeticSignal(m: Meme, pat: string, comp: number): string {
  if (comp < 20) return "Mème stabilisé — propagation maîtrisée, narration cohérente, résonance contrôlée";
  const patLabels: Record<string, string> = {
    viral_cascade:          "Cascade virale",
    echo_chamber_lock:      "Verrouillage chambre d'écho",
    narrative_hijack:       "Détournement narratif",
    counter_meme_collapse:  "Effondrement contre-mème",
    belief_crystallization: "Cristallisation des croyances",
    none:                   "Propagation active",
  };
  const label = patLabels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — viralité ${m.virality_coefficient.toFixed(2)} — pénétration réseau ${m.network_penetration_rate.toFixed(2)} — résonance ${m.resonance_depth_score.toFixed(2)} — composite ${Math.round(comp)}`;
}
function viralDisruptionIndex(m: Meme, comp: number): number {
  return Math.round(Math.min(comp / 100 * (m.virality_coefficient + m.echo_chamber_intensity) / 2 * 10, 10.0) * 100) / 100;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const memes = MOCK_MEMES.map(m => {
      const vir = viralityScore(m), res = resonanceScore(m), per = persistenceScore(m), rch = reachScore(m);
      const comp = composite(vir, res, per, rch);
      const risk = memeticRisk(comp), sev = memeticSeverity(comp);
      const pat = memeticPattern(m), act = memeticAction(risk, pat);
      return {
        meme_id: m.meme_id, meme_type: m.meme_type, region: m.region,
        memetic_risk: risk, memetic_pattern: pat, memetic_severity: sev, recommended_action: act,
        virality_score: vir, resonance_score: res, persistence_score: per, reach_score: rch,
        memetic_composite: comp,
        is_epidemic_threat: comp >= 60,
        requires_active_intervention: comp >= 40,
        estimated_viral_disruption_index: viralDisruptionIndex(m, comp),
        memetic_signal: memeticSignal(m, pat, comp),
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tvir=0, tres=0, tper=0, trch=0, tcomp=0, tdis=0, epidC=0, interC=0;
    for (const mm of memes) {
      rc[mm.memetic_risk]       = (rc[mm.memetic_risk]       || 0) + 1;
      pc[mm.memetic_pattern]    = (pc[mm.memetic_pattern]    || 0) + 1;
      sc[mm.memetic_severity]   = (sc[mm.memetic_severity]   || 0) + 1;
      ac[mm.recommended_action] = (ac[mm.recommended_action] || 0) + 1;
      tvir  += mm.virality_score;
      tres  += mm.resonance_score;
      tper  += mm.persistence_score;
      trch  += mm.reach_score;
      tcomp += mm.memetic_composite;
      tdis  += mm.estimated_viral_disruption_index;
      if (mm.is_epidemic_threat)           epidC++;
      if (mm.requires_active_intervention) interC++;
    }
    const n = memes.length;
    return NextResponse.json(sealResponse({ memes, summary: {
      total: n,
      risk_counts: rc,
      pattern_counts: pc,
      severity_counts: sc,
      action_counts: ac,
      avg_memetic_composite: Math.round(tcomp / n * 10) / 10,
      epidemic_count: epidC,
      active_intervention_count: interC,
      avg_virality_score: Math.round(tvir / n * 10) / 10,
      avg_resonance_score: Math.round(tres / n * 10) / 10,
      avg_persistence_score: Math.round(tper / n * 10) / 10,
      avg_reach_score: Math.round(trch / n * 10) / 10,
      avg_estimated_viral_disruption_index: Math.round(tdis / n * 100) / 100,
    } as Record<string, unknown>}, "memetic-resonance-engine") as Parameters<typeof NextResponse.json>[0]);
  }
  return NextResponse.json(sealResponse(await (await fetch(`${process.env.SWARM_API_URL}/memetic-resonance-engine`)).json(), "memetic-resonance-engine") as Parameters<typeof NextResponse.json>[0]);
}
