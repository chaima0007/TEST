#!/usr/bin/env python3
"""Expertise Knowledge Base — CaelumSwarm™
Base de connaissances expert pour chaque domaine CaelumSwarm — référentiel consultable.
Usage : python3 scripts/expertise-knowledge-base.py
"""

import json
import os

# ---------------------------------------------------------------------------
# Base de connaissances
# ---------------------------------------------------------------------------

KNOWLEDGE_BASE = {
    "CSDDD": {
        "nom_complet": "Corporate Sustainability Due Diligence Directive",
        "référence_légale": "EU 2024/1760, applicable 2027-07-26",
        "entreprises_concernées": (
            "Entreprises >500 salariés et >150M EUR CA (phase 1), "
            ">250 salariés et >40M EUR CA dans secteurs à risque (phase 2)"
        ),
        "obligations_clés": [
            "Due diligence droits humains et environnement sur toute la chaîne de valeur",
            "Plan de transition climatique aligné Accord de Paris",
            "Responsabilité civile pour dommages causés ou facilités",
            "Rapportage annuel public sur mesures due diligence",
            "Engagement parties prenantes (travailleurs, communautés affectées)",
        ],
        "sanctions": "Jusqu'à 5% du CA mondial net",
        "autorité_surveillance": "Autorités nationales désignées par chaque État membre",
        "sources_officielles": [
            "eur-lex.europa.eu/legal-content/FR/TXT/?uri=OJ:L_202401760",
            "ec.europa.eu/info/business-economy-euro/doing-business-eu/corporate-sustainability-due-diligence",
        ],
        "mots_clés": [
            "due diligence", "chaîne de valeur", "supply chain", "droits humains",
            "CSRD", "transition climatique", "responsabilité civile", "compliance",
        ],
        "liens_engines": [
            "supply_chain_transparency", "forced_labor_supply_chain",
            "corporate_accountability", "climate_transition"
        ],
    },
    "3TG_MINERAIS": {
        "nom_complet": "Tantalum, Tungsten, Tin, Gold — Minerais de conflit",
        "référence_légale": "US Dodd-Frank Act Section 1502 (2010) + EU Reg 2017/821",
        "description": (
            "Minerais extraits dans des zones de conflit et finançant des groupes armés, "
            "principalement en Afrique centrale"
        ),
        "sources": [
            "SEC.gov — Section 1502 Conflict Minerals Reporting",
            "ITRI iTSCi (tin, tantalum, tungsten)",
            "OECD Due Diligence Guidance for Responsible Mineral Supply Chains",
            "RMI — Responsible Minerals Initiative",
        ],
        "pays_risque": ["DRC (RDC)", "Rwanda", "Uganda", "Burundi", "Centrafrique", "Zimbabwe"],
        "certifications": [
            "RCS/RMI RMAP (Responsible Minerals Assurance Process)",
            "iTSCi (ITRI Tin Supply Chain Initiative)",
            "Better Gold Initiative",
            "London Bullion Market Association (LBMA) — or",
        ],
        "mots_clés": [
            "conflict minerals", "minerais conflit", "tantalum", "tungsten", "tin", "gold",
            "3TG", "RDC", "Congo", "supply chain", "OECD guidance",
        ],
        "obligations_reporting": "Formulaire SD + Rapport CM sur SEC EDGAR (entreprises cotées US)",
    },
    "ILO_CORE_CONVENTIONS": {
        "nom_complet": "Conventions fondamentales de l'Organisation Internationale du Travail",
        "adoptées": "Déclaration OIT de 1998 — principes et droits fondamentaux au travail",
        "conventions": [
            "C87 — Liberté syndicale et protection du droit syndical (1948)",
            "C98 — Droit d'organisation et de négociation collective (1949)",
            "C29 — Travail forcé ou obligatoire (1930)",
            "C105 — Abolition du travail forcé (1957)",
            "C138 — Âge minimum d'admission à l'emploi (1973)",
            "C182 — Pires formes de travail des enfants (1999)",
            "C100 — Égalité de rémunération (1951)",
            "C111 — Discrimination (emploi et profession) (1958)",
        ],
        "nb_ratifications": "187 États membres OIT",
        "source": "ilo.org/global/standards/introduction-to-international-labour-standards",
        "mots_clés": [
            "travail forcé", "enfants", "syndicat", "discrimination", "rémunération",
            "OIT", "ILO", "conventions fondamentales", "droits au travail",
        ],
        "liens_engines": [
            "forced_labor_supply_chain", "child_labor_exploitation",
            "gender_wage_gap", "freedom_of_association"
        ],
    },
    "UNGP": {
        "nom_complet": "UN Guiding Principles on Business & Human Rights (Principes Ruggie)",
        "adoptés": "2011, unanimité Conseil ONU des droits de l'homme (résolution 17/4)",
        "auteur": "John Ruggie, Représentant spécial du Secrétaire général de l'ONU",
        "piliers": [
            "Pilier 1 — Protéger : obligation des États de protéger contre les violations par les entreprises",
            "Pilier 2 — Respecter : responsabilité des entreprises de respecter les droits humains",
            "Pilier 3 — Remédier : accès effectif à des mécanismes de recours",
        ],
        "source": "ohchr.org/en/business-and-human-rights/guiding-principles",
        "portée": "Non contraignant mais référence mondiale pour les normes due diligence",
        "mots_clés": [
            "UNGPs", "Ruggie", "droits humains", "entreprises", "due diligence",
            "recours", "mécanismes", "Conseil ONU", "OHCHR",
        ],
        "liens_engines": [
            "corporate_accountability", "access_to_justice", "human_rights_defenders",
        ],
    },
    "CSRD": {
        "nom_complet": "Corporate Sustainability Reporting Directive",
        "référence_légale": "EU 2022/2464, applicable par phases 2024-2028",
        "phases": [
            "2024 — Entreprises déjà soumises NFRD (>500 salariés, cotées)",
            "2025 — Grandes entreprises non cotées (>250 salariés OU >40M CA OU >20M total bilan)",
            "2026 — PME cotées (option opt-out jusqu'en 2028)",
            "2028 — Filiales UE d'entreprises pays tiers",
        ],
        "standards_reporting": [
            "ESRS E1 à E5 — Environnement (climat, biodiversité, eau, ressources, pollution)",
            "ESRS S1 à S4 — Social (salariés, travailleurs chaîne valeur, communautés, consommateurs)",
            "ESRS G1 — Gouvernance, éthique, lobbying",
        ],
        "concept_clé": "Double matérialité : impact de l'entreprise sur le monde + risques/opportunités pour l'entreprise",
        "assurance": "Vérification par commissaire aux comptes (limited assurance d'abord, reasonable ensuite)",
        "sources": [
            "ec.europa.eu/info/publications/sustainable-finance-eu-taxonomy",
            "efrag.org/public-interest/sustainability-reporting",
        ],
        "mots_clés": [
            "CSRD", "reporting", "durabilité", "ESG", "ESRS", "double matérialité",
            "non-financial", "NFRD", "EFRAG", "taxonomie UE",
        ],
    },
    "GRI_STANDARDS": {
        "nom_complet": "Global Reporting Initiative Standards",
        "editeur": "Global Reporting Initiative (GRI), Amsterdam",
        "structure": [
            "GRI 1 — Fondements 2021 (principes de reporting)",
            "GRI 2 — Informations générales 2021 (gouvernance, stratégie)",
            "GRI 3 — Sujets matériels 2021 (détermination matérialité)",
            "GRI 200 — Thèmes économiques",
            "GRI 300 — Thèmes environnementaux (301-308)",
            "GRI 400 — Thèmes sociaux (401-419)",
        ],
        "utilisateurs": "Environ 10 000 organisations dans 100+ pays",
        "interopérabilité": "Aligné CSRD/ESRS, ISSB, SASB, SDGs ONU",
        "source": "gri.org/standards",
        "mots_clés": [
            "GRI", "reporting", "matérialité", "ESG", "social", "environnement",
            "gouvernance", "indicateurs", "standards",
        ],
    },
    "OCDE_MNEGUIDELINES": {
        "nom_complet": "Principes directeurs de l'OCDE à l'intention des entreprises multinationales",
        "version_actuelle": "2023 (mise à jour incluant changement climatique et biodiversité)",
        "adoptés_par": "50 gouvernements adhérents (pays OCDE + pays partenaires)",
        "domaines": [
            "Droits de l'homme", "Emploi et relations professionnelles",
            "Environnement", "Lutte contre la corruption",
            "Intérêts des consommateurs", "Science et technologie",
            "Concurrence", "Fiscalité",
        ],
        "mécanisme": "Points de contact nationaux (PCN) pour résolution des différends",
        "source": "mneguidelines.oecd.org",
        "mots_clés": [
            "OCDE", "multinationales", "MNE", "PCN", "due diligence",
            "droits humains", "principes directeurs",
        ],
    },
    "TRAVAIL_FORCE": {
        "nom_complet": "Travail forcé — définition, indicateurs et législation",
        "définition_ilo": (
            "Tout travail ou service exigé d'un individu sous la menace d'une peine quelconque "
            "et pour lequel ledit individu ne s'est pas offert de plein gré (Convention C29)"
        ),
        "indicateurs_ilo": [
            "Abus de vulnérabilité", "Tromperie", "Restriction de liberté de mouvement",
            "Isolement", "Violence physique et sexuelle", "Intimidation et menaces",
            "Rétention de documents d'identité", "Servitude pour dettes",
            "Conditions de vie et de travail abusives", "Heures supplémentaires excessives",
        ],
        "législations_clés": [
            "US Uyghur Forced Labor Prevention Act (UFLPA) 2021",
            "EU Forced Labour Regulation (2024/3015)",
            "UK Modern Slavery Act 2015",
            "Australian Modern Slavery Act 2018",
        ],
        "sources": [
            "ilo.org/global/topics/forced-labour",
            "ilo.org/wcmsp5/groups/public/---ed_norm/---declaration/documents/publication/wcms_203832.pdf",
        ],
        "mots_clés": [
            "travail forcé", "esclavage moderne", "forced labor", "UFLPA",
            "Xinjiang", "Modern Slavery Act", "servitude", "traite",
        ],
        "liens_engines": [
            "forced_labor_supply_chain", "forced_marriage_rights",
            "debt_bondage_modern_slavery", "human_trafficking_exploitation",
        ],
    },
    "DROITS_ENFANT_ENTREPRISES": {
        "nom_complet": "Droits de l'enfant et principes pour les entreprises",
        "cadre": "Children's Rights and Business Principles (UNICEF, UN Global Compact, Save the Children)",
        "principes_clés": [
            "Respecter et soutenir les droits de l'enfant dans toutes les activités",
            "Contribuer à l'élimination du travail des enfants",
            "Assurer des conditions de travail décentes pour les parents",
            "Protéger les enfants dans les activités de marketing et publicité",
            "Respecter et soutenir les droits de l'enfant dans le cadre de la sécurité",
        ],
        "age_minimum_travail": "15 ans (14 dans pays développement sous conditions), 18 ans pour travaux dangereux",
        "pires_formes": [
            "Esclavage, traite, servitude pour dettes",
            "Prostitution et pornographie",
            "Activités illicites (trafic drogues)",
            "Travaux dangereux pour la santé/sécurité",
        ],
        "source": "unicef.org/csr/childrensrights.html",
        "mots_clés": [
            "travail enfant", "child labor", "âge minimum", "pires formes",
            "UNICEF", "C182", "C138", "droits enfant",
        ],
    },
    "ACCES_JUSTICE_MECANISMES": {
        "nom_complet": "Mécanismes d'accès à la justice et recours non judiciaires",
        "catégories": [
            "Judiciaires : tribunaux nationaux, juridictions internationales (CPI, CIJ)",
            "Non judiciaires étatiques : médiateurs, institutions droits humains, PCN OCDE",
            "Non judiciaires non étatiques : mécanismes de réclamation entreprises, arbitrage",
        ],
        "principes_effectivité": [
            "Légitimité", "Accessibilité", "Prévisibilité", "Équité",
            "Transparence", "Compatibilité avec les droits", "Source d'apprentissage continu",
            "Fondés sur l'engagement et le dialogue (pour mécanismes non étatiques)",
        ],
        "source": "ohchr.org/en/access-to-justice",
        "mots_clés": [
            "accès justice", "recours", "mécanismes réclamation", "PCN", "médiation",
            "arbitrage", "judiciaire", "non judiciaire", "Pilier 3 UNGP",
        ],
    },
    "PARIS_AGREEMENT_CLIMATE": {
        "nom_complet": "Accord de Paris sur le changement climatique",
        "adoptés": "COP21, 12 décembre 2015, entré en vigueur 4 novembre 2016",
        "objectifs": [
            "Limiter le réchauffement à 1.5°C au-dessus des niveaux préindustriels",
            "Renforcer la capacité d'adaptation aux impacts climatiques",
            "Aligner les flux financiers sur une trajectoire bas-carbone",
        ],
        "mécanismes_entreprises": [
            "Science Based Targets initiative (SBTi) — objectifs alignés 1.5°C",
            "CDP Climate Disclosure — reporting carbone",
            "TCFD — recommandations disclosure risques climatiques",
            "Net Zero Standard (SBTi) — neutralité carbone 2050",
        ],
        "source": "unfccc.int/process-and-meetings/the-paris-agreement",
        "mots_clés": [
            "accord paris", "1.5°C", "neutralité carbone", "net zero", "GES",
            "transition climatique", "SBTi", "TCFD", "CDP", "COP",
        ],
        "liens_engines": [
            "climate_transition", "carbon_emissions_tracking",
            "renewable_energy_transition", "climate_litigation_risk",
        ],
    },
    "BIODIVERSITE_TNFD": {
        "nom_complet": "Taskforce on Nature-related Financial Disclosures",
        "cadre": "TNFD — cadre de reporting des dépendances et impacts sur la nature",
        "version": "v1.0 publiée septembre 2023",
        "approche": "LEAP : Localiser, Évaluer, Évaluer, Préparer (en anglais : Locate, Evaluate, Assess, Prepare)",
        "capitaux_naturels": [
            "Biodiversité", "Eau douce", "Sols et terres", "Océans",
            "Atmosphère (hors climat)", "Minéraux et ressources",
        ],
        "alignements": ["COP15 Kunming-Montréal Global Biodiversity Framework", "CSRD ESRS E4", "ISSB"],
        "source": "tnfd.global",
        "mots_clés": [
            "TNFD", "biodiversité", "nature", "LEAP", "capital naturel",
            "dépendances", "impacts", "COP15", "Kunming",
        ],
    },
}


# ---------------------------------------------------------------------------
# Fonctions de recherche et consultation
# ---------------------------------------------------------------------------

def search_knowledge(query: str) -> list:
    """Recherche par mots-clés dans la base de connaissances.
    Retourne une liste d'entrées correspondantes triées par pertinence.
    """
    query_lower = query.lower()
    query_terms = query_lower.split()

    results = []
    for key, entry in KNOWLEDGE_BASE.items():
        score = 0

        # Recherche dans les mots-clés
        entry_keywords = [kw.lower() for kw in entry.get("mots_clés", [])]
        for term in query_terms:
            for kw in entry_keywords:
                if term in kw or kw in term:
                    score += 3

        # Recherche dans nom_complet
        nom = entry.get("nom_complet", "").lower()
        for term in query_terms:
            if term in nom:
                score += 2

        # Recherche dans description / définition
        for field in ["description", "définition_ilo", "concept_clé"]:
            val = entry.get(field, "").lower()
            for term in query_terms:
                if term in val:
                    score += 1

        # Recherche dans sources et obligations
        for field in ["obligations_clés", "conventions", "piliers"]:
            items = entry.get(field, [])
            for item in items:
                for term in query_terms:
                    if term in item.lower():
                        score += 1

        if score > 0:
            results.append({
                "clé": key,
                "nom_complet": entry.get("nom_complet", key),
                "pertinence": score,
                "aperçu": _get_entry_summary(entry),
            })

    results.sort(key=lambda x: x["pertinence"], reverse=True)
    return results


def _get_entry_summary(entry: dict) -> str:
    """Génère un bref aperçu d'une entrée."""
    for field in ["description", "définition_ilo", "concept_clé", "description"]:
        val = entry.get(field)
        if val:
            return val[:120] + ("..." if len(val) > 120 else "")
    # Fallback : première obligation ou premier pilier
    for field in ["obligations_clés", "piliers", "conventions"]:
        items = entry.get(field, [])
        if items:
            return items[0][:120]
    return entry.get("référence_légale", "")


def get_domain_brief(domain_key: str) -> dict:
    """Retourne un résumé structuré d'un domaine de la base."""
    entry = KNOWLEDGE_BASE.get(domain_key.upper())
    if not entry:
        # Essai insensible à la casse
        for k in KNOWLEDGE_BASE:
            if k.lower() == domain_key.lower():
                entry = KNOWLEDGE_BASE[k]
                break
    if not entry:
        return {"erreur": f"Domaine '{domain_key}' non trouvé dans la base"}

    return {
        "clé": domain_key,
        "nom_complet": entry.get("nom_complet"),
        "référence_légale": entry.get("référence_légale"),
        "point_clé": entry.get("obligations_clés", entry.get("piliers", entry.get("conventions", [None])))[0],
        "source_principale": (entry.get("sources", entry.get("sources_officielles", [entry.get("source", "N/A")])
                               ) or ["N/A"])[0],
        "mots_clés": entry.get("mots_clés", [])[:5],
    }


def get_sources_for_engine(engine_prefix: str) -> list:
    """Retourne les sources recommandées pour un engine donné (via engine_prefix ou liens_engines)."""
    prefix_lower = engine_prefix.lower()
    sources = []

    for key, entry in KNOWLEDGE_BASE.items():
        # Vérifier si l'engine est listé dans liens_engines
        liens = entry.get("liens_engines", [])
        matched = any(prefix_lower in lien.lower() or lien.lower() in prefix_lower for lien in liens)

        # Vérifier aussi si le préfixe apparaît dans les mots-clés
        if not matched:
            kws = entry.get("mots_clés", [])
            matched = any(prefix_lower in kw.lower() for kw in kws)

        if matched:
            entry_sources = (
                entry.get("sources", [])
                or entry.get("sources_officielles", [])
                or ([entry["source"]] if "source" in entry else [])
            )
            sources.append({
                "domaine": key,
                "nom_complet": entry.get("nom_complet"),
                "sources": entry_sources,
            })

    return sources


def export_knowledge_summary(output_path: str = None) -> str:
    """Exporte toute la base en docs/knowledge-base.md."""
    docs_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
    os.makedirs(docs_dir, exist_ok=True)

    if output_path is None:
        output_path = os.path.join(docs_dir, "knowledge-base.md")

    lines = [
        "# CaelumSwarm™ — Knowledge Base Expert",
        "",
        f"Base de connaissances pour les {len(KNOWLEDGE_BASE)} domaines référencés.",
        "",
        "---",
        "",
        "## Sommaire",
        "",
    ]

    for key, entry in KNOWLEDGE_BASE.items():
        nom = entry.get("nom_complet", key)
        lines.append(f"- [{nom}](#{key.lower().replace('_', '-')})")

    lines += ["", "---", ""]

    for key, entry in KNOWLEDGE_BASE.items():
        nom = entry.get("nom_complet", key)
        lines += [
            f"## {nom}",
            "",
            f"**Clé :** `{key}`  ",
        ]

        for field_label, field_key in [
            ("Référence légale", "référence_légale"),
            ("Adopté", "adoptés"),
            ("Auteur", "auteur"),
            ("Éditeur", "editeur"),
            ("Cadre", "cadre"),
            ("Version", "version"),
            ("Approche", "approche"),
            ("Portée", "portée"),
            ("Description", "description"),
            ("Définition", "définition_ilo"),
            ("Concept clé", "concept_clé"),
            ("Assurance", "assurance"),
            ("Entreprises concernées", "entreprises_concernées"),
            ("Sanctions", "sanctions"),
        ]:
            val = entry.get(field_key)
            if val:
                lines.append(f"**{field_label} :** {val}  ")

        lines.append("")

        for list_field_label, list_field_key in [
            ("Obligations clés", "obligations_clés"),
            ("Piliers", "piliers"),
            ("Conventions", "conventions"),
            ("Principes clés", "principes_clés"),
            ("Catégories", "catégories"),
            ("Principes d'effectivité", "principes_effectivité"),
            ("Domaines", "domaines"),
            ("Phases", "phases"),
            ("Standards reporting", "standards_reporting"),
            ("Structure", "structure"),
            ("Législations clés", "législations_clés"),
            ("Indicateurs", "indicateurs_ilo"),
            ("Pires formes", "pires_formes"),
            ("Mécanismes entreprises", "mécanismes_entreprises"),
            ("Capitaux naturels", "capitaux_naturels"),
            ("Alignements", "alignements"),
            ("Certifications", "certifications"),
        ]:
            items = entry.get(list_field_key)
            if items:
                lines.append(f"**{list_field_label} :**")
                for item in items:
                    lines.append(f"- {item}")
                lines.append("")

        for str_list_field_label, str_list_field_key in [
            ("Sources", "sources"),
            ("Sources officielles", "sources_officielles"),
        ]:
            srcs = entry.get(str_list_field_key)
            if srcs:
                lines.append(f"**{str_list_field_label} :**")
                for src in srcs:
                    lines.append(f"- {src}")
                lines.append("")

        if "source" in entry and "sources" not in entry and "sources_officielles" not in entry:
            lines.append(f"**Source :** {entry['source']}  ")
            lines.append("")

        kws = entry.get("mots_clés", [])
        if kws:
            lines.append(f"**Mots-clés :** {', '.join(kws)}")
            lines.append("")

        engines = entry.get("liens_engines", [])
        if engines:
            lines.append(f"**Engines liés :** {', '.join(f'`{e}`' for e in engines)}")
            lines.append("")

        lines += ["---", ""]

    lines += [
        "",
        "*Généré automatiquement par expertise-knowledge-base.py — CaelumSwarm™*",
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_path


# ---------------------------------------------------------------------------
# Affichage console
# ---------------------------------------------------------------------------

BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"


def print_search_results(query: str, results: list) -> None:
    """Affiche les résultats d'une recherche."""
    print(f"\n{BOLD}Recherche : \"{query}\"{RESET}")
    if not results:
        print("  Aucun résultat trouvé.")
        return
    print(f"  {len(results)} résultat(s) :\n")
    for i, r in enumerate(results, start=1):
        print(f"  {i}. {BOLD}{r['clé']}{RESET} — {r['nom_complet']}")
        print(f"     Pertinence : {r['pertinence']} | {r['aperçu']}")
    print()


def print_brief(domain_key: str) -> None:
    """Affiche le brief d'un domaine."""
    brief = get_domain_brief(domain_key)
    if "erreur" in brief:
        print(f"  {YELLOW}{brief['erreur']}{RESET}")
        return
    print(f"\n{BOLD}Brief — {brief['nom_complet']}{RESET}")
    print(f"  Clé              : {brief['clé']}")
    if brief.get("référence_légale"):
        print(f"  Référence légale : {brief['référence_légale']}")
    if brief.get("point_clé"):
        print(f"  Point clé        : {brief['point_clé']}")
    if brief.get("source_principale"):
        print(f"  Source           : {brief['source_principale']}")
    if brief.get("mots_clés"):
        print(f"  Mots-clés        : {', '.join(brief['mots_clés'])}")
    print()


def print_kb_stats() -> None:
    """Affiche les statistiques globales de la base."""
    total_keywords = sum(len(e.get("mots_clés", [])) for e in KNOWLEDGE_BASE.values())
    total_sources = sum(
        len(e.get("sources", []) or e.get("sources_officielles", []))
        for e in KNOWLEDGE_BASE.values()
    )
    with_engines = sum(1 for e in KNOWLEDGE_BASE.values() if e.get("liens_engines"))

    print(f"\n{BOLD}Statistiques — Knowledge Base CaelumSwarm™{RESET}")
    print(f"  Domaines indexés      : {len(KNOWLEDGE_BASE)}")
    print(f"  Total mots-clés       : {total_keywords}")
    print(f"  Total sources         : {total_sources}")
    print(f"  Domaines liés engines : {with_engines}")
    print(f"  Domaines disponibles  :")
    for key in KNOWLEDGE_BASE:
        nom = KNOWLEDGE_BASE[key].get("nom_complet", key)
        print(f"    {CYAN}{key:<28}{RESET} — {nom}")
    print()


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}CaelumSwarm™ — Expertise Knowledge Base{RESET}")

    # Statistiques générales
    print_kb_stats()

    # Demo 1 : recherche "travail forcé"
    results_tf = search_knowledge("travail forcé")
    print_search_results("travail forcé", results_tf)

    # Demo 2 : recherche "CSRD reporting durabilité"
    results_csrd = search_knowledge("CSRD reporting durabilité")
    print_search_results("CSRD reporting durabilité", results_csrd)

    # Demo 3 : brief CSDDD
    print_brief("CSDDD")

    # Demo 4 : brief ILO_CORE_CONVENTIONS
    print_brief("ILO_CORE_CONVENTIONS")

    # Demo 5 : sources pour engine forced_marriage_rights
    print(f"\n{BOLD}Sources pour engine 'forced_marriage'{RESET}")
    sources = get_sources_for_engine("forced_marriage")
    if sources:
        for s in sources:
            print(f"  {BOLD}{s['domaine']}{RESET} — {s['nom_complet']}")
            for src in s["sources"]:
                print(f"    • {src}")
    else:
        print("  Aucune source spécifique trouvée.")
    print()

    # Demo 6 : sources pour engine climate_transition
    print(f"{BOLD}Sources pour engine 'climate_transition'{RESET}")
    sources_climate = get_sources_for_engine("climate")
    for s in sources_climate:
        print(f"  {BOLD}{s['domaine']}{RESET} — {s['nom_complet']}")
        for src in s["sources"][:2]:
            print(f"    • {src}")
    print()

    # Export knowledge base complète
    output_path = export_knowledge_summary()
    print(f"{BOLD}Export complet :{RESET} {output_path}")

    # Export JSON résumé
    summary = {
        "nb_domaines": len(KNOWLEDGE_BASE),
        "domaines": list(KNOWLEDGE_BASE.keys()),
        "recherche_demo": {
            "query": "travail forcé",
            "nb_resultats": len(results_tf),
            "top_resultat": results_tf[0]["clé"] if results_tf else None,
        },
    }
    docs_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
    json_path = os.path.join(docs_dir, "knowledge-base-summary.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Export JSON     : {json_path}")

    print(f"\n{BOLD}Knowledge Base terminée.{RESET}\n")


if __name__ == "__main__":
    main()
