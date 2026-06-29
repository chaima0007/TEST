#!/usr/bin/env bash
# PreToolUse gate (P-INTEGRITE-ENVIRONNEMENT / §24).
# Bloque toute écriture si l'environnement est désynchronisé (checkout étranger,
# mauvaise branche, dossiers clés manquants). Lit le JSON du hook sur stdin (ignoré).
#
# Sortie :
#   - environnement sain  -> rien, exit 0 (l'écriture est autorisée)
#   - désync détectée     -> JSON permissionDecision=deny, exit 0 (écriture bloquée)
set -u
DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cat >/dev/null 2>&1 || true   # consommer le stdin du hook
if python3 "$DIR/scripts/env_integrity_check.py" >/dev/null 2>&1; then
  exit 0
fi
raison="Désynchronisation de l'environnement détectée (env_integrity_check). Écriture BLOQUÉE : checkout possiblement positionné sur un autre projet / mauvaise branche / dossiers clés manquants. Action : git fetch puis réaligner (git reset --hard origin/claude/swarm-50-agent-architecture-3l6cno) SUR AUTORISATION avant toute écriture. Ne jamais commiter depuis un checkout étranger (§24)."
printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$raison"
exit 0
