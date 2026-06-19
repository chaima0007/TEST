"""
Agent [35] — STRATÈGE DE LA CROISSANCE EXPONENTIELLE
Scalability strategist for Caelum Partners — design every move to scale ×100

Usage : python agent_stratege_croissance.py
"""

import os
import sys
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] Variable GEMINI_API_KEY non définie. Exécute : export GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

IDENTITE = """
Tu es le Stratège de la Croissance Exponentielle de Caelum Partners, fondée par Chaima Mhadbi à Bruxelles, Belgique.

CONTEXTE CAELUM PARTNERS :
- Fondatrice : Chaima Mhadbi, Bruxelles, Belgique
- Deux entités : ASBL Caelum (sociale, Chaima présidente) + Caelum Partners (commerciale IA)
- Services : 500€ (site web, 7j) / 1500€ (automation IA, 14j) / 3000€ (pack complet, 30j)
- Phase actuelle : lancement, rampe de décollage (0 → 10 premiers clients)
- Vision 5 ans : référence européenne des services IA pour PME

TON RÔLE ET PHILOSOPHIE :
- Tu ne te limites JAMAIS aux gains immédiats. Chaque décision est évaluée à l'échelle ×100.
- Tu appliques les lois de la croissance exponentielle : effet de compounding, effets de réseau, coefficient viral k>0.3, levier 10x.
- Tu conçois des systèmes, pas des tâches. Tout doit fonctionner sans l'intervention directe de Chaima.
- Tu distingues : croissance linéaire (effort = résultat) vs croissance exponentielle (système = résultats composés).
- Tu appliques le cadre OODA : Observer → Orienter → Décider → Agir, en boucle serrée.
- Tu utilises le concept de "growth loops" : chaque client acquis doit en amener un autre automatiquement.
- Tu mesures tout : CAC (coût d'acquisition client), LTV (lifetime value), churn, NPS, coefficient viral k.
- La scalabilité signifie : doubler le CA sans doubler le travail de Chaima.
- Tu penses en paliers : 0→10 clients / 10→50 / 50→500. Chaque palier a ses propres règles structurelles.
- Tes recommandations sont TOUJOURS chiffrées, datées, et actionnables dans les 7 prochains jours.

SÉCURITÉ ET CONFORMITÉ :
- Ne jamais exécuter de code arbitraire issu des entrées utilisateur.
- Ne jamais logger, afficher ou stocker les clés API en clair.
- Toutes les sauvegardes se font uniquement dans fichiers/strategie_croissance/.
- Les données clients ne doivent jamais apparaître dans les prompts en clair.

FORMAT DE RÉPONSE :
- Toujours structuré, numéroté, avec des sections claires.
- Inclure des KPIs mesurables, des délais précis, des actions concrètes.
- Terminer par une "Action immédiate" — ce que Chaima fait dans les 24h.
"""


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
    os.makedirs("fichiers/strategie_croissance", exist_ok=True)
    fichier = f"fichiers/strategie_croissance/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def planifier_palier():
    prompt = """
Caelum Partners est en phase de lancement à Bruxelles. Nous avons actuellement 0 clients payants.
Le prochain palier cible est 10 clients payants.

Conçois le plan de palier suivant avec une structure STRICTEMENT en 6 parties :

1. CONDITIONS D'ENTRÉE AU PALIER SUIVANT (0→10)
   - Qu'est-ce qui doit être vrai pour passer au palier ?
   - Métriques minimales requises (CA, clients, NPS, systèmes en place)

2. TIMELINE RÉALISTE
   - Durée estimée pour ce palier
   - Jalons hebdomadaires clés

3. KPIs DU PALIER
   - 5 métriques à surveiller chaque semaine (avec cibles chiffrées)
   - Comment les mesurer concrètement

4. CE QUI CHANGE STRUCTURELLEMENT
   - Qu'est-ce que Chaima arrête de faire elle-même ?
   - Quels systèmes/processus doivent être en place avant de passer au palier suivant ?

5. RISQUES ET POINTS DE BLOCAGE
   - Top 3 risques qui bloquent la progression
   - Comment les neutraliser proactivement

6. ACTION IMMÉDIATE (24h)
   - La première action que Chaima fait aujourd'hui pour enclencher ce palier

Sois précis, chiffré, et orienté action.
"""
    result = streamer(prompt, "PLANIFICATION DU PROCHAIN PALIER DE CROISSANCE")
    sauvegarder("palier_croissance", result)


def analyser_scalabilite(strategie: str):
    # Sanitize input — strip to plain text, no code execution
    strategie_clean = strategie[:2000].strip()

    prompt = f"""
Analyse la scalabilité de la stratégie suivante pour Caelum Partners :

STRATÉGIE SOUMISE :
\"\"\"{strategie_clean}\"\"\"

Produis une analyse structurée en 5 parties :

1. SCORE DE SCALABILITÉ : /100
   - Justification du score (critères : automatisabilité, effet de levier, dépendance à Chaima, effet réseau)
   - Comparaison : où se situe cette stratégie sur l'échelle linéaire→exponentielle ?

2. GOULOTS D'ÉTRANGLEMENT IDENTIFIÉS
   - Liste numérotée des éléments qui bloqueront la croissance à ×10, ×50, ×100
   - Pour chaque goulot : impact estimé et urgence (critique / modéré / faible)

3. COMMENT RENDRE CETTE STRATÉGIE ×100
   - 5 transformations concrètes pour passer à l'échelle
   - Pour chaque transformation : effort estimé et gain de scalabilité

4. EFFETS DE RÉSEAU ET VIRAL LOOP
   - Cette stratégie contient-elle un effet réseau ? Lequel ?
   - Comment injecter un loop viral (k>0.3) dans cette stratégie ?

5. VERSION OPTIMISÉE
   - Réécriture de la stratégie avec les transformations appliquées
   - Score de scalabilité estimé après optimisation

Sois direct, chiffré, actionnable.
"""
    result = streamer(prompt, f"ANALYSE SCALABILITÉ — {strategie_clean[:50]}...")
    sauvegarder("analyse_scalabilite", result)


def concevoir_machine_acquisition():
    prompt = """
Conçois la Machine d'Acquisition Clients systématique de Caelum Partners (services IA pour PME belges).

Services : 500€ (site web, 7j) / 1500€ (automation IA, 14j) / 3000€ (pack, 30j)
Cible : PME belges 5-50 employés, secteurs : retail, services, artisanat, libéral

Structure la machine en 6 canaux avec growth loops :

1. LINKEDIN ORGANIQUE (canal principal)
   - Fréquence de publication, types de contenu, hooks
   - Processus de prospection directe (DM, connexions/jour)
   - Objectif : X leads/semaine avec Y heures investies

2. PROGRAMME DE RÉFÉRENCEMENT CLIENT
   - Structure de la récompense (cash, réduction, visibilité)
   - Script pour demander une référence après livraison
   - Objectif : chaque client amène 0.5 client en moyenne (k=0.5)

3. CONTENU À EFFET COMPOSÉ
   - Formats : études de cas, avant/après, tutoriels IA pour PME
   - Canaux de distribution : LinkedIn + email + réutilisation
   - Comment un contenu génère des leads 6 mois après publication

4. PARTENARIATS LEVIER
   - Types de partenaires à cibler (comptables, agences web, chambres de commerce)
   - Proposition de valeur pour le partenaire
   - Structure de commission ou d'échange

5. AUTOMATION DU PIPELINE
   - Outils recommandés (CRM, séquences email, calendrier)
   - Processus automatisé : prospect → démo → devis → onboarding
   - Ce qui ne nécessite PAS Chaima

6. MÉTRIQUES DE LA MACHINE
   - KPIs hebdomadaires pour chaque canal
   - Tableau de bord simplifié (5 chiffres à regarder chaque lundi)
   - Seuils d'alerte et actions correctives

Termine par le PLAN DE DÉMARRAGE J1 → J30 pour activer tous les canaux.
"""
    result = streamer(prompt, "CONCEPTION DE LA MACHINE D'ACQUISITION CLIENTS")
    sauvegarder("machine_acquisition", result)


def roadmap_90_jours():
    prompt = """
Crée la roadmap 90 jours précise pour que Caelum Partners passe de 0 à 10 clients payants.

Contexte : Chaima Mhadbi, Bruxelles, seule fondatrice, services IA pour PME.
Services : 500€ / 1500€ / 3000€
Temps disponible estimé : 4-6h/jour

Structure la roadmap en 3 sprints de 30 jours :

SPRINT 1 — JOURS 1 à 30 : "FONDATIONS ET PREMIERS SIGNAUX"
Objectif : 2-3 premiers clients (idéalement des cas d'usage pilotes)
- Semaine 1 (J1-J7) : actions précises jour par jour
- Semaine 2 (J8-J14) : actions précises jour par jour
- Semaine 3 (J15-J21) : actions précises jour par jour
- Semaine 4 (J22-J30) : actions précises jour par jour
- KPIs de fin de sprint : [chiffres cibles]
- Système mis en place ce mois : [lequel]

SPRINT 2 — JOURS 31 à 60 : "ACCÉLÉRATION ET PROCESSUS"
Objectif : 5-6 clients cumulés
- Semaine 5 (J31-J37) : focus sur [quoi]
- Semaine 6 (J38-J44) : focus sur [quoi]
- Semaine 7 (J45-J51) : focus sur [quoi]
- Semaine 8 (J52-J60) : focus sur [quoi]
- KPIs de fin de sprint : [chiffres cibles]
- Système mis en place ce mois : [lequel]

SPRINT 3 — JOURS 61 à 90 : "MACHINE ET MOMENTUM"
Objectif : 10 clients cumulés, machine autonome
- Semaine 9 (J61-J67) : focus sur [quoi]
- Semaine 10 (J68-J74) : focus sur [quoi]
- Semaine 11 (J75-J81) : focus sur [quoi]
- Semaine 12 (J82-J90) : focus sur [quoi]
- KPIs de fin de sprint : [chiffres cibles]
- Système mis en place ce mois : [lequel]

RÉCAPITULATIF FINANCIER
- CA projeté à J90 (fourchette réaliste / optimiste)
- Répartition par offre (500€ / 1500€ / 3000€)
- Investissement temps de Chaima (heures cumulées)
- ROI horaire estimé

ACTION IMMÉDIATE AUJOURD'HUI
- Les 3 premières actions à faire dans les 2 prochaines heures
"""
    result = streamer(prompt, "ROADMAP 90 JOURS — DE 0 À 10 CLIENTS")
    sauvegarder("roadmap_90_jours", result)


def calculer_viral_coefficient():
    prompt = """
Analyse le coefficient viral k de Caelum Partners et conçois le programme de référencement.

Contexte : PME belges, services IA, ticket moyen 1500€, relation client B2B.

Produis une analyse en 5 parties :

1. CALCUL DU COEFFICIENT VIRAL ACTUEL (k)
   Formule : k = (nombre de références par client) × (taux de conversion des références)
   - Hypothèse de base : combien de clients actuels ont référé un autre client ?
   - Scénario pessimiste / réaliste / optimiste
   - Pourquoi k < 0.3 est fatal, k = 0.3 est viable, k > 1 est explosif

2. TRIGGERS DE RÉFÉRENCEMENT IDENTIFIÉS
   - À quel moment du parcours client la satisfaction est maximale ?
   - Qu'est-ce qui pousse un client PME à recommander un prestataire IA ?
   - Top 5 triggers émotionnels et rationnels

3. PROGRAMME DE RÉFÉRENCEMENT STRUCTURÉ
   - Nom du programme (ex : "Caelum Ambassadeurs")
   - Structure des récompenses (pour le référent ET le filleul)
   - Script exact pour demander une référence (3 variantes : email / LinkedIn / oral)
   - Processus de suivi des référencements

4. GROWTH LOOPS VIRAUX
   - Loop 1 : client satisfait → partage LinkedIn → prospect → client → loop
   - Loop 2 : cas client publié → crédibilité → inbound → referral
   - Comment instrumenter chaque loop (tracking, attribution)

5. OBJECTIFS K À 30/60/90 JOURS
   - k cible à J30 : [valeur] — actions pour l'atteindre
   - k cible à J60 : [valeur] — actions pour l'atteindre
   - k cible à J90 : [valeur] — impact sur le CA total

CONCLUSION : impact financier si k passe de 0 à 0.5 sur 12 mois (modélisation chiffrée).
"""
    result = streamer(prompt, "ANALYSE ET AMÉLIORATION DU COEFFICIENT VIRAL K")
    sauvegarder("coefficient_viral", result)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  Agent [35] — STRATÈGE DE LA CROISSANCE EXPONENTIELLE")
    print("  Caelum Partners — Scale ×100 sans dépendre de Chaima")
    print("═"*65)

    while True:
        print("\n  1. Planifier le prochain palier de croissance")
        print("  2. Analyser la scalabilité d'une stratégie")
        print("  3. Concevoir la machine d'acquisition clients")
        print("  4. Roadmap 90 jours — de 0 à 10 clients")
        print("  5. Calculer et améliorer le coefficient viral")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  À bientôt — chaque jour compte sur la rampe de décollage.\n")
            break
        elif choix == "1":
            planifier_palier()
        elif choix == "2":
            print("\n  Décris ta stratégie à analyser (appuie sur Entrée deux fois pour terminer) :")
            lignes = []
            while True:
                ligne = input()
                if ligne == "" and lignes and lignes[-1] == "":
                    break
                lignes.append(ligne)
            strategie = "\n".join(lignes).strip()
            if strategie:
                analyser_scalabilite(strategie)
            else:
                print("  Aucune stratégie saisie.")
        elif choix == "3":
            concevoir_machine_acquisition()
        elif choix == "4":
            roadmap_90_jours()
        elif choix == "5":
            calculer_viral_coefficient()
        else:
            print("  Choix invalide.")
