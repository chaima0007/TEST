# 🔴 ATLAS — ERREURS

> Une erreur **réellement survenue** = une entrée datée. Le plus récent en haut.
> Format fixe : **Ce qui s'est passé · Cause (confirmée par reproduction) · Comment la détecter
> la prochaine fois · Correctif (VÉRIFIÉ)**.
>
> **Toute entrée ici est remontée dans le Drive** (`../continuite/SYNC-DRIVE.md`).
> **Si Chaima doit corriger deux fois la même chose, c'est une entrée ici** — la boucle
> d'apprentissage est cassée, et c'est un incident en soi (`sentinelle-derive`, dérive n°1).
>
> Vérité totale : seules des erreurs réelles figurent ici, avec leur preuve. Pas d'erreur
> anticipée, pas d'erreur « probable ». Les risques prévus vivent dans les chartes d'agents.

---

## ERR-ATLAS-002 — Le bloc de commande invitait à être recollé (2026-09-16)

- **Ce qui s'est passé :** après le téléchargement du modèle, Chaima a collé
  `ollama run qwen2.5:3b --verbose` **dans l'invite `>>>` du modèle**, au lieu d'y écrire une
  question. Le modèle a traité la commande comme une question et a répondu à côté.
- **Cause :** l'instruction disait bien « quand tu vois `>>>`, écris-lui une vraie question ».
  Mais **le dernier élément copiable de mon message était la commande elle-même**. Face à une
  invite qui attend quelque chose, on recolle ce qu'on a sous la main. L'instruction était
  juste ; **sa mise en page disait le contraire.**
- **Détection :** le modèle répond *à propos de la commande* au lieu d'y obéir. Autrement dit,
  l'invite `>>>` n'est plus PowerShell : **elle ne prend plus de commandes, seulement du
  texte adressé au modèle.**
- **Correctif :** dire explicitement, à chaque commande qui ouvre une session interactive :
  **« cette commande est finie, ne la recolle pas — désormais tu parles au modèle. »** Et ne
  jamais laisser un bloc de commande comme dernier élément copiable avant une invite.
- **Conséquence heureuse :** l'erreur a produit le relevé le plus instructif du projet — le
  modèle a inventé un nom de modèle inexistant avec une assurance totale
  (`../mesure/JEU-D-OR.md`). Ça ne rachète pas le défaut d'instruction, mais ça se consigne.

## ERR-ATLAS-001 — L'instruction a envoyé Chaima dans la mauvaise fenêtre (2026-09-16)

- **Ce qui s'est passé :** instruction donnée — « touche Windows, taper `powershell`, Entrée ».
  Chaima s'est retrouvée dans **Invite de commandes** (`cmd.exe`), pas dans PowerShell.
  Le bloc de commandes fourni ne pouvait donc pas fonctionner.
- **Cause (CONFIRMÉE par la capture d'écran) :** l'instruction supposait que taper `powershell`
  dans la recherche Windows **ouvre** PowerShell. Selon ce qui est épinglé et ce que la
  recherche propose en premier, c'est `cmd.exe` qui s'ouvre. **L'instruction ne contenait
  aucun moyen pour Chaima de savoir dans quelle fenêtre elle était** — c'est ça, le vrai
  défaut : pas le mauvais programme, l'absence de repère pour le constater.
- **Aggravant, entièrement imputable à l'agent :** R-005 exigeait « la commande · la
  vérification · quoi faire si ça rate ». La partie « si ça rate » listait trois cas, **aucun
  n'était le bon**. Une liste d'échecs qui ne contient pas l'échec réel donne une fausse
  impression de filet de sécurité.
- **Détection la prochaine fois :** le texte avant le curseur. `C:\Users\Chaima>` = Invite de
  commandes. `PS C:\Users\Chaima>` = PowerShell. Le `PS` est le seul repère qui compte, et il
  doit être **dit à l'avance**, pas après la panne.
- **Correctif (VÉRIFIÉ sur la capture) :** ne plus demander d'**ouvrir** PowerShell, mais de
  taper `powershell` **dans la fenêtre déjà ouverte** — ça bascule dans la même fenêtre, rien
  à fermer, et le `PS` qui apparaît est la preuve visible que ça a marché. L'instruction porte
  désormais son propre test.
- **Gain collatéral :** la capture a livré `Microsoft Windows [version 10.0.26200.9457]` — l'OS
  est **VÉRIFIÉ** par l'échec lui-même. Une commande qui rate en disant qui elle est reste une
  commande utile.
