import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[autonomous-weapons-ai-warfare-rights-engine] SWARM_API_URL is not set — using mock data");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  {
    entity_id: "AWR-001",
    name: "USA/DARPA — Autonomous F-16 Dogfight, Drone Swarms, Loitering Munitions Kargu & LAWS Aucun Veto Humain Cible",
    country: "USA",
    sector: "Systèmes Armes Autonomes Létales",
    lethal_autonomous_weapon_civilian_harm_severity_score: 94.0,
    human_control_accountability_removal_scale_score: 92.0,
    ai_bias_targeting_discrimination_score: 93.0,
    autonomous_weapon_ban_treaty_deficit_gap_score: 91.0,
    primary_pattern: "lethal_autonomous_weapon_civilian_harm_severity",
  },
  {
    entity_id: "AWR-002",
    name: "Russie/Uran-9 — Robots Combat Syrie, S-70 Okhotnik Drone, IA Cibles Non-Supervisée & KUB-BLA Kamikaze",
    country: "Russie",
    sector: "Robots Combat IA Non-Supervisée",
    lethal_autonomous_weapon_civilian_harm_severity_score: 90.0,
    human_control_accountability_removal_scale_score: 92.0,
    ai_bias_targeting_discrimination_score: 88.0,
    autonomous_weapon_ban_treaty_deficit_gap_score: 90.0,
    primary_pattern: "human_control_accountability_removal_scale",
  },
  {
    entity_id: "AWR-003",
    name: "Chine/PLA — IA Militaire Plan 2030, Drone CH-5 Ventes Export, Systèmes Anti-Drones IA & Sharp Sword UCAV",
    country: "Chine",
    sector: "IA Militaire Exportation",
    lethal_autonomous_weapon_civilian_harm_severity_score: 87.0,
    human_control_accountability_removal_scale_score: 85.0,
    ai_bias_targeting_discrimination_score: 88.0,
    autonomous_weapon_ban_treaty_deficit_gap_score: 86.0,
    primary_pattern: "lethal_autonomous_weapon_civilian_harm_severity",
  },
  {
    entity_id: "AWR-004",
    name: "Israël/Elbit — Système Harpy LAWS, Hermes Ciblage Automatique, Iron Dome IA & Export Sans Contrôle Humain",
    country: "Israël",
    sector: "Export LAWS Ciblage Automatique",
    lethal_autonomous_weapon_civilian_harm_severity_score: 83.0,
    human_control_accountability_removal_scale_score: 82.0,
    ai_bias_targeting_discrimination_score: 84.0,
    autonomous_weapon_ban_treaty_deficit_gap_score: 81.0,
    primary_pattern: "ai_bias_targeting_discrimination",
  },
  {
    entity_id: "AWR-005",
    name: "UE/Défense — Eurodrone Autonomie Partielle, FCAS Humain Supervisé, Politique IA Éthique Défense & Règlement IA Exemption Militaire",
    country: "Europe",
    sector: "Défense Européenne IA Éthique",
    lethal_autonomous_weapon_civilian_harm_severity_score: 56.0,
    human_control_accountability_removal_scale_score: 54.0,
    ai_bias_targeting_discrimination_score: 55.0,
    autonomous_weapon_ban_treaty_deficit_gap_score: 57.0,
    primary_pattern: "autonomous_weapon_ban_treaty_deficit_gap",
  },
  {
    entity_id: "AWR-006",
    name: "Turquie/Bayraktar — TB2 Usage Libyen/Azerbaïdjan, Kargu-2 LAWS Exporté, Pas Veto Humain Obligatoire & Réglementations Absentes",
    country: "Turquie",
    sector: "Export Drones LAWS Réglementation Absente",
    lethal_autonomous_weapon_civilian_harm_severity_score: 52.0,
    human_control_accountability_removal_scale_score: 51.0,
    ai_bias_targeting_discrimination_score: 54.0,
    autonomous_weapon_ban_treaty_deficit_gap_score: 53.0,
    primary_pattern: "human_control_accountability_removal_scale",
  },
  {
    entity_id: "AWR-007",
    name: "ICRC/PAX — Campagne Stop Killer Robots, CICR Appel Réglementation, CCW GGE LAWS Genève & Principes Martens Application",
    country: "Global",
    sector: "Plaidoyer International LAWS",
    lethal_autonomous_weapon_civilian_harm_severity_score: 27.0,
    human_control_accountability_removal_scale_score: 25.0,
    ai_bias_targeting_discrimination_score: 28.0,
    autonomous_weapon_ban_treaty_deficit_gap_score: 26.0,
    primary_pattern: "autonomous_weapon_ban_treaty_deficit_gap",
  },
  {
    entity_id: "AWR-008",
    name: "ONU/CCW — Convention Certaines Armes Classiques GGE LAWS, Résolution ONU IA Militaire 2023 & Dix Principes Guterres",
    country: "Global",
    sector: "Cadre Normatif International LAWS",
    lethal_autonomous_weapon_civilian_harm_severity_score: 4.0,
    human_control_accountability_removal_scale_score: 4.0,
    ai_bias_targeting_discrimination_score: 4.0,
    autonomous_weapon_ban_treaty_deficit_gap_score: 4.0,
    primary_pattern: "lethal_autonomous_weapon_civilian_harm_severity",
  },
];

type AWRInput = (typeof MOCK_ENTITIES)[0];

function computeComposite(e: AWRInput): number {
  return Math.round(
    (e.lethal_autonomous_weapon_civilian_harm_severity_score * 0.30
    + e.human_control_accountability_removal_scale_score * 0.25
    + e.ai_bias_targeting_discrimination_score * 0.25
    + e.autonomous_weapon_ban_treaty_deficit_gap_score * 0.20) * 100
  ) / 100;
}

function riskLevel(composite: number): string {
  if (composite >= 60) return "critique";
  if (composite >= 40) return "élevé";
  if (composite >= 20) return "modéré";
  return "faible";
}

function severity(composite: number): string {
  if (composite >= 60) return "crise_gouvernance_laws_létale_systémique";
  if (composite >= 40) return "crise_prolifération_armes_autonomes_majeure";
  if (composite >= 20) return "risque_biais_algorithmique_ciblage_structurel";
  return "surveillance_traités_armes_autonomes";
}

function recommendedAction(risk: string): string {
  if (risk === "critique") return "intervention_urgente_contrôle_laws_humain";
  if (risk === "élevé") return "renforcement_traités_non_prolifération_laws";
  if (risk === "modéré") return "révision_mécanismes_supervision_humaine_ia";
  return "veille_gouvernance_armes_autonomes_continue";
}

function signal(risk: string): string {
  if (risk === "critique") return "CRITIQUE — Crise gouvernance LAWS létale systémique — contrôle humain en péril";
  if (risk === "élevé") return "ÉLEVÉ — Crise prolifération armes autonomes majeure détectée";
  if (risk === "modéré") return "MODÉRÉ — Risque biais algorithmique ciblage structurel actif";
  return "FAIBLE — Surveillance traités armes autonomes continue";
}

function estimatedIndex(composite: number): number {
  return Math.round(composite / 100 * 10 * 100) / 100;
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map((e) => {
      const composite = computeComposite(e);
      const risk = riskLevel(composite);
      return {
        entity_id: e.entity_id,
        name: e.name,
        country: e.country,
        sector: e.sector,
        lethal_autonomous_weapon_civilian_harm_severity_score: e.lethal_autonomous_weapon_civilian_harm_severity_score,
        human_control_accountability_removal_scale_score: e.human_control_accountability_removal_scale_score,
        ai_bias_targeting_discrimination_score: e.ai_bias_targeting_discrimination_score,
        autonomous_weapon_ban_treaty_deficit_gap_score: e.autonomous_weapon_ban_treaty_deficit_gap_score,
        composite_score: composite,
        risk_level: risk,
        primary_pattern: e.primary_pattern,
        severity: severity(composite),
        recommended_action: recommendedAction(risk),
        signal: signal(risk),
        estimated_autonomous_weapons_ai_warfare_rights_index: estimatedIndex(composite),
        last_updated: "2026-06-21",
      };
    });

    const risk_distribution: Record<string, number> = {};
    const pattern_distribution: Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number> = {};
    let totalComposite = 0;
    let critiqueCount = 0, élevéCount = 0, modéréCount = 0, faibleCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level] = (risk_distribution[ent.risk_level] || 0) + 1;
      pattern_distribution[ent.primary_pattern] = (pattern_distribution[ent.primary_pattern] || 0) + 1;
      severity_distribution[ent.severity] = (severity_distribution[ent.severity] || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      totalComposite += ent.composite_score;
      if (ent.risk_level === "critique") critiqueCount++;
      else if (ent.risk_level === "élevé") élevéCount++;
      else if (ent.risk_level === "modéré") modéréCount++;
      else faibleCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(totalComposite / n * 100) / 100;

    const summary = {
      module_id: 981,
      module_name: "Autonomous Weapons AI Warfare Rights Intelligence Engine",
      agent: "Autonomous Weapons AI Warfare Rights Engine Agent",
      domain: "autonomous_weapons_ai_warfare_rights",
      total: n,
      critique: critiqueCount,
      élevé: élevéCount,
      modéré: modéréCount,
      faible: faibleCount,
      avg_composite: avgComposite,
      avg_estimated_autonomous_weapons_ai_warfare_rights_index: estimatedIndex(avgComposite),
      risk_distribution,
      pattern_distribution,
      severity_distribution,
      action_distribution,
      confidence_score: 0.85,
      data_sources: [
        "icrc_autonomous_weapons_report",
        "stop_killer_robots_campaign_report",
        "un_secretary_general_new_agenda_peace",
      ],
      last_analysis: "2026-06-21",
      engine_version: "1.0.0",
    };

    return NextResponse.json(
      sealResponse({ entities, summary } as Record<string, unknown>)
    );
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/autonomous-weapons-ai-warfare-rights-engine`);
    const res = await fetch(url.toString(), { next: { revalidate: 30 } });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(
    sealResponse({ entities: [], summary: {} } as Record<string, unknown>),
    { status: 502 }
  );
}
