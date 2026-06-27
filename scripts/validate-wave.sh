#!/usr/bin/env bash
# Agent [92] — Caelum Partners Auto-Repair & Prediction Engine
# Exécuté automatiquement après chaque wave pour détecter et corriger les erreurs avant le push

set -e
ERRORS=0
FIXED=0
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}  ✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}  ⚠${NC} $1"; }
log_err()  { echo -e "${RED}  ✗${NC} $1"; ERRORS=$((ERRORS+1)); }
log_fix()  { echo -e "${BLUE}  →${NC} $1"; FIXED=$((FIXED+1)); }

echo -e "\n${BLUE}═══════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Agent [92] — Caelum Validation & Prediction  ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════${NC}\n"

# ─── CHECK 1 : Branche correcte ─────────────────────────────────
echo "[ CHECK 1 ] Branche de travail"
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "claude/swarm-50-agent-architecture-3l6cno" ]; then
  log_ok "Branche : $BRANCH"
else
  log_err "Mauvaise branche : $BRANCH (attendu: claude/swarm-50-agent-architecture-3l6cno)"
fi

# ─── CHECK 2 : Fichiers non-tracés ──────────────────────────────
echo "[ CHECK 2 ] Fichiers non-committés"
UNTRACKED=$(git status --short | grep "^??" | wc -l)
MODIFIED=$(git status --short | grep "^ M\|^M " | wc -l)
if [ "$UNTRACKED" -eq 0 ] && [ "$MODIFIED" -eq 0 ]; then
  log_ok "Working tree propre"
else
  log_err "$UNTRACKED fichier(s) non-tracé(s), $MODIFIED modifié(s) non-stagé(s)"
  git status --short
fi

# ─── CHECK 3 : entity_id dans les routes récentes ────────────────
echo "[ CHECK 3 ] Détection entity_id → id (routes)"
ENTITY_ID_FILES=$(git diff HEAD~3..HEAD --name-only 2>/dev/null | grep "app/api.*route\.ts" || true)
BAD_ENTITY=0
for f in $ENTITY_ID_FILES; do
  if [ -f "$f" ] && grep -q "entity_id:" "$f" 2>/dev/null; then
    log_warn "entity_id détecté dans $f — correction automatique"
    sed -i 's/entity_id:/id:/g' "$f"
    log_fix "Corrigé : $f"
    BAD_ENTITY=$((BAD_ENTITY+1))
  fi
done
if [ "$BAD_ENTITY" -eq 0 ]; then
  log_ok "Aucun entity_id dans les routes récentes"
fi

# ─── CHECK 4 : Virgules parasites ────────────────────────────────
echo "[ CHECK 4 ] Virgules parasites en début de ligne"
BAD_COMMA=$(grep -rln "^," app/api/ 2>/dev/null | wc -l)
if [ "$BAD_COMMA" -gt 0 ]; then
  log_warn "$BAD_COMMA fichier(s) avec virgule parasite — correction automatique"
  for f in $(grep -rln "^," app/api/ 2>/dev/null); do
    sed -i 's/^,\(\s*\)/\1/' "$f"
    log_fix "Corrigé : $f"
  done
else
  log_ok "Aucune virgule parasite détectée"
fi

# ─── CHECK 5 : "use client" dans les dashboards ──────────────────
echo "[ CHECK 5 ] Directive 'use client' dans les dashboards"
DASH_FILES=$(git diff HEAD~3..HEAD --name-only 2>/dev/null | grep "app/dashboard.*page\.tsx" || true)
BAD_CLIENT=0
for f in $DASH_FILES; do
  if [ -f "$f" ]; then
    FIRST_LINE=$(head -1 "$f")
    if [ "$FIRST_LINE" != '"use client"' ]; then
      log_err "'use client' manquant en ligne 1 dans $f"
      BAD_CLIENT=$((BAD_CLIENT+1))
    fi
  fi
done
if [ "$BAD_CLIENT" -eq 0 ] && [ -n "$DASH_FILES" ]; then
  log_ok "Tous les dashboards ont 'use client'"
elif [ -z "$DASH_FILES" ]; then
  log_ok "Aucun dashboard dans cette wave"
fi

# ─── CHECK 6 : Doublons dans Sidebar.tsx ─────────────────────────
echo "[ CHECK 6 ] Doublons d'icônes dans Sidebar.tsx"
DUPLICATES=$(grep "^function Icon" components/Sidebar.tsx | awk -F'[{ ]' '{print $3}' | sort | uniq -d)
if [ -z "$DUPLICATES" ]; then
  log_ok "Aucun doublon d'icône dans Sidebar.tsx"
else
  log_err "Doublons détectés dans Sidebar.tsx : $DUPLICATES"
fi

# ─── CHECK 7 : Pattern sealResponse dans les routes récentes ─────
echo "[ CHECK 7 ] Pattern sealResponse (conformité sécurité)"
BAD_SEAL=0
for f in $ENTITY_ID_FILES; do
  if [ -f "$f" ]; then
    if ! grep -q "sealResponse" "$f" 2>/dev/null; then
      log_err "sealResponse manquant dans $f"
      BAD_SEAL=$((BAD_SEAL+1))
    fi
    if ! grep -q "SWARM_API_URL" "$f" 2>/dev/null; then
      log_err "SWARM_API_URL guard manquant dans $f"
      BAD_SEAL=$((BAD_SEAL+1))
    fi
    if ! grep -q "revalidate: 30" "$f" 2>/dev/null; then
      log_warn "revalidate:30 manquant dans $f"
    fi
    if grep -q "status: 503" "$f" 2>/dev/null; then
      log_err "503 détecté dans $f (doit être 502)"
      sed -i 's/status: 503/status: 502/g' "$f"
      log_fix "503 → 502 corrigé dans $f"
    fi
  fi
done
if [ "$BAD_SEAL" -eq 0 ]; then
  log_ok "Pattern sécurité conforme sur les routes récentes"
fi

# ─── CHECK 8 : GaugeRing SVG dans les dashboards ─────────────────
echo "[ CHECK 8 ] GaugeRing pattern (r=36 cx=44 cy=44)"
BAD_GAUGE=0
for f in $DASH_FILES; do
  if [ -f "$f" ]; then
    if ! grep -q "r = 36" "$f" 2>/dev/null; then
      log_warn "GaugeRing r=36 non trouvé dans $f"
      BAD_GAUGE=$((BAD_GAUGE+1))
    fi
  fi
done
if [ "$BAD_GAUGE" -eq 0 ] && [ -n "$DASH_FILES" ]; then
  log_ok "GaugeRing pattern conforme"
fi

# ─── RÉSUMÉ ──────────────────────────────────────────────────────
echo ""
echo -e "${BLUE}═══════════════════ RÉSUMÉ ═══════════════════${NC}"
if [ "$ERRORS" -eq 0 ]; then
  echo -e "${GREEN}  ✓ Validation RÉUSSIE — $FIXED correction(s) auto-appliquée(s)${NC}"
  echo -e "${GREEN}  → Prêt pour git push${NC}"
else
  echo -e "${RED}  ✗ $ERRORS erreur(s) critique(s) — corriger avant push${NC}"
  if [ "$FIXED" -gt 0 ]; then
    echo -e "${YELLOW}  → $FIXED correction(s) auto-appliquée(s) — re-stage et commit${NC}"
  fi
  exit 1
fi
echo -e "${BLUE}═══════════════════════════════════════════════${NC}\n"
