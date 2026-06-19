"""
GARDIEN DU PLAYBOOK — Mémoire institutionnelle de Caelum Partners
Décisions loggées · Templates réutilisables · Leçons apprises · Jamais résoudre deux fois le même problème

Usage : python agent_gardien_playbook.py
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

IDENTITE = """# GARDIEN DU PLAYBOOK — CAELUM PARTNERS

## IDENTITÉ ET RÔLE
Tu es le Gardien du Playbook de Caelum Partners.
Ta mission : maintenir et enrichir la mémoire institutionnelle de l'entreprise.
Chaque décision validée, chaque template réussi, chaque leçon apprise doit être
encodée, structurée et rendue immédiatement accessible pour les situations futures.
Principe fondamental : Chaima ne doit JAMAIS résoudre deux fois le même problème.

## THÉORIE DE LA GESTION DU SAVOIR INSTITUTIONNEL

### LE PROBLÈME DE LA CONNAISSANCE IMPLICITE
La majorité du savoir dans une entreprise est TACITE (implicite dans la tête du fondateur).
Problème : si Chaima est absente, malade, ou si l'entreprise grandit, cette connaissance est perdue.
Solution : transformer le savoir tacite en savoir EXPLICITE (documenté, structuré, transmissible).

### TYPES DE CONNAISSANCE À CAPTURER
1. DÉCISIONS : "J'ai décidé X parce que Y, et le résultat a été Z"
2. TEMPLATES : "Pour faire X, voici le modèle qui fonctionne"
3. PROCESSUS : "Pour accomplir X, suivre ces étapes dans cet ordre"
4. LEÇONS : "Ce qui ne fonctionne pas et pourquoi"
5. CONTACTS : "Pour avoir X, contacter Y (qui, comment, quand)"

### PRINCIPE ANTI-RÉPÉTITION
Chaque problème résolu coûte du temps.
Résoudre le même problème deux fois = gaspillage inacceptable.
Le Playbook est le système qui garantit que chaque solution n'est construite qu'une fois,
puis réutilisée à l'infini avec des adaptations mineures.

### STRUCTURE DU PLAYBOOK CAELUM
LIVRE 1 — COMMERCIAL : prospection, qualification, closing, contrats, facturation
LIVRE 2 — LIVRAISON : processus par type de service (site web, automation, pack)
LIVRE 3 — CLIENT : onboarding, suivi, gestion des insatisfactions, renouvellement
LIVRE 4 — FINANCIER : conditions de paiement, relances, gestion TVA, INASTI
LIVRE 5 — LÉGAL : contrats types, RGPD, conditions générales, gestion des litiges
LIVRE 6 — OPÉRATIONNEL : workflows agents IA, checklist quotidienne, procédures d'urgence
LIVRE 7 — STRATÉGIQUE : décisions majeures loggées avec contexte et résultat

### VERSION CONTROL DES DÉCISIONS
Chaque décision a une version (v1.0, v1.1, v2.0) et une date.
Les révisions sont documentées : "v1.0 → v1.1 parce que X a changé."
Jamais d'écrasement sans traçabilité.

## FORMAT DE SORTIE OBLIGATOIRE
1. ENTRÉE PLAYBOOK : décision ou template formaté pour la base de données
2. RECHERCHE PLAYBOOK : résultats pertinents avec niveau de similarité
3. TEMPLATE EXTRAIT : modèle réutilisable avec variables à personnaliser
4. PLAYBOOK COMPLET : document structuré et paginé
5. PATTERNS DÉTECTÉS : tendances dans les décisions passées"""


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
    os.makedirs("fichiers/playbook", exist_ok=True)
    fichier = f"fichiers/playbook/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def sauvegarder_decision_json(decision: str, contexte: str, resultat: str):
    """Sauvegarde la décision dans un fichier JSON structuré."""
    os.makedirs("fichiers/playbook", exist_ok=True)
    log_file = "fichiers/playbook/decisions_log.json"
    entree = {
        "id": f"D{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "date": datetime.now().isoformat(),
        "decision": decision,
        "contexte": contexte,
        "resultat": resultat,
        "version": "1.0"
    }
    decisions = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                decisions = json.load(f)
        except Exception:
            decisions = []
    decisions.append(entree)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(decisions, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Décision loggée → {log_file} (ID: {entree['id']})")


def enregistrer_decision():
    print("\n  ENREGISTREMENT D'UNE DÉCISION DANS LE PLAYBOOK")
    decision = input("  Quelle décision as-tu prise ? → ").strip()
    if not decision:
        return
    contexte = input("  Dans quel contexte ? (problème rencontré) → ").strip()
    resultat = input("  Quel a été le résultat ? (ou 'en cours') → ").strip()

    sauvegarder_decision_json(decision, contexte, resultat)

    r = streamer(
        f"""Formate cette décision pour le Playbook de Caelum Partners.

DÉCISION : {decision}
CONTEXTE : {contexte}
RÉSULTAT : {resultat}

FORMATER EN ENTRÉE DE PLAYBOOK :

1. TITRE DE L'ENTRÉE : [verbe d'action] + [contexte] (ex: "Gérer un client qui refuse de payer")

2. SITUATION DÉCLENCHEUSE :
   - Symptômes qui indiquent que cette entrée du playbook s'applique
   - À utiliser quand : ...

3. DÉCISION PRISE ET JUSTIFICATION :
   - Décision : [décision]
   - Pourquoi : [raisonnement]
   - Alternatives considérées et pourquoi rejetées

4. ÉTAPES D'EXÉCUTION :
   - Étape 1 : ...
   - Étape 2 : ...
   [continuer]

5. RÉSULTAT OBTENU ET APPRENTISSAGES :
   - Résultat : [résultat]
   - Ce qui a bien fonctionné : ...
   - Ce qu'on ferait différemment : ...

6. TEMPLATE RÉUTILISABLE :
   [Extraire un modèle applicable à des situations similaires futures]

7. MOTS-CLÉS DE RECHERCHE :
   [5-10 mots-clés pour retrouver cette entrée facilement]""",
        "ENREGISTREMENT DÉCISION — Playbook Caelum Partners"
    )
    sauvegarder(f"decision_{decision[:25].replace(' ', '_')}", r)


def consulter_playbook():
    probleme = input("\n  Quel problème cherches-tu à résoudre ? → ").strip()
    if not probleme:
        return

    decisions_existantes = []
    log_file = "fichiers/playbook/decisions_log.json"
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                decisions_existantes = json.load(f)
        except Exception:
            pass

    contexte_decisions = json.dumps(decisions_existantes[-20:], ensure_ascii=False) if decisions_existantes else "Aucune décision encore loggée."

    r = streamer(
        f"""Recherche dans le Playbook de Caelum Partners pour ce problème : {probleme}

DÉCISIONS PRÉCÉDENTES DISPONIBLES :
{contexte_decisions}

RECHERCHE ET RECOMMANDATION :

1. DÉCISIONS SIMILAIRES TROUVÉES :
   (chercher dans les décisions disponibles celles qui sont proches du problème actuel)
   - Niveau de similarité : [haute / moyenne / faible]
   - Entrée du playbook applicable : [titre]

2. SI DÉCISION SIMILAIRE TROUVÉE :
   - Adapter la solution précédente au contexte actuel
   - Points de différence entre l'ancien et le nouveau contexte
   - Ajustements recommandés

3. SI AUCUNE DÉCISION SIMILAIRE :
   - Le playbook ne contient pas encore ce cas
   - Recommandation pour résoudre le problème depuis zéro
   - Suggestion d'entrée playbook à créer après résolution

4. TEMPLATE APPLICABLE (si disponible) :
   [modèle directement utilisable pour ce problème]

5. CONTACTS ET RESSOURCES UTILES (si applicable) :
   [qui contacter, quelle ressource utiliser]""",
        f"CONSULTATION PLAYBOOK — {probleme[:45]}"
    )
    sauvegarder(f"consultation_{probleme[:25].replace(' ', '_')}", r)


def extraire_template():
    description_succes = input("\n  Décris un succès récent dont tu veux extraire un template → ").strip()
    if not description_succes:
        return
    r = streamer(
        f"""Extrait un template réutilisable depuis ce succès de Caelum Partners.
Succès décrit : {description_succes}

ANALYSE DU SUCCÈS :
1. Qu'est-ce qui a exactement fonctionné ? (facteurs de succès)
2. Dans quelles conditions ce succès s'est-il produit ? (prérequis)
3. Qu'est-ce qui aurait pu faire échouer ce succès ? (risques évités)

EXTRACTION DU TEMPLATE :

TITRE DU TEMPLATE : [action + contexte]
APPLICABLE QUAND : [conditions d'utilisation]
PRÉREQUIS : [ce qui doit être en place avant d'utiliser ce template]

ÉTAPES DU TEMPLATE :
Étape 1 : [action précise] → Résultat attendu : [...]
Étape 2 : [action précise] → Résultat attendu : [...]
Étape 3 : [action précise] → Résultat attendu : [...]
[continuer selon le succès]

VARIABLES À PERSONNALISER :
- [Variable 1] = [ce que c'était dans ce cas] → remplacer par [...]
- [Variable 2] = [ce que c'était dans ce cas] → remplacer par [...]

RÉSULTAT ATTENDU SI TEMPLATE BIEN SUIVI : [résultat quantifié si possible]

AVERTISSEMENTS :
- Ne pas utiliser ce template si : [contre-indications]
- Adapter ce template si : [variantes contextuelles]

VERSION : 1.0 — Date : {datetime.now().strftime('%d/%m/%Y')}""",
        "EXTRACTION TEMPLATE — Playbook Caelum Partners"
    )
    sauvegarder(f"template_{description_succes[:25].replace(' ', '_')}", r)


def generer_playbook_complet():
    decisions_existantes = []
    log_file = "fichiers/playbook/decisions_log.json"
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                decisions_existantes = json.load(f)
        except Exception:
            pass

    nb_decisions = len(decisions_existantes)
    contexte = json.dumps(decisions_existantes, ensure_ascii=False)[:3000] if decisions_existantes else "Aucune décision encore loggée."

    r = streamer(
        f"""Génère le Playbook complet de Caelum Partners à partir des décisions enregistrées.
Nombre de décisions dans la base : {nb_decisions}
Décisions disponibles : {contexte}

PLAYBOOK CAELUM PARTNERS — ÉDITION {datetime.now().strftime('%B %Y').upper()}

═══════════════════════════════════════════════════════════════
LIVRE 1 — COMMERCIAL
═══════════════════════════════════════════════════════════════
1.1 Processus de prospection (étapes, scripts, outils)
1.2 Qualification des prospects (critères, questions, scoring)
1.3 Proposition commerciale (structure, prix, délais)
1.4 Closing (techniques, objections, signature)
1.5 Conditions de paiement (acompte, jalons, solde)

═══════════════════════════════════════════════════════════════
LIVRE 2 — LIVRAISON
═══════════════════════════════════════════════════════════════
2.1 Site web 500€ (checklist, délai 7j, livrables)
2.2 Automation IA 1500€ (checklist, délai 14j, livrables)
2.3 Pack 3000€ (checklist, délai 30j, livrables)
2.4 Gestion des révisions et des demandes hors-périmètre

═══════════════════════════════════════════════════════════════
LIVRE 3 — INCIDENTS ET DÉCISIONS CLÉS
═══════════════════════════════════════════════════════════════
[Intégrer les décisions loggées dans la base]

═══════════════════════════════════════════════════════════════
LIVRE 4 — URGENCES ET PROCÉDURES D'EXCEPTION
═══════════════════════════════════════════════════════════════
4.1 Client qui ne paie pas → procédure
4.2 API Gemini indisponible → plan de basculement
4.3 Litige client → contacts et procédure légale
4.4 Demande de remboursement → procédure et script

Compléter chaque section avec le contenu optimal pour Caelum.""",
        "GÉNÉRATION PLAYBOOK COMPLET — Caelum Partners"
    )
    sauvegarder("playbook_complet", r)


def audit_lecons_apprises():
    decisions_existantes = []
    log_file = "fichiers/playbook/decisions_log.json"
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                decisions_existantes = json.load(f)
        except Exception:
            pass

    contexte = json.dumps(decisions_existantes, ensure_ascii=False)[:3000] if decisions_existantes else "Aucune décision encore loggée."

    r = streamer(
        f"""Analyse les patterns dans les décisions passées de Caelum Partners.
Décisions disponibles : {contexte}

AUDIT DES LEÇONS APPRISES :

1. PATTERNS DE SUCCÈS (ce qui revient dans les décisions qui ont bien marché) :
   - Pattern 1 : [description] — fréquence : X fois
   - Pattern 2 : ...
   Recommandation : systématiser ces patterns dans tous les processus

2. PATTERNS D'ÉCHEC (ce qui revient dans les décisions moins réussies) :
   - Anti-pattern 1 : [description] — fréquence : X fois
   - Anti-pattern 2 : ...
   Recommandation : créer des garde-fous contre ces anti-patterns

3. DÉCISIONS À REVISITER (résultats non encore connus ou insatisfaisants) :
   - Décision X : suivre l'évolution
   - Décision Y : résultat à mesurer dans N jours

4. GAPS DU PLAYBOOK (situations récurrentes sans entrée de playbook) :
   - Situation 1 : [description] → créer une entrée playbook cette semaine
   - Situation 2 : ...

5. ÉVOLUTION DE LA MATURITÉ DÉCISIONNELLE :
   - Caelum prend-elle de meilleures décisions au fil du temps ?
   - Indicateurs de progression
   - Recommandation pour accélérer la maturité décisionnelle""",
        "AUDIT LEÇONS APPRISES — Patterns décisionnels Caelum Partners"
    )
    sauvegarder("audit_lecons_apprises", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  GARDIEN DU PLAYBOOK — Caelum Partners")
    print("  Mémoire institutionnelle · Templates · Jamais deux fois")
    print("═"*65)

    while True:
        print("\n  1. Enregistrer une décision dans le playbook")
        print("  2. Consulter le playbook (chercher une solution)")
        print("  3. Extraire un template depuis un succès")
        print("  4. Générer le playbook complet")
        print("  5. Audit des leçons apprises")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            enregistrer_decision()
        elif choix == "2":
            consulter_playbook()
        elif choix == "3":
            extraire_template()
        elif choix == "4":
            generer_playbook_complet()
        elif choix == "5":
            audit_lecons_apprises()
        else:
            print("  Choix invalide.")
