import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ORGANISMS = [
  // BMS-001 swarm_intelligence EMEA — critical extinction_spiral
  { organism_id:"BMS-001", strategy_archetype:"swarm_intelligence",    region:"EMEA",  adaptive_mutation_rate:0.12, environmental_fit_score:0.18, competitive_selection_pressure:0.82, symbiotic_partnership_depth:0.15, resource_efficiency_ratio:0.20, extinction_vulnerability:0.88, niche_differentiation_score:0.15, resilience_redundancy:0.18, swarm_coordination_score:0.20, phenotypic_plasticity:0.15, territorial_defense_strength:0.18, information_propagation_speed:0.15, energy_metabolism_efficiency:0.20, coevolution_readiness:0.12, biodiversity_analog_score:0.15, regeneration_capacity:0.18, ecological_dominance_index:0.15 },
  // BMS-002 evolutionary_selection NAMER — low thriving
  { organism_id:"BMS-002", strategy_archetype:"evolutionary_selection", region:"NAMER", adaptive_mutation_rate:0.88, environmental_fit_score:0.92, competitive_selection_pressure:0.10, symbiotic_partnership_depth:0.90, resource_efficiency_ratio:0.88, extinction_vulnerability:0.05, niche_differentiation_score:0.92, resilience_redundancy:0.90, swarm_coordination_score:0.88, phenotypic_plasticity:0.90, territorial_defense_strength:0.85, information_propagation_speed:0.90, energy_metabolism_efficiency:0.88, coevolution_readiness:0.90, biodiversity_analog_score:0.88, regeneration_capacity:0.92, ecological_dominance_index:0.90 },
  // BMS-003 predator_prey_dynamics APAC — high niche_collapse
  { organism_id:"BMS-003", strategy_archetype:"predator_prey_dynamics", region:"APAC",  adaptive_mutation_rate:0.28, environmental_fit_score:0.42, competitive_selection_pressure:0.65, symbiotic_partnership_depth:0.35, resource_efficiency_ratio:0.48, extinction_vulnerability:0.58, niche_differentiation_score:0.22, resilience_redundancy:0.38, swarm_coordination_score:0.40, phenotypic_plasticity:0.35, territorial_defense_strength:0.42, information_propagation_speed:0.38, energy_metabolism_efficiency:0.45, coevolution_readiness:0.30, biodiversity_analog_score:0.35, regeneration_capacity:0.40, ecological_dominance_index:0.30 },
  // BMS-004 mycelial_network LATAM — moderate adapting
  { organism_id:"BMS-004", strategy_archetype:"mycelial_network",       region:"LATAM", adaptive_mutation_rate:0.45, environmental_fit_score:0.55, competitive_selection_pressure:0.50, symbiotic_partnership_depth:0.48, resource_efficiency_ratio:0.52, extinction_vulnerability:0.35, niche_differentiation_score:0.55, resilience_redundancy:0.48, swarm_coordination_score:0.52, phenotypic_plasticity:0.55, territorial_defense_strength:0.58, information_propagation_speed:0.48, energy_metabolism_efficiency:0.55, coevolution_readiness:0.52, biodiversity_analog_score:0.50, regeneration_capacity:0.52, ecological_dominance_index:0.55 },
  // BMS-005 symbiotic_alliance MEA — critical symbiosis_breakdown
  { organism_id:"BMS-005", strategy_archetype:"symbiotic_alliance",     region:"MEA",   adaptive_mutation_rate:0.20, environmental_fit_score:0.40, competitive_selection_pressure:0.75, symbiotic_partnership_depth:0.18, resource_efficiency_ratio:0.22, extinction_vulnerability:0.80, niche_differentiation_score:0.55, resilience_redundancy:0.20, swarm_coordination_score:0.22, phenotypic_plasticity:0.18, territorial_defense_strength:0.22, information_propagation_speed:0.20, energy_metabolism_efficiency:0.25, coevolution_readiness:0.18, biodiversity_analog_score:0.20, regeneration_capacity:0.22, ecological_dominance_index:0.42 },
  // BMS-006 camouflage_strategy EMEA — moderate none
  { organism_id:"BMS-006", strategy_archetype:"camouflage_strategy",    region:"EMEA",  adaptive_mutation_rate:0.52, environmental_fit_score:0.58, competitive_selection_pressure:0.42, symbiotic_partnership_depth:0.55, resource_efficiency_ratio:0.50, extinction_vulnerability:0.38, niche_differentiation_score:0.55, resilience_redundancy:0.52, swarm_coordination_score:0.55, phenotypic_plasticity:0.50, territorial_defense_strength:0.55, information_propagation_speed:0.52, energy_metabolism_efficiency:0.55, coevolution_readiness:0.50, biodiversity_analog_score:0.52, regeneration_capacity:0.55, ecological_dominance_index:0.50 },
  // BMS-007 migration_adaptation NAMER — high evolutionary_stagnation
  { organism_id:"BMS-007", strategy_archetype:"migration_adaptation",   region:"NAMER", adaptive_mutation_rate:0.25, environmental_fit_score:0.48, competitive_selection_pressure:0.60, symbiotic_partnership_depth:0.40, resource_efficiency_ratio:0.45, extinction_vulnerability:0.55, niche_differentiation_score:0.42, resilience_redundancy:0.40, swarm_coordination_score:0.45, phenotypic_plasticity:0.28, territorial_defense_strength:0.38, information_propagation_speed:0.42, energy_metabolism_efficiency:0.48, coevolution_readiness:0.28, biodiversity_analog_score:0.40, regeneration_capacity:0.42, ecological_dominance_index:0.38 },
  // BMS-008 regenerative_cycle APAC — critical territorial_loss
  { organism_id:"BMS-008", strategy_archetype:"regenerative_cycle",     region:"APAC",  adaptive_mutation_rate:0.15, environmental_fit_score:0.38, competitive_selection_pressure:0.78, symbiotic_partnership_depth:0.55, resource_efficiency_ratio:0.18, extinction_vulnerability:0.55, niche_differentiation_score:0.55, resilience_redundancy:0.22, swarm_coordination_score:0.45, phenotypic_plasticity:0.40, territorial_defense_strength:0.15, information_propagation_speed:0.22, energy_metabolism_efficiency:0.18, coevolution_readiness:0.20, biodiversity_analog_score:0.18, regeneration_capacity:0.20, ecological_dominance_index:0.22 },
];

type Organism = typeof MOCK_ORGANISMS[0];

function fitnessScore(o: Organism): number {
  let s = 0;
  if      (o.environmental_fit_score <= 0.25) s += 40; else if (o.environmental_fit_score <= 0.50) s += 22; else if (o.environmental_fit_score <= 0.70) s += 8;
  if      (o.extinction_vulnerability >= 0.70) s += 35; else if (o.extinction_vulnerability >= 0.45) s += 18; else if (o.extinction_vulnerability >= 0.20) s += 6;
  if      (o.competitive_selection_pressure >= 0.70) s += 25; else if (o.competitive_selection_pressure >= 0.45) s += 12;
  return Math.min(s, 100);
}
function adaptationScore(o: Organism): number {
  let s = 0;
  if      (o.adaptive_mutation_rate <= 0.25) s += 40; else if (o.adaptive_mutation_rate <= 0.50) s += 22; else if (o.adaptive_mutation_rate <= 0.70) s += 8;
  if      (o.phenotypic_plasticity <= 0.25) s += 35; else if (o.phenotypic_plasticity <= 0.50) s += 18; else if (o.phenotypic_plasticity <= 0.70) s += 6;
  if      (o.coevolution_readiness <= 0.25) s += 25; else if (o.coevolution_readiness <= 0.50) s += 12;
  return Math.min(s, 100);
}
function resilienceScore(o: Organism): number {
  let s = 0;
  if      (o.resilience_redundancy <= 0.25) s += 40; else if (o.resilience_redundancy <= 0.50) s += 22; else if (o.resilience_redundancy <= 0.70) s += 8;
  if      (o.regeneration_capacity <= 0.25) s += 35; else if (o.regeneration_capacity <= 0.50) s += 18; else if (o.regeneration_capacity <= 0.70) s += 6;
  if      (o.biodiversity_analog_score <= 0.25) s += 25; else if (o.biodiversity_analog_score <= 0.50) s += 12;
  return Math.min(s, 100);
}
function synergyScore(o: Organism): number {
  let s = 0;
  if      (o.symbiotic_partnership_depth <= 0.25) s += 40; else if (o.symbiotic_partnership_depth <= 0.50) s += 22; else if (o.symbiotic_partnership_depth <= 0.70) s += 8;
  if      (o.swarm_coordination_score <= 0.25) s += 35; else if (o.swarm_coordination_score <= 0.50) s += 18; else if (o.swarm_coordination_score <= 0.70) s += 6;
  if      (o.information_propagation_speed <= 0.25) s += 25; else if (o.information_propagation_speed <= 0.50) s += 12;
  return Math.min(s, 100);
}
function composite(fit: number, ada: number, res: number, syn: number): number {
  return Math.min(Math.round((fit * 0.30 + ada * 0.25 + res * 0.25 + syn * 0.20) * 100) / 100, 100);
}
function evolutionaryPattern(o: Organism): string {
  if (o.extinction_vulnerability >= 0.65 && o.environmental_fit_score <= 0.35) return "extinction_spiral";
  if (o.niche_differentiation_score <= 0.30 && o.competitive_selection_pressure >= 0.60) return "niche_collapse";
  if (o.symbiotic_partnership_depth <= 0.30 && o.swarm_coordination_score <= 0.35) return "symbiosis_breakdown";
  if (o.adaptive_mutation_rate <= 0.30 && o.phenotypic_plasticity <= 0.35) return "evolutionary_stagnation";
  if (o.territorial_defense_strength <= 0.30 && o.ecological_dominance_index <= 0.35) return "territorial_loss";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "extinct_risk"; if (c >= 40) return "endangered"; if (c >= 20) return "adapting"; return "thriving"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "extinction_spiral") return "evolutionary_pivot";
    return "niche_reconstruction";
  }
  if (r === "high") {
    if (p === "symbiosis_breakdown") return "symbiosis_forge";
    return "adaptation_acceleration";
  }
  if (r === "moderate") return "evolution_monitoring";
  return "no_action";
}
function signal(o: Organism, pat: string, comp: number): string {
  if (comp < 20) return "Organisme en plein essor évolutif — fitness environnementale élevée, mutation adaptative active, résilience forte, synergies symbiotiques robustes";
  const labels: Record<string,string> = {
    extinction_spiral:       "Spirale d'extinction",
    niche_collapse:          "Effondrement de niche",
    symbiosis_breakdown:     "Rupture symbiotique",
    evolutionary_stagnation: "Stagnation évolutive",
    territorial_loss:        "Perte territoriale",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — fitness environnementale ${Math.round(o.environmental_fit_score*100)}% — vulnérabilité extinction ${Math.round(o.extinction_vulnerability*100)}% — taux mutation adaptative ${Math.round(o.adaptive_mutation_rate*100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const organisms = MOCK_ORGANISMS.map(o => {
      const fit = fitnessScore(o), ada = adaptationScore(o), res = resilienceScore(o), syn = synergyScore(o);
      const comp = composite(fit, ada, res, syn), pat = evolutionaryPattern(o), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        organism_id: o.organism_id, region: o.region,
        biomimetic_risk: r, evolutionary_pattern: pat, biomimetic_severity: sev, recommended_action: act,
        fitness_score: fit, adaptation_score: ada, resilience_score: res, synergy_score: syn,
        biomimetic_composite: comp,
        has_extinction_signal: comp >= 40 || o.extinction_vulnerability >= 0.60 || o.environmental_fit_score <= 0.30 || o.niche_differentiation_score <= 0.25,
        requires_evolutionary_intervention: comp >= 25 || o.extinction_vulnerability >= 0.45 || o.adaptive_mutation_rate <= 0.30,
        estimated_extinction_risk_index: Math.min(Math.round(comp/100*(1-o.resilience_redundancy+0.01)*10*100)/100, 10.0),
        biomimetic_signal: signal(o, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tfit=0,tada=0,tres=0,tsyn=0,tcomp=0,trisk=0,extC=0,intervC=0;
    for (const org of organisms) {
      rc[org.biomimetic_risk]      = (rc[org.biomimetic_risk]      ||0)+1;
      pc[org.evolutionary_pattern] = (pc[org.evolutionary_pattern] ||0)+1;
      sc[org.biomimetic_severity]  = (sc[org.biomimetic_severity]  ||0)+1;
      ac[org.recommended_action]   = (ac[org.recommended_action]   ||0)+1;
      tfit+=org.fitness_score; tada+=org.adaptation_score; tres+=org.resilience_score; tsyn+=org.synergy_score;
      tcomp+=org.biomimetic_composite; trisk+=org.estimated_extinction_risk_index;
      if (org.has_extinction_signal)              extC++;
      if (org.requires_evolutionary_intervention) intervC++;
    }
    const n = organisms.length;
    return NextResponse.json(sealResponse({ organisms, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_biomimetic_composite: Math.round(tcomp/n*10)/10,
      extinction_signal_count: extC, evolutionary_intervention_count: intervC,
      avg_fitness_score: Math.round(tfit/n*10)/10,
      avg_adaptation_score: Math.round(tada/n*10)/10,
      avg_resilience_score: Math.round(tres/n*10)/10,
      avg_synergy_score: Math.round(tsyn/n*10)/10,
      avg_estimated_extinction_risk_index: Math.round(trisk/n*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/biomimetic-strategy-engine`)).json());
}
