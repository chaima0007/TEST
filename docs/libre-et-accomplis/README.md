# 📜 Libre & Accomplis – Système Ultime

Documentation du système « Libre & Accomplis » : une application autonome, multilingue,
pilotée par des agents IA testés à 95–100 % en local, validés par des experts, et
déployée uniquement après 100 % de tests réussis.

## Contenu

| Fichier | Description |
|---------|-------------|
| [`SYSTEME_ULTIME.md`](./SYSTEME_ULTIME.md) | Document maître : vision, équipes, rôles, processus, architecture, règles d'or. |
| [`CHECKLIST_DEPLOIEMENT.md`](./CHECKLIST_DEPLOIEMENT.md) | Checklist à cocher avant chaque déploiement. |
| [`scripts/backup.sh`](./scripts/backup.sh) | Script de sauvegarde automatique (local + Drive + Cloud), avec contrôle d'espace disque, vérification d'intégrité et alertes Slack. |
| [`scripts/verifier_traductions.py`](./scripts/verifier_traductions.py) | Vérifie que toutes les clés sont traduites dans chaque langue (utilisable en CI). |
| [`scripts/gerer_feedback_experts.py`](./scripts/gerer_feedback_experts.py) | CLI de gestion des feedbacks d'experts : ajout, liste par expert, rappels (CSV importable dans Airtable). |
| [`exemples/ci-cd-pipeline.yml`](./exemples/ci-cd-pipeline.yml) | Exemple de pipeline CI/CD (GitHub Actions) avec job sécurité et déploiement conditionnel — modèle à adapter, non activé. |
| [`scaffolding/python/`](./scaffolding/python/) | Agents Nutrition + Santé et base de connaissances en Python, avec tests unitaires exécutables. |
| [`scaffolding/nodejs/`](./scaffolding/nodejs/) | Agents Nutrition + Objectifs en Node.js (ESM + `node:test`). |
| [`traductions/messages.json`](./traductions/messages.json) | Fichier de traduction multilingue (FR, EN, ES, DE). |
| [`modeles/feedback-expert.md`](./modeles/feedback-expert.md) | Modèle de feedback/correction d'expert. |
| [`modeles/feedback_experts.csv`](./modeles/feedback_experts.csv) | Registre des feedbacks (Agent, Action, Statut, Expert, Priorité) — importable dans Airtable. |
| [`modeles/resolution-conflit.md`](./modeles/resolution-conflit.md) | Modèle de résolution de conflit (médiation diplomatique). |
| [`modeles/plan_testing_alpha_beta.md`](./modeles/plan_testing_alpha_beta.md) | Plan détaillé des phases alpha (interne) et bêta (externe), avec critères de sortie. |
| [`modeles/roadmap_6mois.md`](./modeles/roadmap_6mois.md) | Roadmap sur 6 mois avec jalons et KPIs de sortie. |
| [`modeles/fiche_poste_cto.md`](./modeles/fiche_poste_cto.md) | Fiche de poste pour recruter le CTO. |
| [`modeles/fiche_poste_expert_sante.md`](./modeles/fiche_poste_expert_sante.md) | Fiche de poste pour recruter un Expert en Santé. |

## Lancer les tests des scaffoldings

```bash
# Python (4 tests)
python3 -m unittest discover docs/libre-et-accomplis/scaffolding/python -v

# Node.js (4 tests)
node --test docs/libre-et-accomplis/scaffolding/nodejs/*.test.mjs

# Validation multilingue
python3 docs/libre-et-accomplis/scripts/verifier_traductions.py
```

## Règles d'or (résumé)

1. 🚫 Pas de déploiement sans 100 % de tests réussis.
2. 💾 Toujours sauvegarder en local + Drive + Cloud.
3. 👨‍🔬 Toute modification doit être validée par un expert.
4. 🌍 Communication diplomatique et multilingue.
5. 🤖 Agents à 95 % de réussite en simulation avant intégration.
6. 📝 Toute action doit être documentée.
7. 🔒 Données sensibles chiffrées (AES-256).
8. 📊 Performances monitorées (Prometheus + Grafana).
