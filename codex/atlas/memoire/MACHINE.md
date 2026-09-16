# ATLAS — LA MACHINE DE CHAIMA

> **VÉRIFIÉ le 2026-09-16** par sortie PowerShell (capture d'écran), pas par déclaration.
> Toute recommandation d'ATLAS part de ce fichier. S'en écarter exige de dire pourquoi.

## Les chiffres réels

| Poste | Valeur | Ce que ça change |
|---|---|---|
| **OS** | Microsoft **Windows 11 Pro** (build `10.0.26200.9457`) | Toutes les commandes sont Windows/PowerShell |
| **RAM** | **15,9 Go** (≈ 16 Go) | **C'est LA ressource utile.** Tout tournera là-dedans |
| **Processeur** | **Intel Core i7-8650U @ 1,90 GHz** | 4 cœurs / 8 threads, puce **mobile basse consommation** |
| **Carte graphique** | **Intel UHD Graphics 620** (intégrée) | **Aucune accélération exploitable.** Pas de CUDA, pas de VRAM dédiée |
| **Disque C libre** | **120,2 Go** | Largement suffisant — un modèle pèse 2 à 5 Go |
| **NVIDIA** | **aucune** | Confirmé par la carte : UHD 620 est intégrée au processeur |

**PLAUSIBLE, fiabilité ÉLEVÉE, non sourcé ici :** le i7-8650U est une puce **Kaby Lake
Refresh de 2017, enveloppe thermique ~15 W**, conçue pour des ordinateurs portables fins.
Vérifiable sur la fiche Intel officielle. Conséquence si confirmé : machine d'environ **9 ans**
et **qui chauffe vite** — deux faits qui pèsent sur les décisions ci-dessous.

## Le verdict, sans adoucissement

**Il n'y a pas de carte graphique utilisable pour de l'IA. Tout tournera sur le processeur.**

Ce n'est pas un détail : c'est **la** contrainte structurante. Un processeur mobile 15 W de 2017
fait de l'inférence, mais lentement, et il **throttle** (se bride pour ne pas surchauffer) au
bout de quelques minutes de charge. Le débit mesuré à froid sur les premiers mots ne sera
**pas** le débit réel d'une conversation longue.

**Ce qui est possible :** un modèle de 3 à 8 milliards de paramètres, quantifié. Du conseil
texte, de la lecture de documents, de la rédaction. Le cœur du besoin de Chaima.

**Ce qui n'est PAS possible sur cette machine, et il faut le savoir maintenant :**

| Envie | Verdict | Pourquoi |
|---|---|---|
| Un « gros » modèle (30B, 70B) | **NON** | Ne rentre pas, ou à une lenteur inutilisable |
| Génération d'images | **NON** en pratique | Demande une carte graphique |
| **Fine-tuning LoRA/QLoRA** | **NON** | Demande une carte graphique. `atlas-finetuning` le refusait déjà par défaut ; il y a désormais un **motif matériel définitif**, pas seulement méthodologique. Ce palier est **fermé** tant que la machine ne change pas. |
| Réponses instantanées | **NON** | Ce sera de l'ordre de la lecture à voix haute, pas du texte qui jaillit |

## Ce que cette contrainte valide

**Elle rend la stratégie d'ATLAS obligatoire au lieu d'optionnelle.** Puisque le modèle ne peut
pas être gros, toute la valeur doit venir du **corpus et de la mémoire**. C'est exactement ce
que Chaima a demandé — « une base de données qui grandit avec le temps ». Sa contrainte
matérielle et son objectif pointent dans la même direction : **un petit modèle bien alimenté
bat un gros modèle qui répond de mémoire.**

Le fine-tuning étant matériellement fermé, il n'y a plus d'ambiguïté sur où investir l'effort.

## Estimations de débit — NON VÉRIFIÉES, à mesurer (R-003)

Ordres de grandeur **raisonnés** à partir de la bande passante mémoire, **jamais mesurés sur
cette machine**. Ils servent à choisir quoi tester en premier, **pas** à promettre un résultat.

| Taille de modèle (quantifié Q4) | Poids en mémoire | Attente raisonnée | Fiabilité |
|---|---|---|---|
| 3 milliards de paramètres | ~2 Go | utilisable, lecture fluide | **MODÉRÉE** |
| 7-8 milliards | ~4,5 Go | lent mais praticable | **MODÉRÉE** |
| 13 milliards et + | ~8 Go et + | trop lent pour un usage réel | **MODÉRÉE** |

**Le chiffre qui comptera est celui mesuré sur la machine de Chaima, après 10 minutes de
charge.** Tout ce tableau est à remplacer par des mesures dès la couche 1 installée.

## Conséquences pratiques, non négociables

1. **Brancher l'ordinateur sur secteur.** Sur batterie, Windows bride le processeur : le
   même modèle paraîtra deux fois plus lent, et on conclura à tort que le modèle est mauvais.
2. **Mesurer après 10 minutes, pas au premier mot.** Sinon on mesure l'ordinateur froid.
3. **Machine d'environ 9 ans** (si la date 2017 se confirme) : la probabilité de panne
   matérielle n'est pas négligeable. C'est un argument de plus pour la règle des 3 copies
   (`../continuite/RESTAURATION.md`) — et pas un argument pour acheter quoi que ce soit, ce
   qui reste §10.

---

## Ce qui est installé sur cette machine

| Logiciel | Version | Installé le | Statut | Comment le vérifier |
|---|---|---|---|---|
| **Ollama** | non relevée | 2026-09-16 | **VÉRIFIÉ** — application ouverte, capture d'écran | `ollama --version` dans PowerShell |

**Modèles téléchargés :** aucun à ce jour. Les lister : `ollama list`.

**Point de vigilance permanent (`sentinelle-exfiltration`) :** l'application Ollama propose de
connecter des **outils tiers**, dont plusieurs sont des services **cloud**. Ollama installé
localement ne rend pas local ce qui s'y branche, et un compte connecté peut ouvrir l'accès à
des modèles distants. **« Local » ne se déclare pas, il se vérifie** : tant qu'aucune
observation du trafic sortant n'a été faite, la souveraineté des données est **NON VÉRIFIÉE**.
