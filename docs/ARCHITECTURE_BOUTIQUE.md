# Architecture de la boutique dropshipping — CompeteIQ Commerce

Document d'architecture rédigé par l'orchestrateur. La niche et les produits
sont définis dans `docs/PLAN_LANCEMENT.md` (rapport du growth-strategist).
Marché : France d'abord. API Shopify : 2026-07.

## 1. Structure de la boutique

### Pages et parcours
- **Accueil** : proposition de valeur en un écran (héros + preuve sociale),
  3 collections mises en avant, section « pourquoi nous » (différenciant),
  newsletter (`{% form 'customer' %}`).
- **Collections** : une collection par usage (pas par type de produit — on
  vend un résultat, pas un objet). Modèle multi-sources 2026-07 avec
  conditions typées (tags produits normalisés par catalog-manager).
- **Fiche produit** : galerie (photos + vidéo courte ; modèle 3D GLB pour les
  produits phares), bénéfices avant caractéristiques, prix unitaire si
  pertinent, `{{ form | payment_button }}` (checkout accéléré),
  `{{ form | payment_terms }}` (Shop Pay Installments), bloc livraison
  honnête (délai réel affiché), avis clients.
- **Panier** : tiroir (actions standards `Shopify.actions.updateCart`/
  `openCart`), réductions affichées ligne + panier, sous-total
  `data-cart-subtotal`.
- **Pages confiance** : livraison & retours (délais réels, qui paie quoi),
  CGV, confidentialité, contact (`{% form 'contact' %}`), suivi de commande.
- **Blog** : 2 articles/mois minimum sur la niche (SEO + fidélisation).

### Thème
- Base **Skeleton**, sections modulaires, réglages `color_palette`.
- Qualité imposée en CI : `theme check --fail-level error` + Lighthouse CI
  (perf ≥ 0.6, accessibilité ≥ 0.9) sur chaque PR.
- Mobile d'abord : la maquette se valide sur 390 px avant le desktop.

## 2. Différenciant structurel : la transparence logistique

Le talon d'Achille du dropshipping est la livraison. Notre position :
**afficher la vérité et la tenir**.

- Fournisseurs avec **entrepôt UE uniquement** (délai ≤ 10 jours ouvrés,
  critère bloquant du pipeline produits).
- Sur chaque fiche : date de livraison estimée réelle (pas « 24/48 h » mensonger).
- Page de suivi de commande intégrée (notre app Next.js) : statut fournisseur
  → transporteur → client, e-mails proactifs en cas de retard (un retard
  annoncé est un client conservé).
- SAV : réponse < 24 h, politique de retour simple, remboursement sans friction
  sous seuil (le coût d'un litige > le coût d'un remboursement).

## 3. Boucle d'automatisation (qui fait quoi, quand)

| Fréquence | Agent | Tâche |
|---|---|---|
| Continu (CI) | theme-designer | `theme check` + Lighthouse sur chaque PR |
| Quotidien | growth-strategist | Lecture analytics (ventes, CPA, taux de conversion) → top 3 actions |
| Quotidien | catalog-manager | Stock fournisseurs / ruptures → passage en rupture propre sur la boutique |
| Hebdo | growth-strategist | Pipeline produits : 2 nouveaux candidats scorés, 1 test lancé, verdicts garder/tuer sur les tests en cours |
| Hebdo | security-guardian | `npm audit`, revue des accès, vérification webhooks |
| Mensuel | agent-auditor | Audit complet : chiffres annoncés vs réels, conformité process |
| À chaque livraison d'agent | agent-auditor | Verdict ✅/⚠️/❌ avant intégration |

Mise en œuvre : routines planifiées (Claude Code web → triggers) invoquant
chaque agent avec sa mission ; les actions d'écriture sur la boutique en
production restent soumises à validation du propriétaire (voir règles de
l'orchestrateur).

### Ce qui reste humain (volontairement)
- Validation des dépenses publicitaires et des budgets de test.
- Validation de la mise en ligne d'un produit (l'IA prépare en DRAFT).
- Choix final des fournisseurs et paiements fournisseurs.
- Litiges clients sensibles.

## 4. Stack technique

- **Boutique** : Shopify (dev store pour construire → plan payant au lancement).
- **Thème** : Skeleton customisé, repo Git dédié ou dossier `theme/` ici,
  connecté via l'intégration GitHub (synchro bidirectionnelle).
- **App maison** (`app/shopify/` existante) étendue avec :
  - page de suivi de commande transparente (différenciant §2) ;
  - tableau de bord CompeteIQ : veille prix des concurrents de la niche
    (notre cœur de métier — la boutique est aussi une vitrine de l'outil) ;
  - webhooks commandes pour alimenter les métriques du growth-strategist.
- **Import produits** : JSONL + `bulkOperationRunMutation` (produits créés en
  DRAFT, activés après validation), médias via CDN Shopify.
- **Analytics** : ShopifyQL (`run-analytics-query` MCP) + Web Pixel plus tard.

## 5. Étapes d'exécution (pipeline agents)

1. **store-setup** : dev store FR (EUR, fr), paiements Bogus/test, zones de
   livraison France (franco dès X €, seuil fixé par le plan de lancement),
   pages légales, marchés BE/CH préparés mais désactivés.
2. **theme-designer** : thème Skeleton + sections ci-dessus, checkout
   accéléré, formulaires, badges, hCaptcha vérifié.
3. **catalog-manager** : import des 10 produits candidats en DRAFT (fiches
   complètes : bénéfices, photos, alt text, tags normalisés), collections,
   activation des 3 produits de test après validation.
4. **store-builder** : page de suivi de commande + webhooks commandes.
5. **growth-strategist** : campagnes de test (protocole du plan de lancement),
   revue hebdo.
6. **security-guardian + agent-auditor** : à chaque étape (voir §3).

Chaque étape se termine par une checklist transmise à la suivante via
l'orchestrateur. Aucune étape n'est « terminée » sans verdict de l'auditeur.
