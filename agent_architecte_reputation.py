"""
ARCHITECTE DE RÉPUTATION — Gardien de l'image et de la confiance de Caelum Partners
Usage : python agent_architecte_reputation.py
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
IDENTITE = """Tu es l'Architecte de Réputation de Caelum Partners, fondée par Chaima Mhadbi à Bruxelles.
Ta devise absolue : "La valeur perçue est le premier actif de l'empire. Protège-la contre toute incohérence."
La réputation est un capital qui se compose : une bonne réputation attire de meilleurs clients à des prix plus élevés.
Elle est fragile : une seule incohérence peut éroder des mois de construction de confiance.
Elle est un fossé concurrentiel : impossible à copier rapidement par les concurrents.
Tu surveilles l'empreinte digitale complète : LinkedIn, site web, signatures email, qualité des propositions commerciales.
Tu garantis la cohérence éthique : ce que Caelum promet doit correspondre exactement à ce qui est livré.
Tu assures la cohérence de communication : ton, valeurs et positionnement identiques sur tous les canaux.
Tu construis la preuve sociale de manière systématique : études de cas, témoignages, programme de références.
Tu gères les crises de réputation avec protocoles clairs, rapidité et transparence contrôlée.
Les signaux de confiance B2B belge que tu priorises : présence dans l'écosystème Hub.Brussels, BECI, StartupBelgium.
Le temps de réponse aux clients est un signal de réputation : moins de 4h = professionnel, plus = risque de perception.
La qualité des factures et devis (mentions légales complètes, conformité TVA) est un signal de confiance fort.
La conformité RGPD clairement affichée est non négociable pour le marché belge et européen.
Caelum Partners propose : site web 500€ (7j), automation IA 1500€ (14j), pack complet 3000€ (30j).
La phase actuelle est le lancement : 0 clients, chaque premier contact est fondateur de la réputation à long terme.
Tu analyses les canaux de communication avec un score /100 et un plan d'action prioritaire et chiffré.
Tu détectes les incohérences de ton, de valeurs et de positionnement entre les différents canaux.
Tes recommandations sont toujours spécifiques, actionnables, adaptées au marché belge francophone et néerlandophone.
Tu parles en français, tu es rigoureux, stratégique et tu protèges l'empire comme s'il était déjà au sommet."""

def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.15, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse

def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/reputation", exist_ok=True)
    fichier = f"fichiers/reputation/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def audit_empreinte_digitale():
    prompt = """Effectue un audit complet de l'empreinte digitale de Caelum Partners pour Chaima Mhadbi, fondatrice basée à Bruxelles.

Analyse les canaux suivants avec un score /100 chacun et un plan d'action détaillé :

1. PROFIL LINKEDIN DE LA FONDATRICE
   - Évalue : photo professionnelle, titre accrocheur, résumé About, expériences listées, publications régulières, taux d'engagement
   - Score /100 + 5 actions prioritaires numérotées pour atteindre 90+/100
   - Benchmark : à quoi ressemble un profil LinkedIn B2B de référence dans l'IA en Belgique ?

2. SITE WEB CAELUM PARTNERS
   - Évalue : clarté du message en above-the-fold, proposition de valeur visible en 5 secondes, appel à l'action, preuve sociale, conformité RGPD, version FR/NL, vitesse de chargement
   - Score /100 + 5 actions prioritaires numérotées
   - Éléments critiques manquants les plus courants pour les agences IA belges

3. SIGNATURE EMAIL PROFESSIONNELLE
   - Évalue : nom complet, titre, coordonnées, lien LinkedIn, lien site web, mention légale RGPD, cohérence visuelle
   - Score /100 + modèle de signature optimale à copier-coller
   - Template de signature professionnel en français et néerlandais

4. QUALITÉ DES PROPOSITIONS COMMERCIALES
   - Évalue : structure, mentions légales belges obligatoires, clarté des livrables, conditions de paiement, politique de révision, charte graphique
   - Score /100 + checklist des 10 éléments non négociables d'une proposition commerciale belge

5. SCORE GLOBAL DE RÉPUTATION DIGITALE /100
   - Synthèse : points forts à capitaliser, risques réputationnels immédiats, plan d'action 30 jours
   - Priorisation : les 3 actions qui auront le plus grand impact sur la perception professionnelle en Belgique

Format : structuré, numéroté, avec scores clairs et actions concrètes. Langue : français."""

    resultat = streamer(prompt, "AUDIT — Empreinte digitale Caelum Partners")
    sauvegarder("audit_empreinte", resultat)

def detecter_incoherences_communication():
    print("\n  Collez vos exemples de communication (LinkedIn, email, proposition) — tapez FIN sur une ligne seule pour terminer :")
    lignes = []
    while True:
        ligne = input()
        if ligne.strip().upper() == "FIN":
            break
        lignes.append(ligne)
    exemples = "\n".join(lignes)
    # Sanitize: truncate to reasonable length, no API key patterns
    exemples = exemples[:4000]

    prompt = f"""Analyse les échantillons de communication ci-dessous de Caelum Partners et détecte toutes les incohérences qui pourraient nuire à la réputation et à la confiance des clients potentiels.

ÉCHANTILLONS DE COMMUNICATION :
{exemples}

Effectue une analyse structurée en 5 parties :

1. ANALYSE DU TON ET REGISTRE
   - Identifie les variations de registre (formel/informel, tutoiement/vouvoiement, technique/vulgarisé)
   - Quelles variations sont acceptables vs. lesquelles créent de la confusion ?
   - Recommandation : quel ton unique adopter pour Caelum Partners ?

2. COHÉRENCE DES VALEURS EXPRIMÉES
   - Liste les valeurs explicitement ou implicitement exprimées dans chaque canal
   - Détecte les contradictions entre valeurs affichées et formulations utilisées
   - Exemple : dire "nous sommes accessibles" mais utiliser un jargon impénétrable

3. COHÉRENCE DU POSITIONNEMENT
   - Le positionnement (qui on est, pour qui, pourquoi nous ?) est-il identique sur tous les canaux ?
   - Identifier les messages contradictoires sur la cible client, le bénéfice principal, la différenciation
   - Impact potentiel de ces incohérences sur la décision d'achat

4. SIGNAUX DE CONFIANCE MANQUANTS
   - Quels éléments de réassurance B2B belge sont absents ? (certifications, références, conformité RGPD, localisation Bruxelles)
   - Quelles formulations créent de la méfiance plutôt que de la confiance ?

5. PLAN DE CORRECTION PRIORISÉ
   - 10 corrections numérotées par ordre d'impact sur la réputation
   - Pour chaque correction : avant/après avec exemple reformulé
   - Délai de mise en œuvre recommandé (immédiat / cette semaine / ce mois)

Format : précis, avec citations directes des exemples fournis. Langue : français."""

    resultat = streamer(prompt, "DÉTECTION — Incohérences de communication")
    sauvegarder("incoherences_communication", resultat)

def construire_preuve_sociale():
    prompt = """Conçois une stratégie systématique de construction de preuve sociale pour Caelum Partners, agence IA bruxelloise en phase de lancement (0 clients actuellement).

Livre un plan complet en 5 sections :

1. STRATÉGIE DE COLLECTE DE TÉMOIGNAGES
   - À quel moment précis du parcours client demander le témoignage (pas avant, pas après — le moment optimal)
   - Script exact en français et néerlandais pour demander un témoignage sans gêne
   - Format des témoignages : vidéo / texte / LinkedIn recommendation — lequel prioriser et pourquoi
   - Système de relance automatique si pas de réponse (J+3, J+7, J+14)
   - Template de page de remerciement après témoignage reçu

2. TEMPLATE D'ÉTUDE DE CAS (CASE STUDY)
   - Structure complète : Contexte client → Problème → Solution Caelum → Livrables → Résultats mesurables → Citation client
   - Questions à poser au client pour rédiger l'étude de cas sans le solliciter trop
   - Format court (LinkedIn, 300 mots) ET format long (site web, 1000 mots)
   - Comment anonymiser si le client ne veut pas être nommé

3. PROGRAMME DE RÉFÉRENCES (REFERRAL)
   - Structure du programme : incitation financière ou non financière ? Quel montant/avantage pour le marché belge B2B ?
   - Conditions claires : qui peut référer, quel type de contact, quelle récompense, quand versée
   - Script de demande de référence à un client satisfait
   - Suivi et traçabilité des références dans le CRM

4. PRÉSENCE DANS L'ÉCOSYSTÈME BELGE
   - Plan de visibilité : Hub.Brussels (comment s'inscrire et participer), BECI (événements pertinents), StartupBelgium (profil à créer)
   - 5 événements networking IA/tech à Bruxelles à cibler en 2025
   - Stratégie de partenariats de crédibilité : qui contacter en priorité (comptables, avocats, consultants RH) pour des recommandations croisées

5. CALENDRIER DE DÉPLOIEMENT — 90 JOURS
   - Semaine 1-4 : actions immédiates (profils, templates, demandes aux premiers contacts)
   - Semaine 5-8 : premières preuves sociales en ligne
   - Semaine 9-12 : programme de références opérationnel, premières études de cas publiées
   - KPIs à suivre : nombre de témoignages, références reçues, mentions dans l'écosystème

Format : plans d'action numérotés, templates prêts à l'emploi. Langue : français."""

    resultat = streamer(prompt, "STRATÉGIE — Construction de la preuve sociale")
    sauvegarder("preuve_sociale", resultat)

def gerer_crise_reputation():
    situation = input("\n  Décrivez la situation de crise réputationnelle (avis négatif, litige, malentendu, etc.) :\n  → ").strip()
    # Sanitize input
    situation = situation[:2000]
    if not situation:
        print("  Aucune situation fournie.")
        return

    prompt = f"""Caelum Partners (agence IA, Bruxelles, fondatrice Chaima Mhadbi) fait face à la crise réputationnelle suivante :

SITUATION : {situation}

Fournis un protocole complet de gestion de crise en 6 étapes :

1. ÉVALUATION DE LA GRAVITÉ (dans les 15 premières minutes)
   - Niveau de criticité : Rouge (menace existentielle) / Orange (risque significatif) / Jaune (incident gérable)
   - Vitesse de propagation potentielle : qui peut voir/entendre cette situation ?
   - Impact estimé sur le pipeline commercial et la réputation à 30/90/180 jours
   - Cette situation est-elle visible publiquement ou contenue en privé ?

2. RÉPONSE IMMÉDIATE (dans l'heure)
   - Ce qu'il faut faire MAINTENANT vs ce qu'il ne faut SURTOUT PAS faire
   - Si réponse publique nécessaire : script exact de la réponse initiale (court, professionnel, non défensif)
   - Si contact direct nécessaire : script de l'appel ou email à la partie concernée
   - Qui prévenir en interne (même en solo, quels partenaires ou mentors alerter)

3. INVESTIGATION HONNÊTE (dans les 24h)
   - Analyse sans émotion : quelle est la part de responsabilité de Caelum dans cette situation ?
   - Quels faits sont vérifiables vs perceptions subjectives ?
   - Leçon structurelle : s'agit-il d'un problème de processus, de communication ou de livrable ?

4. PLAN DE RÉSOLUTION (dans les 72h)
   - Solution proposée à la partie lésée : compensation, correction, explication, excuse ?
   - Formulation exacte de l'offre de résolution
   - Délai de résolution réaliste et comment le communiquer
   - Documentation interne de l'incident pour éviter la récurrence

5. RECONSTRUCTION DE LA CONFIANCE (dans les 30 jours)
   - Actions concrètes pour reconquérir la confiance de la partie concernée
   - Comment transformer cet incident en démonstration de professionnalisme
   - Message de suivi J+7 et J+30 après résolution

6. PRÉVENTION SYSTÉMIQUE
   - Quel processus ou standard manquait qui a permis cette situation ?
   - Protocole à mettre en place immédiatement pour éviter la récurrence
   - Indicateur d'alerte précoce à surveiller à l'avenir

Format : urgent, actionnable, scripts prêts à l'emploi. Langue : français."""

    resultat = streamer(prompt, f"CRISE — Protocole de gestion réputationnelle")
    sauvegarder("crise_reputation", resultat)

def generer_kit_credibilite():
    prompt = """Génère le kit de crédibilité complet de Chaima Mhadbi / Caelum Partners, agence IA bruxelloise spécialisée dans l'automatisation pour les PME belges.

Services : site web 500€ (7j), automation IA 1500€ (14j), pack complet 3000€ (30j).
Vision : référence européenne pour les services IA aux PME en 5 ans.

Livre un kit en 5 composantes :

1. BIO VERSIONS (3 formats)

   A) BIO COURTE — 50 mots
   Pour : signature email, profil annuaire, carte de visite numérique
   Ton : professionnel, mémorable, différenciant
   Inclure : nom, titre, spécialité unique, localisation, impact chiffrable

   B) BIO MOYENNE — 150 mots
   Pour : présentation événement networking, profil LinkedIn résumé, présentation partenaires
   Ton : storytelling bref, crédibilité, aspiration
   Inclure : parcours condensé, pourquoi Caelum, résultats clients, vision

   C) BIO LONGUE — 300 mots
   Pour : page À propos du site web, dossier de presse, candidatures partenariats
   Ton : inspirant, détaillé, humain mais professionnel
   Inclure : genèse de Caelum, expertise technique, valeurs, mission, vision 5 ans

2. PROPOSITIONS DE VALEUR (5 variations)
   - Version technique (pour DSI, CTO, profils tech)
   - Version ROI (pour dirigeants, CFO — focus économies/revenus)
   - Version temps gagné (pour fondateurs débordés)
   - Version risque réduit (pour profils prudents/juridiques)
   - Version vision (pour innovateurs early adopters)
   Pour chaque version : 1 phrase d'accroche + 3 bénéfices + 1 call-to-action

3. CHECKLIST DES SIGNAUX DE CONFIANCE POUR PROPOSITIONS COMMERCIALES
   15 éléments numérotés à vérifier avant d'envoyer toute proposition :
   - Mentions légales belges obligatoires (numéro TVA, siège social, forme juridique)
   - Éléments RGPD (politique de traitement des données, durée de conservation)
   - Signaux de qualité (portfolio, références, garanties)
   - Éléments contractuels de protection (conditions de révision, propriété intellectuelle)
   - Présentation visuelle (charte graphique, lisibilité, professionnalisme)

4. RÉPERTOIRE DES PREUVES SOCIALES À CONSTRUIRE
   - 10 types de preuves sociales classées par impact et facilité d'obtention
   - Plan de collecte pour chaque type : qui contacter, comment, quand
   - Format d'affichage recommandé (site web, LinkedIn, proposition commerciale)

5. PHRASE DE POSITIONNEMENT SIGNATURE
   - 3 versions d'une phrase d'accroche mémorable pour Caelum Partners
   - Testable en 5 secondes : est-ce que le prospect comprend immédiatement qui nous servons et quel résultat on délivre ?
   - Analyse de chaque version : forces, risques, public cible optimal

Format : prêt à copier-coller, professionnel, adapté au marché belge B2B. Langue : français."""

    resultat = streamer(prompt, "KIT — Crédibilité complète Caelum Partners")
    sauvegarder("kit_credibilite", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  ARCHITECTE DE RÉPUTATION — Gardien de l'image Caelum Partners")
    print("═"*65)
    while True:
        print("\n  [menu]")
        print("  1. Audit empreinte digitale")
        print("  2. Détecter incohérences communication")
        print("  3. Construire la preuve sociale")
        print("  4. Gérer une crise de réputation")
        print("  5. Générer le kit de crédibilité")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            audit_empreinte_digitale()
        elif choix == "2":
            detecter_incoherences_communication()
        elif choix == "3":
            construire_preuve_sociale()
        elif choix == "4":
            gerer_crise_reputation()
        elif choix == "5":
            generer_kit_credibilite()
        else:
            print("  Choix invalide.")
