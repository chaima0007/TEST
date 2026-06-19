"""
AGENT ADMINISTRATION MÉDICALE BELGE — Automatisation documentaire pour cabinets médicaux et paramédicaux
Usage : python agent_medical_admin.py
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
Tu es un assistant IA spécialisé dans l'administration des cabinets médicaux et paramédicaux belges, développé par Caelum Partners (Bruxelles).
La Belgique compte plus de 18 000 médecins généralistes, 10 000 spécialistes, 15 000 kinésithérapeutes, 8 000 dentistes — tous confrontés à une charge administrative considérable.
Tu maîtrises parfaitement l'écosystème INAMI (Institut National d'Assurance Maladie-Invalidité) : nomenclature, codes de prestation, remboursements et attestations.
Tu connais le DMG (Dossier Médical Global) : gestion, droits du patient, obligation de partage entre prestataires, financement annuel INAMI.
Tu comprends les obligations eHealth en Belgique : Réseau santé wallon, Hub-Metahub bruxellois, RSB flamand, consentement électronique du patient, plateforme eHealth.
Tu sais rédiger des lettres de référence médicales au format belge standard : identification du patient, anamnèse, motif de référence, traitements en cours, demande précise.
Tu génères des fiches d'information patient claires et accessibles, conformes aux recommandations INAMI et aux guidelines des sociétés scientifiques belges.
Tu connais les mutuelles belges principales : Mutualité Chrétienne (MC), Mutualité Socialiste (Solidaris), Mutualité Libérale, Mutualité Neutre, Mutualité Libre — et leurs formats de correspondance.
Tu maîtrises les autorisations préalables INAMI (accord préalable) : formulaires requis, délais de réponse, procédure de recours en cas de refus.
Tu sais rédiger des rapports de bilan de santé structurés pour le dossier patient, en respectant les obligations légales de conservation (30 ans selon loi belge).
Tu comprends le RGPD appliqué aux données de santé (catégorie sensible Art. 9 RGPD) : consentement, minimisation, droits d'accès, data breach notification.
Un médecin généraliste belge voit 30 à 40 patients par jour. Son gestionnaire de cabinet consacre 3 à 5 heures par jour à l'administration.
Le package Caelum à 1 500 € économise 60h/mois en tâches admin, libérant du temps pour les soins et améliorant la qualité de vie professionnelle.
Tu rédiges en français médical professionnel, clair et précis, adapté au contexte belge francophone.
Tu adaptes le niveau de langage selon le destinataire : technique pour lettres entre professionnels, accessible pour communications patients.
Tu ne fournis jamais de conseil médical ou diagnostic : tes documents sont des outils administratifs à valider par un professionnel de santé qualifié.
Tu intègres systématiquement le disclaimer médical obligatoire dans chaque document produit.
Tu es orienté vers la valeur opérationnelle immédiate : chaque document est directement utilisable par le secrétariat médical ou le praticien.
"""

DISCLAIMER_MEDICAL = "\n\n---\n⚠️  AVERTISSEMENT : Ce contenu est généré par IA (Caelum Partners) à des fins administratives de référence uniquement. Il doit impérativement être relu, complété et validé par un professionnel de santé qualifié avant tout usage clinique, envoi à un patient ou transmission à une mutuelle."

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
    os.makedirs("fichiers/medical_admin", exist_ok=True)
    fichier = f"fichiers/medical_admin/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu + DISCLAIMER_MEDICAL)
    print(f"  ✅ Sauvegardé → {fichier}")

def lettre_reference_medecin():
    print("\n  — Lettre de référence médecin —")
    situation_patient = sanitize(input("  Situation clinique du patient (âge, motif, antécédents pertinents) : "))
    motif_reference = sanitize(input("  Motif précis de la référence : "))
    type_specialiste = sanitize(input("  Type de spécialiste / service ciblé (cardiologue, dermatologue, urgences, etc.) : "))
    traitements_cours = sanitize(input("  Traitements et médicaments en cours : "))

    prompt = f"""Génère une lettre de référence médicale professionnelle au format belge standard.

DONNÉES CLINIQUES :
- Situation patient : {situation_patient}
- Motif de référence : {motif_reference}
- Spécialiste ciblé : {type_specialiste}
- Traitements en cours : {traitements_cours}

STRUCTURE DE LA LETTRE DE RÉFÉRENCE :

1. EN-TÊTE MÉDICAL
   - Coordonnées du médecin référent (à compléter : nom, spécialité, cabinet, INAMI n°, téléphone, email)
   - Destinataire : Dr [Nom], {type_specialiste}
   - Date
   - Objet : "Référence — Patient(e) : [Prénom Nom] — né(e) le [date]"
   - Mention CONFIDENTIEL — Document médical

2. IDENTIFICATION DU PATIENT
   - Données fictives à remplacer (nom, prénom, date de naissance, numéro INAMI patient / NISS)
   - Médecin traitant détenteur du DMG

3. MOTIF DE CONSULTATION ET ANAMNÈSE
   - Motif principal de consultation chez le référent
   - Historique de la situation clinique actuelle
   - Antécédents médicaux et chirurgicaux pertinents
   - Antécédents familiaux si pertinents pour le motif

4. EXAMEN CLINIQUE ET RÉSULTATS (section à compléter par le médecin)
   - Paramètres vitaux récents si disponibles
   - Résultats de biologie ou d'imagerie récents pertinents
   - Examens complémentaires déjà réalisés

5. TRAITEMENTS EN COURS
   - Liste structurée des médicaments : {traitements_cours}
   - Posologies et depuis quand (à compléter)
   - Allergies connues (à mentionner impérativement)

6. DEMANDE PRÉCISE AU SPÉCIALISTE
   - Ce qui est attendu du {type_specialiste} : avis diagnostique / prise en charge / acte technique
   - Questions précises posées
   - Degré d'urgence

7. FORMULE DE CONFRATERNITÈ
   - Remerciements confraternels
   - Disponibilité pour information complémentaire
   - Signature et cachet

Format : lettre médicale belge standard, directement utilisable après complétion des données personnalisées."""

    resultat = streamer(prompt, "LETTRE DE RÉFÉRENCE MÉDICALE")
    sauvegarder("lettre_reference", resultat)

def fiche_information_patient():
    print("\n  — Fiche d'information patient —")
    pathologie = sanitize(input("  Pathologie, procédure ou condition (ex: diabète type 2, coloscopie, hypertension) : "))
    public_cible = sanitize(input("  Public cible (adulte tout venant / personne âgée / parent d'enfant / etc.) : "))

    prompt = f"""Génère une fiche d'information patient complète en français clair et accessible pour le cabinet médical belge.

PATHOLOGIE / PROCÉDURE : {pathologie}
PUBLIC CIBLE : {public_cible}

STRUCTURE DE LA FICHE D'INFORMATION PATIENT :

1. EN-TÊTE
   - Nom du cabinet médical (à compléter)
   - Titre : "Information Patient — {pathologie}"
   - Date de mise à jour

2. QU'EST-CE QUE C'EST ? (explication simple, 3-5 phrases)
   - Définition accessible de {pathologie} en langage non médical
   - Prévalence en Belgique si connue
   - Qui est concerné

3. COMMENT RECONNAÎTRE LES SYMPTÔMES
   - Liste des symptômes principaux (langage patient, pas jargon médical)
   - Symptômes d'alarme nécessitant une consultation urgente
   - Distinction symptômes normaux vs préoccupants

4. PRÉPARATION / CE QU'IL FAUT FAIRE
   Si procédure médicale :
   □ Préparation avant la procédure (jeûne, arrêt médicaments, etc.)
   □ Ce qui se passera pendant la procédure
   □ Durée estimée et retour à la maison
   Si pathologie chronique :
   □ Mesures d'hygiène de vie recommandées
   □ Alimentation et activité physique
   □ Surveillance à domicile

5. TRAITEMENTS COURANTS
   - Aperçu des options de traitement (sans prescription)
   - Durée habituelle du traitement
   - Ce que le patient peut faire lui-même

6. QUAND RAPPELER OU CONSULTER EN URGENCE
   - Signaux d'alarme à surveiller
   - Numéros à appeler : médecin traitant, garde médicale (1733), urgences (112)
   - Délai de suivi recommandé

7. RESSOURCES COMPLÉMENTAIRES BELGES
   - Sites officiels : INAMI.be, health.belgium.be, association de patients belge spécialisée
   - Application eHealthbox si pertinent

Style : phrases courtes, langage B1 maximum, structuré avec des listes à puces. Illustrations suggérées (non générées ici)."""

    resultat = streamer(prompt, f"FICHE INFORMATION PATIENT — {pathologie.upper()}")
    sauvegarder("fiche_patient", resultat)

def rapport_bilan_sante():
    print("\n  — Rapport de bilan de santé —")
    profil_patient = sanitize(input("  Profil du patient (âge, sexe, antécédents principaux) : "))
    indicateurs = sanitize(input("  Indicateurs de santé disponibles (TA, IMC, glycémie, cholestérol, etc.) : "))
    contexte = sanitize(input("  Contexte du bilan (bilan annuel / médecine du travail / pré-opératoire / autre) : "))

    prompt = f"""Génère un modèle structuré de rapport de bilan de santé pour dossier patient belge.

PROFIL PATIENT : {profil_patient}
INDICATEURS : {indicateurs}
CONTEXTE : {contexte}

STRUCTURE DU RAPPORT DE BILAN DE SANTÉ :

1. EN-TÊTE DU RAPPORT
   - Cabinet médical (coordonnées à compléter, n° INAMI)
   - Patient : [Nom Prénom] — NISS : [à compléter] — né(e) le [date]
   - Date du bilan : {datetime.now().strftime("%d/%m/%Y")}
   - Type de bilan : {contexte}
   - Médecin réalisant le bilan

2. MOTIF ET CONTEXTE DU BILAN
   - Raison de la consultation de bilan
   - Antécédents médicaux personnels pertinents
   - Antécédents familiaux à risque
   - Traitements en cours et automédication
   - Mode de vie : tabac, alcool, activité physique, alimentation (à compléter)

3. EXAMEN CLINIQUE (template à compléter)
   - Poids : ___ kg | Taille : ___ cm | IMC : ___ kg/m²
   - Tension artérielle : ___ / ___ mmHg | Fréquence cardiaque : ___ bpm
   - Saturation O2 : ___% | Température : ___°C
   - Examen cardiovasculaire : [à compléter]
   - Examen pulmonaire : [à compléter]
   - Examen abdominal : [à compléter]
   - Autres examens spécifiques selon contexte

4. RÉSULTATS DES ANALYSES ET EXAMENS
   BIOLOGIE (valeurs de référence laboratoire belge incluses) :
   - Glycémie à jeun : ___ mg/dL (norme : 70-100)
   - Cholestérol total : ___ mg/dL (norme : < 200)
   - LDL : ___ | HDL : ___ | Triglycérides : ___
   - Créatinine : ___ | DFG estimé : ___
   - NFS : [valeurs à compléter]
   - Autres selon contexte : {indicateurs}

5. ANALYSE ET INTERPRÉTATION
   - Indicateurs dans les normes
   - Indicateurs hors norme nécessitant attention
   - Facteurs de risque identifiés
   - Score de risque cardiovasculaire si applicable (Score SCORE2 belge)

6. PLAN DE SUIVI ET RECOMMANDATIONS
   - Modifications du mode de vie recommandées
   - Traitements à initier, modifier ou poursuivre (à compléter par le médecin)
   - Examens complémentaires à planifier
   - Prochaine consultation de contrôle : dans ___ mois
   - Dépistages recommandés selon âge et sexe (dépistage cancer colorectal, mammographie, etc.)

7. SIGNATURE ET VALIDATION
   - Visa du médecin responsable du bilan
   - Remis au patient le : ___

Ce rapport est conservé dans le DMG pendant 30 ans conformément à la législation belge."""

    resultat = streamer(prompt, "RAPPORT DE BILAN DE SANTÉ")
    sauvegarder("rapport_bilan", resultat)

def lettre_mutualite():
    print("\n  — Lettre à la mutualité —")
    situation = sanitize(input("  Situation (autorisation préalable / recours refus / certificat / remboursement / etc.) : "))
    mutualite = sanitize(input("  Mutualité destinataire (MC / Solidaris / ML / Neutre / Libre / autre) : "))
    details = sanitize(input("  Détails de la demande (prestation concernée, code INAMI si connu, contexte médical) : "))

    prompt = f"""Génère une lettre professionnelle adressée à une mutualité belge pour le compte d'un cabinet médical.

SITUATION : {situation}
MUTUALITÉ : {mutualite}
DÉTAILS : {details}

LIVRABLES :

1. LETTRE OFFICIELLE À LA MUTUALITÉ
   EN-TÊTE :
   - Coordonnées du médecin / cabinet (à compléter : nom, n° INAMI, adresse, date)
   - Destinataire : Service médical de {mutualite}
   - Objet précis : "{situation} — Patient(e) [Nom Prénom] — NISS [à compléter]"
   - Référence dossier mutualité si connue

   CORPS DE LA LETTRE :
   A. IDENTIFICATION DU PATIENT ET DU MÉDECIN
      - Données patient (à compléter)
      - Médecin traitant et n° INAMI
      - Relation thérapeutique (DMG si applicable)

   B. EXPOSÉ DE LA SITUATION MÉDICALE (langage adapté au médecin-conseil)
      - Contexte clinique justifiant la demande
      - Diagnostic principal et comorbidités pertinentes
      - Traitements déjà tentés ou en cours
      - Motif médical précis de la demande : {details}

   C. DEMANDE FORMELLE
      - Nature exacte de la demande : {situation}
      - Code INAMI de la prestation si applicable
      - Urgence médicale éventuelle (délai de traitement requis)
      - Documents joints en annexe

   D. FONDEMENT RÉGLEMENTAIRE
      - Références à la nomenclature INAMI applicable
      - Articles de la loi coordonnée du 14 juillet 1994 (assurance maladie-invalidité) si pertinent
      - Précédents de remboursement éventuels

   E. CONCLUSION
      - Demande de décision dans les délais légaux (délai légal : 15 jours ouvrables pour accord préalable)
      - Coordonnées pour information médicale complémentaire
      - Signature du médecin

2. CHECKLIST DES DOCUMENTS À JOINDRE
   □ Formulaire INAMI spécifique si requis (type de formulaire)
   □ Rapport médical de justification
   □ Résultats d'examens à l'appui
   □ Copie de la prescription
   □ Consentement du patient (si transmission données médicales)

3. PROCÉDURE DE RECOURS (si refus anticipé ou déjà reçu)
   - Délai de recours : 90 jours après notification du refus
   - Adresse de recours : Chambre de recours INAMI
   - Arguments type pour renforcer le recours"""

    resultat = streamer(prompt, f"LETTRE À LA MUTUALITÉ — {mutualite.upper()}")
    sauvegarder("lettre_mutualite", resultat)

def kit_prospection_cabinets_medicaux():
    prompt = """Génère un kit de prospection commercial complet pour Caelum Partners ciblant les cabinets médicaux et paramédicaux belges.

CONTEXTE CAELUM PARTNERS :
- Cabinet d'automatisation IA basé à Bruxelles, fondé par Chaima Mhadbi
- Services : 500 € (starter), 1 500 € (standard), 3 000 € (premium)
- Cible : médecins généralistes, spécialistes, kinésithérapeutes, dentistes en Belgique
- Offre phare pour ce secteur : package 1 500 € standard
- Volume total cible : 50 000+ professionnels de santé en Belgique

LIVRABLES :

1. EMAIL DE PROSPECTION (objet + corps complet)
   - Objet : basé sur la douleur principale (surcharge administrative, temps perdu sur correspondances, conformité RGPD santé)
   - Accroche percutante : chiffrer le temps admin (3-5h/jour × 220 jours = 660-1100h/an sur l'administration)
   - Argument différenciant : Caelum connaît l'écosystème belge (INAMI, mutuelles, eHealth, RGPD santé)
   - ROI concret : 1 500 € → économie de 60h/mois → valeur libérée ≥ 3 000 €/mois
   - Angle RGPD santé : Caelum aide à la conformité des communications patient (données catégorie spéciale Art. 9)
   - Call to action : démonstration gratuite de 30 minutes au cabinet ou en visio
   - Ton : respectueux de la charge de travail des médecins, sobre, factuel

2. MESSAGE LINKEDIN POUR PRATICIENS BELGES (300 caractères max)
   - Accroche sur la surcharge administrative médicale belge
   - Proposition de valeur en 2 phrases
   - Call to action adapté au milieu médical (ton professionnel et non commercial)

3. CALCUL ROI DÉTAILLÉ POUR CE SECTEUR
   Avant IA (cabinet MG, 30 patients/jour) :
   - Lettre de référence : 20 min → Après IA : 3 min
   - Lettre à la mutualité : 30 min → Après IA : 5 min
   - Fiche info patient (à créer) : 1h → Après IA : 8 min
   - Rapport de bilan de santé : 25 min → Après IA : 5 min
   → Économie par patient référé : 17 min
   → Si 60 références/mois = 17h économisées
   → À 80 €/h valeur temps médecin = 1 360 €/mois
   → ROI package 1 500 € : rentabilisé en 1,1 mois

4. RÉPONSES AUX 3 OBJECTIONS SPÉCIFIQUES SECTEUR MÉDICAL
   - "Le RGPD santé interdit de passer des données patients à une IA externe"
   - "Les médecins ne sont pas des cibles pour des outils tech"
   - "Le secrétariat médical gère déjà très bien sans IA"

5. SCRIPT D'APPROCHE DU GESTIONNAIRE DE CABINET (pas du médecin directement)
   - Cibler en priorité : secrétaires médicales et office managers
   - Introduction en 20 secondes
   - 3 questions pour identifier le volume administratif
   - Démonstration rapide sur un exemple concret du cabinet

6. ARGUMENT CONFIANCE / RGPD
   - Positionnement Caelum : outil de rédaction, pas de stockage de données patient
   - Les praticiens complètent les données sensibles localement
   - Conformité au principe de minimisation des données (Art. 5 RGPD)"""

    resultat = streamer(prompt, "KIT PROSPECTION CABINETS MÉDICAUX BELGES")
    sauvegarder("kit_prospection_medical", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT ADMINISTRATION MÉDICALE BELGE")
    print("  Automatisation documentaire — Caelum Partners")
    print("═"*65)
    while True:
        print("\n  [menu]")
        print("  1. Lettre de référence médecin")
        print("  2. Fiche information patient")
        print("  3. Rapport bilan santé")
        print("  4. Lettre à la mutualité")
        print("  5. Kit prospection cabinets médicaux")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            print("  Au revoir.")
            break
        elif choix == "1":
            lettre_reference_medecin()
        elif choix == "2":
            fiche_information_patient()
        elif choix == "3":
            rapport_bilan_sante()
        elif choix == "4":
            lettre_mutualite()
        elif choix == "5":
            kit_prospection_cabinets_medicaux()
        else:
            print("  Choix invalide.")
