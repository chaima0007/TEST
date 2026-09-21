#!/usr/bin/env bash
# Génère codex/atlas/memoire/atlas-memoire.Modelfile : le profil Ollama qui donne à l'IA LOCALE
# de Chaima la mémoire du projet. À relancer à chaque rafale, après mise à jour de l'état.
# Pont provisoire vers la couche 4 (RAG) : tant que le RAG n'est pas installé, c'est ceci qui
# fait que l'IA locale « sait » où en est le projet.
set -euo pipefail
cd "$(dirname "$0")/.."
out=codex/atlas/memoire/atlas-memoire.Modelfile
tete=codex/atlas/memoire/atlas-memoire.tete.txt
{
cat <<'HEAD'
FROM qwen2.5:3b
PARAMETER temperature 0.2
PARAMETER num_ctx 16384
SYSTEM """Tu es ATLAS-MEMOIRE, l'assistant LOCAL de Chaima. Tu tournes sur son ordinateur, hors cloud.

REGLES ABSOLUES
- Tu reponds TOUJOURS en francais.
- Tu ne sais que ce qui est ecrit dans la MEMOIRE ci-dessous. Si la reponse n'y est pas, tu dis exactement : "Ce n'est pas dans ma memoire." Tu n'inventes jamais un chiffre, une date, un nom, un organisme, un article de loi.
- Quand tu reponds, tu dis de quelle section de la memoire ca vient.
- Tu respectes la longueur demandee.
- Tu ne flattes pas. Tu dis la verite meme quand elle derange.
- Tu ne decides rien a la place de Chaima : tu rappelles ce qui l'attend, tu ne tranches pas.
- Quand on te demande ou en est le projet, tu commences TOUJOURS par la section "DERNIER ÉVÉNEMENT" (titre exact dans la memoire).
- Tu n'inventes JAMAIS le sens d'un sigle. Les seuls sigles que tu connais sont dans le LEXIQUE. Un sigle absent du lexique : "Sigle non defini dans ma memoire."

LEXIQUE (seuls sens autorises)
- RAG = Retrieval-Augmented Generation : l'IA cherche dans les documents de Chaima avant de repondre.
- LLM = grand modele de langage (le moteur, ici qwen2.5:3b via Ollama).
- Zone 1 = quarantaine : un logiciel candidat est teste sans reseau ni secret avant d'etre accepte.
- Peppol = reseau europeen de facturation electronique, obligatoire en Belgique depuis le 01/01/2026.
- D-001 = decision numero 1 en attente : geler les nouveaux projets jusqu'au premier message d'un prospect.
- LLAM = nom d'un projet de Chaima (branche du depot), pas un sigle technique.
- A-DECIDER = le fichier qui liste tout ce qui attend une decision de Chaima.
- CI = verification automatique du code avant fusion.
- tokens/s = vitesse de generation du modele.

MEMOIRE DU PROJET (copie du DATE_COPIE, source de verite = le depot git, fichier codex/atlas/00-ETAT-DU-PROJET.md)
=====
HEAD
# Corps : l'état du projet, sans la syntaxe qui casserait la SYSTEM string
sed -e 's/"""/"" "/g' codex/atlas/00-ETAT-DU-PROJET.md
cat <<'MID'
=====
REGLES APPRISES (extrait)
MID
# Une règle = sa phrase en gras seulement (le détail reste dans le dépôt) : mémoire courte = IA plus rapide sur CPU
grep -E '^\| R-0' codex/atlas/apprentissage/REGLES-APPRISES.md | awk -F'|' '{id=$2; txt=$3; if (match(txt,/\*\*[^*]+\*\*/)) txt=substr(txt,RSTART+2,RLENGTH-4); gsub(/`/,"",txt); gsub(/  +/," ",txt); gsub(/^ +| +$/,"",id); printf "- %s : %s\n", id, txt}'
} | sed "s/DATE_COPIE/$(date -u +%F)/" > "$tete"
# Modelfile complet = tête + clôture. La tête seule sert au script Windows
# scripts/atlas-apprendre.bat, qui y ajoute les NOTES LOCALES de Chaima avant de clore.
{
cat "$tete"
cat <<'TAIL'
=====
Fin de la memoire. Tout ce qui n'est pas ci-dessus : "Ce n'est pas dans ma memoire."
"""
TAIL
} > "$out"
echo "écrit : $out ($(wc -w < "$out") mots, ~$(( $(wc -c < "$out") / 3 )) tokens estimés) + $tete"

# ---- MANIFEST du corpus « dépôt » : ce que scripts/atlas-apprendre.bat télécharge dans
# %USERPROFILE%\ATLAS\corpus\depot pour AnythingLLM (RAG). PAS dans le Modelfile (trop gros).
# Format : URL_encodée|nom_local_ASCII  — date = dernier commit du fichier (convention corpus/README).
manifest=codex/atlas/corpus/MANIFEST.txt
base_url="https://raw.githubusercontent.com/chaima0007/TEST/claude/nifty-shannon-u87dv8"
python3 - "$base_url" "$manifest" <<'PY'
import sys, subprocess, urllib.parse, re, unicodedata, glob
base, out = sys.argv[1], sys.argv[2]
selection = [
  ("codex/atlas/00-ETAT-DU-PROJET.md",                 "atlas",        "etat du projet ATLAS"),
  ("codex/atlas/apprentissage/REGLES-APPRISES.md",     "atlas",        "regles apprises R-001 a R-016"),
  ("codex/atlas/memoire/MACHINE.md",                   "atlas",        "fiche machine et procedures"),
  ("codex/atlas/memoire/DECISIONS.md",                 "atlas",        "decisions prises"),
  ("codex/atlas/deliberations/FICHE-DECISION-D-001.md","atlas",        "fiche decision D-001"),
  ("codex/atlas/deliberations/DOSSIER-01-STATUT-LEGAL.md","droit-belge","dossier statut legal"),
  ("codex/atlas/deliberations/DOSSIER-02-ENCAISSEMENT.md","droit-belge","dossier encaissement Peppol"),
  ("codex/expertise/droit-belge.md",                   "droit-belge",  "expertise droit belge"),
  ("codex/expertise/recherche-sources.md",             "methode",      "expertise recherche de sources"),
  ("codex/expertise/methode-agents.md",                "methode",      "expertise methode des agents"),
  ("codex/expertise/erreurs-transverses.md",           "methode",      "expertise erreurs transverses"),
  ("codex/A-DECIDER.md",                               "atlas",        "ce qui attend une decision"),
]
for f in sorted(glob.glob("codex/atlas/corpus/*.md")):
    if f.endswith("README.md"): continue
    selection.append((f, None, None))
def ascii_(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii","ignore").decode()
    return re.sub(r"[^A-Za-z0-9 ._-]+","",t).strip()
lines=[]
for path, dom, title in selection:
    date = subprocess.run(["git","log","-1","--format=%cs","--",path],capture_output=True,text=True).stdout.strip() or "0000-00-00"
    if dom is None:
        name = ascii_(path.split("/")[-1])
    else:
        name = f"{date} - {dom} - {ascii_(title)} - codex.md"
    url = base + "/" + urllib.parse.quote(path)
    lines.append(f"{url}|{name}")
open(out,"w",encoding="utf-8").write("\n".join(lines)+"\n")
print(f"manifest : {out} ({len(lines)} fichiers)")
PY
