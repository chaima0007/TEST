#!/usr/bin/env bash
# ===========================================================================
# Netlify "ignore" command — économise les crédits de build.
#
# Netlify exécute ce script avant chaque build :
#   - code retour 0  => build ANNULÉ (rien à redéployer)
#   - code retour 1  => build LANCÉ
#
# Règle : on ne reconstruit le site QUE si un fichier réellement déployé a
# changé (app/, components/, lib/, public/, prisma/, config de build…).
# Les commits qui ne touchent que swarm/ (moteurs Python), scripts/, data/,
# docs/ ou *.md ne déclenchent AUCUN build → zéro crédit consommé.
# ===========================================================================
set -u  # PAS de pipefail : grep -q ferme le tube tôt (SIGPIPE) et fausserait le code retour

BASE="${CACHED_COMMIT_REF:-}"
HEAD="${COMMIT_REF:-HEAD}"

# Liste des fichiers modifiés depuis le dernier déploiement réussi.
if [ -n "$BASE" ]; then
  changed=$(git diff --name-only "$BASE" "$HEAD" 2>/dev/null)
else
  changed=$(git diff --name-only HEAD~1 HEAD 2>/dev/null)
fi

# Sécurité : si on ne sait pas ce qui a changé, on construit (exit 1).
if [ -z "$changed" ]; then
  echo "Aucun diff détecté — build par sécurité."
  exit 1
fi

# Chemins qui exigent un rebuild du site déployé.
DEPLOY_PATTERN='^(app/|components/|lib/|public/|prisma/|styles/|src/|package\.json|package-lock\.json|next\.config|netlify\.toml|tsconfig|postcss|tailwind|middleware|\.env)'

if grep -qE "$DEPLOY_PATTERN" <<< "$changed"; then
  echo "Fichiers du site modifiés → BUILD lancé :"
  grep -E "$DEPLOY_PATTERN" <<< "$changed" | head
  exit 1
fi

echo "Seuls backend/scripts/docs modifiés → BUILD ANNULÉ (économie de crédits)."
head <<< "$changed"
exit 0
