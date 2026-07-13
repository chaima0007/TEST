# 📌 Plan de Testing Alpha/Bêta — Libre & Accomplis

## 🎯 Objectifs

- **Alpha** : valider la stabilité du système avec 10–20 utilisateurs internes.
- **Bêta** : tester à grande échelle avec 100–1 000 utilisateurs externes.

**Prérequis d'entrée en alpha** (règles d'or) : 100 % de tests unitaires verts,
95 % de réussite en simulation pour chaque agent, backups vérifiés, validation
de chaque agent par son expert dédié.

---

## 📅 Phase Alpha (2 semaines, 10–20 utilisateurs internes)

| Tâche | Responsable | Critères de réussite | Outils |
|-------|-------------|----------------------|--------|
| Tester l'Agent Objectifs | Équipe QA | 100 % des micro-objectifs générés et suivis correctement | Cypress, Jest, `scaffolding/nodejs` |
| Tester l'Agent Santé | Expert en Santé | 0 erreur dans les conseils (sommeil, exercices) | Tests manuels, `scaffolding/python` |
| Tester l'Agent Nutrition | Expert en Santé | 0 recette contenant un allergène déclaré | Tests manuels + simulations |
| Valider les backups | Spécialiste Backup | 100 % des données récupérables après restauration à blanc | `scripts/backup.sh` |
| Vérifier les notifications | Équipe Développement | 100 % des alertes Slack reçues (échec et succès) | Slack, AWS SNS |
| Vérifier les traductions | Experts en Langues | 0 clé manquante/vide dans les 4 langues | `scripts/verifier_traductions.py` |

**Critères de sortie d'alpha :**
- 0 bug critique ouvert ; bugs majeurs < 3 et planifiés.
- Tous les feedbacks experts au statut ✅ dans `modeles/feedback_experts.csv`.
- Une restauration complète de backup réalisée avec succès.

---

## 📅 Phase Bêta (4 semaines, 100–1 000 utilisateurs externes)

| Tâche | Responsable | Critères de réussite | Outils |
|-------|-------------|----------------------|--------|
| Tester les intégrations (wearables, paiements) | Ingénieur Intégration | 0 échec d'intégration | Postman, Kafka |
| Valider les traductions en conditions réelles | Experts en Langues | 100 % des clés traduites, 0 signalement de contresens | `scripts/verifier_traductions.py`, feedbacks |
| Mesurer les performances | Analyste QA | Temps de réponse < 200 ms au p95 sous charge | k6, Prometheus, Grafana |
| Test de charge | Spécialiste en Simulation | 1 000 utilisateurs simultanés sans dégradation | Locust, k6 |
| Recueillir les feedbacks utilisateurs | Médiateur Diplomatique | NPS > 50, taux de réponse > 30 % | SurveyMonkey, Typeform |
| Surveiller les erreurs en continu | Ingénieur DevOps | Taux d'erreur < 0,1 % des requêtes | Sentry, Elasticsearch |

**Critères de sortie de bêta (go/no-go production) :**
- Checklist de déploiement ([`CHECKLIST_DEPLOIEMENT.md`](../CHECKLIST_DEPLOIEMENT.md)) cochée à 100 %.
- 95 % de réussite en simulation confirmée sur les données réelles de la bêta.
- Approbation finale CTO/Chef de Projet.

---

## 🔄 Boucle de correction (pendant les deux phases)

1. Bug/erreur signalé (utilisateur, expert ou monitoring).
2. Feedback consigné via `scripts/gerer_feedback_experts.py ajouter …`.
3. Correction en local + re-test (100 % vert) + re-simulation (95 %).
4. Re-validation par l'expert → statut ✅.
5. Backup + documentation avant tout redéploiement.
