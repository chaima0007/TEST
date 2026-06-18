"""
Agent de Facturation Automatique - AgentClaude Solutions
Gestion intelligente des factures, relances et rapports financiers.
"""

import os
import json
from datetime import datetime, timedelta
import google.generativeai as genai

from memoire import ajouter_interaction, charger_memoire, sauvegarder_memoire, incrementer_stat

# Configuration
MODEL = "gemini-2.0-flash"
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

ENTREPRISE = {
    "nom": "AgentClaude Solutions",
    "adresse": "12 Rue de l'Innovation, 75008 Paris",
    "siret": "123 456 789 00012",
    "tva": "FR 12 123456789",
    "email": "contact@agentclaude.fr",
    "telephone": "+33 1 23 45 67 89",
    "iban": "FR76 XXXX XXXX XXXX XXXX XXXX XXX",
    "bic": "AGRIFRPP",
}

TVA_TAUX = 0.21
DELAI_PAIEMENT = 30  # jours


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def _prochain_numero_facture(memoire: dict) -> str:
    """Génère un numéro de facture unique au format FACT-YYYY-NNN."""
    annee = datetime.now().year
    factures = memoire.get("factures", [])
    factures_annee = [f for f in factures if f.get("numero", "").startswith(f"FACT-{annee}-")]
    numero = len(factures_annee) + 1
    return f"FACT-{annee}-{numero:03d}"


def _ligne_separateur(largeur: int = 60, caractere: str = "-") -> str:
    return caractere * largeur


def _centrer(texte: str, largeur: int = 60) -> str:
    return texte.center(largeur)


def _statut_facture(facture: dict) -> str:
    """Détermine le statut affiché d'une facture."""
    if facture.get("payee"):
        return "PAYEE"
    date_echeance_str = facture.get("date_echeance")
    if date_echeance_str:
        date_echeance = datetime.fromisoformat(date_echeance_str)
        if datetime.now() > date_echeance:
            return "EN RETARD"
    return "EN ATTENTE"


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


# ---------------------------------------------------------------------------
# 1. Génération de facture
# ---------------------------------------------------------------------------

def generer_facture(client: dict, services: list[dict], montant: float) -> dict:
    """
    Génère une facture professionnelle et la sauvegarde.

    Args:
        client: dict avec clés 'nom', 'adresse', 'email', 'siret' (optionnel)
        services: liste de dicts {'description': str, 'quantite': int, 'prix_unitaire': float}
        montant: montant HT total (utilisé si services vide)
    """
    memoire = charger_memoire()

    numero = _prochain_numero_facture(memoire)
    date_emission = datetime.now()
    date_echeance = date_emission + timedelta(days=DELAI_PAIEMENT)

    # Calcul des montants
    if services:
        sous_total = sum(s["quantite"] * s["prix_unitaire"] for s in services)
    else:
        sous_total = montant

    tva_montant = sous_total * TVA_TAUX
    total_ttc = sous_total + tva_montant

    # Génération du fichier texte de la facture
    largeur = 65
    sep = _ligne_separateur(largeur, "=")
    sep_fin = _ligne_separateur(largeur, "-")

    lignes = [
        sep,
        _centrer("FACTURE", largeur),
        _centrer(ENTREPRISE["nom"].upper(), largeur),
        sep,
        "",
        f"  {ENTREPRISE['adresse']}",
        f"  SIRET : {ENTREPRISE['siret']}  |  TVA : {ENTREPRISE['tva']}",
        f"  Tel   : {ENTREPRISE['telephone']}  |  Email : {ENTREPRISE['email']}",
        "",
        sep_fin,
        f"  Numero de facture : {numero}",
        f"  Date d'emission   : {date_emission.strftime('%d/%m/%Y')}",
        f"  Date d'echeance   : {date_echeance.strftime('%d/%m/%Y')}",
        sep_fin,
        "",
        "  FACTURER A :",
        f"  {client['nom']}",
        f"  {client.get('adresse', 'Adresse non renseignee')}",
        f"  Email : {client.get('email', '-')}",
    ]

    if client.get("siret"):
        lignes.append(f"  SIRET : {client['siret']}")

    lignes += [
        "",
        sep_fin,
        f"  {'DESCRIPTION':<35} {'QTE':>5} {'P.U. HT':>10} {'TOTAL HT':>10}",
        sep_fin,
    ]

    if services:
        for s in services:
            total_ligne = s["quantite"] * s["prix_unitaire"]
            desc = s["description"][:35]
            lignes.append(
                f"  {desc:<35} {s['quantite']:>5} {s['prix_unitaire']:>10.2f} {total_ligne:>10.2f}"
            )
    else:
        lignes.append(
            f"  {'Prestation AgentClaude Solutions':<35} {'1':>5} {sous_total:>10.2f} {sous_total:>10.2f}"
        )

    lignes += [
        "",
        sep_fin,
        f"  {'Sous-total HT':<50} {sous_total:>10.2f} EUR",
        f"  {'TVA (21%)':<50} {tva_montant:>10.2f} EUR",
        _ligne_separateur(largeur, "="),
        f"  {'TOTAL TTC':<50} {total_ttc:>10.2f} EUR",
        _ligne_separateur(largeur, "="),
        "",
        "  CONDITIONS DE PAIEMENT :",
        f"  Reglement sous {DELAI_PAIEMENT} jours a compter de la date d'emission.",
        f"  Virement bancaire uniquement.",
        "",
        f"  IBAN : {ENTREPRISE['iban']}",
        f"  BIC  : {ENTREPRISE['bic']}",
        "",
        "  Merci de mentionner le numero de facture lors du virement.",
        "",
        sep_fin,
        "  En cas de retard de paiement, des penalites de 3x le taux",
        "  legal seront appliquees (Art. L441-10 du Code de Commerce).",
        sep_fin,
        "",
        _centrer(f"Facture generee le {date_emission.strftime('%d/%m/%Y a %H:%M')}", largeur),
        sep,
    ]

    contenu_facture = "\n".join(lignes)

    # Sauvegarde dans un fichier .txt
    nom_fichier = f"facture_{numero}.txt"
    chemin_fichier = os.path.join(os.getcwd(), nom_fichier)
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        f.write(contenu_facture)

    # Sauvegarde en memoire
    facture_data = {
        "numero": numero,
        "date_emission": date_emission.isoformat(),
        "date_echeance": date_echeance.isoformat(),
        "client": client,
        "services": services,
        "sous_total": sous_total,
        "tva": tva_montant,
        "total_ttc": total_ttc,
        "payee": False,
        "fichier": chemin_fichier,
    }

    if "factures" not in memoire:
        memoire["factures"] = []
    memoire["factures"].append(facture_data)
    sauvegarder_memoire(memoire)

    ajouter_interaction(
        "systeme",
        f"Facture {numero} generee pour {client['nom']} - Montant TTC : {total_ttc:.2f} EUR"
    )
    incrementer_stat("factures_generees")

    print(contenu_facture)
    print(f"\n  Facture sauvegardee : {chemin_fichier}")

    return facture_data


# ---------------------------------------------------------------------------
# 2. Relance de paiement
# ---------------------------------------------------------------------------

def agent_relance_paiement(client: dict | str, facture_num: str, jours_retard: int) -> str:
    """
    Genere un email de relance professionnel adapte au nombre de jours de retard.

    Args:
        client: dict avec 'nom' et 'email', ou chaine de caracteres (nom du client)
        facture_num: numero de facture (ex: FACT-2025-001)
        jours_retard: nombre de jours de retard de paiement
    """
    if isinstance(client, str):
        client_nom = client
        client_email = "non renseigne"
    else:
        client_nom = client.get("nom", "Client")
        client_email = client.get("email", "non renseigne")

    # Recuperation du montant depuis la memoire
    memoire = charger_memoire()
    factures = memoire.get("factures", [])
    facture = next((f for f in factures if f["numero"] == facture_num), None)
    montant_info = f"{facture['total_ttc']:.2f} EUR" if facture else "montant non trouve"

    # Determination du ton selon le delai
    if jours_retard <= 15:
        ton = "courtois et comprenant, rappel amical en supposant qu'il s'agit d'un oubli"
        niveau = "premiere relance (niveau 1)"
    elif jours_retard <= 30:
        ton = "ferme mais professionnel, rappelant les obligations contractuelles"
        niveau = "deuxieme relance (niveau 2)"
    else:
        ton = "tres ferme, mentionnant les penalites de retard et les actions legales possibles si non regle sous 8 jours"
        niveau = "relance finale avant contentieux (niveau 3)"

    prompt = f"""Tu es le service comptabilite de {ENTREPRISE['nom']}, une entreprise specialisee dans les solutions d'agents IA autonomes.

Redige un email de relance de paiement ({niveau}) avec les informations suivantes :

- Client : {client_nom} (email : {client_email})
- Numero de facture : {facture_num}
- Montant TTC : {montant_info}
- Retard de paiement : {jours_retard} jour(s)
- Date d'aujourd'hui : {datetime.now().strftime('%d/%m/%Y')}

Ton requis : {ton}

L'email doit inclure :
1. Un objet d'email precis
2. Une salutation appropriee
3. Le rappel des informations de facturation
4. Les coordonnees bancaires pour le virement : IBAN {ENTREPRISE['iban']}, BIC {ENTREPRISE['bic']}
5. Une conclusion adaptee au niveau de relance
6. La signature complete de {ENTREPRISE['nom']}

Redige uniquement l'email, sans commentaires supplementaires.
"""

    print(f"\n  Generation de la relance pour {client_nom} ({jours_retard} jour(s) de retard)...")
    print(_ligne_separateur())

    reponse = _streamer_reponse(prompt)

    ajouter_interaction(
        "agent_relance",
        f"Relance generee pour {client_nom} - Facture {facture_num} - {jours_retard}j de retard"
    )
    incrementer_stat("relances_envoyees")

    return reponse


# ---------------------------------------------------------------------------
# 3. Rapport financier mensuel
# ---------------------------------------------------------------------------

def agent_rapport_financier() -> str:
    """
    Genere un rapport financier mensuel base sur les donnees en memoire.
    """
    memoire = charger_memoire()
    factures = memoire.get("factures", [])
    stats = memoire.get("stats", {})

    # Calculs
    mois_courant = datetime.now().month
    annee_courante = datetime.now().year

    factures_mois = [
        f for f in factures
        if datetime.fromisoformat(f["date_emission"]).month == mois_courant
        and datetime.fromisoformat(f["date_emission"]).year == annee_courante
    ]

    ca_total = sum(f["total_ttc"] for f in factures)
    ca_mois = sum(f["total_ttc"] for f in factures_mois)
    ca_paye = sum(f["total_ttc"] for f in factures if f.get("payee"))
    ca_en_attente = ca_total - ca_paye

    nb_factures_total = len(factures)
    nb_factures_payees = sum(1 for f in factures if f.get("payee"))
    nb_en_retard = sum(1 for f in factures if _statut_facture(f) == "EN RETARD")

    taux_conversion = (nb_factures_payees / nb_factures_total * 100) if nb_factures_total > 0 else 0

    # Projection simple sur 3 mois
    moyenne_mensuelle = ca_mois if ca_mois > 0 else (ca_total / max(mois_courant, 1))
    projection_3mois = moyenne_mensuelle * 3

    donnees_rapport = f"""
Donnees financieres disponibles pour {ENTREPRISE['nom']} :

PERIODE : {datetime.now().strftime('%B %Y')}

CHIFFRE D'AFFAIRES :
- CA total (toutes periodes) : {ca_total:.2f} EUR TTC
- CA du mois en cours : {ca_mois:.2f} EUR TTC
- CA encaisse : {ca_paye:.2f} EUR TTC
- CA en attente : {ca_en_attente:.2f} EUR TTC

FACTURES :
- Nombre total : {nb_factures_total}
- Payees : {nb_factures_payees}
- En attente : {nb_factures_total - nb_factures_payees - nb_en_retard}
- En retard : {nb_en_retard}
- Taux de recouvrement : {taux_conversion:.1f}%

STATISTIQUES AGENT :
- Factures generees (session) : {stats.get('factures_generees', 0)}
- Relances envoyees (session) : {stats.get('relances_envoyees', 0)}

PROJECTIONS :
- Projection CA 3 prochains mois : {projection_3mois:.2f} EUR TTC
"""

    prompt = f"""Tu es un directeur financier expert de {ENTREPRISE['nom']}, specialiste en solutions d'agents IA.

Sur la base des donnees financieres suivantes, redige un rapport financier mensuel complet, professionnel et analytique :

{donnees_rapport}

Le rapport doit inclure :
1. Un resume executif (3-4 lignes)
2. Analyse du chiffre d'affaires avec tendances
3. Etat du portefeuille client (paiements, retards)
4. Analyse du taux de recouvrement et recommandations
5. Projections financieres et opportunites
6. Plan d'action recommande (3 actions prioritaires)
7. Conclusion

Utilise un format structure avec des titres clairs. Sois analytique, precis et oriente resultats.
Date du rapport : {datetime.now().strftime('%d/%m/%Y')}
"""

    print(f"\n  Generation du rapport financier mensuel...")
    print(_ligne_separateur())

    reponse = _streamer_reponse(prompt)

    ajouter_interaction("agent_rapport", "Rapport financier mensuel genere")
    incrementer_stat("rapports_generes")

    return reponse


# ---------------------------------------------------------------------------
# 4. Liste des factures
# ---------------------------------------------------------------------------

def lister_factures() -> None:
    """Affiche toutes les factures stockees en memoire avec leur statut."""
    memoire = charger_memoire()
    factures = memoire.get("factures", [])

    largeur = 85
    print("\n" + "=" * largeur)
    print(_centrer("LISTE DES FACTURES - " + ENTREPRISE["nom"], largeur))
    print("=" * largeur)

    if not factures:
        print("\n  Aucune facture enregistree.")
        print("=" * largeur)
        return

    print(f"\n  {'N° FACTURE':<18} {'CLIENT':<22} {'DATE':<12} {'MONTANT TTC':>12} {'ECHEANCE':<12} {'STATUT':<12}")
    print("-" * largeur)

    total_ttc = 0.0
    total_en_attente = 0.0
    total_en_retard = 0.0

    for f in sorted(factures, key=lambda x: x["date_emission"], reverse=True):
        statut = _statut_facture(f)
        date_em = datetime.fromisoformat(f["date_emission"]).strftime("%d/%m/%Y")
        date_ech = datetime.fromisoformat(f["date_echeance"]).strftime("%d/%m/%Y")
        client_nom = f["client"]["nom"][:21]
        montant = f["total_ttc"]
        total_ttc += montant

        if statut == "EN ATTENTE":
            total_en_attente += montant
        elif statut == "EN RETARD":
            total_en_retard += montant

        # Indicateur visuel selon statut
        indicateur = {"PAYEE": "[OK]", "EN ATTENTE": "[...]", "EN RETARD": "[!!!]"}.get(statut, "[ ]")

        print(
            f"  {f['numero']:<18} {client_nom:<22} {date_em:<12} {montant:>12.2f} EUR  {date_ech:<12} {indicateur} {statut}"
        )

    print("-" * largeur)
    print(f"\n  Total facturation   : {total_ttc:>10.2f} EUR TTC")
    print(f"  En attente          : {total_en_attente:>10.2f} EUR TTC")
    print(f"  En retard           : {total_en_retard:>10.2f} EUR TTC")
    print(f"\n  Nombre de factures  : {len(factures)}")
    print("=" * largeur + "\n")


# ---------------------------------------------------------------------------
# Menu principal
# ---------------------------------------------------------------------------

def afficher_menu() -> None:
    print("\n" + "=" * 55)
    print(_centrer("AGENT FACTURATION - AgentClaude Solutions", 55))
    print("=" * 55)
    print("  1. Generer une nouvelle facture")
    print("  2. Envoyer une relance de paiement")
    print("  3. Generer le rapport financier mensuel")
    print("  4. Lister les factures")
    print("  0. Quitter")
    print("=" * 55)


def saisir_services() -> tuple[list[dict], float]:
    """Saisie interactive des services d'une facture."""
    services = []
    print("\n  Saisie des services (laisser vide pour terminer) :")
    index = 1
    while True:
        print(f"\n  -- Service {index} --")
        description = input("  Description : ").strip()
        if not description:
            break
        try:
            quantite = int(input("  Quantite : ").strip() or "1")
            prix_unitaire = float(input("  Prix unitaire HT (EUR) : ").strip())
        except ValueError:
            print("  Valeur invalide. Service ignore.")
            continue
        services.append({"description": description, "quantite": quantite, "prix_unitaire": prix_unitaire})
        index += 1

    montant = 0.0
    if not services:
        try:
            montant = float(input("\n  Montant HT total (EUR) : ").strip())
        except ValueError:
            montant = 0.0

    return services, montant


def saisir_client() -> dict:
    """Saisie interactive des informations client."""
    print("\n  Informations client :")
    nom = input("  Nom / Raison sociale : ").strip()
    adresse = input("  Adresse : ").strip()
    email = input("  Email : ").strip()
    siret = input("  SIRET (optionnel) : ").strip()
    return {"nom": nom, "adresse": adresse, "email": email, "siret": siret}


def main() -> None:
    """Point d'entree principal du menu interactif."""
    print("\n  Demarrage de l'agent de facturation...")

    while True:
        afficher_menu()
        choix = input("  Votre choix : ").strip()

        if choix == "1":
            # Generer une facture
            client = saisir_client()
            services, montant = saisir_services()
            generer_facture(client, services, montant)

        elif choix == "2":
            # Relance de paiement
            lister_factures()
            facture_num = input("  Numero de facture a relancer : ").strip().upper()
            memoire = charger_memoire()
            factures = memoire.get("factures", [])
            facture = next((f for f in factures if f["numero"] == facture_num), None)

            if facture:
                client = facture["client"]
                try:
                    jours_retard = int(input("  Nombre de jours de retard : ").strip())
                except ValueError:
                    print("  Nombre invalide.")
                    continue
                agent_relance_paiement(client, facture_num, jours_retard)
            else:
                print(f"\n  Facture {facture_num} introuvable.")

        elif choix == "3":
            # Rapport financier
            agent_rapport_financier()

        elif choix == "4":
            # Lister les factures
            lister_factures()

        elif choix == "0":
            print("\n  Au revoir ! Agent de facturation arrete.\n")
            break

        else:
            print("\n  Choix invalide. Veuillez reessayer.")


if __name__ == "__main__":
    main()
