---
name: atlas
description: Orchestre le projet ATLAS — IA locale, privée, qui accumule mémoire et corpus. Aiguille vers les 7 experts de domaine et les 3 sentinelles, impose l'ordre matériel → runtime → jeu d'or → mémoire → RAG → outils, et refuse toute recommandation de modèle sans diagnostic matériel réel.
---

# Skill : ATLAS (IA locale)

**À lire avant toute tâche ATLAS, dans cet ordre :**
`codex/atlas/apprentissage/REGLES-APPRISES.md` (ne pas refaire une erreur déjà corrigée) →
`codex/atlas/00-ETAT-DU-PROJET.md` (où on en est) →
`codex/atlas/memoire/PROFIL-CHAIMA.md` (à qui je parle, et ce qui est encore NON VÉRIFIÉ).

**Avant d'écrire le moindre fichier :** `codex/atlas/ROUTAGE.md`. Un type d'information = un
sous-dossier = **un seul fichier vivant**, ajout en tête. Créer un fichier daté par événement
est une faute (R-007) — c'est ce qui entremêle les documents.

## Verrou n°1 — le diagnostic passe avant tout

**Aucune recommandation de modèle, de runtime ou de quantification sans OS, RAM, VRAM et
disque réels.** Une recommandation faite sans ces chiffres est **NON VÉRIFIÉE** (§13) et se
retire, elle ne se nuance pas. Tant que l'ÉTAPE 0 est sans réponse : on construit la
gouvernance, on ne choisit pas de modèle.

## Verrou n°2 — le jeu d'or se fige avant le premier changement

C'est la seule étape de la boucle **impossible à rattraper après coup**. Sans mesure d'avant,
« ça s'est amélioré » est une impression, pas un constat.

## Ordre des couches — aucune étape sautée

    atlas-materiel  →  atlas-runtime-llm  →  [JEU D'OR figé]  →  interface
         ↓                                                          ↓
    budget mémoire chiffré                             atlas-rag-memoire (mémoire, puis RAG)
                                                                    ↓
                                                        outils/agent + sentinelle-exfiltration

## Aiguillage

| Le sujet touche… | Convoquer |
|---|---|
| RAM, VRAM, disque, watts, thermique, « est-ce que ça tient ? » | `atlas-materiel` |
| Ollama / llama.cpp / LM Studio, GGUF, quantification, contexte | `atlas-runtime-llm` |
| Mémoire entre sessions, corpus, découpage, embeddings, citations | `atlas-rag-memoire` |
| LoRA / QLoRA, jeu de données d'entraînement | `atlas-finetuning` (refuse par défaut) |
| Une commande sur la machine, un service, un port, une panne | `atlas-systemes-reseaux` |
| « est-ce que ça s'améliore vraiment ? », jeu d'or, versionnage | `atlas-mlops` |
| Une question dont la réponse n'est pas dans `/codex/expertise/` | `atlas-chercheur-sources` |
| Une donnée qui pourrait **sortir** de la machine | `sentinelle-exfiltration` |
| Un `git`, un fichier partagé, une ressource commune | `sentinelle-perimetre` |
| Le système grossit — se dégrade-t-il ? | `sentinelle-derive` |
| Données **personnelles**, RGPD | `gardien-donnees` (rôle §1 existant) |
| Un composant externe qu'on veut installer | Parcours 1 : `scout` → `guardian-licences` + `sentinel-securite` |
| Une décision **engageante** | skill `debat` (Parcours 2) — avocat et contradicteur ensemble |

## Format de sortie vers Chaima — les trois temps, à chaque étape

**(a)** ce qu'on vient de faire · **(b)** la commande exacte qui **vérifie** que c'est bon ·
**(c)** **la** prochaine action, une seule.

Puis le bloc de passation §14. Et la règle anti-bruit (§5) : rien n'a changé → une ligne.

## Ne jamais

Installer, supprimer, acheter, ouvrir un port, autoriser une sortie de données, lancer un
entraînement, merger dans `main` — **tout cela est §10, c'est Chaima.**
Promettre qu'un modèle local « vaut » un modèle cloud : affirmation *sur nous*, la plus
dangereuse (§13).
Sauter le contradicteur parce que la décision paraît évidente : **permanent, non
désactivable** (§1).
