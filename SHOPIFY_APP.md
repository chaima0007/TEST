# CompeteIQ — application Shopify intégrée

CompeteIQ s'exécute aussi comme **application intégrée dans l'admin Shopify** (modèle
iframe App Home), construite sur la stack Next.js existante du projet — le chemin
« votre propre pile technologique » de la documentation Shopify.

## Architecture

| Élément | Emplacement | Rôle |
| --- | --- | --- |
| Configuration de l'app | `shopify.app.toml` | Scopes, webhooks, accès direct API, URLs |
| UI intégrée (App Home) | `app/shopify/` | Pages Polaris web components + App Bridge, rendues dans l'iframe admin |
| Authentification | `lib/shopify/` | Vérification des session tokens App Bridge + token exchange (installation gérée par Shopify, sans redirection OAuth) |
| API authentifiées | `app/api/shopify/competitors` | Données CompeteIQ pour la surface intégrée (Bearer session token) |
| Webhooks | `app/api/shopify/webhooks` | `app/uninstalled`, `app/scopes_update`, `fulfillments/create`, `fulfillments/update` + topics de conformité RGPD (HMAC vérifié) |
| Suivi de commande | `app/suivi/[orderId]` + `lib/shopify/tracking.ts` | Page publique de transparence logistique (statut + date estimée), hors admin et hors `/shopify` |
| Persistance | `prisma/schema.prisma` → `ShopifyShop`, `OrderTracking` | Access tokens offline par boutique ; dernier état de suivi par commande |

Points notables :

- **Session tokens** : App Bridge intercepte `fetch()` et ajoute `Authorization: Bearer <jwt>`
  aux appels same-origin. `lib/shopify/session-token.ts` vérifie le JWT (HS256, signé avec
  le secret de l'app) ; `lib/shopify/token-exchange.ts` l'échange contre un access token
  offline stocké en base.
- **Accès direct à l'API Admin** : activé dans le TOML (`embedded_app_direct_api_access`),
  la page d'accueil interroge `shopify:admin/api/graphql.json` directement depuis le
  navigateur (nom de la boutique, nombre de produits).
- **En-têtes de sécurité** : le site principal garde `frame-ancestors 'none'`, mais
  `next.config.ts` sert au segment `/shopify` une CSP avec
  `frame-ancestors https://*.myshopify.com https://admin.shopify.com` et autorise
  `cdn.shopify.com` (App Bridge + Polaris), sans `X-Frame-Options`.
- **Navigation** : le menu latéral de l'app (`ui-nav-menu`) est déclaré dans
  `app/shopify/layout.tsx` (Accueil, Concurrents, Paramètres), conformément aux
  directives de conception d'applications.
- **Transparence logistique** : la page publique `/suivi/[orderId]` affiche la
  progression d'une commande (confirmée → expédiée → en livraison → livrée) et la
  date estimée. `lib/shopify/tracking.ts` lit d'abord la boutique connectée (Admin
  API, query `order` → `fulfillments`) et, tant qu'aucune boutique n'est reliée,
  sert des données de démonstration typées (bannière « aperçu »). Les webhooks
  `fulfillments/create|update` mettent à jour le modèle `OrderTracking`.
- **Accès par token (anti-IDOR)** : dès qu'une vraie boutique est connectée, la
  page exige un token de suivi non devinable passé en query string :
  `/suivi/<orderId>?k=<token>`. Le token est généré une seule fois par
  `fulfillments/create` (champ `OrderTracking.token`), conservé sur les updates
  suivants, et comparé en temps constant (`crypto.timingSafeEqual`). Sans token
  valide → `notFound()`, et aucun appel Admin API n'est émis (pas d'oracle
  d'énumération). Le lien complet — avec `?k=<token>` — devra être intégré au
  futur e-mail de confirmation d'expédition. Le mode démo reste accessible sans
  token (données fictives).
- **RGPD** : `shop/redact` purge `ShopifyShop` puis `OrderTracking` du shop.
  `customers/redact` ne purge pas `OrderTracking` : ce modèle ne contient aucune
  PII client (orderId, statut, URL transporteur, token aléatoire) — choix assumé.

## Réglages ajoutés

- **Scope `read_orders`** (`shopify.app.toml`) : requis pour lire les fulfillments
  d'une commande et recevoir les webhooks `fulfillments/*`. À faire valider par
  security-guardian (changement de scope). L'app demande toujours le minimum :
  `read_products,read_orders`.
- **`SHOPIFY_STORE_DOMAIN`** (optionnel, `.env.local`) : domaine
  `xxx.myshopify.com` de la boutique servie par la page publique de suivi. Non
  secret. S'il est absent, `lib/shopify/tracking.ts` prend la seule boutique
  installée en base ; s'il n'y en a aucune, la page bascule en mode démo. Ne jamais
  mettre d'identifiant/secret ici.

## Prérequis

- Node.js 18+, la dernière version de Shopify CLI (4.x) :

  ```bash
  npm install -g @shopify/cli@latest
  ```

  Depuis la CLI 4.0 (SemVer), la CLI se met à jour automatiquement via votre gestionnaire
  de paquets (sauf en CI). Pour désactiver : `shopify config autoupgrade off`.
- Un compte avec permissions de développement d'apps et un **dev store**.
- Derrière un proxy réseau : `export SHOPIFY_HTTP_PROXY=http://proxy:8080`
  (et `SHOPIFY_HTTPS_PROXY` si distinct).

## Première configuration

1. Copiez `.env.example` vers `.env.local`.
2. Liez le projet à une app du Dev Dashboard (crée/complète `client_id` dans le TOML) :

   ```bash
   shopify app config link
   ```

3. Renseignez `SHOPIFY_API_KEY` / `SHOPIFY_API_SECRET` dans `.env.local` avec les
   identifiants client de l'app (Dev Dashboard → votre app → paramètres client).
4. Initialisez la base locale : `npx prisma db push` (ou `npm run db:push`).

## Tester localement (`shopify app dev`)

```bash
shopify app dev
```

La CLI :

- vous connecte à votre compte développeur et vous fait choisir un dev store ;
- démarre ce serveur Next.js et crée un tunnel HTTPS (Cloudflare) ;
- met à jour l'URL de l'app pour le dev store choisi
  (`automatically_update_urls_on_dev = true` — isolé à ce store) ;
- pousse la configuration TOML en *dev preview* sur le store ;
- sert GraphiQL pour l'API Admin avec les scopes de l'app.

Appuyez sur `p` pour ouvrir l'URL de prévisualisation, puis **Installer l'app** sur le
dev store. Les requêtes de l'admin arrivent sur `/` avec `?shop=&host=` et le middleware
les redirige vers la surface intégrée `/shopify`.

Après l'arrêt de `app dev`, la *dev preview* reste active sur le store. Pour la nettoyer
(restaure la version active de l'app) :

```bash
shopify app dev clean
```

Pour changer d'organisation, d'app ou de store : `shopify app dev --reset`.
En équipe : une instance d'app de dev partagée (via `app config link`), mais **un dev
store par personne**, car `app dev` pousse la config sur le store choisi.

## Déployer

```bash
shopify app deploy
```

Publie une nouvelle version de l'app (configuration incluse,
`include_config_on_deploy = true`). En CI/CD, utilisez `--allow-updates` — le drapeau
`--force` a été supprimé dans la CLI 4.0 ; réservez `--allow-deletes` aux exécutions
manuelles car les suppressions d'extensions sont irréversibles.

L'hébergement du serveur Next.js (Vercel, etc.) reste à votre charge : mettez à jour
`application_url` et `redirect_urls` avec l'URL de production avant le déploiement.
