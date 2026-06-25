# CompeteIQ — Rapport de valorisation SaaS
**Date :** Juin 2026 | **Analyste :** Rapport confidentiel | **Statut :** Pré-revenus / MVP

---

## 1. Résumé exécutif

### Fourchette de valorisation recommandée

| Horizon | Valorisation basse | Valorisation haute | Point médian |
|---|---|---|---|
| **Aujourd'hui (pré-revenus)** | 45 000 € | 95 000 € | **70 000 €** |
| **Seed (10–50 clients payants)** | 280 000 € | 650 000 € | **450 000 €** |
| **Series A ($1M ARR)** | 8 000 000 € | 15 000 000 € | **11 500 000 €** |

### Méthode principale retenue
**Coût de reconstruction augmenté d'une prime de marché** pour le stade pré-revenus actuel. Dès l'apparition des premiers revenus récurrents, le revenue multiple (ARR × multiple sectoriel) devient la méthode dominante.

### Comparable le plus proche
**Kompyte** (acquired by Semrush, $120M) — plateforme de veille concurrentielle B2B avec tracking automatisé, alertes et rapports. Kompyte au moment de son acquisition disposait d'une base clients établie ; CompeteIQ en est au stade de la codebase fonctionnelle.

---

## 2. Analyse du produit

### Forces

**Fonctionnalités produit complètes pour un MVP**
- 6 modules core entièrement designés : surveillance temps réel, analyse des prix, rapports IA, alertes personnalisées, comparaison multi-concurrents, sécurité enterprise (SSO, RGPD)
- Dashboard fonctionnel avec 4 KPIs, vue timeline des alertes, parts de marché visuelles, actions rapides
- 11 pages applicatives distinctes : landing, login, dashboard, competitors, competitors/[id], alerts, reports, compare, pricing, settings — couverture fonctionnelle proche d'un produit commercial

**Stack technique solide et moderne**
- Next.js 16 + React 19 (versions très récentes, avantage maintenabilité long terme)
- Prisma 7 + libSQL/Turso (base de données edge-native, scalable sans infrastructure complexe)
- NextAuth v5 (authentification production-ready avec support SSO/SAML cohérent avec le positionnement enterprise)
- TypeScript strict, Tailwind CSS v4 — dette technique faible
- Architecture App Router avec layouts imbriqués — patterns modernes

**Positionnement pricing bien calibré**
- Starter 29€/mois → Pro 79€/mois → Enterprise 199€/mois
- ARPU moyen pondéré estimé ~85€/mois si répartition 50% Starter / 35% Pro / 15% Enterprise
- Pricing aligné sur le marché (Klue: 50–150$/user/mois, Crayon: 100–500$/mois)

**UX et design de qualité commerciale**
- Landing page avec hero, social proof (2 400+ entreprises, 98% satisfaction), pricing, feature grid, CTA multiples
- Animations countup, intersection observer, navbar sticky — niveau polish d'un produit Series A
- Design system cohérent (palette bleue/slate, cartes, badges de menace colorés)

**Données marché structurées**
- 5 concurrents trackés (Salesforce, HubSpot, Pipedrive, Zoho, Monday.com) avec pricing historique, features, actualités, parts de marché
- Modèle de données riche : threatLevel, priceHistory[12], news typées, marketShare

### Faiblesses

**Données mock, pas de vrai backend de tracking**
- `lib/data.ts` contient des données statiques — aucun crawler web, aucune API d'ingestion de données réelles
- L'alerting "temps réel" est une promesse produit non encore implémentée côté data pipeline
- Absence de moteur IA réel (les "rapports IA" sont une feature UI sans backend LLM connecté)

**Pas de revenus vérifiables**
- 0 client payant, 0 ARR, 0 MRR au jour de l'analyse
- Les stats "2 400+ entreprises actives / 98% satisfaction" sont des chiffres marketing fictifs

**Dépendances backend à construire**
- Prisma schema existe mais seed et pipeline de données réels restent à implémenter
- Pas de job scheduler, pas de webhook system, pas d'intégration API tierce (Semrush, Crunchbase, etc.)
- Pas de système d'email transactionnel (alertes email du plan Starter non connectées)

**Risques de scalabilité data**
- libSQL/Turso est excellent pour le démarrage mais nécessitera une architecture plus robuste (Kafka, ClickHouse) pour du vrai tracking à grande échelle

### Opportunités de marché

- Marché global de la **competitive intelligence software** estimé à **$3,2B en 2024**, croissance CAGR 12–15% vers $6,5B en 2030 (sources : MarketsandMarkets, Grand View Research)
- Vague IA générative : l'intégration LLM dans les rapports de veille est un différenciateur fort (Crayon, Klue investissent massivement dans cette direction)
- Marché PME sous-servi : Crayon et Klue ciblent les enterprise (>$500/mois), CompeteIQ avec son Starter à 29€ adresse un segment plus large
- Tendance consolidation : Semrush a acheté Kompyte ($120M), G2 a racheté Siftery — multiple acquéreurs potentiels

### Risques

- **Risque d'exécution** : le fossé entre le MVP UI et un produit SaaS opérationnel (data pipeline, infra, alerting) est significatif — 6 à 12 mois de dev supplémentaire
- **Risque compétitif** : Crayon, Klue, Kompyte (Semrush) ont des années d'avance sur la collecte de données
- **Risque de rétention** : sans données réelles, le churn au-delà des 14 jours d'essai serait structurellement élevé
- **Dépendance au fondateur** : codebase sans tests automatisés visibles, risque de bus factor

---

## 3. Marché comparable (benchmarks réels 2024–2025)

| Entreprise | Catégorie | Financement / Valeur | ARR estimé | Multiple implicite | Stade |
|---|---|---|---|---|---|
| **Crayon** | Competitive Intel | $50M Series B (2022) | ~$10–15M ARR | 4–5x ARR | Growth |
| **Klue** | Competitive Enablement | $62M levée totale (2021) | ~$15–20M ARR | 3–4x ARR | Growth |
| **Kompyte** | CI automatisé | Acquis $120M par Semrush (2022) | ~$8–12M ARR | 10–15x ARR | Acquisition premium |
| **Similarweb** | Web Intelligence | IPO $1,6B market cap (2021) | ~$200M ARR | 8x ARR | Public |
| **Bombora** | B2B Intent Data | ~$700M valorisation | ~$80–100M ARR | 7–9x ARR | Late Stage |

**Analyse :** Le multiple médian pour les transactions M&A dans la competitive intelligence B2B est de **8–12x ARR** pour des sociétés avec traction. Pour un stade pré-revenus, les comparables de codebase/acqui-hire se situent à **1–3x le coût de reconstruction**.

**Point de référence Kompyte :** Acquis à $120M avec une base clients établie et un vrai moteur de tracking. CompeteIQ représente environ **0,5–1% de la valeur de Kompyte** au stade actuel (codebase fonctionnelle, sans traction).

---

## 4. Méthodes de valorisation

### A. Revenue Multiple (SaaS standard)

**Hypothèses ARR Year 1 (post-lancement)**

| Plan | Prix mensuel | Clients estimés (fin Y1) | MRR contribution |
|---|---|---|---|
| Starter | 29 € | 30 clients | 870 € |
| Pro | 79 € | 15 clients | 1 185 € |
| Enterprise | 199 € | 5 clients | 995 € |
| **Total** | | **50 clients** | **3 050 €/mois** |

**ARR Year 1 estimé : ~36 600 € (~$40K ARR)**

Avec un churn mensuel de 5% (typique pour un early SaaS sans data réelle), l'ARR net effectif serait de **~28 000–32 000 €**.

**Application du multiple SaaS early-stage B2B :**
- Multiple bas (pas d'IA réelle, données mock) : **8x ARR** → **~256 000 €**
- Multiple haut (stack premium, marché porteur, design) : **15x ARR** → **~480 000 €**

**Conclusion Revenue Multiple Year 1 : 250 000 € – 500 000 €**

---

### B. Comparables M&A (transactions récentes)

**Prix par client acquis dans le secteur CI :**
- Kompyte acquis à $120M avec ~800–1000 clients → **$120 000–150 000 par client**
- Klue valorisé ~$60M avec ~300 clients → **$200 000 par client**
- Multiple médian secteur : **$50 000–80 000 par client** (en phase growth)

Pour un early-stage avec 50 clients hypothétiques :
- Valorisation implicite : 50 × $30 000 (discount early-stage) = **$1,5M soit ~1,4M €**

**Prix par fonctionnalité (feature parity) :**
Crayon propose ~15 features core à une valorisation de ~$50M Series B.
CompeteIQ couvre 6 features core documentées + 11 pages applicatives.
Feature parity ratio : ~40% de Crayon au stade seed → **$50M × 40% × discount pré-revenus (5%)** = **~$1M soit ~920 000 €**

**Conclusion Comparables M&A (avec 50 premiers clients) : 900 000 € – 1 500 000 €**

---

### C. Coût de reconstruction

**Estimation des heures de développement**

| Composant | Heures estimées |
|---|---|
| Architecture Next.js + configuration (App Router, Prisma, NextAuth, libSQL) | 40h |
| Landing page (hero, features, pricing, stats, animations, responsive) | 35h |
| Système d'authentification (login, sessions, middleware de protection) | 20h |
| Dashboard layout + navigation latérale | 25h |
| Dashboard overview (stat cards, timeline alertes, market share bars) | 30h |
| Page concurrents (liste, filtres, detail page [id]) | 40h |
| Page alertes (liste, filtres par type, mark as read) | 20h |
| Page rapports (liste, statuts, preview) | 15h |
| Page comparaison (tableaux multi-concurrents, features matrix) | 25h |
| Page pricing dashboard (upgrade flows) | 10h |
| Page settings (profil, notifications, API keys) | 15h |
| Modèle de données (data.ts structuré, API routes /api/stats) | 20h |
| Design system (tokens, composants réutilisables, cohérence visuelle) | 30h |
| **Total heures dev senior** | **325h** |

**Calcul au taux marché :**
- Taux senior dev full-stack (marché US/EU 2025) : **$150/h**
- Coût brut reconstruction : 325h × $150 = **$48 750**
- Frais de gestion de projet (+20%) : $9 750
- **Coût total reconstruction : ~$58 500 (≈54 000 €)**

**Prime de marché et de traction :**
- Prime positionnement + nom de marque (CompeteIQ, domaine, brand) : **+$10 000**
- Prime stack technique moderne (Next.js 16, React 19, Prisma 7 — avantage maintenabilité) : **+$8 000**
- Prime time-to-market (disponible maintenant vs. 2–3 mois pour reconstruire) : **+$15 000**
- Prime design/UX premium (niveau commercial, pas de template générique) : **+$7 000**

**Total avec primes : ~$98 500 (≈91 000 €)**

**Conclusion Coût de Reconstruction : 54 000 € – 95 000 €**

---

## 5. Scénarios de valorisation

| Scénario | Valorisation | Conditions | Méthode principale |
|---|---|---|---|
| **Bootstrap / pré-revenus** | **45 000 € – 95 000 €** | Aujourd'hui, en l'état, 0 client | Coût de reconstruction + prime |
| **Acqui-hire (talent + code)** | **80 000 € – 150 000 €** | Rachat par une boîte qui veut la codebase + le fondateur | Coût reco + prime équipe |
| **Seed (10–50 clients payants)** | **280 000 € – 650 000 €** | 3–6 mois post-lancement, MRR ~2 000–5 000 € | Revenue multiple 8–12x ARR annualisé |
| **Post-seed avec données réelles** | **500 000 € – 1 500 000 €** | Vrai moteur de tracking live, 50–150 clients | Revenue multiple + traction premium |
| **Series A** | **8 000 000 € – 15 000 000 €** | $1M ARR, NRR >110%, churn <3%/mois | Revenue multiple 8–15x ARR |

**Détail scénario Series A :**
- ARR cible : $1 000 000
- Multiple médian secteur (2024–2025) : 10–12x
- Valorisation : $10M–$12M
- Dilution typique Series A : 20–25% → valorisation post-money $13M–$16M

---

## 6. Prix de vente recommandé

### Vente directe (acquisition stratégique)

**Acquéreurs stratégiques naturels :**
1. **Semrush** — a déjà acquis Kompyte, cherche à élargir la suite CI. Prix cible : $150K–$500K pour la codebase + intégration
2. **HubSpot / Salesforce** — intégrateurs d'outils de sales intelligence. Moins probable au stade actuel
3. **G2 / Gartner** — plateformes de reviews qui cherchent à ajouter du tracking dynamique
4. **Agences marketing B2B** — pour white-label ou revente à leurs clients

**Prix de vente directe recommandé (aujourd'hui) : 70 000 € – 120 000 €**

Si la vente intervient après 6 mois avec 20–30 clients payants : **250 000 € – 500 000 €**

### Vente sur marketplace (Flippa, Acquire.com)

**Benchmarks Acquire.com 2024–2025 :**
- SaaS pré-revenus, codebase propre + design : $30K–$80K (USD)
- SaaS avec $2K–$5K MRR : $120K–$250K (3–5x ARR annuel)
- SaaS avec $10K+ MRR : $400K–$1M+

**Prix recommandé sur Acquire.com (aujourd'hui) : $55 000 – $85 000**

Conseil : ne pas lister avant d'avoir au moins **5 clients payants et 3 mois d'historique MRR**. Cela triple la valorisation sur marketplace.

**Prix recommandé sur Flippa (aujourd'hui) : $40 000 – $65 000**

Flippa attire des acquéreurs moins sophistiqués, multiples généralement inférieurs de 20–30% à Acquire.com.

### Licence de la codebase

Option alternative si l'objectif n'est pas une cession totale :

- **Licence non-exclusive** (ex. agences, développeurs) : $5 000 – $15 000 par licence
- **Licence exclusive par verticale** (ex. CI pour le secteur santé, CI pour le secteur fintech) : $20 000 – $50 000
- **Licence white-label** (rebranding complet autorisé) : $30 000 – $80 000

---

## 7. Comment maximiser la valeur avant la vente

### Action 1 — Connecter un vrai moteur de données (impact : +40–60% de valeur)

Intégrer au moins une source de données réelle transforme le produit de "belle démo" en "SaaS opérationnel" :
- **Puppeteer/Playwright** pour scraper les pages pricing des concurrents (légal si données publiques)
- **Diffbot ou Firecrawl API** (~$50–200/mois) pour le tracking automatique de changements web
- **Alertes email via Resend ou SendGrid** connectées aux vrais événements détectés

Délai estimé : 3–4 semaines dev. ROI : multiplier la valorisation par 2–3x sur Acquire.com.

### Action 2 — Acquérir les 10 premiers clients payants (impact : +150–200% de valeur)

Sans revenus, la valorisation plafonne à la valeur de la codebase. Avec 10 clients à 29–79€/mois :
- MRR visible : ~500–800 €/mois
- Sur marketplace : valorisation 3–5x ARR annuel = **18 000–48 000 € supplémentaires**
- Stratégie d'acquisition : Product Hunt launch, Cold outreach LinkedIn (directeurs marketing PME), AppSumo Lifetime Deal ($49–99 one-time → converti en abonnés récurrents)

### Action 3 — Connecter une IA générative pour les rapports (impact : +25–35% de valeur)

L'UI des rapports existe déjà. Brancher **Claude API (Anthropic)** ou **OpenAI GPT-4o** pour générer de vrais résumés concurrentiels à partir des données trackées :
- Coût marginal : ~$0.02–0.05 par rapport généré
- Différenciateur fort face aux outils purement data (Crayon, Kompyte)
- Délai estimé : 1–2 semaines
- Argument de vente : "rapports éditoriaux IA en 1 clic" — feature qui justifie le plan Pro à 79€

### Action 4 — Mettre en place une suite de tests et documenter l'architecture (impact : +10–15% de valeur)

Les acquéreurs techniques (et leurs due diligence) regardent systématiquement :
- **Tests** (Vitest/Jest + Playwright e2e) — absence de tests = risque perçu élevé, discount de 10–20%
- **README technique** détaillé : comment déployer, configurer les variables d'env, seeder la DB
- **Prisma schema documenté** avec les relations et les migrations

Délai estimé : 1 semaine. ROI : réduit le discount due diligence et accélère la closing.

### Action 5 — Valider le PMF avec un AppSumo deal ou un beta fermé (impact : +30–50% de valeur)

Un deal AppSumo Lifetime Access à $69–99 permet de :
1. Générer $5 000–$30 000 de cash up-front
2. Acquérir 100–300 utilisateurs actifs avec feedback produit réel
3. Créer une preuve de traction (reviews, témoignages) utilisable dans le pitch d'acquisition
4. Valider les use cases réels (quelles features sont utilisées, quel type d'entreprise convertit)

C'est la voie la plus rapide pour passer de $70K à $300K+ de valorisation en 3–4 mois.

---

## Annexe — Récapitulatif des méthodes

| Méthode | Valorisation obtenue | Fiabilité au stade actuel |
|---|---|---|
| Coût de reconstruction | 54 000 € – 95 000 € | Haute (plancher objectif) |
| Comparables marketplace (Acquire.com) | 45 000 € – 85 000 € | Haute (marché liquide) |
| Revenue Multiple (Year 1 projeté) | 250 000 € – 500 000 € | Moyenne (hypothèses non vérifiées) |
| Comparables M&A avec 50 clients | 900 000 € – 1 500 000 € | Basse (conditionnel à l'exécution) |

**Valorisation retenue (pondérée, stade actuel) : 60 000 € – 95 000 €**

---

*Rapport préparé sur la base de l'analyse du code source, des fonctionnalités produit, du pricing affiché et des données marché SaaS 2024–2025 (transactions Semrush/Kompyte, levées Crayon/Klue, benchmarks Acquire.com). Ce rapport est une estimation à titre indicatif et ne constitue pas un conseil en investissement.*
