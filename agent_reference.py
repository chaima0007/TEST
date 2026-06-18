"""
AGENT DE RÉFÉRENCE PROJETS
Indexe, documente et retrouve n'importe quoi dans tous tes projets.
Usage : python agent_reference.py
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"
INDEX_FILE = "index_projets.json"

EXTENSIONS_CODE = {".py", ".js", ".ts", ".html", ".css", ".php", ".java", ".go", ".rb", ".cs", ".sql"}
EXTENSIONS_DOC  = {".md", ".txt", ".pdf", ".docx", ".rst"}
IGNORER         = {"__pycache__", ".git", "node_modules", ".venv", "venv", "dist", "build"}


# ─────────────────────────────────────────────────────────────
# INDEXATION
# ─────────────────────────────────────────────────────────────

def _creer_model(model_name=None, system_instruction="", generation_config=None, **kwargs):
    """Compatibilité: retourne un proxy GenerativeModel pour google.genai."""
    class _ModelProxy:
        def __init__(self, mn, si, cfg):
            self.model_name = mn or MODEL
            self.system_instruction = si
            self.config = cfg or types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
            if isinstance(self.config, types.GenerateContentConfig):
                self.config = types.GenerateContentConfig(
                    system_instruction=si,
                    temperature=self.config.temperature if hasattr(self.config, 'temperature') else 0.3,
                    max_output_tokens=self.config.max_output_tokens if hasattr(self.config, 'max_output_tokens') else 2000,
                )
        def generate_content(self, prompt, stream=False):
            if stream:
                return client.models.generate_content_stream(
                    model=self.model_name, contents=prompt, config=self.config)
            return client.models.generate_content(
                model=self.model_name, contents=prompt, config=self.config)
    config = generation_config
    if config and not isinstance(config, types.GenerateContentConfig):
        config = types.GenerateContentConfig(
            temperature=getattr(config, 'temperature', 0.3),
            max_output_tokens=getattr(config, 'max_output_tokens', 2000),
        )
    return _ModelProxy(model_name, system_instruction, config)


def scanner_dossier(chemin):
    """Scanne un dossier et retourne la structure complète."""
    index = {}
    for racine, dossiers, fichiers in os.walk(chemin):
        dossiers[:] = [d for d in dossiers if d not in IGNORER]
        for fichier in fichiers:
            chemin_complet = os.path.join(racine, fichier)
            _, ext = os.path.splitext(fichier)
            if ext not in EXTENSIONS_CODE | EXTENSIONS_DOC:
                continue
            try:
                taille = os.path.getsize(chemin_complet)
                modif  = datetime.fromtimestamp(os.path.getmtime(chemin_complet)).isoformat()
                with open(chemin_complet, "r", encoding="utf-8", errors="ignore") as f:
                    contenu = f.read()
                index[chemin_complet] = {
                    "nom": fichier,
                    "extension": ext,
                    "taille": taille,
                    "modifie": modif,
                    "lignes": contenu.count("\n"),
                    "resume": "",
                    "tags": [],
                    "hash": hashlib.md5(contenu.encode()).hexdigest()[:8],
                }
            except Exception:
                pass
    return index


def charger_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"projets": {}, "derniere_mise_a_jour": "", "total_fichiers": 0}


def sauvegarder_index(index):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────
# AGENTS IA
# ─────────────────────────────────────────────────────────────

def creer_agent(instructions):
    return _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=2048),
    )


def stream_agent(model, prompt, label):
    print(f"\n{'─'*60}\n  ► {label}\n{'─'*60}\n")
    reponse = ""
    try:
        for chunk in model.generate_content(prompt, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        reponse = f"[Erreur : {e}]"
        print(reponse)
    print()
    return reponse


def agent_resumer_fichier(chemin, contenu):
    """Génère un résumé intelligent d'un fichier."""
    agent = creer_agent("""Tu es un analyste de code expert.
Pour le fichier fourni, produis en JSON :
{"resume": "1 phrase max", "tags": ["tag1","tag2"], "type": "agent|config|util|test|doc", "dependances": ["module1"]}
Rien d'autre que ce JSON.""")
    try:
        r = agent.generate_content(f"Fichier: {os.path.basename(chemin)}\n\n{contenu[:1500]}")
        texte = r.text.strip()
        debut = texte.find("{"); fin = texte.rfind("}") + 1
        return json.loads(texte[debut:fin])
    except Exception:
        return {"resume": "Fichier de code", "tags": [], "type": "util", "dependances": []}


def agent_indexer_projet(nom_projet, chemin):
    """Indexe un projet complet avec résumés IA."""
    print(f"\n  Scan de '{nom_projet}' en cours...")
    fichiers = scanner_dossier(chemin)
    print(f"  {len(fichiers)} fichiers trouvés. Analyse IA...")

    index = charger_index()
    index["projets"][nom_projet] = {
        "chemin": chemin,
        "date_index": datetime.now().isoformat(),
        "fichiers": {},
        "description": "",
        "technologies": [],
        "agents_disponibles": [],
    }

    for chemin_f, meta in list(fichiers.items())[:50]:  # limite 50 fichiers
        try:
            with open(chemin_f, "r", encoding="utf-8", errors="ignore") as f:
                contenu = f.read()
            analyse = agent_resumer_fichier(chemin_f, contenu)
            meta.update(analyse)
            index["projets"][nom_projet]["fichiers"][chemin_f] = meta
            if meta.get("type") == "agent":
                index["projets"][nom_projet]["agents_disponibles"].append(meta["nom"])
            print(f"  ✓ {meta['nom']} — {meta.get('resume', '')[:60]}")
        except Exception:
            pass

    # Description globale du projet
    noms_fichiers = [m["nom"] for m in fichiers.values()]
    agent_desc = creer_agent("Tu es un architecte logiciel. Décris un projet en 2 phrases max basé sur ses fichiers.")
    try:
        r = agent_desc.generate_content(f"Fichiers du projet : {', '.join(noms_fichiers[:20])}")
        index["projets"][nom_projet]["description"] = r.text.strip()
    except Exception:
        pass

    index["derniere_mise_a_jour"] = datetime.now().isoformat()
    index["total_fichiers"] = sum(len(p["fichiers"]) for p in index["projets"].values())
    sauvegarder_index(index)
    print(f"\n  ✅ Projet '{nom_projet}' indexé — {len(fichiers)} fichiers.")


def agent_rechercher(question):
    """Recherche intelligente dans tous les projets indexés."""
    index = charger_index()
    if not index["projets"]:
        print("\n  Aucun projet indexé. Utilise l'option 1 d'abord.")
        return

    # Construire contexte de recherche
    contexte = []
    for nom_projet, projet in index["projets"].items():
        contexte.append(f"\n=== {nom_projet} ===")
        contexte.append(f"Description : {projet.get('description', '')}")
        contexte.append(f"Agents : {', '.join(projet.get('agents_disponibles', []))}")
        for chemin_f, meta in projet["fichiers"].items():
            contexte.append(f"• {meta['nom']} [{meta.get('type','')}] — {meta.get('resume','')} | Tags: {','.join(meta.get('tags',[]))}")

    agent = creer_agent("""Tu es un assistant de référence projet expert.
Tu connais parfaitement tous les projets indexés.
Réponds précisément à la question en citant les fichiers/agents concernés.
Si tu ne trouves pas, dis-le clairement.""")

    return stream_agent(agent,
        f"BASE DE CONNAISSANCE :\n{''.join(contexte)}\n\nQUESTION : {question}",
        "Recherche dans les projets"
    )


def agent_generer_doc(nom_projet):
    """Génère une documentation complète d'un projet."""
    index = charger_index()
    if nom_projet not in index["projets"]:
        print(f"\n  Projet '{nom_projet}' non trouvé. Indexe-le d'abord.")
        return

    projet = index["projets"][nom_projet]
    fichiers_info = "\n".join([
        f"- {m['nom']} ({m.get('type','')}): {m.get('resume','')} | {m['lignes']} lignes"
        for m in projet["fichiers"].values()
    ])

    agent = creer_agent("""Tu es un expert en documentation technique.
Génère une documentation complète et professionnelle avec :
# Titre du projet
## Description
## Architecture
## Agents disponibles (avec ce que chacun fait)
## Installation et usage
## Exemples d'utilisation
## Sécurité
## Roadmap suggérée""")

    doc = stream_agent(agent,
        f"Projet : {nom_projet}\nDescription : {projet.get('description','')}\n\nFichiers :\n{fichiers_info}",
        f"Documentation — {nom_projet}"
    )

    nom_doc = f"DOC_{nom_projet.replace(' ', '_')}.md"
    with open(nom_doc, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"\n  ✅ Documentation sauvegardée → {nom_doc}")


def agent_comparer_projets():
    """Compare tous les projets et génère un rapport de cohérence."""
    index = charger_index()
    if len(index["projets"]) < 2:
        print("\n  Il faut au moins 2 projets indexés pour comparer.")
        return

    resume = "\n".join([
        f"{nom} : {p.get('description','')} | {len(p['fichiers'])} fichiers | Agents: {', '.join(p.get('agents_disponibles',[]))}"
        for nom, p in index["projets"].items()
    ])

    agent = creer_agent("""Tu es un architecte logiciel senior.
Compare les projets fournis et produis :
1. Points communs et synergies possibles
2. Doublons à éviter
3. Recommandations d'intégration
4. Architecture globale suggérée pour tous les projets ensemble
5. Priorités de développement""")

    stream_agent(agent, f"Projets à comparer :\n{resume}", "Comparaison des projets")


def afficher_index():
    """Affiche l'index complet de tous les projets."""
    index = charger_index()
    if not index["projets"]:
        print("\n  Aucun projet indexé.")
        return
    print(f"\n  Dernière mise à jour : {index.get('derniere_mise_a_jour','?')[:10]}")
    print(f"  Total fichiers indexés : {index.get('total_fichiers', 0)}\n")
    for nom, projet in index["projets"].items():
        agents = projet.get("agents_disponibles", [])
        print(f"  📁 {nom}")
        print(f"     {projet.get('description','')[:80]}")
        print(f"     {len(projet['fichiers'])} fichiers | Agents : {', '.join(agents) if agents else 'aucun'}")
        print()


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  AGENT DE RÉFÉRENCE — Index de tous tes projets")
    print("═"*60)

    while True:
        print("\n  1. Indexer un projet (nouveau ou mise à jour)")
        print("  2. Rechercher dans tous les projets")
        print("  3. Générer la documentation d'un projet")
        print("  4. Comparer tous les projets")
        print("  5. Voir l'index complet")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            nom = input("  Nom du projet → ").strip()
            chemin = input("  Chemin du dossier (. pour dossier actuel) → ").strip() or "."
            agent_indexer_projet(nom, chemin)
        elif choix == "2":
            question = input("  Ta question → ").strip()
            if question:
                agent_rechercher(question)
        elif choix == "3":
            afficher_index()
            nom = input("  Nom du projet à documenter → ").strip()
            agent_generer_doc(nom)
        elif choix == "4":
            agent_comparer_projets()
        elif choix == "5":
            afficher_index()
        else:
            print("  Choix invalide.")
