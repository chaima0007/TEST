import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[telemedicine-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Telemedicine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/telemedicine-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Telemedicine Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Telemedicine Agent"),
      { status: 502 }
    );
  }
}

function getMockData() {
  const entities = [
    {
      id: "TLM-001",
      name: "CHU Afrique Sub-Saharienne",
      country: "Senegal",
      sector: "Healthcare",
      composite_score: 79.0,
      access_score: 85.0,
      quality_score: 78.0,
      security_score: 72.0,
      adoption_score: 80.0,
      risk_level: "critique",
      primary_pattern: "Désert Médical Numérique",
      recommended_action: "intervention_urgente_infrastructure_télémédecine",
      key_signals: [
        "Couverture réseau mobile inférieure à 30% dans les zones rurales périphériques",
        "Absence de dispositifs de diagnostic connectés dans 68% des centres de santé",
        "Délai moyen de téléconsultation supérieur à 72 heures faute d'infrastructure",
      ],
      estimated_telemedicine_index: 7.9,
      last_updated: "2026-06-20",
    },
    {
      id: "TLM-002",
      name: "Clinique Rurale Myanmar",
      country: "Myanmar",
      sector: "Healthcare",
      composite_score: 79.5,
      access_score: 90.0,
      quality_score: 82.0,
      security_score: 68.0,
      adoption_score: 75.0,
      risk_level: "critique",
      primary_pattern: "Désert Médical Numérique",
      recommended_action: "intervention_urgente_infrastructure_télémédecine",
      key_signals: [
        "Ratio médecin-patient de 1 pour 12 000 habitants en zone rurale",
        "Infrastructure électrique défaillante rendant inutilisables 40% des équipements télé-médicaux",
        "Barrière linguistique critique affectant la qualité des consultations à distance",
      ],
      estimated_telemedicine_index: 7.95,
      last_updated: "2026-06-20",
    },
    {
      id: "TLM-003",
      name: "TeleSanté Haïti",
      country: "Haiti",
      sector: "Healthcare",
      composite_score: 75.4,
      access_score: 88.0,
      quality_score: 75.0,
      security_score: 65.0,
      adoption_score: 70.0,
      risk_level: "critique",
      primary_pattern: "Fraude Téléconsultation",
      recommended_action: "intervention_urgente_infrastructure_télémédecine",
      key_signals: [
        "Multiplication des plateformes non agréées proposant des consultations médicales frauduleuses",
        "Usurpation d'identité de médecins détectée dans 23% des sessions de téléconsultation auditées",
        "Facturation illicite de médicaments non prescrits via des canaux de télémédecine parallèles",
      ],
      estimated_telemedicine_index: 7.54,
      last_updated: "2026-06-20",
    },
    {
      id: "TLM-004",
      name: "Hopital District Maroc",
      country: "Morocco",
      sector: "Healthcare",
      composite_score: 49.0,
      access_score: 55.0,
      quality_score: 48.0,
      security_score: 42.0,
      adoption_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "Faille Sécurité Données Santé",
      recommended_action: "audit_sécurité_données_santé_prioritaire",
      key_signals: [
        "Dossiers médicaux électroniques stockés sans chiffrement sur des serveurs locaux vulnérables",
        "Absence de protocole d'authentification multifacteur pour les accès aux systèmes médicaux distants",
        "Trois incidents de fuite de données patients signalés au cours des six derniers mois",
      ],
      estimated_telemedicine_index: 4.9,
      last_updated: "2026-06-20",
    },
    {
      id: "TLM-005",
      name: "DocConnect India Rural",
      country: "India",
      sector: "HealthTech",
      composite_score: 49.05,
      access_score: 58.0,
      quality_score: 45.0,
      security_score: 40.0,
      adoption_score: 52.0,
      risk_level: "élevé",
      primary_pattern: "Faille Sécurité Données Santé",
      recommended_action: "audit_sécurité_données_santé_prioritaire",
      key_signals: [
        "API de partage de données médicales exposées sans authentification sur des endpoints publics",
        "Conformité PDPA insuffisante avec stockage de données biométriques hors consentement",
        "Vulnérabilités zero-day non corrigées dans l'application mobile de téléconsultation",
      ],
      estimated_telemedicine_index: 4.91,
      last_updated: "2026-06-20",
    },
    {
      id: "TLM-006",
      name: "MedTech SARL",
      country: "France",
      sector: "HealthTech",
      composite_score: 26.65,
      access_score: 30.0,
      quality_score: 28.0,
      security_score: 25.0,
      adoption_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "Adoption Insuffisante",
      recommended_action: "programme_adoption_sensibilisation_médecins",
      key_signals: [
        "Taux d'utilisation de la plateforme de télémédecine inférieur à 15% parmi les praticiens inscrits",
        "Résistance au changement des équipes médicales formées aux pratiques de consultation présentielle",
        "Absence de remboursement systématique des téléconsultations par les organismes de sécurité sociale partenaires",
      ],
      estimated_telemedicine_index: 2.66,
      last_updated: "2026-06-20",
    },
    {
      id: "TLM-007",
      name: "TeleClinic Nordic",
      country: "Sweden",
      sector: "Healthcare",
      composite_score: 11.1,
      access_score: 12.0,
      quality_score: 10.0,
      security_score: 8.0,
      adoption_score: 15.0,
      risk_level: "faible",
      primary_pattern: "Qualité Consultation Dégradée",
      recommended_action: "veille_qualité_téléconsultation_continue",
      key_signals: [
        "Score de satisfaction patient en baisse de 18 points suite à la dégradation de la qualité audio-vidéo",
        "Taux de rediagnostic post-téléconsultation de 8% indiquant des erreurs d'évaluation à distance",
        "Durée moyenne de consultation réduite à 4 minutes en raison de la surcharge des files d'attente virtuelles",
      ],
      estimated_telemedicine_index: 1.11,
      last_updated: "2026-06-20",
    },
    {
      id: "TLM-008",
      name: "DigitalHealth AG",
      country: "Switzerland",
      sector: "HealthTech",
      composite_score: 10.0,
      access_score: 10.0,
      quality_score: 8.0,
      security_score: 12.0,
      adoption_score: 10.0,
      risk_level: "faible",
      primary_pattern: "Qualité Consultation Dégradée",
      recommended_action: "veille_qualité_téléconsultation_continue",
      key_signals: [
        "Latence réseau moyenne de 340ms dégradant significativement la qualité des consultations spécialisées",
        "Taux d'abandon en cours de téléconsultation de 22% lié à des problèmes de connectivité",
        "Manque d'intégration avec les systèmes HIS hospitaliers entraînant des doublons de prescriptions",
      ],
      estimated_telemedicine_index: 1.0,
      last_updated: "2026-06-20",
    },
  ];

  const risk_distribution: Record<string, number> = {};
  const pattern_distribution: Record<string, number> = {};
  const top_risk_entities: string[] = [];
  const critical_alerts: string[] = [];
  let totalComposite = 0;

  for (const e of entities) {
    risk_distribution[e.risk_level] = (risk_distribution[e.risk_level] || 0) + 1;
    pattern_distribution[e.primary_pattern] = (pattern_distribution[e.primary_pattern] || 0) + 1;
    totalComposite += e.composite_score;
    if (e.risk_level === "critique") {
      top_risk_entities.push(e.name);
      critical_alerts.push(e.name);
    }
  }

  const n = entities.length;
  const avg_composite = Math.round((totalComposite / n) * 100) / 100;

  return {
    total_entities: n,
    avg_composite,
    risk_distribution,
    pattern_distribution,
    top_risk_entities,
    critical_alerts,
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "telemedicine",
    confidence_score: 0.91,
    data_sources: [
      "WHO Telemedicine Registry",
      "ITU Digital Health Index",
      "GSMA Mobile Health Report",
    ],
    entities,
    avg_estimated_telemedicine_index: Math.round((avg_composite / 100) * 10 * 100) / 100,
  };
}
