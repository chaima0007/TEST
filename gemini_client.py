"""
Module central Gemini — google.genai (nouvelle API unifiée)
Toutes les fonctions utilisées par les agents passent par ici.
"""
import os
from google import genai
from google.genai import types

MODEL_DEFAULT = "gemini-2.0-flash"

_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            raise RuntimeError("Variable GEMINI_API_KEY manquante. Relance installer.bat.")
        _client = genai.Client(api_key=api_key)
    return _client


def generer(
    instructions: str,
    prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 2000,
    model: str = MODEL_DEFAULT,
) -> str:
    """Génère du texte (sans streaming)."""
    client = get_client()
    config = types.GenerateContentConfig(
        system_instruction=instructions,
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    return response.text or ""


def streamer(
    instructions: str,
    prompt: str,
    label: str = "",
    temperature: float = 0.3,
    max_tokens: int = 3000,
    model: str = MODEL_DEFAULT,
) -> str:
    """Génère du texte en streaming et l'affiche en temps réel."""
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    client = get_client()
    config = types.GenerateContentConfig(
        system_instruction=instructions,
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    texte = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=prompt,
            config=config,
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                texte += chunk.text
    except Exception as e:
        print(f"[Erreur Gemini : {e}]")
    print()
    return texte


def creer_model_expert(role: str, description: str, temperature: float = 0.2) -> "_ExpertProxy":
    """Retourne un proxy qui simule l'ancienne interface GenerativeModel."""
    return _ExpertProxy(role=role, description=description, temperature=temperature)


class _ExpertProxy:
    """Proxy compatible avec l'ancienne interface genai.GenerativeModel."""

    def __init__(self, role: str, description: str, temperature: float = 0.2):
        self.system_instruction = (
            f"Tu es {role} — {description}.\n"
            "Tu travailles pour Caelum Partners (Bruxelles, Belgique).\n"
            "Fondatrice : Chaima Mhadbi | contact@caelumpartners.agency\n"
            "Services : Site web 500€ / Automation IA 1500€ / Pack 3000€\n\n"
            "Tu es MÉTICULEUX, PARANO (positivement), AMBITIEUX, PROTECTEUR, ANALYTIQUE.\n"
            "Tu donnes des réponses précises, chiffrées, actionnables. Jamais vague."
        )
        self.temperature = temperature

    def generate_content(self, prompt: str, stream: bool = False):
        client = get_client()
        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=self.temperature,
            max_output_tokens=500,
        )
        if stream:
            return client.models.generate_content_stream(
                model=MODEL_DEFAULT,
                contents=prompt,
                config=config,
            )
        return client.models.generate_content(
            model=MODEL_DEFAULT,
            contents=prompt,
            config=config,
        )
