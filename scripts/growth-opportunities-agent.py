#!/usr/bin/env python3
"""
Growth Opportunities Agent — Caelum Partners SPRL
Identification des leviers de croissance pour dominer le marché ESG/CSDDD 2026
"""

import json
from datetime import datetime, timedelta
from math import ceil

# ── Données des leviers de croissance ────────────────────────────────────────

GROWTH_LEVERS = {
    "partenariats": [
        {
            "nom": "Alliance Big4 (Deloitte/EY/KPMG/PwC) — white-label",
            "description": (
                "Intégrer CaelumSwarm dans les offres CSDDD des Big4 en marque blanche. "
                "Chaque cabinet dispose d'une base de 500+ clients grands groupes."
            ),
            "type": "partenariat",
            "impact": 9,
            "effort": 8,
            "delai_mois": 9,
            "cout_eur_estime": 45_000,
            "kpi_succes": "2 accords signés en 12 mois",
        },
        {
            "nom": "Réseau cabinets avocats compliance EU",
            "description": (
                "Partenariats avec 20+ cabinets avocats spécialisés droits humains/compliance. "
                "Référencement outil recommandé dans leurs missions CSDDD."
            ),
            "type": "partenariat",
            "impact": 7,
            "effort": 4,
            "delai_mois": 4,
            "cout_eur_estime": 12_000,
            "kpi_succes": "15 cabinets partenaires actifs",
        },
        {
            "nom": "Consultants ESG indépendants (réseau 500+)",
            "description": (
                "Programme de partenaires certifiés CaelumSwarm pour consultants ESG. "
                "Commission 20% sur les contrats apportés."
            ),
            "type": "partenariat",
            "impact": 6,
            "effort": 3,
            "delai_mois": 3,
            "cout_eur_estime": 8_000,
            "kpi_succes": "50 consultants certifiés actifs",
        },
        {
            "nom": "Intégration ERP SAP (module plug-in)",
            "description": (
                "Développer un connecteur SAP S/4HANA pour importer "
                "automatiquement les données fournisseurs dans CaelumSwarm. "
                "SAP marketplace = accès à 450k clients."
            ),
            "type": "partenariat_tech",
            "impact": 8,
            "effort": 9,
            "delai_mois": 12,
            "cout_eur_estime": 85_000,
            "kpi_succes": "Plugin certifié SAP Store",
        },
    ],
    "canaux_acquisition": [
        {
            "nom": "LinkedIn B2B — campagnes ciblées DG Compliance / RSE",
            "description": (
                "Campagnes LinkedIn Ads ciblant responsables compliance, DRH, RSE "
                "dans les entreprises EU +500 salariés. "
                "Content marketing : études de cas CSDDD + calculateurs de risques."
            ),
            "type": "acquisition_digitale",
            "impact": 7,
            "effort": 4,
            "delai_mois": 2,
            "cout_eur_estime": 24_000,
            "kpi_succes": "500 leads qualifiés/trimestre",
        },
        {
            "nom": "Conférences ESG (Sustainable Finance Summit, Bruxelles ESG Week)",
            "description": (
                "Présence active dans les 5 grandes conférences ESG EU/an. "
                "Speaking slots + stands. Networking direct avec décideurs."
            ),
            "type": "acquisition_evenementielle",
            "impact": 7,
            "effort": 5,
            "delai_mois": 4,
            "cout_eur_estime": 35_000,
            "kpi_succes": "200 contacts qualifiés/événement",
        },
        {
            "nom": "Appels à projets EU (Horizon Europe, Just Transition Fund)",
            "description": (
                "Candidater aux financements EU pour outils de compliance droits humains. "
                "Potentiel grant : 500k-2M EUR + visibilité institutionnelle."
            ),
            "type": "financement_public",
            "impact": 8,
            "effort": 6,
            "delai_mois": 10,
            "cout_eur_estime": 18_000,
            "kpi_succes": "1 grant EU obtenu en 18 mois",
        },
        {
            "nom": "SEO/Content : hub d'expertise CSDDD francophone",
            "description": (
                "Créer le référentiel SEO #1 sur CSDDD/CS3D en français et néerlandais. "
                "Guides, checklist, calculateurs de conformité gratuits = lead magnets."
            ),
            "type": "acquisition_organique",
            "impact": 7,
            "effort": 4,
            "delai_mois": 5,
            "cout_eur_estime": 15_000,
            "kpi_succes": "10k visites organiques/mois en 6 mois",
        },
        {
            "nom": "Programme pilote gratuit 90 jours (grands groupes)",
            "description": (
                "Offrir accès complet 90 jours à 10 grands groupes belges ciblés. "
                "Objectif : 7/10 convertis → social proof + références sectorielles."
            ),
            "type": "acquisition_trial",
            "impact": 9,
            "effort": 5,
            "delai_mois": 3,
            "cout_eur_estime": 0,
            "kpi_succes": "7 grands comptes convertis en payant",
        },
    ],
    "fonctionnalites_differenciantes": [
        {
            "nom": "Certification ISO 26000 / SA8000 intégrée",
            "description": (
                "Module de préparation et suivi certification ISO 26000 (RS) et SA8000 "
                "(droits travailleurs). Gap analysis automatisée + plan d'action IA."
            ),
            "type": "produit",
            "impact": 8,
            "effort": 7,
            "delai_mois": 8,
            "cout_eur_estime": 55_000,
            "kpi_succes": "Module utilisé par 30% des clients Enterprise",
        },
        {
            "nom": "Rapport CSRD auto-généré (Word/PDF)",
            "description": (
                "Génération automatique du rapport de durabilité CSRD (ESRS S1-S4) "
                "à partir des données CaelumSwarm. Time-to-report : 2h vs 3 semaines."
            ),
            "type": "produit",
            "impact": 10,
            "effort": 7,
            "delai_mois": 6,
            "cout_eur_estime": 68_000,
            "kpi_succes": "100+ rapports CSRD générés en 12 mois",
        },
        {
            "nom": "API publique + webhooks pour intégration client",
            "description": (
                "REST API documentée (OpenAPI 3.1) permettant aux clients d'intégrer "
                "CaelumSwarm dans leurs SI internes. SDK Python + JS."
            ),
            "type": "produit_tech",
            "impact": 8,
            "effort": 5,
            "delai_mois": 4,
            "cout_eur_estime": 32_000,
            "kpi_succes": "50+ intégrations actives clients",
        },
        {
            "nom": "Score de risque fournisseur en temps réel (watchlist)",
            "description": (
                "Monitoring continu des fournisseurs : alerte automatique si "
                "un événement adverse est détecté (scandale, grève, condamnation). "
                "Feeds : actualités, ONG, bases sanctions."
            ),
            "type": "produit",
            "impact": 9,
            "effort": 6,
            "delai_mois": 5,
            "cout_eur_estime": 42_000,
            "kpi_succes": "Taux d'alerte actionné > 80% par les clients",
        },
    ],
    "expansion_geographique": [
        {
            "nom": "Belgique — marché domestique (phase actuelle)",
            "description": "Consolider la présence en Belgique. Cibler les 500 plus grands groupes belges.",
            "type": "geo",
            "impact": 9,
            "effort": 3,
            "delai_mois": 0,
            "cout_eur_estime": 0,
            "kpi_succes": "50 clients belges actifs",
        },
        {
            "nom": "France — expansion prioritaire (CAC40 + ETI)",
            "description": (
                "La France a la Loi de Vigilance depuis 2017 + CSDDD = culture compliance forte. "
                "Marché 5x Belgique. Bureau Paris + 2 commerciaux France."
            ),
            "type": "geo",
            "impact": 9,
            "effort": 6,
            "delai_mois": 6,
            "cout_eur_estime": 120_000,
            "kpi_succes": "80 clients France en 18 mois",
        },
        {
            "nom": "Luxembourg — fonds ESG & finance responsable",
            "description": (
                "Luxembourg = hub européen des fonds ESG (3500+ fonds SFDR). "
                "Faible distance culturelle/géographique depuis Belgique."
            ),
            "type": "geo",
            "impact": 7,
            "effort": 4,
            "delai_mois": 4,
            "cout_eur_estime": 35_000,
            "kpi_succes": "20 fonds ESG clients actifs",
        },
        {
            "nom": "Pays-Bas — marché DURABLE et compliance avancée",
            "description": (
                "NL a des multinationales compliance-matures (Shell, Unilever, Philips). "
                "Version EN + NL de la plateforme nécessaire."
            ),
            "type": "geo",
            "impact": 7,
            "effort": 7,
            "delai_mois": 10,
            "cout_eur_estime": 85_000,
            "kpi_succes": "40 clients NL en 24 mois",
        },
    ],
    "pricing_strategy": [
        {
            "nom": "Freemium — accès limité 3 engines (acquisition virale)",
            "description": (
                "Plan gratuit avec 3 engines, 5 fournisseurs, export PDF watermarked. "
                "Objectif : 10k utilisateurs gratuits → 5% conversion payant."
            ),
            "type": "pricing",
            "impact": 7,
            "effort": 3,
            "delai_mois": 2,
            "cout_eur_estime": 8_000,
            "kpi_succes": "10k comptes free, 500 conversions/an",
        },
        {
            "nom": "Plan PME 199 EUR/mois — up à 20 fournisseurs",
            "description": (
                "Tier PME accessible pour le marché belge/français. "
                "Inclut 10 engines, 20 fournisseurs, rapport CSDDD basique."
            ),
            "type": "pricing",
            "impact": 6,
            "effort": 2,
            "delai_mois": 1,
            "cout_eur_estime": 3_000,
            "kpi_succes": "200 clients PME en 12 mois",
        },
        {
            "nom": "Plan Enterprise 2500 EUR/mois — illimité + SLA",
            "description": (
                "Tier Enterprise : engines illimités, fournisseurs illimités, "
                "API dédiée, SLA 99.9%, account manager dédié, onboarding custom."
            ),
            "type": "pricing",
            "impact": 9,
            "effort": 4,
            "delai_mois": 3,
            "cout_eur_estime": 25_000,
            "kpi_succes": "30 clients Enterprise en 12 mois → 75k MRR",
        },
    ],
}


def compute_score(lever: dict) -> float:
    """Score = impact × 2 / effort (≥1 pour éviter division par zéro)"""
    effort = max(lever["effort"], 1)
    return round((lever["impact"] * 2) / effort, 2)


def all_levers_flat(data: dict) -> list:
    flat = []
    for category, levers in data.items():
        for lever in levers:
            lever_copy = dict(lever)
            lever_copy["categorie"] = category
            lever_copy["score_global"] = compute_score(lever)
            flat.append(lever_copy)
    return flat


def build_roadmap_12m(top_levers: list) -> list:
    """Construit une roadmap en positionnant les leviers dans le temps."""
    roadmap = []
    base_date = datetime(2026, 7, 1)
    for lev in top_levers:
        start = base_date
        end = start + timedelta(days=lev["delai_mois"] * 30)
        roadmap.append({
            "levier": lev["nom"],
            "categorie": lev["categorie"],
            "score": lev["score_global"],
            "debut": start.strftime("%Y-%m"),
            "fin": end.strftime("%Y-%m"),
            "cout_eur": lev["cout_eur_estime"],
            "kpi": lev["kpi_succes"],
        })
    return roadmap


def render_bar(value: float, max_val: float = 10, width: int = 25) -> str:
    filled = round(value / max_val * width)
    return "[" + "█" * filled + "░" * (width - filled) + f"] {value:.2f}"


def run_agent():
    print("=" * 68)
    print("  CAELUM PARTNERS — GROWTH OPPORTUNITIES AGENT")
    print(f"  Analyse au : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 68)

    all_levers = all_levers_flat(GROWTH_LEVERS)
    all_levers.sort(key=lambda x: x["score_global"], reverse=True)
    top5 = all_levers[:5]
    total_cost = sum(l["cout_eur_estime"] for l in all_levers)
    top5_cost = sum(l["cout_eur_estime"] for l in top5)

    # ── Vue globale ──────────────────────────────────────────────────────────
    print(f"\n{'─'*68}")
    print(f"  VUE GLOBALE — {len(all_levers)} leviers analysés")
    print(f"{'─'*68}")
    print(f"  Budget total estimé (tous leviers) : {total_cost:,.0f} EUR")
    print(f"  Budget Top 5 recommandés            : {top5_cost:,.0f} EUR")
    print()

    # ── Leviers par catégorie ─────────────────────────────────────────────────
    for cat, levers in GROWTH_LEVERS.items():
        cat_label = cat.replace("_", " ").upper()
        print(f"\n{'─'*68}")
        print(f"  {cat_label}")
        print(f"{'─'*68}")
        levers_scored = sorted(levers, key=lambda x: compute_score(x), reverse=True)
        for lev in levers_scored:
            sc = compute_score(lev)
            print(f"\n  ► {lev['nom']}")
            print(f"    Score              : {render_bar(sc, 18)}")
            print(f"    Impact (1-10)      : {lev['impact']}")
            print(f"    Effort (1-10)      : {lev['effort']}")
            print(f"    Délai              : {lev['delai_mois']} mois")
            print(f"    Coût estimé        : {lev['cout_eur_estime']:,} EUR")
            print(f"    KPI succès         : {lev['kpi_succes']}")

    # ── TOP 5 recommandations ─────────────────────────────────────────────────
    print(f"\n{'─'*68}")
    print("  TOP 5 RECOMMANDATIONS (score = impact×2 / effort)")
    print(f"{'─'*68}")
    for rank, lev in enumerate(top5, 1):
        print(f"\n  #{rank} — {lev['nom']}")
        print(f"    Score              : {render_bar(lev['score_global'], 18)}")
        print(f"    Catégorie          : {lev['categorie'].replace('_', ' ')}")
        print(f"    Impact / Effort    : {lev['impact']}/10  /  {lev['effort']}/10")
        print(f"    Délai              : {lev['delai_mois']} mois")
        print(f"    Coût               : {lev['cout_eur_estime']:,} EUR")
        print(f"    KPI                : {lev['kpi_succes']}")

    # ── Roadmap 12 mois ───────────────────────────────────────────────────────
    roadmap = build_roadmap_12m(top5)
    print(f"\n{'─'*68}")
    print("  ROADMAP 12 MOIS (Top 5 leviers)")
    print(f"{'─'*68}")
    print(f"  {'Levier':<42} {'Début':<9} {'Fin':<9} {'Coût EUR':<10}")
    print(f"  {'─'*40} {'─'*7} {'─'*7} {'─'*8}")
    for r in roadmap:
        short = r["levier"][:40]
        print(
            f"  {short:<42} {r['debut']:<9} {r['fin']:<9} "
            f"{r['cout_eur']:>8,}"
        )
    print(f"\n  Budget roadmap Top 5 total : {top5_cost:,.0f} EUR")
    print(f"{'─'*68}\n")

    output = {
        "agent": "growth-opportunities-agent",
        "generated_at": datetime.now().isoformat(),
        "total_leviers": len(all_levers),
        "budget_total_estime_eur": total_cost,
        "leviers_par_categorie": GROWTH_LEVERS,
        "top5_recommandations": top5,
        "roadmap_12_mois": roadmap,
        "methode_scoring": "score = (impact × 2) / effort",
    }

    output_path = "/home/user/TEST/scripts/growth-opportunities-agent-output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  JSON sauvegardé → {output_path}")
    print()
    return output


if __name__ == "__main__":
    run_agent()
