# État du projet — source de vérité unique

**But de ce fichier** : que chaque agent sache *où il en est* en **une seule lecture**,
sans relire tous les docs. Mis à jour par l'orchestrateur après chaque étape.
Dernière mise à jour : 2026-07-03.

> Règle : un agent lit d'abord CE fichier, puis seulement la ou les sections de
> `docs/` qui concernent sa tâche du moment. Ne pas tout relire.

---

## 1. Où en est le projet (vue d'ensemble)

| Volet | État | Où |
|---|---|---|
| Base de connaissances Shopify | ✅ Fait | `docs/SHOPIFY_KNOWLEDGE_BASE.md` |
| Plan de lancement (niche, produits, protocole) | ✅ Fait | `docs/PLAN_LANCEMENT.md` |
| Architecture boutique + différenciant | ✅ Fait | `docs/ARCHITECTURE_BOUTIQUE.md` |
| Benchmark concurrents + actions | ✅ Fait | `docs/BENCHMARK_CONCURRENTS.md` |
| App Shopify intégrée (auth, webhooks) | ✅ Fait, build vert | `app/shopify/`, `lib/shopify/` |
| Couche autonomie (suivi commande) | ✅ Construit, revue sécu en cours | `app/suivi/`, `lib/shopify/tracking.ts` |
| Sécurité du code | ✅ 7/7 OK + 3 durcissements | `docs/RAPPORT_SECURITE.md` |
| Thème vitrine (Skeleton customisé) | 🔨 En construction | `theme/` |
| **Boutique Shopify réelle** | ⛔ **Bloqué : inscription requise** | (clic propriétaire sur un aperçu) |
| Produits en ligne | ⛔ Dépend de la boutique | — |
| Campagnes pub / SEO actifs | ⛔ Dépend de la boutique | — |

**Chemin critique** : le seul blocage dur est la **création du compte Shopify**
(clic du propriétaire sur le lien d'inscription d'un aperçu). Tout le reste
s'exécute ou se prépare sans lui.

---

## 2. Où en est chaque agent (dernière livraison → prochaine action)

| Agent | Dernière livraison | Prochaine action quand… |
|---|---|---|
| **boutique-orchestrator** | Coordination, commits, ce fichier | Lance audit + simulation à la fin du thème |
| **growth-strategist** | Plan de lancement + benchmark | Routine hebdo (recherche produit + spy) une fois la boutique live |
| **store-builder** | Couche autonomie (suivi commande) | Vérifier query `order→fulfillments` contre le schéma live (dev store) |
| **theme-designer** | (en cours) thème Skeleton | Intégrer fiche produit modèle (benchmark §4) + bandeau livraison |
| **catalog-manager** | — (rien encore) | Créer les 3 fiches héros en DRAFT dès la boutique live |
| **store-setup** | — (rien encore) | Config FR/EUR, livraison, pages légales dès la boutique live |
| **seo-strategist** | Créé | Fondations SEO (balises, données structurées, blog) sur le thème |
| **security-guardian** | Audit 7/7 + durcissements ; (revue autonomie en cours) | Revoir chaque changement sensible avant prod |
| **agent-auditor** | — | Audit complet de l'état final (après thème) |
| **scenario-simulator** | Créé | Simuler succès + attaque sur le build complet (après thème) |
| **ops-doctor** | Diagnostic connexion Shopify | Rediagnostiquer si un connecteur retombe |
| **marketing-ads** | Créé (ancré benchmark) | Scripts créas + funnel + e-mails dès les fiches prêtes |
| **brand-designer** | Créé (ancré benchmark) | Système de design/typo, en coordination avec theme-designer |
| **copy-editor** | Créé | Relecture FR de tous les textes clients (thème, fiches, e-mails) |
| **dropship-ops** | Créé | Sourcing fiable, traitement commandes, marge réelle, retours |

---

## 3. Leviers de rentabilité — état (issus du benchmark, à maximiser)

| Levier | Source | État | Responsable |
|---|---|---|---|
| Fiche produit haute conversion | benchmark §4 | Modèle prêt, à intégrer au thème | theme-designer + catalog-manager |
| Différenciant livraison transparente | archi §2 | Code fait, à afficher sur chaque fiche | theme-designer |
| Bundles pour AOV → 50 € | benchmark §5.3 | Spécifié, non construit | catalog-manager + theme-designer |
| Upsell post-achat 1-clic | benchmark §5.2 | À faire | store-builder |
| TikTok organique (dé-risque Meta) | benchmark §5.1 | Stratégie prête, exécution humaine | growth-strategist (specs) |
| Protocole de test 100 €/produit | plan §3 | Prêt, attend la boutique | growth-strategist |
| SEO longue traîne + blog | benchmark §3-7 | À démarrer sur le thème | seo-strategist |
| Séquences e-mail (bienvenue, panier, réachat) | benchmark §5.2 | À spécifier | growth-strategist → store-builder |

---

## 4. Décisions en attente du propriétaire (bloquantes pour la prod)

1. **Créer la boutique** (clic sur un aperçu) — débloque tout le reste.
2. Confirmer budget (1 500 €) et niche (accessoires animaux).
3. Valider la grille de prix (44,90 / 32,90 / 21,90 €) et le seuil de franco (49 €).
4. Valider la politique de retours 30 jours.
5. Toute mise en ligne de produit / lancement de promo / dépense pub.

---

## 5. Règles permanentes (rappel, ne pas les re-déduire)

- Rien en production sans validation explicite du propriétaire (actions
  irréversibles : publication, vraies transactions, suppressions de masse).
- Aucun dark pattern (fausse urgence/rareté, faux avis, prix gonflés).
- Chaque livrable passe par agent-auditor ; les changements sensibles par
  security-guardian (peut bloquer).
- Chiffres toujours marqués [mesuré] vs [estimation] ; sources citées.
- Build toujours vert ; `theme check` sans erreur.
