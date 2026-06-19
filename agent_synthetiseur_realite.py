"""
AGENT SYNTHÉTISEUR DE RÉALITÉ (GROUND TRUTH) — Filtre ultime de la flotte
Compression · Vérification fondamentale · Détection de biais · Vérité brute
Mission : transformer le bruit en vérité opérationnelle actionnable

Usage : python agent_synthetiseur_realite.py
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

IDENTITE = """# AGENT SYNTHÉTISEUR DE RÉALITÉ — GROUND TRUTH

## IDENTITÉ ET RÔLE
Tu es le Synthétiseur de Réalité de Caelum Partners.
Tu es le filtre ultime entre la complexité de la flotte et la capacité de décision de Chaima.
Tu transformes le bruit en vérité opérationnelle.

Ta loi fondamentale : une idée qui ne repose pas sur une vérité fondamentale
(mathématique, logique, physique, légale) est une opinion déguisée en stratégie.
Tu élimines les opinions avant qu'elles arrivent sur le bureau du fondateur.

## TROIS FONCTIONS CORE

### 1. VÉRIFICATION FONDAMENTALE
Chaque proposition est soumise à ce test en 3 questions :
- Q1 : Cette affirmation est-elle une LOI (mathématique, physique, légale, logique) ou une OPINION ?
- Q2 : Peut-on la falsifier (Popper) ? Si non, c'est une croyance, pas une vérité.
- Q3 : Repose-t-elle sur des données réelles (chiffrées, datées, sourcées) ou sur des hypothèses ?

Lois fondamentales applicables à Caelum Partners :
- LOI DE PARETO : 20% des actions génèrent 80% des résultats → toujours identifier ces 20%
- LOI DE METCALFE : la valeur d'un réseau est proportionnelle au carré du nombre de ses membres
- LOI DE MOORE (adaptée IA) : la puissance des agents IA double environ tous les 12-18 mois
- LOI DES RENDEMENTS COMPOSÉS : une croissance de 1%/jour = 37x en 1 an (e^365×0.01)
- LOI DE BROOKS : ajouter des personnes à un projet en retard le retarde davantage
- LOI DE GOODHART : quand une mesure devient un objectif, elle cesse d'être une bonne mesure
- LOI DU SEUIL ONEM : net Caelum trimestriel ≤ 6 521.45€ (chef famille) — LÉGAL, non négociable
- LOI TVA BELGE : CA annuel ≥ 25 000€ → TVA 21% obligatoire — LÉGAL, non négociable

### 2. COMPRESSION MAXIMALE
Format de sortie obligatoire pour toute synthèse :
- UNE PHRASE DE VÉRITÉ BRUTE : ce qui est réellement vrai, sans fioritures
- 3 POINTS D'ACTION : les 3 seules actions qui comptent vraiment
- CE QUI PEUT ATTENDRE : tout le reste (classé par priorité décroissante)

Règle de compression : si une décision nécessite plus de 3 phrases pour être expliquée,
elle n'est pas encore assez claire pour être exécutée.

### 3. DÉTECTION DE BIAIS
Biais à traquer dans les outputs de la flotte :
- BIAIS DE CONFIRMATION : la flotte cherche-t-elle des preuves pour valider une idée déjà choisie ?
- BIAIS D'OPTIMISME : les projections sont-elles basées sur le meilleur scénario plutôt que le médian ?
- BIAIS DE SUNK COST : continue-t-on une direction parce qu'on y a déjà investi du temps ?
- BIAIS D'AUTORITÉ : accepte-t-on une recommandation parce qu'elle vient d'un "agent expert" ?
- BIAIS DE RÉCENCE : surpondère-t-on les événements récents par rapport aux tendances longues ?
- BIAIS DE COMPLEXITÉ : une solution complexe est-elle préférée à une simple parce qu'elle paraît plus sérieuse ?

## CONTEXTE CAELUM PARTNERS
- Fondatrice : Chaima Mhadbi, Bruxelles, Belgique
- Phase : lancement, 0 client — chaque décision compte double
- Contraintes réelles : ONEM (seuil légal), ASBL (séparation légale), budget bootstrap (~0€)
- Vérités fondamentales de la phase lancement :
  * Zéro CA = zéro données = zéro apprentissage → priorité absolue : premier client
  * 85-95% de marge = l'argent n'est pas le problème, le client est le problème
  * Un agent IA ne génère pas de revenus seul — Chaima doit prospecter

## FORMAT DE SORTIE OBLIGATOIRE
1. VÉRITÉ BRUTE (1 phrase, maximum 20 mots)
2. FONDEMENT (loi ou donnée réelle sur laquelle repose cette vérité)
3. BIAIS DÉTECTÉS (liste des biais présents dans l'input, avec exemple précis)
4. 3 ACTIONS PRIORITAIRES (et rien d'autre)
5. CE QUI PEUT ATTENDRE (tout ce qui ne figure pas dans les 3 actions)
6. NIVEAU DE CONFIANCE (0-100%) avec justification basée sur des données réelles"""


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
                max_output_tokens=2500,
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
    os.makedirs("fichiers/ground_truth", exist_ok=True)
    fichier = f"fichiers/ground_truth/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def comprimer_rapport():
    """Compresse un rapport long (output d'un autre agent) en vérité brute + 3 actions."""
    print("\n  Colle le rapport ou l'analyse à compresser.")
    print("  (Entrée vide deux fois pour terminer)\n")
    lignes = []
    vide = 0
    while vide < 2:
        ligne = input()
        if ligne == "":
            vide += 1
        else:
            vide = 0
            lignes.append(ligne)

    rapport = "\n".join(lignes).strip()
    if not rapport:
        return

    r = streamer(
        f"""COMPRESSION — Synthèse de ce rapport en vérité opérationnelle brute

RAPPORT À COMPRESSER :
{rapport[:4000]}

APPLIQUER LE PROTOCOLE GROUND TRUTH :
1. Extraire la VÉRITÉ BRUTE en une seule phrase (≤ 20 mots)
2. Identifier le FONDEMENT (loi ou donnée réelle derrière cette vérité)
3. Détecter les BIAIS présents dans le rapport
4. Distiller en 3 ACTIONS PRIORITAIRES seulement (éliminer tout le reste)
5. Lister CE QUI PEUT ATTENDRE (par ordre de priorité décroissante)
6. Donner le NIVEAU DE CONFIANCE (0-100%) et pourquoi

Si le rapport contient des affirmations non fondées sur des données réelles, les signaler explicitement.""",
        "COMPRESSION GROUND TRUTH"
    )
    sauvegarder("compression", r)


def verifier_fondement():
    """Vérifie si une proposition repose sur une loi fondamentale ou une opinion."""
    print("\n  Quelle proposition ou idée veux-tu soumettre à la vérification ?\n")
    proposition = input("  Proposition → ").strip()
    if not proposition:
        return

    r = streamer(
        f"""VÉRIFICATION FONDAMENTALE — Test Ground Truth

PROPOSITION SOUMISE : {proposition}

APPLIQUER LE TEST EN 3 QUESTIONS :
Q1 — LOI ou OPINION ? Est-ce une vérité fondamentale (mathématique, physique, légale, logique)
     ou une convention sectorielle/opinion déguisée en stratégie ?

Q2 — FALSIFIABILITÉ (Popper) : peut-on concevoir une expérience qui prouverait que c'est faux ?
     Si non → c'est une croyance, pas une vérité.

Q3 — DONNÉES RÉELLES : cette proposition repose-t-elle sur des chiffres datés et sourcés
     ou sur des hypothèses et estimations non vérifiées ?

VERDICT :
- VÉRITÉ FONDAMENTALE (repose sur une loi) → préciser laquelle + comment l'exploiter
- VÉRITÉ CONDITIONNELLE (vraie sous certaines conditions) → préciser les conditions exactes
- OPINION SECTORIELLE (convention, pas une loi) → reformuler comme hypothèse testable
- BIAIS COGNITIF (erreur de raisonnement) → nommer le biais + version corrigée

CONCLUSION : version purifiée de la proposition, exprimée comme une vérité testable.""",
        f"VÉRIFICATION FONDAMENTALE — {proposition[:50]}"
    )
    sauvegarder("verification_fondement", r)


def detecter_biais_flotte():
    """Analyse les outputs de plusieurs agents pour détecter les biais systémiques."""
    print("\n  Colle les outputs de la flotte à analyser pour détecter les biais.")
    print("  (Entrée vide deux fois pour terminer)\n")
    lignes = []
    vide = 0
    while vide < 2:
        ligne = input()
        if ligne == "":
            vide += 1
        else:
            vide = 0
            lignes.append(ligne)

    outputs = "\n".join(lignes).strip()
    if not outputs:
        return

    r = streamer(
        f"""DÉTECTION DE BIAIS — Analyse critique des outputs de la flotte

OUTPUTS SOUMIS :
{outputs[:4000]}

ANALYSER CHAQUE BIAIS :
1. BIAIS DE CONFIRMATION : la flotte cherche-t-elle des preuves pour valider une décision déjà prise ?
   → Exemple concret dans le texte si présent

2. BIAIS D'OPTIMISME : les projections utilisent-elles le meilleur scénario comme scénario de base ?
   → Quelle est la projection médiane réaliste vs celle présentée ?

3. BIAIS DE SUNK COST : une direction est-elle maintenue à cause de l'investissement passé ?
   → Si oui, quel est le coût réel de continuer vs pivoter ?

4. BIAIS D'AUTORITÉ : des recommandations sont-elles acceptées sans preuve parce qu'elles viennent d'un "expert" ?

5. BIAIS DE RÉCENCE : les événements récents sont-ils surpondérés vs les tendances longues ?

6. BIAIS DE COMPLEXITÉ : une solution complexe est-elle préférée à une plus simple ?

SCORE DE BIAIS GLOBAL (0-100 : 0 = zéro biais, 100 = entièrement biaisé)
RECOMMANDATION : version débiaisée de la conclusion principale""",
        "DÉTECTION DE BIAIS — Analyse de la flotte"
    )
    sauvegarder("detection_biais", r)


def vérité_phase_lancement():
    """Génère les vérités fondamentales de la phase lancement Caelum."""
    r = streamer(
        """VÉRITÉS FONDAMENTALES — Phase lancement Caelum Partners

Générer les vérités brutes non négociables de la phase actuelle (0 client, bootstrap, Bruxelles).

FORMAT POUR CHAQUE VÉRITÉ :
- VÉRITÉ BRUTE (1 phrase ≤ 20 mots)
- LOI FONDAMENTALE (quelle loi la sous-tend)
- IMPLICATION OPÉRATIONNELLE (ce que ça signifie concrètement pour Chaima cette semaine)
- ERREUR CLASSIQUE (ce que les fondateurs font souvent à la place)

Couvrir :
1. La vérité sur l'acquisition clients au lancement
2. La vérité sur le pricing à 0 référence
3. La vérité sur la scalabilité avec 0 client
4. La vérité sur les agents IA comme outil (pas comme magie)
5. La vérité sur le temps disponible vs les priorités
6. La vérité sur la conformité légale (ONEM/INASTI/BCE)
7. La vérité sur le premier euro gagné

Chaque vérité doit pouvoir tenir sur un post-it.""",
        "VÉRITÉS FONDAMENTALES — Phase lancement Caelum"
    )
    sauvegarder("verites_fondamentales_lancement", r)


def synthese_decision_finale():
    """Synthétise toutes les données disponibles en une décision unique."""
    donnees = {}
    for fichier, cle in [
        ("memoire_entreprise.json", "memoire"),
        ("crm_pipeline.json", "pipeline"),
        ("historique_caelum.json", "historique"),
        ("autopilot_log.json", "autopilot"),
    ]:
        if os.path.exists(fichier):
            try:
                with open(fichier, "r", encoding="utf-8") as f:
                    donnees[cle] = json.load(f)
            except Exception:
                pass

    contexte = json.dumps(donnees, ensure_ascii=False)[:3000] if donnees else "Aucune donnée disponible"

    print("\n  Quelle est la décision en suspens que tu veux trancher ?\n")
    decision = input("  Décision → ").strip()
    if not decision:
        return

    r = streamer(
        f"""SYNTHÈSE DÉCISION FINALE — Ground Truth pour une décision unique

DÉCISION EN SUSPENS : {decision}
DONNÉES DISPONIBLES : {contexte}

PROTOCOLE DE DÉCISION GROUND TRUTH :

1. VÉRITÉ BRUTE (1 phrase) : quelle est la réalité objective de cette décision ?
2. CE QU'ON SAIT AVEC CERTITUDE (données confirmées)
3. CE QU'ON NE SAIT PAS ENCORE (hypothèses non testées — ne pas décider dessus)
4. BIAIS POTENTIELS dans le cadrage de cette décision
5. LA DÉCISION (oui/non/attendre) basée uniquement sur les faits
6. CONDITION DE RÉVISION : quand et si quoi réviser cette décision

Interdiction : recommander "explorer les deux options" ou "faire les deux". UNE décision.""",
        f"DÉCISION FINALE — {decision[:50]}"
    )
    sauvegarder("decision_finale", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  SYNTHÉTISEUR DE RÉALITÉ — Ground Truth Caelum Partners")
    print("  Compression · Vérification · Biais · Vérité brute")
    print("═"*65)

    while True:
        print("\n  1. Compresser un rapport en vérité brute + 3 actions")
        print("  2. Vérifier le fondement d'une proposition (loi ou opinion ?)")
        print("  3. Détecter les biais dans les outputs de la flotte")
        print("  4. Vérités fondamentales de la phase lancement")
        print("  5. Synthèse décision finale (trancher une question ouverte)")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            comprimer_rapport()
        elif choix == "2":
            verifier_fondement()
        elif choix == "3":
            detecter_biais_flotte()
        elif choix == "4":
            vérité_phase_lancement()
        elif choix == "5":
            synthese_decision_finale()
        else:
            print("  Choix invalide.")
