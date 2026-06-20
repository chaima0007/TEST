import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-divide-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Digital Divide Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-divide-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Digital Divide Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Digital Divide Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "DD-001", name: "Agence Numérique Mali", country: "Mali", sector: "Infrastructure Télécoms", composite_score: 80.80, infrastructure_gap_score: 88, skills_exclusion_score: 82, economic_barrier_score: 78, governance_gap_score: 72, risk_level: "critique", primary_pattern: "Désert Numérique", key_signals: ["Taux pénétration internet 18% — zones rurales < 3%", "85% population sans compétences numériques de base", "Coût data mobile > 15% revenu mensuel médian"], estimated_divide_index: 8.08, last_updated: "2026-06-20" },
    { entity_id: "DD-002", name: "Autorité Numérique Bangladesh", country: "Bangladesh", sector: "Éducation Numérique", composite_score: 75.50, infrastructure_gap_score: 78, skills_exclusion_score: 82, economic_barrier_score: 72, governance_gap_score: 68, risk_level: "critique", primary_pattern: "Analphabétisme Numérique", key_signals: ["60 millions sans accès internet fiable", "Femmes rurales : 92% sans accès smartphones", "Aucune loi de protection données personnelles"], estimated_divide_index: 7.55, last_updated: "2026-06-20" },
    { entity_id: "DD-003", name: "Ministère Transformation Digitale Nigeria", country: "Nigeria", sector: "Gouvernance Numérique", composite_score: 69.85, infrastructure_gap_score: 72, skills_exclusion_score: 65, economic_barrier_score: 80, governance_gap_score: 60, risk_level: "critique", primary_pattern: "Barrière Économique Numérique", key_signals: ["Fracture nord-sud : Lagos 78% vs nord < 12% connecté", "Prix données parmi les plus élevés d'Afrique/revenu", "Réglementation données fragmentée entre 36 États"], estimated_divide_index: 6.99, last_updated: "2026-06-20" },
    { entity_id: "DD-004", name: "Instituto Digital Brésil Rural", country: "Brésil", sector: "Infrastructure Télécoms", composite_score: 59.80, infrastructure_gap_score: 58, skills_exclusion_score: 55, economic_barrier_score: 65, governance_gap_score: 62, risk_level: "élevé", primary_pattern: "Fracture Numérique Structurelle", key_signals: ["Amazonie : 45 millions sans haut débit", "Fracture générationnelle senior > 60 ans critique", "Inégalité numérique corrèle à inégalité revenus Gini"], estimated_divide_index: 5.98, last_updated: "2026-06-20" },
    { entity_id: "DD-005", name: "Agence Connexion Rurale Inde", country: "Inde", sector: "Éducation Numérique", composite_score: 53.10, infrastructure_gap_score: 52, skills_exclusion_score: 48, economic_barrier_score: 58, governance_gap_score: 55, risk_level: "élevé", primary_pattern: "Fracture Numérique Structurelle", key_signals: ["350 millions utilisateurs connectés mais peu qualifiés", "Fracture genre : 40% moins de femmes en ligne", "Qualité connexion rurale 2G vs 5G urbain"], estimated_divide_index: 5.31, last_updated: "2026-06-20" },
    { entity_id: "DD-006", name: "Observatoire Inclusion Numérique Roumanie", country: "Roumanie", sector: "Gouvernance Numérique", composite_score: 36.55, infrastructure_gap_score: 38, skills_exclusion_score: 35, economic_barrier_score: 40, governance_gap_score: 32, risk_level: "modéré", primary_pattern: "Fracture Numérique Structurelle", key_signals: ["Rural : 35% ménages sans internet fixe", "Seniors > 65 ans : 70% exclus services numériques", "Administration numérique insuffisante vs UE moyenne"], estimated_divide_index: 3.66, last_updated: "2026-06-20" },
    { entity_id: "DD-007", name: "Agence Numérique Finlande", country: "Finlande", sector: "Infrastructure Télécoms", composite_score: 14.00, infrastructure_gap_score: 15, skills_exclusion_score: 12, economic_barrier_score: 18, governance_gap_score: 10, risk_level: "faible", primary_pattern: "Inclusion Numérique Satisfaisante", key_signals: ["Internet haut débit : droit constitutionnel reconnu", "95% population compétences numériques certifiées", "RGPD + loi nationale données — cadre exemplaire"], estimated_divide_index: 1.40, last_updated: "2026-06-20" },
    { entity_id: "DD-008", name: "Ministère Digital Pays-Bas", country: "Pays-Bas", sector: "Éducation Numérique", composite_score: 9.60, infrastructure_gap_score: 10, skills_exclusion_score: 8, economic_barrier_score: 12, governance_gap_score: 8, risk_level: "faible", primary_pattern: "Inclusion Numérique Satisfaisante", key_signals: ["98% ménages fibre ou câble haut débit", "Programme NL leert door — formation permanente", "Coût abonnement internet parmi les plus bas EU"], estimated_divide_index: 0.96, last_updated: "2026-06-20" },
  ];

  const n = entities.length;
  const avg_composite = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / n * 100) / 100;

  return {
    total_entities: n,
    avg_composite,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: { "Désert Numérique": 1, "Analphabétisme Numérique": 1, "Barrière Économique Numérique": 1, "Fracture Numérique Structurelle": 3, "Inclusion Numérique Satisfaisante": 2 },
    top_risk_entities: ["Agence Numérique Mali", "Autorité Numérique Bangladesh", "Ministère Transformation Digitale Nigeria"],
    critical_alerts: 3,
    last_analysis: "2026-06-20",
    engine_version: "2.1.0",
    domain: "divide",
    confidence_score: 84.2,
    data_sources: ["UIT — Rapport Mondial Connectivité 2025", "Banque Mondiale — Digital Economy Data 2026", "Web Foundation — Digital Rights Report 2026"],
    entities,
    avg_estimated_divide_index: Math.round(avg_composite / 100 * 10 * 100) / 100,
  };
}
