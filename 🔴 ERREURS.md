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

## ERR-019 — Branche créée sur un `main` périmé : récidive d'ERR-011, par la session qui ne l'avait pas lue (2026-09-14, corrigée)
- **Ce qui s'est passé :** chargé d'une mesure d'accès en écriture, l'agent a enchaîné `git status` puis `git checkout -b codex/mesure-option3` **sans un seul `git fetch`**. La branche est partie de `9cc15c2f`, l'état local figé à l'ouverture du conteneur, alors que `origin/main` était déjà à `75ebe4af`. Résultat mesuré : la branche ignorait **12 commits** et, si elle avait été mergée, aurait **supprimé 457 lignes** de travail produit par d'autres sessions (ERR-011 à ERR-018, ICP Caelum, protections RGPD, gate ré-exécuté).
- **Cause (CONFIRMÉE par reproduction) :** `git merge-base codex/mesure-option3 origin/main` = `9cc15c2f` ≠ `git rev-parse origin/main` = `75ebe4af`. L'agent a traité l'affichage de `git branch -a` — qui ne liste que les refs **déjà** en cache local — comme un état serveur. Un `-a` sans `fetch` préalable ne prouve rien sur le dépôt distant.
- **Aggravant — la boucle :** l'entrée ERR-011 décrit **exactement** cette erreur, et le motif récurrent n°6 la nomme. L'agent ne les a pas appliquées **parce qu'elles faisaient partie des 12 commits qu'il ne voyait pas**. Un registre d'erreurs ne protège que la session qui a fetché ; l'omission du fetch est donc l'erreur qui **rend toutes les autres leçons invisibles**, pas une erreur parmi d'autres.
- **Second défaut, mineur :** la consigne demandait d'insérer une ligne sous `|---|---|---|---|` ; aucun tableau n'existait dans ce fichier (`grep -c "^|"` = 0, sur `main` comme en local). L'agent a fabriqué l'ancrage manquant plutôt que de s'arrêter. Il l'a signalé — c'était le bon réflexe — mais le fichier porte désormais deux formats (`## ERR-NNN` et un tableau).
- **Détection :** aucune alerte automatique. L'échec a été **rapporté comme un succès** (`RESULTAT : ECRITURE OK`) : le critère vérifié (« le push passe ») était vrai, le critère qui comptait (« la branche est saine ») n'avait pas été regardé. Découvert seulement au `git fetch` de la session suivante, 3 jours plus tard.
- **Correctif (APPLIQUÉ et VÉRIFIÉ 2026-09-14) :** `origin/main` mergé dans `codex/mesure-option3` (merge, pas rebase : préserve `cc22b83`, la preuve de la mesure, et ne réécrit l'historique de personne). Conflit sur ce fichier résolu en **union** — motifs récurrents de `main` conservés, tableau de mesure conservé. Vérification : `git diff codex/mesure-option3...origin/main --shortstat` → **vide**, et `git log codex/mesure-option3..origin/main` → **0 commit**. La branche ne supprime plus rien.
- **Prévention, sous forme de test :** *`git fetch` est la PREMIÈRE commande de toute session qui touchera à git — avant `status`, avant `branch`, avant toute conclusion.* Et avant d'annoncer un succès : `git diff <ma-branche>...origin/main --shortstat` doit être **vide**. Une branche qui supprime des lignes qu'on n'a pas écrites est un échec, même si le push a réussi.

---

### Motifs récurrents (méta-leçons)
1. **Distinguer « environnemental » de « régression »** avant de toucher au code (ERR-004, ERR-008).
2. **Vercel = bruit connu**, pas notre code (ERR-002, ERR-003) — commenter une fois, ne pas répéter.
3. **Les webhooks ne disent pas tout** (merge-conflit, CI post-fix) → le check-in périodique est indispensable (ERR-009).
4. **Nos propres textes doivent respecter nos propres garde-fous** — les tester (ERR-006, ERR-007).
5. **Secrets/config du dépôt ≠ code** : diagnostiquer via « échoue-t-il aussi sur un commit vide/doc ? » (ERR-010).
6. **L'état du dépôt à l'ouverture n'est pas l'état du dépôt maintenant** — re-vérifier côté serveur avant tout commit et avant toute conclusion, surtout quand plusieurs sessions tournent en parallèle (ERR-011).
11. **Découper avant d'escalader** — le §10 liste des actions humaines, pas des sujets contaminants ; livrer la part livrable AVANT de rendre la main, et nommer précisément ce qui reste (ERR-018).
10. **Tout texte qui traverse un shell doit être quoté** — heredoc à délimiteur quoté par défaut ; un backtick non quoté est une substitution de commande, pas un caractère (ERR-017).
9. **Un garde-fou se vérifie sur le chemin qui tourne, pas sur celui qu'on craignait** — placé au mauvais endroit, il rassure sans protéger, et le repli d'un contrôle ne doit jamais être la sortie non contrôlée (ERR-016).
8. **Un agent ne voit que le contexte qu'on lui donne** — une omission dans l'énoncé devient un angle mort dans la décision ; la visibilité du dépôt, le volume et le canal font partie de l'énoncé (ERR-015).
12. **`git fetch` avant tout le reste** — un registre d'erreurs ne protège que la session qui l'a fetché ; sans fetch, les leçons déjà écrites sont invisibles et on les recommet (ERR-019, récidive d'ERR-011).
7. **Un résumé n'est pas une source ; un périmètre filtré n'est pas un audit** — recouper avec l'artefact d'origine, annoncer le périmètre, vérifier sur le fichier réel (ERR-012, ERR-013, ERR-014).
