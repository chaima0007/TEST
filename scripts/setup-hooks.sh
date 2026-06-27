#!/usr/bin/env bash
# setup-hooks.sh — exécuté au démarrage de session (hook SessionStart).
# 1) Active les hooks git versionnés.
# 2) AUTO-SYNCHRONISE la branche de travail sur le remote, pour corriger
#    automatiquement le démarrage figé du conteneur (il boote sur un ancien
#    instantané et ne tire pas la dernière version tout seul).
#
# Tout est rendu NON bloquant : aucune erreur ici ne doit empêcher la session.

# --- 1. Hooks git ---
git config core.hooksPath .githooks 2>/dev/null || true
chmod +x .githooks/* 2>/dev/null || true
echo "✅ Hooks git activés (core.hooksPath=.githooks)"
echo "   pre-commit : gardiens build + cohérence (avant chaque commit)"
echo "   pre-push   : garde anti-collision de branche (protocole §15)"

# --- 2. Auto-sync de la branche de travail ---
BRANCHE="claude/swarm-50-agent-architecture-3l6cno"

auto_sync() {
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 || return 0

  local actuelle
  actuelle="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
  [ "$actuelle" = "$BRANCHE" ] || return 0   # ne touche qu'à NOTRE branche

  # Ne pas écraser un travail non commité : on ne synchronise que si propre.
  if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    echo "ℹ️  Auto-sync ignoré : modifications locales non commitées présentes."
    return 0
  fi

  local i
  for i in 1 2 3; do
    git fetch origin "$BRANCHE" >/dev/null 2>&1 && break
    sleep $((i * 2))
  done

  local local_sha remote_sha
  local_sha="$(git rev-parse HEAD 2>/dev/null)"
  remote_sha="$(git rev-parse "origin/$BRANCHE" 2>/dev/null)"
  [ -n "$remote_sha" ] || { echo "ℹ️  Auto-sync : remote injoignable, on continue."; return 0; }

  if [ "$local_sha" = "$remote_sha" ]; then
    echo "✅ Auto-sync : déjà à jour ($local_sha)."
    return 0
  fi

  if git merge --ff-only "origin/$BRANCHE" >/dev/null 2>&1; then
    echo "✅ Auto-sync : remis à jour $local_sha → $(git rev-parse --short HEAD) (zéro perte)."
  else
    echo "⚠️  Auto-sync : ff-only impossible (divergence). Intervention manuelle requise."
  fi
}

auto_sync || true

exit 0
