"""
MAÎTRE DE LA CULTURE INTERNE — Architecte des standards d'excellence de Caelum Partners
Usage : python agent_culture_interne.py
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
IDENTITE = """Tu es le Maître de la Culture Interne de Caelum Partners, fondée par Chaima Mhadbi à Bruxelles.
Ta conviction fondamentale : "Chaque décision doit refléter l'excellence opérationnelle de Caelum Partners. Si ça ne correspond pas aux standards, ça ne sort pas."
La culture pour une fondatrice solo, c'est : les standards que Chaima s'applique à elle-même, le niveau de qualité de chaque livrable, l'état d'esprit pour chaque interaction, et l'alignement de chaque agent IA avec les valeurs de Caelum.
Les cinq valeurs non négociables de Caelum Partners sont les suivantes.
Excellence : rien ne sort en dessous du standard défini — un livrable moyen est un livrable refusé.
Vélocité : fait > parfait, mais fait bien — la vitesse et la qualité ne s'excluent pas, elles se complètent.
Intégrité : ne promettre que ce qui est livrable, livrer exactement ce qui a été promis — zéro écart.
Innovation : chaque projet doit apporter quelque chose de nouveau à Caelum — aucun projet ne doit être "routinier".
Client-First : le succès du client est le succès de Caelum — pas de satisfaction Caelum sans satisfaction client.
Les standards opérationnels à maintenir sont : qualité des propositions (professionnelles, légales, complètes, sans faute), qualité des livrables (dans les délais, documentés, avec support post-livraison), qualité de la communication (claire, rapide moins de 4 heures, bilingue FR/NL si nécessaire), qualité des agents (tous les outputs des agents sont revus avant livraison client — jamais de livraison brute).
La culture solo est plus difficile à maintenir qu'une culture d'équipe : personne pour rappeler les standards, personne pour signaler la dérive.
Les pièges de la culture solo : la fatigue qui abaisse les standards, les clients difficiles qui poussent aux compromis, la pression du temps qui raccourcit les processus.
Tu évalues les livrables avec précision, tu génères des checklists actionnables, et tu rappelles les valeurs de Caelum à chaque analyse.
Tu construis des rituels et des systèmes qui maintiennent la culture sans y penser — des automatismes d'excellence.
Tu alignes les 50+ agents IA de Caelum sur les valeurs : un agent qui produit un output médiocre trahit la culture Caelum.
Tu parles en français, tu es exigeant mais constructif, et tu sais qu'une culture forte est la seule protection contre la médiocrité systémique."""

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
    os.makedirs("fichiers/culture_interne", exist_ok=True)
    fichier = f"fichiers/culture_interne/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def evaluer_standard_livrable():
    print("\n  Décrivez ou collez le livrable à évaluer — tapez FIN sur une ligne seule pour terminer :")
    lignes = []
    while True:
        ligne = input()
        if ligne.strip().upper() == "FIN":
            break
        lignes.append(ligne)
    description = "\n".join(lignes)[:4000]
    if not description.strip():
        print("  Aucun livrable fourni.")
        return

    prompt = f"""Évalue le livrable suivant selon les standards de Caelum Partners. Sois exigeant et précis — le but est d'élever la qualité, pas de valider la médiocrité.

LIVRABLE À ÉVALUER :
{description}

Effectue une évaluation en 6 dimensions :

1. EXCELLENCE — Score /20
   - Ce livrable est-il au niveau d'un professionnel reconnu dans son domaine ?
   - Qu'est-ce qui est clairement en dessous du standard d'excellence Caelum ?
   - Qu'est-ce qui est exemplaire et doit être maintenu ou amplifié ?
   - Score /20 avec justification ligne par ligne

2. VÉLOCITÉ — Score /20
   - Ce livrable a-t-il été produit avec la vitesse attendue (7j site, 14j automation, 30j pack) ?
   - Y a-t-il des éléments qui auraient pu être produits plus rapidement sans perte de qualité ?
   - Y a-t-il des raccourcis qui ont sacrifié la qualité au profit de la vitesse ?
   - Score /20 avec recommandations de processus

3. INTÉGRITÉ — Score /20
   - Ce qui a été promis dans la proposition correspond-il exactement à ce qui est livré ?
   - Y a-t-il des écarts entre la promesse et le livrable (en plus ou en moins) ?
   - Les conditions négociées (révisions, support, délais) sont-elles respectées ?
   - Score /20 avec liste des écarts identifiés

4. INNOVATION — Score /20
   - Ce projet a-t-il apporté quelque chose de nouveau à Caelum ? Quelle leçon transférable ?
   - Le livrable utilise-t-il les capacités les plus avancées disponibles, ou des solutions génériques ?
   - Y a-t-il une opportunité d'innovation manquée dans ce livrable ?
   - Score /20 avec suggestion d'innovation applicable au prochain projet similaire

5. CLIENT-FIRST — Score /20
   - Ce livrable résout-il le problème réel du client ou juste le problème exprimé ?
   - Y a-t-il des éléments qui ont été inclus pour Caelum (showcase) plutôt que pour le client ?
   - Le livrable est-il compréhensible et utilisable par le client sans expertise technique ?
   - Score /20 avec ajustements recommandés orientés client

6. SCORE GLOBAL ET VERDICT
   - Score total /100
   - VERDICT : LIVRABLE APPROUVÉ / LIVRABLE À CORRIGER / LIVRABLE REJETÉ
   - Si correction requise : liste des 5 corrections prioritaires numérotées avec délai de correction estimé
   - Si approuvé : 2 éléments à documenter comme "bonnes pratiques Caelum" pour les futurs projets

Format : évaluation rigoureuse, scores justifiés, corrections actionnables. Langue : français."""

    resultat = streamer(prompt, "ÉVALUATION — Standard de qualité Caelum")
    sauvegarder("evaluation_livrable", resultat)

def generer_charte_culture():
    prompt = """Génère la charte culture complète et officielle de Caelum Partners — le document fondateur qui définit qui nous sommes, comment nous travaillons, et ce que nous refusons de faire.

Caelum Partners : agence IA bruxelloise, fondatrice Chaima Mhadbi, services 500€/1500€/3000€, vision référence européenne IA pour PME en 5 ans.

La charte doit couvrir 6 sections :

1. DÉCLARATION D'IDENTITÉ CULTURELLE
   - Qui est Caelum Partners au-delà de ses services ? (la raison d'être profonde)
   - Ce que Caelum représente pour ses clients, pour l'écosystème belge, pour l'avenir de l'IA en Europe
   - La promesse implicite que chaque interaction Caelum fait au monde
   - Formulation mémorable de l'identité en 3 phrases (comme un manifeste)

2. LES CINQ VALEURS — DÉFINITIONS OPÉRATIONNELLES
   Pour chaque valeur (Excellence, Vélocité, Intégrité, Innovation, Client-First) :
   - Définition précise appliquée au contexte Caelum (pas une définition générique)
   - Ce que cette valeur signifie concrètement au quotidien
   - Ce que cette valeur INTERDIT (les comportements opposés)
   - Exemple concret d'une décision guidée par cette valeur dans le contexte Caelum

3. STANDARDS DE QUALITÉ PAR TYPE DE SERVICE
   SITE WEB 500€ — Standards non négociables :
   - Checklist de 10 éléments minimum avant livraison
   - Délai de livraison garanti et politique si dépassé
   - Standard de communication client pendant le projet
   - Standard de support post-livraison

   AUTOMATION IA 1500€ — Standards non négociables :
   [même structure]

   PACK COMPLET 3000€ — Standards non négociables :
   [même structure]

4. LES NON-NÉGOCIABLES — CE QUE CAELUM NE FAIT JAMAIS
   - 10 comportements, pratiques, ou compromis que Caelum refuse absolument
   - Pour chaque non-négociable : pourquoi c'est une ligne rouge et ce qui se passe si elle est franchie
   - Exemple : "Caelum ne livre jamais un agent IA sans revue humaine du premier output"

5. RITUELS D'EXCELLENCE QUOTIDIENS
   - Liste des 7 habitudes journalières qui maintiennent la culture sans effort conscient
   - Rituels hebdomadaires : qu'est-ce qui doit être fait chaque semaine pour auditer la qualité ?
   - Rituels mensuels : quel bilan de culture faire chaque mois ?
   - Comment transformer les standards en automatismes plutôt qu'en contraintes perçues

6. ÉVOLUTION DE LA CULTURE
   - Cette charte est-elle figée ou évolutive ? Comment la faire évoluer sans perdre le cœur des valeurs ?
   - Processus de révision annuelle : quand et comment revoir la charte ?
   - Comment la culture Caelum devra-t-elle évoluer si l'équipe s'agrandit (de solo à 3-5 personnes) ?

Format : document officiel, prêt à être utilisé comme référence interne. Langue : français."""

    resultat = streamer(prompt, "CHARTE — Culture officielle Caelum Partners")
    sauvegarder("charte_culture", resultat)

def audit_alignement_agents():
    prompt = """Effectue un audit d'alignement culturel des agents IA de Caelum Partners. L'objectif : vérifier si les 50+ agents produisent des outputs qui reflètent les valeurs de Caelum ou si certains les trahissent.

Valeurs de Caelum : Excellence, Vélocité, Intégrité, Innovation, Client-First.

Produis un framework d'audit en 5 parties :

1. CRITÈRES D'ALIGNEMENT CULTUREL POUR UN AGENT IA CAELUM
   Pour qu'un agent soit considéré "aligné Caelum", il doit satisfaire à 10 critères :
   - Critères liés à l'Excellence : quels standards de qualité d'output un agent doit-il respecter ?
   - Critères liés à la Vélocité : temps de réponse, longueur d'output optimale, efficacité des prompts
   - Critères liés à l'Intégrité : transparence sur les limites de l'IA, pas de confabulation présentée comme fait
   - Critères liés à l'Innovation : l'agent utilise-t-il les capacités les plus avancées disponibles ?
   - Critères liés au Client-First : l'agent parle-t-il le langage du client ou jargon technique ?

2. SIGNAUX D'ALERTE — QUAND UN AGENT TRAHIT LES VALEURS CAELUM
   - Outputs génériques qui ne reflètent pas la spécificité Caelum (anti-Excellence)
   - Réponses trop longues, trop lentes, inefficaces (anti-Vélocité)
   - Affirmations non vérifiées, promesses excessives dans les outputs (anti-Intégrité)
   - Utilisation de templates sans adaptation au contexte spécifique (anti-Innovation)
   - Outputs orientés "impressionner" plutôt que "résoudre" (anti-Client-First)

3. PROCÉDURE D'AUDIT D'UN AGENT EN 15 MINUTES
   - 8 questions à poser à un agent pour tester son alignement
   - Comment interpréter les réponses : scoring 0-5 par dimension
   - Score d'alignement global /25 par agent
   - Seuil de requalification : en dessous de quel score l'agent doit-il être reconfiguré ?

4. PROCESSUS DE RECALIBRAGE D'UN AGENT NON ALIGNÉ
   - Étapes pour recalibrer un agent : révision du system prompt, ajout d'exemples, test et validation
   - Comment documenter chaque itération pour ne pas refaire les mêmes erreurs
   - Délai moyen de recalibrage par agent : estimation et processus

5. SYSTÈME DE MAINTENANCE CULTURELLE DES AGENTS
   - Fréquence d'audit recommandée par type d'agent (agents clients vs agents internes)
   - Processus d'intégration culturelle pour tout nouveau agent créé
   - Comment intégrer la "charte culture" directement dans les system prompts des agents
   - Template de system prompt "aligné Caelum" : structure qui garantit l'alignement par défaut

Format : framework opérationnel, procédures numérotées, critères de décision clairs. Langue : français."""

    resultat = streamer(prompt, "AUDIT — Alignement culturel des agents IA Caelum")
    sauvegarder("audit_alignement_agents", resultat)

def rituel_excellence_quotidien():
    prompt = """Conçois le rituel d'excellence quotidien de Chaima Mhadbi, fondatrice solo de Caelum Partners, pour maintenir les standards culturels sans équipe qui les rappelle.

Le défi solo : sans équipe, les standards se dégradent progressivement et invisiblement. Le rituel est le système qui compense.

Conçois un système complet de rituels en 4 temporalités :

1. RITUEL QUOTIDIEN — 15 MINUTES CHRONO
   Matin (5 minutes) :
   - Revue des 3 engagements du jour (alignement Vélocité + Intégrité)
   - Vérification : y a-t-il des communications en attente de réponse depuis plus de 4h ?
   - Intention du jour : quelle valeur Caelum sera-t-elle particulièrement sollicitée aujourd'hui ?

   Avant chaque livraison (5 minutes) :
   - Checklist de 5 questions à se poser avant d'envoyer n'importe quel output à un client
   - Question filtre : "Est-ce que je signerais fièrement ce livrable ?" → si non, qu'est-ce qui manque ?
   - Revue RGPD rapide : ce document contient-il des données clients à protéger ?

   Soir (5 minutes) :
   - Bilan du jour : un succès à documenter, une leçon à intégrer
   - Revue de la to-do de demain : est-elle réaliste (Vélocité) et complète (Excellence) ?
   - Déconnexion intentionnelle : à quelle heure stopper pour maintenir la qualité sur la durée

2. RITUEL HEBDOMADAIRE — 30 MINUTES (vendredi ou lundi)
   - Revue de la semaine : score personnel /10 sur chacune des 5 valeurs Caelum cette semaine
   - Audit rapide des livrables de la semaine : y a-t-il un output dont on n'est pas fier ?
   - Revue des communications : y a-t-il eu des délais de réponse client inacceptables ?
   - Une leçon documentée dans le journal d'apprentissage
   - Ajustement des processus : quel processus améliorer la semaine prochaine ?

3. RITUEL MENSUEL — 2 HEURES (dernier vendredi du mois)
   - Audit de culture complète : les valeurs Caelum ont-elles été tenues ce mois ?
   - Revue de tous les livrables du mois : score d'excellence moyen
   - Bilan des agents IA : y en a-t-il qui dérivent des standards Caelum ?
   - Revue des finances : le modèle économique tient-il les promesses ?
   - Décision stratégique mensuelle : quelle priorité pour le mois suivant ?

4. RITUELS DE CRISE — QUAND LES STANDARDS SONT SOUS PRESSION
   Situation A — Fatigue ou surcharge :
   - Protocole de préservation de la qualité sous pression de temps
   - Ce qu'on peut déléguer aux agents IA vs ce qui nécessite l'attention humaine
   - Signal d'alarme : comment reconnaître que la fatigue affecte la qualité avant qu'un client le voie ?

   Situation B — Client difficile qui pousse aux compromis :
   - Comment tenir les standards sans perdre le client
   - Script de conversation pour remettre un client dans le cadre de la charte
   - Quand accepter de perdre un client plutôt que de compromettre les valeurs

   Situation C — Pression de délai extrême :
   - Protocole de livraison d'urgence : comment livrer vite sans sacrifier l'Intégrité
   - Ce qu'on dit au client quand on ne peut pas tenir le délai standard
   - Post-mortem obligatoire : comment éviter que cette situation se reproduise

Format : protocoles pratiques, timings précis, scripts prêts à l'emploi. Langue : français."""

    resultat = streamer(prompt, "RITUELS — Excellence quotidienne Caelum Partners")
    sauvegarder("rituel_excellence", resultat)

def gerer_dilution_mission():
    situation = input("\n  Décrivez la situation où les standards risquent d'être compromis :\n  → ").strip()[:2000]
    if not situation:
        print("  Aucune situation fournie.")
        return

    prompt = f"""Caelum Partners (agence IA, Bruxelles, fondatrice Chaima Mhadbi) fait face à une situation de dilution de mission potentielle :

SITUATION DÉCRITE : {situation}

Fournis un protocole complet de protection de la mission en 5 parties :

1. DIAGNOSTIC DE LA DILUTION
   - Quelle(s) valeur(s) de Caelum est (sont) en danger dans cette situation ? (Excellence/Vélocité/Intégrité/Innovation/Client-First)
   - Niveau de risque de dilution : ÉLEVÉ / MODÉRÉ / FAIBLE — avec justification
   - Est-ce une dilution temporaire acceptable ou une dérive systémique à stopper immédiatement ?
   - Y a-t-il déjà eu compromis sur les standards dans des situations similaires ? Quel précédent dangereux cela crée-t-il ?

2. ANALYSE DES PRESSIONS EN JEU
   - Pression financière : quelle est la pression économique réelle dans cette situation ?
   - Pression relationnelle : y a-t-il une relation client ou personnelle qui biaise le jugement ?
   - Pression temporelle : le délai est-il réellement incompressible ou semble-t-il urgent ?
   - Pression d'ego : y a-t-il une envie de "dire oui" pour paraître accommodant ou compétent ?

3. PROTOCOLE DE PROTECTION IMMÉDIATE
   - Actions à prendre dans les prochaines 24h pour protéger les standards
   - Ce qu'il faut dire au client / partenaire / interlocuteur concerné : script exact en français
   - Ce qu'il ne faut PAS faire : les réponses réactives qui créent plus de problèmes
   - Comment gagner du temps si la décision n'est pas encore claire

4. DÉCISION STRATÉGIQUE — TENIR OU ADAPTER
   OPTION A — TENIR LES STANDARDS ABSOLUMENT :
   - Comment tenir la position sans nuire à la relation ?
   - Conséquences acceptables de cette décision
   - Comment transformer ce "non" en démonstration de professionnalisme ?

   OPTION B — ADAPTATION PONCTUELLE ET ENCADRÉE :
   - Dans quelles conditions une exception est-elle acceptable ? (critères précis)
   - Comment accorder l'exception sans créer un précédent dangereux ?
   - Garde-fous à mettre en place pour que cette exception reste unique

5. PRÉVENTION SYSTÉMIQUE
   - Quel processus ou garde-fou aurait évité cette situation ?
   - Clause contractuelle ou processus client à ajouter immédiatement
   - Comment documenter cet incident pour que la même situation soit gérée plus vite la prochaine fois ?
   - Leçon de culture : que dit cette situation sur les standards à renforcer dans la charte Caelum ?

Format : protocole de décision clair, scripts prêts, orienté maintien des valeurs. Langue : français."""

    resultat = streamer(prompt, "PROTECTION — Mission et standards Caelum")
    sauvegarder("protection_mission", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  MAÎTRE DE LA CULTURE INTERNE — Standards d'excellence Caelum")
    print("═"*65)
    while True:
        print("\n  [menu]")
        print("  1. Évaluer le standard d'un livrable")
        print("  2. Générer la charte culture Caelum")
        print("  3. Audit alignement des agents")
        print("  4. Rituel excellence quotidien")
        print("  5. Gérer la dilution de mission")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            evaluer_standard_livrable()
        elif choix == "2":
            generer_charte_culture()
        elif choix == "3":
            audit_alignement_agents()
        elif choix == "4":
            rituel_excellence_quotidien()
        elif choix == "5":
            gerer_dilution_mission()
        else:
            print("  Choix invalide.")
