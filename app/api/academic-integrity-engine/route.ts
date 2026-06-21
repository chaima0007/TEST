import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // AIE-001 — critical, data_fabrication_fraud_ring (data_fab>0.85, retraction>0.80)
  {
    id: "AIE-001", research_field: "sciences_biomédicales", region: "APAC",
    retraction_rate: 0.88, data_fabrication_index: 0.90,
    plagiarism_detection_gap: 0.75, predatory_journal_prevalence: 0.70,
    paper_mill_activity: 0.68, peer_review_quality: 0.80,
    open_access_integrity: 0.30, replication_success_rate: 0.72,
    statistical_manipulation: 0.85, conflicts_of_interest: 0.78,
    industry_funding_bias: 0.80, ai_generated_content_rate: 0.65,
    preprint_misinformation: 0.70, institutional_misconduct_response: 0.82,
    whistleblower_protection: 0.20, reproducibility_infrastructure: 0.22,
    research_fraud_prosecution: 0.18,
  },
  // AIE-002 — critical, predatory_publishing_ecosystem (predatory>0.85, paper_mill>0.80)
  {
    id: "AIE-002", research_field: "sciences_sociales", region: "AFRIQUE_SUBSAHARIENNE",
    retraction_rate: 0.72, data_fabrication_index: 0.68,
    plagiarism_detection_gap: 0.78, predatory_journal_prevalence: 0.90,
    paper_mill_activity: 0.85, peer_review_quality: 0.82,
    open_access_integrity: 0.25, replication_success_rate: 0.70,
    statistical_manipulation: 0.65, conflicts_of_interest: 0.72,
    industry_funding_bias: 0.70, ai_generated_content_rate: 0.68,
    preprint_misinformation: 0.72, institutional_misconduct_response: 0.80,
    whistleblower_protection: 0.18, reproducibility_infrastructure: 0.20,
    research_fraud_prosecution: 0.15,
  },
  // AIE-003 — critical, peer_review_capture (peer_review>0.80, conflicts>0.75)
  {
    id: "AIE-003", research_field: "pharmacologie_clinique", region: "NOAM",
    retraction_rate: 0.70, data_fabrication_index: 0.72,
    plagiarism_detection_gap: 0.68, predatory_journal_prevalence: 0.65,
    paper_mill_activity: 0.62, peer_review_quality: 0.88,
    open_access_integrity: 0.28, replication_success_rate: 0.75,
    statistical_manipulation: 0.70, conflicts_of_interest: 0.85,
    industry_funding_bias: 0.88, ai_generated_content_rate: 0.60,
    preprint_misinformation: 0.65, institutional_misconduct_response: 0.85,
    whistleblower_protection: 0.15, reproducibility_infrastructure: 0.18,
    research_fraud_prosecution: 0.12,
  },
  // AIE-004 — high, replication_crisis_collapse (replication>0.85, preprint_mis>0.80)
  {
    id: "AIE-004", research_field: "psychologie_expérimentale", region: "EMEA",
    retraction_rate: 0.50, data_fabrication_index: 0.48,
    plagiarism_detection_gap: 0.52, predatory_journal_prevalence: 0.45,
    paper_mill_activity: 0.48, peer_review_quality: 0.50,
    open_access_integrity: 0.45, replication_success_rate: 0.88,
    statistical_manipulation: 0.50, conflicts_of_interest: 0.48,
    industry_funding_bias: 0.50, ai_generated_content_rate: 0.52,
    preprint_misinformation: 0.85, institutional_misconduct_response: 0.50,
    whistleblower_protection: 0.42, reproducibility_infrastructure: 0.40,
    research_fraud_prosecution: 0.38,
  },
  // AIE-005 — high, ai_generated_research_flood (ai_content>0.80, plagiarism>0.75)
  {
    id: "AIE-005", research_field: "intelligence_artificielle", region: "APAC",
    retraction_rate: 0.45, data_fabrication_index: 0.42,
    plagiarism_detection_gap: 0.80, predatory_journal_prevalence: 0.48,
    paper_mill_activity: 0.50, peer_review_quality: 0.52,
    open_access_integrity: 0.48, replication_success_rate: 0.55,
    statistical_manipulation: 0.45, conflicts_of_interest: 0.50,
    industry_funding_bias: 0.52, ai_generated_content_rate: 0.85,
    preprint_misinformation: 0.55, institutional_misconduct_response: 0.52,
    whistleblower_protection: 0.40, reproducibility_infrastructure: 0.38,
    research_fraud_prosecution: 0.35,
  },
  // AIE-006 — moderate, none
  {
    id: "AIE-006", research_field: "sciences_de_lenvironnement", region: "LATAM",
    retraction_rate: 0.28, data_fabrication_index: 0.25,
    plagiarism_detection_gap: 0.30, predatory_journal_prevalence: 0.28,
    paper_mill_activity: 0.25, peer_review_quality: 0.30,
    open_access_integrity: 0.35, replication_success_rate: 0.28,
    statistical_manipulation: 0.25, conflicts_of_interest: 0.30,
    industry_funding_bias: 0.28, ai_generated_content_rate: 0.30,
    preprint_misinformation: 0.28, institutional_misconduct_response: 0.30,
    whistleblower_protection: 0.32, reproducibility_infrastructure: 0.30,
    research_fraud_prosecution: 0.28,
  },
  // AIE-007 — low, none
  {
    id: "AIE-007", research_field: "mathématiques_pures", region: "EMEA",
    retraction_rate: 0.08, data_fabrication_index: 0.06,
    plagiarism_detection_gap: 0.10, predatory_journal_prevalence: 0.08,
    paper_mill_activity: 0.06, peer_review_quality: 0.08,
    open_access_integrity: 0.12, replication_success_rate: 0.08,
    statistical_manipulation: 0.06, conflicts_of_interest: 0.08,
    industry_funding_bias: 0.06, ai_generated_content_rate: 0.10,
    preprint_misinformation: 0.08, institutional_misconduct_response: 0.08,
    whistleblower_protection: 0.10, reproducibility_infrastructure: 0.12,
    research_fraud_prosecution: 0.10,
  },
  // AIE-008 — low, none
  {
    id: "AIE-008", research_field: "physique_théorique", region: "NOAM",
    retraction_rate: 0.10, data_fabrication_index: 0.08,
    plagiarism_detection_gap: 0.08, predatory_journal_prevalence: 0.10,
    paper_mill_activity: 0.08, peer_review_quality: 0.10,
    open_access_integrity: 0.10, replication_success_rate: 0.10,
    statistical_manipulation: 0.08, conflicts_of_interest: 0.10,
    industry_funding_bias: 0.08, ai_generated_content_rate: 0.08,
    preprint_misinformation: 0.10, institutional_misconduct_response: 0.10,
    whistleblower_protection: 0.12, reproducibility_infrastructure: 0.10,
    research_fraud_prosecution: 0.12,
  },
];

type AIEInput = (typeof MOCK_ENTITIES)[0];

function fraudScore(e: AIEInput): number {
  return Math.round((e.data_fabrication_index * 0.4 + e.retraction_rate * 0.35 + e.statistical_manipulation * 0.25) * 100 * 100) / 100;
}
function publishingScore(e: AIEInput): number {
  return Math.round((e.predatory_journal_prevalence * 0.4 + e.paper_mill_activity * 0.35 + e.plagiarism_detection_gap * 0.25) * 100 * 100) / 100;
}
function replicationScore(e: AIEInput): number {
  return Math.round((e.replication_success_rate * 0.4 + e.preprint_misinformation * 0.35 + e.ai_generated_content_rate * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: AIEInput): number {
  return Math.round((e.peer_review_quality * 0.4 + e.institutional_misconduct_response * 0.35 + e.conflicts_of_interest * 0.25) * 100 * 100) / 100;
}
function compositeScore(fr: number, pub: number, rep: number, gov: number): number {
  return Math.round((fr * 0.30 + pub * 0.25 + rep * 0.25 + gov * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function integrityPattern(e: AIEInput): string {
  if (e.data_fabrication_index > 0.85 && e.retraction_rate > 0.80) return "data_fabrication_fraud_ring";
  if (e.predatory_journal_prevalence > 0.85 && e.paper_mill_activity > 0.80) return "predatory_publishing_ecosystem";
  if (e.replication_success_rate > 0.85 && e.preprint_misinformation > 0.80) return "replication_crisis_collapse";
  if (e.peer_review_quality > 0.80 && e.conflicts_of_interest > 0.75) return "peer_review_capture";
  if (e.ai_generated_content_rate > 0.80 && e.plagiarism_detection_gap > 0.75) return "ai_generated_research_flood";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_intégrité_recherche_systémique";
  if (composite >= 40) return "crise_fraude_scientifique_majeure";
  if (composite >= 20) return "déficit_intégrité_académique_structurel";
  return "surveillance_intégrité_recherche_continue";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_intégrité_recherche_critique";
  if (risk === "high") return "renforcement_mécanismes_détection_fraude_accéléré";
  if (risk === "moderate") return "amélioration_gouvernance_publication_scientifique";
  return "veille_intégrité_académique_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise intégrité recherche systémique — fraude scientifique en péril";
  if (risk === "high") return "🟠 Crise fraude scientifique majeure détectée";
  if (risk === "moderate") return "🟡 Déficit intégrité académique structurel actif";
  return "🟢 Intégrité recherche sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const fr   = fraudScore(e);
      const pub  = publishingScore(e);
      const rep  = replicationScore(e);
      const gov  = governanceScore(e);
      const comp = compositeScore(fr, pub, rep, gov);
      const risk = riskLevel(comp);
      const pat  = integrityPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                       e.entity_id,
        research_field:                  e.research_field,
        region:                          e.region,
        fraud_score:                     fr,
        publishing_score:                pub,
        replication_score:               rep,
        governance_score:                gov,
        composite_score:                 comp,
        risk_level:                      risk,
        integrity_pattern:               pat,
        severity:                        sev,
        recommended_action:              action,
        signal:                          sig,
        retraction_rate:                 e.retraction_rate,
        data_fabrication_index:          e.data_fabrication_index,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tFr = 0, tPub = 0, tRep = 0, tGov = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.integrity_pattern] = (pattern_distribution[ent.integrity_pattern] || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tFr   += ent.fraud_score;
      tPub  += ent.publishing_score;
      tRep  += ent.replication_score;
      tGov  += ent.governance_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const avgFraud     = Math.round(tFr   / n * 10) / 10;

    const summary = {
      module_id:                                  428,
      module_name:                                "Intégrité Recherche Académique & Fraude Scientifique Intelligence Engine",
      total:                                      n,
      critical:                                   criticalCount,
      high:                                       highCount,
      moderate:                                   moderateCount,
      low:                                        lowCount,
      avg_composite:                              avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_research_integrity_index:     Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_fraud: avgFraud }, "academic-integrity-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/academic-integrity-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "academic-integrity-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "academic-integrity-engine"),
      { status: 502 }
    );
  }
}
