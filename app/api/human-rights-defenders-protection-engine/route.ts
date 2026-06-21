import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[human-rights-defenders-protection-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  "agent": "Human Rights Defenders Protection Engine Agent",
  "domain": "human_rights_defenders_protection",
  "total_entities": 8,
  "avg_composite": 61.46,
  "confidence_score": 0.85,
  "risk_distribution": {
    "critique": 4,
    "élevé": 2,
    "modéré": 1,
    "faible": 1
  },
  "pattern_distribution": {
    "hrd_killing_disappearance_severity": 3,
    "ngo_restriction_foreign_agent_law_deficit_gap": 2,
    "criminalization_legal_harassment_scale": 2,
    "digital_surveillance_doxxing_hrd": 1
  },
  "top_risk_entities": [
    "Colombie — Premier Pays Monde Meurtres Défenseurs, Leaders Sociaux Assassinés, Communautés Autochtones Ciblées & Impunité 95%",
    "Mexique — Journalistes Défenseurs Environnement Assassinés, Cartels Ciblant Activistes, Disparitions Forcées & Protection Insuffisante",
    "Russie — Lois Agents Étrangers Museler ONG, Alexei Navalny Assassiné Prison, Memorial Liquidé & Défenseurs Exilés Persécutés"
  ],
  "critical_alerts": [
    "Colombie: hrd_killing_disappearance_severity",
    "Mexique: hrd_killing_disappearance_severity",
    "Russie: ngo_restriction_foreign_agent_law_deficit_gap",
    "Éthiopie/Soudan: criminalization_legal_harassment_scale"
  ],
  "last_analysis": "2026-06-21",
  "engine_version": "1.0.0",
  "avg_estimated_human_rights_defenders_protection_index": 6.15,
  "data_sources": [
    "front_line_defenders_annual_report_hrd_killings",
    "global_witness_hrd_murders_tracking_database",
    "civicus_ngo_restriction_closing_space_monitor"
  ],
  "entities": [
    {
      "entity_id": "HRD-001",
      "name": "Colombie — Premier Pays Monde Meurtres Défenseurs, Leaders Sociaux Assassinés, Communautés Autochtones Ciblées & Impunité 95%",
      "country": "Colombie",
      "hrd_killing_disappearance_severity_score": 96.0,
      "criminalization_legal_harassment_scale_score": 92.0,
      "digital_surveillance_doxxing_hrd_score": 90.0,
      "ngo_restriction_foreign_agent_law_deficit_gap_score": 94.0,
      "primary_pattern": "hrd_killing_disappearance_severity",
      "last_updated": "2026-06-21",
      "composite_score": 93.1,
      "risk_level": "critique",
      "estimated_human_rights_defenders_protection_index": 9.31
    },
    {
      "entity_id": "HRD-002",
      "name": "Mexique — Journalistes Défenseurs Environnement Assassinés, Cartels Ciblant Activistes, Disparitions Forcées & Protection Insuffisante",
      "country": "Mexique",
      "hrd_killing_disappearance_severity_score": 93.0,
      "criminalization_legal_harassment_scale_score": 89.0,
      "digital_surveillance_doxxing_hrd_score": 90.0,
      "ngo_restriction_foreign_agent_law_deficit_gap_score": 88.0,
      "primary_pattern": "hrd_killing_disappearance_severity",
      "last_updated": "2026-06-21",
      "composite_score": 90.25,
      "risk_level": "critique",
      "estimated_human_rights_defenders_protection_index": 9.03
    },
    {
      "entity_id": "HRD-003",
      "name": "Russie — Lois Agents Étrangers Museler ONG, Alexei Navalny Assassiné Prison, Memorial Liquidé & Défenseurs Exilés Persécutés",
      "country": "Russie",
      "hrd_killing_disappearance_severity_score": 90.0,
      "criminalization_legal_harassment_scale_score": 87.0,
      "digital_surveillance_doxxing_hrd_score": 86.0,
      "ngo_restriction_foreign_agent_law_deficit_gap_score": 85.0,
      "primary_pattern": "ngo_restriction_foreign_agent_law_deficit_gap",
      "last_updated": "2026-06-21",
      "composite_score": 87.25,
      "risk_level": "critique",
      "estimated_human_rights_defenders_protection_index": 8.73
    },
    {
      "entity_id": "HRD-004",
      "name": "Éthiopie/Soudan — Défenseurs Tigré Arrêtés, Journalistes Emprisonnés Conflit, Activistes Disparus & Accès Humanitaire Bloqué",
      "country": "Éthiopie/Soudan",
      "hrd_killing_disappearance_severity_score": 87.0,
      "criminalization_legal_harassment_scale_score": 83.0,
      "digital_surveillance_doxxing_hrd_score": 82.0,
      "ngo_restriction_foreign_agent_law_deficit_gap_score": 84.0,
      "primary_pattern": "criminalization_legal_harassment_scale",
      "last_updated": "2026-06-21",
      "composite_score": 84.15,
      "risk_level": "critique",
      "estimated_human_rights_defenders_protection_index": 8.42
    },
    {
      "entity_id": "HRD-005",
      "name": "Chine/Vietnam — Avocats Droits Homme Détenus Arbitrairement, Loi Cybersécurité Surveillance Massive & ONG Sous Contrôle Parti",
      "country": "Chine/Vietnam",
      "hrd_killing_disappearance_severity_score": 57.0,
      "criminalization_legal_harassment_scale_score": 54.0,
      "digital_surveillance_doxxing_hrd_score": 55.0,
      "ngo_restriction_foreign_agent_law_deficit_gap_score": 53.0,
      "primary_pattern": "digital_surveillance_doxxing_hrd",
      "last_updated": "2026-06-21",
      "composite_score": 54.95,
      "risk_level": "élevé",
      "estimated_human_rights_defenders_protection_index": 5.5
    },
    {
      "entity_id": "HRD-006",
      "name": "Égypte/Bangladesh — Défenseurs Emprisonnés Lois Antiterrorisme, ONG Loi 70/2017 Restrictive & Doxxing Militantes Femmes",
      "country": "Égypte/Bangladesh",
      "hrd_killing_disappearance_severity_score": 54.0,
      "criminalization_legal_harassment_scale_score": 51.0,
      "digital_surveillance_doxxing_hrd_score": 52.0,
      "ngo_restriction_foreign_agent_law_deficit_gap_score": 50.0,
      "primary_pattern": "ngo_restriction_foreign_agent_law_deficit_gap",
      "last_updated": "2026-06-21",
      "composite_score": 51.95,
      "risk_level": "élevé",
      "estimated_human_rights_defenders_protection_index": 5.2
    },
    {
      "entity_id": "HRD-007",
      "name": "Front Line Defenders — Système Alerte Urgence Défenseurs Risque, Documentation Meurtres Annuels & Bourses Protection Numérique",
      "country": "Global",
      "hrd_killing_disappearance_severity_score": 28.0,
      "criminalization_legal_harassment_scale_score": 25.0,
      "digital_surveillance_doxxing_hrd_score": 26.0,
      "ngo_restriction_foreign_agent_law_deficit_gap_score": 24.0,
      "primary_pattern": "hrd_killing_disappearance_severity",
      "last_updated": "2026-06-21",
      "composite_score": 25.95,
      "risk_level": "modéré",
      "estimated_human_rights_defenders_protection_index": 2.6
    },
    {
      "entity_id": "HRD-008",
      "name": "ONU Déclaration 1998 — Déclaration Défenseurs Droits Homme, Rapporteur Spécial HRD & Résolutions Conseil Droits Homme",
      "country": "Global",
      "hrd_killing_disappearance_severity_score": 5.0,
      "criminalization_legal_harassment_scale_score": 4.0,
      "digital_surveillance_doxxing_hrd_score": 4.0,
      "ngo_restriction_foreign_agent_law_deficit_gap_score": 3.0,
      "primary_pattern": "criminalization_legal_harassment_scale",
      "last_updated": "2026-06-21",
      "composite_score": 4.1,
      "risk_level": "faible",
      "estimated_human_rights_defenders_protection_index": 0.41
    }
  ]
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/human-rights-defenders-protection-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
