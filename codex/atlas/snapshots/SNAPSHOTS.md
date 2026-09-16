# ATLAS — SNAPSHOTS

> Rituel d'entrée §5, **avant toute autre tâche**. État réel **vérifié**, jamais de mémoire.
> Le plus récent en haut. Rien n'a changé → **une seule ligne**, puis silence.
> Un snapshot dit *ce qui a changé*. Il ne dit pas *si c'est cohérent* — ça, c'est `audits/`.

---

## SNAPSHOT 2026-09-16 (2) — OS VÉRIFIÉ + première erreur ATLAS consignée

- **OS confirmé : Windows 11, build `10.0.26200.9457`, session `C:\Users\Chaima`.** Preuve :
  capture d'écran de l'invite de commandes. Passe de PLAUSIBLE à **VÉRIFIÉ** — et la preuve
  vient de l'échec de la commande, pas de son succès.
- **ERR-ATLAS-001 ouverte** : mon instruction a envoyé Chaima dans `cmd.exe` au lieu de
  PowerShell, et ma section « si ça rate » ne contenait pas l'échec réel. Faute d'agent, pas
  d'utilisatrice. Règle **R-010** posée : toute instruction doit porter le repère qui dit où
  on est (`PS` avant le curseur), et la liste des échecs doit contenir l'échec réel.
- **La boucle d'apprentissage a tourné pour de vrai** : une erreur réelle → une entrée datée →
  une règle qui l'empêche de se reproduire, dans le même tour. C'est le premier tour complet.
- **Toujours NON VÉRIFIÉ** : RAM, carte graphique, VRAM, disque libre. Rien n'est installé.

## SNAPSHOT 2026-09-16 — Rangement en sous-dossiers + profil de Chaima ouvert

État réel vérifié par `git ls-remote` : branche `claude/nifty-shannon-u87dv8` à `0e9240f`,
`main` inchangé.

- **Structure en sous-dossiers créée** à la demande de Chaima, avec `ROUTAGE.md` : un type
  d'information = un sous-dossier = **un seul fichier vivant**, où l'on ajoute en tête. Jamais
  un fichier daté par événement — c'est ça qui fait s'entremêler les documents.
- **Trois informations recueillies sur Chaima** et consignées dans `memoire/PROFIL-CHAIMA.md` :
  elle ne code pas encore bien (⇒ tout doit être copiable-collable, une action à la fois) ;
  elle veut un système « inarrêtable » ; elle veut du rangement strict.
- **Recherche dans le Drive : les caractéristiques machine n'y sont PAS.** Un seul document
  mentionne de la RAM — le guide d'examen MQ06 (Windows Server 2022, VM 16 Go) — c'est un
  **exercice d'école, pas la machine de Chaima**. S'en servir aurait violé R-003. L'ÉTAPE 0
  reste donc ouverte : **NON VÉRIFIÉ**.
- **Drive rangé** : dossier dédié `ATLAS — IA locale (Empire Chaima)` créé, contenant
  `01 — FICHE MACHINE — À REMPLIR` (vide, en attente de Chaima) et `02 — ERREURS ET
  RÉUSSITES — ATLAS`. Les deux contenus **relus après écriture** — une création Drive peut
  renvoyer un succès et un document vide, constaté aujourd'hui.
- **Écart connu, non corrigé** : le document Drive `02` cite les anciens chemins
  (`codex/atlas/JOURNAL-APPRENTISSAGE.md`…) d'avant le rangement en sous-dossiers. L'outil
  disponible ne modifie que le titre et l'emplacement d'un document, pas son contenu. Sans
  conséquence — le document dit lui-même que **le dépôt a raison** — et corrigé à la première
  remontée réelle. Signalé plutôt que tu, conformément au §5.
- **OS : « je pense windows » (Chaima, 2026-09-16).** Consigné **PLAUSIBLE, fiabilité
  MODÉRÉE** — pas VÉRIFIÉ. Une commande PowerShell lui a été donnée, choisie pour être **sa
  propre preuve** : si elle s'exécute, c'est Windows ; si elle échoue, ce n'en est pas. Aucune
  installation ne partira d'une impression.
- **Rien installé, rien acheté, rien engagé.**
