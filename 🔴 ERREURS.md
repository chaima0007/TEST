# 🔴 ERREURS — ce qui a réellement cassé, et ce qu'on en a appris (dépôt partagé)

## 2026-08-10 — Une fiche juridique dépassée par une réforme entrée en vigueur
`premier_emploi` affirmait « depuis 2014, la période d'essai a été supprimée » sans mentionner la
réforme du 01/08/2026. Exact la veille, trompeur le lendemain.
**Correction :** fiche mise à jour, avec le bon critère (date de début d'exécution du contrat).
**Leçon :** une fiche juridique n'est jamais « finie » ; sans date de vérification affichée et
re-contrôle périodique, un corpus se périme en silence — c'est le risque n°1 d'un produit qui vend
de la conformité.

## 2026-07-13 — Des liens vers des fiches qui ne résolvaient pas
Le routage `/loi/[domaine]` matche le champ `module` du JSON, pas le nom du fichier ; 11 fiches ont
un nom différent de leur module. Les liens écrits de mémoire cassaient en silence.
**Correction :** garde `liens_fiches_guard.py`, qui bloque désormais tout lien mort avant commit.
**Leçon :** ce qui casse en silence doit être transformé en contrôle automatique, pas en vigilance.

## Récurrent — Conteneur recyclé, clone local revenu en arrière
Le clone local retombe parfois sur un état ancien et divergent ; les fichiers semblent avoir disparu.
**Correction :** vérifier l'état réel par `git ls-remote` avant toute conclusion, puis réaligner sur
origin. Le travail poussé n'a jamais été perdu.
**Leçon :** §5.1 — état réel vérifié, jamais de mémoire. Cette règle vient d'un fait, pas d'un principe.
