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
