"""
AGENT KPI & TABLEAU DE BORD — AgentClaude Solutions
Système nerveux central de l'entreprise : lit toutes les données des agents
et fournit une vue santé en temps réel.

Usage : python agent_kpi.py
"""

import os
import sys
import json
from datetime import datetime, timedelta
from google import genai
from google.genai import types

from memoire import charger_memoire, incrementer_stat

# ─── Configuration ────────────────────────────────────────────
API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] Variable GEMINI_API_KEY non définie. Exécutez : export GEMINI_API_KEY=votre_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

ENTREPRISE = "AgentClaude Solutions"
KPI_DIR = os.path.join("fichiers", "kpi")
os.makedirs(KPI_DIR, exist_ok=True)

LARGEUR = 70


# ═══════════════════════════════════════════════════════════════
# UTILITAIRES
# ═══════════════════════════════════════════════════════════════

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


def _sep(car="═", n=LARGEUR):
    return car * n


def _titre(texte, car="═"):
    return f"\n{_sep(car)}\n  {texte}\n{_sep(car)}"


def _barre_ascii(valeur, maxi, largeur=30, car_plein="█", car_vide="░"):
    """Génère une barre ASCII proportionnelle."""
    if maxi == 0:
        rempli = 0
    else:
        rempli = int((valeur / maxi) * largeur)
    rempli = min(rempli, largeur)
    vide = largeur - rempli
    return f"[{car_plein * rempli}{car_vide * vide}]"


def _streamer(prompt: str, temperature: float = 0.5) -> str:
    """Appelle Gemini en streaming et retourne le texte complet."""
    modele = _creer_model(
        model_name=MODEL,
        generation_config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=4096,
        ),
    )
    print()
    texte = ""
    for chunk in modele.generate_content(prompt, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            texte += chunk.text
    print("\n")
    return texte


def _sauvegarder_rapport(nom_fichier: str, contenu: str) -> str:
    """Sauvegarde un rapport dans fichiers/kpi/ et retourne le chemin."""
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = os.path.join(KPI_DIR, f"{nom_fichier}_{horodatage}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


def _jours_depuis(date_str: str) -> int:
    """Calcule le nombre de jours depuis une date ISO."""
    try:
        date = datetime.fromisoformat(date_str)
        return (datetime.now() - date).days
    except Exception:
        return 0


def _extraire_metriques(memoire: dict) -> dict:
    """Extrait et calcule toutes les métriques depuis la mémoire."""
    clients = memoire.get("clients", {})
    factures = memoire.get("factures", [])
    tickets = memoire.get("tickets", [])
    projets = memoire.get("projets", {})
    interactions = memoire.get("interactions", [])
    stats = memoire.get("stats", {})
    now = datetime.now()

    # ── Clients ──
    nb_clients_actifs = sum(1 for c in clients.values() if c.get("statut") == "actif")
    nb_prospects = sum(1 for c in clients.values() if c.get("statut") == "prospect")
    nb_clients_total = len(clients)
    taux_conversion = (
        round(nb_clients_actifs / nb_clients_total * 100, 1)
        if nb_clients_total > 0 else 0
    )

    # ── Revenus ──
    revenus_encaisses = sum(f.get("total_ttc", 0) for f in factures if f.get("payee"))
    revenus_en_attente = sum(
        f.get("total_ttc", 0) for f in factures
        if not f.get("payee") and _statut_facture(f) == "EN ATTENTE"
    )
    revenus_en_retard = sum(
        f.get("total_ttc", 0) for f in factures
        if not f.get("payee") and _statut_facture(f) == "EN RETARD"
    )
    revenus_total = revenus_encaisses + revenus_en_attente + revenus_en_retard
    nb_factures_retard = sum(
        1 for f in factures
        if not f.get("payee") and _statut_facture(f) == "EN RETARD"
    )

    # ── Tickets ──
    nb_tickets = len(tickets)
    nb_tickets_resolus = sum(1 for t in tickets if t.get("resolu"))
    nb_tickets_ouverts = nb_tickets - nb_tickets_resolus
    nb_tickets_critiques = sum(
        1 for t in tickets
        if t.get("urgence") == "CRITIQUE" and not t.get("resolu")
    )
    nb_tickets_haute = sum(
        1 for t in tickets
        if t.get("urgence") == "HAUTE" and not t.get("resolu")
    )

    # ── Projets ──
    nb_projets = len(projets)
    nb_projets_en_cours = sum(
        1 for p in projets.values()
        if p.get("statut") not in ("terminé", "annulé")
    )
    nb_projets_termines = sum(
        1 for p in projets.values() if p.get("statut") == "terminé"
    )

    # ── Agents les plus utilisés ──
    agents_utilises = stats.get("agents_utilises", {})
    top_agents = sorted(agents_utilises.items(), key=lambda x: x[1], reverse=True)[:5]
    total_demandes = stats.get("total_demandes", 0)

    # ── Alertes ──
    alertes = []

    # Factures en retard >30j
    for f in factures:
        if not f.get("payee") and _statut_facture(f) == "EN RETARD":
            jours = _jours_depuis(f.get("date_echeance", ""))
            if jours > 30:
                client_nom = f.get("client", {}).get("nom", "Inconnu")
                alertes.append({
                    "niveau": "CRITIQUE",
                    "type": "facture_retard",
                    "message": f"Facture {f.get('numero')} ({client_nom}) — {jours}j de retard — {f.get('total_ttc', 0):.0f}€ TTC",
                })

    # Tickets critiques non résolus
    for t in tickets:
        if t.get("urgence") == "CRITIQUE" and not t.get("resolu"):
            alertes.append({
                "niveau": "CRITIQUE",
                "type": "ticket_critique",
                "message": f"Ticket {t.get('ref', '?')} CRITIQUE non résolu — {t.get('question', '')[:60]}...",
            })

    # Projets en retard
    for nom, p in projets.items():
        date_fin = p.get("date_fin") or p.get("echeance") or p.get("deadline")
        if date_fin and p.get("statut") not in ("terminé", "annulé"):
            try:
                df = datetime.fromisoformat(date_fin)
                if df < now:
                    jours_retard = (now - df).days
                    alertes.append({
                        "niveau": "HAUTE",
                        "type": "projet_retard",
                        "message": f"Projet '{nom}' en retard de {jours_retard}j (échéance : {df.strftime('%d/%m/%Y')})",
                    })
            except Exception:
                pass

    return {
        "nb_clients_actifs": nb_clients_actifs,
        "nb_prospects": nb_prospects,
        "nb_clients_total": nb_clients_total,
        "taux_conversion": taux_conversion,
        "revenus_encaisses": revenus_encaisses,
        "revenus_en_attente": revenus_en_attente,
        "revenus_en_retard": revenus_en_retard,
        "revenus_total": revenus_total,
        "nb_factures": len(factures),
        "nb_factures_retard": nb_factures_retard,
        "nb_tickets": nb_tickets,
        "nb_tickets_resolus": nb_tickets_resolus,
        "nb_tickets_ouverts": nb_tickets_ouverts,
        "nb_tickets_critiques": nb_tickets_critiques,
        "nb_tickets_haute": nb_tickets_haute,
        "nb_projets": nb_projets,
        "nb_projets_en_cours": nb_projets_en_cours,
        "nb_projets_termines": nb_projets_termines,
        "top_agents": top_agents,
        "total_demandes": total_demandes,
        "alertes": alertes,
        "clients": clients,
        "factures": factures,
        "tickets": tickets,
        "projets": projets,
        "interactions": interactions,
    }


def _statut_facture(facture: dict) -> str:
    """Détermine le statut d'une facture."""
    if facture.get("payee"):
        return "PAYEE"
    date_ech = facture.get("date_echeance")
    if date_ech:
        try:
            if datetime.now() > datetime.fromisoformat(date_ech):
                return "EN RETARD"
        except Exception:
            pass
    return "EN ATTENTE"


def _formatter_montant(montant: float) -> str:
    """Formate un montant en euros lisible."""
    if montant >= 1_000_000:
        return f"{montant / 1_000_000:.1f}M€"
    if montant >= 1_000:
        return f"{montant / 1_000:.1f}k€"
    return f"{montant:.0f}€"


# ═══════════════════════════════════════════════════════════════
# AGENT 1 — TABLEAU DE BORD EXÉCUTIF
# ═══════════════════════════════════════════════════════════════

def agent_tableau_bord() -> str:
    """
    Lit TOUTES les données de la mémoire et génère un tableau de bord
    exécutif complet avec graphiques ASCII.
    """
    incrementer_stat("agent_kpi_tableau_bord")
    memoire = charger_memoire()
    m = _extraire_metriques(memoire)

    print(_titre("TABLEAU DE BORD EXÉCUTIF — " + ENTREPRISE))
    print(f"  Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")

    # ── Section revenus ──
    print(_sep("─"))
    print("  REVENUS")
    print(_sep("─"))
    rev_max = max(m["revenus_total"], 1)
    print(f"  Encaissé    {_barre_ascii(m['revenus_encaisses'], rev_max)} {_formatter_montant(m['revenus_encaisses'])}")
    print(f"  En attente  {_barre_ascii(m['revenus_en_attente'], rev_max)} {_formatter_montant(m['revenus_en_attente'])}")
    print(f"  En retard   {_barre_ascii(m['revenus_en_retard'], rev_max)} {_formatter_montant(m['revenus_en_retard'])}")
    print(f"\n  Total facturation : {_formatter_montant(m['revenus_total'])}")
    taux_recouv = round(m["revenus_encaisses"] / max(m["revenus_total"], 1) * 100, 1)
    print(f"  Taux de recouvrement : {taux_recouv}%\n")

    # ── Section clients ──
    print(_sep("─"))
    print("  CLIENTS & PROSPECTS")
    print(_sep("─"))
    cli_max = max(m["nb_clients_total"], 1)
    print(f"  Clients actifs  {_barre_ascii(m['nb_clients_actifs'], cli_max)} {m['nb_clients_actifs']}")
    print(f"  Prospects       {_barre_ascii(m['nb_prospects'], cli_max)} {m['nb_prospects']}")
    print(f"\n  Total contacts : {m['nb_clients_total']}")
    print(f"  Taux conversion prospects→clients : {m['taux_conversion']}%\n")

    # ── Section tickets ──
    print(_sep("─"))
    print("  TICKETS SUPPORT")
    print(_sep("─"))
    tkt_max = max(m["nb_tickets"], 1)
    print(f"  Résolus   {_barre_ascii(m['nb_tickets_resolus'], tkt_max)} {m['nb_tickets_resolus']}")
    print(f"  Ouverts   {_barre_ascii(m['nb_tickets_ouverts'], tkt_max)} {m['nb_tickets_ouverts']}")
    if m["nb_tickets_critiques"] > 0:
        print(f"  !! CRITIQUES non résolus : {m['nb_tickets_critiques']}")
    if m["nb_tickets_haute"] > 0:
        print(f"  !  HAUTE priorité ouverts : {m['nb_tickets_haute']}")
    taux_res = round(m["nb_tickets_resolus"] / max(m["nb_tickets"], 1) * 100, 1)
    print(f"\n  Taux de résolution : {taux_res}%\n")

    # ── Section projets ──
    print(_sep("─"))
    print("  PROJETS")
    print(_sep("─"))
    proj_max = max(m["nb_projets"], 1)
    print(f"  En cours   {_barre_ascii(m['nb_projets_en_cours'], proj_max)} {m['nb_projets_en_cours']}")
    print(f"  Terminés   {_barre_ascii(m['nb_projets_termines'], proj_max)} {m['nb_projets_termines']}")
    print(f"\n  Total projets : {m['nb_projets']}\n")

    # ── Section agents ──
    print(_sep("─"))
    print("  AGENTS LES PLUS UTILISÉS")
    print(_sep("─"))
    if m["top_agents"]:
        top_val = m["top_agents"][0][1] if m["top_agents"] else 1
        for agent_nom, count in m["top_agents"]:
            barre = _barre_ascii(count, max(top_val, 1), largeur=20)
            print(f"  {agent_nom:<30} {barre} {count}")
    else:
        print("  Aucune utilisation enregistrée.")
    print(f"\n  Total requêtes agents : {m['total_demandes']}\n")

    # ── Section alertes ──
    print(_sep("─"))
    print("  ALERTES CRITIQUES")
    print(_sep("─"))
    alertes = m["alertes"]
    if not alertes:
        print("  Aucune alerte critique. Situation saine.\n")
    else:
        for alerte in alertes:
            prefixe = "  !! " if alerte["niveau"] == "CRITIQUE" else "  !  "
            print(f"{prefixe}[{alerte['niveau']}] {alerte['message']}")
        print()

    print(_sep("═"))

    # Résumé textuel par Gemini
    donnees_str = f"""
Données du tableau de bord AgentClaude Solutions au {datetime.now().strftime('%d/%m/%Y')} :

REVENUS :
- Total facturé : {_formatter_montant(m['revenus_total'])}
- Encaissé : {_formatter_montant(m['revenus_encaisses'])} (taux recouvrement : {taux_recouv}%)
- En attente : {_formatter_montant(m['revenus_en_attente'])}
- En retard de paiement : {_formatter_montant(m['revenus_en_retard'])} ({m['nb_factures_retard']} facture(s))

CLIENTS :
- Clients actifs : {m['nb_clients_actifs']}
- Prospects : {m['nb_prospects']}
- Taux conversion : {m['taux_conversion']}%

TICKETS :
- Ouverts : {m['nb_tickets_ouverts']} (dont {m['nb_tickets_critiques']} critiques)
- Taux résolution : {taux_res}%

PROJETS :
- En cours : {m['nb_projets_en_cours']}
- Terminés : {m['nb_projets_termines']}

ALERTES : {len(alertes)} alerte(s) détectée(s)
"""

    prompt = f"""Tu es le Directeur Général de {ENTREPRISE}, spécialisée en agents IA autonomes.

Sur la base de ce tableau de bord, rédige un résumé exécutif en français de 150 à 200 mots maximum.
Sois direct, analytique, et conclus avec 2 priorités immédiates pour la semaine.

{donnees_str}

Format :
RÉSUMÉ EXÉCUTIF
[Texte du résumé]

PRIORITÉS IMMÉDIATES :
1. ...
2. ...
"""

    print("\n  Analyse IA en cours...\n")
    print(_sep("─"))
    print("  RÉSUMÉ EXÉCUTIF (IA)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.4)

    # Sauvegarde
    contenu_rapport = f"TABLEAU DE BORD — {ENTREPRISE}\n"
    contenu_rapport += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    contenu_rapport += "=" * LARGEUR + "\n\n"
    contenu_rapport += f"Revenus total : {_formatter_montant(m['revenus_total'])}\n"
    contenu_rapport += f"Clients actifs : {m['nb_clients_actifs']} | Prospects : {m['nb_prospects']}\n"
    contenu_rapport += f"Tickets ouverts : {m['nb_tickets_ouverts']}\n"
    contenu_rapport += f"Projets en cours : {m['nb_projets_en_cours']}\n"
    contenu_rapport += f"Alertes : {len(alertes)}\n\n"
    contenu_rapport += "ANALYSE IA :\n" + reponse

    chemin = _sauvegarder_rapport("tableau_bord", contenu_rapport)
    print(f"  Rapport sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# AGENT 2 — ALERTES PROACTIVES
# ═══════════════════════════════════════════════════════════════

def agent_alerte_proactive() -> str:
    """
    Scanne toutes les données de la mémoire et identifie proactivement
    les risques avant qu'ils ne deviennent des problèmes.
    """
    incrementer_stat("agent_kpi_alertes")
    memoire = charger_memoire()
    clients = memoire.get("clients", {})
    factures = memoire.get("factures", [])
    projets = memoire.get("projets", {})
    interactions = memoire.get("interactions", [])
    now = datetime.now()

    print(_titre("SYSTÈME D'ALERTES PROACTIVES — " + ENTREPRISE))
    print(f"  Analyse du {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")

    risques = []

    # ── Clients inactifs depuis >30j (risque churn) ──
    for nom_client, data in clients.items():
        if data.get("statut") == "actif":
            # Chercher la dernière interaction
            derniere_interaction = None
            for inter in sorted(interactions, key=lambda x: x.get("date", ""), reverse=True):
                if inter.get("client") == nom_client:
                    derniere_interaction = inter.get("date")
                    break
            # Aussi vérifier interactions dans la fiche client
            if not derniere_interaction and data.get("interactions"):
                derniere_interaction = max(
                    (i.get("date", "") for i in data["interactions"]),
                    default=None
                )
            if derniere_interaction:
                jours = _jours_depuis(derniere_interaction)
                if jours > 30:
                    risques.append({
                        "niveau": "HAUTE",
                        "categorie": "CHURN",
                        "client": nom_client,
                        "jours": jours,
                        "detail": f"Client actif sans contact depuis {jours}j",
                        "action": f"Relancer {nom_client} cette semaine — proposer un point bilan ou une nouvelle offre",
                    })
            elif data.get("date_ajout"):
                jours = _jours_depuis(data["date_ajout"])
                if jours > 30:
                    risques.append({
                        "niveau": "MOYENNE",
                        "categorie": "CHURN",
                        "client": nom_client,
                        "jours": jours,
                        "detail": f"Client sans historique d'interaction depuis {jours}j",
                        "action": f"Vérifier la relation avec {nom_client} — aucune interaction enregistrée",
                    })

    # ── Prospects sans relance depuis >14j ──
    for nom_client, data in clients.items():
        if data.get("statut") == "prospect":
            date_ref = data.get("date_ajout", "")
            derniere_interaction = None
            for inter in sorted(interactions, key=lambda x: x.get("date", ""), reverse=True):
                if inter.get("client") == nom_client:
                    derniere_interaction = inter.get("date")
                    break
            date_calcul = derniere_interaction or date_ref
            if date_calcul:
                jours = _jours_depuis(date_calcul)
                if jours > 14:
                    risques.append({
                        "niveau": "MOYENNE",
                        "categorie": "PROSPECT",
                        "client": nom_client,
                        "jours": jours,
                        "detail": f"Prospect sans relance depuis {jours}j",
                        "action": f"Envoyer une relance commerciale à {nom_client} — besoin : {data.get('besoin_principal', 'non renseigné')}",
                    })

    # ── Factures impayées >45j ──
    for f in factures:
        if not f.get("payee"):
            date_ech = f.get("date_echeance", "")
            if date_ech:
                jours = _jours_depuis(date_ech)
                if jours > 45:
                    client_nom = f.get("client", {}).get("nom", "Inconnu")
                    risques.append({
                        "niveau": "CRITIQUE",
                        "categorie": "IMPAYÉ",
                        "client": client_nom,
                        "jours": jours,
                        "detail": f"Facture {f.get('numero')} impayée depuis {jours}j — {f.get('total_ttc', 0):.0f}€ TTC",
                        "action": f"Déclencher procédure contentieux pour {client_nom} — contacter un avocat si nécessaire",
                    })
                elif jours > 30:
                    client_nom = f.get("client", {}).get("nom", "Inconnu")
                    risques.append({
                        "niveau": "HAUTE",
                        "categorie": "IMPAYÉ",
                        "client": client_nom,
                        "jours": jours,
                        "detail": f"Facture {f.get('numero')} en retard de {jours}j — {f.get('total_ttc', 0):.0f}€ TTC",
                        "action": f"Envoyer relance niveau 3 à {client_nom} et bloquer de nouveaux services",
                    })

    # ── Projets sans standup depuis >7j ──
    for nom_projet, p in projets.items():
        if p.get("statut") not in ("terminé", "annulé"):
            derniere_maj = (
                p.get("date_derniere_maj")
                or p.get("last_update")
                or p.get("date_creation")
                or p.get("date_debut")
            )
            if derniere_maj:
                jours = _jours_depuis(derniere_maj)
                if jours > 7:
                    risques.append({
                        "niveau": "MOYENNE",
                        "categorie": "PROJET",
                        "client": p.get("client", "N/A"),
                        "jours": jours,
                        "detail": f"Projet '{nom_projet}' sans mise à jour depuis {jours}j",
                        "action": f"Organiser un standup pour '{nom_projet}' — vérifier les blocages éventuels",
                    })

    # ── Affichage ──
    if not risques:
        print("  Aucun risque détecté. Situation saine.\n")
    else:
        # Tri par priorité
        ordre = {"CRITIQUE": 0, "HAUTE": 1, "MOYENNE": 2}
        risques.sort(key=lambda x: ordre.get(x["niveau"], 9))

        critiques = [r for r in risques if r["niveau"] == "CRITIQUE"]
        hautes = [r for r in risques if r["niveau"] == "HAUTE"]
        moyennes = [r for r in risques if r["niveau"] == "MOYENNE"]

        for label, liste, icone in [
            ("CRITIQUES", critiques, "!!"),
            ("HAUTE PRIORITÉ", hautes, "! "),
            ("MOYENNES", moyennes, "i "),
        ]:
            if liste:
                print(_sep("─"))
                print(f"  {icone} {label} ({len(liste)} risque(s))")
                print(_sep("─"))
                for r in liste:
                    print(f"\n  [{r['categorie']}] {r['detail']}")
                    print(f"  → ACTION : {r['action']}")
                print()

    # Résumé IA
    if risques:
        risques_str = "\n".join([
            f"- [{r['niveau']}][{r['categorie']}] {r['detail']} | Action : {r['action']}"
            for r in risques
        ])
    else:
        risques_str = "Aucun risque identifié."

    prompt = f"""Tu es le Directeur des Opérations de {ENTREPRISE}, spécialisée en agents IA.

Voici les risques détectés automatiquement dans les données de l'entreprise :

{risques_str}

En français, rédige une analyse proactive courte (150 mots max) avec :
1. Synthèse des risques prioritaires
2. Recommandations concrètes
3. Indicateur de santé global (Vert/Orange/Rouge) avec justification

Sois direct et actionnable.
"""

    print(_sep("─"))
    print("  ANALYSE PROACTIVE (IA)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.4)

    # Sauvegarde
    contenu = f"ALERTES PROACTIVES — {ENTREPRISE}\n"
    contenu += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    contenu += "=" * LARGEUR + "\n\n"
    contenu += f"Nombre de risques détectés : {len(risques)}\n\n"
    for r in risques:
        contenu += f"[{r['niveau']}][{r['categorie']}] {r['detail']}\n"
        contenu += f"  Action : {r['action']}\n\n"
    contenu += "\nANALYSE IA :\n" + reponse

    chemin = _sauvegarder_rapport("alertes_proactives", contenu)
    print(f"  Rapport sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# AGENT 3 — RAPPORT HEBDOMADAIRE
# ═══════════════════════════════════════════════════════════════

def agent_rapport_hebdomadaire() -> str:
    """
    Génère un rapport hebdomadaire complet : faits marquants, KPIs vs semaine
    précédente (simulés), victoires, préoccupations, priorités.
    """
    incrementer_stat("agent_kpi_rapport_hebdo")
    memoire = charger_memoire()
    m = _extraire_metriques(memoire)
    now = datetime.now()
    semaine = now.isocalendar()[1]
    annee = now.year

    print(_titre(f"RAPPORT HEBDOMADAIRE S{semaine}/{annee} — {ENTREPRISE}"))
    print(f"  Période : semaine du {(now - timedelta(days=now.weekday())).strftime('%d/%m/%Y')}\n")

    # Interactions de la semaine
    debut_semaine = now - timedelta(days=now.weekday())
    interactions_semaine = [
        i for i in m["interactions"]
        if _jours_depuis(i.get("date", "")) <= 7
    ]
    factures_semaine = [
        f for f in m["factures"]
        if _jours_depuis(f.get("date_emission", "")) <= 7
    ]
    revenus_semaine = sum(f.get("total_ttc", 0) for f in factures_semaine)
    tickets_semaine = [
        t for t in m["tickets"]
        if _jours_depuis(t.get("date", "")) <= 7
    ]

    # Affichage KPIs de la semaine
    print(_sep("─"))
    print("  KPIs DE LA SEMAINE")
    print(_sep("─"))
    print(f"  Factures émises cette semaine  : {len(factures_semaine)} ({_formatter_montant(revenus_semaine)})")
    print(f"  Tickets traités cette semaine  : {len(tickets_semaine)}")
    print(f"  Interactions enregistrées      : {len(interactions_semaine)}")
    print(f"  Clients actifs (total)         : {m['nb_clients_actifs']}")
    print(f"  Projets en cours               : {m['nb_projets_en_cours']}")
    print(f"  Alertes actives                : {len(m['alertes'])}\n")

    # Données structurées pour le prompt
    donnees_semaine = f"""
Données AgentClaude Solutions — Semaine {semaine}/{annee}

ACTIVITÉ SEMAINE :
- Factures émises : {len(factures_semaine)} pour {_formatter_montant(revenus_semaine)}
- Tickets traités : {len(tickets_semaine)}
- Interactions clients : {len(interactions_semaine)}

ÉTAT GLOBAL :
- Revenus encaissés (cumulé) : {_formatter_montant(m['revenus_encaisses'])}
- Revenus en attente : {_formatter_montant(m['revenus_en_attente'])}
- Clients actifs : {m['nb_clients_actifs']}
- Prospects : {m['nb_prospects']}
- Taux conversion : {m['taux_conversion']}%
- Projets en cours : {m['nb_projets_en_cours']}
- Tickets ouverts : {m['nb_tickets_ouverts']} (dont {m['nb_tickets_critiques']} critiques)
- Alertes : {len(m['alertes'])}

TOP AGENTS UTILISÉS : {', '.join(f"{a}({n})" for a, n in m['top_agents'][:3]) if m['top_agents'] else 'N/A'}
"""

    prompt = f"""Tu es le Directeur Général de {ENTREPRISE}, spécialisée en agents IA autonomes.

Génère un rapport hebdomadaire complet et professionnel en français pour la semaine {semaine}/{annee}.

Données disponibles :
{donnees_semaine}

Le rapport doit inclure EXACTEMENT ces sections :

1. FAITS MARQUANTS DE LA SEMAINE
   (3-4 points clés, ce qui s'est passé d'important)

2. KPIS VS SEMAINE PRÉCÉDENTE
   (Compare avec des valeurs simulées réalistes de la semaine d'avant — calcule des variations %)

3. VICTOIRES (WINS)
   (Ce qui fonctionne bien, succès à célébrer — au moins 2)

4. PRÉOCCUPATIONS
   (Ce qui mérite attention — au moins 1, maximum 3)

5. PRIORITÉS SEMAINE PROCHAINE
   (3 actions concrètes avec responsable suggéré)

6. DÉCISION CLÉ REQUISE DE LA DIRECTION
   (1 décision stratégique que le leadership doit prendre cette semaine)

Ton : professionnel, direct, orienté action. Longueur : 300-400 mots.
"""

    print(_sep("─"))
    print("  RAPPORT COMPLET (IA)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.5)

    contenu = f"RAPPORT HEBDOMADAIRE S{semaine}/{annee} — {ENTREPRISE}\n"
    contenu += f"Date : {now.strftime('%d/%m/%Y %H:%M:%S')}\n"
    contenu += "=" * LARGEUR + "\n\n"
    contenu += f"Activité semaine : {len(factures_semaine)} factures, {len(tickets_semaine)} tickets\n\n"
    contenu += reponse

    chemin = _sauvegarder_rapport(f"rapport_hebdo_S{semaine}_{annee}", contenu)
    print(f"  Rapport sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# AGENT 4 — OBJECTIFS & SUIVI
# ═══════════════════════════════════════════════════════════════

def agent_objectifs(objectif: str, valeur_cible: float, echeance: str) -> str:
    """
    Définit un objectif business, suit la progression depuis la mémoire,
    génère un plan d'action avec jalons.

    Args:
        objectif : Description de l'objectif (ex: "Atteindre 100k€ de CA")
        valeur_cible : Valeur numérique cible (ex: 100000)
        echeance : Date limite au format JJ/MM/AAAA (ex: "31/12/2026")
    """
    incrementer_stat("agent_kpi_objectifs")
    memoire = charger_memoire()
    m = _extraire_metriques(memoire)

    print(_titre(f"SUIVI D'OBJECTIF — {ENTREPRISE}"))
    print(f"  Objectif : {objectif}")
    print(f"  Cible    : {valeur_cible:,.0f}")
    print(f"  Échéance : {echeance}\n")

    # Calcul de l'avancement selon le type d'objectif
    # On essaie de faire correspondre l'objectif aux métriques disponibles
    valeur_actuelle = 0.0
    metrique_utilisee = "personnalisée"

    obj_lower = objectif.lower()
    if any(k in obj_lower for k in ["chiffre", "revenu", "ca ", "€", "euro"]):
        valeur_actuelle = m["revenus_encaisses"]
        metrique_utilisee = "revenus encaissés"
    elif any(k in obj_lower for k in ["client", "compte"]):
        valeur_actuelle = float(m["nb_clients_actifs"])
        metrique_utilisee = "clients actifs"
    elif any(k in obj_lower for k in ["ticket", "support"]):
        valeur_actuelle = float(m["nb_tickets_resolus"])
        metrique_utilisee = "tickets résolus"
    elif any(k in obj_lower for k in ["projet"]):
        valeur_actuelle = float(m["nb_projets_termines"])
        metrique_utilisee = "projets terminés"
    elif any(k in obj_lower for k in ["conversion", "prospect"]):
        valeur_actuelle = m["taux_conversion"]
        metrique_utilisee = "taux de conversion (%)"

    # Calcul avancement
    progression = round(valeur_actuelle / max(valeur_cible, 1) * 100, 1)
    progression = min(progression, 100)
    barre = _barre_ascii(valeur_actuelle, valeur_cible, largeur=40)

    # Calcul jours restants
    try:
        date_echeance = datetime.strptime(echeance, "%d/%m/%Y")
        jours_restants = (date_echeance - datetime.now()).days
    except Exception:
        jours_restants = 90  # défaut

    print(_sep("─"))
    print("  PROGRESSION ACTUELLE")
    print(_sep("─"))
    print(f"  Métrique suivie : {metrique_utilisee}")
    print(f"  Valeur actuelle : {valeur_actuelle:,.1f}")
    print(f"  Valeur cible    : {valeur_cible:,.0f}")
    print(f"  {barre} {progression}%")
    print(f"\n  Jours restants : {jours_restants}")
    ecart = valeur_cible - valeur_actuelle
    print(f"  Écart à combler : {ecart:,.1f}\n")

    prompt = f"""Tu es un consultant en performance business pour {ENTREPRISE}, spécialisée en agents IA.

OBJECTIF : {objectif}
Valeur cible : {valeur_cible:,.0f} ({metrique_utilisee})
Valeur actuelle : {valeur_actuelle:,.1f}
Progression : {progression}%
Jours restants : {jours_restants}
Échéance : {echeance}

Contexte actuel de l'entreprise :
- Clients actifs : {m['nb_clients_actifs']} | Prospects : {m['nb_prospects']}
- Revenus encaissés : {_formatter_montant(m['revenus_encaisses'])}
- Projets en cours : {m['nb_projets_en_cours']}
- Taux conversion : {m['taux_conversion']}%

En français, génère un plan d'action complet pour atteindre cet objectif :

1. ANALYSE DE FAISABILITÉ
   (L'objectif est-il atteignable dans le délai ? Quelle est la vitesse requise ?)

2. PLAN D'ACTION EN 3 PHASES
   Phase 1 (premier tiers du délai) : actions à lancer immédiatement
   Phase 2 (deuxième tiers) : actions de consolidation
   Phase 3 (dernier tiers) : sprint final

3. JALONS CLÉS (5 checkpoints avec dates approximatives et critères de succès)

4. RISQUES ET PLANS B
   (2-3 risques principaux avec solutions alternatives)

5. RESSOURCES NÉCESSAIRES
   (Humaines, financières, techniques)

Sois concret, chiffré et actionnable.
"""

    print(_sep("─"))
    print("  PLAN D'ACTION (IA)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.5)

    contenu = f"SUIVI OBJECTIF — {ENTREPRISE}\n"
    contenu += f"Objectif : {objectif}\n"
    contenu += f"Cible : {valeur_cible:,.0f} | Actuel : {valeur_actuelle:,.1f} | Progression : {progression}%\n"
    contenu += f"Échéance : {echeance} ({jours_restants}j restants)\n"
    contenu += "=" * LARGEUR + "\n\n"
    contenu += reponse

    chemin = _sauvegarder_rapport("objectif", contenu)
    print(f"  Plan sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# AGENT 5 — PRÉDICTIONS & PROJECTIONS
# ═══════════════════════════════════════════════════════════════

def agent_prediction(horizon_mois: int) -> str:
    """
    Génère des projections business sur un horizon donné :
    revenus, croissance clients, besoins ressources, risques, opportunités.

    Args:
        horizon_mois : Horizon de prédiction en mois (ex: 3, 6, 12)
    """
    incrementer_stat("agent_kpi_prediction")
    memoire = charger_memoire()
    m = _extraire_metriques(memoire)

    print(_titre(f"PROJECTIONS {horizon_mois} MOIS — {ENTREPRISE}"))
    print(f"  Horizon : {datetime.now().strftime('%d/%m/%Y')} → {(datetime.now() + timedelta(days=horizon_mois * 30)).strftime('%d/%m/%Y')}\n")

    # Calculs de tendances
    factures = m["factures"]
    nb_factures_total = len(factures)
    revenu_mensuel_moyen = (
        m["revenus_total"] / max(nb_factures_total, 1) * (nb_factures_total / max(6, 1))
        if nb_factures_total > 0
        else 0
    )
    # Estimation simplifiée
    croissance_mensuelle_clients = max(m["nb_prospects"] * m["taux_conversion"] / 100, 0.5)

    # Projections linéaires
    revenu_proj = m["revenus_encaisses"] + (revenu_mensuel_moyen * horizon_mois)
    clients_proj = m["nb_clients_actifs"] + int(croissance_mensuelle_clients * horizon_mois)

    print(_sep("─"))
    print("  PROJECTIONS CALCULÉES")
    print(_sep("─"))
    print(f"  Revenus projetés dans {horizon_mois} mois : {_formatter_montant(revenu_proj)}")
    print(f"  Clients actifs projetés            : {clients_proj}")
    print(f"  Croissance clients/mois estimée    : +{croissance_mensuelle_clients:.1f}")
    print()

    prompt = f"""Tu es un analyste financier et stratégique senior de {ENTREPRISE}, spécialisée en agents IA autonomes.

Données actuelles :
- Revenus encaissés : {_formatter_montant(m['revenus_encaisses'])}
- Revenus en attente : {_formatter_montant(m['revenus_en_attente'])}
- Revenus totaux facturés : {_formatter_montant(m['revenus_total'])}
- Clients actifs : {m['nb_clients_actifs']}
- Prospects pipeline : {m['nb_prospects']}
- Taux conversion actuel : {m['taux_conversion']}%
- Projets en cours : {m['nb_projets_en_cours']}
- Tickets support : {m['nb_tickets_ouverts']} ouverts
- Alertes actives : {len(m['alertes'])}

HORIZON D'ANALYSE : {horizon_mois} mois
Date de départ : {datetime.now().strftime('%d/%m/%Y')}

En français, génère des projections business complètes et réalistes :

1. PRÉVISIONS DE REVENUS
   - Scénario pessimiste / réaliste / optimiste
   - Hypothèses pour chaque scénario
   - Tableau mensuel simplifié sur {horizon_mois} mois

2. CROISSANCE CLIENT
   - Évolution du nombre de clients actifs
   - Pipeline prospects → conversion estimée
   - Secteurs porteurs à cibler

3. BESOINS EN RESSOURCES
   - Ressources humaines (recrutements nécessaires ?)
   - Infrastructure technique (agents IA, outils)
   - Budget marketing et commercial estimé

4. RISQUES IDENTIFIÉS
   (3 risques majeurs avec probabilité et impact)

5. OPPORTUNITÉS À SAISIR
   (3 opportunités concrètes dans cet horizon)

6. RECOMMANDATION STRATÉGIQUE
   (Quelle stratégie adopter pour maximiser la croissance sur {horizon_mois} mois ?)

Utilise des chiffres concrets, des pourcentages et des fourchettes réalistes.
Calibre tes projections sur la taille réelle de l'entreprise (PME/startup IA).
"""

    print(_sep("─"))
    print("  ANALYSE PRÉDICTIVE (IA)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.6)

    contenu = f"PROJECTIONS {horizon_mois} MOIS — {ENTREPRISE}\n"
    contenu += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    contenu += f"Horizon : {horizon_mois} mois\n"
    contenu += "=" * LARGEUR + "\n\n"
    contenu += f"Revenus actuels : {_formatter_montant(m['revenus_total'])}\n"
    contenu += f"Clients actifs : {m['nb_clients_actifs']}\n\n"
    contenu += reponse

    chemin = _sauvegarder_rapport(f"prediction_{horizon_mois}mois", contenu)
    print(f"  Rapport sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def afficher_menu():
    print("\n" + "═" * LARGEUR)
    print(f"  AGENT KPI & TABLEAU DE BORD — {ENTREPRISE}")
    print(f"  Système nerveux central de l'entreprise")
    print("═" * LARGEUR)
    print("  1. Tableau de bord exécutif complet")
    print("  2. Alertes proactives (risques avant problèmes)")
    print("  3. Rapport hebdomadaire")
    print("  4. Définir un objectif & plan d'action")
    print("  5. Prédictions & projections business")
    print("  0. Quitter")
    print("═" * LARGEUR)


def menu():
    while True:
        afficher_menu()
        choix = input("\n  Votre choix → ").strip()

        if choix == "0":
            print("\n  Au revoir. Le système KPI reste actif.\n")
            break

        elif choix == "1":
            agent_tableau_bord()

        elif choix == "2":
            agent_alerte_proactive()

        elif choix == "3":
            agent_rapport_hebdomadaire()

        elif choix == "4":
            print("\n  Définition d'un objectif business")
            print("  " + "─" * 40)
            objectif = input("  Description de l'objectif : ").strip()
            if not objectif:
                print("  Objectif requis.")
                continue
            try:
                valeur_cible = float(input("  Valeur cible (nombre) : ").strip())
            except ValueError:
                print("  Valeur numérique invalide.")
                continue
            echeance = input("  Échéance (JJ/MM/AAAA) : ").strip()
            if not echeance:
                echeance = (datetime.now() + timedelta(days=90)).strftime("%d/%m/%Y")
                print(f"  Échéance par défaut : {echeance}")
            agent_objectifs(objectif, valeur_cible, echeance)

        elif choix == "5":
            print("\n  Horizon de projection :")
            print("    1. 3 mois    2. 6 mois    3. 12 mois    4. Personnalisé")
            sous_choix = input("  Votre choix → ").strip()
            horizons = {"1": 3, "2": 6, "3": 12}
            if sous_choix in horizons:
                horizon = horizons[sous_choix]
            elif sous_choix == "4":
                try:
                    horizon = int(input("  Nombre de mois : ").strip())
                    if horizon <= 0:
                        raise ValueError
                except ValueError:
                    print("  Nombre invalide.")
                    continue
            else:
                print("  Choix invalide.")
                continue
            agent_prediction(horizon)

        else:
            print("  Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    menu()
