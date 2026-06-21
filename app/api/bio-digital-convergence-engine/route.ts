import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // BDC-001 — EMEA, biocomputing → critical, bio_digital_desync
  { id:"BDC-001", convergence_domain:"biocomputing", region:"EMEA",
    bio_integration_rate:0.10, digital_twin_fidelity:0.20, synthetic_viability:0.30,
    biocompute_efficiency:0.28, dna_data_density:0.25, neural_coupling_depth:0.20,
    bio_signal_clarity:0.18, organic_error_rate:0.72, cellular_adaptation:0.22,
    protein_fold_accuracy:0.25, evolutionary_drift:0.60, regulatory_compliance_bio:0.30,
    containment_integrity:0.35, cross_domain_coherence:0.28, emergence_risk:0.62,
    biological_instability:0.82, interface_degradation:0.75 },
  // BDC-002 — APAC, synthetic_biology → low, none
  { id:"BDC-002", convergence_domain:"synthetic_biology", region:"APAC",
    bio_integration_rate:0.92, digital_twin_fidelity:0.88, synthetic_viability:0.90,
    biocompute_efficiency:0.88, dna_data_density:0.85, neural_coupling_depth:0.82,
    bio_signal_clarity:0.88, organic_error_rate:0.08, cellular_adaptation:0.90,
    protein_fold_accuracy:0.92, evolutionary_drift:0.10, regulatory_compliance_bio:0.90,
    containment_integrity:0.92, cross_domain_coherence:0.90, emergence_risk:0.08,
    biological_instability:0.08, interface_degradation:0.10 },
  // BDC-003 — NOAM, neural_coupling → high, synthetic_collapse
  { id:"BDC-003", convergence_domain:"neural_coupling", region:"NOAM",
    bio_integration_rate:0.38, digital_twin_fidelity:0.42, synthetic_viability:0.28,
    biocompute_efficiency:0.40, dna_data_density:0.38, neural_coupling_depth:0.32,
    bio_signal_clarity:0.35, organic_error_rate:0.62, cellular_adaptation:0.40,
    protein_fold_accuracy:0.42, evolutionary_drift:0.48, regulatory_compliance_bio:0.40,
    containment_integrity:0.45, cross_domain_coherence:0.38, emergence_risk:0.52,
    biological_instability:0.55, interface_degradation:0.50 },
  // BDC-004 — LATAM, biocomputing → low, none
  { id:"BDC-004", convergence_domain:"biocomputing", region:"LATAM",
    bio_integration_rate:0.85, digital_twin_fidelity:0.82, synthetic_viability:0.88,
    biocompute_efficiency:0.85, dna_data_density:0.80, neural_coupling_depth:0.78,
    bio_signal_clarity:0.82, organic_error_rate:0.12, cellular_adaptation:0.88,
    protein_fold_accuracy:0.85, evolutionary_drift:0.12, regulatory_compliance_bio:0.85,
    containment_integrity:0.88, cross_domain_coherence:0.85, emergence_risk:0.12,
    biological_instability:0.10, interface_degradation:0.12 },
  // BDC-005 — MEA, synthetic_biology → critical, biocompute_failure
  { id:"BDC-005", convergence_domain:"synthetic_biology", region:"MEA",
    bio_integration_rate:0.18, digital_twin_fidelity:0.15, synthetic_viability:0.50,
    biocompute_efficiency:0.12, dna_data_density:0.18, neural_coupling_depth:0.15,
    bio_signal_clarity:0.12, organic_error_rate:0.40, cellular_adaptation:0.20,
    protein_fold_accuracy:0.15, evolutionary_drift:0.55, regulatory_compliance_bio:0.20,
    containment_integrity:0.25, cross_domain_coherence:0.18, emergence_risk:0.68,
    biological_instability:0.60, interface_degradation:0.70 },
  // BDC-006 — EMEA, neural_coupling → moderate, none
  { id:"BDC-006", convergence_domain:"neural_coupling", region:"EMEA",
    bio_integration_rate:0.68, digital_twin_fidelity:0.65, synthetic_viability:0.72,
    biocompute_efficiency:0.68, dna_data_density:0.65, neural_coupling_depth:0.70,
    bio_signal_clarity:0.68, organic_error_rate:0.30, cellular_adaptation:0.70,
    protein_fold_accuracy:0.68, evolutionary_drift:0.28, regulatory_compliance_bio:0.70,
    containment_integrity:0.72, cross_domain_coherence:0.68, emergence_risk:0.28,
    biological_instability:0.25, interface_degradation:0.30 },
  // BDC-007 — APAC, dna_computing → high, emergence_cascade
  { id:"BDC-007", convergence_domain:"dna_computing", region:"APAC",
    bio_integration_rate:0.40, digital_twin_fidelity:0.38, synthetic_viability:0.45,
    biocompute_efficiency:0.42, dna_data_density:0.40, neural_coupling_depth:0.35,
    bio_signal_clarity:0.38, organic_error_rate:0.55, cellular_adaptation:0.42,
    protein_fold_accuracy:0.40, evolutionary_drift:0.50, regulatory_compliance_bio:0.42,
    containment_integrity:0.35, cross_domain_coherence:0.40, emergence_risk:0.72,
    biological_instability:0.58, interface_degradation:0.52 },
  // BDC-008 — NOAM, biocomputing → critical, evolutionary_drift
  { id:"BDC-008", convergence_domain:"biocomputing", region:"NOAM",
    bio_integration_rate:0.22, digital_twin_fidelity:0.18, synthetic_viability:0.45,
    biocompute_efficiency:0.42, dna_data_density:0.20, neural_coupling_depth:0.18,
    bio_signal_clarity:0.20, organic_error_rate:0.50, cellular_adaptation:0.18,
    protein_fold_accuracy:0.45, evolutionary_drift:0.82, regulatory_compliance_bio:0.25,
    containment_integrity:0.30, cross_domain_coherence:0.22, emergence_risk:0.60,
    biological_instability:0.60, interface_degradation:0.70 },
];

type Entity = typeof MOCK_ENTITIES[0];

function integrationScore(e: Entity): number {
  const raw = (
    e.biological_instability * 0.4 +
    e.interface_degradation * 0.3 +
    (1 - e.bio_integration_rate) * 0.3
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function syntheticScore(e: Entity): number {
  const raw = (
    (1 - e.synthetic_viability) * 0.4 +
    e.organic_error_rate * 0.35 +
    e.evolutionary_drift * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function biocomputeScore(e: Entity): number {
  const raw = (
    (1 - e.biocompute_efficiency) * 0.4 +
    (1 - e.protein_fold_accuracy) * 0.3 +
    (1 - e.dna_data_density) * 0.3
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function coherenceScore(e: Entity): number {
  const raw = (
    (1 - e.cross_domain_coherence) * 0.4 +
    e.emergence_risk * 0.35 +
    (1 - e.containment_integrity) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function composite(intg: number, syn: number, bio: number, coh: number): number {
  return Math.round((intg * 0.30 + syn * 0.25 + bio * 0.25 + coh * 0.20) * 100) / 100;
}
function convergenceRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function convergencePattern(e: Entity): string {
  if (e.biological_instability >= 0.65 && (1 - e.bio_integration_rate) >= 0.55) return "bio_digital_desync";
  if ((1 - e.synthetic_viability) >= 0.65 && e.organic_error_rate >= 0.55) return "synthetic_collapse";
  if ((1 - e.biocompute_efficiency) >= 0.65 && (1 - e.protein_fold_accuracy) >= 0.55) return "biocompute_failure";
  if (e.emergence_risk >= 0.65 && (1 - e.containment_integrity) >= 0.50) return "emergence_cascade";
  if (e.evolutionary_drift >= 0.65 && (1 - e.cellular_adaptation) >= 0.55) return "evolutionary_drift";
  return "none";
}
function convergenceSeverity(comp: number): string {
  if (comp >= 75) return "critical_divergence";
  if (comp >= 50) return "high_instability";
  if (comp >= 25) return "developing_risk";
  return "stable_convergence";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "bio_digital_emergency";
  if (risk === "high") {
    if (pattern === "emergence_cascade") return "containment_protocol";
    return "convergence_stabilization";
  }
  if (risk === "moderate") return "bio_monitoring";
  return "no_action";
}
function convergenceSignal(e: Entity, risk: string, comp: number): string {
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — intégration bio-digitale ${Math.round(e.bio_integration_rate*100)}% — viabilité synthétique ${Math.round(e.synthetic_viability*100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — dérive évolutive ${Math.round(e.evolutionary_drift*100)}% — cohérence domaines ${Math.round(e.cross_domain_coherence*100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — efficacité biocompute ${Math.round(e.biocompute_efficiency*100)}% — composite ${compInt}`;
  }
  return "Convergence bio-digitale optimale — systèmes synthétiques stables, biocomputing performant";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const intg = integrationScore(e);
      const syn  = syntheticScore(e);
      const bio  = biocomputeScore(e);
      const coh  = coherenceScore(e);
      const comp = composite(intg, syn, bio, coh);
      const pat  = convergencePattern(e);
      const risk = convergenceRisk(comp);
      const sev  = convergenceSeverity(comp);
      const act  = recommendedAction(risk, pat);
      return {
        id:                 e.entity_id,
        region:                    e.region,
        convergence_domain:        e.convergence_domain,
        convergence_risk:          risk,
        convergence_pattern:       pat,
        convergence_severity:      sev,
        recommended_action:        act,
        integration_score:         intg,
        synthetic_score:           syn,
        biocompute_score:          bio,
        coherence_score:           coh,
        convergence_composite:     comp,
        is_in_convergence_crisis:  comp >= 60,
        requires_bio_intervention: comp >= 40,
        convergence_signal:        convergenceSignal(e, risk, comp),
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tIntg=0, tSyn=0, tBio=0, tCoh=0, tComp=0, crisisC=0, interventionC=0;
    for (const ent of entities) {
      rc[ent.convergence_risk]    = (rc[ent.convergence_risk]    || 0) + 1;
      pc[ent.convergence_pattern] = (pc[ent.convergence_pattern] || 0) + 1;
      sc[ent.convergence_severity]= (sc[ent.convergence_severity]|| 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tIntg += ent.integration_score;
      tSyn  += ent.synthetic_score;
      tBio  += ent.biocompute_score;
      tCoh  += ent.coherence_score;
      tComp += ent.convergence_composite;
      if (ent.is_in_convergence_crisis)  crisisC++;
      if (ent.requires_bio_intervention) interventionC++;
    }
    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                              n,
      risk_counts:                        rc,
      pattern_counts:                     pc,
      severity_counts:                    sc,
      action_counts:                      ac,
      avg_convergence_composite:          Math.round(avgComp * 10) / 10,
      convergence_crisis_count:           crisisC,
      bio_intervention_required_count:    interventionC,
      avg_integration_score:              Math.round(tIntg / n * 10) / 10,
      avg_synthetic_score:                Math.round(tSyn  / n * 10) / 10,
      avg_biocompute_score:               Math.round(tBio  / n * 10) / 10,
      avg_coherence_score:                Math.round(tCoh  / n * 10) / 10,
      avg_estimated_bio_digital_index:    Math.round(avgComp / 100 * 10 * 100) / 100,
    };
    return NextResponse.json(sealResponse({ entities, summary }, "bio-digital-convergence-engine"));
  }
  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/bio-digital-convergence-engine`);
    if (!upstream.ok) throw new Error(`upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "bio-digital-convergence-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "upstream unavailable" }, "bio-digital-convergence-engine"),
      { status: 502 }
    );
  }
}
