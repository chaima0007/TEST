# Rapport de sécurité CompeteIQ — exercice « êtes-vous prêt pour l'attaque »

Date : 2026-07-03 · Périmètre : notre propre code (`/home/user/TEST`), surface Shopify (`app/shopify/`, `lib/shopify/`, `next.config.ts`, `shopify.app.toml`). Cible tierce : aucune.

Méthode : chaque verdict est prouvé par lecture du code (fichier:ligne) et/ou commande exécutée avec sa sortie. Aucun [OK] sans preuve.

---

## 1. Webhook forgé — [OK]

Preuve — `app/api/shopify/webhooks/route.ts:7-12` : le handler `POST` lit le corps brut (`request.text()`), récupère l'en-tête `x-shopify-hmac-sha256`, puis appelle `verifyWebhookHmac(...)` et retourne **`401` avant tout traitement** si la vérification échoue. Le `switch` sur le topic (ligne 17) n'est atteint qu'après validation.

Preuve — `lib/shopify/webhooks.ts:6-15` :
- HMAC-SHA256 calculé sur le corps brut avec le client secret de l'app (`shopifyApiSecret()`).
- En-tête absent → `return false` (ligne 7).
- Comparaison **à temps constant** : `timingSafeEqual` (ligne 15), précédée du contrôle de longueur `received.length === digest.length` (obligatoire, sinon `timingSafeEqual` jette sur des longueurs différentes).
- Décodage base64 protégé par `try/catch` (lignes 10-14).

Verdict : validation HMAC correcte, avant traitement, réponse 401, comparaison à temps constant. Conforme.

Observation mineure [CONSEIL] : `x-shopify-shop-domain` (route.ts:15) est utilisé tel quel dans les requêtes Prisma. Le risque d'injection est nul (Prisma paramètre les requêtes) et l'appel n'est atteint qu'après HMAC valide, mais valider ce domaine via `isValidShopDomain()` serait une défense en profondeur peu coûteuse.

---

## 2. Session token invalide — [OK]

Preuve — `lib/shopify/session-token.ts:27-53`, `verifySessionToken` :
- Format JWT à 3 segments contrôlé (ligne 28-29), sinon `SessionTokenError`.
- **Signature HS256** recalculée avec `shopifyApiSecret()` (lignes 32-34).
- **`timingSafeEqual`** avec contrôle de longueur préalable (ligne 36).
- **`alg === "HS256"`** vérifié (ligne 41) ; comme le digest est imposé côté serveur (sha256), une confusion d'algorithme (`alg: none`/RS256) est impossible.
- **`exp`** contrôlé (ligne 45) avec tolérance d'horloge `CLOCK_SKEW_SECONDS = 10` (ligne 19).
- **`nbf`** contrôlé (ligne 46).
- **`aud === shopifyApiKey()`** contrôlé (ligne 47) — lie le token à notre app.
- **Shop validé `*.myshopify.com`** : `isValidShopDomain(new URL(payload.dest).hostname)` (lignes 49-50), regex ancrée `^[a-zA-Z0-9][a-zA-Z0-9-]*\.myshopify\.com$` (`config.ts:15`).

Preuve — `lib/shopify/authenticate.ts:14-28` : Bearer extrait de l'en-tête `Authorization` (lignes 15-16), token vérifié (ligne 19), shop dérivé du **payload signé** (ligne 20, pas d'un paramètre client). En cas d'échec, `unauthorizedResponse` retourne **`401`** avec `X-Shopify-Retry-Invalid-Session-Request` (lignes 30-37).

Preuve — `app/api/shopify/competitors/route.ts:7-12` : `authenticateShopify` enveloppé dans `try/catch`, toute erreur → `unauthorizedResponse(error)` (401). Aucune donnée servie sans authentification.

Verdict : HS256 + timingSafeEqual + exp/nbf/aud + shop `*.myshopify.com` + 401 sur token invalide. Conforme.

Observation [CONSEIL] : Shopify recommande de vérifier que `iss` et `dest` désignent la même boutique (host match). Ici seul `dest` est utilisé/validé ; ajouter `new URL(payload.iss).hostname === shop` durcirait davantage. Non bloquant : la signature (secret connu de Shopify seul) empêche déjà toute forge.

---

## 3. Fuite de secrets — [OK]

Commande : grep de motifs (`shpat_`, `shpss_`, `shpca_`, `shppa_`, `SHOPIFY_API_SECRET=…`, `password=…`, `api_key=…`) sur `*.ts/tsx/toml/json/env/mjs`.
Résultat : seules correspondances = noms de champs Prisma générés (`lib/generated/prisma/...:password: 'password'`) et types Hydrogen (`.agents/skills/...`). **Aucun secret réel.**

Commande : `git ls-files | grep -iE '\.env'` → **seul `.env.example`** est suivi. `git log --all --diff-filter=A` sur `.env` → **seul `.env.example`** a jamais été ajouté (jamais de `.env.local`).

Commande : `git log -p --all | grep` de valeurs de secrets → les seules correspondances sont du **code source** (`access_token: string;` déclaration de type, `client_secret: shopifyApiSecret()` appel de fonction) et des lignes de documentation/mission. Aucune valeur de secret littérale committée.

Preuve — `.env.example` : contient uniquement des clés vides (`SHOPIFY_API_KEY=`, `SHOPIFY_API_SECRET=`) avec le commentaire « never commit real values ».

Preuve — `.gitignore` : `.env*` ignoré (section « env files »). Le secret ne vit qu'en `.env.local` (runtime via `process.env`, `lib/shopify/config.ts:3-13`). Le client secret n'est utilisé que côté serveur (`webhooks.ts`, `session-token.ts`, `token-exchange.ts`) — jamais exposé au navigateur (`app/shopify/page.tsx` n'y référence aucun secret ; l'appel Admin direct passe par App Bridge `fetch("shopify:admin/...")`, page.tsx:28).

Verdict : aucun secret dans le code ni l'historique, `.env*` ignoré. Conforme.

---

## 4. CSP / clickjacking — [OK]

Preuve — `next.config.ts:3-20` + `49-63` : le site principal (`source: "/((?!shopify).*)"`, ligne 52) reçoit `securityHeaders` incluant **`X-Frame-Options: DENY`** (ligne 5) **et `frame-ancestors 'none'`** (ligne 17).

Preuve — `next.config.ts:25-40` + `55-62` : `/shopify` et `/shopify/:path*` reçoivent `shopifyEmbeddedHeaders`, qui :
- **N'envoient PAS `X-Frame-Options`** (absent de la liste ligne 25-28) — correct pour un embed.
- Autorisent **uniquement** `frame-ancestors https://*.myshopify.com https://admin.shopify.com` (ligne 37).
- Restreignent `script-src`/`style-src`/`font-src` à `'self'` + `https://cdn.shopify.com`.

Le lookahead négatif `(?!shopify)` exclut bien `/shopify` du bloc « site principal », évitant tout conflit d'en-têtes.

Verdict : site principal verrouillé (`frame-ancestors 'none'` + `X-Frame-Options: DENY`), seul `/shopify` ouvre l'iframe admin Shopify. Conforme.

Observation [CONSEIL] : `script-src 'unsafe-inline' 'unsafe-eval'` sur le site principal (ligne 11) affaiblit la protection XSS. Non lié au clickjacking ; à resserrer (nonces) lors d'une itération future si le framework le permet.

---

## 5. Injection GraphQL / validation des entrées — [OK]

Preuve — `lib/shopify/admin.ts:8-21` : `adminGraphql(shop, accessToken, query, variables)` envoie `body: JSON.stringify({ query, variables })` (ligne 20). Les données dynamiques passent par **`variables`**, jamais concaténées dans la chaîne de requête. L'URL utilise `shop`, déjà validé `*.myshopify.com` en amont (dérivé du token signé).

Commande : grep `(query|mutation)…${` dans `app`/`lib` → seule correspondance = un **commentaire de doc Prisma généré** (`lib/generated/prisma/internal/class.ts:150`), pas de code applicatif. **Aucune interpolation dans une requête GraphQL.**

Preuve — `app/shopify/page.tsx:28-32` : la requête côté client est une **constante statique** (`query HomeShopInfo { shop { name } productsCount { count } }`), sans interpolation d'entrée utilisateur.

Preuve — validation du paramètre `shop` : `lib/shopify/config.ts:15-19` (regex ancrée) appliquée dans `session-token.ts:50`. Le `shop` n'est jamais pris d'un paramètre client non vérifié — il provient du `dest` du token signé.

Verdict : variables GraphQL partout, aucune concaténation, `shop` validé par regex stricte issue du token signé. Conforme.

---

## 6. npm audit — [OK]

Commande : `npm audit` → `found 0 vulnerabilities`.
Commande : `npm audit --json` (metadata.vulnerabilities) → `info:0, low:0, moderate:0, high:0, critical:0, total:0`.

Verdict : aucune vulnérabilité haute/critique (ni d'aucun niveau). Conforme. À relancer à chaque revue de dépendances.

---

## 7. Build sain — [OK]

Commande : `npx next build` → `✓ Compiled successfully in 5.0s`, `✓ Finished TypeScript`, `✓ Generating static pages (24/24)`. 24 routes générées, dont `/api/shopify/webhooks`, `/api/shopify/competitors`, `/shopify`.

Verdict : le projet compile et type-check sans erreur. Conforme.

Observation [CONSEIL] non-sécuritaire : avertissement « middleware file convention is deprecated, use proxy » — migration à planifier (voir aussi `middleware.ts`, protection dashboard par cookie).

---

## Tableau récapitulatif

| # | Point audité | Verdict | Preuve principale |
|---|--------------|---------|-------------------|
| 1 | Webhook forgé (HMAC avant traitement, 401, temps constant) | **[OK]** | `route.ts:7-12`, `webhooks.ts:6-15` |
| 2 | Session token (HS256, timingSafeEqual, exp/nbf/aud, shop, 401) | **[OK]** | `session-token.ts:27-53`, `authenticate.ts:14-37`, `competitors/route.ts:7-12` |
| 3 | Fuite de secrets (tree + historique git, `.env*` ignoré) | **[OK]** | grep (0 réel), `git ls-files`/`log`, `.gitignore`, `.env.example` |
| 4 | CSP / clickjacking | **[OK]** | `next.config.ts:5,17,25-40,52-62` |
| 5 | Injection GraphQL / validation `shop` | **[OK]** | `admin.ts:8-21`, `config.ts:15-19`, `session-token.ts:50` |
| 6 | npm audit (hautes/critiques) | **[OK]** | `npm audit` → 0 vulnérabilité |
| 7 | Build sain | **[OK]** | `npx next build` → compiled successfully, 24 routes |

**Aucun constat [BLOQUANT] ni [IMPORTANT].** Livraison non refusée.

### Conseils de durcissement (non bloquants)
- [CONSEIL] `session-token.ts` : vérifier la correspondance `iss`/`dest` (même boutique).
- [CONSEIL] `webhooks/route.ts:15` : valider `x-shopify-shop-domain` via `isValidShopDomain()` (défense en profondeur).
- [CONSEIL] `next.config.ts:11` : retirer `'unsafe-inline'`/`'unsafe-eval'` de `script-src` du site principal (nonces) pour renforcer l'anti-XSS.
- [CONSEIL] `middleware.ts` : la protection dashboard ne vérifie que la présence du cookie `ciq_session`, pas sa validité — s'assurer que chaque handler `/api/*` protégé revalide la session côté serveur ; migrer vers la convention `proxy`.

### Limites de cet audit
Cette revue protège le code et la configuration à l'instant T. La protection continue repose sur la plateforme Shopify (PCI, hCaptcha), la 2FA du propriétaire, le mode test des paiements sur les boutiques de dev, et des audits réguliers. Recommandation : relancer cet exercice (grep secrets, `npm audit`, revue CSP/HMAC/session) à chaque changement sensible.
