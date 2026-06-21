import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[human-rights-defenders-engine] SWARM_API_URL non défini — mode mock activé");
}

const MOCK = {
  agent: "Human Rights Defenders Engine Agent",
  domain: "human_rights_defenders",
  total_entities: 8,
  avg_composite: 61.83,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: { defender_killing_criminalization_severity: 5, surveillance_harassment_intimidation: 1, legal_framework_protection_absence: 2 },
  top_risk_entities: [
    "Colombie — 180+ Défenseurs Tués/An, Syndicats/Environnementalistes & Impunité 95%",
    "Philippines — Red-Tagging, Duterte Legacy, Journalistes/Avocats Assassinés",
    "Mexique — Cartels vs Journalistes, 15 Journalistes Tués 2023 & Sans Protection État",
  ],
  critical_alerts: [
    "Colombie: defender_killing_criminalization_severity",
    "Philippines: defender_killing_criminalization_severity",
    "Mexique: defender_killing_criminalization_severity",
    "Russie/Biélorussie: defender_killing_criminalization_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_human_rights_defenders_index: 6.18,
  data_sources: [
    "front_line_defenders_annual_report_human_rights_defenders_killed",
    "reporters_sans_frontieres_world_press_freedom_index_report",
    "civicus_monitor_civic_space_closing_global_tracker_report",
  ],
  entities: [
    { entity_id: "HRD-001", name: "Colombie — 180+ Défenseurs Tués/An, Syndicats/Environnementalistes & Impunité 95%", country: "Amérique Latine", sector: "Colombie 187 Défenseurs Tués 2023 Global Witness Record LATAM, Syndicats/Défenseurs Terres Autochtones Ciblés, Groupes Armés Post-FARC Paramilitaires & Impunité 95% Meurtres Défenseurs", composite_score: 94.15, defender_killing_criminalization_severity_score: 97.0, surveillance_harassment_intimidation_scale_score: 93.0, legal_framework_protection_absence_score: 92.0, civic_space_shrinking_repression_score: 94.0, risk_level: "critique", primary_pattern: "defender_killing_criminalization_severity", estimated_human_rights_defenders_index: 9.42, last_updated: "2026-06-21" },
    { entity_id: "HRD-002", name: "Philippines — Red-Tagging, Duterte Legacy, Journalistes/Avocats Assassinés", country: "Asie du Sud-Est", sector: "Philippines Red-Tagging Défenseurs Qualifiés Terroristes NTF-ELCAC, 900+ Activistes Tués Depuis 2016, Avocats/Journalistes/Prêtres Assassinés Karapatan & Impunité Forces Sécurité", composite_score: 91.15, defender_killing_criminalization_severity_score: 93.0, surveillance_harassment_intimidation_scale_score: 91.0, legal_framework_protection_absence_score: 90.0, civic_space_shrinking_repression_score: 90.0, risk_level: "critique", primary_pattern: "defender_killing_criminalization_severity", estimated_human_rights_defenders_index: 9.12, last_updated: "2026-06-21" },
    { entity_id: "HRD-003", name: "Mexique — Cartels vs Journalistes, 15 Journalistes Tués 2023 & Sans Protection État", country: "Amérique Latine", sector: "Mexique 15 Journalistes Tués 2023 RSF, Cartels Tuent Défenseurs Sans Réaction État, Mécanisme Protection Sous-Financé 2012 & Veracruz/Guerrero Zones Mort Défenseurs", composite_score: 87.9, defender_killing_criminalization_severity_score: 90.0, surveillance_harassment_intimidation_scale_score: 87.0, legal_framework_protection_absence_score: 87.0, civic_space_shrinking_repression_score: 87.0, risk_level: "critique", primary_pattern: "defender_killing_criminalization_severity", estimated_human_rights_defenders_index: 8.79, last_updated: "2026-06-21" },
    { entity_id: "HRD-004", name: "Russie/Biélorussie — Memorial Liquidé, Navalny, Journalistes Emprisonnés & Exil Forcé", country: "Europe de l'Est", sector: "Russie Memorial International Liquidé 2021, Alexeï Navalny Tué Détention 2024, Biélorussie 300+ Journalistes Emprisonnés Post-2020, Loi Agents Étrangers & Exil Forcé Défenseurs", composite_score: 85.15, defender_killing_criminalization_severity_score: 87.0, surveillance_harassment_intimidation_scale_score: 85.0, legal_framework_protection_absence_score: 84.0, civic_space_shrinking_repression_score: 84.0, risk_level: "critique", primary_pattern: "defender_killing_criminalization_severity", estimated_human_rights_defenders_index: 8.52, last_updated: "2026-06-21" },
    { entity_id: "HRD-005", name: "Chine/Hong Kong — NSL HK, Avocats 709 & Surveillance AI Défenseurs", country: "Asie du Nord-Est", sector: "Hong Kong National Security Law 2020 Fermeture Médias/ONG, Chine Rafle 709 Avocats 300+, Surveillance AI Reconnaissance Faciale Défenseurs Ouïghours & Interdiction Sortie Territoire", composite_score: 54.55, defender_killing_criminalization_severity_score: 58.0, surveillance_harassment_intimidation_scale_score: 55.0, legal_framework_protection_absence_score: 52.0, civic_space_shrinking_repression_score: 52.0, risk_level: "élevé", primary_pattern: "surveillance_harassment_intimidation", estimated_human_rights_defenders_index: 5.46, last_updated: "2026-06-21" },
    { entity_id: "HRD-006", name: "Turquie/Azerbaïdjan — Procès Journalistes, Lois ONG Restrictives & Harcèlement Judiciaire", country: "Europe du Sud-Est", sector: "Turquie 1 500 Avocats Poursuivis 2016-2024, Taner Kılıç Amnesty 6 Ans Procès, Azerbaïdjan Journalistes Emprisonnés COP29 & Lois ONG Restrictives Agents Étrangers 2022", composite_score: 51.55, defender_killing_criminalization_severity_score: 55.0, surveillance_harassment_intimidation_scale_score: 51.0, legal_framework_protection_absence_score: 50.0, civic_space_shrinking_repression_score: 49.0, risk_level: "élevé", primary_pattern: "defender_killing_criminalization_severity", estimated_human_rights_defenders_index: 5.16, last_updated: "2026-06-21" },
    { entity_id: "HRD-007", name: "Front Line Defenders/RSF/CPJ — Protection Urgente, Alerte Précoce & Relocalisation", country: "Global", sector: "Front Line Defenders Protection Urgente Défenseurs Danger, RSF Reporters Sans Frontières Index Liberté Presse, CPJ Committee Protect Journalists Relocalisation & Alerte Précoce Mécanismes", composite_score: 26.1, defender_killing_criminalization_severity_score: 28.0, surveillance_harassment_intimidation_scale_score: 25.0, legal_framework_protection_absence_score: 25.0, civic_space_shrinking_repression_score: 26.0, risk_level: "modéré", primary_pattern: "legal_framework_protection_absence", estimated_human_rights_defenders_index: 2.61, last_updated: "2026-06-21" },
    { entity_id: "HRD-008", name: "ONU/Déclaration Défenseurs 1998 — Rapporteur Spécial, Mécanismes HRC & SDG 16", country: "Global", sector: "Déclaration ONU Défenseurs Droits Homme 1998 Résolution A/RES/53/144, Rapporteur Spécial ONU HRD Mary Lawlor Depuis 2020, Mécanismes HRC CIDH/UA & SDG 16 Paix Justice", composite_score: 4.05, defender_killing_criminalization_severity_score: 5.0, surveillance_harassment_intimidation_scale_score: 3.0, legal_framework_protection_absence_score: 4.0, civic_space_shrinking_repression_score: 4.0, risk_level: "faible", primary_pattern: "legal_framework_protection_absence", estimated_human_rights_defenders_index: 0.41, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/human-rights-defenders-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
