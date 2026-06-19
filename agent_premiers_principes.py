"""
STRATÈGE DES PREMIERS PRINCIPES — Décomposer chaque problème à ses vérités fondamentales
Méthode Elon Musk · Aristote · Socrate · Reconstruire sans analogie

Usage : python agent_premiers_principes.py
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

IDENTITE = """# STRATÈGE DES PREMIERS PRINCIPES — CAELUM PARTNERS

## IDENTITÉ ET RÔLE
Tu es le Stratège des Premiers Principes de Caelum Partners.
Ta mission : décomposer CHAQUE problème jusqu'à ses vérités atomiques fondamentales,
éliminer toutes les hypothèses et la sagesse conventionnelle, puis reconstruire
des solutions UNIQUEMENT depuis ces vérités. Jamais par analogie.

## LA MÉTHODE DES PREMIERS PRINCIPES

### ARISTOTE (384-322 av. J.-C.) — LES CAUSES PREMIÈRES
Aristote distinguait deux types de connaissance :
- La connaissance par analogie : "ça ressemble à X, donc ça devrait fonctionner comme X"
- La connaissance par premiers principes : "qu'est-ce qui est fondamentalement vrai ici ?"
La connaissance analogique est rapide mais conduit à des solutions médiocres.
La connaissance par premiers principes est lente mais conduit à des percées.

### ELON MUSK — APPLICATION MODERNE
"Je pense en premiers principes plutôt que par analogie. Avec SpaceX, j'aurais pu dire
'les fusées coûtent X milliards, donc c'est impossible.' Au lieu, j'ai demandé :
de quoi est faite une fusée ? Aluminium, titane, cuivre, carbone. Quel est le coût
de ces matériaux sur le marché ? 2% du prix d'une fusée achetée toute faite."

### PROCESSUS DE DÉCOMPOSITION EN 5 ÉTAPES
1. IDENTIFIER : quel est le problème exact (formulé sans solution implicite) ?
2. DÉCOMPOSER : quels sont les composants fondamentaux de ce problème ?
3. QUESTIONNER : quelles hypothèses sont cachées dans la formulation du problème ?
4. VÉRIFIER : quelles vérités fondamentales restent après élimination des hypothèses ?
5. RECONSTRUIRE : construire la solution uniquement depuis ces vérités atomiques

## FAUSSES HYPOTHÈSES COMMUNES EN CONSULTING IA (à éliminer)
- "Il faut une grande équipe" → FAUX : l'IA remplace l'équipe
- "Il faut du capital VC" → FAUX : services professionnels = cash positif dès le premier client
- "Il faut un bureau" → FAUX : les clients paient pour les résultats, pas le bureau
- "Il faut des certifications pour être crédible" → FAUX : les résultats sont la preuve
- "Il faut d'abord construire le produit parfait" → FAUX : vendre d'abord, construire ensuite
- "Les prix doivent s'aligner sur le marché" → FAUX : la valeur détermine le prix, pas le marché

## MÉTHODE SOCRATIQUE — QUESTIONNER JUSQU'À LA VÉRITÉ
Pour chaque conviction : poser "pourquoi ?" 5 fois de suite jusqu'à atteindre la vérité atomique.
Exemple :
- "Je dois faire du SEO" → Pourquoi ? → "Pour avoir des visiteurs" → Pourquoi ? → "Pour trouver des clients"
→ Pourquoi ? → "Pour avoir du CA" → PREMIER PRINCIPE : "Je dois trouver du CA.
  Le SEO est une option parmi 100 autres — probablement pas la plus rapide."

## FORMAT DE SORTIE OBLIGATOIRE
1. HYPOTHÈSES IDENTIFIÉES : liste de toutes les hypothèses cachées
2. VÉRITÉS ATOMIQUES : ce qui reste après élimination des hypothèses
3. SOLUTION RECONSTRUITE : bâtie uniquement depuis les vérités atomiques
4. COMPARAISON : solution par analogie vs solution par premiers principes
5. ACTION IMMÉDIATE : quelle est la première action découlant des premiers principes ?"""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.2, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/premiers_principes", exist_ok=True)
    fichier = f"fichiers/premiers_principes/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def decomposer_probleme():
    probleme = input("\n  Décris le problème à décomposer → ").strip()
    if not probleme:
        return
    r = streamer(
        f"""Décompose ce problème jusqu'à ses vérités atomiques fondamentales.
Problème : {probleme}

ÉTAPE 1 — REFORMULATION NEUTRE :
Reformuler le problème sans aucune solution implicite (éliminer le biais de cadrage).

ÉTAPE 2 — DÉCOMPOSITION EN COMPOSANTS :
Quels sont les éléments constitutifs fondamentaux de ce problème ?
(Utiliser la méthode des arbres de décomposition — du général au particulier)

ÉTAPE 3 — IDENTIFICATION DES HYPOTHÈSES CACHÉES :
Quelles hypothèses sont implicitement intégrées dans la formulation ?
Pour chaque hypothèse : est-elle une vérité fondamentale ou une convention sociale ?

ÉTAPE 4 — LES VÉRITÉS ATOMIQUES :
Après élimination de toutes les hypothèses, que reste-t-il ?
Ce sont les premiers principes de ce problème.

ÉTAPE 5 — RECONSTRUCTION DE LA SOLUTION :
En partant UNIQUEMENT des vérités atomiques identifiées (sans analogie, sans "c'est comme..."),
quelle est la solution optimale ?

ÉTAPE 6 — COMPARAISON AVEC LA SOLUTION CONVENTIONNELLE :
Solution par analogie (ce que tout le monde ferait) : ...
Solution par premiers principes : ...
Différence et avantage de l'approche premiers principes.""",
        f"DÉCOMPOSITION PREMIERS PRINCIPES — {probleme[:40]}"
    )
    sauvegarder(f"decomposition_{probleme[:25].replace(' ', '_')}", r)


def identifier_assumptions():
    r = streamer(
        """Identifie TOUTES les hypothèses cachées dans la stratégie actuelle de Caelum Partners.

AUDIT DES HYPOTHÈSES STRATÉGIQUES :

HYPOTHÈSES SUR LE MARCHÉ :
- "Les PME belges ont besoin d'IA" → est-ce une vérité ou une hypothèse ?
- "Le prix 500-3000€ est accessible aux PME" → vérité ou hypothèse ?
- "Bruxelles est le bon marché de départ" → vérité ou hypothèse ?

HYPOTHÈSES SUR LE MODÈLE DE SERVICE :
- "Il faut livrer en moins de 30 jours" → vérité ou hypothèse ?
- "Le client doit être impliqué dans la livraison" → vérité ou hypothèse ?
- "La qualité justifie ce prix" → vérité ou hypothèse ?

HYPOTHÈSES SUR LA CONCURRENCE :
- "Les agences traditionnelles sont mes concurrents directs" → vérité ou hypothèse ?
- "Les clients comparent les prix entre consultants IA" → vérité ou hypothèse ?
- "Un concurrent peut copier l'écosystème de 50 agents" → vérité ou hypothèse ?

HYPOTHÈSES SUR CHAIMA :
- "Une solopreneuse peut gérer 5+ clients simultanément" → vérité ou hypothèse ?
- "L'expertise IA est suffisante pour convaincre des dirigeants PME" → vérité ou hypothèse ?
- "Le statut ASBL + commercial est un avantage" → vérité ou hypothèse ?

POUR CHAQUE HYPOTHÈSE :
- Statut : VÉRITÉ FONDAMENTALE / CONVENTION SOCIALE / HYPOTHÈSE NON TESTÉE
- Comment la tester empiriquement (en < 48h) ?
- Si elle est fausse : quelle stratégie alternative émerge des premiers principes ?

CONCLUSION : les 3 hypothèses les plus dangereuses à tester immédiatement.""",
        "AUDIT DES HYPOTHÈSES — Stratégie Caelum Partners"
    )
    sauvegarder("audit_hypotheses", r)


def reconstruire_solution():
    r = streamer(
        """Reconstruis la stratégie de Caelum Partners depuis les premiers principes uniquement.
INTERDICTION ABSOLUE d'utiliser des analogies ("c'est comme une agence web", "les consultants font...")

VÉRITÉS ATOMIQUES DE CAELUM PARTNERS (point de départ) :
1. Il y a des PME belges qui ont des problèmes de productivité et d'efficacité
2. L'IA peut résoudre ces problèmes automatiquement
3. Chaima sait construire et orchestrer des agents IA
4. Les clients paient pour les RÉSULTATS (économies réalisées, temps gagné, revenus générés)
5. Chaque heure de travail automatisée a une valeur économique mesurable
6. La confiance se construit par la preuve (résultats démontrables)
7. Le bouche-à-oreille est le canal d'acquisition le plus efficient

RECONSTRUCTION DE LA STRATÉGIE DEPUIS CES 7 VÉRITÉS :

1. QUE VENDRE ? (déduit des vérités 1, 2, 4)
2. À QUI VENDRE ? (déduit des vérités 1, 5)
3. À QUEL PRIX ? (déduit des vérités 4, 5 — prix = fraction de la valeur créée)
4. COMMENT ACQUÉRIR DES CLIENTS ? (déduit des vérités 6, 7)
5. COMMENT LIVRER ? (déduit des vérités 2, 3)
6. COMMENT CROÎTRE ? (déduit de toutes les vérités combinées)

COMPARER :
La stratégie actuelle de Caelum vs la stratégie reconstruite par premiers principes.
Quelles différences ? Quels ajustements immédiats ?""",
        "RECONSTRUCTION PAR PREMIERS PRINCIPES — Stratégie Caelum"
    )
    sauvegarder("reconstruction_solution", r)


def challenger_conviction():
    conviction = input("\n  Énonce une conviction ou croyance à challenger → ").strip()
    if not conviction:
        return
    r = streamer(
        f"""Challenge cette conviction à l'aide de la méthode des premiers principes.
Conviction : {conviction}

MÉTHODE SOCRATIQUE — 5 POURQUOI SUCCESSIFS :
Pourquoi 1 : Pourquoi crois-tu cela ?
Pourquoi 2 : Pourquoi est-ce que cette raison est valide ?
Pourquoi 3 : Pourquoi est-ce fondamentalement vrai ?
Pourquoi 4 : Pourquoi pas l'inverse ?
Pourquoi 5 : Quelle est la vérité atomique que tu ne peux pas remettre en question ?

ANALYSE DE LA CONVICTION :
1. Origine de cette conviction : expérience personnelle, convention sociale, ou donnée empirique ?
2. Cas où cette conviction est vraie (conditions de validité)
3. Cas où cette conviction est fausse (contre-exemples)
4. Biais cognitifs potentiels dans cette conviction (confirmation bias, disponibilité, ancrage)

ALTERNATIVE PAR PREMIERS PRINCIPES :
Si on part de zéro, sans cette conviction pré-établie, que dit la logique pure ?

VERDICT :
- Cette conviction est : VÉRITÉ FONDAMENTALE / MYTHE UTILE / FAUSSE CROYANCE DANGEREUSE
- Action recommandée : conserver / modifier / abandonner
- Impact sur la stratégie Caelum si on abandonne cette conviction""",
        f"CHALLENGE CONVICTION — {conviction[:45]}"
    )
    sauvegarder(f"challenge_{conviction[:25].replace(' ', '_')}", r)


def analyser_paradigme_concurrent():
    r = streamer(
        """Identifie les hypothèses que font les concurrents de Caelum Partners — et comment les violer.

CARTOGRAPHIE DES PARADIGMES CONCURRENTS :

AGENCES WEB TRADITIONNELLES (Bruxelles) — leurs hypothèses :
1. "Il faut une équipe de 5+ personnes pour livrer un site web professionnel"
   → Comment Caelum viole cette hypothèse : 1 personne + IA = même résultat
2. "Un site web prend 6-12 semaines"
   → Comment Caelum viole cette hypothèse : 7 jours
3. "Le prix doit refléter le nombre d'heures travaillées"
   → Comment Caelum viole cette hypothèse : prix basé sur la valeur créée

CONSULTANTS IA INDÉPENDANTS — leurs hypothèses :
1. "Il faut être généraliste pour avoir assez de clients"
   → Comment Caelum peut violer cette hypothèse
2. "Les petits budgets ne valent pas le déplacement"
   → Comment Caelum peut violer cette hypothèse
3. "La crédibilité vient de l'expérience passée (années de consulting)"
   → Comment Caelum viole cette hypothèse (résultats démontrables dès J1)

GRANDS CABINETS CONSEIL — leurs hypothèses :
1. "Les PME ne peuvent pas se payer un cabinet de conseil"
   → Comment Caelum se positionne entre eux et rien
2. "L'IA est trop complexe pour des non-techniciens"
   → Comment Caelum viole cette hypothèse

VIOLATIONS DE PARADIGME À EXPLOITER IMMÉDIATEMENT :
- Liste des 5 hypothèses des concurrents que Caelum peut violer cette semaine
- Script de vente basé sur ces violations de paradigme
- Slogan ou accroche commerciale qui cristallise ces violations""",
        "ANALYSE PARADIGMES CONCURRENTS — Violations stratégiques Caelum"
    )
    sauvegarder("paradigmes_concurrents", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  STRATÈGE DES PREMIERS PRINCIPES — Caelum Partners")
    print("  Aristote · Elon Musk · Socrate · Reconstruire depuis zéro")
    print("═"*65)

    while True:
        print("\n  1. Décomposer un problème en vérités atomiques")
        print("  2. Identifier toutes les hypothèses cachées")
        print("  3. Reconstruire la stratégie depuis zéro")
        print("  4. Challenger une conviction par premiers principes")
        print("  5. Analyser les paradigmes des concurrents à violer")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            decomposer_probleme()
        elif choix == "2":
            identifier_assumptions()
        elif choix == "3":
            reconstruire_solution()
        elif choix == "4":
            challenger_conviction()
        elif choix == "5":
            analyser_paradigme_concurrent()
        else:
            print("  Choix invalide.")
