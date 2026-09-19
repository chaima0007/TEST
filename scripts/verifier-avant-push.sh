#!/usr/bin/env bash
# PROTECTION AVANT PUSH — ce dépôt est PUBLIC (🔴 ERR-015, incident du 2026-09-19).
# Cherche dans les fichiers INDEXÉS et dans le MESSAGE DE COMMIT préparé (si fourni)
# ce qui n'a rien à faire sur un dépôt public : secrets, e-mails perso, téléphones belges,
# dates de naissance, adresses postales, numéros de registre national.
# Usage :  bash scripts/verifier-avant-push.sh [fichier-message-de-commit]
# Sortie : 0 = rien trouvé · 1 = à relire AVANT de pousser (ne bloque pas : signale, §5).
set -u
msg="${1:-}"
pat='(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY'
pat+='|[A-Za-z0-9._%+-]+@(gmail|hotmail|outlook|yahoo|proton)\.[a-z]+'
pat+='|\+32 ?[0-9]{1,3}[ ./]?[0-9]{2,3}[ ./]?[0-9]{2}[ ./]?[0-9]{2}|\b0[1-9][0-9]{1,2}[ ./]?[0-9]{2}[ ./]?[0-9]{2}[ ./]?[0-9]{2}\b'
pat+='|\b(né|née|naissance)[^\n]{0,20}[0-9]{2}/[0-9]{2}/[0-9]{4}|\b[0-9]{2}\.[0-9]{2}\.[0-9]{2}-[0-9]{3}\.[0-9]{2}\b'
pat+='|\b(rue|avenue|boulevard|bd|chaussée|place)\b[^\n|]{2,40}\b[0-9]{1,4}\b[^\n|]{0,15}\b1[0-9]{3}\b)'
found=0
echo "── fichiers indexés ──"
if git diff --cached -U0 | grep -v '^+++' | grep -E '^\+' | grep -inE "$pat" ; then found=1; else echo "   rien"; fi
if [ -n "$msg" ] && [ -f "$msg" ]; then
  echo "── message de commit ──"
  if grep -inE "$pat" "$msg"; then found=1; else echo "   rien"; fi
fi
if [ "$found" = 1 ]; then
  echo; echo "⚠️  À RELIRE avant de pousser : un message de commit ne se retire pas (R-002)."; exit 1
fi
echo "✓ rien de personnel ni de secret détecté (ce n'est pas une garantie, c'est un filet)"
