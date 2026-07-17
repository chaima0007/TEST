# ETAT — projet Patchou (état vivant)

> Mis à jour à chaque événement. Dernier point : **2026-07-17 21h52 CEST**.
> Lire d'abord `00-LIRE-D-ABORD.md`.

## SYNOPSIS
**Quoi** : où en est réellement le projet Patchou, maintenant. **Pourquoi** : éviter de relire tout le dépôt pour savoir quoi faire ensuite. **État** : prêt à l'allumage, boutique non créée, en attente de gestes propriétaire.

## Feu tricolore
- 🟢 **Code / thème / stratégie / sécurité** : faits et vérifiés (voir dernier audit `reports/`).
- 🟠 **Opérationnel** : dépend d'une boutique réelle + d'un échantillon reçu.
- 🔴 **En vente** : non. Aucune commande possible tant que la boutique n'existe pas.

## Prochaine action attendue (ordre)
1. **Propriétaire** : créer la boutique Shopify + connecter le connecteur claude.ai.
2. **Propriétaire** : commander 1 échantillon fontaine (~35 €).
3. **Claude (dès connexion)** : pousser le thème, importer la vague 1 en DRAFT, config FR/EUR/livraison/pages légales.
4. **dropship-ops + propriétaire** : valider l'échantillon (délai ≤ 10 j, CE, TVA, white-label) avant toute publication.

## Journal (un événement = une ligne, ajout seulement)
| Date/heure (CEST) | Auteur | Événement | Preuve / lien |
|---|---|---|---|
| 2026-07-17 21h38 | Claude | Audit honnête FAIT/VÉRIFIÉ/RESTE créé | `reports/2026-07-17-21h38-Claude-audit-patchou.md` |
| 2026-07-17 21h46 | Claude | Copie de l'audit déposée sur le Drive « Empire Chaima » | docs.google.com/document/d/1M0RKDE53preiE4zjfZvnnSwZeLCTTBo1KQFHPDq4ScA |
| 2026-07-17 21h46 | Claude | Passation créée (`00-LIRE-D-ABORD.md`, `ETAT.md`) | ce dépôt |
| 2026-07-17 21h52 | Claude | Doublon Drive tranché : « Empire Chaima » canonique, ancien dossier obsolète (non détruit) | `ETAT.md` §Convention Drive |

## Point de vigilance connu
- **Décalage d'horloge** : les commits Git portent `2026-07-03` (horloge du bac à sable). L'heure réelle des rapports est prise via `TZ="Europe/Brussels" date` et recoupée avec le `createdTime` Drive. Chronologie relative des commits = exacte.

## Convention Drive (décision tranchée le 2026-07-17 21h52)
- **Dossier CANONIQUE unique** = « COMPILATION & SYNOPSIS — Empire Chaima » (id `1qXUj9D9r7HSmIMzMcsScz4Ynlv4auP4G`). **Tout audit/synopsis va là, nulle part ailleurs.**
- **Obsolète — NE PLUS UTILISER** : « Patchou — Projet Dropshipping » (id `1t-jBq9yHNMSC_o12Z0EZvxB2P7yUNwRF`), créé avant le protocole. Laissé en place (les outils Drive dispo ne permettent ni renommage ni suppression) mais aucun nouveau dépôt n'y est fait. Le propriétaire peut le supprimer manuellement s'il le souhaite.
