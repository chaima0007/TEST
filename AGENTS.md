<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

<!-- BEGIN:codex-regle-decoupage -->
# Règle du découpage obligatoire — avant toute escalade vers Chaima

Le §10 de `CLAUDE.md` liste ce qui reste strictement humain. Il ne dit pas qu'une
tâche **touchant** à ces sujets devient humaine **en entier**. C'est pourtant
l'erreur commise le 2026-09-14 (voir `🔴 ERREURS.md`, ERR-018) : un correctif à
deux volets a été présenté comme bloqué parce que **l'un des deux** l'était.

**Avant d'écrire « c'est ta décision », découper :**

1. Lister ce que la tâche exige, point par point.
2. Marquer chaque point : figure-t-il **explicitement** dans la liste du §10 ?
3. **Livrer immédiatement tout ce qui n'y figure pas.**
4. N'escalader que le reste, en le nommant précisément.

**Interdits**

- Présenter un ensemble comme bloqué parce qu'une fraction l'est.
- Escalader sans avoir livré la part livrable.
- Escalader « le correctif » sans dire de quelle partie du correctif il s'agit.

**Test de contrôle, à s'appliquer avant d'envoyer le message**

> Si la phrase d'escalade peut être remplacée par
> « j'ai fait X, il reste Y qui t'appartient », **alors elle devait l'être.**

Une escalade qui ne nomme pas ce qui a déjà été livré est une escalade prématurée.
<!-- END:codex-regle-decoupage -->

<!-- BEGIN:codex-regle-fetch -->
# Règle du `git fetch` d'ouverture — avant toute commande git

Le conteneur d'une session est un **instantané figé à sa création**. `git status`,
`git branch -a`, `git log` et tout fichier du dépôt affichent cet instantané, pas
l'état du serveur. Plusieurs sessions travaillent en parallèle sur ce dépôt : l'écart
se creuse pendant que tu lis. Voir `🔴 ERREURS.md`, ERR-011 puis ERR-019 (récidive).

**`git fetch origin` est la PREMIÈRE commande de toute session qui touchera à git.**
Avant `status`, avant `branch`, avant `checkout -b`, avant toute conclusion sur l'état
du dépôt.

## Les deux tests, non négociables

**1. Avant de créer une branche** — elle part de l'état serveur, jamais du local :

```bash
git fetch origin
git checkout -b <nom> origin/main    # et non : git checkout -b <nom>
```

**2. Avant d'annoncer un succès** — le retard doit être nul :

```bash
git log --oneline <ma-branche>..origin/main | wc -l   # doit afficher 0
```

Non nul = la branche est périmée. Corriger par `git merge origin/main` (jamais
`rebase` ni `push --force` sur une branche que quelqu'un d'autre peut avoir
récupérée), puis re-tester.

## Interdits

- Conclure quoi que ce soit sur l'état du dépôt sans un `fetch` dans la même session.
- Lire `git branch -a` comme un état serveur : sans `fetch`, il ne liste que le cache local.
- Annoncer « poussé », « OK » ou « terminé » sans avoir vérifié le retard.
- Affirmer une conséquence git (« ça aurait supprimé X ») sans l'avoir **reproduite**.
  Un merge en conflit n'est pas une suppression — le §13 exige de mesurer, pas de conclure.

**Pourquoi cette règle passe avant les autres :** le registre d'erreurs ne protège
que la session qui l'a fetché. Sans fetch, les leçons déjà écrites sont invisibles —
et on les recommet. C'est précisément comme ça qu'ERR-011 a été rejouée le 2026-09-14.
<!-- END:codex-regle-fetch -->
