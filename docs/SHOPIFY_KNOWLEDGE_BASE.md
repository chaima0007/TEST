# Base de connaissances Shopify — CompeteIQ

Synthèse **dédupliquée et organisée** de toute la documentation Shopify fournie
(juillet 2026). Les doublons ont été fusionnés. Chaque agent de `.claude/agents/`
doit consulter la section correspondant à son domaine avant d'agir.

Version d'API de référence : **2026-07** (stable). CLI : **4.x** (SemVer, auto-update).

---

## 1. Développement d'applications

### Deux modèles pour App Home
| | Iframe (hébergé par nous) | Extension UI (hébergée par Shopify) |
|---|---|---|
| Framework | N'importe lequel (notre Next.js) | Preact uniquement |
| Bundle | Illimité | 64 Ko compressés |
| Distribution | Publique et personnalisée | **Personnalisée uniquement** |
| Backend | Complet (webhooks, jobs) | Aucun (cible `admin.app.home.render`) |

**Notre choix : iframe** — implémenté dans `app/shopify/` (voir `SHOPIFY_APP.md`).

### Briques du modèle iframe
- **Session tokens App Bridge** (JWT HS256 signés avec le secret) + **token exchange**
  → access token offline. Implémenté dans `lib/shopify/`.
- **Accès direct API** : `fetch("shopify:admin/api/graphql.json")` côté navigateur,
  activé via `[access.admin] embedded_app_direct_api_access = true` dans le TOML.
- **Polaris web components** (`s-page`, `s-section`, `s-table`…) via
  `cdn.shopify.com/shopifycloud/polaris.js` ; **App Bridge web components**
  (`ui-nav-menu`, `ui-title-bar`, `ui-save-bar`) via `app-bridge.js`.
  Types : `@shopify/polaris-types`, `@shopify/app-bridge-types`.
- **Patterns de pages** : page d'accueil, index, détails, paramètres + compositions
  (guide de configuration, état vide, tableau d'index…). Les respecter aide à
  atteindre **Built for Shopify** (badge, boost App Store, revue prioritaire).
- Scopes : demander **le strict minimum** dans `[access_scopes]`.

### Directives de conception (résumé)
- Navigation dans `ui-nav-menu`, jamais de plein écran lancé depuis la nav.
- Mobile d'abord, accessible, cohérent avec l'admin (Polaris).
- Extensions admin : blocs < 600 px, actions < 1200 px, pas de promo/pub
  (exigence App Store ; idem pour les extensions **Sidekick**, règles 2.2.8/2.2.9).
- Web vitals admin (LCP, INP, CLS) suivis dans le **Dev Dashboard**, seuils
  Built for Shopify.

### CLI applications (4.x)
- `shopify app init` (modèles React Router / extension-only), `shopify app dev`
  (tunnel Cloudflare, dev preview isolée au store choisi, GraphiQL),
  `shopify app dev clean` (retire la preview), `--reset`.
- `shopify app deploy` : publie config + extensions. **CI/CD : `--allow-updates`**
  (le `--force` a été supprimé) ; `--allow-deletes` réservé au manuel.
- **Admin API en CLI** : `shopify app execute --query/--variables` (mutations
  limitées aux dev stores) ; `shopify app bulk execute [--watch]`,
  `app bulk status`, `app bulk cancel`.
- Proxy réseau : `SHOPIFY_HTTP_PROXY` / `SHOPIFY_HTTPS_PROXY`.
- Équipe : une instance d'app dev partagée (`app config link`), **un dev store
  par personne**.

### Webhooks & conformité
- HMAC SHA-256 base64 dans `X-Shopify-Hmac-Sha256`, répondre 200 < 5 s, 401 si invalide.
- Topics obligatoires : `app/uninstalled`, `app/scopes_update` + conformité RGPD
  (`customers/data_request`, `customers/redact`, `shop/redact`).

## 2. Opérations en masse (import/export)

- **Export** : `bulkOperationRunQuery` (requête avec connexions, max 5 connexions,
  2 niveaux d'imbrication, pas de `node`/`nodes` racine). Résultat **JSONL**
  (`__parentId` pour les enfants), URL signée valable 7 jours. À parser **ligne
  par ligne** (streaming), jamais tout en mémoire.
- **Import** : JSONL de variables (1 ligne = 1 exécution de mutation) →
  `stagedUploadsCreate` (resource `BULK_MUTATION_VARIABLES`, mime `text/jsonl`,
  POST multipart, champ `file` en dernier) → `bulkOperationRunMutation`.
  Erreurs rapportées **par ligne** dans le fichier de sortie.
- **Attente** : webhook `bulk_operations/finish` (recommandé) ou polling
  `bulkOperation(id:)` (2026-01+ ; `currentBulkOperation` déprécié).
  Nouvelles requêtes `bulkOperations` (filtres status/type/date, pagination).
- Limites : **5 opérations simultanées par type et par boutique** (2026-01+),
  requêtes ≤ 10 jours, mutations ≤ 24 h, fichier ≤ 100 Mo. Jusqu'à **4× plus rapide**.
- Le coût ne compte pas dans les rate limits (seule la mutation de lancement compte).
- Exemples : dépôt `Shopify/bulk-operations-sample-app`, outil
  `ScreenStaring/shopify-dev-tools` (fixtures de test).

## 3. Thèmes & vitrine

### Outils
- `shopify theme init` (thème **Skeleton**), `theme dev --store X` (127.0.0.1:9292,
  hot reload), `theme push [--unpublished]`, `theme publish`, `theme check`
  (linter, `.theme-check.yml`, `--fail-level` en CI), `theme console` (REPL),
  `theme profile`.
- Éditeur : extension VS Code Shopify Liquid (complétion, Theme Check, hover),
  plugin **Prettier Liquid**, **LiquidDoc** (`{% doc %}` + `@param`/`@example`,
  validation des `render`).
- Perf : **Theme Inspector** Chrome (flame graph Liquid), **Lighthouse CI GitHub
  Action** (`shopify/lighthouse-ci-action@v1`, secrets `SHOP_CLIENT_ID`/`SECRET`/
  `SHOP_STORE`/`SHOP_PASSWORD`, seuils perf 0.6 / accessibilité 0.9).
- **Intégration GitHub** : branche ↔ thème, synchro bidirectionnelle (commits du
  bot `shopify` pour les changements admin), structure de dossiers standard requise.
- **Theme Access app** : mots de passe scoped `write_themes` pour les développeurs
  (`SHOPIFY_CLI_THEME_TOKEN` en CI, lien à usage unique, 7 jours).

### Liquid (essentiel)
- `{{ objet }}` sortie, `{% tag %}` logique, filtres chaînés gauche→droite.
- Éditeur de thèmes : réglages dans `settings_schema.json` + sections/blocs JSON ;
  live preview couleurs/textes soumise à contraintes (pas de filtre Liquid sur le
  réglage, valeur seule dans son parent) ; détection éditeur :
  `request.design_mode` (Liquid), `Shopify.designMode` (JS).
- Overrides par marché dans l'éditeur (réglages/visibilité/ordre) — un override
  casse l'héritage du Default sur ce point précis.
- Nouveau réglage **`color_palette`** (recommandé, cf. Horizon 4.0).

### Événements & actions standards vitrine
- Événements DOM `shopify:*` émis par le thème (`page:view`, `product:view/select`,
  `cart:view/lines-update/note-update/discount-update/error`, `collection:*`,
  `search:update`) — payloads camelCase type Storefront API, promesses différées
  pour l'asynchrone. Bibliothèque : `cdn.shopify.com/storefront/standard-events.js`.
- Actions `Shopify.actions.getCart/updateCart/openCart` (défauts Storefront API,
  configurables par le thème, `updateCart` auto-émet les événements ; vérifier
  `userErrors`/`warnings`). Debug : `shopify theme dev --standard-events-inspector`.

### Fonctionnalités à implémenter dans un thème
- **Merchandising** : variantes, médias (images/vidéo/3D `model_source` GLB ~4 Mo,
  max 15 Mo), recommandations, cartes cadeaux, bundles.
- **Prix/paiements** : réductions (`discount_application`/`discount_allocation`,
  prix barrés ligne + panier), prix unitaire (`unit_price_with_measurement`),
  abonnements/précommandes/TBYB (plans de vente), checkout accéléré
  (`{{ form | payment_button }}`, `content_for_additional_checkout_buttons`,
  custom properties CSS `--shopify-accelerated-checkout-*`),
  Shop Pay Installments (`{{ form | payment_terms }}`, `data-cart-subtotal`).
  ⚠️ Shopify Scripts : **fin de vie 30 juin 2026**.
- **Engagement** : newsletter `{% form 'customer' %}` (`contact[email]`),
  formulaire de contact `{% form 'contact' %}` (email requis, champs `contact[...]`).
- **Livraison** : afficher la disponibilité du retrait local sur les pages produits.
- **Confiance/sécurité** : hCaptcha automatique (formulaires `form_type` ; forçage
  `data-shopify-captcha="true"` ou `window.Shopify.captcha.protect`, ne jamais
  toucher `window.hCaptcha` directement), badges PCI (SVG clair/sombre).

## 4. Markets & international

- **Localisation** : jusqu'à 20 langues, sélecteurs `{% form 'localization' %}`
  (`country_code`, `language_code`, seulement si > 1 option), URLs dynamiques
  (`routes.cart_url`, `window.Shopify.routes.root`) — **jamais d'URL en dur**,
  hreflang automatique via `content_for_header`, `priceCurrency` = devise du panier
  dans les données structurées. Traductions : app Translate & Adapt ou CSV
  (tags non traduisibles). Checkout pré-traduit en 33 langues.
- **Devises par marché** : taux automatiques (frais 1,5 % US/UK/EEE ou 2 % ailleurs,
  inclus dans le prix affiché) ou manuels (frais déduits du versement, à intégrer
  au taux), arrondis psychologiques, remboursements convertis **au taux du jour**
  (risque de change), rétrofacturations idem.
- **Markets API 2026-07** : `Market.delivery.shipping` (options forfait/valeur/
  poids/transporteur via `marketCreate`/`marketUpdate`, scopes `read/write_markets`),
  marchés de canaux (`MarketType.CHANNEL`), transport orienté marché (les API
  `deliveryProfile*` marchandes deviennent obsolètes — rollout 1er oct. 2026 →
  1er juil. 2027).
- Apps **canal de vente** : extension `channel_config` + spécifications
  (pays/langues/devise, capacités, `merchantOfRecord`), attribution des commandes
  (`Order.attribution`, `Order.channelInformation` déprécié).

## 5. Business Partenaire & boutiques clientes

- **3 types de boutiques** (Dev Dashboard → Stores) : *dev store* (tests, données
  générées, mot de passe non retirable), *boutique de transfert client* (gratuite,
  sans limite de temps, commission récurrente après transfert — **jamais d'essai
  gratuit**), *collaboration* (boutique du marchand, accès limité, expire après
  90 jours sans connexion).
- **Accès** : compte collaborateur recommandé (code à 4 chiffres possible),
  **jamais les identifiants du marchand**.
- **Tests de commandes** (transfert client) : Bogus Gateway (carte `1`=succès,
  `2`=échec, `3`=exception) ou mode test Shopify Payments (cartes 4242…),
  **jamais de vraies transactions**, ni cartes cadeaux/store credit/draft orders.
- Étapes : créer la boutique → thème → migration/import produits (CSV, Matrixify
  pour Plus) → collections → paiements/livraison → transfert → suivi (Referrals).
- POS : synchronisé automatiquement avec la boutique en ligne ; leads via le
  Partner Dashboard.
- Modèles 3D pour marchands : photos multi-angles + dimensions mm, GLB ~4 Mo,
  checklist qualité (échelle réelle, quads, PBR, UV 1:1).

## 6. Changelog 2026-07 — points de vigilance

| Changement | Impact CompeteIQ |
|---|---|
| Collections multi-sources (`Collection.sources` remplace `ruleSet`) | Aucun (on ne lit pas les collections) |
| Transport orienté marché (dépréciation `deliveryProfile*` marchands) | Aucun |
| `marketingEngagementCreate.isCumulative` déprécié | Aucun |
| Carrier services plus auto-ajoutés au profil général (2026-10) | Aucun |
| `priceRule` supprimé (2026-10) → `discountTitle`/`discountCode` | Aucun |
| Storefront MCP cart tools → **UCP Cart MCP** (31 août 2026) | Aucun |
| Extensions checkout/comptes clients → Polaris web components **avant le 1er oct. 2026** | Notre App Home est déjà en web components |
| Retours/abonnements : API compte client obligatoire (BFS, 1er déc. 2026) | Aucun (pas de flux acheteurs) |
| `shippingLabelPurchase` (achat d'étiquettes, scope `write_orders` + permission) | Opportunité future |
| Metafields d'app : définition requise pour l'API compte client | Aucun |
| Intents API : `pick:shopify/File` (sélecteur de fichiers natif) | Opportunité App Home |
| Sidekick app extensions ouvertes à tous | Opportunité (« quels concurrents ont bougé ? ») |

## 7. Outillage IA

- **Shopify AI Toolkit** (recommandé) : plugin Claude Code
  `claude plugin install shopify-ai-toolkit@claude-plugins-official`,
  ou skills `npx skills add Shopify/shopify-ai-toolkit`,
  ou MCP `claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest`.
  Donne accès aux docs, schémas d'API et validation de code officiels.
- Le serveur MCP Shopify connecté à cette session expose déjà :
  produits/collections/commandes/clients/inventaire/analytics/GraphQL Admin
  (`mcp__Shopify__*`).
