# /codex/A-DECIDER.md — le seul fichier à ouvrir

> Trié par ancienneté, le plus vieux en haut. > 14 jours = mis en évidence.
> Une ligne ne disparaît que lorsque Chaima a tranché (jamais parce qu'elle a vieilli).

| Quoi | Projet | Type | En attente depuis | Résumé en 1 ligne |
|---|---|---|---|---|
| Nettoyer les projets Vercel liés au repo | TEST | Financier/Technique | 2026-07-17 | 8 projets déploient ce repo → quota saturé ; déconnecter les superflus (Caelum = Cloudflare Pages). Action compte Vercel (§10). |
| Réconcilier `.claude/agents/` avec le set canonique | TEST | Technique/Protocole | 2026-09-06 | Les 21 agents sont dérivés du §1 (NON VÉRIFIÉ comme officiels) ; les remplacer par le set canonique de l'Empire s'il existe. **Chaima 2026-09-11 : « laisser en l'état », à rouvrir si un besoin concret apparaît.** Ligne maintenue : la décision a été prise sur une description périmée (« ce dépôt n'a pas d'agents ») alors que `.claude/agents/` existe désormais — à reconfirmer. |
| Merger la PR #1 (pipeline + agents Nexus-Market) | TEST | Engagement | 2026-06-18 | Check pertinent (`test`) vert ; merge = décision humaine (§10). |
| Fournir `ANTHROPIC_API_KEY` (chemin LLM) | TEST | Technique | 2026-07-17 | Extraction/rédaction Claude codées mais NON VÉRIFIÉES ; seul le repli heuristique est prouvé. **Volet CI retiré le 2026-09-11** : la revue auto des PR est désactivée (ERR-010 close), le secret n'est plus requis pour que le gate soit propre — il reste requis pour le chemin LLM applicatif. |
| Statut CompeteIQ | CompeteIQ | Produit | 2026-07 | EN PAUSE (marché dominé) ; réveil lié à Caelum — pas de développement sans décision (intégré depuis `main`). Pause reconfirmée par Chaima le 2026-09-11. |
| Définir l'ICP cible + fournir la liste de prospects | Caelum/TEST | Marché/Humain | 2026-09-11 | Route/UI HERMES livrées (`/dashboard/prospection`) ; reste à définir QUI cibler et à fournir 5–10 prospects réels (l'envoi reste manuel, §10). Liste annoncée par Chaima pour la prochaine session. |
| Définir les modalités de facturation réelles (statut + paiement) | Caelum/TEST | Légal/Financier | 2026-09-11 | PACTE laisse les modalités « À CONFIRMER » ; un devis ne peut pas être envoyé/signé tant que le statut légal et le moyen de règlement (virement/facture) ne sont pas tranchés (§10/§11). |

---
## Décisions tranchées (consignées)
- **2026-09-11** — **Revue automatique des PR désactivée** : faute du secret `ANTHROPIC_API_KEY`, le check finissait en `failure` sur chaque PR (ERR-010). Workflow `claude-code-review` rendu inerte (`workflow_dispatch` seul, déclencheur `pull_request` commenté), procédure de réactivation en tête de fichier. Mesure temporaire, levée dès que la clé est posée. **TRANCHÉ PAR CHAIMA.**
- **2026-09-11** — **Conflit de gouvernance PR #1 ↔ PR #8** : version **Nexus-Market/Caelum canonique**, décisions de `main` intégrées (EVOLUTION en union). **TRANCHÉ PAR CHAIMA.**
- **2026-09-11** — **Installation CODEX sur ce dépôt** : « protocole + structure d'abord », sans créer d'agents (côté `main`/CompeteIQ). **TRANCHÉ PAR CHAIMA.**
- **2026-07-17** — **Landing CompeteIQ** (hébergée dans keywordmoneymaker) passée en « en développement — non disponible ». **TRANCHÉ PAR CHAIMA.**
