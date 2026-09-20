# ATLAS — Remontée vers le Drive

> Demande de Chaima (2026-09-16) : *« toutes tes erreurs doivent être communiquées dans le
> Drive, et les réussites dans le fichier concerné. »*

## Le sens de circulation — il n'y en a qu'un

    DÉPÔT (source de vérité)  ──remontée──▶  DRIVE (copie consultable)

**Jamais l'inverse.** Un document Drive corrigé à la main et divergeant du dépôt est pire
qu'un document absent : il fait croire à une correction qui n'existe pas dans le système. En
cas de divergence, **le dépôt a raison**.

## Où va quoi

| Événement | Fichier du dépôt (original) | Drive |
|---|---|---|
| **Erreur réelle** | `🔴 ERREURS.md` (racine) | **oui, dès l'incident** |
| Leçon d'une tâche | `codex/atlas/JOURNAL-APPRENTISSAGE.md` | à la remontée suivante |
| Correction de Chaima → règle | `codex/atlas/REGLES-APPRISES.md` | **oui, dès l'écriture** |
| **Réussite = jalon réel vérifié** | `codex/EVOLUTION.md` (append-only, §6.5) + `codex/atlas/ETAT-DU-PROJET.md` | oui |
| Snapshot de session | `📋 JOURNAL.md` | non (bruit) |
| Décision en attente | `codex/A-DECIDER.md` | non (Chaima le lit dans le dépôt) |

**« Réussite » a un sens strict** : une couche qui fonctionne et dont le fonctionnement est
**vérifié**. Pas « j'ai écrit des fichiers ». La distinction JOURNAL / EVOLUTION du §6.5 est
exactement celle-là, et la confondre est ce qui noie un Empire sous le bruit.

## Dossier Drive d'ATLAS — rangé, pour ne pas se mélanger aux autres projets

**`ATLAS — IA locale (Empire Chaima)`** — `1Ual-L_FKyitVvi71bQph51-gpOQeq4Ao`

| Document | ID | Sens |
|---|---|---|
| `01 — FICHE MACHINE — À REMPLIR` | `1GRzD4Oow7O8wWjg-Dv3iirUbmlYpKyilyek0YsVOl20` | **Chaima écrit, ATLAS lit** — la seule exception |
| `02 — ERREURS ET RÉUSSITES — ATLAS (à jour au 2026-09-19)` | `19sqt-VCsfAifo1YIK0axYlu-wtZtfNzVL0lVgzz1C7g` | ATLAS écrit, Chaima lit — **version courante** |
| `02 — … (version du 16/09 — REMPLACÉE, conservée)` | `1cKad7xISrny7R5KGr1hseX0HlOUWATHQ3QfvhlCDZkU` | périmée, gardée (un doc = un événement) |
| `03 — PROMPT MAÎTRE v2 (amendé après test à froid)` | `1wmi71buYd5L143BNl5jNd9Wmz3S-Pg2y5Nu-g5Mdla4` | **version courante**, relue après écriture |
| `03 — … (version 13h29 — REMPLACÉE, conservée)` | `1dvZzc_DyMApBYOipJiug1WC6zYPiappmO1Z0PjMko4M` | périmée, gardée |

Les documents des autres projets restent où ils sont : on ne déplace que les nôtres
(`sentinelle-perimetre`).

**L'outil Drive ne modifie pas le contenu d'un document existant** (titre et dossier seulement).
Mettre à jour = renommer l'ancien « REMPLACÉ le <date>, conservé » + créer le nouveau. Ça respecte
la convention de Chaima (un doc = un événement, jamais d'écrasement) tout en gardant **un seul
document courant** par type. Ne jamais supprimer (§10).

**Vérifier après chaque écriture Drive.** Une création peut renvoyer un succès et un document
vide — constaté le 2026-09-16. On relit systématiquement le contenu écrit.

## Règles

1. **Anti-bruit (§5).** Rien de neuf → **aucune remontée**. Un document Drive de plus pour dire
   qu'il n'y a rien à dire est une faute.
2. **Jamais de donnée personnelle ni de secret** dans une remontée (§10, 🔴 ERR-015 : sept
   agents ont recommandé d'écrire des données personnelles dans un fichier sans savoir que le
   dépôt était **public**). Le Drive est privé, le dépôt ne l'est pas — vérifier **avant**.
3. **Ajouter, ne pas réécrire.** Les autres projets ont leurs propres documents dans ce
   dossier : on n'y touche pas (`sentinelle-perimetre`).
4. **Envoyer quoi que ce soit à un TIERS reste §10.** Le Drive de Chaima n'est pas un tiers ;
   un partage vers l'extérieur, si.
