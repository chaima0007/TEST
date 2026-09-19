#!/usr/bin/env bash
# ─── AUDIT CODEX — le rituel §5 rendu exécutable ─────────────────────────────
#
# Répond en quelques secondes à « est-ce que tout va bien ? », par des mesures
# et non de mémoire. Aucune écriture, aucun réseau sortant hors `git fetch`.
#
#   bash scripts/audit-codex.sh
#
# Né d'ERR-020/021/022 : trois erreurs où une vérification de dix secondes
# aurait évité des jours de travail invisible. Un audit qu'on refait à la main
# est un audit qu'on oublie de refaire.

set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1

KO=0
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
ko()   { printf '  \033[31m✗\033[0m %s\n' "$1"; KO=$((KO+1)); }
info() { printf '  · %s\n' "$1"; }
titre(){ printf '\n\033[1m%s\033[0m\n' "$1"; }

# ── 0. L'état serveur, jamais la mémoire (règle du git fetch, ERR-020) ───────
titre "0. ÉTAT SERVEUR"
git fetch origin --prune --quiet 2>/dev/null || { echo "  fetch impossible — audit interrompu"; exit 2; }
MAIN=$(git rev-parse origin/main)
info "origin/main = $(git rev-parse --short origin/main) — $(git log -1 --format='%s' origin/main | cut -c1-60)"
info "dernier commit : $(git log -1 --format='%cd' --date=short origin/main)"

# ── 1. Travail poussé mais pas livré (ERR-022) ───────────────────────────────
titre "1. ÉCART BRANCHES ↔ MAIN  — « pourquoi rien n'a changé ? »"
EN_ATTENTE=0; ETRANGERES=0
while read -r ref; do
  b=${ref#origin/}
  [ "$b" = "main" ] && continue
  ahead=$(git rev-list --count "$MAIN..$ref")
  [ "$ahead" -eq 0 ] && continue
  # on ne signale que les branches actives : touchées dans les 14 derniers jours
  age=$(( ( $(date +%s) - $(git log -1 --format=%ct "$ref") ) / 86400 ))
  [ "$age" -gt 14 ] && continue
  behind=$(git rev-list --count "$ref..$MAIN")
  # Une branche dont l'historique diverge de plus de 100 commits n'est pas du
  # travail en attente : c'est un projet étranger hébergé dans ce dépôt (voir
  # A-DECIDER, « sortir les projets étrangers »). La compter gonflerait le
  # total et noierait le signal — l'erreur du premier audit des branches.
  if [ "$ahead" -gt 100 ]; then
    printf '  · %-46s historique étranger (%d commits) — hors périmètre\n' "$b" "$ahead"
    ETRANGERES=$((ETRANGERES+1)); continue
  fi
  printf '  · %-46s %2d commit(s) en attente de merge, retard %d (%dj)\n' "$b" "$ahead" "$behind" "$age"
  EN_ATTENTE=$((EN_ATTENTE+ahead))
done < <(git for-each-ref --format='%(refname:short)' refs/remotes/origin | grep -v HEAD)
[ "$ETRANGERES" -gt 0 ] && info "$ETRANGERES branche(s) de projets étrangers exclues du total (§ A-DECIDER)"
if [ "$EN_ATTENTE" -eq 0 ]; then ok "rien en attente : tout le travail récent est sur main"
else info "TOTAL $EN_ATTENTE commit(s) hors de main. Le merge est humain (§10) — un agent ne peut pas le faire."; fi

# ── 2. Chaque correctif annoncé est-il EN VIGUEUR sur main ? (ERR-021) ───────
titre "2. CORRECTIFS EN VIGUEUR SUR MAIN"
# Format : ERR|libellé|fichier[|motif grep dans ce fichier]
while IFS='|' read -r err libelle fichier motif; do
  [ -z "${err:-}" ] && continue
  if [ -n "${motif:-}" ]; then
    if git show "origin/main:$fichier" 2>/dev/null | grep -q -- "$motif"; then ok "$err  $libelle"; else ko "$err  $libelle  → absent de main"; fi
  else
    if git cat-file -e "origin/main:$fichier" 2>/dev/null; then ok "$err  $libelle"; else ko "$err  $libelle  → absent de main"; fi
  fi
done <<'TABLE'
ERR-001|client Prisma généré au postinstall|package.json|prisma generate
ERR-010|revue auto des PR non bloquante|.github/workflows/claude-code-review.yml|workflow_dispatch
ERR-015|données de prospection gitignorées|.gitignore|prospects
ERR-016|garde-fou anti-survente|lib/agents/garde-fou.ts|
ERR-018|règle du découpage obligatoire|AGENTS.md|codex-regle-decoupage
ERR-020|règle du git fetch d'ouverture|AGENTS.md|codex-regle-fetch
TABLE
info "un ✗ ici = le correctif est ÉCRIT quelque part, mais ne protège personne"

# ── 3. Intégrité du registre d'erreurs ───────────────────────────────────────
titre "3. REGISTRE D'ERREURS"
REG="🔴 ERREURS.md"
if [ -f "$REG" ]; then
  n=$(grep -cE '^## ERR-[0-9]+' "$REG")
  dup=$(grep -oE '^## ERR-[0-9]+' "$REG" | sort | uniq -d)
  [ -z "$dup" ] && ok "$n entrées, aucun ID en double" || ko "ID en double : $(echo "$dup" | tr '\n' ' ')"
  # une entrée sans correctif est une entrée inachevée
  sans=$(awk '/^## ERR-/{if(t&&!c)print t; t=$0; c=0} /^- \*\*Correctif/{c=1} END{if(t&&!c)print t}' "$REG" | grep -oE 'ERR-[0-9]+' | tr '\n' ' ')
  [ -z "$sans" ] && ok "chaque entrée porte un correctif" || ko "sans ligne Correctif : $sans"
else ko "$REG introuvable"; fi

# ── 4. Structure §12 ─────────────────────────────────────────────────────────
titre "4. STRUCTURE §12"
manque=""
for f in "CLAUDE.md" "🔴 ERREURS.md" "📋 JOURNAL.md" "codex/A-DECIDER.md" "codex/EVOLUTION.md" \
         "codex/candidates" "codex/expertise" "codex/opportunites" "codex/licences-sortantes" ".claude/agents" ".claude/skills/debat"; do
  [ -e "$f" ] || manque="$manque $f"
done
[ -z "$manque" ] && ok "structure complète" || ko "manque :$manque"
n21=0
for r in scout guardian-licences sentinel-securite architecte-integration avocat contradicteur \
         simulateur-scenarios arbitre-expert verificateur-verite superviseur-vigie cartographe \
         scribe-empire eclaireur-opportunites gardien-donnees intendant-couts conservateur-secrets \
         testeur-adverse avocat-du-client croque-mort responsable-continuite archiviste-preuves; do
  [ -f ".claude/agents/$r.md" ] && n21=$((n21+1))
done
[ "$n21" -eq 21 ] && ok "les 21 rôles du §1 sont présents ($(ls .claude/agents/*.md 2>/dev/null | wc -l) agents au total)" \
                  || ko "seulement $n21 des 21 rôles du §1"

# ── 5. Cohérence entre fichiers d'instruction (§5) ───────────────────────────
titre "5. COHÉRENCE DES FICHIERS D'INSTRUCTION"
dev_claude=$(grep -oE 'branche de dev :\*\* `[^`]+`' CLAUDE.md 2>/dev/null | grep -oE '`[^`]+`' | tr -d '`')
if [ -n "$dev_claude" ] && grep -q "n'est plus la branche de travail" ETAT.md 2>/dev/null \
   && grep -q "$dev_claude" ETAT.md 2>/dev/null; then
  ko "CLAUDE.md désigne « $dev_claude » comme branche de dev, ETAT.md dit qu'elle ne l'est plus"
else ok "CLAUDE.md et ETAT.md s'accordent sur la branche de dev"; fi

# ── 6. Décisions qui dorment (§6 : > 14 jours) ───────────────────────────────
titre "6. DÉCISIONS EN ATTENTE (§6)"
if [ -f codex/A-DECIDER.md ]; then
  total=$(awk '/^\| /{n++} END{print n-1}' codex/A-DECIDER.md)
  vieilles=$(grep -oE '\| 20[0-9]{2}-[0-9]{2}-[0-9]{2} \|' codex/A-DECIDER.md | grep -oE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' \
    | while read -r d; do
        j=$(( ( $(date +%s) - $(date -d "$d" +%s 2>/dev/null || echo "$(date +%s)") ) / 86400 ))
        [ "$j" -gt 14 ] && echo "$d ($j j)"
      done)
  info "$total ligne(s) en attente de ta décision"
  [ -z "$vieilles" ] && ok "aucune ne dort depuis plus de 14 jours" \
                     || ko "> 14 jours (§6 : à remonter en tête) : $(echo "$vieilles" | tr '\n' ' ')"
else ko "codex/A-DECIDER.md introuvable"; fi

# ── Verdict ──────────────────────────────────────────────────────────────────
titre "VERDICT"
if [ "$KO" -eq 0 ]; then printf '  \033[32mTout est cohérent.\033[0m\n'; else printf '  \033[31m%d point(s) à traiter ci-dessus.\033[0m\n' "$KO"; fi
[ "$EN_ATTENTE" -gt 0 ] && printf '  \033[33m%d commit(s) attendent un merge humain (§10) — rien d'"'"'eux n'"'"'est en vigueur.\033[0m\n' "$EN_ATTENTE"
exit 0
