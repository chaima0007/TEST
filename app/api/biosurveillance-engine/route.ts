import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // BSE-001 — critical, outbreak_detection_failure (outbreak_detection_delay>0.85, early_warning_system_weakness>0.80)
  {
    id: "BSE-001", surveillance_system: "détection_épidémique_défaillante", region: "APAC",
    outbreak_detection_delay: 0.90, genomic_sequencing_gap: 0.72, zoonotic_interface_monitoring: 0.68,
    one_health_integration_failure: 0.70, lab_network_capacity: 0.65, data_sharing_obstruction: 0.68,
    early_warning_system_weakness: 0.88, cross_border_surveillance_gap: 0.72, community_level_detection_gap: 0.80,
    mobile_surveillance_coverage: 0.70, veterinary_surveillance_failure: 0.65, environmental_health_monitoring_gap: 0.68,
    WHO_reporting_compliance: 0.65, climate_disease_nexus_monitoring: 0.70, wastewater_surveillance_implementation: 0.72,
    AI_surveillance_deployment: 0.68, political_outbreak_suppression: 0.75,
  },
  // BSE-002 — low, none
  {
    id: "BSE-002", surveillance_system: "surveillance_de_base", region: "NOAM",
    outbreak_detection_delay: 0.08, genomic_sequencing_gap: 0.10, zoonotic_interface_monitoring: 0.08,
    one_health_integration_failure: 0.10, lab_network_capacity: 0.08, data_sharing_obstruction: 0.10,
    early_warning_system_weakness: 0.08, cross_border_surveillance_gap: 0.10, community_level_detection_gap: 0.08,
    mobile_surveillance_coverage: 0.10, veterinary_surveillance_failure: 0.08, environmental_health_monitoring_gap: 0.10,
    WHO_reporting_compliance: 0.08, climate_disease_nexus_monitoring: 0.10, wastewater_surveillance_implementation: 0.08,
    AI_surveillance_deployment: 0.10, political_outbreak_suppression: 0.08,
  },
  // BSE-003 — high, zoonotic_surveillance_gap (zoonotic_interface_monitoring>0.85, veterinary_surveillance_failure>0.80)
  {
    id: "BSE-003", surveillance_system: "interface_zoonotique_critique", region: "EMEA",
    outbreak_detection_delay: 0.50, genomic_sequencing_gap: 0.48, zoonotic_interface_monitoring: 0.88,
    one_health_integration_failure: 0.52, lab_network_capacity: 0.50, data_sharing_obstruction: 0.48,
    early_warning_system_weakness: 0.50, cross_border_surveillance_gap: 0.52, community_level_detection_gap: 0.48,
    mobile_surveillance_coverage: 0.50, veterinary_surveillance_failure: 0.85, environmental_health_monitoring_gap: 0.52,
    WHO_reporting_compliance: 0.48, climate_disease_nexus_monitoring: 0.50, wastewater_surveillance_implementation: 0.48,
    AI_surveillance_deployment: 0.50, political_outbreak_suppression: 0.52,
  },
  // BSE-004 — moderate, none
  {
    id: "BSE-004", surveillance_system: "surveillance_partielle", region: "LATAM",
    outbreak_detection_delay: 0.28, genomic_sequencing_gap: 0.30, zoonotic_interface_monitoring: 0.28,
    one_health_integration_failure: 0.30, lab_network_capacity: 0.28, data_sharing_obstruction: 0.30,
    early_warning_system_weakness: 0.28, cross_border_surveillance_gap: 0.30, community_level_detection_gap: 0.28,
    mobile_surveillance_coverage: 0.30, veterinary_surveillance_failure: 0.28, environmental_health_monitoring_gap: 0.30,
    WHO_reporting_compliance: 0.28, climate_disease_nexus_monitoring: 0.30, wastewater_surveillance_implementation: 0.28,
    AI_surveillance_deployment: 0.30, political_outbreak_suppression: 0.28,
  },
  // BSE-005 — critical, data_sharing_political_suppression (political_outbreak_suppression>0.85, WHO_reporting_compliance>0.80)
  {
    id: "BSE-005", surveillance_system: "suppression_politique_données", region: "MEA",
    outbreak_detection_delay: 0.78, genomic_sequencing_gap: 0.72, zoonotic_interface_monitoring: 0.68,
    one_health_integration_failure: 0.75, lab_network_capacity: 0.70, data_sharing_obstruction: 0.78,
    early_warning_system_weakness: 0.72, cross_border_surveillance_gap: 0.75, community_level_detection_gap: 0.70,
    mobile_surveillance_coverage: 0.68, veterinary_surveillance_failure: 0.65, environmental_health_monitoring_gap: 0.72,
    WHO_reporting_compliance: 0.88, climate_disease_nexus_monitoring: 0.68, wastewater_surveillance_implementation: 0.70,
    AI_surveillance_deployment: 0.65, political_outbreak_suppression: 0.90,
  },
  // BSE-006 — high, genomic_surveillance_collapse (genomic_sequencing_gap>0.80, lab_network_capacity>0.75)
  {
    id: "BSE-006", surveillance_system: "effondrement_génomique", region: "APAC",
    outbreak_detection_delay: 0.50, genomic_sequencing_gap: 0.85, zoonotic_interface_monitoring: 0.48,
    one_health_integration_failure: 0.52, lab_network_capacity: 0.80, data_sharing_obstruction: 0.50,
    early_warning_system_weakness: 0.48, cross_border_surveillance_gap: 0.52, community_level_detection_gap: 0.50,
    mobile_surveillance_coverage: 0.48, veterinary_surveillance_failure: 0.50, environmental_health_monitoring_gap: 0.52,
    WHO_reporting_compliance: 0.50, climate_disease_nexus_monitoring: 0.48, wastewater_surveillance_implementation: 0.50,
    AI_surveillance_deployment: 0.48, political_outbreak_suppression: 0.50,
  },
  // BSE-007 — critical, cross_border_surveillance_failure (cross_border_surveillance_gap>0.80, data_sharing_obstruction>0.75)
  {
    id: "BSE-007", surveillance_system: "défaillance_transfrontalière", region: "EMEA",
    outbreak_detection_delay: 0.78, genomic_sequencing_gap: 0.75, zoonotic_interface_monitoring: 0.72,
    one_health_integration_failure: 0.78, lab_network_capacity: 0.70, data_sharing_obstruction: 0.82,
    early_warning_system_weakness: 0.75, cross_border_surveillance_gap: 0.88, community_level_detection_gap: 0.72,
    mobile_surveillance_coverage: 0.68, veterinary_surveillance_failure: 0.70, environmental_health_monitoring_gap: 0.75,
    WHO_reporting_compliance: 0.72, climate_disease_nexus_monitoring: 0.70, wastewater_surveillance_implementation: 0.68,
    AI_surveillance_deployment: 0.65, political_outbreak_suppression: 0.72,
  },
  // BSE-008 — high, none
  {
    id: "BSE-008", surveillance_system: "surveillance_fragile", region: "NOAM",
    outbreak_detection_delay: 0.52, genomic_sequencing_gap: 0.50, zoonotic_interface_monitoring: 0.48,
    one_health_integration_failure: 0.52, lab_network_capacity: 0.50, data_sharing_obstruction: 0.48,
    early_warning_system_weakness: 0.52, cross_border_surveillance_gap: 0.50, community_level_detection_gap: 0.52,
    mobile_surveillance_coverage: 0.48, veterinary_surveillance_failure: 0.50, environmental_health_monitoring_gap: 0.52,
    WHO_reporting_compliance: 0.50, climate_disease_nexus_monitoring: 0.52, wastewater_surveillance_implementation: 0.50,
    AI_surveillance_deployment: 0.48, political_outbreak_suppression: 0.50,
  },
];

type BSEInput = typeof MOCK_ENTITIES[0];

function detectionScore(e: BSEInput): number {
  return Math.round((e.outbreak_detection_delay * 0.40 + e.early_warning_system_weakness * 0.35 + e.community_level_detection_gap * 0.25) * 100 * 100) / 100;
}
function responseScore(e: BSEInput): number {
  return Math.round((e.cross_border_surveillance_gap * 0.40 + e.lab_network_capacity * 0.35 + e.mobile_surveillance_coverage * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: BSEInput): number {
  return Math.round((e.WHO_reporting_compliance * 0.40 + e.data_sharing_obstruction * 0.35 + e.political_outbreak_suppression * 0.25) * 100 * 100) / 100;
}
function systemicScore(e: BSEInput): number {
  return Math.round((e.one_health_integration_failure * 0.40 + e.zoonotic_interface_monitoring * 0.35 + e.genomic_sequencing_gap * 0.25) * 100 * 100) / 100;
}
function compositeScore(det: number, res: number, gov: number, sys: number): number {
  return Math.round((det * 0.30 + res * 0.25 + gov * 0.25 + sys * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function biosurveillancePattern(e: BSEInput): string {
  if (e.outbreak_detection_delay > 0.85 && e.early_warning_system_weakness > 0.80) return "outbreak_detection_failure";
  if (e.political_outbreak_suppression > 0.85 && e.WHO_reporting_compliance > 0.80) return "data_sharing_political_suppression";
  if (e.zoonotic_interface_monitoring > 0.85 && e.veterinary_surveillance_failure > 0.80) return "zoonotic_surveillance_gap";
  if (e.genomic_sequencing_gap > 0.80 && e.lab_network_capacity > 0.75) return "genomic_surveillance_collapse";
  if (e.cross_border_surveillance_gap > 0.80 && e.data_sharing_obstruction > 0.75) return "cross_border_surveillance_failure";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "effondrement_biosurveillance_systémique";
  if (composite >= 40) return "crise_alerte_précoce_épidémique_majeure";
  if (composite >= 20) return "défaillance_biosurveillance_structurelle";
  return "biosurveillance_sous_contrôle";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_biosurveillance_urgence_mondiale";
  if (risk === "high") return "renforcement_alerte_précoce_urgence";
  if (risk === "moderate") return "amélioration_surveillance_épidémique_systémique";
  return "veille_biosurveillance_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Effondrement biosurveillance — alerte épidémique critique";
  if (risk === "high") return "🟠 Crise alerte précoce épidémique majeure détectée";
  if (risk === "moderate") return "🟡 Défaillance biosurveillance structurelle active";
  return "🟢 Biosurveillance sous contrôle et contenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[biosurveillance-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.biosurveillance_pattern] = (pattern_distribution[ent.biosurveillance_pattern] || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                           391,
      module_name:                         "Biosurveillance & Epidemic Early Warning Intelligence Engine",
      total:                               n,
      critical:                            criticalCount,
      high:                                highCount,
      moderate:                            moderateCount,
      low:                                 lowCount,
      avg_composite:                       avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_biosurveillance_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "biosurveillance-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/biosurveillance-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json(), "biosurveillance-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "biosurveillance-engine"),
      { status: 502 }
    ));
  }
}
