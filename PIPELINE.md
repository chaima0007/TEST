# Nexus-Market — Pipeline de matching freelance (V1)

## ADR : pourquoi une state machine TypeScript, pas « 50 agents »

**Contexte.** La vision initiale décrivait 50 agents autonomes (scraping LinkedIn,
rotation d'IP, etc.). Deux problèmes : (1) la fiabilité « grade entreprise » vient
du *minimum* de composants observables, pas du *maximum* d'agents ; (2) le scraping
LinkedIn + contournement de blocage est contraire aux CGU et expose au RGPD.

**Décision.** Une **state machine séquentielle en TypeScript** (5 étapes), persistée
dans la base existante (Prisma/SQLite). Un seul runtime, déployable tel quel avec
l'app Next.js. Pas de Python/LangGraph (éviterait un second runtime à déployer).

**Conséquences.** Chaque étape est isolée et testable ; l'état vit en base, donc un
run en échec est *reprenable*. On peut paralléliser/dupliquer plus tard sans réécrire.

## Les 5 étapes

| # | Étape         | Entrée → Sortie                                  | Code |
|---|---------------|--------------------------------------------------|------|
| 1 | Ingestion     | Connecteur de source → `RawJob`                  | `lib/pipeline/steps.ts` · `connectors.ts` |
| 2 | Filtrage      | `RawJob` → `AnalyzedJob` (qualified/rejected)    | `steps.ts` · `analyzer.ts` |
| 3 | Matching      | `AnalyzedJob` × `FreelanceProfile` → `JobMatch`  | `steps.ts` · `matcher.ts` |
| 4 | Enrichissement| `JobMatch` → snippet « pourquoi ça matche »      | `steps.ts` |
| 5 | Notification  | propositions prêtes pour validation humaine      | `steps.ts` |

Orchestration : `lib/pipeline/orchestrator.ts` (`startRun`, `resumeRun`).

## Légal — sources de données

Les connecteurs de **production** doivent utiliser uniquement des sources légales :
APIs officielles, flux publiés, partenariats data. **Pas** de scraping LinkedIn, ni
rotation d'IP, ni contournement de blocage. La V1 ships un `MockJobBoardConnector`
(données fictives) ; tout nouveau connecteur implémente `SourceConnector`.

## Boucle de rétroaction (auto-correction)

Quand l'utilisateur rejette une proposition pour « pas assez cher », l'API relève
automatiquement `minBudgetThreshold` (`PipelineSetting`) ; les futurs runs filtrent
alors les offres trop basses dès l'étape 2. Cf. `app/api/pipeline/matches/[id]/route.ts`.

## Démarrer

```bash
npm install
npm run db:push            # crée/synchronise dev.db
npm run db:seed:pipeline   # insère des profils freelance de démo
npm run dev                # puis ouvrir /dashboard/pipeline
npm test                   # tests unitaires (analyzer + matcher)
```

## Extraction LLM (optionnelle)

L'étape 2 utilise par défaut un extracteur **heuristique** déterministe. Si la
variable d'environnement `ANTHROPIC_API_KEY` est définie, `createAnalyzer()`
bascule automatiquement sur `LLMAnalyzer` (`lib/pipeline/llm-analyzer.ts`), qui
délègue l'extraction à Claude (`claude-opus-4-8`, structured outputs). En cas
d'absence de clé ou d'erreur (réseau, parsing), il **retombe sur l'heuristique** —
aucune casse, aucune dépendance réseau obligatoire.

```bash
export ANTHROPIC_API_KEY=sk-...   # active l'extraction par Claude ; sinon heuristique
```

## Agents Conseiller & Simulateur

- **Simulateur** (`lib/pipeline/simulator.ts`) : probabilité de gagner chaque mission
  + valeur attendue + simulation Monte-Carlo déterministe (revenu médian, p10/p90).
- **Conseiller** (`lib/pipeline/advisor.ts`) : classe les opportunités, désigne la
  priorité, rédige une recommandation. `GET /api/pipeline/runs/[id]/advice`.

## Agents d'action — Rédacteur & Négociateur

Au-delà de l'analyse, les agents peuvent **agir** (la validation reste humaine) :

- **Rédacteur** : rédige une proposition sur-mesure.
- **Négociateur** : prépare les réponses aux questions de suivi du recruteur.

Action : `POST /api/pipeline/matches/[id]/draft` (`lib/pipeline/writer.ts`). Rédaction
par Claude si `ANTHROPIC_API_KEY`, sinon gabarit heuristique. Bouton « Préparer le
dossier » sur chaque proposition du dashboard.

## Agent Auto-pilote

Orchestre Conseiller + Rédacteur + Négociateur : prépare automatiquement le
dossier des opportunités « à viser » (recommandation ≥ niveau, défaut `strong`).
**Ne fait que préparer** — il n'approuve, ne rejette ni n'envoie. `lib/pipeline/autopilot.ts`,
`POST /api/pipeline/runs/[id]/autopilot`, bouton « 🚀 Auto-pilote » dans le dashboard.

## Reprise sur panne

Un run en échec est repris depuis l'étape fautive via `POST /api/pipeline/runs/[id]/resume`
(bouton « Reprendre » dans le dashboard) — cf. `lib/pipeline/orchestrator.ts` (`resumeRun`).

## Extension

- **Vrai LLM à l'étape 2** : déjà branché (`LLMAnalyzer`) ; ou implémenter un autre `Analyzer`.
- **Nouvelle source** : implémenter `SourceConnector` (`lib/pipeline/connectors.ts`) — uniquement des sources légales (APIs officielles/flux), pas de scraping.
- **Scoring** : ajuster `scoreMatch` (`lib/pipeline/matcher.ts`) — couvert par les tests.
