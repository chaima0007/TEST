import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[biopower-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Bio-Power Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/biopower-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Bio-Power Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Bio-Power Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "BP-001", name: "Chine — Biopolitique Totale", country: "Asie", sector: "Surveillance Génomique & Biométrique Maximale", composite_score: 89.85, biometric_surveillance_intensity_score: 98.0, genetic_data_control_score: 95.0, pharmaceutical_dependency_score: 72.0, reproductive_control_score: 90.0, risk_level: "critique", primary_pattern: "biopolitique_totale", key_signals: ["Biopolitique totale en Chine — corps des citoyens sous surveillance génomique/biométrique", "Banques de données génomiques étatiques et biométrie obligatoire systémique", "Autonomie reproductive et corporelle structurellement contrainte par l'État"], estimated_biopower_index: 8.99, last_updated: "2026-06-20" },
    { id: "BP-002", name: "Inde — Aadhaar Biométrique", country: "Asie du Sud", sector: "Biométrie Obligatoire 1.4Md Personnes", composite_score: 81.5, biometric_surveillance_intensity_score: 88.0, genetic_data_control_score: 82.0, pharmaceutical_dependency_score: 75.0, reproductive_control_score: 78.0, risk_level: "critique", primary_pattern: "biopolitique_totale", key_signals: ["Biopolitique totale en Inde — corps des citoyens sous surveillance génomique/biométrique", "Banques de données génomiques étatiques et biométrie obligatoire systémique", "Autonomie reproductive et corporelle structurellement contrainte par l'État"], estimated_biopower_index: 8.15, last_updated: "2026-06-20" },
    { id: "BP-003", name: "Russie — Bio-Pouvoir Militarisé", country: "Europe de l'Est", sector: "Contrôle Reproductif & Biométrique d'État", composite_score: 78.25, biometric_surveillance_intensity_score: 80.0, genetic_data_control_score: 78.0, pharmaceutical_dependency_score: 70.0, reproductive_control_score: 85.0, risk_level: "critique", primary_pattern: "surveillance_biologique", key_signals: ["Biopolitique totale en Russie — corps des citoyens sous surveillance génomique/biométrique", "Banques de données génomiques étatiques et biométrie obligatoire systémique", "Autonomie reproductive et corporelle structurellement contrainte par l'État"], estimated_biopower_index: 7.83, last_updated: "2026-06-20" },
    { id: "BP-004", name: "Moyen-Orient Autoritaire", country: "MENA", sector: "Contrôle Corporel Religieux & Étatique", composite_score: 76.25, biometric_surveillance_intensity_score: 75.0, genetic_data_control_score: 70.0, pharmaceutical_dependency_score: 65.0, reproductive_control_score: 88.0, risk_level: "critique", primary_pattern: "surveillance_biologique", key_signals: ["Biopolitique totale au Moyen-Orient Autoritaire — corps des citoyens sous surveillance génomique/biométrique", "Banques de données génomiques étatiques et biométrie obligatoire systémique", "Autonomie reproductive et corporelle structurellement contrainte par l'État"], estimated_biopower_index: 7.63, last_updated: "2026-06-20" },
    { id: "BP-005", name: "États-Unis — Surveillance Privée", country: "Amérique du Nord", sector: "Big Pharma & Biométrie Corporative", composite_score: 65.75, biometric_surveillance_intensity_score: 65.0, genetic_data_control_score: 60.0, pharmaceutical_dependency_score: 80.0, reproductive_control_score: 55.0, risk_level: "élevé", primary_pattern: "controle_corporel_avance", key_signals: ["Surveillance biologique avancée aux États-Unis — contrôle corporel institutionnel", "Données biométriques collectées massivement — droits corporels fragilisés", "Politiques biopolitiques structurant les comportements reproductifs et sanitaires"], estimated_biopower_index: 6.58, last_updated: "2026-06-20" },
    { id: "BP-006", name: "Europe — GDPR Partiel", country: "Europe", sector: "Tension Santé Publique & Droits Corporels", composite_score: 38.75, biometric_surveillance_intensity_score: 40.0, genetic_data_control_score: 35.0, pharmaceutical_dependency_score: 45.0, reproductive_control_score: 32.0, risk_level: "modéré", primary_pattern: "tension_biopolitique", key_signals: ["Tensions biopolitiques modérées en Europe — bio-surveillance croissante", "Équilibre fragile entre santé publique et autonomie corporelle individuelle", "Régulation biométrique insuffisante face à l'expansion des biotechnologies"], estimated_biopower_index: 3.88, last_updated: "2026-06-20" },
    { id: "BP-007", name: "Corée du Sud — Digital Health", country: "Asie du Nord-Est", sector: "Santé Numérique Avancée avec Garde-fous", composite_score: 32.75, biometric_surveillance_intensity_score: 35.0, genetic_data_control_score: 30.0, pharmaceutical_dependency_score: 38.0, reproductive_control_score: 25.0, risk_level: "modéré", primary_pattern: "tension_biopolitique", key_signals: ["Tensions biopolitiques modérées en Corée du Sud — bio-surveillance croissante", "Équilibre fragile entre santé publique et autonomie corporelle individuelle", "Régulation biométrique insuffisante face à l'expansion des biotechnologies"], estimated_biopower_index: 3.28, last_updated: "2026-06-20" },
    { id: "BP-008", name: "Nordiques — Autonomie Maximale", country: "Europe du Nord", sector: "Droits Corporels Exemplaires", composite_score: 11.75, biometric_surveillance_intensity_score: 12.0, genetic_data_control_score: 10.0, pharmaceutical_dependency_score: 15.0, reproductive_control_score: 8.0, risk_level: "faible", primary_pattern: "autonomie_corporelle", key_signals: ["Nordiques — Autonomie Maximale préserve l'autonomie corporelle — droits fondamentaux biopolitiques protégés", "Cadre légal robuste limitant la bio-surveillance et protégeant les données génomiques", "Modèle de résistance au bio-pouvoir à valoriser et diffuser"], estimated_biopower_index: 1.18, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 1, "modéré": 2, faible: 1 },
    pattern_distribution: { biopolitique_totale: 2, surveillance_biologique: 2, controle_corporel_avance: 1, tension_biopolitique: 2, autonomie_corporelle: 1 },
    top_risk_entities: ["Chine — Biopolitique Totale", "Inde — Aadhaar Biométrique", "Russie — Bio-Pouvoir Militarisé"],
    critical_alerts: ["Chine: biopolitique totale", "Inde: biopolitique totale", "Russie: surveillance biologique", "Moyen-Orient: surveillance biologique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "biopower",
    confidence_score: 0.74,
    data_sources: ["biometric_surveillance_index", "genomic_data_tracker", "reproductive_rights_monitor"],
    entities,
    avg_estimated_biopower_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
