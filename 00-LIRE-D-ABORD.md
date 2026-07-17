# 00 — LIRE D'ABORD (passation projet Patchou)

> **Si tu reprends ce projet (humain ou IA), lis CE fichier en premier, puis `ETAT.md`.**

## SYNOPSIS
**Quoi** : boutique dropshipping FR **Patchou** (accessoires chat, produit héros = fontaine à eau, lancement lean <150 € organique). **Pourquoi ce fichier** : point d'entrée unique de la passation, pour ne rien relire inutilement. **État** : préparation complète (code, thème, stratégie, sécurité) **vérifiée** ; la boutique réelle n'existe pas encore — rien n'est en vente.

## Où est quoi (carte du projet)
- **État vivant du projet** → `ETAT.md` (mis à jour à chaque événement).
- **Audit daté le plus récent** → `reports/` (un fichier = un événement, jamais écrasé) + copie Drive.
- **Stratégie** : `docs/PLAN_LEAN_150.md` (décisions verrouillées), `docs/PLAN_CATALOGUE.md`, `docs/PLAN_CONTENU_30J.md`.
- **Architecture & sécurité** : `docs/ARCHITECTURE_BOUTIQUE.md`, `docs/RAPPORT_SECURITE.md`, `docs/RAPPORT_SIMULATION.md`, `docs/FOURNISSEURS.md`.
- **Code app Shopify** : `app/shopify/`, `lib/shopify/`, `app/api/shopify/webhooks/`.
- **Thème vitrine** : `theme/` (Patchou, 46 fichiers, 0 offense theme-check).
- **Équipe d'agents** : `.claude/agents/*.md` (17 agents) — voir `EQUIPE_AGENTS.md`.
- **Drive** : dossier « COMPILATION & SYNOPSIS — Empire Chaima » (id `1qXUj9D9r7HSmIMzMcsScz4Ynlv4auP4G`).

## Protocole obligatoire (à appliquer à CHAQUE livrable)
1. **Vraie date/heure** : `TZ="Europe/Brussels" date` — l'utiliser partout.
2. **Audit honnête** : FAIT / VÉRIFIÉ (avec preuve : test, capture, commande) / RESTE. Ne jamais dire « fini » si ça ne tourne pas.
3. **SYNOPSIS** en tête de chaque document (2-3 lignes : quoi, pourquoi, état).
4. **Titre horodaté** : `AAAA-MM-JJ-HHhMM — [auteur] — [sujet]`.
5. **Copie dans le Drive** (dossier ci-dessus). Sinon, le dire et mettre le rapport dans `reports/`.
6. **Mettre à jour la passation** (`00-LIRE-D-ABORD.md` / `ETAT.md`).
7. **Un document = un événement** ; ajout, jamais d'écrasement. Vérité totale, zéro invention, sources datées.

## Règles non négociables (garde-fous)
- Produits en **DRAFT** tant que le propriétaire n'a pas validé.
- **Aucune transaction / commande fournisseur / dépense réelle** sans accord explicite du propriétaire.
- **Entrepôt UE uniquement** (livraison FR ≤ 10 j) — jamais d'expédition directe Chine sous la promesse « livré 2-4 j ».
- **Pas de dark patterns** : pas de fausse urgence, faux avis, fausse « erreur de prix », ni promesse de résultat garanti.
- **Secrets** uniquement dans `.env.local` (jamais committé).

## Ce que SEUL le propriétaire peut faire (bloquants humains)
1. Créer la boutique Shopify (compte + ~1 €/mois).
2. Connecter Claude à la boutique (OAuth dans claude.ai → Réglages → Connecteurs → Shopify).
3. Réserver le nom : recherche INPI + domaine `patchou.fr` chez un registrar.
4. Commander 1 échantillon fontaine (~35 €).
5. Filmer le contenu (smartphone) et poster @patchou (TikTok/Instagram).
