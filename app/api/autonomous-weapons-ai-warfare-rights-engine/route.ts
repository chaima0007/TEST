import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[autonomous-weapons-ai-warfare-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Autonomous Weapons AI Warfare Rights Engine Agent",
  domain: "autonomous_weapons_ai_warfare_rights",
  total_entities: 8,
  avg_composite: 61.28,
  confidence_score: 0.85,
  risk_distribution: { "critique": 4, "élevé": 2, "modéré": 1, "faible": 1 },
  pattern_distribution: { "lethal_autonomous_weapon_civilian_harm_severity": 3, "human_control_accountability_removal_scale": 2, "ai_bias_targeting_discrimination": 1, "autonomous_weapon_ban_treaty_deficit_gap": 2 },
  top_risk_entities: ["USA/DARPA — Autonomous F-16 Dogfight, Drone Swarms, Loitering Munitions Kargu & LAWS Aucun Veto Humain Cible", "Russie/Uran-9 — Robots Combat Syrie, S-70 Okhotnik Drone, IA Cibles Non-Supervisée & KUB-BLA Kamikaze", "Chine/PLA — IA Militaire Plan 2030, Drone CH-5 Ventes Export, Systèmes Anti-Drones IA & Sharp Sword UCAV"],
  critical_alerts: ["USA/DARPA: lethal_autonomous_weapon_civilian_harm_severity", "Russie/Uran-9: human_control_accountability_removal_scale", "Chine/PLA: lethal_autonomous_weapon_civilian_harm_severity", "Israël/Elbit: ai_bias_targeting_discrimination"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_autonomous_weapons_ai_warfare_rights_index: 6.13,
  data_sources: ["icrc_autonomous_weapons_report", "stop_killer_robots_campaign_report", "un_secretary_general_new_agenda_peace"],
  entities: [
    {
,      entity_id: "AWR-001"
      name: "USA/DARPA — Autonomous F-16 Dogfight, Drone Swarms, Loitering Munitions Kargu & LAWS Aucun Veto Humain Cible"
      country: "USA"
      lethal_autonomous_weapon_civilian_harm_severity_score: 94.0
      human_control_accountability_removal_scale_score: 92.0
      ai_bias_targeting_discrimination_score: 93.0
      autonomous_weapon_ban_treaty_deficit_gap_score: 91.0
      composite_score: 92.65
      risk_level: "critique"
      primary_pattern: "lethal_autonomous_weapon_civilian_harm_severity"
      estimated_autonomous_weapons_ai_warfare_rights_index: 9.27
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AWR-002"
      name: "Russie/Uran-9 — Robots Combat Syrie, S-70 Okhotnik Drone, IA Cibles Non-Supervisée & KUB-BLA Kamikaze"
      country: "Russie"
      lethal_autonomous_weapon_civilian_harm_severity_score: 90.0
      human_control_accountability_removal_scale_score: 92.0
      ai_bias_targeting_discrimination_score: 88.0
      autonomous_weapon_ban_treaty_deficit_gap_score: 90.0
      composite_score: 90.0
      risk_level: "critique"
      primary_pattern: "human_control_accountability_removal_scale"
      estimated_autonomous_weapons_ai_warfare_rights_index: 9.0
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AWR-003"
      name: "Chine/PLA — IA Militaire Plan 2030, Drone CH-5 Ventes Export, Systèmes Anti-Drones IA & Sharp Sword UCAV"
      country: "Chine"
      lethal_autonomous_weapon_civilian_harm_severity_score: 87.0
      human_control_accountability_removal_scale_score: 85.0
      ai_bias_targeting_discrimination_score: 88.0
      autonomous_weapon_ban_treaty_deficit_gap_score: 86.0
      composite_score: 86.55
      risk_level: "critique"
      primary_pattern: "lethal_autonomous_weapon_civilian_harm_severity"
      estimated_autonomous_weapons_ai_warfare_rights_index: 8.65
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AWR-004"
      name: "Israël/Elbit — Système Harpy LAWS, Hermes Ciblage Automatique, Iron Dome IA & Export Sans Contrôle Humain"
      country: "Israël"
      lethal_autonomous_weapon_civilian_harm_severity_score: 83.0
      human_control_accountability_removal_scale_score: 82.0
      ai_bias_targeting_discrimination_score: 84.0
      autonomous_weapon_ban_treaty_deficit_gap_score: 81.0
      composite_score: 82.6
      risk_level: "critique"
      primary_pattern: "ai_bias_targeting_discrimination"
      estimated_autonomous_weapons_ai_warfare_rights_index: 8.26
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AWR-005"
      name: "UE/Défense — Eurodrone Autonomie Partielle, FCAS Humain Supervisé, Politique IA Éthique Défense & Règlement IA Exemption Militaire"
      country: "Europe"
      lethal_autonomous_weapon_civilian_harm_severity_score: 56.0
      human_control_accountability_removal_scale_score: 54.0
      ai_bias_targeting_discrimination_score: 55.0
      autonomous_weapon_ban_treaty_deficit_gap_score: 57.0
      composite_score: 55.45
      risk_level: "élevé"
      primary_pattern: "autonomous_weapon_ban_treaty_deficit_gap"
      estimated_autonomous_weapons_ai_warfare_rights_index: 5.54
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AWR-006"
      name: "Turquie/Bayraktar — TB2 Usage Libyen/Azerbaïdjan, Kargu-2 LAWS Exporté, Pas Veto Humain Obligatoire & Réglementations Absentes"
      country: "Turquie"
      lethal_autonomous_weapon_civilian_harm_severity_score: 52.0
      human_control_accountability_removal_scale_score: 51.0
      ai_bias_targeting_discrimination_score: 54.0
      autonomous_weapon_ban_treaty_deficit_gap_score: 53.0
      composite_score: 52.45
      risk_level: "élevé"
      primary_pattern: "human_control_accountability_removal_scale"
      estimated_autonomous_weapons_ai_warfare_rights_index: 5.25
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AWR-007"
      name: "ICRC/PAX — Campagne Stop Killer Robots, CICR Appel Réglementation, CCW GGE LAWS Genève & Principes Martens Application"
      country: "Global"
      lethal_autonomous_weapon_civilian_harm_severity_score: 27.0
      human_control_accountability_removal_scale_score: 25.0
      ai_bias_targeting_discrimination_score: 28.0
      autonomous_weapon_ban_treaty_deficit_gap_score: 26.0
      composite_score: 26.55
      risk_level: "modéré"
      primary_pattern: "autonomous_weapon_ban_treaty_deficit_gap"
      estimated_autonomous_weapons_ai_warfare_rights_index: 2.66
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AWR-008"
      name: "ONU/CCW — Convention Certaines Armes Classiques GGE LAWS, Résolution ONU IA Militaire 2023 & Dix Principes Guterres"
      country: "Global"
      lethal_autonomous_weapon_civilian_harm_severity_score: 4.0
      human_control_accountability_removal_scale_score: 4.0
      ai_bias_targeting_discrimination_score: 4.0
      autonomous_weapon_ban_treaty_deficit_gap_score: 4.0
      composite_score: 4.0
      risk_level: "faible"
      primary_pattern: "lethal_autonomous_weapon_civilian_harm_severity"
      estimated_autonomous_weapons_ai_warfare_rights_index: 0.4
      last_updated: "2026-06-21"
    }
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/autonomous-weapons-ai-warfare-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
