import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // CM-001: EMEA, oral_traditions → critical, civilizational_amnesia
  { entity_id:"CM-001", heritage_category:"oral_traditions", region:"EMEA",
    memory_preservation_rate:0.12, cultural_transmission_fidelity:0.20, knowledge_erosion_rate:0.82,
    digital_archival_completeness:0.15, intergenerational_transfer:0.18, linguistic_vitality:0.22,
    oral_tradition_preservation:0.15, artifact_integrity:0.30, collective_identity_coherence:0.20,
    cultural_innovation_rate:0.25, heritage_monetization_potential:0.40, diaspora_network_strength:0.28,
    institutional_fragility:0.80, memory_distortion_rate:0.78, cultural_resilience:0.15,
    knowledge_accessibility:0.18, narrative_coherence:0.20 },
  // CM-002: APAC, written_heritage → low, vibrant_heritage/none
  { entity_id:"CM-002", heritage_category:"written_heritage", region:"APAC",
    memory_preservation_rate:0.92, cultural_transmission_fidelity:0.90, knowledge_erosion_rate:0.08,
    digital_archival_completeness:0.92, intergenerational_transfer:0.88, linguistic_vitality:0.92,
    oral_tradition_preservation:0.90, artifact_integrity:0.92, collective_identity_coherence:0.90,
    cultural_innovation_rate:0.88, heritage_monetization_potential:0.30, diaspora_network_strength:0.85,
    institutional_fragility:0.10, memory_distortion_rate:0.08, cultural_resilience:0.92,
    knowledge_accessibility:0.90, narrative_coherence:0.90 },
  // CM-003: NOAM, indigenous_knowledge → high, cultural_fragmentation
  { entity_id:"CM-003", heritage_category:"indigenous_knowledge", region:"NOAM",
    memory_preservation_rate:0.38, cultural_transmission_fidelity:0.42, knowledge_erosion_rate:0.52,
    digital_archival_completeness:0.35, intergenerational_transfer:0.40, linguistic_vitality:0.48,
    oral_tradition_preservation:0.38, artifact_integrity:0.55, collective_identity_coherence:0.28,
    cultural_innovation_rate:0.45, heritage_monetization_potential:0.38, diaspora_network_strength:0.42,
    institutional_fragility:0.58, memory_distortion_rate:0.48, cultural_resilience:0.35,
    knowledge_accessibility:0.38, narrative_coherence:0.32 },
  // CM-004: LATAM, digital_archives → low, vibrant_heritage/none
  { entity_id:"CM-004", heritage_category:"digital_archives", region:"LATAM",
    memory_preservation_rate:0.88, cultural_transmission_fidelity:0.85, knowledge_erosion_rate:0.10,
    digital_archival_completeness:0.95, intergenerational_transfer:0.82, linguistic_vitality:0.88,
    oral_tradition_preservation:0.80, artifact_integrity:0.90, collective_identity_coherence:0.85,
    cultural_innovation_rate:0.80, heritage_monetization_potential:0.25, diaspora_network_strength:0.78,
    institutional_fragility:0.12, memory_distortion_rate:0.10, cultural_resilience:0.88,
    knowledge_accessibility:0.85, narrative_coherence:0.85 },
  // CM-005: MEA, linguistic_heritage → critical, linguistic_extinction
  { entity_id:"CM-005", heritage_category:"linguistic_heritage", region:"MEA",
    memory_preservation_rate:0.55, cultural_transmission_fidelity:0.50, knowledge_erosion_rate:0.45,
    digital_archival_completeness:0.20, intergenerational_transfer:0.45, linguistic_vitality:0.08,
    oral_tradition_preservation:0.42, artifact_integrity:0.35, collective_identity_coherence:0.45,
    cultural_innovation_rate:0.20, heritage_monetization_potential:0.35, diaspora_network_strength:0.30,
    institutional_fragility:0.88, memory_distortion_rate:0.72, cultural_resilience:0.12,
    knowledge_accessibility:0.15, narrative_coherence:0.48 },
  // CM-006: EMEA, material_culture → moderate, none
  { entity_id:"CM-006", heritage_category:"material_culture", region:"EMEA",
    memory_preservation_rate:0.62, cultural_transmission_fidelity:0.65, knowledge_erosion_rate:0.32,
    digital_archival_completeness:0.58, intergenerational_transfer:0.60, linguistic_vitality:0.68,
    oral_tradition_preservation:0.62, artifact_integrity:0.72, collective_identity_coherence:0.65,
    cultural_innovation_rate:0.60, heritage_monetization_potential:0.45, diaspora_network_strength:0.58,
    institutional_fragility:0.38, memory_distortion_rate:0.30, cultural_resilience:0.62,
    knowledge_accessibility:0.60, narrative_coherence:0.65 },
  // CM-007: APAC, performing_arts → high, transmission_collapse
  { entity_id:"CM-007", heritage_category:"performing_arts", region:"APAC",
    memory_preservation_rate:0.42, cultural_transmission_fidelity:0.30, knowledge_erosion_rate:0.48,
    digital_archival_completeness:0.40, intergenerational_transfer:0.28, linguistic_vitality:0.55,
    oral_tradition_preservation:0.32, artifact_integrity:0.60, collective_identity_coherence:0.50,
    cultural_innovation_rate:0.45, heritage_monetization_potential:0.40, diaspora_network_strength:0.38,
    institutional_fragility:0.55, memory_distortion_rate:0.42, cultural_resilience:0.38,
    knowledge_accessibility:0.40, narrative_coherence:0.50 },
  // CM-008: NOAM, oral_traditions → critical, heritage_commodification_risk
  { entity_id:"CM-008", heritage_category:"oral_traditions", region:"NOAM",
    memory_preservation_rate:0.52, cultural_transmission_fidelity:0.22, knowledge_erosion_rate:0.48,
    digital_archival_completeness:0.20, intergenerational_transfer:0.25, linguistic_vitality:0.38,
    oral_tradition_preservation:0.20, artifact_integrity:0.32, collective_identity_coherence:0.22,
    cultural_innovation_rate:0.30, heritage_monetization_potential:0.82, diaspora_network_strength:0.35,
    institutional_fragility:0.88, memory_distortion_rate:0.78, cultural_resilience:0.12,
    knowledge_accessibility:0.15, narrative_coherence:0.55 },
];

type Entity = typeof MOCK_ENTITIES[0];

function preservationScore(e: Entity): number {
  const raw = (
    e.knowledge_erosion_rate * 0.4
    + e.memory_distortion_rate * 0.3
    + (1 - e.memory_preservation_rate) * 0.3
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function transmissionScore(e: Entity): number {
  const raw = (
    (1 - e.cultural_transmission_fidelity) * 0.4
    + (1 - e.intergenerational_transfer) * 0.35
    + (1 - e.oral_tradition_preservation) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function identityScore(e: Entity): number {
  const raw = (
    (1 - e.collective_identity_coherence) * 0.4
    + (1 - e.linguistic_vitality) * 0.35
    + (1 - e.narrative_coherence) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function resilienceScore(e: Entity): number {
  const raw = (
    (1 - e.cultural_resilience) * 0.4
    + e.institutional_fragility * 0.35
    + (1 - e.knowledge_accessibility) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function composite(pres: number, trans: number, ident: number, resil: number): number {
  return Math.round((pres * 0.30 + trans * 0.25 + ident * 0.25 + resil * 0.20) * 100) / 100;
}
function memoryPattern(e: Entity): string {
  if (e.knowledge_erosion_rate >= 0.65 && (1 - e.memory_preservation_rate) >= 0.55) return "civilizational_amnesia";
  if ((1 - e.collective_identity_coherence) >= 0.65 && (1 - e.narrative_coherence) >= 0.55) return "cultural_fragmentation";
  if ((1 - e.intergenerational_transfer) >= 0.65 && (1 - e.cultural_transmission_fidelity) >= 0.55) return "transmission_collapse";
  if ((1 - e.linguistic_vitality) >= 0.70) return "linguistic_extinction";
  if (e.heritage_monetization_potential >= 0.70 && (1 - e.artifact_integrity) >= 0.55) return "heritage_commodification_risk";
  return "none";
}
function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function severity(comp: number): string {
  if (comp >= 75) return "civilizational_crisis";
  if (comp >= 50) return "high_erosion";
  if (comp >= 25) return "developing_loss";
  return "vibrant_heritage";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "civilizational_emergency";
  if (risk === "high") {
    if (pattern === "civilizational_amnesia") return "emergency_archival";
    return "cultural_preservation_program";
  }
  if (risk === "moderate") return "heritage_monitoring";
  return "no_action";
}
function memorySignal(e: Entity, risk: string, comp: number): string {
  if (risk === "critical") {
    return `Critique — préservation mémoire ${Math.round(e.memory_preservation_rate * 100)}% — transmission culturelle ${Math.round(e.cultural_transmission_fidelity * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — vitalité linguistique ${Math.round(e.linguistic_vitality * 100)}% — cohérence identitaire ${Math.round(e.collective_identity_coherence * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — taux d'érosion ${Math.round(e.knowledge_erosion_rate * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Mémoire civilisationnelle préservée — transmission culturelle forte, identité collective cohérente";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const pres  = preservationScore(e);
      const trans = transmissionScore(e);
      const ident = identityScore(e);
      const resil = resilienceScore(e);
      const comp  = composite(pres, trans, ident, resil);
      const pat   = memoryPattern(e);
      const risk  = riskLevel(comp);
      const sev   = severity(comp);
      const act   = recommendedAction(risk, pat);
      return {
        entity_id:                      e.entity_id,
        region:                         e.region,
        heritage_category:              e.heritage_category,
        memory_risk:                    risk,
        memory_pattern:                 pat,
        memory_severity:                sev,
        recommended_action:             act,
        preservation_score:             pres,
        transmission_score:             trans,
        identity_score:                 ident,
        resilience_score:               resil,
        memory_composite:               comp,
        is_in_memory_crisis:            comp >= 60,
        requires_heritage_intervention: comp >= 40,
        memory_signal:                  memorySignal(e, risk, comp),
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tComp=0, tPres=0, tTrans=0, tIdent=0, tResil=0, crisisC=0, interventionC=0;
    for (const ent of entities) {
      rc[ent.memory_risk]        = (rc[ent.memory_risk]        || 0) + 1;
      pc[ent.memory_pattern]     = (pc[ent.memory_pattern]     || 0) + 1;
      sc[ent.memory_severity]    = (sc[ent.memory_severity]    || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tComp  += ent.memory_composite;
      tPres  += ent.preservation_score;
      tTrans += ent.transmission_score;
      tIdent += ent.identity_score;
      tResil += ent.resilience_score;
      if (ent.is_in_memory_crisis)            crisisC++;
      if (ent.requires_heritage_intervention) interventionC++;
    }
    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                           n,
      risk_counts:                     rc,
      pattern_counts:                  pc,
      severity_counts:                 sc,
      action_counts:                   ac,
      avg_memory_composite:            Math.round(avgComp * 10) / 10,
      memory_crisis_count:             crisisC,
      heritage_intervention_count:     interventionC,
      avg_preservation_score:          Math.round(tPres / n * 10) / 10,
      avg_transmission_score:          Math.round(tTrans / n * 10) / 10,
      avg_identity_score:              Math.round(tIdent / n * 10) / 10,
      avg_resilience_score:            Math.round(tResil / n * 10) / 10,
      avg_estimated_memory_loss_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };
    return NextResponse.json(sealResponse({ entities, summary }, "civilizational-memory-engine"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/civilizational-memory-engine`);
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    return NextResponse.json(sealResponse(await res.json(), "civilizational-memory-engine"));
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream unavailable" }, "civilizational-memory-engine"), { status: 502 });
  }
}
