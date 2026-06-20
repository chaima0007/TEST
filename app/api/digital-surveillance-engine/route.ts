import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-surveillance-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Digital Surveillance Engine Agent",
  domain: "digital_surveillance",
  total_entities: 8,
  avg_composite: 60.15,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { mass_surveillance_scale: 2, journalist_activist_targeting: 2, legal_safeguard_absence: 2, spyware_export_impunity: 2 },
  top_risk_entities: [
    "Chine — Système Crédit Social, Reconnaissance Faciale 1,4Mrd & Surveillance Totale Xinjiang",
    "NSO Group/Pegasus — Spyware Vendu 45 Pays, Journalistes/Activistes Ciblés & Impunité Israël",
    "Russie — SORM Interception Totale, Loi Yarovaya & Surveillance Opposants Post-2022",
  ],
  critical_alerts: [
    "Chine: mass_surveillance_scale",
    "NSO Group/Pegasus: journalist_activist_targeting",
    "Russie: legal_safeguard_absence",
    "Iran: legal_safeguard_absence",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_digital_surveillance_index: 6.02,
  data_sources: [
    "citizen_lab_pegasus_spyware_global_targeting_report",
    "access_now_digital_rights_surveillance_annual_report",
    "freedom_house_freedom_on_the_net_global_internet_freedom_index",
  ],
  entities: [
    { entity_id: "DS-001", name: "Chine — Système Crédit Social, Reconnaissance Faciale 1,4Mrd & Surveillance Totale Xinjiang", country: "Asie du Nord-Est", composite_score: 94.15, mass_surveillance_scale_score: 98.0, journalist_activist_targeting_score: 95.0, legal_safeguard_absence_score: 92.0, spyware_export_impunity_score: 90.0, risk_level: "critique", primary_pattern: "mass_surveillance_scale", estimated_digital_surveillance_index: 9.42, last_updated: "2026-06-20" },
    { entity_id: "DS-002", name: "NSO Group/Pegasus — Spyware Vendu 45 Pays, Journalistes/Activistes Ciblés & Impunité Israël", country: "Global/Moyen-Orient", composite_score: 89.05, mass_surveillance_scale_score: 88.0, journalist_activist_targeting_score: 92.0, legal_safeguard_absence_score: 85.0, spyware_export_impunity_score: 92.0, risk_level: "critique", primary_pattern: "journalist_activist_targeting", estimated_digital_surveillance_index: 8.91, last_updated: "2026-06-20" },
    { entity_id: "DS-003", name: "Russie — SORM Interception Totale, Loi Yarovaya & Surveillance Opposants Post-2022", country: "Europe de l'Est", composite_score: 84.75, mass_surveillance_scale_score: 85.0, journalist_activist_targeting_score: 88.0, legal_safeguard_absence_score: 85.0, spyware_export_impunity_score: 80.0, risk_level: "critique", primary_pattern: "legal_safeguard_absence", estimated_digital_surveillance_index: 8.48, last_updated: "2026-06-20" },
    { entity_id: "DS-004", name: "Iran — Internet National, VPN Criminalité & Coupures Réseau lors Protestations Mahsa Amini", country: "Moyen-Orient", composite_score: 81.35, mass_surveillance_scale_score: 80.0, journalist_activist_targeting_score: 82.0, legal_safeguard_absence_score: 85.0, spyware_export_impunity_score: 78.0, risk_level: "critique", primary_pattern: "legal_safeguard_absence", estimated_digital_surveillance_index: 8.14, last_updated: "2026-06-20" },
    { entity_id: "DS-005", name: "USA/Five Eyes — PRISM/NSA Métadonnées, Section 702 FISA & Surveillance Internationale Massive", country: "Amérique du Nord", composite_score: 53.0, mass_surveillance_scale_score: 55.0, journalist_activist_targeting_score: 50.0, legal_safeguard_absence_score: 52.0, spyware_export_impunity_score: 55.0, risk_level: "élevé", primary_pattern: "spyware_export_impunity", estimated_digital_surveillance_index: 5.3, last_updated: "2026-06-20" },
    { entity_id: "DS-006", name: "UE/Règlement eSurveillance — Débat Chat Control, Chiffrement Menacé & Résistance Société Civile", country: "Europe", composite_score: 48.65, mass_surveillance_scale_score: 48.0, journalist_activist_targeting_score: 45.0, legal_safeguard_absence_score: 52.0, spyware_export_impunity_score: 50.0, risk_level: "élevé", primary_pattern: "spyware_export_impunity", estimated_digital_surveillance_index: 4.87, last_updated: "2026-06-20" },
    { entity_id: "DS-007", name: "Access Now/EFF — Défense Chiffrement, Rapports Pegasus & Plaidoyer Régulation Spyware", country: "Global", composite_score: 25.85, mass_surveillance_scale_score: 22.0, journalist_activist_targeting_score: 28.0, legal_safeguard_absence_score: 25.0, spyware_export_impunity_score: 30.0, risk_level: "modéré", primary_pattern: "mass_surveillance_scale", estimated_digital_surveillance_index: 2.59, last_updated: "2026-06-20" },
    { entity_id: "DS-008", name: "ONU/Rapporteur Vie Privée — Rapport Surveillance Numerique, Normes & Recommandations États", country: "Global", composite_score: 4.4, mass_surveillance_scale_score: 4.0, journalist_activist_targeting_score: 5.0, legal_safeguard_absence_score: 3.0, spyware_export_impunity_score: 6.0, risk_level: "faible", primary_pattern: "journalist_activist_targeting", estimated_digital_surveillance_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-surveillance-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
