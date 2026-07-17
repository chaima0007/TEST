# Agent Composio — Caelum

Agent qui donne à Claude (Opus 4.8) l'accès à de vrais outils (GitHub, Gmail, Agenda…)
via **Composio** + **Vercel AI SDK**.

> ⚠️ Sécurité : les clés API vivent **uniquement** dans `.env` (jamais dans le code,
> jamais dans un commit). Le fichier `.env` est ignoré par git.

## Mise en route (sur ton ordinateur)

1. **Ouvre un terminal dans ce dossier** (`caelum-composio-agent`).

2. **Installe les dépendances** :
   ```
   npm install @composio/core @composio/vercel ai @ai-sdk/anthropic dotenv tsx
   ```

3. **Configure tes clés** : copie le modèle puis édite-le.
   ```
   copy .env.example .env       (Windows)
   # ou : cp .env.example .env  (Linux/macOS)
   ```
   Ouvre `.env` et colle :
   - `COMPOSIO_API_KEY=` ta clé Composio (dashboard.composio.dev → Manage API Keys)
   - `ANTHROPIC_API_KEY=` ta clé Anthropic (laisse vide si elle est déjà une variable
     d'environnement système).

4. **Lance l'agent** :
   ```
   npm start
   ```
   ou avec ta propre instruction :
   ```
   npm start -- "Crée un événement demain 15h dans mon agenda"
   ```

Les **Logs** du dashboard Composio afficheront les appels d'outils en temps réel.

## Dépannage
- `COMPOSIO_API_KEY manquante` → tu n'as pas créé/copié le `.env`.
- `ANTHROPIC_API_KEY manquante` → colle la clé dans `.env`, ou vérifie la variable
  système avec `echo %ANTHROPIC_API_KEY%` (Windows).
- `claude ... n'est pas reconnu` / `npm ...` → Node.js n'est pas installé ou le
  terminal n'a pas été rouvert après l'installation.
