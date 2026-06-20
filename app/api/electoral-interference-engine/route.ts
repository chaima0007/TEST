import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[electoral-interference-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Electoral Interference Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/electoral-interference-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Electoral Interference Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Electoral Interference Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "EI-001", name: "Russie — Ingérence Électorale Systémique", country: "Europe de l'Est", sector: "GRU/FSB: Hack-and-Leak, Désinformation & Soutien Partis Eurosceptiques", composite_score: 86.95, cyberattack_score: 92.0, disinformation_campaign_score: 90.0, illicit_foreign_funding_score: 85.0, electoral_infrastructure_vulnerability_score: 78.0, risk_level: "critique", primary_pattern: "ingérence_systémique_active", key_signals: ["Ingérence électorale systémique dans Russie — opérations étrangères compromettant la souveraineté démocratique", "Cyberattaques ciblant l'infrastructure électorale — registres, systèmes de vote et centres de dépouillement", "Désinformation électorale massive — campagnes coordonnées visant à polariser et déstabiliser l'électorat"], estimated_interference_index: 8.7, last_updated: "2026-06-20" },
    { entity_id: "EI-002", name: "Chine — Influence Long Terme & Financement", country: "Asie", sector: "Financements Universités/Médias & Ingérence Taïwan, Australie, Canada", composite_score: 78.5, cyberattack_score: 75.0, disinformation_campaign_score: 80.0, illicit_foreign_funding_score: 88.0, electoral_infrastructure_vulnerability_score: 70.0, risk_level: "critique", primary_pattern: "financement_illicite_étranger", key_signals: ["Ingérence électorale systémique dans Chine — opérations étrangères compromettant la souveraineté démocratique", "Cyberattaques ciblant l'infrastructure électorale — registres, systèmes de vote et centres de dépouillement", "Désinformation électorale massive — campagnes coordonnées visant à polariser et déstabiliser l'électorat"], estimated_interference_index: 7.85, last_updated: "2026-06-20" },
    { entity_id: "EI-003", name: "Iran — Opérations Psychologiques Ciblées", country: "MENA", sector: "Ciblage Diaspora Iranienne & Fausses Identités sur Réseaux Sociaux", composite_score: 75.9, cyberattack_score: 80.0, disinformation_campaign_score: 85.0, illicit_foreign_funding_score: 65.0, electoral_infrastructure_vulnerability_score: 72.0, risk_level: "critique", primary_pattern: "ingérence_systémique_active", key_signals: ["Ingérence électorale systémique dans Iran — opérations étrangères compromettant la souveraineté démocratique", "Cyberattaques ciblant l'infrastructure électorale — registres, systèmes de vote et centres de dépouillement", "Désinformation électorale massive — campagnes coordonnées visant à polariser et déstabiliser l'électorat"], estimated_interference_index: 7.59, last_updated: "2026-06-20" },
    { entity_id: "EI-004", name: "Arabie Saoudite & EAU — Lobbying Opaque", country: "MENA", sector: "Financement Partis Occidentaux via Façades & Opérations d'Influence", composite_score: 64.4, cyberattack_score: 58.0, disinformation_campaign_score: 62.0, illicit_foreign_funding_score: 82.0, electoral_infrastructure_vulnerability_score: 55.0, risk_level: "critique", primary_pattern: "financement_illicite_étranger", key_signals: ["Ingérence électorale systémique dans Arabie Saoudite & EAU — opérations étrangères compromettant la souveraineté démocratique", "Cyberattaques ciblant l'infrastructure électorale — registres, systèmes de vote et centres de dépouillement", "Désinformation électorale massive — campagnes coordonnées visant à polariser et déstabiliser l'électorat"], estimated_interference_index: 6.44, last_updated: "2026-06-20" },
    { entity_id: "EI-005", name: "USA — Cible & Acteur d'Ingérence", country: "Amérique du Nord", sector: "Élections 2016-2020 Ciblées + Interventions CIA Historiques à l'Étranger", composite_score: 52.2, cyberattack_score: 52.0, disinformation_campaign_score: 55.0, illicit_foreign_funding_score: 45.0, electoral_infrastructure_vulnerability_score: 58.0, risk_level: "élevé", primary_pattern: "manipulation_infrastructure", key_signals: ["Opérations d'ingérence significatives dans USA — financement illicite et manipulation de l'opinion", "Flux financiers étrangers vers des acteurs politiques — opacité des donations et façades associatives", "Infrastructure électorale partiellement vulnérable — systèmes de vote électronique sans audit suffisant"], estimated_interference_index: 5.22, last_updated: "2026-06-20" },
    { entity_id: "EI-006", name: "Turquie — Diaspora comme Arme Électorale", country: "Europe/MENA", sector: "AKP Mobilisant Diaspora Turque en Europe pour Référendums & Élections", composite_score: 46.35, cyberattack_score: 42.0, disinformation_campaign_score: 48.0, illicit_foreign_funding_score: 55.0, electoral_infrastructure_vulnerability_score: 40.0, risk_level: "élevé", primary_pattern: "manipulation_infrastructure", key_signals: ["Opérations d'ingérence significatives dans Turquie — financement illicite et manipulation de l'opinion", "Flux financiers étrangers vers des acteurs politiques — opacité des donations et façades associatives", "Infrastructure électorale partiellement vulnérable — systèmes de vote électronique sans audit suffisant"], estimated_interference_index: 4.64, last_updated: "2026-06-20" },
    { entity_id: "EI-007", name: "Hongrie & Pologne — Ingérence Interne", country: "Europe de l'Est", sector: "Manipulation Registres Électoraux & Médias Publics comme Outils Partisans", composite_score: 39.8, cyberattack_score: 38.0, disinformation_campaign_score: 45.0, illicit_foreign_funding_score: 35.0, electoral_infrastructure_vulnerability_score: 42.0, risk_level: "modéré", primary_pattern: "influence_diasporique", key_signals: ["Risques d'ingérence électorale dans Hongrie & Pologne — vulnérabilités identifiées mais pas encore exploitées", "Tentatives de manipulation des communautés diasporiques lors des consultations électorales", "Renforcement nécessaire de la cybersécurité des systèmes de vote et des registres électoraux"], estimated_interference_index: 3.98, last_updated: "2026-06-20" },
    { entity_id: "EI-008", name: "Pays-Bas & Canada — Résilience Électorale", country: "Global Nord", sector: "Systèmes Papier, Audits Indépendants & Cybersécurité Électorale Robuste", composite_score: 7.4, cyberattack_score: 8.0, disinformation_campaign_score: 10.0, illicit_foreign_funding_score: 6.0, electoral_infrastructure_vulnerability_score: 5.0, risk_level: "faible", primary_pattern: "resilience_electorale", key_signals: ["Pays-Bas & Canada maintient des systèmes électoraux robustes — résilience avérée face aux tentatives d'ingérence", "Observateurs indépendants, audit des finances politiques et cybersécurité électorale effectifs", "Modèle de souveraineté électorale à diffuser — transparence, vérifiabilité et protection des données"], estimated_interference_index: 0.74, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { "ingérence_systémique_active": 2, "financement_illicite_étranger": 2, manipulation_infrastructure: 2, influence_diasporique: 1, resilience_electorale: 1 },
    top_risk_entities: ["Russie — Ingérence Électorale Systémique", "Chine — Influence Long Terme & Financement", "Iran — Opérations Psychologiques Ciblées"],
    critical_alerts: ["Russie: ingérence systémique active", "Chine: financement illicite étranger", "Iran: ingérence systémique active", "Arabie Saoudite & EAU: financement illicite étranger"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "electoral_interference",
    confidence_score: 0.83,
    data_sources: ["atlantic_council_election_forensics", "eu_disinfo_lab", "freedom_house_electoral_integrity"],
    entities,
    avg_estimated_interference_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
