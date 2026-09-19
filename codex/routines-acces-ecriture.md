# Accès en écriture des Routines programmées — état, mesures, recette

> Dernière vérification : **2026-09-19 13:40 UTC**. Rien ici n'est écrit de mémoire.
> Entrée liée : `🔴 ERREURS.md` → **ERR-020** (NON CLOSE).

---

## 1. Le symptôme

Les sessions déclenchées par une Routine programmée peuvent **lire** les dépôts mais **pas
pousser**. Chaque `git push` échoue :

```
not in this session's authorized repository set   (HTTP 403)
```

Conséquence concrète : des correctifs restent en attente dans la session programmée et meurent
avec son conteneur. Ce n'est pas un problème de droits GitHub — c'est un problème de
**rattachement du dépôt à la session**.

## 2. Ce qui est VÉRIFIÉ

| Fait | Preuve | Date |
|---|---|---|
| Le compte a bien les droits d'écriture sur les deux dépôts | pushs réels : `bea133e` (keywordmoneymaker), `cc22b83` / `09e2ab1` (test) | 2026-09-14 |
| Une session **manuelle** avec le dépôt attaché à sa création pousse sans erreur | cette session même | en continu |
| Les deux dépôts sont listés et sélectionnables dans l'environnement « Par défaut » | vérifié par Chaima dans l'interface | 2026-09-16 |

## 3. Ce qui est ÉLIMINÉ PAR LA MESURE — ne pas le retenter

Une Routine créée par l'outil `create_trigger` **ne peut pas porter de connecteurs**, donc pas
d'accès dépôt, donc pas de push. Trois mesures indépendantes :

| Tentative | Résultat | Date |
|---|---|---|
| `create_trigger` avec `environment_id: env_019H6JJv6xsE8pEoWXiTWdba` explicite | session lancée, `mcp_connections: []`, **aucune branche poussée** (durée 70 s) | 2026-09-16 |
| `create_trigger` sans `environment_id` (héritage pur d'une session qui tourne pourtant en « Par défaut » avec les deux dépôts et tous les connecteurs) | `mcp_connections: []` — **identique** | 2026-09-16 |
| `create_trigger` avec le paramètre `connectors: ["github"]` | refus explicite de l'API : *« the connectors parameter is not available for this organization »* | **2026-09-19** |

Deux correctifs tentés et **infirmés** :

- ajouter un préambule `add_repo` en tête du prompt de la Routine → deux exécutions (2 min 46 s
  et 2 min 42 s), **aucune branche poussée**. Préambule retiré depuis : il affirmait une chose
  fausse.
- compter sur l'héritage d'environnement depuis une session qui, elle, a les accès → voir
  tableau ci-dessus.

**Conclusion outillage :** aucune Routine créée depuis un agent ne peut pousser. La limite est
côté organisation, pas côté prompt ni côté environnement.

## 4. La seule configuration jamais essayée

Une Routine créée **depuis l'interface Routines de claude.ai** — c'est le seul chemin qui
attache réellement les connecteurs à la Routine. C'est une action d'interface sur le compte de
Chaima : **aucun agent ne peut la faire** (§10).

### Recette — test minimal, ~5 minutes

1. **claude.ai → Routines → Nouvelle Routine.**
2. **Environnement : « Par défaut »** (celui où les deux dépôts sont sélectionnables).
   Vérifier que `chaima0007/TEST` **et** `chaima0007/keywordmoneymaker` sont bien cochés.
3. **Planification :** une seule fois, dans ~10 minutes.
4. **Prompt — à coller tel quel :**

   > Crée la branche `codex/test-ecriture-routine-ui` depuis `main` dans `chaima0007/TEST`,
   > ajoute une ligne horodatée à la fin de `📋 JOURNAL.md`, commit, puis
   > `git push -u origin codex/test-ecriture-routine-ui`.
   > Si le push échoue, recopie le message d'erreur **mot pour mot** et arrête-toi là.
   > Ne touche à rien d'autre. Ne crée aucune PR.

5. **Lecture du résultat — binaire, pas d'interprétation :**
   - la branche `codex/test-ecriture-routine-ui` apparaît sur GitHub → **l'interface règle le
     problème.** Recréer depuis l'interface les Routines qui doivent pousser (voir §5),
     désactiver les anciennes sans les supprimer.
   - pas de branche, et le message `not in this session's authorized repository set` est
     recopié → **le problème n'est pas le mode de création.** Il est côté droits de
     l'organisation, et c'est un ticket support, pas un réglage.

### Ce qui changerait ce verdict

Un `connectors` rendu disponible à l'organisation : `create_trigger` redeviendrait suffisant et
toute cette recette tomberait. À re-tester d'un appel si les réglages d'organisation changent.

## 5. Routines concernées le jour où le test passe

À recréer depuis l'interface, **avec le prompt et la planification existants repris à
l'identique** (les prompts ne sont pas exposés par l'API : les recopier depuis l'interface) :

| Routine | Planification (UTC) | Pourquoi elle a besoin de pousser |
|---|---|---|
| `Caelum — Chaîne veille brevets & capitaux` | `35 9 * * *` | c'est la chaîne de veille CODEX qui passe sur les deux dépôts ; c'est elle qui portait le patch bloqué |
| `Caelum — BOUCLE de production` | `22 */8 * * *` | même cause probable — à corriger dans la foulée, pour ne pas redécouvrir le même 403 dans trois semaines |

**Désactiver les anciennes, ne pas les supprimer** : une Routine supprimée emporte son prompt,
et les prompts ne sont pas récupérables par l'API.

---

    DE : session Claude Code (TEST)          POUR : CHAIMA
    OBJET : créer une Routine de test depuis l'interface Routines de claude.ai, environnement
            « Par défaut », avec le prompt du §4 — et lire le résultat comme un binaire.
    VERDICT : NON VÉRIFIÉ — la configuration « Routine créée depuis l'interface » n'a jamais
            été essayée ; toutes les autres sont éliminées par la mesure.
    PARCE QUE : `create_trigger` refuse le paramètre `connectors` au niveau de l'organisation
            (mesuré le 2026-09-19), et une Routine sans connecteurs n'a aucun dépôt attaché.
    NON VÉRIFIÉ : si l'interface attache réellement les connecteurs à la Routine, ou seulement
            à la session qui la crée.
    CE QUI CHANGERAIT MON AVIS : la branche `codex/test-ecriture-routine-ui` apparaissant sur
            GitHub après le test — ou `connectors` devenant disponible à l'organisation.
