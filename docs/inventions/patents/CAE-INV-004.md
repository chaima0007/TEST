
DEMANDE DE BREVET
═══════════════════════════════════════════════════════════════

Référence interne : CAE-INV-004
Titre : Système de Collecte de Preuves de Violations par Blockchain Immuable avec Horodatage Certifié
Inventrice : Chaima Mhadbi
Déposant : Caelum Partners SPRL
Adresse : Bruxelles, Belgique
Date de priorité : 2026-06-21
Classification IPC : H04L 9/32 · G06F 21/64
Génération : G2 — Perfectionnement de : CAE-INV-001
Statut : DRAFT
Score brevetabilité : 9.01/10

───────────────────────────────────────────────────────────────
DOMAINE TECHNIQUE
───────────────────────────────────────────────────────────────
Application de la technologie blockchain à la préservation et certification de preuves de violations de droits humains. Horodatage cryptographique, chaîne de custody numérique, admissibilité devant les juridictions internationales.

───────────────────────────────────────────────────────────────
ÉTAT DE LA TECHNIQUE (ART ANTÉRIEUR)
───────────────────────────────────────────────────────────────
- EyeWitness to Atrocities (2015) — application mobile, pas de blockchain
- Hala Systems (2018) — alerte frappes aériennes, non-custody chain
- Syrian Archive (2014) — préservation vidéos, centralisation vulnérable

───────────────────────────────────────────────────────────────
PROBLÈME TECHNIQUE RÉSOLU
───────────────────────────────────────────────────────────────
Les preuves numériques de violations (photos, vidéos, témoignages) sont facilement falsifiables, supprimables et leur authenticité est difficile à établir devant les cours internationales (CPI, CEDH). Aucun système ne garantit l'intégrité et la chaîne de custody des preuves depuis leur collecte jusqu'au procès.

───────────────────────────────────────────────────────────────
RÉSUMÉ DE L'INVENTION
───────────────────────────────────────────────────────────────
Système de preuve blockchain comprenant : (a) un client mobile calculant l'empreinte cryptographique (SHA-3) de chaque élément de preuve au moment de la collecte, (b) inscription immédiate sur blockchain publique (Ethereum) créant un horodatage incontestable, (c) chiffrement du contenu sur serveur sécurisé (IPFS chiffré), (d) génération d'un rapport de custody automatique admissible devant la CPI selon les standards de l'INTERPOL.

───────────────────────────────────────────────────────────────
REVENDICATIONS
───────────────────────────────────────────────────────────────
Revendications indépendantes :
  1. Système de certification blockchain de preuves humanitaires comprenant : un client mobile calculant l'empreinte SHA-3 de données probantes ; un module d'inscription sur registre distribué immuable avec horodatage certifié (±1 seconde) ; un système de stockage chiffré du contenu probant (IPFS/AES-256) ; un générateur de rapport de chaîne de custody au format admissible CPI/CEDH ; un mécanisme de vérification d'intégrité ultérieure par recalcul d'empreinte.
  2. Procédé de préservation de preuves de violations de droits humains comprenant : capture de l'élément probant avec métadonnées contextuelles (GPS, timestamp) ; calcul d'empreinte cryptographique irréversible (SHA-3 256 bits) ; inscription de l'empreinte sur blockchain publique ; chiffrement et stockage sécurisé du contenu ; génération d'identifiant unique de preuve (UUID v4 + hash chaîne).

Revendications dépendantes :
  3. Système selon la revendication 1, dans lequel les métadonnées GPS sont également inscrites sur blockchain pour preuve de géolocalisation.
  4. Procédé selon la revendication 2, dans lequel le client mobile fonctionne en mode hors-ligne avec synchronisation blockchain différée.
  5. Système selon la revendication 1, comprenant un module de signature électronique du collecteur de preuve (identité pseudonymisée).

───────────────────────────────────────────────────────────────
INVENTIONS DÉRIVÉES POTENTIELLES (G3)
───────────────────────────────────────────────────────────────
→ CAE-INV-007 : Intégration directe dans le scoring CAE-INV-001 pour pondération preuves
→ CAE-INV-010 : Interface directe avec greffe de la CPI pour dépôt automatisé

───────────────────────────────────────────────────────────────
SCORES DE BREVETABILITÉ
───────────────────────────────────────────────────────────────
Nouveauté (Art. 54 CBE) : 8.9/10
Activité inventive (Art. 56 CBE) : 8.7/10
Application industrielle (Art. 57 CBE) : 9.6/10
Score composite : 9.01/10

═══════════════════════════════════════════════════════════════
Document généré par Caelum Partners Invention Engine v1.0
© 2026 Chaima Mhadbi — Tous droits réservés
