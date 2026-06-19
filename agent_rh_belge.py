"""
AGENT RH & DROIT DU TRAVAIL BELGE — Automatisation documentaire RH pour employeurs et gestionnaires belges
Usage : python agent_rh_belge.py
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
Tu es un assistant IA spécialisé en ressources humaines et droit du travail belge, développé par Caelum Partners (Bruxelles).
Le droit du travail belge est l'un des plus complexes d'Europe : CCT (Conventions Collectives de Travail) sectorielles, statut unique depuis 2014, plus de 200 commissions paritaires (CP) avec leurs règles spécifiques.
Tu maîtrises parfaitement l'ONSS (Office National de Sécurité Sociale), le calcul des cotisations sociales patronales (~27 %) et personnelles (~13,07 %).
Tu connais l'obligation Dimona : déclaration obligatoire à l'ONSS dans les 24h de tout début de prestation, sous peine d'amende de 1 000 € par travailleur non déclaré.
Tu maîtrises les avantages extralégaux belges : eco-chèques (250 €/an max), chèques-repas (8 €/jour max en 2024 dont 1,09 € à charge travailleur), chèques-sport et culture, hospitalisation assurance obligatoire depuis 2023.
Tu sais calculer les préavis de licenciement selon la Loi du 26 décembre 2013 (statut unique) : formule ancienneté en semaines de préavis (1 semaine par année tranche + règle des tranches).
Tu rédiges des offres d'emploi conformes aux obligations légales belges : non-discrimination, mention de la rémunération ou fourchette, langue de l'offre selon région.
Tu génères des kits d'onboarding conformes au droit belge : remise obligatoire du règlement de travail, notice de Dimona, fiches d'information ONSS.
Tu connais les spécificités régionales en matière d'emploi : primes à l'emploi en Wallonie et Bruxelles, activa.brussels, mesures flamandes VDAB.
Tu comprends la structure de la fiche de salaire belge : rémunération brute, ONSS personnel, précompte professionnel, net imposable, avantages en nature.
Le 13ème mois et le double pécule de vacances (pécule de sortie) sont des spécificités belges fondamentales à toujours mentionner dans les contrats.
Tu aides Caelum Partners à démontrer que l'automatisation IA permet d'économiser 15h/mois à un gestionnaire RH d'une PME de 10 personnes.
Le package Caelum à 1 500 € génère un ROI immédiat pour toute PME belge dépassant 5 salariés.
Tu rédiges en français professionnel RH, avec des équivalents néerlandais lorsque le contexte bruxellois ou flamand l'exige.
Tes documents respectent strictement la législation du travail belge et les CCT applicables au secteur mentionné.
Tu ne fournis jamais de conseil juridique en droit social engageant : tes documents doivent être validés par un conseiller social ou avocat spécialisé.
Tu es orienté vers la valeur opérationnelle immédiate : chaque livrable est utilisable directement par un responsable RH ou dirigeant de PME belge.
Tu connais les outils RH belges : Securex, Partena, Attentia, SD Worx — les secrétariats sociaux agréés auxquels les PME font appel.
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
    os.makedirs("fichiers/rh_belge", exist_ok=True)
    fichier = f"fichiers/rh_belge/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def generer_offre_emploi():
    print("\n  — Générer une offre d'emploi FR + NL —")
    poste = sanitize(input("  Intitulé du poste : "))
    secteur = sanitize(input("  Secteur d'activité / commission paritaire si connue : "))
    localisation = sanitize(input("  Localisation (commune, région) : "))
    competences = sanitize(input("  Compétences et qualifications requises : "))
    salaire = sanitize(input("  Fourchette salariale brute mensuelle (€) : "))
    avantages = sanitize(input("  Avantages extralégaux proposés : "))

    prompt = f"""Génère une offre d'emploi professionnelle complète conforme au droit belge.

DONNÉES DU POSTE :
- Intitulé : {poste}
- Secteur / CP : {secteur}
- Localisation : {localisation}
- Compétences requises : {competences}
- Rémunération brute : {salaire} €/mois
- Avantages extralégaux : {avantages}

LIVRABLES :

1. OFFRE D'EMPLOI EN FRANÇAIS — FORMAT STEPSTONE / LINKEDIN (350-450 mots)
   - Titre accrocheur et précis
   - Présentation de l'entreprise (section à personnaliser)
   - Description du poste et des missions principales (liste à puces)
   - Profil recherché : compétences techniques et soft skills
   - Ce que nous offrons : rémunération, avantages (chèques-repas {avantages if avantages else "8 €/jour"}, assurance hospitalisation, 13ème mois, etc.)
   - Mentions légales obligatoires belges : non-discrimination, égalité H/F, régime de travail
   - Procédure de candidature claire

2. NEDERLANDSTALIGE SAMENVATTING (150 mots)
   - Titre en néerlandais
   - Description synthétique du poste et du profil
   - Avantages et procédure de candidature

3. FOURCHETTE SALARIALE DE MARCHÉ
   - Benchmark salaire brut mensuel pour ce poste en Belgique
   - Coût employeur estimé (brut × ~1,33 pour cotisations patronales ONSS)
   - Équivalent net mensuel indicatif

4. QUESTIONS D'ENTRETIEN SUGGÉRÉES (5 questions)
   - Adaptées au poste et conformes à la législation anti-discrimination belge
   - Pas de questions sur état civil, religion, origine, plans de grossesse (interdits)

Conformité : non-discrimination selon la Loi Antidiscrimination du 10 mai 2007, langue selon région de l'offre."""

    resultat = streamer(prompt, "OFFRE D'EMPLOI FR + NL")
    sauvegarder("offre_emploi", resultat)

def kit_onboarding_employe():
    print("\n  — Kit d'onboarding employé —")
    nom_employe = sanitize(input("  Prénom et nom de l'employé (optionnel) : "))
    poste = sanitize(input("  Poste occupé : "))
    date_entree = sanitize(input("  Date d'entrée en service : "))
    avantages = sanitize(input("  Avantages proposés (chèques-repas, voiture, etc.) : "))

    employe_ref = nom_employe if nom_employe else "Madame/Monsieur [Nom Prénom]"

    prompt = f"""Génère un kit d'onboarding complet pour un nouvel employé dans une PME belge.

DONNÉES :
- Employé : {employe_ref}
- Poste : {poste}
- Date d'entrée : {date_entree}
- Avantages : {avantages}

LIVRABLES :

1. LETTRE DE BIENVENUE PERSONNALISÉE
   - Accueil chaleureux et professionnel de l'employeur
   - Contexte de l'entreprise et de l'équipe
   - Expression de la confiance accordée et des attentes
   - Invitation à poser des questions librement

2. CHECKLIST PREMIÈRE SEMAINE (format jour par jour)
   Jour 1 :
   □ Accueil par le responsable direct et tour des locaux
   □ Remise du règlement de travail (obligation légale — Art. 11 Loi du 8/04/1965)
   □ Activation des accès informatiques et badges
   □ Présentation de l'équipe
   □ Vérification Dimona effectuée par l'employeur (avant le premier jour ou jour même)
   Jours 2-3 : Formation aux outils et processus internes
   Jours 4-5 : Premières missions accompagnées

3. EXPLICATION DIMONA EN LANGAGE SIMPLE
   - Qu'est-ce que la Dimona et pourquoi c'est important
   - Ce que l'employé doit savoir sur sa propre déclaration ONSS
   - Comment vérifier sa propre Dimona sur mySocial.be

4. RÉSUMÉ DES AVANTAGES ET RÉMUNÉRATION
   - Structure du salaire brut → net expliquée simplement
   - Détail des avantages : {avantages}
   - Chèques-repas : montant, utilisation, carte Edenred/Sodexo
   - Assurance hospitalisation : démarches d'affiliation
   - Pécule de vacances : calcul et droits (4 semaines légales + double pécule)

5. CONTACTS CLÉS
   - Responsable direct
   - Service RH / secrétariat social
   - IT support
   - Contact d'urgence entreprise

Ton : bienveillant, clair, structuré. Donne envie à l'employé de s'engager dès le premier jour."""

    resultat = streamer(prompt, "KIT ONBOARDING EMPLOYÉ BELGE")
    sauvegarder("kit_onboarding", resultat)

def lettre_evaluation_performance():
    print("\n  — Lettre d'évaluation de performance —")
    nom_employe = sanitize(input("  Nom de l'employé : "))
    periode = sanitize(input("  Période évaluée (ex: 2024, S1 2025) : "))
    realisations = sanitize(input("  Principales réalisations et points positifs : "))
    axes_amelioration = sanitize(input("  Axes d'amélioration identifiés : "))
    objectifs_suivants = sanitize(input("  Objectifs pour la prochaine période : "))

    prompt = f"""Génère une lettre d'évaluation de performance professionnelle pour un employé belge.

DONNÉES :
- Employé : {nom_employe}
- Période évaluée : {periode}
- Réalisations : {realisations}
- Axes d'amélioration : {axes_amelioration}
- Objectifs prochaine période : {objectifs_suivants}

LIVRABLES :

1. LETTRE D'ÉVALUATION DE PERFORMANCE
   - En-tête professionnel (date, destinataire, objet)
   - Introduction : contexte de l'entretien annuel d'évaluation
   - SECTION A — BILAN DE LA PÉRIODE {periode}
     · Réalisations et points forts valorisés positivement
     · Contribution à l'équipe et à l'entreprise
     · Respect des objectifs fixés lors de l'évaluation précédente
   - SECTION B — POINTS D'AMÉLIORATION
     · Axes de développement identifiés (formulés de manière constructive et non accusatoire)
     · Obstacles rencontrés et analyse bienveillante
   - SECTION C — OBJECTIFS POUR LA PROCHAINE PÉRIODE
     · 3 à 5 objectifs SMART (Spécifiques, Mesurables, Atteignables, Réalistes, Temporels)
     · Moyens mis à disposition par l'employeur (formation, accompagnement)
   - SECTION D — RÉMUNÉRATION ET ÉVOLUTION (si applicable)
     · Mention d'une révision salariale éventuelle ou perspectives d'évolution
   - Conclusion positive et encourageante
   - Signatures (employeur et employé — pour validation de la lecture)

2. FICHE DE SUIVI DES OBJECTIFS
   - Tableau récapitulatif des objectifs N+1 avec indicateurs de mesure et échéances

Note : cette lettre doit rester bienveillante et constructive. Elle ne constitue pas un document disciplinaire.
Conformité : droit belge du travail, principe de non-discrimination, respect de la vie privée (RGPD)."""

    resultat = streamer(prompt, "LETTRE D'ÉVALUATION DE PERFORMANCE")
    sauvegarder("evaluation_performance", resultat)

def calculer_preavis_licenciement():
    print("\n  — Calculer le préavis de licenciement —")
    anciennete = sanitize(input("  Ancienneté en années (ex: 5.5 pour 5 ans et demi) : "))
    statut = sanitize(input("  Statut (ouvrier / employé / statut unique post-2014) : "))
    date_entree = sanitize(input("  Date d'entrée en service (ex: 01/03/2018) : "))
    contexte = sanitize(input("  Contexte supplémentaire (licenciement / démission / force majeure / etc.) : "))

    prompt = f"""Calcule le préavis de licenciement légal belge et génère un guide complet pour l'employeur.

DONNÉES :
- Ancienneté : {anciennete} ans
- Statut : {statut}
- Date d'entrée en service : {date_entree}
- Contexte : {contexte}

LIVRABLES :

1. CALCUL DU PRÉAVIS LÉGAL (Loi du 26 décembre 2013 — Statut unique)

   RÈGLE GÉNÉRALE (statut unique, applicable depuis le 01/01/2014) :
   Le préavis est calculé en semaines selon les tranches d'ancienneté :
   - De 0 à < 3 mois : 1 semaine
   - De 3 mois à < 6 mois : 3 semaines
   - De 6 mois à < 9 mois : 6 semaines
   - De 9 mois à < 12 mois : 7 semaines
   - De 12 mois à < 15 mois : 8 semaines
   - De 15 mois à < 18 mois : 9 semaines
   - De 18 mois à < 21 mois : 10 semaines
   - De 21 mois à < 24 mois : 11 semaines
   - De 2 ans à < 3 ans : 12 semaines
   - De 3 à < 4 ans : 13 semaines
   - Puis +3 semaines par année supplémentaire complète au-delà de 3 ans

   APPLICATION À CE CAS : {anciennete} ans d'ancienneté
   → Calcul détaillé étape par étape
   → Préavis total en semaines
   → Conversion en jours calendriers et jours ouvrables
   → Date de fin de contrat si préavis débuté aujourd'hui

2. ALTERNATIVE : INDEMNITÉ DE RUPTURE
   - Calcul de l'indemnité compensatoire de préavis (salaire brut × semaines / 4,33)
   - Base de calcul : rémunération brute mensuelle variable incluse
   - Impact social et fiscal de l'indemnité (exonérations éventuelles)

3. PROCÉDURE LÉGALE DE LICENCIEMENT
   □ Motivation de licenciement (CRE — Convention Collective n°109 obligatoire depuis 2014)
   □ Forme du congé : lettre recommandée avec accusé de réception ou exploit d'huissier
   □ Prise de cours du préavis : le lundi suivant la semaine de réception
   □ Documents à remettre à la fin du contrat : C4, fiche de paie finale, certificat de travail, attestation ONSS
   □ Outplacement obligatoire si ancienneté ≥ 30 semaines de préavis

4. RISQUES ET MISES EN GARDE
   - Licenciement manifestement déraisonnable (CRE n°109) : indemnité de 3 à 17 semaines
   - Protections spéciales (délégué syndical, femme enceinte, crédit-temps, etc.)
   - Recommandation de consulter un conseiller social ou avocat spécialisé avant toute action

AVERTISSEMENT : Ce calcul est indicatif. Les cas particuliers (commissions paritaires spécifiques, ancienneté avant 2014) peuvent modifier ce résultat. Consultez un juriste social belge qualifié."""

    resultat = streamer(prompt, "CALCUL PRÉAVIS DE LICENCIEMENT BELGE")
    sauvegarder("preavis_licenciement", resultat)

def kit_prospection_rh_belge():
    prompt = """Génère un kit de prospection commercial complet pour Caelum Partners ciblant les responsables RH et dirigeants de PME belges.

CONTEXTE CAELUM PARTNERS :
- Cabinet d'automatisation IA basé à Bruxelles, fondé par Chaima Mhadbi
- Services : 500 € (starter), 1 500 € (standard), 3 000 € (premium)
- Cible : responsables RH de PME (5-100 salariés) et dirigeants d'entreprises belges
- Secteurs prioritaires : services, construction, commerce, soins de santé, logistique

LIVRABLES :

1. EMAIL DE PROSPECTION (objet + corps complet)
   - Objet : basé sur la douleur principale (conformité Dimona, complexité CCT, temps admin RH)
   - Accroche chiffrée : "Le droit du travail belge a 200+ commissions paritaires. Combien de temps passez-vous sur la documentation RH ?"
   - Argument ROI : package 1 500 € → économie de 15h/mois → valeur 1 500-3 000 €/mois selon salaire RH
   - Cas d'usage concrets : offres d'emploi FR+NL, onboarding, calculs de préavis, évaluations
   - Garantie conformité droit belge (Loi du 26/12/2013, CCT applicables)
   - Call to action : démonstration gratuite de 30 minutes
   - Ton professionnel, direct et empathique face à la complexité RH belge

2. MESSAGE LINKEDIN (300 caractères max)
   - Accroche sur la complexité du droit social belge
   - Proposition de valeur en 2 phrases
   - Call to action

3. CALCUL ROI DÉTAILLÉ POUR CE SECTEUR
   Avant IA (PME 15 salariés) :
   - Rédiger une offre d'emploi FR+NL : 3h → Après IA : 20 min
   - Kit onboarding complet : 2h → Après IA : 15 min
   - Calcul préavis + lettre licenciement : 1,5h → Après IA : 10 min
   - Évaluation annuelle (5 employés) : 5h → Après IA : 45 min
   → Total économisé : ~15h/mois
   → Valeur selon coût RH interne (40-80 €/h) = 600-1 200 €/mois
   → ROI package 1 500 € : rentabilisé en 1 à 2,5 mois

4. RÉPONSES AUX 3 OBJECTIONS PRINCIPALES
   - "Le droit du travail belge est trop complexe pour l'IA"
   - "Nous avons déjà un secrétariat social (Securex, SD Worx)"
   - "Nos documents RH sont déjà standardisés"

5. SCRIPT D'APPEL DE DÉCOUVERTE (2 minutes)
   - Introduction Caelum Partners en 30 secondes
   - 3 questions de qualification (taille équipe, volume recrutements/an, douleur principale)
   - Transition vers démo produit"""

    resultat = streamer(prompt, "KIT PROSPECTION RH BELGE")
    sauvegarder("kit_prospection_rh", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT RH & DROIT DU TRAVAIL BELGE")
    print("  Automatisation documentaire RH — Caelum Partners")
    print("═"*65)
    while True:
        print("\n  [menu]")
        print("  1. Générer une offre d'emploi FR+NL")
        print("  2. Kit onboarding employé")
        print("  3. Lettre d'évaluation performance")
        print("  4. Calculer préavis de licenciement")
        print("  5. Kit prospection RH belge")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            print("  Au revoir.")
            break
        elif choix == "1":
            generer_offre_emploi()
        elif choix == "2":
            kit_onboarding_employe()
        elif choix == "3":
            lettre_evaluation_performance()
        elif choix == "4":
            calculer_preavis_licenciement()
        elif choix == "5":
            kit_prospection_rh_belge()
        else:
            print("  Choix invalide.")
