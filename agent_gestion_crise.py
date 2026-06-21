"""
AGENT GESTION DE CRISE MAJEURE [96] — Protocoles de continuité, communication, confinement
Cyberattaque, scandale public, rupture logistique : activation immédiate des plans d'urgence.

Usage : python agent_gestion_crise.py
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

IDENTITE = """# AGENT GESTION DE CRISE MAJEURE — Caelum Partners

## IDENTITÉ
Tu es le responsable de crise de Caelum Partners.
Tu actives les protocoles d'urgence et gères la communication en situation critique.
Réponse en moins de 15 minutes. Protocoles clairs. Pas de panique.

## TYPES DE CRISES COUVERTS
1. CYBER : ransomware, fuite de données client, compromission API key
2. RÉPUTATION : bad buzz LinkedIn, client mécontent viral, fausse accusation
3. LÉGALE : mise en demeure, plainte RGPD à l'APD, conflit contractuel
4. OPÉRATIONNELLE : panne API Gemini, perte accès GitHub, PC hors service
5. FINANCIÈRE : client défaillant (impayé majeur), dépense imprévue critique
6. PERSONNELLE : Chaima indisponible (maladie, accident), surcharge

## PRINCIPES DE GESTION DE CRISE
- CONFINER D'ABORD : arrêter la propagation avant de communiquer
- COMMUNIQUER VITE : mieux vaut 1 message incomplet que le silence
- DOCUMENT TOUT : chaque action horodatée (essentiel pour le légal)
- 1 PORTE-PAROLE : Chaima uniquement, jamais de messages contradictoires
- PLAN B ACTIF : identifier l'alternative avant d'en avoir besoin

## NIVEAUX D'ALERTE
🟢 VERT : situation normale
🟡 JAUNE : alerte précoce — surveiller, préparer
🟠 ORANGE : crise en développement — activer plan partiel
🔴 ROUGE : crise active — activer tous les protocoles
⚫ NOIR : crise existentielle — mode survie business"""


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
                max_output_tokens=3000,
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
    os.makedirs("fichiers/crise", exist_ok=True)
    fichier = f"fichiers/crise/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def activation_urgence():
    print("\n⚠️  ACTIVATION PROTOCOLE D'URGENCE")
    print("  Type de crise (cyber / réputation / légale / opérationnelle / financière / personnelle) :")
    type_crise = input("  Type → ").strip().lower()
    print("  Décris la situation en 2-3 phrases :")
    situation = input("  Situation → ").strip()
    if not situation:
        return
    r = streamer(
        f"""🚨 ACTIVATION PROTOCOLE CRISE — {type_crise.upper()}
HEURE D'ACTIVATION : {datetime.now().strftime('%d/%m/%Y %H:%M')}

SITUATION : {situation}

PROTOCOLE D'URGENCE — EXÉCUTER DANS L'ORDRE :

⏱️ DANS LES 15 PREMIÈRES MINUTES (confinement) :
[actions immédiates pour arrêter la propagation]

⏱️ DANS L'HEURE (stabilisation) :
[actions pour stabiliser la situation]

⏱️ DANS LES 24H (gestion) :
[communication, documentation, plan de reprise]

📋 COMMUNICATION IMMÉDIATE À RÉDIGER :
[message à envoyer aux clients/partenaires concernés — si nécessaire]

📊 INDICATEURS DE SORTIE DE CRISE :
[comment savoir que c'est terminé]

⚖️ DOCUMENTATION LÉGALE REQUISE :
[ce qu'il faut tracer pour se protéger]

✅ LEÇON À INTÉGRER :
[comment éviter que ça se reproduise]""",
        f"🚨 CRISE {type_crise.upper()} — PROTOCOLE ACTIVÉ"
    )
    sauvegarder(f"crise_{type_crise}_{datetime.now().strftime('%Y%m%d_%H%M')}", r)


def communication_crise():
    print("\n  Type de crise et destinataire du message :")
    situation = input("  Situation + destinataire → ").strip()
    if not situation:
        return
    r = streamer(
        f"""Rédige les MESSAGES DE COMMUNICATION DE CRISE pour : {situation}

Génère 3 messages adaptés :

MESSAGE 1 — INTERNE (à soi-même / notes de suivi)
Format : log horodaté, factuel, juridiquement solide

MESSAGE 2 — CLIENT CONCERNÉ (si impact client)
Format : email professionnel, empathique, sans admettre de faute,
avec action concrète et délai de résolution

MESSAGE 3 — RÉSEAU (si la crise est publique / LinkedIn)
Format : post de 100 mots max, transparent, humain, proactif
(parfois le silence est meilleur — indiquer quand ne pas communiquer)

Ton dans tous les cas : calme, professionnel, jamais défensif.""",
        "COMMUNICATION DE CRISE"
    )
    sauvegarder("communication_crise", r)


def plan_continuite():
    print("\n  Actif ou service dont la perte pourrait paralyser Caelum :")
    actif = input("  Actif critique → ").strip() or "accès API Gemini"
    r = streamer(
        f"""PLAN DE CONTINUITÉ pour perte de : {actif}

Génère le plan complet :

1. SCÉNARIO : comment cela se produit-il ?
2. DURÉE ESTIMÉE D'INTERRUPTION : combien de temps dans le pire cas ?
3. IMPACT IMMÉDIAT : quelles opérations sont bloquées ?
4. PLAN B OPÉRATIONNEL : quelle alternative disponible dans les 30 minutes ?
5. PLAN B LONG TERME : alternative durable si l'interruption dure > 48h
6. COMMUNICATION CLIENT : que dire si un délai est affecté ?
7. PROCÉDURE DE RESTAURATION : comment revenir à la normale ?
8. PRÉVENTION : que faire maintenant pour réduire ce risque ?""",
        f"PLAN CONTINUITÉ — {actif}"
    )
    sauvegarder(f"continuite_{actif.replace(' ', '_')}", r)


def checklist_prevention():
    r = streamer(
        """Génère la CHECKLIST MENSUELLE DE PRÉVENTION DES CRISES pour Caelum Partners.

Vérifications à faire chaque mois :

🔐 SÉCURITÉ (15 min)
□ [check 1]
□ [check 2]
[...]

💼 LÉGAL & CONTRACTUEL (10 min)
□ [check 1]
[...]

💰 FINANCIER (10 min)
□ [check 1]
[...]

🤝 CLIENTS (10 min)
□ [check 1]
[...]

🖥️ TECHNIQUE (10 min)
□ [check 1]
[...]

FORMAT : checklist pratique, avec la conséquence si la case n'est pas cochée.""",
        "CHECKLIST PRÉVENTION MENSUELLE"
    )
    sauvegarder("checklist_prevention_mensuelle", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  GESTION DE CRISE MAJEURE — Caelum Partners")
    print("  Activation · Communication · Continuité · Prévention")
    print("═"*65)

    while True:
        print("\n  1. 🚨 ACTIVATION URGENCE (crise en cours)")
        print("  2. Rédiger communication de crise")
        print("  3. Plan de continuité (actif critique)")
        print("  4. Checklist prévention mensuelle")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            activation_urgence()
        elif choix == "2":
            communication_crise()
        elif choix == "3":
            plan_continuite()
        elif choix == "4":
            checklist_prevention()
        else:
            print("  Choix invalide.")
