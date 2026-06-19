"""
AGENT ONBOARDING CLIENT [83] — Intégration post-signature, démarrage projet
Du contrat signé au projet lancé : séquence complète d'accueil client.

Usage : python agent_onboarding_client.py
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

IDENTITE = """# AGENT ONBOARDING CLIENT — Caelum Partners

## IDENTITÉ
Tu gères l'intégration des clients Caelum Partners après signature du contrat.
Ta mission : transformer un prospect signataire en client satisfait et engagé dès le 1er jour.

## OFFRES CAELUM
- 500€ (Site web IA, 7 jours)
- 1 500€ (Automation IA, 14 jours)
- 3 000€ (Pack complet, 30 jours)

## PROCESSUS ONBOARDING STANDARD
JOUR 0 (signature) : email bienvenue + accès espace client
JOUR 1 : réunion kick-off (30 min max, agenda précis)
JOUR 3 : questionnaire de démarrage rempli par le client
JOUR 7 : premier livrable intermédiaire partagé
JOUR 14 : point mi-parcours (offre 1500€) ou livraison finale (offre 500€)

## RÈGLES
- Réponse client < 4h pendant la phase active
- Tout livrable documenté (pas de surprise)
- Aligner les attentes dès le kick-off (périmètre = limite stricte)
- NPS demandé à J+7 (premier signe de satisfaction)
- Préparer l'upsell dès le kick-off (mentionner les prochaines étapes possibles)"""


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
    os.makedirs("fichiers/onboarding", exist_ok=True)
    fichier = f"fichiers/onboarding/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def email_bienvenue():
    print("\n  Nom du client :")
    nom = input("  Nom → ").strip()
    print("  Offre souscrite (500€ / 1500€ / 3000€) :")
    offre = input("  Offre → ").strip() or "1500€"
    print("  Secteur du client (ex: cabinet comptable, restaurant) :")
    secteur = input("  Secteur → ").strip() or "PME"
    if not nom:
        return
    r = streamer(
        f"""Écris l'EMAIL DE BIENVENUE pour le nouveau client :
Nom : {nom}
Offre : {offre}
Secteur : {secteur}

L'email doit :
1. Confirmer la signature et remercier chaleureusement
2. Présenter les prochaines étapes concrètes (avec dates)
3. Demander les éléments nécessaires au démarrage (accès, documents)
4. Donner le contact direct Chaima + délai de réponse garanti
5. Créer l'enthousiasme (ils ont pris la bonne décision)

Objet + Corps complet. Ton : professionnel mais humain.""",
        f"EMAIL BIENVENUE — {nom}"
    )
    sauvegarder(f"bienvenue_{nom.replace(' ', '_')}", r)


def plan_kickoff():
    print("\n  Nom du client et offre souscrite :")
    nom = input("  Nom + offre → ").strip()
    print("  Objectif principal du client (ex: automatiser ses relances factures) :")
    objectif = input("  Objectif → ").strip()
    if not nom:
        return
    r = streamer(
        f"""Prépare l'AGENDA DE RÉUNION KICK-OFF pour : {nom}
Objectif client : {objectif}

Format agenda (30 minutes) :
- 0-5 min : accueil, présentation, objectif de la réunion
- 5-15 min : découverte approfondie (questions spécifiques à poser)
- 15-20 min : présentation du plan de livraison (timeline, livrables)
- 20-25 min : validation du périmètre (ce qu'on fait, ce qu'on ne fait PAS)
- 25-30 min : prochaines étapes + éléments à fournir par le client

Inclure : liste des questions à poser + pièges à éviter (scope creep).""",
        f"AGENDA KICK-OFF — {nom}"
    )
    sauvegarder(f"kickoff_{nom[:20].replace(' ', '_')}", r)


def questionnaire_demarrage():
    print("\n  Secteur du client :")
    secteur = input("  Secteur → ").strip() or "PME"
    print("  Type de mission (site web / automation / pack complet) :")
    mission = input("  Mission → ").strip() or "automation"
    r = streamer(
        f"""Crée un QUESTIONNAIRE DE DÉMARRAGE pour un client {secteur} — mission : {mission}

Le questionnaire doit collecter :
1. Informations business (secteur, taille, volume)
2. Problèmes actuels (processus manuels, temps perdu)
3. Outils existants (logiciels utilisés, intégrations nécessaires)
4. Accès techniques (emails, identifiants à partager sécurisément)
5. Objectifs mesurables (KPIs attendus)
6. Contraintes (délais, budget supplémentaire, personnes impliquées)

Format : questions numérotées, réponse courte ou choix multiple.
Max 15 questions. Pratique à remplir en 10 minutes.""",
        f"QUESTIONNAIRE DÉMARRAGE — {secteur}"
    )
    sauvegarder(f"questionnaire_{secteur.replace(' ', '_')}", r)


def checklist_livraison():
    print("\n  Type de livraison (site web / automation / pack complet) :")
    livraison = input("  Type → ").strip() or "automation"
    r = streamer(
        f"""Crée une CHECKLIST DE LIVRAISON pour {livraison} Caelum Partners.

Sections :
AVANT LIVRAISON (ce que Caelum doit vérifier en interne) :
□ Tests fonctionnels
□ Documentation
□ Sécurité des données
□ Performance

RÉUNION DE LIVRAISON (agenda 30-45 min) :
□ Démo complète
□ Formation utilisateur
□ Questions/réponses
□ Validation signée

APRÈS LIVRAISON (J+1, J+7, J+30) :
□ Email de suivi
□ Disponibilité support
□ Demande NPS
□ Proposition upsell

Format : checklist prête à utiliser, cases à cocher.""",
        f"CHECKLIST LIVRAISON — {livraison}"
    )
    sauvegarder(f"checklist_{livraison.replace(' ', '_')}", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  ONBOARDING CLIENT — Caelum Partners")
    print("  Du contrat signé au client satisfait")
    print("═"*65)

    while True:
        print("\n  1. Email de bienvenue (post-signature)")
        print("  2. Agenda réunion kick-off")
        print("  3. Questionnaire de démarrage client")
        print("  4. Checklist de livraison")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            email_bienvenue()
        elif choix == "2":
            plan_kickoff()
        elif choix == "3":
            questionnaire_demarrage()
        elif choix == "4":
            checklist_livraison()
        else:
            print("  Choix invalide.")
