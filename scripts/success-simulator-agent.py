#!/usr/bin/env python3
"""
Success Simulator Agent — Caelum Partners
Moteur de simulation de probabilité de succès pour chaque appel à projet
"""
import json

CAELUM_PROFILE = {
    "forme_juridique": "SPRL",
    "ancienneté_mois": 18,
    "secteur": ["compliance", "ESG", "IA", "SaaS", "droits humains"],
    "localisation": "Bruxelles",
    "effectif": 2,
    "ca_annuel_eur": 45000,
    "investissement_r&d_pct": 0.80,
    "partenariats_academiques": False,
    "partenariats_industriels": False,
    "publications": 0,
    "traction": "early (3 clients beta)",
    "tech_stack": ["Next.js", "Python", "IA multi-agents"],
    "domaine_innovation": "compliance CSDDD EU 2024/1760",
    "differenciateurs": ["first-mover CSDDD", "IA multi-agents", "droits humains spécifique"],
    "faiblesses": ["équipe petite", "pas encore de revenus stables", "pas de partenaire académique"],
}

ALL_CALLS = [
  {
    "id": "INV-2026-001",
    "nom": "Innoviris — Proof of Concept",
    "organisme": "Innoviris (Bruxelles)",
    "type": "subvention",
    "montant_min": 25000, "montant_max": 100000,
    "taux_cofinancement": 0.70,
    "eligibilite": ["PME", "startup", "indépendant"],
    "secteurs": ["tech", "IA", "digital", "innovation sociale"],
    "criteres_selection": ["innovation", "faisabilité technique", "marché", "équipe"],
    "deadline_typical": "Rolling (dépôt continu)",
    "duree_projet_mois": 12,
    "delai_reponse_semaines": 8,
    "taux_succes_historique": 0.35,
    "difficulte": "moyen",
    "notes": "Idéal pour POC technique CaelumSwarm. Rolling = aucune deadline fixe.",
    "requis_partenaire_academique": False,
    "requis_partenaire_industriel": False,
    "requis_consortium": False,
    "anciennete_min_mois": 0,
    "ca_min_eur": 0,
    "effectif_min": 1,
  },
  {
    "id": "INV-2026-002",
    "nom": "Innoviris — Bridge",
    "organisme": "Innoviris (Bruxelles)",
    "type": "subvention",
    "montant_min": 100000, "montant_max": 500000,
    "taux_cofinancement": 0.60,
    "eligibilite": ["PME", "startup post-POC"],
    "secteurs": ["tech", "IA", "impact social", "ESG"],
    "criteres_selection": ["scalabilité", "impact", "partenariats", "équipe", "traction marché"],
    "deadline_typical": "2 sessions/an (mars et septembre)",
    "duree_projet_mois": 24,
    "delai_reponse_semaines": 12,
    "taux_succes_historique": 0.25,
    "difficulte": "élevé",
    "notes": "Nécessite lettre d'intention partenaire industriel.",
    "requis_partenaire_academique": False,
    "requis_partenaire_industriel": True,
    "requis_consortium": False,
    "anciennete_min_mois": 12,
    "ca_min_eur": 0,
    "effectif_min": 1,
  },
  {
    "id": "WAL-2026-001",
    "nom": "Chèques-Entreprises Numérique",
    "organisme": "Agence du Numérique (Wallonie)",
    "type": "chèque",
    "montant_min": 5000, "montant_max": 25000,
    "taux_cofinancement": 0.75,
    "eligibilite": ["PME", "indépendant", "startup"],
    "secteurs": ["digitalisation", "IA", "cybersécurité", "cloud"],
    "criteres_selection": ["utilité", "simplicité", "impact immédiat"],
    "deadline_typical": "Rolling",
    "duree_projet_mois": 6,
    "delai_reponse_semaines": 4,
    "taux_succes_historique": 0.60,
    "difficulte": "facile",
    "notes": "Très accessible. Pour outils numériques internes ou conseil.",
    "requis_partenaire_academique": False,
    "requis_partenaire_industriel": False,
    "requis_consortium": False,
    "anciennete_min_mois": 0,
    "ca_min_eur": 0,
    "effectif_min": 1,
  },
  {
    "id": "FED-2026-001",
    "nom": "FEDER Bruxelles — Innovation & Croissance",
    "organisme": "SRIB / Brussels Invest & Export",
    "type": "subvention",
    "montant_min": 50000, "montant_max": 300000,
    "taux_cofinancement": 0.50,
    "eligibilite": ["PME bruxelloises", "startup"],
    "secteurs": ["innovation", "emploi", "développement durable", "tech"],
    "criteres_selection": ["création emploi", "ancrage bruxellois", "innovation", "viabilité"],
    "deadline_typical": "Session annuelle (octobre)",
    "duree_projet_mois": 18,
    "delai_reponse_semaines": 16,
    "taux_succes_historique": 0.30,
    "difficulte": "moyen-élevé",
    "notes": "Critère emploi fort — prévoir plan recrutement bruxellois.",
    "requis_partenaire_academique": False,
    "requis_partenaire_industriel": False,
    "requis_consortium": False,
    "anciennete_min_mois": 0,
    "ca_min_eur": 0,
    "effectif_min": 1,
  },
  {
    "id": "EU-2026-001",
    "nom": "EIC Accelerator — Open",
    "organisme": "European Innovation Council",
    "type": "grant + equity",
    "montant_min": 500000, "montant_max": 2500000,
    "taux_cofinancement": 0.70,
    "eligibilite": ["startup EU", "scale-up", "PME"],
    "secteurs": ["deeptech", "IA", "green tech", "healthtech", "compliance tech"],
    "criteres_selection": ["innovation de rupture", "scalabilité EU", "équipe world-class", "marché global"],
    "deadline_typical": "3 sessions/an",
    "duree_projet_mois": 24,
    "delai_reponse_semaines": 20,
    "taux_succes_historique": 0.05,
    "difficulte": "très élevé",
    "notes": "Très compétitif. Nécessite pitch vidéo + full proposal. Investissement equity possible.",
    "requis_partenaire_academique": False,
    "requis_partenaire_industriel": False,
    "requis_consortium": False,
    "anciennete_min_mois": 0,
    "ca_min_eur": 0,
    "effectif_min": 1,
  },
  {
    "id": "EU-2026-002",
    "nom": "Horizon Europe — ERC Starting Grant",
    "organisme": "European Research Council",
    "type": "grant recherche",
    "montant_min": 1000000, "montant_max": 1500000,
    "taux_cofinancement": 1.0,
    "eligibilite": ["chercheurs 2-7 ans post-doctorat", "institution hôte EU"],
    "secteurs": ["recherche fondamentale", "IA", "droits humains", "droit"],
    "criteres_selection": ["excellence scientifique", "innovation", "faisabilité"],
    "deadline_typical": "Annuel (novembre)",
    "duree_projet_mois": 60,
    "delai_reponse_semaines": 24,
    "taux_succes_historique": 0.12,
    "difficulte": "très élevé",
    "notes": "Requiert PI avec affiliation académique. Partenariat ULB/VUB recommandé.",
    "requis_partenaire_academique": True,
    "requis_partenaire_industriel": False,
    "requis_consortium": False,
    "anciennete_min_mois": 0,
    "ca_min_eur": 0,
    "effectif_min": 1,
  },
  {
    "id": "BEI-2026-001",
    "nom": "BEI — European Fund for Strategic Investments (EFSI)",
    "organisme": "Banque Européenne d'Investissement",
    "type": "prêt/garantie",
    "montant_min": 100000, "montant_max": 1000000,
    "taux_cofinancement": 0.0,
    "eligibilite": ["PME EU", "startup 3+ ans"],
    "secteurs": ["innovation", "numérique", "ESG", "infrastructure"],
    "criteres_selection": ["viabilité financière", "impact économique", "innovation"],
    "deadline_typical": "Rolling",
    "duree_projet_mois": 36,
    "delai_reponse_semaines": 12,
    "taux_succes_historique": 0.40,
    "difficulte": "moyen",
    "notes": "Prêt, pas subvention. Via banque partenaire (BNP, ING, KBC).",
    "requis_partenaire_academique": False,
    "requis_partenaire_industriel": False,
    "requis_consortium": False,
    "anciennete_min_mois": 36,
    "ca_min_eur": 50000,
    "effectif_min": 3,
  },
  {
    "id": "HE-2026-001",
    "nom": "Horizon Europe — RIA (Research & Innovation Action)",
    "organisme": "Commission Européenne",
    "type": "grant consortium",
    "montant_min": 200000, "montant_max": 500000,
    "taux_cofinancement": 1.0,
    "eligibilite": ["consortium 3+ partenaires EU", "PME éligible"],
    "secteurs": ["compliance", "ESG", "droits humains", "IA responsable", "CSDD"],
    "criteres_selection": ["excellence", "impact", "implémentation", "équipe pluridisciplinaire"],
    "deadline_typical": "Appels thématiques (voir Work Programme 2025-2027)",
    "duree_projet_mois": 36,
    "delai_reponse_semaines": 18,
    "taux_succes_historique": 0.15,
    "difficulte": "élevé",
    "notes": "Cluster 3 (Civil Security) ou Cluster 6 (Food/Bio/Nat Res/Env) les plus pertinents.",
    "requis_partenaire_academique": False,
    "requis_partenaire_industriel": False,
    "requis_consortium": True,
    "anciennete_min_mois": 0,
    "ca_min_eur": 0,
    "effectif_min": 1,
  },
]


def score_eligibilite(call: dict, profile: dict) -> float:
    """Score d'éligibilité (0-1) : la société satisfait-elle les critères formels ?"""
    score = 1.0
    # Ancienneté
    if profile["ancienneté_mois"] < call.get("anciennete_min_mois", 0):
        score *= 0.3
    # CA minimum
    if profile["ca_annuel_eur"] < call.get("ca_min_eur", 0):
        score *= 0.5
    # Effectif minimum
    if profile["effectif"] < call.get("effectif_min", 1):
        score *= 0.6
    # Partenaire académique requis
    if call.get("requis_partenaire_academique") and not profile["partenariats_academiques"]:
        score *= 0.1
    # Partenaire industriel requis
    if call.get("requis_partenaire_industriel") and not profile["partenariats_industriels"]:
        score *= 0.5
    # Consortium requis
    if call.get("requis_consortium"):
        score *= 0.4  # difficile sans consortium préexistant
    return min(1.0, max(0.0, score))


def score_adequation_secteur(call: dict, profile: dict) -> float:
    """Score d'adéquation sectorielle (0-1)."""
    secteurs_call = [s.lower() for s in call["secteurs"]]
    secteurs_profile = [s.lower() for s in profile["secteur"]]
    overlap = len(set(secteurs_call) & set(secteurs_profile))
    max_possible = max(len(secteurs_call), 1)
    base_score = overlap / max_possible
    # Bonus si CSDDD/compliance explicite dans critères
    if any("csddd" in c.lower() or "compliance" in c.lower() for c in call["criteres_selection"]):
        base_score = min(1.0, base_score + 0.2)
    return min(1.0, base_score)


def score_maturite(call: dict, profile: dict) -> float:
    """Score de maturité tech/marché (0-1)."""
    score = 0.5  # Base
    # Traction
    if "beta" in profile["traction"].lower():
        score += 0.15
    # R&D investment
    if profile["investissement_r&d_pct"] >= 0.7:
        score += 0.15
    # Tech stack moderne
    if "IA multi-agents" in profile["tech_stack"]:
        score += 0.10
    # Ancienneté réduit le score pour les appels qui veulent de la maturité
    if "scalabilité" in " ".join(call["criteres_selection"]).lower() and profile["ancienneté_mois"] < 24:
        score -= 0.15
    # Revenus stables
    if profile["ca_annuel_eur"] < 50000:
        score -= 0.10
    return min(1.0, max(0.0, score))


def score_equipe(call: dict, profile: dict) -> float:
    """Score d'équipe (0-1)."""
    score = 0.5
    # Effectif réduit
    if profile["effectif"] <= 2:
        score -= 0.15
    # Faiblesses déclarées
    if "équipe petite" in profile["faiblesses"]:
        score -= 0.10
    # Expertise domaine
    if "compliance" in profile["secteur"] and "compliance" in " ".join(call["secteurs"]).lower():
        score += 0.20
    # First-mover advantage
    if "first-mover CSDDD" in profile["differenciateurs"]:
        score += 0.15
    # Publications (aucune → pénalité pour appels recherche)
    if profile["publications"] == 0 and "recherche" in call["type"].lower():
        score -= 0.30
    return min(1.0, max(0.0, score))


def score_dossier_potentiel(call: dict, profile: dict) -> float:
    """Score potentiel de dossier (0-1) : peut-on rédiger un bon dossier ?"""
    score = 0.6  # Base neutre
    # Innovation claire
    if profile["domaine_innovation"]:
        score += 0.15
    # Différenciateurs forts
    score += min(0.15, len(profile["differenciateurs"]) * 0.05)
    # Faiblesses
    score -= min(0.20, len(profile["faiblesses"]) * 0.05)
    # Critères de sélection matchables
    criteres = " ".join(call["criteres_selection"]).lower()
    if "innovation" in criteres:
        score += 0.05
    if "équipe world-class" in criteres and profile["effectif"] <= 2:
        score -= 0.15
    return min(1.0, max(0.0, score))


def simulate_success(call: dict, profile: dict) -> dict:
    """Calcule la probabilité de succès complète pour un appel."""
    # Scores pondérés
    weights = {
        "eligibilite": 0.30,
        "adequation_secteur": 0.25,
        "maturite": 0.20,
        "equipe": 0.15,
        "dossier_potentiel": 0.10,
    }
    scores = {
        "eligibilite": score_eligibilite(call, profile),
        "adequation_secteur": score_adequation_secteur(call, profile),
        "maturite": score_maturite(call, profile),
        "equipe": score_equipe(call, profile),
        "dossier_potentiel": score_dossier_potentiel(call, profile),
    }
    score_moyen = sum(scores[k] * weights[k] for k in weights)

    # Probabilités
    prob_brute = score_moyen * call["taux_succes_historique"] * 100
    prob_bon_dossier = min(95.0, prob_brute * 1.75)  # +75% avec bon dossier
    prob_coaching = min(95.0, prob_bon_dossier * 1.20)  # +20% avec coaching spécialisé

    # Verdict
    if prob_bon_dossier >= 30:
        verdict = "RECOMMANDÉ — Priorité haute"
    elif prob_bon_dossier >= 15:
        verdict = "ENVISAGEABLE — Priorité moyenne"
    elif prob_bon_dossier >= 5:
        verdict = "RISQUÉ — Priorité basse"
    else:
        verdict = "DÉCONSEILLÉ — Critères non remplis"

    # Axes d'amélioration
    axes = []
    if scores["eligibilite"] < 0.7:
        axes.append("Renforcer l'éligibilité (partenaires, ancienneté, CA)")
    if scores["adequation_secteur"] < 0.6:
        axes.append("Mieux aligner le positionnement sectoriel")
    if scores["maturite"] < 0.6:
        axes.append("Renforcer la traction marché (clients payants, MRR)")
    if scores["equipe"] < 0.6:
        axes.append("Étoffer l'équipe ou mentionner les advisors")
    if scores["dossier_potentiel"] < 0.7:
        axes.append("Ajouter lettre de soutien client beta ou partenaire")
    if not axes:
        axes.append("Renforcer section innovation et impact CSDDD")
        axes.append("Ajouter témoignage/lettre de soutien client beta")

    # Score global (0-100)
    score_global = int(score_moyen * 100)

    # ROI espéré
    roi_esperé = int(call["montant_max"] * call["taux_cofinancement"] * prob_bon_dossier / 100)

    return {
        "call_id": call["id"],
        "nom": call["nom"],
        "probabilite_brute_pct": round(prob_brute, 1),
        "probabilite_avec_bon_dossier_pct": round(prob_bon_dossier, 1),
        "probabilite_avec_coaching_pct": round(prob_coaching, 1),
        "verdict": verdict,
        "axes_amélioration": axes,
        "delai_preparation_semaines": call["delai_reponse_semaines"] // 2,
        "roi_esperé_eur": roi_esperé,
        "score_global": score_global,
        "scores_détail": {k: round(v, 2) for k, v in scores.items()},
    }


def rank_calls(profile: dict) -> list:
    """Classe tous les appels par score ROI espéré pondéré par probabilité."""
    results = [simulate_success(call, profile) for call in ALL_CALLS]
    # Tri par probabilité_avec_bon_dossier_pct × montant_max
    for i, r in enumerate(results):
        call = ALL_CALLS[i]
        r["_sort_key"] = r["probabilite_avec_bon_dossier_pct"] * call["montant_max"]
    results.sort(key=lambda x: x["_sort_key"], reverse=True)
    for r in results:
        del r["_sort_key"]
    return results


if __name__ == "__main__":
    print("=" * 65)
    print("SUCCESS SIMULATOR AGENT — Caelum Partners")
    print("=" * 65)

    rankings = rank_calls(CAELUM_PROFILE)

    print(f"\n{'Rang':<4} {'Appel':<42} {'P(bon dossier)':<16} {'ROI espéré':>12} {'Verdict'}")
    print("-" * 100)
    for i, r in enumerate(rankings, 1):
        nom_short = r["nom"][:40]
        print(f"  {i:<3} {nom_short:<42} {r['probabilite_avec_bon_dossier_pct']:>5.1f}%          {r['roi_esperé_eur']:>10,} EUR   {r['verdict']}")

    print("\n[DÉTAIL TOP 3]")
    for r in rankings[:3]:
        print(f"\n  >>> {r['nom']}")
        print(f"      Probabilité brute         : {r['probabilite_brute_pct']}%")
        print(f"      Avec bon dossier          : {r['probabilite_avec_bon_dossier_pct']}%")
        print(f"      Avec coaching spécialisé  : {r['probabilite_avec_coaching_pct']}%")
        print(f"      Score global              : {r['score_global']}/100")
        print(f"      ROI espéré                : {r['roi_esperé_eur']:,} EUR")
        print(f"      Délai préparation         : {r['delai_preparation_semaines']} semaines")
        print(f"      Axes d'amélioration :")
        for axe in r["axes_amélioration"]:
            print(f"        - {axe}")

    print("\n[OK] Agent success-simulator opérationnel.")
