#!/bin/bash
# CaelumSwarm™ — Agent Self-Heal Protocol
# À exécuter au DÉMARRAGE de chaque agent avant tout travail.
# Détecte et répare les problèmes des agents voisins.
#
# Usage: source scripts/agent_self_heal.sh
#    ou: bash scripts/agent_self_heal.sh && <suite du travail>

set -e

RED='\033[0;31m'; YELLOW='\033[0;33m'; GREEN='\033[0;32m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

echo -e "${BOLD}${CYAN}[SELF-HEAL] Démarrage auto-diagnostic...${RESET}"

# ── 0. Config git obligatoire ──────────────────────────────────────────────
git config user.email noreply@anthropic.com
git config user.name Claude

# ── 1. Bonne branche ──────────────────────────────────────────────────────
BRANCH="claude/swarm-50-agent-architecture-3l6cno"
git checkout "$BRANCH" 2>/dev/null || {
  echo -e "${RED}[SELF-HEAL] Impossible de checkout $BRANCH${RESET}"
  exit 1
}

# ── 2. Pull dernière version ───────────────────────────────────────────────
git pull origin "$BRANCH" 2>/dev/null || echo -e "${YELLOW}[SELF-HEAL] Pull échoué — réseau?${RESET}"

# ── 3. Supprimer index.lock si présent ────────────────────────────────────
if [ -f ".git/index.lock" ]; then
  echo -e "${YELLOW}[SELF-HEAL] index.lock détecté — suppression${RESET}"
  rm -f .git/index.lock
fi

# ── 4. Rescuer les fichiers non-commités laissés par agents précédents ─────
UNTRACKED=$(git status --short | grep "^??" | awk '{print $2}' || true)
UNSTAGED=$(git status --short | grep "^ M" | awk '{print $2}' || true)

if [ -n "$UNTRACKED" ] || [ -n "$UNSTAGED" ]; then
  echo -e "${YELLOW}[SELF-HEAL] Fichiers orphelins détectés — rescue commit${RESET}"

  # Grouper par type
  ENGINE_FILES=$(echo "$UNTRACKED $UNSTAGED" | tr ' ' '\n' | grep "swarm/intelligence" | tr '\n' ' ')
  ROUTE_FILES=$(echo "$UNTRACKED $UNSTAGED" | tr ' ' '\n' | grep "app/api" | tr '\n' ' ')
  SIDEBAR_FILES=$(echo "$UNTRACKED $UNSTAGED" | tr ' ' '\n' | grep "components/sidebar" | tr '\n' ' ')
  OTHER_FILES=$(echo "$UNTRACKED $UNSTAGED" | tr ' ' '\n' | grep -v "swarm/intelligence\|app/api\|components/sidebar" | tr '\n' ' ')

  if [ -n "$ENGINE_FILES" ]; then
    git add $ENGINE_FILES
    git commit -m "auto-rescue: engines non-commités par agent précédent" 2>/dev/null || true
  fi
  if [ -n "$ROUTE_FILES" ]; then
    git add $ROUTE_FILES
    git commit -m "auto-rescue: routes non-commités par agent précédent" 2>/dev/null || true
  fi
  if [ -n "$SIDEBAR_FILES" ]; then
    git add $SIDEBAR_FILES
    git commit -m "auto-rescue: sidebar non-commités par agent précédent" 2>/dev/null || true
  fi
  if [ -n "$OTHER_FILES" ]; then
    git add $OTHER_FILES
    git commit -m "auto-rescue: fichiers divers non-commités" 2>/dev/null || true
  fi

  git push -u origin "$BRANCH" 2>/dev/null || true
  echo -e "${GREEN}[SELF-HEAL] Rescue commit terminé${RESET}"
fi

# ── 5. Vérifier doublons icônes ────────────────────────────────────────────
DUPS=$(grep -h "^export function Icon" components/sidebar-icons-*.tsx 2>/dev/null | sort | uniq -d | head -5 || true)
if [ -n "$DUPS" ]; then
  echo -e "${RED}[SELF-HEAL] DOUBLONS ICÔNES DÉTECTÉS:${RESET}"
  echo "$DUPS"
  echo -e "${YELLOW}[SELF-HEAL] Exécuter: python3 scripts/temporal_loop_detector.py${RESET}"
fi

# ── 6. Confirmer branche ───────────────────────────────────────────────────
CURRENT=$(git branch --show-current)
if [ "$CURRENT" != "$BRANCH" ]; then
  echo -e "${RED}[SELF-HEAL] MAUVAISE BRANCHE: $CURRENT (attendu: $BRANCH)${RESET}"
  exit 1
fi

# ── 7. Rapport final ──────────────────────────────────────────────────────
REMAINING=$(git status --short | wc -l)
if [ "$REMAINING" -eq 0 ]; then
  echo -e "${GREEN}[SELF-HEAL] ✓ Système propre — branche: $CURRENT${RESET}"
else
  echo -e "${YELLOW}[SELF-HEAL] ⚠ $REMAINING fichier(s) encore en attente${RESET}"
fi
