# ATLAS — SNAPSHOTS

> Rituel d'entrée §5, **avant toute autre tâche**. État réel **vérifié**, jamais de mémoire.
> Le plus récent en haut. Rien n'a changé → **une seule ligne**, puis silence.
> Un snapshot dit *ce qui a changé*. Il ne dit pas *si c'est cohérent* — ça, c'est `audits/`.

---

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
