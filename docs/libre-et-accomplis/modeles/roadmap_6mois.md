# 🗺 Roadmap 6 mois — Libre & Accomplis

> Chaque jalon respecte les règles d'or : rien ne passe au jalon suivant sans
> 100 % de tests verts, 95 % de réussite en simulation, backups vérifiés et
> validation des experts.

## Mois 1 — Fondations

- Mise en place des outils : GitHub, Slack, Notion, Trello, environnements Docker.
- Recrutement prioritaire : CTO, 2 développeurs d'agents, Expert en Santé, Chef de la Validation.
- Base de connaissances centralisée v1 (PostgreSQL + Redis) et orchestrateur squelette (Kafka).
- **KPI de sortie :** CI/CD opérationnelle et bloquante, backup quotidien automatisé.

## Mois 2 — Premiers agents

- Agents Objectifs et Nutrition développés à partir des scaffoldings, testés à 100 % en local.
- Simulations Locust/k6 (1 000 profils variés) → seuil de 95 % atteint.
- Registre de feedbacks experts actif (`gerer_feedback_experts.py`).
- **KPI de sortie :** 2 agents validés par leurs experts, 0 doublon en base.

## Mois 3 — Agents restants + frontend

- Agents Santé, Émotionnel, Cycle Biologique, Social développés et simulés.
- Frontend React Native + Web (parcours onboarding, tableau de bord).
- Traductions FR/EN/ES/DE intégrées et validées (`verifier_traductions.py` en CI).
- **KPI de sortie :** 6 agents à ≥ 95 % en simulation, app utilisable de bout en bout.

## Mois 4 — Alpha interne

- Phase alpha (10–20 utilisateurs internes) selon [`plan_testing_alpha_beta.md`](./plan_testing_alpha_beta.md).
- Restauration de backup à blanc réussie ; durcissement sécurité (pentest interne).
- **KPI de sortie :** 0 bug critique, NPS interne > 40, critères de sortie d'alpha cochés.

## Mois 5 — Bêta externe

- Phase bêta (100–1 000 utilisateurs) : intégrations wearables/paiements, tests de charge.
- Monitoring production complet (Prometheus, Grafana, Sentry, Elasticsearch).
- Ajout des langues NL/IT si la demande le justifie.
- **KPI de sortie :** p95 < 200 ms, taux d'erreur < 0,1 %, NPS > 50.

## Mois 6 — Lancement production

- Checklist de déploiement cochée à 100 % + approbation finale CTO/Chef de Projet.
- Lancement public progressif (10 % → 50 % → 100 % du trafic).
- Rétrospective complète et planification du semestre 2 (entreprises/écoles, programmes bien-être).
- **KPI de sortie :** production stable 4 semaines, 0 perte de données, backups quotidiens verts.
