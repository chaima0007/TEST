import { NextResponse } from "next/server";

const MOCK_ORGANOIDS = [
  // OR-001 neural_organoid EMEA — critical/biological_collapse
  { organoid_id:"OR-001", substrate_type:"neural_organoid",   region:"EMEA",  viability_score:0.12, computational_coherence:0.20, biological_stability_rate:0.15, emergence_complexity_index:0.22, substrate_efficiency_score:0.18, mutation_drift_rate:0.80, cross_substrate_compatibility:0.20, signal_propagation_fidelity:0.18, metabolic_overhead_ratio:0.85, self_repair_capacity:0.10, information_density_score:0.15, temporal_resolution_score:0.20, noise_tolerance_level:0.18, bio_digital_interface_quality:0.12, replication_accuracy:0.15, environmental_sensitivity:0.88, evolutionary_adaptability:0.12 },
  // OR-002 dna_circuit NAMER — low
  { organoid_id:"OR-002", substrate_type:"dna_circuit",       region:"NAMER", viability_score:0.92, computational_coherence:0.90, biological_stability_rate:0.88, emergence_complexity_index:0.85, substrate_efficiency_score:0.90, mutation_drift_rate:0.08, cross_substrate_compatibility:0.88, signal_propagation_fidelity:0.92, metabolic_overhead_ratio:0.10, self_repair_capacity:0.90, information_density_score:0.88, temporal_resolution_score:0.92, noise_tolerance_level:0.90, bio_digital_interface_quality:0.88, replication_accuracy:0.95, environmental_sensitivity:0.08, evolutionary_adaptability:0.90 },
  // OR-003 synthetic_synapse APAC — high/computational_drift
  { organoid_id:"OR-003", substrate_type:"synthetic_synapse", region:"APAC",  viability_score:0.55, computational_coherence:0.28, biological_stability_rate:0.52, emergence_complexity_index:0.48, substrate_efficiency_score:0.45, mutation_drift_rate:0.52, cross_substrate_compatibility:0.50, signal_propagation_fidelity:0.30, metabolic_overhead_ratio:0.58, self_repair_capacity:0.48, information_density_score:0.32, temporal_resolution_score:0.45, noise_tolerance_level:0.42, bio_digital_interface_quality:0.40, replication_accuracy:0.55, environmental_sensitivity:0.58, evolutionary_adaptability:0.45 },
  // OR-004 mycelium_network LATAM — low
  { organoid_id:"OR-004", substrate_type:"mycelium_network",  region:"LATAM", viability_score:0.85, computational_coherence:0.82, biological_stability_rate:0.88, emergence_complexity_index:0.80, substrate_efficiency_score:0.85, mutation_drift_rate:0.12, cross_substrate_compatibility:0.82, signal_propagation_fidelity:0.85, metabolic_overhead_ratio:0.15, self_repair_capacity:0.88, information_density_score:0.80, temporal_resolution_score:0.85, noise_tolerance_level:0.88, bio_digital_interface_quality:0.80, replication_accuracy:0.90, environmental_sensitivity:0.12, evolutionary_adaptability:0.85 },
  // OR-005 protein_computer EMEA — critical/mutation_cascade
  { organoid_id:"OR-005", substrate_type:"protein_computer",  region:"EMEA",  viability_score:0.25, computational_coherence:0.30, biological_stability_rate:0.22, emergence_complexity_index:0.28, substrate_efficiency_score:0.20, mutation_drift_rate:0.82, cross_substrate_compatibility:0.25, signal_propagation_fidelity:0.28, metabolic_overhead_ratio:0.80, self_repair_capacity:0.18, information_density_score:0.25, temporal_resolution_score:0.28, noise_tolerance_level:0.22, bio_digital_interface_quality:0.20, replication_accuracy:0.20, environmental_sensitivity:0.82, evolutionary_adaptability:0.22 },
  // OR-006 quantum_bio MEA — moderate
  { organoid_id:"OR-006", substrate_type:"quantum_bio",       region:"MEA",   viability_score:0.62, computational_coherence:0.58, biological_stability_rate:0.60, emergence_complexity_index:0.55, substrate_efficiency_score:0.60, mutation_drift_rate:0.38, cross_substrate_compatibility:0.55, signal_propagation_fidelity:0.60, metabolic_overhead_ratio:0.42, self_repair_capacity:0.58, information_density_score:0.55, temporal_resolution_score:0.60, noise_tolerance_level:0.58, bio_digital_interface_quality:0.55, replication_accuracy:0.65, environmental_sensitivity:0.38, evolutionary_adaptability:0.58 },
  // OR-007 membrane_processor NAMER — high/substrate_incompatibility
  { organoid_id:"OR-007", substrate_type:"membrane_processor",region:"NAMER", viability_score:0.48, computational_coherence:0.50, biological_stability_rate:0.45, emergence_complexity_index:0.42, substrate_efficiency_score:0.28, mutation_drift_rate:0.55, cross_substrate_compatibility:0.28, signal_propagation_fidelity:0.50, metabolic_overhead_ratio:0.62, self_repair_capacity:0.42, information_density_score:0.45, temporal_resolution_score:0.48, noise_tolerance_level:0.40, bio_digital_interface_quality:0.38, replication_accuracy:0.48, environmental_sensitivity:0.58, evolutionary_adaptability:0.40 },
  // OR-008 hybrid_wetware APAC — low
  { organoid_id:"OR-008", substrate_type:"hybrid_wetware",    region:"APAC",  viability_score:0.88, computational_coherence:0.85, biological_stability_rate:0.90, emergence_complexity_index:0.82, substrate_efficiency_score:0.88, mutation_drift_rate:0.10, cross_substrate_compatibility:0.85, signal_propagation_fidelity:0.88, metabolic_overhead_ratio:0.12, self_repair_capacity:0.92, information_density_score:0.85, temporal_resolution_score:0.88, noise_tolerance_level:0.90, bio_digital_interface_quality:0.85, replication_accuracy:0.92, environmental_sensitivity:0.10, evolutionary_adaptability:0.88 },
];

type Organoid = typeof MOCK_ORGANOIDS[0];

function viabilityScore(o: Organoid): number {
  const raw = (o.viability_score + o.biological_stability_rate + o.self_repair_capacity) / 3;
  return Math.min(Math.round((1 - raw) * 100 * 100) / 100, 100);
}
function computationScore(o: Organoid): number {
  const raw = (o.computational_coherence + o.information_density_score + o.signal_propagation_fidelity) / 3;
  return Math.min(Math.round((1 - raw) * 100 * 100) / 100, 100);
}
function stabilityScore(o: Organoid): number {
  const raw = (o.mutation_drift_rate + o.environmental_sensitivity + (1 - o.replication_accuracy)) / 3;
  return Math.min(Math.round(raw * 100 * 100) / 100, 100);
}
function emergenceScore(o: Organoid): number {
  const raw = (o.emergence_complexity_index + o.evolutionary_adaptability + o.cross_substrate_compatibility) / 3;
  return Math.min(Math.round((1 - raw) * 100 * 100) / 100, 100);
}
function bioComposite(v: number, c: number, s: number, e: number): number {
  return Math.min(Math.round((v * 0.30 + c * 0.25 + s * 0.25 + e * 0.20) * 100) / 100, 100);
}
function bioPattern(o: Organoid): string {
  if (o.viability_score <= 0.30 && o.biological_stability_rate <= 0.30) return "biological_collapse";
  if (o.computational_coherence <= 0.35 || o.signal_propagation_fidelity <= 0.35) return "computational_drift";
  if (o.mutation_drift_rate >= 0.65 || o.replication_accuracy <= 0.35) return "mutation_cascade";
  if (o.cross_substrate_compatibility <= 0.35 && o.substrate_efficiency_score <= 0.35) return "substrate_incompatibility";
  if (o.emergence_complexity_index <= 0.30 && o.evolutionary_adaptability <= 0.30) return "emergence_suppression";
  return "none";
}
function bioRisk(comp: number): string { if (comp >= 60) return "critical"; if (comp >= 40) return "high"; if (comp >= 20) return "moderate"; return "low"; }
function bioSeverity(comp: number): string { if (comp >= 60) return "collapsing"; if (comp >= 40) return "degrading"; if (comp >= 20) return "adapting"; return "thriving"; }
function bioAction(risk: string, pat: string): string {
  if (risk === "critical") {
    if (pat === "biological_collapse") return "emergency_stabilization";
    return "substrate_isolation";
  }
  if (risk === "high") {
    if (pat === "mutation_cascade")          return "mutation_containment";
    if (pat === "substrate_incompatibility") return "bio_circuit_reset";
    return "bio_circuit_reset";
  }
  if (risk === "moderate") return "viability_monitoring";
  return "no_action";
}
function bioSignal(o: Organoid, pat: string, comp: number): string {
  if (comp < 20) return "Organoïde bio-computationnel stable — viabilité confirmée, cohérence maximale, émergence contrôlée";
  const labels: Record<string,string> = {
    biological_collapse:      "Effondrement biologique",
    computational_drift:      "Dérive computationnelle",
    mutation_cascade:         "Cascade mutationnelle",
    substrate_incompatibility: "Incompatibilité substrat",
    emergence_suppression:    "Suppression d'émergence",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — viabilité ${o.viability_score.toFixed(2)} — cohérence ${o.computational_coherence.toFixed(2)} — dérive mutation ${o.mutation_drift_rate.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const organoids = MOCK_ORGANOIDS.map(o => {
      const vs = viabilityScore(o), cs = computationScore(o), ss = stabilityScore(o), es = emergenceScore(o);
      const comp = bioComposite(vs, cs, ss, es), pat = bioPattern(o), risk = bioRisk(comp), sev = bioSeverity(comp), act = bioAction(risk, pat);
      const collapseIndex = Math.min(Math.round(comp / 100 * (o.mutation_drift_rate + o.environmental_sensitivity) / 2 * 10 * 100) / 100, 10.0);
      return {
        organoid_id: o.organoid_id, substrate_type: o.substrate_type, region: o.region,
        bio_risk: risk, bio_pattern: pat, bio_severity: sev, recommended_action: act,
        viability_sub_score: vs, computation_sub_score: cs, stability_sub_score: ss, emergence_sub_score: es,
        bio_composite: comp,
        critical_collapse_risk: risk === "critical",
        requires_emergency: act === "emergency_stabilization" || act === "substrate_isolation",
        estimated_collapse_index: collapseIndex,
        bio_signal: bioSignal(o, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tv=0, tc=0, ts=0, te=0, tcomp=0, tci=0, collapseC=0, emergC=0;
    for (const org of organoids) {
      rc[org.bio_risk]          = (rc[org.bio_risk]          || 0) + 1;
      pc[org.bio_pattern]       = (pc[org.bio_pattern]       || 0) + 1;
      sc[org.bio_severity]      = (sc[org.bio_severity]      || 0) + 1;
      ac[org.recommended_action]= (ac[org.recommended_action]|| 0) + 1;
      tv += org.viability_sub_score; tc += org.computation_sub_score;
      ts += org.stability_sub_score; te += org.emergence_sub_score;
      tcomp += org.bio_composite; tci += org.estimated_collapse_index;
      if (org.critical_collapse_risk) collapseC++;
      if (org.requires_emergency)     emergC++;
    }
    const n = organoids.length;
    return NextResponse.json({ organoids, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_bio_composite: Math.round(tcomp / n * 10) / 10,
      critical_collapse_count: collapseC, emergency_count: emergC,
      avg_viability_score:   Math.round(tv / n * 10) / 10,
      avg_computation_score: Math.round(tc / n * 10) / 10,
      avg_stability_score:   Math.round(ts / n * 10) / 10,
      avg_emergence_score:   Math.round(te / n * 10) / 10,
      avg_estimated_collapse_index: Math.round(tci / n * 100) / 100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/bio-computational-intelligence-engine`)).json());
}
