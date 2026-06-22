import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[migration-crisis-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Types ────────────────────────────────────────────────────────────────────

interface McrInput {
  id: string;
  migration_corridor: string;
  region: string;
  forced_displacement_rate: number;
  climate_migration_acceleration: number;
  economic_migration_pressure: number;
  border_violence_index: number;
  asylum_system_saturation: number;
  integration_failure_rate: number;
  xenophobia_political_exploitation: number;
  demographic_aging_severity: number;
  brain_drain_intensity: number;
  stateless_population_growth: number;
  migration_route_lethality: number;
  remittance_dependency_fragility: number;
  migration_policy_collapse: number;
  diaspora_radicalisation_risk: number;
  demographic_dividend_loss: number;
  host_society_social_cohesion_erosion: number;
  labor_market_displacement_cascade: number;
}

// ─── Math (mirrors Python exactly) ───────────────────────────────────────────

function displacementScore(e: McrInput): number {
  return Math.round((e.forced_displacement_rate * 0.4 + e.climate_migration_acceleration * 0.35 + e.migration_route_lethality * 0.25) * 100 * 100) / 100;
}

function receptionScore(e: McrInput): number {
  return Math.round((e.asylum_system_saturation * 0.4 + e.integration_failure_rate * 0.35 + e.migration_policy_collapse * 0.25) * 100 * 100) / 100;
}

function socialScore(e: McrInput): number {
  return Math.round((e.xenophobia_political_exploitation * 0.4 + e.host_society_social_cohesion_erosion * 0.35 + e.diaspora_radicalisation_risk * 0.25) * 100 * 100) / 100;
}

function demographicScore(e: McrInput): number {
  return Math.round((e.demographic_aging_severity * 0.4 + e.brain_drain_intensity * 0.35 + e.demographic_dividend_loss * 0.25) * 100 * 100) / 100;
}

function composite(d: number, r: number, s: number, dem: number): number {
  return Math.round((d * 0.30 + r * 0.25 + s * 0.25 + dem * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function migrationPattern(e: McrInput): string {
  if (e.forced_displacement_rate >= 0.70 && e.migration_route_lethality >= 0.65) return "mass_displacement_crisis";
  if (e.asylum_system_saturation >= 0.70 && e.migration_policy_collapse >= 0.65) return "asylum_system_collapse";
  if (e.climate_migration_acceleration >= 0.70 && e.economic_migration_pressure >= 0.65) return "climate_exodus";
  if (e.xenophobia_political_exploitation >= 0.70 && e.host_society_social_cohesion_erosion >= 0.65) return "xenophobia_cascade";
  if (e.demographic_aging_severity >= 0.70 && e.brain_drain_intensity >= 0.65) return "demographic_implosion";
  return "none";
}

function severity(comp: number): string {
  if (comp >= 60) return "crise_migratoire_systémique";
  if (comp >= 40) return "choc_démographique_majeur";
  if (comp >= 20) return "pression_migratoire_structurelle";
  return "migration_gérée";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_humanitaire_urgente";
  if (risk === "high") return "réforme_système_asile_accélérée";
  if (risk === "moderate") return "renforcement_intégration_systémique";
  return "veille_démographique_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise migratoire systémique — choc humanitaire extrême";
  if (risk === "high") return "🟠 Choc démographique majeur détecté";
  if (risk === "moderate") return "🟡 Pression migratoire structurelle active";
  return "🟢 Flux migratoires relativement gérés";
}

function analyzeEntity(e: McrInput) {
  const d   = displacementScore(e);
  const r   = receptionScore(e);
  const s   = socialScore(e);
  const dem = demographicScore(e);
  const comp = composite(d, r, s, dem);
  const risk = riskLevel(comp);
  const pat  = migrationPattern(e);
  const sev  = severity(comp);
  const action = recommendedAction(risk);
  const sig  = signal(risk);

  return {
    id: e.entity_id,
    migration_corridor: e.migration_corridor,
    region: e.region,
    displacement_score: d,
    reception_score: r,
    social_score: s,
    demographic_score: dem,
    composite_score: comp,
    risk_level: risk,
    migration_pattern: pat,
    severity: sev,
    recommended_action: action,
    signal: sig,
    forced_displacement_rate: e.forced_displacement_rate,
    climate_migration_acceleration: e.climate_migration_acceleration,
  };
}

// ─── Mock entities (8 total — all 5 patterns, all 4 risk levels) ──────────────

const mockEntities: McrInput[] = [
  {
    // MCR-001: critical / mass_displacement_crisis
    id: "MCR-001", migration_corridor: "Syria-Turkey-EU", region: "EMEA",
    forced_displacement_rate: 0.88, climate_migration_acceleration: 0.70, economic_migration_pressure: 0.75,
    border_violence_index: 0.80, asylum_system_saturation: 0.82, integration_failure_rate: 0.78,
    xenophobia_political_exploitation: 0.85, demographic_aging_severity: 0.40, brain_drain_intensity: 0.45,
    stateless_population_growth: 0.72, migration_route_lethality: 0.75, remittance_dependency_fragility: 0.60,
    migration_policy_collapse: 0.80, diaspora_radicalisation_risk: 0.65, demographic_dividend_loss: 0.50,
    host_society_social_cohesion_erosion: 0.72, labor_market_displacement_cascade: 0.68,
  },
  {
    // MCR-002: low / none
    id: "MCR-002", migration_corridor: "Canada-US", region: "NOAM",
    forced_displacement_rate: 0.10, climate_migration_acceleration: 0.12, economic_migration_pressure: 0.10,
    border_violence_index: 0.08, asylum_system_saturation: 0.12, integration_failure_rate: 0.10,
    xenophobia_political_exploitation: 0.10, demographic_aging_severity: 0.15, brain_drain_intensity: 0.10,
    stateless_population_growth: 0.05, migration_route_lethality: 0.08, remittance_dependency_fragility: 0.10,
    migration_policy_collapse: 0.08, diaspora_radicalisation_risk: 0.10, demographic_dividend_loss: 0.12,
    host_society_social_cohesion_erosion: 0.10, labor_market_displacement_cascade: 0.08,
  },
  {
    // MCR-003: high / asylum_system_collapse
    id: "MCR-003", migration_corridor: "Afghanistan-Pakistan-EU", region: "APAC",
    forced_displacement_rate: 0.55, climate_migration_acceleration: 0.48, economic_migration_pressure: 0.52,
    border_violence_index: 0.60, asylum_system_saturation: 0.78, integration_failure_rate: 0.62,
    xenophobia_political_exploitation: 0.58, demographic_aging_severity: 0.42, brain_drain_intensity: 0.50,
    stateless_population_growth: 0.55, migration_route_lethality: 0.50, remittance_dependency_fragility: 0.45,
    migration_policy_collapse: 0.72, diaspora_radicalisation_risk: 0.48, demographic_dividend_loss: 0.40,
    host_society_social_cohesion_erosion: 0.50, labor_market_displacement_cascade: 0.48,
  },
  {
    // MCR-004: low / none
    id: "MCR-004", migration_corridor: "Australia-NZ", region: "APAC",
    forced_displacement_rate: 0.08, climate_migration_acceleration: 0.10, economic_migration_pressure: 0.12,
    border_violence_index: 0.05, asylum_system_saturation: 0.10, integration_failure_rate: 0.08,
    xenophobia_political_exploitation: 0.08, demographic_aging_severity: 0.12, brain_drain_intensity: 0.08,
    stateless_population_growth: 0.05, migration_route_lethality: 0.06, remittance_dependency_fragility: 0.08,
    migration_policy_collapse: 0.06, diaspora_radicalisation_risk: 0.08, demographic_dividend_loss: 0.10,
    host_society_social_cohesion_erosion: 0.08, labor_market_displacement_cascade: 0.06,
  },
  {
    // MCR-005: critical / climate_exodus
    // forced_displacement_rate<0.70 ensures mass_displacement_crisis is NOT triggered first
    id: "MCR-005", migration_corridor: "Sahel-Libya-Mediterranean", region: "MEA",
    forced_displacement_rate: 0.60, climate_migration_acceleration: 0.82, economic_migration_pressure: 0.78,
    border_violence_index: 0.70, asylum_system_saturation: 0.60, integration_failure_rate: 0.70,
    xenophobia_political_exploitation: 0.72, demographic_aging_severity: 0.35, brain_drain_intensity: 0.40,
    stateless_population_growth: 0.65, migration_route_lethality: 0.50, remittance_dependency_fragility: 0.72,
    migration_policy_collapse: 0.68, diaspora_radicalisation_risk: 0.60, demographic_dividend_loss: 0.55,
    host_society_social_cohesion_erosion: 0.65, labor_market_displacement_cascade: 0.70,
  },
  {
    // MCR-006: moderate / none
    id: "MCR-006", migration_corridor: "Mexico-US", region: "NOAM",
    forced_displacement_rate: 0.32, climate_migration_acceleration: 0.28, economic_migration_pressure: 0.38,
    border_violence_index: 0.35, asylum_system_saturation: 0.30, integration_failure_rate: 0.28,
    xenophobia_political_exploitation: 0.30, demographic_aging_severity: 0.22, brain_drain_intensity: 0.28,
    stateless_population_growth: 0.20, migration_route_lethality: 0.25, remittance_dependency_fragility: 0.35,
    migration_policy_collapse: 0.28, diaspora_radicalisation_risk: 0.22, demographic_dividend_loss: 0.25,
    host_society_social_cohesion_erosion: 0.28, labor_market_displacement_cascade: 0.30,
  },
  {
    // MCR-007: high / xenophobia_cascade
    // forced_displacement_rate<0.70, asylum_system_saturation<0.70, climate_migration_acceleration<0.70 to avoid prior patterns
    id: "MCR-007", migration_corridor: "Bangladesh-India-EU", region: "APAC",
    forced_displacement_rate: 0.50, climate_migration_acceleration: 0.48, economic_migration_pressure: 0.52,
    border_violence_index: 0.55, asylum_system_saturation: 0.55, integration_failure_rate: 0.58,
    xenophobia_political_exploitation: 0.78, demographic_aging_severity: 0.45, brain_drain_intensity: 0.48,
    stateless_population_growth: 0.50, migration_route_lethality: 0.42, remittance_dependency_fragility: 0.48,
    migration_policy_collapse: 0.52, diaspora_radicalisation_risk: 0.55, demographic_dividend_loss: 0.45,
    host_society_social_cohesion_erosion: 0.72, labor_market_displacement_cascade: 0.55,
  },
  {
    // MCR-008: critical / demographic_implosion
    // forced_displacement_rate<0.70, asylum_system_saturation<0.70, climate_migration_acceleration<0.70,
    // xenophobia_political_exploitation<0.70 — ensuring demographic_implosion fires
    id: "MCR-008", migration_corridor: "Eastern-Europe-West", region: "EMEA",
    forced_displacement_rate: 0.55, climate_migration_acceleration: 0.50, economic_migration_pressure: 0.65,
    border_violence_index: 0.55, asylum_system_saturation: 0.60, integration_failure_rate: 0.72,
    xenophobia_political_exploitation: 0.65, demographic_aging_severity: 0.80, brain_drain_intensity: 0.75,
    stateless_population_growth: 0.60, migration_route_lethality: 0.50, remittance_dependency_fragility: 0.55,
    migration_policy_collapse: 0.60, diaspora_radicalisation_risk: 0.58, demographic_dividend_loss: 0.72,
    host_society_social_cohesion_erosion: 0.62, labor_market_displacement_cascade: 0.68,
  },
];

// ─── Route handler ────────────────────────────────────────────────────────────

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!SWARM_API_URL) {
    const allResults = mockEntities.map(analyzeEntity);
    let entities = [...allResults];
    if (risk)    entities = entities.filter((e) => e.risk_level === risk);
    if (pattern) entities = entities.filter((e) => e.migration_pattern === pattern);

    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_comp = 0, total_disp = 0, total_rec = 0, total_soc = 0, total_dem = 0;
    let critical_count = 0, high_count = 0, moderate_count = 0, low_count = 0;

    for (const r of allResults) {
      risk_distribution[r.risk_level]           = (risk_distribution[r.risk_level] || 0) + 1;
      pattern_distribution[r.migration_pattern] = (pattern_distribution[r.migration_pattern] || 0) + 1;
      severity_distribution[r.severity]         = (severity_distribution[r.severity] || 0) + 1;
      action_distribution[r.recommended_action] = (action_distribution[r.recommended_action] || 0) + 1;
      total_comp += r.composite_score;
      total_disp += r.displacement_score;
      total_rec  += r.reception_score;
      total_soc  += r.social_score;
      total_dem  += r.demographic_score;
      if (r.risk_level === "critical") critical_count++;
      else if (r.risk_level === "high") high_count++;
      else if (r.risk_level === "moderate") moderate_count++;
      else low_count++;
    }

    const n = allResults.length;
    const avg_composite = Math.round((total_comp / n) * 10) / 10;

    return sealResponse(NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 338,
        module_name: "Migration Crisis & Demographic Shock Intelligence Engine",
        total_entities: n,
        critical_count,
        high_count,
        moderate_count,
        low_count,
        avg_composite,
        pattern_distribution,
        risk_distribution,
        severity_distribution,
        action_distribution,
        avg_estimated_migration_crisis_index: Math.round((avg_composite / 100 * 10) * 100) / 100,
      },
    } as Record<string, unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/migration-crisis-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json() as Record<string, unknown>)));
  } catch {}

  return sealResponse(NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 }));
}
