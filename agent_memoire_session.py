"""
AGENT MÉMOIRE SESSION — Se souvient de tout
Retient chaque décision, achat, étape et agent construit.
Te donne un briefing complet à tout moment pour reprendre exactement là où on s'est arrêté.

Usage : python agent_memoire_session.py
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

HISTORIQUE_FILE = "historique_caelum.json"


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


def charger_historique():
    if os.path.exists(HISTORIQUE_FILE):
        try:
            with open(HISTORIQUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def sauvegarder_historique(h):
    with open(HISTORIQUE_FILE, "w", encoding="utf-8") as f:
        json.dump(h, f, ensure_ascii=False, indent=2)


def streamer(instructions, prompt, label=""):
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    model = _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=2500),
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


# ─────────────────────────────────────────────────────────────
# 1. BRIEFING COMPLET — Tout ce qu'on a fait ensemble
# ─────────────────────────────────────────────────────────────

def briefing_complet():
    h = charger_historique()
    agents = h.get("agents_construits", [])
    achats = h.get("achats_et_depenses", [])
    decisions = h.get("decisions_cles", [])
    milestones = h.get("milestones", [])
    infra = h.get("infrastructure", {})
    legal = h.get("statut_legal", {})
    services = h.get("services_vendus", [])

    faits = [m for m in milestones if m.get("statut") == "fait"]
    en_attente = [m for m in milestones if m.get("statut") == "en_attente"]
    en_cours = [m for m in milestones if m.get("statut") == "en_cours"]

    print(f"\n{'═'*65}")
    print(f"  MÉMOIRE COMPLÈTE — {h.get('projet', 'Caelum Partners')}")
    print(f"  Fondatrice : {h.get('fondatrice', '')} | {h.get('email', '')}")
    print(f"{'═'*65}\n")

    print(f"  ── CE QU'ON A CONSTRUIT ENSEMBLE ──\n")

    print(f"  📌 INFRASTRUCTURE")
    dns = infra.get("domaine", {})
    heberg = infra.get("hebergement", {})
    api = infra.get("api_ia", {})
    print(f"     Domaine   : {dns.get('nom','')} (acheté sur {dns.get('registrar','')})")
    print(f"     DNS       : {dns.get('nameservers','')}")
    print(f"     Hébergement : {heberg.get('service','')} — {heberg.get('cout','')} — Statut : {heberg.get('statut','')}")
    print(f"     API IA    : {api.get('service','')} — {api.get('cout','')}")
    print(f"     Note API  : {api.get('note','')}")

    print(f"\n  💰 ACHATS & DÉPENSES")
    for a in achats:
        print(f"     [{a.get('date','')}] {a.get('quoi','')} — {a.get('montant','')} ({a.get('fournisseur','')})")
        print(f"     Note : {a.get('note','')}")

    print(f"\n  ⚖️  STATUT LÉGAL")
    print(f"     {legal.get('statut','')} | {legal.get('pays','')}")
    print(f"     Stripe : {legal.get('stripe','')}")
    print(f"     ASBL : {legal.get('asbl','')}")

    print(f"\n  💼 SERVICES VENDUS")
    for s in services:
        print(f"     • {s.get('nom','')} : {s.get('prix','')}€ — {s.get('delai','')}")

    print(f"\n  🤖 AGENTS CONSTRUITS ({len(agents)})")
    for i in range(0, len(agents), 4):
        ligne = agents[i:i+4]
        print(f"     {' | '.join(f'{a:<30}' for a in ligne)}")

    print(f"\n  🎯 DÉCISIONS CLÉS")
    for d in decisions:
        print(f"     [{d.get('date','')}] {d.get('decision','')}")
        print(f"     Raison : {d.get('raison','')}\n")

    print(f"  ── ÉTAT ACTUEL ──\n")
    print(f"  ✅ FAIT ({len(faits)}) :")
    for m in faits:
        print(f"     ✓ {m['etape']}")
    print(f"\n  🔄 EN COURS ({len(en_cours)}) :")
    for m in en_cours:
        print(f"     ⚙ {m['etape']}")
    print(f"\n  ⏳ EN ATTENTE ({len(en_attente)}) :")
    for m in en_attente:
        print(f"     □ {m['etape']}")


# ─────────────────────────────────────────────────────────────
# 2. BRIEFING IA — Résumé intelligent de la session
# ─────────────────────────────────────────────────────────────

def briefing_ia():
    h = charger_historique()

    streamer(
        """Tu es l'assistant personnel de Chaima Mhadbi, fondatrice de Caelum Partners.
Tu connais TOUTE l'histoire du projet depuis le début.
Tu fais un briefing complet, chaleureux et précis :
1. Résumé de ce qu'on a accompli ensemble
2. État exact de l'infrastructure
3. Ce qui reste à faire par ordre de priorité
4. Prochain pas concret immédiat
5. Message d'encouragement final (elle a accompli beaucoup)

Ton : professionnel mais humain. Tu te souviens de tout.""",
        json.dumps(h, ensure_ascii=False, indent=2),
        "BRIEFING COMPLET — Tout ce qu'on a construit ensemble"
    )


# ─────────────────────────────────────────────────────────────
# 3. AJOUTER UN ÉVÉNEMENT — Mémoriser quelque chose de nouveau
# ─────────────────────────────────────────────────────────────

def ajouter_evenement():
    print("\n  ── NOUVEL ÉVÉNEMENT À MÉMORISER ──")
    print("  Types : achat / décision / milestone / note / problème / victoire")
    type_event = input("  Type → ").strip() or "note"
    description = input("  Description → ").strip()
    if not description:
        return

    h = charger_historique()
    if "evenements" not in h:
        h["evenements"] = []

    h["evenements"].append({
        "date": datetime.now().isoformat()[:10],
        "heure": datetime.now().strftime("%H:%M"),
        "type": type_event,
        "description": description,
    })

    # Si c'est un achat, l'ajouter aussi dans achats_et_depenses
    if type_event == "achat":
        montant = input("  Montant (ex: 4.47$) → ").strip()
        fournisseur = input("  Fournisseur → ").strip()
        h["achats_et_depenses"].append({
            "date": datetime.now().isoformat()[:10],
            "quoi": description,
            "fournisseur": fournisseur,
            "montant": montant,
            "statut": "actif",
            "note": f"Ajouté le {datetime.now().strftime('%d/%m/%Y')}"
        })

    # Si c'est un milestone accompli
    if type_event == "milestone" or type_event == "victoire":
        h["milestones"].append({
            "date": datetime.now().isoformat()[:10],
            "etape": description,
            "statut": "fait"
        })

    sauvegarder_historique(h)
    print(f"\n  ✅ Mémorisé : {description}")


# ─────────────────────────────────────────────────────────────
# 4. PROCHAINE ÉTAPE — Que faire maintenant
# ─────────────────────────────────────────────────────────────

def prochaine_etape():
    h = charger_historique()
    en_attente = [m for m in h.get("milestones", []) if m.get("statut") == "en_attente"]
    en_cours = [m for m in h.get("milestones", []) if m.get("statut") == "en_cours"]
    agents = h.get("agents_construits", [])
    services = h.get("services_vendus", [])

    streamer(
        """Tu es le conseiller stratégique de Chaima Mhadbi.
Tu connais tout l'historique de Caelum Partners.
Tu lui dis EXACTEMENT quoi faire maintenant, dans quel ordre, et avec quel agent.
Sois précis, direct, encourageant. Maximum 10 actions.""",
        f"""En attente : {[m['etape'] for m in en_attente]}
En cours : {[m['etape'] for m in en_cours]}
Agents disponibles : {agents[:20]}
Services : {services}
Infra : domaine actif, Cloudflare configuré, site en 403 (pas de contenu)
Objectif immédiat : premier client à 500€""",
        "PROCHAINE ÉTAPE — Que faire maintenant"
    )


# ─────────────────────────────────────────────────────────────
# 5. VOIR TOUS LES ÉVÉNEMENTS
# ─────────────────────────────────────────────────────────────

def voir_evenements():
    h = charger_historique()
    evenements = h.get("evenements", [])

    if not evenements:
        print("\n  Aucun événement enregistré.")
        return

    print(f"\n{'═'*65}")
    print(f"  JOURNAL D'ÉVÉNEMENTS — {len(evenements)} entrées")
    print(f"{'═'*65}\n")

    for e in reversed(evenements[-20:]):  # 20 derniers
        icone = {"achat": "💰", "décision": "🎯", "milestone": "✅",
                 "victoire": "🏆", "problème": "⚠️", "note": "📝"}.get(e.get("type", ""), "•")
        print(f"  {icone} [{e.get('date','')} {e.get('heure','')}] {e.get('description','')}")


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT MÉMOIRE SESSION — Se souvient de tout")
    print("  Caelum Partners x Claude")
    print("═"*65)

    while True:
        print("\n  1. Briefing complet — Tout ce qu'on a fait ensemble")
        print("  2. Résumé IA — Analyse intelligente de la progression")
        print("  3. Ajouter un événement — Mémoriser quelque chose")
        print("  4. Prochaine étape — Que faire maintenant")
        print("  5. Voir le journal d'événements")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            briefing_complet()
        elif choix == "2":
            briefing_ia()
        elif choix == "3":
            ajouter_evenement()
        elif choix == "4":
            prochaine_etape()
        elif choix == "5":
            voir_evenements()
        else:
            print("  Choix invalide.")
