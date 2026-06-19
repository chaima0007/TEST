"""
AGENT : AUDITEUR FINANCIER & STATUTAIRE (BELGIQUE)
Expert en optimisation de revenus, cumul chômage/indépendant, rentabilité opérationnelle.
ONEM · INASTI · Seuils revenus · Optimisation net après charges

Usage : python agent_auditeur_financier.py
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

IDENTITE = """# AGENT : AUDITEUR FINANCIER & STATUTAIRE (BELGIQUE)

## 1. IDENTITÉ ET RÔLE
- Nom : Auditeur Financier & Statutaire (Belgique)
- Rôle : Expert en optimisation de revenus, gestion du cumul chômage/indépendant et rentabilité opérationnelle.
- Domaine d'expertise : Législation sociale belge (ONEM/INASTI), calcul de seuils de revenus, optimisation fiscale, stratégie de prospection.

## 2. DIRECTIVES DE COMPORTEMENT
- Ton : Pragmatique, factuel, orienté résultat.
- Style : Analyse chiffrée, tableaux de simulation, évaluation rigoureuse des risques.
- Contraintes :
  1. Chaque stratégie doit être étayée par une simulation financière (Revenus - Charges - Cotisations).
  2. Alerte prioritaire sur le maintien des droits ONEM.
  3. Chaque conseil doit viser le "net après impôts et cotisations".

## 3. PROTOCOLE DE CONNAISSANCE
- Référence : Code de la sécurité sociale belge, règles ONEM en vigueur 2024-2025, barèmes INASTI (cotisations sociales trimestrielles indépendant complémentaire : 20,5% sur revenus nets).
- Règles ONEM clés :
  * Article 48 AR du 25/11/1991 : cumul chômage + activité indépendante AUTORISÉE si déclarée
  * Formulaire C1 / C2 : déclaration obligatoire de chaque jour d'activité indépendante
  * Seuil de tolérance ONEM (activité accessoire antérieure) : revenus plafonnés selon situation familiale
  * Revenus bruts trimestriels indépendant complémentaire (2024) :
    - Cohabitant avec charge de famille : ~6 500€ brut/trimestre max sans perte allocations
    - Isolé : ~5 200€ brut/trimestre max
    - Cohabitant sans charge : ~4 500€ brut/trimestre max
  * Au-delà des seuils : suspension totale des allocations pour la période concernée
  * Régularisation possible en fin d'année — risque de remboursement
- INASTI cotisations indépendant complémentaire 2024 :
  * 20,5% sur revenus nets de l'activité
  * Minimum trimestriel si revenus nets > 1 568,17€/trimestre : cotisation minimale 79,07€/trim
  * Régularisation sur revenus réels après déclaration fiscale annuelle
- Gestion du risque : En cas d'incertitude fiscale, l'agent signale le besoin d'une validation comptable externe.

## 3bis. ORGANISME DE PAIEMENT : CSC (Confédération des Syndicats Chrétiens)
Chaima est affiliée à la CSC pour ses allocations de chômage.
Procédures CSC spécifiques à connaître :
  * Déclaration activité indépendante complémentaire : via le formulaire C1 remis à la CSC
  * La CSC transmet ensuite à l'ONEM — c'est la CSC qui gère le dossier, pas l'ONEM directement
  * Contact CSC Bruxelles : Rue de la Loi 121, 1040 Bruxelles | www.lacsc.be
  * MyCSC (portail en ligne) : déclarations et suivi dossier chômage en ligne
  * Délai de traitement CSC : prévoir 2-4 semaines pour valider une nouvelle situation
  * AVANT de signer le premier contrat Caelum : contacter la CSC pour déclarer l'activité
  * Document à demander à la CSC : "autorisation de cumul activité indépendante"
  * Si activité existait AVANT le chômage (ex: ASBL) : la déclarer comme activité antérieure
  * Fréquence de déclaration : mensuelle via C1 électronique ou papier selon ton dossier
  * En cas de doute : appeler le 0800 13 900 (numéro gratuit CSC) ou passer en agence

## 4. STRUCTURE DE SORTIE OBLIGATOIRE
Tes réponses doivent impérativement suivre cette structure :
1. RÉSUMÉ : Synthèse immédiate de la rentabilité et de la conformité.
2. SIMULATION CHIFFRÉE : tableau Revenus / Cotisations / Impact Chômage / Net Final
3. VÉRIFICATION LÉGALE : Analyse des risques (Seuils, déclarations, conformité ONEM/INASTI)
4. PLAN D'ACTION PROSPECT : Étapes concrètes pour atteindre les revenus visés sans risque.

## 5. CONTEXTE CAELUM PARTNERS
- Fondatrice : Chaima Mhadbi, Bruxelles
- Organisme de paiement chômage : CSC (Confédération des Syndicats Chrétiens)
- Situation ASBL : Présidente d'une ASBL en parallèle (activité à déclarer à la CSC comme activité bénévole ou antérieure)
- Services Caelum : Site web 500€ / Automation IA 1500€ / Pack 3000€
- Phase : lancement, 0 clients actuellement
- Objectif : maximiser le revenu NET total (allocations CSC/ONEM + revenus Caelum) tout en restant conforme
- PRIORITÉ ABSOLUE : contacter la CSC AVANT de signer le premier contrat"""

DIRECTIVE_SIMULATION = """Agis en tant qu'Auditeur Financier & Statutaire belge.
Effectue une simulation complète selon la structure obligatoire :
1. Impact réel sur les allocations chômage ONEM si signature de X contrats à Y euros par mois.
2. Identification du seuil de revenu optimal (maximiser le gain total activité + chômage).
3. Liste des 3 points critiques de vigilance pour rester en règle avec ONEM et INASTI.
4. Méthode de prospection ciblée pour atteindre ce seuil de rentabilité optimale."""


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
                temperature=0.1,
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
    os.makedirs("fichiers/audit_financier", exist_ok=True)
    fichier = f"fichiers/audit_financier/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def simulation_chomage_vs_caelum():
    """Simulation complète cumul ONEM + revenus Caelum Partners."""
    print("\n  ── INFORMATIONS POUR LA SIMULATION ──")
    print("  (Appuie Entrée pour utiliser la valeur par défaut)")

    allocation = input("\n  Ton allocation chômage mensuelle actuelle (€) [laisser vide si inconnue] → ").strip()
    situation = input("  Situation familiale [1=chef de famille, 2=isolé, 3=cohabitant] → ").strip() or "2"
    contrats = input("  Nombre de contrats Caelum visés par mois → ").strip() or "1"
    prix_moyen = input("  Prix moyen par contrat (€) [ex: 500, 1500 ou 3000] → ").strip() or "500"

    situation_labels = {"1": "chef de famille (avec charge)", "2": "isolé", "3": "cohabitant sans charge"}
    sit_label = situation_labels.get(situation, "isolé")

    prompt = f"""{DIRECTIVE_SIMULATION}

DONNÉES DE LA SIMULATION :
- Allocation chômage mensuelle : {allocation or "inconnue (utilise une estimation moyenne belge de 1 200€/mois)"}
- Situation familiale : {sit_label}
- Contrats Caelum Partners visés par mois : {contrats} contrat(s)
- Prix moyen par contrat : {prix_moyen}€
- Revenus Caelum mensuels bruts estimés : {int(contrats or 1) * int(prix_moyen or 500)}€/mois

EFFECTUE :
1. Simulation mois par mois sur 3 scénarios : 0 client / {contrats} client(s) / 2x{contrats} clients
2. Pour chaque scénario : revenus bruts, cotisations INASTI (20,5%), impact ONEM, revenu NET total
3. Identification du SEUIL OPTIMAL (point où revenus Caelum compensent la perte ONEM)
4. Les déclarations obligatoires à faire (C1, INASTI, BCE)
5. Recommandation : quel contrat signer EN PREMIER pour maximiser le net ?"""

    r = streamer(prompt, "SIMULATION COMPLÈTE — ONEM + Caelum Partners")
    sauvegarder("simulation_chomage_caelum", r)


def seuil_optimal():
    """Calcule le seuil de revenu qui maximise le revenu total net."""
    r = streamer(
        """Calcule le seuil de revenu optimal pour Caelum Partners en Belgique.
Objectif : trouver le point exact où les revenus Caelum + allocations ONEM sont maximisés.

Pour chaque situation familiale (chef de famille / isolé / cohabitant) :
1. Seuil trimestriel ONEM 2024 (revenus bruts max sans perte)
2. Cotisations INASTI à payer sur ces revenus
3. Revenu NET de Caelum après INASTI
4. Total net = allocations ONEM + net Caelum à ce seuil optimal
5. Ce qui se passe au-delà du seuil (perte d'allocations — vaut-il mieux continuer ?)

FORMAT :
Tableau comparatif par situation familiale + recommandation stratégique.
Inclure : à partir de quel CA mensuel Caelum vaut-il mieux renoncer aux allocations ?""",
        "SEUIL OPTIMAL — Maximiser revenus ONEM + Caelum"
    )
    sauvegarder("seuil_optimal", r)


def points_vigilance_onem():
    """Les points critiques pour rester en conformité ONEM."""
    r = streamer(
        """Liste exhaustive des obligations légales pour cumuler chômage ONEM et activité indépendante Caelum Partners en Belgique.

POUR CHAQUE OBLIGATION :
- Ce qui est requis (document, formulaire, délai)
- La conséquence si non respecté (amende, remboursement, exclusion)
- Comment le faire concrètement

COUVRIR :
1. L'autorisation préalable ONEM (T47 / activité accessoire antérieure)
2. La déclaration quotidienne ou mensuelle (formulaire C1/C2)
3. La déclaration à l'INASTI (inscription indépendant complémentaire)
4. Le plafond trimestriel de revenus et comment le calculer
5. La déclaration fiscale annuelle IPP (revenus divers / revenus professionnels ?)
6. Ce qu'il faut faire si on dépasse accidentellement le seuil
7. Les contrôles possibles de l'ONEM et comment se protéger

FORMAT : Checklist avec cases à cocher, délais et organismes de contact.""",
        "POINTS DE VIGILANCE LÉGALE — ONEM + Indépendant"
    )
    sauvegarder("vigilance_onem", r)


def strategie_prospection_seuil():
    """Stratégie de prospection pour atteindre le seuil optimal sans le dépasser."""
    r = streamer(
        """Caelum Partners doit atteindre un seuil de revenus optimal (max sans perdre les allocations).
Concrètement : environ 1 500-2 000€ nets/mois de Caelum sans déclencher la perte ONEM.

CRÉE UNE STRATÉGIE DE PROSPECTION CIBLÉE :

OBJECTIF MOIS 1 : 1 contrat site web à 500€
OBJECTIF MOIS 2 : 1 contrat automation à 1 500€
OBJECTIF MOIS 3 : niveau optimal — 2 000-2 500€ bruts/mois

Pour chaque mois :
1. Nombre de prospects à contacter (avec taux conversion réaliste B2B belge : 3-5%)
2. Canal prioritaire (LinkedIn, réseau, partenariats)
3. Message d'accroche adapté à la situation Caelum
4. Action quotidienne en 30 minutes pour tenir l'objectif
5. Signal d'alarme si on risque de dépasser le seuil ONEM ce trimestre

FORMAT : Plan semaine par semaine avec actions quotidiennes et alertes ONEM intégrées.""",
        "PROSPECTION CIBLÉE — Atteindre le seuil optimal ONEM"
    )
    sauvegarder("prospection_seuil", r)


def simulation_personnalisee():
    """Simulation sur mesure avec les chiffres réels de Chaima."""
    print("\n  ── SIMULATION PERSONNALISÉE ──")
    print("  Décris ta situation exacte et je calcule tout.")
    situation = input("\n  Décris ta situation (allocations, revenus actuels, objectifs) → ").strip()
    if not situation:
        print("  Annulé.")
        return
    r = streamer(
        f"""{DIRECTIVE_SIMULATION}

SITUATION PERSONNALISÉE À ANALYSER :
{situation}

EFFECTUE UNE SIMULATION COMPLÈTE avec :
1. Tableau chiffré selon la structure obligatoire
2. Seuil optimal identifié
3. 3 points de vigilance prioritaires
4. Plan d'action prospection pour 30 jours""",
        "SIMULATION PERSONNALISÉE"
    )
    sauvegarder("simulation_personnalisee", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AUDITEUR FINANCIER & STATUTAIRE — Belgique")
    print("  ONEM · INASTI · Optimisation revenus Caelum Partners")
    print("  Maximiser le net après impôts et cotisations")
    print("═"*65)

    while True:
        print("\n  1. Simulation cumul chômage ONEM + revenus Caelum")
        print("  2. Calculer le seuil optimal — maximiser total net")
        print("  3. Points de vigilance ONEM — rester en conformité")
        print("  4. Stratégie prospection ciblée pour atteindre le seuil")
        print("  5. Simulation personnalisée — ma situation exacte")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            simulation_chomage_vs_caelum()
        elif choix == "2":
            seuil_optimal()
        elif choix == "3":
            points_vigilance_onem()
        elif choix == "4":
            strategie_prospection_seuil()
        elif choix == "5":
            simulation_personnalisee()
        else:
            print("  Choix invalide.")
