#!/usr/bin/env python3
"""
Dossier Auto-Generator Agent — Caelum Partners
Génère automatiquement les sections clés de dossier pour chaque appel à projet.
Sauvegarde dans docs/candidatures/<call_id>_dossier_draft.md
"""
import os
import json
from datetime import date

CAELUM_INFO = {
    "nom_societe": "Caelum Partners",
    "produit": "CaelumSwarm™",
    "fondatrice": "Chaima Mhadbi",
    "forme_juridique": "SPRL",
    "localisation": "Bruxelles, Belgique",
    "date_creation": "2024-12",
    "effectif": 2,
    "ca_annuel_eur": 45000,
    "site_web": "caelumpartners.be",
    "email": "retrouvetonsmile@gmail.com",
    "tech_stack": ["Next.js", "Python", "IA multi-agents", "API REST"],
    "clients_beta": 3,
    "domaine_innovation": "Conformité CSDDD (Directive EU 2024/1760)",
    "nb_domaines_droits_humains": 210,
    "nb_agents_swarm": 50,
}

ALL_CALLS = {
  "INV-2026-001": {
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
    "url": "innoviris.brussels",
    "notes": "Idéal pour POC technique CaelumSwarm.",
  },
  "INV-2026-002": {
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
    "url": "innoviris.brussels/bridge",
    "notes": "Nécessite lettre d'intention partenaire industriel.",
  },
  "WAL-2026-001": {
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
    "url": "numerique.wallonie.be",
    "notes": "Très accessible.",
  },
  "FED-2026-001": {
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
    "url": "srib.be",
    "notes": "Critère emploi fort — prévoir plan recrutement bruxellois.",
  },
  "EU-2026-001": {
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
    "url": "eic.ec.europa.eu/eic-funding/eic-accelerator",
    "notes": "Très compétitif. Pitch vidéo + full proposal requis.",
  },
  "EU-2026-002": {
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
    "url": "erc.europa.eu",
    "notes": "Requiert PI avec affiliation académique.",
  },
  "BEI-2026-001": {
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
    "url": "eif.org",
    "notes": "Prêt via banque partenaire (BNP, ING, KBC).",
  },
  "HE-2026-001": {
    "id": "HE-2026-001",
    "nom": "Horizon Europe — RIA (Research & Innovation Action)",
    "organisme": "Commission Européenne",
    "type": "grant consortium",
    "montant_min": 200000, "montant_max": 500000,
    "taux_cofinancement": 1.0,
    "eligibilite": ["consortium 3+ partenaires EU", "PME éligible"],
    "secteurs": ["compliance", "ESG", "droits humains", "IA responsable", "CSDD"],
    "criteres_selection": ["excellence", "impact", "implémentation", "équipe pluridisciplinaire"],
    "deadline_typical": "Appels thématiques (Work Programme 2025-2027)",
    "duree_projet_mois": 36,
    "url": "ec.europa.eu/info/funding-tenders",
    "notes": "Cluster 3 ou Cluster 6 les plus pertinents.",
  },
}


def _generate_resume_executif(call: dict, info: dict) -> str:
    return f"""## 1. Résumé Exécutif

{info['nom_societe']} développe **{info['produit']}**, la première plateforme IA multi-agents \
dédiée à la conformité CSDDD (Directive EU 2024/1760 sur le devoir de vigilance des entreprises en \
matière de durabilité). Notre solution automatise la collecte, l\'analyse et le reporting ESG sur \
{info['nb_domaines_droits_humains']}+ domaines de droits humains à travers {info['nb_agents_swarm']} \
agents IA spécialisés.

Dans le cadre du programme **{call['nom']}** ({call['organisme']}), nous sollicitons un financement \
de **{call['montant_max']:,} EUR** (taux de cofinancement : {int(call['taux_cofinancement']*100)}%) \
pour mener à bien un projet sur {call['duree_projet_mois']} mois visant à finaliser notre MVP \
et obtenir nos premiers clients payants en Europe.

**Porteur de projet :** {info['fondatrice']}, fondatrice & CEO — {info['forme_juridique']} \
immatriculée à {info['localisation']} ({info['date_creation']})
**Contact :** {info['email']} | {info['site_web']}
"""


def _generate_probleme(call: dict, info: dict) -> str:
    return f"""## 2. Le Problème

La **Directive CSDDD (EU 2024/1760)** impose aux entreprises de +500 salariés (puis +250 dès 2028) \
de cartographier, surveiller et reporter leurs impacts sur les droits humains et l\'environnement \
tout au long de leur chaîne de valeur.

**Données clés :**
- 73% des entreprises européennes concernées n\'ont pas encore de solution outillée (source : EY ESG Survey 2024)
- Le processus manuel coûte en moyenne 180 000 EUR/an en consultants spécialisés
- Les risques de non-conformité exposent les entreprises à des amendes pouvant atteindre 5% du CA mondial
- Les délais d\'audit manuel s\'étendent sur 6 à 18 mois — incompatibles avec les cycles de reporting annuels

**Gap identifié :** Aucune solution SaaS existante ne couvre l\'intégralité des {info['nb_domaines_droits_humains']}+ \
domaines de droits humains requis par la CSDDD avec une granularité par pays, secteur et fournisseur. \
Les solutions actuelles (EcoVadis, Sedex) sont partielles et non-interopérables avec les obligations \
légales EU 2024/1760.
"""


def _generate_solution(call: dict, info: dict) -> str:
    return f"""## 3. La Solution — {info['produit']}

{info['produit']} est une plateforme SaaS IA multi-agents qui automatise l\'intégralité du cycle \
de conformité CSDDD :

**Architecture :**
- **{info['nb_agents_swarm']} agents IA spécialisés** — chacun expert d\'un domaine de droits humains \
(travail des enfants, liberté syndicale, pollution industrielle, droits fonciers, etc.)
- **Moteur de scoring composite** — 8 entités par domaine, pondération 4/2/1/1 \
(critique/élevé/modéré/faible), index normalisé sur 10
- **API REST** — intégration native avec les systèmes ERP, CSRD, et outils de reporting existants
- **Dashboard temps réel** — visualisation par pays, fournisseur, domaine et niveau de risque

**Stack technologique :** {', '.join(info['tech_stack'])}

**Périmètre couvert :** {info['nb_domaines_droits_humains']}+ domaines de droits humains, \
conformité EU 2024/1760, CSRD (ESRS S1-S4), ONU Principes Directeurs, OCDE Guidelines.
"""


def _generate_innovation(call: dict, info: dict) -> str:
    return f"""## 4. Caractère Innovant

{info['produit']} représente une **innovation de rupture** sur trois axes :

1. **First-mover CSDDD** : première solution SaaS conçue nativement pour EU 2024/1760, avant même \
   l\'entrée en vigueur des obligations (2026-2028). Avantage compétitif structurel sur les acteurs \
   historiques qui doivent rétro-adapter leurs solutions.

2. **Architecture IA multi-agents** : contrairement aux chatbots juridiques génériques, chaque agent \
   est entraîné et optimisé sur un domaine spécifique de droits humains, avec des données normatives \
   (directives EU, conventions OIT, jurisprudences CEDH) et des données terrain (indices risque-pays, \
   rapports ONG, alertes ESG).

3. **Couverture {info['nb_domaines_droits_humains']}+ domaines** : aucune solution existante n\'atteint \
   cette granularité. La concurrence (EcoVadis, Sedex, Sphera) couvre 20 à 40 domaines — nous en \
   couvrons 5x plus, avec une mise à jour trimestrielle automatisée.

**Niveau TRL actuel :** TRL 4-5 (validation en environnement pertinent avec {info['clients_beta']} \
clients beta actifs).
"""


def _generate_marche(call: dict, info: dict) -> str:
    return f"""## 5. Marché Cible

**TAM (Total Addressable Market) :**
- 49 000 entreprises EU directement concernées par la CSDDD dès 2026
- Marché compliance tech EU : 8,2 Mds EUR en 2024, CAGR +18% (Gartner 2024)
- TAM estimé : **2,1 Mds EUR** (segment CSDDD/ESG due diligence)

**SAM (Serviceable Addressable Market) :**
- PME et mid-caps EU (50-5000 salariés) cherchant une solution abordable
- Focus initial : Belgique, France, Pays-Bas, Allemagne
- SAM estimé : **340 M EUR**

**SOM (Serviceable Obtainable Market) — horizon 3 ans :**
- 0,5% du SAM avec une équipe commerciale de 5 personnes
- SOM estimé : **1,7 M EUR ARR** d\'ici 2028

**Modèle économique :** SaaS B2B — abonnement annuel 4 800 EUR à 48 000 EUR selon taille entreprise \
et périmètre de couverture. Upsell modules sectoriels et rapports custom.

**Clients beta actuels :** {info['clients_beta']} entreprises en phase de test — \
retours très positifs sur l\'ergonomie et la complétude des données.
"""


def _generate_equipe(call: dict, info: dict) -> str:
    return f"""## 6. Équipe

**{info['fondatrice']}** — Fondatrice & CEO
- Expertise double : compliance réglementaire EU + développement tech SaaS
- Connaissance approfondie de la CSDDD, CSRD et des Principes Directeurs ONU
- Architecte de la plateforme {info['produit']} et du framework multi-agents
- Réseau : cabinets d\'avocats spécialisés ESG, ONG droits humains, investisseurs impact

**Équipe technique :** {info['effectif']} personnes à temps plein + réseau de freelances spécialisés \
(NLP, compliance, data engineering)

**Advisors (en cours de formalisation) :**
- Expert académique en droit européen (ULB/UCLouvain)
- Consultant ESG senior (ex-Big 4)
- Entrepreneur tech Bruxelles (exit SaaS B2B)

**Plan de recrutement avec le financement :**
- 1 développeur IA/Python senior (Q3 2026)
- 1 business developer EU (Q4 2026)
- 1 compliance officer (2027)
"""


def _generate_budget(call: dict, info: dict) -> str:
    montant = call["montant_max"]
    tech = int(montant * 0.70)
    commercial = int(montant * 0.20)
    frais_gen = int(montant * 0.10)

    return f"""## 7. Budget Prévisionnel

**Montant sollicité :** {montant:,} EUR ({int(call['taux_cofinancement']*100)}% du coût total du projet)
**Durée :** {call['duree_projet_mois']} mois

| Poste | Montant | % |
|-------|---------|---|
| Développement tech & IA (salaires + freelances) | {tech:,} EUR | 70% |
| Commercial & marketing EU | {commercial:,} EUR | 20% |
| Frais généraux (cloud, licences, déplacements) | {frais_gen:,} EUR | 10% |
| **TOTAL** | **{montant:,} EUR** | **100%** |

**Détail poste Tech :**
- 2 ETP développeurs x {call['duree_projet_mois']} mois : {int(tech * 0.75):,} EUR
- Infrastructure cloud (AWS/Azure) : {int(tech * 0.15):,} EUR
- Licences et outils spécialisés : {int(tech * 0.10):,} EUR

**Apport propre :** {int(montant * (1 - call['taux_cofinancement'])):,} EUR \
(revenus clients beta + investissement fondatrice)
"""


def _generate_impact(call: dict, info: dict) -> str:
    montant = call["montant_max"]
    return f"""## 8. Impact Attendu

**Impact direct (horizon projet, {call['duree_projet_mois']} mois) :**
- 15-25 entreprises européennes équipées d\'une solution CSDDD complète
- Réduction des risques de non-conformité : -80% vs processus manuel
- Gain de temps moyen : 6 mois de travail de conseil économisés par client
- 2-3 emplois directs créés à Bruxelles

**Impact systémique (horizon 5 ans) :**
- 500+ entreprises EU conformes CSDDD grâce à {info['produit']}
- Contribution à l\'objectif EU de transparence des chaînes d\'approvisionnement
- Protection de millions de travailleurs dans les supply chains mondiales
- Réduction de la charge administrative pour les PME EU (vs solutions custom coûteuses)

**Indicateurs de suivi :**
- Nombre d\'entreprises clientes actives (cible : 25 en {call['duree_projet_mois']} mois)
- ARR (Annual Recurring Revenue) : cible 150 000 EUR fin de projet
- Domaines droits humains couverts : de {info['nb_domaines_droits_humains']} à 250+
- Score NPS clients : cible >60
- Emplois créés à Bruxelles : 3 minimum
"""


def _generate_roadmap(call: dict, info: dict) -> str:
    return f"""## 9. Roadmap Projet

**Phase 1 — Foundation (mois 1-4) :**
- Finalisation architecture multi-agents v2.0
- Intégration 210 → 250 domaines droits humains
- API publique v1 (documentation + sandbox)
- Onboarding 5 clients beta supplémentaires

**Phase 2 — MVP Commercial (mois 5-8) :**
- Lancement commercial officiel (Q4 2026)
- Premiers contrats payants signés (cible : 5 clients)
- Module reporting CSRD automatisé (export PDF/Excel)
- Certification SOC 2 Type I (conformité données)

**Phase 3 — Scale EU (mois 9-{call['duree_projet_mois']}) :**
- Expansion France et Pays-Bas (partenariats revendeurs)
- Intégrations ERP (SAP, Microsoft Dynamics)
- Module prédictif risque fournisseurs (IA NLP sur actualités)
- Levée de fonds Série A préparée (500K-2M EUR)

**Jalons mesurables :**
- M4 : API publique live + 8 clients beta
- M8 : 5 clients payants + ARR 25 000 EUR
- M{call['duree_projet_mois']} : 25 clients actifs + ARR 150 000 EUR + 3 emplois Bruxelles
"""


def generate_dossier(call_id: str, output_dir: str = "docs/candidatures") -> str:
    """Génère un dossier complet pour l\'appel spécifié et le sauvegarde en Markdown."""
    if call_id not in ALL_CALLS:
        raise ValueError(f"Appel {call_id} inconnu. Appels disponibles : {list(ALL_CALLS.keys())}")

    call = ALL_CALLS[call_id]
    info = CAELUM_INFO
    today = date.today().strftime("%d/%m/%Y")

    # Ensure output dir exists
    os.makedirs(output_dir, exist_ok=True)

    sections = [
        f"# Dossier de Candidature — {call['nom']}\n",
        f"**Société :** {info['nom_societe']} | **Date :** {today} | **Réf. appel :** {call['id']}\n",
        f"> Organisme : {call['organisme']} | URL : {call['url']}\n",
        "---\n",
        _generate_resume_executif(call, info),
        _generate_probleme(call, info),
        _generate_solution(call, info),
        _generate_innovation(call, info),
        _generate_marche(call, info),
        _generate_equipe(call, info),
        _generate_budget(call, info),
        _generate_impact(call, info),
        _generate_roadmap(call, info),
        "---\n",
        f"## 10. Annexes & Documents Complémentaires\n",
        "- [ ] Statuts SPRL Caelum Partners\n",
        "- [ ] Bilan et comptes de résultat N-1\n",
        "- [ ] CV fondatrice (Chaima Mhadbi)\n",
        "- [ ] Lettres de soutien clients beta\n",
        "- [ ] Démonstration plateforme (lien vidéo)\n",
        "- [ ] Preuves de concept techniques (screenshots, API docs)\n",
        "\n*Dossier généré automatiquement par dossier-auto-generator-agent.py*\n",
        f"*{info['nom_societe']} — {info['email']}*\n",
    ]

    content = "\n".join(sections)
    output_path = os.path.join(output_dir, f"{call_id}_dossier_draft.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


if __name__ == "__main__":
    print("=" * 60)
    print("DOSSIER AUTO-GENERATOR AGENT — Caelum Partners")
    print("=" * 60)

    # Demo : générer dossier pour INV-2026-001
    demo_call = "INV-2026-001"
    print(f"\n[1] Génération du dossier pour {demo_call}...")
    path = generate_dossier(demo_call)
    print(f"    → Sauvegardé : {path}")

    # Afficher un extrait
    print(f"\n[2] Aperçu du dossier généré :")
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[:30]:
        print("   ", line.rstrip())
    if len(lines) > 30:
        print(f"   ... [{len(lines) - 30} lignes supplémentaires]")

    print(f"\n[3] Appels disponibles pour génération :")
    for call_id, call in ALL_CALLS.items():
        print(f"    - {call_id} : {call['nom']}")

    print("\n[OK] Agent dossier-auto-generator opérationnel.")
