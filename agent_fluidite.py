"""
AGENT FLUIDITÉ — Optimisateur zéro-friction
Détecte tout ce qui ralentit l'entreprise et l'élimine.
Maintient tout en état de flux parfait et sans effort.

Usage : python agent_fluidite.py
"""

import os
import sys
import json
from datetime import datetime
from google import genai
from google.genai import types
from memoire import charger_memoire, incrementer_stat

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] Variable GEMINI_API_KEY non définie. Exécutez : export GEMINI_API_KEY=votre_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

FLUIDITE_DIR = os.path.join("fichiers", "fluidite")
os.makedirs(FLUIDITE_DIR, exist_ok=True)

PROFIL_ENTREPRISE = """
Nom : AgentClaude Solutions
Spécialité : Automatisation par agents IA (Claude, Gemini)
Services :
  - Agents autonomes sur mesure pour entreprises
  - Migration et modernisation de code legacy
  - Sécurité et audit IA
  - Formation équipes sur agents IA
  - Orchestrateurs autonomes clé en main
Valeurs : Réactivité, transparence, excellence technique, accompagnement humain
"""


# ─── Utilitaires ──────────────────────────────────────────────

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


def creer_agent(instructions, temperature=0.4):
    return _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(
            temperature=temperature, max_output_tokens=4096
        ),
    )


def executer_stream(model, prompt, label):
    print(f"\n{'─' * 65}")
    print(f"  ► {label}")
    print(f"{'─' * 65}\n")
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


def sauvegarder_sortie(prefixe, contenu, contexte=""):
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"{prefixe}_{horodatage}.txt"
    chemin = os.path.join(FLUIDITE_DIR, nom_fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"AGENT FLUIDITÉ — {prefixe.replace('_', ' ').upper()}\n")
        f.write(f"Généré le : {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n")
        if contexte:
            f.write(f"Contexte : {contexte}\n")
        f.write("=" * 65 + "\n\n")
        f.write(contenu)
    print(f"\n  Rapport sauvegardé → {chemin}")
    return chemin


def extraire_resume_memoire(memoire):
    """Convertit la mémoire en résumé textuel structuré pour le prompt."""
    clients = memoire.get("clients", {})
    projets = memoire.get("projets", {})
    interactions = memoire.get("interactions", [])
    stats = memoire.get("stats", {})
    tickets = memoire.get("tickets", [])

    resume = []

    # Clients
    if clients:
        resume.append(f"CLIENTS ({len(clients)}) :")
        for nom, data in clients.items():
            nb_inter = len(data.get("interactions", []))
            statut = data.get("statut", "inconnu")
            resume.append(f"  - {nom} | statut: {statut} | interactions: {nb_inter} | secteur: {data.get('secteur','?')}")
    else:
        resume.append("CLIENTS : aucun enregistré.")

    # Projets
    if projets:
        resume.append(f"\nPROJETS ({len(projets)}) :")
        for nom, data in projets.items():
            resume.append(f"  - {nom} | statut: {data.get('statut','?')} | avancement: {data.get('avancement','?')}")
    else:
        resume.append("\nPROJETS : aucun enregistré.")

    # Interactions récentes
    if interactions:
        resume.append(f"\nINTERACTIONS RÉCENTES ({len(interactions)} au total, 10 dernières) :")
        for inter in interactions[-10:]:
            date = inter.get("date", "")[:10]
            client = inter.get("client", "?")
            action = inter.get("action", "?")
            resultat = inter.get("resultat", "")[:80]
            resume.append(f"  [{date}] {client} — {action} : {resultat}")
    else:
        resume.append("\nINTERACTIONS : aucune enregistrée.")

    # Tickets
    if tickets:
        resume.append(f"\nTICKETS ({len(tickets)} au total) :")
        urgences = {}
        for t in tickets:
            u = t.get("urgence", "INCONNUE")
            urgences[u] = urgences.get(u, 0) + 1
        for u, n in sorted(urgences.items()):
            resume.append(f"  - Urgence {u} : {n} ticket(s)")
    else:
        resume.append("\nTICKETS : aucun enregistré.")

    # Stats agents
    agents_utilises = stats.get("agents_utilises", {})
    if agents_utilises:
        resume.append(f"\nUSAGE AGENTS :")
        agents_tries = sorted(agents_utilises.items(), key=lambda x: x[1], reverse=True)
        for agent, nb in agents_tries[:8]:
            resume.append(f"  - {agent} : {nb} utilisation(s)")

    resume.append(f"\nTOTAL DEMANDES TRAITÉES : {stats.get('total_demandes', 0)}")

    return "\n".join(resume)


# ─── AGENT 1 : Détecteur de frictions ─────────────────────────

def agent_detecter_frictions():
    incrementer_stat("agent_fluidite")

    memoire = charger_memoire()
    resume_memoire = extraire_resume_memoire(memoire)

    agent = creer_agent(f"""Tu es l'Agent Anti-Friction — le lubrifiant de l'entreprise.
Tu analyses les données réelles de l'entreprise pour détecter tout ce qui freine, bloque ou ralentit.

Contexte entreprise :
{PROFIL_ENTREPRISE}

Ta mission : produire une CARTE DES FRICTIONS exhaustive et actionnables.

Pour chaque friction détectée, tu fournis :
1. **Nom de la friction** — titre court et percutant
2. **Score de sévérité** — de 1 (gêne) à 5 (blocage critique)
3. **Coût temps estimé** — heures perdues par semaine
4. **Symptômes observés** — ce que les données révèlent
5. **Plan d'élimination** — 3 actions concrètes pour la supprimer

Catégories à analyser :
- Processus lents (tickets qui traînent, délais répétés)
- Problèmes récurrents (même erreur qui revient)
- Lacunes de communication (clients non informés, agents non synchronisés)
- Goulots d'étranglement (concentration sur un seul agent/personne)
- Charge déséquilibrée (surcharge vs sous-utilisation)

Termine par un INDICE DE FLUIDITÉ GLOBAL (0 à 100) et la TOP 3 des frictions à éliminer en priorité absolue.

Ton ton : direct, médecin qui annonce un diagnostic — pas de détour, pas de ménagement, des faits et des solutions.""",
    temperature=0.3)

    prompt = f"""Voici les données réelles de l'entreprise à analyser :

{resume_memoire}

Analyse toutes ces données et génère la carte complète des frictions.
Si les données sont limitées, identifie quand même les frictions probables compte tenu du profil de l'entreprise
et signale clairement ce qui manque comme donnée pour un diagnostic plus précis."""

    reponse = executer_stream(agent, prompt, "Détection des frictions — analyse en cours...")

    sauvegarder_sortie("carte_frictions", reponse)
    return reponse


# ─── AGENT 2 : Simplificateur de processus ────────────────────

def agent_simplifier_processus(processus_decrit):
    incrementer_stat("agent_fluidite")

    agent = creer_agent(f"""Tu es l'Agent Simplificateur — l'ingénieur qui transforme le compliqué en élégant.
Tu reçois la description d'un processus actuel et tu le réinventes pour une simplicité maximale.

Contexte entreprise :
{PROFIL_ENTREPRISE}

Ta méthode en 4 filtres :
1. **ÉLIMINER** — Qu'est-ce qui peut disparaître entièrement sans perte de valeur ?
2. **AUTOMATISER** — Qu'est-ce qu'un agent IA peut faire à la place d'un humain ?
3. **PARALLÉLISER** — Qu'est-ce qui peut se faire simultanément plutôt que séquentiellement ?
4. **STANDARDISER** — Qu'est-ce qui peut devenir un template ou une règle fixe ?

Structure de ta réponse :

### PROCESSUS ACTUEL (tel que décrit)
- Cartographie des étapes
- Points de friction identifiés
- Durée estimée actuelle

### ANALYSE PAR FILTRE
Pour chaque filtre : ce qui s'applique et pourquoi.

### PROCESSUS REDESSINÉ
- Nouvelles étapes (seulement celles qui restent)
- Flux optimisé étape par étape
- Responsable de chaque étape (humain / agent / automatique)

### COMPARAISON AVANT / APRÈS
| Métrique | Avant | Après | Gain |
| Nombre d'étapes | X | Y | -Z% |
| Temps total | X | Y | -Z% |
| Interventions humaines | X | Y | -Z% |
| Risque d'erreur | Élevé/Moyen/Faible | ... | ... |

### ÉTAPES D'IMPLÉMENTATION
Actions concrètes pour passer de l'ancien au nouveau (dans l'ordre).

Ton ton : architecte logiciel — précis, pragmatique, zero bullshit.""",
    temperature=0.4)

    prompt = f"""Processus à simplifier :

{processus_decrit}

Applique les 4 filtres et génère le nouveau processus optimisé."""

    reponse = executer_stream(agent, prompt, f"Simplification du processus...")

    contexte_court = processus_decrit[:60].replace("\n", " ") + "..." if len(processus_decrit) > 60 else processus_decrit
    sauvegarder_sortie("simplification_processus", reponse, contexte_court)
    return reponse


# ─── AGENT 3 : Automatiseur de tâches ─────────────────────────

def agent_automatiser_tache(tache_repetitive):
    incrementer_stat("agent_fluidite")

    agent = creer_agent(f"""Tu es l'Agent Automatiseur — le spécialiste qui transforme toute tâche répétitive en machine autonome.
Tu conçois des spécifications d'automatisation complètes, prêtes à implémenter.

Contexte entreprise :
{PROFIL_ENTREPRISE}

Ta spécification d'automatisation couvre OBLIGATOIREMENT ces 8 dimensions :

1. **AGENT RESPONSABLE**
   - Quel type d'agent IA gère cette tâche ?
   - Nom fonctionnel, rôle, compétences requises

2. **DÉCLENCHEUR**
   - Qu'est-ce qui lance l'automatisation ? (événement / schedule / seuil / signal humain)
   - Conditions de déclenchement précises

3. **DONNÉES EN ENTRÉE**
   - Quelles informations l'agent a-t-il besoin ?
   - Sources de données, formats, accès requis

4. **TRAITEMENT ET LOGIQUE**
   - Ce que l'agent fait exactement, étape par étape
   - Règles de décision, priorités, logique conditionnelle

5. **SORTIE PRODUITE**
   - Ce que l'automatisation génère : document / email / action / alerte / mise à jour
   - Format, destination, qui est notifié

6. **CONTRÔLE QUALITÉ**
   - Comment vérifier que le résultat est correct ?
   - Critères de validation, score de confiance minimum, revue humaine si nécessaire

7. **GESTION DES EXCEPTIONS**
   - Que se passe-t-il si les données manquent ?
   - Que se passe-t-il si le résultat est incertain ?
   - Escalade humaine : quand et comment ?

8. **MÉTRIQUES DE PERFORMANCE**
   - Comment mesurer que l'automatisation fonctionne bien ?
   - KPIs à suivre, seuils d'alerte, fréquence de révision

Termine par : ESTIMATION DU ROI — temps économisé par semaine, coût d'implémentation estimé, retour sur investissement.

Ton ton : chef de projet technique — spec claire, sans ambiguïté, implémentable demain.""",
    temperature=0.3)

    prompt = f"""Tâche répétitive à automatiser :

{tache_repetitive}

Génère la spécification d'automatisation complète sur les 8 dimensions."""

    reponse = executer_stream(agent, prompt, "Conception de l'automatisation...")

    contexte_court = tache_repetitive[:60].replace("\n", " ") + "..." if len(tache_repetitive) > 60 else tache_repetitive
    sauvegarder_sortie("specification_automatisation", reponse, contexte_court)
    return reponse


# ─── AGENT 4 : Adaptateur de rythme ───────────────────────────

def agent_adapter_rythme(charge_actuelle, ressources, urgences):
    incrementer_stat("agent_fluidite")

    agent = creer_agent(f"""Tu es l'Agent Contrôleur Aérien — le coordinateur qui évite les collisions et maintient chaque vol sur sa trajectoire.
Tu gères la charge de travail en temps réel avec une précision chirurgicale.

Contexte entreprise :
{PROFIL_ENTREPRISE}

Face à la situation actuelle, tu génères un PLAN D'ACTION IMMÉDIAT structuré :

### DIAGNOSTIC DE CHARGE
- Évaluation de la surcharge (rouge/orange/vert par domaine)
- Risques si rien ne change dans les prochaines 24h

### RECLASSIFICATION PRIORITAIRE
Pour chaque tâche/projet identifié :
- **FAIRE MAINTENANT** — impact élevé + urgence réelle
- **PLANIFIER** — important mais peut attendre (avec date)
- **DÉLÉGUER** — qui d'autre peut le prendre ?
- **SUPPRIMER** — pas de valeur réelle, à abandonner

### AJUSTEMENTS DE PLANNING
- Nouvelles échéances réalistes (avec justification)
- Ce qui doit être renégocié avec les clients/parties prenantes
- Marges de sécurité à intégrer

### ALLOCATION D'ÉNERGIE
| Tâche | Énergie requise | Créneau optimal | Durée bloc |
(Haute concentration / Pilote automatique / Créatif / Relationnel)

### TÂCHES À BATCHER
Quelles tâches similaires regrouper pour un traitement en série efficace ?
(Ex : tous les emails d'un coup, toutes les révisions à la suite)

### PROGRAMME DE MICRO-PAUSES
- Quand s'arrêter pour maintenir la performance cognitive
- Durée et type de pause recommandée
- Signal d'alarme de surcharge à surveiller

### MÉTÉO DU LENDEMAIN
Prévision de charge pour les prochaines 24-48h et recommandations préventives.

Ton ton : contrôleur aérien — calme, précis, directif. Pas de panique, des solutions.""",
    temperature=0.4)

    prompt = f"""SITUATION ACTUELLE :

CHARGE DE TRAVAIL :
{charge_actuelle}

RESSOURCES DISPONIBLES :
{ressources}

URGENCES EN COURS :
{urgences}

Génère le plan d'adaptation immédiat."""

    reponse = executer_stream(agent, prompt, "Adaptation du rythme — calcul en cours...")

    sauvegarder_sortie("adaptation_rythme", reponse, f"Charge: {charge_actuelle[:40]}...")
    return reponse


# ─── AGENT 5 : Flux optimal ────────────────────────────────────

def agent_flux_optimal():
    incrementer_stat("agent_fluidite")

    memoire = charger_memoire()
    resume_memoire = extraire_resume_memoire(memoire)

    agent = creer_agent(f"""Tu es l'Agent Architecte du Flux — le designer de l'entreprise parfaite.
Tu conçois le système d'exploitation optimal de l'entreprise : comment tout doit s'organiser pour que tout coule naturellement.

Contexte entreprise :
{PROFIL_ENTREPRISE}

Tu génères un document complet : le "COMPANY OPERATING SYSTEM" — la constitution opérationnelle de l'entreprise.

Ce document couvre :

## 1. STRUCTURE DE LA SEMAINE PARFAITE
- Lundi au vendredi : quel type de travail chaque jour
- Créneaux par type : travail profond / réunions / admin / créatif / urgent
- Zones protégées (ne jamais programmer autre chose)
- Zones flexibles (adaptables selon les besoins)

## 2. RYTHMES DE TRAVAIL PAR TYPE
Pour chaque type de travail :
- **TRAVAIL PROFOND** : quand, durée de bloc, conditions requises, signaux de concentration
- **RÉUNIONS ET ÉCHANGES** : quand, durée max, fréquence, format (sync/async)
- **TÂCHES ADMIN** : quand, batch ou non, temps alloué
- **TRAVAIL CRÉATIF** : quand, environnement idéal, durée optimale
- **GESTION DES URGENCES** : buffer dédié, protocole de décision

## 3. PROTOCOLES DE PASSATION
- Agent → Agent : comment transmettre un dossier sans perte d'information
- Agent → Humain : quand escalader, quelle information passer, sous quel format
- Humain → Agent : comment briefer un agent pour résultat optimal
- En cas d'absence : protocole de remplacement et continuité

## 4. FLUX D'INFORMATION OPTIMISÉ
- Qui a besoin de savoir quoi, et quand ?
- Canaux par type d'information (urgent / FYI / décision / archive)
- Fréquence des points de synchronisation par équipe
- Ce qui ne mérite PAS d'être communiqué (règle du silence productif)

## 5. ACCÉLÉRATEUR DE DÉCISION
- Quelles décisions peuvent être prises par les agents sans validation humaine ?
- Seuils de décision autonome vs décision humaine requise
- Protocole de décision rapide pour les situations ambiguës
- Temps maximum acceptable pour chaque type de décision

## 6. INDICATEURS DE FLUX
- 5 signaux qui montrent que l'entreprise est en flux optimal
- 5 signaux d'alerte que le flux se dégrade
- Revue hebdomadaire : quoi vérifier, en combien de temps

## 7. RITUELS D'ENTRETIEN DU FLUX
- Daily : 1 action quotidienne pour maintenir le flux
- Weekly : revue hebdomadaire du système
- Monthly : audit et ajustement mensuel

Ton ton : architecte systèmes — visionnaire mais concret, chaque recommandation est implémentable.""",
    temperature=0.5)

    prompt = f"""Données actuelles de l'entreprise pour contextualiser le flux optimal :

{resume_memoire}

Génère le Company Operating System complet — le manuel d'opération de l'entreprise idéale."""

    reponse = executer_stream(agent, prompt, "Conception du flux optimal de l'entreprise...")

    sauvegarder_sortie("company_operating_system", reponse)
    return reponse


# ─── MENU PRINCIPAL ───────────────────────────────────────────

def saisir_multilignes(invite):
    """Saisie multiligne, terminée par une ligne vide."""
    print(f"\n  {invite}")
    print("  (Terminez avec une ligne vide)\n")
    lignes = []
    while True:
        ligne = input()
        if ligne == "":
            break
        lignes.append(ligne)
    return "\n".join(lignes).strip()


def menu():
    print("\n" + "═" * 65)
    print("  AGENT FLUIDITÉ — Optimisateur zéro-friction")
    print("  Détecte et élimine tout ce qui ralentit l'entreprise.")
    print("═" * 65)

    while True:
        print("\n  1. Détecter les frictions de l'entreprise")
        print("  2. Simplifier un processus")
        print("  3. Automatiser une tâche répétitive")
        print("  4. Adapter le rythme à la charge actuelle")
        print("  5. Concevoir le flux optimal de l'entreprise")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  Au revoir. Le flux continue.\n")
            break

        elif choix == "1":
            print("\n  Analyse de la mémoire d'entreprise en cours...")
            agent_detecter_frictions()

        elif choix == "2":
            processus = saisir_multilignes("Décrivez le processus actuel à simplifier :")
            if not processus:
                print("  Aucun processus décrit.")
                continue
            agent_simplifier_processus(processus)

        elif choix == "3":
            tache = saisir_multilignes("Décrivez la tâche répétitive à automatiser :")
            if not tache:
                print("  Aucune tâche décrite.")
                continue
            agent_automatiser_tache(tache)

        elif choix == "4":
            charge = saisir_multilignes("Décrivez la charge de travail actuelle (projets en cours, volume, délais) :")
            if not charge:
                print("  Charge non décrite.")
                continue
            ressources = saisir_multilignes("Ressources disponibles (agents actifs, temps humain, outils) :")
            if not ressources:
                ressources = "Non précisé — ressources standards de l'entreprise."
            urgences = saisir_multilignes("Urgences en cours (ce qui ne peut pas attendre) :")
            if not urgences:
                urgences = "Aucune urgence identifiée."
            agent_adapter_rythme(charge, ressources, urgences)

        elif choix == "5":
            print("\n  Conception du système d'exploitation optimal de l'entreprise...")
            agent_flux_optimal()

        else:
            print("  Choix invalide. Entrez un nombre entre 0 et 5.")


if __name__ == "__main__":
    menu()
