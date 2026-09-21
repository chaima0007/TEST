#!/usr/bin/env bash
# ─── CONTRÔLE DES REGISTRES — ce que `audit-codex.sh` ne regarde pas ─────────
#
# FRONTIÈRE, à lire avant d'ajouter quoi que ce soit ici (2026-09-21) :
#
#   `scripts/audit-codex.sh` possède le rituel §5 — état serveur, écart
#   branches/main, correctifs réellement en vigueur, ID en double, structure
#   §12, fraîcheur d'ETAT.md, décisions qui dorment.
#
#   CE fichier possède les défauts qui arrivent à l'ÉCRITURE d'un fichier :
#   marqueurs de conflit, références orphelines, rétrécissement d'un registre,
#   donnée personnelle sur un dépôt public. Trois d'entre eux sont passés à
#   travers `git status`, la CI verte ET la relecture humaine.
#
#   Les deux scripts ont failli faire doublon : le contrôle « ID en double »
#   écrit ici le 2026-09-20 existait déjà dans `audit-codex.sh`, écrit la
#   veille par une autre session. Il a été RETIRÉ d'ici. Avant d'ajouter un
#   contrôle, ouvrir l'autre fichier — c'est la règle §1 « ne jamais
#   réinventer un rôle existant », appliquée aux scripts.
#
# Usage :  bash scripts/verifier-registres.sh
# Sortie :  0 = tout va bien · 1 = au moins un contrôle a échoué.

set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1

REG="🔴 ERREURS.md"
echec=0
ko() { echo "❌ $*" >&2; echec=1; }
ok() { echo "✅ $*"; }

# Deux conventions de numérotation coexistent, et c'est assumé (TRANCHÉ PAR
# CHAIMA le 2026-09-19) : `ERR-001`…`ERR-021` séquentiels, puis `ERR-AAAAMMJJ-HHMM`
# horodatés. Tout motif qui ne reconnaît qu'une des deux est un contrôle aveugle.
ID='ERR-([0-9]{8}-[0-9]{4}|[0-9]{3})([^0-9-]|$)'
# Motif strict : soit `ERR-` + 3 chiffres, soit `ERR-` + date + `-` + heure.
# `ERR-[0-9]{3,8}` attrapait aussi une date nue (« ERR-20260914 »).

# Identifiants cités comme EXEMPLES DE FORMAT, qui ne désignent aucune entrée.
# Les exclure explicitement plutôt que d'élargir le motif : une liste courte et
# nommée se relit, un motif permissif rend le contrôle aveugle.
ILLUSTRATIFS='ERR-20260914-2147|ERR-20260919-1340'

# ── 1. Marqueurs de conflit git commités (ERR-20260919-1259) ─────────────────
# Le 2026-09-19, des marqueurs sont partis sur le dépôt distant : `git status`
# était propre, la CI verte. C'est un agent, hors de son mandat, qui les a vus.
if git grep -lE '^(<<<<<<< |>>>>>>> |=======$)' -- '*.md' '*.ts' '*.tsx' '*.json' '*.yml' 2>/dev/null | grep -q .; then
  ko "Marqueurs de conflit git dans des fichiers suivis :"
  git grep -lE '^(<<<<<<< |>>>>>>> )' -- '*.md' '*.ts' '*.tsx' '*.json' '*.yml' | sed 's/^/     /' >&2
else
  ok "Aucun marqueur de conflit dans les fichiers suivis."
fi

# ── 2. Références orphelines (ERR-20260919-1316) ─────────────────────────────
# Sept entrées ont disparu dans un merge en laissant trois fichiers qui les
# citaient. Un renvoi vers une page arrachée ne se voit pas à la relecture.
presentes=$(grep -oE "^## $ID" "$REG" 2>/dev/null | grep -oE 'ERR-([0-9]{8}-[0-9]{4}|[0-9]{3})' | sort -u)
orphelines=""
for ref in $(git grep -hoE "$ID" -- '*.md' 2>/dev/null | grep -oE 'ERR-([0-9]{8}-[0-9]{4}|[0-9]{3})' | sort -u | grep -vE "^($ILLUSTRATIFS)$"); do
  echo "$presentes" | grep -qx "$ref" || orphelines="$orphelines $ref"
done
if [ -n "$orphelines" ]; then
  ko "Références à des entrées qui n'existent pas :$orphelines"
else
  ok "Aucune référence orpheline."
fi

# ── 3. Le registre ne doit jamais rétrécir (ERR-20260919-1316) ───────────────
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

# ── 4. Données personnelles dans un fichier versionné (ERR-20260919-1324) ────
# Ce dépôt est PUBLIC. Seul le FAIT DÉCISIONNEL entre dans un fichier versionné,
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
