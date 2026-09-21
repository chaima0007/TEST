# ATLAS — JOURNAL D'APPRENTISSAGE

> Une entrée par tâche réelle. Format fixe : **Tâche · Ce qui a marché · Ce qui a raté ·
> Leçon retenue**. Rien de neuf → **une ligne**, pas un rapport (§5).
> Une leçon qui se répète monte en règle dans `REGLES-APPRISES.md`.
> Une leçon utile aux autres projets monte en fiche dans `/codex/expertise/` (transverse, §4).

---

## 2026-09-16 — Deux questions de droit posées au modèle nu

- **Tâche :** mesurer ce que vaut `qwen2.5:3b` sans corpus, sur le terrain réel de Chaima.
- **Ce qui a marché :** poser **exprès** une question piège (un montant d'amende précis).
  Le modèle a refusé d'inventer le chiffre — mais a inventé, dans la même réponse, une
  **institution entière**. Sans la question piège, on aurait conclu « il est prudent ».
- **Ce qui a raté :** rien côté méthode. Côté modèle : deux réponses sur deux sont fausses.
- **Leçon retenue :** *tester la prudence d'un modèle sur un seul type d'invention ne dit rien
  de sa prudence.* Il refuse d'inventer un **chiffre** (motif visiblement appris) et invente
  sans hésiter un **organisme**. Le jeu d'or doit couvrir plusieurs formes d'invention :
  chiffre, date, institution, article de loi, citation.
- **Leçon qui vaut pour moi aussi :** j'ai corrigé six erreurs de mémoire, sans source. Le
  réflexe correct n'est pas de me croire, c'est de marquer mes corrections NON VÉRIFIÉES et
  de les faire confirmer. Un agent qui corrige une hallucination par une affirmation non
  sourcée n'a rien corrigé.

## 2026-09-21 — Les notes locales entrent dans la mémoire (PLAUSIBLE jusqu'à capture)

- **Tâche :** Chaima demande « continuer les commandes pour qu'elle apprenne ». Couche 3 selon
  l'ordre du skill `atlas` : la mémoire doit grandir avec **ses** notes, pas seulement les
  fichiers du dépôt.
- **Choix :** un script `.bat` (`scripts/atlas-apprendre.bat`), parce que son shell réel est
  l'Invite de commandes (CONFIRMÉ). Il télécharge la tête du Modelfile, concatène les notes
  de `%USERPROFILE%\ATLAS\corpus`, clôt la chaîne SYSTEM et reconstruit `atlas-memoire`.
- **Pourquoi pas le RAG tout de suite :** l'installation d'AnythingLLM est humaine (§10) et la
  Zone 1 n'est pas faite. Le `.bat` donne la croissance dès maintenant, avec un seuil mesurable
  (30 000 octets) qui deviendra l'argument chiffré pour passer au RAG.
- **Sécurité :** les notes restent sur sa machine, jamais dans le dépôt public (R-015). Le
  script ne fait qu'un téléchargement sortant ; `sentinelle-exfiltration` n'a rien à redire.
- **Risques connus, à vérifier sur capture :** encodage des accents via `type` sous
  `chcp 65001` ; une note contenant trois guillemets droits casserait le Modelfile.
- **Verdict :** PLAUSIBLE. Passe à CONFIRMÉ à la première capture où l'IA cite une note locale.

## 2026-09-21 — Premier test réel de la mémoire locale (CONFIRMÉ)

- **Tâche :** Chaima charge `atlas-memoire` sur sa machine et pose la question de contrôle
  « où en est le projet ATLAS ? ».
- **Ce qui a marché :** le pont fichiers → Modelfile → Ollama fonctionne. L'IA locale a cité
  des faits qui ne peuvent venir que de nos fichiers : le débit mesuré, le RAG validé en attente
  de Zone 1, Peppol, le statut LLAM, le prompt maître v2 dans le Drive. Aucun chiffre inventé.
- **Ce qui a raté :** (1) le fait le plus récent, la routine en pause, n'a pas été cité alors
  qu'il était dans la mémoire ; (2) le sigle RAG a reçu un sens inventé. C'est la « réponse
  fluide et fausse » que `sentinelle-derive` décrit — observée pour de vrai, pas en théorie.
- **Ce qui a aussi raté, côté instructions :** la commande `ollama run` a été collée avec un
  mot en trop (`atlas-memoireollama`). Une commande sur une seule ligne, dans son propre bloc,
  réduit ce risque (R-011).
- **Leçon retenue :** R-016. Un modèle de 3 milliards de paramètres avec 8 192 tokens de
  contexte ne cherche pas un fait, il prend ce qui est saillant. La structure du fichier
  d'état est donc une décision de fiabilité, pas de mise en page : dernier événement en tête,
  lexique fermé pour les sigles.
- **Mesure « après » (2026-09-21, capture) : CONFIRMÉ.** Après rechargement, la réponse à la
  même question commence par « DERNIER ÉVÉNEMENT » et la routine en pause, avec le coût exact
  et la marche à suivre. Résidu cosmétique : le titre a été récité avec sa parenthèse de
  consigne → parenthèse retirée du titre, la consigne reste dans les règles SYSTEM.
  Test du lexique (RAG), capture du 2026-09-21 : **CONFIRMÉ** — « Retrieval-Augmented
  Generation », explication juste, aucun sens inventé. **R-016 prouvée sur ses deux volets.**
- **Incident de collage :** coller dans l'invite `>>>` a injecté `200~` (marqueur de collage
  de Windows Terminal, non compris par Ollama). Solution : taper au clavier. Ajouté à
  `MACHINE.md`.

## 2026-09-16 — Mise en place de la gouvernance ATLAS

- **Tâche :** créer les agents de domaine, les sentinelles et la boucle d'apprentissage d'une
  IA locale, avant tout diagnostic matériel.
- **Ce qui a marché :** appliquer la règle du découpage (`AGENTS.md`) au lieu d'attendre les
  réponses de l'ÉTAPE 0. Les agents, la gouvernance et les sentinelles ne dépendent pas du
  matériel ; seuls le choix de modèle et de runtime en dépendent. Une session entière aurait
  pu être perdue à attendre.
- **Ce qui a raté :** rien de constaté sur cette tâche.
- **Leçon retenue :** *« quelle partie de cette tâche dépend vraiment de l'information qui
  manque ? »* — presque toujours moins qu'il n'y paraît. C'est la formulation opérationnelle
  d'🔴 ERR-018 (escalade prématurée).

## 2026-09-16 — Constat de périmètre (fonde `sentinelle-perimetre`)

- **Tâche :** vérifier l'état réel du dépôt avant d'écrire (§5).
- **Ce qui a marché :** `git ls-remote` plutôt que la mémoire. Plus de 30 branches, dont une
  quinzaine de projets étrangers, **aucune mergée dans `main`** — donc chacune est l'unique
  copie de son travail.
- **Leçon retenue :** sur ce dépôt, `push --force`, suppression de branche et réécriture
  d'historique détruisent du travail sans sauvegarde. Montée en règle **R-002**.
