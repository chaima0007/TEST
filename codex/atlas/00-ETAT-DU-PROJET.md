# ATLAS — ÉTAT DU PROJET

> Mis à jour à la fin de chaque session. Reprendre ici sans relire l'historique.
> Dernière mise à jour : **2026-09-16**.

## FAIT (VÉRIFIÉ)

- **2026-09-16** — 10 agents créés et poussés : 7 experts de domaine (`atlas-materiel`,
  `atlas-runtime-llm`, `atlas-rag-memoire`, `atlas-finetuning`, `atlas-systemes-reseaux`,
  `atlas-mlops`, `atlas-chercheur-sources`) + 3 sentinelles (`sentinelle-exfiltration`,
  `sentinelle-perimetre`, `sentinelle-derive`). Anti-doublon §9 justifié agent par agent.
- **2026-09-16** — Gouvernance en place, **rangée en sous-dossiers** à la demande de Chaima :
  `ROUTAGE.md` (où va quoi) · `snapshots/` · `audits/` · `erreurs/` · `apprentissage/` ·
  `memoire/` · `corpus/` · `mesure/` · `continuite/`. Règle R-007 : un type = un dossier =
  **un seul fichier vivant**, ajout en tête, jamais de fichier daté par événement.
- **2026-09-16** — `continuite/RESTAURATION.md` : réponse honnête à « inarrêtable » — la
  machine s'arrête toujours, la **connaissance** ne doit pas. 3 copies + restauration testée +
  les 4 pannes qui arrêtent vraiment un système local, chacune avec son responsable.
- **2026-09-16** — `memoire/PROFIL-CHAIMA.md` ouvert : 6 faits VÉRIFIÉS (dits par elle),
  6 points bloquants NON VÉRIFIÉS, et le signal Windows du Drive explicitement **écarté**.
- **2026-09-16** — Drive rangé : dossier **ATLAS — IA locale (Empire Chaima)**
  (`1Ual-L_FKyitVvi71bQph51-gpOQeq4Ao`) contenant `01 — FICHE MACHINE — À REMPLIR`
  (`1GRzD4Oow7O8wWjg-Dv3iirUbmlYpKyilyek0YsVOl20`, **contenu relu après écriture**) et
  `02 — ERREURS ET RÉUSSITES — ATLAS`.
- **2026-09-16** — Table de routage d'`orchestrateur` étendue aux domaines ATLAS.
- **2026-09-16** — Document Drive ouvert et **vérifié** (contenu relu après écriture) :
  `🔴 ERREURS ET RÉUSSITES — ATLAS (IA locale) — ouvert le 2026-09-16`,
  ID `1cKad7xISrny7R5KGr1hseX0HlOUWATHQ3QfvhlCDZkU`, dans le dossier
  `1qXUj9D9r7HSmIMzMcsScz4Ynlv4auP4G` (le même que la base d'erreurs Nexus-Market).
  Procédure de remontée : `codex/atlas/continuite/SYNC-DRIVE.md`.

## EN COURS

- **ÉTAPE 0 — diagnostic matériel. Toujours ouverte, c'est le seul blocage.**
  Cherché dans le Drive le 2026-09-16 : **les caractéristiques machine n'y sont pas**. Une
  fiche vide a donc été créée pour que Chaima la remplisse (`01 — FICHE MACHINE`). Bloque tout
  le reste : aucun modèle, runtime ni quantification ne peut être recommandé sans OS/RAM/VRAM
  réels — ce serait **NON VÉRIFIÉ** (R-003, R-009).

## RESTE (dans l'ordre, une action à la fois)

1. Réponses ÉTAPE 0 → fiche matériel par `atlas-materiel` (budget mémoire chiffré).
2. Couche 1 — runtime + 1 modèle de départ (`atlas-runtime-llm`), commande exacte pour l'OS réel.
3. **Jeu d'or figé AVANT tout autre changement** (`atlas-mlops`) — sinon aucun progrès ne sera
   mesurable ensuite. Non négociable, c'est l'étape qu'on ne peut pas rattraper après coup.
4. Couche 2 — interface.
5. Couche 3 — mémoire persistante (fichiers Markdown structurés d'abord).
6. Couche 4 — RAG, procédure d'ingestion d'un document.
7. Couche 5 — outils/agent, avec garde-fous `sentinelle-exfiltration`.
8. Passe `sentinelle-derive` au 1er mois, puis palier fine-tuning si et seulement si les
   4 conditions sont réunies.

## DÉCISIONS PRISES

- **2026-09-16** — Création des 10 agents ATLAS, demandée par Chaima. Les 21 rôles du §1 sont
  inchangés. **TRANCHÉ PAR CHAIMA.**
- **2026-09-16** — Source de vérité = le dépôt ; le Drive est une copie consultable.

## DÉCISIONS EN ATTENTE DE CHAIMA

Voir `/codex/A-DECIDER.md`, ligne « Périmètre d'ATLAS ».

## NON VÉRIFIÉ à ce jour

Tout ce qui concerne la machine de Chaima : OS, RAM, VRAM, disque, niveau en ligne de commande,
budget, exigence de confidentialité, emplacement des données. **Aucune donnée matérielle n'a
été supposée.**
