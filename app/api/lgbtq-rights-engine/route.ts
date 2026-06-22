import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[lgbtq-rights-engine] SWARM_API_URL non défini — mode mock activé");
}

const MOCK = {
  agent: "LGBTQ+ Rights Engine Agent",
  domain: "lgbtq_rights",
  total_entities: 8,
  avg_composite: 61.22,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: { criminalization_violence_severity: 4, legal_protection_recognition_absence: 3, asylum_refugee_lgbtq_protection_gap: 1 },
  top_risk_entities: [
    "Afrique Sub-Saharienne — 32 Pays Criminalisation, Peine Mort Uganda/Mauritanie & Violence Police",
    "Moyen-Orient/Iran-Arabie Saoudite — Exécutions Légales, Torture & Zéro Protection Réfugiés",
    "Russie/Europe de l'Est — Loi Propagande, Chasse aux Gays Tchétchénie & Discrimination",
  ],
  critical_alerts: [
    "Afrique Sub-Saharienne: criminalization_violence_severity",
    "Moyen-Orient/Iran-Arabie Saoudite: criminalization_violence_severity",
    "Russie/Europe de l'Est: legal_protection_recognition_absence",
    "Asie du Sud-Est/Malaisie-Brunei: criminalization_violence_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_lgbtq_rights_index: 6.12,
  data_sources: [
    "ilga_world_state_sponsored_homophobia_global_legislation_report",
    "human_rights_watch_lgbtq_rights_criminalization_violence_report",
    "rainbow_europe_map_index_lgbtq_rights_comparative_report",
  ],
  entities: [
    { id: "LGR-001", name: "Afrique Sub-Saharienne — 32 Pays Criminalisation, Peine Mort Uganda/Mauritanie & Violence Police", country: "Afrique Sub-Saharienne", sector: "32 Pays Criminalisation Homosexualité Afrique Sub-Saharienne ILGA 2024, Ouganda Anti-Homosexuality Act 2023 Peine Mort, Mauritanie Lapidation, Violence Police Impunie & ONG LGBT Fermées", composite_score: 92.9, criminalization_violence_severity_score: 95.0, legal_protection_recognition_absence_score: 93.0, healthcare_access_discrimination_scale_score: 91.0, asylum_refugee_lgbtq_protection_gap_score: 92.0, risk_level: "critique", primary_pattern: "criminalization_violence_severity", estimated_lgbtq_rights_index: 9.29, last_updated: "2026-06-21" },
    { id: "LGR-002", name: "Moyen-Orient/Iran-Arabie Saoudite — Exécutions Légales, Torture & Zéro Protection Réfugiés", country: "Moyen-Orient", sector: "Iran 75+ Exécutions LGBT 1979-2024 Pendaison, Arabie Saoudite Flagellation/Prison Charia, Torture Systématique, Zéro Protection Réfugiés LGBTQ+ & Surveillance Digitale Applications", composite_score: 91.05, criminalization_violence_severity_score: 93.0, legal_protection_recognition_absence_score: 91.0, healthcare_access_discrimination_scale_score: 88.0, asylum_refugee_lgbtq_protection_gap_score: 92.0, risk_level: "critique", primary_pattern: "criminalization_violence_severity", estimated_lgbtq_rights_index: 9.11, last_updated: "2026-06-21" },
    { id: "LGR-003", name: "Russie/Europe de l'Est — Loi Propagande, Chasse aux Gays Tchétchénie & Discrimination", country: "Europe de l'Est", sector: "Russie Loi Propagande Homosexuelle 2013/2023 Élargie, Chasse aux Gays Tchétchénie 2017-19 Camps Clandestins HRW, Kadyrov Déni Total, Criminalisation Trans Proposée & 700+ ONG Restreintes", composite_score: 87.0, criminalization_violence_severity_score: 90.0, legal_protection_recognition_absence_score: 88.0, healthcare_access_discrimination_scale_score: 84.0, asylum_refugee_lgbtq_protection_gap_score: 85.0, risk_level: "critique", primary_pattern: "legal_protection_recognition_absence", estimated_lgbtq_rights_index: 8.7, last_updated: "2026-06-21" },
    { id: "LGR-004", name: "Asie du Sud-Est/Malaisie-Brunei — Flagellation Sharia, Arrestations LGBT & Pression Sociale", country: "Asie du Sud-Est", sector: "Brunei Code Pénal Charia 2019 Lapidation Homosexualité, Malaisie Flagellation/Prison LGBT, Arrestations Régulières Actes Sexuels Consentis & Pression Sociale/Religieuse Extrême", composite_score: 84.05, criminalization_violence_severity_score: 87.0, legal_protection_recognition_absence_score: 85.0, healthcare_access_discrimination_scale_score: 82.0, asylum_refugee_lgbtq_protection_gap_score: 81.0, risk_level: "critique", primary_pattern: "criminalization_violence_severity", estimated_lgbtq_rights_index: 8.41, last_updated: "2026-06-21" },
    { id: "LGR-005", name: "Amérique Latine/Brésil — Assassinats Trans Record, Violence Malgré Légalisation & Impunité", country: "Amérique Latine", sector: "Brésil 1er Mondial Meurtres Trans 2023 TGEU, Violence LGBT Despite Mariage Légal 2013, Impunité Quasi-Totale Auteurs & Rhétorique Anti-LGBT Bolsonaro Legacy", composite_score: 53.85, criminalization_violence_severity_score: 58.0, legal_protection_recognition_absence_score: 52.0, healthcare_access_discrimination_scale_score: 53.0, asylum_refugee_lgbtq_protection_gap_score: 51.0, risk_level: "élevé", primary_pattern: "criminalization_violence_severity", estimated_lgbtq_rights_index: 5.39, last_updated: "2026-06-21" },
    { id: "LGR-006", name: "USA/Régression — Lois Anti-Trans Mineurs, Books Bans & Recul Droits Post-2022", country: "Amérique du Nord", sector: "USA 20+ États Lois Anti-Trans Mineurs Soins Médicaux 2023, Interdictions Livres LGBT Bibliothèques, Recul Droits Post-Dobbs & Harcèlement Communauté LGBTQ+", composite_score: 51.0, criminalization_violence_severity_score: 52.0, legal_protection_recognition_absence_score: 52.0, healthcare_access_discrimination_scale_score: 52.0, asylum_refugee_lgbtq_protection_gap_score: 47.0, risk_level: "élevé", primary_pattern: "legal_protection_recognition_absence", estimated_lgbtq_rights_index: 5.1, last_updated: "2026-06-21" },
    { id: "LGR-007", name: "ILGA World/Rainbow Europe — Cartographie Droits, Plaidoyer ONU & Standards Protection", country: "Global", sector: "ILGA World State Sponsored Homophobia Report Annuel 2024, Rainbow Europe Map Index Droits LGBTQ+, Plaidoyer CDH-ONU Résolutions & Standards Protection Internationaux", composite_score: 25.85, criminalization_violence_severity_score: 28.0, legal_protection_recognition_absence_score: 25.0, healthcare_access_discrimination_scale_score: 24.0, asylum_refugee_lgbtq_protection_gap_score: 26.0, risk_level: "modéré", primary_pattern: "legal_protection_recognition_absence", estimated_lgbtq_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "LGR-008", name: "ONU/Principes Jogjakarta — Résolution HRC, Experts Indépendants & SDG Inclusion", country: "Global", sector: "Principes Jogjakarta 2006/2017 Cadre Normatif International, Résolution CDH-ONU SOGI, Expert Indépendant IE SOGI Mandate & SDG Inclusion Orientation Sexuelle Identité Genre", composite_score: 4.05, criminalization_violence_severity_score: 5.0, legal_protection_recognition_absence_score: 4.0, healthcare_access_discrimination_scale_score: 3.0, asylum_refugee_lgbtq_protection_gap_score: 4.0, risk_level: "faible", primary_pattern: "asylum_refugee_lgbtq_protection_gap", estimated_lgbtq_rights_index: 0.41, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/lgbtq-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
