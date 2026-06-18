# PASSATION — Caelum Partners / Nexus-Market

> Document de reprise. Permet à un autre agent (ou à un humain) de reprendre le
> travail sans contexte préalable. Tenu à jour à chaque étape importante.

---

## 1. État général

- **Repo** : `chaima0007/test`
- **Branche de travail** : `claude/nexus-market-agents-63dlku` (NE PAS pousser ailleurs sans accord)
- **Pull Request** : #1 → `main` — https://github.com/chaima0007/TEST/pull/1 (ouverte, pas encore mergée)
- **Stack** : Next.js 16 + TypeScript + Prisma (SQLite via adapter libsql) + Tailwind + next-auth
- **Qualité actuelle** : 33 tests verts · `lint` 0 erreur · `tsc` 0 erreur · `build` OK

### CI / déploiement
- Le seul check rouge est **Vercel** : `Resource is limited - try again in 24 hours` (quota plan gratuit). **Pas un problème de code**, se débloque seul.
- Caelum héberge sur **Cloudflare Pages**, pas Vercel → l'intégration Vercel sur ce repo est résiduelle et peut être **déconnectée** (action compte Vercel, côté Chaima).

---

## 2. Ce qui a été construit (par commit)

| Commit | Contenu |
|---|---|
| `668804c` | Pipeline V1 : state machine 5 étapes + dashboard |
| `79410e0` | Reprise sur panne (`resumeRun`) + tests d'intégration |
| `e8e523e` | Extraction Claude optionnelle (LLM) + correction de 6 erreurs lint préexistantes |
| `97be0b0` | Agents **Conseiller** + **Simulateur de réussite** |
| `c5fb0b2` | Agents d'action **Rédacteur** + **Négociateur** |
| `8fc7da9` | Agent **Auto-pilote** |
| `0063c1c` | Auto-pilote déclenché automatiquement en fin de run |
| `8a21af1` | Agents premium **COMMANDANT** + **RÉSOLVEUR** (+ registre de flotte) |

---

## 3. Architecture du pipeline (matching freelance)

State machine séquentielle, persistée en base (chaque étape lit l'état précédent,
écrit le suivant → run **reprenable** après panne).

```
ingest → filter → match → enrich → notify
                                      └─(fin de run)→ Auto-pilote → Rédacteur+Négociateur
```

Orchestrateur : `lib/pipeline/orchestrator.ts` (`startRun`, `resumeRun`, `STEPS`).

---

## 4. Inventaire des fichiers

### Pipeline (`lib/pipeline/`)
| Fichier | Rôle |
|---|---|
| `orchestrator.ts` | Enchaîne les étapes ; `startRun`/`resumeRun` ; lance l'auto-pilote en fin de run |
| `steps.ts` | Les 5 étapes (ingest/filter/match/enrich/notify) + `defaultDeps` |
| `connectors.ts` | `SourceConnector` + `MockJobBoardConnector` (sources LÉGALES uniquement) |
| `analyzer.ts` | Extracteur heuristique déterministe (budget, compétences, durée, lieu) |
| `llm-analyzer.ts` | Extracteur Claude (`createAnalyzer()` : LLM si `ANTHROPIC_API_KEY`, sinon heuristique) |
| `matcher.ts` | Score de compatibilité offre × profil (logique pure) |
| `settings.ts` | Boucle de rétroaction (seuil budget auto-ajusté) |
| `simulator.ts` | Probabilité de gagner + Monte-Carlo déterministe |
| `advisor.ts` | Conseiller : classe, recommande (heuristique ou Claude) |
| `writer.ts` | Rédacteur + Négociateur : proposition + réponses de suivi |
| `autopilot.ts` | Auto-pilote : prépare les dossiers prioritaires (PRÉPARE seulement) |

### Agents premium / flotte (`lib/agents/`)
| Fichier | Rôle |
|---|---|
| `registry.ts` | Registre des 11 agents (9 + COMMANDANT + RÉSOLVEUR) |
| `commandant.ts` | Décide la stratégie : respect × succès (simulation) × ROI (profit = revenu − coût) |
| `compliance.ts` | Règles dures (« respect ») : pas de scraping, plafond LinkedIn manuel, pas d'encaissement avant inscription légale, base RGPD |
| `resolveur.ts` | Diagnostic + remédiation des frictions (run échoué, taux de réponse faible, déploiement, plan non conforme) |

### API (`app/api/pipeline/`)
- `POST/GET run` — lancer un run / lister les runs
- `GET runs/[id]` — détail d'un run
- `POST runs/[id]/resume` — reprendre un run en échec
- `GET runs/[id]/advice` — Conseiller + Simulateur
- `POST runs/[id]/autopilot` — déclencher l'auto-pilote
- `POST matches/[id]` — valider (approve/reject ; reject « budget » relève le seuil)
- `POST matches/[id]/draft` — préparer le dossier (Rédacteur+Négociateur)

### Dashboard
- `app/dashboard/pipeline/page.tsx` — runs, journal des étapes, panneau Conseil + simulation, propositions (proba/valeur attendue), dossiers, boutons « Préparer le dossier » et « 🚀 Auto-pilote ».

### Base de données (`prisma/schema.prisma`)
Modèles ajoutés : `PipelineRun`, `PipelineStepLog`, `RawJob`, `AnalyzedJob`,
`FreelanceProfile`, `JobMatch` (dont `proposalDraft`, `followupsDraft`), `PipelineSetting`.

---

## 5. Comment lancer / tester

```bash
npm install
npm run db:push            # crée dev.db
npm run db:seed:pipeline   # profils freelance de démo
npm run dev                # → http://localhost:3000/dashboard/pipeline
npm test                   # 33 tests
npm run lint && npx tsc --noEmit && npm run build
```

### Variable d'environnement
- `ANTHROPIC_API_KEY` (optionnelle) : active l'extraction + la rédaction par Claude (`claude-opus-4-8`). **Absente → repli heuristique automatique** (gratuit, hors-ligne). À mettre dans `.env.local`.

---

## 6. Frontière d'autonomie (RÈGLE DE SÉCURITÉ — à respecter par tout agent)

| Les agents font SEULS | Exige une validation HUMAINE |
|---|---|
| Ingestion, filtrage, matching, scoring | **Envoyer un message à un vrai prospect** |
| Simulation, recommandation, classement | **Signer / engager un client** |
| **Préparer** propositions & réponses de suivi | **Encaisser de l'argent** (Stripe non activé) |
| Reprise de run, ajustement de seuil | Toute action irréversible / sortante |

L'auto-pilote **prépare** mais **n'envoie/n'approuve jamais**. Le COMMANDANT
**écarte** les plans non conformes avant toute optimisation.

---

## 7. Décision simulée en cours (objectif : 1er client à 500€)

50 scénarios. Plan « scraping » = meilleur profit brut (380€) mais **ÉCARTÉ**
(CGU LinkedIn + RGPD). Recommandation COMMANDANT = **prospection ciblée + preuve
sociale** : ~56 % de signer, profit attendu ~220€, ROI ~1,83.
→ Traduction opérationnelle : **HERMES en 5 msg/jour très ciblés** + portfolio (FORGE/NEXUS), plutôt que du volume.

---

## 8. Prochaines étapes possibles (pour reprise)

1. **Brancher COMMANDANT → HERMES** : générer les 5 messages LinkedIn ciblés/jour, prêts à envoyer (validation humaine à l'envoi).
2. **Brancher RÉSOLVEUR** sur la surveillance des runs (auto-reprise + alerte).
3. **Connecteur de source réel** (API légale, ToS-compliant) — bloqué sur le choix de la source.
4. **Charte d'autonomie** codifiée (qui fait quoi sans validation) + journal d'audit.
5. **Déconnecter Vercel** / merger la PR #1.

---

## 9. Conventions
- Livrables signés « L'équipe Caelum Partners ».
- Contact : contact@caelumpartners.agency · Site : caelumpartners.agency
- Pas de scraping, pas d'encaissement avant inscription légale, RGPD respecté.
- Construire sur l'existant, ne pas réinventer.
