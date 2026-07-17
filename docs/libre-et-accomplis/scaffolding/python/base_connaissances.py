"""Libre & Accomplis — Base de connaissances centralisée (scaffolding).

Version en mémoire pour le développement et les tests locaux. En production,
cette classe est remplacée par une implémentation adossée à Neo4j (relations),
PostgreSQL (données structurées) et Redis (cache) — même interface publique.
"""

# Correspondance objectif utilisateur -> tags de recettes recherchés
TAGS_PAR_OBJECTIF = {
    "perte_de_poids": ["leger", "faible_calories"],
    "prise_de_muscle": ["proteines"],
    "energie": ["glucides_complexes"],
}

RECETTES_PAR_DEFAUT = [
    {
        "id": 1,
        "nom": "Salade de quinoa aux légumes",
        "ingredients": ["quinoa", "tomate", "concombre", "citron"],
        "tags": ["leger", "faible_calories", "vegan"],
    },
    {
        "id": 2,
        "nom": "Poulet grillé et brocoli",
        "ingredients": ["poulet", "brocoli", "huile_olive"],
        "tags": ["proteines", "leger"],
    },
    {
        "id": 3,
        "nom": "Granola maison aux noix",
        "ingredients": ["avoine", "noix", "miel"],
        "tags": ["glucides_complexes", "energie"],
    },
    {
        "id": 4,
        "nom": "Omelette aux épinards",
        "ingredients": ["oeuf", "epinard", "fromage"],
        "tags": ["proteines"],
    },
]


class BaseConnaissances:
    """Mémoire partagée entre les agents : profils utilisateurs et recettes.

    Garantit l'absence de doublons : ajouter un utilisateur existant met à
    jour son profil au lieu de créer une seconde entrée.
    """

    def __init__(self):
        self._utilisateurs = {}
        self._recettes = [dict(r) for r in RECETTES_PAR_DEFAUT]
        self._sommeil = {}

    # -- Utilisateurs ---------------------------------------------------------

    def ajouter_utilisateur(self, utilisateur: dict) -> None:
        if "id" not in utilisateur:
            raise ValueError("Un utilisateur doit avoir un champ 'id'.")
        self._utilisateurs[utilisateur["id"]] = dict(utilisateur)

    def get_utilisateur(self, user_id: int) -> dict:
        if user_id not in self._utilisateurs:
            raise KeyError(f"Utilisateur {user_id} inconnu dans la base de connaissances.")
        return dict(self._utilisateurs[user_id])

    # -- Sommeil --------------------------------------------------------------

    def ajouter_sommeil(self, user_id: int, duree: float, date: str = "") -> None:
        """Enregistre une nuit de sommeil (durée en heures)."""
        self.get_utilisateur(user_id)  # valide que l'utilisateur existe
        self._sommeil.setdefault(user_id, []).append({"date": date, "duree": duree})

    def get_historique_sommeil(self, user_id: int) -> list:
        return [dict(nuit) for nuit in self._sommeil.get(user_id, [])]

    # -- Recettes -------------------------------------------------------------

    def ajouter_recette(self, recette: dict) -> None:
        self._recettes.append(dict(recette))

    def get_recettes(self, allergies=(), objectifs=()) -> list:
        """Retourne les recettes compatibles avec les allergies de l'utilisateur.

        Les allergènes sont exclus strictement (règle de sécurité) ; les
        objectifs servent ensuite au tri par pertinence côté agent.
        """
        allergies = set(allergies or ())
        return [
            dict(r) for r in self._recettes
            if not allergies.intersection(r["ingredients"])
        ]
