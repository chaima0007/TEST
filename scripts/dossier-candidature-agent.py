#!/usr/bin/env python3
"""
Dossier Candidature Agent — Caelum Partners SPRL
Génère un dossier de candidature complet aux appels à projets de financement.
Produit un template structuré + checklist des pièces justificatives.
"""

import json
import os
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────
# Profil Caelum Partners (données de référence)
# ─────────────────────────────────────────────
CAELUM_PROFILE = {
    "nom": "Caelum Partners SPRL",
    "numero_tva": "BE 1234.567.890",
    "numero_bce": "1234.567.890",
    "forme_juridique": "SPRL (Société Privée à Responsabilité Limitée)",
    "adresse": "Avenue Louise 000, 1050 Bruxelles, Belgique",
    "region": "Bruxelles-Capitale",
    "date_creation": "1er septembre 2024",
    "secteur": "Tech / SaaS / Compliance / ESG",
    "code_nace": "6201 — Développement et production de logiciels",
    "site_web": "https://caelum.partners",
    "email_contact": "contact@caelum.partners",
    "capital_social": "18 500 EUR",
    "effectif_actuel": 3,
    "effectif_prevu_2ans": 12,
    "ca_annuel": "85 000 EUR (exercice 2025)",
    "ca_prevu_2026": "380 000 EUR",
    "fondateurs": [
        {
            "nom": "Fondateur A",
            "role": "CEO & Product Lead",
            "expertise": "10 ans en management & compliance EU",
        },
        {
            "nom": "Fondateur B",
            "role": "CTO & AI Architect",
            "expertise": "8 ans en IA, architectures distribuées & SaaS B2B",
        },
        {
            "nom": "Fondateur C",
            "role": "Head of Legal & ESG",
            "expertise": "Juriste spécialisé droit EU, CSDDD & droits humains",
        },
    ],
}

PROJET = {
    "nom_produit": "CaelumSwarm(tm)",
    "nom_complet": (
        "CaelumSwarm(tm) — Plateforme IA Multi-Agents pour la Conformité "
        "CSDDD et la Due Diligence en Droits Humains"
    ),
    "technologie": "Plateforme SaaS B2B, architecture multi-agents IA (Python + Next.js)",
    "marche_cible": "Grands groupes et ETI européens (>250 salariés, assujettis CSDDD)",
    "taille_marche": "4,2 milliards EUR (marché RegTech EU 2026, croissance 28% p.a.)",
    "prix_moyen_abonnement": "3 500 EUR/mois par client",
    "clients_cibles": [
        "Multinationales belges assujetties à la CSDDD (EU 2024/1760)",
        "Groupes industriels avec supply chains complexes",
        "Cabinets d'audit et de conseil ESG",
        "Fonds d'investissement ESG et ESG rating agencies",
    ],
    "differenciateurs": [
        "Seule plateforme 100% dédiée à CSDDD EU 2024/1760 avec 50+ agents IA spécialisés",
        "Architecture multi-agents vs mono-LLM (précision ×3, coût /2)",
        "Intégration native des 17 domaines de droits humains (OIT, OCDE, ONU)",
        "Onboarding en 48h, pas de données sensibles stockées côté client",
        "Made in Belgium & EU — souveraineté des données garantie",
    ],
    "directive_ciblee": "EU 2024/1760 (CSDDD) — entrée en vigueur progressive 2027-2029",
    "budget_total_projet": 750000,
    "duree_projet_mois": 24,
    "debut_projet": "2026-09-01",
}


# ─────────────────────────────────────────────
# Générateur de sections du dossier
# ─────────────────────────────────────────────
def generate_section_identification() -> dict:
    return {
        "titre": "1. IDENTIFICATION DU DEMANDEUR",
        "contenu": {
            "raison_sociale": CAELUM_PROFILE["nom"],
            "forme_juridique": CAELUM_PROFILE["forme_juridique"],
            "numero_BCE": CAELUM_PROFILE["numero_bce"],
            "numero_TVA": CAELUM_PROFILE["numero_tva"],
            "adresse_siege": CAELUM_PROFILE["adresse"],
            "region": CAELUM_PROFILE["region"],
            "date_creation": CAELUM_PROFILE["date_creation"],
            "code_NACE": CAELUM_PROFILE["code_nace"],
            "site_web": CAELUM_PROFILE["site_web"],
            "contact_principal": CAELUM_PROFILE["email_contact"],
            "capital_social": CAELUM_PROFILE["capital_social"],
            "effectif_ETP": CAELUM_PROFILE["effectif_actuel"],
            "classification_EU": "Micro-entreprise (< 10 ETP, CA < 2M EUR)",
        },
    }


def generate_section_resume_executif() -> dict:
    return {
        "titre": "2. RÉSUMÉ EXÉCUTIF",
        "contenu": {
            "pitch_100_mots": (
                "Caelum Partners développe CaelumSwarm(tm), la première plateforme "
                "SaaS d'intelligence artificielle multi-agents dédiée à la conformité "
                "avec la directive européenne CSDDD (EU 2024/1760). Notre solution "
                "automatise la due diligence en droits humains et la cartographie "
                "des risques ESG dans les chaînes d'approvisionnement mondiales. "
                "Ciblant les grands groupes et ETI européens désormais soumis à "
                "une obligation légale, nous adressons un marché de 4,2 Mrd EUR "
                "en croissance de 28% p.a. Basés à Bruxelles, nous sollicitons "
                "un financement pour accélérer notre mise à l'échelle commerciale "
                "et technique en Europe."
            ),
            "probleme_adresse": (
                "La directive CSDDD (EU 2024/1760) impose à +50 000 entreprises "
                "européennes une obligation de due diligence en droits humains sur "
                "toute leur chaîne d'approvisionnement, avec des sanctions pouvant "
                "atteindre 5% du CA mondial. Aujourd'hui, cette conformité est "
                "réalisée manuellement par des cabinets de conseil, pour un coût "
                "prohibitif (200k-500k EUR/an) et des délais de plusieurs mois. "
                "Il n'existe aucun outil SaaS automatisé, standardisé et accessible."
            ),
            "solution": (
                "CaelumSwarm(tm) automatise 90% du processus via 50+ agents IA "
                "spécialisés par domaine (travail, environnement, gouvernance, "
                "droits fondamentaux). Le résultat : un rapport CSDDD complet "
                "en 72h au lieu de 4 mois, pour un coût 10x inférieur aux "
                "alternatives humaines."
            ),
            "montant_demande": "À préciser selon le programme visé",
            "impact_prevu": (
                "200 entreprises conformes d'ici 2028, représentant 15 000 fournisseurs "
                "analysés et un impact direct sur les conditions de travail de "
                "+500 000 travailleurs dans les supply chains."
            ),
        },
    }


def generate_section_description_projet() -> dict:
    return {
        "titre": "3. DESCRIPTION DU PROJET",
        "contenu": {
            "nom_projet": PROJET["nom_complet"],
            "technologie": PROJET["technologie"],
            "directive_ciblee": PROJET["directive_ciblee"],
            "objectifs_principaux": [
                "Développer et valider 3 modules IA supplémentaires (supply chain mapping, "
                "grievance mechanism, corrective action plan)",
                "Recruter 5 ingénieurs IA et 2 juristes ESG",
                "Atteindre 20 clients grands comptes signés (ARR > 840k EUR)",
                "Obtenir la certification ISO 27001 et SOC 2 Type II",
                "Lancer une version anglophone pour le marché UK et DACH",
            ],
            "methodologie": {
                "phase_1": "Mois 1-6 : R&D technique — nouveaux agents IA + intégration API clients",
                "phase_2": "Mois 7-12 : Pilotes commerciaux — 5 clients bêta grands comptes",
                "phase_3": "Mois 13-18 : Déploiement commercial — sales team + marketing B2B",
                "phase_4": "Mois 19-24 : Internationalisation — UK, Pays-Bas, Allemagne",
            },
            "livrables": [
                "Plateforme CaelumSwarm v2.0 avec 75+ agents IA",
                "API publique documentée pour intégration ERP/GRC",
                "Bibliothèque de 1000+ critères CSDDD validés juridiquement",
                "Rapport d'impact : 200 entreprises auditées, 15 000 fournisseurs mappés",
                "Documentation technique et guide utilisateur (FR/EN/NL/DE)",
            ],
            "maturite_technologique": "TRL 7 — Prototype validé en conditions réelles",
            "propriete_intellectuelle": (
                "Architecture multi-agents propriétaire, modèles ML fine-tunés, "
                "base de connaissances CSDDD/ESG — secret d'affaires + dépôt "
                "de logiciel prévu auprès de l'INPI."
            ),
            "differenciateurs": PROJET["differenciateurs"],
        },
    }


def generate_section_impact() -> dict:
    return {
        "titre": "4. IMPACT ATTENDU",
        "contenu": {
            "impact_economique": {
                "emplois_crees_directs": 9,
                "emplois_crees_indirects": 25,
                "ca_prevu_fin_projet": "1 200 000 EUR",
                "roi_investissement": "4,8x sur 3 ans",
                "clients_cibles_fin_projet": 20,
                "marche_adressable": "4 200 000 000 EUR (RegTech EU 2026)",
            },
            "impact_social": {
                "entreprises_conformes_csddd": 200,
                "fournisseurs_analyses": 15000,
                "travailleurs_proteges_indirectement": 500000,
                "secteurs_geographiques": [
                    "Bangladesh (textile)", "RDC (minerais)", "Brésil (agriculture)",
                    "Vietnam (électronique)", "Inde (chimie/pharma)",
                ],
                "domaines_droits_humains_couverts": 17,
            },
            "impact_environnemental": {
                "solution_100_cloud": True,
                "serveurs_green_energy": True,
                "reduction_deplacements_auditeurs": "Réduction estimée de 80% des voyages d'audit",
                "footprint_vs_audit_traditionnel": "CO2 -95% par audit réalisé",
            },
            "impact_ecosysteme": {
                "startups_inspirees": "Modèle reproductible pour LegalTech EU",
                "ecosystem_bruxelles": "Ancrage Bruxelles : hub compliance EU",
                "contribution_politique_eu": (
                    "Data insights partagés avec la Commission pour améliorer l'application CSDDD"
                ),
            },
            "indicateurs_cles": [
                {"kpi": "Nombre d'entreprises clientes", "t0": 2, "t12": 8, "t24": 20},
                {"kpi": "ARR (Annual Recurring Revenue)", "t0": "84k EUR", "t12": "336k EUR", "t24": "840k EUR"},
                {"kpi": "Fournisseurs analysés cumul", "t0": 0, "t12": 2000, "t24": 15000},
                {"kpi": "Agents IA opérationnels", "t0": 52, "t12": 65, "t24": 75},
                {"kpi": "Effectif ETP", "t0": 3, "t12": 7, "t24": 12},
            ],
        },
    }


def generate_section_budget() -> dict:
    budget_total = PROJET["budget_total_projet"]
    return {
        "titre": "5. BUDGET PRÉVISIONNEL DÉTAILLÉ",
        "contenu": {
            "budget_total_eur": budget_total,
            "duree_projet_mois": PROJET["duree_projet_mois"],
            "postes": [
                {
                    "categorie": "Personnel (salaires + charges)",
                    "montant_eur": 420000,
                    "pourcentage": 56,
                    "detail": [
                        "2 ingénieurs IA senior (×2 × 75k EUR/an × 2 ans) : 300 000 EUR",
                        "1 juriste ESG senior (×1 × 70k EUR/an × 2 ans) : 140 000 EUR",
                        "Charges sociales employeur (~35%) incluses",
                    ],
                },
                {
                    "categorie": "Sous-traitance & prestataires",
                    "montant_eur": 120000,
                    "pourcentage": 16,
                    "detail": [
                        "Développement front-end UX/UI : 40 000 EUR",
                        "Audit légal et certification conformité CSDDD : 30 000 EUR",
                        "Traduction multilingue (EN/NL/DE) : 15 000 EUR",
                        "Tests sécurité et pentest ISO 27001 : 35 000 EUR",
                    ],
                },
                {
                    "categorie": "Infrastructure cloud & licences",
                    "montant_eur": 85000,
                    "pourcentage": 11,
                    "detail": [
                        "AWS/Azure (calcul GPU pour modèles IA) : 50 000 EUR",
                        "Licences logicielles (outils ML, monitoring) : 20 000 EUR",
                        "Sécurité et backup données : 15 000 EUR",
                    ],
                },
                {
                    "categorie": "Commercial & marketing B2B",
                    "montant_eur": 60000,
                    "pourcentage": 8,
                    "detail": [
                        "Salons professionnels EU (ESG Congress, Compliance Week) : 20 000 EUR",
                        "Contenu marketing et SEO : 15 000 EUR",
                        "CRM et outreach commercial : 10 000 EUR",
                        "Relations presse et thought leadership : 15 000 EUR",
                    ],
                },
                {
                    "categorie": "Frais généraux & divers",
                    "montant_eur": 65000,
                    "pourcentage": 9,
                    "detail": [
                        "Loyer bureaux Bruxelles (×24 mois) : 36 000 EUR",
                        "Assurances RC Pro + cyber : 12 000 EUR",
                        "Comptabilité et juridique : 10 000 EUR",
                        "Divers et imprévus (5%) : 7 000 EUR",
                    ],
                },
            ],
            "plan_financement": {
                "subvention_demandee": "À préciser selon programme (cible : 50-70% du budget total)",
                "fonds_propres_caelum": "75 000 EUR (10%)",
                "revenus_propres_projet": "150 000 EUR (20% — revenus clients pilotes)",
                "autres_cofinancements": "Autres aides régionales en cours de recherche",
            },
            "note_financiere": (
                "Budget construit sur base des tarifs belges en vigueur (barème CCT). "
                "Toutes les dépenses seront documentées par factures et fiches de paie. "
                "Un compte bancaire dédié au projet sera ouvert pour le suivi."
            ),
        },
    }


def generate_section_calendrier() -> dict:
    return {
        "titre": "6. CALENDRIER D'EXÉCUTION",
        "contenu": {
            "date_debut": PROJET["debut_projet"],
            "date_fin": "2028-08-31",
            "duree_totale": "24 mois",
            "jalons": [
                {
                    "mois": "M1-M2",
                    "livrable": "Kick-off projet, recrutements, setup infrastructure",
                    "indicateur": "2 ingénieurs IA recrutés, environnement tech opérationnel",
                },
                {
                    "mois": "M3-M6",
                    "livrable": "CaelumSwarm v1.5 — 3 nouveaux modules IA développés",
                    "indicateur": "TRL 8, tests unitaires 100% passants",
                },
                {
                    "mois": "M7-M9",
                    "livrable": "Programme pilote — 5 clients bêta grands comptes",
                    "indicateur": "5 contrats pilotes signés, NPS > 40",
                },
                {
                    "mois": "M10-M12",
                    "livrable": "Rapport mi-projet + certification ISO 27001",
                    "indicateur": "Certification obtenue, 8 clients actifs",
                },
                {
                    "mois": "M13-M18",
                    "livrable": "Déploiement commercial EU — 15 clients",
                    "indicateur": "ARR 504k EUR, expansion DACH/NL",
                },
                {
                    "mois": "M19-M24",
                    "livrable": "CaelumSwarm v2.0 — Internationalisation + API publique",
                    "indicateur": "20 clients, ARR 840k EUR, 75+ agents IA",
                },
            ],
            "rapport_avancement": "Rapport trimestriel transmis à l'organisme financeur",
            "audit_mi_parcours": "Audit indépendant prévu à M12",
        },
    }


def generate_section_equipe() -> dict:
    return {
        "titre": "7. ÉQUIPE & COMPÉTENCES",
        "contenu": {
            "equipe_fondatrice": CAELUM_PROFILE["fondateurs"],
            "recrutements_prevus": [
                {
                    "poste": "Ingénieur IA Senior",
                    "profil": "PhD ou 5+ ans ML/NLP, expertise LLM et agents autonomes",
                    "date_recrutement_prevue": "M2",
                    "salaire_brut": "75 000 EUR/an",
                },
                {
                    "poste": "Ingénieur IA Backend",
                    "profil": "Python expert, architectures microservices, APIs",
                    "date_recrutement_prevue": "M2",
                    "salaire_brut": "65 000 EUR/an",
                },
                {
                    "poste": "Juriste ESG Senior",
                    "profil": "Master droit EU + 5 ans compliance/CSDDD/ESG",
                    "date_recrutement_prevue": "M3",
                    "salaire_brut": "70 000 EUR/an",
                },
                {
                    "poste": "Account Executive B2B",
                    "profil": "5+ ans vente SaaS B2B grands comptes en Belgique/EU",
                    "date_recrutement_prevue": "M6",
                    "salaire_brut": "55 000 EUR/an + variable",
                },
                {
                    "poste": "Customer Success Manager",
                    "profil": "Profil ESG + expérience onboarding SaaS enterprise",
                    "date_recrutement_prevue": "M9",
                    "salaire_brut": "50 000 EUR/an",
                },
            ],
            "gouvernance": {
                "conseil_administration": "3 administrateurs fondateurs",
                "advisory_board": "À constituer (cible : expert BNB, ex-DG Justice EU, VP ESG groupe industriel)",
                "comite_scientifique": "Partenariat en cours avec ULB — Faculté de droit",
            },
        },
    }


def generate_section_demande_subvention() -> dict:
    return {
        "titre": "8. DEMANDE DE SUBVENTION",
        "contenu": {
            "montant_demande_indicatif": "375 000 EUR (50% du budget total)",
            "justification_montant": (
                "Le cofinancement demandé représente 50% du budget total du projet "
                "(750 000 EUR). Les fonds propres de Caelum (75k EUR) et les revenus "
                "clients prévisionnels (150k EUR) couvrent le solde. Ce ratio est "
                "conforme aux pratiques des programmes visés (Innoviris: max 70%, "
                "FEDER: max 50%)."
            ),
            "utilisation_subvention": [
                "Personnel technique et juridique : 60%",
                "Infrastructure et outils : 25%",
                "Commercial et marketing : 15%",
            ],
            "impact_sans_financement": (
                "Sans ce financement, Caelum ne pourra pas recruter les compétences "
                "nécessaires ni valider les pilotes commerciaux dans les délais "
                "imposés par le calendrier réglementaire CSDDD (2027). "
                "La croissance serait réduite de 70% et l'expansion européenne "
                "repoussée de 18 mois minimum."
            ),
            "engagement_caelum": [
                "Maintien du siège social à Bruxelles pour la durée du projet",
                "Reporting trimestriel et accès complet aux données pour audit",
                "Maintien de l'emploi créé pendant minimum 3 ans post-projet",
                "Publication d'un rapport d'impact annuel open access",
            ],
            "declarations": {
                "aide_d_etat": "Aucune aide d'État reçue au cours des 3 dernières années",
                "cumul_aides": "Pas d'autre aide sollicitée simultanément pour le même projet",
                "conformite_fiscale": "Situation fiscale régulière — attestation ONSS jointe",
            },
        },
    }


def generate_checklist_pieces() -> list[dict]:
    return [
        {"piece": "Statuts constitutifs de la SPRL (copie certifiée conforme)", "obligatoire": True, "disponible": True},
        {"piece": "Extrait BCE / Banque-Carrefour des Entreprises", "obligatoire": True, "disponible": True},
        {"piece": "Attestation ONSS (cotisations sociales à jour)", "obligatoire": True, "disponible": True},
        {"piece": "Attestation TVA (situation fiscale régulière)", "obligatoire": True, "disponible": True},
        {"piece": "Derniers comptes annuels déposés (exercice 2024-2025)", "obligatoire": True, "disponible": True},
        {"piece": "Plan financier sur 3 ans (bilan, compte de résultats, cash-flow)", "obligatoire": True, "disponible": False, "action": "À préparer avec l'expert-comptable"},
        {"piece": "CV des dirigeants et personnes-clés (max 2 pages chacun)", "obligatoire": True, "disponible": False, "action": "À rédiger et harmoniser"},
        {"piece": "Description technique du projet (max 10 pages)", "obligatoire": True, "disponible": False, "action": "Généré par cet agent — à compléter"},
        {"piece": "Budget détaillé avec justification des postes", "obligatoire": True, "disponible": True},
        {"piece": "Lettre de motivation / note d'intention (max 2 pages)", "obligatoire": True, "disponible": False, "action": "À rédiger"},
        {"piece": "Lettres d'intérêt de clients potentiels (Letter of Intent)", "obligatoire": False, "recommande": True, "disponible": False, "action": "Solliciter 2-3 grands comptes"},
        {"piece": "Accord de partenariat université/centre de recherche", "obligatoire": False, "recommande": True, "disponible": False, "action": "Formaliser accord ULB"},
        {"piece": "Preuves de la propriété intellectuelle (dépôt logiciel)", "obligatoire": False, "recommande": True, "disponible": False, "action": "Déposer auprès INPI.fr ou equivalent belge"},
        {"piece": "Certificat d'assurance RC Professionnelle", "obligatoire": True, "disponible": True},
        {"piece": "Relevé d'identité bancaire (RIB/IBAN) de la société", "obligatoire": True, "disponible": True},
        {"piece": "Attestation de siège social (bail commercial ou domiciliation)", "obligatoire": True, "disponible": True},
        {"piece": "Formulaire de candidature officiel de l'organisme", "obligatoire": True, "disponible": False, "action": "Télécharger sur le site de l'organisme visé"},
    ]


# ─────────────────────────────────────────────
# Génération du fichier Markdown template
# ─────────────────────────────────────────────
MARKDOWN_TEMPLATE = '''# TEMPLATE DOSSIER DE CANDIDATURE — FINANCEMENT BELGE/EUROPÉEN
## Caelum Partners SPRL

---

> **Usage :** Ce template est pré-rempli avec le profil de Caelum Partners.
> Adapter la Section 8 (montant demandé) au programme visé.
> Supprimer les [CHAMPS À COMPLÉTER] avant envoi.

---

## SECTION 1 — IDENTIFICATION DU DEMANDEUR

| Champ | Valeur |
|---|---|
| Raison sociale | Caelum Partners SPRL |
| Forme juridique | SPRL (Société Privée à Responsabilité Limitée) |
| N° BCE / TVA | BE 1234.567.890 |
| Adresse siège | Avenue Louise 000, 1050 Bruxelles |
| Région | Bruxelles-Capitale |
| Date de création | 1er septembre 2024 |
| Code NACE | 6201 — Développement et production de logiciels |
| Site web | https://caelum.partners |
| Email contact | contact@caelum.partners |
| Capital social | 18 500 EUR |
| Effectif actuel | 3 ETP |
| Classification EU | Micro-entreprise (< 10 ETP, CA < 2M EUR) |

---

## SECTION 2 — RÉSUMÉ EXÉCUTIF (max 500 mots)

**Caelum Partners** développe **CaelumSwarm(tm)**, la première plateforme SaaS
d'intelligence artificielle multi-agents dédiée à la conformité avec la directive
européenne **CSDDD (EU 2024/1760)**. Notre solution automatise la due diligence en
droits humains et la cartographie des risques ESG dans les chaînes
d'approvisionnement mondiales.

**Le problème :** La directive CSDDD impose à +50 000 entreprises européennes une
obligation légale de due diligence sur toute leur chaîne d'approvisionnement, avec
des sanctions pouvant atteindre 5% du CA mondial. Aujourd'hui, cette conformité est
réalisée manuellement pour un coût de 200k-500k EUR/an et des délais de plusieurs mois.

**Notre solution :** CaelumSwarm(tm) automatise 90% du processus via 50+ agents IA
spécialisés, réduisant le coût à <35k EUR/an et le délai à 72 heures.

**Le marché :** 4,2 milliards EUR (RegTech EU 2026, croissance 28% p.a.)

**L'impact :** 200 entreprises conformes, 15 000 fournisseurs analysés,
500 000 travailleurs mieux protégés d'ici 2028.

**Le financement demandé :** [MONTANT] EUR pour accélérer le développement
technique et la mise à l'échelle commerciale sur 24 mois.

---

## SECTION 3 — DESCRIPTION DU PROJET

### 3.1 Contexte réglementaire

La directive CSDDD (Corporate Sustainability Due Diligence Directive, EU 2024/1760)
est entrée en vigueur en juillet 2024 avec une transposition progressive jusqu'en 2029.
Elle impose aux entreprises de +250 salariés (puis +1000) d'identifier, prévenir et
remédier aux impacts négatifs sur les droits humains et l'environnement dans leurs
opérations et chaînes de valeur.

**Calendrier d'application :**
- 2027 : Entreprises +5000 salariés et CA mondial +1,5Md EUR
- 2028 : Entreprises +1000 salariés et CA +450M EUR
- 2029 : Entreprises +250 salariés et CA +40M EUR

### 3.2 Description de CaelumSwarm(tm)

CaelumSwarm(tm) est une architecture SaaS B2B composée de 50+ agents IA spécialisés,
organisés en 17 domaines thématiques couvrant l'intégralité des exigences CSDDD :

- Travail des enfants et travail forcé
- Droits syndicaux et libertés fondamentales
- Conditions de travail et sécurité
- Impacts environnementaux (biodiversité, eau, sols)
- Gouvernance et anti-corruption
- Droits des populations autochtones
- ...et 11 autres domaines

**Stack technique :** Python (agents IA) + Next.js (frontend/API) + architecture
cloud EU (RGPD-compliant).

### 3.3 Objectifs du projet financé

1. Développer 3 nouveaux modules IA (supply chain mapping, grievance mechanism,
   corrective action plan generator)
2. Recruter 5 ingénieurs IA + 2 juristes ESG
3. Atteindre 20 clients grands comptes (ARR > 840k EUR)
4. Obtenir la certification ISO 27001 + SOC 2 Type II
5. Lancer une version EN/NL/DE pour les marchés DACH et Pays-Bas

### 3.4 Différenciateurs concurrentiels

- **Seule solution 100% dédiée CSDDD** avec 50+ agents IA spécialisés
- Architecture **multi-agents vs mono-LLM** : précision ×3, coût /2
- **Made in Belgium & EU** — souveraineté des données garantie
- Intégration **17 domaines de droits humains** (OIT, OCDE, ONU Principes Ruggie)
- Onboarding **en 48h**, zéro données sensibles stockées côté client

---

## SECTION 4 — IMPACT ATTENDU

### 4.1 Impact économique

| Indicateur | An 1 | An 2 | An 3 |
|---|---|---|---|
| Clients actifs | 8 | 20 | 45 |
| ARR (EUR) | 336 000 | 840 000 | 1 890 000 |
| Effectif ETP | 7 | 12 | 18 |
| Emplois créés directs | +4 | +5 | +6 |
| Emplois indirects | +10 | +15 | +25 |

### 4.2 Impact social

- **200 entreprises** conformes CSDDD d'ici 2028
- **15 000 fournisseurs** dans 40+ pays analysés
- **500 000 travailleurs** mieux protégés dans les supply chains
- Couverture géographique : Bangladesh, RDC, Brésil, Vietnam, Inde

### 4.3 Impact environnemental

- Réduction de 80% des déplacements d'auditeurs (empreinte carbone /95%)
- Serveurs 100% green energy (fournisseur certifié EU)
- Solution dématérialisée vs audit papier traditionnel

---

## SECTION 5 — BUDGET PRÉVISIONNEL

| Poste | Montant (EUR) | % |
|---|---|---|
| Personnel (salaires + charges) | 420 000 | 56% |
| Sous-traitance et prestataires | 120 000 | 16% |
| Infrastructure cloud et licences | 85 000 | 11% |
| Commercial et marketing B2B | 60 000 | 8% |
| Frais généraux et divers | 65 000 | 9% |
| **TOTAL** | **750 000** | **100%** |

**Plan de financement :**
| Source | Montant | % |
|---|---|---|
| Subvention demandée | [MONTANT] | [X]% |
| Fonds propres Caelum | 75 000 | 10% |
| Revenus clients pilotes | 150 000 | 20% |
| Cofinancement complémentaire | [SOLDE] | [X]% |

---

## SECTION 6 — CALENDRIER

| Période | Jalons | Indicateurs |
|---|---|---|
| M1-M2 | Kick-off, recrutements, setup infra | 2 ingénieurs recrutés |
| M3-M6 | CaelumSwarm v1.5 — 3 nouveaux modules IA | TRL 8, tests 100% |
| M7-M9 | Programme pilote — 5 clients bêta | 5 contrats signés, NPS > 40 |
| M10-M12 | Rapport mi-projet + ISO 27001 | Certification obtenue, 8 clients |
| M13-M18 | Déploiement commercial EU — 15 clients | ARR 504k EUR |
| M19-M24 | CaelumSwarm v2.0 + Internationalisation | 20 clients, ARR 840k EUR |

**Rapport d'avancement :** Trimestriel, transmis à l'organisme financeur.
**Audit mi-parcours :** Prévu à M12 par auditeur indépendant agréé.

---

## SECTION 7 — ÉQUIPE

### Fondateurs

| Nom | Rôle | Expertise |
|---|---|---|
| [Fondateur A] | CEO & Product Lead | 10 ans management & compliance EU |
| [Fondateur B] | CTO & AI Architect | 8 ans IA, architectures distribuées & SaaS B2B |
| [Fondateur C] | Head of Legal & ESG | Juriste EU, CSDDD & droits humains |

### Recrutements prévus dans le cadre du projet

| Poste | Profil | Mois recrutement |
|---|---|---|
| Ingénieur IA Senior | PhD/5+ ans ML, LLM, agents | M2 |
| Ingénieur IA Backend | Python expert, microservices | M2 |
| Juriste ESG Senior | Master droit EU + 5 ans CSDDD | M3 |
| Account Executive B2B | 5+ ans vente SaaS grands comptes EU | M6 |
| Customer Success Manager | Profil ESG + onboarding SaaS enterprise | M9 |

### Gouvernance

- **Conseil d'administration :** 3 administrateurs fondateurs
- **Advisory Board :** À constituer (ex-DG Justice EU, VP ESG groupe industriel, expert BNB)
- **Comité scientifique :** Partenariat en cours avec ULB — Faculté de droit

---

## SECTION 8 — DEMANDE DE SUBVENTION

**Montant demandé :** [MONTANT À COMPLÉTER] EUR

**Taux de subventionnement demandé :** [X]% du budget total

**Justification :** Le cofinancement permettra de couvrir les postes de personnel
et d'infrastructure critiques pour atteindre les jalons du projet dans les délais
imposés par le calendrier CSDDD. Sans ce financement, la croissance serait réduite
de 70% et l'expansion européenne repoussée de 18 mois.

**Engagements de Caelum Partners :**
- Maintien du siège social à Bruxelles pendant toute la durée du projet
- Reporting trimestriel complet avec accès aux données pour contrôle
- Maintien des emplois créés pendant minimum 3 ans post-projet
- Publication d'un rapport d'impact annuel en open access

**Déclarations sur l'honneur :**
- Aucune aide d'État reçue sur les 3 dernières années pour ce projet
- Situation fiscale et sociale régulière (attestations jointes)
- Pas de cumul interdit avec d'autres financements publics

---

## CHECKLIST — PIÈCES JUSTIFICATIVES À JOINDRE

### Obligatoires

- [ ] Statuts constitutifs SPRL (copie certifiée conforme)
- [ ] Extrait BCE (Banque-Carrefour des Entreprises)
- [ ] Attestation ONSS (cotisations sociales à jour)
- [ ] Attestation TVA (situation fiscale régulière)
- [ ] Derniers comptes annuels déposés
- [ ] Plan financier 3 ans (bilan, P&L, cash-flow)
- [ ] CV des dirigeants et personnes-clés (max 2 pages/personne)
- [ ] Description technique du projet (max 10 pages)
- [ ] Budget détaillé avec justification des postes
- [ ] Lettre de motivation / note d'intention (max 2 pages)
- [ ] Formulaire officiel de candidature de l'organisme
- [ ] Certificat d'assurance RC Professionnelle
- [ ] RIB/IBAN de la société
- [ ] Attestation de siège social (bail ou domiciliation)

### Recommandés (non-obligatoires mais valorisés)

- [ ] Lettres d'intérêt (LOI) de 2-3 clients potentiels grands comptes
- [ ] Accord de partenariat avec université ou centre de recherche (ULB/VUB)
- [ ] Preuves de propriété intellectuelle (dépôt logiciel, marque)
- [ ] Références / témoignages de pilotes ou early adopters

---

*Template généré par le Dossier Candidature Agent — Caelum Partners SPRL*
*Version : 1.0.0 | Date : [DATE_GENERATION]*
*Pour toute question : contact@caelum.partners*
'''


# ─────────────────────────────────────────────
# Rapport console
# ─────────────────────────────────────────────
def print_dossier_summary(dossier: dict):
    print("\n" + "=" * 70)
    print("  CAELUM PARTNERS — DOSSIER DE CANDIDATURE GÉNÉRÉ")
    print("  Dossier Candidature Agent")
    print("=" * 70)
    print(f"  Société     : {CAELUM_PROFILE['nom']}")
    print(f"  Projet      : CaelumSwarm(tm)")
    print(f"  Budget total: {PROJET['budget_total_projet']:,}€".replace(",", "."))
    print(f"  Durée       : {PROJET['duree_projet_mois']} mois")
    print(f"  Date analyse: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    print("\n  SECTIONS GÉNÉRÉES :")
    for section in dossier["sections"]:
        print(f"    ✓ {section['titre']}")

    print("\n  CHECKLIST PIÈCES JUSTIFICATIVES :")
    pieces = dossier["checklist_pieces"]
    obligatoires = [p for p in pieces if p.get("obligatoire")]
    disponibles = [p for p in obligatoires if p.get("disponible")]
    a_preparer = [p for p in obligatoires if not p.get("disponible")]

    print(f"    Pièces obligatoires : {len(obligatoires)}")
    print(f"    Déjà disponibles    : {len(disponibles)}")
    print(f"    À préparer          : {len(a_preparer)}")

    if a_preparer:
        print("\n  ACTIONS REQUISES AVANT ENVOI :")
        for p in a_preparer:
            action = p.get("action", "À préparer")
            print(f"    - {p['piece'][:55]:<55} → {action}")

    print(f"\n  FICHIER MARKDOWN GENERE :")
    print(f"    docs/candidatures/template_dossier_financement.md")
    print("=" * 70 + "\n")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    print("[Dossier Candidature Agent] Génération du dossier de candidature...")

    sections = [
        generate_section_identification(),
        generate_section_resume_executif(),
        generate_section_description_projet(),
        generate_section_impact(),
        generate_section_budget(),
        generate_section_calendrier(),
        generate_section_equipe(),
        generate_section_demande_subvention(),
    ]

    checklist = generate_checklist_pieces()

    dossier = {
        "agent": "dossier-candidature-agent",
        "version": "1.0.0",
        "date_generation": datetime.now().isoformat(),
        "societe": CAELUM_PROFILE["nom"],
        "projet": PROJET["nom_complet"],
        "budget_total_eur": PROJET["budget_total_projet"],
        "duree_mois": PROJET["duree_projet_mois"],
        "sections": sections,
        "checklist_pieces": checklist,
        "statistiques": {
            "nb_sections": len(sections),
            "pieces_obligatoires": len([p for p in checklist if p.get("obligatoire")]),
            "pieces_disponibles": len([p for p in checklist if p.get("disponible")]),
            "pieces_a_preparer": len([p for p in checklist if p.get("obligatoire") and not p.get("disponible")]),
            "pieces_recommandees": len([p for p in checklist if p.get("recommande")]),
        },
    }

    print_dossier_summary(dossier)

    # Génération du fichier Markdown
    docs_dir = Path("/home/user/TEST/docs/candidatures")
    docs_dir.mkdir(parents=True, exist_ok=True)

    md_path = docs_dir / "template_dossier_financement.md"
    md_content = MARKDOWN_TEMPLATE.replace(
        "[DATE_GENERATION]", datetime.now().strftime("%Y-%m-%d")
    )
    md_path.write_text(md_content, encoding="utf-8")
    print(f"[Dossier Candidature Agent] Fichier Markdown créé : {md_path}")

    print(json.dumps(dossier, ensure_ascii=False, indent=2))
    return dossier


if __name__ == "__main__":
    main()
