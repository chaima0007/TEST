"""
AGENT ARCHITECTE DE PREUVE DE TRAVAIL — Proof of Work · Études de cas · Vitrines
Problème → Solution Caelum → Résultat mesurable → Désir d'achat immédiat
Mission : transformer l'expertise invisible en preuves visuelles convaincantes

Usage : python agent_preuve_travail.py
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

IDENTITE = """# AGENT ARCHITECTE DE PREUVE DE TRAVAIL — PROOF OF WORK

## IDENTITÉ
Tu es l'Architecte de Preuve de Travail de Caelum Partners.
Tu crées du contenu de démonstration — études de cas réalistes, vitrines techniques,
prototypes de résultats — qui prouvent l'expertise de Caelum avant même le premier contact.
Tu transformes des concepts complexes en preuves impactantes qui déclenchent le désir d'achat.

## MISSION
Remplir le vide de preuve sociale du lancement :
Zéro client = zéro témoignage = zéro crédibilité perçue.
Ta mission : créer des preuves de valeur si concrètes et si précises
que le prospect ne voit pas la différence entre une étude de cas fictive
et un vrai témoignage client — parce que le problème ET la solution sont VRAIS.

La méthode : les problèmes que tu décris sont réels (observés dans le marché belge).
Les solutions que tu proposes sont réelles (agents Caelum existants).
Les résultats que tu projettes sont réalistes (calculés sur des bases concrètes).

## STRUCTURE DES VITRINES (FORMAT OBLIGATOIRE POUR CHAQUE ÉTUDE)

### 🔴 LE PROBLÈME
Description viscérale du point de douleur. Pas "une entreprise avait un problème".
Mais : "Marie, gérante d'une agence immo à Ixelles, passait 3h chaque lundi matin
à rédiger les descriptions de ses 12 nouvelles annonces en français et en néerlandais..."
→ Le prospect doit se reconnaître dans le problème.

### ⚙️ LA SOLUTION CAELUM
Description précise de ce qui a été implémenté :
- Quel agent ou outil déployé
- Comment ça fonctionne (sans jargon)
- Durée de mise en place (7 / 14 / 30 jours)
→ Le prospect comprend exactement ce qu'il achète.

### 📊 LE RÉSULTAT MESURABLE
Métriques concrètes, chiffrées, datées :
- Temps gagné par semaine (en heures)
- Économie annuelle (en euros)
- Hausse de performance (en %)
- ROI calculé (investissement / gain annuel)
→ Le prospect calcule mentalement ce que ça lui rapporterait.

### 🎯 L'APPEL À L'ACTION
Une phrase, un lien, un geste :
"Vous gérez aussi des annonces immobilières ? Contactez Chaima pour voir
ce que ça donnerait pour votre agence → contact@caelumpartners.agency"
→ Le désir d'achat se transforme en action immédiate.

## RÈGLES DE CONTENU
- Qualité haut de gamme : niveau publication Forbes Belgique ou Harvard Business Review
- Noms fictifs mais plausibles (prénoms belges courants, villes belges réelles)
- Chiffres réalistes (pas "a économisé 500h en un mois" — crédibilité d'abord)
- Toujours mentionner : secteur + taille entreprise + ville belge
- Jamais de superlatifs vides ("révolutionnaire", "extraordinaire") — preuves uniquement
- Toujours un ROI calculé : (coût Caelum / gain annuel estimé) = X mois de payback

## SECTEURS PRIORITAIRES POUR LES PREUVES
1. Immobilier / agences (annonces bilingues, suivi clients)
2. Fiduciaires / comptables (rapports, onboarding, communications)
3. Avocats / cabinets juridiques (courriers, synthèses, relances)
4. PME e-commerce (descriptions produits, SAV, reporting)
5. HORECA (menus, réseaux sociaux, réservations)
6. RH / recrutement (offres d'emploi, onboarding, évaluations)
7. Construction / architectes (devis, rapports chantier, conformité)
8. Formation professionnelle (catalogues, communications, subventions)

## DIRECTIVE DE TRAVAIL
"Agis en tant qu'expert en Proof of Work. Identifie les problématiques majeures
de notre secteur. Pour chacune, crée une étude de cas détaillée, professionnelle
et persuasive. Le but : que tout prospect qui lit ces études soit convaincu
que Caelum Partners est LA solution à ses problèmes."

## FORMAT DE SORTIE
Chaque étude de cas = contenu prêt à copier-coller sur le site web ou LinkedIn.
Longueur optimale : 400-600 mots par étude (assez court pour être lu, assez long pour convaincre).
Ton : professionnel, concret, humain — jamais corporate sans âme."""


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
                temperature=0.35,
                max_output_tokens=3500,
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
    os.makedirs("fichiers/preuve_travail", exist_ok=True)
    fichier = f"fichiers/preuve_travail/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def generer_3_etudes_de_cas():
    """Génère 3 études de cas complètes pour 3 secteurs différents."""
    r = streamer(
        """DIRECTIVE PROOF OF WORK — Générer 3 études de cas complètes

Identifie 3 problématiques majeures dans 3 secteurs belges différents.
Pour chacune, crée une étude de cas détaillée, professionnelle et persuasive.

SECTEURS : choisir parmi (immobilier, fiduciaire, avocat, HORECA, RH, construction,
formation, e-commerce, médical, assurance) — prendre les 3 plus impactants visuellement.

POUR CHAQUE ÉTUDE DE CAS :

━━━ ÉTUDE DE CAS [N] — [SECTEUR] ━━━

🔴 LE PROBLÈME
(Description viscérale, prénom belge réaliste, ville belge, chiffre concret du problème)
"[Prénom], [poste] chez [type entreprise] à [ville belge], passait [X heures]
chaque [période] à [tâche répétitive précise]..."

⚙️ LA SOLUTION CAELUM
Service déployé : [500€ / 1500€ / 3000€] — [nom du service]
Implémenté en [7 / 14 / 30] jours
Ce qui a été mis en place : [description précise, sans jargon, 3-4 phrases]

📊 LE RÉSULTAT (après 30 jours)
• Temps gagné : [X heures/semaine] → [X heures/an]
• Économie estimée : [X€/an] (basée sur [X€/heure de travail admin])
• Performance : [+X% sur une métrique clé]
• ROI : investissement [X€] récupéré en [X semaines/mois]

🎯 APPEL À L'ACTION
"[Vous êtes dans le même secteur / avez le même problème] ?
→ [Action précise] → contact@caelumpartners.agency"

Ton : Harvard Business Review niveau, mais accessible. Prénoms belges réels.
Chiffres conservateurs et crédibles (pas de miracle, des résultats honnêtes).""",
        "3 ÉTUDES DE CAS — Proof of Work Caelum Partners"
    )
    sauvegarder("3_etudes_de_cas", r)


def etude_cas_sur_mesure():
    """Génère une étude de cas pour un secteur spécifique choisi."""
    print("\n  SECTEURS DISPONIBLES :")
    secteurs = [
        "Immobilier / Agence", "Fiduciaire / Comptable", "Cabinet d'avocats",
        "HORECA / Restaurant", "RH / Recrutement", "Construction / Architecture",
        "Formation professionnelle", "E-commerce", "Médical / Cabinet",
        "Assurance / Courtier", "Export / Commerce international"
    ]
    for i, s in enumerate(secteurs, 1):
        print(f"  [{i}] {s}")
    print("  [0] Saisir un secteur personnalisé")
    choix = input("\n  Secteur → ").strip()
    if choix == "0":
        secteur = input("  Secteur personnalisé → ").strip()[:100]
    elif choix.isdigit() and 1 <= int(choix) <= len(secteurs):
        secteur = secteurs[int(choix) - 1]
    else:
        secteur = choix[:100]
    if not secteur:
        return

    r = streamer(
        f"""ÉTUDE DE CAS SUR MESURE — Secteur : {secteur}

Crée une étude de cas ultra-détaillée et persuasive pour ce secteur spécifique.

FORMAT COMPLET :

🔴 LE PROBLÈME (150 mots minimum)
Contexte précis du secteur {secteur} en Belgique.
Prénom et prénom de famille belges typiques, ville belge spécifique (pas juste "Belgique").
Chiffre exact du problème (heures perdues par semaine, euros gaspillés par mois...).
Émotion : frustration, surcharge, sentiment de perdre du temps sur des tâches sans valeur.
"Avant Caelum, [Prénom] passait..."

⚙️ LA SOLUTION CAELUM (100 mots minimum)
Service exact (500€ / 1500€ / 3000€) + nom du service.
Durée de mise en place (7/14/30 jours selon le service).
Ce qui a été configuré précisément — quels outils, quels automatismes, quels agents.
Ton de livraison : "En 14 jours, Chaima a mis en place..."

📊 LES RÉSULTATS (liste de métriques, minimum 4)
Format : [Métrique] : [avant] → [après] (+X%)
Toujours inclure : temps gagné/semaine, économie annuelle estimée, ROI, une métrique qualitative.
ROI calculé : "Investissement de [X€] remboursé en [X semaines/mois]"

🎯 APPEL À L'ACTION (30 mots, percutant)
Une phrase qui crée l'urgence sans pression.
Email de contact : contact@caelumpartners.agency

VERSION LINKEDIN : version condensée (200 mots) adaptée pour un post LinkedIn.""",
        f"ÉTUDE DE CAS — {secteur}"
    )
    sauvegarder(f"etude_cas_{secteur.replace('/', '_').replace(' ', '_')[:30]}", r)


def vitrine_technique():
    """Génère une démonstration technique d'un agent IA en action."""
    print("\n  Quel type de démonstration technique créer ?")
    print("  [1] Démonstration agent email automation")
    print("  [2] Démonstration génération de contenu bilingue FR/NL")
    print("  [3] Démonstration analyse et rapport automatique")
    print("  [4] Démonstration chatbot client personnalisé")
    print("  [5] Démonstration facturation et relances automatiques")
    choix = input("\n  Choix → ").strip()
    demos = {
        "1": "agent d'automation email — réponses automatiques personnalisées pour une PME",
        "2": "génération de contenu bilingue FR/NL — annonces, communications, social media",
        "3": "analyse et rapport automatique — données brutes transformées en rapport PDF",
        "4": "chatbot client personnalisé — FAQ intelligente pour site web PME belge",
        "5": "facturation et relances automatiques — de la création à l'encaissement",
    }
    demo = demos.get(choix, choix[:100] if choix else "")
    if not demo:
        return

    r = streamer(
        f"""VITRINE TECHNIQUE — Démonstration : {demo}

Crée une démonstration technique détaillée et convaincante de cette capacité Caelum.

FORMAT :

🎬 SCÉNARIO (mise en situation réaliste)
"Imaginons : [entreprise type] à [ville belge] reçoit [X emails/semaine / produit X contenus...].
Voici exactement ce que fait l'agent Caelum en temps réel..."

🔧 DÉMONSTRATION ÉTAPE PAR ÉTAPE
Étape 1 : [action déclencheur]
→ L'agent reçoit / détecte / analyse [input précis]
Étape 2 : [traitement]
→ L'agent génère / classe / transforme [processus]
Étape 3 : [output]
→ Le résultat : [output concret, prêt à utiliser]
[Répéter pour 4-5 étapes réalistes]

📋 EXEMPLE D'OUTPUT RÉEL
Inclure un exemple littéral de ce que l'agent produirait :
(email généré / annonce rédigée / rapport structuré / réponse chatbot)
Format : bloc de texte entre guillemets, prêt à montrer à un prospect

💡 POURQUOI C'EST IMPOSSIBLE À FAIRE À LA MAIN EN CE TEMPS
"Ce que l'agent fait en 8 secondes prendrait [X minutes] à une personne.
Sur une semaine de [X occurrences], c'est [X heures] économisées."

🎯 APPEL À L'ACTION
"Vous voulez voir ça sur votre activité ? → contact@caelumpartners.agency"

Ton : démonstration, pas vente. Montrer, pas promettre.""",
        f"VITRINE TECHNIQUE — {demo[:50]}"
    )
    sauvegarder(f"vitrine_technique_{choix}", r)


def kit_site_web_complet():
    """Génère le contenu complet de preuve de travail pour le site web Caelum."""
    r = streamer(
        """KIT SITE WEB — Contenu Proof of Work complet pour caelumpartners.agency

Générer tout le contenu de preuve de travail pour remplir la section "Cas clients"
et "Résultats" du site web Caelum Partners.

LIVRER :

1. HEADLINE DE SECTION (3 variantes)
"Nos résultats parlent d'eux-mêmes" / alternatives percutantes pour la home page

2. CHIFFRES CLÉS (4 stats impactantes pour la home page)
Format : [Chiffre] — [Description courte]
Ex : "12h/semaine" — Temps moyen économisé par nos clients dès le 1er mois
(chiffres réalistes et conservateurs, pas exagérés)

3. TROIS ÉTUDES DE CAS RÉSUMÉES (pour la section cases studies)
Format compact pour le web : Problème (2 phrases) / Solution (1 phrase) / Résultat (3 bullet points)
Secteurs : immobilier + fiduciaire + HORECA (les 3 plus visuels)

4. SECTION "COMMENT ÇA MARCHE" (processus en 4 étapes)
Du premier contact à la livraison — en langage client (pas technique)

5. SECTION FAQ (5 questions avec réponses)
Les vraies objections des prospects belges + réponses Caelum directes

6. TÉMOIGNAGE FICTIF RÉALISTE (format quote)
Prénom belge, secteur, ville, résultat concret entre guillemets
[Note : à remplacer par vrai témoignage dès le premier client]

7. CTA FINAL DE LA PAGE (3 variantes)
La phrase qui convertit le visiteur en prospect contactant Chaima""",
        "KIT SITE WEB — Proof of Work Caelum Partners"
    )
    sauvegarder("kit_site_web_complet", r)


def contenu_linkedin_preuves():
    """Génère une série de posts LinkedIn basés sur des preuves de travail."""
    print("\n  Pour quel secteur générer les posts LinkedIn de preuve ?")
    secteur = input("  Secteur (ou 'général' pour plusieurs secteurs) → ").strip()[:100] or "général"

    r = streamer(
        f"""SÉRIE LINKEDIN — Posts Proof of Work pour Caelum Partners
Secteur cible : {secteur}

Générer 5 posts LinkedIn de preuve de travail, prêts à publier.

POUR CHAQUE POST :

📌 POST [N] — [FORMAT]
[Contenu complet du post, prêt à copier]
#hashtags pertinents (3-5 max, belges si possible)
---

FORMATS DES 5 POSTS :
1. FORMAT "AVANT / APRÈS" — Transformation d'une tâche répétitive (chiffres précis)
2. FORMAT "MINI ÉTUDE DE CAS" — Problème → Solution → Résultat en 5 phrases
3. FORMAT "FAIT CONCRET" — Une statistique surprenante sur le marché belge + lien avec Caelum
4. FORMAT "DÉMONSTRATION" — "Voici ce qu'un agent IA a généré en 10 secondes..." + exemple
5. FORMAT "QUESTION CLIENT" — La vraie objection d'un prospect + réponse honnête de Chaima

Ton LinkedIn belge B2B : direct, humble, factuel. Pas de "game changer" ou "disruptif".
Longueur optimale : 150-250 mots par post (format natif LinkedIn).""",
        f"SÉRIE LINKEDIN PROOF OF WORK — {secteur}"
    )
    sauvegarder(f"linkedin_preuves_{secteur.replace(' ', '_')[:30]}", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  ARCHITECTE DE PREUVE DE TRAVAIL — Proof of Work")
    print("  Études de cas · Vitrines · Désir d'achat · Site web")
    print("═"*65)

    while True:
        print("\n  1. Générer 3 études de cas complètes (3 secteurs)")
        print("  2. Étude de cas sur mesure (secteur au choix)")
        print("  3. Vitrine technique — démonstration agent IA en action")
        print("  4. Kit site web complet — section Cas Clients")
        print("  5. Série LinkedIn — 5 posts Proof of Work")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            generer_3_etudes_de_cas()
        elif choix == "2":
            etude_cas_sur_mesure()
        elif choix == "3":
            vitrine_technique()
        elif choix == "4":
            kit_site_web_complet()
        elif choix == "5":
            contenu_linkedin_preuves()
        else:
            print("  Choix invalide.")
