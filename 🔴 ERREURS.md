# 🔴 ERREURS — chaima0007/TEST

Erreurs et pièges constatés (VÉRIFIÉ = reproduit dans ce dépôt). Une entrée = un événement réel.

- **2026-09-06 — Horloges décalées (VÉRIFIÉ)** : l'horloge du conteneur et celle du Drive ont
  affiché des dates de juillet 2026 alors que la date réelle était le 2026-09-06. Conséquence :
  des fichiers Drive et des commits portent des dates trompeuses. Règle : dater manuellement
  chaque document avec la date fournie par le système, jamais l'horloge locale seule.
- **2026-09-06 — Connecteur Google Drive : pas d'édition (VÉRIFIÉ)** : impossible de modifier
  un Google Doc existant via le connecteur. Règle : créer un document « — partie N » ; deux
  fichiers ne couvrent jamais les mêmes actions.
- **2026-09-06 — Connecteurs claude.ai non autorisés (VÉRIFIÉ)** : Canva,
  Cloudflare_Developer_Platform et composio demandent une autorisation OAuth que seule Chaima
  peut donner (claude.ai → Paramètres → Connecteurs). Inutilisables d'ici là — voir
  /codex/A-DECIDER.md.
- **2026-09-06 — Conteneur éphémère (VÉRIFIÉ)** : le conteneur de session est re-provisionné
  entre les sessions ; tout travail non poussé sur la branche est perdu. Règle : commit + push
  sur la branche désignée avant toute fin de tâche.
