
DEMANDE DE BREVET
═══════════════════════════════════════════════════════════════

Référence interne : CAE-INV-001
Titre : Système de Scoring Automatisé des Violations de Droits Humains par Intelligence Artificielle Multi-Dimensionnelle
Inventrice : Chaima Mhadbi
Déposant : Caelum Partners SPRL
Adresse : Bruxelles, Belgique
Date de priorité : 2026-06-21
Classification IPC : G06N 20/00 · G06F 40/56
Génération : G1 — Invention de premier rang (fondation)
Statut : DRAFT
Score brevetabilité : 8.72/10

───────────────────────────────────────────────────────────────
DOMAINE TECHNIQUE
───────────────────────────────────────────────────────────────
Intelligence artificielle appliquée à l'analyse et la quantification automatisée des violations de droits humains à l'échelle mondiale. Traitement du langage naturel, apprentissage automatique supervisé, et systèmes d'indexation composite multi-critères.

───────────────────────────────────────────────────────────────
ÉTAT DE LA TECHNIQUE (ART ANTÉRIEUR)
───────────────────────────────────────────────────────────────
- Freedom House Freedom in the World Index (2006) — scoring binaire non-composite
- V-Dem Dataset (2016) — données électorales, non centré droits humains
- Human Rights Measurement Initiative HRMI (2017) — questionnaires manuels
- Amnesty International Urgent Actions (1973) — alertes manuelles non-scorées
- Global Slavery Index (2013) — domaine unique (esclavage), non multi-thématique

───────────────────────────────────────────────────────────────
PROBLÈME TECHNIQUE RÉSOLU
───────────────────────────────────────────────────────────────
L'analyse des violations de droits humains repose actuellement sur des processus manuels chronophages, subjectifs, et non-comparables entre pays. Aucun système automatisé ne produit des scores composites reproductibles, pondérés et comparables sur 100+ domaines thématiques en temps réel.

───────────────────────────────────────────────────────────────
RÉSUMÉ DE L'INVENTION
───────────────────────────────────────────────────────────────
Système informatique comprenant : (a) un moteur d'extraction de signaux depuis sources documentaires (rapports ONU, ONG, médias) via NLP, (b) une architecture de scoring composite à 4 sous-dimensions pondérées (w1=0.30, w2=0.25, w3=0.25, w4=0.20), (c) un module de normalisation sur échelle 0-100 avec seuils de criticité automatiques, (d) une API temps-réel exposant les indices par domaine et entité.

───────────────────────────────────────────────────────────────
REVENDICATIONS
───────────────────────────────────────────────────────────────
Revendications indépendantes :
  1. Système informatique de scoring automatisé des violations de droits humains comprenant : un module d'ingestion de données documentaires multi-sources ; un moteur NLP d'extraction d'entités et d'événements liés aux droits humains ; un calculateur de score composite à pondération différentielle (0.30/0.25/0.25/0.20) ; un classificateur de niveau de risque à seuils prédéfinis (critique/élevé/modéré/faible) ; une interface de programmation (API) exposant les résultats en temps réel.
  2. Procédé de génération d'un indice de violation de droits humains comprenant les étapes : collecte automatisée de documents depuis sources humanitaires ; extraction de signaux factuels par traitement du langage naturel ; calcul d'un score composite selon la formule S = Σ(wi × si) où Σwi = 1 ; classification du niveau de risque selon des seuils prédéterminés ; exposition de l'indice via une interface standardisée.

Revendications dépendantes :
  3. Système selon la revendication 1, dans lequel le module NLP utilise des modèles de langue entraînés spécifiquement sur corpus de droits humains (HRW, Amnesty, ONU).
  4. Système selon la revendication 1, dans lequel les seuils de criticité sont : critique ≥ 60, élevé ≥ 40, modéré ≥ 20, faible < 20, sur échelle 0-100.
  5. Procédé selon la revendication 2, dans lequel le score est mis à jour automatiquement avec revalidation toutes les 30 secondes.
  6. Système selon la revendication 1, comprenant en outre un module d'alerte automatique lorsque le score dépasse le seuil critique.

───────────────────────────────────────────────────────────────
INVENTIONS DÉRIVÉES POTENTIELLES (G2)
───────────────────────────────────────────────────────────────
→ CAE-INV-003 : Version fédérée préservant la vie privée des sources terrain
→ CAE-INV-004 : Déploiement mobile hors-ligne pour zones sans internet
→ CAE-INV-007 : Intégration blockchain pour preuve d'intégrité des scores

───────────────────────────────────────────────────────────────
SCORES DE BREVETABILITÉ
───────────────────────────────────────────────────────────────
Nouveauté (Art. 54 CBE) : 8.7/10
Activité inventive (Art. 56 CBE) : 8.2/10
Application industrielle (Art. 57 CBE) : 9.5/10
Score composite : 8.72/10

═══════════════════════════════════════════════════════════════
Document généré par Caelum Partners Invention Engine v1.0
© 2026 Chaima Mhadbi — Tous droits réservés
