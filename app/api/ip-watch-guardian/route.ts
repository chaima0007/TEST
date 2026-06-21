import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "IP Watch Guardian Agent",
  domain: "ip_protection_monitoring",
  version: "1.0.0",
  alert_email: "retrouvetonsmile@gmail.com",
  report_date: new Date().toISOString().split("T")[0],
  protection_status: "ACTIF",
  assets_protected: { inventions: 5, marques: 6, empreintes_code: 5, domaines: 7 },
  monitoring_channels: 6,
  active_signals: 1,
  critical_alerts: 0,
  alert_protocols: {
    critique: {
      delai_alerte: "IMMÉDIAT (< 1 heure)",
      canal: "Email retrouvetonsmile@gmail.com + SMS",
      action: "Lettre de mise en demeure + saisie tribunal en urgence",
      escalade: "Cabinet IP belge dans les 24h",
    },
    élevé: {
      delai_alerte: "< 24 heures",
      canal: "Email retrouvetonsmile@gmail.com",
      action: "Notification EUIPO/EPO + documentation preuve",
      escalade: "Évaluation juridique sous 48h",
    },
    modéré: {
      delai_alerte: "< 72 heures",
      canal: "Rapport hebdomadaire retrouvetonsmile@gmail.com",
      action: "Surveillance renforcée + documentation",
      escalade: "Revue mensuelle",
    },
    faible: {
      delai_alerte: "Rapport mensuel",
      canal: "Digest retrouvetonsmile@gmail.com",
      action: "Archivage + surveillance continue",
      escalade: "Aucune",
    },
  },
  signals: [
    {
      signal_id: "IPW-2025-001",
      threat_type: "squatting_domaine",
      severity: "élevé",
      source: "dns",
      description: "Domaine 'caelum-partners.com' non réservé — risque de cybersquatting",
      action_required: "Réserver caelum-partners.com, caelumpartners.eu, caelumpartners.org (~€30/an)",
      detected_at: new Date().toISOString().split("T")[0],
      alert_sent: true,
    },
  ],
  monitoring_coverage: [
    { channel: "GitHub Code Search", assets_monitored: ["sealResponse pattern", "GaugeRing SVG", "SWARM_API_URL guard", "composite_score formula"], check_frequency: "quotidien", status: "actif" },
    { channel: "EUIPO Trademark Watch", assets_monitored: ["Caelum Partners", "CaelumSwarm", "CaelumPulse", "ComplianceIQ"], check_frequency: "hebdomadaire", status: "actif" },
    { channel: "EPO Patent Watch", assets_monitored: ["swarm agents human rights", "composite risk scoring", "CSDDD compliance"], check_frequency: "mensuel", status: "actif" },
    { channel: "DNS/Domain Squatting", assets_monitored: ["caelumpartners.*", "caelumswarm.*", "caelumpulse.*"], check_frequency: "quotidien", status: "actif" },
    { channel: "Web Content Scraping", assets_monitored: ["textes dashboards", "formules scoring", "architecture docs"], check_frequency: "hebdomadaire", status: "actif" },
    { channel: "npm/PyPI Package Watch", assets_monitored: ["caelum-swarm", "caelum-seal", "caelum-pulse"], check_frequency: "hebdomadaire", status: "actif" },
  ],
  protected_assets: {
    inventions: [
      "CAE-INV-2025-001 — CaelumSwarm™",
      "CAE-INV-2025-002 — CaelumSeal™",
      "CAE-INV-2025-003 — ComplianceIQ™",
      "CAE-INV-2025-004 — CaelumPulse™",
      "CAE-INV-2025-005 — DueDiligenceOS™",
    ],
    marques: ["Caelum Partners™", "CaelumSwarm™", "CaelumSeal™", "CaelumPulse™", "ComplianceIQ™", "DueDiligenceOS™"],
  },
  next_actions: [
    "Réserver domaines variantes caelumpartners.eu/.org",
    "Déposer marque EUIPO 'Caelum Partners' (classe 42)",
    "Dépôt provisoire EPO CAE-INV-2025-001 avant juillet 2026",
    "Activer Google Alerts: 'CaelumSwarm', 'Caelum Partners'",
    "Configurer GitHub secret scanning",
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[ip-watch-guardian] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/ip-watch-guardian`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
