"""
AGENTS INTELLIGENTS - Version Google Gemini (100% GRATUIT)
Clé API gratuite sur : aistudio.google.com
"""

import os
import sys
import json
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\nERREUR : Clé API manquante.")
    print("1. Va sur https://aistudio.google.com")
    print("2. Clique sur 'Get API Key' → 'Create API Key'")
    print("3. Puis dans ton CMD tape :")
    print("   set GEMINI_API_KEY=ta_cle_ici")
    sys.exit(1)

MODEL = "gemini-2.0-flash"


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


def creer_agent(nom, instructions, effort="normal"):
    """Crée et retourne un agent avec ses instructions."""
    config = types.GenerateContentConfig(
        temperature=0.3 if effort == "precis" else 0.7,
        max_output_tokens=4096,
    )
    model = _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=config,
    )
    return nom, model


def executer_agent(nom, model, message, historique=None):
    """Exécute un agent et retourne sa réponse en streaming."""
    print(f"\n{'='*60}")
    print(f"  Agent : {nom}")
    print(f"{'='*60}")

    chat = model.start_chat(history=historique or [])
    reponse_texte = ""

    try:
        stream = chat.send_message(message, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse_texte += chunk.text
    except Exception as e:
        print(f"\nErreur agent {nom}: {e}")
        return ""

    print("\n")
    return reponse_texte


# ─────────────────────────────────────────────
# AGENT 1 : PROFESSEUR INTERACTIF AVEC SCORE
# ─────────────────────────────────────────────

def lancer_professeur():
    """Agent professeur interactif avec vérification et score."""

    _, prof = creer_agent(
        "Professeur Expert",
        """Tu es un professeur expert, patient et bienveillant.
Règles strictes :
- Explique toujours avec des exemples simples du quotidien
- Ne donne JAMAIS la réponse directement, guide l'élève
- Après chaque explication, pose UNE seule question de vérification
- Si l'élève se trompe, encourage-le et réexplique autrement
- Adapte ton niveau à celui de l'élève""",
        effort="normal"
    )

    _, verificateur = creer_agent(
        "Vérificateur",
        """Tu analyses les réponses d'élèves.
Réponds UNIQUEMENT en JSON valide :
{"score": <0-100>, "compris": <true/false>, "feedback": "<encouragement court>", "conseil": "<si score<70: comment mieux expliquer>"}
Rien d'autre que ce JSON.""",
        effort="precis"
    )

    print("\n" + "═" * 60)
    print("   AGENT PROFESSEUR  —  Gratuit via Google Gemini")
    print("═" * 60)
    print("Tape 'quitter' pour arrêter.\n")

    sujet = input("Sur quel sujet veux-tu être aidé ? → ").strip()
    if not sujet:
        print("Sujet vide, arrêt.")
        return

    historique_prof = []
    derniere_question_prof = ""

    # Premier message du prof
    premier_message = f"L'élève veut apprendre : {sujet}. Commence par une introduction simple et pose une première question."
    reponse = executer_agent("Professeur Expert", prof, premier_message)

    # Extraire la dernière question
    if "?" in reponse:
        derniere_question_prof = reponse.split("?")[-2].strip().split("\n")[-1] + "?"

    historique_prof.append({"role": "model", "parts": [reponse]})

    while True:
        reponse_eleve = input("[Toi] → ").strip()

        if reponse_eleve.lower() in ["quitter", "quit", "exit", "stop"]:
            print("\nBravo pour cette session ! Continue d'apprendre.")
            break

        if not reponse_eleve:
            continue

        # Vérification rapide
        if derniere_question_prof:
            print("\n[Vérification...]", flush=True)
            contenu_verif = f'Question: "{derniere_question_prof}" | Réponse élève: "{reponse_eleve}"'
            chat_verif = verificateur.start_chat()
            try:
                res_verif = chat_verif.send_message(contenu_verif)
                texte_verif = res_verif.text.strip()
                debut = texte_verif.find("{")
                fin = texte_verif.rfind("}") + 1
                data = json.loads(texte_verif[debut:fin])
                score = data.get("score", 50)
                feedback = data.get("feedback", "Continue !")
                conseil = data.get("conseil", "")

                barre = "█" * (score // 10) + "░" * (10 - score // 10)
                print(f"\n  Score : {barre} {score}/100")
                print(f"  {feedback}")
                if conseil:
                    print(f"  Conseil : {conseil}")
                print()

                if score < 50:
                    reponse_eleve += " (L'élève n'a pas bien compris, réexplique différemment avec un nouvel exemple.)"
            except Exception:
                pass

        historique_prof.append({"role": "user", "parts": [reponse_eleve]})

        reponse_suivante = executer_agent("Professeur Expert", prof, reponse_eleve, historique_prof)

        if "?" in reponse_suivante:
            derniere_question_prof = reponse_suivante.split("?")[-2].strip().split("\n")[-1] + "?"

        historique_prof.append({"role": "model", "parts": [reponse_suivante]})


# ─────────────────────────────────────────────
# AGENT 2 : USINE DE MIGRATION LOGICIELLE
# ─────────────────────────────────────────────

def lancer_migration(fichier):
    """Pipeline de migration automatique en 4 étapes."""

    if not os.path.exists(fichier):
        print(f"Fichier introuvable : {fichier}")
        sys.exit(1)

    with open(fichier, "r", encoding="utf-8") as f:
        code = f.read()

    print(f"\nMigration de : {fichier} ({len(code)} caractères)\n")

    _, architecte = creer_agent(
        "Architecte Senior",
        "Tu es un Architecte Logiciel Senior. Analyse le code legacy fourni et produis un plan de migration détaillé : problèmes identifiés, technologies cibles, étapes de refactorisation, risques.",
        effort="precis"
    )

    _, ingenieur = creer_agent(
        "Ingénieur de Code",
        "Tu es un Ingénieur principal. Réécris le code legacy en version moderne, typée, sécurisée, avec gestion d'erreurs. Fournis uniquement le code final prêt à l'emploi.",
        effort="precis"
    )

    _, securite = creer_agent(
        "Expert Sécurité",
        "Tu es un Expert en Sécurité Web (OWASP). Audite le code fourni, corrige toutes les vulnérabilités et retourne le code corrigé et sécurisé avec explications.",
        effort="precis"
    )

    _, testeur = creer_agent(
        "Ingénieur Tests",
        "Tu es un Ingénieur Tests. Génère une suite de tests unitaires et d'intégration complète pour le code fourni. Couvre les cas nominaux, limites et de sécurité.",
        effort="precis"
    )

    plan = executer_agent("Architecte Senior", architecte, f"Analyse ce code legacy :\n\n{code}")
    code_migre = executer_agent("Ingénieur de Code", ingenieur, f"Code original :\n{code}\n\nPlan :\n{plan}\n\nRéécris ce code.")
    code_securise = executer_agent("Expert Sécurité", securite, f"Audite et corrige ce code :\n\n{code_migre}")
    tests = executer_agent("Ingénieur Tests", testeur, f"Génère les tests pour ce code :\n\n{code_securise}")

    # Sauvegarde
    base = os.path.splitext(fichier)[0]
    with open(f"{base}_migre.py", "w", encoding="utf-8") as f:
        f.write(code_securise)
    with open(f"{base}_tests.py", "w", encoding="utf-8") as f:
        f.write(tests)
    with open(f"{base}_plan.txt", "w", encoding="utf-8") as f:
        f.write(plan)

    print("═" * 60)
    print("MIGRATION TERMINÉE")
    print(f"  Code migré   → {base}_migre.py")
    print(f"  Tests        → {base}_tests.py")
    print(f"  Plan         → {base}_plan.txt")
    print("═" * 60)


# ─────────────────────────────────────────────
# MENU PRINCIPAL
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("   AGENTS IA  —  100% Gratuit (Google Gemini)")
    print("═" * 60)
    print("\n  1. Agent Professeur (apprendre n'importe quel sujet)")
    print("  2. Usine de Migration (moderniser du vieux code)")
    print()

    choix = input("Ton choix (1 ou 2) → ").strip()

    if choix == "1":
        lancer_professeur()
    elif choix == "2":
        if len(sys.argv) > 1:
            lancer_migration(sys.argv[1])
        else:
            fichier = input("Chemin du fichier à migrer → ").strip()
            lancer_migration(fichier)
    else:
        print("Choix invalide. Lance avec : python agents.py")
