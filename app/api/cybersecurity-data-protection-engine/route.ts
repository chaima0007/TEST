import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Cybersecurity Data Protection Engine Agent",
  domain: "cybersecurity_data_protection",
  total_entities: 8,
  avg_composite: 59.75,
  confidence_score: 0.91,
  avg_estimated_cybersecurity_data_protection_index: 5.98,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "nist_cybersecurity_framework_2024",
    "owasp_top10_2023",
    "eu_nis2_directive_2024",
    "iso_27001_caelum_2026",
  ],
  critical_alerts: [
    "Injection SQL/NoSQL : validation input obligatoire sur tous les endpoints",
    "Accès API : rotation des clés SWARM_API_URL tous les 90 jours",
    "Ransomware : backup chiffré quotidien hors-site obligatoire",
  ],
  protection_layers: {
    layer1: "sealResponse — signature cryptographique de chaque réponse API",
    layer2: "SWARM_API_URL — credentials jamais dans le code, env vars only",
    layer3: "revalidate:30 — cache court-terme, données fraîches",
    layer4: "HTTPS TLS 1.3 — chiffrement transit",
    layer5: "Accès Chaima uniquement — dashboard protégé auth",
    layer6: "Backup SHA-256 — intégrité vérifiable",
    layer7: "NIS2 compliance — notification incidents 24h",
  },
  data_map: {
    engines_location: "swarm/intelligence/*.py — logique métier",
    api_routes: "app/api/**/ — endpoints protégés sealResponse",
    dashboards: "app/dashboard/**/ — UI lecture seule",
    inventions: "swarm/inventions/*.py — propriété intellectuelle",
    docs: "docs/ — documentation et stratégies",
    git_history: "github.com/chaima0007/TEST — audit trail complet",
  },
  entities: [
    { id: "CAE-SEC-001", name: "Injection SQL/NoSQL", risk_level: "critique", composite_score: 78.0 },
    { id: "CAE-SEC-002", name: "Accès Non Autorisé API", risk_level: "critique", composite_score: 71.5 },
    { id: "CAE-SEC-003", name: "Exfiltration de Données", risk_level: "critique", composite_score: 69.2 },
    { id: "CAE-SEC-004", name: "Malware / Ransomware", risk_level: "critique", composite_score: 65.8 },
    { id: "CAE-SEC-005", name: "Phishing Dirigeants", risk_level: "élevé", composite_score: 54.3 },
    { id: "CAE-SEC-006", name: "Fuites via Prestataires", risk_level: "élevé", composite_score: 49.8 },
    { id: "CAE-SEC-007", name: "DDoS Infrastructure", risk_level: "modéré", composite_score: 35.2 },
    { id: "CAE-SEC-008", name: "Chiffrement Transit/Repos", risk_level: "faible", composite_score: 8.5 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[cybersecurity-data-protection-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/cybersecurity-data-protection-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
