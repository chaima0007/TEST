"""Double controle : un modele PROPOSE, l'autre VERIFIE.

C'est le coeur du systeme. Pour une tache donnee :
  1. le "proposeur" (ex. Claude) genere une solution ;
  2. le "verificateur" (ex. Mistral) controle independamment cette solution
     et rend un verdict APPROUVE / REJETE.

Pour les taches sensibles, on peut aussi inverser les roles (consensus croise).
"""
from dataclasses import dataclass


@dataclass
class Resultat:
    proposition: str
    verdict: str        # "APPROUVE" ou "REJETE"
    justification: str
    approuve: bool


SYSTEME_VERIFICATEUR = (
    "Tu es un verificateur rigoureux et independant. On te donne une tache et une "
    "proposition de reponse produite par une autre IA. Verifie si la proposition est "
    "correcte, complete, et sans danger. Reponds OBLIGATOIREMENT en commencant ta "
    "premiere ligne par 'VERDICT: APPROUVE' ou 'VERDICT: REJETE', puis explique "
    "brievement pourquoi."
)


class DoubleControle:
    def __init__(self, proposeur, verificateur):
        self.proposeur = proposeur
        self.verificateur = verificateur

    def executer(self, tache):
        # 1. Le proposeur genere une solution
        proposition = self.proposeur.demander(tache)

        # 2. Le verificateur controle, de maniere independante
        prompt_verif = (
            f"TACHE :\n{tache}\n\n"
            f"PROPOSITION (par {self.proposeur.nom}) :\n{proposition}\n\n"
            "Verifie cette proposition selon tes consignes."
        )
        avis = self.verificateur.demander(prompt_verif, systeme=SYSTEME_VERIFICATEUR)

        # 3. On lit le verdict sur la premiere ligne
        premiere_ligne = avis.strip().split("\n", 1)[0].upper()
        approuve = "APPROUVE" in premiere_ligne and "REJETE" not in premiere_ligne

        return Resultat(
            proposition=proposition,
            verdict="APPROUVE" if approuve else "REJETE",
            justification=avis,
            approuve=approuve,
        )
