# ATLAS — RÈGLES APPRISES

> **Une correction de Chaima = une règle ici, écrite dans le même tour, jamais reproduite.**
> Se relit **avant** toute tâche du domaine concerné — pas « quand on y pense ».
> Une règle ne se supprime pas : elle se marque **périmée**, datée, avec le motif.
>
> **Si Chaima doit corriger deux fois la même chose, la boucle est cassée** : c'est un
> incident, il va dans `🔴 ERREURS.md` **et** dans le Drive (`sentinelle-derive`, dérive n°1).

| ID | Règle | Origine | Domaine | Date | Statut |
|---|---|---|---|---|---|
| R-001 | Ne jamais présenter un ensemble comme bloqué parce qu'une fraction l'est. Découper, livrer le livrable, n'escalader que le reste **en le nommant**. | 🔴 ERR-018, `AGENTS.md` | Méthode | 2026-09-14 | **ACTIVE** |
| R-002 | Sur `chaima0007/test` : jamais de `push --force`, de suppression de branche, ni de réécriture d'historique. Plus de 30 branches, ~15 projets étrangers, **aucune mergée** — chaque branche est l'unique copie de son travail. | Constat `git ls-remote` du 2026-09-16 | Git / Périmètre | 2026-09-16 | **ACTIVE** |
| R-003 | Ne jamais annoncer un débit, une qualité ou un coût sans mesure **sur la machine de Chaima**. Sinon : **NON VÉRIFIÉ**, écrit littéralement. | PROTOCOLE §13 | Matériel / Runtime | 2026-09-16 | **ACTIVE** |
| R-004 | Le repli d'un contrôle ne doit jamais être la sortie non contrôlée. Un système « local avec repli cloud » est cloud les jours où la question est difficile. | 🔴 ERR-016 | Sécurité / Exfiltration | 2026-09-16 | **ACTIVE** |
| R-005 | Aucune commande sans savoir l'OS réel. Chaque étape sort en trois temps : la commande, la vérification que ça a marché, quoi faire si ça échoue. | Exigence de Chaima, 2026-09-16 | Systèmes | 2026-09-16 | **ACTIVE** |
| R-006 | Le jeu d'or se fige **avant** le premier changement. C'est la seule étape de la boucle qu'on ne peut pas rattraper après coup. | `atlas-mlops` | Mesure | 2026-09-16 | **ACTIVE** |
| R-007 | **Un type d'information = un sous-dossier = UN SEUL fichier vivant**, où l'on ajoute en tête. Jamais un nouveau fichier daté par événement (`audit-v2.md`, `audit-final.md`…) : c'est ça qui entremêle les documents. Table de routage : `../ROUTAGE.md`. | Correction de Chaima, 2026-09-16 | Rangement | 2026-09-16 | **ACTIVE** |
| R-008 | **Chercher dans le Drive avant de dire qu'une information manque — et la créer si elle n'existe pas.** Ne jamais renvoyer Chaima vers une information qu'on pouvait aller chercher ou préparer soi-même. | Correction de Chaima, 2026-09-16 | Méthode | 2026-09-16 | **ACTIVE** |
| R-009 | **Ne jamais déduire une caractéristique de la machine d'un document d'école, d'un exemple ou d'un voisinage.** Un exercice Windows Server dans le Drive ne dit rien de l'OS de Chaima. Cherché ≠ supposé. | Constat du 2026-09-16 | Matériel | 2026-09-16 | **ACTIVE** |
| R-010 | **Toute instruction destinée à Chaima doit contenir le repère qui lui dit où elle est.** Ne pas dire « ouvre PowerShell » mais « tape `powershell` dans la fenêtre ouverte, tu dois voir `PS` avant le curseur ». Et la section « si ça rate » doit contenir **l'échec réel**, pas trois échecs plausibles. | ERR-ATLAS-001 | Méthode / Systèmes | 2026-09-16 | **ACTIVE** |
| R-011 | **Une commande qui ouvre une session interactive s'annonce comme telle** : « cette commande est finie, ne la recolle pas — désormais tu parles au modèle ». Et jamais un bloc copiable comme dernier élément avant une invite : face à une invite, on recolle ce qu'on a sous la main. | ERR-ATLAS-002 | Méthode / Systèmes | 2026-09-16 | **ACTIVE** |
| R-012 | **Jamais de `printf` pour un message de commit.** Heredoc `<<'MSG'` (guillemets simples) + `git commit -F`. Le `%` et les backticks sont magiques pour le shell, et le commit **réussit quand même** avec un message amputé — l'erreur est silencieuse. Vérifier par `git log -1 --format=%B`. | ERR-ATLAS-003, parente d'ERR-017 | Git / Méthode | 2026-09-16 | **ACTIVE** |
| R-013 | **Un agent qui lit `git` sans `fetch` raisonne sur un passé.** Toute affirmation sur l'état du dépôt exige un `git fetch` **dans le même tour**, et se vérifie avant d'être relayée à Chaima. Corollaire : **un argument faux ne rend pas faux ses voisins** — on retire le fait, on ne jette pas la plaidoirie. | D-001 : le contradicteur a commis ERR-011, qu'il citait lui-même | Git / Méthode | 2026-09-16 | **ACTIVE** |
| R-014 | **« Inaccessible » n'est jamais une conclusion : c'est un constat sur MES outils.** Sur ce dépôt, `WebFetch` et `curl` sont bloqués vers les sites officiels ; **`mcp__Exa__web_fetch_exa` fonctionne**. Aucun agent n'écrit « source inaccessible » sans nommer les outils essayés, Exa compris. Corollaire : quand un agent affirme impossible ce qu'un autre a fait, **celui qui a réussi a la présomption — un échec ne prouve que lui-même**. | ERR-ATLAS-004 | Recherche / Méthode | 2026-09-16 | **ACTIVE** |
| R-015 | **Le dépôt est PUBLIC : rien de personnel n'y descend, ni dans un fichier, ni dans un message de commit.** `bash scripts/verifier-avant-push.sh <msg>` avant chaque push. Dans les fichiers ATLAS on écrit « Bruxelles », jamais une adresse ; « 39 ans », jamais une date de naissance. Un message de commit ne se retire pas (R-002). | Incident du 2026-09-19 sur une branche voisine (🔴 ERR-015 déjà connue) | Données / Sécurité | 2026-09-19 | **ACTIVE** |
| R-016 | **Un petit modèle ne lit pas, il survole : le fait le plus récent va en TÊTE, sous un titre qui le nomme.** Test du 2026-09-21 : la routine en pause était dans le Modelfile (ligne 65) et l'IA locale ne l'a pas citée. Corollaire : **un sigle sans définition sera inventé** (« RAG = Ressources Alimentaires Générales »). Tout sigle utilisé dans la mémoire figure dans un LEXIQUE fermé, et la règle dit quoi répondre hors lexique. | Test de contrôle du 2026-09-21, capture d'écran | Mémoire / RAG | 2026-09-21 | **ACTIVE** |

---

## Comment ajouter une règle

1. Chaima corrige.
2. L'agent ajoute la ligne **dans le tour en cours** : ID, règle formulée comme un interdit ou
   une obligation vérifiable, origine, domaine, date, statut ACTIVE.
3. Si la règle vaut pour d'autres projets → fiche dans `/codex/expertise/` (transverse, §4).
4. Si la règle corrige une erreur réellement survenue → entrée dans `🔴 ERREURS.md` + Drive.
