"""Chargement de la configuration (clés API + modèles) depuis l'environnement."""
from __future__ import annotations

import os
from dataclasses import dataclass

try:
    # Charge automatiquement un fichier .env s'il existe (pratique en local).
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv non installé : on lit juste l'environnement.
    pass


@dataclass
class Config:
    anthropic_key: str
    mistral_key: str
    claude_model: str = "claude-opus-4-8"
    mistral_model: str = "mistral-large-latest"


def load_config() -> Config:
    """Lit les clés et modèles depuis l'environnement, avec messages d'erreur clairs."""
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    mistral_key = os.environ.get("MISTRAL_API_KEY")

    missing = []
    if not anthropic_key:
        missing.append("ANTHROPIC_API_KEY")
    if not mistral_key:
        missing.append("MISTRAL_API_KEY")
    if missing:
        raise SystemExit(
            "❌ Variable(s) d'environnement manquante(s) : "
            + ", ".join(missing)
            + "\n   Définis-les (ex. Windows : set ANTHROPIC_API_KEY=...) ou crée un fichier .env."
        )

    return Config(
        anthropic_key=anthropic_key,
        mistral_key=mistral_key,
        claude_model=os.environ.get("CLAUDE_MODEL", "claude-opus-4-8"),
        mistral_model=os.environ.get("MISTRAL_MODEL", "mistral-large-latest"),
    )
