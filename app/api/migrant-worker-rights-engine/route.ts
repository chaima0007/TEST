import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[migrant-worker-rights-engine] SWARM_API_URL not set — returning mock");
}

const MOCK = {
  agent: "Migrant Worker Rights Engine Agent",
  domain: "migrant_worker_rights",
  total_entities: 8,
  avg_composite: 60.94,
  confidence_score: 0.82,
  avg_estimated_migrant_worker_rights_index: 6.09,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: { dependance_systeme_kafala: 5, dette_frais_recrutement: 2, exclusion_droits_travail: 1 },
  top_risk_entities: [
    "Qatar/Kafala — 6 500+ Morts Migrants Coupe du Monde FIFA, Servitude Contractuelle & Réformes 2021 Insuffisantes",
    "Arabie Saoudite/EAU — Servitude Contractuelle, 25M Travailleurs Captifs Système Kafala & Domestiques Sans Protection",
    "Malaisie/Plantations Huile Palme — Esclavage Travailleurs Migrants, Top Glove Sanctions & Frais Recrutement Dettes",
  ],
  critical_alerts: [
    "Qatar/Kafala: dependance_systeme_kafala",
    "Arabie Saoudite/EAU: dependance_systeme_kafala",
    "Malaisie/Plantations Huile Palme: dette_frais_recrutement",
    "Singapour: dette_frais_recrutement",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  data_sources: [
    "ilo_fair_recruitment_2023",
    "migrant_forum_asia_2023",
    "human_rights_watch_migrant_workers_2022",
    "ilo_forced_labour_migrants_2022",
  ],
  entities: [
    { id: "MW-001", name: "Qatar/Kafala — 6 500+ Morts Migrants Coupe du Monde FIFA, Servitude Contractuelle & Réformes 2021 Insuffisantes", country: "MENA", sector: "Qatar 6 500+ Morts Travailleurs Migrants Stades FIFA 2010-22 Estimation Guardian, Kafala Système Captivité, Passeports Confisqués & Réformes 2021 Insuffisantes ILO", wage_theft_exploitation_score: 92.0, recruitment_fee_debt_score: 88.0, kafala_system_dependency_score: 95.0, labor_rights_access_failure_score: 88.0, composite_score: 90.95, risk_level: "critique", primary_pattern: "dependance_systeme_kafala", estimated_migrant_worker_rights_index: 9.10, last_updated: "2026-06-21" },
    { id: "MW-002", name: "Arabie Saoudite/EAU — Servitude Contractuelle, 25M Travailleurs Captifs Système Kafala & Domestiques Sans Protection", country: "MENA", sector: "25M Travailleurs Migrants Golfe Système Kafala EAU/KSA/Koweït/Bahreïn, Changement Emploi Interdit, Travailleuses Domestiques Exclues Code Travail & Réformes Cosmétiques", wage_theft_exploitation_score: 88.0, recruitment_fee_debt_score: 85.0, kafala_system_dependency_score: 92.0, labor_rights_access_failure_score: 85.0, composite_score: 87.65, risk_level: "critique", primary_pattern: "dependance_systeme_kafala", estimated_migrant_worker_rights_index: 8.77, last_updated: "2026-06-21" },
    { id: "MW-003", name: "Malaisie/Plantations Huile Palme — Esclavage Travailleurs Migrants, Top Glove Sanctions & Frais Recrutement Dettes", country: "Asie du Sud-Est", sector: "Top Glove Malaisie Gants Latex 10 000 Travailleurs Migrants Logements Surpeuplés, Frais Recrutement 3 000$, Palm Oil Travailleurs Népalais/Bangladeshis Esclavage & Sanctions USA CBP 2020", wage_theft_exploitation_score: 85.0, recruitment_fee_debt_score: 90.0, kafala_system_dependency_score: 85.0, labor_rights_access_failure_score: 82.0, composite_score: 85.65, risk_level: "critique", primary_pattern: "dette_frais_recrutement", estimated_migrant_worker_rights_index: 8.57, last_updated: "2026-06-21" },
    { id: "MW-004", name: "Singapour — Travailleurs Domestiques Sans Protection Légale, Employment Pass & Exclusion Loi Travail", country: "Asie du Sud-Est", sector: "Singapour 250 000 Travailleurs Domestiques Exclus Employment Act, FDW Employment Agency Frais, Passeports Confisqués Employeurs, Abus Signalés HRW & Recours Juridique Limité", wage_theft_exploitation_score: 82.0, recruitment_fee_debt_score: 85.0, kafala_system_dependency_score: 80.0, labor_rights_access_failure_score: 85.0, composite_score: 82.85, risk_level: "critique", primary_pattern: "dette_frais_recrutement", estimated_migrant_worker_rights_index: 8.29, last_updated: "2026-06-21" },
    { id: "MW-005", name: "Thaïlande — Travailleurs Pêche/Construction Anti-Syndicat, Bateaux Haute Mer & Frais Recrutement Myanmar", country: "Asie du Sud-Est", sector: "Thaïlande Pêche Maritime Travailleurs Migrants Myanmar/Cambodge Esclavage Bateaux, Pêche Haute Mer Hors Portée Inspection, AP Enquête 2015, ILO C188 Non-Ratifié & Syndicats Interdits Migrants", wage_theft_exploitation_score: 55.0, recruitment_fee_debt_score: 52.0, kafala_system_dependency_score: 58.0, labor_rights_access_failure_score: 50.0, composite_score: 54.0, risk_level: "élevé", primary_pattern: "dependance_systeme_kafala", estimated_migrant_worker_rights_index: 5.40, last_updated: "2026-06-21" },
    { id: "MW-006", name: "Jordanie — Réfugiés Syriens Travail Informel, Permis Liés Employeur & Kafala-Like Sponsorship", country: "MENA", sector: "Jordanie 670 000+ Réfugiés Syriens Enregistrés UNHCR, 80% Secteur Informel Sans Protection, Permis Travail Liés Employeur Kafala-Like, Travailleurs Agricoles Exclus Code Travail & Violations Non Sanctionnées", wage_theft_exploitation_score: 52.0, recruitment_fee_debt_score: 48.0, kafala_system_dependency_score: 55.0, labor_rights_access_failure_score: 55.0, composite_score: 52.35, risk_level: "élevé", primary_pattern: "dependance_systeme_kafala", estimated_migrant_worker_rights_index: 5.24, last_updated: "2026-06-21" },
    { id: "MW-007", name: "UE — Directive Travailleurs Saisonniers Partiellement Appliquée, Caporalato Italie & Lacunes Protection", country: "Europe", sector: "UE Directive Travailleurs Saisonniers 2014/36/UE Application Partielle, Italie Caporalato Exploitation Agricole Africains, Allemagne Tönnies COVID 2020, Grèce Fraises Manolada & Décret Flussi Insuffisant", wage_theft_exploitation_score: 30.0, recruitment_fee_debt_score: 28.0, kafala_system_dependency_score: 32.0, labor_rights_access_failure_score: 28.0, composite_score: 29.6, risk_level: "modéré", primary_pattern: "dependance_systeme_kafala", estimated_migrant_worker_rights_index: 2.96, last_updated: "2026-06-21" },
    { id: "MW-008", name: "Nouvelle-Zélande — RSE Travailleurs Migrants, Droits Syndicaux & Ratification Conventions ILO", country: "Pacifique", sector: "Nouvelle-Zélande RSE Migrants Employment Relations Act, Travailleurs Migrants Droit Syndicat, Seasonal Worker Programme Protections, Immigration Advisers Act & Ratification ILO C97 C143", wage_theft_exploitation_score: 5.0, recruitment_fee_debt_score: 4.0, kafala_system_dependency_score: 3.0, labor_rights_access_failure_score: 6.0, composite_score: 4.45, risk_level: "faible", primary_pattern: "exclusion_droits_travail", estimated_migrant_worker_rights_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/migrant-worker-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data));
  } catch {
    return NextResponse.json(sealResponse(MOCK), { status: 502 });
  }
}
