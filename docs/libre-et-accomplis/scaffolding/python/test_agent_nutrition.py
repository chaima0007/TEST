"""Libre & Accomplis — Tests de l'Agent Nutrition (100 % de réussite exigée).

Exécution : python3 -m unittest discover docs/libre-et-accomplis/scaffolding/python
"""
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

    def test_aucune_recette_compatible(self):
        # Si toutes les recettes contiennent un allergène, l'agent refuse (success=False)
        # plutôt que de proposer une recette à risque.
        allergies = ["quinoa", "poulet", "avoine", "oeuf"]
        utilisateur = {"id": 789, "allergies": allergies, "objectifs": []}
        self.base.ajouter_utilisateur(utilisateur)

        reponse = self.agent.proposer_recette(utilisateur["id"])

        self.assertEqual(reponse["success"], False)
        self.assertEqual(reponse["raison"], "aucune_recette_compatible")

    def test_utilisateur_inconnu(self):
        with self.assertRaises(KeyError):
            self.agent.proposer_recette(999)


if __name__ == "__main__":
    unittest.main()
