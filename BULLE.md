# 🫧 Bulle — app Parents-Enfants (MVP démontrable)

> **2026-07-17-20h51 — app-parents-enfants — MVP jouable (côté enfant + côté parent)**
> Projet perso *retrouvetonsmile*. Aider parents et enfants à **mieux se parler** :
> nommer les émotions et désamorcer les conflits en douceur.
> **Démo en données fictives — aucune vraie donnée d'enfant.**

## Synopsis

Bulle est une petite app à **double expérience** :

- **Côté enfant** (ludique, rassurant, grosses cibles tactiles) : cartes émotions
  adaptées à l'âge, rituels de dialogue à faire *ensemble*, et un « coin calme ».
- **Côté parent** (sobre, clair, derrière un **portail parental**) : conseils
  **sourcés** (pédopsychiatrie & organismes officiels), datés et vérifiables.

Le positionnement — et l'angle mort qu'on adresse volontairement :

- **Ce n'est PAS un outil de surveillance.** Aucun suivi, aucun espionnage,
  aucun « rapport » sur l'enfant. L'app aide à **parler**, pas à contrôler.
- **Sécurité enfant par design** : pas de chat, pas de contact avec des inconnus,
  aucune donnée qui identifie/localise l'enfant, pas de pub.
- **Contenu fondé** : chaque conseil cite un organisme reconnu + une année. Jamais inventé.
- **Accessibilité** et **ton jamais moralisateur**.

## Périmètre livré

| # | Fonctionnalité | Route |
|---|----------------|-------|
| 1 | Accueil + choix des deux modes + badges de confiance | `/bulle` |
| 2 | Accueil enfant (3 grandes cartes) | `/bulle/enfant` |
| 3 | **Cartes émotions** (10 émotions, filtre par âge 3-5 / 6-8 / 9-11, corps + déclencheurs + gestes qui aident, lecture à voix haute) | `/bulle/enfant/emotions` |
| 4 | **Rituels de dialogue** guidés pas-à-pas, à faire *ensemble* (météo des émotions, bâton de parole, réparation, 3 ballons, rose & épine) | `/bulle/enfant/rituels` |
| 5 | **Coin calme** (respiration guidée + ancrage 5-4-3-2-1) | `/bulle/enfant/calme` |
| 6 | **Espace parent** derrière portail parental : conseils sourcés filtrables | `/bulle/parent` |
| 7 | **Promesses / Sources / Méthode / RGPD** (transparence) | `/bulle/promesses` |

## Ce qui nous rend « inévitables » (au-delà du brief)

- **Rituels co-régulés** : le téléphone se passe de main en main (tour de parole).
  L'app est un *support de conversation*, pas un écran de plus pour isoler l'enfant.
- **Assentiment de l'enfant** intégré au design (on respecte l'enfant comme une personne,
  pas un objet à monitorer) → différenciateur fort vs. apps de contrôle parental.
- **Transparence radicale** (`/bulle/promesses`) : nos promesses, nos sources datées,
  notre méthode et le cadre RGPD affichés noir sur blanc. La confiance est le produit.
- **Accessibilité de série** : lecture à voix haute *sur l'appareil* (Web Speech API,
  zéro réseau), option « gros texte », grandes cibles, focus clavier, respect de
  `prefers-reduced-motion`.
- **Zéro réseau côté enfant** : tout est local, aucune ressource externe, aucun tracker.

## Fondé sur des sources reconnues (consultées le 2026-07-17)

- **The Gottman Institute** — *Emotion Coaching*, 5 étapes (1997)
- **Dr Daniel Siegel & Tina Payne Bryson** — *The Whole-Brain Child*, « Name it to tame it » (2011)
- **Center on the Developing Child, Harvard** — *Serve and Return* (2020)
- **Yapaka — Fédération Wallonie-Bruxelles** — soutien à la parentalité (2024)
- **ONE — Office de la Naissance et de l'Enfance (Belgique)** (2023)
- **American Academy of Pediatrics — HealthyChildren.org** (2023)
- **UNICEF Parenting** (2022)
- **Yale Center for Emotional Intelligence — RULER / Marc Brackett** (2019)

## Lancer la démo

```bash
npm install
npm run dev
# puis ouvrir http://localhost:3000/bulle
```

Portail parental (démo) : la réponse à « 7 × 8 » est **56**.

## AUDIT

**FAIT**
- Double UX enfant/parent, 7 écrans, 10 cartes émotions, 5 rituels, 8 conseils sourcés.
- Portail parental, accessibilité (TTS on-device, gros texte, focus, reduced-motion).
- Données 100 % fictives, aucun appel réseau, aucune collecte.

**VÉRIFIÉ (preuve)**
- Les 7 routes répondent `HTTP 200` (dev server Next 16.2.9).
- ESLint : **0 erreur** sur `app/bulle`, `components/bulle`, `lib/bulle`.
- Rendu confirmé par captures d'écran (accueil, détail émotion, espace parent
  après passage du portail parental).
- Sources vérifiées par recherche web (organismes réels, non inventés).

**RESTE (hors MVP)**
- Dépôt dédié : ce MVP vit sous `/bulle` **dans le dépôt existant** (qui contient un
  autre projet). Pour un vrai dépôt privé séparé, à extraire.
- Persistance locale opt-in (favoris émotions) — volontairement absente au MVP.
- Traductions / voix off enregistrées, mode illustrations dessinées.
- Tests automatisés (Playwright) à ajouter.

## ⚠️ Caveat (protection des mineurs)

MVP en **données fictives**. Avant toute mise en service avec de **vraies données
d'enfants** : **AIPD/DPIA**, **consentement parental**, **base légale** claire et
conception **age-appropriate design** (minimisation, transparence, pas de profilage).
Contenu **informatif**, il ne remplace pas l'avis d'un·e professionnel·le.
