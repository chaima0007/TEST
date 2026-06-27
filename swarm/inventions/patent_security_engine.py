"""
Patent Security Engine — Caelum Partners SPRL
Inventrice : Chaima Mhadbi
Sécurisation du portefeuille de brevets G1-G4
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import date
import json


@dataclass
class PatentSecurityScore:
    patent_id: str
    title: str
    inventor: str = "Chaima Mhadbi"
    applicant: str = "Caelum Partners SPRL"
    generation: str = "G1"
    ipc_class: str = ""

    # Dimensions sécurité (0.0 à 1.0)
    claim_breadth_score: float = 0.0         # Largeur des revendications ×0.30
    prior_art_novelty_score: float = 0.0     # Solidité face à l'art antérieur ×0.30
    workaround_difficulty_score: float = 0.0 # Difficulté de contournement ×0.25
    international_coverage_score: float = 0.0 # Couverture internationale ×0.15

    composite_security_score: float = field(init=False)
    security_level: str = field(init=False)

    protective_measures: List[str] = field(default_factory=list)
    filing_recommendations: List[str] = field(default_factory=list)
    defensive_publications: List[str] = field(default_factory=list)
    continuation_strategy: str = ""
    trade_secret_aspects: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.composite_security_score = round(
            self.claim_breadth_score * 0.30
            + self.prior_art_novelty_score * 0.30
            + self.workaround_difficulty_score * 0.25
            + self.international_coverage_score * 0.15,
            3
        )
        if self.composite_security_score >= 0.80:
            self.security_level = "FORTEMENT PROTÉGÉ"
        elif self.composite_security_score >= 0.65:
            self.security_level = "BIEN PROTÉGÉ"
        elif self.composite_security_score >= 0.50:
            self.security_level = "PROTECTION MODÉRÉE"
        else:
            self.security_level = "PROTECTION INSUFFISANTE"

    def to_security_report(self) -> str:
        lines = [
            f"# RAPPORT DE SÉCURITÉ — {self.patent_id}",
            f"## {self.title}",
            f"",
            f"**Inventrice :** {self.inventor}",
            f"**Déposant :** {self.applicant}",
            f"**Génération :** {self.generation} | **IPC :** {self.ipc_class}",
            f"**Niveau de protection :** {self.security_level} ({self.composite_security_score*100:.1f}/100)",
            f"",
            f"## Scores de sécurité",
            f"| Dimension | Score | Poids |",
            f"|-----------|-------|-------|",
            f"| Largeur des revendications | {self.claim_breadth_score*100:.0f}% | ×0.30 |",
            f"| Solidité anti-art antérieur | {self.prior_art_novelty_score*100:.0f}% | ×0.30 |",
            f"| Difficulté de contournement | {self.workaround_difficulty_score*100:.0f}% | ×0.25 |",
            f"| Couverture internationale | {self.international_coverage_score*100:.0f}% | ×0.15 |",
            f"",
            f"## Mesures de protection recommandées",
        ]
        for m in self.protective_measures:
            lines.append(f"- {m}")
        lines += [
            f"",
            f"## Stratégie de dépôt",
        ]
        for r in self.filing_recommendations:
            lines.append(f"- {r}")
        lines += [
            f"",
            f"## Publications défensives",
        ]
        for d in self.defensive_publications:
            lines.append(f"- {d}")
        lines += [
            f"",
            f"## Stratégie de continuation",
            f"{self.continuation_strategy}",
            f"",
            f"## Aspects protégés comme secrets commerciaux",
        ]
        for t in self.trade_secret_aspects:
            lines.append(f"- {t}")
        lines.append(
            f"\n---\n*Rapport généré automatiquement — Caelum Partners SPRL · {date.today()}*"
        )
        return "\n".join(lines)


def build_patent_security_portfolio() -> List[PatentSecurityScore]:
    patents = [
        # ── G1 ──────────────────────────────────────────────────────────────
        PatentSecurityScore(
            patent_id="CAE-INV-001",
            title="Système de Scoring IA pour l'Évaluation des Droits Humains",
            generation="G1",
            ipc_class="G06N 20/00 · G06F 16/906",
            claim_breadth_score=0.72,
            prior_art_novelty_score=0.78,
            workaround_difficulty_score=0.68,
            international_coverage_score=0.40,
            protective_measures=[
                "Déposer continuation avec revendications méthode + système",
                "Étendre aux applications mobiles et edge computing",
                "Couvrir les variantes de pondération multi-domaines",
            ],
            filing_recommendations=[
                "Priorité EPO + demande PCT 12 mois",
                "Phase nationale: BE, FR, DE, GB, US, CN, IN",
                "Dépôt provisoire USPTO immédiat ($350)",
            ],
            defensive_publications=[
                "Publication préventive sur variantes algorithmes open-source",
                "Whitepaper technique avant concurrence",
            ],
            continuation_strategy=(
                "Déposer 3 continuations : (1) variante temps-réel, "
                "(2) version edge/mobile, (3) intégration API tiers"
            ),
            trade_secret_aspects=[
                "Pondération exacte des 47 sous-indicateurs",
                "Algorithme de normalisation inter-pays",
                "Formule d'agrégation temporelle",
            ],
        ),
        PatentSecurityScore(
            patent_id="CAE-INV-002",
            title="Détection Précoce de Crises Humanitaires par Analyse Multi-Sources",
            generation="G1",
            ipc_class="G06F 16/9535 · G08B 31/00",
            claim_breadth_score=0.75,
            prior_art_novelty_score=0.80,
            workaround_difficulty_score=0.71,
            international_coverage_score=0.42,
            protective_measures=[
                "Breveter séparément le module de corrélation géographique",
                "Protéger l'algorithme de détection d'anomalies",
                "Couvrir l'interface ONG/gouvernements",
            ],
            filing_recommendations=[
                "PCT prioritaire (150 pays, 30 mois)",
                "Cibler US, EU, CH (siège ONU), AU",
            ],
            defensive_publications=[
                "Publier benchmark comparatif vs systèmes existants",
            ],
            continuation_strategy=(
                "Continuation sur module temps-réel et API alertes push"
            ),
            trade_secret_aspects=[
                "Seuils d'alerte calibrés sur données historiques 2010-2025",
                "Modèle de corrélation géopolitique propriétaire",
            ],
        ),
        # ── G2 ──────────────────────────────────────────────────────────────
        PatentSecurityScore(
            patent_id="CAE-INV-003",
            title="Apprentissage Fédéré Préservant la Vie Privée pour Données Terrain",
            generation="G2",
            ipc_class="G06N 20/00 · H04L 9/32",
            claim_breadth_score=0.80,
            prior_art_novelty_score=0.85,
            workaround_difficulty_score=0.78,
            international_coverage_score=0.50,
            protective_measures=[
                "Breveter le protocole d'agrégation préservant la vie privée",
                "Protéger l'architecture nœuds terrain",
                "Revendiquer l'anonymisation différentielle adaptée",
            ],
            filing_recommendations=[
                "EPO + USPTO en parallèle",
                "Certification ENISA pour EU AI Act 2024",
            ],
            defensive_publications=[
                "Publier avant-brevet sur technique d'anonymisation générique",
            ],
            continuation_strategy=(
                "Continuation sur version offline-first et synchronisation asynchrone"
            ),
            trade_secret_aspects=[
                "Paramètres d'epsilon de confidentialité différentielle",
                "Topologie réseau de nœuds optimisée",
            ],
        ),
        PatentSecurityScore(
            patent_id="CAE-INV-004",
            title="Blockchain pour Preuves Irréfutables de Violations des Droits Humains",
            generation="G2",
            ipc_class="H04L 9/00 · G06F 21/64",
            claim_breadth_score=0.82,
            prior_art_novelty_score=0.88,
            workaround_difficulty_score=0.82,
            international_coverage_score=0.55,
            protective_measures=[
                "Protéger le protocole de scellement cryptographique",
                "Breveter l'horodatage certifié pour usage judiciaire",
                "Couvrir l'interface CPI et tribunaux internationaux",
            ],
            filing_recommendations=[
                "Dépôt PCT urgent — fort potentiel concurrentiel",
                "Phase nationale: US (USPTO), EU (EPO), CH, NL, UK",
            ],
            defensive_publications=[
                "Publier sur les limites des blockchains publiques pour preuves judiciaires",
            ],
            continuation_strategy=(
                "Continuation CPI + continuation arbitrage commercial international"
            ),
            trade_secret_aspects=[
                "Format de preuve compatible greffe CPI",
                "Algorithme de hachage multi-couches propriétaire",
            ],
        ),
        # ── G3 ──────────────────────────────────────────────────────────────
        PatentSecurityScore(
            patent_id="CAE-INV-005",
            title="Plateforme ESG Conforme CSDDD pour Chaînes d'Approvisionnement",
            generation="G3",
            ipc_class="G06Q 10/06 · G06Q 50/00",
            claim_breadth_score=0.88,
            prior_art_novelty_score=0.90,
            workaround_difficulty_score=0.85,
            international_coverage_score=0.70,
            protective_measures=[
                "Protéger urgent avant directive CSDDD 2026",
                "Breveter interface ERP (SAP/Oracle)",
                "Couvrir le module de rapport automatisé conforme",
            ],
            filing_recommendations=[
                "DÉPÔT IMMÉDIAT — timing critique directive EU 2026",
                "EPO + USPTO + CN simultanément",
                "PCT sans attendre",
            ],
            defensive_publications=[
                "Aucune publication défensive — maintenir avantage compétitif maximum",
            ],
            continuation_strategy=(
                "Continuation sur modules sectoriels (textile, mining, agriculture)"
            ),
            trade_secret_aspects=[
                "Méthodologie de scoring fournisseurs tier-3",
                "Algorithme de détection de violations cachées dans chaînes d'approvisionnement",
            ],
        ),
        PatentSecurityScore(
            patent_id="CAE-INV-006",
            title="Indice de Risque Conflit Armé par Fusion Multi-Modale de Données",
            generation="G3",
            ipc_class="G06F 16/9535 · G06N 5/04",
            claim_breadth_score=0.90,
            prior_art_novelty_score=0.88,
            workaround_difficulty_score=0.86,
            international_coverage_score=0.65,
            protective_measures=[
                "Protéger l'indice composite multi-modal",
                "Breveter la fusion données satellite+terrain+médias",
                "Couvrir le module de recommandation diplomatique",
            ],
            filing_recommendations=[
                "PCT prioritaire — fort potentiel B2G (gouvernements, ONU)",
                "Phase nationale: US, EU, CH (OCHA), AU, JP",
            ],
            defensive_publications=[
                "Publier framework général d'indice de risque (sans paramètres propriétaires)",
            ],
            continuation_strategy=(
                "Continuation sur module prédictif 6-18 mois et alertes automatiques OCHA"
            ),
            trade_secret_aspects=[
                "Matrice de pondération des 23 variables de risque",
                "Calibration sur 847 conflits historiques 1990-2025",
            ],
        ),
        # ── G4 ──────────────────────────────────────────────────────────────
        PatentSecurityScore(
            patent_id="CAE-INV-007",
            title="Système de Surveillance Automatisée des Prisonniers Politiques",
            generation="G4",
            ipc_class="G06F 16/906 · G06N 3/08",
            claim_breadth_score=0.74,
            prior_art_novelty_score=0.78,
            workaround_difficulty_score=0.72,
            international_coverage_score=0.38,
            protective_measures=[
                "Breveter le module d'identification des schémas de détention",
                "Protéger l'interface de dépôt de plainte numérique",
                "Couvrir l'agrégation multi-sources journalistes + ONG",
            ],
            filing_recommendations=[
                "EPO prioritaire + USPTO",
                "Phase nationale: BE, FR, DE, GB, US",
                "Dépôt provisoire USPTO ($350) pour sécuriser date",
            ],
            defensive_publications=[
                "Publier méthodologie générale de classification des détenus politiques",
            ],
            continuation_strategy=(
                "Continuation sur module alertes automatiques aux rapporteurs spéciaux ONU"
            ),
            trade_secret_aspects=[
                "Critères de classification prisonniers politiques (15 indicateurs)",
                "Réseau de sources terrain anonymisées",
            ],
        ),
        PatentSecurityScore(
            patent_id="CAE-INV-008",
            title="Plateforme de Cartographie des Violations du Droit à l'Éducation",
            generation="G4",
            ipc_class="G06Q 50/20 · G06F 16/9535",
            claim_breadth_score=0.70,
            prior_art_novelty_score=0.75,
            workaround_difficulty_score=0.70,
            international_coverage_score=0.42,
            protective_measures=[
                "Protéger le modèle de scoring d'accessibilité scolaire",
                "Breveter la méthode de géolocalisation des zones non couvertes",
                "Couvrir le module de recommandation politique publique",
            ],
            filing_recommendations=[
                "PCT recommandé — marché global éducation",
                "Phase nationale: US, EU, IN, ZA, BR",
            ],
            defensive_publications=[
                "Publier index mondial open-data accès éducation (sans moteur propriétaire)",
            ],
            continuation_strategy=(
                "Continuation sur intégration données UNESCO + module prédictif dropout"
            ),
            trade_secret_aspects=[
                "Matrice de pondération des 18 indicateurs d'accès éducatif",
                "Algorithme de priorisation des zones d'intervention",
            ],
        ),
        PatentSecurityScore(
            patent_id="CAE-INV-009",
            title="Outil d'Analyse Automatique des Discours de Haine Transfrontaliers",
            generation="G4",
            ipc_class="G06F 40/56 · G06N 3/08",
            claim_breadth_score=0.76,
            prior_art_novelty_score=0.80,
            workaround_difficulty_score=0.73,
            international_coverage_score=0.45,
            protective_measures=[
                "Breveter le modèle NLP multi-langue spécialisé droits humains",
                "Protéger la taxonomie des discours de haine juridiquement alignée",
                "Couvrir l'interface plateformes sociales (API Meta/X/TikTok)",
            ],
            filing_recommendations=[
                "EPO + USPTO simultanément",
                "Phase nationale: BE, FR, DE, US, CA",
                "Surveiller Digital Services Act EU pour timing optimal",
            ],
            defensive_publications=[
                "Publier taxonomie générale open-source avant dépôt concurrent",
            ],
            continuation_strategy=(
                "Continuation sur module détection coordinations inautentiques + deepfakes"
            ),
            trade_secret_aspects=[
                "Corpus d'entraînement annoté 2.3M exemples multi-langue",
                "Seuils de détection par juridiction et cadre légal",
            ],
        ),
        PatentSecurityScore(
            patent_id="CAE-INV-010",
            title="Système de Scoring ESG Temps-Réel pour Investisseurs Impact",
            generation="G4",
            ipc_class="G06Q 40/06 · G06N 20/00",
            claim_breadth_score=0.78,
            prior_art_novelty_score=0.82,
            workaround_difficulty_score=0.75,
            international_coverage_score=0.50,
            protective_measures=[
                "Breveter l'agrégation temps-réel multi-sources ESG",
                "Protéger le modèle de scoring aligné Principes Directeurs ONU",
                "Couvrir l'interface Bloomberg/Refinitiv/MSCI",
            ],
            filing_recommendations=[
                "PCT recommandé — marché financier global",
                "Phase nationale: US (NYSE/NASDAQ zone), EU, UK, CH, JP, SG",
            ],
            defensive_publications=[
                "Publier framework méthodologique ESG open-source (sans algorithme propriétaire)",
            ],
            continuation_strategy=(
                "Continuation sur module stress-test ESG et simulation de portefeuille"
            ),
            trade_secret_aspects=[
                "Pondération des 31 métriques ESG propriétaires",
                "Algorithme d'ajustement sectoriel et géographique",
            ],
        ),
    ]
    return patents


def run_patent_security_engine() -> Dict:
    patents = build_patent_security_portfolio()
    avg_security = sum(p.composite_security_score for p in patents) / len(patents)

    print("=" * 70)
    print("CAELUM PARTNERS — RAPPORT SÉCURITÉ PORTEFEUILLE BREVETS")
    print(f"Inventrice : Chaima Mhadbi · {date.today()}")
    print("=" * 70)

    for p in patents:
        print(
            f"\n{p.patent_id} [{p.generation}] | {p.security_level} | "
            f"{p.composite_security_score*100:.1f}/100"
        )
        print(f"  → {p.title[:60]}...")

    print(f"\nScore sécurité moyen du portefeuille : {avg_security*100:.1f}/100")

    # Alertes critiques
    urgent = [p for p in patents if p.patent_id in ["CAE-INV-005", "CAE-INV-006"]]
    print("\n⚠ DÉPÔTS URGENTS (risque timing marché) :")
    for p in urgent:
        print(f"  → {p.patent_id} : {p.title[:50]}...")

    # Génération des rapports individuels
    import os
    os.makedirs("docs/inventions/patents/security", exist_ok=True)
    for p in patents:
        report_path = f"docs/inventions/patents/security/{p.patent_id}-security.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(p.to_security_report())
    print(f"\n✓ {len(patents)} rapports individuels générés dans docs/inventions/patents/security/")

    return {"patents": patents, "avg_security": avg_security}


if __name__ == "__main__":
    run_patent_security_engine()
