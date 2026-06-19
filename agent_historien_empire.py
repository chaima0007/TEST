"""
HISTORIEN DE L'EMPIRE — Gardien de la mémoire institutionnelle de Caelum Partners
Usage : python agent_historien_empire.py
"""
import os
import sys
import json
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"
IDENTITE = """Tu es l'Historien de l'Empire de Caelum Partners, fondée par Chaima Mhadbi à Bruxelles.
Ta conviction absolue : "Ne laisse aucune expérience se perdre. Transforme les erreurs passées en protocoles de réussite future."
Chaque décision prise, chaque client gagné ou perdu, chaque agent déployé, chaque stratégie testée — tout est de la donnée précieuse.
Ton travail : capturer la LOGIQUE derrière chaque décision (pas seulement ce qui a été décidé, mais POURQUOI).
Tu extrais les leçons transférables de chaque expérience pour bâtir la connaissance institutionnelle de l'empire.
Tu préviens que les mêmes erreurs soient commises deux fois — c'est le coût invisible de l'absence de mémoire organisationnelle.
Format de la connaissance que tu construis : Journaux de décision (quoi + pourquoi + résultat), Autopsies d'échecs (ce qui a mal tourné + cause racine + protocole de prévention), Patterns de succès (ce qui a fonctionné + pourquoi + comment le reproduire), Évolution stratégique (comment la stratégie a changé dans le temps + le déclencheur de chaque changement).
Tu utilises la méthode des 5 Pourquoi pour identifier les causes racines dans les autopsies d'échecs.
Tu lis les fichiers JSON existants (memoire_entreprise.json, historique_caelum.json, crm_pipeline.json) pour alimenter tes analyses.
Tu structures les entrées de journal en format standardisé : Contexte → Action → Résultat → Leçon → Protocole de prévention.
Tu identifies les patterns récurrents dans les succès : quelles conditions mènent systématiquement à des victoires ?
Tu construis la base de connaissance cumulée de Caelum — le document qui survivrait à la fondatrice si elle devait un jour transmettre.
Tu es le garant de la mémoire à long terme : dans 5 ans, quand Caelum sera une référence européenne, c'est cette base qui expliquera comment on y est arrivé.
Tu parles en français, tu es méthodique, analytique, et tu transformes l'expérience brute en sagesse structurée et actionnable.
Caelum Partners : services 500€/1500€/3000€, phase de lancement, 0 clients initialement, bootstrappée à Bruxelles."""

def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.1, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse

def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/historien_empire", exist_ok=True)
    fichier = f"fichiers/historien_empire/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def _lire_json_existants() -> str:
    """Lit les fichiers JSON de mémoire existants si présents."""
    fichiers_cibles = [
        "memoire_entreprise.json",
        "historique_caelum.json",
        "crm_pipeline.json"
    ]
    donnees_lues = {}
    for nom in fichiers_cibles:
        chemin = os.path.join("fichiers", nom)
        if os.path.exists(chemin):
            try:
                with open(chemin, "r", encoding="utf-8") as f:
                    donnees_lues[nom] = json.load(f)
            except (json.JSONDecodeError, OSError):
                donnees_lues[nom] = f"[Fichier présent mais illisible : {nom}]"
    if donnees_lues:
        return json.dumps(donnees_lues, ensure_ascii=False, indent=2)[:3000]
    return "[Aucun fichier JSON de mémoire trouvé — analyse basée sur les informations fournies]"

def enregistrer_experience():
    print("\n  Type d'expérience : (1) Succès  (2) Échec  (3) Décision stratégique")
    type_choix = input("  → ").strip()
    types_map = {"1": "SUCCÈS", "2": "ÉCHEC", "3": "DÉCISION STRATÉGIQUE"}
    type_experience = types_map.get(type_choix, "EXPÉRIENCE")

    print(f"\n  Décrivez l'expérience ({type_experience}) — tapez FIN sur une ligne seule pour terminer :")
    lignes = []
    while True:
        ligne = input()
        if ligne.strip().upper() == "FIN":
            break
        lignes.append(ligne)
    experience = "\n".join(lignes)[:3000]
    if not experience.strip():
        print("  Aucune expérience fournie.")
        return

    prompt = f"""Structure l'expérience suivante de Caelum Partners en une entrée de journal institutionnel complète et actionnable.

TYPE D'EXPÉRIENCE : {type_experience}
DATE D'ENREGISTREMENT : {datetime.now().strftime('%Y-%m-%d')}

DESCRIPTION BRUTE :
{experience}

Produis une entrée de journal structurée en 7 sections :

1. CONTEXTE COMPLET
   - Situation de départ : quel était l'état de Caelum avant cet événement ?
   - Acteurs impliqués : qui était présent/concerné (client, partenaire, concurrence, facteur externe) ?
   - Environnement : quelles contraintes (temps, budget, ressources) pesaient sur la situation ?
   - Objectif initial : qu'est-ce qu'on cherchait à accomplir ?

2. ACTION(S) PRISE(S)
   - Décision(s) clé(s) : qu'est-ce qui a été décidé, et par qui/comment ?
   - Alternatives non retenues : quelles autres options existaient ? Pourquoi ont-elles été écartées ?
   - Ressources mobilisées : quels outils, agents IA, compétences ont été utilisés ?
   - Timing : séquence chronologique des actions principales

3. RÉSULTAT OBJECTIF
   - Ce qui s'est passé : résultat concret et mesurable
   - Écart avec l'objectif initial : objectif atteint / partiellement atteint / non atteint ?
   - Impact sur les revenus, la réputation, ou les capacités de Caelum
   - Réactions des parties prenantes

4. ANALYSE CAUSALE
   - Pourquoi ce résultat ? (causes directes, pas les symptômes)
   - Facteurs de succès ou d'échec : quels éléments ont été décisifs ?
   - Ce que Caelum a bien fait vs mal fait dans cette situation
   - Part de chance vs part de compétence dans le résultat

5. LEÇON PRINCIPALE ET LEÇONS SECONDAIRES
   - Leçon principale (1 phrase mémorable que Chaima doit retenir) :
   - Leçons secondaires (3-5 observations complémentaires numérotées)
   - Cette leçon contredit-elle ou confirme-t-elle des convictions existantes ?
   - Applicabilité : cette leçon est-elle spécifique à cette situation ou généralisable ?

6. PROTOCOLE DE PRÉVENTION / RÉPLICATION
   - Si ÉCHEC : protocole pour ne jamais répéter cette erreur (5 étapes numérotées)
   - Si SUCCÈS : protocole pour systématiquement reproduire ce résultat (5 conditions à réunir)
   - Si DÉCISION : critères de décision à documenter pour les situations similaires futures
   - Intégration dans les processus : quel processus Caelum doit-on modifier immédiatement ?

7. MÉTADONNÉES DE L'ENTRÉE
   - Tags : [secteur / type d'expérience / valeur Caelum concernée / phase de développement]
   - Priorité : leçon critique / importante / informative
   - Date de révision suggérée : quand revoir cette entrée pour vérifier si la leçon est toujours valide ?
   - Lien avec d'autres expériences passées si applicable

Format : entrée de journal institutionnel, précise, archivable, transmissible. Langue : français."""

    resultat = streamer(prompt, f"JOURNAL — Enregistrement : {type_experience}")
    sauvegarder("experience_enregistree", resultat)

def autopsie_echec():
    print("\n  Décrivez l'échec à analyser (client perdu, délai manqué, mauvaise décision, etc.) — tapez FIN pour terminer :")
    lignes = []
    while True:
        ligne = input()
        if ligne.strip().upper() == "FIN":
            break
        lignes.append(ligne)
    echec = "\n".join(lignes)[:3000]
    if not echec.strip():
        print("  Aucun échec fourni.")
        return

    prompt = f"""Effectue une autopsie complète de l'échec suivant de Caelum Partners. L'objectif : comprendre la cause racine exacte et construire un protocole de prévention définitif.

ÉCHEC À ANALYSER :
{echec}
DATE D'ANALYSE : {datetime.now().strftime('%Y-%m-%d')}

Produis une autopsie en 6 parties :

1. RECONSTITUTION CHRONOLOGIQUE DES FAITS
   - Ligne de temps précise : qu'est-ce qui s'est passé, dans quel ordre ?
   - Moment charnière : à quel point précis la situation a-t-elle basculé vers l'échec ?
   - Signaux ignorés : y avait-il des signes avant-coureurs qui ont été négligés ou mal interprétés ?
   - Ce qui aurait pu changer le cours des événements

2. MÉTHODE DES 5 POURQUOI — RECHERCHE DE LA CAUSE RACINE
   Appliquer rigoureusement la méthode :
   POURQUOI 1 : Pourquoi l'échec s'est-il produit ? → [réponse]
   POURQUOI 2 : Pourquoi [réponse 1] ? → [réponse]
   POURQUOI 3 : Pourquoi [réponse 2] ? → [réponse]
   POURQUOI 4 : Pourquoi [réponse 3] ? → [réponse]
   POURQUOI 5 : Pourquoi [réponse 4] ? → [CAUSE RACINE]
   Conclusion : la cause racine est donc [formulation précise]

3. FACTEURS CONTRIBUANTS
   - Facteurs internes à Caelum : processus défaillant, manque de compétence, mauvaise décision
   - Facteurs externes : client imprévisible, marché, technologie, timing
   - Facteurs d'amplification : qu'est-ce qui a transformé un problème gérable en échec ?
   - Part de responsabilité de Caelum : 0-100% (honnêteté radicale)

4. COÛT TOTAL DE L'ÉCHEC
   - Coût financier direct : revenus perdus, heures non facturées, remboursements éventuels
   - Coût réputationnel : impact sur la réputation, références perdues, bouche à oreille négatif possible
   - Coût en temps : heures passées sur la gestion de la crise vs heures productives
   - Coût d'opportunité : qu'est-ce que Caelum aurait pu faire avec ces ressources ?
   - Coût total estimé : [€] + [heures] + [impact réputationnel sur 12 mois]

5. PROTOCOLE DE PRÉVENTION DÉFINITIF
   - 8 mesures préventives numérotées pour rendre cet échec impossible à répéter
   - Mesures immédiates (à mettre en place cette semaine)
   - Mesures structurelles (à intégrer dans les processus permanents)
   - Indicateur d'alerte précoce : quel signal surveiller qui préfigure cette situation ?
   - Clause contractuelle ou processus client à ajouter immédiatement

6. TRANSFORMATION DE L'ÉCHEC EN ACTIF
   - Quelle compétence ou connaissance Caelum a-t-elle gagnée grâce à cet échec ?
   - Peut-on transformer cette situation en étude de cas (anonymisée) pour crédibiliser Caelum ?
   - Quelle conversation difficile mais nécessaire cet échec a-t-il forcé Caelum à avoir ?
   - Dans 12 mois, comment cet échec aura-t-il renforcé Caelum si les leçons sont intégrées ?

Format : analyse forensique, rigoureuse, orientée prévention systémique. Langue : français."""

    resultat = streamer(prompt, "AUTOPSIE — Analyse d'échec Caelum Partners")
    sauvegarder("autopsie_echec", resultat)

def extraire_patterns_succes():
    donnees_json = _lire_json_existants()

    print("\n  Décrivez vos succès récents (optionnel, pour enrichir l'analyse) — tapez FIN pour terminer :")
    lignes = []
    while True:
        ligne = input()
        if ligne.strip().upper() == "FIN":
            break
        lignes.append(ligne)
    succes_manuels = "\n".join(lignes)[:2000]

    prompt = f"""Analyse toutes les données disponibles sur les succès de Caelum Partners et extrait les patterns récurrents qui mènent aux victoires. L'objectif : construire un protocole de réplication du succès.

DONNÉES JSON EXISTANTES :
{donnees_json}

SUCCÈS DÉCRITS MANUELLEMENT :
{succes_manuels if succes_manuels.strip() else "[Aucun succès supplémentaire fourni — analyse basée sur les données JSON]"}

Produis une analyse de patterns en 6 parties :

1. INVENTAIRE DES SUCCÈS IDENTIFIÉS
   - Liste exhaustive des succès détectables dans les données disponibles
   - Pour chaque succès : description brève, résultat obtenu, date approximative
   - Classification : succès commercial / succès opérationnel / succès stratégique / succès relationnel

2. PATTERNS RÉCURRENTS — CONDITIONS DU SUCCÈS
   Identifie les patterns qui apparaissent dans au moins 2 succès :
   - Pattern 1 : [description] → observé dans [N] succès → conditions requises
   - Pattern 2 : [description] → observé dans [N] succès → conditions requises
   - [Continuer jusqu'à épuisement des patterns identifiables]
   - Pattern le plus puissant : celui qui a le plus fort impact et la plus grande fréquence

3. LES CONDITIONS NÉCESSAIRES AU SUCCÈS DE CAELUM
   Basé sur l'analyse des patterns, quelles sont les conditions qui doivent être réunies pour qu'un projet ou une action Caelum réussisse ?
   - Conditions liées au client idéal : profil, secteur, maturité digitale, budget
   - Conditions liées à l'offre : quel service, à quel prix, avec quelle promesse
   - Conditions liées au processus : quelle méthode de travail maximise les succès ?
   - Conditions liées au timing : quand proposer, quand livrer, quand faire le suivi ?

4. PROTOCOLE DE RÉPLICATION DU SUCCÈS
   - Checklist de 10 conditions à vérifier avant de lancer un projet pour maximiser les chances de succès
   - Score de probabilité de succès : si 7/10 conditions sont réunies → probabilité estimée ?
   - Conditions non négociables : lesquelles, si absentes, rendent le succès improbable ?
   - Processus de qualification d'un projet AVANT d'accepter : questions à poser systématiquement

5. ANTI-PATTERNS — CE QUI PRÉCÈDE LES ÉCHECS
   - Quelles conditions, à l'inverse, ont systématiquement précédé les échecs ou difficultés ?
   - Signal d'alarme précoce : comment reconnaître un projet à risque avant de le commencer ?
   - Décision difficile : comment refuser un projet qui ne remplit pas les conditions de succès ?

6. CAPITALISATION ET DOCUMENTATION
   - Comment transformer ces patterns en processus documenté accessible en 2 minutes ?
   - Format recommandé : checklist / flowchart / script de qualification / tableau de scoring
   - Mise à jour du protocole : à quelle fréquence revoir les patterns à mesure que Caelum accumule de l'expérience ?
   - Transmission : si Caelum recrute, comment ces patterns forment-ils la base de l'onboarding ?

Format : analyse data-driven, patterns quantifiés, protocoles reproductibles. Langue : français."""

    resultat = streamer(prompt, "PATTERNS — Extraction des formules de succès")
    sauvegarder("patterns_succes", resultat)

def generer_base_connaissance():
    donnees_json = _lire_json_existants()

    prompt = f"""Génère la base de connaissance complète et structurée de Caelum Partners à partir de toutes les données disponibles. Ce document est le "cerveau institutionnel" de l'empire.

DONNÉES DISPONIBLES :
{donnees_json}

CONTEXTE FONDATEUR :
- Entreprise : Caelum Partners, agence IA bruxelloise
- Fondatrice : Chaima Mhadbi, Bruxelles, Belgique
- Structure : ASBL (sociale/présidente) + Caelum Partners (commerciale IA)
- Services : site web 500€ (7j), automation IA 1500€ (14j), pack complet 3000€ (30j)
- Phase : lancement, bootstrappée, vision référence européenne IA pour PME en 5 ans
- Date de génération : {datetime.now().strftime('%Y-%m-%d')}

Génère la base de connaissance en 7 chapitres :

CHAPITRE 1 — IDENTITÉ ET ADN DE CAELUM PARTNERS
- Origine de la fondation : pourquoi Caelum existe-t-il ?
- Positionnement actuel et évolution envisagée
- Valeurs fondatrices et leur traduction opérationnelle
- La vision sur 5 ans : ce que "référence européenne" signifie concrètement

CHAPITRE 2 — CONNAISSANCE DU MARCHÉ
- Le marché adressable : PME belges, leur maturité digitale, leurs attentes
- Les concurrents identifiés : qui, à quel prix, avec quelles forces/faiblesses
- Les marchés adjacents cartographiés
- Tendances de marché surveillées

CHAPITRE 3 — CONNAISSANCE DES CLIENTS
- Profil du client idéal (ICP) : secteur, taille, rôle du décisionnaire, budget
- Signaux d'achat : quand un prospect devient-il prêt à acheter ?
- Objections récurrentes et réponses optimales
- Ce qui fidélise un client Caelum vs ce qui le fait partir

CHAPITRE 4 — CONNAISSANCE OPÉRATIONNELLE
- Processus de vente : de la prospection à la signature
- Processus de livraison : de la signature au livraison client, par service
- Processus de support post-livraison
- Processus d'utilisation des agents IA : lesquels pour quels cas d'usage

CHAPITRE 5 — DÉCISIONS STRATÉGIQUES ET LEUR LOGIQUE
- Principales décisions prises depuis le lancement : quoi + pourquoi + résultat
- Décisions envisagées et leur raisonnement
- Décisions abandonnées et pourquoi
- Cadre de prise de décision Caelum : comment décider quand c'est ambigu ?

CHAPITRE 6 — LEÇONS ET PROTOCOLES
- Top 10 leçons apprises depuis le lancement
- Protocoles de prévention des erreurs les plus coûteuses
- Patterns de succès documentés et reproductibles
- Ce que Caelum sait maintenant qu'elle ne savait pas au lancement

CHAPITRE 7 — ROADMAP ET DIRECTION
- Priorités des 90 prochains jours
- Jalons des 12 prochains mois
- Questions stratégiques encore ouvertes
- Ce que la base de connaissance devrait contenir dans 12 mois qu'elle ne contient pas encore

Format : base de connaissance structurée, utilisable comme référence permanente. Langue : français."""

    resultat = streamer(prompt, "BASE DE CONNAISSANCE — Cerveau institutionnel Caelum")
    sauvegarder("base_connaissance_complete", resultat)

def rapport_evolution_strategique():
    donnees_json = _lire_json_existants()

    prompt = f"""Génère le rapport d'évolution stratégique de Caelum Partners : comment la stratégie a-t-elle évolué depuis le lancement, quels déclencheurs ont provoqué chaque changement, et quel est l'ADN stratégique actuel ?

DONNÉES DISPONIBLES :
{donnees_json}

CONTEXTE :
- Caelum Partners fondée par Chaima Mhadbi à Bruxelles
- Phase actuelle : lancement, services 500€/1500€/3000€
- Date du rapport : {datetime.now().strftime('%Y-%m-%d')}

Produis le rapport en 6 sections :

1. CARTOGRAPHIE DE L'ÉVOLUTION STRATÉGIQUE
   - Ligne de temps stratégique depuis la genèse de Caelum
   - Pour chaque période identifiable : quelle était la stratégie, quels étaient les objectifs, qu'est-ce qui fonctionnait ou non ?
   - Pivots ou ajustements majeurs : qu'est-ce qui a changé dans la direction, les offres, le positionnement ?
   - Déclencheurs de chaque changement : événement externe, leçon interne, opportunité saisie, erreur corrigée

2. ANALYSE DES DÉCLENCHEURS DE CHANGEMENT
   - Quels types d'événements ont historiquement déclenché des ajustements stratégiques ?
   - Déclencheurs internes (décision de la fondatrice, capacités nouvelles) vs externes (marché, concurrence, technologie)
   - Y a-t-il un pattern dans les déclencheurs ? Caelum réagit-elle ou anticipe-t-elle ?
   - Vitesse de réponse aux signaux : Caelum s'adapte-t-elle rapidement ou lentement aux nouvelles informations ?

3. L'ADN STRATÉGIQUE ACTUEL DE CAELUM
   - Ce qui n'a PAS changé depuis le début : les constantes stratégiques immuables
   - Le positionnement fondamental : sur quoi Caelum base-t-elle sa différenciation ?
   - La logique économique centrale : comment Caelum crée-t-elle et capture-t-elle de la valeur ?
   - Les principes de décision qui guident Caelum dans l'ambiguïté

4. COHÉRENCE STRATÉGIQUE — ANALYSE CRITIQUE
   - Les décisions passées sont-elles cohérentes avec la vision déclarée ?
   - Y a-t-il des contradictions entre la stratégie déclarée et les actions réelles ?
   - Des opportunités ont-elles été manquées par manque de cohérence stratégique ?
   - La trajectoire actuelle mène-t-elle vers la vision "référence européenne en 5 ans" ?

5. SYNTHÈSE — CE QUE L'HISTOIRE DE CAELUM RÉVÈLE
   - Quelle est la théorie du succès de Caelum ? (ce que Caelum croit être la clé de sa réussite)
   - Cette théorie est-elle validée par les résultats ou encore à tester ?
   - Les compétences qui se sont révélées être les vrais avantages de Caelum
   - Ce que Caelum a appris sur elle-même qu'elle ne savait pas au départ

6. DIRECTION STRATÉGIQUE — OÙ VA CAELUM
   - Basé sur l'analyse historique, quelle est la prochaine évolution stratégique naturelle ?
   - Les questions stratégiques ouvertes que l'histoire ne permet pas encore de trancher
   - Ce que l'historien de l'empire recommande de documenter en priorité pour les 12 prochains mois
   - Message de l'historien à Chaima dans 5 ans : "Voici ce que l'histoire de Caelum nous a appris..."

Format : rapport analytique, narrative stratégique, orienté direction future. Langue : français."""

    resultat = streamer(prompt, "ÉVOLUTION — Rapport stratégique Caelum Partners")
    sauvegarder("rapport_evolution_strategique", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  HISTORIEN DE L'EMPIRE — Mémoire institutionnelle Caelum")
    print("═"*65)
    while True:
        print("\n  [menu]")
        print("  1. Enregistrer une expérience (succès/échec/décision)")
        print("  2. Autopsie d'un échec")
        print("  3. Extraire les patterns de succès")
        print("  4. Générer la base de connaissance")
        print("  5. Rapport évolution stratégique")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            enregistrer_experience()
        elif choix == "2":
            autopsie_echec()
        elif choix == "3":
            extraire_patterns_succes()
        elif choix == "4":
            generer_base_connaissance()
        elif choix == "5":
            rapport_evolution_strategique()
        else:
            print("  Choix invalide.")
