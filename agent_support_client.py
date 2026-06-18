"""
AGENT SUPPORT CLIENT AUTONOME 24/7 — AgentClaude Solutions
Gère tickets, FAQ, onboarding, satisfaction et escalades.
Tout seul. Zéro interruption. Zéro jour de congé.

Usage : python agent_support_client.py
"""

import os
import sys
import json
from datetime import datetime
import google.generativeai as genai
from memoire import (
    ajouter_interaction,
    obtenir_contexte_client,
    charger_memoire,
    sauvegarder_memoire,
    incrementer_stat,
)

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] Variable GEMINI_API_KEY non définie. Exécutez : export GEMINI_API_KEY=votre_cle")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

# ─── Dossier de sauvegarde des tickets ────────────────────────
SUPPORT_DIR = os.path.join("fichiers", "support")
os.makedirs(SUPPORT_DIR, exist_ok=True)

ENTREPRISE_PROFIL = """
Nom : AgentClaude Solutions
Spécialité : Automatisation par agents IA (Claude, Gemini)
Services :
  - Agents autonomes sur mesure pour entreprises
  - Migration et modernisation de code legacy
  - Sécurité et audit IA
  - Formation équipes sur agents IA
  - Orchestrateurs autonomes clé en main
Valeurs : Réactivité, transparence, excellence technique, accompagnement humain
Support : 24h/24, 7j/7 par agents IA avec escalade humaine si nécessaire
"""


# ─── Utilitaires ──────────────────────────────────────────────

def creer_agent(instructions, temperature=0.5):
    return genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(
            temperature=temperature, max_output_tokens=3072
        ),
    )


def executer_stream(model, prompt, label):
    print(f"\n{'─' * 60}")
    print(f"  ► {label}")
    print(f"{'─' * 60}\n")
    reponse = ""
    try:
        stream = model.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        reponse = f"[Erreur agent : {e}]"
        print(reponse)
    print()
    return reponse


def sauvegarder_ticket(ref, contenu):
    """Sauvegarde un ticket dans fichiers/support/ avec horodatage."""
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"ticket_{ref}_{horodatage}.txt"
    chemin = os.path.join(SUPPORT_DIR, nom_fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"=== TICKET SUPPORT — {ref} ===\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(contenu)
    print(f"\n  ✅ Ticket sauvegardé → {chemin}")
    return chemin


def enregistrer_ticket_memoire(ref, question, reponse, urgence):
    """Enregistre le ticket dans la mémoire partagée."""
    m = charger_memoire()
    if "tickets" not in m:
        m["tickets"] = []
    m["tickets"].append({
        "ref": ref,
        "date": datetime.now().isoformat(),
        "question": question[:200],
        "urgence": urgence,
        "resolu": True,
    })
    sauvegarder_memoire(m)
    ajouter_interaction(ref, "ticket_support", reponse[:200])


# ─── AGENT 1 : Répondre aux tickets ───────────────────────────

def agent_repondre_ticket(question, historique_client=""):
    """
    Classifie l'urgence, identifie le sujet, génère une réponse professionnelle
    et empathique, propose une solution et escalade si nécessaire.
    """
    incrementer_stat("agent_repondre_ticket")

    agent = creer_agent(f"""Tu es un agent support client expert pour AgentClaude Solutions,
spécialisé en agents IA et automatisation.

Profil entreprise :
{ENTREPRISE_PROFIL}

Ta mission pour chaque ticket :
1. CLASSIFICATION D'URGENCE : détermine le niveau parmi :
   - CRITIQUE : panne totale en production, perte de données, faille sécurité
   - HAUTE : dysfonctionnement majeur impactant le métier
   - NORMALE : problème fonctionnel avec contournement possible
   - FAIBLE : question, amélioration, curiosité

2. IDENTIFICATION DU SUJET : catégorise parmi :
   - Technique (bug, intégration, API, performance)
   - Facturation (devis, facture, abonnement)
   - Onboarding (mise en place, configuration, formation)
   - Fonctionnel (usage, fonctionnalité, limite)
   - Sécurité (accès, données, conformité)
   - Autre

3. RÉPONSE PROFESSIONNELLE ET EMPATHIQUE :
   - Accuse réception avec empathie selon l'urgence
   - Reformule le problème pour montrer la compréhension
   - Propose une solution concrète et actionnable
   - Indique le délai de résolution attendu

4. SOLUTION PROPOSÉE : étapes précises et claires

5. ESCALADE : précise si le ticket doit être transmis à un humain.
   Escalader si : CRITIQUE, problème juridique, client très mécontent, cas hors compétence IA

Format de réponse :
📋 URGENCE : [niveau]
🏷️ SUJET : [catégorie]
---
[Réponse complète au client]
---
⚡ ESCALADE NÉCESSAIRE : [OUI/NON] — [raison si OUI]""", temperature=0.4)

    contexte = f"\nHistorique client : {historique_client}" if historique_client else ""
    prompt = f"Ticket reçu :\n{question}{contexte}"

    reponse = executer_stream(agent, prompt, "Traitement Ticket Support")

    # Extraction du niveau d'urgence pour la sauvegarde
    urgence = "NORMALE"
    for niveau in ["CRITIQUE", "HAUTE", "NORMALE", "FAIBLE"]:
        if niveau in reponse.upper():
            urgence = niveau
            break

    # Génération de la référence ticket
    ref = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    contenu_ticket = f"Question client :\n{question}\n\nHistorique :\n{historique_client}\n\nRéponse agent :\n{reponse}"
    sauvegarder_ticket(ref, contenu_ticket)
    enregistrer_ticket_memoire(ref, question, reponse, urgence)

    return reponse


# ─── AGENT 2 : Générer une FAQ ────────────────────────────────

def agent_generer_faq(services):
    """
    Génère un document FAQ complet pour les services d'agents IA :
    20+ questions couvrant tarifs, délais, technique, sécurité, support, onboarding.
    """
    incrementer_stat("agent_generer_faq")

    agent = creer_agent(f"""Tu es un expert en documentation client et communication B2B
pour des solutions d'agents IA.

Profil entreprise :
{ENTREPRISE_PROFIL}

Tu dois générer une FAQ exhaustive, professionnelle et rassurante.
La FAQ doit :
- Couvrir au minimum 20 questions-réponses
- Être organisée en sections thématiques claires
- Utiliser un ton professionnel mais accessible
- Anticiper les objections et craintes des acheteurs B2B
- Inclure des exemples concrets et des chiffres réalistes

Sections obligatoires :
1. 💰 Tarifs et facturation (4-5 Q&A)
2. ⏱️ Délais et livraison (3-4 Q&A)
3. 🔧 Questions techniques (4-5 Q&A)
4. 🔒 Sécurité et conformité (3-4 Q&A)
5. 🎓 Onboarding et formation (3-4 Q&A)
6. 🛟 Support et maintenance (3-4 Q&A)

Format pour chaque Q&A :
**Q : [question précise et réaliste]**
R : [réponse complète, rassurante, avec détails pratiques]""", temperature=0.6)

    reponse = executer_stream(agent,
        f"Génère la FAQ complète pour ces services : {services}\n\nEntreprise : AgentClaude Solutions",
        "Génération FAQ Services IA"
    )

    # Sauvegarde du document FAQ
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = os.path.join(SUPPORT_DIR, f"faq_services_{horodatage}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"FAQ — AgentClaude Solutions\n")
        f.write(f"Générée le {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write(f"Services couverts : {services}\n")
        f.write("=" * 60 + "\n\n")
        f.write(reponse)
    print(f"\n  ✅ FAQ sauvegardée → {chemin}")

    return reponse


# ─── AGENT 3 : Onboarding client ──────────────────────────────

def agent_onboarding_client(nom_client, services_achetes):
    """
    Génère un kit d'onboarding personnalisé :
    email de bienvenue, guide de mise en place, checklist semaine 1,
    points de contact, ressources de formation.
    """
    incrementer_stat("agent_onboarding_client")

    contexte = obtenir_contexte_client(nom_client)

    agent = creer_agent(f"""Tu es un Customer Success Manager expert en onboarding
de solutions IA pour entreprises.

Profil entreprise :
{ENTREPRISE_PROFIL}

Tu dois créer un kit d'onboarding complet, chaleureux et opérationnel.
Le kit doit inclure obligatoirement :

1. 📧 EMAIL DE BIENVENUE PERSONNALISÉ
   - Ton chaleureux et professionnel
   - Rappel des services achetés et des bénéfices attendus
   - Prochaines étapes claires

2. 🚀 GUIDE DE MISE EN PLACE ÉTAPE PAR ÉTAPE
   - Étapes numérotées avec durée estimée
   - Prérequis techniques
   - Actions concrètes pour chaque étape
   - Points de validation

3. ✅ CHECKLIST PREMIÈRE SEMAINE
   - J+1 : actions immédiates
   - J+3 : premières vérifications
   - J+7 : bilan de démarrage
   - Critères de succès mesurables

4. 📞 POINTS DE CONTACT
   - Support technique (avec horaires et SLA)
   - Customer Success Manager dédié
   - Documentation et ressources en ligne
   - Canal d'urgence

5. 📚 RESSOURCES DE FORMATION
   - Tutoriels recommandés selon les services
   - Webinaires disponibles
   - Documentation API/technique
   - Communauté utilisateurs

Personnalise chaque section pour le client et ses services spécifiques.""", temperature=0.5)

    reponse = executer_stream(agent,
        f"Client : {nom_client}\nServices achetés : {services_achetes}\nContexte : {contexte}",
        f"Kit Onboarding — {nom_client}"
    )

    # Sauvegarde du kit
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"onboarding_{nom_client.replace(' ', '_')}_{horodatage}.txt"
    chemin = os.path.join(SUPPORT_DIR, nom_fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"KIT ONBOARDING — {nom_client}\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write(f"Services : {services_achetes}\n")
        f.write("=" * 60 + "\n\n")
        f.write(reponse)
    print(f"\n  ✅ Kit onboarding sauvegardé → {chemin}")

    ajouter_interaction(nom_client, "onboarding_kit", reponse[:300])
    return reponse


# ─── AGENT 4 : Satisfaction client ────────────────────────────

def agent_satisfaction(retour_client):
    """
    Analyse le feedback client (NPS/verbatim), extrait le sentiment et
    les thèmes clés, génère un plan d'action et rédige une réponse personnalisée.
    """
    incrementer_stat("agent_satisfaction")

    agent = creer_agent(f"""Tu es un expert en analyse de satisfaction client et
expérience utilisateur pour des solutions IA B2B.

Profil entreprise :
{ENTREPRISE_PROFIL}

Analyse le retour client et produis un rapport structuré :

1. 📊 ANALYSE DU SENTIMENT
   - Score de sentiment : Très positif / Positif / Neutre / Négatif / Très négatif
   - Intensité émotionnelle (1-10)
   - Score NPS estimé si feedback quantitatif présent (-100 à +100)
   - Probabilité de churn (faible / modérée / élevée)

2. 🔍 THÈMES CLÉS IDENTIFIÉS
   - Liste les 3-5 thèmes principaux (positifs et négatifs)
   - Pour chaque thème : impact estimé sur la satisfaction globale

3. 💡 POINTS DE FRICTION DÉTECTÉS
   - Problèmes explicites mentionnés
   - Frustrations implicites (lire entre les lignes)
   - Comparaisons avec concurrents si mentionnées

4. 🎯 PLAN D'ACTION POUR AMÉLIORER LA SATISFACTION
   - Actions immédiates (sous 24h)
   - Actions court terme (sous 1 semaine)
   - Actions structurelles (sous 1 mois)
   - Responsable suggéré pour chaque action

5. ✉️ RÉPONSE PERSONNALISÉE AU CLIENT
   - Ton adapté au sentiment (empathique si négatif, enthousiaste si positif)
   - Accusé réception avec reformulation du feedback
   - Actions concrètes promises avec délais
   - Invitation à un échange si nécessaire
   - Signature professionnelle""", temperature=0.4)

    reponse = executer_stream(agent,
        f"Retour client à analyser :\n{retour_client}",
        "Analyse Satisfaction Client"
    )

    # Sauvegarde
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = os.path.join(SUPPORT_DIR, f"satisfaction_{horodatage}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"ANALYSE SATISFACTION\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Retour client :\n{retour_client}\n\n")
        f.write("Analyse :\n")
        f.write(reponse)
    print(f"\n  ✅ Analyse sauvegardée → {chemin}")

    return reponse


# ─── AGENT 5 : Escalade complexe ──────────────────────────────

def agent_escalade(ticket, tentatives_precedentes):
    """
    Gère les problèmes complexes non résolus : analyse des causes racines,
    proposition de compensation si justifiée, modèle d'email d'escalade direction.
    """
    incrementer_stat("agent_escalade")

    agent = creer_agent(f"""Tu es un Responsable Support Senior et gestionnaire de crise
pour AgentClaude Solutions.

Profil entreprise :
{ENTREPRISE_PROFIL}

Tu gères les escalades complexes avec professionnalisme et résolution déterminée.
Produis un dossier d'escalade complet :

1. 🔬 ANALYSE DES CAUSES RACINES (Root Cause Analysis)
   - Cause principale identifiée
   - Causes contributives
   - Timeline des événements
   - Impact réel sur le client (technique, business, financier)

2. 📋 SYNTHÈSE DES TENTATIVES PRÉCÉDENTES
   - Ce qui a été essayé et pourquoi ça n'a pas fonctionné
   - Leçons apprises
   - Gap entre attentes client et réalité

3. 💰 PROPOSITION DE COMPENSATION (si justifiée)
   Critères : ancienneté client, gravité du problème, faute de notre côté
   Options possibles :
   - Crédit de service (montant suggéré en % de la valeur contrat)
   - Extension gratuite de services
   - Intervention prioritaire dédiée
   - Remboursement partiel
   - Si compensation non justifiée : expliquer pourquoi clairement

4. 🛠️ PLAN DE RÉSOLUTION DÉFINITIVE
   - Actions techniques précises avec responsables
   - Jalons et délais de résolution
   - Critères de validation par le client
   - Mesures préventives pour éviter la récurrence

5. 📨 EMAIL D'ESCALADE DIRECTION
   - À envoyer par le Directeur Technique ou CEO
   - Ton : grave, personnel, engagé
   - Reconnaissance sans excuses excessives
   - Engagements concrets et mesurables
   - Proposition de call de suivi dans les 24h""", temperature=0.3)

    prompt = f"""Ticket escaladé :
{ticket}

Tentatives de résolution précédentes :
{tentatives_precedentes}"""

    reponse = executer_stream(agent, prompt, "Gestion Escalade Complexe")

    # Sauvegarde avec haute priorité
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = os.path.join(SUPPORT_DIR, f"ESCALADE_{horodatage}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"!!! DOSSIER ESCALADE PRIORITAIRE !!!\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Ticket :\n{ticket}\n\n")
        f.write(f"Tentatives précédentes :\n{tentatives_precedentes}\n\n")
        f.write("Analyse et plan de résolution :\n")
        f.write(reponse)
    print(f"\n  🚨 Dossier escalade sauvegardé → {chemin}")

    return reponse


# ─── MENU PRINCIPAL ───────────────────────────────────────────

def afficher_stats_tickets():
    """Affiche les statistiques des tickets depuis la mémoire."""
    m = charger_memoire()
    tickets = m.get("tickets", [])
    if not tickets:
        print("  Aucun ticket enregistré.")
        return
    urgences = {}
    for t in tickets:
        u = t.get("urgence", "INCONNUE")
        urgences[u] = urgences.get(u, 0) + 1
    print(f"\n  Total tickets traités : {len(tickets)}")
    print("  Répartition par urgence :")
    for u, n in sorted(urgences.items()):
        print(f"    {u:<12} : {n}")


def menu():
    print("\n" + "═" * 60)
    print("  AGENT SUPPORT CLIENT 24/7 — AgentClaude Solutions")
    print("═" * 60)

    while True:
        print("\n  1. Répondre à un ticket client")
        print("  2. Générer une FAQ services IA")
        print("  3. Créer un kit d'onboarding client")
        print("  4. Analyser la satisfaction client")
        print("  5. Gérer une escalade complexe")
        print("  6. Voir les statistiques tickets")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  Au revoir. L'agent support reste actif en arrière-plan.\n")
            break

        elif choix == "1":
            print("\n  Entrez la question/problème du client (terminez par une ligne vide) :")
            lignes = []
            while True:
                ligne = input()
                if ligne == "":
                    break
                lignes.append(ligne)
            question = "\n".join(lignes)
            if not question.strip():
                print("  Aucune question saisie.")
                continue
            historique = input("  Nom du client (laisser vide si inconnu) → ").strip()
            historique_ctx = obtenir_contexte_client(historique) if historique else ""
            agent_repondre_ticket(question, historique_ctx)

        elif choix == "2":
            services = input("  Services à couvrir dans la FAQ → ").strip()
            if not services:
                services = "agents IA autonomes, automatisation, migration code, formation"
            agent_generer_faq(services)

        elif choix == "3":
            nom = input("  Nom du client → ").strip()
            if not nom:
                print("  Nom requis.")
                continue
            services = input("  Services achetés → ").strip()
            if not services:
                print("  Services requis.")
                continue
            agent_onboarding_client(nom, services)

        elif choix == "4":
            print("\n  Collez le retour client (NPS, verbatim, email...) :")
            print("  (Terminez avec une ligne vide)")
            lignes = []
            while True:
                ligne = input()
                if ligne == "":
                    break
                lignes.append(ligne)
            retour = "\n".join(lignes)
            if not retour.strip():
                print("  Aucun retour saisi.")
                continue
            agent_satisfaction(retour)

        elif choix == "5":
            print("\n  Décrivez le ticket escaladé :")
            print("  (Terminez avec une ligne vide)")
            lignes = []
            while True:
                ligne = input()
                if ligne == "":
                    break
                lignes.append(ligne)
            ticket = "\n".join(lignes)
            if not ticket.strip():
                print("  Ticket vide.")
                continue
            print("\n  Décrivez les tentatives de résolution précédentes :")
            print("  (Terminez avec une ligne vide)")
            lignes2 = []
            while True:
                ligne = input()
                if ligne == "":
                    break
                lignes2.append(ligne)
            tentatives = "\n".join(lignes2) if lignes2 else "Aucune tentative documentée."
            agent_escalade(ticket, tentatives)

        elif choix == "6":
            afficher_stats_tickets()

        else:
            print("  Choix invalide.")


if __name__ == "__main__":
    menu()
