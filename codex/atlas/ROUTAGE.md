# ATLAS — OÙ VA QUOI

> **Le fichier anti-mélange.** Demande de Chaima (2026-09-16) : *« des snapshots, des audits et
> des fichiers d'erreur commis dans le fichier concerné et existant, comme sous-dossier, pour
> éviter que les documents s'entremêlent. »*

## La règle qui empêche le mélange

**Un type d'information = un sous-dossier = UN SEUL fichier vivant, où l'on AJOUTE en tête.**

Jamais un nouveau fichier daté par événement. C'est précisément ce qui noie un Empire :
`audit-2026-09-16.md`, `audit-2026-09-16-v2.md`, `audit-final.md`… et plus personne ne sait
lequel fait foi. Ici, il n'y a **qu'un** fichier d'audits, **qu'un** fichier de snapshots,
**qu'un** fichier d'erreurs. Ils grossissent par le haut. Le plus récent est toujours la
première chose qu'on lit.

## La table — aucune exception

| Ce que je viens de produire | Où ça va, exactement |
|---|---|
| Un **snapshot** de session (§5) | `snapshots/SNAPSHOTS.md` — en tête |
| Un **audit** (cohérence, angle mort, trimestriel §9) | `audits/AUDITS.md` — en tête |
| Une **erreur réelle** survenue sur ATLAS | `erreurs/ERREURS-ATLAS.md` — en tête, **puis Drive** |
| Une leçon d'une tâche (ce qui a marché / raté) | `apprentissage/JOURNAL-APPRENTISSAGE.md` |
| Une **correction de Chaima** devenue règle | `apprentissage/REGLES-APPRISES.md` — **dans le même tour** |
| Ce que j'apprends **sur Chaima** (préférences, contraintes) | `memoire/PROFIL-CHAIMA.md` |
| Un fait **matériel mesuré** sur sa machine | `memoire/MACHINE.md` |
| Une **décision tranchée par Chaima** sur ATLAS | `memoire/DECISIONS.md` |
| Un **document de Chaima** à faire lire à l'IA | `corpus/` (le RAG) |
| Une mesure de progrès, le jeu d'or | `mesure/JEU-D-OR.md` |
| Une procédure de sauvegarde / restauration | `continuite/RESTAURATION.md` |
| La remontée vers le Drive | `continuite/SYNC-DRIVE.md` |
| Où en est le projet (fait / en cours / reste) | `00-ETAT-DU-PROJET.md` — **le seul fichier à ouvrir pour reprendre** |
| Une décision qui **attend Chaima** | `/codex/A-DECIDER.md` (racine, partagé avec les autres projets) |
| Une leçon **utile aux autres projets** | `/codex/expertise/` (transverse, §4) |
| Un **jalon réel vérifié** | `/codex/EVOLUTION.md` (append-only, §6.5) |

## Trois pièges nommés, pour ne pas les retomber

1. **Snapshot ≠ audit.** Le snapshot dit *ce qui a changé* depuis la dernière fois. L'audit dit
   *si c'est cohérent*. Confondre les deux produit deux documents qui se répètent — et qu'on
   finit par ne plus lire ni l'un ni l'autre.
2. **Journal ≠ EVOLUTION** (§6.5). Le journal accepte « rien de neuf ». EVOLUTION **jamais** :
   il ne reçoit que des jalons réels. C'est exactement la distinction qui empêche l'Empire de
   se noyer sous le bruit.
3. **Règle anti-bruit (§5), qui prime sur tout ce tableau.** Rien n'a changé → **une ligne**,
   puis silence. Un audit écrit pour dire qu'il n'y a rien à auditer est une faute contre le
   protocole, pas une preuve de sérieux.
