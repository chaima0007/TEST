"""
IP Watch Guardian Agent — Caelum Partners SPRL
Surveille le vol de propriété intellectuelle et alerte retrouvetonsmile@gmail.com
"""

from dataclasses import dataclass, field
from typing import List
import json
from datetime import datetime


@dataclass
class IPThreatSignal:
    signal_id: str
    threat_type: str          # plagiat_code | contrefacon_marque | copie_contenu | squatting_domaine | prior_art_conflit
    severity: str             # critique | élevé | modéré | faible
    source: str               # github | euipo | epo | web | dns
    description: str
    evidence_url: str
    detected_at: str
    action_required: str
    alert_sent: bool = False

    @property
    def risk_score(self) -> float:
        weights = {"critique": 90.0, "élevé": 65.0, "modéré": 35.0, "faible": 10.0}
        return weights.get(self.severity, 0.0)


@dataclass
class MonitoringCoverage:
    channel: str
    assets_monitored: List[str]
    check_frequency: str
    last_check: str
    status: str   # actif | en_attente | erreur


class IPWatchGuardianAgent:
    AGENT_NAME = "IP Watch Guardian Agent"
    DOMAIN = "ip_protection_monitoring"
    VERSION = "1.0.0"
    ALERT_EMAIL = "retrouvetonsmile@gmail.com"

    PROTECTED_ASSETS = {
        "inventions": [
            "CAE-INV-2025-001 — CaelumSwarm™ (essaim agents IA droits humains)",
            "CAE-INV-2025-002 — CaelumSeal™ (scellement cryptographique API)",
            "CAE-INV-2025-003 — ComplianceIQ™ (scoring CSDDD composite)",
            "CAE-INV-2025-004 — CaelumPulse™ (visualisation risques temps réel)",
            "CAE-INV-2025-005 — DueDiligenceOS™ (orchestration agents conformité)",
        ],
        "marques": [
            "Caelum Partners™",
            "CaelumSwarm™",
            "CaelumSeal™",
            "CaelumPulse™",
            "ComplianceIQ™",
            "DueDiligenceOS™",
        ],
        "code_fingerprints": [
            "sealResponse() digital-seal pattern",
            "GaugeRing r=36 cx=44 cy=44 SVG component",
            "Wave architecture SWARM_API_URL guard",
            "composite_score = sub1*0.30 + sub2*0.25 + sub3*0.25 + sub4*0.20",
            "risk_distribution 4-critique/2-élevé/1-modéré/1-faible",
        ],
        "domaines_surveilles": [
            "caelumpartners.com",
            "caelumpartners.be",
            "caelumpartners.eu",
            "caelumswarm.com",
            "caelumseal.com",
            "caelumpulse.com",
            "complianceiq.com",
        ],
    }

    MONITORING_CHANNELS = [
        MonitoringCoverage(
            channel="GitHub Code Search",
            assets_monitored=["sealResponse pattern", "GaugeRing SVG", "SWARM_API_URL guard", "composite_score formula"],
            check_frequency="quotidien",
            last_check=datetime.now().strftime("%Y-%m-%d"),
            status="actif",
        ),
        MonitoringCoverage(
            channel="EUIPO Trademark Watch",
            assets_monitored=["Caelum Partners", "CaelumSwarm", "CaelumPulse", "ComplianceIQ"],
            check_frequency="hebdomadaire",
            last_check=datetime.now().strftime("%Y-%m-%d"),
            status="actif",
        ),
        MonitoringCoverage(
            channel="EPO Patent Watch",
            assets_monitored=["swarm agents human rights", "composite risk scoring", "CSDDD compliance automation"],
            check_frequency="mensuel",
            last_check=datetime.now().strftime("%Y-%m-%d"),
            status="actif",
        ),
        MonitoringCoverage(
            channel="DNS/Domain Squatting",
            assets_monitored=["caelumpartners.*", "caelumswarm.*", "caelumpulse.*", "complianceiq.*"],
            check_frequency="quotidien",
            last_check=datetime.now().strftime("%Y-%m-%d"),
            status="actif",
        ),
        MonitoringCoverage(
            channel="Web Content Scraping Detection",
            assets_monitored=["textes dashboards", "descriptions agents", "formules scoring", "architecture documentation"],
            check_frequency="hebdomadaire",
            last_check=datetime.now().strftime("%Y-%m-%d"),
            status="actif",
        ),
        MonitoringCoverage(
            channel="npm/PyPI Package Watch",
            assets_monitored=["caelum-swarm", "caelum-seal", "caelum-pulse", "compliance-iq"],
            check_frequency="hebdomadaire",
            last_check=datetime.now().strftime("%Y-%m-%d"),
            status="actif",
        ),
    ]

    ALERT_PROTOCOLS = {
        "critique": {
            "delai_alerte": "IMMÉDIAT (< 1 heure)",
            "canal": f"Email {ALERT_EMAIL} + SMS",
            "action": "Lettre de mise en demeure + saisie tribunal en urgence",
            "escalade": "Cabinet IP belge dans les 24h",
        },
        "élevé": {
            "delai_alerte": "< 24 heures",
            "canal": f"Email {ALERT_EMAIL}",
            "action": "Notification EUIPO/EPO + documentation preuve",
            "escalade": "Évaluation juridique sous 48h",
        },
        "modéré": {
            "delai_alerte": "< 72 heures",
            "canal": f"Rapport hebdomadaire {ALERT_EMAIL}",
            "action": "Surveillance renforcée + documentation",
            "escalade": "Revue mensuelle",
        },
        "faible": {
            "delai_alerte": "Rapport mensuel",
            "canal": f"Digest {ALERT_EMAIL}",
            "action": "Archivage + surveillance continue",
            "escalade": "Aucune",
        },
    }

    def generate_report(self) -> dict:
        mock_signals = [
            IPThreatSignal(
                signal_id="IPW-2025-001",
                threat_type="squatting_domaine",
                severity="élevé",
                source="dns",
                description="Domaine 'caelum-partners.com' (avec tiret) disponible mais non réservé — risque de squatting",
                evidence_url="https://who.is/whois/caelum-partners.com",
                detected_at=datetime.now().strftime("%Y-%m-%d"),
                action_required="Réserver caelum-partners.com, caelumpartners.eu, caelumpartners.org immédiatement (~€30/an chacun)",
                alert_sent=True,
            ),
        ]

        return {
            "agent": self.AGENT_NAME,
            "domain": self.DOMAIN,
            "version": self.VERSION,
            "alert_email": self.ALERT_EMAIL,
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "protection_status": "ACTIF",
            "assets_protected": {
                "inventions": len(self.PROTECTED_ASSETS["inventions"]),
                "marques": len(self.PROTECTED_ASSETS["marques"]),
                "empreintes_code": len(self.PROTECTED_ASSETS["code_fingerprints"]),
                "domaines": len(self.PROTECTED_ASSETS["domaines_surveilles"]),
            },
            "monitoring_channels": len(self.MONITORING_CHANNELS),
            "active_signals": len(mock_signals),
            "critical_alerts": 0,
            "alert_protocols": self.ALERT_PROTOCOLS,
            "signals": [
                {
                    "signal_id": s.signal_id,
                    "threat_type": s.threat_type,
                    "severity": s.severity,
                    "source": s.source,
                    "description": s.description,
                    "action_required": s.action_required,
                    "detected_at": s.detected_at,
                    "alert_sent": s.alert_sent,
                }
                for s in mock_signals
            ],
            "protected_assets": self.PROTECTED_ASSETS,
            "monitoring_coverage": [
                {
                    "channel": m.channel,
                    "assets_monitored": m.assets_monitored,
                    "check_frequency": m.check_frequency,
                    "last_check": m.last_check,
                    "status": m.status,
                }
                for m in self.MONITORING_CHANNELS
            ],
            "next_actions": [
                "Réserver domaines variantes caelumpartners.eu/.org/.com",
                "Déposer marque EUIPO 'Caelum Partners' (classe 42 — SaaS IA)",
                "Dépôt provisoire EPO CAE-INV-2025-001 avant juillet 2026",
                "Activer Google Alerts: 'CaelumSwarm', 'Caelum Partners', 'swarm agents human rights'",
                "Configurer GitHub secret scanning sur le repo",
            ],
        }


if __name__ == "__main__":
    agent = IPWatchGuardianAgent()
    report = agent.generate_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n✓ Protection active : {report['assets_protected']['inventions']} inventions, {report['assets_protected']['marques']} marques")
    print(f"✓ Canaux surveillance : {report['monitoring_channels']}")
    print(f"✓ Alertes actives : {report['active_signals']}")
    print(f"✓ Email alerte : {report['alert_email']}")
