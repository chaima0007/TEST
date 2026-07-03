# Rapport de simulation de crise — Build CompeteIQ Commerce

**Date : 2026-07-03 · Périmètre : nos propres systèmes uniquement (code, config, boutique). Aucun test contre une cible tierce ou la prod Shopify.**
**Convention : [mesuré] = commande exécutée / source citée ; [estimation] = raisonnement chiffré. Aucun taux de succès inventé.**

Environnement de preuve : repo `/home/user/TEST`, `next build` local, `npm audit`, scripts de reproduction Node, lecture de code ligne à ligne.

---

## Partie A — Scénarios ATTAQUE (défensif, prouvés sur notre code)

### Scénario 1 — IDOR sur `/suivi/[orderId]` : la correction tient-elle ?

**Verdict : PRÊT**

1. **Token requis (`?k=`) en boutique réelle.** `lib/shopify/tracking.ts:296-299` : après résolution d'une vraie boutique, `if (!expectedToken) return null; if (!key || !tokensMatch(expectedToken, key)) return null;`. La page `app/suivi/[orderId]/page.tsx:114-115` fait `notFound()` sur `null`. Sans `k` valide → 404, aucune donnée.
2. **Comparaison à temps constant.** `tracking.ts:251-256` (`tokensMatch`) : test de longueur explicite **avant** `timingSafeEqual`, pas de court-circuit révélant le timing.
3. **Aucun appel Admin avant validation.** `fetchOrderTrackingFromAdmin` (ligne 301) n'est atteint **qu'après** la validation du token. Réponse identique (`notFound`) que la commande existe ou non tant que le token n'est pas prouvé → pas d'oracle d'énumération.
4. **Mode démo préservé.** `tracking.ts:285-291` : si aucune boutique connectée, données 100 % fictives, `isDemo:true`, bandeau d'avertissement. Aucune fuite.
5. **Purge RGPD.** `webhooks/route.ts:124-129` (`shop/redact`) supprime `shopifyShop` **et** `orderTracking` du shop. `customers/redact` documenté (aucune PII client dans le modèle).

Preuves d'exécution : `next build` VERT ; `npm audit` → 0 vulnérabilité ; grep secrets (tree + historique) → aucun ; `.env*` ignoré.

### Scénario 2 — Webhook forgé (HMAC)

**Verdict : PRÊT**

Verrou en tête de `POST` (`webhooks/route.ts:63-67`), avant lecture topic/shop et tout accès base. Reproduction :
```
401 REJETE  <- Aucun header HMAC
401 REJETE  <- Header vide
401 REJETE  <- Mauvais HMAC
401 REJETE  <- HMAC malformé (non-base64)
200 ACCEPTE <- Bon HMAC
```
Comparaison temps constant (`webhooks.ts:15`) ; `isValidShopDomain` re-valide après HMAC (`route.ts:74`) ; JSON parsé en try/catch → 400.

### Scénario 3 — Fraude / card testing (analyse sur table)

**Verdict : FRAGILE** — défenses dépendantes d'une plateforme/config pas encore activées (boutique non créée).

- hCaptcha Shopify : spécifié (livrable theme-designer) mais **pas encore intégré au thème**.
- Shopify Payments fraud filters + Shopify Protect : natifs mais inactifs tant que la boutique n'existe pas.
- Card testing vise le checkout hébergé (que notre code ne touche pas) — protégé côté plateforme.
- **Aucune règle d'alerte chiffrée** (N tentatives échouées → notification owner). Le « SAV < 24 h » est un délai de réaction humaine, pas de détection.

**Actions :** activer hCaptcha + fraud rules + Shopify Protect à la création (store-setup) ; intégrer hCaptcha au thème (theme-designer) ; définir une règle d'alerte chiffrée (security-guardian).

---

## Partie B — Scénarios SUCCÈS (analyse chiffrée)

### Scénario 4 — Pic viral ×50

**Verdict : PAS PRÊT** (stock, trésorerie, SAV).

- **Stock — PAS PRÊT.** Sync BigBuy « carriers » 1,1/5, plaintes « 99 % out of stock » (`FOURNISSEURS.md`). Stock affiché ≠ réel → oversell si la politique d'inventaire n'est pas « refuser » (deny) + tampon manuel.
- **Trésorerie — PAS PRÊT.** On paie le fournisseur d'avance, payout Shopify à T+3/T+5 j [estimation]. Seuil de rupture ≈ `trésorerie / (coût_fournisseur × jours_payout)`. Avec 1 500 € : `1500 / (15 × 5) ≈ 20 commandes/jour` avant d'être à sec. Un ×50 (≈240 cmd/j) = ~3 600 €/j de sortie fournisseur = **2,4× le budget total dès le jour 1**. La trésorerie casse le premier jour.
- **SAV — FRAGILE.** La page `/suivi` dévie une partie des tickets, mais ×50 sur un owner solo sature.

**Actions :** politique stock « deny » + tampon + contrôle manuel (dropship-ops/catalog-manager) ; plafonner la montée pub au seuil trésorerie (growth-strategist) ; macros SAV + FAQ (store-builder).

### Scénario 5 — Défaillance fournisseur / rupture

**Verdict : FRAGILE** (redondance conçue mais non exécutée).

Principal BigBuy → secours CJ (app 4,9/5) : bascule **plausible mais non prouvée** (aucun échantillon commandé, dispo UE non vérifiable sans compte). **Brosse vapeur = maillon faible UE confirmé** : si pas de SKU UE ≤ 10 j → retirer ou remplacer (gamelle anti-glouton / rouleau anti-poils).

**Actions :** exécuter la checklist §5 `FOURNISSEURS.md` (échantillons principal+secours) ; trancher la brosse vapeur en priorité ; documenter la procédure de bascule.

### Scénario 6 — Passage à l'échelle BE / CH

**Verdict : PAS PRÊT** (traduction + logistique CH).

`theme/locales/` = `fr.default.json` uniquement. BE nécessite le NL (moitié du marché) ; CH est **hors UE** (douane, TVA import, CHF → frais conversion 1,5-2 %) → casse la promesse « livré 2-4 j ».

**Actions :** ajouter `nl.default.json` avant BE (copy-editor/theme-designer) ; configurer Shopify Markets BE (store-setup) ; traiter la CH séparément (douane/DDP, marge post-conversion) ; **BE d'abord, CH seulement si validée**.

---

## Tableau de préparation global

| # | Scénario | Verdict | Action prioritaire (agent) |
|---|----------|---------|----------------------------|
| 1 | IDOR `/suivi/[orderId]` | **PRÊT** | Valider query fulfillments sur schéma live (store-builder) |
| 2 | Webhook forgé (HMAC) | **PRÊT** | Garder le script en non-régression (security-guardian) |
| 3 | Fraude / card testing | **FRAGILE** | hCaptcha + fraud rules + règle d'alerte (store-setup, security-guardian) |
| 4 | Pic viral ×50 | **PAS PRÊT** | Politique stock « deny » + tampon + plafond de scale (dropship-ops, growth-strategist) |
| 5 | Défaillance fournisseur | **FRAGILE** | Échantillons + trancher la brosse vapeur (catalog-manager, dropship-ops) |
| 6 | Échelle BE/CH | **PAS PRÊT** | NL avant BE ; CH séparée (copy-editor, store-setup) |

**Synthèse honnête :** le **code** (scénarios 1-2) est solide et prouvé. La **fragilité réelle est opérationnelle, pas technique** : trésorerie sous pic, fiabilité fournisseur non encore mesurée, hCaptcha/alertes à activer, i18n à construire. Tous bloqués en amont par la création de la boutique et l'exécution de la checklist fournisseurs.
