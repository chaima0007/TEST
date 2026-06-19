"""
ANALYSTE DES VALEURS ADJACENTES — Détecteur de marchés adjacents pour Caelum Partners
Usage : python agent_valeurs_adjacentes.py
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
IDENTITE = """Tu es l'Analyste des Valeurs Adjacentes de Caelum Partners, fondée par Chaima Mhadbi à Bruxelles.
Ta question directrice : "Si nous dominons le secteur A, quelle est la prochaine cible où notre avantage technique nous rend imbattables ?"
Les marchés adjacents sont ceux où les capacités actuelles de Caelum s'appliquent avec un investissement additionnel minimal.
Tu utilises trois frameworks : Matrice d'adjacence (tech existante × nouveaux segments), Jobs-to-be-Done croisé (même job, industrie différente), Levier de compétences (quelles compétences se transfèrent à 80%+ de recouvrement).
Capacités actuelles de Caelum à exploiter : orchestration de l'API Gemini, plus de 50 agents IA spécialisés, expertise conformité belge et RGPD.
Capacités supplémentaires : automatisation LinkedIn, génération de contenu multilingue FR/NL, automatisation de processus métier, bilinguisme francophone-néerlandophone.
Secteurs adjacents identifiés à explorer : legal tech (cabinets d'avocats belges), santé administrative (cliniques belges), immobilier (agences belges), RH tech (PME belges), e-commerce (retailers belges en ligne), automatisation comptable (fiducies belges).
Tarification actuelle de Caelum : site web 500€ (7j), automation IA 1500€ (14j), pack complet 3000€ (30j).
Vision : référence européenne pour les services IA aux PME en 5 ans, depuis Bruxelles.
Phase de lancement : 0 clients, la diversification prématurée est un risque, mais la cartographie est stratégique.
Tu évalues chaque marché adjacent sur 5 dimensions : taille du marché, niveau de concurrence, score de fit Caelum (0-100), barrière à l'entrée, potentiel de revenus à 18 mois.
Tu identifies la séquence optimale d'entrée : quel marché adjacent attaquer en premier, pourquoi, avec quelle offre.
Tu analyses les concurrents des marchés adjacents pour identifier leurs angles d'attaque exploitables par Caelum.
Tu construis des offres adjacentes complètes : positionnement, prix, profil client, différenciation vs acteurs établis.
Tu es stratégique, factuel, et tu ne recommandes jamais une diversification sans valider le fit technologique au préalable.
Tes analyses sont quantifiées, comparatives, et elles indiquent clairement quelles compétences existantes de Caelum se transfèrent.
Tu parles en français, tu es rigoureux, et tu penses toujours en termes de levier compétitif, pas seulement d'opportunité de marché."""

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
    os.makedirs("fichiers/valeurs_adjacentes", exist_ok=True)
    fichier = f"fichiers/valeurs_adjacentes/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def scanner_marches_adjacents():
    prompt = """Effectue une cartographie complète de tous les marchés adjacents accessibles à Caelum Partners depuis ses capacités actuelles.

Capacités actuelles de Caelum : agents IA Gemini, automatisation de processus, génération de contenu FR/NL, expertise RGPD belge, automatisation LinkedIn, développement de sites web, orchestration multi-agents.
Marché actuel : PME belges généralistes (site web 500€, automation 1500€, pack 3000€).

Pour chaque marché adjacent, produis une fiche structurée :

SECTEUR 1 : LEGAL TECH BELGE (cabinets d'avocats, notaires)
- Taille du marché en Belgique (nombre de cabinets, chiffre d'affaires estimé)
- Niveau de concurrence actuel : solutions IA existantes ciblant ce secteur en Belgique
- Score de fit Caelum /100 : quelles capacités existantes s'appliquent directement ?
- Barrière à l'entrée : réglementations spécifiques, certifications requises, confiance difficile à établir ?
- Offre potentielle Caelum : quoi vendre, à quel prix, avec quelle promesse ?
- Délai d'entrée réaliste depuis aujourd'hui

SECTEUR 2 : SANTÉ ADMINISTRATIVE (cliniques, cabinets médicaux belges)
[même structure]

SECTEUR 3 : IMMOBILIER BELGE (agences immobilières)
[même structure]

SECTEUR 4 : RH TECH (services RH pour PME belges)
[même structure]

SECTEUR 5 : E-COMMERCE BELGE (retailers en ligne)
[même structure]

SECTEUR 6 : COMPTABILITÉ ET FIDUCIAIRES BELGES
[même structure]

SECTEUR 7 : ASSOCIATIONS ET ASBL BELGES (secteur non-marchand)
[même structure — pertinent car Chaima dirige aussi une ASBL]

SYNTHÈSE FINALE :
- Tableau comparatif des 7 secteurs : score fit, taille marché, barrière, potentiel revenu 18 mois
- Top 3 marchés à cibler en priorité avec justification
- Séquence recommandée : marché 1 → marché 2 → marché 3 avec les jalons déclencheurs de chaque entrée

Format : fiches structurées, chiffres estimés, comparaison visuelle. Langue : français."""

    resultat = streamer(prompt, "SCAN — Cartographie des marchés adjacents")
    sauvegarder("scan_marches_adjacents", resultat)

def evaluer_transferabilite():
    competence = input("\n  Compétence ou service à évaluer (ex: génération de contenu IA) :\n  → ").strip()[:500]
    secteur = input("  Secteur cible à tester (ex: cabinets d'avocats belges) :\n  → ").strip()[:500]
    if not competence or not secteur:
        print("  Données insuffisantes.")
        return

    prompt = f"""Évalue la transférabilité de la compétence suivante de Caelum Partners vers le secteur cible.

COMPÉTENCE À ÉVALUER : {competence}
SECTEUR CIBLE : {secteur}
CONTEXTE : Caelum Partners, agence IA bruxelloise, phase de lancement, fondatrice Chaima Mhadbi.

Produis une analyse de transférabilité en 6 parties :

1. SCORE DE TRANSFÉRABILITÉ GLOBAL : /100
   - Décomposition du score par dimension :
     * Recouvrement technologique (les outils existants fonctionnent-ils ?) : /25
     * Recouvrement métier (la logique du service est-elle similaire ?) : /25
     * Recouvrement client (le profil client est-il similaire ?) : /25
     * Recouvrement réglementaire (les contraintes légales sont-elles maîtrisables ?) : /25

2. CE QUI SE TRANSFÈRE DIRECTEMENT (sans adaptation)
   - Liste des éléments de la compétence applicables immédiatement dans le secteur cible
   - Pourquoi ces éléments fonctionnent sans modification

3. CE QUI NÉCESSITE UNE ADAPTATION MINIMALE (1-2 semaines)
   - Éléments à ajuster et nature de l'ajustement
   - Coût estimé de l'adaptation (temps + investissement potentiel)

4. CE QUI EST INCOMPATIBLE OU NÉCESSITE UN DÉVELOPPEMENT MAJEUR
   - Lacunes critiques : compétences manquantes, certifications requises, connaissances sectorielles absentes
   - Ces lacunes sont-elles comblables ? En combien de temps ? À quel coût ?

5. PLAN D'ADAPTATION MINIMUM VIABLE
   - 10 étapes numérotées pour rendre la compétence opérationnelle dans le secteur cible
   - Délai total réaliste
   - Ressources nécessaires (temps Chaima, outils, partenaires éventuels)

6. VERDICT ET RECOMMANDATION
   - GO / NO-GO / GO CONDITIONNEL avec justification
   - Si GO conditionnel : quelles conditions doivent être remplies d'abord ?
   - Potentiel de revenus si l'adaptation réussit : estimation prudente et optimiste

Format : analytique, chiffré, décisionnel. Langue : français."""

    resultat = streamer(prompt, f"ÉVALUATION — Transférabilité vers {secteur}")
    sauvegarder("transferabilite", resultat)

def concevoir_offre_adjacente():
    secteur = input("\n  Secteur pour lequel concevoir une offre adjacente :\n  → ").strip()[:500]
    if not secteur:
        print("  Secteur non fourni.")
        return

    prompt = f"""Conçois une offre commerciale complète pour Caelum Partners dans le secteur adjacent suivant : {secteur}

Caelum Partners : agence IA bruxelloise, services actuels 500€/1500€/3000€, fondatrice Chaima Mhadbi, vision référence européenne IA pour PME.

Livre une offre complète en 6 composantes :

1. POSITIONNEMENT DE L'OFFRE ADJACENTE
   - Nom de l'offre (mémorable, sectoriel)
   - Proposition de valeur unique en 1 phrase (pas de jargon, focus résultat)
   - Différenciation vs acteurs établis dans ce secteur
   - Pourquoi Caelum est crédible dans ce secteur (pont depuis l'expertise actuelle)

2. PROFIL CLIENT IDÉAL (ICP) DANS CE SECTEUR
   - Taille d'entreprise cible, localisation, chiffre d'affaires
   - Rôle décisionnaire (qui signe ? qui prescrit ? qui utilise ?)
   - Douleur principale que l'offre résout
   - Signal déclencheur : quand ce client cherche activement une solution comme celle de Caelum ?

3. STRUCTURE DE L'OFFRE ET TARIFICATION
   - Offre de base : description des livrables, délai, prix
   - Offre intermédiaire : description des livrables, délai, prix
   - Offre premium : description des livrables, délai, prix
   - Justification des prix par rapport au marché sectoriel et à la valeur délivrée

4. DIFFÉRENCIATION CONCURRENTIELLE
   - Concurrents directs dans ce secteur : qui sont-ils, quels sont leurs prix, leurs faiblesses ?
   - Angle d'attaque de Caelum : pourquoi gagner face à ces concurrents ?
   - Argument de vente unique que les concurrents établis ne peuvent pas répliquer

5. STRATÉGIE D'ACQUISITION CLIENTS DANS CE SECTEUR
   - Canal d'acquisition principal (LinkedIn, association professionnelle, partenariat, événement)
   - Message d'approche initial (email ou LinkedIn — script prêt à l'emploi)
   - 5 actions concrètes pour obtenir le premier client dans ce secteur en 60 jours

6. MÉTRIQUES DE SUCCÈS ET JALONS
   - KPIs pour valider que l'offre fonctionne dans ce secteur
   - Critères de décision : à partir de quand considérer ce secteur comme validé ?
   - Critères d'abandon : quand stopper et pivoter vers un autre secteur adjacent ?

Format : offre commerciale complète, prête à tester sur le marché. Langue : français."""

    resultat = streamer(prompt, f"OFFRE ADJACENTE — {secteur}")
    sauvegarder("offre_adjacente", resultat)

def roadmap_diversification():
    prompt = """Construis la roadmap de diversification sur 18 mois pour Caelum Partners.

Situation de départ : agence IA bruxelloise, 0 clients, services actuels (500€/1500€/3000€), fondatrice Chaima Mhadbi seule, bootstrappée.
Marchés adjacents identifiés : legal tech, santé administrative, immobilier, RH tech, e-commerce, comptabilité, ASBL.

Produis une roadmap en 4 phases :

PHASE 0 — MOIS 1 À 3 : CONSOLIDATION DU MARCHÉ PRIMAIRE
- Objectif : obtenir les 3 premiers clients sur le marché actuel (PME généralistes belges)
- Pourquoi ne PAS diversifier pendant cette phase
- Signaux de fin de phase 0 : quand est-il temps de commencer à explorer les marchés adjacents ?
- Actions concrètes numérotées pour consolider le marché primaire

PHASE 1 — MOIS 4 À 6 : EXPLORATION ADJACENTE CIBLÉE
- Quel premier marché adjacent attaquer ? Justification basée sur le fit et la facilité d'entrée
- Format d'exploration : pas d'offre formelle, mais 3 conversations avec des prospects dans ce secteur
- Ce qu'on cherche à valider pendant cette phase
- Budget temps estimé : combien d'heures par semaine allouer à l'exploration sans nuire au marché primaire ?

PHASE 2 — MOIS 7 À 12 : LANCEMENT DE L'OFFRE ADJACENTE PRINCIPALE
- Construction de l'offre validée dans le premier marché adjacent
- Plan de lancement en 10 étapes numérotées
- Objectif : 2 clients dans le marché adjacent d'ici la fin du mois 12
- Gestion du risque : comment maintenir la qualité sur deux marchés simultanément en solo ?

PHASE 3 — MOIS 13 À 18 : DEUXIÈME MARCHÉ ADJACENT
- Conditions requises avant d'attaquer un deuxième marché adjacent
- Quel deuxième marché adjacent cibler ? Pourquoi ?
- Mutualisation des ressources : comment les agents IA développés pour marché 1 servent-ils marché 2 ?
- Vision fin mois 18 : revenus estimés, clients par marché, positionnement global de Caelum

SYNTHÈSE — TABLEAU DE BORD STRATÉGIQUE
- Calendrier visuel mois par mois
- KPIs clés à suivre pour valider chaque phase
- Points de décision critiques : GO/NO-GO pour chaque entrée dans un nouveau marché
- Risques principaux et mitigation pour chaque phase

Format : roadmap actionnable, jalons clairs, décisions explicites. Langue : français."""

    resultat = streamer(prompt, "ROADMAP — Diversification 18 mois Caelum Partners")
    sauvegarder("roadmap_diversification", resultat)

def analyser_concurrent_adjacent():
    concurrent = input("\n  Nom ou description du concurrent dans un marché adjacent à analyser :\n  → ").strip()[:500]
    if not concurrent:
        print("  Concurrent non fourni.")
        return

    prompt = f"""Analyse le concurrent suivant dans un marché adjacent que Caelum Partners pourrait cibler : {concurrent}

Caelum Partners : agence IA bruxelloise, spécialisée PME, services 500€/1500€/3000€, avantages clés = agents IA personnalisés, bilinguisme FR/NL, conformité belge.

Produis une analyse concurrentielle approfondie en 6 parties :

1. PROFIL DU CONCURRENT
   - Qui sont-ils ? (taille, localisation, date de création, équipe estimée)
   - Quels marchés servent-ils ? (secteurs, taille de clients, zones géographiques)
   - Offres actuelles : produits/services, prix si disponibles, positionnement
   - Forces apparentes : pourquoi leurs clients actuels les choisissent-ils ?

2. ANALYSE DES FAIBLESSES EXPLOITABLES
   - Faiblesses structurelles : taille (trop grande = lente), prix (trop élevé = excluant PME), technologie (stack vieillissante ?), service (support insuffisant ?)
   - Faiblesses de positionnement : zones géographiques non couvertes, segments clients ignorés, langues non servies
   - Faiblesses opérationnelles : délais de livraison, qualité client, personnalisation limitée
   - Faiblesses perçues : avis clients négatifs, plaintes courantes, réputation sectorielle

3. ANGLE D'ATTAQUE DE CAELUM
   - Quelle faiblesse du concurrent Caelum peut-elle exploiter directement avec ses capacités actuelles ?
   - Message de différenciation spécifique face à ce concurrent
   - Segment de clients du concurrent que Caelum peut séduire en priorité
   - Pourquoi un client actuel de ce concurrent quitterait-il pour Caelum ?

4. STRATÉGIE DE POSITIONNEMENT OPPOSÉ
   - Si le concurrent est lent → Caelum se positionne sur la vitesse (délais garantis)
   - Si le concurrent est cher → Caelum se positionne sur l'accessibilité PME
   - Si le concurrent est généraliste → Caelum se positionne sur la spécialisation sectorielle
   - Message clé en 1 phrase : "Contrairement à [concurrent], Caelum [différenciation]"

5. SCÉNARIO D'ENTRÉE EN 90 JOURS
   - Comment Caelum entre dans ce marché en contournant directement ce concurrent
   - 10 actions numérotées sur 90 jours pour capturer les premiers clients
   - Comment éviter une guerre de prix frontale

6. VEILLE ET SURVEILLANCE
   - Comment surveiller ce concurrent sans y passer trop de temps (alertes Google, LinkedIn, etc.)
   - Signaux à surveiller : nouvelles offres, levée de fonds, départs d'équipe, nouveaux clients
   - Fréquence de revue recommandée

Format : analyse stratégique actionnable, orientée compétition intelligente. Langue : français."""

    resultat = streamer(prompt, f"CONCURRENT — Analyse de {concurrent}")
    sauvegarder("analyse_concurrent_adjacent", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  ANALYSTE DES VALEURS ADJACENTES — Marchés à conquérir")
    print("═"*65)
    while True:
        print("\n  [menu]")
        print("  1. Scanner les marchés adjacents")
        print("  2. Évaluer la transférabilité d'une compétence")
        print("  3. Concevoir une offre adjacente")
        print("  4. Roadmap diversification 18 mois")
        print("  5. Analyser un concurrent adjacent")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            scanner_marches_adjacents()
        elif choix == "2":
            evaluer_transferabilite()
        elif choix == "3":
            concevoir_offre_adjacente()
        elif choix == "4":
            roadmap_diversification()
        elif choix == "5":
            analyser_concurrent_adjacent()
        else:
            print("  Choix invalide.")
