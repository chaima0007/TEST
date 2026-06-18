"""
AGENT WATCHDOG — Surveillance 24h/24 de tous les agents
Vérifie que chaque agent est opérationnel, détecte les pannes,
envoie des alertes et génère des rapports de santé.

Usage : python agent_watchdog.py
        python agent_watchdog.py --continu   (boucle infinie)
"""

import os
import sys
import json
import time
import subprocess
import hashlib
from datetime import datetime, timedelta
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

JOURNAL_SANTE = "watchdog_sante.json"

AGENTS_SURVEILLES = {
    "lancer.py":                   {"critique": True,  "timeout": 5},
    "orchestrateur.py":            {"critique": True,  "timeout": 5},
    "agent_commercial.py":         {"critique": True,  "timeout": 5},
    "agent_facturation.py":        {"critique": True,  "timeout": 5},
    "agent_support_client.py":     {"critique": True,  "timeout": 5},
    "securite.py":                 {"critique": True,  "timeout": 5},
    "agent_veille.py":             {"critique": False, "timeout": 5},
    "agent_seo.py":                {"critique": False, "timeout": 5},
    "agent_juridique.py":          {"critique": False, "timeout": 5},
    "agent_recrutement.py":        {"critique": False, "timeout": 5},
    "agent_reference.py":          {"critique": False, "timeout": 5},
    "agent_chef_projet.py":        {"critique": False, "timeout": 5},
    "agent_kpi.py":                {"critique": False, "timeout": 5},
    "agent_reputation.py":         {"critique": False, "timeout": 5},
    "agent_pricing.py":            {"critique": False, "timeout": 5},
    "agent_comptable.py":          {"critique": False, "timeout": 5},
    "agent_strategie.py":          {"critique": False, "timeout": 5},
    "agent_data.py":               {"critique": False, "timeout": 5},
    "agent_veille_techno.py":      {"critique": False, "timeout": 5},
    "agent_partenariats.py":       {"critique": False, "timeout": 5},
    "agent_onboarding_employe.py": {"critique": False, "timeout": 5},
    "agent_formation_equipe.py":   {"critique": False, "timeout": 5},
    "agent_bienetre_equipe.py":    {"critique": False, "timeout": 5},
    "agent_fluidite.py":           {"critique": False, "timeout": 5},
    "agent_adaptation.py":         {"critique": False, "timeout": 5},
    "agent_jumeau_numerique.py":   {"critique": False, "timeout": 5},
    "agent_oracle.py":             {"critique": False, "timeout": 5},
    "agent_innovation.py":         {"critique": False, "timeout": 5},
    "agent_ethique_ia.py":         {"critique": False, "timeout": 5},
    "agent_memoire_collective.py": {"critique": False, "timeout": 5},
    "agent_guide.py":              {"critique": False, "timeout": 5},
    "agent_fantome.py":            {"critique": True,  "timeout": 5},
}


def charger_sante():
    if os.path.exists(JOURNAL_SANTE):
        try:
            with open(JOURNAL_SANTE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"checks": [], "agents": {}, "derniere_verification": ""}


def sauvegarder_sante(sante):
    with open(JOURNAL_SANTE, "w", encoding="utf-8") as f:
        json.dump(sante, f, ensure_ascii=False, indent=2)


def verifier_agent(nom_fichier):
    """Vérifie qu'un agent existe et sa syntaxe Python est valide."""
    resultat = {
        "agent": nom_fichier,
        "timestamp": datetime.now().isoformat(),
        "existe": False,
        "syntaxe_ok": False,
        "taille": 0,
        "hash": "",
        "statut": "INCONNU",
        "erreur": "",
    }

    if not os.path.exists(nom_fichier):
        resultat["statut"] = "MANQUANT"
        resultat["erreur"] = "Fichier introuvable"
        return resultat

    resultat["existe"] = True
    resultat["taille"] = os.path.getsize(nom_fichier)

    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            contenu = f.read()
        resultat["hash"] = hashlib.md5(contenu.encode()).hexdigest()[:8]
    except Exception as e:
        resultat["erreur"] = str(e)
        resultat["statut"] = "ERREUR_LECTURE"
        return resultat

    try:
        proc = subprocess.run(
            [sys.executable, "-m", "py_compile", nom_fichier],
            capture_output=True, text=True, timeout=10
        )
        if proc.returncode == 0:
            resultat["syntaxe_ok"] = True
            resultat["statut"] = "OK"
        else:
            resultat["erreur"] = proc.stderr.strip()
            resultat["statut"] = "SYNTAXE_INVALIDE"
    except subprocess.TimeoutExpired:
        resultat["statut"] = "TIMEOUT"
        resultat["erreur"] = "Vérification trop longue"
    except Exception as e:
        resultat["statut"] = "ERREUR"
        resultat["erreur"] = str(e)

    return resultat


def run_verification_complete():
    """Lance la vérification de tous les agents."""
    print(f"\n{'═'*60}")
    print(f"  WATCHDOG — Vérification {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'═'*60}\n")

    sante = charger_sante()
    resultats = []
    ok = 0
    alertes = []

    for nom, config in AGENTS_SURVEILLES.items():
        r = verifier_agent(nom)
        resultats.append(r)

        icone = "✅" if r["statut"] == "OK" else ("🔴" if config["critique"] else "🟡")
        print(f"  {icone} {nom:<40} [{r['statut']}]")
        if r["erreur"]:
            print(f"     └─ {r['erreur']}")

        if r["statut"] == "OK":
            ok += 1
        elif config["critique"]:
            alertes.append(f"CRITIQUE: {nom} → {r['statut']} — {r['erreur']}")

    total = len(AGENTS_SURVEILLES)
    score = round(ok / total * 100)

    print(f"\n  ── BILAN ──")
    print(f"  Agents OK     : {ok}/{total} ({score}%)")
    print(f"  Alertes crit. : {len(alertes)}")

    # Stocker dans journal
    sante["derniere_verification"] = datetime.now().isoformat()
    sante["agents"] = {r["agent"]: r for r in resultats}
    sante["checks"].append({
        "timestamp": datetime.now().isoformat(),
        "ok": ok,
        "total": total,
        "score": score,
        "alertes": alertes,
    })
    # Garder seulement les 100 derniers checks
    sante["checks"] = sante["checks"][-100:]
    sauvegarder_sante(sante)

    if alertes:
        print(f"\n  🚨 ALERTES CRITIQUES :")
        for a in alertes:
            print(f"  → {a}")
        analyse_ia(alertes, ok, total)

    return score, alertes


def analyse_ia(alertes, ok, total):
    """Demande à l'IA d'analyser les pannes et proposer des actions."""
    print(f"\n{'─'*60}")
    print(f"  ► Analyse IA des pannes")
    print(f"{'─'*60}\n")

    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction="""Tu es l'ingénieur de fiabilité de Caelum Partners.
Tu analyses les pannes d'agents IA et proposes des actions correctives immédiates.
Sois bref, précis, actionnable. Chaque point = 1 action concrète.""",
        generation_config=genai.GenerationConfig(temperature=0.2, max_output_tokens=500),
    )
    try:
        for chunk in model.generate_content(
            f"Agents OK: {ok}/{total}\nAlertes: {chr(10).join(alertes)}\n\nActions correctives :",
            stream=True
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
    except Exception as e:
        print(f"[IA indisponible : {e}]")
    print()


def rapport_sante_ia():
    """Génère un rapport de santé global avec tendances."""
    sante = charger_sante()
    if not sante["checks"]:
        print("\n  Aucune donnée — lance une vérification d'abord.")
        return

    checks = sante["checks"][-10:]
    scores = [c["score"] for c in checks]
    tendance = "stable"
    if len(scores) >= 2:
        if scores[-1] > scores[0]:
            tendance = "en amélioration"
        elif scores[-1] < scores[0]:
            tendance = "en dégradation"

    print(f"\n{'═'*60}")
    print(f"  RAPPORT SANTÉ — {len(checks)} dernières vérifications")
    print(f"{'═'*60}\n")
    print(f"  Score moyen  : {round(sum(scores)/len(scores))}%")
    print(f"  Score actuel : {scores[-1]}%")
    print(f"  Tendance     : {tendance}")
    print(f"  Min / Max    : {min(scores)}% / {max(scores)}%\n")

    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction="Tu es le DSI de Caelum Partners. Analyse les données de santé et donne 3 recommandations prioritaires.",
        generation_config=genai.GenerationConfig(temperature=0.3, max_output_tokens=400),
    )
    try:
        for chunk in model.generate_content(
            f"Historique scores: {scores}\nTendance: {tendance}\nDernières alertes: {checks[-1].get('alertes',[])}",
            stream=True
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
    except Exception as e:
        print(f"[IA indisponible : {e}]")
    print()


def mode_continu(intervalle_minutes=30):
    """Boucle de surveillance continue — vérifie toutes les N minutes."""
    print(f"\n  Mode surveillance continue activé (toutes les {intervalle_minutes} min)")
    print(f"  Appuie sur Ctrl+C pour arrêter.\n")
    try:
        while True:
            score, alertes = run_verification_complete()
            prochaine = datetime.now() + timedelta(minutes=intervalle_minutes)
            print(f"\n  Prochaine vérification : {prochaine.strftime('%H:%M:%S')}")
            time.sleep(intervalle_minutes * 60)
    except KeyboardInterrupt:
        print("\n\n  Watchdog arrêté.")


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--continu" in sys.argv:
        intervalle = 30
        for arg in sys.argv:
            if arg.isdigit():
                intervalle = int(arg)
        mode_continu(intervalle)
        sys.exit(0)

    print("\n" + "═"*60)
    print("  AGENT WATCHDOG — Surveillance 24h/24")
    print("  Caelum Partners — Zéro panne tolérée")
    print("═"*60)

    while True:
        print("\n  1. Vérification complète maintenant")
        print("  2. Rapport de santé & tendances")
        print("  3. Mode surveillance continue (30 min)")
        print("  4. Mode surveillance rapide (5 min)")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            run_verification_complete()
        elif choix == "2":
            rapport_sante_ia()
        elif choix == "3":
            mode_continu(30)
        elif choix == "4":
            mode_continu(5)
        else:
            print("  Choix invalide.")
