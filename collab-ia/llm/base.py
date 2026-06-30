"""Interface commune a tous les modeles (Claude, Mistral, et d'autres demain).

Grace a cette abstraction, l'orchestrateur ne connait pas les details de chaque
API : il appelle simplement `client.demander(prompt)`.
"""
from abc import ABC, abstractmethod


class ClientLLM(ABC):
    """Tout client LLM expose une methode `demander(prompt)` -> texte."""

    nom = "llm"

    @abstractmethod
    def demander(self, prompt: str, systeme: str = "") -> str:
        """Envoie un prompt au modele et renvoie sa reponse texte."""
        ...
