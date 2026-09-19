#!/usr/bin/env bash
# Génère codex/atlas/memoire/atlas-memoire.Modelfile : le profil Ollama qui donne à l'IA LOCALE
# de Chaima la mémoire du projet. À relancer à chaque rafale, après mise à jour de l'état.
# Pont provisoire vers la couche 4 (RAG) : tant que le RAG n'est pas installé, c'est ceci qui
# fait que l'IA locale « sait » où en est le projet.
set -euo pipefail
cd "$(dirname "$0")/.."
out=codex/atlas/memoire/atlas-memoire.Modelfile
{
cat <<'HEAD'
FROM qwen2.5:3b
PARAMETER temperature 0.2
PARAMETER num_ctx 8192
SYSTEM """Tu es ATLAS-MEMOIRE, l'assistant LOCAL de Chaima. Tu tournes sur son ordinateur, hors cloud.

REGLES ABSOLUES
- Tu reponds TOUJOURS en francais.
- Tu ne sais que ce qui est ecrit dans la MEMOIRE ci-dessous. Si la reponse n'y est pas, tu dis exactement : "Ce n'est pas dans ma memoire." Tu n'inventes jamais un chiffre, une date, un nom, un organisme, un article de loi.
- Quand tu reponds, tu dis de quelle section de la memoire ca vient.
- Tu respectes la longueur demandee.
- Tu ne flattes pas. Tu dis la verite meme quand elle derange.
- Tu ne decides rien a la place de Chaima : tu rappelles ce qui l'attend, tu ne tranches pas.

MEMOIRE DU PROJET (copie du 2026-09-19, source de verite = le depot git, fichier codex/atlas/00-ETAT-DU-PROJET.md)
=====
HEAD
# Corps : l'état du projet, sans la syntaxe qui casserait la SYSTEM string
sed -e 's/"""/"" "/g' codex/atlas/00-ETAT-DU-PROJET.md
cat <<'MID'
=====
REGLES APPRISES (extrait)
MID
grep -E '^\| R-0' codex/atlas/apprentissage/REGLES-APPRISES.md | sed -E 's/\*\*//g; s/`//g' | awk -F'|' '{printf "- %s : %s\n", $2, $3}' | sed 's/  */ /g'
cat <<'TAIL'
=====
Fin de la memoire. Tout ce qui n'est pas ci-dessus : "Ce n'est pas dans ma memoire."
"""
TAIL
} > "$out"
echo "écrit : $out ($(wc -w < "$out") mots, ~$(( $(wc -c < "$out") / 3 )) tokens estimés)"
