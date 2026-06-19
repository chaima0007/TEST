"""
AGENT NÉGOCIATEUR [88] — Closing, objections, scripts de vente
Transforme les "je vais réfléchir" en signatures. Défend la valeur sans baisser les prix.

Usage : python agent_negociateur.py
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

IDENTITE = """# AGENT NÉGOCIATEUR — Caelum Partners

## IDENTITÉ
Tu es l'expert en négociation et closing de Caelum Partners.
Ta mission : transformer chaque "je réfléchis" en décision, sans jamais baisser les prix.

## OFFRES (NON NÉGOCIABLES À LA BAISSE)
- 500€ : site web IA, 7 jours
- 1 500€ : automation IA, 14 jours
- 3 000€ : pack complet, 30 jours

## PRINCIPES DE NÉGOCIATION
1. JAMAIS défendre le prix — défendre la valeur et le ROI
2. Comprendre l'objection RÉELLE (souvent ≠ objection exprimée)
3. "C'est trop cher" = "Je ne vois pas encore la valeur" → recadrer par le ROI
4. "Je vais réfléchir" = "Pas encore convaincu" → identifier le blocage réel
5. CONCESSIONS permises : paiement en 2x, démarrage décalé, offre d'essai 500€

## MÉTHODE CLOSING (MEDDIC adaptée PME belge)
M — Metrics : chiffrer le problème (heures perdues, CA manqué)
E — Economic Buyer : parler au décideur (pas l'assistante)
D — Decision Criteria : comprendre sur quoi il décide
D — Decision Process : qui signe, dans quel délai
I — Identify Pain : douleur réelle + impact émotionnel
C — Champion : trouver l'allié interne

## OBJECTIONS FRÉQUENTES PME BELGE
- "C'est trop cher" → ROI en 3 mois maximum
- "Je n'ai pas le temps de m'en occuper" → on gère tout, 1h de leur temps max
- "Je ne connais pas l'IA" → c'est pour ça qu'on est là, résultat visible en 7 jours
- "Je dois en parler à mon comptable" → on peut préparer le dossier financier
- "Je vais réfléchir" → qu'est-ce qui vous retient ? (identifier la vraie objection)"""


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
    os.makedirs("fichiers/negociation", exist_ok=True)
    fichier = f"fichiers/negociation/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def reponse_objection():
    print("\n  Quelle objection a dit le client ? (ex: 'c'est trop cher', 'je vais réfléchir') :")
    objection = input("  Objection → ").strip()
    print("  Contexte (secteur client, offre proposée) :")
    contexte = input("  Contexte → ").strip() or "PME belge, offre 1500€"
    if not objection:
        return
    r = streamer(
        f"""Le client dit : "{objection}"
Contexte : {contexte}

Génère la RÉPONSE DE NÉGOCIATION idéale :

1. ANALYSE : quelle est la vraie objection derrière ces mots ?
2. REFORMULATION EMPATHIQUE : montrer qu'on comprend (sans céder)
3. RECADRAGE ROI : chiffrer ce que ça lui coûte de ne pas agir
4. RÉPONSE DIRECTE : 2-3 phrases naturelles, à dire exactement
5. QUESTION DE REBOND : pour identifier le vrai blocage
6. SI TOUJOURS BLOQUÉ : proposition alternative (paiement 2x, offre d'entrée 500€)

Format : script à lire mot pour mot si besoin.""",
        f"OBJECTION — {objection[:40]}"
    )
    sauvegarder(f"objection_{objection[:20].replace(' ', '_')}", r)


def script_closing():
    print("\n  Stade de la vente (ex: 2ème appel, après devis envoyé, réunion finale) :")
    stade = input("  Stade → ").strip() or "après devis envoyé"
    print("  Offre concernée :")
    offre = input("  Offre → ").strip() or "1500€"
    print("  Ce que tu sais sur ce client (secteur, hésitation, décideur) :")
    contexte = input("  Contexte → ").strip() or "PME, hésitation sur le prix"
    r = streamer(
        f"""Crée un SCRIPT DE CLOSING complet pour :
Stade : {stade}
Offre : {offre}
Contexte client : {contexte}

Script en 5 étapes :
1. OUVERTURE (30 sec) : créer le bon contexte
2. VÉRIFICATION COMPRÉHENSION (1 min) : "Avant d'aller plus loin, est-ce que X et Y sont toujours vos priorités ?"
3. TRAITEMENT OBJECTIONS RESTANTES (2-3 min) : anticiper et adresser
4. FORMULATION DE L'OFFRE (1 min) : direct, sans hésitation
5. CLOSING QUESTION (30 sec) : demander la décision maintenant

Inclure les variantes si "oui", "non" ou "pas encore".""",
        f"SCRIPT CLOSING — {offre}"
    )
    sauvegarder(f"closing_{offre.replace('€', 'e')}", r)


def strategie_negociation():
    print("\n  Décris la situation de négociation :")
    situation = input("  Situation → ").strip()
    if not situation:
        return
    r = streamer(
        f"""Analyse cette situation de négociation et donne la stratégie optimale :
{situation}

Fournis :
1. POUVOIR EN PRÉSENCE : qui a le rapport de force ? Pourquoi ?
2. LEVIER PRINCIPAL : qu'est-ce qui fera basculer la décision ?
3. STRATÉGIE RECOMMANDÉE : étape par étape
4. CE QU'IL NE FAUT JAMAIS FAIRE dans cette situation
5. CONCESSIONS ACCEPTABLES (si nécessaire) vs LIGNES ROUGES
6. PLAN B si la négociation échoue""",
        "STRATÉGIE DE NÉGOCIATION"
    )
    sauvegarder("strategie_negociation", r)


def simuler_negociation():
    print("\n  Je vais simuler un client difficile. Décris son profil :")
    profil = input("  Profil client → ").strip() or "directeur comptable, très prudent sur les dépenses"
    print("  Tape tes réponses — je joue le client. Démarre la conversation.")
    print("\n" + "─"*65)

    contexte_sim = f"Tu joues le rôle d'un {profil} qui hésite à acheter l'offre 1500€ de Caelum Partners. Sois réaliste, pose des objections naturelles. Commence par dire bonjour et exprimer ton hésitation principale."

    historique = []
    r = streamer(contexte_sim, f"SIMULATION — {profil[:40]}")
    historique.append(f"[CLIENT] {r}")

    while True:
        reponse_user = input("\n  [TOI] → ").strip()
        if reponse_user.lower() in ["stop", "fin", "0"]:
            break
        historique_str = "\n".join(historique[-6:])
        suite = streamer(
            f"""Contexte de jeu de rôle — tu es un {profil} en négociation.
Historique récent :
{historique_str}

Vendeur dit : {reponse_user}

Réponds en restant dans le rôle. Continue les objections si pas encore convaincu. Cède progressivement si les arguments sont bons.""",
            ""
        )
        historique.append(f"[VENDEUR] {reponse_user}")
        historique.append(f"[CLIENT] {suite}")

    sauvegarder("simulation_negociation", "\n".join(historique))


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  NÉGOCIATEUR — Caelum Partners")
    print("  Objections · Closing · Scripts de vente")
    print("═"*65)

    while True:
        print("\n  1. Réponse à une objection spécifique")
        print("  2. Script de closing complet")
        print("  3. Stratégie pour situation complexe")
        print("  4. Simulation de négociation (jeu de rôle client)")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            reponse_objection()
        elif choix == "2":
            script_closing()
        elif choix == "3":
            strategie_negociation()
        elif choix == "4":
            simuler_negociation()
        else:
            print("  Choix invalide.")
