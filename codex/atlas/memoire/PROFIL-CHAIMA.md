# ATLAS — PROFIL DE CHAIMA

> **La base qui grandit avec le temps, volet « qui je sers ».**
> Chaque ligne : le fait, la date, et **comment je l'ai su**. Une ligne sans origine est une
> supposition déguisée en connaissance — exactement ce que §13 interdit.
> Une information ne se supprime pas : elle se marque **périmée**, datée, avec le motif.

## Ce qui est VÉRIFIÉ (dit par Chaima elle-même)

| Fait | Conséquence opérationnelle | Dit le | Statut |
|---|---|---|---|
| **Ne code pas encore bien** | Tout est **copiable-collable**, **une action à la fois**, et rien ne suppose qu'elle sache réparer. Chaque étape sort en trois temps : la commande · la vérification · quoi faire si ça rate. Aucun raccourci « tu n'as qu'à… ». | 2026-09-16 | **ACTIF** |
| **Veut un système « inarrêtable »** | Requalifié avec elle : une machine s'arrête toujours ; ce qui doit être inarrêtable, c'est la **connaissance**. Voir `../continuite/RESTAURATION.md`. | 2026-09-16 | **ACTIF** |
| **Veut une base qui grandit avec le temps** | Mémoire + corpus, pas les poids du modèle. `memoire/` et `corpus/`. | 2026-09-16 | **ACTIF** |
| **Veut du rangement strict, pas de documents entremêlés** | `../ROUTAGE.md` : un type = un sous-dossier = un seul fichier vivant, ajout en tête. | 2026-09-16 | **ACTIF** |
| **Exige qu'on ne la flatte pas** | Dire la vérité même quand elle dérange ; se contredire quand c'est justifié. | 2026-09-16 | **ACTIF** |
| **Objectif final : être autonome**, pilote de son système | Chaque étape la rend capable de la refaire seule. Pas de dépendance à moi. | 2026-09-16 | **ACTIF** |
| **OS : Windows 11**, build `10.0.26200.9457` | Toutes les commandes sont Windows. **VÉRIFIÉ** par capture d'écran de l'invite de commandes, pas par déclaration. | 2026-09-16 | **ACTIF** |
| **Session utilisateur : `C:\Users\Chaima`** | C'est là que vivront le modèle, la mémoire et le corpus. | 2026-09-16 | **ACTIF** |
| **Matériel complet relevé** | 16 Go de RAM · i7-8650U · **aucune carte graphique utilisable** · 120 Go libres. Détail et conséquences : `MACHINE.md`. **Le fine-tuning est matériellement fermé.** | 2026-09-16 | **ACTIF** |
| **Ouvre l'Invite de commandes, pas PowerShell** | Ne jamais dire « ouvre PowerShell » : dire « tape `powershell` dans la fenêtre déjà ouverte », et donner le repère `PS` avant le curseur (ERR-ATLAS-001). | 2026-09-16 | **ACTIF** |

## Ce qui est PLAUSIBLE — raisonné, pas confirmé (§13)

| Fait | Fiabilité | Origine | Comment ça devient VÉRIFIÉ |
|---|---|---|---|
| **Version exacte : Windows 11 25H2** | **MODÉRÉE** | La build `26200` appartient à la série Windows 11 ; le nom commercial de cette build n'a pas été vérifié sur une source primaire datée. | Sortie de `winver` ou de `Get-CimInstance Win32_OperatingSystem`. **Sans effet sur nos choix** : ce qui compte est la RAM et la carte graphique, pas le nom commercial. |

## Ce qui est NON VÉRIFIÉ — et le restera tant qu'elle ne l'aura pas dit

- **Son usage n°1**, le cas concret qui doit marcher en premier.
- **Budget** : temps par semaine, argent.
- **Exigence de confidentialité** : 100 % local, ou cloud toléré pour certaines tâches.
- **Où vivent ses données** sur la machine.

**Note sur le signal Drive, conservée exprès :** le `Guide_Examen_MQ06` laissait deviner
Windows, et **il se trouve que c'était juste**. Ça ne valide pas la déduction pour autant — la
preuve est venue de la capture d'écran, pas du document d'école. Une intuition confirmée par
hasard reste une intuition : c'est précisément quand elle tombe juste qu'on est tenté d'en
faire une méthode (R-009 maintenue).

## Ce qui a été cherché, et n'existe pas

- **2026-09-16** — Recherche dans le Drive de caractéristiques machine (RAM, VRAM, processeur,
  config) : **rien**. Cherché, pas supposé — la distinction compte.
