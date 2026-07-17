# 00 — LIRE D'ABORD

## SYNOPSIS
Point d'entrée de passation du dépôt **« Nous »** (app couple locale de Chaima).
Lis ce fichier, puis `ETAT.md` (journal daté), puis le dernier rapport dans
`reports/`. Objectif du projet : aider à comprendre les limites de l'autre et
mieux communiquer (humeur, cycle, sensibilités), en local-first.

_Dernière mise à jour : 2026-07-17 21h35 (Europe/Brussels) — Claude Code._

---

## Ce qu'est le projet
- App **mobile-first, local-first** (Next.js 16 / React 19 / Tailwind v4).
- Données **dans le navigateur** (localStorage) — aucun serveur, aucun compte.
- Données de démo **fictives uniquement** (partenaire « Alex »).
- Contenu fondé sur des approches reconnues (CNV, Gottman, FRIES), sans invention.

## Où travailler
- **Branche de dev :** `claude/couples-app-mvp-chaima-fx3dya` (ne jamais pousser
  ailleurs sans accord).
- **Lancer :** `npm install && npm run dev` → http://localhost:3000
- **Vérifier :** `npm run lint && npm run build && npm run typecheck`

## Carte du dépôt
- `app/` — écrans : `page.tsx` (Aujourd'hui), `reperes/`, `rituels/`, `reglages/`.
- `lib/` — logique & contenu : `store.tsx`, `seed.ts`, `content.ts`,
  `rituals.ts`, `nvc.ts`, `cycle.ts`, `types.ts`, `date.ts`.
- `components/` — `BottomNav.tsx`, `ui.tsx`.
- `.claude/agents/` — panel d'agents orchestrateurs (produit-ux,
  relation-communication, securite-privacy, critique-produit).
- `.claude/workflows/panel-couple.js` — orchestration d'audit + backlog.
- `reports/` — rapports de livraison horodatés (un fichier = un événement).

## Protocole de livraison (obligatoire)
1. Date/heure réelle via `TZ="Europe/Brussels" date`.
2. Audit honnête **FAIT / VÉRIFIÉ (preuve) / RESTE** — ne rien déclarer fini sans preuve.
3. Chaque rapport commence par un **SYNOPSIS**, titre `AAAA-MM-JJ-HHhMM — auteur — sujet`.
4. Copie du rapport dans le Drive « COMPILATION & SYNOPSIS — Empire Chaima »
   (id `1qXUj9D9r7HSmIMzMcsScz4Ynlv4auP4G`) ; sinon dans `reports/`.
5. Mettre à jour `ETAT.md` (ajout daté, jamais d'écrasement).

## État actuel (résumé)
MVP **fait et vérifié**, poussé (commit `fb85fa6`). Panel d'agents créé.
Orchestration **pas encore lancée**. Détail → `ETAT.md` + dernier rapport.
