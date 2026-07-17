# Revue de code — configuration

Ce dépôt est configuré avec deux workflows GitHub Actions.

## 1. `CI` (`.github/workflows/ci.yml`)

S'exécute sur chaque **pull request vers `main`** et sur chaque **push sur `main`**.
Étapes : `npm ci` → `prisma generate` → **lint** (ESLint) → **build** (Next.js) → **typecheck** (TypeScript).

Aucun secret requis.

## 2. `Claude Code Review` (`.github/workflows/claude-code-review.yml`)

S'exécute à l'**ouverture** et à chaque **mise à jour** d'une pull request.
Claude relit le diff et poste des commentaires inline (bugs, sécurité, conventions, qualité).

### Prérequis : secret `ANTHROPIC_API_KEY`

1. Créer une clé API sur https://console.anthropic.com/
2. Dans le dépôt GitHub : **Settings → Secrets and variables → Actions → New repository secret**
3. Nom : `ANTHROPIC_API_KEY` — Valeur : la clé

Sans ce secret, le job de revue échoue (la CI ci-dessus continue de fonctionner).
La revue est automatiquement ignorée sur les PR provenant de forks (la clé n'y est pas exposée).
