import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[psychopolitics-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// PPE-001: EMEA, electoral_politics      → critical, mass_psychosis_politics
// PPE-002: NOAM, local_governance        → low,      none
// PPE-003: MEA,  ethnic_politics         → high,     tribal_warfare_activation
// PPE-004: APAC, civil_society           → low,      none
// PPE-005: LATAM, post_conflict_gov      → critical, trauma_based_control
// PPE-006: EU,   parliamentary_democracy → moderate, none
// PPE-007: EURASIA, authoritarian_regime → high,     authoritarian_personality_cult
// PPE-008: LATAM, fragile_democracy      → critical, democratic_psychological_collapse

const MOCK_ENTITIES = [
  // PPE-001 — critical, mass_psychosis_politics
  // mass_anxiety_political_exploitation≥0.70 AND emotional_contagion_amplification≥0.65
  { id: "PPE-001", political_domain: "electoral_politics", region: "EMEA",
    mass_anxiety_political_exploitation: 0.88, tribal_identity_weaponization: 0.72,
    emotional_contagion_amplification: 0.85, fear_architecture_deployment: 0.82,
    political_gaslighting_prevalence: 0.78, collective_trauma_manipulation: 0.80,
    populist_neuroscience_targeting: 0.75, scapegoating_mechanism_intensity: 0.70,
    authoritarian_personality_activation: 0.76, political_PTSD_induction: 0.72,
    cult_of_personality_formation: 0.68, manufactured_crisis_normalization: 0.75,
    democratic_disillusionment_weaponization: 0.78, political_nostalgia_manipulation: 0.72,
    shame_guilt_political_leverage: 0.70, mass_helplessness_cultivation: 0.68,
    political_identity_addiction: 0.74 },

  // PPE-002 — low, none
  { id: "PPE-002", political_domain: "local_governance", region: "NOAM",
    mass_anxiety_political_exploitation: 0.12, tribal_identity_weaponization: 0.10,
    emotional_contagion_amplification: 0.15, fear_architecture_deployment: 0.12,
    political_gaslighting_prevalence: 0.10, collective_trauma_manipulation: 0.12,
    populist_neuroscience_targeting: 0.10, scapegoating_mechanism_intensity: 0.08,
    authoritarian_personality_activation: 0.10, political_PTSD_induction: 0.08,
    cult_of_personality_formation: 0.10, manufactured_crisis_normalization: 0.12,
    democratic_disillusionment_weaponization: 0.10, political_nostalgia_manipulation: 0.12,
    shame_guilt_political_leverage: 0.08, mass_helplessness_cultivation: 0.10,
    political_identity_addiction: 0.08 },

  // PPE-003 — high, tribal_warfare_activation
  // tribal_identity_weaponization≥0.70 AND scapegoating_mechanism_intensity≥0.65
  { id: "PPE-003", political_domain: "ethnic_politics", region: "MEA",
    mass_anxiety_political_exploitation: 0.60, tribal_identity_weaponization: 0.82,
    emotional_contagion_amplification: 0.60, fear_architecture_deployment: 0.55,
    political_gaslighting_prevalence: 0.52, collective_trauma_manipulation: 0.48,
    populist_neuroscience_targeting: 0.55, scapegoating_mechanism_intensity: 0.78,
    authoritarian_personality_activation: 0.55, political_PTSD_induction: 0.50,
    cult_of_personality_formation: 0.48, manufactured_crisis_normalization: 0.52,
    democratic_disillusionment_weaponization: 0.50, political_nostalgia_manipulation: 0.55,
    shame_guilt_political_leverage: 0.48, mass_helplessness_cultivation: 0.50,
    political_identity_addiction: 0.58 },

  // PPE-004 — low, none
  { id: "PPE-004", political_domain: "civil_society", region: "APAC",
    mass_anxiety_political_exploitation: 0.15, tribal_identity_weaponization: 0.12,
    emotional_contagion_amplification: 0.18, fear_architecture_deployment: 0.10,
    political_gaslighting_prevalence: 0.12, collective_trauma_manipulation: 0.15,
    populist_neuroscience_targeting: 0.12, scapegoating_mechanism_intensity: 0.10,
    authoritarian_personality_activation: 0.12, political_PTSD_induction: 0.10,
    cult_of_personality_formation: 0.08, manufactured_crisis_normalization: 0.12,
    democratic_disillusionment_weaponization: 0.12, political_nostalgia_manipulation: 0.10,
    shame_guilt_political_leverage: 0.10, mass_helplessness_cultivation: 0.12,
    political_identity_addiction: 0.10 },

  // PPE-005 — critical, trauma_based_control
  // collective_trauma_manipulation≥0.70 AND political_PTSD_induction≥0.65
  { id: "PPE-005", political_domain: "post_conflict_governance", region: "LATAM",
    mass_anxiety_political_exploitation: 0.60, tribal_identity_weaponization: 0.55,
    emotional_contagion_amplification: 0.60, fear_architecture_deployment: 0.80,
    political_gaslighting_prevalence: 0.75, collective_trauma_manipulation: 0.88,
    populist_neuroscience_targeting: 0.70, scapegoating_mechanism_intensity: 0.60,
    authoritarian_personality_activation: 0.72, political_PTSD_induction: 0.82,
    cult_of_personality_formation: 0.65, manufactured_crisis_normalization: 0.78,
    democratic_disillusionment_weaponization: 0.70, political_nostalgia_manipulation: 0.68,
    shame_guilt_political_leverage: 0.72, mass_helplessness_cultivation: 0.80,
    political_identity_addiction: 0.65 },

  // PPE-006 — moderate, none
  { id: "PPE-006", political_domain: "parliamentary_democracy", region: "EU",
    mass_anxiety_political_exploitation: 0.35, tribal_identity_weaponization: 0.30,
    emotional_contagion_amplification: 0.32, fear_architecture_deployment: 0.30,
    political_gaslighting_prevalence: 0.28, collective_trauma_manipulation: 0.30,
    populist_neuroscience_targeting: 0.32, scapegoating_mechanism_intensity: 0.28,
    authoritarian_personality_activation: 0.30, political_PTSD_induction: 0.28,
    cult_of_personality_formation: 0.30, manufactured_crisis_normalization: 0.28,
    democratic_disillusionment_weaponization: 0.32, political_nostalgia_manipulation: 0.30,
    shame_guilt_political_leverage: 0.28, mass_helplessness_cultivation: 0.30,
    political_identity_addiction: 0.28 },

  // PPE-007 — high, authoritarian_personality_cult
  // cult_of_personality_formation≥0.70 AND authoritarian_personality_activation≥0.65
  { id: "PPE-007", political_domain: "authoritarian_regime", region: "EURASIA",
    mass_anxiety_political_exploitation: 0.45, tribal_identity_weaponization: 0.42,
    emotional_contagion_amplification: 0.45, fear_architecture_deployment: 0.48,
    political_gaslighting_prevalence: 0.42, collective_trauma_manipulation: 0.42,
    populist_neuroscience_targeting: 0.45, scapegoating_mechanism_intensity: 0.40,
    authoritarian_personality_activation: 0.78, political_PTSD_induction: 0.40,
    cult_of_personality_formation: 0.82, manufactured_crisis_normalization: 0.45,
    democratic_disillusionment_weaponization: 0.48, political_nostalgia_manipulation: 0.50,
    shame_guilt_political_leverage: 0.42, mass_helplessness_cultivation: 0.45,
    political_identity_addiction: 0.48 },

  // PPE-008 — critical, democratic_psychological_collapse
  // democratic_disillusionment_weaponization≥0.70 AND mass_helplessness_cultivation≥0.65
  { id: "PPE-008", political_domain: "fragile_democracy", region: "LATAM",
    mass_anxiety_political_exploitation: 0.65, tribal_identity_weaponization: 0.60,
    emotional_contagion_amplification: 0.62, fear_architecture_deployment: 0.78,
    political_gaslighting_prevalence: 0.72, collective_trauma_manipulation: 0.62,
    populist_neuroscience_targeting: 0.68, scapegoating_mechanism_intensity: 0.62,
    authoritarian_personality_activation: 0.65, political_PTSD_induction: 0.62,
    cult_of_personality_formation: 0.60, manufactured_crisis_normalization: 0.68,
    democratic_disillusionment_weaponization: 0.85, political_nostalgia_manipulation: 0.72,
    shame_guilt_political_leverage: 0.68, mass_helplessness_cultivation: 0.78,
    political_identity_addiction: 0.72 },
];

type Entity = typeof MOCK_ENTITIES[0];

function manipulationScore(e: Entity): number {
  return Math.round((
    e.mass_anxiety_political_exploitation * 0.4 +
    e.fear_architecture_deployment        * 0.35 +
    e.political_gaslighting_prevalence    * 0.25
  ) * 100 * 100) / 100;
}

function identityScore(e: Entity): number {
  return Math.round((
    e.tribal_identity_weaponization * 0.4 +
    e.political_identity_addiction   * 0.35 +
    e.cult_of_personality_formation  * 0.25
  ) * 100 * 100) / 100;
}

function traumaScore(e: Entity): number {
  return Math.round((
    e.collective_trauma_manipulation * 0.4 +
    e.political_PTSD_induction       * 0.35 +
    e.mass_helplessness_cultivation  * 0.25
  ) * 100 * 100) / 100;
}

function structuralScore(e: Entity): number {
  return Math.round((
    e.authoritarian_personality_activation      * 0.4 +
    e.democratic_disillusionment_weaponization  * 0.35 +
    e.manufactured_crisis_normalization         * 0.25
  ) * 100 * 100) / 100;
}

function compositeScore(manip: number, identity: number, trauma: number, structural: number): number {
  return Math.round((manip * 0.30 + identity * 0.25 + trauma * 0.25 + structural * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function psychoPattern(e: Entity): string {
  if (e.mass_anxiety_political_exploitation >= 0.70 && e.emotional_contagion_amplification >= 0.65)
    return "mass_psychosis_politics";
  if (e.tribal_identity_weaponization >= 0.70 && e.scapegoating_mechanism_intensity >= 0.65)
    return "tribal_warfare_activation";
  if (e.collective_trauma_manipulation >= 0.70 && e.political_PTSD_induction >= 0.65)
    return "trauma_based_control";
  if (e.cult_of_personality_formation >= 0.70 && e.authoritarian_personality_activation >= 0.65)
    return "authoritarian_personality_cult";
  if (e.democratic_disillusionment_weaponization >= 0.70 && e.mass_helplessness_cultivation >= 0.65)
    return "democratic_psychological_collapse";
  return "none";
}

function severity(risk: string): string {
  if (risk === "critical") return "psychopolitique_systémique_avancée";
  if (risk === "high")     return "manipulation_masse_majeure";
  if (risk === "moderate") return "exploitation_psychologique_structurelle";
  return "politique_psychologie_contenue";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "résilience_psychologique_collective_urgente";
  if (risk === "high")     return "contre-mesures_manipulation_psychopolitique";
  if (risk === "moderate") return "renforcement_pensée_critique_citoyenne";
  return "veille_psychopolitique_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Psychopolitique systémique — manipulation masse critique";
  if (risk === "high")     return "🟠 Manipulation masse majeure détectée";
  if (risk === "moderate") return "🟡 Exploitation psychologique structurelle active";
  return "🟢 Psychologie politique relativement saine";
}

function buildEntity(e: Entity) {
  const manip      = manipulationScore(e);
  const identity   = identityScore(e);
  const trauma     = traumaScore(e);
  const structural = structuralScore(e);
  const comp       = compositeScore(manip, identity, trauma, structural);
  const risk       = riskLevel(comp);
  const pattern    = psychoPattern(e);
  return {
    id:                               e.entity_id,
    political_domain:                        e.political_domain,
    region:                                  e.region,
    manipulation_score:                      manip,
    identity_score:                          identity,
    trauma_score:                            trauma,
    structural_score:                        structural,
    composite_score:                         comp,
    risk_level:                              risk,
    psycho_pattern:                          pattern,
    severity:                                severity(risk),
    recommended_action:                      recommendedAction(risk),
    signal:                                  signal(risk),
    mass_anxiety_political_exploitation:     e.mass_anxiety_political_exploitation,
    democratic_disillusionment_weaponization: e.democratic_disillusionment_weaponization,
  };
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(buildEntity);

    const risk_counts:    Record<string, number> = {};
    const pattern_counts: Record<string, number> = {};
    const severity_dist:  Record<string, number> = {};
    const action_counts:  Record<string, number> = {};
    let tManip = 0, tIdentity = 0, tTrauma = 0, tStructural = 0, tComp = 0;

    for (const ent of entities) {
      risk_counts[ent.risk_level]         = (risk_counts[ent.risk_level]         || 0) + 1;
      pattern_counts[ent.psycho_pattern]  = (pattern_counts[ent.psycho_pattern]  || 0) + 1;
      severity_dist[ent.severity]         = (severity_dist[ent.severity]         || 0) + 1;
      action_counts[ent.recommended_action] = (action_counts[ent.recommended_action] || 0) + 1;
      tManip      += ent.manipulation_score;
      tIdentity   += ent.identity_score;
      tTrauma     += ent.trauma_score;
      tStructural += ent.structural_score;
      tComp       += ent.composite_score;
    }

    const n = entities.length;
    const avgComp = tComp / n;

    const summary = {
      module_id:                         344,
      module_name:                       "Psychopolitics & Mass Psychology Intelligence Engine",
      total_entities:                    n,
      critical_count:                    risk_counts["critical"]  || 0,
      high_count:                        risk_counts["high"]      || 0,
      moderate_count:                    risk_counts["moderate"]  || 0,
      low_count:                         risk_counts["low"]       || 0,
      avg_composite:                     Math.round(avgComp * 100) / 100,
      pattern_distribution:              pattern_counts,
      risk_distribution:                 risk_counts,
      severity_distribution:             severity_dist,
      action_distribution:               action_counts,
      avg_estimated_psychopolitics_index: Math.round(avgComp / 100 * 10 * 100) / 100,
      avg_manipulation_score:            Math.round((tManip      / n) * 100) / 100,
      avg_identity_score:                Math.round((tIdentity   / n) * 100) / 100,
      avg_trauma_score:                  Math.round((tTrauma     / n) * 100) / 100,
      avg_structural_score:              Math.round((tStructural / n) * 100) / 100,
      results:                           entities,
    };

    return sealResponse(NextResponse.json(sealResponse(summary, "psychopolitics-engine")));
  }

  try {
    const res = await fetch(`${SWARM_API_URL}/psychopolitics-engine`, { cache: "no-store" });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    return sealResponse(NextResponse.json(sealResponse(await res.json(), "psychopolitics-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream psychopolitics intelligence unavailable" }, "psychopolitics-engine"),
      { status: 502 }
    ));
  }
}
