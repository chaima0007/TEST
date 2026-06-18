"""
Agent Comptable Expert - AgentClaude Solutions
Cabinet de niveau Big 4 : comptabilité, fiscalité, optimisation financière.
Plan Comptable Général (PCG) français — TVA — IS — CIR — JEI — SASU/SAS/SARL
"""

import os
import json
from datetime import datetime, timedelta

import google.generativeai as genai

from memoire import charger_memoire, sauvegarder_memoire, incrementer_stat

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "gemini-2.0-flash"
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

ENTREPRISE = {
    "nom": "AgentClaude Solutions",
    "adresse": "12 Rue de l'Innovation, 75008 Paris",
    "siret": "123 456 789 00012",
    "tva_numero": "FR 12 123456789",
    "forme_juridique": "SASU",
    "capital": "10 000 EUR",
    "secteur": "Intelligence Artificielle / Solutions d'agents autonomes",
    "code_naf": "6201Z",  # Programmation informatique
    "exercice_debut": "01/01",
    "exercice_fin": "31/12",
}

DOSSIER_COMPTABILITE = os.path.join(os.getcwd(), "fichiers", "comptabilite")
os.makedirs(DOSSIER_COMPTABILITE, exist_ok=True)

# Taux légaux France 2024-2025
TVA_TAUX_NORMAL = 0.20
TVA_TAUX_INTERMEDIAIRE = 0.10
TVA_TAUX_REDUIT = 0.055
IS_TAUX_NORMAL = 0.25
IS_TAUX_PME = 0.15  # Sur les 42 500 premiers euros
SEUIL_IS_PME = 42_500.0
FRANCHISE_TVA_SEUIL_SERVICE = 36_800.0
FRANCHISE_TVA_SEUIL_MAJOREE = 39_100.0

# ---------------------------------------------------------------------------
# Utilitaires internes
# ---------------------------------------------------------------------------

def _sep(largeur: int = 70, c: str = "=") -> str:
    return c * largeur


def _centrer(texte: str, largeur: int = 70) -> str:
    return texte.center(largeur)


def _horodatage() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _date_fr() -> str:
    return datetime.now().strftime("%d/%m/%Y")


def _mois_fr() -> str:
    mois = [
        "", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
    ]
    return f"{mois[datetime.now().month]} {datetime.now().year}"


def _sauvegarder_rapport(nom_fichier: str, contenu: str) -> str:
    """Sauvegarde un rapport dans fichiers/comptabilite/ et retourne le chemin."""
    chemin = os.path.join(DOSSIER_COMPTABILITE, nom_fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


def _streamer_reponse(prompt: str) -> str:
    """Appelle Gemini en streaming et retourne le texte complet."""
    modele = genai.GenerativeModel(MODEL)
    print()
    texte_complet = ""
    for chunk in modele.generate_content(prompt, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            texte_complet += chunk.text
    print("\n")
    return texte_complet


def _extraire_donnees_financieres_memoire() -> dict:
    """
    Agrège toutes les données financières disponibles en mémoire :
    factures, transactions, clients, projets.
    """
    memoire = charger_memoire()
    factures = memoire.get("factures", [])

    now = datetime.now()
    mois_courant = now.month
    annee_courante = now.year
    mois_precedent = mois_courant - 1 if mois_courant > 1 else 12
    annee_precedente = annee_courante if mois_courant > 1 else annee_courante - 1

    def filtrer_factures(m, a):
        return [
            f for f in factures
            if datetime.fromisoformat(f["date_emission"]).month == m
            and datetime.fromisoformat(f["date_emission"]).year == a
        ]

    fac_mois = filtrer_factures(mois_courant, annee_courante)
    fac_precedent = filtrer_factures(mois_precedent, annee_precedente)

    def somme_ht(liste):
        return sum(f.get("sous_total", f.get("total_ttc", 0) / 1.20) for f in liste)

    def somme_tva(liste):
        return sum(f.get("tva", f.get("total_ttc", 0) - f.get("sous_total", f.get("total_ttc", 0) / 1.20)) for f in liste)

    def somme_ttc(liste):
        return sum(f.get("total_ttc", 0) for f in liste)

    ca_ht_mois = somme_ht(fac_mois)
    ca_tva_mois = somme_tva(fac_mois)
    ca_ttc_mois = somme_ttc(fac_mois)
    ca_ht_precedent = somme_ht(fac_precedent)
    ca_ttc_precedent = somme_ttc(fac_precedent)
    ca_ht_annuel = somme_ht(factures)

    nb_clients_actifs = len({f["client"]["nom"] for f in fac_mois})
    nb_factures_impayees = sum(
        1 for f in factures
        if not f.get("payee")
        and datetime.fromisoformat(f["date_echeance"]) < now
    )
    montant_impaye = sum(
        f.get("total_ttc", 0) for f in factures
        if not f.get("payee")
    )

    transactions = memoire.get("transactions_comptables", [])

    return {
        "ca_ht_mois": ca_ht_mois,
        "ca_tva_mois": ca_tva_mois,
        "ca_ttc_mois": ca_ttc_mois,
        "ca_ht_precedent": ca_ht_precedent,
        "ca_ttc_precedent": ca_ttc_precedent,
        "ca_ht_annuel": ca_ht_annuel,
        "nb_factures_mois": len(fac_mois),
        "nb_clients_actifs": nb_clients_actifs,
        "nb_factures_impayees": nb_factures_impayees,
        "montant_impaye": montant_impaye,
        "total_factures": len(factures),
        "factures": factures,
        "transactions": transactions,
        "mois_libelle": _mois_fr(),
        "mois_courant": mois_courant,
        "annee_courante": annee_courante,
    }


# ---------------------------------------------------------------------------
# 1. Agent Comptabilité — Saisie & Journalisation
# ---------------------------------------------------------------------------

def agent_comptabilite(transactions_texte: str) -> str:
    """
    Enregistre et catégorise des transactions, génère les écritures journal,
    attribue les comptes PCG, identifie les charges déductibles, signale les
    éléments inhabituels.

    Args:
        transactions_texte: Description libre des transactions à comptabiliser
                            (ex: "Achat serveur GPU 8 500 EUR HT, abonnement
                             OpenAI 1 200 EUR HT, honoraires consultant 3 000 EUR HT")
    """
    incrementer_stat("agent_comptabilite")

    print(f"\n{'=' * 70}")
    print(_centrer("AGENT COMPTABILITÉ — SAISIE & JOURNALISATION"))
    print(_centrer("Plan Comptable Général (PCG) — Référentiel Big 4"))
    print(f"{'=' * 70}")
    print(f"\n  Analyse des transactions en cours...\n")

    prompt = f"""Tu es un expert-comptable de niveau Big 4 (Cabinet type Deloitte, PWC, KPMG ou EY),
spécialisé dans les entreprises tech et IA françaises.
Tu travailles pour {ENTREPRISE['nom']} ({ENTREPRISE['forme_juridique']}, SIRET : {ENTREPRISE['siret']}).
Secteur : {ENTREPRISE['secteur']}, Code NAF : {ENTREPRISE['code_naf']}.

## TRANSACTIONS À COMPTABILISER

{transactions_texte}

## TRAVAIL DEMANDÉ

Effectue une comptabilisation experte et complète selon les normes françaises :

### 1. ÉCRITURES AU JOURNAL (format PCG)
Pour chaque transaction, génère l'écriture de journal avec :
- Date de l'opération
- N° de compte PCG à 3 chiffres minimum (débit et crédit)
- Libellé du compte exact
- Montant HT, TVA (20% sauf exception), TTC
- Libellé de l'écriture
- Pièce justificative recommandée

Format tableau :
| Date | Compte | Libellé compte | Débit | Crédit | Libellé écriture |

### 2. CATÉGORISATION & ANALYSE

Pour chaque transaction :
- **Catégorie** : Charge d'exploitation / Investissement / Charge financière / Produit
- **Nature** : Personnel / Technologie & Licences / Marketing / R&D / Administratif / Sous-traitance
- **Déductibilité IS** : Totalement déductible / Partiellement / Non déductible (avec justification)
- **TVA déductible** : Oui / Non / Partiellement (préciser régime)
- **Compte de résultat** : Ligne exacte du compte de résultat

### 3. COMPTES PCG UTILISÉS

Liste récapitulative des comptes mobilisés :
- Classe 2 (Immobilisations) → amortissement sur X ans selon règles fiscales
- Classe 6 (Charges) → sous-comptes détaillés
- Classe 4 (Tiers) → fournisseurs, TVA
- Classe 5 (Trésorerie)

### 4. CHARGES DÉDUCTIBLES — OPTIMISATION FISCALE

Identifie toutes les charges déductibles avec :
- Montant HT déductible
- Base légale (CGI, BOFiP)
- Conditions de déductibilité à respecter
- Opportunités CIR (Crédit Impôt Recherche) pour les dépenses R&D/IA
- Amortissements accélérés éventuels (matériel informatique : 3 ans)

### 5. POINTS D'ATTENTION & SIGNALEMENTS

Signale tout élément inhabituel ou à risque :
- Transactions sans justificatif apparent
- Montants hors norme pour le secteur
- Risques de requalification fiscale
- Obligations documentaires spécifiques
- Délais légaux à respecter (déclarations, paiements)

### 6. RÉCAPITULATIF COMPTABLE

Tableau de synthèse :
- Total charges HT / Total TVA déductible / Total TTC
- Impact sur résultat net estimé
- Économie d'IS générée (taux 25% ou 15% PME si bénéfice < 42 500 EUR)
- Recommandations de classification

Sois précis, rigoureux, et cite les articles du Code Général des Impôts (CGI)
et du Plan Comptable Général (PCG 2014) pour chaque décision comptable.
Date du traitement : {_date_fr()}
"""

    reponse = _streamer_reponse(prompt)

    # Sauvegarder en mémoire
    memoire = charger_memoire()
    if "transactions_comptables" not in memoire:
        memoire["transactions_comptables"] = []
    memoire["transactions_comptables"].append({
        "date": datetime.now().isoformat(),
        "description": transactions_texte[:300],
        "analyse": reponse[:500],
    })
    sauvegarder_memoire(memoire)

    # Sauvegarder le rapport
    nom_fichier = f"journal_comptable_{_horodatage()}.txt"
    contenu = f"JOURNAL COMPTABLE — {ENTREPRISE['nom']}\n"
    contenu += f"Date : {_date_fr()}\n\n"
    contenu += f"TRANSACTIONS ANALYSÉES :\n{transactions_texte}\n\n"
    contenu += "ANALYSE COMPTABLE :\n" + reponse
    chemin = _sauvegarder_rapport(nom_fichier, contenu)
    print(f"  Rapport sauvegardé : {chemin}\n")

    return reponse


# ---------------------------------------------------------------------------
# 2. Agent Bilan Mensuel — Compte de Résultat Complet
# ---------------------------------------------------------------------------

def agent_bilan_mensuel() -> str:
    """
    Génère un compte de résultat mensuel complet à partir des données en mémoire :
    revenus par ligne de service, charges détaillées, EBITDA, résultat net,
    comparaison mois précédent, cash flow prévisionnel 3 mois.
    """
    incrementer_stat("agent_bilan_mensuel")

    print(f"\n{'=' * 70}")
    print(_centrer("AGENT BILAN MENSUEL — COMPTE DE RÉSULTAT"))
    print(_centrer("Analyse P&L complète — Niveau Direction Financière"))
    print(f"{'=' * 70}")
    print("\n  Consolidation des données financières...\n")

    donnees = _extraire_donnees_financieres_memoire()

    # Estimer les charges typiques d'une startup IA (si pas de données réelles)
    charges_estimees = {
        "personnel": donnees["ca_ht_mois"] * 0.35 if donnees["ca_ht_mois"] > 0 else 15_000,
        "technologie": donnees["ca_ht_mois"] * 0.12 if donnees["ca_ht_mois"] > 0 else 3_500,
        "marketing": donnees["ca_ht_mois"] * 0.08 if donnees["ca_ht_mois"] > 0 else 2_000,
        "administratif": donnees["ca_ht_mois"] * 0.05 if donnees["ca_ht_mois"] > 0 else 1_500,
        "rd": donnees["ca_ht_mois"] * 0.10 if donnees["ca_ht_mois"] > 0 else 4_000,
        "sous_traitance": donnees["ca_ht_mois"] * 0.08 if donnees["ca_ht_mois"] > 0 else 2_500,
    }
    total_charges = sum(charges_estimees.values())
    ebitda = donnees["ca_ht_mois"] - total_charges
    amortissements = donnees["ca_ht_mois"] * 0.03
    ebit = ebitda - amortissements
    charges_financieres = 200.0
    resultat_avant_is = ebit - charges_financieres
    is_estime = max(0, min(resultat_avant_is * IS_TAUX_PME, SEUIL_IS_PME * IS_TAUX_PME)) + max(0, (resultat_avant_is - SEUIL_IS_PME) * IS_TAUX_NORMAL)
    resultat_net = resultat_avant_is - is_estime

    variation_ca = ((donnees["ca_ht_mois"] - donnees["ca_ht_precedent"]) / donnees["ca_ht_precedent"] * 100) if donnees["ca_ht_precedent"] > 0 else 0

    contexte_financier = f"""
DONNÉES FINANCIÈRES — {ENTREPRISE['nom']} ({ENTREPRISE['forme_juridique']})
Période analysée : {donnees['mois_libelle']}

═══════════════════════════════════════
REVENUS (Chiffre d'Affaires)
═══════════════════════════════════════
CA HT mois courant          : {donnees['ca_ht_mois']:>12,.2f} EUR
CA HT mois précédent        : {donnees['ca_ht_precedent']:>12,.2f} EUR
Variation mensuelle         : {variation_ca:>+11.1f} %
CA HT annuel cumulé         : {donnees['ca_ht_annuel']:>12,.2f} EUR
TVA collectée mois          : {donnees['ca_tva_mois']:>12,.2f} EUR
Nombre de factures émises   : {donnees['nb_factures_mois']:>12}
Clients actifs ce mois      : {donnees['nb_clients_actifs']:>12}

═══════════════════════════════════════
CHARGES D'EXPLOITATION (estimées)
═══════════════════════════════════════
Charges de personnel (35%)  : {charges_estimees['personnel']:>12,.2f} EUR
Technologie & Licences (12%): {charges_estimees['technologie']:>12,.2f} EUR
R&D / Innovation (10%)      : {charges_estimees['rd']:>12,.2f} EUR
Marketing & Comm. (8%)      : {charges_estimees['marketing']:>12,.2f} EUR
Sous-traitance (8%)         : {charges_estimees['sous_traitance']:>12,.2f} EUR
Frais généraux admin (5%)   : {charges_estimees['administratif']:>12,.2f} EUR
TOTAL CHARGES               : {total_charges:>12,.2f} EUR

═══════════════════════════════════════
INDICATEURS DE RENTABILITÉ
═══════════════════════════════════════
EBITDA                      : {ebitda:>12,.2f} EUR ({(ebitda/donnees['ca_ht_mois']*100 if donnees['ca_ht_mois'] > 0 else 0):.1f}%)
Dotations amortissements    : {amortissements:>12,.2f} EUR
EBIT (Résultat opérationnel): {ebit:>12,.2f} EUR
Charges financières         : {charges_financieres:>12,.2f} EUR
Résultat avant IS           : {resultat_avant_is:>12,.2f} EUR
IS estimé                   : {is_estime:>12,.2f} EUR
RÉSULTAT NET                : {resultat_net:>12,.2f} EUR

═══════════════════════════════════════
CRÉANCES & TRÉSORERIE
═══════════════════════════════════════
Créances clients impayées   : {donnees['montant_impaye']:>12,.2f} EUR
Factures en retard          : {donnees['nb_factures_impayees']:>12}
Total factures émises       : {donnees['total_factures']:>12}

═══════════════════════════════════════
TRANSACTIONS COMPTABILISÉES EN MÉMOIRE
═══════════════════════════════════════
Nombre d'entrées            : {len(donnees['transactions'])}
"""

    prompt = f"""Tu es Directeur Financier et associé comptable de niveau Big 4 chez {ENTREPRISE['nom']}.
Secteur : {ENTREPRISE['secteur']}.

Sur la base des données consolidées ci-dessous, génère un rapport mensuel de gestion
complet, digne d'une présentation au Conseil d'Administration ou aux actionnaires :

{contexte_financier}

## STRUCTURE DU RAPPORT MENSUEL DE GESTION

### EXECUTIVE SUMMARY (5 lignes max)
Synthèse des performances clés du mois, signal fort positif/négatif, décision à prendre.

### 1. ANALYSE DES REVENUS PAR LIGNE DE SERVICE
- Décomposition du CA par nature de prestation (si données disponibles) :
  * Développement d'agents IA sur-mesure
  * Licences & SaaS récurrents (MRR)
  * Conseil & Formation IA
  * Support & Maintenance
- Analyse de la qualité du revenu (récurrent vs ponctuel)
- Mix produit/service et évolution
- Clients concentrés vs diversifiés (risque de concentration)

### 2. COMPTE DE RÉSULTAT DÉTAILLÉ (format CRC 99-02)
Tableau P&L structuré :
```
                                    N          N-1      Var. %
─────────────────────────────────────────────────────────────
Chiffre d'affaires net
Autres produits d'exploitation
─────────────────────────────────────────────────────────────
TOTAL PRODUITS D'EXPLOITATION
─────────────────────────────────────────────────────────────
Achats consommés
Services extérieurs
Charges de personnel
Impôts et taxes
Dotations aux amortissements
Autres charges
─────────────────────────────────────────────────────────────
TOTAL CHARGES D'EXPLOITATION
─────────────────────────────────────────────────────────────
RÉSULTAT D'EXPLOITATION (EBIT)
Résultat financier
─────────────────────────────────────────────────────────────
RÉSULTAT COURANT AVANT IS
Impôt sur les sociétés
─────────────────────────────────────────────────────────────
RÉSULTAT NET
```

### 3. ANALYSE EBITDA & MARGES
- EBITDA absolu et taux de marge EBITDA
- Marge brute et analyse du coût de revient
- Marge opérationnelle nette
- Comparaison avec benchmarks secteur Tech/IA (EBITDA cible : 20-35% pour SaaS)
- Leviers d'amélioration identifiés

### 4. COMPARAISON MOIS PRÉCÉDENT & TENDANCES
- Analyse des écarts en valeur absolue et en pourcentage
- Explication des variations significatives (>10%)
- Tendance des 3 derniers mois
- Saisonnalité éventuelle

### 5. CASH FLOW PRÉVISIONNEL 3 MOIS
Tableau :
```
                        M+1          M+2          M+3
─────────────────────────────────────────────────────
Encaissements prévus
Décaissements prévus
Solde net mensuel
Trésorerie cumulée
```
Hypothèses retenues et facteurs de risque sur le cash.

### 6. RATIOS FINANCIERS CLÉS
- Ratio de liquidité générale (doit être > 1,5)
- Days Sales Outstanding (DSO) — délai moyen de paiement clients
- Taux de recouvrement des créances
- Burn rate (si période pré-rentabilité)
- Runway de trésorerie estimé (en mois)

### 7. POINTS D'ATTENTION & RISQUES
- Créances douteuses à provisionner (CGI art. 39-1)
- Risques de trésorerie court terme
- Obligations comptables et fiscales du mois prochain
- Conformité URSSAF, TVA, IS

### 8. RECOMMANDATIONS DIRECTION FINANCIÈRE (3-5 actions)
Actions concrètes, priorisées, avec responsable et délai.

Date du rapport : {_date_fr()}
Utilise des tableaux formatés, sois analytique et précis. Niveau expertise Big 4.
"""

    reponse = _streamer_reponse(prompt)

    nom_fichier = f"bilan_mensuel_{datetime.now().strftime('%Y_%m')}.txt"
    contenu = f"BILAN MENSUEL — {ENTREPRISE['nom']}\n"
    contenu += f"Période : {donnees['mois_libelle']}\n"
    contenu += f"Généré le : {_date_fr()}\n\n"
    contenu += contexte_financier + "\n\nANALYSE EXPERTE :\n" + reponse
    chemin = _sauvegarder_rapport(nom_fichier, contenu)
    print(f"  Rapport sauvegardé : {chemin}\n")

    return reponse


# ---------------------------------------------------------------------------
# 3. Agent TVA — Déclaration & Optimisation
# ---------------------------------------------------------------------------

def agent_tva(periode: str = "") -> str:
    """
    Gestion complète de la TVA : calcul collectée/déductible, synthèse CA3,
    rappels d'échéances, conseil régime, optimisation.

    Args:
        periode: Période concernée (ex: "Janvier 2025", "T1 2025", "2025")
                 Par défaut : mois courant
    """
    incrementer_stat("agent_tva")

    if not periode:
        periode = _mois_fr()

    print(f"\n{'=' * 70}")
    print(_centrer("AGENT TVA — GESTION & DÉCLARATION"))
    print(_centrer(f"Période : {periode}"))
    print(f"{'=' * 70}")
    print("\n  Calcul de la TVA en cours...\n")

    donnees = _extraire_donnees_financieres_memoire()

    tva_collectee = donnees["ca_tva_mois"]
    tva_deductible_estimee = tva_collectee * 0.35  # estimation charges
    tva_due = max(0, tva_collectee - tva_deductible_estimee)
    ca_ht_annuel = donnees["ca_ht_annuel"]

    # Détermination régime TVA
    if ca_ht_annuel < FRANCHISE_TVA_SEUIL_SERVICE:
        regime_actuel = "Franchise en base de TVA (art. 293 B CGI)"
        regime_conseille = "Franchise en base — attention au dépassement de seuil"
    elif ca_ht_annuel < 254_000:
        regime_actuel = "Régime simplifié d'imposition (RSI) — déclaration annuelle CA12"
        regime_conseille = "RSI adapté — envisager réel normal si TVA déductible importante"
    else:
        regime_actuel = "Régime réel normal — déclaration mensuelle CA3"
        regime_conseille = "Réel normal obligatoire — optimiser les remboursements de crédit TVA"

    # Dates d'échéance TVA 2025
    now = datetime.now()
    mois = now.month
    prochain_mois = (mois % 12) + 1
    annee_prochaine = now.year if prochain_mois > 1 else now.year + 1
    echeance_ca3 = datetime(annee_prochaine if prochain_mois < mois else now.year, prochain_mois, 19)

    contexte_tva = f"""
DONNÉES TVA — {ENTREPRISE['nom']}
Période analysée : {periode}
N° TVA intracommunautaire : {ENTREPRISE['tva_numero']}

CA HT période              : {donnees['ca_ht_mois']:>12,.2f} EUR
CA TTC période             : {donnees['ca_ttc_mois']:>12,.2f} EUR
CA HT annuel cumulé        : {ca_ht_annuel:>12,.2f} EUR

TVA COLLECTÉE (taux 20%)   : {tva_collectee:>12,.2f} EUR
TVA DÉDUCTIBLE (estimée)   : {tva_deductible_estimee:>12,.2f} EUR
TVA NETTE DUE              : {tva_due:>12,.2f} EUR

Régime TVA actuel          : {regime_actuel}
Seuil franchise services   : {FRANCHISE_TVA_SEUIL_SERVICE:>12,.2f} EUR
Prochaine échéance CA3     : {echeance_ca3.strftime('%d/%m/%Y')}
"""

    prompt = f"""Tu es un spécialiste de la fiscalité indirecte française (TVA), de niveau Big 4.
Tu gères la TVA de {ENTREPRISE['nom']} ({ENTREPRISE['forme_juridique']}, NAF {ENTREPRISE['code_naf']}).
Secteur : {ENTREPRISE['secteur']}.

{contexte_tva}

## TRAVAIL DEMANDÉ : ANALYSE TVA EXPERTE

### 1. CALCUL DÉTAILLÉ TVA COLLECTÉE vs DÉDUCTIBLE

**TVA Collectée :**
- CA France (taux 20% standard)
- Prestations intracommunautaires (régime autoliquidation)
- Exportations hors UE (exonérées — art. 262 CGI)
- Opérations à taux réduit éventuelles (10% ou 5,5%)

**TVA Déductible :**
Pour chaque catégorie de charge, précise :
- Technologie & Cloud (API, SaaS, hébergement) → TVA 20% déductible
- Matériel informatique → TVA 20% déductible
- Sous-traitance → TVA 20% déductible
- Déplacements : règles spécifiques (carburant 80%, restaurants 50%, véhicules 0%)
- Formation → TVA déductible sous conditions
- Charges exclues du droit à déduction

**Tableau de liquidation TVA :**
```
                           Base HT        Taux      TVA
─────────────────────────────────────────────────────────
COLLECTÉE
Ventes France                                20%
Acquisitions intrac.                         20%
─────────────────────────────────────────────────────────
TOTAL TVA COLLECTÉE
─────────────────────────────────────────────────────────
DÉDUCTIBLE
Achats & services                            20%
Immobilisations                              20%
─────────────────────────────────────────────────────────
TOTAL TVA DÉDUCTIBLE
─────────────────────────────────────────────────────────
TVA NETTE DUE (ou crédit)
```

### 2. SYNTHÈSE DÉCLARATION CA3

Remplis les cases principales de la déclaration CA3 :
- Case CA : Chiffre d'affaires imposable
- Case 08 : Bases imposables à 20%
- Case 09 : Bases imposables à 10%
- Case 10 : Bases imposables à 5,5%
- Case 16 : TVA à 20% (collectée)
- Case 19 : Total TVA collectée
- Case 20 : TVA déductible sur immobilisations
- Case 21 : TVA déductible sur autres biens et services
- Case 23 : Total TVA déductible
- Case 25/26 : TVA à payer / Crédit de TVA

Ajoute les annexes éventuelles (DEB pour opérations intracommunautaires > 460 000 EUR).

### 3. CALENDRIER DES OBLIGATIONS TVA

Rappels d'échéances :
- CA3 mensuelle : 19 du mois suivant (régime réel normal)
- CA12 annuelle : mai N+1 (régime simplifié)
- Acomptes semestriels : juillet et décembre (RSI)
- DEB (déclaration échanges de biens) : 10e jour ouvrable du mois suivant
- Échanges de services intracommunautaires : DES
- Pénalités de retard : 10% + intérêts 0,20%/mois (art. 1728 CGI)

Prochaines échéances pour {periode} :
{echeance_ca3.strftime('%d/%m/%Y')} — Dépôt CA3 et paiement TVA

### 4. ANALYSE DU RÉGIME TVA

Situation actuelle : {regime_actuel}

Analyse comparative des régimes :
| Critère              | Franchise    | RSI           | Réel Normal   |
|─────────────────────|─────────────|──────────────|──────────────|
| Seuil CA services    | < 36 800 €   | < 254 000 €   | > 254 000 €   |
| Déclarations         | Aucune       | Annuelle CA12 | Mensuelle CA3 |
| TVA déductible       | Non          | Oui           | Oui           |
| Avantage prix        | +20% marché  | Standard      | Standard      |
| Crédit TVA           | Non          | Remb. annuel  | Remb. mensuel |

Recommandation pour {ENTREPRISE['nom']} avec CA annuel {ca_ht_annuel:,.0f} EUR :
{regime_conseille}

### 5. OPTIMISATIONS TVA

Conseils d'optimisation légaux :
1. Timing des déclarations (décaler encaissements/décaissements)
2. Option pour le débitement (TVA exigible à l'encaissement vs facturation)
3. Remboursement de crédit TVA (droit au remboursement si crédit > 760 EUR)
4. TVA intracommunautaire : numéros de TVA clients à valider (VIES)
5. Autoliquidation pour les achats de services à des prestataires étrangers
6. Régularisations annuelles pro rata
7. Assujettissement partiel si activités mixtes

### 6. POINTS DE VIGILANCE

Risques et contrôles fiscaux sur la TVA :
- Conformité des factures (mentions obligatoires art. 242 nonies A CGI)
- Justificatifs de déductibilité
- Opérations intracommunautaires et autoliquidation
- Délai de prescription de 3 ans (art. L176 LPF)

Date d'analyse : {_date_fr()}
Cite les articles du CGI, BOFiP et réponses ministérielles pertinents.
"""

    reponse = _streamer_reponse(prompt)

    nom_fichier = f"tva_{periode.replace(' ', '_').replace('/', '-')}_{_horodatage()}.txt"
    contenu = f"ANALYSE TVA — {ENTREPRISE['nom']}\n"
    contenu += f"Période : {periode} | Généré le : {_date_fr()}\n\n"
    contenu += contexte_tva + "\n\nANALYSE EXPERTE :\n" + reponse
    chemin = _sauvegarder_rapport(nom_fichier, contenu)
    print(f"  Rapport sauvegardé : {chemin}\n")

    return reponse


# ---------------------------------------------------------------------------
# 4. Agent Optimisation Fiscale
# ---------------------------------------------------------------------------

def agent_optimisation_fiscale(
    revenus_annuels: float,
    charges: float,
    statut_juridique: str = "SASU",
) -> str:
    """
    Optimisation fiscale complète pour une entreprise d'IA française :
    forme juridique, rémunération, charges maximales, CIR, JEI, amortissements.

    Args:
        revenus_annuels: CA HT annuel en euros
        charges: Total des charges annuelles en euros
        statut_juridique: Forme actuelle (SASU/SAS/SARL/auto-entrepreneur/EI)
    """
    incrementer_stat("agent_optimisation_fiscale")

    benefice_brut = revenus_annuels - charges
    is_base = max(0, benefice_brut)
    is_estime_standard = (
        min(is_base, SEUIL_IS_PME) * IS_TAUX_PME +
        max(0, is_base - SEUIL_IS_PME) * IS_TAUX_NORMAL
    )

    print(f"\n{'=' * 70}")
    print(_centrer("AGENT OPTIMISATION FISCALE"))
    print(_centrer(f"Revenus : {revenus_annuels:,.0f} EUR | Statut : {statut_juridique}"))
    print(f"{'=' * 70}")
    print("\n  Analyse fiscale en cours...\n")

    prompt = f"""Tu es un avocat fiscaliste et expert-comptable associé de niveau Big 4,
spécialisé dans l'optimisation fiscale des entreprises tech et IA françaises.
Client : {ENTREPRISE['nom']} — Secteur : {ENTREPRISE['secteur']} — Code NAF : {ENTREPRISE['code_naf']}

## DONNÉES FINANCIÈRES

Revenus annuels (CA HT)     : {revenus_annuels:>12,.2f} EUR
Total charges annuelles     : {charges:>12,.2f} EUR
Bénéfice avant optimisation : {benefice_brut:>12,.2f} EUR
IS estimé sans optimisation : {is_estime_standard:>12,.2f} EUR (PME 15% + 25%)
Statut juridique actuel     : {statut_juridique}
Date d'analyse              : {_date_fr()}

## ANALYSE D'OPTIMISATION FISCALE EXPERTE

### 1. AUDIT DU STATUT JURIDIQUE — TABLEAU COMPARATIF

Analyse comparative exhaustive pour une entreprise IA avec {revenus_annuels:,.0f} EUR de CA :

| Critère                    | Auto-Ent.  | EI/EIRL    | SARL        | SAS/SASU    |
|────────────────────────────|────────────|────────────|─────────────|─────────────|
| Plafond CA                 | 77 700 €   | Illimité   | Illimité    | Illimité    |
| Impôt sur revenu/IS        | IR versem. | IR ou IS   | IS 15%/25%  | IS 15%/25%  |
| Cotisations sociales       | 22% CA     | 45% rev.   | 43% sal.    | 43% sal.    |
| Déductibilité charges      | Limitée    | Totale     | Totale      | Totale      |
| Dividendes possibles       | Non        | Non        | Oui (17,2%) | Oui (17,2%) |
| Crédibilité investisseurs  | Faible     | Faible     | Bonne       | Excellente  |
| CIR / JEI accessible       | Non        | Partiel    | Oui         | Oui         |
| Flexibilité capital        | Nulle      | Faible     | Limitée     | Totale      |

**Recommandation optimale** pour ce profil de revenus et le secteur IA :
[Analyse détaillée avec justification fiscale et sociale]

### 2. OPTIMISATION SALAIRE vs DIVIDENDES (si IS)

Simulation pour le dirigeant propriétaire unique :

**Scénario A — Salaire uniquement :**
- Salaire brut annuel recommandé : [montant optimisé]
- Cotisations patronales (~42%) : [montant]
- Cotisations salariales (~22%) : [montant]
- Salaire net imposable : [montant]
- IR estimé (tranches 2025) : [montant]
- Coût total entreprise : [montant]

**Scénario B — Mix Salaire + Dividendes :**
- Salaire brut plancher (sécurité sociale) : 36 000 EUR recommandé
- Dividendes distribués : [montant disponible]
- PFU dividendes 30% (12,8% IR + 17,2% PS) ou barème progressif
- Économie vs salaire pur : [montant]

**Scénario C — Optimisation Maximale :**
- Salaire optimisé (déductible IS) : [montant]
- Intéressement / Participation (déductible IS + exonération IR partiellement)
- Plan d'épargne entreprise (PEE) — abondement déductible
- Contrat Madelin (retraite, prévoyance) — déductible revenus BIC
- Dividendes optimisés
- Comparatif net-net pour le dirigeant

**Tableau comparatif net reçu vs coût entreprise :**
```
                    Salaire pur  Mix optimal  Dividendes max
─────────────────────────────────────────────────────────────
Coût entreprise
IS payé
Net dirigeant
Taux d'efficacité
```

### 3. MAXIMISATION DES CHARGES DÉDUCTIBLES

Charges déductibles légales à maximiser (art. 39 CGI) :

**Charges opérationnelles :**
- Frais de déplacement et réception (règles 2025)
- Téléphone, abonnements, matériel informatique
- Formation professionnelle (CPF, plan de formation)
- Loyer bureau / cotisation domiciliation
- Assurances professionnelles (RC Pro, perte d'exploitation)

**Charges dirigeant en société :**
- Véhicule de société (TCO vs IK)
- Mutuelle collective (loi Madelin)
- Prévoyance dirigeant (loi Madelin)
- Retraite supplémentaire : Madelin ou PER Entreprise
- Frais professionnels forfaitaires ou réels

**Immobilisations et amortissements :**
- Matériel informatique : amortissement linéaire 3 ans (33,33%/an)
- Logiciels : amortissement 12 mois (100% l'année d'acquisition)
- Brevets, propriété intellectuelle : 5 ans
- Amortissement accéléré pour matériel de R&D
- Suramortissement éventuel (dispositif exceptionnel)

**Charges financières :**
- Intérêts d'emprunt (dans les limites ATAD)
- Intérêts comptes courants associés (taux 2025 : 5,67%)

### 4. CRÉDIT IMPÔT RECHERCHE (CIR) — OPPORTUNITÉ MAJEURE POUR L'IA

**Eligibilité {ENTREPRISE['nom']} :** TRÈS PROBABLE (secteur IA — recherche fondamentale et appliquée)

**Critères d'éligibilité (art. 244 quater B CGI) :**
- Travaux de recherche fondamentale, appliquée ou développement expérimental
- Caractère incertain du résultat technique
- Documentation obligatoire (cahiers de laboratoire, livrables)
- Activité exercée en France ou UE/EEE

**Dépenses éligibles au CIR :**
- Personnel chercheurs et techniciens : 100% (+ 50% forfaitaire de frais)
- Dotations amortissements équipements R&D : 100%
- Sous-traitance à organismes agréés : 100%
- Frais de brevet et de défense de brevet : 100%
- Veille technologique : 50% (plafond 60 000 EUR)
- Cloud et calcul scientifique (GPU pour entraînement IA) : à analyser

**Calcul CIR :**
- Taux : 30% des dépenses éligibles jusqu'à 100 M EUR
- Assiette éligible estimée : [à calculer selon détail des charges R&D]
- CIR estimé : [assiette × 30%]
- Remboursement immédiat si PME (Bpifrance)

**Procédure :**
1. Identifier et documenter les projets R&D (critères OCDE Frascati)
2. Préparer le dossier technique (obligatoire si CIR > 100 000 EUR)
3. Déposer le formulaire 2069-A avec la liasse fiscale
4. Option : rescrit fiscal préventif (réponse DRFIP en 6 mois)

**IMPORTANT — Risques à anticiper :**
- Contrôle fiscal renforcé sur le CIR (vérification technique par experts MESRI)
- Documentation rigoureuse indispensable
- Distinction développement expérimental vs amélioration courante

### 5. JEUNE ENTREPRISE INNOVANTE (JEI) — STATUT À ANALYSER

**Critères JEI (art. 44 sexies-0 A CGI) :**
- PME < 8 ans d'existence ✓ (à vérifier)
- Dépenses R&D ≥ 15% des charges déductibles totales (hors CIR)
- Moins de 250 salariés ✓
- Capital détenu à 50%+ par personnes physiques (ou associations, FIP, FCPI)

**Avantages JEI :**
- Exonération IS : 100% année 1-3, 50% années 4-7
- Exonération cotisations sociales patronales sur salaires chercheurs (plafond SMIC × 5)
- Exonération CFE et CVAE (sur délibération communes)
- Exonération IFI pour parts détenues par investisseurs

**Simulation économie JEI :**
- Économie IS estimée (si bénéficiaire) : [calcul]
- Économie charges sociales chercheurs : [calcul]
- Total gain JEI : [montant]

**Procédure :**
- Rescrit JEI auprès de la DRFIP recommandé
- Déclaration 2069-RCI pour les avantages JEI/JEU

### 6. AUTRES DISPOSITIFS FISCAUX FAVORABLES

**BIC & Amortissements :**
- Provisions pour risques et charges (art. 39-1-5° CGI)
- Report déficitaire en avant (illimité) ou en arrière (carry-back 1 an, plafonné 1 M EUR)
- Régime de neutralité des apports et fusions

**Crédits d'impôt complémentaires :**
- CII (Crédit Impôt Innovation) : 30% des dépenses innovation jusqu'à 400 000 EUR (hors JEI)
- CIF (Crédit Impôt Formation dirigeant)
- Crédit d'impôt apprentissage

**Dispositifs d'exonération territoriale :**
- Zone France Relance / France 2030 (si applicable)
- QFZ (Quartier Prioritaire) — exonérations IS et taxes locales

### 7. PLAN D'OPTIMISATION FISCALE — FEUILLE DE ROUTE

**Actions immédiates (0-3 mois) :**
[Liste priorisée avec économie estimée et base légale]

**Actions court terme (3-12 mois) :**
[Restructuration, statut JEI, dossier CIR]

**Actions moyen terme (1-3 ans) :**
[Optimisation patrimoine, holding, pacte d'associés]

### 8. SYNTHÈSE — ÉCONOMIES FISCALES RÉALISABLES

```
Dispositif               Base éligible    Taux    Économie estimée
──────────────────────────────────────────────────────────────────
CIR                                        30%
JEI — IS                                  100%/50%
JEI — Charges sociales                    100%
Charges optimisées (IS)                   15-25%
Dividendes vs salaires
──────────────────────────────────────────────────────────────────
TOTAL ÉCONOMIES ANNUELLES POTENTIELLES
IS sans optimisation       {is_estime_standard:,.2f} EUR
IS après optimisation      [à calculer]
GAIN FISCAL NET            [montant]
```

**AVERTISSEMENT LÉGAL :** Toutes les recommandations s'inscrivent dans le cadre de
l'optimisation fiscale légale. La fraude fiscale est illégale et sanctionnée pénalement.
Recommande de valider les stratégies majeures avec un avocat fiscaliste inscrit au barreau.

Cite systématiquement les articles CGI, BOFiP, et jurisprudences pertinentes.
"""

    reponse = _streamer_reponse(prompt)

    nom_fichier = f"optimisation_fiscale_{datetime.now().year}_{_horodatage()}.txt"
    contenu = f"OPTIMISATION FISCALE — {ENTREPRISE['nom']}\n"
    contenu += f"Revenus : {revenus_annuels:,.2f} EUR | Charges : {charges:,.2f} EUR | Statut : {statut_juridique}\n"
    contenu += f"Généré le : {_date_fr()}\n\nANALYSE EXPERTE :\n" + reponse
    chemin = _sauvegarder_rapport(nom_fichier, contenu)
    print(f"  Rapport sauvegardé : {chemin}\n")

    return reponse


# ---------------------------------------------------------------------------
# 5. Agent Budget Prévisionnel
# ---------------------------------------------------------------------------

def agent_budget_previsionnel(horizon_mois: int = 12, objectif_ca: float = 0.0) -> str:
    """
    Construit un budget prévisionnel détaillé avec scénarios et analyse de risque.

    Args:
        horizon_mois: Durée de la prévision en mois (6, 12, 24, 36)
        objectif_ca: Objectif de CA HT sur la période (0 = calculé automatiquement)
    """
    incrementer_stat("agent_budget_previsionnel")

    donnees = _extraire_donnees_financieres_memoire()
    ca_actuel_mensuel = donnees["ca_ht_mois"]

    if objectif_ca <= 0:
        # Objectif calculé : +30% de croissance annuelle
        objectif_ca = ca_actuel_mensuel * horizon_mois * 1.30

    ca_mensuel_cible = objectif_ca / horizon_mois

    print(f"\n{'=' * 70}")
    print(_centrer("AGENT BUDGET PRÉVISIONNEL"))
    print(_centrer(f"Horizon : {horizon_mois} mois | Objectif CA : {objectif_ca:,.0f} EUR"))
    print(f"{'=' * 70}")
    print("\n  Modélisation budgétaire en cours...\n")

    prompt = f"""Tu es Directeur Financier et associé senior d'un cabinet Big 4,
expert en modélisation financière et planification stratégique pour les startups IA.
Client : {ENTREPRISE['nom']} ({ENTREPRISE['forme_juridique']})
Secteur : {ENTREPRISE['secteur']}

## PARAMÈTRES DE LA MODÉLISATION

Horizon de prévision        : {horizon_mois} mois
CA mensuel actuel           : {ca_actuel_mensuel:>12,.2f} EUR HT
Objectif CA total période   : {objectif_ca:>12,.2f} EUR HT
CA mensuel cible (moyen)    : {ca_mensuel_cible:>12,.2f} EUR HT
Croissance implicite        : {((ca_mensuel_cible/ca_actuel_mensuel - 1)*100 if ca_actuel_mensuel > 0 else 0):.1f}%
Date de départ              : {_date_fr()}

## BUDGET PRÉVISIONNEL EXPERT — {horizon_mois} MOIS

### 1. MODÈLE DE REVENUS PAR LIGNE DE SERVICE

Décompose l'objectif CA par ligne de revenus typique pour une société IA :

| Ligne de service                    | M+1   | M+6   | M+12  | % mix  |
|─────────────────────────────────────|───────|───────|───────|────────|
| Développement agents IA sur-mesure  |       |       |       |        |
| Licences SaaS (MRR récurrent)       |       |       |       |        |
| Conseil & Audit IA                  |       |       |       |        |
| Formation & Workshops               |       |       |       |        |
| Support & Maintenance               |       |       |       |        |
| **TOTAL CA HT**                     |       |       |       | 100%   |

Hypothèses de croissance par ligne et justification marché.

### 2. STRUCTURE DES CHARGES PRÉVISIONNELLES

**Charges fixes mensuelles :**
| Poste                               | Mensuel   | Annuel    | % CA    |
|─────────────────────────────────────|───────────|───────────|─────────|
| Dirigeant (salaire chargé)          |           |           |         |
| Développeurs / Data Scientists      |           |           |         |
| Commercial / Business Dev           |           |           |         |
| Loyer / Domiciliation               |           |           |         |
| Assurances professionnelles         |           |           |         |
| Abonnements Cloud & API             |           |           |         |
| Comptable / Juridique               |           |           |         |
| **TOTAL CHARGES FIXES**             |           |           |         |

**Charges variables (% du CA) :**
| Poste                               | % CA      | M+1       | M+{horizon_mois}  |
|─────────────────────────────────────|───────────|───────────|───────|
| Sous-traitance technique            | 8-12%     |           |       |
| Frais de vente / Commission         | 3-5%      |           |       |
| Marketing & Acquisition             | 5-10%     |           |       |
| Formation & R&D                     | 8-15%     |           |       |
| Frais divers                        | 2-3%      |           |       |
| **TOTAL CHARGES VARIABLES**         |           |           |       |

### 3. COMPTE DE RÉSULTAT PRÉVISIONNEL — MENSUEL

Tableau P&L sur {horizon_mois} mois (format condensé) :
```
Mois              M+1    M+2    M+3    M+4    M+5    M+6    M+12
──────────────────────────────────────────────────────────────────
CA HT
Charges fixes
Charges variables
──────────────────────────────────────────────────────────────────
Marge brute
% marge brute
──────────────────────────────────────────────────────────────────
EBITDA
% EBITDA
Amortissements
EBIT
IS estimé
──────────────────────────────────────────────────────────────────
RÉSULTAT NET
```

### 4. ANALYSE DU POINT MORT (BREAK-EVEN)

**Calcul du seuil de rentabilité :**
- Charges fixes totales mensuelles : [F]
- Taux de marge sur coûts variables : [m = (CA - CV) / CA]
- Point mort = F / m

**Tableau break-even :**
- CA seuil de rentabilité mensuel : [montant]
- Nombre de clients nécessaires (panier moyen estimé) : [nombre]
- Mois d'atteinte du break-even : [mois]
- Marge de sécurité au mois {horizon_mois} : [%]

Graphique textuel de convergence vers le break-even (ASCII) :
```
CA
│                          ╱ CA total
│                   ╱─────
│              ╱───╱ Charges totales
│    ╱────────╱
│───╱ Charges fixes
├─────────────────────────── Mois
  M1  M3  M6  M9  M12
  BREAK-EVEN = M?
```

### 5. SCÉNARIOS — ANALYSE DE SENSIBILITÉ

**Hypothèses de base :**
- Croissance CA : [taux de base]%/mois
- Taux de marge brute : [%]
- Délai de paiement clients : 45 jours

```
                    PESSIMISTE   RÉALISTE    OPTIMISTE
────────────────────────────────────────────────────────
Croissance mensuelle   -5%         Base        +15%
CA total période
Charges totales
EBITDA cumulé
Résultat net cumulé
Cash final
Runway (mois)
────────────────────────────────────────────────────────
Probabilité estimée    20%         60%         20%
```

**Analyse de sensibilité :**
Impact sur le résultat net si :
- CA -10% : résultat = [montant] (impact = [%])
- Charges +10% : résultat = [montant] (impact = [%])
- Délai paiement +30j : besoin BFR supplémentaire = [montant]

### 6. PLAN DE TRÉSORERIE (CASH FLOW) — {horizon_mois} MOIS

```
                M+1   M+2   M+3   M+4   M+5   M+6  ...  M+{horizon_mois}
──────────────────────────────────────────────────────────────────────
ENCAISSEMENTS
Règlements clients
Autres produits
──────────────────────────────────────────────────────────────────────
DÉCAISSEMENTS
Charges de personnel
Fournisseurs
Loyers & charges
TVA nette
IS (si trimestriel)
Investissements
──────────────────────────────────────────────────────────────────────
FLUX NET MENSUEL
TRÉSORERIE CUMULÉE
```

**Besoin en Fonds de Roulement (BFR) :**
- BFR = Créances clients + Stocks - Dettes fournisseurs
- DSO estimé : 45 jours → immobilisation = CA mensuel × 1,5

**Cash Runway :**
- Trésorerie de départ estimée : [montant]
- Burn rate mensuel (si déficitaire) : [montant]
- Runway : [nombre de mois avant 0 EUR]

### 7. BESOINS EN FINANCEMENT

Si le budget révèle un besoin de financement :
- Montant du gap de trésorerie maximum : [montant]
- Mois de pic du besoin : [mois]

**Options de financement adaptées à une startup IA :**
| Source                          | Montant     | Coût     | Délai    | Conditions   |
|─────────────────────────────────|─────────────|──────────|──────────|──────────────|
| Bpifrance — Prêt Numérique      | 50-200 K€   | Taux fixe| 3-6 mois | 3 ans d'exist.|
| Bpifrance — PGE Rebond          | 10-100 K€   | 2-3%     | 2-3 mois | PME           |
| Love money / Business Angels    | 50-500 K€   | Capital  | 1-6 mois | Pitch requis  |
| CIR remboursé (Bpifrance)       | = CIR droit | 0%       | 1-2 mois | PME < 7 ans   |
| Prêt d'honneur Réseau Entreprendre| 15-50 K€  | 0%       | 2-4 mois | Projet innov. |
| Levée de fonds Seed             | 500K-2M€    | Capital  | 6-12 mois| KPIs solides  |

### 8. INDICATEURS DE PILOTAGE (KPIs Budget)

KPIs à suivre mensuellement :
- CA réel vs budget (écart toléré : ±10%)
- Taux de marge brute (seuil d'alerte : <50%)
- EBITDA réel vs budget
- DSO (seuil d'alerte : >60 jours)
- Cash disponible vs projection
- Taux d'atteinte objectifs commerciaux

### 9. RISQUES BUDGÉTAIRES & MITIGATIONS

| Risque                         | Impact | Probabilité | Mitigation recommandée       |
|────────────────────────────────|────────|─────────────|──────────────────────────---|
| Retard signature contrats      | Fort   | Moyen       | Pipeline diversifié, MRR++  |
| Dépassement charges personnel  | Moyen  | Moyen       | Recrutements échelonnés     |
| Défaut client majeur           | Fort   | Faible      | Assurance-crédit, diversif. |
| Évolution réglementaire IA     | Moyen  | Moyen       | Veille juridique, RGPD      |
| Concurrence sur les prix       | Moyen  | Fort        | Différenciation, ValeurAjoutée|

Sois précis dans les chiffres, utilise des hypothèses réalistes pour le secteur IA français 2025.
Benchmark : croissance SaaS B2B ~3-7%/mois en phase early, marge brute cible 65-75%.
"""

    reponse = _streamer_reponse(prompt)

    nom_fichier = f"budget_previsionnel_{horizon_mois}mois_{_horodatage()}.txt"
    contenu = f"BUDGET PRÉVISIONNEL — {ENTREPRISE['nom']}\n"
    contenu += f"Horizon : {horizon_mois} mois | Objectif CA : {objectif_ca:,.2f} EUR\n"
    contenu += f"Généré le : {_date_fr()}\n\nMODÉLISATION EXPERTE :\n" + reponse
    chemin = _sauvegarder_rapport(nom_fichier, contenu)
    print(f"  Rapport sauvegardé : {chemin}\n")

    return reponse


# ---------------------------------------------------------------------------
# 6. Agent Rapport Investisseur
# ---------------------------------------------------------------------------

def agent_rapport_investisseur() -> str:
    """
    Génère un rapport financier investment-grade : métriques SaaS/VC,
    états financiers résumés, unit economics, trajectoire de croissance,
    utilisation des fonds.
    """
    incrementer_stat("agent_rapport_investisseur")

    print(f"\n{'=' * 70}")
    print(_centrer("AGENT RAPPORT INVESTISSEUR"))
    print(_centrer("Investment-Grade Financial Report — VC/BA Ready"))
    print(f"{'=' * 70}")
    print("\n  Préparation du dossier investisseur...\n")

    donnees = _extraire_donnees_financieres_memoire()

    # Calculs métriques investisseur
    mrr = donnees["ca_ht_mois"]  # Monthly Recurring Revenue (approx)
    arr = mrr * 12               # Annual Recurring Revenue
    burn_rate = max(0, mrr * 0.60 - mrr)  # estimé si déficit (placeholder)
    cacuistomers = donnees["nb_clients_actifs"]
    cac_estime = mrr * 0.15 / max(cacuistomers, 1) * 12  # 15% du CA en marketing / clients acquis
    panier_moyen = mrr / max(cacuistomers, 1)
    churn_estime = 0.03  # 3%/mois estimé startup B2B IA
    ltv_estime = panier_moyen / churn_estime

    prompt = f"""Tu es associé d'un fonds de Capital Risque et conseiller M&A,
spécialisé dans les startups IA européennes (portefeuille type Partech, Kima Ventures, BpiFrance).
Tu rédiges le rapport financier trimestriel de {ENTREPRISE['nom']}
pour présentation à des investisseurs VC, Business Angels et Bpifrance.

## DONNÉES DISPONIBLES

Société                     : {ENTREPRISE['nom']} ({ENTREPRISE['forme_juridique']})
Secteur                     : {ENTREPRISE['secteur']}
SIRET                       : {ENTREPRISE['siret']}
Période du rapport          : {donnees['mois_libelle']}
Date de rédaction           : {_date_fr()}

MÉTRIQUES FINANCIÈRES BRUTES :
MRR (approx.)               : {mrr:>12,.2f} EUR
ARR (projeté)               : {arr:>12,.2f} EUR
CA HT mois précédent        : {donnees['ca_ht_precedent']:>12,.2f} EUR
CA HT annuel cumulé         : {donnees['ca_ht_annuel']:>12,.2f} EUR
Clients actifs ce mois      : {cacuistomers:>12}
Factures en cours           : {donnees['nb_factures_mois']:>12}
Créances impayées           : {donnees['montant_impaye']:>12,.2f} EUR
Panier moyen estimé         : {panier_moyen:>12,.2f} EUR/mois
CAC estimé                  : {cac_estime:>12,.2f} EUR
LTV estimé (1/churn 3%)     : {ltv_estime:>12,.2f} EUR
Ratio LTV/CAC               : {(ltv_estime/cac_estime if cac_estime > 0 else 0):>12.1f}x

## RAPPORT FINANCIER INVESTISSEUR — FORMAT VC STANDARD

### 1. EXECUTIVE SUMMARY — THE PITCH IN NUMBERS

Une page de synthèse investment-grade avec :
- Headline metric : ARR de {arr:,.0f} EUR
- Momentum : croissance MoM et annualisée
- Positionnement marché (TAM/SAM/SOM — marché IA agents autonomes)
- Thèse d'investissement en 3 points
- Besoins de financement et utilisation des fonds
- Valorisation indicative (multiple ARR : 5-15x selon croissance)

### 2. MÉTRIQUES SAAS & UNIT ECONOMICS

**Tableau de bord VC (benchmark secteur inclus) :**

| Métrique            | Valeur actuelle  | Benchmark IA SaaS | Statut    |
|─────────────────────|──────────────────|────────────────────|───────────|
| MRR                 | {mrr:,.0f} EUR   | Variable          |           |
| ARR                 | {arr:,.0f} EUR   | Variable          |           |
| Croissance MRR MoM  | [%]              | 5-15%             |           |
| Gross Margin        | [%]              | 65-80%            |           |
| Net Revenue Retention (NRR) | [%]   | >100%             |           |
| Gross Churn         | {churn_estime*100:.1f}%/mois | <3%   |           |
| CAC                 | {cac_estime:,.0f} EUR | Variable     |           |
| LTV                 | {ltv_estime:,.0f} EUR | Variable     |           |
| LTV/CAC ratio       | {(ltv_estime/cac_estime if cac_estime > 0 else 0):.1f}x | >3x |  |
| CAC Payback period  | [mois]           | <18 mois          |           |
| Burn Rate           | [EUR/mois]       | Variable          |           |
| Runway              | [mois]           | >18 mois          |           |
| ARR/FTE             | [EUR]            | >100 K€           |           |

**Analyse de la rétention (Cohort Analysis) :**
- Retention J30 / J60 / J90
- Expansion Revenue (upsell, cross-sell)
- Net Revenue Retention = Gross Retention + Expansion
- Magic Number (efficacité commerciale) = Net New ARR / S&M Spend

### 3. ÉTATS FINANCIERS RÉSUMÉS

**Compte de Résultat Consolidé (format IFRS simplifié) :**
```
                                M-3        M-2        M-1        M
───────────────────────────────────────────────────────────────────
Revenue
Cost of Revenue (COGS)
──────────────────────────────────────────────────────────────────
Gross Profit
Gross Margin %
──────────────────────────────────────────────────────────────────
R&D Expenses
Sales & Marketing
General & Administrative
──────────────────────────────────────────────────────────────────
EBITDA
EBITDA Margin %
D&A
EBIT
──────────────────────────────────────────────────────────────────
Net Income / (Loss)
```

**Bilan simplifié :**
```
ACTIF                          PASSIF
──────────────────────────────  ──────────────────────────────
Trésorerie & équivalents        Capital social
Créances clients                Réserves
Immobilisations nettes          Résultat de l'exercice
Autres actifs                   Dettes financières
                                Dettes fournisseurs
──────────────────────────────  ──────────────────────────────
TOTAL ACTIF                     TOTAL PASSIF
```

**Cash Flow Statement (méthode indirecte) :**
```
Résultat net
+ Amortissements
+/- Variation BFR
= Cash flow opérationnel
───────────────────────────────
Investissements (CAPEX)
= Cash flow investissement
───────────────────────────────
Apports en capital
Emprunts nets
= Cash flow financement
───────────────────────────────
VARIATION DE TRÉSORERIE
Trésorerie début de période
TRÉSORERIE FIN DE PÉRIODE
```

### 4. TRAJECTOIRE DE CROISSANCE & PROJECTIONS

**Modèle de croissance — 3 scénarios investisseur :**

```
                    Base (60%)    Bull (25%)   Bear (15%)
────────────────────────────────────────────────────────────
ARR Year 1
ARR Year 2
ARR Year 3
Croissance Y2/Y1
Croissance Y3/Y2
EBITDA margin Y3
Multiple ARR visé
Valorisation Y3
```

**Jalons de croissance :**
- Prochain milestone : ARR [montant] → [date]
- Break-even opérationnel : [date]
- Series A readiness : [conditions]

**Courbe de croissance S-curve IA :**
Positionner {ENTREPRISE['nom']} sur la courbe de maturité du marché IA agents autonomes 2025-2028.

### 5. ANALYSE DU MARCHÉ & POSITIONNEMENT

**TAM / SAM / SOM :**
- TAM (Marché Total Adressable) : Marché mondial agents IA autonomes → X Mds EUR 2027
- SAM (Marché Adressable Serviceable) : PME françaises + Europe francophone → Y M EUR
- SOM (Marché Obtenu Cible) : Part de marché réaliste à 3 ans → Z M EUR
- Part de marché actuelle : [%]

**Avantages compétitifs durables (moat) :**
1. Propriété intellectuelle (agents IA propriétaires)
2. Effets réseau et données d'entraînement
3. Switching costs élevés (intégration profonde)
4. Marques et réputation
5. Partenariats stratégiques

**Paysage concurrentiel :**
Tableau comparatif : {ENTREPRISE['nom']} vs concurrents directs/indirects.

### 6. UTILISATION DES FONDS

Pour un tour de table cible de [X] EUR :
```
Poste d'utilisation              Montant     % du tour  Période
────────────────────────────────────────────────────────────────
Recrutement Tech & IA
Recrutement Commercial (AE/SDR)
R&D & Infrastructure Cloud
Marketing & Brand Building
Fonds de roulement
Frais légaux & due diligence
────────────────────────────────────────────────────────────────
TOTAL                            100%
```

**Milestones post-financement :**
- M+6 : [KPI cible]
- M+12 : [KPI cible]
- M+18 : [readiness Series A]

### 7. ÉQUIPE & GOUVERNANCE

Structure actuelle et besoins en recrutement clés.
Gouvernance : Conseil d'Administration, pacte d'associés, BSA/BSPCE prévus.

### 8. FACTEURS DE RISQUE (vision franche VC)

Principaux risques et mitigations honnêtes :
1. Risque marché (adoption IA) — probabilité / impact
2. Risque technologique (LLM dependencies, OpenAI/Anthropic/Google)
3. Risque réglementaire (AI Act européen 2025-2027)
4. Risque de concentration clients
5. Risque de recrutement tech (guerre des talents IA)

### 9. TERMES D'INVESTISSEMENT SUGGÉRÉS (Term Sheet indicatif)

Pour un tour seed ou pré-seed :
- Valorisation pre-money : [X × ARR — justification multiple]
- Montant recherché : [Y EUR]
- Dilution : [Z%]
- Instruments : BSPCE, obligations convertibles, actions de préférence
- Droits investisseurs standards : liquidation preference 1x, anti-dilution, information rights

### 10. CONCLUSION — WHY NOW, WHY US

Message de conviction pour clôturer le rapport (1 page max, ton VC-pitch).

---
Utilise le benchmark SaaS 2024-2025 (SaaStr, Bessemer Venture Partners Cloud Index,
France Digitale Annual Barometer). Sois ambitieux mais crédible — les VC repèrent
immédiatement les projections fantaisistes.
"""

    reponse = _streamer_reponse(prompt)

    nom_fichier = f"rapport_investisseur_{_horodatage()}.txt"
    contenu = f"RAPPORT INVESTISSEUR — {ENTREPRISE['nom']}\n"
    contenu += f"Période : {donnees['mois_libelle']} | Généré le : {_date_fr()}\n"
    contenu += f"MRR : {mrr:,.2f} EUR | ARR : {arr:,.2f} EUR | Clients : {cacuistomers}\n\n"
    contenu += "RAPPORT INVESTMENT-GRADE :\n" + reponse
    chemin = _sauvegarder_rapport(nom_fichier, contenu)
    print(f"  Rapport sauvegardé : {chemin}\n")

    return reponse


# ---------------------------------------------------------------------------
# Menu principal
# ---------------------------------------------------------------------------

def _afficher_menu() -> None:
    largeur = 70
    print(f"\n{'=' * largeur}")
    print(_centrer("AGENT COMPTABLE EXPERT — AgentClaude Solutions", largeur))
    print(_centrer("Niveau Cabinet Big 4 | PCG | TVA | IS | CIR | JEI", largeur))
    print(f"{'=' * largeur}")
    print("  1. Comptabilisation & Journal (PCG — écritures)")
    print("  2. Bilan Mensuel (P&L complet — EBITDA — Cash Flow)")
    print("  3. TVA (CA3 — régime — optimisation)")
    print("  4. Optimisation Fiscale (IS — CIR — JEI — statut juridique)")
    print("  5. Budget Prévisionnel (scénarios — break-even — cash runway)")
    print("  6. Rapport Investisseur (ARR — LTV/CAC — term sheet)")
    print("  0. Quitter")
    print(f"{'=' * largeur}")


def main() -> None:
    print("\n  Démarrage de l'Agent Comptable Expert...")
    print(f"  Cabinet virtuel Big 4 — {ENTREPRISE['nom']}")
    print(f"  Répertoire comptabilité : {DOSSIER_COMPTABILITE}\n")

    while True:
        _afficher_menu()
        choix = input("  Votre choix : ").strip()

        if choix == "1":
            print("\n  Saisissez les transactions à comptabiliser")
            print("  (Ex: 'Achat serveur GPU 8 500 EUR HT, abonnement OpenAI 1 200 EUR HT')")
            print("  (Terminez avec une ligne vide)\n")
            lignes = []
            while True:
                ligne = input("  > ")
                if not ligne:
                    break
                lignes.append(ligne)
            if lignes:
                agent_comptabilite("\n".join(lignes))
            else:
                print("  Aucune transaction saisie.")

        elif choix == "2":
            agent_bilan_mensuel()

        elif choix == "3":
            periode = input("\n  Période TVA (ex: 'Janvier 2025', 'T1 2025' — Entrée pour mois courant) : ").strip()
            agent_tva(periode)

        elif choix == "4":
            print("\n  --- Optimisation Fiscale ---")
            try:
                revenus = float(input("  Revenus annuels HT (EUR) : ").strip().replace(" ", "").replace(",", "."))
                charges = float(input("  Charges annuelles totales (EUR) : ").strip().replace(" ", "").replace(",", "."))
                print("  Statut juridique actuel : 1=SASU  2=SAS  3=SARL  4=Auto-entrepreneur  5=EI")
                choix_statut = input("  Votre statut (1-5) : ").strip()
                statuts = {"1": "SASU", "2": "SAS", "3": "SARL", "4": "Auto-entrepreneur", "5": "EI"}
                statut = statuts.get(choix_statut, "SASU")
                agent_optimisation_fiscale(revenus, charges, statut)
            except ValueError:
                print("  Valeur invalide. Veuillez entrer des nombres.")

        elif choix == "5":
            print("\n  --- Budget Prévisionnel ---")
            try:
                horizon_str = input("  Horizon en mois (6/12/24/36, défaut=12) : ").strip()
                horizon = int(horizon_str) if horizon_str else 12
                objectif_str = input("  Objectif CA HT total sur la période (0 = auto) : ").strip().replace(" ", "").replace(",", ".")
                objectif = float(objectif_str) if objectif_str else 0.0
                agent_budget_previsionnel(horizon, objectif)
            except ValueError:
                print("  Valeur invalide.")

        elif choix == "6":
            agent_rapport_investisseur()

        elif choix == "0":
            print("\n  Au revoir ! Agent Comptable Expert arrêté.\n")
            break

        else:
            print("\n  Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
