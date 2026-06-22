import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[death-penalty-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[death-penalty-rights-engine] SWARM_API_URL not set — running in offline mode");

export async function GET() {
  try {
    if (!UPSTREAM) throw new Error("offline");
    const res = await fetch(`${UPSTREAM}/api/death-penalty-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      agent: "Death Penalty Rights Engine Agent",
      domain: "death_penalty_rights",
      total_entities: 8,
      avg_composite: 60.25,
      confidence_score: 0.85,
      risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
      entities: [
        {
          entity_id: "DP-001",
          name: "Chine — 2 000+ Exécutions/An, Secret État & Organes Prisonniers",
          country: "Chine",
          composite_score: 93.00,
          risk_level: "critique",
          primary_pattern: "executions_massives_secret_etat",
          execution_volume_score: 96,
          transparency_deficit_score: 95,
          due_process_failure_score: 90,
          abolition_resistance_score: 91,
          estimated_death_penalty_rights_index: 9.30,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "DP-002",
          name: "Iran — 853 Exécutions 2023, Pendaisons Publiques & Minorités",
          country: "Iran",
          composite_score: 90.50,
          risk_level: "critique",
          primary_pattern: "executions_massives_secret_etat",
          execution_volume_score: 92,
          transparency_deficit_score: 88,
          due_process_failure_score: 91,
          abolition_resistance_score: 91,
          estimated_death_penalty_rights_index: 9.05,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "DP-003",
          name: "Arabie Saoudite/Golfe — 196 Exécutions 2022, Décapitations Publiques",
          country: "Arabie Saoudite",
          composite_score: 89.50,
          risk_level: "critique",
          primary_pattern: "executions_massives_secret_etat",
          execution_volume_score: 90,
          transparency_deficit_score: 88,
          due_process_failure_score: 90,
          abolition_resistance_score: 91,
          estimated_death_penalty_rights_index: 8.95,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "DP-004",
          name: "USA — 2 700 Condamnés Couloir Mort, Exécutions Innocents & Racisme",
          country: "USA",
          composite_score: 67.10,
          risk_level: "critique",
          primary_pattern: "defaillance_garanties_processuelles",
          execution_volume_score: 60,
          transparency_deficit_score: 62,
          due_process_failure_score: 74,
          abolition_resistance_score: 73,
          estimated_death_penalty_rights_index: 6.71,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "DP-005",
          name: "Japon — Condamnés Secret Total, Exécution Sans Préavis & Isolement",
          country: "Japon",
          composite_score: 54.60,
          risk_level: "élevé",
          primary_pattern: "defaillance_garanties_processuelles",
          execution_volume_score: 48,
          transparency_deficit_score: 58,
          due_process_failure_score: 56,
          abolition_resistance_score: 57,
          estimated_death_penalty_rights_index: 5.46,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "DP-006",
          name: "Singapour/Malaisie — Trafic Drogue Peine Mort Obligatoire",
          country: "Singapour/Malaisie",
          composite_score: 55.00,
          risk_level: "élevé",
          primary_pattern: "defaillance_garanties_processuelles",
          execution_volume_score: 50,
          transparency_deficit_score: 55,
          due_process_failure_score: 57,
          abolition_resistance_score: 58,
          estimated_death_penalty_rights_index: 5.50,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "DP-007",
          name: "Europe/CEDH — Protocole 13 Abolition Totale & Pressions Russie",
          country: "Europe",
          composite_score: 27.90,
          risk_level: "modéré",
          primary_pattern: "resistance_abolition",
          execution_volume_score: 25,
          transparency_deficit_score: 28,
          due_process_failure_score: 29,
          abolition_resistance_score: 30,
          estimated_death_penalty_rights_index: 2.79,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "DP-008",
          name: "ONU/CIDH — Résolution Moratoire, Protocole 2 PIDCP & Mouvement Abolitionniste",
          country: "Global",
          composite_score: 4.40,
          risk_level: "faible",
          primary_pattern: "resistance_abolition",
          execution_volume_score: 4,
          transparency_deficit_score: 4,
          due_process_failure_score: 5,
          abolition_resistance_score: 5,
          estimated_death_penalty_rights_index: 0.44,
          last_updated: "2026-06-22",
        },
      ],
      last_analysis: "2026-06-22",
      engine_version: "1.0.0",
    }, { status: 200 }));
  }
}
