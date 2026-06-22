import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[dark-web-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[dark-web-rights-engine] SWARM_API_URL not set");

const MOCK = {
  agent: "dark_web_rights_engine",
  domain: "dark_web_rights",
  total_entities: 8,
  avg_composite: 61.84,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    { id: "DWR-001", name: "North Korea Lazarus Group — Cyberattaques étatiques, droits numériques violés", score: 92.80, risk: "critique" },
    { id: "DWR-002", name: "Russia APT Groups — Désinformation, cyberespionnage, violations droits", score: 89.10, risk: "critique" },
    { id: "DWR-003", name: "China MSS APT41 — Surveillance citoyens, droits numériques bafoués", score: 86.65, risk: "critique" },
  ],
  critical_alerts: [
    "DWR-001: North Korea Lazarus Group — Cyberattaques étatiques — composite 92.80",
    "DWR-002: Russia APT Groups — Désinformation massive, cyberespionnage — composite 89.10",
    "DWR-003: China MSS APT41 — Surveillance citoyens dissidents — composite 86.65",
    "DWR-004: Iran IRGC Cyber — Répression numérique opposants — composite 81.60",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_dark_web_rights_index: 6.18,
  data_sources: [
    "mandiant_apt_report_2024",
    "europol_internet_organised_crime_threat_assessment_2023",
    "tor_project_transparency_report_2024",
    "citizen_lab_digital_rights_report_2024",
  ],
  entities: [
    {
      id: "DWR-001",
      name: "North Korea Lazarus Group — Cyberattaques étatiques, droits numériques violés",
      country: "North Korea",
      state_sponsored_cyber_rights_violations_score: 95.0,
      dark_web_criminal_exploitation_score: 90.0,
      digital_privacy_anonymity_rights_score: 94.0,
      law_enforcement_accountability_deficit_score: 92.0,
      composite_score: 92.80,
      risk_level: "critique",
      primary_pattern: "Lazarus Group vole 3Mrd$ crypto, finance armes nucléaires, viole droits numériques globaux",
      estimated_dark_web_rights_index: 9.28,
      last_updated: "2026-06-22",
    },
    {
      id: "DWR-002",
      name: "Russia APT Groups — Désinformation, cyberespionnage, violations droits",
      country: "Russia",
      state_sponsored_cyber_rights_violations_score: 91.0,
      dark_web_criminal_exploitation_score: 88.0,
      digital_privacy_anonymity_rights_score: 89.0,
      law_enforcement_accountability_deficit_score: 89.0,
      composite_score: 89.10,
      risk_level: "critique",
      primary_pattern: "APT28/29 ciblent journalistes, Killnet attaque infrastr. civiles, RuTor marché dark web",
      estimated_dark_web_rights_index: 8.91,
      last_updated: "2026-06-22",
    },
    {
      id: "DWR-003",
      name: "China MSS APT41 — Surveillance citoyens, droits numériques bafoués",
      country: "China",
      state_sponsored_cyber_rights_violations_score: 88.0,
      dark_web_criminal_exploitation_score: 84.0,
      digital_privacy_anonymity_rights_score: 87.0,
      law_enforcement_accountability_deficit_score: 87.0,
      composite_score: 86.65,
      risk_level: "critique",
      primary_pattern: "Great Firewall, MSS surveillance diaspora, APT41 espionnage industriel et dissidents",
      estimated_dark_web_rights_index: 8.67,
      last_updated: "2026-06-22",
    },
    {
      id: "DWR-004",
      name: "Iran IRGC Cyber — Répression numérique opposants",
      country: "Iran",
      state_sponsored_cyber_rights_violations_score: 83.0,
      dark_web_criminal_exploitation_score: 80.0,
      digital_privacy_anonymity_rights_score: 82.0,
      law_enforcement_accountability_deficit_score: 81.0,
      composite_score: 81.60,
      risk_level: "critique",
      primary_pattern: "IRGC traque opposants via dark web, Charming Kitten cible activistes, internet coupé",
      estimated_dark_web_rights_index: 8.16,
      last_updated: "2026-06-22",
    },
    {
      id: "DWR-005",
      name: "Criminal Marketplaces Dark Web — Trafic humains, drogues, armes",
      country: "Global",
      state_sponsored_cyber_rights_violations_score: 50.0,
      dark_web_criminal_exploitation_score: 62.0,
      digital_privacy_anonymity_rights_score: 55.0,
      law_enforcement_accountability_deficit_score: 52.0,
      composite_score: 54.65,
      risk_level: "élevé",
      primary_pattern: "Hydra/Alphabay trafic drogues, CSAM vendu crypto, passeports falsifiés, identités volées",
      estimated_dark_web_rights_index: 5.47,
      last_updated: "2026-06-22",
    },
    {
      id: "DWR-006",
      name: "Dark Web CSAM Networks — Exploitation enfants en ligne",
      country: "Global",
      state_sponsored_cyber_rights_violations_score: 45.0,
      dark_web_criminal_exploitation_score: 68.0,
      digital_privacy_anonymity_rights_score: 53.0,
      law_enforcement_accountability_deficit_score: 52.0,
      composite_score: 54.15,
      risk_level: "élevé",
      primary_pattern: "Réseaux CSAM cryptés, 400K images/vidéos/jour identifiées IWF, victimes non protégées",
      estimated_dark_web_rights_index: 5.42,
      last_updated: "2026-06-22",
    },
    {
      id: "DWR-007",
      name: "EU Authorities Europol — Lutte dark web, lacunes droits numériques",
      country: "European Union",
      state_sponsored_cyber_rights_violations_score: 25.0,
      dark_web_criminal_exploitation_score: 28.0,
      digital_privacy_anonymity_rights_score: 30.0,
      law_enforcement_accountability_deficit_score: 28.0,
      composite_score: 27.75,
      risk_level: "modéré",
      primary_pattern: "Europol démantèle marchés mais RGPD vs surveillance débat, lacunes juridiques cross-border",
      estimated_dark_web_rights_index: 2.78,
      last_updated: "2026-06-22",
    },
    {
      id: "DWR-008",
      name: "Tor Project — Anonymat légitime, protection lanceurs d&apos;alerte",
      country: "Global",
      state_sponsored_cyber_rights_violations_score: 7.0,
      dark_web_criminal_exploitation_score: 9.0,
      digital_privacy_anonymity_rights_score: 8.0,
      law_enforcement_accountability_deficit_score: 8.0,
      composite_score: 8.00,
      risk_level: "faible",
      primary_pattern: "Tor protège journalistes, lanceurs alerte, dissidents — usage légitime droits humains",
      estimated_dark_web_rights_index: 0.80,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const upstream = await fetch(`${SWARM_API_URL}/dark-web-rights-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`upstream ${upstream.status}`);
    const data = await upstream.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 }));
  }
}
