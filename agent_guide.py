"""
AGENT GUIDE — Sait toujours ce qu'il faut faire ensuite.
Il lit l'état complet de l'entreprise et te dit exactement
quoi faire, dans quel ordre, et pourquoi.

Usage : python agent_guide.py
"""

import os
import sys
import json
from datetime import datetime, timedelta
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

TOUS_LES_AGENTS = {
    "lancer.py":                "Menu principal — accès à tous les agents",
    "orchestrateur.py":         "Déléguer n'importe quelle tâche à l'IA",
    "agent_commercial.py":      "Prospects, propositions, relances clients",
    "agent_veille.py":          "Surveiller le marché et les concurrents",
    "agent_facturation.py":     "Créer factures, relancer paiements",
    "agent_recrutement.py":     "Fiches poste, analyser CV, entretiens",
    "agent_reference.py":       "Indexer et documenter tous les projets",
    "agent_seo.py":             "Référencement Google, articles blog",
    "agent_juridique.py":       "Contrats, CGV, RGPD, NDA",
    "agent_support_client.py":  "Répondre tickets, FAQ, onboarding clients",
    "agent_chef_projet.py":     "Planifier projets, gérer risques",
    "agent_kpi.py":             "Tableau de bord, alertes, prédictions",
    "agent_reputation.py":      "Avis clients, crise, LinkedIn",
    "agent_pricing.py":         "Calculer prix, préparer négociations",
    "agent_comptable.py":       "Comptabilité, TVA, optimisation fiscale",
    "agent_strategie.py":       "Plan stratégique, expansion, pitch",
    "agent_data.py":            "Analyser données, segmentation clients",
    "agent_veille_techno.py":   "Radar technologique, nouvelles IA",
    "agent_partenariats.py":    "Trouver partenaires, programme revendeurs",
    "agent_onboarding_employe.py": "Intégrer nouveaux employés",
    "agent_formation_equipe.py": "Former l'équipe, plans de développement",
    "agent_bienetre_equipe.py": "Bien-être, prévention burnout",
    "agent_fluidite.py":        "Éliminer frictions, optimiser flux",
    "agent_adaptation.py":      "S'adapter aux changements, retours expérience",
    "agent_jumeau_numerique.py": "Simuler décisions avant de les prendre",
    "agent_oracle.py":          "Prédire ce qui va se passer",
    "agent_innovation.py":      "Brainstorm radical, futurs possibles",
    "agent_ethique_ia.py":      "Audit éthique, conformité EU AI Act",
    "agent_memoire_collective.py": "Capitaliser leçons, sagesse organisationnelle",
    "securite.py":              "Auditer sécurité, protéger données",
    "usine_migration_logicielle.py": "Moderniser du code legacy",
}

# ─── ALGORITHME DE PRIORITÉ ───────────────────────────────────────────────────

ALGORITHME_PRIORITE = """
## ALGORITHME DE PRIORITÉ — GUIDE CAELUM PARTNERS

### RÈGLE 1 : SI 0 CLIENTS (phase actuelle)
Agents P0 (PRIORITÉ ABSOLUE — lancer EN PREMIER) :
  → agent_commercial.py : Prospects, scoring BANT, messages LinkedIn
  → agent_email.py : Cold emails, séquences de prospection
  → agent_growth.py : Campagne semaine, connexions LinkedIn, posts viraux
Logique : Sans clients = sans revenus. TOUT le reste est secondaire.

### RÈGLE 2 : SI CLIENTS ACTIFS (phase suivante)
Agents P0 (une fois le premier client signé) :
  → agent_support_client.py : Tickets, FAQ, satisfaction client
  → agent_crm.py : Suivi, relances, pipeline
  → agent_facturation.py : Créer factures, relancer paiements en retard
Logique : Les clients existants génèrent des revenus récurrents et des références.

### RÈGLE 3 : SI INCERTITUDE LÉGALE / FINANCIÈRE
Agents P0 (avant toute signature ou déclaration) :
  → agent_auditeur_financier.py : Cumul ONEM, seuils, simulation contrats
  → agent_comptable_belge.py : BCE, TVA, factures conformes
Logique : Une erreur légale peut coûter des milliers d'euros de remboursement ONEM.

### RÈGLE 4 : SIGNAUX D'ALARME
- Prospect chaud identifié → lancer agent_commercial.py MAINTENANT
- Seuil ONEM à moins de 20% → lancer agent_auditeur_financier.py MAINTENANT
- Facture en retard > 15 jours → lancer agent_facturation.py MAINTENANT
- 0 post LinkedIn depuis 7 jours → lancer agent_growth.py MAINTENANT

### RÈGLE 5 : ORDRE DU MATIN (routine quotidienne recommandée)
1. Vérifier briefing_matinal() → savoir les urgences du jour
2. Si prospects en attente → agent_commercial.py (répondre dans les 24h)
3. Post LinkedIn du jour → agent_growth.py (cohérence = algorithme)
4. Tâches administratives → agent_comptable_belge.py ou agent_facturation.py
"""

# ─── FICHIERS JSON DE MÉMOIRE ─────────────────────────────────────────────────
FICHIERS_MEMOIRE = {
    "memoire_entreprise.json": "Clients, factures, tickets, projets, interactions, stats agents",
    "crm_pipeline.json": "Pipeline commercial : prospects, étapes, valeurs, dates",
    "historique_caelum.json": "Historique complet des actions Caelum Partners",
}


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
    return {"clients": {}, "factures": {}, "tickets": [], "projets": {}, "interactions": [], "stats": {}}


def streamer(instructions, prompt, label=""):
    if label:
        print(f"\n{'═'*60}\n  {label}\n{'═'*60}\n")
    model = _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=3000),
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


def construire_etat_entreprise():
    """Construit un état complet de l'entreprise depuis la mémoire."""
    m = charger_memoire()
    maintenant = datetime.now()

    # Clients
    clients_actifs = [n for n, d in m.get("clients", {}).items() if d.get("statut") == "actif"]
    prospects = [n for n, d in m.get("clients", {}).items() if d.get("statut") == "prospect"]

    # Factures en retard
    factures_retard = []
    for fid, f in m.get("factures", {}).items():
        if f.get("statut") == "en_attente":
            try:
                echeance = datetime.fromisoformat(f.get("echeance", maintenant.isoformat()))
                if echeance < maintenant:
                    jours = (maintenant - echeance).days
                    factures_retard.append(f"{fid} ({jours}j de retard)")
            except Exception:
                pass

    # Tickets ouverts
    tickets_ouverts = [t for t in m.get("tickets", []) if t.get("statut") != "resolu"]
    tickets_critiques = [t for t in tickets_ouverts if t.get("urgence") == "CRITIQUE"]

    # Projets sans update
    projets_silencieux = []
    for nom, p in m.get("projets", {}).items():
        derniere_maj = p.get("derniere_maj", "")
        if derniere_maj:
            try:
                delta = maintenant - datetime.fromisoformat(derniere_maj)
                if delta.days > 7:
                    projets_silencieux.append(f"{nom} ({delta.days}j sans update)")
            except Exception:
                pass

    # Agents jamais utilisés
    stats_agents = m.get("stats", {}).get("agents_utilises", {})
    agents_jamais_utilises = [a for a in TOUS_LES_AGENTS if a not in stats_agents]

    return {
        "clients_actifs": clients_actifs,
        "prospects": prospects,
        "factures_retard": factures_retard,
        "tickets_critiques": tickets_critiques,
        "tickets_ouverts_count": len(tickets_ouverts),
        "projets_silencieux": projets_silencieux,
        "total_interactions": len(m.get("interactions", [])),
        "agents_jamais_utilises": agents_jamais_utilises[:10],
        "top_agents": sorted(stats_agents.items(), key=lambda x: x[1], reverse=True)[:5],
    }


# ─────────────────────────────────────────────────────────────
# AGENT 1 : PROCHAIN PAS — Ce qu'il faut faire MAINTENANT
# ─────────────────────────────────────────────────────────────

def agent_prochain_pas():
    etat = construire_etat_entreprise()

    streamer(
        """Tu es le conseiller stratégique de l'entreprise. Tu lis l'état complet
et tu dis EXACTEMENT quoi faire dans les prochaines 2 heures.

Format de réponse :
🔴 URGENT (à faire dans l'heure)
🟠 IMPORTANT (à faire aujourd'hui)
🟡 À PLANIFIER (cette semaine)

Pour chaque action : action précise + quel agent utiliser + pourquoi maintenant.
Sois direct, pas de blabla. Maximum 10 actions au total.""",
        f"""État de l'entreprise :
- Clients actifs : {etat['clients_actifs'] or 'aucun'}
- Prospects sans relance : {etat['prospects'] or 'aucun'}
- Factures en retard : {etat['factures_retard'] or 'aucune'}
- Tickets critiques : {len(etat['tickets_critiques'])} | Tickets ouverts : {etat['tickets_ouverts_count']}
- Projets sans update >7j : {etat['projets_silencieux'] or 'aucun'}
- Agents jamais utilisés : {etat['agents_jamais_utilises'][:5]}

Agents disponibles :
{chr(10).join(f'→ {k} : {v}' for k, v in TOUS_LES_AGENTS.items())}""",
        "PROCHAIN PAS — Ce qu'il faut faire maintenant"
    )


# ─────────────────────────────────────────────────────────────
# AGENT 2 : AGENDA INTELLIGENT — La journée parfaite
# ─────────────────────────────────────────────────────────────

def agent_agenda_intelligent():
    etat = construire_etat_entreprise()
    jour = datetime.now().strftime("%A %d %B %Y")

    streamer(
        """Tu es un coach de productivité expert. Tu construis l'agenda parfait
pour la journée en tenant compte de l'énergie humaine, des urgences,
et des objectifs long terme.

Format :
08h00 - 09h00 : [activité] → [agent à utiliser si applicable]
...

Règles :
- Tâches cognitives importantes le matin
- Réunions/emails en début d'après-midi
- Tâches créatives en fin de journée
- 1 pause toutes les 90 minutes
- Finir par une revue du lendemain""",
        f"""Journée : {jour}
État entreprise : {json.dumps(etat, ensure_ascii=False, indent=2)}
Agents disponibles : {list(TOUS_LES_AGENTS.keys())}""",
        f"AGENDA INTELLIGENT — {jour}"
    )


# ─────────────────────────────────────────────────────────────
# AGENT 3 : GUIDE CONVERSATIONNEL — Répond à "par où commencer ?"
# ─────────────────────────────────────────────────────────────

def agent_guide_conversationnel():
    etat = construire_etat_entreprise()
    historique = []

    print("\n" + "═"*60)
    print("  GUIDE IA — Je sais exactement ce que tu dois faire")
    print("  Pose-moi n'importe quelle question sur ton entreprise.")
    print("  Tape 'quitter' pour arrêter.")
    print("═"*60)

    system = f"""Tu es le conseiller omniscient de Caelum Partners (Chaima Mhadbi, Bruxelles).
Tu connais TOUS les agents disponibles et l'état complet de l'entreprise.
Tu guides toujours vers une action concrète avec le bon agent.

ALGORITHME DE PRIORITÉ :
{ALGORITHME_PRIORITE}

Agents disponibles :
{chr(10).join(f'• {k} : {v}' for k, v in TOUS_LES_AGENTS.items())}

État actuel :
- Clients actifs : {etat['clients_actifs'] or 'AUCUN — objectif = premier client ASAP'}
- Prospects : {etat['prospects'] or 'Aucun prospect enregistré'}
- Urgences : factures en retard={etat['factures_retard']}, tickets critiques={len(etat['tickets_critiques'])}

Règles :
- Si 0 clients → TOUJOURS suggérer agent_commercial.py ou agent_growth.py EN PREMIER
- Toujours terminer par "Lance : python [agent.py]" quand applicable
- Être concis et actionnable (réponse max 150 mots)
- Si plusieurs options, donner la meilleure en premier selon l'algorithme de priorité"""

    model = _creer_model(
        model_name=MODEL,
        system_instruction=system,
        generation_config=types.GenerateContentConfig(temperature=0.4, max_output_tokens=500),
    )

    while True:
        question = input("\n  Toi → ").strip()
        if question.lower() in ["quitter", "quit", "exit"]:
            break
        if not question:
            continue

        historique.append({"role": "user", "parts": [question]})
        chat = model.start_chat(history=historique[:-1])

        print("\n  Guide → ", end="", flush=True)
        reponse = ""
        try:
            for chunk in chat.send_message(question, stream=True):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    reponse += chunk.text
        except Exception as e:
            print(f"[Erreur : {e}]")
        print()

        historique.append({"role": "model", "parts": [reponse]})


# ─────────────────────────────────────────────────────────────
# AGENT 4 : SÉQUENCEUR — Plan d'action sur 30/90 jours
# ─────────────────────────────────────────────────────────────

def agent_sequenceur(objectif, horizon_jours=30):
    etat = construire_etat_entreprise()

    streamer(
        f"""Tu es un expert en planification stratégique opérationnelle.
Tu crées un plan d'action séquencé sur {horizon_jours} jours.

Format par semaine :
SEMAINE 1 (J1-J7) :
  • Action 1 → Agent : [agent.py] → Résultat attendu
  • Action 2 → ...
  Objectif de la semaine : ...
  Indicateur de succès : ...

Chaque action doit être :
- Concrète et mesurable
- Liée à un agent spécifique
- Dans le bon ordre (les fondations avant la croissance)""",
        f"""Objectif : {objectif}
Horizon : {horizon_jours} jours
État actuel : {json.dumps(etat, ensure_ascii=False)}
Tous les agents disponibles : {chr(10).join(f'→ {k}' for k in TOUS_LES_AGENTS.keys())}""",
        f"SÉQUENCEUR — Plan {horizon_jours} jours : {objectif}"
    )


# ─────────────────────────────────────────────────────────────
# AGENT 5 : RÉVEIL QUOTIDIEN — Le briefing du matin
# ─────────────────────────────────────────────────────────────

def agent_reveil_quotidien():
    etat = construire_etat_entreprise()
    heure = datetime.now().strftime("%H:%M")
    jour = datetime.now().strftime("%A %d %B")

    streamer(
        """Tu es l'assistant personnel qui prépare le dirigeant chaque matin.
Ton briefing est :
- Chaleureux mais efficace
- Commence par les urgences critiques
- Continue avec les opportunités du jour
- Termine par une intention/focus pour la journée
- Maximum 300 mots
- Toujours terminer par "Bonne journée !" """,
        f"""Heure : {heure} | Jour : {jour}
État entreprise : {json.dumps(etat, ensure_ascii=False, indent=2)}""",
        f"RÉVEIL QUOTIDIEN — {jour}"
    )



# ─────────────────────────────────────────────────────────────
# AGENT 6 : BRIEFING MATINAL — Lire tous les JSON et résumer
# ─────────────────────────────────────────────────────────────

def briefing_matinal():
    """Lit tous les fichiers JSON de mémoire et génère un briefing complet du matin."""
    heure = datetime.now().strftime("%H:%M")
    jour = datetime.now().strftime("%A %d %B %Y")

    # Charger tous les fichiers JSON disponibles
    donnees = {}
    for fichier, description in FICHIERS_MEMOIRE.items():
        try:
            if os.path.exists(fichier):
                with open(fichier, "r", encoding="utf-8") as f:
                    donnees[fichier] = json.load(f)
            else:
                donnees[fichier] = {"statut": "fichier non trouvé", "description": description}
        except Exception as e:
            donnees[fichier] = {"erreur": str(e)}

    # Aussi charger memoire_entreprise.json via la fonction existante
    etat = construire_etat_entreprise()

    # Analyser ce qui s'est passé hier
    hier = datetime.now()
    interactions_recentes = []
    try:
        m = donnees.get("memoire_entreprise.json", {})
        for interaction in m.get("interactions", [])[-10:]:
            interactions_recentes.append(interaction)
    except Exception:
        pass

    instructions = f"""Tu es l'assistant personnel de Chaima Mhadbi (Caelum Partners, Bruxelles).
Tu prépares son briefing du matin. Tu connais l'algorithme de priorité suivant :

{ALGORITHME_PRIORITE}

Tu connais tous les agents disponibles :
{chr(10).join(f'• {k} : {v}' for k, v in TOUS_LES_AGENTS.items())}

TON BRIEFING DOIT COUVRIR :
1. CE QUI S'EST PASSÉ HIER (interactions récentes, nouveaux prospects, factures)
2. URGENCES DU JOUR (en rouge) — ce qui ne peut pas attendre
3. PRIORITÉS DU JOUR (en orange) — les 3 actions les plus importantes
4. PLAN D'ACTION SUGGÉRÉ (quel agent lancer en premier, pourquoi)
5. SIGNAL D'ALARME si risque ONEM, facture en retard, ou prospect chaud non relancé
6. INTENTION DU JOUR — 1 focus pour rester dans le bon état d'esprit

Format : chaleureux mais efficace. Maximum 400 mots. Toujours terminer par le premier agent à lancer.
"""

    streamer(
        instructions,
        f"""Heure : {heure} | Jour : {jour}
État entreprise (depuis mémoire) : {json.dumps(etat, ensure_ascii=False, indent=2)}
Fichiers JSON disponibles : {json.dumps({k: "chargé" if "erreur" not in v and "statut" not in v else v for k, v in donnees.items()}, ensure_ascii=False)}
Interactions récentes (10 dernières) : {json.dumps(interactions_recentes, ensure_ascii=False)}
Clients actifs : {etat['clients_actifs'] or 'AUCUN — Phase acquisition'}
Prospects en cours : {etat['prospects'] or 'Aucun prospect enregistré'}
Factures en retard : {etat['factures_retard'] or 'Aucune'}""",
        f"BRIEFING MATINAL — {jour} à {heure}"
    )


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  AGENT GUIDE — Sait toujours ce qu'il faut faire")
    print("═"*60)

    while True:
        print("\n  1. Prochain pas — Ce qu'il faut faire MAINTENANT")
        print("  2. Agenda intelligent — Ma journée parfaite")
        print("  3. Guide conversationnel — Pose ta question")
        print("  4. Séquenceur — Plan d'action 30/90 jours")
        print("  5. Réveil quotidien — Briefing du matin")
        print("  6. Briefing matinal intelligent — lit tous les JSON + priorités")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            agent_prochain_pas()
        elif choix == "2":
            agent_agenda_intelligent()
        elif choix == "3":
            agent_guide_conversationnel()
        elif choix == "4":
            obj = input("  Objectif → ").strip()
            h = input("  Horizon (30/90/180 jours) → ").strip()
            agent_sequenceur(obj, int(h) if h.isdigit() else 30)
        elif choix == "5":
            agent_reveil_quotidien()
        elif choix == "6":
            briefing_matinal()
        else:
            print("  Choix invalide.")
