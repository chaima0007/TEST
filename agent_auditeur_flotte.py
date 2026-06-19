"""
AGENT AUDITEUR DE LA FLOTTE — Contrôleur qualité de tous les agents Caelum
Identité · Mission · Protocole d'audit · Directive de comportement
Mission : zéro output sous-standard ne quitte la flotte

Usage : python agent_auditeur_flotte.py
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

IDENTITE = """# AGENT AUDITEUR DE LA FLOTTE — CONTRÔLEUR QUALITÉ

## IDENTITÉ
Tu es l'Auditeur de la Flotte de Caelum Partners.
Tu es le seul agent autorisé à évaluer, noter et rejeter les outputs des autres agents.
Tu n'es pas un censeur — tu es un garant de l'excellence opérationnelle.
Ton autorité s'applique à tous les 72+ agents de la flotte sans exception.

## MISSION
Garantir que chaque output produit par la flotte répond aux standards de Caelum Partners
avant d'atteindre un client réel ou d'influencer une décision stratégique.
Un output sous-standard qui atteint un client = dommage réputationnel irréversible.
Un output sous-standard qui influence une décision = erreur stratégique coûteuse.

## PROTOCOLE D'AUDIT — 5 DIMENSIONS

### DIMENSION 1 — EXACTITUDE FACTUELLE (0-20 pts)
- Les chiffres sont-ils corrects et sourcés ?
- Les références légales belges sont-elles exactes (articles, seuils, dates) ?
- Les noms d'organismes sont-ils corrects (ONEM, INASTI, BCE, FSMA, AFSCA...) ?
- Les tarifs et délais mentionnés correspondent-ils à 2024/2025 ?
Pénalité : -5 pts par erreur factuelle, -10 pts par erreur légale

### DIMENSION 2 — PERTINENCE CAELUM (0-20 pts)
- L'output est-il aligné avec la mission de Caelum Partners ?
- Sert-il directement un objectif business de Chaima ?
- Evite-t-il les généralités sans valeur ajoutée ?
- Est-il adapté au contexte belge et à la phase actuelle (lancement) ?
Pénalité : -5 pts par recommandation générique non adaptée

### DIMENSION 3 — ACTIONNABILITÉ (0-20 pts)
- L'output contient-il des actions concrètes (verbe + objet + délai) ?
- Peut-on l'exécuter sans reformulation ?
- Les étapes sont-elles dans le bon ordre logique ?
- Evite-t-il les "explorer", "envisager", "considérer" sans action précise ?
Pénalité : -3 pts par recommandation vague non actionnable

### DIMENSION 4 — SÉCURITÉ & CONFORMITÉ (0-20 pts)
- L'output respecte-t-il la séparation ASBL/Caelum Partners ?
- Ne compromet-il pas la conformité ONEM de Chaima ?
- Ne contient-il aucune donnée client sensible exposée ?
- Les recommandations légales sont-elles accompagnées de la mention "consulter un professionnel" ?
Pénalité : -10 pts par risque légal ou sécuritaire identifié

### DIMENSION 5 — QUALITÉ RÉDACTIONNELLE (0-20 pts)
- L'output est-il clair, structuré, lisible ?
- Le niveau de langue est-il professionnel sans être inaccessible ?
- La longueur est-elle adaptée (ni trop court, ni noyé dans le bruit) ?
- L'output commence-t-il par la conclusion (Pyramid Principle) ?
Pénalité : -2 pts par problème de structure ou de clarté

## GRILLE DE VERDICT
- 90-100/100 : ✅ VALIDÉ — output prêt pour utilisation client
- 75-89/100  : ⚠️ VALIDÉ AVEC RÉSERVES — corrections mineures requises
- 60-74/100  : 🔄 RETOUR EN RÉVISION — l'agent doit retravailler cet output
- 0-59/100   : ❌ REJETÉ — output non conforme, reprendre de zéro

## DIRECTIVE DE COMPORTEMENT
- Aucune complaisance : un 75 doit être signalé, pas arrondi à 80
- Aucune notation émotionnelle : noter sur les faits, pas sur l'intention
- Feedback constructif obligatoire : chaque point retiré = correction précise proposée
- Rapidité : un audit ne doit pas prendre plus de 5 minutes
- Traçabilité : chaque audit est horodaté et sauvegardé"""


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
    os.makedirs("fichiers/auditeur_flotte", exist_ok=True)
    fichier = f"fichiers/auditeur_flotte/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Audit sauvegardé → {fichier}")


def auditer_output():
    """Soumet un output d'agent au protocole d'audit complet."""
    print("\n  Quel agent a produit cet output ? (ex: Agent Commercial, Agent Auditeur Financier)")
    nom_agent = input("  Agent source → ").strip()[:100] or "Agent non spécifié"
    print("\n  Colle l'output à auditer. (Entrée vide ×2 pour terminer)\n")
    lignes, vide = [], 0
    while vide < 2:
        ligne = input()
        if ligne == "":
            vide += 1
        else:
            vide = 0
            lignes.append(ligne)
    output = "\n".join(lignes).strip()[:4000]
    if not output:
        return

    r = streamer(
        f"""AUDIT QUALITÉ — Output de l'agent : {nom_agent}

OUTPUT À AUDITER :
{output}

APPLIQUER LE PROTOCOLE D'AUDIT COMPLET SUR 5 DIMENSIONS :

1. EXACTITUDE FACTUELLE (0-20) :
   - Chiffres et sources vérifiables
   - Références légales belges exactes
   - Erreurs factuelles détectées + corrections

2. PERTINENCE CAELUM (0-20) :
   - Alignement mission Caelum Partners
   - Adapté au contexte belge et phase lancement
   - Généralités non adaptées détectées

3. ACTIONNABILITÉ (0-20) :
   - Actions concrètes avec verbe + objet + délai
   - Recommandations vagues identifiées
   - Version actionnabilisée des points flous

4. SÉCURITÉ & CONFORMITÉ (0-20) :
   - Risques légaux ONEM/ASBL/RGPD détectés
   - Données sensibles exposées
   - Mentions professionnelles requises présentes

5. QUALITÉ RÉDACTIONNELLE (0-20) :
   - Structure et clarté
   - Niveau de langue
   - Longueur adaptée

SCORE TOTAL /100 + VERDICT (VALIDÉ / RÉSERVES / RÉVISION / REJETÉ)
CORRECTIONS PRIORITAIRES (liste numérotée)
OUTPUT CORRIGÉ (version améliorée si score < 90)""",
        f"AUDIT — {nom_agent}"
    )
    sauvegarder(f"audit_{nom_agent.replace(' ', '_')[:30]}", r)


def audit_rapide():
    """Audit express — score en 30 secondes sans détail."""
    print("\n  Output à auditer rapidement (max 500 mots)\n")
    output = input("  Output → ").strip()[:2000]
    if not output:
        return
    r = streamer(
        f"""AUDIT EXPRESS — Score rapide

Output : {output}

Donner UNIQUEMENT :
- Score /100 par dimension (5 lignes)
- Score total /100
- Verdict (1 mot)
- 3 corrections prioritaires (3 bullet points)

Format compact, pas de blabla.""",
        "AUDIT EXPRESS"
    )
    sauvegarder("audit_express", r)


def audit_agent_complet(nom_agent: str = ""):
    """Évalue le comportement global d'un agent sur la base de sa description."""
    if not nom_agent:
        print("\n  Quel agent veux-tu évaluer ? (ex: Agent Commercial, Agent Flux Économique)")
        nom_agent = input("  Agent → ").strip()[:100]
    if not nom_agent:
        return
    print(f"  Décris ce que fait cet agent et donne un exemple de son output habituel.")
    description = input("  Description → ").strip()[:3000]

    r = streamer(
        f"""AUDIT COMPORTEMENTAL — Agent : {nom_agent}
Description et comportement : {description}

ÉVALUER :
1. L'agent respecte-t-il son rôle défini dans la flotte Caelum ?
2. Ses outputs sont-ils cohérents avec les standards de la flotte ?
3. Y a-t-il des dérives comportementales (trop vague, trop risqué, hors sujet) ?
4. L'agent crée-t-il de la valeur nette ou du bruit ?
5. RECOMMANDATION : conserver / ajuster l'IDENTITE / fusionner avec un autre agent / supprimer

Score comportemental /100 + plan d'amélioration en 3 actions.""",
        f"AUDIT COMPORTEMENTAL — {nom_agent}"
    )
    sauvegarder(f"audit_comportemental_{nom_agent.replace(' ', '_')[:30]}", r)


def rapport_qualite_flotte():
    """Génère un rapport de qualité global de toute la flotte."""
    r = streamer(
        """RAPPORT DE QUALITÉ GLOBALE — Flotte Caelum Partners (72+ agents)

Générer un protocole d'audit standard applicable à toute la flotte :

1. CHECKLIST D'AUDIT UNIVERSELLE (applicable à tout output de tout agent)
   → 10 questions oui/non, réponse immédiate, score automatique

2. SIGNAUX D'ALERTE PAR TYPE D'AGENT :
   → Agents commerciaux : quels red flags dans leurs outputs ?
   → Agents légaux/financiers : quels red flags spécifiques ?
   → Agents stratégiques : quels red flags ?
   → Agents sectoriels : quels red flags ?

3. PROTOCOLE DE RÉVISION (quand un agent doit être reconfiguré)
   → Critères déclencheurs
   → Procédure de mise à jour
   → Validation post-révision

4. TABLEAU DE BORD QUALITÉ FLOTTE
   → Métriques à suivre hebdomadairement
   → Seuils d'alerte
   → Actions correctives automatiques

5. DIRECTIVE QUALITÉ PERMANENTE
   → Les 5 règles non négociables pour tout output Caelum""",
        "RAPPORT QUALITÉ GLOBALE — Flotte Caelum Partners"
    )
    sauvegarder("rapport_qualite_flotte", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AUDITEUR DE LA FLOTTE — Contrôleur Qualité Caelum")
    print("  Identité · Mission · Protocole Audit · Directive")
    print("═"*65)

    while True:
        print("\n  1. Auditer un output d'agent (protocole complet 5 dimensions)")
        print("  2. Audit express (score rapide /100)")
        print("  3. Audit comportemental d'un agent")
        print("  4. Rapport qualité globale de la flotte")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            auditer_output()
        elif choix == "2":
            audit_rapide()
        elif choix == "3":
            audit_agent_complet()
        elif choix == "4":
            rapport_qualite_flotte()
        else:
            print("  Choix invalide.")
