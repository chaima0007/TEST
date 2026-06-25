#!/usr/bin/env python3
"""
Project Calls Expert Agent — Caelum Partners
Base de connaissance complète des appels à projets belges & européens 2026
"""
import json
from typing import Optional

APPELS_BELGIQUE = [
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
    "url": "innoviris.brussels",
    "taux_succes_historique": 0.35,
    "difficulte": "moyen",
    "notes": "Idéal pour POC technique CaelumSwarm. Rolling = aucune deadline fixe."
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
    "url": "innoviris.brussels/bridge",
    "taux_succes_historique": 0.25,
    "difficulte": "élevé",
    "notes": "Nécessite lettre d'intention partenaire industriel."
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
    "url": "numerique.wallonie.be",
    "taux_succes_historique": 0.60,
    "difficulte": "facile",
    "notes": "Très accessible. Pour outils numériques internes ou conseil."
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
    "url": "srib.be",
    "taux_succes_historique": 0.30,
    "difficulte": "moyen-élevé",
    "notes": "Critère emploi fort — prévoir plan recrutement bruxellois."
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
    "url": "eic.ec.europa.eu/eic-funding/eic-accelerator",
    "taux_succes_historique": 0.05,
    "difficulte": "très élevé",
    "notes": "Très compétitif. Nécessite pitch vidéo + full proposal. Investissement equity possible."
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
    "url": "erc.europa.eu",
    "taux_succes_historique": 0.12,
    "difficulte": "très élevé",
    "notes": "Requiert PI avec affiliation académique. Partenariat ULB/VUB recommandé."
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
    "url": "eif.org",
    "taux_succes_historique": 0.40,
    "difficulte": "moyen",
    "notes": "Prêt, pas subvention. Via banque partenaire (BNP, ING, KBC)."
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
    "url": "ec.europa.eu/info/funding-tenders",
    "taux_succes_historique": 0.15,
    "difficulte": "élevé",
    "notes": "Cluster 3 (Civil Security) ou Cluster 6 (Food/Bio/Nat Res/Env) les plus pertinents."
  },
]

ALL_CALLS = APPELS_BELGIQUE


def search_calls(keywords: list, budget_max: Optional[int] = None, difficulte: Optional[str] = None) -> list:
    """Filtre les appels par mots-clés et critères optionnels."""
    results = []
    keywords_lower = [k.lower() for k in keywords]
    for call in ALL_CALLS:
        # Keyword matching across all string fields
        call_text = " ".join([
            call["nom"], call["organisme"],
            " ".join(call["secteurs"]),
            " ".join(call["eligibilite"]),
            " ".join(call["criteres_selection"]),
            call.get("notes", ""),
            call["type"]
        ]).lower()
        if not any(kw in call_text for kw in keywords_lower):
            continue
        if budget_max and call["montant_max"] > budget_max:
            continue
        if difficulte and call["difficulte"] != difficulte:
            continue
        results.append(call)
    return results


def get_call_details(call_id: str) -> Optional[dict]:
    """Retourne tous les détails d'un appel."""
    for call in ALL_CALLS:
        if call["id"] == call_id:
            return call
    return None


def get_recommended_calls(profile: dict) -> list:
    """Recommande les meilleurs appels pour un profil donné."""
    secteurs_profil = [s.lower() for s in profile.get("secteurs", [])]
    localisation = profile.get("localisation", "").lower()
    anciennete = profile.get("ancienneté_mois", 0)

    scored = []
    for call in ALL_CALLS:
        score = 0
        # Secteur match
        secteurs_call = [s.lower() for s in call["secteurs"]]
        overlap = len(set(secteurs_profil) & set(secteurs_call))
        score += overlap * 20

        # Localisation Brussels boost
        if "bruxell" in localisation and "bruxell" in call["organisme"].lower():
            score += 15

        # Maturité vs eligibilité
        eligibilite_text = " ".join(call["eligibilite"]).lower()
        if "startup" in eligibilite_text:
            score += 10
        if "pme" in eligibilite_text:
            score += 10
        if "3+ ans" in eligibilite_text and anciennete < 36:
            score -= 30
        if "post-poc" in eligibilite_text and anciennete < 24:
            score -= 15
        if "chercheurs" in eligibilite_text and not profile.get("partenariats_academiques"):
            score -= 40

        # Taux de succès pondéré
        score += call["taux_succes_historique"] * 30

        scored.append((score, call))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored]


def export_call_summary(call_id: str) -> str:
    """Résumé formaté prêt à coller dans un email/dossier."""
    call = get_call_details(call_id)
    if not call:
        return f"Appel {call_id} introuvable."

    lines = [
        f"=== {call['nom']} ===",
        f"Organisme    : {call['organisme']}",
        f"Type         : {call['type']}",
        f"Montant      : {call['montant_min']:,} – {call['montant_max']:,} EUR",
        f"Cofinancement: {int(call['taux_cofinancement']*100)}%",
        f"Éligibilité  : {', '.join(call['eligibilite'])}",
        f"Secteurs     : {', '.join(call['secteurs'])}",
        f"Critères     : {', '.join(call['criteres_selection'])}",
        f"Deadline     : {call['deadline_typical']}",
        f"Durée projet : {call['duree_projet_mois']} mois",
        f"Délai réponse: {call['delai_reponse_semaines']} semaines",
        f"Taux succès  : {int(call['taux_succes_historique']*100)}%",
        f"Difficulté   : {call['difficulte']}",
        f"URL          : {call['url']}",
        f"Notes        : {call['notes']}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 60)
    print("PROJECT CALLS EXPERT AGENT — Caelum Partners")
    print("=" * 60)

    CAELUM_PROFILE = {
        "secteurs": ["compliance", "ESG", "IA", "SaaS", "droits humains"],
        "localisation": "Bruxelles",
        "ancienneté_mois": 18,
        "partenariats_academiques": False,
        "partenariats_industriels": False,
    }

    print("\n[1] RECHERCHE : appels IA + compliance")
    results = search_calls(["IA", "compliance", "ESG"])
    print(f"    → {len(results)} appel(s) trouvé(s) : {[r['id'] for r in results]}")

    print("\n[2] TOP 3 APPELS RECOMMANDÉS pour Caelum Partners")
    recommended = get_recommended_calls(CAELUM_PROFILE)[:3]
    for i, call in enumerate(recommended, 1):
        print(f"\n  #{i} {call['nom']}")
        print(f"     Montant max   : {call['montant_max']:,} EUR")
        print(f"     Cofinancement : {int(call['taux_cofinancement']*100)}%")
        print(f"     Difficulté    : {call['difficulte']}")
        print(f"     Taux succès   : {int(call['taux_succes_historique']*100)}%")
        print(f"     Notes         : {call['notes']}")

    print("\n[3] FICHE DÉTAILLÉE : INV-2026-001")
    print(export_call_summary("INV-2026-001"))

    print("\n[OK] Agent project-calls-expert opérationnel.")
