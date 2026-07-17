# 00 — INDEX DU DRIVE — Caelum
> À lire en premier. Sommaire de tout ce que contient le dossier d'audit.
> Mis à jour : 2026-07-17 · Tenu par : l'assistant (rôle orchestrateur) · Pour : Chaima + les agents.

## À quoi sert ce document
C'est le **sommaire** du dossier « 📓 Caelum — Journal de Bord & Audits » (Drive) et de ce dossier `AUDIT/` (repo).
Chaque travail effectué y est listé avec un **titre propre + un synopsis complet**, pour que Chaima (et n'importe quelle future session/agent) sache d'un coup d'œil ce qui existe, ce que chaque document contient, et quand s'en servir. **Aucun doublon** (voir protocole).

## Protocole anti-doublon (les 4 règles, à respecter par tous)
1. **1 projet = 1 dossier.** Caelum ici. « La Loi Avec Moi » = dossier séparé. Jamais mélangés.
2. **1 seul REGISTRE MAÎTRE par projet** = source unique de vérité. On vérifie ICI avant de créer.
3. **Journal daté : on n'écrase jamais.** Chaque session = un nouveau fichier `AAAA-MM-JJ`.
4. **Nommage strict** : `AAAA-MM-JJ — Titre` (ou préfixe `00` pour l'index). Le tri se fait tout seul.

## Audit des travaux — contenu du dossier

| # | Document | Type | MAJ | Synopsis |
|---|----------|------|-----|----------|
| 1 | **REGISTRE MAÎTRE — Agents Caelum** (`REGISTRE_MAITRE.md`) | Registre permanent | 2026-07-13 | Liste complète des 97 agents en 13 blocs. Par agent : n°, fichier .py, rôle, statut (actif / non branché). À utiliser AVANT de créer un agent. ⚠️ 93-97 non branchés dans lancer.py. |
| 2 | **2026-07-13 — Audit de session** (`2026-07-13_session.md`) | Journal daté (ne pas écraser) | 2026-07-13 | Compte rendu du 13/07 : historique git réel (19→21/06), actions, anomalies (93-97 ; escalade « 304 agents » à ignorer), prochaine action = trouver le 1er client. |
| 3 | **GUIDE — Corriger l'erreur SSL 525** (`GUIDE_525_SSL.md`) | Guide pratique | 2026-07-17 | Procédure réversible pour réparer le 525. Cas A GitHub Pages (DNS only → cert → Enforce HTTPS → proxy), Cas B Worker/Pages (Custom Domain). Se fait dans les dashboards, pas dans le code. |

## Comment ajouter un nouveau travail (pour rester propre)
1. Vérifier dans cet index + le REGISTRE MAÎTRE que ça n'existe pas déjà (anti-doublon).
2. Titre propre au format `AAAA-MM-JJ — Titre clair`.
3. Ajouter ici une ligne : titre + type + date + synopsis complet.
4. Ne jamais écraser un journal daté existant : on en crée un nouveau.

> **Note honnête** : ce sont les sessions Claude (rôle orchestrateur) qui tiennent ce dossier à jour, pas les scripts Python tout seuls. Les agents `.py` sont des outils que Chaima lance ; le rangement du Drive est fait ici, à chaque session, selon ce protocole.
