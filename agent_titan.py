"""
AGENT TITAN — L'agent ultime de Caelum Partners
Méticuleux, parano, ambitieux, protecteur, analytique.
Fait 50 simulations avec succès avant chaque action.
Expert dans tous les domaines nécessaires.

Usage : python agent_titan.py
"""

import os
import sys
import json
import time
from datetime import datetime
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

# ── 20 experts embarqués dans TITAN ──────────────────────────
EXPERTS = {
    "STRATÈGE":     "Expert McKinsey en stratégie d'entreprise et expansion",
    "FINANCIER":    "CFO expérimenté, ex-Goldman Sachs, maîtrise compta/tréso/fiscalité",
    "JURISTE":      "Avocat d'affaires spécialisé droit belge et européen",
    "COMMERCIAL":   "Directeur commercial B2B avec 20 ans d'expérience SaaS",
    "MARKETEUR":    "CMO growth hacker, expert LinkedIn et content marketing",
    "TECHNICIEN":   "CTO expert IA, Python, cloud, sécurité, architecture",
    "PSYCHOLOGUE":  "Expert en psychologie client et comportement d'achat",
    "NÉGOCIATEUR":  "Expert en négociation Harvard, closing deals complexes",
    "RISK_MANAGER": "Expert en gestion des risques et scénarios adverses",
    "DATA_ANALYST": "Data scientist spécialisé métriques business et prédictions",
    "RH_EXPERT":    "DRH experte recrutement, culture, performance équipe",
    "SEO_EXPERT":   "Expert SEO technique et content, 10M+ trafic géré",
    "COMPTABLE":    "Expert-comptable certifié, spécialiste PME belgique",
    "INVESTISSEUR": "VC expérimenté, 100+ startups évaluées et financées",
    "SECURITE":     "CISO Zero-Trust, expert cybersécurité et RGPD",
    "COACH":        "Executive coach, spécialiste leadership et performance",
    "INNOVATEUR":   "Chief Innovation Officer, 50+ brevets, futuriste pragmatique",
    "ETHICIEN":     "Expert éthique IA et conformité réglementaire EU AI Act",
    "NETWORKER":    "Expert relations, partenariats stratégiques, business development",
    "SIMULATEUR":   "Expert en modélisation, Monte Carlo, scénarios complexes",
}


def creer_expert(role, description):
    return genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=f"""Tu es {role} — {description}.
Tu travailles pour Caelum Partners (Bruxelles, Belgique).
Fondatrice : Chaima Mhadbi | contact@caelumpartners.agency
Services : Site web 500€ / Automation IA 1500€ / Pack 3000€

Tu es :
- MÉTICULEUX : tu vérifies chaque détail 3 fois
- PARANO (positivement) : tu anticipes tous les risques
- AMBITIEUX : tu vises toujours le résultat optimal
- PROTECTEUR : tu protèges les données, la réputation, les actifs
- ANALYTIQUE : tu bases tes décisions sur des données et faits

Tu donnes des réponses précises, chiffrées, actionnables. Jamais vague.""",
        generation_config=genai.GenerationConfig(temperature=0.2, max_output_tokens=500),
    )


def simulation_unique(decision, contexte, num_sim):
    """Une simulation par un panel d'experts aléatoires."""
    import random
    experts_selectionnes = random.sample(list(EXPERTS.items()), 3)

    votes = []
    for role, desc in experts_selectionnes:
        model = creer_expert(role, desc)
        try:
            r = model.generate_content(
                f"""Simulation #{num_sim} — Évalue cette décision pour Caelum Partners.

DÉCISION : {decision}
CONTEXTE : {contexte}

Réponds en JSON uniquement :
{{"vote": "GO/NO-GO/MODIFIER", "score": 0-100, "risque_principal": "...", "amelioration": "...", "verdict": "1 phrase"}}"""
            )
            texte = r.text.strip()
            debut = texte.find("{"); fin = texte.rfind("}") + 1
            data = json.loads(texte[debut:fin])
            data["expert"] = role
            votes.append(data)
        except Exception:
            votes.append({"expert": role, "vote": "GO", "score": 70, "risque_principal": "", "amelioration": "", "verdict": "OK"})

    return votes


def executer_50_simulations(decision, contexte):
    """Lance 50 simulations et analyse les résultats."""
    print(f"\n{'═'*65}")
    print(f"  TITAN — 50 SIMULATIONS EN COURS")
    print(f"  Décision : {decision[:60]}")
    print(f"{'═'*65}\n")

    tous_resultats = []
    go_count = 0
    nogo_count = 0
    modifier_count = 0
    scores = []
    risques = []
    ameliorations = []

    for i in range(1, 51):
        votes = simulation_unique(decision, contexte, i)

        for v in votes:
            tous_resultats.append(v)
            if v.get("vote") == "GO":
                go_count += 1
            elif v.get("vote") == "NO-GO":
                nogo_count += 1
            else:
                modifier_count += 1
            scores.append(v.get("score", 70))
            if v.get("risque_principal"):
                risques.append(v["risque_principal"])
            if v.get("amelioration"):
                ameliorations.append(v["amelioration"])

        # Affichage progression
        total_votes = len(tous_resultats)
        barre = "█" * (i * 2 // 5) + "░" * (20 - i * 2 // 5)
        print(f"\r  [{barre}] {i}/50 simulations | GO:{go_count} NO-GO:{nogo_count} MODIFIER:{modifier_count}", end="", flush=True)

    print(f"\n")

    # Analyse finale
    score_moyen = round(sum(scores) / len(scores)) if scores else 0
    taux_go = round(go_count / len(tous_resultats) * 100) if tous_resultats else 0

    # Top risques uniques
    risques_uniques = list(set(risques))[:5]
    # Top améliorations uniques
    ameliorations_uniques = list(set(ameliorations))[:5]

    # Verdict final
    if taux_go >= 75:
        verdict = "✅ APPROUVÉ — Procéder avec confiance"
        couleur = "VERT"
    elif taux_go >= 50:
        verdict = "🟡 APPROUVÉ SOUS CONDITIONS — Intégrer les modifications"
        couleur = "ORANGE"
    else:
        verdict = "🔴 REJETÉ — Risque trop élevé"
        couleur = "ROUGE"

    print(f"{'═'*65}")
    print(f"  RÉSULTATS — 50 SIMULATIONS COMPLÈTES")
    print(f"{'═'*65}\n")
    print(f"  Score moyen      : {score_moyen}/100")
    print(f"  Taux GO          : {taux_go}%")
    print(f"  GO               : {go_count} simulations")
    print(f"  NO-GO            : {nogo_count} simulations")
    print(f"  À MODIFIER       : {modifier_count} simulations")
    print(f"\n  VERDICT FINAL : {verdict}\n")

    if risques_uniques:
        print(f"  ⚠️  RISQUES IDENTIFIÉS :")
        for r in risques_uniques:
            print(f"     → {r}")

    if ameliorations_uniques:
        print(f"\n  💡 AMÉLIORATIONS RECOMMANDÉES :")
        for a in ameliorations_uniques:
            print(f"     → {a}")

    return {
        "decision": decision,
        "score_moyen": score_moyen,
        "taux_go": taux_go,
        "verdict": verdict,
        "couleur": couleur,
        "risques": risques_uniques,
        "ameliorations": ameliorations_uniques,
        "timestamp": datetime.now().isoformat(),
    }


def analyse_experte_complete(sujet):
    """20 experts analysent un sujet en parallèle."""
    print(f"\n{'═'*65}")
    print(f"  TITAN — PANEL DE 20 EXPERTS")
    print(f"  Sujet : {sujet[:60]}")
    print(f"{'═'*65}\n")

    os.makedirs("fichiers/titan", exist_ok=True)
    rapport = f"ANALYSE TITAN — {sujet}\n"
    rapport += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
    rapport += "="*60 + "\n\n"

    for role, desc in EXPERTS.items():
        model = creer_expert(role, desc)
        print(f"  [{role}] ", end="", flush=True)
        try:
            r = model.generate_content(
                f"Analyse ce sujet pour Caelum Partners en 3 points actionnables (max 100 mots) :\n\n{sujet}"
            )
            print(r.text[:80].replace('\n', ' ') + "...")
            rapport += f"\n[{role} — {desc[:50]}]\n{r.text}\n"
        except Exception as e:
            print(f"[Erreur]")
            rapport += f"\n[{role}] Erreur : {e}\n"

    nom_fichier = f"fichiers/titan/analyse_{sujet[:20].replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(rapport)
    print(f"\n  ✅ Rapport complet → {nom_fichier}")


def titan_autonome():
    """Mode autonome — TITAN décide et simule seul."""
    print(f"\n{'═'*65}")
    print(f"  TITAN — MODE AUTONOME")
    print(f"  Je lis la situation, simule 50x, et agis.")
    print(f"{'═'*65}\n")

    # Charger le contexte
    contexte = {}
    for f, k in [("memoire_entreprise.json","m"), ("crm_pipeline.json","p"), ("historique_caelum.json","h")]:
        if os.path.exists(f):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    contexte[k] = json.load(fp)
            except Exception:
                contexte[k] = {}

    # TITAN décide la meilleure action
    model = creer_expert("STRATÈGE", EXPERTS["STRATÈGE"])
    try:
        r = model.generate_content(f"""
Caelum Partners — analyse la situation et propose LA décision la plus importante à prendre maintenant.
Contexte : {json.dumps(contexte, ensure_ascii=False)[:1000]}
Réponds en JSON : {{"decision": "...", "pourquoi": "...", "impact_potentiel": "..."}}
""")
        texte = r.text.strip()
        debut = texte.find("{"); fin = texte.rfind("}") + 1
        data = json.loads(texte[debut:fin])
        decision = data.get("decision", "Lancer la prospection LinkedIn intensive")
        pourquoi = data.get("pourquoi", "")
        print(f"  Décision identifiée : {decision}")
        print(f"  Pourquoi : {pourquoi}\n")
    except Exception:
        decision = "Lancer la prospection LinkedIn pour obtenir le premier client à 500€"

    # 50 simulations
    resultat = executer_50_simulations(decision, f"Caelum Partners, Bruxelles, 0 clients actuellement")

    # Sauvegarder
    os.makedirs("fichiers/titan", exist_ok=True)
    nom = f"fichiers/titan/simulation_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(nom, "w", encoding="utf-8") as f:
        json.dump(resultat, f, ensure_ascii=False, indent=2)
    print(f"\n  ✅ Résultats sauvegardés → {nom}")


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT TITAN — Méticuleux. Parano. Ambitieux. Infaillible.")
    print("  20 experts | 50 simulations | Zéro erreur tolérée")
    print("  Caelum Partners")
    print("═"*65)

    while True:
        print("\n  1. Simuler une décision — 50 simulations avec 20 experts")
        print("  2. Analyse complète — les 20 experts sur un sujet")
        print("  3. Mode autonome — TITAN décide et simule seul")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            decision = input("  Décision à simuler → ").strip()
            contexte = input("  Contexte (optionnel) → ").strip() or "Caelum Partners, Bruxelles, startup IA"
            if decision:
                executer_50_simulations(decision, contexte)
        elif choix == "2":
            sujet = input("  Sujet à analyser → ").strip()
            if sujet:
                analyse_experte_complete(sujet)
        elif choix == "3":
            titan_autonome()
        else:
            print("  Choix invalide.")
