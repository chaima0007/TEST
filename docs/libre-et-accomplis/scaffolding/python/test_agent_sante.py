"""Libre & Accomplis — Tests de l'Agent Santé (100 % de réussite exigée)."""
import unittest

from agent_sante import AgentSante
from base_connaissances import BaseConnaissances


class TestAgentSante(unittest.TestCase):
    def setUp(self):
        self.base = BaseConnaissances()
        self.agent = AgentSante(self.base)
        self.base.ajouter_utilisateur({"id": 1, "energie": "basse"})

    def test_sommeil_insuffisant_priorite_haute(self):
        for duree in [5, 5.5, 4, 6, 5]:
            self.base.ajouter_sommeil(1, duree)

        analyse = self.agent.analyser_sommeil(1)

        self.assertTrue(analyse["success"])
        self.assertLess(analyse["moyenne_sommeil"], 6)
        self.assertEqual(analyse["priorite"], "haute")

    def test_bon_sommeil_priorite_basse(self):
        for duree in [8, 7.5, 8, 7]:
            self.base.ajouter_sommeil(1, duree)

        analyse = self.agent.analyser_sommeil(1)

        self.assertEqual(analyse["priorite"], "basse")

    def test_moyenne_sur_nuits_reelles(self):
        # 2 nuits enregistrées seulement : la moyenne doit être 7.0,
        # pas 14/7 = 2.0 (bug du calcul divisé par un 7 fixe).
        self.base.ajouter_sommeil(1, 7)
        self.base.ajouter_sommeil(1, 7)

        analyse = self.agent.analyser_sommeil(1)

        self.assertEqual(analyse["moyenne_sommeil"], 7.0)

    def test_aucune_donnee_sommeil(self):
        reponse = self.agent.analyser_sommeil(1)

        self.assertFalse(reponse["success"])
        self.assertEqual(reponse["raison"], "aucune_donnee_sommeil")

    def test_exercice_selon_energie(self):
        proposition = self.agent.proposer_exercice(1)

        self.assertTrue(proposition["success"])
        self.assertIn("Yoga doux", proposition["exercices"])

    def test_utilisateur_inconnu(self):
        with self.assertRaises(KeyError):
            self.agent.analyser_sommeil(999)


if __name__ == "__main__":
    unittest.main()
