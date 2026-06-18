"""
AGENT CRM — Pipeline commercial complet
Gère les leads de la première contact jusqu'à la fidélisation.
Scoring automatique, suivi étapes, alertes relances.

Usage : python agent_crm.py
"""

import os
import sys
import json
from datetime import datetime, timedelta
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

PIPELINE_FILE = "crm_pipeline.json"

STAGES = {
    "1_lead":       "Lead identifié",
    "2_contact":    "Premier contact envoyé",
    "3_reponse":    "Réponse reçue",
    "4_appel":      "Appel/démo planifié",
    "5_proposition": "Proposition envoyée",
    "6_nego":       "Négociation en cours",
    "7_gagne":      "CLIENT GAGNÉ ✅",
    "7_perdu":      "Perdu ❌",
}

SERVICES = {
    "site_web":   {"nom": "Site web premium",      "prix": 500,  "delai": "7 jours"},
    "automation": {"nom": "Automatisation IA simple", "prix": 1500, "delai": "14 jours"},
    "pack":       {"nom": "Pack complet IA+Web+Marketing", "prix": 3000, "delai": "30 jours"},
}


def charger_pipeline():
    if os.path.exists(PIPELINE_FILE):
        try:
            with open(PIPELINE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"leads": {}, "stats": {"total_leads": 0, "gagnes": 0, "perdus": 0, "ca_signe": 0}}


def sauvegarder_pipeline(pipeline):
    with open(PIPELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(pipeline, f, ensure_ascii=False, indent=2)


def streamer(instructions, prompt, label=""):
    if label:
        print(f"\n{'═'*60}\n  {label}\n{'═'*60}\n")
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(temperature=0.3, max_output_tokens=2000),
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
# GESTION DES LEADS
# ─────────────────────────────────────────────────────────────

def ajouter_lead():
    print("\n  ── NOUVEAU LEAD ──")
    nom = input("  Nom / Entreprise → ").strip()
    if not nom:
        return
    secteur = input("  Secteur d'activité → ").strip()
    besoin = input("  Besoin identifié → ").strip()
    source = input("  Source (LinkedIn/Referral/Site/Autre) → ").strip() or "LinkedIn"
    service = input(f"  Service intéressé ({'/'.join(SERVICES.keys())}) → ").strip() or "site_web"
    contact = input("  Email ou LinkedIn → ").strip()

    pipeline = charger_pipeline()
    lead_id = f"L{len(pipeline['leads'])+1:03d}"

    pipeline["leads"][lead_id] = {
        "id": lead_id,
        "nom": nom,
        "secteur": secteur,
        "besoin": besoin,
        "source": source,
        "service": service,
        "prix": SERVICES.get(service, {}).get("prix", 500),
        "contact": contact,
        "stage": "1_lead",
        "score": 0,
        "notes": [],
        "date_entree": datetime.now().isoformat(),
        "date_dernier_contact": "",
        "date_relance": (datetime.now() + timedelta(days=3)).isoformat(),
    }
    pipeline["stats"]["total_leads"] += 1
    sauvegarder_pipeline(pipeline)

    # Score et analyse IA
    scorer_lead(pipeline["leads"][lead_id])
    print(f"\n  ✅ Lead {lead_id} ajouté : {nom}")


def scorer_lead(lead):
    """Score le lead de 0 à 100 avec l'IA."""
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction="""Tu es un expert en qualification de leads B2B.
Donne un score de 0 à 100 et une analyse en JSON uniquement :
{"score": 75, "potentiel": "élevé/moyen/faible", "raison": "1 phrase", "prochain_pas": "action précise"}""",
        generation_config=genai.GenerationConfig(temperature=0.1, max_output_tokens=200),
    )
    try:
        r = model.generate_content(
            f"Lead : {lead['nom']}, Secteur: {lead['besoin']}, Service: {lead['service']}, Source: {lead['source']}"
        )
        texte = r.text.strip()
        debut = texte.find("{"); fin = texte.rfind("}") + 1
        data = json.loads(texte[debut:fin])
        lead["score"] = data.get("score", 50)
        lead["potentiel"] = data.get("potentiel", "moyen")
        lead["analyse_ia"] = data.get("raison", "")
        lead["prochain_pas"] = data.get("prochain_pas", "")
        print(f"\n  Score IA : {lead['score']}/100 ({lead.get('potentiel','')})")
        print(f"  → {lead.get('prochain_pas','')}")

        pipeline = charger_pipeline()
        if lead["id"] in pipeline["leads"]:
            pipeline["leads"][lead["id"]].update(lead)
            sauvegarder_pipeline(pipeline)
    except Exception:
        pass


def avancer_lead():
    """Fait avancer un lead dans le pipeline."""
    pipeline = charger_pipeline()
    if not pipeline["leads"]:
        print("\n  Aucun lead. Ajoutes-en un d'abord.")
        return

    afficher_pipeline()
    lead_id = input("\n  ID du lead → ").strip().upper()
    if lead_id not in pipeline["leads"]:
        print("  Lead introuvable.")
        return

    lead = pipeline["leads"][lead_id]
    stages_list = list(STAGES.keys())
    stage_actuel_idx = stages_list.index(lead["stage"]) if lead["stage"] in stages_list else 0

    print(f"\n  Lead : {lead['nom']} — Actuellement : {STAGES[lead['stage']]}")
    print("\n  Étapes disponibles :")
    for i, (k, v) in enumerate(STAGES.items()):
        if i > stage_actuel_idx:
            print(f"  [{i+1}] {v}")

    choix = input("\n  Nouvelle étape (numéro) → ").strip()
    if not choix.isdigit() or int(choix) < 1 or int(choix) > len(stages_list):
        return

    nouveau_stage = stages_list[int(choix) - 1]
    note = input("  Note (optionnel) → ").strip()

    lead["stage"] = nouveau_stage
    lead["date_dernier_contact"] = datetime.now().isoformat()
    if note:
        lead["notes"].append({"date": datetime.now().isoformat()[:10], "note": note})

    if nouveau_stage == "7_gagne":
        pipeline["stats"]["gagnes"] += 1
        pipeline["stats"]["ca_signe"] += lead.get("prix", 0)
        print(f"\n  🎉 FÉLICITATIONS ! {lead['nom']} est client ! +{lead.get('prix',0)}€")
    elif nouveau_stage == "7_perdu":
        pipeline["stats"]["perdus"] += 1

    sauvegarder_pipeline(pipeline)

    # Message IA selon l'étape
    generer_message_etape(lead, nouveau_stage)


def generer_message_etape(lead, stage):
    """Génère le message parfait pour l'étape actuelle."""
    stage_nom = STAGES.get(stage, stage)
    service_info = SERVICES.get(lead.get("service", "site_web"), {})

    streamer(
        """Tu es le meilleur commercial de Caelum Partners.
Génère le message parfait pour cette étape du pipeline.
Le message doit être : court, personnalisé, avec une valeur ajoutée claire.
Signature : Chaima Mhadbi — Caelum Partners | contact@caelumpartners.agency""",
        f"""Lead : {lead['nom']} | Secteur : {lead.get('secteur','')}
Besoin : {lead.get('besoin','')}
Service : {service_info.get('nom','')} à {service_info.get('prix','')}€
Étape pipeline : {stage_nom}
Notes précédentes : {lead.get('notes',[])}
Source : {lead.get('source','')}""",
        f"Message — {stage_nom}"
    )


def afficher_pipeline():
    """Vue Kanban texte du pipeline."""
    pipeline = charger_pipeline()
    if not pipeline["leads"]:
        print("\n  Pipeline vide.")
        return

    print(f"\n{'═'*60}")
    print(f"  PIPELINE CRM — Caelum Partners")
    print(f"  CA signé : {pipeline['stats']['ca_signe']}€ | "
          f"Gagnés : {pipeline['stats']['gagnes']} | "
          f"Perdus : {pipeline['stats']['perdus']}")
    print(f"{'═'*60}\n")

    # Grouper par stage
    par_stage = {}
    for lead in pipeline["leads"].values():
        s = lead["stage"]
        if s not in par_stage:
            par_stage[s] = []
        par_stage[s].append(lead)

    for stage_key, stage_nom in STAGES.items():
        leads_stage = par_stage.get(stage_key, [])
        if not leads_stage:
            continue
        print(f"  ── {stage_nom} ({len(leads_stage)}) ──")
        for l in leads_stage:
            score_bar = "█" * (l.get("score", 0) // 10)
            valeur = SERVICES.get(l.get("service", ""), {}).get("prix", "?")
            print(f"  [{l['id']}] {l['nom']:<25} {score_bar:<10} {valeur}€")
            if l.get("prochain_pas"):
                print(f"       → {l['prochain_pas']}")
        print()


def alertes_relances():
    """Identifie les leads qui nécessitent une relance."""
    pipeline = charger_pipeline()
    maintenant = datetime.now()
    a_relancer = []

    for lid, lead in pipeline["leads"].items():
        if lead["stage"] in ["7_gagne", "7_perdu"]:
            continue
        date_relance = lead.get("date_relance", "")
        if date_relance:
            try:
                dr = datetime.fromisoformat(date_relance)
                if dr <= maintenant:
                    jours_retard = (maintenant - dr).days
                    a_relancer.append((jours_retard, lead))
            except Exception:
                pass

    a_relancer.sort(reverse=True)

    if not a_relancer:
        print("\n  ✅ Aucune relance urgente.")
        return

    print(f"\n{'═'*60}")
    print(f"  🔔 RELANCES URGENTES ({len(a_relancer)})")
    print(f"{'═'*60}\n")

    for retard, lead in a_relancer:
        print(f"  ⚠️  {lead['nom']} — {STAGES[lead['stage']]} — {retard}j de retard")

    print()
    lead_prioritaire = a_relancer[0][1]
    generer_message_etape(lead_prioritaire, lead_prioritaire["stage"])


def analyse_pipeline_ia():
    """Analyse globale du pipeline avec recommandations."""
    pipeline = charger_pipeline()
    if not pipeline["leads"]:
        print("\n  Pipeline vide.")
        return

    resume = json.dumps({
        "stats": pipeline["stats"],
        "leads": [{
            "nom": l["nom"], "stage": l["stage"],
            "score": l.get("score", 0), "prix": l.get("prix", 0),
            "service": l.get("service", "")
        } for l in pipeline["leads"].values()]
    }, ensure_ascii=False)

    streamer(
        """Tu es le Directeur Commercial de Caelum Partners.
Analyse le pipeline et donne :
1. État de santé du pipeline (taux conversion, valeur totale, vélocité)
2. Les 3 leads prioritaires à traiter maintenant
3. Les actions à éviter (leads à abandonner)
4. Objectif CA prochain mois
5. Stratégie pour accélérer la conversion""",
        resume,
        "ANALYSE PIPELINE — Intelligence commerciale"
    )


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  AGENT CRM — Pipeline commercial Caelum Partners")
    print("═"*60)

    while True:
        print("\n  1. Voir le pipeline complet")
        print("  2. Ajouter un nouveau lead")
        print("  3. Faire avancer un lead + générer message")
        print("  4. Alertes relances urgentes")
        print("  5. Analyse IA du pipeline")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            afficher_pipeline()
        elif choix == "2":
            ajouter_lead()
        elif choix == "3":
            avancer_lead()
        elif choix == "4":
            alertes_relances()
        elif choix == "5":
            analyse_pipeline_ia()
        else:
            print("  Choix invalide.")
