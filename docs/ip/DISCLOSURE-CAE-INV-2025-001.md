# Note de Divulgation d'Invention — CAE-INV-2025-001

**CONFIDENTIEL — PROPRIÉTÉ EXCLUSIVE CAELUM PARTNERS SPRL**

---

## Informations Administratives

| Champ | Valeur |
|-------|--------|
| **Référence interne** | CAE-INV-2025-001 |
| **Nom commercial** | CaelumSwarm™ |
| **Date de divulgation** | 21 juin 2025 |
| **Inventrice** | Chaima Mhadbi |
| **Titulaire** | Caelum Partners SPRL, Bruxelles, Belgique |
| **Email contact** | retrouvetonsmile@gmail.com |
| **Statut** | Divulgation interne — priorité établie |

---

## Titre de l'Invention

**Système distribué d'évaluation des risques en matière de droits humains par essaim d'agents intelligents avec calcul d'indices composites multicritères**

*(EN: Distributed human rights risk assessment system using intelligent agent swarms with multi-criteria composite index computation)*

---

## Domaine Technique

Intelligence artificielle distribuée — Systèmes multi-agents — Analyse de conformité ESG — Surveillance des droits humains — Traitement de données hétérogènes en temps réel.

---

## Problème Technique Résolu

Avant cette invention, aucun système existant ne permettait de :
1. Agréger automatiquement des données de violation des droits humains provenant de sources hétérogènes (UNHCR, HRW, Amnesty, OIT, etc.)
2. Calculer en temps réel un indice composite pondéré par domaine thématique
3. Distribuer ce calcul via une architecture d'essaim d'agents spécialisés opérant en parallèle
4. Produire une distribution de risque normalisée (critique/élevé/modéré/faible) exploitable pour la conformité CSDDD

Les solutions existantes sont soit manuelles (consultants), soit génériques (sans pondération par domaine), soit non-distribuées (calcul centralisé = goulot d'étranglement).

---

## Description de l'Invention

### Architecture Générale

L'invention comprend :

**A. Couche Agents Spécialisés (Swarm Layer)**
- N agents thématiques indépendants (N ≥ 50 dans l'implémentation actuelle)
- Chaque agent monitore un domaine spécifique : apatridie, violence de genre, traite humaine, liberté presse, etc.
- Les agents opèrent en parallèle sans dépendance inter-agents (architecture *embarrassingly parallel*)

**B. Moteur de Scoring Composite**
- Formule brevetable : `CS = (S1 × 0.30) + (S2 × 0.25) + (S3 × 0.25) + (S4 × 0.20)` appliquée sur sous-scores normalisés [0–10]
- 4 sous-dimensions par domaine, pondérées selon leur corrélation empirique avec les violations documentées
- Indice dérivé : `IDX = round(CS / 100 × 10, 2)` pour normalisation /10

**C. Distribution de Risque Automatique**
- Seuils calibrés : critique (CS ≥ 60), élevé (40 ≤ CS < 60), modéré (20 ≤ CS < 40), faible (CS < 20)
- Distribution obligatoire 4/2/1/1 pour comparabilité inter-waves

**D. Couche de Sécurité (CaelumSeal)**
- Scellement cryptographique de chaque réponse API via `sealResponse()`
- Guard `SWARM_API_URL` pour bascule mock/live transparente
- Revalidation périodique (30s) sans surcharge serveur

**E. Interface de Visualisation**
- Dashboards React temps réel avec jauge circulaire (GaugeRing)
- Distribution visuelle des risques par entité géographique

---

## Nouveauté — Ce qui n'existait pas avant

1. **Combinaison unique** : essaim d'agents IA × scoring composite × conformité CSDDD
2. **Architecture de bascule** : même API, données mock ou live selon variable d'environnement
3. **Pondération par domaine** : chaque domaine droits humains a ses propres poids empiriques
4. **Scalabilité illimitée** : N agents peuvent être ajoutés sans refactorisation (Wave 147, 148...∞)

---

## Revendications (version préliminaire)

1. Système d'évaluation des risques comprenant une pluralité d'agents logiciels spécialisés opérant en parallèle, chaque agent étant dédié à un domaine thématique de droits humains distinct.

2. Le système selon la revendication 1, dans lequel chaque agent calcule un score composite selon la formule `CS = S1×P1 + S2×P2 + S3×P3 + S4×P4` où P1+P2+P3+P4 = 1.

3. Le système selon la revendication 2, dans lequel les scores sont catégorisés automatiquement en niveaux de risque selon des seuils prédéfinis.

4. Procédé de bascule automatique entre données simulées et données temps-réel via une variable d'environnement unique.

5. Interface de visualisation comprenant une représentation circulaire normalisée du score composite par entité géographique.

---

## Preuve de Priorité

Ce document, committé dans le dépôt Git `chaima0007/TEST` avec horodatage cryptographique GitHub, constitue une preuve de date de conception opposable.

**Hash Git de référence :** voir `git log --oneline docs/ip/DISCLOSURE-CAE-INV-2025-001.md`

---

*Document rédigé le 21 juin 2025 — Caelum Partners SPRL — Tous droits réservés*
