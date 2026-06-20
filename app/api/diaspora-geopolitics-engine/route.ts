import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[diaspora-geopolitics-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Diaspora Geopolitics Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/diaspora-geopolitics-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Diaspora Geopolitics Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Diaspora Geopolitics Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "DG-001", name: "Diaspora Chinoise — Opérations Pékin", country: "Global", sector: "Overseas Police Stations & Influence CPC à l'Étranger", composite_score: 86.25, state_coercion_score: 92.0, transnational_repression_score: 88.0, political_influence_score: 85.0, diaspora_radicalization_score: 80.0, risk_level: "critique", primary_pattern: "instrumentalisation_etatique", key_signals: ["Instrumentalisation étatique totale de la diaspora Chinoise — coercition et surveillance des citoyens à l'étranger", "Répression transnationale active — intimidation, menaces sur familles restées au pays et agents du régime", "Opérations d'influence dans les pays d'accueil — manipulation des communautés diasporiques à des fins géopolitiques"], estimated_diaspora_risk_index: 8.63, last_updated: "2026-06-20" },
    { entity_id: "DG-002", name: "Diaspora Russe — Post-2022 Sous Pression", country: "Europe/Global", sector: "FSB Ciblant Opposants Russes à l'Étranger", composite_score: 82.25, state_coercion_score: 85.0, transnational_repression_score: 90.0, political_influence_score: 72.0, diaspora_radicalization_score: 78.0, risk_level: "critique", primary_pattern: "repression_transnationale", key_signals: ["Instrumentalisation étatique totale de la diaspora Russe — coercition et surveillance des citoyens à l'étranger", "Répression transnationale active — intimidation, menaces sur familles restées au pays et agents du régime", "Opérations d'influence dans les pays d'accueil — manipulation des communautés diasporiques à des fins géopolitiques"], estimated_diaspora_risk_index: 8.23, last_updated: "2026-06-20" },
    { entity_id: "DG-003", name: "Diaspora Iranienne — Dualité Régime/Résistance", country: "Global", sector: "Mollahs vs Diaspora Pro-Démocratie — Guerre Froide Transnationale", composite_score: 79.25, state_coercion_score: 80.0, transnational_repression_score: 85.0, political_influence_score: 78.0, diaspora_radicalization_score: 72.0, risk_level: "critique", primary_pattern: "repression_transnationale", key_signals: ["Instrumentalisation étatique totale de la diaspora Iranienne — coercition et surveillance des citoyens à l'étranger", "Répression transnationale active — intimidation, menaces sur familles restées au pays et agents du régime", "Opérations d'influence dans les pays d'accueil — manipulation des communautés diasporiques à des fins géopolitiques"], estimated_diaspora_risk_index: 7.93, last_updated: "2026-06-20" },
    { entity_id: "DG-004", name: "Diaspora Turque — AKP & Mosquées Politiques", country: "Europe", sector: "DITIB comme Bras Politique d'Ankara dans les Diasporas", composite_score: 71.25, state_coercion_score: 72.0, transnational_repression_score: 68.0, political_influence_score: 80.0, diaspora_radicalization_score: 65.0, risk_level: "critique", primary_pattern: "influence_geopolitique_active", key_signals: ["Instrumentalisation étatique totale de la diaspora Turque — coercition et surveillance des citoyens à l'étranger", "Répression transnationale active — intimidation, menaces sur familles restées au pays et agents du régime", "Opérations d'influence dans les pays d'accueil — manipulation des communautés diasporiques à des fins géopolitiques"], estimated_diaspora_risk_index: 7.13, last_updated: "2026-06-20" },
    { entity_id: "DG-005", name: "Diaspora Saoudienne & Golf — Influence Islamiste", country: "Global", sector: "Financement Wahhabite des Communautés Musulmanes Diasporiques", composite_score: 58.35, state_coercion_score: 58.0, transnational_repression_score: 52.0, political_influence_score: 72.0, diaspora_radicalization_score: 60.0, risk_level: "élevé", primary_pattern: "influence_geopolitique_active", key_signals: ["Influence géopolitique active de la diaspora Saoudienne — financement partis et lobbying dans pays d'accueil", "Tensions entre communautés diasporiques et gouvernements d'accueil — suspicion d'ingérence étrangère", "Surveillance diasporique par le pays d'origine — réseaux de renseignement dans les communautés expatriées"], estimated_diaspora_risk_index: 5.84, last_updated: "2026-06-20" },
    { entity_id: "DG-006", name: "Diaspora Indienne — Lobby NRI & Modi", country: "Global", sector: "NRI Influence sur la Politique Étrangère Américaine et UK", composite_score: 47.75, state_coercion_score: 45.0, transnational_repression_score: 35.0, political_influence_score: 68.0, diaspora_radicalization_score: 42.0, risk_level: "élevé", primary_pattern: "influence_geopolitique_active", key_signals: ["Influence géopolitique active de la diaspora Indienne — financement partis et lobbying dans pays d'accueil", "Tensions entre communautés diasporiques et gouvernements d'accueil — suspicion d'ingérence étrangère", "Surveillance diasporique par le pays d'origine — réseaux de renseignement dans les communautés expatriées"], estimated_diaspora_risk_index: 4.78, last_updated: "2026-06-20" },
    { entity_id: "DG-007", name: "Diaspora Africaine — Remittances & Influence", country: "Global", sector: "Transferts Supérieurs à l'Aide Internationale — Soft Power", composite_score: 25.75, state_coercion_score: 25.0, transnational_repression_score: 18.0, political_influence_score: 38.0, diaspora_radicalization_score: 22.0, risk_level: "modéré", primary_pattern: "tensions_identitaires", key_signals: ["Tensions identitaires diasporiques pour Diaspora Africaine — communautés tiraillées entre fidélité et intégration", "Influence politique partielle — organisations diasporiques actives dans les débats du pays d'accueil", "Risques de radicalisation à surveiller — communautés isolées et en contact avec des réseaux extrémistes"], estimated_diaspora_risk_index: 2.58, last_updated: "2026-06-20" },
    { entity_id: "DG-008", name: "Diaspora Scandinave & Canadienne — Intégration", country: "Global", sector: "Modèles d'Intégration Diasporique Exemplaires", composite_score: 6.5, state_coercion_score: 5.0, transnational_repression_score: 4.0, political_influence_score: 12.0, diaspora_radicalization_score: 6.0, risk_level: "faible", primary_pattern: "diaspora_integree", key_signals: ["Diaspora Scandinave & Canadienne intégrée et non-instrumentalisée — pont culturel et économique positif", "Transferts financiers au pays d'origine favorisant le développement sans ingérence politique", "Modèle d'intégration diasporique à valoriser — contribution positive aux deux pays"], estimated_diaspora_risk_index: 0.65, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { instrumentalisation_etatique: 1, repression_transnationale: 2, influence_geopolitique_active: 3, tensions_identitaires: 1, diaspora_integree: 1 },
    top_risk_entities: ["Diaspora Chinoise — Opérations Pékin", "Diaspora Russe — Post-2022 Sous Pression", "Diaspora Iranienne — Dualité Régime/Résistance"],
    critical_alerts: ["Diaspora Chinoise: instrumentalisation étatique", "Diaspora Russe: répression transnationale", "Diaspora Iranienne: répression transnationale", "Diaspora Turque: influence géopolitique active"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "diaspora_geo",
    confidence_score: 0.77,
    data_sources: ["freedom_house_transnational_repression", "globsec_diaspora_monitor", "ifri_diaspora_geopolitics"],
    entities,
    avg_estimated_diaspora_risk_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
