#!/bin/bash
# CaelumSwarm™ QA Watchdog v2 — contrôle automatique
BRANCH="claude/swarm-50-agent-architecture-3l6cno"
ROOT="/home/user/TEST"
ERRORS=0

ok()  { echo "  ✓ $*"; }
err() { echo "  ✗ $*"; ERRORS=$((ERRORS+1)); }

echo "=== QA Watchdog — $(date '+%H:%M:%S') ==="
cd "$ROOT"

# 1. Branche
CURRENT=$(git branch --show-current 2>/dev/null || echo "unknown")
[ "$CURRENT" = "$BRANCH" ] && ok "Branche correcte" || err "Mauvaise branche: $CURRENT"

# 2. Arbre propre
STATUS=$(git status --short 2>/dev/null | wc -l)
[ "$STATUS" -eq 0 ] && ok "Working tree propre" || err "$STATUS fichier(s) non-commités/modifiés"

# 3. Commits non-vérifiés
BAD=$(git log "origin/$BRANCH..HEAD" --format="%ae" 2>/dev/null | grep -cv "noreply@anthropic.com" || true)
[ "$BAD" -eq 0 ] && ok "Tous les commits vérifiés" || err "$BAD commit(s) avec mauvais email"

# 4. Doublons icônes
DUPES=$(grep "^export function Icon" components/sidebar-icons-{1,2,3,4}.tsx 2>/dev/null | \
  awk -F: '{print $2}' | awk '{print $3}' | sort | uniq -d | wc -l)
[ "$DUPES" -eq 0 ] && ok "Aucun doublon d'icône" || err "$DUPES doublon(s) icônes sidebar"

# 5. Sécurité routes API
ROUTES=$(ls app/api/*/route.ts 2>/dev/null | wc -l)
BAD_SEAL=$(grep -rL "sealResponse" app/api/*/route.ts 2>/dev/null | wc -l)
BAD_GUARD=$(grep -rL "SWARM_API_URL" app/api/*/route.ts 2>/dev/null | wc -l)
BAD_502=$(grep -rL "status: 502" app/api/*/route.ts 2>/dev/null | wc -l)
ok "$ROUTES routes API détectées"
[ "$BAD_SEAL" -eq 0 ]  && ok "sealResponse partout"      || err "$BAD_SEAL route(s) sans sealResponse"
[ "$BAD_GUARD" -eq 0 ] && ok "SWARM_API_URL guard OK"    || err "$BAD_GUARD route(s) sans guard"
[ "$BAD_502" -eq 0 ]   && ok "Fallback 502 partout"      || err "$BAD_502 route(s) sans fallback 502"

# 6. Structure sidebar
grep -q "function NavContent" components/Sidebar.tsx 2>/dev/null && \
  ok "NavContent dans Sidebar.tsx" || err "NavContent absent de Sidebar.tsx"
! grep -q "function NavContent" components/sidebar-nav.tsx 2>/dev/null && \
  ok "sidebar-nav.tsx propre" || err "NavContent encore dans sidebar-nav.tsx"
BARREL=$(wc -l < components/sidebar-icons.tsx 2>/dev/null || echo 999)
[ "$BARREL" -le 15 ] && ok "sidebar-icons.tsx barrel ($BARREL lignes)" || \
  err "sidebar-icons.tsx trop grand ($BARREL lignes)"

# 7. 5 derniers engines
echo "  — engines (5 derniers):"
for f in $(ls -t swarm/intelligence/*_engine.py 2>/dev/null | head -5); do
  AVG=$(python3 "$f" 2>/dev/null | awk '/avg_composite:/{print $2}')
  [ "$AVG" = "61.03" ] && echo "    ✓ $(basename $f)" || { echo "    ✗ $(basename $f): avg=$AVG"; ERRORS=$((ERRORS+1)); }
done

# Résumé
echo ""
[ "$ERRORS" -eq 0 ] && echo "✅ QA PASSED" || echo "❌ QA FAILED — $ERRORS erreur(s)"
exit $ERRORS
