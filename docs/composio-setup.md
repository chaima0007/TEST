# GUIDE COMPOSIO — CAELUM PARTNERS
Généré le 2026-06-22 08:25
=================================

## ÉTAPE 1 — Créer un compte Composio
  → composio.dev/signup (gratuit, pas de carte bancaire)
  → Choisir plan "Free" (100 actions/mois offertes)

## ÉTAPE 2 — Installer le SDK Python
  → pip install composio-core composio-openai

## ÉTAPE 3 — Authentification
  → composio login
  → Copier l'API key depuis le dashboard

## ÉTAPE 4 — Connecter Gmail
  → composio add gmail
  → Autoriser l'accès OAuth Google
  → Tester : composio actions --app gmail

## ÉTAPE 5 — Connecter Google Calendar
  → composio add googlecalendar
  → Autoriser l'accès OAuth
  → Tester : composio actions --app googlecalendar

## ÉTAPE 6 — Variables d'environnement
  → export COMPOSIO_API_KEY=your_key_here
  → Ajouter dans .env.local (JAMAIS committer ce fichier)

## ÉTAPE 7 — Tester avec les agents Caelum
  → python3 scripts/composio-email-agent.py
  → python3 scripts/composio-calendar-agent.py
  → python3 scripts/composio-workflow-agent.py

---

## INTÉGRATIONS DISPONIBLES VIA COMPOSIO

  ✓ Gmail — lecture/envoi/recherche emails
  ✓ Google Calendar — création/modification événements
  ✓ Outlook / Office 365 — alternative Microsoft
  ✓ Slack — notifications équipe
  ✓ Notion — documentation
  ✓ Linear / Jira — gestion de tâches
  ✓ HubSpot CRM — suivi prospects
  ✓ LinkedIn — prospection B2B

---

## PLAN CAELUM RECOMMANDÉ

  Phase 1 (maintenant)  : Gmail + Google Calendar
  Phase 2 (Q3 2026)     : Slack équipe + Notion docs
  Phase 3 (Q4 2026)     : HubSpot CRM prospects CSDDD

---

## SCRIPTS DISPONIBLES

  scripts/composio-email-agent.py     — Envoi d'emails (candidatures, prospection)
  scripts/composio-calendar-agent.py  — Gestion du calendrier + export .ics
  scripts/composio-setup-guide.py     — Ce guide (génère aussi ce fichier .md)
  scripts/composio-workflow-agent.py  — Workflows automatisés email + calendrier

---

## VÉRIFICATION RAPIDE DE L'INSTALLATION

```bash
# Vérifier que la clé est présente
echo $COMPOSIO_API_KEY

# Vérifier les apps connectées
composio apps connected

# Tester une action Gmail
composio actions --app gmail --query "send email"

# Tester une action Google Calendar
composio actions --app googlecalendar --query "create event"
```

---

## EN CAS DE PROBLÈME

  Erreur OAuth       → composio logout && composio login
  App non connectée  → composio add gmail (refaire l'autorisation)
  SDK introuvable    → pip install --upgrade composio-core composio-openai
  Quota dépassé      → vérifier plan sur composio.dev/dashboard

---

## SÉCURITÉ

  ✗ Ne jamais committer COMPOSIO_API_KEY dans le code source
  ✗ Ne jamais inclure la clé dans les logs ou prints
  ✓ Utiliser .env.local (ajouté dans .gitignore)
  ✓ Faire tourner les agents en local uniquement
  ✓ Renouveler la clé si compromission suspectée

---

Contact : retrouvetonsmile@gmail.com
Caelum Partners SPRL — Bruxelles, Belgique
