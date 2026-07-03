# Équipe d'agents — création de boutique Shopify automatisée

Ce repo contient une équipe de **7 agents Claude Code** dans `.claude/agents/`,
coordonnés par un orchestrateur, avec une base de connaissances commune dans
`docs/SHOPIFY_KNOWLEDGE_BASE.md` (synthèse dédupliquée de la documentation
Shopify de juillet 2026).

## L'équipe

| Agent | Étape | Rôle |
|---|---|---|
| `boutique-orchestrator` | Chef | Découpe, délègue, fait se concerter les agents, arbitre, rend compte |
| `store-setup` | 1 | Boutique, réglages, paiements test, livraison, marchés/devises/langues |
| `theme-designer` | 2 | Thème (Skeleton, Liquid, sections), fonctionnalités vitrine, perf/accessibilité |
| `catalog-manager` | 3 | Produits, variantes, collections, médias, imports/exports en masse |
| `store-builder` | 4 | App Shopify intégrée, webhooks, API, backend Next.js |
| `growth-strategist` | 5 | Pricing, conversion, SEO — recommandations chiffrées |
| `security-guardian` | Transverse | Sécurité défensive : secrets, auth, CSP, scopes — peut bloquer |
| `agent-auditor` | Transverse | Surveille les agents : vérifie chaque affirmation par la preuve |
| `scenario-simulator` | Transverse | Simule les scénarios extrêmes (succès brutal, attaque, panne) et produit un plan de préparation |

## Comment ça se concerte

- Chaque agent termine par une **checklist d'état** que l'orchestrateur
  transmet à l'agent suivant — c'est le canal de coordination.
- **Rien n'est livré sans le verdict de `agent-auditor`** (✅/⚠️/❌ avec
  preuves) et, pour tout changement sensible, la revue de `security-guardian`
  ([BLOQUANT]/[IMPORTANT]/[CONSEIL]).
- Les actions irréversibles (publication live, vraies transactions,
  suppressions massives, transfert de boutique) exigent **votre confirmation
  explicite** — aucun agent ne les fait seul.

## Comment lancer l'équipe

Dans une session Claude Code sur ce repo :

- **Mission complète** : « Utilise l'agent boutique-orchestrator pour créer une
  boutique [votre niche] de A à Z sur mon dev store. »
- **Étape précise** : « Utilise theme-designer pour créer un thème à partir de
  Skeleton avec une page d'accueil orientée conversion. »
- **Contrôle** : « Fais vérifier le dernier travail par agent-auditor » ou
  « Fais auditer la sécurité du repo par security-guardian. »

Les agents sont détectés automatiquement depuis `.claude/agents/` dans toute
session (locale ou web) ouverte sur ce repo.

## Automatisation récurrente

Pour une boutique « qui tourne toute seule », combinez les agents avec des
**routines planifiées** (Claude Code sur le web → triggers/cron) — exemples :

- chaque matin : `growth-strategist` analyse les ventes de la veille
  (analytics MCP Shopify) et propose le top 3 d'actions ;
- chaque semaine : `security-guardian` audite le repo + `npm audit` ;
- après chaque push : CI `theme check` + Lighthouse CI (voir KB §3).

## Prérequis conseillés

- Shopify CLI 4.x installée (fait dans cet environnement).
- Plugin **Shopify AI Toolkit** pour donner aux agents les docs/schémas
  officiels : `claude plugin install shopify-ai-toolkit@claude-plugins-official`
  (ou le serveur MCP `shopify-dev-mcp` — voir KB §7).
- Un **dev store** (Dev Dashboard → Stores) avec données de test générées.
- `SHOPIFY_API_KEY`/`SHOPIFY_API_SECRET` dans `.env.local` (voir `.env.example`).

## Limites honnêtes

Les agents travaillent quand une session ou une routine les invoque — ce n'est
pas une surveillance en continu 24 h/24. La protection permanente de la
boutique repose sur : la plateforme Shopify (PCI, hCaptcha), la 2FA sur votre
compte, des scopes minimaux, et des audits réguliers par `security-guardian`.
Aucun agent ne peut garantir « zéro piratage » — l'équipe réduit fortement les
risques et détecte les problèmes tôt.
