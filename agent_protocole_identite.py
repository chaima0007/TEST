"""
AGENT PROTOCOLE D'IDENTITÉ — Gardien de l'identité Caelum Partners
Identité · Mission · Audit de cohérence · Directive de communication
Mission : chaque interaction reflète qui est Caelum Partners

Usage : python agent_protocole_identite.py
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

IDENTITE = """# AGENT PROTOCOLE D'IDENTITÉ — GARDIEN DE L'IDENTITÉ CAELUM

## IDENTITÉ
Tu es le Protocole d'Identité de Caelum Partners.
Tu détiens la définition exacte de qui est Caelum Partners, ce qu'elle représente,
comment elle parle, ce qu'elle refuse, et ce qu'elle incarne dans chaque interaction.

## MISSION
Garantir que chaque touchpoint — email, proposition, LinkedIn, facture, appel —
exprime la même identité cohérente et puissante de Caelum Partners.
L'identité est le premier actif de l'empire : elle se construit par la répétition
et se détruit par l'incohérence.

## IDENTITÉ OFFICIELLE DE CAELUM PARTNERS

### QUI EST CAELUM PARTNERS ?
Caelum Partners est l'agence IA de référence pour les PME belges.
Fondée par Chaima Mhadbi, Bruxelles.
Mission : rendre l'intelligence artificielle accessible, concrète et rentable
pour les entreprises qui n'ont ni le temps ni les ressources d'une grande structure.

### CE QUE CAELUM PARTNERS N'EST PAS
- Pas une agence web généraliste
- Pas un freelance qui "fait de l'IA"
- Pas une startup qui cherche des fonds
- Pas une consultante qui vend du conseil théorique

### LES 5 VALEURS D'IDENTITÉ
1. CONCRÉTUDE : on livre des résultats mesurables, pas des slides
2. RAPIDITÉ : 7 jours pour un site, 14 jours pour une automation — promesse tenue
3. PROXIMITÉ : une seule personne, un seul interlocuteur, zéro perte d'information
4. LÉGITIMITÉ LÉGALE : conformité belge intégrée dans chaque livrable
5. EXCELLENCE SANS COMPLEXITÉ : technologie de pointe, explications simples

### TON DE COMMUNICATION
- Direct et confiant (pas arrogant, pas humble au point d'être invisible)
- Concret et chiffré (toujours un exemple, toujours un résultat tangible)
- Professionnel mais humain (pas de jargon, pas de langue de bois corporate)
- Bilingue FR/NL quand le contexte l'exige
- Jamais : "je pense que", "peut-être", "ça dépend" sans suite concrète

### POSITIONNEMENT PRIX
- 500€ : entrée de gamme, site web professionnel en 7 jours
- 1 500€ : automation IA sur mesure, ROI en 30 jours
- 3 000€ : pack complet, transformation digitale PME
- Ces prix ne se négocient pas à la baisse — ils se justifient par le ROI

## PROTOCOLE D'AUDIT D'IDENTITÉ
Pour chaque contenu soumis, vérifier :
- Exprime-t-il la valeur concrète de Caelum (pas juste "on fait de l'IA") ?
- Le ton est-il confiant sans être arrogant ?
- Y a-t-il un résultat chiffré ou un exemple concret ?
- L'identité "PME belge" est-elle visible ?
- Le call-to-action est-il clair et sans friction ?

## DIRECTIVE DE COMPORTEMENT
- Toujours reformuler dans le ton Caelum, jamais réécrire de zéro sans raison
- Signaler chaque déviation d'identité avec le correctif précis
- Défendre le positionnement prix — ne jamais suggérer de baisser
- Maintenir la cohérence entre tous les canaux (LinkedIn = email = proposition = appel)"""


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
                temperature=0.15,
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
    os.makedirs("fichiers/protocole_identite", exist_ok=True)
    fichier = f"fichiers/protocole_identite/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def auditer_coherence_identite():
    """Vérifie si un contenu est cohérent avec l'identité Caelum."""
    print("\n  Colle le contenu à auditer (email, post, proposition, bio...)\n")
    lignes, vide = [], 0
    while vide < 2:
        ligne = input()
        if ligne == "":
            vide += 1
        else:
            vide = 0
            lignes.append(ligne)
    contenu = "\n".join(lignes).strip()[:3000]
    if not contenu:
        return
    r = streamer(
        f"""AUDIT D'IDENTITÉ — Cohérence avec Caelum Partners

CONTENU SOUMIS :
{contenu}

ANALYSER SUR 5 CRITÈRES D'IDENTITÉ :
1. VALEUR CONCRÈTE : le contenu communique-t-il un résultat tangible ?
   → Score /10 + déviation détectée + version corrigée si besoin

2. TON CAELUM : confiant, direct, sans jargon ni langue de bois ?
   → Score /10 + mots ou phrases qui dévient + corrections

3. PREUVE CONCRÈTE : y a-t-il un chiffre, un délai, un exemple réel ?
   → Score /10 + ce qui manque + version enrichie

4. IDENTITÉ PME BELGE : la spécificité belge est-elle visible ?
   → Score /10 + opportunités manquées d'ancrage belge

5. CALL-TO-ACTION : l'action suivante est-elle claire et sans friction ?
   → Score /10 + reformulation si nécessaire

SCORE IDENTITÉ TOTAL /50
VERSION RÉALIGNÉE (le même contenu, 100% identité Caelum)""",
        "AUDIT IDENTITÉ CAELUM"
    )
    sauvegarder("audit_identite", r)


def generer_bio_officielle():
    """Génère les 3 versions de la bio officielle Caelum Partners."""
    r = streamer(
        """Génère les 3 versions officielles de la bio de Chaima Mhadbi / Caelum Partners.

VERSION 1 — BIO COURTE (50 mots) pour LinkedIn headline ou signature email
VERSION 2 — BIO MOYENNE (150 mots) pour profil LinkedIn ou page "À propos" site
VERSION 3 — BIO LONGUE (300 mots) pour articles, interviews, dossiers de presse

POUR CHAQUE VERSION :
- Ton Caelum : confiant, concret, sans arrogance
- Mention : Bruxelles, Belgique, PME belges, IA concrète
- Inclure : ce qu'elle fait + pour qui + résultat concret + ce qui la différencie
- Éviter : buzzwords vides ("passionnée par", "experte en", "j'accompagne")

Générer aussi : 3 accroches LinkedIn alternatives (une ligne chacune)""",
        "BIO OFFICIELLE — Chaima Mhadbi / Caelum Partners"
    )
    sauvegarder("bio_officielle", r)


def reformuler_dans_ton_caelum():
    """Reformule n'importe quel texte dans le ton officiel Caelum."""
    print("\n  Texte à reformuler dans le ton Caelum Partners\n")
    texte = input("  Texte → ").strip()[:2000]
    if not texte:
        return
    r = streamer(
        f"""REFORMULATION IDENTITÉ CAELUM

Texte original : {texte}

REFORMULER dans le ton exact de Caelum Partners :
- Direct et confiant
- Résultat concret chiffré si possible
- PME belge ancré
- Call-to-action clair

Livrer :
1. VERSION REFORMULÉE (prête à utiliser)
2. LISTE DES CHANGEMENTS (ce qui a été modifié et pourquoi)
3. VARIANTE ALTERNATIVE (ton légèrement différent, même message)""",
        "REFORMULATION TON CAELUM"
    )
    sauvegarder("reformulation_caelum", r)


def charte_identite_complete():
    """Génère la charte d'identité complète de Caelum Partners."""
    r = streamer(
        """Génère la CHARTE D'IDENTITÉ COMPLÈTE de Caelum Partners.
Document de référence utilisé par tous les agents de la flotte.

SECTIONS OBLIGATOIRES :
1. QUI NOUS SOMMES (2 paragraphes, définition non négociable)
2. CE QUE NOUS FAISONS (avec exemples concrets pour chaque service)
3. POUR QUI (profil client idéal : secteur, taille, problème, budget)
4. CE QUI NOUS DIFFÉRENCIE (3 différenciateurs uniques, non copiables)
5. NOS VALEURS (5 valeurs avec définition opérationnelle — pas des mots creux)
6. TON DE COMMUNICATION (avec exemples : formule à utiliser / formule à éviter)
7. POSITIONNEMENT PRIX (justification du 500/1500/3000€)
8. CE QUE NOUS REFUSONS (les types de clients/projets à décliner)
9. NOTRE PROMESSE CLIENT (ce qu'on garantit à chaque client)
10. VISION (où sera Caelum Partners dans 5 ans)

Format : document professionnel, applicable immédiatement par tous les agents.""",
        "CHARTE D'IDENTITÉ — Caelum Partners"
    )
    sauvegarder("charte_identite_caelum", r)


def kit_onboarding_client_identite():
    """Génère le kit d'onboarding qui communique l'identité au premier client."""
    r = streamer(
        """Génère le KIT D'ONBOARDING CLIENT de Caelum Partners.
Ce kit est envoyé au premier client dès la signature du contrat.
Il doit communiquer l'identité et les standards de Caelum dès le premier contact.

CONTENU DU KIT :
1. EMAIL DE BIENVENUE (ton Caelum, chaleureux mais professionnel, avec les prochaines étapes)
2. DOCUMENT "COMMENT TRAVAILLE CAELUM PARTNERS" (processus, délais, modes de communication)
3. FORMULAIRE DE BRIEF CLIENT (questions pour cadrer le projet parfaitement)
4. PROMESSE DE LIVRAISON (engagement signable — ce qu'on promet, ce qu'on ne promet pas)
5. CONTACT D'URGENCE ET DISPONIBILITÉS (disponibilité réaliste pour une solopreneuse)

Ton : professionnel, rassurant, qui donne confiance dès le premier email.""",
        "KIT ONBOARDING CLIENT — Identité Caelum"
    )
    sauvegarder("kit_onboarding_client", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  PROTOCOLE D'IDENTITÉ — Gardien de l'Identité Caelum")
    print("  Cohérence · Ton · Positionnement · Charte officielle")
    print("═"*65)

    while True:
        print("\n  1. Auditer la cohérence identité d'un contenu")
        print("  2. Générer les 3 versions de la bio officielle")
        print("  3. Reformuler dans le ton Caelum Partners")
        print("  4. Générer la charte d'identité complète")
        print("  5. Kit onboarding premier client")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            auditer_coherence_identite()
        elif choix == "2":
            generer_bio_officielle()
        elif choix == "3":
            reformuler_dans_ton_caelum()
        elif choix == "4":
            charte_identite_complete()
        elif choix == "5":
            kit_onboarding_client_identite()
        else:
            print("  Choix invalide.")
