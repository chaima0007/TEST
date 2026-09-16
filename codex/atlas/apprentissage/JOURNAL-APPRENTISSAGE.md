# ATLAS — JOURNAL D'APPRENTISSAGE

> Une entrée par tâche réelle. Format fixe : **Tâche · Ce qui a marché · Ce qui a raté ·
> Leçon retenue**. Rien de neuf → **une ligne**, pas un rapport (§5).
> Une leçon qui se répète monte en règle dans `REGLES-APPRISES.md`.
> Une leçon utile aux autres projets monte en fiche dans `/codex/expertise/` (transverse, §4).

---

## 2026-09-16 — Mise en place de la gouvernance ATLAS

- **Tâche :** créer les agents de domaine, les sentinelles et la boucle d'apprentissage d'une
  IA locale, avant tout diagnostic matériel.
- **Ce qui a marché :** appliquer la règle du découpage (`AGENTS.md`) au lieu d'attendre les
  réponses de l'ÉTAPE 0. Les agents, la gouvernance et les sentinelles ne dépendent pas du
  matériel ; seuls le choix de modèle et de runtime en dépendent. Une session entière aurait
  pu être perdue à attendre.
- **Ce qui a raté :** rien de constaté sur cette tâche.
- **Leçon retenue :** *« quelle partie de cette tâche dépend vraiment de l'information qui
  manque ? »* — presque toujours moins qu'il n'y paraît. C'est la formulation opérationnelle
  d'🔴 ERR-018 (escalade prématurée).

## 2026-09-16 — Constat de périmètre (fonde `sentinelle-perimetre`)

- **Tâche :** vérifier l'état réel du dépôt avant d'écrire (§5).
- **Ce qui a marché :** `git ls-remote` plutôt que la mémoire. Plus de 30 branches, dont une
  quinzaine de projets étrangers, **aucune mergée dans `main`** — donc chacune est l'unique
  copie de son travail.
- **Leçon retenue :** sur ce dépôt, `push --force`, suppression de branche et réécriture
  d'historique détruisent du travail sans sauvegarde. Montée en règle **R-002**.
