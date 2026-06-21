import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-privacy-surveillance-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "digital_privacy_surveillance_rights_engine",
  domain: "digital_privacy_surveillance_rights",
  total_entities: 8,
  avg_composite: 60.02,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    surveillance_biometrique_totale: 2,
    shutdown_internet_censure_nationale: 1,
    espionnage_cible_journalistes: 1,
    collecte_masse_sans_cadre_legal: 2,
    protection_vie_privee_exemplaire: 2,
  },
  top_risk_entities: [
    "Chine — Crédit Social, Reconnaissance Faciale 600M Caméras, Surveillance Ouïghours Xinjiang & Firewall",
    "Russie — SORM-3 Surveillance Totale, Blocage VPN, Journalistes Pegasus & Données Trafic FSB Obligatoire",
    "Iran — Surveillance Protestants 2022, Coupures Internet Nationales, Telegram Bloqué & Reconnaissance Faciale Hijab",
    "USA/NSA — PRISM Mass Collection, Pegasus Civils, Section 702 FISA & Absence Loi Fédérale Protection Données",
  ],
  critical_alerts: [
    "Chine — Crédit Social, Reconnaissance Faciale 600M Caméras, Surveillance Ouïghours Xinjiang & Firewall: surveillance biometrique totale",
    "Russie — SORM-3 Surveillance Totale, Blocage VPN, Journalistes Pegasus & Données Trafic FSB Obligatoire: surveillance biometrique totale",
    "Iran — Surveillance Protestants 2022, Coupures Internet Nationales, Telegram Bloqué & Reconnaissance Faciale Hijab: shutdown internet censure nationale",
    "USA/NSA — PRISM Mass Collection, Pegasus Civils, Section 702 FISA & Absence Loi Fédérale Protection Données: espionnage cible journalistes",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_digital_privacy_surveillance_rights_index: 6.0,
  data_sources: [
    "privacy_international_global_surveillance_report",
    "freedom_house_freedom_net_annual_report",
    "citizen_lab_spyware_targeted_surveillance_database",
  ],
  entities: [
    {
      id: "DPS-001",
      name: "Chine — Crédit Social, Reconnaissance Faciale 600M Caméras, Surveillance Ouïghours Xinjiang & Firewall",
      country: "Chine",
      composite_score: 92.6,
      mass_surveillance_biometric_dragnet_severity_score: 96.0,
      internet_shutdown_censorship_scale_score: 92.0,
      spyware_targeted_surveillance_journalist_score: 88.0,
      data_protection_gdpr_enforcement_deficit_gap_score: 94.0,
      risk_level: "critique",
      primary_pattern: "surveillance_biometrique_totale",
      estimated_digital_privacy_surveillance_rights_index: 9.26,
      last_updated: "2026-06-21",
    },
    {
      id: "DPS-002",
      name: "Russie — SORM-3 Surveillance Totale, Blocage VPN, Journalistes Pegasus & Données Trafic FSB Obligatoire",
      country: "Russie",
      composite_score: 88.25,
      mass_surveillance_biometric_dragnet_severity_score: 90.0,
      internet_shutdown_censorship_scale_score: 88.0,
      spyware_targeted_surveillance_journalist_score: 85.0,
      data_protection_gdpr_enforcement_deficit_gap_score: 90.0,
      risk_level: "critique",
      primary_pattern: "surveillance_biometrique_totale",
      estimated_digital_privacy_surveillance_rights_index: 8.83,
      last_updated: "2026-06-21",
    },
    {
      id: "DPS-003",
      name: "Iran — Surveillance Protestants 2022, Coupures Internet Nationales, Telegram Bloqué & Reconnaissance Faciale Hijab",
      country: "Iran",
      composite_score: 85.95,
      mass_surveillance_biometric_dragnet_severity_score: 82.0,
      internet_shutdown_censorship_scale_score: 92.0,
      spyware_targeted_surveillance_journalist_score: 83.0,
      data_protection_gdpr_enforcement_deficit_gap_score: 88.0,
      risk_level: "critique",
      primary_pattern: "shutdown_internet_censure_nationale",
      estimated_digital_privacy_surveillance_rights_index: 8.6,
      last_updated: "2026-06-21",
    },
    {
      id: "DPS-004",
      name: "USA/NSA — PRISM Mass Collection, Pegasus Civils, Section 702 FISA & Absence Loi Fédérale Protection Données",
      country: "États-Unis",
      composite_score: 81.85,
      mass_surveillance_biometric_dragnet_severity_score: 85.0,
      internet_shutdown_censorship_scale_score: 72.0,
      spyware_targeted_surveillance_journalist_score: 83.0,
      data_protection_gdpr_enforcement_deficit_gap_score: 88.0,
      risk_level: "critique",
      primary_pattern: "espionnage_cible_journalistes",
      estimated_digital_privacy_surveillance_rights_index: 8.19,
      last_updated: "2026-06-21",
    },
    {
      id: "DPS-005",
      name: "Inde — Internet Shutdown 84× En 2023, UAPA Surveillance Activistes, Aadhaar Biométrique Obligatoire & Pegasus Journalistes",
      country: "Inde",
      composite_score: 54.25,
      mass_surveillance_biometric_dragnet_severity_score: 55.0,
      internet_shutdown_censorship_scale_score: 58.0,
      spyware_targeted_surveillance_journalist_score: 53.0,
      data_protection_gdpr_enforcement_deficit_gap_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "collecte_masse_sans_cadre_legal",
      estimated_digital_privacy_surveillance_rights_index: 5.43,
      last_updated: "2026-06-21",
    },
    {
      id: "DPS-006",
      name: "UE — Chatcontrol Proposé, RGPD Application Inégale, Métadonnées Stockées & Frontex Surveillance Biométrique",
      country: "Union Européenne",
      composite_score: 47.35,
      mass_surveillance_biometric_dragnet_severity_score: 42.0,
      internet_shutdown_censorship_scale_score: 45.0,
      spyware_targeted_surveillance_journalist_score: 50.0,
      data_protection_gdpr_enforcement_deficit_gap_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "collecte_masse_sans_cadre_legal",
      estimated_digital_privacy_surveillance_rights_index: 4.74,
      last_updated: "2026-06-21",
    },
    {
      id: "DPS-007",
      name: "EFF/Privacy International — Rapports Surveillance, Outils Defense Numérique, Advocacy GDPR & Standards Chiffrement",
      country: "International",
      composite_score: 26.0,
      mass_surveillance_biometric_dragnet_severity_score: 25.0,
      internet_shutdown_censorship_scale_score: 26.0,
      spyware_targeted_surveillance_journalist_score: 28.0,
      data_protection_gdpr_enforcement_deficit_gap_score: 25.0,
      risk_level: "modéré",
      primary_pattern: "protection_vie_privee_exemplaire",
      estimated_digital_privacy_surveillance_rights_index: 2.6,
      last_updated: "2026-06-21",
    },
    {
      id: "DPS-008",
      name: "ONU/Art.17 PIDCP — Droit à la Vie Privée, Rapporteur Spécial Surveillance & SDG 16.10 Liberté Information",
      country: "International",
      composite_score: 3.95,
      mass_surveillance_biometric_dragnet_severity_score: 4.0,
      internet_shutdown_censorship_scale_score: 3.0,
      spyware_targeted_surveillance_journalist_score: 4.0,
      data_protection_gdpr_enforcement_deficit_gap_score: 5.0,
      risk_level: "faible",
      primary_pattern: "protection_vie_privee_exemplaire",
      estimated_digital_privacy_surveillance_rights_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/digital-privacy-surveillance-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
