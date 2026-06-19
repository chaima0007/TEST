"""
AGENT REPORTING ONEM [90] — Conformité chômage belge, simulation revenus, alertes seuil
Calcule l'impact de chaque revenu Caelum sur les allocations de chômage.

Usage : python agent_reporting_onem.py
"""

import os
import sys
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

# Données ONEM Belgique (à vérifier régulièrement sur onem.be)
SEUIL_ONEM = {
    "isole": 5217.16,       # €/trimestre net maximum (isolé)
    "cohabitant": 4500.00,  # €/trimestre net approximatif
    "chef_menage": 6000.00, # €/trimestre net approximatif
}

IDENTITE = f"""# AGENT REPORTING ONEM — Conformité chômage belge

## IDENTITÉ
Tu es l'expert conformité ONEM (Office National de l'Emploi) pour Chaima, au chômage et fondatrice de Caelum Partners.
Tu calcules l'impact de chaque revenu d'activité sur ses allocations de chômage.

## SITUATION DE CHAIMA
- Statut : au chômage, en formation
- Organisation syndicale : CSC (Confédération des Syndicats Chrétiens)
- Catégorie : ISOLÉE
- Seuil ONEM trimestriel net maximum : {SEUIL_ONEM['isole']}€
- Activité déclarée : Caelum Partners (freelance / indépendante complémentaire)

## SEUILS LÉGAUX ACTUELS (à vérifier sur onem.be)
- Isolé·e : {SEUIL_ONEM['isole']}€/trimestre net
- Cohabitant·e : {SEUIL_ONEM['cohabitant']}€/trimestre net (approx.)
- Chef·fe de ménage : {SEUIL_ONEM['chef_menage']}€/trimestre net (approx.)

## RÈGLES IMPORTANTES
1. Revenus à déclarer : TOUS les revenus d'activité dans le trimestre
2. Revenus nets = revenus bruts - cotisations INASTI (20.5%) environ
3. Si dépassement seuil : SUSPENSION PARTIELLE OU TOTALE des allocations
4. Obligation de déclaration : formulaire C45B (avant de commencer l'activité)
5. Statut indépendant complémentaire : possible si conditions remplies

## AVERTISSEMENT LÉGAL
Je fournis des simulations INDICATIVES. Toujours confirmer avec le CSC avant de décider.
Les seuils et règles ONEM peuvent changer — vérifier onem.be pour les montants exacts."""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE,
                temperature=0.1,
                max_output_tokens=2500,
            ),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/onem", exist_ok=True)
    fichier = f"fichiers/onem/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def simulation_revenus():
    print("\n  Revenus Caelum Partners ce trimestre (€ brut) :")
    revenus_brut = input("  Revenus bruts → ").strip()
    print("  Allocations de chômage mensuelles actuelles (€) :")
    allocations = input("  Allocations/mois → ").strip() or "1000"
    if not revenus_brut:
        return
    try:
        brut = float(revenus_brut.replace(",", "."))
        alloc = float(allocations.replace(",", ".")) * 3  # trimestre
    except ValueError:
        print("  Montant invalide.")
        return

    r = streamer(
        f"""SIMULATION REVENUS TRIMESTRE — Chaima ONEM

Revenus Caelum ce trimestre (brut) : {brut}€
Estimation net après INASTI 20.5% : {brut * 0.795:.2f}€
Seuil ONEM isolé : {SEUIL_ONEM['isole']}€/trimestre net

Allocations de chômage ce trimestre : {alloc:.2f}€

Analyse complète :
1. SITUATION vs SEUIL : suis-je en dessous, proche ou au-dessus du seuil ?
2. MARGE RESTANTE : combien puis-je encore facturer ce trimestre sans risque ?
3. IMPACT SUR ALLOCATIONS : que se passe-t-il exactement si je dépasse ?
4. STRATÉGIE OPTIMALE : comment répartir les revenus sur les trimestres ?
5. DÉCLARATION ONEM : quels formulaires remplir et quand ?
6. CONSEIL IMMÉDIAT : que faire maintenant ?

AVERTISSEMENT : simulation indicative, confirmer avec le CSC.""",
        "SIMULATION REVENUS — CONFORMITÉ ONEM"
    )
    sauvegarder("simulation_revenus", r)


def alert_seuil():
    print("\n  Revenus cumulés depuis le début du trimestre (€ net) :")
    cumul = input("  Cumul net → ").strip()
    if not cumul:
        return
    try:
        c = float(cumul.replace(",", "."))
        marge = SEUIL_ONEM["isole"] - c
        pct = (c / SEUIL_ONEM["isole"]) * 100
    except ValueError:
        print("  Montant invalide.")
        return

    niveau = "🟢 SAFE" if pct < 70 else ("🟡 ATTENTION" if pct < 90 else "🔴 DANGER")
    print(f"\n  {niveau} — {pct:.1f}% du seuil utilisé | Marge restante : {marge:.2f}€")

    r = streamer(
        f"""Chaima a cumulé {cumul}€ net ce trimestre.
Seuil ONEM isolé : {SEUIL_ONEM['isole']}€
Marge restante : {marge:.2f}€ ({100 - pct:.1f}% libre)

Niveau d'alerte : {niveau}

Fournis :
1. ANALYSE DE RISQUE détaillée selon ce niveau
2. ACTIONS IMMÉDIATES recommandées
3. STRATÉGIE POUR LE RESTE DU TRIMESTRE (facturer plus, reporter, déclarer ?)
4. SI DÉPASSEMENT : conséquences exactes et procédure de régularisation
5. CONTACT CSC : quand appeler son syndicat (maintenant ou pas encore ?)""",
        f"ALERTE SEUIL ONEM — {pct:.0f}%"
    )
    sauvegarder(f"alerte_seuil_{pct:.0f}pct", r)


def formulaire_c45b():
    r = streamer(
        """Explique comment remplir le formulaire C45B de l'ONEM pour déclarer une activité indépendante complémentaire (Caelum Partners).

Contenu :
1. QU'EST-CE QUE LE C45B (à quoi ça sert, quand le remplir)
2. COMMENT OBTENIR LE FORMULAIRE (ONEM en ligne, CSC, commune)
3. INFORMATIONS À REMPLIR (case par case, explications simples)
4. DÉLAIS : quand déposer (avant de commencer l'activité !)
5. CONSÉQUENCES SI NON DÉCLARÉ (sanctions ONEM)
6. CAS CAELUM PARTNERS : qu'indiquer exactement pour cette activité IA

Format : guide pratique, clair, sans jargon administratif.""",
        "GUIDE FORMULAIRE C45B — ONEM"
    )
    sauvegarder("guide_c45b", r)


def optimisation_trimestrielle():
    print("\n  Revenus prévus sur les 4 prochains trimestres (estimation €/trimestre) :")
    t1 = input("  T1 → ").strip() or "1500"
    t2 = input("  T2 → ").strip() or "3000"
    t3 = input("  T3 → ").strip() or "5000"
    t4 = input("  T4 → ").strip() or "8000"
    r = streamer(
        f"""Chaima prévoit ces revenus Caelum Partners (bruts) :
T1 : {t1}€  T2 : {t2}€  T3 : {t3}€  T4 : {t4}€

Optimise la STRATÉGIE ONEM sur 12 mois :
1. ANALYSE TRIMESTRE PAR TRIMESTRE (safe / risque / dépassement)
2. POINT DE BASCULEMENT : à quel trimestre doit-elle basculer vers indépendant principal ?
3. STRATÉGIE DE LISSAGE : comment répartir les factures pour rester dans les seuils ?
4. SIMULATION REVENU TOTAL : avec allocations + Caelum, quel est le revenu optimal ?
5. TRANSITION : plan pour passer proprement au statut indépendant quand le moment est venu

Inclure les calculs bruts/nets. AVERTISSEMENT légal final.""",
        "OPTIMISATION TRIMESTRIELLE ONEM"
    )
    sauvegarder("optimisation_trimestrielle", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  REPORTING ONEM — Caelum Partners")
    print(f"  Seuil isolé : {SEUIL_ONEM['isole']}€/trimestre net")
    print("  ⚠️  Simulation indicative — confirmer avec le CSC")
    print("═"*65)

    while True:
        print("\n  1. Simulation revenus trimestre")
        print("  2. Alerte seuil (cumul actuel)")
        print("  3. Guide formulaire C45B (déclaration activité)")
        print("  4. Optimisation sur 12 mois")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            simulation_revenus()
        elif choix == "2":
            alert_seuil()
        elif choix == "3":
            formulaire_c45b()
        elif choix == "4":
            optimisation_trimestrielle()
        else:
            print("  Choix invalide.")
