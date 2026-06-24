#!/usr/bin/env bash
# setup-hooks.sh — Active les hooks git versionnés (à lancer une fois par clone)
# Usage : bash scripts/setup-hooks.sh
set -e
git config core.hooksPath .githooks
chmod +x .githooks/* 2>/dev/null || true
echo "✅ Hooks git activés (core.hooksPath=.githooks)"
echo "   pre-push : garde anti-collision de branche (protocole §15)"
