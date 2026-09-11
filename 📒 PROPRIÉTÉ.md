# 📒 BASE DE PROPRIÉTÉ — TEST / Nexus-Market / Caelum Partners

> Registre unique de ce que le projet possède réellement. Consultable par tous les agents.
> **Règle absolue (PROTOCOLE §13) : vérité totale, zéro invention.** Chaque ligne est
> sourcée et datée, ou marquée « À VÉRIFIER ». Les affirmations « sur nous »
> (déposé, breveté, certifié, enregistré) sont les plus dangereuses — aucune n'est
> posée sans preuve.
>
> **Dernière mise à jour : 2026-09-11 (`TZ=Europe/Brussels`).** Tenu à jour à chaque
> ajout d'actif. Détail des créations : historique git + `reports/`.

---

## Légende des statuts

| Statut | Sens |
|---|---|
| **POSSÉDÉ** | Créé par nous / en notre possession de fait (ex. code, contenu original). |
| **VÉRIFIÉ** | Présence + date confirmées par une preuve primaire (commit git, fichier, lien). |
| **À VÉRIFIER** | Revendication non encore confirmée depuis ce dépôt (souvent : actif externe au repo). |
| **À DÉPOSER** | Ne serait sécurisé juridiquement que par un dépôt/enregistrement — **non fait**. |

> **Portée honnête de ce document.** Il est bâti à partir de **ce dépôt** (`chaima0007/test`)
> et de son historique git. Les actifs qui vivent **hors du dépôt** (domaine, comptes,
> inscription légale, dépôts de marque) sont marqués **À VÉRIFIER** : cette instance ne peut
> pas les confirmer — leur preuve est dans les comptes de Chaima.
>
> **Note juridique (NON un conseil juridique — PLAUSIBLE, §13).** En Belgique/UE, le
> **droit d'auteur** protège une œuvre originale **automatiquement dès sa création**, sans dépôt ;
> la date de création peut se prouver par l'horodatage git. En revanche, **un nom de marque
> n'est « possédé » comme marque que s'il est enregistré** (BOIP/EUIPO) — l'usage seul ne
> confère pas de droit de marque. Une **recherche d'antériorité** et un avis d'un conseil PI
> humain restent nécessaires avant tout dépôt (§11).

---

## 1. Noms & marques

| Nom / description | Statut | Date (1re trace) | Source / preuve |
|---|---|---|---|
| **Caelum Partners** (nom d'agence) | À VÉRIFIER (usage interne) · **À DÉPOSER** si protection marque voulue | 2026 | Usage dans le code/contenu du repo ; aucun dépôt de marque confirmé. |
| **Nexus-Market** (nom de produit/pipeline) | À VÉRIFIER · **À DÉPOSER** si voulu | 2026-06 | Nom de la branche/PR ; usage documenté, pas de dépôt. |
| **CompeteIQ** (nom de l'app existante) | À VÉRIFIER · **À DÉPOSER** si voulu | 2026-06-17 | `package.json` → `"name": "competeiq"` ; commit `587fc78`. |
| **PROTOCOLE CODEX — EMPIRE CHAIMA** (nom du cadre de gouvernance) | POSSÉDÉ (contenu) · marque **À DÉPOSER** si voulu | 2026-06-17 | `CLAUDE.md` (commit `587fc78`, version protocole 2026-09-06). |
| **Noms d'agents** : HERMES, BOUSSOLE, PACTE, RELANCE, SENTINEL, ORACLE, NEXUS, FORGE, ECHO, PRISM, ATLAS, NEXAGEN, COMMANDANT, RÉSOLVEUR | À VÉRIFIER (termes courants/mythologiques, faible protégeabilité isolée) · **À DÉPOSER** seulement en tant qu'ensemble/logo si voulu | 2026 | `lib/agents/registry.ts` (`8a21af1`+). Beaucoup sont des mots communs → protection marque limitée. |

> ⚠️ **Aucune de ces marques n'est déposée à ce jour** (aucune preuve de dépôt BOIP/EUIPO
> dans le dépôt). « Possédé » ne s'applique pas à une marque non enregistrée.

---

## 2. Code & modules créés (droit d'auteur automatique)

> Statut **POSSÉDÉ · VÉRIFIÉ** : œuvres de code originales, présentes dans le dépôt, datées par git.
> La date = **première apparition** du fichier dans l'historique (antériorité).

| Module / description | Statut | Date création (git) | Source / preuve (commit) |
|---|---|---|---|
| **Flotte d'agents Caelum** — registre + agents | POSSÉDÉ · VÉRIFIÉ | 2026-06-18 | `lib/agents/registry.ts` `8a21af1` (FLEET = 14 agents) |
| Agent **HERMES** (prospection LinkedIn) | POSSÉDÉ · VÉRIFIÉ | 2026-09-11 | `lib/agents/hermes.ts` `407b424` |
| Agent **BOUSSOLE** (qualification déterministe) | POSSÉDÉ · VÉRIFIÉ | 2026-09-11 | `lib/agents/boussole.ts` `05c7666` |
| Agent **PACTE** (devis / closing) | POSSÉDÉ · VÉRIFIÉ | 2026-09-11 | `lib/agents/pacte.ts` `25dc63c` |
| Agent **RELANCE** (relance de devis) | POSSÉDÉ · VÉRIFIÉ | 2026-09-11 | `lib/agents/relance.ts` `9df5764` |
| Agents **COMMANDANT** + **RÉSOLVEUR** + module **compliance** | POSSÉDÉ · VÉRIFIÉ | 2026-06-18 | `lib/agents/{commandant,resolveur,compliance}.ts` `8a21af1` |
| **Pipeline Nexus-Market** (state machine 5 étapes, orchestrateur reprenable) | POSSÉDÉ · VÉRIFIÉ | 2026-06-17 | `lib/pipeline/orchestrator.ts` `668804c` + `lib/pipeline/*` |
| **Simulateur Monte-Carlo** (RNG déterministe) | POSSÉDÉ · VÉRIFIÉ | 2026-06-18 | `lib/pipeline/simulator.ts` `97be0b0` |
| **Dashboard** (pages `app/dashboard/*`, routes API `app/api/*`) | POSSÉDÉ · VÉRIFIÉ | 2026-06-17 → 2026-09-11 | `app/` (commits `668804c` → `9df5764`) |
| **Suite de tests** (77 tests, Vitest) | POSSÉDÉ · VÉRIFIÉ | 2026-06 → 2026-09 | `lib/**/__tests__/`, `app/**/__tests__/` |
| **Correctif build Prisma** (`postinstall: prisma generate`) | POSSÉDÉ · VÉRIFIÉ | 2026-07-17 | `package.json` `2332776` |

> **Licence sortante / propriété du code : NON DÉFINIE (À VÉRIFIER).** Le dépôt ne contient
> pas de fichier `LICENSE`. Par défaut, sans licence, le code reste « tous droits réservés »
> à l'auteur — mais le statut voulu (propriétaire, revente, open-source) est **une décision de
> Chaima** (cf. §11 licences sortantes, `/codex/licences-sortantes/`).

---

## 3. Contenus originaux (protégés par droit d'auteur dès leur création)

| Contenu / description | Statut | Date | Source / preuve |
|---|---|---|---|
| **Texte du PROTOCOLE CODEX** (§0–§15) | POSSÉDÉ · VÉRIFIÉ | 2026-09-06 (version) | `CLAUDE.md` |
| **Skill « débat »** (orchestration Parcours 2) | POSSÉDÉ · VÉRIFIÉ | 2026-09-06 | `.claude/skills/debat/SKILL.md` `ae13c0b` |
| **21 fiches d'agents** `.claude/agents/*.md` | POSSÉDÉ · VÉRIFIÉ (dérivées du §1, NON VÉRIFIÉ comme set canonique) | 2026-09-06 | `.claude/agents/` (21 fichiers) |
| **Gabarits de messages** (prospection HERMES, devis PACTE, relance RELANCE) | POSSÉDÉ · VÉRIFIÉ | 2026-09-11 | `lib/agents/{hermes,pacte,relance}.ts` |
| **Copie du dashboard** (textes d'interface FR) | POSSÉDÉ · VÉRIFIÉ | 2026 | `app/dashboard/*` |
| **Rapports horodatés** (`reports/*.md`) | POSSÉDÉ · VÉRIFIÉ | 2026-07 → 2026-09 | dossier `reports/` |
| **Offre Caelum** (« site web premium » 500 €, formulations) | POSSÉDÉ · VÉRIFIÉ | 2026-09-11 | `lib/agents/hermes.ts` (`CAELUM_OFFER`) |

---

## 4. Documents d'antériorité (preuve de date de création)

| Preuve | Statut | Date | Source |
|---|---|---|---|
| **Historique git complet** du dépôt `chaima0007/test` | VÉRIFIÉ | depuis 2026-06-17 | `git log` (premier commit `587fc78`) |
| **Rapports horodatés** dans `reports/` (heure Bruxelles) | VÉRIFIÉ | 2026-07-17 → 2026-09-11 | dossier `reports/` |
| **Dépôts Drive** (dossier « COMPILATION & SYNOPSIS — Empire Chaima ») | À VÉRIFIER (hors repo) | 2026-09-11 | Google Drive id `1qXUj9D9r7HSmIMzMcsScz4Ynlv4auP4G` — preuve côté Drive |
| **JOURNAL / EVOLUTION** (snapshots datés) | VÉRIFIÉ | 2026-06 → 2026-09 | `📋 JOURNAL.md`, `codex/EVOLUTION.md` |

---

## 5. Actifs externes au dépôt (À VÉRIFIER — preuve chez Chaima)

> Cette instance Nexus-Market n'a **pas** accès à ces comptes ; elle ne peut donc rien y
> confirmer. Statut **À VÉRIFIER** par Chaima, avec la preuve correspondante.

| Actif / description | Statut | Date | Source / preuve à fournir |
|---|---|---|---|
| **Compte GitHub** `chaima0007` + dépôt `test` | À VÉRIFIER (possession très probable) | — | Accès au compte GitHub |
| **Nom de domaine** (Namecheap, mentionné hors repo) | À VÉRIFIER · **À renouveler** | — | Facture / panneau Namecheap |
| **Inscription légale de l'activité** (indépendant/société) | À VÉRIFIER — **en attente** (cf. `A-DECIDER`) | — | Justificatif d'inscription (BCE/guichet) |
| **Compte Stripe** (paiement) | À VÉRIFIER — **non activé** | — | Tableau de bord Stripe |
| **Hébergement** (Cloudflare Pages visé ; Vercel résiduel) | À VÉRIFIER | — | Comptes Cloudflare / Vercel |
| **Marques déposées** (BOIP/EUIPO) | **À DÉPOSER** — aucune connue | — | Récépissé de dépôt (n'existe pas à ce jour) |
| **Brevets** | Sans objet — **rien déposé** ; logiciel pur généralement non brevetable en UE (art. 52(2)(c) CBE, §11) | — | — |

---

## 6. Ce qui reste à trancher (renvoi vers `/codex/A-DECIDER.md`)

- Définir la **licence** du code (propriétaire / revente / open-source) → crée un `LICENSE`.
- Décider si des **noms/logo** méritent un **dépôt de marque** (avis conseil PI humain, §11).
- Confirmer/rassembler les **preuves externes** (domaine, inscription légale, Stripe).

> Toute évolution de ce registre = une ligne datée et sourcée. Aucune revendication
> « possédé / déposé / breveté » ne sera ajoutée sans preuve primaire (§13).
