
DEMANDE DE BREVET
═══════════════════════════════════════════════════════════════

Référence interne : CAE-INV-003
Titre : Architecture d'Apprentissage Fédéré pour Scoring de Droits Humains Préservant l'Anonymat des Sources Terrain
Inventrice : Chaima Mhadbi
Déposant : Caelum Partners SPRL
Adresse : Bruxelles, Belgique
Date de priorité : 2026-06-21
Classification IPC : G06N 20/00 · H04L 9/32
Génération : G2 — Perfectionnement de : CAE-INV-001
Statut : DRAFT
Score brevetabilité : 8.99/10

───────────────────────────────────────────────────────────────
DOMAINE TECHNIQUE
───────────────────────────────────────────────────────────────
Apprentissage automatique fédéré appliqué aux données sensibles de violations de droits humains. Protocoles cryptographiques préservant l'anonymat des sources dans les zones de conflit.

───────────────────────────────────────────────────────────────
ÉTAT DE LA TECHNIQUE (ART ANTÉRIEUR)
───────────────────────────────────────────────────────────────
- McMahan et al. 'Communication-Efficient Learning' (2017) — FL générique
- Dwork 'Differential Privacy' (2006) — DP théorique, non appliqué HRW
- Bonawitz et al. 'SecAgg' (2017) — agrégation sécurisée générique

───────────────────────────────────────────────────────────────
PROBLÈME TECHNIQUE RÉSOLU
───────────────────────────────────────────────────────────────
Le système CAE-INV-001 requiert la centralisation des données sources, exposant les informateurs et défenseurs des droits humains à des risques de représailles. Les sources terrain en zones de conflit ne peuvent contribuer si leur identité ou localisation peut être déduite.

───────────────────────────────────────────────────────────────
RÉSUMÉ DE L'INVENTION
───────────────────────────────────────────────────────────────
Architecture fédérée où chaque nœud (ONG, bureau terrain) entraîne localement un modèle partiel sur ses données sensibles. Seuls les gradients agrégés (jamais les données brutes) transitent sur le réseau, chiffrés par protocole de confidentialité différentielle (ε-DP). Le modèle global est reconstruit par agrégation sécurisée (SecAgg) sans que le serveur central n'accède aux données individuelles.

───────────────────────────────────────────────────────────────
REVENDICATIONS
───────────────────────────────────────────────────────────────
Revendications indépendantes :
  1. Architecture d'apprentissage fédéré pour droits humains comprenant : des nœuds clients (bureaux terrain) entraînant des modèles locaux sur données sensibles non-partagées ; un protocole de confidentialité différentielle (ε-DP, ε ≤ 1.0) appliqué aux gradients avant transmission ; un serveur d'agrégation sécurisée (SecAgg) reconstruisant le modèle global sans accès aux données individuelles des nœuds ; un mécanisme de vérification d'intégrité des contributions par signature cryptographique.

Revendications dépendantes :
  2. Architecture selon la revendication 1, dans laquelle le paramètre ε de confidentialité différentielle est adaptatif selon la sensibilité géographique du nœud client (zones de conflit : ε ≤ 0.1).
  3. Architecture selon la revendication 1, comprenant un module de détection de contributions malveillantes (Byzantine fault tolerance).
  4. Architecture selon la revendication 1, dans laquelle les nœuds clients peuvent opérer en mode asynchrone pour zones à connectivité limitée.

───────────────────────────────────────────────────────────────
INVENTIONS DÉRIVÉES POTENTIELLES (G3)
───────────────────────────────────────────────────────────────
→ CAE-INV-006 : Nœud mobile offline-first pour agents terrain sans connexion
→ CAE-INV-009 : Certification ISO 27001 adaptée aux données de droits humains

───────────────────────────────────────────────────────────────
SCORES DE BREVETABILITÉ
───────────────────────────────────────────────────────────────
Nouveauté (Art. 54 CBE) : 9.1/10
Activité inventive (Art. 56 CBE) : 9.0/10
Application industrielle (Art. 57 CBE) : 8.8/10
Score composite : 8.99/10

═══════════════════════════════════════════════════════════════
Document généré par Caelum Partners Invention Engine v1.0
© 2026 Chaima Mhadbi — Tous droits réservés
