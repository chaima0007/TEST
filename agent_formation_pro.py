"""
AGENT ORGANISMES DE FORMATION PROFESSIONNELLE — Catalogues, communications, subventions, prospection
Usage : python agent_formation_pro.py
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
Tu es un assistant IA spécialisé pour les organismes de formation professionnelle belges, qu'ils soient publics, parapublics ou privés.
La Belgique compte plus de 3 000 organismes de formation enregistrés, avec des acteurs institutionnels majeurs : Bruxelles Formation, IFAPME (Institut wallon de Formation en Alternance et des indépendants et Petites et Moyennes Entreprises), VDAB (Vlaamse Dienst voor Arbeidsbemiddeling en Beroepsopleiding) et des centaines de centres privés agréés.
Tu maîtrises les mécanismes de financement belges : Chèques-formation en Wallonie (15€ de subvention par heure de formation agréée, plateforme chèques-formation.be), Formation Professionnelle Individuelle (FPI) via Actiris à Bruxelles pour les demandeurs d'emploi, congé-éducation payé (CEP) pour les travailleurs en Wallonie et à Bruxelles.
Tu connais les obligations légales en matière de formation : plan de formation annuel obligatoire pour les entreprises de plus de 20 employés (CCT n°9, article 10 de la loi du 5 mars 2017), et les exigences sectorielles de formation continue (fonds de formation sectoriels — Cefora, Constructiv, Fonds 4S, etc.).
Tu produis des descriptions de formations selon les standards pédagogiques : objectifs SMART, compétences visées selon les référentiels ESCO/ROME, méthodes pédagogiques (présentiel / distanciel / blended), modalités d'évaluation.
Tu connais les exigences SECO (Service d'évaluation et de contrôle des organismes de formation) et CVDC pour la reconnaissance de crédits de développement professionnel continu.
Tu sais rédiger des dossiers de demande de subventions structurés pour les fonds Chèques-formation Wallonie, le fonds de formation de Bruxelles Formation, et les fonds sectoriels.
Tu maîtrises la terminologie pédagogique belge : stagiaire, formateur, tuteur, référentiel de compétences, unité de formation, validation des acquis de l'expérience (VAE).
Tu génères des communications participant complètes : convocations, informations logistiques, questionnaires d'évaluation à chaud (satisfaction) et à froid (transfert en situation de travail).
Post-COVID, la formation en Belgique a connu une croissance de 35% du e-learning et du blended learning, et tu intègres ces modalités dans tes descriptions.
Un organisme de formation belge moyen gère 10 à 50 formateurs et entre 500 et 2 000 participants par an, avec une charge administrative considérable : catalogues de formation, dossiers individuels, certificats, rapports de subvention.
Rédiger un catalogue de 20 formations représente typiquement 3 mois de travail : Caelum Partners réduit ce délai à quelques heures.
Caelum Partners propose un forfait à 1 500€ qui remplace l'équivalent de 3 mois d'écriture de catalogue — ROI immédiat dès la première utilisation.
Ton ton est pédagogique, professionnel, valorisant les compétences, adapté aux exigences institutionnelles belges francophones.
Tu structures systématiquement les objectifs selon la taxonomie de Bloom (savoir, savoir-faire, savoir-être) pour chaque formation décrite.
Tu intègres toujours les mentions légales obligatoires pour les formations agréées : numéro d'agrément COCOF, Communauté française ou Région wallonne selon le cas.
"""

def sanitize(texte: str) -> str:
    return texte.strip()[:3000]

def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.2, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse

def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/formation_pro", exist_ok=True)
    fichier = f"fichiers/formation_pro/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def generer_description_formation(titre: str = ""):
    print("\n  — Génération d'une description de formation —")
    if not titre:
        titre = sanitize(input("  Titre de la formation : "))
    duree = sanitize(input("  Durée totale (ex: 2 jours / 14h / 3 modules de 4h) : "))
    public_cible = sanitize(input("  Public cible (ex: responsables RH, techniciens, managers, demandeurs d'emploi) : "))
    competences = sanitize(input("  Compétences / thèmes principaux couverts : "))
    modalite = sanitize(input("  Modalité (présentiel / distanciel / blended) : "))
    certification = sanitize(input("  Certification ou attestation délivrée (ou 'attestation de participation') : "))

    prompt = f"""Génère une description de formation professionnelle complète pour un organisme de formation belge.

FORMATION :
- Titre : {titre}
- Durée : {duree}
- Public cible : {public_cible}
- Compétences couverts : {competences}
- Modalité : {modalite}
- Certification : {certification}

La description doit inclure toutes les sections standard d'un catalogue belge de formation :

1. TITRE ACCROCHEUR ET SOUS-TITRE
   - Titre principal percutant (valorise le bénéfice professionnel)
   - Sous-titre descriptif (ce que le participant maîtrisera)

2. PRÉSENTATION DE LA FORMATION (100-150 mots)
   - Contexte et enjeux actuels de cette compétence en Belgique
   - Pourquoi cette formation est essentielle maintenant
   - Ce qui distingue cette formation (approche, intervenants, méthode)

3. OBJECTIFS DE FORMATION (taxonomie de Bloom)
   - Savoir (connaissances théoriques) : 3-4 objectifs
   - Savoir-faire (compétences pratiques) : 3-4 objectifs
   - Savoir-être (attitudes professionnelles) : 2-3 objectifs

4. PROGRAMME DÉTAILLÉ
   - Découpage par modules ou journées
   - Contenu précis de chaque module
   - Méthodes pédagogiques par module (exposé, atelier, étude de cas, jeu de rôle, e-learning)

5. PUBLIC CIBLE ET PRÉREQUIS
   - Profil idéal du participant
   - Prérequis obligatoires et recommandés
   - Niveau préalable requis

6. MODALITÉS PRATIQUES
   - Durée totale et planning (présentiel / distanciel / auto-apprentissage)
   - Taille de groupe recommandée
   - Matériel et supports fournis
   - Lieu de formation (si présentiel)

7. ÉVALUATION ET CERTIFICATION
   - Modalités d'évaluation des acquis
   - Attestation ou certification délivrée : {certification}
   - Numéro d'agrément Chèques-formation si applicable (mention à compléter)

8. INFORMATIONS PRATIQUES
   - Tarif HT (à compléter par l'organisme)
   - Financement possible : Chèques-formation Wallonie / FPI Bruxelles / Congé-éducation payé
   - Contact et inscription

Format : prêt pour catalogue imprimé et site web. Langue : français belge professionnel."""

    resultat = streamer(prompt, f"DESCRIPTION FORMATION : {titre.upper()}")
    sauvegarder(f"description_{titre.lower().replace(' ', '_')[:30]}", resultat)

def kit_communication_participants():
    print("\n  — Kit de communication participants —")
    nom_formation = sanitize(input("  Nom de la formation : "))
    date_formation = sanitize(input("  Date(s) de la formation : "))
    lieu = sanitize(input("  Lieu / lien e-learning : "))
    formateur = sanitize(input("  Nom du formateur / de l'équipe pédagogique : "))
    infos_pratiques = sanitize(input("  Informations pratiques supplémentaires (parking, repas, matériel à apporter) : "))

    prompt = f"""Génère un kit de communication complet pour les participants à une formation professionnelle belge.

FORMATION :
- Titre : {nom_formation}
- Date(s) : {date_formation}
- Lieu : {lieu}
- Formateur : {formateur}
- Infos pratiques : {infos_pratiques}

Génère les QUATRE documents suivants :

DOCUMENT 1 — EMAIL DE CONVOCATION (J-14)
- Objet : accrocheur et informatif
- Corps : confirmation d'inscription, rappel de l'objectif de la formation
- Programme résumé en 5 points
- Informations logistiques complètes (lieu, accès, parking, horaires précis)
- Ce qu'il faut apporter / préparer
- Contact organisateur
- Rappel des documents à fournir (attestations employeur, numéro de participant)

DOCUMENT 2 — EMAIL DE RAPPEL (J-2)
- Objet : "Rappel — {nom_formation} dans 2 jours"
- Corps court (10 lignes max) : rappel essentiel, lien carte/accès, contact urgence
- Encouragement et motivation avant la formation

DOCUMENT 3 — QUESTIONNAIRE D'ÉVALUATION À CHAUD (jour J, fin de formation)
- 8 à 10 questions structurées (échelle 1-5 + commentaire libre)
- Évaluation : contenu, formateur, rythme, supports, environnement
- Question ouverte : "Qu'allez-vous appliquer dès demain ?"
- Question NPS : "Recommanderiez-vous cette formation ?"
- Format : imprimable ou formulaire numérique

DOCUMENT 4 — QUESTIONNAIRE DE TRANSFERT (J+30, envoi par email)
- 6 questions sur le transfert des apprentissages en situation réelle
- "Avez-vous pu mettre en pratique les compétences acquises ?"
- Identification des obstacles au transfert
- Bénéfices mesurables observés
- Besoins de formation complémentaire identifiés

Format : documents prêts à utiliser, ton professionnel et bienveillant."""

    resultat = streamer(prompt, "KIT COMMUNICATION PARTICIPANTS FORMATION")
    sauvegarder("kit_communication_participants", resultat)

def rapport_competences_acquises(stagiaire: str = ""):
    print("\n  — Rapport de compétences acquises —")
    if not stagiaire:
        stagiaire = sanitize(input("  Nom du stagiaire / participant : "))
    formation_suivie = sanitize(input("  Formation suivie (titre, durée, dates) : "))
    performance_observee = sanitize(input("  Performance observée pendant la formation (présence, participation, exercices) : "))
    competences_evaluees = sanitize(input("  Compétences spécifiques évaluées et résultats : "))
    contexte_pro = sanitize(input("  Contexte professionnel du stagiaire (poste, secteur, objectif) : "))

    prompt = f"""Génère un rapport formel de compétences acquises pour un organisme de formation belge.

STAGIAIRE : {stagiaire}
FORMATION : {formation_suivie}
PERFORMANCE OBSERVÉE : {performance_observee}
COMPÉTENCES ÉVALUÉES : {competences_evaluees}
CONTEXTE PROFESSIONNEL : {contexte_pro}

Le rapport doit être formellement structuré pour être intégré dans des dossiers RH et pour la validation SECO/CVDC :

1. EN-TÊTE OFFICIEL
   - Organisme de formation (nom, numéro d'agrément, adresse)
   - Référence du rapport et date d'émission
   - Identification du stagiaire (nom, prénom, numéro national fictif ou référence interne)
   - Formation concernée : titre, durée, dates, formateur

2. SYNTHÈSE DES COMPÉTENCES ACQUISES
   Tableau par compétence :
   | Compétence | Référentiel (ESCO/sectoriel) | Niveau atteint (A1→C2 ou 1→5) | Observations |
   Pour chaque domaine : savoir / savoir-faire / savoir-être

3. ÉVALUATION DÉTAILLÉE
   - Présence et assiduité (heures réalisées / heures totales)
   - Participation active et engagement
   - Résultats aux évaluations formatives (exercices, quiz, études de cas)
   - Projet ou travail final (si applicable) : description et appréciation

4. AXES DE DÉVELOPPEMENT
   - Compétences en cours d'acquisition
   - Recommandations pour la pratique professionnelle
   - Formations complémentaires suggérées

5. RECOMMANDATION FORMATEUR
   - Appréciation globale du formateur
   - Adéquation entre le profil du stagiaire et la formation
   - Aptitude à exercer les compétences en situation professionnelle

6. ATTESTATION ET SIGNATURES
   - Attestation de réussite / participation (selon résultats)
   - Mention de la certification reconnue (Chèques-formation, CEP, SECO)
   - Signature du formateur + cachet de l'organisme
   - Lieu et date

Format : document officiel, sobre, prêt à archiver au dossier RH et à transmettre à l'employeur ou au fonds de financement."""

    resultat = streamer(prompt, f"RAPPORT COMPÉTENCES — {stagiaire.upper()}")
    sauvegarder(f"rapport_competences_{stagiaire.lower().replace(' ', '_')[:20]}", resultat)

def dossier_demande_subvention(formation: str = ""):
    print("\n  — Dossier de demande de subvention formation —")
    if not formation:
        formation = sanitize(input("  Titre et description de la formation : "))
    fonds_cible = sanitize(input("  Fonds ciblé (Chèques-formation Wallonie / FPI Actiris Bruxelles / Bruxelles Formation / fonds sectoriel) : "))
    public_beneficiaire = sanitize(input("  Public bénéficiaire (travailleurs / demandeurs d'emploi / indépendants) : "))
    duree_budget = sanitize(input("  Durée de la formation et budget prévisionnel par participant : "))
    organisme = sanitize(input("  Nom et numéro d'agrément de votre organisme : "))

    prompt = f"""Génère un dossier de demande de subvention structuré pour un organisme de formation belge.

FORMATION : {formation}
FONDS CIBLÉ : {fonds_cible}
PUBLIC BÉNÉFICIAIRE : {public_beneficiaire}
DURÉE ET BUDGET : {duree_budget}
ORGANISME : {organisme}

Le dossier doit contenir toutes les sections requises pour une demande de subvention belge :

1. PAGE DE GARDE
   - Identification de l'organisme demandeur (nom, forme juridique, numéro BCE, numéro d'agrément, adresse)
   - Titre du projet de formation
   - Fonds sollicité : {fonds_cible}
   - Montant sollicité (à compléter)
   - Période de mise en œuvre

2. PRÉSENTATION DE L'ORGANISME (1 page)
   - Historique et mission de l'organisme
   - Domaines d'expertise et formations dispensées
   - Références de formations similaires précédemment subventionnées
   - Agrément et accréditations (numéros à compléter)

3. DESCRIPTION DU PROJET DE FORMATION
   - Intitulé et justification du besoin sur le marché belge
   - Objectifs pédagogiques spécifiques et mesurables
   - Public cible et critères de sélection des participants
   - Description détaillée du contenu et du programme
   - Méthodes pédagogiques et ressources mobilisées

4. PLAN FINANCIER DÉTAILLÉ
   - Coûts directs : honoraires formateurs, matériaux pédagogiques, location salle
   - Coûts indirects : administration, frais généraux (% justifié)
   - Cofinancement éventuel (employeurs, autre fonds)
   - Montant sollicité auprès de {fonds_cible}
   - Coût par heure-participant et comparaison au marché

5. INDICATEURS D'IMPACT ET D'ÉVALUATION
   - Nombre de participants prévus
   - Taux de réussite visé
   - Indicateurs de transfert (comment mesurer l'impact en entreprise)
   - Rapport final prévu : contenu et délai de transmission

6. CALENDRIER D'EXÉCUTION
   - Planning des sessions avec dates indicatives
   - Jalons de reporting intermédiaire

7. DÉCLARATIONS ET ANNEXES
   - Déclaration sur l'honneur : pas de double financement pour les mêmes heures
   - Liste des annexes requises (statuts, agrément, CV formateurs, programme détaillé)
   - Signature du représentant légal

Format : dossier administratif officiel, structuré, prêt à soumettre. Langue : français belge administratif."""

    resultat = streamer(prompt, f"DOSSIER SUBVENTION — {fonds_cible.upper()[:40]}")
    sauvegarder("dossier_subvention", resultat)

def kit_prospection_organismes_formation():
    prompt = """Génère un kit de prospection commercial complet pour Caelum Partners ciblant les directeurs d'organismes de formation professionnelle belges.

Le kit doit contenir :

1. EMAIL DE PROSPECTION DIRECTEUR D'ORGANISME (objet + corps, 250 mots max)
   - Accroche sur la douleur réelle : "Rédiger un catalogue de 20 formations = 3 mois de travail"
   - Démonstration concrète : "Je génère 10 descriptions de formation en 30 minutes. Regardez."
   - Chiffre d'impact : gain de 3 mois de délai = catalogue disponible pour la rentrée suivante
   - Offre : forfait 1 500€ Caelum Partners
   - CTA : "Donnez-moi un titre de formation — je vous envoie la description en 5 minutes"

2. MESSAGE LINKEDIN DIRECTEUR FORMATION (300 caractères, punch)
   - Cible : Directeur pédagogique / Responsable formation / Chargé de développement organisme

3. SCRIPT DÉMO EN DIRECT (3 minutes — par email ou en présentiel)
   - Étape 1 : "Quel est votre prochain catalogue ?" → recueillir 3 titres de formations
   - Étape 2 : Génération de 3 descriptions complètes en direct (objectifs, programme, prérequis, financement)
   - Étape 3 : "Ce que vous venez de voir = 6 heures de travail rédactionnel. En 3 minutes."
   - Étape 4 : "Pour 1 500€, vous générez votre catalogue entier. Et les dossiers Chèques-formation. Et les rapports de compétences."

4. CALCUL ROI ORGANISME DE FORMATION
   - Hypothèses : organisme avec 30 formations au catalogue, renouvelé chaque année
   - Temps rédaction catalogue : 30 formations x 3h = 90h/an
   - Dossiers subvention : 10 dossiers/an x 4h = 40h/an
   - Rapports de compétences : 200 participants/an x 30min = 100h/an
   - TOTAL : 230h/an de rédaction administrative
   - Valorisation à 35€/h (chargé de formation) : 8 050€/an
   - Forfait Caelum 1 500€ : ROI 437% — payback en 7 semaines

5. ARGUMENT CHÈQUES-FORMATION
   - "Je génère aussi vos dossiers de demande de subvention Chèques-formation"
   - Impact : plus de subventions obtenues grâce à des dossiers mieux rédigés
   - "Chaque dossier bien rédigé = 15€/h subventionnée récupérée"

6. OBJECTIONS & RÉPONSES
   - "On a une équipe pédagogique" → "Elle sera libre pour créer, pas pour rédiger"
   - "Nos formations sont très spécifiques" → démo sur LEUR formation réelle
   - "1 500€ c'est cher" → "C'est 1 journée de votre chargé de formation. Il y en a 230 en jeu."

Ton : pédagogique, chiffré, axé sur le gain de temps réel. Signé Chaima Mhadbi — Caelum Partners, Bruxelles."""

    resultat = streamer(prompt, "KIT PROSPECTION ORGANISMES DE FORMATION")
    sauvegarder("kit_prospection_formation", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT ORGANISMES DE FORMATION PROFESSIONNELLE")
    print("  Catalogues · Participants · Subventions · Prospection")
    print("  Caelum Partners — Chaima Mhadbi, Bruxelles")
    print("═"*65)

    while True:
        print("\n  [MENU]")
        print("  1. Générer une description de formation")
        print("  2. Kit communication participants")
        print("  3. Rapport compétences acquises")
        print("  4. Dossier demande de subvention")
        print("  5. Kit prospection organismes de formation")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            print("  Au revoir.")
            break
        elif choix == "1":
            generer_description_formation()
        elif choix == "2":
            kit_communication_participants()
        elif choix == "3":
            rapport_competences_acquises()
        elif choix == "4":
            dossier_demande_subvention()
        elif choix == "5":
            kit_prospection_organismes_formation()
        else:
            print("  Choix invalide. Entrez 0 à 5.")
