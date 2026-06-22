import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[diaspora-weaponization-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Diaspora Weaponization Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/diaspora-weaponization-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Diaspora Weaponization Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Diaspora Weaponization Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "DW-001", name: "Chine — Postes Police Étrangère & OCI Mondial", country: "Asie", sector: "53 Postes Police Illicites dans 53 Pays & Surveillance Chinois d'Outre-Mer", composite_score: 88.85, diaspora_political_mobilization_score: 90.0, transnational_surveillance_score: 92.0, remittance_leverage_score: 85.0, diaspora_espionage_recruitment_score: 88.0, risk_level: "critique", primary_pattern: "surveillance_diaspora_totale", key_signals: ["Répression transnationale systémique par Chine — surveillance, harcèlement et coercition des diasporas à l'étranger", "Postes de police étrangers illicites — agents consulaires ou associatifs utilisés pour surveiller et intimider les dissidents expatriés", "Weaponisation des familles restées au pays — menaces sur les proches utilisées pour forcer les membres de diaspora à se soumettre"], estimated_diaspora_weapon_index: 8.89, last_updated: "2026-06-20" },
    { id: "DW-002", name: "Iran — IRGC & Harcèlement Irano-Américains", country: "MENA", sector: "Réseaux IRGC Traquant Dissidents Irano-Américains & Plans Assassinats", composite_score: 82.35, diaspora_political_mobilization_score: 82.0, transnational_surveillance_score: 88.0, remittance_leverage_score: 75.0, diaspora_espionage_recruitment_score: 85.0, risk_level: "critique", primary_pattern: "surveillance_diaspora_totale", key_signals: ["Répression transnationale systémique par Iran — surveillance, harcèlement et coercition des diasporas à l'étranger", "Postes de police étrangers illicites — agents consulaires ou associatifs utilisés pour surveiller et intimider les dissidents expatriés", "Weaponisation des familles restées au pays — menaces sur les proches utilisées pour forcer les membres de diaspora à se soumettre"], estimated_diaspora_weapon_index: 8.24, last_updated: "2026-06-20" },
    { id: "DW-003", name: "Russie — Compatriotes & Manipulation Russophones", country: "Europe de l'Est", sector: "Fonds Poutine 'Compatriotes' & Diaspora Russe comme Levier Géopolitique", composite_score: 81.5, diaspora_political_mobilization_score: 85.0, transnational_surveillance_score: 82.0, remittance_leverage_score: 78.0, diaspora_espionage_recruitment_score: 80.0, risk_level: "critique", primary_pattern: "surveillance_diaspora_totale", key_signals: ["Répression transnationale systémique par Russie — surveillance, harcèlement et coercition des diasporas à l'étranger", "Postes de police étrangers illicites — agents consulaires ou associatifs utilisés pour surveiller et intimider les dissidents expatriés", "Weaponisation des familles restées au pays — menaces sur les proches utilisées pour forcer les membres de diaspora à se soumettre"], estimated_diaspora_weapon_index: 8.15, last_updated: "2026-06-20" },
    { id: "DW-004", name: "Turquie — Diaspora Belge/Allemande Erdoğan", country: "MENA/Europe", sector: "DITIB Mobilisant Turco-Européens pour Référendums & Signalement Opposants", composite_score: 77.5, diaspora_political_mobilization_score: 80.0, transnational_surveillance_score: 72.0, remittance_leverage_score: 82.0, diaspora_espionage_recruitment_score: 75.0, risk_level: "critique", primary_pattern: "instrumentalisation_remittances", key_signals: ["Répression transnationale systémique par Turquie — surveillance, harcèlement et coercition des diasporas à l'étranger", "Postes de police étrangers illicites — agents consulaires ou associatifs utilisés pour surveiller et intimider les dissidents expatriés", "Weaponisation des familles restées au pays — menaces sur les proches utilisées pour forcer les membres de diaspora à se soumettre"], estimated_diaspora_weapon_index: 7.75, last_updated: "2026-06-20" },
    { id: "DW-005", name: "Maroc — CCME & Instrumentalisation MRE", country: "MENA/Europe", sector: "CCME Outil Soft Power & Comunautés Marocaines Europe sous Influence Rabat", composite_score: 55.75, diaspora_political_mobilization_score: 58.0, transnational_surveillance_score: 55.0, remittance_leverage_score: 60.0, diaspora_espionage_recruitment_score: 48.0, risk_level: "élevé", primary_pattern: "levier_diaspora_politique", key_signals: ["Pression politique diasporique significative par Maroc — mobilisation et surveillance des communautés immigrées", "Ingérence électorale via diaspora — vote diasporique influencé par pressions consulaires et mobilisation identitaire", "Transferts d'argent conditionnés — pression informelle sur les remittances pour discipliner les membres non-conformes"], estimated_diaspora_weapon_index: 5.58, last_updated: "2026-06-20" },
    { id: "DW-006", name: "Inde — Diaspora BJP & Hindutva Exporté", country: "Asie du Sud", sector: "Modi Diaspora Events & Hindutva Exporté aux USA/UK via Communautés Indiennes", composite_score: 49.85, diaspora_political_mobilization_score: 52.0, transnational_surveillance_score: 45.0, remittance_leverage_score: 48.0, diaspora_espionage_recruitment_score: 55.0, risk_level: "élevé", primary_pattern: "levier_diaspora_politique", key_signals: ["Pression politique diasporique significative par Inde — mobilisation et surveillance des communautés immigrées", "Ingérence électorale via diaspora — vote diasporique influencé par pressions consulaires et mobilisation identitaire", "Transferts d'argent conditionnés — pression informelle sur les remittances pour discipliner les membres non-conformes"], estimated_diaspora_weapon_index: 4.99, last_updated: "2026-06-20" },
    { id: "DW-007", name: "Éthiopie — Diaspora Mobilisée Guerre Tigré", country: "Afrique de l'Est", sector: "Diaspora Éthiopienne Divisée & Financement Conflit Tigré depuis Diasporas", composite_score: 30.35, diaspora_political_mobilization_score: 32.0, transnational_surveillance_score: 28.0, remittance_leverage_score: 35.0, diaspora_espionage_recruitment_score: 25.0, risk_level: "modéré", primary_pattern: "diaspora_conflict_export", key_signals: ["Instrumentalisation partielle de la diaspora de Éthiopie — tensions politiques exportées sans harcèlement systématique", "Conflits d'identité communautaires — factions politiques du pays d'origine reproduites dans les associations diasporiques", "Surveillance informelle — réseaux de signalement communautaires sans organisation étatique formelle"], estimated_diaspora_weapon_index: 3.04, last_updated: "2026-06-20" },
    { id: "DW-008", name: "Canada & Allemagne — Protections Anti-Répression", country: "Global", sector: "FARA Canadien & BfV Allemand Démantèlent Réseaux de Surveillance Étrangers", composite_score: 4.65, diaspora_political_mobilization_score: 6.0, transnational_surveillance_score: 4.0, remittance_leverage_score: 5.0, diaspora_espionage_recruitment_score: 3.0, risk_level: "faible", primary_pattern: "protection_diaspora_droits", key_signals: ["Canada & Allemagne protège les membres de diaspora contre les ingérences étrangères — cadre légal anti-répression transnationale", "Législation FARA/anti-ingérence étrangère appliquée — postes de police illicites identifiés et démantelés", "Modèle de protection des droits diasporiques — espace sûr pour les communautés immigrées sans coercition d'origine"], estimated_diaspora_weapon_index: 0.47, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { surveillance_diaspora_totale: 3, instrumentalisation_remittances: 1, levier_diaspora_politique: 2, diaspora_conflict_export: 1, protection_diaspora_droits: 1 },
    top_risk_entities: ["Chine — Postes Police Étrangère & OCI Mondial", "Iran — IRGC & Harcèlement Irano-Américains", "Russie — Compatriotes & Manipulation Russophones"],
    critical_alerts: ["Chine: surveillance diaspora totale", "Iran: surveillance diaspora totale", "Russie: surveillance diaspora totale", "Turquie: instrumentalisation remittances"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "diaspora_weapon",
    confidence_score: 0.80,
    data_sources: ["freedom_house_transnational_repression", "safeguard_defenders_police_stations", "ndi_diaspora_political_influence"],
    entities,
    avg_estimated_diaspora_weapon_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
