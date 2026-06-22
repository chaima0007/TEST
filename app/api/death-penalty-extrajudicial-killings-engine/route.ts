import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[death-penalty-extrajudicial-killings-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  "agent": "Death Penalty Extrajudicial Killings Engine Agent",
  "domain": "death_penalty_extrajudicial_killings",
  "total_entities": 8,
  "avg_composite": 61.5,
  "confidence_score": 0.85,
  "risk_distribution": {
    "critique": 4,
    "élevé": 2,
    "modéré": 1,
    "faible": 1
  },
  "pattern_distribution": {
    "extrajudicial_killing_state_sanctioned_severity": 2,
    "death_penalty_wrongful_execution_scale": 2,
    "enforced_disappearance_targeted_assassination": 2,
    "accountability_impunity_state_violence_deficit_gap": 2
  },
  "top_risk_entities": [
    "Philippines/Duterte — Guerre Drogues 30 000 Morts Extrajudiciaires, Escadrons Mort PNP, Impunité Totale & Autodafé Suspects",
    "Chine Exécutions — Plus Grand Nombre Mondial Exécutions, Peine Mort Crimes Non-Violents, Organes Prisonniers Conscience & Exécutions Secrètes",
    "Iran Pendaisons — Exécutions Mineurs, Pendaisons Publiques, Peine Mort Homosexualité & Prisonniers Politiques Exécutés"
  ],
  "critical_alerts": [
    "Philippines/Duterte: extrajudicial_killing_state_sanctioned_severity",
    "Chine Exécutions: death_penalty_wrongful_execution_scale",
    "Iran Pendaisons: enforced_disappearance_targeted_assassination",
    "Syrie/Russie: accountability_impunity_state_violence_deficit_gap"
  ],
  "last_analysis": "2026-06-21",
  "engine_version": "1.0.0",
  "avg_estimated_death_penalty_extrajudicial_killings_index": 6.15,
  "data_sources": [
    "amnesty_international_death_penalty_global_report",
    "reprieve_extrajudicial_killing_documentation",
    "un_special_rapporteur_extrajudicial_executions_reports"
  ],
  "entities": [
    {
      "entity_id": "DPE-001",
      "name": "Philippines/Duterte — Guerre Drogues 30 000 Morts Extrajudiciaires, Escadrons Mort PNP, Impunité Totale & Autodafé Suspects",
      "country": "Philippines",
      "extrajudicial_killing_state_sanctioned_severity_score": 96.0,
      "death_penalty_wrongful_execution_scale_score": 92.0,
      "enforced_disappearance_targeted_assassination_score": 94.0,
      "accountability_impunity_state_violence_deficit_gap_score": 90.0,
      "primary_pattern": "extrajudicial_killing_state_sanctioned_severity",
      "last_updated": "2026-06-21",
      "composite_score": 93.3,
      "risk_level": "critique",
      "estimated_death_penalty_extrajudicial_killings_index": 9.33
    },
    {
      "entity_id": "DPE-002",
      "name": "Chine Exécutions — Plus Grand Nombre Mondial Exécutions, Peine Mort Crimes Non-Violents, Organes Prisonniers Conscience & Exécutions Secrètes",
      "country": "Chine",
      "extrajudicial_killing_state_sanctioned_severity_score": 93.0,
      "death_penalty_wrongful_execution_scale_score": 90.0,
      "enforced_disappearance_targeted_assassination_score": 89.0,
      "accountability_impunity_state_violence_deficit_gap_score": 88.0,
      "primary_pattern": "death_penalty_wrongful_execution_scale",
      "last_updated": "2026-06-21",
      "composite_score": 90.25,
      "risk_level": "critique",
      "estimated_death_penalty_extrajudicial_killings_index": 9.03
    },
    {
      "entity_id": "DPE-003",
      "name": "Iran Pendaisons — Exécutions Mineurs, Pendaisons Publiques, Peine Mort Homosexualité & Prisonniers Politiques Exécutés",
      "country": "Iran",
      "extrajudicial_killing_state_sanctioned_severity_score": 90.0,
      "death_penalty_wrongful_execution_scale_score": 87.0,
      "enforced_disappearance_targeted_assassination_score": 86.0,
      "accountability_impunity_state_violence_deficit_gap_score": 85.0,
      "primary_pattern": "enforced_disappearance_targeted_assassination",
      "last_updated": "2026-06-21",
      "composite_score": 87.25,
      "risk_level": "critique",
      "estimated_death_penalty_extrajudicial_killings_index": 8.73
    },
    {
      "entity_id": "DPE-004",
      "name": "Syrie/Russie — Assassinats Ciblés Opposants, Disparitions Forcées Journalistes, Bombardements Civils Impunis & Wagner Exécutions Filmées",
      "country": "Syrie/Russie",
      "extrajudicial_killing_state_sanctioned_severity_score": 87.0,
      "death_penalty_wrongful_execution_scale_score": 83.0,
      "enforced_disappearance_targeted_assassination_score": 84.0,
      "accountability_impunity_state_violence_deficit_gap_score": 82.0,
      "primary_pattern": "accountability_impunity_state_violence_deficit_gap",
      "last_updated": "2026-06-21",
      "composite_score": 84.25,
      "risk_level": "critique",
      "estimated_death_penalty_extrajudicial_killings_index": 8.43
    },
    {
      "entity_id": "DPE-005",
      "name": "USA/Arabie Saoudite — Peine Mort Débat Innocents Exécutés USA, Décapitations Arabie Saoudite & Disparités Raciales Couloir Mort",
      "country": "USA/Arabie Saoudite",
      "extrajudicial_killing_state_sanctioned_severity_score": 57.0,
      "death_penalty_wrongful_execution_scale_score": 55.0,
      "enforced_disappearance_targeted_assassination_score": 54.0,
      "accountability_impunity_state_violence_deficit_gap_score": 53.0,
      "primary_pattern": "death_penalty_wrongful_execution_scale",
      "last_updated": "2026-06-21",
      "composite_score": 54.95,
      "risk_level": "élevé",
      "estimated_death_penalty_extrajudicial_killings_index": 5.5
    },
    {
      "entity_id": "DPE-006",
      "name": "Brésil/Inde — Violences Policières Favelas Brésil, Rencontres Policières Inde & Impunité Systémique Forces Ordre",
      "country": "Brésil/Inde",
      "extrajudicial_killing_state_sanctioned_severity_score": 54.0,
      "death_penalty_wrongful_execution_scale_score": 52.0,
      "enforced_disappearance_targeted_assassination_score": 51.0,
      "accountability_impunity_state_violence_deficit_gap_score": 50.0,
      "primary_pattern": "extrajudicial_killing_state_sanctioned_severity",
      "last_updated": "2026-06-21",
      "composite_score": 51.95,
      "risk_level": "élevé",
      "estimated_death_penalty_extrajudicial_killings_index": 5.2
    },
    {
      "entity_id": "DPE-007",
      "name": "Amnesty/Reprieve — Documentation Condamnés Innocents, Plaidoyer Abolition Mondiale & Représentation Légale Condamnés Mort",
      "country": "Global",
      "extrajudicial_killing_state_sanctioned_severity_score": 28.0,
      "death_penalty_wrongful_execution_scale_score": 26.0,
      "enforced_disappearance_targeted_assassination_score": 25.0,
      "accountability_impunity_state_violence_deficit_gap_score": 24.0,
      "primary_pattern": "accountability_impunity_state_violence_deficit_gap",
      "last_updated": "2026-06-21",
      "composite_score": 25.95,
      "risk_level": "modéré",
      "estimated_death_penalty_extrajudicial_killings_index": 2.6
    },
    {
      "entity_id": "DPE-008",
      "name": "ONU/2ème Protocole — Protocole Facultatif Abolition Peine Mort, Rapporteur Spécial Exécutions Extrajudiciaires & Moratoire Universel",
      "country": "Global",
      "extrajudicial_killing_state_sanctioned_severity_score": 5.0,
      "death_penalty_wrongful_execution_scale_score": 4.0,
      "enforced_disappearance_targeted_assassination_score": 4.0,
      "accountability_impunity_state_violence_deficit_gap_score": 3.0,
      "primary_pattern": "enforced_disappearance_targeted_assassination",
      "last_updated": "2026-06-21",
      "composite_score": 4.1,
      "risk_level": "faible",
      "estimated_death_penalty_extrajudicial_killings_index": 0.41
    }
  ]
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/death-penalty-extrajudicial-killings-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
