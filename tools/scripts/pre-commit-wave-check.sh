#!/usr/bin/env bash
# pre-commit-wave-check.sh — Caelum Partners Wave Safety Hook
# Install: cp tools/scripts/pre-commit-wave-check.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

set -euo pipefail

ERRORS=0

# ── 1. Check branch ──────────────────────────────────────────────────────────
BRANCH=$(git branch --show-current)
REQUIRED="claude/swarm-50-agent-architecture-3l6cno"
if [ "$BRANCH" != "$REQUIRED" ]; then
  echo "⚠️  WARNING: committing on '$BRANCH' (expected '$REQUIRED')"
  echo "   If this is intentional (feature branch), ignore this warning."
fi

# ── 2. Check Sidebar.tsx for duplicate Icon functions ─────────────────────────
if git diff --cached --name-only | grep -q "components/Sidebar.tsx"; then
  DUPS=$(grep "^function Icon" components/Sidebar.tsx | awk -F'[{ ]' '{print $3}' | sort | uniq -d)
  if [ -n "$DUPS" ]; then
    echo "❌ ERROR: Duplicate Icon functions in components/Sidebar.tsx:"
    echo "$DUPS" | sed 's/^/   - /'
    echo ""
    echo "   Fix: remove the EARLIER occurrence of each duplicate, keep the latest."
    echo "   Check: grep -n \"^function IconXxx\" components/Sidebar.tsx"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ Sidebar.tsx: no duplicate Icon functions"
  fi
fi

# ── 3. Check for untracked files ─────────────────────────────────────────────
UNTRACKED=$(git ls-files --others --exclude-standard)
if [ -n "$UNTRACKED" ]; then
  echo "⚠️  WARNING: Untracked files will NOT be included in this commit:"
  echo "$UNTRACKED" | sed 's/^/   ?? /'
  echo "   Add them with: git add <file>"
fi

# ── 4. Validate Python engines being committed ───────────────────────────────
ENGINES=$(git diff --cached --name-only | grep "swarm/intelligence/.*\.py$" || true)
if [ -n "$ENGINES" ]; then
  for ENGINE in $ENGINES; do
    if [ -f "$ENGINE" ]; then
      if ! python3 -c "import ast; ast.parse(open('$ENGINE').read())" 2>/dev/null; then
        echo "❌ ERROR: Syntax error in $ENGINE"
        ERRORS=$((ERRORS + 1))
      else
        echo "✅ $ENGINE: Python syntax OK"
      fi
    fi
  done
fi

# ── 5. Validate security pattern in API routes ───────────────────────────────
ROUTES=$(git diff --cached --name-only | grep "app/api/.*/route\.ts$" || true)
if [ -n "$ROUTES" ]; then
  for ROUTE in $ROUTES; do
    if [ -f "$ROUTE" ]; then
      MISSING=""
      grep -q "sealResponse" "$ROUTE"          || MISSING="$MISSING sealResponse"
      grep -q "SWARM_API_URL" "$ROUTE"         || MISSING="$MISSING SWARM_API_URL-guard"
      grep -q "revalidate: 30" "$ROUTE"        || MISSING="$MISSING revalidate:30"
      grep -q "status: 502" "$ROUTE"           || MISSING="$MISSING 502-fallback"
      if [ -n "$MISSING" ]; then
        echo "❌ ERROR: $ROUTE missing security patterns:$MISSING"
        ERRORS=$((ERRORS + 1))
      else
        echo "✅ $ROUTE: security pattern OK"
      fi
    fi
  done
fi

# ── Result ───────────────────────────────────────────────────────────────────
if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "❌ Pre-commit check FAILED with $ERRORS error(s). Fix them before committing."
  exit 1
fi

echo ""
echo "✅ All pre-commit checks passed."
exit 0
