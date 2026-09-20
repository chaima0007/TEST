#!/usr/bin/env bash
# Contrôle des registres — ferme les préventions d'ERR-026, ERR-027, ERR-029 et ERR-030.
#
# Pourquoi ce fichier existe : ces quatre erreurs ont la même forme. Un défaut est passé
# à travers `git status`, la CI et la relecture humaine, parce qu'aucun outil ne le
# cherchait. « Un angle sans organe de détection est un angle mort permanent, pas un
# oubli » (méta-leçon 14). Voici l'organe.
#
# Usage :  bash scripts/verifier-registres.sh
# Sortie :  0 = tout va bien · 1 = au moins un contrôle a échoué.

set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1

REG="🔴 ERREURS.md"
echec=0
ko() { echo "❌ $*" >&2; echec=1; }
ok() { echo "✅ $*"; }

# ── 1. Marqueurs de conflit git commités (ERR-027) ─────────────────────────────
# Le 2026-09-19, des marqueurs sont partis sur le dépôt distant : `git status` était
# propre, la CI verte. C'est un agent, hors de son mandat, qui les a vus.
if git grep -lE '^(<<<<<<< |>>>>>>> |=======$)' -- '*.md' '*.ts' '*.tsx' '*.json' '*.yml' 2>/dev/null | grep -q .; then
  ko "Marqueurs de conflit git dans des fichiers suivis :"
  git grep -lE '^(<<<<<<< |>>>>>>> )' -- '*.md' '*.ts' '*.tsx' '*.json' '*.yml' | sed 's/^/     /' >&2
else
  ok "Aucun marqueur de conflit dans les fichiers suivis."
fi

# ── 2. Numéros d'erreur en double (ERR-026) ────────────────────────────────────
# Trois collisions en 48 h : le numéro est un compteur partagé sans verrou.
doublons=$(grep -oE '^## ERR-[0-9]{3}' "$REG" 2>/dev/null | sort | uniq -d)
if [ -n "$doublons" ]; then
  ko "Numéros d'erreur en double dans $REG :"; echo "$doublons" | sed 's/^/     /' >&2
else
  ok "Aucun numéro d'erreur en double."
fi

# ── 3. Références orphelines (ERR-029) ─────────────────────────────────────────
# Sept entrées ont disparu dans un merge en laissant trois fichiers qui les citaient.
presentes=$(grep -oE '^## ERR-[0-9]{3}' "$REG" 2>/dev/null | grep -oE 'ERR-[0-9]{3}' | sort -u)
orphelines=""
# `ERR-[0-9]+` puis filtre sur 3 chiffres exactement : sinon `ERR-20260914-2147`
# (identifiant horodaté cité en exemple dans ERR-026) est lu comme « ERR-202 ».
for ref in $(git grep -hoE 'ERR-[0-9]+' -- '*.md' 2>/dev/null | grep -E '^ERR-[0-9]{3}$' | sort -u); do
  echo "$presentes" | grep -qx "$ref" || orphelines="$orphelines $ref"
done
if [ -n "$orphelines" ]; then
  ko "Références à des entrées qui n'existent pas :$orphelines"
else
  ok "Aucune référence orpheline."
fi

# ── 4. Le registre ne doit jamais rétrécir (ERR-029) ───────────────────────────
# Une fusion en union protège du conflit, pas de la disparition silencieuse.
ici=$(grep -c '^## ERR-' "$REG" 2>/dev/null || echo 0)
if git rev-parse --verify --quiet origin/main >/dev/null 2>&1; then
  ref=$(git show origin/main:"$REG" 2>/dev/null | grep -c '^## ERR-' || echo 0)
  if [ "$ici" -lt "$ref" ]; then
    ko "Le registre a RÉTRÉCI : $ici entrées ici contre $ref sur origin/main. Des entrées ont disparu."
  else
    ok "Registre : $ici entrées (origin/main : $ref) — aucune perte."
  fi
else
  ok "Registre : $ici entrées (origin/main indisponible, comparaison ignorée)."
fi

# ── 5. Données personnelles dans un fichier versionné (ERR-030) ────────────────
# Ce dépôt est public. Seul le FAIT DÉCISIONNEL entre dans un fichier versionné,
# jamais la source personnelle : ni adresse, ni date de naissance.
motifs='[Nn]ée? le [0-9]{1,2}/[0-9]{1,2}/(19|20)[0-9]{2}|(^|[^0-9])(rue|Rue|avenue|Avenue|boulevard|Boulevard|[Bb]d) [A-ZÉÈ][a-zé]+ [0-9]{1,4}'
if git grep -nIE "$motifs" -- '*.md' 2>/dev/null | grep -v 'scripts/verifier-registres.sh' | grep -q .; then
  ko "Donnée personnelle possible dans un fichier versionné (dépôt PUBLIC) :"
  git grep -nIE "$motifs" -- '*.md' | grep -v 'scripts/verifier-registres.sh' | cut -c1-160 | sed 's/^/     /' >&2
else
  ok "Aucune donnée personnelle détectée dans les fichiers suivis."
fi

echo
[ "$echec" -eq 0 ] && echo "Registres : tous les contrôles passent." || echo "Registres : AU MOINS UN CONTRÔLE A ÉCHOUÉ."
exit "$echec"
