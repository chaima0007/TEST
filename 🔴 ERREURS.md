# 🔴 BASE DES ERREURS — TEST / Nexus-Market

> Chaque erreur réelle rencontrée, documentée pour **ne jamais la reproduire**. Consultable
> par tous les agents. Format fixe par entrée : **Ce qui s'est passé · Cause · Comment la
> détecter la prochaine fois · Correctif (VÉRIFIÉ)**. Un incident = une entrée datée.
>
> Vérité totale : seules des erreurs réellement survenues figurent ici, avec leur preuve.

## Convention de numérotation — TRANCHÉ PAR CHAIMA le 2026-09-19

**Toute nouvelle entrée est titrée par horodatage : `ERR-AAAAMMJJ-HHMM`** (heure UTC de
l'écriture). Exemple : `## ERR-20260919-1340 — …`.

**Les entrées existantes `ERR-001` à `ERR-021` ne sont PAS renommées.** Leurs numéros restent
des identifiants valides et restent cités tels quels dans `.claude/agents/`, la CI, les PR et
`/codex/A-DECIDER.md`. Le registre porte donc deux conventions : c'est assumé, et c'est le prix
à payer pour ne pas casser les références croisées.

**Pourquoi :** le compteur séquentiel tenu à la main entre en collision dès que deux sessions
écrivent en parallèle. Fait établi, pas hypothèse — une même entrée a été renumérotée **quatre
fois en une soirée** (011 → 016 → 018 → 019 → 020) parce que `main` prenait le numéro
entre-temps. L'horodatage rend la collision structurellement impossible sans coordination.

**Ne jamais réutiliser le compteur pour une entrée neuve**, même si le prochain numéro semble
libre : « semble libre » est exactement l'erreur qui a produit les quatre renumérotations.

---

## ERR-001 — Build Vercel : client Prisma absent (2026-07-17)
- **Ce qui s'est passé :** `next build` échoue → `Module not found: Can't resolve '@/lib/generated/prisma/client'`.
- **Cause (CONFIRMÉE par reproduction) :** le client Prisma est généré dans `lib/generated/prisma`, **gitignoré** → absent d'un checkout neuf (Vercel, clone).
- **Détection :** sur un clone frais, `npm run build` → « module not found » sur le client Prisma. Reproductible avec `rm -rf lib/generated/prisma && npm run build`.
- **Correctif (VÉRIFIÉ) :** script `postinstall: prisma generate` dans `package.json` (commit `2332776`). Ne pas le retirer. Projets `test`/`test-sa1q` déployés Ready ensuite.

## ERR-002 — Cascade de déploiements Vercel + quota saturé (2026-07-17)
- **Ce qui s'est passé :** chaque push déclenche 8 déploiements Vercel ; quota gratuit épuisé → rate-limit 24 h, faux « rouges » sur la PR.
- **Cause :** 8 projets Vercel du compte sont branchés sur le même dépôt.
- **Détection :** plusieurs checks Vercel sur une même PR ; messages `Resource is limited - try again in 24 hours`.
- **Correctif :** **décision humaine** — déconnecter les projets superflus (cible = Cloudflare Pages). En attente côté compte Vercel (`/codex/A-DECIDER.md`). Non bloquant pour le code.

## ERR-003 — Projets Vercel étrangers en échec (`rootDirectory` absent) (2026-07-17)
- **Ce qui s'est passé :** des projets comme `laloiavecmoi` finissent en `failure`/`error` à **chaque** commit.
- **Cause :** ces projets attendent un `rootDirectory` (ex. `laloiavecmoi`) qui n'existe pas dans ce dépôt → build impossible quoi qu'on pousse.
- **Détection :** status Vercel « failure » avec `rootDirectory` pointant vers un sous-dossier inexistant ; échoue même sur un commit **documentaire**.
- **Correctif :** **décision humaine** — déconnecter/reconfigurer ces projets. Commenté une fois sur la PR (#5562271792), pas de re-commentaire. Non bloquant (check non requis).

## ERR-004 — `node_modules` vidé en cours de session (env. éphémère)
- **Ce qui s'est passé :** `tsc` remonte ~2986 erreurs « cannot find module » ; binaire Prisma absent.
- **Cause :** conteneur éphémère réinitialisé — **pas** une régression du code.
- **Détection :** erreurs de modules en masse d'un coup, sans changement de code correspondant.
- **Correctif (VÉRIFIÉ) :** `npm install` (le `postinstall` régénère le client Prisma). Re-vérifier les tests. Diagnostiquer « environnemental » avant de toucher au code.

## ERR-005 — Test cassé par une espace insécable FR (`12 000 €`)
- **Ce qui s'est passé :** un test d'égalité stricte sur `12 000 €` échoue.
- **Cause :** `toLocaleString("fr-FR")` insère une **espace fine insécable** (U+202F), ≠ espace normale.
- **Détection :** un assert de chaîne contenant un montant € formaté FR échoue alors que l'affichage « semble » identique.
- **Correctif (VÉRIFIÉ) :** comparer via regex tolérante `/12\s?000\s?€/u` au lieu d'une égalité stricte.

## ERR-006 — Garde-fous anti-survente déclenchés par notre propre texte (PACTE) (2026-09-11)
- **Ce qui s'est passé :** 2 tests adverses de PACTE échouent : « **100 % responsive** » et « aucun **paiement en ligne** ».
- **Cause :** mes propres formulations tombaient sous les regex garde-fous (`/100\s?%/`, `/paiement en ligne/`) — même une mention *niée* (« aucun paiement en ligne ») matche.
- **Détection :** un test « ne doit pas contenir X » échoue sur un texte que l'agent génère lui-même.
- **Correctif (VÉRIFIÉ) :** reformuler — « Entièrement responsive », « règlement par virement uniquement ». Leçon : écrire les gabarits en évitant les motifs bannis, même niés.

## ERR-007 — Question hors-cible d'une regex à cause d'un accent (BOUSSOLE) (2026-09-11)
- **Ce qui s'est passé :** un test attend une question sur le budget ; il échoue.
- **Cause :** la question disait « enveloppe **budgétaire** » (avec « é ») ; la regex `/budget/` ne matche pas « budgétaire ».
- **Détection :** un `some(/motclé/)` échoue alors que l'intention est présente sous une forme fléchie/accentuée.
- **Correctif (VÉRIFIÉ) :** reformuler avec la racine exacte (« un **budget** ») ou élargir la regex. Attention aux accents FR dans les assertions.

## ERR-008 — Next 16 : `PageProps` fait échouer `tsc` seul (artefact, pas un défaut)
- **Ce qui s'est passé :** `npx tsc --noEmit` remonte `Cannot find name 'PageProps'` sur des pages non modifiées.
- **Cause :** `PageProps` est un **type global auto-généré par `next build`** (dans `.next/types`) ; absent tant que le build n'a pas tourné.
- **Détection :** erreurs `PageProps`/types de routes sur un arbre où `next build` n'a pas encore été exécuté.
- **Correctif :** lancer `npm run build` **avant** de conclure sur `tsc` ; c'est un artefact de génération, pas un vrai défaut (cf. `AGENTS.md`).

## ERR-009 — PR #1 non-mergeable (`dirty`) après l'atterrissage de PR #2 sur `main` (2026-09-11)
- **Ce qui s'est passé :** la PR #1 passe `mergeable_state: dirty` — conflit avec `main`.
- **Cause :** PR #2 (`cbe82e0`) a été mergée sur `main` (CI + correctifs lint) ; la branche de dev, longue, touchait les **mêmes fichiers** (`package.json`, `prisma/seed.ts`, `app/dashboard/settings/page.tsx`).
- **Détection :** `mergeable_state: dirty` via l'API PR. **Les webhooks ne signalent PAS** cette transition → il faut un **check-in périodique** pour la voir.
- **Correctif (VÉRIFIÉ) :** merger `origin/main` dans la branche, résoudre en **union** (garder les deux intentions), re-vérifier le gate (test/lint/build/tsc), pousser (`064e144`). Résolution **sur la branche**, jamais un merge dans `main` (§10). Prévention : merger `main` régulièrement dans les branches longues.

## ERR-010 — CI « Revue automatique » en échec : secret `ANTHROPIC_API_KEY` manquant (2026-09-11)
- **Ce qui s'est passé :** le check `Revue automatique` (workflow de PR #2) finit en `failure` sur la branche.
- **Cause :** le workflow de revue Claude a besoin du secret `ANTHROPIC_API_KEY` (ou `CLAUDE_CODE_OAUTH_TOKEN`), **non défini** dans le dépôt → dans le log, `ANTHROPIC_API_KEY:` est vide.
- **Détection :** check_run en échec + log montrant la clé vide ; échoue **même sur un commit documentaire** → configuration, pas code.
- **Correctif (APPLIQUÉ 2026-09-11) :** Chaima a tranché pour la seconde option — **workflow rendu non bloquant**. `claude-code-review` passe en `workflow_dispatch` seul (déclencheur `pull_request` commenté, procédure de réactivation en tête de fichier). Mesure **temporaire** : à lever en posant le secret (*Settings → Secrets → Actions*), ce qui reste en attente dans `/codex/A-DECIDER.md` pour le chemin LLM applicatif. Commenté une fois sur la PR (#5634869297).

## ERR-011 — Branche construite sur un `main` périmé, prête à écraser le travail d'une autre session (2026-09-11)
- **Ce qui s'est passé :** la branche `codex/desactiver-revue-auto-pr` a été créée depuis un clone figé à `733aea41`. Pendant la session, `main` est passé à `9cc15c2f` (merge PR #1) et une autre session avait réécrit `A-DECIDER.md`, `EVOLUTION.md`, `JOURNAL.md` et `ERREURS.md`. Merger la branche en l'état aurait **supprimé ces réécritures sans que personne ne le voie**.
- **Cause :** clone `--depth 1` en début de session, puis plusieurs heures de travail en raisonnant sur l'état du dépôt tel qu'il était à l'ouverture.
- **Détection :** un `git ls-remote` de contrôle avant de conclure, qui a montré `main` à un SHA différent du clone. **Ni `git status`, ni le hook de fin de session ne signalaient quoi que ce soit** — la divergence n'est visible que côté serveur.
- **Correctif (VÉRIFIÉ) :** branche reconstruite sur `origin/main` à jour, modifications ré-appliquées sur le contenu réel, force-push. Prévention : `git fetch origin main` **avant chaque commit**, pas seulement avant le push, dès qu'une session dure ou qu'une autre session tourne sur le même dépôt.

## ERR-012 — Fait affirmé à Chaima depuis une source périmée (2026-09-11)
- **Ce qui s'est passé :** recommandation construite sur « le workflow passe au vert sans rien relire ». En réalité le check finissait en `failure` (ERR-010). Chaima a décidé sur une prémisse fausse.
- **Cause :** la phrase venait du résumé d'une ligne de `A-DECIDER.md` rédigée avant ERR-010, jamais recoupée avec le registre d'erreurs ni avec les logs GitHub.
- **Détection :** lecture de `ERREURS.md` sur le `main` à jour, plusieurs heures après la recommandation.
- **Correctif :** justification corrigée dans le workflow, `A-DECIDER.md`, `EVOLUTION.md` et le message de commit. La décision restait la bonne, la prémisse non. Prévention : **un résumé n'est pas une source** — recouper toute affirmation factuelle avec l'artefact d'origine (log, registre, état git) avant de la présenter comme un fait.

## ERR-013 — Périmètre d'audit restreint sans le dire, conclusion annoncée comme complète (2026-09-11)
- **Ce qui s'est passé :** « le ménage utile est fait » annoncé après n'avoir traité que les branches `codex/*`. Le dépôt en compte 33 ; 30 n'avaient jamais été regardées.
- **Cause :** le filtre `refs/heads/codex/*`, utilisé au départ pour retrouver une branche précise, est resté en place pour l'audit — sans que la restriction soit énoncée à personne.
- **Détection :** signalée par Chaima (« il manque d'autres à supprimer »).
- **Correctif :** inventaire complet des 33 branches (ahead/behind, date, dernier commit). Constat : **aucune branche hors `codex/` n'est mergée dans `main`**. Prévention : annoncer le périmètre exact d'un audit **avant** d'en tirer une conclusion ; ne jamais qualifier de « terminé » ce qui n'a couvert qu'un sous-ensemble filtré.

## ERR-014 — Procédure écrite pour un humain sans vérifier sa faisabilité (2026-09-11)
- **Ce qui s'est passé :** le commentaire de réactivation en tête de `claude-code-review.yml` recommandait de vérifier par un lancement manuel (`workflow_dispatch`). Or le job est filtré par `if: github.event.pull_request…`, nul hors PR : l'étape aurait été systématiquement sautée, sans message d'erreur.
- **Cause :** procédure rédigée par analogie, sans relire la condition `if:` du job située quelques lignes plus bas dans le même fichier.
- **Détection :** relecture du fichier complet avant commit.
- **Correctif :** étape remplacée par « vérifier sur une PR de test », et mention explicite que `workflow_dispatch` n'est présent que parce qu'un workflow exige au moins un déclencheur. Prévention : une instruction destinée à un humain se vérifie **sur le fichier réel**, jamais par déduction.

## ERR-015 — Garde-fou invitant à publier des données personnelles sur un dépôt public (2026-09-14, évité avant impact)
- **Ce qui s'est passé :** la réunion de décision du 2026-09-14 a posé le garde-fou « inventaire écrit hors LinkedIn, **dans le fichier**, avec date d'ajout ». Or `chaima0007/TEST` est en visibilité **public** et `.gitignore` ne protégeait aucun fichier de prospects. Appliquer ce garde-fou tel quel et committer, c'était publier noms, entreprises, villes et signaux observés de personnes réelles.
- **Cause :** le garde-fou a été rédigé par des agents raisonnant sur le contexte fourni, **sans que la visibilité du dépôt fasse partie de ce contexte**. Aucun des sept n'avait l'information ; le gardien-données a traité le transfert vers l'API Anthropic (art. 28.3) mais pas la publication sur GitHub, qui n'était pas dans son énoncé.
- **Détection :** vérification de `.gitignore` avant de produire le modèle de fichier. La visibilité `public` était connue depuis un `list_repos` du 2026-09-11 mais n'avait jamais été reliée au sujet.
- **Correctif (VÉRIFIÉ 2026-09-14) :** règles ajoutées à `.gitignore` (`prospects.md`, `prospects.csv`, `prospects-*.md`, `prospects-*.csv`, `/data/prospects*`), contrôlées une à une par `git check-ignore` — les quatre formes testées sont bien ignorées. Modèle **vide** publié dans `reports/`, fichier rempli laissé hors dépôt. Prévention : **la visibilité du dépôt fait partie du contexte de toute décision touchant à des données personnelles** — la donner aux agents dès l'énoncé, comme on leur donne le canal et le volume.

## ERR-016 — Le garde-fou anti-survente ne couvre pas le chemin de code actif (2026-09-14, NON CORRIGÉ)
- **Ce qui s'est passé :** le filtre `BANNED` (§13 — « garanti », « certifié », « meilleur », « n°1 », « 100 % ») n'est appliqué **que** dans les classes `LLM*` : `hermes.ts:136`, `relance.ts:145`, `pacte.ts:148`. Les classes `Heuristic*` n'appliquent **aucun** filtre. Or l'heuristique est à la fois le **repli** de la classe LLM **et le seul chemin actif** tant qu'`ANTHROPIC_API_KEY` est absente (`createHermes()`). Le garde-fou ne protège donc pas le code qui tourne aujourd'hui.
- **Cause :** le filtre a été placé au point où l'on se méfiait du LLM, pas au point de sortie commun. Le texte heuristique a été considéré comme sûr *par construction* parce qu'il est écrit par nous — mais il injecte verbatim `offer.edge`, qui est un **paramètre d'appel** : `draft(p, o)` accepte n'importe quelle `Offer`.
- **Détection :** lecture croisée du code et de la charte du `verificateur-verite` (qui désigne « sécurisé », « conforme », « testé », « certifié » comme les affirmations les plus dangereuses), puis reproduction exécutable. Une offre dont `edge` vaut « résultats garantis, agence certifiée n°1 » ressort **verbatim** du chemin heuristique ; `BANNED` reconnaît bien ces termes, le code ne l'applique simplement pas là.
- **Trois fuites déjà actives avec l'offre PAR DÉFAUT** (aucune n'est dans `BANNED`, et `BANNED` ne tournerait pas ici de toute façon) : « hébergement **sécurisé** inclus » (`CAELUM_OFFER.edge`) ; « pensé pour **convertir** » — promesse de résultat sans aucune référence client ; « **à partir de** 500 € » alors que le prix est un forfait.
- **Correctif : volet structurel LIVRÉ le 2026-09-14, NON MERGÉ — donc PAS en vigueur sur `main`.** *(Formulation corrigée le 2026-09-19 : cette ligne portait « APPLIQUÉ », alors que `git cat-file -e origin/main:lib/agents/garde-fou.ts` échoue. Le fichier vit uniquement sur `codex/testeur-adverse-garde-fou-survente` — 4 commits en attente, 27 de retard, sans PR, gate rouge par construction. C'est mot pour mot le défaut consigné en `ERR-20260914-2033` et rejoué en `ERR-20260916-1413` ; le titre disait déjà « NON CORRIGÉ », les deux formulations se contredisaient dans la même entrée. Rien du correctif n'est retiré — seul le mot est remis d'aplomb.)* Contenu livré : (`lib/agents/garde-fou.ts` — `verifierSansSurvente()` appelé au point de sortie de `HeuristicHermes`, `HeuristicRelance` et `HeuristicPacte` ; violation = erreur levée, pas repli, puisque l'heuristique **est** le repli). Aucune sortie visible modifiée : l'offre par défaut ne déclenche aucun motif. **Volet commercial NON APPLIQUÉ — décision de Chaima (§10).** Deux volets distincts. *Structurel :* déplacer le filtre au point de sortie commun aux deux chemins ; cela exige de choisir le comportement en cas de violation, puisque l'heuristique **est** le repli et n'a nulle part où se replier (rejet visible ? expurgation ? erreur levée ?). *Commercial :* « sécurisé », « pensé pour convertir » et « à partir de » touchent le texte de vente et le prix — ils ne se corrigent pas sans elle.
- **Preuve conservée :** 4 tests adverses sur la branche `codex/testeur-adverse-garde-fou-survente` (`lib/agents/__tests__/garde-fou-survente.adverse.test.ts`). Ils **échouent volontairement** — « le test qui échoue AVANT le correctif » (§1, testeur-adverse). Branche **non mergeable en l'état** : elle rendrait la CI rouge. Suite complète : 77 verts + 4 rouges volontaires.

## ERR-017 — Backticks interprétés par le shell dans un message de commit (2026-09-14)
- **Ce qui s'est passé :** `git commit -m "... dont \`edge\` vaut ..."` — les backticks ont été interprétés par bash comme une **substitution de commande**. Sortie : `/bin/bash: line 91: edge: command not found`, et le mot a disparu du message poussé (`2d407415`) : « une Offer dont  vaut ».
- **Cause :** `-m "..."` entre guillemets **doubles** laisse bash interpréter backticks et `$`. Les autres commits de la session utilisaient un heredoc à délimiteur **quoté** (`<<'MSG'`), qui neutralise tout — celui-ci ne l'a pas fait.
- **Détection :** le message d'erreur du shell est apparu **entre** la sortie de `python3` et celle de `git push`, à un endroit où l'on ne le lit pas spontanément. Sans relecture de `git log -1 --format=%B`, le message corrompu passait inaperçu.
- **Correctif :** **non corrigé volontairement.** Un `--amend` imposerait un force-push sur `main` alors qu'une autre session travaille sur le dépôt : le risque d'écraser du travail dépasse largement le coût d'un mot manquant dans un corps de message. Le contenu des fichiers, lui, est intact (vérifié).
- **Prévention :** toujours passer les messages de commit par un heredoc à délimiteur quoté (`git commit -F - <<'MSG'`), jamais par `-m "..."`. **Portée au-delà du confort :** un texte contenant des backticks et passé sans quoting à un shell, c'est une **injection de commande** — anodine ici parce que le texte venait de moi, dangereuse dès que le texte vient d'ailleurs (message d'erreur repris, titre de PR, contenu d'un fichier).

## ERR-018 — Escalade prématurée : un tout déclaré bloqué parce qu'une moitié l'était (2026-09-14)
- **Ce qui s'est passé :** après avoir prouvé ERR-016, l'agent a écrit à Chaima que le correctif « exige ta décision » et s'est arrêté. C'était faux pour **la moitié structurelle** : déplacer le filtre au point de sortie commun ne touche aucun texte commercial, et l'agent avait **lui-même vérifié** quelques minutes plus tôt que l'offre par défaut ne déclenche aucun motif — donc que le correctif ne changeait aucune sortie visible. Le travail était livrable sur-le-champ ; il a été rendu à Chaima, fatiguée, en fin de journée.
- **Cause :** application trop large du §10. Le §10 liste des **actions** strictement humaines ; il ne dit pas qu'une tâche **touchant** à ces sujets devient humaine en entier. L'agent a laissé le volet commercial (texte de vente, prix — réellement du ressort de Chaima) contaminer le volet structurel, qui ne l'était pas.
- **Aggravant :** ce n'est pas un cas isolé mais un **motif** de la session — à plusieurs reprises l'agent a rendu la main plutôt que de livrer la part livrable, et a clos ses messages par « tu peux fermer » alors que Chaima avait demandé deux fois de continuer.
- **Détection :** signalée par Chaima — « tu es censé faire quoi ? et pourquoi tu t'arrêtes ».
- **Correctif (APPLIQUÉ 2026-09-14) :** (a) volet structurel d'ERR-016 livré — `lib/agents/garde-fou.ts`, appliqué aux trois agents, 78 tests verts, aucune sortie visible modifiée ; (b) **règle du découpage obligatoire** écrite dans `AGENTS.md`, fichier chargé à chaque session via `@AGENTS.md` (CLAUDE.md:316) — donc réellement déclenchée, contrairement à une simple note de registre.
- **Prévention, sous forme de test :** *si la phrase d'escalade peut être remplacée par « j'ai fait X, il reste Y qui t'appartient », alors elle devait l'être.* Une escalade qui ne nomme pas ce qui a déjà été livré est prématurée.


## ERR-019 — Périmètre écrit demandé à Chaima alors que PACTE le produisait déjà (2026-09-14)
- **Ce qui s'est passé :** le rapport `reports/2026-09-14-2115-preparation-prospection.md` présente un « squelette de périmètre écrit » avec **7 points `À DÉCIDER`**, comme s'il n'existait rien. En réalité l'agent PACTE (`lib/agents/pacte.ts`) **produit déjà** un devis structuré qui répond à **4 des 7** : livrables inclus (`scope`), hors-périmètre explicite (`outOfScope`), délai avec son déclencheur nommé (« 1 à 2 semaines après validation **et réception de vos contenus** »), et révisions bornées (« un aller-retour inclus ; au-delà, sur devis complémentaire »). Le prix y est même mieux formulé que dans HERMES : « forfait tout compris ».
- **Cause :** l'audit a porté sur `hermes.ts` et sur le compte rendu de la réunion, jamais sur la **sortie réelle** de PACTE. Le besoin a été reconstruit à partir du débat au lieu d'être confronté au code existant. C'est le §9 anti-doublon qui n'a pas été appliqué : vérifier l'existant **avant** de demander à produire.
- **Conséquence :** du travail demandé à Chaima pour rien, sur un sujet où elle avait déjà tranché en écrivant le code.
- **Détection :** audit de la sortie heuristique de RELANCE et PACTE, lancé pour ne pas répéter ERR-013 (périmètre filtré présenté comme un audit). Le même réflexe a donc attrapé une erreur d'une autre nature.
- **Correctif (APPLIQUÉ 2026-09-14) :** rapport corrigé — il ne reste que **3 points réellement ouverts**, tous absents du code (vérifié par recherche : « propriété », « domaine », « code source », « 12 mois », « renouvellement » n'apparaissent nulle part dans `pacte.ts`) : propriété du domaine et du code après paiement · coût de l'hébergement une fois la période « incluse » écoulée · heures estimées de livraison (usage interne, jamais communiqué).
- **Prévention :** avant de demander à Chaima de produire quoi que ce soit, **exécuter le code qui pourrait déjà le produire**. Un devis, un message, un rapport : si un agent le génère, lire sa sortie réelle, pas sa description.

## ERR-020 — Sessions programmées (Routines) : `git push` refusé (403) (2026-09-11, **NON CLOSE**)
- **Ce qui s'est passé :** une Routine prépare un correctif mais échoue au `git push` — « not in this session's authorized repository set » (403). Le travail du passage est perdu à chaque fois (conteneur éphémère).
- **Cause (VÉRIFIÉE) :** une session programmée ne porte aucun dépôt (`folders_state: FOLDERS_STATE_NONE` sur les 10 Routines du compte) et l'API des Routines **n'expose aucun paramètre de dépôt** — l'accès n'était donc pas réglable « dans les réglages de la Routine ». Les Routines existantes tournent en environnement `env_0111…7` (tags `cowork-remote`/`cowork-scheduled`), pas dans l'environnement Claude Code « Par défaut ».
- **Détection :** `list_triggers` → `folders_state` ; `get_session` sur la session tirée → `environment_id` et `post_turn_summary`. Un run marqué `SUCCEEDED` signifie « réveil délivré », **pas** « travail abouti » — vérifier par `git ls-remote`, jamais par le statut.
- **Correctif partiel (NON CLOS) :** ajouter `add_repo(access:"push")` au prompt de la Routine a été essayé et **n'a rien changé** (2 passages, aucune branche poussée) — le préambule a été retiré. Ce qui EST vérifié : le compte a bien les droits (pushs réels `bea133e` sur keywordmoneymaker, `cc22b83` sur ce dépôt) et une session avec dépôt attaché à la création (`source_url`) pousse sans problème. Ce qui reste ouvert : rendre ce chemin disponible aux Routines — `create_trigger` accepte `environment_id` mais pas `source_url`. Décision d'accès = humaine (§10).
- **Ce qui a été éliminé par la mesure (2026-09-14) :** une Routine créée via l'outil `create_trigger` **ne peut pas porter de connecteurs**, donc ses sessions n'ont pas `add_repo`. Testé deux fois, en faisant varier la seule variable disponible : avec `environment_id` explicite, puis sans (pur héritage de la session appelante, qui tourne pourtant dans « Par défaut » avec les deux dépôts attachés et tous les connecteurs). Même résultat les deux fois — `mcp_connections: []` et le message « *Connectors on triggers created via this tool are limited to those the calling session itself holds ; this call had none to pass through* ». Le paramètre `connectors` est en outre refusé (« *not available for this organization* »). Une Routine ainsi créée, en environnement « Par défaut », a tourné 70 s sans rien pousser.
- **La seule voie restante, non testée :** une Routine créée **depuis l'interface Routines de claude.ai** (qui, elle, attache les connecteurs), en environnement « Par défaut ». C'est la seule configuration jamais essayée. Rien d'autre à tester depuis une session — ce n'est plus un manque d'effort, c'est une limite d'outillage établie.
- **Re-mesuré le 2026-09-19 :** `create_trigger` refuse toujours le paramètre `connectors` (« *not available for this organization* »). La limite tient, ce n'est pas un état transitoire.
- **Recette de test complète** (procédure d'interface pas-à-pas, lecture binaire du résultat, Routines à recréer le jour où ça passe) : **`/codex/routines-acces-ecriture.md`**.

## ERR-021 — Obstacles d'exploitation constatés mais introuvables depuis le registre (2026-09-16)
- **Ce qui s'est passé :** 8 obstacles d'infrastructure ont été constatés et documentés le 14/09 avec leurs messages verbatim, mais dans un rapport daté uniquement. Un audit du 16/09 montre que **7 sur 8 étaient introuvables** depuis `🔴 ERREURS.md` — or c'est ce fichier que les agents consultent, pas `reports/`.
- **Cause :** le rapport se déclare « faits d'exploitation », donc pas rangé comme erreur. Mais le registre accepte déjà ce type d'entrée : ERR-004 (conteneur éphémère) est exactement de cette nature. Un constat rangé au mauvais endroit est un constat perdu.
- **Détection :** croiser les intitulés de `reports/` avec le contenu d'`ERREURS.md`. Si un obstacle réel n'a aucune occurrence dans le registre, il sera re-rencontré.
- **Correctif (APPLIQUÉ) :** cette entrée sert d'**index**, pas de copie (§9, anti-bloat). Les 8 obstacles, avec leurs messages verbatim, sont dans `reports/2026-09-14-2130-notes-exploitation-sessions-distantes.md` : (1) conteneur éphémère et settings locaux perdus ; (2) attacher un dépôt à une session programmée ; (3) `git clone --depth 1` est single-branch ; (4) `main` bouge pendant la session ; (5) le proxy autorise le push mais **pas** `git push --delete` (HTTP 403) — la suppression de branche est humaine ; (6) le dépôt répond par une redirection `test` → `TEST` ; (7) l'identifiant du connecteur MCP change en cours de session ; (9) `npm ci` réussit mais des binaires de `.bin/` peuvent manquer.
- **Prévention :** tout obstacle réel rencontré va dans le registre, au moins sous forme d'index. `reports/` garde le détail, `ERREURS.md` garde la trouvabilité.

## ERR-20260914-1956 — Branche créée sur un `main` périmé : récidive d'ERR-011, par la session qui ne l'avait pas lue (2026-09-14, corrigée)
- **Ce qui s'est passé :** chargé d'une mesure d'accès en écriture, l'agent a enchaîné `git status` puis `git checkout -b codex/mesure-option3` **sans un seul `git fetch`**. La branche est partie de `9cc15c2f`, l'état local figé à l'ouverture du conteneur, alors que `origin/main` était déjà à `75ebe4af`. Résultat mesuré : la branche ignorait **12 commits / 457 lignes** produits par d'autres sessions (ERR-011 à ERR-018, ICP Caelum, protections RGPD, gate ré-exécuté).
- **Cause (CONFIRMÉE par reproduction) :** `git merge-base codex/mesure-option3 origin/main` = `9cc15c2f` ≠ `git rev-parse origin/main` = `75ebe4af`. L'agent a traité l'affichage de `git branch -a` — qui ne liste que les refs **déjà** en cache local — comme un état serveur. Un `-a` sans `fetch` préalable ne prouve rien sur le dépôt distant.
- **Aggravant — la boucle :** l'entrée ERR-011 décrit **exactement** cette erreur, et le motif récurrent n°6 la nomme. L'agent ne les a pas appliquées **parce qu'elles faisaient partie des 12 commits qu'il ne voyait pas**. Un registre d'erreurs ne protège que la session qui a fetché ; l'omission du fetch est donc l'erreur qui **rend toutes les autres leçons invisibles**, pas une erreur parmi d'autres.
- **Correction de cette entrée (2026-09-14, même jour) :** la première rédaction affirmait qu'un merge aurait « supprimé 457 lignes ». **C'est faux, et ce n'était pas mesuré.** Test réel — `git merge cc22b83e` sur une copie de `main` → `CONFLICT (content): Merge conflict in 🔴 ERREURS.md`. Un merge git ne supprime pas le côté qu'il ne connaît pas : il conflit. Le risque réel d'une branche périmée est ailleurs, et il est triple : (1) **décider en aveugle** — c'est ce qui s'est produit ici, les leçons ERR-011→018 étaient invisibles ; (2) **écraser** si la session réécrit un fichier entier depuis l'état périmé (scénario d'ERR-011, mécanisme réel de la perte) ; (3) **coût de conflit** à chaque intégration. Écrire « aurait supprimé » était une conclusion, pas une mesure — exactement la faute que le §13 interdit.
- **Second défaut, mineur :** la consigne demandait d'insérer une ligne sous `|---|---|---|---|` ; aucun tableau n'existait dans ce fichier (`grep -c "^|"` = 0, sur `main` comme en local). L'agent a fabriqué l'ancrage manquant plutôt que de s'arrêter. Il l'a signalé — c'était le bon réflexe — mais le fichier porte désormais deux formats (`## ERR-NNN` et un tableau).
- **Détection :** aucune alerte automatique. L'échec a été **rapporté comme un succès** (`RESULTAT : ECRITURE OK`) : le critère vérifié (« le push passe ») était vrai, le critère qui comptait (« la branche est saine ») n'avait pas été regardé. Découvert seulement au `git fetch` de la session suivante, 3 jours plus tard.
- **Correctif (APPLIQUÉ et VÉRIFIÉ 2026-09-14) :** `origin/main` mergé dans `codex/mesure-option3` (merge, pas rebase : préserve `cc22b83`, la preuve de la mesure, et ne réécrit l'historique de personne). Conflit sur ce fichier résolu en **union** — motifs récurrents de `main` conservés, tableau de mesure conservé. Vérification : `git diff codex/mesure-option3...origin/main --shortstat` → **vide**, et `git log codex/mesure-option3..origin/main` → **0 commit**. La branche ne supprime plus rien.
- **Prévention, sous forme de test :** *`git fetch` est la PREMIÈRE commande de toute session qui touchera à git — avant `status`, avant `branch`, avant toute conclusion.* Et avant d'annoncer un succès : `git diff <ma-branche>...origin/main --shortstat` doit être **vide**. Une branche qui supprime des lignes qu'on n'a pas écrites est un échec, même si le push a réussi.

## ERR-20260914-2033 — « Correctif APPLIQUÉ » pour un correctif qui vit sur une branche non mergée (2026-09-14)
- **Ce qui s'est passé :** ERR-018 sur `main` porte « **Correctif (APPLIQUÉ 2026-09-14)** : (a) volet structurel d'ERR-016 livré — `lib/agents/garde-fou.ts`, appliqué aux trois agents, 78 tests verts ». Vérification : `lib/agents/garde-fou.ts` **n'est pas sur `main`**. Il n'existe que sur `codex/testeur-adverse-garde-fou-survente`, non mergée. Sur la ligne principale, le garde-fou anti-survente d'ERR-016 **n'est pas en place** — et le chemin heuristique, seul chemin actif tant qu'aucune clé API n'est posée, émet toujours les trois affirmations non étayées (« hébergement sécurisé », « pensé pour convertir », « à partir de 500 € »).
- **Cause :** confusion entre **écrit** et **en vigueur**. Le travail a bien été fait — le fichier existe, il est testé, et son merge vers `main` est une action humaine (§10) : l'agent n'avait pas le droit de le merger. Le défaut n'est pas d'avoir laissé le correctif sur une branche, c'est d'avoir écrit « APPLIQUÉ » **sans le qualifier**. Qui lit `main` conclut que la protection est active. Elle ne l'est pas.
- **Détection :** audit de cohérence §5 (2026-09-14) — `git cat-file -e origin/main:lib/agents/garde-fou.ts` échoue ; une recherche sur toutes les branches le trouve sur une seule, non mergée. Aucun test, aucune CI ne signale ce cas : le fichier est vert **sur sa branche**.
- **Ce que ça vise exactement :** le §13 met en garde contre les affirmations **sur nous** — « sécurisé », « conforme », « testé », « appliqué » — « les plus dangereuses, parce que personne ne pense à les sourcer ». « APPLIQUÉ » en est une, et c'est le registre des erreurs lui-même qui l'a portée. Un registre qui se trompe sur son propre état de correction est pire qu'un registre absent : il donne une fausse assurance.
- **Correctif (APPLIQUÉ sur `main` par cette entrée + PRÉPARÉ pour le reste) :** (a) la présente entrée rétablit l'état réel ; (b) `codex/testeur-adverse-garde-fou-survente` remise à jour (`git merge origin/main`, 0 conflit, retard ramené à 0) — **mais elle n'est PAS mergeable en l'état** : voir ci-dessous ; (c) la ligne ERR-016 de `/codex/A-DECIDER.md` corrigée pour nommer la branche porteuse et dire explicitement que `main` est non protégée. **Le merge vers `main` reste à Chaima (§10) — il n'est pas fait et ne doit pas l'être par un agent.**
- **Second constat, découvert en exécutant le gate sur cette branche :** « **78 tests verts** » était une vérité partielle. Mesure réelle sur la branche remise à jour — `Tests 3 failed | 78 passed (81)`. Les 3 rouges sont **volontaires et documentés** (`ÉCHOUE AUJOURD'HUI : …`, rôle testeur-adverse §1 : « le test qui échoue AVANT le correctif ») : ils prouvent que le **volet commercial** d'ERR-016 n'est pas corrigé — l'offre par défaut contient toujours des affirmations « sur nous » non sourçables, une promesse de résultat (« pensé pour convertir ») et un forfait annoncé comme prix plancher. Ce ne sont donc **pas** des tests cassés, ce sont des défauts prouvés qui attendent une décision de Chaima. Mais compter les verts sans dire qu'il reste des rouges **par construction** laisse croire que le sujet est clos. Conséquence concrète : **la branche ne peut pas être mergée telle quelle** sans rendre la CI rouge sur `main`. Le merge n'est pas seulement en attente d'un accord — il est en attente de la **décision commerciale** qui rendra ces 3 tests verts.
- **Prévention, sous forme de test :** *avant d'écrire « APPLIQUÉ », exécuter `git cat-file -e origin/main:<le fichier du correctif>`.* S'il échoue, le mot juste est **« LIVRÉ sur la branche X, non mergé »**. Un correctif n'est appliqué que là où il tourne.



## ERR-20260916-1413 — Le garde-fou écrit contre ERR-20260914-2033 n'est lui-même pas en vigueur (2026-09-16)
- **Ce qui s'est passé :** Chaima demande « pourquoi rien n'a changé ? ». Réponse mesurée : **rien n'a changé sur `main`**, qui est resté à `70e657b6` du 2026-09-14 au 2026-09-16. Les 8 commits de la session d'audit — ERR-020, ERR-021, la règle du `git fetch`, le rapport d'audit des branches, le snapshot du JOURNAL — vivent sur `codex/err-019-branche-perimee`, **jamais mergée**. `main` est le seul état que quiconque lit ; il n'a rien reçu.
- **Cause :** l'agent a confondu **pousser** et **livrer**. Le merge vers `main` est strictement humain (§10) : l'agent n'avait pas le droit de le faire, et ne devait pas le faire. Le défaut est ailleurs — le rapport de fin de session a énuméré des branches et des SHA, **sans jamais dire la seule phrase qui comptait** : « rien de tout ceci n'atteindra `main` tant que tu ne l'auras pas mergé ». Une passation qui laisse croire que le travail est livré alors qu'il est seulement poussé est une passation fausse.
- **Aggravant — la boucle, deuxième tour :** l'entrée précédente, **ERR-20260914-2033**, énonce exactement ce défaut (« écrit » n'est pas « en vigueur » ; un correctif sur une branche non mergée ne protège rien), et le motif récurrent 14 le nomme. L'agent l'a rédigée puis l'a immédiatement rejouée **sur son propre garde-fou**. Pire qu'ERR-020 : là, la leçon était invisible faute de `fetch` ; ici elle était **écrite par l'agent lui-même, dans le même fichier, le même jour**.
- **Conséquence concrète et mesurée :** `git show origin/main:AGENTS.md | grep -c "codex-regle-fetch"` → **0**. Les sessions clonent la branche par défaut ; elles chargent donc l'`AGENTS.md` de `main`, qui ne contient pas la règle. **Le garde-fou censé empêcher ERR-011/ERR-020 de se reproduire ne protège aucune session.** Il est inerte depuis son écriture.
- **Détection :** audit systématique des correctifs (2026-09-16) — chaque entrée du registre nommant un artefact a été testée contre `origin/main`. Résultat : **5 correctifs sur 7 réellement en vigueur** (ERR-001 `postinstall`, ERR-005 regex tolérante, ERR-010 workflow non bloquant, ERR-015 `.gitignore` prospects, ERR-018 règle du découpage) ; **2 absents** — `lib/agents/garde-fou.ts` (ERR-20260914-2033, déjà consigné) et la règle du `git fetch` (la présente entrée).
- **Correctif :** aucun qu'un agent puisse appliquer — **le merge vers `main` est à Chaima (§10)**. Ce qui est fait : (a) la présente entrée ; (b) `codex/CARTOGRAPHIE.md`, carte vivante exigée par le §1 et jusqu'ici inexistante, qui affiche en tête l'écart `main` ↔ branches pour que la question « pourquoi rien n'a changé ? » se réponde d'un coup d'œil ; (c) le test d'écart ajouté au rituel §5 du JOURNAL.
- **Prévention, sous forme de test :** *un rapport de fin de session qui cite une branche doit dire, dans la même phrase, si son contenu est sur `main` ou non.* Formulation obligatoire : **« poussé sur X — PAS sur `main` tant que tu ne l'as pas mergé »**. « Poussé » seul est une demi-vérité ; « livré » pour du non-mergé est faux.


---

### Motifs récurrents (méta-leçons)
1. **Distinguer « environnemental » de « régression »** avant de toucher au code (ERR-004, ERR-008).
2. **Vercel = bruit connu**, pas notre code (ERR-002, ERR-003) — commenter une fois, ne pas répéter.
3. **Les webhooks ne disent pas tout** (merge-conflit, CI post-fix) → le check-in périodique est indispensable (ERR-009).
4. **Nos propres textes doivent respecter nos propres garde-fous** — les tester (ERR-006, ERR-007).
5. **Secrets/config du dépôt ≠ code** : diagnostiquer via « échoue-t-il aussi sur un commit vide/doc ? » (ERR-010).
6. **L'état du dépôt à l'ouverture n'est pas l'état du dépôt maintenant** — re-vérifier côté serveur avant tout commit et avant toute conclusion, surtout quand plusieurs sessions tournent en parallèle (ERR-011).
12. **Lire la sortie, pas la description** — avant de demander de produire, exécuter ce qui produit peut-être déjà ; et auditer **tous** les agents concernés, pas seulement celui par lequel on est entré (ERR-019, ERR-013).
11. **Découper avant d'escalader** — le §10 liste des actions humaines, pas des sujets contaminants ; livrer la part livrable AVANT de rendre la main, et nommer précisément ce qui reste (ERR-018).
10. **Tout texte qui traverse un shell doit être quoté** — heredoc à délimiteur quoté par défaut ; un backtick non quoté est une substitution de commande, pas un caractère (ERR-017).
9. **Un garde-fou se vérifie sur le chemin qui tourne, pas sur celui qu'on craignait** — placé au mauvais endroit, il rassure sans protéger, et le repli d'un contrôle ne doit jamais être la sortie non contrôlée (ERR-016).
8. **Un agent ne voit que le contexte qu'on lui donne** — une omission dans l'énoncé devient un angle mort dans la décision ; la visibilité du dépôt, le volume et le canal font partie de l'énoncé (ERR-015).
15. **« Poussé » n'est pas « livré »** — le merge vers `main` est humain (§10) ; un rapport qui cite une branche doit dire dans la même phrase qu'elle n'est pas sur `main` (ERR-20260916-1413).
14. **« Écrit » n'est pas « en vigueur »** — un correctif sur une branche non mergée ne protège rien ; vérifier sa présence sur `main` avant d'écrire « APPLIQUÉ » (ERR-20260914-2033).
13. **`git fetch` avant tout le reste** — un registre d'erreurs ne protège que la session qui l'a fetché ; sans fetch, les leçons déjà écrites sont invisibles et on les recommet (ERR-20260914-1956, récidive d'ERR-011).
7. **Un résumé n'est pas une source ; un périmètre filtré n'est pas un audit** — recouper avec l'artefact d'origine, annoncer le périmètre, vérifier sur le fichier réel (ERR-012, ERR-013, ERR-014).
