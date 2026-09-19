# CARTE DU DRIVE — partie Empire uniquement

> **Demande de Chaima (2026-09-19) :** *« notre IA doit lire tout mon Drive pour comprendre et apprendre. »*
> Cette carte est l'**étape 1** : savoir ce qu'il y a, où, en quel volume — pour que les passes de
> lecture suivantes sachent quoi ouvrir. **Relevé du 2026-09-19** par `search_files` (listing complet,
> paginé, `parentId` par dossier). **Aucun contenu lu** sauf 3 index (§4.3). Coffre : titres seuls.
> **Un seul fichier vivant, ajout en tête si on itère** (R-007). Dépôt PUBLIC → zéro donnée
> personnelle ici (R-015) : titres tronqués quand ils en contiennent, dossiers privés non ouverts.

## 0. Chiffres du relevé (comptés, pas estimés)

| Mesure | Valeur |
|---|---|
| Dossiers à la racine de « Mon Drive » | **23** (19 Empire · 4 personnels antérieurs à 2026, non ouverts) |
| Fichiers libres à la racine créés en 2026 | **33** (22 Empire · 11 formation/perso, listés sans titre) |
| Fichiers Empire comptés (tous dossiers, toutes profondeurs) | **906** (dont les 22 fichiers libres de la racine) |
| Le plus gros dossier | `LA LOI AVEC MOI — Base d'infos sourcées` : **372** fichiers, 0 sous-dossier |
| Le 2e | `COMPILATION & SYNOPSIS` : **283** fichiers directs (+ 2 sous-dossiers : 23 + 372 = **678** au total) |
| Période couverte (Empire) | **2026-06-18** (Archive) → **2026-09-19** (ATLAS, Veille, LLAM) |
| Sous-dossiers vides | **28** (22 pays de la bibliothèque brevets + Opportunités académiques + Communication & Marketing + Financement & Capitaux + Technologies exploitables + Lyra/07-13 + Libre/problemes + Feedback/Audits quotidiens) + dossier `Patchou` vide |
| Fichiers antérieurs à 2026 à la racine | **NON VÉRIFIÉ** (non listés, hors périmètre) |

Types rencontrés : Google Docs (très majoritaires), `text/plain` (rapports 09/2026 et fiches LLAM récentes),
`text/markdown`, 4 `text/html` (maquettes), 1 `.pptx` (59 octets = coquille), 1 `.pdf`, 1 `.docx`, 4 `.ics`, 1 `.py`, 1 Sheet.

## 1. Arborescence Empire — un dossier par ligne

Légende **Git** : branche de `chaima0007/test` d'après `CARTE-PROJETS.md` (2026-09-19). « — » = aucune branche connue.

| # | Dossier (ID) | Rôle déduit des titres | Fichiers | Période | Git servi |
|---|---|---|---|---|---|
| 1 | 📕 CODEX — Empire Chaima (protocole maître) `1M3ta4OZ4gYEI3aI3eUDFHo1v-tyVN4pG` | Le protocole qui gouverne tous les projets (v2026-09-06) | 2 | 09-06 | `claude/protocole-codex-empire-wa4gp6` (source) · `CLAUDE.md` de chaque dépôt |
| 2 | 📂 Caelum — Direction, Stratégie & Conformité `1iMF5ndAz_UA8JVbfpRwApBeag1dU-gVp` | Cerveau de l'agence : CLAUDE.md, JOURNAL, ERREURS, stratégie NIS2, PI, veille 09-14, opportunité O-01 ; sous-dossier PRÉSENTATION (pitch, offres, jalons) | 17 + 7 = **24** | 06-27 → 09-14 | `main` (tronc Caelum/Nexus-Market), `claude/charming-galileo-cqhkn1`, `codex/err-019-*`, `codex/testeur-adverse-*`, `codex/mesure-option3` |
| 3 | Caelum — Infrastructure & Web `1WLUPeevFjclRvRqWfIAcsNAMHBkSJjp-` | Domaine, DNS, SSL 525 : guide + runbook + passation | 1 + 2 = **3** | 07-17 | `main` (site caelumpartners.agency) |
| 4 | Caelum — Flotte d'agents & Orchestration `1pr827nvAlkn_0r1Q1v1AAA8EIcemibfl` | Version 07-17 du système d'agents : prompt maître, 18 définitions, Protocole Drive, « Étape 0 » | 0 + 5 = **5** | 07-17 | ancêtre de `.claude/agents/` (21 agents CODEX) |
| 5 | 🗂️ Caelum — Journal d'Audit (Travaux techniques) `1npTlFufVU03luocJIw365Sd3evziZGg_` | Journaux d'audit 07-13/07-17, PROMPT MAÎTRE « loi commune », protocole d'audit de flotte, LISEZ-MOI règles du journal ; contient **Veille & Opportunités** et PRÉSENTATION KMM & CompeteIQ | 9 + 3 (+ Veille) = **12** | 07-13 → 09-19 | Caelum · KeywordMoneyMaker (dépôt séparé) · CompeteIQ `feat/*` |
| 5a | ↳ Veille & Opportunités `16AljpQP62sBoDfTzkfbz6KCwchW0XK1W` | Chaîne veille : brevetabilité (4), bibliothèque brevets (1 + 23 sous-dossiers **vides**), synergies inter-agents (16 : rôles 2→33, base d'erreurs, table 29 vs 38), plans de mise en œuvre (2), 🔒 Coffre (1), 3 sous-dossiers vides | **24** dans 8 + 23 sous-dossiers | 09-11 → 09-19 | `claude/chaima-patent-audit-ytcxq3` · `claude/adoring-albattani-ue4vtz` (dossier DÉPOSANT) · Caelum |
| 6 | 🗂️ COMPILATION & SYNOPSIS — Empire Chaima (créé 14 juillet) `1qXUj9D9r7HSmIMzMcsScz4Ynlv4auP4G` | **La mémoire opérationnelle** : 149 journaux `boucle-caelum` (routine de surveillance site + dépôt), 62 rapports de session Claude Code, 34 pièces numérotées 00→27 (synopsis, protocoles, angles morts), 13 pièces méta-surveillance / MÉTA-ALERTE, 10 `coach`, 12 autres (registres, bases, transverse), 3 build-caelumswarm | **283** directs (07 : 152 · 08 : 31 · 09 : 100) | 07-17 → 09-19 | tous : Caelum/`main`, TEST (`claude/nexus-market-agents-63dlku`, `chore/codex-protocole-structure`), KMM, CompeteIQ |
| 6a | ↳ 🏛️ LA LOI AVEC MOI — Base d'infos sourcées (accumulation, non publiée) `1a9dROkr2k6N-KWqgOQrj17Gy3IsJUX1I` | **368 fiches** « LLAM — <sujet> (sources vérifiées, date) » + 3 ⚙️ FICHE TECHNIQUE interne (journal qualité, anti-doublon) + 1 `boucle-caelum` égaré | **372** (186 Docs + 186 txt) | 07-17 → 09-19 | `claude/swarm-50-agent-architecture-3l6cno` (LLAM, 3 539 commits) · fiches vitrine Caelum (« Le Greffe ») |
| 6b | ↳ 2026-07-17 — Revue Claude Design — copies · critiques² · idées `1kiuanaonZtazVxQvPAmUEV593VoD7aUT` | Audit Claude Design du 17/07 : verdict Ella (non-achat), tableau de bord « Salle de contrôle », 3 maquettes HTML, 99 — copies de sauvegarde (6) | 17 + 6 = **23** | 07-17 | Caelum design (`main`) |
| 7 | 📁 EMPIRE CHAIMA — Archive & Mémoire `1oASVo2oVM-aRlm7RiPe7YMaRMt87UgTP` | Strate 06-18 → 07-13 : ARCHIVE COMPLÈTE, CLAUDE.md MASTER, CANAL v1/v2, vérification quotidienne, audit maturité, protocole commentaires, 3 stubs HTML « LA LOI AVEC TOI » v2-v4 ; 6 sous-dossiers dont **copies** de Caelum (15), LLAM (14), Lyra (3), Feedback (2), PRÉSENTATION Empire (1), **CV Booster (4)** | 9 + 39 = **48** | 06-18 → 09-02 | transverse ; Caelum ; LLAM |
| 7a | ↳ CV Booster — Application CV anti-ATS `1coqchVPn2GQEESujFfj1BeoMIymeBhPN` | CLAUDE.md + JOURNAL + ERREURS + positionnement | **4** | 09-02 | **—** (aucune branche dans `test`) |
| 8 | ATLAS — IA locale (Empire Chaima) `1Ual-L_FKyitVvi71bQph51-gpOQeq4Ao` | 01 fiche machine (à remplir), 02 erreurs & réussites, 03 PROMPT MAÎTRE v2 (09-19) | **3** | 09-16 → 09-19 | `claude/nifty-shannon-u87dv8` (cette branche) |
| 9 | 00 — PROTOCOLE (Agents & Projets) `1TN4TrQHCgqw_bOEk0HnVie5iWp_YcK8Z` | PROTOCOLE_Agents-et-Projets_v1 (07-17) — ancêtre du CODEX | **1** | 07-17 | `claude/protocole-codex-empire-wa4gp6` |
| 10 | La Loi Avec Moi — Audits `11Nia45zmPqtL9Rox38KP05c8Fy_q64Fa` | CLAUDE.md, JOURNAL, ERREURS, protocole Conseil d'experts, 3 lots de mise au standard (24 fiches), backlog de passation ; sous-dossiers Implémentation App Web (1), PRÉSENTATION (4) | 17 + 5 = **22** | 07-13 → 07-17 | `claude/swarm-50-agent-architecture-3l6cno` |
| 11 | CompeteIQ — Audits & Livrables `1m8xPJYUlGG1FRFocRQWXezNw8knDqHk7` | 2 sous-dossiers 07-17 : uplift enterprise (journal), config revue de code CI + PR #2 (journal + inventaire technique) | 0 + 3 = **3** | 07-17 | `feat/kb-seed`, `feat/kb-api-stub`, `feat/infra-security`, `feat/commercial-*`, `claude/competitive-intel-saas-arch-rfh4x3`, `claude/code-review-setup-b8r9pn` |
| 12 | Lyra — Audits & Livrables `1raDydTYvBYw0YbOPSH55Y3tAs9FsGlai` | Prompt optimisé Mistral (3 md, 07-13) ; Produits numériques Droit Citoyen & intégration Claude×Mistral (07-13 : **vide** ; 07-17 : 3 md + `chainage.py`) | 0 + 7 = **7** | 07-13 → 07-17 | `claude/mistral-mnwb5j` (Pont Mistral) — rapprochement PLAUSIBLE, NON VÉRIFIÉ |
| 13 | SOLEA — Audit `1OMXa_Wkht_HWOf5DOzfNKNhjgVQN1ZRQ` | 00_INDEX + sous-dossier 07-17 (évaluation gouvernée, journal) | 1 + 2 = **3** | 07-17 | `claude/foot-site-business-plan-ch0jt0` |
| 14 | LibreEtAccomplis `1G2t4dn_pejyUjoqJqjuR6I0TWikWMGBD` | audit (2 : 07-13, 09-06 installation CODEX), presentation (1), problemes (**vide**) | 0 + 3 = **3** | 07-13 → 09-06 | `claude/libre-accomplis-system-9wvsnf` |
| 15 | retrouvetonsmile — idées produits perso (HORS Caelum) `1qV3s3teAqONZHOwD6kGWr0eerflNuiGw` | Fiches idées + 2 prompts BUILD : App Couples, App Parents-Enfants | **2** | 07-17 | `claude/couples-app-mvp-chaima-fx3dya` · `claude/parents-enfants-mvp-1xwgqu` |
| 16 | Patchou — Projet Dropshipping `1t-jBq9yHNMSC_o12Z0EZvxB2P7yUNwRF` | **Dossier vide** ; ses pièces sont dans COMPILATION (audit & synopsis 07-17, installation CODEX « competeiq-Patchou » 09-06) | **0** | 07-17 | `claude/shopify-app-development-ri1090` — rapprochement PLAUSIBLE, NON VÉRIFIÉ |
| 17 | 📊 Mon Feedback quotidien — Chaima `13FHtDypmDLiJXqAvr91HGVeb_L70_ExF` | **29 feedbacks quotidiens** (07-13 → 09-18, avec un trou 08-11 → 09-10), Journal des exercices, Mon Système complet ; sous-dossiers Évolution (2), Travail & Exercices (1), Audits quotidiens (**vide**) | 31 + 3 = **34** | 07-13 → 09-18 | transverse — matière première d'`atlas/apprentissage/` |
| 18 | 💼 Dossier Pro — Projet & Compétences (La Loi Avec Moi) `187lCBJmvZnyGSXWQOcfX_7bBHMaQJAWn` | Présentation & compétences, LinkedIn, guide futur collaborateur, produit & interface — **matière CV/école, titres non reproduits** | 1 + 8 = **9** | 06-26 | LLAM (vitrine de compétences) |
| 19 | 🏆 Réalisations & Preuves — Dossier école (été 2026) `1yOQtlkKzYb_4rw-FUMJy0xEd0fsw0gsr` | 1 doc « réalisations du jour (preuve pour l'école) » | **1** | 07-17 | transverse |
| 20 | Racine — fichiers libres Empire (22) | Études de marché/prix Caelum & LLAM (06-29), GO-NO-GO 06-29, kit de contenu, TBA flotte, vision (étoile du Nord, Fondation, rêves), 2 `.ics`, `caelum_pitch.pdf`, cahier des charges `.docx`, registre Jeu Linux (09-16), **📇 INDEX Drive (09-11)**, **🗂️ PLAN DE CONSOLIDATION (09-06)**, 1 doc ERREURS d'une candidature (titre tronqué) | **22** | 06-08 → 09-16 | `claude/empire-chaima-linux-game-54cqgy` (Jeu Linux) · Caelum · LLAM |

**Hors périmètre, non ouverts :** 4 dossiers personnels antérieurs à 2026 à la racine (photos, rapport 2021,
sauvegardes Chrome OS) + 11 fichiers libres de formation/personnels (exercices réseau `.docx`, 2 QCM `.html`,
1 guide d'examen) — comptés, jamais listés par titre. Dossiers `1o14U0Wm…` et `1CzwVoRc…` cités par le plan de
consolidation : **absents du relevé** (corbeillés le 09-11 d'après l'INDEX — NON VÉRIFIÉ).

## 2. Documents structurants par dossier (ID = ce que la passe suivante ouvre)

| Dossier | Titre (tronqué si nécessaire) | ID | Date |
|---|---|---|---|
| CODEX | EMPIRE-CHAIMA-protocole-agents-CODEX.md | `1GFKFky8ziXr7YY_Zd-6Kwk_QqOsvrLei_F_hDaLFHqw` | 09-06 |
| CODEX | EMPIRE-CHAIMA-prompt-maitre-claude-code.md | `1GoOOJ4fmQOGrBoZEQ8HkkYpouIFoOUxBGa5vECdpp9I` | 09-06 |
| Caelum Direction | REGISTRE MAÎTRE — Agents Caelum (source unique de vérité) | `1Vy5Uy6DI8t2_I9HX2yhGjcQ9YxRAwnw8pHyGYFo2zOk` | 07-14 |
| Caelum Direction | 🔴 ERREURS — Caelum Partners (à corriger dans l'ordre) | `14FFTdx3VE6lv-1H7Ocs47oTHq9fWt3QVorDkDwQdOg4` | 07-13 |
| Caelum Direction | 📋 JOURNAL — Caelum Partners (toutes sessions) | `12hiPJdyI8zRdN6Cp84fVrdSS3QGwGrTASDwK0zuczQk` | 07-13 |
| Caelum Direction | CLAUDE.md — Instructions Claude Code (Caelum Partners) | `1wr8R7oPr93sg28zeVvvKlhS_cr1HzoH4PeMvOEsD_DE` | 07-13 |
| Caelum Direction | Plan de lancement (voie B / NIS2) | `1d7XfA_N7puLjPfY49E9ZH6BI0cNG4KoLcWELI0ZjE6U` | 07-17 |
| Caelum Direction | Opportunité O-01 Le passeport fournisseur NIS2 (PROPOSÉ) | `1P4mVqSl3sQ3UMN07Zm9YALwaEdUipl0T` | 09-14 |
| Caelum Direction/PRÉSENTATION | 01 Présentation générale · 02 Offres & tarifs · 03 Marketing 90 j · 04 Jalons | `1Pw5KD2VM8HYXCyDzZyBVfn3v_xFSiPDvZajYzOqGtRU` · `1xpSYe9y7qMNTpbtBKekD1ArSA_il-kn1ReMrQRSnkJ0` · `1-RX2fgyXz6w4IdUDL9SL_rSrQyApoIcXJugWqFhGrQE` · `1McRVuJkhvCyNMEWTb1xenu6nrQKogK46MNhmoYqWv24` | 07-13 |
| Caelum Infra | 00 — Runbook & statut SSL 525.md · 01 — Passation complète pour Claude.md | `1M0QSB-rbyjthoiRaWHfqbdn9CnUh81dU` · `1WKBwIqQBS4eLhhTsDGoHP3SxgjALJR3V` | 07-17 |
| Caelum Flotte | 00 Vue d'ensemble · 01 PROMPT MAÎTRE · 02 Définitions des agents · 04 Protocole Drive | `1KhB0-tyEHSK52bR9cpJLf2Z2TgIrBYzq` · `1LC_xQyFoOeZpBGooR50E9vo0j_5PCQXI` · `1zHjWtY7e67AoFRFwL9w5UJGEYQhamrVO` · `1DLfvcTJhKkFvHUUBpwpJhSCiJs1OyTQE` | 07-17 |
| Journal d'Audit | 🧭 PROMPT MAÎTRE — Loi commune de tous les agents et projets | `1LgXsasXaMJX9MKYNN9Sg3xcUOEnJyamOng878WyOK_c` | 07-17 |
| Journal d'Audit | 🛡️ PROTOCOLE — Journal & audit partagé de la flotte | `19V2uUSAOBkNJKwNdIN92aiyR8PAkVyhvwzeqkQoLIUU` | 07-17 |
| Journal d'Audit | 📖 LISEZ-MOI — Règles du journal (nommage, format, zéro doublon) | `1X8vSSV-Ymsyrh4QNcfOBXbE6wP4UHWw40NAXa_q2Eg8` | 07-13 |
| Journal d'Audit | CLAUDE.md — KeywordMoneyMaker + CompeteIQ | `175fRWioM2eXCmz4popmTPfpDMZ6lcnjc4o_roUeJ3co` | 07-13 |
| Veille/Synergies | BASE D'ERREURS de la chaîne (16 fiches) | `1s4DzGJqCIxZnsNtwei8JzkEoYQoSbm-4RoriEqUcCzY` | 09-11 |
| Veille/Synergies | Table de correspondance : 29 agents en place vs 38 rôles de la chaîne veille | `1bmnf3_YJdkge3906gLEd-T8k7JXJ-cKDVw1eh39PMbI` | 09-11 |
| Veille/Synergies | Rectificatif : la recommandation de fusion est annulée | `1Iaf0aNxwweK9GdEXkqoh-xTsRB0LMd9x0959KFS7Uss` | 09-11 |
| Veille/Brevetabilité | Verdict INSPECTEUR n°1 : simulateur de conformité (NO-GO brevet · GO marque + base de données) | `1RXnLs7UdHxyGDtOiEbVXEAVM8H9jf77x2ATljQMLTvI` | 09-11 |
| Veille/Brevetabilité | Dossier DÉPOSANT n°1 : le dépôt public n'a pas de LICENSE (E-08) | `19S2-X5uAUpQp-L-YSvHCSJgXz-JvjEOpnEY7mu_uE-I` | 09-11 |
| Veille/Brevetabilité | CANDIDATS INVENTIONS n°1 (CONFIDENTIEL) · MÉTHODE DE CONCEPTION DE BREVETS (confidentiel) | `1pzGjn3n4iQK0PvriNCDPiZ7831Y0IOvJA3ZrQqxrMJA` · `1Kk5N6XreelgwLsNlv7l6Yn7pCw9Ma0IqhmEyADREyps` | 09-19 |
| Veille/Bibliothèque | Calendrier des expirations à venir (seul fichier ; 23 sous-dossiers vides) | `1JwLEBvodLaGPP52Ta4imnGwOmGs_aZMckfWkhQJ8tVM` | 09-11 |
| Veille/Plans | Séparation des 3 produits : 3 options chiffrées · Option B détaillée : 5 phases + contrôle CI | `1Xpg72MMPkHHrE_qATeCGfl95I9WqNsbmL8PENi9M2zw` · `1P90z79fIEsPF47cNSnvGimZCuBzG6LtOGz3olagT11Q` | 09-11 |
| 🔒 Coffre `1pfFtLa5zEpYokRUaqieVTRte8YwA9sqV` | 1 doc : « 2026-09-19-13h30 — Droit accessible aux citoyens — Brevetabilité — PISTES OUVERTES … (CONFIDENTIEL) » | `17LqBi3MYYWi1X436YQ_nEDnQ9HwkAJp0j98Vdguismc` | **coffre — contenu non lu, ne doit pas quitter le Drive** |
| COMPILATION | ⭐ SOURCE UNIQUE DE VÉRITÉ — index maître · statut des projets · convention anti-collision (À LIRE EN PREMIER) | `1rYq-XdLlLL55064fhbnuzYVHbaQhWfJ548btYaEckZk` | 07-17 |
| COMPILATION | 00 — SYNOPSIS MAÎTRE — Caelum & La Loi Avec Moi | `113wyGyaofxiN6MfJecnQvL9wulzu7WCiGOtrpUG4vdY` | 07-17 |
| COMPILATION | 🔐 PATRIMOINE — base unique, tenue à jour (désignée CANONIQUE le 09-12) | `1FJmbjyle4hZovPqExSY_Sv91EYurUjN8egYQpWzBlZ4` | 09-11 — **contenu non lu ; traiter comme le coffre** |
| COMPILATION | 📒 BASE DE PROPRIÉTÉ — Nexus-Market / Caelum (doublon, subordonné à PATRIMOINE) | `1jhc4IHZpvONaZzs8xxg52Bq0ybH5t2nrY5utbORcVV8` | 09-11 |
| COMPILATION | 🔴 BASE DES ERREURS — Nexus-Market | `1xj5Mdgzk3gD7E0mXkNCIiKVbvguYlcpQEkhTQaIICZE` | 09-11 |
| COMPILATION | 07 — Protocole de supervision & vérification (anti-erreurs) | `18ScxEHejOPyy6OQOjqZVLy5JuIPmPO9AfyV5qoug8Dg` | 07-17 |
| COMPILATION | 16 — ANGLES MORTS — registre complet trié par urgence | `19U2WxRKK-sqKV6lA5qSyByl-_JhWeUIjztvIexgvTf8` | 07-17 |
| COMPILATION | 18 — PROTOCOLE MAÎTRE INTER-AGENTS — Drive-first · Vérifier · Critique² · Audit horodaté | `1Tj0ctNLxkzVXpata3X7DXqp5DTGj9sgvtFjbxVsvQfU` | 07-17 |
| COMPILATION | 19 — PROTOCOLE UNIVERSEL « DRIVE D'ABORD » (prompt à coller) | `1KsM29Ftv9puCy53fiuPT4i0VXD0wgO8a3OpEwQYXEbU` | 07-17 |
| COMPILATION | 19 — Études de marché par projet (synthèse honnête + priorité) | `1g6fJaiWZ93HQNhyTxrYBXuIK3gNHSBg7GAcneLp53JQ` | 07-17 |
| COMPILATION | 20 — BREVETS — Rapport panel (i-DEPOT = preuve, pas un titre) | `1hDHhn6J8t40F2kkQIzzOxEP9Xd5VIv83iIZwkec4a2s` | 07-17 |
| COMPILATION | 24 — PROTOCOLE DE MÉTA-SURVEILLANCE (le gardien du gardien) | `1TO3OhxSaGT-5xJdtDYpMhRMw6srla5bE0fjEScEBLog` | 07-17 |
| COMPILATION | AUDIT DEMANDÉ PAR CHAIMA : % d'avancement par projet · erreurs · angles morts · MISE À JOUR & GEL (6 apps gelées) | `1sCnSyTF490jXQm0lnTT3zDU9-sLtyLCTgM61OSxnxQQ` · `1ZtB33LkWPgeemMTJg3SF23rKZNu_GP_X_zAOCbWTkrQ` | 07-18 |
| COMPILATION | AUDIT GLOBAL — 2 erreurs d'audit corrigées | `1QOsyefKLrmsXEzbViSOAoe_7kL1pk7LO8MFQoqGBt8k` | 08-10 |
| COMPILATION | CLÔTURE : CODEX déployé + réconcilié sur les 2 dépôts · Réconciliation agents CODEX (PR #14) | `1fkytrc5SRjDvML2PtFbI1-poRWB2h_LBGafxB77qsUs` · `1o_8BU4dSdDu4SvCVFW3qy_hNkbdYlbZcD15M2_G12KI` | 09-11 |
| COMPILATION | CONSOLIDATION DES 2 REGISTRES DE PROPRIÉTÉ : PATRIMOINE canonique | `1Qf-af2ymsn6XZ5LrWMSrTrvJ52iR2uCbCYmctcVHKKE` | 09-12 |
| COMPILATION | Empire (transverse) — Rapport de session — 7 entrées du registre disparues et restaurées | `1yeMgd0p9_MUBK3oC14jq4l3-ghQugrrVLI701BHpUdM` | 09-19 |
| COMPILATION | Audits par projet 07-17 : Patchou · Motif Studio · SOLEA (+ ALERTE doublon protocole) · Bulle parents-enfants · brevets CompeteIQ | `1M0RKDE53preiE4zjfZvnnSwZeLCTTBo1KQFHPDq4ScA` · `1O4SQ3yjOiVflSe_NXdyfY5eWFgJ_pvQCXEqDl_K8zwQ` · `10o3xJMFcp3VDb_4KFFqwcx26fOS-8tMXNPy4qU4VGJM` · `1L-A2CFi_rPzj1JDCDAmq8WT7ViQh3kQ0TMYvOAGjl-Y` · `16aRe44aaP5UW-EUXySQ2yTXONRQB52fL9cnhkGoBbWo` | 07-17 |
| COMPILATION/Revue Design | 00 README/Synopsis · 02 Vérification + CRITIQUES² · 08 VERDICT Ella NON-ACHAT · 21 À LIRE EN PREMIER (copie) | `1FpIRAIbiJ_cXOI4Jt7aDQvX2nExggXEoF5Ioo-V5BxY` · `1qeDAHIfwwbzeWeNkDdiawO21CGOk8ia2ZUTXbi1eqqU` · `1rUJlUpgf8AOhTGRRhXgqFr-wZExjbJubVVes7GmnUOM` · `1dUTtIMnShufOHv1_dAQ6BqF8BCMMw0_uY1EDgl88rWk` | 07-17 |
| LLAM Base | ⚙️ FICHE TECHNIQUE (INTERNE — NE PAS PUBLIER) — Journal qualité & protocole anti-doublon (maj 09-18) | `1OfbjCDaebE4Oeo1JxrO6GrebJY37APZr` | 09-18 |
| LLAM Base | Exemples de fiches : NIS2 (08-09) · RGPD PME (07-23) · marque BOIP/EUIPO (09-11) · DSA (09-18) | `10Wf7tgUYbyah8auWMFZhSibX5PGyT-1U` · `1dA5DubSXAxT0xDs3tshO9X1M_7JnqnNOlUPWQTvlV0g` · `1PZtwpIN5UDx3tzhE7u1mdyJTdOsYSHqN` · `11QPkMRyH0xL8STwGptLBQJCyLW8QVf2GLqGyPY95Yb8` | — |
| Archive & Mémoire | 🗂️ ARCHIVE COMPLÈTE — Empire … — 18 juin 2026 (titre tronqué) | `1hJxjEUNhhdSlKqMA_dAe_zOK69dE9duT0TKxTOgWQj4` | 06-18 |
| Archive & Mémoire | CLAUDE.md — MASTER (Emploi du temps + Système global) | `1ZBZ59GdFhUtm05wqfdh-KxueCZKcnqg03XdO3e8sP0c` | 07-13 |
| Archive & Mémoire | 📡 CANAL v2 — Instructions permanentes · 📅 VÉRIFICATION QUOTIDIENNE & AUDIT HEBDO · 🔍 AUDIT MATURITÉ · 📋 PROTOCOLE COMMENTAIRES | `1J0xvlYRAnkKzFuL-m8KOq0OelyhPkmKqELW542OSkxM` · `1hPDFOOpslC3D_RcFFMIodRaIzH-XWa8d41GR1oXWbwc` · `16ve977yTw5dyuwiRekzbaZTJgo4lUYi61DYK7D04FZQ` · `1mVCbc2u5x0mRmG09l9p5b3E-8SC-NdmgHpM7jf-4hVg` | 07-13 |
| Archive/PRÉSENTATION | 01 — Empire Chaima — Vision Globale, Fondatrice & Carte de l'Empire | `1b4JeM7FkWj6HkjyRExN7B_Ih3BEi6tB3erQ9DWuXemE` | 07-13 |
| Archive/LLAM · racine | GO-NO-GO — Décision de lancement (LLAM + Caelum) — 2026-06-29 (3 copies) | `1mddWNbElvsiE7zENCi5IvJowbqcUlKymzNRWD-h7T3c` (racine) | 06-29 |
| CV Booster | CLAUDE.md · Positionnement & Différenciateurs | `1pgFRyXKUVYBeS6474xfPind8skNVSnhv` · `1Zv0VJjdbaB7amMN0GT94ALvF-N8cBGnmmVRNMuzw7Gw` | 09-02 |
| ATLAS | 01 FICHE MACHINE · 02 ERREURS ET RÉUSSITES · 03 PROMPT MAÎTRE v2 | `1GRzD4Oow7O8wWjg-Dv3iirUbmlYpKyilyek0YsVOl20` · `1cKad7xISrny7R5KGr1hseX0HlOUWATHQ3QfvhlCDZkU` · `1dvZzc_DyMApBYOipJiug1WC6zYPiappmO1Z0PjMko4M` | 09-16/19 |
| 00 PROTOCOLE | PROTOCOLE_Agents-et-Projets_v1_2026-07-17.md | `1hDA3W9jzMs7E3elcQvWM39YRspMrP9fd` | 07-17 |
| LLAM Audits | 00 — Présentation du projet & passation · 🔴 ERREURS · 📋 JOURNAL · CLAUDE.md · PROTOCOLE Conseil d'experts · Problèmes ouverts (backlog) · DOSSIER COMPLET 07-14 & règle anti-doublons | `1sMNeK3jIhoLFNdWnUWy3u2OH2FV2SdRNPsxdI-Et0iQ` · `14Kb5fU6Ll52-H7vJ2oyvNHPKVBhvcqvRNwUlQA3W-Oc` · `1kbWgC_w6I_mKv2p6IfgWEqfBIMWj7R6_i7CxYRflGsc` · `1BBP7u98bdTNhrv7BlpF9zr768qNdNzHAQlVvNELjN24` · `1f0rRofvDaZJJvI5ViXNq2VZK2bdAMr0TVPmHS_Blp_s` · `1qeu4v8hEwCBubZjMC0w1dLOMqqoPO78Tsdy5CmIZoFM` · `1R9sDAMXtGoEHssqoiwMA3AlMIKe6CCgWsfJ_gLOvJU0` | 07-13/14 |
| CompeteIQ | 01 — Inventaire technique.md · 00 — Journal d'audit (uplift enterprise) | `1nJwX6fu2vE2CnAMnBp5IPH3GvelZNgPj7rGjO6NzUuo` · `1T4OminCHKAc3tJg4o0J4nRyh8UOptIqQdagCxyMfCvA` | 07-17 |
| Lyra | 00 — Synthèse & sommaire (README).md · 01 — Prompt optimisé Mistral AI v1.0.md · 03 — Kits juridiques — synthèse & liens GitHub.md | `1nvA37bWnSoBu8pbuo8dQzbadvIXXxwzA` · `1nSjtYBVm46lSHHFcPw2zglEIjfSQ5EVp` · `1dbnWKpxOZPBayIo1U7c8lKR9gB87cMjW` | 07-13/17 |
| SOLEA | 00_INDEX.md · EVALUATION-GOUVERNEE_2026-07-17.md | `1bTc4IZ9-XGrphYYucJF-dunKn-V75teS` · `17oj_0_qKL6eeoZxq3yWA1bhp2Ckm2Ugy` | 07-17 |
| LibreEtAccomplis | Journal d'audit — Installation du Protocole Codex + structure Drive · Présentation (état du projet) | `1crY8KRL08voW8d3FB6nFHoZoILkUE1wjOLogfXUTGjo` · `1tiCeoYVm4x_pLpEXdzy1yl1wYUeoGikHr88sI8cnhIk` | 09-06 |
| Idées perso | Fiches idées App Couples + App Parents-Enfants · 2 PROMPTS BUILD | `19Fdxc8NZyCglZVXY7_Of6xHHUDMOCQnNC0phgjiunmY` · `1vVsg0vzHmecb6rUjvULWDk1A_FkYfTHfy-R0rGoauec` | 07-17 |
| Feedback quotidien | 📋 Mon Système complet — Récapitulatif · Feedback le plus récent (vendredi 18 septembre) · 🎯 Ce que je dois améliorer | `1m-l8zNfgPwG5yPby0DJ9lqki7xwlIQYV299g9YYLQ1w` · `1ll3XXHCMt5ZgMa824xKzYv_ZR2_GBdrmV3MduTpIPrM` · `1r4UJRLU5wYUltmxdWdydmTuYzUoHPWacp6GzzWYRGbs` | 07-13 → 09-18 |
| Racine | 📇 INDEX — Drive Chaima (référence unique).md · 🗂️ PLAN DE CONSOLIDATION — Drive (PROPOSÉ).md · Jeu Linux — Registre & Audit technique · 📊 TBA — Flotte complète | `1pHKZBbXlw1JCjlcir_YqqYDPCH8L9f3-` · `1NRXUXhz_NifzczCqPLnFcztg0lPPlvjn` · `1W0i8sHNBPi47fRtoAjfOnKwQo_PUAJ9THVRa0rVktyM` · `1bt42A_ECR8fhvJdbqPDvtvbSrhC2YpiTptoSKZ5k_2s` | 09-11 · 09-06 · 09-16 · 06-27 |

## 3. Ce que la carte révèle

### 3.1 Doublons de dossiers et de fichiers (comptés sur les titres, contenus non comparés)

| Doublon | Où | Constat |
|---|---|---|
| **Caelum ×2** | `Caelum — Direction` (17) vs `Archive & Mémoire/📂 Caelum` (15) | 10 titres identiques (CLAUDE.md, JOURNAL, ERREURS, Offre conformité, Stratégie marketing, Logique d'entreprise, Évaluation viabilité, Avis appels à projets, 2 journaux d'audit). L'INDEX 09-11 dit « 5 dossiers Caelum → 3 » : la copie d'Archive a survécu à la consolidation. |
| **La Loi Avec Moi ×3** | `LLAM — Audits` (17) vs `Archive/📂 La Loi Avec Moi` (12) vs racine (5) | 7 titres identiques Audits↔Archive ; Étude de marché, Compte-rendu, Avancement et les 2 `.ics` existent à la racine **et** dans Archive. |
| **GO-NO-GO 06-29 · Kit de contenu · Études de marché/prix** | racine + Archive/Caelum + Archive/LLAM | Jusqu'à **3 copies** du même titre. |
| **Feedback quotidien ×2** | racine `📊` (34) vs `Archive/📂 Mon Feedback quotidien` (2) | Les 2 docs d'Archive = copies du 07-13. |
| **Lyra ×2 + sous-dossier vide** | `Lyra/2026-07-13 Optimisation prompt Mistral` (3) = `Archive/Lyra/…` (3) ; `Lyra/2026-07-13 Produits numériques` **vide** à côté du 07-17 (4) | Titres identiques. |
| **Journal d'Audit ↔ Archive/Caelum** | LISEZ-MOI, 2 journaux d'audit 07-13 | Copiés 3 fois. |
| **7 générations de « protocole maître »** | 00 PROTOCOLE v1 (07-17) · 🧭 PROMPT MAÎTRE loi commune (07-17) · Flotte/01 PROMPT MAÎTRE (07-17) · 18 PROTOCOLE MAÎTRE INTER-AGENTS (07-17) · 19 PROTOCOLE UNIVERSEL (07-17) · CODEX (09-06, **référence** d'après CLAUDE.md) · ATLAS/03 PROMPT MAÎTRE v2 (09-19, le plus récent) | Le doc `10o3xJMF…` (07-17) signalait déjà « ALERTE doublon protocole (à supprimer) ». Aucune ligne ne dit lequel des 7 fait foi **aujourd'hui** ; CLAUDE.md du dépôt tranche pour le CODEX 09-06. |
| **2 registres de propriété** | 📒 BASE DE PROPRIÉTÉ vs 🔐 PATRIMOINE (09-11, créés à 3 min d'écart par 2 sessions) | MÉTA-ALERTE `1R6bMro1…` puis consolidation 09-12 : **PATRIMOINE canonique**. Doublon toujours présent (append-only). |
| **3 index du Drive** avant celui-ci | 📇 INDEX (09-11, « seul index, tout autre est un doublon ») · 🗂️ PLAN DE CONSOLIDATION (09-06, PROPOSÉ, non tranché) · index Drive de la branche `claude/multi-agent-migration-factory-riujie` (07-17) · ⭐ SOURCE UNIQUE (07-17) | L'INDEX 09-11 ne couvre que 7 dossiers ; il ignore COMPILATION (678 fichiers avec ses 2 sous-dossiers), Archive (48), Journal d'Audit, Veille, ATLAS, Feedback, la base LLAM (372). **Cette carte est le 4e index** — elle doit remplacer ou être référencée par l'INDEX, pas s'ajouter à côté. |
| **Contradiction de statut LLAM** | ⭐ SOURCE UNIQUE 07-17 : « LLAM = VITRINE de Caelum, PAS gelé » et « fait autorité jusqu'à une SOURCE UNIQUE plus récente » ; 📇 INDEX 09-11 : « LLAM — projet GELÉ jusqu'après le CCNA » | Deux documents « source de vérité » se contredisent. **Non tranché ici** (§10) — à porter dans A-DECIDER. |
| **Dossier vide, pièces ailleurs** | `Patchou` (0) alors que COMPILATION contient audit & synopsis Patchou + installation CODEX Patchou | Le dossier projet n'est pas le lieu où les agents écrivent. |
| **Sous-dossiers coquilles** | 23 pays/offices de la bibliothèque brevets, Communication & Marketing, Financement & Capitaux, Technologies exploitables, Feedback/Audits quotidiens, Libre/problemes | Structure créée le 09-11 sans contenu 8 jours plus tard. |

### 3.2 Drive ↔ git : qui manque où

| Situation | Projets |
|---|---|
| **Dans le Drive, sans branche dans `test`** | CV Booster (4 docs, CLAUDE.md complet) · KeywordMoneyMaker (dépôt séparé `keywordmoneymaker`, nommé dans 9 titres de COMPILATION + 1 CLAUDE.md) · Lyra « Produits numériques Droit Citoyen » (`chainage.py`, kits juridiques) · Dossier école / Feedback quotidien (non-code, normal) |
| **Dans git, sans dossier Drive** (au plus 1 doc dans COMPILATION) | Coupe du Monde 2026 · Prospection B2B · Day-trading · Prototype GTA · CRM ventes · Site Moonbow · Présentation sélection projets · Usine de migration multi-agents · Motif Studio / canvas (1 audit `1O4SQ3yj…`) · Bulle parents-enfants (1 doc `1L-A2CFi…` + fiche idée) · Jeu Linux (1 registre racine + 1 doc COMPILATION) |
| **Présents des deux côtés, alignés** | Caelum/Nexus-Market · LLAM · ATLAS · CompeteIQ · SOLEA · Libre & Accomplis · Audit brevets · CODEX · Couples · Mistral (PLAUSIBLE) · Patchou/Shopify (PLAUSIBLE) |
| **Asymétrie de volume** | LLAM : **368 fiches** dans le Drive vs branche `swarm-50-agent` à 3 539 commits — le Drive est-il la copie ou la source ? **NON VÉRIFIÉ.** Risque de continuité n°1 de CARTE-PROJETS : ici, il y a au moins une seconde copie de la matière (les fiches), pas du code. |
| **Ce que le Drive sait et que git ignore** | 149 journaux `boucle-caelum` (surveillance du site et de `main`, plusieurs pièces par jour en juillet-août d'après les horodatages) · 13 MÉTA-ALERTES (faux positifs répétés : « PR #2 non mergée » rejoué 07-25 → 09-16, E-02) · 29 feedbacks quotidiens de Chaima |

### 3.3 Les vraies portes d'entrée (« 00 — SYNOPSIS / INDEX »)

Par ordre de portée : ⭐ SOURCE UNIQUE DE VÉRITÉ `1rYq-XdL…` (statut officiel des projets, convention
d'horodatage « AAAA-MM-JJ-HHhMM — [auteur] — [titre] », un doc = un événement, append-only) →
00 SYNOPSIS MAÎTRE `113wyGya…` → 📇 INDEX Drive `1pHKZBbX…` → puis un « 00 » par projet : Flotte
`1KhB0-ty…`, Revue Design `1FpIRAIb…`, SOLEA `1bTc4IZ9…`, LLAM Audits `1sMNeK3j…`, Lyra `1nvA37bW…`,
SSL `1M0QSB-r…`, CompeteIQ `1T4OminC…`. Le fil quotidien (COMPILATION) se lit **par préfixe d'auteur**
(`boucle-caelum` / `Code (session …)` / `coach` / `MÉTA-ALERTE`) et par date, jamais par numéro
(les entiers 18-27 sont en collision : deux « 23 », deux « 18 », deux « 19 »).

### 3.4 Les 10 documents à lire EN PREMIER pour comprendre comment l'Empire travaille

| # | Document | ID | Pourquoi |
|---|---|---|---|
| 1 | ⭐ SOURCE UNIQUE DE VÉRITÉ — 2026-07-17 | `1rYq-XdLlLL55064fhbnuzYVHbaQhWfJ548btYaEckZk` | Statut officiel des projets + la convention qui gouverne tout le Drive depuis (lu : cohérent avec le relevé) |
| 2 | EMPIRE-CHAIMA-protocole-agents-CODEX.md | `1GFKFky8ziXr7YY_Zd-6Kwk_QqOsvrLei_F_hDaLFHqw` | Le protocole en vigueur (= tête du CLAUDE.md du dépôt) |
| 3 | EMPIRE-CHAIMA-prompt-maitre-claude-code.md | `1GoOOJ4fmQOGrBoZEQ8HkkYpouIFoOUxBGa5vECdpp9I` | Comment on lance une session |
| 4 | 03 — PROMPT MAÎTRE v2 (ATLAS, 2026-09-19) | `1dvZzc_DyMApBYOipJiug1WC6zYPiappmO1Z0PjMko4M` | La version la plus récente du prompt maître — à confronter au n°3 |
| 5 | 📇 INDEX — Drive Chaima + 🗂️ PLAN DE CONSOLIDATION (PROPOSÉ) | `1pHKZBbXlw1JCjlcir_YqqYDPCH8L9f3-` · `1NRXUXhz_NifzczCqPLnFcztg0lPPlvjn` | Ce que l'Empire croit être son rangement (lus : partiels, voir §3.1) |
| 6 | 00 — SYNOPSIS MAÎTRE — Caelum & La Loi Avec Moi | `113wyGyaofxiN6MfJecnQvL9wulzu7WCiGOtrpUG4vdY` | Les deux projets vivants, en une pièce |
| 7 | 🔴 BASE DES ERREURS — Nexus-Market + BASE D'ERREURS de la chaîne veille (16 fiches) | `1xj5Mdgzk3gD7E0mXkNCIiKVbvguYlcpQEkhTQaIICZE` · `1s4DzGJqCIxZnsNtwei8JzkEoYQoSbm-4RoriEqUcCzY` | Ce qui a déjà raté — la matière d'`apprentissage/` |
| 8 | REGISTRE MAÎTRE — Agents Caelum + Table 29 agents vs 38 rôles | `1Vy5Uy6DI8t2_I9HX2yhGjcQ9YxRAwnw8pHyGYFo2zOk` · `1bmnf3_YJdkge3906gLEd-T8k7JXJ-cKDVw1eh39PMbI` | Qui fait quoi dans la flotte, et l'écart entre rôles prévus et agents réels |
| 9 | 24 — PROTOCOLE DE MÉTA-SURVEILLANCE + 19 — PROTOCOLE UNIVERSEL « DRIVE D'ABORD » | `1TO3OhxSaGT-5xJdtDYpMhRMw6srla5bE0fjEScEBLog` · `1KsM29Ftv9puCy53fiuPT4i0VXD0wgO8a3OpEwQYXEbU` | Comment l'Empire se contrôle lui-même (et pourquoi les MÉTA-ALERTES existent) |
| 10 | 📋 Mon Système complet — Récapitulatif + Feedback du 18 septembre + Rapport transverse 09-19 | `1m-l8zNfgPwG5yPby0DJ9lqki7xwlIQYV299g9YYLQ1w` · `1ll3XXHCMt5ZgMa824xKzYv_ZR2_GBdrmV3MduTpIPrM` · `1yeMgd0p9_MUBK3oC14jq4l3-ghQugrrVLI701BHpUdM` | Comment Chaima travaille au quotidien, et l'état au jour du relevé |

Puis, pour la passe « apprendre » : les 368 fiches LLAM (par sujet, `LLAM — …`), les 149 `boucle-caelum`
(en diagonale : une large part est titrée « INCHANGÉ » — non comptée), les 29 feedbacks, la ⚙️ FICHE TECHNIQUE LLAM `1OfbjCDa…`.

## 4. NON VÉRIFIÉ — ce que le relevé n'établit pas

- Le **contenu** de tout document sauf 3 (INDEX, PLAN DE CONSOLIDATION, SOURCE UNIQUE) ; les « rôles » sont déduits des titres.
- Que les titres identiques soient des contenus identiques (doublons **PLAUSIBLES**, non comparés).
- Le nombre de fichiers antérieurs à 2026 à la racine et dans les 4 dossiers personnels (jamais listés).
- Les rapprochements Lyra ↔ `mistral-mnwb5j` et Patchou ↔ `shopify-app-development` (titres seuls).
- Le sort des 2 dossiers Caelum cités par le PLAN (`1o14U0Wm…`, `1CzwVoRc…`) : absents du relevé, « corbeillés » selon l'INDEX.
- Le « 97 agents Python » du REGISTRE MAÎTRE (affirmation de l'INDEX, doc non ouvert).
- Que la base LLAM du Drive soit synchronisée avec la branche git (aucune comparaison faite).
- Fichiers partagés avec Chaima mais possédés par d'autres (`sharedWithMe`) : non interrogés.

---

    DE : cartographe                POUR : CHAIMA (via l'orchestrateur ATLAS)
    OBJET : Adopter cette carte comme index unique du Drive (remplacer ou faire pointer 📇 INDEX 1pHKZBbX… vers elle), puis porter dans A-DECIDER les 3 points de §3.1 qui t'appartiennent : (a) lequel des 7 « protocoles maîtres » fait foi, (b) statut LLAM « vitrine » (07-17) vs « gelé » (09-11), (c) corbeiller ou non les copies Archive/Caelum, Archive/LLAM, Archive/Lyra, Archive/Feedback.
    VERDICT : VÉRIFIÉ (inventaire : 906 fichiers Empire comptés par listing exhaustif le 2026-09-19) · PLAUSIBLE (doublons et rôles, déduits des titres)
    PARCE QUE : 19 dossiers Empire + 22 fichiers racine listés dossier par dossier, 4 pages pour la base LLAM (372) et 3 pour COMPILATION (283) ; ⭐ SOURCE UNIQUE `1rYq-XdL…` §3 et 📇 INDEX `1pHKZBbX…` lus et confrontés au relevé.
    NON VÉRIFIÉ : §4 ci-dessus — en tête : contenu des documents, identité réelle des doublons, synchronisation Drive↔git des fiches LLAM.
    CE QUI CHANGERAIT MON AVIS : un listing `sharedWithMe = true` ou un dossier Empire hors de « Mon Drive » (Drive partagé) révélant des fichiers non comptés ; ou une lecture montrant que les copies d'Archive divergent des originaux (alors ce ne sont pas des doublons mais des versions).
