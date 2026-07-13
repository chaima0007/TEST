"""Libre & Accomplis — Tests de l'Orchestrateur Central (100 % de réussite exigée)."""
import unittest

from agent_nutrition import AgentNutrition
from agent_sante import AgentSante
from base_connaissances import BaseConnaissances
from orchestrateur import Orchestrateur


def veto_sucre_diabetique(base):
    """Règle de l'Expert en Santé : pas d'ingrédient sucré pour un diabétique."""
    SUCRES = {"miel", "sucre"}

    def regle(user_id, action, reponse):
        if action != "proposer_recette" or not reponse.get("success"):
            return None
        utilisateur = base.get_utilisateur(user_id)
        if utilisateur.get("diabete") and SUCRES.intersection(reponse["ingredients"]):
            return "recette sucrée interdite pour un utilisateur diabétique"
        return None

    return regle


class TestOrchestrateur(unittest.TestCase):
    def setUp(self):
        self.base = BaseConnaissances()
        self.orch = Orchestrateur()
        self.orch.enregistrer_agent(
            "Agent Nutrition",
            {"proposer_recette": AgentNutrition(self.base).proposer_recette},
            priorite="moyenne",
        )
        self.orch.enregistrer_agent(
            "Agent Santé",
            {"analyser_sommeil": AgentSante(self.base).analyser_sommeil},
            priorite="haute",
        )

    def test_route_vers_le_bon_agent(self):
        self.base.ajouter_utilisateur({"id": 1, "allergies": ["noix"], "objectifs": []})

        [resultat] = self.orch.traiter(1, ["proposer_recette"])

        self.assertEqual(resultat["agent"], "Agent Nutrition")
        self.assertTrue(resultat["reponse"]["success"])
        self.assertNotIn("noix", resultat["reponse"]["ingredients"])

    def test_priorisation_sante_avant_nutrition(self):
        self.base.ajouter_utilisateur({"id": 1, "allergies": [], "objectifs": []})
        self.base.ajouter_sommeil(1, 5)

        resultats = self.orch.traiter(1, ["proposer_recette", "analyser_sommeil"])

        # La demande santé (priorité haute) est traitée avant la nutrition.
        self.assertEqual([r["action"] for r in resultats],
                         ["analyser_sommeil", "proposer_recette"])

    def test_doublons_ignores(self):
        self.base.ajouter_utilisateur({"id": 1, "allergies": [], "objectifs": []})

        resultats = self.orch.traiter(1, ["proposer_recette", "proposer_recette"])

        self.assertEqual(len(resultats), 1)
        doublons = [e for e in self.orch.journal if e["evenement"] == "doublon_ignore"]
        self.assertEqual(len(doublons), 1)

    def test_veto_expert_sur_recette_sucree_pour_diabetique(self):
        # Cas du modèle resolution-conflit.md : Agent Nutrition vs Expert en Santé.
        self.orch.ajouter_regle_veto("sucre_diabetique", veto_sucre_diabetique(self.base))
        # Utilisateur diabétique dont le profil pousse vers le granola au miel.
        self.base.ajouter_utilisateur(
            {"id": 2, "allergies": ["poulet", "oeuf", "quinoa"],
             "objectifs": ["energie"], "diabete": True}
        )

        [resultat] = self.orch.traiter(2, ["proposer_recette"])

        self.assertFalse(resultat["reponse"]["success"])
        self.assertEqual(resultat["reponse"]["raison"], "veto_expert")
        self.assertEqual(len(self.orch.conflits()), 1)

    def test_sans_veto_pour_utilisateur_non_diabetique(self):
        self.orch.ajouter_regle_veto("sucre_diabetique", veto_sucre_diabetique(self.base))
        self.base.ajouter_utilisateur(
            {"id": 3, "allergies": ["poulet", "oeuf", "quinoa"],
             "objectifs": ["energie"], "diabete": False}
        )

        [resultat] = self.orch.traiter(3, ["proposer_recette"])

        self.assertTrue(resultat["reponse"]["success"])
        self.assertEqual(self.orch.conflits(), [])

    def test_action_inconnue(self):
        self.base.ajouter_utilisateur({"id": 1})

        [resultat] = self.orch.traiter(1, ["predire_avenir"])

        self.assertFalse(resultat["reponse"]["success"])
        self.assertEqual(resultat["reponse"]["raison"], "action_inconnue")

    def test_conflit_enregistrement_deux_agents_meme_action(self):
        with self.assertRaises(ValueError):
            self.orch.enregistrer_agent(
                "Agent Imposteur",
                {"proposer_recette": lambda user_id: {"success": True}},
            )

    def test_audit_log_trace_les_executions(self):
        self.base.ajouter_utilisateur({"id": 1, "allergies": [], "objectifs": []})

        self.orch.traiter(1, ["proposer_recette"])

        executions = [e for e in self.orch.journal if e["evenement"] == "action_executee"]
        self.assertEqual(len(executions), 1)
        self.assertEqual(executions[0]["agent"], "Agent Nutrition")


if __name__ == "__main__":
    unittest.main()
