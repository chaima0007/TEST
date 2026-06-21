import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Third Party Work Validation Engine Agent",
  domain: "third_party_work_validation",
  total_entities: 8,
  avg_composite: 58.50,
  confidence_score: 0.93,
  avg_estimated_third_party_work_validation_index: 5.85,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "caelum_internal_audit_protocol_2026",
    "iso_9001_quality_management",
    "eu_gdpr_contractor_compliance",
    "nda_ip_assignment_framework_be",
  ],
  critical_alerts: [
    "Tout livrable doit obtenir le feu vert de Chaima Mhadbi avant intégration",
    "Agents IA : chaque commit soumis à revue humaine obligatoire",
  ],
  entities: [
    { id: "CAE-TP-001", name: "Consultant Externe Court-Terme", risk_level: "critique", composite_score: 72.5, contract_ip_clauses: 5.2, approval_compliance: 4.8 },
    { id: "CAE-TP-002", name: "Partenaire Technologique", risk_level: "critique", composite_score: 68.3, contract_ip_clauses: 6.1, approval_compliance: 5.2 },
    { id: "CAE-TP-003", name: "Sous-Traitant Offshore", risk_level: "critique", composite_score: 75.1, contract_ip_clauses: 4.5, approval_compliance: 4.2 },
    { id: "CAE-TP-004", name: "Agent IA Autonome", risk_level: "critique", composite_score: 65.8, contract_ip_clauses: 7.0, approval_compliance: 5.5 },
    { id: "CAE-TP-005", name: "Freelance Spécialisé", risk_level: "élevé", composite_score: 52.4, contract_ip_clauses: 7.5, approval_compliance: 6.8 },
    { id: "CAE-TP-006", name: "Cabinet Conseil Senior", risk_level: "élevé", composite_score: 48.9, contract_ip_clauses: 8.2, approval_compliance: 7.1 },
    { id: "CAE-TP-007", name: "Partenaire Certifié Récurrent", risk_level: "modéré", composite_score: 32.1, contract_ip_clauses: 8.8, approval_compliance: 8.5 },
    { id: "CAE-TP-008", name: "Équipe Interne Caelum", risk_level: "faible", composite_score: 12.5, contract_ip_clauses: 9.9, approval_compliance: 9.8 },
  ],
  validation_protocol: {
    step1: "Contrat signé avec clauses IP/NDA avant tout démarrage",
    step2: "Checkpoint à 25% — revue intermédiaire obligatoire",
    step3: "Checkpoint à 75% — pré-validation technique",
    step4: "Feu vert final Chaima Mhadbi — acceptance signée",
    step5: "Archivage sécurisé + empreinte SHA-256 du livrable",
  },
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[third-party-work-validation-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/third-party-work-validation-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
