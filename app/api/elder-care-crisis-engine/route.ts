import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[elder-care-crisis-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Elder Care Crisis Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/elder-care-crisis-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Elder Care Crisis Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Elder Care Crisis Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "EC-001", name: "Système Soins Âgés Japon", country: "Japon", sector: "Gériatrie & Soins Long Terme", composite_score: 79.55, caregiver_shortage_score: 88, facility_quality_gap: 80, affordability_crisis: 75, social_isolation_index: 72, risk_level: "critique", primary_pattern: "Désert de Soins Gériatriques", key_signals: ["Déficit 380 000 soignants gériatriques d'ici 2025", "Kodawari — 1,8M seniors vivant seuls sans contact hebdomadaire", "Coût EHPAD premium > 80% pension retraite médiane"], estimated_eldercare_index: 7.96, last_updated: "2026-06-20" },
    { entity_id: "EC-002", name: "EHPAD Crisis Monitor France", country: "France", sector: "Établissements Médico-Sociaux", composite_score: 74.10, caregiver_shortage_score: 75, facility_quality_gap: 82, affordability_crisis: 70, social_isolation_index: 68, risk_level: "critique", primary_pattern: "Maltraitance Institutionnelle", key_signals: ["Scandal Orpea 2022 — 7 000 signalements maltraitance 2024", "Reste à charge EHPAD 3 000€/mois — inaccessible pour 70%", "Burn-out soignants EHPAD : taux turn-over 42% annuel"], estimated_eldercare_index: 7.41, last_updated: "2026-06-20" },
    { entity_id: "EC-003", name: "Observatoire Seniors Corée du Sud", country: "Corée du Sud", sector: "Protection Sociale Séniors", composite_score: 73.40, caregiver_shortage_score: 78, facility_quality_gap: 70, affordability_crisis: 78, social_isolation_index: 65, risk_level: "critique", primary_pattern: "Inaccessibilité Financière Soins", key_signals: ["Taux pauvreté 65+ : 40% — le plus élevé OCDE", "Ppenion nationale retraite insuffisante : 30% salaire médian", "Suicide seniors +15% — crise silencieuse nationale"], estimated_eldercare_index: 7.34, last_updated: "2026-06-20" },
    { entity_id: "EC-004", name: "Agence Care Séniors Italie", country: "Italie", sector: "Gériatrie & Soins Long Terme", composite_score: 58.90, caregiver_shortage_score: 55, facility_quality_gap: 52, affordability_crisis: 68, social_isolation_index: 62, risk_level: "élevé", primary_pattern: "Inaccessibilité Financière Soins", key_signals: ["650 000 soignants informels — badanti — sans statut légal", "80% services soins long terme privatisés inaccessibles", "Sud Italie : désert gériatrique — 0.4 lit/100 seniors vs 2.1 nord"], estimated_eldercare_index: 5.89, last_updated: "2026-06-20" },
    { entity_id: "EC-005", name: "Senior Care Observatory USA", country: "États-Unis", sector: "Établissements Médico-Sociaux", composite_score: 54.50, caregiver_shortage_score: 50, facility_quality_gap: 48, affordability_crisis: 58, social_isolation_index: 65, risk_level: "élevé", primary_pattern: "Épidémie d'Isolement Sénior", key_signals: ["Nursing home shortage — 100 000 lits fermés depuis COVID", "Medicare ne couvre pas soins long terme — dépenses catastrophiques", "25% seniors 65+ rapportent isolement social sévère — CDC 2025"], estimated_eldercare_index: 5.45, last_updated: "2026-06-20" },
    { entity_id: "EC-006", name: "Institut Soins Âgés Allemagne", country: "Allemagne", sector: "Protection Sociale Séniors", composite_score: 33.60, caregiver_shortage_score: 35, facility_quality_gap: 32, affordability_crisis: 38, social_isolation_index: 28, risk_level: "modéré", primary_pattern: "Crise Soins Personnes Âgées", key_signals: ["Déficit 200 000 soignants — immigration qualifiée nécessaire", "Pflegeversicherung — assurance dépendance partielle insuffisante", "Digitalisation soins : téléassistance déployée 45% seniors"], estimated_eldercare_index: 3.36, last_updated: "2026-06-20" },
    { entity_id: "EC-007", name: "Agence Care Séniors Danemark", country: "Danemark", sector: "Gériatrie & Soins Long Terme", composite_score: 14.00, caregiver_shortage_score: 15, facility_quality_gap: 12, affordability_crisis: 18, social_isolation_index: 10, risk_level: "faible", primary_pattern: "Soins Séniors Satisfaisants", key_signals: ["Soins à domicile universels gratuits — modèle mondial", "Ratio soignant/résident : 0.8 — exemplaire en Europe", "Isolement seniors : programmes municipaux connexion sociale"], estimated_eldercare_index: 1.40, last_updated: "2026-06-20" },
    { entity_id: "EC-008", name: "Centre Bien-Être Séniors Finlande", country: "Finlande", sector: "Protection Sociale Séniors", composite_score: 9.60, caregiver_shortage_score: 10, facility_quality_gap: 8, affordability_crisis: 12, social_isolation_index: 8, risk_level: "faible", primary_pattern: "Soins Séniors Satisfaisants", key_signals: ["Pension retraite universelle garantit niveau vie décent", "Résidences intergénérationnelles — 200 projets pilotes actifs", "IA soins prédictifs déployée 80% EMS — alertes santé précoces"], estimated_eldercare_index: 0.96, last_updated: "2026-06-20" },
  ];

  const n = entities.length;
  const avg_composite = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / n * 100) / 100;

  return {
    total_entities: n,
    avg_composite,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: { "Désert de Soins Gériatriques": 1, "Maltraitance Institutionnelle": 1, "Inaccessibilité Financière Soins": 2, "Épidémie d'Isolement Sénior": 1, "Crise Soins Personnes Âgées": 1, "Soins Séniors Satisfaisants": 2 },
    top_risk_entities: ["Système Soins Âgés Japon", "EHPAD Crisis Monitor France", "Observatoire Seniors Corée du Sud"],
    critical_alerts: 3,
    last_analysis: "2026-06-20",
    engine_version: "2.1.0",
    domain: "eldercare",
    confidence_score: 88.7,
    data_sources: ["OCDE — Panorama Santé Soins Long Terme 2025", "OMS — Rapport Mondial Vieillissement 2026", "HelpAge International — Global Index Séniors 2026"],
    entities,
    avg_estimated_eldercare_index: Math.round(avg_composite / 100 * 10 * 100) / 100,
  };
}
