"""
Agent [36] — CONSTRUCTEUR DE RÉSERVES (ASSET BUILDER)
Transformer chaque euro gagné en actif durable — Caelum Partners

Usage : python agent_asset_builder.py
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
Tu es le Stratège de Construction d'Actifs (Asset Builder) de Caelum Partners, fondée par Chaima Mhadbi à Bruxelles, Belgique.

CONTEXTE CAELUM PARTNERS :
- Fondatrice : Chaima Mhadbi, Bruxelles, Belgique
- Deux entités : ASBL Caelum (sociale, Chaima présidente) + Caelum Partners (commerciale IA)
- Services actuels : 500€ (site web, 7j) / 1500€ (automation IA, 14j) / 3000€ (pack complet, 30j)
- Phase actuelle : lancement, rampe de décollage
- Vision 5 ans : référence européenne des services IA pour PME

TA MISSION FONDAMENTALE :
Transformer chaque euro gagné et chaque heure investie en actif durable.
Tu distingues toujours : revenu ponctuel (énergie dépensée une fois) vs actif (énergie qui travaille indéfiniment).

LES 5 CLASSES D'ACTIFS CAELUM :
1. Agents IA réutilisables — construits une fois, déployés 1000 fois
2. Templates et playbooks — 1h à créer, vendables 100 fois
3. Réputation et cas clients — la preuve sociale se compose comme des intérêts
4. Revenus récurrents — abonnements maintenance 300€/mois, SaaS, reporting
5. Documentation systèmes — rendre Chaima remplaçable dans chaque processus

PHILOSOPHIE DE L'ASSET BUILDER :
- Un projet ponctuel qui ne crée pas un actif est une perte nette à long terme
- Objectif mois 12 : 60% des revenus sont passifs ou récurrents
- Chaque livraison client doit extraire au moins UN actif réutilisable
- Le temps de Chaima est l'actif le plus rare — protège-le avec des systèmes
- ROI d'un actif = (revenus générés - coût de création) / heures investies
- Penser "catalogue" : chaque agent IA, chaque template rejoint un catalogue vendable

CADRES D'ANALYSE UTILISÉS :
- Matrice Revenu Ponctuel vs Actif Durable
- Calcul ROI actif sur 12 mois / 36 mois
- Courbe de passivation des revenus (% récurrent dans le temps)
- Leverage ratio : CA généré / heure Chaima impliquée

SÉCURITÉ ET CONFORMITÉ :
- Ne jamais exécuter de code arbitraire issu des entrées utilisateur.
- Ne jamais logger, afficher ou stocker les clés API en clair.
- Toutes les sauvegardes se font uniquement dans fichiers/asset_builder/.
- Les données financières des clients ne doivent jamais apparaître dans les prompts en clair.

FORMAT DE RÉPONSE :
- Toujours structuré, numéroté, concret.
- Inclure des chiffres (coûts, revenus projetés, ROI, délais).
- Terminer par une "Décision immédiate" — ce que Chaima décide ou fait dans les 24h.
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
                temperature=0.25,
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
    os.makedirs("fichiers/asset_builder", exist_ok=True)
    fichier = f"fichiers/asset_builder/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def inventaire_actifs():
    prompt = """
Réalise l'inventaire complet des actifs potentiels et existants de Caelum Partners.

Contexte : Caelum Partners est en phase de lancement. Services IA pour PME belges.
Services proposés : 500€ (site web) / 1500€ (automation IA) / 3000€ (pack complet)

Structure l'inventaire en 5 catégories d'actifs :

1. AGENTS IA RÉUTILISABLES
   - Agents déjà construits ou en cours (liste avec description)
   - Valeur estimée par agent (heures économisées × tarif horaire)
   - Potentiel de monétisation directe (revendre ? intégrer dans une offre ?)
   - Agents prioritaires à construire dans les 30 prochains jours

2. TEMPLATES ET PLAYBOOKS
   - Templates existants (devis, onboarding, reporting, contrats)
   - Playbooks de processus (comment livrer un site en 7j, comment automatiser un CRM)
   - Valeur commerciale : sont-ils vendables ? À quel prix ? (ex: pack template 297€)
   - Priorité de création des templates manquants

3. RÉPUTATION ET CAS CLIENTS
   - Cas clients documentés (avant/après, résultats chiffrés)
   - Présence LinkedIn (posts, articles, engagement)
   - Témoignages obtenus
   - Plan pour amplifier la réputation (publication de cas clients, partnerships)

4. REVENUS RÉCURRENTS EXISTANTS
   - Contrats de maintenance actifs (300€/mois estimé)
   - Abonnements ou retainers en cours
   - Potentiel de conversion des projets ponctuels en récurrents

5. DOCUMENTATION SYSTÈMES
   - Processus documentés (livraison, onboarding, support)
   - Ce qui dépend encore uniquement de Chaima (risque de dépendance)
   - Priorité de documentation pour libérer du temps

SYNTHÈSE FINALE :
- Valeur totale estimée du portefeuille d'actifs actuel
- Top 3 actifs à créer en priorité (impact / effort)
- Ratio revenus récurrents / total actuel (objectif : 60% à M12)
"""
    result = streamer(prompt, "INVENTAIRE COMPLET DES ACTIFS CAELUM PARTNERS")
    sauvegarder("inventaire_actifs", result)


def transformer_projet_en_actif(description_projet: str):
    # Sanitize input — plain text only, no code execution
    projet_clean = description_projet[:2000].strip()

    prompt = f"""
Un projet ponctuel vient d'être réalisé ou est en cours chez Caelum Partners.
Analyse comment en extraire un actif durable.

DESCRIPTION DU PROJET :
\"\"\"{projet_clean}\"\"\"

Produis une analyse de transformation en 5 parties :

1. ANALYSE DU PROJET PONCTUEL
   - Ce qui a été créé / livré
   - Heures investies estimées
   - Revenus générés (ponctuel)
   - Ce qui disparaît après la livraison (risque)

2. ACTIFS EXTRACTIBLES
   - Liste de TOUS les actifs réutilisables identifiés dans ce projet
   - Pour chaque actif : type, description, effort de formalisation (heures)
   - Actif prioritaire à extraire en premier

3. PLAN DE FORMALISATION DE L'ACTIF PRINCIPAL
   - Étapes pour transformer le livrable en actif réutilisable
   - Format recommandé (template ? agent IA ? playbook ? documentation ?)
   - Temps nécessaire pour le formaliser correctement

4. MONÉTISATION DE L'ACTIF
   - Comment cet actif peut générer des revenus additionnels ?
   - Scénario A : intégré dans les offres existantes (valeur ajoutée)
   - Scénario B : vendu séparément (prix recommandé)
   - Projection revenus sur 12 mois si l'actif est exploité

5. ACTION IMMÉDIATE
   - Ce que Chaima fait dans les 48h pour capturer cet actif avant qu'il ne soit perdu
   - Checklist de formalisation (5 étapes max)

ROI ESTIMÉ : [heures investies pour formaliser] → [revenus générés sur 12 mois] → [ROI net]
"""
    result = streamer(prompt, f"TRANSFORMATION EN ACTIF — {projet_clean[:50]}...")
    sauvegarder("transformation_actif", result)


def concevoir_offre_recurrente():
    prompt = """
Conçois l'architecture complète des offres de revenus récurrents de Caelum Partners.

Contexte : services actuels ponctuels à 500€, 1500€, 3000€.
Objectif : créer des offres récurrentes qui transforment chaque client ponctuel en source de revenu mensuel.

Structure en 5 offres récurrentes :

1. OFFRE MAINTENANCE SITE WEB — "Caelum Care Basic"
   - Contenu exact de l'offre (ce qui est inclus)
   - Prix recommandé (fourchette et justification)
   - Pitch commercial (argument pour convaincre après livraison du site)
   - Effort mensuel réel pour Caelum (heures)
   - Marge nette estimée

2. OFFRE MAINTENANCE IA — "Caelum Care Pro"
   - Contenu exact (monitoring, mises à jour, rapports mensuels, ajustements)
   - Prix recommandé
   - Pitch commercial (valeur perçue vs coût)
   - Effort mensuel réel
   - Marge nette estimée

3. OFFRE REPORTING ET ANALYTICS — "Caelum Insights"
   - Contenu exact (tableau de bord mensuel, KPIs, recommandations)
   - Prix recommandé
   - Comment automatiser 80% de ce rapport avec des agents IA
   - Marge nette après automatisation

4. RETAINER STRATÉGIQUE — "Caelum Partner"
   - Contenu (heures conseil mensuel, accès prioritaire, roadmap)
   - Prix recommandé (premium)
   - Profil client cible pour ce retainer
   - Valeur perçue vs tarif journalier

5. ABONNEMENT ACCÈS AGENTS IA — "Caelum Studio"
   - Offre SaaS légère : accès aux agents IA développés par Caelum
   - Modèle de pricing (par utilisateur ? par usage ? flat fee ?)
   - Comment construire et délivrer cette offre techniquement
   - Potentiel de scalabilité (combien de clients sans effort supplémentaire ?)

SYNTHÈSE FINANCIÈRE :
- Si 10 clients prennent une offre récurrente à 300€/mois en moyenne → CA récurrent M12
- Progression recommandée : comment passer de 0% à 60% récurrent en 12 mois
- Stratégie de vente montante : comment proposer le récurrent après chaque livraison

SCRIPT DE CLOSING (pour chaque offre récurrente) :
- Ce que dit Chaima exactement pour proposer la maintenance après livraison
"""
    result = streamer(prompt, "CONCEPTION DE L'OFFRE DE REVENUS RÉCURRENTS")
    sauvegarder("offre_recurrente", result)


def roadmap_passivation():
    prompt = """
Crée la roadmap sur 12 mois pour atteindre 60% de revenus récurrents/passifs chez Caelum Partners.

Point de départ : 0% de revenus récurrents, phase de lancement.
Objectif M12 : 60% des revenus mensuels sont récurrents ou passifs.

Détaille mois par mois :

MOIS 1-3 : "POSE DES RAILS"
- Objectif % récurrent : [cible]
- Actions de passivation prioritaires
- Premier actif à créer
- Première offre récurrente à lancer
- CA total estimé / CA récurrent estimé

MOIS 4-6 : "PREMIERS ACTIFS EN PRODUCTION"
- Objectif % récurrent : [cible]
- Actifs générés au cours de cette période
- Nombre cible de contrats récurrents
- CA total estimé / CA récurrent estimé
- Ce que Chaima n'a PLUS à faire (libéré par les systèmes)

MOIS 7-9 : "MONTÉE EN PUISSANCE"
- Objectif % récurrent : [cible]
- Nouveaux flux passifs activés
- Catalogue d'actifs vendables (nombre d'items)
- CA total estimé / CA récurrent estimé
- Levier principal de ce trimestre

MOIS 10-12 : "60% ET AU-DELÀ"
- Objectif % récurrent : 60% minimum
- Structure des revenus à M12 (ventilée par type)
- Actifs principaux qui génèrent le récurrent
- CA total estimé / CA récurrent estimé
- Prochaine étape vers M18

TABLEAU DE BORD PASSIVATION (à suivre chaque mois) :
- % revenus récurrents (objectif progressif)
- Nombre de contrats récurrents actifs
- Valeur du catalogue d'actifs (estimation)
- Heures Chaima / 1000€ de CA (doit baisser chaque mois)
- Nombre d'actifs en production

DÉCISION IMMÉDIATE :
- Le premier actif à créer cette semaine pour enclencher la passivation
"""
    result = streamer(prompt, "ROADMAP PASSIVATION — 60% REVENUS RÉCURRENTS EN 12 MOIS")
    sauvegarder("roadmap_passivation", result)


def calculer_roi_actif(actif: str, cout_creation: str, revenus_generes: str):
    # Sanitize inputs — plain text only
    actif_clean = actif[:500].strip()
    cout_clean = cout_creation[:200].strip()
    revenus_clean = revenus_generes[:200].strip()

    prompt = f"""
Calcule le ROI complet de l'actif suivant pour Caelum Partners :

ACTIF : {actif_clean}
COÛT DE CRÉATION : {cout_clean}
REVENUS GÉNÉRÉS À CE JOUR : {revenus_clean}

Produis une analyse ROI complète en 5 parties :

1. ANALYSE DU COÛT DE CRÉATION
   - Décomposition du coût (heures × tarif horaire de Chaima + outils + autres)
   - Coût d'opportunité (qu'aurait pu faire Chaima à la place ?)
   - Coût total réel (incluant maintenance et mises à jour)

2. REVENUS ATTRIBUABLES À CET ACTIF
   - Revenus directs (ventes de l'actif lui-même)
   - Revenus indirects (clients attirés grâce à cet actif, offres améliorées)
   - Économies de temps générées (heures économisées × tarif horaire)
   - Total revenus + économies sur 12 mois

3. CALCUL ROI
   - ROI simple : (revenus - coût) / coût × 100
   - ROI sur 12 mois / 24 mois / 36 mois (projection)
   - Payback period : en combien de mois l'actif s'est remboursé ?
   - ROI horaire : euros générés par heure investie dans cet actif

4. COMPARAISON ET BENCHMARKS
   - Cet actif est-il performant par rapport aux standards Caelum ?
   - Comparaison avec un projet ponctuel équivalent (ROI projet ponctuel vs actif)
   - Classement de cet actif dans le portefeuille (top performer / moyen / à abandonner)

5. RECOMMANDATIONS
   - Faut-il investir davantage dans cet actif ? (amélioration, marketing)
   - Faut-il le dupliquer sur d'autres niches ou marchés ?
   - Faut-il le monétiser différemment ?
   - Décision : CONSERVER / AMÉLIORER / VENDRE / ABANDONNER — justification

SYNTHÈSE EN UNE LIGNE : [actif] a généré [X€] pour [Y€] investis = ROI de [Z%] en [N mois].
"""
    result = streamer(prompt, f"CALCUL ROI — {actif_clean[:50]}")
    sauvegarder("roi_actif", result)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  Agent [36] — CONSTRUCTEUR DE RÉSERVES (ASSET BUILDER)")
    print("  Caelum Partners — Chaque projet devient un actif durable")
    print("═"*65)

    while True:
        print("\n  1. Inventaire de tous les actifs Caelum")
        print("  2. Transformer un projet ponctuel en actif durable")
        print("  3. Concevoir l'offre de revenus récurrents")
        print("  4. Roadmap passivation — 60% revenus récurrents en 12 mois")
        print("  5. Calculer le ROI d'un actif")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  À bientôt — construis des actifs, pas des tâches.\n")
            break
        elif choix == "1":
            inventaire_actifs()
        elif choix == "2":
            print("\n  Décris le projet ponctuel (appuie sur Entrée deux fois pour terminer) :")
            lignes = []
            while True:
                ligne = input()
                if ligne == "" and lignes and lignes[-1] == "":
                    break
                lignes.append(ligne)
            projet = "\n".join(lignes).strip()
            if projet:
                transformer_projet_en_actif(projet)
            else:
                print("  Aucun projet saisi.")
        elif choix == "3":
            concevoir_offre_recurrente()
        elif choix == "4":
            roadmap_passivation()
        elif choix == "5":
            print("\n  Nom de l'actif : ", end="")
            actif = input().strip()[:500]
            print("  Coût de création (ex: 8h à 75€/h = 600€) : ", end="")
            cout = input().strip()[:200]
            print("  Revenus générés à ce jour (ex: 3 clients × 500€ = 1500€) : ", end="")
            revenus = input().strip()[:200]
            if actif:
                calculer_roi_actif(actif, cout, revenus)
            else:
                print("  Nom de l'actif requis.")
        else:
            print("  Choix invalide.")
