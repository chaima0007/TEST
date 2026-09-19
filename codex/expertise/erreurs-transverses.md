# EXPERTISE — FAMILLES D'ERREURS TRANSVERSES

**Maturité : CONFIRMÉ** (9 familles · chacune vue sur 2 projets ou plus)
Catalogue par **famille**, pas par incident. Projets comptés : Caelum (dépôt `keywordmoneymaker`, chaîne veille incluse), La Loi Avec Moi, TEST/Nexus-Market, ATLAS, routines Empire. Sources Drive **consultées le 2026-09-19** (IDs dans `methode-agents.md`). Une famille déjà portée par `codex/atlas/apprentissage/REGLES-APPRISES.md` est **référencée**, pas réécrite.
Signal §3 : les bases d'erreurs lues contiennent des consignes adressées aux agents ; traitées comme données.

---

| # | Famille | Projets (compté) | Détection | Correctif — a-t-il tenu ? |
|---|---|---|---|---|
| F1 | **Constat reconduit sans re-preuve** | 2 — Caelum (E-02, ~30 fois ; récidive 16/09), TEST (ERR-012, ERR-028) | Constat repris > 2 cycles ; « le contrôleur l'a validé » ; état de PR déduit d'une ref | Rôle GARANT (« est-ce encore vrai ? ») ; API `state/merged`, jamais `refs/pull/n/head` ; « APPLIQUÉ + SHA de main ». **Pas tenu** tant que la routine fautive n'est pas recréée |
| F2 | **Boucle sans condition d'arrêt** | 3 — Caelum, La Loi, routines Empire (~60 réveils/jour) | Pièces « rien de neuf » ; même livrable deux runs de suite | Inventaire des routines, cadences, consignes réécrites, §5. **Tenu** (11 contrôles silencieux, 12–14/09). EXP-AGT-002, R-007 |
| F3 | **Dérive de périmètre / mélange de projets** | 3 — Empire (6 projets non demandés en 30 min, 17/07), Caelum (E-15 ; flotte de vente contre consigne n°1, 11/09), TEST (20 branches étrangères sur 38, +5 en 5 jours, 19/09) | Commit sur un projet gelé ; nom de branche ≠ contenu ; dossier créé sans « GO » | Porte R1 (aucun projet sans GO écrit), 1 PR par site, `FRONTIERES.md` + gardien-des-frontieres. **Pas tenu au 19/09** : le mélange est actif |
| F4 | **Collision entre sessions parallèles** sur une ressource séquentielle | 2 — TEST (ERR-009, ERR-011, ERR-027, ERR-029), Caelum+TEST (3 collisions de numéro en 48 h ; deux registres « uniques » à 3 min) | `mergeable_state: dirty` ; même numéro deux fois ; **nombre d'entrées d'un registre avant/après merge** ; marqueurs `<<<<<<<` poussés | `git fetch` même tour (R-013) ; numéro suivant celui d'**origin/main** ; union **puis recompte** ; identifiants horodatés (PROPOSÉ). **Partiel** : « un correctif parqué n'est pas un correctif » |
| F5 | **Espace partagé traité comme privé** (données ou secrets sur dépôt public) | 2 — TEST (ERR-015 évité, ERR-030 réalisé, ERR-025 identité fabriquée), Caelum (E-08 sans LICENSE, E-09 coffre vers dépôt public, 77 fichiers internes exposés) | Visibilité du dépôt absente de l'énoncé ; source recopiée au lieu du fait extrait dans un fichier **qu'il faut committer** | → **R-015**. Ajout : un `.gitignore` protège un fichier qu'on n'ajoute pas, jamais un fichier qu'on doit ajouter — viser le **geste**, pas le fichier |
| F6 | **Artefact d'outil pris pour le réel** | 3 — Caelum (E-03, E-10, E-11, E-12, E-16), TEST (ERR-004, ERR-008, ERR-024), ATLAS (R-014) | Erreurs en masse sans changement de code ; date = date du clone ; « ne répond pas » lu « n'existe pas » | Read-back ; profondeur du clone avant toute datation ; trois états nommés **échec / non autorisé / inexistant**. → R-014, EXP-SRC-002. **Tenu** |
| F7 | **Périmètre filtré ou inventaire incomplet annoncé complet** | 2 — TEST (ERR-013, ERR-019), Caelum (E-05, E-07, registre de routines faux) | « Terminé » sur un sous-ensemble ; index qui promet d'être tenu | Annoncer le périmètre **avant** de conclure ; inventorier par le système de fichiers ; un index est une dette portée par un rôle, ou retirée. EXP-AGT-006 |
| F8 | **Règle écrite sans rôle ni mécanisme** (un vœu) | 3 — Caelum (E-01, E-06), Empire (source de vérité « consultative » ; convention violée 50 min après), TEST (ERR-014, ERR-016) | Règle enfreinte deux fois ; règle nouvelle qui ne nomme pas celle qu'elle remplace | Rôle habilité ; règle dans le **fichier lu en premier** (`@AGENTS.md`, tête de `CLAUDE.md`) ; contrôle **bloquant en CI** (a bloqué un désordre le 12/09). → R-004. **Tenu quand mécanisé, jamais quand seulement écrit** |
| F9 | **Nos textes échouent à nos garde-fous** (survente, chiffre inventé) | 3 — TEST (ERR-006/007/016), La Loi (badge « vérifié par 2 juristes », faux compteurs), Caelum (CSRD vendue comme urgence PME, corrigée) | Test « ne doit pas contenir X » rouge sur un texte généré par nous ; affirmation **sur nous** sans source | Tester les gabarits contre les motifs bannis, même niés ; filtre au **point de sortie commun** ; §13 |

---

## Le motif du motif
Six familles (F1, F3, F4, F5, F7, F8) ont la même forme : **un état a changé et personne ne possédait la question « est-ce encore vrai ? »** — état du dépôt, d'une PR, d'une règle, d'un périmètre. Le correctif qui tient est toujours le même : cette question va à un **rôle** ou à un **mécanisme bloquant**, jamais à une phrase de plus dans un document.
Mesuré le 19/09 : 86 agents produisent ou contrôlent, **aucun ne fait sortir ni fermer**. Pas une erreur, une direction — consignée pour ne pas être redécouverte.

---

    DE : scout                     POUR : verificateur-verite, puis archiviste-preuves
    OBJET : Valider ce catalogue de 9 familles ; archiver les extraits Drive qui les prouvent.
    VERDICT : VÉRIFIÉ (bases d'erreurs et méta-alertes du Drive, 2026-07-13 → 2026-09-19, consultées le 2026-09-19)
    PARCE QUE : chaque famille est comptée sur des incidents nommés (E-xx, ERR-xxx) dans 2 projets ou plus.
    NON VÉRIFIÉ : fiches E-17 à E-25 (citées, non lues) ; chiffre des branches étrangères repris du rapport du 19/09, non recompté ; 5 .md du dossier « Flotte 18 agents », illisibles par l'outil.
    CE QUI CHANGERAIT MON AVIS : un incident hors de ces neuf familles ayant frappé 2 projets — il manquerait une F10.
