# Collab-IA : Claude × Mistral avec double contrôle

Système où **Claude propose** une solution et **Mistral la vérifie** (double contrôle),
avec journaux structurés, gestion d'erreurs, et connecteurs prêts pour GitHub et
Google Workspace.

## Démarrage rapide

```bash
# 1. Définir les clés (Windows, cmd)
setx ANTHROPIC_API_KEY "sk-ant-votre_cle"
setx MISTRAL_API_KEY "votre_cle_mistral"
# (puis fermer/rouvrir le terminal)

# 2. Lancer
python main.py
```

> Le cœur ne nécessite **aucune installation** (uniquement la bibliothèque standard Python).

## Structure

```
collab-ia/
├── main.py                 # point d'entrée
├── core/
│   ├── config.py           # lecture des clés/paramètres
│   ├── logging.py          # journaux JSON
│   └── retry.py            # reprises sur erreur (backoff)
├── llm/
│   ├── base.py             # interface commune
│   ├── claude.py           # client Anthropic
│   ├── mistral.py          # client Mistral
│   └── verifier.py         # logique du double contrôle
├── orchestrator/
│   └── orchestrator.py     # chef d'orchestre + journaux
├── integrations/
│   ├── github.py           # connecteur GitHub (à compléter)
│   └── google.py           # connecteur Google Workspace (à compléter)
└── tasks/
    └── example_task.py     # exemple de tâche
```

## Comment ça marche

1. Une **tâche** (texte) est envoyée à l'orchestrateur.
2. Le **proposeur** (Claude) génère une solution.
3. Le **vérificateur** (Mistral) contrôle et rend un verdict APPROUVÉ / REJETÉ.
4. Si approuvé, l'orchestrateur peut déclencher une **action** (GitHub, Drive...).
5. Chaque étape est **journalisée** (audit).

## Prochaines étapes

- [ ] Ajouter une file de tâches + planificateur (APScheduler) pour le 24/7
- [ ] Implémenter le connecteur GitHub (PyGithub)
- [ ] Implémenter le connecteur Google Workspace
- [ ] Déployer sur Railway / Render pour un fonctionnement permanent
- [ ] Ajouter alertes (email/Slack) et tableau de bord

## Sécurité

- Les clés se lisent depuis l'environnement, **jamais dans le code**.
- `.env` et fichiers de clés sont ignorés par Git (`.gitignore`).
- Permissions minimales par intégration.
- En production : utiliser un gestionnaire de secrets (Vault, Secret Manager).
