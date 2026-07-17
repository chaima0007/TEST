#!/usr/bin/env python3
"""
Value-Based Matching Agent — Caelum Partners CaelumSwarm™
Mise en relation par valeurs : connecte entreprises, ONG, investisseurs,
experts et décideurs selon alignement valeurs droits humains.
"""

import sys
from datetime import datetime, timezone

HUMAN_RIGHTS_VALUES = {
    "DIGNITY": {"label": "Dignité humaine", "un_ref": "DUDH Art.1", "weight": 0.20},
    "EQUALITY": {"label": "Égalité & Non-discrimination", "un_ref": "DUDH Art.2", "weight": 0.15},
    "JUSTICE": {"label": "Justice & État de droit", "un_ref": "DUDH Art.7-11", "weight": 0.15},
    "ACCOUNTABILITY": {"label": "Responsabilité & Transparence", "un_ref": "UNGP 15", "weight": 0.15},
    "REMEDY": {"label": "Accès aux voies de recours", "un_ref": "UNGP 29-31", "weight": 0.10},
    "PARTICIPATION": {"label": "Participation & Inclusion", "un_ref": "ICCPR Art.25", "weight": 0.10},
    "SUSTAINABILITY": {"label": "Durabilité & Long terme", "un_ref": "CSDDD/CSRD", "weight": 0.10},
    "INNOVATION": {"label": "Innovation responsable", "un_ref": "AI Act / EU", "weight": 0.05},
}

ACTOR_TYPES = {
    "CORPORATION": {
        "label": "Entreprise",
        "typical_values": ["ACCOUNTABILITY", "SUSTAINABILITY", "INNOVATION"],
        "typical_needs": ["conformité CSDDD", "notation ESG", "reporting CSRD"],
    },
    "NGO_ADVOCACY": {
        "label": "ONG militante",
        "typical_values": ["DIGNITY", "JUSTICE", "REMEDY"],
        "typical_needs": ["financement", "données terrain", "partenariats"],
    },
    "INVESTOR_ESG": {
        "label": "Investisseur ESG",
        "typical_values": ["ACCOUNTABILITY", "SUSTAINABILITY", "EQUALITY"],
        "typical_needs": ["due diligence", "scoring ESG", "impact reporting"],
    },
    "REGULATOR": {
        "label": "Régulateur/Autorité",
        "typical_values": ["JUSTICE", "ACCOUNTABILITY", "EQUALITY"],
        "typical_needs": ["données conformité", "rapports sectoriels"],
    },
    "EXPERT_CONSULTANT": {
        "label": "Expert/Consultant",
        "typical_values": ["ACCOUNTABILITY", "INNOVATION", "JUSTICE"],
        "typical_needs": ["mandats", "données", "réseau clients"],
    },
    "COMMUNITY_LEADER": {
        "label": "Leader communautaire",
        "typical_values": ["DIGNITY", "PARTICIPATION", "REMEDY"],
        "typical_needs": ["voix", "accès droits", "réparation"],
    },
    "ACADEMIA": {
        "label": "Chercheur/Université",
        "typical_values": ["JUSTICE", "EQUALITY", "INNOVATION"],
        "typical_needs": ["données", "terrain", "publications"],
    },
}

MATCHING_DOMAINS = {
    "statelessness": ["NGO_ADVOCACY", "REGULATOR", "COMMUNITY_LEADER", "ACADEMIA"],
    "tax_haven": ["REGULATOR", "INVESTOR_ESG", "NGO_ADVOCACY", "CORPORATION"],
    "deepfake": ["REGULATOR", "EXPERT_CONSULTANT", "NGO_ADVOCACY", "CORPORATION"],
    "labor_rights": ["CORPORATION", "NGO_ADVOCACY", "INVESTOR_ESG", "COMMUNITY_LEADER"],
    "climate_hr": ["CORPORATION", "INVESTOR_ESG", "ACADEMIA", "REGULATOR"],
}

COLLABORATION_FORMATS = {
    "STRATEGIC_PARTNERSHIP": {
        "label": "Partenariat stratégique",
        "duration": "3-5 ans",
        "formalization": "Convention signée + gouvernance commune",
        "value_alignment_min": 0.75,
    },
    "PROJECT_COLLABORATION": {
        "label": "Collaboration projet",
        "duration": "6-18 mois",
        "formalization": "Accord projet + KPIs partagés",
        "value_alignment_min": 0.60,
    },
    "KNOWLEDGE_EXCHANGE": {
        "label": "Échange de connaissances",
        "duration": "Ponctuel",
        "formalization": "MOU + NDA si données sensibles",
        "value_alignment_min": 0.50,
    },
    "ADVOCACY_COALITION": {
        "label": "Coalition de plaidoyer",
        "duration": "Durée cause",
        "formalization": "Charte coalition + porte-parole",
        "value_alignment_min": 0.70,
    },
}


def compute_value_alignment(actor1_values: list, actor2_values: list) -> dict:
    """Calcule l'alignement de valeurs entre deux acteurs."""
    shared = set(actor1_values) & set(actor2_values)
    total_values = set(actor1_values) | set(actor2_values)

    jaccard = len(shared) / len(total_values) if total_values else 0

    shared_weight = sum(
        HUMAN_RIGHTS_VALUES[v]["weight"]
        for v in shared
        if v in HUMAN_RIGHTS_VALUES
    )

    return {
        "shared_values": list(shared),
        "shared_values_labels": [HUMAN_RIGHTS_VALUES[v]["label"] for v in shared if v in HUMAN_RIGHTS_VALUES],
        "alignment_score": round(jaccard, 3),
        "weighted_alignment": round(shared_weight, 3),
        "compatibility": (
            "EXCELLENTE" if jaccard >= 0.70
            else "BONNE" if jaccard >= 0.50
            else "PARTIELLE" if jaccard >= 0.30
            else "FAIBLE"
        ),
    }


def recommend_collaboration_format(alignment_score: float) -> dict:
    """Recommande le format de collaboration selon l'alignement."""
    for format_key, format_config in COLLABORATION_FORMATS.items():
        if alignment_score >= format_config["value_alignment_min"]:
            return {"format": format_key, **format_config}
    return {"format": "KNOWLEDGE_EXCHANGE", **COLLABORATION_FORMATS["KNOWLEDGE_EXCHANGE"]}


def match_actors(domain: str, seeking_actor_type: str, seeking_values: list) -> dict:
    """Trouve les meilleurs partenaires pour un acteur donné."""
    compatible_types = MATCHING_DOMAINS.get(domain, list(ACTOR_TYPES.keys()))

    matches = []
    for actor_type_key in compatible_types:
        if actor_type_key == seeking_actor_type:
            continue

        actor_type = ACTOR_TYPES.get(actor_type_key, {})
        typical_values = actor_type.get("typical_values", [])

        alignment = compute_value_alignment(seeking_values, typical_values)
        collab_format = recommend_collaboration_format(alignment["alignment_score"])

        matches.append({
            "actor_type": actor_type_key,
            "actor_label": actor_type.get("label", actor_type_key),
            "typical_needs": actor_type.get("typical_needs", []),
            "value_alignment": alignment,
            "recommended_collaboration": collab_format,
            "match_score": round(alignment["weighted_alignment"] * 100, 1),
        })

    matches.sort(key=lambda x: x["match_score"], reverse=True)

    return {
        "matching_id": f"VBM-{datetime.now().strftime('%Y%m%d%H%M')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Value-Based Matching Agent v1.0",
        "domain": domain,
        "seeking_actor": {
            "type": seeking_actor_type,
            "label": ACTOR_TYPES.get(seeking_actor_type, {}).get("label", seeking_actor_type),
            "declared_values": seeking_values,
        },
        "top_matches": matches[:3],
        "all_matches": matches,
        "matching_rationale": (
            f"Sur le domaine '{domain}', {len(matches)} types d'acteurs analysés. "
            f"Alignement basé sur {len(HUMAN_RIGHTS_VALUES)} valeurs droits humains DUDH/UNGP."
        ),
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — VALUE-BASED MATCHING AGENT")
    print("  Mise en Relation par Valeurs Droits Humains")
    print("=" * 70)

    result = match_actors(
        domain="statelessness",
        seeking_actor_type="CORPORATION",
        seeking_values=["ACCOUNTABILITY", "SUSTAINABILITY", "DIGNITY"],
    )

    print(f"\n🤝 MATCHING: {result['matching_id']}")
    print(f"   Domaine: {result['domain']}")
    sa = result["seeking_actor"]
    print(f"   Acteur cherchant: {sa['label']}")
    print(f"   Valeurs déclarées: {', '.join(HUMAN_RIGHTS_VALUES.get(v, {}).get('label', v) for v in sa['declared_values'])}")

    print(f"\n✨ TOP 3 CORRESPONDANCES:")
    for i, match in enumerate(result["top_matches"], 1):
        alignment = match["value_alignment"]
        collab = match["recommended_collaboration"]
        print(f"\n   {i}. [{match['match_score']:.0f}/100] {match['actor_label']}")
        print(f"      Compatibilité: {alignment['compatibility']}")
        print(f"      Valeurs partagées: {', '.join(alignment['shared_values_labels'][:3])}")
        print(f"      Format recommandé: {collab['label']}")
        print(f"      Durée: {collab['duration']}")
        print(f"      Formalisation: {collab['formalization'][:55]}...")
        print(f"      Besoins acteur: {', '.join(match['typical_needs'][:2])}")

    print(f"\n📋 LOGIQUE DE MATCHING:")
    print(f"   {result['matching_rationale']}")

    print(f"\n✅ Value-Based Matching Agent — {len(result['all_matches'])} correspondances trouvées")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
