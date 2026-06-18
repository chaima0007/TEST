"""
AGENT AUTOPILOT — Cerveau autonome de Caelum Partners
Tourne en boucle 24h/24, analyse l'état de l'entreprise,
décide seul des actions prioritaires et les exécute.

Usage : python agent_autopilot.py          (un cycle)
        python agent_autopilot.py --loop   (boucle infinie)
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

LOG_FILE = "autopilot_log.json"


def charger_tout():
    """Charge toutes les sources de données disponibles."""
    donnees = {}
    for fichier, cle in [
        ("memoire_entreprise.json", "memoire"),
        ("crm_pipeline.json", "pipeline"),
        ("historique_caelum.json", "historique"),
        ("watchdog_sante.json", "sante"),
    ]:
        if os.path.exists(fichier):
            try:
                with open(fichier, "r", encoding="utf-8") as f:
                    donnees[cle] = json.load(f)
            except Exception:
                donnees[cle] = {}
        else:
            donnees[cle] = {}
    return donnees


def charger_log():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"cycles": [], "actions_totales": 0, "derniere_action": ""}


def sauvegarder_log(log):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def sauvegarder_action(titre, contenu):
    """Sauvegarde une action générée dans fichiers/autopilot/"""
    os.makedirs("fichiers/autopilot", exist_ok=True)
    horodatage = datetime.now().strftime("%Y%m%d_%H%M")
    nom = f"fichiers/autopilot/{titre.replace(' ','_')[:30]}_{horodatage}.txt"
    with open(nom, "w", encoding="utf-8") as f:
        f.write(f"AUTOPILOT — {titre}\n")
        f.write(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n")
        f.write("="*60 + "\n\n")
        f.write(contenu)
    return nom


def streamer_silencieux(instructions, prompt):
    """Génère du contenu sans affichage en temps réel."""
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(temperature=0.3, max_output_tokens=2000),
    )
    try:
        reponse = model.generate_content(prompt)
        return reponse.text
    except Exception as e:
        return f"[Erreur : {e}]"


def streamer(instructions, prompt, label=""):
    if label:
        print(f"\n  ► {label}")
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(temperature=0.3, max_output_tokens=2500),
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


def analyser_situation(donnees):
    """L'IA analyse la situation et décide les 3 actions prioritaires."""
    m = donnees.get("memoire", {})
    p = donnees.get("pipeline", {})
    h = donnees.get("historique", {})

    clients = list(m.get("clients", {}).keys())
    leads = p.get("leads", {})
    tickets = [t for t in m.get("tickets", []) if t.get("statut") != "resolu"]
    factures_attente = [f for f in m.get("factures", {}).values() if f.get("statut") == "en_attente"]
    milestones_attente = [mi for mi in h.get("milestones", []) if mi.get("statut") == "en_attente"]

    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction="""Tu es l'IA autonome de Caelum Partners.
Tu analyses la situation et décides les 3 actions à exécuter MAINTENANT.
Réponds en JSON uniquement :
{
  "analyse": "1 phrase sur la situation actuelle",
  "actions": [
    {"id": 1, "titre": "...", "type": "email|proposition|relance|contenu|strategie", "priorite": "CRITIQUE|HAUTE|NORMALE", "pourquoi": "..."},
    {"id": 2, ...},
    {"id": 3, ...}
  ],
  "objectif_semaine": "..."
}""",
        generation_config=genai.GenerationConfig(temperature=0.2, max_output_tokens=800),
    )
    try:
        r = model.generate_content(f"""
Situation Caelum Partners :
- Clients actifs : {clients or 'AUCUN — premier client urgent'}
- Leads pipeline : {len(leads)} leads
- Tickets ouverts : {len(tickets)}
- Factures en attente : {len(factures_attente)} ({sum(f.get('montant',0) for f in factures_attente)}€)
- Milestones en attente : {[m['etape'] for m in milestones_attente[:3]]}
- Services : Site web 500€ / Automation 1500€ / Pack 3000€
- LinkedIn : actif
- Site : caelumpartners.agency (en ligne)
""")
        texte = r.text.strip()
        debut = texte.find("{"); fin = texte.rfind("}") + 1
        return json.loads(texte[debut:fin])
    except Exception:
        return {
            "analyse": "Démarrage — priorité acquisition premier client",
            "actions": [
                {"id": 1, "titre": "Cold email prospects LinkedIn", "type": "email", "priorite": "CRITIQUE", "pourquoi": "Aucun client encore"},
                {"id": 2, "titre": "Proposition site web 500€", "type": "proposition", "priorite": "HAUTE", "pourquoi": "Service d'entrée de gamme"},
                {"id": 3, "titre": "Stratégie contenu LinkedIn", "type": "contenu", "priorite": "NORMALE", "pourquoi": "Visibilité marché"},
            ],
            "objectif_semaine": "Obtenir le premier rendez-vous client"
        }


def executer_action(action, donnees):
    """Exécute une action autonome et retourne le livrable."""
    type_action = action.get("type", "")
    titre = action.get("titre", "")
    print(f"\n  ⚙  Exécution : {titre}")

    if type_action == "email":
        contenu = streamer_silencieux(
            """Tu es le meilleur commercial de Caelum Partners.
Génère 3 cold emails LinkedIn prêts à envoyer à des dirigeants de PME belges.
Pour chaque email : [Prénom], objet, corps (max 100 mots), signature.
Cible : dirigeants PME, startups tech, responsables marketing Belgique.""",
            f"Action : {titre}\nServices : Site web 500€ en 7 jours / Automation IA 1500€\nSignature : Chaima Mhadbi — Caelum Partners | contact@caelumpartners.agency"
        )

    elif type_action == "proposition":
        contenu = streamer_silencieux(
            """Tu es expert en propositions commerciales B2B.
Génère une proposition commerciale complète pour un site web premium à 500€.
Include : contexte, solution, livrables, timeline, prix, garanties, FAQ, CTA.""",
            "Service : Site web premium 500€ livré en 7 jours | Caelum Partners | caelumpartners.agency"
        )

    elif type_action == "relance":
        leads = donnees.get("pipeline", {}).get("leads", {})
        leads_list = [f"{l['nom']} ({l.get('stage','')})" for l in leads.values()]
        contenu = streamer_silencieux(
            "Tu es commercial expert. Génère des messages de relance personnalisés pour chaque lead.",
            f"Leads à relancer : {leads_list}\nService : Site web 500€\nSignature : Chaima — Caelum Partners"
        )

    elif type_action == "contenu":
        contenu = streamer_silencieux(
            """Tu es expert content marketing B2B.
Génère 5 posts LinkedIn viraux pour Caelum Partners.
Formats variés : storytelling, tips, résultats clients, coulisses, question engageante.
Chaque post : accroche + corps + hashtags + CTA.""",
            "Entreprise : Caelum Partners | IA & automatisation pour PME | Bruxelles | caelumpartners.agency"
        )

    elif type_action == "strategie":
        contenu = streamer_silencieux(
            """Tu es stratège growth hacker.
Génère un plan de croissance sur 30 jours pour obtenir les 10 premiers clients.
Inclure : canaux, messages, timing, métriques, actions quotidiennes.""",
            "Caelum Partners — Site web 500€ / Automation 1500€ / Pack 3000€ | Belgique | LinkedIn actif"
        )
    else:
        contenu = streamer_silencieux(
            "Tu es conseiller stratégique. Produis un livrable actionnable pour cette action.",
            f"Action : {titre} | Caelum Partners"
        )

    fichier = sauvegarder_action(titre, contenu)
    print(f"  ✅ Sauvegardé → {fichier}")
    return contenu, fichier


def cycle_autonome():
    """Un cycle complet d'analyse et d'action autonome."""
    maintenant = datetime.now()
    print(f"\n{'═'*65}")
    print(f"  AUTOPILOT — Cycle {maintenant.strftime('%d/%m/%Y %H:%M')}")
    print(f"  Caelum Partners — Mode autonome")
    print(f"{'═'*65}")

    # 1. Charger toutes les données
    print(f"\n  Analyse de la situation...")
    donnees = charger_tout()

    # 2. L'IA décide des actions
    decision = analyser_situation(donnees)
    print(f"\n  Situation : {decision.get('analyse','')}")
    print(f"  Objectif semaine : {decision.get('objectif_semaine','')}")
    print(f"\n  Actions décidées par l'IA :")
    for a in decision.get("actions", []):
        print(f"  [{a['priorite']}] {a['titre']} — {a['pourquoi']}")

    # 3. Exécuter les actions
    actions_log = []
    for action in decision.get("actions", []):
        contenu, fichier = executer_action(action, donnees)
        actions_log.append({
            "titre": action["titre"],
            "type": action["type"],
            "priorite": action["priorite"],
            "fichier": fichier,
            "timestamp": maintenant.isoformat(),
        })

    # 4. Logger le cycle
    log = charger_log()
    log["cycles"].append({
        "timestamp": maintenant.isoformat(),
        "analyse": decision.get("analyse", ""),
        "actions": actions_log,
        "objectif": decision.get("objectif_semaine", ""),
    })
    log["cycles"] = log["cycles"][-50:]
    log["actions_totales"] += len(actions_log)
    log["derniere_action"] = maintenant.isoformat()
    sauvegarder_log(log)

    print(f"\n{'═'*65}")
    print(f"  Cycle terminé — {len(actions_log)} actions exécutées")
    print(f"  Total actions depuis démarrage : {log['actions_totales']}")
    print(f"  Livrables dans : fichiers/autopilot/")
    print(f"{'═'*65}\n")

    return actions_log


def voir_historique():
    """Affiche l'historique des cycles autonomes."""
    log = charger_log()
    if not log["cycles"]:
        print("\n  Aucun cycle exécuté encore.")
        return
    print(f"\n  Total actions : {log['actions_totales']} | Dernière : {log.get('derniere_action','')[:16]}\n")
    for cycle in reversed(log["cycles"][-10:]):
        print(f"  [{cycle['timestamp'][:16]}] {cycle['analyse'][:60]}")
        for a in cycle.get("actions", []):
            print(f"     → {a['titre']}")


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--loop" in sys.argv:
        intervalle = 60
        for arg in sys.argv:
            if arg.isdigit():
                intervalle = int(arg)
        print(f"\n  Mode autonome activé — cycle toutes les {intervalle} minutes")
        print(f"  Ctrl+C pour arrêter\n")
        try:
            while True:
                cycle_autonome()
                print(f"  Prochain cycle dans {intervalle} minutes...")
                time.sleep(intervalle * 60)
        except KeyboardInterrupt:
            print("\n  Autopilot arrêté.")
        sys.exit(0)

    print("\n" + "═"*65)
    print("  AGENT AUTOPILOT — Cerveau autonome Caelum Partners")
    print("  Analyse, décide et agit seul")
    print("═"*65)

    while True:
        print("\n  1. Lancer un cycle autonome maintenant")
        print("  2. Mode boucle — tourne toutes les 60 minutes")
        print("  3. Mode boucle rapide — toutes les 15 minutes")
        print("  4. Voir l'historique des cycles")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            cycle_autonome()
        elif choix == "2":
            try:
                while True:
                    cycle_autonome()
                    print("  Prochain cycle dans 60 minutes...")
                    time.sleep(3600)
            except KeyboardInterrupt:
                print("\n  Arrêté.")
        elif choix == "3":
            try:
                while True:
                    cycle_autonome()
                    print("  Prochain cycle dans 15 minutes...")
                    time.sleep(900)
            except KeyboardInterrupt:
                print("\n  Arrêté.")
        elif choix == "4":
            voir_historique()
        else:
            print("  Choix invalide.")
