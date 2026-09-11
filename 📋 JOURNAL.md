# 📋 JOURNAL — TEST / Nexus-Market

> Snapshots §5. Règle anti-bruit : rien changé → une ligne « aucun changement ». Un événement réel = une entrée datée.

---

SNAPSHOT 2026-09-11 13h42 CEST : état réel `8391052` (poussé sur `claude/nexus-market-agents-63dlku`). **Avancée (hors Vercel, sur demande de Chaima)** : HERMES est désormais **branché dans l'app** — route API `POST /api/hermes/draft` (sans état, aucune persistance, aucun envoi) + page `/dashboard/prospection` (formulaire prospect → 4 brouillons copiables, garde-fou humain visible §10) + entrée sidebar « PROSPECTION (CAELUM) ». Vitest couvre aussi `app/**/__tests__` (+5 tests de route). VÉRIFIÉ : lint 0 err, tsc 0 (post-build), 44/44 tests, `next build` OK. Note Next 16 : `PageProps` (type global auto-généré) n'existe qu'après `next build` — tsc seul échoue tant que `.next/types` est absent ; c'est un artefact, pas un vrai défaut (cf. AGENTS.md).

SNAPSHOT 2026-09-11 13h31 CEST : état réel `ae13c0b` (local = remote), structure §12 en place (21 agents). **Avancée (hors Vercel, sur demande de Chaima)** : agent **HERMES** — rédacteur de brouillons de prospection LinkedIn (note de connexion + variante A/B + 1er message + relance) pour l'offre « site web premium » 500€. Envoi manuel uniquement, aucune automatisation/scraping (§3/§10). Heuristique + Claude optionnel (repli). `lib/agents/hermes.ts` + tests. VÉRIFIÉ : 39/39 tests, lint 0, tsc 0 sur hermes.

SNAPSHOT 2026-09-06 23h12 CEST : **Installation du PROTOCOLE CODEX (v2026-09-06)** dans le projet.
- CLAUDE.md : bloc protocole intégral collé en tête + spécificités projet (§15.4).
- Structure §12 créée : `/codex/{candidates,expertise,opportunites,licences-sortantes}`, `A-DECIDER.md`, `EVOLUTION.md`, `📋 JOURNAL.md`, `🔴 ERREURS.md`.
- `.claude/agents/` : 21 agents générés **dérivés du §1** (NON VÉRIFIÉ comme set canonique) + `.claude/skills/debat/`.
- État réel (git ls-remote) au moment du snapshot : `0d84e42` sur `claude/nexus-market-agents-63dlku`.
- Décision en attente consignée dans `/codex/A-DECIDER.md` : réconcilier les agents avec le set canonique de l'Empire s'il existe ; nettoyer les projets Vercel.
