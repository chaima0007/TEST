#!/bin/sh
# Active les hooks versionnés (.githooks) — à lancer UNE fois par clone.
# Décision volontaire : un hook exécute du code à chaque commit (battement de la
# plateforme autonome + gardiens qualité). C'est pourquoi l'activation est manuelle.
#
#   sh scripts/install_hooks.sh
#
git config core.hooksPath .githooks
chmod +x .githooks/* 2>/dev/null || true
echo "✅ Hooks activés (core.hooksPath=.githooks)."
echo "   La plateforme battra le cœur à chaque commit (voix 🗣️ + signes vitaux)."
echo "   Pour désactiver : git config --unset core.hooksPath"
