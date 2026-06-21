import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // CSE-001 — Tech_Corp, USA → critical, total_employee_surveillance
  // total_employee_surveillance: employee_monitoring_intensity>0.85 AND biometric_workplace_data>0.80
  // composite >=60 → critical
  {
    id: "CSE-001", industry_type: "Tech_Corp", region: "USA",
    employee_monitoring_intensity: 0.92,
    productivity_scoring_opacity: 0.78,
    biometric_workplace_data: 0.88,
    algorithmic_management_control: 0.82,
    consumer_behavior_extraction: 0.85,
    location_tracking_scope: 0.80,
    emotion_recognition_deployment: 0.75,
    keystroke_surveillance: 0.88,
    performance_anxiety_induction: 0.82,
    union_busting_surveillance: 0.70,
    consumer_manipulation_depth: 0.78,
    health_data_employer_access: 0.72,
    housing_tenant_surveillance: 0.60,
    gig_worker_score_opacity: 0.68,
    data_broker_corporate_integration: 0.80,
    regulatory_capture_privacy: 0.75,
    psychological_profiling_depth: 0.78,
  },
  // CSE-002 — Logistics, EU → low, none
  // composite < 20 → low; no pattern triggers
  {
    id: "CSE-002", industry_type: "Logistics", region: "EU",
    employee_monitoring_intensity: 0.12,
    productivity_scoring_opacity: 0.15,
    biometric_workplace_data: 0.10,
    algorithmic_management_control: 0.14,
    consumer_behavior_extraction: 0.12,
    location_tracking_scope: 0.10,
    emotion_recognition_deployment: 0.08,
    keystroke_surveillance: 0.11,
    performance_anxiety_induction: 0.13,
    union_busting_surveillance: 0.10,
    consumer_manipulation_depth: 0.12,
    health_data_employer_access: 0.10,
    housing_tenant_surveillance: 0.08,
    gig_worker_score_opacity: 0.11,
    data_broker_corporate_integration: 0.13,
    regulatory_capture_privacy: 0.10,
    psychological_profiling_depth: 0.12,
  },
  // CSE-003 — Warehouse_Ops, UK → critical, algorithmic_management_tyranny
  // algorithmic_management_tyranny: algorithmic_management_control>0.85 AND productivity_scoring_opacity>0.80
  // employee_monitoring_intensity<=0.85 to avoid total_employee_surveillance
  // composite >=60 → critical
  {
    id: "CSE-003", industry_type: "Warehouse_Ops", region: "UK",
    employee_monitoring_intensity: 0.80,
    productivity_scoring_opacity: 0.88,
    biometric_workplace_data: 0.72,
    algorithmic_management_control: 0.92,
    consumer_behavior_extraction: 0.82,
    location_tracking_scope: 0.78,
    emotion_recognition_deployment: 0.70,
    keystroke_surveillance: 0.82,
    performance_anxiety_induction: 0.88,
    union_busting_surveillance: 0.72,
    consumer_manipulation_depth: 0.75,
    health_data_employer_access: 0.68,
    housing_tenant_surveillance: 0.60,
    gig_worker_score_opacity: 0.65,
    data_broker_corporate_integration: 0.78,
    regulatory_capture_privacy: 0.80,
    psychological_profiling_depth: 0.72,
  },
  // CSE-004 — Retail, Canada → low, none
  // composite < 20 → low; no pattern triggers
  {
    id: "CSE-004", industry_type: "Retail", region: "Canada",
    employee_monitoring_intensity: 0.15,
    productivity_scoring_opacity: 0.18,
    biometric_workplace_data: 0.12,
    algorithmic_management_control: 0.14,
    consumer_behavior_extraction: 0.16,
    location_tracking_scope: 0.13,
    emotion_recognition_deployment: 0.10,
    keystroke_surveillance: 0.14,
    performance_anxiety_induction: 0.16,
    union_busting_surveillance: 0.12,
    consumer_manipulation_depth: 0.15,
    health_data_employer_access: 0.13,
    housing_tenant_surveillance: 0.10,
    gig_worker_score_opacity: 0.14,
    data_broker_corporate_integration: 0.16,
    regulatory_capture_privacy: 0.12,
    psychological_profiling_depth: 0.15,
  },
  // CSE-005 — AdTech_Platform, USA → critical, consumer_manipulation_empire
  // consumer_manipulation_empire: consumer_manipulation_depth>0.85 AND psychological_profiling_depth>0.80
  // employee_monitoring_intensity<=0.85 and algorithmic_management_control<=0.85 to avoid prior patterns
  // composite >=60 → critical
  {
    id: "CSE-005", industry_type: "AdTech_Platform", region: "USA",
    employee_monitoring_intensity: 0.78,
    productivity_scoring_opacity: 0.70,
    biometric_workplace_data: 0.72,
    algorithmic_management_control: 0.80,
    consumer_behavior_extraction: 0.88,
    location_tracking_scope: 0.82,
    emotion_recognition_deployment: 0.80,
    keystroke_surveillance: 0.75,
    performance_anxiety_induction: 0.78,
    union_busting_surveillance: 0.70,
    consumer_manipulation_depth: 0.92,
    health_data_employer_access: 0.72,
    housing_tenant_surveillance: 0.65,
    gig_worker_score_opacity: 0.68,
    data_broker_corporate_integration: 0.85,
    regulatory_capture_privacy: 0.78,
    psychological_profiling_depth: 0.88,
  },
  // CSE-006 — Gig_Economy, Germany → high, gig_worker_score_oppression
  // gig_worker_score_oppression: gig_worker_score_opacity>0.80 AND union_busting_surveillance>0.75
  // no prior patterns must trigger
  // composite >=40 and <60 → high
  {
    id: "CSE-006", industry_type: "Gig_Economy", region: "Germany",
    employee_monitoring_intensity: 0.45,
    productivity_scoring_opacity: 0.50,
    biometric_workplace_data: 0.40,
    algorithmic_management_control: 0.55,
    consumer_behavior_extraction: 0.48,
    location_tracking_scope: 0.50,
    emotion_recognition_deployment: 0.40,
    keystroke_surveillance: 0.45,
    performance_anxiety_induction: 0.52,
    union_busting_surveillance: 0.76,
    consumer_manipulation_depth: 0.42,
    health_data_employer_access: 0.45,
    housing_tenant_surveillance: 0.40,
    gig_worker_score_opacity: 0.82,
    data_broker_corporate_integration: 0.50,
    regulatory_capture_privacy: 0.48,
    psychological_profiling_depth: 0.42,
  },
  // CSE-007 — HealthInsurance, France → high, health_housing_surveillance_fusion
  // health_housing_surveillance_fusion: health_data_employer_access>0.80 AND housing_tenant_surveillance>0.75
  // no prior patterns must trigger
  // composite >=40 and <60 → high
  {
    id: "CSE-007", industry_type: "HealthInsurance", region: "France",
    employee_monitoring_intensity: 0.42,
    productivity_scoring_opacity: 0.48,
    biometric_workplace_data: 0.38,
    algorithmic_management_control: 0.50,
    consumer_behavior_extraction: 0.45,
    location_tracking_scope: 0.48,
    emotion_recognition_deployment: 0.38,
    keystroke_surveillance: 0.42,
    performance_anxiety_induction: 0.48,
    union_busting_surveillance: 0.52,
    consumer_manipulation_depth: 0.45,
    health_data_employer_access: 0.82,
    housing_tenant_surveillance: 0.76,
    gig_worker_score_opacity: 0.48,
    data_broker_corporate_integration: 0.52,
    regulatory_capture_privacy: 0.50,
    psychological_profiling_depth: 0.45,
  },
  // CSE-008 — Finance_Corp, Global → moderate, none
  // composite >=20 and <40 → moderate; no pattern triggers
  {
    id: "CSE-008", industry_type: "Finance_Corp", region: "Global",
    employee_monitoring_intensity: 0.35,
    productivity_scoring_opacity: 0.38,
    biometric_workplace_data: 0.30,
    algorithmic_management_control: 0.35,
    consumer_behavior_extraction: 0.38,
    location_tracking_scope: 0.32,
    emotion_recognition_deployment: 0.28,
    keystroke_surveillance: 0.35,
    performance_anxiety_induction: 0.38,
    union_busting_surveillance: 0.32,
    consumer_manipulation_depth: 0.35,
    health_data_employer_access: 0.30,
    housing_tenant_surveillance: 0.28,
    gig_worker_score_opacity: 0.35,
    data_broker_corporate_integration: 0.38,
    regulatory_capture_privacy: 0.32,
    psychological_profiling_depth: 0.35,
  },
];

type Entity = (typeof MOCK_ENTITIES)[0];

function monitoringScore(e: Entity): number {
  const raw = (
    e.employee_monitoring_intensity * 0.4 +
    e.keystroke_surveillance * 0.35 +
    e.biometric_workplace_data * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function manipulationScore(e: Entity): number {
  const raw = (
    e.consumer_manipulation_depth * 0.4 +
    e.psychological_profiling_depth * 0.35 +
    e.performance_anxiety_induction * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function extractionScore(e: Entity): number {
  const raw = (
    e.consumer_behavior_extraction * 0.4 +
    e.data_broker_corporate_integration * 0.35 +
    e.location_tracking_scope * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function controlScore(e: Entity): number {
  const raw = (
    e.algorithmic_management_control * 0.4 +
    e.regulatory_capture_privacy * 0.35 +
    e.union_busting_surveillance * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(mon: number, man: number, ext: number, ctrl: number): number {
  return Math.round((mon * 0.30 + man * 0.25 + ext * 0.25 + ctrl * 0.20) * 100) / 100;
}

function surveillancePattern(e: Entity): string {
  if (e.employee_monitoring_intensity > 0.85 && e.biometric_workplace_data > 0.80)
    return "total_employee_surveillance";
  if (e.algorithmic_management_control > 0.85 && e.productivity_scoring_opacity > 0.80)
    return "algorithmic_management_tyranny";
  if (e.consumer_manipulation_depth > 0.85 && e.psychological_profiling_depth > 0.80)
    return "consumer_manipulation_empire";
  if (e.gig_worker_score_opacity > 0.80 && e.union_busting_surveillance > 0.75)
    return "gig_worker_score_oppression";
  if (e.health_data_employer_access > 0.80 && e.housing_tenant_surveillance > 0.75)
    return "health_housing_surveillance_fusion";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(risk: string): string {
  if (risk === "critical") return "surveillance_corporative_totale";
  if (risk === "high") return "controle_employes_massif";
  if (risk === "moderate") return "surveillance_structurelle_active";
  return "surveillance_contenue";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "regulation_surveillance_employes_urgente";
  if (risk === "high") return "demantelement_controle_algorithmique";
  if (risk === "moderate") return "renforcement_droits_travailleurs";
  return "veille_surveillance_corporative";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Surveillance corporative totale — contrôle employés systémique";
  if (risk === "high") return "🟠 Contrôle des employés massif détecté";
  if (risk === "moderate") return "🟡 Surveillance structurelle active des employés";
  return "🟢 Surveillance corporative contenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const mon  = monitoringScore(e);
      const man  = manipulationScore(e);
      const ext  = extractionScore(e);
      const ctrl = controlScore(e);
      const comp = compositeScore(mon, man, ext, ctrl);
      const pat  = surveillancePattern(e);
      const risk = riskLevel(comp);
      const sev  = severity(risk);
      const act  = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                      e.entity_id,
        industry_type:                  e.industry_type,
        region:                         e.region,
        monitoring_score:               mon,
        manipulation_score:             man,
        extraction_score:               ext,
        control_score:                  ctrl,
        composite_score:                comp,
        risk_level:                     risk,
        surveillance_pattern:           pat,
        severity:                       sev,
        recommended_action:             act,
        signal:                         sig,
        employee_monitoring_intensity:  e.employee_monitoring_intensity,
        biometric_workplace_data:       e.biometric_workplace_data,
      };
    });

    const patternDist:  Record<string, number> = {};
    const riskDist:     Record<string, number> = {};
    const severityDist: Record<string, number> = {};
    const actionDist:   Record<string, number> = {};
    let totalComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      patternDist[ent.surveillance_pattern]  = (patternDist[ent.surveillance_pattern]  || 0) + 1;
      riskDist[ent.risk_level]               = (riskDist[ent.risk_level]               || 0) + 1;
      severityDist[ent.severity]             = (severityDist[ent.severity]             || 0) + 1;
      actionDist[ent.recommended_action]     = (actionDist[ent.recommended_action]     || 0) + 1;
      totalComp += ent.composite_score;
      if (ent.risk_level === "critical") criticalCount++;
      else if (ent.risk_level === "high") highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(totalComp / n * 100) / 100;
    const summary = {
      module_id:                                   381,
      module_name:                                 "Corporate Surveillance & Employee Monitoring Intelligence Engine",
      total:                                       n,
      critical:                                    criticalCount,
      high:                                        highCount,
      moderate:                                    moderateCount,
      low:                                         lowCount,
      avg_composite:                               avgComposite,
      pattern_distribution:                        patternDist,
      risk_distribution:                           riskDist,
      severity_distribution:                       severityDist,
      action_distribution:                         actionDist,
      avg_estimated_corporate_surveillance_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "corporate-surveillance-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/corporate-surveillance-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "corporate-surveillance-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream corporate surveillance engine unavailable" }, "corporate-surveillance-engine"),
      { status: 502 }
    );
  }
}
