"""
MÉMOIRE PERSISTANTE — Système de contexte inter-sessions
Chaque agent se souvient des clients, projets et interactions passées.
"""

import json
import os
from datetime import datetime

MEMOIRE_FILE = "memoire_entreprise.json"


def charger_memoire():
    if os.path.exists(MEMOIRE_FILE):
        with open(MEMOIRE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "clients": {},
        "projets": {},
        "interactions": [],
        "knowledge_base": [],
        "stats": {"total_demandes": 0, "agents_utilises": {}},
    }


def sauvegarder_memoire(memoire):
    with open(MEMOIRE_FILE, "w", encoding="utf-8") as f:
        json.dump(memoire, f, ensure_ascii=False, indent=2)


def ajouter_client(nom, secteur, besoin, contact=""):
    m = charger_memoire()
    m["clients"][nom] = {
        "secteur": secteur,
        "besoin_principal": besoin,
        "contact": contact,
        "date_ajout": datetime.now().isoformat(),
        "interactions": [],
        "statut": "prospect",
    }
    sauvegarder_memoire(m)
    print(f"  ✅ Client '{nom}' ajouté en mémoire.")


def ajouter_interaction(client, type_action, resultat):
    m = charger_memoire()
    entree = {
        "date": datetime.now().isoformat(),
        "client": client,
        "action": type_action,
        "resultat": resultat[:200],
    }
    m["interactions"].append(entree)
    if client in m["clients"]:
        m["clients"][client]["interactions"].append(entree)
        m["clients"][client]["statut"] = "actif"
    sauvegarder_memoire(m)


def obtenir_contexte_client(nom):
    m = charger_memoire()
    if nom in m["clients"]:
        c = m["clients"][nom]
        return f"Client: {nom} | Secteur: {c['secteur']} | Besoin: {c['besoin_principal']} | Statut: {c['statut']} | Interactions: {len(c['interactions'])}"
    return "Nouveau client — aucun historique."


def lister_clients():
    m = charger_memoire()
    if not m["clients"]:
        print("  Aucun client en mémoire.")
        return
    print(f"\n  {'NOM':<20} {'SECTEUR':<15} {'STATUT':<12} {'INTERACTIONS'}")
    print("  " + "─" * 60)
    for nom, data in m["clients"].items():
        print(f"  {nom:<20} {data['secteur']:<15} {data['statut']:<12} {len(data['interactions'])}")


def incrementer_stat(agent_nom):
    m = charger_memoire()
    m["stats"]["total_demandes"] += 1
    m["stats"]["agents_utilises"][agent_nom] = m["stats"]["agents_utilises"].get(agent_nom, 0) + 1
    sauvegarder_memoire(m)
