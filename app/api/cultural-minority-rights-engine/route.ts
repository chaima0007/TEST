import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[cultural-minority-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Cultural Minority Rights Engine Agent",
  domain: "cultural_minority_rights",
  total_entities: 8,
  avg_composite: 61.44,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { cultural_assimilation_forced_erasure_severity: 1, language_suppression_minority_discrimination_scale: 3, cultural_heritage_destruction_desecration: 2, minority_cultural_participation_exclusion_gap: 2 },
  top_risk_entities: [
    "Ouïghours/Chine — Camps Rééducation, Destruction Mosquées/Cimetières, Langue Interdite Écoles & Assimilation Forcée",
    "Tibétains/Chine — Bouddhisme Contrôlé État, Réincarnation Politisée, Langue Supprimée & Exil Dalaï-Lama",
    "Peuples Autochtones Amazonie — Chamans Assassinés, Rituels Interdits, Langues Mourantes & Évangélisation Forcée",
  ],
  critical_alerts: [
    "Ouïghours/Chine: cultural_assimilation_forced_erasure_severity",
    "Tibétains/Chine: language_suppression_minority_discrimination_scale",
    "Peuples Autochtones Amazonie: cultural_heritage_destruction_desecration",
    "Roms Europe: minority_cultural_participation_exclusion_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_cultural_minority_rights_index: 6.14,
  data_sources: [
    "un_declaration_rights_indigenous_peoples_drip2007",
    "unesco_cultural_diversity_convention_2005_reports",
    "minority_rights_group_international_world_directory",
  ],
  entities: [
    { id: "CMR-001", name: "Ouïghours/Chine — Camps Rééducation, Destruction Mosquées/Cimetières, Langue Interdite Écoles & Assimilation Forcée", country: "Chine", composite_score: 92.95, cultural_assimilation_forced_erasure_severity_score: 95.0, language_suppression_minority_discrimination_scale_score: 93.0, cultural_heritage_destruction_desecration_score: 92.0, minority_cultural_participation_exclusion_gap_score: 91.0, risk_level: "critique", primary_pattern: "cultural_assimilation_forced_erasure_severity", estimated_cultural_minority_rights_index: 9.30, last_updated: "2026-06-21" },
    { id: "CMR-002", name: "Tibétains/Chine — Bouddhisme Contrôlé État, Réincarnation Politisée, Langue Supprimée & Exil Dalaï-Lama", country: "Chine", composite_score: 89.85, cultural_assimilation_forced_erasure_severity_score: 92.0, language_suppression_minority_discrimination_scale_score: 89.0, cultural_heritage_destruction_desecration_score: 88.0, minority_cultural_participation_exclusion_gap_score: 90.0, risk_level: "critique", primary_pattern: "language_suppression_minority_discrimination_scale", estimated_cultural_minority_rights_index: 8.99, last_updated: "2026-06-21" },
    { id: "CMR-003", name: "Peuples Autochtones Amazonie — Chamans Assassinés, Rituels Interdits, Langues Mourantes & Évangélisation Forcée", country: "Brésil/Amazonie", composite_score: 86.90, cultural_assimilation_forced_erasure_severity_score: 89.0, language_suppression_minority_discrimination_scale_score: 86.0, cultural_heritage_destruction_desecration_score: 86.0, minority_cultural_participation_exclusion_gap_score: 86.0, risk_level: "critique", primary_pattern: "cultural_heritage_destruction_desecration", estimated_cultural_minority_rights_index: 8.69, last_updated: "2026-06-21" },
    { id: "CMR-004", name: "Roms Europe — Ségrégation Culturelle, Stérilisations Forcées Histoire, Discrimination Fêtes & Identité Criminalisée", country: "Europe", composite_score: 83.85, cultural_assimilation_forced_erasure_severity_score: 86.0, language_suppression_minority_discrimination_scale_score: 83.0, cultural_heritage_destruction_desecration_score: 82.0, minority_cultural_participation_exclusion_gap_score: 84.0, risk_level: "critique", primary_pattern: "minority_cultural_participation_exclusion_gap", estimated_cultural_minority_rights_index: 8.39, last_updated: "2026-06-21" },
    { id: "CMR-005", name: "Kurdes/Turquie — Langue Kurde Limitée Médias/Éducation, Musique Interdite Périodes, Noms Changés de Force", country: "Turquie", composite_score: 54.85, cultural_assimilation_forced_erasure_severity_score: 57.0, language_suppression_minority_discrimination_scale_score: 54.0, cultural_heritage_destruction_desecration_score: 53.0, minority_cultural_participation_exclusion_gap_score: 55.0, risk_level: "élevé", primary_pattern: "language_suppression_minority_discrimination_scale", estimated_cultural_minority_rights_index: 5.49, last_updated: "2026-06-21" },
    { id: "CMR-006", name: "Bretons/Occitans/Langues Régionales Europe — Standardisation Nationale, Langues Mourantes, Transmission Intergénération Brisée", country: "Europe", composite_score: 51.85, cultural_assimilation_forced_erasure_severity_score: 54.0, language_suppression_minority_discrimination_scale_score: 51.0, cultural_heritage_destruction_desecration_score: 50.0, minority_cultural_participation_exclusion_gap_score: 52.0, risk_level: "élevé", primary_pattern: "language_suppression_minority_discrimination_scale", estimated_cultural_minority_rights_index: 5.19, last_updated: "2026-06-21" },
    { id: "CMR-007", name: "UNESCO Convention Diversité Culturelle — 2005 Convention, Patrimoine Immatériel & Soutien Expressions Minoritaires", country: "Global", composite_score: 27.05, cultural_assimilation_forced_erasure_severity_score: 28.0, language_suppression_minority_discrimination_scale_score: 26.0, cultural_heritage_destruction_desecration_score: 27.0, minority_cultural_participation_exclusion_gap_score: 27.0, risk_level: "modéré", primary_pattern: "cultural_heritage_destruction_desecration", estimated_cultural_minority_rights_index: 2.71, last_updated: "2026-06-21" },
    { id: "CMR-008", name: "ONU/DRIP 2007 — Déclaration Droits Peuples Autochtones, Participation Culturelle & SDG 11.4 Patrimoine Inclusif", country: "Global", composite_score: 4.25, cultural_assimilation_forced_erasure_severity_score: 4.0, language_suppression_minority_discrimination_scale_score: 4.0, cultural_heritage_destruction_desecration_score: 5.0, minority_cultural_participation_exclusion_gap_score: 4.0, risk_level: "faible", primary_pattern: "minority_cultural_participation_exclusion_gap", estimated_cultural_minority_rights_index: 0.43, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/cultural-minority-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
