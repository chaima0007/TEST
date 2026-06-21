import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[dark-web-cybercrime-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "dark_web_cybercrime_rights_engine",
  domain: "dark_web_cybercrime_rights",
  total_entities: 8,
  avg_composite: 63.11,
  confidence_score: 0.91,
  accent: "#7c3aed",
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    state_nexus_cybercrime: 4,
    victim_rights_gap: 2,
    law_enforcement_overreach: 1,
    privacy_erosion: 1,
  },
  top_risk_entities: [
    { id: "DWC-003", name: "Chine — Grand Firewall, APT41, Surveillance Numérique Totale", score: 93.0, risk: "critique" },
    { id: "DWC-002", name: "Corée du Nord — Lazarus Group, Cybercrime Financement Régime", score: 92.6, risk: "critique" },
    { id: "DWC-001", name: "Russie — Infrastructure Cybercrime État-Parrain, Impunité Totale", score: 91.7, risk: "critique" },
  ],
  critical_alerts: [
    "DWC-001: Russie — Infrastructure Cybercrime État-Parrain — composite 91.70",
    "DWC-002: Corée du Nord — Lazarus Group, Cybercrime Financement Régime — composite 92.60",
    "DWC-003: Chine — Grand Firewall, APT41, Surveillance Numérique Totale — composite 93.00",
    "DWC-004: Iran — MOIS Cyberops, Journalistes & Opposants Traqués — composite 88.90",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_dark_web_cybercrime_rights_index: 6.31,
  data_sources: [
    "europol_iocta_cybercrime_2024",
    "crowdstrike_global_threat_report_2024",
    "mandiant_apt_groups_2024",
    "un_odc_cybercrime_report_2023",
  ],
  entities: [
    {
      id: "DWC-001",
      name: "Russie — Infrastructure Cybercrime État-Parrain, Impunité Totale",
      country: "Russie",
      cybercrime_infrastructure_state_nexus_score: 96,
      victim_rights_redress_deficit_score: 92,
      law_enforcement_overreach_rights_score: 88,
      digital_privacy_erosion_score: 90,
      composite_score: 91.7,
      risk_level: "critique",
      primary_pattern: "APT29/Sandworm opèrent avec protection FSB, ransomware REvil toléré, victimes sans recours",
      estimated_dark_web_cybercrime_rights_index: 9.17,
      last_updated: "2026-06-21",
    },
    {
      id: "DWC-002",
      name: "Corée du Nord — Lazarus Group, Cybercrime Financement Régime",
      country: "Corée du Nord",
      cybercrime_infrastructure_state_nexus_score: 97,
      victim_rights_redress_deficit_score: 95,
      law_enforcement_overreach_rights_score: 85,
      digital_privacy_erosion_score: 93,
      composite_score: 92.6,
      risk_level: "critique",
      primary_pattern: "Lazarus Group vole 3B$/an, financement missiles nucléaires, citoyens DPRK zéro droits numériques",
      estimated_dark_web_cybercrime_rights_index: 9.26,
      last_updated: "2026-06-21",
    },
    {
      id: "DWC-003",
      name: "Chine — Grand Firewall, APT41, Surveillance Numérique Totale",
      country: "Chine",
      cybercrime_infrastructure_state_nexus_score: 93,
      victim_rights_redress_deficit_score: 88,
      law_enforcement_overreach_rights_score: 94,
      digital_privacy_erosion_score: 96,
      composite_score: 93.0,
      risk_level: "critique",
      primary_pattern: "APT41 hybride espionnage/cybercrime, PIPL détournée surveillance, dissidents ciblés dark web",
      estimated_dark_web_cybercrime_rights_index: 9.3,
      last_updated: "2026-06-21",
    },
    {
      id: "DWC-004",
      name: "Iran — MOIS Cyberops, Journalistes & Opposants Traqués",
      country: "Iran",
      cybercrime_infrastructure_state_nexus_score: 88,
      victim_rights_redress_deficit_score: 90,
      law_enforcement_overreach_rights_score: 91,
      digital_privacy_erosion_score: 87,
      composite_score: 88.9,
      risk_level: "critique",
      primary_pattern: "Phosphorus/Charming Kitten cible diaspora iranienne, VPN criminalisé, journalistes surveillés Tor",
      estimated_dark_web_cybercrime_rights_index: 8.89,
      last_updated: "2026-06-21",
    },
    {
      id: "DWC-005",
      name: "Nigéria — Fraude BEC, Victimes Sans Protection Légale",
      country: "Nigéria",
      cybercrime_infrastructure_state_nexus_score: 52,
      victim_rights_redress_deficit_score: 58,
      law_enforcement_overreach_rights_score: 48,
      digital_privacy_erosion_score: 50,
      composite_score: 51.7,
      risk_level: "élevé",
      primary_pattern: "Business Email Compromise 1.5B$/an, EFCC sous-financée, victimes internationales sans recours",
      estimated_dark_web_cybercrime_rights_index: 5.17,
      last_updated: "2026-06-21",
    },
    {
      id: "DWC-006",
      name: "Brésil — Darkweb Favelas, Trafic Données Personnelles",
      country: "Brésil",
      cybercrime_infrastructure_state_nexus_score: 48,
      victim_rights_redress_deficit_score: 55,
      law_enforcement_overreach_rights_score: 52,
      digital_privacy_erosion_score: 53,
      composite_score: 51.65,
      risk_level: "élevé",
      primary_pattern: "220M données personnelles vendues dark web 2021, forums cybercrime Lusophone, LGPD ineffective",
      estimated_dark_web_cybercrime_rights_index: 5.16,
      last_updated: "2026-06-21",
    },
    {
      id: "DWC-007",
      name: "Inde — Dark Web Trafic Données Biométriques Aadhaar",
      country: "Inde",
      cybercrime_infrastructure_state_nexus_score: 28,
      victim_rights_redress_deficit_score: 32,
      law_enforcement_overreach_rights_score: 26,
      digital_privacy_erosion_score: 30,
      composite_score: 28.8,
      risk_level: "modéré",
      primary_pattern: "Données Aadhaar 1.1B citoyens vendues dark web, IT Act utilisé contre journalistes, protection faible",
      estimated_dark_web_cybercrime_rights_index: 2.88,
      last_updated: "2026-06-21",
    },
    {
      id: "DWC-008",
      name: "Pays-Bas — Europol Leader Anti-Cybercrime, Droits Numériques Protégés",
      country: "Pays-Bas",
      cybercrime_infrastructure_state_nexus_score: 6,
      victim_rights_redress_deficit_score: 5,
      law_enforcement_overreach_rights_score: 8,
      digital_privacy_erosion_score: 7,
      composite_score: 6.55,
      risk_level: "faible",
      primary_pattern: "Siège Europol, démantèlement Hive ransomware, RGPD strict, droits numériques constitutionnels",
      estimated_dark_web_cybercrime_rights_index: 0.66,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/dark-web-cybercrime-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
