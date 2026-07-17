#!/usr/bin/env python3
"""
Value Chain Cartography Agent — Caelum Partners CaelumSwarm™
Cartographie automatique de la chaîne de valeur selon CSDDD Art.3(g).
Identifie les maillons à risque droits humains — amont, opérations, aval.
"""

import sys
from datetime import datetime, timezone

VALUE_CHAIN_TIERS = {
    "UPSTREAM_TIER3": {
        "label": "Amont T3 — Extraction matières premières",
        "csddd_scope": "Relations d'affaires établies",
        "risk_multiplier": 1.4,
        "key_risks": ["travail forcé", "travail enfants", "droits fonciers", "droits peuples autochtones"],
        "ilo_conventions": ["C138", "C182", "C169"],
    },
    "UPSTREAM_TIER2": {
        "label": "Amont T2 — Transformation & composants",
        "csddd_scope": "Relations d'affaires établies",
        "risk_multiplier": 1.2,
        "key_risks": ["conditions travail", "salaire décent", "liberté syndicale"],
        "ilo_conventions": ["C87", "C98", "C131"],
    },
    "UPSTREAM_TIER1": {
        "label": "Amont T1 — Fournisseurs directs",
        "csddd_scope": "Inclus CSDDD — contrôle direct requis",
        "risk_multiplier": 1.0,
        "key_risks": ["audit social", "code de conduite", "clause contractuelle"],
        "ilo_conventions": ["C29", "C105", "C100", "C111"],
    },
    "OWN_OPERATIONS": {
        "label": "Opérations propres",
        "csddd_scope": "Inclus CSDDD — contrôle total",
        "risk_multiplier": 0.8,
        "key_risks": ["discrimination", "harcèlement", "santé sécurité", "syndicats"],
        "ilo_conventions": ["C87", "C98", "C100", "C111", "C155"],
    },
    "DOWNSTREAM_TIER1": {
        "label": "Aval T1 — Distribution & clients directs",
        "csddd_scope": "Inclus CSDDD Art.3(g)(ii)",
        "risk_multiplier": 0.9,
        "key_risks": ["usage produit", "protection consommateurs", "marketing éthique"],
        "ilo_conventions": [],
    },
    "DOWNSTREAM_TIER2": {
        "label": "Aval T2 — Utilisateurs finaux",
        "csddd_scope": "Hors CSDDD (sauf impact direct)",
        "risk_multiplier": 0.7,
        "key_risks": ["accès équitable", "prix abordables", "données personnelles"],
        "ilo_conventions": [],
    },
}

SECTOR_VALUE_CHAINS = {
    "tech_software": {
        "upstream": {
            "T3": ["Cobalt RDC — batteries", "Lithium Chili — composants"],
            "T2": ["Usines semi-conducteurs Taïwan", "Assemblage Foxconn Chine"],
            "T1": ["Développeurs offshore", "Sous-traitants IT Inde/Pologne"],
        },
        "own_ops": ["Équipes R&D", "Infrastructure cloud", "Support client"],
        "downstream": {
            "T1": ["Distributeurs SaaS", "Intégrateurs système"],
            "T2": ["PME clients", "Citoyens utilisateurs finaux"],
        },
        "high_risk_nodes": ["Cobalt RDC", "Foxconn Chine"],
    },
    "finance": {
        "upstream": {
            "T3": ["Entreprises portefeuille secteur extractif"],
            "T2": ["Correspondants bancaires juridictions offshore"],
            "T1": ["Fournisseurs data — prestataires KYC"],
        },
        "own_ops": ["Trading", "Gestion actifs", "Compliance"],
        "downstream": {
            "T1": ["Clients entreprises", "Clients retail"],
            "T2": ["Communautés impactées investissements"],
        },
        "high_risk_nodes": ["Correspondants offshore", "Entreprises portefeuille secteur extractif"],
    },
    "legal_tech_compliance": {
        "upstream": {
            "T3": ["Sources données publiques (ONU, OCDE, Banque Mondiale)"],
            "T2": ["Fournisseurs API data", "Cloud providers (AWS, Azure)"],
            "T1": ["Développeurs freelance", "Sous-traitants analyse data"],
        },
        "own_ops": ["Équipe CaelumSwarm™", "Infrastructure SaaS", "Recherche droits humains"],
        "downstream": {
            "T1": ["Clients corporates CSDDD", "Cabinets conseil RSE"],
            "T2": ["ONG & régulateurs utilisateurs rapports"],
        },
        "high_risk_nodes": ["Fournisseurs API data — biais potentiels", "Cloud providers — concentration risque"],
    },
}

RISK_ASSESSMENT_CRITERIA = {
    "country_risk": {
        "HIGH": ["Myanmar", "RDC", "Bangladesh", "Éthiopie", "Érythrée"],
        "MEDIUM": ["Chine", "Inde", "Brésil", "Colombie", "Philippines"],
        "LOW": ["UE", "USA", "Canada", "Australie", "Norvège"],
    },
    "sector_risk": {
        "HIGH": ["Extraction minière", "Textile/confection", "Agriculture intensif", "Construction"],
        "MEDIUM": ["Electronique", "Chimie", "Agroalimentaire", "Transport"],
        "LOW": ["Services", "Finance (hors extraction)", "Technologie", "Santé UE"],
    },
}


def assess_node_risk(node_name: str, tier: str, country: str = "") -> dict:
    """Évalue le risque d'un maillon de la chaîne de valeur."""
    tier_config = VALUE_CHAIN_TIERS.get(tier, {})
    multiplier = tier_config.get("risk_multiplier", 1.0)

    country_risk_level = "LOW"
    for level, countries in RISK_ASSESSMENT_CRITERIA["country_risk"].items():
        if any(c.lower() in country.lower() for c in countries):
            country_risk_level = level
            break

    base_risk_score = {"HIGH": 75, "MEDIUM": 50, "LOW": 20}.get(country_risk_level, 30)
    tier_adjusted_score = min(base_risk_score * multiplier, 100)

    risk_level = "critique" if tier_adjusted_score >= 60 else "élevé" if tier_adjusted_score >= 40 else "modéré" if tier_adjusted_score >= 20 else "faible"

    return {
        "node": node_name,
        "tier": tier,
        "tier_label": tier_config.get("label", tier),
        "country": country,
        "country_risk": country_risk_level,
        "base_score": base_risk_score,
        "adjusted_score": round(tier_adjusted_score, 1),
        "risk_level": risk_level,
        "csddd_scope": tier_config.get("csddd_scope", ""),
        "key_risks": tier_config.get("key_risks", []),
        "ilo_conventions": tier_config.get("ilo_conventions", []),
        "action_required": (
            "Audit immédiat + plan correction" if risk_level == "critique"
            else "Évaluation approfondie" if risk_level == "élevé"
            else "Surveillance renforcée" if risk_level == "modéré"
            else "Suivi standard"
        ),
    }


def cartography_value_chain(sector: str, company_name: str, domain_risk: str = None) -> dict:
    """Cartographie complète de la chaîne de valeur."""
    chain_template = SECTOR_VALUE_CHAINS.get(sector, SECTOR_VALUE_CHAINS["legal_tech_compliance"])

    all_nodes = []
    for tier_key, nodes in [
        ("UPSTREAM_TIER3", chain_template["upstream"].get("T3", [])),
        ("UPSTREAM_TIER2", chain_template["upstream"].get("T2", [])),
        ("UPSTREAM_TIER1", chain_template["upstream"].get("T1", [])),
    ]:
        for node in nodes:
            country_hint = ""
            for c in ["RDC", "Chine", "Inde", "Taïwan", "Bangladesh", "Myanmar"]:
                if c in node:
                    country_hint = c
            all_nodes.append(assess_node_risk(node, tier_key, country_hint))

    for node in chain_template.get("own_ops", []):
        all_nodes.append(assess_node_risk(node, "OWN_OPERATIONS", "Belgique"))

    for tier_key, nodes in [
        ("DOWNSTREAM_TIER1", chain_template["downstream"].get("T1", [])),
        ("DOWNSTREAM_TIER2", chain_template["downstream"].get("T2", [])),
    ]:
        for node in nodes:
            all_nodes.append(assess_node_risk(node, tier_key, ""))

    critical_nodes = [n for n in all_nodes if n["risk_level"] == "critique"]
    high_risk_nodes = [n for n in all_nodes if n["risk_level"] == "élevé"]
    high_risk_flagged = chain_template.get("high_risk_nodes", [])

    return {
        "cartography_id": f"VCC-{company_name[:6].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Value Chain Cartography Agent v1.0",
        "company": company_name,
        "sector": sector,
        "domain_risk_filter": domain_risk,
        "summary": {
            "total_nodes": len(all_nodes),
            "critical_nodes": len(critical_nodes),
            "elevated_nodes": len(high_risk_nodes),
            "high_risk_flagged": high_risk_flagged,
            "csddd_coverage": "Tiers 1-3 amont + opérations propres + T1 aval",
        },
        "value_chain_map": all_nodes,
        "priority_actions": [
            {
                "node": n["node"],
                "tier": n["tier_label"],
                "action": n["action_required"],
                "csddd_article": "Art.10" if n["risk_level"] == "critique" else "Art.9",
                "deadline_days": 30 if n["risk_level"] == "critique" else 90,
            }
            for n in (critical_nodes + high_risk_nodes)[:5]
        ],
        "tier_coverage": {tier: tier_config["csddd_scope"] for tier, tier_config in VALUE_CHAIN_TIERS.items()},
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — VALUE CHAIN CARTOGRAPHY AGENT")
    print("  Cartographie Chaîne de Valeur CSDDD Art.3(g)")
    print("=" * 70)

    carto = cartography_value_chain("legal_tech_compliance", "CaelumPartners")

    print(f"\n🗺️  CARTOGRAPHIE: {carto['cartography_id']}")
    print(f"   Entreprise: {carto['company']} | Secteur: {carto['sector']}")
    print(f"   Nœuds cartographiés: {carto['summary']['total_nodes']}")
    print(f"   Nœuds critiques: {carto['summary']['critical_nodes']}")
    print(f"   Nœuds à risque élevé: {carto['summary']['elevated_nodes']}")
    print(f"   Couverture CSDDD: {carto['summary']['csddd_coverage']}")

    print(f"\n⚡ ACTIONS PRIORITAIRES:")
    for action in carto["priority_actions"]:
        print(f"\n   [{action['csddd_article']}] {action['node'][:50]}")
        print(f"   Tier: {action['tier']}")
        print(f"   Action: {action['action']} | Délai: {action['deadline_days']}j")

    print(f"\n📊 CHAÎNE DE VALEUR (nœuds à risque):")
    for node in [n for n in carto["value_chain_map"] if n["risk_level"] in ("critique", "élevé")]:
        icon = "🔴" if node["risk_level"] == "critique" else "🟠"
        print(f"   {icon} [{node['tier'][:15]}] {node['node'][:45]}")
        print(f"      Score: {node['adjusted_score']} | Risques: {', '.join(node['key_risks'][:2])}")

    print(f"\n📋 COUVERTURE PAR TIER:")
    for tier, scope in list(carto["tier_coverage"].items())[:4]:
        print(f"   {tier[:18]}: {scope}")

    print(f"\n✅ Value Chain Cartography Agent — Cartographie générée avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
