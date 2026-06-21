import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // FLE-001 — critical, supply_chain_slavery_nexus (opacity>0.80, accountability<0.25)
  {
    id: "FLE-001", labor_sector: "industrie_textile", region: "APAC",
    forced_labor_prevalence: 0.82, debt_bondage_intensity: 0.75,
    document_confiscation: 0.70, movement_restriction: 0.72,
    recruitment_deception: 0.78, wage_theft: 0.80,
    violence_threat: 0.65, detection_effectiveness: 0.18,
    prosecution_rate: 0.12, victim_support_access: 0.10,
    supply_chain_opacity: 0.88, corporate_accountability: 0.12,
    migrant_worker_vulnerability: 0.85, gender_based_exploitation: 0.72,
    child_labor_link: 0.68, corruption_protection: 0.78,
    survivor_compensation: 0.08,
  },
  // FLE-002 — critical, debt_bondage_trap (debt>0.80, deception>0.75)
  {
    id: "FLE-002", labor_sector: "agriculture_intensive", region: "LATAM",
    forced_labor_prevalence: 0.78, debt_bondage_intensity: 0.88,
    document_confiscation: 0.65, movement_restriction: 0.70,
    recruitment_deception: 0.82, wage_theft: 0.75,
    violence_threat: 0.72, detection_effectiveness: 0.15,
    prosecution_rate: 0.10, victim_support_access: 0.12,
    supply_chain_opacity: 0.75, corporate_accountability: 0.18,
    migrant_worker_vulnerability: 0.80, gender_based_exploitation: 0.65,
    child_labor_link: 0.72, corruption_protection: 0.82,
    survivor_compensation: 0.06,
  },
  // FLE-003 — critical, domestic_servitude_network (confiscation>0.80, restriction>0.75)
  {
    id: "FLE-003", labor_sector: "travail_domestique", region: "MEA",
    forced_labor_prevalence: 0.72, debt_bondage_intensity: 0.68,
    document_confiscation: 0.88, movement_restriction: 0.85,
    recruitment_deception: 0.70, wage_theft: 0.78,
    violence_threat: 0.75, detection_effectiveness: 0.12,
    prosecution_rate: 0.08, victim_support_access: 0.08,
    supply_chain_opacity: 0.70, corporate_accountability: 0.10,
    migrant_worker_vulnerability: 0.88, gender_based_exploitation: 0.82,
    child_labor_link: 0.55, corruption_protection: 0.85,
    survivor_compensation: 0.05,
  },
  // FLE-004 — high, sex_trafficking_economy (gender>0.80, violence>0.75) composite ~49
  {
    id: "FLE-004", labor_sector: "exploitation_sexuelle", region: "EMEA",
    forced_labor_prevalence: 0.42, debt_bondage_intensity: 0.38,
    document_confiscation: 0.45, movement_restriction: 0.40,
    recruitment_deception: 0.42, wage_theft: 0.35,
    violence_threat: 0.80, detection_effectiveness: 0.55,
    prosecution_rate: 0.35, victim_support_access: 0.45,
    supply_chain_opacity: 0.40, corporate_accountability: 0.38,
    migrant_worker_vulnerability: 0.50, gender_based_exploitation: 0.85,
    child_labor_link: 0.42, corruption_protection: 0.42,
    survivor_compensation: 0.35,
  },
  // FLE-005 — high, prison_labor_exploitation (corruption>0.75, prevalence>0.70) composite ~50
  {
    id: "FLE-005", labor_sector: "travail_carcéral", region: "NAMER",
    forced_labor_prevalence: 0.72, debt_bondage_intensity: 0.35,
    document_confiscation: 0.42, movement_restriction: 0.65,
    recruitment_deception: 0.30, wage_theft: 0.45,
    violence_threat: 0.38, detection_effectiveness: 0.45,
    prosecution_rate: 0.35, victim_support_access: 0.42,
    supply_chain_opacity: 0.42, corporate_accountability: 0.40,
    migrant_worker_vulnerability: 0.30, gender_based_exploitation: 0.25,
    child_labor_link: 0.15, corruption_protection: 0.78,
    survivor_compensation: 0.30,
  },
  // FLE-006 — moderate, supply_chain_slavery_nexus (opacity>0.80, accountability<0.25) composite ~37
  {
    id: "FLE-006", labor_sector: "extraction_minière", region: "SSA",
    forced_labor_prevalence: 0.22, debt_bondage_intensity: 0.18,
    document_confiscation: 0.20, movement_restriction: 0.22,
    recruitment_deception: 0.25, wage_theft: 0.20,
    violence_threat: 0.18, detection_effectiveness: 0.60,
    prosecution_rate: 0.48, victim_support_access: 0.55,
    supply_chain_opacity: 0.82, corporate_accountability: 0.18,
    migrant_worker_vulnerability: 0.22, gender_based_exploitation: 0.18,
    child_labor_link: 0.20, corruption_protection: 0.28,
    survivor_compensation: 0.28,
  },
  // FLE-007 — low, supply_chain_slavery_nexus
  {
    id: "FLE-007", labor_sector: "manufacturing_certifié", region: "EUROPE",
    forced_labor_prevalence: 0.08, debt_bondage_intensity: 0.05,
    document_confiscation: 0.04, movement_restriction: 0.06,
    recruitment_deception: 0.07, wage_theft: 0.05,
    violence_threat: 0.04, detection_effectiveness: 0.88,
    prosecution_rate: 0.82, victim_support_access: 0.85,
    supply_chain_opacity: 0.12, corporate_accountability: 0.90,
    migrant_worker_vulnerability: 0.10, gender_based_exploitation: 0.08,
    child_labor_link: 0.05, corruption_protection: 0.06,
    survivor_compensation: 0.88,
  },
  // FLE-008 — low, supply_chain_slavery_nexus
  {
    id: "FLE-008", labor_sector: "technologie_responsable", region: "NAMER",
    forced_labor_prevalence: 0.06, debt_bondage_intensity: 0.04,
    document_confiscation: 0.03, movement_restriction: 0.05,
    recruitment_deception: 0.05, wage_theft: 0.04,
    violence_threat: 0.03, detection_effectiveness: 0.92,
    prosecution_rate: 0.88, victim_support_access: 0.90,
    supply_chain_opacity: 0.08, corporate_accountability: 0.92,
    migrant_worker_vulnerability: 0.07, gender_based_exploitation: 0.05,
    child_labor_link: 0.04, corruption_protection: 0.04,
    survivor_compensation: 0.92,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function exploitationScore(e: Entity): number {
  return Math.min(
    Math.round((e.forced_labor_prevalence * 0.4 + e.debt_bondage_intensity * 0.35 + e.wage_theft * 0.25) * 100 * 100) / 100,
    100
  );
}
function detectionScore(e: Entity): number {
  return Math.min(
    Math.round(((1 - e.detection_effectiveness) * 0.4 + e.supply_chain_opacity * 0.35 + (1 - e.victim_support_access) * 0.25) * 100 * 100) / 100,
    100
  );
}
function impunityScore(e: Entity): number {
  return Math.min(
    Math.round(((1 - e.prosecution_rate) * 0.4 + e.corruption_protection * 0.35 + (1 - e.corporate_accountability) * 0.25) * 100 * 100) / 100,
    100
  );
}
function vulnerabilityScore(e: Entity): number {
  return Math.min(
    Math.round((e.migrant_worker_vulnerability * 0.4 + e.gender_based_exploitation * 0.35 + e.child_labor_link * 0.25) * 100 * 100) / 100,
    100
  );
}
function compositeScore(ex: number, det: number, imp: number, vul: number): number {
  return Math.min(Math.round((ex * 0.30 + det * 0.25 + imp * 0.25 + vul * 0.20) * 100) / 100, 100);
}
function laborPattern(e: Entity): string {
  if (e.supply_chain_opacity > 0.80 && e.corporate_accountability < 0.25) return "supply_chain_slavery_nexus";
  if (e.debt_bondage_intensity > 0.80 && e.recruitment_deception > 0.75)  return "debt_bondage_trap";
  if (e.document_confiscation > 0.80 && e.movement_restriction > 0.75)    return "domestic_servitude_network";
  if (e.gender_based_exploitation > 0.80 && e.violence_threat > 0.75)     return "sex_trafficking_economy";
  if (e.corruption_protection > 0.75 && e.forced_labor_prevalence > 0.70) return "prison_labor_exploitation";
  return "supply_chain_slavery_nexus";
}
function riskLevel(c: number): string {
  if (c >= 60) return "critical";
  if (c >= 40) return "high";
  if (c >= 20) return "moderate";
  return "low";
}
function severity(c: number): string {
  if (c >= 60) return "crise_esclavage_moderne_systémique";
  if (c >= 40) return "exploitation_grave_travail_forcé";
  if (c >= 20) return "vulnérabilité_structurelle_travail_forcé";
  return "surveillance_travail_forcé_active";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_esclavage_moderne_critique";
  if (risk === "high")     return "renforcement_protection_victimes_travail_forcé";
  if (risk === "moderate") return "surveillance_renforcée_chaînes_approvisionnement";
  return "veille_travail_forcé_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise esclavage moderne systémique — intervention d'urgence requise";
  if (risk === "high")     return "🟠 Exploitation grave travail forcé détectée";
  if (risk === "moderate") return "🟡 Vulnérabilité structurelle travail forcé active";
  return "🟢 Surveillance travail forcé continue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map((e) => {
      const ex  = exploitationScore(e);
      const det = detectionScore(e);
      const imp = impunityScore(e);
      const vul = vulnerabilityScore(e);
      const comp = compositeScore(ex, det, imp, vul);
      const pat  = laborPattern(e);
      const risk = riskLevel(comp);
      const sev  = severity(comp);
      const act  = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id: e.entity_id,
        labor_sector: e.labor_sector,
        region: e.region,
        exploitation_score: ex,
        detection_score: det,
        impunity_score: imp,
        vulnerability_score: vul,
        composite_score: comp,
        risk_level: risk,
        labor_pattern: pat,
        severity: sev,
        recommended_action: act,
        signal: sig,
        forced_labor_prevalence: e.forced_labor_prevalence,
        migrant_worker_vulnerability: e.migrant_worker_vulnerability,
      };
    });

    const riskDist: Record<string, number>    = {};
    const patternDist: Record<string, number> = {};
    const severityDist: Record<string, number>= {};
    const actionDist: Record<string, number>  = {};
    let totalComposite = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;
    let totalExploitation = 0, totalDetection = 0, totalImpunity = 0, totalVulnerability = 0;

    for (const r of entities) {
      riskDist[r.risk_level]       = (riskDist[r.risk_level]       || 0) + 1;
      patternDist[r.labor_pattern] = (patternDist[r.labor_pattern] || 0) + 1;
      severityDist[r.severity]     = (severityDist[r.severity]     || 0) + 1;
      actionDist[r.recommended_action] = (actionDist[r.recommended_action] || 0) + 1;
      totalComposite    += r.composite_score;
      totalExploitation += r.exploitation_score;
      totalDetection    += r.detection_score;
      totalImpunity     += r.impunity_score;
      totalVulnerability+= r.vulnerability_score;
      if (r.risk_level === "critical")      criticalCount++;
      else if (r.risk_level === "high")     highCount++;
      else if (r.risk_level === "moderate") moderateCount++;
      else                                  lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(totalComposite / n * 10) / 10;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 418,
        module_name: "Travail Forcé & Esclavage Moderne Intelligence Engine",
        total: n,
        critical: criticalCount,
        high: highCount,
        moderate: moderateCount,
        low: lowCount,
        avg_composite: avgComposite,
        pattern_distribution: patternDist,
        risk_distribution: riskDist,
        severity_distribution: severityDist,
        action_distribution: actionDist,
        avg_estimated_forced_labor_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
      },
    } as Record<string, unknown>));
  }

  const upstream = await fetch(`${process.env.SWARM_API_URL}/api/forced-labor-engine`);
  if (!upstream.ok) {
    return NextResponse.json({ error: "Upstream error" }, { status: 502 });
  }
  return NextResponse.json(await upstream.json());
}
