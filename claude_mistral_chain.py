"""
Enchaînement Claude (Anthropic) -> Mistral
==========================================

Ce script montre comment faire collaborer deux modèles de langage de
fournisseurs différents :

  1. On envoie une question à Claude (API Anthropic).
  2. La réponse de Claude est ensuite réutilisée comme prompt pour Mistral,
     créant ainsi un « enchaînement » (chaining) entre les deux modèles.

------------------------------------------------------------------------
INSTALLATION DES DÉPENDANCES
------------------------------------------------------------------------
Exécutez la commande suivante dans votre terminal avant de lancer le script :

    pip install anthropic mistralai

------------------------------------------------------------------------
CONFIGURATION DES CLÉS API
------------------------------------------------------------------------
Le script récupère automatiquement les clés depuis les variables
d'environnement. Sous Windows (cmd), configurez-les ainsi :

    set MISTRAL_API_KEY=votre_cle_mistral
    set ANTHROPIC_API_KEY=votre_cle_anthropic

(Sous PowerShell : $env:MISTRAL_API_KEY = "votre_cle_mistral")
(Sous Linux / macOS : export MISTRAL_API_KEY="votre_cle_mistral")

Note : les deux SDK lisent par défaut leur clé dans la variable
d'environnement correspondante (ANTHROPIC_API_KEY / MISTRAL_API_KEY).
Ici, on les lit explicitement pour bien montrer le mécanisme et pouvoir
afficher un message d'erreur clair si une clé est manquante.
"""

import os
import sys

from anthropic import Anthropic
from mistralai import Mistral


# ---------------------------------------------------------------------------
# 1. Récupération des clés API depuis les variables d'environnement
# ---------------------------------------------------------------------------
def charger_cles():
    """Récupère les clés API et arrête le script si l'une d'elles manque."""
    cle_anthropic = os.environ.get("ANTHROPIC_API_KEY")
    cle_mistral = os.environ.get("MISTRAL_API_KEY")

    manquantes = []
    if not cle_anthropic:
        manquantes.append("ANTHROPIC_API_KEY")
    if not cle_mistral:
        manquantes.append("MISTRAL_API_KEY")

    if manquantes:
        print(
            "Erreur : variable(s) d'environnement manquante(s) : "
            + ", ".join(manquantes)
            + "\nConfigurez-les avant de relancer le script "
            "(ex. : set MISTRAL_API_KEY=ma_cle).",
            file=sys.stderr,
        )
        sys.exit(1)

    return cle_anthropic, cle_mistral


# ---------------------------------------------------------------------------
# 2. Appel à Claude (API Anthropic)
# ---------------------------------------------------------------------------
def interroger_claude(client_anthropic, prompt, modele="claude-sonnet-4-6"):
    """Envoie un prompt à Claude et renvoie le texte de la réponse."""
    reponse = client_anthropic.messages.create(
        model=modele,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    # La réponse est une liste de blocs ; on concatène le texte de chacun.
    return "".join(
        bloc.text for bloc in reponse.content if bloc.type == "text"
    )


# ---------------------------------------------------------------------------
# 3. Appel à Mistral (API Mistral)
# ---------------------------------------------------------------------------
def interroger_mistral(client_mistral, prompt, modele="mistral-large-latest"):
    """Envoie un prompt à Mistral et renvoie le texte de la réponse."""
    reponse = client_mistral.chat.complete(
        model=modele,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return reponse.choices[0].message.content


# ---------------------------------------------------------------------------
# 4. Programme principal : on enchaîne Claude -> Mistral
# ---------------------------------------------------------------------------
def main():
    cle_anthropic, cle_mistral = charger_cles()

    # Configuration des deux clients.
    client_anthropic = Anthropic(api_key=cle_anthropic)
    client_mistral = Mistral(api_key=cle_mistral)

    # --- Étape 1 : on demande quelque chose à Claude -----------------------
    question_initiale = (
        "Donne-moi une idée originale d'application mobile en une phrase."
    )
    print(">>> Prompt envoyé à Claude :")
    print(question_initiale)
    print()

    reponse_claude = interroger_claude(client_anthropic, question_initiale)
    print(">>> Réponse de Claude :")
    print(reponse_claude)
    print()

    # --- Étape 2 : la réponse de Claude devient le prompt de Mistral -------
    # C'est ici que se fait l'« enchaînement » : la sortie d'un modèle
    # alimente l'entrée de l'autre.
    prompt_pour_mistral = (
        "Voici une idée d'application mobile proposée par un autre assistant :\n\n"
        f"\"{reponse_claude}\"\n\n"
        "En tant qu'expert produit, développe cette idée : décris trois "
        "fonctionnalités clés et le public cible."
    )
    print(">>> Prompt envoyé à Mistral (basé sur la réponse de Claude) :")
    print(prompt_pour_mistral)
    print()

    reponse_mistral = interroger_mistral(client_mistral, prompt_pour_mistral)
    print(">>> Réponse de Mistral :")
    print(reponse_mistral)


if __name__ == "__main__":
    main()
