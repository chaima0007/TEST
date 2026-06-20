import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[academic-freedom-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Academic Freedom Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/academic-freedom-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Academic Freedom Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Academic Freedom Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "AF-001", name: "Chine — Universités Sous Contrôle CPC", country: "Asie", sector: "Censure Politique Totale & Endoctrinement Xi Jinping", composite_score: 90.25, political_censorship_score: 95.0, researcher_persecution_score: 88.0, brain_drain_severity_score: 85.0, institutional_autonomy_loss_score: 92.0, risk_level: "critique", primary_pattern: "controle_ideologique_universitaire", key_signals: ["Répression académique totale dans Chine — chercheurs emprisonnés, universités sous contrôle étatique", "Censure politique systémique — thèmes de recherche interdits, auto-censure généralisée", "Fuite des cerveaux massive — talents académiques quittant le pays pour préserver leur liberté"], estimated_repression_index: 9.03, last_updated: "2026-06-20" },
    { entity_id: "AF-002", name: "Russie — Académiques Emprisonnés & Exil", country: "Europe de l'Est", sector: "Répression Post-2022 & Universités en Exil", composite_score: 89.5, political_censorship_score: 90.0, researcher_persecution_score: 92.0, brain_drain_severity_score: 88.0, institutional_autonomy_loss_score: 85.0, risk_level: "critique", primary_pattern: "repression_academique_totale", key_signals: ["Répression académique totale dans Russie — chercheurs emprisonnés, universités sous contrôle étatique", "Censure politique systémique — thèmes de recherche interdits, auto-censure généralisée", "Fuite des cerveaux massive — talents académiques quittant le pays pour préserver leur liberté"], estimated_repression_index: 8.95, last_updated: "2026-06-20" },
    { entity_id: "AF-003", name: "Iran — Sciences sous Révolution Islamique", country: "MENA", sector: "Purge des Chercheurs & Contrôle Idéologique Total", composite_score: 86.45, political_censorship_score: 88.0, researcher_persecution_score: 85.0, brain_drain_severity_score: 82.0, institutional_autonomy_loss_score: 88.0, risk_level: "critique", primary_pattern: "repression_academique_totale", key_signals: ["Répression académique totale dans Iran — chercheurs emprisonnés, universités sous contrôle étatique", "Censure politique systémique — thèmes de recherche interdits, auto-censure généralisée", "Fuite des cerveaux massive — talents académiques quittant le pays pour préserver leur liberté"], estimated_repression_index: 8.65, last_updated: "2026-06-20" },
    { entity_id: "AF-004", name: "Turquie — Purges Post-Coup 2016", country: "Europe/MENA", sector: "5000 Académiques Licenciés & Universités Fermées", composite_score: 78.25, political_censorship_score: 80.0, researcher_persecution_score: 78.0, brain_drain_severity_score: 75.0, institutional_autonomy_loss_score: 80.0, risk_level: "critique", primary_pattern: "repression_academique_totale", key_signals: ["Répression académique totale dans Turquie — chercheurs emprisonnés, universités sous contrôle étatique", "Censure politique systémique — thèmes de recherche interdits, auto-censure généralisée", "Fuite des cerveaux massive — talents académiques quittant le pays pour préserver leur liberté"], estimated_repression_index: 7.83, last_updated: "2026-06-20" },
    { entity_id: "AF-005", name: "Hongrie — Capture Académique Orban", country: "Europe", sector: "CEU Expulsée & Contrôle Politique des Universités", composite_score: 63.5, political_censorship_score: 65.0, researcher_persecution_score: 60.0, brain_drain_severity_score: 55.0, institutional_autonomy_loss_score: 70.0, risk_level: "élevé", primary_pattern: "pression_systemique", key_signals: ["Pression systémique sur les académiques dans Hongrie — financements conditionnels et ingérence politique", "Autonomie institutionnelle érodée — gouvernance universitaire contrôlée par le politique", "Brain drain accéléré — chercheurs fuyant vers des environnements académiques libres"], estimated_repression_index: 6.35, last_updated: "2026-06-20" },
    { entity_id: "AF-006", name: "USA — Campus Wars & Financement Conditionnel", country: "Amérique du Nord", sector: "Pressions Politiques des Deux Bords & Autocensure", composite_score: 33.5, political_censorship_score: 42.0, researcher_persecution_score: 28.0, brain_drain_severity_score: 22.0, institutional_autonomy_loss_score: 38.0, risk_level: "modéré", primary_pattern: "tensions_academiques", key_signals: ["Tensions sur l'indépendance académique dans USA — pressions politiques mais institutions résistantes", "Autocensure partielle — certains sujets difficiles à étudier sans risques professionnels", "Financement académique partiellement conditionné — risque d'orientation de la recherche"], estimated_repression_index: 3.35, last_updated: "2026-06-20" },
    { entity_id: "AF-007", name: "France & Allemagne — Tensions Académiques", country: "Europe", sector: "Pression sur les Études Postcoloniales & Genre", composite_score: 19.75, political_censorship_score: 25.0, researcher_persecution_score: 12.0, brain_drain_severity_score: 18.0, institutional_autonomy_loss_score: 22.0, risk_level: "faible", primary_pattern: "liberte_academique_exemplaire", key_signals: ["France & Allemagne préserve une liberté académique exemplaire — recherche indépendante garantie légalement", "Universités autonomes et chercheurs protégés — innovation intellectuelle florissante", "Modèle d'infrastructure épistémique à préserver et exporter pour soutenir la démocratie mondiale"], estimated_repression_index: 1.98, last_updated: "2026-06-20" },
    { entity_id: "AF-008", name: "Pays Nordiques & Suisse — Modèles Académiques", country: "Europe du Nord", sector: "Liberté Académique Constitutionnelle & Financement Public", composite_score: 4.5, political_censorship_score: 5.0, researcher_persecution_score: 3.0, brain_drain_severity_score: 8.0, institutional_autonomy_loss_score: 4.0, risk_level: "faible", primary_pattern: "liberte_academique_exemplaire", key_signals: ["Pays Nordiques & Suisse préserve une liberté académique exemplaire — recherche indépendante garantie légalement", "Universités autonomes et chercheurs protégés — innovation intellectuelle florissante", "Modèle d'infrastructure épistémique à préserver et exporter pour soutenir la démocratie mondiale"], estimated_repression_index: 0.45, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 1, "modéré": 1, faible: 2 },
    pattern_distribution: { repression_academique_totale: 3, controle_ideologique_universitaire: 1, pression_systemique: 1, tensions_academiques: 1, liberte_academique_exemplaire: 2 },
    top_risk_entities: ["Chine — Universités Sous Contrôle CPC", "Russie — Académiques Emprisonnés & Exil", "Iran — Sciences sous Révolution Islamique"],
    critical_alerts: ["Chine: contrôle idéologique universitaire", "Russie: répression académique totale", "Iran: répression académique totale", "Turquie: répression académique totale"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "academic_freedom",
    confidence_score: 0.87,
    data_sources: ["scholars_at_risk_network", "academic_freedom_index", "university_world_news_tracker"],
    entities,
    avg_estimated_repression_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
