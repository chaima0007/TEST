# =============================================================================
# Libre & Accomplis — Exemple de test de simulation pour un agent IA
# Chaque agent doit atteindre 100 % de réussite aux tests unitaires locaux
# et 95 % de réussite en simulation avant intégration.
# =============================================================================
import unittest

from agent_nutrition import AgentNutrition
from base_connaissances import BaseConnaissances


class TestAgentNutrition(unittest.TestCase):
    def setUp(self):
        self.base = BaseConnaissances()
        self.agent = AgentNutrition(self.base)

    def test_proposer_recette_sans_allergene(self):
        # Utilisateur allergique aux noix : l'agent doit proposer une recette SANS noix.
        utilisateur = {"id": 123, "allergies": ["noix"], "objectifs": ["perte_de_poids"]}
        self.base.ajouter_utilisateur(utilisateur)

        recette = self.agent.proposer_recette(utilisateur["id"])

        self.assertNotIn("noix", recette["ingredients"])
        self.assertEqual(recette["success"], True)

    def test_proposer_recette_avec_objectif(self):
        # Utilisateur avec objectif "prise de muscle" : la recette doit être protéinée.
        utilisateur = {"id": 456, "allergies": [], "objectifs": ["prise_de_muscle"]}
        self.base.ajouter_utilisateur(utilisateur)

        recette = self.agent.proposer_recette(utilisateur["id"])

        self.assertIn("proteines", recette["tags"])
        self.assertEqual(recette["success"], True)


if __name__ == "__main__":
    unittest.main()
