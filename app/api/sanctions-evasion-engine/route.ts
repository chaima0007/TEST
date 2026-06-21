import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sanctions-evasion-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Sanctions Evasion Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sanctions-evasion-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Sanctions Evasion Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Sanctions Evasion Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "SE-001", name: "Russie — Shadow Fleet 400+ Pétroliers & Contournement G7", country: "Europe de l'Est", sector: "Fleet Fantôme Pavillon Gabon/Palau, Pétrole via Inde/Chine & Plafond 60$/Baril Ignoré", composite_score: 86.85, shadow_fleet_oil_score: 92.0, crypto_sanctions_bypass_score: 85.0, shell_company_network_score: 88.0, correspondent_banking_evasion_score: 80.0, risk_level: "critique", primary_pattern: "evasion_sanctions_systematique", key_signals: ["Évasion de sanctions systématique par Russie — infrastructure organisée de contournement avec déni de responsabilité étatique", "Flotte fantôme et réseaux opaques — pétroliers sous pavillons de complaisance, sociétés écrans et corridors bancaires alternatifs", "Subversion de l'ordre économique international — les sanctions perdent leur effet dissuasif face à des écosystèmes d'évasion industriels"], estimated_sanctions_evasion_index: 8.69, last_updated: "2026-06-20" },
    { id: "SE-002", name: "Iran — NIOC & 40 Ans d'Évasion OFAC Industrielle", country: "MENA", sector: "Pétrole Fantôme via Malaisie/EAU, SWIFT alternatif & Or contre Marchandises Sanctionnées", composite_score: 84.05, shadow_fleet_oil_score: 88.0, crypto_sanctions_bypass_score: 80.0, shell_company_network_score: 85.0, correspondent_banking_evasion_score: 82.0, risk_level: "critique", primary_pattern: "evasion_sanctions_systematique", key_signals: ["Évasion de sanctions systématique par Iran — infrastructure organisée de contournement avec déni de responsabilité étatique", "Flotte fantôme et réseaux opaques — pétroliers sous pavillons de complaisance, sociétés écrans et corridors bancaires alternatifs", "Subversion de l'ordre économique international — les sanctions perdent leur effet dissuasif face à des écosystèmes d'évasion industriels"], estimated_sanctions_evasion_index: 8.41, last_updated: "2026-06-20" },
    { id: "SE-003", name: "Corée du Nord — Lazarus & 3Md$ Cryptos Volés", country: "Asie", sector: "Groupe Lazarus, Ronin Bridge Hack 625M$ & Mixers Tornado Cash pour Financement Nucléaire", composite_score: 78.45, shadow_fleet_oil_score: 72.0, crypto_sanctions_bypass_score: 95.0, shell_company_network_score: 78.0, correspondent_banking_evasion_score: 68.0, risk_level: "critique", primary_pattern: "cryptomonnaies_armes_sanctions", key_signals: ["Évasion de sanctions systématique par Corée du Nord — infrastructure organisée de contournement avec déni de responsabilité étatique", "Flotte fantôme et réseaux opaques — pétroliers sous pavillons de complaisance, sociétés écrans et corridors bancaires alternatifs", "Subversion de l'ordre économique international — les sanctions perdent leur effet dissuasif face à des écosystèmes d'évasion industriels"], estimated_sanctions_evasion_index: 7.85, last_updated: "2026-06-20" },
    { id: "SE-004", name: "Venezuela — Or Illicite CLAP & Routes Caribéennes", country: "Amérique du Sud", sector: "Or Illicite via Guyane/Dominique, Maduro CLAP Corruption & Cryptomonnaies Petro Étatiques", composite_score: 79.6, shadow_fleet_oil_score: 82.0, crypto_sanctions_bypass_score: 72.0, shell_company_network_score: 88.0, correspondent_banking_evasion_score: 75.0, risk_level: "critique", primary_pattern: "reseau_societes_ecrans", key_signals: ["Évasion de sanctions systématique par Venezuela — infrastructure organisée de contournement avec déni de responsabilité étatique", "Flotte fantôme et réseaux opaques — pétroliers sous pavillons de complaisance, sociétés écrans et corridors bancaires alternatifs", "Subversion de l'ordre économique international — les sanctions perdent leur effet dissuasif face à des écosystèmes d'évasion industriels"], estimated_sanctions_evasion_index: 7.96, last_updated: "2026-06-20" },
    { id: "SE-005", name: "Myanmar — Junte & Shadow Banking ASEAN", country: "Asie du Sud-Est", sector: "Juntes TATMADAW, Banques Thaïlandes Complices & Jade/Rubis Illicites via Chine", composite_score: 56.6, shadow_fleet_oil_score: 55.0, crypto_sanctions_bypass_score: 52.0, shell_company_network_score: 62.0, correspondent_banking_evasion_score: 58.0, risk_level: "élevé", primary_pattern: "fraude_financiere_etatique", key_signals: ["Fraude financière étatique par Myanmar — recours actif aux circuits alternatifs SWIFT pour contourner les restrictions internationales", "Shadow banking et hawala — transferts informels et correspondants bancaires complices dans les juridictions non coopératives", "Financement d'activités proscrites — évasion des sanctions alimentant le développement d'armes et programmes proliférants"], estimated_sanctions_evasion_index: 5.66, last_updated: "2026-06-20" },
    { id: "SE-006", name: "Cuba & Nicaragua — Routes Caïmans & Panama", country: "Amérique Centrale", sector: "CIMEX Cuba Offshore, Bancorp Nicaragua & Remises Diaspora Contournant Sanctions OFAC", composite_score: 50.15, shadow_fleet_oil_score: 48.0, crypto_sanctions_bypass_score: 55.0, shell_company_network_score: 52.0, correspondent_banking_evasion_score: 45.0, risk_level: "élevé", primary_pattern: "fraude_financiere_etatique", key_signals: ["Fraude financière étatique par Cuba & Nicaragua — recours actif aux circuits alternatifs SWIFT pour contourner les restrictions internationales", "Shadow banking et hawala — transferts informels et correspondants bancaires complices dans les juridictions non coopératives", "Financement d'activités proscrites — évasion des sanctions alimentant le développement d'armes et programmes proliférants"], estimated_sanctions_evasion_index: 5.02, last_updated: "2026-06-20" },
    { id: "SE-007", name: "Turquie & EAU — Hubs Régionaux de Contournement", country: "MENA/Europe", sector: "Istanbul Hub Russe Post-Sanctions, Dubaï Or Russe & Correspondants Bancaires Non-Coopératifs", composite_score: 34.5, shadow_fleet_oil_score: 32.0, crypto_sanctions_bypass_score: 28.0, shell_company_network_score: 38.0, correspondent_banking_evasion_score: 42.0, risk_level: "modéré", primary_pattern: "fraude_financiere_etatique", key_signals: ["Hub de contournement régional — Turquie & EAU facilite passivement l'évasion de sanctions sans mécanismes de contrôle suffisants", "Supervision insuffisante — lacunes réglementaires permettant le transit de fonds et marchandises sanctionnées sur le territoire", "Risque de sanctions secondaires — exposition aux mesures punitives américaines pour facilitation d'évasion de sanctions"], estimated_sanctions_evasion_index: 3.45, last_updated: "2026-06-20" },
    { id: "SE-008", name: "OFAC & FATF — Conformité Sanctions Multilatérale", country: "Global", sector: "SDN List 10000+ Entités, FATF Recommandations & Coordination G7/UE Sanctions Ciblées", composite_score: 4.45, shadow_fleet_oil_score: 5.0, crypto_sanctions_bypass_score: 4.0, shell_company_network_score: 3.0, correspondent_banking_evasion_score: 6.0, risk_level: "faible", primary_pattern: "conformite_sanctions", key_signals: ["OFAC & FATF maintient une conformité exemplaire aux régimes de sanctions — application rigoureuse OFAC/FATF et coopération internationale", "Registres de bénéficiaires effectifs transparents — propriété réelle vérifiable et blocage des sociétés écrans sanctionnées", "Modèle d'application des sanctions à diffuser — partage de renseignement financier et coordination multilatérale anti-évasion"], estimated_sanctions_evasion_index: 0.45, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { evasion_sanctions_systematique: 2, cryptomonnaies_armes_sanctions: 1, reseau_societes_ecrans: 1, fraude_financiere_etatique: 3, conformite_sanctions: 1 },
    top_risk_entities: ["Russie — Shadow Fleet 400+ Pétroliers & Contournement G7", "Iran — NIOC & 40 Ans d'Évasion OFAC Industrielle", "Venezuela — Or Illicite CLAP & Routes Caribéennes"],
    critical_alerts: ["Russie: évasion sanctions systématique", "Iran: évasion sanctions systématique", "Corée du Nord: cryptomonnaies armes sanctions", "Venezuela: réseau sociétés écrans"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "sanctions_evasion",
    confidence_score: 0.82,
    data_sources: ["ofac_sdn_sanctions_tracker", "fatf_grey_list_monitor", "kyckr_shadow_fleet_database"],
    entities,
    avg_estimated_sanctions_evasion_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
