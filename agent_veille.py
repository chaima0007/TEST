import os
import json
import datetime
import google.generativeai as genai
from memoire import ajouter_interaction, charger_memoire, incrementer_stat

MODEL = "gemini-2.0-flash"

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL)

ENTREPRISE = "AgentClaude Solutions"
DOMAINE = "solutions d'agents IA autonomes"


def streamer(prompt: str) -> str:
    response = model.generate_content(prompt, stream=True)
    texte_complet = ""
    for chunk in response:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            texte_complet += chunk.text
    print()
    return texte_complet


def sauvegarder_rapport(nom_fichier: str, contenu: str) -> str:
    horodatage = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = f"/home/user/TEST/rapports/{nom_fichier}_{horodatage}.txt"
    os.makedirs("/home/user/TEST/rapports", exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


def agent_analyse_concurrent(nom: str, secteur: str) -> str:
    memoire = charger_memoire()
    contexte_memoire = json.dumps(memoire, ensure_ascii=False, indent=2) if memoire else "Aucune analyse précédente."

    prompt = f"""Tu es un analyste stratégique senior spécialisé en intelligence concurrentielle pour {ENTREPRISE}, une entreprise spécialisée dans les {DOMAINE}.

Contexte mémoire des analyses précédentes :
{contexte_memoire}

Effectue une analyse concurrentielle approfondie de "{nom}" qui opère dans le secteur "{secteur}".

Structure ton analyse en sections claires :

## 1. POSITIONNEMENT STRATÉGIQUE
- Proposition de valeur principale
- Positionnement sur le marché des agents IA
- Segment de marché ciblé

## 2. FORCES ET FAIBLESSES
### Forces
- Liste des points forts identifiés
### Faiblesses
- Liste des points faibles identifiés

## 3. STRATÉGIE TARIFAIRE
- Modèles de tarification utilisés
- Gammes de prix estimées
- Stratégie de monétisation

## 4. CLIENTS CIBLES
- Profil des clients principaux
- Industries et secteurs ciblés
- Taille d'entreprise visée

## 5. STRATÉGIE IA ET TECHNOLOGIE
- Approche technologique des agents IA
- Technologies et frameworks utilisés
- Niveau de maturité de l'offre IA

## 6. POSITIONNEMENT FACE À {ENTREPRISE.upper()}
- Points de différenciation avec {ENTREPRISE}
- Zones de chevauchement concurrentiel
- Opportunités de différenciation pour {ENTREPRISE}

Sois précis, concret et actionnable. Base-toi sur des données réelles du marché des agents IA autonomes.
"""

    print(f"\n[ANALYSE CONCURRENTIELLE — {nom.upper()}]\n")
    print("-" * 60)
    resultat = streamer(prompt)

    ajouter_interaction(
        type_interaction="analyse_concurrent",
        contenu={
            "concurrent": nom,
            "secteur": secteur,
            "resume": resultat[:500]
        }
    )
    incrementer_stat("analyses_concurrents")

    chemin = sauvegarder_rapport(f"analyse_{nom.lower().replace(' ', '_')}", resultat)
    print(f"\n[Rapport sauvegardé : {chemin}]")

    return resultat


def agent_veille_marche(secteur: str) -> str:
    memoire = charger_memoire()
    contexte_memoire = json.dumps(memoire, ensure_ascii=False, indent=2) if memoire else "Aucune veille précédente."

    prompt = f"""Tu es un expert en veille stratégique et intelligence de marché pour {ENTREPRISE}, spécialisée dans les {DOMAINE}.

Contexte des analyses précédentes :
{contexte_memoire}

Réalise une veille marché complète sur le secteur "{secteur}" avec un focus sur le marché des agents IA autonomes.

## 1. ÉTAT DU MARCHÉ DES AGENTS IA
- Taille et croissance du marché
- Acteurs dominants actuels
- Dynamiques de consolidation

## 2. TENDANCES ÉMERGENTES
- Tendances technologiques majeures
- Évolution des usages et cas d'utilisation
- Nouvelles architectures d'agents IA

## 3. OPPORTUNITÉS DE MARCHÉ
- Segments sous-exploités
- Besoins non satisfaits des entreprises
- Niches à fort potentiel pour {ENTREPRISE}

## 4. MENACES ET RISQUES
- Risques compétitifs (Big Tech, startups)
- Risques réglementaires (IA Act, RGPD)
- Risques technologiques (obsolescence)

## 5. MOUVEMENTS STRATÉGIQUES RÉCENTS
- Levées de fonds notables
- Acquisitions et partenariats
- Lancements de produits significatifs

## 6. SIGNAUX FAIBLES
- Tendances émergentes à surveiller
- Technologies de rupture potentielles
- Changements de comportement des acheteurs

## 7. RECOMMANDATIONS POUR {ENTREPRISE.upper()}
- Actions prioritaires à court terme (3 mois)
- Positionnement stratégique à moyen terme (1 an)

Fournis une analyse dense, factuelle et orientée décision stratégique.
"""

    print(f"\n[VEILLE MARCHÉ — {secteur.upper()}]\n")
    print("-" * 60)
    resultat = streamer(prompt)

    ajouter_interaction(
        type_interaction="veille_marche",
        contenu={
            "secteur": secteur,
            "resume": resultat[:500]
        }
    )
    incrementer_stat("veilles_marche")

    chemin = sauvegarder_rapport(f"veille_marche_{secteur.lower().replace(' ', '_')}", resultat)
    print(f"\n[Rapport sauvegardé : {chemin}]")

    return resultat


def agent_rapport_concurrentiel(concurrents_analyses: list[dict]) -> str:
    memoire = charger_memoire()
    contexte_memoire = json.dumps(memoire, ensure_ascii=False, indent=2) if memoire else "Aucune donnée mémorisée."

    concurrents_str = "\n\n".join([
        f"### {c.get('nom', 'Inconnu')} ({c.get('secteur', 'N/A')})\n{c.get('analyse', '')[:800]}..."
        for c in concurrents_analyses
    ])

    prompt = f"""Tu es le Directeur Stratégique de {ENTREPRISE}, spécialisée dans les {DOMAINE}.

Mémoire des analyses précédentes :
{contexte_memoire}

Analyses des concurrents disponibles :
{concurrents_str}

Génère un rapport de positionnement concurrentiel complet et stratégique.

# RAPPORT DE POSITIONNEMENT CONCURRENTIEL
## {ENTREPRISE.upper()} — {datetime.datetime.now().strftime("%B %Y").upper()}

## RÉSUMÉ EXÉCUTIF
- Synthèse en 5 points clés de la situation concurrentielle
- Position actuelle de {ENTREPRISE} sur le marché

## 1. CARTOGRAPHIE CONCURRENTIELLE
- Matrice de positionnement des acteurs clés
- Analyse comparative des propositions de valeur
- Segments où {ENTREPRISE} est leader / challenger / suiveur

## 2. AVANTAGES CONCURRENTIELS DE {ENTREPRISE.upper()}
- Différenciateurs uniques et défendables
- Barrières à l'entrée que nous pouvons construire
- Assets stratégiques à valoriser

## 3. ZONES DE VULNÉRABILITÉ
- Fronts concurrentiels les plus exposés
- Risques de disruption identifiés
- Lacunes à combler en priorité

## 4. ANALYSE SWOT CONCURRENTIELLE
| Dimension | Éléments clés |
|-----------|---------------|
| Forces | ... |
| Faiblesses | ... |
| Opportunités | ... |
| Menaces | ... |

## 5. RECOMMANDATIONS STRATÉGIQUES
### Court terme (0-3 mois)
- Actions immédiates à fort impact

### Moyen terme (3-12 mois)
- Initiatives stratégiques à lancer

### Long terme (1-3 ans)
- Vision et repositionnement stratégique

## 6. INDICATEURS DE SUIVI (KPIs)
- Métriques pour mesurer la position concurrentielle
- Signaux d'alerte à surveiller

Sois ambitieux, précis et orienté résultats. Ce rapport doit guider les décisions de direction.
"""

    print(f"\n[RAPPORT CONCURRENTIEL COMPLET — {ENTREPRISE.upper()}]\n")
    print("-" * 60)
    resultat = streamer(prompt)

    ajouter_interaction(
        type_interaction="rapport_concurrentiel",
        contenu={
            "nb_concurrents": len(concurrents_analyses),
            "concurrents": [c.get("nom") for c in concurrents_analyses],
            "resume": resultat[:500]
        }
    )
    incrementer_stat("rapports_concurrentiels")

    chemin = sauvegarder_rapport("rapport_concurrentiel_complet", resultat)
    print(f"\n[Rapport sauvegardé : {chemin}]")

    return resultat


def agent_opportunites(profil_entreprise: str, analyse_marche: str) -> str:
    memoire = charger_memoire()
    contexte_memoire = json.dumps(memoire, ensure_ascii=False, indent=2) if memoire else "Aucune donnée mémorisée."

    prompt = f"""Tu es un consultant en développement commercial et stratégie de croissance spécialisé dans l'IA pour {ENTREPRISE}.

Profil de l'entreprise :
{profil_entreprise}

Analyse de marché disponible :
{analyse_marche[:1500]}

Mémoire des analyses précédentes :
{contexte_memoire}

Identifie les 5 meilleures opportunités business concrètes pour {ENTREPRISE} dans le marché des {DOMAINE}.

Pour chaque opportunité, fournis :

---

## OPPORTUNITÉ N°[X] : [TITRE ACCROCHEUR]

### Description
Explication claire de l'opportunité identifiée.

### Marché adressable
- Taille estimée du segment
- Nombre de clients potentiels
- Revenu potentiel pour {ENTREPRISE}

### Pourquoi maintenant ?
- Facteurs de timing favorables
- Fenêtre d'opportunité estimée

### Avantage compétitif de {ENTREPRISE}
- Pourquoi {ENTREPRISE} est bien positionnée
- Différenciateurs à mettre en avant

### Plan d'action (90 jours)
1. Semaine 1-2 : ...
2. Semaine 3-4 : ...
3. Mois 2-3 : ...

### Indicateurs de succès
- KPI principal à atteindre
- Jalons intermédiaires

### Niveau de priorité : [CRITIQUE / HAUTE / MOYENNE]
### Effort estimé : [FAIBLE / MOYEN / ÉLEVÉ]
### ROI potentiel : [estimation]

---

Classe les opportunités par ordre de priorité décroissante. Sois concret, chiffré et immédiatement actionnable.
"""

    print(f"\n[IDENTIFICATION D'OPPORTUNITÉS — {ENTREPRISE.upper()}]\n")
    print("-" * 60)
    resultat = streamer(prompt)

    ajouter_interaction(
        type_interaction="analyse_opportunites",
        contenu={
            "resume": resultat[:500]
        }
    )
    incrementer_stat("analyses_opportunites")

    chemin = sauvegarder_rapport("opportunites_business", resultat)
    print(f"\n[Rapport sauvegardé : {chemin}]")

    return resultat


def afficher_menu():
    print("\n" + "=" * 60)
    print(f"  SYSTÈME DE VEILLE CONCURRENTIELLE — {ENTREPRISE.upper()}")
    print("=" * 60)
    print("  1. Analyser un concurrent")
    print("  2. Veille marché IA")
    print("  3. Rapport concurrentiel complet")
    print("  4. Identifier opportunités")
    print("  0. Quitter")
    print("=" * 60)
    return input("  Votre choix : ").strip()


def main():
    concurrents_session: list[dict] = []
    derniere_veille: str = ""

    print(f"\nBienvenue dans le système de veille concurrentielle de {ENTREPRISE}.")
    print(f"Domaine : {DOMAINE}")

    while True:
        choix = afficher_menu()

        if choix == "1":
            print("\n[ANALYSE D'UN CONCURRENT]")
            nom = input("Nom du concurrent : ").strip()
            if not nom:
                print("Nom invalide.")
                continue
            secteur = input("Secteur d'activité : ").strip() or "Intelligence artificielle"
            analyse = agent_analyse_concurrent(nom, secteur)
            concurrents_session.append({"nom": nom, "secteur": secteur, "analyse": analyse})

        elif choix == "2":
            print("\n[VEILLE MARCHÉ IA]")
            secteur = input("Secteur à analyser (défaut : agents IA autonomes) : ").strip()
            if not secteur:
                secteur = "agents IA autonomes"
            derniere_veille = agent_veille_marche(secteur)

        elif choix == "3":
            print("\n[RAPPORT CONCURRENTIEL COMPLET]")
            if not concurrents_session:
                print("Aucun concurrent analysé dans cette session.")
                ajouter_quand_meme = input("Saisir manuellement des concurrents ? (o/n) : ").strip().lower()
                if ajouter_quand_meme == "o":
                    while True:
                        nom = input("Nom du concurrent (vide pour terminer) : ").strip()
                        if not nom:
                            break
                        concurrents_session.append({"nom": nom, "secteur": "IA", "analyse": ""})
                else:
                    print("Veuillez d'abord analyser au moins un concurrent (option 1).")
                    continue
            agent_rapport_concurrentiel(concurrents_session)

        elif choix == "4":
            print("\n[IDENTIFICATION D'OPPORTUNITÉS]")
            print("Décrivez le profil de votre entreprise :")
            print(f"(Appuyez sur Entrée pour utiliser le profil par défaut de {ENTREPRISE})")
            profil = input("> ").strip()
            if not profil:
                profil = (
                    f"{ENTREPRISE} est une startup française spécialisée dans le développement "
                    f"et le déploiement de {DOMAINE} pour les entreprises B2B. "
                    "Nous ciblons les PME et ETI souhaitant automatiser leurs processus métier "
                    "grâce à des agents IA personnalisés et autonomes. "
                    "Notre équipe compte 15 personnes dont 10 ingénieurs IA. "
                    "Nous avons levé 2M€ en amorçage et visons une croissance x3 sur 18 mois."
                )

            if not derniere_veille:
                print("Aucune veille marché disponible. Génération d'une analyse rapide...")
                derniere_veille = agent_veille_marche("agents IA autonomes entreprise")

            agent_opportunites(profil, derniere_veille)

        elif choix == "0":
            print(f"\nMerci d'avoir utilisé le système de veille de {ENTREPRISE}. À bientôt !")
            break

        else:
            print("Choix invalide. Veuillez saisir 0, 1, 2, 3 ou 4.")


if __name__ == "__main__":
    main()
