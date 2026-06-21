import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Digital Surveillance Privacy Rights Engine Agent",
  domain: "digital_surveillance_privacy_rights",
  total_entities: 8,
  avg_composite: 59.78,
  confidence_score: 0.88,
  avg_estimated_digital_surveillance_privacy_rights_index: 5.98,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Chine/GFW II SCS — Surveillance de Masse IA, Crédit Social, Reconnaissance Faciale Ouïghours & Contrôle Internet Total",
    "Russie/SORM Nagulny — Interception Totale Télécoms, Blogage VPN, Surveillance Opposants & Loi Souveraineté Internet",
    "Iran/Internet National — Filtrage Contenu Islamique, Coupures Réseau Protestations, Espionnage Activistes & Contrôle Messageries",
  ],
  critical_alerts: [
    "Chine/GFW II SCS: mass_surveillance_state_infrastructure",
    "Russie/SORM Nagulny: digital_repression_dissidents",
    "Iran/Internet National: digital_repression_dissidents",
    "Biélorussie/Répression Telegram: digital_repression_dissidents",
  ],
  data_sources: [
    "freedom_house_freedom_net_2023",
    "privacy_international_surveillance_database",
    "citizen_lab_targeted_threat_lab_2023",
    "electronic_frontier_foundation_global_surveillance_2023",
  ],
  entities: [
    {
      id: "DSPR-001",
      name: "Chine/GFW II SCS — Surveillance de Masse IA, Crédit Social, Reconnaissance Faciale Ouïghours & Contrôle Internet Total",
      country: "Chine",
      composite_score: 91.0,
      mass_surveillance_state_infrastructure_score: 95.0,
      privacy_legal_protection_enforcement_gap_score: 92.0,
      digital_repression_dissidents_score: 90.0,
      data_exploitation_corporate_impunity_score: 85.0,
      risk_level: "critique",
      primary_pattern: "mass_surveillance_state_infrastructure",
      estimated_digital_surveillance_privacy_rights_index: 9.1,
      last_updated: "2026-06-21",
    },
    {
      id: "DSPR-002",
      name: "Russie/SORM Nagulny — Interception Totale Télécoms, Blogage VPN, Surveillance Opposants & Loi Souveraineté Internet",
      country: "Russie",
      composite_score: 85.75,
      mass_surveillance_state_infrastructure_score: 88.0,
      privacy_legal_protection_enforcement_gap_score: 85.0,
      digital_repression_dissidents_score: 90.0,
      data_exploitation_corporate_impunity_score: 78.0,
      risk_level: "critique",
      primary_pattern: "digital_repression_dissidents",
      estimated_digital_surveillance_privacy_rights_index: 8.58,
      last_updated: "2026-06-21",
    },
    {
      id: "DSPR-003",
      name: "Iran/Internet National — Filtrage Contenu Islamique, Coupures Réseau Protestations, Espionnage Activistes & Contrôle Messageries",
      country: "Iran",
      composite_score: 83.0,
      mass_surveillance_state_infrastructure_score: 85.0,
      privacy_legal_protection_enforcement_gap_score: 82.0,
      digital_repression_dissidents_score: 88.0,
      data_exploitation_corporate_impunity_score: 75.0,
      risk_level: "critique",
      primary_pattern: "digital_repression_dissidents",
      estimated_digital_surveillance_privacy_rights_index: 8.3,
      last_updated: "2026-06-21",
    },
    {
      id: "DSPR-004",
      name: "Biélorussie/Répression Telegram — Surveillance Manifestants 2020, Interception Messages, Arrestations via Données Numériques & Coupures Internet",
      country: "Biélorussie",
      composite_score: 80.25,
      mass_surveillance_state_infrastructure_score: 82.0,
      privacy_legal_protection_enforcement_gap_score: 80.0,
      digital_repression_dissidents_score: 85.0,
      data_exploitation_corporate_impunity_score: 72.0,
      risk_level: "critique",
      primary_pattern: "digital_repression_dissidents",
      estimated_digital_surveillance_privacy_rights_index: 8.03,
      last_updated: "2026-06-21",
    },
    {
      id: "DSPR-005",
      name: "USA/PRISM NSA — Collecte Masse Métadonnées, Section 702 FISA, Surveillance Sans Mandat Étrangers & Absence Recours Citoyens",
      country: "USA",
      composite_score: 55.25,
      mass_surveillance_state_infrastructure_score: 55.0,
      privacy_legal_protection_enforcement_gap_score: 58.0,
      digital_repression_dissidents_score: 45.0,
      data_exploitation_corporate_impunity_score: 65.0,
      risk_level: "élevé",
      primary_pattern: "data_exploitation_corporate_impunity",
      estimated_digital_surveillance_privacy_rights_index: 5.53,
      last_updated: "2026-06-21",
    },
    {
      id: "DSPR-006",
      name: "Inde/NATGRID Surveillance — Interception Légale Élargie, Absence Loi Protection Données Robuste, Coupures Cachemire & Surveillance Journalistes",
      country: "Inde",
      composite_score: 51.0,
      mass_surveillance_state_infrastructure_score: 50.0,
      privacy_legal_protection_enforcement_gap_score: 52.0,
      digital_repression_dissidents_score: 48.0,
      data_exploitation_corporate_impunity_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "privacy_legal_protection_enforcement_gap",
      estimated_digital_surveillance_privacy_rights_index: 5.1,
      last_updated: "2026-06-21",
    },
    {
      id: "DSPR-007",
      name: "UE/RGPD Partiel — Protection Données Avancée Mais Lacunes Sécurité Nationale, Surveillance Policière & Adéquation Transferts Données",
      country: "Union Européenne",
      composite_score: 25.5,
      mass_surveillance_state_infrastructure_score: 25.0,
      privacy_legal_protection_enforcement_gap_score: 28.0,
      digital_repression_dissidents_score: 20.0,
      data_exploitation_corporate_impunity_score: 30.0,
      risk_level: "modéré",
      primary_pattern: "privacy_legal_protection_enforcement_gap",
      estimated_digital_surveillance_privacy_rights_index: 2.55,
      last_updated: "2026-06-21",
    },
    {
      id: "DSPR-008",
      name: "Allemagne/BND Réforme — Réforme Service Renseignement 2021, Cour Constitutionnelle Protection Vie Privée & Cadre Légal Surveillance Limité",
      country: "Allemagne",
      composite_score: 6.5,
      mass_surveillance_state_infrastructure_score: 5.0,
      privacy_legal_protection_enforcement_gap_score: 8.0,
      digital_repression_dissidents_score: 4.0,
      data_exploitation_corporate_impunity_score: 10.0,
      risk_level: "faible",
      primary_pattern: "privacy_legal_protection_enforcement_gap",
      estimated_digital_surveillance_privacy_rights_index: 0.65,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[digital-surveillance-privacy-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-surveillance-privacy-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
