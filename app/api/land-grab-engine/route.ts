import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Types ────────────────────────────────────────────────────────────────────

interface LgeInput {
  id: string;
  land_type: string;
  region: string;
  land_concentration: number;
  smallholder_displacement: number;
  indigenous_rights_violation: number;
  food_production_loss: number;
  water_access_loss: number;
  corporate_opacity: number;
  contract_coercion: number;
  community_consent_absence: number;
  legal_protection_gap: number;
  corruption_index: number;
  monoculture_expansion: number;
  biodiversity_loss: number;
  debt_leverage: number;
  export_orientation: number;
  worker_exploitation: number;
  climate_vulnerability: number;
  conflict_intensity: number;
}

// ─── Mock entities (8 entities covering all 5 patterns and all 4 risk levels) ──
// Patterns: foreign_sovereign_land_capture (land_concentration>0.80 AND corporate_opacity>0.75)
//           corporate_agribusiness_displacement (monoculture_expansion>0.80 AND smallholder_displacement>0.75)
//           climate_migration_land_conflict (climate_vulnerability>0.80 AND conflict_intensity>0.75)
//           indigenous_territory_seizure (indigenous_rights_violation>0.80 AND community_consent_absence>0.75)
//           green_colonialism_trap (debt_leverage>0.80 AND export_orientation>0.75)
// Risk levels: ≥3 critical, ≥2 high, ≥1 moderate, ≥2 low

const MOCK_ENTITIES: LgeInput[] = [
  // LGE-001 — critical, foreign_sovereign_land_capture
  // land_concentration>0.80 AND corporate_opacity>0.75 → foreign_sovereign_land_capture
  // composite ≈ 72 → critical
  {
    id: "LGE-001", land_type: "terres_agricoles", region: "AFRIC",
    land_concentration: 0.88,
    smallholder_displacement: 0.82,
    indigenous_rights_violation: 0.75,
    food_production_loss: 0.78,
    water_access_loss: 0.72,
    corporate_opacity: 0.85,
    contract_coercion: 0.78,
    community_consent_absence: 0.72,
    legal_protection_gap: 0.80,
    corruption_index: 0.82,
    monoculture_expansion: 0.70,
    biodiversity_loss: 0.68,
    debt_leverage: 0.65,
    export_orientation: 0.78,
    worker_exploitation: 0.72,
    climate_vulnerability: 0.65,
    conflict_intensity: 0.68,
  },
  // LGE-002 — critical, corporate_agribusiness_displacement
  // monoculture_expansion>0.80 AND smallholder_displacement>0.75 → corporate_agribusiness_displacement
  // land_concentration≤0.80 → avoids foreign_sovereign_land_capture
  // composite ≈ 68 → critical
  {
    id: "LGE-002", land_type: "terres_cultivables", region: "LATAM",
    land_concentration: 0.75,
    smallholder_displacement: 0.85,
    indigenous_rights_violation: 0.70,
    food_production_loss: 0.72,
    water_access_loss: 0.68,
    corporate_opacity: 0.65,
    contract_coercion: 0.72,
    community_consent_absence: 0.68,
    legal_protection_gap: 0.75,
    corruption_index: 0.70,
    monoculture_expansion: 0.88,
    biodiversity_loss: 0.75,
    debt_leverage: 0.62,
    export_orientation: 0.80,
    worker_exploitation: 0.75,
    climate_vulnerability: 0.60,
    conflict_intensity: 0.65,
  },
  // LGE-003 — critical, indigenous_territory_seizure
  // indigenous_rights_violation>0.80 AND community_consent_absence>0.75 → indigenous_territory_seizure
  // land_concentration≤0.80 → avoids foreign_sovereign_land_capture
  // monoculture_expansion≤0.80 → avoids corporate_agribusiness_displacement
  // composite ≈ 65 → critical
  {
    id: "LGE-003", land_type: "territoires_autochtones", region: "APAC",
    land_concentration: 0.72,
    smallholder_displacement: 0.68,
    indigenous_rights_violation: 0.88,
    food_production_loss: 0.65,
    water_access_loss: 0.70,
    corporate_opacity: 0.68,
    contract_coercion: 0.75,
    community_consent_absence: 0.82,
    legal_protection_gap: 0.78,
    corruption_index: 0.72,
    monoculture_expansion: 0.65,
    biodiversity_loss: 0.72,
    debt_leverage: 0.58,
    export_orientation: 0.62,
    worker_exploitation: 0.68,
    climate_vulnerability: 0.60,
    conflict_intensity: 0.65,
  },
  // LGE-004 — high, climate_migration_land_conflict
  // climate_vulnerability>0.80 AND conflict_intensity>0.75 → climate_migration_land_conflict
  // land_concentration≤0.80 → avoids foreign_sovereign_land_capture
  // monoculture_expansion≤0.80 → avoids corporate_agribusiness_displacement
  // indigenous_rights_violation≤0.80 → avoids indigenous_territory_seizure
  // composite ≈ 52 → high
  {
    id: "LGE-004", land_type: "zones_climatiques", region: "MENA",
    land_concentration: 0.55,
    smallholder_displacement: 0.60,
    indigenous_rights_violation: 0.50,
    food_production_loss: 0.58,
    water_access_loss: 0.65,
    corporate_opacity: 0.48,
    contract_coercion: 0.55,
    community_consent_absence: 0.52,
    legal_protection_gap: 0.58,
    corruption_index: 0.55,
    monoculture_expansion: 0.50,
    biodiversity_loss: 0.55,
    debt_leverage: 0.48,
    export_orientation: 0.52,
    worker_exploitation: 0.50,
    climate_vulnerability: 0.85,
    conflict_intensity: 0.80,
  },
  // LGE-005 — high, green_colonialism_trap
  // debt_leverage>0.80 AND export_orientation>0.75 → green_colonialism_trap
  // land_concentration≤0.80 → avoids foreign_sovereign_land_capture
  // monoculture_expansion≤0.80 → avoids corporate_agribusiness_displacement
  // indigenous_rights_violation≤0.80 → avoids indigenous_territory_seizure
  // climate_vulnerability≤0.80 → avoids climate_migration_land_conflict
  // composite ≈ 48 → high
  {
    id: "LGE-005", land_type: "plantations_export", region: "SEASI",
    land_concentration: 0.60,
    smallholder_displacement: 0.58,
    indigenous_rights_violation: 0.52,
    food_production_loss: 0.55,
    water_access_loss: 0.50,
    corporate_opacity: 0.55,
    contract_coercion: 0.52,
    community_consent_absence: 0.50,
    legal_protection_gap: 0.55,
    corruption_index: 0.58,
    monoculture_expansion: 0.62,
    biodiversity_loss: 0.60,
    debt_leverage: 0.85,
    export_orientation: 0.82,
    worker_exploitation: 0.55,
    climate_vulnerability: 0.48,
    conflict_intensity: 0.45,
  },
  // LGE-006 — moderate, no pattern
  // All values below pattern thresholds → no pattern, composite ≈ 30 → moderate
  {
    id: "LGE-006", land_type: "prairies_communautaires", region: "EMEA",
    land_concentration: 0.30,
    smallholder_displacement: 0.28,
    indigenous_rights_violation: 0.25,
    food_production_loss: 0.32,
    water_access_loss: 0.28,
    corporate_opacity: 0.25,
    contract_coercion: 0.30,
    community_consent_absence: 0.28,
    legal_protection_gap: 0.32,
    corruption_index: 0.30,
    monoculture_expansion: 0.28,
    biodiversity_loss: 0.30,
    debt_leverage: 0.25,
    export_orientation: 0.28,
    worker_exploitation: 0.28,
    climate_vulnerability: 0.30,
    conflict_intensity: 0.25,
  },
  // LGE-007 — low, no pattern
  // All values very low → composite ≈ 10 → low
  {
    id: "LGE-007", land_type: "forêts_protégées", region: "NOAM",
    land_concentration: 0.10,
    smallholder_displacement: 0.08,
    indigenous_rights_violation: 0.10,
    food_production_loss: 0.08,
    water_access_loss: 0.10,
    corporate_opacity: 0.08,
    contract_coercion: 0.10,
    community_consent_absence: 0.08,
    legal_protection_gap: 0.10,
    corruption_index: 0.08,
    monoculture_expansion: 0.10,
    biodiversity_loss: 0.08,
    debt_leverage: 0.10,
    export_orientation: 0.08,
    worker_exploitation: 0.08,
    climate_vulnerability: 0.10,
    conflict_intensity: 0.08,
  },
  // LGE-008 — low, no pattern
  // All values very low → composite ≈ 12 → low
  {
    id: "LGE-008", land_type: "terres_réservées", region: "APAC",
    land_concentration: 0.12,
    smallholder_displacement: 0.10,
    indigenous_rights_violation: 0.12,
    food_production_loss: 0.10,
    water_access_loss: 0.12,
    corporate_opacity: 0.10,
    contract_coercion: 0.12,
    community_consent_absence: 0.10,
    legal_protection_gap: 0.12,
    corruption_index: 0.10,
    monoculture_expansion: 0.12,
    biodiversity_loss: 0.10,
    debt_leverage: 0.12,
    export_orientation: 0.10,
    worker_exploitation: 0.10,
    climate_vulnerability: 0.12,
    conflict_intensity: 0.10,
  },
];

// ─── Math (mirrors Python engine exactly) ─────────────────────────────────────

function dispossessionScore(e: LgeInput): number {
  return Math.round(
    (e.land_concentration * 0.4
      + e.smallholder_displacement * 0.35
      + e.indigenous_rights_violation * 0.25) * 100 * 100) / 100;
}

function foodSovereigntyScore(e: LgeInput): number {
  return Math.round(
    (e.food_production_loss * 0.4
      + e.monoculture_expansion * 0.35
      + e.export_orientation * 0.25) * 100 * 100) / 100;
}

function violenceScore(e: LgeInput): number {
  return Math.round(
    (e.conflict_intensity * 0.4
      + e.contract_coercion * 0.35
      + e.worker_exploitation * 0.25) * 100 * 100) / 100;
}

function governanceScore(e: LgeInput): number {
  return Math.round(
    (e.corruption_index * 0.4
      + e.legal_protection_gap * 0.35
      + e.community_consent_absence * 0.25) * 100 * 100) / 100;
}

function compositeScore(d: number, fs: number, v: number, g: number): number {
  return Math.round((d * 0.30 + fs * 0.25 + v * 0.25 + g * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function landPattern(e: LgeInput): string {
  if (e.land_concentration > 0.80 && e.corporate_opacity > 0.75)
    return "foreign_sovereign_land_capture";
  if (e.monoculture_expansion > 0.80 && e.smallholder_displacement > 0.75)
    return "corporate_agribusiness_displacement";
  if (e.climate_vulnerability > 0.80 && e.conflict_intensity > 0.75)
    return "climate_migration_land_conflict";
  if (e.indigenous_rights_violation > 0.80 && e.community_consent_absence > 0.75)
    return "indigenous_territory_seizure";
  if (e.debt_leverage > 0.80 && e.export_orientation > 0.75)
    return "green_colonialism_trap";
  return "none";
}

function severity(comp: number): string {
  if (comp >= 60) return "crise_accaparement_terres_systémique";
  if (comp >= 40) return "crise_souveraineté_alimentaire_majeure";
  if (comp >= 20) return "dépossession_foncière_structurelle";
  return "pression_foncière_sous_surveillance";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_protection_terres_critiques";
  if (risk === "high")     return "réforme_foncière_accélérée_communautés_vulnérables";
  if (risk === "moderate") return "renforcement_droits_fonciers_souveraineté_alimentaire";
  return "veille_accaparement_terres_continue";
}

function landSignal(risk: string): string {
  if (risk === "critical") return "🔴 Crise accaparement terres systémique — souveraineté alimentaire en péril";
  if (risk === "high")     return "🟠 Crise souveraineté alimentaire majeure détectée";
  if (risk === "moderate") return "🟡 Dépossession foncière structurelle active";
  return "🟢 Pression foncière sous surveillance";
}

function analyzeEntity(e: LgeInput) {
  const d   = dispossessionScore(e);
  const fs  = foodSovereigntyScore(e);
  const v   = violenceScore(e);
  const g   = governanceScore(e);
  const comp = compositeScore(d, fs, v, g);
  const risk  = riskLevel(comp);
  const pat   = landPattern(e);
  const sev   = severity(comp);
  const act   = recommendedAction(risk);
  const sig   = landSignal(risk);

  return {
    id:                e.entity_id,
    land_type:                e.land_type,
    region:                   e.region,
    dispossession_score:      d,
    food_sovereignty_score:   fs,
    violence_score:           v,
    governance_score:         g,
    composite_score:          comp,
    risk_level:               risk,
    land_pattern:             pat,
    severity:                 sev,
    recommended_action:       act,
    signal:                   sig,
    land_concentration:       e.land_concentration,
    smallholder_displacement: e.smallholder_displacement,
  };
}

// ─── GET handler ──────────────────────────────────────────────────────────────

export async function GET() {
  if (!SWARM_API_URL) {
    const allResults = MOCK_ENTITIES.map(analyzeEntity);

    const patternDist:  Record<string, number> = {};
    const riskDist:     Record<string, number> = {};
    const severityDist: Record<string, number> = {};
    const actionDist:   Record<string, number> = {};
    let totalComp = 0, totalDisp = 0, totalFood = 0, totalViol = 0, totalGov = 0;

    for (const r of allResults) {
      patternDist[r.land_pattern]       = (patternDist[r.land_pattern]       || 0) + 1;
      riskDist[r.risk_level]            = (riskDist[r.risk_level]            || 0) + 1;
      severityDist[r.severity]          = (severityDist[r.severity]          || 0) + 1;
      actionDist[r.recommended_action]  = (actionDist[r.recommended_action]  || 0) + 1;
      totalComp += r.composite_score;
      totalDisp += r.dispossession_score;
      totalFood += r.food_sovereignty_score;
      totalViol += r.violence_score;
      totalGov  += r.governance_score;
    }

    const n = allResults.length;
    const avgComposite = Math.round((totalComp / n) * 10) / 10;

    const summary = {
      module_id:                      403,
      module_name:                    "Accaparement Terres & Déplacement Agricole Intelligence Engine",
      total:                          n,
      critical:                       riskDist["critical"]  || 0,
      high:                           riskDist["high"]      || 0,
      moderate:                       riskDist["moderate"]  || 0,
      low:                            riskDist["low"]       || 0,
      avg_composite:                  avgComposite,
      pattern_distribution:           patternDist,
      risk_distribution:              riskDist,
      severity_distribution:          severityDist,
      action_distribution:            actionDist,
      avg_estimated_land_grab_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
      avg_dispossession_score:        Math.round((totalDisp / n) * 10) / 10,
      avg_food_sovereignty_score:     Math.round((totalFood / n) * 10) / 10,
      avg_violence_score:             Math.round((totalViol / n) * 10) / 10,
      avg_governance_score:           Math.round((totalGov  / n) * 10) / 10,
    };

    const entities = allResults;
    return NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>));
  }
  try {
    const url = new URL(`${SWARM_API_URL}/api/land-grab-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
