"""
AGENT RÉSOLVEUR — Résout les problèmes de manière ultra-professionnelle
Niveau consultant à 10 000€/jour : diagnostic précis, solutions concrètes,
exécution immédiate. Aucun problème ne reste sans solution.

Usage : python agent_resolveur.py
"""

import os
import sys
import json
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"


def _creer_model(model_name=None, system_instruction="", generation_config=None, **kwargs):
    """Compatibilité: retourne un proxy GenerativeModel pour google.genai."""
    class _ModelProxy:
        def __init__(self, mn, si, cfg):
            self.model_name = mn or MODEL
            self.system_instruction = si
            self.config = cfg or types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
            if isinstance(self.config, types.GenerateContentConfig):
                self.config = types.GenerateContentConfig(
                    system_instruction=si,
                    temperature=self.config.temperature if hasattr(self.config, 'temperature') else 0.3,
                    max_output_tokens=self.config.max_output_tokens if hasattr(self.config, 'max_output_tokens') else 2000,
                )
        def generate_content(self, prompt, stream=False):
            if stream:
                return client.models.generate_content_stream(
                    model=self.model_name, contents=prompt, config=self.config)
            return client.models.generate_content(
                model=self.model_name, contents=prompt, config=self.config)
    config = generation_config
    if config and not isinstance(config, types.GenerateContentConfig):
        config = types.GenerateContentConfig(
            temperature=getattr(config, 'temperature', 0.3),
            max_output_tokens=getattr(config, 'max_output_tokens', 2000),
        )
    return _ModelProxy(model_name, system_instruction, config)


def charger_memoire():
    try:
        if os.path.exists("memoire_entreprise.json"):
            with open("memoire_entreprise.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def streamer(instructions, prompt, label=""):
    if label:
        print(f"\n{'═'*60}\n  {label}\n{'═'*60}\n")
    model = _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=3000),
    )
    reponse = ""
    try:
        for chunk in model.generate_content(prompt, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


SYSTEM_RESOLVEUR = """Tu es le meilleur consultant en résolution de problèmes au monde.
Tu combines les méthodologies de McKinsey (MECE, pyramid principle),
Six Sigma (DMAIC), Design Thinking et les meilleures pratiques opérationnelles.
Ton niveau de précision et de profondeur : cabinet de conseil à 10 000€/jour.

Tes principes :
1. Jamais de réponse vague — toujours du concret et du mesurable
2. Toujours identifier la cause racine, pas juste les symptômes
3. Solutions classées par impact/effort
4. Plan d'action avec responsable + deadline pour chaque action
5. Anticiper les obstacles et prévoir les plans B
6. Définir le succès en termes mesurables"""


# ─────────────────────────────────────────────────────────────
# 1. DIAGNOSTIC ULTRA-RAPIDE — Identifier le vrai problème
# ─────────────────────────────────────────────────────────────

def diagnostic_rapide(probleme):
    streamer(
        SYSTEM_RESOLVEUR + """

FORMAT DE DIAGNOSTIC :
━━━━━━━━━━━━━━━━━━━━━
🔍 PROBLÈME RÉEL (pas le symptôme)
   [Reformulation précise du vrai problème]

🌳 ARBRE DES CAUSES (5 Pourquoi)
   Symptôme → Cause 1 → Cause 2 → Cause racine

📊 IMPACT RÉEL
   Coût estimé / Temps perdu / Opportunité manquée

⚡ SOLUTION IMMÉDIATE (dans l'heure)
   Action 1 → Résultat attendu
   Action 2 → ...

🎯 SOLUTION DÉFINITIVE (dans la semaine)
   Phase 1 / Phase 2 / Phase 3

✅ INDICATEURS DE RÉSOLUTION
   → Quand peut-on dire que c'est résolu ?

⚠️ RISQUES SI NON TRAITÉ
   [Ce qui se passera si on n'agit pas]""",
        f"Problème soumis : {probleme}\nDate : {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"DIAGNOSTIC — {probleme[:50]}"
    )


# ─────────────────────────────────────────────────────────────
# 2. RÉSOLUTION EN MODE CRISE — Urgence maximale
# ─────────────────────────────────────────────────────────────

def mode_crise(situation):
    streamer(
        SYSTEM_RESOLVEUR + """

Tu es en mode GESTION DE CRISE. Chaque minute compte.

FORMAT CRISE :
🚨 NIVEAU D'ALERTE : [CRITIQUE/ÉLEVÉ/MODÉRÉ]
⏰ FENÊTRE D'ACTION : [Combien de temps avant que ça empire]

━━ PROCHAINES 15 MINUTES ━━
   □ Action 1 — Responsable : [qui] — Durée : [X min]
   □ Action 2 — ...

━━ PROCHAINE HEURE ━━
   □ ...

━━ PROCHAINES 24H ━━
   □ ...

📣 COMMUNICATION : [Que dire aux parties prenantes maintenant]
🛡️ PROTECTION : [Comment éviter que ça empire]
📋 POST-MORTEM : [Planifier l'analyse pour éviter la récidive]""",
        f"Situation de crise : {situation}\nHeure : {datetime.now().strftime('%H:%M')}",
        "MODE CRISE — Résolution urgente"
    )


# ─────────────────────────────────────────────────────────────
# 3. RÉSOLUTION SYSTÉMIQUE — Problème récurrent
# ─────────────────────────────────────────────────────────────

def resolution_systemique(probleme_recurrent):
    streamer(
        SYSTEM_RESOLVEUR + """

Ce problème est RÉCURRENT — il faut une solution définitive, pas un patch.
Tu appliques la méthode DMAIC (Six Sigma) :

DEFINE — Définir précisément le problème
MEASURE — Mesurer l'impact actuel
ANALYZE — Analyser les causes profondes
IMPROVE — Concevoir la solution durable
CONTROL — Mécanismes pour éviter la récidive

FORMAT :
📌 DÉFINITION PRÉCISE
   [Ce qui se passe, depuis quand, fréquence]

📏 MESURE D'IMPACT
   Coût total / Fréquence / Personnes touchées

🔬 ANALYSE CAUSALE (Ishikawa 4M)
   Méthode / Matière / Machine / Main d'œuvre

💡 SOLUTION DURABLE
   Court terme (patch) : ...
   Moyen terme (fix) : ...
   Long terme (prévention) : ...

🔒 MÉCANISMES DE CONTRÔLE
   → Alerte si le problème revient : [indicateur]
   → Revue mensuelle : [quoi vérifier]
   → Agent à utiliser : [agent_X.py]""",
        f"Problème récurrent : {probleme_recurrent}",
        f"RÉSOLUTION SYSTÉMIQUE — {probleme_recurrent[:40]}"
    )


# ─────────────────────────────────────────────────────────────
# 4. ARBITRAGE — Choisir entre plusieurs options
# ─────────────────────────────────────────────────────────────

def arbitrage(question, options):
    streamer(
        SYSTEM_RESOLVEUR + """

Tu aides à prendre la MEILLEURE DÉCISION possible en analysant chaque option
avec une grille d'évaluation objective.

FORMAT :
⚖️ QUESTION DE DÉCISION
   [Reformulation précise de l'enjeu]

GRILLE D'ÉVALUATION (sur 5) :
Option | Impact | Faisabilité | Coût | Risque | Score total

ANALYSE DÉTAILLÉE :
Option A :
  ✅ Avantages : ...
  ❌ Inconvénients : ...
  ⚠️ Risques : ...
  💰 Coût estimé : ...

Option B : [même format]

🏆 RECOMMANDATION
   Option choisie : [X]
   Pourquoi : [3 raisons concrètes]
   Condition de succès : [ce qui doit être vrai]
   Plan B si ça ne marche pas : [...]

⏰ DÉCIDER AVANT : [deadline]""",
        f"Question : {question}\nOptions : {options}",
        f"ARBITRAGE — {question[:40]}"
    )


# ─────────────────────────────────────────────────────────────
# 5. RÉTROSPECTIVE & AMÉLIORATION CONTINUE
# ─────────────────────────────────────────────────────────────

def retrospective(periode, ce_qui_sest_passe):
    streamer(
        SYSTEM_RESOLVEUR + """

Tu conduis une rétrospective professionnelle pour extraire
les leçons et améliorer les performances futures.

FORMAT :
📅 PÉRIODE ANALYSÉE : [X]

🌟 CE QUI A BIEN FONCTIONNÉ
   (avec les raisons du succès — à reproduire)

❌ CE QUI N'A PAS FONCTIONNÉ
   (avec les causes — à éviter)

💡 LESSONS LEARNED
   Leçon 1 : [situation → ce qu'on apprend → règle à appliquer]
   Leçon 2 : ...

🔧 ACTIONS D'AMÉLIORATION
   Action | Responsable | Deadline | Agent à utiliser

📈 OBJECTIFS PÉRIODE SUIVANTE
   KPI 1 : [métrique actuelle → objectif]
   KPI 2 : ...

🤖 CALIBRATION DES AGENTS
   Agent X : augmenter utilisation car...
   Agent Y : paramétrer différemment car...""",
        f"Période : {periode}\nFaits : {ce_qui_sest_passe}",
        f"RÉTROSPECTIVE — {periode}"
    )


# ─────────────────────────────────────────────────────────────
# 6. MODE CONVERSATIONNEL — Résolveur en temps réel
# ─────────────────────────────────────────────────────────────

def mode_conversationnel():
    memoire = charger_memoire()
    historique = []

    print("\n" + "═"*60)
    print("  RÉSOLVEUR — Mode consultant temps réel")
    print("  Pose ton problème. Je le résous.")
    print("  Tape 'quitter' pour arrêter.")
    print("═"*60)

    system = f"""{SYSTEM_RESOLVEUR}

Contexte entreprise :
- Clients : {list(memoire.get('clients', {}).keys()) or 'aucun'}
- Tickets : {len(memoire.get('tickets', []))}
- Projets : {list(memoire.get('projets', {}).keys()) or 'aucun'}

Tu résous chaque problème soumis avec précision et profondeur.
Tes réponses sont toujours : diagnostic + solution + plan d'action.
Maximum 300 mots par réponse. Dense, actionnable, pro."""

    model = _creer_model(
        model_name=MODEL,
        system_instruction=system,
        generation_config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=600),
    )

    while True:
        probleme = input("\n  Problème → ").strip()
        if probleme.lower() in ["quitter", "quit", "exit"]:
            break
        if not probleme:
            continue

        historique.append({"role": "user", "parts": [probleme]})
        chat = model.start_chat(history=historique[:-1])

        print("\n  Résolveur → ", end="", flush=True)
        reponse = ""
        try:
            for chunk in chat.send_message(probleme, stream=True):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    reponse += chunk.text
        except Exception as e:
            print(f"[Erreur : {e}]")
        print()

        historique.append({"role": "model", "parts": [reponse]})


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  AGENT RÉSOLVEUR — Consultant à 10 000€/jour")
    print("  Caelum Partners — Zéro problème sans solution")
    print("═"*60)

    while True:
        print("\n  1. Diagnostic rapide — Identifier le vrai problème")
        print("  2. Mode crise — Urgence maximale")
        print("  3. Résolution systémique — Problème récurrent")
        print("  4. Arbitrage — Choisir entre plusieurs options")
        print("  5. Rétrospective — Leçons & amélioration continue")
        print("  6. Mode conversationnel — Consultant en temps réel")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            pb = input("  Décris le problème → ").strip()
            if pb:
                diagnostic_rapide(pb)
        elif choix == "2":
            sit = input("  Décris la situation de crise → ").strip()
            if sit:
                mode_crise(sit)
        elif choix == "3":
            pb = input("  Quel problème revient tout le temps ? → ").strip()
            if pb:
                resolution_systemique(pb)
        elif choix == "4":
            q = input("  Question de décision → ").strip()
            opts = input("  Options (ex: A, B, C) → ").strip()
            if q and opts:
                arbitrage(q, opts)
        elif choix == "5":
            periode = input("  Période (ex: semaine du 10/06) → ").strip()
            faits = input("  Ce qui s'est passé (résumé) → ").strip()
            if periode and faits:
                retrospective(periode, faits)
        elif choix == "6":
            mode_conversationnel()
        else:
            print("  Choix invalide.")
