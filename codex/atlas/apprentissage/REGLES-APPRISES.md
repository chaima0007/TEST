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

---

## Comment ajouter une règle

1. Chaima corrige.
2. L'agent ajoute la ligne **dans le tour en cours** : ID, règle formulée comme un interdit ou
   une obligation vérifiable, origine, domaine, date, statut ACTIVE.
3. Si la règle vaut pour d'autres projets → fiche dans `/codex/expertise/` (transverse, §4).
4. Si la règle corrige une erreur réellement survenue → entrée dans `🔴 ERREURS.md` + Drive.
