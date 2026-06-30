"""Configuration centralisee : lit les cles API et parametres depuis l'environnement.

Aucune cle n'est jamais ecrite en dur dans le code. Tout vient des variables
d'environnement (ANTHROPIC_API_KEY, MISTRAL_API_KEY...).
"""
import os
from dataclasses import dataclass


class ConfigError(Exception):
    """Levee quand une variable d'environnement obligatoire est absente."""


def _get(nom, obligatoire=True, defaut=None):
    valeur = os.environ.get(nom, defaut)
    if obligatoire and not valeur:
        raise ConfigError(f"Variable d'environnement manquante : {nom}")
    return valeur


@dataclass
class Config:
    anthropic_api_key: str
    mistral_api_key: str
    claude_model: str = "claude-sonnet-4-6"
    mistral_model: str = "mistral-large-latest"


def load_config():
    """Charge et valide la configuration. Leve ConfigError si une cle manque."""
    return Config(
        anthropic_api_key=_get("ANTHROPIC_API_KEY"),
        mistral_api_key=_get("MISTRAL_API_KEY"),
        claude_model=_get("CLAUDE_MODEL", obligatoire=False, defaut="claude-sonnet-4-6"),
        mistral_model=_get("MISTRAL_MODEL", obligatoire=False, defaut="mistral-large-latest"),
    )
