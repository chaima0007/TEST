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

## Document Drive d'ATLAS

- **Titre :** `🔴 ERREURS & RÉUSSITES — ATLAS (IA locale) — ouvert le 2026-09-16`
- **Dossier :** `1qXUj9D9r7HSmIMzMcsScz4Ynlv4auP4G` — le même que
  `🔴 BASE DES ERREURS — Nexus-Market`, pour que tout se lise au même endroit.
- **ID du document :** voir `codex/atlas/ETAT-DU-PROJET.md`, section FAIT.

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
