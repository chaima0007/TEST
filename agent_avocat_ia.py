"""
AGENT ASSISTANCE JURIDIQUE CABINET D'AVOCATS — Automatisation documentaire pour cabinets d'avocats belges
Usage : python agent_avocat_ia.py
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
Tu es un assistant IA spécialisé pour les cabinets d'avocats belges, développé par Caelum Partners (Bruxelles).
La Belgique compte plus de 16 000 avocats inscrits auprès de l'Ordre des barreaux francophones et germanophone (OBFG) et l'Orde van Vlaamse Balies (OVB).
Tu maîtrises parfaitement le système judiciaire belge : Justice de Paix, Tribunal de l'entreprise, Tribunal de première instance, Tribunal du travail, Cour d'appel, Cour de cassation.
Tu connais les types de documents juridiques belges essentiels : mise en demeure, conclusions, convention de cession, protocole de rupture, bail commercial, statuts de société, accord de confidentialité, transaction.
Tu sais rédiger des mises en demeure formelles belges avec les mentions légales exactes, la formulation contraignante et les délais appropriés.
Tu produis des synthèses de dossiers structurées : parties, faits, enjeux juridiques, loi applicable, stratégie recommandée.
Tu génères des checklists de révision de contrats exhaustives avec les clauses clés à vérifier selon le droit belge.
Tu rédiges des lettres clients expliquant leur situation juridique en langage clair et rassurant, sans jargon excessif.
Tu maîtrises les références législatives belges : Code civil belge (nouveau depuis 2022), Code de droit économique, Code judiciaire, Code pénal, Code des sociétés et des associations (CSA).
Un avocat belge facture entre 150 € et 350 €/heure selon sa spécialité. Économiser 10h/mois grâce à l'IA représente 1 500 à 3 500 €/mois de gains de productivité.
Le package Caelum à 3 000 € premium est le plus adapté aux cabinets d'avocats : ROI le plus élevé du portefeuille Caelum.
Les avocats ne peuvent pas être remplacés par l'IA pour le conseil juridique et la représentation en justice : l'IA les assiste dans la préparation documentaire.
Tu cites systématiquement les textes de loi belges applicables avec leur numérotation exacte (articles, alinéas).
Tu adaptes le registre de langue : juridique rigoureux pour les documents officiels, clair et accessible pour les communications clients.
Tu connais les délais de prescription belges : droit commun 10 ans (Art. 2262bis ancien Code civil), nouveau Code civil 5 ans, délais spéciaux selon matière.
Tu es orienté vers la création de valeur commerciale pour Caelum Partners dans ce segment à forte valeur ajoutée.
Tu intègres systématiquement le disclaimer légal obligatoire dans chaque document produit.
Tu connais les procédures de recouvrement belges : injonction de payer (Art. 1338 Code judiciaire), saisie conservatoire, procédure en référé pour urgence.
"""

DISCLAIMER = "\n\n---\n⚠️  DISCLAIMER : Ce document est préparé par IA (Caelum Partners) à des fins de référence uniquement. Il doit impérativement être validé par un avocat qualifié inscrit au barreau avant tout usage juridique, dépôt en justice ou envoi à une partie adverse."

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
    os.makedirs("fichiers/avocat_ia", exist_ok=True)
    fichier = f"fichiers/avocat_ia/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu + DISCLAIMER)
    print(f"  ✅ Sauvegardé → {fichier}")

def rediger_mise_en_demeure():
    print("\n  — Rédiger une mise en demeure —")
    expediteur = sanitize(input("  Expéditeur (nom / société / qualité) : "))
    destinataire = sanitize(input("  Destinataire (nom / société / adresse) : "))
    objet_litige = sanitize(input("  Objet du litige (non-paiement / inexécution / violation contrat / etc.) : "))
    montant = sanitize(input("  Montant réclamé (€) ou objet précis de la demande : "))
    delai = sanitize(input("  Délai accordé pour régularisation (ex: 8 jours, 15 jours) : "))
    contexte = sanitize(input("  Contexte et faits supplémentaires : "))

    prompt = f"""Rédige une mise en demeure formelle et juridiquement rigoureuse selon le droit belge.

DONNÉES :
- Expéditeur : {expediteur}
- Destinataire : {destinataire}
- Objet du litige : {objet_litige}
- Montant / objet réclamé : {montant}
- Délai accordé : {delai}
- Contexte : {contexte}

STRUCTURE DE LA MISE EN DEMEURE :

1. EN-TÊTE OFFICIEL
   - Lieu et date
   - Expéditeur complet (nom, adresse, téléphone, email)
   - Destinataire complet (nom, adresse)
   - Objet : "MISE EN DEMEURE — [objet]"
   - Mention "Lettre recommandée avec accusé de réception" (ou exploit d'huissier si applicable)

2. CORPS DE LA MISE EN DEMEURE
   A. RAPPEL DES FAITS
      - Exposé chronologique et factuel des événements
      - Références aux contrats, factures, correspondances antérieures (numéros fictifs à remplacer)

   B. FONDEMENT JURIDIQUE
      - Obligations contractuelles et légales du destinataire
      - Références légales belges exactes : Art. 1244 du Code civil belge (anc.) ou articles pertinents du nouveau Code civil (Livre 5), Code de droit économique si applicable
      - Loi sur les intérêts de retard en B2B si applicable (Loi du 2/08/2002)

   C. MISE EN DEMEURE FORMELLE
      - Formulation contraignante et sans ambiguïté
      - Somme ou prestation réclamée avec précision
      - Délai de {delai} à compter de la réception de la présente lettre
      - Intérêts de retard applicables (taux légal ou contractuel)

   D. CONSÉQUENCES EN CAS DE NON-EXÉCUTION
      - Procédures judiciaires envisagées (citation en justice, référé, saisie)
      - Frais et dépens à charge du destinataire
      - Réserve de tous droits et actions

3. FORMULE DE CONCLUSION
   - Maintien en attente d'une régularisation amiable
   - Coordonnées pour contact immédiat
   - Formule de politesse ferme mais professionnelle
   - Signature

4. LISTE DES PIÈCES JOINTES RECOMMANDÉES
   - Documents à annexer pour renforcer la mise en demeure

Ton : ferme, précis, professionnel. Pas d'émotion, uniquement des faits et du droit."""

    resultat = streamer(prompt, "MISE EN DEMEURE FORMELLE BELGE")
    sauvegarder("mise_en_demeure", resultat)

def synthese_dossier():
    print("\n  — Synthèse de dossier juridique —")
    description = sanitize(input("  Décris le dossier (parties, faits, enjeux, documents disponibles) : "))

    prompt = f"""Génère une synthèse structurée de dossier juridique belge pour usage interne d'un cabinet d'avocats.

DESCRIPTION DU DOSSIER : {description}

STRUCTURE DE LA SYNTHÈSE :

1. FICHE D'IDENTIFICATION DU DOSSIER
   - Référence dossier (à compléter)
   - Date d'ouverture
   - Avocat référent (à compléter)
   - Type de contentieux : [civil / commercial / social / pénal / administratif]

2. PARTIES
   - CLIENT / PARTIE DEMANDERESSE : identification, qualité, coordonnées
   - PARTIE ADVERSE / DÉFENDERESSE : identification, qualité, représentation connue
   - Tiers éventuels : intervenants, garants, assureurs

3. EXPOSÉ DES FAITS (chronologique)
   - Timeline des événements clés avec dates précises
   - Documents existants et leur pertinence
   - Points factuels établis vs points contestés

4. ENJEUX JURIDIQUES
   - Question(s) de droit principale(s) à trancher
   - Fondements légaux applicables (textes et articles exacts du droit belge)
   - Jurisprudence pertinente éventuelle (à rechercher et compléter)
   - Délais de prescription applicables

5. ANALYSE DE LA POSITION DU CLIENT
   - Forces du dossier
   - Faiblesses et risques identifiés
   - Éléments de preuve disponibles / manquants

6. STRATÉGIE RECOMMANDÉE
   - Option 1 : Voie amiable / négociation (avantages, délai estimé)
   - Option 2 : Procédure judiciaire (juridiction compétente, délais, coûts estimés)
   - Recommandation principale motivée

7. PROCHAINES ÉTAPES ET ACTIONS À MENER
   □ Documents à collecter ou requérir
   □ Courriers à rédiger
   □ Délais à respecter impérativement
   □ Expertises ou avis tiers à solliciter

Format : note interne confidentielle, directement classable dans le logiciel de gestion du cabinet."""

    resultat = streamer(prompt, "SYNTHÈSE DE DOSSIER JURIDIQUE")
    sauvegarder("synthese_dossier", resultat)

def checklist_contrat():
    print("\n  — Checklist de révision de contrat —")
    type_contrat = sanitize(input("  Type de contrat (bail commercial / cession de fonds / NDA / contrat de service / statuts SRL / etc.) : "))
    contexte = sanitize(input("  Contexte particulier ou points d'attention signalés par le client : "))

    prompt = f"""Génère une checklist exhaustive de révision de contrat belge pour un avocat d'affaires.

TYPE DE CONTRAT : {type_contrat}
CONTEXTE : {contexte}

STRUCTURE DE LA CHECKLIST :

1. VÉRIFICATIONS PRÉLIMINAIRES
   □ Identité et capacité juridique des parties (personnes physiques : pleine capacité ; sociétés : pouvoirs du signataire selon statuts et extrait BCE)
   □ Forme du contrat requise (acte authentique / seing privé / électronique)
   □ Loi applicable et clause de juridiction
   □ Date de prise d'effet et durée

2. CLAUSES ESSENTIELLES À VÉRIFIER (spécifiques à "{type_contrat}")
   □ Objet du contrat : définition précise et non ambiguë
   □ Prix / contrepartie : montant, TVA, modalités et délais de paiement
   □ Obligations principales de chaque partie : clairement délimitées
   □ Conditions suspensives / résolutoires éventuelles
   □ Garanties accordées et leur étendue
   □ Transfert de propriété / risques (pour contrats de vente)
   □ Droits de propriété intellectuelle si applicable
   □ Clause de confidentialité et durée de l'obligation

3. CLAUSES DE PROTECTION À INSÉRER OU VÉRIFIER
   □ Clause pénale (Art. 5.246 nouveau Code civil belge) : montant raisonnable
   □ Clause d'exonération de responsabilité et ses limites légales
   □ Clause de force majeure (Art. 5.225-5.228 nouveau Code civil) : définition précise
   □ Clause de résiliation anticipée : conditions, délais, indemnités
   □ Clause de renégociation (hardship — Art. 5.74 nouveau Code civil)
   □ Clause d'intérêts moratoires (taux légal ou conventionnel)
   □ Clause de cession du contrat à des tiers

4. RED FLAGS — CLAUSES ABUSIVES OU DANGEREUSES
   □ Clauses limitant excessivement la responsabilité d'une partie
   □ Clauses déséquilibrées (B2C : protections renforcées Livre VI CDE)
   □ Pénalités disproportionnées ou clauses pénales manifestement déraisonnables
   □ Renonciations à des droits impératifs (garanties légales, délais légaux)
   □ Clauses contraires aux lois d'ordre public belges

5. VÉRIFICATIONS FINALES
   □ Cohérence interne du document (pas de contradiction entre articles)
   □ Définitions utilisées de manière uniforme tout au long
   □ Annexes référencées et effectivement jointes
   □ Paraphes sur chaque page et signatures complètes en dernière page
   □ Nombre d'exemplaires originaux (autant que de parties)
   □ Enregistrement fiscal si requis (ex: bail commercial — délai 4 mois)

6. POINTS SPÉCIFIQUES AU DROIT BELGE
   - Références aux articles du Code civil belge (nouveau depuis le 01/01/2023)
   - Lois spéciales applicables selon le type de contrat
   - Jurisprudence de la Cour de cassation belge à consulter si litige prévisible"""

    resultat = streamer(prompt, f"CHECKLIST RÉVISION — {type_contrat.upper()}")
    sauvegarder("checklist_contrat", resultat)

def lettre_client_juridique():
    print("\n  — Lettre client juridique —")
    nom_client = sanitize(input("  Nom du client : "))
    situation = sanitize(input("  Situation à expliquer au client (update de dossier, décision judiciaire, stratégie, etc.) : "))
    prochaines_etapes = sanitize(input("  Prochaines étapes à communiquer : "))

    prompt = f"""Génère une lettre professionnelle d'un cabinet d'avocats belge à son client pour l'informer de l'évolution de son dossier.

CLIENT : {nom_client}
SITUATION / UPDATE : {situation}
PROCHAINES ÉTAPES : {prochaines_etapes}

LIVRABLES :

1. LETTRE CLIENT EN LANGAGE CLAIR
   - En-tête professionnel du cabinet (coordonnées fictives)
   - Référence dossier et date
   - Introduction rassurante et professionnelle
   - SECTION A — ÉTAT ACTUEL DU DOSSIER
     · Résumé de la situation en langage accessible (pas de jargon juridique inutile)
     · Ce qui s'est passé depuis la dernière communication
     · Décision, acte de procédure ou développement récent expliqué clairement
   - SECTION B — ANALYSE ET IMPLICATIONS POUR LE CLIENT
     · Ce que cela signifie concrètement pour le client
     · Risques actuels et mesures prises pour les limiter
     · Opportunités éventuelles identifiées
   - SECTION C — PROCHAINES ÉTAPES
     · Actions à entreprendre par l'avocat (délais précis)
     · Ce que le client doit faire ou fournir
     · Calendrier prévisionnel
   - SECTION D — HONORAIRES ET PROVISION
     · Si applicable : rappel des honoraires en cours ou provision nécessaire
   - Formule de conclusion rassurante avec disponibilité pour questions
   - Signature

2. VERSION EMAIL COURTE (même contenu, format synthétique)
   - Objet percutant
   - Corps en 3 paragraphes maximum

Style : professionnel, rassurant, clair. Le client doit sortir de cette lettre en comprenant exactement où en est son dossier et ce qu'on attend de lui."""

    resultat = streamer(prompt, "LETTRE CLIENT JURIDIQUE")
    sauvegarder("lettre_client_juridique", resultat)

def kit_prospection_cabinets():
    prompt = """Génère un kit de prospection commercial complet pour Caelum Partners ciblant les cabinets d'avocats belges.

CONTEXTE CAELUM PARTNERS :
- Cabinet d'automatisation IA basé à Bruxelles, fondé par Chaima Mhadbi
- Services : 500 € (starter), 1 500 € (standard), 3 000 € (premium)
- Cible : cabinets d'avocats belges (boutiques 2-10 avocats et cabinets mid-size)
- Offre phare : package 3 000 € premium — le plus rentable du portefeuille Caelum
- 16 000+ avocats inscrits aux barreaux belges

LIVRABLES :

1. EMAIL DE PROSPECTION PREMIUM (objet + corps complet)
   - Objet : basé sur la douleur principale (volume documentaire, pression des délais, rentabilité par heure)
   - Accroche ROI immédiate : "Un avocat belge perd en moyenne 10h/mois sur la rédaction de documents de référence. À 200 €/h, ça représente 2 000 €/mois."
   - Positionnement premium : Caelum n'est pas un outil généraliste — c'est une solution juridique belge spécialisée
   - Cas d'usage concrets : mises en demeure, synthèses de dossier, checklists contrats, lettres clients
   - Respect déontologie : l'IA prépare, l'avocat valide et signe — conformité OBFG/OVB
   - Call to action : démonstration gratuite d'1 heure (plus long = plus de valeur perçue)
   - Ton : B2B haut de gamme, sobre, sans fioriture marketing

2. MESSAGE LINKEDIN AVOCAT (300 caractères max)
   - Accroche sur la productivité juridique
   - Mention du ROI chiffré
   - Call to action élégant

3. CALCUL ROI DÉTAILLÉ — CABINET D'AVOCATS
   Avant IA (cabinet de 3 avocats, 60 dossiers actifs) :
   - Mise en demeure : 1,5h → Après IA : 15 min
   - Synthèse dossier : 2h → Après IA : 20 min
   - Checklist révision contrat : 1h → Après IA : 10 min
   - Lettre client d'update : 45 min → Après IA : 8 min
   → Économie par avocat : 8-12h/mois
   → Gain pour 3 avocats à 200 €/h : 4 800-7 200 €/mois
   → ROI package 3 000 € Caelum : rentabilisé en moins de 15 jours

4. RÉPONSES AUX 3 OBJECTIONS SPÉCIFIQUES AVOCATS
   - "Le secret professionnel interdit l'utilisation d'IA avec des données clients"
   - "Les barreaux belges n'ont pas encore statué sur l'IA en droit"
   - "Nos documents sont trop spécifiques pour être automatisés"

5. SCRIPT DÉMO GRATUITE D'1 HEURE (structure complète)
   - 0-10 min : Découverte des besoins du cabinet
   - 10-35 min : Démonstration live (mise en demeure + synthèse dossier)
   - 35-50 min : Personnalisation selon le type de pratique du cabinet
   - 50-60 min : Présentation de l'offre et gestion des objections

6. OFFRE DE LANCEMENT RECOMMANDÉE POUR CE SEGMENT
   - Proposition tarifaire optimale
   - Conditions de démarrage
   - Garantie satisfaction"""

    resultat = streamer(prompt, "KIT PROSPECTION CABINETS D'AVOCATS BELGES")
    sauvegarder("kit_prospection_avocats", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT ASSISTANCE JURIDIQUE — CABINET D'AVOCATS")
    print("  Automatisation documentaire — Caelum Partners")
    print("═"*65)
    while True:
        print("\n  [menu]")
        print("  1. Rédiger une mise en demeure")
        print("  2. Synthèse de dossier")
        print("  3. Checklist revue de contrat")
        print("  4. Lettre client juridique")
        print("  5. Kit prospection cabinets d'avocats")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            print("  Au revoir.")
            break
        elif choix == "1":
            rediger_mise_en_demeure()
        elif choix == "2":
            synthese_dossier()
        elif choix == "3":
            checklist_contrat()
        elif choix == "4":
            lettre_client_juridique()
        elif choix == "5":
            kit_prospection_cabinets()
        else:
            print("  Choix invalide.")
