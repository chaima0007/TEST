"""Libre & Accomplis — Agent Nutrition (scaffolding).

Propose des recettes adaptées au profil de l'utilisateur (allergies,
objectifs). Règles de sécurité validées par l'Expert en Santé :
  - Jamais de recette contenant un allergène de l'utilisateur.
  - En l'absence de recette compatible, répondre success=False plutôt
    que de proposer une recette à risque.
"""
from base_connaissances import BaseConnaissances, TAGS_PAR_OBJECTIF


class AgentNutrition:
    def __init__(self, base: BaseConnaissances):
        self.base = base

    def proposer_recette(self, user_id: int) -> dict:
        """Propose la recette la plus adaptée à l'utilisateur."""
        utilisateur = self.base.get_utilisateur(user_id)
        recettes = self.base.get_recettes(
            allergies=utilisateur.get("allergies", []),
            objectifs=utilisateur.get("objectifs", []),
        )
        recette = self._selectionner_meilleure_recette(
            recettes, utilisateur.get("objectifs", [])
        )
        if recette is None:
            return {"success": False, "raison": "aucune_recette_compatible"}

        return {
            "id": recette["id"],
            "nom": recette["nom"],
            "ingredients": recette["ingredients"],
            "tags": recette["tags"],
            "success": True,
        }

    def _selectionner_meilleure_recette(self, recettes: list, objectifs: list):
        """Sélectionne la recette dont les tags correspondent le mieux aux objectifs."""
        if not recettes:
            return None

        tags_recherches = set()
        for objectif in objectifs:
            tags_recherches.update(TAGS_PAR_OBJECTIF.get(objectif, []))

        def score(recette):
            return len(tags_recherches.intersection(recette["tags"]))

        return max(recettes, key=score)
