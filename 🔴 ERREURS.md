# 🔴 BASE DES ERREURS — TEST / Nexus-Market

> Chaque erreur réelle rencontrée, documentée pour **ne jamais la reproduire**. Consultable
> par tous les agents. Format fixe par entrée : **Ce qui s'est passé · Cause · Comment la
> détecter la prochaine fois · Correctif (VÉRIFIÉ)**. Un incident = une entrée datée.
>
> Vérité totale : seules des erreurs réellement survenues figurent ici, avec leur preuve.

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
- **Correctif : volet structurel APPLIQUÉ le 2026-09-14** (`lib/agents/garde-fou.ts` — `verifierSansSurvente()` appelé au point de sortie de `HeuristicHermes`, `HeuristicRelance` et `HeuristicPacte` ; violation = erreur levée, pas repli, puisque l'heuristique **est** le repli). Aucune sortie visible modifiée : l'offre par défaut ne déclenche aucun motif. **Volet commercial NON APPLIQUÉ — décision de Chaima (§10).** Deux volets distincts. *Structurel :* déplacer le filtre au point de sortie commun aux deux chemins ; cela exige de choisir le comportement en cas de violation, puisque l'heuristique **est** le repli et n'a nulle part où se replier (rejet visible ? expurgation ? erreur levée ?). *Commercial :* « sécurisé », « pensé pour convertir » et « à partir de » touchent le texte de vente et le prix — ils ne se corrigent pas sans elle.
- **Preuve conservée :** 4 tests adverses sur la branche `codex/testeur-adverse-garde-fou-survente` (`lib/agents/__tests__/garde-fou-survente.adverse.test.ts`). Ils **échouent volontairement** — « le test qui échoue AVANT le correctif » (§1, testeur-adverse). Branche **non mergeable en l'état** : elle rendrait la CI rouge. Suite complète : 77 verts + 4 rouges volontaires.

> ⚠️ **CORRECTION DATÉE DU 2026-09-19 (ajoutée sans réécrire l'entrée ci-dessus).** Le « volet structurel APPLIQUÉ » annoncé ci-dessus **n'est pas sur `main`** : `lib/agents/garde-fou.ts` n'existe que sur `codex/testeur-adverse-garde-fou-survente`, non fusionnée. Sur le code actif, `verifierSansSurvente` n'est appelé nulle part et **les trois fuites sont vivantes** (`hermes.ts:32`, `hermes.ts:75`, `pacte.ts:74`). **Le titre « NON CORRIGÉ » est donc exact.** Voir ERR-028.

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

## ERR-020 — 22 vulnérabilités de dépendances, jamais consignées nulle part (2026-09-14)
- **Ce qui s'est passé :** `npm audit` sur `main` (`bc6be2c5`) remonte **22 vulnérabilités : 3 critiques, 11 hautes, 8 modérées**. Aucun document du projet (ETAT, JOURNAL, A-DECIDER, ERREURS, PROPRIÉTÉ) ne les mentionne. Directes et critiques : `next` 16.2.9 et `next-auth` 5.0.0-beta.31 (→ `@auth/core` ≤ 0.41.2, contournement de normalisation d'e-mail par homoglyphe `@`, GHSA-7rqj-j65f-68wh).
- **Sévérité : CRITIQUE** — §9 angle Sécurité. `next-auth` porte l'**authentification** de l'app.
- **Cause racine :** le gate avant push du §4 Parcours 4 est `lint && tsc && test && build`. **Aucune étape n'interroge les dépendances.** Une classe entière de défauts n'a jamais eu d'organe de détection — ce n'est pas un oubli ponctuel, c'est un trou dans le protocole.
- **Recherche de solution existante (mission §9) : AUCUNE.** Rien dans `🔴 ERREURS.md` (ERR-001→015), rien dans `codex/EVOLUTION.md`, rien dans la base Caelum (`.claude/BASE-ERREURS.md`, E-01→E-25). → **ERREUR SANS SOLUTION DOCUMENTÉE.**
- **Détection (à retenir) :** `npm audit` fonctionne **sans `node_modules`** (il lit `package-lock.json`) — donc exécutable même en conteneur neuf.
- **SOLUTION_020 préparée, NON APPLIQUÉE :** (a) `npm audit fix` pour `next` → 16.3.5 et `next-auth` → beta.32 (`isSemVerMajor: false`, non cassant d'après npm) ; (b) **ne pas** appliquer le correctif `prisma` : npm propose une **rétrogradation majeure** 7.10 → 6.19.3, inacceptable sans arbitrage ; (c) ajouter `npm audit --audit-level=high` au gate §4 et à `ci.yml`. **EN ATTENTE DE GO.**

## ERR-021 — Cinq PR ouvertes depuis juin/juillet, hors de tout suivi (2026-09-14)
- **Ce qui s'est passé :** le dépôt porte **5 PR ouvertes** — #3, #4, #5 (brouillons), #6, #7 — créées entre le 2026-06-21 et le 2026-07-17. **Aucune n'apparaît dans `codex/A-DECIDER.md`.** #4 et #5 ciblent `claude/swarm-50-agent-architecture-3l6cno`, elle-même la branche de la PR #3 : une pile de brouillons empilés sur un brouillon.
- **Sévérité : IMPORTANT** — §9 angles Humain/Exécution et Stratégique.
- **Cause racine :** `A-DECIDER.md` suit les **décisions formulées par un agent**, pas l'**état réel de la forge**. Rien ne fait entrer une PR dans le registre : il faut qu'un agent y pense. Personne n'y a pensé en 3 mois.
- **Solution existante liée : PARTIELLE.** ERR-013 (2026-09-11) a traité le même angle mort côté **branches** (33 inventoriées) et la session du 2026-09-14 21h16 en a tiré une ligne A-DECIDER (« sortir les projets étrangers »). **Pourquoi la récurrence :** le correctif d'ERR-013 portait sur les branches uniquement ; les PR n'ont pas été rattachées au même inventaire.
- **SOLUTION_021 préparée, NON APPLIQUÉE :** ajouter une ligne A-DECIDER « Statut des 5 PR ouvertes » et étendre le rituel §5 à `list_pull_requests(state=open)` en plus de `git ls-remote`. **EN ATTENTE DE GO.**

## ERR-022 — Un merge ne met pas à jour les registres d'état (récurrent, 2 projets) (2026-09-14)
- **Ce qui s'est passé :** trois occurrences du même défaut, toutes constatées aujourd'hui.
  1. **TEST** — `ETAT.md` et `00-LIRE-D-ABORD.md` ont annoncé « PR #1 ouverte, pas encore mergée » pendant **3 jours** après son merge (`9cc15c2f`, 2026-09-11 19h19). Corrigé à 21h16 par une session concurrente (`bc6be2c5`).
  2. **Caelum** (`chaima0007/keywordmoneymaker`, `main` = `90b1c87`, PR #21 mergée 2026-09-14 19h40) — `codex/A-DECIDER.md` liste toujours « Auto-héberger Fraunces et Inter (RGPD) » **en attente**, alors que `products/caelum/site/assets/caelum.css` sert désormais 4 `.woff2` locaux : la fuite est **fermée**. Le registre décrit un monde vieux d'une heure.
  3. **Caelum** — la fiche **E-08 « Dépôt public sans fichier LICENSE »** est marquée **⚠️ NON CORRIGÉE**, alors que `LICENSE` (tous droits réservés) est présent à la racine depuis la même PR #21.
- **Sévérité : CRITIQUE par escalade** (§11d de la mission : 3 occurrences, même cause racine, 2 projets).
- **Cause racine :** la mise à jour des registres est un **geste manuel de fin de session**, et une session se termine typiquement **sur** le merge. Le merge est donc systématiquement le dernier événement non consigné. Rien dans la CI ni dans le protocole ne rattache un merge à la mise à jour de l'état.
- **Solution existante liée :** ERR-012 (« un résumé n'est pas une source ») nomme le **symptôme** — décider sur un document périmé — mais sa prévention s'adresse au **lecteur** (« recouper avec l'artefact d'origine »), jamais à l'**écrivain**. **Pourquoi la récurrence :** exactement la leçon de la fiche Caelum **E-23** (« une règle ne vaut que si elle s'adresse à celui qui a le pouvoir de l'appliquer »). Le lecteur ne peut pas empêcher le document de vieillir.
- **SOLUTION_022 préparée, NON APPLIQUÉE :** faire porter l'horodatage par la machine, pas par la mémoire — un contrôle CI (ou une étape du §5) qui compare le SHA cité dans `ETAT.md` à `git ls-remote origin main` et échoue s'ils diffèrent de plus de N commits. **EN ATTENTE DE GO.**

## ERR-023 — Passation corrigée à deux endroits sur trois (2026-09-14, preuve immédiate d'ERR-022)
- **Ce qui s'est passé :** le commit `bc6be2c5` (21h16) a corrigé `ETAT.md` et `00-LIRE-D-ABORD.md` pour dire que la branche `claude/nexus-market-agents-63dlku` est close. **`CLAUDE.md:304` continue de la désigner comme « branche de dev » du projet** — et `CLAUDE.md` est le fichier que *tout* agent lit en premier.
- **Sévérité : IMPORTANT** — §9 angle Humain/Exécution. Un agent obéissant repart d'une branche close, 36 commits derrière `main`.
- **Cause racine :** identique à ERR-022, mais dans sa variante la plus instructive — la correction elle-même a été **partielle**, parce que la liste des endroits où l'information est dupliquée n'existe nulle part. **Le fait est dupliqué dans 3 fichiers ; corriger 2 sur 3 laisse la source d'autorité fausse.**
- **SOLUTION_023 préparée, NON APPLIQUÉE :** un fait d'état = **un seul emplacement** (`ETAT.md`), les autres y renvoient par lien au lieu de le recopier. `CLAUDE.md:304` ne nommerait plus aucune branche. **EN ATTENTE DE GO.**

## ERR-024 — Le proxy d'egress interdit toute vérification externe (récurrent, 2 projets) (2026-09-14)
- **Ce qui s'est passé :** trois blocages distincts, même mur.
  1. `https://caelumpartners.agency/` → `curl: (56) CONNECT tunnel failed, response 403`, HTTP **000**. **La version en production n'est pas comparable au dernier commit depuis une session d'agent.**
  2. Registres de brevets (Espacenet, Patentscope, USPTO, DPMA, EUIPO) → HTTP **000** (consigné dans `codex/A-DECIDER.md` de Caelum, 2026-09-14). Le rôle SCANNER ne peut pas démarrer.
  3. Suppression d'une ref GitHub → HTTP **403** du proxy (consigné dans `📋 JOURNAL.md`, snapshot 2026-09-11 22h03).
- **Sévérité : CRITIQUE par escalade** (3 occurrences, 2 projets, aucune mesure préventive).
- **Cause racine :** l'environnement d'exécution est **cloisonné en sortie par conception**. Ce n'est pas une panne : c'est une propriété permanente. Toute tâche dont le livrable est une **observation du monde extérieur** (site en ligne, registre public, DNS) est structurellement inexécutable ici, quel que soit l'agent.
- **Solution existante liée : PARTIELLE et mal cadrée.** Caelum a consigné le cas des brevets comme une ligne A-DECIDER « accès / outillage » — c'est-à-dire comme un **problème d'accès à obtenir**, pas comme une **contrainte permanente de l'environnement**. **Pourquoi la récurrence :** tant que c'est décrit comme un accès manquant, chaque nouvelle tâche de vérification externe est planifiée comme si elle était faisable, et échoue.
- **SOLUTION_024 préparée, NON APPLIQUÉE :** inscrire la contrainte dans `CLAUDE.md` (« aucune vérification hors dépôt/Drive n'est exécutable depuis une session d'agent ») et router ces tâches vers un canal qui sort (navigateur de Chaima, ou un job CI qui a le réseau). **EN ATTENTE DE GO.**

## ERR-025 — Identité commerciale fabriquée dans un `.env.example`, sur un dépôt public (2026-09-14)
- **Ce qui s'est passé :** le commit `0549fe32` (branche `claude/b2b-outreach-system-7ht0n9`, **non mergée**, publiée) pose comme **valeurs par défaut** d'un outil de prospection : `AGENCY_SIRET="123 456 789 00012"`, `AGENCY_YEARS_EXPERIENCE=10`, `AGENCY_PHONE="+33 1 23 45 67 89"`, `AGENCY_EMAIL="contact@competeiq.io"`. Ces variables alimentent le **pied des e-mails envoyés aux prospects**. Le fichier avertit lui-même : « ces valeurs sont des allégations commerciales […] doivent être EXACTES ».
- **Sévérité : IMPORTANT** (non mergée, donc non exécutée — mais publique et prête à l'emploi).
- **Cause racine :** un gabarit rempli de valeurs **plausibles** au lieu de valeurs **vides**. Un placeholder vide échoue bruyamment ; un faux SIRET bien formé part en production sans un mot.
- **Solution existante liée :** même famille qu'ERR-006 (« nos propres textes doivent respecter nos propres garde-fous ») et que le §13 sur les affirmations « sur nous ». **Pourquoi la récurrence :** le §13 vise ce que les agents **écrivent dans un rapport**, jamais ce qu'ils posent comme **défaut de configuration**.
- **Détection :** `git grep -nE '(SIRET|TVA|PHONE|YEARS)[A-Z_]*=\"[^\"]+\"' -- '*.env.example'`.
- **SOLUTION_025 préparée, NON APPLIQUÉE :** vider ces 6 valeurs par défaut sur la branche concernée et faire échouer l'outil si elles sont absentes, plutôt que de partir avec un faux. **EN ATTENTE DE GO.**
## ERR-026 — Deux sessions ont écrit le même numéro d'erreur le même jour (2026-09-14)
- **Ce qui s'est passé :** deux sessions ont consigné en parallèle dans ce fichier. Chacune a lu « le dernier est ERR-015 » et a écrit son propre **ERR-016**, puis son propre **ERR-017** — contenus entièrement différents. Idem pour les méta-leçons **9, 10 et 11**. `git merge-tree` a confirmé un conflit réel avant toute fusion. Détecté **avant** impact, pendant la vérification d'état d'une troisième demande.
- **Sévérité : IMPORTANT** — §9 angle Humain/Exécution. Aucune perte de donnée, mais la branche était non fusionnable et deux erreurs distinctes portaient le même identifiant dans les citations croisées.
- **Cause racine :** le numéro est attribué **séquentiellement, à la main, au moment de l'écriture**, sans réservation préalable. C'est un compteur partagé sans verrou. Tant que deux sessions peuvent écrire, la collision n'est pas un accident : c'est le comportement attendu du mécanisme.
- **Solution existante liée : AUCUNE pour la numérotation.** ERR-011 traite du `main` périmé (état du dépôt), pas d'un identifiant attribué en double. Le registre Caelum évite le problème autrement : son `🔴 ERREURS.md` est **généré** depuis `.claude/BASE-ERREURS.md`, une source unique — mais la collision de numéro y reste possible à l'écriture de la fiche.
- **Détection :** `git fetch origin && git merge-tree $(git merge-base HEAD origin/main) HEAD origin/main` avant tout commit sur ce fichier. Ou, moins cher : `git show origin/main:"🔴 ERREURS.md" | grep -c "^## ERR-"` juste avant d'écrire.
- **Correctif (2026-09-14, puis REFAIT le 2026-09-19 — voir ERR-029) :** mes sept entrées renumérotées **ERR-020 → ERR-026**, méta-leçons **13 → 16**, merge en union avec `main` (aucune entrée de l'autre session touchée). **Prévention proposée, NON APPLIQUÉE :** faire du numéro une donnée dérivée — un identifiant horodaté (`ERR-20260914-2147`) ne peut pas entrer en collision, ou une génération du registre depuis des fiches séparées, comme côté Caelum. **EN ATTENTE DE GO.**

## ERR-027 — Des marqueurs de conflit git ont été commités ET poussés (2026-09-19)
- **Ce qui s'est passé :** `codex/A-DECIDER.md` et `codex/EVOLUTION.md` ont été poussés sur la branche en portant `<<<<<<< Updated upstream` / `>>>>>>> Stashed changes`. Deux registres de gouvernance, illisibles en l'état, **publiés sur un dépôt public**.
- **Sévérité : IMPORTANT** — §9 angles Technique et Réputation. Aucune donnée perdue (le conflit était en union, les deux versions présentes), mais les deux fichiers que le protocole désigne comme « les seuls à ouvrir » (§6) étaient cassés.
- **Cause racine :** un `git stash pop` partiel a laissé les deux fichiers en état de conflit, puis **`git add -A` a tout avalé sans regarder**. `git add -A` ne distingue pas un fichier résolu d'un fichier en conflit : il ajoute ce qu'il trouve. Aucun garde-fou entre le conflit et le push.
- **Détection :** **signalée par l'agent `avocat`**, hors de son mandat, pendant le Parcours 2. Ni moi, ni `git status` (qui affichait un arbre propre après l'`add`), ni la CI ne l'ont vue. **Le contrôle qui a marché n'était pas un contrôle — c'était un agent qui lisait le fichier pour autre chose.**
- **Correctif (APPLIQUÉ 2026-09-19) :** conflits résolus **en union**, les deux entrées conservées, aucune de la session concurrente touchée. Vérifié : `git grep '^<<<<<<< '` ne renvoie plus rien.
- **Prévention proposée, NON APPLIQUÉE :** refuser le commit si `git grep -l '^<<<<<<< '` renvoie quoi que ce soit — un hook `pre-commit`, ou une étape du gate §4. Trois lignes, coût nul. **EN ATTENTE DE GO.**

## ERR-028 — Le registre d'erreurs annonce « APPLIQUÉ » un correctif qui vit sur une branche non fusionnée (2026-09-19)
- **Ce qui s'est passé :** l'entrée **ERR-016** porte dans son corps « **Correctif : volet structurel APPLIQUÉ le 2026-09-14** (`lib/agents/garde-fou.ts` — `verifierSansSurvente()` appelé au point de sortie…) ». **Ce fichier n'existe ni sur `main`, ni sur aucune branche de travail** — uniquement sur `codex/testeur-adverse-garde-fou-survente`, **jamais fusionnée**. Vérifié par balayage des 33 branches. Sur le code qui tourne, `verifierSansSurvente` n'est appelé nulle part.
- **Sévérité : CRITIQUE** — §9 angles Réputation et Légal. Les trois fuites sont **toujours actives** : `lib/agents/hermes.ts:32` et `lib/agents/pacte.ts:74` (« hébergement **sécurisé** inclus »), `lib/agents/hermes.ts:75` (« **à partir de** {prix} » alors que PACTE annonce un forfait, et « pensé pour **convertir** »). Le titre de l'entrée dit « NON CORRIGÉ » ; son corps dit « APPLIQUÉ ». **Les deux se contredisent, et c'est le titre qui a raison.**
- **Conséquence réelle, le jour même :** l'agent `arbitre-expert` s'est appuyé sur ce corps pour **écarter le garde-fou G6 du contradicteur** (« pas de numéro d'entreprise tant qu'ERR-016 n'est pas corrigé »). Un arbitrage a donc été rendu sur une prémisse fausse. Rattrapé par le `verificateur-verite` avant toute décision de Chaima — c'est exactement la raison pour laquelle le §8 place cette étape entre l'arbitre et `A-DECIDER.md`.
- **Cause racine :** le registre décrit l'**intention** de correction au moment où elle est écrite, pas son **état de fusion**. Une entrée « APPLIQUÉ » ne dit jamais *sur quelle branche*. Tant qu'un correctif vit hors de `main`, le code qui tourne n'en sait rien — mais le registre, lui, affirme le contraire à tous les lecteurs suivants, humains comme agents.
- **Détection :** `ls lib/agents/garde-fou.ts` → absent. Puis balayage : `for b in $(git ls-remote --heads origin | ...); do git ls-tree -r --name-only FETCH_HEAD | grep garde-fou; done`.
- **Correctif (APPLIQUÉ 2026-09-19) :** note de correction datée ajoutée sous ERR-016, sans réécrire l'entrée d'origine (écrite par une session concurrente). **Prévention proposée, NON APPLIQUÉE :** tout « APPLIQUÉ » dans le registre porte le **SHA du commit sur `main`** qui le prouve — sinon le mot autorisé est « **APPLIQUÉ SUR BRANCHE, NON FUSIONNÉ** ». **EN ATTENTE DE GO.**


## ERR-029 — Sept entrées du registre d'erreurs ont disparu dans un merge, en laissant leurs références orphelines (2026-09-19)
- **Ce qui s'est passé :** `ERR-020` à `ERR-026` — consignées le 2026-09-14 (commit `68c64d6a`, ancêtre de la branche courante) — **étaient absentes du fichier**. Vérification : `grep -c '^## ERR-'` = **21** sur la branche, **19** sur `origin/main`, alors que la branche est censée porter `main` + 9 entrées. Pendant ce temps **trois fichiers citaient ces entrées disparues** : `CLAUDE.md:304` (« ERR-022 »), `codex/A-DECIDER.md` (« voir ERR-020 ») et `.claude/agents/controleur-d-application.md` (« ERR-026 »). Les méta-leçons 13 à 16 avaient disparu avec elles.
- **Sévérité : CRITIQUE** — §9 angles Humain/Exécution et Stratégique. Un registre d'erreurs amputé en silence est pire qu'un registre vide : il **affirme** que rien d'autre n'a été constaté.
- **Cause racine :** troisième manifestation d'**ERR-022** (« un merge ne met pas à jour les registres »), mais dans sa forme destructrice. Lors du merge `cda248e6` puis de la résolution en union d'ERR-027, la version de `main` — qui ignorait ces sept entrées — a écrasé la mienne sur cette portion du fichier. `git status` était propre, la CI verte, et **aucun contrôle du protocole ne compare le nombre d'entrées avant et après un merge**. Une fusion en union protège contre le conflit, pas contre la disparition silencieuse.
- **Détection (à retenir) :** `git show origin/main:'🔴 ERREURS.md' | grep -c '^## ERR-'` comparé à la même commande sur `HEAD` — un écart négatif ou nul après un commit qui *ajoute* une entrée est une perte. Et : `git grep -oE 'ERR-[0-9]{3}' | sort -u` recoupé avec les titres réellement présents détecte toute référence orpheline.
- **Correctif (APPLIQUÉ le 2026-09-19, commit de ce jour) :** les sept entrées restaurées depuis `68c64d6a` et renumérotées **ERR-020 → ERR-026** — numérotation qui rend justes, sans les toucher, les trois références existantes. Méta-leçons 13 à 16 restaurées. Aucune entrée d'une autre session modifiée (§10).
- **Prévention proposée, NON APPLIQUÉE :** ajouter au rituel §5 le recoupement « références orphelines » ci-dessus, et au gate §4 un contrôle qui refuse un commit faisant **baisser** le nombre d'entrées d'un registre. **EN ATTENTE DE GO.**

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
7. **Un résumé n'est pas une source ; un périmètre filtré n'est pas un audit** — recouper avec l'artefact d'origine, annoncer le périmètre, vérifier sur le fichier réel (ERR-012, ERR-013, ERR-014).
13. **Un merge est le dernier événement d'une session, donc le premier à ne pas être consigné** — la fraîcheur d'un registre ne peut pas reposer sur la mémoire de celui qui part (ERR-022, ERR-023 ; cf. Caelum E-23).
14. **Le gate ne voit que ce qu'on lui a appris à voir** — `lint/tsc/test/build` ne dit rien des dépendances ni des PR ouvertes ; un angle sans organe de détection est un angle mort permanent, pas un oubli (ERR-020, ERR-021).
15. **Une contrainte permanente décrite comme un accès manquant se reproduit indéfiniment** — le proxy d'egress ne s'obtiendra pas ; les tâches de vérification externe doivent être routées ailleurs (ERR-024).
16. **Un compteur partagé sans verrou finit par compter deux fois** — quand plusieurs sessions écrivent dans le même registre, l'identifiant doit être dérivé (horodaté, généré), jamais choisi de mémoire (ERR-026).
17. **`git add -A` ne regarde pas ce qu'il ajoute** — après tout `stash pop` ou tout merge, vérifier `git grep '^<<<<<<< '` AVANT de committer ; un arbre « propre » au sens de `git status` peut contenir des marqueurs de conflit (ERR-027).
18. **« APPLIQUÉ » sans SHA sur `main` est une intention, pas un fait** — un correctif qui vit sur une branche non fusionnée est absent du code qui tourne, mais présent dans le registre que tout le monde croit (ERR-028).
19. **Une fusion en union protège du conflit, pas de la disparition** — après tout merge sur un registre, recompter les entrées et traquer les références orphelines ; un fichier qui a silencieusement rétréci passe `git status`, la CI et la relecture (ERR-029).
