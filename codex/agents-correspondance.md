# /codex/agents-correspondance.md — réconciliation de `.claude/agents/` avec le set canonique

> **2026-09-11 — TRANCHÉ PAR CHAIMA.** Referme la ligne ouverte le 2026-09-06 dans `/codex/A-DECIDER.md` :
> « Les 21 agents sont dérivés du §1 (NON VÉRIFIÉ comme officiels) ; **les remplacer par le set canonique
> de l'Empire s'il existe** ». Il existe : c'est celui de `chaima0007/keywordmoneymaker`.

## Ce qui a été remplacé
Les 21 fichiers de `.claude/agents/` existaient déjà (commit `ae13c0b`, 2026-09-06). C'étaient des **ébauches
de 11-12 lignes** qui se déclaraient elles-mêmes non canoniques (« Généré dérivé du PROTOCOLE CODEX §1
(NON VÉRIFIÉ comme set canonique de l'Empire) »), sans champ `tools:` et sans socle commun.

Elles sont remplacées par les **versions complètes alignées sur keywordmoneymaker** (51-66 lignes chacune).
Les noms des 21 rôles sont inchangés : aucun agent ajouté, aucun supprimé, aucun renommé.

| | Avant (`ae13c0b`) | Après |
|---|---|---|
| Nombre d'agents | 21 | 21 |
| Lignes au total | 234 | 1149 |
| Champ `tools:` | absent | présent sur les 21 |
| SOCLE COMMUN (§3/§10/§13/§14) | absent | présent, **byte-identique** sur les 21 |
| Statut auto-déclaré | « NON VÉRIFIÉ comme set canonique » | canonique (aligné sur l'Empire) |

## Provenance — VÉRIFIÉ par comparaison, pas de mémoire
- **13 rôles repris à l'identique** de `keywordmoneymaker@ab6d4dd` : `arbitre-expert`, `archiviste-preuves`,
  `avocat-du-client`, `avocat`, `cartographe`, `conservateur-secrets`, `contradicteur`, `croque-mort`,
  `intendant-couts`, `responsable-continuite`, `simulateur-scenarios`, `superviseur-vigie`, `verificateur-verite`.
- **8 rôles rédigés pour ce dépôt** dans le même format, en reprenant la substance des agents métier qui les
  couvraient dans keywordmoneymaker : `scout` (← chercheur-code-libre), `guardian-licences` (← auditeur-licences),
  `sentinel-securite` (← architecte-securite), `architecte-integration` (← dev-backend-integrations),
  `gardien-donnees` (← rgpd-securite), `scribe-empire` (← redacteur-contenu),
  `eclaireur-opportunites` (← analyste-marche), `testeur-adverse` (← qa-verificateur).
- **SOCLE COMMUN identique à celui de keywordmoneymaker** (SHA-256 tronqué `582d8c2cd342`) — cohérence
  inter-dépôts mesurée, pas supposée.
- Aucun pourcentage dans les 21 fichiers (interdit §13).

## Recalages sur la réalité de CE dépôt (6 lignes)
Les agents portent les contraintes réelles d'ici, pas celles de keywordmoneymaker :
- chaîne de vérification avant push : `npm run lint && npx tsc --noEmit && npm test && npm run build` (CLAUDE.md §15.4) ;
- piège `PageProps` / `tsc` avant `next build` (🔴 ERR-008) ;
- garde-fous de nos propres textes (🔴 ERR-006) ;
- priorité produit : entonnoir Nexus-Market / Caelum (HERMES → BOUSSOLE → PACTE → RELANCE) ; CompeteIQ EN PAUSE.

## Pourquoi 21 ici et 42 dans keywordmoneymaker
keywordmoneymaker portait déjà une **flotte métier de 29 agents** (SEO, marketing, dev, design…). La réconciliation
y a **ajouté 13 rôles CODEX et MAPPÉ les 8 autres** vers un agent métier existant, pour ne pas créer de doublon
(§9, anti-bloat) — d'où 42.

Ce dépôt n'a pas de flotte métier dans `.claude/agents/` : rien vers quoi mapper, donc les 21 rôles y vivent
nativement. Les agents applicatifs d'ici (HERMES, BOUSSOLE, PACTE, RELANCE, COMMANDANT, RÉSOLVEUR…) sont du
**code** dans `lib/agents/`, pas des sous-agents Claude — ils ne sont ni concernés ni touchés.

Même règle des deux côtés, états de départ différents : ce n'est pas une divergence de protocole.

## Rôles délibérément NON créés (§1, anti-bloat)
Négociateur-Fournisseurs · Community-Manager · Vulgarisateur (doublon de Scribe-Empire) · Inspecteur-des-Agents.
