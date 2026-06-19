"""
AGENT SATISFACTION & UPSELL [84] — NPS, fidélisation, montée en gamme
Mesure la satisfaction client, détecte le churn, déclenche les upsells au bon moment.

Usage : python agent_satisfaction_upsell.py
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

IDENTITE = """# AGENT SATISFACTION & UPSELL — Caelum Partners

## IDENTITÉ
Tu gères la satisfaction client et la montée en gamme (upsell) pour Caelum Partners.
Un client satisfait = source de recommandations. Un client qui monte en gamme = CA multiplié sans coût d'acquisition.

## OFFRES CAELUM (progression naturelle)
- 500€ : site web IA (7 jours) → upsell vers 1 500€ automation
- 1 500€ : automation IA (14 jours) → upsell vers 3 000€ pack complet
- 3 000€ : pack complet (30 jours) → upsell vers retainer mensuel ou nouveau projet

## SIGNAUX DE CHURN (alerte rouge)
- Pas de réponse depuis 5+ jours
- Plainte non résolue en 24h
- Demande de remboursement ou de délai
- Score NPS < 6

## SIGNAUX D'UPSELL (moment parfait)
- NPS ≥ 8 (promoteur)
- Client mentionne un nouveau problème
- Livraison reçue avec enthousiasme (emojis, merci, "c'est parfait")
- J+30 après livraison (impact visible)

## RÈGLES
- Ne jamais forcer l'upsell — créer le désir
- Partir toujours du résultat obtenu pour proposer la suite
- Offrir une valeur immédiate avant de demander
- Témoignage/référence demandé seulement si NPS ≥ 8"""


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
                temperature=0.25,
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
    os.makedirs("fichiers/satisfaction", exist_ok=True)
    fichier = f"fichiers/satisfaction/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def sondage_nps():
    print("\n  Nom du client et offre livrée :")
    nom = input("  Client → ").strip()
    offre = input("  Offre → ").strip() or "1500€"
    if not nom:
        return
    r = streamer(
        f"""Crée un EMAIL DE SONDAGE NPS pour {nom} (offre {offre} livrée).

L'email doit :
1. Remercier pour la confiance accordée
2. Partager un résumé des résultats obtenus
3. Demander UNE SEULE question : "De 0 à 10, dans quelle mesure recommanderiez-vous Caelum Partners ?"
4. Proposer un champ texte libre optionnel
5. Être court (< 150 mots)
6. Lien fictif vers formulaire : forms.caelumpartners.agency/nps

Ton : chaleureux, pas commercial.""",
        f"EMAIL NPS — {nom}"
    )
    sauvegarder(f"nps_{nom.replace(' ', '_')}", r)


def sequence_upsell():
    print("\n  Nom du client, offre actuelle, score NPS :")
    nom = input("  Client → ").strip()
    offre_actuelle = input("  Offre actuelle → ").strip() or "500€"
    nps = input("  Score NPS (0-10) → ").strip() or "9"
    if not nom:
        return
    r = streamer(
        f"""Crée une SÉQUENCE UPSELL pour {nom} :
Offre actuelle : {offre_actuelle}
Score NPS : {nps}/10

Génère 3 emails espacés de 7 jours :

EMAIL 1 (J+0 — juste après NPS positif) :
- Remercier du score
- Partager 1 insight sur ce qu'on pourrait faire de plus
- Pas de prix encore

EMAIL 2 (J+7 — offre naturelle) :
- Partir du résultat obtenu
- Présenter la prochaine offre comme évolution logique
- Chiffrer le bénéfice supplémentaire
- CTA : appel de 20 min

EMAIL 3 (J+14 — dernière chance douce) :
- Urgence naturelle (disponibilité limitée)
- Témoignage ou stat
- Offre optionnelle (pas de pression)""",
        f"SÉQUENCE UPSELL — {nom}"
    )
    sauvegarder(f"upsell_{nom.replace(' ', '_')}", r)


def alerte_churn():
    print("\n  Décris le comportement inquiétant du client :")
    comportement = input("  Comportement → ").strip()
    nom = input("  Nom du client → ").strip()
    if not comportement:
        return
    r = streamer(
        f"""ALERTE CHURN — Client : {nom}
Comportement observé : {comportement}

Analyse :
1. NIVEAU DE RISQUE : Faible / Moyen / Élevé (avec justification)
2. CAUSE PROBABLE : qu'est-ce qui a pu se passer ?
3. ACTION IMMÉDIATE : quoi faire dans les 24h
4. EMAIL DE RÉCUPÉRATION : message à envoyer maintenant
5. SCRIPT D'APPEL : si le client répond pour une mise au point

Objectif : sauver la relation ET la réputation de Caelum.""",
        f"ALERTE CHURN — {nom}"
    )
    sauvegarder(f"churn_{nom.replace(' ', '_')}", r)


def demande_temoignage():
    print("\n  Nom du client + résultat obtenu :")
    nom = input("  Client → ").strip()
    resultat = input("  Résultat obtenu → ").strip() or "automation mise en place avec succès"
    if not nom:
        return
    r = streamer(
        f"""Crée un EMAIL DE DEMANDE DE TÉMOIGNAGE pour {nom}.
Résultat obtenu : {resultat}

L'email doit :
1. Célébrer le résultat ensemble
2. Demander un témoignage de manière naturelle (pas forcée)
3. Proposer 3 formats au choix : texte 2-3 phrases / avis Google / post LinkedIn
4. Offrir de rédiger le brouillon pour eux (max 2 phrases à valider)
5. Mentionner la contrepartie (visibilité LinkedIn pour leur entreprise)

Format témoignage idéal à demander :
"Avant [problème]. Après Caelum [résultat]. Je recommande parce que [raison]." """,
        f"DEMANDE TÉMOIGNAGE — {nom}"
    )
    sauvegarder(f"temoignage_{nom.replace(' ', '_')}", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  SATISFACTION & UPSELL — Caelum Partners")
    print("  NPS · Fidélisation · Montée en gamme · Témoignages")
    print("═"*65)

    while True:
        print("\n  1. Créer sondage NPS (post-livraison)")
        print("  2. Séquence upsell (client satisfait)")
        print("  3. Alerte churn (client silencieux ou mécontent)")
        print("  4. Demande de témoignage")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            sondage_nps()
        elif choix == "2":
            sequence_upsell()
        elif choix == "3":
            alerte_churn()
        elif choix == "4":
            demande_temoignage()
        else:
            print("  Choix invalide.")
