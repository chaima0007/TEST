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

## Débit — PREMIÈRE MESURE RÉELLE (2026-09-16)

**Relevé sur la machine de Chaima**, sortie `--verbose` d'Ollama, capture d'écran à l'appui.
Modèle `qwen2.5:3b` (1,9 Go téléchargés).

| Mesure | Valeur | Ce que ça veut dire |
|---|---|---|
| **`eval rate`** | **8,10 tokens/s** | **Vitesse d'écriture.** Environ 2× la vitesse de la parole humaine |
| `prompt eval rate` | 21,34 tokens/s | Vitesse de **lecture** de la question |
| `eval count` / `eval duration` | 154 tokens en 19,0 s | Un paragraphe ≈ **20 à 30 secondes** |
| `load duration` | 4,4 ms | Modèle déjà en mémoire — pas de rechargement |

### Le bridage thermique — PRÉDIT, puis MESURÉ le même jour

J'avais inscrit que la mesure à froid serait le **meilleur** cas et que la vraie serait plus
basse. Trois échanges consécutifs l'ont vérifié, sans rien faire d'autre que parler au modèle :

| Échange | `eval rate` | Écart vs le 1er |
|---|---|---|
| 1 — machine froide | **8,10 tokens/s** | référence |
| 2 | **7,75 tokens/s** | **−4 %** |
| 3 | **7,29 tokens/s** | **−10 %** |

**CONFIRMÉ (§13) : la machine se bride en charge.** Environ **−10 % en trois échanges**. La
courbe continuera de descendre puis se stabilisera ; le palier n'est pas encore connu.

**Retenir pour toujours :** un débit annoncé sur un premier échange est **structurellement
optimiste**. Toute mesure future de ce projet indique **le numéro de l'échange**, sinon elle
ne veut rien dire.

### Le second ralentisseur, moins visible et plus vicieux

`prompt eval count` a suivi : **42 → 232 → 620 tokens**. À chaque question, le modèle **relit
toute la conversation**. Deux effets cumulés :

- la machine chauffe → elle écrit plus lentement ;
- la conversation s'allonge → il y a plus à relire **avant** d'écrire.

D'où le `total duration` qui monte (21 s → 56 s → 55 s) plus vite que la seule chute du débit.
Conséquence pratique : **une conversation longue ralentit deux fois.** Repartir d'une session
neuve (`/bye` puis relancer) remet le compteur de lecture à zéro. Le cache aide (361 tokens
déjà en cache au 3e échange) mais ne supprime pas l'effet.

**Honnêteté sur mon estimation :** j'avais annoncé « utilisable, lecture fluide » pour un 3B,
en fiabilité MODÉRÉE. 8,10 tokens/s tombe dans cette fourchette. L'estimation était juste —
ça ne la transforme pas en méthode : c'est la mesure qui fait foi, et elle n'était pas connue
d'avance.

## Projection pour un modèle plus gros — NON VÉRIFIÉE

Sur processeur, la vitesse dépend surtout de la taille du modèle en mémoire. En proportion de
la mesure ci-dessus :

| Modèle | Poids | Projection | Fiabilité |
|---|---|---|---|
| 3 milliards (`qwen2.5:3b`) | 1,9 Go | **8,10 tokens/s — MESURÉ** | **VÉRIFIÉ (à froid)** |
| 7-8 milliards | ~4,5 Go | de l'ordre de 3 à 4 tokens/s | **MODÉRÉE** |

**3 à 4 tokens/s, c'est sous la vitesse de la parole.** Un paragraphe demanderait environ une
minute. Le compromis à trancher est donc réel : **qualité en français contre attente**. Il se
tranchera sur une mesure et sur le jeu d'or, pas sur une préférence.

## Ce que le RAG va coûter en vitesse — projection, NON VÉRIFIÉE (2026-09-19)

Le modèle **relit** les extraits retrouvés avant d'écrire. `prompt eval` mesuré : **21-25
tokens/s**. Quatre extraits ≈ 1 500 à 3 000 tokens → **70 à 140 secondes de lecture** avant
le premier mot, hors bridage thermique. **Une question RAG coûtera 2 à 3 minutes.** Fiabilité
**MODÉRÉE** (calcul du scout, pas mesure). Leviers si c'est trop : moins d'extraits, extraits
plus courts. **Mesurer sur la première vraie question, et inscrire ici.**

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
