"""
AGENT FIDUCIAIRE & EXPERT-COMPTABLE IA — Automatisation documentaire pour cabinets comptables belges
Usage : python agent_fiduciaire.py
"""
import os
import sys
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

IDENTITE = """
Tu es un assistant IA spécialisé pour les fiduciaires et experts-comptables belges, développé par Caelum Partners (Bruxelles).
La Belgique compte plus de 7 000 cabinets comptables enregistrés auprès de l'ITAA (Institut des Experts-Comptables et des Conseils Fiscaux).
Tu maîtrises parfaitement la fiscalité belge : IPP (Impôt des Personnes Physiques), ISOC (Impôt des Sociétés), TVA trimestrielle et mensuelle, INASTI pour les indépendants.
Tu connais toutes les obligations déclaratives belges : dépôt des comptes annuels à la BCE/NBB, registre UBO, bilan social, déclaration TVA, BIZTAX, MyMinFin.
Tu sais rédiger des rapports de gestion mensuelle professionnels avec ratios financiers, commentaires analytiques et recommandations stratégiques.
Tu produis des mémos d'optimisation fiscale légale en référençant le Code des impôts sur les revenus (CIR 92), le Code TVA et les circulaires administratives belges.
Tu génères des checklists de clôture annuelle exhaustives pour PME belges : tous les dépôts obligatoires, délais légaux et documents requis.
Tu rédiges des lettres d'accueil et d'engagement pour nouveaux clients avec toutes les mentions légales ITAA et RGPD.
Tu comprends les spécificités belges : Companyweb, BCE (Banque-Carrefour des Entreprises), numéro d'entreprise TVA BE, forme juridique (SA, SRL, SNC, etc.).
Tu connais les régimes spéciaux : régime de la petite société (article 15 CSA), déduction pour investissement, VVPR bis pour dividendes réduits, régime de la réserve de liquidation.
Une fiduciaire gérant 150-300 dossiers clients peut économiser 20h/mois grâce à l'automatisation des rapports et correspondances IA.
À 150 €/heure de taux de facturation, cela représente 3 000 €/mois économisés, soit un ROI de 24× sur le package Caelum à 1 500 €.
Les fiduciaires ne peuvent pas être remplacées par l'IA pour la signature des déclarations : l'IA les assiste dans la préparation des documents.
Tu es rigoureux, précis et tu cites systématiquement les références légales belges exactes (articles de loi, numéros de circulaire).
Tu rédiges en français professionnel comptable et fiscal, avec un ton adapté aux relations B2B entre fiduciaires et leurs clients PME.
Tes documents sont directement utilisables par un expert-comptable ITAA sans correction substantielle nécessaire.
Tu aides Caelum Partners à démontrer la valeur commerciale de l'automatisation IA aux fiduciaires belges.
Tu ne fournis jamais de conseil fiscal personnalisé engageant : tes documents restent des outils de préparation à valider par un professionnel qualifié.
"""

def sanitize(text: str, max_chars: int = 3000) -> str:
    if not isinstance(text, str):
        text = str(text)
    return text.strip()[:max_chars]

def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.15, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse

def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/fiduciaire", exist_ok=True)
    fichier = f"fichiers/fiduciaire/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def generer_rapport_gestion_mensuel():
    print("\n  — Rapport de gestion mensuel —")
    nom_client = sanitize(input("  Nom du client / société : "))
    secteur = sanitize(input("  Secteur d'activité : "))
    mois = sanitize(input("  Mois concerné (ex: mai 2025) : "))
    ca = sanitize(input("  Chiffre d'affaires du mois (€) : "))
    charges = sanitize(input("  Charges totales du mois (€) : "))
    details = sanitize(input("  Informations supplémentaires (stock, investissements, personnel, etc.) : "))

    prompt = f"""Génère un rapport de gestion mensuel professionnel pour un client PME belge d'une fiduciaire.

DONNÉES DU CLIENT :
- Société : {nom_client}
- Secteur : {secteur}
- Période : {mois}
- Chiffre d'affaires : {ca} €
- Charges totales : {charges} €
- Informations complémentaires : {details}

STRUCTURE DU RAPPORT :

1. EN-TÊTE PROFESSIONNEL
   - Destinataire : [Nom du gérant/directeur financier]
   - Expéditeur : [Nom de la fiduciaire]
   - Objet : Rapport de gestion mensuel — {mois}

2. SYNTHÈSE EXÉCUTIVE (10 lignes max)
   - Performance globale du mois en langage clair pour le chef d'entreprise
   - 3 points positifs et 2 points d'attention

3. ANALYSE FINANCIÈRE DÉTAILLÉE
   - Résultat net du mois (CA - Charges)
   - Marge brute estimée et ratio
   - Ratio charges fixes / CA
   - Commentaire analytique sur l'évolution et les tendances

4. INDICATEURS CLÉS (KPIs)
   - Taux de marge
   - Point mort mensuel estimé
   - Ratio de liquidité si données disponibles
   - Comparaison mois précédent (estimation tendance)

5. RECOMMANDATIONS STRATÉGIQUES
   - 3 recommandations concrètes et actionnables pour le mois suivant
   - Points de vigilance fiscaux et comptables

6. PROCHAINES ÉTAPES
   - Documents à fournir à la fiduciaire pour le mois suivant
   - Échéances fiscales ou sociales du mois à venir

Style : professionnel, clair, orienté décision. Adapté à un dirigeant de PME belge."""

    resultat = streamer(prompt, "RAPPORT DE GESTION MENSUEL")
    sauvegarder("rapport_gestion", resultat)

def memo_optimisation_fiscale():
    print("\n  — Mémo d'optimisation fiscale —")
    situation = sanitize(input("  Décris la situation du client (structure, revenus, charges, objectifs) : "))

    prompt = f"""Génère un mémo d'optimisation fiscale légale pour un client d'une fiduciaire belge.

SITUATION DU CLIENT : {situation}

STRUCTURE DU MÉMO :

1. EN-TÊTE
   - Note interne confidentielle — Optimisation fiscale
   - Date et référence dossier

2. RÉSUMÉ DE LA SITUATION FISCALE ACTUELLE
   - Régime fiscal applicable (IPP / ISOC / assujetti TVA)
   - Charges fiscales et sociales actuelles estimées
   - Points de friction identifiés

3. PISTES D'OPTIMISATION LÉGALE (avec références légales belges exactes)

   A. OPTIMISATION ISOC / IPP
   - Rémunération du dirigeant vs dividendes (arbitrage optimal)
   - VVPR bis pour dividendes à taux réduit (15 % au lieu de 30 %) — Art. 269 §2 CIR 92
   - Réserve de liquidation — Art. 184quater CIR 92
   - Déduction pour investissement (DPI) si applicable — Art. 68-77 CIR 92

   B. OPTIMISATION TVA
   - Régime de déduction applicable
   - Récupération de TVA sur véhicules et frais mixtes
   - Régime du forfait agricole ou simplifié si pertinent

   C. OPTIMISATION SOCIALE (INASTI)
   - Cotisations sociales et leur base de calcul
   - Pension libre complémentaire (PLCI) — avantage fiscal et social
   - Convention de management si applicable

   D. AUTRES LEVIERS
   - Plan cafétéria ou avantages en nature
   - Voiture de société vs indemnité km
   - Eco-chèques et chèques-repas (optimisation coût employeur)

4. RECOMMANDATION PRIORITAIRE
   - Action numéro 1 à mettre en place immédiatement
   - Économie fiscale estimée

5. AVERTISSEMENT LÉGAL
   "Ce mémo est préparé par Caelum Partners IA à des fins de référence et doit être validé par un expert-comptable ITAA qualifié avant toute décision fiscale."

Cite systématiquement les articles du CIR 92, du Code TVA ou des lois sociales belges applicables."""

    resultat = streamer(prompt, "MÉMO OPTIMISATION FISCALE BELGE")
    sauvegarder("memo_fiscal", resultat)

def checklist_cloture_annuelle():
    print("\n  — Checklist de clôture annuelle —")
    type_societe = sanitize(input("  Type de société (SRL / SA / indépendant personne physique / ASBL) : "))
    exercice = sanitize(input("  Exercice comptable (ex: 01/01/2024 - 31/12/2024) : "))

    prompt = f"""Génère une checklist exhaustive de clôture annuelle pour une PME belge.

TYPE D'ENTITÉ : {type_societe}
EXERCICE : {exercice}

CHECKLIST COMPLÈTE DE CLÔTURE ANNUELLE :

1. OPÉRATIONS COMPTABLES DE CLÔTURE
   □ Inventaire physique des stocks valorisé
   □ Réconciliation des comptes bancaires avec extraits
   □ Lettrage de tous les comptes clients et fournisseurs
   □ Provisions pour créances douteuses (évaluation et justification)
   □ Amortissements : calcul et comptabilisation (tableau annuel)
   □ Provisions pour risques et charges éventuelles
   □ Régularisation des charges et produits à imputer (comptes 49x)
   □ Vérification et réconciliation comptes TVA (724/411/451)
   □ Vérification cohérence ONSS et fiches fiscales

2. DOCUMENTS À COLLECTER AUPRÈS DU CLIENT
   □ Extraits bancaires complets de l'exercice
   □ Factures d'achat et de vente de décembre
   □ Contrats de leasing / crédit-bail en cours
   □ Inventaire valorisé des stocks au 31/12
   □ Liste des immobilisations acquises/cédées dans l'exercice
   □ Tableau des dettes et créances fin d'exercice
   □ Procès-verbaux du Conseil d'Administration ou AG
   □ Contrats d'assurance en cours (valeur assurée)

3. OBLIGATIONS DÉCLARATIVES ET DÉLAIS LÉGAUX
   □ Déclaration ISOC ou IPP professionnels : délai légal selon exercice
   □ Dépôt des comptes annuels à la BCE/NBB : dans les 30 jours après AG (max 7 mois après clôture)
   □ Assemblée Générale annuelle : à tenir dans les 6 mois de la clôture
   □ Registre UBO : vérification et mise à jour si changements
   □ Bilan social : à déposer avec les comptes annuels si >20 ETP
   □ Fiches fiscales 281.10 / 281.20 (salaires et honoraires) : avant le 1er mars

4. CONTRÔLES QUALITÉ AVANT DÉPÔT
   □ Vérification équilibre bilan (actif = passif)
   □ Concordance avec déclarations TVA de l'exercice
   □ Cohérence ONSS déclarée et comptabilisée
   □ Vérification des seuils petite société (Art. 1:24 CSA)
   □ Revue analytique : comparaison N vs N-1, ratios clés

5. APRÈS CLÔTURE
   □ Envoi des comptes annuels au client pour approbation
   □ Convocation AG ordinaire
   □ Archivage légal : 7 ans pour pièces comptables (Art. III.86 Code de droit économique)

Adapté spécifiquement aux obligations légales belges pour {type_societe}, exercice {exercice}."""

    resultat = streamer(prompt, "CHECKLIST CLÔTURE ANNUELLE BELGE")
    sauvegarder("checklist_cloture", resultat)

def lettre_onboarding_nouveau_client():
    print("\n  — Lettre d'onboarding nouveau client —")
    nom_client = sanitize(input("  Nom du client / société : "))
    type_client = sanitize(input("  Type (indépendant / SRL / SA / ASBL / particulier) : "))
    services = sanitize(input("  Services souscrits (comptabilité mensuelle / TVA / ISOC / conseils / etc.) : "))

    prompt = f"""Génère un pack d'onboarding professionnel complet pour accueillir un nouveau client dans une fiduciaire belge.

CLIENT : {nom_client}
TYPE D'ENTITÉ : {type_client}
SERVICES SOUSCRITS : {services}

LIVRABLES :

1. LETTRE DE BIENVENUE PROFESSIONNELLE
   - Accueil chaleureux et professionnel
   - Présentation de l'équipe dédiée au dossier
   - Rappel des services souscrits et de la valeur ajoutée de la fiduciaire
   - Engagement de qualité et de disponibilité
   - Coordonnées et canaux de communication préférés

2. CHECKLIST DOCUMENTS À FOURNIR EN PRIORITÉ
   □ Documents identitaires du gérant / actionnaires (UBO)
   □ Statuts coordonnés de la société (extrait BCE)
   □ Extraits bancaires des 3 derniers mois
   □ Dernières déclarations TVA et ISOC/IPP
   □ Derniers comptes annuels déposés à la BCE
   □ Contrats en cours (bail, leasing, personnel)
   □ Tableau des immobilisations existant
   □ Accès comptabilité précédente (si reprise de dossier)

3. LETTRE DE MISSION (ENGAGEMENT LETTER)
   - Identification des parties (fiduciaire et client)
   - Description précise des missions confiées
   - Honoraires convenus et modalités de facturation
   - Obligations réciproques (délais de transmission, réactivité)
   - Clause de confidentialité et protection des données (RGPD)
   - Mention obligations ITAA et anti-blanchiment (loi du 18/09/2017)
   - Clause de résiliation et délai de préavis
   - Loi applicable et juridiction compétente

4. FORMULAIRE DE COLLECTE D'INFORMATIONS
   - Informations générales sur l'activité
   - Coordonnées bancaires et accès ebanking
   - Interlocuteurs clés dans la société
   - Préférences de communication

Ton : professionnel, rassurant et orienté partenariat durable. Conforme aux exigences ITAA et RGPD."""

    resultat = streamer(prompt, "PACK ONBOARDING NOUVEAU CLIENT FIDUCIAIRE")
    sauvegarder("onboarding_client", resultat)

def kit_prospection_fiduciaires():
    prompt = """Génère un kit de prospection commercial complet pour Caelum Partners ciblant les fiduciaires et experts-comptables belges.

CONTEXTE CAELUM PARTNERS :
- Cabinet d'automatisation IA basé à Bruxelles, fondé par Chaima Mhadbi
- Services : 500 € (starter), 1 500 € (standard), 3 000 € (premium)
- Cible : 7 000+ fiduciaires ITAA en Belgique
- Offre phare pour ce secteur : package 1 500 € standard

LIVRABLES :

1. EMAIL DE PROSPECTION (objet + corps complet)
   - Objet : basé sur la douleur principale (volume administratif, pression des délais fiscaux)
   - Accroche chiffrée et percutante pour associé gérant de fiduciaire
   - Calcul ROI intégré : 20h/mois économisées × 150 €/h = 3 000 €/mois = ROI 24× sur 1 500 €
   - Cas d'usage concrets : rapports de gestion, mémos fiscaux, onboarding clients
   - Garantie : conformité ITAA et RGPD
   - Call to action : démonstration gratuite de 45 minutes
   - Ton B2B professionnel, sobre, chiffré

2. MESSAGE LINKEDIN (300 caractères max)
   - Accroche sur la surcharge administrative des fiduciaires belges
   - Chiffre ROI impactant en 2 phrases
   - Call to action

3. CALCUL ROI DÉTAILLÉ PAR TYPE DE TÂCHE
   Avant IA :
   - Rapport de gestion mensuel par client : 3h → Après IA : 30 min
   - Mémo fiscal par dossier complexe : 4h → Après IA : 45 min
   - Checklist clôture annuelle : 2h → Après IA : 20 min
   - Lettre onboarding nouveau client : 1h → Après IA : 10 min
   → Calcul économie totale mensuelle pour fiduciaire de 200 dossiers
   → Comparaison coût Caelum 1 500 € vs gains générés sur 12 mois

4. RÉPONSES AUX 3 OBJECTIONS PRINCIPALES
   - "L'ITAA interdit aux IA de signer des déclarations fiscales"
   - "Nos clients ont des situations trop complexes pour l'IA"
   - "Nous avons déjà un logiciel comptable (Winbooks, Bob50, Exact)"

5. SCRIPT D'APPEL DE DÉCOUVERTE (2 minutes)
   - Introduction Caelum Partners en 30 secondes
   - 3 questions de qualification (volume dossiers, douleur principale, temps admin/semaine)
   - Pivot vers démo produit

6. OFFRE DE DÉMONSTRATION GRATUITE
   - Script de présentation de la démo (30-45 min)
   - Ce que le prospect verra en direct
   - Prochaine étape après la démo"""

    resultat = streamer(prompt, "KIT PROSPECTION FIDUCIAIRES BELGES")
    sauvegarder("kit_prospection_fiduciaire", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT FIDUCIAIRE & EXPERT-COMPTABLE IA")
    print("  Automatisation documentaire — Caelum Partners")
    print("═"*65)
    while True:
        print("\n  [menu]")
        print("  1. Rapport de gestion mensuel")
        print("  2. Mémo optimisation fiscale")
        print("  3. Checklist clôture annuelle")
        print("  4. Lettre onboarding nouveau client")
        print("  5. Kit prospection fiduciaires")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            print("  Au revoir.")
            break
        elif choix == "1":
            generer_rapport_gestion_mensuel()
        elif choix == "2":
            memo_optimisation_fiscale()
        elif choix == "3":
            checklist_cloture_annuelle()
        elif choix == "4":
            lettre_onboarding_nouveau_client()
        elif choix == "5":
            kit_prospection_fiduciaires()
        else:
            print("  Choix invalide.")
