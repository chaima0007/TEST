import sys
from anthropic import Anthropic

client = Anthropic()
MODEL_NAME = "claude-opus-4-8"

SYSTEM_PROFESSEUR = """Tu es un Professeur expert et bienveillant, spécialisé dans l'aide aux apprenants de tous niveaux.

Tes règles :
- Tu expliques toujours avec des exemples simples et concrets
- Tu adaptes ton langage au niveau de l'élève
- Tu ne donnes jamais la réponse directement : tu guides l'élève à trouver par lui-même
- Tu encourages et valorises les efforts
- Tu poses des questions pour vérifier la compréhension après chaque explication
- Si l'élève se trompe, tu corriges avec bienveillance et réexpliques différemment
- Tu utilises des analogies du quotidien pour rendre les concepts abstraits accessibles
- À la fin de chaque réponse, tu poses UNE question de vérification pour t'assurer que l'élève a compris"""

SYSTEM_VERIFICATEUR = """Tu es un agent de vérification pédagogique.
Ton rôle : analyser la réponse d'un élève et déterminer s'il a bien compris.

Réponds UNIQUEMENT avec ce format JSON :
{
  "compris": true/false,
  "score": 0-100,
  "feedback": "commentaire court et encourageant",
  "suggestion": "si score < 70, une piste pour mieux expliquer"
}"""


def verifier_comprehension(question_prof, reponse_eleve):
    """Agent de vérification qui évalue si l'élève a compris."""
    import json

    contenu = f"""Question du professeur : {question_prof}
Réponse de l'élève : {reponse_eleve}

L'élève a-t-il bien compris ?"""

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=500,
        thinking={"type": "adaptive"},
        output_config={"effort": "medium"},
        system=SYSTEM_VERIFICATEUR,
        messages=[{"role": "user", "content": contenu}],
    )

    try:
        texte = response.content[0].text
        # Extraire le JSON de la réponse
        debut = texte.find("{")
        fin = texte.rfind("}") + 1
        return json.loads(texte[debut:fin])
    except Exception:
        return {"compris": True, "score": 50, "feedback": "Continue comme ça !", "suggestion": ""}


def agent_professeur():
    historique = []
    derniere_question = ""

    print("\n" + "=" * 60)
    print("     AGENT PROFESSEUR — Spécialiste en aide et vérification")
    print("=" * 60)
    print("Tape 'quitter' pour arrêter la session.\n")

    sujet = input("Sur quel sujet veux-tu être aidé ? → ").strip()
    if not sujet:
        sujet = "un sujet de ton choix"

    historique.append({
        "role": "user",
        "content": f"Je veux apprendre : {sujet}"
    })

    print("\n" + "-" * 60)

    while True:
        # Le professeur répond
        print("\n[Professeur] ", end="", flush=True)
        reponse_prof = ""

        with client.messages.stream(
            model=MODEL_NAME,
            max_tokens=1000,
            thinking={"type": "adaptive"},
            output_config={"effort": "high"},
            system=SYSTEM_PROFESSEUR,
            messages=historique,
        ) as stream:
            for event in stream:
                if (hasattr(event, "type") and
                        event.type == "content_block_delta" and
                        hasattr(event.delta, "type") and
                        event.delta.type == "text_delta"):
                    print(event.delta.text, end="", flush=True)
                    reponse_prof += event.delta.text

        print("\n")

        # Extraire la dernière question posée par le prof
        lignes = reponse_prof.strip().split("?")
        if len(lignes) > 1:
            derniere_question = lignes[-2].strip().split("\n")[-1] + "?"

        historique.append({"role": "assistant", "content": reponse_prof})

        # L'élève répond
        reponse_eleve = input("[Toi] → ").strip()

        if reponse_eleve.lower() in ["quitter", "quit", "exit", "stop"]:
            print("\nBonne continuation ! Continue d'apprendre chaque jour.")
            break

        if not reponse_eleve:
            continue

        # Vérification de la compréhension
        if derniere_question:
            print("\n[Vérification en cours...]", flush=True)
            verification = verifier_comprehension(derniere_question, reponse_eleve)
            score = verification.get("score", 50)
            feedback = verification.get("feedback", "")

            barre = "█" * (score // 10) + "░" * (10 - score // 10)
            print(f"[Score de compréhension] {barre} {score}/100")
            print(f"[Feedback] {feedback}\n")

            if score < 70:
                suggestion = verification.get("suggestion", "")
                if suggestion:
                    reponse_eleve += f"\n\n(Note interne : l'élève semble ne pas avoir bien compris. {suggestion})"

        historique.append({"role": "user", "content": reponse_eleve})


if __name__ == "__main__":
    agent_professeur()
