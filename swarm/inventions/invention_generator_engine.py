"""
Caelum Partners — Invention Generator Engine
Inventrice : Chaima Mhadbi · Bruxelles · 2026

Système de génération d'inventions qui s'engendrent logiquement les unes les autres.
Chaque génération d'inventions s'appuie sur la précédente — arbre généalogique brevetable.

Domaines couverts :
  G1 (Fondation)   → Moteurs IA droits humains, scoring automatisé
  G2 (Application) → Dérivés de G1 : privacy, mobile, blockchain
  G3 (Hybridation) → Combinaisons cross-domaine G1+G2
  G4 (Émergence)   → Inventions autonomes déclenchées par données G3
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import statistics
import json
from datetime import date


@dataclass
class Invention:
    invention_id: str
    title: str
    inventor: str = "Chaima Mhadbi"
    applicant: str = "Caelum Partners SPRL"
    address: str = "Bruxelles, Belgique"
    filing_date: str = "2026-06-21"
    generation: int = 1
    parent_ids: List[str] = field(default_factory=list)
    technical_field: str = ""
    problem_solved: str = ""
    solution_summary: str = ""
    independent_claims: List[str] = field(default_factory=list)
    dependent_claims: List[str] = field(default_factory=list)
    prior_art: List[str] = field(default_factory=list)
    child_invention_seeds: List[str] = field(default_factory=list)
    novelty_score: float = 0.0
    utility_score: float = 0.0
    inventive_step_score: float = 0.0
    composite_patentability: float = field(init=False)
    status: str = "DRAFT"
    ipc_class: str = ""

    def __post_init__(self):
        self.composite_patentability = round(
            (self.novelty_score * 0.40
             + self.inventive_step_score * 0.35
             + self.utility_score * 0.25),
            2,
        )

    def to_patent_draft(self) -> str:
        claims_text = "\n".join(
            f"  {i+1}. {c}" for i, c in enumerate(self.independent_claims)
        )
        dep_claims_text = "\n".join(
            f"  {len(self.independent_claims)+i+1}. {c}"
            for i, c in enumerate(self.dependent_claims)
        )
        parents_text = (
            f"Perfectionnement de : {', '.join(self.parent_ids)}"
            if self.parent_ids else "Invention de premier rang (fondation)"
        )
        return f"""
DEMANDE DE BREVET
═══════════════════════════════════════════════════════════════

Référence interne : {self.invention_id}
Titre : {self.title}
Inventrice : {self.inventor}
Déposant : {self.applicant}
Adresse : {self.address}
Date de priorité : {self.filing_date}
Classification IPC : {self.ipc_class}
Génération : G{self.generation} — {parents_text}
Statut : {self.status}
Score brevetabilité : {self.composite_patentability}/10

───────────────────────────────────────────────────────────────
DOMAINE TECHNIQUE
───────────────────────────────────────────────────────────────
{self.technical_field}

───────────────────────────────────────────────────────────────
ÉTAT DE LA TECHNIQUE (ART ANTÉRIEUR)
───────────────────────────────────────────────────────────────
{chr(10).join(f'- {p}' for p in self.prior_art)}

───────────────────────────────────────────────────────────────
PROBLÈME TECHNIQUE RÉSOLU
───────────────────────────────────────────────────────────────
{self.problem_solved}

───────────────────────────────────────────────────────────────
RÉSUMÉ DE L'INVENTION
───────────────────────────────────────────────────────────────
{self.solution_summary}

───────────────────────────────────────────────────────────────
REVENDICATIONS
───────────────────────────────────────────────────────────────
Revendications indépendantes :
{claims_text}

Revendications dépendantes :
{dep_claims_text}

───────────────────────────────────────────────────────────────
INVENTIONS DÉRIVÉES POTENTIELLES (G{self.generation + 1})
───────────────────────────────────────────────────────────────
{chr(10).join(f'→ {s}' for s in self.child_invention_seeds)}

───────────────────────────────────────────────────────────────
SCORES DE BREVETABILITÉ
───────────────────────────────────────────────────────────────
Nouveauté (Art. 54 CBE) : {self.novelty_score}/10
Activité inventive (Art. 56 CBE) : {self.inventive_step_score}/10
Application industrielle (Art. 57 CBE) : {self.utility_score}/10
Score composite : {self.composite_patentability}/10

═══════════════════════════════════════════════════════════════
Document généré par Caelum Partners Invention Engine v1.0
© 2026 Chaima Mhadbi — Tous droits réservés
"""


def build_invention_portfolio() -> List[Invention]:
    inventions = [

        # ═══════════════ GÉNÉRATION 1 — FONDATION ═══════════════

        Invention(
            invention_id="CAE-INV-001",
            title="Système de Scoring Automatisé des Violations de Droits Humains par Intelligence Artificielle Multi-Dimensionnelle",
            generation=1,
            parent_ids=[],
            ipc_class="G06N 20/00 · G06F 40/56",
            technical_field=(
                "Intelligence artificielle appliquée à l'analyse et la quantification "
                "automatisée des violations de droits humains à l'échelle mondiale. "
                "Traitement du langage naturel, apprentissage automatique supervisé, "
                "et systèmes d'indexation composite multi-critères."
            ),
            problem_solved=(
                "L'analyse des violations de droits humains repose actuellement sur "
                "des processus manuels chronophages, subjectifs, et non-comparables entre pays. "
                "Aucun système automatisé ne produit des scores composites reproductibles, "
                "pondérés et comparables sur 100+ domaines thématiques en temps réel."
            ),
            solution_summary=(
                "Système informatique comprenant : (a) un moteur d'extraction de signaux "
                "depuis sources documentaires (rapports ONU, ONG, médias) via NLP, "
                "(b) une architecture de scoring composite à 4 sous-dimensions pondérées "
                "(w1=0.30, w2=0.25, w3=0.25, w4=0.20), (c) un module de normalisation "
                "sur échelle 0-100 avec seuils de criticité automatiques, "
                "(d) une API temps-réel exposant les indices par domaine et entité."
            ),
            independent_claims=[
                "Système informatique de scoring automatisé des violations de droits humains comprenant : "
                "un module d'ingestion de données documentaires multi-sources ; "
                "un moteur NLP d'extraction d'entités et d'événements liés aux droits humains ; "
                "un calculateur de score composite à pondération différentielle (0.30/0.25/0.25/0.20) ; "
                "un classificateur de niveau de risque à seuils prédéfinis (critique/élevé/modéré/faible) ; "
                "une interface de programmation (API) exposant les résultats en temps réel.",

                "Procédé de génération d'un indice de violation de droits humains comprenant les étapes : "
                "collecte automatisée de documents depuis sources humanitaires ; "
                "extraction de signaux factuels par traitement du langage naturel ; "
                "calcul d'un score composite selon la formule S = Σ(wi × si) où Σwi = 1 ; "
                "classification du niveau de risque selon des seuils prédéterminés ; "
                "exposition de l'indice via une interface standardisée.",
            ],
            dependent_claims=[
                "Système selon la revendication 1, dans lequel le module NLP utilise des modèles "
                "de langue entraînés spécifiquement sur corpus de droits humains (HRW, Amnesty, ONU).",
                "Système selon la revendication 1, dans lequel les seuils de criticité sont : "
                "critique ≥ 60, élevé ≥ 40, modéré ≥ 20, faible < 20, sur échelle 0-100.",
                "Procédé selon la revendication 2, dans lequel le score est mis à jour "
                "automatiquement avec revalidation toutes les 30 secondes.",
                "Système selon la revendication 1, comprenant en outre un module d'alerte "
                "automatique lorsque le score dépasse le seuil critique.",
            ],
            prior_art=[
                "Freedom House Freedom in the World Index (2006) — scoring binaire non-composite",
                "V-Dem Dataset (2016) — données électorales, non centré droits humains",
                "Human Rights Measurement Initiative HRMI (2017) — questionnaires manuels",
                "Amnesty International Urgent Actions (1973) — alertes manuelles non-scorées",
                "Global Slavery Index (2013) — domaine unique (esclavage), non multi-thématique",
            ],
            child_invention_seeds=[
                "CAE-INV-003 : Version fédérée préservant la vie privée des sources terrain",
                "CAE-INV-004 : Déploiement mobile hors-ligne pour zones sans internet",
                "CAE-INV-007 : Intégration blockchain pour preuve d'intégrité des scores",
            ],
            novelty_score=8.7,
            utility_score=9.5,
            inventive_step_score=8.2,
        ),

        Invention(
            invention_id="CAE-INV-002",
            title="Moteur de Détection Précoce des Crises de Droits Humains par Analyse Prédictive Temporelle",
            generation=1,
            parent_ids=[],
            ipc_class="G06N 5/04 · G06Q 10/04",
            technical_field=(
                "Systèmes d'alerte précoce basés sur l'analyse de séries temporelles "
                "de scores de droits humains. Modèles prédictifs pour anticiper les "
                "dégradations de situations humanitaires avant qu'elles ne deviennent crises."
            ),
            problem_solved=(
                "Les crises humanitaires (génocides, nettoyages ethniques, répressions massives) "
                "présentent des signaux précurseurs documentés mais non-détectés automatiquement. "
                "L'absence de système d'alerte précoce basé sur données quantitatives cause "
                "des retards d'intervention diplomatique et humanitaire évitables."
            ),
            solution_summary=(
                "Système prédictif analysant l'évolution temporelle des scores de violations "
                "sur 90 jours glissants. Détecte les inflexions statistiquement significatives "
                "(Δscore > 2σ sur 30 jours), corrèle avec facteurs contextuels (élections, "
                "conflits voisins, indicateurs économiques), et génère des alertes précoces "
                "graduées avec probabilité d'escalade estimée."
            ),
            independent_claims=[
                "Système de détection précoce de crises humanitaires comprenant : "
                "une base de données de séries temporelles de scores de violations (>90 jours) ; "
                "un moteur de détection d'anomalies statistiques (inflexions ≥ 2 écarts-types) ; "
                "un module de corrélation avec facteurs contextuels externes ; "
                "un générateur d'alertes précoces graduées (surveillance/alerte/urgence) ; "
                "un tableau de bord temps-réel avec probabilité d'escalade estimée.",

                "Procédé d'alerte précoce humanitaire comprenant : "
                "acquisition continue de scores de violations sur fenêtre glissante ; "
                "détection d'inflexions statistiquement significatives (Δ > 2σ/30j) ; "
                "calcul de probabilité d'escalade par modèle de régression logistique ; "
                "émission d'alerte graduée avec recommandation d'action.",
            ],
            dependent_claims=[
                "Système selon la revendication 1, dans lequel la fenêtre temporelle "
                "d'analyse est configurable entre 30 et 365 jours.",
                "Système selon la revendication 1, comprenant un module de backtesting "
                "sur crises historiques documentées pour validation du modèle.",
                "Procédé selon la revendication 2, dans lequel le modèle prédictif "
                "intègre des corrélations avec indicateurs de conflits voisins.",
            ],
            prior_art=[
                "ACLED (Armed Conflict Location & Event Data) — données binaires, non-prédictif",
                "Early Warning Project (USHMM) — focus génocide uniquement, manuel",
                "GDELT Project — événements média, non centré droits humains",
                "Uppsala Conflict Data Program — conflits armés, rétrospectif",
            ],
            child_invention_seeds=[
                "CAE-INV-005 : Alertes automatiques vers ONG et gouvernements via API push",
                "CAE-INV-008 : Version multi-pays avec corrélation régionale",
            ],
            novelty_score=8.5,
            utility_score=9.3,
            inventive_step_score=8.6,
        ),

        # ═══════════════ GÉNÉRATION 2 — APPLICATIONS ═══════════════

        Invention(
            invention_id="CAE-INV-003",
            title="Architecture d'Apprentissage Fédéré pour Scoring de Droits Humains Préservant l'Anonymat des Sources Terrain",
            generation=2,
            parent_ids=["CAE-INV-001"],
            ipc_class="G06N 20/00 · H04L 9/32",
            technical_field=(
                "Apprentissage automatique fédéré appliqué aux données sensibles de "
                "violations de droits humains. Protocoles cryptographiques préservant "
                "l'anonymat des sources dans les zones de conflit."
            ),
            problem_solved=(
                "Le système CAE-INV-001 requiert la centralisation des données sources, "
                "exposant les informateurs et défenseurs des droits humains à des risques "
                "de représailles. Les sources terrain en zones de conflit ne peuvent "
                "contribuer si leur identité ou localisation peut être déduite."
            ),
            solution_summary=(
                "Architecture fédérée où chaque nœud (ONG, bureau terrain) entraîne "
                "localement un modèle partiel sur ses données sensibles. Seuls les "
                "gradients agrégés (jamais les données brutes) transitent sur le réseau, "
                "chiffrés par protocole de confidentialité différentielle (ε-DP). "
                "Le modèle global est reconstruit par agrégation sécurisée (SecAgg) "
                "sans que le serveur central n'accède aux données individuelles."
            ),
            independent_claims=[
                "Architecture d'apprentissage fédéré pour droits humains comprenant : "
                "des nœuds clients (bureaux terrain) entraînant des modèles locaux "
                "sur données sensibles non-partagées ; "
                "un protocole de confidentialité différentielle (ε-DP, ε ≤ 1.0) "
                "appliqué aux gradients avant transmission ; "
                "un serveur d'agrégation sécurisée (SecAgg) reconstruisant le modèle global "
                "sans accès aux données individuelles des nœuds ; "
                "un mécanisme de vérification d'intégrité des contributions par signature cryptographique.",
            ],
            dependent_claims=[
                "Architecture selon la revendication 1, dans laquelle le paramètre ε "
                "de confidentialité différentielle est adaptatif selon la sensibilité "
                "géographique du nœud client (zones de conflit : ε ≤ 0.1).",
                "Architecture selon la revendication 1, comprenant un module de détection "
                "de contributions malveillantes (Byzantine fault tolerance).",
                "Architecture selon la revendication 1, dans laquelle les nœuds clients "
                "peuvent opérer en mode asynchrone pour zones à connectivité limitée.",
            ],
            prior_art=[
                "McMahan et al. 'Communication-Efficient Learning' (2017) — FL générique",
                "Dwork 'Differential Privacy' (2006) — DP théorique, non appliqué HRW",
                "Bonawitz et al. 'SecAgg' (2017) — agrégation sécurisée générique",
            ],
            child_invention_seeds=[
                "CAE-INV-006 : Nœud mobile offline-first pour agents terrain sans connexion",
                "CAE-INV-009 : Certification ISO 27001 adaptée aux données de droits humains",
            ],
            novelty_score=9.1,
            utility_score=8.8,
            inventive_step_score=9.0,
        ),

        Invention(
            invention_id="CAE-INV-004",
            title="Système de Collecte de Preuves de Violations par Blockchain Immuable avec Horodatage Certifié",
            generation=2,
            parent_ids=["CAE-INV-001"],
            ipc_class="H04L 9/32 · G06F 21/64",
            technical_field=(
                "Application de la technologie blockchain à la préservation et "
                "certification de preuves de violations de droits humains. "
                "Horodatage cryptographique, chaîne de custody numérique, "
                "admissibilité devant les juridictions internationales."
            ),
            problem_solved=(
                "Les preuves numériques de violations (photos, vidéos, témoignages) "
                "sont facilement falsifiables, supprimables et leur authenticité est "
                "difficile à établir devant les cours internationales (CPI, CEDH). "
                "Aucun système ne garantit l'intégrité et la chaîne de custody "
                "des preuves depuis leur collecte jusqu'au procès."
            ),
            solution_summary=(
                "Système de preuve blockchain comprenant : (a) un client mobile "
                "calculant l'empreinte cryptographique (SHA-3) de chaque élément "
                "de preuve au moment de la collecte, (b) inscription immédiate sur "
                "blockchain publique (Ethereum) créant un horodatage incontestable, "
                "(c) chiffrement du contenu sur serveur sécurisé (IPFS chiffré), "
                "(d) génération d'un rapport de custody automatique admissible "
                "devant la CPI selon les standards de l'INTERPOL."
            ),
            independent_claims=[
                "Système de certification blockchain de preuves humanitaires comprenant : "
                "un client mobile calculant l'empreinte SHA-3 de données probantes ; "
                "un module d'inscription sur registre distribué immuable "
                "avec horodatage certifié (±1 seconde) ; "
                "un système de stockage chiffré du contenu probant (IPFS/AES-256) ; "
                "un générateur de rapport de chaîne de custody au format admissible CPI/CEDH ; "
                "un mécanisme de vérification d'intégrité ultérieure par recalcul d'empreinte.",

                "Procédé de préservation de preuves de violations de droits humains comprenant : "
                "capture de l'élément probant avec métadonnées contextuelles (GPS, timestamp) ; "
                "calcul d'empreinte cryptographique irréversible (SHA-3 256 bits) ; "
                "inscription de l'empreinte sur blockchain publique ; "
                "chiffrement et stockage sécurisé du contenu ; "
                "génération d'identifiant unique de preuve (UUID v4 + hash chaîne).",
            ],
            dependent_claims=[
                "Système selon la revendication 1, dans lequel les métadonnées GPS "
                "sont également inscrites sur blockchain pour preuve de géolocalisation.",
                "Procédé selon la revendication 2, dans lequel le client mobile "
                "fonctionne en mode hors-ligne avec synchronisation blockchain différée.",
                "Système selon la revendication 1, comprenant un module de signature "
                "électronique du collecteur de preuve (identité pseudonymisée).",
            ],
            prior_art=[
                "EyeWitness to Atrocities (2015) — application mobile, pas de blockchain",
                "Hala Systems (2018) — alerte frappes aériennes, non-custody chain",
                "Syrian Archive (2014) — préservation vidéos, centralisation vulnérable",
            ],
            child_invention_seeds=[
                "CAE-INV-007 : Intégration directe dans le scoring CAE-INV-001 pour pondération preuves",
                "CAE-INV-010 : Interface directe avec greffe de la CPI pour dépôt automatisé",
            ],
            novelty_score=8.9,
            utility_score=9.6,
            inventive_step_score=8.7,
        ),

        # ═══════════════ GÉNÉRATION 3 — HYBRIDATION ═══════════════

        Invention(
            invention_id="CAE-INV-005",
            title="Plateforme ESG Droits Humains pour Due Diligence Automatisée des Chaînes d'Approvisionnement selon Directive CSDDD",
            generation=3,
            parent_ids=["CAE-INV-001", "CAE-INV-002"],
            ipc_class="G06Q 10/06 · G06N 20/00",
            technical_field=(
                "Système d'automatisation de la due diligence en droits humains "
                "pour les entreprises soumises à la Directive européenne CSDDD (2024). "
                "Scoring automatisé des risques fournisseurs, génération de rapports "
                "conformes CSRD/GRI, alertes réglementaires en temps réel."
            ),
            problem_solved=(
                "La Directive CSDDD impose aux entreprises +1000 salariés un devoir "
                "de vigilance sur leurs chaînes d'approvisionnement. L'analyse manuelle "
                "de milliers de fournisseurs dans 100+ pays est impossible. "
                "Aucun outil n'automatise ce processus en intégrant des scores "
                "pays/secteur en temps réel conformes aux standards réglementaires."
            ),
            solution_summary=(
                "Plateforme SaaS combinant : (a) les scores pays de CAE-INV-001 "
                "filtrés par secteur d'activité, (b) les alertes précoces de CAE-INV-002 "
                "pour anticiper les dégradations fournisseurs, (c) un module de "
                "cartographie automatique de la chaîne d'approvisionnement par "
                "analyse des déclarations financières, (d) un générateur de rapports "
                "CSRD/CSDDD conformes aux standards GRI 412 (Droits humains) et "
                "UN Guiding Principles Reporting Framework."
            ),
            independent_claims=[
                "Plateforme de due diligence automatisée droits humains comprenant : "
                "un module d'ingestion de la liste de fournisseurs (ERP/CSV) ; "
                "un moteur de scoring pays×secteur en temps réel (dérivé CAE-INV-001) ; "
                "un système d'alerte précoce fournisseurs à risque (dérivé CAE-INV-002) ; "
                "un générateur de plans de vigilance conformes CSDDD Art. 5-8 ; "
                "un module de reporting automatique GRI 412 / UNGPRF.",
            ],
            dependent_claims=[
                "Plateforme selon la revendication 1, dans laquelle le scoring "
                "intègre des pondérations sectorielles (textile × 1.4, mines × 1.6, tech × 1.2).",
                "Plateforme selon la revendication 1, comprenant un module d'audit trail "
                "horodaté blockchain pour démonstration de diligence raisonnable.",
                "Plateforme selon la revendication 1, avec génération automatique "
                "de questionnaires fournisseurs adaptés au niveau de risque détecté.",
            ],
            prior_art=[
                "EcoVadis (2007) — évaluation manuelle fournisseurs, non temps-réel",
                "Sedex (2001) — questionnaires, pas de scoring droits humains automatisé",
                "Sustainalytics ESG Risk Ratings — scoring ESG général, non CSDDD-spécifique",
                "Ulula (2015) — collecte données terrain, non intégré chaîne approvisionnement",
            ],
            child_invention_seeds=[
                "CAE-INV-008 : Intégration API directe avec systèmes ERP (SAP, Oracle)",
                "CAE-INV-011 : Module de vérification automatique des certifications fournisseurs",
            ],
            novelty_score=9.2,
            utility_score=9.7,
            inventive_step_score=9.1,
        ),

        Invention(
            invention_id="CAE-INV-006",
            title="Système d'Indice de Risque de Conflit Armé Intégrant Droits Humains, Données Satellitaires et NLP Multilingue",
            generation=3,
            parent_ids=["CAE-INV-001", "CAE-INV-002", "CAE-INV-003"],
            ipc_class="G06N 20/00 · G06F 40/56 · G06T 7/00",
            technical_field=(
                "Système d'intelligence géopolitique intégrant scoring de droits humains, "
                "analyse d'images satellites (détection camps, destructions), et NLP "
                "multilingue (arabe, français, anglais, swahili, russe) pour construction "
                "d'un indice de risque de conflit armé préventif."
            ),
            problem_solved=(
                "Les indices de risque de conflit existants sont mono-sources, "
                "rétrospectifs, ou ne couvrent pas le nexus droits humains-conflit. "
                "L'intégration de sources hétérogènes (textes, images satellites, "
                "données économiques) en un score composite temps-réel n'existe pas."
            ),
            solution_summary=(
                "Architecture multi-modale combinant : flux de scoring droits humains "
                "(CAE-INV-001), analyse d'images satellites par CNN (détection camps "
                "de réfugiés, destructions d'infrastructures), NLP multilingue "
                "(extraction d'événements depuis sources locales non-anglophones), "
                "et apprentissage fédéré (CAE-INV-003) pour protection des sources. "
                "Produit un Conflict Risk Index (CRI) 0-100 mis à jour quotidiennement."
            ),
            independent_claims=[
                "Système de calcul d'indice de risque de conflit armé multi-modal comprenant : "
                "un module de scoring des droits humains (selon CAE-INV-001) ; "
                "un module d'analyse d'images satellitaires par réseau de neurones convolutif ; "
                "un moteur NLP multilingue extrayant événements depuis médias locaux ; "
                "un agrégateur pondéré produisant un Conflict Risk Index (CRI) 0-100 ; "
                "un système d'alerte géolocalisée par pays et région infranationale.",
            ],
            dependent_claims=[
                "Système selon la revendication 1, dans lequel l'analyse satellitaire "
                "détecte spécifiquement : camps de déplacés, destructions de bâtiments, "
                "mouvements de troupes, et corridors humanitaires bloqués.",
                "Système selon la revendication 1, dans lequel le NLP multilingue "
                "couvre a minima : arabe, français, anglais, swahili, russe, mandarin.",
                "Système selon la revendication 1, comprenant un mode de fonctionnement "
                "fédéré (CAE-INV-003) pour les sources en zones de conflit actif.",
            ],
            prior_art=[
                "ACLED conflict data — événements manuels, rétrospectif",
                "Planet Labs — images satellites, pas d'analyse droits humains",
                "GDELT — NLP anglais dominant, pas de scoring droits humains",
                "Crisis Group CrisisWatch — manuel, mensuel, pas de score composite",
            ],
            child_invention_seeds=[
                "CAE-INV-009 : Module de recommandation d'intervention diplomatique automatisé",
                "CAE-INV-012 : Intégration avec systèmes d'alerte ONU (OCHA ReliefWeb)",
            ],
            novelty_score=9.4,
            utility_score=9.5,
            inventive_step_score=9.3,
        ),
    ]

    return inventions


def run_invention_generator_engine():
    inventions = build_invention_portfolio()

    print("=" * 60)
    print("CAELUM PARTNERS — PORTEFEUILLE DE BREVETS")
    print("Inventrice : Chaima Mhadbi · Bruxelles · 2026")
    print("=" * 60)
    print(f"Total inventions : {len(inventions)}")

    by_gen = {}
    for inv in inventions:
        by_gen.setdefault(inv.generation, []).append(inv)

    for gen, gen_invs in sorted(by_gen.items()):
        print(f"\nGénération G{gen} ({len(gen_invs)} inventions) :")
        for inv in gen_invs:
            print(f"  {inv.invention_id} | Score: {inv.composite_patentability}/10 | {inv.title[:60]}...")

    scores = [inv.composite_patentability for inv in inventions]
    print(f"\nScore moyen de brevetabilité : {round(statistics.mean(scores), 2)}/10")
    print(f"Invention la plus forte : {max(inventions, key=lambda x: x.composite_patentability).invention_id}")

    print("\n" + "=" * 60)
    print("ARBRE GÉNÉALOGIQUE")
    print("=" * 60)
    for inv in inventions:
        parents = " ← " + ", ".join(inv.parent_ids) if inv.parent_ids else " (fondation)"
        children = " → " + ", ".join(inv.child_invention_seeds[:2]) if inv.child_invention_seeds else ""
        print(f"{inv.invention_id}{parents}{children}")

    return inventions


if __name__ == "__main__":
    run_invention_generator_engine()
