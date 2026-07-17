#!/usr/bin/env python3
"""
Market Positioning Agent — Caelum Partners SPRL
Positionnement stratégique sur le marché ESG/CSDDD 2026
"""

import json
from datetime import datetime
from math import sqrt

# ── SWOT ─────────────────────────────────────────────────────────────────────

SWOT = {
    "forces": [
        {
            "id": "F1",
            "texte": "Architecture IA multi-agents (CaelumSwarm) — 42+ engines spécialisés",
            "poids": 10,
        },
        {
            "id": "F2",
            "texte": "Seule plateforme CSDDD/CS3D native sur le marché EU",
            "poids": 9,
        },
        {
            "id": "F3",
            "texte": "Couverture ultra-granulaire droits humains (50+ domaines)",
            "poids": 9,
        },
        {
            "id": "F4",
            "texte": "Stack Next.js + Python moderne, API temps réel (<200ms)",
            "poids": 7,
        },
        {
            "id": "F5",
            "texte": "Pricing accessible vs concurrents (ETI + grands groupes)",
            "poids": 8,
        },
        {
            "id": "F6",
            "texte": "Fondée en Belgique — hub UE, accès institutionnel facilité",
            "poids": 6,
        },
    ],
    "faiblesses": [
        {
            "id": "W1",
            "texte": "Notoriété marché encore limitée (phase early startup)",
            "poids": 8,
        },
        {
            "id": "W2",
            "texte": "Équipe commerciale à développer",
            "poids": 7,
        },
        {
            "id": "W3",
            "texte": "Base clients initiale restreinte (proof-of-concept à démontrer)",
            "poids": 6,
        },
        {
            "id": "W4",
            "texte": "Dépendance à l'écosystème cloud pour la scalabilité",
            "poids": 4,
        },
        {
            "id": "W5",
            "texte": "Pas encore de certifications ISO 27001 / SOC2",
            "poids": 5,
        },
    ],
    "opportunites": [
        {
            "id": "O1",
            "texte": "CSDDD obligatoire 2026-2027 pour +500 salariés EU → marché captif",
            "poids": 10,
        },
        {
            "id": "O2",
            "texte": "CSRD reporting non-financier obligatoire dès 2024 — demande exploser",
            "poids": 9,
        },
        {
            "id": "O3",
            "texte": "Fonds ESG en croissance exponentielle (+40%/an en EU)",
            "poids": 7,
        },
        {
            "id": "O4",
            "texte": "Règlement EU déforestation, minerais de conflit → nouveaux modules",
            "poids": 7,
        },
        {
            "id": "O5",
            "texte": "Cabinets d'audit Big4 cherchent des outils IA à white-labeler",
            "poids": 8,
        },
        {
            "id": "O6",
            "texte": "Expansion géographique naturelle : BE→FR→LU→NL→DE",
            "poids": 7,
        },
    ],
    "menaces": [
        {
            "id": "T1",
            "texte": "EcoVadis (80k clients) peut lancer module CSDDD en 6 mois",
            "poids": 8,
        },
        {
            "id": "T2",
            "texte": "Consolidation marché (M&A) — rachat de startups concurrentes",
            "poids": 6,
        },
        {
            "id": "T3",
            "texte": "Délai ou assouplissement de la transposition CSDDD dans certains États",
            "poids": 5,
        },
        {
            "id": "T4",
            "texte": "Grands éditeurs ERP (SAP, Oracle) intégrant des modules ESG natifs",
            "poids": 7,
        },
        {
            "id": "T5",
            "texte": "Risque de commoditisation des LLM → avantage IA érodable",
            "poids": 4,
        },
    ],
}

# ── Matrice de positionnement ─────────────────────────────────────────────────
# Axes : (prix_relatif 0=cher→10=pas_cher) × (sophistication_ia 0-10)
#         (couverture_csddd 0-10) × (facilite_utilisation 0-10)

POSITIONING_MATRIX = [
    {
        "acteur": "Caelum Partners",
        "prix_relatif": 8,
        "sophistication_ia": 9.5,
        "couverture_csddd": 9.8,
        "facilite_utilisation": 7.5,
        "est_caelum": True,
    },
    {
        "acteur": "EcoVadis",
        "prix_relatif": 3,
        "sophistication_ia": 4,
        "couverture_csddd": 3,
        "facilite_utilisation": 7,
        "est_caelum": False,
    },
    {
        "acteur": "IntegrityNext",
        "prix_relatif": 6,
        "sophistication_ia": 3.5,
        "couverture_csddd": 6,
        "facilite_utilisation": 6.5,
        "est_caelum": False,
    },
    {
        "acteur": "Sedex",
        "prix_relatif": 8,
        "sophistication_ia": 1.5,
        "couverture_csddd": 2,
        "facilite_utilisation": 5,
        "est_caelum": False,
    },
    {
        "acteur": "Datamaran",
        "prix_relatif": 2,
        "sophistication_ia": 6,
        "couverture_csddd": 4,
        "facilite_utilisation": 4,
        "est_caelum": False,
    },
    {
        "acteur": "Sustainalytics",
        "prix_relatif": 1,
        "sophistication_ia": 5,
        "couverture_csddd": 1,
        "facilite_utilisation": 5.5,
        "est_caelum": False,
    },
    {
        "acteur": "Sourcemap",
        "prix_relatif": 2.5,
        "sophistication_ia": 4.5,
        "couverture_csddd": 2.5,
        "facilite_utilisation": 6,
        "est_caelum": False,
    },
]

# ── Segments de marché cibles ─────────────────────────────────────────────────

TARGET_SEGMENTS = [
    {
        "segment": "Grands groupes belges/français obligés CSDDD (>500 salariés)",
        "taille_marche_eu_entreprises": 50_000,
        "pouvoir_achat_mensuel_eur": 2_500,
        "urgence_achat": "CRITIQUE",
        "argument_principal": "Conformité légale obligatoire CSDDD 2026-2027",
        "cycle_vente_mois": 4,
        "score_priorite": 9.5,
    },
    {
        "segment": "Cabinets d'audit (Big4, Mid-tier, boutiques ESG)",
        "taille_marche_eu_entreprises": 12_000,
        "pouvoir_achat_mensuel_eur": 4_800,
        "urgence_achat": "ÉLEVÉE",
        "argument_principal": "White-label IA + génération de rapports CSDDD automatisée",
        "cycle_vente_mois": 6,
        "score_priorite": 8.7,
    },
    {
        "segment": "Juristes / cabinets avocats compliance & droits humains",
        "taille_marche_eu_entreprises": 8_500,
        "pouvoir_achat_mensuel_eur": 1_800,
        "urgence_achat": "ÉLEVÉE",
        "argument_principal": "Documentation juridique automatisée + veille réglementaire",
        "cycle_vente_mois": 3,
        "score_priorite": 8.2,
    },
    {
        "segment": "Fonds ESG / asset managers",
        "taille_marche_eu_entreprises": 3_200,
        "pouvoir_achat_mensuel_eur": 6_500,
        "urgence_achat": "MODÉRÉE",
        "argument_principal": "Scoring droits humains portefeuille + SFDR alignment",
        "cycle_vente_mois": 8,
        "score_priorite": 7.4,
    },
]

# ── Scénarios go-to-market ────────────────────────────────────────────────────

GTM_SCENARIOS = [
    {
        "id": "A",
        "nom": "Niche droits humains CSDDD",
        "description": (
            "Se positionner comme la plateforme de référence droits humains "
            "et CSDDD en EU. Marketing éducatif ciblé direction juridique "
            "et RSE des grands groupes belges/français."
        ),
        "cible_principale": "Responsables compliance + DRH grands groupes",
        "prix_entry_eur": 599,
        "prix_enterprise_eur": 3_500,
        "investissement_12m_eur": 280_000,
        "mrr_cible_12m_eur": 85_000,
        "criteres": {
            "roi_score": 8.5,
            "delai_score": 8,
            "risque_score": 8,  # Inversé : 10=risque faible
            "differenciation_score": 10,
        },
    },
    {
        "id": "B",
        "nom": "Plateforme ESG généraliste",
        "description": (
            "Élargir la couverture à l'ensemble des dimensions ESG "
            "(E+S+G) pour rivaliser frontalement avec EcoVadis. "
            "Nécessite un investissement produit plus important."
        ),
        "cible_principale": "Directions achats + RSE tous secteurs",
        "prix_entry_eur": 299,
        "prix_enterprise_eur": 5_000,
        "investissement_12m_eur": 620_000,
        "mrr_cible_12m_eur": 140_000,
        "criteres": {
            "roi_score": 7,
            "delai_score": 4,
            "risque_score": 5,
            "differenciation_score": 5,
        },
    },
    {
        "id": "C",
        "nom": "White-label pour cabinets d'audit",
        "description": (
            "Vendre la plateforme en marque blanche aux Big4 et "
            "cabinets mid-tier. Accélère l'adoption via des réseaux "
            "commerciaux établis, sans effort de brand building direct."
        ),
        "cible_principale": "Big4, cabinets compliance, boutiques ESG",
        "prix_entry_eur": 0,
        "prix_enterprise_eur": 18_000,
        "investissement_12m_eur": 160_000,
        "mrr_cible_12m_eur": 65_000,
        "criteres": {
            "roi_score": 8,
            "delai_score": 7,
            "risque_score": 7,
            "differenciation_score": 6,
        },
    },
]


def score_scenario(s: dict) -> float:
    c = s["criteres"]
    return round(
        (c["roi_score"] * 0.35 + c["delai_score"] * 0.20
         + c["risque_score"] * 0.20 + c["differenciation_score"] * 0.25),
        2,
    )


def render_bar(value: float, max_val: float = 10, width: int = 25) -> str:
    filled = round(value / max_val * width)
    return "[" + "█" * filled + "░" * (width - filled) + f"] {value:.1f}/{max_val:.0f}"


def compute_swot_score(swot: dict) -> dict:
    score_f = sum(x["poids"] for x in swot["forces"])
    score_w = sum(x["poids"] for x in swot["faiblesses"])
    score_o = sum(x["poids"] for x in swot["opportunites"])
    score_t = sum(x["poids"] for x in swot["menaces"])
    net = (score_f + score_o) - (score_w + score_t)
    return {
        "forces_total": score_f,
        "faiblesses_total": score_w,
        "opportunites_total": score_o,
        "menaces_total": score_t,
        "bilan_net": net,
        "verdict": "FAVORABLE" if net > 0 else "DÉFAVORABLE",
    }


def run_agent():
    print("=" * 68)
    print("  CAELUM PARTNERS — MARKET POSITIONING AGENT")
    print(f"  Analyse au : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 68)

    # SWOT
    swot_scores = compute_swot_score(SWOT)
    print(f"\n{'─'*68}")
    print("  ANALYSE SWOT — CAELUM PARTNERS SPRL")
    print(f"{'─'*68}")
    for cat, label, items in [
        ("forces", "FORCES", SWOT["forces"]),
        ("faiblesses", "FAIBLESSES", SWOT["faiblesses"]),
        ("opportunites", "OPPORTUNITÉS", SWOT["opportunites"]),
        ("menaces", "MENACES", SWOT["menaces"]),
    ]:
        score = swot_scores[f"{cat}_total"]
        print(f"\n  [{label}] — Score pondéré : {score}")
        for item in items:
            bar = render_bar(item["poids"])
            print(f"    {item['id']} {bar}  {item['texte']}")

    print(f"\n  BILAN NET SWOT : {swot_scores['bilan_net']:+d} → {swot_scores['verdict']}")

    # Matrice de positionnement
    print(f"\n{'─'*68}")
    print("  MATRICE DE POSITIONNEMENT")
    print("  Axe 1 : Prix relatif (0=cher → 10=accessible) × Sophistication IA")
    print("  Axe 2 : Couverture CSDDD × Facilité d'utilisation")
    print(f"{'─'*68}")
    print(f"  {'Acteur':<26} {'Prix':<6} {'IA':<6} {'CSDDD':<8} {'UX':<6}")
    print(f"  {'─'*24} {'─'*5} {'─'*5} {'─'*7} {'─'*5}")
    for p in POSITIONING_MATRIX:
        marker = " ◄ CAELUM" if p["est_caelum"] else ""
        print(
            f"  {p['acteur']:<26} "
            f"{p['prix_relatif']:<6.1f} "
            f"{p['sophistication_ia']:<6.1f} "
            f"{p['couverture_csddd']:<8.1f} "
            f"{p['facilite_utilisation']:<6.1f}"
            f"{marker}"
        )

    # Segments cibles
    print(f"\n{'─'*68}")
    print("  SEGMENTS DE MARCHÉ CIBLES")
    print(f"{'─'*68}")
    for seg in TARGET_SEGMENTS:
        print(f"\n  ► {seg['segment']}")
        print(f"    Marché EU          : ~{seg['taille_marche_eu_entreprises']:,} entreprises")
        print(f"    Budget moyen/mois  : {seg['pouvoir_achat_mensuel_eur']:,} EUR")
        print(f"    Urgence            : {seg['urgence_achat']}")
        print(f"    Cycle de vente     : {seg['cycle_vente_mois']} mois")
        print(f"    Priorité           : {render_bar(seg['score_priorite'])}")
        print(f"    Argument clé       : {seg['argument_principal']}")

    # Scénarios GTM
    print(f"\n{'─'*68}")
    print("  SCÉNARIOS GO-TO-MARKET — SCORING")
    print(f"{'─'*68}")

    scores_gtm = []
    for s in GTM_SCENARIOS:
        sc = score_scenario(s)
        scores_gtm.append((sc, s))

    scores_gtm.sort(reverse=True)
    winner = scores_gtm[0][1]

    for sc, s in scores_gtm:
        tag = " ← RECOMMANDÉ" if s["id"] == winner["id"] else ""
        print(f"\n  Scénario {s['id']} : {s['nom']}{tag}")
        print(f"    Score global       : {render_bar(sc, 10)}")
        print(f"    ROI                : {render_bar(s['criteres']['roi_score'])}")
        print(f"    Délai              : {render_bar(s['criteres']['delai_score'])}")
        print(f"    Risque (inv.)      : {render_bar(s['criteres']['risque_score'])}")
        print(f"    Différenciation    : {render_bar(s['criteres']['differenciation_score'])}")
        print(f"    Investissement 12m : {s['investissement_12m_eur']:,} EUR")
        print(f"    MRR cible 12m      : {s['mrr_cible_12m_eur']:,} EUR")
        print(f"    Prix entry         : {s['prix_entry_eur']:,} EUR/mois")
        print(f"    Description        : {s['description'][:70]}...")

    print(f"\n{'─'*68}")
    print(f"  RECOMMANDATION FINALE")
    print(f"{'─'*68}")
    print(f"  Scénario gagnant : {winner['id']} — {winner['nom']}")
    print(f"  Justification    : Meilleur équilibre ROI + différenciation maximale")
    print(f"                     sur l'axe droits humains CSDDD-native.")
    print(f"                     Investissement maîtrisé + premiers revenus rapides.")
    print(f"{'─'*68}\n")

    output = {
        "agent": "market-positioning-agent",
        "generated_at": datetime.now().isoformat(),
        "swot": SWOT,
        "swot_scores": swot_scores,
        "matrice_positionnement": POSITIONING_MATRIX,
        "segments_cibles": TARGET_SEGMENTS,
        "scenarios_gtm": [
            {**s, "score_global": score_scenario(s)} for s in GTM_SCENARIOS
        ],
        "recommandation": {
            "scenario_gagnant": winner["id"],
            "nom": winner["nom"],
            "score": score_scenario(winner),
            "investissement_eur": winner["investissement_12m_eur"],
            "mrr_cible_12m_eur": winner["mrr_cible_12m_eur"],
        },
    }

    output_path = "/home/user/TEST/scripts/market-positioning-agent-output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  JSON sauvegardé → {output_path}")
    print()
    return output


if __name__ == "__main__":
    run_agent()
