"""
AGENT ARCHITECTE DE LA SYNTHÈSE EXPONENTIELLE — Unificateur de vision stratégique
Fusionne les outputs de tous les agents · Décisions structurées · Trajectoire unique

Usage : python agent_synthese_exponentielle.py
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

IDENTITE = """# AGENT ARCHITECTE DE LA SYNTHÈSE EXPONENTIELLE

## IDENTITÉ ET RÔLE
Tu es l'Architecte de la Synthèse Exponentielle de Caelum Partners.
Tu es le cerveau unificateur : tu fusionnes les outputs de tous les autres agents
pour générer UNE trajectoire stratégique unique, cohérente et exponentielle.

Tu ne produis PAS de rapports passifs. Tu produis des DÉCISIONS STRUCTURÉES.
Tu garantis l'alignement permanent de chaque action avec la vision empire de Caelum Partners.

## CONTEXTE — VISION EMPIRE CAELUM PARTNERS
### Fondatrice : Chaima Mhadbi, Bruxelles, Belgique
### Les deux entités :
1. ASBL (présidente) — activité sociale/associative séparée
2. CAELUM PARTNERS (activité commerciale IA) — l'empire en construction

### Services actuels : 500€ / 1500€ / 3000€
### Vision 5 ans : référence européenne IA pour PME
### Phase actuelle : lancement — rampe de lancement, pas un plafond

## AGENTS QUE TU SYNTHÉTISES (31+ agents Caelum Partners)
Tu connais les outputs de tous ces agents et tu les unifies :
- COMMERCIAL : prospects, pipeline, closing
- AUDITEUR FINANCIER : conformité ONEM/CSC, seuils
- COMPTABLE BELGE : TVA, BCE, INASTI, déductions
- GROWTH : leviers acquisition, LinkedIn, campagnes
- EMPIRE : vision 5 ans, expansion, franchise
- RED TEAM : failles, Black Swans, résilience
- FLUX ÉCONOMIQUE : vélocité capital, frictions, DSO
- TITAN : 50 simulations, 20 experts, verdicts
- AUTOPILOT : cycles autonomes, actions générées
- GUIDE : priorités quotidiennes, prochaine étape
- FINANCEMENT : subventions, Innoviris, Hub Brussels

## FRAMEWORK DE SYNTHÈSE EXPONENTIELLE

### LOIS DE L'EXPONENTIEL QUE TU APPLIQUES
1. LOI DU LEVIER : chaque action doit créer 10x son effort initial
2. LOI DE L'ACTIF : préférer construire un actif (agent, processus, réputation) plutôt qu'un revenu ponctuel
3. LOI DU RÉSEAU : chaque client doit en amener 3 autres (coefficient viral k > 0.3)
4. LOI DE LA COMPOUNDISATION : les petits gains composés sur 5 ans créent l'empire

### MATRICE DE DÉCISION STRATÉGIQUE
Pour chaque décision, évaluer sur 5 axes :
- IMPACT EMPIRE (1-10) : contribution à la vision 5 ans
- VITESSE REVENU (1-10) : rapidité de retour financier
- SCALABILITÉ (1-10) : peut-on le répliquer × 100 ?
- RÉSILIENCE (1-10) : résiste aux Black Swans ?
- ALIGNEMENT LÉGAL (1-10) : 10 = parfaitement conforme Belgique

Score total > 35/50 = PRIORITÉ HAUTE
Score total 25-35 = À PLANIFIER
Score total < 25 = DÉPRIORISER ou REFUSER

## FORMAT DE SORTIE — SYNTHÈSE EXPONENTIELLE
1. ÉTAT DE L'EMPIRE (snapshot de tous les agents actifs)
2. DÉCISION UNIFIÉE (pas de rapport — une décision avec score matrice)
3. TRAJECTOIRE (les 3 prochains paliers de l'empire avec conditions de déclenchement)
4. ALIGNEMENT (vérification que tous les agents pointent dans la même direction)
5. PROCHAINE ACTION EMPIRE (UNE action, maintenant, qui génère le plus de valeur composée)"""


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
    os.makedirs("fichiers/synthese", exist_ok=True)
    fichier = f"fichiers/synthese/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def charger_tous_les_contextes() -> dict:
    """Charge tous les fichiers JSON pour la synthèse complète."""
    ctx = {}
    for fichier, cle in [
        ("memoire_entreprise.json", "memoire"),
        ("crm_pipeline.json", "pipeline"),
        ("historique_caelum.json", "historique"),
        ("autopilot_log.json", "autopilot"),
        ("watchdog_sante.json", "watchdog"),
    ]:
        if os.path.exists(fichier):
            try:
                with open(fichier, "r", encoding="utf-8") as f:
                    ctx[cle] = json.load(f)
            except Exception:
                ctx[cle] = {}
    return ctx


def synthese_empire_hebdomadaire():
    ctx = charger_tous_les_contextes()
    r = streamer(
        f"""SYNTHÈSE EMPIRE HEBDOMADAIRE — Caelum Partners
Données de tous les agents : {json.dumps(ctx, ensure_ascii=False)[:3000]}

GÉNÉRER :
1. ÉTAT DE L'EMPIRE cette semaine (ce qui a avancé, ce qui est bloqué)
2. SCORE EMPIRE /100 (combinaison : revenus, pipeline, résilience, légalité, croissance)
3. DÉCISION STRATÉGIQUE UNIFIÉE : quelle est LA décision la plus importante à prendre ?
   → Évaluer avec la matrice (Impact Empire / Vitesse Revenu / Scalabilité / Résilience / Légalité)
4. TRAJECTOIRE 3 PALIERS :
   - Palier 1 : prochain jalon (conditions + délai)
   - Palier 2 : expansion suivante
   - Palier 3 : vision empire (12 mois)
5. ALIGNEMENT DES AGENTS : est-ce que tous les agents pointent dans la même direction ?
6. ACTION EMPIRE DE LA SEMAINE : UNE action, maintenant""",
        "SYNTHÈSE EXPONENTIELLE HEBDOMADAIRE — Empire Caelum Partners"
    )
    sauvegarder("synthese_hebdo", r)


def evaluer_decision_empire():
    decision = input("\n  Décision à évaluer → ").strip()
    if not decision:
        return
    r = streamer(
        f"""ÉVALUATION STRATÉGIQUE — Matrice Exponentielle Caelum Partners
Décision soumise : {decision}

ÉVALUER SUR 5 AXES (score /10 chacun, justification) :
1. IMPACT EMPIRE : contribution à la vision 5 ans Caelum ?
2. VITESSE REVENU : dans combien de jours génère-t-elle du CA ?
3. SCALABILITÉ : peut-on répliquer cette décision × 100 sans Chaima ?
4. RÉSILIENCE : résiste à un Black Swan (API coupée, Chaima malade) ?
5. ALIGNEMENT LÉGAL : parfaitement conforme Belgique (ONEM, TVA, ASBL) ?

VERDICT :
- Score > 35/50 → DÉCISION EMPIRE (exécuter maintenant)
- Score 25-35 → PLANIFIER (dans 30 jours, après ajustements)
- Score < 25 → REFUSER ou PIVOTER (explication + alternative)

VARIANTES : proposer 2 alternatives avec leur score respectif.""",
        f"ÉVALUATION EMPIRE — {decision[:50]}"
    )
    sauvegarder("evaluation_decision", r)


def trajectoire_exponentielle():
    r = streamer(
        """Génère la trajectoire exponentielle complète de Caelum Partners.
De la situation actuelle (0 clients, lancement) jusqu'à l'empire européen.

FORMAT EXPONENTIEL :
PALIER 0 — MAINTENANT : 0 client, 0€ CA Caelum
  → Condition de passage au palier 1 : [X événement]

PALIER 1 — RAMPE (J+90) : 10 clients, 15 000€ CA
  → Ce qui change structurellement à ce palier
  → Condition de passage au palier 2

PALIER 2 — DÉCOLLAGE (M+6) : 30 clients, 50 000€ CA
  → Premier embauche ou sous-traitant ?
  → Premiers actifs récurrents (abonnements ?)

PALIER 3 — CROISSANCE (M+12) : 100 clients, 150 000€ CA
  → Légitimité pour lever des fonds
  → Expansion France/Luxembourg

PALIER 4 — EMPIRE (M+36) : 500 clients, 1M€ CA
  → Modèle franchise, licences, SaaS

PALIER 5 — SINGULARITÉ (M+60) : référence européenne IA PME

Pour chaque palier : métriques clés, décisions structurelles, risques principaux.""",
        "TRAJECTOIRE EXPONENTIELLE — De 0 à l'empire Caelum Partners"
    )
    sauvegarder("trajectoire_exponentielle", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  SYNTHÈSE EXPONENTIELLE — Architecte de l'Empire Caelum")
    print("  Unifier · Décider · Aligner · Trajectoire unique")
    print("═"*65)

    while True:
        print("\n  1. Synthèse empire hebdomadaire (tous agents unifiés)")
        print("  2. Évaluer une décision avec la matrice exponentielle")
        print("  3. Trajectoire exponentielle — de 0 à l'empire")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            synthese_empire_hebdomadaire()
        elif choix == "2":
            evaluer_decision_empire()
        elif choix == "3":
            trajectoire_exponentielle()
        else:
            print("  Choix invalide.")
