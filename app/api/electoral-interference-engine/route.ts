import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[electoral-interference-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Electoral Interference Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/electoral-interference-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Electoral Interference Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Electoral Interference Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "EI-001", name: "Russie — GRU/IRA & Active Measures Mondiales", country: "Europe de l'Est", sector: "IRA Trolls, Fancy Bear USA 2016, MacronLeaks & RT/Sputnik 65+ Élections Ciblées", composite_score: 87.6, foreign_influence_operation_score: 92.0, disinformation_campaign_score: 90.0, campaign_finance_infiltration_score: 82.0, electoral_infrastructure_attack_score: 85.0, risk_level: "critique", primary_pattern: "ingérence_systémique", key_signals: ["Ingérence électorale systémique de Russie — opérations coordonnées ciblant les processus démocratiques de multiples États", "Active Measures 2.0 — fermes à trolls, fuites de données et amplification algorithmique comme armes électorales industrielles", "Corruption de la souveraineté populaire — manipulation de l'opinion publique étrangère via la désinformation ciblée à grande échelle"], estimated_electoral_interference_index: 8.76, last_updated: "2026-06-20" },
    { id: "EI-002", name: "Chine — APT41 & Financement Partis Occulte", country: "Asie", sector: "Sociétés Écrans Dons Partis, APT10 Réseaux Politiques & TikTok Ingérence Diaspora", composite_score: 83.0, foreign_influence_operation_score: 85.0, disinformation_campaign_score: 82.0, campaign_finance_infiltration_score: 88.0, electoral_infrastructure_attack_score: 75.0, risk_level: "critique", primary_pattern: "financement_occulte_campagnes", key_signals: ["Ingérence électorale systémique de Chine — opérations coordonnées ciblant les processus démocratiques de multiples États", "Active Measures 2.0 — fermes à trolls, fuites de données et amplification algorithmique comme armes électorales industrielles", "Corruption de la souveraineté populaire — manipulation de l'opinion publique étrangère via la désinformation ciblée à grande échelle"], estimated_electoral_interference_index: 8.3, last_updated: "2026-06-20" },
    { id: "EI-003", name: "Iran — IRGC & Cyberciblage Électeurs Musulmans", country: "MENA", sector: "Campagnes Email Électeurs Musulmans USA, Hack-and-Leak & Cyberharcèlement Opposants", composite_score: 78.5, foreign_influence_operation_score: 80.0, disinformation_campaign_score: 78.0, campaign_finance_infiltration_score: 72.0, electoral_infrastructure_attack_score: 85.0, risk_level: "critique", primary_pattern: "sabotage_infrastructure_electorale", key_signals: ["Ingérence électorale systémique de Iran — opérations coordonnées ciblant les processus démocratiques de multiples États", "Active Measures 2.0 — fermes à trolls, fuites de données et amplification algorithmique comme armes électorales industrielles", "Corruption de la souveraineté populaire — manipulation de l'opinion publique étrangère via la désinformation ciblée à grande échelle"], estimated_electoral_interference_index: 7.85, last_updated: "2026-06-20" },
    { id: "EI-004", name: "EAU & Israël — NSO Pegasus & Surveillance Politique", country: "MENA", sector: "Pegasus 50+ Pays, Ciblage Journalistes/Politiques & Dark PR Campagnes Influence", composite_score: 76.1, foreign_influence_operation_score: 75.0, disinformation_campaign_score: 72.0, campaign_finance_infiltration_score: 88.0, electoral_infrastructure_attack_score: 68.0, risk_level: "critique", primary_pattern: "financement_occulte_campagnes", key_signals: ["Ingérence électorale systémique de EAU & Israël — opérations coordonnées ciblant les processus démocratiques de multiples États", "Active Measures 2.0 — fermes à trolls, fuites de données et amplification algorithmique comme armes électorales industrielles", "Corruption de la souveraineté populaire — manipulation de l'opinion publique étrangère via la désinformation ciblée à grande échelle"], estimated_electoral_interference_index: 7.61, last_updated: "2026-06-20" },
    { id: "EI-005", name: "Turquie — AKP & Ingérence Diaspora Européenne", country: "MENA/Europe", sector: "DITIB Mobilisation Électorale, Bots Turcs & Financement Partis Européens Pro-Erdoğan", composite_score: 53.6, foreign_influence_operation_score: 55.0, disinformation_campaign_score: 58.0, campaign_finance_infiltration_score: 52.0, electoral_infrastructure_attack_score: 48.0, risk_level: "élevé", primary_pattern: "manipulation_narrative_électorale", key_signals: ["Manipulation narrative électorale par Turquie — campagnes actives de désinformation sans attribution formelle établie", "Polarisation instrumentalisée — amplification des fractures sociales pour fragiliser la cohésion pré-électorale des sociétés cibles", "Écosystèmes informationnels corrompus — médias pro-régime, influenceurs rémunérés et campagnes coordonnées inautentiques"], estimated_electoral_interference_index: 5.36, last_updated: "2026-06-20" },
    { id: "EI-006", name: "Hongrie — Orbán & Réseau Anti-Démocrate Européen", country: "Europe", sector: "Financement Partis Européens Via Fondations, RT Relay & Propaganda Souverainiste", composite_score: 49.55, foreign_influence_operation_score: 48.0, disinformation_campaign_score: 52.0, campaign_finance_infiltration_score: 55.0, electoral_infrastructure_attack_score: 42.0, risk_level: "élevé", primary_pattern: "manipulation_narrative_électorale", key_signals: ["Manipulation narrative électorale par Hongrie — campagnes actives de désinformation sans attribution formelle établie", "Polarisation instrumentalisée — amplification des fractures sociales pour fragiliser la cohésion pré-électorale des sociétés cibles", "Écosystèmes informationnels corrompus — médias pro-régime, influenceurs rémunérés et campagnes coordonnées inautentiques"], estimated_electoral_interference_index: 4.96, last_updated: "2026-06-20" },
    { id: "EI-007", name: "UE — Fragmentation Réglementaire Anti-Ingérence", country: "Europe", sector: "Digital Services Act Insuffisant, Positions Nationales Divisées & Absence FARA Européen", composite_score: 26.65, foreign_influence_operation_score: 30.0, disinformation_campaign_score: 28.0, campaign_finance_infiltration_score: 25.0, electoral_infrastructure_attack_score: 22.0, risk_level: "modéré", primary_pattern: "manipulation_narrative_électorale", key_signals: ["Vulnérabilité électorale dans UE — exposition aux ingérences étrangères sans contre-mesures systémiques adéquates", "Réglementation insuffisante — lacunes dans la transparence des financements politiques et la sécurité des systèmes électoraux", "Risque d'influence étrangère — plateformes non régulées permettant des campagnes d'influence sans obligation de traçabilité"], estimated_electoral_interference_index: 2.67, last_updated: "2026-06-20" },
    { id: "EI-008", name: "Islande & Canada — Intégrité Électorale Modèle", country: "Global", sector: "CRTC Régulation, Loi Élections Canada & Islande Résilience Info Modèle Mondial", composite_score: 4.6, foreign_influence_operation_score: 5.0, disinformation_campaign_score: 4.0, campaign_finance_infiltration_score: 6.0, electoral_infrastructure_attack_score: 3.0, risk_level: "faible", primary_pattern: "intégrité_electorale", key_signals: ["Islande & Canada maintient une intégrité électorale exemplaire — systèmes robustes et résilience face aux ingérences étrangères", "Transparence des financements politiques — déclarations exhaustives et interdiction des dons étrangers appliquée", "Modèle d'intégrité à exporter — observateurs internationaux, vérification des faits et éducation civique institutionnalisés"], estimated_electoral_interference_index: 0.46, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { "ingérence_systémique": 1, financement_occulte_campagnes: 2, sabotage_infrastructure_electorale: 1, "manipulation_narrative_électorale": 3, "intégrité_electorale": 1 },
    top_risk_entities: ["Russie — GRU/IRA & Active Measures Mondiales", "Chine — APT41 & Financement Partis Occulte", "Iran — IRGC & Cyberciblage Électeurs Musulmans"],
    critical_alerts: ["Russie: ingérence systémique", "Chine: financement occulte campagnes", "Iran: sabotage infrastructure électorale", "EAU & Israël: financement occulte campagnes"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "electoral_interference",
    confidence_score: 0.85,
    data_sources: ["freedom_house_election_integrity", "atlantic_council_dfrlab_election_watch", "ndi_democracy_interference_monitor"],
    entities,
    avg_estimated_electoral_interference_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
