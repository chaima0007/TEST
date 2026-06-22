import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[power-vacuum-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Power Vacuum Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/power-vacuum-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Power Vacuum Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Power Vacuum Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "PV-001", name: "Corée du Nord — Succession Kim", country: "Asie du Nord-Est", sector: "Succession Dynastique & Arsenal Nucléaire", composite_score: 91.35, succession_crisis_score: 95.0, institutional_vacuum_score: 92.0, proxy_war_attraction_score: 90.0, regional_destabilization_score: 88.0, risk_level: "critique", primary_pattern: "vide_catastrophique", key_signals: ["Vide de pouvoir catastrophique dans Corée du Nord — compétition chaotique entre factions armées", "Guerre par procuration imminente — puissances régionales et mondiales mobilisant leurs alliés", "Effondrement institutionnel total — aucun mécanisme de succession légitime opérationnel"], estimated_vacuum_index: 9.14, last_updated: "2026-06-20" },
    { id: "PV-002", name: "Syrie — Post-Conflit & Fragmentation", country: "MENA", sector: "Vide Hégémonique & Zones de Contrôle Multiples", composite_score: 86.75, succession_crisis_score: 88.0, institutional_vacuum_score: 85.0, proxy_war_attraction_score: 92.0, regional_destabilization_score: 82.0, risk_level: "critique", primary_pattern: "guerre_succession", key_signals: ["Vide de pouvoir catastrophique dans Syrie — compétition chaotique entre factions armées", "Guerre par procuration imminente — puissances régionales et mondiales mobilisant leurs alliés", "Effondrement institutionnel total — aucun mécanisme de succession légitime opérationnel"], estimated_vacuum_index: 8.68, last_updated: "2026-06-20" },
    { id: "PV-003", name: "Sahel — Effritement Souveraineté Étatique", country: "Afrique", sector: "Coups d'État en Cascade & Retrait Français", composite_score: 83.5, succession_crisis_score: 82.0, institutional_vacuum_score: 88.0, proxy_war_attraction_score: 85.0, regional_destabilization_score: 80.0, risk_level: "critique", primary_pattern: "vide_catastrophique", key_signals: ["Vide de pouvoir catastrophique dans Sahel — compétition chaotique entre factions armées", "Guerre par procuration imminente — puissances régionales et mondiales mobilisant leurs alliés", "Effondrement institutionnel total — aucun mécanisme de succession légitime opérationnel"], estimated_vacuum_index: 8.35, last_updated: "2026-06-20" },
    { id: "PV-004", name: "Libye — Dualisme Étatique Permanent", country: "Afrique du Nord", sector: "Deux Gouvernements & Proxies Étrangers Multiples", composite_score: 82.0, succession_crisis_score: 80.0, institutional_vacuum_score: 85.0, proxy_war_attraction_score: 88.0, regional_destabilization_score: 75.0, risk_level: "critique", primary_pattern: "guerre_succession", key_signals: ["Vide de pouvoir catastrophique dans Libye — compétition chaotique entre factions armées", "Guerre par procuration imminente — puissances régionales et mondiales mobilisant leurs alliés", "Effondrement institutionnel total — aucun mécanisme de succession légitime opérationnel"], estimated_vacuum_index: 8.2, last_updated: "2026-06-20" },
    { id: "PV-005", name: "Venezuela — Pouvoir Contesté", country: "Amériques", sector: "Légitimité Duale & Compétition USA/Russie/Chine", composite_score: 66.5, succession_crisis_score: 68.0, institutional_vacuum_score: 65.0, proxy_war_attraction_score: 72.0, regional_destabilization_score: 60.0, risk_level: "élevé", primary_pattern: "competition_hegemonique", key_signals: ["Instabilité de succession sévère dans Venezuela — factions rivales sans arbitre institutionnel", "Attraction pour les guerres par procuration — acteurs extérieurs mobilisant des proxies internes", "Déstabilisation régionale en cours — le vide débordant au-delà des frontières nationales"], estimated_vacuum_index: 6.65, last_updated: "2026-06-20" },
    { id: "PV-006", name: "Irak — Souveraineté Fragmentée", country: "MENA", sector: "État Faible entre Iran, USA & Milices Armées", composite_score: 63.75, succession_crisis_score: 62.0, institutional_vacuum_score: 68.0, proxy_war_attraction_score: 65.0, regional_destabilization_score: 58.0, risk_level: "élevé", primary_pattern: "competition_hegemonique", key_signals: ["Instabilité de succession sévère dans Irak — factions rivales sans arbitre institutionnel", "Attraction pour les guerres par procuration — acteurs extérieurs mobilisant des proxies internes", "Déstabilisation régionale en cours — le vide débordant au-delà des frontières nationales"], estimated_vacuum_index: 6.38, last_updated: "2026-06-20" },
    { id: "PV-007", name: "Bolivie & Nicaragua — Démocratie Érodée", country: "Amériques", sector: "Dérive Autoritaire & Institutions Fragilisées", composite_score: 35.1, succession_crisis_score: 38.0, institutional_vacuum_score: 35.0, proxy_war_attraction_score: 30.0, regional_destabilization_score: 32.0, risk_level: "modéré", primary_pattern: "transition_fragile", key_signals: ["Transition de pouvoir fragile dans Bolivie & Nicaragua — succession incertaine mais conflit armé évité", "Institutions partiellement fonctionnelles — cadre de succession existant mais sous pression", "Risque de compétition hégémonique externe si la transition s'enlise"], estimated_vacuum_index: 3.51, last_updated: "2026-06-20" },
    { id: "PV-008", name: "Suède & Canada — Démocraties Résilientes", country: "Europe/Amériques", sector: "Succession Institutionnelle Exemplaire", composite_score: 4.35, succession_crisis_score: 5.0, institutional_vacuum_score: 4.0, proxy_war_attraction_score: 3.0, regional_destabilization_score: 6.0, risk_level: "faible", primary_pattern: "succession_institutionnalisee", key_signals: ["Suède & Canada maintient une succession institutionnalisée — transfert de pouvoir pacifique garanti", "Institutions démocratiques solides absorbant les transitions politiques sans violence", "Modèle de gouvernance à fort capital institutionnel — résistant aux crises de succession"], estimated_vacuum_index: 0.44, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { vide_catastrophique: 2, guerre_succession: 2, competition_hegemonique: 2, transition_fragile: 1, succession_institutionnalisee: 1 },
    top_risk_entities: ["Corée du Nord — Succession Kim", "Syrie — Post-Conflit & Fragmentation", "Sahel — Effritement Souveraineté Étatique"],
    critical_alerts: ["Corée du Nord: vide catastrophique", "Sahel: vide catastrophique", "Syrie: guerre de succession", "Libye: guerre de succession"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "power_vacuum",
    confidence_score: 0.79,
    data_sources: ["fragile_states_index", "succession_crisis_tracker", "proxy_conflict_monitor"],
    entities,
    avg_estimated_vacuum_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
