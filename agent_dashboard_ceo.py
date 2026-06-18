"""
AGENT DASHBOARD CEO — Vue exécutive en temps réel
Rapport hebdomadaire complet : revenus, pipeline, KPIs, alertes, prévisions.
Ce que voit un CEO qui dirige avec les données.

Usage : python agent_dashboard_ceo.py
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


def charger_toutes_les_donnees():
    """Agrège toutes les sources de données disponibles."""
    donnees = {
        "memoire": {},
        "pipeline": {},
        "watchdog": {},
        "date": datetime.now().isoformat(),
    }

    for fichier, cle in [
        ("memoire_entreprise.json", "memoire"),
        ("crm_pipeline.json", "pipeline"),
        ("watchdog_sante.json", "watchdog"),
    ]:
        if os.path.exists(fichier):
            try:
                with open(fichier, "r", encoding="utf-8") as f:
                    donnees[cle] = json.load(f)
            except Exception:
                pass

    return donnees


def calculer_metriques(donnees):
    """Calcule les métriques clés."""
    m = donnees.get("memoire", {})
    p = donnees.get("pipeline", {})
    w = donnees.get("watchdog", {})

    # Clients & revenus
    clients = m.get("clients", {})
    factures = m.get("factures", {})
    ca_encaisse = sum(
        f.get("montant", 0) for f in factures.values()
        if f.get("statut") == "payee"
    )
    ca_en_attente = sum(
        f.get("montant", 0) for f in factures.values()
        if f.get("statut") == "en_attente"
    )

    # Pipeline CRM
    leads = p.get("leads", {})
    ca_pipeline = sum(l.get("prix", 0) for l in leads.values()
                      if l.get("stage") not in ["7_gagne", "7_perdu"])
    leads_actifs = [l for l in leads.values()
                    if l.get("stage") not in ["7_gagne", "7_perdu"]]

    # Tickets support
    tickets = m.get("tickets", [])
    tickets_ouverts = [t for t in tickets if t.get("statut") != "resolu"]
    tickets_critiques = [t for t in tickets_ouverts if t.get("urgence") == "CRITIQUE"]

    # Santé système
    checks = w.get("checks", [])
    score_sante = checks[-1].get("score", 100) if checks else 100

    # Agents utilisés
    stats_agents = m.get("stats", {}).get("agents_utilises", {})
    total_interactions = len(m.get("interactions", []))

    return {
        "clients_actifs": len([c for c in clients.values() if c.get("statut") == "actif"]),
        "prospects": len([c for c in clients.values() if c.get("statut") == "prospect"]),
        "ca_encaisse": ca_encaisse,
        "ca_en_attente": ca_en_attente,
        "ca_pipeline": ca_pipeline,
        "leads_actifs": len(leads_actifs),
        "tickets_ouverts": len(tickets_ouverts),
        "tickets_critiques": len(tickets_critiques),
        "score_sante_systeme": score_sante,
        "total_interactions": total_interactions,
        "agents_utilises_count": len(stats_agents),
        "top_agents": sorted(stats_agents.items(), key=lambda x: x[1], reverse=True)[:5],
        "pipeline_stats": p.get("stats", {}),
    }


def barre_ascii(valeur, max_valeur, largeur=20):
    """Génère une barre de progression ASCII."""
    if max_valeur == 0:
        remplissage = 0
    else:
        remplissage = int(min(valeur / max_valeur, 1) * largeur)
    barre = "█" * remplissage + "░" * (largeur - remplissage)
    return f"[{barre}] {valeur}"


def afficher_dashboard():
    """Affiche le dashboard CEO complet en temps réel."""
    donnees = charger_toutes_les_donnees()
    m = calculer_metriques(donnees)
    maintenant = datetime.now()

    print(f"\n{'═'*65}")
    print(f"  DASHBOARD CEO — CAELUM PARTNERS")
    print(f"  {maintenant.strftime('%A %d %B %Y — %H:%M')}")
    print(f"{'═'*65}\n")

    # ── REVENUS ──
    print(f"  {'─'*30}  REVENUS  {'─'*20}")
    print(f"  CA encaissé    : {m['ca_encaisse']:>8}€  {barre_ascii(m['ca_encaisse'], 10000)}")
    print(f"  En attente     : {m['ca_en_attente']:>8}€")
    print(f"  Pipeline CRM   : {m['ca_pipeline']:>8}€  (potentiel)")
    print(f"  CA total proj. : {m['ca_encaisse'] + m['ca_en_attente'] + m['ca_pipeline']:>8}€")

    # ── CLIENTS ──
    print(f"\n  {'─'*30}  CLIENTS  {'─'*20}")
    print(f"  Clients actifs : {m['clients_actifs']:>3}")
    print(f"  Prospects      : {m['prospects']:>3}")
    print(f"  Leads pipeline : {m['leads_actifs']:>3}")
    p_stats = m["pipeline_stats"]
    if p_stats:
        total_l = p_stats.get("total_leads", 0)
        gagnes = p_stats.get("gagnes", 0)
        taux = round(gagnes / total_l * 100) if total_l > 0 else 0
        print(f"  Taux conversion: {taux:>3}%  ({gagnes}/{total_l} leads)")

    # ── OPÉRATIONS ──
    print(f"\n  {'─'*30}  OPÉRATIONS  {'─'*17}")
    statut_tickets = "🔴 CRITIQUE" if m["tickets_critiques"] > 0 else ("🟡" if m["tickets_ouverts"] > 0 else "✅")
    print(f"  Tickets ouverts  : {m['tickets_ouverts']:>3}  {statut_tickets}")
    print(f"  Tickets critiques: {m['tickets_critiques']:>3}")
    print(f"  Interactions IA  : {m['total_interactions']:>5}")
    print(f"  Agents actifs    : {m['agents_utilises_count']:>3}")

    # ── SANTÉ SYSTÈME ──
    score = m["score_sante_systeme"]
    statut_sys = "✅ OPTIMAL" if score >= 90 else ("🟡 DÉGRADÉ" if score >= 70 else "🔴 CRITIQUE")
    print(f"\n  {'─'*30}  SYSTÈME  {'─'*21}")
    print(f"  Santé agents     : {score}%  {statut_sys}")

    # ── TOP AGENTS ──
    if m["top_agents"]:
        print(f"\n  {'─'*30}  TOP AGENTS  {'─'*18}")
        for agent, count in m["top_agents"]:
            print(f"  {agent:<35} {count:>3}x")

    print(f"\n{'═'*65}\n")


def rapport_hebdomadaire():
    """Génère le rapport CEO hebdomadaire complet avec l'IA."""
    donnees = charger_toutes_les_donnees()
    m = calculer_metriques(donnees)

    semaine = datetime.now().strftime("Semaine %W — %B %Y")

    model = _creer_model(
        model_name=MODEL,
        system_instruction="""Tu es le Chief of Staff de Caelum Partners.
Tu rédiges le rapport hebdomadaire CEO avec la rigueur d'un cabinet de conseil.
Le rapport est dense, chiffré, actionnable. Pas de blabla.
Fondatrice : Chaima Mhadbi | contact@caelumpartners.agency""",
        generation_config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=2500),
    )

    print(f"\n{'═'*65}")
    print(f"  RAPPORT CEO — {semaine}")
    print(f"{'═'*65}\n")

    prompt = f"""DONNÉES DE LA SEMAINE :
CA encaissé : {m['ca_encaisse']}€
CA en attente : {m['ca_en_attente']}€
Pipeline : {m['ca_pipeline']}€
Clients actifs : {m['clients_actifs']}
Leads actifs : {m['leads_actifs']}
Tickets critiques : {m['tickets_critiques']}
Score système : {m['score_sante_systeme']}%
Interactions IA : {m['total_interactions']}

Génère le rapport selon ce format :

# RAPPORT CEO — {semaine}

## 🎯 RÉSUMÉ EXÉCUTIF (3 lignes max)

## 💰 PERFORMANCE FINANCIÈRE
[Analyse revenus, tendances, projections mois prochain]

## 🔄 PIPELINE COMMERCIAL
[Leads chauds, actions prioritaires, deals à fermer cette semaine]

## ⚠️ ALERTES & RISQUES
[Ce qui nécessite attention immédiate]

## 🚀 OPPORTUNITÉS
[Ce qu'on peut accélérer cette semaine]

## 📋 PLAN D'ACTION SEMAINE PROCHAINE
Lundi : ...
Mardi : ...
Mercredi : ...
Jeudi : ...
Vendredi : ...

## 📊 KPIs SEMAINE PROCHAINE
→ Objectif CA : ...€
→ Nouveaux leads : ...
→ Deals à conclure : ..."""

    reponse = ""
    try:
        for chunk in model.generate_content(prompt, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()

    # Sauvegarder le rapport
    nom_fichier = f"rapport_ceo_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(f"RAPPORT CEO — {semaine}\n")
        f.write(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n\n")
        f.write(reponse)
    print(f"\n  ✅ Rapport sauvegardé → {nom_fichier}")


def alerte_ceo():
    """Détecte les anomalies et crée une alerte immédiate."""
    donnees = charger_toutes_les_donnees()
    m = calculer_metriques(donnees)
    alertes = []

    if m["tickets_critiques"] > 0:
        alertes.append(f"🔴 {m['tickets_critiques']} ticket(s) CRITIQUE(S) non traité(s)")
    if m["ca_en_attente"] > 0:
        alertes.append(f"🟠 {m['ca_en_attente']}€ de factures en attente de paiement")
    if m["score_sante_systeme"] < 80:
        alertes.append(f"🔴 Santé système dégradée : {m['score_sante_systeme']}%")
    if m["leads_actifs"] == 0:
        alertes.append("🟡 Pipeline vide — aucun lead actif")
    if m["clients_actifs"] == 0 and m["ca_encaisse"] == 0:
        alertes.append("🟠 Aucun client actif — priorité acquisition")

    print(f"\n{'═'*60}")
    print(f"  ALERTES CEO — {datetime.now().strftime('%H:%M')}")
    print(f"{'═'*60}\n")

    if not alertes:
        print("  ✅ Tout est nominal. Aucune alerte.")
    else:
        for a in alertes:
            print(f"  {a}")

        model = _creer_model(
            model_name=MODEL,
            system_instruction="Tu es le conseiller du CEO. En 5 points max, dis quoi faire MAINTENANT pour gérer ces alertes.",
            generation_config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=400),
        )
        print(f"\n  Actions recommandées :\n")
        try:
            for chunk in model.generate_content(
                f"Alertes CEO Caelum Partners:\n" + "\n".join(alertes),
                stream=True
            ):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
        except Exception as e:
            print(f"[Erreur : {e}]")
        print()


def objectifs_mensuels():
    """Définit et suit les objectifs du mois."""
    donnees = charger_toutes_les_donnees()
    m = calculer_metriques(donnees)
    mois = datetime.now().strftime("%B %Y")

    model = _creer_model(
        model_name=MODEL,
        system_instruction="""Tu es le stratège de Caelum Partners.
Tu fixes des objectifs SMART pour le mois et un plan de bataille pour les atteindre.
Objectifs réalistes mais ambitieux. Chaque objectif = 1 métrique chiffrée.""",
        generation_config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=1500),
    )

    print(f"\n{'═'*60}")
    print(f"  OBJECTIFS — {mois}")
    print(f"{'═'*60}\n")

    try:
        for chunk in model.generate_content(
            f"""Situation actuelle de Caelum Partners :
CA encaissé : {m['ca_encaisse']}€ | Pipeline : {m['ca_pipeline']}€
Clients : {m['clients_actifs']} | Leads : {m['leads_actifs']}
Services : Site web 500€ / Automation 1500€ / Pack 3000€

Fixe les objectifs pour {mois} avec :
1. Objectif CA (réaliste + ambitieux)
2. Nombre de nouveaux clients
3. Nombre de leads à générer
4. Objectif LinkedIn (connexions, posts, messages)
5. Plan semaine par semaine pour atteindre ces objectifs
6. Agent IA à utiliser pour chaque objectif""",
            stream=True
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  AGENT DASHBOARD CEO — Vue exécutive temps réel")
    print("  Caelum Partners")
    print("═"*60)

    while True:
        print("\n  1. Dashboard temps réel")
        print("  2. Rapport hebdomadaire complet")
        print("  3. Alertes CEO — Ce qui nécessite attention")
        print("  4. Objectifs du mois — Plan de bataille")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            afficher_dashboard()
        elif choix == "2":
            rapport_hebdomadaire()
        elif choix == "3":
            alerte_ceo()
        elif choix == "4":
            objectifs_mensuels()
        else:
            print("  Choix invalide.")
