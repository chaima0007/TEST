"""
Patent Watch Agent — Caelum Partners SPRL
Inventrice : Chaima Mhadbi
Surveillance concurrentielle du portefeuille de brevets G1-G4
"""

from dataclasses import dataclass, field
from typing import List
from datetime import date


@dataclass
class PatentWatchConfig:
    patent_id: str
    title: str
    search_keywords: List[str] = field(default_factory=list)
    competitor_assignees: List[str] = field(default_factory=list)
    ipc_classes_to_monitor: List[str] = field(default_factory=list)
    alert_criteria: List[str] = field(default_factory=list)


def build_patent_watch_configs() -> List[PatentWatchConfig]:
    return [
        PatentWatchConfig(
            patent_id="CAE-INV-001",
            title="Système de Scoring IA pour l'Évaluation des Droits Humains",
            search_keywords=[
                "human rights scoring AI",
                "droits humains intelligence artificielle scoring",
                "human rights index machine learning",
                "composite human rights indicator neural network",
                "automated human rights assessment",
                "rights violation detection algorithm",
            ],
            competitor_assignees=[
                "Palantir Technologies",
                "IBM Research",
                "Amnesty International Tech",
                "Human Rights Watch Digital",
                "OHCHR Data Unit",
            ],
            ipc_classes_to_monitor=["G06N 20/00", "G06F 16/906", "G06Q 50/00"],
            alert_criteria=[
                "Nouveau dépôt combinant IA + droits humains + scoring composite",
                "Publication PCT dans G06N par déposant ONG/tech",
                "Dépôt USPTO par ex-employés Caelum Partners",
            ],
        ),
        PatentWatchConfig(
            patent_id="CAE-INV-002",
            title="Détection Précoce de Crises Humanitaires par Analyse Multi-Sources",
            search_keywords=[
                "humanitarian crisis early warning system",
                "conflict prediction machine learning",
                "crisis detection multi-source data fusion",
                "early warning humanitarian AI",
                "predictive crisis index satellite data",
                "anomaly detection humanitarian indicators",
            ],
            competitor_assignees=[
                "UN Global Pulse",
                "ACLED (Armed Conflict Location & Event Data)",
                "Crisis Group Digital",
                "Google.org Crisis AI",
                "Microsoft AI for Humanitarian Action",
            ],
            ipc_classes_to_monitor=["G06F 16/9535", "G08B 31/00", "G06N 5/04"],
            alert_criteria=[
                "Dépôt PCT combinant satellite + open-source intelligence + crise humanitaire",
                "Publication ONU sur système de détection précoce automatisé",
                "Dépôt par déposant lié au CERF ou OCHA",
            ],
        ),
        PatentWatchConfig(
            patent_id="CAE-INV-003",
            title="Apprentissage Fédéré Préservant la Vie Privée pour Données Terrain",
            search_keywords=[
                "federated learning differential privacy field data",
                "privacy-preserving machine learning humanitarian",
                "distributed learning offline NGO data",
                "federated learning low connectivity",
                "differential privacy aggregation field nodes",
                "secure multi-party computation humanitarian data",
            ],
            competitor_assignees=[
                "Google Research (TensorFlow Federated)",
                "Apple Inc.",
                "OpenMined",
                "Flower Labs",
                "Meta AI Research",
            ],
            ipc_classes_to_monitor=["G06N 20/00", "H04L 9/32", "G06F 21/62"],
            alert_criteria=[
                "Dépôt combinant federated learning + données humanitaires",
                "Publication sur apprentissage fédéré offline-first",
                "Dépôt par NGO-tech combinant anonymisation + terrain",
            ],
        ),
        PatentWatchConfig(
            patent_id="CAE-INV-004",
            title="Blockchain pour Preuves Irréfutables de Violations des Droits Humains",
            search_keywords=[
                "blockchain evidence human rights violations",
                "cryptographic proof humanitarian court",
                "tamper-proof evidence collection ICC",
                "blockchain legal evidence chain custody",
                "immutable witness testimony blockchain",
                "digital forensics human rights court admissible",
            ],
            competitor_assignees=[
                "Hala Systems",
                "EvidenceAid Digital",
                "Syrian Archive / Mnemonic",
                "Witness.org Tech",
                "Ethereum Foundation (applied)",
            ],
            ipc_classes_to_monitor=["H04L 9/00", "G06F 21/64", "H04L 9/32"],
            alert_criteria=[
                "Dépôt combinant blockchain + preuve judiciaire internationale",
                "Publication sur compatibilité blockchain / greffe CPI",
                "Dépôt par cabinet juridique spécialisé droits humains",
            ],
        ),
        PatentWatchConfig(
            patent_id="CAE-INV-005",
            title="Plateforme ESG Conforme CSDDD pour Chaînes d'Approvisionnement",
            search_keywords=[
                "CSDDD compliance platform supply chain",
                "ESG due diligence supply chain AI",
                "corporate sustainability reporting directive automation",
                "supply chain human rights monitoring ESG",
                "tier-3 supplier screening AI platform",
                "forced labor detection supply chain software",
            ],
            competitor_assignees=[
                "SAP SE",
                "Oracle Corporation",
                "Sustainalytics (Morningstar)",
                "EcoVadis",
                "Sourcemap Inc.",
                "Trase / Global Canopy",
            ],
            ipc_classes_to_monitor=["G06Q 10/06", "G06Q 50/00", "G06Q 10/0833"],
            alert_criteria=[
                "ALERTE HAUTE — Dépôt par SAP/Oracle sur CSDDD compliance",
                "Dépôt combinant supply chain + human rights due diligence + AI",
                "Publication directive CSDDD sur plateforme technique officielle",
                "Tout dépôt EPO G06Q avec mots-clés CSDDD/CS3D/due diligence",
            ],
        ),
        PatentWatchConfig(
            patent_id="CAE-INV-006",
            title="Indice de Risque Conflit Armé par Fusion Multi-Modale de Données",
            search_keywords=[
                "armed conflict risk index multi-modal",
                "conflict risk satellite social media fusion",
                "predictive conflict analysis diplomatic",
                "armed conflict early warning composite index",
                "multi-source conflict prediction B2G",
                "conflict risk scoring government intelligence",
            ],
            competitor_assignees=[
                "Jane's Information Group (Janes)",
                "Control Risks Group",
                "Stratfor / RANE Network",
                "Verisk Maplecroft",
                "Crisis Group Digital",
            ],
            ipc_classes_to_monitor=["G06F 16/9535", "G06N 5/04", "G01S 13/00"],
            alert_criteria=[
                "Dépôt combinant satellite + NLP + indice de risque conflit",
                "Publication B2G sur système d'alerte gouvernementaux IA",
                "Dépôt par déposant lié OTAN/OCHA/UA sur prédiction conflits",
            ],
        ),
        PatentWatchConfig(
            patent_id="CAE-INV-007",
            title="Système de Surveillance Automatisée des Prisonniers Politiques",
            search_keywords=[
                "political prisoner monitoring automated",
                "arbitrary detention tracking AI",
                "prisoner of conscience database automated",
                "political detention pattern recognition",
                "human rights defender surveillance tool",
            ],
            competitor_assignees=[
                "Amnesty International Tech Lab",
                "Freedom House Digital",
                "Prisoner Alert (CSW)",
                "Frontline Defenders",
            ],
            ipc_classes_to_monitor=["G06F 16/906", "G06N 3/08", "G06F 40/56"],
            alert_criteria=[
                "Dépôt combinant détention + IA + ONG",
                "Publication sur base de données prisonniers politiques automatisée",
            ],
        ),
        PatentWatchConfig(
            patent_id="CAE-INV-008",
            title="Plateforme de Cartographie des Violations du Droit à l'Éducation",
            search_keywords=[
                "education access mapping violations AI",
                "right to education monitoring platform",
                "school access geospatial analysis human rights",
                "education deprivation index automated",
            ],
            competitor_assignees=[
                "UNESCO Digital",
                "Save the Children Tech",
                "Unicef Innovation",
                "Education Cannot Wait Digital",
            ],
            ipc_classes_to_monitor=["G06Q 50/20", "G06F 16/9535", "G06T 17/05"],
            alert_criteria=[
                "Dépôt combinant cartographie + droit à l'éducation + IA",
                "Publication UNESCO sur outil de monitoring scolaire automatisé",
            ],
        ),
        PatentWatchConfig(
            patent_id="CAE-INV-009",
            title="Outil d'Analyse Automatique des Discours de Haine Transfrontaliers",
            search_keywords=[
                "hate speech detection cross-border AI",
                "online hate speech multilingual NLP legal",
                "automated hate speech classification human rights",
                "digital services act compliance hate speech",
                "incitement detection transnational platform",
            ],
            competitor_assignees=[
                "Meta AI (content moderation)",
                "Google Jigsaw",
                "Hive Moderation",
                "Spectrum Labs",
                "ActiveFence",
            ],
            ipc_classes_to_monitor=["G06F 40/56", "G06N 3/08", "G06F 40/30"],
            alert_criteria=[
                "Dépôt combinant NLP + hate speech + droits humains + multi-langue",
                "Publication sur conformité DSA pour détection discours haineux",
                "Dépôt par plateforme sociale sur modération automatisée juridiquement alignée",
            ],
        ),
        PatentWatchConfig(
            patent_id="CAE-INV-010",
            title="Système de Scoring ESG Temps-Réel pour Investisseurs Impact",
            search_keywords=[
                "ESG real-time scoring impact investors",
                "ESG data aggregation Bloomberg API",
                "UN guiding principles ESG scoring automated",
                "impact investing ESG composite index real-time",
                "ESG due diligence investor platform AI",
            ],
            competitor_assignees=[
                "MSCI Inc.",
                "Sustainalytics",
                "Bloomberg ESG",
                "Refinitiv (LSEG)",
                "S&P Trucost",
                "RepRisk",
            ],
            ipc_classes_to_monitor=["G06Q 40/06", "G06N 20/00", "G06Q 10/06"],
            alert_criteria=[
                "Dépôt combinant ESG temps-réel + IA + Principes Directeurs ONU",
                "Publication par MSCI/Bloomberg sur scoring ESG automatisé",
                "Dépôt dans G06Q 40/06 par acteur fintech impact",
            ],
        ),
    ]


def run_patent_watch_agent():
    configs = build_patent_watch_configs()

    print("=" * 70)
    print("CAELUM PARTNERS — PATENT WATCH AGENT")
    print(f"Inventrice : Chaima Mhadbi · {date.today()}")
    print(f"Total brevets surveillés : {len(configs)}")
    print("=" * 70)

    for c in configs:
        print(
            f"\n{c.patent_id} — {len(c.search_keywords)} mots-clés, "
            f"{len(c.competitor_assignees)} concurrents surveillés"
        )
        print(f"  IPC : {', '.join(c.ipc_classes_to_monitor)}")
        print(f"  Alertes configurées : {len(c.alert_criteria)}")

    # Résumé
    total_keywords = sum(len(c.search_keywords) for c in configs)
    total_competitors = sum(len(c.competitor_assignees) for c in configs)
    total_alerts = sum(len(c.alert_criteria) for c in configs)

    print("\n" + "=" * 70)
    print(f"RÉSUMÉ SURVEILLANCE GLOBALE")
    print(f"  Mots-clés totaux    : {total_keywords}")
    print(f"  Concurrents suivis  : {total_competitors}")
    print(f"  Critères d'alerte   : {total_alerts}")
    print(f"  Bases à surveiller  : Espacenet · PatSnap · Google Patents · USPTO · WIPO")
    print("=" * 70)

    return configs


if __name__ == "__main__":
    run_patent_watch_agent()
