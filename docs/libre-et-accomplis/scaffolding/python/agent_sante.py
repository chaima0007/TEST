"""Libre & Accomplis — Agent Santé (scaffolding).

Analyse le sommeil et propose des exercices adaptés au niveau d'énergie.
Règles validées par l'Expert en Santé :
  - Ne jamais conclure sans données : si aucun historique de sommeil,
    répondre success=False plutôt que d'inventer une moyenne.
  - La moyenne est calculée sur les nuits réellement enregistrées
    (7 dernières au maximum), jamais divisée par un 7 fixe.
"""
from base_connaissances import BaseConnaissances

EXERCICES_PAR_ENERGIE = {
    "basse": ["Yoga doux", "Méditation guidée", "Marche de 10 min"],
    "moyenne": ["Natation", "Vélo", "Pilates"],
    "haute": ["HIIT", "Course à pied", "Musculation"],
}


class AgentSante:
    def __init__(self, base: BaseConnaissances):
        self.base = base

    def analyser_sommeil(self, user_id: int) -> dict:
        """Analyse le sommeil de l'utilisateur et propose un conseil priorisé."""
        self.base.get_utilisateur(user_id)  # KeyError si inconnu
        historique = self.base.get_historique_sommeil(user_id)
        if not historique:
            return {"success": False, "raison": "aucune_donnee_sommeil"}

        dernieres_nuits = historique[-7:]
        moyenne = sum(nuit["duree"] for nuit in dernieres_nuits) / len(dernieres_nuits)

        if moyenne < 6:
            conseil = "Tu dors trop peu ! Essaie de te coucher plus tôt."
            priorite = "haute"
        elif moyenne < 7:
            conseil = "Ton sommeil est insuffisant. Vise 7-8h par nuit."
            priorite = "moyenne"
        else:
            conseil = "Bonne moyenne de sommeil ! Continue comme ça."
            priorite = "basse"

        return {
            "moyenne_sommeil": round(moyenne, 2),
            "conseil": conseil,
            "priorite": priorite,
            "success": True,
        }

    def proposer_exercice(self, user_id: int) -> dict:
        """Propose des exercices adaptés au niveau d'énergie de l'utilisateur."""
        utilisateur = self.base.get_utilisateur(user_id)
        energie = utilisateur.get("energie", "moyenne")
        exercices = EXERCICES_PAR_ENERGIE.get(energie, EXERCICES_PAR_ENERGIE["moyenne"])
        return {"exercices": list(exercices), "energie": energie, "success": True}
