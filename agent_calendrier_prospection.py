"""
AGENT CALENDRIER PROSPECTION [89] — Planning outreach, suivi relances, organisation
Organise la prospection quotidienne pour trouver 10 clients en 90 jours.

Usage : python agent_calendrier_prospection.py
"""

import os
import sys
from datetime import datetime, timedelta
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

IDENTITE = """# AGENT CALENDRIER PROSPECTION — Caelum Partners

## IDENTITÉ
Tu organises la prospection commerciale quotidienne de Chaima pour Caelum Partners.
Objectif : 10 clients en 90 jours, en partant de 0, seule, avec du temps limité.

## CONTEXTE
- Chaima est au chômage + en formation (temps disponible variable)
- Budget prospection : 0€ (LinkedIn gratuit uniquement)
- Marché : PME belges, Bruxelles d'abord
- Offres : 500€, 1500€, 3000€

## RYTHME CIBLE (RÉALISTE)
- 10 messages LinkedIn/jour (règle de sécurité anti-ban)
- 2-3 appels/semaine (prospects chauds)
- 1 proposition commerciale/semaine
- Relances : J+3, J+7, J+14 (3 touchpoints max)

## PIPELINE STANDARD
PROSPECT → CONTACT (message LinkedIn) → RÉPONSE → APPEL → PROPOSITION → SIGNATURE

## SECTEURS PRIORITAIRES (par ROI Caelum)
1. Cabinets comptables / fiduciaires (pain fort, budget, récurrent)
2. Avocats / notaires (besoin doc, conformité RGPD)
3. PME tech (comprennent la valeur IA)
4. HORECA (menus, réseaux sociaux, réservations)
5. Médical / paramédical (administratif, conformité INAMI)"""


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
                temperature=0.2,
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
    os.makedirs("fichiers/prospection", exist_ok=True)
    fichier = f"fichiers/prospection/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def planning_semaine():
    print("\n  Combien d'heures par jour peux-tu consacrer à la prospection cette semaine ?")
    heures = input("  Heures/jour → ").strip() or "2"
    print("  Secteur prioritaire cette semaine (ex: comptables, HORECA, avocats) :")
    secteur = input("  Secteur → ").strip() or "cabinets comptables"
    r = streamer(
        f"""Crée le PLANNING DE PROSPECTION SEMAINE pour Chaima.
Disponibilité : {heures}h/jour
Secteur prioritaire : {secteur}

FORMAT PAR JOUR (Lundi → Vendredi) :

LUNDI (ex: 2h)
- 0-30 min : [tâche précise]
- 30-60 min : [tâche précise]
- 60-90 min : [tâche précise]
- 90-120 min : [tâche précise]

Inclure pour la semaine :
✓ 50 messages LinkedIn envoyés (10/jour)
✓ Relances des prospects J+3 et J+7 de la semaine précédente
✓ 1-2 appels avec prospects chauds
✓ 1 proposition commerciale rédigée

Être très concret : pas "contacter des prospects" mais "envoyer 10 messages à des directeurs de cabinets comptables Bruxelles via LinkedIn".""",
        f"PLANNING SEMAINE — {secteur}"
    )
    sauvegarder(f"planning_semaine_{secteur.replace(' ', '_')}", r)


def plan_90_jours():
    r = streamer(
        """Crée le PLAN DE PROSPECTION 90 JOURS pour Caelum Partners.
Objectif : 10 clients payants en 90 jours, budget 0€, seule.

MOIS 1 (Jours 1-30) — Fondations
Semaine 1-2 : [actions précises]
Semaine 3-4 : [actions précises]
Objectif M1 : [métriques cibles]

MOIS 2 (Jours 31-60) — Accélération
Semaine 5-6 : [actions précises]
Semaine 7-8 : [actions précises]
Objectif M2 : [métriques cibles]

MOIS 3 (Jours 61-90) — Closing
Semaine 9-10 : [actions précises]
Semaine 11-13 : [actions précises]
Objectif M3 : 10 clients signés

Métriques à suivre chaque semaine :
- Messages envoyés
- Réponses reçues (taux cible)
- Appels réalisés
- Propositions envoyées
- Contrats signés""",
        "PLAN 90 JOURS — 0 à 10 CLIENTS"
    )
    sauvegarder("plan_90_jours", r)


def relances_automatiques():
    print("\n  Nom du prospect et date du 1er contact :")
    nom = input("  Prospect → ").strip()
    date_contact = input("  Date 1er contact (JJ/MM) → ").strip() or datetime.now().strftime("%d/%m")
    statut = input("  Statut actuel (pas de réponse / réponse tiède / intéressé) → ").strip() or "pas de réponse"
    if not nom:
        return
    r = streamer(
        f"""Crée la SÉQUENCE DE RELANCE pour le prospect : {nom}
Date 1er contact : {date_contact}
Statut : {statut}

Génère 3 messages de relance :

RELANCE J+3 (message LinkedIn, < 100 mots) :
[message naturel, ajouter de la valeur, pas "je relance juste"]

RELANCE J+7 (email ou LinkedIn, < 150 mots) :
[message avec insight sectoriel ou mini-cas concret]

RELANCE J+14 (dernière, < 80 mots) :
[clôture propre — laisser la porte ouverte sans pression]

Chaque relance : différente de la précédente, apporte quelque chose.""",
        f"RELANCES — {nom}"
    )
    sauvegarder(f"relances_{nom.replace(' ', '_')}", r)


def tableau_bord():
    print("\n  Décris ton pipeline actuel (prospects contactés, en cours, signés) :")
    pipeline = input("  Pipeline → ").strip() or "5 contactés, 2 réponses, 0 signé"
    r = streamer(
        f"""Analyse mon pipeline de prospection et donne les recommandations :
Pipeline actuel : {pipeline}

Fournis :
1. ANALYSE : taux de conversion à chaque étape (vs benchmark B2B de 2-5%)
2. GOULOT D'ÉTRANGLEMENT : où ça bloque et pourquoi
3. PRIORITÉ IMMÉDIATE : que faire AUJOURD'HUI pour débloquer une vente
4. PRÉVISION : si on maintient ce rythme, quand le 1er client ?
5. AJUSTEMENTS : 3 changements concrets pour améliorer le taux de conversion

Format : diagnostic rapide, actionnable.""",
        "TABLEAU DE BORD PROSPECTION"
    )
    sauvegarder("tableau_bord", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  CALENDRIER PROSPECTION — Caelum Partners")
    print("  Planning · Relances · 0 à 10 clients en 90 jours")
    print("═"*65)

    while True:
        print("\n  1. Planning de prospection cette semaine")
        print("  2. Plan 90 jours complet (0 → 10 clients)")
        print("  3. Séquence de relance pour un prospect")
        print("  4. Analyse du pipeline actuel")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            planning_semaine()
        elif choix == "2":
            plan_90_jours()
        elif choix == "3":
            relances_automatiques()
        elif choix == "4":
            tableau_bord()
        else:
            print("  Choix invalide.")
